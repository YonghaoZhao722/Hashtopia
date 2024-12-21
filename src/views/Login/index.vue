<script setup>
import {ref} from "vue";

import {ElMessage} from 'element-plus'
import 'element-plus/theme-chalk/el-message.css'
import {User, Lock, ChatLineSquare} from "@element-plus/icons-vue";
import {useUserStore} from "@/stores/user";
import {useRouter} from "vue-router";

// 定义路由
const emit = defineEmits(['changeShow']);
const router = useRouter()
// 账户加密码校验
// 准备表单对象
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

// 准备规则对象
const rulesRegister = {
  email: [
    {required: true, message: '邮箱不能为空', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
        var emailRegExp1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        if ((!emailRegExp.test(value) && value !== '') || (!emailRegExp1.test(value) && value !== '')) {
          callback(new Error('请输入有效邮箱格式！'));
        } else {
          callback();
        }
      }
    }
  ],
  username: [
    {required: true, message: '用户名不能为空！', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '密码不能为空', trigger: 'blur'},
    {min: 6, max: 14, message: '密码不符合要求', trigger: 'blur'}
  ],
  retryPwd: [
    {required: true, message: '密码不能为空', trigger: 'blur'},
    {min: 6, max: 14, message: '密码不符合要求', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        if (value !== formRegister.value.password) {
          callback(new Error('两次密码不一致！'));
        } else {
          callback();
        }
      }
    }
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        // 自定义校验逻辑
        if (value) {
          callback()
        } else {
          callback(new Error('请勾选协议'))
        }
      }
    }
  ]
}
const rulesLogin = {
  email: [
    {required: true, message: '邮箱不能为空', trigger: 'blur'},
    {
      validator: (rule, value, callback) => {
        var emailRegExp = /^([a-zA-Z0-9_-])+@([a-zA-Z0-9_-])+(\.[a-zA-Z0-9_-])+/;
        var emailRegExp1 = /^([a-zA-Z]|[0-9])(\w|\-)+@[a-zA-Z0-9]+\.([a-zA-Z]{2,4})$/;
        if ((!emailRegExp.test(value) && value !== '') || (!emailRegExp1.test(value) && value !== '')) {
          callback(new Error('请输入有效邮箱格式！'));
        } else {
          callback();
        }
      }
    }
  ],
  password: [
    {required: true, message: '密码不能为空', trigger: 'blur'},
    {min: 6, max: 14, message: '密码不符合要求', trigger: 'blur'}
  ],
  agree: [
    {
      validator: (rule, value, callback) => {
        // 自定义校验逻辑
        if (value) {
          callback()
        } else {
          callback(new Error('请勾选协议'))
        }
      }
    }
  ]
}

// 获取form实例校验
const formLoginRef = ref(null)
const formRegisterRef = ref(null)

// 准备用户
const userStore = useUserStore();
const doLogin = () => {
  const {email, password} = formLogin.value
  formLoginRef.value.validate(async (valid) => {
    if (valid) {
      // 提示用户
      await userStore.getUserInfo({email, password})
      emit('changeShow')
      await router.replace(`/user/index/${userStore.userInfo.id}`)
      ElMessage({type: 'success', message: '登陆成功'})
    }
  })
}
const doRegister = () => {
  const {email, username, password} = formRegister.value
  formRegisterRef.value.validate(async (valid) => {
    if (valid) {
      await userStore.userRegister({email, username, password})
      ElMessage({type: 'success', message: '注册成功'})
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
          <div class="title">登录</div>
          <div class="form">
            <el-form ref="formLoginRef" :model="formLogin" :rules="rulesLogin" label-position="right" label-width="0" status-icon>
              <el-form-item prop="email" class="input-item">
                <el-input v-model="formLogin.email" placeholder="请输入邮箱号" :prefix-icon="User"/>
              </el-form-item>
              <el-form-item prop="password" class="input-item">
                <el-input v-model="formLogin.password" placeholder="请输入密码" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="agree" label-width="22px" class="input-item">
                <el-checkbox size="large" v-model="formLogin.agree">
                  我已同意隐私条款和服务条款
                </el-checkbox>
              </el-form-item>
              <el-button size="large" class="submit-btn" @click="doLogin">点击登录</el-button>
            </el-form>
          </div>
          <el-divider content-position="center">或</el-divider>
          <el-button size="large" class="submit-btn" @click="toggleForm()">新用户注册</el-button>
        </div>

        <!-- Right Area - Register Form -->
        <div class="right-area" v-if="!showWhich">
          <div class="title">注册</div>
          <div class="form">
            <el-form ref="formRegisterRef" :model="formRegister" :rules="rulesRegister" label-position="right" label-width="0" status-icon>
              <el-form-item prop="email" class="input-item">
                <el-input v-model="formRegister.email" placeholder="请输入注册邮箱" :prefix-icon="ChatLineSquare"/>
              </el-form-item>
              <el-form-item prop="username" class="input-item">
                <el-input v-model="formRegister.username" placeholder="请输入用户名" :prefix-icon="User" maxlength="32" show-word-limit/>
              </el-form-item>
              <el-form-item prop="password" class="input-item">
                <el-input v-model="formRegister.password" placeholder="请输入密码" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="retryPwd" class="input-item">
                <el-input v-model="formRegister.retryPwd" placeholder="请确认输入密码" :prefix-icon="Lock" show-password/>
              </el-form-item>
              <el-form-item prop="agree" label-width="22px" class="input-item">
                <el-checkbox size="large" v-model="formRegister.agree">
                  我已同意隐私条款和服务条款
                </el-checkbox>
              </el-form-item>
              <el-button size="large" class="submit-btn" @click="doRegister">点击注册</el-button>
            </el-form>
          </div>
          <el-divider content-position="center">或</el-divider>
          <el-button size="large" class="submit-btn" @click="toggleForm()">立即登录</el-button>
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
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
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
  }

  .content-wrapper {
    min-height: 100vh;
  }

  .form {
    padding: 0;
  }
}
</style>