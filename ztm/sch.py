from datetime import datetime
from itertools import chain, repeat
from typing import AbstractSet, MutableSet

from .consts import DAY, HOUR, MONTH, WEEK, YEAR, ZERO
from .types import Snaps


def tabulate(snapshots: AbstractSet[datetime], now: datetime) -> Snaps:
    recent = {*snapshots}
    yearly = {snap for snap in recent if now - snap > YEAR}
    recent -= yearly
    monthly = {snap for snap in recent if now - snap > MONTH}
    recent -= monthly
    weekly = {snap for snap in recent if now - snap > WEEK}
    recent -= weekly
    daily = {snap for snap in recent if now - snap > DAY}
    recent -= daily
    hourly = {snap for snap in recent if now - snap > HOUR}
    recent -= hourly

    snaps = Snaps(
        yearly=yearly,
        monthly=monthly,
        weekly=weekly,
        daily=daily,
        hourly=hourly,
        recent=recent,
    )
    return snaps


def take(snaps: Snaps) -> bool:
    return not snaps.recent


def keep(snaps: Snaps) -> AbstractSet[datetime]:
    acc: MutableSet[datetime] = set()

    series = (
        (snaps.recent, repeat(ZERO)),
        (snaps.hourly, chain((ZERO,), repeat(HOUR))),
        (snaps.daily, chain((HOUR,), repeat(DAY))),
        (snaps.weekly, chain((DAY,), repeat(WEEK))),
        (snaps.monthly, chain((WEEK,), repeat(MONTH))),
        (snaps.yearly, chain((MONTH,), repeat(YEAR))),
    )

    prev = datetime.max
    for snapshots, deltas in series:
        for snapshot, delta in zip(sorted(snapshots, reverse=True), deltas):
            if prev - snapshot >= delta:
                acc.add(snapshot)
                prev = snapshot

    return acc
