<script setup>
import { ref, onMounted, onUnmounted, defineAsyncComponent, watch, nextTick } from 'vue';
import { useRoute } from 'vue-router';

const DesktopView = defineAsyncComponent(() => import('@/views/DesktopView/DesktopPostDetail.vue'))
const MobileView = defineAsyncComponent(() => import('@/views/MobileView/MobilePostDetail.vue'))

const emit = defineEmits(['needBackPage', 'closeOverlay', 'mounted', 'afterDoComment'])

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

const isMobile = ref(window.innerWidth <= 768);

const checkDevice = () => {
  isMobile.value = window.innerWidth <= 768;
};

// Add a ref to track the component's mounted state
const isMounted = ref(false);

const hideNavigation = async () => {
  await nextTick(); // Ensure DOM is updated
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    if (el) el.style.display = 'none';
  });
};

const showNavigation = () => {
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    if (el) el.style.display = 'block'; // Be explicit with display value
  });
};

const handleComponentMounted = async () => {
  if (!isMounted.value) {
    isMounted.value = true;
    await hideNavigation();
    emit('needBackPage');
    emit('mounted');
  }
};

onMounted(async () => {
  checkDevice();
  window.addEventListener('resize', checkDevice);
  await handleComponentMounted();
});



onUnmounted(() => {
  window.removeEventListener('resize', checkDevice);
  showNavigation();
});

// 监听 overlay 关闭
const handleClose = () => {
  showNavigation();
  emit('closeOverlay');
};

const route = useRoute();
watch(() => route.path, async () => {
  await nextTick();
  hideNavigation();
  emit('needBackPage');
});

// 添加 Suspense fallback 处理
const handleFallback = () => {
  hideNavigation();
  emit('needBackPage');
};
</script>

<template>
  <Suspense @fallback="handleFallback">
    <template #default>
      <component 
        :is="isMobile ? MobileView : DesktopView"
        :detail="detail"
        :review="review"
        @mounted="handleComponentMounted"
        @close="handleClose"
        @after-do-comment="handleAfterComment"
      />
    </template>
    <template #fallback>
      <div>Loading...</div>
    </template>
  </Suspense>
</template>