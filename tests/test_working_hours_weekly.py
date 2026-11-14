"""Tests for schedul-ai working hours profile and weekly calendar view."""

import unittest
from datetime import datetime, time, timedelta
from schedul.models import TimeSlot, Event
from schedul.working_hours import WorkingHoursProfile
from schedul.weekly_view import WeeklyCalendarView


class TestWorkingHoursAndWeeklyView(unittest.TestCase):
    def test_working_hours_profile(self):
        wh = WorkingHoursProfile(start_hour=9, end_hour=17) # 9am-5pm Mon-Fri
        
        # Valid slot: Monday 10:00 - 11:00 (Nov 9, 2026 is Monday)
        valid_slot = TimeSlot(datetime(2026, 11, 9, 10, 0), datetime(2026, 11, 9, 11, 0))
        self.assertTrue(wh.is_within_working_hours(valid_slot))

        # Invalid slot: Monday 08:00 - 09:30 (starts before 9am)
        early_slot = TimeSlot(datetime(2026, 11, 9, 8, 0), datetime(2026, 11, 9, 9, 30))
        self.assertFalse(wh.is_within_working_hours(early_slot))

        # Invalid slot: Sunday 10:00 - 11:00 (Nov 15, 2026 is Sunday)
        weekend_slot = TimeSlot(datetime(2026, 11, 15, 10, 0), datetime(2026, 11, 15, 11, 0))
        self.assertFalse(wh.is_within_working_hours(weekend_slot))

    def test_weekly_view_rendering(self):
        week_start = datetime(2026, 11, 9) # Monday
        wv = WeeklyCalendarView(week_start)

        ev = Event(id="e1", title="Sprint Review", organizer_id="u1", attendee_ids=["u1", "u2"], duration_minutes=60)
        slot = TimeSlot(datetime(2026, 11, 9, 14, 0), datetime(2026, 11, 9, 15, 0))

        rendered = wv.render_ascii_week([(ev, slot)])
        self.assertIn("WEEKLY SCHEDULE", rendered)
        self.assertIn("Sprint Review", rendered)
        self.assertIn("14:00 - 15:00", rendered)


if __name__ == "__main__":
    unittest.main()
