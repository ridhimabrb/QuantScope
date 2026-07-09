"""
Feature engineering for the Market Direction Analyst.

If you already have Features/live_features.py in Trading-Analyst, you can
drop that file's contents in here instead -- this is a clean re-implementation
of the same feature set described in that repo's README (RSI, short/long
moving averages, rolling volatility, daily returns).
"""

import pandas as pd
import numpy as np


def compute_rsi(close: pd.Series, window: int = 14) -> pd.Series:
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window).mean()
    avg_loss = loss.rolling(window).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi.fillna(50)


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Expects df with a 'Close' column (and ideally 'Volume').
    Returns df with added feature columns. Row 0..window-1 will have NaNs
    from rolling windows -- drop them before training/inference.
    """
    out = df.copy()
    out["Return"] = out["Close"].pct_change()
    out["MA_5"] = out["Close"].rolling(5).mean()
    out["MA_20"] = out["Close"].rolling(20).mean()
    out["Volatility_10"] = out["Return"].rolling(10).std()
    out["RSI_14"] = compute_rsi(out["Close"], 14)
    return out


def build_live_features(df: pd.DataFrame) -> pd.DataFrame:
    """Alias matching the original Trading-Analyst import name."""
    return build_features(df)


FEATURE_COLUMNS = ["MA_5", "MA_20", "Volatility_10", "RSI_14"]
