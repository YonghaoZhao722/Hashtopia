<script setup xmlns="http://www.w3.org/1999/html">
import {computed, onBeforeMount, onMounted, ref, onBeforeUnmount} from 'vue'
import {queryUserPostControl, postDelete, controlUserCollectOrLike, unFollow, removeFan} from "@/apis/main";
import {ElMessage} from 'element-plus'
import {useUserStore} from "@/stores/user";
import enUS from 'element-plus/dist/locale/en.mjs'
import {useTableStore} from "@/stores/tableStore";
import {InfoFilled} from "@element-plus/icons-vue";
import {useRouter} from "vue-router";

const router = useRouter()
const userStore = useUserStore();
const checkLogin = () => {
  if (!userStore.userInfo.id) {
    router.replace('/login')
  }
}

onBeforeMount(() => checkLogin())
// Configuring global language and table caches//////////////////////////////////////////////
const locale = enUS
const tableStore = useTableStore();
const loading = ref(true)
const isMobile = ref(false)
// Control selector /////////////////////////////////////////////////////
const value = ref('posts')

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 900
}

const options = [
  {
    label: 'Post Management',
    options: [
      {
        value: 'posts',
        label: 'Posts',
      },
      {
        value: 'collected',
        label: 'Collects',
      },
      {
        value: 'favorites',
        label: 'Likes'
      }
    ],
  },
  {
    label: 'User management',
    options: [
      {
        value: 'fans',
        label: 'Following',
      },
      {
        value: 'follow',
        label: 'Followers',
      },
    ],
  },
]
const type = computed(() => {
  if (value.value === 'posts' || value.value === 'collected' || value.value === 'favorites')
    return 1
  else
    return 2
})
const changeShow = async () => {
  multipleSelection.value = [];
  const valueType = value.value;
  const offset = 0;
  const types = valueType;
  const data = tableStore.retrieveData(valueType, 1);
  if (type.value === 1) {
    if (data) {
      tableData.value = data.data;
      total_post.value = data.total;
    } else {
      loading.value = true
      const res = await queryUserPostControl({offset, types});
      tableData.value = res.info;
      total_post.value = res.total;
      tableStore.storeMessage(types, 1, res.info, res.total);
      loading.value = false
    }
  } else {
    if (data) {
      userData.value = data.data;
      total_user.value = data.total;
    } else {
      loading.value = true
      const res = await queryUserPostControl({offset, types});
      userData.value = res.info;
      total_user.value = res.total;
      tableStore.storeMessage(types, 1, res.info, res.total);
      loading.value = false
    }
  }
  currentPage.value = 1;
};
////////////////////////////////////////////////////////////////

