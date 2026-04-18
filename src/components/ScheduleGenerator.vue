<script setup>
import { ref, watch, computed } from "vue";
import { createEvents } from "ics";

// 定义props
const props = defineProps({
  selectedProduct: {
    type: Object,
    default: () => null,
  },
  searchQuery: {
    type: String,
    default: "",
  },
});

// 响应式数据
const isLoading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const userQuery = ref("我想吃披萨，选了必胜客超级至尊披萨");
const extraShopName = ref("必胜客中关村店");
const extraAddress = ref("中关村大街1号");
const showCalendarOptions = ref(false);
const googleCalendarLink = ref("");
const outlookCalendarLink = ref("");

// 环境变量
const isDev = import.meta.env.DEV;
const useMock = import.meta.env.VITE_USE_MOCK === "true";

// 监听props变化，自动填充数据
watch(
  () => props.selectedProduct,
  (newProduct) => {
    if (newProduct) {
      // 自动填充商品信息
      userQuery.value = `我想购买${newProduct.name}，价格¥${newProduct.price}`;
      extraShopName.value = newProduct.platform;
      extraAddress.value = "根据平台定位";

      // 显示提示
      successMessage.value = "已自动填充商品信息，点击生成日程按钮即可规划";
      setTimeout(() => {
        successMessage.value = "";
      }, 3000);
    }
  },
  { immediate: true },
);

watch(
  () => props.searchQuery,
  (newQuery) => {
    if (newQuery && !props.selectedProduct) {
      userQuery.value = newQuery;
    }
  },
  { immediate: true },
);

// 根据商品信息生成Mock事件
const generateMockEventsFromProduct = (product) => {
  if (!product) return mockEvents;

  const now = new Date();
  const twoHoursLater = new Date(now.getTime() + 2 * 60 * 60 * 1000);
  const threeHoursLater = new Date(now.getTime() + 3 * 60 * 60 * 1000);
  const fourHoursLater = new Date(now.getTime() + 4 * 60 * 60 * 1000);

  return [
    {
      title: `AI规划：购买${product.name}`,
      start: twoHoursLater.toISOString(),
      end: threeHoursLater.toISOString(),
      location: product.platform,
      description: `根据您的需求，AI为您规划了购买${product.name}的时间，价格¥${product.price}`,
    },
    {
      title: "AI规划：相关活动",
      start: threeHoursLater.toISOString(),
      end: fourHoursLater.toISOString(),
      location: "根据情况安排",
      description: "购买后的相关活动安排",
    },
  ];
};

// Mock数据备用方案
const mockEvents = [
  {
    title: "AI规划：披萨晚餐",
    start: "2026-04-18T19:00:00.000Z",
    end: "2026-04-18T20:30:00.000Z",
    location: "必胜客中关村店",
    description: "根据您的需求，AI为您规划了披萨晚餐时间",
  },
  {
    title: "AI规划：购物时间",
    start: "2026-04-18T21:00:00.000Z",
    end: "2026-04-18T22:00:00.000Z",
    location: "附近商场",
    description: "预留购物时间",
  },
];

// 计算当前应该使用的事件数据
const currentMockEvents = computed(() => {
  return props.selectedProduct
    ? generateMockEventsFromProduct(props.selectedProduct)
    : mockEvents;
});

// ISO时间转数组函数
function isoToArray(isoString) {
  const d = new Date(isoString);
  return [
    d.getFullYear(),
    d.getMonth() + 1,
    d.getDate(),
    d.getHours(),
    d.getMinutes(),
  ];
}

// 生成.ics文件并触发下载
function generateAndDownloadICS(events) {
  try {
    const icsEvents = events.map((event) => ({
      title: event.title,
      start: isoToArray(event.start),
      end: isoToArray(event.end),
      location: event.location,
      description: event.description || "",
    }));

    const { error, value } = createEvents(icsEvents);

    if (error) {
      throw new Error("日历文件生成失败");
    }

    // 创建Blob并下载
    const blob = new Blob([value], { type: "text/calendar;charset=utf-8" });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.setAttribute("download", "ai_schedule.ics");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);

    return { success: true, icsData: value, events: events };
  } catch (err) {
    console.error("ICS生成错误:", err);
    return { success: false, error: err.message };
  }
}

