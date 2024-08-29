# Telegram chatbot using SimpleAI LLM deployment

Adapted from [Icarus](https://github.com/Ycmelon/icarus).

**Warning:** please listen to the following advice.

> A separate Telegram user account from your own, i.e. a second phone number to register for one (or use a service like [Textverified](https://www.textverified.com/))

There is a chance your number gets banned and you don't want it to happen with your main one.

## Usage

1. Clone repo, install dependencies in `requirements.txt`
2. Rename `template.env` to `.env`
3. Create a Telegram user account and [obtain its API ID and hash](https://docs.telethon.dev/en/stable/basic/signing-in.html)
4. Create a Telegram bot ([message @BotFather](https://t.me/botfather)) and obtain its bot token
5. Optional: get your personal Telegram account's user ID (not that of the bot you created earlier) ([message @userinfobot](https://t.me/userinfobot))
6. Generate a `StringSession` for your bot account with `python generate_session.py`.
7. Update `.env` with all above information
8. Run `main.py`, or through Docker.
