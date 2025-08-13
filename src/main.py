import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

news_sources = {
  "chinese": (
    "https://cn.chinadaily.com.cn", 
    "div.Home_content_Item_Text h1 a"
  ),
  "french": (
    "https://www.lemonde.fr/", 
    "h3.article__title a"
  ),
  "german": (
    "https://www.spiegel.de/", 
    "article h2 a span"
  ),
  "spanish": (
    "https://elpais.com/", 
    "h2 a"
  )
}

def fetch_headlines(language: str, limit: int = 5):
  if language not in news_sources:
    print(f"[error]: don't support '{language}'.")
    return None

  url, selector = news_sources[language]

  headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
  }

  try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    headline_elements = soup.select(selector)
    
    headlines = [elem.get_text(strip=True) for elem in headline_elements if elem.get_text(strip=True)]
    
    if not headlines:
      print(f"[error]: can't find headline in '{selector}'.")
      return None
    return headlines[:limit]

  except requests.RequestException as e:
      print(f"[error]: fetch headlines error: {e}")
      return None

def create_prompt(headlines: list):
  headlines_str = "\n".join(headlines)
  
  prompt = f"""
Translate the following headlines into English and provide a one-sentence summary for each.

Headlines:
---
{headlines_str}
---

Your response should be in the format:
1. [English Translation] - [One-sentence summary]
2. [English Translation] - [One-sentence summary]
...
"""
  return prompt

def main():

  load_dotenv()
  api_key = os.getenv("OPENAI_API_KEY")

  if not api_key:
      print('[error]: OPENAI_API_KEY NOT in .env')
      return
  
  try:
    client = OpenAI(api_key=api_key)
    
    language_choice = input("Choose language (chinese, french, german, spanish): ").lower()
    print (f"Get news from this source: '{news_sources[language_choice][0]}'")

    selected_headlines = fetch_headlines(language_choice, limit=5)
    
    if selected_headlines:
      prompt_for_gpt = create_prompt(selected_headlines)
      
      response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "You are a helpful assistant specialized in translating and summarizing news headlines."},
          {"role": "user", "content": prompt_for_gpt}
        ],
        temperature=0.3, # reduce creativity -> consistency of rs
        max_tokens=400   # limitation length of output
      )
      
      print("\n--- trans results ---")
      translation_result = response.choices[0].message.content.strip()
      print(translation_result)

  except Exception as e:
    print(f"\n[error]: Something went wrong: {e}")


if __name__ == "__main__":
  main()