"""Bibliothèque de composants de design (style « Infografity »).

Chaque composant renvoie une liste de noeuds IR. Les composants gèrent
l'alignement, les marges, les dégradés, la typographie et les animations.
"""
from __future__ import annotations

import math
from typing import Sequence

import iconlib
from ir import (Arc, Ellipse, Fill, Group, Icon, Line, Poly, Rect, Run, Stroke,
                Text, ellipse, hx, icon_paths, line, mix, poly, rgrad, rect,
                rich, text, vgrad)
from theme import (CONTENT_W, H, MARGIN, PX_PER_IN, T_BODY, T_HERO, T_KICKER,
                   T_SMALL, T_STAT, T_SUB, T_TITLE, W)
from textfit import fit_text, text_width


# ------------------------------------------------------------------ utils
def A(c, a):
    return (hx(c), a)


def tint(c, bg, t):
    return mix(bg, c, t)


def card_fill(p, strength=1.0) -> Fill:
    return Fill(color=p["card"], color2=tint(p["accent"], p["card"], 0.12 * strength),
                angle=115, alpha=1.0)


def panel(p):
    return Fill(color=p["card"], alpha=0.92)


def hair(p, a=0.5):
    return Stroke(color=p["line"], width=1.4, alpha=a)


def shadow(p, a=0.30, blur=34, dist=12):
    return None


# ------------------------------------------------------------------ fond
def background(p, variant=0, style=None):
    """Fond de diapositive : dégradé + halos + motif, selon la peau active."""
    import variation
    style = style or variation.current()["bg_style"]
    motif = variation.current()["motif"]
    n = [rect(0, 0, W, H, fill=Fill(color=p["bg"], color2=p["bg2"], angle=125))]
    if style == "noir":
        n = [rect(0, 0, W, H, fill=Fill(color=p["bg"], color2=mix(p["bg"], "#000000", 0.55),
                                        angle=160))]
    if style == "griddense":
        col = mix(p["bg"], "#FFFFFF", 0.05)
        for x in range(0, W, 48):
            n.append(line(x, 0, x, H, Stroke(color=col, width=1, alpha=0.45)))
        for y in range(0, H, 48):
            n.append(line(0, y, W, y, Stroke(color=col, width=1, alpha=0.45)))
        n.append(ellipse(W * 0.78, H * 0.16, 620,
                         fill=Fill(color=p["accent"], stops=[(0, p["accent"], 0.22), (1, p["accent"], 0)])))
        n.append(ellipse(W * 0.12, H * 0.94, 520,
                         fill=Fill(color=p["accent2"], stops=[(0, p["accent2"], 0.16), (1, p["accent2"], 0)])))
        return n
    if motif == "diag":
        for i in range(-4, 14):
            n.append(line(i * 170, H, i * 170 + H, 0,
                          Stroke(color=mix(p["bg"], p["accent"], 0.35), width=1, alpha=0.28)))
    elif motif == "dots":
        for x in range(80, W, 74):
            for y in range(70, H, 74):
                n.append(ellipse(x, y, 2.2, fill=Fill(color=p["text"], alpha=0.13)))
    if style in ("glow", "mesh"):
        blobs = [
            (0.02, -0.08, 0.30, p["accent"], 0.085),
            (1.0, 0.02, 0.26, p["accent2"], 0.075),
            (0.94, 1.04, 0.28, p["accent3"], 0.065),
        ]
        if variant % 3 == 1:
            blobs = [
                (0.55, -0.26, 0.40, p["accent"], 0.10),
                (-0.06, 0.96, 0.30, p["accent2"], 0.075),
            ]
        elif variant % 3 == 2:
            blobs = [
                (1.04, 0.42, 0.32, p["accent"], 0.09),
                (0.06, 0.96, 0.26, p["accent3"], 0.075),
            ]
        for cx, cy, r, c, a in blobs:
            n.append(ellipse(cx * W, cy * H, r * W, r * W,
                             fill=Fill(color=c, stops=[(0.0, c, a), (0.65, c, a * 0.35), (1.0, c, 0.0)],
                                       radial=True)))
    if motif == "rings":
        for i in range(5):
            n.append(ellipse(W * 0.86, H * 0.50, 260 + i * 110, fill=None,
                             stroke=Stroke(color=p["accent2"], width=1.2, alpha=0.20 - i * 0.03)))
    if style in ("grid", "glow", "mesh") and p["bg"].upper() < "#800000":
        step = 96
        col = mix(p["bg"], "#FFFFFF", 0.06)
        for x in range(0, W, step):
            n.append(line(x, 0, x, H, Stroke(color=col, width=1, alpha=0.5)))
        for y in range(0, H, step):
            n.append(line(0, y, W, y, Stroke(color=col, width=1, alpha=0.5)))
    return n


