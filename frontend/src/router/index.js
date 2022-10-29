import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import AboutView from '@/views/AboutView.vue'
import SignInView from '@/views/SignInView.vue'
import NotFoundView from '@/views/errorViews/NotFoundView.vue'
import ForbiddenView from '@/views/errorViews/ForbiddenView.vue'
import { useUserStore } from '@/stores/user'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Auth
    {
      path: '/signin',
      name: 'SignIn',
      component: SignInView,
    },


    // Base
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'About',
      component: AboutView
    },



    // Errors
    {
      path: '/403',
      name: '403',
      component: ForbiddenView,
    },
    {
      path: '/404',
      name: '404',
      component: NotFoundView,
    },
    {
      path: "/:catchAll(.*)",
      redirect: '/404'
    }
  ]
})

router.beforeEach((to, from) => {
  const userStore = useUserStore()
  if (userStore.hasUser())
    if (to.name == 'SignIn')
      return { name: 'Home' }
    else
      return true
  else
    if (to.name == 'SignIn')
      return true
    else
      return { name: 'SignIn' }
})

export default router
