<template>
  <div class="search-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">智能搜索</h1>
      <p class="page-subtitle">输入您的需求，AI帮您分析意图并提供解决方案</p>
    </div>

    <!-- 搜索区域 -->
    <div class="search-section">
      <div class="search-container">
        <!-- 搜索输入框 -->
        <div class="search-input-wrapper">
          <el-input
            v-model="searchQuery"
            placeholder="请输入您的需求，例如：我想吃披萨、帮我制定考研计划、明天下午3点开会提醒"
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

        <!-- 热门关键词 -->
        <div class="hot-keywords" v-if="hotKeywords.length > 0">
          <div class="hot-keywords-title">热门搜索：</div>
          <div class="keywords-list">
            <el-tag
              v-for="keyword in hotKeywords"
              :key="keyword"
              class="keyword-tag"
              @click="searchWithKeyword(keyword)"
            >
              {{ keyword }}
            </el-tag>
          </div>
        </div>

        <!-- 搜索提示 -->
        <div class="search-tips">
          <div class="tips-title">搜索示例：</div>
          <div class="tips-list">
            <div class="tip-item" @click="searchWithKeyword('我想吃麻辣烫')">
              <el-icon><ShoppingCart /></el-icon>
              <span>我想吃麻辣烫</span>
            </div>
            <div
              class="tip-item"
              @click="searchWithKeyword('帮我制定考研复习计划')"
            >
              <el-icon><Calendar /></el-icon>
              <span>帮我制定考研复习计划</span>
            </div>
            <div
              class="tip-item"
              @click="searchWithKeyword('明天下午3点开会提醒')"
            >
              <el-icon><Bell /></el-icon>
              <span>明天下午3点开会提醒</span>
            </div>
            <div
              class="tip-item"
              @click="searchWithKeyword('附近有什么好吃的')"
            >
              <el-icon><Location /></el-icon>
              <span>附近有什么好吃的</span>
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

      <!-- 意图分析结果 -->
      <div class="intent-section" v-if="!searching && searchResult">
        <el-card class="intent-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <el-icon><MagicStick /></el-icon>
              <span>AI意图分析</span>
            </div>
          </template>

          <div class="intent-content">
            <!-- 意图类型 -->
            <div class="intent-type">
              <el-tag
                :type="getIntentTagType(searchResult.intent.intent)"
                size="large"
              >
                {{ getIntentText(searchResult.intent.intent) }}
              </el-tag>
              <div class="intent-desc">
                {{ getIntentDescription(searchResult.intent.intent) }}
              </div>
            </div>

            <!-- 购物意图详情 -->
            <div
              class="intent-details"
              v-if="searchResult.intent.intent === 'shopping'"
            >
              <div class="detail-item">
                <span class="detail-label">商品关键词：</span>
                <div class="detail-value">
                  <el-tag
                    v-for="keyword in searchResult.intent.product_keywords"
                    :key="keyword"
                    type="info"
                    size="small"
                    class="keyword-tag"
                  >
                    {{ keyword }}
                  </el-tag>
                </div>
              </div>
              <div class="detail-item">
                <span class="detail-label">位置偏好：</span>
                <span class="detail-value">{{
                  getLocationText(searchResult.intent.location_hint)
                }}</span>
              </div>
            </div>

            <!-- 日程意图详情 -->
            <div
              class="intent-details"
              v-if="
                searchResult.intent.intent === 'schedule' &&
                searchResult.intent.schedule_info
              "
            >
              <div class="detail-item">
                <span class="detail-label">目标：</span>
                <span class="detail-value">{{
                  searchResult.intent.schedule_info.goal
                }}</span>
              </div>
              <div
                class="detail-item"
                v-if="searchResult.intent.schedule_info.target_date"
              >
                <span class="detail-label">目标日期：</span>
                <span class="detail-value">{{
                  searchResult.intent.schedule_info.target_date
                }}</span>
              </div>
              <div
                class="detail-item"
                v-if="searchResult.intent.schedule_info.daily_hours"
              >
                <span class="detail-label">每日可用时间：</span>
                <span class="detail-value"
                  >{{ searchResult.intent.schedule_info.daily_hours }}小时</span
                >
              </div>
              <div
                class="detail-item"
                v-if="searchResult.intent.schedule_info.subjects"
              >
                <span class="detail-label">科目/任务：</span>
                <div class="detail-value">
                  <el-tag
                    v-for="subject in searchResult.intent.schedule_info
                      .subjects"
                    :key="subject"
                    type="info"
                    size="small"
                    class="keyword-tag"
                  >
                    {{ subject }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 比价结果 -->
      <div
        class="deals-section"
        v-if="
          !searching &&
          searchResult &&
          searchResult.deals &&
          searchResult.deals.length > 0
        "
      >
        <div class="section-header">
          <h2 class="section-title">比价结果</h2>
          <div class="section-subtitle">
            为您找到{{ searchResult.deals.length }}个相关商品
          </div>
        </div>

        <div class="deals-grid">
          <el-card
            v-for="deal in searchResult.deals"
            :key="deal.id"
            class="deal-card"
            shadow="hover"
          >
            <div class="deal-content">
              <!-- 商品图片 -->
              <div class="deal-image">
                <img
                  :src="deal.image_url"
                  :alt="deal.name"
                  v-if="deal.image_url"
                />
                <div class="image-placeholder" v-else>
                  <el-icon><Picture /></el-icon>
                </div>
              </div>

              <!-- 商品信息 -->
              <div class="deal-info">
                <h3 class="deal-title">{{ deal.name }}</h3>
                <div class="deal-price">
                  <span class="price-currency">¥</span>
                  <span class="price-amount">{{ deal.price }}</span>
                </div>
                <div class="deal-rating">
                  <el-rate
                    v-model="deal.rating"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}分"
                    class="rating-stars"
                  />
                  <span class="rating-count"
                    >({{ deal.review_count }}条评价)</span
                  >
                </div>
                <div class="deal-platform">
                  <el-tag
                    :type="getPlatformTagType(deal.platform)"
                    size="small"
                  >
                    {{ deal.platform }}
                  </el-tag>
                </div>
                <div class="deal-actions">
                  <el-button
                    type="primary"
                    size="small"
                    @click="viewDealDetail(deal)"
                  >
                    查看详情
                  </el-button>
                  <el-button size="small" @click="addToCart(deal)">
                    加入购物车
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 无结果提示 -->
      <div
        class="no-results"
        v-if="
          !searching &&
          searchResult &&
          (!searchResult.deals || searchResult.deals.length === 0)
        "
      >
        <el-empty description="暂无相关商品" />
        <p class="no-results-hint">您可以尝试其他关键词或调整搜索条件</p>
      </div>

      <!-- 热门关键词结果 -->
      <div
        class="hot-keywords-section"
        v-if="!searching && searchResult && searchResult.hot_keywords"
      >
        <div class="section-header">
          <h2 class="section-title">热门搜索</h2>
          <div class="section-subtitle">大家都在搜</div>
        </div>
        <div class="keywords-grid">
          <el-card
            v-for="keyword in searchResult.hot_keywords.slice(0, 10)"
            :key="keyword"
            class="keyword-card"
            shadow="hover"
            @click="searchWithKeyword(keyword)"
          >
            <div class="keyword-content">
              <el-icon><Promotion /></el-icon>
              <span class="keyword-text">{{ keyword }}</span>
            </div>
          </el-card>
        </div>
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
          @click="searchWithKeyword(item.query)"
          closable
          @close="removeHistoryItem(item.id)"
        >
          {{ item.query }}
          <span class="history-time">{{ formatTime(item.timestamp) }}</span>
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import { ElMessage } from "element-plus";
import {
  Search,
  ShoppingCart,
  Calendar,
  Bell,
  Location,
  MagicStick,
  Picture,
  Promotion,
} from "@element-plus/icons-vue";
import { analyzeIntent, getHotKeywords } from "../services/api";

