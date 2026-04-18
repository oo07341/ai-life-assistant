<template>
  <div class="calendar-preview">
    <div class="preview-header">
      <h3>
        <el-icon><Calendar /></el-icon> 日历预览
      </h3>
      <p class="preview-subtitle">预览生成的日程事件</p>
    </div>

    <div class="preview-content">
      <div class="empty-state" v-if="events.length === 0">
        <el-icon class="empty-icon"><Calendar /></el-icon>
        <p class="empty-text">暂无日程事件</p>
        <p class="empty-hint">生成的日程将显示在这里</p>
      </div>

      <div class="events-list" v-else>
        <div class="event-item" v-for="(event, index) in events" :key="index">
          <div class="event-time">
            <div class="event-date">{{ formatDate(event.start) }}</div>
            <div class="event-duration">
              {{ formatDuration(event.start, event.end) }}
            </div>
          </div>
          <div class="event-details">
            <div class="event-title">{{ event.title }}</div>
            <div class="event-location" v-if="event.location">
              <el-icon><Location /></el-icon> {{ event.location }}
            </div>
            <div class="event-description" v-if="event.description">
              {{ event.description }}
            </div>
          </div>
          <div class="event-actions">
            <el-button type="primary" size="small" @click="viewEvent(event)">
              <el-icon><View /></el-icon>
            </el-button>
            <el-button type="success" size="small" @click="exportEvent(event)">
              <el-icon><Download /></el-icon>
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <div class="preview-footer" v-if="events.length > 0">
      <el-button
        type="primary"
        @click="exportAll"
        :disabled="events.length === 0"
      >
        <el-icon><Download /></el-icon> 导出所有事件
      </el-button>
      <el-button @click="clearEvents" :disabled="events.length === 0">
        <el-icon><Delete /></el-icon> 清空预览
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps, watch } from "vue";
import {
  Calendar,
  Location,
  View,
  Download,
  Delete,
} from "@element-plus/icons-vue";

const props = defineProps({
  events: {
    type: Array,
    default: () => [],
  },
});

// 本地事件副本
const events = ref([...props.events]);

// 监听props变化
watch(
  () => props.events,
  (newEvents) => {
    events.value = [...newEvents];
  },
  { deep: true },
);

// 格式化日期
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
};

// 格式化持续时间
const formatDuration = (startString, endString) => {
  const start = new Date(startString);
  const end = new Date(endString);
  const duration = (end - start) / (1000 * 60 * 60); // 小时

  if (duration < 1) {
    return `${Math.round(duration * 60)}分钟`;
  } else if (duration < 24) {
    return `${Math.round(duration)}小时`;
  } else {
    return `${Math.round(duration / 24)}天`;
  }
};

// 查看事件
const viewEvent = (event) => {
  console.log("查看事件:", event);
  // 这里可以显示事件详情
};

// 导出单个事件
const exportEvent = (event) => {
  console.log("导出事件:", event);
  // 这里可以导出单个事件为ics文件
};

// 导出所有事件
const exportAll = () => {
  console.log("导出所有事件:", events.value);
  // 这里可以导出所有事件为ics文件
};

// 清空事件
const clearEvents = () => {
  events.value = [];
};
</script>

<style scoped>
.calendar-preview {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid #e2e8f0;
}

.preview-header {
  margin-bottom: 24px;
}

.preview-header h3 {
  font-size: 20px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.preview-header h3 .el-icon {
  color: #4299e1;
}

.preview-subtitle {
  font-size: 14px;
  color: #718096;
  margin: 0;
}

.preview-content {
  min-height: 200px;
  margin-bottom: 24px;
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

.events-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.event-item {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  transition: border-color 0.2s;
}

.event-item:hover {
  border-color: #4299e1;
}

.event-time {
  flex-shrink: 0;
  min-width: 120px;
}

.event-date {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 4px;
}

.event-duration {
  font-size: 12px;
  color: #718096;
  background: #f7fafc;
  padding: 4px 8px;
  border-radius: 4px;
  display: inline-block;
}

.event-details {
  flex: 1;
  min-width: 0;
}

.event-title {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
}

.event-location {
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.event-location .el-icon {
  color: #718096;
}

.event-description {
  font-size: 14px;
  color: #718096;
  line-height: 1.5;
}

.event-actions {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.preview-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .calendar-preview {
    padding: 16px;
  }

  .preview-header h3 {
    font-size: 18px;
  }

  .event-item {
    flex-direction: column;
    gap: 12px;
  }

  .event-time {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .event-actions {
    width: 100%;
    flex-direction: row;
    justify-content: flex-end;
  }

  .preview-footer {
    flex-direction: column;
  }

  .preview-footer .el-button {
    width: 100%;
  }
}
</style>
