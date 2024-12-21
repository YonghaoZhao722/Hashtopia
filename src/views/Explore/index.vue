<script setup>
import {onMounted, ref, nextTick} from "vue";
import HomeCard from "@/components/homeCard.vue";
import {Back} from "@element-plus/icons-vue";
import CardDetail from "@/components/cardDetail.vue";
import {queryPost} from "@/apis/main";
import {useRoute} from "vue-router";
import {controlDetail} from "@/stores/controlDetail";
import {onClickOutside} from '@vueuse/core';

const query = useRoute().query.query
const Details = controlDetail()

// 主页卡片 //////////////////////////////////////////////////////////////////
const cards = ref([]);
const loading = ref(false); // 加载状态
const hasMore = ref(true); // 是否还有更多数据

// 主页获取帖子
const doQuery = async (offset) => {
  const res = await queryPost({
    offset,
    query
  });
  cards.value = res.info;
  hasMore.value = res.has_more; // 使用后端返回的has_more标志
};

const pageSize = 10;
// 加载更多
const loadMore = async () => {
  if (loading.value || !hasMore.value) return;
  
  loading.value = true;
  try {
    const offset = cards.value.length;
    const res = await queryPost({
      offset,
      query
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

// 卡片详情 //////////////////////////////////////////////////////////////////
const detail = Details.detail;
const show = ref(false);
const overlayX = ref(0);
const overlayY = ref(0);
const overlay = ref(null)

const getDetails = async (id) => Details.getDetail(id)
const showMessage = async (id, left, top) => {
  window.history.pushState({}, "", `/explore/${id}`);
  overlayX.value = left;
  overlayY.value = top;
  await getDetails(id);
  show.value = true;
  // 确保在显示后添加返回按钮
  await nextTick();
  addBackPage();
};

const afterDoComment = (comment) => Details.afterDoComment(comment);

onClickOutside(overlay, () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = '欢迎来到Dlock!'
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
          10% {
            transform: scale(0.5);
          }
          100% {
            transform: scale(1);
          }
       }`
  document.head.appendChild(style);
}

const addBackPage = () => {
  nextTick(() => {
    const backButton = document.querySelector('.backPage');
    if (backButton) {
      backButton.style.display = 'block'; // 改为 block 确保显示
    }
  });
};

const handleOverlayClose = () => {
  close();
  const backButton = document.querySelector('.backPage');
  if (backButton) {
    backButton.style.display = 'none';
  }
  // 恢复导航栏显示
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    el.style.display = '';
  });
};

// 修改 close 函数
const close = () => {
  window.history.pushState({}, "", "/");
  show.value = false;
  document.title = '欢迎来到Dlock!'
  // 恢复导航栏显示
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    el.style.display = '';
  });
};

// 更新 onAfterEnter
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


onMounted(async () => {
  await doQuery(0);
  if (window.location.pathname.includes('/explore/')) {
    const id = window.location.pathname.split('/').pop();
    await getDetails(id);
    show.value = true;
    await nextTick();
    addBackPage();
  }
});


</script>

<template>
  <div class="Empty" v-if="cards.length === 0">
    <el-empty description="没有帖子..."/>
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
    <div class="overlay" v-if="show">
      <button class="backPage" @click="close" style="display: none;">
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
  color: #666; /* 灰色图标 */
}

/* 添加hover效果 */
.backPage:hover {
  background: rgba(0, 0, 0, 0.1);
}



/* 添加card-detail的样式 */
.card-detail {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  margin-top: 48px; /* 为顶部返回按钮留出空间 */
}



/* 加载更多按钮样式 */
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
  animation: scale-up-center 0.5s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}

.fade-leave-active {
  animation: scale-up-center 0.3s ease-out both reverse;
}
</style>