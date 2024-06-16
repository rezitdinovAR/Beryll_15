import {createRouter, createWebHistory} from 'vue-router'

const routes = [

  {
    path: '/video',
    children: [
      {
        path: ':id',
        name: 'Video',
        component: () => import('@/components/SingleVideo.vue')
      }
    ],
  },
  {
    path: '/video',
    name: 'Videos',
    component: () => import('@/components/Videos.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: {name: 'Videos'}
  },

]
const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from) => {
  // TODO add something for videos further
})
export default router
