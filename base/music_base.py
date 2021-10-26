import asyncio

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped
from solidAPI import add_chat, get_message

from utils.functions import get_audio_link

from .call_base import CallBase


class MusicBase(CallBase):
    async def _play(self, chat_id: int, title: str, uri: str, user_id: int):
        playlist = self.playlist
        call = self.call
        playlist[chat_id] = [{"title": title, "uri": uri, "user_id": user_id}]
        await call.join_group_call(
            chat_id, AudioPiped(uri), stream_type=StreamType().pulse_stream
        )

    async def _set_play(self, chat_id: int, title: str, uri: str, user_id: int):
        try:
            return await self._play(chat_id, title, uri, user_id)
        except NoActiveGroupCall:
            await self.create_call(chat_id)
            await self._play(chat_id, title, uri, user_id)

    async def play(self, cb: types.CallbackQuery, result):
        playlist = self.playlist
        chat_id = cb.message.chat.id
        title = result["title"]
        duration = result["duration"]
        uri = result["uri"]
        user_id = cb.message.from_user.id
        user = (await cb.message.chat.get_member(user_id)).user
        lang = user.language_code
        if not playlist:
            try:
                y = await cb.edit_message_text(get_message(chat_id, "process"))
            except KeyError:
                add_chat(chat_id, lang)
                y = await cb.edit_message_text(get_message(chat_id, "process"))
            url = get_audio_link(uri)
            try:
                await self._set_play(chat_id, title, url, user_id)
                await y.edit(
                    "now playing\n"
                    f"title: {title}\n"
                    f"duration: {duration}\n"
                    f"requested by: {user.mention}"
                )
            except FloodWait as e:
                await y.edit(f"getting floodwait, bot sleeping for {e.x} seconds")
                await asyncio.sleep(e.x)
                await self._set_play(chat_id, title, url, user_id)
                await y.edit(
                    "now playing\n"
                    f"title: {title}\n"
                    f"duration: {duration}\n"
                    f"requested by: {user.mention}"
                )
        elif len(playlist[chat_id]) >= 1:
            playlist[chat_id].extend([{"title": title, "uri": uri, "user_id": user_id}])
            y = await cb.edit_message_text("queued")
            await asyncio.sleep(5)
            return await y.delete()
