import pandas as pd

from app.detect.swing import detect_price_swings
from data.load import load_candles
from detect.fvg import detect_fvg_starts
from vis.render import plot_candles

if __name__ == "__main__":
    start_time = pd.Timestamp("2025-10-29 09:30:00")
    end_time   = pd.Timestamp("2025-10-29 12:00:00")

    min_fvg_size = 5
    min_swing_length = 3
    min_swing_points = 30
    df = load_candles(start_time, end_time)
    fvgs   = detect_fvg_starts(df, min_size=min_fvg_size)
    swings = detect_price_swings(df, min_length=min_swing_length, min_size_points=min_swing_points)

    print(f"Detected {len(fvgs)} FVGs and {len(swings)} price swings\n")

    fvg_lines = []
    fvg_colors = []
    fvg_styles = []
    fvg_widths = []

    for start_ts, size, fvg_type in fvgs:
        i = df.index.get_loc(start_ts)
        high_1 = df['High'].iloc[i]
        low_1  = df['Low'].iloc[i]
        low_3  = df['Low'].iloc[i + 2]
        high_3 = df['High'].iloc[i + 2]

        if fvg_type == "Bullish":
            bottom, top = high_1, low_3
            color = "limegreen"
        else:
            bottom, top = high_3, low_1
            color = "crimson"

        end_ts = start_ts + pd.Timedelta(minutes=5)

        fvg_lines.extend([
            (start_ts, bottom, end_ts, bottom),
            (start_ts, top,    end_ts, top)
        ])
        fvg_colors.extend([color, color])
        fvg_styles.extend(["-", "-"])
        fvg_widths.extend([3.5, 3.5])

    swing_rects   = []
    swing_colors  = ["royalblue"] * len(swings)
    swing_styles  = ["--"] * len(swings)
    swing_widths  = [1.6] * len(swings)

    for start_ts, end_ts, _, sh, sl in swings:
        swing_rects.append((start_ts, end_ts, sh, sl))

    plot_candles(
        df=df,
        lines=fvg_lines,
        line_colors=fvg_colors,
        line_styles=fvg_styles,
        line_widths=fvg_widths,

        rectangles=swing_rects,
        rect_colors=swing_colors,
        rect_styles=swing_styles,
        rect_widths=swing_widths,

        filename="chart.png",
        title=f"{len(fvgs)} FVGs {len(swings)} Swings | FVG size {min_fvg_size}, swing length {min_swing_length}, swing size {min_swing_points}"
    )
