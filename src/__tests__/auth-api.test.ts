import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { login, setToken, getToken, removeToken, getCurrentUser, fetchWithAuth } from '@/api/auth'

const mockLocalStorage = {
  store: {} as Record<string, string>,
  getItem: vi.fn((key: string) => mockLocalStorage.store[key] || null),
  setItem: vi.fn((key: string, value: string) => { mockLocalStorage.store[key] = value }),
  removeItem: vi.fn((key: string) => { delete mockLocalStorage.store[key] }),
  clear: vi.fn(() => { mockLocalStorage.store = {} })
}

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage,
  writable: true
})

const mockFetch = vi.fn()
global.fetch = mockFetch

describe('Auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    mockLocalStorage.clear()
  })

  afterEach(() => {
    mockLocalStorage.clear()
  })

  describe('setToken', () => {
    it('should set auth_token in localStorage', () => {
      setToken('test-token-123')
      expect(mockLocalStorage.setItem).toHaveBeenCalledWith('auth_token', 'test-token-123')
    })
  })

  describe('getToken', () => {
    it('should return token from localStorage', () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      expect(getToken()).toBe('my-token')
    })

    it('should return null when no token', () => {
      expect(getToken()).toBeNull()
    })
  })

  describe('removeToken', () => {
    it('should remove token from localStorage', () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      removeToken()
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('auth_token')
    })
  })

  describe('login', () => {
    it('should call API with correct credentials', async () => {
      const mockResponse = {
        ok: true,
        json: () => Promise.resolve({ access_token: 'test-token' })
      }
      mockFetch.mockResolvedValue(mockResponse)
      
      const result = await login('test@cuk.ga', 'password123')
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://127.0.0.1:8765/api/v1/auth/login',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })
      )
      expect(result.access_token).toBe('test-token')
    })

    it('should throw error on failed login', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ detail: 'Invalid credentials' })
      })
      
      await expect(login('test@cuk.ga', 'wrong')).rejects.toThrow('Invalid credentials')
    })
  })

  describe('getCurrentUser', () => {
    it('should fetch current user data', async () => {
      const mockUser = {
        id: 1,
        email: 'test@cuk.ga',
        nom: 'Test',
        prenom: 'User',
        role: 'ETUDIANT'
      }
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockUser)
      })
      
      const result = await getCurrentUser('test-token')
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://127.0.0.1:8765/api/v1/auth/me',
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer test-token'
          })
        })
      )
      expect(result).toEqual(mockUser)
    })

    it('should throw error when fetch fails', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ detail: 'Unauthorized' })
      })
      
      await expect(getCurrentUser('invalid-token')).rejects.toThrow('Failed to get user')
    })
  })

  describe('fetchWithAuth', () => {
    it('should add authorization header', async () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) })
      
      await fetchWithAuth('http://example.com/data')
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://example.com/data',
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer my-token'
          })
        })
      )
    })

    it('should throw error if no token', async () => {
      await expect(fetchWithAuth('http://example.com/data')).rejects.toThrow('No auth token')
    })
  })
})
