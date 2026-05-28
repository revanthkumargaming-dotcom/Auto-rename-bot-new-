import os
import re
import time
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ================= FLASK =================

flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot Is Running Successfully ✅"

def run_web():
    flask_app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()

# ================= CONFIG =================

API_ID = int(os.getenv("API_ID", "123456"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
START_PIC = os.getenv("START_PIC")

# ================= BOT =================

bot = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= STORAGE =================

user_prefix = {}
user_suffix = {}
user_autorename = {}
user_font = {}
sequence_mode = {}
sequence_files = {}

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    text = """
🤖 AUTO RENAME BOT

📁 Send file → rename → return
⚡ Fast & Clean Bot
"""

    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔥 Join Channel", url="https://t.me/YOUR_CHANNEL")]]
    )

    if START_PIC:
        await message.reply_photo(START_PIC, text, reply_markup=btn)
    else:
        await message.reply_text(text, reply_markup=btn)

# ================= HELP =================

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text("""
📌 COMMANDS

/prefix text
/suffix text
/autorename format
/font bold|italic|mono|normal
/sequence
/endsequence
""")

# ================= PREFIX =================

@bot.on_message(filters.command("prefix"))
async def prefix(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /prefix text")

    user_prefix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Prefix Saved")

# ================= SUFFIX =================

@bot.on_message(filters.command("suffix"))
async def suffix(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /suffix text")

    user_suffix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Suffix Saved")

# ================= FONT =================

@bot.on_message(filters.command("font"))
async def set_font(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /font mono")

    font = message.command[1].lower()

    if font not in ["bold", "italic", "mono", "normal"]:
        return await message.reply_text("❌ Invalid Font")

    user_font[message.from_user.id] = font
    await message.reply_text(f"✅ Font set to {font}")

# ================= AUTORENAME =================

@bot.on_message(filters.command("autorename"))
async def autorename(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /autorename format")

    user_autorename[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ AutoRename Saved")

# ================= SEQUENCE START =================

@bot.on_message(filters.command("sequence"))
async def start_sequence(client, message):

    sequence_mode[message.from_user.id] = True
    sequence_files[message.from_user.id] = []

    await message.reply_text("📥 Sequence Started")

# ================= END SEQUENCE =================

@bot.on_message(filters.command("endsequence"))
async def end_sequence(client, message):

    user_id = message.from_user.id
    files = sequence_files.get(user_id, [])

    if not files:
        return await message.reply_text("❌ No files")

    for msg in files:
        await bot.copy_message(message.chat.id, msg.chat.id, msg.id)

    sequence_mode[user_id] = False
    sequence_files[user_id] = []

    await message.reply_text("✅ Done")

# ================= FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def rename_file(client, message):

    user_id = message.from_user.id

    if sequence_mode.get(user_id):
        sequence_files[user_id].append(message)
        return await message.reply_text("📥 Added")

    file = await message.download()
    base = os.path.basename(file)

    prefix = user_prefix.get(user_id, "")
    suffix = user_suffix.get(user_id, "")
    font = user_font.get(user_id, "normal")

    new_name = f"{prefix} RENAMED_{base} {suffix}".strip()

    # ================= FONT APPLY =================
    if font == "bold":
        caption = f"**{new_name}**"
    elif font == "italic":
        caption = f"__{new_name}__"
    elif font == "mono":
        caption = f"`{new_name}`"
    else:
        caption = new_name

    await message.reply_document(
        file,
        file_name=new_name,
        caption=caption
    )

    os.remove(file)

# ================= RUN =================

print("🚀 Bot Started Successfully")
bot.run()
