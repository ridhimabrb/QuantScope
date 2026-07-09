"""
Loads the trained classifier and turns its output into a LONG / SHORT /
NO TRADE decision with a plain-language explanation.

Matches the role of Models/ai_agent.py in the original Trading-Analyst repo.

--------------------------------------------------------------------------
TO PLUG IN YOUR REAL TRAINED MODEL:
1. Put your original Models/ai_agent.py's trained model file (the .pkl /
   .joblib your `Models/ai_agent.py` currently loads) at:
       equity/model.pkl
2. That's it -- load_model() below will pick it up automatically. If your
   original ai_agent.py has custom pre/post-processing around the raw
   sklearn prediction, copy that logic into `ai_trade_decision()` below,
   replacing the block marked "DEFAULT LOGIC".
--------------------------------------------------------------------------
"""

import os
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from .features import FEATURE_COLUMNS

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None  # falls back to train_model.train_quick_model() at call time


def ai_trade_decision(latest_features: pd.DataFrame, model=None) -> dict:
    """
    latest_features: single-row DataFrame containing FEATURE_COLUMNS.
    Returns dict with decision, prob_up, prob_down, explanation.
    """
    if model is None:
        model = load_model()

    X = latest_features[FEATURE_COLUMNS].values

    if model is not None:
        # ---- DEFAULT LOGIC: replace with your original ai_agent.py logic ----
        prob_up = float(model.predict_proba(X)[0][1])
    else:
        # Cold-start fallback so the app runs before any model.pkl exists.
        rsi = latest_features["RSI_14"].values[0]
        ma5 = latest_features["MA_5"].values[0]
        ma20 = latest_features["MA_20"].values[0]
        score = 0.5 + 0.15 * np.tanh((ma5 - ma20) / max(ma20, 1e-6) * 20) + 0.1 * np.tanh((50 - rsi) / 50)
        prob_up = float(np.clip(score, 0.05, 0.95))

    prob_down = 1 - prob_up

    if prob_up > 0.56:
        decision = "LONG"
        explanation = (
            f"Model assigns a {prob_up*100:.1f}% probability to an upward move, "
            "driven by short-term momentum outweighing longer-term trend. Bias: bullish."
        )
    elif prob_up < 0.44:
        decision = "SHORT"
        explanation = (
            f"Model assigns a {prob_down*100:.1f}% probability to a downward move, "
            "with momentum and RSI both pointing to weakening price action. Bias: bearish."
        )
    else:
        decision = "NO TRADE"
        explanation = (
            f"Probability is split ({prob_up*100:.1f}% up / {prob_down*100:.1f}% down) -- "
            "no clear directional edge, so the agent stays flat."
        )

    return {
        "decision": decision,
        "prob_up": prob_up,
        "prob_down": prob_down,
        "explanation": explanation,
    }
