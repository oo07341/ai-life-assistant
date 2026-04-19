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
          <div class="stat-value">{{ stats.priceComparisonCount || 0 }}</div>
          <div class="stat-label">比价次数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.futureScheduleCount || 0 }}</div>
          <div class="stat-label">未来日程</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ stats.calendarFileCount || 0 }}</div>
          <div class="stat-label">日历文件</div>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { UserFilled } from "@element-plus/icons-vue";
import { ref, onMounted } from "vue";
import { userAPI, planAPI } from "@/services/api.js";

const stats = ref({
  priceComparisonCount: 0,
  futureScheduleCount: 0,
  calendarFileCount: 0,
});

// 模拟用户ID（实际项目中应从登录状态获取）
const mockUserId = "test-user-123";

async function loadUserStats() {
  try {
    // 使用新的stats接口获取统计数据
    const statsData = await userAPI.getStats();

    stats.value = {
      priceComparisonCount: statsData.price_comparison_count || 0,
      futureScheduleCount: statsData.future_schedule_count || 0,
      calendarFileCount: statsData.calendar_file_count || 0,
    };
  } catch (error) {
    console.error("加载用户统计信息失败:", error);
    // 如果新接口失败，回退到旧方法
    try {
      const profile = await userAPI.getProfile();
      const plans = await planAPI.getPlans();
      const calendarFileCount = plans.filter((plan) => plan.ics_content).length;

      stats.value = {
        priceComparisonCount: 12, // 临时模拟数据
        futureScheduleCount: profile.plan_count || plans.length || 0,
        calendarFileCount: calendarFileCount,
      };
    } catch (fallbackError) {
      console.error("回退方法也失败:", fallbackError);
      // 使用默认值
      stats.value = {
        priceComparisonCount: 0,
        futureScheduleCount: 0,
        calendarFileCount: 0,
      };
    }
  }
}

onMounted(() => {
  loadUserStats();
});
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
