"""
Router pour la vie étudiante et services
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db
from security.auth import get_current_user, require_permission
from models.user import User, UserRole
from schemas.vie_etudiante import (
    PortfolioResponse, PortfolioCreate, PortfolioUpdate,
    ExperiencePortfolioResponse, ExperiencePortfolioCreate,
    TypeBourseResponse, TypeBourseCreate, TypeBourseUpdate,
    DossierBourseResponse, DossierBourseCreate, DossierBourseUpdate,
    SuiviEtudiantResponse, SuiviEtudiantCreate, SuiviEtudiantUpdate,
    OffreStageEmploiResponse, OffreStageEmploiCreate, OffreStageEmploiUpdate,
    EntreprisePartenaireResponse, EntreprisePartenaireCreate, EntreprisePartenaireUpdate,
    CandidatureResponse, CandidatureCreate, CandidatureUpdate,
    AlumniResponse, AlumniCreate, AlumniUpdate
)
import services.vie_etudiante as service


router = APIRouter()


# ==================== PORTFOLIO ====================

@router.get("/portfolio/etudiant/{etudiant_id}", response_model=PortfolioResponse)
async def get_portfolio(
    etudiant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer le portfolio d'un étudiant"""
    portfolio = await service.get_portfolio_by_etudiant(db, etudiant_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio non trouvé")
    return portfolio


@router.post("/portfolio", response_model=PortfolioResponse)
async def create_portfolio(
    portfolio_data: PortfolioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("portfolio:create"))
):
    """Créer un portfolio étudiant"""
    return await service.create_portfolio(db, portfolio_data)


@router.put("/portfolio/etudiant/{etudiant_id}", response_model=PortfolioResponse)
async def update_portfolio(
    etudiant_id: int,
    portfolio_data: PortfolioUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("portfolio:update"))
):
    """Mettre à jour un portfolio"""
    portfolio = await service.update_portfolio(db, etudiant_id, portfolio_data)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio non trouvé")
    return portfolio


@router.post("/portfolio/{portfolio_id}/experiences", response_model=ExperiencePortfolioResponse)
async def add_experience(
    portfolio_id: int,
    experience_data: ExperiencePortfolioCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("portfolio:update"))
):
    """Ajouter une expérience au portfolio"""
    if experience_data.portfolio_id != portfolio_id:
        raise HTTPException(status_code=400, detail="ID portfolio incohérent")
    
    experience = await service.add_experience_portfolio(db, portfolio_id, experience_data.model_dump())
    return experience


@router.delete("/portfolio/experiences/{experience_id}")
async def delete_experience(
    experience_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("portfolio:delete"))
):
    """Supprimer une expérience du portfolio"""
    success = await service.delete_experience_portfolio(db, experience_id)
    if not success:
        raise HTTPException(status_code=404, detail="Expérience non trouvée")
    return {"message": "Expérience supprimée avec succès"}


# ==================== BOURSES ====================

@router.get("/bourses/types", response_model=List[TypeBourseResponse])
async def get_types_bourses(
    actif_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les types de bourses disponibles"""
    return await service.get_all_types_bourse(db, actif_only)


@router.post("/bourses/types", response_model=TypeBourseResponse)
async def create_type_bourse(
    type_bourse_data: TypeBourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("bourses:admin"))
):
    """Créer un nouveau type de bourse"""
    return await service.create_type_bourse(db, type_bourse_data.model_dump())


@router.get("/bourses/dossiers/{dossier_id}", response_model=DossierBourseResponse)
async def get_dossier_bourse(
    dossier_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un dossier de bourse"""
    dossier = await service.get_dossier_bourse(db, dossier_id)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return dossier


@router.get("/bourses/dossiers/etudiant/{etudiant_id}", response_model=List[DossierBourseResponse])
async def get_dossiers_etudiant(
    etudiant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les dossiers de bourse d'un étudiant"""
    return await service.get_dossiers_by_etudiant(db, etudiant_id)


@router.post("/bourses/dossiers", response_model=DossierBourseResponse)
async def create_dossier_bourse(
    dossier_data: DossierBourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("bourses:create"))
):
    """Créer un dossier de demande de bourse"""
    # Calcul automatique du score social
    etudiant_data = {"moyenne": 12, "nb_personnes_charge": 3, "score_geo": 0.7, "handicap": False}
    score = await service.calculate_score_social(etudiant_data)
    dossier_data_dict = dossier_data.model_dump()
    dossier_data_dict["score_social"] = score
    
    return await service.create_dossier_bourse(db, DossierBourseCreate(**dossier_data_dict))


@router.put("/bourses/dossiers/{dossier_id}", response_model=DossierBourseResponse)
async def update_dossier_bourse(
    dossier_id: int,
    dossier_data: DossierBourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("bourses:update"))
):
    """Mettre à jour un dossier de bourse (traitement par admin)"""
    dossier = await service.update_dossier_bourse(db, dossier_id, dossier_data)
    if not dossier:
        raise HTTPException(status_code=404, detail="Dossier non trouvé")
    return dossier


# ==================== SUIVI ÉTUDIANT ====================

