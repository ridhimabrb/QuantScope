import streamlit as st

from equity.data import fetch_live_data
from equity.features import build_live_features, FEATURE_COLUMNS
from equity.model import ai_trade_decision

from styles import load_css

load_css()

col1, col2 = st.columns([1, 6])

with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")

st.title("📈 Equity Intelligence")

ticker = st.text_input("Enter Market Ticker", "^GSPC")

if st.button("Run AI Analysis", use_container_width=True):

    with st.spinner("Running model..."):

        df = fetch_live_data(ticker)

        features = build_live_features(df)

        latest = features.dropna(subset=FEATURE_COLUMNS).iloc[-1:]

        decision = ai_trade_decision(latest)

    c1, c2, c3 = st.columns(3)

    c1.metric("Recommendation", decision["decision"])

    c2.metric("Bullish", f"{decision['prob_up']*100:.1f}%")

    c3.metric("Bearish", f"{decision['prob_down']*100:.1f}%")

    st.info(decision["explanation"])

    left,right=st.columns(2)

    with left:
        st.subheader("Price")
        st.line_chart(df["Close"].tail(120))

    with right:
        st.subheader("Volume")
        st.bar_chart(df["Volume"].tail(120))

    st.subheader("Feature Snapshot")

    st.dataframe(
        latest[FEATURE_COLUMNS],
        use_container_width=True
    )