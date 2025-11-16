# detect/fvg.py
from typing import List, Tuple
import pandas as pd

"""
Detects Fair Value Gaps (FVGs) using strict ICT rules.

Parameters:
    df (pd.DataFrame): OHLC data with columns ['Open', 'High', 'Low', 'Close'] and datetime index
    min_size (float): Minimum gap size in points. FVGs smaller than this are ignored (default: 0.0 = all)

Returns:
    List[Tuple[Timestamp, size, type]]:
        - Timestamp: Start time of FVG (first candle of the 3-candle pattern)
        - size: Gap size in price points (float)
        - type: "Bullish" or "Bearish"
"""
def detect_fvg_starts(
    df: pd.DataFrame,
    min_size: float = 0.0
) -> List[Tuple[pd.Timestamp, float, str]]:
    if len(df) < 3:
        return []

    fvg_list = []
    high = df['High'].values
    low = df['Low'].values
    idx = df.index

    for i in range(2, len(df)):
        high_1 = high[i - 2]   # Candle 1
        low_1  = low[i - 2]
        low_3  = low[i]        # Candle 3
        high_3 = high[i]

        # Bullish FVG: price jumped up, leaving a gap below
        if low_3 > high_1:
            gap_size = low_3 - high_1
            if gap_size >= min_size:
                fvg_list.append((idx[i - 2], gap_size, "Bullish"))

        # Bearish FVG: price dropped, leaving a gap above
        elif high_3 < low_1:
            gap_size = low_1 - high_3
            if gap_size >= min_size:
                fvg_list.append((idx[i - 2], gap_size, "Bearish"))

    return fvg_list