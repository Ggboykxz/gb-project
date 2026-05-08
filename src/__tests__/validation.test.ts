import { describe, it, expect } from 'vitest'

describe('Validation', () => {
  describe('Email validation', () => {
    it('should validate correct email format', () => {
      const isValidEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(email)
      }
      
      expect(isValidEmail('test@cuk.ga')).toBe(true)
      expect(isValidEmail('user@domain.com')).toBe(true)
      expect(isValidEmail('name.surname@university.edu')).toBe(true)
    })

    it('should reject invalid email format', () => {
      const isValidEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(email)
      }
      
      expect(isValidEmail('invalid-email')).toBe(false)
      expect(isValidEmail('@cuk.ga')).toBe(false)
      expect(isValidEmail('test@')).toBe(false)
      expect(isValidEmail('test@.com')).toBe(false)
      expect(isValidEmail('')).toBe(false)
    })
  })

  describe('Password validation', () => {
    it('should validate password is not empty', () => {
      const isValidPassword = (password: string) => password.length > 0
      expect(isValidPassword('password123')).toBe(true)
      expect(isValidPassword('Abc123!@#')).toBe(true)
    })

    it('should reject empty password', () => {
      const isValidPassword = (password: string) => password.length > 0
      expect(isValidPassword('')).toBe(false)
    })

    it('should validate minimum length', () => {
      const isValidPassword = (password: string) => password.length >= 8
      expect(isValidPassword('12345678')).toBe(true)
      expect(isValidPassword('1234567')).toBe(false)
    })
  })

  describe('NIP Gabon validation', () => {
    it('should validate correct NIP format', () => {
      const isValidNIP = (nip: string) => {
        return nip && nip.length >= 6 && /^[A-Z0-9]+$/.test(nip)
      }
      
      expect(isValidNIP('123456')).toBe(true)
      expect(isValidNIP('ABC123')).toBe(true)
      expect(isValidNIP('NKL123456')).toBe(true)
    })

    it('should reject invalid NIP', () => {
      const isValidNIP = (nip: string) => {
        return nip && nip.length >= 6 && /^[A-Z0-9]+$/.test(nip)
      }
      
      expect(isValidNIP('12345')).toBe(false)
      expect(isValidNIP('abc123')).toBe(false)
      expect(isValidNIP('ABC 123')).toBe(false)
    })

    it('should handle empty NIP', () => {
      const isValidNIP = (nip: string) => {
        if (!nip) return false
        return nip.length >= 6 && /^[A-Z0-9]+$/.test(nip)
      }
      
      expect(isValidNIP('')).toBe(false)
    })
  })

  describe('Phone number validation', () => {
    it('should validate Gabon phone format', () => {
      const isValidPhone = (phone: string) => {
        const phoneRegex = /^(\+241|0)?[0-9]{8,9}$/
        return phoneRegex.test(phone.replace(/\s/g, ''))
      }
      
      expect(isValidPhone('074123456')).toBe(true)
      expect(isValidPhone('+24174123456')).toBe(true)
      expect(isValidPhone('064123456')).toBe(true)
    })

    it('should reject invalid phone', () => {
      const isValidPhone = (phone: string) => {
        const phoneRegex = /^(\+241|0)?[0-9]{8,9}$/
        return phoneRegex.test(phone.replace(/\s/g, ''))
      }
      
      expect(isValidPhone('12345')).toBe(false)
      expect(isValidPhone('123456789012')).toBe(false)
    })
  })

  describe('Date validation', () => {
    it('should validate correct date format', () => {
      const isValidDate = (dateStr: string) => {
        const date = new Date(dateStr)
        return !isNaN(date.getTime())
      }
      
      expect(isValidDate('2024-01-15')).toBe(true)
      expect(isValidDate('2024-12-25')).toBe(true)
      expect(isValidDate('1990-05-20')).toBe(true)
    })

    it('should reject invalid date', () => {
      const isValidDate = (dateStr: string) => {
        const date = new Date(dateStr)
        return !isNaN(date.getTime())
      }
      
      expect(isValidDate('invalid')).toBe(false)
      expect(isValidDate('2024-13-01')).toBe(false)
    })
  })

  describe('Name validation', () => {
    it('should validate correct name format', () => {
      const isValidName = (name: string) => {
        return name && name.length >= 2 && /^[A-Za-zÀ-ÿ\s'-]+$/.test(name)
      }
      
      expect(isValidName('Ondo')).toBe(true)
      expect(isValidName('Nguema Marie-Claire')).toBe(true)
      expect(isValidName("O'Brien")).toBe(true)
    })

    it('should reject invalid name', () => {
      const isValidName = (name: string) => {
        if (!name || name.length < 2) return false
        return /^[A-Za-zÀ-ÿ\s'-]+$/.test(name)
      }
      
      expect(isValidName('')).toBe(false)
      expect(isValidName('A')).toBe(false)
      expect(isValidName('12345')).toBe(false)
    })
  })
})
