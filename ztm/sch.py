from datetime import datetime
from itertools import chain, repeat
from typing import AbstractSet, MutableSet

from .consts import DAY, HOUR, MONTH, WEEK, ZERO
from .types import Snaps


def tabulate(snapshots: AbstractSet[datetime], now: datetime) -> Snaps:
    recent = {*snapshots}

    gt_month = {snap for snap in recent if now - snap > MONTH}
    recent -= gt_month

    week_month = {snap for snap in recent if now - snap > WEEK}
    recent -= week_month

    day_week = {snap for snap in recent if now - snap > DAY}
    recent -= day_week

    hour_day = {snap for snap in recent if now - snap > HOUR}
    recent -= hour_day

    snaps = Snaps(
        gt_month=gt_month,
        week_month=week_month,
        day_week=day_week,
        hour_day=hour_day,
        le_hour=recent,
    )
    return snaps


def take(snaps: Snaps) -> bool:
    return not snaps.le_hour


def keep(snaps: Snaps) -> AbstractSet[datetime]:
    acc: MutableSet[datetime] = set()

    series = (
        (snaps.le_hour, repeat(ZERO)),
        (snaps.hourly, chain((ZERO,), repeat(HOUR))),
        (snaps.daily, chain((HOUR,), repeat(DAY))),
        (snaps.weekly, repeat(DAY)),
        (snaps.monthly, chain((WEEK,), repeat(MONTH))),
    )

    prev = datetime.max
    for snapshots, deltas in series:
        for snapshot, delta in zip(sorted(snapshots, reverse=True), deltas):
            if prev - snapshot >= delta:
                acc.add(snapshot)
                prev = snapshot

    return acc
