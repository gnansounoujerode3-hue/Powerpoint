"""Chapitre : infographies (processus, cycles, anneaux, entonnoirs, pyramides,
timelines, équipements, scènes, marketing, arbres, comparaisons)."""
from __future__ import annotations

import math

import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_KICKER, T_SUB,
                           T_TITLE, W, bg, cnt, layout)
from content_data import MONTHS, SECTORS
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths,
                line, poly, rgrad, rect, rich, text, vgrad)


def _anim(nodes, kind="rise", start=0, step=70, only_unset=True):
    i = 0
    for n in nodes:
        if getattr(n, "anim", "") == "" and only_unset:
            n.anim = kind
            n.anim_delay = start + i * step
            i += 1
    return nodes


# ============================================================ PROCESSUS
@layout("process-horizontal", "Processus — 5 étapes", "Infographies de processus")
def process_horizontal(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Méthode", c.get("title", "Notre processus en cinq étapes"),
                        c.get("subtitle", "Une démarche éprouvée, du diagnostic à l'industrialisation."),
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = c.get("steps") or ["Diagnostic", "Cadrage", "Déploiement", "Mesure", "Pilotage"]
    icons = c.get("icons") or ["search", "clipboard-list", "rocket", "gauge", "repeat"]
    n = len(steps)
    y = 560
    x0 = MARGIN + 40
    w = (W - 2 * MARGIN - 80) / n
    out.append(rect(x0 + 40, y + 58, W - 2 * MARGIN - 160, 3, fill=Fill(color=p["line"], alpha=0.9)))
    for i, s in enumerate(steps):
        cx = x0 + w * i + w / 2
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]][i % 5]
        out.append(ellipse(cx, y + 60, 62, fill=Fill(color=col, alpha=0.14),
                           stroke=Stroke(color=col, width=2, alpha=0.65)))
        out.append(ellipse(cx, y + 60, 44, fill=Fill(color=col), anim="zoom", anim_delay=90 * i))
        out.append(icon_paths(cx - 22, y + 38, 44, iconlib.icon_paths(icons[i % len(icons)]),
                              color="#FFFFFF", width=2.0))
        out.append(Text(x=cx - 150, y=y + 150, w=300, h=34,
                        runs=[Run(f"0{i+1}", color=col)], size=20, bold=True, align="center",
                        spacing=2))
        out.append(Text(x=cx - 170, y=y + 186, w=340, h=40, runs=[Run(s, color=p["text"])],
                        size=25, bold=True, align="center"))
        out.append(Text(x=cx - 170, y=y + 232, w=340, h=110,
                        runs=[Run(c.get("descriptions", [
                            "Cadrer les enjeux et les attentes.",
                            "Définir le périmètre et les jalons.",
                            "Exécuter par itérations courtes.",
                            "Mesurer l'impact réel chaque mois.",
                            "Ajuster et industrialiser."][i]), color=p["muted"])],
                        size=19, align="center", line=1.4, fit=True))
    return out


@layout("process-vertical", "Processus — vertical numéroté", "Infographies de processus")
def process_vertical(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Étapes", c.get("title", "Du besoin au résultat"),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    steps = c.get("steps") or ["Écouter", "Concevoir", "Construire", "Lancer", "Améliorer"]
    descs = c.get("descriptions") or [
        "Immersion auprès des équipes et des utilisateurs.",
        "Prototypes rapides, testés en conditions réelles.",
        "Développement itératif et revues hebdomadaires.",
        "Mise en production progressive et accompagnée.",
        "Mesure, apprentissage et optimisation continue.",
    ]
    x = 780
    y0 = 320
    out.append(rect(x + 44, y0 + 20, 2, 460, fill=Fill(color=p["line"])))
    for i, s in enumerate(steps):
        y = y0 + i * 100
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]][i % 5]
        out.append(ellipse(x + 45, y + 20, 26, fill=Fill(color=col), anim="circle", anim_delay=80 * i))
        out.append(Text(x=x + 45 - 26, y=y + 8, w=52, h=30,
                        runs=[Run(str(i + 1), color="#FFFFFF")], size=20, bold=True, align="center"))
        out.append(Text(x=x + 96, y=y - 2, w=380, h=40, runs=[Run(s, color=p["text"])], size=27,
                        bold=True))
        out.append(Text(x=x + 470, y=y, w=620, h=80, runs=[Run(descs[i], color=p["muted"])],
                        size=20, line=1.45, fit=True))
    return out


@layout("process-chevron", "Processus — chevrons", "Infographies de processus")
def process_chevron(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Parcours", c.get("title", "Le parcours client, étape par étape"),
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = c.get("steps") or ["Découverte", "Évaluation", "Achat", "Adoption", "Fidélisation"]
    n = len(steps)
    y = 480
    h = 200
    w = (W - 2 * MARGIN) / n
    cols = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]]
    for i, s in enumerate(steps):
        x = MARGIN + i * w
        notch = 40
        pts = [(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h),
               (x, y + h), (x + notch, y + h / 2)] if i > 0 else \
              [(x, y), (x + w - notch, y), (x + w, y + h / 2), (x + w - notch, y + h), (x, y + h)]
        out.append(poly(pts, fill=Fill(color=cols[i % 5], alpha=0.20 + i * 0.02),
                        stroke=Stroke(color=cols[i % 5], width=1.6, alpha=0.7),
                        anim="wipe-left", anim_delay=90 * i))
        out.append(Text(x=x + 70, y=y + 60, w=w - 130, h=36, runs=[Run(f"0{i+1}", color=cols[i % 5])],
                        size=20, bold=True, spacing=2))
        out.append(Text(x=x + 70, y=y + 96, w=w - 130, h=70, runs=[Run(s, color=p["text"])],
                        size=24, bold=True, line=1.2, fit=True))
    # jalons sous les chevrons
    for i, lab in enumerate(["J+0", "J+15", "J+30", "J+60", "J+90"]):
        out.append(Text(x=MARGIN + i * w + w / 2 - 80, y=y + h + 40, w=160, h=30,
                        runs=[Run(lab, color=p["muted"])], size=19, align="center"))
    return out


