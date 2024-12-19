<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref, computed} from "vue";
import HomeCard from "@/components/homeCard.vue";
import CardDetail from "@/components/cardDetail.vue";
import {Back,Plus } from "@element-plus/icons-vue";
import { genFileId } from 'element-plus'
import {doFocus, queryUserIndex, queryUserPost, unFollow, queryUserFocus, updateUserInfo} from "@/apis/main";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from "@vueuse/core";
import {resizeWaterFall, waterFallInit, waterFallMore} from "@/utils/waterFall";
import {useUserStore} from "@/stores/user";
import {ElMessage} from "element-plus";

const route = useRoute()
const Details = controlDetail()
const userStore = useUserStore()

// 加载用户信息 //////////////////////////////////////////////////////////////
const userInfo = ref({})
const getUserInfo = async () => {
  const id = route.params.id
  const res = await queryUserIndex({id})
  userInfo.value = res.data
  document.title = res.data.user.username
}
const checkFollow = (id) => {
  // 确保安全地访问
  if (!userStore.userFocus.value) {
    return false
  }
  return userStore.userFocus.value.includes(id)
}
// 修改关注操作函数
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({type: 'warning', message: '不能对自己进行关注操作'})
    return
  }
  
  try {
    const res = await doFocus({id})
    // 确保初始化数组
    if (!userStore.userFocus.value) {
      userStore.userFocus.value = []
    }
    // 更新状态
    userStore.extendUserInfo(1, id)
    userInfo.value.user.fans += 1
    
    // 重新获取用户关注列表以确保状态同步
    const focusResult = await queryUserFocus()
    userStore.userFocus.value = focusResult.follow
    
    ElMessage({type: 'success', message: res.info})
  } catch(error) {
    ElMessage({type: 'error', message: '关注失败'})
  }
}

// 加载用户信息结束 ////////////////////////////////////////////////////////////

// 主页切换标签 //////////////////////////////////////////////////////////////
const radio = ref('帖子')
const userPost = ref([])
const userCollect = ref([])
const userFavorite = ref([])
const disabled = ref(true); // 初始禁用滚动加载

const columns = ref(0)
const card_columns_posts = ref({})
const card_columns_like = ref({})
const card_columns_collect = ref({})
const arrHeight = ref([])


const Toggle = async () => {
  const user_id = route.params.id
  const offset = 0
  const types = radio.value
  if (radio.value === '帖子' && userPost.value.length === 0) {
    const post = await queryUserPost({user_id, types, offset})
    userPost.value = post.info
    waterFallInit(columns, card_columns_posts, arrHeight, userPost)
  } else if (radio.value === '收藏' && userCollect.value.length === 0) {
    const post = await queryUserPost({user_id, types, offset})
    userCollect.value = post.info
    waterFallInit(columns, card_columns_collect, arrHeight, userCollect)
  } else if (radio.value === '点赞' && userFavorite.value.length === 0) {
    const post = await queryUserPost({user_id, types, offset})
    userFavorite.value = post.info
    waterFallInit(columns, card_columns_like, arrHeight, userFavorite)
  }
  disabled.value = false;
}
const load = async () => {
  disabled.value = true;
  const user_id = userInfo.value.user.id;
  const types = radio.value;
  if (types === '帖子') {
    const offset = userPost.value.length;
    const post = await queryUserPost({user_id, types, offset});
    if (post.info.length === 0) {
      disabled.value = true;
    } else {
      userPost.value = [...userPost.value, ...post.info];
      waterFallMore(arrHeight, card_columns_posts, post.info)
      disabled.value = false;
    }
  } else if (types === '点赞') {
    const offset = userFavorite.value.length;
    const like = await queryUserPost({user_id, types, offset});
    if (like.info.length === 0) {
      disabled.value = true;
    } else {
      userFavorite.value = [...userFavorite.value, ...like.info];
      waterFallMore(arrHeight, card_columns_like, like.info)
      disabled.value = false;
    }
  } else if (types === '收藏') {
    const offset = userCollect.value.length;
    const collect = await queryUserPost({user_id, types, offset});
    if (collect.info.length === 0) {
      disabled.value = true;
    } else {
      userCollect.value = [...userCollect.value, ...collect.info];
      waterFallMore(arrHeight, card_columns_collect, collect.info)
      disabled.value = false;
    }
  }
};
// 主页切换标签结束 ///////////////////////////////////////////////////////////

