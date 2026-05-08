import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import type { User } from '@/stores/auth'

describe('useAuthStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('should initialize with null user', () => {
    const store = useAuthStore()
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should set user correctly', () => {
    const store = useAuthStore()
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

  it('should logout and clear user', () => {
    const store = useAuthStore()
    const testUser: User = {
      id: '1',
      email: 'test@cuk.ga',
      nom: 'Test',
      prenom: 'User',
      role: 'ADMIN_SCOL'
    }
    
    store.setUser(testUser)
    store.logout()
    
    expect(store.user).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })

  it('should check user roles correctly', () => {
    const store = useAuthStore()
    const adminUser: User = {
      id: '1',
      email: 'admin@cuk.ga',
      nom: 'Admin',
      prenom: 'Super',
      role: 'SUPER_ADMIN'
    }
    
    store.setUser(adminUser)
    
    expect(store.hasRole(['SUPER_ADMIN'])).toBe(true)
    expect(store.hasRole(['ADMIN_SCOL'])).toBe(false)
    expect(store.hasRole(['SUPER_ADMIN', 'ADMIN_SCOL'])).toBe(true)
  })

  it('should return false for hasRole when no user', () => {
    const store = useAuthStore()
    expect(store.hasRole(['SUPER_ADMIN'])).toBe(false)
  })
})
