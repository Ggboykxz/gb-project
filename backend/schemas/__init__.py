"""Schemas package for GabonEdu Campus"""
from schemas.auth import (
    UserRole, UserBase, UserCreate, UserUpdate, UserProfile, UserLogin,
    TokenResponse,
    TOTPSetupResponse, TOTPVerifyRequest, PasswordChangeRequest
)

from schemas.administration import (
    DomaineEtude, NiveauFiliere, FiliereBase, FiliereCreate, FiliereUpdate, FiliereResponse,
    UETypEnum, UEBase, UECreate, UEUpdate, UEResponse,
    MaquetteStatut, MaquetteBase, MaquetteCreate, MaquetteUpdate, MaquetteResponse,
    GenreEnum, StatutEtudiantEnum, EtudiantBase, EtudiantCreate, EtudiantUpdate, EtudiantResponse,
    TypeInscriptionEnum, StatutWorkflowEnum, NiveauEtude,
    InscriptionBase, InscriptionCreate, InscriptionUpdate, InscriptionResponse,
    TypeSalleEnum, SalleBase, SalleCreate, SalleUpdate, SalleResponse,
    TypeCoursEnum, StatutCoursEnum, JourSemaine, SemaineType,
    CoursBase, CoursCreate, CoursUpdate, CoursResponse,
    TypeEvalEnum, NoteBase, NoteCreate, NoteUpdate, NoteResponse,
    StatutPresence, ModePresence, PresenceBase, PresenceCreate, PresenceUpdate, PresenceResponse
)

from schemas.finances import (
    ModePaiementEnum, OperateurPaiementEnum, TypeRelanceEnum, CanalRelanceEnum,
    StatutBudgetEnum, StatutDemandeAchatEnum, UrgenceAchatEnum,
    EtatBienEnum, TypeBienEnum, UrgenceMaintenanceEnum, TypeMaintenanceEnum,
    TypePersonnelEnum, StatutPersonnelEnum, TypeCongeEnum,
    PaiementBase, PaiementCreate, PaiementUpdate, PaiementResponse,
    FraisScolariteBase, FraisScolariteCreate, FraisScolariteUpdate, FraisScolariteResponse,
    RelanceBase, RelanceCreate, RelanceResponse, TableauRecouvrement,
    LigneBudgetaire, BudgetDepartementBase, BudgetDepartementCreate, BudgetDepartementUpdate, BudgetDepartementResponse,
    EcritureComptableBase, EcritureComptableCreate, EcritureComptableUpdate, EcritureComptableResponse, BalanceComptable,
    FournisseurBase, FournisseurCreate, FournisseurUpdate, FournisseurResponse,
    DemandeAchatBase, DemandeAchatCreate, DemandeAchatUpdate, DemandeAchatResponse,
    BienImmobilierBase, BienImmobilierCreate, BienImmobilierUpdate, BienImmobilierResponse,
    InterventionMaintenanceBase, InterventionMaintenanceCreate, InterventionMaintenanceUpdate, InterventionMaintenanceResponse, StatistiquesMaintenance,
    PersonnelBase, PersonnelCreate, PersonnelUpdate, PersonnelResponse,
    CongeAbsenceBase, CongeAbsenceCreate, CongeAbsenceUpdate, CongeAbsenceResponse,
    EvaluationPersonnelBase, EvaluationPersonnelCreate, EvaluationPersonnelResponse,
    HeureVacationBase, HeureVacationCreate, HeureVacationUpdate, HeureVacationResponse, MasseSalariale
)

from schemas.sync import (
    OperationType, SyncStatusEnum, SyncPriority,
    SyncQueueBase, SyncQueueCreate, SyncQueueUpdate, SyncQueueResponse,
    SyncBatchRequest, SyncBatchResponse,
    ConflictResolution, ResolveConflictRequest, SyncStats
)

