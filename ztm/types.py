from dataclasses import dataclass
from datetime import datetime
from typing import AbstractSet


@dataclass(frozen=True)
class Snaps:
    gt_month: AbstractSet[datetime]
    day_month: AbstractSet[datetime]
    hour_day: AbstractSet[datetime]
    le_hour: AbstractSet[datetime]
