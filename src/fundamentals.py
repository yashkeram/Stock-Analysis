import pandas as pd


def compute_valuation_metrics(fundamentals: dict) -> dict:
    """
    Compute valuation-related metrics from raw fundamentals.

    Parameters
    ----------
    fundamentals : dict
        Output from fetch_fundamentals()

    Returns
    -------
    dict
        Valuation metrics
    """
    pe = fundamentals.get("pe_ratio")
    pb = fundamentals.get("pb_ratio")

    valuation = {
        "ticker": fundamentals.get("ticker"),
        "pe_ratio": pe,
        "pb_ratio": pb,
        "valuation_flag": _valuation_flag(pe, pb),
    }

    return valuation


def compute_profitability_metrics(fundamentals: dict) -> dict:
    """
    Compute profitability-related metrics.

    Parameters
    ----------
    fundamentals : dict

    Returns
    -------
    dict
        Profitability metrics
    """
    roe = fundamentals.get("roe")

    profitability = {
        "ticker": fundamentals.get("ticker"),
        "roe": roe,
        "roe_quality": _roe_quality(roe),
    }

    return profitability


def compute_growth_metrics(fundamentals: dict) -> dict:
    """
    Compute growth-related metrics.

    Parameters
    ----------
    fundamentals : dict

    Returns
    -------
    dict
        Growth metrics
    """
    growth = fundamentals.get("revenue_growth")

    growth_metrics = {
        "ticker": fundamentals.get("ticker"),
        "revenue_growth": growth,
        "growth_flag": _growth_flag(growth),
    }

    return growth_metrics


def _valuation_flag(pe, pb):
    if pe is None or pb is None:
        return "insufficient_data"
    if pe < 15 and pb < 3:
        return "undervalued"
    if pe > 30:
        return "overvalued"
    return "fairly_valued"


def _roe_quality(roe):
    if roe is None:
        return "insufficient_data"
    if roe > 0.20:
        return "excellent"
    if roe > 0.12:
        return "good"
    return "weak"


def _growth_flag(growth):
    if growth is None:
        return "insufficient_data"
    if growth > 0.15:
        return "high_growth"
    if growth > 0.05:
        return "moderate_growth"
    return "low_growth"
