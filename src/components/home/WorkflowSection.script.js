import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { ShoppingCart, Calendar, VideoPlay } from "@element-plus/icons-vue";

const router = useRouter();

const showDemo = () => {
  ElMessage.info("演示功能开发中");
};

const navigateToPrice = () => {
  router.push("/price");
};

const navigateToSchedule = () => {
  router.push("/schedule");
};

// 工作流程步骤
const workflowSteps = [
  {
    step: 1,
    title: "输入需求",
    description: "用自然语言描述你的需求，比如'我想吃披萨'或'明天下午开会'",
    icon: "📝",
    color: "#4F46E5",
  },
  {
    step: 2,
    title: "AI智能分析",
    description: "AI理解你的意图，搜索相关信息并生成优化方案",
    icon: "🤖",
    color: "#10B981",
  },
  {
    step: 3,
    title: "查看结果",
    description: "获取比价结果或日程安排，可进一步调整和优化",
    icon: "📊",
    color: "#F59E0B",
  },
  {
    step: 4,
    title: "导出使用",
    description: "一键导出日历文件或保存比价结果，方便后续使用",
    icon: "📥",
    color: "#EF4444",
  },
];

// 导出
export {
  workflowSteps,
  showDemo,
  navigateToPrice,
  navigateToSchedule,
  ShoppingCart,
  Calendar,
  VideoPlay,
};
