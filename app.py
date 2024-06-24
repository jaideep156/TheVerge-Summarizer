import streamlit as st
import datetime
import google.generativeai as genai
from functions import generate_gemini_content,get_api_data,fetch_and_extract_article

st.set_page_config(
    page_title="TheVerge Summarizer",
    page_icon="🧙‍♂️",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.subheader("""Checkout the code below""")
    st.page_link("https://github.com/jaideep156/TheVerge-Summarizer", label="GitHub", icon="⚡")

prompt="""You are a news article summarizer. You will be getting the whole article and you are tasked to summarize the entire article in points with at most 150 words. This is the article: """

# I have added my secret API keys using the streamlit cloud UI. You can follow the process using this link https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management#deploy-an-app-and-set-up-secrets

NEWS_API = st.secrets["NEWS_API"]
BACKUP_NEWS_API_KEY = st.secrets['backup_key']['BACKUP_NEWS_KEY']
google_api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=google_api_key)

@st.cache_data(ttl=7200)
def fetch_data():
    return get_api_data(NEWS_API, BACKUP_NEWS_API_KEY)

data, error_message = fetch_data()

st.title("Verge-Digest: AI-Powered Article Summarizer🔮")
st.markdown("##### Get the latest scoop on tech news🪄This project uses the power of Google Gemini to deliver crisp summaries of the hottest articles from [The Verge](https://www.theverge.com/).")

st.markdown("###### 📰The articles are extracted from the ```/v2/top-headlines``` endpoint of [newsapi.org](https://newsapi.org/docs/endpoints/top-headlines).")
st.markdown("###### 💻Checkout the full code on [GitHub](https://github.com/jaideep156/TheVerge-Summarizer/).")
st.write("---")

if error_message:
    st.error(error_message)
else:
    st.markdown("###### The following are the articles. Click on their respective buttons to summarize them.")
    verge_present = any(article['title'] == "The Verge" for article in data['articles'])

    filtered_articles = [article for article in data['articles'] if article['title'] != "The Verge"]

    if not verge_present:
        filtered_articles = filtered_articles[:5]

    for index, article in enumerate(filtered_articles):
        title = article['title']
        url = article['url']
        author = article['author']
        urlToImage = article['urlToImage']
        publishedAt = article['publishedAt']

        publishedAt = article['publishedAt']
        publishedAt = publishedAt.replace("Z", "")
        dt = datetime.datetime.fromisoformat(publishedAt)
        formatted_date = dt.strftime("%d/%m/%Y")

        st.subheader(title)
        st.image(urlToImage, width=675)
        st.write(f"Written by {author} & published on {formatted_date}")

        if st.button(f"Summarize this article", key=f"summarize_{index}"):
            with st.spinner("Fetching article..."):
                article_content = fetch_and_extract_article(url)
            
            with st.spinner("Summarizing using Google Gemini..."):
                summary = generate_gemini_content(prompt, article_content)
                
            st.write(summary)
            st.caption(f"[View the full article]({url})")

        st.write("---")
    st.markdown("⭐ this project on [GitHub](https://github.com/jaideep156/TheVerge-Summarizer/).")