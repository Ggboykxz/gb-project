<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Centre de Synchronisation</h1>
        <p class="text-sm text-gray-500 mt-1">Gérez la synchronisation des données entre votre poste et le serveur central</p>
      </div>
      <div class="flex items-center gap-3">
        <div :class="[
          'px-3 py-1.5 rounded-full text-sm font-medium flex items-center gap-2',
          syncStore.isOnline 
            ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400' 
            : 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400'
        ]">
          <div :class="[
            'w-2 h-2 rounded-full',
            syncStore.isOnline ? 'bg-green-500' : 'bg-red-500'
          ]"></div>
          {{ syncStore.isOnline ? 'En ligne' : 'Hors ligne' }}
        </div>
      </div>
    </div>

    <!-- Statut global -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Opérations en attente</div>
        <div class="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-1">
          {{ syncStore.status?.pending_operations ?? 0 }}
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Échecs</div>
        <div class="text-2xl font-bold text-red-600 dark:text-red-400 mt-1">
          {{ syncStore.status?.failed_operations ?? 0 }}
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Conflits</div>
        <div class="text-2xl font-bold text-orange-600 dark:text-orange-400 mt-1">
          {{ syncStore.status?.unresolved_conflicts ?? 0 }}
        </div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        <div class="text-sm text-gray-500 dark:text-gray-400">Dernière sync</div>
        <div class="text-sm font-semibold text-gray-900 dark:text-white mt-2">
          {{ syncStore.lastSyncDate ? formatDateTime(syncStore.lastSyncDate) : 'Jamais' }}
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Actions de synchronisation</h2>
      
      <div class="space-y-4">
        <!-- Barre de progression -->
        <div v-if="syncStore.isSyncing" class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
          <div 
            class="bg-blue-600 h-2.5 rounded-full transition-all duration-300" 
            :style="{ width: `${syncStore.syncProgress}%` }"
          ></div>
        </div>

        <div class="flex flex-wrap gap-3">
          <button
            @click="handleSyncAll"
            :disabled="syncStore.isSyncing"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium rounded-lg transition-colors flex items-center gap-2"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            {{ syncStore.isSyncing ? 'Synchronisation...' : 'Synchroniser tout' }}
          </button>

          <button
            @click="handleUpload"
            :disabled="syncStore.isSyncing || !syncStore.hasPendingOperations"
            class="px-4 py-2 bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-medium rounded-lg transition-colors"
          >
            Envoyer les modifications ({{ syncStore.status?.pending_operations ?? 0 }})
          </button>

          <button
            @click="handleDownload"
            :disabled="syncStore.isSyncing"
            class="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-purple-400 text-white font-medium rounded-lg transition-colors"
          >
            Récupérer depuis le serveur
          </button>

          <button
            @click="fetchStatus"
            :disabled="syncStore.isSyncing"
            class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200 font-medium rounded-lg transition-colors"
          >
            Actualiser le statut
          </button>
        </div>
      </div>
    </div>

    <!-- Conflits -->
    <div v-if="syncStore.hasConflicts" class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <svg class="w-5 h-5 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>
        </svg>
        Conflits à résoudre ({{ syncStore.conflicts.length }})
      </h2>

      <div class="space-y-3">
        <div v-for="conflict in syncStore.conflicts" :key="conflict.id" 
             class="border border-orange-200 dark:border-orange-800 rounded-lg p-4 bg-orange-50 dark:bg-orange-900/20">
          <div class="flex items-start justify-between">
            <div>
              <div class="font-medium text-gray-900 dark:text-white">
                Table: {{ conflict.table_name }} - ID: {{ conflict.record_id }}
              </div>
              <div class="text-sm text-gray-500 mt-1">
                Détecté le: {{ formatDateTime(new Date(conflict.detected_at)) }}
              </div>
            </div>
            <div class="flex gap-2">
              <button
                @click="resolveConflict(conflict.id, 'local')"
                class="px-3 py-1.5 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded transition-colors"
              >
                Garder version locale
              </button>
              <button
                @click="resolveConflict(conflict.id, 'remote')"
                class="px-3 py-1.5 text-sm bg-purple-600 hover:bg-purple-700 text-white rounded transition-colors"
              >
                Prendre version serveur
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Historique récent -->
    <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
      <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Statistiques</h2>
      <div class="text-sm text-gray-600 dark:text-gray-400">
        <p>Appareil: <span class="font-mono">{{ syncStore.status?.device_id ?? 'Inconnu' }}</span></p>
        <p class="mt-2">La synchronisation fonctionne en mode offline-first. Toutes vos modifications sont stockées localement et envoyées au serveur lorsque la connexion est disponible.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useSyncStore } from '@/stores/sync';
import { toast } from 'vue-sonner';

const syncStore = useSyncStore();

onMounted(() => {
  fetchStatus();
});

async function fetchStatus() {
  await syncStore.fetchStatus();
}

async function handleSyncAll() {
  const result = await syncStore.syncAll();
  if (result.success) {
    toast.success(result.message);
  } else {
    toast.error(result.message);
  }
}

async function handleUpload() {
  const result = await syncStore.uploadChanges();
  if (result.success) {
    toast.success(result.message);
  } else {
    toast.error(result.message);
  }
}

async function handleDownload() {
  const result = await syncStore.downloadChanges();
  if (result.success) {
    toast.success(result.message);
  } else {
    toast.error(result.message);
  }
}

async function resolveConflict(conflictId: number, resolution: 'local' | 'remote') {
  const result = await syncStore.resolveConflict(conflictId, resolution);
  if (result.success) {
    toast.success('Conflit résolu avec succès');
  } else {
    toast.error(result.message);
  }
}

function formatDateTime(date: Date): string {
  return date.toLocaleString('fr-GA', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}
</script>
