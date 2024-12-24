<script setup>
import { LazyImg, Waterfall } from 'vue-waterfall-plugin-next'
import 'vue-waterfall-plugin-next/dist/style.css'

const props = defineProps({
  list: {
    type: Array,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  },
  hasMore: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['show-detail', 'load-more'])

const details = (id, event) => {
  const target = event.target;
  const rect = target.getBoundingClientRect();
  emit('show-detail', id, rect.left, rect.top)
}

const handleLoadMore = () => {
  emit('load-more')
}
</script>

<template>
  <div class="page-container">
    <Waterfall 
      :list="list" 
      :width="250"
      :gutter="20"
      imgSelector="img"
      :breakpoints="{
        1200: { rowPerView: 4 },
        900: { rowPerView: 3 },
        600: { rowPerView: 2 },
        400: { rowPerView: 1 }
      }"
    >
      <template #default="{ item, url, index }">
        <div class="card">
          <a :href="`/explore/${item.id}`" @click.prevent="(e) => details(item.id, e)">
            <LazyImg :url="item.img" class="image" :alt="`post_${item.id}_img`"/>
          </a>
          <div class="card-content">
            <div class="card-title-container">
              <span class="card-title" @click="(e) => details(item.id, e)">{{ item.title }}</span>
            </div>
            <div class="bottom">
              <el-row class="user-info">
                <RouterLink :to="`/user/index/${item.user.id}`">
                  <el-avatar :src="item.user.avatar" size="small" :alt="`user_${item.user.id}_avatar`" />
                </RouterLink>
                <RouterLink :to="`/user/index/${item.user.id}`">
                 <div class="username">{{ item.user.username }}</div>
                </RouterLink>
              </el-row>
            </div>
          </div>
        </div>
      </template>
    </Waterfall>

    <!-- Load more -->
    <div class="load-more-container">
      <el-button
        v-if="hasMore"
        :loading="loading"
        @click="handleLoadMore"
        class="load-more-btn"
      >
        {{ loading ? 'Loading...' : 'Load More' }}
      </el-button>
      <div v-else class="no-more">No More Posts...</div>
      <div class="bottom-space"></div>
    </div>
  </div>
</template>

<style scoped>
.page-container {
  width: 100%;
  height: 100vh;
  overflow-y: auto;
  position: relative;
}

.card {
  width: 100%;
  border-radius: 0.8rem;
  background-color: white;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

a {
  text-decoration: none;
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
  font-weight: 400;
  font-size: 0.875rem;
  cursor: pointer;
  margin: 0;
  line-height: 1.2;
}

.load-more-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  padding: 10px;
  
}

.load-more-btn {
  align-items: center;
  justify-content: center;
  width: 4.8vw;
  height: 2vw;
  font-weight: 600;
  font-size: 0.8vw;

  min-width: 60px;
  min-height: 25px;
  cursor: pointer;
  background-color: #cc0000; /* Darkened red for better contrast */
  border-radius: 1000px;
  color: #ffffff; /* Kept white for strong contrast */
  border-color: transparent;
  margin-top: 1rem;
  transition: all 0.3s;
}

.load-more-btn:hover {
  background-color: #b30000; /* Darker red for hover effect */
}

@media screen and (max-width: 768px) {
 .load-more-btn {
  font-size: 1.2vh;
 }
}
.load-more-btn:hover {
  background-color: #fd5656;
}

.no-more {
  color: black;
  font-size: 14px;
  text-align: center;
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

.bottom-space {
  height: 16vh; 
}

</style>