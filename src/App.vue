<script setup>
import { onMounted } from 'vue'

onMounted(() => {
  document.body.style.setProperty('--el-color-primary', 'red');
})

</script>

<template>
  <RouterView/>
</template>

<style scoped>
:root{
  --el-text-color-secondary:black !important;
}
</style>