@layout("process-steps-cards", "Processus — cartes 4 étapes", "Infographies de processus")
def process_cards(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Mise en œuvre", c.get("title", "Quatre étapes pour démarrer"),
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = c.get("items") or [
        ("Cadrage", "Un atelier de deux heures pour aligner les équipes.", "compass"),
        ("Pilote", "Un périmètre restreint, déployé en trois semaines.", "rocket"),
        ("Mesure", "Des indicateurs partagés et revus chaque mois.", "gauge"),
        ("Généralisation", "Extension progressive à toutes les équipes.", "layers")]
    w = 400
    for i, (t, d, ic) in enumerate(steps):
        x = MARGIN + i * (w + 27)
        y = 400
        out += B.card(p, x, y, w, 400, anim="rise", delay=80 * i)
        out.append(Text(x=x + 30, y=y + 26, w=w - 60, h=90,
                        runs=[Run(f"0{i+1}", color=p["accent"])], size=64, bold=True))
        out += B.circle_icon(p, x + w - 74, y + 78, 34, ic, p["accent2"], alpha=0.18)
        out.append(Text(x=x + 30, y=y + 138, w=w - 60, h=40, runs=[Run(t, color=p["text"])],
                        size=26, bold=True))
        out.append(Text(x=x + 30, y=y + 192, w=w - 60, h=170, runs=[Run(d, color=p["muted"])],
                        size=20, line=1.45, fit=True))
        if i < 3:
            out.append(icon_paths(x + w + 4, y + 190, 20, iconlib.icon_paths("arrow-right"),
                                  color=p["accent"], width=2.2))
    return out


# ============================================================ CYCLES
@layout("cycle-arrows", "Cycle — flèches circulaires", "Infographies sur le cycle")
def cycle_arrows(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Cycle", c.get("title", "Un cycle d'amélioration continue"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    steps = c.get("steps") or ["Planifier", "Déployer", "Vérifier", "Ajuster"]
    cx, cy, r = 640, 610, 250
    n = len(steps)
    cols = [p["accent"], p["accent2"], p["accent3"], p["accent2"]]
    for i in range(n):
        a0 = -90 + 360 * i / n + 5
        a1 = -90 + 360 * (i + 1) / n - 5
        out.append(Arc(cx=cx, cy=cy, r=r, a0=a0, a1=a1, fill=Fill(color=cols[i % 4]),
                       inner=0.78, anim="fade", anim_delay=90 * i))
        mid = math.radians((a0 + a1) / 2)
        # flèche
        tip = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        bx = (cx + (r * 0.78) * math.cos(math.radians(a1)), cy + (r * 0.78) * math.sin(math.radians(a1)))
        out.append(poly([tip, bx], fill=None, closed=False,
                        stroke=Stroke(color=cols[i % 4], width=4)))
        lx, ly = cx + (r * 0.885) * math.cos(mid), cy + (r * 0.885) * math.sin(mid)
        out.append(Text(x=lx - 130, y=ly - 40, w=260, h=80,
                        runs=[Run(steps[i], color="#FFFFFF")], size=24, bold=True,
                        align="center", line=1.15))
    out.append(Text(x=cx - 200, y=cy - 46, w=400, h=60, runs=[Run(c.get("center", "Itérer"),
                                                                  color=p["text"])],
                    size=36, bold=True, align="center"))
    out.append(Text(x=cx - 200, y=cy + 12, w=400, h=30, runs=[Run(c.get("center_sub", "en continu"),
                                                                  color=p["muted"])],
                    size=19, align="center", caps=True, spacing=2))
    # légende à droite
    for i, s in enumerate(steps):
        yy = 380 + i * 130
        out.append(Text(x=1030, y=yy, w=60, h=36, runs=[Run(f"0{i+1}", color=cols[i % 4])], size=22,
                        bold=True))
        out.append(Text(x=1090, y=yy, w=680, h=90,
                        runs=[Run(c.get("descriptions", [
                            "Fixer les objectifs et les moyens.",
                            "Exécuter à petite échelle, vite.",
                            "Comparer les résultats aux attentes.",
                            "Corriger, standardiser, recommencer."][i]), color=p["muted"])],
                        size=20, line=1.4, fit=True))
    return out


@layout("cycle-rings", "Cycle — anneaux concentriques", "Infographies sur les anneaux")
def cycle_rings(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Anneaux", c.get("title", "Trois cercles d'influence"),
                        c.get("subtitle", "Du cœur de l'offre à l'écosystème élargi."),
                        page=ctx.get("page"), total=ctx.get("total"))
    cx, cy = 640, 620
    layers = c.get("layers") or [("Cœur", 130, p["accent"]), ("Proche", 210, p["accent2"]),
                                 ("Élargi", 290, p["accent3"])]
    for i, (lab, r, col) in enumerate(layers):
        out.append(ellipse(cx, cy, r, fill=Fill(color=col, alpha=0.13 + 0.02 * i),
                           stroke=Stroke(color=col, width=2, alpha=0.55)))
        out.append(Text(x=cx - r + 30, y=cy + r - 56, w=200, h=32, runs=[Run(lab.upper(), color=col)],
                        size=19, bold=True, spacing=2))
    out.append(Text(x=cx - 120, y=cy - 40, w=240, h=50, runs=[Run(c.get("center", "Offre"), color=p["text"])],
                    size=30, bold=True, align="center"))
    out.append(icon_paths(cx - 26, cy + 16, 52, iconlib.icon_paths(c.get("icon", "target")),
                          color=p["accent"], width=2.0))
    items = c.get("items") or [("Clients fidèles", 82), ("Partenaires", 64), ("Communauté", 47),
                               ("Prospects", 35)]
    for i, (lab, v) in enumerate(items):
        yy = 460 + i * 100
        out.append(Text(x=1070, y=yy, w=460, h=36, runs=[Run(lab, color=p["text"])], size=23))
        out += B.progress(p, 1070, yy + 46, 520, v / 100, [p["accent"], p["accent2"],
                                                           p["accent3"], p["accent"]][i], h=10)
    return out


@layout("cycle-ring-progress", "Anneau de progression + liste", "Infographies sur les anneaux")
def cycle_ring_progress(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Objectifs", c.get("title", "Où nous en sommes"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    rings = c.get("rings") or [("Ventes", 0.78, p["accent"]), ("Marketing", 0.62, p["accent2"]),
                               ("Produit", 0.91, p["accent3"])]
    cx, cy = 560, 640
    for i, (lab, v, col) in enumerate(rings):
        r = 260 - i * 62
        out.append(Arc(cx=cx, cy=cy, r=r, a0=-90, a1=270, fill=Fill(color=col, alpha=0.13),
                       inner=0.84))
        out.append(Arc(cx=cx, cy=cy, r=r, a0=-90, a1=-90 + 360 * v, fill=Fill(color=col),
                       inner=0.84, anim="fade", anim_delay=90 * i, key="ring"))
    out.append(Text(x=cx - 200, y=cy - 56, w=400, h=80, runs=[Run(c.get("center", "77 %"),
                                                                  color=p["text"])],
                    size=64, bold=True, align="center"))
    out.append(Text(x=cx - 200, y=cy + 30, w=400, h=30, runs=[Run("moyenne pondérée", color=p["muted"])],
                    size=18, align="center", caps=True, spacing=1.5))
    for i, (lab, v, col) in enumerate(rings):
        yy = 430 + i * 130
        out.append(Text(x=980, y=yy, w=400, h=36, runs=[Run(lab, color=p["text"])], size=25, bold=True))
        out.append(Text(x=1400, y=yy, w=200, h=36, runs=[Run(f"{int(v*100)} %", color=col)], size=25,
                        bold=True, align="right"))
        out += B.progress(p, 980, yy + 50, 620, v, col, h=12, delay=90 * i)
    return out


@layout("cycle-circular-list", "Infographie circulaire — 6 items", "Infographies circulaires")
def cycle_circular_list(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Écosystème", c.get("title", "Six leviers articulés"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Produit", "layers"), ("Prix", "tag"), ("Place", "map-pin"),
                               ("Promotion", "megaphone"), ("Personnes", "users"),
                               ("Process", "cog")]
    cx, cy, r = W / 2, 600, 265
    out.append(ellipse(cx, cy, r, fill=None, stroke=Stroke(color=p["line"], width=1.6, alpha=0.8)))
    out.append(ellipse(cx, cy, 120, fill=Fill(color=p["accent"], alpha=0.16),
                       stroke=Stroke(color=p["accent"], width=1.6, alpha=0.6)))
    out.append(Text(x=cx - 110, y=cy - 26, w=220, h=44, runs=[Run(c.get("center", "Mix"), color=p["text"])],
                    size=30, bold=True, align="center"))
    n = len(items)
    for i, (lab, ic) in enumerate(items):
        a = -math.pi / 2 + 2 * math.pi * i / n
        px, py = cx + r * math.cos(a), cy + r * math.sin(a)
        col = [p["accent"], p["accent2"], p["accent3"]][i % 3]
        out.append(ellipse(px, py, 68, fill=Fill(color=p["card"]), stroke=Stroke(color=col, width=2))
                   )
        out.append(icon_paths(px - 26, py - 26, 52, iconlib.icon_paths(ic), color=col, width=1.9))
        ca, sa = math.cos(a), math.sin(a)
        lx, ly = cx + (r + 104) * ca, cy + (r + 104) * sa
        if ca > 0.35:            # à droite de l'anneau
            tx, al = lx + 6, "left"
        elif ca < -0.35:         # à gauche de l'anneau
            tx, al = lx - 306, "right"
        else:                    # au-dessus / en dessous
            tx, al = lx - 150, "center"
        ty = ly - 34 if sa > 0.7 else (ly - 20 if sa > -0.7 else ly - 44)
        out.append(Text(x=tx, y=ty, w=300, h=44, runs=[Run(lab, color=p["text"])],
                        size=22, bold=True, align=al))
    return out


@layout("rings-four", "Anneaux — 4 segments", "Infographies sur les anneaux")
def rings_four(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Répartition", c.get("title", "Quatre piliers, un seul cap"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Personnes", 0.86), ("Processus", 0.72),
                               ("Technologie", 0.64), ("Culture", 0.55)]
    cx = 620
    for i, (lab, v) in enumerate(items):
        cy = 380 + i * 160
        col = [p["accent"], p["accent2"], p["accent3"], p["accent2"]][i]
        out.append(Arc(cx=cx, cy=cy, r=56, a0=-90, a1=270, fill=Fill(color=col, alpha=0.15),
                       inner=0.80))
        out.append(Arc(cx=cx, cy=cy, r=56, a0=-90, a1=-90 + 360 * v, fill=Fill(color=col),
                       inner=0.80, anim="fade", anim_delay=80 * i))
        out.append(Text(x=cx - 56, y=cy - 24, w=112, h=34, runs=[Run(f"{int(v*100)}", color=p["text"])],
                        size=22, bold=True, align="center"))
        out.append(Text(x=cx + 100, y=cy - 30, w=420, h=36, runs=[Run(lab, color=p["text"])], size=26,
                        bold=True))
        out.append(Text(x=cx + 100, y=cy + 8, w=600, h=32,
                        runs=[Run(c.get("descriptions", ["Engagement et compétences",
                                                         "Fluidité et qualité d'exécution",
                                                         "Outils et données fiables",
                                                         "Valeurs partagées au quotidien"][i]),
                                  color=p["muted"])], size=19))
    return out


