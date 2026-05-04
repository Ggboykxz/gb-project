"""
Schémas Pydantic pour le module Gestion Financière & Logistique
Phase 5 - GabonEdu Campus
"""
from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum


# ─── ENUMS ───

class ModePaiementEnum(str, Enum):
    ESPECES = "especes"
    MOOV_MONEY = "moov_money"
    AIRTEL_MONEY = "airtel_money"
    VIREMENT = "virement"
    CHEQUE = "cheque"


class OperateurPaiementEnum(str, Enum):
    MOOV = "Moov"
    AIRTEL = "Airtel"
    BGFIBANK = "BGFIBank"
    UGB = "UGB"
    NONE = "none"


class TypeRelanceEnum(str, Enum):
    PREMIER = "1er"
    DEUXIEME = "2eme"
    TROISIEME = "3eme"
    SUSPENSION = "suspension"


class CanalRelanceEnum(str, Enum):
    SMS = "sms"
    EMAIL = "email"
    COURRIER = "courrier"


class StatutBudgetEnum(str, Enum):
    PREVISIONNEL = "prévisionnel"
    VOTE = "voté"
    REVISE = "révisé"
    EXECUTE = "exécuté"


class StatutDemandeAchatEnum(str, Enum):
    DEMANDE = "demande"
    VISA_CHEF = "visa_chef"
    APPEL_OFFRES = "appel_offres"
    DEPOUILLEMENT = "depouillement"
    ATTRIBUTION = "attribution"
    RECEPTION = "reception"
    PAIEMENT = "paiement"
    CLOTURE = "cloture"


class UrgenceAchatEnum(str, Enum):
    NORMALE = "normale"
    URGENTE = "urgente"
    CRITIQUE = "critique"


class EtatBienEnum(str, Enum):
    NEUF = "neuf"
    BON = "bon"
    DEGRADE = "dégradé"
    EN_PANNE = "en_panne"
    REFORME = "réformé"


class TypeBienEnum(str, Enum):
    IMMOBILIER = "immobilier"
    MOBILIER = "mobilier"
    EQUIPEMENT = "équipement"
    VEHICULE = "véhicule"
    INFORMATIQUE = "informatique"


class UrgenceMaintenanceEnum(str, Enum):
    CRITIQUE = "critique"
    NORMALE = "normale"
    PLANIFIEE = "planifiée"


class TypeMaintenanceEnum(str, Enum):
    PREVENTIF = "préventif"
    CURATIF = "curatif"
    CORRECTIF = "correctif"


class TypePersonnelEnum(str, Enum):
    ENSEIGNANT = "enseignant"
    ADMINISTRATIF = "administratif"
    TECHNIQUE = "technique"
    VACATAIRE = "vacataire"
    STAGIAIRE = "stagiaire"


class StatutPersonnelEnum(str, Enum):
    ACTIF = "actif"
    CONGE = "congé"
    DETACHEMENT = "détachement"
    RETRAITE = "retraite"
    SUSPENDU = "suspendu"


class TypeCongeEnum(str, Enum):
    ANNUAL = "annuel"
    MALADIE = "maladie"
    MATERNITE = "maternité"
    PATERNITE = "paternité"
    SANS_SOLDE = "sans_solde"
    FORMATION = "formation"
    AUTRE = "autre"


# ─── 5.1 FACTURATION & RECOUVREMENT ───

class EcheancierItem(BaseModel):
    echeance: str
    montant: float
    paye: bool = False


class FraisScolariteBase(BaseModel):
    filiere_id: int
    annee_academique: str = Field(..., min_length=9, max_length=9)
    niveau: str
    montant_inscription_fcfa: float = 0.0
    montant_scolarite_fcfa: float = 0.0
    echeancier_json: Optional[List[Dict[str, Any]]] = None


class FraisScolariteCreate(FraisScolariteBase):
    pass


class FraisScolariteUpdate(BaseModel):
    montant_inscription_fcfa: Optional[float] = None
    montant_scolarite_fcfa: Optional[float] = None
    echeancier_json: Optional[List[Dict[str, Any]]] = None


class FraisScolariteResponse(FraisScolariteBase):
    id: int
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class PaiementBase(BaseModel):
    inscription_id: int
    montant_fcfa: float = Field(..., gt=0)
    mode_paiement: ModePaiementEnum
    operateur: OperateurPaiementEnum = OperateurPaiementEnum.NONE
    reference_transaction: Optional[str] = None
    commentaire: Optional[str] = None


class PaiementCreate(PaiementBase):
    saisi_par: int


class PaiementUpdate(BaseModel):
    statut: Optional[str] = None
    commentaire: Optional[str] = None
    recu_url: Optional[str] = None


class PaiementResponse(PaiementBase):
    id: int
    frais_scolarite_id: Optional[int] = None
    date_paiement: datetime
    recu_url: Optional[str] = None
    saisi_par: int
    statut: str
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


class RelanceBase(BaseModel):
    inscription_id: int
    type_relance: TypeRelanceEnum
    canal: CanalRelanceEnum
    contenu: Optional[str] = None
    destinaire: Optional[str] = None


