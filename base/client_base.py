from pyrogram import Client
from konfig import config
from tgEasy import tgClient


user = Client(
    config.SESSION,
    config.API_ID,
    config.API_HASH
)


bots = Client(
    ":memory:",
    config.API_ID,
    config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="solidmusic.handlers")
)


bot = tgClient(bots)
