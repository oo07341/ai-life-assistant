import { useRouter } from "vue-router";
import { ShoppingCart, Calendar } from "@element-plus/icons-vue";

const router = useRouter();

// 导航函数
const navigateToPrice = () => {
  router.push("/price");
};

const navigateToSchedule = () => {
  router.push("/schedule");
};

// 导出函数
export { navigateToPrice, navigateToSchedule, ShoppingCart, Calendar };
