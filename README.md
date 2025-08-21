# 

**OS: fedora 42**
**course**: web scraping with gpt: translate foreign news headlines

## HOW TO DO IT?

### SETUP

#### setup tools

- Python
- OpenAI API Key:
  - sign up [here](https://platform.openai.com/) > API Keys > Create new secret key > Save
  - billings: need credit balance for using apikey (at least 5$)

#### init virtual environment
```bash 
# create virtual env `venv`
python3 -m venv venv

# activate virtual env
source venv/bin/activate

# install lib
pip install requests beautifulsoup4 openai python-dotenv lxml

# run proj
python3 src/main.py
```

#### config OpenAI API Key
`.env`
```.env
OPENAI_API_KEY="ur-openai-api-key-here"
```
`.gitignore`
```.gitignore
.evn
venv/
```



