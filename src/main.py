import os
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

def main():
  load_dotenv()

  api_key = os.getenv("OPENAI_API_KEY")
  if not api_key:
    print('[error]: can NOT find apikey.')
    return
  
  try: 
    client = OpenAI(api_key=api_key)
    print('create client success')

    res = client.chat.completions.create(
      model='gpt-3.5-turbo',
      messages=[
        {"role": "system", "content": "you are my assistant"},
        {"role": "user", "content": "hello user"}
      ]
    )
    print(res.choices[0].message.content)
  except Exception as e:
    print (f'[error]: error init client: {e}')

  new_sites = {
    "china": "chinese site url here",
    "korean": "korean site url here",
  }

  user_language = input('what language are you interested in hearing news headlines summarised in?')
  select_url = new_sites.get(user_language, 'language not supported')
  print(select_url)

if __name__ == "__main__":
  main()