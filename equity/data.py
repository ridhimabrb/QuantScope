"""
Live and historical market data access, via yfinance.

Matches the role of Data/live_data.py in the original Trading-Analyst repo.
"""

import yfinance as yf
import pandas as pd


def fetch_live_data(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    df = yf.download(ticker, period=period, interval=interval, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.dropna()
    return df


def fetch_training_history(ticker: str, period: str = "5y", interval: str = "1d") -> pd.DataFrame:
    """Longer history used for model training (see train_model.py)."""
    return fetch_live_data(ticker, period=period, interval=interval)
