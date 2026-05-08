import { describe, it, expect } from 'vitest'

describe('Validation', () => {
  describe('Email validation', () => {
    it('should validate email format', () => {
      const isValidEmail = (email: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return emailRegex.test(email)
      }
      
      expect(isValidEmail('test@cuk.ga')).toBe(true)
      expect(isValidEmail('user@domain.com')).toBe(true)
      expect(isValidEmail('invalid-email')).toBe(false)
      expect(isValidEmail('@cuk.ga')).toBe(false)
    })
  })

  describe('Password validation', () => {
    it('should validate password is not empty', () => {
      const isValidPassword = (password: string) => password.length > 0
      expect(isValidPassword('password123')).toBe(true)
      expect(isValidPassword('')).toBe(false)
    })
  })

  describe('NIP Gabon validation', () => {
    it('should validate NIP Gabon format', () => {
      const isValidNIP = (nip: string) => {
        return nip && nip.length >= 6 && /^[A-Z0-9]+$/.test(nip)
      }
      
      expect(isValidNIP('123456')).toBe(true)
      expect(isValidNIP('ABC123')).toBe(true)
      expect(isValidNIP('12345')).toBe(false)
      expect(isValidNIP('abc123')).toBe(false)
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
      expect(isValidPhone('12345')).toBe(false)
    })
  })
})
