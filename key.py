import os.path
from dotenv import load_dotenv


# dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv()

CK = os.getenv("API_KEY")
CS = os.getenv("API_SECRET")
AK = os.getenv("ACCESS_TOKEN")
AS = os.getenv("ACCESS_TOKEN_SECRET")

NW = os.getenv("NEWS_KEY")

