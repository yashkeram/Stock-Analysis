import yfinance as yf
import pandas as pd
from pathlib import Path


DATA_DIR = Path("data/raw")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def fetch_price_data(
    ticker: str,
    start: str = "2018-01-01",
    end: str | None = None,
    save: bool = True
) -> pd.DataFrame:
    """
    Fetch historical price data for a stock.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol (e.g., 'AAPL', 'RELIANCE.NS')
    start : str
        Start date (YYYY-MM-DD)
    end : str | None
        End date (YYYY-MM-DD)
    save : bool
        Whether to save raw data to disk

    Returns
    -------
    pd.DataFrame
        Historical OHLCV data
    """
    stock = yf.Ticker(ticker)
    df = stock.history(start=start, end=end)

    if df.empty:
        raise ValueError(f"No price data found for ticker: {ticker}")

    df.reset_index(inplace=True)

    if save:
        file_path = DATA_DIR / f"{ticker}_prices.csv"
        df.to_csv(file_path, index=False)

    return df


def fetch_fundamentals(ticker: str) -> dict:
    """
    Fetch key fundamental metrics for a stock.

    Parameters
    ----------
    ticker : str
        Stock ticker symbol

    Returns
    -------
    dict
        Dictionary of fundamental metrics
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    fundamentals = {
        "ticker": ticker,
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "pb_ratio": info.get("priceToBook"),
        "roe": info.get("returnOnEquity"),
        "revenue_growth": info.get("revenueGrowth"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
    }

    return fundamentals
