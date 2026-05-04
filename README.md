# 🚀 Guide de Démarrage - GabonEdu Campus

## Prérequis

### Système
- **Windows 10/11** ou **macOS 12+** ou **Linux (Ubuntu 22.04+)**
- **Node.js 18+** : `https://nodejs.org`
- **Python 3.12+** : `https://python.org`
- **Rust** : `https://rustup.rs`

### Installation des dépendances

```bash
# 1. Installer les dépendances Node.js
cd /workspace
npm install

# 2. Installer les dépendances Python
cd backend
pip install -r requirements.txt

# 3. Installer Tauri CLI
cargo install tauri-cli
```

## Développement

### Lancer en mode développement

```bash
# Terminal 1 : Lancer le backend Python (optionnel, Tauri le gère)
cd backend
python main.py --port 8765

# Terminal 2 : Lancer l'application Tauri
cd /workspace
npm run tauri dev
```

L'application s'ouvrira automatiquement avec :
- Frontend Vue 3 sur `http://localhost:5173`
- Backend FastAPI sur `http://127.0.0.1:8765`
- Base de données SQLite dans `AppData/gabon_edu/campus.db`

## Build Production

### 1. Build du sidecar Python

```bash
# Windows
.\build-sidecar.ps1

# macOS/Linux
./build-sidecar.sh
```

### 2. Build de l'application Tauri

```bash
# Build complet (MSI/DMG/AppImage)
npm run tauri build

# Les installateurs seront dans :
# - Windows : src-tauri/target/release/bundle/msi/
# - macOS : src-tauri/target/release/bundle/dmg/
# - Linux : src-tauri/target/release/bundle/appimage/
```

## Comptes de Test

Après avoir exécuté le seed (`python backend/seed.py`), utilisez :

| Rôle | Email | Mot de passe |
|------|-------|-------------|
| Super Admin | `admin@gabonedu.ga` | `Gabon2024!` |
| Scolarité | `scolarite@cuk.ga` | `Gabon2024!` |
| Enseignant | `prof@cuk.ga` | `Gabon2024!` |
| Étudiant | `etudiant@cuk.ga` | `Gabon2024!` |
| Financier | `finance@cuk.ga` | `Gabon2024!` |

## Architecture

```
┌─────────────────────────────────────────┐
│         GabonEdu Campus (Tauri)         │
│  ┌───────────────────────────────────┐  │
│  │      Frontend Vue 3 + TS          │  │
│  │  - Components Shadcn/Tailwind     │  │
│  │  - Pinia Stores                   │  │
│  │  - Vue Router                     │  │
│  └─────────────┬─────────────────────┘  │
│                │ HTTP (localhost:8765)  │
│  ┌─────────────▼─────────────────────┐  │
│  │    Sidecar Python FastAPI         │  │
│  │  - SQLAlchemy ORM                 │  │
│  │  - JWT Auth                       │  │
│  │  - Business Logic                 │  │
│  └─────────────┬─────────────────────┘  │
│                │ SQLite                 │
│  ┌─────────────▼─────────────────────┐  │
│  │   SQLite DB (chiffrée)            │  │
│  │   - AppData/campus.db             │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

## Structure du Projet

```
gabon-edu-campus/
├── src/                  # Frontend Vue 3
│   ├── components/       # Composants UI
│   ├── views/           # Pages par module
│   ├── stores/          # Pinia stores
│   ├── router/          # Routes protégées
│   └── lib/             # Utils & API client
├── src-tauri/           # Shell Rust Tauri
│   ├── src/main.rs      # Point d'entrée + sidecar
│   └── tauri.conf.json  # Configuration
├── backend/             # Sidecar Python
│   ├── main.py          # Entry point FastAPI
│   ├── models/          # Modèles SQLAlchemy
│   ├── schemas/         # Schémas Pydantic
│   ├── routers/         # Endpoints API
│   ├── services/        # Business logic
│   └── security/        # Auth & permissions
├── tests/               # Tests pytest & Vitest
└── scripts/             # Scripts utilitaires
```

## Modules Implémentés

✅ **Administration Académique**
- Gestion des étudiants & inscriptions
- Filières & maquettes pédagogiques (LMD)
- Notes & délibérations
- Emplois du temps

✅ **Vie Étudiante**
- Portfolio numérique
- Bourses & aides sociales
- Stages & emplois
- Réseau Alumni

✅ **Gestion Financière**
- Facturation & recouvrement
- Budget & comptabilité OHADA
- Ressources humaines
- Patrimoine

✅ **Sécurité**
- Authentification JWT + 2FA TOTP
- RBAC (permissions granulaires)
- Journal d'audit
- Chiffrement des données

## Synchronisation Offline

L'application fonctionne 100% hors-ligne. La synchronisation avec un serveur central se fait :
- Manuellement via le "Centre de synchronisation"
- Automatiquement lors de la détection de connexion

Les données sont stockées localement dans une base SQLite chiffrée.

## Dépannage

### Le backend ne démarre pas
```bash
# Vérifier que Python 3.12 est installé
python --version

# Vérifier les dépendances
pip install -r backend/requirements.txt

# Lancer manuellement pour voir les erreurs
cd backend
python main.py --port 8765
```

### Erreur de compilation Rust
```bash
# Mettre à jour Rust
rustup update

# Nettoyer et rebuild
cd src-tauri
cargo clean
cd ..
npm run tauri build
```

### Base de données corrompue
```bash
# Supprimer la DB et re-seeder
rm -rf $APPDATA/gabon_edu/campus.db
python backend/seed.py
```

## Licence

© 2024 GabonEdu - Centre Universitaire de Koulamoutou (CUK/USTM)

---

*"Une université connectée, même sans connexion."*
