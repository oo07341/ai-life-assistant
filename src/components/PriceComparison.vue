<template>
  <div class="price-comparison">
    <!-- 搜索区域 -->
    <div class="search-section">
      <h2>🔍 AI智能比价</h2>
      <p class="subtitle">输入您的需求，AI帮您全网比价</p>

      <div class="search-box">
        <el-input
          v-model="searchQuery"
          placeholder="例如：我想吃披萨、想买手机、想喝咖啡..."
          size="large"
          @keyup.enter="handleSearch"
        >
          <template #append>
            <el-button
              type="primary"
              :loading="isAnalyzing"
              @click="handleSearch"
            >
              {{ isAnalyzing ? "AI分析中..." : "智能比价" }}
            </el-button>
          </template>
        </el-input>
      </div>

      <!-- AI思考过程 -->
      <div v-if="showAIAnalysis" class="ai-analysis">
        <div class="ai-thinking">
          <el-icon class="thinking-icon"><Loading /></el-icon>
          <span>AI正在分析您的需求...</span>
        </div>

        <div v-if="intentResult" class="ai-result">
          <el-card class="intent-card">
            <template #header>
              <div class="card-header">
                <el-icon><MagicStick /></el-icon>
                <span>AI分析结果</span>
              </div>
            </template>

            <div class="intent-content">
              <div class="intent-item">
                <strong>用户需求：</strong>
                <el-tag type="info">{{ intentResult.query }}</el-tag>
              </div>

              <div class="intent-item">
                <strong>分析意图：</strong>
                <el-tag type="success">{{ intentResult.intent }}</el-tag>
              </div>

              <div class="intent-item">
                <strong>推荐关键词：</strong>
                <div class="keywords">
                  <el-tag
                    v-for="keyword in intentResult.keywords"
                    :key="keyword"
                    type="primary"
                    size="small"
                  >
                    {{ keyword }}
                  </el-tag>
                </div>
              </div>

              <div class="intent-item">
                <strong>推荐平台：</strong>
                <div class="platforms">
                  <el-tag
                    v-for="platform in intentResult.platforms"
                    :key="platform"
                    type="warning"
                    size="small"
                  >
                    {{ platform }}
                  </el-tag>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 比价结果 -->
    <div v-if="showResults" class="results-section">
      <div class="results-header">
        <h3>💰 比价结果 ({{ filteredProducts.length }}个商品)</h3>
        <div class="filter-controls">
          <el-select
            v-model="selectedPlatform"
            placeholder="筛选平台"
            size="small"
            clearable
          >
            <el-option
              v-for="platform in platforms"
              :key="platform"
              :label="platform"
              :value="platform"
            />
          </el-select>

          <el-select v-model="sortBy" placeholder="排序方式" size="small">
            <el-option label="价格从低到高" value="price-asc" />
            <el-option label="价格从高到低" value="price-desc" />
            <el-option label="评分从高到低" value="rating-desc" />
          </el-select>

          <el-button type="text" @click="resetFilters">重置筛选</el-button>
        </div>
      </div>

      <div class="products-grid">
        <el-card
          v-for="product in filteredProducts"
          :key="product.id"
          class="product-card"
          :class="{ 'best-value': product.isBestValue }"
        >
          <template #header>
            <div class="card-header">
              <span class="product-name">{{ product.name }}</span>
              <div class="platform-tags">
                <el-tag :type="getPlatformType(product.platform)" size="small">
                  {{ product.platform }}
                </el-tag>
                <el-tag v-if="product.isBestValue" type="danger" size="small">
                  最佳性价比
                </el-tag>
              </div>
            </div>
          </template>

          <div class="product-content">
            <div class="price-info">
              <div class="price-value">¥{{ product.price }}</div>
              <div v-if="product.originalPrice" class="price-original">
                原价: ¥{{ product.originalPrice }}
              </div>
              <div v-if="product.discount" class="discount">
                <el-tag type="success" size="small">
                  {{ product.discount }}折
                </el-tag>
              </div>
            </div>

            <div class="product-details">
              <div class="detail-item">
                <el-icon><Location /></el-icon>
                <span>{{ product.shopName }}</span>
              </div>
              <div class="detail-item">
                <el-icon><Star /></el-icon>
                <span>评分: {{ product.rating }}/5.0</span>
              </div>
              <div class="detail-item">
                <el-icon><Timer /></el-icon>
                <span>预计送达: {{ product.deliveryTime }}</span>
              </div>
            </div>

            <div class="product-description">
              {{ product.description }}
            </div>

            <div class="product-actions">
              <el-button
                type="primary"
                class="buy-button"
                @click="handleBuy(product)"
              >
                一键购买
              </el-button>
              <el-button
                type="success"
                class="schedule-button"
                @click="handleAddToSchedule(product)"
              >
                添加到日程
              </el-button>
            </div>
          </div>
        </el-card>
      </div>

      <div v-if="filteredProducts.length === 0" class="no-results">
        <p>没有找到符合条件的商品，请调整筛选条件</p>
      </div>
    </div>

    <!-- 购买建议 -->
    <div
      v-if="showResults && filteredProducts.length > 0"
      class="advice-section"
    >
      <el-card class="advice-card">
        <template #header>
          <div class="card-header">
            <el-icon><InfoFilled /></el-icon>
            <span>AI购买建议</span>
          </div>
        </template>
        <p class="advice">
          {{ getAdvice() }}
        </p>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  MagicStick,
  Loading,
  Location,
  Star,
  Timer,
  InfoFilled,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

