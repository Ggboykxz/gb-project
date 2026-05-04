"""Modèles Filière, UE, Maquette, Salle et Créneaux"""
from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, JSON, Boolean
from sqlalchemy.orm import relationship
import enum
from ..database import Base

class NiveauLMD(enum.Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    M1 = "M1"
    M2 = "M2"
    D = "D"

class TypeUE(enum.Enum):
    OBLIGATOIRE = "OBLIGATOIRE"
    OPTIONNEL = "OPTIONNEL"

class StatutMaquette(enum.Enum):
    BROUILLON = "BROUILLON"
    VALIDE = "VALIDE"
    ARCHIVE = "ARCHIVE"

class TypeSalle(enum.Enum):
    AMPHI = "AMPHI"
    TD = "TD"
    TP = "TP"
    INFO = "INFO"

class Filiere(Base):
    __tablename__ = "filieres"
    
    id = Column(String(36), primary_key=True)
    code = Column(String(10), unique=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    domaine = Column(String(100))
    niveau_principal = Column(SQLEnum(NiveauLMD))
    duree_annees = Column(Integer, default=3)
    responsable_id = Column(String(36), ForeignKey("users.id"))
    created_at = Column(String(50))
    
    inscriptions = relationship("Inscription", back_populates="filiere")
    ues = relationship("UE", back_populates="filiere")
    maquettes = relationship("Maquette", back_populates="filiere")

class UE(Base):
    __tablename__ = "ues"
    
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    code_ue = Column(String(20), nullable=False)
    libelle = Column(String(200), nullable=False)
    credits_ects = Column(Integer, nullable=False, default=6)
    semestre = Column(Integer, nullable=False)
    heures_cm = Column(Integer, default=0)
    heures_td = Column(Integer, default=0)
    heures_tp = Column(Integer, default=0)
    coefficient = Column(Integer, default=1)
    ue_type = Column(SQLEnum(TypeUE), default=TypeUE.OBLIGATOIRE)
    
    filiere = relationship("Filiere", back_populates="ues")
    cours = relationship("Cours", back_populates="ue")
    notes = relationship("Note", back_populates="ue")

class Maquette(Base):
    __tablename__ = "maquettes"
    
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    annee_academique = Column(String(20), nullable=False)
    ues_json = Column(JSON, default=list)
    statut = Column(SQLEnum(StatutMaquette), default=StatutMaquette.BROUILLON)
    
    filiere = relationship("Filiere", back_populates="maquettes")

class Salle(Base):
    __tablename__ = "salles"
    
    id = Column(String(36), primary_key=True)
    nom = Column(String(50), nullable=False)
    capacite = Column(Integer, nullable=False)
    type_salle = Column(SQLEnum(TypeSalle), default=TypeSalle.TD)
    equipements_json = Column(JSON, default=list)
    batiment = Column(String(50))
    disponible = Column(Boolean, default=True)
    
    creneaux = relationship("Creneau", back_populates="salle")
    cours = relationship("Cours", back_populates="salle")

class Creneau(Base):
    __tablename__ = "creneaux"
    
    id = Column(String(36), primary_key=True)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    enseignant_id = Column(String(36), ForeignKey("users.id"))
    salle_id = Column(String(36), ForeignKey("salles.id"))
    groupe = Column(String(20))
    jour = Column(String(20))
    heure_debut = Column(String(10))
    heure_fin = Column(String(10))
    semaine_type = Column(String(10), default="toutes")
    couleur_hex = Column(String(7), default="#3498db")
    
    ue = relationship("UE", back_populates="creneaux")
    salle = relationship("Salle", back_populates="creneaux")