// 生成Google日历链接
function generateGoogleCalendarLink(event) {
  const startTime = encodeURIComponent(
    event.start.replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z"),
  );
  const endTime = encodeURIComponent(
    event.end.replace(/[-:]/g, "").replace(/\.\d{3}Z$/, "Z"),
  );
  const title = encodeURIComponent(event.title);
  const details = encodeURIComponent(event.description || "");
  const location = encodeURIComponent(event.location || "");

  return `https://calendar.google.com/calendar/render?action=TEMPLATE&dates=${startTime}/${endTime}&text=${title}&details=${details}&location=${location}`;
}

// 生成Outlook日历链接
function generateOutlookCalendarLink(event) {
  const startTime = encodeURIComponent(
    new Date(event.start)
      .toISOString()
      .replace(/[-:]/g, "")
      .replace(/\.\d{3}Z$/, "Z"),
  );
  const endTime = encodeURIComponent(
    new Date(event.end)
      .toISOString()
      .replace(/[-:]/g, "")
      .replace(/\.\d{3}Z$/, "Z"),
  );
  const title = encodeURIComponent(event.title);
  const body = encodeURIComponent(
    `${event.description || ""}\n\n地点: ${event.location || ""}`,
  );
  const location = encodeURIComponent(event.location || "");

  return `https://outlook.live.com/calendar/0/deeplink/compose?path=/calendar/action/compose&rru=addevent&startdt=${startTime}&enddt=${endTime}&subject=${title}&body=${body}&location=${location}`;
}

