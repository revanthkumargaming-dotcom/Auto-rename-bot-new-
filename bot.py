import os
import time
import random
from flask import Flask
from threading import Thread

from pyrogram import Client, filters

from config import *

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Is Running Successfully ✅"

Thread(target=lambda: app.run(host="0.0.0.0", port=8080)).start()

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
user_caption = {}
user_font = {}
user_metadata = {}
user_thumbnail = {}

sequence_mode = {}
sequence_files = {}

# ================= PROGRESS BAR =================

async def progress_bar(current, total, message, start, text):
    try:
        now = time.time()
        diff = now - start

        if diff == 0:
            return

        speed = current / diff
        percentage = current * 100 / total

        bar = int((current / total) * 10) * "█" + (10 - int((current / total) * 10)) * "░"

        await message.edit(
            f"{text}\n\n[{bar}]\n"
            f"📊 {percentage:.1f}%\n"
            f"⚡ {speed/1024/1024:.2f} MB/s"
        )
    except:
        pass

# ================= HELP =================

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):
    await message.reply_text(HELP_TEXT)

# ================= SETTINGS =================

@bot.on_message(filters.command("prefix"))
async def prefix_cmd(client, message):
    user_prefix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Prefix Saved")

@bot.on_message(filters.command("suffix"))
async def suffix_cmd(client, message):
    user_suffix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Suffix Saved")

@bot.on_message(filters.command("autorename"))
async def autorename_cmd(client, message):
    user_autorename[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Autorename Saved")

@bot.on_message(filters.command("metadata"))
async def metadata_cmd(client, message):
    user_metadata[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Metadata Saved")

# ================= THUMB =================

@bot.on_message(filters.photo)
async def save_thumb(client, message):
    path = await message.download()
    user_thumbnail[message.from_user.id] = path
    await message.reply_text("Thumbnail Saved")

# ================= START =================

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    photo = random.choice(START_PICS)

    await message.reply_photo(
        photo=photo,
        caption=START_TEXT.format(mention=message.from_user.mention)
    )

# ================= MAIN FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):

    user_id = message.from_user.id

    # sequence
    if sequence_mode.get(user_id):
        sequence_files.setdefault(user_id, []).append(message)
        return await message.reply_text("Added to sequence")

    status = await message.reply_text("Downloading...")

    file_path = await message.download()

    base = os.path.basename(file_path)

    # rename logic
    prefix = user_prefix.get(user_id, "")
    suffix = user_suffix.get(user_id, "")
    auto = user_autorename.get(user_id)

    if auto:
        new_name = auto.replace("{filename}", base)
    else:
        new_name = f"{prefix}{base}{suffix}"

    # caption
    caption = new_name

    meta = user_metadata.get(user_id)
    if meta:
        caption += f"\n\n📌 {meta}"

    # upload
    await message.reply_document(
        document=file_path,
        file_name=new_name,
        caption=caption
    )

    await status.delete()

    if os.path.exists(file_path):
        os.remove(file_path)

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
async def seq_start(client, message):
    sequence_mode[message.from_user.id] = True
    sequence_files[message.from_user.id] = []
    await message.reply_text("Sequence Started")

@bot.on_message(filters.command("endsequence"))
async def seq_end(client, message):
    uid = message.from_user.id

    for msg in sequence_files.get(uid, []):
        await message.reply_document(msg.document.file_id)

    sequence_mode[uid] = False
    sequence_files[uid] = []

    await message.reply_text("Sequence Ended")

# ================= RUN =================

print("Bot Started Successfully")
bot.run()
