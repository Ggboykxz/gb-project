"""
Modèles SQLAlchemy pour le module Gestion Financière & Logistique
Phase 5 - GabonEdu Campus
"""

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, 
    Enum, Text, Boolean, JSON, Date, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from database import Base


# ─── 5.1 FACTURATION & RECOUVREMENT ───

class ModePaiement(str, enum.Enum):
    ESPECES = "especes"
    MOOV_MONEY = "moov_money"
    AIRTEL_MONEY = "airtel_money"
    VIREMENT = "virement"
    CHEQUE = "cheque"


class OperateurPaiement(str, enum.Enum):
    MOOV = "Moov"
    AIRTEL = "Airtel"
    BGFIBANK = "BGFIBank"
    UGB = "UGB"
    NONE = "none"


class TypeRelance(str, enum.Enum):
    PREMIER = "1er"
    DEUXIEME = "2eme"
    TROISIEME = "3eme"
    SUSPENSION = "suspension"


class CanalRelance(str, enum.Enum):
    SMS = "sms"
    EMAIL = "email"
    COURRIER = "courrier"


class FraisScolarite(Base):
    """Configuration des frais de scolarité par filière et niveau"""
    __tablename__ = "frais_scolarite"
    
    id = Column(Integer, primary_key=True, index=True)
    filiere_id = Column(Integer, ForeignKey("filiere.id"), nullable=False)
    annee_academique = Column(String(9), nullable=False, index=True)  # ex: "2024-2025"
    niveau = Column(String(20), nullable=False)  # L1, L2, L3, M1, M2, D1...
    montant_inscription_fcfa = Column(Numeric(12, 2), default=0)
    montant_scolarite_fcfa = Column(Numeric(12, 2), default=0)
    echeancier_json = Column(JSON, default=list)  # [{echeance: "2024-10-01", montant: 50000}, ...]
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    filiere = relationship("Filiere", back_populates="frais_scolarite")
    paiements = relationship("Paiement", back_populates="frais_scolarite_config")


class Paiement(Base):
    """Enregistrement des paiements effectués par les étudiants"""
    __tablename__ = "paiement"
    
    id = Column(Integer, primary_key=True, index=True)
    inscription_id = Column(Integer, ForeignKey("inscription.id"), nullable=False, index=True)
    frais_scolarite_id = Column(Integer, ForeignKey("frais_scolarite.id"), nullable=True)
    montant_fcfa = Column(Numeric(12, 2), nullable=False)
    date_paiement = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    mode_paiement = Column(Enum(ModePaiement), nullable=False)
    operateur = Column(Enum(OperateurPaiement), default=OperateurPaiement.NONE)
    reference_transaction = Column(String(100), unique=True, nullable=True)  # ID transaction mobile money
    recu_url = Column(String(500), nullable=True)  # Chemin vers le PDF du reçu
    saisi_par = Column(Integer, ForeignKey("user.id"), nullable=False)
    commentaire = Column(Text, nullable=True)
    statut = Column(String(20), default="validé")  # validé, en_attente, annulé
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    inscription = relationship("Inscription", back_populates="paiements")
    frais_scolarite_config = relationship("FraisScolarite", back_populates="paiements")
    utilisateur = relationship("User", back_populates="paiements_saisis")


class Relance(Base):
    """Gestion des relances pour impayés"""
    __tablename__ = "relance"
    
    id = Column(Integer, primary_key=True, index=True)
    inscription_id = Column(Integer, ForeignKey("inscription.id"), nullable=False, index=True)
    type_relance = Column(Enum(TypeRelance), nullable=False)
    date_envoi = Column(DateTime(timezone=True), server_default=func.now())
    canal = Column(Enum(CanalRelance), nullable=False)
    statut = Column(String(20), default="envoyée")  # envoyée, lue, ignorée
    contenu = Column(Text, nullable=True)  # Message personnalisé
    destinaire = Column(String(100), nullable=True)  # Email ou téléphone
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    inscription = relationship("Inscription", back_populates="relances")


# ─── 5.2 BUDGET & COMPTABILITÉ ANALYTIQUE ───

class StatutBudget(str, enum.Enum):
    PREVISIONNEL = "prévisionnel"
    VOTE = "voté"
    REVISE = "révisé"
    EXECUTE = "exécuté"