class RelanceCreate(RelanceBase):
    pass


class RelanceResponse(RelanceBase):
    id: int
    date_envoi: datetime
    statut: str
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TableauRecouvrement(BaseModel):
    """Statistiques de recouvrement"""
    total_a_recouvrer: float
    total_recouvre: float
    taux_recouvrement: float
    nombre_impayes: int
    par_filiere: List[Dict[str, Any]]
    par_echeance: List[Dict[str, Any]]


# ─── 5.2 BUDGET & COMPTABILITÉ ANALYTIQUE ───

class LigneBudgetaire(BaseModel):
    code: str
    libelle: str
    prevu: float
    realise: float = 0.0


class BudgetDepartementBase(BaseModel):
    departement_id: Optional[int] = None
    annee: str = Field(..., min_length=4, max_length=4)
    lignes_budgetaires_json: Optional[List[Dict[str, Any]]] = None
    statut: StatutBudgetEnum = StatutBudgetEnum.PREVISIONNEL


class BudgetDepartementCreate(BudgetDepartementBase):
    pass


class BudgetDepartementUpdate(BaseModel):
    lignes_budgetaires_json: Optional[List[Dict[str, Any]]] = None
    statut: Optional[StatutBudgetEnum] = None
    total_prevu_fcfa: Optional[float] = None
    total_realise_fcfa: Optional[float] = None


class BudgetDepartementResponse(BudgetDepartementBase):
    id: int
    total_prevu_fcfa: float
    total_realise_fcfa: float
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class EcritureComptableBase(BaseModel):
    date_ecriture: date
    libelle: str = Field(..., max_length=255)
    compte_debit: str = Field(..., min_length=3, max_length=20)
    compte_credit: str = Field(..., min_length=3, max_length=20)
    montant_fcfa: float = Field(..., gt=0)
    piece_justificative_url: Optional[str] = None
    departement_id: Optional[int] = None
    projet_id: Optional[int] = None
    budget_id: Optional[int] = None


class EcritureComptableCreate(EcritureComptableBase):
    saisie_par: int


class EcritureComptableUpdate(BaseModel):
    validee: Optional[bool] = None
    piece_justificative_url: Optional[str] = None


class EcritureComptableResponse(EcritureComptableBase):
    id: int
    saisie_par: int
    validee: bool
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BalanceComptable(BaseModel):
    """Balance comptable OHADA"""
    compte: str
    libelle: str
    debit_total: float
    credit_total: float
    solde: float
    solde_type: str  # débiteur/créditeur


# ─── 5.3 MARCHÉS PUBLICS INTERNES ───

class FournisseurBase(BaseModel):
    raison_sociale: str = Field(..., max_length=255)
    nif_gabon: Optional[str] = Field(None, max_length=20)
    activite: Optional[str] = None
    contact_nom: Optional[str] = None
    contact_telephone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    adresse: Optional[str] = None
    evaluation: float = Field(default=0.0, ge=0.0, le=5.0)
    agree: bool = False


class FournisseurCreate(FournisseurBase):
    pass


class FournisseurUpdate(BaseModel):
    activite: Optional[str] = None
    contact_telephone: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    evaluation: Optional[float] = None
    agree: Optional[bool] = None
    date_agrement: Optional[date] = None


class FournisseurResponse(FournisseurBase):
    id: int
    date_agrement: Optional[date] = None
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


class DemandeAchatBase(BaseModel):
    departement_id: int
    objet: str = Field(..., max_length=255)
    description: Optional[str] = None
    montant_estime_fcfa: float = Field(..., gt=0)
    urgence: UrgenceAchatEnum = UrgenceAchatEnum.NORMALE


class DemandeAchatCreate(DemandeAchatBase):
    demandeur_id: int


class DemandeAchatUpdate(BaseModel):
    statut_workflow: Optional[StatutDemandeAchatEnum] = None
    fournisseur_retenu_id: Optional[int] = None
    bon_commande_url: Optional[str] = None
    facture_url: Optional[str] = None
    commentaires_json: Optional[List[Dict[str, Any]]] = None
    date_validation: Optional[datetime] = None
    date_reception: Optional[datetime] = None


class DemandeAchatResponse(DemandeAchatBase):
    id: int
    demandeur_id: int
    statut_workflow: StatutDemandeAchatEnum
    fournisseur_retenu_id: Optional[int] = None
    bon_commande_url: Optional[str] = None
    facture_url: Optional[str] = None
    date_demande: datetime
    date_validation: Optional[datetime] = None
    date_reception: Optional[datetime] = None
    commentaires_json: List[Dict[str, Any]]
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ─── 5.4 PATRIMOINE & MAINTENANCE ───

class BienImmobilierBase(BaseModel):
    designation: str = Field(..., max_length=255)
    type_bien: TypeBienEnum
    batiment: Optional[str] = None
    localisation_detail: Optional[str] = None
    superficie_m2: Optional[float] = None
    valeur_fcfa: float = 0.0
    etat: EtatBienEnum = EtatBienEnum.BON
    date_acquisition: Optional[date] = None
    affectation: Optional[str] = None
    numero_inventaire: Optional[str] = None
    observations: Optional[str] = None


