# 🎓 GabonEdu Campus — Super-Prompt OpenCode
> Application desktop tout-en-un pour la gestion académique, administrative et pédagogique des universités gabonaises. Offline-first. Alignée Gabon Digital.

---

## ⚙️ STACK TECHNIQUE DÉFINITIVE

| Couche | Technologie |
|---|---|
| Shell desktop | **Tauri 2.0** (Rust) → .msi Windows / .dmg macOS |
| Frontend | **Vue 3 + TypeScript + TailwindCSS v3 + Pinia** |
| UI Components | **Shadcn-vue + Lucide Icons** |
| Backend local | **Python 3.12 + FastAPI** (sidecar Tauri) |
| ORM | **SQLAlchemy 2.0** (async) |
| Base de données | **SQLite** (chiffré via SQLCipher) |
| PDF/QR | **WeasyPrint + qrcode** |
| Sync | **WebSocket + file d'attente JSON + LZ4** |
| Auth | **JWT (PyJWT) + TOTP 2FA (pyotp)** |
| Tests | **pytest + Vitest** |
| Packaging | **PyInstaller** (sidecar) + **Tauri bundler** |

---

## 🗂️ STRUCTURE DU PROJET

```
gabon-edu-campus/
├── src-tauri/           # Shell Rust Tauri
│   ├── src/main.rs
│   └── tauri.conf.json
├── src/                 # Frontend Vue 3
│   ├── main.ts
│   ├── App.vue
│   ├── router/index.ts
│   ├── stores/          # Pinia stores
│   ├── components/      # Composants UI réutilisables
│   ├── views/           # Pages par module
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── administration/
│   │   ├── etudiants/
│   │   ├── pedagogie/
│   │   ├── recherche/
│   │   └── finances/
│   └── lib/
│       ├── api.ts       # Client HTTP vers FastAPI sidecar
│       └── utils.ts
├── backend/             # Sidecar Python FastAPI
│   ├── main.py
│   ├── database.py
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── routers/         # FastAPI routers par module
│   ├── services/        # Business logic
│   ├── security/
│   └── sync/
├── tests/
└── README.md
```

---

## 🏗️ PHASE 0 — BOOTSTRAP DU PROJET

```
Tu es un expert Tauri 2.0 + Vue 3 + Python FastAPI. Initialise le projet GabonEdu Campus selon ces specs exactes :

1. Crée un projet Tauri 2.0 avec frontend Vue 3 + TypeScript + TailwindCSS v3 + Pinia + Vue Router 4 + shadcn-vue.

2. Configure Tauri pour spawner automatiquement le sidecar Python FastAPI au démarrage de l'app (port 8765 local, liaison 127.0.0.1 uniquement).

3. Crée le backend Python (FastAPI + SQLAlchemy 2.0 async + SQLite via aiosqlite). Le fichier DB est stocké dans AppData (Windows) / Application Support (macOS) sous le chemin {app_data}/gabon_edu/campus.db. Active SQLCipher pour chiffrer la DB avec AES-256.

4. Crée le système de thème Vue avec CSS variables : couleurs primaires #1B4F72 (bleu université), #F39C12 (or gabonais), #27AE60 (vert), fond clair #F8F9FA, fond sombre #1A1D23. Police Geist Mono pour codes/données, Sora pour titres, Inter pour corps de texte.

5. Crée le layout principal avec :
   - Sidebar gauche modulaire (icônes + labels, rétractable)
   - Header avec : nom établissement, utilisateur connecté, statut sync (en ligne/hors ligne), notifications
   - Zone contenu principale avec breadcrumb
   - Footer avec version app + date/heure locale

6. Crée le système d'auth :
   - Écran de login (logo université + champs email/mot de passe + 2FA TOTP optionnel)
   - JWT stocké en mémoire Tauri (pas localStorage)
   - Rôles : SUPER_ADMIN, ADMIN_SCOL, ENSEIGNANT, ETUDIANT, FINANCIER, BIBLIOTHECAIRE, CHERCHEUR
   - Middleware de route Vue Router selon rôle

7. Crée le Dashboard principal adaptatif selon le rôle connecté avec :
   - KPI cards animées (étudiants inscrits, cours actifs, taux de réussite, recettes du mois)
   - Graphiques recharts (évolution inscriptions, répartition filières, taux de présence)
   - Alertes actives (décrochages, retards de paiement, examens à venir)
   - Raccourcis vers actions fréquentes selon le rôle

Fournis tous les fichiers avec leur contenu complet. Aucun placeholder.
```

