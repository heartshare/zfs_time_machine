from datetime import datetime, timezone
from unittest import TestCase

from ..ztm.consts import DAY, HOUR, MINUTE, MONTH, WEEK
from ..ztm.sch import keep, tabulate


class Tabulate(TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(tz=timezone.utc)

    def test_1(self) -> None:
        snapshots = {
            self.now - MONTH,
            self.now - WEEK,
            self.now - DAY,
            self.now - HOUR,
            self.now - MINUTE,
            self.now,
            self.now + MINUTE,
        }
        snaps = tabulate(snapshots, now=self.now)
        self.assertEqual(len(snaps.gt_month), 1)
        self.assertEqual(len(snaps.day_month), 2)
        self.assertEqual(len(snaps.hour_day), 1)
        self.assertEqual(len(snaps.le_hour), 2)
        self.assertEqual(len(snaps.future), 1)


class Keep(TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(tz=timezone.utc)
        self.t1 = {self.now - MINUTE * n for n in range(0, HOUR // MINUTE)}
        self.t2 = {self.now - HOUR * n for n in range(1, DAY // HOUR)}
        self.t3 = {self.now - DAY * n for n in range(1, MONTH // DAY)}
        self.t4 = {self.now - WEEK * n for n in range(MONTH // DAY, MONTH // DAY + 500)}

        self.snapshots = self.t1 | self.t2 | self.t3 | self.t4
        assert len(self.snapshots) == len(self.t1) + len(self.t2) + len(self.t3) + len(
            self.t4
        )
        assert len(self.snapshots) == HOUR // MINUTE + DAY // HOUR + MONTH // DAY + 498

    def test_1(self) -> None:
        snapshots = {
            self.now - MONTH,
            self.now - WEEK,
            self.now - DAY,
            self.now - HOUR,
            self.now - MINUTE,
            self.now,
            self.now + MINUTE,
        }
        snaps = tabulate(snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(snapshots, kept)

    def test_2(self) -> None:
        snaps = tabulate(self.snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(self.snapshots, kept)

    def test_3(self) -> None:
        superfluous = {self.now - MINUTE * n for n in range(100)} - self.snapshots
        self.snapshots |= superfluous
        snaps = tabulate(self.snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(self.snapshots - kept, superfluous)

    def test_4(self) -> None:
        superfluous = {self.now - HOUR * n for n in range(100)} - self.snapshots
        self.snapshots |= superfluous
        snaps = tabulate(self.snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(self.snapshots - kept, superfluous)
