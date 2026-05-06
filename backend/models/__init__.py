"""Modèles SQLAlchemy de GabonEdu Campus"""
from .user import User, Role
from .etudiant import Etudiant, Inscription
from .filiere import Filiere, UE, Maquette, Salle, Creneau
from .note import Note, Deliberation
from .vie_etudiante import (
    Portfolio, ExperiencePortfolio, TypeBourse, DossierBourse, 
    SuiviEtudiant, EntreprisePartenaire, OffreStageEmploi, Candidature, Alumni
)
from .finances import FraisScolarite, Paiement, Relance
from .pedagogie import Ouvrage, Pret, MemoireThese, Sujet
from .recherche import ProjetRecherche, Laboratoire, Publication, Equipement, Partenariat
from .sync import SyncQueue, SyncConfig, SyncLog, ConflitSync
from .securite import SessionUtilisateur, TentativeConnexion, AuditLog