---

## 🏛️ PHASE 1 — MODULE ADMINISTRATION & GESTION ACADÉMIQUE

```
Module 1 : Administration académique de GabonEdu Campus.

Crée le module complet ADMINISTRATION avec les sous-modules suivants. Tous les formulaires ont validation Zod côté Vue et Pydantic côté FastAPI.

─── 1.1 INSCRIPTIONS & RÉINSCRIPTIONS ───
- Table SQLAlchemy : Etudiant (id, nip_gabon, nom, prenom, date_naissance, genre, nationalite, telephone, email, photo_url, statut)
- Table : Inscription (id, etudiant_id, annee_academique, filiere_id, niveau, type[nouveau/reinscription], statut_workflow[soumis/validé_scol/validé_doyen/confirmé], date_soumission, documents_json, frais_payes)
- Vue liste inscriptions avec filtres (année, filière, statut, recherche texte)
- Formulaire wizard en 4 étapes : Identité → Documents → Choix filière → Paiement
- Workflow de validation hiérarchique avec historique des actions et notifications push Tauri
- Export Excel de la liste des inscrits (openpyxl)
- Impression fiche d'inscription PDF (WeasyPrint, template officiel gabonais)

─── 1.2 GESTION DES PARCOURS ───
- Table : Filiere (id, code, libelle, domaine, niveau[L/M/D], duree_annees, responsable_id)
- Table : UE (id, filiere_id, code_ue, libelle, credits_ects, semestre, heures_cm, heures_td, heures_tp, coefficient, ue_type[obligatoire/optionnel])
- Table : Maquette (id, filiere_id, annee_academique, ues_json, statut[brouillon/validé/archivé])
- Interface drag-and-drop pour construire les maquettes pédagogiques
- Vue grille semestre avec total crédits ECTS calculé automatiquement (alerte si ≠ 60/semestre)
- Historique des versions de maquettes

─── 1.3 EMPLOI DU TEMPS INTELLIGENT ───
- Table : Salle (id, nom, capacite, type[amphi/td/tp/info], equipements_json, batiment, disponible)
- Table : Creneau (id, ue_id, enseignant_id, salle_id, groupe, jour, heure_debut, heure_fin, semaine_type[A/B/toutes], couleur_hex)
- Algorithme de génération automatique : détection de conflits (enseignant/salle/groupe), respect capacités salles, répartition équilibrée
- Vue calendrier hebdomadaire (FullCalendar-like en Vue) avec vue par enseignant/salle/groupe
- Détection et affichage des conflits en rouge avec suggestions de résolution
- Export PDF emploi du temps par filière/enseignant + envoi par email

─── 1.4 NOTES & DÉLIBÉRATIONS ───
- Table : Note (id, inscription_id, ue_id, type_eval[cc/tp/examen], note, absence_justifiee, date_saisie, saisi_par, validee)
- Table : Deliberation (id, filiere_id, annee_academique, semestre, date, jury_json, statut[brouillon/validé/signé], pv_url)
- Grille de saisie des notes (tableau Excel-like éditable, validation 0-20, gestion absences justifiées)
- Calcul automatique : moyenne UE = (note_cc×coeff_cc + note_exam×coeff_exam), moyenne semestre, moyenne annuelle, mention
- Règles LMD gabonaises : validation si moy ≥ 10, compensation inter-UE, rattrapage
- Génération PV de jury PDF signable électroniquement
- Relevé de notes individuel PDF avec QR Code de vérification

─── 1.5 DIPLÔMES & ATTESTATIONS ───
- Table : Diplome (id, etudiant_id, filiere_id, annee_obtention, mention, numero_serie, qr_token[uuid4], date_emission, signe_par)
- Génération PDF diplôme avec template officiel + logo université + QR Code
- Page de vérification en ligne (endpoint public FastAPI : GET /verify/{qr_token})
- Registre numérique centralisé consultable
- Attestations de scolarité, de réussite, d'inscription générées à la demande

Fournis tous les fichiers complets (models, schemas, routers, services Python + composants Vue + stores Pinia).
```

---

