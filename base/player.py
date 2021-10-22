from .music_base import MusicBase
from pytgcalls import PyTgCalls
from .client_base import user


class Player(MusicBase):
    ...


player = Player(PyTgCalls(user))