class BienImmobilierCreate(BienImmobilierBase):
    pass


class BienImmobilierUpdate(BaseModel):
    etat: Optional[EtatBienEnum] = None
    affectation: Optional[str] = None
    observations: Optional[str] = None


class BienImmobilierResponse(BienImmobilierBase):
    id: int
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class InterventionMaintenanceBase(BaseModel):
    bien_id: int
    type_maintenance: TypeMaintenanceEnum
    description: str
    urgence: UrgenceMaintenanceEnum = UrgenceMaintenanceEnum.NORMALE
    technicien: Optional[str] = None
    cout_fcfa: float = 0.0


class InterventionMaintenanceCreate(InterventionMaintenanceBase):
    pass


class InterventionMaintenanceUpdate(BaseModel):
    statut: Optional[str] = None
    cout_fcfa: Optional[float] = None
    date_intervention: Optional[datetime] = None
    rapport_url: Optional[str] = None
    photos_avant_apres_json: Optional[List[Dict[str, Any]]] = None


class InterventionMaintenanceResponse(InterventionMaintenanceBase):
    id: int
    statut: str
    date_intervention: Optional[datetime] = None
    date_demande: datetime
    rapport_url: Optional[str] = None
    photos_avant_apres_json: List[Dict[str, Any]]
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class StatistiquesMaintenance(BaseModel):
    """Statistiques de maintenance"""
    total_interventions: int
    par_statut: Dict[str, int]
    par_urgence: Dict[str, int]
    cout_total: float
    temps_moyen_resolution_jours: float


# ─── 5.5 RESSOURCES HUMAINES ───

class PersonnelBase(BaseModel):
    nom: str = Field(..., max_length=100)
    prenom: str = Field(..., max_length=100)
    matricule: str = Field(..., min_length=3, max_length=20)
    type_personnel: TypePersonnelEnum
    grade: Optional[str] = None
    departement_id: Optional[int] = None
    date_embauche: date
    date_naissance: Optional[date] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    salaire_brut_fcfa: float = 0.0
    statut: StatutPersonnelEnum = StatutPersonnelEnum.ACTIF


class PersonnelCreate(PersonnelBase):
    pass


class PersonnelUpdate(BaseModel):
    grade: Optional[str] = None
    departement_id: Optional[int] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    salaire_brut_fcfa: Optional[float] = None
    statut: Optional[StatutPersonnelEnum] = None
    contrat_url: Optional[str] = None


class PersonnelResponse(PersonnelBase):
    id: int
    contrat_url: Optional[str] = None
    photo_url: Optional[str] = None
    date_creation: datetime
    date_modification: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class CongeAbsenceBase(BaseModel):
    personnel_id: int
    type_conge: TypeCongeEnum
    date_debut: date
    date_fin: date
    justificatif_url: Optional[str] = None
    commentaire: Optional[str] = None


class CongeAbsenceCreate(CongeAbsenceBase):
    pass


class CongeAbsenceUpdate(BaseModel):
    statut: Optional[str] = None
    valide_par: Optional[int] = None
    date_validation: Optional[datetime] = None


class CongeAbsenceResponse(CongeAbsenceBase):
    id: int
    statut: str
    valide_par: Optional[int] = None
    date_demande: datetime
    date_validation: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class EvaluationPersonnelBase(BaseModel):
    personnel_id: int
    evaluateur_id: int
    annee: str = Field(..., min_length=4, max_length=4)
    criteres_json: Dict[str, Any] = {}
    note_globale: float = Field(default=0.0, ge=0.0, le=20.0)
    commentaire: Optional[str] = None
    objectifs_suivants_json: List[Dict[str, Any]] = []


class EvaluationPersonnelCreate(EvaluationPersonnelBase):
    pass


class EvaluationPersonnelResponse(EvaluationPersonnelBase):
    id: int
    date_evaluation: datetime
    date_creation: datetime
    
    model_config = ConfigDict(from_attributes=True)


class HeureVacationBase(BaseModel):
    vacataire_id: int
    cours_id: Optional[int] = None
    ue_id: Optional[int] = None
    date_vacation: date
    nombre_heures: float = Field(..., gt=0)
    taux_horaire_fcfa: float = 0.0
    observation: Optional[str] = None


class HeureVacationCreate(HeureVacationBase):
    pass


class HeureVacationUpdate(BaseModel):
    montant_total_fcfa: Optional[float] = None
    statut_paiement: Optional[str] = None
    valide_par: Optional[int] = None
    date_validation: Optional[datetime] = None


class HeureVacationResponse(HeureVacationBase):
    id: int
    montant_total_fcfa: float
    statut_paiement: str
    valide_par: Optional[int] = None
    date_saisie: datetime
    date_validation: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class MasseSalariale(BaseModel):
    """Statistiques masse salariale"""
    total_brut: float
    total_vacations: float
    effectif_total: int
    par_departement: List[Dict[str, Any]]
    par_type_personnel: List[Dict[str, Any]]