@router.get("/suivis/{suivi_id}", response_model=SuiviEtudiantResponse)
async def get_suivi(
    suivi_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer un suivi étudiant"""
    suivi = await service.get_suivi_etudiant(db, suivi_id)
    if not suivi:
        raise HTTPException(status_code=404, detail="Suivi non trouvé")
    return suivi


@router.get("/suivis/etudiant/{etudiant_id}", response_model=List[SuiviEtudiantResponse])
async def get_suivis_etudiant(
    etudiant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les suivis d'un étudiant"""
    return await service.get_suivis_by_etudiant(db, etudiant_id)


@router.get("/suivis/conseiller/{conseiller_id}", response_model=List[SuiviEtudiantResponse])
async def get_suivis_conseiller(
    conseiller_id: int,
    statut: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les suivis d'un conseiller pédagogique"""
    return await service.get_suivis_by_conseiller(db, conseiller_id, statut)


@router.post("/suivis", response_model=SuiviEtudiantResponse)
async def create_suivi(
    suivi_data: SuiviEtudiantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("suivis:create"))
):
    """Créer un suivi étudiant (alerte décrochage, échec, etc.)"""
    return await service.create_suivi_etudiant(db, suivi_data)


@router.put("/suivis/{suivi_id}", response_model=SuiviEtudiantResponse)
async def update_suivi(
    suivi_id: int,
    suivi_data: SuiviEtudiantUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("suivis:update"))
):
    """Mettre à jour un suivi étudiant"""
    suivi = await service.update_suivi_etudiant(db, suivi_id, suivi_data)
    if not suivi:
        raise HTTPException(status_code=404, detail="Suivi non trouvé")
    return suivi


# ==================== OFFRES STAGE/EMPLOI ====================

@router.get("/offres", response_model=List[OffreStageEmploiResponse])
async def get_offres(
    statut: Optional[str] = None,
    type_offre: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les offres de stage/emploi"""
    return await service.get_all_offres(db, statut, type_offre)


@router.get("/offres/{offre_id}", response_model=OffreStageEmploiResponse)
async def get_offre(
    offre_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Récupérer une offre détaillée"""
    offre = await service.get_offre(db, offre_id)
    if not offre:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return offre


@router.post("/offres", response_model=OffreStageEmploiResponse)
async def create_offre(
    offre_data: OffreStageEmploiCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("offres:create"))
):
    """Créer une nouvelle offre de stage/emploi"""
    return await service.create_offre(db, offre_data)


@router.put("/offres/{offre_id}", response_model=OffreStageEmploiResponse)
async def update_offre(
    offre_id: int,
    offre_data: OffreStageEmploiUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("offres:update"))
):
    """Mettre à jour une offre"""
    offre = await service.update_offre(db, offre_id, offre_data)
    if not offre:
        raise HTTPException(status_code=404, detail="Offre non trouvée")
    return offre


# ==================== ENTREPRISES PARTENAIRES ====================

@router.get("/entreprises", response_model=List[EntreprisePartenaireResponse])
async def get_entreprises(
    actif_only: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les entreprises partenaires"""
    return await service.get_all_entreprises(db, actif_only)


@router.post("/entreprises", response_model=EntreprisePartenaireResponse)
async def create_entreprise(
    entreprise_data: EntreprisePartenaireCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("entreprises:create"))
):
    """Ajouter une entreprise partenaire"""
    return await service.create_entreprise(db, entreprise_data.model_dump())


# ==================== CANDIDATURES ====================

@router.get("/candidatures/offre/{offre_id}", response_model=List[CandidatureResponse])
async def get_candidatures_offre(
    offre_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les candidatures pour une offre"""
    return await service.get_candidatures_by_offre(db, offre_id)


@router.get("/candidatures/etudiant/{etudiant_id}", response_model=List[CandidatureResponse])
async def get_candidatures_etudiant(
    etudiant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les candidatures d'un étudiant"""
    return await service.get_candidatures_by_etudiant(db, etudiant_id)


@router.post("/candidatures", response_model=CandidatureResponse)
async def create_candidature(
    candidature_data: CandidatureCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("candidatures:create"))
):
    """Postuler à une offre"""
    return await service.create_candidature(db, candidature_data)


@router.put("/candidatures/{candidature_id}", response_model=CandidatureResponse)
async def update_candidature(
    candidature_id: int,
    candidature_data: CandidatureUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("candidatures:update"))
):
    """Mettre à jour une candidature (traitement par entreprise)"""
    candidature = await service.update_candidature(db, candidature_id, candidature_data)
    if not candidature:
        raise HTTPException(status_code=404, detail="Candidature non trouvée")
    return candidature


# ==================== ALUMNI ====================

@router.get("/alumni", response_model=List[AlumniResponse])
async def get_alumni(
    promo: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les anciens étudiants (alumni)"""
    return await service.get_all_alumni(db, promo)


@router.get("/alumni/mentors", response_model=List[AlumniResponse])
async def get_mentors(
    domaine: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Lister les alumni disponibles pour le mentorat"""
    return await service.get_mentors_disponibles(db, domaine)


@router.post("/alumni", response_model=AlumniResponse)
async def create_alumni(
    alumni_data: AlumniCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("alumni:create"))
):
    """Créer un profil alumni"""
    return await service.create_alumni(db, alumni_data)


@router.put("/alumni/etudiant/{etudiant_id}", response_model=AlumniResponse)
async def update_alumni(
    etudiant_id: int,
    alumni_data: AlumniUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_permission("alumni:update"))
):
    """Mettre à jour un profil alumni"""
    alumni = await service.update_alumni(db, etudiant_id, alumni_data)
    if not alumni:
        raise HTTPException(status_code=404, detail="Profil alumni non trouvé")
    return alumni
