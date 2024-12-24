<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref, computed, nextTick} from "vue";
import HomeCard from "@/components/homeCard.vue";
import CardDetail from "@/components/cardDetail.vue";
import {Back,Plus } from "@element-plus/icons-vue";
import { genFileId } from 'element-plus'
import {doFocus, queryUserIndex, queryUserPost, unFollow, queryUserFocus, updateUserInfo, changePassword} from "@/apis/main";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from "@vueuse/core";
import {useUserStore} from "@/stores/user";
import {ElMessage} from "element-plus";
import { LazyImg, Waterfall } from 'vue-waterfall-plugin-next'
import 'vue-waterfall-plugin-next/dist/style.css'
import '../../styles/common.css'

const route = useRoute()
const Details = controlDetail()
const userStore = useUserStore()
const baseURL = import.meta.env.VITE_API_BASE_URL
// Load user information //////////////////////////////////////////////////////////////
const userInfo = ref({})
const getUserInfo = async () => {
  const id = route.params.id
  const res = await queryUserIndex({id})
  userInfo.value = res.data
  document.title = res.data.user.username
}

const checkFollow = (id) => {
  // Ensure safe access
  if (!userStore.userFocus.value) {
    return false
  }
  return userStore.userFocus.value.includes(id)
}

// Modify follow operation function
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({type: 'warning', message: 'Cannot follow yourself'})
    return
  }
  
  try {
    const res = await doFocus({id})
    // Ensure array initialization
    if (!userStore.userFocus.value) {
      userStore.userFocus.value = []
    }
    // Update status
    userStore.extendUserInfo(1, id)
    userInfo.value.user.fans += 1
    
    // Refresh user follow list to ensure state synchronization
    const focusResult = await queryUserFocus()
    userStore.userFocus.value = focusResult.follow
    
    ElMessage({type: 'success', message: res.info})
  } catch(error) {
    ElMessage({type: 'warning', message: 'Follow failed'})
  }
}

// End of loading user information ////////////////////////////////////////////////////////////

// Homepage tab switching //////////////////////////////////////////////////////////////
const radio = ref('Posts')
const userPost = ref([])
const userCollect = ref([])
const userFavorite = ref([])

const loading = ref(false)
const hasMore = ref(true)

const Toggle = async () => {
  loading.value = true
  hasMore.value = true // Reset hasMore status
  const user_id = route.params.id
  const offset = 0
  const types = radio.value
  
  try {
    if (radio.value === 'Posts' && userPost.value.length === 0) {
      const post = await queryUserPost({user_id, types, offset})
      userPost.value = post.info
      hasMore.value = post.has_more
    } else if (radio.value === 'Collections' && userCollect.value.length === 0) {
      const post = await queryUserPost({user_id, types, offset})
      userCollect.value = post.info
      hasMore.value = post.has_more
    } else if (radio.value === 'Likes' && userFavorite.value.length === 0) {
      const post = await queryUserPost({user_id, types, offset})
      userFavorite.value = post.info
      hasMore.value = post.has_more
    }
  } catch (error) {
    console.error('Loading failed:', error)
  } finally {
    loading.value = false
  }
}

const load = async () => {
  if (loading.value || !hasMore.value) return
  
  loading.value = true
  try {
    const user_id = userInfo.value.user.id
    const types = radio.value
    let currentList = radio.value === 'Posts' ? userPost : 
                     radio.value === 'Collections' ? userCollect : userFavorite
    
    const offset = currentList.value.length
    const result = await queryUserPost({user_id, types, offset})
    
    if (result.info.length > 0) {
      currentList.value = [...currentList.value, ...result.info]
    }
    hasMore.value = result.has_more
  } catch (error) {
    console.error('Load more failed:', error)
  } finally {
    loading.value = false
  }
}

// End of homepage tab switching ///////////////////////////////////////////////////////////

// Card detail page content //////////////////////////////////////////////////////////
const detail = Details.detail
const overlayX = ref(0)
const overlayY = ref(0)
const overlay = ref(null)
const show = ref(false)

const getDetails = async (id) => Details.getDetail(id)

const handleOverlayClose = () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = 'Welcome to Hashtopia!';
  
  const backButton = document.querySelector('.backPage');
  if (backButton) {
    backButton.style.display = 'none';
  }
  
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    el.style.display = '';
  });
};

const addBackPage = () => {
  nextTick(() => {
    const backButton = document.querySelector('.backPage');
    if (backButton) {
      backButton.style.display = 'block';
    }
  });
};

