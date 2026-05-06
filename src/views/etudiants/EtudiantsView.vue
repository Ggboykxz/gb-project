<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  Users, 
  Search, 
  Plus, 
  Download,
  Upload,
  Filter,
  MoreVertical,
  Phone,
  Mail,
  Calendar,
  MapPin,
  GraduationCap,
  FileText,
  AlertCircle
} from 'lucide-vue-next'

const searchQuery = ref('')
const activeTab = ref('inscriptions')

const tabs = [
  { id: 'inscriptions', label: 'Inscriptions', icon: Users },
  { id: 'dossiers', label: 'Dossiers académiques', icon: FileText },
  { id: 'documents', label: 'Documents', icon: FileText },
]

const etudiants = ref([
  { 
    id: 1, 
    nom: 'Mouanda', 
    prenom: 'Marie', 
    nip: 'NIP20240001',
    email: 'mouanda.marie@etu.cuk.ga',
    telephone: '+241 74 12 34 56',
    filiere: 'Informatique',
    niveau: 'L3',
    statut: 'Actif',
    date_naissance: '2002-05-15',
    nationalite: 'Gabonaise'
  },
  { 
    id: 2, 
    nom: 'Nkoghe', 
    prenom: 'Junior', 
    nip: 'NIP20240002',
    email: 'nkoghe.junior@etu.cuk.ga',
    telephone: '+241 74 23 45 67',
    filiere: 'Droit',
    niveau: 'L2',
    statut: 'Actif',
    date_naissance: '2003-08-22',
    nationalite: 'Gabonaise'
  },
  { 
    id: 3, 
    nom: 'Mboghe', 
    prenom: 'Christelle', 
    nip: 'NIP20240003',
    email: 'mboghe.christelle@etu.cuk.ga',
    telephone: '+241 74 34 56 78',
    filiere: 'Sciences Économiques',
    niveau: 'M1',
    statut: 'Actif',
    date_naissance: '2001-12-10',
    nationalite: 'Gabonaise'
  },
  { 
    id: 4, 
    nom: 'Obame', 
    prenom: 'Yannick', 
    nip: 'NIP20240004',
    email: 'obame.yannick@etu.cuk.ga',
    telephone: '+241 74 45 67 89',
    filiere: 'Médecine',
    niveau: 'DEMS',
    statut: 'Actif',
    date_naissance: '2000-03-25',
    nationalite: 'Gabonaise'
  },
  { 
    id: 5, 
    nom: 'Nguema', 
    prenom: 'Alain', 
    nip: 'NIP20240005',
    email: 'nguema.alain@etu.cuk.ga',
    telephone: '+241 74 56 78 90',
    filiere: 'Informatique',
    niveau: 'L1',
    statut: 'Suspendu',
    date_naissance: '2004-01-18',
    nationalite: 'Gabonaise'
  },
])

const inscriptions = ref([
  { 
    id: 1, 
    etudiant: 'Mouanda Marie', 
    filiere: 'Informatique', 
    niveau: 'L3',
    type: 'Réinscription',
    annee: '2024-2025',
    statut: 'Confirmée',
    date: '2024-09-01',
    frais_payes: true
  },
  { 
    id: 2, 
    etudiant: 'Nkoghe Junior', 
    filiere: 'Droit', 
    niveau: 'L2',
    type: 'Réinscription',
    annee: '2024-2025',
    statut: 'En attente',
    date: '2024-09-05',
    frais_payes: false
  },
  { 
    id: 3, 
    etudiant: 'Mboghe Christelle', 
    filiere: 'Sciences Économiques', 
    niveau: 'M1',
    type: 'Nouveau',
    annee: '2024-2025',
    statut: 'Validée',
    date: '2024-08-20',
    frais_payes: true
  },
])