class BudgetDepartement(Base):
    """Budget annuel par département"""
    __tablename__ = "budget_departement"
    
    id = Column(Integer, primary_key=True, index=True)
    departement_id = Column(Integer, ForeignKey("filiere.id"), nullable=True)  # NULL pour budget général
    annee = Column(String(4), nullable=False, index=True)
    lignes_budgetaires_json = Column(JSON, default=list)  # [{code: "6061", libelle: "Fournitures", prevu: 1000000, realise: 850000}, ...]
    statut = Column(Enum(StatutBudget), default=StatutBudget.PREVISIONNEL)
    total_prevu_fcfa = Column(Numeric(15, 2), default=0)
    total_realise_fcfa = Column(Numeric(15, 2), default=0)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    departement = relationship("Filiere", back_populates="budgets")
    ecritures = relationship("EcritureComptable", back_populates="budget")


class EcritureComptable(Base):
    """Écritures comptables selon plan OHADA"""
    __tablename__ = "ecriture_comptable"
    
    id = Column(Integer, primary_key=True, index=True)
    date_ecriture = Column(Date, nullable=False, index=True)
    libelle = Column(String(255), nullable=False)
    compte_debit = Column(String(20), nullable=False)  # Ex: 5211 (Banque)
    compte_credit = Column(String(20), nullable=False)  # Ex: 7011 (Ventes)
    montant_fcfa = Column(Numeric(15, 2), nullable=False)
    piece_justificative_url = Column(String(500), nullable=True)
    departement_id = Column(Integer, ForeignKey("filiere.id"), nullable=True)
    projet_id = Column(Integer, ForeignKey("projet_recherche.id"), nullable=True)
    budget_id = Column(Integer, ForeignKey("budget_departement.id"), nullable=True)
    saisie_par = Column(Integer, ForeignKey("user.id"), nullable=False)
    validee = Column(Boolean, default=False)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    budget = relationship("BudgetDepartement", back_populates="ecritures")
    departement = relationship("Filiere", back_populates="ecritures_comptables")
    projet = relationship("ProjetRecherche", back_populates="ecritures_comptables")
    utilisateur = relationship("User", back_populates="ecritures_saisies")


# ─── 5.3 MARCHÉS PUBLICS INTERNES ───

class StatutDemandeAchat(str, enum.Enum):
    DEMANDE = "demande"
    VISA_CHEF = "visa_chef"
    APPEL_OFFRES = "appel_offres"
    DEPOUILLEMENT = "depouillement"
    ATTRIBUTION = "attribution"
    RECEPTION = "reception"
    PAIEMENT = "paiement"
    CLOTURE = "cloture"


class UrgenceAchat(str, enum.Enum):
    NORMALE = "normale"
    URGENTE = "urgente"
    CRITIQUE = "critique"


