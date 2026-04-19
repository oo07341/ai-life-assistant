# 意图解析
# DeepSeek封装
# services/deepseek.py
import json
import requests
from config import Config

def parse_intent(query: str) -> dict:
    """调用 DeepSeek API 解析用户意图（保持不变）"""
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

    if not query or not isinstance(query, str):
        return default_response

    headers = {
        "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

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
        "temperature": 0.1,
        "max_tokens": 400
    }

    try:
        resp = requests.post(Config.DEEPSEEK_API_URL, headers=headers, json=payload, timeout=10)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        if not content:
            return default_response

        # 解析 JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)

        # 补全字段
        result.setdefault("intent", "general")
        result.setdefault("product_keywords", [])
        result.setdefault("location_hint", "不限")

        if result.get("intent") == "schedule":
            schedule_info = result.get("schedule_info")
            if not isinstance(schedule_info, dict):
                schedule_info = {}
            schedule_info.setdefault("goal", "期末考")
            schedule_info.setdefault("target_date", None)
            schedule_info.setdefault("daily_hours", 4)
            schedule_info.setdefault("subjects", ["复习"])
            result["schedule_info"] = schedule_info
        else:
            result["schedule_info"] = None

        return result

    except Exception as e:
        print(f"[ERROR] parse_intent failed: {e}")
        return default_response


def generate_ai_schedule(goal: str, target_date: str, daily_hours: float = 4.0, subjects: list = None) -> dict:
    """
    调用 DeepSeek API 生成个性化学习计划
    返回包含 AI 生成阶段和任务的结构，失败时返回 ai_generated=False
    """
    if subjects is None:
        subjects = []

    default_response = {
        "ai_generated": False,
        "phases": [],
        "daily_tasks": [],
        "advice": "",
        "total_days": 30,
        "total_hours": 120
    }

    if not goal or not target_date:
        print("⚠️ AI 日程缺少 goal 或 target_date，跳过调用")
        return default_response

    # 检查 API Key 是否存在
    if not Config.DEEPSEEK_API_KEY:
        print("❌ DEEPSEEK_API_KEY 未配置，无法调用 AI")
        return default_response

    headers = {
        "Authorization": f"Bearer {Config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    subjects_text = "、".join(subjects) if subjects else "相关科目"
    prompt = f"""
你是一位专业的学业规划师。请根据以下信息为用户生成一个详细的备考计划建议。

用户目标：{goal}
考试/截止日期：{target_date}
每日可用学习时间：{daily_hours} 小时
需要准备的科目/任务：{subjects_text}

请以严格的 JSON 格式返回，包含以下字段：
- phases: 数组，每个元素包含 name (阶段名称)、days (该阶段天数)、tasks (该阶段典型每日任务列表，字符串数组)
- daily_tasks: 数组，示例的每日任务模板（可用于每日具体安排）
- advice: 字符串，给用户的个性化学习建议（如时间分配、复习技巧等）
- total_days: 整数，总学习天数
- total_hours: 整数，总学习小时数

只返回 JSON，不要其他文字。
"""

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一个专业的日程规划助手，只输出 JSON。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 800
    }

    try:
        print(f"📤 向 DeepSeek 请求日程生成: goal={goal}, target_date={target_date}")
        resp = requests.post(Config.DEEPSEEK_API_URL, headers=headers, json=payload, timeout=20)
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()
        print(f"📥 DeepSeek 响应内容长度: {len(content)} 字符")

        if not content:
            print("⚠️ DeepSeek 返回空内容")
            return default_response

        # 解析 JSON
        try:
            result = json.loads(content)
        except json.JSONDecodeError:
            content = content.replace("```json", "").replace("```", "").strip()
            result = json.loads(content)

        # 标记为 AI 生成
        result["ai_generated"] = True
        result.setdefault("phases", [])
        result.setdefault("daily_tasks", [])
        result.setdefault("advice", "")
        result.setdefault("total_days", 30)
        result.setdefault("total_hours", int(daily_hours * 30))

        print(f"✅ AI 日程生成成功，包含 {len(result['phases'])} 个阶段")
        return result

    except Exception as e:
        print(f"❌ AI 日程生成失败: {e}")
        return default_response