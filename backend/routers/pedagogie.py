from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import pedagogie, filiere, note as note_model
from schemas import administration as schemas

router = APIRouter()

@router.get("/cours")
def get_cours(db: Session = Depends(get_db)):
    return db.query(pedagogie.Cours).all()

@router.get("/cours/{cours_id}")
def get_cours_detail(cours_id: int, db: Session = Depends(get_db)):
    return db.query(pedagogie.Cours).filter(pedagogie.Cours.id == cours_id).first()

@router.post("/cours")
def create_cours(data: schemas.CoursCreate, db: Session = Depends(get_db)):
    c = pedagogie.Cours(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/cours/{cours_id}")
def update_cours(cours_id: int, data: schemas.CoursUpdate, db: Session = Depends(get_db)):
    c = db.query(pedagogie.Cours).filter(pedagogie.Cours.id == cours_id).first()
    if not c:
        return {"error": "Cours non trouvé"}
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(c, k, v)
    db.commit()
    return c

@router.get("/presences")
def get_presences(cours_id: int = None, db: Session = Depends(get_db)):
    if cours_id:
        return db.query(pedagogie.Presence).filter(pedagogie.Presence.cours_id == cours_id).all()
    return db.query(pedagogie.Presence).all()

@router.post("/presences")
def create_presence(data: schemas.PresenceCreate, db: Session = Depends(get_db)):
    p = pedagogie.Presence(**data.model_dump())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/notes")
def get_notes(etudiant_id: int = None, cours_id: int = None, db: Session = Depends(get_db)):
    query = db.query(note_model.Note)
    if etudiant_id:
        query = query.filter(note_model.Note.etudiant_id == etudiant_id)
    if cours_id:
        query = query.filter(note_model.Note.cours_id == cours_id)
    return query.all()

@router.post("/notes")
def create_note(data: schemas.NoteCreate, db: Session = Depends(get_db)):
    n = note_model.Note(**data.model_dump())
    db.add(n)
    db.commit()
    db.refresh(n)
    return n

@router.get("/maquettes")
def get_maquettes(filiere_id: int = None, db: Session = Depends(get_db)):
    query = db.query(filiere.Maquette)
    if filiere_id:
        query = query.filter(filiere.Maquette.filiere_id == filiere_id)
    return query.all()

@router.post("/maquettes")
def create_maquette(data: schemas.MaquetteCreate, db: Session = Depends(get_db)):
    m = filiere.Maquette(**data.model_dump())
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/edt")
def get_edt(cours_id: int = None, db: Session = Depends(get_db)):
    query = db.query(pedagogie.EmploisDuTemps)
    if cours_id:
        query = query.filter(pedagogie.EmploisDuTemps.cours_id == cours_id)
    return query.all()

@router.post("/edt")
def create_edt(data: dict, db: Session = Depends(get_db)):
    edt = pedagogie.EmploisDuTemps(**data)
    db.add(edt)
    db.commit()
    db.refresh(edt)
    return edt