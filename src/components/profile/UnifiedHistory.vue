<template>
  <el-card class="unified-history-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><Clock /></el-icon>
        <span>历史记录</span>
        <span class="history-count" v-if="totalItems > 0">
          ({{ totalItems }}条记录)
        </span>
      </div>
    </template>

    <!-- 筛选和搜索 -->
    <div class="history-controls">
      <div class="filter-section">
        <el-select
          v-model="filter.type"
          placeholder="筛选类型"
          size="small"
          style="width: 120px"
        >
          <el-option label="全部类型" value="all" />
          <el-option label="比价记录" value="price" />
          <el-option label="日程记录" value="schedule" />
        </el-select>

        <el-select
          v-model="filter.timeRange"
          placeholder="时间范围"
          size="small"
          style="width: 120px"
        >
          <el-option label="全部时间" value="all" />
          <el-option label="今天" value="today" />
          <el-option label="最近7天" value="week" />
          <el-option label="最近30天" value="month" />
        </el-select>
      </div>

      <div class="search-section">
        <el-input
          v-model="searchQuery"
          placeholder="搜索历史记录..."
          size="small"
          style="width: 200px"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="filteredHistory.length === 0" class="empty-history">
      <el-icon class="empty-icon"><Document /></el-icon>
      <p class="empty-text">暂无历史记录</p>
      <p class="empty-hint">开始使用比价或日程功能后，记录将显示在这里</p>
    </div>

    <!-- 历史记录列表（使用分页数据） -->
    <div v-else class="history-list">
      <div
        v-for="item in paginatedHistory"
        :key="item.id"
        class="history-item"
        :class="item.type"
      >
        <div class="item-icon">
          <el-icon v-if="item.type === 'price'"><ShoppingCart /></el-icon>
          <el-icon v-if="item.type === 'schedule'"><Calendar /></el-icon>
        </div>

        <div class="item-content">
          <div class="item-header">
            <span class="item-title">{{ item.title }}</span>
            <span class="item-time">{{ formatTime(item.timestamp) }}</span>
          </div>

          <div class="item-details">
            <p class="item-query">{{ item.query }}</p>

            <div class="item-meta">
              <el-tag v-if="item.type === 'price'" type="success" size="small">
                {{ item.resultCount || 0 }}个结果
              </el-tag>
              <el-tag
                v-if="item.type === 'schedule'"
                type="primary"
                size="small"
              >
                {{ item.eventCount || 0 }}个事件
              </el-tag>
              <span class="item-platform" v-if="item.platform">
                {{ item.platform }}
              </span>
            </div>
          </div>
        </div>

        <div class="item-actions">
          <el-button type="primary" size="small" @click="viewItem(item)">
            <el-icon><View /></el-icon>
            查看
          </el-button>
          <el-button type="danger" size="small" plain @click="deleteItem(item)">
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
      </div>
    </div>

    <!-- 批量操作 -->
    <div v-if="filteredHistory.length > 0" class="batch-actions">
      <el-checkbox v-model="selectAll" @change="toggleSelectAll">
        全选
      </el-checkbox>

      <div class="batch-buttons">
        <el-button
          type="danger"
          size="small"
          :disabled="selectedItems.length === 0"
          @click="deleteSelected"
        >
          <el-icon><Delete /></el-icon>
          删除选中 ({{ selectedItems.length }})
        </el-button>

        <el-button type="info" size="small" @click="clearAllHistory">
          <el-icon><DeleteFilled /></el-icon>
          清空全部
        </el-button>
      </div>
    </div>

    <!-- 分页 -->
    <div v-if="filteredHistory.length > 0" class="history-pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="filteredHistory.length"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        small
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue";
import {
  Clock,
  Document,
  Search,
  ShoppingCart,
  Calendar,
  View,
  Delete,
  DeleteFilled,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

// 历史记录数据
const history = ref([]);
const selectedItems = ref([]);
const selectAll = ref(false);

// 筛选和搜索
const filter = ref({
  type: "all",
  timeRange: "all",
});
const searchQuery = ref("");

// 分页
const currentPage = ref(1);
const pageSize = ref(10);

// 计算属性
const totalItems = computed(() => history.value.length);

const filteredHistory = computed(() => {
  let result = [...history.value];

  // 按类型筛选
  if (filter.value.type !== "all") {
    result = result.filter((item) => item.type === filter.value.type);
  }

  // 按时间范围筛选
  if (filter.value.timeRange !== "all") {
    const now = new Date();
    let cutoffDate;

    switch (filter.value.timeRange) {
      case "today":
        cutoffDate = new Date(now.setHours(0, 0, 0, 0));
        break;
      case "week":
        cutoffDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000);
        break;
      case "month":
        cutoffDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000);
        break;
    }

    result = result.filter((item) => new Date(item.timestamp) >= cutoffDate);
  }

  // 搜索
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase().trim();
    result = result.filter(
      (item) =>
        item.title.toLowerCase().includes(query) ||
        item.query.toLowerCase().includes(query) ||
        (item.platform && item.platform.toLowerCase().includes(query)),
    );
  }

  // 按时间倒序排序
  result.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));

  return result;
});

