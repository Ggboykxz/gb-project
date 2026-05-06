"""
Script seed minimal pour GabonEdu Campus - Version simplifiée
"""
import sys
import os

sys.path.insert(0, '.')

# Create database path
if os.name == 'nt':
    APP_DATA = os.path.join(os.environ.get('APPDATA', ''), 'gabon_edu')
else:
    APP_DATA = os.path.join(os.path.expanduser('~'), '.local', 'share', 'gabon_edu')
os.makedirs(APP_DATA, exist_ok=True)
DB_PATH = os.path.join(APP_DATA, 'campus.db')

# Remove old db
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

import sqlite3
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create users table with same schema as models
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    role TEXT NOT NULL,
    telephone TEXT,
    is_active INTEGER DEFAULT 1,
    is_verified INTEGER DEFAULT 0,
    totp_secret TEXT,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create admin user
import uuid
admin_id = str(uuid.uuid4())
password = "admin123"

# Use passlib to hash password
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
hashed_password = pwd_context.hash(password)

cursor.execute(
    "INSERT INTO users (id, email, hashed_password, nom, prenom, role, is_active) VALUES (?, ?, ?, ?, ?, ?, ?)",
    (admin_id, "admin@cuk.ga", hashed_password, "ADMIN", "Super", "SUPER_ADMIN", 1)
)

conn.commit()
conn.close()

print("Base creee: " + DB_PATH)
print("Utilisateur admin: admin@cuk.ga / admin123")