# ============================================================ ENTONNOIRS
@layout("funnel-5", "Entonnoir — 5 niveaux", "Infographies en entonnoir")
def funnel_5(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Conversion", c.get("title", "De la visite à la fidélisation"),
                        c.get("subtitle", "Chaque étape a son objectif et son indicateur."),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    steps = c.get("steps") or [("Visiteurs", "48 200", 1.0), ("Prospects", "12 400", 0.78),
                               ("Qualifiés", "4 800", 0.58), ("Clients", "1 640", 0.40),
                               ("Fidèles", "620", 0.24)]
    x, y = 200, 380
    hh = 96
    wmax = 1520
    for i, (lab, val, ratio) in enumerate(steps):
        w = wmax * ratio
        cx = x + wmax / 2
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]][i]
        pts = [(cx - w / 2, y + i * (hh + 8)), (cx + w / 2, y + i * (hh + 8)),
               (cx + w * 0.44, y + i * (hh + 8) + hh), (cx - w * 0.44, y + i * (hh + 8) + hh)]
        out.append(poly(pts, fill=Fill(color=col, alpha=0.85),
                        anim="wipe-down", anim_delay=70 * i))
        out.append(Text(x=cx - w / 2 + 30, y=y + i * (hh + 8) + 26, w=w - 60, h=42,
                        runs=[Run(lab, color="#FFFFFF")], size=26, bold=True))
        out.append(Text(x=cx + w / 2 - 260, y=y + i * (hh + 8) + 28, w=230, h=40,
                        runs=[Run(val, color="#FFFFFF")], size=24, bold=True, align="right"))
    out.append(Text(x=W - MARGIN - 340, y=352, w=340, h=34,
                    runs=[Run("Taux de conversion global", color=p["muted"])], size=19, align="right"))
    out.append(Text(x=W - MARGIN - 340, y=384, w=340, h=80, runs=[Run("1,29 %", color=p["accent2"])],
                    size=56, bold=True, align="right"))
    return out


@layout("funnel-sales", "Entonnoir de vente — pipeline", "Entonnoirs de vente")
def funnel_sales(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Pipeline", c.get("title", "Notre pipeline commercial"),
                        page=ctx.get("page"), total=ctx.get("total"))
    stages = c.get("items") or [("Leads entrants", "842", 0.96), ("Qualification", "486", 0.78),
                                ("Démonstration", "312", 0.60), ("Proposition", "184", 0.44),
                                ("Négociation", "96", 0.30), ("Signé", "58", 0.18)]
    x0, y = 200, 380
    hh = 78
    for i, (lab, val, ratio) in enumerate(stages):
        w = 1200 * ratio
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"], p["accent3"]][i]
        out.append(rect(x0 + (1200 - w) / 2, y + i * (hh + 10), w, hh,
                        fill=Fill(color=col, alpha=0.20), radius=14,
                        stroke=Stroke(color=col, width=1.6, alpha=0.7)))
        out.append(rect(x0 + (1200 - w) / 2, y + i * (hh + 10), max(8, w * 0.18), hh,
                        fill=Fill(color=col), radius=14, anim="wipe-left", anim_delay=70 * i))
        out.append(Text(x=x0 + (1200 - w) / 2 + 26, y=y + i * (hh + 10) + 20, w=w - 120, h=40,
                        runs=[Run(lab, color=p["text"])], size=23, bold=True))
        out.append(Text(x=x0 + 1230, y=y + i * (hh + 10) + 18, w=240, h=40,
                        runs=[Run(val, color=col)], size=25, bold=True))
        if i:
            out.append(Text(x=x0 + 1230, y=y + i * (hh + 10) + 46, w=240, h=26,
                            runs=[Run(f"↓ {int(ratio*100)} %", color=p["muted"])], size=17))
    out += B.stat(p, 1520, 420, 340, "58", "deals signés ce trimestre", color=p["accent2"], size=64)
    out += B.stat(p, 1520, 620, 340, "38 j", "cycle de vente moyen", color=p["accent3"], size=64)
    return out