// 卡片详情页的内容 //////////////////////////////////////////////////////////
const detail = Details.detail
const overlayX = ref(0); // 覆盖层的水平位置
const overlayY = ref(0); // 覆盖层的垂直位置
const overlay = ref(null)
const show = ref(false)

const getDetails = async (id) => Details.getDetail(id)
const showMessage = async (id, left, top) => {
  window.history.pushState({}, "", `/explore/${id}`);
  overlayX.value = left;
  overlayY.value = top;
  await getDetails(id);
  show.value = true;
};
const afterDoComment = (comment) => Details.afterDoComment(comment)
const close = () => {
  window.history.pushState({}, '', `/user/index/${userInfo.value.user.id}`);
  document.title = userInfo.value.user.username
  show.value = false
}
onClickOutside(overlay, () => {
  window.history.pushState({}, "", `/user/index/${userInfo.value.user.id}`);
  document.title = userInfo.value.user.username
  show.value = false;
});
let style = null;
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
  document.head.appendChild(style);
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
    document.head.removeChild(style);
    style = null;
  }
}
// 卡片详情页的内容结束 //////////////////////////////////////////////////////////
const resize = () => {
  if (radio.value === '帖子') {
    resizeWaterFall(columns, card_columns_posts, arrHeight, userPost)
  } else if (radio.value === '收藏') {
    resizeWaterFall(columns, card_columns_collect, arrHeight, userCollect)
  } else if (radio.value === '点赞') {
    resizeWaterFall(columns, card_columns_like, arrHeight, userFavorite)
  }
}
onMounted(async () => {
  await getUserInfo()
  // 确保 userFocus 被初始化
  if (!userStore.userFocus.value) {
    userStore.userFocus.value = []
    // 获取关注列表
    try {
      const focusResult = await queryUserFocus()
      if (focusResult && focusResult.follow) {
        userStore.userFocus.value = focusResult.follow
      }
    } catch (error) {
      console.error('获取关注列表失败:', error)
    }
  }
  await Toggle()
  resize()
})

// 添加状态控制
const hoverButton = ref(false)

// 修改关注状态的按钮文本
const buttonText = computed(() => {
  if (!userStore.userFocus.value || !checkFollow(userInfo.value?.user?.id)) {
    return '关注'
  }
  return hoverButton.value ? '取消关注' : '已关注'
})



// 添加取消关注函数
const cancelFocus = async (id) => {
  try {
    const res = await unFollow({id})  // 修改为正确的函数名
    // 更新状态
    userStore.removeFocus(1, id)
    userInfo.value.user.fans -= 1
    
    // 重新获取用户关注列表以确保状态同步
    const focusResult = await queryUserFocus()
    userStore.userFocus.value = focusResult.follow
    
    ElMessage({type: 'success', message: res.info})
  } catch(error) {
    ElMessage({type: 'error', message: '取消关注失败'})
  }
}

// 统一的关注操作处理
const handleFocus = async (id) => {
  if(checkFollow(id)) {
    await cancelFocus(id)
  } else {
    await doFocusOn(id)
  }
}

// 在 script setup 中添加
const isOwnProfile = computed(() => {
  return userStore.userInfo && userInfo.value?.user && userStore.userInfo.id === userInfo.value.user.id
})

const dialogFormVisible = ref(false)
const upload = ref(null)
const avatar = ref('')
const fileList = ref([])
const form = ref({
  username: '',
  signature: ''
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
    ElMessage.error('请上传正确的图片文件!')
    fileList.value = []
    return false
  } 
  
  if (uploadFile.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`文件大小最多${maxSize}MB!`)
    fileList.value = []
    return false
  }

  // 直接更新 fileList
  fileList.value = [uploadFile]
  return true
}

