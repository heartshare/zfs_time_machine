from json import dump
from locale import strxfrm
from sys import stdout
from typing import MutableMapping, MutableSequence

from .time import utc_to_local
from .zfs import ls_snapshots


def pretty_print() -> None:
    snap_set = ls_snapshots()
    acc: MutableMapping[str, MutableSequence[str]] = {}

    for key in sorted(snap_set.keys(), key=lambda k: strxfrm(str(k))):
        for val in sorted(snap_set[key], reverse=True):
            value = utc_to_local(val).strftime("%x %X %Z")
            acc.setdefault(str(key)).append(value)

    dump(acc, stdout, check_circular=False, ensure_ascii=False, indent=2)
