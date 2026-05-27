import os
import time
from pyrogram import Client, filters
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from dotenv import load_dotenv

load_dotenv()

# ================= IMPORT CONFIG =================

from config import *

# ================================================

bot = Client(
    "AutoRenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= STORAGE =================

user_caption = {}
user_thumbnail = {}
user_sequence = {}

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔥 Join Channel",
                    url=f"https://t.me/{FORCE_SUB_CHANNEL}"
                )
            ]
        ]
    )

    try:
        member = await bot.get_chat_member(
            FORCE_SUB_CHANNEL,
            message.from_user.id
        )

        if member.status in ["left", "kicked"]:
            return await message.reply_text(
                "**⚠️ First Join Our Channel To Use Bot**",
                reply_markup=buttons
            )

    except:
        return await message.reply_text(
            "**⚠️ Join Channel First**",
            reply_markup=buttons
        )

    txt = f"""
**🤖 {BOT_NAME} Started Successfully**

**Available Commands**

`/setcaption` - Set Caption  
`/delcaption` - Delete Caption  

`/setthumb` - Set Thumbnail  
`/delthumb` - Delete Thumbnail  

`/sequence on` - Enable Sequence  
`/sequence off` - Disable Sequence  

`/help` - Help Menu
"""

    await message.reply_text(txt)

# ================= HELP =================

@bot.on_message(filters.command("help"))
async def help_cmd(client, message):

    await message.reply_text(
        """
**📌 How To Use**

1️⃣ Send Any File  
2️⃣ Bot Will Auto Rename  
3️⃣ Receive Renamed File ✅
"""
    )

# ================= CAPTION =================

@bot.on_message(filters.command("setcaption"))
async def set_caption(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n`/setcaption Your Caption`"
        )

    caption = message.text.split(None, 1)[1]

    user_caption[message.from_user.id] = caption

    await message.reply_text(
        "**✅ Caption Saved Successfully**"
    )

@bot.on_message(filters.command("delcaption"))
async def del_caption(client, message):

    user_caption.pop(message.from_user.id, None)

    await message.reply_text(
        "**🗑 Caption Deleted Successfully**"
    )

# ================= THUMBNAIL =================

@bot.on_message(filters.command("setthumb"))
async def set_thumb(client, message):

    await message.reply_text(
        "**📸 Send Thumbnail Photo Now**"
    )

@bot.on_message(filters.photo)
async def save_thumb(client, message):

    path = await message.download()

    user_thumbnail[message.from_user.id] = path

    await message.reply_text(
        "**✅ Thumbnail Saved Successfully**"
    )

@bot.on_message(filters.command("delthumb"))
async def del_thumb(client, message):

    thumb = user_thumbnail.get(message.from_user.id)

    if thumb and os.path.exists(thumb):
        os.remove(thumb)

    user_thumbnail.pop(message.from_user.id, None)

    await message.reply_text(
        "**🗑 Thumbnail Deleted Successfully**"
    )

# ================= SEQUENCE =================

@bot.on_message(filters.command("sequence"))
async def sequence_cmd(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n`/sequence on` or `/sequence off`"
        )

    option = message.command[1].lower()

    if option == "on":
        user_sequence[message.from_user.id] = True

        return await message.reply_text(
            "**✅ Sequence Enabled**"
        )

    elif option == "off":
        user_sequence[message.from_user.id] = False

        return await message.reply_text(
            "**❌ Sequence Disabled**"
        )

    else:
        return await message.reply_text(
            "**Invalid Option ❌**"
        )

# ================= STATS =================

@bot.on_message(filters.command("stats") & filters.user(ADMIN))
async def stats(client, message):

    users = len(user_caption)

    await message.reply_text(
        f"**📊 Total Users :** `{users}`"
    )

# ================= BROADCAST =================

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN))
async def broadcast(client, message):

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:**\n`/broadcast message`"
        )

    text = message.text.split(None, 1)[1]

    success = 0

    for user_id in user_caption.keys():

        try:
            await bot.send_message(user_id, text)
            success += 1
            time.sleep(1)

        except:
            pass

    await message.reply_text(
        f"**✅ Broadcast Sent To {success} Users**"
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

    sequence_enabled = user_sequence.get(
        message.from_user.id,
        False
    )

    if sequence_enabled:
        new_name = f"[{message.id}]_{old_name}"
    else:
        new_name = f"Renamed_{old_name}"

    msg = await message.reply_text(
        "**⬇️ Downloading File...**"
    )

    downloaded = await message.download(
        file_name=new_name
    )

    await msg.edit(
        "**⬆️ Uploading File...**"
    )

    caption = user_caption.get(
        message.from_user.id,
        f"**✅ Renamed Successfully**\n\n`{new_name}`"
    )

    thumb = user_thumbnail.get(
        message.from_user.id
    )

    await message.reply_document(
        document=downloaded,
        caption=caption,
        thumb=thumb
    )

    await msg.delete()

    if os.path.exists(downloaded):
        os.remove(downloaded)

# ================= RUN =================

print("✅ Bot Started Successfully")

bot.run()
