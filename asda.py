# %%
from wand.color import Color
from wand.image import Image
from wand.drawing import Drawing
from wand.compat import nested
import math

import subprocess
import os
import random
import hashlib
import struct
import datetime
import os

random.seed()

def rasterize_text(text):
    img_width = 52
    img_height = 7

    with Drawing() as draw:
        with Image(width=img_width, height=img_height, background=Color('white')) as img:
            draw.font_family = 'Comic Sans'
            draw.font_size = 9.0
            img.font_antialias = True
            draw.push()
            draw.fill_color = Color('hsl(0%, 0%, 0%)')
        
            font_metrics = draw.get_font_metrics(img, text)

            draw.text(img_width - math.floor(font_metrics.text_width), img_height, text)

            # offset = 0

            # for chr in text:
            #     draw.text(offset, 7, chr)
            #     draw.text(offset, 7, chr)

            #     font_metrics = draw.get_font_metrics(img, text[0])
            #     offset += math.floor(font_metrics.text_width) + 1

            draw.pop()        
            draw(img)
            img.threshold(0.5)

            pixels = img.export_pixels(0, 0, channel_map='R')
            transposed_pixels = [ pixels[i % img_height * img_width + i // img_height ] for i in range(len(pixels)) ]

            # print(pixels)
            # print(transposed_pixels)
            # img.save(filename='image.png')

            return transposed_pixels

def get_random_hash():
    m = hashlib.sha256()
    r = random.random()
    m.update(bytearray(struct.pack("d", r)))
    return m.hexdigest()

contributions_text = 'PLETHORA'
commits_per_pixel = 30
repo_path = '/home/g/source/verbose-fiesta'
file_name = 'THE_FILE'
file_path = f'{repo_path}/{file_name}'

pixels = rasterize_text(contributions_text)

today = datetime.datetime.today()
# UTC 8:00 sunday 52 weeks ago
start_date = (today - datetime.timedelta(days=52 * 7 + today.weekday() + 1)).replace(hour=8, minute=0, second=0, microsecond=0)

# for i in range(52):
#     line = [ ('1' if pixels[(i * 7 + j)] == 0 else '0') for j in range(7) ]
#     print(''.join(line))

# init a git repo
p = subprocess.Popen(['git', 'init'], cwd=repo_path)
p.wait()

for i in range(len(pixels)):
    pixel = pixels[i]
    
    if (pixel > 0):
        # empty pixel
        continue

    date = start_date + datetime.timedelta(days=i)

    for j in range(commits_per_pixel):
        commit_time = date + datetime.timedelta(minutes=j*5)

        commit_time_fmt = f'"{commit_time.strftime('%Y-%m-%d %H:%M:%S')}"' 
        # print(commit_time_fmt)

        hash = get_random_hash()

        # update file
        with open(file_path, "w") as file:
            file.write(hash)

        # do commit
        p = subprocess.Popen(['git', 'add', file_name], cwd=repo_path)
        p.wait()

        env = {**os.environ, 'GIT_COMMITTER_DATE': commit_time_fmt}

        p = subprocess.Popen(['git', 'commit', '--date', commit_time_fmt, '-m', hash[:7] ], cwd=repo_path)
        p.wait()

# %%
