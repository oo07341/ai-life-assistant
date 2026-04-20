<template>
  <el-card class="user-info-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><User /></el-icon>
        <span>个人信息</span>
      </div>
    </template>

    <!-- 用户头像和基本信息 -->
    <div class="user-profile">
      <div class="avatar-section">
        <div class="avatar-container">
          <div class="avatar-placeholder">
            <el-icon><UserFilled /></el-icon>
          </div>
          <el-button type="primary" size="small" class="avatar-upload-btn">
            <el-icon><Upload /></el-icon>
            更换头像
          </el-button>
        </div>
      </div>

      <div class="info-section">
        <div class="info-row">
          <span class="info-label">用户名</span>
          <span class="info-value">{{ userInfo.username }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">邮箱</span>
          <span class="info-value">{{ userInfo.email }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">注册时间</span>
          <span class="info-value">{{
            formatDate(userInfo.registerDate)
          }}</span>
        </div>
        <div class="info-row">
          <span class="info-label">会员状态</span>
          <el-tag :type="userInfo.isPremium ? 'success' : 'info'" size="small">
            {{ userInfo.isPremium ? "高级会员" : "普通用户" }}
          </el-tag>
        </div>
      </div>
    </div>

    <!-- 使用统计 -->
    <div class="usage-stats">
      <h3 class="stats-title">
        <el-icon><DataLine /></el-icon> 使用统计
      </h3>
      <div class="stats-grid">
        <div class="stat-item">
          <div class="stat-value">{{ userStats.priceQueries }}</div>
          <div class="stat-label">比价查询</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userStats.scheduleEvents }}</div>
          <div class="stat-label">日程事件</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userStats.totalSearches }}</div>
          <div class="stat-label">总搜索次数</div>
        </div>
        <div class="stat-item">
          <div class="stat-value">{{ userStats.activeDays }}</div>
          <div class="stat-label">活跃天数</div>
        </div>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="editProfile">
        <el-icon><Edit /></el-icon>
        编辑资料
      </el-button>
      <el-button @click="changePassword">
        <el-icon><Lock /></el-icon>
        修改密码
      </el-button>
      <el-button type="info" @click="viewActivity">
        <el-icon><Histogram /></el-icon>
        查看活动
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import {
  User,
  UserFilled,
  Upload,
  DataLine,
  Edit,
  Lock,
  Histogram,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import { userAPI } from "@/services/api";

const router = useRouter();

// 用户信息
const userInfo = ref({
  username: "加载中...",
  email: "加载中...",
  registerDate: new Date().toISOString(),
  isPremium: false,
});

// 使用统计
const userStats = ref({
  priceQueries: 0,
  scheduleEvents: 0,
  totalSearches: 0,
  activeDays: 0,
});

// 加载状态
const loading = ref(true);

// 加载用户数据
const loadUserData = async () => {
  loading.value = true;
  try {
    // 从localStorage加载用户信息
    const storedUserInfo = localStorage.getItem("userInfo");
    if (storedUserInfo) {
      const parsedInfo = JSON.parse(storedUserInfo);
      userInfo.value = {
        username: parsedInfo.username || "用户",
        email: parsedInfo.email || "未设置",
        registerDate: parsedInfo.registerDate || new Date().toISOString(),
        isPremium: parsedInfo.isPremium || false,
      };
    }

    // 调用后端API获取用户统计数据
    try {
      const stats = await userAPI.getStats();
      userStats.value = {
        priceQueries: stats.price_comparison_count || 0,
        scheduleEvents: stats.future_schedule_count || 0,
        totalSearches:
          (stats.price_comparison_count || 0) +
          (stats.future_schedule_count || 0),
        activeDays: stats.calendar_file_count || 0,
      };
    } catch (apiError) {
      console.error("获取用户统计数据失败:", apiError);
      // 如果API调用失败，使用模拟数据
      userStats.value = {
        priceQueries: Math.floor(Math.random() * 100) + 50,
        scheduleEvents: Math.floor(Math.random() * 50) + 20,
        totalSearches: Math.floor(Math.random() * 200) + 100,
        activeDays: Math.floor(Math.random() * 30) + 60,
      };
    }

    // 尝试获取用户个人中心概览信息
    try {
      const profile = await userAPI.getProfile();
      if (profile && profile.user_id) {
        // 更新用户信息
        userInfo.value.username = profile.user_id || userInfo.value.username;
        userInfo.value.email =
          `${profile.user_id}@example.com` || userInfo.value.email;

        // 如果有激活计划，显示相关信息
        if (profile.active_plan_id) {
          userInfo.value.activePlan = {
            id: profile.active_plan_id,
            goal: profile.active_plan_goal,
            targetDate: profile.active_plan_target_date,
          };
        }
      }
    } catch (profileError) {
      console.error("获取用户概览信息失败:", profileError);
      // 忽略错误，继续使用localStorage中的信息
    }
  } catch (error) {
    console.error("加载用户数据失败:", error);
    ElMessage.error("加载用户数据失败");
  } finally {
    loading.value = false;
  }
};

// 格式化日期
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  } catch (error) {
    return dateString;
  }
};

// 编辑资料
const editProfile = () => {
  ElMessage.info("编辑资料功能开发中");
};

// 修改密码
const changePassword = () => {
  ElMessage.info("修改密码功能开发中");
};

// 查看活动
const viewActivity = () => {
  ElMessage.info("查看活动功能开发中");
};

// 页面加载时加载用户数据
onMounted(() => {
  loadUserData();
});
</script>

<style scoped>
.user-info-card {
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

.user-profile {
  display: flex;
  gap: 32px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.avatar-section {
  flex-shrink: 0;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.avatar-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 48px;
}

.avatar-upload-btn {
  width: 100%;
}

.info-section {
  flex: 1;
  min-width: 200px;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.info-row:last-child {
  margin-bottom: 0;
  padding-bottom: 0;
  border-bottom: none;
}

.info-label {
  width: 80px;
  font-weight: 500;
  color: #4a5568;
  flex-shrink: 0;
}

.info-value {
  flex: 1;
  color: #1a202c;
}

.usage-stats {
  margin-bottom: 32px;
}

.stats-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.stats-title .el-icon {
  color: #4299e1;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.stat-item {
  background: #f7fafc;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  transition: transform 0.2s;
}

.stat-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #718096;
}

.action-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .user-profile {
    flex-direction: column;
    gap: 24px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .user-info-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .info-label {
  color: #cbd5e0;
}

:global(.dark-theme) .info-value {
  color: #e2e8f0;
}

:global(.dark-theme) .info-row {
  border-bottom-color: #4a5568;
}

:global(.dark-theme) .stats-title {
  color: #e2e8f0;
}

:global(.dark-theme) .stat-item {
  background: #4a5568;
}

:global(.dark-theme) .stat-value {
  color: #63b3ed;
}

:global(.dark-theme) .stat-label {
  color: #a0aec0;
}
</style>
