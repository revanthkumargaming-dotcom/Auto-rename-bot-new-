import os
import asyncio
import subprocess
from threading import Thread

from flask import Flask

from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import (
    API_ID,
    API_HASH,
    BOT_TOKEN
)

# Create folders
os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

# Flask App
web = Flask(__name__)

@web.route("/")
def home():
    return "Bot Running Successfully"

# Queue
QUEUE = []

# Telegram Bot
app = Client(
    "renamebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START
@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="settings"
            )
        ],
        [
            InlineKeyboardButton(
                "📢 Updates",
                url="https://t.me/yourchannel"
            )
        ]
    ])

    text = """
**🔥 ADVANCED AUTO RENAME BOT 🔥**

**✅ Features**
• Metadata Mode
• Prefix / Suffix
• Queue System
• x264/x265 Tags
• Thumbnail Support
• Bold Captions
"""

    await message.reply_text(
        text,
        reply_markup=buttons
    )

# Prefix/Suffix
PREFIX = "@MovieHub"
SUFFIX = "x265"

# Set Prefix
@app.on_message(filters.command("setprefix"))
async def setprefix(client, message):

    global PREFIX

    try:

        PREFIX = message.text.split(
            None, 1
        )[1]

        await message.reply_text(
            f"**✅ Prefix Saved:** `{PREFIX}`"
        )

    except:

        await message.reply_text(
            "**Usage:** `/setprefix text`"
        )

# Set Suffix
@app.on_message(filters.command("setsuffix"))
async def setsuffix(client, message):

    global SUFFIX

    try:

        SUFFIX = message.text.split(
            None, 1
        )[1]

        await message.reply_text(
            f"**✅ Suffix Saved:** `{SUFFIX}`"
        )

    except:

        await message.reply_text(
            "**Usage:** `/setsuffix text`"
        )

# Save Thumbnail
@app.on_message(filters.photo)
async def save_thumb(client, message):

    await message.download(
        file_name="thumbnails/thumb.jpg"
    )

    await message.reply_text(
        "**✅ Thumbnail Saved Successfully**"
    )

# Rename System
@app.on_message(filters.document)
async def rename_file(client, message):

    file = message.document

    old_name = file.file_name

    # Rename Format
    new_name = (
        f"{PREFIX} "
        f"{old_name} "
        f"{SUFFIX}"
    )

    # Queue Add
    QUEUE.append(new_name)

    # Download File
    path = await message.download(
        file_name=f"downloads/{new_name}"
    )

    # Metadata Output
    metadata_path = (
        f"downloads/meta_{new_name}"
    )

    # FFmpeg Metadata
    cmd = [
        "ffmpeg",
        "-i", path,
        "-map", "0",
        "-c", "copy",
        "-metadata",
        "title=Encoded By Rename Bot",
        metadata_path
    ]

    subprocess.run(cmd)

    # Caption
    caption = f"""
**✅ File Renamed Successfully**

**📂 File Name:** `{new_name}`

**⚡ Features Applied**
• Metadata Added
• x265 Tag Added
• Queue Processed

**🤖 Powered By:** @YourBot
"""

    thumb = "thumbnails/thumb.jpg"

    # Upload File
    if os.path.exists(thumb):

        await message.reply_document(
            document=metadata_path,
            thumb=thumb,
            caption=caption
        )

    else:

        await message.reply_document(
            document=metadata_path,
            caption=caption
        )

    # Cleanup
    if os.path.exists(path):
        os.remove(path)

    if os.path.exists(metadata_path):
        os.remove(metadata_path)

    # Queue Remove
    if new_name in QUEUE:
        QUEUE.remove(new_name)

 # Run Telegram Bot
def run_bot():

    import asyncio

    print("✅ Telegram Bot Starting")

    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    app.start()

    print("✅ Telegram Bot Started")

    loop.run_forever()

Thread(
    target=run_bot,
    daemon=True
).start()

# Flask Port
PORT = int(
    os.environ.get("PORT", 10000)
)

print("✅ Bot Started Successfully")
print("✅ Flask Running")

web.run(
    host="0.0.0.0",
    port=PORT
)
