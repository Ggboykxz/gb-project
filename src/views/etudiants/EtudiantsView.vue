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
  FileCheck,
  Eye,
  Edit,
  Trash2,
  ChevronRight,
  Calendar,
  Clock,
  CheckCircle,
  XCircle,
  TrendingUp,
  IdCard,
  Award,
  BookOpen,
  MapPin,
  DollarSign,
  AlertTriangle,
  Wifi,
  WifiOff,
  X
} from 'lucide-vue-next'
import { fetchWithAuth } from '@/api/auth'

const searchQuery = ref('')
const activeTab = ref('inscriptions')
const loading = ref(false)
const showModal = ref(false)
const selectedEtudiant = ref<any>(null)
const etudiants = ref<any[]>([])
const inscriptions = ref<any[]>([])

const tabs = [
  { id: 'inscriptions', label: 'Inscriptions', icon: UserPlus, count: 342 },
  { id: 'dossiers', label: 'Dossiers académiques', icon: FileText, count: 1247 },
  { id: 'documents', label: 'Documents', icon: FileCheck, count: 0 },
]

const stats = ref({
  total: 1247,
  inscriptions_annee: 342,
  en_attente: 45,
  nouveaux: 89,
  confirmes: 297,
  debiteurs: 23
})

const etudiantsList = ref([
  { id: '1', nom: 'Ondo', prenom: 'Jean-Marie', nip_gabon: 'NKL123456', email: 'ondo.jm@cuk.ga', telephone: '+241074123456', filiere: 'Informatique', niveau: 'L3', statut: 'ACTIF', moyenne: 14.5, absences: 2, genre: 'M' },
  { id: '2', nom: 'Nguema', prenom: 'Marie-Claire', nip_gabon: 'NKL234567', email: 'nguema.mc@cuk.ga', telephone: '+241074234567', filiere: 'Droit', niveau: 'L2', statut: 'ACTIF', moyenne: 15.2, absences: 0, genre: 'F' },
  { id: '3', nom: 'Mba', prenom: 'Paul', nip_gabon: 'NKL345678', email: 'mba.p@cuk.ga', telephone: '+241074345678', filiere: 'Sciences Eco', niveau: 'M1', statut: 'ACTIF', moyenne: 12.8, absences: 5, genre: 'M' },
  { id: '4', nom: 'Obame', prenom: 'Espoir', nip_gabon: 'NKL456789', email: 'obame.e@cuk.ga', telephone: '+241074456789', filiere: 'Chimie', niveau: 'L1', statut: 'SUSPENDU', moyenne: 8.5, absences: 15, genre: 'M' },
  { id: '5', nom: 'Mouanda', prenom: 'Sandrine', nip_gabon: 'NKL567890', email: 'mouanda.s@cuk.ga', telephone: '+241074567890', filiere: 'Info Bio', niveau: 'L3', statut: 'ACTIF', moyenne: 16.0, absences: 1, genre: 'F' },
])

const inscriptionsList = ref([
  { id: '1', etudiant: 'Nkoghe Junior', nip: 'NKL111111', filiere: 'Informatique', niveau: 'L3', type: 'NOUVEAU', statut: 'CONFIRME', frais: true, date: '2024-09-15' },
  { id: '2', etudiant: 'Obame Yannick', nip: 'NKL222222', filiere: 'Droit', niveau: 'L2', type: 'REINSCRIPTION', statut: 'VALIDE_SCOL', frais: true, date: '2024-09-18' },
  { id: '3', etudiant: 'Mouanda Christelle', nip: 'NKL333333', filiere: 'Sciences Eco', niveau: 'M1', type: 'NOUVEAU', statut: 'SOUMIS', frais: false, date: '2024-09-20' },
  { id: '4', etudiant: 'Bounda Eric', nip: 'NKL444444', filiere: 'Chimie', niveau: 'L1', type: 'NOUVEAU', statut: 'VALIDE_DOyEN', frais: true, date: '2024-09-22' },
  { id: '5', etudiant: 'Nguema Alain', nip: 'NKL555555', filiere: 'Info Bio', niveau: 'L3', type: 'REINSCRIPTION', statut: 'CONFIRME', frais: true, date: '2024-09-25' },
])

