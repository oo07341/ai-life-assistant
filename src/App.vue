<script setup>
import ScheduleGenerator from "./components/ScheduleGenerator.vue";
</script>

<template>
  <div class="app-container">
    <header class="app-header">
      <h1>AI生活助手 - 智能日程规划</h1>
      <p class="subtitle">利用AI技术为您智能规划日常安排</p>
    </header>

    <main class="app-main">
      <ScheduleGenerator />
    </main>

    <footer class="app-footer">
      <p>© 2026 AI生活助手 | 基于Vue 3 + Vite构建</p>
    </footer>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family:
    -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu,
    Cantarell, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem 1rem;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.app-header h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.app-header .subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 600px;
  margin: 0 auto;
}

.app-main {
  flex: 1;
  padding: 2rem 1rem;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.app-footer {
  background: #2c3e50;
  color: white;
  text-align: center;
  padding: 1.5rem;
  margin-top: auto;
}

.app-footer p {
  opacity: 0.8;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .app-header h1 {
    font-size: 2rem;
  }

  .app-header .subtitle {
    font-size: 1rem;
  }

  .app-main {
    padding: 1rem;
  }
}

@media (max-width: 480px) {
  .app-header h1 {
    font-size: 1.5rem;
  }

  .app-header {
    padding: 1.5rem 1rem;
  }
}
</style>
