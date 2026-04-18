// 简单的Mock服务器，用于模拟后端API响应
import express from "express";
import cors from "cors";

const app = express();
const PORT = 3001;

app.use(cors());
app.use(express.json());

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
