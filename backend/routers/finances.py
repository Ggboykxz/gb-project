"""
Router FastAPI pour le module Gestion Financière & Logistique
Phase 5 - GabonEdu Campus
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
from datetime import datetime, date

from database import get_db
from models.finances import (
    FraisScolarite, Paiement, Relance, BudgetDepartement, 
    EcritureComptable, Fournisseur, DemandeAchat, BienImmobilier,
    InterventionMaintenance, Personnel, CongeAbsence, EvaluationPersonnel,
    HeureVacation, ModePaiement, TypeRelance, CanalRelance, StatutBudget,
    StatutDemandeAchat, UrgenceAchat, EtatBien, TypeBien, TypeMaintenance,
    UrgenceMaintenance, TypePersonnel, StatutPersonnel, TypeConge
)
from schemas.finances import (
    FraisScolariteCreate, FraisScolariteUpdate, FraisScolariteResponse,
    PaiementCreate, PaiementUpdate, PaiementResponse,
    RelanceCreate, RelanceResponse, TableauRecouvrement,
    BudgetDepartementCreate, BudgetDepartementUpdate, BudgetDepartementResponse,
    EcritureComptableCreate, EcritureComptableUpdate, EcritureComptableResponse,
    BalanceComptable,
    FournisseurCreate, FournisseurUpdate, FournisseurResponse,
    DemandeAchatCreate, DemandeAchatUpdate, DemandeAchatResponse,
    BienImmobilierCreate, BienImmobilierUpdate, BienImmobilierResponse,
    InterventionMaintenanceCreate, InterventionMaintenanceUpdate, InterventionMaintenanceResponse,
    StatistiquesMaintenance,
    PersonnelCreate, PersonnelUpdate, PersonnelResponse,
    CongeAbsenceCreate, CongeAbsenceUpdate, CongeAbsenceResponse,
    EvaluationPersonnelCreate, EvaluationPersonnelResponse,
    HeureVacationCreate, HeureVacationUpdate, HeureVacationResponse,
    MasseSalariale
)
from security.auth import get_current_user, require_permission
from models.user import User as UserModel

router = APIRouter(prefix="/api/v1/finances", tags=["Finances"])


# ─── 5.1 FACTURATION & RECOUVREMENT ───

@router.post("/frais-scolarite", response_model=FraisScolariteResponse, status_code=status.HTTP_201_CREATED)
async def create_frais_scolarite(
    frais: FraisScolariteCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("frais_scolarite:create"))
):
    """Créer une configuration de frais de scolarité"""
    db_frais = FraisScolarite(**frais.model_dump())
    db.add(db_frais)
    await db.commit()
    await db.refresh(db_frais)
    return db_frais


@router.get("/frais-scolarite", response_model=List[FraisScolariteResponse])
async def list_frais_scolarite(
    filiere_id: Optional[int] = None,
    annee_academique: Optional[str] = None,
    niveau: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("frais_scolarite:read"))
):
    """Lister les configurations de frais de scolarité"""
    query = select(FraisScolarite)
    
    if filiere_id:
        query = query.where(FraisScolarite.filiere_id == filiere_id)
    if annee_academique:
        query = query.where(FraisScolarite.annee_academique == annee_academique)
    if niveau:
        query = query.where(FraisScolarite.niveau == niveau)
    
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/frais-scolarite/{frais_id}", response_model=FraisScolariteResponse)
async def get_frais_scolarite(
    frais_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("frais_scolarite:read"))
):
    """Obtenir une configuration de frais spécifique"""
    result = await db.execute(select(FraisScolarite).where(FraisScolarite.id == frais_id))
    frais = result.scalar_one_or_none()
    if not frais:
        raise HTTPException(status_code=404, detail="Frais de scolarité non trouvés")
    return frais


@router.put("/frais-scolarite/{frais_id}", response_model=FraisScolariteResponse)
async def update_frais_scolarite(
    frais_id: int,
    frais_update: FraisScolariteUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("frais_scolarite:update"))
):
    """Mettre à jour une configuration de frais"""
    result = await db.execute(select(FraisScolarite).where(FraisScolarite.id == frais_id))
    frais = result.scalar_one_or_none()
    if not frais:
        raise HTTPException(status_code=404, detail="Frais de scolarité non trouvés")
    
    update_data = frais_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(frais, key, value)
    
    await db.commit()
    await db.refresh(frais)
    return frais


@router.post("/paiements", response_model=PaiementResponse, status_code=status.HTTP_201_CREATED)
async def create_paiement(
    paiement: PaiementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("paiement:create"))
):
    """Enregistrer un nouveau paiement"""
    db_paiement = Paiement(**paiement.model_dump())
    db.add(db_paiement)
    await db.commit()
    await db.refresh(db_paiement)
    return db_paiement


@router.get("/paiements", response_model=List[PaiementResponse])
async def list_paiements(
    inscription_id: Optional[int] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    mode_paiement: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("paiement:read"))
):
    """Lister les paiements avec filtres"""
    query = select(Paiement)
    
    if inscription_id:
        query = query.where(Paiement.inscription_id == inscription_id)
    if date_debut:
        query = query.where(Paiement.date_paiement >= datetime.combine(date_debut, datetime.min.time()))
    if date_fin:
        query = query.where(Paiement.date_paiement <= datetime.combine(date_fin, datetime.max.time()))
    if mode_paiement:
        query = query.where(Paiement.mode_paiement == mode_paiement)
    
    query = query.offset(skip).limit(limit).order_by(Paiement.date_paiement.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/recouvrement/tableau", response_model=TableauRecouvrement)
async def get_tableau_recouvrement(
    annee_academique: Optional[str] = None,
    filiere_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("paiement:read"))
):
    """Obtenir le tableau de recouvrement global"""
    # Calcul simplifié - à implémenter complètement selon besoins métier
    return TableauRecouvrement(
        total_a_recouvrer=0.0,
        total_recouvre=0.0,
        taux_recouvrement=0.0,
        nombre_impayes=0,
        par_filiere=[],
        par_echeance=[]
    )


@router.post("/relances", response_model=RelanceResponse, status_code=status.HTTP_201_CREATED)
async def create_relance(
    relance: RelanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("relance:create"))
):
    """Créer une relance pour impayé"""
    db_relance = Relance(**relance.model_dump())
    db.add(db_relance)
    await db.commit()
    await db.refresh(db_relance)
    return db_relance


@router.get("/relances", response_model=List[RelanceResponse])
async def list_relances(
    inscription_id: Optional[int] = None,
    type_relance: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(require_permission("relance:read"))
):
    """Lister les relances envoyées"""
    query = select(Relance)
    
    if inscription_id:
        query = query.where(Relance.inscription_id == inscription_id)
    if type_relance:
        query = query.where(Relance.type_relance == type_relance)
    
    result = await db.execute(query.order_by(Relance.date_envoi.desc()))
    return result.scalars().all()


# ─── 5.2 BUDGET & COMPTABILITÉ ANALYTIQUE ───

@router.post("/budgets", response_model=BudgetDepartementResponse, status_code=status.HTTP_201_CREATED)
async def create_budget_departement(
    budget: BudgetDepartementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer un budget départemental"""
    db_budget = BudgetDepartement(**budget.model_dump())
    db.add(db_budget)
    await db.commit()
    await db.refresh(db_budget)
    return db_budget


