from datetime import time

import plotly.graph_objects as go

from engine.data.load import load, DateRangeConfig, TimeRangeConfig

# Load data
date = '2025-10-28'
date_range = DateRangeConfig(start_date=date, end_date=date)
time_range = TimeRangeConfig(start_time=time(9, 30), end_time=time(16, 0))
df = load(date_range=date_range, time_range=time_range)

# Create candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candlestick'
)])

# Update layout
fig.update_layout(
    xaxis_rangeslider_visible=False,
    template='plotly_dark',
    yaxis=dict(
        tickformat='.2f',
        showexponent='none'
    )
)

# Show the chart
fig.show()
