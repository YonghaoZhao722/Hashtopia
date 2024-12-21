<script setup>
import {useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.js";
import {computed, onBeforeMount, ref} from "vue";
import {Back, Plus, Upload} from '@element-plus/icons-vue'
import {ElMessage} from "element-plus";
import {uploadPost} from "@/apis/main";

const router = useRouter()
const userStore = useUserStore()

// 登录检查
const checkLogin = () => {
  if (!userStore.userInfo.id) {
    router.replace('/login')
  }
}
onBeforeMount(() => checkLogin())

// 文件和表单数据
const fileList = ref([])
const fileListUrl = computed(() => fileList.value.map(item => item.url))
const title = ref('')
const content = ref('')
const postId = ref(0)
const upload = ref(null)

// 控制编辑区域显示
const showEditArea = computed(() => {
  return fileList.value.length > 0
})

// 拖拽上传区域
const isDragging = ref(false)
const handleDrop = async (e) => {
  e.preventDefault()
  isDragging.value = false
  
  const files = Array.from(e.dataTransfer.files)
  for (const file of files) {
    const isValid = await validateFile(file)
    if (isValid) {
      const reader = new FileReader()
      reader.onload = (e) => {
        fileList.value.push({
          raw: file,
          url: e.target.result
        })
      }
      reader.readAsDataURL(file)
    }
  }
}

const validateFile = (file) => {
  return new Promise((resolve) => {
    const allowedTypes = ['image/jpeg', 'image/png']
    const maxSize = 2 // MB
    
    if (!file) {
      ElMessage.error('文件不能为空!')
      resolve(false)
      return
    }

    // 检查是否是图片文件
    const isImage = file.type.startsWith('image/')
    if (!isImage) {
      ElMessage.error('请上传图片文件!')
      resolve(false)
      return
    }

    // 检查文件类型
    if (!allowedTypes.includes(file.type)) {
      ElMessage.error('只支持 JPG/PNG 格式的图片!')
      resolve(false)
      return
    }

    // 检查文件大小
    if (file.size / 1024 / 1024 > maxSize) {
      ElMessage.error(`文件大小不能超过 ${maxSize}MB!`)
      resolve(false)
      return
    }

    // 检查文件数量
    if (fileList.value.length >= 9) {
      ElMessage.warning('最多只能上传9张图片!')
      resolve(false)
      return
    }

    // 创建图片对象验证
    const img = new Image()
    img.src = URL.createObjectURL(file)
    img.onload = () => {
      URL.revokeObjectURL(img.src)
      resolve(true)
    }
    img.onerror = () => {
      URL.revokeObjectURL(img.src)
      ElMessage.error('文件不是有效的图片!')
      resolve(false)
    }
  })
}

// 图片预览
const dialogImageUrl = ref('')
const dialogVisible = ref(false)
const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url
  dialogVisible.value = true
}

// 发布帖子
const doUploads = async () => {
  if (title.value === '') {
    ElMessage.warning('请输入标题')
    return
  }
  if (fileList.value.length === 0) {
    ElMessage.warning('请至少上传一张图片!')
    return
  }

  try {
    // 1. 先上传文字内容
    const postData = {
      title: title.value,
      content: content.value,
      user_id: userStore.userInfo.id,
    }
    const res = await uploadPost(postData)
    postId.value = res.info
    
    // 2. 上传图片
    upload.value.submit()
    
    ElMessage({type: 'success', message: 'Post Successfully'})
    setTimeout(() => {
      router.replace('/')
    }, 1000)
  } catch (error) {
    ElMessage.error('发布失败,请重试')
  }
}

const handleChange = (file, fileList) => {
  const allowedTypes = ['image/jpeg', 'image/png']
  const maxSize = 2 // 最大2MB

  // 检查文件类型
  if (!file.raw.type.startsWith('image/')) {
    ElMessage.error('只允许上传图片文件!')
    fileList.pop() // 移除不合法的文件
    return
  }

  if (!allowedTypes.includes(file.raw.type)) {
    ElMessage.error('文件格式不支持，请上传 JPG 或 PNG 格式!')
    fileList.pop() // 移除不合法的文件
    return
  }

  // 检查文件大小
  if (file.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`文件大小不能超过 ${maxSize}MB!`)
    fileList.pop() // 移除不合法的文件
    return
  }

}


</script>

<template>
  <div class="upload-container">
    <!-- 图片上传区 -->
    <div class="upload-area">
      <h2 class="upload-title">图片编辑 ({{ fileList.length }}/9)</h2>
      <div class="drop-zone" 
           :class="{ 'is-dragover': isDragging }"
           @dragover.prevent="isDragging = true"
           @dragleave.prevent="isDragging = false"
           @drop="handleDrop">
        
          <el-upload
              v-model:file-list="fileList"
              action="http://localhost:8000/upload/"
              ref="upload"
              :on-change="handleChange"
              list-type="picture-card"
              multiple
              :headers="userStore.headersObj"
              :limit="9"
              :on-preview="handlePictureCardPreview"
              :auto-upload="false"
              :data="{id: postId}"
          >
          <template #default>
            <el-icon><Plus /></el-icon>
          </template>
        </el-upload>
      </div>
    </div>

    <!-- 文本编辑区域 - 仅在上传图片后显示 -->
    <transition name="fade">
      <div v-if="showEditArea" class="edit-area">
        <div class="title-input">
          <el-input
              v-model="title"
              maxlength="64"
              placeholder="填写标题会有更多赞哦~"
              show-word-limit
              type="text"
          />
        </div>
        
        <div class="content-input">
          <el-input
              v-model="content"
              maxlength="1000"
              placeholder="输入正文描述，真诚有价值的分享才人温暖"
              show-word-limit
              type="textarea"
              :rows="6"
          />
        </div>
        
        <div class="button-group">
          <el-button type="primary" @click="doUploads">发布</el-button>
        </div>
      </div>
    </transition>
  </div>

  <!-- 图片预览弹窗 -->
  <el-dialog v-model="dialogVisible">
    <img :src="dialogImageUrl" alt="Preview Image" style="width: 100%"/>
  </el-dialog>
</template>

<style scoped>
.upload-container {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.upload-title {
  font-size: 16px;
  color: #333;
  margin-bottom: 20px;
}

.upload-area {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.drop-zone {
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
}

.drop-zone.is-dragover {
  border-color: #409eff;
  background-color: rgba(64, 158, 255, 0.1);
}

.upload-text {
  color: #909399;
  font-size: 14px;
  text-align: center;
  margin-top: 8px;
}

/* 编辑区域样式 */
.edit-area {
  margin-top: 20px;
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.title-input {
  margin-bottom: 20px;
}

.content-input {
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.el-upload--picture-card) {
  --el-upload-picture-card-size: 100px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  --el-upload-list-picture-card-size: 100px;
}
</style>