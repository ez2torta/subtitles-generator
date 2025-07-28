import os
import glob
import json
from pydub import AudioSegment, silence
from datetime import datetime

def remove_silence(input_file, project_name, silence_threshold=-40, min_silence_len=500, padding=350):
    audio = AudioSegment.from_file(input_file, format="mp4")

    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)
    # Calcular rangos de silencio
    silent_ranges = []
    last_end = 0
    for start, end in non_silent_ranges:
        if start > last_end:
            silent_ranges.append([last_end, start])
        last_end = end
    if last_end < len(audio):
        silent_ranges.append([last_end, len(audio)])

    # Guardar rangos en JSON
    def ms_to_timestamp(ms):
        s = ms // 1000
        ms_rem = ms % 1000
        m = s // 60
        s = s % 60
        h = m // 60
        m = m % 60
        return f"{h:02}:{m:02}:{s:02}.{ms_rem:03}"

    non_silent_json = [
        {"start_ms": start, "end_ms": end, "start": ms_to_timestamp(start), "end": ms_to_timestamp(end)}
        for start, end in non_silent_ranges
    ]
    silent_json = [
        {"start_ms": start, "end_ms": end, "start": ms_to_timestamp(start), "end": ms_to_timestamp(end)}
        for start, end in silent_ranges
    ]
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with open(os.path.join(output_dir, f"{project_name}_non_silent_ranges.json"), "w") as f:
        json.dump(non_silent_json, f, indent=2)
    with open(os.path.join(output_dir, f"{project_name}_silent_ranges.json"), "w") as f:
        json.dump(silent_json, f, indent=2)

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