@layout("funnel-stage-scene", "Infographie de scène — entonnoir", "Infographies de scène")
def funnel_scene(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Acquisition", c.get("title", "Attirer, convertir, fidéliser"),
                        page=ctx.get("page"), total=ctx.get("total"))
    # scène : bloc produit + flux
    out.append(rect(MARGIN, 380, 760, 520, fill=Fill(color=p["card"]), radius=32,
                    stroke=Stroke(color=p["line"], width=1.4)))
    out.append(ellipse(MARGIN + 380, 560, 170,
                       fill=Fill(color=p["accent"], stops=[(0, p["accent"], 0.45), (1, p["accent"], 0)])))
    out.append(icon_paths(MARGIN + 380 - 70, 490, 140, iconlib.icon_paths("magnet"),
                          color=p["text"], width=1.5))
    out.append(Text(x=MARGIN + 40, y=760, w=680, h=60,
                    runs=[Run(c.get("scene_title", "Trafic qualifié"), color=p["text"])],
                    size=30, bold=True, align="center"))
    for i, (lab, val) in enumerate([("Visiteurs", "48,2 k"), ("Leads", "12,4 k"), ("Clients", "1,6 k")]):
        y = 420 + i * 170
        out += B.card(p, 950, y, 420, 140, anim="rise", delay=80 * i)
        out.append(Text(x=980, y=y + 22, w=360, h=32, runs=[Run(lab, color=p["muted"])], size=19))
        out.append(Text(x=980, y=y + 58, w=360, h=60, runs=[Run(val, color=p["text"])], size=40,
                        bold=True))
        out.append(icon_paths(1290, y + 50, 40, iconlib.icon_paths(["mouse-pointer-click",
                                                                    "filter", "heart"][i]),
                              color=p["accent2"], width=1.9))
    out += B.stat(p, 1450, 430, 400, "3,4 %", "conversion moyenne", color=p["accent"], size=64)
    out += B.stat(p, 1450, 620, 400, "−28 %", "coût d'acquisition", color=p["accent2"], size=64)
    return out


# ============================================================ PYRAMIDE / MCDO
@layout("pyramid-4", "Pyramide — 4 niveaux", "Infographie pyramidale")
def pyramid_4(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Hiérarchie", c.get("title", "De la vision à l'exécution"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    levels = c.get("items") or [("Vision", "Où nous allons"), ("Stratégie", "Comment y aller"),
                                ("Tactique", "Quoi faire cette année"), ("Opérations", "Qui fait quoi")]
    cx, y = 620, 340
    for i, (t, d) in enumerate(levels):
        w = 300 + i * 150
        h = 100
        yy = y + i * (h + 8)
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"]][i]
        pts = [(cx - w / 2, yy), (cx + w / 2, yy), (cx + w / 2 + 40, yy + h), (cx - w / 2 - 40, yy + h)]
        out.append(poly(pts, fill=Fill(color=col, alpha=0.85), anim="wipe-up", anim_delay=80 * i))
        out.append(Text(x=cx - w / 2 + 30, y=yy + 22, w=w - 60, h=40, runs=[Run(t, color="#FFFFFF")],
                        size=27, bold=True, align="center"))
        out.append(Text(x=cx + w / 2 + 90, y=yy + 24, w=520, h=56, runs=[Run(d, color=p["muted"])],
                        size=21, line=1.25))
    return out


@layout("pyramid-maslow", "Pyramide — besoins / maturité", "Infographie pyramidale")
def pyramid_maslow(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Maturité", c.get("title", "Les niveaux de maturité data"),
                        page=ctx.get("page"), total=ctx.get("total"))
    levels = c.get("items") or [("Prédictif", "Anticiper les usages futurs", "brain"),
                                ("Prescriptif", "Recommander la bonne action", "sparkles"),
                                ("Diagnostic", "Comprendre le pourquoi", "chart-line"),
                                ("Descriptif", "Mesurer ce qui s'est passé", "chart-column")]
    cx, base_y = 560, 900
    for i, (t, d, ic) in enumerate(levels):
        w = 260 + i * 110
        h = 110
        yy = base_y - (i + 1) * (h + 6)
        col = [p["accent2"], p["accent"], p["accent3"], p["accent2"]][i]
        pts = [(cx - w / 2, yy + h), (cx + w / 2, yy + h), (cx + w / 2 - 34, yy), (cx - w / 2 + 34, yy)]
        out.append(poly(pts, fill=Fill(color=col, alpha=0.18), stroke=Stroke(color=col, width=1.6),
                        anim="rise", anim_delay=80 * i))
        out.append(icon_paths(cx - 22, yy + 28, 44, iconlib.icon_paths(ic), color=col, width=1.9))
        out.append(Text(x=cx - 250, y=yy + 20, w=200, h=34, runs=[Run(t, color=p["text"])], size=22,
                        bold=True, align="right"))
        out.append(Text(x=cx + 250, y=yy + 30, w=560, h=40, runs=[Run(d, color=p["muted"])], size=20))
    return out


# ============================================================ TIMELINE
@layout("timeline-horizontal", "Chronologie — horizontale", "Infographie chronologique")
def timeline_horizontal(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Roadmap", c.get("title", "Les grandes étapes du projet"),
                        page=ctx.get("page"), total=ctx.get("total"))
    milestones = c.get("items") or [("T1 2026", "Cadrage", "Périmètre et budget validés"),
                                    ("T2 2026", "Pilote", "Déploiement sur deux équipes"),
                                    ("T3 2026", "Extension", "Montée en charge nationale"),
                                    ("T4 2026", "Bilan", "Mesure et arbitrages 2027")]
    y = 640
    x0 = MARGIN
    w = (W - 2 * MARGIN) / len(milestones)
    out.append(rect(x0, y - 2, W - 2 * MARGIN, 4, fill=Fill(color=p["line"])))
    for i, (t, lab, d) in enumerate(milestones):
        cx = x0 + w * i + w / 2
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"]][i]
        up = i % 2 == 0
        out.append(rect(cx - 1.5, y - (90 if up else 0), 3, 90, fill=Fill(color=col, alpha=0.6)))
        out.append(ellipse(cx, y, 16, fill=Fill(color=col), stroke=Stroke(color=p["bg"], width=4),
                           anim="zoom", anim_delay=80 * i))
        by = y - 260 if up else y + 110
        out += B.card(p, cx - w / 2 + 30, by, w - 60, 170, anim="rise", delay=80 * i)
        out.append(Text(x=cx - w / 2 + 52, y=by + 18, w=w - 104, h=30, runs=[Run(t, color=col)],
                        size=19, bold=True, spacing=2))
        out.append(Text(x=cx - w / 2 + 52, y=by + 52, w=w - 104, h=36, runs=[Run(lab, color=p["text"])],
                        size=24, bold=True))
        out.append(Text(x=cx - w / 2 + 52, y=by + 94, w=w - 104, h=60, runs=[Run(d, color=p["muted"])],
                        size=18, line=1.35, fit=True))
    return out


