from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def main_buttons():

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

    return buttons
