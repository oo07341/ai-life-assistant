# AI生活助手 - 开发文档

## 项目概述

AI生活助手是一个基于Vue 3 + Element Plus的智能生活工具，结合了AI智能比价和日程规划两大核心功能。

## 技术架构

### 前端架构

```
Vue 3 (Composition API)
├── Element Plus (UI组件库)
├── Vite (构建工具)
├── ics (日历生成库)
└── CSS3 + Flexbox/Grid (样式)
```

### 后端架构

```
Node.js + Express
├── Mock API服务器
├── RESTful API设计
└── CORS支持
```

## 核心组件

### 1. PriceComparison.vue (AI智能比价组件)

- **功能**：自然语言比价搜索、AI意图分析、多平台比价展示
- **状态管理**：Vue Composition API (ref, computed)
- **数据流**：用户输入 → AI分析 → 比价结果 → 商品选择
- **事件**：`add-to-schedule` (传递选中商品到日程规划)

### 2. ScheduleGenerator.vue (AI日程规划组件)

- **功能**：接收比价结果、调用AI日程API、生成.ics日历文件
- **Props**：`selected-product`, `search-query`
- **状态管理**：响应式数据 + 环境变量控制
- **特性**：Mock模式切换、多层错误处理、多日历格式支持

### 3. Home.vue (主视图组件)

- **功能**：整合比价和日程功能、Tab导航、用户引导
- **布局**：响应式设计、移动端适配
- **状态管理**：Tab状态、选中商品、搜索查询

## 数据流

### 正向流程

```
用户输入 → PriceComparison组件 → AI分析 → 比价结果
    ↓
商品选择 → add-to-schedule事件 → Home组件接收
    ↓
Tab切换 → ScheduleGenerator组件 → 自动填充数据
    ↓
生成日程 → API调用/Mock数据 → .ics文件生成
    ↓
浏览器下载 → 日历应用导入
```

### 错误处理流程

```
API调用失败 → 降级到Mock数据 → Mock数据失败
    ↓
显示错误信息 → 提供重试选项 → 用户重试
```

## 环境配置

### 开发环境 (.env.development)

```env
VITE_USE_MOCK=true
```

### 生产环境 (.env.production)

```env
VITE_USE_MOCK=false
```

## Mock服务器

### 启动命令

```bash
npm run mock:server      # 单独启动Mock服务器
npm run dev:full         # 同时启动前端和Mock服务器
```

### API端点

1. `POST /api/generate_schedule` - AI日程规划
2. `GET /api/health` - 健康检查

### Mock数据配置

在 `mock-server.js` 中配置：

- 商品数据
- 平台信息
- 价格策略
- 日程事件模板

## 开发指南

### 1. 添加新功能

1. 在对应组件中添加功能模块
2. 更新状态管理和事件处理
3. 添加样式和响应式设计
4. 测试功能完整性

### 2. 修改现有功能

1. 理解当前数据流和状态管理
2. 在对应位置进行修改
3. 确保向后兼容性
4. 测试修改后的功能

### 3. 调试技巧

- **前端调试**：浏览器开发者工具 + Vue Devtools
- **API调试**：curl命令测试API端点
- **Mock调试**：修改Mock数据测试不同场景
- **错误调试**：查看控制台日志和网络请求

## 测试指南

### 单元测试重点

1. **PriceComparison组件**
   - 搜索功能测试
   - AI分析模拟测试
   - 比价结果排序测试

2. **ScheduleGenerator组件**
   - 数据接收测试
   - API调用测试
   - 日历生成测试
   - 错误处理测试

3. **集成测试**
   - 比价→日程完整流程
   - Tab切换功能
   - 响应式布局测试

### 端到端测试场景

1. **正常流程**：搜索披萨 → 选择商品 → 生成日程
2. **异常流程**：网络错误 → Mock降级 → 重试机制
3. **边界情况**：空输入、超时处理、大屏/小屏适配

## 部署指南

### 开发环境部署

1. 安装依赖：`npm install`
2. 启动开发服务器：`npm run dev:full`
3. 访问应用：http://localhost:5173

### 生产环境部署

1. 构建项目：`npm run build`
2. 部署dist目录到Web服务器
3. 配置生产环境变量
4. 启动生产服务器

### Docker部署（可选）

```dockerfile
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 性能优化

### 前端优化

1. **代码分割**：按需加载组件
2. **图片优化**：使用WebP格式，懒加载
3. **缓存策略**：合理设置HTTP缓存头
4. **资源压缩**：Gzip/Brotli压缩

### 构建优化

1. **Tree Shaking**：移除未使用代码
2. **代码分割**：分割vendor和业务代码
3. **预加载**：关键资源预加载
4. **PWA支持**：添加Service Worker

## 安全考虑

### 前端安全

1. **XSS防护**：Vue自动转义，避免innerHTML
2. **CSRF防护**：API请求添加CSRF令牌
3. **CSP配置**：内容安全策略
4. **输入验证**：用户输入验证和清理

### API安全

1. **速率限制**：防止API滥用
2. **输入验证**：请求参数验证
3. **错误处理**：避免信息泄露
4. **HTTPS**：生产环境强制HTTPS

## 扩展计划

### 短期扩展

1. 添加更多商品类别
2. 集成真实电商API
3. 添加用户账户系统
4. 实现收藏和历史记录

### 长期扩展

1. 集成真实AI服务
2. 添加语音输入功能
3. 实现个性化推荐
4. 开发移动端App

## 故障排除

### 常见问题

1. **Mock服务器无法启动**：检查端口占用，Node.js版本
2. **前端编译错误**：检查依赖安装，Vue版本兼容性
3. **API调用失败**：检查CORS配置，网络连接
4. **日历文件无法导入**：检查.ics格式，日历应用权限

### 调试命令

```bash
# 检查端口占用
netstat -ano | findstr :3001
netstat -ano | findstr :5173

# 检查Node.js版本
node --version

# 测试API端点
curl http://localhost:3001/api/health
```

## 贡献指南

1. Fork项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

MIT License - 详见LICENSE文件

---

**最后更新**：2026-04-18
**版本**：1.0.0
**状态**：生产就绪