const etudiantsFiltres = computed(() => {
  if (!searchQuery.value) return etudiants.value
  const query = searchQuery.value.toLowerCase()
  return etudiants.value.filter(e => 
    e.nom.toLowerCase().includes(query) ||
    e.prenom.toLowerCase().includes(query) ||
    e.nip.toLowerCase().includes(query) ||
    e.email.toLowerCase().includes(query) ||
    e.filiere.toLowerCase().includes(query)
  )
})

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'Actif': 'bg-green-100 text-green-800',
    'Suspendu': 'bg-red-100 text-red-800',
    'Radié': 'bg-gray-100 text-gray-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function formatStatutInscription(statut: string) {
  const colors: Record<string, string> = {
    'Confirmée': 'bg-green-100 text-green-800',
    'En attente': 'bg-yellow-100 text-yellow-800',
    'Validée': 'bg-blue-100 text-blue-800',
    'Rejetée': 'bg-red-100 text-red-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">Étudiants</h1>
        <p class="text-gray-500 mt-1">Gestion des inscriptions et dossiers académiques</p>
      </div>
      <div class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2">
          <Upload class="w-4 h-4" />
          Importer
        </button>
        <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle inscription
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Total étudiants</div>
        <div class="text-2xl font-bold text-primary mt-1">1,245</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Inscriptions 2024-2025</div>
        <div class="text-2xl font-bold text-green-600 mt-1">892</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">En attente validation</div>
        <div class="text-2xl font-bold text-yellow-600 mt-1">23</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Nouveaux inscrits</div>
        <div class="text-2xl font-bold text-blue-600 mt-1">156</div>
      </div>
    </div>

    <!-- Tabs -->
    <div class="border-b border-gray-200">
      <nav class="flex space-x-8">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="[
            'py-4 px-1 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors',
            activeTab === tab.id
              ? 'border-primary text-primary'
              : 'border-transparent text-gray-500 hover:text-gray-700'
          ]"
        >
          <component :is="tab.icon" class="w-4 h-4" />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Contenu -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-100">
      <!-- Inscriptions -->
      <div v-if="activeTab === 'inscriptions'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher un étudiant..." 
              class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" 
            />
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Filter class="w-4 h-4" />
              Filtres
            </button>
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Download class="w-4 h-4" />
              Exporter
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Étudiant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Filière</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Niveau</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Année</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Frais</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="inscription in inscriptions" :key="inscription.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4">
                  <div class="font-medium text-gray-900">{{ inscription.etudiant }}</div>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.filiere }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.niveau }}</td>
                <td class="py-3 px-4 text-sm">
                  <span :class="inscription.type === 'Nouveau' ? 'bg-blue-100 text-blue-800' : 'bg-purple-100 text-purple-800'" class="px-2 py-1 text-xs font-medium rounded">
                    {{ inscription.type }}
                  </span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ inscription.annee }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatutInscription(inscription.statut)]">
                    {{ inscription.statut }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span v-if="inscription.frais_payes" class="text-green-600">✓ Payé</span>
                  <span v-else class="text-red-500">✗ Impayé</span>
                </td>
                <td class="py-3 px-4">
                  <button class="text-primary hover:underline text-sm">Voir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Liste étudiants -->
      <div v-if="activeTab === 'dossiers'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="Rechercher..." 
              class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" 
            />
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="etudiant in etudiantsFiltres" :key="etudiant.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start gap-3 mb-3">
              <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                <span class="text-primary font-semibold">{{ etudiant.prenom[0] }}{{ etudiant.nom[0] }}</span>
              </div>
              <div class="flex-1">
                <div class="font-medium text-gray-900">{{ etudiant.prenom }} {{ etudiant.nom }}</div>
                <div class="text-sm text-gray-500">{{ etudiant.nip }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(etudiant.statut)]">
                {{ etudiant.statut }}
              </span>
            </div>
            
            <div class="space-y-2 text-sm">
              <div class="flex items-center gap-2 text-gray-600">
                <GraduationCap class="w-4 h-4 text-gray-400" />
                {{ etudiant.filiere }} - {{ etudiant.niveau }}
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <Mail class="w-4 h-4 text-gray-400" />
                {{ etudiant.email }}
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <Phone class="w-4 h-4 text-gray-400" />
                {{ etudiant.telephone }}
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-gray-100 flex gap-2">
              <button class="flex-1 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-center">
                Voir dossier
              </button>
              <button class="flex-1 px-3 py-2 text-sm bg-primary/10 text-primary hover:bg-primary/20 rounded-lg text-center">
                Notes
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Documents -->
      <div v-if="activeTab === 'documents'" class="p-6">
        <div class="text-center py-12">
          <FileText class="w-16 h-16 text-primary/20 mx-auto mb-4" />
          <h3 class="text-lg font-semibold text-gray-900 mb-2">Documents des étudiants</h3>
          <p class="text-gray-500 mb-4">Photos, pièces d'identité, bulletins, diplômes</p>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90">
            Gérer les documents
          </button>
        </div>
      </div>
    </div>
  </div>
</template>