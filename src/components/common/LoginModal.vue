<!-- src/components/common/LoginModal.vue -->
<template>
  <el-dialog
    v-model="visible"
    :show-close="false"
    :modal="true"
    custom-class="login-container"
    width="800px"
  >
    <div class="login-wrapper">
      <!-- Left side - Image/Welcome -->
      <div class="login-left">
        <img src="@/assets/logo.png" alt="Welcome" class="login-image">
        <div class="welcome-text">
          <h2>Welcome Back</h2>
          <p>Share your wonderful moments with friends</p>
        </div>
      </div>

      <!-- Right side - Login Form -->
      <div class="login-right">
        <div class="form-header">
          <h3>{{ isLogin ? 'Login' : 'Register' }}</h3>
          <div class="close-icon" @click="closeDialog">
            <el-icon><Close /></el-icon>
          </div>
        </div>

        <el-form 
          :model="form" 
          :rules="rules"
          ref="formRef"
          label-position="top"
          class="login-form"
          @submit.prevent="handleSubmit"
        >
          <el-form-item 
            label="Email" 
            prop="email" 
            v-if="!isLogin"
          >
            <el-input 
              v-model="form.email" 
              placeholder="Enter your email"
            />
          </el-form-item>

          <el-form-item 
            label="Username" 
            prop="username"
          >
            <el-input 
              v-model="form.username" 
              placeholder="Enter your username"
            />
          </el-form-item>

          <el-form-item 
            label="Password" 
            prop="password"
          >
            <el-input 
              v-model="form.password" 
              type="password" 
              placeholder="Enter your password"
              show-password
            />
          </el-form-item>

          <el-alert
            v-if="error"
            :title="error"
            type="error"
            show-icon
            class="form-error"
            @close="error = ''"
          />

          <el-button 
            type="primary" 
            class="submit-btn" 
            @click="handleSubmit"
            :loading="loading"
          >
            {{ isLogin ? 'Login' : 'Register' }}
          </el-button>

          <div class="switch-mode">
            <span @click="toggleMode">
              {{ isLogin ? 'New user? Create an account' : 'Already have an account? Login' }}
            </span>
          </div>
        </el-form>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue'
import { Close } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const props = defineProps({
  modelValue: Boolean
})

const emit = defineEmits(['update:modelValue'])
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const isLogin = ref(true)
const error = ref('')
const visible = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const form = ref({
  email: '',
  username: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: 'Please enter email', trigger: 'blur' },
    { type: 'email', message: 'Please enter valid email', trigger: 'blur' }
  ],
  username: [
    { required: true, message: 'Please enter username', trigger: 'blur' },
    { min: 3, message: 'Minimum 3 characters', trigger: 'blur' }
  ],
  password: [
    { required: true, message: 'Please enter password', trigger: 'blur' },
    { min: 6, message: 'Minimum 6 characters', trigger: 'blur' }
  ]
}

const toggleMode = () => {
  isLogin.value = !isLogin.value
  form.value = {
    email: '',
    username: '',
    password: ''
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  error.value = ''
  
  try {
    await formRef.value.validate()
    loading.value = true
    
    if (isLogin.value) {
      await userStore.login(form.value)
      ElMessage.success('Welcome back to Hashtopia!')
    } else {
      await userStore.register(form.value)
      ElMessage.success('Welcome to Hashtopia!')
    }
    
    visible.value = false
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

const closeDialog = () => {
  visible.value = false
}
</script>

<style scoped>
.login-container {
  background: var(--background-white);
  border-radius: 16px;
  box-shadow: var(--box-shadow);
  height: 480px;
  width: 800px;
  padding: 0 !important;
  overflow: hidden;
}

.login-wrapper {
  display: flex;
  height: 100%;
}

.login-left {
  display: grid;
  place-items: center; 
  position: relative;
  width: 50%;
  overflow: hidden;
  padding-right: 20px;
}

.login-image {
  margin-bottom: 30%;
  width: 50%;
  height: auto;
}

.welcome-text {
  position: absolute;
  bottom: 40px;
  left: 30px;
  color: red;
}

.welcome-text h2 {
  margin: 0;
  font-size: 24px;
  margin-bottom: 8px;
}

.welcome-text p {
  margin: 0;
  font-size: 16px;
}

.login-right {
  width: 50%;
  padding: 30px;
  position: relative;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.form-header h3 {
  margin: 0;
  font-size: 24px;
  color: #333;
}

.close-icon {
  cursor: pointer;
  padding: 8px;
}

.login-form {
  max-width: 320px;
  margin: 0 auto;
}

.submit-btn {
  width: 100%;
  height: 40px;
  margin-top: 20px;
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.submit-btn:hover {
  background-color: var(--primary-hover);
  border-color: var(--primary-hover);
}

.switch-mode {
  text-align: center;
  margin-top: 16px;
  color: var(--primary-color);
  cursor: pointer;
}

.switch-mode:hover {
  text-decoration: underline;
}

:deep(.el-dialog__header),
:deep(.el-dialog__body) {
  padding: 0;
  margin: 0;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}
</style>