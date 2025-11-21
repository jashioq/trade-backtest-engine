from typing import List
import pandas as pd
from app.detect.model.swing import Swing, BullishSwing, BearishSwing

def detect_swings(
        df: pd.DataFrame,
        min_length: int = 3,
        min_size_points: float = 0.0
) -> List[Swing]:
    """
    Detects price swings and their OTE levels.

    Rules:
    - Bullish: consecutive bullish candles
      - High = max of closes, Low = min of opens
    - Bearish: consecutive bearish candles
      - High = max of opens, Low = min of closes
    - Extensions: swing boundaries extend to capture volume imbalances from adjacent candles
    - OTE levels: 62% and 79% retracement range

    Parameters:
    df : pd.DataFrame - OHLC data with datetime index
    min_length : int - Minimum consecutive candles
    min_size_points : float - Minimum swing range in points
    """
    if len(df) < min_length:
        return []

    swings: List[Swing] = []
    close = df['Close'].values
    open_ = df['Open'].values
    idx = df.index

    i = 0
    while i < len(df):
        # Bullish
        if close[i] > open_[i]:
            start_idx = i
            current = i

            while current + 1 < len(df) and close[current + 1] > open_[current + 1]:
                current += 1

            end_idx = current
            length = end_idx - start_idx + 1

            if length >= min_length:
                # For bullish candles: body high = close, body low = open
                segment_highs = close[start_idx:end_idx + 1]
                segment_lows = open_[start_idx:end_idx + 1]

                swing_high = segment_highs.max()
                swing_low = segment_lows.min()

                # Check candle before the swing
                if start_idx > 0 and close[start_idx - 1] < open_[start_idx]:
                    swing_low = min(swing_low, close[start_idx - 1])

                # Check candle after the swing
                if end_idx + 1 < len(df) and open_[end_idx + 1] > close[end_idx]:
                    swing_high = max(swing_high, open_[end_idx + 1])

                # Calculate OTE levels for bullish swing
                # Retracement from high: 62% and 79%
                swing_range = swing_high - swing_low
                ote_top = swing_high - (swing_range * 0.62)
                ote_bottom = swing_high - (swing_range * 0.79)

                if swing_high - swing_low >= min_size_points:
                    swings.append(BullishSwing(
                        start=idx[start_idx],
                        end=idx[end_idx],
                        high=swing_high,
                        low=swing_low,
                        ote_top=ote_top,
                        ote_bottom=ote_bottom
                    ))

            i = end_idx + 1
            continue

        # Bearish
        elif close[i] < open_[i]:
            start_idx = i
            current = i

            while current + 1 < len(df) and close[current + 1] < open_[current + 1]:
                current += 1

            end_idx = current
            length = end_idx - start_idx + 1

            if length >= min_length:
                # For bearish candles: body high = open, body low = close
                segment_highs = open_[start_idx:end_idx + 1]
                segment_lows = close[start_idx:end_idx + 1]

                swing_high = segment_highs.max()
                swing_low = segment_lows.min()

                # Check candle before the swing
                if start_idx > 0 and close[start_idx - 1] > open_[start_idx]:
                    swing_high = max(swing_high, close[start_idx - 1])

                # Check candle after the swing
                if end_idx + 1 < len(df) and open_[end_idx + 1] < close[end_idx]:
                    swing_low = min(swing_low, open_[end_idx + 1])

                # Calculate OTE levels for bearish swing
                # Retracement from low: 62% and 79%
                swing_range = swing_high - swing_low
                ote_bottom = swing_low + (swing_range * 0.62)
                ote_top = swing_low + (swing_range * 0.79)

                if swing_high - swing_low >= min_size_points:
                    swings.append(BearishSwing(
                        start=idx[start_idx],
                        end=idx[end_idx],
                        high=swing_high,
                        low=swing_low,
                        ote_top=ote_top,
                        ote_bottom=ote_bottom
                    ))

            i = end_idx + 1
            continue

        # Doji or neutral candle - skip it
        i += 1

    print(f"Found {len(swings)} swings")
    return swings
