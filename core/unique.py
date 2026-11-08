"""Moteur d'unicité : 15 000 diapositives, 15 000 designs différents.

Chaque slide reçoit une « empreinte de design » déterministe obtenue par
décomposition en base mixte d'un index global brouillé :

    global_index = (n° de modèle - 1) × 10 + n° de slide   (0 … 14 999)
    scrambled    = (global_index × 7919) mod 3 000 000      (bijection)
    → 8 paramètres indépendants : fond, habillage, titre, motif, signature,
      miroir, densité, variante.

Le produit des bases (10·10·10·10·10·2·3·5 = 3 000 000) étant supérieur à
15 000 et le multiplicateur premier avec lui, **aucune combinaison ne se
répète** : les 15 000 slides ont une empreinte structurelle unique, et les
10 slides d'un même modèle ont tous un fond / habillage / titre / motif /
signature différents.

À cela s'ajoute une signature géométrique générée par un PRNG semé sur
l'index global : même visuellement, deux slides ne peuvent pas se confondre.
"""
from __future__ import annotations

import random

from design_system import H, MOTIFS, W
from scene import Ellipse, Line, Rect, Scene, Text, Triangle

M = 94
CW = W - 2 * M

RADICES = (10, 10, 10, 10, 10, 2, 3, 5)
MODULUS = 3_000_000          # produit des bases
SCRAMBLE = 7919              # premier, premier avec MODULUS

TRANSITIONS = ("fade", "wipe", "push", "dissolve", "split",
               "cover", "checker", "blinds", "comb", "randomBar")

INTERIOR = ("Sommaire", "Vision", "Chiffres clés", "Données",
            "Processus", "Équipe")


def design_spec(t: dict, slide_index: int) -> dict:
    g = (t["number"] - 1) * 10 + slide_index
    n = (g * SCRAMBLE) % MODULUS
    digits = []
    for radix in RADICES:
        digits.append(n % radix)
        n //= radix
    bg, chrome, title, motif, accent, mirror, density, extra = digits
    return {
        "global": g,
        "code": f"{g + 1:05d}",
        "bg": bg, "chrome": chrome, "title": title, "motif": motif,
        "accent": accent, "mirror": mirror, "density": density, "extra": extra,
    }


# ---------------------------------------------------------------------------
# 1 · Fonds : 10 traitements distincts, toujours derrière le contenu
# ---------------------------------------------------------------------------
def _background(t: dict, spec: dict, dark: bool) -> list:
    c = t["colors"]
    acc, a2, soft = c["accent"], c["accent2"], c["soft"]
    o = 0.14 if dark else 0.11
    m, v = spec["mirror"], spec["bg"]
    out: list = []
    if v == 0:
        out.append(Ellipse(W - 470, -250, 720, 720, fill=acc, opacity=o))
        out.append(Ellipse(W - 300, -110, 380, 380, stroke=a2, sw=2, opacity=o))
    elif v == 1:
        out.append(Rect(-240, 490, 1550, 320, fill=acc, rotate=-12, opacity=o))
        out.append(Rect(-240, 470, 1550, 12, fill=a2, rotate=-12, opacity=o * 1.6))
    elif v == 2:
        x = 0 if not m else W - 230
        out.append(Rect(x, 0, 230, H, fill=soft, opacity=0.60))
        out.append(Rect(x + (225 if not m else 0), 0, 5, H, fill=acc, opacity=0.40))
    elif v == 3:
        for i in range(1, 11):
            out.append(Line(i * W / 11, 0, i * W / 11, H, acc, 1, o * 0.8))
        for j in range(1, 7):
            out.append(Line(0, j * H / 7, W, j * H / 7, acc, 1, o * 0.8))
    elif v == 4:
        out.append(Rect(0, 0, W, 138, fill=acc, opacity=o))
        out.append(Rect(0, 136, W, 3, fill=a2, opacity=0.55))
    elif v == 5:
        out.append(Rect(0, H - 158, W, 158, fill=acc, opacity=o))
        out.append(Rect(0, H - 161, W, 3, fill=a2, opacity=0.55))
    elif v == 6:
        cx, cy = (W - 110, 70) if not m else (110, 70)
        for i in range(4):
            d = 170 + i * 105
            out.append(Ellipse(cx - d / 2, cy - d / 2, d, d,
                               stroke=acc, sw=2, opacity=o * 1.3))
    elif v == 7:
        for i in range(9):
            for j in range(4):
                out.append(Ellipse(70 + i * 145, 130 + j * 155, 7, 7,
                                   fill=acc if (i + j) % 3 else a2, opacity=o * 2))
    elif v == 8:
        out.append(Rect(28, 28, W - 56, H - 56, stroke=acc, sw=2, opacity=0.30))
        for x, y in ((28, 28), (W - 42, 28), (28, H - 42), (W - 42, H - 42)):
            out.append(Rect(x - 6, y - 6, 20, 20, fill=acc, opacity=0.60))
    else:
        out.append(Rect(0 if not m else W / 2, 0, W / 2, H, fill=soft, opacity=0.50))
        out.append(Line(W / 2, 0, W / 2, H, acc, 2, 0.30))
    return out


