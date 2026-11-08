"""10 mises en page premium, déclinées par famille graphique et palette.

Chaque modèle produit 10 diapositives 16:9 :
 1 Couverture · 2 Sommaire · 3 Transition · 4 Vision · 5 Chiffres clés
 6 Données · 7 Processus · 8 Équipe · 9 Citation · 10 Clôture
"""
from __future__ import annotations

from design_system import W, H, darken, lighten, luminance
from media import face_key, hero_key
from scene import (Ellipse, Line, Picture, Rect, Scene, Text, Triangle, gradient, wrap)

M = 94                    # marge
CW = W - 2 * M            # largeur de contenu
BOTTOM = H - 96           # limite basse du contenu


# ---------------------------------------------------------------------------
# Briques communes
# ---------------------------------------------------------------------------
def C(t: dict) -> dict:
    return t["colors"]


def deco(scene: Scene, t: dict, area=(0, 0, W, H), strength: float = 1.0) -> None:
    """Motif décoratif propre à la famille, toujours très discret."""
    c, motif = C(t), t["motif"]
    ax, ay, aw, ah = area
    a, a2 = c["accent"], c["accent2"]
    op = (0.13 if t["mode"] == "light" else 0.18) * strength
    r = t["radius"]

    if motif == "lines":
        for i in range(6):
            y = ay + ah * (0.16 + i * 0.13)
            x1 = ax + aw * (0.60 + (i % 3) * 0.05)
            scene.add(Line(x1, y, ax + aw * 0.97, y, a2, 1.2 + (i % 2), op * 1.5))
    elif motif == "bars":
        for i in range(7):
            bh = ah * (0.14 + (i % 4) * 0.10)
            scene.add(Rect(ax + aw * (0.62 + i * 0.052), ay + ah - bh,
                           aw * 0.026, bh, fill=a, radius=min(6, r), opacity=op))
    elif motif == "grid":
        for i in range(1, 8):
            scene.add(Line(ax + aw * i / 8, ay, ax + aw * i / 8, ay + ah, a, 1, op * 0.7))
        for j in range(1, 5):
            scene.add(Line(ax, ay + ah * j / 5, ax + aw, ay + ah * j / 5, a, 1, op * 0.7))
    elif motif == "blobs":
        scene.add(Ellipse(ax + aw * 0.55, ay - ah * 0.25, aw * 0.62, ah * 0.95,
                          fill=gradient(a, a2, 40), opacity=op * 1.5))
        scene.add(Ellipse(ax + aw * 0.76, ay + ah * 0.42, aw * 0.36, ah * 0.62,
                          fill=a2, opacity=op))
        scene.add(Ellipse(ax + aw * 0.40, ay + ah * 0.72, aw * 0.22, ah * 0.30,
                          fill=a, opacity=op))
    elif motif == "circles":
        cx, cy = ax + aw * 0.78, ay + ah * 0.50
        for i in range(5):
            d = min(aw, ah) * (0.32 + i * 0.17)
            scene.add(Ellipse(cx - d / 2, cy - d / 2, d, d, stroke=a, sw=2, opacity=op * 1.6))
        scene.add(Ellipse(cx - 26, cy - 26, 52, 52, fill=a2, opacity=op * 2))
    elif motif == "dots":
        for i in range(9):
            for j in range(5):
                scene.add(Ellipse(ax + aw * (0.58 + i * 0.047), ay + ah * (0.14 + j * 0.17),
                                  6, 6, fill=a if (i + j) % 4 else a2, opacity=op * 2.2))
    elif motif == "blocks":
        scene.add(Rect(ax + aw * 0.63, ay + ah * 0.12, aw * 0.30, ah * 0.42,
                       fill=a, opacity=op, radius=r, rotate=-4))
        scene.add(Rect(ax + aw * 0.76, ay + ah * 0.48, aw * 0.22, ah * 0.34,
                       fill=a2, opacity=op * 1.3, radius=r, rotate=6))
        scene.add(Rect(ax + aw * 0.55, ay + ah * 0.66, aw * 0.14, ah * 0.20,
                       fill=a, opacity=op, radius=r))
    elif motif == "waves":
        for i in range(3):
            d = aw * (0.55 + i * 0.16)
            scene.add(Ellipse(ax + aw * 0.78 - d / 2, ay + ah * 0.52 - d / 2, d, d,
                              stroke=a, sw=3, opacity=op * 1.3))
        scene.add(Ellipse(ax + aw * 0.62, ay + ah * 0.70, aw * 0.30, ah * 0.26,
                          fill=a2, opacity=op))
    elif motif == "triangles":
        scene.add(Triangle(ax + aw * 0.66, ay + ah * 0.12, aw * 0.18, ah * 0.24,
                           fill=a, opacity=op * 1.4, rotate=18))
        scene.add(Triangle(ax + aw * 0.82, ay + ah * 0.52, aw * 0.13, ah * 0.18,
                           fill=a2, opacity=op * 1.6, rotate=-24))
        scene.add(Triangle(ax + aw * 0.60, ay + ah * 0.72, aw * 0.10, ah * 0.14,
                           fill=a, opacity=op, rotate=45))
    elif motif == "arcs":
        cx, cy = ax + aw * 0.80, ay + ah * 0.55
        for i in range(4):
            d = min(aw, ah) * (0.35 + i * 0.20)
            scene.add(Ellipse(cx - d / 2, cy - d / 2, d, d, stroke=a2,
                              sw=10 - i * 1.5, opacity=op * 0.7))


