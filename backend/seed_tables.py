"""
Ajout des tables supplémentaires pour le backend
"""
import sys
import os

sys.path.insert(0, '.')

# Database path
if os.name == 'nt':
    APP_DATA = os.path.join(os.environ.get('APPDATA', ''), 'gabon_edu')
else:
    APP_DATA = os.path.join(os.path.expanduser('~'), '.local', 'share', 'gabon_edu')
DB_PATH = os.path.join(APP_DATA, 'campus.db')

import sqlite3
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create etudiants table
cursor.execute('''
CREATE TABLE IF NOT EXISTS etudiants (
    id TEXT PRIMARY KEY,
    nip_gabon TEXT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    date_naissance DATE,
    genre TEXT,
    nationalite TEXT,
    telephone TEXT,
    email TEXT,
    photo_url TEXT,
    adresse TEXT,
    statut TEXT DEFAULT 'actif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create filieres table
cursor.execute('''
CREATE TABLE IF NOT EXISTS filieres (
    id TEXT PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,
    libelle TEXT NOT NULL,
    domaine TEXT,
    niveau TEXT,
    duree_annees INTEGER,
    responsable_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create sessions table for security
cursor.execute('''
CREATE TABLE IF NOT EXISTS sessions_utilisateurs (
    id TEXT PRIMARY KEY,
    utilisateur_id TEXT NOT NULL,
    jeton_refresh TEXT,
    date_connexion TIMESTAMP,
    adresse_ip TEXT,
    statut TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# Create tentatives_connexion table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tentatives_connexion (
    id TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    adresse_ip TEXT,
    succes INTEGER,
    date_essai TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
conn.close()

print("Tables supplémentaires créées")