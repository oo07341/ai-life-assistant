# app.py
# Flask 应用入口，负责创建应用实例、注册蓝图、配置跨域等

from flask import Flask           # Flask 框架核心类
from config import Config         # 导入配置类
from flask_cors import CORS       # 跨域资源共享支持
import logging                    # 日志模块

def create_app():
    """应用工厂函数，创建并配置 Flask 应用实例"""
    app = Flask(__name__)                     # 创建 Flask 实例
    app.config.from_object(Config)            # 从 Config 类加载配置

    # 启用 CORS，允许前端跨域访问（开发时尤其重要）
    CORS(app)

    # 配置日志记录，级别为 INFO，便于跟踪请求和错误
    logging.basicConfig(level=logging.INFO)

    # 导入蓝图对象（每个蓝图已在各自文件中定义了 url_prefix='/api'）
    from api.parse import parse_bp        # 一体化搜索接口
    from api.prices import price_bp       # 独立价格查询接口（可选）
    from api.schedule import schedule_bp  # 日程生成接口

    # 注册蓝图到应用
    app.register_blueprint(parse_bp)
    app.register_blueprint(price_bp)
    app.register_blueprint(schedule_bp)

    @app.route("/test")
    def test():
        from utils.response import success
        return success({"test": "hello"})

    # 根路径，用于健康检查或欢迎信息
    @app.route("/")
    def index():
        return {"msg": "AI Life Assistant Backend Running"}

    return app

# 当直接运行此文件时（而非被导入），启动开发服务器
if __name__ == "__main__":
    app = create_app()          # 创建应用实例
    app.run(host="127.0.0.1", port=5000, debug=True)         # 启动 Flask 开发服务器，debug=True 开启热重载和调试模式