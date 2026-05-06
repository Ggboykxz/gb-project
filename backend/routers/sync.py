"""
Routes API pour la synchronisation Offline-First
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any

from database import get_db
from services.sync import SyncService, check_connectivity
from schemas.sync import (
    SyncStatusResponse,
    SyncOperationResponse,
    ConflictResolutionRequest,
    SyncManualRequest
)
from security.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/api/v1/sync", tags=["Synchronisation"])


@router.get("/status", response_model=SyncStatusResponse)
async def get_sync_status(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne l'état complet de la synchronisation"""
    service = SyncService(db)
    status = await service.get_sync_status()
    
    # Vérifier connectivité
    is_online = await check_connectivity()
    
    return SyncStatusResponse(
        **status,
        is_online=is_online
    )


@router.post("/upload", response_model=SyncOperationResponse)
async def upload_changes(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Déclenche l'envoi des opérations pending au serveur"""
    service = SyncService(db)
    result = await service.upload_changes()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return SyncOperationResponse(
        success=True,
        message=result["message"],
        count=result["count"],
        conflicts=result.get("conflicts", [])
    )


@router.post("/download", response_model=SyncOperationResponse)
async def download_changes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Déclenche le téléchargement des changements depuis le serveur"""
    service = SyncService(db)
    result = await service.download_changes()
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])
    
    return SyncOperationResponse(
        success=True,
        message=result["message"],
        count=result["count"],
        conflicts=[]
    )


@router.post("/sync-all", response_model=SyncOperationResponse)
async def sync_all(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Synchronisation complète: upload puis download"""
    service = SyncService(db)
    
    # Upload d'abord
    upload_result = await service.upload_changes()
    if upload_result["status"] == "error":
        raise HTTPException(status_code=500, detail=f"Upload échoué: {upload_result['message']}")
    
    # Puis download
    download_result = await service.download_changes()
    if download_result["status"] == "error":
        raise HTTPException(status_code=500, detail=f"Download échoué: {download_result['message']}")
    
    total_count = upload_result["count"] + download_result["count"]
    
    return SyncOperationResponse(
        success=True,
        message=f"Synchronisation complète: {total_count} opérations",
        count=total_count,
        conflicts=upload_result.get("conflicts", [])
    )


@router.post("/conflicts/resolve", response_model=Dict[str, Any])
async def resolve_conflict(
    request: ConflictResolutionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Résout un conflit de synchronisation"""
    service = SyncService(db)
    
    success = await service.resolve_conflict(
        conflict_id=request.conflict_id,
        resolution=request.resolution,
        merged_data=request.merged_data
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Échec de résolution du conflit")
    
    return {"success": True, "message": "Conflit résolu avec succès"}


@router.get("/conflicts", response_model=List[Dict[str, Any]])
async def get_conflicts(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne la liste des conflits non résolus"""
    from sqlalchemy import select
    from models.sync import ConflitSync
    
    stmt = select(ConflitSync).where(ConflitSync.status == "unresolved")
    result = await db.execute(stmt)
    conflicts = list(result.scalars().all())
    
    return [
        {
            "id": c.id,
            "table_name": c.table_name,
            "record_id": c.record_id,
            "local_data": c.local_data,
            "remote_data": c.remote_data,
            "detected_at": c.detected_at.isoformat(),
            "status": c.status
        }
        for c in conflicts
    ]


@router.get("/health")
async def health_check():
    """Endpoint de santé pour la détection de connectivité"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@router.post("/queue", response_model=Dict[str, Any])
async def queue_operation(
    operation: str,
    table_name: str,
    record_id: int,
    payload: Dict[str, Any],
    priority: str = "NORMAL",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Ajoute manuellement une opération à la file (pour tests)"""
    service = SyncService(db)
    
    sync_op = await service.queue_operation(
        operation=operation,
        table_name=table_name,
        record_id=record_id,
        payload=payload,
        priority=priority
    )
    
    return {
        "success": True,
        "operation_id": sync_op.id,
        "status": sync_op.status
    }
