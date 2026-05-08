<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  Users,
  BookOpen,
  GraduationCap,
  TrendingUp,
  AlertTriangle,
  Calendar,
  FileText,
  DollarSign,
  CheckCircle,
  Loader2,
  RefreshCw,
  Plus,
  Eye,
  Download,
  ArrowUpRight,
  ArrowDownRight,
  Clock,
  TrendingDown,
  Award,
  UsersRound,
  Wallet,
  Receipt,
  CreditCard,
  Banknote,
  Building2,
  FlaskConical,
  BookMarked,
  ClipboardList,
  Wifi,
  WifiOff,
  Server,
  Activity
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { fetchWithAuth } from '@/api/auth'
import { useSyncStore } from '@/stores/sync'

const authStore = useAuthStore()
const syncStore = useSyncStore()

const loading = ref(true)
const error = ref('')
const currentTime = ref(new Date())
const activeTab = ref('overview')

const stats = ref({
  etudiants: 1247,
  filieres: 7,
  inscriptions: 342,
  paiements: 156,
  nouveaux: 45,
  debiteurs: 23,
  cours_aujourdhui: 24,
  taux_reussite: 89
})

const weeklyData = ref([
  { day: 'Lun', inscriptions: 12, paiements: 8 },
  { day: 'Mar', inscriptions: 18, paiements: 15 },
  { day: 'Mer', inscriptions: 8, paiements: 22 },
  { day: 'Jeu', inscriptions: 25, paiements: 12 },
  { day: 'Ven', inscriptions: 15, paiements: 19 },
  { day: 'Sam', inscriptions: 5, paiements: 3 },
  { day: 'Dim', inscriptions: 0, paiements: 0 }
])

const kpis = computed(() => [
  {
    title: 'Étudiants actifs',
    value: stats.value.etudiants.toLocaleString('fr-FR'),
    change: '+12%',
    trend: 'up',
    icon: UsersRound,
    color: 'from-blue-500 to-blue-600',
    subtitle: '1247 → 1396 prevu'
  },
  {
    title: 'Nouvelles inscriptions',
    value: stats.value.nouveaux.toString(),
    change: '+8%',
    trend: 'up',
    icon: UserPlus,
    color: 'from-green-500 to-green-600',
    subtitle: 'Ce mois'
  },
  {
    title: 'Paiements recus',
    value: (stats.value.paiements * 150000).toLocaleString('fr-FR') + ' FCFA',
    change: '+18%',
    trend: 'up',
    icon: Banknote,
    color: 'from-emerald-500 to-emerald-600',
    subtitle: 'Ce mois'
  },
  {
    title: 'Taux de réussite',
    value: stats.value.taux_reussite + '%',
    change: '+3%',
    trend: 'up',
    icon: Award,
    color: 'from-purple-500 to-purple-600',
    subtitle: 'Annuel'
  }
])

const alerts = ref([
  { id: 1, type: 'warning', title: 'Décrochages détectés', count: 23, icon: AlertTriangle, urgent: true },
  { id: 2, type: 'info', title: 'Examens à venir', count: 12, icon: Calendar, urgent: false },
  { id: 3, type: 'success', title: 'Dossiers validés', count: 89, icon: CheckCircle, urgent: false },
  { id: 4, type: 'error', title: 'Retards de paiement', count: 34, icon: FileText, urgent: true },
  { id: 5, type: 'info', title: 'Cours annulés', count: 3, icon: Clock, urgent: false },
])

const recentActivities = ref([
  { id: 1, action: 'Nouvelle inscription', user: 'Marie Nguema', detail: 'L3 Informatique', time: '5 min', type: 'inscription' },
  { id: 2, action: 'Note validée', user: 'Prof. Mbadinga', detail: 'Base de Données', time: '12 min', type: 'note' },
  { id: 3, action: 'Paiement reçu', user: 'Jean-Pierre Ondo', detail: '150 000 FCFA', time: '18 min', type: 'paiement' },
  { id: 4, action: 'Emploi du temps modifié', user: 'Admin Scolarité', detail: 'Semaine 12', time: '1h', type: 'edt' },
  { id: 5, action: 'Nouveau diplôme', user: 'Système', detail: 'Promo 2023', time: '2h', type: 'diplome' },
])

