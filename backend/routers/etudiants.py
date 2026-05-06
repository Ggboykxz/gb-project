from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import etudiant
from schemas.etudiant import EtudiantCreate, EtudiantUpdate, InscriptionCreate

router = APIRouter()

@router.get("/")
def get_etudiants(db: Session = Depends(get_db)):
    return db.query(etudiant.Etudiant).all()

@router.get("/{etudiant_id}")
def get_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    return db.query(etudiant.Etudiant).filter(etudiant.Etudiant.id == etudiant_id).first()

@router.post("/")
def create_etudiant(data: EtudiantCreate, db: Session = Depends(get_db)):
    e = etudiant.Etudiant(**data.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return e

@router.put("/{etudiant_id}")
def update_etudiant(etudiant_id: int, data: EtudiantUpdate, db: Session = Depends(get_db)):
    e = db.query(etudiant.Etudiant).filter(etudiant.Etudiant.id == etudiant_id).first()
    if not e:
        return {"error": "Étudiant non trouvé"}
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(e, k, v)
    db.commit()
    return e

@router.delete("/{etudiant_id}")
def delete_etudiant(etudiant_id: int, db: Session = Depends(get_db)):
    e = db.query(etudiant.Etudiant).filter(etudiant.Etudiant.id == etudiant_id).first()
    if not e:
        return {"error": "Étudiant non trouvé"}
    db.delete(e)
    db.commit()
    return {"message": "Étudiant supprimé"}

@router.get("/{etudiant_id}/documents")
def get_documents(etudiant_id: int, db: Session = Depends(get_db)):
    e = db.query(etudiant.Etudiant).filter(etudiant.Etudiant.id == etudiant_id).first()
    if not e:
        return {"error": "Étudiant non trouvé"}
    return e.documents

@router.post("/{etudiant_id}/inscription")
def create_inscription(etudiant_id: int, data: InscriptionCreate, db: Session = Depends(get_db)):
    from models import filiere
    f = db.query(filiere.Filiere).filter(filiere.Filiere.id == data.filiere_id).first()
    if not f:
        return {"error": "Filière non trouvée"}
    ins = etudiant.Inscription(
        etudiant_id=etudiant_id,
        filiere_id=data.filiere_id,
        anneeAcademique=data.anneeAcademique,
        niveau=data.niveau,
        statut="actif"
    )
    db.add(ins)
    db.commit()
    db.refresh(ins)
    return ins