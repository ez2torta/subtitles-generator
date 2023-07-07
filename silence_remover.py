import os
import glob
from pydub import AudioSegment, silence
from datetime import datetime

def remove_silence(input_file, project_name, silence_threshold=-40, min_silence_len=500, padding=350):
    audio = AudioSegment.from_file(input_file, format="mp4")

    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

    # Define the output directory
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))

    # Check and create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, (start, end) in enumerate(non_silent_ranges):
        start = max(0, start - padding)
        end = min(len(audio), end + padding)
        output_audio = audio[start:end]
        output_file = os.path.join(output_dir, f"audio_{project_name}_{i+1}.mp3")
        output_audio.export(output_file, format="mp3")
