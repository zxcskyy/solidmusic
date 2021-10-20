import asyncio

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped
from solidAPI import get_message

from utils.functions import get_audio_link
from .call_base import CallBase


class MusicBase(CallBase):
    async def _play(self, chat_id: int, title: str, uri: str):
        playlist = self.playlist
        call = self.call
        playlist[chat_id] = [{"title": title, "uri": uri}]
        await call.join_group_call(
            chat_id,
            AudioPiped(uri),
            stream_type=StreamType().pulse_stream
        )

    async def _set_play(self, chat_id: int, title: str, uri: str):
        try:
            return await self._play(chat_id, title, uri)
        except NoActiveGroupCall:
            await self.create_call(chat_id)
            await self._play(chat_id, title, uri)

    async def play(self, cb: types.CallbackQuery, result: dict[str, str]):
        playlist = self.playlist
        chat_id = cb.message.chat.id
        title = result["title"]
        uri = result["uri"]
        if not playlist:
            y = await cb.edit_message_text(get_message(chat_id, "process"))
            url = get_audio_link(uri)
            try:
                await self._set_play(chat_id, title, url)
                await y.edit(f"playing {result['title']} in here")
            except FloodWait as e:
                await y.edit(f"getting floodwait, bot sleeping for {e.x} seconds")
                await asyncio.sleep(e.x)
                await self._set_play(chat_id, title, url)
            except Exception as e:
                await y.edit(f"an error occured\n\n{e}")
        elif len(playlist[chat_id]) >= 1:
            playlist[chat_id].extend([{"title": title, "uri": uri}])
            y = await cb.edit_message_text("queued")
            await asyncio.sleep(5)
            return await y.delete()
