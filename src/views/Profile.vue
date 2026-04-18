<template>
  <div class="profile-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>
        <el-icon><User /></el-icon> 个人中心
      </h1>
      <p class="page-subtitle">查看您的个人信息、历史记录和系统设置</p>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧：用户信息 -->
      <div class="left-panel">
        <UserInfo />
        <SystemSettings />
      </div>

      <!-- 右侧：历史记录和帮助 -->
      <div class="right-panel">
        <UnifiedHistory />
        <HelpGuide />
      </div>
    </div>
  </div>
</template>

<script setup>
import { User } from "@element-plus/icons-vue";
import UserInfo from "@/components/profile/UserInfo.vue";
import SystemSettings from "@/components/profile/SystemSettings.vue";
import UnifiedHistory from "@/components/profile/UnifiedHistory.vue";
import HelpGuide from "@/components/profile/HelpGuide.vue";
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  background: #f7fafc;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.page-header h1 {
  font-size: 36px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.page-subtitle {
  font-size: 18px;
  color: #4a5568;
  max-width: 600px;
  margin: 0 auto;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 32px;
}

.left-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.right-panel {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .profile-page {
    padding: 16px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .page-subtitle {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
</style>
