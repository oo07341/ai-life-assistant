# 🤖 AI生活助手

一个基于Vue 3 + Element Plus + Node.js的智能生活工具，结合了AI智能比价和日程规划两大核心功能。

## ✨ 核心功能

### 🔍 AI智能比价

- **自然语言理解**：理解用户需求，如"我想吃披萨"、"想买手机"
- **意图分析**：AI分析用户意图，提取关键词和推荐平台
- **全网比价**：聚合多个平台价格信息，智能排序筛选
- **最佳性价比**：自动标识最佳性价比商品
- **一键购买**：直接唤起购物App，2秒超时降级处理

### 📅 AI日程规划

- **智能规划**：根据比价结果智能规划日程
- **日历生成**：生成标准.ics日历文件
- **一键导入**：支持Google日历、Outlook日历、系统日历
- **数据传递**：比价结果自动传递到日程规划

## 🚀 技术栈

### 前端

- **框架**：Vue 3 + Vite
- **UI库**：Element Plus + 图标库
- **状态管理**：Vue Composition API
- **样式**：CSS3 + Flexbox/Grid + 响应式设计

### 后端

- **服务器**：Node.js + Express
- **API**：RESTful API设计
- **Mock数据**：完整的Mock服务器
- **CORS**：跨域资源共享支持

### 开发工具

- **构建工具**：Vite
- **包管理**：npm
- **代码格式化**：Prettier
- **并发运行**：concurrently

## 📁 项目结构

```
e:\ai-life-assistant\
├── src/
│   ├── components/
│   │   ├── PriceComparison.vue      # AI智能比价组件（稳定版本）
│   │   └── ScheduleGenerator.vue    # AI日程规划组件
│   ├── views/
│   │   └── Home.vue                 # 主视图组件
│   ├── App.vue                      # 根组件
│   └── main.js                      # 应用入口
├── mock-server.js                   # Mock API服务器
├── package.json                     # 项目配置
├── vite.config.js                   # Vite配置
├── .env.development                 # 开发环境配置
├── .env.production                  # 生产环境配置
└── README.md                        # 项目说明文档
```

## 🔄 最近更新

### 2026-04-18

- ✅ **组件清理**：删除了所有测试文件，统一了组件命名
- ✅ **环境配置**：完善了开发和生产环境配置
- ✅ **功能验证**：验证了完整的端到端流程
- ✅ **错误处理**：完善了多层降级错误处理机制
- ✅ **Mock服务器**：验证了Mock API服务器的正常运行

### 核心组件状态

- **PriceComparison.vue**：稳定版本，完整功能
- **ScheduleGenerator.vue**：完整功能，支持Mock切换
- **Home.vue**：主视图，整合所有功能

## 🛠️ 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发环境

```bash
# 同时启动前端和Mock服务器（推荐）
npm run dev:full

# 或分别启动
npm run mock:server  # 启动Mock服务器 (http://localhost:3001)
npm run dev          # 启动前端开发服务器 (http://localhost:5173)
```

### 3. 访问应用

- **前端应用**：http://localhost:5173
- **Mock API**：http://localhost:3001

### 4. 构建生产版本

```bash
npm run build        # 构建生产版本
npm run preview      # 预览构建结果
```

## 📡 API接口

### Mock服务器端点

#### 1. AI意图分析

```http
POST /api/analyze-intent
Content-Type: application/json

{
  "query": "我想吃披萨"
}
```

响应：

```json
{
  "success": true,
  "intent": "比价购物",
  "keywords": ["必胜客披萨", "达美乐披萨", "棒约翰披萨"],
  "platforms": ["美团", "饿了么", "京东到家"],
  "advice": "披萨建议选择连锁品牌，品质有保障，配送速度快。",
  "query": "我想吃披萨"
}
```

#### 2. 商品搜索

```http
GET /api/search-products?keyword=披萨&platform=美团
```

响应：

```json
{
  "success": true,
  "keyword": "披萨",
  "platform": "美团",
  "total": 4,
  "products": [
    {
      "id": 1,
      "name": "必胜客超级至尊披萨",
      "price": 89,
      "originalPrice": 108,
      "platform": "美团",
      "rating": 4.8,
      "sales": 1250,
      "deliveryTime": "30分钟",
      "urlScheme": "imeituan://",
      "image": "🍕"
    }
  ]
}
```

#### 3. AI日程规划

```http
POST /api/generate_schedule
Content-Type: application/json

{
  "query": "我想吃披萨，选了必胜客超级至尊披萨",
  "extra_info": {
    "shop_name": "必胜客中关村店",
    "address": "中关村大街1号"
  }
}
```

#### 4. 健康检查

```http
GET /api/health
```

## 🎯 使用流程

