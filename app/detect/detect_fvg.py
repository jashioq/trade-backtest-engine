from typing import List
import pandas as pd

from app.detect.model.fvg import Fvg, Bisi, Sibi

def detect_fvg(df: pd.DataFrame, min_size: float = 0.0) -> List[Fvg]:
    if len(df) < 3:
        return []

    fvgs: List[Fvg] = []
    high = df['High'].values
    low = df['Low'].values
    idx = df.index

    for i in range(2, len(df)):
        ts = idx[i - 2]
        high_1 = high[i - 2]
        low_1 = low[i - 2]
        low_3 = low[i]
        high_3 = high[i]

        if low_3 > high_1:
            gap_size = low_3 - high_1
            if gap_size >= min_size:
                fvgs.append(Bisi(start=ts, low=high_1, high=low_3))

        elif high_3 < low_1:
            gap_size = low_1 - high_3
            if gap_size >= min_size:
                fvgs.append(Sibi(start=ts, low=high_3, high=low_1))

    print(f"Found {len(fvgs)} FVGs")
    return fvgs
