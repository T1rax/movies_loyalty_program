import os

from dotenv import load_dotenv


load_dotenv()


LENGTH_CODE = int(os.getenv("LENGTH_CODE", default=5))
