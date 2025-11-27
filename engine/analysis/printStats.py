def print_stats(strat):
    # Get the analysis dict from TradeAnalyzer
    analysis = strat.analyzers.tradeanalyzer.get_analysis()

    # Since mult=1 and commission=0, P&L values are directly in points

    # 1. Total points captured (total gross P&L)
    total_points = analysis['pnl']['gross']['total']
    print(f"1. Total points captured: {total_points:.2f}")

    # 2. Average win rate (percentage)
    total_trades = analysis['total']['closed']
    won_trades = analysis['won']['total']
    win_rate = (won_trades / total_trades * 100) if total_trades > 0 else 0
    print(f"2. Average win rate: {win_rate:.2f}%")

    # 3. Number of trades executed (closed trades)
    print(f"3. Number of trades executed: {total_trades}")

    # 4. Biggest loss in a single trade (most negative P&L, in points)
    biggest_loss_points = analysis['lost']['pnl']['max']  # This is the most negative value
    print(f"4. Biggest loss in a single trade: {biggest_loss_points:.2f} points")

    # 5. Biggest profit in a single trade (max positive P&L, in points)
    biggest_profit_points = analysis['won']['pnl']['max']
    print(f"5. Biggest profit in a single trade: {biggest_profit_points:.2f} points")

    # 6. Longest winning trade that was open (in bars)
    longest_win_bars = analysis['len']['won']['max']
    print(f"6. Longest winning trade: {longest_win_bars} bars")

    # 6. Longest losing trade that was open (in bars)
    longest_lose_bars = analysis['len']['lost']['max']
    print(f"7. Longest losing trade: {longest_lose_bars} bars")

    # 8. Average trade length for losing trades (in bars)
    avg_lose_bars = analysis['len']['lost']['average']
    print(f"8. Average trade length for losing trades: {avg_lose_bars:.2f} bars")

    # 9. Average trade length for winning trades (in bars)
    avg_win_bars = analysis['len']['won']['average']
    print(f"9. Average trade length for winning trades: {avg_win_bars:.2f} bars")
