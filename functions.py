import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

def generate_gemini_content(prompt,article_content):
    model=genai.GenerativeModel("gemini-1.5-pro")
    response=model.generate_content(prompt+article_content)
    return response.text

BASE_URL = "https://newsapi.org/v2/top-headlines"

def get_api_data(api_key, backup_api_key):
    endpoint_url = f"{BASE_URL}?sources=the-verge&apiKey={api_key}&pageSize=6"
    
    try:
        response = requests.get(endpoint_url)
        response.raise_for_status()
        data = response.json()
        return data, None
    except requests.exceptions.HTTPError as http_err:
        error_code = response.status_code
        custom_messages = {
            400: f"Bad request. Please check your input. (Error code: {error_code})",
            401: f"Your API key is invalid or incorrect. Check your key, or go to https://newsapi.org to create a free API key.(Error code: {error_code})",
            403: f"Forbidden request. You don't have permission to access this resource. (Error code: {error_code})",
            404: f"Resource not found. Please check the URL. (Error code: {error_code})",
            429: f"Either exceeded API rate limits or too many requests. Please try again later. (Error code: {error_code})",
            500: f"Internal server error. Please try again later. (Error code: {error_code})",
        }
        error_message = custom_messages.get(error_code, f"HTTP error occurred: {response.reason} (Error code: {error_code})")
        # Check if the error is due to API key issue and attempt using backup key
        if error_message in custom_messages.values() and api_key != backup_api_key:
            return get_api_data(backup_api_key, api_key)  # Switching to backup API key
        else:
            return None, error_message
    except requests.exceptions.RequestException as err:
        return None, "An error occurred while making the request. Please try again later."
    except ValueError as json_err:
        return None, "Error decoding the response. Please try again later."
    
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