class Fournisseur(Base):
    """Registre des fournisseurs agréés"""
    __tablename__ = "fournisseur"
    
    id = Column(Integer, primary_key=True, index=True)
    raison_sociale = Column(String(255), nullable=False, index=True)
    nif_gabon = Column(String(20), unique=True, nullable=True)  # Numéro Identification Fiscale
    activite = Column(String(100), nullable=True)
    contact_nom = Column(String(100), nullable=True)
    contact_telephone = Column(String(20), nullable=True)
    contact_email = Column(String(100), nullable=True)
    adresse = Column(Text, nullable=True)
    historique_commandes_json = Column(JSON, default=list)
    evaluation = Column(Float, default=0.0)  # Note sur 5
    agree = Column(Boolean, default=False)
    date_agrement = Column(Date, nullable=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    demandes = relationship("DemandeAchat", back_populates="fournisseur_retenu")


class DemandeAchat(Base):
    """Demandes d'achat et marchés publics internes"""
    __tablename__ = "demande_achat"
    
    id = Column(Integer, primary_key=True, index=True)
    departement_id = Column(Integer, ForeignKey("filiere.id"), nullable=False)
    demandeur_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    objet = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    montant_estime_fcfa = Column(Numeric(15, 2), nullable=False)
    urgence = Column(Enum(UrgenceAchat), default=UrgenceAchat.NORMALE)
    statut_workflow = Column(Enum(StatutDemandeAchat), default=StatutDemandeAchat.DEMANDE)
    fournisseur_retenu_id = Column(Integer, ForeignKey("fournisseur.id"), nullable=True)
    bon_commande_url = Column(String(500), nullable=True)
    facture_url = Column(String(500), nullable=True)
    date_demande = Column(DateTime(timezone=True), server_default=func.now())
    date_validation = Column(DateTime(timezone=True), nullable=True)
    date_reception = Column(DateTime(timezone=True), nullable=True)
    commentaires_json = Column(JSON, default=list)  # Historique des validations
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    departement = relationship("Filiere", back_populates="demandes_achat")
    demandeur = relationship("User", back_populates="demandes_achat")
    fournisseur_retenu = relationship("Fournisseur", back_populates="demandes")


# ─── 5.4 PATRIMOINE & MAINTENANCE ───

class EtatBien(str, enum.Enum):
    NEUF = "neuf"
    BON = "bon"
    DEGRADE = "dégradé"
    EN_PANNE = "en_panne"
    REFORME = "réformé"


class TypeBien(str, enum.Enum):
    IMMOBILIER = "immobilier"
    MOBILIER = "mobilier"
    EQUIPEMENT = "équipement"
    VEHICULE = "véhicule"
    INFORMATIQUE = "informatique"


class BienImmobilier(Base):
    """Inventaire des biens immobiliers et équipements"""
    __tablename__ = "bien_immobilier"
    
    id = Column(Integer, primary_key=True, index=True)
    designation = Column(String(255), nullable=False)
    type_bien = Column(Enum(TypeBien), nullable=False)
    batiment = Column(String(100), nullable=True)
    localisation_detail = Column(String(100), nullable=True)
    superficie_m2 = Column(Float, nullable=True)
    valeur_fcfa = Column(Numeric(15, 2), default=0)
    etat = Column(Enum(EtatBien), default=EtatBien.BON)
    date_acquisition = Column(Date, nullable=True)
    affectation = Column(String(100), nullable=True)  # Département/service affectataire
    numero_inventaire = Column(String(50), unique=True, nullable=True)
    observations = Column(Text, nullable=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    interventions = relationship("InterventionMaintenance", back_populates="bien")


class UrgenceMaintenance(str, enum.Enum):
    CRITIQUE = "critique"
    NORMALE = "normale"
    PLANIFIEE = "planifiée"


class TypeMaintenance(str, enum.Enum):
    PREVENTIF = "préventif"
    CURATIF = "curatif"
    CORRECTIF = "correctif"


class InterventionMaintenance(Base):
    """Suivi des interventions de maintenance"""
    __tablename__ = "intervention_maintenance"
    
    id = Column(Integer, primary_key=True, index=True)
    bien_id = Column(Integer, ForeignKey("bien_immobilier.id"), nullable=False, index=True)
    type_maintenance = Column(Enum(TypeMaintenance), nullable=False)
    description = Column(Text, nullable=False)
    urgence = Column(Enum(UrgenceMaintenance), default=UrgenceMaintenance.NORMALE)
    statut = Column(String(20), default="ouverte")  # ouverte, en_cours, terminee, closee
    technicien = Column(String(100), nullable=True)
    cout_fcfa = Column(Numeric(15, 2), default=0)
    date_intervention = Column(DateTime(timezone=True), nullable=True)
    date_demande = Column(DateTime(timezone=True), server_default=func.now())
    rapport_url = Column(String(500), nullable=True)
    photos_avant_apres_json = Column(JSON, default=list)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    bien = relationship("BienImmobilier", back_populates="interventions")


# ─── 5.5 RESSOURCES HUMAINES ───

class TypePersonnel(str, enum.Enum):
    ENSEIGNANT = "enseignant"
    ADMINISTRATIF = "administratif"
    TECHNIQUE = "technique"
    VACATAIRE = "vacataire"
    STAGIAIRE = "stagiaire"


class StatutPersonnel(str, enum.Enum):
    ACTIF = "actif"
    CONGE = "congé"
    DETACHEMENT = "détachement"
    RETRAITE = "retraite"
    SUSPENDU = "suspendu"


class Personnel(Base):
    """Gestion du personnel de l'université"""
    __tablename__ = "personnel"
    
    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    matricule = Column(String(20), unique=True, nullable=False, index=True)
    type_personnel = Column(Enum(TypePersonnel), nullable=False)
    grade = Column(String(50), nullable=True)  # Professeur, Maître de conférences, etc.
    departement_id = Column(Integer, ForeignKey("filiere.id"), nullable=True)
    date_embauche = Column(Date, nullable=False)
    date_naissance = Column(Date, nullable=True)
    telephone = Column(String(20), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    salaire_brut_fcfa = Column(Numeric(12, 2), default=0)
    contrat_url = Column(String(500), nullable=True)
    statut = Column(Enum(StatutPersonnel), default=StatutPersonnel.ACTIF)
    photo_url = Column(String(500), nullable=True)
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    date_modification = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    departement = relationship("Filiere", back_populates="personnels")
    conges = relationship("CongeAbsence", back_populates="personnel")
    evaluations = relationship("EvaluationPersonnel", back_populates="personnel")
    heures_vacations = relationship("HeureVacation", back_populates="vacataire")


class TypeConge(str, enum.Enum):
    ANNUAL = "annuel"
    MALADIE = "maladie"
    MATERNITE = "maternité"
    PATERNITE = "paternité"
    SANS_SOLDE = "sans_solde"
    FORMATION = "formation"
    AUTRE = "autre"


class CongeAbsence(Base):
    """Gestion des congés et absences"""
    __tablename__ = "conge_absence"
    
    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id"), nullable=False, index=True)
    type_conge = Column(Enum(TypeConge), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    statut = Column(String(20), default="en_attente")  # en_attente, validé, refusé
    valide_par = Column(Integer, ForeignKey("user.id"), nullable=True)
    justificatif_url = Column(String(500), nullable=True)
    commentaire = Column(Text, nullable=True)
    date_demande = Column(DateTime(timezone=True), server_default=func.now())
    date_validation = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    personnel = relationship("Personnel", back_populates="conges")
    validateur = relationship("User", back_populates="conges_valides")


class EvaluationPersonnel(Base):
    """Évaluations annuelles du personnel"""
    __tablename__ = "evaluation_personnel"
    
    id = Column(Integer, primary_key=True, index=True)
    personnel_id = Column(Integer, ForeignKey("personnel.id"), nullable=False, index=True)
    evaluateur_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    annee = Column(String(4), nullable=False, index=True)
    criteres_json = Column(JSON, default=dict)  # {competence_pedagogique: 4, ponctualite: 5, ...}
    note_globale = Column(Float, default=0.0)  # Sur 5 ou 20
    commentaire = Column(Text, nullable=True)
    objectifs_suivants_json = Column(JSON, default=list)
    date_evaluation = Column(DateTime(timezone=True), server_default=func.now())
    date_creation = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    personnel = relationship("Personnel", back_populates="evaluations")
    evaluateur = relationship("User", back_populates="evaluations_faites")


class HeureVacation(Base):
    """Suivi des heures de vacation pour les vacataires"""
    __tablename__ = "heure_vacation"
    
    id = Column(Integer, primary_key=True, index=True)
    vacataire_id = Column(Integer, ForeignKey("personnel.id"), nullable=False, index=True)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=True)
    ue_id = Column(Integer, ForeignKey("ue.id"), nullable=True)
    date_vacation = Column(Date, nullable=False)
    nombre_heures = Column(Float, nullable=False)
    taux_horaire_fcfa = Column(Numeric(10, 2), default=0)
    montant_total_fcfa = Column(Numeric(12, 2), default=0)
    statut_paiement = Column(String(20), default="a_payer")  # a_payer, payé
    observation = Column(Text, nullable=True)
    valide_par = Column(Integer, ForeignKey("user.id"), nullable=True)
    date_saisie = Column(DateTime(timezone=True), server_default=func.now())
    date_validation = Column(DateTime(timezone=True), nullable=True)
    
    # Relations
    vacataire = relationship("Personnel", back_populates="heures_vacations")
    cours = relationship("Cours", back_populates="heures_vacations")
    ue = relationship("UE", back_populates="heures_vacations")
    validateur = relationship("User", back_populates="vacations_validees")
