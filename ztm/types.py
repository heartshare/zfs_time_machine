from dataclasses import dataclass
from datetime import datetime
from typing import AbstractSet


@dataclass(frozen=True)
class Snaps:
    yearly: AbstractSet[datetime]
    monthly: AbstractSet[datetime]
    weekly: AbstractSet[datetime]
    daily: AbstractSet[datetime]
    hourly: AbstractSet[datetime]
    recent: AbstractSet[datetime]
