"""Pydantic schemas for administration module"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Any
from datetime import datetime, date
from enum import Enum


# === Filiere Schemas ===
class DomaineEtude(str, Enum):
    SCIENCES = "SCIENCES"
    LETTRES = "LETTRES"
    DROIT = "DROIT"
    ECONOMIE = "ECONOMIE"
    MEDECINE = "MEDECINE"
    INGENIERIE = "INGENIERIE"


class NiveauFiliere(str, Enum):
    LICENCE = "LICENCE"
    MASTER = "MASTER"
    DOCTORAT = "DOCTORAT"


class FiliereBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=20)
    libelle: str = Field(..., min_length=5, max_length=200)
    domaine: DomaineEtude
    niveau: NiveauFiliere
    duree_annees: int = Field(default=3, ge=1, le=10)
    responsable_id: Optional[int] = None
    description: Optional[str] = None


class FiliereCreate(FiliereBase):
    pass


class FiliereUpdate(BaseModel):
    libelle: Optional[str] = None
    domaine: Optional[DomaineEtude] = None
    niveau: Optional[NiveauFiliere] = None
    duree_annees: Optional[int] = None
    responsable_id: Optional[int] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FiliereResponse(FiliereBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === UE Schemas ===
class UETypEnum(str, Enum):
    OBLIGATOIRE = "obligatoire"
    OPTIONNEL = "optionnel"


class UEBase(BaseModel):
    filiere_id: int
    code_ue: str = Field(..., min_length=2, max_length=20)
    libelle: str = Field(..., min_length=5, max_length=200)
    credits_ects: int = Field(..., ge=1, le=30)
    semestre: int = Field(..., ge=1, le=6)
    heures_cm: int = Field(default=0, ge=0)
    heures_td: int = Field(default=0, ge=0)
    heures_tp: int = Field(default=0, ge=0)
    coefficient: float = Field(default=1.0, ge=0.5)
    ue_type: UETypEnum = UETypEnum.OBLIGATOIRE


class UECreate(UEBase):
    pass


class UEUpdate(BaseModel):
    libelle: Optional[str] = None
    credits_ects: Optional[int] = None
    semestre: Optional[int] = None
    heures_cm: Optional[int] = None
    heures_td: Optional[int] = None
    heures_tp: Optional[int] = None
    coefficient: Optional[float] = None
    ue_type: Optional[UETypEnum] = None
    is_active: Optional[bool] = None


class UEResponse(UEBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Maquette Schemas ===
class MaquetteStatut(str, Enum):
    BROUILLON = "brouillon"
    VALIDE = "valide"
    ARCHIVE = "archive"


class MaquetteBase(BaseModel):
    filiere_id: int
    annee_academique: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    ues_json: List[int] = Field(default_factory=list)
    statut: MaquetteStatut = MaquetteStatut.BROUILLON


class MaquetteCreate(MaquetteBase):
    pass


class MaquetteUpdate(BaseModel):
    ues_json: Optional[List[int]] = None
    statut: Optional[MaquetteStatut] = None


class MaquetteResponse(MaquetteBase):
    id: int
    created_at: datetime
    validated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === Etudiant Schemas ===
class GenreEnum(str, Enum):
    M = "M"
    F = "F"


class StatutEtudiantEnum(str, Enum):
    INSCRIT = "INSCRIT"
    SUSPENDU = "SUSPENDU"
    EXCLUT = "EXCLUT"
    DIPLOME = "DIPLome"
    ABANDON = "ABANDON"


class EtudiantBase(BaseModel):
    nip_gabon: Optional[str] = None
    nom: str = Field(..., min_length=2, max_length=100)
    prenom: str = Field(..., min_length=2, max_length=100)
    date_naissance: date
    genre: GenreEnum
    nationalite: str = "Gabonaise"
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    statut: StatutEtudiantEnum = StatutEtudiantEnum.INSCRIT
    adresse: Optional[str] = None
    ville: str = "Libreville"


class EtudiantCreate(EtudiantBase):
    pass


class EtudiantUpdate(BaseModel):
    nip_gabon: Optional[str] = None
    nom: Optional[str] = None
    prenom: Optional[str] = None
    date_naissance: Optional[date] = None
    genre: Optional[GenreEnum] = None
    nationalite: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    photo_url: Optional[str] = None
    statut: Optional[StatutEtudiantEnum] = None
    adresse: Optional[str] = None
    ville: Optional[str] = None


class EtudiantResponse(EtudiantBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === Inscription Schemas ===
class TypeInscriptionEnum(str, Enum):
    NOUVEAU = "NOUVEAU"
    REINSCRIPTION = "REINSCRIPTION"


class StatutWorkflowEnum(str, Enum):
    SOUMIS = "SOUMIS"
    VALIDE_SCOL = "VALIDE_SCOL"
    VALIDE_DOYEN = "VALIDE_DOYEN"
    CONFIRME = "CONFIRME"
    REJETE = "REJETE"


class NiveauEtude(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    M1 = "M1"
    M2 = "M2"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"


class InscriptionBase(BaseModel):
    etudiant_id: int
    annee_academique: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    filiere_id: int
    niveau: NiveauEtude
    type_inscription: TypeInscriptionEnum = TypeInscriptionEnum.NOUVEAU
    documents_json: List[Any] = Field(default_factory=list)
    frais_total: float = Field(..., ge=0)


class InscriptionCreate(InscriptionBase):
    pass


class InscriptionUpdate(BaseModel):
    statut_workflow: Optional[StatutWorkflowEnum] = None
    documents_json: Optional[List[Any]] = None
    frais_payes: Optional[float] = None
    frais_total: Optional[float] = None


class InscriptionResponse(InscriptionBase):
    id: int
    statut_workflow: StatutWorkflowEnum
    date_soumission: datetime
    frais_payes: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === Salle Schemas ===
class TypeSalleEnum(str, Enum):
    AMPHI = "amphi"
    TD = "td"
    TP = "tp"
    INFO = "info"


class SalleBase(BaseModel):
    nom: str = Field(..., min_length=2, max_length=50)
    capacite: int = Field(..., ge=10, le=1000)
    type_salle: TypeSalleEnum
    equipements_json: List[str] = Field(default_factory=list)
    batiment: Optional[str] = None
    etage: Optional[str] = None
    disponible: bool = True


class SalleCreate(SalleBase):
    pass


class SalleUpdate(BaseModel):
    nom: Optional[str] = None
    capacite: Optional[int] = None
    type_salle: Optional[TypeSalleEnum] = None
    equipements_json: Optional[List[str]] = None
    batiment: Optional[str] = None
    etage: Optional[str] = None
    disponible: Optional[bool] = None


class SalleResponse(SalleBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Cours Schemas ===
class TypeCoursEnum(str, Enum):
    CM = "CM"
    TD = "TD"
    TP = "TP"


class StatutCoursEnum(str, Enum):
    PLANIFIE = "PLANIFIE"
    EN_COURS = "EN_COURS"
    TERMINE = "TERMINE"
    ANNULE = "ANNULE"


class JourSemaine(str, Enum):
    LUNDI = "LUNDI"
    MARDI = "MARDI"
    MERCREDI = "MERCREDI"
    JEUDI = "JEUDI"
    VENDREDI = "VENDREDI"
    SAMEDI = "SAMEDI"


class SemaineType(str, Enum):
    A = "A"
    B = "B"
    TOUTES = "toutes"


class CoursBase(BaseModel):
    ue_id: int
    enseignant_id: int
    titre_seance: str = Field(..., min_length=5, max_length=200)
    type_cours: TypeCoursEnum
    date_cours: date
    heure_debut: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    heure_fin: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    salle_id: Optional[int] = None
    groupe: Optional[str] = None
    semaine_type: SemaineType = SemaineType.TOUTES
    statut: StatutCoursEnum = StatutCoursEnum.PLANIFIE
    support_url: Optional[str] = None
    description: Optional[str] = None
    couleur_hex: str = "#1B4F72"


class CoursCreate(CoursBase):
    pass


class CoursUpdate(BaseModel):
    titre_seance: Optional[str] = None
    type_cours: Optional[TypeCoursEnum] = None
    date_cours: Optional[date] = None
    heure_debut: Optional[str] = None
    heure_fin: Optional[str] = None
    salle_id: Optional[int] = None
    groupe: Optional[str] = None
    semaine_type: Optional[SemaineType] = None
    statut: Optional[StatutCoursEnum] = None
    support_url: Optional[str] = None
    description: Optional[str] = None
    couleur_hex: Optional[str] = None


class CoursResponse(CoursBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Note Schemas ===
class TypeEvalEnum(str, Enum):
    CC = "CC"
    TP = "TP"
    EXAMEN = "EXAMEN"
    RATTRAPAGE = "RATTRAPAGE"


class NoteBase(BaseModel):
    inscription_id: int
    ue_id: int
    type_eval: TypeEvalEnum
    note: Optional[float] = Field(None, ge=0, le=20)
    coefficient: float = Field(default=1.0, ge=0.5)
    absence_justifiee: bool = False
    commentaires: Optional[str] = None


class NoteCreate(NoteBase):
    saisi_par: int


class NoteUpdate(BaseModel):
    note: Optional[float] = Field(None, ge=0, le=20)
    absence_justifiee: Optional[bool] = None
    validee: Optional[bool] = None
    commentaires: Optional[str] = None


class NoteResponse(NoteBase):
    id: int
    saisi_par: int
    validee: bool
    date_saisie: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Presence Schemas ===
class StatutPresence(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    RETARD = "retard"
    JUSTIFIE = "justifie"


class ModePresence(str, Enum):
    MANUEL = "manuel"
    QR = "qr"


class PresenceBase(BaseModel):
    cours_id: int
    inscription_id: int
    etudiant_id: int
    statut: StatutPresence = StatutPresence.ABSENT
    mode: ModePresence = ModePresence.MANUEL
    justificatif_url: Optional[str] = None


class PresenceCreate(PresenceBase):
    pass


class PresenceUpdate(BaseModel):
    statut: Optional[StatutPresence] = None
    justificatif_url: Optional[str] = None


class PresenceResponse(PresenceBase):
    id: int
    heure_pointage: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Creneau Schemas (Emploi du temps) ===
class CreneauBase(BaseModel):
    ue_id: int
    enseignant_id: int
    salle_id: int
    groupe: Optional[str] = None
    jour: JourSemaine
    heure_debut: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    heure_fin: str = Field(..., pattern=r"^([01]\d|2[0-3]):([0-5]\d)$")
    semaine_type: SemaineType = SemaineType.TOUTES
    couleur_hex: str = "#1B4F72"


class CreneauCreate(CreneauBase):
    pass


class CreneauUpdate(BaseModel):
    ue_id: Optional[int] = None
    enseignant_id: Optional[int] = None
    salle_id: Optional[int] = None
    groupe: Optional[str] = None
    jour: Optional[JourSemaine] = None
    heure_debut: Optional[str] = None
    heure_fin: Optional[str] = None
    semaine_type: Optional[SemaineType] = None
    couleur_hex: Optional[str] = None


class CreneauResponse(CreneauBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# === Deliberation Schemas ===
class StatutDeliberation(str, Enum):
    BROUILLON = "brouillon"
    VALIDE = "valide"
    SIGNE = "signe"


class DeliberationBase(BaseModel):
    filiere_id: int
    annee_academique: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    semestre: int = Field(..., ge=1, le=6)
    jury_json: List[Any] = Field(default_factory=list)
    date_deliberation: Optional[date] = None


class DeliberationCreate(DeliberationBase):
    pass


class DeliberationUpdate(BaseModel):
    jury_json: Optional[List[Any]] = None
    statut: Optional[StatutDeliberation] = None
    pv_url: Optional[str] = None
    date_deliberation: Optional[date] = None


class DeliberationResponse(DeliberationBase):
    id: int
    statut: StatutDeliberation
    pv_url: Optional[str] = None
    created_at: datetime
    validated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# === Diplome Schemas ===
class MentionDiplome(str, Enum):
    PASSABLE = "Passable"
    ASSEZ_BIEN = "Assez Bien"
    BIEN = "Bien"
    TRES_BIEN = "Très Bien"
    FELICITATIONS = "Félicitations du Jury"


class DiplomeBase(BaseModel):
    etudiant_id: int
    filiere_id: int
    annee_obtention: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    mention: MentionDiplome = MentionDiplome.PASSABLE
    numero_serie: str = Field(..., min_length=5, max_length=50)


class DiplomeCreate(DiplomeBase):
    pass


class DiplomeUpdate(BaseModel):
    mention: Optional[MentionDiplome] = None
    numero_serie: Optional[str] = None


class DiplomeResponse(DiplomeBase):
    id: int
    qr_token: str
    date_emission: datetime
    signe_par: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
