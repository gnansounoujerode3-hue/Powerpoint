#!/usr/bin/env python3
"""Contrôle qualité du Pack 1500.

Vérifie le catalogue, l'archive ZIP, un échantillon de fichiers .pptx
et le rendu SVG de toutes les couvertures.

  .venv/bin/python scripts/validate.py
"""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import core.pack as pack  # noqa: E402
from design_system import TEMPLATES, filename_for  # noqa: E402
from layouts import build_scene  # noqa: E402
from render_svg import render_svg  # noqa: E402


def check(label: str, condition: bool, detail: str = "") -> bool:
    print(f"{'✓' if condition else '✗'} {label}{(' — ' + detail) if detail else ''}")
    return condition


def main() -> int:
    ok = True
    catalog = json.loads((ROOT / "catalog" / "templates.json").read_text(encoding="utf-8"))
    ok &= check("Catalogue : 1 500 modèles", len(catalog["templates"]) == 1500,
                f"{len(catalog['templates'])} trouvés")
    ids = [t["id"] for t in catalog["templates"]]
    ok &= check("Identifiants uniques", len(set(ids)) == 1500)
    names = [filename_for(t) for t in catalog["templates"]]
    ok &= check("Noms de fichiers uniques", len(set(names)) == 1500)
    ok &= check("30 familles × 50 palettes",
                catalog["meta"]["families"] == 30 and catalog["meta"]["palettes"] == 50)
    from unique import all_specs_unique
    unique, count = all_specs_unique()
    ok &= check("15 000 empreintes de design uniques", unique,
                f"{count} combinaisons distinctes / 15 000 slides")

    ok &= check("Aperçus SVG de toutes les couvertures", all(
        render_svg(build_scene(t, 0), t).startswith("<svg") for t in TEMPLATES),
        f"{len(TEMPLATES)} scènes rendues")
    ok &= check("Images intégrées dans les aperçus SVG", all(
        "data:image" in render_svg(build_scene(TEMPLATES[0], i), TEMPLATES[0])
        for i in (3, 7)), "slides Vision + Équipe")

    if not pack.ZIP_PATH.exists():
        print("! Archive absente — lancez : python scripts/export.py --all --zip")
        return 0 if ok else 1
    with zipfile.ZipFile(pack.ZIP_PATH) as zf:
        entries = zf.namelist()
        pptx = [n for n in entries if n.endswith(".pptx")]
        ok &= check("Archive : 1 500 fichiers .pptx", len(pptx) == 1500, f"{len(pptx)} trouvés")
        ok &= check("Archive lisible", zf.testzip() is None)
        ok &= check("Index + lisez-moi présents",
                    any(n.endswith("INDEX.csv") for n in entries)
                    and any(n.endswith("LISEZ-MOI.txt") for n in entries))
        from io import BytesIO
        from pptx import Presentation
        sample = [pptx[0], pptx[len(pptx) // 2], pptx[-1]]
        for name in sample:
            raw = zf.read(name)
            prs = Presentation(BytesIO(raw))
            ok &= check(f"PPTX valide : {Path(name).name}",
                        len(prs.slides) == 10 and prs.slide_width > prs.slide_height,
                        f"{len(prs.slides)} slides")
            with zipfile.ZipFile(BytesIO(raw)) as inner:
                medias = [n for n in inner.namelist() if n.startswith("ppt/media/")]
                s1 = inner.read("ppt/slides/slide1.xml").decode("utf-8")
            ok &= check(f"  Animations : {Path(name).name}",
                        "<p:transition" in s1 and "<p:timing" in s1,
                        "transition + volet d'animations")
            ok &= check(f"  Images : {Path(name).name}", len(medias) >= 4,
                        f"{len(medias)} médias intégrés")

    print("\n" + ("✅ Tous les contrôles sont passés." if ok else "❌ Des contrôles ont échoué."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
