"""
Script de seed des données pour GabonEdu Campus
Configuration: Centre Universitaire de Koulamoutou (CUK) - USTM
"""
import asyncio
import sys
from datetime import datetime, timedelta
import random

sys.path.insert(0, '/workspace/backend')

from database import async_engine, async_session_maker, init_db

from sqlalchemy import text

# Import des modèles (depuis le package models)
from models import (
    Etudiant, Inscription, UE, Filiere, Maquette,
    Salle, Note
)
from models.user import User, Role as RoleType
from models.vie_etudiante import Portfolio, ExperiencePortfolio, TypeBourse, DossierBourse
from models.finances import FraisScolarite, Paiement

# Données CUK - Le modèle Etablissement n'existe pas encore, on le skip pour l'instant
ETABLISSEMENT_DATA = {
    "nom": "Centre Universitaire de Koulamoutou",
    "sigle": "CUK",
    "ville": "Koulamoutou",
}

FILIERES_DATA = [
    {"code": "AEC", "libelle": "Architecture et Éco-construction", "domaine": "Ingénierie & Construction", "niveau": "L3", "duree_annees": 3},
    {"code": "CI", "libelle": "Chimie Industrielle", "domaine": "Sciences & Technologies", "niveau": "L3", "duree_annees": 3},
    {"code": "GTR", "libelle": "Génie Thermique et Énergies Renouvelables", "domaine": "Énergie", "niveau": "L3", "duree_annees": 3},
    {"code": "IC", "libelle": "Informatique et Communication", "domaine": "Numérique", "niveau": "L3", "duree_annees": 3},
    {"code": "PM", "libelle": "Productique Mécanique", "domaine": "Industrie", "niveau": "L3", "duree_annees": 3},
    {"code": "ABB", "libelle": "Analyses Biologiques et Biochimiques", "domaine": "Santé", "niveau": "L3", "duree_annees": 3},
    {"code": "MEB", "libelle": "Maintenance des Équipements Biomédicaux", "domaine": "Santé & Technologie", "niveau": "L3", "duree_annees": 3},
]

