from datetime import datetime
from pathlib import PurePath
from subprocess import check_call, check_output
from typing import AbstractSet, Mapping, MutableMapping, MutableSet, Optional, Tuple

from .consts import DATASET_MARK, SNAP_PREFIX


def _unify(paths: AbstractSet[PurePath]) -> AbstractSet[PurePath]:
    return {p for p in paths if {*p.parents}.isdisjoint(paths)}


def ls_datasets() -> AbstractSet[PurePath]:
    raw = check_output(
        ("zfs", "get", DATASET_MARK, "-t", "filesystem", "-H", "-o", "value,name"),
        text=True,
    ).rstrip()
    acc: MutableSet[PurePath] = set()

    for line in raw.splitlines():
        if line.startswith("-"):
            pass
        else:
            _, _, dataset = line.partition("\t")
            acc.add(PurePath(dataset))

    datasets = _unify(acc)
    return datasets


def _unparse(dataset: PurePath, time: datetime) -> str:
    iso_date = time.replace(tzinfo=None).isoformat()
    name = f"{dataset}@{SNAP_PREFIX}{iso_date}"
    return name


def _parse(fullname: str) -> Optional[Tuple[PurePath, datetime]]:
    dataset, _, snapshot = fullname.partition("@")
    if snapshot.startswith(SNAP_PREFIX):
        maybe_date = snapshot[len(SNAP_PREFIX) :]
        maybe_iso = maybe_date + "+00:00"
        try:
            dt = datetime.fromisoformat(maybe_iso)
        except ValueError:
            return None
        else:
            return PurePath(dataset), dt
    else:
        return None


def ls_snapshots() -> Mapping[PurePath, AbstractSet[datetime]]:
    raw = check_output(
        ("zfs", "list", "-t", "snapshot", "-H", "-o", "name"), text=True
    ).rstrip()

    acc: MutableMapping[PurePath, MutableSet[datetime]] = {}

    for line in raw.splitlines():
        ans = _parse(line)
        if ans:
            dataset, time = ans
            acc.setdefault(dataset, set()).add(time)

    return acc


def take_snapshot(dataset: PurePath, time: datetime) -> None:
    name = _unparse(dataset, time=time)
    check_call(("zfs", "snapshot", "-r", name))


def rm_snapshot(dataset: PurePath, time: datetime) -> None:
    name = _unparse(dataset, time=time)
    check_call(("zfs", "destroy", "-d", "-r", name))
