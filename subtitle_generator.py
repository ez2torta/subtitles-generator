from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import os
import glob

def generate_subtitles(
    subtitle_text, project_name, font_path=None,
    text_alignment="center", line_separation=1.0, font_size=48, font_color="#FFFFFF",
    alpha_threshold=255, border_size=4, border_color="#000000",
    shadow_size=2, shadow_color="#000000", shadow_alpha=128, shadow_blur=0,
    img_width=1080
):
    # Split the contents into subtitles (separated by empty lines)
    subtitles = [subtitle.strip() for subtitle in subtitle_text.split('\n\n') if subtitle.strip() != '']

    # Insert a line break every 13 words
    subtitles_with_breaks = []
    for subtitle in subtitles:
        words = subtitle.split(' ')
        result = ''
        for i in range(0, len(words), 13):
            result += ' '.join(words[i:i + 13]) + '\n'
        subtitles_with_breaks.append(result.strip())

    def get_font(font_path=None, font_size=48):
        if font_path and os.path.isfile(font_path):
            try:
                print(f"[INFO] Usando fuente: {font_path}")
                return ImageFont.truetype(font_path, font_size)
            except OSError:
                print(f"[ADVERTENCIA] No se pudo cargar la fuente '{font_path}'. Se buscará otra.")
        font_files = glob.glob(os.path.join('fonts', '*.ttf'))
        if font_files:
            try:
                print(f"[INFO] Usando fuente: {font_files[0]}")
                return ImageFont.truetype(font_files[0], font_size)
            except OSError:
                print(f"[ADVERTENCIA] No se pudo cargar la fuente '{font_files[0]}'. Se buscará otra.")
        try:
            print("[INFO] Usando 'LiberationSans-Regular.ttf' de la raíz.")
            return ImageFont.truetype("LiberationSans-Regular.ttf", font_size)
        except OSError:
            try:
                print("[INFO] Usando 'Arial.ttf' del sistema.")
                return ImageFont.truetype("Arial.ttf", font_size)
            except OSError:
                print("[ADVERTENCIA] No se encontró ninguna fuente TTF válida. Usando fuente por defecto.")
                return ImageFont.load_default()

    font = get_font(font_path=font_path, font_size=font_size)
    padding = 10

    # Obtener nombre de la fuente para la carpeta
    font_name = None
    if font_path and os.path.isfile(font_path):
        font_name = os.path.splitext(os.path.basename(font_path))[0]
    else:
        font_files = glob.glob(os.path.join('fonts', '*.ttf'))
        if font_files:
            font_name = os.path.splitext(os.path.basename(font_files[0]))[0]
        else:
            font_name = 'default'

    # Define the output directory (con subcarpeta de fuente)
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'), font_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate image for each subtitle
    max_lines_per_image = 2
    subtitle_img_index = 1
    for index_of_subtitle, subtitle in enumerate(subtitles_with_breaks, start=1):
        lines = textwrap.wrap(subtitle, width=40)
        def get_text_size(text):
            if hasattr(font, 'getbbox'):
                bbox = font.getbbox(text)
                width = bbox[2] - bbox[0]
                height = bbox[3] - bbox[1]
                return (width, height)
            else:
                return font.getsize(text)

        # Dividir en bloques de máximo 2 líneas
        for i in range(0, len(lines), max_lines_per_image):
            block = lines[i:i+max_lines_per_image]
            line_height = get_text_size('hg')[1] * line_separation
            img_height = padding + int(line_height * len(block)) + padding + 40
            # img_width fijo
            width = img_width
            img = Image.new('RGBA', (width, img_height), (0, 0, 0, 0))
            d = ImageDraw.Draw(img)
            y_text = padding + 20
            for line in block:
                line_width = get_text_size(line)[0]
                # Alineación
                if text_alignment == "center":
                    x = (width - line_width) / 2
                elif text_alignment == "left":
                    x = padding
                else:
                    x = width - line_width - padding
                # Dibuja borde
                for dx in range(-border_size, border_size+1):
                    for dy in range(-border_size, border_size+1):
                        if dx != 0 or dy != 0:
                            d.text((x + dx, y_text + dy), line, font=font, fill=border_color)
                # Dibuja sombra
                if shadow_size > 0:
                    for dx in range(shadow_size, shadow_size+shadow_blur+1):
                        for dy in range(shadow_size, shadow_size+shadow_blur+1):
                            d.text((x + dx, y_text + dy), line, font=font, fill=shadow_color)
                # Dibuja texto principal
                d.text((x, y_text), line, font=font, fill=font_color)
                y_text += line_height
            # Guardar imagen
            output_file = os.path.join(output_dir, f"subtitle_{project_name}_{subtitle_img_index}.png")
            img.save(output_file)
            subtitle_img_index += 1
            y_text += line_height
        # Eliminada la generación de archivos image_*
