import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAdministrationStore } from '@/stores/administration'

vi.mock('@/lib/api', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    patch: vi.fn()
  }
}))

import * as apiModule from '@/lib/api'
const mockApi = apiModule.default

describe('useAdministrationStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.clearAllMocks()
  })

  describe('initialization', () => {
    it('should initialize with empty arrays', () => {
      const store = useAdministrationStore()
      expect(store.etudiants).toEqual([])
      expect(store.inscriptions).toEqual([])
      expect(store.filieres).toEqual([])
      expect(store.ues).toEqual([])
    })

    it('should initialize loading as false', () => {
      const store = useAdministrationStore()
      expect(store.loading).toBe(false)
    })

    it('should initialize error as null', () => {
      const store = useAdministrationStore()
      expect(store.error).toBeNull()
    })
  })

  describe('computed getters', () => {
    it('should have getEtudiantById function', () => {
      const store = useAdministrationStore()
      expect(typeof store.getEtudiantById).toBe('function')
    })

    it('should have getInscriptionsByFiliere function', () => {
      const store = useAdministrationStore()
      expect(typeof store.getInscriptionsByFiliere).toBe('function')
    })

    it('should have getUesByFiliere function', () => {
      const store = useAdministrationStore()
      expect(typeof store.getUesByFiliere).toBe('function')
    })

    it('should find etudiant by id', () => {
      const store = useAdministrationStore()
      store.etudiants = [
        { id: '1', nom: 'Test', prenom: 'One', nip_gabon: '123', email: 'a@c.ga', telephone: '111', date_naissance: '2000', genre: 'M', nationalite: 'GA', statut: 'ACTIF' },
        { id: '2', nom: 'Test', prenom: 'Two', nip_gabon: '456', email: 'b@c.ga', telephone: '222', date_naissance: '2001', genre: 'F', nationalite: 'GA', statut: 'ACTIF' }
      ]
      const found = store.getEtudiantById('1')
      expect(found?.nom).toBe('Test')
      expect(found?.prenom).toBe('One')
    })

    it('should return undefined for non-existent id', () => {
      const store = useAdministrationStore()
      store.etudiants = [{ id: '1', nom: 'Test', prenom: 'One', nip_gabon: '123', email: 'a@c.ga', telephone: '111', date_naissance: '2000', genre: 'M', nationalite: 'GA', statut: 'ACTIF' }]
      const found = store.getEtudiantById('999')
      expect(found).toBeUndefined()
    })

    it('should filter inscriptions by filiere', () => {
      const store = useAdministrationStore()
      store.inscriptions = [
        { id: '1', etudiant_id: '1', filiere_id: 'IC', annee_academique: '2024', niveau: 'L3', type: 'nouveau', statut_workflow: 'confirme', date_soumission: '2024', frais_payes: true },
        { id: '2', etudiant_id: '2', filiere_id: 'DROIT', annee_academique: '2024', niveau: 'L2', type: 'nouveau', statut_workflow: 'confirme', date_soumission: '2024', frais_payes: true },
        { id: '3', etudiant_id: '3', filiere_id: 'IC', annee_academique: '2024', niveau: 'L3', type: 'reinscription', statut_workflow: 'confirme', date_soumission: '2024', frais_payes: true }
      ]
      const filtered = store.getInscriptionsByFiliere('IC')
      expect(filtered).toHaveLength(2)
    })
  })

  describe('fetchEtudiants', () => {
    it('should fetch etudiants from API', async () => {
      const mockEtudiants = [
        { id: '1', nom: 'Ondo', prenom: 'Jean', nip_gabon: '123' },
        { id: '2', nom: 'Nguema', prenom: 'Marie', nip_gabon: '456' }
      ]
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockEtudiants } as any)
      
      const store = useAdministrationStore()
      await store.fetchEtudiants()
      
      expect(mockApi.get).toHaveBeenCalledWith('/etudiants')
      expect(store.etudiants).toEqual(mockEtudiants)
    })

    it('should handle fetch error', async () => {
      vi.mocked(mockApi.get).mockRejectedValue(new Error('Network error'))
      
      const store = useAdministrationStore()
      await store.fetchEtudiants()
      
      expect(store.error).toBe('Network error')
      expect(store.loading).toBe(false)
    })
  })

  describe('createEtudiant', () => {
    it('should create etudiant via API', async () => {
      const newEtudiant = { nom: 'Mba', prenom: 'Paul', nip_gabon: '789' }
      vi.mocked(mockApi.post).mockResolvedValue({ data: { id: '3', ...newEtudiant } } as any)
      
      const store = useAdministrationStore()
      const result = await store.createEtudiant(newEtudiant)
      
      expect(mockApi.post).toHaveBeenCalledWith('/etudiants', newEtudiant)
      expect(store.etudiants).toContainEqual({ id: '3', ...newEtudiant })
    })

    it('should throw error on failure', async () => {
      vi.mocked(mockApi.post).mockRejectedValue(new Error('Create failed'))
      
      const store = useAdministrationStore()
      await expect(store.createEtudiant({ nom: 'Test' } as any)).rejects.toThrow('Create failed')
    })
  })

  describe('updateEtudiant', () => {
    it('should update etudiant via API', async () => {
      const updated = { id: '1', nom: 'Ondo Updated', prenom: 'Jean', nip_gabon: '123' }
      vi.mocked(mockApi.put).mockResolvedValue({ data: updated } as any)
      
      const store = useAdministrationStore()
      store.etudiants = [{ id: '1', nom: 'Ondo', prenom: 'Jean', nip_gabon: '123', email: 'a@c.ga', telephone: '111', date_naissance: '2000', genre: 'M', nationalite: 'GA', statut: 'ACTIF' }]
      
      const result = await store.updateEtudiant('1', updated)
      
      expect(mockApi.put).toHaveBeenCalledWith('/etudiants/1', updated)
      expect(store.etudiants[0].nom).toBe('Ondo Updated')
    })
  })

  describe('fetchInscriptions', () => {
    it('should fetch inscriptions from API', async () => {
      const mockInscriptions = [{ id: '1', etudiant_id: '1', annee_academique: '2024-2025' }]
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockInscriptions } as any)
      
      const store = useAdministrationStore()
      await store.fetchInscriptions()
      
      expect(mockApi.get).toHaveBeenCalledWith('/inscriptions')
      expect(store.inscriptions).toEqual(mockInscriptions)
    })
  })

  describe('fetchFilieres', () => {
    it('should fetch filieres from API', async () => {
      const mockFilieres = [{ id: '1', code: 'IC', libelle: 'Informatique' }]
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockFilieres } as any)
      
      const store = useAdministrationStore()
      await store.fetchFilieres()
      
      expect(mockApi.get).toHaveBeenCalledWith('/filieres')
      expect(store.filieres).toEqual(mockFilieres)
    })
  })

  describe('fetchUes', () => {
    it('should fetch UEs from API', async () => {
      const mockUes = [{ id: '1', code_ue: 'INFO101', libelle: 'Algorithmique' }]
      vi.mocked(mockApi.get).mockResolvedValue({ data: mockUes } as any)
      
      const store = useAdministrationStore()
      await store.fetchUes()
      
      expect(mockApi.get).toHaveBeenCalledWith('/ues')
      expect(store.ues).toEqual(mockUes)
    })
  })
})
