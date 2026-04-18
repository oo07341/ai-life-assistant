// 智能Mock服务器，支持DeepSeek AI和Mock数据
import express from "express";
import cors from "cors";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import dotenv from "dotenv";

// 加载环境变量 - 根据NODE_ENV加载不同的环境文件
const nodeEnv = process.env.NODE_ENV || "development";
const envFile =
  nodeEnv === "production" ? ".env.production" : ".env.development";

console.log(`📁 加载环境文件: ${envFile}`);
dotenv.config({ path: envFile });

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 导入DeepSeek服务
import DeepSeekService from "./services/deepseek-service.js";

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// 初始化DeepSeek服务
const deepseekApiKey =
  process.env.DEEPSEEK_API_KEY || process.env.VITE_DEEPSEEK_API_KEY;
const useAI =
  process.env.VITE_USE_AI === "true" || process.env.VITE_USE_AI === true;

let deepseekService = null;
if (useAI && deepseekApiKey) {
  try {
    deepseekService = new DeepSeekService(deepseekApiKey);
    console.log("✅ DeepSeek AI服务已初始化");
  } catch (error) {
    console.error("❌ DeepSeek AI服务初始化失败:", error.message);
    console.log("⚠️  将使用Mock数据模式");
  }
} else {
  console.log("ℹ️  DeepSeek AI未启用，使用Mock数据模式");
}

// 智能服务选择器 - 强制使用Mock数据用于测试
const getIntentService = () => {
  // 强制使用Mock数据，即使DeepSeek服务已初始化
  console.log("🔧 服务选择器: 强制使用Mock数据模式");
  return {
    type: "mock",
    service: null,
  };
};

const getScheduleService = () => {
  // 强制使用Mock数据，即使DeepSeek服务已初始化
  console.log("🔧 服务选择器: 强制使用Mock数据模式");
  return {
    type: "mock",
    service: null,
  };
};

// 智能AI意图分析API（支持DeepSeek AI和Mock降级）
app.post("/api/analyze-intent", async (req, res) => {
  console.log("收到AI意图分析请求:", req.body);

  const query = req.body.query || "";
  const serviceInfo = getIntentService();

  try {
    if (serviceInfo.type === "ai" && serviceInfo.service) {
      console.log("使用DeepSeek AI进行意图分析...");

      try {
        const result = await serviceInfo.service.analyzeIntent(query);

        if (result.success) {
          console.log("DeepSeek AI分析成功");
          res.json({
            success: true,
            ...result.data,
            source: "deepseek_ai",
          });
        } else {
          throw new Error("AI分析返回失败");
        }
      } catch (aiError) {
        console.error("DeepSeek AI分析失败，降级到Mock数据:", aiError.message);
        // 降级到Mock分析
        useMockIntentAnalysis(query, res);
      }
    } else {
      console.log("使用Mock数据进行意图分析");
      useMockIntentAnalysis(query, res);
    }
  } catch (error) {
    console.error("意图分析处理失败:", error);
    res.status(500).json({
      success: false,
      error: "意图分析服务暂时不可用",
      query: query,
    });
  }
});

