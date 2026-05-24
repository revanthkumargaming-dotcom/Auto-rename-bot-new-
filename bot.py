import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import API_ID, API_HASH, BOT_TOKEN

# Create folders
os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

# Queue
QUEUE = []

app = Client(
    "renamebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START MESSAGE
@app.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("⚙ Settings", callback_data="settings")],
        [InlineKeyboardButton("📢 Updates", url="https://t.me/yourchannel")]
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
• Custom Buttons
"""

    await message.reply_text(
        text,
        reply_markup=buttons
    )

# PREFIX COMMAND
PREFIX = "@MovieHub"
SUFFIX = "x265"

@app.on_message(filters.command("setprefix"))
async def setprefix(client, message):

    global PREFIX

    try:
        PREFIX = message.text.split(None, 1)[1]

        await message.reply_text(
            f"**✅ Prefix Saved:** `{PREFIX}`"
        )

    except:
        await message.reply_text(
            "**Usage:** `/setprefix text`"
        )

# SUFFIX COMMAND
@app.on_message(filters.command("setsuffix"))
async def setsuffix(client, message):

    global SUFFIX

    try:
        SUFFIX = message.text.split(None, 1)[1]

        await message.reply_text(
            f"**✅ Suffix Saved:** `{SUFFIX}`"
        )

    except:
        await message.reply_text(
            "**Usage:** `/setsuffix text`"
        )

# SAVE THUMBNAIL
@app.on_message(filters.photo)
async def save_thumb(client, message):

    await message.download(
        file_name="thumbnails/thumb.jpg"
    )

    await message.reply_text(
        "**✅ Thumbnail Saved Successfully**"
    )

# MAIN RENAME SYSTEM
@app.on_message(filters.document)
async def rename_file(client, message):

    file = message.document

    old_name = file.file_name

    # Rename format
    new_name = f"{PREFIX} {old_name} {SUFFIX}"

    # Queue add
    QUEUE.append(new_name)

    # Download
    path = await message.download(
        file_name=f"downloads/{new_name}"
    )

    # Metadata output
    metadata_path = f"downloads/meta_{new_name}"

    # FFmpeg metadata
    cmd = [
        "ffmpeg",
        "-i", path,
        "-map", "0",
        "-c", "copy",
        "-metadata", "title=Encoded By Rename Bot",
        metadata_path
    ]

    subprocess.run(cmd)

    # Bold caption
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
    os.remove(path)
    os.remove(metadata_path)

    # Queue remove
    QUEUE.remove(new_name)

# BOT START
print("✅ Bot Started Successfully")

app.run()
