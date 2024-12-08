# src/components/common/Sidebar.vue
<template>
  <div class="sidebar">
    <div class="logo">
      <h2>Hashtopia</h2>
    </div>
    <el-menu
      class="sidebar-menu"
      :default-active="activeIndex"
      @select="handleSelect"
    >
      <el-menu-item index="discover">
        <el-icon><Compass /></el-icon>
        <span>Discover</span>
      </el-menu-item>
      <el-menu-item index="new-post">
        <el-icon><Plus /></el-icon>
        <span>New Post</span>
      </el-menu-item>
      <el-menu-item index="notifications">
        <el-icon><Bell /></el-icon>
        <span>Notifications</span>
      </el-menu-item>
      
      <!-- 未登录显示登录按钮 -->
      <el-menu-item v-if="!userStore.isLoggedIn" index="login" @click="handleLogin">
        <el-icon><User /></el-icon>
        <span>Login</span>
      </el-menu-item>
      
      <!-- 已登录显示用户菜单 -->
      <el-sub-menu v-else index="user" popper-class="user-dropdown">
        <template #title>
          <div class="user-menu-title">
            <img 
              :src="defaultAvatar" 
              class="user-avatar"
              alt="avatar"
            />
            <span class="username">{{ userStore.username }}</span>
          </div>
        </template>
        <el-menu-item index="profile" @click="goToProfile">
          <el-icon><User /></el-icon>
          <span>个人主页</span>
        </el-menu-item>
        <el-menu-item index="logout" @click="handleLogout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-sub-menu>
    </el-menu>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { 
  Compass,
  Plus,
  Bell,
  User,
  SwitchButton
} from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import defaultAvatar from '@/assets/default-avatar.png'

const emit = defineEmits(['show-login'])
const router = useRouter()
const userStore = useUserStore()
const activeIndex = ref('discover')

const handleSelect = (index) => {
  if (index !== 'login') {
    router.push(`/${index}`)
  }
}

const handleLogin = () => {
  emit('show-login')
}

const goToProfile = () => {
  router.push(`/profile/${userStore.username}`)
}

const handleLogout = () => {
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/')
}
</script>

<style scoped lang="scss">
.sidebar {
  height: 100%;
  background-color: var(--background-white);
  border-right: 1px solid var(--border-color);
}

.logo {
  padding: 20px;
  text-align: center;

  h2 {
    margin: 0;
    color: var(--primary-color);
    font-weight: bold;
  }
}

.sidebar-menu {
  border-right: none;

  :deep(.el-menu-item) {
    &:hover {
      background-color: rgba(255, 36, 66, 0.1);
    }

    &.is-active {
      color: var(--primary-color);
      background-color: rgba(255, 36, 66, 0.1);

      &::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 4px;
        height: 100%;
        background-color: var(--primary-color);
      }
    }
  }
}

.user-menu-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  object-fit: cover;
}

.username {
  font-size: 14px;
  color: var(--text-primary);
}

:deep(.el-menu-item) {
  .el-icon {
    color: var(--text-secondary);
  }

  &.is-active .el-icon {
    color: var(--primary-color);
  }
}

:deep(.el-sub-menu) {
  &.is-active {
    .el-sub-menu__title {
      color: var(--primary-color);
    }
  }
}

// 用户下拉菜单样式
:deep(.user-dropdown) {
  .el-menu {
    border: none;
  }

  .el-menu-item {
    height: 40px;
    line-height: 40px;
  }
}
</style>