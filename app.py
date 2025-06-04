import streamlit as st
import feedparser

st.set_page_config(page_title="🔍 מעקב חדשות חכם", layout="centered")
st.title("🔔 מערכת חכמה למעקב אחרי מילות מפתח בחדשות")

# קלט מהממשק
user_input = st.text_input("הזן מילות מפתח (מופרדות בפסיקים)", "ביטקוין, קריסה, מלחמה, המלצה")

keywords = [w.strip() for w in user_input.lower().split(',') if w.strip()]
news_feed_url = "https://www.globes.co.il/rss/homepage.xml"

st.write("מחפש בחדשות...")

feed = feedparser.parse(news_feed_url)
matches = []

for entry in feed.entries:
    title = entry.title.lower()
    summary = entry.summary.lower()
    for word in keywords:
        if word in title or word in summary:
            matches.append({
                "title": entry.title,
                "link": entry.link,
                "word": word
            })
            break

# תצוגה
if matches:
    st.success(f"נמצאו {len(matches)} תוצאות:")
    for match in matches:
        st.markdown(
            f"- 🔹 **{match['title']}**  \n"
            f"🔗 [קרא בכתבה]({match['link']})  \n"
            f"💡 מילת מפתח: `{match['word']}`"
        )
else:
    st.info("לא נמצאו תוצאות עם המילים שהוזנו.")