## 👨‍🎓 PHASE 2 — MODULE VIE ÉTUDIANTE & SERVICES

```
Module 2 : Vie étudiante et services de GabonEdu Campus.

─── 2.1 PORTFOLIO ÉTUDIANT NUMÉRIQUE ───
- Table : Portfolio (id, etudiant_id, bio, competences_json, langues_json, visibilite[privé/établissement/public])
- Table : ExperiencePortfolio (id, portfolio_id, type[stage/projet/certification/bénévolat], titre, organisation, date_debut, date_fin, description, fichier_url)
- Interface portfolio type LinkedIn (vue carte + vue détail)
- Génération CV PDF automatique à partir du portfolio (template élégant)
- Partage de portfolio par lien sécurisé

─── 2.2 BOURSES & AIDES SOCIALES ───
- Table : TypeBourse (id, libelle, montant_mensuel, criteres_json, quota_annuel, financeur)
- Table : DossierBourse (id, etudiant_id, type_bourse_id, annee, statut, score_social, documents_json, decision, date_decision, commentaire)
- Scoring automatique selon critères (moyenne académique, situation familiale, géographie, handicap)
- Workflow de traitement avec tableau de bord gestionnaire
- Lien avec registre social unique (export/import JSON)
- Historique des attributions

─── 2.3 ORIENTATION & SUIVI PÉDAGOGIQUE ───
- Table : SuiviEtudiant (id, etudiant_id, conseiller_id, type_alerte[décrochage/échec/absence_répétée], statut, notes_suivi_json, date_creation)
- Algorithme de détection de décrochage : absence > 30%, moyenne < 8, 3 notes manquantes
- Tableau de bord conseiller avec liste d'alertes prioritaires
- Planification de RDV (calendrier intégré)
- Plans de réussite personnalisés (formulaire structuré + suivi d'objectifs)
- Dashboard analytics : taux de réussite par filière/cohorte/année

─── 2.4 INSERTION PROFESSIONNELLE ───
- Table : OffreStageEmploi (id, entreprise_id, titre, description, type[stage/cdi/cdd/alternance], domaine, localisation_gabon, date_debut, date_limite, statut, contact_json)
- Table : Candidature (id, etudiant_id, offre_id, date_candidature, statut, cv_url, lettre_url)
- Table : EntreprisePartenaire (id, raison_sociale, secteur, localisation, contact_rh, conventions_json)
- CVthèque (recherche par compétence, filière, disponibilité)
- Offres de stages/emplois avec matching automatique profil/offre
- Tableau de bord placement (taux d'insertion, délai moyen, secteurs)

─── 2.5 ALUMNI NETWORK ───
- Table : Alumni (id, etudiant_id, promo, poste_actuel, entreprise_actuelle, localisation, linkedin_url, disponible_mentorat, domaines_expertise_json)
- Annuaire des anciens avec recherche avancée
- Système de mentorat (mise en relation étudiant ↔ alumni)
- Offres emploi publiées par les alumni
- Statistiques d'insertion par promotion

Fournis tous les fichiers complets.
```

---

## 📚 PHASE 3 — MODULE PÉDAGOGIE & RESSOURCES

