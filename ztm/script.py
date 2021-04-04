from .zfs import ls_snapshots, rm_snapshot, take_snapshot

from json import dump
from locale import strxfrm
from pathlib import PurePath
from sys import stdout





def _pretty_print() -> None:
    snap_set = ls_snapshots()
    acc: MutableMapping[str, MutableSequence[str]] = {}

    for key in sorted(snap_set.keys(), key=lambda k: strxfrm(str(k))):
        for val in sorted(snap_set[key], reverse=True):
            value = val.strftime("%x %X %Z")
            acc.setdefault(str(key)).append(value)

    dump(acc, stdout, check_circular=False, ensure_ascii=False, indent=2)