const quickActions = ref([
  { id: 1, title: 'Inscrire étudiant', icon: Plus, color: 'bg-blue-500', route: '/etudiants', count: null },
  { id: 2, title: 'Saisir notes', icon: FileText, color: 'bg-green-500', route: '/pedagogie', count: null },
  { id: 3, title: 'Enregistrer paiement', icon: DollarSign, color: 'bg-emerald-500', route: '/finances', count: null },
  { id: 4, title: 'Générer rapport', icon: Download, color: 'bg-purple-500', route: null, count: null },
  { id: 5, title: 'Voir planning', icon: Calendar, color: 'bg-orange-500', route: '/pedagogie', count: null },
  { id: 6, title: 'Gérer filière', icon: BookOpen, color: 'bg-teal-500', route: '/administration', count: null },
])

const topModules = [
  { title: 'Inscriptions', value: 342, total: 400, color: 'bg-blue-500' },
  { title: 'Paiements', value: 156, total: 180, color: 'bg-green-500' },
  { title: 'Notes saisies', value: 1847, total: 2100, color: 'bg-purple-500' },
  { title: 'Deliberations', value: 89, total: 100, color: 'bg-orange-500' },
]

const statsCards = ref([
  { label: 'Filieres actives', value: '7', icon: BookOpen, color: 'text-green-600' },
  { label: 'Cours aujourd\'hui', value: '24', icon: Clock, color: 'text-blue-600' },
  { label: 'Enseignants', value: '45', icon: Users, color: 'text-purple-600' },
  { label: 'Debiteurs', value: '23', icon: AlertTriangle, color: 'text-red-600' },
])

function formatTime(date: Date) {
  return date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })
}

function formatDate(date: Date) {
  return date.toLocaleDateString('fr-FR', { weekday: 'long', day: 'numeric', month: 'long' })
}

