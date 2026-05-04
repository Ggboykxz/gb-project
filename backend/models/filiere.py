from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class DomaineEtude(str, enum.Enum):
    SCIENCES = "SCIENCES"
    LETTRES = "LETTRES"
    DROIT = "DROIT"
    ECONOMIE = "ECONOMIE"
    MEDECINE = "MEDECINE"
    INGENIERIE = "INGENIERIE"

class NiveauFiliere(str, enum.Enum):
    LICENCE = "LICENCE"
    MASTER = "MASTER"
    DOCTORAT = "DOCTORAT"

class Filiere(Base):
    __tablename__ = "filieres"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False, index=True)
    libelle = Column(String(200), nullable=False)
    domaine = Column(SQLEnum(DomaineEtude), nullable=False)
    niveau = Column(SQLEnum(NiveauFiliere), nullable=False)
    duree_annees = Column(Integer, default=3)
    responsable_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inscriptions = relationship("Inscription", back_populates="filiere")
    ues = relationship("UE", back_populates="filiere")
    maquettes = relationship("Maquette", back_populates="filiere")

class UE(Base):
    """Unité d'Enseignement"""
    __tablename__ = "ues"

    id = Column(Integer, primary_key=True, index=True)
    filiere_id = Column(Integer, ForeignKey("filieres.id"), nullable=False, index=True)
    code_ue = Column(String(20), nullable=False)
    libelle = Column(String(200), nullable=False)
    credits_ects = Column(Integer, nullable=False)
    semestre = Column(Integer, nullable=False)  # 1-6 for Licence, 1-4 for Master
    heures_cm = Column(Integer, default=0)
    heures_td = Column(Integer, default=0)
    heures_tp = Column(Integer, default=0)
    coefficient = Column(Float, default=1.0)
    ue_type = Column(SQLEnum('obligatoire', 'optionnel', name='ue_type_enum'), default='obligatoire')
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    filiere = relationship("Filiere", back_populates="ues")
    cours = relationship("Cours", back_populates="ue")
    notes = relationship("Note", back_populates="ue")

class Maquette(Base):
    """Maquette pédagogique par année académique"""
    __tablename__ = "maquettes"

    id = Column(Integer, primary_key=True, index=True)
    filiere_id = Column(Integer, ForeignKey("filieres.id"), nullable=False)
    annee_academique = Column(String(20), nullable=False)
    ues_json = Column(JSON, default=list)  # Liste des IDs d'UE
    statut = Column(SQLEnum('brouillon', 'valide', 'archive', name='maquette_statut'), default='brouillon')
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    validated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    filiere = relationship("Filiere", back_populates="maquettes")