```
Module 3 : Pédagogie et ressources de GabonEdu Campus.

─── 3.1 GESTION DES COURS ───
- Table : Cours (id, ue_id, enseignant_id, titre_seance, type[CM/TD/TP], date, heure_debut, heure_fin, salle_id, statut, support_url, description)
- Table : Presence (id, cours_id, inscription_id, statut[present/absent/retard/justifié], heure_pointage, mode[manuel/qr])
- QR Code de présence dynamique (généré au début du cours, valable 15 minutes)
- Feuille de présence PDF générée automatiquement
- Statistiques de présence par étudiant, par UE, alertes seuil

─── 3.2 BIBLIOTHÈQUE NUMÉRIQUE LOCALE ───
- Table : Ouvrage (id, titre, auteurs_json, isbn, annee, editeur, domaine, localisation_physique, exemplaires_total, exemplaires_dispo, fichier_pdf_local, couverture_url)
- Table : Pret (id, etudiant_id, ouvrage_id, date_pret, date_retour_prevue, date_retour_effective, statut, penalite_fcfa)
- Catalogue avec recherche full-text (FTS5 SQLite)
- Téléchargement PDF pour lecture hors-ligne (stockage local chiffré)
- Gestion des prêts physiques avec rappels automatiques
- Import catalogue depuis fichier CSV/Excel

─── 3.3 DÉPÔT DE MÉMOIRES & THÈSES ───
- Table : MemoireThese (id, etudiant_id, directeur_id, titre, resume, mots_cles_json, annee, filiere_id, type[mémoire/thèse/rapport], version_courante, statut_validation, fichier_url, embargo_jusqu_au)
- Table : VersionDoc (id, memoire_id, numero_version, fichier_url, commentaires_directeur, date_depot, statut)
- Workflow : Dépôt → Revue directeur → Corrections → Validation finale → Archivage
- Détection de plagiat basique (similarité cosine entre résumés)
- Génération page de garde officielle PDF
- Archive consultable (avec gestion d'embargo)

─── 3.4 CLASSE VIRTUELLE LÉGÈRE ───
- Intégration Jitsi Meet (mode embarqué dans WebView Tauri, serveur public ou auto-hébergé)
- Table : SessionVirtuelle (id, cours_id, lien_jitsi, date_heure, duree_minutes, enregistrement_url, participants_json)
- Interface de lancement en un clic depuis le planning
- Mode basse bande passante : désactivation vidéo auto si débit < seuil
- Chat texte de session persisté en local
- Partage de fichiers pendant la session (upload vers dossier local partagé)

─── 3.5 BANQUE DE SUJETS & EXAMENS ───
- Table : Sujet (id, ue_id, enseignant_id, titre, type[qcm/rédigé/pratique], difficulte, annee_utilisation, fichier_chiffre_url, tags_json)
- Table : EpreuveExamen (id, ue_id, session[normale/rattrapage], date_examen, duree_minutes, salle_ids_json, sujets_selectionnes_json, statut[planifié/imprimé/déroulé/corrigé])
- Tirage aléatoire sécurisé de sujets selon critères
- Chiffrement des sujets jusqu'à J-1 (AES-256, clé révélée par admin)
- Impression contrôlée (watermark numéroté par salle)
- Statistiques d'utilisation des sujets

Fournis tous les fichiers complets.
```

---

## 🔬 PHASE 4 — MODULE RECHERCHE & INNOVATION

```
Module 4 : Recherche et innovation de GabonEdu Campus.

─── 4.1 GESTION DE PROJETS DE RECHERCHE ───
- Table : ProjetRecherche (id, titre, responsable_id, laboratoire_id, type[fondamentale/appliquée/développement], date_debut, date_fin, budget_total_fcfa, statut, partenaires_json, mots_cles_json)
- Table : LivrableRecherche (id, projet_id, titre, type[rapport/publication/brevet/logiciel], date_prevue, date_livraison, fichier_url, statut)
- Table : BudgetRecherche (id, projet_id, ligne_budgetaire, montant_alloue, montant_depense, justificatifs_json)
- Tableau de bord Gantt simplifié (vue planning projets)
- Rapports d'avancement PDF générés automatiquement

─── 4.2 VALORISATION SCIENTIFIQUE ───
- Table : Publication (id, auteurs_json, titre, journal_conference, annee, doi, type[article/communication/brevet/rapport], fichier_url, citations_count)
- Import automatique depuis DOI (appel API CrossRef)
- Indicateurs bibliométriques par chercheur/laboratoire (H-index simplifié, publications/an)
- Veille thématique (mots-clés surveillés, alertes nouvelles publications)

─── 4.3 LABORATOIRES & ÉQUIPEMENTS ───
- Table : Laboratoire (id, nom, responsable_id, localisation, specialite, budget_annuel_fcfa)
- Table : Equipement (id, labo_id, nom, reference, marque, etat[bon/dégradé/en_panne/réformé], date_acquisition, valeur_fcfa, prochaine_maintenance)
- Table : ReservationEquipement (id, equipement_id, utilisateur_id, date_debut, date_fin, motif, statut)
- Calendrier de réservation par équipement
- Alertes maintenance préventive
- Inventaire exportable (Excel, PDF)

─── 4.4 PARTENARIATS INTERNATIONAUX ───
- Table : Partenariat (id, institution_partenaire, pays, type[cotutelle/échange/recherche/formation], date_signature, date_expiration, convention_url, responsable_gabon_id, statut)
- Table : Mobilite (id, partenariat_id, personne_id, type[sortant/entrant], date_depart, date_retour, financement, rapport_url)
- Tableau de bord conventions (actives, à renouveler, expirées)
- Suivi des mobilités avec rapports de mission

─── 4.5 PROPRIÉTÉ INTELLECTUELLE ───
- Table : BrevetIP (id, titre, inventeurs_json, date_depot, numero_depot, office[OAPI/EPO/USPTO], statut, frais_json, contrat_valorisation_url)
- Suivi des échéances (renouvellements, réponses à actions d'office)
- Alertes automatiques avant échéance

Fournis tous les fichiers complets.
```