const tableData = ref([])
const userData = ref([])
const multipleSelection = ref([])
const tableRef = ref(null)
const getData = async () => {
  const offset = 0
  const types = value.value
  const data = tableStore.retrieveData(types, 1);
  if (data) {
    tableData.value = data.data;
    total_post.value = data.total;
    loading.value = false
  } else {
    loading.value = true
    const res = await queryUserPostControl({offset, types})
    tableData.value = res.info
    total_post.value = res.total
    tableStore.storeMessage(types, 1, res.info, res.total)
    loading.value = false
  }
}
const handleSelectionChange = (val) => {
  multipleSelection.value = val
}
const handleDelete = async (index, row) => {
  const id = row.id
  if (type.value === 1) {
    tableData.value.splice(index, 1)
    if (value.value === 'posts') {
      const res = await postDelete({id})
      ElMessage({type: 'success', message: res.success})
    } else if (value.value === 'collected' || value.value === 'favorites') {
      const post_id = id
      const operator = 1
      const type = value.value === 'collected' ? 'collect' : 'like'
      const res = await controlUserCollectOrLike({post_id, operator, type})
      // Update the store after successful API call
      if (res.info) {
        const storeUpdateType = type === 'collect' ? 3 : 2
        userStore.removeFocus(storeUpdateType, post_id)
      }
      ElMessage({type: 'success', message: res.info})
    }
  } else {
    userData.value.splice(index, 1)
    if (value.value === 'fans') {
      const res = await removeFan({id})
      ElMessage({type: 'success', message: res.info})
    } else if (value.value === 'follow') {
      const res = await unFollow({id})
      userStore.removeFocus(1, id)
      ElMessage({type: 'success', message: res.info})
    }
  }
}
////////////////////////////////////////////////////////////////
const getTableColumns = computed(() => {
  if (isMobile.value) {
    return type.value === 1 ? [
      { label: 'Title', prop: 'title' },
      { label: 'Operation', slot: 'operation', align: 'center' }
    ] : [
      { label: 'Username', prop: 'username' },
      { label: 'Operation', slot: 'operation', align: 'center' }
    ]
  }
  
  return type.value === 1 ? [
    { label: 'Date', prop: 'date', sortable: true },
    { label: 'Username', prop: 'username' },
    { label: 'Title', prop: 'title' },
    { label: 'Content', prop: 'content', showOverflowTooltip: true },
    { label: 'Comment Count', prop: 'commentCount', sortable: true },
    { label: 'Like Count', prop: 'likeCount', sortable: true },
    { label: 'Collect Count', prop: 'collectCount', sortable: true },
    { label: 'Operation', slot: 'operation', align: 'center' }
  ] : [
    { label: 'Avatar', slot: 'avatar', align: 'center' },
    { label: 'Username', prop: 'username', sortable: true, showOverflowTooltip: true },
    { label: 'Fans', prop: 'fans' },
    { label: 'Following', prop: 'follow' },
    { label: 'Notes', prop: 'note' },
    { label: 'Operation', slot: 'operation', align: 'center' }
  ]
})
// Paginator ///////////////////////////////////////////////////////
const pageSize = ref(10)
const currentPage = ref(1)
const total_post = ref(0)
const total_user = ref(0)
const handleCurrentChange = async (val) => {
  const offset = (val - 1) * pageSize.value;
  const types = value.value;
  const cachedData = tableStore.retrieveData(types, val);
  let data, total;
  if (type.value === 1) {
    if (cachedData) {
      const cachedData = tableStore.retrieveData(types, val);
      data = cachedData.data;
      total = cachedData.total;
    } else {
      loading.value = true
      const res = await queryUserPostControl({offset, types});
      data = res.info;
      total = res.total;
      tableStore.storeMessage(types, val, data, total);
      loading.value = false
    }
    tableData.value = data;
    total_post.value = total;
  } else {
    if (cachedData) {
      const cachedData = tableStore.retrieveData(types, val);
      data = cachedData.data;
      total = cachedData.total;
    } else {
      loading.value = true
      const res = await queryUserPostControl({offset, types});
      data = res.info;
      total = res.total;
      tableStore.storeMessage(types, val, data, total);
      loading.value = false
    }
    userData.value = data;
    total_user.value = total;
  }
};

const handleBulkDelete = async () => {
  try {
    for (const item of multipleSelection.value) {
      const index = tableData.value.findIndex(row => row.id === item.id)
      if (index !== -1) {
        if (type.value === 1) {
          if (value.value === 'posts') {
            await postDelete({id: item.id})
          } else if (value.value === 'collected' || value.value === 'favorites') {
            const post_id = item.id
            const operator = 1
            const deleteType = value.value === 'collected' ? 'collect' : 'like'
            const res = await controlUserCollectOrLike({post_id, operator, type: deleteType})
            // Update the store after successful API call
            if (res.info) {
              const storeUpdateType = deleteType === 'collect' ? 3 : 2
              userStore.removeFocus(storeUpdateType, post_id)
            }
          }
          tableData.value.splice(index, 1)
        } else {
          if (value.value === 'fans') {
            await removeFan({id: item.id})
          } else if (value.value === 'follow') {
            await unFollow({id: item.id})
            userStore.removeFocus(1, item.id)
          }
          userData.value.splice(index, 1)
        }
      }
    }
    ElMessage({type: 'success', message: 'Successfully deleted selected items'})
    tableRef.value.clearSelection()
  } catch (error) {
    ElMessage({type: 'error', message: 'Failed to delete selected items'})
  }
}


