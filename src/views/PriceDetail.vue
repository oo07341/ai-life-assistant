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
import {
  analyzeIntent as apiAnalyzeIntent,
  searchProducts,
} from "@/services/api.js";
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
    // 调用AI接口分析意图
    const useAI = import.meta.env.VITE_USE_AI === "true";

    let intentResult = null;
    let intent = "通用购物";
    let category = "商品";
    let keywords = [searchQuery.value];
    let confidence = 0.85 + Math.random() * 0.1;

    if (useAI) {
      console.log("🔍 启用AI分析，调用统一的API服务...");
      try {
        // 使用统一的API服务层调用AI分析
        intentResult = await apiAnalyzeIntent(searchQuery.value);
        console.log("🤖 AI分析结果:", intentResult);

        // 解析AI返回的意图
        if (intentResult.intent) {
          const aiIntent = intentResult.intent.intent || intentResult.intent;
          console.log("🎯 AI意图:", aiIntent);
          console.log("📋 商品关键词:", intentResult.intent.product_keywords);

          // 根据AI意图设置参数
          if (aiIntent === "shopping" || aiIntent === "购物") {
            intent = "智能购物";
            category = "商品";
          } else if (aiIntent === "schedule" || aiIntent === "日程") {
            intent = "学习规划";
            category = "教育";
          } else if (aiIntent === "餐饮" || aiIntent === "饮食") {
            intent = "餐饮安排";
            category = "食品";
          }

          // 使用AI返回的关键词
          if (
            intentResult.intent.product_keywords &&
            intentResult.intent.product_keywords.length > 0
          ) {
            keywords = intentResult.intent.product_keywords;
          }

          confidence = 0.92; // AI分析的置信度更高
        }
      } catch (error) {
        console.error("❌ AI分析失败，使用备用方案:", error);
        // AI分析失败时使用备用方案
      }
    } else {
      console.log("🔧 AI分析未启用 (VITE_USE_AI=false)");
    }

    // 如果AI分析失败或未启用AI，使用增强的关键词匹配
    if (!intentResult) {
      const query = searchQuery.value.toLowerCase();

      if (query.includes("披萨") || query.includes("pizza")) {
        intent = "购买披萨";
        category = "食品";
        keywords = ["披萨", "外卖", "晚餐"];
      } else if (query.includes("汉堡") || query.includes("hamburger")) {
        intent = "购买汉堡";
        category = "快餐";
        keywords = ["汉堡", "快餐", "外卖"];
      } else if (
        query.includes("奶茶") ||
        query.includes("茶") ||
        query.includes("饮料")
      ) {
        intent = "购买饮品";
        category = "饮品";
        keywords = ["奶茶", "饮料", "饮品"];
      } else if (
        query.includes("学习") ||
        query.includes("复习") ||
        query.includes("考试")
      ) {
        intent = "学习规划";
        category = "教育";
        keywords = ["学习", "复习", "计划"];
      }
    }

    analysisResult.value = {
      intent: intent,
      category: category,
      keywords: keywords,
      confidence: confidence,
      advice: "根据您的需求，AI为您推荐以下商品",
    };

    // 调用价格搜索API获取真实的mock数据
    try {
      console.log("🔍 调用价格搜索API...");
      // 使用第一个关键词进行搜索
      const searchKeyword =
        keywords.length > 0 ? keywords[0] : searchQuery.value;
      const searchResults = await searchProducts(searchKeyword);
      console.log("💰 价格搜索结果:", searchResults);

      if (searchResults && searchResults.length > 0) {
        // 使用API返回的真实mock数据
        priceResults.value = searchResults.map((product, index) => ({
          id: index + 1,
          platform: product.platform,
          name:
            product.item_name ||
            product.name ||
            `${searchKeyword} ${product.platform}专享`,
          price: product.price,
          original_price: Math.round(
            product.price * (1.1 + Math.random() * 0.1),
          ), // 原价比现价高10-20%
          discount: `${Math.round((1 - product.price / (product.price * 1.15)) * 100)}折`,
          delivery_time: product.delivery_time || "30-45分钟",
          rating: 4.5 + Math.random() * 0.3 - 0.15, // 4.35-4.65的评分
          features: product.features || ["热销", "优质"],
        }));
      } else {
        // 如果API没有返回数据，使用模拟数据
        console.log("⚠️ API未返回数据，使用模拟数据");
        priceResults.value = generateMockPriceResults(
          intent,
          searchQuery.value,
        );
      }
    } catch (error) {
      console.error("❌ 价格搜索失败，使用模拟数据:", error);
      // 价格搜索失败时使用模拟数据
      priceResults.value = generateMockPriceResults(intent, searchQuery.value);
    }

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
    results: priceResults.value,
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

// 生成模拟价格结果
const generateMockPriceResults = (intent, query) => {
  const baseProducts = [
    {
      platform: "美团",
      basePrice: 50,
      deliveryTime: "30-45分钟",
      rating: 4.5,
      features: ["热销", "免配送费"],
    },
    {
      platform: "饿了么",
      basePrice: 55,
      deliveryTime: "25-40分钟",
      rating: 4.6,
      features: ["新品", "优惠券"],
    },
    {
      platform: "京东",
      basePrice: 60,
      deliveryTime: "次日达",
      rating: 4.7,
      features: ["正品保证", "快速配送"],
    },
  ];

  return baseProducts.map((base, index) => {
    const priceVariation = Math.random() * 20 - 10; // -10到+10的价格变化
    const price = Math.round(base.basePrice + priceVariation);
    const originalPrice = Math.round(price * (1.1 + Math.random() * 0.1)); // 原价比现价高10-20%
    const discount = Math.round((1 - price / originalPrice) * 100);

    let productName = `${query} ${base.platform}专享`;
    if (intent === "购买披萨") {
      productName = ["超级至尊披萨", "经典意式披萨", "豪华海鲜披萨"][index % 3];
    } else if (intent === "购买汉堡") {
      productName = ["经典牛肉汉堡", "鸡肉汉堡套餐", "豪华双层汉堡"][index % 3];
    } else if (intent === "购买饮品") {
      productName = ["招牌奶茶", "果茶特饮", "咖啡拿铁"][index % 3];
    } else if (intent === "学习规划") {
      productName = ["学习资料", "参考书籍", "文具套装"][index % 3];
    }

    return {
      id: index + 1,
      platform: base.platform,
      name: productName,
      price: price,
      original_price: originalPrice,
      discount: `${discount}折`,
      delivery_time: base.deliveryTime,
      rating: base.rating + Math.random() * 0.3 - 0.15, // 轻微评分变化
      features: base.features,
    };
  });
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
