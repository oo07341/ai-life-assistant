// 简单的Mock服务器，用于模拟后端API响应
import express from "express";
import cors from "cors";

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

// 模拟AI意图分析API
app.post("/api/analyze-intent", (req, res) => {
  console.log("收到AI意图分析请求:", req.body);

  // 模拟处理延迟
  setTimeout(() => {
    const query = req.body.query || "";

    // 根据用户查询分析意图
    let keywords = [];
    let platforms = [];
    let advice = "";

    if (query.includes("披萨") || query.includes("pizza")) {
      keywords = ["必胜客披萨", "达美乐披萨", "棒约翰披萨"];
      platforms = ["美团", "饿了么", "京东到家"];
      advice = "披萨建议选择连锁品牌，品质有保障，配送速度快。";
    } else if (query.includes("咖啡") || query.includes("coffee")) {
      keywords = ["星巴克咖啡", "瑞幸咖啡", "库迪咖啡"];
      platforms = ["美团", "饿了么", "星巴克App"];
      advice = "咖啡建议根据口味选择，美式适合提神，拿铁适合休闲。";
    } else if (query.includes("奶茶") || query.includes("bubble tea")) {
      keywords = ["喜茶", "奈雪的茶", "蜜雪冰城"];
      platforms = ["美团", "饿了么", "小程序"];
      advice = "奶茶建议选择少糖，健康又美味。";
    } else if (query.includes("手机") || query.includes("iphone")) {
      keywords = ["iPhone 16", "华为Mate 60", "小米14"];
      platforms = ["京东", "淘宝", "拼多多"];
      advice = "手机建议对比各平台价格，注意查看用户评价。";
    } else {
      keywords = [query + " 商品"];
      platforms = ["京东", "淘宝", "拼多多"];
      advice = "建议多平台比价，选择信誉好的商家。";
    }

    const response = {
      success: true,
      intent: "比价购物",
      keywords: keywords,
      platforms: platforms,
      advice: advice,
      query: query,
    };

    res.json(response);
  }, 800); // 0.8秒延迟模拟AI处理
});

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

// 模拟AI日程规划API
app.post("/api/generate_schedule", (req, res) => {
  console.log("收到AI日程规划请求:", req.body);

  // 模拟处理延迟
  setTimeout(() => {
    const query = req.body.query || "晚餐安排";
    const shopName = req.body.extra_info?.shop_name || "默认地点";
    const address = req.body.extra_info?.address || "";

    // 根据查询内容生成相关事件
    const events = [];

    // 主事件 - 根据用户查询生成
    const mainEventTitle = query.includes("吃")
      ? "AI规划：用餐时间"
      : query.includes("购物")
        ? "AI规划：购物时间"
        : query.includes("会议")
          ? "AI规划：工作会议"
          : query.includes("运动")
            ? "AI规划：健身时间"
            : "AI规划：主要活动";

    events.push({
      title: mainEventTitle,
      start: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(), // 2小时后
      end: new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString(), // 3小时后
      location: shopName + (address ? ` (${address})` : ""),
      description: `根据您的需求"${query}"智能规划的日程`,
    });

    // 第二个事件 - 相关活动
    if (query.includes("吃")) {
      events.push({
        title: "AI规划：餐后活动",
        start: new Date(Date.now() + 3.5 * 60 * 60 * 1000).toISOString(), // 3.5小时后
        end: new Date(Date.now() + 4.5 * 60 * 60 * 1000).toISOString(), // 4.5小时后
        location: "附近休闲场所",
        description: "餐后建议的休闲活动",
      });
    } else if (query.includes("购物")) {
      events.push({
        title: "AI规划：休息时间",
        start: new Date(Date.now() + 3.5 * 60 * 60 * 1000).toISOString(), // 3.5小时后
        end: new Date(Date.now() + 4.5 * 60 * 60 * 1000).toISOString(), // 4.5小时后
        location: "咖啡厅",
        description: "购物后的休息时间",
      });
    }

    // 第三个事件 - 后续安排
    events.push({
      title: "AI规划：后续计划",
      start: new Date(Date.now() + 5 * 60 * 60 * 1000).toISOString(), // 5小时后
      end: new Date(Date.now() + 6 * 60 * 60 * 1000).toISOString(), // 6小时后
      location: "根据情况安排",
      description: "AI为您规划的后续时间安排",
    });

    const response = {
      success: true,
      message: "AI已成功根据您的需求规划日程",
      events: events,
    };

    res.json(response);
  }, 1000); // 1秒延迟模拟AI处理
});

// 健康检查端点
app.get("/api/health", (req, res) => {
  res.json({ status: "ok", message: "Mock服务器运行正常" });
});

app.listen(PORT, () => {
  console.log(`Mock服务器运行在 http://localhost:${PORT}`);
  console.log("可用端点:");
  console.log("  POST /api/generate_schedule - AI日程规划");
  console.log("  GET  /api/health - 健康检查");
});

// 处理优雅关闭
process.on("SIGTERM", () => {
  console.log("收到SIGTERM信号，正在关闭服务器...");
  process.exit(0);
});
