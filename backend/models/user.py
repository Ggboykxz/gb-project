"""Modèle Utilisateur avec rôles et permissions"""
from sqlalchemy import Column, String, DateTime, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from database import Base

class Role(enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
    ADMIN_SCOL = "ADMIN_SCOL"
    ENSEIGNANT = "ENSEIGNANT"
    ETUDIANT = "ETUDIANT"
    FINANCIER = "FINANCIER"
    BIBLIOTHECAIRE = "BIBLIOTHECAIRE"
    CHERCHEUR = "CHERCHEUR"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLEnum(Role), nullable=False, default=Role.ETUDIANT)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    totp_secret = Column(String(100), nullable=True)
    totp_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, default=dict)
    
    # Relations
    inscriptions = relationship("Inscription", back_populates="etudiant", foreign_keys="Inscription.etudiant_id")
    cours_enseignes = relationship("Cours", back_populates="enseignant")
    notes_saisies = relationship("Note", back_populates="saisi_par")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.email} ({self.role.value})>"
