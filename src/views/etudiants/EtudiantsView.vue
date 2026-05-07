<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { 
  Users, 
  Search, 
  Plus, 
  Download,
  Upload,
  Filter,
  MoreVertical,
  Phone,
  Mail,
  GraduationCap,
  FileText,
  AlertCircle,
  Loader2,
  RefreshCw,
  UserPlus,
  FileCheck
} from 'lucide-vue-next'
import { fetchWithAuth } from '@/api/auth'

const searchQuery = ref('')
const activeTab = ref('inscriptions')
const loading = ref(false)
const etudiants = ref<any[]>([])
const inscriptions = ref<any[]>([])

const tabs = [
  { id: 'inscriptions', label: 'Inscriptions', icon: UserPlus },
  { id: 'dossiers', label: 'Dossiers académiques', icon: FileText },
  { id: 'documents', label: 'Documents', icon: FileCheck },
]

const stats = ref({
  total: 0,
  inscriptions_annee: 0,
  en_attente: 0,
  nouveaux: 0
})

const etudiantsFiltres = computed(() => {
  if (!searchQuery.value) return etudiants.value
  const query = searchQuery.value.toLowerCase()
  return etudiants.value.filter(e => 
    e.nom?.toLowerCase().includes(query) ||
    e.prenom?.toLowerCase().includes(query) ||
    e.nip_gabon?.toLowerCase().includes(query) ||
    e.email?.toLowerCase().includes(query)
  )
})

async function fetchEtudiants() {
  try {
    loading.value = true
    const token = localStorage.getItem('auth_token')
    if (!token) return

    const response = await fetchWithAuth('http://127.0.0.1:8765/api/v1/admin/etudiants')
    if (response.ok) {
      etudiants.value = await response.json()
      stats.value.total = etudiants.value.length
    }
  } catch (e) {
    console.error('Failed to fetch etudiants:', e)
  } finally {
    loading.value = false
  }
}

async function fetchInscriptions() {
  try {
    const token = localStorage.getItem('auth_token')
    const response = await fetchWithAuth('http://127.0.0.1:8765/api/v1/admin/inscriptions')
    if (response.ok) {
      inscriptions.value = await response.json()
      stats.value.inscriptions_annee = inscriptions.value.length
      stats.value.en_attente = inscriptions.value.filter((i: any) => 
        i.statut_workflow !== 'CONFIRME'
      ).length
    }
  } catch (e) {
    console.error('Failed to fetch inscriptions:', e)
  }
}

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'ACTIF': 'bg-green-100 text-green-800',
    'SUSPENDU': 'bg-red-100 text-red-800',
    'EXCLU': 'bg-gray-100 text-gray-800',
    'DIPLOME': 'bg-blue-100 text-blue-800',
    'ABANDON': 'bg-gray-100 text-gray-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function formatStatutInscription(statut: string) {
  const colors: Record<string, string> = {
    'CONFIRME': 'bg-green-100 text-green-800',
    'VALIDE_DOyEN': 'bg-blue-100 text-blue-800',
    'VALIDE_SCOL': 'bg-blue-100 text-blue-800',
    'SOUMIS': 'bg-yellow-100 text-yellow-800',
    'REJETE': 'bg-red-100 text-red-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function getEtudiantNom(inscription: any) {
  const e = inscription.etudiant
  if (typeof e === 'string') return e
  return `${e?.nom || ''} ${e?.prenom || ''}`.trim()
}

