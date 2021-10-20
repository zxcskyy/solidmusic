from base.client_base import bot
from base.player import player
from pyrogram import idle

player.call.start()
bot.start()
print("[ Bot running ]")
idle()