const etudiantsFiltres = computed(() => {
  if (!searchQuery.value) return etudiantsList.value
  const query = searchQuery.value.toLowerCase()
  return etudiantsList.value.filter(e =>
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

function getInitials(nom: string, prenom: string) {
  return `${prenom?.[0] || ''}${nom?.[0] || ''}`
}

function openEtudiantDetail(etudiant: any) {
  selectedEtudiant.value = etudiant
  showModal.value = true
}

function getMoyenneColor(moyenne: number) {
  if (moyenne >= 14) return 'text-green-600 bg-green-100'
  if (moyenne >= 10) return 'text-yellow-600 bg-yellow-100'
  return 'text-red-600 bg-red-100'
}

onMounted(() => {
  fetchEtudiants()
  fetchInscriptions()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">Étudiants</h1>
        <p class="text-gray-500 mt-1">Gestion des inscriptions et dossiers académiques</p>
      </div>
      <div class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2">
          <Upload class="w-4 h-4" />
          Importer CSV
        </button>
        <button class="px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle inscription
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
      <div class="bg-gradient-to-br from-[#1B4F72] to-[#154360] rounded-xl p-4 text-white">
        <div class="text-sm opacity-80">Total</div>
        <div class="text-2xl font-bold">{{ stats.total }}</div>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center gap-2 text-green-600 text-sm font-medium">
          <CheckCircle class="w-4 h-4" />
          Confirmés
        </div>
        <div class="text-2xl font-bold text-gray-900 mt-1">{{ stats.confirmes }}</div>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center gap-2 text-yellow-600 text-sm font-medium">
          <Clock class="w-4 h-4" />
          En attente
        </div>
        <div class="text-2xl font-bold text-gray-900 mt-1">{{ stats.en_attente }}</div>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center gap-2 text-blue-600 text-sm font-medium">
          <UserPlus class="w-4 h-4" />
          Nouveaux
        </div>
        <div class="text-2xl font-bold text-gray-900 mt-1">{{ stats.nouveaux }}</div>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center gap-2 text-red-600 text-sm font-medium">
          <AlertTriangle class="w-4 h-4" />
          Débiteurs
        </div>
        <div class="text-2xl font-bold text-gray-900 mt-1">{{ stats.debiteurs }}</div>
      </div>
      <div class="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
        <div class="flex items-center gap-2 text-purple-600 text-sm font-medium">
          <Award class="w-4 h-4" />
          Taux réussite
        </div>
        <div class="text-2xl font-bold text-gray-900 mt-1">89%</div>
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
          <span v-if="tab.count" class="px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full text-xs">
            {{ tab.count }}
          </span>
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
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
          <div class="relative flex-1 max-w-md">
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
              <tr v-for="inscription in inscriptionsList" :key="inscription.id" class="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                <td class="py-3 px-4">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-[#1B4F72]/10 rounded-full flex items-center justify-center">
                      <span class="text-[#1B4F72] font-semibold text-xs">{{ inscription.etudiant.split(' ').map((n: string) => n[0]).join('') }}</span>
                    </div>
                    <div class="font-medium text-gray-900">{{ inscription.etudiant }}</div>
                  </div>
                </td>
                <td class="py-3 px-4 text-sm font-mono text-gray-600">{{ inscription.nip }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.filiere }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.niveau }}</td>
                <td class="py-3 px-4 text-sm">
                  <span :class="inscription.type === 'NOUVEAU' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'" class="px-2 py-1 text-xs font-medium rounded">
                    {{ inscription.type }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatutInscription(inscription.statut)]">
                    {{ inscription.statut }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <div class="flex items-center gap-2">
                    <CheckCircle v-if="inscription.frais" class="w-4 h-4 text-green-600" />
                    <XCircle v-else class="w-4 h-4 text-red-500" />
                    <span :class="inscription.frais ? 'text-green-600' : 'text-red-500'" class="text-sm">
                      {{ inscription.frais ? 'Payé' : 'Impayé' }}
                    </span>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <div class="flex gap-2">
                    <button class="p-1 hover:bg-gray-100 rounded" title="Voir">
                      <Eye class="w-4 h-4 text-gray-600" />
                    </button>
                    <button class="p-1 hover:bg-gray-100 rounded" title="Modifier">
                      <Edit class="w-4 h-4 text-gray-600" />
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Liste étudiants -->
      <div v-if="activeTab === 'dossiers'" class="p-6">
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
          <div class="relative flex-1 max-w-md">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Rechercher un étudiant..."
              class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-[#1B4F72]"
            />
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Filter class="w-4 h-4" />
              Filtres
            </button>
          </div>
        </div>

        <div v-if="etudiantsFiltres.length === 0" class="text-center py-12">
          <Users class="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <p class="text-gray-500">Aucun étudiant trouvé</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="etudiant in etudiantsFiltres" :key="etudiant.id"
               class="border border-gray-200 rounded-xl p-5 hover:shadow-lg hover:border-[#1B4F72]/30 transition-all cursor-pointer group"
               @click="openEtudiantDetail(etudiant)">
            <div class="flex items-start gap-4 mb-4">
              <div class="w-14 h-14 bg-[#1B4F72] rounded-xl flex items-center justify-center">
                <span class="text-white font-bold text-lg">{{ getInitials(etudiant.nom, etudiant.prenom) }}</span>
              </div>
              <div class="flex-1">
                <div class="font-semibold text-gray-900 text-lg">{{ etudiant.prenom }} {{ etudiant.nom }}</div>
                <div class="text-sm text-gray-500 font-mono">{{ etudiant.nip_gabon }}</div>
                <span :class="['px-2 py-1 text-xs font-medium rounded-full mt-2 inline-block', formatStatut(etudiant.statut)]">
                  {{ etudiant.statut }}
                </span>
              </div>
            </div>

            <div class="space-y-2 text-sm">
              <div class="flex items-center gap-2 text-gray-600">
                <BookOpen class="w-4 h-4 text-gray-400" />
                {{ etudiant.filiere }} - {{ etudiant.niveau }}
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <Mail class="w-4 h-4 text-gray-400" />
                {{ etudiant.email }}
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <Phone class="w-4 h-4 text-gray-400" />
                {{ etudiant.telephone }}
              </div>
            </div>

            <div class="grid grid-cols-2 gap-3 mt-4 pt-4 border-t border-gray-100">
              <div class="text-center">
                <div :class="['text-lg font-bold', getMoyenneColor(etudiant.moyenne)]">
                  {{ etudiant.moyenne }}/20
                </div>
                <div class="text-xs text-gray-500">Moyenne</div>
              </div>
              <div class="text-center">
                <div :class="[
                  'text-lg font-bold',
                  etudiant.absences < 5 ? 'text-green-600' : etudiant.absences < 10 ? 'text-yellow-600' : 'text-red-600'
                ]">
                  {{ etudiant.absences }}
                </div>
                <div class="text-xs text-gray-500">Absences</div>
              </div>
            </div>

            <div class="mt-4 flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button class="flex-1 px-3 py-2 text-sm bg-[#1B4F72]/10 text-[#1B4F72] hover:bg-[#1B4F72]/20 rounded-lg text-center flex items-center justify-center gap-1">
                <Eye class="w-4 h-4" />
                Voir
              </button>
              <button class="flex-1 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-center flex items-center justify-center gap-1">
                <FileText class="w-4 h-4" />
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

    <!-- Modal Detail -->
    <Teleport to="body">
      <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="fixed inset-0 bg-black/50" @click="showModal = false"></div>
        <div class="relative bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
          <div class="p-6 border-b border-gray-100 flex items-center justify-between">
            <h3 class="text-lg font-semibold">Détails de l'étudiant</h3>
            <button @click="showModal = false" class="p-2 hover:bg-gray-100 rounded-lg">
              <X class="w-5 h-5" />
            </button>
          </div>
          <div v-if="selectedEtudiant" class="p-6">
            <div class="flex items-start gap-4 mb-6">
              <div class="w-20 h-20 bg-[#1B4F72] rounded-xl flex items-center justify-center">
                <span class="text-white font-bold text-2xl">{{ getInitials(selectedEtudiant.nom, selectedEtudiant.prenom) }}</span>
              </div>
              <div>
                <h2 class="text-xl font-bold text-gray-900">{{ selectedEtudiant.prenom }} {{ selectedEtudiant.nom }}</h2>
                <p class="text-gray-500">{{ selectedEtudiant.filiere }} - {{ selectedEtudiant.niveau }}</p>
                <span :class="['px-2 py-1 text-xs font-medium rounded-full mt-2 inline-block', formatStatut(selectedEtudiant.statut)]">
                  {{ selectedEtudiant.statut }}
                </span>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4 mb-6">
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="text-sm text-gray-500">NIP Gabon</div>
                <div class="font-mono font-semibold text-gray-900">{{ selectedEtudiant.nip_gabon }}</div>
              </div>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="text-sm text-gray-500">Moyenne</div>
                <div :class="['font-bold text-xl', getMoyenneColor(selectedEtudiant.moyenne)]">
                  {{ selectedEtudiant.moyenne }}/20
                </div>
              </div>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="text-sm text-gray-500">Email</div>
                <div class="font-medium text-gray-900">{{ selectedEtudiant.email }}</div>
              </div>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="text-sm text-gray-500">Téléphone</div>
                <div class="font-medium text-gray-900">{{ selectedEtudiant.telephone }}</div>
              </div>
            </div>
          </div>
          <div class="p-6 border-t border-gray-100 flex gap-3">
            <button class="flex-1 px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90">
              Modifier
            </button>
            <button class="px-4 py-2 border border-gray-200 rounded-lg text-sm font-medium hover:bg-gray-50">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
