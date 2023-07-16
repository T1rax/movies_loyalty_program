import json
import os

from dotenv import load_dotenv


load_dotenv()

# Уровни указываются списком с числами по возрастанию.
# Первый уровень является дефолтным при создании счета
LOYALTY_LEVELS: list[int] = json.loads(
    os.getenv("LOYALTY_LEVELS", default="[5, 10, 15]")
)
