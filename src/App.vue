<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  HomeFilled,
  ShoppingCart,
  Calendar,
  User,
  Menu as IconMenu,
  SwitchButton,
  Setting,
  Search,
  Document,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const route = useRoute();
const router = useRouter();

// 用户状态
const isLoggedIn = ref(false);
const userInfo = ref(null);

// 检查登录状态
const checkLoginStatus = () => {
  const loggedIn = localStorage.getItem("isLoggedIn") === "true";
  const userData = localStorage.getItem("userInfo");

  isLoggedIn.value = loggedIn;
  if (userData) {
    try {
      userInfo.value = JSON.parse(userData);
    } catch (error) {
      userInfo.value = null;
    }
  } else {
    userInfo.value = null;
  }
};

// 当前激活的菜单
const activeMenu = computed(() => route.name || "Home");

// 是否显示导航栏
const showNavigation = computed(() => {
  return !route.meta.hideNavigation;
});

// 导航菜单项
const menuItems = [
  { name: "Home", path: "/", icon: HomeFilled, label: "首页" },
  { name: "Search", path: "/search", icon: Search, label: "智能搜索" },
  {
    name: "PriceSearch",
    path: "/price-search",
    icon: ShoppingCart,
    label: "价格查询",
  },
  { name: "Schedule", path: "/schedule", icon: Calendar, label: "未来日程" },
  { name: "Plans", path: "/plans", icon: Document, label: "计划管理" },
  { name: "Profile", path: "/profile", icon: User, label: "个人中心" },
];

// 移动端菜单状态
const isMobileMenuOpen = ref(false);

// 导航到指定页面
const navigateTo = (path) => {
  router.push(path);
  isMobileMenuOpen.value = false;
};

// 用户操作
const handleUserCommand = (command) => {
  switch (command) {
    case "profile":
      router.push("/profile");
      break;
    case "settings":
      // 这里可以跳转到设置页面
      ElMessage.info("设置功能开发中");
      break;
    case "logout":
      handleLogout();
      break;
  }
};

const handleLogout = () => {
  localStorage.removeItem("isLoggedIn");
  localStorage.removeItem("userInfo");
  isLoggedIn.value = false;
  userInfo.value = null;
  ElMessage.success("已退出登录");

  if (route.meta.requiresAuth) {
    router.push("/login");
  } else {
    router.push("/");
  }
};

const handleLogin = () => {
  router.push("/login");
};

// 响应式判断
const isMobile = ref(false);
const handleResize = () => {
  isMobile.value = window.innerWidth < 768;
};

// 监听路由变化
watch(
  () => route.path,
  () => {
    checkLoginStatus();
    isMobileMenuOpen.value = false;
  },
);

onMounted(() => {
  handleResize();
  window.addEventListener("resize", handleResize);
  checkLoginStatus();
});

