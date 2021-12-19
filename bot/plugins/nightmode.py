from pyrogram.types import ChatPermissions
from pyrogram import Client, __version__
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import pytz
import requests
from bot import app
from datetime import datetime

async def job_close():
    now = datetime.now(pytz.timezone('Asia/Jakarta'))
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    month = ['Unknown', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    tgl = now.strftime('%d')
    tahun = now.strftime('%Y')
    jam = now.strftime('%H:%M')
    await app.send_sticker(-1001128045651, "CAACAgQAAxkDAAEDfNhgygZBqbTlbOQ6Gk3CmtD-bnkRDAACLxsAAvEGNAY-qWSFYAqy3R4E")
    await app.send_message(
      -1001128045651, f"📆 {days[now.weekday()]}, {tgl} {month[now.month]} {tahun}\n⏰ Jam : {jam}\n\n**🌗 Mode Malam Aktif**\n`Proses LockDown dimulai, Grup ditutup dan semua member tidak akan bisa mengirim pesan. Selamat beristirahat dan bermimpi indah !!`\n\n~ Dbuat dengan Pyrogram v{__version__}.."
    )
    await app.set_chat_permissions(-1001128045651, ChatPermissions(can_send_messages=False, can_invite_users=True)
    )

async def job_close_ymoviez():
    now = datetime.now(pytz.timezone('Asia/Jakarta'))
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    month = ['Unknown', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    tgl = now.strftime('%d')
    tahun = now.strftime('%Y')
    jam = now.strftime('%H:%M')
    await app.send_message(
      -1001255283935, f"📆 {days[now.weekday()]}, {tgl} {month[now.month]} {tahun}\n⏰ Jam : {jam}\n\n**🌗 Mode Malam Aktif**\n`Grup ditutup hingga jam 9 pagi. Selamat beristirahat.....`\n\n~ Dbuat dengan Pyrogram v{__version__}.."
    )
    await app.set_chat_permissions(-1001255283935, ChatPermissions(can_send_messages=False, can_invite_users=True)
    )

async def job_open():
    now = datetime.now(pytz.timezone('Asia/Jakarta'))
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    month = ['Unknown', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    tgl = now.strftime('%d')
    tahun = now.strftime('%Y')
    jam = now.strftime('%H:%M')
    req = requests.get('https://api.lolhuman.xyz/api/random/quotes?apikey=d6933a59588ca5e57e7eb141')
    json = req.json()
    quote = json["result"]["quote"]
    by = json["result"]["by"]
    await app.send_sticker(-1001128045651, "CAACAgQAAxkDAAEDeJhgyLPTe0shLKykbafLA-rZk3CYZAAC4xoAAvEGNAYXtspUoZE5Nx4E")
    await app.send_message(
        -1001128045651, f"📆 {days[now.weekday()]}, {tgl} {month[now.month]} {tahun}\n⏰ {jam}`\n\n🌗 Mode Malam Selesai\nSelamat pagi, grup kini telah dibuka semoga hari-harimu menyenangkan.`\n\n**Quotes Today:**\n{quote} ~{by}"
    )
    await app.set_chat_permissions(-1001128045651, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_stickers=False, can_send_animations=True, can_invite_users=True, can_add_web_page_previews=True, can_use_inline_bots=True)
    )

async def job_open_ymoviez():
    now = datetime.now(pytz.timezone('Asia/Jakarta'))
    days = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    month = ['Unknown', 'Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    tgl = now.strftime('%d')
    tahun = now.strftime('%Y')
    jam = now.strftime('%H:%M')
    req = requests.get('https://api.lolhuman.xyz/api/random/quotes?apikey=d6933a59588ca5e57e7eb141')
    json = req.json()
    by = json["result"]["by"]
    quote = json["result"]["quote"]
    await app.send_message(
        -1001255283935, f"📆 {days[now.weekday()]}, {tgl} {month[now.month]} {tahun}\n⏰ {jam}`\n\n🌗 Mode Malam Selesai\nSelamat pagi, grup kini telah dibuka semoga hari-harimu menyenangkan.`\n\n**Quotes Today:**\n{quote} ~{by}"
    )
    await app.set_chat_permissions(-1001255283935, ChatPermissions(can_send_messages=True, can_send_media_messages=True, can_send_stickers=True, can_send_animations=True, can_invite_users=True, can_add_web_page_previews=True, can_use_inline_bots=True)
    )

scheduler = AsyncIOScheduler(timezone="Asia/Jakarta")
scheduler.add_job(job_close, trigger="cron", hour=22, minute=0)
scheduler.add_job(job_close_ymoviez, trigger="cron", hour=22, minute=15)
scheduler.add_job(job_open, trigger="cron", hour=6, minute=0)
scheduler.add_job(job_open_ymoviez, trigger="cron", hour=9, minute=0)
scheduler.start()