const showMessage = async (id, left, top) => {
  sessionStorage.setItem('cardDetailSource', window.location.pathname);
  
  window.history.pushState({}, "", `/explore/${id}`);
  overlayX.value = left;
  overlayY.value = top;
  await getDetails(id);
  show.value = true;
  await nextTick();
};

const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  window.history.pushState({}, '', `/user/index/${userInfo.value.user.id}`)
  document.title = userInfo.value.user.username
  show.value = false
}

onClickOutside(overlay, () => {
  window.history.pushState({}, "", `/user/index/${userInfo.value.user.id}`)
  document.title = userInfo.value.user.username
  show.value = false
})

let style = null
const onBeforeEnter = () => {
  style = document.createElement('style')
  style.innerHTML =
      `@keyframes scale-up-center {
          0% {
            transform: scale(0.5);
            transform-origin: ${overlayX.value}px ${overlayY.value}px;
          }
          100% {
            transform: scale(1);
          }
       }`
  document.head.appendChild(style)
}

const onAfterEnter = (el) => {
  el.style = 'background-color: #fff'
  const button = el.querySelector('.backPage')
  button.style.display = ''
}

const onBeforeLeave = (el) => {
  const button = el.querySelector('.backPage')
  button.style.display = 'none'
  el.style = 'background-color: transparent'
}

const onAfterLeave = () => {
  if (style) {
    document.head.removeChild(style)
    style = null
  }
}

onMounted(async () => {
  await getUserInfo()
  // Ensure userFocus is initialized
  if (!userStore.userFocus.value) {
    userStore.userFocus.value = []
    // Get follow list
    try {
      const focusResult = await queryUserFocus()
      if (focusResult && focusResult.follow) {
        userStore.userFocus.value = focusResult.follow
      }
    } catch (error) {
      console.error('Failed to get follow list:', error)
    }
  }
  await Toggle()
  const currentPath = window.location.pathname;
  if (currentPath.includes('/explore/')) {
    const postId = currentPath.split('/').pop();
    if (postId) {
      await getDetails(postId);
      show.value = true;
      await nextTick();
    }
  }
})

// Add state control
const hoverButton = ref(false)

// Modify follow status button text
const buttonText = computed(() => {
  if (!userStore.userFocus.value || !checkFollow(userInfo.value?.user?.id)) {
    return 'Follow'
  }
  return hoverButton.value ? 'Unfollow' : 'Following'
})

// Add unfollow function
const cancelFocus = async (id) => {
  try {
    const res = await unFollow({id})
    // Update status
    userStore.removeFocus(1, id)
    userInfo.value.user.fans -= 1
    
    // Refresh user follow list to ensure state synchronization
    const focusResult = await queryUserFocus()
    userStore.userFocus.value = focusResult.follow
    
    ElMessage({type: 'success', message: res.info})
  } catch(error) {
    ElMessage({type: 'warning', message: 'Unfollow failed'})
  }
}

// Unified follow operation handling
const handleFocus = async (id) => {
  if(checkFollow(id)) {
    await cancelFocus(id)
  } else {
    await doFocusOn(id)
  }
}

// Add to script setup
const isOwnProfile = computed(() => {
  return userStore.userInfo && userInfo.value?.user && userStore.userInfo.id === userInfo.value.user.id
})

const dialogFormVisible = ref(false)
const upload = ref(null)
const avatar = ref('')
const fileList = ref([])
const form = ref({
  username: '',
  signature: '',
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const handleExceed = (files) => {
  upload.value.clearFiles()
  const file = files[0]
  file.uid = genFileId()
  upload.value.handleStart(file)
}

const handleChange = (uploadFile) => {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif']
  const maxSize = 2

  if (!allowedTypes.includes(uploadFile.raw.type)) {
    ElMessage.error('Please upload a valid image file!')
    fileList.value = []
    return false
  } 
  
  if (uploadFile.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`File size cannot exceed ${maxSize}MB!`)
    fileList.value = []
    return false
  }

  // Directly update fileList
  fileList.value = [uploadFile]
  return true
}

const closeDialog = async () => {
  dialogFormVisible.value = false
  await getUserInfo()
  fileList.value = []
  form.value.oldPassword = ''
  form.value.newPassword = ''
  form.value.confirmPassword = ''
}

const onSuccess = async (response) => {
  avatar.value = response.filepath
  // Update user store with new avatar
  userStore.changeInfo({
    ...userStore.userInfo,
    avatar: response.filepath
  })
  // Refresh user information
  await getUserInfo()
  // Force refresh all components that depend on userStore
  await nextTick()
}

const onError = async (error) => {
  ElMessage({
    type: 'warning',
    message: 'Avatar upload failed'
  })
  const userStore = useUserStore()
  await userStore.userLogout()
  await router.replace('/')
}

const openDialog = () => {
  dialogFormVisible.value = true
  form.value.username = userStore.userInfo.username
  form.value.signature = userStore.userInfo.signature
}

const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback()
    return
  }
  if (value.length < 6) {
    callback(new Error('Password must be at least 6 characters!'))
    return
  }
  callback()
}

