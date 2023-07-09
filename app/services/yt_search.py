from yt_dlp import YoutubeDL
import requests
import re
import os
from services.songs import add_song

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}


def search_yt(item):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            info = ydl.extract_info("ytsearch5:%s" % item, download=False)['entries']
        except Exception:
            return False

    return list(map(lambda i:
        {'source': next((obj for obj in i['formats'] if obj.get('resolution') == 'audio only'), None)['url'],
        'title': i['title']}, info))


async def create_hls_from_yt(url: str, artist: str, title: str):
    m3u8_url = requests.get(url)
    m3u8_file = m3u8_url.text
    segments = re.findall(r"https://\S+", m3u8_file)

    output_folder = f'{artist}-{title}'
    os.makedirs(f'songs/{output_folder}', exist_ok=True)


    for i, element in enumerate(segments):
        with open(f'songs/{output_folder}/seg_{i}.ts', 'wb') as f:
            f.write(requests.get(element).content)
        m3u8_file = m3u8_file.replace(element, f'seg_{i}.ts')


    with open(f'songs/{output_folder}/playlist.m3u8', 'w') as f:
        f.write(m3u8_file)



    durations = re.findall(r"#EXTINF:(\S+)", m3u8_file)
    total_duration = sum(float(duration[:-1]) for duration in durations)

    await add_song(artist, title, total_duration)

    return {'msg': 'Success', 'url': f'/songs/{output_folder}/playlist.m3u8'}

