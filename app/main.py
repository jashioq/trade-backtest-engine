# main.py
import pandas as pd
from data.load import load_candles
from detect.fvg import detect_fvg_starts
from vis.render import plot_candles

if __name__ == "__main__":
    # Time range
    start_time = pd.Timestamp("2025-10-29 9:30:00")
    end_time = pd.Timestamp("2025-10-29 12:00:00")

    # Load data
    df = load_candles(start_time, end_time)

    # Detect FVGs
    min_size = 5
    fvgs = detect_fvg_starts(df, min_size)

    # Build lines
    lines = []
    colors = []
    styles = []
    widths = []

    for start_ts, size, fvg_type in fvgs:
        start_idx = df.index.get_loc(start_ts)

        # Get exact levels
        high_1 = df['High'].iloc[start_idx]
        low_1 = df['Low'].iloc[start_idx]
        low_3 = df['Low'].iloc[start_idx + 2]
        high_3 = df['High'].iloc[start_idx + 2]

        if fvg_type == "Bullish":
            bottom = high_1
            top = low_3
            color = "green"
        else:
            bottom = high_3
            top = low_1
            color = "red"

        # End time: 5 min after start
        end_ts = start_ts + pd.Timedelta(minutes=5)

        # Add bottom line
        lines.append((start_ts, bottom, end_ts, bottom))
        colors.append(color)
        styles.append("-")
        widths.append(3.5)

        # Add top line
        lines.append((start_ts, top, end_ts, top))
        colors.append(color)
        styles.append("-")
        widths.append(3.5)

    # Plot with all FVG lines
    plot_candles(
        df=df,
        lines=lines,
        line_colors=colors,
        line_styles=styles,
        line_widths=widths,
        filename="fvg_chart.png",
        title=f"{len(fvgs)} FVGs Detected | Minimum size {min_size}"
    )
