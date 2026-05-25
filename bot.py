import os
import asyncio
import threading
import subprocess

from flask import Flask

from pyrogram import Client, filters, idle
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ================= CONFIG =================

API_ID = "20879824"
API_HASH = "5f70a9a12a4bb8cc322bed62bc6007ce"
BOT_TOKEN = "8849121451:AAEu-1_X1Y-j8jjmt1nyRtuUIvxpavnd-Zk"

OWNER_ID = "7340960697"

PREFIX = "MovieHub"
SUFFIX = "x265"

# ================= CREATE FOLDERS =================

os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

# ================= FLASK =================

web = Flask(__name__)

@web.route("/")
def home():
    return "🔥 Auto Rename Bot Running Successfully"

def run_flask():

    port = int(os.environ.get("PORT", 10000))

    web.run(
        host="0.0.0.0",
        port=port
    )

# ================= TELEGRAM BOT =================

bot = Client(
    "renamebot",
    api_id =  "20879824",
    api_hash =  "5f70a9a12a4bb8cc322bed62bc6007ce",
    bot_token = "8849121451:AAEu-1_X1Y-j8jjmt1nyRtuUIvxpavnd-Zk"
)

QUEUE = []

# ================= START =================

@bot.on_message(filters.command("start"))
async def start_handler(client, message):

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 Updates",
                url="https://t.me/yourchannel"
            )
        ]
    ])

    text = f"""
🔥 AUTO RENAME BOT

✅ Bot Status : Active
✅ Prefix : `{PREFIX}`
✅ Suffix : `{SUFFIX}`

📂 Send Any File To Rename
"""

    await message.reply_text(
        text,
        reply_markup=buttons
    )

# ================= HELP =================

@bot.on_message(filters.command("help"))
async def help_handler(client, message):

    text = """
📌 COMMANDS

/setprefix text
→ Set Prefix

/setsuffix text
→ Set Suffix

📂 Send Photo
→ Save Thumbnail

📂 Send File
→ Auto Rename
"""

    await message.reply_text(text)

# ================= SET PREFIX =================

@bot.on_message(filters.command("setprefix"))
async def setprefix_handler(client, message):

    global PREFIX

    try:

        PREFIX = message.text.split(None, 1)[1]

        await message.reply_text(
            f"✅ Prefix Saved\n\n`{PREFIX}`"
        )

    except:

        await message.reply_text(
            "❌ Usage:\n/setprefix MovieHub"
        )

# ================= SET SUFFIX =================

@bot.on_message(filters.command("setsuffix"))
async def setsuffix_handler(client, message):

    global SUFFIX

    try:

        SUFFIX = message.text.split(None, 1)[1]

        await message.reply_text(
            f"✅ Suffix Saved\n\n`{SUFFIX}`"
        )

    except:

        await message.reply_text(
            "❌ Usage:\n/setsuffix x265"
        )

# ================= SAVE THUMBNAIL =================

@bot.on_message(filters.photo)
async def thumbnail_handler(client, message):

    await message.download(
        file_name="thumbnails/thumb.jpg"
    )

    await message.reply_text(
        "✅ Thumbnail Saved Successfully"
    )

# ================= RENAME SYSTEM =================

@bot.on_message(filters.document)
async def rename_handler(client, message):

    file = message.document

    old_name = file.file_name

    safe_name = old_name.replace("/", "_")

    new_name = f"{PREFIX} {safe_name} {SUFFIX}"

    QUEUE.append(new_name)

    wait_msg = await message.reply_text(
        "⏳ Downloading File..."
    )

    # Download

    download_path = await message.download(
        file_name=f"downloads/{safe_name}"
    )

    output_path = f"downloads/{new_name}"

    await wait_msg.edit_text(
        "⚡ Adding Metadata..."
    )

    # FFmpeg Metadata

    cmd = [
        "ffmpeg",
        "-i", download_path,
        "-map", "0",
        "-c", "copy",
        "-metadata", f"title={new_name}",
        output_path,
        "-y"
    ]

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    await wait_msg.edit_text(
        "📤 Uploading File..."
    )

    caption = f"""
🔥 FILE RENAMED SUCCESSFULLY

📂 File Name :
`{new_name}`

⚡ Features Applied
• Metadata Added
• Prefix Added
• Suffix Added
• Queue Processed

🤖 Powered By Auto Rename Bot
"""

    thumb = "thumbnails/thumb.jpg"

    try:

        if os.path.exists(thumb):

            await message.reply_document(
                document=output_path,
                thumb=thumb,
                caption=caption
            )

        else:

            await message.reply_document(
                document=output_path,
                caption=caption
            )

    except Exception as e:

        await message.reply_text(
            f"❌ Upload Error\n\n{e}"
        )

    # Cleanup

    try:

        if os.path.exists(download_path):
            os.remove(download_path)

        if os.path.exists(output_path):
            os.remove(output_path)

    except:
        pass

    if new_name in QUEUE:
        QUEUE.remove(new_name)

    await wait_msg.delete()

# ================= OWNER ONLY =================

@bot.on_message(filters.command("queue"))
async def queue_handler(client, message):

    if message.from_user.id != OWNER_ID:
        return

    text = f"📂 Queue Files : {len(QUEUE)}"

    await message.reply_text(text)

# ================= MAIN =================

async def main():

    print("🚀 Starting Bot...")

    await bot.start()

    print("✅ Bot Started Successfully")

    await idle()

    await bot.stop()

# ================= RUN =================

if __name__ == "__main__":

    threading.Thread(
        target=run_flask,
        daemon=True
    ).start()

    asyncio.run(main())
