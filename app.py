import streamlit as st
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Smart Hedge AI Terminal", layout="wide")

st.title("Smart Hedge AI Terminal")

symbols = {
"NIFTY 50":"^NSEI",
"SENSEX":"^BSESN"
}

symbol = st.selectbox("Select Market Index", list(symbols.keys()))

if st.button("RUN ANALYSIS"):

    ticker = yf.Ticker(symbols[symbol])

    data = ticker.history(period="5d")

    price = data["Close"].iloc[-1]
    support = data["Low"].min()
    resistance = data["High"].max()
    vwap = data["Close"].mean()

    bullish = 0
    bearish = 0

    if price > vwap:
        bullish += 40
    else:
        bearish += 40

    if price > support:
        bullish += 30
    else:
        bearish += 30

    if price < resistance:
        bullish += 20
    else:
        bearish += 20

    bullish += 10
    bearish += 10

    total = bullish + bearish

    bull_prob = round((bullish/total)*100)
    bear_prob = round((bearish/total)*100)

    st.subheader("Market Structure")

    st.write("Current Price:", round(price,2))
    st.write("Support:", round(support,2))
    st.write("Resistance:", round(resistance,2))
    st.write("VWAP:", round(vwap,2))

    st.subheader("AI Direction Probability")

    st.write("Bullish Probability:", bull_prob,"%")
    st.write("Bearish Probability:", bear_prob,"%")

    if bull_prob > 70:
        st.success("🟢 GREEN SIGNAL – Bullish Bias")

    elif bull_prob > 55:
        st.warning("🟠 NEUTRAL – Wait for Confirmation")

    else:
        st.error("🔴 RED SIGNAL – Bearish Bias")
