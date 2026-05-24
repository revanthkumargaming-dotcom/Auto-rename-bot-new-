import os
from pyrogram import Client, filters

API_ID = 20879824
API_HASH = "5f70a9a12a4bb8cc322bed62bc6007ce"
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Client(
    "renamebot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("🔥 Bot Working Successfully")

print("🚀 Starting Bot")

bot.run()
