import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import type { User, UserRole } from '@/stores/auth'

describe('useAuthStore', () => {
  let store: ReturnType<typeof useAuthStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useAuthStore()
  })

  afterEach(() => {
    store.logout()
  })

  describe('initialization', () => {
    it('should initialize with null user', () => {
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(store.userRole).toBeUndefined()
    })

    it('should initialize with empty getters', () => {
      expect(store.hasRole([])).toBe(false)
    })
  })

  describe('setUser', () => {
    it('should set user correctly', () => {
      const testUser: User = {
        id: '1',
        email: 'test@cuk.ga',
        nom: 'Test',
        prenom: 'User',
        role: 'ETUDIANT'
      }
      
      store.setUser(testUser)
      
      expect(store.user).toEqual(testUser)
      expect(store.isAuthenticated).toBe(true)
      expect(store.userRole).toBe('ETUDIANT')
    })

    it('should update user properties', () => {
      const user1: User = {
        id: '1',
        email: 'user1@cuk.ga',
        nom: 'User',
        prenom: 'One',
        role: 'ETUDIANT'
      }
      
      store.setUser(user1)
      expect(store.user?.email).toBe('user1@cuk.ga')
      
      const user2: User = {
        id: '2',
        email: 'user2@cuk.ga',
        nom: 'User',
        prenom: 'Two',
        role: 'ADMIN_SCOL'
      }
      
      store.setUser(user2)
      expect(store.user?.id).toBe('2')
      expect(store.userRole).toBe('ADMIN_SCOL')
    })

    it('should handle all user roles', () => {
      const roles: UserRole[] = ['SUPER_ADMIN', 'ADMIN_SCOL', 'ENSEIGNANT', 'ETUDIANT', 'FINANCIER', 'BIBLIOTHECAIRE', 'CHERCHEUR']
      
      roles.forEach(role => {
        const user: User = {
          id: '1',
          email: 'test@cuk.ga',
          nom: 'Test',
          prenom: 'User',
          role
        }
        store.setUser(user)
        expect(store.userRole).toBe(role)
        store.logout()
      })
    })
  })

  describe('logout', () => {
    it('should clear user on logout', () => {
      const testUser: User = {
        id: '1',
        email: 'test@cuk.ga',
        nom: 'Test',
        prenom: 'User',
        role: 'SUPER_ADMIN'
      }
      
      store.setUser(testUser)
      expect(store.isAuthenticated).toBe(true)
      
      store.logout()
      
      expect(store.user).toBeNull()
      expect(store.isAuthenticated).toBe(false)
      expect(store.userRole).toBeUndefined()
    })

    it('should allow re-login after logout', () => {
      const user1: User = {
        id: '1',
        email: 'user1@cuk.ga',
        nom: 'User',
        prenom: 'One',
        role: 'ETUDIANT'
      }
      
      const user2: User = {
        id: '2',
        email: 'user2@cuk.ga',
        nom: 'User',
        prenom: 'Two',
        role: 'ADMIN_SCOL'
      }
      
      store.setUser(user1)
      store.logout()
      store.setUser(user2)
      
      expect(store.user?.id).toBe('2')
      expect(store.userRole).toBe('ADMIN_SCOL')
    })
  })

  describe('hasRole', () => {
    it('should return true for matching role', () => {
      const user: User = {
        id: '1',
        email: 'admin@cuk.ga',
        nom: 'Admin',
        prenom: 'Super',
        role: 'SUPER_ADMIN'
      }
      
      store.setUser(user)
      expect(store.hasRole(['SUPER_ADMIN'])).toBe(true)
    })

    it('should return false for non-matching role', () => {
      const user: User = {
        id: '1',
        email: 'student@cuk.ga',
        nom: 'Student',
        prenom: 'Test',
        role: 'ETUDIANT'
      }
      
      store.setUser(user)
      expect(store.hasRole(['ADMIN_SCOL'])).toBe(false)
    })

    it('should return true when user has one of multiple roles', () => {
      const user: User = {
        id: '1',
        email: 'admin@cuk.ga',
        nom: 'Admin',
        prenom: 'Test',
        role: 'ADMIN_SCOL'
      }
      
      store.setUser(user)
      expect(store.hasRole(['SUPER_ADMIN', 'ADMIN_SCOL'])).toBe(true)
    })

    it('should return false for empty roles array', () => {
      const user: User = {
        id: '1',
        email: 'admin@cuk.ga',
        nom: 'Admin',
        prenom: 'Test',
        role: 'SUPER_ADMIN'
      }
      
      store.setUser(user)
      expect(store.hasRole([])).toBe(false)
    })

    it('should return false when no user is logged in', () => {
      expect(store.hasRole(['SUPER_ADMIN'])).toBe(false)
      expect(store.hasRole(['ADMIN_SCOL', 'ETUDIANT'])).toBe(false)
    })
  })

  describe('computed properties', () => {
    it('should reactively update isAuthenticated', () => {
      expect(store.isAuthenticated).toBe(false)
      
      store.setUser({
        id: '1',
        email: 'test@cuk.ga',
        nom: 'Test',
        prenom: 'User',
        role: 'ETUDIANT'
      })
      
      expect(store.isAuthenticated).toBe(true)
    })

    it('should reactively update userRole', () => {
      expect(store.userRole).toBeUndefined()
      
      store.setUser({
        id: '1',
        email: 'test@cuk.ga',
        nom: 'Test',
        prenom: 'User',
        role: 'ENSEIGNANT'
      })
      
      expect(store.userRole).toBe('ENSEIGNANT')
    })
  })
})