### 完整用户体验流程

1. **输入需求**：在比价页面输入自然语言需求
2. **AI分析**：AI分析意图，推荐关键词和平台
3. **比价展示**：展示全网比价结果，智能排序
4. **选择商品**：查看商品详情，选择最佳性价比
5. **一键购买**：直接打开购物App或跳转下载
6. **日程规划**：自动切换到日程规划页面
7. **生成日程**：智能规划购买时间，生成日历文件
8. **导入日历**：一键导入到Google/Outlook/系统日历

### 核心交互功能

#### 比价功能

- **智能搜索**：支持自然语言搜索
- **平台筛选**：按平台过滤商品
- **智能排序**：价格、评分、销量排序
- **最佳标识**：自动标识最佳性价比商品
- **App唤起**：一键打开购物App

#### 日程功能

- **自动填充**：比价结果自动填充到日程
- **智能规划**：AI根据商品信息规划时间
- **多格式导出**：.ics文件、Google日历、Outlook日历
- **系统集成**：支持Windows日历应用

## 🎨 设计特点

### 响应式设计

- **桌面端**：多列布局，丰富交互
- **平板端**：自适应布局，优化显示
- **移动端**：单列布局，触摸友好

### 用户体验

- **加载状态**：清晰的加载提示和动画
- **错误处理**：友好的错误提示和降级方案
- **成功反馈**：明确的操作成功反馈
- **数据持久**：页面间数据传递

### 视觉设计

- **渐变背景**：现代感的渐变背景
- **卡片设计**：圆角卡片，阴影效果
- **图标系统**：丰富的图标系统
- **动画效果**：平滑的过渡动画

## 🔧 配置选项

### 环境变量

#### .env.development

```env
VITE_USE_MOCK=true
```

#### .env.production

```env
VITE_USE_MOCK=false
```

### Mock数据配置

在 `mock-server.js` 中可以配置：

- 商品数据（披萨、咖啡、奶茶、手机等）
- 平台信息（美团、饿了么、京东、淘宝等）
- 价格策略和折扣信息
- 配送时间和评分数据

## 🧪 测试

### 功能测试

1. **比价功能测试**
   - 输入不同需求测试AI分析
   - 测试平台筛选和排序功能
   - 测试App唤起功能

2. **日程功能测试**
   - 测试数据传递功能
   - 测试日历文件生成
   - 测试日历导入功能

3. **集成测试**
   - 测试比价→日程完整流程
   - 测试Tab切换功能
   - 测试响应式布局

### API测试

```bash
# 测试健康检查
curl http://localhost:3001/api/health

# 测试意图分析
curl -X POST http://localhost:3001/api/analyze-intent \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"我想吃披萨\"}"

# 测试商品搜索
curl "http://localhost:3001/api/search-products?keyword=披萨"
```

## 📱 兼容性

### 浏览器支持

- Chrome 90+ ✅
- Firefox 88+ ✅
- Safari 14+ ✅
- Edge 90+ ✅

### 移动端支持

- iOS Safari ✅
- Android Chrome ✅
- 微信内置浏览器 ✅

### 日历应用支持

- Google日历 ✅
- Outlook日历 ✅
- Apple日历 ✅
- Windows日历 ✅
- 系统日历应用 ✅

## 🚨 故障排除

### 常见问题

#### 1. Mock服务器无法启动

```bash
# 检查端口占用
netstat -ano | findstr :3001

# 检查Node.js版本
node --version
```

#### 2. 前端无法访问

```bash
# 检查Vite服务器
npm run dev

# 检查依赖安装
npm install
```

#### 3. API调用失败

- 检查Mock服务器是否运行
- 检查CORS配置
- 检查网络连接

#### 4. 日历文件无法导入

- 检查.ics文件格式
- 检查日历应用权限
- 检查时间格式

### 调试技巧

1. **浏览器开发者工具**
   - 查看网络请求
   - 检查控制台错误
   - 调试JavaScript

2. **Mock模式调试**
   - 启用Mock模式测试前端逻辑
   - 修改Mock数据测试不同场景

3. **API调试**
   - 使用curl测试API端点
   - 查看Mock服务器日志

## 📈 扩展计划

### 短期计划

- [ ] 添加更多商品类别
- [ ] 集成真实电商API
- [ ] 添加用户账户系统
- [ ] 实现收藏和历史记录

### 长期计划

- [ ] 集成DeepSeek真实AI
- [ ] 添加语音输入功能
- [ ] 实现个性化推荐
- [ ] 开发移动端App

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

MIT License

## 🙏 致谢

- Vue 3 团队
- Element Plus 团队
- Vite 团队
- 所有开源贡献者

---

**AI生活助手** - 让AI为您的生活提供智能解决方案！
