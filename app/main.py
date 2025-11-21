import pandas as pd

from app.detect.detect_fvgs import detect_fvgs
from app.detect.detect_swings import detect_swings
from app.vis.model.drawable import Drawable
from data.load import load_candles
from vis.render import render

if __name__ == "__main__":
    start_time = pd.Timestamp("2025-10-23 09:30:00")
    end_time = pd.Timestamp("2025-10-23 12:00:00")

    min_fvg_size = 5.0
    min_swing_length = 3
    min_swing_points = 30.0

    df = load_candles(start_time, end_time)

    swings = detect_swings(df, min_length=min_swing_length, min_size_points=min_swing_points)

    # Detect FVGs only within swings
    fvgs = []
    for swing in swings:
        # Get the subset of data within this swing's time range
        swing_df = df.loc[swing.start:swing.end]

        # Detect FVGs only in this swing
        swing_fvgs = detect_fvgs(swing_df, min_size=min_fvg_size)
        fvgs.extend(swing_fvgs)

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
                width=2
            ),
            Drawable.horizontal_line(
                start_time=fvg.start,
                end_time=end_time,
                price=fvg.high,
                color=color,
                width=2
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
                width=1
            )
        ),
        drawables.extend([
            Drawable.horizontal_line(
                start_time=swing.start,
                end_time=swing.end,
                price=swing.ote_top,
                color="yellow",
                style=":",
                width=2
            ),
            Drawable.horizontal_line(
                start_time=swing.start,
                end_time=swing.end,
                price=swing.ote_bottom,
                color="yellow",
                style=":",
                width=2
            ),
        ])

    render(
        df=df,
        drawables=drawables,
        filename="chart.png",
        title=f"{len(fvgs)} FVGs {len(swings)} Swings | "
              f"FVG size {min_fvg_size}, "
              f"swing length {min_swing_length}, "
              f"swing size {min_swing_points}"
    )
