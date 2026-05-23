import os

from pyrogram import Client, filters

from database.users import (
    add_user,
    set_thumbnail
)


@Client.on_message(filters.photo)
async def save_thumb(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    path = await message.download(
        file_name=f"thumbnails/{user_id}.jpg"
    )

    await set_thumbnail(
        user_id,
        path
    )

    await message.reply_text(
        "**✅ Thumbnail Saved Successfully**"
    )


# DELETE THUMBNAIL
@Client.on_message(filters.command("delthumb"))
async def delete_thumb(client, message):

    user_id = message.from_user.id

    path = f"thumbnails/{user_id}.jpg"

    if os.path.exists(path):

        os.remove(path)

        await set_thumbnail(
            user_id,
            None
        )

        await message.reply_text(
            "**✅ Thumbnail Deleted**"
        )

    else:

        await message.reply_text(
            "**❌ No Thumbnail Found**"
        )
