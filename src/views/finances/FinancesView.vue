<script setup lang="ts">
import { ref } from 'vue'
import { 
  Banknote, 
  Receipt,
  PieChart,
  ShoppingCart,
  Building2,
  Users,
  Search,
  Plus,
  Download,
  Filter,
  Calendar,
  CheckCircle,
  AlertCircle,
  Clock,
  TrendingUp,
  TrendingDown,
  DollarSign,
  CreditCard,
  Wallet,
  FileText,
  Send,
  Building,
  Truck,
  ClipboardList,
  UserCheck
} from 'lucide-vue-next'

const activeTab = ref('recouvrement')

const tabs = [
  { id: 'recouvrement', label: 'Recouvrement', icon: Receipt },
  { id: 'budget', label: 'Budget', icon: PieChart },
  { id: 'achats', label: 'Marchés', icon: ShoppingCart },
  { id: 'patrimoine', label: 'Patrimoine', icon: Building2 },
  { id: 'rh', label: 'Ressources Humaines', icon: Users },
]

const factures = ref([
  { id: 1, etudiant: 'Mouanda Marie', filiere: 'Informatique L3', montant: 450000, statut: 'payee', date: '2024-09-15', mode: 'Mobile Money' },
  { id: 2, etudiant: 'Nkoghe Junior', filiere: 'Droit L2', montant: 350000, statut: 'impayee', date: '2024-09-01', mode: '-' },
  { id: 3, etudiant: 'Mboghe Christelle', filiere: 'Éco M1', montant: 500000, statut: 'payee', date: '2024-09-10', mode: 'Virement' },
  { id: 4, etudiant: 'Obame Yannick', filiere: 'Médecine DEMS', montant: 650000, statut: 'partiel', date: '2024-09-05', mode: 'Espèces', reste: 250000 },
])

const budgets = ref([
  { id: 1, departement: 'Informatique', annee: '2024-2025', prevu: 150000000, execute: 98000000, taux: 65 },
  { id: 2, departement: 'Droit', annee: '2024-2025', prevu: 120000000, execute: 75000000, taux: 62 },
  { id: 3, departement: 'Sciences Économiques', annee: '2024-2025', prevu: 100000000, execute: 45000000, taux: 45 },
  { id: 4, departement: 'Médecine', annee: '2024-2025', prevu: 200000000, execute: 180000000, taux: 90 },
])

const demandesAchats = ref([
  { id: 1, objet: 'Équipements informatiques', demandeur: 'Pr. Ondo', departement: 'Info', montant: 8500000, urgence: 'normale', statut: 'approuvee', date: '2024-09-20' },
  { id: 2, objet: 'Mobilier bureau', demandeur: 'Mme. Nguema', departement: 'Admin', montant: 3200000, urgence: 'planifiee', statut: 'en_cours', date: '2024-09-25' },
  { id: 3, objet: 'Produits chimiques labo', demandeur: 'Dr. Mba', departement: 'Sciences', montant: 1500000, urgence: 'critique', statut: 'soumise', date: '2024-10-01' },
])

const patrimoine = ref([
  { id: 1, designation: 'Bâtiment A - Administrative', type: 'batiment', surface: 1200, valeur: 250000000, etat: 'bon', affectation: 'Administration' },
  { id: 2, designation: 'Amphi 500 places', type: 'batiment', surface: 800, valeur: 180000000, etat: 'bon', affectation: 'Enseignement' },
  { id: 3, designation: 'Salle info 50 postes', type: 'materiel', surface: 150, valeur: 45000000, etat: 'bon', affectation: 'Informatique' },
  { id: 4, designation: ' Véhicule administratif', type: 'materiel', surface: 0, valeur: 28000000, etat: 'degrade', affectation: 'Logistique' },
])

const personnel = ref([
  { id: 1, nom: 'Ondo', prenom: 'Mathieu', type: 'Enseignant', grade: 'Professeur', departement: 'Informatique', statut: 'actif', salaire: 2500000 },
  { id: 2, nom: 'Nguéma', prenom: 'Alain', type: 'Enseignant', grade: 'Maître de conférences', departement: 'Droit', statut: 'actif', salaire: 2200000 },
  { id: 3, nom: 'Mba', prenom: 'Nadia', type: 'Administratif', grade: 'Chef service', departement: ' Scolarité', statut: 'actif', salaire: 1800000 },
  { id: 4, nom: 'Mouanda', prenom: 'Espoir', type: 'Vacataire', grade: '-', departement: 'Info', statut: 'actif', salaire: 450000 },
])

