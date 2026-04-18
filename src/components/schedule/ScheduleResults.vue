<template>
  <el-card class="results-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><Calendar /></el-icon>
        <span>日程结果</span>
        <span v-if="events.length" class="result-count">
          ({{ events.length }}个事件)
        </span>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="isGenerating" class="loading-state">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p>AI正在为您规划日程，请稍候...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!events.length" class="empty-state">
      <el-icon><Search /></el-icon>
      <p>暂无日程结果，请先输入需求并点击"AI生成日程"</p>
    </div>

    <!-- 日程结果 -->
    <div v-else class="results-content">
      <!-- 日程摘要 -->
      <div v-if="scheduleResult" class="schedule-summary">
        <div class="summary-header">
          <el-icon><Lightning /></el-icon>
          <span>AI规划摘要</span>
        </div>
        <div class="summary-content">
          <div class="summary-item">
            <span class="label">意图：</span>
            <span class="value">{{ scheduleResult.intent }}</span>
          </div>
          <div class="summary-item">
            <span class="label">时间建议：</span>
            <span class="value">{{
              scheduleResult.time_slots.join("、")
            }}</span>
          </div>
          <div class="summary-item">
            <span class="label">持续时间：</span>
            <span class="value">{{ scheduleResult.duration }}</span>
          </div>
          <div class="summary-item">
            <span class="label">地点：</span>
            <span class="value">{{ scheduleResult.location }}</span>
          </div>
          <div class="summary-item">
            <span class="label">备注：</span>
            <span class="value">{{ scheduleResult.notes }}</span>
          </div>
        </div>
      </div>

      <!-- 事件列表 -->
      <div class="events-list">
        <div v-for="event in events" :key="event.id" class="event-item">
          <div class="event-header">
            <h3 class="event-title">{{ event.title }}</h3>
            <div class="event-time">
              <el-icon><Clock /></el-icon>
              <span>{{ formatEventTime(event) }}</span>
            </div>
          </div>
          <div class="event-details">
            <div class="detail-item">
              <el-icon><Location /></el-icon>
              <span>{{ event.location }}</span>
            </div>
            <div class="detail-item">
              <el-icon><Document /></el-icon>
              <span>{{ event.description }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 下载按钮 -->
      <div class="download-section">
        <el-button type="primary" size="large" @click="$emit('download-ics')">
          <el-icon><Download /></el-icon>
          下载日历文件 (.ics)
        </el-button>
        <p class="download-tip">支持导入到手机日历、Outlook、Google日历等</p>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import {
  Calendar,
  Loading,
  Search,
  Lightning,
  Clock,
  Location,
  Document,
  Download,
} from "@element-plus/icons-vue";

const props = defineProps({
  scheduleResult: {
    type: Object,
    default: null,
  },
  isGenerating: {
    type: Boolean,
    default: false,
  },
  events: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["download-ics"]);

const formatEventTime = (event) => {
  const start = new Date(event.start);
  const end = new Date(event.end);

  const formatDate = (date) => {
    return date.toLocaleDateString("zh-CN", {
      month: "2-digit",
      day: "2-digit",
      weekday: "short",
    });
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString("zh-CN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  return `${formatDate(start)} ${formatTime(start)} - ${formatTime(end)}`;
};
</script>

<style scoped>
.results-card {
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

.result-count {
  font-size: 12px;
  color: #718096;
  margin-left: 4px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #4a5568;
  text-align: center;
}

.loading-icon {
  font-size: 48px;
  margin-bottom: 16px;
  color: #667eea;
  animation: spin 2s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #a0aec0;
  text-align: center;
}

.empty-state .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

/* 日程摘要样式 */
.schedule-summary {
  margin-bottom: 24px;
  padding: 20px;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-weight: 600;
  color: #1a202c;
}

.summary-header .el-icon {
  color: #f6ad55;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.summary-item .label {
  font-weight: 500;
  color: #4a5568;
  min-width: 60px;
}

.summary-item .value {
  color: #1a202c;
  font-weight: 500;
}

/* 事件列表样式 */
.events-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 24px;
}

.event-item {
  padding: 16px;
  background: white;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: box-shadow 0.3s ease;
}

.event-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.event-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.event-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin: 0;
}

.event-time {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #4a5568;
  font-size: 14px;
}

.event-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #4a5568;
  font-size: 14px;
}

.detail-item .el-icon {
  color: #718096;
}

/* 下载区域样式 */
.download-section {
  text-align: center;
  padding: 20px;
  background: #f0fff4;
  border-radius: 8px;
  border: 1px dashed #48bb78;
}

.download-tip {
  margin-top: 12px;
  color: #276749;
  font-size: 14px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .event-header {
    flex-direction: column;
    gap: 8px;
  }

  .summary-item {
    flex-direction: column;
    gap: 4px;
  }

  .summary-item .label {
    min-width: auto;
  }
}
</style>