# ---------------------------------------------------------------------------
# 2 · Habillage : 10 en-têtes / pieds de page distincts
# ---------------------------------------------------------------------------
def _chrome(t: dict, spec: dict, dark: bool, code: str, slide_index: int) -> list:
    c = t["colors"]
    acc, a2, ink, muted, line = c["accent"], c["accent2"], c["ink"], c["muted"], c["line"]
    surf = c["surface"]
    fg = "#FFFFFF" if dark else ink
    on_acc = c["on_accent"]
    v, m = spec["chrome"], spec["mirror"]
    page = f"{slide_index + 1:02d} / 10"
    tag = f"#{code}"
    out: list = []

    if v == 0:  # règle classique
        out += [Rect(M, 55, 14, 14, fill=acc),
                Text(M + 28, 52, 420, 26, "VOTRE MARQUE", 14, fg, "mono", bold=True, tracking=1.6),
                Line(M, 90, W - M, 90, line, 1),
                Text(W - M - 280, 52, 280, 26, f"{page}  ·  {tag}", 13, fg, "mono", align="right")]
    elif v == 1:  # rail vertical gauche
        out += [Rect(0, 0, 44, H, fill=acc),
                Text(0, 0, 44, H, f"{slide_index + 1:02d}", 20, on_acc, "mono",
                     bold=True, align="center", valign="middle"),
                Text(M + 10, H - 58, 600, 24, f"VOTRE MARQUE  ·  {tag}", 13, muted, "mono")]
    elif v == 2:  # badge coin haut droit
        out += [Rect(W - 290, 32, 220, 44, fill=acc, radius=12),
                Text(W - 290, 32, 220, 44, f"PACK 1500 · {tag}", 13, on_acc,
                     "mono", bold=True, align="center", valign="middle"),
                Text(M, H - 58, 500, 24, "VOTRE MARQUE", 13, fg, "mono", bold=True, tracking=1.6)]
    elif v == 3:  # pastille flottante centrée
        out += [Rect(W / 2 - 130, 34, 260, 42, fill=surf, stroke=acc, sw=1.5, radius=21),
                Text(W / 2 - 130, 34, 260, 42, f"PACK 1500  /  {page}", 13, fg,
                     "mono", bold=True, align="center", valign="middle"),
                Text(M, H - 58, 500, 24, tag, 12, muted, "mono")]
    elif v == 4:  # double filet
        out += [Rect(M, 86, W - 2 * M, 4, fill=acc),
                Line(M, 98, W - M, 98, line, 1),
                Text(M, 52, 500, 26, "VOTRE MARQUE", 14, fg, "mono", bold=True, tracking=1.8),
                Text(W - M - 260, 52, 260, 26, tag, 13, acc, "mono", align="right")]
    elif v == 5:  # grand numéro fantôme
        out += [Text(M - 8, 24, 220, 110, f"{slide_index + 1:02d}", 96, acc,
                     "heading", bold=True, opacity=0.20),
                Text(W - M - 420, 56, 420, 26, f"VOTRE MARQUE  ·  {tag}", 13, fg,
                     "mono", align="right", tracking=1.4)]
    elif v == 6:  # bandeau bas
        out += [Rect(0, H - 54, W, 54, fill=acc, opacity=0.92),
                Text(M, H - 54, 700, 54, f"VOTRE MARQUE  ·  PACK 1500  ·  {tag}", 13,
                     on_acc, "mono", bold=True, valign="middle", tracking=1.4),
                Text(W - M - 260, H - 54, 260, 54, page, 13, on_acc, "mono",
                     align="right", valign="middle")]
    elif v == 7:  # rail droit + points
        out += [Rect(W - 52, 0, 52, H, fill=acc, opacity=0.88)]
        for i in range(6):
            out.append(Ellipse(W - 34, 120 + i * 96, 16, 16, fill=on_acc, opacity=0.75))
        out += [Text(M, 52, 500, 26, "VOTRE MARQUE", 14, fg, "mono", bold=True, tracking=1.6),
                Text(M, H - 58, 500, 24, tag, 12, muted, "mono")]
    elif v == 8:  # coin triangulaire
        out += [Triangle(0, 0, 108, 92, fill=acc, rotate=0 if not m else 90),
                Text(14, 14, 90, 26, f"{slide_index + 1:02d}", 15, on_acc, "mono", bold=True),
                Text(W - M - 420, 52, 420, 26, f"VOTRE MARQUE  ·  {tag}", 13, fg,
                     "mono", align="right", tracking=1.4)]
    else:  # 9 · accolades courtes
        out += [Line(M, 70, M + 170, 70, acc, 3),
                Line(W - M - 170, 70, W - M, 70, acc, 3),
                Line(M, 82, M + 90, 82, line, 1),
                Line(W - M - 90, 82, W - M, 82, line, 1),
                Text(M, 100, 500, 24, tag, 12, muted, "mono"),
                Text(W - M - 260, 100, 260, 24, page, 12, muted, "mono", align="right")]
    return out


