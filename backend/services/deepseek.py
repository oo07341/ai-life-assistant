# 意图解析
# DeepSeek封装
import json
import requests
from config import Config



def parse_intent(query: str) -> dict:
    """
    调用 DeepSeek API 解析用户意图
    返回标准结构，永不抛异常
    """

    # 默认返回值，防止任何异常导致接口崩溃
    default_response = {
        "intent": "general",
        "product_keywords": [],
        "location_hint": "不限",
        "schedule_info": {
            "goal": "",
            "target_date": None,
            "daily_hours": 4,
            "subjects": []
        }
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
                    "你是一个校园生活助手的意图解析器。分析用户输入，返回严格 JSON 格式。\n"
                    "字段说明：\n"
                    "- intent: 'shopping'（想买东西/点外卖）或 'schedule'（制定计划/日程）或 'general'\n"
                    "- product_keywords: 商品关键词数组，如 ['披萨','麻辣烫']\n"
                    "- schedule_info: 对象，仅当 intent='schedule' 时提供，包含：\n"
                    "    - goal: 目标类型，如 '考研'、'期末考'、'比赛'、'考证' 或具体描述\n"
                    "    - target_date: YYYY-MM-DD 格式，未提及则为 null\n"
                    "    - daily_hours: 每日可用小时数，未提及默认为 4\n"
                    "    - subjects: 科目/任务列表，如 ['高数','英语']\n"
                    "- location_hint: '校内'、'校外' 或 '不限'，默认不限\n"
                    "只输出 JSON，无其他文字。"
                )
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "temperature": 0.1,   # 保证输出稳定、结构化
        "max_tokens": 400  # 限制返回的最大 token 数，避免过长回复
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

        # 3. 防御：空字符串直接返回默认值
        content = content.strip()
        if not content:
            return default_response

        # 4. 容错解析 JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            # 尝试去掉 ```json ``` 这种包裹
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)

        # 5. 字段兜底（防止缺字段报错）
        result.setdefault("intent", "general")
        result.setdefault("product_keywords", [])
        result.setdefault("location_hint", "不限")

        # 如果意图是日程，确保 schedule_info 存在且结构完整
        if result.get("intent") == "schedule":
            schedule_info = result.get("schedule_info")
            if not isinstance(schedule_info, dict):
                schedule_info = {}
            # 补全 schedule_info 子字段
            schedule_info.setdefault("goal", "期末考")
            schedule_info.setdefault("target_date", None)
            schedule_info.setdefault("daily_hours", 4)
            schedule_info.setdefault("subjects", ["复习"])
            result["schedule_info"] = schedule_info
        else:
            # 非日程意图，依然提供空对象避免前端 undefined
            result["schedule_info"] = None

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