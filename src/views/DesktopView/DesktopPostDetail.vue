<script setup>
import {ChatRound, Edit} from "@element-plus/icons-vue";
import {onMounted, ref} from "vue";
import {doComment, doFocus, unFollow, controlUserCollectOrLike, getComment, loadReplies} from "@/apis/main";
import {ElMessage} from "element-plus";
import {useUserStore} from "@/stores/user";
import {getCurrentTime} from "@/utils/getTime";

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
const comments = ref([])
// 子传父
const emit = defineEmits(['afterDoComment'])
const userStore = useUserStore()

// 更改用户对帖子的状态 /////////////////////////////////////////////////
const doFocusOn = async (id) => {
  if (userStore.userInfo.id === id) {
    ElMessage({type: 'warning', message: 'Cannot follow yourself'})
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
//更改帖子的点赞收藏状态
const doSomething = async (type, detail) => {
  const post_id = detail.id
  if (type === 'like') {
    const operator = checkFavorite(post_id)
    const res = await controlUserCollectOrLike({post_id, operator, type})
    if (operator) {
      userStore.removeFocus(2, post_id)
      detail.likeCount--;
      ElMessage({type: 'success', message: res.info})
    } else {
      userStore.extendUserInfo(2, post_id)
      detail.likeCount++;
      ElMessage({type: 'success', message: res.info})
    }
  } else if (type === 'collect') {
    const operator = checkCollect(post_id)
    const res = await controlUserCollectOrLike({post_id, operator, type})
    if (operator) {
      detail.collectCount--;
      userStore.removeFocus(3, post_id)
      ElMessage({type: 'success', message: res.info})
    } else {
      detail.collectCount++;
      userStore.extendUserInfo(3, post_id)
      ElMessage({type: 'success', message: res.info})
    }
  }
}
//////////////////////////////////////////////////////////////////

// 评论内容////////////////////////////////////////////////////////
const content = ref('')
const to = ref(0)
const commentInput = ref(null)
const sendComment = async (post, to) => {
  const info = ref([{
    id: 0,
    user: userStore.userInfo,
    content: content.value,
    createTime: getCurrentTime(),
    replyCount: 0,
    replies: []
  }])
  if (to === 0 || to === '0') {
    const data = {
      post_id: post.id,
      content: content.value,
    }
    const res = await doComment({data})
    ElMessage({type: 'success', message: res.info})
    info.value[0].id = res.id
    console.log(res.id, info.value)
    comments.value = [...comments.value, ...info.value]
  } else {
    const data = {
      post_id: post.id,
      content: content.value,
      parent_comment_id: to
    }
    const res = await doComment({data})
    ElMessage({type: 'success', message: res.info})
    const comment = comments.value.find(item => item.id === to);
    comment.replies = [...comment.replies, ...info.value]
    clearReply()
  }
  emit('afterDoComment')
  content.value = ''
}
const commentMain = (item) => {
  to.value = item.id
  console.log(item)
  const toPeople = item.user.username
  commentInput.value.input.placeholder = `Reply ${toPeople}: `
}
const loadReply = async (item) => {
  const offset = item.replies.length
  const id = item.id
  const res = await loadReplies({id, offset})
  item.replies = [...item.replies, ...res.info]
  item.replyCount -= res.count
}
const clearReply = () => {
  commentInput.value.input.placeholder = `Say something....`
  to.value = 0
}
const disabled = ref(true)
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

onMounted(async () => {
  await load();
});
</script>

<template>
  <div class="box" v-if="detail.id">
    <div style="border-radius: 0.8rem;background-color:#fff;">
      <el-row :gutter="50">
        <!-- Image Area -->
        <el-col :span="50">
          <div class="banner">
            <el-carousel height="45vw">
              <el-carousel-item v-for="item in detail.imgs" :key="item" class="carousel-item">
                <img class="image"
                     :src="item"
                     alt=""/>
              </el-carousel-item>
            </el-carousel>
          </div>
        </el-col>
        <!-- Image Area End -->
        <!-- Card details area-->
        <el-col :span="50">
          <div class="info" style="width: 35vw;margin-top: 0.5vw;">
            <el-row style="align-items: center;width: 35vw;">
              <a :href="`/user/index/${detail.user.id}`">
                <el-avatar :src="detail.user.avatar" size="large"/>
              </a>
              <div class="username">{{ detail.user.username }}</div>
              <button @click="cancelFocusOn(detail.user.id)" class="focusOn" v-if="checkFollow(detail.user.id)">Followed
              </button>
              <button class="focusOn" v-else @click="doFocusOn(detail.user.id)">Follow</button>
            </el-row>
            <div class="main-content">
              <el-row style="margin-top: 0;">
                <h2>{{ detail.title }}</h2>
              </el-row>
              <el-row>
                <div class="content">{{ detail.content }}</div>
              </el-row>
              <el-row>
                <time class="time">{{ detail.createTime }}</time>
              </el-row>
              <!-- End of card content -->
              <hr/>
              <!-- Comments -->
              <div class="comments" v-if="comments" v-infinite-scroll="load" :infinite-scroll-disabled="disabled">
                <el-empty description="There are no comments yet" v-if="comments.length === 0"/>
                <div v-else class="commentBox">
                  <div class="commentTitle" style="margin-bottom: 0.5vw;">Total {{ detail.commentCount }} comments</div>
                  <div v-for="item in comments" :key="item.id">
                    <el-row :gutter="20">
                      <el-col :span="2.5">
                        <a :href="`/user/index/${item.user.id}`">
                          <el-avatar :src="item.user.avatar" :size="30"></el-avatar>
                        </a>
                      </el-col>
                      <el-col :span="20" style="font-size: 1.1vw">
                        <div style="color:#33333399;">{{ item.user.username }}</div>
                        <div style="color:#333333;margin-top: 0.1vw;margin-bottom: 0.3vw;">{{ item.content }}</div>
                        <time class="time">{{ item.createTime }}</time>
                        <el-icon style="float: right;font-size: medium" @click="commentMain(item)">
                          <ChatRound/>
                        </el-icon>
                      </el-col>
                      <el-col style="margin-top: 0.3vw;">
                        <div v-for="reply in item.replies" :key="reply.id" style="margin-left: 2vw">
                          <el-row :gutter="20">
                            <el-col :span="2.5">
                              <a :href="`/user/index/${reply.user.id}`">
                                <el-avatar :src="reply.user.avatar" :size="25"></el-avatar>
                              </a>
                            </el-col>
                            <el-col :span="20" style="font-size: 1vw;margin-bottom: 2vw;">
                              <div style="color:#33333399;">{{ reply.user.username }}</div>
                              <div style="color:#333333;margin-top: 0.5vw;margin-bottom: 0.5vw;">{{ reply.content }}</div>
                              <time class="time">{{ reply.createTime }}</time>
                            </el-col>
                          </el-row>
                        </div>
                        <div class="more" @click="loadReply(item)" v-if="item.replyCount > 0">Expand {{
                            item.replyCount
                          }} replies
                        </div>
                      </el-col>
                    </el-row>
                    <el-divider/>
                  </div>
                </div>
              </div>
            </div>
            <!-- End of comments section -->
          </div>
          <div class="bottomArea">
            <div class="buttonArea">
              <el-row>
                <el-button link class="warp" @click="doSomething('like', detail)" :disabled="review">
                  <svg x="1689147877558" class="icon" viewBox="0 0 1024 1024" version="1.1"
                       xmlns="http://www.w3.org/2000/svg" p-id="3345" width="2vw" height="2vw">
                    <path
                        d="M512 901.746939c-13.583673 0-26.122449-4.179592-37.093878-13.061225-8.881633-7.314286-225.697959-175.020408-312.424489-311.379592C133.746939 532.37551 94.040816 471.24898 94.040816 384.522449c0-144.718367 108.146939-262.269388 240.326531-262.269388 67.395918 0 131.657143 30.82449 177.632653 84.636735 45.453061-54.334694 109.191837-84.636735 177.110204-84.636735 132.702041 0 240.326531 117.55102 240.326531 262.269388 0 85.159184-37.093878 143.673469-67.395919 191.216327l-1.044898 1.567346c-86.726531 136.359184-303.542857 304.587755-312.424489 311.379592-10.44898 8.359184-22.987755 13.061224-36.571429 13.061225z"
                        :fill="!checkFavorite(detail.id)?'#cecccc':'#d81e06'" p-id="3346"></path>
                  </svg>
                  <el-text size="large" tag="b" type="info">{{ detail.likeCount }}</el-text>
                </el-button>
                <el-button link class="warp" @click="doSomething('collect', detail)" :disabled="review">
                  <svg x="1689148085763" class="icon" viewBox="0 0 1024 1024" version="1.1"
                       xmlns="http://www.w3.org/2000/svg" p-id="4912" width="2vw" height="2vw">
                    <path
                        d="M512.009505 25.054894l158.199417 320.580987 353.791078 51.421464L767.995248 646.579761l60.432101 352.365345-316.417844-166.354615-316.436854 166.354615 60.432101-352.365345L0 397.057345l353.791078-51.421464z"
                        :fill="!checkCollect(detail.id)?'#cecccc':'#f4ea2a'" p-id="4913"></path>
                  </svg>
                  <el-text size="large" tag="b" type="info">{{ detail.collectCount }}</el-text>
                </el-button>
                <el-button link class="warp" @click="clearReply">
                  <svg x="1689148939874" class="icon" viewBox="0 0 1024 1024" version="1.1"
                       xmlns="http://www.w3.org/2000/svg" p-id="6375" width="2vw" height="2vw">
                    <path
                        d="M512 0C226.742857 0 0 197.485714 0 446.171429c0 138.971429 73.142857 270.628571 190.171429 351.085714L190.171429 1024l226.742857-138.971429c29.257143 7.314286 65.828571 7.314286 95.085714 7.314286 285.257143 0 512-197.485714 512-446.171429C1024 197.485714 797.257143 0 512 0zM256 512C219.428571 512 190.171429 482.742857 190.171429 446.171429S219.428571 380.342857 256 380.342857c36.571429 0 65.828571 29.257143 65.828571 65.828571S292.571429 512 256 512zM512 512C475.428571 512 446.171429 482.742857 446.171429 446.171429S475.428571 380.342857 512 380.342857c36.571429 0 65.828571 29.257143 65.828571 65.828571S548.571429 512 512 512zM768 512C731.428571 512 702.171429 482.742857 702.171429 446.171429s29.257143-65.828571 65.828571-65.828571c36.571429 0 65.828571 29.257143 65.828571 65.828571S804.571429 512 768 512z"
                        p-id="6376" fill="#cecccc"></path>
                  </svg>
                  <el-text size="small" tag="b" type="info">{{ detail.commentCount }}</el-text>
                </el-button>
              </el-row>
            </div>
            <el-input
                v-model="content" class="comment-input my" type="text" placeholder="Say something..." ref="commentInput"
                :prefix-icon="Edit" @keyup.enter="sendComment(detail, to)" clearable style="margin-top: 0.3vw"
                :disabled="review"
            />
          </div>
        </el-col>
        <!-- End of card details area -->
      </el-row>
    </div>
  </div>
</template>

<style scoped>
.content {
  margin: 0;
  font-weight: 400;
  font-size: 1.1vw;
  line-height: 2vw;
  color: #333;
  white-space: pre-wrap;
  overflow-wrap: break-word;
  margin: 3%;
}

.more {
  margin-left: 2vw;
  margin-top: 1vw;
  line-height: 1vw;
  color: #13386c;
  cursor: pointer;
}

.commentTitle {
  font-size: 1vw;
  line-height: 1.1vw;
  color: #666;
}

.box {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  border-radius: 0.8rem;
  width: 90vw;
  height: 45vw;
  box-shadow: -26px 28px 28px -20px rgba(0, 0, 0, 0.3), 30px 10px 61px -20px rgba(0, 0, 0, 0.3);
}

.banner {
  width: 45vw;
  border-radius: 0.8rem;
  overflow: hidden;
}

.username {
  margin-left: 1vw;
}

.focusOn {
  position: absolute;
  right: 1vw;
  padding: 0.6rem 0.8rem;
  color: white;
  background-color: red;
  border: 0;
  border-radius: 0.8rem;
}

.focusOn:hover {
  background-color: #fd5656;
}

.image {
  width: 100%;       
  height: 45vw;      
  border-radius: 0.8rem 0 0 0.8rem;
  object-fit: contain; 
  background-color: white;
}

.main-content::-webkit-scrollbar {
  width: 0.1em;
  background-color: transparent;
}

.main-content {
  margin-bottom: 0%;
  position: relative;
  width: 40vw;
  height: 34vw;
  overflow-y: scroll;
}

.time {
  font-size: 1vw;
  color: #999;
}

.bottomArea {
  width: 10vw;
  position: relative;
}

.buttonArea {
  margin-left: -1.5vw;

  width: 40vw;
  height: 4vw;
  bottom: 1vw;
}

.warp {
  display: flex;
  align-items: center;
  margin-right: 2vw;
}

.comment-input {
  margin-left: -2vw;
  position: relative;
  bottom: 1vw;
  font-size: 1vw;
  width: 40vw;
}
</style>