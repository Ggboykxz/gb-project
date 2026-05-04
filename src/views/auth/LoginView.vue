<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSyncStore } from '@/stores/sync'
import { LogIn, Shield } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const syncStore = useSyncStore()

const email = ref('admin@gabonedu.ga')
const password = ref('admin123')
const totpCode = ref('')
const showTotp = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    // Simuler une connexion (à remplacer par appel API réel)
    await new Promise(resolve => setTimeout(resolve, 1000))

    // Mock user data
    const user = {
      id: '1',
      email: email.value,
      nom: 'ADMINISTRATEUR',
      prenom: 'Super',
      role: 'SUPER_ADMIN' as const,
    }

    authStore.setUser(user)
    
    // Simuler token JWT
    localStorage.setItem('auth_token', 'mock-jwt-token')
    
    // Simuler statut online
    syncStore.setOnline(true)

    router.push('/')
  } catch (err) {
    error.value = 'Échec de la connexion. Vérifiez vos identifiants.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex bg-background-light">
    <!-- Left Panel -->
    <div class="hidden lg:flex lg:w-1/2 bg-primary flex-col justify-between p-12 text-white">
      <div>
        <div class="flex items-center gap-3 mb-8">
          <div class="w-14 h-14 bg-secondary rounded-xl flex items-center justify-center">
            <span class="text-primary font-bold text-2xl">GE</span>
          </div>
          <div>
            <h1 class="font-heading text-2xl font-bold">GabonEdu Campus</h1>
            <p class="text-primary/80 text-sm">Université Connectée</p>
          </div>
        </div>
        
        <h2 class="text-3xl font-heading font-semibold mb-4">
          Bienvenue sur votre plateforme de gestion académique
        </h2>
        <p class="text-primary/70 text-lg leading-relaxed">
          Solution complète pour la gestion administrative, pédagogique et financière 
          des universités gabonaises. Offline-first, conforme Gabon Digital.
        </p>
      </div>

      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <Shield class="w-5 h-5 text-secondary" />
          <span>Sécurité renforcée avec chiffrement AES-256</span>
        </div>
        <div class="flex items-center gap-3">
          <LogIn class="w-5 h-5 text-secondary" />
          <span>Fonctionne hors-ligne avec synchronisation automatique</span>
        </div>
      </div>
    </div>

    <!-- Right Panel - Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <!-- Mobile Logo -->
        <div class="lg:hidden flex items-center gap-3 mb-8 justify-center">
          <div class="w-14 h-14 bg-primary rounded-xl flex items-center justify-center">
            <span class="text-secondary font-bold text-2xl">GE</span>
          </div>
        </div>

        <div class="mb-8">
          <h2 class="text-2xl font-heading font-bold text-gray-900 mb-2">
            Connexion
          </h2>
          <p class="text-gray-500">
            Accédez à votre espace de gestion
          </p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-5">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-1.5">
              Adresse email
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              required
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              placeholder="nom@universite.ga"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1.5">
              Mot de passe
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              placeholder="••••••••"
            />
          </div>

          <div v-if="showTotp">
            <label for="totp" class="block text-sm font-medium text-gray-700 mb-1.5">
              Code 2FA
            </label>
            <input
              id="totp"
              v-model="totpCode"
              type="text"
              maxlength="6"
              class="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent transition-all text-center tracking-widest"
              placeholder="000000"
            />
          </div>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
            {{ error }}
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <LogIn class="w-5 h-5" />
            {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
          </button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-sm text-gray-500">
            Identifiants de test: admin@gabonedu.ga / admin123
          </p>
        </div>
      </div>
    </div>
  </div>
</template>
