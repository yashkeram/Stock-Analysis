import pandas as pd
import numpy as np


def compute_daily_returns(price_df: pd.DataFrame) -> pd.Series:
    """
    Compute daily returns from price data.

    Parameters
    ----------
    price_df : pd.DataFrame
        DataFrame containing at least a 'Close' column

    Returns
    -------
    pd.Series
        Daily percentage returns
    """
    if "Close" not in price_df.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    returns = price_df["Close"].pct_change().dropna()
    return returns


def compute_volatility(returns: pd.Series, trading_days: int = 252) -> float:
    """
    Compute annualized volatility.

    Parameters
    ----------
    returns : pd.Series
        Daily returns
    trading_days : int
        Number of trading days per year

    Returns
    -------
    float
        Annualized volatility
    """
    return returns.std() * np.sqrt(trading_days)


def compute_max_drawdown(price_df: pd.DataFrame) -> float:
    """
    Compute maximum drawdown.

    Parameters
    ----------
    price_df : pd.DataFrame

    Returns
    -------
    float
        Maximum drawdown (negative number)
    """
    if "Close" not in price_df.columns:
        raise ValueError("DataFrame must contain 'Close' column")

    cumulative_max = price_df["Close"].cummax()
    drawdown = (price_df["Close"] - cumulative_max) / cumulative_max

    return drawdown.min()


def risk_summary(price_df: pd.DataFrame) -> dict:
    """
    Generate a summary of key risk metrics.

    Parameters
    ----------
    price_df : pd.DataFrame

    Returns
    -------
    dict
        Risk metrics summary
    """
    returns = compute_daily_returns(price_df)

    return {
        "volatility": compute_volatility(returns),
        "max_drawdown": compute_max_drawdown(price_df),
        "avg_daily_return": returns.mean(),
    }
