# api/prices.py
# 独立的价格查询接口（用于调试或扩展）

from flask import Blueprint, request, jsonify
from services.mock_prices import search_products_by_keywords # 使用新的搜索函数
from utils.response import success, error

# 创建蓝图，url_prefix 为 /api
price_bp = Blueprint("prices", __name__, url_prefix='/api')

@price_bp.route("/prices", methods=["POST"])
def prices():
    """
    POST /api/prices
    请求体 JSON 格式：{"keywords": ["关键词1", "关键词2"]}
    返回比价结果列表，按价格升序排列
    """
    data = request.get_json(silent=True) or {}
    if not data:
        return error("Invalid JSON body")

    keywords = data.get("keywords", [])
    if not isinstance(keywords, list):
        return error("keywords must be a list")   # 如果 keywords 不是列表，则设为空列表

    # 调用搜索服务，传入关键词列表，自动完成模糊匹配、去重和排序
    deals = search_products_by_keywords(keywords)

    return success(deals)