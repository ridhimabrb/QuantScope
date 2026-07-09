"""
Trains the Logistic Regression market-direction classifier on real
historical data and saves it to equity/model.pkl.

Run once locally (or in a notebook) before deploying:

    python -m equity.train_model --ticker ^GSPC

This mirrors the "time-aware train-test split, no shuffling" approach
described in the original Trading-Analyst README.
"""

import argparse
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from .data import fetch_training_history
from .features import build_features, FEATURE_COLUMNS
from .model import MODEL_PATH


def train(ticker: str = "^GSPC", period: str = "5y"):
    df = fetch_training_history(ticker, period=period)
    feats = build_features(df)

    # Label: did price go up the next session?
    feats["Target"] = (feats["Close"].shift(-1) > feats["Close"]).astype(int)
    feats = feats.dropna(subset=FEATURE_COLUMNS + ["Target"])

    X = feats[FEATURE_COLUMNS]
    y = feats["Target"]

    # Time-aware split -- no shuffling, train on the past, test on the future.
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Hold-out directional accuracy on {ticker}: {accuracy*100:.2f}%")

    joblib.dump(model, MODEL_PATH)
    print(f"Saved trained model to {MODEL_PATH}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticker", default="^GSPC")
    parser.add_argument("--period", default="5y")
    args = parser.parse_args()
    train(args.ticker, args.period)
