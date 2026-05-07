<script setup lang="ts">
import { ref, computed } from 'vue'
import { 
  BookOpen, 
  Calendar,
  ClipboardList,
  GraduationCap,
  Users,
  MapPin,
  FileText,
  Download,
  Plus,
  Search,
  ChevronLeft,
  ChevronRight,
  AlertCircle
} from 'lucide-vue-next'

const activeTab = ref('cours')

const tabs = [
  { id: 'cours', label: 'Cours & Présences', icon: BookOpen },
  { id: 'maquettes', label: 'Maquettes', icon: ClipboardList },
  { id: 'notes', label: 'Notes & Délibérations', icon: GraduationCap },
  { id: 'edt', label: 'Emploi du temps', icon: Calendar },
]

const cours = ref([
  { 
    id: 1, 
    ue: 'Algorithmique Avancée', 
    type: 'CM', 
    enseignant: 'Pr. Mfouba',
    groupe: 'L3 Info',
    salle: 'Amphi A',
    jour: 'Lundi',
    heure: '08:00-10:00',
    effectif: 45,
    presences: 42
  },
  { 
    id: 2, 
    ue: 'Droit des Obligations', 
    type: 'TD', 
    enseignant: 'Me. Nzamba',
    groupe: 'L2 Droit',
    salle: 'Salle 12',
    jour: 'Lundi',
    heure: '10:30-12:30',
    effectif: 30,
    presences: 28
  },
  { 
    id: 3, 
    ue: 'Macroéconomie', 
    type: 'CM', 
    enseignants: 'Pr. Bounda',
    groupe: 'M1 Éco',
    salle: 'Amphi B',
    jour: 'Mardi',
    heure: '14:00-16:00',
    effectif: 38,
    presences: 35
  },
])

const maquettes = ref([
  { 
    id: 1, 
    filiere: 'Informatique', 
    niveau: 'L3',
    annee: '2024-2025',
    semestre: 'S5',
    ue_count: 6,
    credits: 30,
    statut: 'Validée'
  },
  { 
    id: 2, 
    filiere: 'Droit', 
    niveau: 'L2',
    annee: '2024-2025',
    semestre: 'S3',
    ue_count: 5,
    credits: 30,
    statut: 'Brouillon'
  },
  { 
    id: 3, 
    filiere: 'Sciences Économiques', 
    niveau: 'M1',
    annee: '2024-2025',
    semestre: 'S1',
    ue_count: 4,
    credits: 30,
    statut: 'Validée'
  },
])

const notes = ref([
{ 
    id: 1, 
    ue: 'Base de Données', 
    type: 'Examen',
    moyenne: 12.5,
    max: 18,
    min: 6,
    saisie: '80%',
    statut: 'En cours'
  },
  { 
    id: 2, 
    ue: 'Programmation Web', 
    type: 'CC',
    moyenne: 14.2,
    max: 19,
    min: 8,
    saisie: '100%',
    statut: 'Validée'
  },
  { 
    id: 2, 
    ue: 'Programmation Web', 
    type: 'CC',
    moyenne: 14.2,
   最高分: 19,
   最低分: 8,
    saisie: '100%',
    statut: 'Validée'
  },
])

constEDULET = ref([
  { 
    id: 1, 
    jour: 'Lundi', 
    creneaux: [
      { heure: '08:00-10:00', ue: 'Algorithmique', type: 'CM', salle: 'Amphi A', groupe: 'L3 Info' },
      { heure: '10:30-12:30', ue: 'Droit des Obligations', type: 'TD', salle: 'Salle 12', groupe: 'L2 Droit' },
      { heure: '14:00-16:00', ue: 'Anglais', type: 'TD', salle: 'Salle 5', groupe: 'L1' },
    ]
  },
  { 
    id: 2, 
    jour: 'Mardi', 
    creneaux: [
      { heure: '08:00-10:00', ue: 'Systèmes d\'information', type: 'CM', salle: 'Amphi B', groupe: 'L3 Info' },
      { heure: '10:30-12:30', ue: 'Macroéconomie', type: 'CM', salle: 'Amphi B', groupe: 'M1 Éco' },
    ]
  },
  { 
    id: 3, 
    jour: 'Mercredi', 
    creneaux: [
      { heure: '08:00-10:00', ue: 'Statistiques', type: 'TD', salle: 'Salle 8', groupe: 'L2 Éco' },
      { heure: '14:00-16:00', ue: 'Projet Tutoré', type: 'TP', salle: 'Labo Info', groupe: 'M2 Info' },
    ]
  },
  { 
    id: 4, 
    jour: 'Jeudi', 
    creneaux: [
      { heure: '10:30-12:30', ue: 'Droit Commercial', type: 'CM', salle: 'Amphi A', groupe: 'L3 Droit' },
      { heure: '14:00-16:00', ue: 'Communication', type: 'TD', salle: 'Salle 3', groupe: 'L1' },
    ]
  },
  { 
    id: 5, 
    jour: 'Vendredi', 
    creneaux: [
      { heure: '08:00-10:00', ue: 'Recherche Documentaire', type: 'TD', salle: 'Bibliothèque', groupe: 'M1' },
    ]
  },
])

