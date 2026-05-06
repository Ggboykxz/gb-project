"""Modèles Finances - VERSION CORRIGÉE"""
import enum
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, JSON, Boolean, Float
from datetime import datetime
from database import Base
import uuid

# Enums
class ModePaiement(enum.Enum):
    ESPECES = "especes"
    MOBILE_MONEY = "mobile_money"
    VIREMENT = "virement"
    CHEQUE = "cheque"

class TypeRelance(enum.Enum):
    PREMIER = "1er"
    DEUXIEME = "2eme"
    TROISIEME = "3eme"
    SUSPENSION = "suspension"

class CanalRelance(enum.Enum):
    SMS = "sms"
    EMAIL = "email"
    COURRIER = "courrier"

class StatutBudget(enum.Enum):
    PREVISIONNEL = "previsionnel"
    VOTE = "vote"
    REVISION = "revisé"

class StatutDemandeAchat(enum.Enum):
    SOUMISE = "soumise"
    EN_COURS = "en_cours"
    APPROUVEE = "approuvee"
    REJETEE = "rejetee"

class UrgenceAchat(enum.Enum):
    CRITIQUE = "critique"
    NORMALE = "normale"
    PLANIFIEE = "planifiee"

class TypeBien(enum.Enum):
    BÂTIMENT = "batiment"
    MATERIEL = "materiel"
    MOBILIER = "mobilier"
    TERRAIN = "terrain"

class TypeMaintenance(enum.Enum):
    PREVENTIF = "preventif"
    CURATIF = "curatif"
    AMELIORATION = "amelioration"

class UrgenceMaintenance(enum.Enum):
    CRITIQUE = "critique"
    NORMALE = "normale"
    PLANIFIEE = "planifiee"

class TypePersonnel(enum.Enum):
    ENSEIGNANT = "enseignant"
    ADMINISTRATIF = "administratif"
    VACATAIRE = "vacataire"

class StatutPersonnel(enum.Enum):
    ACTIF = "actif"
    CONGE = "conge"
    SUSPENDU = "suspendu"
    RETRAITE = "retraite"

class TypeConge(enum.Enum):
    ANNUEL = "annuel"
    MALADIE = "maladie"
    MATERNITE = "maternite"
    AUTRE = "autre"

