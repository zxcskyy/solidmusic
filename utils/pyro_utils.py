from youtube_search import YoutubeSearch

music_result = []


def yt_search(query: str):
    result = []
    i = j = 0
    for _ in range(10):
        i += 1
        yt_res = YoutubeSearch(query, 10).to_dict()
        x = {
            "title": yt_res[j]["title"],
            "url": f"https://youtube.com{yt_res[j]['url_suffix']}",
            "duration": yt_res[j]["duration"]
        }
        result.append(x.copy())
        j += 1
    return result
