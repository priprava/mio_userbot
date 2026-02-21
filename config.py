import os
import spacy
from dotenv import load_dotenv

load_dotenv()

API_KEY = str(os.getenv("api_key"))
BASE_URL = str(os.getenv("base_url"))
MODEL = str(os.getenv("model"))
LOGIN=str(os.getenv("LOGIN"))
API_ID=int(os.getenv("API_ID"))
HASH_ID=str(os.getenv("HASH_ID"))
USERNAME=str(os.getenv("USERNAME"))
PHONE= str(os.getenv("PHONE"))

llms = {}
nlp = spacy.load("ru_core_news_sm")

with open(r"ai\mio_prompt1.txt", encoding="utf-8") as txt_prompt:
    SYSTEM_MESSAGE = txt_prompt.read().strip()