// 响应式数据
const searchQuery = ref("");
const isAnalyzing = ref(false);
const showAIAnalysis = ref(false);
const showResults = ref(false);
const intentResult = ref(null);
const selectedPlatform = ref("");
const sortBy = ref("price-asc");

// 模拟数据
const products = ref([
  {
    id: 1,
    name: "必胜客超级至尊披萨",
    platform: "美团",
    price: 89.9,
    originalPrice: 109.9,
    discount: 8.2,
    shopName: "必胜客中关村店",
    rating: 4.8,
    deliveryTime: "30分钟",
    description: "12寸超级至尊披萨，适合3-4人分享，含芝士加倍",
    isBestValue: true,
  },
  {
    id: 2,
    name: "必胜客超级至尊披萨",
    platform: "饿了么",
    price: 85.9,
    originalPrice: 109.9,
    discount: 7.8,
    shopName: "必胜客中关村店",
    rating: 4.7,
    deliveryTime: "35分钟",
    description: "12寸超级至尊披萨，满减优惠，配送费减免",
    isBestValue: false,
  },
  {
    id: 3,
    name: "达美乐经典披萨",
    platform: "达美乐APP",
    price: 79.9,
    originalPrice: 99.9,
    discount: 8.0,
    shopName: "达美乐披萨",
    rating: 4.9,
    deliveryTime: "30分钟",
    description: "经典口味披萨，30分钟送达保证，热销产品",
    isBestValue: false,
  },
  {
    id: 4,
    name: "棒约翰特色披萨",
    platform: "美团",
    price: 92.9,
    originalPrice: 119.9,
    discount: 7.7,
    shopName: "棒约翰披萨",
    rating: 4.6,
    deliveryTime: "40分钟",
    description: "特色风味披萨，使用进口奶酪，口感浓郁",
    isBestValue: false,
  },
  {
    id: 5,
    name: "尊宝披萨套餐",
    platform: "饿了么",
    price: 75.9,
    originalPrice: 95.9,
    discount: 7.9,
    shopName: "尊宝披萨",
    rating: 4.5,
    deliveryTime: "45分钟",
    description: "披萨+小吃+饮料套餐，性价比高",
    isBestValue: false,
  },
]);

// 计算属性
const platforms = computed(() => {
  const uniquePlatforms = new Set();
  products.value.forEach((product) => {
    uniquePlatforms.add(product.platform);
  });
  return Array.from(uniquePlatforms);
});