const closeDialog = async () => {
  dialogFormVisible.value = false;
  await getUserInfo()
  fileList.value = [];
}

const onSuccess = async (response) => {
  avatar.value = response.filepath
  // 刷新用户信息
  await getUserInfo()
}
const onError = async (error) => {
  ElMessage({
    type: 'warning',
    message: '头像上传失败'
  })
  const userStore = useUserStore();
  await userStore.userLogout()
  await router.replace('/')
}

const openDialog = () => {
  dialogFormVisible.value = true
  form.value.username = userStore.userInfo.username
  form.value.signature = userStore.userInfo.signature
}
// 表单验证规则
const rules = {
  username: [
    {required: true, message: '用户名不能为空！', trigger: 'blur'}
  ],
  signature: [
    {required: true, message: '个性签名不能为空!', trigger: 'blur'}
  ]
}
// 表单对象
const formRef = ref(null)
const doUpdate = async () => {
  const {username, signature} = form.value;
  const isModified = username !== userStore.userInfo.username || signature !== userStore.userInfo.signature;
  const isAvatarUploaded = fileList.value.length === 1;

  if (!isModified && !isAvatarUploaded) {
    ElMessage({type: 'warning', message: '未作任何修改！'});
    return;
  }

  try {
    if (isModified && !isAvatarUploaded) {
      await updateUserInfo({username, signature});
      avatar.value = userStore.userInfo.avatar;
      userStore.changeInfo({username, signature, avatar});
      ElMessage({type: 'success', message: '用户信息更新成功'});
      dialogFormVisible.value = false;
      await getUserInfo();
      return;
    }

    if (!isModified && isAvatarUploaded) {
      await upload.value.submit();
      userStore.changeInfo({username, signature, avatar});
      ElMessage({type: 'success', message: '头像上传成功'});
      dialogFormVisible.value = false;
      await getUserInfo();
      return;
    }

    if (isModified && isAvatarUploaded) {
      const res = await updateUserInfo({username, signature});
      await upload.value.submit();
      userStore.changeInfo({username, signature, avatar});
      ElMessage({type: 'success', message: res.info});
      dialogFormVisible.value = false;
      await getUserInfo();
    }
  } catch (error) {
    ElMessage({type: 'error', message: '更新失败，请重试'});
  }
  
};

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
          <el-tag class="ml-2" type="success" round>{{ userInfo.user.focusOn }} 关注</el-tag>
          <el-tag class="ml-2" type="info" round>{{ userInfo.user.fans }} 粉丝</el-tag>
          <el-tag class="ml-2" type="warning" round>{{ userInfo.user.postsCount }} 笔记数</el-tag>
        </div>
      </el-col>
      <el-col :span="5">
        <template v-if="isOwnProfile">
          <el-button 
            type="primary" 
            class="update-btn"
            @click="openDialog">
            更新资料
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
        <el-radio-button class="radio" style="margin: 1vw;" label="帖子" name="post"/>
        <el-radio-button class="radio" style="margin: 1vw;" label="收藏" name="collect"/>
        <el-radio-button class="radio" style="margin: 1vw;" label="点赞" name="like"/>
    </el-radio-group>
  </template>
  </div>


  <div v-if="userInfo.user">
    <div v-if="radio === '帖子'">
      <div v-if="userPost.length === 0">
        <el-empty description="现在还没有帖子..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_posts" @show-detail="showMessage"></home-card>
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
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay"/>
        </div>
      </transition>
    </div>
    <div v-else-if="radio === '收藏'">
      <div v-if="userCollect.length === 0">
        <el-empty description="现在还没有收藏..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_collect" ref="overlay" @show-detail="showMessage"></home-card>
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
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay"/>
        </div>
      </transition>
    </div>
    <div v-else-if="radio === '点赞'">
      <div v-if="userFavorite.length === 0">
        <el-empty description="现在还没有点赞..."/>
      </div>
      <div v-infinite-scroll="load" :infinite-scroll-disabled="disabled" :infinite-scroll-delay="200"
           :infinite-scroll-distance="100"
           v-else>
        <home-card :card_columns="card_columns_like" @show-detail="showMessage"></home-card>
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
          <card-detail :detail="detail" @afterDoComment="afterDoComment" ref="overlay"/>
        </div>
      </transition>
    </div>

    <!-- 添加更新个人信息的弹窗 -->
        <el-dialog 
        v-model="dialogFormVisible" 
        title="" 
        @closed="closeDialog"
        center 
        draggable
        class="update-info-dialog"
        style="width: 30%;"
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
        <el-form-item prop="username" label="昵称" label-width="7vw" style="margin: 2vw;font-size: 100%;">
          <el-input v-model="form.username" maxlength="6"
                    show-word-limit class="my"/>
        </el-form-item>
        <el-form-item prop="signature" label="个性签名" label-width="7vw" style="margin: 2vw;">
          <el-input v-model="form.signature" class="my"/>
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="closeDialog" round>取消</el-button>
        <el-button type="primary" @click="doUpdate" round>
          确认
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
@media screen and (max-width: 768px) {
 .userInfo {
   padding: 20px;
 }

 .el-row {
   flex-direction: column;
   align-items: center;
 }

 .el-col {
   width: 100% !important;
   margin-bottom: 20px;
   display: flex;
   flex-direction: column;
   align-items: center;
   text-align: center;
 }

 .el-avatar {
   width: 15vw;
   height: 15vw;
 }

 .tagArea {
   display: flex;
   justify-content: center;
   gap: 10px;
   flex-wrap: wrap;
   margin-top: 10px;
 }

 .update-btn,
 .focusOn {
   margin-top: 10px;
   width: 120px;
 }
}

