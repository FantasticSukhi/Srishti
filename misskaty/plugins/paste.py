"""
 * @author        yasir <yasiramunandar@gmail.com>
 * @date          2022-12-01 09:12:27
 * @lastModified  2022-12-01 09:32:31
 * @projectName   MissKatyPyro
 * Copyright @YasirPedia All rights reserved
"""
from os import remove
from re import compile as compiles
from misskaty.helper.http import http
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from json import loads as json_loads
from misskaty import app
from misskaty.vars import COMMAND_HANDLER
from misskaty.helper.tools import rentry

__MODULE__ = "Paste"
__HELP__ = """
/paste [Text/Reply To Message] - Post text to Rentry using markdown style.
/temp_paste [Text/Reply To Message] - Post text to tempaste.com using html style.
"""

# Size Checker for Limit
def humanbytes(size: int):
    """Convert Bytes To Bytes So That Human Can Read It"""
    if not isinstance(command, int):
        try:
            size = size
        except ValueError:
            size = None
    if not size:
        return "0 B"
    size = int(size)
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {
        0: "",
        1: "K",
        2: "M",
        3: "G",
        4: "T",
        5: "P",
        6: "E",
        7: "Z",
        8: "Y",
    }
    while size > power:
        size /= power
        raised_to_pow += 1
    try:
        real_size = f"{str(round(size, 2))} {dict_power_n[raised_to_pow]}B"
    except KeyError:
        real_size = "Can't Define Real Size !"
    return real_size


# Pattern if extension supported, PR if want to add more
pattern = compiles(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$|x-subrip$")


@app.on_message(filters.command(["paste"], COMMAND_HANDLER))
async def create(_, message):
    reply = message.reply_to_message
    target = str(message.command[0]).split("@", maxsplit=1)[0]
    if not reply and len(message.command) < 2:
        return await message.reply_text(f"**Reply To A Message With /{target} or with command**")

    msg = await message.reply_text("`Pasting to Rentry...`")
    data = ""
    limit = 1024 * 1024
    if reply and reply.document:
        if reply.document.file_size > limit:
            return await msg.edit(f"**You can only paste files smaller than {humanbytes(limit)}.**")
        if not pattern.search(reply.document.mime_type):
            return await msg.edit("**Only text files can be pasted.**")
        file = await reply.download()
        try:
            with open(file, "r") as text:
                data = text.read()
            remove(file)
        except UnicodeDecodeError:
            try:
                remove(file)
            except:
                pass
            return await msg.edit("`File Not Supported !`")
    elif reply and (reply.text or reply.caption):
        data = reply.text.markdown or reply.caption.markdown
    elif not reply and len(message.command) >= 2:
        data = message.text.split(None, 1)[1]

    if message.from_user:
        if message.from_user.username:
            uname = f"@{message.from_user.username}"
        else:
            uname = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    else:
        uname = message.sender_chat.title

    try:
        url = await rentry(data)
    except Exception as e:
        await msg.edit(f"`{e}`")
        return

    if not url:
        return await msg.edit("Text Too Short Or File Problems")
    button = [[InlineKeyboardButton("Open Link", url=url)]]
    button.append([InlineKeyboardButton("Share Link", url=f"https://telegram.me/share/url?url={url}")])

    pasted = f"**Successfully pasted your data to Rentry<a href='{url}'>.</a>\n\nPaste by {uname}**"
    await msg.edit(pasted, reply_markup=InlineKeyboardMarkup(button))


@app.on_message(filters.command(["temp_paste"], COMMAND_HANDLER))
async def create(_, message):
    reply = message.reply_to_message
    target = str(message.command[0]).split("@", maxsplit=1)[0]
    if not reply and len(message.command) < 2:
        return await message.reply_text(f"**Reply To A Message With /{target} or with command**")

    msg = await message.reply_text("`Pasting to TempPaste...`")
    data = ""
    limit = 1024 * 1024
    if reply and reply.document:
        if reply.document.file_size > limit:
            return await msg.edit(f"**You can only paste files smaller than {humanbytes(limit)}.**")
        if not pattern.search(reply.document.mime_type):
            return await msg.edit("**Only text files can be pasted.**")
        file = await reply.download()
        try:
            with open(file, "r") as text:
                data = text.read()
            remove(file)
        except UnicodeDecodeError:
            try:
                remove(file)
            except:
                pass
            return await msg.edit("`File Not Supported !`")
    elif reply and (reply.text or reply.caption):
        data = reply.text.html or reply.caption.html
    elif not reply and len(message.command) >= 2:
        data = message.text.split(None, 1)[1]

    if message.from_user:
        if message.from_user.username:
            uname = f"@{message.from_user.username}"
        else:
            uname = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    else:
        uname = message.sender_chat.title

    try:
        req = await http.post(
            "https://tempaste.com/api/v1/create-paste/",
            data={
                "api_key": "xnwuzXubxk3kCUz9Q2pjMVR8xeTO4t",
                "title": "MissKaty Paste",
                "paste_content": data,
                "visibility": "public",
                "expiry_date_type": "months",
                "expiry_date": 12,
            },
        )
        url = f"https://tempaste.com/{json_loads(req.text)['url']}"
    except Exception as e:
        await msg.edit(f"`{e}`")
        return

    if not url:
        return await msg.edit("Text Too Short Or File Problems")
    button = [[InlineKeyboardButton("Open Link", url=url)]]
    button.append([InlineKeyboardButton("Share Link", url=f"https://telegram.me/share/url?url={url}")])

    pasted = f"**Successfully pasted your data to Tempaste<a href='{url}'>.</a>\n\nPaste by {uname}**"
    await msg.edit(pasted, reply_markup=InlineKeyboardMarkup(button))
