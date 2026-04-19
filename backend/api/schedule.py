# api/schedule.py
# 日程生成接口：支持两种调用方式
# 1. 新版：传入完整 schedule_info，返回多天计划 + .ics 内容
# 2. 旧版兼容：传入 item + preferred_time，返回单个事件提醒

from flask import Blueprint, request
from services.scheduler import generate_schedule, generate_schedule_event
from utils.response import success, error

schedule_bp = Blueprint("schedule", __name__, url_prefix='/api')


@schedule_bp.route("/schedule", methods=["POST"])
def schedule():
    """
    POST /api/schedule

    新版请求体（推荐）：
    {
        "schedule_info": {
            "goal": "考研",                // 目标类型，如 "考研"、"期末考"、"比赛"、"考证"
            "target_date": "2026-12-20",   // 目标日期，YYYY-MM-DD
            "daily_hours": 6,              // 每日可用小时数
            "subjects": ["政治", "英语", "数学"],  // 科目/任务列表
            "start_date": "2026-05-01"     // 可选，计划开始日期，默认为今天
        }
    }

    旧版请求体（兼容）：
    {
        "item": "披萨",
        "preferred_time": "周末"
    }

    新版响应：
    {
        "code": 0,
        "msg": "success",
        "data": {
            "schedule": [
                {"date": "2026-05-01", "tasks": ["基础阶段：政治 2.0h", ...]},
                ...
            ],
            "ics_content": "BEGIN:VCALENDAR ..."
        }
    }

    旧版响应：
    {
        "code": 0,
        "msg": "success",
        "data": {
            "event": {
                "title": "购买 披萨",
                "description": "...",
                "start": [2026, 5, 3, 18, 0],
                ...
            }
        }
    }
    """
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return error("Invalid JSON body")

    # 判断调用方式：新版有 schedule_info 字段
    if "schedule_info" in data:
        schedule_info = data.get("schedule_info")
        if not schedule_info or not isinstance(schedule_info, dict):
            return error("schedule_info must be a non-empty object")

        # 必填字段校验
        if not schedule_info.get("goal"):
            return error("schedule_info.goal is required")
        if not schedule_info.get("target_date"):
            return error("schedule_info.target_date is required")

        try:
            result = generate_schedule(schedule_info)
        except Exception as e:
            return error(f"Schedule generation failed: {str(e)}")

        return success(result)

    # 旧版兼容逻辑：有 item 字段
    elif "item" in data:
        item = data.get("item")
        preferred_time = data.get("preferred_time")
        if not item:
            return error("item is required")

        event = generate_schedule_event(item, preferred_time)
        return success({"event": event})

    else:
        return error("Missing required fields: either 'schedule_info' or 'item'")