def brand(scene: Scene, t: dict, y: float = 52, x: float = M,
          light: str | None = None, right: bool = True) -> None:
    c = C(t)
    ink = light or c["muted"]
    scene.add(Rect(x, y + 3, 14, 14, fill=light or c["accent"]))
    scene.add(Text(x + 28, y, 360, 26, "VOTRE MARQUE", 15, ink, "mono",
                   bold=True, tracking=1.6))
    if right:
        scene.add(Text(W - M - 360, y, 360, 26, "PRÉSENTATION · 2026", 14, ink,
                       "body", align="right", tracking=1.2))


def chrome(scene: Scene, t: dict, index: int, section: str) -> None:
    c = C(t)
    scene.bg = c["bg"]
    brand(scene, t, right=False)
    scene.add(Line(M, 92, W - M, 92, c["line"], 1.1))
    scene.add(Line(M, H - 82, W - M, H - 82, c["line"], 1.1))
    scene.add(Text(M, H - 66, 600, 24, "PACK 1500  ·  100 % MODIFIABLE", 13,
                   c["muted"], "mono", tracking=1.2))
    scene.add(Text(W - M - 200, H - 66, 200, 24, f"{index:02d} / 10", 13,
                   c["muted"], "mono", align="right", tracking=1.2))
    scene.add(Text(W - M - 360, 50, 360, 26, section.upper(), 14, c["accent"],
                   "body", bold=True, align="right", tracking=1.6))
    # repère d'accent à gauche du titre
    scene.add(Rect(M, 148, 46, 5, fill=c["accent"], radius=2))


def title_block(scene: Scene, t: dict, kicker: str, title: str,
                sub: str = "", y: float = 176, size: float = 62) -> None:
    c = C(t)
    scene.add(Text(M, 124, 800, 26, kicker.upper(), 15, c["accent"], "mono",
                   bold=True, tracking=2.2))
    scene.add(Text(M, y, 1000, 170, title, size, c["ink"], "heading",
                   bold=True, leading=1.08))
    if sub:
        scene.add(Text(M, y + 118, 900, 60, sub, 21, c["muted"], "body", leading=1.35))


def pill(scene: Scene, t: dict, x: float, y: float, w: float, h: float,
         label: str, fill: str | None = None, color: str | None = None) -> None:
    c = C(t)
    scene.add(Rect(x, y, w, h, fill=fill or c["accent"], radius=min(t["radius"] or 2, h / 2) or h / 2))
    scene.add(Text(x, y, w, h, label, 16, color or c["on_accent"], "body",
                   bold=True, align="center", valign="middle", tracking=1.0))


def card(scene: Scene, t: dict, x: float, y: float, w: float, h: float,
         fill: str | None = None, border: str | None = None) -> None:
    c = C(t)
    scene.add(Rect(x, y, w, h, fill=fill or c["surface"], stroke=border or c["line"],
                   sw=1.2, radius=t["radius"]))


def note(text: str) -> str:
    return ("ASTUCE PACK 1500 — " + text +
            " Tous les éléments sont des formes, images et zones de texte PowerPoint natives : "
            "modifiez les couleurs, les polices et les textes en un clic.")


def tag_animations(scene: Scene, t: dict, index: int = 0) -> Scene:
    """Choisit les éléments clés à animer, dans l'ordre de lecture.

    Priorité : images > grands titres > cartes. Maximum 7 effets par slide
    pour rester lisible et professionnel.
    """
    for el in scene.elements:
        el.anim = 0
    candidates: list[tuple[float, float, int, object]] = []
    for i, el in enumerate(scene.elements):
        priority = None
        if isinstance(el, Picture):
            priority = 0
        elif isinstance(el, Text) and el.size >= 34 and el.y < 620:
            priority = 0
        elif (isinstance(el, Rect) and 150 <= el.w <= 1150 and el.h >= 80
              and el.opacity >= 0.9 and not el.rotate and el.fill
              and not isinstance(el.fill, dict)):
            priority = 1
        if priority is not None:
            candidates.append((el.y, el.x, i, el))
    candidates.sort(key=lambda z: (round(z[0] / 45), z[1], z[2]))
    for order, (_, _, _, el) in enumerate(candidates[:7], start=1):
        el.anim = order
    scene.transition = t["archetype"]
    return scene


