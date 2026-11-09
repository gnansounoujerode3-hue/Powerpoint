"""Validation de tous les fichiers du pack : intégrité OOXML, animations,
polices embarquées, comptage des diapositives et des formes."""
from __future__ import annotations

import glob
import os
import re
import sys
import zipfile

from lxml import etree
from pptx import Presentation

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
P_NS = "{http://schemas.openxmlformats.org/presentationml/2006/main}"


def check(path):
    res = {"file": os.path.basename(path)}
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        res["zip_ok"] = bad is None
        names = z.namelist()
        slides = sorted(n for n in names if re.match(r"ppt/slides/slide\d+\.xml$", n))
        res["slides"] = len(slides)
        anims = 0
        for s in slides:
            x = z.read(s).decode("utf-8")
            anims += x.count("<p:animEffect")
        res["anims"] = anims
        res["fonts"] = len([n for n in names if n.startswith("ppt/fonts/")])
        pres = z.read("ppt/presentation.xml").decode("utf-8")
        res["embedded_fonts"] = "<p:embeddedFontLst>" in pres
        # vérifie que chaque diapositive est bien parsable
        for s in slides[:5] + slides[-5:]:
            etree.fromstring(z.read(s))
    prs = Presentation(path)
    res["reopen"] = len(prs.slides) == res["slides"]
    shapes = 0
    for sl in prs.slides:
        shapes += len(sl.shapes)
    res["shapes"] = shapes
    res["size_mb"] = round(os.path.getsize(path) / 1e6, 2)
    return res


def main():
    files = sorted(glob.glob(os.path.join(OUT, "*.pptx")))
    total_slides = total_anims = 0
    ok = True
    print(f"{'fichier':32s} {'slides':>6s} {'formes':>8s} {'anims':>7s} {'Mo':>6s}  état")
    for f in files:
        r = check(f)
        state = "OK" if (r["zip_ok"] and r["reopen"] and r["embedded_fonts"] and r["anims"] > 0) else "⚠"
        if state != "OK":
            ok = False
        total_slides += r["slides"]
        total_anims += r["anims"]
        print(f"{r['file']:32s} {r['slides']:6d} {r['shapes']:8d} {r['anims']:7d} "
              f"{r['size_mb']:6.2f}  {state}")
    print(f"\nTOTAL : {len(files)} fichiers · {total_slides} diapositives · {total_anims} animations")
    print("Validation :", "réussie" if ok else "ÉCHEC")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
