from datetime import datetime, timezone
from subprocess import CalledProcessError
from sys import stderr
from time import sleep

from .sch import keep, tabulate, take
from .zfs import ls_datasets, ls_snapshots, rm_snapshot, take_snapshot


def mon() -> None:
    while True:
        now = datetime.now(tz=timezone.utc).replace(microsecond=0)
        try:
            datasets = ls_datasets()
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
            print(e.cmd, e, file=stderr)

        sleep(60)