---

## 💰 PHASE 5 — MODULE GESTION FINANCIÈRE & LOGISTIQUE

```
Module 5 : Gestion financière et logistique de GabonEdu Campus.

─── 5.1 FACTURATION & RECOUVREMENT ───
- Table : FraisScolarite (id, filiere_id, annee_academique, niveau, montant_inscription_fcfa, montant_scolarite_fcfa, echeancier_json)
- Table : Paiement (id, inscription_id, montant_fcfa, date_paiement, mode[especes/mobile_money/virement], reference_transaction, operateur[Moov/Airtel/BGFIBank], recu_url, saisi_par)
- Table : Relance (id, inscription_id, type[1er/2eme/3eme/suspension], date_envoi, canal[sms/email/courrier], statut)
- Intégration Mobile Money Gabon : génération code de paiement Moov Money / Airtel Money via API (mock en dev, réel en prod)
- Tableau de bord recouvrement : taux de paiement, retards par filière, prévisionnel
- Génération reçu de paiement PDF
- Relances automatisées par SMS/email selon calendrier défini
- Export OHADA : tableau des recettes compatible avec plan comptable OHADA

─── 5.2 BUDGET & COMPTABILITÉ ANALYTIQUE ───
- Table : BudgetDepartement (id, departement_id, annee, lignes_budgetaires_json, statut[prévisionnel/voté/révisé])
- Table : EcritureComptable (id, date, libelle, compte_debit, compte_credit, montant_fcfa, piece_justificative_url, departement_id, projet_id)
- Plan comptable OHADA pré-chargé (secteur éducation)
- Tableau de bord budgétaire avec taux d'exécution par ligne
- États financiers automatiques : compte de résultat, balance, grand livre
- Exports Excel/CSV pour audit externe

─── 5.3 MARCHÉS PUBLICS INTERNES ───
- Table : DemandeAchat (id, departement_id, demandeur_id, objet, montant_estime_fcfa, urgence, statut_workflow, fournisseur_retenu_id, bon_commande_url)
- Workflow : Demande → Visa chef → Appel offres → Dépouillement → Attribution → Réception → Paiement
- Table : Fournisseur (id, raison_sociale, nif_gabon, activite, contact, historique_commandes_json, evaluation)
- Registre des fournisseurs agréés
- Conformité réglementaire ARMP Gabon (seuils de passation)

─── 5.4 PATRIMOINE & MAINTENANCE ───
- Table : BienImmobilier (id, designation, batiment, superficie_m2, valeur_fcfa, etat, date_acquisition, affectation)
- Table : InterventionMaintenance (id, bien_id, type[préventif/curatif], description, urgence[critique/normale/planifiée], statut, technicien, cout_fcfa, date_intervention, rapport_url)
- Cartographie simplifiée du campus (plan SVG interactif)
- Planning de maintenance préventive avec alertes
- Inventaire des biens exportable

─── 5.5 RESSOURCES HUMAINES ───
- Table : Personnel (id, nom, prenom, matricule, type[enseignant/administratif/vacataire], grade, departement_id, date_embauche, salaire_brut_fcfa, contrat_url, statut)
- Table : CongeAbsence (id, personnel_id, type, date_debut, date_fin, statut, validé_par, justificatif_url)
- Table : EvaluationPersonnel (id, personnel_id, evaluateur_id, annee, criteres_json, note_globale, commentaire, objectifs_suivants_json)
- Gestion des vacataires : suivi des heures, calcul des rémunérations, fiches de paie simplifiées
- Tableau de bord RH : effectifs, masse salariale, absences, évaluations en cours

Fournis tous les fichiers complets.
```

---

