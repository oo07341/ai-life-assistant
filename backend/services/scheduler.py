# services/scheduler.py
# 多场景日程生成模块：支持考研、期末考、比赛等目标
# 输出结构化每日任务列表 + iCalendar 格式日历内容

import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

try:
    from ics import Calendar, Event
    ICS_AVAILABLE = True
except ImportError:
    ICS_AVAILABLE = False

try:
    from services.deepseek import generate_ai_schedule
    DEEPSEEK_AVAILABLE = True
except ImportError:
    DEEPSEEK_AVAILABLE = False


def _parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def _get_phase_distribution(goal: str) -> List[Tuple[str, float]]:
    goal_lower = goal.lower()
    if "考研" in goal_lower:
        return [("基础阶段", 0.4), ("强化阶段", 0.4), ("冲刺阶段", 0.2)]
    elif "期末" in goal_lower or "考试" in goal_lower:
        return [("基础复习", 0.5), ("刷题强化", 0.3), ("考前冲刺", 0.2)]
    elif "比赛" in goal_lower or "竞赛" in goal_lower:
        return [("知识储备", 0.3), ("模拟实战", 0.4), ("最终打磨", 0.3)]
    elif "考证" in goal_lower:
        return [("教材学习", 0.4), ("真题训练", 0.4), ("查漏补缺", 0.2)]
    else:
        return [("准备阶段", 1.0)]


def _escape_ics_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\n", "\\n")
    text = text.replace("\r", "")
    return text


def _build_ics_content(schedule: List[Dict], goal: str, start_hour: int = 9, duration_hours: float = 2.0) -> str:
    if ICS_AVAILABLE:
        cal = Calendar()
        for day in schedule:
            event = Event()
            event.name = f"{goal} · 学习任务"
            event_start = datetime.strptime(day["date"], "%Y-%m-%d").replace(hour=start_hour, minute=0)
            event.begin = event_start
            event.duration = timedelta(hours=duration_hours)
            event.description = "\n".join(day["tasks"])
            cal.events.add(event)
        return cal.serialize()
    else:
        lines = [
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//AI Life Assistant//Schedule//EN"
        ]
        for day in schedule:
            date_str = day["date"].replace("-", "")
            dtstart = f"{date_str}T{start_hour:02d}0000"
            total_minutes = int(duration_hours * 60)
            end_hour = start_hour + total_minutes // 60
            end_minute = total_minutes % 60
            dtend = f"{date_str}T{end_hour:02d}{end_minute:02d}00"
            summary = _escape_ics_text(f"{goal} 学习任务")
            raw_description = "\n".join(day["tasks"])
            description = _escape_ics_text(raw_description)
            lines.extend([
                "BEGIN:VEVENT",
                f"DTSTART:{dtstart}",
                f"DTEND:{dtend}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                "END:VEVENT"
            ])
        lines.append("END:VCALENDAR")
        return "\r\n".join(lines)


