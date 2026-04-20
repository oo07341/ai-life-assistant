# 喂来日程 - AI生活助手

一个基于Vue 3 + Flask的智能生活助手，提供一点外卖、价格查询、智能搜索和未来日程管理等核心功能。

## 🚀 功能特性

### 1. 智能搜索

- **自然语言意图分析**：智能解析用户输入，识别购物、日程等意图
- **降级机制**：当AI服务不可用时，自动切换到本地关键词分析
- **多平台比价**：自动比较美团、饿了么等平台的价格
- **实时推荐**：根据用户意图推荐最佳商品和方案

### 2. 一点外卖（PriceDetail）

- **详细比价**：展示商品的详细价格、评分、配送信息
- **多维度筛选**：支持价格、评分、配送时间等筛选
- **收藏功能**：支持收藏感兴趣的商品
- **历史记录**：自动保存浏览历史

### 3. 价格查询（PriceSearch）

- **快速比价**：输入关键词快速获取多平台价格对比
- **批量搜索**：支持多个关键词同时搜索
- **结果排序**：按价格、评分、销量等排序
- **导出功能**：支持结果导出为CSV格式

### 4. 未来日程管理

- **智能计划生成**：根据学习/工作目标生成详细时间安排
- **进度跟踪**：实时跟踪计划完成进度
- **日历导出**：支持导出iCalendar格式日程
- **多任务管理**：支持同时管理多个学习/工作计划

### 5. 用户中心

- **个人资料**：完善的用户信息管理
- **统一历史**：集中查看搜索、比价、计划历史
- **系统设置**：个性化主题、通知等设置
- **帮助指南**：详细的使用说明和常见问题解答

### 6. 智能错误处理

- **分级错误提示**：根据错误类型提供不同的用户指导
- **降级策略**：从AI服务到本地分析到演示数据的完整降级链
- **友好空状态**：数据为空时显示友好的提示信息
- **实时反馈**：操作结果实时反馈给用户

## 🛠️ 技术栈

### 前端技术

- **Vue 3** + Composition API - 现代化的前端框架
- **Element Plus** - 企业级UI组件库
- **Vue Router 4** - 路由管理
- **Vite** - 下一代前端构建工具
- **Axios** - HTTP客户端
- **LocalStorage** - 本地数据存储

### 后端技术

- **Flask** - 轻量级Python Web框架
- **Flask-CORS** - 跨域资源共享支持
- **DeepSeek API** - AI意图分析服务
- **ics** - iCalendar文件生成库
- **SQLite** - 轻量级数据库（开发环境）
- **JSON Web Tokens** - 用户认证

### 架构特点

- **前后端分离**：清晰的API接口设计
- **统一认证**：基于X-User-Id头部的认证机制
- **错误分层**：从网络错误到业务错误的完整处理
- **响应式设计**：支持桌面端和移动端
- **主题切换**：支持亮色/深色主题

## 📁 项目结构

```
ai-life-assistant/
├── backend/                 # Flask后端
│   ├── api/                # API接口层
│   │   ├── __init__.py
│   │   ├── parse.py        # 意图分析API
│   │   ├── plan.py         # 计划管理API
│   │   ├── price.py        # 价格查询API
│   │   ├── schedule.py     # 日程生成API
│   │   └── user.py         # 用户管理API
│   ├── services/           # 业务逻辑层
│   │   ├── deepseek.py     # DeepSeek AI服务
│   │   └── local_analyzer.py # 本地意图分析（降级方案）
│   ├── utils/              # 工具函数
│   ├── tests/              # 测试文件
│   ├── app.py              # Flask应用入口
│   ├── config.py           # 配置文件
│   ├── models.py           # 数据模型
│   └── requirements.txt    # Python依赖
├── src/                    # Vue前端
│   ├── components/         # 可复用组件
│   │   └── profile/        # 个人中心组件
│   │       ├── UserInfo.vue           # 用户信息
│   │       ├── UnifiedHistory.vue     # 统一历史
│   │       ├── SystemSettings.vue     # 系统设置
│   │       └── HelpGuide.vue          # 帮助指南
│   ├── views/             # 页面视图
│   │   ├── Login.vue                  # 登录页面
│   │   ├── Register.vue               # 注册页面
│   │   ├── Profile.vue                # 个人中心
│   │   ├── Search.vue                 # 智能搜索
│   │   ├── PriceSearch.vue            # 价格查询
│   │   ├── PriceDetail.vue            # 一点外卖详情
│   │   ├── Plans.vue                  # 计划管理
│   │   └── ScheduleDetail.vue         # 日程详情
│   ├── router/            # 路由配置
│   │   └── index.js
│   ├── services/          # 前端服务
│   │   └── api.js         # 统一的API服务层
│   ├── App.vue            # 根组件
│   └── main.js            # 应用入口
├── public/                 # 静态资源
├── package.json           # 前端依赖
├── vite.config.js         # Vite配置
├── start.bat              # Windows启动脚本
└── README.md              # 项目说明
```

