<template>
  <div class="register-page">
    <!-- 背景装饰 -->
    <div class="background-decoration">
      <div class="decoration-circle circle-1"></div>
      <div class="decoration-circle circle-2"></div>
      <div class="decoration-circle circle-3"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="register-container">
      <div class="register-card">
        <!-- Logo和标题 -->
        <div class="register-header">
          <div class="logo">
            <div class="logo-icon">🤖</div>
            <div class="logo-text">
              <h1>喂来日程</h1>
              <p class="logo-subtitle">一点外卖 + 未来日程</p>
            </div>
          </div>
          <h2 class="register-title">创建新账户</h2>
          <p class="register-subtitle">加入我们，体验智能生活助手</p>
        </div>

        <!-- 注册表单 -->
        <el-form
          ref="registerFormRef"
          :model="registerForm"
          :rules="registerRules"
          class="register-form"
          @submit.prevent="handleRegister"
        >
          <!-- 用户名 -->
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="请输入用户名"
              size="large"
              :prefix-icon="User"
            />
          </el-form-item>

          <!-- 邮箱 -->
          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              size="large"
              :prefix-icon="Message"
              type="email"
            />
          </el-form-item>

          <!-- 密码 -->
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              placeholder="请输入密码（至少6位）"
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

          <!-- 确认密码 -->
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              placeholder="请再次输入密码"
              size="large"
              :prefix-icon="Lock"
              :type="showConfirmPassword ? 'text' : 'password'"
            >
              <template #suffix>
                <el-icon
                  class="password-toggle"
                  @click="showConfirmPassword = !showConfirmPassword"
                >
                  <View v-if="showConfirmPassword" />
                  <Hide v-else />
                </el-icon>
              </template>
            </el-input>
          </el-form-item>

          <!-- 用户协议 -->
          <div class="agreement-section">
            <el-checkbox v-model="registerForm.agreed">
              我已阅读并同意
              <el-link type="primary" :underline="false" @click="showTerms">
                《用户协议》
              </el-link>
              和
              <el-link type="primary" :underline="false" @click="showPrivacy">
                《隐私政策》
              </el-link>
            </el-checkbox>
          </div>

          <!-- 注册按钮 -->
          <el-form-item>
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleRegister"
              class="register-button"
            >
              {{ loading ? "注册中..." : "立即注册" }}
            </el-button>
          </el-form-item>

          <!-- 登录链接 -->
          <div class="login-link">
            <span>已有账户？</span>
            <el-link type="primary" :underline="false" @click="goToLogin">
              立即登录
            </el-link>
          </div>
        </el-form>

        <!-- 快速注册 -->
        <div class="quick-register">
          <div class="divider">
            <span class="divider-text">快速注册</span>
          </div>
          <div class="social-buttons">
            <el-button
              class="social-button wechat"
              @click="handleWechatRegister"
            >
              <el-icon><ChatDotRound /></el-icon>
              微信注册
            </el-button>
            <el-button
              class="social-button github"
              @click="handleGithubRegister"
            >
              <el-icon><Promotion /></el-icon>
              GitHub注册
            </el-button>
          </div>
        </div>
      </div>

      <!-- 功能优势 -->
      <div class="benefits-section">
        <h3 class="benefits-title">注册即可享受</h3>
        <div class="benefits-list">
          <div class="benefit-item">
            <div class="benefit-icon">
              <el-icon><Star /></el-icon>
            </div>
            <div class="benefit-content">
              <h4>免费高级功能</h4>
              <p>新用户注册即可享受30天高级会员特权</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <el-icon><DataLine /></el-icon>
            </div>
            <div class="benefit-content">
              <h4>个性化推荐</h4>
              <p>根据您的使用习惯提供个性化建议</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <el-icon><UploadFilled /></el-icon>
            </div>
            <div class="benefit-content">
              <h4>云端同步</h4>
              <p>多设备数据同步，随时随地访问</p>
            </div>
          </div>
          <div class="benefit-item">
            <div class="benefit-icon">
              <el-icon><Headset /></el-icon>
            </div>
            <div class="benefit-content">
              <h4>专属支持</h4>
              <p>优先技术支持和使用指导</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 用户协议对话框 -->
    <el-dialog
      v-model="termsVisible"
      title="用户协议"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="terms-content">
        <h4>喂来日程用户协议</h4>
        <p>欢迎使用喂来日程！请仔细阅读以下协议内容：</p>
        <ol>
          <li>您同意遵守相关法律法规和本协议条款</li>
          <li>您承诺提供真实、准确、完整的注册信息</li>
          <li>您对账户安全负有全部责任</li>
          <li>我们承诺保护您的个人信息安全</li>
          <li>本协议可能会不时更新，请定期查看</li>
        </ol>
        <p>详细协议内容请访问我们的官方网站。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="termsVisible = false">关闭</el-button>
          <el-button type="primary" @click="acceptTerms">
            我已阅读并同意
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 隐私政策对话框 -->
    <el-dialog
      v-model="privacyVisible"
      title="隐私政策"
      width="600px"
      :close-on-click-modal="false"
    >
      <div class="privacy-content">
        <h4>喂来日程隐私政策</h4>
        <p>我们高度重视您的隐私保护：</p>
        <ol>
          <li>我们仅收集必要的个人信息以提供服务</li>
          <li>您的数据将受到严格的安全保护</li>
          <li>我们不会向第三方出售或共享您的个人信息</li>
          <li>您有权访问、修改或删除您的个人信息</li>
          <li>我们使用加密技术保护数据传输安全</li>
        </ol>
        <p>详细隐私政策请访问我们的官方网站。</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="privacyVisible = false">关闭</el-button>
          <el-button type="primary" @click="acceptPrivacy">
            我已阅读并同意
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import { useRouter } from "vue-router";
import {
  User,
  Message,
  Lock,
  View,
  Hide,
  ChatDotRound,
  Promotion,
  Star,
  DataLine,
  UploadFilled,
  Headset,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

const router = useRouter();
const registerFormRef = ref();

// 注册表单
const registerForm = reactive({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
  agreed: false,
});

// 状态
const loading = ref(false);
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const termsVisible = ref(false);
const privacyVisible = ref(false);

// 验证规则
const validateUsername = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请输入用户名"));
  } else if (value.length < 3) {
    callback(new Error("用户名长度不能少于3位"));
  } else if (value.length > 20) {
    callback(new Error("用户名长度不能超过20位"));
  } else {
    callback();
  }
};

const validatePassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请输入密码"));
  } else if (value.length < 6) {
    callback(new Error("密码长度不能少于6位"));
  } else {
    callback();
  }
};

const validateConfirmPassword = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请再次输入密码"));
  } else if (value !== registerForm.password) {
    callback(new Error("两次输入的密码不一致"));
  } else {
    callback();
  }
};

const validateAgreement = (rule, value, callback) => {
  if (!value) {
    callback(new Error("请同意用户协议和隐私政策"));
  } else {
    callback();
  }
};

const registerRules = {
  username: [{ required: true, validator: validateUsername, trigger: "blur" }],
  email: [
    { required: true, message: "请输入邮箱地址", trigger: "blur" },
    { type: "email", message: "请输入正确的邮箱地址", trigger: "blur" },
  ],
  password: [{ required: true, validator: validatePassword, trigger: "blur" }],
  confirmPassword: [
    { required: true, validator: validateConfirmPassword, trigger: "blur" },
  ],
  agreed: [{ required: true, validator: validateAgreement, trigger: "change" }],
};

// 注册处理
const handleRegister = async () => {
  if (!registerFormRef.value) return;

  try {
    await registerFormRef.value.validate();
    loading.value = true;

    // 模拟注册API调用
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // 保存用户信息到localStorage
    const userInfo = {
      id: "user_" + Date.now(),
      username: registerForm.username,
      email: registerForm.email,
      isPremium: true,
      registerDate: new Date().toISOString(),
      isNewUser: true,
    };

    localStorage.setItem("userInfo", JSON.stringify(userInfo));
    localStorage.setItem("isLoggedIn", "true");

    ElMessage.success("注册成功！欢迎使用喂来日程");

    // 跳转到首页
    router.push("/");
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || "注册失败，请稍后重试");
    }
  } finally {
    loading.value = false;
  }
};

