"""Modèles Filière, UE, Maquette, Salle - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Boolean, Enum as SQLEnum, Float, Date, Time, DateTime
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database import Base
import uuid

class NiveauLMD(enum.Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    M1 = "M1"
    M2 = "M2"
    D = "D"

class TypeUE(enum.Enum):
    OBLIGATOIRE = "obligatoire"
    OPTIONNEL = "optionnel"

class StatutMaquette(enum.Enum):
    BROUILLON = "brouillon"
    VALIDE = "validé"
    ARCHIVE = "archivé"

class TypeSalle(enum.Enum):
    AMPHI = "amphi"
    TD = "td"
    TP = "tp"
    INFO = "info"

class Filiere(Base):
    __tablename__ = "filieres"
    
    id = Column(String(36), primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    domaine = Column(String(100))
    niveau = Column(SQLEnum(NiveauLMD))
    duree_annees = Column(Integer)
    responsable_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class UE(Base):
    __tablename__ = "ues"
    
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    code_ue = Column(String(20), nullable=False)
    libelle = Column(String(200), nullable=False)
    credits_ects = Column(Integer, default=6)
    semestre = Column(Integer)
    heures_cm = Column(Integer, default=0)
    heures_td = Column(Integer, default=0)
    heures_tp = Column(Integer, default=0)
    coefficient = Column(Float, default=1.0)
    ue_type = Column(SQLEnum(TypeUE), default=TypeUE.OBLIGATOIRE)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Maquette(Base):
    __tablename__ = "maquettes"
    
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    annee_academique = Column(String(20), nullable=False)
    ues_json = Column(JSON, default=list)
    statut = Column(SQLEnum(StatutMaquette), default=StatutMaquette.BROUILLON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Salle(Base):
    __tablename__ = "salles"
    
    id = Column(String(36), primary_key=True)
    nom = Column(String(50), nullable=False)
    capacite = Column(Integer, nullable=False)
    type_salle = Column(SQLEnum(TypeSalle), default=TypeSalle.TD)
    equipements_json = Column(JSON, default=list)
    batiment = Column(String(50))
    disponible = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Creneau(Base):
    __tablename__ = "creneaux"
    
    id = Column(String(36), primary_key=True)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    enseignant_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    salle_id = Column(String(36), ForeignKey("salles.id"), nullable=True)
    groupe = Column(String(50))
    jour = Column(String(20))
    heure_debut = Column(Time)
    heure_fin = Column(Time)
    semaine_type = Column(String(10), default="toutes")
    couleur_hex = Column(String(7), default="#3B82F6")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())