def soft_background(p, variant=0):
    """Fond clair / néomorphique."""
    n = [rect(0, 0, W, H, fill=Fill(color=p["bg"], color2=p["bg2"], angle=120))]
    for cx, cy, r, c, a in [(0.06, 0.02, 0.32, p["accent"], 0.10), (0.96, 0.98, 0.30, p["accent2"], 0.08)]:
        n.append(ellipse(cx * W, cy * H, r * W, r * W,
                         fill=Fill(color=c, stops=[(0.0, c, a), (1.0, c, 0.0)], radial=True)))
    return n


def neomorph(p, x, y, w, h, radius=32, raised=True, fill=None):
    """Carte néomorphique : ombre basse + reflet clair."""
    base = fill or p["card"]
    if raised:
        s1 = mix(base, "#000000", 0.10)
        s2 = mix(base, "#FFFFFF", 0.85)
        return [rect(x + 6, y + 8, w, h, fill=Fill(color=s1, alpha=0.55), radius=radius),
                rect(x - 5, y - 6, w, h, fill=Fill(color=s2, alpha=0.9), radius=radius),
                rect(x, y, w, h, fill=Fill(color=base), radius=radius)]
    return [rect(x, y, w, h, fill=Fill(color=base, alpha=0.7), radius=radius),
            rect(x, y, w, h, fill=None, stroke=Stroke(color=mix(base, "#000000", 0.12), width=1.5,
                                                      alpha=0.40), radius=radius)]


# ------------------------------------------------------------------ chrome
def kicker(p, x, y, label, color=None, w=None, width_bar=True):
    import variation
    color = color or p["accent"]
    style = variation.current()["kicker"]
    out = []
    if width_bar and style == "bar":
        out.append(rect(x, y + 4, 26, 3, fill=Fill(color=color), radius=2))
        x += 40
    elif width_bar and style == "dot":
        out.append(ellipse(x + 7, y + 13, 6, fill=Fill(color=color)))
        x += 28
    t = Text(x=x, y=y - 8, w=w or 900, h=34, runs=[Run(label.upper(), color=color)],
             size=T_KICKER, bold=True, spacing=3.0, caps=True)
    out.append(t)
    return out


def title(p, x, y, w, s, size=T_TITLE, color=None, bold=True, line_mult=1.10,
          fit_w=None, h=140):
    out = [Text(x=x, y=y, w=w, h=h, runs=[Run(s, color=color or p["text"])], size=size,
                bold=bold, line=line_mult, fit=bool(fit_w))]
    return out


def subtitle(p, x, y, w, s, size=T_SUB, color=None, h=90, line_mult=1.45):
    return [Text(x=x, y=y, w=w, h=h, runs=[Run(s, color=color or p["muted"])],
                 size=size, line=line_mult, fit=True)]


def body(p, x, y, w, h, s, size=T_BODY, color=None, line_mult=1.55, bold=False):
    return [Text(x=x, y=y, w=w, h=h, runs=[Run(s, color=color or p["muted"], bold=bold)],
                 size=size, line=line_mult, fit=True)]


def footer(p, page, total=None, brand="INFOGRAFITY", color=None, style="light"):
    c = color or p["muted"]
    yy = H - 62
    out = [Text(x=MARGIN, y=yy, w=520, h=30, runs=[Run(brand, color=c)], size=19,
                spacing=3.2, bold=True, caps=True)]
    right = f"{page:02d}" + (f" / {total}" if total else "")
    out.append(Text(x=W - MARGIN - 220, y=yy, w=220, h=30, runs=[Run(right, color=c)],
                    size=19, align="right", bold=True, spacing=2.0))
    out.append(rect(MARGIN, yy - 18, W - 2 * MARGIN, 1, fill=Fill(color=p["line"], alpha=0.7)))
    return out


