from datetime import datetime, timezone


def now() -> datetime:
    dt = datetime.now(tz=timezone.utc)
    now = datetime(
        tzinfo=dt.tzinfo,
        year=dt.year,
        month=dt.month,
        day=dt.day,
        hour=dt.hour,
        minute=dt.minute,
        second=dt.second,
    )
    return now


def utc_to_local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
