import os
import json
from datetime import datetime
from gtts import gTTS
# Placeholder for Microsoft API import
# from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig

def text_to_speech_gtts(texts, project_name, lang='es', slow=False):
    """
    Convierte una lista de textos a archivos de audio usando gTTS y genera un JSON con los tiempos y textos.
    """
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    results = []
    current_ms = 0
    for i, text in enumerate(texts):
        tts = gTTS(text=text, lang=lang, slow=slow)
        output_file = os.path.join(output_dir, f"tts_{project_name}_{i+1}.mp3")
        tts.save(output_file)
        # Estimar duración (opcional: usar pydub para obtener duración real)
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(output_file)
            duration_ms = len(audio)
        except ImportError:
            duration_ms = None
        results.append({
            "index": i+1,
            "text": text,
            "file": output_file,
            "start_ms": current_ms,
            "end_ms": current_ms + duration_ms if duration_ms else None
        })
        if duration_ms:
            current_ms += duration_ms
    with open(os.path.join(output_dir, f"{project_name}_tts.json"), "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"{len(results)} audios generados en {output_dir}")

# Placeholder para Microsoft API
def text_to_speech_microsoft(texts, project_name, lang='es-ES'):
    """
    Convierte una lista de textos a archivos de audio usando Microsoft Azure TTS (requiere configuración de API).
    """
    raise NotImplementedError("Microsoft TTS API integration is not implemented. Please add your credentials and implementation.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convierte textos a audio usando gTTS o Microsoft TTS.")
    parser.add_argument("--input", required=True, help="Archivo de texto con una frase por línea")
    parser.add_argument("--project", required=True, help="Nombre del proyecto para los archivos de salida")
    parser.add_argument("--engine", choices=["gtts", "microsoft"], default="gtts", help="Motor de TTS a usar")
    parser.add_argument("--lang", default="es", help="Idioma (default: es)")
    parser.add_argument("--slow", action="store_true", help="Voz lenta (solo gTTS)")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as f:
        texts = [line.strip() for line in f if line.strip()]
    if args.engine == "gtts":
        text_to_speech_gtts(texts, args.project, lang=args.lang, slow=args.slow)
    else:
        text_to_speech_microsoft(texts, args.project, lang=args.lang)