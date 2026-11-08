# Schedul-AI

Intelligent scheduling assistant using rule-based heuristics and constraint satisfaction.

## Features
- **Multi-person Availability:** Models complex calendars across teammates with timezone awareness.
- **Constraint Satisfaction:** Discovers conflict-free meeting windows honoring working hours and blocked slots.
- **Heuristic Optimizer:** Scores and ranks potential slots based on time-of-day preference, weekday convenience, and schedule balance.
- **iCalendar (.ics) Export:** Generates RFC 5545 compliant `.ics` calendar events.
- **Zero External Dependencies:** Built with pure Python 3.12 standard library.

## Quickstart
```bash
python -m schedul.cli suggest --attendees "Alice,Bob" --duration 60
```
