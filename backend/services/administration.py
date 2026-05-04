"""
Services pour le module Administration
Business logic pour la gestion académique
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional
from datetime import datetime
import uuid

from models.filiere import Filiere, UE, Maquette
from models.etudiant import Etudiant
from models.inscription import Inscription
from models.note import Note
from models.cours import Salle

# Import schemas mais pas CreneauCreate/DeliberationCreate/DiplomeCreate car ces modèles n'existent pas encore
from schemas.administration import (
    EtudiantCreate, EtudiantUpdate, InscriptionCreate, InscriptionUpdate,
    FiliereCreate, UECreate, SalleCreate,
    NoteCreate
)


# ==================== ÉTUDIANTS ====================

async def create_etudiant_service(db: AsyncSession, etudiant_data: EtudiantCreate) -> Etudiant:
    """Créer un nouvel étudiant avec NIP unique"""
    # Vérifier unicité du NIP
    result = await db.execute(select(Etudiant).where(Etudiant.nip_gabon == etudiant_data.nip_gabon))
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError(f"Le NIP {etudiant_data.nip_gabon} existe déjà")
    
    etudiant = Etudiant(**etudiant_data.model_dump())
    db.add(etudiant)
    await db.commit()
    await db.refresh(etudiant)
    return etudiant


async def get_etudiants_service(
    db: AsyncSession, 
    skip: int = 0, 
    limit: int = 50,
    search: str = None,
    filiere_id: int = None,
    statut: str = None
) -> List[Etudiant]:
    """Liste des étudiants avec filtres"""
    query = select(Etudiant)
    
    conditions = []
    if search:
        search_filter = or_(
            Etudiant.nom.ilike(f"%{search}%"),
            Etudiant.prenom.ilike(f"%{search}%"),
            Etudiant.email.ilike(f"%{search}%"),
            Etudiant.nip_gabon.ilike(f"%{search}%")
        )
        conditions.append(search_filter)
    
    if statut:
        conditions.append(Etudiant.statut == statut)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit).order_by(Etudiant.nom)
    result = await db.execute(query)
    return list(result.scalars().all())


async def get_etudiant_service(db: AsyncSession, etudiant_id: int) -> Optional[Etudiant]:
    """Récupérer un étudiant par ID"""
    result = await db.execute(select(Etudiant).where(Etudiant.id == etudiant_id))
    return result.scalar_one_or_none()


async def update_etudiant_service(
    db: AsyncSession, 
    etudiant_id: int, 
    etudiant_data: EtudiantUpdate
) -> Etudiant:
    """Mettre à jour un étudiant"""
    result = await db.execute(select(Etudiant).where(Etudiant.id == etudiant_id))
    etudiant = result.scalar_one_or_none()
    if not etudiant:
        raise ValueError("Étudiant non trouvé")
    
    update_data = etudiant_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(etudiant, field, value)
    
    await db.commit()
    await db.refresh(etudiant)
    return etudiant


# ==================== INSCRIPTIONS ====================

async def create_inscription_service(db: AsyncSession, inscription_data: InscriptionCreate) -> Inscription:
    """Créer une nouvelle inscription"""
    inscription = Inscription(
        **inscription_data.model_dump(),
        statut_workflow="soumis",
        date_soumission=datetime.utcnow()
    )
    db.add(inscription)
    await db.commit()
    await db.refresh(inscription)
    return inscription


async def get_inscriptions_service(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 50,
    annee_academique: str = None,
    filiere_id: int = None,
    statut: str = None
) -> List[Inscription]:
    """Liste des inscriptions avec filtres"""
    query = select(Inscription)
    
    conditions = []
    if annee_academique:
        conditions.append(Inscription.annee_academique == annee_academique)
    if filiere_id:
        conditions.append(Inscription.filiere_id == filiere_id)
    if statut:
        conditions.append(Inscription.statut_workflow == statut)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.offset(skip).limit(limit).order_by(Inscription.date_soumission.desc())
    result = await db.execute(query)
    return list(result.scalars().all())


async def validate_inscription_service(
    db: AsyncSession, 
    inscription_id: int, 
    user_id: int
) -> Inscription:
    """Valider une inscription (avancer dans le workflow)"""
    result = await db.execute(select(Inscription).where(Inscription.id == inscription_id))
    inscription = result.scalar_one_or_none()
    if not inscription:
        raise ValueError("Inscription non trouvée")
    
    # Workflow hiérarchique
    workflow_order = ["soumis", "validé_scol", "validé_doyen", "confirmé"]
    current_index = workflow_order.index(inscription.statut_workflow)
    
    if current_index < len(workflow_order) - 1:
        inscription.statut_workflow = workflow_order[current_index + 1]
        await db.commit()
        await db.refresh(inscription)
    
    return inscription


# ==================== FILIÈRES ====================

async def create_filiere_service(db: AsyncSession, filiere_data: FiliereCreate) -> Filiere:
    """Créer une nouvelle filière"""
    filiere = Filiere(**filiere_data.model_dump())
    db.add(filiere)
    await db.commit()
    await db.refresh(filiere)
    return filiere


async def get_filieres_service(db: AsyncSession) -> List[Filiere]:
    """Liste toutes les filières"""
    result = await db.execute(select(Filiere).order_by(Filiere.libelle))
    return list(result.scalars().all())


async def create_ue_service(db: AsyncSession, ue_data: UECreate) -> UE:
    """Créer une nouvelle unité d'enseignement"""
    ue = UE(**ue_data.model_dump())
    db.add(ue)
    await db.commit()
    await db.refresh(ue)
    return ue


