from telethon import TelegramClient, events

import os
from dotenv import load_dotenv

from db import get_context, set_context

load_dotenv()

from config import ADMIN_ID

api_id = int(os.environ["TELEGRAM_API_ID"])
api_hash = os.environ["TELEGRAM_API_HASH"]
bot = TelegramClient("bot", api_id, api_hash)


@bot.on(
    events.NewMessage(
        incoming=True, 
        from_users=[ADMIN_ID], 
        pattern="\\/get_context"
    )
)
async def on_get_context(event):
    await event.reply(get_context())


@bot.on(
    events.NewMessage(
        incoming=True, 
        from_users=[ADMIN_ID], 
        pattern="\\/set_context\\s.*"
    )
)
async def on_set_context(event):
    new_context = event.raw_text.replace("/set_context ", "")
    set_context(new_context)
    await event.reply(("Context set."))