// Mock意图分析函数
function useMockIntentAnalysis(query, res) {
  // 模拟处理延迟
  setTimeout(() => {
    // 根据用户查询分析意图
    let keywords = [];
    let platforms = [];
    let advice = "";
    let intent = "比价购物";

    if (query.includes("披萨") || query.includes("pizza")) {
      intent = "餐饮外卖";
      keywords = ["必胜客披萨", "达美乐披萨", "棒约翰披萨"];
      platforms = ["美团", "饿了么", "京东到家"];
      advice = "披萨建议选择连锁品牌，品质有保障，配送速度快。";
    } else if (query.includes("咖啡") || query.includes("coffee")) {
      intent = "饮品购物";
      keywords = ["星巴克咖啡", "瑞幸咖啡", "库迪咖啡"];
      platforms = ["美团", "饿了么", "星巴克App"];
      advice = "咖啡建议根据口味选择，美式适合提神，拿铁适合休闲。";
    } else if (query.includes("奶茶") || query.includes("bubble tea")) {
      intent = "饮品购物";
      keywords = ["喜茶", "奈雪的茶", "蜜雪冰城"];
      platforms = ["美团", "饿了么", "小程序"];
      advice = "奶茶建议选择少糖，健康又美味。";
    } else if (query.includes("手机") || query.includes("iphone")) {
      intent = "电子产品购物";
      keywords = ["iPhone 16", "华为Mate 60", "小米14"];
      platforms = ["京东", "淘宝", "拼多多"];
      advice = "手机建议对比各平台价格，注意查看用户评价。";
    } else if (query.includes("纸巾") || query.includes("纸")) {
      intent = "日用品购物";
      keywords = ["纸巾", "生活用品", "清洁用品"];
      platforms = ["淘宝", "京东", "拼多多"];
      advice = "纸巾建议选择大品牌，注意查看用户评价和销量。";
    } else {
      intent = "通用购物";
      keywords = [query + " 商品"];
      platforms = ["京东", "淘宝", "拼多多"];
      advice = "建议多平台比价，选择信誉好的商家。";
    }

    const response = {
      success: true,
      intent: intent,
      keywords: keywords,
      platforms: platforms,
      advice: advice,
      query: query,
      source: "mock_data",
    };

    res.json(response);
  }, 800); // 0.8秒延迟模拟AI处理
}

