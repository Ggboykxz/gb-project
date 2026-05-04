from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, Enum as SQLEnum, JSON, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class NiveauEtude(str, enum.Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    M1 = "M1"
    M2 = "M2"
    D1 = "D1"
    D2 = "D2"
    D3 = "D3"

class TypeInscription(str, enum.Enum):
    NOUVEAU = "NOUVEAU"
    REINSCRIPTION = "REINSCRIPTION"

class StatutWorkflow(str, enum.Enum):
    SOUMIS = "SOUMIS"
    VALIDE_SCOL = "VALIDE_SCOL"
    VALIDE_DOYEN = "VALIDE_DOYEN"
    CONFIRME = "CONFIRME"
    REJETE = "REJETE"

class Inscription(Base):
    __tablename__ = "inscriptions"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False, index=True)
    annee_academique = Column(String(20), nullable=False, index=True)  # e.g., "2024-2025"
    filiere_id = Column(Integer, ForeignKey("filieres.id"), nullable=False)
    niveau = Column(SQLEnum(NiveauEtude), nullable=False)
    type_inscription = Column(SQLEnum(TypeInscription), default=TypeInscription.NOUVEAU)
    statut_workflow = Column(SQLEnum(StatutWorkflow), default=StatutWorkflow.SOUMIS)
    date_soumission = Column(DateTime(timezone=True), server_default=func.now())
    documents_json = Column(JSON, default=list)
    frais_payes = Column(Float, default=0.0)
    frais_total = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    etudiant = relationship("Etudiant", back_populates="inscriptions")
    filiere = relationship("Filiere", back_populates="inscriptions")
    notes = relationship("Note", back_populates="inscription")
    paiements = relationship("Paiement", back_populates="inscription")
