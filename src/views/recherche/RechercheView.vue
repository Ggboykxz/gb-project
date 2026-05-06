<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  FlaskConical, 
  Search, 
  Plus, 
  Download,
  FileText,
  Users,
  Building2,
  Globe,
  Award,
  Calendar,
  TrendingUp,
  AlertCircle,
  MoreVertical,
  ExternalLink,
  Edit,
  Trash2,
  Eye
} from 'lucide-vue-next'

const activeTab = ref('projets')

const tabs = [
  { id: 'projets', label: 'Projets', icon: FlaskConical },
  { id: 'publications', label: 'Publications', icon: FileText },
  { id: 'laboratoires', label: 'Laboratoires', icon: Building2 },
  { id: 'partenariats', label: 'Partenariats', icon: Globe },
  { id: 'equipements', label: 'Équipements', icon: Award },
]

const projets = ref([
  { 
    id: 1, 
    titre: 'Système de Gestion Intelligente de l\'Énergie Solaire au Gabon',
    responsable: 'Pr. M. Ondo',
    laboratoire: 'LITIC',
    type: 'Appliquée',
    date_debut: '2024-01-15',
    date_fin: '2025-12-31',
    budget: 45000000,
    statut: 'en_cours',
    partenaires: ['USTM', 'ANINF']
  },
  { 
    id: 2, 
    titre: 'Étude de la Biodiversité du Parc National de la Lopé',
    responsable: 'Dr. N. Mba',
    laboratoire: 'LERN',
    type: 'Fondamentale',
    date_debut: '2023-06-01',
    date_fin: '2026-05-31',
    budget: 78000000,
    statut: 'en_cours',
    partenaires: ['CENAREST', 'WWF']
  },
  { 
    id: 3, 
    titre: 'Plateforme Numérique de Santé pour Zones Rurales',
    responsable: 'Pr. J. Nguéma',
    laboratoire: 'LISA',
    type: 'Développement',
    date_debut: '2024-03-01',
    date_fin: '2025-08-31',
    budget: 32000000,
    statut: 'en_cours',
    partenaires: ['Ministère Santé', 'OMS']
  },
])

const publications = ref([
  { 
    id: 1, 
    titre: 'Machine Learning for Solar Energy Prediction in Central Africa',
    auteurs: ['Ondo M.', 'Nguéma A.', 'Mouanda J.'],
    journal: 'IEEE Access',
    annee: 2024,
    doi: '10.1109/ACCESS.2024.123456',
    citations: 12,
    type: 'article'
  },
  { 
    id: 2, 
    titre: 'Biodiversity Conservation in Gabon: Challenges and Opportunities',
    auteurs: ['Mba N.', 'Obame Y.'],
    journal: 'Journal of Conservation Biology',
    annee: 2023,
    doi: '10.1111/conb.12345',
    citations: 28,
    type: 'article'
  },
  { 
    id: 3, 
    titre: 'Digital Health Solutions for Remote Areas',
    auteurs: ['Nguéma J.', 'Mouanda S.', 'Nkoghe P.'],
    journal: 'International Conference on e-Health',
    annee: 2024,
    citations: 5,
    type: 'communication'
  },
])

const laboratoires = ref([
  { 
    id: 1, 
    nom: 'Laboratoire d\'Informatique et Technologies de l\'Information et de la Communication',
    sigle: 'LITIC',
    responsable: 'Pr. M. Ondo',
    specialite: 'Intelligence Artificielle',
    budget: 25000000,
    chercheurs: 12,
    projets: 4
  },
  { 
    id: 2, 
    nom: 'Laboratoire d\'Environnement et Ressources Naturelles',
    sigle: 'LERN',
    responsable: 'Dr. N. Mba',
    specialite: 'Biodiversité',
    budget: 18000000,
    chercheurs: 8,
    projets: 3
  },
  { 
    id: 3, 
    nom: 'Laboratoire d\'Ingénierie des Systèmes et Automatique',
    sigle: 'LISA',
    responsable: 'Pr. J. Nguéma',
    specialite: 'Systèmes Embarqués',
    budget: 22000000,
    chercheurs: 10,
    projets: 5
  },
])

