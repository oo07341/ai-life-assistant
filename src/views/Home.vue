<template>
  <div class="home-container">
    <!-- 应用标题 -->
    <header class="app-header">
      <div class="header-content">
        <h1>🤖 AI生活助手</h1>
        <p class="subtitle">智能比价 + 日程规划，一站式生活解决方案</p>
        <div class="header-tags">
          <el-tag type="success" size="large">AI智能分析</el-tag>
          <el-tag type="warning" size="large">全网比价</el-tag>
          <el-tag type="danger" size="large">一键购买</el-tag>
          <el-tag type="info" size="large">日程规划</el-tag>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- Tab切换 -->
      <div class="tabs-container">
        <el-tabs v-model="activeTab" type="border-card" class="main-tabs">
          <el-tab-pane label="🔍 AI智能比价" name="price">
            <PriceComparisonStable
              ref="priceComparisonRef"
              @add-to-schedule="handleAddToSchedule"
            />
          </el-tab-pane>

          <el-tab-pane label="📅 AI日程规划" name="schedule">
            <ScheduleGenerator
              ref="scheduleGeneratorRef"
              :selected-product="selectedProduct"
              :search-query="searchQuery"
            />
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 功能说明 -->
      <div class="features-section">
        <h2>✨ 核心功能</h2>
        <div class="features-grid">
          <el-card class="feature-card">
            <template #header>
              <div class="feature-header">
                <el-icon><MagicStick /></el-icon>
                <span>AI意图分析</span>
              </div>
            </template>
            <p>理解自然语言需求，智能分析用户意图，提取关键词和推荐平台。</p>
          </el-card>

          <el-card class="feature-card">
            <template #header>
              <div class="feature-header">
                <el-icon><TrendCharts /></el-icon>
                <span>全网比价</span>
              </div>
            </template>
            <p>聚合多个平台价格信息，智能排序筛选，自动标识最佳性价比商品。</p>
          </el-card>

          <el-card class="feature-card">
            <template #header>
              <div class="feature-header">
                <el-icon><Phone /></el-icon>
                <span>一键购买</span>
              </div>
            </template>
            <p>直接唤起购物App，2秒超时降级处理，跳转到下载页面。</p>
          </el-card>

          <el-card class="feature-card">
            <template #header>
              <div class="feature-header">
                <el-icon><Calendar /></el-icon>
                <span>日程规划</span>
              </div>
            </template>
            <p>根据比价结果智能规划日程，生成.ics日历文件，支持多平台导入。</p>
          </el-card>
        </div>
      </div>

      <!-- 使用流程 -->
      <div class="workflow-section">
        <h2>📋 使用流程</h2>
        <div class="workflow-steps">
          <div class="step">
            <div class="step-number">1</div>
            <div class="step-content">
              <h3>输入需求</h3>
              <p>在比价页面输入自然语言需求，如"我想吃披萨"</p>
            </div>
          </div>

          <div class="step-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>

          <div class="step">
            <div class="step-number">2</div>
            <div class="step-content">
              <h3>AI分析</h3>
              <p>AI分析意图，推荐关键词和平台</p>
            </div>
          </div>

          <div class="step-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>

          <div class="step">
            <div class="step-number">3</div>
            <div class="step-content">
              <h3>比价展示</h3>
              <p>展示全网比价结果，智能排序筛选</p>
            </div>
          </div>

          <div class="step-arrow">
            <el-icon><ArrowRight /></el-icon>
          </div>

          <div class="step">
            <div class="step-number">4</div>
            <div class="step-content">
              <h3>日程规划</h3>
              <p>智能规划购买时间，生成日历文件</p>
            </div>
          </div>
        </div>
      </div>
    </main>

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
import {
  MagicStick,
  TrendCharts,
  Phone,
  Calendar,
  ArrowRight,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import PriceComparisonStable from "../components/PriceComparison-stable.vue";
import ScheduleGenerator from "../components/ScheduleGenerator.vue";

// 响应式数据
const activeTab = ref("price");
const priceComparisonRef = ref(null);
const scheduleGeneratorRef = ref(null);
const selectedProduct = ref(null);
const searchQuery = ref("");

// 对话框控制
const showAboutDialog = ref(false);
const showHelpDialog = ref(false);
const showMockInfoDialog = ref(false);

// 处理添加到日程事件
const handleAddToSchedule = (event) => {
  selectedProduct.value = event.detail.product;
  searchQuery.value = event.detail.query;

  // 切换到日程规划Tab
  activeTab.value = "schedule";

  ElMessage.success("已切换到日程规划，请点击生成日程按钮");
};

// 显示关于对话框
const showAbout = () => {
  showAboutDialog.value = true;
};

// 显示帮助对话框
const showHelp = () => {
  showHelpDialog.value = true;
  ElMessage.info("帮助功能开发中");
};

// 显示Mock信息对话框
const showMockInfo = () => {
  showMockInfoDialog.value = true;
  ElMessage.info("当前使用Mock数据演示");
};
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 40px 20px;
  text-align: center;
}

.header-content h1 {
  font-size: 36px;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 18px;
  opacity: 0.9;
  margin-bottom: 20px;
}

.header-tags {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin-top: 20px;
}

.main-content {
  flex: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  width: 100%;
}

.tabs-container {
  margin-bottom: 40px;
}

.main-tabs {
  border-radius: 12px;
  overflow: hidden;
}

.features-section {
  margin: 60px 0;
}

.features-section h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 24px;
  margin-top: 20px;
}

.feature-card {
  height: 100%;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.feature-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: bold;
}

.feature-header .el-icon {
  font-size: 20px;
}

.workflow-section {
  margin: 60px 0;
}

.workflow-section h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.workflow-steps {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 30px;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  min-width: 180px;
}

.step-number {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 12px;
}

.step-content h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 8px;
}

.step-content p {
  color: #666;
  font-size: 14px;
}

.step-arrow {
  color: #667eea;
  font-size: 24px;
}

.app-footer {
  background: #f5f7fa;
  padding: 20px;
  text-align: center;
  margin-top: 40px;
}

.app-footer p {
  color: #666;
  margin-bottom: 10px;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.about-content {
  line-height: 1.6;
}

.about-content h3 {
  color: #333;
  margin: 20px 0 10px 0;
  font-size: 18px;
}

.about-content ul {
  padding-left: 20px;
  margin: 10px 0;
}

.about-content li {
  margin-bottom: 8px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content h1 {
    font-size: 28px;
  }

  .subtitle {
    font-size: 16px;
  }

  .header-tags {
    gap: 8px;
  }

  .header-tags .el-tag {
    font-size: 12px;
    padding: 4px 8px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .workflow-steps {
    flex-direction: column;
  }

  .step-arrow {
    transform: rotate(90deg);
    margin: 10px 0;
  }

  .step {
    min-width: 100%;
  }
}

@media (max-width: 480px) {
  .app-header {
    padding: 30px 15px;
  }

  .main-content {
    padding: 20px 15px;
  }

  .features-section h2,
  .workflow-section h2 {
    font-size: 24px;
  }
}
</style>
