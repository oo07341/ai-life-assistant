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
              :icon="Search"
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
                <strong>搜索关键词：</strong>
                <div class="keywords">
                  <el-tag
                    v-for="(keyword, index) in intentResult.keywords"
                    :key="index"
                    type="primary"
                    class="keyword-tag"
                  >
                    {{ keyword }}
                  </el-tag>
                </div>
              </div>

              <div class="intent-item">
                <strong>推荐平台：</strong>
                <div class="platforms">
                  <el-tag
                    v-for="(platform, index) in intentResult.platforms"
                    :key="index"
                    type="success"
                    class="platform-tag"
                  >
                    {{ platform }}
                  </el-tag>
                </div>
              </div>

              <div class="intent-item">
                <strong>AI建议：</strong>
                <p class="advice">{{ intentResult.advice }}</p>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 比价结果 -->
    <div v-if="showResults" class="results-section">
      <div class="results-header">
        <h3>💰 比价结果（{{ products.length }}个商品）</h3>
        <div class="filter-controls">
          <el-select
            v-model="selectedPlatform"
            placeholder="筛选平台"
            size="small"
            @change="filterByPlatform"
          >
            <el-option label="全部平台" value=""></el-option>
            <el-option
              v-for="platform in uniquePlatforms"
              :key="platform"
              :label="platform"
              :value="platform"
            />
          </el-select>

          <el-select
            v-model="sortBy"
            placeholder="排序方式"
            size="small"
            @change="sortProducts"
          >
            <el-option label="价格从低到高" value="price-asc"></el-option>
            <el-option label="价格从高到低" value="price-desc"></el-option>
            <el-option label="评分从高到低" value="rating-desc"></el-option>
            <el-option label="销量从高到低" value="sales-desc"></el-option>
          </el-select>
        </div>
      </div>

      <!-- 商品卡片列表 -->
      <div class="products-grid">
        <el-card
          v-for="product in filteredProducts"
          :key="product.id"
          class="product-card"
          :class="{ 'best-value': isBestValue(product) }"
        >
          <template #header>
            <div class="product-header">
              <span class="product-image">{{ product.image }}</span>
              <div class="product-title">
                <h4>{{ product.name }}</h4>
                <div class="product-platform">
                  <el-tag
                    size="small"
                    :type="getPlatformType(product.platform)"
                  >
                    {{ product.platform }}
                  </el-tag>
                </div>
              </div>
            </div>
          </template>

          <div class="product-content">
            <!-- 价格信息 -->
            <div class="price-info">
              <div class="current-price">
                <span class="price-label">现价：</span>
                <span class="price-value">¥{{ product.price }}</span>
              </div>
              <div class="original-price">
                <span class="price-label">原价：</span>
                <span class="price-original">¥{{ product.originalPrice }}</span>
              </div>
              <div class="discount">
                <el-tag type="danger" size="small">
                  省¥{{ product.originalPrice - product.price }}
                </el-tag>
              </div>
            </div>

            <!-- 商品信息 -->
            <div class="product-details">
              <div class="detail-item">
                <el-icon><Star /></el-icon>
                <span>评分：{{ product.rating }}</span>
              </div>
              <div class="detail-item">
                <el-icon><Sold /></el-icon>
                <span>销量：{{ product.sales.toLocaleString() }}</span>
              </div>
              <div class="detail-item">
                <el-icon><Clock /></el-icon>
                <span>配送：{{ product.deliveryTime }}</span>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="product-actions">
              <el-button
                type="primary"
                size="small"
                @click="openApp(product)"
                class="buy-button"
              >
                <el-icon><ShoppingCart /></el-icon>
                去购买
              </el-button>

              <el-button
                type="success"
                size="small"
                @click="addToSchedule(product)"
                class="schedule-button"
              >
                <el-icon><Calendar /></el-icon>
                添加到日程
              </el-button>
            </div>
          </div>

          <!-- 最佳性价比标识 -->
          <div v-if="isBestValue(product)" class="best-value-badge">
            <el-icon><Trophy /></el-icon>
            <span>最佳性价比</span>
          </div>
        </el-card>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredProducts.length === 0" class="empty-state">
        <el-empty description="没有找到符合条件的商品">
          <el-button type="primary" @click="resetFilters">重置筛选</el-button>
        </el-empty>
      </div>
    </div>

    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-overlay">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p>正在搜索商品...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Search,
  Loading,
  MagicStick,
  Star,
  Sold,
  Clock,
  ShoppingCart,
  Calendar,
  Trophy,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

