@echo off
echo ========================================
echo   AI Life Assistant 启动脚本
echo ========================================
echo.

echo 1. 检查前端依赖...
if not exist "node_modules" (
    echo   安装前端依赖...
    call npm install
) else (
    echo   前端依赖已安装
)

echo.
echo 2. 检查后端依赖...
cd backend
python -c "import flask, flask_cors, requests, dotenv, ics, tatsu, sqlalchemy, pymysql, cryptography, flask_sqlalchemy" 2>nul
if errorlevel 1 (
    echo   安装后端依赖...
    pip install -r requirements.txt
) else (
    echo   后端依赖已安装
)
cd ..

echo.
echo 3. 启动后端服务...
start cmd /k "cd backend && python app.py"
echo   后端启动中... (http://localhost:3001)

echo.
echo 4. 启动前端开发服务器...
start cmd /k "npm run dev"
echo   前端启动中... (http://localhost:5173)

echo.
echo ========================================
echo   启动完成！
echo   前端: http://localhost:5173
echo   后端: http://localhost:3001
echo ========================================
echo.
echo 按任意键打开浏览器访问前端...
pause >nul
start http://localhost:5173