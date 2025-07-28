import os
import json
from datetime import datetime
import speech_recognition as sr
from pydub import AudioSegment

def audio_to_text(input_file, project_name, lang='es-ES', chunk_length_ms=None):
    """
    Transcribe un archivo de audio a texto usando SpeechRecognition (Google Web Speech API por defecto).
    Si chunk_length_ms está definido, divide el audio en partes antes de transcribir.
    """
    import subprocess
    recognizer = sr.Recognizer()
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Chunking rápido con ffmpeg -f segment
    import glob
    segment_sec = chunk_length_ms // 1000 if chunk_length_ms else 600
    chunk_pattern = os.path.join(output_dir, f"chunk_{project_name}_%04d.wav")
    print(f"[DEBUG] Ejecutando ffmpeg para crear chunks de {segment_sec} segundos...")
    subprocess.run([
        "ffmpeg", "-y", "-i", input_file, "-f", "segment", "-segment_time", str(segment_sec),
        "-acodec", "pcm_s16le", "-ar", "16000", chunk_pattern
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[DEBUG] Chunks creados en {output_dir}")
    chunk_files = sorted(glob.glob(os.path.join(output_dir, f"chunk_{project_name}_*.wav")))
    print(f"[DEBUG] Total de chunks: {len(chunk_files)}")
    results = []
    for idx, chunk_file in enumerate(chunk_files):
        start_ms = idx * segment_sec * 1000
        end_ms = start_ms + segment_sec * 1000
        print(f"[DEBUG] Mandando chunk {idx+1}/{len(chunk_files)} a la API: {chunk_file}")
        with sr.AudioFile(chunk_file) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data, language=lang)
                print(f"[DEBUG] Respuesta de la API para chunk {idx+1}: {text[:60]}{'...' if len(text) > 60 else ''}")
            except sr.UnknownValueError:
                text = "[No se pudo transcribir]"
                print(f"[DEBUG] Chunk {idx+1}: No se pudo transcribir")
            except sr.RequestError as e:
                text = f"[Error de API: {e}]"
                print(f"[DEBUG] Chunk {idx+1}: Error de API: {e}")
        results.append({
            "index": idx+1,
            "start_ms": start_ms,
            "end_ms": end_ms,
            "file": chunk_file,
            "text": text
        })
    with open(os.path.join(output_dir, f"{project_name}_transcription.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    with open(os.path.join(output_dir, f"{project_name}_transcription.txt"), "w", encoding="utf-8") as f:
        for r in results:
            f.write(r["text"] + "\n")
    print(f"Transcripción completa. Resultados en {output_dir}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Transcribe audio a texto usando SpeechRecognition.")
    parser.add_argument("--input", required=True, help="Archivo de audio (mp3, wav, etc)")
    parser.add_argument("--project", required=True, help="Nombre del proyecto para los archivos de salida")
    parser.add_argument("--lang", default="es-ES", help="Idioma para la transcripción (default: es-ES)")
    parser.add_argument("--minutes", type=int, help="Duración máxima de cada chunk en minutos (opcional)")
    parser.add_argument("--seconds", type=int, help="Duración máxima de cada chunk en segundos (opcional, recomendado: 10)")
    args = parser.parse_args()
    if args.seconds:
        chunk_length_ms = args.seconds * 1000
    elif args.minutes:
        chunk_length_ms = args.minutes * 60000
    else:
        chunk_length_ms = None
    audio_to_text(args.input, args.project, lang=args.lang, chunk_length_ms=chunk_length_ms)
