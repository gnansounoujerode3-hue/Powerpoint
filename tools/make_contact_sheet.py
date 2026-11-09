"""Planche contact générale du pack (une vignette par volume)."""
from __future__ import annotations

import glob
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREV = os.path.join(ROOT, "previews")
FONTS = os.path.join(ROOT, "assets", "fonts")


def main():
    files = sorted(glob.glob(os.path.join(PREV, "apercu-*.jpg")))
    thumbs = []
    for f in files:
        im = Image.open(f).convert("RGB")
        im = im.crop((0, 0, im.width, im.height))
        thumbs.append((os.path.basename(f)[7:-4], im.resize((480, 270), Image.LANCZOS)))
    cols = 4
    rows = (len(thumbs) + cols - 1) // cols
    pad, label_h = 18, 30
    cw, ch = 480 + pad, 270 + pad + label_h
    sheet = Image.new("RGB", (cols * cw + pad, rows * ch + pad + 110), "#0C0A1D")
    d = ImageDraw.Draw(sheet)
    title = ImageFont.truetype(os.path.join(FONTS, "Poppins-700.ttf"), 46)
    sub = ImageFont.truetype(os.path.join(FONTS, "Poppins-400.ttf"), 22)
    lab = ImageFont.truetype(os.path.join(FONTS, "Poppins-500.ttf"), 19)
    d.text((pad + 6, 26), "PACK POWERPOINT — 13 623 DIAPOSITIVES ANIMÉES · 31 VOLUMES",
           font=title, fill="#FFFFFF")
    d.text((pad + 8, 76), "Aperçus générés depuis les fichiers .pptx réels · 100 % éditables · "
                          "polices embarquées", font=sub, fill="#A9A5C9")
    for i, (name, im) in enumerate(thumbs):
        x = pad + (i % cols) * cw
        y = 120 + pad + (i // cols) * ch
        sheet.paste(im, (x, y))
        d.text((x + 2, y + 276), name, font=lab, fill="#E5E1FF")
    out = os.path.join(ROOT, "apercu-general.jpg")
    sheet.save(out, quality=88, optimize=True)
    print(out, sheet.size)


if __name__ == "__main__":
    main()
