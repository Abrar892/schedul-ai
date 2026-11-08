"""Domain models for Schedul-AI."""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional


@dataclass
class Person:
    id: str
    name: str
    email: str
    timezone: str = "UTC"


@dataclass
class TimeSlot:
    start: datetime
    end: datetime

    @property
    def duration_minutes(self) -> int:
        return int((self.end - self.start).total_seconds() / 60)

    def overlaps(self, other: "TimeSlot") -> bool:
        return self.start < other.end and other.start < self.end

    def contains(self, other: "TimeSlot") -> bool:
        return self.start <= other.start and other.end <= self.end


@dataclass
class Event:
    id: str
    title: str
    organizer_id: str
    attendee_ids: List[str]
    duration_minutes: int
    priority: int = 1
    deadline: Optional[datetime] = None


@dataclass
class Constraint:
    type: str  # 'working_hours', 'blocked_time'
    person_id: str
    start_time: datetime
    end_time: datetime