## 🔄 PHASE 6 — SYNCHRONISATION OFFLINE/ONLINE

```
Module synchronisation de GabonEdu Campus.

Architecture : l'app fonctionne 100% hors-ligne. La sync est déclenchée manuellement ou automatiquement dès qu'une connexion est détectée.

Implémente le moteur de synchronisation complet :

─── DÉTECTION DE CONNECTIVITÉ ───
- Polling réseau toutes les 30s (ping vers endpoint minimal /health du serveur central)
- Indicateur visuel dans le header : vert (sync OK), orange (en attente), rouge (hors-ligne)
- Notification Tauri lors du changement d'état

─── FILE D'ATTENTE DE SYNC ───
- Table SQLite : SyncQueue (id, operation[CREATE/UPDATE/DELETE], table_name, record_id, payload_json, timestamp, status[pending/syncing/done/failed/conflict], retry_count, error_message)
- Toute création/modification locale insère un enregistrement dans SyncQueue
- Chaque table possède un champ updated_at et un device_id (UUID de l'installation)

─── PROTOCOLE DE SYNCHRONISATION ───
1. Upload : envoi des opérations pending au serveur central (batch, compressé LZ4, HTTP POST)
2. Download : récupération des changements serveur depuis le dernier sync_timestamp local
3. Résolution de conflits :
   - Stratégie "last-write-wins" basée sur updated_at
   - Conflits métier (ex: même note modifiée par 2 postes) → journal de conflit avec notification admin
4. Confirmation : marquage done/failed dans SyncQueue, mise à jour sync_timestamp local

─── PRIORISATION ───
- Priorité HAUTE : paiements, notes validées, diplômes émis
- Priorité NORMALE : inscriptions, présences
- Priorité BASSE : supports de cours, bibliothèque

─── COMPRESSION ───
- Compression LZ4 des payloads > 1KB avant envoi
- Reprise automatique après coupure (chunk upload avec curseur)

─── UI SYNC ───
- Page dédiée "Centre de synchronisation" avec :
  - Statut global + progression
  - Historique des syncs (succès/erreurs)
  - Liste des conflits en attente de résolution
  - Bouton sync manuelle
  - Estimation données à synchroniser (KB/nombre d'opérations)

Fournis tous les fichiers complets (Python sync service + Vue sync store + composants).
```

---

## 🔐 PHASE 7 — SÉCURITÉ & CONFORMITÉ

```
Module sécurité de GabonEdu Campus.

─── AUTHENTIFICATION ───
- JWT (access_token 15min + refresh_token 7j, stockés en mémoire Tauri via invoke)
- TOTP 2FA avec QR Code d'enrôlement (pyotp + qrcode)
- Politique de mot de passe : min 8 chars, 1 majuscule, 1 chiffre, 1 spécial
- Verrouillage compte après 5 tentatives échouées (30 minutes)
- Session unique par poste (invalidation des autres sessions à la connexion)

─── PERMISSIONS GRANULAIRES ───
Implémente un système RBAC complet :
- Matrice permissions : RESOURCE × ACTION (CREATE/READ/UPDATE/DELETE/EXPORT/VALIDATE)
- Ressources : Etudiant, Note, Paiement, Document, Utilisateur, Configuration, Rapport
- Décorateur Python @require_permission("notes:validate") sur chaque endpoint FastAPI
- Guard Vue Router côté frontend
- Affichage conditionnel des boutons/menus selon permissions

─── JOURNAL D'AUDIT ───
- Table : AuditLog (id, user_id, action, resource_type, resource_id, old_value_json, new_value_json, ip_address, device_id, timestamp)
- Chaque opération CRUD sur données sensibles génère une entrée immuable
- Interface d'audit pour SUPER_ADMIN : filtres, export, alertes sur actions suspectes

─── CHIFFREMENT DES DONNÉES ───
- DB SQLite chiffrée via SQLCipher (clé dérivée du mot de passe admin + salt)
- Fichiers sensibles (sujets d'examen, contrats) chiffrés AES-256-GCM en local
- Clés gérées via Tauri's secure storage (OS keychain)
- TLS 1.3 obligatoire pour toutes les communications réseau

─── SIGNATURE ÉLECTRONIQUE ───
- Génération de paires de clés RSA-2048 par utilisateur autorisé
- Signature des PV de jury, diplômes, attestations (hash SHA-256 + signature RSA)
- Vérification de signature via page publique (/verify/{token})
- Compatible avec future intégration PKI nationale gabonaise (ANINF)

─── CONFORMITÉ LOI GABONAISE ───
- Durées de rétention des données configurables par type
- Export des données personnelles d'un étudiant (RGPD-like)
- Anonymisation des données pour statistiques
- Consentement explicite collecté à l'inscription

Fournis tous les fichiers complets.
```

