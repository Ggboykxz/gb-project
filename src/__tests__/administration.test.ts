import { describe, it, expect, vi, beforeEach } from 'vitest'

vi.mock('@/lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn()
  }
}))

import { setActivePinia, createPinia } from 'pinia'
import { useAdministrationStore } from '@/stores/administration'

describe('useAdministrationStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('should initialize with empty arrays', () => {
    const store = useAdministrationStore()
    expect(store.etudiants).toEqual([])
    expect(store.inscriptions).toEqual([])
    expect(store.filieres).toEqual([])
    expect(store.ues).toEqual([])
    expect(store.loading).toBe(false)
    expect(store.error).toBeNull()
  })

  it('should have getEtudiantById getter', () => {
    const store = useAdministrationStore()
    expect(typeof store.getEtudiantById).toBe('function')
  })

  it('should have getInscriptionsByFiliere getter', () => {
    const store = useAdministrationStore()
    expect(typeof store.getInscriptionsByFiliere).toBe('function')
  })

  it('should have getUesByFiliere getter', () => {
    const store = useAdministrationStore()
    expect(typeof store.getUesByFiliere).toBe('function')
  })

  it('should have fetchEtudiants action', () => {
    const store = useAdministrationStore()
    expect(typeof store.fetchEtudiants).toBe('function')
  })

  it('should have createEtudiant action', () => {
    const store = useAdministrationStore()
    expect(typeof store.createEtudiant).toBe('function')
  })

  it('should have updateEtudiant action', () => {
    const store = useAdministrationStore()
    expect(typeof store.updateEtudiant).toBe('function')
  })

  it('should have fetchInscriptions action', () => {
    const store = useAdministrationStore()
    expect(typeof store.fetchInscriptions).toBe('function')
  })

  it('should have createInscription action', () => {
    const store = useAdministrationStore()
    expect(typeof store.createInscription).toBe('function')
  })

  it('should have validerInscription action', () => {
    const store = useAdministrationStore()
    expect(typeof store.validerInscription).toBe('function')
  })

  it('should have fetchFilieres action', () => {
    const store = useAdministrationStore()
    expect(typeof store.fetchFilieres).toBe('function')
  })

  it('should have createFiliere action', () => {
    const store = useAdministrationStore()
    expect(typeof store.createFiliere).toBe('function')
  })

  it('should have fetchUes action', () => {
    const store = useAdministrationStore()
    expect(typeof store.fetchUes).toBe('function')
  })

  it('should have createUE action', () => {
    const store = useAdministrationStore()
    expect(typeof store.createUE).toBe('function')
  })

  it('should manage loading state', async () => {
    const store = useAdministrationStore()
    expect(store.loading).toBe(false)
  })

  it('should manage error state', async () => {
    const store = useAdministrationStore()
    expect(store.error).toBeNull()
  })
})