# ---------------------------------------------------------------------------
# 1 · Couverture
# ---------------------------------------------------------------------------
def slide_cover(t: dict) -> Scene:
    c, s = C(t), Scene("Couverture")
    a, a2, ink, muted = c["accent"], c["accent2"], c["ink"], c["muted"]
    acc, line, soft = c["accent"], c["line"], c["soft"]
    r, ar = t["radius"], t["archetype"]
    head, sub = t["headline"], t["subtitle"]
    s.bg = c["bg"]
    s.note = note("Remplacez le titre, le sous-titre et « VOTRE MARQUE » par les vôtres.")

    if ar == "fullbleed":
        s.bg = gradient(a, darken(a, 0.55), 55, a2 if luminance(a2) > luminance(a) else None)
        fg = "#FFFFFF"  # dégradé toujours suffisamment sombre pour du texte blanc
        s.add(Ellipse(W * 0.62, -220, 740, 740, fill="#FFFFFF", opacity=0.07))
        s.add(Ellipse(W * 0.78, 360, 420, 420, stroke="#FFFFFF", sw=2, opacity=0.16))
        brand(s, t, light=fg)
        s.add(Text(M, 138, 700, 26, "COLLECTION PREMIUM / 2026", 15, fg, "mono",
                   bold=True, tracking=2.4, opacity=0.85))
        s.add(Text(M, 250, 1040, 300, wrap(head, 1040, 104, 0.56), 104, fg,
                   "heading", bold=True, leading=1.04))
        s.add(Text(M, 520, 880, 60, sub, 23, fg, "body", opacity=0.85, leading=1.3))
        pill(s, t, M, 610, 240, 54, "DÉCOUVRIR →", fill=fg, color=a)
        s.add(Text(W - M - 300, H - 70, 300, 26, "01 / 10", 14, fg, "mono",
                   align="right", opacity=0.8))
        return s

    if ar == "split":
        s.add(Rect(700, 0, W - 700, H, fill=gradient(a, darken(a, 0.32), 70)))
        s.add(Ellipse(1030, -110, 300, 300, fill=a2, opacity=0.30))
        s.add(Picture(748, 118, 512, 392, hero_key(t), clip="round", radius=max(6, r)))
        s.add(Rect(748, 118, 512, 392, stroke="#FFFFFF", sw=2, opacity=0.35,
                   radius=max(6, r)))
        s.add(Text(760, 540, 500, 40, "IMAGE A REMPLACER  ·  PACK 1500", 14,
                   "#FFFFFF", "mono", bold=True, tracking=2, align="center", opacity=0.9))
        brand(s, t)
        s.add(Text(M, 138, 540, 26, "PRÉSENTATION PREMIUM", 15, a, "mono",
                   bold=True, tracking=2.4))
        s.add(Text(M, 226, 570, 300, wrap(head, 570, 76, 0.55), 76, ink,
                   "heading", bold=True, leading=1.08))
        s.add(Rect(M, 486, 92, 5, fill=a, radius=2))
        s.add(Text(M, 520, 540, 90, wrap(sub, 540, 22, 0.50), 22, muted,
                   "body", leading=1.35))
        s.add(Text(M, H - 78, 540, 26, "VOTRE MARQUE  ·  2026", 14, muted, "mono",
                   tracking=1.6))
        return s

    if ar == "frame":
        s.add(Rect(46, 46, W - 92, H - 92, stroke=line, sw=2))
        for x, y in ((46, 46), (W - 62, 46), (46, H - 62), (W - 62, H - 62)):
            s.add(Rect(x - 8, y - 8, 24, 24, fill=a))
        brand(s, t, y=88, x=110)
        s.add(Text(110, 178, 700, 26, "DOSSIER DE PRÉSENTATION  /  2026", 15,
                   a, "mono", bold=True, tracking=2.2))
        s.add(Text(110, 250, 1080, 240, wrap(head, 1080, 92, 0.55), 92, ink,
                   "heading", bold=True, leading=1.06))
        s.add(Rect(110, 522, 180, 4, fill=a))
        s.add(Text(110, 556, 880, 60, sub, 22, muted, "body"))
        s.add(Line(110, H - 130, W - 110, H - 130, line, 1))
        s.add(Text(110, H - 110, 500, 26, "STRATÉGIE  ·  DESIGN  ·  IMPACT", 14,
                   muted, "mono", tracking=2))
        s.add(Text(W - 410, H - 110, 300, 26, "01 / 10", 14, muted, "mono", align="right"))
        return s

    if ar == "sidebar":
        s.add(Rect(0, 0, 150, H, fill=a))
        s.add(Rect(0, 0, 150, H, fill=gradient(a, darken(a, 0.35), 90), opacity=0.6))
        for i in range(3):
            s.add(Ellipse(58, 130 + i * 62, 34, 34, stroke=c["on_accent"], sw=2, opacity=0.6))
        s.add(Text(28, 470, 100, 300, "2 0 2 6", 32, c["on_accent"], "mono",
                   bold=True, align="center", valign="middle"))
        x = M + 110
        brand(s, t, y=52, x=x)
        s.add(Text(x, 168, 700, 26, "COLLECTION / PACK 1500", 15, a, "mono",
                   bold=True, tracking=2.2))
        s.add(Text(x, 240, 900, 280, wrap(head, 900, 92, 0.55), 92, ink,
                   "heading", bold=True, leading=1.06))
        s.add(Text(x, 520, 820, 70, sub, 22, muted, "body", leading=1.35))
        s.add(Rect(x, 614, 120, 54, fill=a, radius=min(r, 27)))
        s.add(Text(x, 614, 120, 54, "01", 20, c["on_accent"], "mono",
                   bold=True, align="center", valign="middle"))
        for i in range(4):
            s.add(Rect(x + 140 + i * 60, 636, 42, 8, fill=a2 if i == 0 else line, radius=4))
        return s

    if ar == "grid":
        for i in range(1, 13):
            s.add(Line(i * W / 13, 0, i * W / 13, H, line, 1, 0.75))
        for j in range(1, 8):
            s.add(Line(0, j * H / 8, W, j * H / 8, line, 1, 0.75))
        s.add(Rect(M, 196, 760, 356, fill=soft, radius=max(2, r)))
        brand(s, t)
        s.add(Text(M + 40, 230, 700, 26, "GRILLE / 01 — PRÉSENTATION", 15, a,
                   "mono", bold=True, tracking=2))
        s.add(Text(M + 40, 290, 680, 200, wrap(head, 680, 74, 0.55), 74, ink,
                   "heading", bold=True, leading=1.08))
        s.add(Text(M + 40, 486, 680, 40, sub, 19, muted, "body"))
        for i, label in enumerate(("VISION", "STRATÉGIE", "RÉSULTATS", "SUITE")):
            y = 196 + i * 89
            s.add(Rect(900, y, 340, 78, fill=c["surface"], stroke=line, sw=1, radius=r))
            s.add(Text(920, y, 60, 78, f"0{i + 1}", 26, a, "mono", bold=True,
                       valign="middle"))
            s.add(Text(995, y, 230, 78, label, 19, ink, "body", bold=True,
                       valign="middle", tracking=1.4))
        s.add(Text(M, H - 66, 600, 26, "PACK 1500  ·  MODÈLE ÉDITABLE", 13,
                   muted, "mono", tracking=1.4))
        return s

    if ar == "asymmetric":
        s.add(Ellipse(-190, 90, 560, 560, stroke=a, sw=2, opacity=0.28))
        s.add(Picture(40, 210, 300, 300, hero_key(t), clip="circle"))
        s.add(Ellipse(40, 210, 300, 300, stroke=a, sw=3, opacity=0.55))
        s.add(Text(M + 10, 528, 240, 26, "IMAGE A REMPLACER", 11, muted,
                   "mono", bold=True, tracking=1.2))
        brand(s, t)
        s.add(Text(560, 150, 680, 26, "COLLECTION PREMIUM", 15, a, "mono",
                   bold=True, align="right", tracking=2.4))
        s.add(Text(560, 240, 680, 300, wrap(head, 680, 84, 0.57), 84, ink,
                   "heading", bold=True, align="right", leading=1.06))
        s.add(Rect(W - M - 130, 560, 130, 5, fill=a, radius=2))
        s.add(Text(560, 586, 680, 70, sub, 21, muted, "body", align="right", leading=1.3))
        s.add(Text(M, H - 70, 600, 26, "VOTRE MARQUE  ·  2026", 14, muted, "mono",
                   tracking=1.6))
        return s

    if ar == "editorial":
        s.add(Line(M, 108, W - M, 108, ink, 2))
        s.add(Line(M, 116, W - M, 116, ink, 0.8))
        brand(s, t, y=58, x=M)
        s.add(Text(M, 150, 900, 26, "ÉDITION 2026  /  DOSSIER N° 01", 15, a,
                   "mono", bold=True, tracking=2.4))
        s.add(Text(M, 200, 1120, 250, wrap(head, 1120, 100, 0.56), 100, ink,
                   "heading", bold=True, leading=1.02))
        s.add(Rect(M, 500, W - 2 * M, 170, fill=soft, radius=r))
        s.add(Picture(W - 390, 486, 296, 168, hero_key(t), clip="round", radius=max(4, r)))
        s.add(Text(W - 390, 656, 296, 22, "IMAGE A REMPLACER", 11, muted,
                   "mono", align="right", tracking=1.2))
        s.add(Text(M + 40, 530, 760, 60, sub, 24, ink, "body", leading=1.3))
        s.add(Text(M + 40, 610, 760, 30, "STRATÉGIE  ·  DESIGN  ·  RÉSULTATS", 15,
                   a, "mono", tracking=2))
        s.add(Text(W - M - 200, H - 66, 200, 26, "01 / 10", 14, muted, "mono",
                   align="right"))
        return s

    if ar == "stacked":
        s.add(Ellipse(W / 2 - 40, 120, 80, 80, fill=a, opacity=0.9))
        s.add(Ellipse(W / 2 - 24, 136, 48, 48, fill=c["on_accent"], opacity=0.85))
        s.add(Text(M, 230, CW, 220, wrap(head, CW, 90, 0.56), 90, ink,
                   "heading", bold=True, align="center", leading=1.06))
        s.add(Text(M, 460, CW, 60, sub, 22, muted, "body", align="center"))
        bands = [(a, 0.95), (a2, 0.75), (soft, 1), (c["line"], 1)]
        for i, (col, o) in enumerate(bands):
            s.add(Rect(0, 560 + i * 48, W, 48, fill=col, opacity=o))
        s.add(Text(M, H - 40, 700, 26, "VOTRE MARQUE  ·  PACK 1500", 13,
                   c["on_accent"] if luminance(a) < 0.5 else ink, "mono", tracking=1.8))
        s.add(Text(W - M - 200, H - 40, 200, 26, "01 / 10", 13, muted, "mono",
                   align="right"))
        return s

    if ar == "diagonal":
        s.add(Rect(-180, 250, 1700, 280, fill=a, rotate=-11, opacity=0.96))
        s.add(Rect(-180, 250, 1700, 280, fill=gradient(a, a2, 20), rotate=-11, opacity=0.28))
        s.add(Ellipse(1050, -160, 420, 420, fill=a2, opacity=0.20))
        brand(s, t)
        s.add(Text(M, 160, 800, 26, "PACK 1500  /  COLLECTION 2026", 15, a,
                   "mono", bold=True, tracking=2.2))
        fg = c["on_accent"]
        s.add(Text(M, 315, 1060, 150, wrap(head, 1060, 82, 0.55), 82, fg,
                   "heading", bold=True, leading=1.05))
        # sous-titre sur cartouche : lisible quel que soit le mode clair / nuit
        s.add(Rect(M, 572, 840, 84, fill=c["surface"], opacity=0.95, radius=r))
        s.add(Text(M + 26, 572, 790, 84, wrap(sub, 790, 21, 0.50), 21, ink,
                   "body", valign="middle", leading=1.3))
        s.add(Text(W - M - 240, H - 70, 240, 26, "01 / 10", 14, muted, "mono",
                   align="right"))
        return s

    # centred (par défaut)
    deco(s, t, (0, 0, W, H), 0.75)
    s.add(Rect(W / 2 - 34, 142, 68, 5, fill=a, radius=2))
    s.add(Text(M, 182, CW, 26, "PACK 1500  ·  COLLECTION PREMIUM", 15, a,
               "mono", bold=True, align="center", tracking=3))
    s.add(Text(M, 254, CW, 240, wrap(head, CW, 96, 0.57), 96, ink,
               "heading", bold=True, align="center", leading=1.06))
    s.add(Rect(W / 2 - 90, 500, 180, 3, fill=a))
    s.add(Text(M, 536, CW, 70, sub, 22, muted, "body", align="center", leading=1.3))
    pill(s, t, W / 2 - 110, 622, 220, 50, "VOTRE MARQUE")
    s.add(Text(M, H - 60, CW, 26, "2026  ·  PRÉSENTATION 16:9", 13, muted,
               "mono", align="center", tracking=2))
    return s


