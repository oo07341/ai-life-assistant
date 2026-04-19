# 日程动态调整接口：根据已完成打卡日期重新生成剩余计划

from flask import Blueprint, request
from services.scheduler import adjust_schedule
from utils.response import success, error

# 创建蓝图，url_prefix 为 /api
adjust_bp = Blueprint("adjust", __name__, url_prefix='/api')


@adjust_bp.route("/adjust-schedule", methods=["POST"])
def adjust():
    """
    POST /api/adjust-schedule

    请求体 JSON 格式：
    {
        "original_schedule": [ ... ],      // 原计划列表（由 generate_schedule 返回的 schedule 字段）
        "completed_dates": ["2026-05-01", "2026-05-02"],  // 已完成打卡的日期列表
        "remaining_subjects": ["高数", "英语"],           // 剩余未完成的科目
        "target_date": "2026-12-20",                    // 目标日期
        "daily_hours": 4                                // 每日可用小时数
    }

    返回：
    {
        "code": 0,
        "msg": "success",
        "data": {
            "schedule": [ ... ],      // 新生成的剩余计划
            "ics_content": "..."      // 对应的日历文件内容
        }
    }
    """
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict):
        return error("Invalid JSON body")

    # 提取并校验必要字段
    original_schedule = data.get("original_schedule")
    if not original_schedule or not isinstance(original_schedule, list):
        return error("original_schedule is required and must be a list")

    completed_dates = data.get("completed_dates")
    if not isinstance(completed_dates, list):
        return error("completed_dates must be a list")

    remaining_subjects = data.get("remaining_subjects")
    if not remaining_subjects or not isinstance(remaining_subjects, list):
        return error("remaining_subjects is required and must be a non-empty list")

    target_date = data.get("target_date")
    if not target_date or not isinstance(target_date, str):
        return error("target_date is required and must be a string (YYYY-MM-DD)")

    daily_hours = data.get("daily_hours")
    if daily_hours is None:
        daily_hours = 4.0
    try:
        daily_hours = float(daily_hours)
    except (TypeError, ValueError):
        return error("daily_hours must be a number")

    # 调用服务层进行调整
    try:
        result = adjust_schedule(
            original_schedule=original_schedule,
            completed_dates=completed_dates,
            remaining_subjects=remaining_subjects,
            target_date_str=target_date,
            daily_hours=daily_hours
        )
    except Exception as e:
        # 服务层异常（如日期解析错误等）
        return error(f"Schedule adjustment failed: {str(e)}")

    # 返回新计划
    return success({
        "schedule": result.get("schedule", []),
        "ics_content": result.get("ics_content", "")
    })