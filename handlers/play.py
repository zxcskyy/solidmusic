from pyrogram import types, filters, Client
from solidAPI import emoji

from utils.functions import group_only
from utils.pyro_utils import music_result, yt_search


button_keyboard = types.InlineKeyboardButton


def play_keyboard(user_id: int):
    i = 0
    for j in range(5):
        i += 1
        yield button_keyboard(f"{i}", callback_data=f"play {j}|{user_id}")
        j += 1


@Client.on_message(filters.command("play") & group_only)
async def play_(client: Client, message: types.Message):
    bot_username = (await client.get_me()).username
    query = " ".join(message.command[1:])
    user_id = message.from_user.id
    yts = yt_search(query)
    cache = []
    chat_id = message.chat.id
    music_result[chat_id] = []
    for count, j in enumerate(yts, start=1):
        cache.append(j)
        if count % 5 == 0:
            music_result[chat_id].append(cache)
            cache = []
        if count == len(yts):
            music_result[chat_id].append(cache)
    yts.clear()
    results = "\n"
    k = 0
    for i in music_result[chat_id][0]:
        k += 1
        results += f"{k}. [{i['title'][:35]}...]({i['url']})\n"
        results += f"┣ {emoji.LIGHT_BULB} duration - {i['duration']}\n"
        results += f"┣ {emoji.FIRE} [More Information](https://t.me/{bot_username}?start=ytinfo_{i['id']})\n"
        results += "┗ powered by solid project\n\n"

    temps = []
    keyboards = []
    in_board = list(play_keyboard(user_id))
    for count, j in enumerate(in_board, start=1):
        temps.append(j)
        if count % 3 == 0:
            keyboards.append(temps)
            temps = []
        if count == len(in_board):
            keyboards.append(temps)
    await message.reply(
        f"{results}", reply_markup=types.InlineKeyboardMarkup(
            [
                keyboards[0],
                keyboards[1],
                [
                    button_keyboard(f"next {emoji.RIGHT_ARROW}", f"next|{user_id}"),
                    button_keyboard(f"close {emoji.WASTEBASKET}", f"close|{user_id}")
                ]
            ]
        ),
        disable_web_page_preview=True
    )
