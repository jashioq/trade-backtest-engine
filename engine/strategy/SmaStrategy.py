import backtrader as bt


class SmaStrategy(bt.Strategy):
    params = (
        ('fast_period', 50),  # Fast MA period
        ('slow_period', 200),  # Slow MA period
    )

    def __init__(self):
        self.fast_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.fast_period)
        self.slow_ma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.slow_period)
        self.crossover = bt.indicators.CrossOver(self.fast_ma, self.slow_ma)

    def next(self):
        # Get current datetime (in NY timezone, as per data)
        current_time = self.data.datetime.time()

        # Close position if near end of session (e.g., after 15:59)
        if self.position and current_time.hour >= 15 and current_time.minute >= 59:
            self.close()
            return  # Exit early after closing

        # Only trade if no position open
        if not self.position:
            if self.crossover > 0:  # Fast MA crosses above slow MA: Buy (long)
                self.buy()
            elif self.crossover < 0:  # Fast MA crosses below slow MA: Sell (short)
                self.sell()