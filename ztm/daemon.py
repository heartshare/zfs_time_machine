from typing import AbstractSet, Iterable
from pathlib import PurePath

from .dt import now

def _unify(paths: AbstractSet[PurePath]) -> AbstractSet[PurePath]:
    return {p for p in paths if {*p.parents}.isdisjoint(paths)}

def mon(paths: Iterable[PurePath]) -> None:
    now = now()
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