const filteredProducts = computed(() => {
  let filtered = [...products.value];

  // 平台筛选
  if (selectedPlatform.value) {
    filtered = filtered.filter(
      (product) => product.platform === selectedPlatform.value,
    );
  }

  // 排序
  if (sortBy.value === "price-asc") {
    filtered.sort((a, b) => a.price - b.price);
  } else if (sortBy.value === "price-desc") {
    filtered.sort((a, b) => b.price - a.price);
  } else if (sortBy.value === "rating-desc") {
    filtered.sort((a, b) => b.rating - a.rating);
  }

  return filtered;
});

// 方法
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning("请输入搜索内容");
    return;
  }

  isAnalyzing.value = true;
  showAIAnalysis.value = true;

  try {
    // 调用真实AI分析API
    const response = await fetch("http://localhost:3001/api/analyze-intent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: searchQuery.value,
      }),
    });

    if (!response.ok) {
      throw new Error(`API请求失败: ${response.status}`);
    }

    const data = await response.json();

    if (data.success) {
      intentResult.value = {
        query: data.query,
        intent: data.intent,
        keywords: data.keywords,
        platforms: data.platforms,
        advice: data.advice,
        source: data.source || "mock_data",
      };

      // 根据AI分析结果搜索商品
      await searchProducts(data.keywords[0] || searchQuery.value);

      ElMessage.success(
        `AI分析完成 (${data.source === "deepseek_ai" ? "DeepSeek AI" : "Mock数据"})`,
      );
    } else {
      throw new Error(data.error || "AI分析失败");
    }
  } catch (error) {
    console.error("AI分析错误:", error);

    // 降级到模拟AI分析
    intentResult.value = {
      query: searchQuery.value,
      intent: "通用购物",
      keywords: [searchQuery.value],
      platforms: ["京东", "淘宝", "拼多多"],
      advice: "根据您的需求，我们推荐选择信誉好的平台购买。",
      source: "fallback",
    };

    // 使用模拟数据
    await searchProducts(searchQuery.value);

    ElMessage.warning("AI分析失败，使用备用方案");
  } finally {
    isAnalyzing.value = false;
    showResults.value = true;
  }
};

// 搜索商品
const searchProducts = async (keyword) => {
  try {
    const response = await fetch(
      `http://localhost:3001/api/search-products?keyword=${encodeURIComponent(keyword)}`,
    );

    if (!response.ok) {
      throw new Error(`商品搜索失败: ${response.status}`);
    }

    const data = await response.json();

    if (data.success && data.products.length > 0) {
      // 转换API返回的商品格式为组件需要的格式
      products.value = data.products.map((product, index) => ({
        id: product.id || index + 1,
        name: product.name,
        platform: product.platform,
        price: product.price,
        originalPrice: product.originalPrice || product.price * 1.2,
        discount: product.originalPrice
          ? Math.round((1 - product.price / product.originalPrice) * 100)
          : 20,
        shopName: product.shopName || `${product.platform}官方店`,
        rating: product.rating || 4.5,
        deliveryTime: product.deliveryTime || "1-3天",
        description:
          product.description || `来自${product.platform}的${product.name}`,
        isBestValue: index === 0, // 第一个商品作为最佳推荐
      }));
    } else {
      // 如果没有搜索结果，使用模拟数据
      useMockProducts(keyword);
    }
  } catch (error) {
    console.error("商品搜索错误:", error);
    // 降级到模拟数据
    useMockProducts(keyword);
  }
};

// 使用模拟商品数据（降级方案）
const useMockProducts = (keyword) => {
  const mockProducts = [
    {
      id: 1,
      name: `${keyword} 商品A`,
      platform: "京东",
      price: 99,
      originalPrice: 129,
      discount: 23,
      shopName: "京东官方店",
      rating: 4.5,
      deliveryTime: "次日达",
      description: `来自京东的${keyword}商品，品质保证`,
      isBestValue: true,
    },
    {
      id: 2,
      name: `${keyword} 商品B`,
      platform: "淘宝",
      price: 149,
      originalPrice: 199,
      discount: 25,
      shopName: "淘宝旗舰店",
      rating: 4.3,
      deliveryTime: "3天",
      description: `来自淘宝的${keyword}商品，价格优惠`,
      isBestValue: false,
    },
    {
      id: 3,
      name: `${keyword} 商品C`,
      platform: "拼多多",
      price: 79,
      originalPrice: 99,
      discount: 20,
      shopName: "拼多多品牌店",
      rating: 4.2,
      deliveryTime: "4天",
      description: `来自拼多多的${keyword}商品，性价比高`,
      isBestValue: false,
    },
  ];

  products.value = mockProducts;
};