// 响应式数据
const searchQuery = ref("我想吃披萨");
const isAnalyzing = ref(false);
const isLoading = ref(false);
const showAIAnalysis = ref(false);
const showResults = ref(false);

// 意图分析结果
const intentResult = ref(null);

// 商品数据
const products = ref([]);
const filteredProducts = ref([]);
const selectedPlatform = ref("");
const sortBy = ref("price-asc");

// 模拟API调用 - 分析用户意图
const analyzeIntent = async (query) => {
  isAnalyzing.value = true;
  showAIAnalysis.value = true;

  try {
    // 调用Mock API
    const response = await fetch("http://localhost:3001/api/analyze-intent", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await response.json();

    if (data.success) {
      intentResult.value = data;
      ElMessage.success("AI已分析您的需求");

      // 自动搜索商品
      await searchProducts(data.keywords[0]);
    } else {
      ElMessage.error("AI分析失败，请重试");
    }
  } catch (error) {
    console.error("分析意图失败:", error);
    // 使用模拟数据
    intentResult.value = {
      success: true,
      intent: "比价购物",
      keywords: ["披萨"],
      platforms: ["美团", "饿了么"],
      advice: "披萨建议选择连锁品牌，品质有保障。",
      query: query,
    };
    ElMessage.warning("使用模拟数据演示");

    // 自动搜索商品
    await searchProducts("披萨");
  } finally {
    isAnalyzing.value = false;
  }
};

// 搜索商品
const searchProducts = async (keyword) => {
  isLoading.value = true;
  showResults.value = true;

  try {
    const response = await fetch(
      `http://localhost:3001/api/search-products?keyword=${encodeURIComponent(keyword)}`,
    );
    const data = await response.json();

    if (data.success) {
      products.value = data.products;
      filteredProducts.value = [...data.products];
      ElMessage.success(`找到${data.total}个商品`);
    } else {
      ElMessage.error("搜索商品失败");
    }
  } catch (error) {
    console.error("搜索商品失败:", error);
    // 使用模拟数据
    products.value = [
      {
        id: 1,
        name: "必胜客超级至尊披萨",
        price: 89,
        originalPrice: 108,
        platform: "美团",
        rating: 4.8,
        sales: 1250,
        deliveryTime: "30分钟",
        urlScheme: "imeituan://",
        image: "🍕",
      },
      {
        id: 2,
        name: "达美乐经典意式肉酱披萨",
        price: 79,
        originalPrice: 98,
        platform: "饿了么",
        rating: 4.7,
        sales: 980,
        deliveryTime: "35分钟",
        urlScheme: "eleme://",
        image: "🍕",
      },
    ];
    filteredProducts.value = [...products.value];
    ElMessage.warning("使用模拟数据演示");
  } finally {
    isLoading.value = false;
  }
};

// 处理搜索
const handleSearch = () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning("请输入搜索内容");
    return;
  }

  analyzeIntent(searchQuery.value);
};

// 计算唯一平台列表
const uniquePlatforms = computed(() => {
  const platforms = new Set();
  products.value.forEach((product) => platforms.add(product.platform));
  return Array.from(platforms);
});

// 根据平台筛选
const filterByPlatform = () => {
  if (!selectedPlatform.value) {
    filteredProducts.value = [...products.value];
  } else {
    filteredProducts.value = products.value.filter(
      (product) => product.platform === selectedPlatform.value,
    );
  }
  sortProducts();
};

// 排序商品
const sortProducts = () => {
  const sorted = [...filteredProducts.value];

  switch (sortBy.value) {
    case "price-asc":
      sorted.sort((a, b) => a.price - b.price);
      break;
    case "price-desc":
      sorted.sort((a, b) => b.price - a.price);
      break;
    case "rating-desc":
      sorted.sort((a, b) => b.rating - a.rating);
      break;
    case "sales-desc":
      sorted.sort((a, b) => b.sales - a.sales);
      break;
  }

  filteredProducts.value = sorted;
};

// 判断是否为最佳性价比
const isBestValue = (product) => {
  if (filteredProducts.value.length === 0) return false;

  // 简单算法：价格低且评分高
  const bestProduct = filteredProducts.value.reduce((best, current) => {
    const bestScore = best.rating / best.price;
    const currentScore = current.rating / current.price;
    return currentScore > bestScore ? current : best;
  });

  return product.id === bestProduct.id;
};

