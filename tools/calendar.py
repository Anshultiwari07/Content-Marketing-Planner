from datetime import date, timedelta
from typing import List, Dict

class CalendarTool:
    def build_calendar(self, posts: List[Dict], start_date: date | None = None) -> List[Dict]:
        if start_date is None:
            start_date = date.today()
        scheduled = []
        day = start_date
        for p in posts:
            scheduled.append({**p, "date": day.isoformat()})
            day += timedelta(days=2)
        return scheduled
