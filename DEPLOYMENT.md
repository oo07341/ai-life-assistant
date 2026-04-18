# AI生活助手 - 部署指南

## 部署概述

本文档提供AI生活助手项目的完整部署指南，包括开发环境、生产环境和云平台部署。

## 环境要求

### 系统要求

- **Node.js**: 18.x 或更高版本
- **npm**: 8.x 或更高版本
- **操作系统**: Windows 10+, macOS 10.15+, Linux

### 浏览器要求

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 开发环境部署

### 1. 克隆项目

```bash
git clone https://github.com/oo07341/ai-life-assistant.git
cd ai-life-assistant
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

```bash
# 开发环境配置（已包含）
# .env.development 文件已存在
```

### 4. 启动开发服务器

```bash
# 同时启动前端和Mock服务器（推荐）
npm run dev:full

# 或分别启动
npm run mock:server  # Mock服务器 (http://localhost:3001)
npm run dev          # 前端开发服务器 (http://localhost:5173)
```

### 5. 访问应用

- **前端应用**: http://localhost:5173
- **Mock API**: http://localhost:3001

## 生产环境部署

### 1. 构建项目

```bash
# 安装依赖（如果尚未安装）
npm install

# 构建生产版本
npm run build
```

构建完成后，会在 `dist` 目录生成静态文件。

### 2. 配置生产环境

```bash
# 确保生产环境配置正确
# .env.production 文件应包含：
VITE_USE_MOCK=false
```

### 3. 部署静态文件

将 `dist` 目录中的文件部署到Web服务器：

#### Nginx配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/ai-life-assistant;
    index index.html;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

    # 缓存设置
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # SPA路由支持
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

#### Apache配置示例

```apache
<VirtualHost *:80>
    ServerName your-domain.com
    DocumentRoot /var/www/ai-life-assistant

    <Directory /var/www/ai-life-assistant>
        Options Indexes FollowSymLinks
        AllowOverride All
        Require all granted

        # SPA路由支持
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>
</VirtualHost>
```

### 4. 配置HTTPS（推荐）

使用Let's Encrypt获取免费SSL证书：

```bash
# 安装Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com
```

## Docker部署

### 1. 创建Dockerfile

```dockerfile
# 构建阶段
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# 生产阶段
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 2. 创建nginx.conf

```nginx
events {
    worker_connections 1024;
}

http {
    include /etc/nginx/mime.types;
    default_type application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        # Gzip压缩
        gzip on;
        gzip_vary on;
        gzip_min_length 1024;
        gzip_types text/plain text/css text/xml text/javascript application/javascript application/xml+rss application/json;

        # 缓存设置
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }

        # SPA路由支持
        location / {
            try_files $uri $uri/ /index.html;
        }
    }
}
```

### 3. 构建和运行Docker容器

```bash
# 构建Docker镜像
docker build -t ai-life-assistant .

# 运行容器
docker run -d -p 80:80 --name ai-life-assistant ai-life-assistant
```

## 云平台部署

### Vercel部署

1. 导入GitHub仓库到Vercel
2. 配置构建命令：`npm run build`
3. 输出目录：`dist`
4. 环境变量：`VITE_USE_MOCK=false`

### Netlify部署

1. 导入GitHub仓库到Netlify
2. 构建命令：`npm run build`
3. 发布目录：`dist`
4. 环境变量：`VITE_USE_MOCK=false`

### GitHub Pages部署

1. 在 `vite.config.js` 中设置 `base`：

```javascript
export default defineConfig({
  base: "/ai-life-assistant/",
  // ...其他配置
});
```

2. 创建部署脚本：

```bash
#!/bin/bash
npm run build
cd dist
git init
git add -A
git commit -m 'deploy'
git push -f git@github.com:oo07341/ai-life-assistant.git main:gh-pages
cd -
```

## 环境变量配置

### 开发环境 (.env.development)

```env
VITE_USE_MOCK=true
```

### 生产环境 (.env.production)

```env
VITE_USE_MOCK=false
```

### 自定义环境变量

如果需要添加其他环境变量：

1. 在 `.env` 文件中定义变量：`VITE_API_URL=https://api.example.com`
2. 在代码中访问：`import.meta.env.VITE_API_URL`

## 监控和维护

### 应用监控

1. **错误监控**：集成Sentry或类似服务
2. **性能监控**：使用Google Analytics或类似工具
3. **用户分析**：跟踪用户行为和功能使用情况

### 日志管理

1. **前端日志**：使用console.log和错误捕获
2. **服务器日志**：Nginx/Apache访问日志和错误日志
3. **应用日志**：如果需要，集成日志服务

### 备份策略

1. **代码备份**：GitHub仓库自动备份
2. **数据备份**：如果有数据库，定期备份
3. **配置文件备份**：备份环境变量和配置文件

## 性能优化

### 构建优化

```bash
# 分析构建大小
npm run build -- --report

# 查看依赖大小
npx vite-bundle-analyzer
```

### 运行时优化

1. **代码分割**：Vite自动处理
2. **懒加载**：按需加载组件
3. **缓存策略**：合理设置HTTP缓存头
4. **CDN加速**：使用CDN分发静态资源

### 图片优化

1. **格式选择**：使用WebP格式
2. **尺寸优化**：根据设备加载合适尺寸
3. **懒加载**：图片滚动到视口再加载

## 安全配置

### HTTPS配置

```nginx
# Nginx SSL配置
ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
```

### 安全头设置

```nginx
# 安全HTTP头
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:;" always;
```

### 速率限制

```nginx
# API速率限制
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

location /api/ {
    limit_req zone=api burst=20 nodelay;
    proxy_pass http://localhost:3001;
}
```

## 故障排除

### 常见问题

#### 1. 构建失败

```bash
# 清理缓存
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

#### 2. 端口冲突

```bash
# 检查端口占用
netstat -ano | findstr :5173
netstat -ano | findstr :3001

# 杀死占用进程
taskkill /PID <PID> /F
```

#### 3. 环境变量不生效

```bash
# 检查环境文件
cat .env.development
cat .env.production

# 重启开发服务器
npm run dev
```

#### 4. 路由问题（SPA）

确保Web服务器配置了SPA路由支持：

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

### 调试命令

```bash
# 检查Node.js版本
node --version

# 检查npm版本
npm --version

# 检查依赖
npm list

# 测试API
curl http://localhost:3001/api/health
```

## 更新和维护

### 更新依赖

```bash
# 检查过时依赖
npm outdated

# 更新依赖
npm update

# 更新特定包
npm update package-name
```

### 项目更新

1. 拉取最新代码：`git pull origin main`
2. 更新依赖：`npm install`
3. 重新构建：`npm run build`
4. 重启服务

### 备份和恢复

```bash
# 备份项目
tar -czf ai-life-assistant-backup-$(date +%Y%m%d).tar.gz .

# 恢复项目
tar -xzf ai-life-assistant-backup-20240418.tar.gz
npm install
```

## 联系和支持

### 问题报告

1. GitHub Issues: https://github.com/oo07341/ai-life-assistant/issues
2. 邮件支持: support@example.com

### 文档资源

1. 项目文档: README.md
2. 开发文档: DEVELOPMENT.md
3. API文档: README-schedule.md

### 社区支持

- GitHub Discussions
- Stack Overflow (标签: vue3, vite, element-plus)

---

**最后更新**: 2026-04-18  
**版本**: 1.0.0  
**状态**: 生产就绪

> 注意：本文档会随着项目更新而更新，请定期查看最新版本。
