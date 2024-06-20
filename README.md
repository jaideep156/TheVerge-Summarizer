# [verge-digest](https://verge-digest.streamlit.app/): AI-powered article summarizer of [TheVerge](https://www.theverge.com/)🪄

This project is aimed at performing [text summarization](https://en.wikipedia.org/wiki/Automatic_summarization#:~:text=Text%20summarization%20is%20usually%20implemented%20by%20natural%20language%20processing%20methods%2C%20designed%20to%20locate%20the%20most%20informative%20sentences%20in%20a%20given%20document.) of top tech news articles from [The Verge](https://www.theverge.com/) using [Google Gemini 1.5 Pro](https://deepmind.google/technologies/gemini/pro/).

## To access the live version of the app, click [here](https://verge-digest.streamlit.app/).
## 📊Data
The articles are fetched from the ```/v2/top-headlines``` endpoint of [newsapi.org](https://newsapi.org/docs/endpoints/top-headlines) with a fallback to the same API but with another key if it fails due to some reason. It gives 6 observations in  `JSON` format with various key value pairs like `article`, `date`, `author`, `link`, etc.   

For summarizing, the [Google Gemini API](https://ai.google.dev/api/python/google/generativeai) key from [AI Studio](https://aistudio.google.com/).

## 📖API Reference
#### Get all items

```http
  GET https://newsapi.org/v2/top-headlines?sources=the-verge&apiKey={YOUR_KEY_HERE}&pageSize=6
```
### Limitations
Since I am using the free version of the API, it is  limited to 100 requests over a 24 hour period (50 requests available every 12 hours).

## 📝Dependencies
The [`requirements.txt`](https://github.com/jaideep156/TheVerge-Summarizer/blob/main/requirements.txt) has the following libraries:
- [google-generativeai](https://ai.google.dev/api/python/google/generativeai) to build with Gemini API.
- [streamlit](https://streamlit.io/) to transform Python scripts into interactive web apps.
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)  to scrape information from web pages.

## 🛠️Methodology
First we GET  the `JSON` output from [newsapi.org](https://newsapi.org/docs/endpoints/top-headlines). 

I have set the API to give 6 results because one of them might contain an article about The Verge itself which isn't relevant. If it exists in the `JSON` response of the API, we skip it & show the remaining 5 results. If not then only the first 5 results. 

### Article fetching & summarization
Next, we use `beautifulsoup4` to fetch & extract the articles from the `link` key value pair in the `JSON` response from the```/v2/top-headlines``` endpoint of [newsapi.org](https://newsapi.org/docs/endpoints/top-headlines) as mentioned above.

Then, it is looped using a `for` loop to extract different attributes of the `JSON` response like `title`, `link`, `date`, `author`, `urlToImage` 

### Summarization
Finally, each article has a button below it, which when pressed, initiates the `generate_gemini_content` function that takes `prompt` and  `article_content` as arguments combines them, and uses Google Gemini to produce a new piece of summarized text as the output.


## 💻Run Locally
Clone the project

```bash
  git clone https://github.com/jaideep156/TheVerge-Summarizer.git
```

Go to the project directory

```bash
  cd TheVerge-Summarizer
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  streamlit run app.py
```
P.S. Make sure to provide your correct API credentials in `.streamlit/secrets.toml` file to run it locally on your machine. Mine are added to `.gitignore` so its not exposed. 

Also, I have added my API keys using the streamlit cloud UI using [these](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management#deploy-an-app-and-set-up-secrets) steps from the official documentation.
## ☁️Deployment
This code has been deployed using [Streamlit Community Cloud](https://streamlit.io/cloud) & the file is [`app.py`](https://github.com/jaideep156/TheVerge-Summarizer/blob/main/app.py)