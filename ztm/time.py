from datetime import datetime, timezone


def now() -> datetime:
    return datetime.now(tz=timezone.utc).replace(microsecond=0)


def utc_to_local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
