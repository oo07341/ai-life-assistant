# 意图解析
# DeepSeek封装
import json
import requests
from config import Config
from flask import current_app

def parse_intent(query: str) -> dict:
    """
    调用 DeepSeek API 解析用户意图
    返回标准结构，永不抛异常
    """

    # 默认返回值，防止任何异常导致接口崩溃
    default_response = {
        "intent": "general",
        "product_keywords": [],
        "time_intent": "",
        "category": "",  # 商品品类，默认为空
        "price_range": None  # 价格区间，默认为 None
    }

    # 1. 基础校验
    if not query or not isinstance(query, str):
        return default_response

    # 构造请求头
    headers = {
        "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    # 构造请求体
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一个智能助理的意图解析器。请将用户的自然语言输入转换为 JSON 格式输出，"
                    "严格按照以下字段："
                    "- intent: 意图类型，可选 'shopping', 'event', 'general'"
                    "- product_keywords: 用于搜索商品的关键词数组"
                    "- category: 商品大致分类"
                    "- price_range: 价格区间描述，如 '50-100'"
                    "- time_intent: 提取的时间表述，如 '今晚', '周末'"
                    "只输出合法 JSON，不要包含其他文字。"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.1,   # 保证输出稳定、结构化
        "max_tokens": 300  # 限制返回的最大 token 数，避免过长回复
    }

    try:
        # 2. 请求 DeepSeek
        resp = requests.post(
            Config.DEEPSEEK_API_URL,
            headers=headers,
            json=payload,
            timeout=10  # 防止请求卡死
        )
        resp.raise_for_status()  # HTTP 错误直接抛异常

        # 安全提取返回内容
        content = resp.json() \
                      .get("choices", [{}])[0] \
                      .get("message", {}) \
                      .get("content", "")

        # 3. 容错解析 JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # 尝试去掉 ```json ``` 这种包裹
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)

        # 4. 字段兜底（防止缺字段报错）
        result.setdefault("intent", "general")
        result.setdefault("product_keywords", [])
        result.setdefault("time_intent", "")
        result.setdefault("category", "")
        result.setdefault("price_range", None)

        return result

    except requests.RequestException as e:
        # 兼容非 Flask 环境：尝试用 current_app.logger，失败则用 print
        try:
            from flask import current_app
            current_app.logger.error(f"DeepSeek API error: {e}")
        except RuntimeError:
            print(f"[ERROR] DeepSeek API error: {e}")
        return default_response
    except Exception as e:
        try:
            from flask import current_app
            current_app.logger.error(f"Unexpected error: {e}")
        except RuntimeError:
            print(f"[ERROR] Unexpected error: {e}")
        return default_response