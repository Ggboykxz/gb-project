from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class TypeEval(str, enum.Enum):
    CC = "CC"  # Contrôle Continu
    TP = "TP"  # Travaux Pratiques
    EXAMEN = "EXAMEN"
    RATTRAPAGE = "RATTRAPAGE"

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    inscription_id = Column(Integer, ForeignKey("inscriptions.id"), nullable=False, index=True)
    ue_id = Column(Integer, ForeignKey("ues.id"), nullable=False, index=True)
    type_eval = Column(SQLEnum(TypeEval), nullable=False)
    note = Column(Float, nullable=True)  # Nullable pour absence
    coefficient = Column(Float, default=1.0)
    absence_justifiee = Column(Boolean, default=False)
    date_saisie = Column(DateTime(timezone=True), server_default=func.now())
    saisi_par = Column(Integer, ForeignKey("users.id"), nullable=False)
    validee = Column(Boolean, default=False)
    commentaires = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inscription = relationship("Inscription", back_populates="notes")
    ue = relationship("UE", back_populates="notes")
    saisi_par_user = relationship("User", foreign_keys=[saisi_par])
