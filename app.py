import streamlit as st
import feedparser

st.set_page_config(page_title="🔍 מעקב חדשות חכם", layout="centered")
st.title("🔔 מערכת חכמה למעקב אחרי מילות מפתח בחדשות")

# קלט מהממשק
user_input = st.text_input("הזן מילות מפתח (מופרדות בפסיקים)", "ביטקוין")

# פירוק מילות מפתח
keywords = [w.strip() for w in user_input.split(',') if w.strip()]
st.write(f"מילות מפתח שנסרקות: {keywords}")

# RSS מגלובס
news_feed_url = "https://www.globes.co.il/rss/homepage.xml"
st.write("מחפש בחדשות...")

feed = feedparser.parse(news_feed_url)
matches = []

# ניתוח כל חדשה
for entry in feed.entries:
    title = entry.title
    summary = entry.summary
    for word in keywords:
        if word in title or word in summary:
            matches.append({
                "title": entry.title,
                "link": entry.link,
                "word": word
            })
            break

# תצוגת כל הכותרות
if st.checkbox("הצג את כל כותרות החדשות"):
    st.write("### כל הכותרות:")
    for entry in feed.entries:
        st.markdown(f"- {entry.title}")

# תוצאות תואמות
if matches:
    st.success(f"נמצאו {len(matches)} תוצאות עם מילות מפתח:")
    for match in matches:
        st.markdown(
            f"- 🔹 **{match['title']}**  
"
            f"🔗 [קרא בכתבה]({match['link']})  
"
            f"💡 מילת מפתח: `{match['word']}`"
        )
else:
    st.info("לא נמצאו תוצאות עם המילים שהוזנו.")
