# AI生活助手

一个基于Vue 3 + Flask的智能生活助手，提供AI智能比价和日程规划两大核心功能。

## 项目结构

```
ai-life-assistant/
├── backend/                 # Flask后端
│   ├── api/                # API接口
│   ├── services/           # 业务逻辑服务
│   ├── utils/              # 工具函数
│   ├── tests/              # 测试文件
│   ├── app.py              # Flask应用入口
│   ├── config.py           # 配置文件
│   └── requirements.txt    # Python依赖
├── src/                    # Vue前端
│   ├── components/         # 组件
│   ├── views/             # 页面视图
│   ├── router/            # 路由配置
│   ├── services/          # 前端服务
│   ├── App.vue            # 根组件
│   └── main.js            # 应用入口
├── public/                 # 静态资源
├── package.json           # 前端依赖
├── vite.config.js         # Vite配置
└── README.md              # 项目说明
```

## 功能特性

### 1. AI智能比价

- 自然语言输入解析用户意图
- 多平台商品比价（美团、饿了么等）
- 智能推荐最佳性价比商品
- 实时价格对比和筛选

### 2. AI日程规划

- 智能分析学习/工作目标
- 生成详细的时间安排计划
- 导出iCalendar格式日程
- 支持多科目/任务分配

### 3. 用户中心

- 个人资料管理
- 搜索历史记录
- 收藏的商品和计划

## 技术栈

### 前端

- Vue 3 + Composition API
- Element Plus UI组件库
- Vue Router 4
- Vite构建工具

### 后端

- Flask Web框架
- Flask-CORS跨域支持
- DeepSeek AI API集成
- ics日历生成库

## 快速开始

### 环境要求

- Node.js 16+
- Python 3.8+
- npm或yarn包管理器

### 安装步骤

1. **克隆项目**

```bash
git clone <repository-url>
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
   复制`.env.example`为`.env.development`并配置：

```bash
cp .env.example .env.development
```

编辑`.env.development`文件，设置DeepSeek API密钥等。

### 启动项目

#### 方法一：分别启动（推荐开发）

```bash
# 终端1：启动后端
cd backend
python app.py

# 终端2：启动前端
npm run dev
```

#### 方法二：使用启动脚本

```bash
# Windows
npm run start:win

# Linux/Mac
npm run start
```

### 访问应用

- 前端：http://localhost:5173
- 后端API：http://localhost:3001

## API接口

### 主要接口

#### 1. 意图分析

```
POST /api/search
请求体：{"query": "用户输入文本"}
响应：意图分析结果 + 商品推荐
```

#### 2. 商品搜索

```
POST /api/prices
请求体：{"keywords": ["关键词1", "关键词2"]}
响应：比价结果列表
```

#### 3. 日程生成

```
POST /api/schedule
请求体：{"schedule_info": {...}}
响应：日程计划 + iCalendar内容
```

#### 4. 用户相关

- `GET /api/user/profile` - 获取用户信息
- `PUT /api/user/profile` - 更新用户信息
- `GET /api/user/history` - 获取历史记录

#### 5. 计划管理

- `GET /api/plan` - 获取计划列表
- `POST /api/plan` - 创建计划
- `PUT /api/plan/:id` - 更新计划
- `DELETE /api/plan/:id` - 删除计划

## 开发指南

### 前端开发

```bash
# 开发模式
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

### 后端开发

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动开发服务器
python app.py
```

### 代码规范

- 前端使用ESLint + Prettier
- 后端遵循PEP 8规范
- 提交前运行代码检查

## 部署

### 前端部署

```bash
npm run build
# 将dist目录部署到静态服务器
```

### 后端部署

```bash
# 使用Gunicorn部署
cd backend
gunicorn -w 4 -b 0.0.0.0:3001 app:app
```

## 常见问题

### 1. 跨域问题

确保后端已启用CORS，前端配置正确的API地址。

### 2. DeepSeek API密钥

需要在`.env.development`中配置有效的DeepSeek API密钥。

### 3. 端口冲突

如果端口被占用，可以修改：

- 前端：修改`.env.development`中的`VITE_API_BASE_URL`
- 后端：修改`backend/app.py`中的端口号

### 4. 依赖安装失败

- 确保使用正确的Python版本（3.8+）
- 使用虚拟环境管理Python依赖
- 清除npm缓存：`npm cache clean --force`

## 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License
