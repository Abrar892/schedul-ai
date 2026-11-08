"""Full automated test suite for schedul-ai."""
import unittest
from datetime import datetime, timedelta
from schedul.models import Person, TimeSlot, Event, Constraint
from schedul.calendar import PersonalCalendar, MultiCalendar
from schedul.scheduler import SchedulingEngine
from schedul.optimizer import SlotScorer
from schedul.ical import generate_ical


class TestSchedulAI(unittest.TestCase):
    def setUp(self):
        self.p1 = Person(id="alice", name="Alice", email="alice@test.com")
        self.p2 = Person(id="bob", name="Bob", email="bob@test.com")
        self.cal1 = PersonalCalendar(self.p1)
        self.cal2 = PersonalCalendar(self.p2)
        self.multi = MultiCalendar({"alice": self.cal1, "bob": self.cal2})
        self.engine = SchedulingEngine(self.multi)

    def test_slot_overlap(self):
        t0 = datetime(2026, 11, 10, 10, 0)
        s1 = TimeSlot(t0, t0 + timedelta(hours=1))
        s2 = TimeSlot(t0 + timedelta(minutes=30), t0 + timedelta(hours=2))
        s3 = TimeSlot(t0 + timedelta(hours=2), t0 + timedelta(hours=3))
        self.assertTrue(s1.overlaps(s2))
        self.assertFalse(s1.overlaps(s3))

    def test_find_and_schedule_meeting(self):
        day_start = datetime(2026, 11, 10, 9, 0)
        search_range = TimeSlot(day_start, day_start + timedelta(hours=8))

        # Block Bob at 10:00 - 11:00
        bob_busy = TimeSlot(day_start + timedelta(hours=1), day_start + timedelta(hours=2))
        self.cal2.add_event(bob_busy, "Dental Appt")

        event = Event("e1", "Architecture Review", "alice", ["bob"], 60)
        free_slots = self.engine.find_meeting_slots(event, search_range)

        # None of the suggested slots should overlap with Bob's appointment
        for s in free_slots:
            self.assertFalse(s.overlaps(bob_busy))

        best_slot = free_slots[0]
        self.assertTrue(self.engine.schedule_event(event, best_slot))
        self.assertFalse(self.cal1.is_available(best_slot))
        self.assertFalse(self.cal2.is_available(best_slot))

    def test_slot_scorer(self):
        s_midday = TimeSlot(datetime(2026, 11, 10, 12, 0), datetime(2026, 11, 10, 13, 0))
        s_night = TimeSlot(datetime(2026, 11, 10, 22, 0), datetime(2026, 11, 10, 23, 0))
        self.assertGreater(SlotScorer.score_slot(s_midday), SlotScorer.score_slot(s_night))

    def test_ical_generation(self):
        slot = TimeSlot(datetime(2026, 11, 10, 10, 0), datetime(2026, 11, 10, 11, 0))
        ics = generate_ical("Team Standup", slot)
        self.assertIn("BEGIN:VCALENDAR", ics)
        self.assertIn("SUMMARY:Team Standup", ics)
        self.assertIn("END:VCALENDAR", ics)


if __name__ == "__main__":
    unittest.main()
