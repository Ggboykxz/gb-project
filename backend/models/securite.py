"""Modèles pour le module Sécurité et Audit - Phase 7"""
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON, BigInteger
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from database import Base


class TypeAction(enum.Enum):
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    EXPORT = "EXPORT"
    VALIDATE = "VALIDATE"
    REJECT = "REJECT"
    SYNC = "SYNC"


class AuditLog(Base):
    """Table 7.x - Journal d'audit complet"""
    __tablename__ = "audit_logs"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    action: Mapped[TypeAction] = mapped_column(SQLEnum(TypeAction), nullable=False, index=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # Etudiant, Note, Paiement, etc.
    resource_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    old_value_json: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON compressé si volumineux
    new_value_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)  # IPv4 ou IPv6
    device_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    est_anomalie: Mapped[bool] = mapped_column(Boolean, default=False)
    note_anomalie: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Relation
    user = relationship("User", back_populates="audit_logs")
    
    def __repr__(self):
        return f"<AuditLog {self.user_id} {self.action} {self.resource_type}:{self.resource_id}>"


class SessionUtilisateur(Base):
    """Table 7.x - Gestion des sessions utilisateurs"""
    __tablename__ = "sessions_utilisateurs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    token_refresh: Mapped[str] = mapped_column(String(500), unique=True, nullable=False, index=True)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False)
    device_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    date_connexion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_expiration: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_derniere_activite: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    est_active: Mapped[bool] = mapped_column(Boolean, default=True)
    est_revoquee: Mapped[bool] = mapped_column(Boolean, default=False)
    date_revocation: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    motif_revocation: Mapped[str | None] = mapped_column(String(200), nullable=True)
    
    # Relation
    user = relationship("User", back_populates="sessions")


class CleSignature(Base):
    """Table 7.x - Clés de signature électronique"""
    __tablename__ = "cles_signature"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    cle_publique_pem: Mapped[str] = mapped_column(Text, nullable=False)
    cle_privee_chiffree: Mapped[str | None] = mapped_column(Text, nullable=True)  # Stockée chiffrée dans OS keychain
    algorithme: Mapped[str] = mapped_column(String(20), default="RSA-2048")
    date_generation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_expiration: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    est_active: Mapped[bool] = mapped_column(Boolean, default=True)
    empreinte: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA-256 fingerprint
    
    # Relation
    user = relationship("User", back_populates="cle_signature")


class SignatureDocument(Base):
    """Table 7.x - Signatures de documents officiels"""
    __tablename__ = "signatures_documents"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    document_type: Mapped[str] = mapped_column(String(50), nullable=False)  # PV_JURY, DIPLOME, ATTESTATION
    document_id: Mapped[int] = mapped_column(Integer, nullable=False)  # ID du document dans sa table
    signataire_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    signature_base64: Mapped[str] = mapped_column(Text, nullable=False)  # Signature RSA
    hash_document: Mapped[str] = mapped_column(String(64), nullable=False)  # SHA-256 du document
    date_signature: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    est_valide: Mapped[bool] = mapped_column(Boolean, default=True)
    date_verification: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(JSON, default=dict)
    
    # Relation
    signataire = relationship("User", back_populates="signatures_effectuees")


class TentativeConnexion(Base):
    """Table 7.x - Historique des tentatives de connexion"""
    __tablename__ = "tentatives_connexion"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    device_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    est_succes: Mapped[bool] = mapped_column(Boolean, default=False)
    echec_raison: Mapped[str | None] = mapped_column(String(50), nullable=True)  # mauvais_mdp, compte_verrouille, 2fa_invalide
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)


class VerrouillageCompte(Base):
    """Table 7.x - Comptes verrouillés"""
    __tablename__ = "verrouillages_comptes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    nb_echecs: Mapped[int] = mapped_column(Integer, default=0)
    date_verrouillage: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_deblocage: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    est_verrouille: Mapped[bool] = mapped_column(Boolean, default=True)
    debloque_par: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relations
    user = relationship("User", back_populates="verrouillage", foreign_keys=[user_id])
    admin_deblocage = relationship("User", back_populates="deblocages_effectues", foreign_keys=[debloque_par])


class PermissionRole(Base):
    """Table 7.x - Matrice des permissions par rôle"""
    __tablename__ = "permissions_roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    resource: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(20), nullable=False)  # create, read, update, delete, export, validate
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    conditions_json: Mapped[str | None] = mapped_column(JSON, nullable=True)  # Conditions métier optionnelles
    date_maj: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        # Unique constraint sur role + resource + action
        {'sqlite_autoincrement': True}
    )


class ConsentementRGPD(Base):
    """Table 7.x - Consentements RGPD / Loi gabonaise"""
    __tablename__ = "consentements_rgpd"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    etudiant_id: Mapped[int] = mapped_column(Integer, ForeignKey("etudiants.id"), nullable=False)
    type_consentement: Mapped[str] = mapped_column(String(50), nullable=False)  # donnees_personnelles, photo, stats, alumni
    est_accepte: Mapped[bool] = mapped_column(Boolean, default=False)
    date_consentement: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_expiration: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)
    peut_retirer: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Relation
    etudiant = relationship("Etudiant", back_populates="consentements")


class ExportDonnees(Base):
    """Table 7.x - Demandes d'export de données personnelles"""
    __tablename__ = "exports_donnees"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    format_export: Mapped[str] = mapped_column(String(10), default="JSON")  # JSON, CSV, PDF
    statut: Mapped[str] = mapped_column(String(20), default="demande")  # demande, en_cours, termine, echec
    fichier_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    date_demande: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_generation: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_expiration_fichier: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relation
    user = relationship("User", back_populates="exports_donnees")
