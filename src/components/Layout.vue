<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { 
  LayoutDashboard, 
  Building2, 
  Users, 
  BookOpen, 
  FlaskConical, 
  Banknote,
  GraduationCap,
  RefreshCw,
  LogOut,
  Menu,
  Bell,
  Wifi,
  WifiOff
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useSyncStore } from '@/stores/sync'

const authStore = useAuthStore()
const syncStore = useSyncStore()
const route = useRoute()

const sidebarItems = computed(() => [
  { icon: LayoutDashboard, label: 'Tableau de bord', path: '/' },
  { icon: Building2, label: 'Administration', path: '/administration' },
  { icon: Users, label: 'Étudiants', path: '/etudiants' },
  { icon: BookOpen, label: 'Pédagogie', path: '/pedagogie' },
  { icon: GraduationCap, label: 'Vie Étudiante', path: '/vie-etudiante' },
  { icon: FlaskConical, label: 'Recherche', path: '/recherche' },
  { icon: Banknote, label: 'Finances', path: '/finances' },
  { icon: RefreshCw, label: 'Synchronisation', path: '/sync' },
])

const isSidebarOpen = computed(() => true)

const syncStatusColor = computed(() => {
  switch (syncStore.status) {
    case 'online': return 'bg-success text-white'
    case 'offline': return 'bg-red-500 text-white'
    case 'syncing': return 'bg-orange-500 text-white'
    default: return 'bg-gray-400 text-white'
  }
})

const syncIcon = computed(() => syncStore.isOnline ? Wifi : WifiOff)

function handleLogout() {
  authStore.logout()
  window.location.href = '/login'
}
</script>

<template>
  <div class="flex h-screen bg-background-light">
    <!-- Sidebar -->
    <aside 
      :class="[
        'bg-primary text-white transition-all duration-300 flex flex-col',
        isSidebarOpen ? 'w-64' : 'w-16'
      ]"
    >
      <!-- Logo -->
      <div class="p-4 border-b border-primary/20">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-secondary rounded-lg flex items-center justify-center">
            <span class="text-primary font-bold text-lg">GE</span>
          </div>
          <span v-if="isSidebarOpen" class="font-heading font-semibold text-lg">
            GabonEdu
          </span>
        </div>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <RouterLink
          v-for="item in sidebarItems"
          :key="item.path"
          :to="item.path"
          :class="[
            'flex items-center gap-3 px-3 py-2.5 rounded-lg transition-colors',
            route.path === item.path
              ? 'bg-secondary text-primary font-medium'
              : 'hover:bg-primary/80'
          ]"
        >
          <component :is="item.icon" class="w-5 h-5 flex-shrink-0" />
          <span v-if="isSidebarOpen">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <!-- Logout -->
      <div class="p-3 border-t border-primary/20">
        <button
          @click="handleLogout"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg hover:bg-primary/80 w-full transition-colors"
        >
          <LogOut class="w-5 h-5 flex-shrink-0" />
          <span v-if="isSidebarOpen">Déconnexion</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header -->
      <header class="bg-white border-b border-gray-200 px-6 py-3">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <button class="lg:hidden">
              <Menu class="w-6 h-6" />
            </button>
            <nav class="flex items-center gap-2 text-sm text-gray-500">
              <span class="font-medium text-primary">GabonEdu Campus</span>
              <span>/</span>
              <span>{{ route.name }}</span>
            </nav>
          </div>

          <div class="flex items-center gap-4">
            <!-- Sync Status -->
            <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100">
              <component :is="syncIcon" :class="['w-4 h-4', syncStatusColor]" />
              <span class="text-xs font-medium capitalize">{{ syncStore.status }}</span>
            </div>

            <!-- Notifications -->
            <button class="relative p-2 hover:bg-gray-100 rounded-full">
              <Bell class="w-5 h-5 text-gray-600" />
              <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            <!-- User Info -->
            <div class="flex items-center gap-3 pl-4 border-l border-gray-200">
              <div class="text-right">
                <p class="text-sm font-medium text-gray-900">
                  {{ authStore.user?.prenom }} {{ authStore.user?.nom }}
                </p>
                <p class="text-xs text-gray-500">{{ authStore.user?.role }}</p>
              </div>
              <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                <span class="text-primary font-semibold">
                  {{ authStore.user?.prenom[0] }}{{ authStore.user?.nom[0] }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Content Area -->
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>

      <!-- Footer -->
      <footer class="bg-white border-t border-gray-200 px-6 py-2">
        <div class="flex items-center justify-between text-xs text-gray-500">
          <span>GabonEdu Campus v1.0.0</span>
          <span>{{ new Date().toLocaleDateString('fr-FR') }}</span>
        </div>
      </footer>
    </div>
  </div>
</template>
