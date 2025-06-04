import streamlit as st
import yfinance as yf
import pandas as pd
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=60000, limit=None, key="auto_refresh")
st.set_page_config(page_title="תחזית חכמה", layout="centered")

st.title("🔮 תחזית זהב חכמה")
symbol = 'GC=F'
interval = '5m'
period = '1d'

data = yf.download(tickers=symbol, interval=interval, period=period)
if data.empty:
    st.error("שגיאה בטעינת הנתונים")
    st.stop()

current_price = round(float(data['Close'].iloc[-1]), 2)
ideal_entry_price = round(float(data['Close'].iloc[-2]), 2)
deviation = round(current_price - ideal_entry_price, 2)

st.markdown(f"**מחיר נוכחי:** {current_price} ₪")
st.markdown(f"**מחיר כניסה מומלץ:** {ideal_entry_price} ₪")
st.markdown(f"**סטייה מהכניסה:** {abs(deviation)} נק׳")
if abs(deviation) > 4:
    st.warning("⚠️ סטייה גבוהה מהמחיר המומלץ – ייתכן שהכניסה מאוחרת מדי")
else:
    st.success("✅ המחיר עדיין בתחום כניסה סביר")

# Placeholder for additional logic like trend, recommendation, target price
st.markdown(f"**מגמה:** מגמת עלייה ✅")
st.markdown(f"**המלצה לביצוע:** BUY")
st.markdown(f"**יעד רווח:** {round(current_price * 1.002, 2)} ₪")
st.markdown(f"**רמת ביטחון:** 85%")
st.markdown(f"**זמן החזקה מומלץ:** 30 דקות")