---

## 🔗 PHASE 8 — INTEROPÉRABILITÉ GABON DIGITAL

```
Module interopérabilité de GabonEdu Campus.

─── CONNECTEURS API ───
Crée les connecteurs vers les systèmes nationaux gabonais (mode mock en dev, réel en prod via variables d'environnement) :

1. ANINF / NIP Gabon :
   - Vérification du NIP étudiant à l'inscription
   - Endpoint : POST /aninf/verify-nip → {valid: bool, nom, prenom, date_naissance}

2. Ministère Enseignement Supérieur :
   - Export statistiques annuelles (format XML SIF)
   - Déclaration des diplômés (JSON normé)

3. CNSS Gabon :
   - Vérification affiliation pour conventions de stage
   - Déclaration des stagiaires

─── API INTERNE DOCUMENTÉE ───
- FastAPI génère automatiquement OpenAPI 3.1 (accessible via /docs en dev)
- Tous les endpoints préfixés /api/v1/
- Authentification Bearer JWT sur tous les endpoints protégés
- Rate limiting : 100 req/min par token
- Versioning d'API pour rétrocompatibilité

─── FORMATS D'EXPORT ───
- PDF/A-1b pour archivage légal (WeasyPrint + conformance PDF/A)
- Excel (.xlsx) via openpyxl pour données tabulaires
- JSON-LD pour données liées (profils étudiants, publications)
- XML SIF pour rapports ministère
- CSV UTF-8 pour imports/exports génériques

─── WEBHOOKS ───
- Table : WebhookConfig (id, url, events_json, secret, actif)
- Events : etudiant.inscrit, paiement.reçu, diplome.emis, note.validée
- Livraison avec signature HMAC-SHA256 + retry exponentiel

Fournis tous les fichiers complets.
```

---

## 📦 PHASE 9 — PACKAGING & DÉPLOIEMENT

```
Phase de packaging et déploiement de GabonEdu Campus.

─── PACKAGING TAURI ───
1. Configure tauri.conf.json pour :
   - Installateur Windows .msi signé (certificat auto-signé en dev)
   - Bundle macOS .dmg
   - Icône app (université logo placeholder)
   - Mise à jour automatique différentielle via tauri-plugin-updater
   - Mode kiosque configurable (désactive fermeture fenêtre, plein écran forcé)
   - AppData isolation par établissement (clé de configuration à l'installation)

─── SIDECAR PYTHON ───
2. Configure PyInstaller pour bundler le backend FastAPI :
   - Commande : pyinstaller --onefile --name gabon_edu_backend main.py
   - Intégration dans les resources Tauri
   - Spawn automatique par Tauri avec port aléatoire (évite conflits)
   - Health check au démarrage (Tauri attend que l'API réponde avant d'afficher l'UI)

─── CONFIGURATION PAR ÉTABLISSEMENT ───
3. Fichier de configuration établissement (config.json) :
   {
     "etablissement": "Université Omar Bongo",
     "sigle": "UOB",
     "logo_url": "...",
     "ville": "Libreville",
     "modules_actifs": ["admin", "etudiants", "pedagogie", "finances"],
     "sync_server_url": "https://sync.gabon-edu.ga",
     "devise": "FCFA",
     "annee_academique_courante": "2024-2025"
   }
   Interface de configuration au premier lancement (wizard de setup).

─── MODE KIOSQUE ───
4. Mode poste partagé :
   - Auto-logout après 10 minutes d'inactivité
   - Nettoyage session à la fermeture
   - Impression directe sans dialogue (imprimante par défaut)

─── SCRIPTS DE DÉPLOIEMENT ───
5. Scripts shell pour :
   - Installation silencieuse (entreprise, déploiement masse)
   - Migration de base de données (Alembic)
   - Sauvegarde automatique (cron local)
   - Restauration depuis backup

Fournis tous les fichiers complets.
```