// 模拟商品搜索API
app.get("/api/search-products", (req, res) => {
  console.log("收到商品搜索请求:", req.query);

  const keyword = req.query.keyword || "";
  const platform = req.query.platform || "";

  // 模拟处理延迟
  setTimeout(() => {
    // Mock商品数据
    const mockProducts = {
      披萨: [
        {
          id: 1,
          name: "必胜客超级至尊披萨",
          price: 89,
          originalPrice: 108,
          platform: "美团",
          rating: 4.8,
          sales: 1250,
          deliveryTime: "30分钟",
          urlScheme: "imeituan://",
          image: "🍕",
        },
        {
          id: 2,
          name: "达美乐经典意式肉酱披萨",
          price: 79,
          originalPrice: 98,
          platform: "饿了么",
          rating: 4.7,
          sales: 980,
          deliveryTime: "35分钟",
          urlScheme: "eleme://",
          image: "🍕",
        },
        {
          id: 3,
          name: "棒约翰特色海鲜披萨",
          price: 95,
          originalPrice: 120,
          platform: "美团",
          rating: 4.6,
          sales: 650,
          deliveryTime: "40分钟",
          urlScheme: "imeituan://",
          image: "🍕",
        },
        {
          id: 4,
          name: "尊宝披萨奥尔良烤鸡披萨",
          price: 68,
          originalPrice: 88,
          platform: "饿了么",
          rating: 4.5,
          sales: 2100,
          deliveryTime: "25分钟",
          urlScheme: "eleme://",
          image: "🍕",
        },
      ],
      咖啡: [
        {
          id: 5,
          name: "星巴克拿铁咖啡",
          price: 32,
          originalPrice: 38,
          platform: "美团",
          rating: 4.9,
          sales: 5200,
          deliveryTime: "20分钟",
          urlScheme: "imeituan://",
          image: "☕",
        },
        {
          id: 6,
          name: "瑞幸生椰拿铁",
          price: 19,
          originalPrice: 29,
          platform: "瑞幸App",
          rating: 4.8,
          sales: 8900,
          deliveryTime: "15分钟",
          urlScheme: "luckincoffee://",
          image: "☕",
        },
        {
          id: 7,
          name: "库迪星辰厚乳拿铁",
          price: 16,
          originalPrice: 24,
          platform: "库迪App",
          rating: 4.7,
          sales: 4300,
          deliveryTime: "18分钟",
          urlScheme: "cotti://",
          image: "☕",
        },
      ],
      奶茶: [
        {
          id: 8,
          name: "喜茶多肉葡萄",
          price: 29,
          originalPrice: 32,
          platform: "喜茶小程序",
          rating: 4.9,
          sales: 12500,
          deliveryTime: "25分钟",
          urlScheme: "heytea://",
          image: "🧋",
        },
        {
          id: 9,
          name: "奈雪霸气橙子",
          price: 26,
          originalPrice: 30,
          platform: "奈雪小程序",
          rating: 4.8,
          sales: 9800,
          deliveryTime: "30分钟",
          urlScheme: "naixue://",
          image: "🧋",
        },
        {
          id: 10,
          name: "蜜雪冰城柠檬水",
          price: 4,
          originalPrice: 5,
          platform: "美团",
          rating: 4.6,
          sales: 25600,
          deliveryTime: "15分钟",
          urlScheme: "imeituan://",
          image: "🧋",
        },
      ],
      手机: [
        {
          id: 11,
          name: "iPhone 16 Pro 256GB",
          price: 8999,
          originalPrice: 9999,
          platform: "京东",
          rating: 4.9,
          sales: 5200,
          deliveryTime: "次日达",
          urlScheme: "openapp.jd.com/",
          image: "📱",
        },
        {
          id: 12,
          name: "华为Mate 60 Pro",
          price: 6999,
          originalPrice: 7999,
          platform: "淘宝",
          rating: 4.8,
          sales: 8900,
          deliveryTime: "3天",
          urlScheme: "taobao://",
          image: "📱",
        },
        {
          id: 13,
          name: "小米14 Ultra",
          price: 6499,
          originalPrice: 6999,
          platform: "小米商城",
          rating: 4.7,
          sales: 4300,
          deliveryTime: "次日达",
          urlScheme: "mishop://",
          image: "📱",
        },
      ],
    };

    // 根据关键词查找商品
    let products = [];

    for (const [category, categoryProducts] of Object.entries(mockProducts)) {
      if (
        keyword.toLowerCase().includes(category.toLowerCase()) ||
        category.toLowerCase().includes(keyword.toLowerCase())
      ) {
        products = [...products, ...categoryProducts];
        break;
      }
    }

    // 如果没有匹配到特定类别，返回默认商品
    if (products.length === 0) {
      products = [
        {
          id: 14,
          name: `${keyword} 商品A`,
          price: 99,
          originalPrice: 129,
          platform: "京东",
          rating: 4.5,
          sales: 1000,
          deliveryTime: "2天",
          urlScheme: "openapp.jd.com/",
          image: "🛒",
        },
        {
          id: 15,
          name: `${keyword} 商品B`,
          price: 149,
          originalPrice: 199,
          platform: "淘宝",
          rating: 4.3,
          sales: 800,
          deliveryTime: "3天",
          urlScheme: "taobao://",
          image: "🛒",
        },
        {
          id: 16,
          name: `${keyword} 商品C`,
          price: 79,
          originalPrice: 99,
          platform: "拼多多",
          rating: 4.2,
          sales: 1500,
          deliveryTime: "4天",
          urlScheme: "pinduoduo://",
          image: "🛒",
        },
      ];
    }

    // 按平台过滤
    if (platform) {
      products = products.filter((p) => p.platform.includes(platform));
    }

    // 按价格排序
    products.sort((a, b) => a.price - b.price);

    const response = {
      success: true,
      keyword: keyword,
      platform: platform,
      total: products.length,
      products: products,
    };

    res.json(response);
  }, 600); // 0.6秒延迟
});

// 智能AI日程规划API（支持DeepSeek AI和Mock降级）
app.post("/api/generate_schedule", async (req, res) => {
  console.log("收到AI日程规划请求:", req.body);

  const query = req.body.query || "";
  const contextTime = req.body.context_time || new Date().toISOString();
  const extraInfo = req.body.extra_info || {};
  const serviceInfo = getScheduleService();

  try {
    if (serviceInfo.type === "ai" && serviceInfo.service) {
      console.log("使用DeepSeek AI进行日程规划...");

      try {
        const result = await serviceInfo.service.generateSchedule(
          query,
          contextTime,
          extraInfo,
        );

        if (result.success) {
          console.log("DeepSeek AI日程规划成功");
          res.json({
            success: true,
            message: result.message,
            events: result.events,
            source: "deepseek_ai",
          });
        } else {
          throw new Error("AI日程规划返回失败");
        }
      } catch (aiError) {
        console.error(
          "DeepSeek AI日程规划失败，降级到Mock数据:",
          aiError.message,
        );
        // 降级到Mock日程规划
        useMockScheduleGeneration(query, contextTime, extraInfo, res);
      }
    } else {
      console.log("使用Mock数据进行日程规划");
      useMockScheduleGeneration(query, contextTime, extraInfo, res);
    }
  } catch (error) {
    console.error("日程规划处理失败:", error);
    res.status(500).json({
      success: false,
      error: "日程规划服务暂时不可用",
      query: query,
    });
  }
});

