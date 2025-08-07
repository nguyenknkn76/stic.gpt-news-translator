import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

new_sites = {
  "chinese": (
    "https://cn.chinadaily.com.cn", 
    "div.Home_content_Item_Text h1 a"
  ),
}

def fetch_headlines (language):
  url, tag = new_sites.get(language, (None, None))
  if not url:
    print("language is not supported")
    return
  res = requests.get(url)
  soup = BeautifulSoup(res.text, 'lxml')
  headlines = [h.getText() for h in soup.select(tag)[:5]]
  return headlines

def create_prompt (headlines):
  join_headlines = "\n".join(headlines)
  prompt = f"Translate the following healines into English: \n{join_headlines}"
  return prompt

def main():
  load_dotenv()

  api_key = os.getenv("OPENAI_API_KEY")
  if not api_key:
    print('[error]: can NOT find apikey.')
    return
    
  client = OpenAI(api_key=api_key)

  user_language = input('what language are you interested in hearing news headlines summarised in?')
  selected_headlines = fetch_headlines(user_language)
  prompt = create_prompt(selected_headlines)
  res = client.chat.completions.create(
    model='gpt-3.5-turbo',
      messages=[{"role": "user", "content": prompt}
    ],
    temperature=0.1,
    max_tokens=200
  )

  print(res.choices[0].message.content)

if __name__ == "__main__":
  main()