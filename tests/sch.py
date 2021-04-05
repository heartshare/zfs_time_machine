from datetime import datetime, timezone
from unittest import TestCase

from ..ztm.consts import DAY, HOUR, MINUTE, MONTH, WEEK
from ..ztm.sch import keep, tabulate
from ..ztm.types import Snaps


class Tabulate(TestCase):
    def setUp(self) -> None:
        self.now = datetime.now(tz=timezone.utc)

    def test_1(self) -> None:
        snapshots = {
            self.now + MONTH,
            self.now + WEEK,
            self.now + DAY,
            self.now + HOUR,
            self.now + MINUTE,
        }
        snaps = tabulate(snapshots, now=self.now)
        print(snaps)


class Keep(TestCase):
    def test_1(self) -> None:
        snaps = Snaps(
            gt_month=set(),
            day_month=set(),
            hour_day=set(),
            le_hour=set(),
        )
        self.assertEqual(snaps, snaps)
