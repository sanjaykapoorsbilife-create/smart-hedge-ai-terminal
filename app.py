import streamlit as st
import requests
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="Smart Hedge AI Terminal", layout="wide")

st.title("Smart Hedge AI Terminal V4")

symbol = st.selectbox(
"Select Instrument",
["NIFTY","SENSEX","RELIANCE","HDFCBANK","ICICIBANK","TCS"]
)

def fetch_option_chain(symbol):

    if symbol == "NIFTY":
        url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"
    else:
        url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"

    headers = {"User-Agent": "Mozilla/5.0"}

    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)

    response = session.get(url, headers=headers)
    data = response.json()

    return data["records"]["data"]

if st.button("RUN ANALYSIS"):

    try:

        records = fetch_option_chain(symbol)

        call_data=[]
        put_data=[]

        for item in records:

            if "CE" in item and "PE" in item:

                strike=item["strikePrice"]
                call_oi=item["CE"]["openInterest"]
                put_oi=item["PE"]["openInterest"]

                call_data.append((strike,call_oi))
                put_data.append((strike,put_oi))

        call_df=pd.DataFrame(call_data,columns=["strike","call_oi"])
        put_df=pd.DataFrame(put_data,columns=["strike","put_oi"])

        highest_call=call_df.loc[call_df["call_oi"].idxmax()]
        highest_put=put_df.loc[put_df["put_oi"].idxmax()]

        support=highest_put["strike"]
        resistance=highest_call["strike"]

        merged=pd.merge(call_df,put_df,on="strike")
        merged["total_oi"]=merged["call_oi"]+merged["put_oi"]

        max_pain=merged.loc[merged["total_oi"].idxmax()]["strike"]

        price = yf.Ticker("^NSEI").history(period="1d")["Close"].iloc[-1]

        pcr = put_df["put_oi"].sum() / call_df["call_oi"].sum()

        bullish=0
        bearish=0

        if price>support:
            bullish+=20
        else:
            bearish+=20

        if price<max_pain:
            bullish+=10
        else:
            bearish+=10

        if pcr>1:
            bullish+=10
        else:
            bearish+=10

        bullish+=25
        bearish+=15

        total=bullish+bearish

        bull_prob=round((bullish/total)*100)
        bear_prob=round((bearish/total)*100)

        st.subheader("Market Structure")

        st.write("Price:",round(price,2))
        st.write("Support:",support)
        st.write("Resistance:",resistance)
        st.write("Max Pain:",max_pain)

        st.subheader("Sentiment")

        st.write("PCR:",round(pcr,2))

        st.subheader("AI Probability")

        st.write("Bullish:",bull_prob,"%")
        st.write("Bearish:",bear_prob,"%")

        if bull_prob>70:
            st.success("🟢 GREEN SIGNAL")
            st.write("Trade: BUY",max_pain,"CE")

        elif bull_prob>55:
            st.warning("🟠 WAIT")

        else:
            st.error("🔴 RED SIGNAL")
            st.write("Trade: BUY",max_pain,"PE")

    except:
        st.error("Data fetch failed. Please try again.")
