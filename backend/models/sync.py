"""Modèles Synchronisation - VERSION CORRIGÉE"""
from sqlalchemy import Column, String, DateTime, Integer, JSON, Boolean
from datetime import datetime
from database import Base
import uuid

class SyncQueue(Base):
    __tablename__ = "sync_queue"
    id = Column(String(36), primary_key=True)
    operation = Column(String(20))  # CREATE, UPDATE, DELETE
    table_name = Column(String(50), nullable=False)
    record_id = Column(String(36), nullable=False)
    payload_json = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="pending")  # pending, syncing, done, failed, conflict
    retry_count = Column(Integer, default=0)
    error_message = Column(String(500))
    device_id = Column(String(36))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class SyncLog(Base):
    __tablename__ = "sync_logs"
    id = Column(String(36), primary_key=True)
    direction = Column(String(20))  # upload, download
    records_count = Column(Integer, default=0)
    status = Column(String(20))  # success, error
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error_message = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class ConflitSync(Base):
    __tablename__ = "conflits_sync"
    id = Column(String(36), primary_key=True)
    table_name = Column(String(50), nullable=False)
    record_id = Column(String(36), nullable=False)
    local_data = Column(JSON, default=dict)
    remote_data = Column(JSON, default=dict)
    detected_at = Column(DateTime, default=datetime.utcnow)
    statut = Column(String(20), default="non_resolu")
    resolution = Column(String(20))
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())

class SyncConfig(Base):
    __tablename__ = "sync_config"
    id = Column(String(36), primary_key=True)
    sync_server_url = Column(String(300))
    device_id = Column(String(36), unique=True)
    last_sync = Column(DateTime)
    auto_sync_enabled = Column(Boolean, default=True)
    sync_interval_minutes = Column(Integer, default=30)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.id:
            self.id = str(uuid.uuid4())