onMounted(() => {
  fetchEtudiants()
  fetchInscriptions()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">Étudiants</h1>
        <p class="text-gray-500 mt-1">Gestion des inscriptions et dossiers académiques</p>
      </div>
      <div class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2">
          <Upload class="w-4 h-4" />
          Importer
        </button>
        <button class="px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle inscription
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Total étudiants</div>
        <div class="text-2xl font-bold text-[#1B4F72] mt-1">{{ stats.total.toLocaleString() }}</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Inscriptions 2024-2025</div>
        <div class="text-2xl font-bold text-green-600 mt-1">{{ stats.inscriptions_annee.toLocaleString() }}</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">En attente validation</div>
        <div class="text-2xl font-bold text-yellow-600 mt-1">{{ stats.en_attente }}</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Nouveaux inscrits</div>
        <div class="text-2xl font-bold text-blue-600 mt-1">{{ stats.nouveaux }}</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex space-x-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors',
            activeTab === tab.id
              ? 'border-[#1B4F72] text-[#1B4F72]'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center">
      <Loader2 class="w-8 h-8 animate-spin text-[#1B4F72] mx-auto mb-4" />
      <p class="text-gray-500">Chargement des données...</p>
    </div>

    <!-- Contenu -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100">
      <!-- Inscriptions -->
      <div v-if="activeTab === 'inscriptions'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher une inscription..." 
              class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-[#1B4F72]" 
            />
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Filter class="w-4 h-4" />
              Filtres
            </button>
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Download class="w-4 h-4" />
              Exporter
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Étudiant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">NIP Gabon</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Filière</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Niveau</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Frais</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="inscription in inscriptions" :key="inscription.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4">
                  <div class="font-medium text-gray-900">{{ getEtudiantNom(inscription) }}</div>
                </td>
                <td class="py-3 px-4 text-sm font-mono text-gray-600">{{ inscription.etudiant?.nip_gabon || '-' }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.filiere?.libelle || inscription.filiere_id }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.niveau }}</td>
                <td class="py-3 px-4 text-sm">
                  <span :class="inscription.type_inscription === 'NOUVEAU' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'" class="px-2 py-1 text-xs font-medium rounded">
                    {{ inscription.type_inscription }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatutInscription(inscription.statut_workflow)]">
                    {{ inscription.statut_workflow }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span v-if="inscription.frais_payes" class="text-green-600">✓ Payé</span>
                  <span v-else class="text-red-500">✗ Impayé</span>
                </td>
                <td class="py-3 px-4">
                  <button class="text-[#1B4F72] hover:underline text-sm">Voir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Liste étudiants -->
      <div v-if="activeTab === 'dossiers'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher un étudiant..." 
              class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-[#1B4F72]" 
            />
          </div>
        </div>

        <div v-if="etudiantsFiltres.length === 0" class="text-center py-12">
          <Users class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500">Aucun étudiant trouvé</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="etudiant in etudiantsFiltres" :key="etudiant.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start gap-3 mb-3">
              <div class="w-12 h-12 bg-[#1B4F72]/10 rounded-full flex items-center justify-center">
                <span class="text-[#1B4F72] font-semibold">{{ etudiant.prenom?.[0] || '' }}{{ etudiant.nom?.[0] || '' }}</span>
              </div>
              <div class="flex-1">
                <div class="font-medium text-gray-900">{{ etudiant.prenom }} {{ etudiant.nom }}</div>
                <div class="text-sm text-gray-500 font-mono">{{ etudiant.nip_gabon }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(etudiant.statut)]">
                {{ etudiant.statut }}
              </span>
            </div>
            
            <div class="space-y-2 text-sm">
              <div v-if="etudiant.genre" class="flex items-center gap-2 text-gray-600">
                <GraduationCap class="w-4 h-4 text-gray-400" />
                {{ etudiant.genre }}
              </div>
              <div v-if="etudiant.email" class="flex items-center gap-2 text-gray-600">
                <Mail class="w-4 h-4 text-gray-400" />
                {{ etudiant.email }}
              </div>
              <div v-if="etudiant.telephone" class="flex items-center gap-2 text-gray-600">
                <Phone class="w-4 h-4 text-gray-400" />
                {{ etudiant.telephone }}
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-gray-100 flex gap-2">
              <button class="flex-1 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-center">
                Voir dossier
              </button>
              <button class="flex-1 px-3 py-2 text-sm bg-[#1B4F72]/10 text-[#1B4F72] hover:bg-[#1B4F72]/20 rounded-lg text-center">
                Notes
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Documents -->
      <div v-if="activeTab === 'documents'" class="p-6">
        <div class="text-center py-12">
          <FileText class="w-16 h-16 text-[#1B4F72]/20 mx-auto mb-4" />
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Documents des étudiants</h3>
          <p class="text-gray-500 mb-4">Photos, pièces d'identité, bulletins, diplômes</p>
          <button class="px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90">
            Gérer les documents
          </button>
        </div>
      </div>
    </div>
  </div>
</template>