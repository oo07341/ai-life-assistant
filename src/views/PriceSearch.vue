<template>
  <div class="price-search-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">价格查询</h1>
      <p class="page-subtitle">输入商品关键词，获取多平台比价结果</p>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-container">
        <!-- 搜索输入框 -->
        <div class="search-input-wrapper">
          <el-input
            v-model="searchKeywords"
            placeholder="请输入商品关键词，例如：披萨、麻辣烫、奶茶、汉堡"
            size="large"
            @keyup.enter="handleSearch"
            class="search-input"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
            <template #append>
              <el-button
                type="primary"
                :icon="Search"
                @click="handleSearch"
                :loading="searching"
                class="search-button"
              >
                搜索
              </el-button>
            </template>
          </el-input>
        </div>

        <!-- 热门商品 -->
        <div class="hot-products" v-if="hotProducts.length > 0">
          <div class="hot-products-title">热门商品：</div>
          <div class="products-list">
            <el-tag
              v-for="product in hotProducts"
              :key="product"
              class="product-tag"
              @click="searchWithProduct(product)"
            >
              {{ product }}
            </el-tag>
          </div>
        </div>

        <!-- 搜索提示 -->
        <div class="search-tips">
          <div class="tips-title">搜索提示：</div>
          <div class="tips-list">
            <div class="tip-item">
              <el-icon><InfoFilled /></el-icon>
              <span>支持多个关键词，用空格分隔</span>
            </div>
            <div class="tip-item">
              <el-icon><InfoFilled /></el-icon>
              <span>系统会自动匹配相关商品</span>
            </div>
            <div class="tip-item">
              <el-icon><InfoFilled /></el-icon>
              <span>结果按价格从低到高排序</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 搜索结果区域 -->
    <div class="results-section" v-if="showResults">
      <!-- 加载状态 -->
      <div class="loading-section" v-if="searching">
        <el-skeleton :rows="5" animated />
      </div>

      <!-- 搜索结果 -->
      <div class="search-results" v-if="!searching && searchResults.length > 0">
        <div class="results-header">
          <h2 class="results-title">比价结果</h2>
          <div class="results-summary">
            为您找到 {{ searchResults.length }} 个相关商品
            <el-tag type="info" size="small" class="keywords-tag">
              关键词：{{ searchKeywords }}
            </el-tag>
          </div>
        </div>

        <!-- 筛选和排序 -->
        <div class="filters-section">
          <div class="filter-group">
            <span class="filter-label">排序：</span>
            <el-radio-group v-model="sortBy" @change="sortResults">
              <el-radio label="price">价格从低到高</el-radio>
              <el-radio label="rating">评分从高到低</el-radio>
              <el-radio label="reviews">评价数量</el-radio>
            </el-radio-group>
          </div>
          <div class="filter-group">
            <span class="filter-label">平台：</span>
            <el-checkbox-group
              v-model="selectedPlatforms"
              @change="filterResults"
            >
              <el-checkbox label="美团">美团</el-checkbox>
              <el-checkbox label="饿了么">饿了么</el-checkbox>
              <el-checkbox label="京东">京东</el-checkbox>
              <el-checkbox label="淘宝">淘宝</el-checkbox>
            </el-checkbox-group>
          </div>
        </div>

        <!-- 商品列表 -->
        <div class="products-grid">
          <el-card
            v-for="product in filteredResults"
            :key="product.id"
            class="product-card"
            shadow="hover"
          >
            <div class="product-content">
              <!-- 商品图片 -->
              <div class="product-image">
                <img
                  :src="product.image_url"
                  :alt="product.name"
                  v-if="product.image_url"
                />
                <div class="image-placeholder" v-else>
                  <el-icon><Picture /></el-icon>
                </div>
              </div>

              <!-- 商品信息 -->
              <div class="product-info">
                <h3 class="product-title">{{ product.name }}</h3>

                <!-- 价格信息 -->
                <div class="product-price">
                  <span class="price-currency">¥</span>
                  <span class="price-amount">{{ product.price }}</span>
                  <span class="price-unit" v-if="product.unit"
                    >/{{ product.unit }}</span
                  >
                </div>

                <!-- 评分信息 -->
                <div class="product-rating">
                  <el-rate
                    v-model="product.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}分"
                    class="rating-stars"
                  />
                  <span class="rating-count"
                    >({{ product.review_count }}条评价)</span
                  >
                </div>

                <!-- 平台信息 -->
                <div class="product-platform">
                  <el-tag
                    :type="getPlatformTagType(product.platform)"
                    size="small"
                  >
                    {{ product.platform }}
                  </el-tag>
                  <span class="platform-desc" v-if="product.platform_desc">
                    {{ product.platform_desc }}
                  </span>
                </div>

                <!-- 商品描述 -->
                <div class="product-desc" v-if="product.description">
                  {{ product.description }}
                </div>

                <!-- 操作按钮 -->
                <div class="product-actions">
                  <el-button
                    type="primary"
                    size="small"
                    @click="viewProductDetail(product)"
                  >
                    查看详情
                  </el-button>
                  <el-button size="small" @click="addToCart(product)">
                    加入购物车
                  </el-button>
                  <el-button
                    type="text"
                    size="small"
                    @click="comparePrice(product)"
                  >
                    比价
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>

        <!-- 分页 -->
        <div class="pagination-section" v-if="filteredResults.length > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 30, 50]"
            :total="filteredResults.length"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 无结果提示 -->
      <div class="no-results" v-if="!searching && searchResults.length === 0">
        <el-empty description="暂无相关商品" />
        <p class="no-results-hint">
          您可以尝试：
          <el-button type="text" @click="searchWithProduct('披萨')"
            >披萨</el-button
          >
          <el-button type="text" @click="searchWithProduct('麻辣烫')"
            >麻辣烫</el-button
          >
          <el-button type="text" @click="searchWithProduct('奶茶')"
            >奶茶</el-button
          >
          <el-button type="text" @click="searchWithProduct('汉堡')"
            >汉堡</el-button
          >
        </p>
      </div>
    </div>

    <!-- 搜索历史 -->
    <div class="history-section" v-if="searchHistory.length > 0">
      <div class="section-header">
        <h2 class="section-title">搜索历史</h2>
        <el-button type="text" @click="clearHistory" class="clear-history-btn">
          清空历史
        </el-button>
      </div>
      <div class="history-list">
        <el-tag
          v-for="item in searchHistory"
          :key="item.id"
          class="history-tag"
          @click="searchWithProduct(item.query)"
          closable
          @close="removeHistoryItem(item.id)"
        >
          {{ item.query }}
          <span class="history-time">{{ formatTime(item.timestamp) }}</span>
        </el-tag>
      </div>
    </div>

    <!-- 价格对比对话框 -->
    <el-dialog
      v-model="compareDialogVisible"
      :title="compareProduct ? `价格对比 - ${compareProduct.name}` : '价格对比'"
      width="800px"
    >
      <div v-if="compareProduct" class="compare-dialog">
        <div class="compare-header">
          <div class="compare-product">
            <div class="compare-image">
              <img
                :src="compareProduct.image_url"
                :alt="compareProduct.name"
                v-if="compareProduct.image_url"
              />
              <div class="image-placeholder" v-else>
                <el-icon><Picture /></el-icon>
              </div>
            </div>
            <div class="compare-info">
              <h3>{{ compareProduct.name }}</h3>
              <div class="compare-price">
                <span class="price-currency">¥</span>
                <span class="price-amount">{{ compareProduct.price }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="compare-table">
          <el-table :data="compareData" style="width: 100%">
            <el-table-column prop="platform" label="平台" width="120" />
            <el-table-column prop="price" label="价格" width="100">
              <template #default="scope">
                <span class="price-cell">¥{{ scope.row.price }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="rating" label="评分" width="100">
              <template #default="scope">
                <el-rate v-model="scope.row.rating" disabled size="small" />
              </template>
            </el-table-column>
            <el-table-column
              prop="delivery_time"
              label="配送时间"
              width="120"
            />
            <el-table-column prop="discount" label="优惠" width="120" />
            <el-table-column label="操作" width="120">
              <template #default="scope">
                <el-button
                  type="primary"
                  size="small"
                  @click="goToPlatform(scope.row)"
                >
                  前往购买
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { Search, InfoFilled, Picture } from "@element-plus/icons-vue";
import { priceAPI } from "@/services/api";

// 搜索状态
const searchKeywords = ref("");
const searching = ref(false);
const showResults = ref(false);

// 搜索结果
const searchResults = ref([]);
const filteredResults = ref([]);

// 热门商品
const hotProducts = ref([
  "披萨",
  "麻辣烫",
  "奶茶",
  "汉堡",
  "烧烤",
  "火锅",
  "寿司",
  "炸鸡",
  "咖啡",
  "蛋糕",
]);

// 筛选和排序
const sortBy = ref("price");
const selectedPlatforms = ref(["美团", "饿了么", "京东", "淘宝"]);
const currentPage = ref(1);
const pageSize = ref(10);

// 搜索历史
const searchHistory = ref([]);

// 价格对比对话框
const compareDialogVisible = ref(false);
const compareProduct = ref(null);
const compareData = ref([]);

// 页面加载时加载搜索历史
onMounted(() => {
  loadSearchHistory();
});

// 加载搜索历史
const loadSearchHistory = () => {
  const history = localStorage.getItem("priceSearchHistory");
  if (history) {
    try {
      searchHistory.value = JSON.parse(history);
    } catch (error) {
      searchHistory.value = [];
    }
  }
};

// 保存搜索历史
const saveSearchHistory = (query) => {
  const historyItem = {
    id: Date.now(),
    query,
    timestamp: new Date().toISOString(),
  };

  // 添加到历史列表开头
  searchHistory.value.unshift(historyItem);

  // 只保留最近20条记录
  if (searchHistory.value.length > 20) {
    searchHistory.value = searchHistory.value.slice(0, 20);
  }

  // 保存到localStorage
  localStorage.setItem(
    "priceSearchHistory",
    JSON.stringify(searchHistory.value),
  );
};

// 处理搜索
const handleSearch = async () => {
  if (!searchKeywords.value.trim()) {
    ElMessage.warning("请输入搜索关键词");
    return;
  }

  searching.value = true;
  showResults.value = true;

  try {
    // 分割关键词
    const keywords = searchKeywords.value.split(/\s+/).filter((k) => k.trim());

    // 调用价格查询API
    const results = await priceAPI.searchProducts(keywords);
    searchResults.value = results;
    filteredResults.value = [...results];

    // 默认按价格排序
    sortResults();

    // 保存搜索历史
    saveSearchHistory(searchKeywords.value);

    ElMessage.success(`找到 ${results.length} 个相关商品`);
  } catch (error) {
    console.error("搜索失败:", error);
    ElMessage.error("搜索失败，请稍后重试");

    // 显示模拟结果用于演示
    searchResults.value = generateMockResults();
    filteredResults.value = [...searchResults.value];
    sortResults();
  } finally {
    searching.value = false;
  }
};

// 使用商品搜索
const searchWithProduct = (product) => {
  searchKeywords.value = product;
  handleSearch();
};

// 生成模拟结果
const generateMockResults = () => {
  const products = [
    {
      id: 1,
      name: "必胜客超级至尊披萨",
      price: 89.9,
      rating: 4.5,
      review_count: 128,
      platform: "美团",
      platform_desc: "30分钟送达",
      description: "经典意式披萨，多种配料",
      unit: "份",
    },
    {
      id: 2,
      name: "达美乐经典意式肉酱披萨",
      price: 69.9,
      rating: 4.3,
      review_count: 96,
      platform: "饿了么",
      platform_desc: "45分钟送达",
      description: "浓郁肉酱，薄脆饼底",
      unit: "份",
    },
    {
      id: 3,
      name: "麦当劳巨无霸汉堡套餐",
      price: 39.9,
      rating: 4.2,
      review_count: 256,
      platform: "美团",
      platform_desc: "25分钟送达",
      description: "经典汉堡配薯条可乐",
      unit: "份",
    },
    {
      id: 4,
      name: "肯德基香辣鸡腿堡套餐",
      price: 42.9,
      rating: 4.4,
      review_count: 189,
      platform: "饿了么",
      platform_desc: "30分钟送达",
      description: "香辣鸡腿堡配薯条可乐",
      unit: "份",
    },
    {
      id: 5,
      name: "星巴克拿铁咖啡",
      price: 32.0,
      rating: 4.6,
      review_count: 342,
      platform: "美团",
      platform_desc: "35分钟送达",
      description: "经典意式浓缩咖啡",
      unit: "杯",
    },
    {
      id: 6,
      name: "瑞幸生椰拿铁",
      price: 19.9,
      rating: 4.7,
      review_count: 421,
      platform: "饿了么",
      platform_desc: "25分钟送达",
      description: "椰香浓郁，口感顺滑",
      unit: "杯",
    },
    {
      id: 7,
      name: "海底捞自热火锅",
      price: 45.0,
      rating: 4.8,
      review_count: 567,
      platform: "京东",
      platform_desc: "次日达",
      description: "麻辣牛油口味，方便快捷",
      unit: "盒",
    },
    {
      id: 8,
      name: "自嗨锅麻辣牛肉自热锅",
      price: 38.9,
      rating: 4.5,
      review_count: 289,
      platform: "淘宝",
      platform_desc: "3天送达",
      description: "麻辣鲜香，牛肉丰富",
      unit: "盒",
    },
  ];

  return products;
};

// 排序结果
const sortResults = () => {
  if (!filteredResults.value.length) return;

  const sorted = [...filteredResults.value];

  switch (sortBy.value) {
    case "price":
      sorted.sort((a, b) => a.price - b.price);
      break;
    case "rating":
      sorted.sort((a, b) => b.rating - a.rating);
      break;
    case "reviews":
      sorted.sort((a, b) => b.review_count - a.review_count);
      break;
  }

  filteredResults.value = sorted;
};

// 筛选结果
const filterResults = () => {
  if (!searchResults.value.length) return;

  if (selectedPlatforms.value.length === 0) {
    filteredResults.value = [];
    return;
  }

  const filtered = searchResults.value.filter((product) =>
    selectedPlatforms.value.includes(product.platform),
  );

  filteredResults.value = filtered;
  sortResults();
};

// 获取平台标签类型
const getPlatformTagType = (platform) => {
  switch (platform) {
    case "美团":
      return "success";
    case "饿了么":
      return "warning";
    case "京东":
      return "danger";
    case "淘宝":
      return "primary";
    default:
      return "info";
  }
};

// 查看商品详情
const viewProductDetail = (product) => {
  ElMessage.info(`查看商品详情: ${product.name}`);
  // 这里可以跳转到商品详情页面
};

// 加入购物车
const addToCart = (product) => {
  ElMessage.success(`已添加 ${product.name} 到购物车`);
  // 这里可以实现购物车逻辑
};

// 比价功能
const comparePrice = (product) => {
  compareProduct.value = product;

  // 生成比价数据
  compareData.value = [
    {
      platform: "美团",
      price: product.price,
      rating: product.rating,
      delivery_time: "30分钟",
      discount: "满30减5",
    },
    {
      platform: "饿了么",
      price: product.price * 0.95, // 模拟不同价格
      rating: product.rating - 0.1,
      delivery_time: "45分钟",
      discount: "新用户立减10元",
    },
    {
      platform: "京东",
      price: product.price * 1.1,
      rating: product.rating + 0.1,
      delivery_time: "次日达",
      discount: "包邮",
    },
    {
      platform: "淘宝",
      price: product.price * 0.9,
      rating: product.rating - 0.2,
      delivery_time: "3天",
      discount: "店铺优惠券",
    },
  ];

  compareDialogVisible.value = true;
};

// 前往平台购买
const goToPlatform = (platformData) => {
  ElMessage.info(`跳转到 ${platformData.platform} 购买页面`);
  // 这里可以实现跳转到外部链接
};

// 分页大小改变
const handleSizeChange = (size) => {
  pageSize.value = size;
  currentPage.value = 1;
};

// 当前页改变
const handleCurrentChange = (page) => {
  currentPage.value = page;
};

// 移除历史记录
const removeHistoryItem = (id) => {
  searchHistory.value = searchHistory.value.filter((item) => item.id !== id);
  localStorage.setItem(
    "priceSearchHistory",
    JSON.stringify(searchHistory.value),
  );
};

// 清空历史记录
const clearHistory = () => {
  searchHistory.value = [];
  localStorage.removeItem("priceSearchHistory");
  ElMessage.success("已清空搜索历史");
};

// 格式化时间
const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  const now = new Date();
  const diff = now - date;

  if (diff < 60000) {
    // 1分钟内
    return "刚刚";
  } else if (diff < 3600000) {
    // 1小时内
    return `${Math.floor(diff / 60000)}分钟前`;
  } else if (diff < 86400000) {
    // 1天内
    return `${Math.floor(diff / 3600000)}小时前`;
  } else {
    return `${Math.floor(diff / 86400000)}天前`;
  }
};
</script>

<style scoped>
.price-search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 32px;
  text-align: center;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

/* 搜索区域 */
.search-section {
  margin-bottom: 40px;
}

.search-container {
  max-width: 800px;
  margin: 0 auto;
}

.search-input-wrapper {
  margin-bottom: 24px;
}

.search-input {
  border-radius: 12px;
}

.search-input :deep(.el-input__inner) {
  border-radius: 12px 0 0 12px;
}

.search-input :deep(.el-input-group__append) {
  border-radius: 0 12px 12px 0;
}

.search-button {
  height: 40px;
  padding: 0 24px;
}

/* 热门商品 */
.hot-products {
  margin-bottom: 24px;
}

.hot-products-title {
  font-size: 14px;
  color: #718096;
  margin-bottom: 8px;
  font-weight: 500;
}

.products-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.product-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.product-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 搜索提示 */
.search-tips {
  margin-top: 24px;
}

.tips-title {
  font-size: 14px;
  color: #718096;
  margin-bottom: 12px;
  font-weight: 500;
}

.tips-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: #f7fafc;
  border-radius: 8px;
  color: #4a5568;
}

