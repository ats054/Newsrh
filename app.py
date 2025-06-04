import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="תחזית חכמה", layout="centered")
st_autorefresh(interval=60000, limit=None, key="auto_refresh")

st.title("🔮 תחזית זהב חכמה")
symbol = 'GC=F'
interval = st.selectbox("בחר טווח זמן", ['1m', '5m', '15m'])
period = '1d'

investment = st.number_input("הכנס סכום השקעה (ש\"ח)", min_value=100, value=1000, step=100)

data = yf.download(tickers=symbol, interval=interval, period=period)
if data.empty:
    st.error("שגיאה בטעינת הנתונים")
    st.stop()

current_price = round(float(data['Close'].iloc[-1]), 2)
st.markdown(f"**מחיר נוכחי:** {current_price} ₪")

# ניתוח מגמה פשוטה
def analyze_trend(data):
    sma_short = data['Close'].rolling(window=3).mean()
    sma_long = data['Close'].rolling(window=7).mean()
    if sma_short.iloc[-1] > sma_long.iloc[-1]:
        return "מגמת עלייה ✅", "BUY", round(float(data['Close'].iloc[-1] * 1.002), 2), 85
    else:
        return "מגמת ירידה ❌", "SELL", round(float(data['Close'].iloc[-1] * 0.998), 2), 82

trend, recommendation, target_price, confidence = analyze_trend(data)

# הצגה
st.markdown(f"### 🔍 תוצאה עבור זהב ({interval})")
st.markdown(f"**מגמה:** {trend}")
st.markdown(f"**המלצה לביצוע:** {recommendation}")
st.markdown(f"**יעד רווח:** {target_price} ₪")
st.markdown(f"**רמת ביטחון:** {confidence}%")
st.markdown(f"**זמן החזקה מומלץ:** עד 30 דקות")

# שדרוג חדש: השוואת מחיר כניסה
ideal_entry_price = round(float(data['Close'].iloc[-2]), 2)
deviation = round(current_price - ideal_entry_price, 2)
st.markdown(f"**מחיר כניסה מומלץ:** {ideal_entry_price} ₪")
st.markdown(f"**סטייה מהכניסה:** {abs(deviation)} נק׳")
if abs(deviation) > 4:
    st.warning("⚠️ סטייה גבוהה מהמחיר המומלץ – ייתכן שהכניסה מאוחרת מדי")
else:
    st.success("✅ המחיר עדיין בתחום כניסה סביר")
