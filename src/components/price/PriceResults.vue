<template>
  <el-card class="results-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><TrendCharts /></el-icon>
        <span>比价结果</span>
        <span v-if="priceResults.length" class="result-count">
          (共{{ priceResults.length }}个结果)
        </span>
      </div>
    </template>

    <!-- 加载状态 -->
    <div v-if="isAnalyzing" class="loading-state">
      <el-icon class="loading-icon"><Loading /></el-icon>
      <p>AI正在分析您的需求，请稍候...</p>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!priceResults.length" class="empty-state">
      <el-icon><Search /></el-icon>
      <p>暂无比价结果，请先输入需求并点击"AI分析意图"</p>
    </div>

    <!-- 比价结果列表 -->
    <div v-else class="results-list">
      <div
        v-for="product in priceResults"
        :key="product.id"
        class="product-card"
      >
        <div class="product-header">
          <div class="product-info">
            <h3 class="product-name">{{ product.name }}</h3>
            <div class="product-platform">
              <el-icon><Shop /></el-icon>
              <span>{{ product.platform }}</span>
            </div>
          </div>
          <div class="product-price">
            <div class="current-price">¥{{ product.price }}</div>
            <div class="original-price">¥{{ product.originalPrice }}</div>
            <div class="discount">
              {{ calculateDiscount(product.price, product.originalPrice) }}
            </div>
          </div>
        </div>

        <div class="product-details">
          <div class="detail-item">
            <el-icon><Clock /></el-icon>
            <span>{{ product.deliveryTime }}</span>
          </div>
          <div class="detail-item">
            <el-icon><Star /></el-icon>
            <span>{{ product.rating }}分</span>
          </div>
          <div class="detail-item">
            <el-icon><SoldOut /></el-icon>
            <span>销量{{ product.sales }}</span>
          </div>
        </div>

        <div class="product-actions">
          <el-button type="primary" size="small" @click="viewDetails(product)">
            <el-icon><View /></el-icon>
            查看详情
          </el-button>
          <el-button
            type="success"
            size="small"
            @click="addToSchedule(product)"
          >
            <el-icon><Calendar /></el-icon>
            添加到日程
          </el-button>
          <el-button type="warning" size="small" @click="openApp(product)">
            <el-icon><Link /></el-icon>
            打开App
          </el-button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { defineProps } from "vue";
import {
  TrendCharts,
  Loading,
  Search,
  Shop,
  Clock,
  Star,
  SoldOut,
  View,
  Calendar,
  Link,
} from "@element-plus/icons-vue";

const props = defineProps({
  priceResults: {
    type: Array,
    default: () => [],
  },
  isAnalyzing: {
    type: Boolean,
    default: false,
  },
});

// 计算折扣
const calculateDiscount = (price, originalPrice) => {
  if (!originalPrice || originalPrice <= price) return "";
  const discount = Math.round((1 - price / originalPrice) * 100);
  return `-${discount}%`;
};

// 查看详情
const viewDetails = (product) => {
  console.log("查看商品详情:", product);
  // 这里可以显示商品详情
};

// 添加到日程
const addToSchedule = (product) => {
  console.log("添加到日程:", product);
  // 这里可以触发添加到日程的事件
};

// 打开App
const openApp = (product) => {
  console.log("打开App:", product);
  if (product.urlScheme) {
    // 这里可以尝试打开App
    window.location.href = product.urlScheme;
  }
};
</script>

<style scoped>
.results-card {
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

.result-count {
  font-size: 14px;
  color: #718096;
  margin-left: 8px;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 40px 20px;
}

.loading-icon {
  font-size: 48px;
  color: #667eea;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.loading-state p {
  color: #4a5568;
  font-size: 16px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 40px 20px;
}

.empty-state .el-icon {
  font-size: 48px;
  color: #cbd5e0;
  margin-bottom: 16px;
}

.empty-state p {
  color: #718096;
  font-size: 16px;
}

/* 比价结果列表 */
.results-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.product-card {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 16px;
  transition: border-color 0.2s;
}

.product-card:hover {
  border-color: #667eea;
}

.product-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.4;
}

.product-platform {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #718096;
}

.product-platform .el-icon {
  font-size: 16px;
}

.product-price {
  text-align: right;
  min-width: 120px;
}

.current-price {
  font-size: 20px;
  font-weight: 700;
  color: #e53e3e;
  margin-bottom: 4px;
}

.original-price {
  font-size: 14px;
  color: #a0aec0;
  text-decoration: line-through;
  margin-bottom: 4px;
}

.discount {
  font-size: 12px;
  color: #48bb78;
  background: #f0fff4;
  padding: 2px 6px;
  border-radius: 4px;
  display: inline-block;
}

.product-details {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  color: #4a5568;
}

.detail-item .el-icon {
  color: #718096;
}

.product-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .product-header {
    flex-direction: column;
    gap: 12px;
  }

  .product-price {
    text-align: left;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .current-price {
    font-size: 18px;
  }

  .product-details {
    flex-direction: column;
    gap: 8px;
  }

  .product-actions {
    flex-direction: column;
  }

  .product-actions .el-button {
    width: 100%;
  }
}
</style>
