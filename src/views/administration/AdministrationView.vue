<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { 
  Building2, 
  Users, 
  BookOpen, 
  Calendar,
  FileText,
  GraduationCap,
  Layers,
  Settings,
  Plus,
  Search,
  ChevronRight,
  Loader2
} from 'lucide-vue-next'
import { fetchWithAuth } from '@/api/auth'

const loading = ref(true)
const filieres = ref<any[]>([])
const salles = ref<any[]>([])

const modules = [
  {
    title: 'Inscriptions',
    description: 'Gérer les inscriptions et réinscriptions des étudiants',
    icon: Users,
    stats: '210 inscriptions',
    color: 'bg-blue-500'
  },
  {
    title: 'Parcours pédagogiques',
    description: 'Configurer les filières, UE et maquettes pédagogiques',
    icon: Layers,
    stats: '7 filières actives',
    color: 'bg-green-500'
  },
  {
    title: 'Emploi du temps',
    description: 'Planifier les cours et gérer les salles',
    icon: Calendar,
    stats: '7 salles',
    color: 'bg-purple-500'
  },
  {
    title: 'Notes & Délibérations',
    description: 'Saisir les notes et générer les PV de jury',
    icon: FileText,
    stats: '180 notes',
    color: 'bg-orange-500'
  },
  {
    title: 'Diplômes',
    description: 'Émettre et vérifier les diplômes',
    icon: GraduationCap,
    stats: '',
    color: 'bg-teal-500'
  },
  {
    title: 'Paramètres',
    description: 'Configuration du système',
    icon: Settings,
    stats: '',
    color: 'bg-gray-500'
  },
]

const filieresList = [
  { code: 'IC', libelle: 'Informatique et Communication', etudiants: 30 },
  { code: 'AEC', libelle: 'Architecture et Éco-construction', etudiants: 30 },
  { code: 'CI', libelle: 'Chimie Industrielle', etudiants: 30 },
  { code: 'GTR', libelle: 'Génie Thermique et Énergies Renouvelables', etudiants: 30 },
  { code: 'PM', libelle: 'Productique Mécanique', etudiants: 30 },
  { code: 'ABB', libelle: 'Analyses Biologiques et Biochimiques', etudiants: 30 },
  { code: 'MEB', libelle: 'Maintenance des Équipements Biomédicaux', etudiants: 30 },
]

async function fetchData() {
  try {
    loading.value = true
    const token = localStorage.getItem('auth_token')
    if (!token) return

    const respFilieres = await fetchWithAuth('http://127.0.0.1:8765/api/v1/administration/filieres')
    if (respFilieres.ok) {
      filieres.value = await respFilieres.json()
    }

    const respSalles = await fetchWithAuth('http://127.0.0.1:8765/api/v1/administration/salles')
    if (respSalles.ok) {
      salles.value = await respSalles.json()
    }
  } catch (e) {
    console.error('Failed to fetch data:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-heading font-bold text-gray-900">Administration</h1>
      <p class="text-gray-500 mt-1">Gestion académique et administrative du CUK</p>
    </div>

    <!-- Modules Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="module in modules"
        :key="module.title"
        class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-[#1B4F72] transition-all group cursor-pointer"
      >
        <div class="flex items-start justify-between mb-4">
          <div :class="['w-12 h-12 rounded-lg flex items-center justify-center', module.color]">
            <component :is="module.icon" class="w-6 h-6 text-white" />
          </div>
          <ChevronRight class="w-5 h-5 text-gray-400 group-hover:text-[#1B4F72] transition-colors" />
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ module.title }}</h3>
        <p class="text-sm text-gray-500 mb-3">{{ module.description }}</p>
        <p v-if="module.stats" class="text-xs font-medium text-[#1B4F72]">
          {{ module.stats }}
        </p>
      </div>
    </div>

    <!-- Filières Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-heading font-semibold text-gray-900">Filières actives</h2>
        <button class="px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle filière
        </button>
      </div>

      <div v-if="loading" class="text-center py-8">
        <Loader2 class="w-8 h-8 animate-spin text-[#1B4F72] mx-auto mb-4" />
        <p class="text-gray-500">Chargement des filières...</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="w-full">
          <thead>
            <tr class="border-b border-gray-200">
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Code</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Libellé</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Domaine</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Niveau</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="filiere in filieresList" :key="filiere.code" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4">
                <span class="font-mono font-semibold text-[#1B4F72]">{{ filiere.code }}</span>
              </td>
              <td class="py-3 px-4 font-medium text-gray-900">{{ filiere.libelle }}</td>
              <td class="py-3 px-4 text-sm text-gray-600">-</td>
              <td class="py-3 px-4">
                <span class="px-2 py-1 text-xs font-medium bg-purple-100 text-purple-800 rounded">
                  {{ filiere.etudiants }} étudiants
                </span>
              </td>
              <td class="py-3 px-4">
                <button class="text-sm text-[#1B4F72] hover:underline">Voir</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Salles Section -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div class="flex items-center justify-between mb-6">
        <h2 class="text-lg font-heading font-semibold text-gray-900">Salles disponibles</h2>
        <button class="px-4 py-2 bg-[#1B4F72] text-white rounded-lg text-sm font-medium hover:bg-[#1B4F72]/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle salle
        </button>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="i in 7" :key="i" class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
          <div class="flex items-center justify-between mb-2">
            <span class="font-medium text-gray-900">Salle {{ i }}</span>
            <span class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded">
              Disponible
            </span>
          </div>
          <div class="text-sm text-gray-500">
            Capacité: {{ [25, 40, 100, 150][i % 4] }} places
          </div>
        </div>
      </div>
    </div>
  </div>
</template>