// 获取平台类型
const getPlatformType = (platform) => {
  const types = {
    美团: "success",
    饿了么: "warning",
    京东: "danger",
    淘宝: "danger",
    拼多多: "info",
  };
  return types[platform] || "info";
};

// 打开App
const openApp = (product) => {
  ElMessageBox.confirm(
    `即将打开${product.platform}App，如果未安装将跳转到下载页面`,
    "打开App",
    {
      confirmButtonText: "确定",
      cancelButtonText: "取消",
      type: "info",
    },
  )
    .then(() => {
      // 尝试打开App
      window.location.href = product.urlScheme;

      // 2秒后检查是否成功
      setTimeout(() => {
        if (!document.hidden) {
          // 打开失败，跳转到下载页面
          const downloadUrls = {
            美团: "https://apps.apple.com/cn/app/id423084029",
            饿了么: "https://apps.apple.com/cn/app/id507161324",
            京东: "https://apps.apple.com/cn/app/id414245413",
            淘宝: "https://apps.apple.com/cn/app/id387682726",
            拼多多: "https://apps.apple.com/cn/app/id1044283059",
          };

          const downloadUrl =
            downloadUrls[product.platform] ||
            "https://www.apple.com/app-store/";
          window.open(downloadUrl, "_blank");

          ElMessage.info("已为您打开下载页面");
        }
      }, 2000);
    })
    .catch(() => {
      // 用户取消
    });
};

// 添加到日程
const addToSchedule = (product) => {
  // 触发自定义事件，让父组件处理
  const event = new CustomEvent("add-to-schedule", {
    detail: {
      product: product,
      query: searchQuery.value,
    },
  });
  window.dispatchEvent(event);

  ElMessage.success("已准备添加到日程");
};

// 重置筛选
const resetFilters = () => {
  selectedPlatform.value = "";
  sortBy.value = "price-asc";
  filteredProducts.value = [...products.value];
};

// 初始化时自动搜索
onMounted(() => {
  // 延迟执行，确保UI已渲染
  setTimeout(() => {
    handleSearch();
  }, 500);
});
</script>

<style scoped>
.price-comparison {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-section {
  margin-bottom: 40px;
}

.search-section h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  margin-bottom: 24px;
  font-size: 16px;
}

.search-box {
  max-width: 600px;
  margin: 0 auto 30px;
}

.ai-analysis {
  margin-top: 30px;
}

.ai-thinking {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.thinking-icon {
  margin-right: 10px;
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

.keyword-tag,
.platform-tag {
  margin-right: 8px;
}

.advice {
  margin: 0;
  padding: 12px;
  background: #f0f9ff;
  border-radius: 6px;
  border-left: 4px solid #409eff;
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
  border-color: #ffd700;
  background: linear-gradient(135deg, #fff9e6 0%, #fff 100%);
}

.product-header {
  display: flex;
  align-items: center;
  gap: 16px;
}

.product-image {
  font-size: 40px;
}

.product-title h4 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
  line-height: 1.4;
}

.product-platform {
  margin-top: 4px;
}

.product-content {
  padding: 16px 0;
}

.price-info {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.current-price,
.original-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.price-label {
  color: #666;
  font-size: 14px;
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
}

.discount {
  text-align: right;
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

.product-actions {
  display: flex;
  gap: 12px;
  margin-top: 20px;
}

.buy-button,
.schedule-button {
  flex: 1;
}

.best-value-badge {
  position: absolute;
  top: -10px;
  right: -10px;
  background: linear-gradient(135deg, #ffd700 0%, #ffa500 100%);
  color: #333;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 4px;
  box-shadow: 0 2px 8px rgba(255, 165, 0, 0.3);
  z-index: 1;
}

.empty-state {
  margin: 60px 0;
  text-align: center;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-icon {
  font-size: 48px;
  color: #409eff;
  margin-bottom: 20px;
  animation: spin 1s linear infinite;
}

.loading-overlay p {
  font-size: 18px;
  color: #333;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .price-comparison {
    padding: 16px;
  }

  .search-section h2 {
    font-size: 24px;
  }

  .results-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .filter-controls {
    width: 100%;
    justify-content: space-between;
  }

  .products-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .product-card {
    margin-bottom: 16px;
  }
}

@media (max-width: 480px) {
  .search-box {
    margin-bottom: 20px;
  }

  .intent-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .intent-item strong {
    min-width: auto;
  }

  .product-actions {
    flex-direction: column;
  }

  .buy-button,
  .schedule-button {
    width: 100%;
  }
}
</style>
