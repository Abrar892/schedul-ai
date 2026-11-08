"""Personal and multi-calendar management for Schedul-AI."""
from datetime import datetime, timedelta
from typing import List, Dict
from schedul.models import Person, TimeSlot, Constraint


class PersonalCalendar:
    def __init__(self, person: Person):
        self.person = person
        self.booked_events: List[tuple[TimeSlot, str]] = []
        self.constraints: List[Constraint] = []

    def add_event(self, slot: TimeSlot, title: str):
        self.booked_events.append((slot, title))

    def add_constraint(self, constraint: Constraint):
        self.constraints.append(constraint)

    def get_busy_slots(self, window: TimeSlot) -> List[TimeSlot]:
        busy = []
        for s, _ in self.booked_events:
            if s.overlaps(window):
                busy.append(s)
        for c in self.constraints:
            c_slot = TimeSlot(c.start_time, c.end_time)
            if c_slot.overlaps(window):
                busy.append(c_slot)
        return busy

    def is_available(self, slot: TimeSlot) -> bool:
        busy = self.get_busy_slots(slot)
        return len(busy) == 0

    def get_free_slots(self, search_range: TimeSlot, min_duration: int = 30) -> List[TimeSlot]:
        busy = sorted(self.get_busy_slots(search_range), key=lambda x: x.start)
        free = []
        cur = search_range.start

        for b in busy:
            if b.start > cur:
                gap = TimeSlot(cur, b.start)
                if gap.duration_minutes >= min_duration:
                    free.append(gap)
            cur = max(cur, b.end)

        if cur < search_range.end:
            gap = TimeSlot(cur, search_range.end)
            if gap.duration_minutes >= min_duration:
                free.append(gap)
        return free


class MultiCalendar:
    def __init__(self, calendars: Dict[str, PersonalCalendar]):
        self.calendars = calendars

    def get_common_free_slots(self, person_ids: List[str], search_range: TimeSlot, duration: int) -> List[TimeSlot]:
        if not person_ids:
            return []

        # Find intersections of availability
        step = timedelta(minutes=15)
        current = search_range.start
        target_delta = timedelta(minutes=duration)

        valid_slots = []
        while current + target_delta <= search_range.end:
            candidate = TimeSlot(current, current + target_delta)
            if all(self.calendars[pid].is_available(candidate) for pid in person_ids if pid in self.calendars):
                valid_slots.append(candidate)
            current += step

        return valid_slots
