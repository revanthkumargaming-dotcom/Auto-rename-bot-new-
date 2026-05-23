import os
import subprocess

from pyrogram import Client, filters

from database.users import (
    add_user,
    get_user,
    update_count
)

from helpers.filename import (
    clean_filename,
    detect_quality,
    detect_codec
)

# Queue
PROCESS = []


@Client.on_message(filters.document)
async def rename_file(client, message):

    user_id = message.from_user.id

    # Prevent multiple processing
    if user_id in PROCESS:

        return await message.reply_text(
            "**⏳ Previous File Processing...**"
        )

    PROCESS.append(user_id)

    try:

        file = message.document

        # User create
        await add_user(user_id)

        # Get settings
        data = await get_user(user_id)

        prefix = data["prefix"]
        suffix = data["suffix"]

        metadata = data["metadata"]

        sequence = data["sequence"]

        count = data["count"]

        # Original filename
        old_name = file.file_name

        # Cleanup tags
        old_name = clean_filename(old_name)

        # Detect quality
        quality = detect_quality(old_name)

        # Detect codec
        codec = detect_codec(old_name)

        # Sequence mode
        if sequence:

            seq = str(count).zfill(3)

            new_name = (
                f"{prefix} "
                f"{seq} "
                f"{old_name} "
                f"[{quality}] "
                f"{codec} "
                f"{suffix}"
            )

            await update_count(
                user_id,
                count + 1
            )

        else:

            new_name = (
                f"{prefix} "
                f"{old_name} "
                f"[{quality}] "
                f"{codec} "
                f"{suffix}"
            )

        # Remove extra spaces
        new_name = " ".join(new_name.split())

        # Download
        path = await message.download(
            file_name=f"downloads/{new_name}"
        )

        output_path = path

        # Metadata mode
        if metadata:

            output_path = f"downloads/meta_{new_name}"

            cmd = [
                "ffmpeg",
                "-i", path,
                "-map", "0",
                "-c", "copy",
                "-metadata",
                "title=Encoded By Rename Bot",
                output_path
            ]

            subprocess.run(cmd)

        # Caption
        caption = f"""
**✅ File Renamed Successfully**

**📂 Name:** `{new_name}`

**⚡ Features Applied**
• Metadata
• Queue
• Auto Tags
• Sequence

**🤖 Powered By:** @YourBot
"""

        # Thumbnail
        thumb = "thumbnails/thumb.jpg"

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

        # Cleanup
        if os.path.exists(path):
            os.remove(path)

        if os.path.exists(output_path):
            os.remove(output_path)

    except Exception as e:

        await message.reply_text(
            f"**❌ Error:** `{e}`"
        )

    finally:

        if user_id in PROCESS:
            PROCESS.remove(user_id)