# Unités d'enseignement par filière (simplifié pour la démo)
UES_DATA = {
    "IC": [
        {"code": "INFO101", "libelle": "Algorithmes et Structures de Données", "credits": 6, "semestre": 1, "heures_cm": 30, "heures_td": 30, "heures_tp": 0},
        {"code": "INFO102", "libelle": "Programmation Python", "credits": 6, "semestre": 1, "heures_cm": 20, "heures_td": 20, "heures_tp": 40},
        {"code": "INFO103", "libelle": "Bases de Données", "credits": 5, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 20},
        {"code": "INFO104", "libelle": "Développement Web", "credits": 6, "semestre": 2, "heures_cm": 20, "heures_td": 20, "heures_tp": 40},
        {"code": "INFO201", "libelle": "Réseaux et Télécommunications", "credits": 6, "semestre": 3, "heures_cm": 30, "heures_td": 30, "heures_tp": 20},
        {"code": "INFO202", "libelle": "Sécurité Informatique", "credits": 5, "semestre": 3, "heures_cm": 30, "heures_td": 20, "heures_tp": 30},
    ],
    "AEC": [
        {"code": "AEC101", "libelle": "Dessin Technique et CAO", "credits": 6, "semestre": 1, "heures_cm": 20, "heures_td": 20, "heures_tp": 40},
        {"code": "AEC102", "libelle": "Matériaux de Construction", "credits": 5, "semestre": 1, "heures_cm": 30, "heures_td": 30, "heures_tp": 20},
        {"code": "AEC103", "libelle": "Éco-conception Bâtiment", "credits": 6, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 20},
    ],
    "CI": [
        {"code": "CI101", "libelle": "Chimie Générale", "credits": 6, "semestre": 1, "heures_cm": 40, "heures_td": 20, "heures_tp": 40},
        {"code": "CI102", "libelle": "Procédés Industriels", "credits": 6, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
    ],
    "GTR": [
        {"code": "GTR101", "libelle": "Thermodynamique Appliquée", "credits": 6, "semestre": 1, "heures_cm": 40, "heures_td": 20, "heures_tp": 30},
        {"code": "GTR102", "libelle": "Énergies Renouvelables", "credits": 6, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
    ],
    "PM": [
        {"code": "PM101", "libelle": "Conception Mécanique", "credits": 6, "semestre": 1, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
        {"code": "PM102", "libelle": "Automatisme Industriel", "credits": 5, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 20},
    ],
    "ABB": [
        {"code": "ABB101", "libelle": "Biochimie Métabolique", "credits": 6, "semestre": 1, "heures_cm": 40, "heures_td": 20, "heures_tp": 40},
        {"code": "ABB102", "libelle": "Microbiologie Appliquée", "credits": 6, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
    ],
    "MEB": [
        {"code": "MEB101", "libelle": "Électronique Médicale", "credits": 6, "semestre": 1, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
        {"code": "MEB102", "libelle": "Maintenance Hospitalière", "credits": 6, "semestre": 2, "heures_cm": 30, "heures_td": 30, "heures_tp": 30},
    ],
}

NOMS_GABONAIS = [
    "Mba", "Ndong", "Obame", "Owono", "Minko", "Eyeghe", "Nguema", "Ondoua", "Meviane", "Owolabi",
    "Bekale", "Moussavou", "Okoga", "Razafindrazaka", "Ibinga", "Kombila", "Louembe", "Mayi-Maya",
    "Nsie", "Ossomba", "Pambou", "Queffelec", "Ribot", "Sitruk", "Toupet", "Urruty", "Vandaele",
    "Wang", "Xavier", "Yala", "Zue"
]

PRENOMS_GABONAIS = [
    "Jean", "Pierre", "Paul", "Jacques", "Michel", "André", "Louis", "François", "Joseph", "Charles",
    "Marie", "Claire", "Anne", "Sophie", "Isabelle", "Catherine", "Brigitte", "Nathalie", "Sylvie",
    "Arnaud", "Bruno", "Christophe", "Daniel", "Éric", "Fabrice", "Gilles", "Henri", "Ivan", "Julien",
    "Kevin", "Laurent", "Maxime", "Nicolas", "Olivier", "Patrick", "Quentin", "Raphaël", "Stéphane",
    "Thierry", "Vincent", "Wilfried", "Xavier", "Yann", "Zacharie"
]

async def seed_database():
    """Peuple la base de données avec les données du CUK"""
    
    # D'abord créer les tables
    print("📦 Initialisation des tables de la base de données...")
    await init_db()
    
    async with async_session_maker() as session:
        try:
            # 1. Skip établissement (modèle n'existe pas encore)
            print("\n🏫 Configuration pour le Centre Universitaire de Koulamoutou (CUK)...")
            etablissement_id = None  # Sera ajouté ultérieurement

            # 2. Créer les utilisateurs (8 profils)
            print("\n👥 Création des utilisateurs de test...")
            users_data = [
                {"email": "superadmin@cuk.ga", "role": RoleType.SUPER_ADMIN, "nom": "Admin", "prenom": "Super"},
                {"email": "scolarite@cuk.ga", "role": RoleType.ADMIN_SCOL, "nom": "Scolarité", "prenom": "Service"},
                {"email": "enseignant@cuk.ga", "role": RoleType.ENSEIGNANT, "nom": "Professeur", "prenom": "Jean"},
                {"email": "financier@cuk.ga", "role": RoleType.FINANCIER, "nom": "Comptable", "prenom": "Marie"},
                {"email": "bibliotheque@cuk.ga", "role": RoleType.BIBLIOTHECAIRE, "nom": "Bibliothèque", "prenom": "Paul"},
                {"email": "chercheur@cuk.ga", "role": RoleType.CHERCHEUR, "nom": "Chercheur", "prenom": "Dr Pierre"},
                {"email": "etudiant.demo@cuk.ga", "role": RoleType.ETUDIANT, "nom": "Demo", "prenom": "Étudiant"},
                {"email": "rectorat@cuk.ga", "role": RoleType.SUPER_ADMIN, "nom": "Recteur", "prenom": "Monsieur"},
            ]
            
            users = []
            for u in users_data:
                # Vérifier si l'utilisateur existe déjà
                result = await session.execute(
                    text("SELECT id FROM users WHERE email = :email"),
                    {"email": u["email"]}
                )
                if result.fetchone():
                    print(f"   ⚠️ {u['email']} existe déjà")
                    continue
                    
                user = User(
                    email=u["email"],
                    role=u["role"],
                    nom=u["nom"],
                    prenom=u["prenom"],
                    telephone=f"+241 {random.randint(10000000, 99999999)}",
                    is_active=True
                )
                # Mot de passe par défaut: Gabon2024!
                from security.auth import get_password_hash
                user.hashed_password = get_password_hash("Gabon2024!")
                session.add(user)
                users.append(user)
            
            await session.commit()
            for u in users:
                await session.refresh(u)
                print(f"   ✓ {u.email} ({u.role.value})")

            # 3. Créer les filières
            print("\n📚 Création des 7 filières du CUK...")
            filieres = {}
            responsable_id = users[2].id if users else None
            
            for f in FILIERES_DATA:
                # Vérifier si la filière existe déjà
                result = await session.execute(
                    text("SELECT id FROM filieres WHERE code = :code"),
                    {"code": f["code"]}
                )
                if result.fetchone():
                    print(f"   ⚠️ Filière {f['code']} existe déjà")
                    continue
                    
                filiere = Filiere(
                    code=f["code"],
                    libelle=f["libelle"],
                    domaine=f["domaine"],
                    niveau=f["niveau"],
                    duree_annees=f["duree_annees"],
                    responsable_id=responsable_id,
                )
                session.add(filiere)
                filieres[f["code"]] = filiere
            
            await session.commit()
            for code, f in filieres.items():
                await session.refresh(f)
                print(f"   ✓ {f.code} - {f.libelle}")

            # 4. Créer les UE par filière
            print("\n📖 Création des Unités d'Enseignement...")
            ues_par_filiere = {}
            for code_filiere, ues in UES_DATA.items():
                if code_filiere in filieres:
                    ues_par_filiere[code_filiere] = []
                    for ue_data in ues:
                        ue = UE(
                            filiere_id=filieres[code_filiere].id,
                            code_ue=ue_data["code"],
                            libelle=ue_data["libelle"],
                            credits_ects=ue_data["credits"],
                            semestre=ue_data["semestre"],
                            heures_cm=ue_data["heures_cm"],
                            heures_td=ue_data["heures_td"],
                            heures_tp=ue_data["heures_tp"],
                            coefficient=ue_data["credits"] // 2,
                            ue_type="obligatoire"
                        )
                        session.add(ue)
                        ues_par_filiere[code_filiere].append(ue)
            
            await session.commit()
            total_ue = sum(len(ues) for ues in ues_par_filiere.values())
            print(f"   ✓ {total_ue} UE créées")

            # 5. Créer les maquettes pédagogiques
            print("\n📋 Création des maquettes pédagogiques...")
            annee_courante = "2024-2025"
            for code_filiere, ues in ues_par_filiere.items():
                ues_json = [{"ue_id": ue.id, "semestre": ue.semestre} for ue in ues]
                maquette = Maquette(
                    filiere_id=filieres[code_filiere].id,
                    annee_academique=annee_courante,
                    ues_json=ues_json,
                    statut="validé"
                )
                session.add(maquette)
            
            await session.commit()
            print(f"   ✓ 7 maquettes créées pour {annee_courante}")

            # 6. Créer les salles
            print("\n🏛️ Création des salles...")
            salles_data = [
                {"nom": "Amphi A", "capacite": 150, "type": "amphi", "batiment": "Bâtiment Principal"},
                {"nom": "Amphi B", "capacite": 100, "type": "amphi", "batiment": "Bâtiment Principal"},
                {"nom": "Salle TD1", "capacite": 40, "type": "td", "batiment": "Bâtiment A"},
                {"nom": "Salle TD2", "capacite": 40, "type": "td", "batiment": "Bâtiment A"},
                {"nom": "Labo Info", "capacite": 25, "type": "tp", "batiment": "Bâtiment B", "equipements": '{"ordinateurs": 25, "projecteur": true}'},
                {"nom": "Labo Chimie", "capacite": 20, "type": "tp", "batiment": "Bâtiment C", "equipements": '{"paillasses": 20, "hotte": 4}'},
                {"nom": "Labo Mécanique", "capacite": 15, "type": "tp", "batiment": "Atelier", "equipements": '{"machines_outils": 10}'},
            ]
            
            salles = []
            for s in salles_data:
                salle = Salle(
                    nom=s["nom"],
                    capacite=s["capacite"],
                    type_salle=s["type"],
                    equipements_json=s.get("equipements", "{}"),
                    batiment=s["batiment"],
                    disponible=True
                )
                session.add(salle)
                salles.append(salle)
            
            await session.commit()
            print(f"   ✓ {len(salles)} salles créées")

            # 7. Créer 210 étudiants répartis dans les filières
            print("\n🎓 Création de 210 étudiants...")
            codes_filieres = list(filieres.keys())
            etudiants_par_filiere = {code: [] for code in codes_filieres}
            
            for i in range(210):
                nom = random.choice(NOMS_GABONAIS)
                prenom = random.choice(PRENOMS_GABONAIS)
                code_filiere = codes_filieres[i % len(codes_filieres)]  # Répartition équitable
                niveau = random.choice(["L1", "L2", "L3"])
                
                # Générer un NIP gabonais fictif
                nip = f"GAB{random.randint(100000, 999999)}"
                
                etudiant = Etudiant(
                    nip_gabon=nip,
                    nom=nom.upper(),
                    prenom=prenom.capitalize(),
                    date_naissance=datetime(2000 + random.randint(0, 5), random.randint(1, 12), random.randint(1, 28)),
                    genre=random.choice(["M", "F"]),
                    nationalite="Gabonaise",
                    telephone=f"+241 {random.randint(10000000, 99999999)}",
                    email=f"{prenom.lower()}.{nom.lower()}{i}@cuk.ga",
                    photo_url=None,
                    statut="ACTIF"
                )
                session.add(etudiant)
                etudiants_par_filiere[code_filiere].append((etudiant, niveau))
                
                if (i + 1) % 30 == 0:
                    print(f"   ... {i + 1}/210 étudiants créés")
            
            await session.commit()
            
            # Rafraîchir tous les étudiants
            for code in codes_filieres:
                for j, (etud, _) in enumerate(etudiants_par_filiere[code]):
                    await session.refresh(etud)
            
            print(f"   ✓ 210 étudiants créés")

            # 8. Créer les inscriptions
            print("\n📝 Création des inscriptions...")
            inscriptions = []
            frais_base = 150000  # FCFA
            
            for code_filiere, etudiants_niveaux in etudiants_par_filiere.items():
                filiere = filieres[code_filiere]
                for etudiant, niveau in etudiants_niveaux:
                    inscription = Inscription(
                        etudiant_id=etudiant.id,
                        annee_academique=annee_courante,
                        filiere_id=filiere.id,
                        niveau=niveau,
                        type_inscription="NOUVEAU" if niveau == "L1" else "REINSCRIPTION",
                        statut_workflow="CONFIRME",
                        date_soumission=datetime.now() - timedelta(days=random.randint(1, 60)),
                        documents_json='{"cin": true, "bac": true, "casier_judiciaire": true}',
                        frais_payes=random.choice([True, True, True, False])  # 75% ont payé
                    )
                    session.add(inscription)
                    inscriptions.append(inscription)
            
            await session.commit()
            print(f"   ✓ {len(inscriptions)} inscriptions créées")

            # 9. Créer les frais de scolarité
            print("\n💰 Configuration des frais de scolarité...")
            for code_filiere, filiere in filieres.items():
                for niveau in ["L1", "L2", "L3"]:
                    frais = FraisScolarite(
                        filiere_id=filiere.id,
                        annee_academique=annee_courante,
                        niveau=niveau,
                        montant_inscription=25000,
                        montant_scolarite=frais_base,
                        echeancier_json=[
                            {"echeance": "Septembre", "montant": 50000, "type": "inscription"},
                            {"echeance": "Novembre", "montant": 50000, "type": "scolarite"},
                            {"echeance": "Janvier", "montant": 50000, "type": "scolarite"},
                            {"echeance": "Mars", "montant": 50000, "type": "scolarite"}
                        ]
                    )
                    session.add(frais)
            
            await session.commit()
            print(f"   ✓ Frais configurés pour toutes les filières")

            # 10. Créer des paiements
            print("\n💳 Génération des paiements...")
            modes_paiement = ["especes", "mobile_money", "virement"]
            operateurs = ["Moov", "Airtel", "BGFIBank"]
            
            paiements_count = 0
            for inscription in inscriptions:
                if inscription.frais_payes:
                    # Créer 1 à 3 paiements par inscription
                    nb_paiements = random.randint(1, 3)
                    reste_du = frais_base
                    
                    for _ in range(nb_paiements):
                        if reste_du <= 0:
                            break
                        
                        montant = min(reste_du, random.choice([25000, 50000, 75000]))
                        mode = random.choice(modes_paiement)
                        
                        paiement = Paiement(
                            inscription_id=inscription.id,
                            montant=montant,
                            date_paiement=datetime.now() - timedelta(days=random.randint(1, 90)),
                            mode_paiement=mode,
                            reference_transaction=f"TXN{random.randint(100000000, 999999999)}",
                            operateur=random.choice(operateurs) if mode == "mobile_money" else None,
                            recu_url=f"/recus/recu_{inscription.id}_{paiements_count}.pdf",
                            saisi_par=users[3].id  # Le financier
                        )
                        session.add(paiement)
                        paiements_count += 1
                        reste_du -= montant
            
            await session.commit()
            print(f"   ✓ {paiements_count} paiements enregistrés")

            # 11. Créer des notes pour quelques étudiants (démo)
            print("\n📊 Génération de notes de démonstration...")
            notes_count = 0
            
            # Prendre les 30 premiers étudiants IC pour la démo
            etudiants_ic = [e for e, n in etudiants_par_filiere["IC"][:30]]
            ues_ic = ues_par_filiere.get("IC", [])
            
            if ues_ic and etudiants_ic:
                for etudiant in etudiants_ic:
                    # Trouver l'inscription de cet étudiant en IC
                    inscription = next((i for i in inscriptions if i.etudiant_id == etudiant.id and i.filiere_id == filieres["IC"].id), None)
                    if not inscription:
                        continue
                    
                    for ue in ues_ic[:3]:  # 3 UE pour la démo
                        # Note CC
                        note_cc = Note(
                            inscription_id=inscription.id,
                            ue_id=ue.id,
                            type_eval="cc",
                            note=random.uniform(8, 18),
                            absence_justifiee=False,
                            date_saisie=datetime.now() - timedelta(days=random.randint(1, 30)),
                            saisi_par=users[2].id,  # L'enseignant
                            validee=True
                        )
                        session.add(note_cc)
                        notes_count += 1
                        
                        # Note Examen
                        note_exam = Note(
                            inscription_id=inscription.id,
                            ue_id=ue.id,
                            type_eval="examen",
                            note=random.uniform(6, 19),
                            absence_justifiee=random.choice([False, False, False, True]),
                            date_saisie=datetime.now() - timedelta(days=random.randint(1, 15)),
                            saisi_par=users[2].id,
                            validee=True
                        )
                        session.add(note_exam)
                        notes_count += 1
                
                await session.commit()
                print(f"   ✓ {notes_count} notes générées (filière IC)")

            print("\n" + "="*60)
            print("✅ SEED TERMINÉ AVEC SUCCÈS !")
            print("="*60)
            print(f"\n📊 Résumé des données créées:")
            print(f"   • 1 établissement: {ETABLISSEMENT_DATA['nom']}")
            print(f"   • 8 utilisateurs de test")
            print(f"   • 7 filières (AEC, CI, GTR, IC, PM, ABB, MEB)")
            print(f"   • {total_ue} Unités d'Enseignement")
            print(f"   • {len(salles)} salles")
            print(f"   • 210 étudiants")
            print(f"   • {len(inscriptions)} inscriptions")
            print(f"   • {paiements_count} paiements")
            print(f"   • {notes_count} notes (démo)")
            print(f"\n🔐 Identifiants de test:")
            print(f"   • Super Admin: superadmin@cuk.ga / Gabon2024!")
            print(f"   • Scolarité: scolarite@cuk.ga / Gabon2024!")
            print(f"   • Enseignant: enseignant@cuk.ga / Gabon2024!")
            print(f"   • Étudiant: etudiant.demo@cuk.ga / Gabon2024!")
            print(f"   • Financier: financier@cuk.ga / Gabon2024!")
            print("="*60)
            
        except Exception as e:
            await session.rollback()
            print(f"\n❌ ERREUR: {str(e)}")
            raise

if __name__ == "__main__":
    print("🚀 Initialisation de la base de données GabonEdu Campus...")
    print(f"🏫 Établissement: {ETABLISSEMENT_DATA['nom']} ({ETABLISSEMENT_DATA['sigle']})")
    print(f"📍 Ville: {ETABLISSEMENT_DATA['ville']}")
    print("-"*60)
    
    asyncio.run(seed_database())
