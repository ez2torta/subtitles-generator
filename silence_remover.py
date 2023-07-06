import sys
import os
import glob
from pydub import AudioSegment, silence
import ffmpeg

def remove_silence_and_save_parts(input_file, output_folder, silence_threshold=-40, min_silence_len=500, padding=350):
    audio = AudioSegment.from_file(input_file, format="mp4")

    non_silent_ranges = silence.detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_threshold)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for i, (start, end) in enumerate(non_silent_ranges):
        start = max(0, start - padding)
        end = min(len(audio), end + padding)
        output_audio = audio[start:end]
        output_file = os.path.join(output_folder, f"output_{i+1}.mp3")
        output_audio.export(output_file, format="mp3")

def find_mp4_file():
    mp4_files = glob.glob("*.mp4")
    if not mp4_files:
        print("No mp4 files found in the current directory.")
        sys.exit(1)
    return mp4_files[0]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python remove_silence_and_save_parts.py <output_folder>")
        sys.exit(1)

    input_file = find_mp4_file()
    output_folder = sys.argv[1]

    remove_silence_and_save_parts(input_file, output_folder)
