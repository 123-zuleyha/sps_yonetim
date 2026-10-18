# test_login.py
import bcrypt
import mysql.connector
from config import DB_CONFIG

def test_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def test_user():
    conn = test_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Kullanıcıyı bul
    email = "admin@sps.com"
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
    
    if user:
        print("✅ Kullanıcı bulundu:")
        print(f"   ID: {user['id']}")
        print(f"   Email: {user['kullanici_adi']}")
        print(f"   Rol: {user['rol']}")
        print(f"   Aktif mi: {user['aktif_mi']}")
        print(f"   İlgili kişi ID: {user['ilgili_kisi_id']}")
        print(f"   Şifre hash (ilk 30 karakter): {user['sifre'][:30]}...")
        
        # Şifre kontrolü
        test_password = "admin123"
        try:
            if bcrypt.checkpw(test_password.encode('utf-8'), user['sifre'].encode('utf-8')):
                print("   ✅ Şifre DOĞRU!")
            else:
                print("   ❌ Şifre YANLIŞ!")
        except Exception as e:
            print(f"   ❌ Şifre kontrol hatası: {e}")
            print(f"   Hash değeri: {user['sifre']}")
    else:
        print("❌ Kullanıcı bulunamadı!")
        
        # Tüm kullanıcıları listele
        cursor.execute("SELECT kullanici_id, email, aktif_mi, is_deleted FROM kullanici")
        all_users = cursor.fetchall()
        print("\n📋 Veritabanındaki tüm kullanıcılar:")
        for u in all_users:
            print(f"   ID: {u['kullanici_id']}, Email: {u['email']}, Aktif: {u['aktif_mi']}, Silindi: {u['is_deleted']}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    test_user()