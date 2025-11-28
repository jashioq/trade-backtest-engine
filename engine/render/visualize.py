from datetime import time

import plotly.graph_objects as go

from engine.data.load import load, DateRangeConfig, TimeRangeConfig
from engine.detect.detectSwings import detect_swings
from engine.detect.detectFvgs import detect_fvgs


# Load data
date = '2025-10-28'
date_range = DateRangeConfig(start_date=date, end_date=date)
time_range = TimeRangeConfig(start_time=time(9, 30), end_time=time(16, 0))
df = load(date_range=date_range, time_range=time_range)

# Detect swing highs and lows
swing_length = 2
swings = detect_swings(df, swing_length=swing_length)

# Detect Fair Value Gaps
fvgs = detect_fvgs(df, join_consecutive=False)

swing_highs = [swing for swing in swings if swing.is_high]
swing_lows = [swing for swing in swings if not swing.is_high]

# Create candlestick chart
fig = go.Figure(data=[go.Candlestick(
    x=df.index,
    open=df['open'],
    high=df['high'],
    low=df['low'],
    close=df['close'],
    name='Candlestick'
)])

# Add swing highs
if swing_highs:
    fig.add_trace(go.Scatter(
        x=[swing.datetime for swing in swing_highs],
        y=[swing.level for swing in swing_highs],
        mode='markers',
        marker=dict(
            symbol='triangle-down',
            size=12,
            color = 'green',
            line = dict(width=2, color='darkgreen')
        ),
        name='Swing High',
        hovertemplate='Swing High<br>Time: %{x}<br>Level: %{y:.2f}<extra></extra>'
    ))

# Add swing lows
if swing_lows:
    fig.add_trace(go.Scatter(
        x=[swing.datetime for swing in swing_lows],
        y=[swing.level for swing in swing_lows],
        mode='markers',
        marker=dict(
            symbol='triangle-up',
            size=12,
            color='red',
            line=dict(width=2, color='darkred')
        ),
        name='Swing Low',
        hovertemplate='Swing Low<br>Time: %{x}<br>Level: %{y:.2f}<extra></extra>'
    ))

# Add FVG rectangles
for fvg in fvgs:
    try:
        fvg_pos = df.index.get_loc(fvg.datetime)
        end_pos = min(fvg_pos + 10, len(df.index) - 1)
        end_datetime = df.index[end_pos]
    except (KeyError, IndexError):
        continue
    
    # Choose color based on bullish/bearish
    color = 'green' if fvg.is_bullish else 'red'
    
    # Add rectangle shape
    fig.add_shape(
        type="rect",
        x0=fvg.datetime,
        y0=fvg.low,
        x1=end_datetime,
        y1=fvg.high,
        fillcolor=color,
        opacity=0.2,
        line=dict(width=0),
        layer="below",
        name=f"{'Bullish' if fvg.is_bullish else 'Bearish'} FVG"
    )

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
