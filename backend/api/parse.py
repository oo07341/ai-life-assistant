# api/parse.py
# 一体化搜索接口：接收用户输入，返回意图解析结果和比价数据

from flask import Blueprint, request   # Blueprint 用于模块化路由，request 获取请求数据
from services.deepseek import parse_intent   # 意图解析服务
from services.mock_prices import search_products_by_keywords  # 商品搜索服务
from utils.response import success, error    # 统一响应格式工具

# 创建蓝图，url_prefix 设为 /api，使得该蓝图下的路由都以 /api 开头
parse_bp = Blueprint("parse", __name__, url_prefix='/api')

@parse_bp.route("/search", methods=["POST"])
def search():
    """
    POST /api/search
    请求体 JSON 格式：{"query": "用户自然语言输入"}
    返回：{"code": 0, "msg": "success", "data": {"intent": {...}, "deals": [...]}}
    """
    data = request.get_json()           # 获取请求的 JSON 数据
    if not data:
        return error("Invalid JSON body")   # 如果请求体不是合法 JSON，返回错误

    query = data.get("query")           # 提取用户输入文本
    if not query or not isinstance(query, str):
        return error("query is required and must be a string")

    # 1. 调用 DeepSeek 解析意图
    intent = parse_intent(query)

    # 2. 根据意图类型决定是否进行比价搜索
    deals = []
    if intent.get("intent") in ["shopping","general"]:  # 购物意图或通用意图都尝试搜索
        keywords = intent.get("keywords", [])
        if keywords:
            deals = search_products_by_keywords(keywords)

    # 3. 组装返回数据
    result_data = {
        "intent": intent,
        "deals": deals
    }
    return success(result_data)