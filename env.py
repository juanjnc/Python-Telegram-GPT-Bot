import os
from dotenv import load_dotenv
from ast import literal_eval

load_dotenv()
USERS = literal_eval(os.getenv("USERS"))
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL")