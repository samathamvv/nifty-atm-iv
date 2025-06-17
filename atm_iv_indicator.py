import streamlit as st
import requests
import time

def fetch_nifty_iv():
    headers = {"User-Agent": "Mozilla/5.0"}
    session = requests.Session()
    session.get("https://www.nseindia.com", headers=headers)
    res = session.get("https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY", headers=headers)
    data = res.json()
    spot = data['records']['underlyingValue']
    atm = round(spot / 50) * 50

    iv = None
    for item in data['records']['data']:
        if item['strikePrice'] == atm and 'CE' in item:
            iv = item['CE'].get('impliedVolatility', None)
            break
    return spot, atm, iv

st.set_page_config(page_title="Live NIFTY ATM IV", layout="wide")
st.title("📈 Live NIFTY ATM IV Tracker")
spot, atm, iv = fetch_nifty_iv()
st.metric("NIFTY Spot Price", spot)
st.metric("ATM Strike", atm)
st.metric("ATM IV (%)", iv)

st.markdown("🔁 Auto-refreshing every 60 seconds...")
time.sleep(60)
st.experimental_rerun()
