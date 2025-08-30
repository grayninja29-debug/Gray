from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
import os

# Get your credentials from environment variables
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize clients
app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
pytgcalls = PyTgCalls(app)

# /start command
@app.on_message(filters.command("start") & filters.private)
async def start(_, message):
    await message.reply(
        "👋 Hello! I am your Music Bot.\n\n"
        "➤ Add me to a group and use /play <file_path> to play music.\n"
        "➤ Use /stop to stop the music."
    )

# /play command
@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a file path after /play")
        return

    song = message.command[1]
    chat_id = message.chat.id

    if not os.path.exists(song):
        await message.reply("❌ File not found. Upload a valid .mp3 file path.")
        return

    try:
        await pytgcalls.join_group_call(
            chat_id,
            InputAudioStream(song)  # Works with py-tgcalls v2
        )
        await message.reply(f"▶️ Playing `{song}` in voice chat!")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

# /stop command
@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("⏹️ Stopped playing.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

# Run the bot
app.start()
pytgcalls.start()
print("✅ Music Bot is running...")
app.idle()
