# api/plan.py
from flask import Blueprint, request
from services.user_store import save_plan, update_plan, merge_and_regenerate
from services.scheduler import generate_schedule
from utils.response import success, error

plan_bp = Blueprint("plan", __name__, url_prefix='/api')

@plan_bp.route("/plan/save", methods=["POST"])
def save():
    """保存一个新计划（不合并，直接新建）"""
    user_id = request.headers.get("X-User-Id")
    data = request.get_json(silent=True) or {}
    schedule_info = data.get("schedule_info")
    if not user_id or not schedule_info:
        return error("Missing parameters")

    result = generate_schedule(schedule_info)
    plan_id = save_plan(user_id, {
        "goal": schedule_info.get("goal"),
        "schedule_info": schedule_info,
        "schedule": result["schedule"],
        "ics_content": result["ics_content"],
        "completed_dates": [],
    })
    result["plan_id"] = plan_id
    return success(result)

@plan_bp.route("/plan/update-progress", methods=["POST"])
def update_progress():
    """更新打卡进度"""
    user_id = request.headers.get("X-User-Id")
    data = request.get_json(silent=True) or {}
    plan_id = data.get("plan_id")
    completed_dates = data.get("completed_dates", [])
    if not user_id or not plan_id:
        return error("Missing parameters")
    ok = update_plan(user_id, plan_id, {"completed_dates": completed_dates})
    return success() if ok else error("Update failed")

@plan_bp.route("/plan/merge", methods=["POST"])
def merge():
    """合并当前激活计划与新增目标"""
    user_id = request.headers.get("X-User-Id")
    data = request.get_json(silent=True) or {}
    new_schedule_info = data.get("schedule_info")
    if not user_id or not new_schedule_info:
        return error("Missing parameters")
    merged_plan = merge_and_regenerate(user_id, new_schedule_info)
    return success(merged_plan)