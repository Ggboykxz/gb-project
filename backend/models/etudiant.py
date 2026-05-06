"""Modèles Étudiant et Inscription - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum as SQLEnum, JSON, Integer
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database import Base
import uuid

class StatutEtudiant(enum.Enum):
    ACTIF = "ACTIF"
    SUSPENDU = "SUSPENDU"
    EXCLU = "EXCLU"
    DIPLOME = "DIPLOME"
    ABANDON = "ABANDON"

class StatutInscription(enum.Enum):
    SOUMIS = "SOUMIS"
    VALIDE_SCOL = "VALIDE_SCOL"
    VALIDE_DOYEN = "VALIDE_DOYEN"
    CONFIRME = "CONFIRME"
    REJETE = "REJETE"

class Etudiant(Base):
    __tablename__ = "etudiants"
    
    id = Column(String(36), primary_key=True)
    nip_gabon = Column(String(20), unique=True, nullable=False, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(DateTime, nullable=False)
    genre = Column(String(10), nullable=False)
    nationalite = Column(String(50), default="Gabonaise")
    telephone = Column(String(20))
    email = Column(String(255), unique=True)
    photo_url = Column(String(500), nullable=True)
    statut = Column(SQLEnum(StatutEtudiant), default=StatutEtudiant.ACTIF)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Inscription(Base):
    __tablename__ = "inscriptions"
    
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    annee_academique = Column(String(20), nullable=False, index=True)
    niveau = Column(String(10), nullable=False)
    type_inscription = Column(String(20), default="nouveau")
    statut_workflow = Column(SQLEnum(StatutInscription), default=StatutInscription.SOUMIS)
    date_soumission = Column(DateTime, default=datetime.utcnow)
    documents_json = Column(JSON, default=list)
    frais_payes = Column(Boolean, default=False)
    montant_paye = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())