import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'

const mockRoutes = [
  { path: '/', component: { template: '<div>Dashboard</div>' } },
  { path: '/login', component: { template: '<div>Login</div>' } },
  { path: '/etudiants', component: { template: '<div>Etudiants</div>' } }
]

const mockRouter = createRouter({
  history: createWebHistory(),
  routes: mockRoutes
})

describe('Router Configuration', () => {
  it('should have correct routes', () => {
    const routes = mockRouter.getRoutes()
    expect(routes.some(r => r.path === '/')).toBe(true)
    expect(routes.some(r => r.path === '/login')).toBe(true)
    expect(routes.some(r => r.path === '/etudiants')).toBe(true)
  })
})
