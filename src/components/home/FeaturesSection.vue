<template>
  <section class="features-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">✨ 核心功能</h2>
        <p class="section-subtitle">两大AI功能，满足您的日常生活需求</p>
      </div>

      <div class="features-grid">
        <!-- 功能1：AI智能比价 -->
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><ShoppingCart /></el-icon>
          </div>
          <h3 class="feature-title">AI智能比价</h3>
          <p class="feature-description">
            输入您的购物需求，AI分析意图并为您推荐最佳购买方案，支持多平台比价
          </p>
          <ul class="feature-list">
            <li>智能意图分析</li>
            <li>多平台价格对比</li>
            <li>历史价格趋势</li>
            <li>购买建议推荐</li>
          </ul>
          <el-button type="primary" @click="navigateToPrice">
            开始比价
          </el-button>
        </div>

        <!-- 功能2：AI日程规划 -->
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><Calendar /></el-icon>
          </div>
          <h3 class="feature-title">AI日程规划</h3>
          <p class="feature-description">
            描述您的日程需求，AI为您生成完整的日程安排，并导出为日历文件
          </p>
          <ul class="feature-list">
            <li>智能日程生成</li>
            <li>时间冲突检测</li>
            <li>日历文件导出</li>
            <li>多设备同步</li>
          </ul>
          <el-button type="success" @click="navigateToSchedule">
            规划日程
          </el-button>
        </div>

        <!-- 功能3：个人中心 -->
        <div class="feature-card">
          <div class="feature-icon">
            <el-icon><User /></el-icon>
          </div>
          <h3 class="feature-title">个人中心</h3>
          <p class="feature-description">
            管理您的历史记录、个性化设置和使用偏好，获得更好的使用体验
          </p>
          <ul class="feature-list">
            <li>历史记录查看</li>
            <li>个性化设置</li>
            <li>使用偏好配置</li>
            <li>数据统计</li>
          </ul>
          <el-button type="info" @click="navigateToProfile">
            个人中心
          </el-button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ShoppingCart, Calendar, User } from "@element-plus/icons-vue";

const router = useRouter();

// 导航函数
const navigateToPrice = () => {
  router.push("/price");
};

const navigateToSchedule = () => {
  router.push("/schedule");
};

const navigateToProfile = () => {
  router.push("/profile");
};
</script>

<style scoped>
.features-section {
  padding: 80px 20px;
  background: #f7fafc;
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

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 32px;
}

.feature-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.feature-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.feature-icon .el-icon {
  font-size: 36px;
  color: white;
}

.feature-title {
  font-size: 24px;
  font-weight: 600;
  color: #1a202c;
  margin-bottom: 16px;
}

.feature-description {
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 24px;
  flex-grow: 1;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px 0;
  text-align: left;
  width: 100%;
}

.feature-list li {
  padding: 8px 0;
  color: #4a5568;
  position: relative;
  padding-left: 24px;
}

.feature-list li:before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #48bb78;
  font-weight: bold;
}

.feature-card .el-button {
  width: 100%;
  margin-top: auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .features-section {
    padding: 60px 16px;
  }

  .section-title {
    font-size: 28px;
  }

  .section-subtitle {
    font-size: 16px;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 24px;
  }

  .feature-card {
    padding: 24px;
  }

  .feature-icon {
    width: 64px;
    height: 64px;
  }

  .feature-icon .el-icon {
    font-size: 28px;
  }

  .feature-title {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .features-section {
    padding: 40px 12px;
  }

  .section-title {
    font-size: 24px;
  }

  .feature-card {
    padding: 20px;
  }
}
</style>
