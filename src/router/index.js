import { createRouter, createWebHashHistory, createWebHistory } from 'vue-router'
// 项目创建时引入组件
// import NavLayout from '../views/HomeView.vue'
import store from '../store/index.js'

const routes = [
  {
    path: '/',
    name: 'navLayout',
    component: () => import('../views/Layout/NavLayout.vue'),
    // 子路由，又称为二级路由、嵌套路由，在本页面下保持地址不变，内容发生改变
    children: [
      {
        path: '/',
        name: 'index',
        component: () => import('../views/pages/indexList.vue')
      },
      {
        path: '/user',
        name: 'user',
        component: () => import('../views/pages/usersList.vue')
      },
      {
        path: '/roles',
        name: 'roles',
        component: () => import('../views/pages/rolesList.vue')
      },
      {
        path: '/goods',
        name: 'goods',
        component: () => import('../views/pages/goodsList.vue')
      },
    ]
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/pages/login.vue')
  }
]

const router = createRouter({
  // 哈希模式
  // history: createWebHashHistory(),

  // 历史模式
  history: createWebHistory(process.env.BASE_URL),
  // 路由配置
  routes
})

// 路由守卫
/**
 * to：跳转的页面
 * from：哪个页面跳的
 * next：放行函数，如果调用 next() 则表示放行，否则表示取消跳转
 */
router.beforeEach((to, from, next) => {
  // 登录验证
  console.log(store.state.userLogin);
  const uInfo = store.state.userLogin.userLogin;
  // console.log(uInfo.username);
  if (!uInfo.username) {
    if (to.path === '/login') {
      next()
      return;
    }
    next('/login')
  } else {
    next()
  }
})

export default router
