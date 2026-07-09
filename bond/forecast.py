"""
Loads the trained Random Forest yield forecaster and produces a 30-day
yield forecast from recent yield history.

--------------------------------------------------------------------------
TO PLUG IN YOUR REAL TRAINED MODEL:
1. Put your original models/ file (whatever .pkl / .joblib your bond
   repo's `models/` folder currently loads) at:
       bond/model.pkl
2. forecast_yield() below will use it automatically. If your original code
   builds different features, copy that feature logic into
   `build_yield_features()` below.
--------------------------------------------------------------------------
"""

import os
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def build_yield_features(yield_series: pd.Series) -> pd.DataFrame:
    df = pd.DataFrame({"Yield": yield_series})
    df["MA_5"] = df["Yield"].rolling(5).mean()
    df["MA_20"] = df["Yield"].rolling(20).mean()
    df["Volatility_10"] = df["Yield"].pct_change().rolling(10).std()
    return df


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def forecast_yield(yield_series: pd.Series, model=None) -> float:
    """Returns a single 30-day-ahead forecasted yield (%)."""
    if model is None:
        model = load_model()

    feats = build_yield_features(yield_series).dropna()
    latest = feats.iloc[-1:][["MA_5", "MA_20", "Volatility_10"]]

    if model is not None:
        return float(model.predict(latest.values)[0])

    # Cold-start fallback: simple mean-reversion toward the 20-day average.
    current = yield_series.iloc[-1]
    ma20 = feats["MA_20"].iloc[-1]
    return float(current + 0.3 * (ma20 - current))
