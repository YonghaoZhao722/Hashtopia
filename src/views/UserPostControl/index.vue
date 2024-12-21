<script setup xmlns="http://www.w3.org/1999/html">
import {computed, onBeforeMount, onMounted, ref, onBeforeUnmount} from 'vue'
import {queryUserPostControl, postDelete, controlUserCollectOrLike, unFollow, removeFan} from "@/apis/main";
import {ElMessage} from 'element-plus'
import {useUserStore} from "@/stores/user";
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
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
// 配置全局语言和表格缓存//////////////////////////////////////////////
const locale = zhCn
const tableStore = useTableStore();
const loading = ref(true)
const isMobile = ref(false)
// 控制选择器 /////////////////////////////////////////////////////
const value = ref('posts')

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
}

const options = [
  {
    label: '帖子管理',
    options: [
      {
        value: 'posts',
        label: '个人帖子管理',
      },
      {
        value: 'collected',
        label: '收藏帖子管理',
      },
      {
        value: 'favorites',
        label: '喜欢帖子管理'
      }
    ],
  },
  {
    label: '个人用户管理',
    options: [
      {
        value: 'fans',
        label: '粉丝管理',
      },
      {
        value: 'follow',
        label: '关注管理',
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
  // 先将多选置空
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

// 表格/////////////////////////////////////////////////////////
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
      { type: 'selection', width: '55' },
      { label: '标题', prop: 'title' },
      { label: '操作', slot: 'operation', align: 'center' }
    ] : [
      { type: 'selection', width: '55' },
      { label: '用户名', prop: 'username' },
      { label: '操作', slot: 'operation', align: 'center' }
    ]
  }
  
  return type.value === 1 ? [
    { type: 'selection', width: '55' },
    { label: '日期', prop: 'date', sortable: true },
    { label: '作者', prop: 'username' },
    { label: '标题', prop: 'title' },
    { label: '内容', prop: 'content', showOverflowTooltip: true },
    { label: '评论量', prop: 'commentCount', sortable: true },
    { label: '点赞量', prop: 'likeCount', sortable: true },
    { label: '收藏量', prop: 'collectCount', sortable: true },
    { label: '操作', slot: 'operation', align: 'center' }
  ] : [
    { type: 'selection', width: '55' },
    { label: '头像', slot: 'avatar', align: 'center' },
    { label: '用户名', prop: 'username', sortable: true, showOverflowTooltip: true },
    { label: '粉丝量', prop: 'fans' },
    { label: '关注量', prop: 'follow' },
    { label: '笔记数', prop: 'note' },
    { label: '操作', slot: 'operation', align: 'center' }
  ]
})
// 分页器 ///////////////////////////////////////////////////////
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
        >
          <template #prefix>
            <el-tooltip
                placement="top"
                effect="light"
            >
              <template #content>
                <h2 style="color:red;">表格内容会缓存到本地</h2>
                <p>如果进行
                  <span style="color:red;">修改数据</span>
                  没有更新
                  <span style="color:red;">刷新就可以了</span>
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
            style="width: 100%"
            ref="tableRef"
            :default-sort="{ prop: 'date', order: 'descending' }"
            @selection-change="handleSelectionChange"
            v-loading="loading"
            border
            stripe
            :size="isMobile ? 'small' : 'default'"
        >
          <template v-for="col in getTableColumns" :key="col.prop || col.type">
            <el-table-column v-bind="col">
              <template #default="scope" v-if="col.slot === 'operation'">
                <el-button
                    :size="isMobile ? 'small' : 'default'"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">
                  删除
                </el-button>
              </template>
            </el-table-column>
          </template>
        </el-table>

        <div class="action-buttons" v-show="multipleSelection.length !== 0">
          <el-button disabled round :size="isMobile ? 'small' : 'default'">选中删除</el-button>
          <el-button @click="tableRef.clearSelection()" round :size="isMobile ? 'small' : 'default'">清空全选</el-button>
        </div>

        <div class="pagination">
          <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :background="true"
              layout="prev, pager, next, jumper"
              :total="total_post"
              @current-change="handleCurrentChange"
              :small="isMobile"
          />
        </div>
      </div>

      <div class="table-container" v-else>
        <el-table
            :data="userData"
            style="width: 100%"
            ref="tableRef"
            @selection-change="handleSelectionChange"
            border
            v-loading="loading"
            stripe
            :size="isMobile ? 'small' : 'default'"
        >
          <template v-for="col in getTableColumns" :key="col.prop || col.type">
            <el-table-column v-bind="col">
              <template #default="scope" v-if="col.slot === 'avatar'">
                <el-avatar :size="isMobile ? 'small' : 'default'" :src="scope.row.avatar"></el-avatar>
              </template>
              <template #default="scope" v-if="col.slot === 'operation'">
                <el-button
                    :size="isMobile ? 'small' : 'default'"
                    type="danger"
                    @click="handleDelete(scope.$index, scope.row)">
                  移除
                </el-button>
              </template>
            </el-table-column>
          </template>
        </el-table>

        <div class="action-buttons" v-show="multipleSelection.length !== 0">
          <el-button disabled round :size="isMobile ? 'small' : 'default'">选中删除</el-button>
          <el-button @click="tableRef.clearSelection()" round :size="isMobile ? 'small' : 'default'">清空全选</el-button>
        </div>

        <div class="pagination">
          <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :background="true"
              layout="prev, pager, next, jumper"
              :total="total_user"
              @current-change="handleCurrentChange"
              :small="isMobile"
          />
        </div>
      </div>
    </div>
  </el-config-provider>
</template>

<style scoped>
.container {
  width: 100%;
  padding: 1rem;
  box-sizing: border-box;
}

.select-container {
  margin-bottom: 1.25rem;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.action-buttons {
  margin-top: 1.25rem;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
}

.pagination {
  margin-top: 1.25rem;
  display: flex;
  justify-content: center;
}

/* Mobile Styles */
@media screen and (max-width: 768px) {
  .container {
    padding: 0.5rem;
  }

  .select-container {
    margin-bottom: 1rem;
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
}
</style>