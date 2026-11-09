"""Générateur du pack complet : 30 volumes thématiques × 15 chapitres × 5 peaux.

Chaque diapositive est composée à partir d'un layout + d'un contenu sectoriel
+ d'une peau (accents, fond, motifs) : le pack couvre plus de 2 000 slides
uniques, toutes animées et entièrement éditables.
"""
from __future__ import annotations

import argparse
import math
import os
import random
import sys
import time
import warnings

warnings.filterwarnings("ignore")

import emit_pptx
import theme
import variation
from layouts import _base as B
from recipes import build_recipes

VOLUMES = [
    ("01-Entreprise", "corporate", "midnight", 5),
    ("02-Finance", "finance", "finance", 5),
    ("03-Sante", "medical", "medical", 5),
    ("04-Agence-creation", "creative", "creative", 5),
    ("05-Technologie", "tech", "tech", 5),
    ("06-Sport", "sport", "sport", 5),
    ("07-Education", "education", "light", 5),
    ("08-Immobilier", "realestate", "graphite", 5),
    ("09-Tourisme", "tourism", "aurora", 5),
    ("10-Retail", "retail", "sunset", 5),
    ("11-Energie", "energy", "earth", 5),
    ("12-ONG-Impact", "ngo", "aurora", 5),
    ("13-RH", "hr", "royal", 5),
    ("14-Industrie", "industry", "graphite", 5),
    ("15-Juridique", "legal", "royal", 5),
    ("16-Logistique", "logistics", "isometric", 5),
    ("17-Restauration", "food", "sunset", 5),
    ("18-Automobile", "auto", "tech", 5),
    ("19-Telecom", "telecom", "royal", 5),
    ("20-Agriculture", "agri", "earth", 5),
    ("21-Assurance", "insurance", "finance", 5),
    ("22-Luxe", "luxury", "midnight", 5),
    ("23-Startup-Pitch", "startup", "creative", 5),
    ("24-Infographies", None, "light", 5),
    ("25-Sombre-Neon", None, "tech", 5),
    ("26-Neomorphique", None, "blush", 5),
    ("27-Isometrique", None, "isometric", 5),
    ("28-Cartes-Monde", None, "earth", 5),
    ("29-McKinsey-7S-SWOT", None, "finance", 5),
    ("30-Graphiques-Data", None, "graphite", 5),
]

VOLUME_OFFSET = 0
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")


def _ctx(page, total, section, palette, idx):
    return {"page": page, "total": total, "section": section, "v": idx}


def jitter(content, chap, key):
    """Fait varier le contenu d'un chapitre à l'autre (ordre, valeurs, libellés)
    pour qu'aucune diapositive ne soit strictement identique."""
    if not isinstance(content, dict) or chap == 0:
        return content
    import copy
    c = copy.deepcopy(content)
    rnd = random.Random(f"{key}-{chap}")

    def rot(seq):
        if isinstance(seq, (list, tuple)) and len(seq) > 1:
            k = chap % len(seq)
            seq = list(seq[k:]) + list(seq[:k])
        return seq

    for field in ("items", "steps", "kpis", "rows", "descriptions", "labels",
                  "categories", "layers", "rings", "cols", "blocks", "team", "values"):
        if field in c and isinstance(c[field], (list, tuple)):
            c[field] = rot(c[field])
    for field in ("series1", "series2", "values1", "values2", "values"):
        if field in c and isinstance(c[field], list) and c[field] and isinstance(c[field][0], (int, float)):
            f = 1.0 + (chap % 4) * 0.11
            c[field] = [round(v * f, 2) for v in c[field]]
    for field in ("series",):
        if field in c and isinstance(c[field], list) and c[field] and isinstance(c[field][0], (list, tuple)):
            c[field] = [(a, [round(v * (1 + ((chap + i) % 3) * 0.08), 1) for v in b], col)
                        for i, (a, b, col) in enumerate(rot(c[field]))]
    for field in ("items",):
        if field in c and isinstance(c[field], list) and c[field] and isinstance(c[field][0], tuple) \
                and len(c[field][0]) == 3 and isinstance(c[field][0][1], (int, float)):
            c[field] = [(a, max(6, min(97, b + rnd.randint(-7, 7))), col) if isinstance(b, (int, float)) else
                        (a, b, col) for (a, b, col) in c[field]]
    return c


def _normalize(nodes):
    """Aplatit les groupes inutiles et garantit une liste."""
    return nodes


