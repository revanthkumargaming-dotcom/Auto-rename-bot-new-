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

def run():
    app.run(host="0.0.0.0", port=8080)

Thread(target=run).start()

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
user_font = {}
user_metadata = {}

sequence_mode = {}
sequence_files = {}

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

# ================= PREFIX =================
@bot.on_message(filters.command("prefix"))
async def prefix_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /prefix text")

    user_prefix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Prefix saved ✅")

# ================= SUFFIX =================
@bot.on_message(filters.command("suffix"))
async def suffix_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /suffix text")

    user_suffix[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Suffix saved ✅")

# ================= AUTORENAME =================
@bot.on_message(filters.command("autorename"))
async def autorename_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /autorename {filename}")

    user_autorename[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("AutoRename saved ✅")

# ================= FONT =================
@bot.on_message(filters.command("font"))
async def font_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("/font bold | italic | mono | normal")

    user_font[message.from_user.id] = message.command[1].lower()
    await message.reply_text("Font updated ✅")

# ================= METADATA =================
@bot.on_message(filters.command("metadata"))
async def metadata_cmd(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /metadata text")

    user_metadata[message.from_user.id] = message.text.split(None, 1)[1]
    await message.reply_text("Metadata saved ✅")

# ================= SEQUENCE =================
@bot.on_message(filters.command("sequence"))
async def seq_start(client, message):
    uid = message.from_user.id
    sequence_mode[uid] = True
    sequence_files[uid] = []
    await message.reply_text("Sequence ON ✅")

@bot.on_message(filters.command("endsequence"))
async def seq_end(client, message):
    uid = message.from_user.id

    files = sequence_files.get(uid, [])
    if not files:
        return await message.reply_text("No files ❌")

    for m in files:
        await bot.copy_message(message.chat.id, m.chat.id, m.id)

    sequence_mode[uid] = False
    sequence_files[uid] = []
    await message.reply_text("Sequence Done ✅")

# ================= FILE HANDLER =================
@bot.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):

    uid = message.from_user.id

    # sequence mode
    if sequence_mode.get(uid):
        sequence_files.setdefault(uid, []).append(message)
        return await message.reply_text("Added to sequence 📥")

    file_path = await message.download()
    base = os.path.basename(file_path)

    prefix = user_prefix.get(uid, "")
    suffix = user_suffix.get(uid, "")
    font = user_font.get(uid, "normal")
    meta = user_metadata.get(uid, "")
    auto = user_autorename.get(uid)

    # rename logic
    if auto:
        new_name = auto.replace("{filename}", base)
    else:
        new_name = f"{prefix}{base}{suffix}"

    # font style
    if font == "bold":
        new_name = f"**{new_name}**"
    elif font == "italic":
        new_name = f"__{new_name}__"
    elif font == "mono":
        new_name = f"`{new_name}`"

    caption = new_name
    if meta:
        caption += f"\n\n{meta}"

    thumb = user_thumbnail.get(uid)

    status = await message.reply_text("Uploading...")

    await message.reply_document(
        document=file_path,
        file_name=base,
        caption=caption,
        thumb=thumb if thumb else None
    )

    await status.delete()

    if os.path.exists(file_path):
        os.remove(file_path)

# ================= RUN =================
print("Bot Started 🚀")

bot.run()
