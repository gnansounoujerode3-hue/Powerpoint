"""Scène vectorielle neutre.

Une scène est une liste de primitives (rectangles, ellipses, traits, textes,
images). Elle est rendue deux fois, à l'identique :
  · en SVG pour les aperçus du site web,
  · en formes/images PowerPoint natives et éditables pour le .pptx.

Coordonnées : 0..1333 × 0..750 (16:9). 1 unité = 0,01 pouce = 9 144 EMU.
Les tailles de texte sont exprimées en unités de scène (100 unités ≈ 72 pt).
`anim` = ordre d'apparition dans la séquence d'animations PowerPoint (0 = aucune).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from design_system import W, H

EMU = 9144
PT_PER_UNIT = 0.72  # 960 pt de large pour 1333 unités

Color = str
Gradient = dict[str, Any]  # {"stops": [(0, "#..."), (1, "#...")], "angle": 45}


def gradient(c1: str, c2: str, angle: float = 35, c3: str | None = None) -> Gradient:
    stops = [(0.0, c1)]
    if c3:
        stops.append((0.55, c3))
    stops.append((1.0, c2))
    return {"stops": stops, "angle": angle}


@dataclass
class Rect:
    x: float
    y: float
    w: float
    h: float
    fill: Color | Gradient | None = None
    stroke: Color | None = None
    sw: float = 1
    radius: float = 0
    opacity: float = 1
    rotate: float = 0
    anim: int = 0
    tag: str = ""


@dataclass
class Ellipse:
    x: float
    y: float
    w: float
    h: float
    fill: Color | Gradient | None = None
    stroke: Color | None = None
    sw: float = 1
    opacity: float = 1
    rotate: float = 0
    anim: int = 0
    tag: str = ""


@dataclass
class Triangle:
    x: float
    y: float
    w: float
    h: float
    fill: Color | Gradient | None = None
    opacity: float = 1
    rotate: float = 0
    anim: int = 0
    tag: str = ""


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float
    stroke: Color
    sw: float = 1
    opacity: float = 1
    dash: bool = False
    anim: int = 0
    tag: str = ""


@dataclass
class Text:
    x: float
    y: float
    w: float
    h: float
    text: str
    size: float = 26
    color: Color = "#111111"
    font: str = "body"            # heading | body | mono | explicit family
    bold: bool = False
    italic: bool = False
    align: str = "left"           # left | center | right
    valign: str = "top"           # top | middle | bottom
    opacity: float = 1
    tracking: float = 0           # unités de scène
    leading: float = 1.22
    upper: bool = False
    anim: int = 0
    tag: str = ""


@dataclass
class Picture:
    """Image réelle, remplaçable dans PowerPoint (clic droit > Modifier l'image).

    `key` identifie un visuel généré par core/media.py.
    `clip` : rect | round | circle
    """
    x: float
    y: float
    w: float
    h: float
    key: str
    clip: str = "rect"
    radius: float = 0
    opacity: float = 1
    anim: int = 0
    tag: str = ""


@dataclass
class Scene:
    title: str = ""
    bg: Color | Gradient = "#FFFFFF"
    elements: list[Any] = field(default_factory=list)
    note: str = ""
    transition: str = "fade"

    def add(self, *items: Any) -> "Scene":
        self.elements.extend(items)
        return self

    @property
    def width(self) -> int:
        return W

    @property
    def height(self) -> int:
        return H


def wrap(text: str, width: float, size: float, ratio: float = 0.52) -> str:
    """Retour à la ligne approximatif, partagé par les deux moteurs de rendu."""
    max_chars = max(6, int(width / (size * ratio)))
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if len(trial) > max_chars and current:
            lines.append(current)
            current = word
        else:
            current = trial
    if current:
        lines.append(current)
    return "\n".join(lines)


def fit_font(t: dict, key: str = "body", svg: bool = False) -> str:
    """Résout heading/body/mono vers une vraie famille de police."""
    from design_system import FONTS
    if key == "mono":
        return "'Courier New', monospace" if svg else "Consolas"
    if key not in ("heading", "body"):
        return key
    field = "svg_heading" if svg else "heading"
    if key == "body":
        field = "svg_body" if svg else "body"
    return FONTS[t["typo"]][field]


def E(x: float) -> int:
    return int(round(x * EMU))
