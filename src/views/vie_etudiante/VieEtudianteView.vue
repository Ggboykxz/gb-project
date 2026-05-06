<script setup lang="ts">
import { ref } from 'vue'
import { 
  Briefcase, 
  GraduationCap, 
  Award, 
  Users, 
  Search,
  FileText,
  Building2,
  TrendingUp,
  AlertCircle,
  Download
} from 'lucide-vue-next'

const activeTab = ref('portfolio')

const tabs = [
  { id: 'portfolio', label: 'Portfolio', icon: FileText },
  { id: 'bourses', label: 'Bourses & Aides', icon: Award },
  { id: 'stages', label: 'Stages & Emploi', icon: Briefcase },
  { id: 'alumni', label: 'Alumni', icon: Users },
  { id: 'orientation', label: 'Orientation', icon: TrendingUp },
]

const modules = [
  {
    id: 'portfolio',
    title: 'Portfolio Numérique',
    description: 'Créez et gérez votre portfolio professionnel, générez votre CV automatiquement',
    icon: FileText,
    stats: [
      { label: 'Profils actifs', value: '245' },
      { label: 'CV générés', value: '189' },
      { label: 'Partages externes', value: '42' },
    ]
  },
  {
    id: 'bourses',
    title: 'Bourses & Aides Sociales',
    description: 'Gérez les demandes de bourses, seguimiento des attributions et statistiques',
    icon: Award,
    stats: [
      { label: 'Dossiers en attente', value: '18' },
      { label: 'Boursiers actifs', value: '892' },
      { label: 'Budget alloué', value: '45.2M' },
    ]
  },
  {
    id: 'stages',
    title: 'Stages & Emploi',
    description: 'Publiez des offres, gérez les candidatures etSuivez l\'insertion professionnelle',
    icon: Briefcase,
    stats: [
      { label: 'Offres actives', value: '34' },
      { label: 'Candidatures', value: '127' },
      { label: 'Taux placement', value: '78%' },
    ]
  },
  {
    id: 'alumni',
    title: 'Réseau Alumni',
    description: 'Annuaire des anciens, système de mentorat et offres d\'emploi',
    icon: Users,
    stats: [
      { label: 'Diplômés', value: '2,450' },
      { label: 'Mentors actifs', value: '156' },
      { label: 'Offres alumni', value: '23' },
    ]
  },
  {
    id: 'orientation',
    title: 'Orientation & Suivi',
    description: 'Détection de décrochage, plans de réussite et accompagnement personnalisé',
    icon: TrendingUp,
    stats: [
      { label: 'Alertes actives', value: '12' },
      { label: 'Étudiants suivis', value: '89' },
      { label: 'Plans actifs', value: '34' },
    ]
  },
]

const selectedModule = ref(modules[0])

function selectModule(moduleId: string) {
  activeTab.value = moduleId
  selectedModule.value = modules.find(m => m.id === moduleId) || modules[0]
}

const dossiersBourse = ref([
  { id: 1, etudiant: 'Mouanda Marie', type: 'Excellence', montant: 150000, statut: 'En attente', date: '2024-01-15' },
  { id: 2, etudiant: 'Nkoghe Junior', type: 'Sociale', montant: 80000, statut: 'Approuvé', date: '2024-01-10' },
  { id: 3, etudiant: 'Mboghe Christelle', type: 'Excellence', montant: 150000, statut: 'En cours', date: '2024-01-12' },
])

const offreStages = ref([
  { id: 1, titre: 'Développeur Web', entreprise: 'Gabon Telecom', localisation: 'Libreville', type: 'Stage', date_limite: '2024-02-01' },
  { id: 2, titre: 'Assistant Marketing', entreprise: 'Shell Gabon', localisation: 'Port-Gentil', type: 'CDD', date_limite: '2024-01-25' },
  { id: 3, titre: 'Analyste Financier', entreprise: 'BGFI Bank', localisation: 'Libreville', type: 'Stage', date_limite: '2024-02-15' },
])

