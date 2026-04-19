<template>
  <el-card class="user-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><UserFilled /></el-icon>
        <span>个人信息</span>
      </div>
    </template>

    <div class="user-info">
      <div class="avatar-section">
        <div class="avatar">
          <el-avatar :size="80" :icon="UserFilled" />
        </div>
        <div class="user-basic">
          <h3>喂来日程用户</h3>
          <p class="user-email">user@example.com</p>
          <el-tag type="success" size="small">普通用户</el-tag>
        </div>
      </div>

      <div class="user-stats">
        <div class="stat-item">
          <div class="stat-value">12</div>
          <div class="stat-label">比价次数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">8</div>
          <div class="stat-label">未来日程</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">5</div>
          <div class="stat-label">日历文件</div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { UserFilled } from "@element-plus/icons-vue";
</script>

<style scoped>
.user-card {
  height: fit-content;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: #1a202c;
}

.card-header .el-icon {
  color: #667eea;
}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar {
  flex-shrink: 0;
}

.user-basic h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.user-email {
  font-size: 14px;
  color: #718096;
  margin: 0 0 12px 0;
}

.user-stats {
  display: flex;
  justify-content: space-around;
  padding: 16px;
  background: #f7fafc;
  border-radius: 8px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #667eea;
}

.stat-label {
  font-size: 12px;
  color: #718096;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .avatar-section {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .user-stats {
    flex-direction: column;
    gap: 16px;
  }
}
</style>
