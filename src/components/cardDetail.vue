<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import DesktopView from '@/views/DesktopView/DesktopPostDetail.vue';  // 原来的桌面端组件
import MobileView from '@/views/MobileView/MobilePostDetail.vue';     // 之前创建的移动端组件

const props = defineProps({
  detail: {
    type: Object,
    required: true,
  },
  review: {
    type: Boolean,
    default: false
  }
});

const isMobile = ref(false);

const checkDevice = () => {
  // 使用768px作为移动设备的断点
  isMobile.value = window.innerWidth <= 768;
};

// 监听窗口大小变化
onMounted(() => {
  checkDevice();
  window.addEventListener('resize', checkDevice);
});

onUnmounted(() => {
  window.removeEventListener('resize', checkDevice);
});
</script>

<template>
  <component 
    :is="isMobile ? MobileView : DesktopView"
    :detail="detail"
    :review="review"
  />
</template>
