"""Modèles pour le module Pédagogie et Ressources - Phase 3"""
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from database import Base


class TypeSupport(enum.Enum):
    CM = "CM"
    TD = "TD"
    TP = "TP"
    PROJET = "Projet"
    AUTRE = "Autre"


class StatutDocument(enum.Enum):
    BROUILLON = "brouillon"
    PUBLIE = "publié"
    ARCHIVE = "archivé"


class CoursSupport(Base):
    """Table 3.1 - Supports de cours"""
    __tablename__ = "cours_supports"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ue_id: Mapped[int] = mapped_column(Integer, ForeignKey("ues.id"), nullable=False)
    enseignant_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    type_support: Mapped[TypeSupport] = mapped_column(SQLEnum(TypeSupport), nullable=False)
    fichier_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    contenu_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    ordre_sequence: Mapped[int] = mapped_column(Integer, default=0)
    statut: Mapped[StatutDocument] = mapped_column(SQLEnum(StatutDocument), default=StatutDocument.BROUILLON)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_maj: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    ue = relationship("UE", back_populates="supports")
    enseignant = relationship("User", back_populates="supports_cours")


class QRCodePresence(Base):
    """Table 3.1 - QR Codes de présence dynamiques"""
    __tablename__ = "qr_presence"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cours_id: Mapped[int] = mapped_column(Integer, ForeignKey("cours.id"), nullable=False)
    token: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    date_generation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_expiration: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    est_valide: Mapped[bool] = mapped_column(Boolean, default=True)
    nb_scans: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relation
    cours = relationship("Cours", back_populates="qr_codes")


class Ouvrage(Base):
    """Table 3.2 - Catalogue bibliothèque"""
    __tablename__ = "ouvrages"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    auteurs_json: Mapped[str] = mapped_column(JSON, default=list)  # Liste des auteurs
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True, index=True)
    annee_publication: Mapped[int | None] = mapped_column(Integer, nullable=True)
    editeur: Mapped[str | None] = mapped_column(String(100), nullable=True)
    domaine: Mapped[str | None] = mapped_column(String(100), nullable=True)
    localisation_physique: Mapped[str | None] = mapped_column(String(50), nullable=True)
    exemplaires_total: Mapped[int] = mapped_column(Integer, default=1)
    exemplaires_dispo: Mapped[int] = mapped_column(Integer, default=1)
    fichier_pdf_local: Mapped[str | None] = mapped_column(String(500), nullable=True)
    couverture_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
    mots_cles_json: Mapped[str | None] = mapped_column(JSON, default=list)
    date_ajout: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relations
    prets = relationship("Pret", back_populates="ouvrage")


class Pret(Base):
    """Table 3.2 - Prêts d'ouvrages"""
    __tablename__ = "prets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    etudiant_id: Mapped[int] = mapped_column(Integer, ForeignKey("etudiants.id"), nullable=False)
    ouvrage_id: Mapped[int] = mapped_column(Integer, ForeignKey("ouvrages.id"), nullable=False)
    date_pret: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_retour_prevue: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_retour_effective: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    statut: Mapped[str] = mapped_column(String(20), default="en_cours")  # en_cours, retourne, retarde, perdu
    penalite_fcfa: Mapped[int] = mapped_column(Integer, default=0)
    renouvellements: Mapped[int] = mapped_column(Integer, default=0)
    
    # Relations
    ouvrage = relationship("Ouvrage", back_populates="prets")
    etudiant = relationship("Etudiant", back_populates="prets")


