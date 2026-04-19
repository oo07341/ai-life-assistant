<template>
  <el-card class="input-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><ChatDotRound /></el-icon>
        <span>输入您的需求</span>
      </div>
    </template>

    <div class="input-section">
      <el-input
        v-model="searchQueryModel"
        type="textarea"
        :rows="3"
        placeholder="请输入您的需求，例如：我想吃披萨、我想吃辣的、我想吃便宜的..."
        resize="none"
        class="query-input"
      />

      <div class="input-actions">
        <el-button
          type="primary"
          :loading="isAnalyzing"
          @click="$emit('analyze')"
          :disabled="!searchQuery.trim()"
        >
          <el-icon><MagicStick /></el-icon>
          AI分析意图
        </el-button>

        <el-button @click="$emit('clear')">
          <el-icon><Delete /></el-icon>
          清空
        </el-button>
      </div>
    </div>

    <!-- AI分析结果 -->
    <div v-if="analysisResult" class="analysis-result">
      <div class="result-header">
        <el-icon><Lightning /></el-icon>
        <span>AI分析结果</span>
      </div>

      <div class="result-content">
        <div class="result-item">
          <span class="item-label">意图分析：</span>
          <span class="item-value">{{ analysisResult.intent }}</span>
        </div>
        <div class="result-item">
          <span class="item-label">商品类别：</span>
          <span class="item-value">{{ analysisResult.category }}</span>
        </div>
        <div class="result-item">
          <span class="item-label">预算范围：</span>
          <span class="item-value">{{ analysisResult.budget }}</span>
        </div>
        <div class="result-item">
          <span class="item-label">时间偏好：</span>
          <span class="item-value">{{ analysisResult.time_preference }}</span>
        </div>
        <div class="result-item">
          <span class="item-label">位置偏好：</span>
          <span class="item-value">{{
            analysisResult.location_preference
          }}</span>
        </div>
      </div>
    </div>

    <!-- 使用提示 -->
    <div class="usage-tips">
      <div class="tips-header">
        <el-icon><InfoFilled /></el-icon>
        <span>使用提示</span>
      </div>
      <ul class="tips-list">
        <li>尽量详细描述您的需求，AI能更准确分析</li>
        <li>可以包含预算、时间、地点等限制条件</li>
        <li>支持中文、英文混合输入</li>
        <li>分析结果仅供参考，请结合实际情况判断</li>
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
  Lightning,
  InfoFilled,
} from "@element-plus/icons-vue";

const props = defineProps({
  searchQuery: {
    type: String,
    default: "",
  },
  isAnalyzing: {
    type: Boolean,
    default: false,
  },
  analysisResult: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["update:search-query", "analyze", "clear"]);

// 使用计算属性来处理v-model
const searchQueryModel = computed({
  get: () => props.searchQuery,
  set: (value) => emit("update:search-query", value),
});

// 示例查询
const exampleQueries = [
  "我想买iPhone 15 Pro Max",
  "周末去露营需要什么装备",
  "给女朋友买生日礼物",
  "办公室用的咖啡机推荐",
  "性价比高的笔记本电脑",
];

// 处理输入变化
const handleInput = (event) => {
  emit("update:search-query", event.target.value);
};

// 触发分析
const triggerAnalyze = () => {
  if (props.searchQuery.trim()) {
    emit("analyze");
  }
};

// 清除输入
const triggerClear = () => {
  emit("clear");
};

// 使用示例查询
const useExample = (query) => {
  emit("update:search-query", query);
};
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

.input-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

/* AI分析结果样式 */
.analysis-result {
  margin-top: 24px;
  padding: 20px;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  font-weight: 600;
  color: #1a202c;
}

.result-header .el-icon {
  color: #f6ad55;
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.item-label {
  font-weight: 500;
  color: #4a5568;
  min-width: 80px;
}

.item-value {
  color: #1a202c;
  font-weight: 500;
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

  .result-item {
    flex-direction: column;
    gap: 4px;
  }

  .item-label {
    min-width: auto;
  }
}
</style>