# ---------------------------------------------------------------------------
# 2 · Sommaire
# ---------------------------------------------------------------------------
def slide_agenda(t: dict) -> Scene:
    c, s = C(t), Scene("Sommaire")
    chrome(s, t, 2, "Sommaire")
    title_block(s, t, "Le fil de la présentation", "Quatre temps, une seule idée",
                "Un déroulé clair pour garder l'attention du premier au dernier slide.")
    items = [
        ("01", "Vision & contexte", "Comprendre le point de départ"),
        ("02", "Stratégie & parti pris", "Poser les choix structurants"),
        ("03", "Résultats & preuves", "Montrer ce qui change"),
        ("04", "Prochaines étapes", "Décider et passer à l'action"),
    ]
    y0 = 348
    for i, (num, label, desc) in enumerate(items):
        y = y0 + i * 78
        s.add(Rect(M, y, 56, 56, fill=c["soft"] if i else c["accent"], radius=t["radius"]))
        s.add(Text(M, y, 56, 56, num, 20, c["on_accent"] if i == 0 else c["accent"],
                   "mono", bold=True, align="center", valign="middle"))
        s.add(Text(M + 78, y + 2, 520, 34, label, 25, c["ink"], "heading", bold=True))
        s.add(Text(M + 78, y + 36, 620, 24, desc, 15, c["muted"], "body"))
        s.add(Line(M + 78, y + 66, W - M - 250, y + 66, c["line"], 1))
    deco(s, t, (W - 380, 300, 340, 380), 0.9)
    s.add(Rect(W - M - 210, 348, 210, 312, fill=c["panel"], radius=t["radius"]))
    s.add(Text(W - M - 210, 380, 210, 60, "04", 76, c["accent"], "heading",
               bold=True, align="center"))
    s.add(Text(W - M - 190, 470, 170, 90, "SÉQUENCES\nPOUR\nCONVAINCRE", 15,
               c["ink"], "mono", bold=True, align="center", leading=1.5))
    s.note = note("Modifiez les quatre intitulés pour refléter votre propre plan.")
    return s


