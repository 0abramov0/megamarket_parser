import os
from dotenv import load_dotenv

load_dotenv()
URL = os.environ.get("URL")
TIMEOUT = int(os.environ.get("TIMEOUT"))
