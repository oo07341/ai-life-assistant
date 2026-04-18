import { useRouter } from "vue-router";
import { ShoppingCart, Calendar, User } from "@element-plus/icons-vue";

const router = useRouter();

// 导航函数
const navigateToPrice = () => {
  router.push("/price");
};

const navigateToSchedule = () => {
  router.push("/schedule");
};

const navigateToProfile = () => {
  router.push("/profile");
};

// 功能描述
const features = [
  {
    title: "AI智能比价",
    description: "输入商品描述，AI自动搜索全网价格，提供最优购买建议",
    icon: ShoppingCart,
    action: navigateToPrice,
    color: "#4F46E5",
  },
  {
    title: "AI日程规划",
    description: "描述你的日程需求，AI自动生成日历事件并导出为.ics文件",
    icon: Calendar,
    action: navigateToSchedule,
    color: "#10B981",
  },
  {
    title: "个人中心",
    description: "查看历史记录、管理个人设置、获取使用帮助",
    icon: User,
    action: navigateToProfile,
    color: "#F59E0B",
  },
];

// 导出
export {
  features,
  navigateToPrice,
  navigateToSchedule,
  navigateToProfile,
  ShoppingCart,
  Calendar,
  User,
};
