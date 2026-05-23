from pyrogram import Client, filters


@Client.on_callback_query()
async def callbacks(client, query):

    data = query.data

    # SETTINGS PANEL
    if data == "settings":

        text = """
**⚙ BOT SETTINGS**

Commands:

/setprefix
/setsuffix
/sequence
/nosequence
/metadata
/nometadata
/delthumb
"""

        await query.message.edit_text(
            text
        )
