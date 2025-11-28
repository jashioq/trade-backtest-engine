from dataclasses import dataclass
from typing import List
from datetime import datetime
from smartmoneyconcepts import smc
import pandas as pd


@dataclass
class FairValueGap:
    """
    Data model for Fair Value Gap (FVG).
    
    Attributes:
        datetime: The datetime when the FVG occurred (the middle candle)
        high: The upper price level of the FVG
        low: The lower price level of the FVG
        is_bullish: True if bullish FVG, False if bearish FVG
    """
    datetime: datetime
    high: float
    low: float
    is_bullish: bool


def detect_fvgs(df: pd.DataFrame, join_consecutive: bool = False) -> List[FairValueGap]:
    """
    Detect Fair Value Gaps.
    
    A fair value gap is when the previous high is lower than the next low if the current candle is bullish.
    Or when the previous low is higher than the next high if the current candle is bearish.
    
    Args:
        df: DataFrame with OHLCV data, indexed by datetime.
            Expected columns: 'open', 'high', 'low', 'close'
        join_consecutive: If True, merge consecutive FVGs into one using highest top and lowest bottom.
    
    Returns:
        List of FairValueGap objects, sorted by datetime.
    """
    # Validate input
    required_columns = ['open', 'high', 'low', 'close']
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"DataFrame missing required columns: {missing_columns}")
    
    df_work = df[required_columns].copy()
    
    # Detect Fair Value Gaps
    fvg_data = smc.fvg(df_work, join_consecutive=join_consecutive)
    
    fvgs = []
    
    # Extract valid FVG points
    valid_mask = (fvg_data['FVG'].notna()) & (fvg_data['Top'].notna()) & (fvg_data['Bottom'].notna())
    valid_fvgs = fvg_data[valid_mask]
    
    # Map integer indices back to original datetime index
    for idx in valid_fvgs.index:
        fvg = valid_fvgs.loc[idx, 'FVG']
        top = valid_fvgs.loc[idx, 'Top']
        bottom = valid_fvgs.loc[idx, 'Bottom']
        
        # Get datetime from original index by position
        datetime_val = df_work.index[idx].to_pydatetime()
        
        is_bullish = fvg == 1
        fvgs.append(FairValueGap(
            datetime=datetime_val,
            high=float(top),
            low=float(bottom),
            is_bullish=bool(is_bullish)
        ))
    
    fvgs.sort(key=lambda x: x.datetime)
    
    return fvgs
