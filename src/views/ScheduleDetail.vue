<template>
  <div class="schedule-detail-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>
        <el-icon><Calendar /></el-icon> AI日程规划
      </h1>
      <p class="page-subtitle">
        智能规划您的购物时间，生成日历文件，支持多平台导入
      </p>
    </div>

    <!-- 主内容区域 -->
    <div class="main-content">
      <!-- 左侧：日程生成 -->
      <div class="left-panel">
        <ScheduleInput
          :schedule-query="scheduleQuery"
          :shop-name="shopName"
          :address="address"
          :is-generating="isGenerating"
          @update:schedule-query="scheduleQuery = $event"
          @update:shop-name="shopName = $event"
          @update:address="address = $event"
          @generate="generateSchedule"
          @clear="clearInput"
        />

        <ScheduleHistory
          :history="scheduleHistory"
          @select-history="loadHistory"
          @clear-history="clearHistory"
        />
      </div>

      <!-- 右侧：日程结果 -->
      <div class="right-panel">
        <ScheduleResults
          :schedule-result="scheduleResult"
          :is-generating="isGenerating"
          :events="events"
          @download-ics="downloadICS"
        />

        <CalendarPreview :events="events" v-if="events.length > 0" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";
import { Calendar } from "@element-plus/icons-vue";
import ScheduleInput from "@/components/schedule/ScheduleInput.vue";
import ScheduleResults from "@/components/schedule/ScheduleResults.vue";
import ScheduleHistory from "@/components/schedule/ScheduleHistory.vue";
import CalendarPreview from "@/components/schedule/CalendarPreview.vue";

// 响应式数据
const scheduleQuery = ref("");
const shopName = ref("");
const address = ref("");
const isGenerating = ref(false);
const scheduleResult = ref(null);
const events = ref([]);
const scheduleHistory = ref([]);

// 生成日程
const generateSchedule = async () => {
  if (!scheduleQuery.value.trim()) {
    ElMessage.warning("请输入您的日程需求");
    return;
  }

  isGenerating.value = true;
  try {
    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 模拟日程结果
    scheduleResult.value = {
      intent: "购买披萨",
      time_slots: ["18:00-19:00", "19:30-20:30"],
      duration: "1小时",
      location: address.value || "附近餐厅",
      notes: "建议提前预订",
    };

    // 模拟日程事件
    events.value = [
      {
        id: 1,
        title: "购买披萨 - 必胜客",
        start: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 明天
        end: new Date(
          Date.now() + 24 * 60 * 60 * 1000 + 60 * 60 * 1000,
        ).toISOString(), // 明天+1小时
        location: address.value || "必胜客中关村店",
        description: "购买超级至尊披萨",
      },
      {
        id: 2,
        title: "购物时间规划",
        start: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), // 后天
        end: new Date(
          Date.now() + 2 * 24 * 60 * 60 * 1000 + 90 * 60 * 1000,
        ).toISOString(), // 后天+1.5小时
        location: "附近商场",
        description: "购买日常用品",
      },
    ];

    // 添加到历史记录
    addToHistory();

    ElMessage.success("日程生成完成！");
  } catch (error) {
    ElMessage.error("日程生成失败，请重试");
  } finally {
    isGenerating.value = false;
  }
};

// 清空输入
const clearInput = () => {
  scheduleQuery.value = "";
  shopName.value = "";
  address.value = "";
  scheduleResult.value = null;
  events.value = [];
};

// 添加到历史记录
const addToHistory = () => {
  const historyItem = {
    id: Date.now(),
    query: scheduleQuery.value,
    shop_name: shopName.value,
    address: address.value,
    event_count: events.value.length,
    timestamp: new Date().toISOString(),
    result: scheduleResult.value,
  };

  scheduleHistory.value.unshift(historyItem);

  // 限制历史记录数量
  if (scheduleHistory.value.length > 10) {
    scheduleHistory.value = scheduleHistory.value.slice(0, 10);
  }

  // 保存到本地存储
  localStorage.setItem(
    "scheduleHistory",
    JSON.stringify(scheduleHistory.value),
  );
};

// 加载历史记录
const loadHistory = (historyItem) => {
  scheduleQuery.value = historyItem.query;
  shopName.value = historyItem.shop_name || "";
  address.value = historyItem.address || "";
  scheduleResult.value = historyItem.result;
  events.value = historyItem.events || [];
};

// 清空历史记录
const clearHistory = () => {
  scheduleHistory.value = [];
  localStorage.removeItem("scheduleHistory");
};

// 下载ICS文件
const downloadICS = () => {
  if (events.value.length === 0) {
    ElMessage.warning("没有可下载的日程事件");
    return;
  }

  // 这里应该调用ics库生成日历文件
  // 暂时用模拟下载
  ElMessage.success("日历文件生成成功！开始下载...");

  // 模拟下载
  setTimeout(() => {
    const blob = new Blob(["模拟日历文件内容"], { type: "text/calendar" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "schedule.ics";
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 500);
};

// 初始化
onMounted(() => {
  // 从本地存储加载历史记录
  const savedHistory = localStorage.getItem("scheduleHistory");
  if (savedHistory) {
    try {
      scheduleHistory.value = JSON.parse(savedHistory);
    } catch (error) {
      console.error("加载历史记录失败:", error);
    }
  }
});
</script>

<style scoped>
.schedule-detail-page {
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
  .schedule-detail-page {
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
  .schedule-detail-page {
    padding: 12px;
  }

  .page-header h1 {
    font-size: 24px;
  }
}
</style>
