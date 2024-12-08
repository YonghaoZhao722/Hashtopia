<!-- src/views/HomeView.vue -->
<template>
  <div class="home">
    <div class="post-grid">
      <div v-for="post in posts" :key="post.id" class="post-card">
        <el-card :body-style="{ padding: '0px' }">
          <img :src="post.image" class="post-image">
          <div class="post-content">
            <div class="post-title">{{ post.title }}</div>
            <div class="post-info">
              <el-avatar :size="24" :src="post.author.avatar" />
              <span class="author-name">{{ post.author.name }}</span>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const posts = ref([
  {
    id: 1,
    title: 'Amazing Travel Experience',
    image: 'https://picsum.photos/300/400',
    author: {
      name: 'John Doe',
      avatar: 'https://picsum.photos/40/40'
    }
  },
  {
    id: 2,
    title: 'Delicious Food Review',
    image: 'https://picsum.photos/300/400?random=2',
    author: {
      name: 'Jane Smith',
      avatar: 'https://picsum.photos/40/40?random=2'
    }
  },
  // 添加更多测试数据...
])
</script>

<style scoped>
.post-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  padding: 20px;
}

.post-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.post-card:hover {
  transform: translateY(-5px);
}

.post-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.post-content {
  padding: 14px;
}

.post-title {
  font-size: 16px;
  margin-bottom: 8px;
}

.post-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-size: 14px;
  color: #666;
}
</style>