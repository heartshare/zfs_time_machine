from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone
from itertools import chain, repeat
from json import dump
from locale import strxfrm
from pathlib import PurePath
from sys import stdout
from typing import AbstractSet, Iterable, MutableMapping, MutableSequence, MutableSet

from .consts import DAY, HOUR, MONTH, WEEK, YEAR, ZERO
from .types import Snaps
from .zfs import ls_snapshots, rm_snapshot, take_snapshot


def _now() -> datetime:
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


def _tabulate(snapshots: AbstractSet[datetime], now: datetime) -> Snaps:
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


def _take(snaps: Snaps) -> bool:
    return not snaps.recent


def _keep(snaps: Snaps) -> AbstractSet[datetime]:
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


def _unify(paths: AbstractSet[PurePath]) -> AbstractSet[PurePath]:
    return {p for p in paths if {*p.parents}.isdisjoint(paths)}


def _pretty_print() -> None:
    snap_set = ls_snapshots()
    acc: MutableMapping[str, MutableSequence[str]] = {}

    for key in sorted(snap_set.keys(), key=lambda k: strxfrm(str(k))):
        for val in sorted(snap_set[key], reverse=True):
            value = val.strftime("%x %X %Z")
            acc.setdefault(str(key)).append(value)

    dump(acc, stdout, check_circular=False, ensure_ascii=False, indent=2)


def _mon(paths: Iterable[PurePath]) -> None:
    now = _now()
    snap_set = ls_snapshots()
    datasets = _unify({*paths})
    for dataset in datasets:
        snapshots = snap_set.get(dataset, set())
        snaps = _tabulate(snapshots, now=now)
        take = _take(snaps)
        keep = _keep(snaps)

        if take:
            take_snapshot(dataset, time=now)
        for time in snapshots - keep:
            rm_snapshot(dataset, time=time)


def _parse_args() -> Namespace:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title="operation", required=True)

    _ = subparsers.add_parser("ls")

    daemon = subparsers.add_parser("daemon")
    daemon.add_argument("datasets", type=PurePath, nargs="+")

    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    if args.operation == "ls":
        _pretty_print()
    elif args.operation == "daemon":
        _mon(args.datasets)
    else:
        assert False


main()