.focusOn {
  align-items: center;
  justify-content: center;
  width: 6vw;
  height: 2.5vw;
  font-weight: 600;
  font-size: 100%;
  min-width: 60px;
  min-height: 25px;
  cursor: pointer;
  background-color: red;
  border-radius: 1000px;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
  transition: all 0.3s;
}

.focusOn:hover {
  background-color: #fd5656;
}

/* 已关注状态 */
.focusOn.followed {
  background-color: #f4f4f5;
  color: #909399;
}

/* 已关注状态下的hover效果 */
.focusOn.followed:hover {
  background-color: #f56c6c;
  color: #fff;
}

.tagArea {
  width: 40vw;
}

.tagArea .ml-2 {
  margin-right: 1vw;
}

.checkBox {
  margin-top: 2vh;
  position: relative;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 9999;
}

.backPage {
  position: fixed;
  top: 3%;
  left: 3%;
  justify-content: center;
  align-items: center;
  width: 4vw;
  height: 4vw;
  max-width: 45px;
  max-height: 45px;
  border-radius: 40px;
  cursor: pointer;
  transition: all .3s;
}

@media screen and (max-width: 768px) {
 .backPage {
   top: 2%;
   left: 2%;
   width: 4vh;
   height: 4vh;
   border-radius: 35px;
 }
}

.fade-enter-active {
  animation: scale-up-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

.fade-leave-active {
  animation: scale-up-center 0.5s linear both reverse;
}

.update-btn {
  align-items: center;
  justify-content: center;
  width: 6vw;
  height: 2.5vw;
  font-weight: 600;
  font-size: 1.1vw;
  min-width: 60px;
  min-height: 25px;
  cursor: pointer;
  background-color: red;
  border-radius: 1000px;
  color: #fff;
  border-color: transparent;
  margin-top: 1rem;
  transition: all 0.3s;
}
@media screen and (max-width: 768px) {
 .update-btn {
  font-size: 80%;

 }
}
.update-btn:hover {
  background-color: #fd5656;
}

:deep(.el-dialog__title) {
  width: 100%;
  text-align: center;
  display: block;
}

/* 上传区域容器样式 */
.upload-container {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
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
  margin: 0 auto; /* 确保水平居中 */
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

/* 确保文件上传区域居中 */
.fileUpload {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}


</style>