## 🚀 快速开始

### 环境要求

- **Node.js** 16+
- **Python** 3.8+
- **npm** 或 **yarn** 包管理器

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/oo07341/ai-life-assistant.git
cd ai-life-assistant
```

2. **安装前端依赖**

```bash
npm install
```

3. **安装后端依赖**

```bash
cd backend
pip install -r requirements.txt
cd ..
```

4. **配置环境变量**

```bash
# 复制环境变量模板
cp .env.example .env.development
```

编辑`.env.development`文件，配置以下内容：

```env
# 前端配置
VITE_API_BASE_URL=http://localhost:3001

# 后端配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
FLASK_ENV=development
FLASK_DEBUG=true
```

### 启动项目

#### 方法一：分别启动（推荐开发）

```bash
# 终端1：启动后端服务（端口3001）
cd backend
python app.py

# 终端2：启动前端开发服务器（端口5175）
npm run dev
```

#### 方法二：使用启动脚本（Windows）

```bash
# 双击start.bat或运行
start.bat
```

### 访问应用

- **前端应用**：http://localhost:5175
- **后端API**：http://localhost:3001

### 测试用户

系统默认使用测试用户ID：`test_user_001`

- 可以使用任意邮箱密码登录
- 所有用户相关API会自动使用该测试用户ID

## 📡 API接口文档

### 认证机制

所有用户相关API需要在请求头部添加：

```http
X-User-Id: test_user_001
```

### 主要接口

#### 1. 智能搜索（支持降级机制）

```http
POST /api/search
Content-Type: application/json

请求体：
{
  "query": "我想吃披萨"
}

响应：
{
  "code": 0,
  "data": {
    "intent": "shopping",
    "keywords": ["披萨"],
    "location_hint": null,
    "platforms": ["美团", "饿了么"],
    "hot_keywords": ["奶茶", "咖啡", "汉堡"]
  },
  "msg": "success"
}
```

**降级机制**：当DeepSeek API不可用时，自动切换到本地关键词分析。

#### 2. 价格查询

```http
POST /api/prices
Content-Type: application/json
X-User-Id: test_user_001

请求体：
{
  "keywords": ["披萨", "奶茶"]
}

响应：
{
  "code": 0,
  "data": {
    "results": [
      {
        "keyword": "披萨",
        "platforms": [
          {"name": "美团", "price": 68, "rating": 4.5},
          {"name": "饿了么", "price": 72, "rating": 4.3}
        ]
      }
    ]
  },
  "msg": "success"
}
```

#### 3. 用户管理

```http
# 获取用户信息
GET /api/user/profile
X-User-Id: test_user_001

# 获取用户计划列表
GET /api/user/plans
X-User-Id: test_user_001

# 获取用户历史记录
GET /api/user/history
X-User-Id: test_user_001
```

#### 4. 计划管理

```http
# 保存新计划
POST /api/plan/save
Content-Type: application/json
X-User-Id: test_user_001

# 更新计划进度
POST /api/plan/update-progress
Content-Type: application/json
X-User-Id: test_user_001

# 合并计划
POST /api/plan/merge
Content-Type: application/json
X-User-Id: test_user_001
```

#### 5. 日程生成

```http
POST /api/schedule
Content-Type: application/json

