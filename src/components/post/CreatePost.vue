<!-- CreatePost.vue -->
<template>
    <div class="create-post-container">
      <el-card class="post-card">
        <template #header>
          <div class="card-header">
            <h2>Create New Post</h2>
          </div>
        </template>
  
        <el-form :model="postForm" :rules="rules" ref="postFormRef">
          <!-- Image Upload -->
          <el-form-item prop="images">
            <el-upload
              v-model:file-list="postForm.images"
              action="#"
              list-type="picture-card"
              :auto-upload="false"
              :limit="9"
              :on-change="handleImageChange"
            >
              <template #default>
                <el-icon><Plus /></el-icon>
              </template>
            </el-upload>
          </el-form-item>
  
          <!-- Title -->
          <el-form-item prop="title">
            <el-input
              v-model="postForm.title"
              placeholder="Give your post a title"
              maxlength="100"
              show-word-limit
            />
          </el-form-item>
  
          <!-- Content -->
          <el-form-item prop="content">
            <el-input
              v-model="postForm.content"
              type="textarea"
              placeholder="Share your story..."
              :rows="4"
              maxlength="2000"
              show-word-limit
            />
          </el-form-item>
  
          <!-- Tags -->
          <el-form-item prop="tags">
            <el-tag
              v-for="tag in postForm.tags"
              :key="tag"
              closable
              :disable-transitions="false"
              @close="handleTagClose(tag)"
              class="tag"
            >
              #{{ tag }}
            </el-tag>
            <el-input
              v-if="inputTagVisible"
              ref="tagInputRef"
              v-model="inputTagValue"
              class="tag-input"
              size="small"
              @keyup.enter="handleInputConfirm"
              @blur="handleInputConfirm"
            />
            <el-button
              v-else
              class="button-new-tag"
              size="small"
              @click="showTagInput"
            >
              + New Tag
            </el-button>
          </el-form-item>
  
          <!-- Submit Button -->
          <el-form-item>
            <el-button
              type="primary"
              :loading="loading"
              @click="submitPost"
            >
              Post
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, reactive } from 'vue'
  import { Plus } from '@element-plus/icons-vue'
  import { ElMessage } from 'element-plus'
  
  const postFormRef = ref(null)
  const tagInputRef = ref(null)
  const inputTagVisible = ref(false)
  const inputTagValue = ref('')
  const loading = ref(false)
  
  const postForm = reactive({
    title: '',
    content: '',
    images: [],
    tags: []
  })
  
  const rules = {
    title: [
      { required: true, message: 'Please enter a title', trigger: 'blur' },
      { min: 3, max: 100, message: 'Length should be 3 to 100 characters', trigger: 'blur' }
    ],
    content: [
      { required: true, message: 'Please enter content', trigger: 'blur' },
      { min: 10, max: 2000, message: 'Length should be 10 to 2000 characters', trigger: 'blur' }
    ],
    images: [
      { required: true, message: 'Please upload at least one image', trigger: 'change' }
    ]
  }
  
  const handleImageChange = (uploadFile) => {
    // Handle image validation here
    const isImage = uploadFile.raw.type.startsWith('image/')
    if (!isImage) {
      ElMessage.error('Please upload image files only!')
      return false
    }
    const isLt5M = uploadFile.raw.size / 1024 / 1024 < 5
    if (!isLt5M) {
      ElMessage.error('Image must be smaller than 5MB!')
      return false
    }
    return true
  }
  
  const handleTagClose = (tag) => {
    postForm.tags = postForm.tags.filter(t => t !== tag)
  }
  
  const showTagInput = () => {
    inputTagVisible.value = true
    nextTick(() => {
      tagInputRef.value.focus()
    })
  }
  
  const handleInputConfirm = () => {
    if (inputTagValue.value) {
      const tag = inputTagValue.value.trim().toLowerCase()
      if (!postForm.tags.includes(tag)) {
        if (postForm.tags.length < 10) {
          postForm.tags.push(tag)
        } else {
          ElMessage.warning('Maximum 10 tags allowed')
        }
      }
    }
    inputTagVisible.value = false
    inputTagValue.value = ''
  }
  
  const submitPost = async () => {
    if (!postFormRef.value) return
    
    await postFormRef.value.validate(async (valid) => {
      if (valid) {
        try {
          loading.value = true
          // Format data for API
          const formData = new FormData()
          formData.append('title', postForm.title)
          formData.append('content', postForm.content)
          postForm.images.forEach((file, index) => {
            formData.append(`image${index}`, file.raw)
          })
          formData.append('tags', JSON.stringify(postForm.tags))
  
          // API call would go here
          // await api.posts.create(formData)
  
          ElMessage.success('Post created successfully!')
          // Reset form
          postFormRef.value.resetFields()
          postForm.images = []
          postForm.tags = []
        } catch (error) {
          ElMessage.error('Failed to create post. Please try again.')
          console.error('Error creating post:', error)
        } finally {
          loading.value = false
        }
      }
    })
  }
  </script>
  
  <style scoped>
  .create-post-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 0 20px;
  }
  
  .post-card {
    background: var(--el-color-white);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .card-header h2 {
    margin: 0;
    color: var(--el-text-color-primary);
  }
  
  .tag {
    margin-right: 8px;
    margin-bottom: 8px;
  }
  
  .tag-input {
    width: 90px;
    margin-right: 8px;
    vertical-align: bottom;
  }
  
  .button-new-tag {
    margin-right: 8px;
    height: 32px;
    padding-top: 0;
    padding-bottom: 0;
  }
  
  :deep(.el-upload--picture-card) {
    --el-upload-picture-card-size: 100px;
  }
  
  :deep(.el-form-item__content) {
    flex-wrap: wrap;
  }
  </style>