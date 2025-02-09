import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: () => import('../views/Home.vue'), },
    { path: '/upload', name: 'upload', component: () => import('@/components/Upload.vue'), },
  ],
})

export default router
