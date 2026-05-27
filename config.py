import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.environ.get("API_ID", "20879824"))
API_HASH = os.environ.get("API_HASH", "5f70a9a12a4bb8cc322bed62bc6007ce")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "7336133398:AAFmQyV7EbtWzVXT9J1MJdz-nnih1sFSWpM")

MONGO_URL = os.getenv(
    "MONGO_URL",
    "mongodb+srv://rupamedical:dQv9oKG7QK93BkIh@james.oufkybu.mongodb.net/?appName=james"
)

LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))
ADMIN = 7340960697
