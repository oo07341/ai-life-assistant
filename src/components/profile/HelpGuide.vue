<template>
  <el-card class="help-guide-card" shadow="hover">
    <template #header>
      <div class="card-header">
        <el-icon><QuestionFilled /></el-icon>
        <span>使用帮助</span>
      </div>
    </template>

    <!-- 搜索帮助 -->
    <div class="help-search">
      <el-input
        v-model="searchQuery"
        placeholder="搜索帮助内容..."
        size="large"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <!-- 帮助分类 -->
    <div class="help-categories">
      <el-tabs v-model="activeCategory" type="card" @tab-click="handleTabClick">
        <el-tab-pane label="快速入门" name="quickstart">
          <div class="category-content">
            <h3>喂来日程快速入门</h3>
            <p>
              欢迎使用喂来日程！本应用提供两大核心功能：一点外卖和未来日程。
            </p>

            <div class="feature-section">
              <h4>📊 一点外卖功能</h4>
              <ol>
                <li>在比价页面输入您想查询的商品名称</li>
                <li>选择您关注的电商平台（淘宝、京东、拼多多等）</li>
                <li>点击"一点外卖"按钮</li>
                <li>系统将为您展示各平台的价格对比和优惠信息</li>
                <li>您可以收藏感兴趣的商品或查看历史比价记录</li>
              </ol>
            </div>

            <div class="feature-section">
              <h4>📅 未来日程功能</h4>
              <ol>
                <li>在日程页面输入您的日程安排需求</li>
                <li>例如："下周一上午开会，下午写报告，晚上健身"</li>
                <li>系统将为您生成智能日程安排</li>
                <li>您可以查看日历预览，调整时间安排</li>
                <li>支持导出日程到日历应用</li>
              </ol>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="功能详解" name="features">
          <div class="category-content">
            <h3>功能详细说明</h3>

            <el-collapse v-model="activeFeatures">
              <el-collapse-item title="一点外卖" name="price">
                <div class="feature-detail">
                  <h4>核心特性：</h4>
                  <ul>
                    <li>
                      <strong>多平台比价</strong
                      >：同时查询多个电商平台的价格信息
                    </li>
                    <li>
                      <strong>价格趋势</strong>：查看商品价格的历史变化趋势
                    </li>
                    <li><strong>优惠提醒</strong>：自动识别优惠券和促销活动</li>
                    <li>
                      <strong>收藏功能</strong>：收藏感兴趣的商品，方便后续查看
                    </li>
                    <li><strong>历史记录</strong>：保存您的比价查询记录</li>
                  </ul>

                  <h4>使用技巧：</h4>
                  <ul>
                    <li>使用具体的商品名称可以获得更准确的比价结果</li>
                    <li>关注价格趋势可以帮助您选择最佳购买时机</li>
                    <li>定期查看收藏商品的价格变化</li>
                  </ul>
                </div>
              </el-collapse-item>

              <el-collapse-item title="未来日程" name="schedule">
                <div class="feature-detail">
                  <h4>核心特性：</h4>
                  <ul>
                    <li>
                      <strong>智能解析</strong>：自动解析自然语言描述的日程需求
                    </li>
                    <li><strong>时间优化</strong>：智能安排时间，避免冲突</li>
                    <li>
                      <strong>日历预览</strong>：直观的日历视图展示日程安排
                    </li>
                    <li><strong>提醒设置</strong>：为重要日程设置提醒</li>
                    <li><strong>导出功能</strong>：支持导出到主流日历应用</li>
                  </ul>

                  <h4>使用技巧：</h4>
                  <ul>
                    <li>尽量详细描述您的日程需求</li>
                    <li>可以指定具体的时间段或持续时间</li>
                    <li>使用"重要"、"紧急"等关键词标记优先级</li>
                  </ul>
                </div>
              </el-collapse-item>

              <el-collapse-item title="个人中心" name="profile">
                <div class="feature-detail">
                  <h4>核心特性：</h4>
                  <ul>
                    <li><strong>用户信息</strong>：查看和编辑个人信息</li>
                    <li><strong>系统设置</strong>：个性化应用设置</li>
                    <li><strong>历史记录</strong>：统一查看比价和日程历史</li>
                    <li><strong>使用帮助</strong>：查看应用使用指南</li>
                  </ul>

                  <h4>使用技巧：</h4>
                  <ul>
                    <li>定期清理不需要的历史记录</li>
                    <li>根据个人习惯调整系统设置</li>
                    <li>查看使用帮助解决常见问题</li>
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>

        <el-tab-pane label="常见问题" name="faq">
          <div class="category-content">
            <h3>常见问题解答</h3>

            <el-collapse v-model="activeFaq">
              <el-collapse-item title="比价功能相关问题" name="price-faq">
                <div class="faq-item">
                  <h4>Q: 为什么比价结果有时不准确？</h4>
                  <p>A: 比价结果的准确性受多种因素影响：</p>
                  <ul>
                    <li>商品名称的准确性</li>
                    <li>电商平台数据的实时性</li>
                    <li>促销活动的时效性</li>
                  </ul>
                  <p>建议使用具体的商品型号或链接进行查询。</p>
                </div>

                <div class="faq-item">
                  <h4>Q: 如何获取最新的优惠信息？</h4>
                  <p>A: 系统会定期更新优惠信息，您也可以：</p>
                  <ul>
                    <li>关注商品的价格趋势</li>
                    <li>设置价格提醒</li>
                    <li>定期查看收藏商品</li>
                  </ul>
                </div>
              </el-collapse-item>

              <el-collapse-item title="日程功能相关问题" name="schedule-faq">
                <div class="faq-item">
                  <h4>Q: 日程安排可以调整吗？</h4>
                  <p>A: 是的，您可以：</p>
                  <ul>
                    <li>在日历视图中直接拖拽调整时间</li>
                    <li>编辑日程的详细信息</li>
                    <li>删除不需要的日程安排</li>
                  </ul>
                </div>

                <div class="faq-item">
                  <h4>Q: 如何导出日程到其他日历应用？</h4>
                  <p>A: 在日程详情页面：</p>
                  <ol>
                    <li>点击"导出"按钮</li>
                    <li>选择导出格式（iCal、Google Calendar等）</li>
                    <li>按照提示完成导出操作</li>
                  </ol>
                </div>
              </el-collapse-item>

              <el-collapse-item title="账户和设置问题" name="account-faq">
                <div class="faq-item">
                  <h4>Q: 如何修改个人信息？</h4>
                  <p>A: 在个人中心页面：</p>
                  <ol>
                    <li>点击"编辑信息"按钮</li>
                    <li>修改需要更新的信息</li>
                    <li>点击"保存"按钮</li>
                  </ol>
                </div>

                <div class="faq-item">
                  <h4>Q: 如何清理历史记录？</h4>
                  <p>A: 在历史记录页面：</p>
                  <ul>
                    <li>可以删除单个历史记录</li>
                    <li>支持批量删除选中的记录</li>
                    <li>可以清空所有历史记录</li>
                  </ul>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>

        <el-tab-pane label="联系支持" name="contact">
          <div class="category-content">
            <h3>联系我们</h3>

            <div class="contact-info">
              <div class="contact-item">
                <el-icon><Message /></el-icon>
                <div class="contact-details">
                  <h4>反馈建议</h4>
                  <p>如果您有任何建议或发现了问题，请通过以下方式联系我们：</p>
                  <ul>
                    <li>邮箱：support@ai-life-assistant.com</li>
                    <li>反馈表单：在应用内提交反馈</li>
                  </ul>
                </div>
              </div>

              <div class="contact-item">
                <el-icon><ChatDotRound /></el-icon>
                <div class="contact-details">
                  <h4>技术支持</h4>
                  <p>遇到技术问题？我们的技术支持团队随时为您服务：</p>
                  <ul>
                    <li>工作时间：周一至周五 9:00-18:00</li>
                    <li>响应时间：24小时内</li>
                    <li>优先处理紧急问题</li>
                  </ul>
                </div>
              </div>

              <div class="contact-item">
                <el-icon><Document /></el-icon>
                <div class="contact-details">
                  <h4>文档资源</h4>
                  <p>更多详细的使用文档和教程：</p>
                  <ul>
                    <li>用户手册：完整的使用指南</li>
                    <li>API文档：开发者接口文档</li>
                    <li>更新日志：版本更新记录</li>
                  </ul>
                </div>
              </div>
            </div>

            <div class="feedback-form">
              <h4>快速反馈</h4>
              <el-form :model="feedbackForm" label-width="80px">
                <el-form-item label="反馈类型">
                  <el-select
                    v-model="feedbackForm.type"
                    placeholder="请选择反馈类型"
                  >
                    <el-option label="功能建议" value="suggestion" />
                    <el-option label="问题报告" value="bug" />
                    <el-option label="其他反馈" value="other" />
                  </el-select>
                </el-form-item>

                <el-form-item label="反馈内容">
                  <el-input
                    v-model="feedbackForm.content"
                    type="textarea"
                    :rows="4"
                    placeholder="请详细描述您的反馈内容..."
                    maxlength="500"
                    show-word-limit
                  />
                </el-form-item>

                <el-form-item label="联系方式">
                  <el-input
                    v-model="feedbackForm.contact"
                    placeholder="邮箱或电话（选填）"
                  />
                </el-form-item>

                <el-form-item>
                  <el-button type="primary" @click="submitFeedback">
                    提交反馈
                  </el-button>
                  <el-button @click="resetFeedback"> 重置 </el-button>
                </el-form-item>
              </el-form>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from "vue";