const partenariats = ref([
  { 
    id: 1, 
    institution: 'Université de Bordeaux',
    pays: 'France',
    type: 'Cotutelle',
    date_signature: '2022-09-15',
    date_expiration: '2027-09-14',
    responsable: 'Pr. M. Ondo',
    statut: 'actif'
  },
  { 
    id: 2, 
    institution: 'Université de Pretoria',
    pays: 'Afrique du Sud',
    type: 'Recherche',
    date_signature: '2023-03-20',
    date_expiration: '2026-03-19',
    responsable: 'Dr. N. Mba',
    statut: 'actif'
  },
  { 
    id: 3, 
    institution: 'Université de Montréal',
    pays: 'Canada',
    type: 'Formation',
    date_signature: '2021-06-10',
    date_expiration: '2026-06-09',
    responsable: 'Pr. J. Nguéma',
    statut: 'actif'
  },
])

const equipements = ref([
  { 
    id: 1, 
    nom: 'Station de mesure solaire',
    reference: 'SMS-2024-001',
    marque: 'Campbell Scientific',
    etat: 'bon',
    labo: 'LITIC',
    valeur: 15000000,
    prochaine_maintenance: '2024-12-01'
  },
  { 
    id: 2, 
    nom: 'Drone de cartographie',
    reference: 'DRN-2023-012',
    marque: 'DJI',
    etat: 'bon',
    labo: 'LERN',
    valeur: 8500000,
    prochaine_maintenance: '2024-08-15'
  },
])

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'en_cours': 'bg-green-100 text-green-800',
    'termine': 'bg-blue-100 text-blue-800',
    'suspendu': 'bg-red-100 text-red-800',
    'actif': 'bg-green-100 text-green-800',
    'expire': 'bg-gray-100 text-gray-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function formatType(type_: string) {
  const colors: Record<string, string> = {
    'article': 'bg-blue-100 text-blue-800',
    'communication': 'bg-purple-100 text-purple-800',
    'brevet': 'bg-orange-100 text-orange-800',
    'rapport': 'bg-gray-100 text-gray-800',
  }
  return colors[type_] || 'bg-gray-100 text-gray-800'
}

function formatBudget(budget: number) {
  return budget.toLocaleString() + ' FCA'
}