@layout("timeline-vertical", "Chronologie — verticale", "Infographie chronologique")
def timeline_vertical(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Historique", c.get("title", "Sept ans de construction"),
                        page=ctx.get("page"), total=ctx.get("total"))
    events = c.get("items") or [("2019", "Création", "Trois fondateurs, un premier client."),
                                ("2020", "Premier million", "Le cap du million d'euros est franchi."),
                                ("2022", "International", "Ouverture de deux bureaux en Afrique."),
                                ("2024", "Levé de fonds", "8 M€ pour accélérer la plateforme."),
                                ("2026", "Leader régional", "Position de référence sur notre marché.")]
    x = 260
    y0 = 340
    out.append(rect(x, y0, 3, 560, fill=Fill(color=p["line"])))
    for i, (yr, t, d) in enumerate(events):
        y = y0 + i * 112
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]][i]
        out.append(Text(x=MARGIN, y=y - 6, w=140, h=40, runs=[Run(yr, color=col)], size=26, bold=True,
                        align="right"))
        out.append(ellipse(x + 1.5, y + 14, 12, fill=Fill(color=col),
                           stroke=Stroke(color=p["bg"], width=4), anim="zoom", anim_delay=70 * i))
        out.append(Text(x=x + 60, y=y - 8, w=520, h=38, runs=[Run(t, color=p["text"])], size=25,
                        bold=True))
        out.append(Text(x=x + 330, y=y - 2, w=1100, h=44, runs=[Run(d, color=p["muted"])], size=20))
    out += B.stat(p, 1080, 380, 340, "12×", "croissance en 5 ans", color=p["accent2"], size=64)
    out += B.stat(p, 1440, 380, 340, "180", "collaborateurs", color=p["accent3"], size=64)
    out += B.stat(p, 1080, 580, 340, "18", "pays", color=p["accent"], size=64)
    out += B.stat(p, 1440, 580, 340, "4,9/5", "note clients", color=p["accent2"], size=64)
    return out


@layout("timeline-curved", "Chronologie — courbe", "Infographie chronologique")
def timeline_curved(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Étapes", c.get("title", "Un parcours en cinq jalons"),
                        page=ctx.get("page"), total=ctx.get("total"))
    pts = []
    for i in range(60):
        t = i / 59
        x = MARGIN + 120 + t * (W - 2 * MARGIN - 240)
        y = 660 + 150 * math.sin(t * math.pi * 1.6 + 0.4)
        pts.append((x, y))
    out.append(poly(pts, fill=None, closed=False, smooth=True,
                    stroke=Stroke(color=p["line"], width=6, cap="round")))
    out.append(poly(pts[:34], fill=None, closed=False, smooth=True,
                    stroke=Stroke(color=p["accent"], width=6, cap="round"),
                    anim="wipe-left", key="curve"))
    milestones = c.get("steps") or ["Idéation", "Prototype", "Test", "Lancement", "Scale"]
    descs = c.get("descriptions") or ["Le cadre et les objectifs", "Les premiers essais terrain",
                                      "Les retours utilisateurs", "La mise sur le marché",
                                      "Le passage à l'échelle"]
    for i, s in enumerate(milestones):
        t = (i + 0.5) / len(milestones)
        x = MARGIN + 120 + t * (W - 2 * MARGIN - 240)
        y = 660 + 150 * math.sin(t * math.pi * 1.6 + 0.4)
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"], p["accent2"]][i]
        up = y < 660
        out.append(ellipse(x, y, 26, fill=Fill(color=p["bg"]), stroke=Stroke(color=col, width=5),
                           anim="zoom", anim_delay=80 * i))
        top = y - 250 if up else min(y + 62, 830)
        out += B.card(p, x - 140, top, 280, 168, anim="rise", delay=80 * i)
        out.append(Text(x=x - 128, y=top + 22, w=256, h=34, runs=[Run(s, color=p["text"])],
                        size=23, bold=True, align="center"))
        out.append(Text(x=x - 128, y=top + 58, w=256, h=40,
                        runs=[Run(f"0{i+1}", color=col)], size=19, bold=True, align="center",
                        spacing=2))
        out.append(Text(x=x - 128, y=top + 98, w=256, h=52,
                        runs=[Run(descs[i % len(descs)], color=p["muted"])], size=18,
                        align="center", line=1.3))
    return out


# ============================================================ ÉQUIPEMENTS / ICONES
@layout("icons-grid-8", "Icônes — grille 8", "Icônes")
def icons_grid_8(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Bibliothèque", c.get("title", "Huit icônes, mille usages"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Stratégie", "target"), ("Finance", "wallet"), ("Équipe", "users"),
                               ("Produit", "layers"), ("Données", "database"), ("Sécurité", "shield-check"),
                               ("Croissance", "trending-up"), ("Support", "headphones")]
    w = 400
    for i, (lab, ic) in enumerate(items):
        col, row = i % 4, i // 4
        x = MARGIN + col * (w + 27)
        y = 380 + row * 300
        out += B.card(p, x, y, w, 260, anim="zoom", delay=50 * i)
        out += B.circle_icon(p, x + w / 2, y + 100, 56, ic,
                             [p["accent"], p["accent2"], p["accent3"]][i % 3], alpha=0.16)
        out.append(Text(x=x + 20, y=y + 180, w=w - 40, h=36, runs=[Run(lab, color=p["text"])],
                        size=24, bold=True, align="center"))
        out.append(Text(x=x + 20, y=y + 218, w=w - 40, h=30, runs=[Run(ic, color=p["muted"])],
                        size=17, align="center"))
    return out


@layout("icons-feature-4", "Icônes — 4 fonctionnalités", "Icônes")
def icons_feature_4(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Fonctionnalités", c.get("title", "Ce qui fait la différence"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Rapide", "Déployé en trois semaines, sans projet informatique lourd.", "zap"),
                               ("Fiable", "Une disponibilité de 99,98 % mesurée chaque mois.", "shield-check"),
                               ("Ouvert", "API documentées et connecteurs standards.", "code"),
                               ("Humain", "Un accompagnement dédié du premier jour.", "heart-handshake")]
    w = 400
    for i, (t, d, ic) in enumerate(items):
        x = MARGIN + i * (w + 27)
        y = 400
        out += B.card(p, x, y, w, 420, anim="rise", delay=80 * i)
        out += B.badge(p, x + 34, y + 34, 84, ic, [p["accent"], p["accent2"], p["accent3"], p["accent"]][i],
                       style="outline")
        out.append(Text(x=x + 34, y=y + 150, w=w - 68, h=40, runs=[Run(t, color=p["text"])], size=27,
                        bold=True))
        out.append(Text(x=x + 34, y=y + 202, w=w - 68, h=180, runs=[Run(d, color=p["muted"])],
                        size=20, line=1.5, fit=True))
    return out


