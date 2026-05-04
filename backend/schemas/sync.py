"""Pydantic schemas for synchronisation module"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum


class OperationType(str, Enum):
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"


class SyncStatusEnum(str, Enum):
    PENDING = "pending"
    SYNCING = "syncing"
    DONE = "done"
    FAILED = "failed"
    CONFLICT = "conflict"


class SyncPriority(str, Enum):
    HAUTE = "haute"
    NORMALE = "normale"
    BASSE = "basse"


class SyncQueueBase(BaseModel):
    operation: OperationType
    table_name: str
    record_id: int
    payload_json: dict
    device_id: str
    priority: SyncPriority = SyncPriority.NORMALE


class SyncQueueCreate(SyncQueueBase):
    pass


class SyncQueueUpdate(BaseModel):
    status: Optional[SyncStatusEnum] = None
    retry_count: Optional[int] = None
    error_message: Optional[str] = None


class SyncQueueResponse(SyncQueueBase):
    id: int
    timestamp: datetime
    status: SyncStatusEnum
    retry_count: int = 0
    error_message: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)


class SyncBatchRequest(BaseModel):
    operations: List[SyncQueueCreate]
    last_sync_timestamp: Optional[datetime] = None


class SyncBatchResponse(BaseModel):
    uploaded_count: int
    downloaded_count: int
    conflicts: List[dict] = Field(default_factory=list)
    new_sync_timestamp: datetime


class ConflictResolution(str, Enum):
    LOCAL_WINS = "local_wins"
    SERVER_WINS = "server_wins"
    MANUAL = "manual"


class ResolveConflictRequest(BaseModel):
    sync_queue_id: int
    resolution: ConflictResolution
    merged_data: Optional[dict] = None


class SyncStats(BaseModel):
    total_pending: int
    by_priority: dict
    by_operation: dict
    failed_count: int
    last_successful_sync: Optional[datetime] = None


class SyncStatusResponse(BaseModel):
    pending_operations: int
    failed_operations: int
    unresolved_conflicts: int
    last_sync: Optional[str]
    last_sync_status: Optional[str]
    device_id: str
    is_online: bool


class SyncOperationResponse(BaseModel):
    success: bool
    message: str
    count: int
    conflicts: List[dict] = []


class ConflictResolutionRequest(BaseModel):
    conflict_id: int
    resolution: str  # "local", "remote", "merge"
    merged_data: Optional[dict] = None


class SyncManualRequest(BaseModel):
    operation: str
    table_name: str
    record_id: int
    payload: dict
    priority: str = "NORMAL"


class SyncLogResponse(BaseModel):
    id: int
    direction: str
    records_count: int
    status: str
    started_at: str
    completed_at: Optional[str]
    error_message: Optional[str]

    model_config = ConfigDict(from_attributes=True)
