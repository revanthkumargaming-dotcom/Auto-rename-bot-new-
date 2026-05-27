# ================= IMPORTS =================

import os
import time
import asyncio

from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import API_ID, API_HASH, BOT_TOKEN
from keep_alive import keep_alive

# ================= BOT CLIENT =================

bot = Client(
    "RenameBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= CREATE FOLDERS =================

os.makedirs("downloads", exist_ok=True)
os.makedirs("thumbnails", exist_ok=True)

# ================= PROGRESS FUNCTION =================

async def progress(current, total, message, start_time, action):

    now = time.time()
    diff = now - start_time

    if diff == 0:
        return

    if round(diff % 10) == 0 or current == total:

        percentage = current * 100 / total
        speed = current / diff
        speed_mb = speed / (1024 * 1024)

        text = (
            f"🚀 {action}\n\n"
            f"📊 Progress : {percentage:.1f}%\n"
            f"⚡ Speed : {speed_mb:.2f} MB/s"
        )

        try:
            await message.edit_text(text)
        except:
            pass

# ================= START COMMAND =================

@bot.on_message(filters.command("start"))
async def start_command(client, message):

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📢 Channel",
                    url="https://t.me/yourchannel"
                )
            ]
        ]
    )

    text = (
        "👋 Hello!\n\n"
        "📂 File pampu.\n"
        "✨ Nenu automatic ga rename chestanu."
    )

    await message.reply_text(
        text=text,
        reply_markup=buttons
    )

# ================= RENAME HANDLER =================

@bot.on_message(filters.document | filters.video)
async def rename_handler(client, message):

    file = message.document or message.video

    # ================= FILE SIZE CHECK =================

    if file.file_size > 2 * 1024 * 1024 * 1024:

        await message.reply_text(
            "❌ 2GB kante pedda file upload cheyyalem!"
        )
        return

    # ================= FILE NAMES =================

    old_name = file.file_name
    new_name = f"Renamed_{old_name}"

    # ================= DOWNLOAD =================

    status = await message.reply_text("⏳ Downloading...")
    start_time = time.time()

    download_path = await message.download(
        file_name=f"downloads/{old_name}",
        progress=progress,
        progress_args=(status, start_time, "Downloading")
    )

    # ================= PROCESS =================

    await status.edit_text("⚡ Processing...")

    output_path = f"downloads/{new_name}"

    cmd = [
        "ffmpeg",
        "-y",
        "-i", download_path,
        "-map", "0",
        "-c", "copy",
        "-metadata", f"title={new_name}",
        output_path
    ]

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )

    await process.wait()

    # ================= UPLOAD =================

    await status.edit_text("📤 Uploading...")

    caption = (
        f"✅ **File Renamed Successfully**\n\n"
        f"📄 **File Name :** `{new_name}`\n"
        f"🤖 **Bot :** RenameBot"
    )

    thumb = f"thumbnails/{message.from_user.id}.jpg"

    try:

        await message.reply_document(
            document=output_path,
            thumb=thumb if os.path.exists(thumb) else None,
            caption=caption,
            progress=progress,
            progress_args=(status, start_time, "Uploading")
        )

        await status.delete()

    except Exception as error:

        await message.reply_text(
            f"❌ Error:\n`{error}`"
        )

    finally:

        if os.path.exists(download_path):
            os.remove(download_path)

        if os.path.exists(output_path):
            os.remove(output_path)

# ================= MAIN FUNCTION =================

async def main():

    keep_alive()

    await bot.start()

    print("✅ Bot Started Successfully")

    await idle()

    await bot.stop()

# ================= RUN BOT =================

if __name__ == "__main__":
    asyncio.run(main())