// 添加确认密码验证函数
const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback()
    return
  }
  if (value !== form.value.newPassword) {
    callback(new Error('Passwords do not match!'))
    return
  }
  callback()
}

// Form validation rules
const rules = {
  username: [
    { required: true, message: 'Username cannot be empty!', trigger: 'blur' }
  ],
  signature: [
    { required: true, message: 'Signature cannot be empty!', trigger: 'blur' }
  ],
  oldPassword: [
    { validator: validatePassword, trigger: 'blur' }
  ],
  newPassword: [
    { validator: validatePassword, trigger: 'blur' }
  ],
  confirmPassword: [
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}




// Form object
const formRef = ref(null)
const doUpdate = async () => {
  const { username, signature, oldPassword, newPassword, confirmPassword } = form.value
  const isModified = username !== userStore.userInfo.username || signature !== userStore.userInfo.signature
  const isAvatarUploaded = fileList.value.length === 1
  const isPasswordChanged = oldPassword && newPassword && confirmPassword

  if (!isModified && !isAvatarUploaded && !isPasswordChanged) {
    ElMessage({type: 'warning', message: 'No changes made!'})
    return
  }

  try {
    if (isPasswordChanged) {
      if (newPassword !== confirmPassword) {
        ElMessage({type: 'error', message: 'Passwords do not match!'})
        return
      }
      await changePassword({
        oldPassword,
        newPassword
      })
      ElMessage({type: 'success', message: 'Password updated successfully'})
    }

    if (isModified || isAvatarUploaded) {
      if (isModified) {
        await updateUserInfo({username, signature})
      }
      if (isAvatarUploaded) {
        await upload.value.submit()
      }
      userStore.changeInfo({username, signature, avatar: avatar.value})
      ElMessage({type: 'success', message: 'Profile updated successfully'})
    }

    dialogFormVisible.value = false
    await getUserInfo()
  } catch (error) {
    ElMessage({type: 'error', message: error.response?.data?.error || 'Update failed, please try again'})
  }
}
</script>

<template>
  <div class="userInfo" v-if="userInfo.user">
    <el-row :gutter="10">
      <el-col :span="7" style="width: 20vw;">
        <el-avatar style="width: 10vw;height: 10vw;" :src="userInfo.user.avatar"></el-avatar>
      </el-col>
      <el-col :span="7" style="width: 15vw;">
        <h2>{{ userInfo.user.username }}</h2>
        <p>{{ userInfo.user.signature }}</p>
        <div class="tagArea">
          <el-tag class="ml-2" type="success" round>{{ userInfo.user.focusOn }} Following</el-tag>
          <el-tag class="ml-2" type="info" round>{{ userInfo.user.fans }} Followers</el-tag>
          <el-tag class="ml-2" type="warning" round>{{ userInfo.user.postsCount }} Posts</el-tag>
        </div>
      </el-col>
      <el-col :span="5">
        <template v-if="isOwnProfile">
          <el-button 
            type="primary" 
            class="update-btn"
            @click="openDialog">
            Update
          </el-button>
        </template>
        <button 
          v-if="userStore.userInfo.id !== userInfo.user.id"
          class="focusOn"
          :class="{ 'followed': checkFollow(userInfo.user.id) }"
          @click="handleFocus(userInfo.user.id)"
          @mouseover="hoverButton = true"
          @mouseleave="hoverButton = false">
          {{ buttonText }}
        </button>
      </el-col>
    </el-row>
  </div>
  <div class="checkBox" @change="Toggle" style="text-align: center">
    <template v-if="isOwnProfile">
      <el-radio-group v-model="radio"  size="large">
        <el-radio-button class="radio" style="margin: 1vw;" label="Posts" name="Post"/>
        <el-radio-button class="radio" style="margin: 1vw;" label="Collections" name="Collections"/>
        <el-radio-button class="radio" style="margin: 1vw;" label="Likes" name="Likes"/>
    </el-radio-group>
  </template>
  </div>


  <div class="radio" v-if="userInfo.user">
    <div v-if="radio === 'Posts'">
      <div v-if="userPost.length === 0">
        <el-empty description="No posts yet..."/>
      </div>
      <div v-else  class="scroll-container">
        <home-card 
          :list="userPost" 
          :loading="loading"
          :has-more="hasMore"
          @show-detail="showMessage"
          @load-more="load"
        ></home-card>
      </div>
      <transition
        name="fade"
        @before-enter="onBeforeEnter"
        @after-enter="onAfterEnter"
        @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave"
    >
      <div class="overlay" v-if="show" @click.self="handleOverlayClose">
        <button class="backPage" @click="handleOverlayClose">
          <el-icon>
            <Back/>
          </el-icon>
        </button>
        <card-detail 
          :detail="detail" 
          @afterDoComment="afterDoComment" 
          @closeOverlay="handleOverlayClose" 
          @needBackPage="addBackPage"
          ref="overlay"
        />
      </div>
    </transition>
    </div>

    <div v-else-if="radio === 'Collections'">
      <div v-if="userCollect.length === 0">
        <el-empty description="No collections yet..."/>
      </div>
      <div v-else  class="scroll-container">
        <home-card 
          :list="userCollect"
          :loading="loading"
          :has-more="hasMore"
          @show-detail="showMessage"
          @load-more="load"
        ></home-card>
      </div>
      <transition
        name="fade"
        @before-enter="onBeforeEnter"
        @after-enter="onAfterEnter"
        @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave"
    >
      <div class="overlay" v-if="show">
        <button style="display:none;" class="backPage" @click="close">
          <el-icon>
            <Back/>
          </el-icon>
        </button>
        <card-detail 
          :detail="detail" 
          @afterDoComment="afterDoComment"
          @needBackPage="addBackPage"
          @closeOverlay="handleOverlayClose"
          ref="overlay"
        />
      </div>
    </transition>
    </div>

    <div v-else-if="radio === 'Likes'">
      <div v-if="userFavorite.length === 0">
        <el-empty description="No likes yet..."/>
      </div>
      <div v-else class="scroll-container">
        <home-card 
          :list="userFavorite"
          :loading="loading"
          :has-more="hasMore"
          @show-detail="showMessage"
          @load-more="load"
        ></home-card>
      </div>
      <transition
        name="fade"
        @before-enter="onBeforeEnter"
        @after-enter="onAfterEnter"
        @before-leave="onBeforeLeave"
        @after-leave="onAfterLeave"
    >
      <div class="overlay" v-if="show" @click.self="handleOverlayClose">
        <button class="backPage" @click="handleOverlayClose">
          <el-icon>
            <Back/>
          </el-icon>
        </button>
        <card-detail 
          :detail="detail" 
          @afterDoComment="afterDoComment" 
          @closeOverlay="handleOverlayClose" 
          @needBackPage="addBackPage"
          ref="overlay"
        />
      </div>
    </transition>
    </div>

        <el-dialog 
        v-model="dialogFormVisible" 
        title="" 
        @closed="closeDialog"
        center 
        draggable
        class="update-info-dialog"
      >
        <div class="fileUpload">
          <el-upload v-model:file-list="fileList"
          :show-file-list="true"
          list-type="picture-card"
          ref="upload"
          action="http://localhost:8000/user/avatar/"
          :limit="1"
          :on-exceed="handleExceed"
          :auto-upload="false"
          :on-change="handleChange"
          :headers="userStore.headersObj"
          :on-success="onSuccess"
          :on-error="onError"
          class="upload-container"
          :on-preview="handlePictureCardPreview"
          >
          <template #trigger>
            <div v-if="!fileList.length" class="upload-area">
              <div class="upload-box">
                <el-icon class="upload-icon"><Plus /></el-icon>
              </div>
              <div class="upload-text">Drag or Click</div>
            </div>
          </template>
      </el-upload>

    </div>
    <div class="fileUpload">
      <el-form :model="form" ref="formRef" :rules="rules" label-position="top">
        <el-form-item prop="username" label="Name" label-width="7vw" style="margin: 2vw;font-size: 100%;">
          <el-input v-model="form.username" maxlength="32"
                    show-word-limit class="my"/>
        </el-form-item>
        <el-form-item prop="signature" label="Bio" label-width="7vw" style="margin: 2vw;">
          <el-input v-model="form.signature" class="my"/>
        </el-form-item>

        <el-divider content-position="center">Change Password</el-divider>
        <el-form-item prop="oldPassword" label="Current Password" label-width="7vw" style="margin: 2vw;">
          <el-input v-model="form.oldPassword" type="password" show-password class="my"/>
        </el-form-item>
        
        <el-form-item prop="newPassword" label="New Password" label-width="7vw" style="margin: 2vw;">
          <el-input v-model="form.newPassword" type="password" show-password class="my"/>
        </el-form-item>
        
        <el-form-item prop="confirmPassword" label="Confirm Password" label-width="7vw" style="margin: 2vw;">
          <el-input v-model="form.confirmPassword" type="password" show-password class="my"/>
        </el-form-item>

      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog" round>Cancel</el-button>
        <el-button type="primary" @click="doUpdate" round>
          Confirm
        </el-button>
      </span>
    </template>
  </el-dialog>
  </div>
</template>

<style scoped>
.userInfo {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
}

h2 {
  font-size: clamp(15px, 2vw, 24px);  /* 响应式字体大小 */
  overflow: hidden;
  text-overflow: ellipsis;  /* 超出部分显示省略号 */
  white-space: nowrap;  /* 防止换行 */
}
@media screen and (max-width: 375px) {
  .el-col:nth-child(2) {
    font-size: 10;
  }

  .el-col:last-child {
    font-size: 100;
  }

  h2 {
      font-size: 14px;  /* 固定更小的字体大小 */
    }

  .update-btn, .focusOn {
    min-width: 60px;
    min-height: 26px;
    padding: 2px 8px;
    font-size: 12px;
  }
}

.focusOn:hover {
  background-color: #fd5656;
}

.focusOn.followed {
  background-color: #f4f4f5;
  color: #909399;
}

.focusOn.followed:hover {
  background-color: #f56c6c;
  color: #fff;
}
.update-btn, .focusOn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 8vw;
  min-width: 80px;  /* 增加最小宽度 */
  height: 2.5vw;
  min-height: 32px;  /* 增加最小高度 */
  font-weight: 600;
  font-size: clamp(14px, 1vw, 20px);  /* 使用 clamp 控制字体大小范围 */
  line-height: 1;
  padding: 12px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  background-color: red;
  border-radius: 1000px;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
  margin-left: 1rem;
  transition: all 0.3s;
}