// 搜索状态
const searchQuery = ref("");
const searching = ref(false);
const showResults = ref(false);

// 搜索结果
const searchResult = ref(null);

// 热门关键词
const hotKeywords = ref([]);

// 搜索历史
const searchHistory = ref([]);

// 页面加载时获取热门关键词
onMounted(async () => {
  await loadHotKeywords();
  loadSearchHistory();
});

// 加载热门关键词
const loadHotKeywords = async () => {
  try {
    const keywords = await getHotKeywords();
    hotKeywords.value = keywords.slice(0, 8); // 只显示前8个
  } catch (error) {
    console.error("加载热门关键词失败:", error);
    // 使用默认关键词
    hotKeywords.value = [
      "披萨",
      "麻辣烫",
      "考研",
      "健身",
      "外卖",
      "学习计划",
      "会议提醒",
    ];
  }
};

// 加载搜索历史
const loadSearchHistory = () => {
  const history = localStorage.getItem("searchHistory");
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
  localStorage.setItem("searchHistory", JSON.stringify(searchHistory.value));
};

// 处理搜索
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning("请输入搜索内容");
    return;
  }

  searching.value = true;
  showResults.value = true;

  try {
    // 调用AI意图分析API
    const result = await analyzeIntent(searchQuery.value);
    searchResult.value = result;

    // 保存搜索历史
    saveSearchHistory(searchQuery.value);

    ElMessage.success("搜索成功");
  } catch (error) {
    console.error("搜索失败:", error);

    // 提供更详细的错误信息
    let errorMessage = "搜索失败，请稍后重试";
    if (error.message && error.message.includes("Failed to fetch")) {
      errorMessage = "无法连接到服务器，请检查后端服务是否运行";
    } else if (error.message && error.message.includes("NetworkError")) {
      errorMessage = "网络连接失败，请检查网络设置";
    } else if (error.message && error.message.includes("timeout")) {
      errorMessage = "请求超时，服务器响应过慢";
    }

    ElMessage.error(errorMessage);

    // 显示模拟结果用于演示，并告知用户这是演示数据
    searchResult.value = {
      intent: {
        intent: "shopping",
        product_keywords: ["披萨"],
        location_hint: "不限",
      },
      deals: [
        {
          id: 1,
          name: "必胜客超级至尊披萨",
          price: 89.9,
          rating: 4.5,
          review_count: 128,
          platform: "美团",
          image_url: "",
        },
        {
          id: 2,
          name: "达美乐经典意式肉酱披萨",
          price: 69.9,
          rating: 4.3,
          review_count: 96,
          platform: "饿了么",
          image_url: "",
        },
      ],
      hot_keywords: [
        "披萨",
        "麻辣烫",
        "汉堡",
        "奶茶",
        "烧烤",
        "火锅",
        "寿司",
        "炸鸡",
      ],
    };

    // 添加一个提示，告诉用户这是演示数据
    setTimeout(() => {
      ElMessage.info("当前显示的是演示数据，真实数据将在后端服务正常后显示");
    }, 500);
  } finally {
    searching.value = false;
  }
};

