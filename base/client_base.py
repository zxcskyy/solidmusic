from pyrogram import Client
from pytgcalls import PyTgCalls

from konfig import config

user = Client(
    config.SESSION,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
)

call_py = PyTgCalls(user)

bot = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="handlers"),
)
