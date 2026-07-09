"""
Trains the Random Forest yield forecaster on historical G-Sec yield data
and saves it to bond/model.pkl.

Run once locally before deploying:

    python -m bond.train_model --csv data/gsec_yields.csv

Expects a CSV with at least a 'Date' and 'Price' (yield) column, matching
the "Historical Indian 10-Year Government Security Yield Data" described
in the ML-Powered-Bond-Yield-Forecaster README (Price, Open, High, Low,
Change %, 2016-2026).
"""

import argparse
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

from .forecast import build_yield_features, MODEL_PATH


def train(csv_path: str, horizon_days: int = 30):
    df = pd.read_csv(csv_path, parse_dates=["Date"]).sort_values("Date")
    yields = df["Price"]

    feats = build_yield_features(yields)
    feats["Target"] = yields.shift(-horizon_days)
    feats = feats.dropna()

    X = feats[["MA_5", "MA_20", "Volatility_10"]]
    y = feats["Target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestRegressor(n_estimators=300, max_depth=6, random_state=42)
    model.fit(X_train, y_train)

    r2 = model.score(X_test, y_test)
    print(f"Hold-out R^2: {r2:.3f}")

    joblib.dump(model, MODEL_PATH)
    print(f"Saved trained model to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to historical yield CSV")
    parser.add_argument("--horizon", type=int, default=30)
    args = parser.parse_args()
    train(args.csv, args.horizon)
