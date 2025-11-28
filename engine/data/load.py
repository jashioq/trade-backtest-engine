import pandas as pd
import pytz
from dataclasses import dataclass
from typing import Optional
from datetime import time
from pathlib import Path


@dataclass
class DateRangeConfig:
    """Configuration for date range filtering."""
    start_date: Optional[str] = None  # Start date (YYYY-MM-DD) or None for no lower bound
    end_date: Optional[str] = None    # End date (YYYY-MM-DD) or None for no upper bound


@dataclass
class TimeRangeConfig:
    """Configuration for daily time range filtering."""
    start_time: time = time(9, 30)   # Start time (e.g., time(9, 30) for 9:30)
    end_time: time = time(16, 0)     # End time (e.g., time(16, 0) for 16:00)


def _load_event_dates() -> set:
    """
    Load high impact event dates.
    
    Returns:
        Set of date strings in format 'YYYY-MM-DD'
    """
    event_filepath = Path(__file__).parent.parent / 'res' / 'event_dates.csv'
    event_dates = set()
    
    with open(event_filepath, 'r') as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith('#'):
                continue

            try:
                parts = line.split('/')
                if len(parts) == 3:
                    day, month, year = parts
                    formatted_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
                    event_dates.add(formatted_date)
            except (ValueError, IndexError):
                continue
    
    return event_dates

def load(
    date_range: Optional[DateRangeConfig] = None,
    time_range: Optional[TimeRangeConfig] = None,
    exclude_event_days: bool = False,
) -> pd.DataFrame:
    """
    Load and prepare data for backtesting.

    Args:
        date_range: Optional DateRangeConfig for filtering dates.
        time_range: Optional TimeRangeConfig for filtering daily time range.
        exclude_event_days: If True, exclude high impact event days (FOMC, NFP, etc.).

    Returns:
        Filtered DataFrame with OHLCV data, indexed by datetime in NY timezone.
    """
    print("Loading data...")

    filepath = Path(__file__).parent.parent / 'res' / 'nq_data.csv'

    # Load data
    df = pd.read_csv(
        filepath,
        sep=';',
        header=None,
        names=['date', 'time', 'open', 'high', 'low', 'close', 'volume']
    )

    # Combine date and time into datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%Y %H:%M')

    # Convert from Chicago time to NY time
    chicago_tz = pytz.timezone('America/Chicago')
    ny_tz = pytz.timezone('America/New_York')
    df['datetime'] = df['datetime'].dt.tz_localize(chicago_tz).dt.tz_convert(ny_tz)

    # Set index and select/convert columns
    df.set_index('datetime', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']].astype(float)

    # Sort by index (datetime)
    df = df.sort_index()

    print(f"Full data loaded: {len(df)} rows")

    # Exclude event days
    if exclude_event_days:
        event_dates = _load_event_dates()
        date_strings = df.index.strftime('%Y-%m-%d')
        # Filter out rows where date matches event dates
        mask = pd.Series(date_strings, index=df.index).isin(event_dates)
        df = df[~mask].copy()
        print(f"After excluding event days: {len(df)} rows")

    # Apply time range filter if specified
    if time_range:
        session_mask = (df.index.time >= time_range.start_time) & (df.index.time <= time_range.end_time)
        df = df[session_mask].copy()

    # Apply date range filter if specified
    if date_range and (date_range.start_date or date_range.end_date):
        tz = df.index.tz  # NY timezone
        start_date_obj = (
            pd.to_datetime(date_range.start_date).tz_localize(tz)
            if date_range.start_date else df.index.min()
        )
        end_date_obj = (
            (pd.to_datetime(date_range.end_date).tz_localize(tz) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1))
            if date_range.end_date else df.index.max()
        )

        df = df[(df.index >= start_date_obj) & (df.index <= end_date_obj)].copy()

        print(f"After date and time range filters: {len(df)} rows")

    return df
