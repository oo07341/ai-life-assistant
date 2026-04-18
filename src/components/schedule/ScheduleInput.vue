<template>
  <el-card class="input-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><ChatDotRound /></el-icon>
        <span>日程规划需求</span>
      </div>
    </template>

    <div class="input-section">
      <el-input
        v-model="scheduleQueryModel"
        type="textarea"
        :rows="3"
        placeholder="请输入您的日程需求，例如：我想吃披萨、需要规划购物时间等"
        resize="none"
        class="query-input"
      />

      <div class="extra-info">
        <div class="info-item">
          <span class="label">时间地点：</span>
          <el-input
            v-model="timeLocationModel"
            placeholder="可选，如：明天下午3点，中关村"
            size="small"
            class="time-location-input"
          />
        </div>
      </div>

      <div class="input-actions">
        <el-button
          type="primary"
          :loading="isGenerating"
          @click="$emit('generate')"
          :disabled="!scheduleQuery.trim()"
        >
          <el-icon><MagicStick /></el-icon>
          AI生成日程
        </el-button>

        <el-button @click="$emit('clear')">
          <el-icon><Delete /></el-icon>
          清空
        </el-button>
      </div>
    </div>

    <!-- 使用提示 -->
    <div class="usage-tips">
      <div class="tips-header">
        <el-icon><InfoFilled /></el-icon>
        <span>使用提示</span>
      </div>
      <ul class="tips-list">
        <li>描述您的日程需求，AI会为您规划最佳时间</li>
        <li>可以包含时间地点信息，生成更准确的日程</li>
        <li>生成的日历文件支持导入到手机日历</li>
        <li>支持多设备同步，随时随地查看日程</li>
      </ul>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps, defineEmits, computed } from "vue";
import {
  ChatDotRound,
  MagicStick,
  Delete,
  InfoFilled,
} from "@element-plus/icons-vue";

const props = defineProps({
  scheduleQuery: {
    type: String,
    default: "",
  },
  timeLocation: {
    type: String,
    default: "",
  },
  isGenerating: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits([
  "update:schedule-query",
  "update:time-location",
  "generate",
  "clear",
]);

// 使用计算属性来处理v-model
const scheduleQueryModel = computed({
  get: () => props.scheduleQuery,
  set: (value) => emit("update:schedule-query", value),
});

const timeLocationModel = computed({
  get: () => props.timeLocation,
  set: (value) => emit("update:time-location", value),
});
</script>

<style scoped>
.input-card {
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
  font-size: 18px;
  color: #667eea;
}

.input-section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.query-input :deep(.el-textarea__inner) {
  font-size: 14px;
  line-height: 1.5;
  border-color: #e2e8f0;
  transition: border-color 0.3s ease;
}

.query-input :deep(.el-textarea__inner):focus {
  border-color: #667eea;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.1);
}

.extra-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.info-item .label {
  font-size: 14px;
  color: #4a5568;
  min-width: 70px;
}

.time-location-input {
  flex: 1;
}

.input-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

/* 使用提示样式 */
.usage-tips {
  margin-top: 24px;
  padding: 16px;
  background: #f0fff4;
  border-radius: 8px;
  border-left: 4px solid #48bb78;
}

.tips-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
  font-weight: 600;
  color: #276749;
}

.tips-header .el-icon {
  color: #48bb78;
}

.tips-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tips-list li {
  padding: 4px 0;
  color: #276749;
  font-size: 13px;
  position: relative;
  padding-left: 16px;
}

.tips-list li:before {
  content: "•";
  position: absolute;
  left: 0;
  color: #48bb78;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .input-actions {
    flex-direction: column;
  }

  .input-actions .el-button {
    width: 100%;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .info-item .label {
    min-width: auto;
  }
}
</style>