请求体：
{
  "schedule_info": {
    "goal": "学习Vue 3",
    "target_date": "2026-05-15",
    "daily_hours": 6,
    "subjects": ["Vue基础", "组件开发", "状态管理"]
  }
}
```

## 🗄️ 数据库设计

### 核心数据表

#### 1. users 用户表

| 字段       | 类型               | 说明           |
| ---------- | ------------------ | -------------- |
| id         | INT PRIMARY KEY    | 用户ID         |
| user_uuid  | VARCHAR(36) UNIQUE | 前端生成的UUID |
| nickname   | VARCHAR(64)        | 用户昵称       |
| email      | VARCHAR(255)       | 邮箱地址       |
| created_at | DATETIME           | 创建时间       |
| updated_at | DATETIME           | 更新时间       |

#### 2. plans 计划表

| 字段          | 类型               | 说明           |
| ------------- | ------------------ | -------------- |
| id            | INT PRIMARY KEY    | 计划ID         |
| plan_uuid     | VARCHAR(36) UNIQUE | 计划唯一标识   |
| user_id       | INT                | 用户ID（外键） |
| goal          | VARCHAR(128)       | 计划目标       |
| schedule_info | JSON               | 原始计划信息   |
| schedule_data | JSON               | 生成的日程数据 |
| is_active     | BOOLEAN            | 是否激活       |
| progress      | INT                | 完成进度       |
| created_at    | DATETIME           | 创建时间       |

#### 3. search_history 搜索历史表

| 字段       | 类型            | 说明       |
| ---------- | --------------- | ---------- |
| id         | INT PRIMARY KEY | 记录ID     |
| user_id    | INT             | 用户ID     |
| query      | VARCHAR(255)    | 搜索关键词 |
| intent     | VARCHAR(32)     | 意图类型   |
| results    | JSON            | 搜索结果   |
| created_at | DATETIME        | 搜索时间   |

## 🛠️ 开发指南

### 前端开发

```bash
# 开发模式（热重载）
npm run dev

# 代码检查
npm run lint

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### 后端开发

```bash
# 进入后端目录
cd backend

# 安装依赖（使用虚拟环境推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# 启动开发服务器
python app.py

# 运行测试
python -m pytest tests/
```

### 代码规范

- **前端**：ESLint + Prettier，遵循Vue 3最佳实践
- **后端**：遵循PEP 8规范，使用类型提示
- **提交信息**：使用约定式提交（Conventional Commits）
- **Git工作流**：功能分支 + Pull Request

## 🚢 部署指南

### 前端部署

```bash
# 构建生产版本
npm run build

# 部署到静态服务器（如Nginx）
# dist目录包含所有静态资源
```

### 后端部署

```bash
# 使用Gunicorn部署（生产环境）
cd backend
gunicorn -w 4 -b 0.0.0.0:3001 app:app

# 使用Docker部署
docker build -t ai-life-assistant-backend .
docker run -p 3001:3001 ai-life-assistant-backend
```

### 环境配置

生产环境需要配置：

1. **数据库**：MySQL/PostgreSQL（替换SQLite）
2. **缓存**：Redis（可选）
3. **文件存储**：云存储或本地存储
4. **监控**：日志收集和性能监控

## 🔧 常见问题与解决方案

### 1. 智能搜索失败

**问题**：DeepSeek API服务不可用
**解决方案**：

- 系统自动切换到本地关键词分析
- 支持购物意图（吃、外卖、披萨等关键词）
- 支持日程意图（计划、学习、会议等关键词）
- 提供友好的错误提示和降级说明

### 2. 计划数据加载失败

**问题**：API返回401错误或数据格式不匹配
**解决方案**：

- 修复用户认证，自动添加X-User-Id头部
- 正确处理API返回的数据结构（{ plans: [] }）
- 优化错误处理，提供详细的错误分类
- 添加演示数据作为后备方案

### 3. 用户登录无法跳转

**问题**：登录后页面不跳转
**解决方案**：

- 修复登录逻辑，保存正确的userId到localStorage
- 确保API服务使用一致的测试用户ID
- 优化路由跳转逻辑

### 4. 导航栏功能缺失

**问题**：缺少"一点外卖"等菜单项
**解决方案**：

- 添加完整的导航菜单系统
- 包含：首页、智能搜索、价格查询、一点外卖、未来日程、计划管理、个人中心
- 支持响应式设计（桌面端和移动端）

### 5. 跨域问题

**解决方案**：

- 后端已配置Flask-CORS支持
- 前端配置正确的API基础URL
- 开发环境使用代理配置

### 6. 环境变量配置

**解决方案**：

- 提供完整的.env.example模板
- 详细的配置说明文档
- 开发和生产环境分离配置

## 🤝 贡献指南

我们欢迎任何形式的贡献！请遵循以下步骤：

1. **Fork项目**
2. **创建功能分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **提交更改**
   ```bash
   git commit -m 'feat: add amazing feature'
   ```
4. **推送到分支**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **创建Pull Request**

### 贡献规范

- 遵循现有的代码风格和项目结构
- 添加适当的测试用例
- 更新相关文档
- 确保代码通过所有检查

## 📞 支持与反馈

如果您遇到问题或有建议：

1. 查看[常见问题](#常见问题与解决方案)部分
2. 检查项目Issues中是否已有类似问题
3. 创建新的Issue，提供详细的问题描述
4. 包括：环境信息、复现步骤、期望行为、实际行为

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

---

**最后更新**：2026年4月20日  
**版本**：1.0.0  
**状态**：稳定运行，功能完整
