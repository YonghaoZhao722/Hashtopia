<script setup>
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.js";
import { computed, onBeforeMount, ref } from "vue";
import { Back, Plus, Upload } from '@element-plus/icons-vue';
import { ElMessage } from "element-plus";
import { uploadPost } from "@/apis/main";

const router = useRouter();
const userStore = useUserStore();

// Login check
const checkLogin = () => {
  if (!userStore.userInfo.id) {
    router.replace('/login');
  }
};
onBeforeMount(() => checkLogin());

// File and form data
const fileList = ref([]);
const fileListUrl = computed(() => fileList.value.map(item => item.url));
const title = ref('');
const content = ref('');
const postId = ref(0);
const upload = ref(null);
const baseURL = import.meta.env.VITE_API_BASE_URL

// Control the visibility of the edit area
const showEditArea = computed(() => {
  return fileList.value.length > 0;
});

// Drag-and-drop upload area
const isDragging = ref(false);
const handleDrop = async (e) => {
  e.preventDefault();
  isDragging.value = false;

  const files = Array.from(e.dataTransfer.files);
  for (const file of files) {
    const isValid = await validateFile(file);
    if (isValid) {
      const reader = new FileReader();
      reader.onload = (e) => {
        fileList.value.push({
          raw: file,
          url: e.target.result,
        });
      };
      reader.readAsDataURL(file);
    }
  }
};

const validateFile = (file) => {
  return new Promise((resolve) => {
    const allowedTypes = ['image/jpeg', 'image/png'];
    const maxSize = 2; // MB

    if (!file) {
      ElMessage.error('File cannot be empty!');
      resolve(false);
      return;
    }

    // Check if the file is an image
    const isImage = file.type.startsWith('image/');
    if (!isImage) {
      ElMessage.error('Please upload an image file!');
      resolve(false);
      return;
    }

    // Check file type
    if (!allowedTypes.includes(file.type)) {
      ElMessage.error('Only JPG/PNG formats are supported!');
      resolve(false);
      return;
    }

    // Check file size
    if (file.size / 1024 / 1024 > maxSize) {
      ElMessage.error(`File size cannot exceed ${maxSize}MB!`);
      resolve(false);
      return;
    }

    // Check the number of files
    if (fileList.value.length >= 9) {
      ElMessage.warning('You can only upload up to 9 images!');
      resolve(false);
      return;
    }

    // Validate the image object
    const img = new Image();
    img.src = URL.createObjectURL(file);
    img.onload = () => {
      URL.revokeObjectURL(img.src);
      resolve(true);
    };
    img.onerror = () => {
      URL.revokeObjectURL(img.src);
      ElMessage.error('The file is not a valid image!');
      resolve(false);
    };
  });
};

// Image preview
const dialogImageUrl = ref('');
const dialogVisible = ref(false);
const handlePictureCardPreview = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url;
  dialogVisible.value = true;
};

// Publish post
const doUploads = async () => {
  if (title.value === '') {
    ElMessage.warning('Please enter a title');
    return;
  }
  if (fileList.value.length === 0) {
    ElMessage.warning('Please upload at least one image!');
    return;
  }

  try {
    // 1. Upload text content first
    const postData = {
      title: title.value,
      content: content.value,
      user_id: userStore.userInfo.id,
    };
    const res = await uploadPost(postData);
    postId.value = res.info;

    // 2. Upload images
    upload.value.submit();

    ElMessage({ type: 'success', message: 'Post Successfully' });
    setTimeout(() => {
      router.replace('/');
    }, 3000);
  } catch (error) {
    ElMessage.error('Failed to post, please try again');
  }
};

const handleChange = (file, fileList) => {
  const allowedTypes = ['image/jpeg', 'image/png'];
  const maxSize = 2; // Maximum 2MB

  // Check file type
  if (!file.raw.type.startsWith('image/')) {
    ElMessage.error('Only image files are allowed!');
    fileList.pop(); // Remove invalid file
    return;
  }

  if (!allowedTypes.includes(file.raw.type)) {
    ElMessage.error('Unsupported file format. Please upload JPG or PNG!');
    fileList.pop(); // Remove invalid file
    return;
  }

  // Check file size
  if (file.raw.size / 1024 / 1024 > maxSize) {
    ElMessage.error(`File size cannot exceed ${maxSize}MB!`);
    fileList.pop(); // Remove invalid file
    return;
  }
};
</script>

<template> 
<el-container class="page-container">
  <el-main class="scrollable-main">
  <div class="upload-container">
    <!-- Image Upload Area -->
    <div class="upload-area">
      <h2 class="upload-title">Image Editing ({{ fileList.length }}/9)</h2>
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

    <!-- Text Editing Area - Displayed only after images are uploaded -->
    <transition name="fade">
      <div v-if="showEditArea" class="edit-area">
        <div class="title-input">
          <el-input
              v-model="title"
              maxlength="64"
              placeholder="Adding a title can get more likes~"
              show-word-limit
              type="text"
          />
        </div>
        
        <div class="content-input">
          <el-input
              v-model="content"
              maxlength="3000"
              placeholder="Say something..."
              show-word-limit
              type="textarea"
              :rows="6"
          />
        </div>
        
        <div class="button-group">
          <el-button type="primary" @click="doUploads">Post</el-button>
        </div>
      </div>
    </transition>
  </div>

  <!-- Image Preview Modal -->
  <el-dialog v-model="dialogVisible">
    <img :src="dialogImageUrl" alt="Preview Image" style="width: 100%;"/>
  </el-dialog>
  </el-main>
</el-container>
</template>

<style scoped>
.page-container {
  height: 90vh;
}

.scrollable-main {
  height: 100%;
  overflow-y: auto;
  padding: 0;
}

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
  padding: 2vw;
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

/* Styling for the editing area */
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

/* Transition animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

:deep(.el-upload--picture-card) {
  --el-upload-picture-card-size: 10vw;
}
:deep(.el-upload-list__item){
  width: 10vw;
  height: 10vw;
}
:deep(.el-upload-list--picture-card .el-upload-list__item) {
}
</style>
