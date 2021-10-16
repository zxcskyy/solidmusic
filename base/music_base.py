import asyncio

from pyrogram import types
from pyrogram.errors import FloodWait
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.exceptions import NoActiveGroupCall
from pytgcalls.types.input_stream import AudioPiped
from solidAPI import get_message

from utils.functions import get_audio_link
from .call_base import CallBase


class MusicBase(CallBase):
    async def _play(self, message: types.Message, source: str, y: types.Message, query=""):
        chat_id = message.chat.id
        playlist = self.playlist
        call = self.call
        playlist[chat_id] = [{"query": query}]
        await y.edit(get_message(chat_id, "stream").format(query))
        await call.join_group_call(
            chat_id,
            AudioPiped(source),
            stream_type=StreamType().pulse_stream
        )

    async def _set_play(self, message: types.Message, source: str, y: types.Message, query=""):
        playlist = self.playlist
        chat_id = message.chat.id
        try:
            await self._play(message, source, y, query)
            return
        except FloodWait as e:
            await message.reply(f"getting floodwait {e.x} second, bot sleeping")
            await asyncio.sleep(e.x)
            await self._play(message, source, y, query)
        except NoActiveGroupCall:
            try:
                await self.create_call(chat_id)
                await self._play(message, source, y, query)
            except Exception as ex:
                await y.edit(
                    f"{type(ex).__name__}: {ex}"
                )
                del playlist[chat_id]
        except Exception as ex:
            await y.edit(f"{type(ex).__name__}: {ex}")
            del playlist[chat_id]

    async def play(self, message: types.Message, query=""):
        chat_id = message.chat.id
        playlist = self.playlist
        if not playlist:
            y = await message.reply(get_message(chat_id, "process"))
            url = get_audio_link(query)
            await self._set_play(message, url, y, query)
            return
        if len(playlist[chat_id]) >= 1:
            playlist[chat_id].extend([{"query": query}])
            y = await message.reply("queued")
            await asyncio.sleep(5)
            await y.delete()
            return


