# src/views/ProfileView.vue
<template>
  <div class="profile-container">
    <!-- Profile Header -->
    <div class="profile-header">
      <el-card>
        <div class="profile-info">
          <div class="profile-avatar">
            <el-image
              :src="userProfile?.avatar || defaultAvatar"
              fit="cover"
              class="avatar-image"
            >
              <template #error>
                <img :src="defaultAvatar" class="avatar-image" />
              </template>
            </el-image>
          </div>
          <div class="profile-details">
            <div class="profile-username">
              <h1>{{ userProfile?.username }}</h1>
              <el-button
                v-if="isCurrentUser"
                type="primary"
                @click="showEditProfile"
                class="edit-btn"
              >
                Edit Profile
              </el-button>
            </div>
            <div class="profile-stats">
              <div class="stat-item">
                <span class="stat-value">{{ postsCount }}</span>
                <span class="stat-label">Posts</span>
              </div>
              <div class="stat-divider"></div>
              <div class="stat-item">
                <span class="stat-value">{{ likesCount }}</span>
                <span class="stat-label">Likes</span>
              </div>
            </div>
            <div class="profile-bio">
              <p v-if="userProfile?.bio">{{ userProfile.bio }}</p>
              <p v-else-if="isCurrentUser" class="empty-bio">Add a bio to let others know you...</p>
            </div>
            <div class="profile-meta">
              <template v-if="userProfile?.gender || userProfile?.age || userProfile?.location">
                <el-tag v-if="userProfile.gender" size="small" class="meta-tag">
                  {{ userProfile.gender }}
                </el-tag>
                <el-tag v-if="userProfile.age" size="small" class="meta-tag">
                  {{ userProfile.age }} years
                </el-tag>
                <el-tag v-if="userProfile.location" size="small" class="meta-tag">
                  {{ userProfile.location }}
                </el-tag>
              </template>
              <p v-else-if="isCurrentUser" class="empty-meta">
                Add personal information...
              </p>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <!-- Content Tabs -->
    <div class="profile-content">
      <el-card>
        <el-tabs v-model="activeTab" class="demo-tabs">
          <el-tab-pane label="Posts" name="posts">
            <div class="posts-grid" v-if="userPosts.length">
              <el-card
                v-for="post in userPosts"
                :key="post.id"
                class="post-card"
                @click="viewPost(post.id)"
                shadow="hover"
              >
                <div class="post-image">
                  <el-image
                    :src="post.cover_image || defaultPostCover"
                    fit="cover"
                  />
                </div>
                <div class="post-info">
                  <h3>{{ post.title }}</h3>
                  <div class="post-meta">
                    <span>
                      <el-icon><View /></el-icon>
                      {{ post.views }}
                    </span>
                    <span>
                      <el-icon><Star /></el-icon>
                      {{ post.likes }}
                    </span>
                  </div>
                </div>
              </el-card>
            </div>
            <div v-else class="empty-state">
              <el-empty description="No posts yet" />
            </div>
          </el-tab-pane>

          <el-tab-pane label="Likes" name="likes">
            <div class="posts-grid" v-if="likedPosts.length">
              <!-- Similar post cards structure -->
            </div>
            <div v-else class="empty-state">
              <el-empty description="No liked posts yet" />
            </div>
          </el-tab-pane>
        </el-tabs>
      </el-card>
    </div>

    <!-- Edit Profile Dialog -->
    <el-dialog
      v-model="editProfileVisible"
      title="Edit Profile"
      width="500px"
      class="edit-profile-dialog"
    >
      <el-form
        ref="editFormRef"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="Avatar">
          <el-upload
            class="avatar-uploader"
            action="/api/upload/avatar"
            :show-file-list="false"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
          >
            <img v-if="editForm.avatar" :src="editForm.avatar" class="upload-avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
        </el-form-item>

        <el-form-item label="Bio">
          <el-input
            v-model="editForm.bio"
            type="textarea"
            :rows="3"
            placeholder="Introduce yourself..."
          />
        </el-form-item>

        <el-form-item label="Gender">
          <el-select v-model="editForm.gender" placeholder="Select gender">
            <el-option label="Male" value="Male" />
            <el-option label="Female" value="Female" />
            <el-option label="Other" value="Other" />
          </el-select>
        </el-form-item>

        <el-form-item label="Age">
          <el-input-number
            v-model="editForm.age"
            :min="1"
            :max="120"
            controls-position="right"
          />
        </el-form-item>

        <el-form-item label="Location">
          <el-input v-model="editForm.location" placeholder="Enter location" />
        </el-form-item>
      </el-form>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editProfileVisible = false">Cancel</el-button>
          <el-button type="primary" @click="updateProfile" :loading="updating">
            Save
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>


<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
import { View, Star, Plus } from '@element-plus/icons-vue';
import defaultAvatar from '@/assets/default-avatar.png';
import defaultPostCover from '@/assets/default-post-cover.png';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();

// State
const userProfile = ref(null);
const userPosts = ref([]);
const likedPosts = ref([]);
const activeTab = ref('posts');
const editProfileVisible = ref(false);
const updating = ref(false);
const editFormRef = ref(null);

const editForm = ref({
  avatar: '',
  bio: '',
  gender: '',
  age: null,
  location: ''
});

const props = defineProps({
  id: {
    type: [String, Number],
    default: null
  }
});

