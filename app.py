import streamlit as st
FRED_API_KEY = st.secrets["FRED_API_KEY"]


import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
import requests

st.set_page_config(page_title="Malaysia Macro Dashboard", layout="wide")
st.title("🇲🇾 Malaysia & ASEAN Macroeconomic Dashboard")

# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def get_fred_data(series_id):
    """Pull data from FRED API without installing fredapi."""
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": "YOUR_FRED_API_KEY",
        "file_type": "json"
    }
    r = requests.get(url, params=params).json()
    df = pd.DataFrame(r["observations"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"])
    return df    

def get_yahoo(symbol, period="1y"):
    df = yf.download(symbol, period=period)
    return df.reset_index()

# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------

st.subheader("📌 Key Malaysia Indicators")

# Replace with your own FRED API Key
st.warning("Replace YOUR_FRED_API_KEY with your real FRED API key inside the code.")

inflation = get_fred_data("MYCPIALLMINMEI")   # Malaysia CPI
gdp = get_fred_data("MYSNGDP")                 # Malaysia GDP
opr = get_fred_data("IRMMONDTB")               # Interest rate proxy

# Market Data
klci = get_yahoo("^KLSE", "1y")
usdmyr = get_yahoo("MYR=X", "1y")

# ---------------------------------------------------------
# Display Charts
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.write("### 🇲🇾 Malaysia Inflation (CPI)")
    fig = px.line(inflation, x="date", y="value")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### 🇲🇾 GDP Growth")
    fig = px.line(gdp, x="date", y="value")
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.write("### 🏦 Interest Rate (OPR Proxy)")
    fig = px.line(opr, x="date", y="value")
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.write("### 💵 USD/MYR Exchange Rate")
    fig = px.line(usdmyr, x="Date", y="Close")
    st.plotly_chart(fig, use_container_width=True)

st.write("### 📈 FBM KLCI")
fig = px.line(klci, x="Date", y="Close")
st.plotly_chart(fig, use_container_width=True)
