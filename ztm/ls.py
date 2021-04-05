from datetime import datetime, timezone
from json import dump
from locale import strxfrm
from sys import stdout
from typing import MutableMapping, MutableSequence

from .zfs import ls_snapshots


def _utc_to_local(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc).astimezone(tz=None)


def pretty_print() -> None:
    snap_set = ls_snapshots()
    acc: MutableMapping[str, MutableSequence[str]] = {}

    for key in sorted(snap_set.keys(), key=lambda k: strxfrm(str(k))):
        for val in sorted(snap_set[key], reverse=True):
            value = _utc_to_local(val).strftime("%x %X %Z")
            acc.setdefault(str(key)).append(value)

    dump(acc, stdout, check_circular=False, ensure_ascii=False, indent=2)