const targetUserId = computed(() =>
  props.id || userStore.user?.id
);

// Computed
const isCurrentUser = computed(() =>
  userStore.user?.id === Number(targetUserId.value)
);

const postsCount = computed(() => userPosts.value.length);
const likesCount = computed(() =>
  userPosts.value.reduce((total, post) => total + post.likes, 0)
);

// Methods
const fetchUserProfile = async () => {
  try {
    const response = await axios.get(`/api/users/profile/${targetUserId.value}`);
    userProfile.value = response.data;

    if (isCurrentUser.value) {
      editForm.value = {
        avatar: userProfile.value.avatar || '',
        bio: userProfile.value.bio || '',
        gender: userProfile.value.gender || '',
        age: userProfile.value.age || null,
        location: userProfile.value.location || ''
      };
    }
  } catch (error) {
    ElMessage.error('Failed to fetch user profile.');
  }
};

const fetchUserPosts = async () => {
  try {
    const response = await axios.get(`/api/users/${targetUserId.value}/posts`);
    userPosts.value = response.data.posts;
  } catch (error) {
    ElMessage.error('Failed to fetch posts.');
  }
};

const fetchLikedPosts = async () => {
  try {
    const response = await axios.get(`/api/users/${targetUserId.value}/liked-posts`);
    likedPosts.value = response.data.posts;
  } catch (error) {
    ElMessage.error('Failed to fetch liked posts.');
  }
};

const showEditProfile = () => {
  editProfileVisible.value = true;
};

const updateProfile = async () => {
  if (!editFormRef.value) return;

  try {
    updating.value = true;
    const response = await axios.put('/api/users/profile', editForm.value);
    userProfile.value = response.data.user;
    editProfileVisible.value = false;
    ElMessage.success('Profile updated successfully.');
  } catch (error) {
    ElMessage.error('Failed to update profile. Please try again.');
  } finally {
    updating.value = false;
  }
};

const viewPost = (postId) => {
  router.push(`/posts/${postId}`);
};

// Lifecycle
onMounted(() => {
  fetchUserProfile();
  fetchUserPosts();
  fetchLikedPosts();
});
</script>


<style scoped lang="scss">
.profile-container {
  max-width: 1200px;
  margin: 20px auto;
  padding: 0 20px;
}

.profile-header {
  margin-bottom: 20px;
}

.profile-info {
  display: flex;
  gap: 30px;
  padding: 20px;
}

.profile-avatar {
  flex-shrink: 0;

  .avatar-image {
    width: 150px;
    height: 150px;
    border-radius: 50%;
    object-fit: cover;
  }
}

.profile-details {
  flex: 1;
}

.profile-username {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;

  h1 {
    margin: 0;
    font-size: 24px;
    font-weight: 600;
  }

  .edit-btn {
    height: 32px;
  }
}

.profile-stats {
  display: flex;
  align-items: center;
  margin-bottom: 20px;

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0 20px;

    .stat-value {
      font-size: 18px;
      font-weight: 600;
    }

    .stat-label {
      font-size: 14px;
      color: var(--text-secondary);
    }
  }

  .stat-divider {
    width: 1px;
    height: 20px;
    background-color: var(--border-color);
  }
}

.profile-bio {
  margin-bottom: 20px;
  color: var(--text-secondary);

  .empty-bio {
    color: #999;
    font-style: italic;
  }
}

.profile-meta {
  .meta-tag {
    margin-right: 10px;
    background-color: #f5f5f5;
    .empty-meta {
      color: #999;
      font-style: italic;
    }
  }
}

.profile-content {
  .posts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px 0;
  }

  .post-card {
    cursor: pointer;
    transition: transform 0.2s;

    &:hover {
      transform: translateY(-5px);
    }
  }

  .post-image {
    height: 200px;
    overflow: hidden;

    .el-image {
      width: 100%;
      height: 100%;
    }
  }

  .post-info {
    padding: 12px;

    h3 {
      margin: 0 0 10px 0;
      font-size: 16px;
      line-height: 1.4;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

    .post-meta {
      display: flex;
      gap: 15px;
      color: var(--text-secondary);
      font-size: 14px;

      span {
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
  }
}

.empty-state {
  padding: 40px 0;
  text-align: center;
}

// Edit Profile Dialog Styles
.edit-profile-dialog {
  :deep(.el-dialog__body) {
    padding-top: 20px;
  }

  .avatar-uploader {
    text-align: center;

    .upload-avatar {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      object-fit: cover;
    }

    .avatar-uploader-icon {
      font-size: 28px;
      color: #8c939d;
      width: 100px;
      height: 100px;
      text-align: center;
      border: 1px dashed var(--border-color);
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;

      &:hover {
        border-color: var(--primary-color);
        color: var(--primary-color);
      }
    }
  }

  .dialog-footer {
    width: 100%;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding-top: 20px;
  }
}

// Responsive Design
@media (max-width: 768px) {
  .profile-info {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .profile-username {
    justify-content: center;
  }

  .profile-stats {
    justify-content: center;
  }

  .profile-meta {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 8px;
  }

  .posts-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}

.el-tabs__nav-wrap::after {
  height: 1px;
  background-color: var(--border-color);
}

.el-tabs__active-bar {
  background-color: var(--primary-color);
}

.el-tabs__item.is-active {
  color: var(--primary-color);
}
</style>
