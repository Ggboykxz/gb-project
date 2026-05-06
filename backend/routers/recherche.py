from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import recherche as recherche_model

router = APIRouter()

@router.get("/projets")
def get_projets(db: Session = Depends(get_db)):
    return db.query(recherche_model.ProjetRecherche).all()

@router.get("/projets/{projet_id}")
def get_projet(projet_id: int, db: Session = Depends(get_db)):
    return db.query(recherche_model.ProjetRecherche).filter(recherche_model.ProjetRecherche.id == projet_id).first()

@router.post("/projets")
def create_projet(data: dict, db: Session = Depends(get_db)):
    p = recherche_model.ProjetRecherche(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/publications")
def get_publications(auteur_id: int = None, db: Session = Depends(get_db)):
    query = db.query(recherche_model.Publication)
    if auteur_id:
        query = query.filter(recherche_model.Publication.auteur_id == auteur_id)
    return query.all()

@router.post("/publications")
def create_publication(data: dict, db: Session = Depends(get_db)):
    p = recherche_model.Publication(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/laboratoires")
def get_laboratoires(db: Session = Depends(get_db)):
    return db.query(recherche_model.Laboratoire).all()

@router.post("/laboratoires")
def create_laboratoire(data: dict, db: Session = Depends(get_db)):
    l = recherche_model.Laboratoire(**data)
    db.add(l)
    db.commit()
    db.refresh(l)
    return l

@router.get("/partenariats")
def get_partenariats(db: Session = Depends(get_db)):
    return db.query(recherche_model.Partenariat).all()

@router.post("/partenariats")
def create_partenariat(data: dict, db: Session = Depends(get_db)):
    p = recherche_model.Partenariat(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/equipements")
def get_equipements(laboratoire_id: int = None, db: Session = Depends(get_db)):
    query = db.query(recherche_model.Equipement)
    if laboratoire_id:
        query = query.filter(recherche_model.Equipement.laboratoire_id == laboratoire_id)
    return query.all()

@router.post("/equipements")
def create_equipement(data: dict, db: Session = Depends(get_db)):
    e = recherche_model.Equipement(**data)
    db.add(e)
    db.commit()
    db.refresh(e)
    return e