class FraisScolarite(Base):
    __tablename__ = "frais_scolarite"
    id = Column(String(36), primary_key=True)
    filiere_id = Column(String(36), ForeignKey("filieres.id"), nullable=False)
    annee_academique = Column(String(20), nullable=False)
    niveau = Column(String(10), nullable=False)
    montant_inscription = Column(Integer, default=0)
    montant_scolarite = Column(Integer, default=0)
    echeancier_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Paiement(Base):
    __tablename__ = "paiements"
    id = Column(String(36), primary_key=True)
    inscription_id = Column(String(36), ForeignKey("inscriptions.id"), nullable=False)
    montant = Column(Integer, nullable=False)
    date_paiement = Column(DateTime, default=datetime.utcnow)
    mode_paiement = Column(String(30))
    reference_transaction = Column(String(100))
    operateur = Column(String(30))
    recu_url = Column(String(500))
    saisi_par = Column(String(36), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Relance(Base):
    __tablename__ = "relances"
    id = Column(String(36), primary_key=True)
    inscription_id = Column(String(36), ForeignKey("inscriptions.id"), nullable=False)
    type_relance = Column(String(30))
    date_envoi = Column(DateTime, default=datetime.utcnow)
    canal = Column(String(30))
    statut = Column(String(30), default="envoyee")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class BudgetDepartement(Base):
    __tablename__ = "budgets_departements"
    id = Column(String(36), primary_key=True)
    departement = Column(String(100))
    annee = Column(String(10))
    lignes_budgetaires_json = Column(JSON, default=list)
    statut = Column(String(30), default="previsionnel")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class EcritureComptable(Base):
    __tablename__ = "ecritures_comptables"
    id = Column(String(36), primary_key=True)
    date_ecriture = Column(DateTime, default=datetime.utcnow)
    libelle = Column(String(200))
    compte_debit = Column(String(20))
    compte_credit = Column(String(20))
    montant = Column(Float, default=0)
    piece_justificative_url = Column(String(500))
    departement_id = Column(String(36), nullable=True)
    projet_id = Column(String(36), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Fournisseur(Base):
    __tablename__ = "fournisseurs"
    id = Column(String(36), primary_key=True)
    raison_sociale = Column(String(200), nullable=False)
    nif_gabon = Column(String(50))
    activite = Column(String(100))
    contact = Column(String(200))
    historique_json = Column(JSON, default=list)
    evaluation = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class BienImmobilier(Base):
    __tablename__ = "biens_immobiliers"
    id = Column(String(36), primary_key=True)
    designation = Column(String(200), nullable=False)
    batiment = Column(String(100))
    superficie = Column(Integer)
    valeur_fcfa = Column(Integer, default=0)
    etat = Column(String(50), default="bon")
    date_acquisition = Column(DateTime)
    affectation = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class Personnel(Base):
    __tablename__ = "personnel"
    id = Column(String(36), primary_key=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    matricule = Column(String(50), unique=True)
    type_personnel = Column(String(30))
    grade = Column(String(100))
    departement_id = Column(String(36), nullable=True)
    date_embauche = Column(DateTime)
    salaire_brut = Column(Integer, default=0)
    contrat_url = Column(String(500))
    statut = Column(String(30), default="actif")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class DemandeAchat(Base):
    __tablename__ = "demandes_achats"
    id = Column(String(36), primary_key=True)
    departement_id = Column(String(36), nullable=True)
    demandeur_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    objet = Column(String(300), nullable=False)
    montant_estime = Column(Integer, default=0)
    urgence = Column(String(30), default="normale")
    statut_workflow = Column(String(30), default="soumise")
    fournisseur_retenu_id = Column(String(36), ForeignKey("fournisseurs.id"), nullable=True)
    bon_commande_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class InterventionMaintenance(Base):
    __tablename__ = "interventions_maintenance"
    id = Column(String(36), primary_key=True)
    bien_id = Column(String(36), ForeignKey("biens_immobiliers.id"), nullable=False)
    type_intervention = Column(String(30))
    description = Column(String(500))
    urgence = Column(String(30), default="normale")
    statut = Column(String(30), default="en_attente")
    technicien = Column(String(100))
    cout_fcfa = Column(Integer, default=0)
    date_intervention = Column(DateTime)
    rapport_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class CongeAbsence(Base):
    __tablename__ = "conges_absences"
    id = Column(String(36), primary_key=True)
    personnel_id = Column(String(36), ForeignKey("personnel.id"), nullable=False)
    type_conge = Column(String(30))
    date_debut = Column(DateTime, nullable=False)
    date_fin = Column(DateTime, nullable=False)
    statut = Column(String(30), default="en_attente")
    valide_par = Column(String(36), ForeignKey("users.id"), nullable=True)
    justificatif_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class EvaluationPersonnel(Base):
    __tablename__ = "evaluations_personnel"
    id = Column(String(36), primary_key=True)
    personnel_id = Column(String(36), ForeignKey("personnel.id"), nullable=False)
    evaluateur_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    annee = Column(String(10))
    criteres_json = Column(JSON, default=dict)
    note_globale = Column(Float)
    commentaire = Column(String(500))
    objectifs_suivants_json = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class HeureVacation(Base):
    __tablename__ = "heures_vacations"
    id = Column(String(36), primary_key=True)
    personnel_id = Column(String(36), ForeignKey("personnel.id"), nullable=False)
    ue_id = Column(String(36), ForeignKey("ues.id"), nullable=False)
    nombre_heures = Column(Integer, default=0)
    taux_horaire = Column(Integer, default=0)
    mois = Column(String(10))
    annee = Column(String(10))
    statut = Column(String(30), default="en_attente")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())