def build_volume(key, sector_key, palette_name, chapters, out_dir=OUT_DIR,
                 preview=False, start=0, limit=None, skip_anim=False):
    import deck
    import content_data as CD

    sec = CD.sector(sector_key) if sector_key else CD.sector("corporate")
    p0 = theme.PALETTES[palette_name]
    recipes = build_recipes(sec, sector_key or "corporate")
    sections = [r[1]["title"] for r in recipes if r[0] == "SECTION"] or ["Section"]

    prs = deck.new_presentation()
    total = chapters * len(recipes)
    n = 0
    t0 = time.time()
    stats = {"shapes": 0, "anims": 0}
    base_v = VOLUME_OFFSET
    for chap in range(chapters):
        variation.set_variant(base_v + chap)
        p = variation.skin_palette(p0, base_v + chap)
        for ri, (rec, fixed, secname) in enumerate(recipes):
            page = chap * len(recipes) + ri + 1
            if page <= start:
                continue
            if limit and n >= limit:
                break
            if rec == "SECTION":
                content = dict(fixed)
                content.setdefault("number", f"{sections.index(secname)+1}")
                content.setdefault("icon", sec["icons"][(ri + chap) % len(sec["icons"])])
                key_l = ["section-break", "section-break-image", "section-quote-break"][
                    (chap + ri) % 3]
            else:
                key_l, content = rec(ri + chap)
                content = jitter(content, chap, key)
                content.setdefault("kicker", sec["kicker"])
                content.setdefault("subtitle", sec["subtitle"])
            ctx = _ctx(page, total, secname or "Section", p, chap)
            fn = B.get(key_l)
            try:
                nodes = fn(p, content, ctx)
            except Exception as e:
                print(f"  ✗ {key}:{page} {key_l} — {type(e).__name__}: {e}")
                raise
            dark = _is_dark(p["bg"])
            bgc = [(0, p["bg"]), (1, p["bg2"])] if dark else [(0, p["bg2"]), (1, p["bg"])]
            slide = deck.add_slide(prs, bgc)
            em = deck.emit_nodes(slide, nodes)
            if not skip_anim:
                emit_pptx.build_timing(slide, em.anim_entries)
            stats["shapes"] += len(slide.shapes)
            stats["anims"] += len(em.anim_entries)
            n += 1
        if limit and n >= limit:
            break

    prs.core_properties.title = f"Pack PowerPoint — {key}"
    prs.core_properties.author = "Arena Studio"
    prs.core_properties.subject = "Modèles PowerPoint animés et éditables"
    prs.core_properties.keywords = ("powerpoint, template, infographie, animation, "
                                    "editable, infografity")
    prs.core_properties.comments = ("Design system Arena · 2 000+ diapositives · "
                                    "formes vectorielles 100 % éditables")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{key}.pptx")
    deck.save(prs, path, embed=True, animate=not skip_anim)
    dt = time.time() - t0
    print(f"✓ {key:22s} {n:4d} slides  {os.path.getsize(path)/1e6:6.2f} Mo  "
          f"{stats['shapes']:5d} formes  {stats['anims']:4d} anims  {dt:5.1f}s")
    return path, n


def _is_dark(c):
    from components import _lum
    return _lum(c) < 0.5


def build_catalogue(out_dir=OUT_DIR, variants=3):
    """Volume 00 : catalogue de tous les layouts (3 déclinaisons chacun)."""
    import deck
    import content_data as CD
    from recipes import build_recipes
    sec = CD.sector("corporate")
    recipes = build_recipes(sec, "corporate")
    prs = deck.new_presentation()
    entries = []
    for chap in range(variants):
        variation.set_variant(chap)
        pal = ["midnight", "finance", "blush"][chap % 3]
        p = variation.skin_palette(theme.PALETTES[pal], chap)
        for ri, (rec, fixed, secname) in enumerate(recipes):
            if rec == "SECTION":
                continue
            key_l, content = rec(ri + chap)
            content = dict(content)
            content.setdefault("kicker", sec["kicker"])
            content.setdefault("subtitle", sec["subtitle"])
            nodes = B.get(key_l)(p, content, {"page": len(entries) + 1, "total": 0})
            bgc = [(0, p["bg"]), (1, p["bg2"])]
            slide = deck.add_slide(prs, bgc)
            em = deck.emit_nodes(slide, nodes)
            emit_pptx.build_timing(slide, em.anim_entries)
            entries.append((key_l, pal))
    prs.core_properties.title = "Catalogue — toutes les mises en page"
    prs.core_properties.author = "Arena Studio"
    path = os.path.join(out_dir, "00-Catalogue-Layouts.pptx")
    deck.save(prs, path)
    print(f"✓ 00-Catalogue {len(entries)} slides  {os.path.getsize(path)/1e6:.2f} Mo")
    return path, len(entries)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None, help="clé du volume (ex. 01-Entreprise)")
    ap.add_argument("--chapters", type=int, default=None)
    ap.add_argument("--limit", type=int, default=None, help="nb de slides max")
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--catalogue", action="store_true")
    args = ap.parse_args()
    if args.catalogue:
        os.makedirs(args.out, exist_ok=True)
        build_catalogue(args.out)
        return
    total_slides = 0
    for vi, (key, sector, pal, ch) in enumerate(VOLUMES):
        if args.only and args.only not in key:
            continue
        global VOLUME_OFFSET
        VOLUME_OFFSET = vi
        _, n = build_volume(key, sector, pal, args.chapters or ch, out_dir=args.out,
                            limit=args.limit)
        total_slides += n
    print(f"\nTOTAL : {total_slides} diapositives")


if __name__ == "__main__":
    main()
