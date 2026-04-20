<template>
  <div class="login-page">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>

    <!-- 登录卡片 -->
    <div class="login-container">
      <div class="login-card">
        <!-- Logo和标题 -->
        <div class="login-header">
          <div class="logo">
            <div class="logo-icon">🤖</div>
            <div class="logo-text">
              <h1>喂来日程</h1>
              <p class="logo-subtitle">一点外卖 + 未来日程</p>
            </div>
          </div>
          <h2 class="login-title">欢迎回来</h2>
          <p class="login-subtitle">请登录您的账户继续使用</p>
        </div>

        <!-- 登录表单 -->
        <el-form
          ref="loginFormRef"
          :model="loginForm"
          :rules="loginRules"
          class="login-form"
          @submit.prevent="handleLogin"
        >
          <!-- 邮箱输入 -->
          <el-form-item prop="email">
            <el-input
              v-model="loginForm.email"
              placeholder="请输入邮箱"
              size="large"
              :prefix-icon="Message"
              type="email"
            />
          </el-form-item>

          <!-- 密码输入 -->
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              placeholder="请输入密码"
              size="large"
              :prefix-icon="Lock"
              :type="showPassword ? 'text' : 'password'"
            >
              <template #suffix>
                <el-icon
                  class="password-toggle"
                  @click="showPassword = !showPassword"
                >
                  <View v-if="showPassword" />
                  <Hide v-else />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 记住我和忘记密码 -->
          <div class="form-options">
            <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
            <el-link
              type="primary"
              :underline="false"
              @click="showForgotPassword"
            >
              忘记密码？
            </el-link>
          </div>

          <!-- 登录按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleLogin"
              class="login-button"
            >
              {{ loading ? "登录中..." : "登录" }}
            </el-button>
          </el-form-item>

          <!-- 注册链接 -->
          <div class="register-link">
            <span>还没有账户？</span>
            <el-link type="primary" :underline="false" @click="goToRegister">
              立即注册
            </el-link>
          </div>
        </el-form>

        <!-- 第三方登录 -->
        <div class="social-login">
          <div class="divider">
            <span class="divider-text">或使用以下方式登录</span>
          </div>
          <div class="social-buttons">
            <el-button class="social-button wechat" @click="handleWechatLogin">
              <el-icon><ChatDotRound /></el-icon>
              微信登录
            </el-button>
            <el-button class="social-button github" @click="handleGithubLogin">
              <el-icon><Promotion /></el-icon>
              GitHub登录
            </el-button>
          </div>
        </div>
      </div>

      <!-- 功能展示 -->
      <div class="features-section">
        <h3 class="features-title">为什么选择喂来日程？</h3>
        <div class="features-list">
          <div class="feature-item">
            <el-icon><ShoppingCart /></el-icon>
            <div class="feature-content">
              <h4>智能比价</h4>
              <p>一键比较多个平台价格，找到最优惠的商品</p>
            </div>
          </div>
          <div class="feature-item">
            <el-icon><Calendar /></el-icon>
            <div class="feature-content">
              <h4>未来日程</h4>
              <p>智能解析自然语言，生成个性化日程安排</p>
            </div>
          </div>
          <div class="feature-item">
            <el-icon><User /></el-icon>
            <div class="feature-content">
              <h4>个人中心</h4>
              <p>完整的历史记录和个性化设置</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 忘记密码对话框 -->
    <el-dialog
      v-model="forgotPasswordVisible"
      title="重置密码"
      width="400px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="forgotFormRef"
        :model="forgotForm"
        :rules="forgotRules"
        label-width="80px"
      >
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="forgotForm.email"
            placeholder="请输入注册邮箱"
            :prefix-icon="Message"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="forgotPasswordVisible = false">取消</el-button>
          <el-button type="primary" @click="handleForgotPassword">
            发送重置链接
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import {
  Message,
  Lock,
  View,
  Hide,
  ChatDotRound,
  Promotion,
  ShoppingCart,
  Calendar,
  User,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const router = useRouter();
const loginFormRef = ref();
const forgotFormRef = ref();

// 登录表单
const loginForm = reactive({
  email: "",
  password: "",
  remember: false,
});

// 忘记密码表单
const forgotForm = reactive({
  email: "",
});

// 状态
const loading = ref(false);
const showPassword = ref(false);
const forgotPasswordVisible = ref(false);

// 验证规则
const loginRules = {
  email: [
    { required: true, message: "请输入邮箱地址", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱地址", trigger: "blur" },
  ],
  password: [
    { required: true, message: "请输入密码", trigger: "blur" },
    { min: 6, message: "密码长度不能少于6位", trigger: "blur" },
  ],
};

const forgotRules = {
  email: [
    { required: true, message: "请输入邮箱地址", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱地址", trigger: "blur" },
  ],
};

// 登录处理
const handleLogin = async () => {
  if (!loginFormRef.value) return;

  try {
    await loginFormRef.value.validate();
    loading.value = true;

    // 模拟登录API调用
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 保存用户信息到localStorage
    const userId = "test_user_001"; // 使用固定的测试用户ID，与API服务一致
    const userInfo = {
      id: userId,
      email: loginForm.email,
      username: loginForm.email.split("@")[0],
      isPremium: true,
      registerDate: new Date().toISOString(),
    };

    localStorage.setItem("userInfo", JSON.stringify(userInfo));
    localStorage.setItem("isLoggedIn", "true");
    localStorage.setItem("userId", userId); // 保存userId供API服务使用

    ElMessage.success("登录成功！");

    // 跳转到首页
    router.push("/");
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || "登录失败，请检查邮箱和密码");
    }
  } finally {
    loading.value = false;
  }
};

// 忘记密码
const showForgotPassword = () => {
  forgotPasswordVisible.value = true;
};

const handleForgotPassword = async () => {
  if (!forgotFormRef.value) return;

  try {
    await forgotFormRef.value.validate();

    // 模拟发送重置邮件
    await new Promise((resolve) => setTimeout(resolve, 1000));

    ElMessage.success(`重置链接已发送到 ${forgotForm.email}，请查收邮件`);
    forgotPasswordVisible.value = false;
    forgotForm.email = "";
  } catch (error) {
    // 验证失败，不处理
  }
};

// 第三方登录
const handleWechatLogin = () => {
  ElMessage.info("微信登录功能开发中");
};

const handleGithubLogin = () => {
  ElMessage.info("GitHub登录功能开发中");
};

// 跳转到注册页面
const goToRegister = () => {
  router.push("/register");
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  position: relative;
  overflow: hidden;
}

/* 背景装饰 */
.background-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.circle-1 {
  width: 300px;
  height: 300px;
  top: -150px;
  right: -150px;
}

.circle-2 {
  width: 200px;
  height: 200px;
  bottom: -100px;
  left: -100px;
}

.circle-3 {
  width: 150px;
  height: 150px;
  top: 50%;
  left: 10%;
}

/* 登录容器 */
.login-container {
  display: flex;
  gap: 60px;
  max-width: 1000px;
  width: 100%;
  z-index: 1;
}

/* 登录卡片 */
.login-card {
  flex: 1;
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.logo-icon {
  font-size: 40px;
}

.logo-text h1 {
  font-size: 24px;
  font-weight: 700;
  color: #1a202c;
  margin: 0;
  line-height: 1.2;
}

.logo-subtitle {
  font-size: 14px;
  color: #718096;
  margin: 0;
}

.login-title {
  font-size: 28px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.login-subtitle {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

/* 登录表单 */
.login-form {
  margin-bottom: 32px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.password-toggle {
  cursor: pointer;
  color: #cbd5e0;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #667eea;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.register-link {
  text-align: center;
  margin-top: 24px;
  color: #718096;
}

.register-link span {
  margin-right: 8px;
}

/* 第三方登录 */
.social-login {
  margin-top: 32px;
  padding-top: 32px;
  border-top: 1px solid #e2e8f0;
}

.divider {
  display: flex;
  align-items: center;
  margin-bottom: 24px;
}

.divider::before,
.divider::after {
  content: "";
  flex: 1;
  height: 1px;
  background: #e2e8f0;
}

.divider-text {
  padding: 0 16px;
  color: #a0aec0;
  font-size: 14px;
}

.social-buttons {
  display: flex;
  gap: 16px;
}

.social-button {
  flex: 1;
  height: 44px;
}

.social-button.wechat {
  background: #07c160;
  border-color: #07c160;
  color: white;
}

.social-button.wechat:hover {
  background: #06ad56;
  border-color: #06ad56;
}

.social-button.github {
  background: #24292e;
  border-color: #24292e;
  color: white;
}

.social-button.github:hover {
  background: #1a1e22;
  border-color: #1a1e22;
}

/* 功能展示 */
.features-section {
  flex: 1;
  max-width: 400px;
  color: white;
}

.features-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 32px;
  text-align: center;
}

.features-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.feature-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.feature-item .el-icon {
  font-size: 24px;
  color: #63b3ed;
  flex-shrink: 0;
  margin-top: 4px;
}

.feature-content h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: white;
}

.feature-content p {
  font-size: 14px;
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    flex-direction: column;
    gap: 40px;
  }

  .features-section {
    max-width: 100%;
  }

  .login-card {
    padding: 32px 24px;
  }

  .social-buttons {
    flex-direction: column;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .login-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .logo-text h1 {
  color: #e2e8f0;
}

:global(.dark-theme) .logo-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .login-title {
  color: #e2e8f0;
}

:global(.dark-theme) .login-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .social-login {
  border-top-color: #4a5568;
}

:global(.dark-theme) .divider::before,
:global(.dark-theme) .divider::after {
  background: #4a5568;
}

:global(.dark-theme) .divider-text {
  color: #cbd5e0;
}
</style>
