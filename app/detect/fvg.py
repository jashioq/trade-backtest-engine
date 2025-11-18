from typing import List, Tuple
import pandas as pd

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
        high_1 = high[i - 2]
        low_1  = low[i - 2]
        low_3  = low[i]
        high_3 = high[i]

        if low_3 > high_1:
            gap_size = low_3 - high_1
            if gap_size >= min_size:
                fvg_list.append((idx[i - 2], gap_size, "Bullish"))

        elif high_3 < low_1:
            gap_size = low_1 - high_3
            if gap_size >= min_size:
                fvg_list.append((idx[i - 2], gap_size, "Bearish"))

    return fvg_list
