"""Modèles Recherche - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Float
from datetime import datetime
from database import Base
import uuid

class ProjetRecherche(Base):
    __tablename__ = "projets_recherche"
    id = Column(String(36), primary_key=True)
    titre = Column(String(400), nullable=False)
    responsable_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    laboratoire_id = Column(String(36), ForeignKey("laboratoires.id"), nullable=True)
    type_projet = Column(String(50))  # fondamentale, appliquee, developpement
    date_debut = Column(DateTime)
    date_fin = Column(DateTime)
    budget_total = Column(Integer, default=0)
    statut = Column(String(30), default="en_cours")
    partenaires_json = Column(JSON, default=list)
    mots_cles_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Laboratoire(Base):
    __tablename__ = "laboratoires"
    id = Column(String(36), primary_key=True)
    nom = Column(String(200), nullable=False)
    responsable_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    localisation = Column(String(100))
    specialite = Column(String(100))
    budget_annuel = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Publication(Base):
    __tablename__ = "publications"
    id = Column(String(36), primary_key=True)
    auteurs_json = Column(JSON, default=list)
    titre = Column(String(400), nullable=False)
    journal_conference = Column(String(200))
    annee = Column(Integer)
    doi = Column(String(100))
    type_publication = Column(String(50))  # article, communication, rapport
    fichier_url = Column(String(500))
    citations_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Equipement(Base):
    __tablename__ = "equipements"
    id = Column(String(36), primary_key=True)
    labo_id = Column(String(36), ForeignKey("laboratoires.id"), nullable=False)
    nom = Column(String(200), nullable=False)
    reference = Column(String(100))
    marque = Column(String(100))
    etat = Column(String(30), default="bon")  # bon, degrade, en_panne, reforme
    date_acquisition = Column(DateTime)
    valeur_fcfa = Column(Integer, default=0)
    prochaine_maintenance = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Partenariat(Base):
    __tablename__ = "partenariats"
    id = Column(String(36), primary_key=True)
    institution_partenaire = Column(String(200), nullable=False)
    pays = Column(String(100))
    type_partenariat = Column(String(50))  # cotutelle, exchange, recherche, formation
    date_signature = Column(DateTime)
    date_expiration = Column(DateTime)
    convention_url = Column(String(500))
    responsable_gabon_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    statut = Column(String(30), default="actif")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())