from abc import ABC
from dataclasses import dataclass
from datetime import datetime

class Swing(ABC):
    pass

@dataclass(frozen=True, slots=True)
class BullishSwing(Swing):
    start: datetime
    end: datetime
    high: float
    low: float


@dataclass(frozen=True, slots=True)
class BearishSwing(Swing):
    start: datetime
    end: datetime
    high: float
    low: float
