"""working_hours.py — Working hours constraint enforcement and profile management."""

from __future__ import annotations
from datetime import time, datetime
from typing import Dict, List, Optional
from schedul.models import TimeSlot


class WorkingHoursProfile:
    """Defines daily working hours windows (e.g. 09:00 - 17:00, Mon-Fri)."""

    def __init__(
        self,
        start_hour: int = 9,
        start_minute: int = 0,
        end_hour: int = 17,
        end_minute: int = 0,
        work_days: Optional[List[int]] = None,  # 0=Monday, 4=Friday, 5=Saturday, 6=Sunday
    ):
        self.start_time = time(start_hour, start_minute)
        self.end_time = time(end_hour, end_minute)
        self.work_days = work_days if work_days is not None else [0, 1, 2, 3, 4]

    def is_within_working_hours(self, slot: TimeSlot) -> bool:
        """Check if both start and end of slot fall on a working day within working hours."""
        if slot.start.weekday() not in self.work_days or slot.end.weekday() not in self.work_days:
            return False
        if slot.start.date() != slot.end.date():
            return False
        
        slot_start_time = slot.start.time()
        slot_end_time = slot.end.time()
        return slot_start_time >= self.start_time and slot_end_time <= self.end_time

    def clamp_to_working_hours(self, dt: datetime) -> TimeSlot:
        """Return the working hours TimeSlot for the given day."""
        start_dt = datetime.combine(dt.date(), self.start_time)
        end_dt = datetime.combine(dt.date(), self.end_time)
        return TimeSlot(start=start_dt, end=end_dt)
