<template>
  <section class="workflow-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">🚀 使用流程</h2>
        <p class="section-subtitle">简单三步，快速体验AI生活助手</p>
      </div>

      <div class="workflow-steps">
        <!-- 步骤1 -->
        <div class="step">
          <div class="step-number">1</div>
          <div class="step-content">
            <h3 class="step-title">输入需求</h3>
            <p class="step-description">
              在比价页面输入您的购物需求，或在日程页面描述您的日程安排
            </p>
            <div class="step-example">
              <div class="example-bubble">我想吃披萨</div>
              <div class="example-bubble">明天下午开会</div>
            </div>
          </div>
        </div>

        <!-- 步骤2 -->
        <div class="step">
          <div class="step-number">2</div>
          <div class="step-content">
            <h3 class="step-title">AI分析</h3>
            <p class="step-description">
              AI智能分析您的意图，生成比价结果或日程安排
            </p>
            <div class="step-icon">🤖</div>
          </div>
        </div>

        <!-- 步骤3 -->
        <div class="step">
          <div class="step-number">3</div>
          <div class="step-content">
            <h3 class="step-title">查看结果</h3>
            <p class="step-description">
              获取详细的比价推荐或日程安排，可导出使用
            </p>
            <div class="step-actions">
              <el-button type="primary" @click="navigateToPrice">
                开始比价
              </el-button>
              <el-button type="success" @click="navigateToSchedule">
                规划日程
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

// 导航函数
const navigateToPrice = () => {
  router.push("/price");
};

const navigateToSchedule = () => {
  router.push("/schedule");
};
</script>

<style scoped>
.workflow-section {
  padding: 80px 20px;
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 60px;
}

.section-title {
  font-size: 36px;
  font-weight: 700;
  color: #1a202c;
  margin-bottom: 16px;
}

.section-subtitle {
  font-size: 18px;
  color: #4a5568;
  max-width: 600px;
  margin: 0 auto;
}

.workflow-steps {
  display: flex;
  flex-direction: column;
  gap: 40px;
  max-width: 800px;
  margin: 0 auto;
}

.step {
  display: flex;
  align-items: flex-start;
  gap: 24px;
}

.step-number {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: 700;
  flex-shrink: 0;
}

.step-content {
  flex: 1;
}

.step-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 12px;
}

.step-description {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 16px;
}

.step-example {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.example-bubble {
  background: #edf2f7;
  padding: 8px 16px;
  border-radius: 20px;
  color: #4a5568;
  font-size: 14px;
}

.step-icon {
  font-size: 48px;
  text-align: center;
  margin-top: 16px;
}

.step-actions {
  display: flex;
  gap: 12px;
  margin-top: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .workflow-section {
    padding: 60px 16px;
  }

  .section-title {
    font-size: 28px;
  }

  .section-subtitle {
    font-size: 16px;
  }

  .workflow-steps {
    gap: 32px;
  }

  .step {
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 16px;
  }

  .step-number {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }

  .step-title {
    font-size: 20px;
  }

  .step-example {
    justify-content: center;
  }

  .step-actions {
    justify-content: center;
    flex-wrap: wrap;
  }
}

@media (max-width: 480px) {
  .workflow-section {
    padding: 40px 12px;
  }

  .section-title {
    font-size: 24px;
  }

  .step-actions {
    flex-direction: column;
    width: 100%;
  }

  .step-actions .el-button {
    width: 100%;
  }
}
</style>
