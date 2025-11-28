from dataclasses import dataclass
from typing import List
from datetime import datetime
from smartmoneyconcepts import smc
import pandas as pd


@dataclass
class SwingHighLow:
    """
    Data model for swing high or low points.
    
    Attributes:
        datetime: The datetime when the swing occurred
        level: The price level of the swing (top of body for swing high, bottom of body for swing low)
        is_high: True if this is a swing high, False if swing low
    """
    datetime: datetime
    level: float
    is_high: bool


def detect_swings(df: pd.DataFrame, swing_length: int) -> List[SwingHighLow]:
    """
    Detect swing highs and lows using candle bodies only.

    Args:
        df: DataFrame with OHLCV data, indexed by datetime.
            Expected columns: 'open', 'high', 'low', 'close'
        swing_length: Number of candles to look back and forward to determine swings.

    Returns:
        List of SwingHighLow objects, sorted by datetime.
    """
    # Validate input
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame missing required columns: {missing_columns}")

    df_work = df[required_columns].copy()
    
    # Calculate body high and body low
    df_work['body_high'] = df_work[['open', 'close']].max(axis=1)
    df_work['body_low'] = df_work[['open', 'close']].min(axis=1)
    
    # Replace high/low with body high/low
    df_work['high'] = df_work['body_high']
    df_work['low'] = df_work['body_low']
    
    # Detect swing highs and lows
    swing_data = smc.swing_highs_lows(df_work, swing_length=swing_length)

    swings = []
    
    # Extract valid swing points
    valid_mask = (swing_data['HighLow'].notna()) & (swing_data['Level'].notna())
    valid_swings = swing_data[valid_mask]
    
    # Filter out boundary swings where there isn't enough lookback/lookforward data
    # A swing needs at least swing_length candles before and after it
    boundary_mask = (valid_swings.index >= swing_length) & (valid_swings.index < len(df_work.index) - swing_length)
    valid_swings = valid_swings[boundary_mask]
    
    # Map integer indices back to original datetime index
    for idx in valid_swings.index:
        high_low = valid_swings.loc[idx, 'HighLow']
        level = valid_swings.loc[idx, 'Level']
        
        # Get datetime from original index by position
        datetime_val = df_work.index[idx].to_pydatetime()
        
        is_high = high_low == 1
        swings.append(SwingHighLow(
            datetime=datetime_val,
            level=float(level),
            is_high=bool(is_high)
        ))

    swings.sort(key=lambda x: x.datetime)
    
    return swings
