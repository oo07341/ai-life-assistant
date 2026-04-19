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
          :time-location="timeLocation"
          :is-generating="isGenerating"
          @update:schedule-query="scheduleQuery = $event"
          @update:time-location="timeLocation = $event"
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
import { analyzeIntent } from "@/services/api.js";
import ScheduleInput from "@/components/schedule/ScheduleInput.vue";
import ScheduleResults from "@/components/schedule/ScheduleResults.vue";
import ScheduleHistory from "@/components/schedule/ScheduleHistory.vue";
import CalendarPreview from "@/components/schedule/CalendarPreview.vue";

// 响应式数据
const scheduleQuery = ref("");
const timeLocation = ref("");
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
    // 调用AI接口分析意图
    const apiBaseUrl =
      import.meta.env.VITE_API_BASE_URL || "http://localhost:3001";
    const useAI = import.meta.env.VITE_USE_AI === "true";

    let intentResult = null;
    let intent = "通用日程";
    let timeSlots = ["18:00-19:00", "19:30-20:30"];
    let duration = "1小时";
    let location = timeLocation.value || "待定地点";
    let notes = "建议提前规划";

    if (useAI) {
      console.log("🔍 启用AI分析，调用统一的API服务...");
      try {
        // 使用统一的API服务层调用AI分析
        intentResult = await analyzeIntent(scheduleQuery.value);
        console.log("🤖 AI分析结果:", intentResult);

        // 解析AI返回的意图
        if (intentResult.intent) {
          const aiIntent = intentResult.intent.intent || intentResult.intent;
          console.log("🎯 AI意图:", aiIntent);
          console.log("📋 商品关键词:", intentResult.intent.product_keywords);

          // 根据AI意图设置日程参数
          if (aiIntent === "shopping" || aiIntent === "购物") {
            intent = "购物安排";
            timeSlots = ["14:00-16:00", "19:00-21:00"];
            duration = "2小时";
            notes = "建议选择非高峰时段购物";
            location = timeLocation.value || "附近商场";
            console.log("🛍️ 设置为购物安排");
          } else if (aiIntent === "schedule" || aiIntent === "日程") {
            intent = "学习规划";
            timeSlots = ["09:00-11:00", "14:00-16:00", "19:00-21:00"];
            duration = "2小时";
            notes = "建议分段学习，每2小时休息一次";
            location = timeLocation.value || "图书馆";
            console.log("📚 设置为学习规划");
          } else if (aiIntent === "餐饮" || aiIntent === "饮食") {
            intent = "餐饮安排";
            timeSlots = ["18:00-19:30"];
            duration = "1.5小时";
            notes = "建议选择晚餐时间，避开高峰期";
            location = timeLocation.value || "餐厅";
            console.log("🍽️ 设置为餐饮安排");
          } else if (aiIntent === "娱乐" || aiIntent === "休闲") {
            intent = "观影娱乐";
            timeSlots = ["19:30-21:30", "21:30-23:30"];
            duration = "2小时";
            notes = "建议提前购票，选择合适场次";
            location = timeLocation.value || "电影院";
            console.log("🎬 设置为观影娱乐");
          } else if (aiIntent === "运动" || aiIntent === "健身") {
            intent = "运动健身";
            timeSlots = ["07:00-08:00", "18:00-19:00"];
            duration = "1小时";
            notes = "建议选择早晨或傍晚运动";
            location = timeLocation.value || "健身房";
            console.log("💪 设置为运动健身");
          } else {
            console.log("❓ 未知AI意图，使用通用日程");
          }

          // 如果有商品关键词，进一步细化意图
          if (
            intentResult.intent.product_keywords &&
            intentResult.intent.product_keywords.length > 0
          ) {
            const keywords = intentResult.intent.product_keywords
              .join(" ")
              .toLowerCase();
            console.log("🔤 关键词组合:", keywords);

            if (keywords.includes("披萨") || keywords.includes("pizza")) {
              intent = "购买披萨";
              notes = "建议选择晚餐时间，避开高峰期";
              location = timeLocation.value || "必胜客中关村店";
              console.log("🍕 细化为购买披萨");
            } else if (
              keywords.includes("汉堡") ||
              keywords.includes("hamburger")
            ) {
              intent = "购买汉堡";
              notes = "建议选择午餐时间，快餐更快捷";
              location = timeLocation.value || "麦当劳餐厅";
              console.log("🍔 细化为购买汉堡");
            } else if (
              keywords.includes("奶茶") ||
              keywords.includes("茶") ||
              keywords.includes("饮料")
            ) {
              intent = "购买饮品";
              notes = "建议选择下午茶时间";
              location = timeLocation.value || "附近饮品店";
              console.log("🧋 细化为购买饮品");
            }
          }
        } else {
          console.log("⚠️ AI返回数据中没有intent字段");
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
      const query = scheduleQuery.value.toLowerCase();

      // 增强的意图识别逻辑（备用方案）
      if (
        query.includes("披萨") ||
        query.includes("pizza") ||
        query.includes("必胜客") ||
        query.includes("达美乐")
      ) {
        intent = "购买披萨";
        notes = "建议选择晚餐时间，避开高峰期";
        location = timeLocation.value || "必胜客中关村店";
      } else if (
        query.includes("汉堡") ||
        query.includes("hamburger") ||
        query.includes("麦当劳") ||
        query.includes("肯德基")
      ) {
        intent = "购买汉堡";
        notes = "建议选择午餐时间，快餐更快捷";
        location = timeLocation.value || "麦当劳餐厅";
      } else if (
        query.includes("奶茶") ||
        query.includes("茶") ||
        query.includes("饮料") ||
        query.includes("咖啡")
      ) {
        intent = "购买饮品";
        notes = "建议选择下午茶时间";
        location = timeLocation.value || "附近饮品店";
      } else if (
        query.includes("学习") ||
        query.includes("复习") ||
        query.includes("考试") ||
        query.includes("读书") ||
        query.includes("看书")
      ) {
        intent = "学习规划";
        timeSlots = ["09:00-11:00", "14:00-16:00", "19:00-21:00"];
        duration = "2小时";
        notes = "建议分段学习，每2小时休息一次";
        location = timeLocation.value || "图书馆";
      } else if (
        query.includes("会议") ||
        query.includes("开会") ||
        query.includes("讨论") ||
        query.includes("汇报")
      ) {
        intent = "会议安排";
        timeSlots = ["10:00-11:30", "15:00-16:30"];
        duration = "1.5小时";
        notes = "建议预留会前准备时间";
        location = timeLocation.value || "会议室";
      } else if (
        query.includes("购物") ||
        query.includes("买") ||
        query.includes("购买") ||
        query.includes("逛街")
      ) {
        intent = "购物安排";
        timeSlots = ["14:00-16:00", "19:00-21:00"];
        duration = "2小时";
        notes = "建议选择非高峰时段购物";
        location = timeLocation.value || "附近商场";
      } else if (
        query.includes("运动") ||
        query.includes("健身") ||
        query.includes("跑步") ||
        query.includes("锻炼")
      ) {
        intent = "运动健身";
        timeSlots = ["07:00-08:00", "18:00-19:00"];
        duration = "1小时";
        notes = "建议选择早晨或傍晚运动";
        location = timeLocation.value || "健身房";
      } else if (
        query.includes("电影") ||
        query.includes("看片") ||
        query.includes("影院")
      ) {
        intent = "观影娱乐";
        timeSlots = ["19:30-21:30", "21:30-23:30"];
        duration = "2小时";
        notes = "建议提前购票，选择合适场次";
        location = timeLocation.value || "电影院";
      } else if (
        query.includes("吃饭") ||
        query.includes("用餐") ||
        query.includes("晚餐") ||
        query.includes("午餐") ||
        query.includes("早餐")
      ) {
        intent = "餐饮安排";
        if (query.includes("早餐")) {
          timeSlots = ["07:00-08:00"];
          notes = "建议早起享用早餐";
        } else if (query.includes("午餐")) {
          timeSlots = ["12:00-13:00"];
          notes = "建议避开午餐高峰时段";
        } else if (query.includes("晚餐")) {
          timeSlots = ["18:00-19:30"];
          notes = "建议选择晚餐时间，避开高峰期";
        }
        location = timeLocation.value || "餐厅";
      }
    }

    scheduleResult.value = {
      intent: intent,
      time_slots: timeSlots,
      duration: duration,
      location: location,
      notes: notes,
    };

    // 模拟日程事件 - 根据查询动态生成
    const now = new Date();
    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    const dayAfterTomorrow = new Date(now.getTime() + 2 * 24 * 60 * 60 * 1000);

    let event1Title = "用户日程安排";
    let event1Location = timeLocation.value || "待定地点";
    let event1Description = "根据您的需求安排的日程";

    let event2Title = "相关活动规划";
    let event2Location = "根据情况安排";
    let event2Description = "相关后续活动安排";

    if (intent === "购买披萨") {
      event1Title = "购买披萨 - 必胜客";
      event1Location = timeLocation.value || "必胜客中关村店";
      event1Description = "购买超级至尊披萨";
      event2Title = "晚餐时间";
      event2Description = "享用披萨晚餐";
    } else if (intent === "购买汉堡") {
      event1Title = "购买汉堡 - 麦当劳";
      event1Location = timeLocation.value || "麦当劳餐厅";
      event1Description = "购买汉堡套餐";
      event2Title = "午餐时间";
      event2Description = "享用汉堡午餐";
    } else if (intent === "购买饮品") {
      event1Title = "购买饮品 - 奶茶店";
      event1Location = timeLocation.value || "附近饮品店";
      event1Description = "购买招牌奶茶";
      event2Title = "下午茶时间";
      event2Description = "享用饮品休息";
    } else if (intent === "学习规划") {
      event1Title = "学习时间 - 上午";
      event1Location = timeLocation.value || "图书馆";
      event1Description = "上午学习时段";
      event2Title = "学习时间 - 下午";
      event2Location = "自习室";
      event2Description = "下午学习时段";
    } else if (intent === "会议安排") {
      event1Title = "工作会议";
      event1Location = timeLocation.value || "会议室";
      event1Description = "团队工作会议";
      event2Title = "会议准备";
      event2Location = "办公室";
      event2Description = "会议材料准备";
    } else if (intent === "购物安排") {
      event1Title = "购物时间";
      event1Location = timeLocation.value || "附近商场";
      event1Description = "购买日常用品";
      event2Title = "休息时间";
      event2Description = "购物后休息";
    } else if (intent === "运动健身") {
      event1Title = "运动时间";
      event1Location = timeLocation.value || "健身房";
      event1Description = "健身锻炼";
      event2Title = "放松时间";
      event2Description = "运动后放松";
    } else if (intent === "观影娱乐") {
      event1Title = "观影时间";
      event1Location = timeLocation.value || "电影院";
      event1Description = "观看电影";
      event2Title = "讨论时间";
      event2Description = "电影观后讨论";
    } else if (intent === "餐饮安排") {
      if (query.includes("早餐")) {
        event1Title = "早餐时间";
        event1Description = "享用早餐";
      } else if (query.includes("午餐")) {
        event1Title = "午餐时间";
        event1Description = "享用午餐";
      } else if (query.includes("晚餐")) {
        event1Title = "晚餐时间";
        event1Description = "享用晚餐";
      } else {
        event1Title = "用餐时间";
        event1Description = "享用美食";
      }
      event1Location = timeLocation.value || "餐厅";
      event2Title = "休息时间";
      event2Description = "用餐后休息";
    }

    events.value = [
      {
        id: 1,
        title: event1Title,
        start: tomorrow.toISOString(),
        end: new Date(tomorrow.getTime() + 60 * 60 * 1000).toISOString(), // 明天+1小时
        location: event1Location,
        description: event1Description,
      },
      {
        id: 2,
        title: event2Title,
        start: dayAfterTomorrow.toISOString(),
        end: new Date(
          dayAfterTomorrow.getTime() + 90 * 60 * 1000,
        ).toISOString(), // 后天+1.5小时
        location: event2Location,
        description: event2Description,
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
  timeLocation.value = "";
  scheduleResult.value = null;
  events.value = [];
};

// 添加到历史记录
const addToHistory = () => {
  const historyItem = {
    id: Date.now(),
    query: scheduleQuery.value,
    time_location: timeLocation.value,
    event_count: events.value.length,
    timestamp: new Date().toISOString(),
    result: scheduleResult.value,
    events: events.value,
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
  timeLocation.value = historyItem.time_location || "";
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
