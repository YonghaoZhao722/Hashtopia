import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/profile/:username?',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      props: true,
      meta: { 
        title: '个人主页'
      }
    },
    {
      // 用户详情页的另一个URL格式
      path: '/user/:username',
      redirect: to => {
        return { path: `/profile/${to.params.username}` }
      }
    },
    
  ],
})

// 路由守卫（如果已有就不需要添加）
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - Hashtopia`
  }
  next()
})

export default router