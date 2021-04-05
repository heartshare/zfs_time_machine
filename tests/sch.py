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
        t1 = {self.now - MINUTE * n for n in range(HOUR // MINUTE + 1)}
        t2 = {self.now - HOUR * n for n in range(DAY // HOUR + 1)}
        t3 = {self.now - DAY * n for n in range(MONTH // DAY + 1)}
        snapshots = t1 | t2 | t3
        assert len(snapshots) == len(t1) + len(t2) + len(t3)

        snaps = tabulate(snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(snapshots, kept)

    def test_3(self) -> None:
        t1 = {self.now - MINUTE * n for n in range(HOUR // MINUTE + 2)}
        t2 = {self.now - HOUR * n for n in range(DAY // HOUR + 2)}
        t3 = {self.now - DAY * n for n in range(MONTH // DAY + 2)}
        snapshots = t1 | t2 | t3
        assert len(snapshots) == len(t1) + len(t2) + len(t3)

        snaps = tabulate(snapshots, now=self.now)
        kept = keep(snaps)
        self.assertEqual(len(snapshots - kept), 3)
