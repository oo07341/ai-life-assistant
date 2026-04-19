# api/user.py
# 用户个人中心相关接口

from flask import Blueprint, request
from services.user_store import get_user_plans, get_active_plan, set_active_plan
from utils.response import success, error

user_bp = Blueprint("user", __name__, url_prefix='/api')


@user_bp.route("/user/plans", methods=["GET"])
def list_plans():
    """获取用户的所有计划列表"""
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return error("Missing X-User-Id header")
    plans = get_user_plans(user_id)
    return success({"plans": plans})


@user_bp.route("/user/active-plan", methods=["GET"])
def active_plan():
    """获取当前激活的计划"""
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return error("Missing X-User-Id header")
    plan = get_active_plan(user_id)
    return success({"active_plan": plan})


@user_bp.route("/user/switch-plan", methods=["POST"])
def switch_plan():
    """切换激活计划"""
    user_id = request.headers.get("X-User-Id")
    data = request.get_json(silent=True) or {}
    plan_id = data.get("plan_id")
    if not user_id or not plan_id:
        return error("Missing parameters")
    ok = set_active_plan(user_id, plan_id)
    return success() if ok else error("Plan not found")


@user_bp.route("/user/profile", methods=["GET"])
def profile():
    """
    获取用户个人中心概览信息
    返回：用户ID、计划总数、当前激活计划ID及目标
    """
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return error("Missing X-User-Id header")

    plans = get_user_plans(user_id)
    active = get_active_plan(user_id)

    return success({
        "user_id": user_id,
        "plan_count": len(plans),
        "active_plan_id": active.get("plan_id") if active else None,
        "active_plan_goal": active.get("goal") if active else None,
        "active_plan_target_date": active.get("schedule_info", {}).get("target_date") if active else None
    })