//////////////////////////////////////////////////////////////////
onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  getData()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', checkMobile)
})
</script>

<template>
  <el-config-provider :locale="locale">
    <div class="container">
      <div class="select-container">
        <el-select
            v-model="value"
            placeholder="Select"
            @change="changeShow"
            :style="{ width: isMobile ? '100%' : '200px' }"
            aria-label="Select option for post or user management"
          >
          <template #prefix>
            <el-tooltip
                placement="top"
                effect="light"
            >
              <template #content>
                <h2 style="color:red;">The table contents will be cached locally</h2>
                <p>If you
                  <span style="color:red;">modify data</span>
                  It is not updated
                  <span style="color:red;">Just refresh</span>
                </p>
              </template>
              <el-icon>
                <info-filled/>
              </el-icon>
            </el-tooltip>
          </template>
          <el-option-group
              v-for="group in options"
              :key="group.label"
              :label="group.label"
          >
            <el-option
                v-for="item in group.options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-option-group>
        </el-select>
      </div>

      <div class="table-container" v-if="type === 1">
        <el-table
            :data="tableData"
            :row-key="'id'"
            style="width: 100%"
            ref="tableRef"
            :default-sort="{ prop: 'date', order: 'descending' }"
            @selection-change="handleSelectionChange"
            v-loading="loading"
            border
            stripe
            :size="isMobile ? 'small' : 'default'"
        >
          <el-table-column 
              type="selection" 
              width="55"
              :selectable="(row) => true"
              :reserve-selection="true"
              :label="'Select row'"
              aria-label="Select row checkbox"
              title="Select"
          />Select
          <template v-for="col in getTableColumns" :key="col.prop || col.type">
            <el-table-column v-bind="col">
              <template #default="scope" v-if="col.slot === 'operation'">
                <el-button
                  :size="isMobile ? 'small' : 'default'"
                  type="danger"
                  @click="handleDelete(scope.$index, scope.row)"
                  aria-label="Delete post"
                >
                  Delete
                </el-button>
              </template>
            </el-table-column>
          </template>
        </el-table>

        <div class="action-buttons" v-show="multipleSelection.length !== 0">
          <el-button 
              type="danger" 
              round 
              :size="isMobile ? 'small' : 'default'"
              @click="handleBulkDelete"
              aria-label="Delete selected items"
          >
            Delete Selected
          </el-button>
          <el-button 
              @click="tableRef.clearSelection()" 
              round 
              :size="isMobile ? 'small' : 'default'"
              aria-label="Clear selection"
          >
            Clear All
          </el-button>
        </div>

        <div class="pagination" role="navigation" aria-label="Pagination">
          <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :background="true"
              layout="prev, pager, next, jumper"
              :total="total_post"
              @current-change="handleCurrentChange"
              :small="isMobile"
              aria-label="Pagination control"
          />
        </div>
      </div>

      <div class="table-container" v-else>
            <el-table
                :data="userData"
                :row-key="'id'"
                style="width: 100%"
                ref="tableRef"
                @selection-change="handleSelectionChange"
                border
                v-loading="loading"
                stripe
                :size="isMobile ? 'small' : 'default'"
            >
              <el-table-column 
                  type="selection" 
                  width="55"
                  :selectable="(row) => true"
                  :reserve-selection="true"
                  label="Select All"
                  :aria-label="'Select all items'"
              />
          <template v-for="col in getTableColumns" :key="col.prop || col.type">
            <el-table-column v-bind="col">
              <template #default="scope" v-if="col.slot === 'avatar'">
                <el-avatar :size="isMobile ? 'small' : 'default'" :src="scope.row.avatar" :alt="`${scope.row.name}'s avatar`"/>
              </template>
              <template #default="scope" v-if="col.slot === 'operation'">
                <el-button
                    :size="isMobile ? 'small' : 'default'"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)"
                    aria-label="Remove user"
                >
                  Remove
                </el-button>
              </template>
            </el-table-column>
          </template>
        </el-table>

        <div class="action-buttons" v-show="multipleSelection.length !== 0">
          <el-button 
              type="danger" 
              round 
              :size="isMobile ? 'small' : 'default'"
              @click="handleBulkDelete"
              aria-label="Delete selected users"
          >
            Delete Selected
          </el-button>
          <el-button 
              @click="tableRef.clearSelection()" 
              round 
              :size="isMobile ? 'small' : 'default'"
              aria-label="Clear selection"
          >
            Clear All
          </el-button>
        </div>

        <div class="pagination" role="navigation" aria-label="Pagination">
          <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :background="true"
              layout="prev, pager, next, jumper"
              :total="total_user"
              @current-change="handleCurrentChange"
              :small="isMobile"
              aria-label="Pagination control"
          />
        </div>
      </div>
    </div>
  </el-config-provider>
