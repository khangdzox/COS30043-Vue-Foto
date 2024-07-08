import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    component: () => import(/* webpackChunkName: "register" */ '../views/RegisterView.vue')
  },
  {
    path: '/post/:postId',
    name: 'post',
    component: () => import(/* webpackChunkName: "post" */ '../views/PostView.vue')
  },
  {
    path: '/user/:userId',
    name: 'user',
    component: () => import(/* webpackChunkName: "user" */ '../views/UserView.vue')
  },
  {
    path: '/user/edit',
    name: 'user-edit',
    component: () => import(/* webpackChunkName: "user-edit" */ '../views/UserEditView.vue')
  },
  {
    path: '/post/new',
    name: 'post-new',
    component: () => import(/* webpackChunkName: "post-new" */ '../views/PostEditView.vue')
  },
  {
    path: '/post/:postId/edit',
    name: 'post-edit',
    component: () => import(/* webpackChunkName: "post-edit" */ '../views/PostEditView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

export default router
