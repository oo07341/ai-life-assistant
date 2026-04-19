<script setup>
import { ref, computed,onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import {
  HomeFilled,
  ShoppingCart,
  Calendar,
  User,
  Menu as IconMenu,
} from "@element-plus/icons-vue";

const route = useRoute();
const router = useRouter();

// 当前激活的菜单
const activeMenu = computed(() => route.name || "Home");

// 导航菜单项
const menuItems = [
  { name: "Home", path: "/", icon: HomeFilled, label: "首页" },
  { name: "Price", path: "/price", icon: ShoppingCart, label: "智能比价" },
  { name: "Schedule", path: "/schedule", icon: Calendar, label: "日程规划" },
  { name: "Profile", path: "/profile", icon: User, label: "个人中心" },
];

// 移动端菜单状态
const isMobileMenuOpen = ref(false);

// 导航到指定页面
const navigateTo = (path) => {
  router.push(path);
  isMobileMenuOpen.value = false;
};

// 响应式判断
const isMobile = ref(window.innerWidth < 768);
window.addEventListener("resize", () => {
  isMobile.value = window.innerWidth < 768;
  onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<template>
  <div class="app-container">
    <!-- 顶部导航栏 -->
    <header class="app-header">
      <div class="header-container">
        <!-- Logo和标题 -->
        <div class="header-logo" @click="navigateTo('/')">
          <div class="logo-icon">🤖</div>
          <div class="logo-text">
            <h1>AI生活助手</h1>
            <p class="logo-subtitle">智能比价 + 日程规划</p>
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
</style>
