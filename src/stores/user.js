// src/stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = 'http://localhost:5001/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
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
        localStorage.setItem('user', JSON.stringify(response.data.user))
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
      } catch (error) {
        throw new Error(error.response?.data?.error || 'Login failed')
      }
    },

    async register(userData) {
      try {
        const response = await axios.post(`${API_URL}/auth/register`, userData)
        this.token = response.data.token
        this.user = response.data.user
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`
      } catch (error) {
        throw new Error(error.response?.data?.error || 'Registration failed')
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      delete axios.defaults.headers.common['Authorization']
    },

    async checkAuth() {
      if (!this.token) return false

      try {
        const response = await axios.get(`${API_URL}/auth/verify`)
        this.user = response.data.user
        localStorage.setItem('user', JSON.stringify(response.data.user))
        return true
      } catch (error) {
        this.logout()
        return false
      }
    },

    // 初始化方法，在应用启动时调用
    initializeAuth() {
      const token = localStorage.getItem('token')
      if (token) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      }
    }
  },
})

// 创建一个插件来自动初始化认证状态
export function createAuthPlugin() {
  return {
    install(app) {
      const userStore = useUserStore()
      userStore.initializeAuth()
    }
  }
}
