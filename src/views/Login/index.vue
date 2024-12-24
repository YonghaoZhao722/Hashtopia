<script setup>
import {ref} from "vue";

import {ElMessage} from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import {User, Lock, ChatLineSquare} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";
import {useRouter} from "vue-router";

const emit = defineEmits(['changeShow']);
const router = useRouter()
const formLogin = ref({
  email: '',
  password: '',
  agree: false
})
const formRegister = ref({
  email: '',
  username: '',
  password: '',
  retryPwd: '',
  agree: false
})

const rulesRegister = {
  email: [
    {required: true, message: 'Email address cannot be empty', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
          var emailRegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
          if (value && !emailRegExp.test(value)) {
              callback(new Error('Please enter a valid email format!'));
          } else {
              callback();
          }
      }
    }
  ],
  username: [
    {required: true, message: 'Username cannot be empty!', trigger: 'blur'}
  ],
  password: [
    {required: true, message: 'Password cannot be empty!', trigger: 'blur'},
    {min: 6, max: 14, message: 'Password does not meet requirements', trigger: 'blur'}
  ],
  retryPwd: [
    {required: true, message: 'Confirm password cannot be empty!', trigger: 'blur'},
    {min: 6, max: 14, message: 'Comfirm password does not meet requirements', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        if (value !== formRegister.value.password) {
          callback(new Error('The two passwords do not match!'));
        } else {
          callback();
        }
      }
    }
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        if (value) {
          callback()
        } else {
          callback(new Error('Please check the agreement'))
        }
      }
    }
  ]
}
const rulesLogin = {
  email: [
    {required: true, message: 'Email address cannot be empty', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
          var emailRegExp = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
          if (value && !emailRegExp.test(value)) {
              callback(new Error('Please enter a valid email format!'));
          } else {
              callback();
          }
      }
    }
  ],
  password: [
    {required: true, message: 'Password cannot be empty!', trigger: 'blur'},
    {min: 6, max: 14, message: 'Password does not meet requirements', trigger: 'blur'}
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        // 自定义校验逻辑
        if (value) {
          callback()
        } else {
          callback(new Error('Please read the terms and conditions'))
        }
      }
    }
  ]
}

const formLoginRef = ref(null)
const formRegisterRef = ref(null)

const userStore = useUserStore();
const doLogin = () => {
  const {email, password} = formLogin.value
  formLoginRef.value.validate(async (valid) => {
    if (valid) {
      await userStore.getUserInfo({email, password})
      emit('changeShow')
      await router.replace(`/user/index/${userStore.userInfo.id}`)
      ElMessage({type: 'success', message: 'Login Successfully'})
    }
  })
}
const doRegister = () => {
  const {email, username, password} = formRegister.value
  formRegisterRef.value.validate(async (valid) => {
    if (valid) {
      await userStore.userRegister({email, username, password})
      ElMessage({type: 'success', message: 'Register Successfully'})
      toggleForm()
    }
  })
}
const showWhich = ref(true)
const toggleForm = () => {
  showWhich.value = !showWhich.value
}
</script>

