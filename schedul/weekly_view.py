"""weekly_view.py — Formatted weekly schedule calendar view generator."""

from __future__ import annotations
from datetime import datetime, timedelta
from typing import Dict, List
from schedul.models import Event, TimeSlot


class WeeklyCalendarView:
    """Renders a 7-day terminal text grid of events."""

    def __init__(self, week_start_date: datetime):
        # Align to Monday of that week
        self.monday = week_start_date - timedelta(days=week_start_date.weekday())
        self.monday = self.monday.replace(hour=0, minute=0, second=0, microsecond=0)

    def render_ascii_week(self, scheduled_slots: List[tuple[Event, TimeSlot]]) -> str:
        """Render ASCII weekly schedule grid."""
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day_events: Dict[int, List[tuple[Event, TimeSlot]]] = {i: [] for i in range(7)}

        for ev, slot in scheduled_slots:
            diff_days = (slot.start.date() - self.monday.date()).days
            if 0 <= diff_days < 7:
                day_events[diff_days].append((ev, slot))

        lines = [
            "=" * 75,
            f" WEEKLY SCHEDULE: Week of {self.monday.strftime('%Y-%m-%d')}",
            "=" * 75,
        ]

        for i, day_name in enumerate(days):
            day_date = (self.monday + timedelta(days=i)).strftime("%Y-%m-%d")
            lines.append(f"[{day_name} - {day_date}]")
            evs = day_events[i]
            if not evs:
                lines.append("  (No events scheduled)")
            else:
                # Sort by start time
                evs.sort(key=lambda item: item[1].start)
                for ev, slot in evs:
                    time_str = f"{slot.start.strftime('%H:%M')} - {slot.end.strftime('%H:%M')}"
                    lines.append(f"  • {time_str} | {ev.title} (Duration: {ev.duration_minutes}m)")
            lines.append("-" * 75)

        return "\n".join(lines)