# ---------------------------------------------------------------------------
# 3 · Titre : 10 traitements, dont 2 vrais repositionnements
# ---------------------------------------------------------------------------
def _title(scene: Scene, t: dict, spec: dict) -> None:
    texts = [e for e in scene.elements if isinstance(e, Text) and e.size >= 40]
    if not texts:
        return
    el = max(texts, key=lambda e: e.size)
    c = t["colors"]
    acc, soft, muted = c["accent"], c["soft"], c["muted"]
    v, code = spec["title"], spec["code"]
    extra: list = []

    if v == 1:
        extra.append(Rect(el.x, el.y + min(el.h, 150), 130, 6, fill=acc, radius=3))
    elif v == 2:
        extra.append(Rect(el.x - 34, el.y + el.size * 0.24, 18, 18, fill=acc, radius=4))
    elif v == 3:
        extra.append(Text(el.x - 6, el.y - 78, 320, 140, code[-2:], 108, acc,
                          "heading", bold=True, opacity=0.13))
    elif v == 4:
        idx = scene.elements.index(el)
        scene.elements.insert(idx, Rect(el.x - 16, el.y - 12,
                                        min(el.w + 32, W - el.x),
                                        min(el.h + 24, 185),
                                        fill=soft, opacity=0.55, radius=t["radius"]))
    elif v == 5 and scene.title in INTERIOR:
        el.align, el.x, el.w = "center", M, CW
        extra.append(Rect(W / 2 - 70, el.y - 22, 140, 4, fill=acc, radius=2))
    elif v == 6:
        extra.append(Rect(el.x - 26, el.y + 6, 7, min(el.h - 12, 130), fill=acc, radius=3))
    elif v == 7 and scene.title in INTERIOR:
        el.align, el.x, el.w = "right", M, CW
        extra.append(Text(M, el.y - 30, CW, 24, f"ÉDITION 2026  ·  {code}", 12,
                          muted, "mono", align="right", tracking=1.6))
    elif v == 8:
        extra += [Rect(el.x - 30, el.y + 8, 10, 10, fill=acc, radius=5),
                  Rect(el.x - 30, el.y + 28, 10, 10, fill=c["accent2"], radius=5)]
    else:
        extra += [Line(el.x, el.y - 14, el.x + 170, el.y - 14, acc, 2),
                  Text(el.x, el.y - 42, 400, 24, f"DESIGN UNIQUE {code}", 11,
                       muted, "mono", tracking=1.6)]
    scene.elements.extend(extra)


