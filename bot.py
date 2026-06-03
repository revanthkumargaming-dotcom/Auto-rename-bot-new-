import os
import time
import random
from threading import Thread
from flask import Flask
from pyrogram import Client, filters

from config import *

# ================= FLASK =================

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Running ✅"

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

# ================= AUTH =================

AUTH_USERS = set([ADMIN])  # add more IDs if needed

def is_auth(user_id):
    return user_id in AUTH_USERS

# ================= STORAGE =================

user_prefix = {}
user_suffix = {}
user_font = {}
user_caption = {}
user_metadata = {}
user_autorename = {}
user_thumbnail = {}

sequence_mode = {}
sequence_files = {}

# ================= PROGRESS =================

async def progress(current, total, message, start, text):
    now = time.time()
    diff = now - start

    if diff == 0:
        return

    percent = current * 100 / total
    speed = current / diff
    eta = int((total - current) / speed) if speed else 0

    bar_len = 12
    filled = int(bar_len * current / total)

    bar = "█" * filled + "░" * (bar_len - filled)

    try:
        await message.edit(
            f"{text}\n[{bar}] {percent:.1f}%\n⚡ {speed/1024/1024:.2f} MB/s | ETA {eta}s"
        )
    except:
        pass

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    photo = random.choice(START_PICS)

    await message.reply_photo(
        photo=photo,
        caption=START_TEXT.format(
            mention=message.from_user.mention
        )
    )

# ================= AUTH DECORATOR =================

def auth_required(func):
    async def wrapper(client, message):
        if not is_auth(message.from_user.id):
            return await message.reply_text("❌ Not authorised")
        return await func(client, message)
    return wrapper

# ================= SETTINGS =================

@bot.on_message(filters.command("prefix"))
@auth_required
async def prefix(client, message):
    user_prefix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Prefix saved")

@bot.on_message(filters.command("suffix"))
@auth_required
async def suffix(client, message):
    user_suffix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Suffix saved")

@bot.on_message(filters.command("autorename"))
@auth_required
async def autorename(client, message):
    user_autorename[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ AutoRename saved")

@bot.on_message(filters.command("metadata"))
@auth_required
async def metadata(client, message):
    user_metadata[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("✅ Metadata saved")

# ================= THUMB =================

@bot.on_message(filters.photo)
@auth_required
async def save_thumb(client, message):
    path = await message.download()
    user_thumbnail[message.from_user.id] = path
    await message.reply_text("✅ Thumbnail saved")

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
@auth_required
async def start_seq(client, message):

    uid = message.from_user.id
    sequence_mode[uid] = True
    sequence_files[uid] = []

    await message.reply_text("📥 Sequence started")

@bot.on_message(filters.command("endsequence"))
@auth_required
async def end_seq(client, message):

    uid = message.from_user.id
    files = sequence_files.get(uid, [])

    if not files:
        return await message.reply_text("❌ No files")

    await message.reply_text("📤 Sending sequence...")

    for msg in files:
        try:
            f = await msg.download()
            await message.reply_document(f)
            if os.path.exists(f):
                os.remove(f)
        except:
            pass

    sequence_mode[uid] = False
    sequence_files[uid] = []

    await message.reply_text("✅ Done")

# ================= FILE HANDLER =================

@bot.on_message(filters.document | filters.video | filters.audio)
@auth_required
async def rename(client, message):

    uid = message.from_user.id

    # sequence check
    if sequence_mode.get(uid):
        sequence_files.setdefault(uid, []).append(message)
        return await message.reply_text("📥 Added to sequence")

    status = await message.reply_text("📥 Downloading...")

    file = await message.download(
        progress=progress,
        progress_args=(status, time.time(), "📥 Downloading")
    )

    base = os.path.basename(file)

    prefix = user_prefix.get(uid, "")
    suffix = user_suffix.get(uid, "")
    rename = user_autorename.get(uid)

    if rename:
        new_name = rename.replace("{filename}", base)
    else:
        new_name = f"{prefix}{base}{suffix}"

    caption = new_name + "\n" + (user_metadata.get(uid) or "")

    await status.edit("📤 Uploading...")

    await message.reply_document(
        document=file,
        file_name=new_name,
        caption=caption
    )

    await status.delete()

    if os.path.exists(file):
        os.remove(file)

# ================= RUN =================

print("🚀 Bot Started")
bot.run()
