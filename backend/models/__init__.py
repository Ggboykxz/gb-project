"""Models package for GabonEdu Campus"""
from models.user import User, UserRole
from models.etudiant import Etudiant, Genre, StatutEtudiant
from models.filiere import Filiere, UE, Maquette, DomaineEtude, NiveauFiliere
from models.inscription import Inscription, TypeInscription, StatutWorkflow, NiveauEtude
from models.cours import Cours, Salle, Presence, TypeCours, StatutCours, JourSemaine
from models.note import Note, TypeEval
from models.vie_etudiante import (
    Portfolio, ExperiencePortfolio, TypeExperience, VisibilitePortfolio,
    DossierBourse, StatutDossierBourse, TypeBourse,
    SuiviEtudiant, TypeAlerteEtudiant, StatutSuivi,
    OffreStageEmploi, TypeOffre, StatutOffre, Candidature, StatutCandidature, EntreprisePartenaire,
    Alumni
)
from models.finances import (
    FraisScolarite, Paiement, Relance, ModePaiement, OperateurPaiement,
    BudgetDepartement, EcritureComptable, StatutBudget,
    DemandeAchat, StatutDemandeAchat, Fournisseur,
    BienImmobilier, InterventionMaintenance, UrgenceMaintenance,
    Personnel, TypePersonnel, CongeAbsence, TypeConge, EvaluationPersonnel, StatutPersonnel
)
from models.pedagogie import (
    CoursSupport, TypeSupport, StatutDocument,
    QRCodePresence,
    Ouvrage, Pret,
    MemoireThese, VersionDoc,
    SessionVirtuelle,
    Sujet, EpreuveExamen
)
from models.recherche import (
    ProjetRecherche, TypeProjet, StatutProjet,
    LivrableRecherche, TypeLivrable, StatutLivrable,
    BudgetRecherche,
    Publication,
    Laboratoire,
    Equipement, ReservationEquipement,
    Partenariat, Mobilite,
    BrevetIP
)
from models.sync import (
    SyncQueue, OperationSync, StatutSync, PrioriteSync,
    SyncConfig, SyncLog, ConflitSync, SyncMapping
)
from models.securite import (
    AuditLog, TypeAction,
    SessionUtilisateur,
    CleSignature, SignatureDocument,
    TentativeConnexion, VerrouillageCompte,
    PermissionRole,
    ConsentementRGPD, ExportDonnees
)

__all__ = [
    # User
    "User",
    "UserRole",
    # Etudiant
    "Etudiant",
    "Genre",
    "StatutEtudiant",
    # Filiere
    "Filiere",
    "UE",
    "Maquette",
    "DomaineEtude",
    "NiveauFiliere",
    # Inscription
    "Inscription",
    "TypeInscription",
    "StatutWorkflow",
    "NiveauEtude",
    # Cours
    "Cours",
    "Salle",
    "Presence",
    "TypeCours",
    "StatutCours",
    "JourSemaine",
    # Note
    "Note",
    "TypeEval",
    # Vie étudiante
    "Portfolio",
    "ExperiencePortfolio",
    "TypeExperience",
    "VisibilitePortfolio",
    "DossierBourse",
    "StatutDossierBourse",
    "TypeBourse",
    "SuiviEtudiant",
    "TypeAlerteEtudiant",
    "StatutSuivi",
    "OffreStageEmploi",
    "TypeOffre",
    "StatutOffre",
    "Candidature",
    "StatutCandidature",
    "EntreprisePartenaire",
    "Alumni",
    # Finances
    "FraisScolarite",
    "Paiement",
    "Relance",
    "ModePaiement",
    "OperateurPaiement",
    "BudgetDepartement",
    "EcritureComptable",
    "StatutBudget",
    "DemandeAchat",
    "StatutDemandeAchat",
    "Fournisseur",
    "BienImmobilier",
    "InterventionMaintenance",
    "UrgenceMaintenance",
    "Personnel",
    "TypePersonnel",
    "CongeAbsence",
    "TypeConge",
    "EvaluationPersonnel",
    "StatutPersonnel",
    # Pédagogie
    "CoursSupport",
    "TypeSupport",
    "StatutDocument",
    "QRCodePresence",
    "Ouvrage",
    "Pret",
    "MemoireThese",
    "VersionDoc",
    "SessionVirtuelle",
    "Sujet",
    "EpreuveExamen",
    # Recherche
    "ProjetRecherche",
    "TypeProjet",
    "StatutProjet",
    "LivrableRecherche",
    "TypeLivrable",
    "StatutLivrable",
    "BudgetRecherche",
    "Publication",
    "Laboratoire",
    "Equipement",
    "ReservationEquipement",
    "Partenariat",
    "Mobilite",
    "BrevetIP",
    # Synchronisation
    "SyncQueue",
    "OperationSync",
    "StatutSync",
    "PrioriteSync",
    "SyncConfig",
    "SyncLog",
    "ConflitSync",
    "SyncMapping",
    # Sécurité
    "AuditLog",
    "TypeAction",
    "SessionUtilisateur",
    "CleSignature",
    "SignatureDocument",
    "TentativeConnexion",
    "VerrouillageCompte",
    "PermissionRole",
    "ConsentementRGPD",
    "ExportDonnees",
]
