# api/parse.py
# 一体化搜索接口：接收用户输入，返回意图解析结果和比价数据

from flask import Blueprint, request   # Blueprint 用于模块化路由，request 获取请求数据
from services.deepseek import parse_intent   # 意图解析服务
from services.mock_prices import search_products_by_keywords  # 商品搜索服务
from services.search_history import record_keywords, get_hot_keywords
from utils.response import success, error    # 统一响应格式工具

# 创建蓝图，url_prefix 设为 /api，使得该蓝图下的路由都以 /api 开头
parse_bp = Blueprint("parse", __name__, url_prefix='/api')

@parse_bp.route("/search", methods=["POST"])
def search():
    """
    POST /api/search
    请求体 JSON 格式：{"query": "用户自然语言输入"}
    返回数据结构：
    {
        "code": 0,
        "msg": "success",
        "data": {
            "intent": {
                "intent": "shopping" | "schedule" | "general",
                "product_keywords": ["披萨"],
                "location_hint": "校内" | "校外" | "不限",
                "schedule_info": { ... }  // 仅当 intent="schedule" 时存在
            },
            "deals": [ ... ]  // 比价聚合结果，仅购物意图有内容
        }
    }
    """
    data = request.get_json(silent=True) or {}          # 获取请求的 JSON 数据
    if not isinstance(data, dict):
        return error("Invalid JSON body")   # 如果请求体不是合法 JSON，返回错误

    query = data.get("query")           # 提取用户输入文本
    if not query or not isinstance(query, str):
        return error("query is required and must be a string")

    # 1. 调用 DeepSeek 解析意图
    raw_intent = parse_intent(query)

    # 2️.标准化字段（防止前端 undefined）
    intent = {
        "intent": raw_intent.get("intent", "general"),
        "product_keywords": raw_intent.get("product_keywords", []),
        "location_hint": raw_intent.get("location_hint", "不限"),
        "schedule_info": None
    }

    # 如果意图是日程，提取 schedule_info 字段
    if intent["intent"] == "schedule":
        schedule_info = raw_intent.get("schedule_info", {})
        if not isinstance(schedule_info, dict):
            schedule_info = {}
        intent["schedule_info"] = {
            "goal": schedule_info.get("goal", "期末考"),
            "target_date": schedule_info.get("target_date"),
            "daily_hours": schedule_info.get("daily_hours", 4),
            "subjects": schedule_info.get("subjects", ["复习"])
        }
    else:
        # 确保购物意图下也有空对象，防止前端访问报错
        intent["schedule_info"] = None

    # 3. 根据意图类型决定是否进行比价搜索
    deals = []
    if intent["intent"] in ["shopping", "general"]:
        keywords = intent.get("product_keywords", [])
        if keywords:
            # 新版 search_products_by_keywords 返回聚合后的商品组列表
            deals = search_products_by_keywords(keywords)
            # 可选：根据 location_hint 过滤
            if intent["location_hint"] != "不限":
                deals = [
                    g for g in deals
                    if g.get("location") == intent["location_hint"]
                ]

    # 4. 记录搜索关键词（用于历史与热门）
    if keywords:
        record_keywords(keywords)

    # 5. 获取热门关键词（供前端展示）
    hot_keywords = get_hot_keywords(limit=5)

    # 6. 组装返回数据
    return success({
        "intent": intent,
        "deals": deals,  # 前端可识别为商品组数组
        "hot_keywords": hot_keywords
    })