import os
import re
import time
from threading import Thread
from flask import Flask

from pyrogram import Client, filters
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
user_sequence_number = {}
user_autorename = {}
user_prefix = {}
user_suffix = {}
user_metadata = {}

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    txt = f"""
**🤖 Auto Rename Bot Started Successfully**

**Available Commands**

`/prefix` - Set Prefix
`/suffix` - Set Suffix

`/autorename` - Setup Auto Rename
`/sequence` - Start Sequence

`/setcaption` - Set Caption
`/delcaption` - Delete Caption

`/setthumb` - Set Thumbnail
`/delthumb` - Delete Thumbnail

`/metadata` - Set Metadata

`/help` - Help Menu
"""

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔥 Join Channel",
                    url="https://t.me/YOUR_CHANNEL_USERNAME"
                )
            ]
        ]
    )

    await message.reply_text(
        txt,
        reply_markup=buttons
    )

# ================= HELP =================

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):

    await message.reply_text(
"""
**📌 HOW TO USE**

1️⃣ Send File  
2️⃣ Bot Renames Automatically  
3️⃣ Get Renamed File ✅

**📌 SEQUENCE**
`/sequence 157`

**📌 PREFIX**
`/prefix @Team_AC`

**📌 SUFFIX**
`/suffix WEKakashi`

**📌 AUTORENAME**
`/autorename [S{season} - E{episode}] {quality} Naruto`
"""
    )

# ================= PREFIX =================

@bot.on_message(filters.command("prefix"))
async def set_prefix(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/prefix YourPrefix`"
        )

    text = message.text.split(None, 1)[1]

    user_prefix[message.from_user.id] = text

    await message.reply_text(
        f"**✅ Prefix Saved**\n`{text}`"
    )

# ================= SUFFIX =================

@bot.on_message(filters.command("suffix"))
async def set_suffix(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/suffix YourSuffix`"
        )

    text = message.text.split(None, 1)[1]

    user_suffix[message.from_user.id] = text

    await message.reply_text(
        f"**✅ Suffix Saved**\n`{text}`"
    )

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
async def sequence_cmd(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/sequence 157`"
        )

    try:

        start_number = int(message.command[1])

        user_sequence_number[
            message.from_user.id
        ] = start_number

        await message.reply_text(
            f"**✅ Sequence Started From:** `{start_number}`"
        )

    except:

        await message.reply_text(
            "**❌ Invalid Number**"
        )

# ================= AUTORENAME =================

@bot.on_message(filters.command("autorename"))
async def auto_rename(client, message):

    if len(message.command) < 2:

        current = user_autorename.get(
            message.from_user.id,
            "Not Set"
        )

        return await message.reply_text(
f"""
**SETUP AUTO RENAME FORMAT**

Use These Keywords:

✓ `{{season}}`
✓ `{{episode}}`
✓ `{{quality}}`
✓ `{{title}}`
✓ `{{audio}}`
✓ `{{volume}}`
✓ `{{chapter}}`

**Example**
`/autorename [S{{season}} - E{{episode}}] {{quality}} Naruto`

**Current Format**
`{current}`
"""
        )

    format_text = message.text.split(None, 1)[1]

    user_autorename[
        message.from_user.id
    ] = format_text

    await message.reply_text(
        f"**✅ Auto Rename Format Saved**\n\n`{format_text}`"
    )

# ================= CAPTION =================

@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/setcaption Your Caption`"
        )

    caption = message.text.split(None, 1)[1]

    user_caption[
        message.from_user.id
    ] = caption

    await message.reply_text(
        "**✅ Caption Saved**"
    )

@bot.on_message(filters.command("delcaption"))
async def del_caption(client, message):

    user_caption.pop(
        message.from_user.id,
        None
    )

    await message.reply_text(
        "**🗑 Caption Deleted**"
    )

# ================= THUMBNAIL =================

@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):

    await message.reply_text(
        "**📸 Send Thumbnail Photo**"
    )

@bot.on_message(filters.photo)
async def save_thumb(client, message):

    path = await message.download()

    user_thumbnail[
        message.from_user.id
    ] = path

    await message.reply_text(
        "**✅ Thumbnail Saved**"
    )

