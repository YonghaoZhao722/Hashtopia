// src/stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:5000/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.token,
    username: (state) => state.user?.username,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await axios.post(`${API_URL}/auth/login`, credentials)
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('token', response.data.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
      } catch (error) {
        throw new Error(error.response?.data?.error || 'Login failed')
      }
    },

    async register(userData) {
      try {
        console.log('Sending register request:', userData)
        const response = await axios.post(`${API_URL}/auth/register`, userData)
        console.log('Register response:', response.data)
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('token', response.data.token)
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
      } catch (error) {
        console.error('Register error:', error.response?.data || error)
        throw new Error(error.response?.data?.error || 'Registration failed')
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      delete axios.defaults.headers.common['Authorization']
    },

    async checkAuth() {
      if (!this.token) return false
      
      try {
        // Optional: Verify token with backend
        // const response = await axios.get('/api/auth/verify')
        // this.setUser(response.data.user)
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },
  },
})