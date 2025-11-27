from datetime import time

import backtrader as bt

from engine.analysis.printStats import print_stats
from engine.data.load import DateRangeConfig, TimeRangeConfig, load

from engine.strategy.SmaStrategy import SmaStrategy

# ===== CONFIG =====
# Load filtered NQ data (NY session: 9:30-16:00 ET)
date_range = DateRangeConfig(start_date='2024-01-01', end_date='2024-12-30')
time_range = TimeRangeConfig(start_time=time(9,30), end_time=time(16,0))
exclude_event_days = True
# Set strategy
strategy = SmaStrategy
# ===== CONFIG =====

# Load data
df = load(date_range=date_range, time_range=time_range, exclude_event_days=exclude_event_days)

# Create Cerebro engine
cerebro = bt.Cerebro()

# Load strategy
cerebro.addstrategy(strategy)

# Add data feed from Pandas DataFrame
data = bt.feeds.PandasData(dataname=df)
cerebro.adddata(data)

# Set broker parameters
cerebro.broker.setcash(1000000)

# Analyzers for performance metrics
cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer')

# Run the backtest
results = cerebro.run()
print("Backtest complete.")

# Optional: Print some results
strat = results[0]
print_stats(strat)
