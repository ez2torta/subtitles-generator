from pydub import AudioSegment
import os
import json
from datetime import datetime

def split_audio_chunks(input_file, project_name, chunk_length_ms=300000):
    """
    Divide un archivo de audio en chunks de duración fija (por defecto 5 minutos) y genera un JSON con los tiempos.
    """
    audio = AudioSegment.from_file(input_file)
    total_length = len(audio)
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    chunks = []
    for i, start in enumerate(range(0, total_length, chunk_length_ms)):
        end = min(start + chunk_length_ms, total_length)
        chunk_audio = audio[start:end]
        output_file = os.path.join(output_dir, f"chunk_{project_name}_{i+1}.mp3")
        chunk_audio.export(output_file, format="mp3")
        chunks.append({
            "index": i+1,
            "start_ms": start,
            "end_ms": end,
            "start": ms_to_timestamp(start),
            "end": ms_to_timestamp(end),
            "file": output_file
        })
    with open(os.path.join(output_dir, f"{project_name}_chunks.json"), "w") as f:
        json.dump(chunks, f, indent=2)
    print(f"{len(chunks)} chunks generados en {output_dir}")

def ms_to_timestamp(ms):
    s = ms // 1000
    ms_rem = ms % 1000
    m = s // 60
    s = s % 60
    h = m // 60
    m = m % 60
    return f"{h:02}:{m:02}:{s:02}.{ms_rem:03}"

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dividir audio en chunks de duración fija y generar JSON de tiempos.")
    parser.add_argument("--input", required=True, help="Archivo de audio (mp3, mp4, wav, etc)")
    parser.add_argument("--project", required=True, help="Nombre del proyecto para los archivos de salida")
    parser.add_argument("--minutes", type=int, default=5, help="Duración de cada chunk en minutos (default: 5)")
    args = parser.parse_args()
    split_audio_chunks(args.input, args.project, chunk_length_ms=args.minutes*60000)
