from pyrogram import Client, filters

from database.users import (
    add_user,
    set_prefix,
    set_suffix,
    set_sequence,
    set_metadata
)


# SET PREFIX
@Client.on_message(filters.command("setprefix"))
async def prefix(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    try:
        value = message.text.split(None, 1)[1]

    except:
        return await message.reply_text(
            "**Usage:** `/setprefix text`"
        )

    await set_prefix(
        user_id,
        value
    )

    await message.reply_text(
        f"**✅ Prefix Saved:** `{value}`"
    )


# SET SUFFIX
@Client.on_message(filters.command("setsuffix"))
async def suffix(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    try:
        value = message.text.split(None, 1)[1]

    except:
        return await message.reply_text(
            "**Usage:** `/setsuffix text`"
        )

    await set_suffix(
        user_id,
        value
    )

    await message.reply_text(
        f"**✅ Suffix Saved:** `{value}`"
    )


# ENABLE SEQUENCE
@Client.on_message(filters.command("sequence"))
async def enable_sequence(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    await set_sequence(
        user_id,
        True
    )

    await message.reply_text(
        "**✅ Sequence Enabled**"
    )


# DISABLE SEQUENCE
@Client.on_message(filters.command("nosequence"))
async def disable_sequence(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    await set_sequence(
        user_id,
        False
    )

    await message.reply_text(
        "**❌ Sequence Disabled**"
    )


# ENABLE METADATA
@Client.on_message(filters.command("metadata"))
async def enable_metadata(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    await set_metadata(
        user_id,
        True
    )

    await message.reply_text(
        "**✅ Metadata Enabled**"
    )


# DISABLE METADATA
@Client.on_message(filters.command("nometadata"))
async def disable_metadata(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    await set_metadata(
        user_id,
        False
    )

    await message.reply_text(
        "**❌ Metadata Disabled**"
    )
