from pyrogram import Client
from pytgcalls import PyTgCalls, AudioPiped
import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("Please provide a YouTube link or file path.")
        return
    
    link = message.command[1]
    chat_id = message.chat.id

    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(link)
    )
    await message.reply("▶️ Now playing!")

app.start()
pytgcalls.start()
app.idle()
