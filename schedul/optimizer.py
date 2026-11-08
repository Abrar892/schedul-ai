"""Heuristic slot optimizer and ranking."""
from typing import List, Tuple
from schedul.models import Event, TimeSlot, Person


class SlotScorer:
    """Scores candidate slots by convenience, time-of-day, and schedule health."""

    @staticmethod
    def score_slot(slot: TimeSlot) -> float:
        # Prefer mid-day hours (10:00 - 15:00)
        hour = slot.start.hour
        if 10 <= hour <= 14:
            base_score = 0.95
        elif 9 <= hour <= 17:
            base_score = 0.80
        else:
            base_score = 0.40

        # Avoid weekends
        weekday = slot.start.weekday()
        if weekday >= 5:
            base_score *= 0.5

        return round(base_score, 2)

    @classmethod
    def rank_slots(cls, slots: List[TimeSlot]) -> List[Tuple[TimeSlot, float]]:
        scored = [(s, cls.score_slot(s)) for s in slots]
        return sorted(scored, key=lambda x: x[1], reverse=True)
