import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get("TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
NUMBER_OF_PRODUCT = 50

search_settings = {
    "price_min": 0,
    "price_max": 1e10,
    "cashback_min": 0,
    "product_name": "",
}
