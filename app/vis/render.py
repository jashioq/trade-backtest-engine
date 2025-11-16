# vis/render.py
import pandas as pd
import mplfinance as mpf
from typing import List, Tuple, Optional, Dict, Any

"""
Renders a candlestick chart.
Supports drawing lines with individual colors/styles/widths.

Parameters:
    df             : OHLC DataFrame with datetime index
    lines          : List of lines → [(t1, p1, t2, p2), ...]  (None = no lines)
    line_colors    : List of colors (one per line, or single color repeated)
    line_styles    : List of styles ("-", "--", ":", "-.") per line
    line_widths    : List of linewidths per line
    filename       : Output PNG
    title          : Chart title
"""
def plot_candles(
    df: pd.DataFrame,
    lines: Optional[List[Tuple[pd.Timestamp, float, pd.Timestamp, float]]] = None,
    line_colors: Optional[List[str]] = None,
    line_styles: Optional[List[str]] = None,
    line_widths: Optional[List[float]] = None,
    filename: str = "chart.png",
    title: Optional[str] = None
) -> None:
    # Style
    market_colors = mpf.make_marketcolors(
        up='#4caf50', down='black', edge='black', wick='black', inherit=True
    )

    style = mpf.make_mpf_style(
        base_mpl_style='classic',
        marketcolors=market_colors,
        gridstyle='', gridcolor='none',
        facecolor='#d1d4dc',
        figcolor='#d1d4dc',
        rc={
            'ytick.left': False,
            'ytick.labelleft': False,
            'axes.labelcolor': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'xtick.labelsize': 24,
            'font.size': 24,
            'figure.titlesize': 24,
            'figure.titleweight': 'bold',
            'lines.linewidth': 4.0,
            'lines.color': 'black',
            'lines.antialiased': False,
        }
    )

    # Lines
    alines_dict: Optional[Dict[str, Any]] = None

    if lines:
        first = df.index.min()
        last = df.index.max()

        segments = []
        colors = []
        styles = []
        widths = []

        # Default fallbacks
        default_color = line_colors[0] if line_colors and len(line_colors) == 1 else "red"
        default_style = line_styles[0] if line_styles and len(line_styles) == 1 else "-"
        default_width = line_widths[0] if line_widths and len(line_widths) == 1 else 3.5

        for i, (t1_raw, p1, t2_raw, p2) in enumerate(lines):
            # Clip to data range
            t1 = max(t1_raw, first)
            t1 = min(t1, last)
            t2 = max(t2_raw, first)
            t2 = min(t2, last)

            if t1 == t2:
                t2 = t1 + pd.Timedelta(seconds=1)

            segments.append(((t1, p1), (t2, p2)))

            # Per-line styling
            colors.append(line_colors[i] if line_colors and i < len(line_colors) else default_color)
            styles.append(line_styles[i] if line_styles and i < len(line_styles) else default_style)
            widths.append(line_widths[i] if line_widths and i < len(line_widths) else default_width)

        alines_dict = {
            "alines": segments,
            "colors": colors,
            "linestyle": styles,
            "linewidths": widths,
        }

    # Plot
    savefig_dict = {
        "fname": filename,
        "dpi": 100,
        "bbox_inches": "tight",
        "pad_inches": 0.35,
        "facecolor": "#d1d4dc"
    }

    kwargs = {
        "type": "candle",
        "style": style,
        "volume": False,
        "show_nontrading": False,
        "figsize": (19.20, 10.80),
        "tight_layout": True,
        "xrotation": 0,
        "datetime_format": "%H:%M",
        "ylabel": "",
        "savefig": savefig_dict,
    }

    if title:
        kwargs["title"] = title
    if alines_dict:
        kwargs["alines"] = alines_dict

    mpf.plot(df, **kwargs)

    print(f"Chart saved: {filename}")