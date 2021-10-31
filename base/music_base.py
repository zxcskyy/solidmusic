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
    async def _play(
        self,
        chat_id: int,
        title: str,
        audio_url: str,
        user_id: int,
        duration,
        yt_url,
        yt_id,
    ):
        playlist = self._playlist
        call = self._call
        playlist[chat_id] = [
            {
                "title": title,
                "duration": duration,
                "user_id": user_id,
                "uri": yt_url,
                "yt_id": yt_id,
            }
        ]
        await call.join_group_call(
            chat_id, AudioPiped(audio_url), stream_type=StreamType().pulse_stream
        )

    async def _set_play(
        self, chat_id: int, title: str, uri: str, user_id: int, duration, yt_url, yt_id
    ):
        try:
            return await self._play(
                chat_id, title, uri, user_id, duration, yt_url, yt_id
            )
        except NoActiveGroupCall:
            await self.create_call(chat_id)
            await self._play(chat_id, title, uri, user_id, duration, yt_url, yt_id)

    async def play(self, cb: types.CallbackQuery, result):
        playlist = self._playlist
        chat_id = cb.message.chat.id
        title = result["title"]
        duration = result["duration"]
        yt_url = result["uri"]
        user_id = result["user_id"]
        yt_id = result["yt_id"]
        user = (await cb.message.chat.get_member(user_id)).user
        lang = user.language_code
        bot_username = (await self._bot.get_me()).username
        if not playlist:
            try:
                y = await cb.edit_message_text(get_message(chat_id, "process"))
            except KeyError:
                add_chat(chat_id, lang)
                y = await cb.edit_message_text(get_message(chat_id, "process"))
            audio_url = get_audio_link(yt_url)
            try:
                await self._set_play(
                    chat_id, title, audio_url, user_id, duration, yt_url, yt_id
                )
                await y.edit(
                    "now playing\n"
                    f"📌 title: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})\n"
                    f"⏱ duration: {duration}\n"
                    f"🙌 requested by: {user.mention}"
                )
            except FloodWait as e:
                await y.edit(f"getting floodwait, bot sleeping for {e.x} seconds")
                await asyncio.sleep(e.x)
                await self._set_play(
                    chat_id, title, audio_url, user_id, duration, yt_url, yt_id
                )
                await y.edit(
                    "now playing\n"
                    f"📌 title: [{title}](https://t.me/{bot_username}?start=ytinfo_{yt_id})\n"
                    f"⏱ duration: {duration}\n"
                    f"🙌 requested by: {user.mention}"
                )
        elif len(playlist[chat_id]) >= 1:
            playlist[chat_id].extend(
                [
                    {
                        "title": title,
                        "duration": duration,
                        "user_id": user_id,
                        "uri": yt_url,
                        "yt_id": yt_id,
                    }
                ]
            )
            y = await cb.edit_message_text("queued")
            await asyncio.sleep(5)
            return await y.delete()
