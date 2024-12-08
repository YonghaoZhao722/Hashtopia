<!-- src/App.vue -->
<template>
  <div class="app-container">
    <Sidebar class="sidebar" @show-login="showLogin = true" />
    <div class="main-content">
      <div class="search-container">
        <el-input
          v-model="searchQuery"
          placeholder="Search posts"
          :prefix-icon="Search"
          class="search-input"
        />
      </div>
      <router-view />
    </div>
    <LoginModal v-model="showLogin" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search } from '@element-plus/icons-vue'
import Sidebar from './components/common/Sidebar.vue'
import LoginModal from './components/common/LoginModal.vue'

const searchQuery = ref('')
const showLogin = ref(false)
</script>

<style lang="scss">
@import '@/styles/variables.scss';

body {
  background-color: var(--background-white);
  color: var(--text-primary);
}

.el-button--primary {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
  
  &:hover {
    background-color: var(--primary-hover);
    border-color: var(--primary-hover);
  }
  
  &:active {
    background-color: var(--primary-active);
    border-color: var(--primary-active);
  }
}

html, body {
  margin: 0;
  padding: 0;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.app-container {
  display: flex;
  height: 100vh;
  width: 100vw;
  background-color: #f5f5f5;
}

.sidebar {
  width: 240px;
  min-width: 240px;
  height: 100vh;
  border-right: 1px solid #e6e6e6;
  background-color: white;
}

.main-content {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  padding: 20px;
}

.search-container {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  position: sticky;
  top: 0;
  background-color: #f5f5f5;
  z-index: 1;
}

.search-input {
  width: 400px;
  max-width: 90%;
}
</style>