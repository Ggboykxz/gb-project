"""Modèles SQLAlchemy de GabonEdu Campus - CUK/USTM"""
from .user import User, Role
from .etudiant import Etudiant, Inscription
from .filiere import Filiere, UE, Maquette, Salle, Creneau
from .note import Note, Deliberation
from .cours import Cours, Presence, QRCodePresence
from .vie_etudiante import Portfolio, ExperiencePortfolio, DossierBourse, TypeBourse, SuiviEtudiant, OffreStageEmploi, Candidature, EntreprisePartenaire, Alumni
from .finances import FraisScolarite, Paiement, Relance, BudgetDepartement, EcritureComptable, DemandeAchat, Fournisseur, BienImmobilier, InterventionMaintenance, Personnel, CongeAbsence
from .pedagogie import Ouvrage, Pret, MemoireThese, VersionDoc, SessionVirtuelle, Sujet, EpreuveExamen
from .recherche import ProjetRecherche, LivrableRecherche, BudgetRecherche, Publication, Laboratoire, Equipement, ReservationEquipement, Partenariat, Mobilite, BrevetIP
from .sync import SyncQueue, SyncConfig, SyncLog, ConflitSync
from .securite import AuditLog, SessionUtilisateur, PermissionRole

__all__ = [
    'User', 'Role', 'Etudiant', 'Inscription', 'Filiere', 'UE', 'Maquette',
    'Salle', 'Creneau', 'Note', 'Deliberation', 'Cours', 'Presence',
    'QRCodePresence', 'Portfolio', 'ExperiencePortfolio', 'DossierBourse',
    'TypeBourse', 'SuiviEtudiant', 'OffreStageEmploi', 'Candidature',
    'EntreprisePartenaire', 'Alumni', 'FraisScolarite', 'Paiement', 'Relance',
    'BudgetDepartement', 'EcritureComptable', 'DemandeAchat', 'Fournisseur',
    'BienImmobilier', 'InterventionMaintenance', 'Personnel', 'CongeAbsence',
    'Ouvrage', 'Pret', 'MemoireThese', 'VersionDoc', 'SessionVirtuelle',
    'Sujet', 'EpreuveExamen', 'ProjetRecherche', 'LivrableRecherche',
    'BudgetRecherche', 'Publication', 'Laboratoire', 'Equipement',
    'ReservationEquipement', 'Partenariat', 'Mobilite', 'BrevetIP',
    'SyncQueue', 'SyncConfig', 'SyncLog', 'ConflitSync', 'AuditLog',
    'SessionUtilisateur', 'PermissionRole'
]