def slide_head(p, kicker_txt, title_txt, sub=None, x=MARGIN, y=76, w=1180,
               size=T_TITLE, color_accent=None, page=None, total=None, brand=True,
               max_title_h=220):
    """En-tête standard : kicker + titre (mesuré) + sous-titre (mesuré) + pied."""
    from textfit import fit_text
    out = []
    out += kicker(p, x, y, kicker_txt, color=color_accent)
    ty = y + 46
    tsize, lines = fit_text([Run(title_txt, color=p["text"])], w, max_title_h, size, 1.10,
                            bold=True, min_size=26)
    th = len(lines) * tsize * 1.10
    out.append(Text(x=x, y=ty, w=w, h=th + 6, runs=[Run(title_txt, color=p["text"])],
                    size=size, bold=True, line=1.10, fit=True))
    if sub:
        sy = ty + th + 10
        sw = min(w, 900)
        ssize, slines = fit_text([Run(sub, color=p["muted"])], sw, 120, T_SUB, 1.42,
                                 min_size=18)
        out.append(Text(x=x, y=sy, w=sw, h=len(slines) * ssize * 1.42 + 6,
                        runs=[Run(sub, color=p["muted"])], size=ssize, line=1.42))
    if page:
        out += footer(p, page, total)
    return out


# ------------------------------------------------------------------ cartes
def card(p, x, y, w, h, radius=26, fill=None, stroke=True, accent=None,
         glow=False, anim="fade", delay=0, key="", alpha=0.92):
    accent = accent or p["accent"]
    f = fill or Fill(color=p["card"], color2=tint(accent, p["card"], 0.10), angle=120, alpha=alpha)
    out = [rect(x, y, w, h, fill=f, radius=radius,
                stroke=Stroke(color=p["line"], width=1.4, alpha=0.85) if stroke else None,
                anim=anim, anim_delay=delay, key=key)]
    return out


def badge(p, x, y, size, icon_name, color=None, radius=None, style="tint",
          icon_scale=0.46, filled=False, anim="zoom", delay=0, key=""):
    """Pastille d'icône (carré arrondi) + icône Lucide."""
    color = color or p["accent"]
    radius = size * 0.30 if radius is None else radius
    out = []
    if filled:
        out.append(rect(x, y, size, size, fill=Fill(color=color), radius=radius, anim=anim,
                        anim_delay=delay, key=key or "badge"))
        icol = "#FFFFFF" if _lum(color) < 0.62 else p["bg"]
    else:
        out.append(rect(x, y, size, size,
                        fill=Fill(color=tint(color, p["card"], 0.22),
                                  color2=tint(color, p["card"], 0.06), angle=120, alpha=1),
                        radius=radius, stroke=Stroke(color=color, width=1.5, alpha=0.45),
                        anim=anim, anim_delay=delay, key=key or "badge"))
        icol = color
    ic = size * icon_scale
    out.append(icon_paths(x + (size - ic) / 2, y + (size - ic) / 2, ic,
                          iconlib.icon_paths(icon_name), color=icol, width=1.9,
                          anim="" if key else anim, anim_delay=delay))
    return out


def _lum(c):
    c = hx(c)
    r, g, b = int(c[0:2], 16) / 255, int(c[2:4], 16) / 255, int(c[4:6], 16) / 255
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def circle_icon(p, cx, cy, r, icon_name, color=None, icon_ratio=0.5, ring=True,
                filled=False, anim="zoom", delay=0, alpha=0.16):
    color = color or p["accent"]
    out = []
    if filled:
        out.append(ellipse(cx, cy, r, fill=Fill(color=color), anim=anim, anim_delay=delay))
        icol = "#FFFFFF" if _lum(color) < 0.62 else p["bg"]
    else:
        out.append(ellipse(cx, cy, r, fill=Fill(color=color, alpha=alpha), anim=anim,
                           anim_delay=delay))
        if ring:
            out.append(ellipse(cx, cy, r, fill=None, stroke=Stroke(color=color, width=1.6, alpha=0.5)))
        icol = color
    ic = r * 2 * icon_ratio
    out.append(icon_paths(cx - ic / 2, cy - ic / 2, ic, iconlib.icon_paths(icon_name), color=icol,
                          width=1.9))
    return out