@router.get("/budgets", response_model=List[BudgetDepartementResponse])
async def list_budgets(
    departement_id: Optional[int] = None,
    annee: Optional[str] = None,
    statut: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les budgets"""
    query = select(BudgetDepartement)
    
    if departement_id:
        query = query.where(BudgetDepartement.departement_id == departement_id)
    if annee:
        query = query.where(BudgetDepartement.annee == annee)
    if statut:
        query = query.where(BudgetDepartement.statut == statut)
    
    result = await db.execute(query.order_by(BudgetDepartement.annee.desc()))
    return result.scalars().all()


@router.post("/ecritures-comptables", response_model=EcritureComptableResponse, status_code=status.HTTP_201_CREATED)
async def create_ecriture_comptable(
    ecriture: EcritureComptableCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer une écriture comptable"""
    db_ecriture = EcritureComptable(**ecriture.model_dump())
    db.add(db_ecriture)
    await db.commit()
    await db.refresh(db_ecriture)
    return db_ecriture


@router.get("/ecritures-comptables", response_model=List[EcritureComptableResponse])
async def list_ecritures_comptables(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    compte_debit: Optional[str] = None,
    compte_credit: Optional[str] = None,
    departement_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les écritures comptables"""
    query = select(EcritureComptable)
    
    if date_debut:
        query = query.where(EcritureComptable.date_ecriture >= date_debut)
    if date_fin:
        query = query.where(EcritureComptable.date_ecriture <= date_fin)
    if compte_debit:
        query = query.where(EcritureComptable.compte_debit == compte_debit)
    if compte_credit:
        query = query.where(EcritureComptable.compte_credit == compte_credit)
    if departement_id:
        query = query.where(EcritureComptable.departement_id == departement_id)
    
    query = query.offset(skip).limit(limit).order_by(EcritureComptable.date_ecriture.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/comptabilite/balance", response_model=List[BalanceComptable])
async def get_balance_comptable(
    annee: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Obtenir la balance comptable OHADA"""
    # Implémentation simplifiée - nécessite agrégation SQL complète
    return []


# ─── 5.3 MARCHÉS PUBLICS INTERNES ───

@router.post("/fournisseurs", response_model=FournisseurResponse, status_code=status.HTTP_201_CREATED)
async def create_fournisseur(
    fournisseur: FournisseurCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer un nouveau fournisseur"""
    db_fournisseur = Fournisseur(**fournisseur.model_dump())
    db.add(db_fournisseur)
    await db.commit()
    await db.refresh(db_fournisseur)
    return db_fournisseur


@router.get("/fournisseurs", response_model=List[FournisseurResponse])
async def list_fournisseurs(
    agree_only: bool = False,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les fournisseurs"""
    query = select(Fournisseur)
    
    if agree_only:
        query = query.where(Fournisseur.agree == True)
    if search:
        query = query.where(or_(
            Fournisseur.raison_sociale.ilike(f"%{search}%"),
            Fournisseur.nif_gabon.ilike(f"%{search}%")
        ))
    
    result = await db.execute(query.order_by(Fournisseur.raison_sociale))
    return result.scalars().all()


@router.post("/demandes-achat", response_model=DemandeAchatResponse, status_code=status.HTTP_201_CREATED)
async def create_demande_achat(
    demande: DemandeAchatCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer une demande d'achat"""
    db_demande = DemandeAchat(**demande.model_dump())
    db.add(db_demande)
    await db.commit()
    await db.refresh(db_demande)
    return db_demande


@router.get("/demandes-achat", response_model=List[DemandeAchatResponse])
async def list_demandes_achat(
    departement_id: Optional[int] = None,
    statut_workflow: Optional[str] = None,
    urgence: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les demandes d'achat"""
    query = select(DemandeAchat)
    
    if departement_id:
        query = query.where(DemandeAchat.departement_id == departement_id)
    if statut_workflow:
        query = query.where(DemandeAchat.statut_workflow == statut_workflow)
    if urgence:
        query = query.where(DemandeAchat.urgence == urgence)
    
    result = await db.execute(query.order_by(DemandeAchat.date_demande.desc()))
    return result.scalars().all()


@router.put("/demandes-achat/{demande_id}", response_model=DemandeAchatResponse)
async def update_demande_achat(
    demande_id: int,
    demande_update: DemandeAchatUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Mettre à jour une demande d'achat (workflow)"""
    result = await db.execute(select(DemandeAchat).where(DemandeAchat.id == demande_id))
    demande = result.scalar_one_or_none()
    if not demande:
        raise HTTPException(status_code=404, detail="Demande d'achat non trouvée")
    
    update_data = demande_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(demande, key, value)
    
    await db.commit()
    await db.refresh(demande)
    return demande


# ─── 5.4 PATRIMOINE & MAINTENANCE ───

@router.post("/biens-immobiliers", response_model=BienImmobilierResponse, status_code=status.HTTP_201_CREATED)
async def create_bien_immobilier(
    bien: BienImmobilierCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer un nouveau bien immobilier/équipement"""
    db_bien = BienImmobilier(**bien.model_dump())
    db.add(db_bien)
    await db.commit()
    await db.refresh(db_bien)
    return db_bien


@router.get("/biens-immobiliers", response_model=List[BienImmobilierResponse])
async def list_biens_immobiliers(
    type_bien: Optional[str] = None,
    etat: Optional[str] = None,
    batiment: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les biens immobiliers et équipements"""
    query = select(BienImmobilier)
    
    if type_bien:
        query = query.where(BienImmobilier.type_bien == type_bien)
    if etat:
        query = query.where(BienImmobilier.etat == etat)
    if batiment:
        query = query.where(BienImmobilier.batiment == batiment)
    
    result = await db.execute(query.order_by(BienImmobilier.designation))
    return result.scalars().all()


@router.post("/interventions-maintenance", response_model=InterventionMaintenanceResponse, status_code=status.HTTP_201_CREATED)
async def create_intervention_maintenance(
    intervention: InterventionMaintenanceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer une intervention de maintenance"""
    db_intervention = InterventionMaintenance(**intervention.model_dump())
    db.add(db_intervention)
    await db.commit()
    await db.refresh(db_intervention)
    return db_intervention


@router.get("/interventions-maintenance", response_model=List[InterventionMaintenanceResponse])
async def list_interventions_maintenance(
    bien_id: Optional[int] = None,
    statut: Optional[str] = None,
    urgence: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les interventions de maintenance"""
    query = select(InterventionMaintenance)
    
    if bien_id:
        query = query.where(InterventionMaintenance.bien_id == bien_id)
    if statut:
        query = query.where(InterventionMaintenance.statut == statut)
    if urgence:
        query = query.where(InterventionMaintenance.urgence == urgence)
    
    result = await db.execute(query.order_by(InterventionMaintenance.date_demande.desc()))
    return result.scalars().all()


@router.get("/maintenance/statistiques", response_model=StatistiquesMaintenance)
async def get_statistiques_maintenance(
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Obtenir les statistiques de maintenance"""
    # Implémentation simplifiée
    return StatistiquesMaintenance(
        total_interventions=0,
        par_statut={},
        par_urgence={},
        cout_total=0.0,
        temps_moyen_resolution_jours=0.0
    )


# ─── 5.5 RESSOURCES HUMAINES ───

@router.post("/personnels", response_model=PersonnelResponse, status_code=status.HTTP_201_CREATED)
async def create_personnel(
    personnel: PersonnelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer un nouveau membre du personnel"""
    db_personnel = Personnel(**personnel.model_dump())
    db.add(db_personnel)
    await db.commit()
    await db.refresh(db_personnel)
    return db_personnel


@router.get("/personnels", response_model=List[PersonnelResponse])
async def list_personnels(
    type_personnel: Optional[str] = None,
    departement_id: Optional[int] = None,
    statut: Optional[str] = None,
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister le personnel"""
    query = select(Personnel)
    
    if type_personnel:
        query = query.where(Personnel.type_personnel == type_personnel)
    if departement_id:
        query = query.where(Personnel.departement_id == departement_id)
    if statut:
        query = query.where(Personnel.statut == statut)
    if search:
        query = query.where(or_(
            Personnel.nom.ilike(f"%{search}%"),
            Personnel.prenom.ilike(f"%{search}%"),
            Personnel.matricule.ilike(f"%{search}%")
        ))
    
    result = await db.execute(query.order_by(Personnel.nom))
    return result.scalars().all()


@router.post("/conges-absences", response_model=CongeAbsenceResponse, status_code=status.HTTP_201_CREATED)
async def create_conge_absence(
    conge: CongeAbsenceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Demander un congé ou déclarer une absence"""
    db_conge = CongeAbsence(**conge.model_dump())
    db.add(db_conge)
    await db.commit()
    await db.refresh(db_conge)
    return db_conge


@router.get("/conges-absences", response_model=List[CongeAbsenceResponse])
async def list_conges_absences(
    personnel_id: Optional[int] = None,
    type_conge: Optional[str] = None,
    statut: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les congés et absences"""
    query = select(CongeAbsence)
    
    if personnel_id:
        query = query.where(CongeAbsence.personnel_id == personnel_id)
    if type_conge:
        query = query.where(CongeAbsence.type_conge == type_conge)
    if statut:
        query = query.where(CongeAbsence.statut == statut)
    
    result = await db.execute(query.order_by(CongeAbsence.date_demande.desc()))
    return result.scalars().all()


@router.post("/evaluations-personnel", response_model=EvaluationPersonnelResponse, status_code=status.HTTP_201_CREATED)
async def create_evaluation_personnel(
    evaluation: EvaluationPersonnelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Créer une évaluation de personnel"""
    db_evaluation = EvaluationPersonnel(**evaluation.model_dump())
    db.add(db_evaluation)
    await db.commit()
    await db.refresh(db_evaluation)
    return db_evaluation


@router.get("/evaluations-personnel", response_model=List[EvaluationPersonnelResponse])
async def list_evaluations_personnel(
    personnel_id: Optional[int] = None,
    annee: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les évaluations de personnel"""
    query = select(EvaluationPersonnel)
    
    if personnel_id:
        query = query.where(EvaluationPersonnel.personnel_id == personnel_id)
    if annee:
        query = query.where(EvaluationPersonnel.annee == annee)
    
    result = await db.execute(query.order_by(EvaluationPersonnel.annee.desc()))
    return result.scalars().all()


@router.post("/heures-vacation", response_model=HeureVacationResponse, status_code=status.HTTP_201_CREATED)
async def create_heure_vacation(
    heure: HeureVacationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Déclarer des heures de vacation"""
    db_heure = HeureVacation(**heure.model_dump())
    # Calcul automatique du montant
    db_heure.montant_total_fcfa = heure.nombre_heures * heure.taux_horaire_fcfa
    db.add(db_heure)
    await db.commit()
    await db.refresh(db_heure)
    return db_heure


@router.get("/heures-vacation", response_model=List[HeureVacationResponse])
async def list_heures_vacation(
    vacataire_id: Optional[int] = None,
    statut_paiement: Optional[str] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Lister les heures de vacation"""
    query = select(HeureVacation)
    
    if vacataire_id:
        query = query.where(HeureVacation.vacataire_id == vacataire_id)
    if statut_paiement:
        query = query.where(HeureVacation.statut_paiement == statut_paiement)
    if date_debut:
        query = query.where(HeureVacation.date_vacation >= date_debut)
    if date_fin:
        query = query.where(HeureVacation.date_vacation <= date_fin)
    
    result = await db.execute(query.order_by(HeureVacation.date_vacation.desc()))
    return result.scalars().all()


@router.get("/rh/masse-salariale", response_model=MasseSalariale)
async def get_masse_salariale(
    annee: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    """Obtenir les statistiques de masse salariale"""
    # Implémentation simplifiée
    return MasseSalariale(
        total_brut=0.0,
        total_vacations=0.0,
        effectif_total=0,
        par_departement=[],
        par_type_personnel=[]
    )
