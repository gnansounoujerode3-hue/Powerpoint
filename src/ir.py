"""
IR (Intermediate Representation) de dessin.

Un slide est une liste d'objets Draw émis par un layout. Le même IR est
consommé par deux backends :
  - emit_svg.py   -> aperçu PNG (contrôle qualité visuel)
  - emit_pptx.py  -> formes DrawingML natives (100% éditables + animables)

Coordonnées en "px" sur une grille 1920 x 1080 (1 px = 1/144 pouce).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Sequence

PX = 6350  # EMU par px


# ------------------------------------------------------------------ couleurs
def hx(c: str) -> str:
    c = c.strip()
    if c.startswith("#"):
        c = c[1:]
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    return c.upper()


def mix(a: str, b: str, t: float) -> str:
    a, b = hx(a), hx(b)
    ra, ga, ba = int(a[0:2], 16), int(a[2:4], 16), int(a[4:6], 16)
    rb, gb, bb = int(b[0:2], 16), int(b[2:4], 16), int(b[4:6], 16)
    return "#%02X%02X%02X" % (
        round(ra + (rb - ra) * t),
        round(ga + (gb - ga) * t),
        round(ba + (bb - ba) * t),
    )


def alpha(c: str, a: float) -> tuple[str, float]:
    return hx(c), max(0.0, min(1.0, a))


# ------------------------------------------------------------------ paint
@dataclass
class Fill:
    color: str = "#FFFFFF"
    alpha: float = 1.0
    # dégradé linéaire
    color2: Optional[str] = None
    angle: float = 90.0          # degrés, 0 = gauche->droite
    # dégradé radial
    radial: bool = False
    stops: Optional[Sequence[tuple[float, str, float]]] = None  # (pos, color, alpha)


@dataclass
class Stroke:
    color: str = "#FFFFFF"
    alpha: float = 1.0
    width: float = 1.0
    dash: Optional[str] = None   # 'dash' | 'dot' | 'sysdash'
    cap: str = "flat"            # flat | round
    join: str = "miter"          # miter | round


@dataclass
class Shadow:
    color: str = "#000000"
    alpha: float = 0.35
    blur: float = 24.0
    dist: float = 8.0
    angle: float = 90.0


@dataclass
class Glow:
    color: str = "#7C5CFF"
    alpha: float = 0.55
    radius: float = 18.0


# ------------------------------------------------------------------ noeuds
@dataclass
class Node:
    kind: str = "shape"
    x: float = 0
    y: float = 0
    w: float = 0
    h: float = 0
    key: str = ""                       # identifiant logique (animation)
    anim: str = ""                      # '', 'fade', 'wipe-up', 'fly-left', ...
    anim_delay: int = 0
    name: str = ""
    group: str = ""


@dataclass
class Rect(Node):
    kind: str = "rect"
    fill: Optional[Fill] = None
    stroke: Optional[Stroke] = None
    radius: float = 0.0                 # rayon des coins (px)
    nocap: bool = False


@dataclass
class Ellipse(Node):
    kind: str = "ellipse"
    fill: Optional[Fill] = None
    stroke: Optional[Stroke] = None


@dataclass
class Poly(Node):
    """Polygone / polyligne. pts en coordonnées absolues (px)."""
    kind: str = "poly"
    pts: Sequence[tuple[float, float]] = ()
    closed: bool = True
    fill: Optional[Fill] = None
    stroke: Optional[Stroke] = None
    smooth: bool = False                # courbe Catmull-Rom -> bezier


@dataclass
class Arc(Node):
    kind: str = "arc"
    cx: float = 0
    cy: float = 0
    r: float = 100
    a0: float = 0.0                     # degrés
    a1: float = 180.0
    stroke: Optional[Stroke] = None
    width: float = 10.0                 # épaisseur de l'anneau
    fill: Optional[Fill] = None         # si rempli (camembert)
    pie: bool = False
    inner: float = 0.0                  # 0 = anneau plein, >0 = donut (ratio)


@dataclass
class Line(Node):
    kind: str = "line"
    x1: float = 0
    y1: float = 0
    x2: float = 100
    y2: float = 0
    stroke: Optional[Stroke] = None


@dataclass
class Run:
    text: str
    color: str = "#FFFFFF"
    bold: bool = False
    size: Optional[float] = None
    italic: bool = False
    alpha: float = 1.0
    spacing: float = 0.0                # interlettrage en pt


@dataclass
class Text(Node):
    kind: str = "text"
    runs: Sequence[Run] = ()
    size: float = 16
    color: str = "#FFFFFF"
    bold: bool = False
    align: str = "left"                 # left | center | right
    valign: str = "top"                 # top | middle | bottom
    line: float = 1.2                   # interligne (multiple)
    spacing: float = 0.0
    caps: bool = False
    italic: bool = False
    margins: tuple[float, float, float, float] = (0, 0, 0, 0)
    autofit: bool = True
    rotation: float = 0.0
    anchor_center: bool = False         # x,y = centre du bloc
    fit: bool = False                   # réduit la taille pour tenir


@dataclass
class Icon(Node):
    """Icône Lucide : chemins normalisés dans une viewBox 24x24."""
    kind: str = "icon"
    paths: Sequence[str] = ()           # sous-chemins SVG 'd'
    size: float = 32
    stroke: Optional[Stroke] = None
    color: str = "#FFFFFF"
    fill: Optional[Fill] = None


@dataclass
class Group(Node):
    kind: str = "group"
    children: list = field(default_factory=list)


# ------------------------------------------------------------------ builders
def rect(x, y, w, h, fill=None, stroke=None, radius=0.0, **kw) -> Rect:
    return Rect(x=x, y=y, w=w, h=h, fill=fill, stroke=stroke, radius=radius, **kw)


def ellipse(cx, cy, rx, ry=None, fill=None, stroke=None, **kw) -> Ellipse:
    ry = rx if ry is None else ry
    return Ellipse(x=cx - rx, y=cy - ry, w=2 * rx, h=2 * ry, fill=fill, stroke=stroke, **kw)


def poly(pts, fill=None, stroke=None, closed=True, smooth=False, **kw) -> Poly:
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return Poly(pts=pts, closed=closed, fill=fill, stroke=stroke, smooth=smooth,
                x=min(xs), y=min(ys), w=max(xs) - min(xs), h=max(ys) - min(ys), **kw)


def line(x1, y1, x2, y2, stroke=None, **kw) -> Line:
    return Line(x1=x1, y1=y1, x2=x2, y2=y2,
                x=min(x1, x2), y=min(y1, y2),
                w=abs(x2 - x1), h=abs(y2 - y1),
                stroke=stroke or Stroke(color="#FFFFFF", width=1), **kw)


def text(x, y, w, h, s, size=16, color="#FFFFFF", bold=False, align="left",
         valign="top", line=1.2, spacing=0.0, caps=False, italic=False, **kw) -> Text:
    runs = s if isinstance(s, (list, tuple)) else [Run(str(s), color=color, bold=bold)]
    return Text(x=x, y=y, w=w, h=h, runs=runs, size=size, color=color, bold=bold,
                align=align, valign=valign, line=line, spacing=spacing, caps=caps,
                italic=italic, **kw)


def rich(x, y, w, h, runs, size=16, align="left", valign="top", line=1.2,
         spacing=0.0, **kw) -> Text:
    return Text(x=x, y=y, w=w, h=h, runs=runs, size=size, align=align,
                valign=valign, line=line, spacing=spacing, **kw)


def icon_paths(x, y, size, paths, color="#FFFFFF", width=2.0, alpha_=1.0, **kw) -> Icon:
    return Icon(x=x, y=y, w=size, h=size, paths=paths, size=size,
                stroke=Stroke(color=color, width=width, alpha=alpha_, cap="round", join="round"),
                color=color, **kw)


# ------------------------------------------------------------------ helpers
def vgrad(c1, c2, a1=1.0, a2=1.0, angle=90.0) -> Fill:
    return Fill(color=c1, alpha=a1, color2=c2, angle=angle)


def rgrad(c1, c2, a1=1.0, a2=1.0) -> Fill:
    return Fill(color=c1, alpha=a1, color2=c2, radial=True)
