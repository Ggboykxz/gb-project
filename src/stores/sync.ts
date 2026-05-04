/**
 * Store Pinia pour la synchronisation Offline-First
 * Gère l'état de connectivité, la file d'attente locale et les conflits
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { api } from '@/lib/api';

export interface SyncStatus {
  pending_operations: number;
  failed_operations: number;
  unresolved_conflicts: number;
  last_sync: string | null;
  last_sync_status: string | null;
  device_id: string;
  is_online: boolean;
}

export interface SyncLog {
  id: number;
  direction: 'upload' | 'download';
  records_count: number;
  status: 'success' | 'error';
  started_at: string;
  completed_at: string | null;
  error_message: string | null;
}

export interface Conflict {
  id: number;
  table_name: string;
  record_id: number;
  local_data: any;
  remote_data: any;
  detected_at: string;
  status: string;
}

export const useSyncStore = defineStore('sync', () => {
  // État
  const status = ref<SyncStatus | null>(null);
  const isSyncing = ref(false);
  const syncProgress = ref(0);
  const logs = ref<SyncLog[]>([]);
  const conflicts = ref<Conflict[]>([]);
  const connectivityCheckInterval = ref<number | null>(null);

  // Getters
  const isOnline = computed(() => status.value?.is_online ?? false);
  const hasPendingOperations = computed(() => (status.value?.pending_operations ?? 0) > 0);
  const hasConflicts = computed(() => (status.value?.unresolved_conflicts ?? 0) > 0);
  const lastSyncDate = computed(() => {
    if (!status.value?.last_sync) return null;
    return new Date(status.value.last_sync);
  });

  // Actions
  async function fetchStatus() {
    try {
      const response = await api.get('/sync/status');
      status.value = response.data;
      return status.value;
    } catch (error) {
      console.error('Erreur lors de la récupération du statut de sync:', error);
      // En cas d'erreur, considérer comme hors ligne
      status.value = {
        pending_operations: 0,
        failed_operations: 0,
        unresolved_conflicts: 0,
        last_sync: null,
        last_sync_status: 'error',
        device_id: 'unknown',
        is_online: false
      };
      return status.value;
    }
  }

  async function uploadChanges() {
    isSyncing.value = true;
    syncProgress.value = 0;
    
    try {
      const response = await api.post('/sync/upload');
      syncProgress.value = 50;
      
      await fetchStatus();
      
      syncProgress.value = 100;
      setTimeout(() => { syncProgress.value = 0; }, 1000);
      
      return { success: true, ...response.data };
    } catch (error: any) {
      console.error('Erreur upload:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Échec de l\'upload' 
      };
    } finally {
      isSyncing.value = false;
    }
  }

  async function downloadChanges() {
    isSyncing.value = true;
    syncProgress.value = 0;
    
    try {
      const response = await api.post('/sync/download');
      syncProgress.value = 50;
      
      await fetchStatus();
      
      syncProgress.value = 100;
      setTimeout(() => { syncProgress.value = 0; }, 1000);
      
      return { success: true, ...response.data };
    } catch (error: any) {
      console.error('Erreur download:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Échec du download' 
      };
    } finally {
      isSyncing.value = false;
    }
  }

  async function syncAll() {
    isSyncing.value = true;
    syncProgress.value = 0;
    
    try {
      const response = await api.post('/sync/sync-all');
      syncProgress.value = 100;
      
      await fetchStatus();
      await fetchLogs();
      
      setTimeout(() => { syncProgress.value = 0; }, 2000);
      
      return { success: true, ...response.data };
    } catch (error: any) {
      console.error('Erreur sync all:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Échec de la synchronisation' 
      };
    } finally {
      isSyncing.value = false;
    }
  }

  async function fetchLogs() {
    try {
      logs.value = [];
    } catch (error) {
      console.error('Erreur récupération logs:', error);
    }
  }

  async function fetchConflicts() {
    try {
      const response = await api.get('/sync/conflicts');
      conflicts.value = response.data;
      return conflicts.value;
    } catch (error) {
      console.error('Erreur récupération conflits:', error);
      return [];
    }
  }

  async function resolveConflict(conflictId: number, resolution: 'local' | 'remote' | 'merge', mergedData?: any) {
    try {
      const response = await api.post('/sync/conflicts/resolve', {
        conflict_id: conflictId,
        resolution,
        merged_data: mergedData
      });
      
      await fetchConflicts();
      await fetchStatus();
      
      return { success: true, ...response.data };
    } catch (error: any) {
      console.error('Erreur résolution conflit:', error);
      return { 
        success: false, 
        message: error.response?.data?.detail || 'Échec de la résolution' 
      };
    }
  }

  function startConnectivityCheck(intervalMs: number = 30000) {
    fetchStatus();
    
    if (connectivityCheckInterval.value) {
      clearInterval(connectivityCheckInterval.value);
    }
    
    connectivityCheckInterval.value = window.setInterval(() => {
      fetchStatus();
    }, intervalMs);
  }

  function stopConnectivityCheck() {
    if (connectivityCheckInterval.value) {
      clearInterval(connectivityCheckInterval.value);
      connectivityCheckInterval.value = null;
    }
  }

  startConnectivityCheck(30000);

  return {
    status,
    isSyncing,
    syncProgress,
    logs,
    conflicts,
    isOnline,
    hasPendingOperations,
    hasConflicts,
    lastSyncDate,
    fetchStatus,
    uploadChanges,
    downloadChanges,
    syncAll,
    fetchLogs,
    fetchConflicts,
    resolveConflict,
    startConnectivityCheck,
    stopConnectivityCheck
  };
});