@layout("equipment-scene", "Équipements — scène 3D", "Infographie sur les équipements")
def equipment_scene(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Écosystème", c.get("title", "Des outils connectés entre eux"),
                        page=ctx.get("page"), total=ctx.get("total"))
    cx, cy = W / 2, 640
    # plateforme isométrique
    out.append(poly([(cx, cy - 120), (cx + 460, cy - 30), (cx, cy + 60), (cx - 460, cy - 30)],
                    fill=Fill(color=p["card"])))
    out.append(poly([(cx, cy - 120), (cx + 460, cy - 30), (cx, cy + 60), (cx - 460, cy - 30)],
                    fill=None, stroke=Stroke(color=p["accent"], width=2, alpha=0.7)))
    tools = [("Serveur", "server", -300), ("Cloud", "cloud", -150), ("Mobile", "smartphone", 150),
             ("Poste", "monitor", 300)]
    for i, (lab, ic, dx) in enumerate(tools):
        x = cx + dx
        y = cy - 30 + abs(dx) * 0.13 - 190
        out.append(rect(x - 60, y, 120, 120, fill=Fill(color=p["accent2"], alpha=0.16), radius=20,
                        stroke=Stroke(color=p["accent2"], width=1.6, alpha=0.7),
                        anim="rise", anim_delay=70 * i))
        out.append(icon_paths(x - 30, y + 30, 60, iconlib.icon_paths(ic), color=p["accent2"], width=1.8))
        out.append(Text(x=x - 90, y=y + 132, w=180, h=32, runs=[Run(lab, color=p["text"])], size=20,
                        align="center"))
    out.append(icon_paths(cx - 40, cy - 150, 80, iconlib.icon_paths("cpu"), color=p["accent"], width=1.6))
    return out


# ============================================================ MARKETING / CORPORATE
@layout("marketing-funnel-cards", "Marketing — funnel + KPI", "Infographies marketing")
def marketing_funnel_cards(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Campagne", c.get("title", "Performance de la campagne"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Impressions", "3,2 M", "eye"), ("Clics", "128 k", "mouse-pointer-click"),
                               ("Leads", "12,4 k", "user-plus"), ("Ventes", "1 640", "shopping-cart")]
    w = 400
    for i, (lab, val, ic) in enumerate(items):
        x = MARGIN + i * (w + 27)
        y = 380 + i * 0
        out += B.card(p, x, y, w, 230, anim="rise", delay=70 * i)
        out += B.circle_icon(p, x + 60, y + 60, 34, ic, [p["accent"], p["accent2"], p["accent3"],
                                                          p["accent"]][i], alpha=0.18)
        out.append(Text(x=x + 30, y=y + 108, w=w - 60, h=60, runs=[Run(val, color=p["text"])], size=44,
                        bold=True))
        out.append(Text(x=x + 30, y=y + 172, w=w - 60, h=36, runs=[Run(lab, color=p["muted"])], size=20))
        if i < 3:
            out.append(Text(x=x + w + 2, y=y + 96, w=24, h=40,
                            runs=[Run("›", color=p["accent"])], size=30, bold=True))
    # courbe dépenses / revenus
    out += B.card(p, MARGIN, 660, W - 2 * MARGIN, 280, anim="fade")
    out.append(Text(x=MARGIN + 30, y=684, w=700, h=34, runs=[Run("Retour sur investissement publicitaire",
                                                                 color=p["text"])], size=22, bold=True))
    from layouts.charts import area_chart, axis_y
    out += area_chart(p, MARGIN + 60, 740, W - 2 * MARGIN - 400, 160,
                      [12, 18, 15, 26, 32, 30, 44, 52], p["accent"], 0.3, 3.4, True)
    out += B.stat(p, W - MARGIN - 320, 730, 280, "4,8×", "ROAS", color=p["accent2"], size=58)
    return out


@layout("corporate-pillars", "Entreprise — 4 piliers", "Infographies d'entreprise")
def corporate_pillars(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Modèle", c.get("title", "Quatre piliers de notre modèle"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Produit", "Une plateforme unique et modulaire.", "layers"),
                               ("Go-to-market", "Vente directe et partenaires.", "handshake"),
                               ("Opérations", "Support et delivery industrialisés.", "settings"),
                               ("Finance", "Un modèle récurrent et rentable.", "trending-up")]
    base_y = 780
    for i, (t, d, ic) in enumerate(items):
        x = MARGIN + i * 440
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"]][i]
        out.append(rect(x + 60, base_y - 300, 300, 300, fill=Fill(color=col, alpha=0.12), radius=26,
                        stroke=Stroke(color=col, width=1.4, alpha=0.5), anim="rise", anim_delay=80 * i))
        out.append(icon_paths(x + 190, base_y - 260, 44, iconlib.icon_paths(ic), color=col, width=1.8))
        out.append(Text(x=x + 70, y=base_y - 190, w=280, h=70, runs=[Run(t, color=p["text"])], size=24,
                        bold=True, align="center", line=1.2))
        out.append(Text(x=x + 70, y=base_y - 110, w=280, h=90, runs=[Run(d, color=p["muted"])], size=18,
                        align="center", line=1.35, fit=True))
        out.append(poly([(x + 210, base_y), (x + 250, base_y), (x + 230, base_y + 40)],
                        fill=Fill(color=col, alpha=0.6)))
    out.append(rect(MARGIN, base_y + 40, W - 2 * MARGIN, 60, fill=Fill(color=p["accent"], alpha=0.16),
                    radius=12))
    out.append(Text(x=MARGIN, y=base_y + 54, w=W - 2 * MARGIN, h=34,
                    runs=[Run(c.get("base", "Une exécution alignée sur un seul objectif : la satisfaction client"),
                              color=p["text"])], size=21, align="center", bold=True))
    return out


