<template>
  <div class="plans-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">计划管理</h1>
      <p class="page-subtitle">创建、查看和管理您的日程计划</p>
    </div>

    <!-- 创建新计划卡片 -->
    <el-card class="create-plan-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Plus /></el-icon>
          <span>创建新计划</span>
        </div>
      </template>

      <div class="create-plan-form">
        <el-form
          ref="createPlanFormRef"
          :model="createPlanForm"
          :rules="createPlanRules"
          label-width="100px"
        >
          <el-form-item label="计划目标" prop="goal">
            <el-input
              v-model="createPlanForm.goal"
              placeholder="请输入您的计划目标，例如：学习Vue 3"
              :rows="2"
              type="textarea"
              maxlength="200"
              show-word-limit
            />
          </el-form-item>

          <el-form-item label="目标日期" prop="targetDate">
            <el-date-picker
              v-model="createPlanForm.targetDate"
              type="date"
              placeholder="选择目标完成日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
            />
          </el-form-item>

          <el-form-item label="时间安排" prop="timeSlots">
            <div class="time-slots-container">
              <div
                class="time-slot-item"
                v-for="(slot, index) in createPlanForm.timeSlots"
                :key="index"
              >
                <el-time-select
                  v-model="slot.startTime"
                  placeholder="开始时间"
                  :start="startTimeOptions.start"
                  :step="startTimeOptions.step"
                  :end="startTimeOptions.end"
                  style="width: 120px; margin-right: 8px"
                />
                <span class="time-separator">至</span>
                <el-time-select
                  v-model="slot.endTime"
                  placeholder="结束时间"
                  :start="endTimeOptions.start"
                  :step="endTimeOptions.step"
                  :end="endTimeOptions.end"
                  :min-time="slot.startTime"
                  style="width: 120px; margin-left: 8px"
                />
                <el-button
                  type="danger"
                  :icon="Minus"
                  circle
                  size="small"
                  @click="removeTimeSlot(index)"
                  style="margin-left: 12px"
                  v-if="createPlanForm.timeSlots.length > 1"
                />
              </div>
              <el-button
                type="primary"
                :icon="Plus"
                link
                @click="addTimeSlot"
                style="margin-top: 8px"
              >
                添加时间段
              </el-button>
            </div>
          </el-form-item>

          <el-form-item label="重复设置" prop="repeat">
            <el-select
              v-model="createPlanForm.repeat"
              placeholder="选择重复模式"
            >
              <el-option label="不重复" value="none" />
              <el-option label="每天" value="daily" />
              <el-option label="每周" value="weekly" />
              <el-option label="每月" value="monthly" />
            </el-select>
          </el-form-item>

          <el-form-item label="优先级" prop="priority">
            <el-rate
              v-model="createPlanForm.priority"
              :max="3"
              :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
              show-text
              :texts="['低', '中', '高']"
            />
          </el-form-item>

          <el-form-item label="备注" prop="notes">
            <el-input
              v-model="createPlanForm.notes"
              placeholder="可选：添加计划备注"
              type="textarea"
              :rows="2"
              maxlength="500"
              show-word-limit
            />
          </el-form-item>

          <el-form-item>
            <el-button
              type="primary"
              @click="handleCreatePlan"
              :loading="creatingPlan"
            >
              {{ creatingPlan ? "创建中..." : "创建计划" }}
            </el-button>
            <el-button @click="resetCreateForm">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-card>

    <!-- 计划列表 -->
    <div class="plans-section">
      <div class="section-header">
        <h2 class="section-title">我的计划</h2>
        <div class="section-actions">
          <el-input
            v-model="searchQuery"
            placeholder="搜索计划..."
            style="width: 200px; margin-right: 12px"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <el-select
            v-model="filterStatus"
            placeholder="状态筛选"
            style="width: 120px"
          >
            <el-option label="全部" value="all" />
            <el-option label="进行中" value="active" />
            <el-option label="已完成" value="completed" />
            <el-option label="已过期" value="expired" />
          </el-select>
        </div>
      </div>

      <!-- 计划列表 -->
      <div class="plans-list">
        <div v-if="filteredPlans.length === 0" class="empty-plans">
          <el-empty description="暂无计划" />
          <p class="empty-hint">点击上方"创建新计划"开始您的第一个计划</p>
        </div>

        <div v-else class="plans-grid">
          <el-card
            v-for="plan in filteredPlans"
            :key="plan.id"
            class="plan-card"
            :class="{ 'active-plan': plan.isActive }"
            shadow="hover"
          >
            <template #header>
              <div class="plan-header">
                <div class="plan-title-section">
                  <h3 class="plan-title">{{ plan.goal }}</h3>
                  <el-tag
                    :type="getStatusTagType(plan.status)"
                    size="small"
                    class="plan-status"
                  >
                    {{ getStatusText(plan.status) }}
                  </el-tag>
                  <el-tag
                    v-if="plan.isActive"
                    type="success"
                    size="small"
                    class="active-tag"
                  >
                    当前激活
                  </el-tag>
                </div>
                <div class="plan-actions">
                  <el-dropdown @command="handlePlanCommand(plan.id, $event)">
                    <el-button
                      type="primary"
                      :icon="More"
                      circle
                      size="small"
                    />
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="view">
                          <el-icon><View /></el-icon>
                          查看详情
                        </el-dropdown-item>
                        <el-dropdown-item command="edit">
                          <el-icon><Edit /></el-icon>
                          编辑计划
                        </el-dropdown-item>
                        <el-dropdown-item
                          command="toggleActive"
                          v-if="!plan.isActive"
                        >
                          <el-icon><Check /></el-icon>
                          设为激活
                        </el-dropdown-item>
                        <el-dropdown-item
                          command="complete"
                          v-if="plan.status === 'active'"
                        >
                          <el-icon><Finished /></el-icon>
                          标记完成
                        </el-dropdown-item>
                        <el-dropdown-item divided command="delete">
                          <el-icon><Delete /></el-icon>
                          删除计划
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </div>
              </div>
            </template>

            <div class="plan-content">
              <!-- 计划信息 -->
              <div class="plan-info">
                <div class="info-item">
                  <el-icon><Calendar /></el-icon>
                  <span class="info-label">目标日期：</span>
                  <span class="info-value">{{ plan.targetDate }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Clock /></el-icon>
                  <span class="info-label">时间安排：</span>
                  <span class="info-value">{{ plan.timeSlots }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Refresh /></el-icon>
                  <span class="info-label">重复：</span>
                  <span class="info-value">{{
                    getRepeatText(plan.repeat)
                  }}</span>
                </div>
                <div class="info-item">
                  <el-icon><Flag /></el-icon>
                  <span class="info-label">优先级：</span>
                  <el-rate
                    :model-value="plan.priority"
                    disabled
                    :max="3"
                    :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
                    size="small"
                  />
                </div>
              </div>

              <!-- 进度条 -->
              <div class="plan-progress">
                <div class="progress-header">
                  <span class="progress-label">完成进度</span>
                  <span class="progress-percentage">{{ plan.progress }}%</span>
                </div>
                <el-progress
                  :percentage="plan.progress"
                  :color="getProgressColor(plan.progress)"
                  :show-text="false"
                />
              </div>

              <!-- 备注 -->
              <div class="plan-notes" v-if="plan.notes">
                <el-icon><Document /></el-icon>
                <span class="notes-label">备注：</span>
                <span class="notes-content">{{ plan.notes }}</span>
              </div>

              <!-- 创建时间 -->
              <div class="plan-meta">
                <span class="meta-item">
                  <el-icon><Timer /></el-icon>
                  创建于：{{ plan.createdAt }}
                </span>
                <span class="meta-item" v-if="plan.completedAt">
                  <el-icon><Finished /></el-icon>
                  完成于：{{ plan.completedAt }}
                </span>
              </div>
            </div>
          </el-card>
        </div>
      </div>
    </div>

    <!-- 计划详情对话框 -->
    <el-dialog
      v-model="planDetailVisible"
      :title="selectedPlan ? selectedPlan.goal : '计划详情'"
      width="600px"
    >
      <div v-if="selectedPlan" class="plan-detail">
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="detail-label">目标：</span>
              <span class="detail-value">{{ selectedPlan.goal }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">目标日期：</span>
              <span class="detail-value">{{ selectedPlan.targetDate }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">时间安排：</span>
              <span class="detail-value">{{ selectedPlan.timeSlots }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">重复：</span>
              <span class="detail-value">{{
                getRepeatText(selectedPlan.repeat)
              }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">优先级：</span>
              <el-rate
                :model-value="selectedPlan.priority"
                disabled
                :max="3"
                :colors="['#99A9BF', '#F7BA2A', '#FF9900']"
              />
            </div>
            <div class="detail-item">
              <span class="detail-label">状态：</span>
              <el-tag
                :type="getStatusTagType(selectedPlan.status)"
                size="small"
              >
                {{ getStatusText(selectedPlan.status) }}
              </el-tag>
            </div>
          </div>
        </div>

        <div class="detail-section" v-if="selectedPlan.notes">
          <h4>备注</h4>
          <p class="detail-notes">{{ selectedPlan.notes }}</p>
        </div>

        <div class="detail-section">
          <h4>进度跟踪</h4>
          <div class="progress-detail">
            <el-progress
              :percentage="selectedPlan.progress"
              :color="getProgressColor(selectedPlan.progress)"
              style="margin-bottom: 16px"
            />
            <div class="progress-stats">
              <div class="stat-item">
                <span class="stat-label">已进行：</span>
                <span class="stat-value"
                  >{{ selectedPlan.daysElapsed }} 天</span
                >
              </div>
              <div class="stat-item">
                <span class="stat-label">剩余：</span>
                <span class="stat-value"
                  >{{ selectedPlan.daysRemaining }} 天</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="planDetailVisible = false">关闭</el-button>
          <el-button type="primary" @click="handleEditPlan(selectedPlan)">
            编辑计划
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  Plus,
  Minus,
  Search,
  More,
  View,
  Edit,
  Check,
  Finished,
  Delete,
  Calendar,
  Clock,
  Refresh,
  Flag,
  Document,
  Timer,
} from "@element-plus/icons-vue";
import { userAPI, planAPI, scheduleAPI } from "@/services/api";

// 创建计划表单
const createPlanFormRef = ref();
const createPlanForm = reactive({
  goal: "",
  targetDate: "",
  timeSlots: [{ startTime: "09:00", endTime: "12:00" }],
  repeat: "none",
  priority: 2,
  notes: "",
});

const creatingPlan = ref(false);

// 时间选择器选项
const startTimeOptions = {
  start: "08:00",
  step: "00:30",
  end: "22:00",
};

const endTimeOptions = {
  start: "08:30",
  step: "00:30",
  end: "23:00",
};

// 验证规则
const createPlanRules = {
  goal: [
    { required: true, message: "请输入计划目标", trigger: "blur" },
    { min: 3, message: "目标描述至少3个字符", trigger: "blur" },
  ],
  targetDate: [
    { required: true, message: "请选择目标日期", trigger: "change" },
  ],
};

// 搜索和筛选
const searchQuery = ref("");
const filterStatus = ref("all");

// 加载状态
const loading = ref(true);

// 计划列表数据
const plans = ref([]);

// 加载计划数据
const loadPlans = async () => {
  loading.value = true;
  try {
    // 从后端API获取计划列表
    const response = await userAPI.getPlans();

    // API返回的是 { plans: [] } 格式
    const plansData = response.plans || [];

    // 转换数据格式以匹配前端
    plans.value = plansData.map((plan) => ({
      id: plan.plan_id || plan.id,
      goal: plan.goal || "未命名计划",
      targetDate:
        plan.schedule_info?.target_date ||
        plan.target_date ||
        new Date().toISOString().split("T")[0],
      timeSlots: "09:00-12:00", // 默认值，实际应该从schedule中获取
      repeat: "none", // 默认值
      priority: 2, // 默认值
      status: plan.completed_dates?.length > 0 ? "completed" : "active",
      progress: plan.completed_dates?.length > 0 ? 100 : 0,
      notes: plan.notes || "",
      createdAt: plan.created_at || new Date().toISOString().split("T")[0],
      completedAt:
        plan.completed_dates?.length > 0
          ? plan.completed_dates[plan.completed_dates.length - 1]
          : null,
      isActive: plan.is_active || false,
      daysElapsed: plan.days_elapsed || 0,
      daysRemaining: plan.days_remaining || 0,
    }));

    // 如果没有数据，显示空状态，不显示演示数据
    if (plans.value.length === 0) {
      // 不显示演示数据，让用户创建自己的计划
      console.log("用户暂无计划，显示空状态");
    }
  } catch (error) {
    console.error("加载计划数据失败:", error);

    // 提供更详细的错误信息
    let errorMessage = "加载计划数据失败，请稍后重试";
    if (error.message && error.message.includes("Failed to fetch")) {
      errorMessage = "无法连接到服务器，请检查后端服务是否运行";
    } else if (error.message && error.message.includes("NetworkError")) {
      errorMessage = "网络连接失败，请检查网络设置";
    } else if (error.message && error.message.includes("timeout")) {
      errorMessage = "请求超时，服务器响应过慢";
    } else if (
      (error.message && error.message.includes("401")) ||
      error.message.includes("未授权")
    ) {
      errorMessage = "请先登录以查看计划数据";
    }

    ElMessage.error(errorMessage);

    // 只有在API完全失败时才显示演示数据
    if (error.message && error.message.includes("Failed to fetch")) {
      // 使用模拟数据作为后备
      plans.value = [
        {
          id: "1",
          goal: "学习Vue 3和Composition API",
          targetDate: "2026-05-15",
          timeSlots: "09:00-12:00, 14:00-17:00",
          repeat: "daily",
          priority: 3,
          status: "active",
          progress: 65,
          notes: "重点学习响应式系统和组合式函数",
          createdAt: "2026-04-10",
          completedAt: null,
          isActive: true,
          daysElapsed: 10,
          daysRemaining: 25,
        },
        {
          id: "2",
          goal: "完成健身计划",
          targetDate: "2026-06-30",
          timeSlots: "18:00-19:30",
          repeat: "weekly",
          priority: 2,
          status: "active",
          progress: 40,
          notes: "每周三次力量训练，两次有氧运动",
          createdAt: "2026-04-01",
          completedAt: null,
          isActive: false,
          daysElapsed: 19,
          daysRemaining: 71,
        },
      ];

      // 添加一个提示，告诉用户这是演示数据
      setTimeout(() => {
        ElMessage.info("当前显示的是演示数据，真实数据将在后端服务正常后显示");
      }, 500);
    }
  } finally {
    loading.value = false;
  }
};

// 对话框状态
const planDetailVisible = ref(false);
const selectedPlan = ref(null);

// 计算属性：筛选后的计划
const filteredPlans = computed(() => {
  let filtered = plans.value;

  // 搜索筛选
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (plan) =>
        plan.goal.toLowerCase().includes(query) ||
        plan.notes?.toLowerCase().includes(query),
    );
  }

  // 状态筛选
  if (filterStatus.value !== "all") {
    filtered = filtered.filter((plan) => plan.status === filterStatus.value);
  }

  return filtered;
});

// 添加时间段
const addTimeSlot = () => {
  createPlanForm.timeSlots.push({
    startTime: "09:00",
    endTime: "12:00",
  });
};

// 移除时间段
const removeTimeSlot = (index) => {
  if (createPlanForm.timeSlots.length > 1) {
    createPlanForm.timeSlots.splice(index, 1);
  }
};

// 创建计划
const handleCreatePlan = async () => {
  if (!createPlanFormRef.value) return;

  try {
    await createPlanFormRef.value.validate();
    creatingPlan.value = true;

    // 模拟API调用
    await new Promise((resolve) => setTimeout(resolve, 1500));

    // 格式化时间安排
    const timeSlotsStr = createPlanForm.timeSlots
      .map((slot) => `${slot.startTime}-${slot.endTime}`)
      .join(", ");

    // 创建新计划
    const newPlan = {
      id: "plan_" + Date.now(),
      goal: createPlanForm.goal,
      targetDate: createPlanForm.targetDate,
      timeSlots: timeSlotsStr,
      repeat: createPlanForm.repeat,
      priority: createPlanForm.priority,
      status: "active",
      progress: 0,
      notes: createPlanForm.notes,
      createdAt: new Date().toISOString().split("T")[0],
      completedAt: null,
      isActive: false,
      daysElapsed: 0,
      daysRemaining: Math.ceil(
        (new Date(createPlanForm.targetDate) - new Date()) /
          (1000 * 60 * 60 * 24),
      ),
    };

    // 添加到计划列表
    plans.value.unshift(newPlan);

    ElMessage.success("计划创建成功！");

    // 重置表单
    resetCreateForm();
  } catch (error) {
    if (error instanceof Error) {
      ElMessage.error(error.message || "创建计划失败");
    }
  } finally {
    creatingPlan.value = false;
  }
};

// 重置创建表单
const resetCreateForm = () => {
  createPlanForm.goal = "";
  createPlanForm.targetDate = "";
  createPlanForm.timeSlots = [{ startTime: "09:00", endTime: "12:00" }];
  createPlanForm.repeat = "none";
  createPlanForm.priority = 2;
  createPlanForm.notes = "";
};

// 计划操作
const handlePlanCommand = (planId, command) => {
  const planIndex = plans.value.findIndex((p) => p.id === planId);
  if (planIndex === -1) return;

  const plan = plans.value[planIndex];

  switch (command) {
    case "view":
      selectedPlan.value = { ...plan };
      planDetailVisible.value = true;
      break;
    case "edit":
      handleEditPlan(plan);
      break;
    case "toggleActive":
      toggleActivePlan(planId);
      break;
    case "complete":
      completePlan(planId);
      break;
    case "delete":
      deletePlan(planId);
      break;
  }
};

// 编辑计划
const handleEditPlan = (plan) => {
  ElMessage.info("编辑功能开发中");
  // 这里可以打开编辑对话框
};

// 切换激活状态
const toggleActivePlan = (planId) => {
  plans.value.forEach((plan) => {
    plan.isActive = plan.id === planId;
  });
  ElMessage.success("已切换激活计划");
};

// 完成计划
const completePlan = (planId) => {
  const planIndex = plans.value.findIndex((p) => p.id === planId);
  if (planIndex !== -1) {
    plans.value[planIndex].status = "completed";
    plans.value[planIndex].progress = 100;
    plans.value[planIndex].completedAt = new Date().toISOString().split("T")[0];
    ElMessage.success("计划已完成！");
  }
};

// 删除计划
const deletePlan = (planId) => {
  ElMessageBox.confirm("确定要删除这个计划吗？此操作不可恢复。", "删除确认", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  })
    .then(() => {
      const planIndex = plans.value.findIndex((p) => p.id === planId);
      if (planIndex !== -1) {
        plans.value.splice(planIndex, 1);
        ElMessage.success("计划已删除");
      }
    })
    .catch(() => {
      // 用户取消
    });
};

// 获取状态标签类型
const getStatusTagType = (status) => {
  switch (status) {
    case "active":
      return "primary";
    case "completed":
      return "success";
    case "expired":
      return "danger";
    default:
      return "info";
  }
};

// 获取状态文本
const getStatusText = (status) => {
  switch (status) {
    case "active":
      return "进行中";
    case "completed":
      return "已完成";
    case "expired":
      return "已过期";
    default:
      return "未知";
  }
};

// 获取重复模式文本
const getRepeatText = (repeat) => {
  switch (repeat) {
    case "none":
      return "不重复";
    case "daily":
      return "每天";
    case "weekly":
      return "每周";
    case "monthly":
      return "每月";
    default:
      return repeat;
  }
};

// 获取进度条颜色
const getProgressColor = (progress) => {
  if (progress < 30) return "#F56C6C";
  if (progress < 70) return "#E6A23C";
  return "#67C23A";
};

// 页面加载时初始化
onMounted(() => {
  loadPlans();
});
</script>

<style scoped>
.plans-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px 20px;
}

/* 页面标题 */
.page-header {
  margin-bottom: 32px;
  text-align: center;
}

.page-title {
  font-size: 32px;
  font-weight: 700;
  color: #1a202c;
  margin: 0 0 8px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #718096;
  margin: 0;
}

/* 创建计划卡片 */
.create-plan-card {
  margin-bottom: 40px;
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

.create-plan-form {
  padding: 8px 0;
}

.time-slots-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.time-slot-item {
  display: flex;
  align-items: center;
}

.time-separator {
  margin: 0 8px;
  color: #909399;
}

/* 计划列表区域 */
.plans-section {
  margin-top: 40px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-title {
  font-size: 24px;
  font-weight: 600;
  color: #2d3748;
  margin: 0;
}

.section-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 计划列表 */
.plans-list {
  min-height: 400px;
}

.empty-plans {
  text-align: center;
  padding: 60px 0;
}

.empty-hint {
  margin-top: 16px;
  color: #718096;
  font-size: 14px;
}

.plans-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
}

.plan-card {
  transition: all 0.3s;
}

.plan-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.plan-card.active-plan {
  border: 2px solid #67c23a;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.plan-title-section {
  flex: 1;
  min-width: 0;
}

.plan-title {
  font-size: 18px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.plan-status {
  margin-right: 8px;
}

.active-tag {
  margin-left: 8px;
}

.plan-actions {
  flex-shrink: 0;
}

/* 计划内容 */
.plan-content {
  padding: 8px 0;
}

.plan-info {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
}

.info-item .el-icon {
  color: #909399;
  font-size: 16px;
}

.info-label {
  color: #606266;
  font-weight: 500;
}

.info-value {
  color: #303133;
}

/* 进度条 */
.plan-progress {
  margin-bottom: 20px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-label {
  font-size: 14px;
  color: #606266;
}

.progress-percentage {
  font-size: 14px;
  font-weight: 600;
  color: #409eff;
}

/* 备注 */
.plan-notes {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 16px;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
  font-size: 14px;
}

.plan-notes .el-icon {
  color: #909399;
  margin-top: 2px;
  flex-shrink: 0;
}

.notes-label {
  color: #606266;
  font-weight: 500;
  flex-shrink: 0;
}

.notes-content {
  color: #303133;
  line-height: 1.5;
}

/* 元信息 */
.plan-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #e4e7ed;
  font-size: 12px;
  color: #909399;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.meta-item .el-icon {
  font-size: 12px;
}

/* 计划详情对话框 */
.plan-detail {
  max-height: 500px;
  overflow-y: auto;
  padding-right: 10px;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  font-size: 16px;
  font-weight: 600;
  color: #1a202c;
  margin: 0 0 16px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e7ed;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-label {
  color: #606266;
  font-weight: 500;
  min-width: 80px;
}

.detail-value {
  color: #303133;
}

.detail-notes {
  color: #303133;
  line-height: 1.6;
  margin: 0;
  padding: 12px;
  background: #f5f7fa;
  border-radius: 6px;
}

.progress-detail {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
}

.progress-stats {
  display: flex;
  justify-content: space-around;
  margin-top: 16px;
}

.stat-item {
  text-align: center;
}

.stat-label {
  display: block;
  font-size: 14px;
  color: #606266;
  margin-bottom: 4px;
}

.stat-value {
  display: block;
  font-size: 20px;
  font-weight: 600;
  color: #409eff;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .plans-page {
    padding: 16px;
  }

  .page-title {
    font-size: 24px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .section-actions {
    width: 100%;
    justify-content: space-between;
  }

  .plans-grid {
    grid-template-columns: 1fr;
  }

  .plan-info {
    grid-template-columns: 1fr;
  }

  .detail-grid {
    grid-template-columns: 1fr;
  }

  .progress-stats {
    flex-direction: column;
    gap: 12px;
  }
}

/* 深色主题样式 */
:global(.dark-theme) .page-title {
  color: #e2e8f0;
}

:global(.dark-theme) .page-subtitle {
  color: #a0aec0;
}

:global(.dark-theme) .card-header {
  color: #e2e8f0;
}

:global(.dark-theme) .section-title {
  color: #e2e8f0;
}

:global(.dark-theme) .plan-title {
  color: #e2e8f0;
}

:global(.dark-theme) .info-label {
  color: #a0aec0;
}

:global(.dark-theme) .info-value {
  color: #e2e8f0;
}

:global(.dark-theme) .progress-label {
  color: #a0aec0;
}

:global(.dark-theme) .notes-label {
  color: #a0aec0;
}

:global(.dark-theme) .notes-content {
  color: #e2e8f0;
}

:global(.dark-theme) .plan-notes {
  background: #4a5568;
}

:global(.dark-theme) .detail-section h4 {
  color: #e2e8f0;
  border-bottom-color: #4a5568;
}

:global(.dark-theme) .detail-label {
  color: #a0aec0;
}

:global(.dark-theme) .detail-value {
  color: #e2e8f0;
}

:global(.dark-theme) .detail-notes {
  color: #e2e8f0;
  background: #4a5568;
}

:global(.dark-theme) .progress-detail {
  background: #4a5568;
}

:global(.dark-theme) .stat-label {
  color: #a0aec0;
}
</style>
