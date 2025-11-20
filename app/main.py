import pandas as pd

from app.detect.detect_fvg import detect_fvg
from app.detect.detect_swing import detect_swing
from app.vis.model.drawable import Drawable
from data.load import load_candles
from vis.render import render


if __name__ == "__main__":
    start_time = pd.Timestamp("2025-10-29 09:30:00")
    end_time   = pd.Timestamp("2025-10-29 12:00:00")

    min_fvg_size       = 5.0
    min_swing_length   = 3
    min_swing_points   = 30.0

    df = load_candles(start_time, end_time)

    fvgs   = detect_fvg(df, min_size=min_fvg_size)
    swings = detect_swing(df, min_length=min_swing_length, min_size_points=min_swing_points)

    drawables = []

    for fvg in fvgs:
        color = "limegreen" if fvg.__class__.__name__ == "Bisi" else "crimson"
        end_time = fvg.start + pd.Timedelta(minutes=5)

        drawables.extend([
            Drawable.horizontal_line(
                start_time=fvg.start,
                end_time=end_time,
                price=fvg.low,
                color=color,
                width=3.5
            ),
            Drawable.horizontal_line(
                start_time=fvg.start,
                end_time=end_time,
                price=fvg.high,
                color=color,
                width=3.5
            ),
        ])

    for swing in swings:
        drawables.extend(
            Drawable.rectangle(
                start_time=swing.start,
                end_time=swing.end,
                top=swing.high,
                bottom=swing.low,
                color="royalblue",
                style="--",
                width=1.6
            )
        )

    render(
        df=df,
        drawables=drawables,
        filename="chart.png",
        title=f"{len(fvgs)} FVGs {len(swings)} Swings | "
              f"FVG size {min_fvg_size}, "
              f"swing length {min_swing_length}, "
              f"swing size {min_swing_points}"
    )
