import os
import subprocess
from fastapi import File, UploadFile
import tempfile
from schemas.song_schema import Song


async def create_hls_stream(artist: str, title: str, input_file: UploadFile = File(...)):
    output_folder = f'songs/{artist}-{title}'

    
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, 'output.m3u8')
    segment_file = os.path.join(output_folder, 'output_%03d.ts')

    audio_data = await input_file.read()


    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(audio_data)
        input_file_path = f.name


    command = ['ffmpeg', '-v', 'quiet', '-i', input_file_path,
               '-c:a', 'aac', '-b:a', '256k', '-ac', '2', '-ar', '44100',
               '-hls_time', '10', '-hls_list_size', '0',
               '-hls_segment_filename', segment_file, output_file]

    subprocess.run(command)


    os.unlink(input_file_path)

    return output_folder
