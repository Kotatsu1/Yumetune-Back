from yt_dlp import YoutubeDL


YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}


def search_yt(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info("ytsearch5:%s" % item, download=False)['entries']
        except Exception:
            return False

        results = list(map(lambda i: {'source': i['formats'][5]['url'], 'title': i['title']}, info))
        
    return results