import streamlit as st
st.set_page_config(page_title="חיזוי חכם למסחר", layout="centered")

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=60000, limit=None, key="auto_refresh")

st.title("📈 תחזית מסחר חכמה - זהב, מניות וקריפטו")
st.write("🔄 המערכת מתרעננת כל 60 שניות, מזהה מגמות חכמות ומציגה גם מה קורה בטווח דקה כשאתה עובד עם טווח 5 דקות.")

now = datetime.now(pytz.timezone('Asia/Jerusalem'))
hour = now.hour

if 15 <= hour < 18:
    market_time_msg = "✅ זמן חזק למסחר – פתיחת שוק אמריקאי"
elif 9 <= hour < 11:
    market_time_msg = "✅ זמן טוב למסחר – פתיחת אירופה"
elif 18 <= hour < 22:
    market_time_msg = "⚠️ תיתכנה תנודות – היו זהירים"
else:
    market_time_msg = "❌ זמן חלש למסחר – השוק שקט"

st.markdown(f"### 🕒 {now.strftime('%H:%M')} — {market_time_msg}")

assets = {
    'זהב (Gold)': 'GC=F',
    'ביטקוין (Bitcoin)': 'BTC-USD',
    'נאסד"ק 100': '^NDX',
    'ת"א 125': 'TA125.TA'
}

asset_name = st.selectbox("בחר נכס", list(assets.keys()))
symbol = assets[asset_name]

timeframes = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '15 דקות': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d'
}
timeframe_label = st.selectbox("בחר טווח זמן", list(timeframes.keys()))
interval = timeframes[timeframe_label]

investment = st.number_input("הכנס סכום השקעה (ש\"ח)", min_value=100, value=1000, step=100)

@st.cache_data
def load_data(symbol, interval):
    try:
        data = yf.download(tickers=symbol, period="1d", interval=interval)
        return data
    except:
        return None

data = load_data(symbol, interval)

def analyze_trend(data):
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    data['SMA50'] = data['Close'].rolling(window=50).mean()
    sma20 = float(data['SMA20'].iloc[-1])
    sma50 = float(data['SMA50'].iloc[-1])
    if sma20 > sma50:
        return "מגמת עלייה ✅"
    elif sma20 < sma50:
        return "מגמת ירידה ❌"
    else:
        return "מגמה לא ברורה ⚠️"

if data is None or data.empty:
    st.error("❗ שגיאה בטעינת הנתונים. נסה שוב בטווח זמן אחר או עם נכס שונה.")
else:
    trend_main = analyze_trend(data)
    st.subheader(f"🔍 תוצאה עבור {asset_name} ({interval})")
    st.markdown(f"**מגמה בטווח {timeframe_label}:** {trend_main}")

    if interval == '5m':
        data_1m = load_data(symbol, '1m')
        if data_1m is not None and not data_1m.empty:
            trend_1m = analyze_trend(data_1m)
            st.markdown(f"**מגמה בטווח 1 דקה:** {trend_1m}")

            if "עלייה" in trend_main and "עלייה" in trend_1m:
                st.success("✅ שתי התחזיות תואמות – אפשר לשקול כניסה בלב שקט.")
            elif "ירידה" in trend_main and "ירידה" in trend_1m:
                st.success("✅ שתי התחזיות תואמות – אפשר לשקול כניסה למכירה.")
            else:
                st.warning("⚠️ סתירה בין התחזיות – עדיף להמתין או לבדוק שוב עוד כמה דקות.")