def generate_schedule(schedule_info: Dict) -> Dict:
    goal = schedule_info.get("goal", "期末考")
    target_date_str = schedule_info.get("target_date")
    if not target_date_str:
        target_date = datetime.now() + timedelta(days=30)
    else:
        target_date = _parse_date(target_date_str)

    daily_hours = float(schedule_info.get("daily_hours", 4))
    subjects = schedule_info.get("subjects", ["复习"])
    if not isinstance(subjects, list) or len(subjects) == 0:
        subjects = ["复习"]

    start_date_str = schedule_info.get("start_date")
    if start_date_str:
        start_date = _parse_date(start_date_str)
    else:
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    preferred_start_hour = int(schedule_info.get("preferred_start_hour", 9))
    preferred_start_hour = max(0, min(23, preferred_start_hour))
    calendar_duration = min(daily_hours, 8.0)

    total_days = (target_date - start_date).days
    if total_days <= 0:
        return {"schedule": [], "ics_content": ""}

    # 尝试使用AI生成日程
    ai_schedule_result = None
    if DEEPSEEK_AVAILABLE and target_date_str:
        try:
            print(f"🔍 尝试使用AI生成日程: goal={goal}, target_date={target_date_str}")
            ai_schedule_result = generate_ai_schedule(
                goal=goal,
                target_date=target_date_str,
                daily_hours=daily_hours,
                subjects=subjects
            )
            print(f"🤖 AI日程生成结果: ai_generated={ai_schedule_result.get('ai_generated', False)}")
        except Exception as e:
            print(f"❌ AI日程生成失败: {e}")
            ai_schedule_result = None

    # 如果AI生成成功，使用AI结果
    if ai_schedule_result and ai_schedule_result.get("ai_generated", False):
        print("🎯 使用AI生成的日程")
        phases = ai_schedule_result.get("phases", [])
        daily_tasks = ai_schedule_result.get("daily_tasks", [])
        advice = ai_schedule_result.get("advice", "")
        
        # 将AI结果转换为标准格式
        schedule = []
        current_date = start_date
        
        # 如果有AI阶段划分，使用AI的阶段
        if phases and len(phases) > 0:
            for phase in phases:
                phase_name = phase.get("name", "阶段")
                phase_days = phase.get("days", 0)
                phase_tasks = phase.get("tasks", [])
                
                for day in range(phase_days):
                    if current_date >= target_date:
                        break
                    
                    # 使用AI的每日任务或阶段任务
                    if daily_tasks and len(daily_tasks) > 0:
                        task_index = len(schedule) % len(daily_tasks)
                        tasks = daily_tasks[task_index]
                    elif phase_tasks and len(phase_tasks) > 0:
                        task_index = day % len(phase_tasks)
                        tasks = [phase_tasks[task_index]]
                    else:
                        tasks = [f"{phase_name}：复习 {daily_hours:.1f}h"]
                    
                    schedule.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "tasks": tasks if isinstance(tasks, list) else [tasks],
                        "ai_generated": True,
                        "phase": phase_name
                    })
                    current_date += timedelta(days=1)
        else:
            # 如果没有AI阶段，使用静态规则
            phases = _get_phase_distribution(goal)
            for phase_name, ratio in phases:
                phase_days = max(1, int(total_days * ratio))
                phase_days = min(phase_days, (target_date - current_date).days)

                for _ in range(phase_days):
                    if current_date >= target_date:
                        break
                    
                    # 使用AI的每日任务
                    if daily_tasks and len(daily_tasks) > 0:
                        task_index = len(schedule) % len(daily_tasks)
                        tasks = daily_tasks[task_index]
                    else:
                        hours_per_subject = daily_hours / len(subjects)
                        tasks = [
                            f"{phase_name}：{subj} {hours_per_subject:.1f}h"
                            for subj in subjects
                        ]
                    
                    schedule.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "tasks": tasks if isinstance(tasks, list) else [tasks],
                        "ai_generated": True,
                        "phase": phase_name
                    })
                    current_date += timedelta(days=1)
        
        # 添加AI建议
        if advice:
            schedule.append({
                "date": "建议",
                "tasks": [f"AI建议：{advice}"],
                "ai_generated": True,
                "phase": "建议"
            })
    else:
        # AI生成失败，使用静态规则
        print("🔧 AI生成失败，使用静态规则")
        phases = _get_phase_distribution(goal)
        schedule = []
        current_date = start_date

        for phase_name, ratio in phases:
            phase_days = max(1, int(total_days * ratio))
            phase_days = min(phase_days, (target_date - current_date).days)

            for _ in range(phase_days):
                if current_date >= target_date:
                    break
                remaining = (target_date - current_date).days
                if remaining <= 0:
                    break

                hours_per_subject = daily_hours / len(subjects)
                tasks = [
                    f"{phase_name}：{subj} {hours_per_subject:.1f}h"
                    for subj in subjects
                ]

                schedule.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "tasks": tasks,
                    "ai_generated": False,
                    "phase": phase_name
                })
                current_date += timedelta(days=1)

            if current_date >= target_date:
                break

    ics_content = _build_ics_content(schedule, goal, preferred_start_hour, calendar_duration)
    
    # 返回结果，包含AI生成标识
    result = {
        "schedule": schedule,
        "ics_content": ics_content,
        "ai_generated": ai_schedule_result.get("ai_generated", False) if ai_schedule_result else False,
        "total_days": total_days,
        "total_hours": total_days * daily_hours
    }
    
    # 如果有AI建议，添加到结果中
    if ai_schedule_result and ai_schedule_result.get("advice"):
        result["ai_advice"] = ai_schedule_result["advice"]
    
    return result


def adjust_schedule(original_schedule: List[Dict],
                    completed_dates: List[str],
                    remaining_subjects: List[str],
                    target_date_str: str,
                    daily_hours: float,
                    preferred_start_hour: int = 9) -> Dict:
    today = datetime.now().date()
    completed_set = set(completed_dates)

    incomplete_days = []
    for day in original_schedule:
        day_date = datetime.strptime(day["date"], "%Y-%m-%d").date()
        if (day_date > today) or (day_date == today and day["date"] not in completed_set):
            incomplete_days.append(day["date"])

    if len(incomplete_days) == 0:
        return {"schedule": [], "ics_content": ""}

    target_date = _parse_date(target_date_str)
    start_date = datetime.combine(today, datetime.min.time())

    new_info = {
        "goal": "调整计划",
        "target_date": target_date_str,
        "daily_hours": daily_hours,
        "subjects": remaining_subjects,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "preferred_start_hour": preferred_start_hour
    }
    return generate_schedule(new_info)


from typing import Optional

def generate_schedule_event(item: Optional[str] = None, preferred_time: Optional[str] = None) -> dict:
    item_str = (item or "未指定商品").strip()
    preferred_time_str = (preferred_time or "").strip()
    time_intent = preferred_time_str.lower() if preferred_time_str else ""

    now = datetime.now()
    start_time = now + timedelta(days=1)
    start_time = start_time.replace(hour=18, minute=0, second=0, microsecond=0)

    if "周末" in time_intent:
        days_ahead = 5 - now.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        start_time = now + timedelta(days=days_ahead)
        start_time = start_time.replace(hour=18, minute=0)

    elif "今晚" in time_intent:
        start_time = now.replace(hour=20, minute=0)
        if now > start_time:
            start_time += timedelta(days=1)

    end_time = start_time + timedelta(minutes=30)

    def format_time(dt):
        return [dt.year, dt.month, dt.day, dt.hour, dt.minute]

    return {
        "title": f"购买 {item_str}",
        "description": f"AI 智能比价推荐：{item_str}。建议 {start_time.strftime('%Y-%m-%d %H:%M')} 出发",
        "location": "线上/附近门店",
        "start": format_time(start_time),
        "end": format_time(end_time),
        "time": preferred_time_str or "明天",
        "url": ""
    }
