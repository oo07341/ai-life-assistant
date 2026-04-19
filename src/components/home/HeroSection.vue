<template>
  <section class="hero-section">
    <div class="hero-content">
      <div class="hero-text">
        <h1 class="hero-title">🤖 喂来日程</h1>
        <p class="hero-subtitle">一点外卖 + 未来日程，一站式生活解决方案</p>
        <p class="hero-description">
          基于AI技术，为您提供智能购物比价和未来日程服务，让生活更简单、更高效
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="navigateToPrice">
            <el-icon><ShoppingCart /></el-icon>
            一点外卖
          </el-button>
          <el-button type="success" size="large" @click="navigateToSchedule">
            <el-icon><Calendar /></el-icon>
            未来规划
          </el-button>
        </div>
      </div>
      <div class="hero-image">
        <div class="image-placeholder">
          <div class="ai-robot">🤖</div>
          <div class="floating-elements">
            <div class="floating-element price">💰</div>
            <div class="floating-element calendar">📅</div>
            <div class="floating-element shopping">🛒</div>
            <div class="floating-element time">⏰</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from "vue-router";
import { ShoppingCart, Calendar } from "@element-plus/icons-vue";

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
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px;
}

.hero-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 40px;
}

.hero-text {
  flex: 1;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 16px;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 20px;
  opacity: 0.9;
  margin-bottom: 20px;
}

.hero-description {
  font-size: 16px;
  opacity: 0.8;
  margin-bottom: 32px;
  line-height: 1.6;
  max-width: 600px;
}

.hero-actions {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-image {
  flex: 1;
  display: flex;
  justify-content: center;
}

.image-placeholder {
  width: 300px;
  height: 300px;
  position: relative;
}

.ai-robot {
  font-size: 120px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: float 3s ease-in-out infinite;
}

.floating-elements {
  position: absolute;
  width: 100%;
  height: 100%;
}

.floating-element {
  position: absolute;
  font-size: 32px;
  animation: float 3s ease-in-out infinite;
  animation-delay: calc(var(--i) * 0.5s);
}

.floating-element.price {
  top: 20%;
  left: 10%;
  --i: 1;
}

.floating-element.calendar {
  top: 10%;
  right: 20%;
  --i: 2;
}

.floating-element.shopping {
  bottom: 20%;
  left: 20%;
  --i: 3;
}

.floating-element.time {
  bottom: 10%;
  right: 10%;
  --i: 4;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-content {
    flex-direction: column;
    text-align: center;
  }

  .hero-title {
    font-size: 36px;
  }

  .hero-subtitle {
    font-size: 18px;
  }

  .hero-description {
    font-size: 14px;
    margin: 0 auto 24px;
  }

  .hero-actions {
    justify-content: center;
  }

  .image-placeholder {
    width: 200px;
    height: 200px;
  }

  .ai-robot {
    font-size: 80px;
  }

  .floating-element {
    font-size: 24px;
  }
}

@media (max-width: 480px) {
  .hero-section {
    padding: 40px 16px;
  }

  .hero-title {
    font-size: 28px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .hero-actions {
    flex-direction: column;
    width: 100%;
  }

  .hero-actions .el-button {
    width: 100%;
  }

  .image-placeholder {
    width: 150px;
    height: 150px;
  }

  .ai-robot {
    font-size: 60px;
  }
}
</style>
