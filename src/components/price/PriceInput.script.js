import { defineProps, defineEmits } from "vue";
import {
  ChatDotRound,
  MagicStick,
  Delete,
  Lightning,
  InfoFilled,
} from "@element-plus/icons-vue";

const props = defineProps({
  searchQuery: {
    type: String,
    default: "",
  },
  isAnalyzing: {
    type: Boolean,
    default: false,
  },
  analysisResult: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["update:search-query", "analyze", "clear"]);

// 示例查询
const exampleQueries = [
  "我想买iPhone 15 Pro Max",
  "周末去露营需要什么装备",
  "给女朋友买生日礼物",
  "办公室用的咖啡机推荐",
  "性价比高的笔记本电脑",
];

// 处理输入变化
const handleInput = (event) => {
  emit("update:search-query", event.target.value);
};

// 触发分析
const triggerAnalyze = () => {
  if (props.searchQuery.trim()) {
    emit("analyze");
  }
};

// 清除输入
const triggerClear = () => {
  emit("clear");
};

// 使用示例查询
const useExample = (query) => {
  emit("update:search-query", query);
};

// 导出
export {
  props,
  emit,
  exampleQueries,
  handleInput,
  triggerAnalyze,
  triggerClear,
  useExample,
  ChatDotRound,
  MagicStick,
  Delete,
  Lightning,
  InfoFilled,
};