__all__ = [
    # Auth
    "UserRole", "UserBase", "UserCreate", "UserUpdate", "UserProfile", "UserLogin",
    "TokenResponse",
    "TOTPSetupResponse", "TOTPVerifyRequest", "PasswordChangeRequest",
    # Administration
    "DomaineEtude", "NiveauFiliere", "FiliereBase", "FiliereCreate", "FiliereUpdate", "FiliereResponse",
    "UETypEnum", "UEBase", "UECreate", "UEUpdate", "UEResponse",
    "MaquetteStatut", "MaquetteBase", "MaquetteCreate", "MaquetteUpdate", "MaquetteResponse",
    "GenreEnum", "StatutEtudiantEnum", "EtudiantBase", "EtudiantCreate", "EtudiantUpdate", "EtudiantResponse",
    "TypeInscriptionEnum", "StatutWorkflowEnum", "NiveauEtude",
    "InscriptionBase", "InscriptionCreate", "InscriptionUpdate", "InscriptionResponse",
    "TypeSalleEnum", "SalleBase", "SalleCreate", "SalleUpdate", "SalleResponse",
    "TypeCoursEnum", "StatutCoursEnum", "JourSemaine", "SemaineType",
    "CoursBase", "CoursCreate", "CoursUpdate", "CoursResponse",
    "TypeEvalEnum", "NoteBase", "NoteCreate", "NoteUpdate", "NoteResponse",
    "StatutPresence", "ModePresence", "PresenceBase", "PresenceCreate", "PresenceUpdate", "PresenceResponse",
    # Finances
    "ModePaiementEnum", "OperateurPaiementEnum", "TypeRelanceEnum", "CanalRelanceEnum",
    "StatutBudgetEnum", "StatutDemandeAchatEnum", "UrgenceAchatEnum",
    "EtatBienEnum", "TypeBienEnum", "UrgenceMaintenanceEnum", "TypeMaintenanceEnum",
    "TypePersonnelEnum", "StatutPersonnelEnum", "TypeCongeEnum",
    "PaiementBase", "PaiementCreate", "PaiementUpdate", "PaiementResponse",
    "FraisScolariteBase", "FraisScolariteCreate", "FraisScolariteUpdate", "FraisScolariteResponse",
    "RelanceBase", "RelanceCreate", "RelanceResponse", "TableauRecouvrement",
    "LigneBudgetaire", "BudgetDepartementBase", "BudgetDepartementCreate", "BudgetDepartementUpdate", "BudgetDepartementResponse",
    "EcritureComptableBase", "EcritureComptableCreate", "EcritureComptableUpdate", "EcritureComptableResponse", "BalanceComptable",
    "FournisseurBase", "FournisseurCreate", "FournisseurUpdate", "FournisseurResponse",
    "DemandeAchatBase", "DemandeAchatCreate", "DemandeAchatUpdate", "DemandeAchatResponse",
    "BienImmobilierBase", "BienImmobilierCreate", "BienImmobilierUpdate", "BienImmobilierResponse",
    "InterventionMaintenanceBase", "InterventionMaintenanceCreate", "InterventionMaintenanceUpdate", "InterventionMaintenanceResponse", "StatistiquesMaintenance",
    "PersonnelBase", "PersonnelCreate", "PersonnelUpdate", "PersonnelResponse",
    "CongeAbsenceBase", "CongeAbsenceCreate", "CongeAbsenceUpdate", "CongeAbsenceResponse",
    "EvaluationPersonnelBase", "EvaluationPersonnelCreate", "EvaluationPersonnelResponse",
    "HeureVacationBase", "HeureVacationCreate", "HeureVacationUpdate", "HeureVacationResponse", "MasseSalariale",
    # Sync
    "OperationType", "SyncStatusEnum", "SyncPriority",
    "SyncQueueBase", "SyncQueueCreate", "SyncQueueUpdate", "SyncQueueResponse",
    "SyncBatchRequest", "SyncBatchResponse",
    "ConflictResolution", "ResolveConflictRequest", "SyncStats",
]
