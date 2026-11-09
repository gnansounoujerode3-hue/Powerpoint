"""Couvertures, sections, séparateurs, fins — le squelette du pack."""
from __future__ import annotations

import math

import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_HERO, T_KICKER,
                           T_SMALL, T_SUB, T_TITLE, W, bg, cnt, layout)
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths, line,
                poly, rgrad, rect, rich, text, vgrad)


# ============================================================ COUVERTURES
@layout("cover-hero-glow", "Couverture — halo central", "Couvertures", anim="fade")
def cover_hero(p, c, ctx):
    out = bg(p, 0)
    # arc lumineux derrière le titre
    out.append(ellipse(W * 0.5, H * 0.22, 900, 420,
                       fill=Fill(color=p["accent"], stops=[(0, p["accent"], 0.42),
                                                          (0.55, p["accent"], 0.10),
                                                          (1, p["accent"], 0)])))
    for i, (an, r, w, al) in enumerate([(200, 470, 2, 0.55), (215, 540, 1.5, 0.35)]):
        out.append(Arc(cx=W * 0.5, cy=H * 0.24, r=r, a0=an, a1=340,
                       stroke=Stroke(color=p["accent2"], width=w, alpha=al)))
    out += B.kicker(p, MARGIN, 150, c.get("kicker", "Présentation"), p["accent2"])
    out.append(Text(x=MARGIN, y=200, w=1120, h=300,
                    runs=[Run(c["title"], color=p["text"])], size=76, bold=True,
                    line=1.02, fit=True))
    out.append(Text(x=MARGIN, y=470, w=800, h=90, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=34, line=1.42, fit=True))
    # signature
    out += B.chip(p, MARGIN, 610, c.get("tag", "INFOGRAFITY • 2026"), color=p["accent"], size=22)
    if c.get("author"):
        out.append(Text(x=MARGIN, y=672, w=600, h=30, runs=[Run(c["author"], color=p["muted"])],
                        size=23, bold=True, spacing=1.2))
    # anneau décoratif droit
    out.append(ellipse(W - 330, H * 0.58, 210, fill=None, stroke=Stroke(color=p["accent"], width=26, alpha=0.85)))
    out.append(ellipse(W - 330, H * 0.58, 132, fill=None, stroke=Stroke(color=p["accent2"], width=1.6, alpha=0.5)))
    out.append(icon_paths(W - 390, H * 0.58 - 60, 120, iconlib.icon_paths(c.get("icon", "sparkles")),
                          color=p["accent2"], width=1.6))
    out.append(rect(MARGIN, H - 120, 120, 4, fill=Fill(color=p["accent"]), radius=2))
    return out


@layout("cover-split-block", "Couverture — bloc scindé", "Couvertures")
def cover_split(p, c, ctx):
    out = bg(p, 1)
    out.append(rect(W * 0.55, 0, W * 0.45, H, fill=Fill(color=p["accent"], color2=p["accent3"],
                                                        angle=145, alpha=0.95)))
    out.append(poly([(W * 0.55, 0), (W * 0.62, 0), (W * 0.47, H), (W * 0.40, H)],
                    fill=Fill(color=p["bg"], alpha=0.35)))
    out += B.kicker(p, MARGIN, 170, c.get("kicker", "Rapport annuel"), p["accent2"])
    out.append(Text(x=MARGIN, y=214, w=760, h=340, runs=[Run(c["title"], color=p["text"])],
                    size=68, bold=True, line=1.04, fit=True))
    out.append(Text(x=MARGIN, y=560, w=620, h=120, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=30, line=1.5, fit=True))
    out.append(Text(x=MARGIN, y=H - 190, w=520, h=80,
                    runs=[Run(c.get("author", "Votre nom"), color=p["text"], bold=True),
                          Run("\n" + c.get("role", "Direction"), color=p["muted"])],
                    size=25, line=1.5))
    # visuel droit : arcs concentriques
    cx, cy = W * 0.775, H * 0.5
    for i, r in enumerate([300, 232, 164, 96]):
        out.append(ellipse(cx, cy, r, fill=Fill(color="#FFFFFF", alpha=0.05 + i * 0.02)))
    out.append(ellipse(cx, cy, 300, fill=None, stroke=Stroke(color="#FFFFFF", width=1.4, alpha=0.35)))
    out.append(icon_paths(cx - 90, cy - 90, 180, iconlib.icon_paths(c.get("icon", "chart-bar-big")),
                          color="#FFFFFF", width=1.4))
    return out


