## Estructura de carpetas de entrada

La carpeta `input/` contiene tus archivos `.txt` de subtítulos. Por ejemplo:

```
input/
  ejemplo_subtitulos.txt
  .donotremove.txt
```

El archivo `ejemplo_subtitulos.txt` puede tener este formato:

```
Hola, este es el primer subtítulo.

Este es el segundo subtítulo, que aparecerá en una imagen diferente.

¡Y este es el tercero! Puedes agregar tantos como quieras, separados por una línea en blanco.
```



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


## Ejemplos de uso del CLI


### 1. Generar subtítulos (básico)
```sh
python3 cli.py subtitle --project ejemplo --textfile ejemplo_subtitulos.txt
```


### 2. Generar subtítulos desde una carpeta personalizada de entrada y salida
```sh
python3 cli.py subtitle --project mi_proyecto --textfile mi_archivo.txt --input_dir input --output_dir output
```

### 3. Generar subtítulos con personalización de fuente y estilo
```sh
python3 cli.py subtitle --project demo --textfile subtitulos.txt \
    --font Roboto-Bold.ttf \
    --font_size 48 \
    --line_separation 1.5 \
    --font_color "#FFFF00" \
    --border_size 6 \
    --border_color "#000000" \
    --shadow_size 3 \
    --shadow_color "#222222" \
    --img_width 1080
```

### 4. Remover silencios de un video MP4
```sh
python3 cli.py remove_silence --project demo --input video.mp4
```

### 5. Limpiar la salida y dejar solo fuentes regulares
```sh
python3 clean_output.py
```

---

**Notas:**
- El parámetro `--textfile` busca por defecto en la carpeta indicada por `--input_dir` (por defecto `input/`).
- El resultado de los subtítulos se guarda en la carpeta indicada por `--output_dir` (por defecto `output/`).
- Puedes combinar todos los parámetros de personalización según tus necesidades.

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
