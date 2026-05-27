import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID", "20879824"))
API_HASH = os.getenv("API_HASH", "5f70a9a12a4bb8cc322bed62bc6007ce")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8849121451:AAEu-1_X1Y-j8jjmt1nyRtuUIvxpavnd-Zk")

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://rupamedical:dQv9oKG7QK93BkIh@james.oufkybu.mongodb.net/?appName=james"
)

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))
ADMIN = 7340960697
