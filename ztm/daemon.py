from datetime import datetime, timezone
from pathlib import PurePath
from subprocess import CalledProcessError
from sys import stderr
from time import sleep
from typing import AbstractSet, Iterable

from .sch import keep, tabulate, take
from .zfs import ls_snapshots, rm_snapshot, take_snapshot


def _unify(paths: AbstractSet[PurePath]) -> AbstractSet[PurePath]:
    return {p for p in paths if {*p.parents}.isdisjoint(paths)}


def mon(paths: Iterable[PurePath]) -> None:
    datasets = _unify({*paths})
    while True:
        now = datetime.now(tz=timezone.utc).replace(microsecond=0)
        try:
            snap_set = ls_snapshots()

            for dataset in datasets:
                snapshots = snap_set.get(dataset, set())
                snaps = tabulate(snapshots, now=now)
                do_take = take(snaps)
                do_keep = keep(snaps)

                if do_take:
                    take_snapshot(dataset, time=now)
                for time in snapshots - do_keep:
                    rm_snapshot(dataset, time=time)
        except CalledProcessError as e:
            print(e, file=stderr)

        sleep(60)
