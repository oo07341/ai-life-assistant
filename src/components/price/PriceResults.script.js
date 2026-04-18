import { defineProps, defineEmits } from "vue";
import {
  TrendCharts,
  Loading,
  Search,
  Shop,
  Clock,
  Star,
  Calendar,
  ShoppingCart,
  Share,
  Lightning,
} from "@element-plus/icons-vue";

const props = defineProps({
  analysisResult: {
    type: Object,
    default: null,
  },
  isAnalyzing: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits(["refresh", "save"]);

// Mock数据 - 当没有真实数据时显示
const mockResults = {
  query: "iPhone 15 Pro Max",
  intent: "购买高端智能手机",
  confidence: 0.92,
  recommendations: [
    {
      id: 1,
      platform: "京东",
      price: 8999,
      originalPrice: 9999,
      discount: "9折",
      rating: 4.8,
      reviews: 12500,
      delivery: "次日达",
      link: "#",
      features: ["官方旗舰店", "24期免息", "赠原装壳"],
    },
    {
      id: 2,
      platform: "天猫",
      price: 8799,
      originalPrice: 9999,
      discount: "88折",
      rating: 4.7,
      reviews: 9800,
      delivery: "2-3天",
      link: "#",
      features: ["品牌授权", "7天无理由", "赠贴膜"],
    },
    {
      id: 3,
      platform: "拼多多",
      price: 8299,
      originalPrice: 9999,
      discount: "83折",
      rating: 4.5,
      reviews: 15600,
      delivery: "3-5天",
      link: "#",
      features: ["百亿补贴", "正品保证", "价格最低"],
    },
  ],
  analysis: {
    bestValue: "拼多多 - 价格最低，性价比高",
    fastestDelivery: "京东 - 次日达",
    mostReliable: "京东官方旗舰店 - 正品保障",
    summary: "建议根据需求选择：追求速度选京东，追求性价比选拼多多",
  },
  timestamp: new Date().toISOString(),
};

// 获取显示结果
const getDisplayResults = () => {
  return props.analysisResult || mockResults;
};

// 刷新结果
const refreshResults = () => {
  emit("refresh");
};

// 保存结果
const saveResults = () => {
  emit("save");
};

// 格式化价格
const formatPrice = (price) => {
  return `¥${price.toLocaleString()}`;
};

// 计算节省金额
const calculateSavings = (item) => {
  return item.originalPrice - item.price;
};

// 导出
export {
  props,
  emit,
  mockResults,
  getDisplayResults,
  refreshResults,
  saveResults,
  formatPrice,
  calculateSavings,
  TrendCharts,
  Loading,
  Search,
  Shop,
  Clock,
  Star,
  Calendar,
  ShoppingCart,
  Share,
  Lightning,
};