# ---------------------------------------------------------------------------
# 3 · Transition de section
# ---------------------------------------------------------------------------
def slide_section(t: dict) -> Scene:
    c, s = C(t), Scene("Transition")
    a, a2 = c["accent"], c["accent2"]
    s.bg = gradient(a, darken(a, 0.42), 65)
    fg = "#FFFFFF"
    s.add(Ellipse(W - 420, -180, 700, 700, fill="#FFFFFF", opacity=0.06))
    s.add(Ellipse(W - 300, 250, 420, 420, stroke="#FFFFFF", sw=2, opacity=0.16))
    s.add(Picture(W - 370, 156, 250, 250, hero_key(t), clip="circle"))
    s.add(Ellipse(W - 370, 156, 250, 250, stroke="#FFFFFF", sw=2, opacity=0.38))
    s.add(Text(M, 66, 700, 26, "VOTRE MARQUE  /  PACK 1500", 15, fg, "mono",
               bold=True, tracking=2.2, opacity=0.85))
    s.add(Text(M, 150, 400, 240, "01", 250, fg, "heading", bold=True, opacity=0.22))
    s.add(Rect(M, 380, 110, 6, fill=fg, opacity=0.8, radius=3))
    s.add(Text(M, 420, 1000, 150, "Notre vision", 96, fg, "heading", bold=True))
    s.add(Text(M, 556, 900, 80,
               "Une phrase qui résume la section et donne envie d'aller plus loin.",
               23, fg, "body", opacity=0.86, leading=1.3))
    s.add(Text(W - M - 300, H - 74, 300, 26, "03 / 10", 14, fg, "mono",
               align="right", opacity=0.8))
    s.note = note("Dupliquez ce slide pour chaque nouvelle partie du discours.")
    return s