onUnmounted(() => {
  window.removeEventListener("resize", handleResize);
});
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header" v-if="showNavigation">
      <div class="header-container">
        <!-- Logo和标题 -->
        <div class="header-logo" @click="navigateTo('/')">
          <div class="logo-icon">🤖</div>
          <div class="logo-text">
            <h1>喂来日程</h1>
            <p class="logo-subtitle">一点外卖 + 未来日程</p>
          </div>
        </div>

        <!-- 用户操作区域 -->
        <div class="user-actions" v-if="!isMobile">
          <div class="user-info" v-if="isLoggedIn && userInfo">
            <span class="username">{{ userInfo.username }}</span>
            <el-dropdown @command="handleUserCommand">
              <span class="user-avatar">
                <el-avatar :size="32" :src="userInfo.avatar">
                  {{ userInfo.username.charAt(0).toUpperCase() }}
                </el-avatar>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>
                    个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>
                    设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
          <div class="auth-buttons" v-else>
            <el-button type="primary" size="small" @click="handleLogin">
              登录
            </el-button>
            <el-button size="small" @click="navigateTo('/register')">
              注册
            </el-button>
          </div>
        </div>

        <!-- 桌面端导航菜单 -->
        <nav class="desktop-nav" v-if="!isMobile">
          <el-menu
            :default-active="activeMenu"
            mode="horizontal"
            class="main-menu"
            @select="
              (key) =>
                navigateTo(
                  menuItems.find((item) => item.name === key)?.path || '/',
                )
            "
          >
            <el-menu-item
              v-for="item in menuItems"
              :key="item.name"
              :index="item.name"
              class="menu-item"
            >
              <el-icon><component :is="item.icon" /></el-icon>
              <span>{{ item.label }}</span>
            </el-menu-item>
          </el-menu>
        </nav>

        <!-- 移动端菜单按钮 -->
        <div
          class="mobile-menu-btn"
          v-if="isMobile"
          @click="isMobileMenuOpen = !isMobileMenuOpen"
        >
          <el-icon size="24"><IconMenu /></el-icon>
        </div>
      </div>

      <!-- 移动端下拉菜单 -->
      <div class="mobile-menu" v-if="isMobile && isMobileMenuOpen">
        <div class="mobile-menu-content">
          <div
            v-for="item in menuItems"
            :key="item.name"
            class="mobile-menu-item"
            :class="{ active: activeMenu === item.name }"
            @click="navigateTo(item.path)"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </div>
          <!-- 移动端用户操作 -->
          <div class="mobile-user-actions">
            <div v-if="isLoggedIn && userInfo" class="mobile-user-info">
              <el-avatar :size="40" :src="userInfo.avatar">
                {{ userInfo.username.charAt(0).toUpperCase() }}
              </el-avatar>
              <div class="mobile-user-details">
                <div class="mobile-username">{{ userInfo.username }}</div>
                <div class="mobile-email">{{ userInfo.email }}</div>
              </div>
            </div>
            <div class="mobile-auth-buttons" v-else>
              <el-button
                type="primary"
                @click="handleLogin"
                class="mobile-login-btn"
              >
                登录
              </el-button>
              <el-button
                @click="navigateTo('/register')"
                class="mobile-register-btn"
              >
                注册
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <!-- 移动端底部导航 -->
    <footer class="mobile-footer" v-if="isMobile">
      <div class="footer-nav">
        <div
          v-for="item in menuItems"
          :key="item.name"
          class="footer-nav-item"
          :class="{ active: activeMenu === item.name }"
          @click="navigateTo(item.path)"
        >
          <el-icon><component :is="item.icon" /></el-icon>
          <span class="footer-nav-label">{{ item.label }}</span>
        </div>
      </div>
    </footer>

    <!-- 页面加载进度条 -->
    <div class="page-loading" v-if="false">
      <div class="loading-bar"></div>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 顶部导航栏样式 */
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  box-shadow: 0 2px 12px rgba(102, 126, 234, 0.2);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
}

.header-logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.header-logo:hover {
  opacity: 0.9;
}

.logo-icon {
  font-size: 32px;
}

.logo-text h1 {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 12px;
  opacity: 0.9;
  margin: 0;
}

/* 用户操作区域 */
.user-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.username {
  font-size: 14px;
  font-weight: 500;
  color: white;
}

.user-avatar {
  cursor: pointer;
  transition: opacity 0.2s;
}

.user-avatar:hover {
  opacity: 0.9;
}

.auth-buttons {
  display: flex;
  gap: 8px;
}

/* 桌面端导航菜单 */
.desktop-nav {
  flex: 1;
  display: flex;
  justify-content: center;
}

.main-menu {
  background: transparent;
  border: none;
}

.main-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.9);
  font-weight: 500;
  height: 64px;
  border-bottom: 3px solid transparent;
  transition: all 0.3s;
}

.main-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.main-menu :deep(.el-menu-item.is-active) {
  color: white;
  border-bottom-color: white;
  background: rgba(255, 255, 255, 0.1);
}

.main-menu :deep(.el-menu-item .el-icon) {
  margin-right: 6px;
}

/* 移动端菜单按钮 */
.mobile-menu-btn {
  padding: 8px;
  cursor: pointer;
  border-radius: 6px;
  transition: background 0.2s;
}

.mobile-menu-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