async function fetchStats() {
  try {
    loading.value = true
    error.value = ''

    const token = localStorage.getItem('auth_token')
    if (!token) return

    const response = await fetchWithAuth('http://127.0.0.1:8765/api/v1/admin/stats')
    if (response.ok) {
      const data = await response.json()
      stats.value = { ...stats.value, ...data }
    }
  } catch (e) {
    console.error('Failed to fetch stats:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStats()
  setInterval(() => { currentTime.value = new Date() }, 60000)
})

function refresh() {
  fetchStats()
}
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">
          Tableau de bord
        </h1>
        <p class="text-gray-500 mt-1 flex items-center gap-2">
          <span class="capitalize">{{ formatDate(currentTime) }}</span>
          <span class="text-[#1B4F72] font-semibold">{{ formatTime(currentTime) }}</span>
        </p>
      </div>
      <div class="flex items-center gap-3">
        <!-- Connection Status -->
        <div :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2',
          syncStore.isOnline ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        ]">
          <component :is="syncStore.isOnline ? Wifi : WifiOff" class="w-4 h-4" />
          {{ syncStore.isOnline ? 'En ligne' : 'Hors ligne' }}
        </div>
        <!-- Academic Year -->
        <span class="px-3 py-1.5 bg-[#1B4F72]/10 text-[#1B4F72] rounded-full text-sm font-medium">
          2024-2025
        </span>
        <button
          @click="refresh"
          :disabled="loading"
          class="p-2 hover:bg-gray-100 rounded-lg transition-colors disabled:opacity-50"
        >
          <RefreshCw :class="['w-5 h-5 text-gray-600', { 'animate-spin': loading }]" />
        </button>
      </div>
    </div>

    <!-- Welcome Banner -->
    <div class="bg-gradient-to-r from-[#1B4F72] to-[#154360] rounded-xl p-6 text-white">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-xl font-semibold mb-1">Bienvenue, {{ authStore.user?.prenom }} {{ authStore.user?.nom }}</h2>
          <p class="text-white/80 text-sm">Gestion Académique - Centre Universitaire de Koulamoutou</p>
        </div>
        <div class="hidden md:flex items-center gap-4">
          <div class="text-right">
            <div class="text-3xl font-bold">{{ stats.etudiants }}</div>
            <div class="text-sm text-white/80">Étudiants</div>
          </div>
          <div class="w-px h-12 bg-white/30"></div>
          <div class="text-right">
            <div class="text-3xl font-bold">{{ stats.filieres }}</div>
            <div class="text-sm text-white/80">Filières</div>
          </div>
          <div class="w-px h-12 bg-white/30"></div>
          <div class="text-right">
            <div class="text-3xl font-bold">{{ stats.taux_reussite }}%</div>
            <div class="text-sm text-white/80">Réussite</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div v-for="i in 4" :key="i" class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 animate-pulse">
        <div class="h-14 w-14 bg-gray-200 rounded-xl mb-4"></div>
        <div class="h-10 bg-gray-200 rounded mb-2 w-32"></div>
        <div class="h-4 bg-gray-200 rounded w-24"></div>
      </div>
    </div>

    <!-- KPI Cards -->
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="kpi in kpis"
        :key="kpi.title"
        class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-lg transition-all group"
      >
        <div class="flex items-start justify-between mb-4">
          <div :class="['w-14 h-14 rounded-xl flex items-center justify-center bg-gradient-to-br', kpi.color]">
            <component :is="kpi.icon" class="w-7 h-7 text-white" />
          </div>
          <div :class="[
            'flex items-center gap-1 text-sm font-medium px-2 py-1 rounded-full',
            kpi.trend === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          ]">
            <component :is="kpi.trend === 'up' ? ArrowUpRight : ArrowDownRight" class="w-4 h-4" />
            {{ kpi.change }}
          </div>
        </div>
        <h3 class="text-3xl font-bold text-gray-900 mb-1">{{ kpi.value }}</h3>
        <p class="text-sm text-gray-500">{{ kpi.title }}</p>
        <p class="text-xs text-gray-400 mt-1">{{ kpi.subtitle }}</p>
      </div>
    </div>

    <!-- Stats Cards Row -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="stat in statsCards" :key="stat.label" class="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center gap-3">
        <div :class="['w-10 h-10 rounded-lg flex items-center justify-center bg-gray-100', stat.color]">
          <component :is="stat.icon" class="w-5 h-5" />
        </div>
        <div>
          <div class="text-xl font-bold text-gray-900">{{ stat.value }}</div>
          <div class="text-xs text-gray-500">{{ stat.label }}</div>
        </div>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Alerts Panel -->
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-heading font-semibold text-gray-900 flex items-center gap-2">
            <AlertTriangle class="w-5 h-5 text-orange-500" />
            Alertes actives
          </h2>
          <span class="text-xs text-gray-500">{{ alerts.length }} alertes</span>
        </div>
        <div class="p-4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          <div
            v-for="alert in alerts"
            :key="alert.id"
            :class="[
              'flex items-center gap-3 p-4 rounded-lg border transition-all cursor-pointer hover:scale-[1.02]',
              alert.urgent 
                ? 'bg-red-50 border-red-200 hover:border-red-300' 
                : 'bg-gray-50 border-gray-200 hover:border-gray-300'
            ]"
          >
            <div :class="[
              'w-10 h-10 rounded-lg flex items-center justify-center',
              alert.type === 'warning' ? 'bg-yellow-100 text-yellow-600' :
              alert.type === 'info' ? 'bg-blue-100 text-blue-600' :
              alert.type === 'success' ? 'bg-green-100 text-green-600' :
              'bg-red-100 text-red-600'
            ]">
              <component :is="alert.icon" class="w-5 h-5" />
            </div>
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-900 text-sm truncate">{{ alert.title }}</p>
              <p class="text-xs text-gray-500">{{ alert.count }} elements</p>
            </div>
            <div v-if="alert.urgent" class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>

      <!-- Recent Activities -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-heading font-semibold text-gray-900 flex items-center gap-2">
            <Activity class="w-5 h-5 text-[#1B4F72]" />
            Activités recentes
          </h2>
          <button class="text-xs text-[#1B4F72] hover:underline">Voir tout</button>
        </div>
        <div class="p-4 space-y-3">
          <div
            v-for="activity in recentActivities"
            :key="activity.id"
            class="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer"
          >
            <div class="w-2 h-2 mt-2 rounded-full bg-[#1B4F72] flex-shrink-0" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900">{{ activity.action }}</p>
              <p class="text-xs text-gray-500">{{ activity.user }}</p>
              <p class="text-xs text-[#1B4F72] mt-0.5">{{ activity.detail }}</p>
            </div>
            <span class="text-xs text-gray-400 whitespace-nowrap">{{ activity.time }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-heading font-semibold text-gray-900">
          Actions rapides
        </h2>
        <span class="text-xs text-gray-500">Acces direct aux fonctions principales</span>
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        <button
          v-for="action in quickActions"
          :key="action.id"
          class="flex flex-col items-center gap-2 p-4 rounded-xl border border-gray-200 hover:border-[#1B4F72] hover:bg-[#1B4F72]/5 transition-all group"
        >
          <div :class="['w-12 h-12 rounded-xl flex items-center justify-center text-white', action.color]">
            <component :is="action.icon" class="w-6 h-6" />
          </div>
          <span class="text-sm font-medium text-gray-700 text-center">{{ action.title }}</span>
        </button>
      </div>
    </div>

    <!-- Progress Bars -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h2 class="text-lg font-heading font-semibold text-gray-900 mb-4">
        Progression mensuelle
      </h2>
      <div class="space-y-4">
        <div v-for="module in topModules" :key="module.title">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-medium text-gray-700">{{ module.title }}</span>
            <span class="text-sm text-gray-500">{{ module.value }} / {{ module.total }}</span>
          </div>
          <div class="flex items-center gap-4">
            <div class="flex-1 bg-gray-100 rounded-full h-3">
              <div
                :class="['h-3 rounded-full transition-all', module.color]"
                :style="{ width: (module.value / module.total * 100) + '%' }"
              ></div>
            </div>
            <span class="text-sm font-semibold text-gray-900 w-12 text-right">
              {{ Math.round(module.value / module.total * 100) }}%
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Weekly Chart Preview -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-heading font-semibold text-gray-900">Inscriptions hebdo</h2>
          <span class="text-xs text-green-600 font-medium">+18% vs semaine dernière</span>
        </div>
        <div class="flex items-end justify-between h-32 gap-2">
          <div v-for="day in weeklyData" :key="day.day" class="flex-1 flex flex-col items-center gap-2">
            <div
              class="w-full bg-blue-500 rounded-t-lg transition-all hover:bg-blue-600"
              :style="{ height: (day.inscriptions / 25 * 100) + '%', minHeight: day.inscriptions > 0 ? '8px' : '0' }"
            ></div>
            <span class="text-xs text-gray-500">{{ day.day }}</span>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-heading font-semibold text-gray-900">Paiements hebdo</h2>
          <span class="text-xs text-green-600 font-medium">+12% vs semaine dernière</span>
        </div>
        <div class="flex items-end justify-between h-32 gap-2">
          <div v-for="day in weeklyData" :key="day.day" class="flex-1 flex flex-col items-center gap-2">
            <div
              class="w-full bg-green-500 rounded-t-lg transition-all hover:bg-green-600"
              :style="{ height: (day.paiements / 25 * 100) + '%', minHeight: day.paiements > 0 ? '8px' : '0' }"
            ></div>
            <span class="text-xs text-gray-500">{{ day.day }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Banner -->
    <div v-if="error" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-700 flex items-center gap-3">
      <AlertTriangle class="w-5 h-5" />
      {{ error }}
    </div>
  </div>
</template>
