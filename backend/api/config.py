import os

from dotenv import load_dotenv


load_dotenv()


OAUTH_SECRET_KEY = os.environ.get("OAUTH_SECRET_KEY")
