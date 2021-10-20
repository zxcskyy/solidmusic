from base.client_base import bot
from base.player import player
from utils.decorators import authorized_only
from pyrogram import types, filters

from utils.functions import group_only


@bot.on_message(filters.command("pause") & group_only)
@authorized_only
async def pause_(_, message: types.Message):
    await player.change_status("pause", message.chat.id)
    await message.reply("paused")


@bot.on_message(filters.command("resume") & group_only)
@authorized_only
async def resume_(_, message: types.Message):
    await player.change_status("resume", message.chat.id)
    await message.reply("resumed")


@bot.on_message(filters.command("skip") & group_only)
@authorized_only
async def skip_(_, msg: types.Message):
    x = await player.change_stream(msg.chat.id)
    await msg.reply(x)


@bot.on_message(filters.command("end") & group_only)
@authorized_only
async def end_(_, msg: types.Message):
    x = await player.end_stream(msg.chat.id)
    await msg.reply(x)
