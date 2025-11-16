# data/load.py
import pandas as pd
from pathlib import Path

"""
Loads candles from a CSV file located in the same directory as this module.
Filters data between first_timestamp and last_timestamp (inclusive).

CSV format: DD/MM/YYYY;HH:MM;Open;High;Low;Close;Volume  (semicolon-srepaated, no header)
"""
def load_candles(
        first_timestamp: pd.Timestamp,
        last_timestamp: pd.Timestamp,
        filename: str = "nq-1m_bk.csv"
) -> pd.DataFrame:
    csv_path = Path(__file__).parent / filename

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    df = pd.read_csv(
        csv_path,
        header=None,
        names=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume'],
        sep=';',
        dtype={'Open': float, 'High': float, 'Low': float, 'Close': float, 'Volume': int}
    )

    # Build proper datetime index
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M')
    df = df.set_index('Datetime')
    df = df.drop(columns=['Date', 'Time'])

    # Filter the requested time range
    mask = (df.index >= first_timestamp) & (df.index <= last_timestamp)
    filtered = df[mask].copy()

    if filtered.empty:
        print(f"Warning: No data found between {first_timestamp} and {last_timestamp}")
    else:
        print(
            f"Loaded {len(filtered)} bars from {first_timestamp.strftime('%Y-%m-%d %H:%M')} to {last_timestamp.strftime('%H:%M')}")

    return filtered