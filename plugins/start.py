import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users import add_user
from config import START_TEXT, HELP_TEXT, PICS, UPDATES

@Client.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    await add_user(user_id)

    # Checking if PICS is a list or a single string
    start_pic = random.choice(PICS) if isinstance(PICS, list) else PICS

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Settings", callback_data="settings")
        ],
        [
            InlineKeyboardButton("Updates", url=UPDATES),
            InlineKeyboardButton("Support", url="https://t.me/yoursupport")
        ]
    ])

    await message.reply_photo(
        photo=start_pic,
        caption=START_TEXT,
        reply_markup=buttons
    )
    
