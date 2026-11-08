"""CLI entry point for schedul-ai."""
import argparse
from datetime import datetime, timedelta
from schedul.models import Person, TimeSlot, Event
from schedul.calendar import PersonalCalendar, MultiCalendar
from schedul.scheduler import SchedulingEngine
from schedul.optimizer import SlotScorer
from schedul.ical import generate_ical


def main():
    parser = argparse.ArgumentParser(description="Schedul-AI Intelligent Meeting Assistant")
    subparsers = parser.add_subparsers(dest="command", required=True)

    suggest_p = subparsers.add_parser("suggest")
    suggest_p.add_argument("--attendees", default="Alice,Bob")
    suggest_p.add_argument("--duration", type=int, default=60)
    suggest_p.add_argument("--ics", help="Output path for .ics calendar file")

    args = parser.parse_args()

    if args.command == "suggest":
        attendee_names = [a.strip() for a in args.attendees.split(",")]
        cals = {}
        for name in attendee_names:
            p = Person(id=name.lower(), name=name, email=f"{name.lower()}@example.com")
            cals[p.id] = PersonalCalendar(p)

        multi = MultiCalendar(cals)
        engine = SchedulingEngine(multi)

        now = datetime.now().replace(minute=0, second=0, microsecond=0) + timedelta(days=1, hours=9)
        search_range = TimeSlot(now, now + timedelta(hours=8))

        event = Event(
            id="evt1",
            title="Strategic Sync",
            organizer_id=attendee_names[0].lower(),
            attendee_ids=[n.lower() for n in attendee_names[1:]],
            duration_minutes=args.duration
        )

        candidates = engine.find_meeting_slots(event, search_range)
        ranked = SlotScorer.rank_slots(candidates)

        print(f"Top suggested slots for {args.attendees} (Duration: {args.duration}m):")
        for slot, score in ranked[:5]:
            print(f"  - {slot.start.strftime('%Y-%m-%d %H:%M')} to {slot.end.strftime('%H:%M')} (Score: {score})")

        if args.ics and ranked:
            best_slot = ranked[0][0]
            ics_content = generate_ical("Strategic Sync", best_slot)
            with open(args.ics, "w", encoding="utf-8") as f:
                f.write(ics_content)
            print(f"\nBest meeting saved to {args.ics}")


if __name__ == "__main__":
    main()
