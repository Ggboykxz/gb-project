"""
Routers pour le module Administration
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas.administration import (
    EtudiantCreate, EtudiantResponse, EtudiantUpdate,
    InscriptionCreate, InscriptionResponse, InscriptionUpdate,
    FiliereCreate, FiliereResponse, UECreate, UEResponse,
    SalleCreate, SalleResponse, CreneauCreate, CreneauResponse,
    NoteCreate, NoteResponse, DeliberationCreate, DeliberationResponse,
    DiplomeCreate, DiplomeResponse
)
from models.filiere import Filiere, UE, Maquette, Salle, Creneau
from models.etudiant import Etudiant, Inscription
from models.note import Note
from services.administration import (
    create_etudiant_service, get_etudiants_service, get_etudiant_service, update_etudiant_service,
    create_inscription_service, get_inscriptions_service, validate_inscription_service,
    create_filiere_service, get_filieres_service, create_ue_service,
    create_salle_service, get_salles_service,
    create_note_service, get_notes_service,
    verify_diplome_service
)

router = APIRouter(prefix="/api/v1/admin", tags=["Administration"])

# ==================== ÉTUDIANTS ====================

@router.post("/etudiants", response_model=EtudiantResponse, status_code=status.HTTP_201_CREATED)
async def create_etudiant(
    etudiant_data: EtudiantCreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer un nouvel étudiant"""
    return await create_etudiant_service(db, etudiant_data)

@router.get("/etudiants", response_model=List[EtudiantResponse])
async def get_etudiants(
    skip: int = 0,
    limit: int = 50,
    search: str = None,
    filiere_id: int = None,
    statut: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Liste des étudiants avec filtres"""
    return await get_etudiants_service(db, skip, limit, search, filiere_id, statut)

@router.get("/etudiants/{etudiant_id}", response_model=EtudiantResponse)
async def get_etudiant(
    etudiant_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Détails d'un étudiant"""
    etudiant = await get_etudiant_service(db, etudiant_id)
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return etudiant

@router.put("/etudiants/{etudiant_id}", response_model=EtudiantResponse)
async def update_etudiant(
    etudiant_id: int,
    etudiant_data: EtudiantUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Mettre à jour un étudiant"""
    return await update_etudiant_service(db, etudiant_id, etudiant_data)

# ==================== INSCRIPTIONS ====================

@router.post("/inscriptions", response_model=InscriptionResponse, status_code=status.HTTP_201_CREATED)
async def create_inscription(
    inscription_data: InscriptionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer une nouvelle inscription"""
    return await create_inscription_service(db, inscription_data)

@router.get("/inscriptions", response_model=List[InscriptionResponse])
async def get_inscriptions(
    skip: int = 0,
    limit: int = 50,
    annee_academique: str = None,
    filiere_id: int = None,
    statut: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Liste des inscriptions avec filtres"""
    return await get_inscriptions_service(db, skip, limit, annee_academique, filiere_id, statut)

@router.post("/inscriptions/{inscription_id}/validate", response_model=InscriptionResponse)
async def validate_inscription(
    inscription_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Valider une inscription (workflow hiérarchique)"""
    return await validate_inscription_service(db, inscription_id)

# ==================== FILIÈRES & MAQUETTES ====================

@router.post("/filieres", response_model=FiliereResponse, status_code=status.HTTP_201_CREATED)
async def create_filiere(
    filiere_data: FiliereCreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer une nouvelle filière"""
    return await create_filiere_service(db, filiere_data)

@router.get("/filieres", response_model=List[FiliereResponse])
async def get_filieres(
    db: AsyncSession = Depends(get_db)
):
    """Liste toutes les filières"""
    return await get_filieres_service(db)

@router.post("/ues", response_model=UEResponse, status_code=status.HTTP_201_CREATED)
async def create_ue(
    ue_data: UECreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer une nouvelle unité d'enseignement"""
    return await create_ue_service(db, ue_data)

# ==================== SALLES ====================

@router.post("/salles", response_model=SalleResponse, status_code=status.HTTP_201_CREATED)
async def create_salle(
    salle_data: SalleCreate,
    db: AsyncSession = Depends(get_db)
):
    """Créer une nouvelle salle"""
    return await create_salle_service(db, salle_data)

@router.get("/salles", response_model=List[SalleResponse])
async def get_salles(
    db: AsyncSession = Depends(get_db)
):
    """Liste toutes les salles"""
    return await get_salles_service(db)

# ==================== NOTES ====================

@router.post("/notes", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    db: AsyncSession = Depends(get_db)
):
    """Saisir une note"""
    return await create_note_service(db, note_data)

@router.get("/notes", response_model=List[NoteResponse])
async def get_notes(
    ue_id: int = None,
    inscription_id: int = None,
    db: AsyncSession = Depends(get_db)
):
    """Liste les notes avec filtres"""
    return await get_notes_service(db, ue_id, inscription_id)

# ==================== DIPLÔMES (endpoint public pour vérification) ====================

@router.get("/diplomes/verify/{qr_token}")
async def verify_diplome(
    qr_token: str,
    db: AsyncSession = Depends(get_db)
):
    """Vérifier l'authenticité d'un diplôme via QR Code (endpoint public)"""
    result = await verify_diplome_service(db, qr_token)
    if not result:
        raise HTTPException(status_code=404, detail="Diplôme non trouvé ou invalide")
    return result
