from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Date, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class Genre(str, enum.Enum):
    M = "M"
    F = "F"

class StatutEtudiant(str, enum.Enum):
    INSCRIT = "INSCRIT"
    SUSPENDU = "SUSPENDU"
    EXCLUT = "EXCLUT"
    DIPLome = "DIPLome"
    ABANDON = "ABANDON"

class Etudiant(Base):
    __tablename__ = "etudiants"

    id = Column(Integer, primary_key=True, index=True)
    nip_gabon = Column(String(50), unique=True, index=True, nullable=True)
    nom = Column(String(100), nullable=False, index=True)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date, nullable=False)
    genre = Column(SQLEnum(Genre), nullable=False)
    nationalite = Column(String(50), default="Gabonaise")
    telephone = Column(String(20))
    email = Column(String(255), unique=True, index=True)
    photo_url = Column(Text, nullable=True)
    statut = Column(SQLEnum(StatutEtudiant), default=StatutEtudiant.INSCRIT)
    adresse = Column(Text)
    ville = Column(String(100), default="Libreville")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inscriptions = relationship("Inscription", back_populates="etudiant", cascade="all, delete-orphan")
    portfolio = relationship("Portfolio", back_populates="etudiant", uselist=False)
    presences = relationship("Presence", back_populates="etudiant")
