import streamlit as st
import pandas as pd

from bond.dcf import price_bond,reprice_under_shock
from bond.forecast import forecast_yield

from styles import load_css

load_css()

col1, col2 = st.columns([1, 6])

with col1:
    if st.button("← Back to Dashboard"):
        st.switch_page("app.py")
        
st.title("🏦 Fixed Income Analytics")

left,right=st.columns(2)

with left:

    face=st.number_input("Face Value",1000.0)

    coupon=st.number_input("Coupon Rate (%)",7.2)

    years=st.number_input("Years",10.0)

    ytm=st.number_input("Yield (%)",7.0)

    freq=st.selectbox(
        "Coupon Frequency",
        [2,1],
        format_func=lambda x:"Semi Annual" if x==2 else "Annual"
    )

result=price_bond(face,coupon,years,ytm,freq)

with right:

    st.metric("Fair Price",f"₹{result.price:,.2f}")

    st.metric("Macaulay",f"{result.macaulay_duration:.2f}")

    st.metric("Modified",f"{result.modified_duration:.2f}")

st.divider()

shock=st.slider(
    "Yield Shock (bps)",
    -200,
    200,
    50
)

new=reprice_under_shock(
    face,
    coupon,
    years,
    ytm,
    shock,
    freq
)

st.metric(
    "Repriced Bond",
    f"₹{new.price:,.2f}",
    delta=f"₹{new.price-result.price:,.2f}"
)

st.divider()

uploaded=st.file_uploader(
    "Upload Yield CSV",
    type="csv"
)

if uploaded:

    df=pd.read_csv(
        uploaded,
        parse_dates=["Date"]
    )

    df=df.sort_values("Date")

    forecast=forecast_yield(df["Price"])

    st.metric(
        "30-Day Forecast",
        f"{forecast:.2f}%"
    )

    st.line_chart(
        df.set_index("Date")["Price"]
    )