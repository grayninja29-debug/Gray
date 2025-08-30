import logging
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

# Logging setup
logging.basicConfig(level=logging.INFO)

# Create Pyrogram client (replace with your values or use config.py)
api_id = int(os.environ.get("API_ID", 12345))       # Add your API_ID
api_hash = os.environ.get("API_HASH", "your_api")   # Add your API_HASH
bot_token = os.environ.get("BOT_TOKEN", "your_token")  # Add your BOT_TOKEN

app = Client("music_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
pytgcalls = PyTgCalls(app)


# Start command
@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("✅ Bot is online!\nUse `/play <link>` to play music.")


# Play command
@app.on_message(filters.command("play"))
async def play(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Please provide a link or file path.\nExample: `/play song.mp3`")
        return

    link = message.command[1]
    chat_id = message.chat.id

    try:
        await pytgcalls.join_group_call(
            chat_id,
            AudioPiped(link)   # Correct for v2.2.6
        )
        await message.reply(f"▶️ Playing audio: {link}")
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")


# Stop command
@app.on_message(filters.command("stop"))
async def stop(client, message):
    chat_id = message.chat.id
    try:
        await pytgcalls.leave_group_call(chat_id)
        await message.reply("⏹️ Stopped the music.")
    except Exception as e:
        await message.reply(f"⚠️ Error: {str(e)}")


# Run the bot
async def main():
    await app.start()
    await pytgcalls.start()
    logging.info("Bot started...")
    await idle()

if __name__ == "__main__":
    import os
    from pyrogram import idle

    app.run(main())
