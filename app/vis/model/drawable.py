from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Literal, List

LineStyle = Literal["-", "--", ":", "-.", ""]
Color = str

@dataclass(frozen=True, slots=True)
class Drawable:
    start_time: datetime
    start_price: float
    end_time: datetime
    end_price: float

    color: Color = "royalblue"
    style: LineStyle = "-"
    width: float = 2.0

    @classmethod
    def horizontal_line(
        cls,
        start_time: datetime,
        end_time: datetime,
        price: float,
        *,
        color: Color = "royalblue",
        style: LineStyle = "-",
        width: float = 3.0,
    ) -> "Drawable":
        return cls(start_time, price, end_time, price, color, style, width)

    @classmethod
    def vertical_line(
        cls,
        time: datetime,
        low_price: float,
        high_price: float,
        *,
        color: Color = "royalblue",
        style: LineStyle = "-",
        width: float = 1.6,
    ) -> "Drawable":
        return cls(time, low_price, time, high_price, color, style, width)

    @classmethod
    def rectangle(
        cls,
        start_time: datetime,
        end_time: datetime,
        top: float,
        bottom: float,
        *,
        color: Color = "royalblue",
        style: LineStyle = "-",
        width: float = 1.6,
    ) -> List["Drawable"]:
        return [
            cls.horizontal_line(start_time, end_time, top,    color=color, style=style, width=width),
            cls.horizontal_line(start_time, end_time, bottom, color=color, style=style, width=width),
            cls.vertical_line(start_time, bottom, top,        color=color, style=style, width=width),
            cls.vertical_line(end_time,   bottom, top,        color=color, style=style, width=width),
        ]