</template>

<style scoped>
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.container {
  width: 100%;
  padding: 1rem;
  box-sizing: border-box;
  height: 92vh; /* Full viewport height */
  display: flex;
  flex-direction: column;
}

.select-container {
  margin-bottom: 1.25rem;
  flex-shrink: 0; /* Prevent shrinking */
}

.table-container {
  width: 100%;
  flex-grow: 1; /* Allow growing */
  display: flex;
  flex-direction: column;
  min-height: 0; /* Important for Firefox */
  position: relative;
}

/* Make the table scrollable */
.table-container :deep(.el-table) {
  height: 100%;
  max-height: calc(92vh - 200px); /* Adjust based on header/footer height */
  overflow-y: auto;
}

.action-buttons {
  margin-top: 1.25rem;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-shrink: 0; /* Prevent shrinking */
}

.pagination {
  margin-top: 1.25rem;
  display: flex;
  justify-content: center;
  flex-shrink: 0; /* Prevent shrinking */
}

/* Mobile Styles */
@media screen and (max-width: 900) {
  .container {
    padding: 0.5rem;
  }

  .select-container {
    margin-bottom: 1rem;
  }

  .table-container :deep(.el-table) {
    max-height: calc(92vh - 180px); /* Slightly adjusted for mobile */
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }

  .action-buttons .el-button {
    width: 100%;
    max-width: 200px;
  }
}

/* Tablet Styles */
@media screen and (min-width: 769px) and (max-width: 1024px) {
  .container {
    padding: 0.75rem;
  }

  .table-container :deep(.el-table) {
    max-height: calc(92vh - 190px); /* Adjusted for tablet */
  }
}

/* Handle table header sticky positioning */
.table-container :deep(.el-table__header-wrapper) {
  position: sticky;
  top: 0;
  z-index: 0;
  background: #fff;
}

/* Ensure proper scrollbar appearance */
.table-container :deep(.el-table__body-wrapper) {
  overflow-y: auto;
  scrollbar-width: thin;
}

/* Custom scrollbar styling for webkit browsers */
.table-container :deep(.el-table__body-wrapper)::-webkit-scrollbar {
  width: 6px;
}

.table-container :deep(.el-table__body-wrapper)::-webkit-scrollbar-track {
  background: #f1f1f1;
}

.table-container :deep(.el-table__body-wrapper)::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.table-container :deep(.el-table__body-wrapper)::-webkit-scrollbar-thumb:hover {
  background: #555;
}

:deep(.table-container){
  z-index: 0;
}
</style>