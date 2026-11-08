"""RFC 5545 iCalendar (.ics) generator."""
from datetime import datetime
from schedul.models import Event, TimeSlot


def format_ical_dt(dt: datetime) -> str:
    return dt.strftime("%Y%m%dT%H%M%SZ")


def generate_ical(title: str, slot: TimeSlot, organizer_email: str = "organizer@example.com") -> str:
    now_str = format_ical_dt(datetime.utcnow())
    start_str = format_ical_dt(slot.start)
    end_str = format_ical_dt(slot.end)

    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Schedul-AI//EN
CALSCALE:GREGORIAN
BEGIN:VEVENT
UID:{now_str}-{title.replace(' ', '_')}@schedul-ai
DTSTAMP:{now_str}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{title}
ORGANIZER:MAILTO:{organizer_email}
STATUS:CONFIRMED
END:VEVENT
END:VCALENDAR"""