.update-btn:hover {
  background-color: #fd5656;
}
.tagArea {
  width: 40vw;
}

.tagArea .ml-2 {
  margin-right: 1vw;
}

:deep(.el-tag){
  height: 2.5vh;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: white;
  z-index: 9999;
  display: flex;
  flex-direction: column;
}

:deep(.el-dialog) {
  width: 35vw;
  min-width: 420px;
}
.backPage {
  position: absolute;
  left: 16px;
  top: 16px;
  display: flex !important;
  justify-content: center;
  align-items: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.05);
  cursor: pointer;
  border: none;
  z-index: 10000;
}

.backPage .el-icon {
  font-size: 20px;
  color: #666;
}

.backPage:hover {
  background: rgba(0, 0, 0, 0.1);
}


.fade-enter-active {
  animation: scale-up-center 0.3s ease-out both;
}

.fade-leave-active {
  animation: scale-up-center 0.3s ease-in both reverse;
}


.upload-area {
  width: 200px;
  height: 200px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
  margin: 0 auto;
}

.upload-area:hover {
  border-color: #409eff;
}

.upload-box {
  width: 80px;
  height: 80px;
  border: 2px dashed #dcdfe6;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.upload-icon {
  font-size: 24px;
  color: #909399;
}

.upload-text {
  color: #909399;
  font-size: 14px;
}

