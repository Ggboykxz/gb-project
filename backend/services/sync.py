"""
Service de synchronisation Offline-First
Gère la file d'attente, la compression LZ4, la résolution de conflits
et la synchronisation bidirectionnelle avec le serveur central.
"""
import json
import lz4.frame
import httpx
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from models.sync import SyncQueue, SyncLog, ConflitSync, SyncConfig
from database import get_db

# Configuration
SYNC_SERVER_URL = "https://sync.gabon-edu.ga/api/v1"  # Mock en dev
BATCH_SIZE = 50
COMPRESSION_THRESHOLD = 1024  # 1KB


class SyncService:
    """Service principal de synchronisation"""
    
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.device_id = self._get_device_id()
    
    def _get_device_id(self) -> str:
        """Récupère l'UUID unique de l'appareil"""
        # En production: lire depuis Tauri secure storage
        # Ici: valeur mockée
        return "device-uuid-12345"
    
    async def queue_operation(
        self,
        operation: str,
        table_name: str,
        record_id: int,
        payload: Dict[str, Any],
        priority: str = "NORMAL"
    ) -> SyncQueue:
        """Ajoute une opération à la file de synchronisation"""
        sync_op = SyncQueue(
            operation=operation,
            table_name=table_name,
            record_id=record_id,
            payload_json=json.dumps(payload),
            device_id=self.device_id,
            status="pending",
            priority=priority,
            retry_count=0
        )
        self.db.add(sync_op)
        await self.db.commit()
        await self.db.refresh(sync_op)
        return sync_op
    
    async def get_pending_operations(self, limit: int = BATCH_SIZE) -> List[SyncQueue]:
        """Récupère les opérations en attente, triées par priorité"""
        priority_order = {"HAUTE": 0, "NORMAL": 1, "BASSE": 2}
        
        stmt = (
            select(SyncQueue)
            .where(SyncQueue.status == "pending")
            .order_by(
                SyncQueue.priority.asc(),
                SyncQueue.timestamp.asc()
            )
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
    
    def _compress_payload(self, data: str) -> bytes:
        """Compresse les données avec LZ4 si > 1KB"""
        if len(data.encode('utf-8')) > COMPRESSION_THRESHOLD:
            return lz4.frame.compress(data.encode('utf-8'))
        return data.encode('utf-8')
    
    async def upload_changes(self) -> Dict[str, Any]:
        """Envoie les opérations pending au serveur central"""
        pending_ops = await self.get_pending_operations()
        
        if not pending_ops:
            return {"status": "success", "message": "Aucune opération à synchroniser", "count": 0}
        
        # Préparer le batch
        batch = []
        for op in pending_ops:
            batch.append({
                "id": op.id,
                "operation": op.operation,
                "table_name": op.table_name,
                "record_id": op.record_id,
                "payload": json.loads(op.payload_json),
                "device_id": op.device_id,
                "timestamp": op.timestamp.isoformat()
            })
        
        # Compression du batch
        batch_json = json.dumps(batch)
        compressed_data = self._compress_payload(batch_json)
        
        try:
            # Envoi au serveur (mock en dev)
            async with httpx.AsyncClient(timeout=30.0) as client:
                headers = {
                    "Content-Encoding": "lz4" if len(compressed_data) < len(batch_json.encode('utf-8')) else "identity",
                    "X-Device-ID": self.device_id
                }
                
                # En mode mock: simuler la réponse
                # response = await client.post(
                #     f"{SYNC_SERVER_URL}/sync/upload",
                #     content=compressed_data,
                #     headers=headers
                # )
                
                # Mock response
                server_response = {
                    "status": "success",
                    "processed_count": len(batch),
                    "conflicts": [],
                    "server_timestamp": datetime.now(timezone.utc).isoformat()
                }
            
            # Marquer les opérations comme terminées
            for op in pending_ops:
                op.status = "done"
                op.synced_at = datetime.now(timezone.utc)
            
            await self.db.commit()
            
            # Logger la synchronisation
            log = SyncLog(
                direction="upload",
                records_count=len(batch),
                status="success",
                started_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
            self.db.add(log)
            await self.db.commit()
            
            return {
                "status": "success",
                "message": f"{len(batch)} opérations synchronisées",
                "count": len(batch),
                "conflicts": server_response.get("conflicts", [])
            }
            
        except Exception as e:
            # Marquer comme échec
            for op in pending_ops:
                op.status = "failed"
                op.error_message = str(e)
                op.retry_count += 1
            await self.db.commit()
            
            return {"status": "error", "message": str(e), "count": 0}
    
    async def download_changes(self, last_sync_timestamp: Optional[datetime] = None) -> Dict[str, Any]:
        """Récupère les changements depuis le serveur"""
        if last_sync_timestamp is None:
            # Récupérer le dernier timestamp local
            stmt = select(SyncConfig).where(SyncConfig.key == "last_sync_timestamp")
            result = await self.db.execute(stmt)
            config = result.scalar_one_or_none()
            last_sync_timestamp = datetime.fromisoformat(config.value) if config else None
        
        try:
            # Appel au serveur (mock en dev)
            async with httpx.AsyncClient(timeout=30.0) as client:
                params = {}
                if last_sync_timestamp:
                    params["since"] = last_sync_timestamp.isoformat()
                
                # response = await client.get(
                #     f"{SYNC_SERVER_URL}/sync/download",
                #     params=params
                # )
                # changes = response.json()
                
                # Mock: générer des changements fictifs
                changes = {
                    "students": [],
                    "inscriptions": [],
                    "notes": [],
                    "payments": []
                }
            
            # Appliquer les changements locaux
            applied_count = 0
            for table_name, records in changes.items():
                for record in records:
                    await self._apply_remote_change(table_name, record)
                    applied_count += 1
            
            # Mettre à jour le timestamp
            new_timestamp = datetime.now(timezone.utc)
            await self._update_sync_config("last_sync_timestamp", new_timestamp.isoformat())
            
            # Logger
            log = SyncLog(
                direction="download",
                records_count=applied_count,
                status="success",
                started_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
            self.db.add(log)
            await self.db.commit()
            
            return {
                "status": "success",
                "message": f"{applied_count} changements appliqués",
                "count": applied_count
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e), "count": 0}
    
    async def _apply_remote_change(self, table_name: str, record: Dict[str, Any]):
        """Applique un changement venant du serveur"""
        # Logique simplifiée - à adapter selon les tables réelles
        # Détection de conflit basée sur updated_at
        pass
    
    async def resolve_conflict(
        self,
        conflict_id: int,
        resolution: str,  # "local", "remote", "merge"
        merged_data: Optional[Dict] = None
    ) -> bool:
        """Résout un conflit de synchronisation"""
        stmt = select(ConflitSync).where(ConflitSync.id == conflict_id)
        result = await self.db.execute(stmt)
        conflict = result.scalar_one_or_none()
        
        if not conflict:
            return False
        
        if resolution == "local":
            data = json.loads(conflict.local_data)
        elif resolution == "remote":
            data = json.loads(conflict.remote_data)
        elif resolution == "merge" and merged_data:
            data = merged_data
        else:
            return False
        
        # Ré-ajouter l'opération avec les données résolues
        await self.queue_operation(
            operation="UPDATE",
            table_name=conflict.table_name,
            record_id=conflict.record_id,
            payload=data,
            priority="HAUTE"
        )
        
        # Marquer le conflit comme résolu
        conflict.status = "resolved"
        conflict.resolved_at = datetime.now(timezone.utc)
        conflict.resolution_strategy = resolution
        
        await self.db.commit()
        return True
    
    async def _update_sync_config(self, key: str, value: str):
        """Met à jour la configuration de sync"""
        stmt = select(SyncConfig).where(SyncConfig.key == key)
        result = await self.db.execute(stmt)
        config = result.scalar_one_or_none()
        
        if config:
            config.value = value
        else:
            config = SyncConfig(key=key, value=value)
            self.db.add(config)
        
        await self.db.commit()
    
    async def get_sync_status(self) -> Dict[str, Any]:
        """Retourne l'état complet de la synchronisation"""
        # Compter les opérations par statut
        stmt_pending = select(SyncQueue).where(SyncQueue.status == "pending")
        result = await self.db.execute(stmt_pending)
        pending = len(list(result.scalars().all()))
        
        stmt_failed = select(SyncQueue).where(SyncQueue.status == "failed")
        result = await self.db.execute(stmt_failed)
        failed = len(list(result.scalars().all()))
        
        stmt_conflicts = select(ConflitSync).where(ConflitSync.status == "unresolved")
        result = await self.db.execute(stmt_conflicts)
        conflicts = len(list(result.scalars().all()))
        
        # Dernier sync
        stmt_log = select(SyncLog).order_by(SyncLog.completed_at.desc()).limit(1)
        result = await self.db.execute(stmt_log)
        last_log = result.scalar_one_or_none()
        
        return {
            "pending_operations": pending,
            "failed_operations": failed,
            "unresolved_conflicts": conflicts,
            "last_sync": last_log.completed_at.isoformat() if last_log else None,
            "last_sync_status": last_log.status if last_log else None,
            "device_id": self.device_id
        }
    
    async def clear_old_logs(self, days: int = 30):
        """Nettoie les anciens logs de synchronisation"""
        from sqlalchemy import func
        cutoff_date = datetime.now(timezone.utc).replace(
            day=datetime.now(timezone.utc).day - days
        )
        
        stmt = delete(SyncLog).where(SyncLog.completed_at < cutoff_date)
        await self.db.execute(stmt)
        await self.db.commit()


async def check_connectivity() -> bool:
    """Vérifie la connectivité réseau vers le serveur de sync"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # En mode mock: toujours connecté
            # response = await client.get(f"{SYNC_SERVER_URL}/health")
            # return response.status_code == 200
            return True  # Mock: considéré connecté
    except Exception:
        return False
