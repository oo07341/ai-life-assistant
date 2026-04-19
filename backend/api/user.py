# api/user.py
# 用户个人中心相关接口

from flask import Blueprint, request
from services.user_store import get_user_plans, get_active_plan, set_active_plan
from services.search_history import get_hot_keywords
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


@user_bp.route("/user/stats", methods=["GET"])
def user_stats():
    """
    获取用户统计数据
    返回：比价次数、未来日程数量、日历文件数量
    """
    user_id = request.headers.get("X-User-Id")
    if not user_id:
        return error("Missing X-User-Id header")

    # 获取用户计划
    plans = get_user_plans(user_id)
    
    # 计算统计数据
    plan_count = len(plans)
    
    # 计算有日历文件的计划数量
    calendar_file_count = sum(1 for plan in plans if plan.get("ics_content"))
    
    # 获取热门关键词（用于计算总搜索次数）
    hot_keywords = get_hot_keywords(limit=100)  # 获取所有关键词
    
    # 从search_history.json读取搜索次数
    import json
    import os
    search_count = 0
    history_file = "search_history.json"
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
                # 计算总搜索次数（所有关键词的频率总和）
                search_count = sum(history_data.values())
        except Exception:
            search_count = 0
    
    return success({
        "price_comparison_count": search_count,
        "future_schedule_count": plan_count,
        "calendar_file_count": calendar_file_count
    })
