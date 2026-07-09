"""
QuantScope -- combined entry point.

Merges the two original Streamlit apps (equity market direction +
fixed-income DCF/yield forecasting) into one navigable dashboard.

Run locally:
    streamlit run app.py

Deploy: push this repo to GitHub, then deploy on Streamlit Community Cloud
pointing at app.py. (GitHub Pages cannot run this -- see README.)
"""

import streamlit as st
import pandas as pd

from equity.data import fetch_live_data
from equity.features import build_live_features, FEATURE_COLUMNS
from equity.model import ai_trade_decision
from bond.dcf import price_bond, reprice_under_shock
from bond.forecast import forecast_yield

from styles import load_css

load_css()

st.set_page_config(page_title="QuantScope", page_icon="📊", layout="wide")


st.markdown(
    "<h1 style='text-align:center;'>Quant<span style='color:#C6A15B;'>Scope</span></h1>"
    "<h4 style='text-align:center; color:#8C93A6;'>Quantitative Market Intelligence Platform <br><br>" 
    "Real-time Equity Signals • Fixed Income Analytics • ML Forecasting </h4>",
    
    unsafe_allow_html=True,
)
st.divider()
with st.sidebar:

    st.markdown("""
### About

**QuantScope**

AI-powered quantitative finance dashboard combining

- Equity Intelligence

- Fixed Income Analytics
                
Created by

**Ridhima Pant**

---


#### Tech Stack

Python

Streamlit

Scikit-learn

Plotly

Pandas

Yahoo Finance

Random Forest

Logistic Regression

""")

col1, col2 = st.columns(2)

with col1:

    st.markdown("""
    <div style="
    background:#708B75;
    padding:25px;
    border-radius:22px;
    color:black;
    min-height:320px;
    ">

    <h2 style="color:black;">Equity Intelligence</h2>

    On entering a ticker, Logistic Regression classifier predicts short-term UP/DOWN
            probability from technical indicators on live OHLCV data, and returns a LONG / SHORT / NO TRADE call. 

    <br>
                
    ✓ Live Yahoo Finance

    ✓ RSI & Moving Averages

    ✓ Technical Indicators

    ✓ LONG / SHORT Prediction

    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    if st.button("Launch Market Direction Module", use_container_width=True):
        st.switch_page("pages/market_direction.py")

with col2:

    st.markdown("""
    <div style="
    background:#708B75;
    padding:25px;
    border-radius:22px;
    color:black;
    min-height:320px;
    ">

    <h2 style="color:black;">Fixed Income Analytics</h2>

    Prices bonds via discounted cash flow, forecasts 30-day G-Sec
            yield moves with a Random Forest model trained on 10 years of data, then reprices the bond
            under that forecast. 

    <br>

    ✓ Random Forest

    ✓ DCF Pricing

    ✓ Duration Analysis

    ✓ Yield Forecasting

    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    if st.button("Launch Bond Yield Module", use_container_width=True):
        st.switch_page("pages/bond_yield.py")
