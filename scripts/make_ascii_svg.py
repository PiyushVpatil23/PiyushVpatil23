"""Convert source-prepped.png into a row-by-row animated monochrome ASCII SVG."""
from PIL import Image, ImageEnhance, ImageOps
import html

RAMP = " .`:-=+*cs#%@"
COLS = 72
CHAR_W = 6.2
LINE_H = 9.2
PAD = 10

img = Image.open("source-prepped.png").convert("L")
img = ImageOps.autocontrast(img)
img = ImageEnhance.Contrast(img).enhance(1.15)
ratio = img.height / img.width
rows = max(1, round(COLS * ratio * 0.48))
img = img.resize((COLS, rows))

lines = []
for y in range(rows):
    chars = []
    for x in range(COLS):
        value = img.getpixel((x, y))
        # White -> leading space; black -> densest glyph.
        index = round((255 - value) / 255 * (len(RAMP) - 1))
        chars.append(RAMP[index])
    lines.append("".join(chars).rstrip())

width = PAD * 2 + COLS * CHAR_W
height = PAD * 2 + rows * LINE_H
clips, text = [], []
for i, line in enumerate(lines):
    y = PAD + (i + 1) * LINE_H
    begin = i * 0.045
    clips.append(
        f'<clipPath id="row{i}"><rect x="{PAD}" y="{y-LINE_H+1:.1f}" width="0" height="{LINE_H+2}">'
        f'<animate attributeName="width" from="0" to="{COLS*CHAR_W:.1f}" dur="0.42s" begin="{begin:.3f}s" fill="freeze"/>'
        '</rect></clipPath>'
    )
    text.append(f'<text x="{PAD}" y="{y:.1f}" clip-path="url(#row{i})">{html.escape(line)}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" viewBox="0 0 {width:.0f} {height:.0f}">
<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:7px;fill:#c9d1d9;white-space:pre}}</style>
<defs>{''.join(clips)}</defs>{''.join(text)}</svg>'''
open("piyush-ascii.svg", "w", encoding="utf-8").write(svg)
print("Wrote piyush-ascii.svg")
