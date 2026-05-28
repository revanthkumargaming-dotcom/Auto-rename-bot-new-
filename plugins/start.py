from pyrogram import Client, filters
from config import START_TEXT, HELP_TEXT, PICS, UPDATES
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from database.users import add_user


@Client.on_message(filters.command("start"))
async def start(client, message):

    user_id = message.from_user.id

    await add_user(user_id)

    buttons = InlineKeyboardMarkup([

        [
            InlineKeyboardButton(
                "⚙ Settings",
                callback_data="settings"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 Updates",
                url="https://t.me/yourchannel"
            ),

            InlineKeyboardButton(
                "💬 Support",
                url="https://t.me/yoursupport"
            )
        ]
    ])

    text = """
**🔥 ADVANCED AUTO RENAME BOT 🔥**

**✅ Features**
• FFmpeg Metadata
• Queue Processing
• Prefix/Suffix
• Sequence Rename
• Thumbnail Support
• x264/x265 Auto Tags
• Auto Quality Detection
• Persistent Settings
• Bold Styled Captions

**📂 Commands**
/setprefix
/setsuffix
/sequence
/nosequence
/metadata
/nometadata
/delthumb

Send Any File To Start Rename
"""

    await message.reply_text(
        text,
        reply_markup=buttons
    )
    
