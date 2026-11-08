"""Scheduling resolution engine for Schedul-AI."""
from typing import List, Optional
from schedul.models import Event, TimeSlot
from schedul.calendar import MultiCalendar


class SchedulingEngine:
    def __init__(self, multi_calendar: MultiCalendar):
        self.multi_calendar = multi_calendar

    def find_meeting_slots(self, event: Event, search_range: TimeSlot) -> List[TimeSlot]:
        all_participants = [event.organizer_id] + event.attendee_ids
        return self.multi_calendar.get_common_free_slots(
            person_ids=all_participants,
            search_range=search_range,
            duration=event.duration_minutes
        )

    def schedule_event(self, event: Event, slot: TimeSlot) -> bool:
        all_participants = [event.organizer_id] + event.attendee_ids
        for pid in all_participants:
            cal = self.multi_calendar.calendars.get(pid)
            if not cal or not cal.is_available(slot):
                return False

        for pid in all_participants:
            self.multi_calendar.calendars[pid].add_event(slot, event.title)
        return True