# ---------------------------------------------------------------------------
# 4 · Vision / deux colonnes
# ---------------------------------------------------------------------------
def slide_vision(t: dict) -> Scene:
    c, s = C(t), Scene("Vision")
    chrome(s, t, 4, "Vision")
    title_block(s, t, "01 / Vision & contexte", "L'idée, en deux colonnes",
                "Un message principal, trois preuves, et un espace visuel à personnaliser.")
    left_w = 560
    s.add(Text(M, 344, left_w, 120,
               wrap("Partez du problème réel, formulez une conviction simple, puis "
                    "donnez au public une raison de vous suivre.", left_w, 22, 0.50),
               22, c["ink"], "body", leading=1.42))
    bullets = ["Un constat partagé et documenté", "Une promesse facile à retenir", "Un bénéfice mesurable"]
    for i, b in enumerate(bullets):
        y = 490 + i * 54
        s.add(Rect(M, y + 8, 14, 14, fill=c["accent"], radius=3))
        s.add(Text(M + 30, y, left_w - 30, 36, b, 19, c["ink"], "body"))
        s.add(Line(M + 30, y + 42, M + left_w, y + 42, c["line"], 1))
    x = M + left_w + 60
    w = W - M - x
    card(s, t, x, 344, w, 320, fill=c["panel"])
    s.add(Rect(x + 28, 372, w - 56, 264, fill=c["soft"], radius=t["radius"]))
    s.add(Picture(x + 28, 372, w - 56, 208, hero_key(t), clip="round",
                  radius=max(4, t["radius"])))
    s.add(Rect(x + 28, 580, w - 56, 56, fill=c["surface"], opacity=0.96,
               radius=max(2, t["radius"])))
    s.add(Text(x + 30, 580, w - 60, 56, "IMAGE A REMPLACER  ·  CLIC DROIT > MODIFIER L'IMAGE",
               12, c["muted"], "mono", bold=True, align="center",
               valign="middle", tracking=1.0))
    s.note = note("Clic droit sur l'image > « Modifier l'image » pour mettre la vôtre.")
    return s


# ---------------------------------------------------------------------------
# 5 · Chiffres clés
# ---------------------------------------------------------------------------
def slide_kpi(t: dict) -> Scene:
    c, s = C(t), Scene("Chiffres clés")
    chrome(s, t, 5, "Résultats")
    title_block(s, t, "02 / Les preuves", "Les chiffres qui parlent",
                "Quatre indicateurs, une lecture immédiate.")
    data = [("+38 %", "Croissance", "sur 12 mois"), ("4,9/5", "Satisfaction", "clients interrogés"),
            ("12 M€", "Valeur créée", "exercice 2026"), ("24", "Marchés", "couverts")]
    gap = 20
    cw = (CW - 3 * gap) / 4
    for i, (big, label, sub) in enumerate(data):
        x = M + i * (cw + gap)
        card(s, t, x, 344, cw, 310, fill=c["surface"])
        s.add(Rect(x + 24, 372, 42, 5, fill=c["accent"] if i % 2 == 0 else c["accent2"], radius=2))
        s.add(Text(x + 24, 400, cw - 48, 100, big, 60, c["accent"] if i % 2 == 0 else c["ink"],
                   "heading", bold=True))
        s.add(Text(x + 24, 512, cw - 48, 34, label.upper(), 18, c["ink"], "body",
                   bold=True, tracking=1.2))
        s.add(Text(x + 24, 550, cw - 48, 28, sub, 15, c["muted"], "body"))
        s.add(Line(x + 24, 596, x + cw - 24, 596, c["line"], 1))
        s.add(Text(x + 24, 606, cw - 48, 26, f"0{i + 1}  /  INDICATEUR", 12,
                   c["muted"], "mono", tracking=1.2))
    s.note = note("Cliquez sur les nombres pour saisir vos propres indicateurs.")
    return s


