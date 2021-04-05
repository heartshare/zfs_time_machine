from datetime import datetime
from unittest import TestCase

from ..ztm.consts import WEEK
from ..ztm.sch import keep, tabulate
from ..ztm.types import Snaps


class Tabulate(TestCase):
    def test_1(self) -> None:
        self.assertEqual(1, 1)


class Keep(TestCase):
    def test_1(self) -> None:
        self.assertEqual(1, 1)
