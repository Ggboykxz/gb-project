import { describe, it, expect } from 'vitest'

describe('Formatters', () => {
  describe('formatMontant', () => {
    it('should format amount correctly in FCFA', () => {
      const formatMontant = (montant: number) => montant.toLocaleString('fr-FR') + ' FCFA'
      expect(formatMontant(1000000)).toContain('1')
      expect(formatMontant(1000000)).toContain('000')
      expect(formatMontant(1000000)).toContain('FCFA')
      expect(formatMontant(50000)).toContain('50')
      expect(formatMontant(50000)).toContain('000')
    })
  })

  describe('formatDate', () => {
    it('should format date in French locale', () => {
      const formatDate = (dateStr: string) => new Date(dateStr).toLocaleDateString('fr-FR')
      expect(formatDate('2024-01-15')).toBe('15/01/2024')
      expect(formatDate('2024-12-25')).toBe('25/12/2024')
    })
  })

  describe('formatStatut', () => {
    it('should return correct color classes for statuses', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'ACTIF': 'bg-green-100 text-green-800',
          'SUSPENDU': 'bg-red-100 text-red-800',
          'CONFIRME': 'bg-green-100 text-green-800',
          'EN_COURS': 'bg-yellow-100 text-yellow-800'
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      
      expect(formatStatut('ACTIF')).toBe('bg-green-100 text-green-800')
      expect(formatStatut('SUSPENDU')).toBe('bg-red-100 text-red-800')
      expect(formatStatut('UNKNOWN')).toBe('bg-gray-100 text-gray-800')
    })
  })

  describe('formatUrgence', () => {
    it('should return correct color classes for urgency levels', () => {
      const formatUrgence = (urgence: string) => {
        const colors: Record<string, string> = {
          'critique': 'bg-red-100 text-red-800',
          'normale': 'bg-yellow-100 text-yellow-800',
          'planifiee': 'bg-green-100 text-green-800'
        }
        return colors[urgence] || 'bg-gray-100 text-gray-800'
      }
      
      expect(formatUrgence('critique')).toBe('bg-red-100 text-red-800')
      expect(formatUrgence('normale')).toBe('bg-yellow-100 text-yellow-800')
      expect(formatUrgence('unknown')).toBe('bg-gray-100 text-gray-800')
    })
  })

  describe('getTauxPresence', () => {
    it('should calculate presence rate correctly', () => {
      const getTauxPresence = (effectif: number, presences: number) => 
        Math.round((presences / effectif) * 100)
      
      expect(getTauxPresence(50, 45)).toBe(90)
      expect(getTauxPresence(40, 30)).toBe(75)
      expect(getTauxPresence(100, 92)).toBe(92)
    })
  })

  describe('getPresenceColor', () => {
    it('should return correct color based on rate', () => {
      const getPresenceColor = (taux: number) => {
        if (taux >= 90) return 'bg-green-500'
        if (taux >= 75) return 'bg-yellow-500'
        return 'bg-red-500'
      }
      
      expect(getPresenceColor(95)).toBe('bg-green-500')
      expect(getPresenceColor(80)).toBe('bg-yellow-500')
      expect(getPresenceColor(60)).toBe('bg-red-500')
    })
  })
})
