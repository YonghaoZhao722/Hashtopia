<script setup>
import { ChatRound, Edit } from "@element-plus/icons-vue";
import { onMounted, ref } from "vue";
import { doComment, doFocus, unFollow, controlUserCollectOrLike, getComment, loadReplies } from "@/apis/main";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/user";
import { getCurrentTime } from "@/utils/getTime";
import router from "@/router";

const props = defineProps({
  detail: {
    type: Object,
    required: true,
  },
  review: {
    type: Boolean,
    default: false
  }
})

// Same state management and methods as desktop version
const comments = ref([])
const emit = defineEmits(['afterDoComment'])
const userStore = useUserStore()
const content = ref('')
const to = ref(0)
const commentInput = ref(null)
const disabled = ref(true)

// Reuse existing methods
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({type: 'warning', message: '不能对自己进行关注操作'})
    return
  }
  const res = await doFocus({id})
  userStore.extendUserInfo(1, id)
  ElMessage({type: 'success', message: res.info})
}

const cancelFocusOn = async (id) => {
  const res = await unFollow({id})
  userStore.removeFocus(1, id)
  ElMessage({type: 'success', message: res.info})
}

const checkFollow = (id) => {
  return userStore.userFocus.includes(id)
}

const checkCollect = (id) => {
  return userStore.userCollect.includes(id)
}

const checkFavorite = (id) => {
  return userStore.userFavorite.includes(id)
}

const doSomething = async (type, detail) => {
  const post_id = detail.id
  if (type === 'like') {
    const operator = checkFavorite(post_id)
    const res = await controlUserCollectOrLike({post_id, operator, type})
    if (operator) {
      userStore.removeFocus(2, post_id)
      detail.likeCount--;
    } else {
      userStore.extendUserInfo(2, post_id)
      detail.likeCount++;
    }
    ElMessage({type: 'success', message: res.info})
  } else if (type === 'collect') {
    const operator = checkCollect(post_id)
    const res = await controlUserCollectOrLike({post_id, operator, type})
    if (operator) {
      detail.collectCount--;
      userStore.removeFocus(3, post_id)
    } else {
      detail.collectCount++;
      userStore.extendUserInfo(3, post_id)
    }
    ElMessage({type: 'success', message: res.info})
  }
}

// Load comments
const load = async () => {
  disabled.value = true
  const offset = comments.value.length
  const id = props.detail.id
  const res1 = await getComment({id, offset})
  const data = res1.info
  if (data.length !== 0) {
    disabled.value = false
    comments.value = [...comments.value, ...data]
  } else {
    disabled.value = true
  }
}
const handleBack = () => {
  router.back();
};
onMounted(() => load())
</script>

