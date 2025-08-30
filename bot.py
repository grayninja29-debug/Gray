import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import InputStream, AudioPiped
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "music-bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pytgcalls = PyTgCalls(app)

@app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("🎶 Hello! I’m your Music Bot.\nUse /play <song name> to play in VC.")

@app.on_message(filters.command("play"))
async def play(_, message):
    if len(message.command) < 2:
        return await message.reply_text("❌ Please provide a song name.\nExample: /play Faded")

    query = " ".join(message.command[1:])
    await message.reply_text(f"🔍 Searching and playing **{query}**...")

    import yt_dlp
    opts = {
        'format': 'bestaudio',
        'outtmpl': 'song.%(ext)s',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch1:{query}", download=True)
        file = ydl.prepare_filename(info['entries'][0])

    chat_id = message.chat.id
    await pytgcalls.join_group_call(
        chat_id,
        InputStream(
            AudioPiped(file)
        )
    )
    await message.reply_text(f"▶️ Now playing: {info['entries'][0]['title']}")

@app.on_message(filters.command("stop"))
async def stop(_, message):
    chat_id = message.chat.id
    await pytgcalls.leave_group_call(chat_id)
    await message.reply_text("⏹ Music stopped.")

async def main():
    await app.start()
    await pytgcalls.start()
    print("✅ Music Bot is running...")
    await idle()

if __name__ == "__main__":
    asyncio.run(main())