const alertesDecrochage = ref([
  { id: 1, etudiant: 'Obame Yannick', niveau: 'L2 Info', motif: 'Absences > 30%', priorite: 'Haute' },
  { id: 2, etudiant: 'Mouanda Espoir', niveau: 'L3 Droit', motif: 'Moyenne < 8', priorite: 'Critique' },
])

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'En attente': 'bg-yellow-100 text-yellow-800',
    'Approuvé': 'bg-green-100 text-green-800',
    'En cours': 'bg-blue-100 text-blue-800',
    'Rejeté': 'bg-red-100 text-red-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function formatPriorite(priorite: string) {
  const colors: Record<string, string> = {
    'Haute': 'bg-orange-100 text-orange-800',
    'Critique': 'bg-red-100 text-red-800',
    'Normale': 'bg-blue-100 text-blue-800',
  }
  return colors[priorite] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-2xl font-heading font-bold text-gray-900">Vie Étudiante</h1>
      <p class="text-gray-500 mt-1">Services, accompagnement et insertion professionnelle</p>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div v-for="stat in selectedModule.stats" :key="stat.label" 
           class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">{{ stat.label }}</div>
        <div class="text-2xl font-bold text-primary mt-1">{{ stat.value }}</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex space-x-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="selectModule(tab.id)"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors',
            activeTab === tab.id
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Contenu par onglet -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100">
      <!-- Portfolio -->
      <div v-if="activeTab === 'portfolio'" class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">Portfolio Numérique</h2>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <FileText class="w-4 h-4" />
            Nouveau Portfolio
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                <FileText class="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">Portfolio académique</div>
                <div class="text-xs text-gray-500">Modifié hier</div>
              </div>
            </div>
            <div class="text-sm text-gray-600 mb-3">
              Compétences: Python, Vue.js, SQL, Gestion de projet
            </div>
            <div class="flex gap-2">
              <button class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded">Modifier</button>
              <button class="px-3 py-1.5 text-xs bg-primary/10 text-primary hover:bg-primary/20 rounded">Générer CV</button>
            </div>
          </div>

          <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
                <Award class="w-5 h-5 text-green-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">Certifications</div>
                <div class="text-xs text-gray-500">5 certifications</div>
              </div>
            </div>
            <div class="text-sm text-gray-600 mb-3">
              AWS Cloud Practitioner, Google Analytics, CCNA
            </div>
            <div class="flex gap-2">
              <button class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded">Voir</button>
            </div>
          </div>

          <div class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer">
            <div class="flex items-center gap-3 mb-3">
              <div class="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
                <Briefcase class="w-5 h-5 text-purple-600" />
              </div>
              <div>
                <div class="font-medium text-gray-900">Expériences</div>
                <div class="text-xs text-gray-500">3 expériences</div>
              </div>
            </div>
            <div class="text-sm text-gray-600 mb-3">
              Stage CUK, Projet Fin Year, Bénévolat
            </div>
            <div class="flex gap-2">
              <button class="px-3 py-1.5 text-xs bg-gray-100 hover:bg-gray-200 rounded">Ajouter</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Bourses -->
      <div v-if="activeTab === 'bourses'" class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">Gestion des Bourses</h2>
          <div class="flex gap-3">
            <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 flex items-center gap-2">
              <Download class="w-4 h-4" />
              Exporter
            </button>
            <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
              <Award class="w-4 h-4" />
              Nouveau dossier
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Étudiant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Montant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Date</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="dossier in dossiersBourse" :key="dossier.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 text-sm text-gray-900">{{ dossier.etudiant }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ dossier.type }}</td>
                <td class="py-3 px-4 text-sm font-medium text-gray-900">{{ dossier.montant.toLocaleString() }} FCA</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(dossier.statut)]">
                    {{ dossier.statut }}
                  </span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-500">{{ dossier.date }}</td>
                <td class="py-3 px-4">
                  <button class="text-primary hover:underline text-sm">Voir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Stages & Emploi -->
      <div v-if="activeTab === 'stages'" class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">Offres de Stages & Emploi</h2>
          <div class="flex gap-3">
            <div class="relative">
              <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input type="text" placeholder="Rechercher..." 
                     class="pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
            </div>
            <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
              <Briefcase class="w-4 h-4" />
              Nouvelle offre
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="offre in offreStages" :key="offre.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">{{ offre.titre }}</h3>
                <div class="flex items-center gap-2 text-sm text-gray-500 mt-1">
                  <Building2 class="w-4 h-4" />
                  {{ offre.entreprise }}
                </div>
              </div>
              <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                {{ offre.type }}
              </span>
            </div>
            <div class="flex items-center justify-between mt-4">
              <div class="text-sm text-gray-500">
                <span>{{ offre.localisation }}</span>
                <span class="mx-2">•</span>
                <span>Deadline: {{ offre.date_limite }}</span>
              </div>
              <button class="px-3 py-1.5 text-sm bg-primary text-white rounded hover:bg-primary/90">
                Postuler
              </button>
            </div>
          </div>
        </div>

        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-3">
            <TrendingUp class="w-5 h-5 text-green-600" />
            <div>
              <div class="text-sm font-medium text-gray-900">Taux d'insertion professionnelle</div>
              <div class="text-sm text-gray-500">78% des diplômés trouvent un emploi dans les 6 mois</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Alumni -->
      <div v-if="activeTab === 'alumni'" class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">Réseau Alumni</h2>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Users class="w-4 h-4" />
            Rejoindre le réseau
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div class="bg-gradient-to-br from-primary to-primary/80 rounded-lg p-4 text-white">
            <div class="text-sm opacity-80">Total diplômés</div>
            <div class="text-3xl font-bold mt-1">2,450</div>
          </div>
          <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-80">Mentors actifs</div>
            <div class="text-3xl font-bold mt-1">156</div>
          </div>
          <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg p-4 text-white">
            <div class="text-sm opacity-80">Offres alumni</div>
            <div class="text-3xl font-bold mt-1">23</div>
          </div>
        </div>

        <h3 class="font-medium text-gray-900 mb-4">Annuaire des anciens (extrait)</h3>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
            <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-medium">OM</div>
            <div class="flex-1">
              <div class="font-medium text-gray-900">Ondo M. - Promo 2020</div>
              <div class="text-sm text-gray-500">Développeur @ BGFI Bank</div>
            </div>
            <span class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">Mentor</span>
          </div>
          <div class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
            <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-medium">NA</div>
            <div class="flex-1">
              <div class="font-medium text-gray-900">Nguema A. - Promo 2019</div>
              <div class="text-sm text-gray-500">Chef de projet @ Shell Gabon</div>
            </div>
          </div>
          <div class="flex items-center gap-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50">
            <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 font-medium">MB</div>
            <div class="flex-1">
              <div class="font-medium text-gray-900">Mouamba B. - Promo 2021</div>
              <div class="text-sm text-gray-500">Analyste @ Gabon Telecom</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Orientation -->
      <div v-if="activeTab === 'orientation'" class="p-6">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-lg font-semibold text-gray-900">Orientation & Suivi Pédagogique</h2>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <TrendingUp class="w-4 h-4" />
            Nouveau plan
          </button>
        </div>

        <!-- Alertes décrochage -->
        <div class="mb-6">
          <h3 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
            <AlertCircle class="w-5 h-5 text-red-500" />
            Alertes de décrochage
          </h3>
          <div class="space-y-2">
            <div v-for="alerte in alertesDecrochage" :key="alerte.id" 
                 class="flex items-center justify-between p-3 bg-red-50 border border-red-200 rounded-lg">
              <div>
                <div class="font-medium text-gray-900">{{ alerte.etudiant }}</div>
                <div class="text-sm text-gray-500">{{ alerte.niveau }} - {{ alerte.motif }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatPriorite(alerte.priorite)]">
                {{ alerte.priorite }}
              </span>
            </div>
          </div>
        </div>

        <!-- Plans de réussite -->
        <div>
          <h3 class="font-medium text-gray-900 mb-3">Plans de réussite actifs</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-gray-900">Plan L2 Informatique</span>
                <span class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded">En cours</span>
              </div>
              <div class="text-sm text-gray-500 mb-3">3 objectifs sur 5 atteints</div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-green-500 h-2 rounded-full" style="width: 60%"></div>
              </div>
            </div>
            <div class="border border-gray-200 rounded-lg p-4">
              <div class="flex items-center justify-between mb-2">
                <span class="font-medium text-gray-900">Plan L3 Droit</span>
                <span class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded">En cours</span>
              </div>
              <div class="text-sm text-gray-500 mb-3">1 objectif sur 4 atteint</div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div class="bg-blue-500 h-2 rounded-full" style="width: 25%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>