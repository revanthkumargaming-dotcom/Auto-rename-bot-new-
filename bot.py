import os
import asyncio
import subprocess
from flask import Flask
from threading import Thread

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# =========================
# CONFIG (USE ENV IN RENDER)
# =========================
API_ID = 20879824
API_HASH = "5f70a9a12a4bb8cc322bed62bc6007ce"
BOT_TOKEN = ("8849121451:AAEu-1_X1Y-j8jjmt1nyRtuUIvxpavnd-Zk")
OWNER_ID = 7340960697


# =========================
# FLASK APP
# =========================
app_web = Flask(__name__)


@app_web.route("/")
def home():
    return "Bot Running Successfully"


# =========================
# PYROGRAM BOT
# =========================
bot = Client(
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
@bot.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/yourchannel")]
    ])

    await message.reply_text(
        "🔥 AUTO RENAME BOT IS LIVE 🔥",
        reply_markup=buttons
    )


# =========================
# PREFIX / SUFFIX
# =========================
@bot.on_message(filters.command("setprefix"))
async def setprefix(client, message):
    global PREFIX

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Not allowed")

    try:
        PREFIX = message.text.split(None, 1)[1]
        await message.reply_text(f"✅ Prefix: {PREFIX}")
    except:
        await message.reply_text("Usage: /setprefix text")


@bot.on_message(filters.command("setsuffix"))
async def setsuffix(client, message):
    global SUFFIX

    if message.from_user.id != OWNER_ID:
        return await message.reply_text("❌ Not allowed")

    try:
        SUFFIX = message.text.split(None, 1)[1]
        await message.reply_text(f"✅ Suffix: {SUFFIX}")
    except:
        await message.reply_text("Usage: /setsuffix text")


# =========================
# THUMBNAIL
# =========================
@bot.on_message(filters.photo)
async def save_thumb(client, message):
    os.makedirs("thumbnails", exist_ok=True)
    await message.download(file_name="thumbnails/thumb.jpg")
    await message.reply_text("✅ Thumbnail Saved")


# =========================
# RENAME SYSTEM
# =========================
@bot.on_message(filters.document)
async def rename_file(client, message):

    file = message.document
    old_name = file.file_name

    new_name = f"{PREFIX} {old_name} {SUFFIX}"

    path = await message.download(file_name=f"downloads/{new_name}")
    output = f"downloads/encoded_{new_name}"

    subprocess.run([
        "ffmpeg",
        "-i", path,
        "-map", "0",
        "-c", "copy",
        "-metadata", "title=Encoded By Bot",
        output
    ])

    caption = f"""
✅ RENAMED SUCCESS

📂 {new_name}
⚡ Metadata Added
"""

    thumb = "thumbnails/thumb.jpg"

    if os.path.exists(thumb):
        await message.reply_document(output, thumb=thumb, caption=caption)
    else:
        await message.reply_document(output, caption=caption)

    if os.path.exists(path):
        os.remove(path)

    if os.path.exists(output):
        os.remove(output)


# =========================
# RUN BOT
# =========================
def run_bot():
    async def start_bot():
        await bot.start()
        print("🤖 Bot Running")
        await asyncio.Event().wait()

    asyncio.run(start_bot())


# =========================
# RUN FLASK
# =========================
def run_flask():
    PORT = int(os.environ.get("PORT", 10000))
    print("🌐 Flask Running")
    app_web.run(host="0.0.0.0", port=PORT)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    Thread(target=run_bot).start()
    Thread(target=run_flask).start()