@bot.on_message(filters.command("delthumb"))
async def del_thumb(client, message):

    thumb = user_thumbnail.get(
        message.from_user.id
    )

    if thumb and os.path.exists(thumb):
        os.remove(thumb)

    user_thumbnail.pop(
        message.from_user.id,
        None
    )

    await message.reply_text(
        "**🗑 Thumbnail Deleted**"
    )

# ================= METADATA =================

@bot.on_message(filters.command("metadata"))
async def metadata_cmd(client, message):

    if len(message.command) < 2:

        current = user_metadata.get(
            message.from_user.id,
            "Not Set"
        )

        return await message.reply_text(
f"""
**📀 Metadata Setup**

Usage:
`/metadata Team AC Encodes`

Current Metadata:
`{current}`
"""
        )

    text = message.text.split(None, 1)[1]

    user_metadata[
        message.from_user.id
    ] = text

    await message.reply_text(
        f"**✅ Metadata Saved**\n`{text}`"
    )

# ================= AUTO RENAME =================

@bot.on_message(filters.document | filters.video | filters.audio)
async def rename_file(client, message):

    file = (
        message.document
        or message.video
        or message.audio
    )

    old_name = file.file_name

    # ===== TITLE =====

    title = old_name.replace(".", " ")

    # ===== DETECT =====

    season = "01"
    episode = "01"
    quality = "720p"
    audio = "Multi Audio"
    volume = "01"
    chapter = "01"

    season_match = re.search(r"S(\d+)", old_name, re.I)
    episode_match = re.search(r"E(\d+)", old_name, re.I)
    quality_match = re.search(r"(\d{3,4}p)", old_name, re.I)

    if season_match:
        season = season_match.group(1)

    if episode_match:
        episode = episode_match.group(1)

    if quality_match:
        quality = quality_match.group(1)

    # ===== AUTORENAME =====

    rename_format = user_autorename.get(
        message.from_user.id
    )

    if rename_format:

        new_name = rename_format \
            .replace("{season}", season) \
            .replace("{episode}", episode) \
            .replace("{quality}", quality) \
            .replace("{title}", title) \
            .replace("{audio}", audio) \
            .replace("{volume}", volume) \
            .replace("{chapter}", chapter)

    else:

        new_name = old_name

    # ===== PREFIX =====

    prefix = user_prefix.get(
        message.from_user.id,
        ""
    )

    suffix = user_suffix.get(
        message.from_user.id,
        ""
    )

    new_name = f"{prefix} {new_name} {suffix}".strip()

    # ===== SEQUENCE =====

    current_number = user_sequence_number.get(
        message.from_user.id
    )

    if current_number is not None:

        new_name = f"[{current_number}] {new_name}"

        user_sequence_number[
            message.from_user.id
        ] += 1

    # ===== EXTENSION =====

    ext = os.path.splitext(old_name)[1]

    if not new_name.endswith(ext):
        new_name += ext

    # ===== DOWNLOAD =====

    msg = await message.reply_text(
        "**⬇️ Downloading File...**"
    )

    downloaded = await message.download(
        file_name=new_name
    )

    await msg.edit(
        "**⬆️ Uploading File...**"
    )

    # ===== CAPTION =====

    caption = user_caption.get(
        message.from_user.id,
        f"**✅ Renamed Successfully**\n\n`{new_name}`"
    )

    # ===== THUMB =====

    thumb = user_thumbnail.get(
        message.from_user.id
    )

    # ===== METADATA =====

    metadata_text = user_metadata.get(
        message.from_user.id,
        "Auto Rename Bot"
    )

    # ===== UPLOAD =====

    await message.reply_document(
        document=downloaded,
        caption=caption,
        thumb=thumb,
        file_name=new_name
    )

    await msg.delete()

    # ===== DELETE LOCAL FILE =====

    if os.path.exists(downloaded):
        os.remove(downloaded)

# ================= RUN =================

print("✅ Bot Started Successfully")

bot.run()
