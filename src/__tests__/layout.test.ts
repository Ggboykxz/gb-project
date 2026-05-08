import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/components/Layout.vue'
import { setActivePinia, createPinia } from 'pinia'

vi.mock('@/stores/auth', () => ({
  useAuthStore: () => ({
    isAuthenticated: true,
    user: { name: 'Test User', prenom: 'Test', nom: 'User' },
    logout: vi.fn()
  })
}))

vi.mock('@/stores/sync', () => ({
  useSyncStore: () => ({
    isSyncing: false,
    isOnline: true
  })
}))

describe('Layout.vue', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  const router = createRouter({
    history: createWebHistory(),
    routes: [
      { path: '/', component: { template: '<div>Dashboard</div>' }, name: 'dashboard' },
      { path: '/etudiants', component: { template: '<div>Etudiants</div>' }, name: 'etudiants' }
    ]
  })

  it('should render sidebar with navigation items', async () => {
    router.push('/')
    await router.isReady()
    
    const wrapper = mount(Layout, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.html()).toContain('Tableau de bord')
    expect(wrapper.html()).toContain('Étudiants')
  })

  it('should have RouterLink components', () => {
    const wrapper = mount(Layout, {
      global: {
        plugins: [router]
      }
    })
    
    expect(wrapper.findAllComponents({ name: 'RouterLink' }).length).toBeGreaterThan(0)
  })
})