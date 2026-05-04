"""Modèles pour le module Recherche et Innovation - Phase 4"""
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from database import Base


class TypeProjet(enum.Enum):
    FONDAMENTALE = "fondamentale"
    APPLIQUEE = "appliquée"
    DEVELOPPEMENT = "développement"


class StatutProjet(enum.Enum):
    SOUMIS = "soumis"
    EN_COURS = "en_cours"
    TERMINE = "terminé"
    SUSPENDU = "suspendu"
    ANNULE = "annulé"


class TypeLivrable(enum.Enum):
    RAPPORT = "rapport"
    PUBLICATION = "publication"
    BREVET = "brevet"
    LOGICIEL = "logiciel"
    PROTOTYPE = "prototype"


class StatutLivrable(enum.Enum):
    PREVU = "prévu"
    EN_RETARD = "en_retard"
    LIVRE = "livré"
    VALIDE = "validé"


class ProjetRecherche(Base):
    """Table 4.1 - Projets de recherche"""
    __tablename__ = "projets_recherche"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(300), nullable=False)
    responsable_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    laboratoire_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("laboratoires.id"), nullable=True)
    type_projet: Mapped[TypeProjet] = mapped_column(SQLEnum(TypeProjet), nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    budget_total_fcfa: Mapped[int] = mapped_column(Integer, default=0)
    statut: Mapped[StatutProjet] = mapped_column(SQLEnum(StatutProjet), default=StatutProjet.SOUMIS)
    partenaires_json: Mapped[str] = mapped_column(JSON, default=list)  # [{nom, pays, role}]
    mots_cles_json: Mapped[str] = mapped_column(JSON, default=list)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relations
    responsable = relationship("User", back_populates="projets_diriges")
    laboratoire = relationship("Laboratoire", back_populates="projets")
    livrables = relationship("LivrableRecherche", back_populates="projet", cascade="all, delete-orphan")
    budget = relationship("BudgetRecherche", back_populates="projet", cascade="all, delete-orphan")


class LivrableRecherche(Base):
    """Table 4.1 - Livrables de projets"""
    __tablename__ = "livrables_recherche"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    projet_id: Mapped[int] = mapped_column(Integer, ForeignKey("projets_recherche.id"), nullable=False)
    titre: Mapped[str] = mapped_column(String(200), nullable=False)
    type_livrable: Mapped[TypeLivrable] = mapped_column(SQLEnum(TypeLivrable), nullable=False)
    date_prevue: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_livraison: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fichier_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    statut: Mapped[StatutLivrable] = mapped_column(SQLEnum(StatutLivrable), default=StatutLivrable.PREVU)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relation
    projet = relationship("ProjetRecherche", back_populates="livrables")


class BudgetRecherche(Base):
    """Table 4.1 - Budget de projets"""
    __tablename__ = "budgets_recherche"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    projet_id: Mapped[int] = mapped_column(Integer, ForeignKey("projets_recherche.id"), nullable=False)
    ligne_budgetaire: Mapped[str] = mapped_column(String(100), nullable=False)  # Personnel, Equipement, Mission, etc.
    montant_alloue: Mapped[int] = mapped_column(Integer, nullable=False)
    montant_depense: Mapped[int] = mapped_column(Integer, default=0)
    justificatifs_json: Mapped[str | None] = mapped_column(JSON, default=list)
    date_maj: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    projet = relationship("ProjetRecherche", back_populates="budget")


class Publication(Base):
    """Table 4.2 - Publications scientifiques"""
    __tablename__ = "publications"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    auteurs_json: Mapped[str] = mapped_column(JSON, nullable=False)  # [{nom, prenom, affiliation}]
    titre: Mapped[str] = mapped_column(String(400), nullable=False)
    journal_conference: Mapped[str] = mapped_column(String(200), nullable=False)
    annee: Mapped[int] = mapped_column(Integer, nullable=False)
    doi: Mapped[str | None] = mapped_column(String(100), nullable=True, index=True)
    type_publication: Mapped[str] = mapped_column(String(30))  # article, communication, brevet, rapport
    fichier_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    citations_count: Mapped[int] = mapped_column(Integer, default=0)
    date_ajout: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    mots_cles_json: Mapped[str | None] = mapped_column(JSON, default=list)
    auteur_gabonais_principal: Mapped[bool] = mapped_column(Boolean, default=True)


class Laboratoire(Base):
    """Table 4.3 - Laboratoires de recherche"""
    __tablename__ = "laboratoires"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    responsable_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    localisation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    specialite: Mapped[str | None] = mapped_column(String(200), nullable=True)
    budget_annuel_fcfa: Mapped[int] = mapped_column(Integer, default=0)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relations
    responsable = relationship("User", back_populates="laboratoires_diriges")
    projets = relationship("ProjetRecherche", back_populates="laboratoire")
    equipements = relationship("Equipement", back_populates="laboratoire")


class Equipement(Base):
    """Table 4.3 - Équipements de laboratoire"""
    __tablename__ = "equipements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    labo_id: Mapped[int] = mapped_column(Integer, ForeignKey("laboratoires.id"), nullable=False)
    nom: Mapped[str] = mapped_column(String(200), nullable=False)
    reference: Mapped[str | None] = mapped_column(String(100), nullable=True)
    marque: Mapped[str | None] = mapped_column(String(100), nullable=True)
    etat: Mapped[str] = mapped_column(String(20), default="bon")  # bon, dégradé, en_panne, réformé
    date_acquisition: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    valeur_fcfa: Mapped[int] = mapped_column(Integer, default=0)
    prochaine_maintenance: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_derniere_maintenance: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    
    # Relation
    laboratoire = relationship("Laboratoire", back_populates="equipements")
    reservations = relationship("ReservationEquipement", back_populates="equipement")


class ReservationEquipement(Base):
    """Table 4.3 - Réservations d'équipements"""
    __tablename__ = "reservations_equipements"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    equipement_id: Mapped[int] = mapped_column(Integer, ForeignKey("equipements.id"), nullable=False)
    utilisateur_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    date_debut: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    motif: Mapped[str] = mapped_column(String(300), nullable=False)
    statut: Mapped[str] = mapped_column(String(20), default="demande")  # demande, validee, terminee, annulee
    date_demande: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relations
    equipement = relationship("Equipement", back_populates="reservations")
    utilisateur = relationship("User", back_populates="reservations_equipements")


class Partenariat(Base):
    """Table 4.4 - Partenariats internationaux"""
    __tablename__ = "partenariats"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    institution_partenaire: Mapped[str] = mapped_column(String(200), nullable=False)
    pays: Mapped[str] = mapped_column(String(100), nullable=False)
    type_partenariat: Mapped[str] = mapped_column(String(30))  # cotutelle, échange, recherche, formation
    date_signature: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_expiration: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    convention_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    responsable_gabon_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    statut: Mapped[str] = mapped_column(String(20), default="actif")  # actif, expire, en_attente, termine
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Relations
    responsable_gabon = relationship("User", back_populates="partenariats_gerees")
    mobilites = relationship("Mobilite", back_populates="partenariat")


class Mobilite(Base):
    """Table 4.4 - Mobilités internationales"""
    __tablename__ = "mobilites"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    partenariat_id: Mapped[int] = mapped_column(Integer, ForeignKey("partenariats.id"), nullable=False)
    personne_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    type_mobilite: Mapped[str] = mapped_column(String(20))  # sortant, entrant
    date_depart: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_retour: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    financement: Mapped[str | None] = mapped_column(String(100), nullable=True)
    rapport_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    statut: Mapped[str] = mapped_column(String(20), default="prevue")  # prevue, en_cours, terminee
    
    # Relations
    partenariat = relationship("Partenariat", back_populates="mobilites")
    personne = relationship("User", back_populates="mobilites_effectuees")


class BrevetIP(Base):
    """Table 4.5 - Brevets et propriété intellectuelle"""
    __tablename__ = "brevets_ip"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titre: Mapped[str] = mapped_column(String(300), nullable=False)
    inventeurs_json: Mapped[str] = mapped_column(JSON, nullable=False)  # [{nom, prenom, affiliation}]
    date_depot: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    numero_depot: Mapped[str | None] = mapped_column(String(100), nullable=True)
    office: Mapped[str] = mapped_column(String(20))  # OAPI, EPO, USPTO, INPI
    statut: Mapped[str] = mapped_column(String(30), default="depot")  # depot, examen, accorde, rejete, expire
    frais_json: Mapped[str | None] = mapped_column(JSON, default=list)  # [{type, montant, date, paye}]
    contrat_valorisation_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    date_echeance: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    resume: Mapped[str | None] = mapped_column(Text, nullable=True)
