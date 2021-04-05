from dataclasses import dataclass
from datetime import datetime
from typing import AbstractSet


@dataclass(frozen=True)
class Snaps:
    gt_year: AbstractSet[datetime]
    month_year: AbstractSet[datetime]
    day_month: AbstractSet[datetime]
    hour_day: AbstractSet[datetime]
    le_hour: AbstractSet[datetime]
    future: AbstractSet[datetime]