const paginatedHistory = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return filteredHistory.value.slice(start, end);
});

// 加载历史记录
const loadHistory = () => {
  try {
    const priceHistory = JSON.parse(
      localStorage.getItem("priceHistory") || "[]",
    );
    const scheduleHistory = JSON.parse(
      localStorage.getItem("scheduleHistory") || "[]",
    );

    const priceItems = priceHistory.map((item) => ({
      id: `price_${item.id || Date.now()}`,
      type: "price",
      title: "比价查询",
      query: item.query || "未知查询",
      timestamp: item.timestamp || new Date().toISOString(),
      resultCount: item.result_count || item.products?.length || 0,
      platform: item.platform || "多个平台",
      data: item,
    }));

    const scheduleItems = scheduleHistory.map((item) => ({
      id: `schedule_${item.id || Date.now()}`,
      type: "schedule",
      title: "未来日程",
      query: item.query || "未知查询",
      timestamp: item.timestamp || new Date().toISOString(),
      eventCount: item.events?.length || 0,
      data: item,
    }));

    history.value = [...priceItems, ...scheduleItems];

    // 重置选中状态和分页到第一页
    selectedItems.value = [];
    selectAll.value = false;
    currentPage.value = 1;
  } catch (error) {
    console.error("加载历史记录失败:", error);
    history.value = [];
    ElMessage.error("读取历史记录失败，请检查浏览器存储设置");
  }
};

// 格式化时间
const formatTime = (timestamp) => {
  try {
    const date = new Date(timestamp);
    const now = new Date();

    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);
    if (date.toDateString() === yesterday.toDateString()) {
      return (
        "昨天 " +
        date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
      );
    }

    const diff = now - date;
    if (diff < 7 * 24 * 60 * 60 * 1000) {
      const days = Math.floor(diff / (24 * 60 * 60 * 1000));
      return `${days}天前`;
    }

    return (
      date.toLocaleDateString() +
      " " +
      date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
    );
  } catch (error) {
    return "未知时间";
  }
};

// 查看项目
const viewItem = (item) => {
  console.log("查看历史记录:", item);
  // 可通过 emit 事件向父组件传递查看请求
  // emit('view', item)

  if (item.type === "price") {
    ElMessage.info("跳转到比价详情（需实现路由或事件传递）");
  } else if (item.type === "schedule") {
    ElMessage.info("跳转到日程详情（需实现路由或事件传递）");
  }
};

// 删除单个项目
const deleteItem = async (item) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除这条${item.type === "price" ? "比价" : "日程"}记录吗？`,
      "确认删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    if (item.type === "price") {
      const priceHistory = JSON.parse(
        localStorage.getItem("priceHistory") || "[]",
      );
      const updatedHistory = priceHistory.filter(
        (priceItem) => `price_${priceItem.id || ""}` !== item.id,
      );
      localStorage.setItem("priceHistory", JSON.stringify(updatedHistory));
    } else if (item.type === "schedule") {
      const scheduleHistory = JSON.parse(
        localStorage.getItem("scheduleHistory") || "[]",
      );
      const updatedHistory = scheduleHistory.filter(
        (scheduleItem) => `schedule_${scheduleItem.id || ""}` !== item.id,
      );
      localStorage.setItem("scheduleHistory", JSON.stringify(updatedHistory));
    }

    loadHistory();
    ElMessage.success("记录已删除");
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("删除失败: " + error.message);
    }
  }
};

// 全选/取消全选
const toggleSelectAll = (checked) => {
  if (checked) {
    selectedItems.value = paginatedHistory.value.map((item) => item.id);
  } else {
    selectedItems.value = [];
  }
};

// 删除选中的项目
const deleteSelected = async () => {
  if (selectedItems.value.length === 0) return;

  const count = selectedItems.value.length; // 提前保存数量

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${count} 条记录吗？`,
      "确认批量删除",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    const priceIds = selectedItems.value
      .filter((id) => id.startsWith("price_"))
      .map((id) => id.replace("price_", ""));
    const scheduleIds = selectedItems.value
      .filter((id) => id.startsWith("schedule_"))
      .map((id) => id.replace("schedule_", ""));

    if (priceIds.length > 0) {
      const priceHistory = JSON.parse(
        localStorage.getItem("priceHistory") || "[]",
      );
      const updatedHistory = priceHistory.filter(
        (item) => !priceIds.includes(String(item.id || "")),
      );
      localStorage.setItem("priceHistory", JSON.stringify(updatedHistory));
    }

    if (scheduleIds.length > 0) {
      const scheduleHistory = JSON.parse(
        localStorage.getItem("scheduleHistory") || "[]",
      );
      const updatedHistory = scheduleHistory.filter(
        (item) => !scheduleIds.includes(String(item.id || "")),
      );
      localStorage.setItem("scheduleHistory", JSON.stringify(updatedHistory));
    }

    loadHistory();
    ElMessage.success(`已删除 ${count} 条记录`);
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("删除失败: " + error.message);
    }
  }
};

