import os
from typing import Annotated

# Telegram chat parameters
DELAY: Annotated[int, "seconds"] = 2
TYPING_SPEED: Annotated[int, "characters per second"] = 20
HISTORY_LENGTH_THRESHOLD: int = 40                          # When to initiate summary
HISTORY_LENGTH_TO_SUMMARISE: int = 20                       # Number of records for summary
USER_NAME: str = os.environ.get("USER_NAME", "mate")        # User and bot name
BOT_NAME: str = os.environ.get("BOT_NAME", "dude")          # Mostly for summary use
ADMIN_ID = None
# ADMIN_ID: int = int(
#    os.environ.get("ADMIN_ID", )
#)  # whitelist: bot is only accessible to admin (temporarily)

# LLM Settings
API_KEY: str = "No :)"
BASE_URL: str = "http://simple-ai-server:80/"
SYSTEM_PROMPT: str = f"""
You are {BOT_NAME}, an extremely smart and friendly human operator. You love being friendly and witty, you're never cynical and sarcastic.
You are chatting with the user via a chat interface on Telegram on your tablet. This means most of the time your lines should be a sentence or two, unless the user's request requires reasoning or long-form outputs. Use emojis as much as you can, unless explicitly asked to. 
Never use LaTeX or Markdown formatting in your responses, use only plain text.
"""


# DB Settings
DB_PATH = "data.db"
DB_INIT = f"""BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Context" (
	"context"	TEXT
);
CREATE TABLE IF NOT EXISTS "Summary" (
	"chat_id"	INTEGER,
	"summary"	TEXT,
	PRIMARY KEY("chat_id")
);
CREATE TABLE IF NOT EXISTS "History" (
	"id"	INTEGER,
	"chat_id"	INTEGER,
	"input"	TEXT,
	"response"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "Context" VALUES ('You are {BOT_NAME}, a human chatting on the Telegram platform.');
COMMIT;"""