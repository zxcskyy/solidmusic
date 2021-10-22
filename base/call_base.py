import random

from pyrogram.raw.functions.phone import CreateGroupCall
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import GroupCallNotFound
from pytgcalls.types.input_stream import AudioPiped

from utils.functions import get_audio_link
from .client_base import user


class CallBase:
    def __init__(self, pytgcalls: PyTgCalls):
        self.call = pytgcalls
        self.playlist: dict[int, list[dict[str, str]]] = {}

    @staticmethod
    async def create_call(chat_id: int):
        await user.send(CreateGroupCall(
            peer=await user.resolve_peer(chat_id),
            random_id=random.randint(10000, 999999999)
        ))

    async def change_status(self, status: str, chat_id: int):
        if status == "pause":
            call = self.call
            if call.get_call(chat_id):
                await call.pause_stream(chat_id)
        elif status == "resume":
            call = self.call
            if call.get_call(chat_id):
                await call.resume_stream(chat_id)

    async def change_vol(self, chat_id: int, vol: int):
        call = self.call
        if call.get_call(chat_id):
            await call.change_volume_call(chat_id, vol)

    async def stream_change(self, chat_id: int, query: str):
        call = self.call
        url = get_audio_link(query)
        await call.change_stream(
            chat_id,
            AudioPiped(url)
        )

    async def change_stream(self, chat_id):
        playlist = self.playlist
        if not playlist:
            return "not playlist"
        if len(playlist[chat_id]) > 1:
            playlist[chat_id].pop(0)
            query = playlist[chat_id][0]["uri"]
            title = playlist[chat_id][0]["title"]
            await self.stream_change(chat_id, query)
            return f"skipped track, and playing {title}"

    async def end_stream(self, chat_id):
        playlist = self.playlist
        call = self.call
        try:
            if call.get_call(chat_id):
                await call.leave_group_call(chat_id)
                del playlist[chat_id]
                return "ended"
        except GroupCallNotFound:
            return "not streaming"
