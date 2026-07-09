# QuantScope

Market direction analyst + fixed income (bond) valuation and yield forecasting, combined into one dashboard.

By **Ridhima Pant**. Originally two separate projects:
- [Trading-Analyst](https://github.com/ridhimabrb/Trading-Analyst) -- ML market direction classifier
- [ML-Powered-Bond-Yield-Forecaster](https://github.com/ridhimabrb/ML-Powered-Bond-Yield-Forecaster) -- DCF bond valuation + yield forecasting

## What it does

**Market Direction Analyst** -- fetches live OHLCV data (Yahoo Finance), builds technical
features (RSI, moving averages, rolling volatility), runs a Logistic Regression classifier,
and turns the probability into a LONG / SHORT / NO TRADE call with a plain-language explanation.

**Bond Yield Lab** -- prices a bond via discounted cash flow (DCF), computes Macaulay and
modified duration, lets you shock the yield curve and see the repriced value instantly, and
forecasts 30-day G-Sec yield moves with a Random Forest model trained on historical yield data.