<template>
  <div class="mobile-container">
    <!-- Header -->
    <div class="mobile-header">
      <div class="left-section">
      </div>
      <div class="center-section">
        <div class="user-info">
          <el-avatar :src="detail.user.avatar" :size="36" />
          <span class="username">{{ detail.user.username }}</span>
        </div>
      </div>
      <div class="right-section">
        <el-icon :size="24"><More /></el-icon>
      </div>
    </div>

    <!-- Main Content -->
    <div class="mobile-content">
      <!-- Image Carousel -->
      <el-carousel height="300px" indicator-position="inside">
        <el-carousel-item v-for="item in detail.imgs" :key="item">
          <img :src="item" class="carousel-image" />
        </el-carousel-item>
      </el-carousel>

      <!-- Post Details -->
      <div class="post-info">
        <h2>{{ detail.title }}</h2>
        <p class="post-text">{{ detail.content }}</p>
        <div class="post-meta">
          <span class="time">{{ detail.createTime }}</span>
        </div>
      </div>

      <!-- Interaction Buttons -->
      <div class="interaction-buttons">
        <div class="button-group">
          <el-button link @click="doSomething('like', detail)">
            <svg x="1689147877558" class="icon" viewBox="0 0 1024 1024" version="1.1"
                 xmlns="http://www.w3.org/2000/svg" width="20" height="20">
              <path d="M512 901.746939c-13.583673 0-26.122449-4.179592-37.093878-13.061225-8.881633-7.314286-225.697959-175.020408-312.424489-311.379592C133.746939 532.37551 94.040816 471.24898 94.040816 384.522449c0-144.718367 108.146939-262.269388 240.326531-262.269388 67.395918 0 131.657143 30.82449 177.632653 84.636735 45.453061-54.334694 109.191837-84.636735 177.110204-84.636735 132.702041 0 240.326531 117.55102 240.326531 262.269388 0 85.159184-37.093878 143.673469-67.395919 191.216327l-1.044898 1.567346c-86.726531 136.359184-303.542857 304.587755-312.424489 311.379592-10.44898 8.359184-22.987755 13.061224-36.571429 13.061225z"
                    :fill="!checkFavorite(detail.id)?'#999':'#d81e06'" />
            </svg>
            <span>{{ detail.likeCount }}</span>
          </el-button>
          <el-button link @click="doSomething('collect', detail)">
            <svg x="1689148085763" class="icon" viewBox="0 0 1024 1024" version="1.1"
                 xmlns="http://www.w3.org/2000/svg" width="20" height="20">
              <path d="M512.009505 25.054894l158.199417 320.580987 353.791078 51.421464L767.995248 646.579761l60.432101 352.365345-316.417844-166.354615-316.436854 166.354615 60.432101-352.365345L0 397.057345l353.791078-51.421464z"
                    :fill="!checkCollect(detail.id)?'#999':'#f4ea2a'" />
            </svg>
            <span>{{ detail.collectCount }}</span>
          </el-button>
          <el-button link>
            <el-icon><chat-round /></el-icon>
            <span>{{ detail.commentCount }}</span>
          </el-button>
        </div>
      </div>

      <!-- Comments Section -->
      <div class="comments-section" v-infinite-scroll="load" :infinite-scroll-disabled="disabled">
        <div class="comment-count">评论 {{ detail.commentCount }}</div>
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <el-avatar :src="comment.user.avatar" :size="30" />
          <div class="comment-content">
            <div class="comment-user">{{ comment.user.username }}</div>
            <div class="comment-text">{{ comment.content }}</div>
            <div class="comment-meta">
              <span class="time">{{ comment.createTime }}</span>
              <el-button link size="small" @click="$refs.commentInput.focus()">回复</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comment Input -->
    <div class="comment-input-container">
      <el-input
        v-model="content"
        placeholder="说点什么..."
        ref="commentInput"
        :prefix-icon="Edit"
        @keyup.enter="sendComment(detail, to)"
        clearable
      />
    </div>
  </div>
</template>

<style scoped>
.mobile-container {
  height: 100vh;
  background: #fff;
  display: flex;
  flex-direction: column;
}

.mobile-header {
  padding: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #eee;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  font-size: 16px;
  font-weight: 500;
}

.mobile-content {
  flex: 1;
  overflow-y: auto;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.post-info {
  padding: 16px;
}

.post-text {
  margin: 12px 0;
  font-size: 14px;
  line-height: 1.6;
  color: #333;
}

.interaction-buttons {
  padding: 12px 16px;
  border-top: 1px solid #eee;
  border-bottom: 1px solid #eee;
}

.button-group {
  display: flex;
  justify-content: space-around;
}

.comments-section {
  padding: 16px;
}

.comment-count {
  font-weight: 500;
  margin-bottom: 16px;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.comment-content {
  flex: 1;
}

.comment-user {
  font-weight: 500;
  font-size: 14px;
}

.comment-text {
  margin: 4px 0;
  font-size: 14px;
}

.comment-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.comment-input-container {
  padding: 12px;
  border-top: 1px solid #eee;
  background: #fff;
}

.time {
  font-size: 12px;
  color: #999;
}
</style>