# ---------------------------------------------------------------------------
# 6 · Données / graphique
# ---------------------------------------------------------------------------
def slide_chart(t: dict) -> Scene:
    c, s = C(t), Scene("Données")
    chrome(s, t, 6, "Données")
    title_block(s, t, "02 / Analyse", "La tendance, sans bruit",
               "Un graphique entièrement composé de formes modifiables.")
    x0, y0, plot_w, plot_h = M, 348, 720, 250
    for i in range(5):
        gy = y0 + i * plot_h / 4
        s.add(Line(x0, gy, x0 + plot_w, gy, c["line"], 1, 0.9))
        s.add(Text(x0 - 46, gy - 12, 40, 24, str(100 - i * 25), 12, c["muted"],
                   "mono", align="right"))
    values = [38, 52, 47, 68, 76, 92]
    labels = ["T1", "T2", "T3", "T4", "T5", "T6"]
    bw = 62
    for i, (v, lab) in enumerate(zip(values, labels)):
        bx = x0 + 38 + i * 112
        bh = plot_h * v / 100
        col = c["accent"] if i < 5 else c["accent2"]
        s.add(Rect(bx, y0 + plot_h - bh, bw, bh, fill=col,
                   radius=min(t["radius"], 10), opacity=0.92))
        s.add(Text(bx, y0 + plot_h - bh - 34, bw, 28, f"{v}", 15, c["ink"],
                   "mono", bold=True, align="center"))
        s.add(Text(bx, y0 + plot_h + 14, bw, 28, lab, 15, c["muted"], "mono",
                   align="center"))
    s.add(Line(x0, y0 + plot_h, x0 + plot_w, y0 + plot_h, c["ink"], 1.5))
    s.add(Text(x0, y0 + plot_h + 44, plot_w, 26, "ÉVOLUTION DE L'INDICATEUR  ·  2026",
               13, c["muted"], "mono", tracking=1.6))
    x = M + plot_w + 46
    w = W - M - x
    card(s, t, x, 348, w, 292, fill=c["panel"])
    s.add(Text(x + 28, 380, w - 56, 26, "LECTURE CLÉ", 14, c["accent"], "mono",
               bold=True, tracking=2))
    s.add(Text(x + 28, 424, w - 56, 90, "+24 %", 70, c["ink"], "heading", bold=True))
    s.add(Text(x + 28, 520, w - 56, 80,
               wrap("Le dernier trimestre confirme la trajectoire. Capitalisez sur ce qui fonctionne.",
                    w - 56, 18, 0.50), 18, c["muted"], "body", leading=1.35))
    s.add(Ellipse(x + 28, 604, 12, 12, fill=c["accent"]))
    s.add(Text(x + 50, 598, 130, 26, "Réalisé", 14, c["muted"], "body"))
    s.add(Ellipse(x + 168, 604, 12, 12, fill=c["accent2"]))
    s.add(Text(x + 190, 598, 130, 26, "Objectif", 14, c["muted"], "body"))
    s.note = note("Ajustez la hauteur des barres ou remplacez-les par un graphique PowerPoint natif.")
    return s


# ---------------------------------------------------------------------------
# 7 · Processus
# ---------------------------------------------------------------------------
def slide_process(t: dict) -> Scene:
    c, s = C(t), Scene("Processus")
    chrome(s, t, 7, "Méthode")
    title_block(s, t, "03 / Méthode", "Quatre étapes, un cap",
                "Un déroulé simple qui montre comment vous tenez vos engagements.")
    steps = [
        ("01", "Écouter", "Cadrer le besoin réel"),
        ("02", "Concevoir", "Prototyper la réponse"),
        ("03", "Déployer", "Livrer avec rigueur"),
        ("04", "Mesurer", "Prouver l'impact"),
    ]
    y = 468
    s.add(Line(M + 60, y, W - M - 60, y, c["line"], 3))
    span = (CW - 120) / 3
    for i, (num, name, desc) in enumerate(steps):
        cx = M + 60 + i * span
        first = i == 0
        s.add(Ellipse(cx - 42, y - 42, 84, 84,
                      fill=c["accent"] if first else c["surface"],
                      stroke=None if first else c["accent"], sw=2.5))
        s.add(Text(cx - 42, y - 42, 84, 84, num, 24,
                   c["on_accent"] if first else c["accent"], "mono", bold=True,
                   align="center", valign="middle"))
        top = i % 2 == 0
        ty = 356 if top else 520
        s.add(Text(cx - 150, ty, 300, 40, name, 28, c["ink"], "heading",
                   bold=True, align="center"))
        s.add(Text(cx - 150, ty + 44, 300, 34, desc, 16, c["muted"], "body",
                   align="center"))
        s.add(Line(cx, ty + (86 if top else -22), cx, y - (44 if top else -44),
                   c["accent"], 1.5, 0.55))
    s.add(Rect(M, 610, CW, 42, fill=c["soft"], radius=t["radius"]))
    s.add(Text(M, 610, CW, 42,
               "LIVRABLE  ·  UN PARCOURS CLAIR, DE LA PREMIÈRE IDÉE AU RÉSULTAT", 14,
               c["ink"], "mono", bold=True, align="center", valign="middle", tracking=1.4))
    s.note = note("Ajoutez ou retirez des étapes selon votre propre méthode.")
    return s


# ---------------------------------------------------------------------------
# 8 · Équipe
# ---------------------------------------------------------------------------
def slide_team(t: dict) -> Scene:
    c, s = C(t), Scene("Équipe")
    chrome(s, t, 8, "Équipe")
    title_block(s, t, "03 / Les personnes", "Celles et ceux qui font",
                "Présentez les visages derrière le projet.")
    people = [
        ("CD", "Camille Diallo", "Direction générale", [90, 74, 62]),
        ("NK", "Noah Kpossa", "Design & produit", [78, 92, 68]),
        ("IA", "Inès Ahouan", "Stratégie & impact", [84, 68, 90]),
    ]
    gap = 24
    cw = (CW - 2 * gap) / 3
    for i, (initials, name, role, bars) in enumerate(people):
        x = M + i * (cw + gap)
        card(s, t, x, 344, cw, 320, fill=c["surface"])
        s.add(Rect(x, 344, cw, 86, fill=c["soft"], radius=t["radius"]))
        s.add(Rect(x, 400, cw, 30, fill=c["soft"]))
        s.add(Ellipse(x + cw / 2 - 58, 378, 116, 116, stroke=c["accent"], sw=2, opacity=0.55))
        s.add(Picture(x + cw / 2 - 52, 384, 104, 104, face_key(t, i), clip="circle"))
        s.add(Text(x + 24, 506, cw - 48, 36, name, 24, c["ink"], "heading",
                   bold=True, align="center"))
        s.add(Text(x + 24, 544, cw - 48, 28, role.upper(), 14, c["accent"],
                   "mono", align="center", tracking=1.2))
        for j, val in enumerate(bars):
            by = 588 + j * 16
            s.add(Rect(x + 60, by, cw - 120, 6, fill=c["line"], radius=3))
            s.add(Rect(x + 60, by, (cw - 120) * val / 100, 6,
                       fill=c["accent"], radius=3, opacity=0.85))
    s.note = note("Clic droit sur chaque portrait > « Modifier l'image » pour mettre vos photos.")
    return s


