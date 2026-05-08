<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
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
  ChevronDown,
  ChevronUp,
  Loader2,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertCircle,
  Edit,
  Trash2,
  Eye,
  Download,
  UsersRound,
  BookMarked,
  ClipboardList,
  Award,
  Database,
  Shield,
  Wifi,
  HardDrive,
  Key,
  UserCog,
  LogOut,
  RefreshCw
} from 'lucide-vue-next'
import { fetchWithAuth } from '@/api/auth'

const loading = ref(true)
const filieres = ref<any[]>([])
const salles = ref<any[]>([])
const expandedModule = ref<string | null>(null)

const modules = ref([
  {
    id: 'inscriptions',
    title: 'Inscriptions',
    description: 'Gérer les inscriptions et réinscriptions des étudiants, suivi des dossiers et validation workflow',
    icon: Users,
    color: 'bg-blue-500',
    stats: { total: 210, nouveaux: 45, reinscrits: 165, en_attente: 12 },
    progress: 94,
    quickActions: [
      { label: 'Nouvelle inscription', icon: Plus },
      { label: 'Liste complète', icon: List },
      { label: 'Export PDF', icon: Download },
      { label: 'Relances', icon: AlertCircle }
    ],
    recentActivity: [
      { user: 'Mouanda J.', action: 'Nouvelle inscription', time: '5 min' },
      { user: 'Nguema M.', action: 'Réinscription validée', time: '12 min' },
      { user: 'Obame Y.', action: 'Dossier incomplet', time: '25 min' }
    ]
  },
  {
    id: 'parcours',
    title: 'Parcours Pédagogiques',
    description: 'Configurer les filières, UE, maquettes pédagogiques et plan de formation',
    icon: Layers,
    color: 'bg-green-500',
    stats: { filieres: 7, ue_count: 156, maquettes: 15, credits: 2400 },
    progress: 72,
    quickActions: [
      { label: 'Nouvelle filière', icon: Plus },
      { label: 'Maquettes', icon: ClipboardList },
      { label: 'UE', icon: BookMarked },
      { label: 'Import', icon: Download }
    ],
    recentActivity: [
      { user: 'Pr. Bounda', action: 'Maquette L3 validée', time: '1h' },
      { user: 'Admin', action: 'Nouvelle UE ajoutée', time: '3h' }
    ]
  },
  {
    id: 'emploidutemps',
    title: 'Emploi du Temps',
    description: 'Planifier les cours, gérer les salles et les créneaux horaires',
    icon: Calendar,
    color: 'bg-purple-500',
    stats: { cours_aujourdhui: 24, salles: 12, enseignants: 45, taux_occupation: 78 },
    progress: 85,
    quickActions: [
      { label: 'Générer EDT', icon: RefreshCw },
      { label: 'Nouvelle planification', icon: Plus },
      { label: 'Occupation salles', icon: Building2 },
      { label: 'Export', icon: Download }
    ],
    recentActivity: [
      { user: 'Admin', action: 'EDT Semaine 12 publié', time: '2h' },
      { user: 'Pr. Mba', action: 'Cours annulé', time: '4h' }
    ]
  },
  {
    id: 'notes',
    title: 'Notes & Délibérations',
    description: 'Saisir les notes, calculer les moyennes et générer les PV de jury',
    icon: FileText,
    color: 'bg-orange-500',
    stats: { notes_saisies: 1847, moyenne_classe: 12.4, admissibles: 89, debiteurs: 23 },
    progress: 68,
    quickActions: [
      { label: 'Saisir notes', icon: Edit },
      { label: 'Délibération', icon: Award },
      { label: 'PV Jury', icon: FileText },
      { label: 'Statistiques', icon: TrendingUp }
    ],
    recentActivity: [
      { user: 'Pr. Ondo', action: 'Notes BD saisies', time: '30 min' },
      { user: 'Pr. Nzamba', action: 'Délibération validée', time: '2h' }
    ]
  },
  {
    id: 'diplomes',
    title: 'Diplômes',
    description: 'Émettre, vérifier et gérer les diplômes et attestations',
    icon: GraduationCap,
    color: 'bg-teal-500',
    stats: { diplomes_delivres: 1245, en_cours: 45, verificateurs: 234 },
    progress: 55,
    quickActions: [
      { label: 'Nouveau diplôme', icon: Plus },
      { label: 'Vérification', icon: Shield },
      { label: 'Attestations', icon: FileText },
      { label: 'Statistiques', icon: TrendingUp }
    ],
    recentActivity: [
      { user: 'Admin', action: '25 diplômes émis', time: '1j' },
      { user: 'Système', action: '12 vérifications externes', time: '2j' }
    ]
  },
  {
    id: 'parametres',
    title: 'Paramètres Système',
    description: 'Configuration du système, utilisateurs, rôles et sécurité',
    icon: Settings,
    color: 'bg-gray-500',
    stats: { utilisateurs: 156, roles: 7, connexions: 89, last_backup: '2h' },
    progress: 40,
    quickActions: [
      { label: 'Utilisateurs', icon: UserCog },
      { label: 'Rôles', icon: Key },
      { label: 'Sauvegarde', icon: HardDrive },
      { label: 'Logs', icon: Database }
    ],
    recentActivity: [
      { user: 'Admin', action: 'Backup effectué', time: '2h' },
      { user: 'Admin', action: 'Nouvel utilisateur créé', time: '1j' }
    ]
  }
])

