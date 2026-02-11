import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

// 布局组件
const DefaultLayout = () => import('@/layouts/DefaultLayout.vue')
const AuthLayout = () => import('@/layouts/AuthLayout.vue')

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue')
      },
      {
        path: 'houses',
        name: 'Houses',
        component: () => import('@/views/Houses.vue')
      },
      {
        path: 'recommend',
        name: 'Recommend',
        component: () => import('@/views/Recommend.vue')
      },
      {
        path: 'user-center',
        name: 'UserCenter',
        component: () => import('@/views/UserCenter.vue')
      }
    ]
  },
  {
    path: '/login',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: () => import('@/views/Login.vue')
      }
    ]
  },
  {
    path: '/register',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Register',
        component: () => import('@/views/Register.vue')
      }
    ]
  },
  {
    path: '/user',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'User',
        component: () => import('@/views/User.vue')
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router