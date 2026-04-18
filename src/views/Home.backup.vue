<template>
  <div class="home-page">
    <!-- 导入组件 -->
    <HeroSection />
    <FeaturesSection />
    <WorkflowSection />

    <!-- 页脚 -->
    <footer class="app-footer">
      <p>AI生活助手 - 让AI为您的生活提供智能解决方案</p>
      <p class="footer-links">
        <el-button type="text" @click="showAbout">关于</el-button>
        <el-button type="text" @click="showHelp">帮助</el-button>
        <el-button type="text" @click="showMockInfo">Mock模式</el-button>
      </p>
    </footer>

    <!-- 关于对话框 -->
    <el-dialog v-model="showAboutDialog" title="关于AI生活助手" width="500px">
      <div class="about-content">
        <h3>项目简介</h3>
        <p>
          AI生活助手是一个基于Vue 3 + Element
          Plus的智能生活工具，结合了AI智能比价和日程规划两大核心功能。
        </p>

        <h3>技术栈</h3>
        <ul>
          <li><strong>前端</strong>: Vue 3 + Vite + Element Plus</li>
          <li><strong>后端</strong>: Node.js + Express (Mock服务器)</li>
          <li><strong>日历生成</strong>: ics库</li>
        </ul>

        <h3>开发目标</h3>
        <p>实现最小可行产品，核心流程可演示、可交互。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAboutDialog = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { ElMessage } from "element-plus";
import HeroSection from "@/components/home/HeroSection.vue";
import FeaturesSection from "@/components/home/FeaturesSection.vue";
import WorkflowSection from "@/components/home/WorkflowSection.vue";

// 对话框控制
const showAboutDialog = ref(false);

// 显示关于对话框
const showAbout = () => {
  showAboutDialog.value = true;
};

// 显示帮助对话框
const showHelp = () => {
  ElMessage.info("帮助功能开发中");
};

// 显示Mock信息对话框
const showMockInfo = () => {
  ElMessage.info("当前使用Mock数据演示");
};
</script>

<style scoped>
.home-page {
  min-height: 100vh;
}

/* 页脚样式 */
.app-footer {
  background: #1a202c;
  color: white;
  padding: 40px 20px;
  text-align: center;
}

.app-footer p {
  margin-bottom: 16px;
  opacity: 0.9;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 24px;
}

.footer-links .el-button {
  color: white;
}

.footer-links .el-button:hover {
  color: #667eea;
}

/* 关于对话框样式 */
.about-content {
  line-height: 1.6;
}

.about-content h3 {
  color: #1a202c;
  margin: 20px 0 12px 0;
  font-size: 18px;
}

.about-content ul {
  padding-left: 20px;
  margin: 12px 0;
}

.about-content li {
  margin-bottom: 8px;
  color: #4a5568;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer-links {
    flex-direction: column;
    gap: 12px;
  }

  .footer-links .el-button {
    width: 100%;
  }
}
</style>
