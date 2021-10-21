from base.client_base import bot
from base.player import player
from pyrogram import idle
from os import path, mkdir

if not path.exists("search"):
    mkdir("search")


player.call.start()
bot.start()
print("[ Bot running ]")
idle()
