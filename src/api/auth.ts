import { ref } from 'vue'

const API_BASE = 'http://127.0.0.1:8765/api/v1'

interface LoginResponse {
  access_token: string
  refresh_token?: string
  token_type: string
  expires_in: number
}

interface UserProfile {
  id: number
  email: string
  nom: string
  prenom: string
  role: string
}

export async function login(email: string, password: string): Promise<LoginResponse> {
  const formData = new URLSearchParams()
  formData.append('username', email)
  formData.append('password', password)

  const response = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'Login failed' }))
    throw new Error(error.detail || 'Login failed')
  }

  return response.json()
}

export async function getCurrentUser(token: string): Promise<UserProfile> {
  const response = await fetch(`${API_BASE}/auth/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error('Failed to get user')
  }

  return response.json()
}

export function setToken(token: string) {
  localStorage.setItem('auth_token', token)
}

export function getToken(): string | null {
  return localStorage.getItem('auth_token')
}

export function removeToken() {
  localStorage.removeItem('auth_token')
}

export async function fetchWithAuth(url: string, options: RequestInit = {}) {
  const token = getToken()
  if (!token) {
    throw new Error('No auth token')
  }
  const headers = {
    ...options.headers,
    Authorization: `Bearer ${token}`,
  }
  
  const response = await fetch(url, { ...options, headers })
  
  if (response.status === 401) {
    removeToken()
    window.location.href = '/login'
  }
  
  return response
}