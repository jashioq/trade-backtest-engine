import pandas as pd
import mplfinance as mpf
from typing import List, Optional
from app.vis.model.drawable import Drawable

def render(
        df: pd.DataFrame,
        drawables: List[Drawable],
        filename: str = "chart.png",
        title: Optional[str] = None,
) -> None:

    market_colors = mpf.make_marketcolors(
        up='#4caf50', down='black', edge='black', wick='black', inherit=True
    )
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

    segments = []
    colors = []
    styles = []
    widths = []

    first = df.index.min()
    last = df.index.max()

    for obj in drawables:
        t1 = max(obj.start_time, first)
        t1 = min(t1, last)
        t2 = max(obj.end_time, first)
        t2 = min(t2, last)

        segments.append(((t1, obj.start_price), (t2, obj.end_price)))
        colors.append(obj.color)
        styles.append(obj.style)
        widths.append(obj.width)

    alines_dict = None
    if segments:
        alines_dict = {
            "alines": segments,
            "colors": colors,
            "linestyle": styles,
            "linewidths": widths,
        }

    savefig_dict = {
        "fname": filename,
        "dpi": 100,
        "bbox_inches": "tight",
        "pad_inches": 0.35,
        "facecolor": "#d1d4dc"
    }

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
    if title:
        kwargs["title"] = title
    if alines_dict:
        kwargs["alines"] = alines_dict

    mpf.plot(df, **kwargs)
    print(f"Chart saved: {filename}")
