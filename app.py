import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px
import requests

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="U.S. Macro Dashboard", layout="wide")
st.title("🇺🇸 United States Macroeconomic Dashboard")

# FRED API Key
FRED_API_KEY = "cc7a4c2477721fc8d59d2f03b849d722"

# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def get_fred_data(series_id):
    """Fetch data from FRED API."""
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    r = requests.get(url, params=params).json()
    if "observations" not in r:
        st.error(f"Failed to fetch data for {series_id}.")
        return pd.DataFrame(columns=["date", "value"])
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

st.subheader("📌 Key U.S. Indicators")

# FRED Series IDs
inflation = get_fred_data("CPIAUCSL")       # Consumer Price Index
gdp = get_fred_data("GDP")                  # Gross Domestic Product
interest_rate = get_fred_data("FEDFUNDS")   # Federal Funds Rate

# Market Data
sp500 = get_yahoo("^GSPC", "1y")            # S&P 500 Index
usdeur = get_yahoo("EURUSD=X", "1y")        # USD/EUR Exchange Rate

# ---------------------------------------------------------
# Display Charts
# ---------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.write("### 📊 U.S. Inflation (CPI)")
    fig = px.line(inflation, x="date", y="value", labels={"value": "CPI"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write("### 📈 U.S. GDP")
    fig = px.line(gdp, x="date", y="value", labels={"value": "GDP (Trillions USD)"})
    st.plotly_chart(fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.write("### 🏦 Federal Funds Rate")
    fig = px.line(interest_rate, x="date", y="value", labels={"value": "Interest Rate (%)"})
    st.plotly_chart(fig, use_container_width=True)

with col4:
    st.write("### 💱 USD/EUR Exchange Rate")
    fig = px.line(usdeur, x="Date", y="Close", labels={"Close": "USD/EUR"})
    st.plotly_chart(fig, use_container_width=True)

st.write("### 📉 S&P 500 Index")
fig = px.line(sp500, x="Date", y="Close", labels={"Close": "S&P 500"})
st.plotly_chart(fig, use_container_width=True)
