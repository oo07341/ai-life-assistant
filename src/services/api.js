/**
 * 统一的API服务层
 * 封装所有前后端通信逻辑
 */

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:3001";

/**
 * 统一的请求函数
 */
async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  // 从localStorage获取用户ID
  const userId = localStorage.getItem("userId") || "test_user_001";

  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
      "X-User-Id": userId,
    },
  };

  try {
    const response = await fetch(url, {
      ...defaultOptions,
      ...options,
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // 检查后端返回的格式
    if (data.code !== undefined && data.code !== 0) {
      throw new Error(data.msg || "API请求失败");
    }

    return data.data || data;
  } catch (error) {
    console.error(`API请求失败 ${endpoint}:`, error);
    throw error;
  }
}

/**
 * AI意图分析
 * @param {string} query - 用户查询
 * @returns {Promise<Object>} 意图分析结果
 */
export async function analyzeIntent(query) {
  return request("/api/search", {
    method: "POST",
    body: JSON.stringify({ query }),
  });
}

/**
 * 商品搜索
 * @param {string} keyword - 搜索关键词
 * @returns {Promise<Array>} 商品列表
 */
export async function searchProducts(keyword) {
  return request(`/api/prices`, {
    method: "POST",
    body: JSON.stringify({ keywords: [keyword] }),
  });
}

/**
 * 生成日程计划
 * @param {Object} scheduleInfo - 日程信息
 * @returns {Promise<Object>} 日程计划结果
 */
export async function generateSchedule(scheduleInfo) {
  return request("/api/schedule", {
    method: "POST",
    body: JSON.stringify({ schedule_info: scheduleInfo }),
  });
}

/**
 * 获取热门关键词
 * @returns {Promise<Array>} 热门关键词列表
 */
export async function getHotKeywords() {
  // 这个接口在parse.py的search接口中返回，需要单独调用
  try {
    const result = await request("/api/search", {
      method: "POST",
      body: JSON.stringify({ query: "" }),
    });
    return result.hot_keywords || [];
  } catch (error) {
    console.error("获取热门关键词失败:", error);
    return [];
  }
}

/**
 * 用户相关API
 */
export const userAPI = {
  // 获取用户信息
  getProfile: () => request("/api/user/profile"),

  // 更新用户信息
  updateProfile: (profile) =>
    request("/api/user/profile", {
      method: "PUT",
      body: JSON.stringify(profile),
    }),

  // 获取用户历史
  getHistory: () => request("/api/user/history"),

  // 获取用户统计数据
  getStats: () => request("/api/user/stats"),

  // 获取用户计划列表
  getPlans: () => request("/api/user/plans"),

  // 获取激活计划
  getActivePlan: () => request("/api/user/active-plan"),

  // 切换激活计划
  switchPlan: (planId) =>
    request("/api/user/switch-plan", {
      method: "POST",
      body: JSON.stringify({ plan_id: planId }),
    }),
};

/**
 * 计划相关API
 */
export const planAPI = {
  // 保存新计划
  savePlan: (scheduleInfo) =>
    request("/api/plan/save", {
      method: "POST",
      body: JSON.stringify({ schedule_info: scheduleInfo }),
    }),

  // 更新计划进度
  updateProgress: (planId, completedDates) =>
    request("/api/plan/update-progress", {
      method: "POST",
      body: JSON.stringify({
        plan_id: planId,
        completed_dates: completedDates,
      }),
    }),

  // 合并计划
  mergePlan: (scheduleInfo) =>
    request("/api/plan/merge", {
      method: "POST",
      body: JSON.stringify({ schedule_info: scheduleInfo }),
    }),
};

/**
 * 日程相关API
 */
export const scheduleAPI = {
  // 生成日程计划
  generateSchedule: (scheduleInfo) =>
    request("/api/schedule", {
      method: "POST",
      body: JSON.stringify({ schedule_info: scheduleInfo }),
    }),

  // 调整日程计划
  adjustSchedule: (
    originalSchedule,
    completedDates,
    remainingSubjects,
    targetDate,
    dailyHours,
  ) =>
    request("/api/adjust-schedule", {
      method: "POST",
      body: JSON.stringify({
        original_schedule: originalSchedule,
        completed_dates: completedDates,
        remaining_subjects: remainingSubjects,
        target_date: targetDate,
        daily_hours: dailyHours,
      }),
    }),
};

/**
 * 价格相关API
 */
export const priceAPI = {
  // 搜索商品
  searchProducts: (keywords) =>
    request("/api/prices", {
      method: "POST",
      body: JSON.stringify({ keywords }),
    }),
};

// 重命名函数以避免冲突
const analyzeIntentApi = analyzeIntent;
const searchProductsApi = searchProducts;
const generateScheduleApi = generateSchedule;

export default {
  analyzeIntent: analyzeIntentApi,
  searchProducts: searchProductsApi,
  generateSchedule: generateScheduleApi,
  getHotKeywords,
  userAPI,
  planAPI,
  scheduleAPI,
  priceAPI,
};
