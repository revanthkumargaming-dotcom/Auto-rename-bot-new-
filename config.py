import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.environ.get("API_ID", "20879824"))
API_HASH = os.environ.get("API_HASH", "5f70a9a12a4bb8cc322bed62bc6007ce")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8849121451:AAFGdIoQiV6SR_LOnzW5hDgwztTYAKzl08Y")
MONGO_URL = os.getenv( "MONGO_URL",  "mongodb+srv://rupamedical:dQv9oKG7QK93BkIh@james.oufkybu.mongodb.net/?appName=james")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))
ADMIN = 7340960697
START_PIC = os.getenv("START_PIC", "https://ibb.co/N6sFQf4j.jpg")
START_TEXT = """
👋 Hello {mention}

✨ Welcome to Auto Rename Bot

📂 Send me any file and I will automatically rename it.

⚡ Fast • Simple • Easy To Use
"""
HELP_TEXT = """
📖 Help Menu

1️⃣ /start - Bot start cheyyadaniki
2️⃣ Send any file - Rename process start avtundi

⚡ How it works:
• File send cheyyi
• New name set cheyyi
• Bot rename chesi return chestundi

❓ Any issue unte support channel check cheyyi
"""
