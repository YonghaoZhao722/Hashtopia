<script setup>
import { LazyImg, Waterfall } from 'vue-waterfall-plugin-next'
import 'vue-waterfall-plugin-next/dist/style.css'

const props = defineProps({
  list: {
    type: Array,
    required: true
  }
})

const emit = defineEmits(['show-detail'])
const details = (id, event) => {
  const target = event.target;
  const rect = target.getBoundingClientRect();
  emit('show-detail', id, rect.left, rect.top)
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
            <LazyImg :url="item.img" class="image" />
          </a>
          <div class="card-content">
            <div class="card-title-container">
              <span class="card-title" @click="(e) => details(item.id, e)">{{ item.title }}</span>
            </div>
            <div class="bottom">
              <el-row class="user-info">
                <RouterLink :to="`/user/index/${item.user.id}`">
                  <el-avatar :src="item.user.avatar" size="small" />
                </RouterLink>
                <div class="username">{{ item.user.username }}</div>
              </el-row>
            </div>
          </div>
        </div>
      </template>
    </Waterfall>
    <div class="bottom-space"></div>
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
  -webkit-line-clamp: 2;
}

.card-title {
  font-weight: 800;
  font-size: 0.875rem;
  cursor: pointer;
  margin: 0;
  line-height: 1.2;
}

.bottom-space {
  height: 10vh; 
  width: 100%;
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
</style>