// Mock日程规划函数
function useMockScheduleGeneration(query, contextTime, extraInfo, res) {
  // 模拟处理延迟
  setTimeout(() => {
    console.log("🔍 Mock日程规划 - 查询分析:");
    console.log("  原始查询:", query);
    console.log("  查询类型:", typeof query);
    console.log("  查询长度:", query.length);

    const shopName = extraInfo?.shop_name || "默认地点";
    const address = extraInfo?.address || "";

    // 根据查询内容生成相关事件
    const events = [];

    // 主事件 - 根据用户查询生成更相关的标题
    let mainEventTitle = "AI规划：主要活动";
    console.log("  初始标题:", mainEventTitle);

    // 更智能的查询分析
    const hasEat =
      query.includes("吃") ||
      query.includes("餐") ||
      query.includes("饭") ||
      query.includes("披萨") ||
      query.includes("火锅") ||
      query.includes("烧烤");
    const hasMovie =
      query.includes("电影") ||
      query.includes("看") ||
      query.includes("影院") ||
      query.includes("剧场");
    const hasShop =
      query.includes("购物") ||
      query.includes("买") ||
      query.includes("购") ||
      query.includes("商品") ||
      query.includes("东西");

    console.log("  包含'吃'相关词:", hasEat);
    console.log("  包含'电影'相关词:", hasMovie);
    console.log("  包含'购物'相关词:", hasShop);

    if (hasEat) {
      mainEventTitle = "AI规划：用餐时间";
    } else if (hasMovie) {
      mainEventTitle = "AI规划：观影时间";
    } else if (hasShop) {
      mainEventTitle = "AI规划：购物时间";
    } else if (
      query.includes("会议") ||
      query.includes("工作") ||
      query.includes("办公") ||
      query.includes("讨论")
    ) {
      mainEventTitle = "AI规划：工作会议";
    } else if (
      query.includes("运动") ||
      query.includes("健身") ||
      query.includes("锻炼") ||
      query.includes("跑步")
    ) {
      mainEventTitle = "AI规划：健身时间";
    } else if (
      query.includes("学习") ||
      query.includes("读书") ||
      query.includes("阅读") ||
      query.includes("课程")
    ) {
      mainEventTitle = "AI规划：学习时间";
    } else if (
      query.includes("旅行") ||
      query.includes("旅游") ||
      query.includes("出行") ||
      query.includes("游玩")
    ) {
      mainEventTitle = "AI规划：旅行时间";
    }

    console.log("  关键词分析后标题:", mainEventTitle);

    // 如果可能，从查询中提取更具体的活动名称
    // 改进的正则表达式，支持更多模式
    const activityPatterns = [
      /我想(吃|买|看|去|参加|学习|做)?\s*(.+?)(，|。|$)/,
      /我想要?(.+?)(，|。|$)/,
      /我打算(.+?)(，|。|$)/,
      /我需要(.+?)(，|。|$)/,
    ];

    let extractedActivity = null;
    for (const pattern of activityPatterns) {
      const match = query.match(pattern);
      if (match) {
        console.log("  正则匹配成功:", pattern);
        console.log("  匹配结果:", match);

        // 确定哪个组包含活动内容
        if (match[2]) {
          extractedActivity = match[2].trim();
        } else if (match[1]) {
          extractedActivity = match[1].trim();
        }
        break;
      }
    }

    if (extractedActivity) {
      console.log("  提取的活动:", extractedActivity);
      console.log("  活动长度:", extractedActivity.length);

      if (extractedActivity.length > 0 && extractedActivity.length < 20) {
        mainEventTitle = `AI规划：${extractedActivity}`;
        console.log("  正则提取后标题:", mainEventTitle);
      }
    } else {
      console.log("  未提取到具体活动");
    }

    const baseTime = new Date(contextTime || Date.now());

    events.push({
      title: mainEventTitle,
      start: new Date(baseTime.getTime() + 2 * 60 * 60 * 1000).toISOString(), // 2小时后
      end: new Date(baseTime.getTime() + 3 * 60 * 60 * 1000).toISOString(), // 3小时后
      location: shopName + (address ? ` (${address})` : ""),
      description: `根据您的需求"${query}"智能规划的日程`,
    });

    // 第二个事件 - 相关活动
    if (query.includes("吃")) {
      events.push({
        title: "AI规划：餐后活动",
        start: new Date(
          baseTime.getTime() + 3.5 * 60 * 60 * 1000,
        ).toISOString(), // 3.5小时后
        end: new Date(baseTime.getTime() + 4.5 * 60 * 60 * 1000).toISOString(), // 4.5小时后
        location: "附近休闲场所",
        description: "餐后建议的休闲活动",
      });
    } else if (query.includes("购物")) {
      events.push({
        title: "AI规划：休息时间",
        start: new Date(
          baseTime.getTime() + 3.5 * 60 * 60 * 1000,
        ).toISOString(), // 3.5小时后
        end: new Date(baseTime.getTime() + 4.5 * 60 * 60 * 1000).toISOString(), // 4.5小时后
        location: "咖啡厅",
        description: "购物后的休息时间",
      });
    }

    // 第三个事件 - 后续安排
    events.push({
      title: "AI规划：后续计划",
      start: new Date(baseTime.getTime() + 5 * 60 * 60 * 1000).toISOString(), // 5小时后
      end: new Date(baseTime.getTime() + 6 * 60 * 60 * 1000).toISOString(), // 6小时后
      location: "根据情况安排",
      description: "AI为您规划的后续时间安排",
    });

    const response = {
      success: true,
      message: "AI已成功根据您的需求规划日程",
      events: events,
      source: "mock_data",
    };

    console.log("📅 Mock日程规划完成:");
    console.log("  最终标题:", mainEventTitle);
    console.log("  事件数量:", events.length);
    console.log("  响应source:", response.source);

    res.json(response);
  }, 1000); // 1秒延迟模拟AI处理
}