// 使用关键词搜索
const searchWithKeyword = (keyword) => {
  searchQuery.value = keyword;
  handleSearch();
};

// 获取意图标签类型
const getIntentTagType = (intent) => {
  switch (intent) {
    case "shopping":
      return "success";
    case "schedule":
      return "primary";
    case "general":
      return "info";
    default:
      return "info";
  }
};

// 获取意图文本
const getIntentText = (intent) => {
  switch (intent) {
    case "shopping":
      return "购物意图";
    case "schedule":
      return "日程意图";
    case "general":
      return "通用意图";
    default:
      return "未知意图";
  }
};

// 获取意图描述
const getIntentDescription = (intent) => {
  switch (intent) {
    case "shopping":
      return "AI识别到您想要购买商品，已为您提供比价结果";
    case "schedule":
      return "AI识别到您需要制定计划，可以为您生成详细日程安排";
    case "general":
      return "AI已理解您的需求，正在为您提供相关信息";
    default:
      return "AI正在分析您的需求";
  }
};

// 获取位置文本
const getLocationText = (location) => {
  switch (location) {
    case "校内":
      return "校内配送";
    case "校外":
      return "校外配送";
    case "不限":
      return "不限位置";
    default:
      return location || "不限位置";
  }
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
const viewDealDetail = (deal) => {
  ElMessage.info(`查看商品详情: ${deal.name}`);
  // 这里可以跳转到商品详情页面
};

// 加入购物车
const addToCart = (deal) => {
  ElMessage.success(`已添加 ${deal.name} 到购物车`);
  // 这里可以实现购物车逻辑
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

// 移除历史记录
const removeHistoryItem = (id) => {
  searchHistory.value = searchHistory.value.filter((item) => item.id !== id);
  localStorage.setItem("searchHistory", JSON.stringify(searchHistory.value));
};

// 清空历史记录
const clearHistory = () => {
  searchHistory.value = [];
  localStorage.removeItem("searchHistory");
  ElMessage.success("已清空搜索历史");
};
</script>

<style scoped>
.search-page {
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

/* 热门关键词 */
.hot-keywords {
  margin-bottom: 24px;
}

.hot-keywords-title {
  font-size: 14px;
  color: #718096;
  margin-bottom: 8px;
  font-weight: 500;
}

.keywords-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.keyword-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.keyword-tag:hover {
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
  cursor: pointer;
  transition: all 0.2s;
  color: #4a5568;
}

.tip-item:hover {
  background: #edf2f7;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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

/* 意图分析卡片 */
.intent-card {
  margin-bottom: 32px;
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

.intent-content {
  padding: 8px 0;
}

.intent-type {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 20px;
}

.intent-desc {
  color: #718096;
  font-size: 14px;
}

.intent-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  font-size: 14px;
  color: #718096;
  font-weight: 500;
}

.detail-value {
  color: #2d3748;
  font-weight: 500;
}

/* 比价结果 */
.deals-section {
  margin-bottom: 40px;
}

.section-header {
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.section-subtitle {
  font-size: 14px;
  color: #718096;
  margin: 0;
}

.deals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.deal-card {
  transition: all 0.3s;
}

.deal-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.deal-content {
  display: flex;
  gap: 16px;
}

.deal-image {
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

.deal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  color: #cbd5e0;
  font-size: 32px;
}

.deal-info {
  flex: 1;
  min-width: 0;
}

.deal-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.deal-price {
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

.deal-rating {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.rating-stars {
  --el-rate-icon-size: 16px;
}

.rating-count {
  font-size: 12px;
  color: #a0aec0;
}

.deal-platform {
  margin-bottom: 12px;
}

.deal-actions {
  display: flex;
  gap: 8px;
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

/* 热门关键词结果 */
.hot-keywords-section {
  margin-bottom: 40px;
}

.keywords-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 16px;
}

.keyword-card {
  cursor: pointer;
  transition: all 0.2s;
}

.keyword-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #4299e1;
}

.keyword-content {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
}

.keyword-content .el-icon {
  color: #f56565;
}

.keyword-text {
  font-size: 14px;
  color: #4a5568;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .search-page {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .tips-list {
    grid-template-columns: 1fr;
  }

  .deals-grid {
    grid-template-columns: 1fr;
  }

  .keywords-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .deal-content {
    flex-direction: column;
  }

  .deal-image {
    width: 100%;
    height: 150px;
  }
}

@media (max-width: 480px) {
  .keywords-grid {
    grid-template-columns: 1fr;
  }

  .intent-details {
    grid-template-columns: 1fr;
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

:global(.dark-theme) .tip-item:hover {
  background: #2d3748;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .detail-label {
  color: #a0aec0;
}

:global(.dark-theme) .detail-value {
  color: #e2e8f0;
}

:global(.dark-theme) .section-title {
  color: #e2e8f0;
}

:global(.dark-theme) .section-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .deal-title {
  color: #e2e8f0;
}

:global(.dark-theme) .deal-image {
  background: #4a5568;
}

:global(.dark-theme) .image-placeholder {
  color: #718096;
}

:global(.dark-theme) .keyword-text {
  color: #cbd5e0;
}

:global(.dark-theme) .history-section {
  border-top-color: #4a5568;
}

:global(.dark-theme) .history-time {
  color: #718096;
}
</style>