/* 移动端下拉菜单 */
.mobile-menu {
  background: white;
  border-top: 1px solid #e4e7ed;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.mobile-menu-content {
  padding: 12px 0;
}

.mobile-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 24px;
  cursor: pointer;
  transition: background 0.2s;
  color: #606266;
}

.mobile-menu-item:hover {
  background: #f5f7fa;
}

.mobile-menu-item.active {
  color: #409eff;
  background: #ecf5ff;
}

.mobile-menu-item .el-icon {
  font-size: 18px;
}

/* 移动端用户操作 */
.mobile-user-actions {
  padding: 16px 24px;
  border-top: 1px solid #e4e7ed;
}

.mobile-user-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.mobile-user-details {
  flex: 1;
}

.mobile-username {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.mobile-email {
  font-size: 14px;
  color: #909399;
}

.mobile-auth-buttons {
  display: flex;
  gap: 12px;
}

.mobile-login-btn,
.mobile-register-btn {
  flex: 1;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 24px 20px;
}

/* 移动端底部导航 */
.mobile-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  border-top: 1px solid #e4e7ed;
  box-shadow: 0 -2px 12px rgba(0, 0, 0, 0.05);
  z-index: 1000;
}

.footer-nav {
  display: flex;
  justify-content: space-around;
  padding: 8px 0;
}

.footer-nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  transition: color 0.2s;
  color: #909399;
  flex: 1;
}

.footer-nav-item:hover {
  color: #409eff;
}

.footer-nav-item.active {
  color: #409eff;
}

.footer-nav-item .el-icon {
  font-size: 20px;
  margin-bottom: 4px;
}

.footer-nav-label {
  font-size: 11px;
}

/* 页面切换动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 页面加载进度条 */
.page-loading {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: transparent;
  z-index: 2000;
}

.loading-bar {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  animation: loading 1.5s infinite;
}

@keyframes loading {
  0% {
    width: 0%;
    transform: translateX(0);
  }
  50% {
    width: 70%;
  }
  100% {
    width: 100%;
    transform: translateX(100%);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    height: 56px;
  }

  .logo-icon {
    font-size: 28px;
  }

  .logo-text h1 {
    font-size: 18px;
  }

  .logo-subtitle {
    font-size: 11px;
  }

  .main-content {
    padding: 16px;
    padding-bottom: 72px; /* 为底部导航留出空间 */
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0 12px;
  }

  .main-content {
    padding: 12px;
    padding-bottom: 72px;
  }
}
</style>

<style>
/* 全局样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu,
    Cantarell, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* Element Plus 全局样式覆盖 */
.el-tabs__item {
  font-weight: 500;
}

.el-card {
  border-radius: 12px;
}

.el-button {
  border-radius: 8px;
}

.el-input__inner {
  border-radius: 8px;
}

