<template>
  <div class="price-detail-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>
        <el-icon><ShoppingCart /></el-icon> AI智能比价
      </h1>
      <p class="page-subtitle">
        输入您的需求，AI为您分析意图并推荐最佳购买方案
      </p>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧：输入和AI分析 -->
      <div class="left-panel">
        <PriceInput
          :search-query="searchQuery"
          :is-analyzing="isAnalyzing"
          :analysis-result="analysisResult"
          @update:search-query="searchQuery = $event"
          @analyze="analyzeIntent"
          @clear="clearInput"
        />

        <PriceHistory
          :history="priceHistory"
          @select-history="loadHistory"
          @clear-history="clearHistory"
        />
      </div>

      <!-- 右侧：比价结果 -->
      <div class="right-panel">
        <PriceResults
          :analysis-result="analysisResult"
          :is-analyzing="isAnalyzing"
          :price-results="priceResults"
          @generate-schedule="generateSchedule"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { ShoppingCart } from "@element-plus/icons-vue";
import PriceInput from "@/components/price/PriceInput.vue";
import PriceResults from "@/components/price/PriceResults.vue";
import PriceHistory from "@/components/price/PriceHistory.vue";

// 响应式数据
const searchQuery = ref("");
const isAnalyzing = ref(false);
const analysisResult = ref(null);
const priceResults = ref([]);
const priceHistory = ref([]);

// 分析意图
const analyzeIntent = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning("请输入您的需求");
    return;
  }

  isAnalyzing.value = true;
  try {
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 模拟分析结果
    analysisResult.value = {
      intent: "购买披萨",
      category: "食品",
      budget: "50-100元",
      time_preference: "晚餐时间",
      location_preference: "附近3公里内",
    };

    // 模拟比价结果
    priceResults.value = [
      {
        id: 1,
        platform: "必胜客",
        name: "超级至尊披萨",
        price: 89,
        original_price: 99,
        discount: "9折",
        delivery_time: "30-45分钟",
        rating: 4.8,
        features: ["热销", "免配送费", "30分钟必达"],
      },
      {
        id: 2,
        platform: "达美乐",
        name: "经典意式披萨",
        price: 79,
        original_price: 89,
        discount: "8.8折",
        delivery_time: "25-40分钟",
        rating: 4.7,
        features: ["新品", "买一送一", "免配送费"],
      },
      {
        id: 3,
        platform: "棒约翰",
        name: "豪华海鲜披萨",
        price: 99,
        original_price: 119,
        discount: "8.3折",
        delivery_time: "35-50分钟",
        rating: 4.6,
        features: ["招牌", "海鲜特供", "会员专享"],
      },
    ];

    // 添加到历史记录
    addToHistory();

    ElMessage.success("AI分析完成！");
  } catch (error) {
    ElMessage.error("分析失败，请重试");
  } finally {
    isAnalyzing.value = false;
  }
};

// 清空输入
const clearInput = () => {
  searchQuery.value = "";
  analysisResult.value = null;
  priceResults.value = [];
};

// 添加到历史记录
const addToHistory = () => {
  const historyItem = {
    id: Date.now(),
    query: searchQuery.value,
    result_count: priceResults.value.length,
    timestamp: new Date().toISOString(),
    analysis: analysisResult.value,
  };

  priceHistory.value.unshift(historyItem);

  // 限制历史记录数量
  if (priceHistory.value.length > 10) {
    priceHistory.value = priceHistory.value.slice(0, 10);
  }

  // 保存到本地存储
  localStorage.setItem("priceHistory", JSON.stringify(priceHistory.value));
};

// 加载历史记录
const loadHistory = (historyItem) => {
  searchQuery.value = historyItem.query;
  analysisResult.value = historyItem.analysis;
  priceResults.value = historyItem.results || [];
};

// 清空历史记录
const clearHistory = () => {
  priceHistory.value = [];
  localStorage.removeItem("priceHistory");
};

// 生成日程
const generateSchedule = (product) => {
  ElMessage.info(`正在为${product.name}生成日程...`);
  // 这里可以跳转到日程页面或打开日程生成对话框
};

// 初始化
onMounted(() => {
  // 从本地存储加载历史记录
  const savedHistory = localStorage.getItem("priceHistory");
  if (savedHistory) {
    try {
      priceHistory.value = JSON.parse(savedHistory);
    } catch (error) {
      console.error("加载历史记录失败:", error);
    }
  }
});
</script>

<style scoped>
.price-detail-page {
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

/* 响应式设计 */
@media (max-width: 1200px) {
  .main-content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .price-detail-page {
    padding: 16px;
  }

  .page-header h1 {
    font-size: 28px;
  }

  .page-subtitle {
    font-size: 16px;
  }
}

@media (max-width: 480px) {
  .price-detail-page {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
</style>
