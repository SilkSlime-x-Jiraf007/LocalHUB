import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

import FeedListView from '@/views/FeedListView.vue'
import SignInView from '@/views/SignInView.vue'
import UploadView from '@/views/UploadView.vue'
import TagsListView from '@/views/TagsListView.vue'

import ProfileView from '@/views/ProfileViews/ProfileView.vue'
import ProfileSettingsView from '@/views/ProfileViews/ProfileSettingsView.vue'

import ImagesListView from '@/views/ListViews/ImagesListView.vue'
import MangasListView from '@/views/ListViews/MangasListView.vue'
import StoriesListView from '@/views/ListViews/StoriesListView.vue'
import VideosListView from '@/views/ListViews/VideosListView.vue'

import NotFoundView from '@/views/ErrorViews/NotFoundView.vue'
import ForbiddenView from '@/views/ErrorViews/ForbiddenView.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Base
    {
      path: '/',
      name: 'Feed',
      component: FeedListView
    },
    {
      path: '/signin',
      name: 'Sign In',
      component: SignInView,
    },
    {
      path: '/upload',
      name: 'Upload',
      component: UploadView,
    },
    {
      path: '/tags',
      name: 'Tags',
      component: TagsListView
    },

    // Profile
    {
      path: '/user',
      name: 'Profile',
      component: ProfileView,
    },
    {
      path: '/user/settings',
      name: 'Settings',
      component: ProfileSettingsView,
    },


    // List
    
    {
      path: '/images',
      name: 'Images',
      component: ImagesListView
    },
    {
      path: '/mangas',
      name: 'Mangas',
      component: MangasListView
    },
    {
      path: '/stories',
      name: 'Stories',
      component: StoriesListView
    },
    {
      path: '/videos',
      name: 'Videos',
      component: VideosListView
    },
    



    // Errors
    {
      path: '/403',
      name: 'Forbidden',
      component: ForbiddenView,
    },
    {
      path: '/404',
      name: 'Not Found',
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
    if (to.name == 'Sign In')
      return { name: 'Feed' }
    else
      return true
  else
    if (to.name == 'Sign In')
      return true
    else
      return { name: 'Sign In' }
})

export default router
