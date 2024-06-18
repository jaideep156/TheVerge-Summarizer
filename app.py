import streamlit as st
import requests
import datetime
from bs4 import BeautifulSoup
import google.generativeai as genai

st.set_page_config(
    page_title="TheVerge Summarizer",
    page_icon="🧙‍♂️",
    initial_sidebar_state="collapsed"
)

with st.sidebar:
    st.subheader("""Checkout the code below""")
    st.page_link("https://github.com/jaideep156/TheVerge-Summarizer", label="GitHub", icon="⚡")

prompt="""You are a news article summarizer. You will be getting the whole article and you are tasked to summarize the entire article in points with at most 150 words. This is the article: """

BASE_URL = "https://newsapi.org/v2/top-headlines"

# I have added my secret API keys using the streamlit cloud UI. You can follow the process using this link https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management#deploy-an-app-and-set-up-secrets

NEWS_API = st.secrets["NEWS_API"]
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

def generate_gemini_content(prompt,article_content):
    model=genai.GenerativeModel("gemini-1.5-pro")
    response=model.generate_content(prompt+article_content)
    return response.text

def get_api_data(api_key):
    endpoint_url = f"{BASE_URL}?sources=the-verge&apiKey={NEWS_API}&pageSize=6"
    
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except ValueError as json_err:
        print(f"JSON decoding error: {json_err}")

data = get_api_data(NEWS_API)

def fetch_and_extract_article(url):
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    paragraphs = soup.find_all('p')
    skip_intro = True
    filtered_paragraphs = []

    for paragraph in paragraphs:
        text = paragraph.text.strip()
        
        if skip_intro:
            skip_intro = False
            continue

        if "/ Sign up for Verge Deals" in text:
            break
        filtered_paragraphs.append(text)
    
    return ' '.join(filtered_paragraphs)

st.title("AI Spotlight: A news digest🔮")

st.markdown("##### Get the latest scoop on tech news🪄This project uses the power of Google Gemini to deliver crisp summaries of the hottest articles from [The Verge](https://www.theverge.com/).")

st.markdown("###### 📰The articles are extracted from the ```/v2/top-headlines``` endpoint of [newsapi.org](https://newsapi.org/docs/endpoints/top-headlines).")
st.markdown("###### 💻Checkout the full code on [GitHub](https://github.com/jaideep156/TheVerge-Summarizer/).")
st.write("---")

st.markdown("###### The following are the articles. Click on their respective buttons to summarize them.")

for index, article in enumerate(data['articles'][1:], start=1):
    title = article['title']
    url = article['url']
    author = article['author']
    urlToImage = article['urlToImage']

    publishedAt = article['publishedAt']
    publishedAt = publishedAt.replace("Z", "")
    dt = datetime.datetime.fromisoformat(publishedAt)
    formatted_date = dt.strftime("%d/%m/%Y")

    st.subheader(title)
    st.image(urlToImage,width=675)
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