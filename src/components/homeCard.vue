<script setup>
import {ref} from "vue";

defineProps({
  card_columns: {
    type: Array,
    default: () => [] // Properly define default as empty array
  }
})
const emit = defineEmits(['show-detail'])
const details = (id) => {
  const target = event.target;
  const left = target.x;
  const top = target.y;
  emit('show-detail', id, left, top)
}
const ok = ref(false)
const handleLoad = (card) => {
  card.load = true
}
</script>

<template>
  <div class="page-container">
    <div class="columns-container">
      <div class="column" v-for="col in card_columns" :key="col.id">
        <section v-for="card in col" :key="card.id">
          <div v-show="card.load" class="card">
            <a :href="`/explore/${card.id}`" @click.prevent="details(card.id)">
              <img
                  :src="card.img"
                  class="image"
                  @load="handleLoad(card)"
                  alt=""
              />
            </a>
            <div class="card-content">
              <div class="card-title-container">
                <span class="card-title" @click="details(card.id)">{{ card.title }}</span>
              </div>
              <div class="bottom">
                <el-row class="user-info">
                  <RouterLink :to="`/user/index/${card.user.id}`">
                    <el-avatar
                        :src="card.user.avatar" 
                        size="small"
                    />
                  </RouterLink>
                  <div class="username">{{ card.user.username }}</div>
                </el-row>
              </div>
            </div>
          </div>
          <div v-if="!card.load" class="card loading">
            <div class="image" :style="{height: card.img_info.height / (card.img_info.width / 250) + 'px'}">
            </div>
            <div class="card-content">
              <div class="card-title-container">
                <span class="card-title" @click="details(card.id)">{{ card.title }}</span>
              </div>
              <div class="bottom">
                <el-row class="user-info">
                  <RouterLink :to="`/user/index/${card.user.id}`">
                    <div class="avatar"></div>
                  </RouterLink>
                  <div class="username">{{ card.user.username }}</div>
                </el-row>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
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

.columns-container {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 20px;
  justify-content: center;
  width: 100%;
  min-height: min-content;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

section {
  width: 250px;
  break-inside: avoid;
  margin: 20px 20px 20px 20px;
}

.card {
  width: 250px;
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
  margin-bottom: 10px;
  height: 24px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-title {
  font-size: 1rem;
  cursor: pointer;
}

.loading .image,
.loading .avatar {
  background: gainsboro linear-gradient(
    100deg,
    rgba(255, 255, 255, 0) 40%,
    rgba(255, 255, 255, .5) 50%,
    rgba(255, 255, 255, 0) 60%
  );
  background-size: 200% 100%;
  background-position-x: 180%;
  animation: 1s loading ease-in-out infinite;
}

.loading .avatar {
  border-radius: 50%;
  height: 24px;
  width: 24px;
}

@keyframes loading {
  to {
    background-position-x: -20%;
  }
}

.bottom-space {
  height: 6vh;  /* 底部预留 60px 的滚动空间 */
  width: 100%;
}
</style>