---

## 🧪 PHASE 10 — TESTS & FINALISATION

```
Phase tests et finalisation de GabonEdu Campus.

─── TESTS BACKEND (pytest) ───
Crée une suite de tests complète couvrant :
1. Tests unitaires : toutes les fonctions de calcul (moyennes, scoring bourses, détection décrochage)
2. Tests d'intégration : tous les endpoints FastAPI (auth, CRUD, workflows)
3. Tests de synchronisation : scénarios offline/online, résolution de conflits
4. Fixtures : base de données de test avec données gabonaises réalistes
   - 5 filières (Informatique, Droit, Médecine, Sciences Eco, Lettres)
   - 200 étudiants fictifs
   - 3 années académiques d'historique
   - Plan comptable OHADA complet

─── TESTS FRONTEND (Vitest + Vue Test Utils) ───
1. Tests composants : formulaires, tableaux, calculs côté client
2. Tests stores Pinia : actions, getters, persistance

─── DONNÉES DE DÉMO ───
Script seed complet (seed.py) insérant :
- Université Omar Bongo (config par défaut)
- 8 utilisateurs test (un par rôle)
- 5 filières avec maquettes pédagogiques complètes
- 1 promotion complète avec notes, présences, paiements
- Documents et exports test

─── FINALISATION UI ───
1. Page de paramètres généraux (thème, langue, notifications, sauvegarde)
2. Centre de notifications (toasts + panneau historique)
3. Module de rapports transversal (génération rapports personnalisés par module)
4. Tour guidé interactif premier lancement (onboarding)
5. Page d'erreur 404/500 élégante
6. Écran de chargement avec progression au démarrage

─── OPTIMISATIONS PERFORMANCE ───
- Virtualisation des longues listes (vue-virtual-scroller)
- Lazy loading des modules Vue (route-based code splitting)
- Pagination côté serveur pour toutes les listes > 50 éléments
- Indexes SQLite optimisés (sur colonnes filtrées fréquemment)
- Debounce sur les recherches texte (300ms)

Fournis tous les fichiers complets. L'application doit être prête pour un déploiement pilote dans une université gabonaise.
```

---

## 📋 INSTRUCTIONS D'UTILISATION OPENCODE

### Utilisation recommandée

1. **Commencer par PHASE 0** — Bootstrap complet du projet
2. **Une phase à la fois** — Attendre la fin avant de passer à la suivante
3. **Après chaque phase**, demander : *"Vérifie que tout compile et corrige les erreurs"*
4. **Pour les correctifs** : coller le message d'erreur + demander la correction ciblée

### Prompt de lancement OpenCode

```
Je construis GabonEdu Campus, une application desktop tout-en-un pour les universités gabonaises (Tauri 2.0 + Vue 3 TypeScript + Python FastAPI sidecar + SQLite). Commence par la PHASE 0 du super-prompt. Crée tous les fichiers avec leur contenu complet, aucun placeholder ni TODO. Le projet doit compiler et s'exécuter immédiatement après chaque phase.
```

### Prompt de continuation (entre phases)

```
La PHASE [N] est terminée et fonctionne. Passe maintenant à la PHASE [N+1] du super-prompt GabonEdu Campus. Tous les fichiers doivent être complets et immédiatement fonctionnels.
```

### Prompt de debug

```
J'ai cette erreur dans GabonEdu Campus : [ERREUR]. Corrige-la sans casser le code existant. Fournis uniquement les fichiers modifiés avec leur contenu complet.
```

---

## 📊 ALIGNEMENT GABON DIGITAL (CSV intégré)

| Objectif Gabon Digital | Module GabonEdu Campus |
|---|---|
| Dématérialisation des services publics | Dossier étudiant numérique unique, interconnecté NIP + registre social |
| Interopérabilité des systèmes | Connecteurs API ANINF, Ministère, CNSS |
| Développement compétences numériques | Module e-learning + suivi compétences digitales |
| Inclusion & accessibilité | Interface multilingue, mode basse conso, compatible vieux matériels |
| Gouvernance des données | Conformité loi gabonaise + audit trail complet |

---

*GabonEdu Campus — "Une université connectée, même sans connexion."*
*Stack : Tauri 2.0 | Vue 3 | Python FastAPI | SQLite | Offline-First*
