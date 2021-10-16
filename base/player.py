from .music_base import MusicBase
from pytgcalls import PyTgCalls
from .client_base import user


class Player(MusicBase):
    ...


player = Player(PyTgCalls(user))


@player.call.on_stream_end()
async def stream_ended(_, update):
    playlist = player.playlist
    call = player.call
    chat_id = update.chat_id
    if playlist:
        if not playlist[chat_id]:
            del playlist[chat_id]
            await call.leave_group_call(chat_id)
        if len(playlist[chat_id]) > 1:
            playlist[chat_id].pop(0)
            query = playlist[chat_id][0]["query"]
            await player.stream_change(chat_id, query)
            return
        return
    return
