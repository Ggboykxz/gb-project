import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type UserRole = 
  | 'SUPER_ADMIN' 
  | 'ADMIN_SCOL' 
  | 'ENSEIGNANT' 
  | 'ETUDIANT' 
  | 'FINANCIER' 
  | 'BIBLIOTHECAIRE' 
  | 'CHERCHEUR'

export interface User {
  id: string
  email: string
  nom: string
  prenom: string
  role: UserRole
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isAuthenticated = computed(() => user.value !== null)
  const userRole = computed(() => user.value?.role)

  function setUser(newUser: User) {
    user.value = newUser
  }

  function logout() {
    user.value = null
  }

  function hasRole(roles: UserRole[]): boolean {
    if (!user.value) return false
    return roles.includes(user.value.role)
  }

  return {
    user,
    isAuthenticated,
    userRole,
    setUser,
    logout,
    hasRole,
  }
})
