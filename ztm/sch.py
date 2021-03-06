from datetime import datetime, timezone
from itertools import chain, repeat
from typing import AbstractSet, MutableSet

from .consts import DAY, HOUR, MINUTE, MONTH, WEEK, YEAR
from .types import Snaps


def tabulate(snapshots: AbstractSet[datetime], now: datetime) -> Snaps:
    recent = {*snapshots}

    gt_year = {snap for snap in recent if now - snap >= YEAR}
    recent -= gt_year

    month_year = {snap for snap in recent if now - snap >= MONTH}
    recent -= month_year

    day_month = {snap for snap in recent if now - snap >= DAY}
    recent -= day_month

    hour_day = {snap for snap in recent if now - snap >= HOUR}
    recent -= hour_day

    future = {snap for snap in recent if snap > now}
    recent -= future

    snaps = Snaps(
        gt_year=gt_year,
        month_year=month_year,
        day_month=day_month,
        hour_day=hour_day,
        le_hour=recent,
        future=future,
    )
    return snaps


def take(snaps: Snaps) -> bool:
    return not snaps.le_hour


def keep(snaps: Snaps) -> AbstractSet[datetime]:
    acc: MutableSet[datetime] = set()

    series = (
        (snaps.future, repeat(MINUTE)),
        (snaps.le_hour, repeat(MINUTE)),
        (snaps.hour_day, chain((MINUTE,), repeat(HOUR))),
        (snaps.day_month, chain((HOUR,), repeat(DAY))),
        (snaps.month_year, chain((DAY,), repeat(WEEK))),
        (snaps.gt_year, chain((WEEK,), repeat(MONTH))),
    )

    prev = datetime.max.replace(tzinfo=timezone.utc)
    for snapshots, deltas in series:
        for snapshot, delta in zip(sorted(snapshots, reverse=True), deltas):
            if prev - snapshot >= delta:
                acc.add(snapshot)
                prev = snapshot

    return acc