@layout("business-model-canvas", "Business model canvas", "Schémas")
def business_model_canvas(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Modèle économique", c.get("title", "Business model canvas"),
                        page=ctx.get("page"), total=ctx.get("total"))
    blocks = c.get("blocks") or [
        ("Partenaires clés", "Fournisseurs cloud, intégrateurs, écoles"),
        ("Activités clés", "Produit, support, marketing"),
        ("Proposition de valeur", "Une plateforme simple qui fait gagner du temps"),
        ("Relation client", "Self-service + accompagnement dédié"),
        ("Segments", "PME et ETI en croissance"),
        ("Ressources clés", "Équipe produit, données, marque"),
        ("Canaux", "Vente directe, partenaires, contenu"),
        ("Coûts", "Équipes, infrastructure, acquisition"),
        ("Revenus", "Abonnement mensuel par utilisateur")]
    x0, y0 = MARGIN, 340
    total_w = W - 2 * MARGIN
    top_w = [total_w * v for v in (0.18, 0.17, 0.30, 0.17, 0.18)]
    h1 = 250
    cols = [p["accent"], p["accent2"], p["accent"], p["accent2"], p["accent"]]
    x = x0
    for i, (t, d) in enumerate(blocks[:5]):
        w = top_w[i]
        out.append(rect(x + 4, y0, w - 8, h1, fill=Fill(color=p["card"], alpha=0.9), radius=16,
                        stroke=Stroke(color=cols[i], width=1.4, alpha=0.55), anim="fade",
                        anim_delay=40 * i))
        out.append(Text(x=x + 22, y=y0 + 18, w=w - 44, h=56,
                        runs=[Run(t.upper(), color=cols[i])], size=14, bold=True, spacing=1.4))
        out.append(Text(x=x + 22, y=y0 + 82, w=w - 44, h=h1 - 100,
                        runs=[Run(d, color=p["text"])], size=17, line=1.4, fit=True))
        x += w
    y1 = y0 + h1 + 12
    h2 = 150
    out.append(rect(x0 + 4, y1, top_w[0] + top_w[1] - 8, h2, fill=Fill(color=p["card"], alpha=0.9),
                    radius=16, stroke=Stroke(color=p["accent3"], width=1.4, alpha=0.55)))
    out.append(Text(x=x0 + 22, y=y1 + 16, w=top_w[0] + top_w[1] - 44, h=30,
                    runs=[Run(blocks[5][0].upper(), color=p["accent3"])], size=14, bold=True,
                    spacing=1.4))
    out.append(Text(x=x0 + 22, y=y1 + 52, w=top_w[0] + top_w[1] - 44, h=80,
                    runs=[Run(blocks[5][1], color=p["text"])], size=17, line=1.4, fit=True))
    xc = x0 + top_w[0] + top_w[1]
    out.append(rect(xc + 4, y1, top_w[2] - 8, h2, fill=Fill(color=p["card"], alpha=0.9), radius=16,
                    stroke=Stroke(color=p["accent3"], width=1.4, alpha=0.55)))
    out.append(Text(x=xc + 22, y=y1 + 16, w=top_w[2] - 44, h=30,
                    runs=[Run(blocks[6][0].upper(), color=p["accent3"])], size=14, bold=True,
                    spacing=1.4))
    out.append(Text(x=xc + 22, y=y1 + 52, w=top_w[2] - 44, h=80,
                    runs=[Run(blocks[6][1], color=p["text"])], size=17, line=1.4, fit=True))
    xr = x0 + top_w[0] + top_w[1] + top_w[2]
    wcost = top_w[3] + top_w[4]
    for i, (t, d) in enumerate(blocks[7:9]):
        xx = xr + 4 if i == 0 else x0 + 4
        w = wcost - 8 if i == 0 else total_w - 8
        y = y1 if i == 0 else y1 + h2 + 12
        out.append(rect(xx, y, w, h2 if i == 0 else 130, fill=Fill(color=p["card"], alpha=0.9),
                        radius=16, stroke=Stroke(color=p["accent2"] if i == 0 else p["accent"],
                                                 width=1.4, alpha=0.55), anim="fade",
                        anim_delay=180 + 60 * i))
        out.append(Text(x=xx + 22, y=y + 16, w=w - 44, h=30,
                        runs=[Run(t.upper(), color=p["accent2"] if i == 0 else p["accent"])],
                        size=14, bold=True, spacing=1.4))
        out.append(Text(x=xx + 22, y=y + 52, w=w - 44, h=(h2 if i == 0 else 130) - 70,
                        runs=[Run(d, color=p["text"])], size=17, line=1.4, fit=True))
    return out


# ============================================================ COMPARAISON / SWOT
@layout("comparison-2", "Comparaison — avant / après", "Infographies d'entreprise")
def comparison_2(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Comparaison", c.get("title", "Avant / après"),
                        page=ctx.get("page"), total=ctx.get("total"))
    cols = c.get("cols") or [("Avant", ["Processus manuels", "Données dispersées",
                                        "Reporting mensuel", "Décisions tardives"], p["accent3"], "x"),
                             ("Après", ["Flux automatisés", "Source unique de vérité",
                                        "Tableau de bord temps réel", "Décisions rapides"],
                              p["accent2"], "check")]
    for i, (title_, items, col, ic) in enumerate(cols):
        x = MARGIN + i * 900
        out.append(rect(x, 350, 830, 520, fill=Fill(color=p["card"], alpha=0.85), radius=28,
                        stroke=Stroke(color=col, width=1.6, alpha=0.6)))
        out.append(Text(x=x + 40, y=380, w=600, h=50, runs=[Run(title_.upper(), color=col)], size=24,
                        bold=True, spacing=3))
        for j, it in enumerate(items):
            yy = 460 + j * 96
            out.append(icon_paths(x + 44, yy + 4, 30, iconlib.icon_paths(ic), color=col, width=2.2))
            out.append(Text(x=x + 92, y=yy, w=700, h=40, runs=[Run(it, color=p["text"])], size=22))
            out.append(rect(x + 44, yy + 62, 740, 1, fill=Fill(color=p["line"], alpha=0.5)))
    out.append(ellipse(W / 2, 610, 52, fill=Fill(color=p["bg"]), stroke=Stroke(color=p["line"], width=2)))
    out.append(icon_paths(W / 2 - 24, 586, 48, iconlib.icon_paths("arrow-right"), color=p["accent"],
                          width=2.2))
    return out