// 清空全部历史记录
const clearAllHistory = async () => {
  try {
    await ElMessageBox.confirm(
      "确定要清空所有历史记录吗？此操作不可恢复。",
      "确认清空",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    localStorage.removeItem("priceHistory");
    localStorage.removeItem("scheduleHistory");

    loadHistory();
    ElMessage.success("所有历史记录已清空");
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("清空失败: " + error.message);
    }
  }
};

// 监听过滤条件变化，重置分页和选中
watch([filter, searchQuery], () => {
  currentPage.value = 1;
  selectedItems.value = [];
  selectAll.value = false;
});

// 监听分页变化，清空选中
watch([currentPage, pageSize], () => {
  selectedItems.value = [];
  selectAll.value = false;
});

// 初始化
onMounted(() => {
  loadHistory();
});
</script>

<style scoped>
.unified-history-card {
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

.history-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.filter-section {
  display: flex;
  gap: 8px;
}

.search-section {
  display: flex;
  gap: 8px;
}

.empty-history {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #a0aec0;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 18px;
  font-weight: 500;
  color: #4a5568;
  margin-bottom: 8px;
}

.empty-hint {
  font-size: 14px;
  margin: 0;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 4px;
}

.history-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  transition: all 0.2s;
  gap: 16px;
}

.history-item:hover {
  border-color: #4299e1;
  box-shadow: 0 2px 8px rgba(66, 153, 225, 0.1);
}

.history-item.price {
  border-left: 4px solid #48bb78;
}

.history-item.schedule {
  border-left: 4px solid #4299e1;
}

.item-icon {
  flex-shrink: 0;
  padding-top: 4px;
}

.item-icon .el-icon {
  font-size: 20px;
  color: #718096;
}

.history-item.price .item-icon .el-icon {
  color: #48bb78;
}

.history-item.schedule .item-icon .el-icon {
  color: #4299e1;
}

.item-content {
  flex: 1;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.item-title {
  font-weight: 600;
  color: #1a202c;
}

.item-time {
  font-size: 12px;
  color: #a0aec0;
}

.item-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item-query {
  margin: 0;
  color: #4a5568;
  font-size: 14px;
}

.item-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.item-platform {
  font-size: 12px;
  color: #718096;
  background: #f7fafc;
  padding: 2px 8px;
  border-radius: 4px;
}

.item-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.batch-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.batch-buttons {
  display: flex;
  gap: 12px;
}

.history-pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 深色主题样式 */
:global(.dark-theme) .unified-history-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .history-count {
  color: #a0aec0;
}

:global(.dark-theme) .history-controls {
  border-bottom-color: #4a5568;
}

:global(.dark-theme) .history-tabs .el-tabs__item {
  color: #cbd5e0;
}

:global(.dark-theme) .history-tabs .el-tabs__item:hover {
  color: #e2e8f0;
}

:global(.dark-theme) .history-tabs .el-tabs__item.is-active {
  color: #63b3ed;
}

:global(.dark-theme) .history-tabs .el-tabs__active-bar {
  background-color: #63b3ed;
}

:global(.dark-theme) .history-tabs .el-tabs__nav-wrap::after {
  background-color: #4a5568;
}

:global(.dark-theme) .history-list {
  border-color: #4a5568;
}

:global(.dark-theme) .history-item {
  border-bottom-color: #4a5568;
}

:global(.dark-theme) .history-item:hover {
  background: #4a5568;
}

:global(.dark-theme) .item-content {
  color: #e2e8f0;
}

:global(.dark-theme) .item-query {
  color: #cbd5e0;
}

:global(.dark-theme) .item-platform {
  color: #a0aec0;
  background: #4a5568;
}

:global(.dark-theme) .item-time {
  color: #a0aec0;
}

:global(.dark-theme) .item-actions .el-button {
  color: #cbd5e0;
}

:global(.dark-theme) .item-actions .el-button:hover {
  color: #63b3ed;
  background: #4a5568;
}

:global(.dark-theme) .batch-actions {
  border-top-color: #4a5568;
}

:global(.dark-theme) .batch-info {
  color: #a0aec0;
}

:global(.dark-theme) .empty-state {
  color: #a0aec0;
}

:global(.dark-theme) .empty-state .el-icon {
  color: #718096;
}

:global(.dark-theme) .empty-state p {
  color: #a0aec0;
}
</style>