<template>
  <div class="login-container">
    <div class="login-box">
      <div class="content-wrapper">
        <!-- Left Area -->
        <div class="left-area">
          <div class="title">Hashtopia</div>
          <img src="/icon.jpg" class="brand-image" alt="Hashtopia logo">
        </div>

        <!-- Right Area - Login Form -->
        <div class="right-area" v-if="showWhich">
          <div class="title">Login</div>
          <div class="form">
            <el-form ref="formLoginRef" :model="formLogin" :rules="rulesLogin" label-position="right" label-width="0" status-icon>
              <el-form-item prop="email" class="input-item">
                <el-input v-model="formLogin.email" placeholder="Please enter your email address" :prefix-icon="User"/>
              </el-form-item>
              <el-form-item prop="password" class="input-item">
                <el-input v-model="formLogin.password" placeholder="Please enter your password" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="agree" label-width="22px" class="input-item">
                <el-checkbox class="checkbox" size="large" v-model="formLogin.agree">
                  I agree to the Privacy Policy and Terms of Service
                </el-checkbox>
              </el-form-item>
              <el-button size="large" class="submit-btn" @click="doLogin">Login</el-button>
            </el-form>
          </div>
          <el-divider content-position="center">Or</el-divider>
          <el-button size="large" class="submit-btn" @click="toggleForm()">Register</el-button>
        </div>

        <!-- Right Area - Register Form -->
        <div class="right-area" v-if="!showWhich">
          <div class="title">Register</div>
          <div class="form">
            <el-form ref="formRegisterRef" :model="formRegister" :rules="rulesRegister" label-position="right" label-width="0" status-icon>
              <el-form-item prop="email" class="input-item">
                <el-input v-model="formRegister.email" placeholder="Please enter your email address" :prefix-icon="ChatLineSquare"/>
              </el-form-item>
              <el-form-item prop="username" class="input-item">
                <el-input v-model="formRegister.username" placeholder="Please enter your username" :prefix-icon="User" maxlength="32" show-word-limit/>
              </el-form-item>
              <el-form-item prop="password" class="input-item">
                <el-input v-model="formRegister.password" placeholder="Please enter your password" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="retryPwd" class="input-item">
                <el-input v-model="formRegister.retryPwd" placeholder="Please confirm your password" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="agree" label-width="22px" class="input-item">
                <el-checkbox size="large" v-model="formRegister.agree">
                  I agree to the Privacy Policy and Terms of Service

                </el-checkbox>
              </el-form-item>
              <el-button size="large" class="submit-btn" @click="doRegister">Register</el-button>
            </el-form>
          </div>
          <el-divider content-position="center">Or</el-divider>
          <el-button size="large" class="submit-btn" @click="toggleForm()">Login</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background-color: white;
}

.login-box {
  width: 100%;
  max-width: 50rem;
  background-color: white;
  border-radius: 2rem;
  border: 3px solid #ff4d4d;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  position: relative;
  transition: box-shadow 0.3s ease;
}

.login-box:hover {
  box-shadow: 0 6px 12px -1px rgba(255, 77, 77, 0.2), 0 4px 8px -1px rgba(255, 77, 77, 0.1);
}

.content-wrapper {
  display: flex;
  position: relative;
  min-height: 35rem;
}

.left-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
  position: relative;
}

.right-area {
  flex: 1;
  padding: 2rem;
  border-left: 2px solid #d5d0d0;
}

.brand-image {
  width: 80%;
  max-width: 200px;
  height: auto;
  object-fit: contain;
  margin-top: 2rem;
}

.title {
  font-size: 1.5rem;
  color: rgba(51, 51, 51, 0.8);
  font-weight: 600;
  text-align: center;
  margin-bottom: 2rem;
}

.form {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.input-item {
  margin-bottom: 1rem;
}

.submit-btn {
  width: 100%;
  background: #ff2441;
  color: #fff;
  height: 48px;
  border-radius: 999px;
  font-size: 16px;
  font-weight: 600;
  opacity: 0.5;
  transition: all 0.2s;
  margin-top: 1rem;
}

.submit-btn:hover {
  opacity: 1;
}

:deep(.el-checkbox) {
  display: flex;
  justify-content: center;
  width: 100%;
  margin: 0;
  padding: 0 1rem;
}

:deep(.el-checkbox__label) {
  line-height: 1.2;
  text-align: center;
  white-space: normal;  
  width: 100%;       
  max-width: 280px;   
  word-wrap: break-word;
}

.input-item {
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-box {
    margin: 1rem;
    max-width: 100%;
  }

  .content-wrapper {
    flex-direction: column;
  }

  .left-area {
    padding: 1rem;
    min-height: auto;
  }

  .right-area {
    border-left: none;
    border-top: 2px solid #d5d0d0;
    padding: 1rem;
  }

  .brand-image {
    width: 60%;
    margin-top: 1rem;
  }

  .title {
    font-size: 1.25rem;
    margin-bottom: 1rem;
  }

  .form {
    padding: 0 1rem;
  }
}

@media (max-width: 480px) {
  .login-box {
    margin: 0;
    border-radius: 0;
    height: 95vh;
  }

  .content-wrapper {
    min-height: 100vh;
  }

  .form {
    padding: 0;
  }
}
</style>