.tip-item .el-icon {
  color: #4299e1;
}

/* 搜索结果区域 */
.results-section {
  margin-top: 40px;
}

.loading-section {
  margin-bottom: 24px;
}

/* 结果头部 */
.results-header {
  margin-bottom: 24px;
}

.results-title {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.results-summary {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #718096;
  font-size: 14px;
}

.keywords-tag {
  margin-left: 8px;
}

/* 筛选区域 */
.filters-section {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f7fafc;
  border-radius: 8px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filter-label {
  font-size: 14px;
  color: #4a5568;
  font-weight: 500;
  white-space: nowrap;
}

/* 商品网格 */
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.product-card {
  transition: all 0.3s;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.product-content {
  display: flex;
  gap: 16px;
}

.product-image {
  flex-shrink: 0;
  width: 100px;
  height: 100px;
  border-radius: 8px;
  overflow: hidden;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  color: #cbd5e0;
  font-size: 32px;
}

.product-info {
  flex: 1;
  min-width: 0;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-price {
  display: flex;
  align-items: baseline;
  margin-bottom: 8px;
}

.price-currency {
  font-size: 14px;
  color: #f56565;
  font-weight: 600;
}

.price-amount {
  font-size: 24px;
  color: #f56565;
  font-weight: 700;
  margin-left: 2px;
}

.price-unit {
  font-size: 14px;
  color: #718096;
  margin-left: 4px;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.rating-stars {
  --el-rate-icon-size: 16px;
}

.rating-count {
  font-size: 12px;
  color: #a0aec0;
}

.product-platform {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.platform-desc {
  font-size: 12px;
  color: #718096;
}

.product-desc {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-actions {
  display: flex;
  gap: 8px;
}

/* 分页 */
.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

/* 无结果提示 */
.no-results {
  text-align: center;
  padding: 40px 0;
}

.no-results-hint {
  margin-top: 16px;
  color: #718096;
  font-size: 14px;
}

/* 搜索历史 */
.history-section {
  margin-top: 40px;
  padding-top: 40px;
  border-top: 1px solid #e2e8f0;
}

.history-section .section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clear-history-btn {
  font-size: 14px;
}

.history-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.history-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.history-tag:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.history-time {
  margin-left: 8px;
  font-size: 12px;
  color: #a0aec0;
}

/* 比价对话框 */
.compare-dialog {
  padding: 8px 0;
}

.compare-header {
  margin-bottom: 24px;
}

.compare-product {
  display: flex;
  align-items: center;
  gap: 16px;
}

.compare-image {
  flex-shrink: 0;
  width: 80px;
  height: 80px;
  border-radius: 8px;
  overflow: hidden;
  background: #f7fafc;
  display: flex;
  align-items: center;
  justify-content: center;
}

.compare-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.compare-info {
  flex: 1;
}

.compare-info h3 {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.compare-price {
  display: flex;
  align-items: baseline;
}

.price-cell {
  color: #f56565;
  font-weight: 600;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .price-search-page {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .filters-section {
    flex-direction: column;
    gap: 16px;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .product-content {
    flex-direction: column;
  }

  .product-image {
    width: 100%;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .filter-group {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .page-title {
  color: #e2e8f0;
}

:global(.dark-theme) .page-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .tip-item {
  background: #4a5568;
  color: #cbd5e0;
}

:global(.dark-theme) .results-title {
  color: #e2e8f0;
}

:global(.dark-theme) .results-summary {
  color: #a0aec0;
}

:global(.dark-theme) .filters-section {
  background: #4a5568;
}

:global(.dark-theme) .filter-label {
  color: #cbd5e0;
}

:global(.dark-theme) .product-title {
  color: #e2e8f0;
}

:global(.dark-theme) .product-image {
  background: #4a5568;
}

:global(.dark-theme) .image-placeholder {
  color: #718096;
}

:global(.dark-theme) .product-desc {
  color: #cbd5e0;
}

:global(.dark-theme) .no-results-hint {
  color: #a0aec0;
}

:global(.dark-theme) .history-section {
  border-top-color: #4a5568;
}

:global(.dark-theme) .history-time {
  color: #718096;
}

:global(.dark-theme) .compare-image {
  background: #4a5568;
}

:global(.dark-theme) .compare-info h3 {
  color: #e2e8f0;
}
</style>
