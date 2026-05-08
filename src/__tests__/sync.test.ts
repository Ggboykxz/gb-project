import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn()
  }
}))

import { setActivePinia, createPinia } from 'pinia'
import { useSyncStore } from '@/stores/sync'

describe('useSyncStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('should initialize with default values', () => {
    const store = useSyncStore()
    expect(store.status).toBeNull()
    expect(store.isSyncing).toBe(false)
    expect(store.syncProgress).toBe(0)
  })

  it('should have isOnline computed', () => {
    const store = useSyncStore()
    expect(typeof store.isOnline).toBe('boolean')
  })

  it('should have hasPendingOperations computed', () => {
    const store = useSyncStore()
    expect(typeof store.hasPendingOperations).toBe('boolean')
  })

  it('should have hasConflicts computed', () => {
    const store = useSyncStore()
    expect(typeof store.hasConflicts).toBe('boolean')
  })

  it('should have fetchStatus action', () => {
    const store = useSyncStore()
    expect(typeof store.fetchStatus).toBe('function')
  })

  it('should have uploadChanges action', () => {
    const store = useSyncStore()
    expect(typeof store.uploadChanges).toBe('function')
  })

  it('should have downloadChanges action', () => {
    const store = useSyncStore()
    expect(typeof store.downloadChanges).toBe('function')
  })

  it('should have syncAll action', () => {
    const store = useSyncStore()
    expect(typeof store.syncAll).toBe('function')
  })

  it('should have fetchLogs action', () => {
    const store = useSyncStore()
    expect(typeof store.fetchLogs).toBe('function')
  })

  it('should have fetchConflicts action', () => {
    const store = useSyncStore()
    expect(typeof store.fetchConflicts).toBe('function')
  })

  it('should have resolveConflict action', () => {
    const store = useSyncStore()
    expect(typeof store.resolveConflict).toBe('function')
  })

  it('should have startConnectivityCheck action', () => {
    const store = useSyncStore()
    expect(typeof store.startConnectivityCheck).toBe('function')
  })

  it('should have stopConnectivityCheck action', () => {
    const store = useSyncStore()
    expect(typeof store.stopConnectivityCheck).toBe('function')
  })

  it('should manage isSyncing state', () => {
    const store = useSyncStore()
    expect(store.isSyncing).toBe(false)
  })

  it('should manage syncProgress state', () => {
    const store = useSyncStore()
    expect(store.syncProgress).toBe(0)
  })

  it('should manage logs state', () => {
    const store = useSyncStore()
    expect(Array.isArray(store.logs)).toBe(true)
  })

  it('should manage conflicts state', () => {
    const store = useSyncStore()
    expect(Array.isArray(store.conflicts)).toBe(true)
  })
})
