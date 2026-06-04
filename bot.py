import os
import time
import random
from flask import Flask
from threading import Thread

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import *

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# ================= BOT =================

bot = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= OWNER AUTH =================

OWNER_ID = 7340960697
allowed_users = set()

def is_auth(user_id):
    return user_id == OWNER_ID or user_id in allowed_users

# ================= STORAGE =================

user_prefix = {}
user_suffix = {}
user_metadata = {}
user_font = {}

sequence_mode = {}
sequence_files = {}

# ================= AUTH GUARD =================

@bot.on_message(~filters.command(["start", "add", "remove"]))
async def auth_guard(client, message):

    uid = message.from_user.id

    if not is_auth(uid):
        return await message.reply_text("❌ Not authorised to use this bot")

# ================= ADD USER =================

@bot.on_message(filters.command("add"))
async def add_user(client, message):

    if message.from_user.id != OWNER_ID:
        return

    uid = int(message.text.split(None, 1)[1])
    allowed_users.add(uid)

    await message.reply_text(f"✅ Added: {uid}")

# ================= REMOVE USER =================

@bot.on_message(filters.command("remove"))
async def remove_user(client, message):

    if message.from_user.id != OWNER_ID:
        return

    uid = int(message.text.split(None, 1)[1])
    allowed_users.discard(uid)

    await message.reply_text(f"🗑 Removed: {uid}")

# ================= SETTINGS =================

@bot.on_message(filters.command("settings"))
async def settings(client, message):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Prefix", callback_data="prefix"),
            InlineKeyboardButton("Suffix", callback_data="suffix")
        ],
        [
            InlineKeyboardButton("Font", callback_data="font"),
            InlineKeyboardButton("Metadata", callback_data="meta")
        ],
        [
            InlineKeyboardButton("Sequence", callback_data="seq")
        ]
    ])

    await message.reply_text("⚙️ Settings Panel", reply_markup=keyboard)

# ================= CALLBACK =================

@bot.on_callback_query()
async def cb(client, callback):

    d = callback.data

    if d == "prefix":
        await callback.message.reply_text("Use: /prefix text")

    elif d == "suffix":
        await callback.message.reply_text("Use: /suffix text")

    elif d == "font":
        await callback.message.reply_text("/font bold|italic|mono|normal")

    elif d == "meta":
        await callback.message.reply_text("Use: /metadata text")

    elif d == "seq":
        await callback.message.reply_text("/sequence then /endsequence")

    await callback.answer()

# ================= PREFIX =================

@bot.on_message(filters.command("prefix"))
async def prefix(client, message):
    user_prefix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Prefix set")

# ================= SUFFIX =================

@bot.on_message(filters.command("suffix"))
async def suffix(client, message):
    user_suffix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Suffix set")

# ================= METADATA =================

@bot.on_message(filters.command("metadata"))
async def metadata(client, message):
    user_metadata[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Metadata set")

# ================= FONT =================

@bot.on_message(filters.command("font"))
async def font(client, message):

    f = message.text.split(None, 1)[1].lower()

    if f not in ["bold", "italic", "mono", "normal"]:
        return await message.reply_text("❌ Invalid font")

    user_font[message.from_user.id] = f

    await message.reply_text(f"✅ Font: {f}")

# ================= SEQUENCE START =================

@bot.on_message(filters.command("sequence"))
async def seq_start(client, message):

    uid = message.from_user.id
    sequence_mode[uid] = True
    sequence_files[uid] = []

    await message.reply_text("📥 Sequence Started")

# ================= SEQUENCE COLLECT =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def collect(client, message):

    uid = message.from_user.id

    if sequence_mode.get(uid):
        sequence_files.setdefault(uid, []).append(message)
        return await message.reply_text("📥 Added to sequence")

# ================= SEQUENCE END =================

@bot.on_message(filters.command("endsequence"))
async def seq_end(client, message):

    uid = message.from_user.id
    files = sequence_files.get(uid, [])

    if not files:
        return await message.reply_text("❌ No files")

    await message.reply_text("📤 Sending files...")

    for msg in files:

        path = await msg.download()
        base = os.path.basename(path)

        await message.reply_document(
            document=path,
            file_name=base,
            caption="📦 Sequence File"
        )

        os.remove(path)

    sequence_mode[uid] = False
    sequence_files[uid] = []

    await message.reply_text("✅ Sequence Done")

# ================= FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def rename(client, message):

    uid = message.from_user.id
    path = await message.download()
    base = os.path.basename(path)

    prefix = user_prefix.get(uid, "")
    suffix = user_suffix.get(uid, "")
    meta = user_metadata.get(uid, "")
    font = user_font.get(uid, "normal")

    new_name = f"{prefix}{base}{suffix}"
    caption = new_name

    if meta:
        caption += f"\n\n📌 {meta}"

    if font == "bold":
        caption = f"**{caption}**"
    elif font == "italic":
        caption = f"__{caption}__"
    elif font == "mono":
        caption = f"`{caption}`"

    await message.reply_document(
        document=path,
        file_name=new_name,
        caption=caption
    )

    os.remove(path)

# ================= START =================

print("🚀 Bot Started")
bot.run()