const relances = ref([
  { id: 1, etudiant: 'Nkoghe Junior', type: '1er rappel', date_envoi: '2024-10-01', canal: 'SMS', statut: 'envoyee' },
  { id: 2, etudiant: 'Obame Yannick', type: '2eme rappel', date_envoi: '2024-10-15', canal: 'Email', statut: 'envoyee' },
])

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'payee': 'bg-green-100 text-green-800',
    'impayee': 'bg-red-100 text-red-800',
    'partiel': 'bg-yellow-100 text-yellow-800',
    'approuvee': 'bg-green-100 text-green-800',
    'en_cours': 'bg-blue-100 text-blue-800',
    'soumise': 'bg-gray-100 text-gray-800',
    'rejetee': 'bg-red-100 text-red-800',
    'actif': 'bg-green-100 text-green-800',
    'conge': 'bg-yellow-100 text-yellow-800',
    'envoyee': 'bg-blue-100 text-blue-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function formatUrgence(urgence: string) {
  const colors: Record<string, string> = {
    'critique': 'bg-red-100 text-red-800',
    'normale': 'bg-yellow-100 text-yellow-800',
    'planifiee': 'bg-green-100 text-green-800',
  }
  return colors[urgence] || 'bg-gray-100 text-gray-800'
}

function formatMontant(montant: number) {
  return montant.toLocaleString() + ' FCA'
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
        <h1 class="text-2xl font-heading font-bold text-gray-900">Gestion Financière</h1>
        <p class="text-gray-500 mt-1">Facturation, budget, achats, patrimoine et RH</p>
      </div>
      <div class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2">
          <Download class="w-4 h-4" />
          Exporter
        </button>
        <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouvelle facture
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-5 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <Wallet class="w-4 h-4" />
          Recettes prévues
        </div>
        <div class="text-xl font-bold text-green-600 mt-1">570M</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <Receipt class="w-4 h-4" />
          Recettes encaissées
        </div>
        <div class="text-xl font-bold text-primary mt-1">398M</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <AlertCircle class="w-4 h-4" />
          Impayés
        </div>
        <div class="text-xl font-bold text-red-600 mt-1">172M</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <TrendingUp class="w-4 h-4" />
          Taux encaissement
        </div>
        <div class="text-xl font-bold text-blue-600 mt-1">70%</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="flex items-center gap-2 text-sm text-gray-500">
          <Users class="w-4 h-4" />
          Personnel
        </div>
        <div class="text-xl font-bold text-purple-600 mt-1">156</div>
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
      <!-- Recouvrement -->
      <div v-if="activeTab === 'recouvrement'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <div class="flex gap-2">
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 flex items-center gap-2">
              <Filter class="w-4 h-4" />
              Filtres
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Étudiant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Filière</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Montant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Date</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Mode</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="facture in factures" :key="facture.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ facture.etudiant }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ facture.filiere }}</td>
                <td class="py-3 px-4 font-semibold text-gray-900">{{ formatMontant(facture.montant) }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(facture.statut)]">
                    {{ facture.statut }}
                  </span>
                  <span v-if="facture.reste" class="block text-xs text-red-500">Restant: {{ formatMontant(facture.reste) }}</span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ formatDate(facture.date) }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ facture.mode }}</td>
                <td class="py-3 px-4">
                  <button v-if="facture.statut === 'impayee'" class="text-sm text-primary hover:underline">Relancer</button>
                  <button v-else class="text-sm text-gray-500 hover:text-gray-700">Voir</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Relances en attente -->
        <div class="mt-6 p-4 bg-yellow-50 rounded-lg border border-yellow-200">
          <h3 class="font-medium text-yellow-800 mb-3 flex items-center gap-2">
            <Clock class="w-4 h-4" />
            Relances en attente
          </h3>
          <div class="grid grid-cols-3 gap-4">
            <div v-for="relance in relances" :key="relance.id" class="bg-white p-3 rounded-lg">
              <div class="font-medium text-gray-900">{{ relance.etudiant }}</div>
              <div class="text-sm text-gray-500">{{ relance.type }} - {{ formatDate(relance.date_envoi) }}</div>
              <span :class="['mt-2 px-2 py-1 text-xs rounded-full inline-block', formatStatut(relance.statut)]">
                {{ relance.canal }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Budget -->
      <div v-if="activeTab === 'budget'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium text-gray-900">Budget par département</h3>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Plus class="w-4 h-4" />
            Nouveau budget
          </button>
        </div>

        <div class="space-y-4">
          <div v-for="budget in budgets" :key="budget.id" 
               class="border border-gray-200 rounded-lg p-4">
            <div class="flex items-center justify-between mb-2">
              <div>
                <h4 class="font-semibold text-gray-900">{{ budget.departement }}</h4>
                <div class="text-sm text-gray-500">{{ budget.annee }}</div>
              </div>
              <div class="text-right">
                <div class="text-sm text-gray-500">Exécution</div>
                <div class="text-lg font-bold text-primary">{{ budget.taux }}%</div>
              </div>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-3">
              <div class="bg-primary h-3 rounded-full transition-all" :style="{ width: budget.taux + '%' }"></div>
            </div>
            <div class="flex justify-between mt-2 text-sm">
              <span class="text-gray-500">Budget: {{ formatMontant(budget.prevu) }}</span>
              <span class="text-gray-500">Dépensé: {{ formatMontant(budget.execute) }}</span>
            </div>
          </div>
        </div>

        <div class="mt-6 grid grid-cols-2 gap-4">
          <div class="p-4 bg-green-50 rounded-lg border border-green-200">
            <h4 class="font-medium text-green-800 mb-2">Recettes</h4>
            <div class="text-2xl font-bold text-green-600">398M FCA</div>
            <div class="text-sm text-green-600">+12% vs année dernière</div>
          </div>
          <div class="p-4 bg-red-50 rounded-lg border border-red-200">
            <h4 class="font-medium text-red-800 mb-2">Dépenses</h4>
            <div class="text-2xl font-bold text-red-600">285M FCA</div>
            <div class="text-sm text-red-600">+8% vs année dernière</div>
          </div>
        </div>
      </div>

      <!-- Achats -->
      <div v-if="activeTab === 'achats'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher une demande..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <ShoppingCart class="w-4 h-4" />
            Nouvelle demande
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Objet</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Demandeur</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Département</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Montant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Urgence</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="demande in demandesAchats" :key="demande.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ demande.objet }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ demande.demandeur }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ demande.departement }}</td>
                <td class="py-3 px-4 font-semibold text-gray-900">{{ formatMontant(demande.montant) }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatUrgence(demande.urgence)]">
                    {{ demande.urgence }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(demande.statut)]">
                    {{ demande.statut }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Patrimoine -->
      <div v-if="activeTab === 'patrimoine'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="font-medium text-gray-900">Inventaire du patrimoine</h3>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Building2 class="w-4 h-4" />
            Ajouter bien
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="bien in patrimoine" :key="bien.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h4 class="font-semibold text-gray-900">{{ bien.designation }}</h4>
                <div class="text-sm text-gray-500">{{ bien.type }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(bien.etat)]">
                {{ bien.etat }}
              </span>
            </div>
            
            <div class="grid grid-cols-2 gap-2 text-sm mt-3">
              <div>
                <span class="text-gray-500">Surface:</span>
                <span class="ml-1 font-medium">{{ bien.surface }} m²</span>
              </div>
              <div>
                <span class="text-gray-500">Valeur:</span>
                <span class="ml-1 font-medium text-green-600">{{ formatMontant(bien.valeur) }}</span>
              </div>
              <div class="col-span-2">
                <span class="text-gray-500">Affectation:</span>
                <span class="ml-1 font-medium">{{ bien.affectation }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- RH -->
      <div v-if="activeTab === 'rh'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher un membre..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Users class="w-4 h-4" />
            Nouveau сотрудник
          </button>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Nom</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Grade</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Département</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Salaire</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="pers in personnel" :key="pers.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ pers.prenom }} {{ pers.nom }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ pers.type }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ pers.grade }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ pers.departement }}</td>
                <td class="py-3 px-4 font-semibold text-gray-900">{{ formatMontant(pers.salaire) }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(pers.statut)]">
                    {{ pers.statut }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>