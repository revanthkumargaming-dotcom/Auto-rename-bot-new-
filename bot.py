import os
import re
import time
from threading import Thread
from flask import Flask
from config import START_PIC   # ✅ only import here
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
user_autorename = {}
user_prefix = {}
user_suffix = {}
user_metadata = {}
user_font = {}

sequence_mode = {}
sequence_files = {}

# ================= PROGRESS BAR =================

async def progress_bar(
    current,
    total,
    message,
    start,
    text
):

    now = time.time()
    diff = now - start

    if diff == 0:
        return

    percentage = current * 100 / total
    speed = current / diff

    remaining_time = round(
        (total - current) / speed
    ) if speed > 0 else 0

    bar_length = 20

    filled_length = int(
        bar_length * current // total
    )

    bar = "█" * filled_length + "░" * (
        bar_length - filled_length
    )

    uploaded = current / 1024 / 1024
    total_size = total / 1024 / 1024
    speed_mb = speed / 1024 / 1024

    txt = f"""
{text}

[{bar}]

**📊 Progress :** `{percentage:.1f}%`
**⚡ Speed :** `{speed_mb:.2f} MB/s`
**📥 Done :** `{uploaded:.2f} MB`
**🗂 Total :** `{total_size:.2f} MB`
**⏳ ETA :** `{remaining_time} sec`
"""

    try:
        await message.edit(txt)
    except:
        pass

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    txt = """
**🤖 AUTO RENAME BOT**

**Available Commands**

`/prefix`
`/suffix`

`/autorename`

`/sequence`
`/endsequence`

`/customfont`
`/font`

`/setcaption`
`/delcaption`

`/setthumb`
`/delthumb`

`/metadata`

`/help`
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

    await message.reply_photo(
        photo=START_PIC,
        caption=txt,
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

**📌 PREFIX**
`/prefix @Buster_ofcl`

**📌 SUFFIX**
`/suffix WEKakashi`

**📌 AUTORENAME**
`/autorename [S{season} - E{episode}] {quality}`

**📌 SEQUENCE**
`/sequence`
Send Files
`/endsequence`

**📌 CUSTOM FONT**
`/customfont`
"""
    )

# ================= PREFIX =================

@bot.on_message(filters.command("prefix"))
async def set_prefix(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/prefix text`"
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
            "**Usage:** `/suffix text`"
        )

    text = message.text.split(None, 1)[1]

    user_suffix[message.from_user.id] = text

    await message.reply_text(
        f"**✅ Suffix Saved**\n`{text}`"
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

    format_text = message.text.split(
        None,
        1
    )[1]

    user_autorename[
        message.from_user.id
    ] = format_text

    await message.reply_text(
        "**✅ Auto Rename Format Saved**"
    )

# ================= CUSTOM FONT =================

@bot.on_message(filters.command("customfont"))
async def custom_font(client, message):

    txt = """
**🎨 Select Font**

`/font bold`
`/font italic`
`/font mono`
`/font normal`
"""

    await message.reply_text(txt)

@bot.on_message(filters.command("font"))
async def set_font(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/font bold`"
        )

    font = message.command[1].lower()

    fonts = [
        "bold",
        "italic",
        "mono",
        "normal"
    ]

    if font not in fonts:
        return await message.reply_text(
            "**❌ Invalid Font**"
        )

    user_font[
        message.from_user.id
    ] = font

    await message.reply_text(
        f"**✅ Font Changed To:** `{font}`"
    )

# ================= CAPTION =================

@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** `/setcaption text`"
        )

    caption = message.text.split(
        None,
        1
    )[1]

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

# ================= THUMB =================

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
        return await message.reply_text(
            "**Usage:** `/metadata text`"
        )

    text = message.text.split(
        None,
        1
    )[1]

    user_metadata[
        message.from_user.id
    ] = text

    await message.reply_text(
        f"**✅ Metadata Saved**\n`{text}`"
    )

# ================= SEQUENCE START =================

@bot.on_message(filters.command("sequence"))
async def start_sequence(client, message):

    sequence_mode[
        message.from_user.id
    ] = True

    sequence_files[
        message.from_user.id
    ] = []

    await message.reply_text(
        "**✅ Sequence Mode Started\n\nSend Files Now**"
    )

