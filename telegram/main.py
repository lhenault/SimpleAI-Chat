import logging
import os
import asyncio
from dotenv import load_dotenv

from bot import bot
from client import client

load_dotenv()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client.start()
bot.start(bot_token=os.environ["TELEGRAM_BOT_TOKEN"])

loop = asyncio.get_event_loop()
loop.run_forever()
