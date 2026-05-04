import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api } from '../lib/api'

export interface Etudiant {
  id: string
  nip_gabon: string
  nom: string
  prenom: string
  date_naissance: string
  genre: string
  nationalite: string
  telephone: string
  email: string
  photo_url?: string
  statut: string
}

export interface Inscription {
  id: string
  etudiant_id: string
  annee_academique: string
  filiere_id: string
  niveau: string
  type: 'nouveau' | 'reinscription'
  statut_workflow: 'soumis' | 'valide_scol' | 'valide_doyen' | 'confirme'
  date_soumission: string
  frais_payes: boolean
  etudiant?: Etudiant
}

export interface Filiere {
  id: string
  code: string
  libelle: string
  domaine: string
  niveau: 'L' | 'M' | 'D'
  duree_annees: number
  responsable_id?: string
}

export interface UE {
  id: string
  filiere_id: string
  code_ue: string
  libelle: string
  credits_ects: number
  semestre: number
  heures_cm: number
  heures_td: number
  heures_tp: number
  coefficient: number
  ue_type: 'obligatoire' | 'optionnel'
}

export const useAdministrationStore = defineStore('administration', () => {
  // État
  const etudiants = ref<Etudiant[]>([])
  const inscriptions = ref<Inscription[]>([])
  const filieres = ref<Filiere[]>([])
  const ues = ref<UE[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const getEtudiantById = computed(() => (id: string) => 
    etudiants.value.find(e => e.id === id)
  )

  const getInscriptionsByFiliere = computed(() => (filiereId: string) => 
    inscriptions.value.filter(i => i.filiere_id === filiereId)
  )

  const getUesByFiliere = computed(() => (filiereId: string) => 
    ues.value.filter(u => u.filiere_id === filiereId)
  )

  // Actions - Étudiants
  async function fetchEtudiants() {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/v1/etudiants')
      etudiants.value = response.data
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createEtudiant(data: Partial<Etudiant>) {
    loading.value = true
    try {
      const response = await api.post('/api/v1/etudiants', data)
      etudiants.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function updateEtudiant(id: string, data: Partial<Etudiant>) {
    loading.value = true
    try {
      const response = await api.put(`/api/v1/etudiants/${id}`, data)
      const index = etudiants.value.findIndex(e => e.id === id)
      if (index !== -1) etudiants.value[index] = response.data
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  // Actions - Inscriptions
  async function fetchInscriptions() {
    loading.value = true
    try {
      const response = await api.get('/api/v1/inscriptions')
      inscriptions.value = response.data
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createInscription(data: Partial<Inscription>) {
    loading.value = true
    try {
      const response = await api.post('/api/v1/inscriptions', data)
      inscriptions.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  async function validerInscription(id: string, statut: string) {
    loading.value = true
    try {
      const response = await api.patch(`/api/v1/inscriptions/${id}/valider`, { statut })
      const index = inscriptions.value.findIndex(i => i.id === id)
      if (index !== -1) inscriptions.value[index] = response.data
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  // Actions - Filières
  async function fetchFilieres() {
    loading.value = true
    try {
      const response = await api.get('/api/v1/filieres')
      filieres.value = response.data
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createFiliere(data: Partial<Filiere>) {
    loading.value = true
    try {
      const response = await api.post('/api/v1/filieres', data)
      filieres.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  // Actions - UE
  async function fetchUes() {
    loading.value = true
    try {
      const response = await api.get('/api/v1/ues')
      ues.value = response.data
    } catch (e: any) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  async function createUE(data: Partial<UE>) {
    loading.value = true
    try {
      const response = await api.post('/api/v1/ues', data)
      ues.value.push(response.data)
      return response.data
    } catch (e: any) {
      error.value = e.message
      throw e
    } finally {
      loading.value = false
    }
  }

  return {
    // État
    etudiants,
    inscriptions,
    filieres,
    ues,
    loading,
    error,
    // Getters
    getEtudiantById,
    getInscriptionsByFiliere,
    getUesByFiliere,
    // Actions
    fetchEtudiants,
    createEtudiant,
    updateEtudiant,
    fetchInscriptions,
    createInscription,
    validerInscription,
    fetchFilieres,
    createFiliere,
    fetchUes,
    createUE
  }
})
