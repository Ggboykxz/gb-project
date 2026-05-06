"""Modèles Pédagogie - VERSION TRÈS SIMPLIFIÉE"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Boolean, Text
from datetime import datetime
from database import Base
import uuid

class Ouvrage(Base):
    __tablename__ = "ouvrages"
    id = Column(String(36), primary_key=True)
    titre = Column(String(300), nullable=False, index=True)
    auteurs_json = Column(JSON, default=list)
    isbn = Column(String(20))
    annee_publication = Column(Integer)
    editeur = Column(String(100))
    domaine = Column(String(100))
    localisation_physique = Column(String(50))
    exemplaires_total = Column(Integer, default=1)
    exemplaires_dispo = Column(Integer, default=1)
    fichier_pdf_local = Column(String(500))
    couverture_url = Column(String(500))
    resume = Column(Text)
    mots_cles_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Pret(Base):
    __tablename__ = "prets"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    ouvrage_id = Column(String(36), ForeignKey("ouvrages.id"), nullable=False)
    date_pret = Column(DateTime, default=datetime.utcnow)
    date_retour_prevue = Column(DateTime, nullable=False)
    date_retour_effective = Column(DateTime)
    statut = Column(String(20), default="en_cours")
    penalite_fcfa = Column(Integer, default=0)
    renouvellements = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class MemoireThese(Base):
    __tablename__ = "memoires_theses"
    id = Column(String(36), primary_key=True)
    etudiant_id = Column(String(36), ForeignKey("etudiants.id"), nullable=False)
    directeur_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    titre = Column(String(400), nullable=False)
    resume = Column(Text)
    mots_cles_json = Column(JSON, default=list)
    annee = Column(Integer, nullable=False)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    type_document = Column(String(20))
    version_courante = Column(Integer, default=1)
    statut_validation = Column(String(30), default="depot")
    fichier_url = Column(String(500))
    embargo_jusqu_au = Column(DateTime)
    date_depot = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Sujet(Base):
    __tablename__ = "sujets"
    id = Column(String(36), primary_key=True)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    enseignant_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    titre = Column(String(200), nullable=False)
    type_sujet = Column(String(20))
    difficulte = Column(Integer, default=1)
    annee_utilisation = Column(Integer)
    fichier_url = Column(String(500))
    tags_json = Column(JSON, default=list)
    nb_utilisations = Column(Integer, default=0)
    est_archive = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class EpreuveExamen(Base):
    __tablename__ = "epreuves_examens"
    id = Column(String(36), primary_key=True)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    session = Column(String(20), default="normale")
    date_examen = Column(DateTime, nullable=False)
    duree_minutes = Column(Integer, nullable=False)
    salle_ids_json = Column(JSON, default=list)
    sujets_selectionnes_json = Column(JSON, default=list)
    statut = Column(String(30), default="planifie")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())