const filieresList = [
  { code: 'IC', libelle: 'Informatique et Communication', etudiants: 30, semestre: 6, ue: 12, status: 'active' },
  { code: 'AEC', libelle: 'Architecture et Éco-construction', etudiants: 28, semestre: 4, ue: 10, status: 'active' },
  { code: 'CI', libelle: 'Chimie Industrielle', etudiants: 25, semestre: 6, ue: 14, status: 'active' },
  { code: 'GTR', libelle: 'Génie Thermique et Énergies Renouvelables', etudiants: 22, semestre: 4, ue: 8, status: 'active' },
  { code: 'PM', libelle: 'Productique Mécanique', etudiants: 18, semestre: 6, ue: 11, status: 'active' },
  { code: 'ABB', libelle: 'Analyses Biologiques et Biochimiques', etudiants: 20, semestre: 4, ue: 9, status: 'active' },
  { code: 'MEB', libelle: 'Maintenance des Équipements Biomédicaux', etudiants: 15, semestre: 4, ue: 8, status: 'active' }
]

const sallesList = [
  { id: 1, nom: 'Amphi A', type: 'Amphithéâtre', capacite: 150, statut: 'disponible', equipements: ['Vidéoprojecteur', 'Micro', 'Climatisation'] },
  { id: 2, nom: 'Amphi B', type: 'Amphithéâtre', capacite: 100, statut: 'disponible', equipements: ['Vidéoprojecteur', 'Climatisation'] },
  { id: 3, nom: 'Salle 101', type: 'Salle TD', capacite: 40, statut: 'disponible', equipements: ['Vidéoprojecteur', 'Tableau blanc'] },
  { id: 4, nom: 'Salle 102', type: 'Salle TD', capacite: 40, statut: 'occupee', equipements: ['Vidéoprojecteur'] },
  { id: 5, nom: 'Salle 201', type: 'Salle CM', capacite: 60, statut: 'disponible', equipements: ['Vidéoprojecteur', 'Tableau interactif'] },
  { id: 6, nom: 'Labo Info', type: 'Laboratoire', capacite: 30, statut: 'disponible', equipements: ['Postes 30', 'Vidéoprojecteur', ' réseau'] },
  { id: 7, nom: 'Labo Chimie', type: 'Laboratoire', capacite: 25, statut: 'maintenance', equipements: ['Paillasses', 'Équipement sécurité'] },
]

const getStatutBadge = (statut: string) => {
  const badges: Record<string, string> = {
    disponible: 'bg-green-100 text-green-800',
    occupee: 'bg-orange-100 text-orange-800',
    maintenance: 'bg-red-100 text-red-800',
    active: 'bg-green-100 text-green-800'
  }
  return badges[statut] || 'bg-gray-100 text-gray-800'
}

