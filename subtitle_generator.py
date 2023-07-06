from PIL import Image, ImageDraw, ImageFont
import textwrap

# Read the contents of the file as a string
with open('subtitles.txt', 'r') as file:
    file_contents = file.read()

# Split the contents into subtitles (separated by empty lines)
subtitles = [subtitle.strip() for subtitle in file_contents.split('\n\n') if subtitle.strip() != '']

# Insert a line break every 13 words
subtitles_with_breaks = []
for subtitle in subtitles:
    words = subtitle.split(' ')
    result = ''
    for i in range(0, len(words), 13):
        result += ' '.join(words[i:i + 13]) + '\n'
    subtitles_with_breaks.append(result.strip())

# Subtitle name parts
first_part_subtitle_name = 'image'
index_of_subtitle = 1
second_part_subtitle_name = '.png'
font = ImageFont.truetype("LiberationSans-Regular.ttf", 35)
padding = 10

# Generate image for each subtitle
for subtitle in subtitles_with_breaks:
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
    filename = first_part_subtitle_name + str(index_of_subtitle) + second_part_subtitle_name
    img.save(filename)
    index_of_subtitle += 1
