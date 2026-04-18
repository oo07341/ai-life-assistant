<template>
  <el-card class="history-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><Clock /></el-icon>
        <span>历史记录</span>
        <span v-if="history.length" class="history-count">
          ({{ history.length }}条)
        </span>
      </div>
    </template>

    <!-- 空状态 -->
    <div v-if="!history.length" class="empty-history">
      <el-icon><Document /></el-icon>
      <p>暂无历史记录</p>
    </div>

    <!-- 历史记录列表 -->
    <div v-else class="history-list">
      <div
        v-for="item in history"
        :key="item.id"
        class="history-item"
        @click="$emit('select-history', item)"
      >
        <div class="history-content">
          <div class="history-query">{{ item.query }}</div>
          <div class="history-meta">
            <span class="result-count">{{ item.result_count }}个结果</span>
            <span class="timestamp">{{ formatTime(item.timestamp) }}</span>
          </div>
        </div>
        <el-button
          type="text"
          size="small"
          @click.stop="$emit('select-history', item)"
        >
          <el-icon><View /></el-icon>
        </el-button>
      </div>
    </div>

    <!-- 操作按钮 -->
    <div v-if="history.length" class="history-actions">
      <el-button type="danger" size="small" @click="$emit('clear-history')">
        <el-icon><Delete /></el-icon>
        清空历史
      </el-button>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import { Clock, Document, View, Delete } from "@element-plus/icons-vue";

const props = defineProps({
  history: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["select-history", "clear-history"]);

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  // 如果是今天
  if (date.toDateString() === now.toDateString()) {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  // 如果是昨天
  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  if (date.toDateString() === yesterday.toDateString()) {
    return "昨天";
  }

  // 其他情况显示日期
  return date.toLocaleDateString();
};
</script>

<style scoped>
.history-card {
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

.history-count {
  font-size: 12px;
  color: #718096;
  margin-left: 4px;
}

.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  color: #a0aec0;
  text-align: center;
}

.empty-history .el-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-history p {
  font-size: 14px;
  margin: 0;
}

.history-list {
  max-height: 300px;
  overflow-y: auto;
}

.history-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-bottom: 1px solid #e2e8f0;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.history-item:last-child {
  border-bottom: none;
}

.history-item:hover {
  background-color: #f7fafc;
}

.history-content {
  flex: 1;
  min-width: 0;
}

.history-query {
  font-size: 14px;
  color: #1a202c;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #718096;
}

.result-count {
  color: #48bb78;
}

.timestamp {
  color: #a0aec0;
}

.history-actions {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
  text-align: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .history-item .el-button {
    align-self: flex-end;
  }
}
</style>