function toggleModule(moduleId: string) {
  expandedModule.value = expandedModule.value === moduleId ? null : moduleId
}

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

    <!-- Modules Cards avec détails -->
    <div class="space-y-4">
      <div
        v-for="module in modules"
        :key="module.id"
        class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
      >
        <!-- Header du module -->
        <div 
          class="p-6 cursor-pointer hover:bg-gray-50 transition-colors"
          @click="toggleModule(module.id)"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-start gap-4">
              <div :class="['w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0', module.color]">
                <component :is="module.icon" class="w-7 h-7 text-white" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ module.title }}</h3>
                <p class="text-sm text-gray-500 max-w-2xl">{{ module.description }}</p>
                
                <!-- Stats inline -->
                <div class="flex flex-wrap gap-4 mt-3">
                  <template v-if="module.id === 'inscriptions'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.total }}</span> inscriptions</span>
                    <span class="text-sm"><span class="font-semibold text-green-600">{{ module.stats.nouveaux }}</span> nouveaux</span>
                    <span class="text-sm"><span class="font-semibold text-orange-600">{{ module.stats.en_attente }}</span> en attente</span>
                  </template>
                  <template v-else-if="module.id === 'parcours'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.filieres }}</span> filières</span>
                    <span class="text-sm"><span class="font-semibold text-green-600">{{ module.stats.ue_count }}</span> UE</span>
                    <span class="text-sm"><span class="font-semibold text-purple-600">{{ module.stats.maquettes }}</span> maquettes</span>
                  </template>
                  <template v-else-if="module.id === 'emploidutemps'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.cours_aujourdhui }}</span> cours</span>
                    <span class="text-sm"><span class="font-semibold text-blue-600">{{ module.stats.salles }}</span> salles</span>
                    <span class="text-sm"><span class="font-semibold text-purple-600">{{ module.stats.taux_occupation }}%</span> occupation</span>
                  </template>
                  <template v-else-if="module.id === 'notes'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.notes_saisies }}</span> notes</span>
                    <span class="text-sm"><span class="font-semibold text-green-600">{{ module.stats.moyenne_classe }}/20</span> moyenne</span>
                    <span class="text-sm"><span class="font-semibold text-orange-600">{{ module.stats.debiteurs }}</span> debiteurs</span>
                  </template>
                  <template v-else-if="module.id === 'diplomes'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.diplomes_delivres }}</span> délivrés</span>
                    <span class="text-sm"><span class="font-semibold text-blue-600">{{ module.stats.verificateurs }}</span> vérifications</span>
                  </template>
                  <template v-else-if="module.id === 'parametres'">
                    <span class="text-sm"><span class="font-semibold text-[#1B4F72]">{{ module.stats.utilisateurs }}</span> utilisateurs</span>
                    <span class="text-sm"><span class="font-semibold text-green-600">{{ module.stats.roles }}</span> rôles</span>
                    <span class="text-sm"><span class="font-semibold text-gray-600">Backup: {{ module.stats.last_backup }}</span></span>
                  </template>
                </div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <ChevronUp v-if="expandedModule === module.id" class="w-5 h-5 text-gray-400" />
              <ChevronDown v-else class="w-5 h-5 text-gray-400" />
            </div>
          </div>
          
          <!-- Barre de progression -->
          <div class="mt-4 flex items-center gap-4">
            <div class="flex-1 bg-gray-100 rounded-full h-2">
              <div 
                :class="['h-2 rounded-full transition-all', module.color.replace('bg-', 'bg-')]"
                :style="{ width: module.progress + '%' }"
              ></div>
            </div>
            <span class="text-sm text-gray-500 font-medium">{{ module.progress }}%</span>
          </div>
        </div>

        <!-- Détails étendus -->
        <div v-if="expandedModule === module.id" class="border-t border-gray-100 p-6 bg-gray-50">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Actions rapides -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
                <CheckCircle class="w-4 h-4 text-[#1B4F72]" />
                Actions rapides
              </h4>
              <div class="grid grid-cols-2 gap-2">
                <button 
                  v-for="action in module.quickActions" 
                  :key="action.label"
                  class="flex items-center gap-2 px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-white hover:border-[#1B4F72] hover:text-[#1B4F72] transition-colors"
                >
                  <component :is="action.icon" class="w-4 h-4" />
                  {{ action.label }}
                </button>
              </div>
            </div>

            <!-- Activité récente -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3 flex items-center gap-2">
                <Clock class="w-4 h-4 text-[#1B4F72]" />
                Activité récente
              </h4>
              <div class="space-y-2">
                <div 
                  v-for="(activity, idx) in module.recentActivity" 
                  :key="idx"
                  class="flex items-center justify-between p-3 bg-white rounded-lg border border-gray-100"
                >
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 bg-[#1B4F72]/10 rounded-full flex items-center justify-center">
                      <Users class="w-4 h-4 text-[#1B4F72]" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-900">{{ activity.user }}</p>
                      <p class="text-xs text-gray-500">{{ activity.action }}</p>
                    </div>
                  </div>
                  <span class="text-xs text-gray-400">{{ activity.time }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
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
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Semestres</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">UE</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Étudiants</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
              <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="filiere in filieresList" :key="filiere.code" class="border-b border-gray-100 hover:bg-gray-50">
              <td class="py-3 px-4">
                <span class="font-mono font-bold text-[#1B4F72]">{{ filiere.code }}</span>
              </td>
              <td class="py-3 px-4 font-medium text-gray-900">{{ filiere.libelle }}</td>
              <td class="py-3 px-4 text-sm text-gray-600">{{ filiere.semestre }}</td>
              <td class="py-3 px-4 text-sm text-gray-600">{{ filiere.ue }}</td>
              <td class="py-3 px-4">
                <div class="flex items-center gap-2">
                  <div class="w-16 bg-gray-100 rounded-full h-2">
                    <div class="bg-[#1B4F72] h-2 rounded-full" :style="{ width: (filiere.etudiants / 30 * 100) + '%' }"></div>
                  </div>
                  <span class="text-sm font-medium">{{ filiere.etudiants }}</span>
                </div>
              </td>
              <td class="py-3 px-4">
                <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatutBadge(filiere.status)]">
                  {{ filiere.status === 'active' ? 'Active' : filiere.status }}
                </span>
              </td>
              <td class="py-3 px-4">
                <div class="flex gap-2">
                  <button class="text-blue-600 hover:text-blue-800" title="Voir">
                    <Eye class="w-4 h-4" />
                  </button>
                  <button class="text-gray-600 hover:text-gray-800" title="Modifier">
                    <Edit class="w-4 h-4" />
                  </button>
                </div>
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

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        <div 
          v-for="salle in sallesList" 
          :key="salle.id" 
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start justify-between mb-3">
            <div>
              <h4 class="font-semibold text-gray-900">{{ salle.nom }}</h4>
              <p class="text-xs text-gray-500">{{ salle.type }}</p>
            </div>
            <span :class="['px-2 py-1 text-xs font-medium rounded-full', getStatutBadge(salle.statut)]">
              {{ salle.statut === 'disponible' ? 'Disponible' : salle.statut === 'occupee' ? 'Occupée' : 'Maintenance' }}
            </span>
          </div>
          
          <div class="space-y-2 text-sm">
            <div class="flex justify-between">
              <span class="text-gray-500">Capacité:</span>
              <span class="font-medium">{{ salle.capacite }} places</span>
            </div>
            <div>
              <span class="text-gray-500">Équipements:</span>
              <div class="flex flex-wrap gap-1 mt-1">
                <span 
                  v-for="eq in salle.equipements" 
                  :key="eq"
                  class="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded"
                >
                  {{ eq }}
                </span>
              </div>
            </div>
          </div>

          <div class="flex gap-2 mt-3 pt-3 border-t border-gray-100">
            <button class="flex-1 px-3 py-1.5 text-xs border border-gray-200 rounded hover:bg-gray-50">
              <Eye class="w-3 h-3 inline mr-1" />
              Détails
            </button>
            <button class="flex-1 px-3 py-1.5 text-xs bg-[#1B4F72]/10 text-[#1B4F72] rounded hover:bg-[#1B4F72]/20">
              <Calendar class="w-3 h-3 inline mr-1" />
              Horaires
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Statistiques globales -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div class="bg-gradient-to-br from-[#1B4F72] to-[#154360] rounded-xl p-5 text-white">
        <UsersRound class="w-8 h-8 mb-2 opacity-80" />
        <div class="text-2xl font-bold">1,247</div>
        <div class="text-sm opacity-80">Étudiants actifs</div>
      </div>
      <div class="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-5 text-white">
        <BookOpen class="w-8 h-8 mb-2 opacity-80" />
        <div class="text-2xl font-bold">7</div>
        <div class="text-sm opacity-80">Filières</div>
      </div>
      <div class="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-5 text-white">
        <GraduationCap class="w-8 h-8 mb-2 opacity-80" />
        <div class="text-2xl font-bold">156</div>
        <div class="text-sm opacity-80">Unités d'enseignement</div>
      </div>
      <div class="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-5 text-white">
        <Award class="w-8 h-8 mb-2 opacity-80" />
        <div class="text-2xl font-bold">89%</div>
        <div class="text-sm opacity-80">Taux de réussite</div>
      </div>
    </div>
  </div>
</template>
