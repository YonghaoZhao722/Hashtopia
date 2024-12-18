<script setup>
import {ref} from "vue";
import {Search} from '@element-plus/icons-vue'
import {useRouter} from "vue-router";

const router = useRouter()
// searchValue
const searchInput = ref('')
// search
const searchThings = () => {
  router.replace(`/?query=${searchInput.value}`)
}

</script>

<template>
  <el-row :gutter="24">
    <el-col :span="4" style="margin-top: 15px;">
    </el-col>
    <el-col :span="16" style="margin-top: 15px;">
      <el-input class="my" v-model="searchInput" placeholder="搜索点什么...." @keyup.enter="searchThings"
                :prefix-icon="Search"
                clearable/>
    </el-col>
  </el-row>
</template>

<style scoped>

</style>