import { createRouter, createWebHistory } from "vue-router";
import { ElMessage } from "element-plus";
import Home from "../views/Home.vue";

// 懒加载其他页面
const PriceDetail = () => import("../views/PriceDetail.vue");
const ScheduleDetail = () => import("../views/ScheduleDetail.vue");
const Profile = () => import("../views/Profile.vue");
const Login = () => import("../views/Login.vue");
const Register = () => import("../views/Register.vue");
const Plans = () => import("../views/Plans.vue");

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
      requiresAuth: true, // 需要登录
    },
  },
  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      title: "登录 - 喂来日程",
      requiresAuth: false,
      hideNavigation: true, // 隐藏导航栏
    },
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: {
      title: "注册 - 喂来日程",
      requiresAuth: false,
      hideNavigation: true, // 隐藏导航栏
    },
  },
  {
    path: "/plans",
    name: "Plans",
    component: Plans,
    meta: {
      title: "计划管理 - 喂来日程",
      requiresAuth: true, // 需要登录
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

// 检查用户是否登录
const checkAuth = () => {
  const isLoggedIn = localStorage.getItem("isLoggedIn") === "true";
  const userInfo = localStorage.getItem("userInfo");
  return isLoggedIn && userInfo;
};

// 全局前置守卫 - 设置页面标题和权限验证
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  // 权限验证逻辑
  if (to.meta.requiresAuth) {
    const isAuthenticated = checkAuth();
    if (!isAuthenticated) {
      // 未登录，重定向到登录页面
      ElMessage.warning("请先登录");
      next("/login");
    } else {
      next();
    }
  } else if (to.name === "Login" || to.name === "Register") {
    // 如果用户已经登录，访问登录/注册页面时重定向到首页
    const isAuthenticated = checkAuth();
    if (isAuthenticated) {
      next("/");
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router;
