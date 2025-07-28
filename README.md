

# Subtitle Generator

Subtitle Generator es una aplicación Python 100% de línea de comandos (CLI) para generar imágenes de subtítulos a partir de texto, remover silencios de archivos MP4 y soporta múltiples fuentes tipográficas.


## Características

1. **Generación de subtítulos**: Genera imágenes PNG para cada subtítulo, dividiendo automáticamente los textos largos en varias imágenes de máximo 2 líneas cada una.
2. **Soporte de fuentes**: Coloca archivos `.ttf` en la carpeta `fonts/` y elige la fuente con `--font`. Si no se especifica, se usa la primera fuente disponible.
3. **Remoción de silencios**: Divide un MP4 en segmentos de audio sin silencio.
4. **Limpieza fácil**: Ejecuta `python3 clean_output.py` para borrar la carpeta de salida y las fuentes no regulares.


## Cómo usar

1. Coloca tu texto en un archivo `.txt` (cada subtítulo separado por una línea en blanco).
2. Ejecuta el comando CLI para generar subtítulos o remover silencios (ver ejemplos abajo).
3. Puedes personalizar la fuente agregando archivos `.ttf` a la carpeta `fonts/` y usando el argumento `--font`.

### Ejemplo de uso CLI

Generar subtítulos con una fuente específica:
```sh
python3 cli.py subtitle --project demo --textfile subtitles.txt --font Roboto-Regular.ttf
```

Remover silencios de un video:
```sh
python3 cli.py remove_silence --project demo --input video.mp4
```

Limpiar la salida y dejar solo fuentes regulares:
```sh
python3 clean_output.py
```

## Organización de la salida

Los archivos generados se guardan en:

```
output/YYYYMMDD/NOMBRE_FUENTE/subtitle_NOMBREPROYECTO_#.png
```

## Personalización

- Puedes agregar más fuentes `.ttf` a la carpeta `fonts/`.
- El código divide automáticamente subtítulos largos en varias imágenes.
- Puedes ajustar el tamaño de fuente y otros estilos en `subtitle_generator.py`.

## Créditos y futuro

- Inspirado en la necesidad de creadores de contenido para subtítulos rápidos y personalizables.
- Próximamente: integración con Text-to-Speech.