@layout("swot", "Analyse SWOT — 4 quadrants", "Analyse SWOT")
def swot_quadrants(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Diagnostic", c.get("title", "Analyse SWOT"),
                        page=ctx.get("page"), total=ctx.get("total"))
    quads = [("Forces", ["Marque reconnue", "Équipe expérimentée", "Trésorerie solide"], p["accent"], "trending-up"),
             ("Faiblesses", ["Notoriété limitée", "Dépendance à 3 clients", "Processus manuels"], p["accent3"], "trending-down"),
             ("Opportunités", ["Nouveaux marchés", "Offre récurrente", "Partenariats"], p["accent2"], "lightbulb"),
             ("Menaces", ["Concurrence accrue", "Coûts logistiques", "Réglementation"], "#C084FC", "triangle-alert")]
    w, h = 830, 300
    for i, (t, items, col, ic) in enumerate(quads):
        x = MARGIN + (i % 2) * (w + 40)
        y = 350 + (i // 2) * (h + 30)
        out.append(rect(x, y, w, h, fill=Fill(color=col, alpha=0.10), radius=24,
                        stroke=Stroke(color=col, width=1.5, alpha=0.6), anim="fade", anim_delay=60 * i))
        out.append(icon_paths(x + 26, y + 24, 32, iconlib.icon_paths(ic), color=col, width=2.0))
        out.append(Text(x=x + 74, y=y + 20, w=500, h=42, runs=[Run(t, color=col)], size=27, bold=True))
        for j, it in enumerate(items):
            out.append(Text(x=x + 30, y=y + 84 + j * 62, w=w - 60, h=44,
                            runs=[Run("•  " + it, color=p["text"])], size=21))
    return out


@layout("swot-matrix", "SWOT — matrice interne/externe", "Analyse SWOT")
def swot_matrix(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "SWOT", c.get("title", "Matrice stratégique"),
                        page=ctx.get("page"), total=ctx.get("total"))
    x0, y0 = 400, 380
    cell = 300
    out.append(Text(x=x0, y=y0 - 46, w=cell * 2 + 20, h=30, runs=[Run("INTERNE", color=p["muted"])],
                    size=17, bold=True, align="center", spacing=4))
    out.append(Text(x=x0 - 290, y=y0 + cell / 2 - 18, w=250, h=40, runs=[Run("POSITIF", color=p["muted"])],
                    size=17, bold=True, align="right", spacing=3))
    out.append(Text(x=x0 - 290, y=y0 + cell * 1.5 - 18, w=250, h=40,
                    runs=[Run("NÉGATIF", color=p["muted"])], size=17, bold=True, align="right",
                    spacing=3))
    out.append(Text(x=x0, y=y0 + cell * 2 + 30, w=cell * 2 + 20, h=30,
                    runs=[Run("EXTERNE", color=p["muted"])], size=17, bold=True, align="center",
                    spacing=4))
    quads = [("Forces", p["accent"], x0, y0), ("Faiblesses", p["accent3"], x0 + cell + 24, y0),
             ("Opportunités", p["accent2"], x0, y0 + cell + 24),
             ("Menaces", "#C084FC", x0 + cell + 24, y0 + cell + 24)]
    data = c.get("data") or [["Marque", "Équipe", "Trésorerie"], ["Notoriété", "Concentration", "Process"],
                             ["Marchés", "Récurrence", "Partenariats"], ["Concurrence", "Coûts", "Réglementation"]]
    for i, (t, col, x, y) in enumerate(quads):
        out.append(rect(x, y, cell, cell, fill=Fill(color=col, alpha=0.12), radius=26,
                        stroke=Stroke(color=col, width=1.5, alpha=0.55)))
        out.append(Text(x=x + 26, y=y + 16, w=cell - 52, h=44, runs=[Run(t.upper(), color=col)], size=21,
                        bold=True, spacing=2))
        for j, v in enumerate(data[i][:3]):
            out.append(Text(x=x + 26, y=y + 72 + j * 58, w=cell - 52, h=52,
                            runs=[Run("•  " + v, color=p["text"])], size=18, line=1.3, fit=True))
    return out


@layout("mckinsey-7s", "Modèle McKinsey 7S", "Modèle McKinsey 7s")
def mckinsey_7s(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Cadre de diagnostic", c.get("title", "Le modèle McKinsey 7S"),
                        c.get("subtitle", "Sept leviers interdépendants : si l'un bouge, tous bougent."),
                        page=ctx.get("page"), total=ctx.get("total"))
    cx, cy = W / 2, 660
    shared = ("Shared values", "Valeurs partagées", p["accent"], "gem")
    hard = [("Strategy", "Stratégie", -90), ("Structure", "Structure", -18),
            ("Systems", "Systèmes", 54)]
    soft = [("Staff", "Personnel", 126), ("Skills", "Compétences", 198), ("Style", "Style de management", 270)]
    nodes = [("Stratégie", "target", -90, p["accent2"]), ("Structure", "network", -18, p["accent2"]),
             ("Systèmes", "settings", 54, p["accent2"]), ("Personnel", "users", 126, p["accent3"]),
             ("Compétences", "award", 198, p["accent3"]), ("Style", "compass", 270, p["accent3"])]
    R = 235
    for i, (lab, ic, ang, col) in enumerate(nodes):
        a = math.radians(ang)
        x, y = cx + R * 1.55 * math.cos(a), cy + R * 0.92 * math.sin(a)
        out.append(line(cx, cy, x, y, Stroke(color=p["line"], width=2, alpha=0.8)))
        out.append(ellipse(x, y, 74, fill=Fill(color=col, alpha=0.16),
                           stroke=Stroke(color=col, width=2, alpha=0.7), anim="zoom", anim_delay=70 * i))
        out.append(icon_paths(x - 26, y - 26, 52, iconlib.icon_paths(ic), color=col, width=1.9))
        out.append(Text(x=x - 120, y=y + 84, w=240, h=34, runs=[Run(lab, color=p["text"])], size=19,
                        bold=True, align="center"))
    out.append(ellipse(cx, cy, 108, fill=Fill(color=p["accent"], color2=p["accent3"], angle=120),
                       anim="circle"))
    out.append(Text(x=cx - 96, y=cy - 40, w=192, h=80, runs=[Run("Valeurs\npartagées", color="#FFFFFF")],
                    size=20, bold=True, align="center", line=1.2))
    # légende bas de page
    out += B.chip(p, 1250, 1000, "Éléments structurels", p["accent2"], size=17, h=38)
    out += B.chip(p, 1560, 1000, "Éléments humains", p["accent3"], size=17, h=38)
    return out


@layout("seven-s-cards", "7S — cartes détaillées", "Modèle McKinsey 7s")
def seven_s_cards(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Diagnostic 7S", c.get("title", "Où agir en priorité"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Stratégie", "Positionnement clair sur trois segments.", 0.82),
                               ("Structure", "Organisation matricielle à simplifier.", 0.54),
                               ("Systèmes", "Outils encore fragmentés.", 0.61),
                               ("Personnel", "Équipe solide et engagée.", 0.88),
                               ("Compétences", "Montée en compétence data à prévoir.", 0.58),
                               ("Style", "Management direct et transparent.", 0.76),
                               ("Valeurs", "Culture forte, partagée par tous.", 0.91)]
    w = 400
    for i, (t, d, v) in enumerate(items[:6]):
        col_i, row = i % 3, i // 3
        x = MARGIN + col_i * (w + 27)
        y = 330 + row * 232
        out += B.card(p, x, y, w, 208, anim="rise", delay=60 * i)
        out.append(Text(x=x + 26, y=y + 18, w=w - 52, h=38, runs=[Run(t, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=x + 26, y=y + 58, w=w - 52, h=64, runs=[Run(d, color=p["muted"])], size=18,
                        line=1.35, fit=True))
        out += B.progress(p, x + 26, y + 150, w - 52, v, p["accent"], h=8, delay=60 * i)
    x = MARGIN + (3 * (w + 27) - w - 480) / 2
    y = 806
    out += B.card(p, x, y, w + 480, 150, anim="rise", delay=420)
    out.append(Text(x=x + 26, y=y + 20, w=w + 428, h=38,
                    runs=[Run(items[6][0], color=p["text"])], size=24, bold=True))
    out.append(Text(x=x + 26, y=y + 60, w=w + 428, h=34, runs=[Run(items[6][1], color=p["muted"])],
                    size=18, fit=True))
    out += B.progress(p, x + 26, y + 110, w - 60, items[6][2], p["accent"], h=8, delay=440)
    out += B.chip(p, x + w + 80, y + 96, "Priorité : aligner structure et systèmes", p["accent2"],
                  size=17, h=38)
    return out
