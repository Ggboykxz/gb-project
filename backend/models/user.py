from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN_SCOL = "ADMIN_SCOL"
    ENSEIGNANT = "ENSEIGNANT"
    ETUDIANT = "ETUDIANT"
    FINANCIER = "FINANCIER"
    BIBLIOTHECAIRE = "BIBLIOTHECAIRE"
    CHERCHEUR = "CHERCHEUR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    role = Column(SQLEnum(UserRole), default=UserRole.ETUDIANT)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    totp_secret = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    inscriptions = relationship("Inscription", back_populates="etudiant")
    notes_saisies = relationship("Note", back_populates="saisi_par_user")
    cours_donnes = relationship("Cours", back_populates="enseignant")
