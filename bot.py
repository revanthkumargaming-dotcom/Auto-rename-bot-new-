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
    return "Bot Running"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

# ================= BOT =================

bot = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= AUTH =================

allowed_users = set()

def is_auth(uid):
    return uid == OWNER_ID or uid in allowed_users

# ================= STORAGE =================

user_autorename = {}
user_font = {}
user_metadata = {}

sequence_mode = {}
sequence_files = {}

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(_, msg):

    if not is_auth(msg.from_user.id):
        return await msg.reply_text("❌ Not authorised")

    photo = random.choice(START_PICS)

    await msg.reply_photo(
        photo=photo,
        caption=START_TEXT.format(mention=msg.from_user.mention)
    )

# ================= OWNER COMMANDS =================

@bot.on_message(filters.command("adduser"))
async def add_user(_, msg):

    if msg.from_user.id != OWNER_ID:
        return await msg.reply_text("❌ Only owner")

    if len(msg.command) < 2:
        return await msg.reply_text("Usage: /adduser user_id")

    uid = int(msg.command[1])
    allowed_users.add(uid)

    await msg.reply_text(f"✅ Added {uid}")

@bot.on_message(filters.command("removeuser"))
async def remove_user(_, msg):

    if msg.from_user.id != OWNER_ID:
        return await msg.reply_text("❌ Only owner")

    if len(msg.command) < 2:
        return await msg.reply_text("Usage: /removeuser user_id")

    uid = int(msg.command[1])
    allowed_users.discard(uid)

    await msg.reply_text(f"❌ Removed {uid}")

@bot.on_message(filters.command("users"))
async def users(_, msg):

    if msg.from_user.id != OWNER_ID:
        return

    if not allowed_users:
        return await msg.reply_text("No users")

    await msg.reply_text("\n".join(map(str, allowed_users)))

# ================= FEATURES =================

@bot.on_message(filters.command("autorename"))
async def autorename(_, msg):

    if not is_auth(msg.from_user.id):
        return

    if len(msg.command) < 2:
        return await msg.reply_text("Usage: /autorename NEW_{filename}")

    user_autorename[msg.from_user.id] = msg.text.split(None, 1)[1]
    await msg.reply_text("✅ Saved")

@bot.on_message(filters.command("font"))
async def font(_, msg):

    if not is_auth(msg.from_user.id):
        return

    if len(msg.command) < 2:
        return await msg.reply_text("Usage: /font bold")

    user_font[msg.from_user.id] = msg.text.split(None, 1)[1].lower()
    await msg.reply_text("✅ Font saved")

@bot.on_message(filters.command("metadata"))
async def metadata(_, msg):

    if not is_auth(msg.from_user.id):
        return

    if len(msg.command) < 2:
        return await msg.reply_text("Usage: /metadata text")

    user_metadata[msg.from_user.id] = msg.text.split(None, 1)[1]
    await msg.reply_text("✅ Metadata saved")

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
async def seq_start(_, msg):

    if not is_auth(msg.from_user.id):
        return

    sequence_mode[msg.from_user.id] = True
    sequence_files[msg.from_user.id] = []

    await msg.reply_text("📥 Sequence started")

@bot.on_message(filters.command("endsequence"))
async def seq_end(_, msg):

    if not is_auth(msg.from_user.id):
        return

    files = sequence_files.get(msg.from_user.id, [])

    if not files:
        return await msg.reply_text("❌ No files")

    await msg.reply_text("📤 Sending...")

    for m in files:
        f = await m.download()
        await msg.reply_document(f)
        os.remove(f)

    sequence_mode[msg.from_user.id] = False
    sequence_files[msg.from_user.id] = []

    await msg.reply_text("✅ Done")

# ================= FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def handler(_, msg):

    uid = msg.from_user.id

    if not is_auth(uid):
        return await msg.reply_text("❌ Not authorised")

    try:
        status = await msg.reply_text("📥 Downloading...")

        file = await msg.download()

        base = os.path.basename(file)

        rename = user_autorename.get(uid)
        font = user_font.get(uid, "normal")
        meta = user_metadata.get(uid)

        new_name = rename.replace("{filename}", base) if rename else base

        caption = new_name

        if meta:
            caption += f"\n\n{meta}"

        if font == "bold":
            caption = f"**{caption}**"
        elif font == "italic":
            caption = f"__{caption}__"
        elif font == "mono":
            caption = f"`{caption}`"

        await status.edit("📤 Uploading...")

        await msg.reply_document(
            document=file,
            file_name=new_name,
            caption=caption
        )

        await status.delete()
        os.remove(file)

    except Exception as e:
        await msg.reply_text(f"❌ Error: {e}")

# ================= RUN =================

print("🚀 Bot Started Successfully")
bot.run()
