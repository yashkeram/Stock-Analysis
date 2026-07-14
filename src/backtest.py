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
    signals.loc[signals["ma_short"] > signals["ma_long"], "signal"] = 1
    signals["position"] = signals["signal"].diff()
    return signals


def _cagr(cumulative_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Compute Compound Annual Growth Rate (CAGR).
    """
    total_periods = cumulative_returns.dropna().shape[0]
    if total_periods == 0:
        return np.nan

    total_return = cumulative_returns.iloc[-1]
    years = total_periods / trading_days
    return total_return ** (1 / years) - 1


def _sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = 252,
) -> float:
    """
    Compute annualized Sharpe Ratio.
    """
    excess_returns = returns - (risk_free_rate / trading_days)
    if excess_returns.std() == 0:
        return np.nan
    return np.sqrt(trading_days) * excess_returns.mean() / excess_returns.std()


def backtest_strategy(price_df: pd.DataFrame) -> dict:
    """
    Backtest moving average crossover strategy and compute
    performance & risk-adjusted metrics.
    """
    df = add_moving_averages(price_df)
    signals = generate_signals(df)

    signals["daily_return"] = signals["Close"].pct_change()
    signals["strategy_return"] = (
        signals["daily_return"] * signals["signal"].shift(1)
    )

    cumulative_market = (1 + signals["daily_return"]).cumprod()
    cumulative_strategy = (1 + signals["strategy_return"]).cumprod()

    market_cagr = _cagr(cumulative_market)
    strategy_cagr = _cagr(cumulative_strategy)

    market_sharpe = _sharpe_ratio(signals["daily_return"].dropna())
    strategy_sharpe = _sharpe_ratio(signals["strategy_return"].dropna())

    return {
        "market_total_return": cumulative_market.iloc[-1] - 1,
        "strategy_total_return": cumulative_strategy.iloc[-1] - 1,
        "market_cagr": market_cagr,
        "strategy_cagr": strategy_cagr,
        "market_sharpe": market_sharpe,
        "strategy_sharpe": strategy_sharpe,
        "outperformance_cagr": strategy_cagr - market_cagr,
    }