// 健康检查端点
app.get("/api/health", async (req, res) => {
  const serverStatus = {
    status: "ok",
    message: "智能Mock服务器运行正常",
    timestamp: new Date().toISOString(),
    endpoints: [
      "POST /api/analyze-intent - AI意图分析",
      "POST /api/generate_schedule - AI日程规划",
      "GET /api/search-products - 商品搜索",
      "GET /api/health - 健康检查",
    ],
    ai_status: {
      enabled: useAI,
      service: deepseekService ? "deepseek_ai" : "mock_only",
      initialized: !!deepseekService,
    },
  };

  // 如果DeepSeek服务已初始化，检查其健康状态
  if (deepseekService) {
    try {
      const aiHealth = await deepseekService.healthCheck();
      serverStatus.ai_status.deepseek_health = aiHealth;
    } catch (error) {
      serverStatus.ai_status.deepseek_health = {
        success: false,
        error: error.message,
      };
    }
  }

  res.json(serverStatus);
});

app.listen(PORT, () => {
  console.log(`🚀 智能Mock服务器运行在 http://localhost:${PORT}`);
  console.log("📡 可用端点:");
  console.log("  POST /api/analyze-intent    - AI意图分析");
  console.log("  POST /api/generate_schedule - AI日程规划");
  console.log("  GET  /api/search-products   - 商品搜索");
  console.log("  GET  /api/health            - 健康检查");
  console.log("");
  console.log("🤖 AI模式:", useAI ? "DeepSeek AI已启用" : "Mock数据模式");
  if (deepseekService) {
    console.log("✅ DeepSeek AI服务已初始化");
  } else {
    console.log("ℹ️  使用Mock数据模式");
  }
});

// 处理优雅关闭
process.on("SIGTERM", () => {
  console.log("收到SIGTERM信号，正在关闭服务器...");
  process.exit(0);
});
