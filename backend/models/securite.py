"""Modèles Sécurité - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON
from datetime import datetime
from database import Base
import uuid

class SessionUtilisateur(Base):
    __tablename__ = "sessions_utilisateurs"
    id = Column(String(36), primary_key=True)
    utilisateur_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    jeton_refresh = Column(String(500), unique=True)
    date_connexion = Column(DateTime, default=datetime.utcnow)
    date_expiration = Column(DateTime)
    adresse_ip = Column(String(50))
    statut = Column(String(20), default="active")  # active, expiree, revoked
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class TentativeConnexion(Base):
    __tablename__ = "tentatives_connexion"
    id = Column(String(36), primary_key=True)
    email = Column(String(255), nullable=False, index=True)
    succes = Column(Boolean, default=False)
    adresse_ip = Column(String(50))
    date_essai = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50))
    resource_id = Column(String(36))
    old_value_json = Column(JSON)
    new_value_json = Column(JSON)
    ip_address = Column(String(50))
    device_id = Column(String(36))
    timestamp = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())