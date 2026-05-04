<script setup lang="ts">
import { Building2, Users, BookOpen, Calendar } from 'lucide-vue-next'

const modules = [
  {
    title: 'Inscriptions',
    description: 'Gérer les inscriptions et réinscriptions des étudiants',
    icon: Users,
    link: '/administration/inscriptions'
  },
  {
    title: 'Parcours pédagogiques',
    description: 'Configurer les filières, UE et maquettes',
    icon: BookOpen,
    link: '/administration/parcours'
  },
  {
    title: 'Emploi du temps',
    description: 'Planifier les cours et gérer les salles',
    icon: Calendar,
    link: '/administration/edt'
  },
  {
    title: 'Notes & Délibérations',
    description: 'Saisir les notes et générer les PV de jury',
    icon: Building2,
    link: '/administration/notes'
  },
]
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-heading font-bold text-gray-900">Administration</h1>
      <p class="text-gray-500 mt-1">Gestion académique et administrative</p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <router-link
        v-for="module in modules"
        :key="module.title"
        :to="module.link"
        class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md hover:border-primary transition-all group"
      >
        <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center mb-4 group-hover:bg-primary group-hover:text-white transition-colors">
          <component :is="module.icon" class="w-6 h-6 text-primary group-hover:text-white" />
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ module.title }}</h3>
        <p class="text-sm text-gray-500">{{ module.description }}</p>
      </router-link>
    </div>
  </div>
</template>
