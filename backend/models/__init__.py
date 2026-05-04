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

__all__ = [
    "User",
    "UserRole",
    "Etudiant",
    "Genre",
    "StatutEtudiant",
    "Filiere",
    "UE",
    "Maquette",
    "DomaineEtude",
    "NiveauFiliere",
    "Inscription",
    "TypeInscription",
    "StatutWorkflow",
    "NiveauEtude",
    "Cours",
    "Salle",
    "Presence",
    "TypeCours",
    "StatutCours",
    "JourSemaine",
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
]
