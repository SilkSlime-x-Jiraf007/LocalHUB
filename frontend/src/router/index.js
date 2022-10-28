import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import SignInView from '@/views/SignInView.vue'
import NotFoundView from '@/views/NotFoundView.vue'
import ForbiddenView from '@/views/ForbiddenView.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      component: AboutView
    },
    {
      path: '/signin',
      name: 'signin',
      component: SignInView
    },
    {
      path: '/403',
      name: '403',
      component: ForbiddenView
    },
    {
      path: '/404',
      name: '404',
      component: NotFoundView
    },
    { 
      path: "/:catchAll(.*)", 
      redirect: '/404' 
    }
  ]
})

export default router
