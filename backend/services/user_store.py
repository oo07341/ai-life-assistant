# services/user_store.py
# 简易用户计划存储（内存 + JSON 文件备份）
# services/user_store.py
# 简易用户计划存储（内存 + JSON 文件备份）
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

STORAGE_FILE = "user_plans.json"

# 内存存储结构：{ user_id: { "plans": [plan_object, ...], "active_plan_id": "xxx" } }
_user_data = {}

def _load_from_file():
    global _user_data
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r', encoding='utf-8') as f:
            _user_data = json.load(f)

def _save_to_file():
    with open(STORAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(_user_data, f, ensure_ascii=False, indent=2)

# 初始化加载
_load_from_file()

def get_user_plans(user_id: str) -> List[Dict]:
    """返回用户所有计划列表（按创建时间倒序）"""
    return _user_data.get(user_id, {}).get("plans", [])

def get_active_plan(user_id: str) -> Optional[Dict]:
    """获取当前激活的计划"""
    user_info = _user_data.get(user_id, {})
    active_id = user_info.get("active_plan_id")
    if active_id:
        for plan in user_info.get("plans", []):
            if plan.get("plan_id") == active_id:
                return plan
    return None

def save_plan(user_id: str, plan_data: Dict, set_active: bool = True) -> str:
    """保存新计划，返回 plan_id"""
    import uuid
    plan_id = str(uuid.uuid4())[:8]
    plan_data["plan_id"] = plan_id
    plan_data["created_at"] = datetime.now().isoformat()
    plan_data["updated_at"] = plan_data["created_at"]

    if user_id not in _user_data:
        _user_data[user_id] = {"plans": [], "active_plan_id": None}

    _user_data[user_id]["plans"].append(plan_data)
    if set_active:
        _user_data[user_id]["active_plan_id"] = plan_id

    _save_to_file()
    return plan_id

def update_plan(user_id: str, plan_id: str, updates: Dict):
    """更新计划（如打卡状态、任务完成情况）"""
    for plan in _user_data.get(user_id, {}).get("plans", []):
        if plan.get("plan_id") == plan_id:
            plan.update(updates)
            plan["updated_at"] = datetime.now().isoformat()
            _save_to_file()
            return True
    return False

def set_active_plan(user_id: str, plan_id: str) -> bool:
    """切换当前激活计划"""
    if user_id in _user_data:
        if any(p.get("plan_id") == plan_id for p in _user_data[user_id]["plans"]):
            _user_data[user_id]["active_plan_id"] = plan_id
            _save_to_file()
            return True
    return False

def _safe_parse_date(date_str: Optional[str]) -> Optional[datetime]:
    """安全解析日期字符串，失败返回 None"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None

def merge_and_regenerate(user_id: str, new_schedule_info: Dict) -> Dict:
    """
    合并当前激活计划与新增目标，重新生成日程。
    返回新计划对象（已保存并设为激活）
    """
    active = get_active_plan(user_id)
    if not active:
        # 无激活计划，直接生成新计划
        from services.scheduler import generate_schedule
        new_plan = generate_schedule(new_schedule_info)
        plan_id = save_plan(user_id, {
            "goal": new_schedule_info.get("goal"),
            "schedule_info": new_schedule_info,
            "schedule": new_plan["schedule"],
            "ics_content": new_plan["ics_content"],
            "completed_dates": [],
        })
        new_plan["plan_id"] = plan_id
        return new_plan

    # 合并逻辑：取出未完成科目 + 新科目，取最晚目标日期
    remaining_subjects = active.get("schedule_info", {}).get("subjects", [])
    new_subjects = new_schedule_info.get("subjects", [])
    merged_subjects = list(set(remaining_subjects + new_subjects))

    # 目标日期取较晚者（使用日期对象比较，修正字符串 max 问题）
    old_target_str = active["schedule_info"].get("target_date")
    new_target_str = new_schedule_info.get("target_date")

    old_dt = _safe_parse_date(old_target_str)
    new_dt = _safe_parse_date(new_target_str)

    # 如果两者都有效，取最晚；否则取有效的那一个；否则默认 30 天后
    if old_dt and new_dt:
        final_dt = max(old_dt, new_dt)
    elif old_dt:
        final_dt = old_dt
    elif new_dt:
        final_dt = new_dt
    else:
        final_dt = datetime.now() + timedelta(days=30)

    final_target = final_dt.strftime("%Y-%m-%d")

    merged_info = {
        "goal": f"{active['schedule_info']['goal']}+{new_schedule_info.get('goal', '新增')}",
        "target_date": final_target,
        "daily_hours": max(active["schedule_info"].get("daily_hours", 4),
                           new_schedule_info.get("daily_hours", 4)),
        "subjects": merged_subjects,
        "start_date": datetime.now().strftime("%Y-%m-%d")
    }

    from services.scheduler import generate_schedule
    new_plan_data = generate_schedule(merged_info)

    # 保存为新计划（原计划保留为历史）
    plan_id = save_plan(user_id, {
        "goal": merged_info["goal"],
        "schedule_info": merged_info,
        "schedule": new_plan_data["schedule"],
        "ics_content": new_plan_data["ics_content"],
        "completed_dates": [],   # 重置打卡
        "parent_plan_ids": [active.get("plan_id")]
    }, set_active=True)

    new_plan_data["plan_id"] = plan_id
    return new_plan_data