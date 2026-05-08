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

  describe('Token Management', () => {
    it('should set auth_token in localStorage', () => {
      setToken('test-token-123')
      expect(mockLocalStorage.setItem).toHaveBeenCalledWith('auth_token', 'test-token-123')
      expect(mockLocalStorage.store['auth_token']).toBe('test-token-123')
    })

    it('should get token from localStorage', () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      expect(getToken()).toBe('my-token')
    })

    it('should return null when no token exists', () => {
      expect(getToken()).toBeNull()
    })

    it('should remove token from localStorage', () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      removeToken()
      expect(mockLocalStorage.removeItem).toHaveBeenCalledWith('auth_token')
      expect(mockLocalStorage.store['auth_token']).toBeUndefined()
    })

    it('should clear all tokens', () => {
      mockLocalStorage.store['auth_token'] = 'token1'
      mockLocalStorage.store['refresh_token'] = 'token2'
      mockLocalStorage.clear()
      expect(mockLocalStorage.store).toEqual({})
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

    it('should return access_token on success', async () => {
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ 
          access_token: 'abc123',
          refresh_token: 'refresh123',
          token_type: 'Bearer',
          expires_in: 3600
        })
      })
      
      const result = await login('user@cuk.ga', 'pass')
      
      expect(result.access_token).toBe('abc123')
      expect(result.refresh_token).toBe('refresh123')
      expect(result.token_type).toBe('Bearer')
      expect(result.expires_in).toBe(3600)
    })

    it('should throw error on 401 unauthorized', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ detail: 'Invalid credentials' })
      })
      
      await expect(login('test@cuk.ga', 'wrong')).rejects.toThrow('Invalid credentials')
    })

    it('should throw error on 423 locked account', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 423,
        json: () => Promise.resolve({ detail: 'Account locked' })
      })
      
      await expect(login('test@cuk.ga', 'pass')).rejects.toThrow('Account locked')
    })

    it('should throw generic error when response has no detail', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.resolve({})
      })
      
      await expect(login('test@cuk.ga', 'pass')).rejects.toThrow('Login failed')
    })
  })

  describe('getCurrentUser', () => {
    it('should fetch current user data with token', async () => {
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

    it('should return user profile with all fields', async () => {
      const mockUser = {
        id: 42,
        email: 'admin@cuk.ga',
        nom: 'Admin',
        prenom: 'Super',
        role: 'SUPER_ADMIN'
      }
      mockFetch.mockResolvedValue({
        ok: true,
        json: () => Promise.resolve(mockUser)
      })
      
      const result = await getCurrentUser('admin-token')
      
      expect(result.id).toBe(42)
      expect(result.email).toBe('admin@cuk.ga')
      expect(result.role).toBe('SUPER_ADMIN')
    })

    it('should throw error when fetch fails', async () => {
      mockFetch.mockResolvedValue({
        ok: false,
        status: 401,
        json: () => Promise.resolve({ detail: 'Unauthorized' })
      })
      
      await expect(getCurrentUser('invalid-token')).rejects.toThrow('Failed to get user')
    })

    it('should throw error on network failure', async () => {
      mockFetch.mockRejectedValue(new Error('Network error'))
      
      await expect(getCurrentUser('token')).rejects.toThrow()
    })
  })

  describe('fetchWithAuth', () => {
    it('should add authorization header with token', async () => {
      mockLocalStorage.store['auth_token'] = 'my-token'
      mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({ data: 'test' }) })
      
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

    it('should handle custom headers in options', async () => {
      mockLocalStorage.store['auth_token'] = 'token'
      mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) })
      
      await fetchWithAuth('http://example.com/data', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key: 'value' })
      })
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://example.com/data',
        expect.objectContaining({
          method: 'POST',
          body: JSON.stringify({ key: 'value' })
        })
      )
    })

    it('should pass through other request options', async () => {
      mockLocalStorage.store['auth_token'] = 'token'
      mockFetch.mockResolvedValue({ ok: true, json: () => Promise.resolve({}) })
      
      await fetchWithAuth('http://example.com/data', {
        method: 'PUT',
        mode: 'cors',
        credentials: 'include'
      })
      
      expect(mockFetch).toHaveBeenCalledWith(
        'http://example.com/data',
        expect.objectContaining({
          method: 'PUT',
          mode: 'cors',
          credentials: 'include'
        })
      )
    })
  })
})