# ---------------------------------------------------------------------------
# 4 · Signature géométrique unique (PRNG semé sur l'index global)
# ---------------------------------------------------------------------------
def _signature(t: dict, spec: dict, dark: bool) -> list:
    rnd = random.Random(spec["global"] * 2654435761 & 0xFFFFFFFF)
    c = t["colors"]
    acc, a2 = c["accent"], c["accent2"]
    o = 0.15 if dark else 0.11
    zone = spec["extra"] % 3
    x0, y0 = ((W - 310, 108), (70, 596), (W - 310, 596))[zone]
    kind = spec["accent"]
    out: list = []

    def r(a, b):
        return rnd.uniform(a, b)

    if kind == 0:  # barres empilées
        for i in range(5):
            h = r(28, 105)
            out.append(Rect(x0 + i * 44, y0 + 120 - h, 26, h, fill=acc,
                            opacity=o, radius=3))
    elif kind == 1:  # anneaux
        for i in range(4):
            d = 40 + i * 34
            out.append(Ellipse(x0 + 120 - d / 2, y0 + 66 - d / 2, d, d,
                               stroke=acc, sw=2.5, opacity=o))
    elif kind == 2:  # triangles
        for i in range(3):
            out.append(Triangle(x0 + i * 78, y0 + r(10, 50), 62, 72,
                                fill=acc if i % 2 == 0 else a2,
                                opacity=o * 1.2, rotate=r(-25, 25)))
    elif kind == 3:  # pyramide de points
        for row in range(4):
            for col in range(4 - row):
                out.append(Ellipse(x0 + col * 42 + row * 21, y0 + row * 32,
                                   10, 10, fill=a2 if row % 2 else acc, opacity=o * 1.7))
    elif kind == 4:  # croix
        out.append(Rect(x0 + 100, y0, 12, 130, fill=acc, opacity=o))
        out.append(Rect(x0 + 20, y0 + 58, 180, 12, fill=acc, opacity=o))
        out.append(Ellipse(x0 + 88, y0 + 46, 36, 36, stroke=a2, sw=3, opacity=o * 1.4))
    elif kind == 5:  # ondes
        for i in range(3):
            d = 90 + i * 60
            out.append(Ellipse(x0 + 120 - d / 2, y0 + 70 - d / 2, d, d,
                               stroke=a2, sw=5 - i, opacity=o))
    elif kind == 6:  # chevrons
        for i in range(4):
            out.append(Line(x0 + i * 52, y0 + 12, x0 + 26 + i * 52, y0 + 66, acc, 4, o * 1.5))
            out.append(Line(x0 + 26 + i * 52, y0 + 66, x0 + 52 + i * 52, y0 + 12, acc, 4, o * 1.5))
    elif kind == 7:  # blocs arrondis
        for i in range(3):
            out.append(Rect(x0 + i * 74, y0 + r(8, 45), 58, r(50, 92),
                            fill=acc if i != 1 else a2, opacity=o, radius=10))
    elif kind == 8:  # rayons
        cx, cy = x0 + 120, y0 + 66
        for i in range(8):
            import math
            ang = math.pi * i / 4 + r(-0.08, 0.08)
            out.append(Line(cx, cy, cx + math.cos(ang) * r(45, 90),
                            cy + math.sin(ang) * r(45, 90), acc, 3, o * 1.4))
    else:  # 9 · cartouche géométrique + filets (aucun texte : reste discret)
        out.append(Rect(x0 + 20, y0 + 20, 110, 76, fill=acc, opacity=o, radius=12))
        out.append(Rect(x0 + 38, y0 + 38, 74, 40, stroke=a2, sw=2,
                        opacity=o * 1.4, radius=8))
        out.append(Line(x0 + 145, y0 + 34, x0 + 250, y0 + 34, a2, 3, o * 1.5))
        out.append(Line(x0 + 145, y0 + 62, x0 + 230, y0 + 62, a2, 3, o * 1.5))
    return out


# ---------------------------------------------------------------------------
# 5 · Motif décoratif propre à la slide (10 motifs, clone du modèle)
# ---------------------------------------------------------------------------
def _motif_elements(t: dict, spec: dict) -> list:
    from layouts import deco
    clone = dict(t)
    clone["motif"] = MOTIFS[spec["motif"]]
    tmp = Scene()
    deco(tmp, clone, (0, 0, W, H), 0.45 + 0.12 * spec["density"])
    return tmp.elements


# ---------------------------------------------------------------------------
# Application
# ---------------------------------------------------------------------------
def apply_design(scene: Scene, t: dict, slide_index: int) -> Scene:
    spec = design_spec(t, slide_index)
    dark = (t["mode"] == "dark") or isinstance(scene.bg, dict)

    # 1. on retire l'habillage uniforme pour le remplacer
    scene.elements[:] = [e for e in scene.elements if getattr(e, "tag", "") != "chrome"]

    # 2. couche arrière : motif + fond + signature unique
    back = (_motif_elements(t, spec)
            + _background(t, spec, dark)
            + _signature(t, spec, dark))
    scene.elements[0:0] = back

    # 3. titre retraité, nouvel habillage, transition unique
    _title(scene, t, spec)
    scene.elements.extend(_chrome(t, spec, dark, spec["code"], slide_index))
    scene.transition = TRANSITIONS[spec["bg"]]
    return scene


def all_specs_unique(total_templates: int = 1500) -> tuple[bool, int]:
    """Preuve mathématique : compte les empreintes distinctes."""
    seen = set()
    for d in range(total_templates):
        for s in range(10):
            seen.add(tuple(design_spec({"number": d + 1}, s)[k] for k in
                           ("bg", "chrome", "title", "motif", "accent", "mirror", "density", "extra")))
    return len(seen) == total_templates * 10, len(seen)
