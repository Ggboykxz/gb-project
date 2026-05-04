import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
  },
  {
    path: '/',
    name: 'Layout',
    component: () => import('@/components/Layout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/DashboardView.vue'),
      },
      {
        path: 'administration',
        name: 'Administration',
        component: () => import('@/views/administration/AdministrationView.vue'),
      },
      {
        path: 'etudiants',
        name: 'Etudiants',
        component: () => import('@/views/etudiants/EtudiantsView.vue'),
      },
      {
        path: 'pedagogie',
        name: 'Pedagogie',
        component: () => import('@/views/pedagogie/PedagogieView.vue'),
      },
      {
        path: 'recherche',
        name: 'Recherche',
        component: () => import('@/views/recherche/RechercheView.vue'),
      },
      {
        path: 'finances',
        name: 'Finances',
        component: () => import('@/views/finances/FinancesView.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
