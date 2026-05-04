"""
Modèles pour la vie étudiante et services
"""
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, Boolean, Float, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class TypeExperience(str, enum.Enum):
    STAGE = "stage"
    PROJET = "projet"
    CERTIFICATION = "certification"
    BENEVOLAT = "benevolat"


class VisibilitePortfolio(str, enum.Enum):
    PRIVE = "prive"
    ETABLISSEMENT = "etablissement"
    PUBLIC = "public"


class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    competences_json = Column(JSON, default=list)
    langues_json = Column(JSON, default=list)
    visibilite = Column(SQLEnum(VisibilitePortfolio), default=VisibilitePortfolio.PRIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    etudiant = relationship("Etudiant", back_populates="portfolio")
    experiences = relationship("ExperiencePortfolio", back_populates="portfolio", cascade="all, delete-orphan")


class ExperiencePortfolio(Base):
    __tablename__ = "experiences_portfolio"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    type_exp = Column(SQLEnum(TypeExperience), nullable=False)
    titre = Column(String(200), nullable=False)
    organisation = Column(String(200), nullable=True)
    date_debut = Column(Date, nullable=True)
    date_fin = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    fichier_url = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    portfolio = relationship("Portfolio", back_populates="experiences")


class TypeBourse(Base):
    __tablename__ = "types_bourse"

    id = Column(Integer, primary_key=True, index=True)
    libelle = Column(String(100), nullable=False, unique=True)
    montant_mensuel = Column(Integer, nullable=False)  # En FCFA
    criteres_json = Column(JSON, default=dict)
    quota_annuel = Column(Integer, nullable=True)
    financeur = Column(String(200), nullable=True)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    dossiers = relationship("DossierBourse", back_populates="type_bourse")


class StatutDossierBourse(str, enum.Enum):
    BROUILLON = "brouillon"
    SOUMIS = "soumis"
    EN_ETUDE = "en_etude"
    ACCEPTE = "accepte"
    REFUSE = "refuse"
    EN_ATTENTE_DOC = "en_attente_doc"


class DossierBourse(Base):
    __tablename__ = "dossiers_bourse"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    type_bourse_id = Column(Integer, ForeignKey("types_bourse.id"), nullable=False)
    annee_academique = Column(String(9), nullable=False)  # ex: "2024-2025"
    statut = Column(SQLEnum(StatutDossierBourse), default=StatutDossierBourse.BROUILLON)
    score_social = Column(Float, nullable=True)
    documents_json = Column(JSON, default=list)
    decision = Column(String(500), nullable=True)
    date_decision = Column(DateTime(timezone=True), nullable=True)
    commentaire = Column(Text, nullable=True)
    soumis_le = Column(DateTime(timezone=True), nullable=True)
    traite_par = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    type_bourse = relationship("TypeBourse", back_populates="dossiers")
    etudiant = relationship("Etudiant", back_populates="dossiers_bourse")


class TypeAlerteEtudiant(str, enum.Enum):
    DECROCHAGE = "decrochage"
    ECHEC = "echec"
    ABSENCE_REPETEE = "absence_repetee"
    RETARD_PAIEMENT = "retard_paiement"
    AUTRE = "autre"


class StatutSuivi(str, enum.Enum):
    OUVERT = "ouvert"
    EN_COURS = "en_cours"
    RESOLU = "resolu"
    CLOS = "clos"


class SuiviEtudiant(Base):
    __tablename__ = "suivis_etudiants"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    conseiller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type_alerte = Column(SQLEnum(TypeAlerteEtudiant), nullable=False)
    statut = Column(SQLEnum(StatutSuivi), default=StatutSuivi.OUVERT)
    notes_suivi_json = Column(JSON, default=list)
    objectifs_json = Column(JSON, default=list)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_cloture = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    etudiant = relationship("Etudiant", back_populates="suivis")
    conseiller = relationship("User", foreign_keys=[conseiller_id])


class TypeOffre(str, enum.Enum):
    STAGE = "stage"
    CDI = "cdi"
    CDD = "cdd"
    ALTERNANCE = "alternance"


class StatutOffre(str, enum.Enum):
    ACTIVE = "active"
    POURVUE = "pourvue"
    EXPIREE = "expiree"
    SUSPENDUE = "suspendue"


class OffreStageEmploi(Base):
    __tablename__ = "offres_stage_emploi"

    id = Column(Integer, primary_key=True, index=True)
    entreprise_id = Column(Integer, ForeignKey("entreprises_partenaires.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    type_offre = Column(SQLEnum(TypeOffre), nullable=False)
    domaine = Column(String(100), nullable=True)
    localisation_gabon = Column(String(100), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_limite = Column(Date, nullable=True)
    statut = Column(SQLEnum(StatutOffre), default=StatutOffre.ACTIVE)
    contact_json = Column(JSON, default=dict)
    competences_requises_json = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    entreprise = relationship("EntreprisePartenaire", back_populates="offres")
    candidatures = relationship("Candidature", back_populates="offre", cascade="all, delete-orphan")


class EntreprisePartenaire(Base):
    __tablename__ = "entreprises_partenaires"

    id = Column(Integer, primary_key=True, index=True)
    raison_sociale = Column(String(200), nullable=False)
    secteur = Column(String(100), nullable=True)
    localisation = Column(String(100), nullable=True)
    contact_rh = Column(String(200), nullable=True)
    email = Column(String(100), nullable=True)
    telephone = Column(String(20), nullable=True)
    conventions_json = Column(JSON, default=list)
    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    offres = relationship("OffreStageEmploi", back_populates="entreprise")


class StatutCandidature(str, enum.Enum):
    SOUMISE = "soumise"
    EN_ETUDE = "en_etude"
    ACCEPTEE = "acceptee"
    REFUSEE = "refusee"
    RETIREE = "retiree"


class Candidature(Base):
    __tablename__ = "candidatures"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False)
    offre_id = Column(Integer, ForeignKey("offres_stage_emploi.id"), nullable=False)
    date_candidature = Column(DateTime(timezone=True), server_default=func.now())
    statut = Column(SQLEnum(StatutCandidature), default=StatutCandidature.SOUMISE)
    cv_url = Column(String(500), nullable=True)
    lettre_url = Column(String(500), nullable=True)
    commentaire = Column(Text, nullable=True)
    date_reponse = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    etudiant = relationship("Etudiant", back_populates="candidatures")
    offre = relationship("OffreStageEmploi", back_populates="candidatures")


class Alumni(Base):
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), unique=True, nullable=False)
    promo = Column(String(9), nullable=False)  # ex: "2023-2024"
    poste_actuel = Column(String(200), nullable=True)
    entreprise_actuelle = Column(String(200), nullable=True)
    localisation = Column(String(100), nullable=True)
    linkedin_url = Column(String(300), nullable=True)
    disponible_mentorat = Column(Boolean, default=False)
    domaines_expertise_json = Column(JSON, default=list)
    email_personnel = Column(String(100), nullable=True)
    telephone_personnel = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    etudiant = relationship("Etudiant", back_populates="alumni")
