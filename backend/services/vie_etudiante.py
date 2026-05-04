"""
Services pour la vie étudiante et services
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_, or_
from typing import List, Optional
from datetime import datetime

from models.vie_etudiante import (
    Portfolio, ExperiencePortfolio, TypeBourse, DossierBourse,
    SuiviEtudiant, OffreStageEmploi, EntreprisePartenaire,
    Candidature, Alumni
)
from models.etudiant import Etudiant
from schemas.vie_etudiante import (
    PortfolioCreate, PortfolioUpdate,
    DossierBourseCreate, DossierBourseUpdate,
    SuiviEtudiantCreate, SuiviEtudiantUpdate,
    OffreStageEmploiCreate, OffreStageEmploiUpdate,
    CandidatureCreate, CandidatureUpdate,
    AlumniCreate, AlumniUpdate
)


# --- Portfolio Services ---
async def get_portfolio_by_etudiant(db: AsyncSession, etudiant_id: int) -> Optional[Portfolio]:
    result = await db.execute(
        select(Portfolio).where(Portfolio.etudiant_id == etudiant_id)
    )
    return result.scalar_one_or_none()


async def create_portfolio(db: AsyncSession, portfolio_data: PortfolioCreate) -> Portfolio:
    # Vérifier si un portfolio existe déjà
    existing = await get_portfolio_by_etudiant(db, portfolio_data.etudiant_id)
    if existing:
        return existing
    
    portfolio = Portfolio(**portfolio_data.model_dump())
    db.add(portfolio)
    await db.commit()
    await db.refresh(portfolio)
    return portfolio


async def update_portfolio(db: AsyncSession, etudiant_id: int, portfolio_data: PortfolioUpdate) -> Optional[Portfolio]:
    portfolio = await get_portfolio_by_etudiant(db, etudiant_id)
    if not portfolio:
        return None
    
    update_data = portfolio_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(portfolio, field, value)
    
    portfolio.updated_at = datetime.now()
    await db.commit()
    await db.refresh(portfolio)
    return portfolio


async def add_experience_portfolio(
    db: AsyncSession, portfolio_id: int, experience_data: dict
) -> ExperiencePortfolio:
    experience = ExperiencePortfolio(portfolio_id=portfolio_id, **experience_data)
    db.add(experience)
    await db.commit()
    await db.refresh(experience)
    return experience


async def delete_experience_portfolio(db: AsyncSession, experience_id: int) -> bool:
    result = await db.execute(
        select(ExperiencePortfolio).where(ExperiencePortfolio.id == experience_id)
    )
    experience = result.scalar_one_or_none()
    if not experience:
        return False
    
    await db.delete(experience)
    await db.commit()
    return True


# --- Bourses Services ---
async def get_all_types_bourse(db: AsyncSession, actif_only: bool = True) -> List[TypeBourse]:
    query = select(TypeBourse)
    if actif_only:
        query = query.where(TypeBourse.actif == True)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_type_bourse(db: AsyncSession, type_bourse_id: int) -> Optional[TypeBourse]:
    result = await db.execute(
        select(TypeBourse).where(TypeBourse.id == type_bourse_id)
    )
    return result.scalar_one_or_none()


async def create_type_bourse(db: AsyncSession, type_bourse_data: dict) -> TypeBourse:
    type_bourse = TypeBourse(**type_bourse_data)
    db.add(type_bourse)
    await db.commit()
    await db.refresh(type_bourse)
    return type_bourse


async def get_dossier_bourse(db: AsyncSession, dossier_id: int) -> Optional[DossierBourse]:
    result = await db.execute(
        select(DossierBourse).where(DossierBourse.id == dossier_id)
    )
    return result.scalar_one_or_none()


async def get_dossiers_by_etudiant(db: AsyncSession, etudiant_id: int) -> List[DossierBourse]:
    result = await db.execute(
        select(DossierBourse).where(DossierBourse.etudiant_id == etudiant_id)
    )
    return list(result.scalars().all())


async def create_dossier_bourse(db: AsyncSession, dossier_data: DossierBourseCreate) -> DossierBourse:
    dossier = DossierBourse(**dossier_data.model_dump())
    dossier.soumis_le = datetime.now()
    db.add(dossier)
    await db.commit()
    await db.refresh(dossier)
    return dossier


async def update_dossier_bourse(
    db: AsyncSession, dossier_id: int, dossier_data: DossierBourseUpdate
) -> Optional[DossierBourse]:
    dossier = await get_dossier_bourse(db, dossier_id)
    if not dossier:
        return None
    
    update_data = dossier_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(dossier, field, value)
    
    dossier.updated_at = datetime.now()
    await db.commit()
    await db.refresh(dossier)
    return dossier


async def calculate_score_social(etudiant_data: dict) -> float:
    """
    Calcule le score social pour une bourse selon critères gabonais
    - Moyenne académique (0-20) → 40%
    - Situation familiale → 30%
    - Géographie (éloignement) → 20%
    - Handicap → 10%
    """
    moyenne = etudiant_data.get("moyenne", 10) / 20 * 40
    situation_familiale = min(etudiant_data.get("nb_personnes_charge", 1), 5) / 5 * 30
    geographie = etudiant_data.get("score_geo", 0.5) * 20
    handicap = 10 if etudiant_data.get("handicap", False) else 0
    
    return round(moyenne + situation_familiale + geographie + handicap, 2)


# --- Suivi Étudiant Services ---
async def get_suivi_etudiant(db: AsyncSession, suivi_id: int) -> Optional[SuiviEtudiant]:
    result = await db.execute(
        select(SuiviEtudiant).where(SuiviEtudiant.id == suivi_id)
    )
    return result.scalar_one_or_none()


async def get_suivis_by_etudiant(db: AsyncSession, etudiant_id: int) -> List[SuiviEtudiant]:
    result = await db.execute(
        select(SuiviEtudiant).where(SuiviEtudiant.etudiant_id == etudiant_id)
    )
    return list(result.scalars().all())


async def get_suivis_by_conseiller(db: AsyncSession, conseiller_id: int, statut: Optional[str] = None) -> List[SuiviEtudiant]:
    query = select(SuiviEtudiant).where(SuiviEtudiant.conseiller_id == conseiller_id)
    if statut:
        query = query.where(SuiviEtudiant.statut == statut)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_suivi_etudiant(db: AsyncSession, suivi_data: SuiviEtudiantCreate) -> SuiviEtudiant:
    suivi = SuiviEtudiant(**suivi_data.model_dump())
    db.add(suivi)
    await db.commit()
    await db.refresh(suivi)
    return suivi


async def update_suivi_etudiant(
    db: AsyncSession, suivi_id: int, suivi_data: SuiviEtudiantUpdate
) -> Optional[SuiviEtudiant]:
    suivi = await get_suivi_etudiant(db, suivi_id)
    if not suivi:
        return None
    
    update_data = suivi_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(suivi, field, value)
    
    await db.commit()
    await db.refresh(suivi)
    return suivi


async def detect_decrochage(etudiant_data: dict) -> bool:
    """
    Détecte les signes de décrochage étudiant
    - Absence > 30%
    - Moyenne < 8
    - 3 notes manquantes ou plus
    """
    taux_absence = etudiant_data.get("taux_absence", 0)
    moyenne = etudiant_data.get("moyenne", 20)
    notes_manquantes = etudiant_data.get("notes_manquantes", 0)
    
    return taux_absence > 30 or moyenne < 8 or notes_manquantes >= 3


# --- Offres Stage/Emploi Services ---
async def get_all_offres(db: AsyncSession, statut: Optional[str] = None, type_offre: Optional[str] = None) -> List[OffreStageEmploi]:
    query = select(OffreStageEmploi)
    if statut:
        query = query.where(OffreStageEmploi.statut == statut)
    if type_offre:
        query = query.where(OffreStageEmploi.type_offre == type_offre)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_offre(db: AsyncSession, offre_id: int) -> Optional[OffreStageEmploi]:
    result = await db.execute(
        select(OffreStageEmploi).where(OffreStageEmploi.id == offre_id)
    )
    return result.scalar_one_or_none()


async def create_offre(db: AsyncSession, offre_data: OffreStageEmploiCreate) -> OffreStageEmploi:
    offre = OffreStageEmploi(**offre_data.model_dump())
    db.add(offre)
    await db.commit()
    await db.refresh(offre)
    return offre


async def update_offre(
    db: AsyncSession, offre_id: int, offre_data: OffreStageEmploiUpdate
) -> Optional[OffreStageEmploi]:
    offre = await get_offre(db, offre_id)
    if not offre:
        return None
    
    update_data = offre_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(offre, field, value)
    
    offre.updated_at = datetime.now()
    await db.commit()
    await db.refresh(offre)
    return offre


async def get_offres_by_entreprise(db: AsyncSession, entreprise_id: int) -> List[OffreStageEmploi]:
    result = await db.execute(
        select(OffreStageEmploi).where(OffreStageEmploi.entreprise_id == entreprise_id)
    )
    return list(result.scalars().all())


# --- Entreprises Services ---
async def get_all_entreprises(db: AsyncSession, actif_only: bool = True) -> List[EntreprisePartenaire]:
    query = select(EntreprisePartenaire)
    if actif_only:
        query = query.where(EntreprisePartenaire.actif == True)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_entreprise(db: AsyncSession, entreprise_id: int) -> Optional[EntreprisePartenaire]:
    result = await db.execute(
        select(EntreprisePartenaire).where(EntreprisePartenaire.id == entreprise_id)
    )
    return result.scalar_one_or_none()


async def create_entreprise(db: AsyncSession, entreprise_data: dict) -> EntreprisePartenaire:
    entreprise = EntreprisePartenaire(**entreprise_data)
    db.add(entreprise)
    await db.commit()
    await db.refresh(entreprise)
    return entreprise


# --- Candidatures Services ---
async def get_candidature(db: AsyncSession, candidature_id: int) -> Optional[Candidature]:
    result = await db.execute(
        select(Candidature).where(Candidature.id == candidature_id)
    )
    return result.scalar_one_or_none()


async def get_candidatures_by_etudiant(db: AsyncSession, etudiant_id: int) -> List[Candidature]:
    result = await db.execute(
        select(Candidature).where(Candidature.etudiant_id == etudiant_id)
    )
    return list(result.scalars().all())


async def get_candidatures_by_offre(db: AsyncSession, offre_id: int) -> List[Candidature]:
    result = await db.execute(
        select(Candidature).where(Candidature.offre_id == offre_id)
    )
    return list(result.scalars().all())


async def create_candidature(db: AsyncSession, candidature_data: CandidatureCreate) -> Candidature:
    candidature = Candidature(**candidature_data.model_dump())
    db.add(candidature)
    await db.commit()
    await db.refresh(candidature)
    return candidature


async def update_candidature(
    db: AsyncSession, candidature_id: int, candidature_data: CandidatureUpdate
) -> Optional[Candidature]:
    candidature = await get_candidature(db, candidature_id)
    if not candidature:
        return None
    
    update_data = candidature_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidature, field, value)
    
    await db.commit()
    await db.refresh(candidature)
    return candidature


# --- Alumni Services ---
async def get_alumni(db: AsyncSession, alumni_id: int) -> Optional[Alumni]:
    result = await db.execute(
        select(Alumni).where(Alumni.id == alumni_id)
    )
    return result.scalar_one_or_none()


async def get_alumni_by_etudiant(db: AsyncSession, etudiant_id: int) -> Optional[Alumni]:
    result = await db.execute(
        select(Alumni).where(Alumni.etudiant_id == etudiant_id)
    )
    return result.scalar_one_or_none()


async def get_all_alumni(db: AsyncSession, promo: Optional[str] = None) -> List[Alumni]:
    query = select(Alumni)
    if promo:
        query = query.where(Alumni.promo == promo)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_alumni(db: AsyncSession, alumni_data: AlumniCreate) -> Alumni:
    # Vérifier si alumni existe déjà
    existing = await get_alumni_by_etudiant(db, alumni_data.etudiant_id)
    if existing:
        return existing
    
    alumni = Alumni(**alumni_data.model_dump())
    db.add(alumni)
    await db.commit()
    await db.refresh(alumni)
    return alumni


async def update_alumni(
    db: AsyncSession, etudiant_id: int, alumni_data: AlumniUpdate
) -> Optional[Alumni]:
    alumni = await get_alumni_by_etudiant(db, etudiant_id)
    if not alumni:
        return None
    
    update_data = alumni_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(alumni, field, value)
    
    alumni.updated_at = datetime.now()
    await db.commit()
    await db.refresh(alumni)
    return alumni


async def get_mentors_disponibles(db: AsyncSession, domaine: Optional[str] = None) -> List[Alumni]:
    query = select(Alumni).where(Alumni.disponible_mentorat == True)
    if domaine:
        # Recherche dans le JSON des domaines d'expertise
        query = query.where(
            Alumnidomaines_expertise_json.cast(String).like(f"%{domaine}%")
        )
    result = await db.execute(query)
    return list(result.scalars().all())
