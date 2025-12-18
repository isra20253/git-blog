import re
import io
import os
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from PIL import Image, ImageDraw, ImageFont

POST_URL = 'http://127.0.0.1:8000/post_detail/11/'
OUT_PATH = os.path.join(os.path.dirname(__file__), 'post_11_screenshot.png')

html = ''
try:
    req = Request(POST_URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
except Exception as e:
    print('Error fetching page:', e)
    raise SystemExit(1)

# extract title (first <h3>...</h3>)
title_m = re.search(r'<h3>(.*?)</h3>', html, re.S | re.I)
title = title_m.group(1).strip() if title_m else 'Post'

# extract first paragraph content
para_m = re.search(r'<p class="text-justify">(.*?)</p>', html, re.S | re.I)
content = para_m.group(1).strip() if para_m else ''
# strip tags simplistically
content = re.sub(r'<[^>]+>', '', content)
content = (content[:400] + '...') if len(content) > 400 else content

# extract img srcs
img_srcs = re.findall(r"<img[^>]+src=[\"']([^\"']+)[\"']", html, re.I)
# normalize and keep unique
seen = set()
imgs = []
for src in img_srcs:
    if src in seen: continue
    seen.add(src)
    if src.startswith('/'):
        full = 'http://127.0.0.1:8000' + src
    elif src.startswith('http'):
        full = src
    else:
        full = 'http://127.0.0.1:8000/' + src
    imgs.append(full)

# download images
images = []
for url in imgs[:5]:  # limit to 5 images max for screenshot
    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req, timeout=10) as r:
            b = r.read()
            im = Image.open(io.BytesIO(b)).convert('RGB')
            images.append((url, im))
    except Exception as e:
        print('Could not download', url, e)

# Compose an image: width 1000px
W = 1000
padding = 20
y = padding
# estimate height
title_h = 60
content_h = 120
imgs_h = 0
thumbs = []
for (u, im) in images:
    max_w = W - padding*2
    ratio = max(1, im.width / max_w)
    h = int(im.height / ratio)
    imgs_h += h + 10
    thumbs.append((u, im.resize((int(im.width/ratio), h))))

H = padding + title_h + 10 + content_h + 10 + imgs_h + padding
canvas = Image.new('RGB', (W, max(H, 400)), 'white')
draw = ImageDraw.Draw(canvas)

# load default font
try:
    font_title = ImageFont.truetype('arial.ttf', 28)
    font_content = ImageFont.truetype('arial.ttf', 16)
except Exception:
    font_title = ImageFont.load_default()
    font_content = ImageFont.load_default()

# title
draw.text((padding, y), title, fill='black', font=font_title)
y += title_h

# content (wrap)
lines = []
words = content.split()
line = ''
for w in words:
    if len(line + ' ' + w) > 80:
        lines.append(line)
        line = w
    else:
        line = (line + ' ' + w).strip()
if line:
    lines.append(line)

for l in lines[:8]:
    draw.text((padding, y), l, fill='black', font=font_content)
    y += 18

y += 10
# paste images
for (u, im) in thumbs:
    canvas.paste(im, (padding, y))
    y += im.height + 10

canvas.save(OUT_PATH)
print('Screenshot saved to', OUT_PATH)
