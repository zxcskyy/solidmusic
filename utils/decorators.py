from typing import Callable

from pyrogram import types, Client
from solidAPI.sudo import get_sudos


def authorized_only(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        user_id = message.from_user.id
        person = await message.chat.get_member(user_id)
        try:
            try:
                if user_id in get_sudos(message.chat.id):
                    return await func(client, message)
            except TypeError:
                pass
            if person.status in ["creator", "administrator"]:
                return await func(client, message)
            if person.status not in ["creator", "administrator", get_sudos(message.chat.id)]:
                return await message.reply("you can't do this command.")
        except AttributeError:
            if person.is_anonymous:
                return await func(client, message)
    return wrapper


def admins_only(func: Callable) -> Callable:
    async def wrapper(client: Client, message: types.Message):
        user_id = message.from_user.id
        person = await message.chat.get_member(user_id)
        try:
            if person.status in ["creator", "administrator"]:
                return await func(client, message)
            if person.status not in ["creator", "administrator"]:
                return await message.reply("you can't use this command.")
        except AttributeError:
            if person.is_anonymous:
                return await func(client, message)
    return wrapper
