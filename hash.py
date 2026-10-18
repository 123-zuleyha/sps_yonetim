import bcrypt

# Şifreniz
password = "admin123"

# Hash oluştur
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print("Hash:", hashed.decode())