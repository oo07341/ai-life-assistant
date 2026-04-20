# config.py
import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


class Config:
    # Flask 配置
    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # DeepSeek API 配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

    # 数据库配置
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")
    
    if DB_TYPE == "sqlite":
        # SQLite配置
        DB_PATH = os.getenv("DB_PATH", "./ai_life_assistant.db")
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    else:
        # MySQL配置
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = int(os.getenv("DB_PORT", 3306))
        DB_USER = os.getenv("DB_USER", "root")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "")
        DB_NAME = os.getenv("DB_NAME", "ai_life_assistant")
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
            "?charset=utf8mb4"
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQL_ECHO", "False").lower() == "true"  # 调试时可设为 True
