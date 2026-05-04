from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Float, Date, Time, Enum as SQLEnum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base

class TypeCours(str, enum.Enum):
    CM = "CM"  # Cours Magistral
    TD = "TD"  # Travaux Dirigés
    TP = "TP"  # Travaux Pratiques

class StatutCours(str, enum.Enum):
    PLANIFIE = "PLANIFIE"
    EN_COURS = "EN_COURS"
    TERMINE = "TERMINE"
    ANNULE = "ANNULE"

class JourSemaine(str, enum.Enum):
    LUNDI = "LUNDI"
    MARDI = "MARDI"
    MERCREDI = "MERCREDI"
    JEUDI = "JEUDI"
    VENDREDI = "VENDREDI"
    SAMEDI = "SAMEDI"

class Salle(Base):
    __tablename__ = "salles"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(50), nullable=False)
    capacite = Column(Integer, nullable=False)
    type_salle = Column(SQLEnum('amphi', 'td', 'tp', 'info', name='type_salle_enum'), nullable=False)
    equipements_json = Column(JSON, default=list)
    batiment = Column(String(100))
    etage = Column(String(10))
    disponible = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    cours = relationship("Cours", back_populates="salle")

class Cours(Base):
    __tablename__ = "cours"

    id = Column(Integer, primary_key=True, index=True)
    ue_id = Column(Integer, ForeignKey("ues.id"), nullable=False, index=True)
    enseignant_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    titre_seance = Column(String(200), nullable=False)
    type_cours = Column(SQLEnum(TypeCours), nullable=False)
    date_cours = Column(Date, nullable=False, index=True)
    heure_debut = Column(Time, nullable=False)
    heure_fin = Column(Time, nullable=False)
    salle_id = Column(Integer, ForeignKey("salles.id"), nullable=True)
    groupe = Column(String(50))
    semaine_type = Column(SQLEnum('A', 'B', 'toutes', name='semaine_type_enum'), default='toutes')
    statut = Column(SQLEnum(StatutCours), default=StatutCours.PLANIFIE)
    support_url = Column(Text)
    description = Column(Text)
    couleur_hex = Column(String(7), default="#1B4F72")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    ue = relationship("UE", back_populates="cours")
    enseignant = relationship("User", back_populates="cours_donnes")
    salle = relationship("Salle", back_populates="cours")
    presences = relationship("Presence", back_populates="cours")

class Presence(Base):
    __tablename__ = "presences"

    id = Column(Integer, primary_key=True, index=True)
    cours_id = Column(Integer, ForeignKey("cours.id"), nullable=False, index=True)
    inscription_id = Column(Integer, ForeignKey("inscriptions.id"), nullable=False)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"), nullable=False, index=True)
    statut = Column(SQLEnum('present', 'absent', 'retard', 'justifie', name='presence_statut'), default='absent')
    heure_pointage = Column(DateTime(timezone=True), nullable=True)
    mode = Column(SQLEnum('manuel', 'qr', name='presence_mode'), default='manuel')
    justificatif_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    cours = relationship("Cours", back_populates="presences")
    etudiant = relationship("Etudiant", back_populates="presences")