# ================= END SEQUENCE =================

@bot.on_message(filters.command("endsequence"))
async def end_sequence(client, message):

    user_id = message.from_user.id

    if user_id not in sequence_files:
        return await message.reply_text(
            "**❌ Sequence Not Started**"
        )

    files = sequence_files[user_id]

    if len(files) == 0:
        return await message.reply_text(
            "**❌ No Files Added**"
        )

    # ===== SORT =====

    def extract_number(name):

        match = re.search(
            r'(?:E|EP|Episode)[ ._-]*(\d+)',
            name,
            re.IGNORECASE
        )

        if match:
            return int(match.group(1))

        nums = re.findall(r'\d+', name)

        if nums:
            return int(nums[0])

        return 0

    files.sort(
        key=lambda msg: extract_number(
            (
                msg.document.file_name
                if msg.document
                else msg.video.file_name
            )
        )
    )

    # ===== SEND =====

    for msg_data in files:

        await bot.copy_message(
            chat_id=message.chat.id,
            from_chat_id=msg_data.chat.id,
            message_id=msg_data.id
        )

    # ===== RESET =====

    sequence_mode[user_id] = False
    sequence_files[user_id] = []

    await message.reply_text(
        "**✅ Done**"
    )

# ================= PROCESS FILE =================

async def process_file(
    message,
    reply_message
):

    file = (
        message.document
        or message.video
        or message.audio
    )

    old_name = file.file_name

    title = old_name.replace(
        ".",
        " "
    )

    season = "01"
    episode = "01"
    quality = "720p"
    audio = "Multi Audio"
    volume = "01"
    chapter = "01"

    season_match = re.search(
        r"S(\d+)",
        old_name,
        re.I
    )

    episode_match = re.search(
        r"E(\d+)",
        old_name,
        re.I
    )

    quality_match = re.search(
        r"(\d{3,4}p)",
        old_name,
        re.I
    )

    if season_match:
        season = season_match.group(1)

    if episode_match:
        episode = episode_match.group(1)

    if quality_match:
        quality = quality_match.group(1)

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

    prefix = user_prefix.get(
        message.from_user.id,
        ""
    )

    suffix = user_suffix.get(
        message.from_user.id,
        ""
    )

    new_name = f"{prefix} {new_name} {suffix}".strip()

    ext = os.path.splitext(
        old_name
    )[1]

    if not new_name.endswith(ext):
        new_name += ext

    font = user_font.get(
        message.from_user.id,
        "mono"
    )

    custom_caption = user_caption.get(
        message.from_user.id
    )

    if custom_caption:

        final_caption = custom_caption

    else:

        if font == "bold":
            final_caption = f"**{new_name}**"

        elif font == "italic":
            final_caption = f"__{new_name}__"

        elif font == "mono":
            final_caption = f"`{new_name}`"

        else:
            final_caption = new_name

    msg = await reply_message.reply_text(
        "**🚀 Starting Process...**"
    )

    start_time = time.time()

    downloaded = await message.download(
        file_name=new_name,
        progress=progress_bar,
        progress_args=(
            msg,
            start_time,
            "⬇️ Downloading..."
        )
    )

    thumb = user_thumbnail.get(
        message.from_user.id
    )

    start_time = time.time()

    await reply_message.reply_document(
        document=downloaded,
        caption=final_caption,
        thumb=thumb,
        file_name=new_name,
        progress=progress_bar,
        progress_args=(
            msg,
            start_time,
            "⬆️ Uploading..."
        )
    )

    await msg.delete()

    if os.path.exists(downloaded):
        os.remove(downloaded)

# ================= MAIN HANDLER =================

@bot.on_message(
    filters.document
    | filters.video
    | filters.audio
)
async def rename_file(client, message):

    if sequence_mode.get(
        message.from_user.id
    ):

        sequence_files[
            message.from_user.id
        ].append(message)

        return await message.reply_text(
            "**📥 File Added To Queue**"
        )

    await process_file(
        message,
        message
    )

# ================= RUN =================

print("✅ Bot Started Successfully")

bot.run()
