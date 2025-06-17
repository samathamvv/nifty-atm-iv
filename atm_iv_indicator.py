import streamlit as st
import requests

def fetch_iv():
    url = "https://nse-data-api.onrender.com/option-chain?symbol=NIFTY"
    response = requests.get(url)
    data = response.json()

    spot = data['records']['underlyingValue']
    atm = round(spot / 50) * 50

    iv = None
    for item in data['records']['data']:
        if item['strikePrice'] == atm and 'CE' in item:
            iv = item['CE'].get('impliedVolatility')
            break

    return spot, atm, iv

# Streamlit App UI
st.set_page_config(page_title="Live NIFTY ATM IV", layout="wide")
st.title("📈 Live NIFTY ATM IV Tracker")

try:
    spot, atm, iv = fetch_iv()
    st.metric("NIFTY Spot Price", spot)
    st.metric("ATM Strike", atm)
    st.metric("ATM IV (%)", iv)
    st.caption("🔁 Refresh the page to update data.")
except Exception as e:
    st.error("⚠️ Could not fetch IV data. Please try again later.")
