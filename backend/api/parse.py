# api/parse.py
# 一体化搜索接口：接收用户输入，返回意图解析结果和比价数据
# api/parse.py
# 一体化搜索接口：接收用户输入，返回意图解析结果和比价数据

from flask import Blueprint, request
from services.deepseek import parse_intent
from services.mock_prices import search_products_by_keywords
from services.search_history import record_keywords, get_hot_keywords
from utils.response import success, error
from models import db, User, SearchLog   # 新增导入

# 创建蓝图，url_prefix 设为 /api
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
            "deals": [ ... ],  // 比价聚合结果，仅购物意图有内容
            "hot_keywords": ["麻辣烫", "披萨", ...]
        }
    }
    """
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return error("Invalid JSON body")

    query = data.get("query")
    if not query or not isinstance(query, str):
        return error("query is required and must be a string")

    # 1. 调用 DeepSeek 解析意图
    raw_intent = parse_intent(query)

    # 2. 标准化字段（防止前端 undefined）
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
        intent["schedule_info"] = None

    # 3. 根据意图进行比价搜索
    deals = []
    keywords = intent.get("product_keywords", [])
    if intent["intent"] in ["shopping", "general"] and keywords:
        deals = search_products_by_keywords(keywords)
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

    # 6. 记录搜索日志到数据库（新增）
    try:
        user_id_header = request.headers.get("X-User-Id")
        user_id = None
        if user_id_header:
            user = User.query.filter_by(user_uuid=user_id_header).first()
            if user:
                user_id = user.id

        log = SearchLog(
            user_id=user_id,
            query=query,
            intent=intent["intent"],
            keywords=intent["product_keywords"] if intent["product_keywords"] else None,
            result_count=len(deals)
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        # 日志记录失败不应影响主流程
        print(f"[WARN] Failed to save search log: {e}")
        db.session.rollback()

    # 7. 组装返回数据
    return success({
        "intent": intent,
        "deals": deals,
        "hot_keywords": hot_keywords
    })