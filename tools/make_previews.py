"""Génère des planches d'aperçu PNG pour chaque volume du pack."""
from __future__ import annotations

import glob
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pptx_preview

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "output")
PREV = os.path.join(ROOT, "previews")


def sheet(files, out, cols=3, cell=(640, 360)):
    ims = [Image.open(f).convert("RGB").resize(cell) for f in files]
    rows = (len(ims) + cols - 1) // cols
    sh = Image.new("RGB", (cell[0] * cols, cell[1] * rows), "#0C0A1D")
    for i, im in enumerate(ims):
        sh.paste(im, ((i % cols) * cell[0], (i // cols) * cell[1]))
    sh.save(out)
    return out


def main():
    os.makedirs(PREV, exist_ok=True)
    import random
    for pptx in sorted(glob.glob(os.path.join(OUT, "*.pptx"))):
        name = os.path.basename(pptx)[:-5]
        tmp = os.path.join("/tmp", "prev_" + name)
        from pptx import Presentation
        n = len(Presentation(pptx).slides)
        # 9 diapositives réparties sur tout le volume, tirées de façon déterministe
        # (graine = nom du fichier) pour que chaque planche montre des layouts variés.
        rnd = random.Random(name)
        picks = set()
        for b in range(9):
            lo = int(2 + b * (n - 2) / 9)          # on saute la diapositive « mode d'emploi »
            hi = int(2 + (b + 1) * (n - 2) / 9) - 1
            picks.add(max(1, min(n, rnd.randint(max(lo, 2), max(hi, lo)))))
        picks = sorted(picks)
        try:
            files = pptx_preview.render(pptx, tmp, set(picks))
        except Exception as e:
            print(" !", name, e)
            continue
        if files:
            p = sheet(files, os.path.join(PREV, f"apercu-{name}.png"))
            print("✓", os.path.basename(p))


if __name__ == "__main__":
    main()