// 显示协议
const showTerms = () => {
  termsVisible.value = true;
};

const showPrivacy = () => {
  privacyVisible.value = true;
};

// 同意协议
const acceptTerms = () => {
  registerForm.agreed = true;
  termsVisible.value = false;
  ElMessage.success("已同意用户协议");
};

const acceptPrivacy = () => {
  registerForm.agreed = true;
  privacyVisible.value = false;
  ElMessage.success("已同意隐私政策");
};

// 第三方注册
const handleWechatRegister = () => {
  ElMessage.info("微信注册功能开发中");
};

const handleGithubRegister = () => {
  ElMessage.info("GitHub注册功能开发中");
};

// 跳转到登录页面
const goToLogin = () => {
  router.push("/login");
};

// 监听密码变化，实时验证确认密码
watch(
  () => registerForm.password,
  () => {
    if (registerForm.confirmPassword) {
      registerFormRef.value?.validateField("confirmPassword");
    }
  },
);
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #48bb78 0%, #4299e1 100%);
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
  width: 400px;
  height: 400px;
  top: -200px;
  left: -200px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  right: -150px;
}

.circle-3 {
  width: 200px;
  height: 200px;
  top: 20%;
  right: 10%;
}

/* 注册容器 */
.register-container {
  display: flex;
  gap: 60px;
  max-width: 1100px;
  width: 100%;
  z-index: 1;
}

/* 注册卡片 */
.register-card {
  flex: 1;
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.register-header {
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

.register-title {
  font-size: 28px;
  font-weight: 600;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.register-subtitle {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

/* 注册表单 */
.register-form {
  margin-bottom: 32px;
}

.agreement-section {
  margin: 24px 0 32px 0;
}

.agreement-section .el-checkbox {
  display: flex;
  align-items: flex-start;
}

.agreement-section .el-link {
  margin: 0 4px;
}

.password-toggle {
  cursor: pointer;
  color: #cbd5e0;
  transition: color 0.2s;
}

.password-toggle:hover {
  color: #4299e1;
}

.register-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 500;
}

.login-link {
  text-align: center;
  margin-top: 24px;
  color: #718096;
}

.login-link span {
  margin-right: 8px;
}

/* 快速注册 */
.quick-register {
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

/* 功能优势 */
.benefits-section {
  flex: 1;
  max-width: 450px;
  color: white;
}

.benefits-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 32px;
  text-align: center;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.benefit-item {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}

.benefit-icon {
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
}

.benefit-icon .el-icon {
  font-size: 24px;
  color: #63b3ed;
}

.benefit-content h4 {
  font-size: 18px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: white;
}

.benefit-content p {
  font-size: 14px;
  margin: 0;
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.5;
}

/* 协议内容 */
.terms-content,
.privacy-content {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
}

.terms-content h4,
.privacy-content h4 {
  margin-top: 0;
  color: #2d3748;
}

.terms-content ol,
.privacy-content ol {
  margin: 16px 0;
  padding-left: 20px;
}

.terms-content li,
.privacy-content li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.terms-content p,
.privacy-content p {
  margin: 16px 0;
  color: #4a5568;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    flex-direction: column;
    gap: 40px;
  }

  .benefits-section {
    max-width: 100%;
  }

  .register-card {
    padding: 32px 24px;
  }

  .social-buttons {
    flex-direction: column;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .register-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .logo-text h1 {
  color: #e2e8f0;
}

:global(.dark-theme) .logo-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .register-title {
  color: #e2e8f0;
}

:global(.dark-theme) .register-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .quick-register {
  border-top-color: #4a5568;
}

:global(.dark-theme) .divider::before,
:global(.dark-theme) .divider::after {
  background: #4a5568;
}

:global(.dark-theme) .divider-text {
  color: #cbd5e0;
}

:global(.dark-theme) .terms-content h4,
:global(.dark-theme) .privacy-content h4 {
  color: #e2e8f0;
}

:global(.dark-theme) .terms-content p,
:global(.dark-theme) .privacy-content p {
  color: #cbd5e0;
}

:global(.dark-theme) .terms-content li,
:global(.dark-theme) .privacy-content li {
  color: #cbd5e0;
}
</style>
