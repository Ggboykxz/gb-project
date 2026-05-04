"""
Schémas Pydantic pour la vie étudiante et services
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from enum import Enum


# --- Enums ---
class TypeExperienceEnum(str, Enum):
    STAGE = "stage"
    PROJET = "projet"
    CERTIFICATION = "certification"
    BENEVOLAT = "benevolat"


class VisibilitePortfolioEnum(str, Enum):
    PRIVE = "prive"
    ETABLISSEMENT = "etablissement"
    PUBLIC = "public"


class StatutDossierBourseEnum(str, Enum):
    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    EN_ETUDE = "en_etude"
    ACCEPTE = "accepte"
    REFUSE = "refuse"
    EN_ATTENTE_DOC = "en_attente_doc"


class TypeAlerteEtudiantEnum(str, Enum):
    DECROCHAGE = "decrochage"
    ECHEC = "echec"
    ABSENCE_REPETEE = "absence_repetee"
    RETARD_PAIEMENT = "retard_paiement"
    AUTRE = "autre"


class StatutSuiviEnum(str, Enum):
    OUVERT = "ouvert"
    EN_COURS = "en_cours"
    RESOLU = "resolu"
    CLOS = "clos"


class TypeOffreEnum(str, Enum):
    STAGE = "stage"
    CDI = "cdi"
    CDD = "cdd"
    ALTERNANCE = "alternance"


class StatutOffreEnum(str, Enum):
    ACTIVE = "active"
    POURVUE = "pourvue"
    EXPIREE = "expiree"
    SUSPENDUE = "suspendue"


class StatutCandidatureEnum(str, Enum):
    SOUMISE = "soumise"
    EN_ETUDE = "en_etude"
    ACCEPTEE = "acceptee"
    REFUSEE = "refusee"
    RETIREE = "retiree"


# --- Portfolio ---
class ExperiencePortfolioBase(BaseModel):
    type_exp: TypeExperienceEnum
    titre: str = Field(..., max_length=200)
    organisation: Optional[str] = None
    date_debut: Optional[date] = None
    date_fin: Optional[date] = None
    description: Optional[str] = None
    fichier_url: Optional[str] = None


class ExperiencePortfolioCreate(ExperiencePortfolioBase):
    portfolio_id: int


class ExperiencePortfolioResponse(ExperiencePortfolioBase):
    id: int
    portfolio_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PortfolioBase(BaseModel):
    bio: Optional[str] = None
    competences_json: List[str] = []
    langues_json: List[str] = []
    visibilite: VisibilitePortfolioEnum = VisibilitePortfolioEnum.PRIVE


class PortfolioCreate(PortfolioBase):
    etudiant_id: int


class PortfolioUpdate(BaseModel):
    bio: Optional[str] = None
    competences_json: Optional[List[str]] = None
    langues_json: Optional[List[str]] = None
    visibilite: Optional[VisibilitePortfolioEnum] = None


class PortfolioResponse(PortfolioBase):
    id: int
    etudiant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    experiences: List[ExperiencePortfolioResponse] = []

    model_config = ConfigDict(from_attributes=True)


# --- Bourses ---
class TypeBourseBase(BaseModel):
    libelle: str = Field(..., max_length=100)
    montant_mensuel: int = Field(..., gt=0)
    criteres_json: dict = {}
    quota_annuel: Optional[int] = None
    financeur: Optional[str] = None
    actif: bool = True


class TypeBourseCreate(TypeBourseBase):
    pass


class TypeBourseUpdate(BaseModel):
    libelle: Optional[str] = None
    montant_mensuel: Optional[int] = None
    criteres_json: Optional[dict] = None
    quota_annuel: Optional[int] = None
    financeur: Optional[str] = None
    actif: Optional[bool] = None


class TypeBourseResponse(TypeBourseBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DossierBourseBase(BaseModel):
    annee_academique: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    statut: StatutDossierBourseEnum = StatutDossierBourseEnum.BROUILLON
    score_social: Optional[float] = None
    documents_json: List[str] = []
    decision: Optional[str] = None
    commentaire: Optional[str] = None


class DossierBourseCreate(DossierBourseBase):
    etudiant_id: int
    type_bourse_id: int


class DossierBourseUpdate(BaseModel):
    statut: Optional[StatutDossierBourseEnum] = None
    score_social: Optional[float] = None
    decision: Optional[str] = None
    date_decision: Optional[datetime] = None
    commentaire: Optional[str] = None
    traite_par: Optional[int] = None


class DossierBourseResponse(DossierBourseBase):
    id: int
    etudiant_id: int
    type_bourse_id: int
    soumis_le: Optional[datetime] = None
    date_decision: Optional[datetime] = None
    traite_par: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    type_bourse: Optional[TypeBourseResponse] = None

    model_config = ConfigDict(from_attributes=True)


# --- Suivi Étudiant ---
class NoteSuivi(BaseModel):
    date: datetime
    contenu: str
    auteur: str


class ObjectifSuivi(BaseModel):
    description: str
    echeance: Optional[date] = None
    atteint: bool = False


class SuiviEtudiantBase(BaseModel):
    type_alerte: TypeAlerteEtudiantEnum
    statut: StatutSuiviEnum = StatutSuiviEnum.OUVERT
    notes_suivi_json: List[NoteSuivi] = []
    objectifs_json: List[ObjectifSuivi] = []


class SuiviEtudiantCreate(SuiviEtudiantBase):
    etudiant_id: int
    conseiller_id: int


class SuiviEtudiantUpdate(BaseModel):
    statut: Optional[StatutSuiviEnum] = None
    notes_suivi_json: Optional[List[NoteSuivi]] = None
    objectifs_json: Optional[List[ObjectifSuivi]] = None
    date_cloture: Optional[datetime] = None


class SuiviEtudiantResponse(SuiviEtudiantBase):
    id: int
    etudiant_id: int
    conseiller_id: int
    date_creation: datetime
    date_cloture: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --- Offres Stage/Emploi ---
class EntreprisePartenaireBase(BaseModel):
    raison_sociale: str = Field(..., max_length=200)
    secteur: Optional[str] = None
    localisation: Optional[str] = None
    contact_rh: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    conventions_json: List[dict] = []
    actif: bool = True


class EntreprisePartenaireCreate(EntreprisePartenaireBase):
    pass


class EntreprisePartenaireUpdate(BaseModel):
    raison_sociale: Optional[str] = None
    secteur: Optional[str] = None
    localisation: Optional[str] = None
    contact_rh: Optional[str] = None
    email: Optional[EmailStr] = None
    telephone: Optional[str] = None
    conventions_json: Optional[List[dict]] = None
    actif: Optional[bool] = None


class EntreprisePartenaireResponse(EntreprisePartenaireBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OffreStageEmploiBase(BaseModel):
    titre: str = Field(..., max_length=200)
    description: str
    type_offre: TypeOffreEnum
    domaine: Optional[str] = None
    localisation_gabon: str
    date_debut: date
    date_limite: Optional[date] = None
    statut: StatutOffreEnum = StatutOffreEnum.ACTIVE
    contact_json: dict = {}
    competences_requises_json: List[str] = []


class OffreStageEmploiCreate(OffreStageEmploiBase):
    entreprise_id: int


class OffreStageEmploiUpdate(BaseModel):
    titre: Optional[str] = None
    description: Optional[str] = None
    type_offre: Optional[TypeOffreEnum] = None
    domaine: Optional[str] = None
    localisation_gabon: Optional[str] = None
    date_debut: Optional[date] = None
    date_limite: Optional[date] = None
    statut: Optional[StatutOffreEnum] = None
    contact_json: Optional[dict] = None
    competences_requises_json: Optional[List[str]] = None


class OffreStageEmploiResponse(OffreStageEmploiBase):
    id: int
    entreprise_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    entreprise: Optional[EntreprisePartenaireResponse] = None

    model_config = ConfigDict(from_attributes=True)


class CandidatureBase(BaseModel):
    cv_url: Optional[str] = None
    lettre_url: Optional[str] = None
    commentaire: Optional[str] = None


class CandidatureCreate(CandidatureBase):
    etudiant_id: int
    offre_id: int


class CandidatureUpdate(BaseModel):
    statut: Optional[StatutCandidatureEnum] = None
    cv_url: Optional[str] = None
    lettre_url: Optional[str] = None
    commentaire: Optional[str] = None
    date_reponse: Optional[datetime] = None


class CandidatureResponse(CandidatureBase):
    id: int
    etudiant_id: int
    offre_id: int
    date_candidature: datetime
    statut: StatutCandidatureEnum
    date_reponse: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# --- Alumni ---
class AlumniBase(BaseModel):
    promo: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    poste_actuel: Optional[str] = None
    entreprise_actuelle: Optional[str] = None
    localisation: Optional[str] = None
    linkedin_url: Optional[str] = None
    disponible_mentorat: bool = False
    domaines_expertise_json: List[str] = []
    email_personnel: Optional[EmailStr] = None
    telephone_personnel: Optional[str] = None


class AlumniCreate(AlumniBase):
    etudiant_id: int


class AlumniUpdate(BaseModel):
    poste_actuel: Optional[str] = None
    entreprise_actuelle: Optional[str] = None
    localisation: Optional[str] = None
    linkedin_url: Optional[str] = None
    disponible_mentorat: Optional[bool] = None
    domaines_expertise_json: Optional[List[str]] = None
    email_personnel: Optional[EmailStr] = None
    telephone_personnel: Optional[str] = None


class AlumniResponse(AlumniBase):
    id: int
    etudiant_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
