import os

from dotenv import load_dotenv


load_dotenv()


NUMBER_OF_WORDS = int(os.getenv("NUMBER_OF_WORDS", default=3))
