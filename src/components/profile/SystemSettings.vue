<template>
  <el-card class="system-settings-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><Setting /></el-icon>
        <span>系统设置</span>
      </div>
    </template>

    <!-- 设置表单 -->
    <div class="settings-form">
      <!-- 主题设置 -->
      <div class="settings-section">
        <h3 class="section-title">
          <el-icon><Brush /></el-icon> 主题设置
        </h3>
        <div class="theme-options">
          <div
            class="theme-option"
            :class="{ active: theme === 'light' }"
            @click="changeTheme('light')"
          >
            <div class="theme-preview light-theme">
              <div class="preview-header"></div>
              <div class="preview-content"></div>
            </div>
            <span class="theme-label">浅色主题</span>
          </div>
          <div
            class="theme-option"
            :class="{ active: theme === 'dark' }"
            @click="changeTheme('dark')"
          >
            <div class="theme-preview dark-theme">
              <div class="preview-header"></div>
              <div class="preview-content"></div>
            </div>
            <span class="theme-label">深色主题</span>
          </div>
          <div
            class="theme-option"
            :class="{ active: theme === 'auto' }"
            @click="changeTheme('auto')"
          >
            <div class="theme-preview auto-theme">
              <div class="preview-header"></div>
              <div class="preview-content"></div>
            </div>
            <span class="theme-label">跟随系统</span>
          </div>
        </div>
      </div>

      <!-- 通知设置 -->
      <div class="settings-section">
        <h3 class="section-title">
          <el-icon><Bell /></el-icon> 通知设置
        </h3>
        <div class="notification-settings">
          <el-switch
            v-model="notifications.priceAlerts"
            active-text="价格提醒"
            inactive-text="价格提醒"
          />
          <el-switch
            v-model="notifications.scheduleReminders"
            active-text="日程提醒"
            inactive-text="日程提醒"
          />
          <el-switch
            v-model="notifications.systemUpdates"
            active-text="系统更新"
            inactive-text="系统更新"
          />
        </div>
      </div>

      <!-- 数据管理 -->
      <div class="settings-section">
        <h3 class="section-title">
          <el-icon><DataLine /></el-icon> 数据管理
        </h3>
        <div class="data-management">
          <el-button type="primary" @click="exportData">
            <el-icon><Download /></el-icon> 导出数据
          </el-button>
          <el-button type="danger" @click="clearData">
            <el-icon><Delete /></el-icon> 清除缓存
          </el-button>
          <el-button type="info" @click="resetSettings">
            <el-icon><Refresh /></el-icon> 恢复默认设置
          </el-button>
        </div>
        <p class="data-info">已使用存储空间: {{ storageUsage }}</p>
      </div>

      <!-- 隐私设置 -->
      <div class="settings-section">
        <h3 class="section-title">
          <el-icon><Lock /></el-icon> 隐私设置
        </h3>
        <div class="privacy-settings">
          <el-switch
            v-model="privacy.collectAnalytics"
            active-text="收集匿名使用数据"
            inactive-text="不收集使用数据"
          />
          <p class="privacy-hint">
            匿名数据帮助我们改进产品体验，不会包含任何个人信息
          </p>
        </div>
      </div>

      <!-- 保存按钮 -->
      <div class="settings-actions">
        <el-button
          type="primary"
          size="large"
          @click="saveSettings"
          :loading="saving"
        >
          <el-icon><Check /></el-icon> 保存设置
        </el-button>
        <el-button @click="resetToCurrent"> 取消 </el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Setting,
  Brush,
  Bell,
  DataLine,
  Download,
  Delete,
  Refresh,
  Lock,
  Check,
} from "@element-plus/icons-vue";
import { ElMessage, ElMessageBox } from "element-plus";

// 主题设置
const theme = ref("light");

// 通知设置
const notifications = ref({
  priceAlerts: true,
  scheduleReminders: true,
  systemUpdates: false,
});

// 隐私设置
const privacy = ref({
  collectAnalytics: true,
});

// 保存状态
const saving = ref(false);

// 计算存储使用情况
const storageUsage = computed(() => {
  try {
    let total = 0;
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      const value = localStorage.getItem(key);
      total += key.length + value.length;
    }
    return (total / 1024).toFixed(2) + " KB";
  } catch (error) {
    return "未知";
  }
});

// 加载设置
const loadSettings = () => {
  try {
    const savedSettings = localStorage.getItem("systemSettings");
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      theme.value = settings.theme || "light";
      notifications.value = settings.notifications || notifications.value;
      privacy.value = settings.privacy || privacy.value;
    }
  } catch (error) {
    console.error("加载设置失败:", error);
  }
};

// 保存设置
const saveSettings = async () => {
  saving.value = true;
  try {
    const settings = {
      theme: theme.value,
      notifications: notifications.value,
      privacy: privacy.value,
      savedAt: new Date().toISOString(),
    };

    localStorage.setItem("systemSettings", JSON.stringify(settings));

    // 应用主题
    applyThemeLocal(theme.value);

    await new Promise((resolve) => setTimeout(resolve, 500)); // 模拟保存延迟

    ElMessage.success("设置已保存");
  } catch (error) {
    ElMessage.error("保存设置失败: " + error.message);
  } finally {
    saving.value = false;
  }
};

