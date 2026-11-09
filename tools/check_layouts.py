"""Contrôle automatique de tous les layouts : détecte les éléments hors cadre
ou les textes qui débordent de leur boîte."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import theme
import layouts
from layouts import _base as B
from ir import Text
from recipes import build_recipes
import content_data as CD
from textfit import fit_text


def walk(nodes):
    for n in nodes:
        yield n
        if getattr(n, "children", None):
            yield from walk(n.children)


def is_decor(n):
    """Grandes ellipses de fond / halos : hors cadre par nature."""
    from ir import Ellipse
    import ir
    if not isinstance(n, ir.Ellipse) or n.w < 300:
        return False
    if n.fill is None:
        return True                      # anneau décoratif
    return bool(n.fill.stops or n.fill.color2)
                


def bbox_ok(n, W, H, tol=2):
    try:
        x, y, w, h = n.x, n.y, n.w, n.h
    except AttributeError:
        return True
    if n.__class__.__name__ in ("Line", "Poly", "Icon", "Arc"):
        return True
    return (x >= -tol and y >= -tol and x + w <= W + tol and y + h <= H + tol)


def main():
    p = theme.PALETTES["midnight"]
    sec = CD.sector("corporate")
    recipes = build_recipes(sec, "corporate")
    content_by_layout = {}
    for rec, fixed, _ in recipes:
        if rec == "SECTION":
            for lk in ("section-break", "section-break-image", "section-quote-break"):
                content_by_layout.setdefault(lk, dict(fixed))
            continue
        for i in range(3):
            k, c = rec(i)
            content_by_layout.setdefault(k, c)
    problems = 0
    for key, info in B.REGISTRY.items():
        c = content_by_layout.get(key, {"title": "Titre de test"})
        c.setdefault("kicker", "Kicker")
        try:
            nodes = info["fn"](p, c, {"page": 1, "total": 10})
        except Exception as e:
            print(f"✗ {key}: {type(e).__name__}: {e}")
            problems += 1
            continue
        bad = []
        for n in walk(nodes):
            if is_decor(n):
                continue
            if not bbox_ok(n, theme.W, theme.H):
                bad.append(f"{n.__class__.__name__}({int(n.x)},{int(n.y)},{int(n.w)}x{int(n.h)})")
            if isinstance(n, Text) and n.fit:
                s, lines = fit_text(n.runs, n.w, n.h, n.size, n.line, n.bold)
                if s < n.size * 0.45 and n.size > 20:
                    bad.append(f"texte réduit {int(n.size)}→{int(s)}: {n.runs[0].text[:30]!r}")
        if bad:
            problems += 1
            print(f"⚠ {key}")
            for b in bad[:6]:
                print("    ", b)
    print(f"\n{len(B.REGISTRY)} layouts contrôlés · {problems} à revoir")


if __name__ == "__main__":
    main()
