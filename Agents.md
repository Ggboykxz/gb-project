# Agents.md - GabonEdu Campus

Instructions pour les agents IA travaillant sur le projet GabonEdu Campus.

## Structure du Projet

```
gabon-edu-campus/
├── src/                    # Frontend Vue 3 + TypeScript
│   ├── api/               # Client API vers FastAPI
│   ├── components/        # Composants UI
│   ├── lib/               # Utils
│   ├── router/            # Routes Vue Router
│   ├── stores/            # Pinia stores
│   ├── styles.css         # Styles Tailwind
│   ├── views/             # Pages principales
│   ├── App.vue
│   └── main.ts
├── src-tauri/             # Shell Rust Tauri
│   ├── src/main.rs        # Point d'entrée + sidecar Python
│   ├── tauri.conf.json    # Configuration
│   └── Cargo.toml
├── backend/               # Sidecar Python FastAPI
│   ├── main.py            # Entry point
│   ├── database.py        # Configuration DB
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── routers/           # Endpoints API
│   ├── services/          # Business logic
│   ├── security/          # Auth & permissions
│   └── seed.py            # Données de test
└── dist/                  # Build frontend
```

## Commandes de Développement

### Frontend (Vue 3 + Vite)
```bash
npm run dev          # Lancer le dev server
npm run build        # Build production
npm run preview      # Preview build
```

### Backend (FastAPI)
```bash
cd backend
python -m uvicorn main:app --reload --port 8765
python seed.py       # Reinitialiser les donnees de test
```

### Tauri
```bash
npm run tauri dev    # Dev mode avec Tauri
npm run tauri build  # Build production
```

## Règles de Commit (1 modification = 1 commit + 1 push)

### Workflow obligatoire
1. Faire la modification/correction
2. Tester que ca fonctionne
3. Commiter avec un message descriptif
4. Pusher immediatement

### Format des messages de commit
```
[type]: description courte

- Detail 1
- Detail 2
```

Types: `fix:`, `feat:`, `docs:`, `refactor:`, `test:`, `chore:`

### Exemple
```bash
git add .
git commit -m "fix: correction FK Candidature dans vie_etudiante.py

- Corrigé 'offres_stages_emplos' -> 'offres_stages_emplois'
- Supprimé colonne inexistante de la DB
- Testé avec seed.py"
git push
```

## Modèles de Données - Conventions

### Nommage des tables (snake_case)
- `users`, `etudiants`, `filieres`, `ues`, `inscriptions`, `paiements`

### Enums (UPPER_CASE)
- Roles: `SUPER_ADMIN`, `ADMIN_SCOL`, `ENSEIGNANT`, `ETUDIANT`, `FINANCIER`, `BIBLIOTHECAIRE`, `CHERCHEUR`
- Statuts: `ACTIF`, `SUSPENDU`, `EXCLU`, `CONFIRME`, `SOUMIS`, `VALIDE_SCOL`
- Types: `NOUVEAU`, `REINSCRIPTION`, `MOBILE_MONEY`, `VIREMENT`

### Champs model User
```python
id, email, nom, prenom, telephone, hashed_password, role (enum Role),
is_active, is_verified, totp_secret, totp_enabled, created_at, updated_at, last_login, metadata_json
```

### Champs model Etudiant
```python
id, nip_gabon, nom, prenom, date_naissance, genre, nationalite, telephone, email, photo_url, statut (enum StatutEtudiant)
```

### Champs model Inscription
```python
id, etudiant_id, filiere_id, annee_academique, niveau, type_inscription, statut_workflow (enum StatutInscription),
date_soumission, documents_json, frais_payes, montant_paye
```

### Champs model Salle
```python
id, nom, capacite, type_salle (enum TypeSalle), equipements_json, batiment, disponible
```

### Champs model FraisScolarite
```python
id, filiere_id, annee_academique, niveau, montant_inscription, montant_scolarite, echeancier_json
```

### Champs model Paiement
```python
id, inscription_id, montant, date_paiement, mode_paiement, reference_transaction, operateur, recu_url, saisi_par
```

## Tests et Validation

### Verifier import FastAPI
```bash
cd backend && python -c "from main import app; print('OK')"
```

### Verifier seed
```bash
cd backend && rm -f ~/.local/share/gabon_edu/campus.db && python seed.py
```

### Verifier build frontend
```bash
npm run build
```

## Credentials de Test

| Role | Email | Mot de passe |
|------|-------|-------------|
| Super Admin | superadmin@cuk.ga | Gabon2024! |
| Scolarité | scolarite@cuk.ga | Gabon2024! |
| Enseignant | enseignant@cuk.ga | Gabon2024! |
| Étudiant | etudiant.demo@cuk.ga | Gabon2024! |
| Financier | financier@cuk.ga | Gabon2024! |

## Notes Importantes

- Le backend utilise SQLite avec aiosqlite (async)
- La base est dans `~/.local/share/gabon_edu/campus.db` (Linux)
- Port API: 8765 (localhost uniquement)
- JWT auth avec argon2 pour les mots de passe