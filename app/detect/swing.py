from typing import List, Tuple
import pandas as pd

def detect_price_swings(
    df: pd.DataFrame,
    min_length: int = 3,
    min_size_points: float = 0.0
) -> List[Tuple[pd.Timestamp, pd.Timestamp, str, float, float]]:
    if len(df) < min_length:
        return []

    swings = []
    high = df['High'].values
    low = df['Low'].values
    idx = df.index

    i = 1
    while i < len(df):
        if low[i] > low[i - 1]:
            start_idx = i - 1
            current = i

            while current + 1 < len(df) and low[current + 1] >= low[current]:
                current += 1

            end_idx = current

            length = end_idx - start_idx + 1
            swing_high = high[start_idx:end_idx + 1].max()
            swing_low = low[start_idx:end_idx + 1].min()
            move_size = swing_high - swing_low

            if length >= min_length and move_size >= min_size_points:
                swings.append((idx[start_idx], idx[end_idx], "bullish", swing_high, swing_low))

            i = end_idx + 1
            continue

        elif high[i] < high[i - 1]:
            start_idx = i - 1
            current = i

            while current + 1 < len(df) and high[current + 1] <= high[current]:
                current += 1

            end_idx = current

            length = end_idx - start_idx + 1
            swing_high = high[start_idx:end_idx + 1].max()
            swing_low = low[start_idx:end_idx + 1].min()
            move_size = swing_high - swing_low

            if length >= min_length and move_size >= min_size_points:
                swings.append((idx[start_idx], idx[end_idx], "bearish", swing_high, swing_low))

            i = end_idx + 1
            continue

        i += 1

    return swings
