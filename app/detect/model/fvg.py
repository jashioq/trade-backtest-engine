import datetime
from abc import ABC
from dataclasses import dataclass

class Fvg(ABC):
    pass

@dataclass(frozen=True)
class Bisi(Fvg):
    start: datetime
    low: float
    high: float

@dataclass(frozen=True)
class Sibi(Fvg):
    start: datetime
    low: float
    high: float
