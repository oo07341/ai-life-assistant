import { createApp } from "vue";
import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import App from "./App.vue";
import router from "./router/index.js";

// 应用初始化时加载主题设置
function loadThemeOnInit() {
  try {
    const savedSettings = localStorage.getItem("systemSettings");
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      const theme = settings.theme || "light";
      applyTheme(theme);
    }
  } catch (error) {
    console.error("加载主题设置失败:", error);
  }
}

// 应用主题
function applyTheme(themeValue) {
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
}

// 监听系统主题变化
window
  .matchMedia("(prefers-color-scheme: dark)")
  .addEventListener("change", (e) => {
    const savedSettings = localStorage.getItem("systemSettings");
    if (savedSettings) {
      const settings = JSON.parse(savedSettings);
      if (settings.theme === "auto") {
        applyTheme("auto");
      }
    }
  });

const app = createApp(App);

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

// 使用Element Plus
app.use(ElementPlus);
// 使用Vue Router
app.use(router);

// 在应用挂载前加载主题
loadThemeOnInit();

app.mount("#app");
