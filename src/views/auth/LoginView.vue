<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useSyncStore } from '@/stores/sync'
import { login, setToken, getCurrentUser } from '@/api/auth'
import { LogIn, Shield, Loader2, AlertCircle, Eye, EyeOff } from 'lucide-vue-next'

const router = useRouter()
const authStore = useAuthStore()
const syncStore = useSyncStore()

const email = ref('superadmin@cuk.ga')
const password = ref('Gabon2024!')
const totpCode = ref('')
const showTotp = ref(false)
const showPassword = ref(false)
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  if (!email.value || !password.value) {
    error.value = 'Veuillez remplir tous les champs'
    return
  }
  
  loading.value = true
  error.value = ''

  try {
    const response = await login(email.value, password.value)
    setToken(response.access_token)
    
    const user = await getCurrentUser(response.access_token)
    authStore.setUser({
      id: user.id,
      email: user.email,
      nom: user.nom,
      prenom: user.prenom,
      role: user.role,
    })
    
    syncStore.setOnline(true)
    router.push('/')
  } catch (err: any) {
    console.error('Login error:', err)
    if (err.message?.includes('Failed to connect') || err.message?.includes('NetworkError') || err.message?.includes('fetch')) {
      error.value = 'Serveur non accessible. Vérifiez votre connexion.'
    } else if (err.message?.includes('401') || err.message?.includes('incorrect')) {
      error.value = 'Email ou mot de passe incorrect'
    } else if (err.message?.includes('423') || err.message?.includes('verrouillé')) {
      error.value = 'Compte temporairement verrouillé. Réessayez dans 30 minutes.'
    } else {
      error.value = err.message || 'Échec de la connexion'
    }
  } finally {
    loading.value = false
  }
}

function togglePassword() {
  showPassword.value = !showPassword.value
}
</script>

<template>
  <div class="min-h-screen flex bg-gray-50">
    <!-- Left Panel - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-[#1B4F72] to-[#154360] flex-col justify-between p-12 text-white">
      <div>
        <div class="flex items-center gap-3 mb-8">
          <div class="w-14 h-14 bg-[#F39C12] rounded-xl flex items-center justify-center">
            <span class="text-[#1B4F72] font-bold text-2xl">GE</span>
          </div>
          <div>
            <h1 class="font-heading text-2xl font-bold">GabonEdu Campus</h1>
            <p class="text-white/80 text-sm">Centre Universitaire de Koulamoutou</p>
          </div>
        </div>
        
        <h2 class="text-3xl font-heading font-semibold mb-4">
          Bienvenue sur votre plateforme de gestion académique
        </h2>
        <p class="text-white/70 text-lg leading-relaxed">
          Solution complète pour la gestion administrative, pédagogique et financière 
          des universités gabonaises. Offline-first, conforme Gabon Digital.
        </p>
      </div>

      <div class="space-y-4">
        <div class="flex items-center gap-3">
          <Shield class="w-5 h-5 text-[#F39C12]" />
          <span class="text-white/90">Sécurité renforcée avec chiffrement AES-256</span>
        </div>
        <div class="flex items-center gap-3">
          <LogIn class="w-5 h-5 text-[#F39C12]" />
          <span class="text-white/90">Fonctionne hors-ligne avec synchronisation</span>
        </div>
      </div>

      <p class="text-white/50 text-sm">
        © 2024 GabonEdu - CUK/USTM
      </p>
    </div>

    <!-- Right Panel - Login Form -->
    <div class="w-full lg:w-1/2 flex items-center justify-center p-8">
      <div class="w-full max-w-md">
        <!-- Mobile Logo -->
        <div class="lg:hidden flex items-center gap-3 mb-8 justify-center">
          <div class="w-14 h-14 bg-[#1B4F72] rounded-xl flex items-center justify-center">
            <span class="text-[#F39C12] font-bold text-2xl">GE</span>
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
              autocomplete="email"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B4F72] focus:border-transparent transition-all"
              placeholder="votre@email.ga"
              :disabled="loading"
            />
          </div>

          <div class="relative">
            <label for="password" class="block text-sm font-medium text-gray-700 mb-1.5">
              Mot de passe
            </label>
            <input
              id="password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
              class="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B4F72] focus:border-transparent transition-all"
              placeholder="••••••••"
              :disabled="loading"
            />
            <button
              type="button"
              @click="togglePassword"
              class="absolute right-3 top-9 text-gray-400 hover:text-gray-600"
            >
              <EyeOff v-if="showPassword" class="w-5 h-5" />
              <Eye v-else class="w-5 h-5" />
            </button>
          </div>

          <div v-if="showTotp" class="relative">
            <label for="totp" class="block text-sm font-medium text-gray-700 mb-1.5">
              Code 2FA
            </label>
            <input
              id="totp"
              v-model="totpCode"
              type="text"
              maxlength="6"
              inputmode="numeric"
              pattern="[0-9]*"
              class="w-full px-4 py-3 text-center tracking-widest border border-gray-300 rounded-lg focus:ring-2 focus:ring-[#1B4F72] focus:border-transparent transition-all"
              placeholder="000000"
              :disabled="loading"
            />
          </div>

          <div v-if="error" class="flex items-start gap-2 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            <AlertCircle class="w-5 h-5 flex-shrink-0 mt-0.5" />
            <p class="text-sm">{{ error }}</p>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-[#1B4F72] hover:bg-[#154360] disabled:opacity-50 disabled:cursor-not-allowed text-white font-medium py-3 rounded-lg transition-colors flex items-center justify-center gap-2"
          >
            <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
            <LogIn v-else class="w-5 h-5" />
            {{ loading ? 'Connexion en cours...' : 'Se connecter' }}
          </button>
        </form>

        <div class="mt-8 p-4 bg-gray-100 rounded-lg">
          <p class="text-sm font-medium text-gray-700 mb-2">Identifiants de test:</p>
          <div class="text-xs text-gray-500 space-y-1">
            <p><span class="font-mono">superadmin@cuk.ga</span> / <span class="font-mono">Gabon2024!</span> (Super Admin)</p>
            <p><span class="font-mono">scolarite@cuk.ga</span> / <span class="font-mono">Gabon2024!</span> (Scolarité)</p>
            <p><span class="font-mono">etudiant.demo@cuk.ga</span> / <span class="font-mono">Gabon2024!</span> (Étudiant)</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>