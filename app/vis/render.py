import pandas as pd
import mplfinance as mpf
from typing import List, Tuple, Optional

def plot_candles(
    df: pd.DataFrame,
    lines: Optional[List[Tuple[pd.Timestamp, float, pd.Timestamp, float]]] = None,
    line_colors: Optional[List[str]] = None,
    line_styles: Optional[List[str]] = None,
    line_widths: Optional[List[float]] = None,

    rectangles: Optional[List[Tuple[pd.Timestamp, pd.Timestamp, float, float]]] = None,
    rect_colors: Optional[List[str]] = None,
    rect_styles: Optional[List[str]] = None,
    rect_widths: Optional[List[float]] = None,

    filename: str = "chart.png",
    title: Optional[str] = None
) -> None:

    market_colors = mpf.make_marketcolors(up='#4caf50', down='black', edge='black', wick='black', inherit=True)
    mpf_style = mpf.make_mpf_style(
        base_mpl_style='classic',
        marketcolors=market_colors,
        gridstyle='', gridcolor='none',
        facecolor='#d1d4dc', figcolor='#d1d4dc',
        rc={
            'ytick.left': False, 'ytick.labelleft': False,
            'xtick.labelsize': 24, 'font.size': 24,
            'figure.titlesize': 24, 'figure.titleweight': 'bold',
            'lines.linewidth': 4.0, 'lines.color': 'black', 'lines.antialiased': False,
            'lines.linestyle': '-'
        }
    )

    all_segments = []
    all_colors   = []
    all_styles   = []
    all_widths   = []

    first = df.index.min()
    last  = df.index.max()

    if lines:
        default_c = line_colors[0] if line_colors and len(line_colors) == 1 else "red"
        default_s = line_styles[0] if line_styles and len(line_styles) == 1 else "-"
        default_w = line_widths[0] if line_widths and len(line_widths) == 1 else 3.5

        for i, (t1_raw, p1, t2_raw, p2) in enumerate(lines):
            t1 = max(t1_raw, first); t1 = min(t1, last)
            t2 = max(t2_raw, first); t2 = min(t2, last)
            if t1 == t2: t2 = t1 + pd.Timedelta(seconds=1)

            all_segments.append(((t1, p1), (t2, p2)))
            all_colors.append(line_colors[i] if line_colors and i < len(line_colors) else default_c)
            all_styles.append(line_styles[i] if line_styles and i < len(line_styles) else default_s)
            all_widths.append(line_widths[i] if line_widths and i < len(line_widths) else default_w)

    if rectangles:
        default_color = rect_colors[0] if rect_colors and len(rect_colors) == 1 else "royalblue"
        default_style = rect_styles[0] if rect_styles and len(rect_styles) == 1 else "--"
        default_width = rect_widths[0] if rect_widths and len(rect_widths) == 1 else 1.8

        for i, (start_raw, end_raw, top, bottom) in enumerate(rectangles):
            color = rect_colors[i] if rect_colors and i < len(rect_colors) else default_color
            rect_style = rect_styles[i] if rect_styles and i < len(rect_styles) else default_style
            width = rect_widths[i] if rect_widths and i < len(rect_widths) else default_width

            s = max(start_raw, first)
            e = min(end_raw, last)

            all_segments.extend([
                ((s, top),     (e, top)),
                ((s, bottom),  (e, bottom)),
                ((s, bottom),  (s, top)),
                ((e, bottom),  (e, top))
            ])
            all_colors.extend([color] * 4)
            all_styles.extend([rect_style] * 4)
            all_widths.extend([width] * 4)

    alines_dict = None
    if all_segments:
        alines_dict = {
            "alines": all_segments,
            "colors": all_colors,
            "linestyle": all_styles,
            "linewidths": all_widths
        }

    savefig_dict = {"fname": filename, "dpi": 100, "bbox_inches": "tight", "pad_inches": 0.35, "facecolor": "#d1d4dc"}

    kwargs = {
        "type": "candle",
        "style": mpf_style,
        "volume": False,
        "show_nontrading": False,
        "figsize": (19.20, 10.80),
        "tight_layout": True,
        "xrotation": 0,
        "datetime_format": "%H:%M",
        "ylabel": "",
        "savefig": savefig_dict,
    }
    if title: kwargs["title"] = title
    if alines_dict: kwargs["alines"] = alines_dict

    mpf.plot(df, **kwargs)
    print(f"Chart saved: {filename}")
