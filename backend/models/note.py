from sqlalchemy import Column, String, Float, ForeignKey, Boolean, DateTime, Integer
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Note(Base):
    __tablename__ = "notes"
    id = Column(String(36), primary_key=True)
    inscription_id = Column(String(36), ForeignKey("inscriptions.id"), nullable=False)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    type_eval = Column(String(20), default="cc")
    note = Column(Float)
    absence_justifiee = Column(Boolean, default=False)
    date_saisie = Column(DateTime, default=datetime.utcnow)
    saisi_par = Column(String(36), ForeignKey("users.id"))
    validee = Column(Boolean, default=False)
    inscription = relationship("Inscription", back_populates="notes")
    ue = relationship("UE", back_populates="notes")
    saisi_par_user = relationship("User", back_populates="notes_saisies")

class Deliberation(Base):
    __tablename__ = "deliberations"
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"))
    annee_academique = Column(String(20))
    semestre = Column(Integer)
    date = Column(DateTime)
    jury_json = Column(String)
    statut = Column(String, default="brouillon")
    pv_url = Column(String)