function formatDate(dateStr: string) {
  return new Date(dateStr).toLocaleDateString('fr-FR')
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">Recherche & Innovation</h1>
        <p class="text-gray-500 mt-1">Gestion des projets, publications et partenariats</p>
      </div>
      <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
        <Plus class="w-4 h-4" />
        Nouveau projet
      </button>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Projets actifs</div>
        <div class="text-2xl font-bold text-primary mt-1">8</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Publications</div>
        <div class="text-2xl font-bold text-blue-600 mt-1">45</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Partenariats actifs</div>
        <div class="text-2xl font-bold text-green-600 mt-1">12</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Budget total</div>
        <div class="text-2xl font-bold text-purple-600 mt-1">245M</div>
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
      <!-- Projets -->
      <div v-if="activeTab === 'projets'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher un projet..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-200 flex items-center gap-2">
            <Download class="w-4 h-4" />
            Exporter
          </button>
        </div>

        <div class="space-y-4">
          <div v-for="projet in projets" :key="projet.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h3 class="font-semibold text-gray-900">{{ projet.titre }}</h3>
                <div class="flex items-center gap-2 text-sm text-gray-500 mt-1">
                  <Users class="w-4 h-4" />
                  {{ projet.responsable }} • {{ projet.laboratoire }}
                </div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(projet.statut)]">
                {{ projet.statut === 'en_cours' ? 'En cours' : projet.statut }}
              </span>
            </div>
            
            <div class="grid grid-cols-4 gap-4 text-sm mt-3">
              <div>
                <span class="text-gray-500">Type:</span>
                <span class="ml-1 font-medium">{{ projet.type }}</span>
              </div>
              <div>
                <span class="text-gray-500">Budget:</span>
                <span class="ml-1 font-medium text-green-600">{{ formatBudget(projet.budget) }}</span>
              </div>
              <div>
                <span class="text-gray-500">Début:</span>
                <span class="ml-1 font-medium">{{ formatDate(projet.date_debut) }}</span>
              </div>
              <div>
                <span class="text-gray-500">Fin:</span>
                <span class="ml-1 font-medium">{{ formatDate(projet.date_fin) }}</span>
              </div>
            </div>

            <div class="mt-3 flex items-center gap-2">
              <span class="text-xs text-gray-500">Partenaires:</span>
              <span v-for="partenaire in projet.partenaires" :key="partenaire" 
                    class="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded">
                {{ partenaire }}
              </span>
            </div>
          </div>
        </div>

        <!-- Vue Gantt simplifiée -->
        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 class="font-medium text-gray-900 mb-4">Planning des projets</h3>
          <div class="grid grid-cols-12 gap-1 text-xs">
            <div class="col-span-2"></div>
            <div v-for="m in ['Jan','Fév','Mar','Avr','Mai','Juin','Juil','Août','Sep','Oct','Nov','Déc']" 
                 :key="m" class="text-center text-gray-500">{{ m }}</div>
            
            <div v-for="projet in projets" :key="projet.id" class="contents">
              <div class="col-span-2 text-xs text-gray-600 truncate">{{ projet.titre.substring(0,20) }}...</div>
              <div class="col-span-3 bg-green-200 rounded h-6"></div>
              <div class="col-span-3 bg-green-300 rounded h-6"></div>
              <div class="col-span-2 bg-green-200 rounded h-6"></div>
              <div class="col-span-2 bg-gray-200 rounded h-6"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Publications -->
      <div v-if="activeTab === 'publications'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher une publication..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Plus class="w-4 h-4" />
            Nouvelle publication
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Titre</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Auteurs</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Journal</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Année</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Citations</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pub in publications" :key="pub.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4">
                  <div class="font-medium text-gray-900 max-w-xs truncate">{{ pub.titre }}</div>
                  <div class="text-xs text-gray-500">{{ pub.doi }}</div>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ pub.auteurs.join(', ') }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ pub.journal }}</td>
                <td class="py-3 px-4 text-sm font-medium">{{ pub.annee }}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                    {{ pub.citations }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatType(pub.type)]">
                    {{ pub.type }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <div class="flex gap-2">
                    <button class="text-gray-400 hover:text-primary"><Eye class="w-4 h-4" /></button>
                    <button class="text-gray-400 hover:text-blue-600"><ExternalLink class="w-4 h-4" /></button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Laboratoires -->
      <div v-if="activeTab === 'laboratoires'" class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="labo in laboratoires" :key="labo.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">{{ labo.sigle }}</h3>
                <p class="text-sm text-gray-500">{{ labo.nom }}</p>
              </div>
              <span class="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Actif</span>
            </div>
            
            <div class="space-y-2 text-sm mt-4">
              <div class="flex justify-between">
                <span class="text-gray-500">Responsable:</span>
                <span class="font-medium">{{ labo.responsable }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Spécialité:</span>
                <span class="font-medium">{{ labo.specialite }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Chercheurs:</span>
                <span class="font-medium">{{ labo.chercheurs }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Budget:</span>
                <span class="font-medium text-green-600">{{ labo.budget.toLocaleString() }} FCA</span>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-gray-100 flex gap-2">
              <button class="flex-1 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-center">
                Voir détails
              </button>
              <button class="flex-1 px-3 py-2 text-sm bg-primary/10 text-primary hover:bg-primary/20 rounded-lg text-center">
                Projets
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Partenariats -->
      <div v-if="activeTab === 'partenariats'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher un partenariat..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Plus class="w-4 h-4" />
            Nouveau partenariat
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Institution</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Pays</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Signature</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Expiration</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="part in partenariats" :key="part.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ part.institution }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">
                  <span class="flex items-center gap-2">
                    <Globe class="w-4 h-4 text-gray-400" />
                    {{ part.pays }}
                  </span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ part.type }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ formatDate(part.date_signature) }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ formatDate(part.date_expiration) }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(part.statut)]">
                    {{ part.statut }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Équipements -->
      <div v-if="activeTab === 'equipements'" class="p-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="equip in equipements" :key="equip.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">{{ equip.nom }}</h3>
                <div class="text-sm text-gray-500">{{ equip.reference }} • {{ equip.marque }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(equip.etat)]">
                {{ equip.etat }}
              </span>
            </div>
            
            <div class="space-y-2 text-sm mt-4">
              <div class="flex justify-between">
                <span class="text-gray-500">Laboratoire:</span>
                <span class="font-medium">{{ equip.labo }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Valeur:</span>
                <span class="font-medium text-green-600">{{ equip.valeur.toLocaleString() }} FCA</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Prochaine maintenance:</span>
                <span class="font-medium">{{ formatDate(equip.prochaine_maintenance) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>