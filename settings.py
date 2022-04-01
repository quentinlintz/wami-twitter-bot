import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = eval(os.environ.get('DEBUG'))
PROPERTY_ID = os.environ.get('PROPERTY_ID')
CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.environ.get('BEARER_TOKEN')
WAMI_API_KEY = os.environ.get('WAMI_API_KEY')
WAMI_URL = os.environ.get('WAMI_URL')