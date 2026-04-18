<template>
  <div class="schedule-history">
    <div class="history-header">
      <h3>
        <el-icon><Clock /></el-icon> 日程历史记录
      </h3>
      <p class="history-subtitle">查看您之前生成的日程规划</p>
    </div>

    <div class="history-content">
      <div class="empty-state" v-if="history.length === 0">
        <el-icon class="empty-icon"><Document /></el-icon>
        <p class="empty-text">暂无历史记录</p>
        <p class="empty-hint">生成的日程将显示在这里</p>
      </div>

      <div class="history-list" v-else>
        <div class="history-item" v-for="(item, index) in history" :key="index">
          <div class="item-header">
            <span class="item-title">{{ item.title }}</span>
            <span class="item-time">{{ formatTime(item.time) }}</span>
          </div>
          <div class="item-content">
            <p class="item-query">{{ item.query }}</p>
            <div class="item-actions">
              <el-button type="primary" size="small" @click="viewDetails(item)">
                <el-icon><View /></el-icon> 查看详情
              </el-button>
              <el-button type="success" size="small" @click="regenerate(item)">
                <el-icon><Refresh /></el-icon> 重新生成
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { Clock, Document, View, Refresh } from "@element-plus/icons-vue";

// 历史记录数据
const history = ref([]);

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString("zh-CN", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 查看详情
const viewDetails = (item) => {
  console.log("查看日程详情:", item);
  // 这里可以跳转到详情页面或显示模态框
};

// 重新生成
const regenerate = (item) => {
  console.log("重新生成日程:", item);
  // 这里可以触发重新生成日程的逻辑
};

// 模拟加载历史记录
onMounted(() => {
  // 从本地存储加载历史记录
  const savedHistory = localStorage.getItem("scheduleHistory");
  if (savedHistory) {
    try {
      history.value = JSON.parse(savedHistory);
    } catch (error) {
      console.error("解析历史记录失败:", error);
    }
  }
});
</script>

<style scoped>
.schedule-history {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.history-header {
  margin-bottom: 24px;
}

.history-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.history-header h3 .el-icon {
  color: #4299e1;
}

.history-subtitle {
  font-size: 14px;
  color: #718096;
  margin: 0;
}

.history-content {
  min-height: 200px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  color: #cbd5e0;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 18px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  color: #a0aec0;
  margin: 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  transition: border-color 0.2s;
}

.history-item:hover {
  border-color: #4299e1;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.item-title {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
}

.item-time {
  font-size: 12px;
  color: #718096;
  background: #f7fafc;
  padding: 4px 8px;
  border-radius: 4px;
}

.item-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item-query {
  font-size: 14px;
  color: #4a5568;
  margin: 0;
  line-height: 1.5;
}

.item-actions {
  display: flex;
  gap: 8px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .schedule-history {
    padding: 16px;
  }

  .history-header h3 {
    font-size: 18px;
  }

  .item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .item-actions {
    flex-direction: column;
  }

  .item-actions .el-button {
    width: 100%;
  }
}
</style>
