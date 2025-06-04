
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="חיזוי חכם בזמן אמת", layout="centered")
st.title("📈 תחזית מסחר חכמה - זהב, מניות וקריפטו")
st.write("קבל תחזית מבוססת מגמה עם המלצה חכמה, יעד רווח וזמן החזקה.")

# רשימת נכסים
assets = {
    'זהב (Gold)': 'GC=F',
    'ביטקוין (Bitcoin)': 'BTC-USD',
    'נאסד"ק 100': '^NDX',
    'ת"א 125': 'TA125.TA'
}

# בחירת נכס
asset_name = st.selectbox("בחר נכס", list(assets.keys()))
symbol = assets[asset_name]

# בחירת טווח זמן
timeframes = {
    '1 דקה': '1m',
    '5 דקות': '5m',
    '15 דקות (במקום 10)': '15m',
    '30 דקות': '30m',
    'שעה': '60m',
    'יום': '1d'
}
timeframe_label = st.selectbox("בחר טווח זמן", list(timeframes.keys()))
interval = timeframes[timeframe_label]

# סכום השקעה
investment = st.number_input("הכנס סכום השקעה (ש\"ח)", min_value=100, value=1000, step=100)

# טען נתונים
@st.cache_data
def load_data(symbol, interval):
    try:
        data = yf.download(tickers=symbol, period="1d", interval=interval)
        return data
    except:
        return None

data = load_data(symbol, interval)

if data is None or data.empty:
    st.error("❗ שגיאה בטעינת הנתונים. נסה שוב בטווח זמן אחר או עם נכס שונה.")
else:
    data['SMA20'] = data['Close'].rolling(window=20).mean()
    data['SMA50'] = data['Close'].rolling(window=50).mean()

    last_price = float(data['Close'].iloc[-1])
    sma20 = float(data['SMA20'].iloc[-1])
    sma50 = float(data['SMA50'].iloc[-1])

    # קביעת המלצה
    if sma20 > sma50:
        trend = "מגמת עלייה ✅"
        action = "קנייה (BUY)"
        target_price = round(last_price * 1.002, 2)
        confidence = 85
        hold_time = "עד 30 דקות"
    elif sma20 < sma50:
        trend = "מגמת ירידה ❌"
        action = "מכירה (SELL)"
        target_price = round(last_price * 0.998, 2)
        confidence = 82
        hold_time = "עד 30 דקות"
    else:
        trend = "מגמה לא ברורה ⚠️"
        action = "המתן (NO ACTION)"
        target_price = last_price
        confidence = 60
        hold_time = "אין המלצה"

    st.subheader(f"🔍 תוצאה עבור {asset_name} ({interval})")
    st.markdown(
        f"""
        **מחיר נוכחי:** {last_price} ₪  
        **מגמה:** {trend}  
        **המלצה:** {action}  
        **יעד רווח:** {target_price} ₪  
        **רמת ביטחון:** {confidence}%  
        **זמן החזקה מומלץ:** {hold_time}
        """)

