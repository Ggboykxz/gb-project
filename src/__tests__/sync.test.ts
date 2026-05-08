import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useSyncStore } from '@/stores/sync'

vi.mock('@/lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

import * as apiModule from '@/lib/api'
const mockApi = apiModule.default

describe('useSyncStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('initialization', () => {
    it('should initialize with default values', () => {
      const store = useSyncStore()
      expect(store.status).toBeNull()
      expect(store.isSyncing).toBe(false)
      expect(store.syncProgress).toBe(0)
    })

    it('should initialize logs as empty array', () => {
      const store = useSyncStore()
      expect(Array.isArray(store.logs)).toBe(true)
      expect(store.logs).toHaveLength(0)
    })

    it('should initialize conflicts as empty array', () => {
      const store = useSyncStore()
      expect(Array.isArray(store.conflicts)).toBe(true)
      expect(store.conflicts).toHaveLength(0)
    })
  })

  describe('computed properties', () => {
    it('should compute isOnline as false when status is null', () => {
      const store = useSyncStore()
      expect(store.isOnline).toBe(false)
    })

    it('should compute hasPendingOperations as false when status is null', () => {
      const store = useSyncStore()
      expect(store.hasPendingOperations).toBe(false)
    })

    it('should compute hasConflicts as false when status is null', () => {
      const store = useSyncStore()
      expect(store.hasConflicts).toBe(false)
    })

    it('should compute lastSyncDate as null when no sync', () => {
      const store = useSyncStore()
      expect(store.lastSyncDate).toBeNull()
    })

    it('should return isOnline true when status is online', () => {
      const store = useSyncStore()
      store.status = {
        pending_operations: 0,
        failed_operations: 0,
        unresolved_conflicts: 0,
        last_sync: null,
        last_sync_status: null,
        device_id: 'test',
        is_online: true
      }
      expect(store.isOnline).toBe(true)
    })

    it('should return hasPendingOperations true when pending > 0', () => {
      const store = useSyncStore()
      store.status = {
        pending_operations: 5,
        failed_operations: 0,
        unresolved_conflicts: 0,
        last_sync: null,
        last_sync_status: null,
        device_id: 'test',
        is_online: true
      }
      expect(store.hasPendingOperations).toBe(true)
    })

    it('should return hasConflicts true when conflicts > 0', () => {
      const store = useSyncStore()
      store.status = {
        pending_operations: 0,
        failed_operations: 0,
        unresolved_conflicts: 3,
        last_sync: null,
        last_sync_status: null,
        device_id: 'test',
        is_online: true
      }
      expect(store.hasConflicts).toBe(true)
    })
  })

  describe('fetchStatus', () => {
    it('should fetch status from API', async () => {
      const mockStatus = {
        pending_operations: 5,
        failed_operations: 2,
        unresolved_conflicts: 1,
        last_sync: '2024-01-15T10:30:00Z',
        last_sync_status: 'success',
        device_id: 'device-123',
        is_online: true
      }
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockStatus } as any)
      
      const store = useSyncStore()
      const result = await store.fetchStatus()
      
      expect(mockApi.get).toHaveBeenCalledWith('/sync/status')
      expect(store.status).toEqual(mockStatus)
    })

    it('should set default status on error', async () => {
      vi.mocked(mockApi.get).mockRejectedValue(new Error('Network error'))
      
      const store = useSyncStore()
      const result = await store.fetchStatus()
      
      expect(store.status).toEqual({
        pending_operations: 0,
        failed_operations: 0,
        unresolved_conflicts: 0,
        last_sync: null,
        last_sync_status: 'error',
        device_id: 'unknown',
        is_online: false
      })
    })
  })

  describe('uploadChanges', () => {
    it('should upload changes successfully', async () => {
      vi.mocked(mockApi.post).mockResolvedValue({ data: { uploaded: 5 } } as any)
      
      const store = useSyncStore()
      store.status = {
        pending_operations: 5,
        failed_operations: 0,
        unresolved_conflicts: 0,
        last_sync: null,
        last_sync_status: null,
        device_id: 'test',
        is_online: true
      }
      
      const result = await store.uploadChanges()
      
      expect(mockApi.post).toHaveBeenCalledWith('/sync/upload')
      expect(result.success).toBe(true)
    })

    it('should handle upload failure', async () => {
      vi.mocked(mockApi.post).mockRejectedValue({ response: { data: { detail: 'Upload failed' } } })

      const store = useSyncStore()
      const result = await store.uploadChanges()
      
      expect(result.success).toBe(false)
      expect(result.message).toBe('Upload failed')
    })
  })

  describe('downloadChanges', () => {
    it('should download changes successfully', async () => {
      vi.mocked(mockApi.post).mockResolvedValue({ data: { downloaded: 10 } } as any)
      
      const store = useSyncStore()
      const result = await store.downloadChanges()
      
      expect(mockApi.post).toHaveBeenCalledWith('/sync/download')
      expect(result.success).toBe(true)
    })

    it('should handle download failure', async () => {
      vi.mocked(mockApi.post).mockRejectedValue({ response: { data: { detail: 'Download failed' } } })

      const store = useSyncStore()
      const result = await store.downloadChanges()
      
      expect(result.success).toBe(false)
      expect(result.message).toBe('Download failed')
    })
  })

  describe('syncAll', () => {
    it('should sync all data successfully', async () => {
      vi.mocked(mockApi.post).mockResolvedValue({ data: { synced: true } } as any)
      
      const store = useSyncStore()
      const result = await store.syncAll()
      
      expect(mockApi.post).toHaveBeenCalledWith('/sync/sync-all')
      expect(result.success).toBe(true)
    })

    it('should handle sync failure', async () => {
      vi.mocked(mockApi.post).mockRejectedValue({ response: { data: { detail: 'Sync failed' } } })

      const store = useSyncStore()
      const result = await store.syncAll()
      
      expect(result.success).toBe(false)
      expect(result.message).toBe('Sync failed')
    })
  })

  describe('fetchConflicts', () => {
    it('should fetch conflicts from API', async () => {
      const mockConflicts = [{ id: 1, table_name: 'etudiants', record_id: 123 }]
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockConflicts } as any)
      
      const store = useSyncStore()
      const result = await store.fetchConflicts()
      
      expect(mockApi.get).toHaveBeenCalledWith('/sync/conflicts')
      expect(result).toEqual(mockConflicts)
    })

    it('should handle fetch conflicts error', async () => {
      vi.mocked(mockApi.get).mockRejectedValue(new Error('Error'))
      
      const store = useSyncStore()
      const result = await store.fetchConflicts()
      
      expect(result).toEqual([])
    })
  })

  describe('resolveConflict', () => {
    it('should resolve conflict successfully', async () => {
      vi.mocked(mockApi.post).mockResolvedValue({ data: { resolved: true } } as any)
      
      const store = useSyncStore()
      const result = await store.resolveConflict(1, 'local')
      
      expect(mockApi.post).toHaveBeenCalledWith('/sync/conflicts/resolve', {
        conflict_id: 1,
        resolution: 'local',
        merged_data: undefined
      })
      expect(result.success).toBe(true)
    })

    it('should handle resolve conflict failure', async () => {
      vi.mocked(mockApi.post).mockRejectedValue({ response: { data: { detail: 'Resolve failed' } } })

      const store = useSyncStore()
      const result = await store.resolveConflict(1, 'local')
      
      expect(result.success).toBe(false)
      expect(result.message).toBe('Resolve failed')
    })
  })

  describe('connectivity check', () => {
    it('should have startConnectivityCheck function', () => {
      const store = useSyncStore()
      expect(typeof store.startConnectivityCheck).toBe('function')
    })

    it('should have stopConnectivityCheck function', () => {
      const store = useSyncStore()
      expect(typeof store.stopConnectivityCheck).toBe('function')
    })
  })
})
