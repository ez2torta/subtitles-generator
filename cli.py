import argparse
import sys
import os
import subtitle_generator
import silence_remover

def main():
    parser = argparse.ArgumentParser(description="Subtitles Generator CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subparser for generating subtitles
    parser_sub = subparsers.add_parser("subtitle", help="Generar imágenes de subtítulos a partir de texto")
    parser_sub.add_argument("--project", required=True, help="Nombre del proyecto (carpetas y archivos)")
    parser_sub.add_argument("--textfile", required=True, help="Archivo de texto con los subtítulos")
    parser_sub.add_argument("--font", required=False, help="Nombre del archivo de fuente TTF en la carpeta fonts (ej: Roboto-Bold.ttf)")

    # Subparser para remover silencios
    parser_sil = subparsers.add_parser("remove_silence", help="Remover silencios de un archivo MP4")
    parser_sil.add_argument("--project", required=True, help="Nombre del proyecto (carpetas y archivos)")
    parser_sil.add_argument("--input", required=True, help="Archivo MP4 de entrada")

    args = parser.parse_args()

    if args.command == "subtitle":
        if not os.path.isfile(args.textfile):
            print(f"Archivo de texto no encontrado: {args.textfile}")
            sys.exit(1)
        with open(args.textfile, "r", encoding="utf-8") as f:
            subtitle_text = f.read()
        font_path = None
        if args.font:
            font_candidate = os.path.join("fonts", args.font)
            if os.path.isfile(font_candidate):
                font_path = font_candidate
            else:
                print(f"[ADVERTENCIA] No se encontró la fuente '{args.font}' en la carpeta fonts. Se usará la primera fuente disponible.")
        subtitle_generator.generate_subtitles(subtitle_text, args.project, font_path=font_path)
        print("Subtítulos generados correctamente.")
    elif args.command == "remove_silence":
        if not os.path.isfile(args.input):
            print(f"Archivo de entrada no encontrado: {args.input}")
            sys.exit(1)
        silence_remover.remove_silence(args.input, args.project)
        print("Silencios removidos correctamente.")

if __name__ == "__main__":
    main()
