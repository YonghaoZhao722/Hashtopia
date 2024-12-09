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
    // {
    //   path: '/create-post',
    //   name: 'CreatePost',
    //   component: () => import('@/views/PostView.vue'),
    //   meta: { requiresAuth: true }
    // },
    {
      path: '/profile/:id?',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      props: true,
      meta: {
        title: 'Profile'
      }
    },
  ],
})

export default router
