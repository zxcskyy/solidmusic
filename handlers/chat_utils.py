import asyncio

from pyrogram import filters, Client
from pyrogram.types import ChatMemberUpdated, Message

from base.client_base import user
from solidAPI.chat import add_chat, del_chat

from utils.functions import group_only


@Client.on_chat_member_updated(filters=filters.group)
async def on_bot_added(client: Client, msg: ChatMemberUpdated):
    try:
        bot_id = (await client.get_me()).id
        chat_id = msg.chat.id
        members_id = msg.new_chat_member.user.id
        lang = msg.new_chat_member.invited_by.language_code
        if members_id == bot_id:
            add_chat(chat_id, lang) if lang else "en"
    except AttributeError:
        pass


@Client.on_message(filters=filters.left_chat_member)
async def on_bot_kicked(client: Client, msg: Message):
    try:
        bot_id = (await client.get_me()).id
        chat_id = msg.chat.id
        members = msg.left_chat_member
        if members.id == bot_id:
            del_chat(chat_id)
            await user.send_message(chat_id, "bot left from chat, assistant left this chat too.")
            await asyncio.sleep(3)
            await user.leave_chat(chat_id)
            return
    except Exception as e:
        await msg.reply(f"{e}")


@Client.on_message(filters.command("addchat") & group_only)
async def add_chat_(_, message: Message):
    try:
        chat_id = message.chat.id
        lang = (await message.chat.get_member(message.from_user.id)).user.language_code
        x = add_chat(chat_id, lang)
        if x == 201:
            return await message.reply(f"{chat_id} added to our database")
        if x == 409:
            return await message.reply("this chat already added to our database.")
    except Exception as e:
        await message.reply(f"{e}")


@Client.on_message(filters.command("delchat") & group_only)
async def del_chat_(_, message: Message):
    try:
        chat_id = int("".join(message.command[1]))
    except (KeyError, IndexError):
        chat_id = message.chat.id
    try:
        x = del_chat(chat_id)
        if x == 200:
            return await message.reply("chat deleted from db")
        if x == 404:
            return await message.reply(f"{chat_id} already deleted from our database.")
    except Exception as e:
        await message.reply(f"{e}")
