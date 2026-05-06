"""Modèles Vie Étudiante - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean, ForeignKey
from datetime import datetime
from database import Base
import uuid

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    bio = Column(String(500))
    competences_json = Column(JSON, default=list)
    langues_json = Column(JSON, default=list)
    visibilite = Column(String(20), default="privé")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class ExperiencePortfolio(Base):
    __tablename__ = "experiences_portfolio"
    id = Column(String(36), primary_key=True)
    portfolio_id = Column(String(36), ForeignKey("portfolios.id"), nullable=False)
    type_experience = Column(String(30))  # stage, projet, certification, benevolat
    titre = Column(String(200), nullable=False)
    organisation = Column(String(200))
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    description = Column(String(1000))
    fichier_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class TypeBourse(Base):
    __tablename__ = "types_bourses"
    id = Column(String(36), primary_key=True)
    libelle = Column(String(200), nullable=False)
    montant_mensuel = Column(Integer)
    criteres_json = Column(JSON, default=dict)
    quota_annuel = Column(Integer)
    financeur = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class DossierBourse(Base):
    __tablename__ = "dossiers_bourses"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    type_bourse_id = Column(String(36), ForeignKey("types_bourses.id"), nullable=False)
    annee = Column(String(20))
    statut = Column(String(30), default="en_attente")
    score_social = Column(Integer)
    documents_json = Column(JSON, default=list)
    decision = Column(String(30))
    date_decision = Column(DateTime)
    commentaire = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class SuiviEtudiant(Base):
    __tablename__ = "suivis_etudiants"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    conseiller_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    type_alerte = Column(String(50))  # decrochage, echec, absence_repetee
    statut = Column(String(30), default="actif")
    notes_suivi_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class EntreprisePartenaire(Base):
    __tablename__ = "entreprises_partenaires"
    id = Column(String(36), primary_key=True)
    raison_sociale = Column(String(200), nullable=False)
    secteur = Column(String(100))
    localisation = Column(String(100))
    contact_rh = Column(String(200))
    conventions_json = Column(JSON, default=list)
    evaluation = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class OffreStageEmploi(Base):
    __tablename__ = "offres_stages_emplois"
    id = Column(String(36), primary_key=True)
    entreprise_id = Column(String(36), ForeignKey("entreprises_partenaires.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(String(1000))
    type_offre = Column(String(30))  # stage, cdi, cdd, alternance
    domaine = Column(String(100))
    localisation_gabon = Column(String(100))
    date_debut = Column(DateTime)
    date_limite = Column(DateTime)
    statut = Column(String(30), default="active")
    contact_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Candidature(Base):
    __tablename__ = "candidatures"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    offre_id = Column(String(36), ForeignKey("offres_stages_emploi.id"), nullable=False)
    date_candidature = Column(DateTime, default=datetime.utcnow)
    statut = Column(String(30), default="en_attente")
    cv_url = Column(String(500))
    lettre_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Alumni(Base):
    __tablename__ = "alumni"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    promo = Column(String(20))
    poste_actuel = Column(String(200))
    entreprise_actuelle = Column(String(200))
    localisation = Column(String(100))
    linkedin_url = Column(String(300))
    disponible_mentorat = Column(Boolean, default=False)
    domaines_expertise_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())