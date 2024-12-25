<script setup>
import {onMounted, ref, nextTick,watch} from "vue";
import HomeCard from "@/components/homeCard.vue";
import {Back} from "@element-plus/icons-vue";
import CardDetail from "@/components/cardDetail.vue";
import {queryPost} from "@/apis/main";
import {useRoute} from "vue-router";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from '@vueuse/core';

const query = ref(useRoute().query.query || '')
const Details = controlDetail()

// Card //////////////////////////////////////////////////////////////////
const cards = ref([]);
const loading = ref(false); 
const hasMore = ref(true);

const doQuery = async (offset) => {
 const res = await queryPost({
   offset,
   query: query.value
 });
 cards.value = res.info;
 hasMore.value = res.has_more;
};

const pageSize = 10;
const loadMore = async () => {
  if (loading.value || !hasMore.value) return;
  
  loading.value = true;
  try {
    const offset = cards.value.length;
    const res = await queryPost({
      offset,
      query: query.value 
    });
    const more = res.info;
    
    if (more.length < pageSize) {
      hasMore.value = false;
    }
    if (more.length > 0) {
      cards.value = [...cards.value, ...more];
    }
  } catch (error) {
    console.error('加载失败:', error);
  } finally {
    loading.value = false;
  }
};

watch(() => useRoute().query.query, async (newQuery) => {
  query.value = newQuery || '';
  await doQuery(0);
}, { immediate: true });

// Detail //////////////////////////////////////////////////////////////////
const detail = Details.detail;
const show = ref(false);
const overlayX = ref(0);
const overlayY = ref(0);
const overlay = ref(null)

const getDetails = async (id) => Details.getDetail(id)
const showMessage = async (id, left, top) => {
  console.log('showMessage called', { id, left, top }); // 添加日志
  
  sessionStorage.setItem('cardDetailSource', window.location.pathname);
  window.history.pushState({}, "", `/explore/${id}`);
  
  // 确保这里的值是正确的
  overlayX.value = left;
  overlayY.value = top;
  
  await getDetails(id);
  show.value = true;
  await nextTick();
};

const reopenDetail = async (postId) => {
  // 获取当前卡片的位置信息
  const card = document.querySelector(`[data-post-id="${postId}"]`);
  if (card) {
    const rect = card.getBoundingClientRect();
    await showMessage(postId, rect.left, rect.top);
  } else {
    // 如果找不到卡片，使用默认位置
    await showMessage(postId, window.innerWidth / 2, window.innerHeight / 2);
  }
};
const afterDoComment = (comment) => Details.afterDoComment(comment);

onClickOutside(overlay, () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = 'Welcome to Hashtopia'
});

let style = null;
const onBeforeEnter = (el) => {
  // 获取点击的卡片元素
  const card = document.querySelector(`[data-post-id="${detail.value.id}"]`);
  if (!card) {
    console.log('Card not found, using fallback animation');
    // 如果找不到卡片，使用基础动画作为后备方案
    style = document.createElement('style');
    style.innerHTML = `
      @keyframes scale-up-center {
        0% {
          transform: translate(${overlayX.value}px, ${overlayY.value}px) scale(0.5);
          transform-origin: 0 0;
          opacity: 0.5;
        }
        100% {
          transform: translate(0, 0) scale(1);
          transform-origin: 0 0;
          opacity: 1;
        }
      }
    `;
    document.head.appendChild(style);
    return;
  }

  // 获取卡片和窗口的尺寸信息
  const cardRect = card.getBoundingClientRect();
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;

  // 计算缩放比例
  const scaleX = cardRect.width / windowWidth;
  const scaleY = cardRect.height / windowHeight;
  const scale = Math.max(scaleX, scaleY); // 使用较大的缩放比例确保完整覆盖

  // 计算位置偏移
  const translateX = cardRect.left;
  const translateY = cardRect.top;

  style = document.createElement('style');
  style.innerHTML = `
    @keyframes scale-up-center {
      0% {
        transform: translate(${translateX}px, ${translateY}px) scale(${scale});
        opacity: 0.9;
      }
      20% {
        transform: translate(${translateX}px, ${translateY}px) scale(${scale});
        opacity: 0.95;
      }
      100% {
        transform: translate(0, 0) scale(1);
        opacity: 1;
      }
    }
  `;
  document.head.appendChild(style);

  // 设置初始状态
  el.style.transformOrigin = '0 0';
};

const addBackPage = () => {
  nextTick(() => {
    const backButton = document.querySelector('.backPage');
    if (backButton) {
      backButton.style.display = 'block';
    }
  });
};

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


const onAfterEnter = (el) => {
  el.style = 'background-color: #fff';
  const backButton = el.querySelector('.backPage');
  if (backButton) {
    backButton.style.display = '';
  }
};

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

const route = useRoute();

onMounted(async () => {
  await doQuery(0);
  if (window.location.pathname.includes('/explore/')) {
    const id = window.location.pathname.split('/').pop();
    await getDetails(id);
    show.value = true;
    await nextTick();
    addBackPage();
  }
  const postId = route.params.id;
  if (postId && sessionStorage.getItem('cardDetailSource')) {
    await reopenDetail(postId);
  }
  const currentPath = window.location.pathname;
  if (currentPath.includes('/explore/')) {
    const postId = currentPath.split('/').pop();
    if (postId) {
      await getDetails(postId);
      show.value = true;
      await nextTick();
    }
  }
});


</script>

<template>
  <div class="Empty" v-if="cards.length === 0">
    <el-empty description="No posts..."/>
  </div>
  <div v-else>
    <home-card :list="cards" 
  :loading="loading"
  :has-more="hasMore"
  @show-detail="showMessage"
  @load-more="loadMore"
  ref="homeCardRef"></home-card>
    
    

  <transition
      name="fade"
      @before-enter="onBeforeEnter"
      @after-enter="onAfterEnter"
      @before-leave="onBeforeLeave"
      @after-leave="onAfterLeave"
  >
    <div class="overlay" v-if="show" @click.self="handleOverlayClose">
      <button class="backPage" aria-label="Back" @click="handleOverlayClose">
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
</template>

<style scoped>
.Empty {
  margin-top: 10%;
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



.card-detail {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  margin-top: 48px;
}


.load-more-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
  padding: 10px;
}

.load-more-btn {
  min-width: 120px;
}

.no-more {
  color: #909399;
  font-size: 14px;
  text-align: center;
}

@media screen and (max-width: 768px) {
  .backPage {
    top: 12px;
    left: 2%;
    border-radius: 35px;
  }
}

.fade-enter-active {
  animation: scale-up-center 0.4s cubic-bezier(0.33, 1, 0.68, 1) both;
}

.fade-leave-active {
  animation: scale-up-center 0.4s cubic-bezier(0.32, 0, 0.67, 0) both reverse;
}
</style>