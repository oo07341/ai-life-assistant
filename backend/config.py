# 配置（DeepSeek /环境)
import os
from dotenv import load_dotenv
load_dotenv()  # 自动读取 .env


class Config:
    DEBUG = True
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
    DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"