// 应用主题（本地函数，避免与main.js中的函数冲突）
const applyThemeLocal = (themeValue) => {
  const html = document.documentElement;

  if (themeValue === "dark") {
    html.classList.add("dark-theme");
  } else if (themeValue === "light") {
    html.classList.remove("dark-theme");
  } else if (themeValue === "auto") {
    // 跟随系统
    const prefersDark = window.matchMedia(
      "(prefers-color-scheme: dark)",
    ).matches;
    if (prefersDark) {
      html.classList.add("dark-theme");
    } else {
      html.classList.remove("dark-theme");
    }
  }
};

// 切换主题
const changeTheme = (newTheme) => {
  theme.value = newTheme;
  // 立即应用主题，无需等待保存
  applyThemeLocal(newTheme);
};

// 导出数据
const exportData = async () => {
  try {
    const data = {
      systemSettings: localStorage.getItem("systemSettings"),
      priceHistory: localStorage.getItem("priceHistory"),
      scheduleHistory: localStorage.getItem("scheduleHistory"),
      exportDate: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `ai-life-assistant-backup-${new Date().toISOString().split("T")[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    ElMessage.success("数据导出成功");
  } catch (error) {
    ElMessage.error("导出数据失败: " + error.message);
  }
};

// 清除数据
const clearData = async () => {
  try {
    await ElMessageBox.confirm(
      "确定要清除所有缓存数据吗？此操作不可恢复。",
      "警告",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    // 清除缓存数据，但保留系统设置
    const settings = localStorage.getItem("systemSettings");
    localStorage.clear();
    if (settings) {
      localStorage.setItem("systemSettings", settings);
    }

    ElMessage.success("缓存数据已清除");
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("清除数据失败: " + error.message);
    }
  }
};

// 恢复默认设置
const resetSettings = async () => {
  try {
    await ElMessageBox.confirm(
      "确定要恢复默认设置吗？当前设置将被覆盖。",
      "确认",
      {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      },
    );

    theme.value = "light";
    notifications.value = {
      priceAlerts: true,
      scheduleReminders: true,
      systemUpdates: false,
    };
    privacy.value = {
      collectAnalytics: true,
    };

    ElMessage.success("已恢复默认设置");
  } catch (error) {
    if (error !== "cancel") {
      ElMessage.error("恢复设置失败: " + error.message);
    }
  }
};

// 取消更改
const resetToCurrent = () => {
  loadSettings();
  ElMessage.info("已取消更改");
};

// 初始化
onMounted(() => {
  loadSettings();
  applyThemeLocal(theme.value);
});
</script>

<style scoped>
.system-settings-card {
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

.settings-form {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.settings-section {
  padding-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.settings-section:last-child {
  border-bottom: none;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title .el-icon {
  color: #4299e1;
}

/* 主题设置 */
.theme-options {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.theme-option {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  padding: 12px;
  border-radius: 8px;
  transition: all 0.2s;
}

.theme-option:hover {
  background: #f7fafc;
}

.theme-option.active {
  background: #ebf8ff;
  border: 2px solid #4299e1;
}

.theme-preview {
  width: 120px;
  height: 80px;
  border-radius: 6px;
  overflow: hidden;
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

.preview-header {
  height: 20px;
  background: #667eea;
}

.preview-content {
  flex: 1;
  background: #f7fafc;
}

.light-theme .preview-content {
  background: #ffffff;
}

.dark-theme .preview-header {
  background: #4a5568;
}

.dark-theme .preview-content {
  background: #1a202c;
}

.auto-theme .preview-header {
  background: linear-gradient(90deg, #667eea 50%, #4a5568 50%);
}

.auto-theme .preview-content {
  background: linear-gradient(90deg, #ffffff 50%, #1a202c 50%);
}

.theme-label {
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
}

/* 通知设置 */
.notification-settings {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.notification-settings .el-switch {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 数据管理 */
.data-management {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 16px;
}

.data-info {
  font-size: 14px;
  color: #718096;
  margin: 0;
}

/* 隐私设置 */
.privacy-settings {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.privacy-hint {
  font-size: 13px;
  color: #a0aec0;
  margin: 0;
  line-height: 1.5;
}

/* 保存按钮 */
.settings-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  padding-top: 24px;
  border-top: 1px solid #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .theme-options {
    flex-direction: column;
    align-items: center;
  }

  .data-management {
    flex-direction: column;
  }

  .data-management .el-button {
    width: 100%;
  }

  .settings-actions {
    flex-direction: column;
  }

  .settings-actions .el-button {
    width: 100%;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .system-settings-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .settings-section {
  border-bottom-color: #4a5568;
}

:global(.dark-theme) .section-title {
  color: #e2e8f0;
}

:global(.dark-theme) .theme-option:hover {
  background: #4a5568;
}

:global(.dark-theme) .theme-option.active {
  background: #2d3748;
  border-color: #4299e1;
}

:global(.dark-theme) .theme-label {
  color: #cbd5e0;
}

:global(.dark-theme) .data-info {
  color: #a0aec0;
}

:global(.dark-theme) .privacy-hint {
  color: #718096;
}
</style>
