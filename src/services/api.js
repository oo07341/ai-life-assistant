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

  const defaultOptions = {
    headers: {
      "Content-Type": "application/json",
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
};

/**
 * 计划相关API
 */
export const planAPI = {
  // 获取计划列表
  getPlans: () => request("/api/plan"),

  // 创建计划
  createPlan: (plan) =>
    request("/api/plan", {
      method: "POST",
      body: JSON.stringify(plan),
    }),

  // 更新计划
  updatePlan: (id, plan) =>
    request(`/api/plan/${id}`, {
      method: "PUT",
      body: JSON.stringify(plan),
    }),

  // 删除计划
  deletePlan: (id) =>
    request(`/api/plan/${id}`, {
      method: "DELETE",
    }),
};

export default {
  analyzeIntent,
  searchProducts,
  generateSchedule,
  getHotKeywords,
  userAPI,
  planAPI,
};
