from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import START_TEXT, HELP_TEXT, START_PIC


def get_start_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📖 Help", callback_data="help_menu"),
            InlineKeyboardButton("❄️ Update", url=UPDATES),
        ],
        [
            InlineKeyboardButton("About ☘️", callback_data="about_menu")
        ]
    ])


@Client.on_message(filters.command("start") & filters.private)
async def start_handler(client, message):

    try:
        await message.reply_photo(
            photo=START_PIC,
            caption=START_TEXT,
            reply_markup=get_start_buttons()
        )
    except Exception:
        await message.reply_text(
            START_TEXT,
            reply_markup=get_start_buttons()
        )


@Client.on_message(filters.command("help") & filters.private)
async def help_handler(client, message):
    await message.reply_text(HELP_TEXT)
