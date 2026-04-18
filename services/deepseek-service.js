// DeepSeek AI服务模块
class DeepSeekService {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseURL = "https://api.deepseek.com/v1";
    this.model = "deepseek-chat";
  }

  /**
   * 调用DeepSeek API
   * @param {Array} messages - 消息数组
   * @param {Object} options - 选项
   * @returns {Promise<Object>} - API响应
   */
  async callAPI(messages, options = {}) {
    const {
      max_tokens = 500,
      temperature = 0.7,
      response_format = { type: "text" },
    } = options;

    try {
      const response = await fetch(`${this.baseURL}/chat/completions`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          model: this.model,
          messages,
          max_tokens,
          temperature,
          response_format,
        }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`DeepSeek API错误: ${response.status} - ${errorText}`);
      }

      return await response.json();
    } catch (error) {
      console.error("DeepSeek API调用失败:", error.message);
      throw error;
    }
  }

  /**
   * 分析用户购物意图
   * @param {string} query - 用户查询
   * @returns {Promise<Object>} - 分析结果
   */
  async analyzeIntent(query) {
    const messages = [
      {
        role: "system",
        content: `你是一个智能购物助手，专门分析用户的购物意图。
请分析用户的查询，返回以下JSON格式的结果：
{
  "intent": "购物意图描述，如'餐饮外卖'、'日用品购物'、'电子产品购物'等",
  "keywords": ["关键词1", "关键词2", "关键词3"],
  "category": "商品类别，如'披萨'、'纸巾'、'咖啡'、'手机'等",
  "platforms": ["推荐平台1", "推荐平台2", "推荐平台3"],
  "advice": "给用户的购物建议"
}

请确保返回的是有效的JSON，不要包含其他内容。`,
      },
      {
        role: "user",
        content: query,
      },
    ];

    try {
      const response = await this.callAPI(messages, {
        max_tokens: 300,
        temperature: 0.3,
        response_format: { type: "json_object" },
      });

      const content = response.choices[0].message.content;

      // 解析JSON响应
      try {
        const result = JSON.parse(content);
        return {
          success: true,
          data: {
            intent: result.intent || "通用购物",
            keywords: result.keywords || [query],
            category: result.category || "通用",
            platforms: result.platforms || ["淘宝", "京东", "拼多多"],
            advice:
              result.advice || "根据您的需求，我们推荐选择信誉好的平台购买。",
            query: query,
          },
        };
      } catch (parseError) {
        console.error("解析AI响应失败:", parseError);
        // 降级到简单分析
        return this.fallbackIntentAnalysis(query);
      }
    } catch (error) {
      console.error("AI意图分析失败:", error);
      return this.fallbackIntentAnalysis(query);
    }
  }

  /**
   * 生成AI日程规划
   * @param {string} query - 用户查询
   * @param {string} contextTime - 上下文时间
   * @param {Object} extraInfo - 额外信息
   * @returns {Promise<Object>} - 日程规划结果
   */
  async generateSchedule(query, contextTime, extraInfo = {}) {
    const messages = [
      {
        role: "system",
        content: `你是一个智能日程规划助手，根据用户的购物需求规划合理的日程。
请根据用户的需求，返回以下JSON格式的日程规划：
{
  "events": [
    {
      "title": "事件标题",
      "start": "ISO时间字符串",
      "end": "ISO时间字符串", 
      "location": "地点",
      "description": "事件描述"
    }
  ],
  "message": "给用户的提示信息"
}

规则：
1. 根据用户需求规划2-3个相关事件
2. 事件时间要合理，基于context_time: ${contextTime}
3. 如果有extra_info，要合理利用
4. 事件标题要清晰描述活动
5. 返回有效的JSON，不要包含其他内容。`,
      },
      {
        role: "user",
        content: `用户需求: ${query}
上下文时间: ${contextTime}
额外信息: ${JSON.stringify(extraInfo)}`,
      },
    ];

    try {
      const response = await this.callAPI(messages, {
        max_tokens: 600,
        temperature: 0.5,
        response_format: { type: "json_object" },
      });

      const content = response.choices[0].message.content;

      try {
        const result = JSON.parse(content);

        // 验证和格式化事件
        const events = (result.events || []).map((event, index) => ({
          title: event.title || `AI规划事件 ${index + 1}`,
          start: event.start || this.generateTime(contextTime, index * 2),
          end: event.end || this.generateTime(contextTime, index * 2 + 1),
          location: event.location || "根据情况安排",
          description: event.description || `根据需求"${query}"智能规划的日程`,
        }));

        return {
          success: true,
          message: result.message || "AI已根据您的需求智能规划日程",
          events: events.slice(0, 3), // 最多3个事件
        };
      } catch (parseError) {
        console.error("解析日程规划响应失败:", parseError);
        return this.fallbackScheduleGeneration(query, contextTime, extraInfo);
      }
    } catch (error) {
      console.error("AI日程规划失败:", error);
      return this.fallbackScheduleGeneration(query, contextTime, extraInfo);
    }
  }

  /**
   * 降级：简单的意图分析
   */
  fallbackIntentAnalysis(query) {
    const queryLower = query.toLowerCase();

    let intent = "通用购物";
    let keywords = [query];
    let category = "通用";
    let platforms = ["淘宝", "京东", "拼多多"];
    let advice = "根据您的需求，我们推荐选择信誉好的平台购买。";

    if (
      queryLower.includes("披萨") ||
      queryLower.includes("吃") ||
      queryLower.includes("外卖")
    ) {
      intent = "餐饮外卖";
      keywords = ["披萨", "外卖", "餐饮"];
      category = "披萨";
      platforms = ["美团", "饿了么", "达美乐APP"];
      advice = "披萨建议选择连锁品牌，品质有保障，配送速度快。";
    } else if (queryLower.includes("纸巾") || queryLower.includes("纸")) {
      intent = "日用品购物";
      keywords = ["纸巾", "生活用品", "清洁"];
      category = "纸巾";
      platforms = ["淘宝", "京东", "拼多多"];
      advice = "纸巾建议选择大品牌，注意查看用户评价和销量。";
    } else if (queryLower.includes("咖啡") || queryLower.includes("喝")) {
      intent = "饮品购物";
      keywords = ["咖啡", "奶茶", "饮品"];
      category = "咖啡";
      platforms = ["美团", "饿了么", "星巴克APP"];
      advice = "咖啡可以选择外卖平台，注意配送时间和温度。";
    } else if (queryLower.includes("手机") || queryLower.includes("电子")) {
      intent = "电子产品购物";
      keywords = ["手机", "电子产品", "数码"];
      category = "手机";
      platforms = ["京东", "天猫", "苏宁"];
      advice = "电子产品建议选择官方旗舰店，注意查看保修政策。";
    }

    return {
      success: true,
      data: { intent, keywords, category, platforms, advice, query },
    };
  }

  /**
   * 降级：简单的日程生成
   */
  fallbackScheduleGeneration(query, contextTime, extraInfo) {
    const baseTime = new Date(contextTime || new Date().toISOString());

    const events = [
      {
        title: `AI规划：${query.substring(0, 10)}...`,
        start: new Date(baseTime.getTime() + 60 * 60 * 1000).toISOString(),
        end: new Date(baseTime.getTime() + 2 * 60 * 60 * 1000).toISOString(),
        location: extraInfo.shop_name || extraInfo.address || "根据情况安排",
        description: `根据您的需求"${query}"智能规划的日程`,
      },
      {
        title: "AI规划：后续活动",
        start: new Date(baseTime.getTime() + 3 * 60 * 60 * 1000).toISOString(),
        end: new Date(baseTime.getTime() + 4 * 60 * 60 * 1000).toISOString(),
        location: "附近场所",
        description: "AI为您规划的后续时间安排",
      },
    ];

    return {
      success: true,
      message: "已使用备用方案生成日程",
      events,
    };
  }

  /**
   * 生成时间（辅助函数）
   */
  generateTime(baseTime, hoursOffset) {
    const time = new Date(baseTime);
    time.setHours(time.getHours() + hoursOffset);
    return time.toISOString();
  }

  /**
   * 健康检查
   */
  async healthCheck() {
    try {
      const response = await this.callAPI([{ role: "user", content: "ping" }], {
        max_tokens: 10,
      });

      return {
        success: true,
        status: "healthy",
        model: this.model,
        response_time: "正常",
      };
    } catch (error) {
      return {
        success: false,
        status: "unhealthy",
        error: error.message,
      };
    }
  }
}

export default DeepSeekService;