class MemoireThese(Base):
    """Table 3.3 - Dépôt de mémoires et thèses"""
    __tablename__ = "memoires_theses"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    etudiant_id: Mapped[int] = mapped_column(Integer, ForeignKey("etudiants.id"), nullable=False)
    directeur_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    titre: Mapped[str] = mapped_column(String(400), nullable=False)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
    mots_cles_json: Mapped[str] = mapped_column(JSON, default=list)
    annee: Mapped[int] = mapped_column(Integer, nullable=False)
    filiere_id: Mapped[int] = mapped_column(Integer, ForeignKey("filieres.id"), nullable=False)
    type_document: Mapped[str] = mapped_column(String(20))  # mémoire, thèse, rapport
    version_courante: Mapped[int] = mapped_column(Integer, default=1)
    statut_validation: Mapped[str] = mapped_column(String(30), default="depot")  # depot, revue, corrections, valide, archive
    fichier_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    embargo_jusqu_au: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_depot: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relations
    etudiant = relationship("Etudiant", back_populates="memoires")
    directeur = relationship("User", back_populates="memoires_diriges")
    filiere = relationship("Filiere", back_populates="memoires")
    versions = relationship("VersionDoc", back_populates="memoire", cascade="all, delete-orphan")


class VersionDoc(Base):
    """Table 3.3 - Versions de documents"""
    __tablename__ = "versions_docs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    memoire_id: Mapped[int] = mapped_column(Integer, ForeignKey("memoires_theses.id"), nullable=False)
    numero_version: Mapped[int] = mapped_column(Integer, nullable=False)
    fichier_url: Mapped[str] = mapped_column(String(500), nullable=False)
    commentaires_directeur: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_depot: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    statut: Mapped[str] = mapped_column(String(30), default="soumis")
    
    # Relation
    memoire = relationship("MemoireThese", back_populates="versions")


class SessionVirtuelle(Base):
    """Table 3.4 - Sessions de classe virtuelle"""
    __tablename__ = "sessions_virtuelles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cours_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("cours.id"), nullable=True)
    lien_jitsi: Mapped[str] = mapped_column(String(300), nullable=False)
    date_heure: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duree_minutes: Mapped[int] = mapped_column(Integer, default=60)
    enregistrement_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    participants_json: Mapped[str | None] = mapped_column(JSON, default=list)
    chat_messages_json: Mapped[str | None] = mapped_column(JSON, default=list)
    statut: Mapped[str] = mapped_column(String(20), default="planifie")  # planifie, en_cours, termine
    
    # Relation
    cours = relationship("Cours", back_populates="sessions_virtuelles")


class Sujet(Base):
    """Table 3.5 - Banque de sujets d'examen"""
    __tablename__ = "sujets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ue_id: Mapped[int] = mapped_column(Integer, ForeignKey("ues.id"), nullable=False)
    enseignant_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    type_sujet: Mapped[str] = mapped_column(String(20))  # qcm, redige, pratique, oral
    difficulte: Mapped[int] = mapped_column(Integer, default=1)  # 1-5
    annee_utilisation: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fichier_chiffre_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    tags_json: Mapped[str | None] = mapped_column(JSON, default=list)
    nb_utilisations: Mapped[int] = mapped_column(Integer, default=0)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    est_archive: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Relations
    ue = relationship("UE", back_populates="sujets")
    enseignant = relationship("User", back_populates="sujets_proposes")


class EpreuveExamen(Base):
    """Table 3.5 - Épreuves d'examen"""
    __tablename__ = "epreuves_examens"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ue_id: Mapped[int] = mapped_column(Integer, ForeignKey("ues.id"), nullable=False)
    session: Mapped[str] = mapped_column(String(20), default="normale")  # normale, rattrapage
    date_examen: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duree_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    salle_ids_json: Mapped[str] = mapped_column(JSON, default=list)
    sujets_selectionnes_json: Mapped[str] = mapped_column(JSON, default=list)  # IDs des sujets
    statut: Mapped[str] = mapped_column(String(30), default="planifie")  # planifie, imprime, deroule, corrige
    responsable_surveillance: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    date_impression: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relations
    ue = relationship("UE", back_populates="epreuves")
    responsable = relationship("User", back_populates="epreuves_surveillees")
