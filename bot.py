import os
import subprocess
from flask import Flask
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# CONFIG
# =========================
API_ID = 20879824
API_HASH = "5f70a9a12a4bb8cc322bed62bc6007ce"
BOT_TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"  # ⚠️ don't hardcode in public repo
OWNER_ID = 7340960697

MONGO_URL = "mongodb+srv://rupamedical:dQv9oKG7QK93BkIh@james.oufkybu.mongodb.net/?appName=james"


# =========================
# FOLDERS
# =========================
os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)


# =========================
# FLASK APP
# =========================
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot Running Successfully"


# =========================
# BOT CLIENT
# =========================
app = Client(
    "renamebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


QUEUE = []
PREFIX = "MovieHub"
SUFFIX = "x265"


# =========================
# START COMMAND
# =========================
@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/yourchannel")]
    ])

    await message.reply_text(
        "🔥 AUTO RENAME BOT IS RUNNING 🔥",
        reply_markup=buttons
    )


# =========================
# PREFIX
# =========================
@app.on_message(filters.command("setprefix"))
async def setprefix(client, message):
    global PREFIX

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Not allowed")

    try:
        PREFIX = message.text.split(None, 1)[1]
        await message.reply_text(f"✅ Prefix set: {PREFIX}")
    except:
        await message.reply_text("Usage: /setprefix text")


# =========================
# SUFFIX
# =========================
@app.on_message(filters.command("setsuffix"))
async def setsuffix(client, message):
    global SUFFIX

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Not allowed")

    try:
        SUFFIX = message.text.split(None, 1)[1]
        await message.reply_text(f"✅ Suffix set: {SUFFIX}")
    except:
        await message.reply_text("Usage: /setsuffix text")


# =========================
# THUMBNAIL
# =========================
@app.on_message(filters.photo)
async def save_thumb(client, message):
    await message.download(file_name="thumbnails/thumb.jpg")
    await message.reply_text("✅ Thumbnail Saved")


# =========================
# RENAME SYSTEM
# =========================
@app.on_message(filters.document)
async def rename_file(client, message):

    file = message.document
    old_name = file.file_name

    new_name = f"{PREFIX} {old_name} {SUFFIX}"
    QUEUE.append(new_name)

    path = await message.download(file_name=f"downloads/{new_name}")
    output_path = f"downloads/encoded_{new_name}"

    subprocess.run([
        "ffmpeg",
        "-i", path,
        "-map", "0",
        "-c", "copy",
        "-metadata", "title=Encoded By Bot",
        output_path
    ])

    caption = f"""
✅ RENAMED SUCCESS

📂 {new_name}
⚡ Metadata Added
"""

    thumb = "thumbnails/thumb.jpg"

    if os.path.exists(thumb):
        await message.reply_document(output_path, thumb=thumb, caption=caption)
    else:
        await message.reply_document(output_path, caption=caption)

    # cleanup
    if os.path.exists(path):
        os.remove(path)

    if os.path.exists(output_path):
        os.remove(output_path)

    if new_name in QUEUE:
        QUEUE.remove(new_name)


# =========================
# START EVERYTHING CLEANLY
# =========================
if __name__ == "__main__":

    print("🚀 Starting Bot...")

    # start bot
    app.start()
    print("✅ Bot Started")

    # start flask (Render needs PORT)
    PORT = int(os.environ.get("PORT", 10000))
    web.run(host="0.0.0.0", port=PORT)      