# ==================== SALLES & CRÉNEAUX ====================

async def create_salle_service(db: AsyncSession, salle_data: SalleCreate) -> Salle:
    """Créer une nouvelle salle"""
    salle = Salle(**salle_data.model_dump())
    db.add(salle)
    await db.commit()
    await db.refresh(salle)
    return salle


async def get_salles_service(db: AsyncSession) -> List[Salle]:
    """Liste toutes les salles"""
    result = await db.execute(select(Salle).where(Salle.disponible == True).order_by(Salle.nom))
    return list(result.scalars().all())


# ==================== NOTES ====================

async def create_note_service(db: AsyncSession, note_data: NoteCreate) -> Note:
    """Saisir une note avec validation"""
    # Validation de la note (0-20)
    if note_data.note is not None and (note_data.note < 0 or note_data.note > 20):
        raise ValueError("La note doit être comprise entre 0 et 20")
    
    note = Note(
        inscription_id=note_data.inscription_id,
        ue_id=note_data.ue_id,
        type_eval=note_data.type_eval,
        note=note_data.note,
        coefficient=note_data.coefficient,
        absence_justifiee=note_data.absence_justifiee,
        commentaires=note_data.commentaires,
        saisi_par=note_data.saisi_par,
        date_saisie=datetime.utcnow(),
        validee=False
    )
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def get_notes_service(
    db: AsyncSession,
    ue_id: int = None,
    inscription_id: int = None
) -> List[Note]:
    """Liste les notes avec filtres"""
    query = select(Note).order_by(Note.date_saisie.desc())
    
    conditions = []
    if ue_id:
        conditions.append(Note.ue_id == ue_id)
    if inscription_id:
        conditions.append(Note.inscription_id == inscription_id)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    result = await db.execute(query)
    return list(result.scalars().all())


# ==================== DIPLÔMES ====================

async def verify_diplome_service(db: AsyncSession, qr_token: str) -> Optional[dict]:
    """Vérifier l'authenticité d'un diplôme"""
    # TODO: Implémenter quand le modèle Diplome sera créé
    return {"valide": False, "message": "Fonctionnalité non implémentée"}