import {
  QuestionFilled,
  Search,
  Message,
  ChatDotRound,
  Document,
} from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";

// 搜索查询
const searchQuery = ref("");

// 活动分类
const activeCategory = ref("quickstart");

// 活动功能折叠面板
const activeFeatures = ref(["price", "schedule", "profile"]);

// 活动FAQ折叠面板
const activeFaq = ref(["price-faq", "schedule-faq", "account-faq"]);

// 反馈表单
const feedbackForm = ref({
  type: "suggestion",
  content: "",
  contact: "",
});

// 处理标签点击
const handleTabClick = (tab) => {
  console.log("切换到分类:", tab.props.name);
};

// 提交反馈
const submitFeedback = () => {
  if (!feedbackForm.value.content.trim()) {
    ElMessage.warning("请填写反馈内容");
    return;
  }

  console.log("提交反馈:", feedbackForm.value);

  // 模拟提交成功
  ElMessage.success("反馈提交成功！感谢您的宝贵意见。");

  // 重置表单
  resetFeedback();
};

// 重置反馈表单
const resetFeedback = () => {
  feedbackForm.value = {
    type: "suggestion",
    content: "",
    contact: "",
  };
};
</script>

<style scoped>
.help-guide-card {
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

/* 搜索区域 */
.help-search {
  margin-bottom: 24px;
}

/* 分类内容 */
.category-content {
  padding: 16px 0;
}

.category-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2d3748;
  font-size: 20px;
}