@layout("cover-minimal-type", "Couverture — typographie XXL", "Couvertures")
def cover_type(p, c, ctx):
    out = bg(p, 2)
    words = c["title"].split(" ")
    out.append(Text(x=MARGIN - 8, y=140, w=W - 2 * MARGIN + 16, h=520,
                    runs=[Run(c["title"], color=p["text"])],
                    size=126, bold=True, line=1.0, fit=True))
    out.append(rect(MARGIN, 690, W - 2 * MARGIN, 1.4, fill=Fill(color=p["line"])))
    out.append(Text(x=MARGIN, y=720, w=700, h=100, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=30, line=1.5, fit=True))
    out.append(Text(x=W - MARGIN - 380, y=724, w=380, h=100,
                    runs=[Run(c.get("kicker", "2026").upper(), color=p["accent"])],
                    size=23, bold=True, align="right", spacing=3))
    return out


@layout("cover-image-frame", "Couverture — cadre média", "Couvertures")
def cover_frame(p, c, ctx):
    out = bg(p, 0)
    x, y, w, h = 690, 110, 1130, 860
    out.append(rect(x + 18, y + 18, w, h, fill=None,
                    stroke=Stroke(color=p["accent"], width=2, alpha=0.6, dash="dash"), radius=34))
    out.append(rect(x, y, w, h, fill=Fill(color=p["bg2"], color2=p["accent"], angle=160, alpha=0.9),
                    radius=34))
    out.append(rect(x, y, w, h, fill=Fill(color=p["bg"], alpha=0.45), radius=34))
    out.append(ellipse(x + w * 0.5, y + h * 0.48, 300,
                       fill=Fill(color=p["accent2"], stops=[(0, p["accent2"], 0.30), (1, p["accent2"], 0)])))
    out.append(icon_paths(x + w / 2 - 130, y + h / 2 - 130, 260,
                          iconlib.icon_paths(c.get("icon", "presentation")), color=p["text"], width=1.1))
    out += B.kicker(p, MARGIN, 190, c.get("kicker", "Studio créatif"), p["accent2"])
    out.append(Text(x=MARGIN, y=234, w=560, h=340, runs=[Run(c["title"], color=p["text"])],
                    size=60, bold=True, line=1.05, fit=True))
    out.append(Text(x=MARGIN, y=560, w=520, h=140, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=29, line=1.5, fit=True))
    out += B.footer(p, ctx.get("page", 1), ctx.get("total"))
    return out


@layout("cover-neomorphism", "Couverture — néomorphique", "Couvertures")
def cover_neo(p, c, ctx):
    out = bg(p, 0)
    cx, cy = 1240, 470
    out += B.neomorph(p, cx - 300, cy - 300, 600, 600, radius=180)
    out.append(ellipse(cx, cy, 190, fill=Fill(color=p["accent"], color2=p["accent2"], angle=140,
                                              alpha=0.95)))
    out.append(icon_paths(cx - 100, cy - 100, 200, iconlib.icon_paths(c.get("icon", "layers")),
                          color="#FFFFFF", width=1.4))
    out += B.kicker(p, MARGIN, 220, c.get("kicker", "Design system"), p["accent"])
    out.append(Text(x=MARGIN, y=262, w=680, h=300, runs=[Run(c["title"], color=p["text"])],
                    size=62, bold=True, line=1.06, fit=True))
    out.append(Text(x=MARGIN, y=580, w=600, h=120, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=29, line=1.55, fit=True))
    out += B.chip(p, MARGIN, 710, c.get("tag", "Nouveau"), color=p["accent"])
    return out


@layout("cover-dark-mesh", "Couverture — mesh sombre", "Couvertures")
def cover_mesh(p, c, ctx):
    out = bg(p, 1, )
    for i in range(5):
        r = 220 + i * 90
        out.append(ellipse(W * 1.02, -60, r, fill=None,
                           stroke=Stroke(color=p["accent"], width=1.2, alpha=0.30 - i * 0.045)))
    out.append(Text(x=MARGIN, y=250, w=1200, h=380, runs=[Run(c["title"], color=p["text"])],
                    size=82, bold=True, line=1.0, fit=True))
    out.append(Text(x=MARGIN, y=640, w=760, h=110, runs=[Run(c.get("subtitle", ""), color=p["muted"])],
                    size=32, line=1.45, fit=True))
    out.append(Text(x=MARGIN, y=120, w=900, h=30,
                    runs=[Run(c.get("kicker", "CONFIDENTIEL").upper(), color=p["accent2"])],
                    size=22, bold=True, spacing=4))
    out.append(rect(MARGIN, 800, 90, 4, fill=Fill(color=p["accent"]), radius=2))
    return out
