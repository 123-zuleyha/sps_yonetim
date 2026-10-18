# database.py
import mysql.connector
from mysql.connector import Error
import bcrypt
from config import DB_CONFIG

def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        print(f"Veritabanı bağlantı hatası: {e}")
        return None

def check_user(email, password):
    """Kullanıcı doğrulama - email ile giriş"""
    conn = get_connection()
    if not conn:
        return None
    
    cursor = conn.cursor(dictionary=True)
    
    # Email ile kullanıcı sorgula
    query = """
        SELECT 
            k.kullanici_id as id,
            k.email as kullanici_adi,
            k.sifre,
            k.aktif_mi,
            k.ilgili_kisi_id,
            r.rol_adi as rol
        FROM kullanici k
        LEFT JOIN rol r ON k.rol_id = r.rol_id
        WHERE k.email = %s AND k.aktif_mi = 1 AND k.is_deleted = 0
    """
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    if user:
        # Şifre kontrolü
        if bcrypt.checkpw(password.encode('utf-8'), user['sifre'].encode('utf-8')):
            # İlgili kişi bilgilerini de al
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ad, soyad, unvan, telefon, email as kisi_email
                FROM ilgili_kisi
                WHERE ilgili_kisi_id = %s
            """, (user['ilgili_kisi_id'],))
            kisi = cursor.fetchone()
            cursor.close()
            conn.close()
            
            if kisi:
                user['ad_soyad'] = f"{kisi['ad']} {kisi['soyad']}"
                user['ad'] = kisi['ad']
                user['soyad'] = kisi['soyad']
                user['unvan'] = kisi['unvan']
                user['telefon'] = kisi['telefon']
            else:
                user['ad_soyad'] = user['kullanici_adi']
            
            return user
    
    return None

def test_connection():
    conn = get_connection()
    if conn:
        print("✓ Veritabanı bağlantısı başarılı!")
        conn.close()
        return True
    else:
        print("✗ Veritabanı bağlantısı başarısız!")
        return False