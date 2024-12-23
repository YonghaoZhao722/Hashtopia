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

// Add resize handler
const handleResize = () => {
  isMobile.value = window.innerWidth <= 768;
};

const isMounted = ref(false);

const hideNavigation = async () => {
  await nextTick();
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    if (el) el.style.display = 'none';
  });
};

const showNavigation = () => {
  const navigationElements = document.querySelectorAll('.menu,.el-header');
  navigationElements.forEach(el => {
    if (el) el.style.display = 'block';
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

onMounted(() => {
  // Add resize event listener
  window.addEventListener('resize', handleResize);
  
  if (window.performance && window.performance.navigation.type === 1) {
    const savedPath = sessionStorage.getItem('cardDetailSource');
    if (savedPath) {
      window.location.href = savedPath;
    }
  }
});

onUnmounted(() => {
  // Remove resize event listener
  window.removeEventListener('resize', handleResize);
  sessionStorage.removeItem('cardDetailSource');
  showNavigation();
});

const handleClose = () => {
  showNavigation();
  emit('closeOverlay');
};

const handleAfterComment = () => {
  emit('afterDoComment');
};

const route = useRoute();
watch(() => route.path, async () => {
  await nextTick();
  hideNavigation();
  emit('needBackPage');
});

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