.update-info-dialog {
  max-width: 100vw;
}

.fileUpload {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding: 1rem;
}

.upload-container {
  width: 100%;
  max-width: 300px;
  margin: 0 auto;
}

.upload-area {
  width: 100%;
  aspect-ratio: 1;
  max-width: 200px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: border-color 0.3s;
  margin: 0 auto;
}

.upload-box {
  width: 50%;
  aspect-ratio: 1;
  border: 2px dashed #dcdfe6;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.upload-icon {
  font-size: clamp(16px, 3vw, 24px);
  color: #909399;
}

.upload-text {
  color: #909399;
  font-size: clamp(12px, 2.5vw, 14px);
}

.form-container {
  width: 100%;
  max-width: 500px;
}

.form-item {
  width: 100%;
  margin: 1rem 0;
}

.input-field {
  width: 100%;
}

.dialog-footer {
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 1rem;
  padding-top: 0;
}

.card {
  width: 100%;
  border-radius: 0.8rem;
  background-color: white;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.image {
  width: 100%;
  border-radius: 0.8rem 0.8rem 0 0;
  display: block;
  transition: opacity 0.2s;
}

.image:hover {
  opacity: 0.7;
}

.card-content {
  padding: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 400;
  font-size: 0.875rem;
  color: #333;
}

.card-title-container {
  margin-bottom: 1vh;
  height: auto;
  max-height: 48px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
}

.card-title {
  font-weight: 800;
  font-size: 0.875rem;
  cursor: pointer;
  margin: 0;
  line-height: 1.2;
}

:deep(.lazy__img[lazy=loading]) {
  padding: 5em 0;
  width: 48px;
}

:deep(.lazy__img[lazy=loaded]) {
  width: 100%;
}

:deep(.lazy__img[lazy=error]) {
  padding: 5em 0;
  width: 48px;
}

.scroll-container {
  height: calc(100vh - 250px);
  overflow-y: auto;
  overflow-x: hidden;
  padding: 0 20px;
}

.scroll-container::-webkit-scrollbar {
  width: 6px;
}

.scroll-container::-webkit-scrollbar-thumb {
  background-color: #dcdfe6;
  border-radius: 3px;
}

.scroll-container::-webkit-scrollbar-track {
  background-color: #f5f7fa;
}


@media screen and (max-width: 768px) {
  :deep(.el-main){
    overflow: hidden;
  }
  .userInfo {
    padding: 2.5vh;
    width: 100%;
    height: 12vh;
  }

  .el-row {
    height: auto;
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
  }

  .el-col:first-child {
    width: 20% !important;
    position: relative;
  }

  .el-col:nth-child(2) {
    width: 60% !important;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .el-avatar {
    width: 15vw !important;
    height: 15vw !important;
  }



  .tagArea {
    position: absolute;
    left: 0;
    top: 100%; 
    transform: translateY(10px);
    width: calc(100% + 2vw);
    display: flex;
    gap: 3vw;
    margin-top: 0.5vh;
  }

  .el-col:last-child {
    
    width: 20% !important;
    display: flex;
    justify-content: flex-end;
    align-items: flex-start;
  }


  .ml-2 {
    margin: 0;
    font-size: 12px;
    padding: 0 8px;
  }

  .update-btn, .focusOn {
    width: 20vw;
    max-width: 100px;
    margin: -10px;
    font-size: 110%;
    height: auto;
    margin-left: 1rem;
  }

  .focusOn {
    margin: -10px;
    font-size: 12px;
    height: auto;
    min-width: auto;
  }


 .checkBox {
  margin-top: 6vw;
 }
 .scroll-container {
    height: calc(100vh - 200px);
    padding: 0 10px;
  }
  .upload-area {
    max-width: 150px;
  }

  .upload-box {
    width: 60%;
  }

  .form-item {
    margin: 0.5rem 0;
  }

  :deep(.el-dialog) {
    width: 90vw;
  }


  .dialog-footer button {
    min-width: 80px;
    padding: 8px 16px;
  }
  .radio {
    width: 100%;
    display: flex;
    flex-direction: column;
  }

  .el-radio-group {
    display: flex;
    width: 100%;
    height: 3vh;
    justify-content: space-between;
    margin-top: 8px;
    margin-bottom: 16px;
  }

  .el-radio-button {
    flex: 1;
    text-align: center;
  }

  :deep(.el-radio-button__inner) {
    width: 100%;
    padding: 1vh 0;
    border-radius: 0;
  }

  .el-radio-button__inner {
    padding: 8px 0;
    font-size: 14px;
  }

  h2 {
    font-size: clamp(14px, 4vw, 20px); 
  }
  
  
  p {
    margin: 4px 0;
    font-size: 2.8vw;
  }
 .backPage {
    top: 12px;
    left: 2%;
    border-radius: 35px;
  }
}

:deep(.el-upload-list--picture-card) {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 8px;
  width: 100%;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 100%;
  aspect-ratio: 1;
  margin: 0;
}

:deep(.el-upload--picture-card) {
  width: 100%;
  aspect-ratio: 1;
  margin: 0;
}

.el-divider {
  text-align: center;
}
</style>