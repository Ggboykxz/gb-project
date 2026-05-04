<script setup lang="ts">
import { computed } from 'vue'
import { 
  Users, 
  BookOpen, 
  GraduationCap, 
  TrendingUp, 
  AlertTriangle,
  Calendar,
  FileText,
  DollarSign,
  CheckCircle
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const kpis = computed(() => [
  { 
    title: 'Étudiants inscrits', 
    value: '2,847', 
    change: '+12%', 
    icon: Users,
    color: 'bg-blue-500'
  },
  { 
    title: 'Cours actifs', 
    value: '156', 
    change: '+5%', 
    icon: BookOpen,
    color: 'bg-green-500'
  },
  { 
    title: 'Taux de réussite', 
    value: '87.3%', 
    change: '+2.1%', 
    icon: GraduationCap,
    color: 'bg-purple-500'
  },
  { 
    title: 'Recettes du mois', 
    value: '45.2M FCFA', 
    change: '+8%', 
    icon: DollarSign,
    color: 'bg-orange-500'
  },
])

const alerts = [
  { type: 'warning', title: 'Décrochages détectés', count: 23, icon: AlertTriangle },
  { type: 'info', title: 'Examens à venir', count: 12, icon: Calendar },
  { type: 'success', title: 'Dossiers validés', count: 89, icon: CheckCircle },
  { type: 'error', title: 'Retards de paiement', count: 34, icon: FileText },
]

const recentActivities = [
  { action: 'Nouvelle inscription', user: 'Marie Nguema', time: 'Il y a 5 min' },
  { action: 'Note validée', user: 'Prof. Mbadinga', time: 'Il y a 12 min' },
  { action: 'Paiement reçu', user: 'Jean-Pierre Ondo', time: 'Il y a 18 min' },
  { action: 'Emploi du temps modifié', user: 'Admin Scolarité', time: 'Il y a 1h' },
]
</script>

<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">
          Tableau de bord
        </h1>
        <p class="text-gray-500 mt-1">
          Vue d'ensemble de votre établissement
        </p>
      </div>
      <div class="flex items-center gap-3">
        <span class="text-sm text-gray-500">
          Année académique: 2024-2025
        </span>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="kpi in kpis"
        :key="kpi.title"
        class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow"
      >
        <div class="flex items-center justify-between mb-4">
          <div :class="['w-12 h-12 rounded-lg flex items-center justify-center', kpi.color]">
            <component :is="kpi.icon" class="w-6 h-6 text-white" />
          </div>
          <span :class="[
            'text-sm font-medium',
            kpi.change.startsWith('+') ? 'text-green-600' : 'text-red-600'
          ]">
            {{ kpi.change }}
          </span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900">{{ kpi.value }}</h3>
        <p class="text-sm text-gray-500 mt-1">{{ kpi.title }}</p>
      </div>
    </div>

    <!-- Alerts & Activities -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Alerts -->
      <div class="lg:col-span-2 bg-white rounded-xl shadow-sm border border-gray-100">
        <div class="p-6 border-b border-gray-100">
          <h2 class="text-lg font-heading font-semibold text-gray-900">
            Alertes actives
          </h2>
        </div>
        <div class="p-6 grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div
            v-for="alert in alerts"
            :key="alert.title"
            class="flex items-center gap-4 p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors cursor-pointer"
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
            <div>
              <p class="font-medium text-gray-900">{{ alert.title }}</p>
              <p class="text-sm text-gray-500">{{ alert.count }} éléments</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-100">
        <div class="p-6 border-b border-gray-100">
          <h2 class="text-lg font-heading font-semibold text-gray-900">
            Activités récentes
          </h2>
        </div>
        <div class="p-6 space-y-4">
          <div
            v-for="(activity, index) in recentActivities"
            :key="index"
            class="flex items-start gap-3 pb-4 border-b border-gray-50 last:border-0 last:pb-0"
          >
            <div class="w-2 h-2 mt-2 rounded-full bg-primary flex-shrink-0" />
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ activity.action }}
              </p>
              <p class="text-xs text-gray-500 mt-0.5">
                {{ activity.user }} • {{ activity.time }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <h2 class="text-lg font-heading font-semibold text-gray-900 mb-4">
        Actions rapides
      </h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <button class="flex flex-col items-center gap-2 p-4 rounded-lg border border-gray-200 hover:border-primary hover:bg-primary/5 transition-colors">
          <Users class="w-6 h-6 text-primary" />
          <span class="text-sm font-medium text-gray-700">Inscrire étudiant</span>
        </button>
        <button class="flex flex-col items-center gap-2 p-4 rounded-lg border border-gray-200 hover:border-primary hover:bg-primary/5 transition-colors">
          <FileText class="w-6 h-6 text-primary" />
          <span class="text-sm font-medium text-gray-700">Saisir notes</span>
        </button>
        <button class="flex flex-col items-center gap-2 p-4 rounded-lg border border-gray-200 hover:border-primary hover:bg-primary/5 transition-colors">
          <DollarSign class="w-6 h-6 text-primary" />
          <span class="text-sm font-medium text-gray-700">Enregistrer paiement</span>
        </button>
        <button class="flex flex-col items-center gap-2 p-4 rounded-lg border border-gray-200 hover:border-primary hover:bg-primary/5 transition-colors">
          <TrendingUp class="w-6 h-6 text-primary" />
          <span class="text-sm font-medium text-gray-700">Générer rapport</span>
        </button>
      </div>
    </div>
  </div>
</template>
