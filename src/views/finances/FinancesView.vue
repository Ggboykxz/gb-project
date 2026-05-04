<script setup lang="ts">
import { Banknote } from 'lucide-vue-next'
</script>

<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-2xl font-heading font-bold text-gray-900">Finances</h1>
      <p class="text-gray-500 mt-1">Gestion financière et logistique</p>
    </div>
    <div class="bg-white rounded-xl p-12 shadow-sm border border-gray-100 text-center">
      <Banknote class="w-16 h-16 text-primary/20 mx-auto mb-4" />
      <h3 class="text-lg font-semibold text-gray-900 mb-2">Module Finances</h3>
      <p class="text-gray-500">Facturation, budget, marchés publics, patrimoine, RH</p>
    </div>
  </div>
</template>
