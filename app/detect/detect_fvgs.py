from typing import List
import pandas as pd

from app.detect.model.fvg import Fvg, Bisi, Sibi

def detect_fvgs(df: pd.DataFrame, min_size: float = 0.0) -> List[Fvg]:
    """
    Detects Fair Value Gaps in OHLC price data.

    Rules:
    - Bullish FVG: candle 3 low > candle 1 high
    - Bearish FVG: candle 3 high < candle 1 low
    - Extends to include volume imbalances between candle bodies:
      - If candle 1 close gaps from candle 2 open, include that gap
      - If candle 3 open gaps from candle 2 close, include that gap

    Parameters:
    df : pd.DataFrame - OHLC data with datetime index
    min_size : float - Minimum gap size in points
    """
    if len(df) < 3:
        return []

    fvgs: List[Fvg] = []
    high = df['High'].values
    low = df['Low'].values
    close = df['Close'].values
    open_ = df['Open'].values
    idx = df.index

    for i in range(2, len(df)):
        ts = idx[i - 2]

        # Candle 1 (i-2)
        high_1 = high[i - 2]
        low_1 = low[i - 2]
        close_1 = close[i - 2]

        # Candle 2 (i-1)
        open_2 = open_[i - 1]
        close_2 = close[i - 1]

        # Candle 3 (i)
        low_3 = low[i]
        high_3 = high[i]
        open_3 = open_[i]

        # Bullish
        if low_3 > high_1:
            fvg_low = high_1
            fvg_high = low_3

            # Check for volume imbalance at the bottom
            if close_1 < open_2:
                fvg_low = close_1

            # Check for volume imbalance at the top
            if open_3 > close_2:
                fvg_high = open_3

            gap_size = fvg_high - fvg_low
            if gap_size >= min_size:
                fvgs.append(Bisi(start=ts, low=fvg_low, high=fvg_high))

        # Bearish
        elif high_3 < low_1:
            fvg_high = low_1
            fvg_low = high_3

            # Check for volume imbalance at the top
            if close_1 > open_2:
                fvg_high = close_1

            # Check for volume imbalance at the bottom
            if open_3 < close_2:
                fvg_low = open_3

            gap_size = fvg_high - fvg_low
            if gap_size >= min_size:
                fvgs.append(Sibi(start=ts, low=fvg_low, high=fvg_high))

    print(f"Found {len(fvgs)} FVGs")
    return fvgs
