import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";

// 懒加载其他页面
const PriceDetail = () => import("../views/PriceDetail.vue");
const ScheduleDetail = () => import("../views/ScheduleDetail.vue");
const Profile = () => import("../views/Profile.vue");

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      title: "喂来日程 - 首页",
      requiresAuth: false,
    },
  },
  {
    path: "/price",
    name: "Price",
    component: PriceDetail,
    meta: {
      title: "一点外卖 - 详情",
      requiresAuth: false,
    },
  },
  {
    path: "/schedule",
    name: "Schedule",
    component: ScheduleDetail,
    meta: {
      title: "未来日程 - 详情",
      requiresAuth: false,
    },
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: {
      title: "个人中心",
      requiresAuth: false,
    },
  },
  // 重定向到首页
  {
    path: "/:pathMatch(.*)*",
    redirect: "/",
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// 全局前置守卫 - 设置页面标题
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  // 这里可以添加权限验证逻辑
  if (to.meta.requiresAuth) {
    // 检查用户是否登录
    // const isAuthenticated = checkAuth()
    // if (!isAuthenticated) {
    //   next('/login')
    // } else {
    //   next()
    // }
    next();
  } else {
    next();
  }
});

export default router;