/* 功能部分 */
.feature-section {
  margin-bottom: 24px;
  padding: 16px;
  background: #f7fafc;
  border-radius: 8px;
  border-left: 4px solid #4299e1;
}

.feature-section h4 {
  margin-top: 0;
  margin-bottom: 12px;
  color: #2d3748;
  font-size: 16px;
}

.feature-section ol,
.feature-section ul {
  margin: 8px 0;
  padding-left: 20px;
}

.feature-section li {
  margin-bottom: 6px;
  line-height: 1.5;
}

/* 功能详情 */
.feature-detail {
  padding: 8px 0;
}

.feature-detail h4 {
  margin: 16px 0 8px 0;
  color: #4a5568;
  font-size: 14px;
}

.feature-detail ul {
  margin: 8px 0;
  padding-left: 20px;
}

.feature-detail li {
  margin-bottom: 6px;
  line-height: 1.5;
}

.feature-detail strong {
  color: #2d3748;
}

/* FAQ项目 */
.faq-item {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.faq-item:last-child {
  border-bottom: none;
}

.faq-item h4 {
  margin-top: 0;
  margin-bottom: 8px;
  color: #2d3748;
  font-size: 14px;
}

.faq-item p {
  margin: 8px 0;
  color: #4a5568;
  line-height: 1.5;
}

/* 联系信息 */
.contact-info {
  margin-bottom: 32px;
}

.contact-item {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 16px;
  background: #f7fafc;
  border-radius: 8px;
}

.contact-item .el-icon {
  font-size: 24px;
  color: #667eea;
  margin-top: 4px;
}

.contact-details h4 {
  margin-top: 0;
  margin-bottom: 8px;
  color: #2d3748;
}

.contact-details p {
  margin: 8px 0;
  color: #4a5568;
  line-height: 1.5;
}

.contact-details ul {
  margin: 8px 0;
  padding-left: 20px;
}

.contact-details li {
  margin-bottom: 4px;
  line-height: 1.5;
}

/* 反馈表单 */
.feedback-form {
  margin-top: 32px;
  padding: 24px;
  background: #f7fafc;
  border-radius: 8px;
}

.feedback-form h4 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #2d3748;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .contact-item {
    flex-direction: column;
    gap: 12px;
  }

  .contact-item .el-icon {
    align-self: flex-start;
  }

  .feature-section {
    padding: 12px;
  }

  .feedback-form {
    padding: 16px;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .help-guide-card {
  background: #2d3748;
  border-color: #4a5568;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .section-title {
  color: #e2e8f0;
}

:global(.dark-theme) .section-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .feature-section {
  background: #4a5568;
  border-color: #718096;
}

:global(.dark-theme) .feature-section h4 {
  color: #e2e8f0;
}

:global(.dark-theme) .feature-section p {
  color: #cbd5e0;
}

:global(.dark-theme) .contact-item {
  border-color: #4a5568;
}

:global(.dark-theme) .contact-item:hover {
  background: #4a5568;
}

:global(.dark-theme) .contact-label {
  color: #e2e8f0;
}

:global(.dark-theme) .contact-value {
  color: #cbd5e0;
}

:global(.dark-theme) .faq-item h4 {
  color: #e2e8f0;
}

:global(.dark-theme) .faq-item p,
:global(.dark-theme) .faq-item li {
  color: #cbd5e0;
}

:global(.dark-theme) .feedback-form {
  background: #4a5568;
  border-color: #718096;
}

:global(.dark-theme) .feedback-form h4 {
  color: #e2e8f0;
}

:global(.dark-theme) .feedback-form p {
  color: #cbd5e0;
}
</style>