// 尝试使用Web Calendar API（实验性功能）
async function tryAddToWebCalendar(events) {
  // 检查浏览器是否支持Web Calendar API
  if (
    "calendar" in window.navigator &&
    typeof window.navigator.calendar === "object"
  ) {
    try {
      // 这是一个实验性API，目前支持有限
      const calendar = await window.navigator.calendar.requestPermission();
      if (calendar === "granted") {
        // 转换事件格式
        const calendarEvents = events.map((event) => ({
          id: `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          title: event.title,
          startTime: new Date(event.start),
          endTime: new Date(event.end),
          location: event.location,
          description: event.description,
        }));

        // 尝试添加事件（注意：这是一个实验性API）
        await window.navigator.calendar.addEvent(calendarEvents[0]);
        return { success: true, method: "web-calendar-api", eventCount: 1 };
      }
    } catch (err) {
      console.log("Web Calendar API不可用:", err);
    }
  }
  return { success: false, method: "web-calendar-api" };
}

// 调用后端API
async function callAIScheduleAPI(query, extraInfo = {}) {
  const requestBody = {
    query: query || "我想吃披萨",
    context_time: new Date().toISOString(),
    extra_info: extraInfo,
  };

  try {
    const response = await fetch("/api/generate_schedule", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`HTTP错误: ${response.status}`);
    }

    const data = await response.json();

    if (data.success && Array.isArray(data.events)) {
      return data.events;
    } else {
      throw new Error("后端返回格式错误");
    }
  } catch (err) {
    console.error("API调用错误:", err);
    throw err;
  }
}

// 主函数：生成日程
async function generateSchedule() {
  // 重置状态
  isLoading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    // 收集页面上下文信息 - 使用用户输入的值
    const query = userQuery.value || "我想吃披萨";
    const extraInfo = {
      shop_name: extraShopName.value || "",
      address: extraAddress.value || "",
    };

    let events;

    // 使用组件顶部定义的useMock变量
    if (useMock) {
      console.log("使用Mock数据生成日程");
      events = currentMockEvents.value;
    } else {
      // 调用真实API
      events = await callAIScheduleAPI(query, extraInfo);
    }

    // 生成ICS文件
    const icsResult = generateAndDownloadICS(events);

    if (icsResult.success) {
      // 尝试使用Web Calendar API（实验性）
      const webCalendarResult = await tryAddToWebCalendar(events);

      if (webCalendarResult.success) {
        successMessage.value = `✅ 日程已自动添加到您的日历！成功添加了${webCalendarResult.eventCount}个事件。`;
        showCalendarOptions.value = false;
      } else {
        // 如果Web Calendar API不可用，提供一键添加链接
        const firstEvent = events[0];
        googleCalendarLink.value = generateGoogleCalendarLink(firstEvent);
        outlookCalendarLink.value = generateOutlookCalendarLink(firstEvent);

        successMessage.value = "📅 日程已生成！";
        showCalendarOptions.value = true;
      }
    } else {
      throw new Error("日历文件生成失败");
    }
  } catch (err) {
    console.error("生成日程错误:", err);

    // 错误处理：尝试使用Mock数据
    errorMessage.value = `生成失败: ${err.message}，正在尝试使用备用方案...`;

    try {
      const icsResult = generateAndDownloadICS(mockEvents);
      if (icsResult.success) {
        successMessage.value = "已使用备用数据生成日程文件";
        errorMessage.value = "";
      } else {
        errorMessage.value = "备用方案也失败了，请稍后重试";
      }
    } catch (mockErr) {
      errorMessage.value = "所有方案都失败了，请检查网络或稍后重试";
    }
  } finally {
    isLoading.value = false;
  }
}
</script>

<template>
  <div class="schedule-generator">
    <h2>AI日程规划</h2>
    <p class="description">
      点击按钮，AI将根据您的需求智能规划日程并生成日历文件
    </p>

    <!-- 用户输入区域 -->
    <div class="input-section">
      <div class="form-group">
        <label for="user-query">您的需求描述：</label>
        <textarea
          id="user-query"
          v-model="userQuery"
          placeholder="请输入您的需求，例如：我想吃披萨，选了必胜客超级至尊披萨"
          rows="3"
          :disabled="isLoading"
        ></textarea>
        <div class="input-hint">AI将根据您的描述智能规划日程</div>
      </div>

      <div class="extra-info">
        <h4>额外信息（可选）：</h4>
        <div class="form-row">
          <div class="form-group">
            <label for="shop-name">店铺名称：</label>
            <input
              id="shop-name"
              type="text"
              v-model="extraShopName"
              placeholder="例如：必胜客中关村店"
              :disabled="isLoading"
            />
          </div>
          <div class="form-group">
            <label for="address">地址：</label>
            <input
              id="address"
              type="text"
              v-model="extraAddress"
              placeholder="例如：中关村大街1号"
              :disabled="isLoading"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="control-section">
      <button
        class="generate-btn"
        @click="generateSchedule"
        :disabled="isLoading"
        :class="{ loading: isLoading }"
      >
        <span v-if="!isLoading">📅 生成日程并添加到日历</span>
        <span v-else>⏳ AI正在为您规划日程...</span>
      </button>

      <div class="mock-toggle" v-if="isDev">
        <label>
          <input
            type="checkbox"
            :checked="useMock"
            @change="(e) => console.log('Mock切换:', e.target.checked)"
          />
          使用Mock数据（开发模式）
        </label>
      </div>
    </div>

    <!-- 状态提示 -->
    <div class="status-messages">
      <div v-if="isLoading" class="loading-indicator">
        <div class="spinner"></div>
        <p>AI正在分析您的需求并规划最佳日程...</p>
      </div>

      <div v-if="errorMessage" class="error-message">⚠️ {{ errorMessage }}</div>

      <div v-if="successMessage" class="success-message">
        <div v-if="!showCalendarOptions">✅ {{ successMessage }}</div>
        <div v-else class="calendar-success">
          <h4>📅 日程已生成！您可以选择以下方式添加到日历：</h4>
          <div class="calendar-options">
            <div class="calendar-option">
              <strong>1. 自动下载文件</strong><br />
              ✅ 已自动下载 schedule.ics 文件<br />
              📁 请在"下载"文件夹中查找并导入日历应用
            </div>
            <div class="calendar-option">
              <strong>2. 一键添加到Google日历</strong><br />
              <a
                :href="googleCalendarLink"
                target="_blank"
                class="calendar-link"
                >📅 点击这里添加到Google日历</a
              >
            </div>
            <div class="calendar-option">
              <strong>3. 一键添加到Outlook日历</strong><br />
              <a
                :href="outlookCalendarLink"
                target="_blank"
                class="calendar-link"
                >📅 点击这里添加到Outlook日历</a
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能说明 -->
    <div class="feature-info">
      <h3>功能说明：</h3>
      <ul>
        <li>📋 收集当前页面上下文信息（商品、时间、地点）</li>
        <li>🤖 调用AI接口智能规划日程事件</li>
        <li>📅 生成标准.ics日历文件</li>
        <li>⬇️ 自动触发浏览器下载</li>
        <li>🔄 内置Mock数据备用方案</li>
      </ul>

      <div class="usage-tips">
        <h4>Windows 11 使用指南：</h4>
        <p><strong>方法一：一键添加到Outlook日历（推荐）</strong></p>
        <ul>
          <li>点击"一键添加到Outlook日历"链接</li>
          <li>登录您的Microsoft账户</li>
          <li>确认事件信息并保存</li>
          <li>事件将自动同步到Windows日历应用</li>
        </ul>

        <p><strong>方法二：使用Windows日历应用</strong></p>
        <ul>
          <li>下载schedule.ics文件到"下载"文件夹</li>
          <li>打开"开始菜单" → 搜索"日历"应用</li>
          <li>在日历应用中：设置 → 管理账户 → 添加账户</li>
          <li>导入ics文件或使用Google/Outlook账户同步</li>
        </ul>

        <p><strong>方法三：直接导入到Outlook</strong></p>
        <ul>
          <li>如果有Microsoft Outlook桌面版：</li>
          <li>打开Outlook → 文件 → 打开和导出 → 导入/导出</li>
          <li>选择"从iCalendar(.ics)文件导入"</li>
          <li>选择下载的schedule.ics文件</li>
        </ul>

        <p><strong>方法四：使用Google日历</strong></p>
        <ul>
          <li>点击"一键添加到Google日历"链接</li>
          <li>登录您的Google账户</li>
          <li>在Google日历网页版中确认并保存</li>
          <li>安装Google日历Windows应用同步查看</li>
        </ul>

        <div class="windows-tip">
          <strong>💡 提示：</strong> Windows
          11内置的"日历和邮件"应用可以同时连接多个日历服务（Outlook、Google、iCloud等），建议使用此应用统一管理所有日历。
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.schedule-generator {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background: rgba(240, 248, 255, 0.95); /* 浅蓝色背景，透明度95% */
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15); /* 浅蓝色阴影 */
  border: 1px solid rgba(102, 126, 234, 0.1); /* 浅蓝色边框 */
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
}

h2 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
  text-align: center;
}

.description {
  color: #666;
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.input-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(248, 250, 252, 0.9); /* 更浅的蓝色背景，透明度90% */
  border-radius: 8px;
  border: 1px solid rgba(226, 232, 240, 0.8); /* 半透明边框 */
  backdrop-filter: blur(5px); /* 轻微的毛玻璃效果 */
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #2c3e50;
}

.form-group textarea,
.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid rgba(102, 126, 234, 0.3); /* 浅蓝色边框 */
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s ease;
  background-color: rgba(240, 248, 255, 0.8); /* 浅蓝色背景 */
  color: #2c3e50;
}

.form-group textarea:focus,
.form-group input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  background-color: rgba(240, 248, 255, 0.95); /* 聚焦时更明显的浅蓝色 */
}

.form-group textarea:disabled,
.form-group input:disabled {
  background-color: rgba(237, 242, 247, 0.6); /* 禁用状态的浅蓝色 */
  cursor: not-allowed;
  opacity: 0.7;
  border-color: rgba(102, 126, 234, 0.2);
}

.form-group textarea::placeholder,
.form-group input::placeholder {
  color: rgba(102, 126, 234, 0.6); /* 浅蓝色占位符文字 */
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.input-hint {
  font-size: 0.85rem;
  color: #718096;
  margin-top: 0.5rem;
}

.extra-info {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.extra-info h4 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

@media (max-width: 640px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.control-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.generate-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.2rem;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-width: 300px;
}

.generate-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.generate-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.generate-btn.loading {
  background: linear-gradient(135deg, #4a5568 0%, #718096 100%);
}

.mock-toggle {
  font-size: 0.9rem;
  color: #666;
}

.mock-toggle label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.status-messages {
  margin: 1.5rem 0;
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #e2e8f0;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-message {
  background: #fed7d7;
  color: #9b2c2c;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #e53e3e;
  margin: 1rem 0;
}

.success-message {
  background: #c6f6d5;
  color: #276749;
  padding: 1rem;
  border-radius: 8px;
  border-left: 4px solid #38a169;
  margin: 1rem 0;
}

/* 覆盖成功消息内部的日历选项样式 */
.success-message .calendar-options {
  margin-top: 1rem;
}

.success-message .calendar-option {
  background: rgba(255, 255, 255, 0.95);
  color: #2c3e50;
  border-left: 4px solid #4299e1;
}

.success-message .calendar-option strong {
  color: #2c3e50;
}

.success-message .calendar-option .calendar-link {
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
}

.success-message .calendar-option .calendar-link:hover {
  background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
}

/* 覆盖成功消息内部的日历选项边框颜色 */
.success-message .calendar-options .calendar-option:nth-child(1) {
  border-left-color: #38a169; /* 绿色 - 文件下载 */
}

.success-message .calendar-options .calendar-option:nth-child(2) {
  border-left-color: #ea4335; /* 红色 - Google日历 */
}

.success-message .calendar-options .calendar-option:nth-child(3) {
  border-left-color: #0078d4; /* 蓝色 - Outlook日历 */
}

.success-message a.calendar-link {
  color: #2b6cb0;
  text-decoration: none;
  font-weight: 600;
  border-bottom: 2px solid #4299e1;
  padding: 2px 4px;
  margin: 0 4px;
  transition: all 0.2s ease;
  word-break: break-all; /* 允许长URL换行 */
  overflow-wrap: break-word; /* 确保长单词换行 */
  display: inline-block;
  max-width: 100%; /* 限制最大宽度 */
}

.success-message a.calendar-link:hover {
  background-color: #bee3f8;
  border-radius: 4px;
  border-bottom-color: #2b6cb0;
}

.success-message ol,
.success-message ul {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
  overflow-wrap: break-word; /* 确保列表内容换行 */
}

.success-message li {
  margin: 0.25rem 0;
  line-height: 1.5;
  word-break: break-word; /* 允许长内容换行 */
}

/* 确保整个成功消息区域不会导致横向滚动 */
.success-message {
  overflow-wrap: break-word;
  word-break: break-word;
  max-width: 100%;
}

/* 日历选项样式 */
.calendar-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-top: 1rem;
}

.calendar-option {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px;
  padding: 1rem;
  border-left: 4px solid #4299e1;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.calendar-option strong {
  color: #2c3e50;
  font-size: 1.1rem;
  display: block;
  margin-bottom: 0.5rem;
}

.calendar-option .calendar-link {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
  color: white;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  border: none;
  border-bottom: none;
}

.calendar-option .calendar-link:hover {
  background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(49, 130, 206, 0.3);
}

/* 不同选项的不同边框颜色 */
.calendar-options .calendar-option:nth-child(1) {
  border-left-color: #38a169; /* 绿色 - 文件下载 */
}

.calendar-options .calendar-option:nth-child(2) {
  border-left-color: #ea4335; /* 红色 - Google日历 */
}

.calendar-options .calendar-option:nth-child(3) {
  border-left-color: #0078d4; /* 蓝色 - Outlook日历 */
}

.feature-info {
  margin-top: 2rem;
  padding-top: 2rem;
  border-top: 1px solid #e2e8f0;
}

.feature-info h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
}

.feature-info ul {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.feature-info li {
  padding: 0.5rem 0;
  color: #4a5568;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.feature-info li:before {
  content: "•";
  color: #667eea;
  font-weight: bold;
  display: inline-block;
  width: 1em;
}

.usage-tips {
  background: #f7fafc;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1.5rem;
}

.usage-tips h4 {
  color: #2c3e50;
  margin-bottom: 0.5rem;
}

.usage-tips p {
  color: #4a5568;
  margin-bottom: 1rem;
}

.usage-tips ul {
  margin: 0;
  padding-left: 1.5rem;
}

.usage-tips li {
  color: #4a5568;
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.windows-tip {
  background: #e6fffa;
  border-left: 4px solid #38b2ac;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  color: #234e52;
}

.windows-tip strong {
  color: #2c7a7b;
}
</style>
