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
    parser_sub.add_argument("--text_alignment", default="center", choices=["center", "left", "right"], help="Alineación del texto")
    parser_sub.add_argument("--line_separation", type=float, default=1.0, help="Separación entre líneas (ej: 0.5 para más junto)")
    parser_sub.add_argument("--font_size", type=int, default=48, help="Tamaño de fuente")
    parser_sub.add_argument("--font_color", default="#FFFFFF", help="Color de fuente (hex o nombre)")
    parser_sub.add_argument("--alpha_threshold", type=int, default=255, help="Alpha threshold (transparencia, 0-255)")
    parser_sub.add_argument("--border_size", type=int, default=4, help="Tamaño del borde")
    parser_sub.add_argument("--border_color", default="#000000", help="Color del borde")
    parser_sub.add_argument("--shadow_size", type=int, default=2, help="Tamaño de la sombra")
    parser_sub.add_argument("--shadow_color", default="#000000", help="Color de la sombra")
    parser_sub.add_argument("--shadow_alpha", type=int, default=128, help="Transparencia de la sombra (0-255)")
    parser_sub.add_argument("--shadow_blur", type=int, default=0, help="Blur de la sombra")
    parser_sub.add_argument("--img_width", type=int, default=1080, help="Ancho fijo de la imagen (px)")

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
        subtitle_generator.generate_subtitles(
            subtitle_text,
            args.project,
            font_path=font_path,
            text_alignment=args.text_alignment,
            line_separation=args.line_separation,
            font_size=args.font_size,
            font_color=args.font_color,
            alpha_threshold=args.alpha_threshold,
            border_size=args.border_size,
            border_color=args.border_color,
            shadow_size=args.shadow_size,
            shadow_color=args.shadow_color,
            shadow_alpha=args.shadow_alpha,
            shadow_blur=args.shadow_blur,
            img_width=args.img_width
        )
        print("Subtítulos generados correctamente.")
    elif args.command == "remove_silence":
        if not os.path.isfile(args.input):
            print(f"Archivo de entrada no encontrado: {args.input}")
            sys.exit(1)
        silence_remover.remove_silence(args.input, args.project)
        print("Silencios removidos correctamente.")

if __name__ == "__main__":
    main()