const handleBuy = (product) => {
  ElMessage.success(`正在跳转到${product.platform}购买${product.name}`);

  // 模拟跳转
  setTimeout(() => {
    window.open(`https://${product.platform}.com`, "_blank");
  }, 1000);
};

const handleAddToSchedule = (product) => {
  const event = new CustomEvent("add-to-schedule", {
    detail: {
      product: product,
      query: searchQuery.value,
    },
  });
  window.dispatchEvent(event);

  ElMessage.success("已准备添加到日程");
};

const getPlatformType = (platform) => {
  const types = {
    美团: "success",
    饿了么: "warning",
    达美乐APP: "danger",
  };
  return types[platform] || "info";
};

const getAdvice = () => {
  const bestProduct = products.value.find((p) => p.isBestValue);
  if (bestProduct) {
    return `推荐选择${bestProduct.platform}的"${bestProduct.name}"，价格¥${bestProduct.price}，评分${bestProduct.rating}，性价比最高。`;
  }
  return "根据您的需求，我们推荐选择评分较高且价格合理的商品。";
};

const resetFilters = () => {
  selectedPlatform.value = "";
  sortBy.value = "price-asc";
};

// 初始化时自动搜索示例
onMounted(() => {
  searchQuery.value = "我想吃披萨";
});
</script>

<style scoped>
.price-comparison {
  padding: 20px;
}

.search-section h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  margin-bottom: 24px;
}

.search-box {
  margin-bottom: 30px;
}

.ai-analysis {
  margin: 30px 0;
}

.ai-thinking {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f0f9ff;
  border-radius: 8px;
  margin-bottom: 20px;
}

.thinking-icon {
  color: #409eff;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.intent-card {
  margin-top: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.intent-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.intent-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.intent-item strong {
  min-width: 100px;
  color: #333;
}

.keywords,
.platforms {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.results-section {
  margin-top: 40px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.results-header h3 {
  font-size: 22px;
  color: #333;
  margin: 0;
}

.filter-controls {
  display: flex;
  gap: 12px;
  align-items: center;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 20px;
}

.product-card {
  position: relative;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  border: 1px solid #e4e7ed;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.product-card.best-value {
  border-color: #f56c6c;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.product-name {
  font-weight: bold;
  font-size: 16px;
  color: #333;
  flex: 1;
}

.platform-tags {
  display: flex;
  gap: 8px;
}

.price-info {
  margin-bottom: 16px;
}

.price-value {
  font-size: 24px;
  font-weight: bold;
  color: #f56c6c;
}

.price-original {
  font-size: 14px;
  color: #999;
  text-decoration: line-through;
  margin-top: 4px;
}

.discount {
  margin-top: 8px;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.detail-item .el-icon {
  color: #409eff;
}

.product-description {
  color: #666;
  font-size: 14px;
  line-height: 1.5;
  margin-bottom: 20px;
}

.product-actions {
  display: flex;
  gap: 12px;
}

.buy-button,
.schedule-button {
  flex: 1;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #999;
  font-size: 16px;
}

.advice-section {
  margin-top: 30px;
}

.advice-card {
  background: #f0f9ff;
  border-color: #409eff;
}

.advice {
  margin: 0;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 6px;
  border-left: 4px solid #409eff;
  color: #333;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .filter-controls {
    width: 100%;
    flex-wrap: wrap;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .intent-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .intent-item strong {
    min-width: auto;
  }
}
</style>
