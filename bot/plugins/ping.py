import time
from pyrogram import filters
from info import COMMAND_HANDLER
from bot import app, user, botStartTime
from bot.utils.human_read import get_readable_time

@app.on_message(filters.command(["ping","ping@MissKatyRoBot"], COMMAND_HANDLER))
async def ping(_, message):
    currentTime = get_readable_time(time.time() - botStartTime)
    start_t = time.time()
    rm = await message.reply_text("🐱 Pong!!...")
    end_t = time.time()
    time_taken_s = round(end_t - start_t, 3)
    await rm.edit(f"<b>🐈 Pong!</b>\n<code>{time_taken_s} detik</code>\n\n<b>Userbot:</b> <a href='https://t.me/{(await user.get_me()).username}'>{(await user.get_me()).first_name}</a>\n<b>Bot:</b> @{(await app.get_me()).username}\n<b>Uptime:</b> <code>{currentTime}</code>", disable_web_page_preview=True)
