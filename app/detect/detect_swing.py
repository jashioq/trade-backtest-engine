from typing import List
import pandas as pd
from app.detect.model.swing import Swing, BullishSwing, BearishSwing

def detect_swing(
    df: pd.DataFrame,
    min_length: int = 3,
    min_size_points: float = 0.0
) -> List[Swing]:

    if len(df) < min_length:
        return []

    swings: List[Swing] = []
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
                swings.append(BullishSwing(
                    start=idx[start_idx],
                    end=idx[end_idx],
                    high=swing_high,
                    low=swing_low
                ))

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
                swings.append(BearishSwing(
                    start=idx[start_idx],
                    end=idx[end_idx],
                    high=swing_high,
                    low=swing_low
                ))

            i = end_idx + 1
            continue

        i += 1

    print(f"Found {len(swings)} swings")
    return swings
