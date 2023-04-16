from pykeyboard import InlineKeyboard
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from misskaty import app
from misskaty.core.decorator.ratelimiter import ratelimiter
from misskaty.helper.http import http
from misskaty.vars import COMMAND_HANDLER


async def getData(chat_id, message_id, GetWord, CurrentPage):
    UDJson = (await http.get(f"https://api.urbandictionary.com/v0/define?term={GetWord}")).json()

    if "list" not in UDJson:
        return await app.send_msg(chat_id=chat_id, reply_to_message_id=message_id, text=f"Word: {GetWord}\nResults: Sorry could not find any matching results!", del_in=5)
    try:
        index = int(CurrentPage - 1)
        PageLen = len(UDJson["list"])
        UDReasult = f"**Definition of {GetWord}**\n" f"{UDJson['list'][index]['definition']}\n\n" "**📌 Examples**\n" f"__{UDJson['list'][index]['example']}__"
        UDFReasult = "".join(i for i in UDReasult if i not in "[]")
        return (UDFReasult, PageLen)

    except IndexError or KeyError:
        await app.send_msg(chat_id=chat_id, reply_to_message_id=message_id, text=f"Word: {GetWord}\nResults: Sorry could not find any matching results!", del_in=5)


@app.on_message(filters.command(["ud"], COMMAND_HANDLER))
@ratelimiter
async def urbanDictionary(self: Client, ctx: Message):
    message_id = ctx.id
    chat_id = ctx.chat.id
    GetWord = " ".join(ctx.command[1:])
    if not GetWord:
        message = await ctx.chat.ask("Now give any word for query!", identifier=(ctx.from_user.id, ctx.from_user.id, None))
        GetWord = message.text

    CurrentPage = 1
    UDReasult, PageLen = await getData(chat_id, message_id, GetWord, CurrentPage)

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, "pagination_urban#{number}" + f"#{GetWord}")
    await ctx.reply_msg(text=f"{UDReasult}", reply_markup=keyboard)


@app.on_callback_query(filters.create(lambda _, __, query: "pagination_urban#" in query.data))
@ratelimiter
async def ud_callback(self: Client, callback_query: CallbackQuery):
    message_id = callback_query.message.id
    chat_id = callback_query.message.chat.id
    CurrentPage = int(callback_query.data.split("#")[1])
    GetWord = callback_query.data.split("#")[2]

    try:
        UDReasult, PageLen = await getData(chat_id, message_id, GetWord, CurrentPage)
    except TypeError:
        return

    keyboard = InlineKeyboard()
    keyboard.paginate(PageLen, CurrentPage, "pagination_urban#{number}" + f"#{GetWord}")
    await app.edit_msg(chat_id=chat_id, message_id=message_id, text=UDReasult, reply_markup=keyboard)
