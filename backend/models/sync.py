"""Modèles pour le module Synchronisation - Phase 6"""
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, Text, Enum as SQLEnum, JSON, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
import enum

from database import Base


class OperationSync(enum.Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class StatutSync(enum.Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    DONE = "done"
    FAILED = "failed"
    CONFLICT = "conflict"


class PrioriteSync(enum.Enum):
    HAUTE = "haute"
    NORMALE = "normale"
    BASSE = "basse"


class SyncQueue(Base):
    """Table principale de la file d'attente de synchronisation"""
    __tablename__ = "sync_queue"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    operation: Mapped[OperationSync] = mapped_column(SQLEnum(OperationSync), nullable=False)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)  # Données compressées LZ4 si > 1KB
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    statut: Mapped[StatutSync] = mapped_column(SQLEnum(StatutSync), default=StatutSync.PENDING)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)  # UUID de l'installation
    priorite: Mapped[PrioriteSync] = mapped_column(SQLEnum(PrioriteSync), default=PrioriteSync.NORMALE)
    sync_timestamp_server: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    conflict_data_json: Mapped[str | None] = mapped_column(JSON, nullable=True)  # En cas de conflit
    
    def __repr__(self):
        return f"<SyncQueue {self.operation} {self.table_name}:{self.record_id} [{self.statut}]>"


class SyncConfig(Base):
    """Configuration de synchronisation par appareil"""
    __tablename__ = "sync_config"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    device_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_sync_timestamp: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_successful_sync: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    total_syncs: Mapped[int] = mapped_column(Integer, default=0)
    failed_syncs: Mapped[int] = mapped_column(Integer, default=0)
    auto_sync_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    auto_sync_interval_seconds: Mapped[int] = mapped_column(Integer, default=300)  # 5 minutes
    wifi_only: Mapped[bool] = mapped_column(Boolean, default=False)
    compression_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    compression_threshold_bytes: Mapped[int] = mapped_column(Integer, default=1024)  # 1KB
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    date_maj: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SyncLog(Base):
    """Journal des opérations de synchronisation"""
    __tablename__ = "sync_logs"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    device_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    sync_type: Mapped[str] = mapped_column(String(20), nullable=False)  # upload, download, full
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="started")  # started, success, partial, failed
    records_uploaded: Mapped[int] = mapped_column(Integer, default=0)
    records_downloaded: Mapped[int] = mapped_column(Integer, default=0)
    bytes_sent: Mapped[int] = mapped_column(Integer, default=0)
    bytes_received: Mapped[int] = mapped_column(Integer, default=0)
    errors_json: Mapped[str | None] = mapped_column(JSON, default=list)
    conflicts_resolved: Mapped[int] = mapped_column(Integer, default=0)
    compression_ratio: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    def __repr__(self):
        return f"<SyncLog {self.sync_type} {self.status} at {self.start_time}>"


class ConflitSync(Base):
    """Journal des conflits de synchronisation"""
    __tablename__ = "conflits_sync"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    table_name: Mapped[str] = mapped_column(String(100), nullable=False)
    record_id: Mapped[int] = mapped_column(Integer, nullable=False)
    device_id_local: Mapped[str] = mapped_column(String(64), nullable=False)
    device_id_distant: Mapped[str] = mapped_column(String(64), nullable=False)
    local_value_json: Mapped[str] = mapped_column(Text, nullable=False)
    distant_value_json: Mapped[str] = mapped_column(Text, nullable=False)
    local_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    distant_timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    statut_resolution: Mapped[str] = mapped_column(String(30), default="en_attente")  # en_attente, resolu, ignore
    resolution_strategy: Mapped[str | None] = mapped_column(String(50), nullable=True)  # last_write_wins, manual, merge
    resolved_by: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    date_resolution: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    date_creation: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relation
    resolveur = relationship("User", back_populates="conflits_resolus")


class SyncMapping(Base):
    """Mapping des tables et priorités de synchronisation"""
    __tablename__ = "sync_mapping"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    table_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    priorite_defaut: Mapped[PrioriteSync] = mapped_column(SQLEnum(PrioriteSync), default=PrioriteSync.NORMALE)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    champs_sync_json: Mapped[str | None] = mapped_column(JSON, nullable=True)  # Liste des champs à synchroniser
    champ_timestamp: Mapped[str] = mapped_column(String(50), default="updated_at")
    dependances_json: Mapped[str | None] = mapped_column(JSON, default=list)  # Tables dépendantes
    date_maj: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
