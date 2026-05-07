from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db

router = APIRouter(tags=["Étudiants"])

@router.get("/")
async def get_etudiants(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    from models.etudiant import Etudiant
    result = await db.execute(select(Etudiant).offset(skip).limit(limit))
    etudiants = result.scalars().all()
    return etudiants

@router.get("/{etudiant_id}")
async def get_etudiant(
    etudiant_id: str,
    db: AsyncSession = Depends(get_db)
):
    from models.etudiant import Etudiant
    result = await db.execute(select(Etudiant).where(Etudiant.id == etudiant_id))
    etudiant = result.scalar_one_or_none()
    if not etudiant:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    return etudiant

@router.post("/")
async def create_etudiant(
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    from models.etudiant import Etudiant
    e = Etudiant(**data)
    db.add(e)
    await db.commit()
    await db.refresh(e)
    return e

@router.put("/{etudiant_id}")
async def update_etudiant(
    etudiant_id: str,
    data: dict,
    db: AsyncSession = Depends(get_db)
):
    from models.etudiant import Etudiant
    result = await db.execute(select(Etudiant).where(Etudiant.id == etudiant_id))
    e = result.scalar_one_or_none()
    if not e:
        raise HTTPException(status_code=404, detail="Étudiant non trouvé")
    for k, v in data.items():
        if hasattr(e, k):
            setattr(e, k, v)
    await db.commit()
    return e

@router.get("/{etudiant_id}/inscriptions")
async def get_etudiant_inscriptions(
    etudiant_id: str,
    db: AsyncSession = Depends(get_db)
):
    from models.etudiant import Inscription
    result = await db.execute(
        select(Inscription).where(Inscription.etudiant_id == etudiant_id)
    )
    return result.scalars().all()