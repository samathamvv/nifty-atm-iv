import streamlit as st
import requests

def fetch_iv():
    url = "https://nse-data-api.onrender.com/option-chain?symbol=NIFTY"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, None, None

        data = response.json()
        spot = data['records']['underlyingValue']
        atm = round(spot / 50) * 50

        iv = None
        for item in data['records']['data']:
            if item['strikePrice'] == atm and 'CE' in item:
                iv = item['CE'].get('impliedVolatility')
                break

        return spot, atm, iv
    except Exception as e:
        return None, None, None

# Streamlit App
st.set_page_config(page_title="Live NIFTY ATM IV", layout="wide")
st.title("📈 Live NIFTY ATM IV Tracker")

spot, atm, iv = fetch_iv()

if spot is not None:
    st.metric("NIFTY Spot Price", spot)
    st.metric("ATM Strike", atm)
    st.metric("ATM IV (%)", iv)
    st.caption("🔁 Refresh to update.")
else:
    st.error("⚠️ Could not fetch IV data. The data provider may be offline temporarily.")
