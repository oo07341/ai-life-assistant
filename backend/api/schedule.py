# api/schedule.py
# 日程生成接口：接收商品信息，返回结构化日历事件数据

from flask import Blueprint, request
from services.scheduler import generate_schedule_event  # 日程生成服务
from utils.response import success, error
# 创建蓝图，url_prefix 为 /api
schedule_bp = Blueprint("schedule", __name__, url_prefix='/api')

@schedule_bp.route("/schedule", methods=["POST"])
def schedule():
    """
    POST /api/schedule
    请求体 JSON 格式：{"item": "商品名称", "preferred_time": "时间意图（可选）"}
    返回：{"code": 0, "msg": "success", "data": {"event": {...}}}
    """
    data = request.get_json(silent=True) or {}
    if not data:
        return error("Invalid JSON body")

    item = data.get("item")                 # 商品名称
    preferred_time = data.get("preferred_time")  # 时间意图，如 "周末"

    # 接口层兜底
    if not item:
        return error("item 不能为空")

    # 调用服务生成事件字典
    event = generate_schedule_event(item, preferred_time)

    # 将事件对象包装在 data 中返回
    return success({"event": event})