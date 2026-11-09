"""Icônes Lucide -> chemins normalisés (viewBox 24x24) réutilisables
en SVG (aperçu) et en DrawingML (formes PowerPoint éditables)."""
from __future__ import annotations

import functools
import os
import re

from svgpathtools import parse_path

ICON_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "icons")

_cache: dict[str, list[str]] = {}


def _svg_body(name: str) -> str:
    p = os.path.join(ICON_DIR, name + ".svg")
    if not os.path.exists(p):
        raise KeyError(name)
    return open(p, encoding="utf-8").read()


def icon_paths(name: str) -> list[str]:
    """Liste des attributs 'd' d'une icône Lucide (sans les cercles -> convertis)."""
    if name in _cache:
        return _cache[name]
    body = _svg_body(name)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', body)
    for attrs in re.findall(r"<(circle|ellipse|line|rect|polyline|polygon)([^>]*)/?>", body):
        tag, a = attrs
        g = dict(re.findall(r'([\w-]+)="([^"]+)"', a))
        if tag == "circle":
            cx, cy, r = float(g["cx"]), float(g["cy"]), float(g["r"])
            paths.append(f"M {cx-r} {cy} a {r} {r} 0 1 0 {2*r} 0 a {r} {r} 0 1 0 {-2*r} 0")
        elif tag == "line":
            paths.append(f"M {g['x1']} {g['y1']} L {g['x2']} {g['y2']}")
        elif tag in ("polyline", "polygon"):
            pts = " ".join(g["points"].strip().replace(",", " ").split())
            nums = [float(x) for x in pts.split()]
            d = "M " + " L ".join(f"{nums[i]} {nums[i+1]}" for i in range(0, len(nums), 2))
            if tag == "polygon":
                d += " Z"
            paths.append(d)
        elif tag == "rect":
            x, y = float(g["x"]), float(g["y"])
            w, h = float(g["width"]), float(g["height"])
            rr = float(g.get("rx", 0))
            paths.append(f"M {x+rr} {y} H {x+w-rr} A {rr} {rr} 0 0 1 {x+w} {y+rr} "
                         f"V {y+h-rr} A {rr} {rr} 0 0 1 {x+w-rr} {y+h} H {x+rr} "
                         f"A {rr} {rr} 0 0 1 {x} {y+h-rr} V {y+rr} A {rr} {rr} 0 0 1 {x+rr} {y} Z")
    _cache[name] = paths
    return paths


@functools.lru_cache(maxsize=20000)
def icon_cmds(d: str) -> tuple:
    """Convertit un 'd' SVG en commandes de dessin en coordonnées 24x24."""
    p = parse_path(d)
    cmds: list[tuple] = []
    pending = None
    for seg in p:
        start = (seg.start.real, seg.start.imag)
        if pending != start:
            cmds.append(("M", start))
        if seg.__class__.__name__ == "Line":
            cmds.append(("L", (seg.end.real, seg.end.imag)))
        elif seg.__class__.__name__ == "CubicBezier":
            cmds.append(("C", (seg.control1.real, seg.control1.imag),
                         (seg.control2.real, seg.control2.imag),
                         (seg.end.real, seg.end.imag)))
        elif seg.__class__.__name__ == "QuadraticBezier":
            cmds.append(("C",
                         (seg.start.real + 2 / 3 * (seg.control.real - seg.start.real),
                          seg.start.imag + 2 / 3 * (seg.control.imag - seg.start.imag)),
                         (seg.end.real + 2 / 3 * (seg.control.real - seg.end.real),
                          seg.end.imag + 2 / 3 * (seg.control.imag - seg.end.imag)),
                         (seg.end.real, seg.end.imag)))
        elif seg.__class__.__name__ == "Arc":
            for i in range(1, 13):
                pt = seg.point(i / 12)
                cmds.append(("L", (pt.real, pt.imag)))
        pending = (seg.end.real, seg.end.imag)
    return tuple(cmds)


ICON_NAMES = sorted(f[:-4] for f in os.listdir(ICON_DIR) if f.endswith(".svg"))


def has_icon(name: str) -> bool:
    return os.path.exists(os.path.join(ICON_DIR, name + ".svg"))
