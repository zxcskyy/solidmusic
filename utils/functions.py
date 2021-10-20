import re
from pyrogram import filters
import pafy
from youtube_search import YoutubeSearch


def get_yt_link(query: str):
    return f"https://youtube.com{YoutubeSearch(query, 1).to_dict()[0]['url_suffix']}"


def get_audio_link(query: str) -> str:
    match = re.match(r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))", query)
    if match:
        url = query
    else:
        url = get_yt_link(query)
    pufy = pafy.new(url)
    audios = pufy.getbestaudio()
    return audios.url


group_only = filters.group & ~filters.private & ~filters.edited & ~filters.forwarded & ~filters.via_bot
