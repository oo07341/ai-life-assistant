<template>
  <div class="home-test">
    <h1>测试页面 - 最简单的Vue组件</h1>
    <p>如果这个页面能正常显示，说明Vite配置正常</p>
    <p>当前时间：{{ currentTime }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const currentTime = ref("");

onMounted(() => {
  currentTime.value = new Date().toLocaleString();
});
</script>

<style scoped>
.home-test {
  padding: 20px;
  text-align: center;
}

h1 {
  color: #333;
  margin-bottom: 20px;
}

p {
  color: #666;
  margin: 10px 0;
}
</style>