.el-tag {
  border-radius: 6px;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

/* 深色主题样式 */
.dark-theme body {
  background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
  color: #e2e8f0;
}

.dark-theme .app-header {
  background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
}

.dark-theme .main-menu :deep(.el-menu-item) {
  color: rgba(255, 255, 255, 0.8);
}

.dark-theme .main-menu :deep(.el-menu-item:hover) {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

.dark-theme .main-menu :deep(.el-menu-item.is-active) {
  color: white;
  border-bottom-color: white;
  background: rgba(255, 255, 255, 0.1);
}

.dark-theme .mobile-menu {
  background: #2d3748;
  border-top: 1px solid #4a5568;
}

.dark-theme .mobile-menu-item {
  color: #cbd5e0;
}

.dark-theme .mobile-menu-item:hover {
  background: #4a5568;
}

.dark-theme .mobile-menu-item.active {
  color: #63b3ed;
  background: #2d3748;
}

.dark-theme .mobile-footer {
  background: #2d3748;
  border-top: 1px solid #4a5568;
}

.dark-theme .footer-nav-item {
  color: #a0aec0;
}

.dark-theme .footer-nav-item:hover {
  color: #63b3ed;
}

.dark-theme .footer-nav-item.active {
  color: #63b3ed;
}

/* 深色主题下的滚动条 */
.dark-theme ::-webkit-scrollbar-track {
  background: #2d3748;
}

.dark-theme ::-webkit-scrollbar-thumb {
  background: #4a5568;
}

.dark-theme ::-webkit-scrollbar-thumb:hover {
  background: #718096;
}

/* Element Plus 深色主题变量 */
.dark-theme {
  --el-color-primary: #409eff;
  --el-color-primary-light-3: #3375b9;
  --el-color-primary-light-5: #2a598a;
  --el-color-primary-light-7: #213d5b;
  --el-color-primary-light-9: #1d3043;
  --el-color-primary-dark-2: #66b1ff;

  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger: #f56c6c;
  --el-color-error: #f56c6c;
  --el-color-info: #909399;

  --el-bg-color: #1a202c;
  --el-bg-color-page: #0a0c10;
  --el-bg-color-overlay: #1d1e1f;

  --el-text-color-primary: #e5eaf3;
  --el-text-color-regular: #cfd3dc;
  --el-text-color-secondary: #a3a6ad;
  --el-text-color-placeholder: #8d9095;
  --el-text-color-disabled: #6c6e72;

  --el-border-color: #4c4d4f;
  --el-border-color-light: #414243;
  --el-border-color-lighter: #363637;
  --el-border-color-extra-light: #2b2b2c;

  --el-fill-color: #424243;
  --el-fill-color-light: #39393a;
  --el-fill-color-lighter: #303030;
  --el-fill-color-extra-light: #262727;
  --el-fill-color-blank: transparent;

  --el-mask-color: rgba(0, 0, 0, 0.8);
  --el-mask-color-extra-light: rgba(0, 0, 0, 0.3);
}

/* Element Plus 组件深色样式 */
.dark-theme .el-card {
  background-color: var(--el-bg-color-overlay);
  border-color: var(--el-border-color-light);
}

.dark-theme .el-card__header {
  border-bottom-color: var(--el-border-color-light);
  color: var(--el-text-color-primary);
}

.dark-theme .el-button {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
  color: var(--el-text-color-primary);
}

.dark-theme .el-button:hover {
  background-color: var(--el-fill-color-light);
  border-color: var(--el-border-color-light);
}

.dark-theme .el-button--primary {
  background-color: var(--el-color-primary);
  border-color: var(--el-color-primary);
}

.dark-theme .el-button--primary:hover {
  background-color: var(--el-color-primary-light-3);
  border-color: var(--el-color-primary-light-3);
}

.dark-theme .el-switch__core {
  background-color: var(--el-fill-color);
  border-color: var(--el-border-color);
}

.dark-theme .el-switch.is-checked .el-switch__core {
  background-color: var(--el-color-primary);
  border-color: var(--el-color-primary);
}

.dark-theme .el-tabs__item {
  color: var(--el-text-color-regular);
}

.dark-theme .el-tabs__item:hover {
  color: var(--el-text-color-primary);
}

.dark-theme .el-tabs__item.is-active {
  color: var(--el-color-primary);
}

.dark-theme .el-tabs__active-bar {
  background-color: var(--el-color-primary);
}

.dark-theme .el-tabs__nav-wrap::after {
  background-color: var(--el-border-color-light);
}

.dark-theme .el-input__wrapper {
  background-color: var(--el-bg-color);
  border-color: var(--el-border-color);
}

.dark-theme .el-input__inner {
  color: var(--el-text-color-primary);
}

.dark-theme .el-input__inner::placeholder {
  color: var(--el-text-color-placeholder);
}

.dark-theme .el-dialog {
  background-color: var(--el-bg-color-overlay);
  border-color: var(--el-border-color-light);
}

.dark-theme .el-dialog__header {
  color: var(--el-text-color-primary);
  border-bottom-color: var(--el-border-color-light);
}

.dark-theme .el-dialog__body {
  color: var(--el-text-color-regular);
}

.dark-theme .el-message-box {
  background-color: var(--el-bg-color-overlay);
  border-color: var(--el-border-color-light);
}

.dark-theme .el-message-box__title {
  color: var(--el-text-color-primary);
}

.dark-theme .el-message-box__content {
  color: var(--el-text-color-regular);
}
</style>
