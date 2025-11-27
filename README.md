## This is a trade backtesting engine that I am developing.
Based on [Backtrader](https://www.backtrader.com/) project.
Supports backtesting event driven strategies on a set of historical OHLC data.
Backtests can be performed on selected date range and in selected trading session.
Includes detailed performance analysis with data plotting capabilites coming soon.
Can render an interactive candlestick chart for a selected date and time range.
Rendering is based on [Plotly](https://plotly.com/python/) project.
Rendering feature is intended for manual inspection and tuning of strategy trade signal detection conditions.
<br /> 
### Example render:
<img width="1904" height="903" alt="newplot(1)" src="https://github.com/user-attachments/assets/3f2b392a-145a-4f10-97f9-931991e5a746" />

### Example performance analysis stats (with a demo strategy to test the engine):
> Backtest complete.
> 1. Total points captured: 299.97
> 2. Average win rate: 45.51%
> 3. Number of trades executed: 167
> 4. Biggest loss in a single trade: -129.18 points
> 5. Biggest profit in a single trade: 340.63 points
> 6. Longest winning trade: 151 bars
> 7. Longest losing trade: 149 bars
> 8. Average trade length for losing trades: 47.97 bars
> 9. Average trade length for winning trades: 44.72 bars