def chip(p, x, y, label, color=None, size=22, padx=22, h=46, filled=False, icon_name=None, w=None):
    color = color or p["accent"]
    tw = text_width(label, size, True)
    w = w or (tw + 2 * padx + (28 if icon_name else 0) + 12)
    out = []
    if filled:
        out.append(rect(x, y, w, h, fill=Fill(color=color), radius=h / 2))
        col = "#FFFFFF" if _lum(color) < 0.62 else p["bg"]
    else:
        out.append(rect(x, y, w, h, fill=Fill(color=color, alpha=0.13), radius=h / 2,
                        stroke=Stroke(color=color, width=1.2, alpha=0.55)))
        col = color
    tx = x + padx
    if icon_name:
        ic = h * 0.46
        out.append(icon_paths(x + padx - 6, y + (h - ic) / 2, ic, iconlib.icon_paths(icon_name),
                              color=col, width=2.0))
        tx += 22
    out.append(Text(x=tx, y=y + h / 2 - size * 0.78, w=tw + 16, h=h,
                    runs=[Run(label, color=col)], size=size, bold=True))
    return out


def stat(p, x, y, w, value, label, delta=None, color=None, size=T_STAT, align="left",
         icon_name=None, anim="rise", delay=0, label_size=24):
    color = color or p["accent"]
    out = [Text(x=x, y=y, w=w, h=size * 1.28, runs=[Run(value, color=color)], size=size,
                bold=True, align=align, anim=anim, anim_delay=delay, key="stat", fit=True)]
    yy = y + size * 1.06
    out.append(Text(x=x, y=yy + 8, w=w, h=label_size * 2.9, runs=[Run(label, color=p["muted"])],
                    size=label_size, align=align, line=1.32, fit=True))
    if delta is not None:
        col = p["accent2"] if str(delta).startswith("+") else p["accent3"]
        out.append(Text(x=x + (0 if align == "left" else w / 2 - 40), y=yy + label_size * 2.9, w=140, h=30,
                        runs=[Run(delta, color=col, bold=True)], size=21,
                        align="left" if align == "left" else "center"))
    return out


def bullet(p, x, y, w, s, color=None, size=T_BODY, icon_name="check", h=30, dot=True):
    color = color or p["accent"]
    out = []
    if icon_name:
        out.append(icon_paths(x, y + size * 0.18, size * 1.05, iconlib.icon_paths(icon_name),
                              color=color, width=2.4))
    else:
        out.append(ellipse(x + size * 0.3, y + size * 0.62, size * 0.16, fill=Fill(color=color)))
    out.append(Text(x=x + size * 1.55, y=y - 1, w=w - size * 1.6, h=h,
                    runs=[Run(s, color=p["text"])], size=size, line=1.45))
    return out


def progress(p, x, y, w, ratio, color=None, h=8, bg_alpha=0.18, anim="wipe-left",
             delay=0, label=None):
    color = color or p["accent"]
    out = [rect(x, y, w, h, fill=Fill(color=color, alpha=bg_alpha), radius=h / 2)]
    if ratio > 0:
        out.append(rect(x, y, max(h, w * min(1.0, ratio)), h, fill=Fill(color=color),
                        radius=h / 2, anim=anim, anim_delay=delay, key="progress"))
    if label:
        out.append(Text(x=x + w + 18, y=y - 12, w=110, h=32, runs=[Run(label, color=p["text"])],
                        size=22, bold=True))
    return out


def divider(p, x, y, w, color=None, alpha=0.5):
    return [rect(x, y, w, 1, fill=Fill(color=color or p["line"], alpha=alpha))]


def num_badge(p, x, y, n, size=44, color=None, filled=True):
    color = color or p["accent"]
    out = []
    if filled:
        out.append(ellipse(x + size / 2, y + size / 2, size / 2, fill=Fill(color=color)))
        col = "#FFFFFF" if _lum(color) < 0.62 else p["bg"]
    else:
        out.append(ellipse(x + size / 2, y + size / 2, size / 2, fill=None,
                           stroke=Stroke(color=color, width=2)))
        col = color
    out.append(Text(x=x, y=y + size / 2 - size * 0.42, w=size, h=size,
                    runs=[Run(str(n).zfill(2), color=col, bold=True)], size=size * 0.42,
                    align="center"))
    return out


# ------------------------------------------------------------------ animation
def stagger(items, kind="rise", step=90, start=0):
    """Assigne des délais en cascade à une liste de noeuds."""
    i = 0
    for n in items:
        if getattr(n, "anim", None) == "":
            n.anim = kind
            n.anim_delay = start + i * step
            i += 1
    return items
