import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface SyncStatus {
  isOnline: boolean
  lastSync: Date | null
  pendingOperations: number
  status: 'online' | 'offline' | 'syncing' | 'error'
}

export const useSyncStore = defineStore('sync', () => {
  const syncStatus = ref<SyncStatus>({
    isOnline: false,
    lastSync: null,
    pendingOperations: 0,
    status: 'offline',
  })

  const isOnline = computed(() => syncStatus.value.isOnline)
  const lastSync = computed(() => syncStatus.value.lastSync)
  const status = computed(() => syncStatus.value.status)

  function setOnline(online: boolean) {
    syncStatus.value.isOnline = online
    syncStatus.value.status = online ? 'online' : 'offline'
  }

  function setSyncing(syncing: boolean) {
    if (syncing) {
      syncStatus.value.status = 'syncing'
    } else if (syncStatus.value.isOnline) {
      syncStatus.value.status = 'online'
      syncStatus.value.lastSync = new Date()
    }
  }

  function updatePendingOperations(count: number) {
    syncStatus.value.pendingOperations = count
  }

  return {
    syncStatus,
    isOnline,
    lastSync,
    status,
    setOnline,
    setSyncing,
    updatePendingOperations,
  }
})
