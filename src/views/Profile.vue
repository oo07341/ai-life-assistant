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
        <div class="placeholder-card">
          <h3>
            <el-icon><Setting /></el-icon> 系统设置
          </h3>
          <p class="placeholder-text">系统设置功能正在开发中...</p>
        </div>
      </div>

      <!-- 右侧：历史记录和帮助 -->
      <div class="right-panel">
        <div class="placeholder-card">
          <h3>
            <el-icon><Clock /></el-icon> 历史记录
          </h3>
          <p class="placeholder-text">历史记录功能正在开发中...</p>
        </div>
        <div class="placeholder-card">
          <h3>
            <el-icon><QuestionFilled /></el-icon> 使用帮助
          </h3>
          <p class="placeholder-text">帮助文档功能正在开发中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { User, Setting, Clock, QuestionFilled } from "@element-plus/icons-vue";
import UserInfo from "@/components/profile/UserInfo.vue";
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

/* 占位卡片样式 */
.placeholder-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
  transition:
    transform 0.2s,
    box-shadow 0.2s;
}

.placeholder-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}

.placeholder-card h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.placeholder-card h3 .el-icon {
  color: #4299e1;
}

.placeholder-text {
  font-size: 16px;
  color: #718096;
  line-height: 1.6;
  margin: 0;
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

  .placeholder-card {
    padding: 20px;
  }

  .placeholder-card h3 {
    font-size: 18px;
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .placeholder-card {
    padding: 16px;
  }

  .placeholder-card h3 {
    font-size: 16px;
  }

  .placeholder-text {
    font-size: 14px;
  }
}
</style>
