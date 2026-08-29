from datetime import date, timedelta

EPOCH = date(2026, 1, 1)

def to_day(iso_date: str) -> int:
    y, m, d = map(int, iso_date.split("-"))
    return (date(y, m, d) - EPOCH).days

def from_day(day: int) -> str:
    return (EPOCH + timedelta(days=day)).isoformat()
