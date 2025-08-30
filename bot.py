from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
import os

# Get from environment (Render → Environment Variables)
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize Pyrogram client
app = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.reply("👋 Hello! I am your Music Bot.\nAdd me to a group and use `/play` to play music.")


@app.on_message(filters.command("play") & filters.group)
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply("❌ Please give me a file path or song name after /play")
    
    # Here we use a local file path
    song = message.text.split(" ", 1)[1]

    if not os.path.exists(song):
        return await message.reply("❌ File not found. Upload a valid .mp3 file path.")

    chat_id = message.chat.id

    try:
        await pytgcalls.join_group_call(
            chat_id,
            InputAudioStream(song)
        )
        await message.reply(f"▶️ Playing `{song}` in voice chat!")
    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")


@app.on_message(filters.command("stop") & filters.group)
async def stop(_, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("⏹️ Stopped playing.")
    except:
        await message.reply("❌ No active voice chat to stop.")


# Run
app.start()
pytgcalls.start()
print("✅ Bot is running...")
app.run()
