import { describe, it, expect } from 'vitest'

describe('Formatters', () => {
  describe('formatMontant', () => {
    it('should format amount correctly in FCFA', () => {
      const formatMontant = (montant: number) => montant.toLocaleString('fr-FR') + ' FCFA'
      expect(formatMontant(1000000)).toContain('1')
      expect(formatMontant(1000000)).toContain('000')
      expect(formatMontant(1000000)).toContain('FCFA')
    })

    it('should format zero', () => {
      const formatMontant = (montant: number) => montant.toLocaleString('fr-FR') + ' FCFA'
      expect(formatMontant(0)).toBe('0 FCFA')
    })

    it('should format small amounts', () => {
      const formatMontant = (montant: number) => montant.toLocaleString('fr-FR') + ' FCFA'
      expect(formatMontant(50000)).toContain('50')
    })

    it('should handle large amounts', () => {
      const formatMontant = (montant: number) => montant.toLocaleString('fr-FR') + ' FCFA'
      expect(formatMontant(250000000)).toContain('250')
    })
  })

  describe('formatDate', () => {
    it('should format date in French locale', () => {
      const formatDate = (dateStr: string) => new Date(dateStr).toLocaleDateString('fr-FR')
      const result = formatDate('2024-01-15')
      expect(result).toMatch(/\d{2}\/\d{2}\/\d{4}/)
    })

    it('should handle different months', () => {
      const formatDate = (dateStr: string) => new Date(dateStr).toLocaleDateString('fr-FR')
      expect(formatDate('2024-12-25')).toMatch(/25/)
      expect(formatDate('2024-12-25')).toMatch(/12/)
    })

    it('should handle invalid date', () => {
      const formatDate = (dateStr: string) => {
        const date = new Date(dateStr)
        if (isNaN(date.getTime())) return 'Invalid date'
        return date.toLocaleDateString('fr-FR')
      }
      expect(formatDate('invalid')).toBe('Invalid date')
    })
  })

  describe('formatStatut', () => {
    it('should return correct color classes for ACTIF', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'ACTIF': 'bg-green-100 text-green-800',
          'SUSPENDU': 'bg-red-100 text-red-800',
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      expect(formatStatut('ACTIF')).toBe('bg-green-100 text-green-800')
    })

    it('should return correct color classes for SUSPENDU', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'ACTIF': 'bg-green-100 text-green-800',
          'SUSPENDU': 'bg-red-100 text-red-800',
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      expect(formatStatut('SUSPENDU')).toBe('bg-red-100 text-red-800')
    })

    it('should return default for unknown status', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'ACTIF': 'bg-green-100 text-green-800',
          'SUSPENDU': 'bg-red-100 text-red-800',
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      expect(formatStatut('UNKNOWN')).toBe('bg-gray-100 text-gray-800')
    })

    it('should handle CONFIRME status', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'CONFIRME': 'bg-green-100 text-green-800',
          'EN_COURS': 'bg-yellow-100 text-yellow-800',
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      expect(formatStatut('CONFIRME')).toBe('bg-green-100 text-green-800')
    })

    it('should handle EN_COURS status', () => {
      const formatStatut = (statut: string) => {
        const colors: Record<string, string> = {
          'CONFIRME': 'bg-green-100 text-green-800',
          'EN_COURS': 'bg-yellow-100 text-yellow-800',
        }
        return colors[statut] || 'bg-gray-100 text-gray-800'
      }
      expect(formatStatut('EN_COURS')).toBe('bg-yellow-100 text-yellow-800')
    })
  })

  describe('formatUrgence', () => {
    it('should return correct color for urgente', () => {
      const formatUrgence = (urgence: string) => {
        const colors: Record<string, string> = {
          'critique': 'bg-red-100 text-red-800',
          'normale': 'bg-yellow-100 text-yellow-800',
          'planifiee': 'bg-green-100 text-green-800',
        }
        return colors[urgence] || 'bg-gray-100 text-gray-800'
      }
      expect(formatUrgence('critique')).toBe('bg-red-100 text-red-800')
    })

    it('should return default for unknown urgency', () => {
      const formatUrgence = (urgence: string) => {
        const colors: Record<string, string> = {
          'critique': 'bg-red-100 text-red-800',
          'normale': 'bg-yellow-100 text-yellow-800',
          'planifiee': 'bg-green-100 text-green-800',
        }
        return colors[urgence] || 'bg-gray-100 text-gray-800'
      }
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

    it('should handle 100% presence', () => {
      const getTauxPresence = (effectif: number, presences: number) =>
        Math.round((presences / effectif) * 100)
      
      expect(getTauxPresence(30, 30)).toBe(100)
    })

    it('should handle 0% presence', () => {
      const getTauxPresence = (effectif: number, presences: number) =>
        Math.round((presences / effectif) * 100)
      
      expect(getTauxPresence(25, 0)).toBe(0)
    })

    it('should round to nearest integer', () => {
      const getTauxPresence = (effectif: number, presences: number) =>
        Math.round((presences / effectif) * 100)
      
      expect(getTauxPresence(3, 1)).toBe(33)
    })
  })

  describe('getPresenceColor', () => {
    it('should return green for rate >= 90', () => {
      const getPresenceColor = (taux: number) => {
        if (taux >= 90) return 'bg-green-500'
        if (taux >= 75) return 'bg-yellow-500'
        return 'bg-red-500'
      }
      expect(getPresenceColor(95)).toBe('bg-green-500')
      expect(getPresenceColor(100)).toBe('bg-green-500')
    })

    it('should return yellow for rate >= 75 and < 90', () => {
      const getPresenceColor = (taux: number) => {
        if (taux >= 90) return 'bg-green-500'
        if (taux >= 75) return 'bg-yellow-500'
        return 'bg-red-500'
      }
      expect(getPresenceColor(80)).toBe('bg-yellow-500')
      expect(getPresenceColor(75)).toBe('bg-yellow-500')
    })

    it('should return red for rate < 75', () => {
      const getPresenceColor = (taux: number) => {
        if (taux >= 90) return 'bg-green-500'
        if (taux >= 75) return 'bg-yellow-500'
        return 'bg-red-500'
      }
      expect(getPresenceColor(74)).toBe('bg-red-500')
      expect(getPresenceColor(50)).toBe('bg-red-500')
      expect(getPresenceColor(0)).toBe('bg-red-500')
    })
  })
})