# ---------------------------------------------------------------------------
# 9 · Citation
# ---------------------------------------------------------------------------
def slide_quote(t: dict) -> Scene:
    c, s = C(t), Scene("Citation")
    s.bg = c["soft"]
    brand(s, t)
    s.add(Line(M, 92, W - M, 92, c["line"], 1.1))
    s.add(Line(M, H - 82, W - M, H - 82, c["line"], 1.1))
    deco(s, t, (0, 0, W, H), 0.7)
    s.add(Text(M - 10, 110, 240, 220, "“", 240, c["accent"], "heading",
               bold=True, opacity=0.30))
    quote = "Une bonne présentation ne montre pas des données : elle rend une décision évidente."
    s.add(Text(M + 120, 240, CW - 240, 260, wrap(quote, CW - 240, 52, 0.52), 52,
               c["ink"], "heading", bold=True, align="center", valign="middle",
               leading=1.22))
    s.add(Rect(W / 2 - 60, 526, 120, 4, fill=c["accent"], radius=2))
    s.add(Text(M, 556, CW, 34, "VOTRE PORTE-PAROLE", 17, c["ink"], "body",
               bold=True, align="center", tracking=2))
    s.add(Text(M, 590, CW, 30, "Directrice générale  ·  Votre marque", 16,
               c["muted"], "body", align="center"))
    s.add(Text(M, H - 66, 600, 24, "PACK 1500  ·  100 % MODIFIABLE", 13,
               c["muted"], "mono", tracking=1.2))
    s.add(Text(W - M - 200, H - 66, 200, 24, "09 / 10", 13, c["muted"], "mono",
               align="right"))
    s.note = note("Utilisez ce slide pour une citation, un témoignage client ou une conviction forte.")
    return s


# ---------------------------------------------------------------------------
# 10 · Clôture
# ---------------------------------------------------------------------------
def slide_end(t: dict) -> Scene:
    c, s = C(t), Scene("Clôture")
    a, a2 = c["accent"], c["accent2"]
    s.bg = gradient(c["bg"], c["soft"], 30) if t["archetype"] not in ("fullbleed", "diagonal") \
        else gradient(a, darken(a, 0.55), 55)
    on_dark = t["archetype"] in ("fullbleed", "diagonal")
    fg = "#FFFFFF" if on_dark else c["ink"]
    muted = "#FFFFFF" if on_dark else c["muted"]
    muted_op = 0.8 if on_dark else 1
    s.add(Ellipse(W - 420, 280, 620, 620, fill=a, opacity=0.10))
    s.add(Ellipse(W - 300, 400, 380, 380, stroke=a, sw=2, opacity=0.30))
    brand(s, t, light=fg)
    s.add(Line(M, 92, W - M, 92, c["line"], 1.1))
    s.add(Text(M, 170, 900, 26, "MERCI DE VOTRE ATTENTION", 15,
               "#FFFFFF" if on_dark else a, "mono",
               bold=True, tracking=2.6, opacity=0.85 if on_dark else 1))
    s.add(Text(M, 240, 900, 200, "Merci.", 150, fg, "heading", bold=True))
    s.add(Text(M, 430, 860, 70,
               "Et maintenant, construisons la suite ensemble.", 26, muted,
               "body", opacity=muted_op))
    pill(s, t, M, 520, 250, 58, "PARLONS-EN →")
    s.add(Line(M, 624, W - M, 624, c["line"], 1.1))
    s.add(Text(M, 648, 420, 28, "contact@votremarque.com", 17, fg, "body", bold=True))
    s.add(Text(M + 430, 648, 360, 28, "+229 01 00 00 00", 17, fg, "body"))
    s.add(Text(W - M - 340, 648, 340, 28, "www.votremarque.com", 17, fg,
               "body", align="right"))
    s.add(Text(W - M - 200, H - 66, 200, 24, "10 / 10", 13, muted, "mono",
               align="right"))
    s.note = note("Mettez vos coordonnées à jour et ajoutez votre logo sur le slide de clôture.")
    return s


SLIDES = [
    slide_cover, slide_agenda, slide_section, slide_vision, slide_kpi,
    slide_chart, slide_process, slide_team, slide_quote, slide_end,
]

SLIDE_LABELS = [
    "Couverture", "Sommaire", "Transition", "Vision", "Chiffres clés",
    "Données", "Processus", "Équipe", "Citation", "Clôture",
]


def build_scene(t: dict, index: int) -> Scene:
    idx = max(0, min(index, len(SLIDES) - 1))
    return tag_animations(SLIDES[idx](t), t, idx)


def build_scenes(t: dict) -> list[Scene]:
    return [build_scene(t, i) for i in range(len(SLIDES))]
