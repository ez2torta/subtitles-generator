from PIL import Image, ImageDraw, ImageFont
import textwrap
from datetime import datetime
import os

def generate_subtitles(subtitle_text, project_name):
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

    font = ImageFont.truetype("LiberationSans-Regular.ttf", 35)
    padding = 10

    # Define the output directory
    output_dir = os.path.join('output', datetime.now().strftime('%Y%m%d'))

    # Check and create directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate image for each subtitle
    for index_of_subtitle, subtitle in enumerate(subtitles_with_breaks, start=1):
        lines = textwrap.wrap(subtitle, width=50)  # adjust width as needed
        line_height = font.getsize('hg')[1]
        img_height = padding + line_height * len(lines) + padding
        img_width = max([font.getsize(line)[0] for line in lines]) + 2 * padding
        img = Image.new('RGBA', (img_width, img_height), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        y_text = padding
        for line in lines:
            line_width = font.getsize(line)[0]
            d.text(((img_width - line_width) / 2, y_text), line, font=font, fill='white')
            y_text += line_height
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))  # adjust last value for opacity, 0-255
        img = Image.alpha_composite(img, overlay)
        filename = os.path.join(output_dir, f"{project_name}_{index_of_subtitle}.png")
        img.save(filename)
