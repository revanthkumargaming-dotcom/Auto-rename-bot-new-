from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import *


def get_start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📖 Help",
                callback_data="help_menu"
            )
        ]
    ])


@Client.on_message(filters.command("start"))
async def start_handler(client, message):

    print("🔥 START COMMAND RECEIVED")

    try:

        await message.reply_text(
            "✅ START TEXT WORKING"
        )

        print("✅ TEXT SENT")

    except Exception as e:

        print("❌ START ERROR =", e)
