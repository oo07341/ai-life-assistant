# services/scheduler.py
# 日程生成模块：根据商品信息和时间意图生成结构化日历事件数据

# services/scheduler.py
from datetime import datetime, timedelta

def generate_schedule_event(item: str = None, preferred_time: str = None) -> dict:
    item = (item or "未指定商品").strip()
    preferred_time = (preferred_time or "").strip()
    time_intent = preferred_time.lower()

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
        "title": f"购买 {item}",
        "time": preferred_time or "明天",
        "note": f"已为您生成购物日程，建议 {start_time.strftime('%Y-%m-%d %H:%M')} 出发",
        "event": {
            "title": f"购买 {item}",
            "description": f"AI 智能比价推荐：{item}",
            "start": format_time(start_time),
            "end": format_time(end_time),
            "location": "线上/附近门店",
            "url": ""
        }
    }