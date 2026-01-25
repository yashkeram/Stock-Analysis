import pandas as pd
import numpy as np


def add_moving_averages(
    price_df: pd.DataFrame,
    short_window: int = 50,
    long_window: int = 200,
) -> pd.DataFrame:
    """
    Add moving average columns to price data.
    """
    df = price_df.copy()

    df["ma_short"] = df["Close"].rolling(window=short_window).mean()
    df["ma_long"] = df["Close"].rolling(window=long_window).mean()

    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate trading signals based on moving average crossover.
    """
    signals = df.copy()
    signals["signal"] = 0

    signals.loc[
        signals["ma_short"] > signals["ma_long"], "signal"
    ] = 1

    signals["position"] = signals["signal"].diff()

    return signals


def backtest_strategy(price_df: pd.DataFrame) -> dict:
    """
    Backtest moving average crossover strategy.

    Returns
    -------
    dict
        Performance metrics
    """
    df = add_moving_averages(price_df)
    signals = generate_signals(df)

    signals["daily_return"] = signals["Close"].pct_change()
    signals["strategy_return"] = (
        signals["daily_return"] * signals["signal"].shift(1)
    )

    cumulative_market = (1 + signals["daily_return"]).cumprod()
    cumulative_strategy = (1 + signals["strategy_return"]).cumprod()

    total_market_return = cumulative_market.iloc[-1] - 1
    total_strategy_return = cumulative_strategy.iloc[-1] - 1

    return {
        "market_return": total_market_return,
        "strategy_return": total_strategy_return,
        "outperformance": total_strategy_return - total_market_return,
    }
