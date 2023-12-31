from sqlalchemy import select
from database.postgresql import get_session
from fastapi import Depends, HTTPException, File, UploadFile
from security.user import get_current_user
from database.models import Songs
import os
import subprocess
import tempfile
from mutagen.mp3 import MP3


async def fetch_songs_from_db(current_user = Depends(get_current_user)):
    async with get_session() as session:
        stmt = select(Songs)
        result = await session.execute(stmt)
        songs = result.scalars().all()

    return songs


async def create_hls_stream(artist: str, title: str, input_file: UploadFile = File(...)):
    try:
        output_folder = f'songs/{artist}-{title}'
        if os.path.exists(output_folder):
            raise HTTPException(status_code=409, detail="Song already exists")

        os.makedirs(output_folder, exist_ok=True)

        output_file = os.path.join(output_folder, 'playlist.m3u8')
        segment_file = os.path.join(output_folder, 'seg_%03d.ts')

        audio_data = await input_file.read()


        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(audio_data)
            input_file_path = f.name


        command = ['ffmpeg', '-v', 'quiet', '-i', input_file_path,
                '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
                '-hls_time', '10', '-hls_list_size', '0',
                '-hls_segment_filename', segment_file, output_file]

        subprocess.run(command)


        audio = MP3(input_file_path)
        length_in_seconds = int(audio.info.length)


        os.unlink(input_file_path)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        await add_song(artist, title, length_in_seconds)
        return {"msg":"Song uploaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
async def add_song(artist: str, title: str, length: int):
    async with get_session() as session:
        new_song = Songs(
            artist=artist,
            title=title,
            length=length
        )

        session.add(new_song)
        await session.commit()
        await session.refresh(new_song)
    return new_song

