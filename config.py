import os
from dotenv import load_dotenv
load_dotenv()
API_ID = int(os.environ.get("API_ID", "20879824"))
API_HASH = os.environ.get("API_HASH", "5f70a9a12a4bb8cc322bed62bc6007ce")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "8849121451:AAFGdIoQiV6SR_LOnzW5hDgwztTYAKzl08Y")
MONGO_URL = os.getenv( "MONGO_URL",  "mongodb+srv://rupamedical:dQv9oKG7QK93BkIh@james.oufkybu.mongodb.net/?appName=james")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "0"))
ADMIN = 7340960697
# UI Images
PICS = [
    "https://ibb.co/N6sFQf4j",
    "https://ibb.co/v4FX9rMN",
    "https://ibb.co/8L9rDmB4",
    "https://ibb.co/kVTGm4Rn",
    "https://ibb.co/Hff6FyNH",
    "https://ibb.co/DDRzKfv5",
    "https://ibb.co/Y7ds8xGg",
    "https://ibb.co/0jY0HHND",
    "https://ibb.co/Z1kCz73X"
]

def get_random_pic():
    return random.choice(PICS)

# Initial images
START_PIC = PICS[0]
FORCE_PIC = PICS[1]