const selectedDay = ref(0)
const jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']

function formatStatut(statut: string) {
  const colors: Record<string, string> = {
    'Validée': 'bg-green-100 text-green-800',
    'Brouillon': 'bg-yellow-100 text-yellow-800',
    'En cours': 'bg-blue-100 text-blue-800',
    'Archivée': 'bg-gray-100 text-gray-800',
  }
  return colors[statut] || 'bg-gray-100 text-gray-800'
}

function getTauxPresence(effectif: number, presences: number): number {
  return Math.round((presences / effectif) * 100)
}

function getPresenceColor(taux: number): string {
  if (taux >= 90) return 'bg-green-500'
  if (taux >= 75) return 'bg-yellow-500'
  return 'bg-red-500'
}
</script>

<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-heading font-bold text-gray-900">Pédagogie</h1>
        <p class="text-gray-500 mt-1">Gestion des cours, maquettes et notes</p>
      </div>
      <div class="flex gap-3">
        <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50 flex items-center gap-2">
          <Download class="w-4 h-4" />
          Exporter
        </button>
        <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
          <Plus class="w-4 h-4" />
          Nouveau cours
        </button>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Cours aujourd'hui</div>
        <div class="text-2xl font-bold text-primary mt-1">6</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Taux présence moyen</div>
        <div class="text-2xl font-bold text-green-600 mt-1">92%</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Notes saisies</div>
        <div class="text-2xl font-bold text-blue-600 mt-1">78%</div>
      </div>
      <div class="bg-white rounded-lg shadow-sm border border-gray-100 p-4">
        <div class="text-sm text-gray-500">Maquettes validées</div>
        <div class="text-2xl font-bold text-purple-600 mt-1">12/15</div>
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
              ? 'border-[#1B4F72] text-[#1B4F72]'
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
      <!-- Cours & Présences -->
      <div v-if="activeTab === 'cours'" class="p-6">
        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">UE</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Enseignant</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Groupe</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Salle</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Horaire</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Présence</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="c in cours" :key="c.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ c.ue }}</td>
                <td class="py-3 px-4">
                  <span class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">{{ c.type }}</span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ c.enseignant }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ c.groupe }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ c.salle }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ c.jour }} {{ c.heure }}</td>
                <td class="py-3 px-4">
                  <div class="flex items-center gap-2">
                    <div class="w-24 bg-gray-200 rounded-full h-2">
                      <div :class="['h-2 rounded-full', getPresenceColor(getTauxPresence(c.effectif, c.presences))]" 
                           :style="{ width: `${getTauxPresence(c.effectif, c.presences)}%` }"></div>
                    </div>
                    <span class="text-xs text-gray-500">{{ c.presences }}/{{ c.effectif }}</span>
                  </div>
                </td>
                <td class="py-3 px-4">
                  <button class="text-primary hover:underline text-sm">Prendre présence</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-2 text-sm text-gray-600">
            <FileText class="w-4 h-4" />
            <span>QR Code de présence généré automatiquement au début de chaque cours</span>
          </div>
        </div>
      </div>

      <!-- Maquettes pédagogiques -->
      <div v-if="activeTab === 'maquettes'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex gap-2">
            <button class="px-3 py-2 text-sm bg-primary text-white rounded-lg">L3</button>
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">L2</button>
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">L1</button>
            <button class="px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">M1</button>
          </div>
          <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
            <Plus class="w-4 h-4" />
            Nouvelle maquette
          </button>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div v-for="maq in maquettes" :key="maq.id" 
               class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="font-semibold text-gray-900">{{ maq.filiere }}</h3>
                <div class="text-sm text-gray-500">{{ maq.niveau }} - {{ maq.semestre }}</div>
              </div>
              <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(maq.statut)]">
                {{ maq.statut }}
              </span>
            </div>
            <div class="space-y-2 text-sm text-gray-600">
              <div class="flex justify-between">
                <span>Année:</span>
                <span class="font-medium">{{ maq.annee }}</span>
              </div>
              <div class="flex justify-between">
                <span>UE:</span>
                <span class="font-medium">{{ maq.ue_count }}</span>
              </div>
              <div class="flex justify-between">
                <span>Crédits:</span>
                <span class="font-medium">{{ maq.credits }}</span>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-gray-100 flex gap-2">
              <button class="flex-1 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg text-center">
                Modifier
              </button>
              <button class="flex-1 px-3 py-2 text-sm bg-primary/10 text-primary hover:bg-primary/20 rounded-lg text-center">
                Voir détail
              </button>
            </div>
          </div>
        </div>

        <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <div class="flex items-center gap-2">
            <AlertCircle class="w-5 h-5 text-blue-600" />
            <span class="text-sm text-blue-800">Drag-and-drop pour réorganiser les UE. Alerte automatique si crédits ≠ 30/semestre</span>
          </div>
        </div>
      </div>

      <!-- Notes -->
      <div v-if="activeTab === 'notes'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="relative w-80">
            <Search class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input type="text" placeholder="Rechercher une UE..." 
                   class="w-full pl-10 pr-4 py-2 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-primary" />
          </div>
          <div class="flex gap-3">
            <button class="px-4 py-2 bg-white border border-gray-200 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50">
              Générer PV Jury
            </button>
            <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90">
              Saisir notes
            </button>
          </div>
        </div>

        <div class="overflow-x-auto">
          <table class="w-full">
            <thead>
              <tr class="border-b border-gray-200">
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">UE</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Type</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Moyenne</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Max</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Min</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Saisie</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Statut</th>
                <th class="text-left py-3 px-4 text-sm font-medium text-gray-500">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="note in notes" :key="note.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="py-3 px-4 font-medium text-gray-900">{{ note.ue }}</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ note.type }}</td>
                <td class="py-3 px-4 text-sm font-medium text-gray-900">{{ note.moyenne }}/20</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ note.max }}/20</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ note.min }}/20</td>
                <td class="py-3 px-4 text-sm text-gray-600">{{ note.saisie }}</td>
                <td class="py-3 px-4">
                  <span :class="['px-2 py-1 text-xs font-medium rounded-full', formatStatut(note.statut)]">
                    {{ note.statut }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <button class="text-primary hover:underline text-sm">Modifier</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="p-4 bg-green-50 rounded-lg border border-green-200">
            <div class="text-sm text-green-800 font-medium">Validation automatique</div>
            <div class="text-xs text-green-600 mt-1">Moyenne ≥ 10 = UE validée</div>
          </div>
          <div class="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <div class="text-sm text-blue-800 font-medium">Compensation inter-UE</div>
            <div class="text-xs text-blue-600 mt-1">Moyenne générale ≥ 10 valide tout</div>
          </div>
          <div class="p-4 bg-yellow-50 rounded-lg border border-yellow-200">
            <div class="text-sm text-yellow-800 font-medium">Rattrapage</div>
            <div class="text-xs text-yellow-600 mt-1">Session 2 pour UE non validées</div>
          </div>
        </div>
      </div>

      <!-- Emploi du temps -->
      <div v-if="activeTab === 'edt'" class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-4">
            <button @click="selectedDay = Math.max(0, selectedDay - 1)" class="p-2 hover:bg-gray-100 rounded-lg">
              <ChevronLeft class="w-5 h-5" />
            </button>
            <div class="flex gap-2">
              <button v-for="(jour, idx) in jours" :key="idx"
                      @click="selectedDay = idx"
                      :class="[
                        'px-4 py-2 text-sm rounded-lg font-medium transition-colors',
                        selectedDay === idx 
                          ? 'bg-[#1B4F72] text-white' 
                          : 'border border-gray-200 hover:bg-gray-50'
                      ]">
                {{ jour }}
              </button>
            </div>
            <button @click="selectedDay = Math.min(jours.length - 1, selectedDay + 1)" class="p-2 hover:bg-gray-100 rounded-lg">
              <ChevronRight class="w-5 h-5" />
            </button>
          </div>
          <div class="flex gap-2">
            <select class="px-3 py-2 border border-gray-200 rounded-lg text-sm">
              <option>Toutes les filières</option>
              <option>Informatique</option>
              <option>Droit</option>
              <option>Sciences Économiques</option>
            </select>
            <button class="px-4 py-2 bg-primary text-white rounded-lg text-sm font-medium hover:bg-primary/90 flex items-center gap-2">
              <Download class="w-4 h-4" />
              Exporter PDF
            </button>
          </div>
        </div>

        <div class="space-y-3">
          <div v-if="EDULET[selectedDay]" :key="EDULET[selectedDay].id">
            <h3 class="font-medium text-gray-900 mb-3">{{ EDULET[selectedDay].jour }}</h3>
            <div class="space-y-2">
              <div v-for="creneau in EDULET[selectedDay].creneaux" :key="creneau.heure" 
                   class="flex items-center gap-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                <div class="w-24 text-sm font-medium text-gray-600">{{ creneau.heure }}</div>
                <div class="flex-1">
                  <div class="font-medium text-gray-900">{{ creneau.ue }}</div>
                  <div class="text-sm text-gray-500">{{ creneau.groupe }}</div>
                </div>
                <div class="flex items-center gap-4 text-sm text-gray-600">
                  <span class="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">{{ creneau.type }}</span>
                  <span class="flex items-center gap-1">
                    <MapPin class="w-4 h-4" />
                    {{ creneau.salle }}
                  </span>
                </div>
              </div>
              <div v-if="EDULET[selectedDay].creneaux.length === 0" class="text-center py-8 text-gray-500">
                Aucun cours prévu
              </div>
            </div>
          </div>
        </div>

        <div class="mt-6 p-4 bg-gray-50 rounded-lg">
          <div class="flex items-center gap-4 text-sm">
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 bg-blue-500 rounded"></div>
              <span class="text-gray-600">CM</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 bg-green-500 rounded"></div>
              <span class="text-gray-600">TD</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 bg-purple-500 rounded"></div>
              <span class="text-gray-600">TP</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>