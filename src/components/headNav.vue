<script setup>
import { ref } from "vue";
import { Search } from '@element-plus/icons-vue'
import { useRouter } from "vue-router";

const router = useRouter()
const searchInput = ref('')

const searchThings = () => {
  const searchTerm = searchInput.value.trim()
  if (searchTerm) {
    // Navigate to the explore page with query parameters
    router.push({
      path: '/',
      query: { query: searchTerm }
    })
  }
}

</script>

<template>
  <el-row :gutter="24">
    <el-col :span="4" style="margin-top: 1.5vh;">
    </el-col>
    <el-col :span="16" style="margin-top: 1.5vh;">
      <el-input 
        class="my" 
        v-model="searchInput" 
        placeholder="Search for something...." 
        @keyup.enter="searchThings"
        :prefix-icon="Search"
        clearable
      />
    </el-col>
  </el-row>
</template>

<style scoped>
</style>