# services/user_store.py
# 简易用户计划存储（内存 + JSON 文件备份）
# services/user_store.py
# 简易用户计划存储（内存 + JSON 文件备份）
from models import db, User, Plan, DailyTask
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import uuid

def get_user_plans(user_uuid: str) -> List[Dict]:
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if not user:
        return []
    plans = Plan.query.filter_by(user_id=user.id).order_by(Plan.created_at.desc()).all()
    return [p.to_dict() for p in plans]

def get_active_plan(user_uuid: str) -> Optional[Dict]:
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if not user:
        return None
    plan = Plan.query.filter_by(user_id=user.id, is_active=True).first()
    return plan.to_dict() if plan else None

def save_plan(user_uuid: str, plan_data: Dict, set_active: bool = True) -> str:
    user = User.get_or_create(user_uuid)
    if set_active:
        # 先将该用户其他计划设为非激活
        Plan.query.filter_by(user_id=user.id, is_active=True).update({'is_active': False})

    plan = Plan(
        plan_uuid=plan_data.get('plan_id') or str(uuid.uuid4())[:8],
        user_id=user.id,
        goal=plan_data['goal'],
        schedule_info=plan_data['schedule_info'],
        schedule_data=plan_data['schedule'],
        ics_content=plan_data.get('ics_content', ''),
        is_active=set_active,
        parent_plan_id=None
    )
    db.session.add(plan)
    db.session.flush()  # 获取 plan.id

    # 初始化打卡记录（全部未完成）
    for day in plan_data['schedule']:
        if day.get('date') == '建议':
            continue
        task = DailyTask(
            plan_id=plan.id,
            task_date=datetime.strptime(day['date'], '%Y-%m-%d').date(),
            completed=False
        )
        db.session.add(task)

    db.session.commit()
    return plan.plan_uuid

def update_plan(user_uuid: str, plan_uuid: str, updates: Dict):
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if not user:
        return False
    plan = Plan.query.filter_by(user_id=user.id, plan_uuid=plan_uuid).first()
    if not plan:
        return False

    if 'completed_dates' in updates:
        # 更新打卡状态
        completed_dates = set(updates['completed_dates'])
        for task in plan.daily_tasks:
            should_complete = task.task_date.isoformat() in completed_dates
            if task.completed != should_complete:
                task.completed = should_complete
                task.completed_at = datetime.utcnow() if should_complete else None
    if 'schedule' in updates:
        plan.schedule_data = updates['schedule']
    if 'ics_content' in updates:
        plan.ics_content = updates['ics_content']

    db.session.commit()
    return True

def set_active_plan(user_uuid: str, plan_uuid: str) -> bool:
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if not user:
        return False
    # 先将所有计划设为非激活
    Plan.query.filter_by(user_id=user.id).update({'is_active': False})
    # 激活目标计划
    plan = Plan.query.filter_by(user_id=user.id, plan_uuid=plan_uuid).first()
    if plan:
        plan.is_active = True
        db.session.commit()
        return True
    return False

def merge_and_regenerate(user_uuid: str, new_schedule_info: Dict) -> Dict:
    """合并当前激活计划与新增目标，重新生成日程，返回新计划对象"""
    active = get_active_plan(user_uuid)
    if not active:
        # 无激活计划，直接生成新计划
        from services.scheduler import generate_schedule
        new_plan = generate_schedule(new_schedule_info)
        plan_id = save_plan(user_uuid, {
            "goal": new_schedule_info.get("goal"),
            "schedule_info": new_schedule_info,
            "schedule": new_plan["schedule"],
            "ics_content": new_plan["ics_content"],
            "completed_dates": [],
        })
        new_plan["plan_id"] = plan_id
        return new_plan

    # 合并科目
    remaining_subjects = active.get("schedule_info", {}).get("subjects", [])
    new_subjects = new_schedule_info.get("subjects", [])
    merged_subjects = list(set(remaining_subjects + new_subjects))

    # 目标日期取较晚者（安全解析）
    old_target_str = active["schedule_info"].get("target_date")
    new_target_str = new_schedule_info.get("target_date")

    def _safe_parse(d):
        try:
            return datetime.strptime(d, "%Y-%m-%d") if d else None
        except:
            return None

    old_dt = _safe_parse(old_target_str)
    new_dt = _safe_parse(new_target_str)

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

    # 保存为新计划，原计划保留为历史
    plan_id = save_plan(user_uuid, {
        "goal": merged_info["goal"],
        "schedule_info": merged_info,
        "schedule": new_plan_data["schedule"],
        "ics_content": new_plan_data["ics_content"],
        "completed_dates": [],
        "parent_plan_ids": [active.get("plan_id")]
    }, set_active=True)

    new_plan_data["plan_id"] = plan_id
    return new_plan_data