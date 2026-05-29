import os
import re
import time
from threading import Thread
from flask import Flask
from pyrogram import Client, filters
import plugins.start
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from config import *

# ================= FLASK SERVER =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Is Running Successfully ✅"

def run_web():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run_web).start()

# ================= BOT =================

bot = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= STORAGE =================

user_caption = {}
user_thumbnail = {}
user_autorename = {}
user_prefix = {}
user_suffix = {}
user_metadata = {}
user_font = {}

sequence_mode = {}
sequence_files = {}

# ================= PROGRESS BAR =================

async def progress_bar(current, total, message, start, text):

    now = time.time()
    diff = now - start

    if diff == 0:
        return

    percentage = current * 100 / total
    speed = current / diff

    remaining_time = round((total - current) / speed) if speed > 0 else 0

    bar_length = 20
    filled_length = int(bar_length * current // total)

    bar = "█" * filled_length + "░" * (bar_length - filled_length)

    uploaded = current / 1024 / 1024
    total_size = total / 1024 / 1024
    speed_mb = speed / 1024 / 1024

    txt = f"""
{text}

[{bar}]

📊 Progress : {percentage:.1f}%
⚡ Speed : {speed_mb:.2f} MB/s
📥 Done : {uploaded:.2f} MB
🗂 Total : {total_size:.2f} MB
⏳ ETA : {remaining_time} sec
"""

    try:
        await message.edit(txt)
    except:
        pass

# ================= PREFIX =================

@bot.on_message(filters.command("prefix"))
async def set_prefix(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /prefix text")

    text = message.text.split(None, 1)[1]
    user_prefix[message.from_user.id] = text

    await message.reply_text(f"✅ Prefix Saved\n{text}")

# ================= SUFFIX =================

@bot.on_message(filters.command("suffix"))
async def set_suffix(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /suffix text")

    text = message.text.split(None, 1)[1]
    user_suffix[message.from_user.id] = text

    await message.reply_text(f"✅ Suffix Saved\n{text}")

# ================= AUTORENAME =================

@bot.on_message(filters.command("autorename"))
async def auto_rename(client, message):

    if len(message.command) < 2:
        current = user_autorename.get(message.from_user.id, "Not Set")

        return await message.reply_text(f"""
SETUP AUTO RENAME FORMAT

Current: {current}
""")

    format_text = message.text.split(None, 1)[1]
    user_autorename[message.from_user.id] = format_text

    await message.reply_text("✅ Auto Rename Format Saved")

# ================= CUSTOM FONT =================

@bot.on_message(filters.command("customfont"))
async def custom_font(client, message):

    await message.reply_text("""
🎨 Select Font

/font bold
/font italic
/font mono
/font normal
""")

@bot.on_message(filters.command("font"))
async def set_font(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /font bold")

    font = message.command[1].lower()

    if font not in ["bold", "italic", "mono", "normal"]:
        return await message.reply_text("❌ Invalid Font")

    user_font[message.from_user.id] = font

    await message.reply_text(f"✅ Font Changed To: {font}")

# ================= CAPTION =================

@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /setcaption text")

    caption = message.text.split(None, 1)[1]
    user_caption[message.from_user.id] = caption

    await message.reply_text("✅ Caption Saved")

@bot.on_message(filters.command("delcaption"))
async def del_caption(client, message):

    user_caption.pop(message.from_user.id, None)

    await message.reply_text("🗑 Caption Deleted")

# ================= THUMB =================

@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):
    await message.reply_text("📸 Send Thumbnail Photo")

@bot.on_message(filters.photo)
async def save_thumb(client, message):

    path = await message.download()
    user_thumbnail[message.from_user.id] = path

    await message.reply_text("✅ Thumbnail Saved")

@bot.on_message(filters.command("delthumb"))
async def del_thumb(client, message):

    thumb = user_thumbnail.get(message.from_user.id)

    if thumb and os.path.exists(thumb):
        os.remove(thumb)

    user_thumbnail.pop(message.from_user.id, None)

    await message.reply_text("🗑 Thumbnail Deleted")

# ================= METADATA =================

@bot.on_message(filters.command("metadata"))
async def metadata_cmd(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Usage: /metadata text")

    text = message.text.split(None, 1)[1]
    user_metadata[message.from_user.id] = text

    await message.reply_text(f"✅ Metadata Saved\n{text}")

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
async def start_sequence(client, message):

    user_id = message.from_user.id
    sequence_mode[user_id] = True
    sequence_files[user_id] = []

    await message.reply_text("✅ Sequence Mode Started")

@bot.on_message(filters.command("endsequence"))
async def end_sequence(client, message):

    user_id = message.from_user.id
    files = sequence_files.get(user_id, [])

    if len(files) == 0:
        return await message.reply_text("❌ No Files Added")

    for msg_data in files:
        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=msg_data.chat.id,
            message_id=msg_data.id
        )

    sequence_mode[user_id] = False
    sequence_files[user_id] = []

    await message.reply_text("✅ Done")

# ================= FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def rename_file(client, message):

    user_id = message.from_user.id

    if sequence_mode.get(user_id):
        sequence_files[user_id].append(message)
        return await message.reply_text("📥 File Added")

    file = await message.download()
    base = os.path.basename(file)

    prefix = user_prefix.get(user_id, "")
    suffix = user_suffix.get(user_id, "")
    font = user_font.get(user_id, "normal")

    new_name = f"{prefix} RENAMED_{base} {suffix}".strip()

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
