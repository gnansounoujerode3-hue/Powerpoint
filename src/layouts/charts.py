"""Chapitre : graphiques (courbes, barres, donuts, jauges, tableaux, KPI)."""
from __future__ import annotations

import math

import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_KICKER, T_SUB,
                           T_TITLE, W, bg, cnt, layout)
from content_data import MONTHS, QUARTERS
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths,
                line, poly, rgrad, rect, rich, text, vgrad)


# ------------------------------------------------------------------ helpers
def axis_y(p, x, y, w, h, ticks=4, labels=None, fmt="{:.0f}"):
    out = []
    for i in range(ticks + 1):
        yy = y + h - h * i / ticks
        out.append(rect(x, yy, w, 1, fill=Fill(color=p["line"], alpha=0.45 if i < ticks else 0.9)))
        if labels:
            out.append(Text(x=x - 74, y=yy - 14, w=64, h=28,
                            runs=[Run(labels[i], color=p["muted"])], size=19, align="right"))
    return out


def axis_x(p, x, y, w, cats, size=19):
    out = []
    n = len(cats)
    for i, c in enumerate(cats):
        cx = x + w * (i + 0.5) / n if n > 1 else x + w / 2
        out.append(Text(x=cx - 60, y=y + 12, w=120, h=30, runs=[Run(str(c), color=p["muted"])],
                        size=size, align="center"))
    return out


def legend(p, x, y, items):
    """items = [(label, color)]"""
    out = []
    cx = x
    for label, col in items:
        from textfit import text_width
        out.append(rect(cx, y + 6, 14, 14, fill=Fill(color=col), radius=4))
        out.append(Text(x=cx + 24, y=y, w=text_width(label, 19) + 30, h=28,
                        runs=[Run(label, color=p["muted"])], size=19))
        cx += 24 + text_width(label, 19) + 46
    return out


def smooth_line(pts):
    return poly(pts, fill=None, closed=False, smooth=True,
                stroke=Stroke(color="#FFFFFF", width=0) if False else None)


def area_chart(p, x, y, w, h, values, color, fill_alpha=0.32, width=4, points=False,
               labels=None, anim="wipe-left", delay=0, key="area"):
    """Courbe lissée + aire sous la courbe."""
    n = len(values)
    vmax = max(values) * 1.18 or 1
    pts = [(x + w * i / (n - 1), y + h - h * v / vmax) for i, v in enumerate(values)]
    area = pts + [(x + w, y + h), (x, y + h)]
    out = [poly(area, fill=Fill(color=color, stops=[(0, color, fill_alpha), (1, color, 0.02)],
                                radial=False, angle=90), closed=True)]
    out.append(poly(pts, fill=None, closed=False, smooth=True,
                    stroke=Stroke(color=color, width=width, cap="round", join="round"),
                    anim=anim, anim_delay=delay, key=key))
    if points:
        for i, pt in enumerate(pts):
            out.append(ellipse(pt[0], pt[1], 9, fill=Fill(color=p["bg"]),
                               stroke=Stroke(color=color, width=3.4)))
    if labels:
        for i, (pt, lab) in enumerate(zip(pts, labels)):
            out.append(Text(x=pt[0] - 50, y=pt[1] - 46, w=100, h=32,
                            runs=[Run(lab, color=p["text"], bold=True)], size=20, align="center"))
    return out


def bar_set(p, x, y, w, h, values, maxv, color, gap=0.34, round_=True, labels=None,
            anim="wipe-up", delay=0, horizontal=False, value_size=19):
    out = []
    n = len(values)
    step = w / n
    bw = step * (1 - gap)
    for i, v in enumerate(values):
        bh = h * v / maxv
        bx = x + step * i + (step - bw) / 2
        if horizontal:
            continue
        out.append(rect(bx, y + h - bh, bw, max(bh, 2),
                        fill=Fill(color=color, color2=p["accent2"], angle=30, alpha=0.95),
                        radius=min(10, bw / 2) if round_ else 0,
                        anim=anim, anim_delay=delay + i * 60, key="bar"))
        if labels:
            out.append(Text(x=bx - 20, y=y + h - bh - 36, w=bw + 40, h=30,
                            runs=[Run(labels[i], color=p["text"], bold=True)], size=value_size,
                            align="center"))
    return out


# ------------------------------------------------------------------ slides
@layout("chart-line", "Graphique — courbe", "Graphiques")
def chart_line(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Évolution", c.get("title", "Progression sur douze mois"),
                        c.get("subtitle", "Une dynamique régulière, portée par la demande."),
                        page=ctx.get("page"), total=ctx.get("total"))
    x, y, w, h = 250, 430, 1340, 470
    labels = c.get("ylabels") or ["0", "25", "50", "75", "100"]
    out += axis_y(p, x, y, w, h, 4, labels)
    cats = c.get("categories") or MONTHS
    out += axis_x(p, x, y, w, cats)
    v1 = c.get("series1") or [22, 30, 27, 42, 48, 44, 56, 62, 58, 71, 78, 86]
    v2 = c.get("series2") or [12, 16, 18, 22, 26, 30, 33, 36, 40, 44, 49, 54]
    out += area_chart(p, x, y, w, h, v1, p["accent"], 0.34, 4.4, True, delay=0)
    out += area_chart(p, x, y, w, h, v2, p["accent2"], 0.20, 3.2, True, delay=120)
    out += legend(p, x, y - 60, [(c.get("l1", "Revenus"), p["accent"]),
                                 (c.get("l2", "Marge"), p["accent2"])])
    out.append(Text(x=W - MARGIN - 420, y=196, w=420, h=60,
                    runs=[Run(c.get("delta", "+38,4 %"), color=p["accent2"])], size=48, bold=True,
                    align="right"))
    out.append(Text(x=W - MARGIN - 420, y=256, w=420, h=30,
                    runs=[Run("vs. année précédente", color=p["muted"])], size=19, align="right"))
    return out


@layout("chart-line-multi", "Graphique — 3 courbes", "Graphiques")
def chart_line_multi(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Comparatif", c.get("title", "Trois scénarios de croissance"),
                        page=ctx.get("page"), total=ctx.get("total"))
    x, y, w, h = 250, 400, 1340, 480
    out += axis_y(p, x, y, w, h, 4, ["0", "30", "60", "90", "120"])
    out += axis_x(p, x, y, w, QUARTERS * 2 if len(QUARTERS) else [])
    sets = [(p["accent"], [18, 34, 52, 70, 84, 96, 108, 118], 0.30),
            (p["accent2"], [14, 26, 38, 48, 58, 66, 74, 84], 0.20),
            (p["accent3"], [10, 16, 24, 30, 38, 46, 52, 60], 0.14)]
    for i, (col, vals, a) in enumerate(sets):
        out += area_chart(p, x, y, w, h, vals, col, a, 3.6, True, delay=80 * i)
    out += legend(p, x, y - 56, [("Optimiste", p["accent"]), ("Central", p["accent2"]),
                                 ("Prudent", p["accent3"])])
    for i, (lab, val) in enumerate([("Optimiste", "118"), ("Central", "84"), ("Prudent", "60")]):
        out.append(Text(x=x + i * 430, y=y + h + 60, w=400, h=40,
                        runs=[Run(val + " ", color=p["text"], bold=True),
                              Run("pts", color=p["muted"])], size=22))
    return out


@layout("chart-bar", "Graphique — barres verticales", "Graphiques")
def chart_bar(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Volumes", c.get("title", "Ventes par trimestre"),
                        page=ctx.get("page"), total=ctx.get("total"))
    x, y, w, h = 250, 420, 1340, 470
    vals = c.get("values") or [62, 78, 54, 96, 71, 88]
    labels = c.get("labels") or ["T1", "T2", "T3", "T4", "T5", "T6"]
    vmax = max(vals) * 1.22
    out += axis_y(p, x, y, w, h, 4, [f"{int(vmax*i/4)}k" for i in range(5)])
    out += bar_set(p, x, y, w, h, vals, vmax, p["accent"], labels=[str(v) + "k" for v in vals])
    out += axis_x(p, x, y, w, labels)
    out += B.chip(p, x + w - 300, y - 96, c.get("tag", "+24 % vs N-1"), p["accent2"], size=21,
                  icon_name="trending-up")
    return out


@layout("chart-bar-h", "Graphique — barres horizontales", "Graphiques")
def chart_bar_h(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Classement", c.get("title", "Parts de marché par région"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Europe", 82), ("Amérique du Nord", 68), ("Asie-Pacifique", 54),
                               ("Afrique", 39), ("Amérique latine", 27)]
    x, y, w = 480, 400, 1120
    for i, (lab, v) in enumerate(items):
        yy = y + i * 96
        out.append(Text(x=MARGIN, y=yy + 8, w=380, h=36, runs=[Run(lab, color=p["text"])],
                        size=24, bold=True, align="left"))
        out.append(rect(x, yy, w, 34, fill=Fill(color=p["line"], alpha=0.45), radius=17))
        out.append(rect(x, yy, w * v / 100, 34,
                        fill=Fill(color=p["accent"] if i == 0 else p["accent2"],
                                  color2=p["accent3"] if i == 0 else p["accent"],
                                  angle=0, alpha=0.95), radius=17,
                        anim="wipe-left", anim_delay=70 * i, key="bar"))
        out.append(Text(x=x + w + 24, y=yy + 2, w=100, h=34, runs=[Run(f"{v} %", color=p["text"])],
                        size=23, bold=True))
    return out


@layout("chart-stacked", "Graphique — barres empilées", "Graphiques")
def chart_stacked(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Structure", c.get("title", "Répartition du chiffre d'affaires"),
                        c.get("subtitle", "Une base récurrente qui sécurise la croissance."),
                        page=ctx.get("page"), total=ctx.get("total"))
    x, y, w, h = 250, 430, 1340, 440
    series = c.get("series") or [
        ("Abonnements", [34, 38, 41, 46, 49, 54], p["accent"]),
        ("Services", [22, 24, 26, 27, 30, 31], p["accent2"]),
        ("Licences", [12, 11, 13, 12, 14, 13], p["accent3"]),
    ]
    labels = c.get("labels") or ["2021", "2022", "2023", "2024", "2025", "2026"]
    vmax = max(sum(s[1][i] for s in series) for i in range(len(labels))) * 1.2
    out += axis_y(p, x, y, w, h, 4, [str(int(vmax * i / 4)) for i in range(5)])
    n = len(labels)
    step = w / n
    bw = step * 0.52
    for i in range(n):
        base = 0
        for si, (nm, vals, col) in enumerate(series):
            bh = h * vals[i] / vmax
            out.append(rect(x + step * i + (step - bw) / 2, y + h - base - bh, bw, bh,
                            fill=Fill(color=col, alpha=0.95),
                            radius=0 if si < len(series) - 1 else 8,
                            anim="wipe-up", anim_delay=40 * i + si * 20, key="bar"))
            base += bh
        out.append(Text(x=x + step * i - 20, y=y + h - base - 44, w=bw + 40, h=32,
                        runs=[Run(str(int(sum(s[1][i] for s in series))) + "M", color=p["text"],
                                  bold=True)], size=20, align="center"))
    out += axis_x(p, x, y, w, labels)
    out += legend(p, x, y - 60, [(s[0], s[2]) for s in series])
    return out


@layout("chart-donut", "Graphique — donut", "Graphiques")
def chart_donut(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Répartition", c.get("title", "Portefeuille d'activités"),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    cmap = {"A": p["accent"], "B": p["accent2"], "C": p["accent3"], "D": p["muted"]}
    items = [(a, b, cmap.get(cc, cc)) for a, b, cc in (c.get("items") or [
        ("Logiciel", 46, "A"), ("Services", 28, "B"), ("Maintenance", 16, "C"), ("Autres", 10, "D")])]
    cx, cy, r = 640, 620, 250
    a = -90
    for i, (lab, v, col) in enumerate(items):
        sweep = v / 100 * 360
        out.append(Arc(cx=cx, cy=cy, r=r, a0=a + 2, a1=a + sweep - 2, fill=Fill(color=col),
                       inner=0.62, anim="fade", anim_delay=60 * i, key="arc"))
        a += sweep
    out.append(Text(x=cx - 200, y=cy - 78, w=400, h=90, runs=[Run(c.get("center", "48,2 M€"),
                                                                  color=p["text"])],
                    size=62, bold=True, align="center"))
    out.append(Text(x=cx - 200, y=cy + 16, w=400, h=34, runs=[Run(c.get("center_sub", "total 2026"),
                                                                  color=p["muted"])],
                    size=20, align="center", caps=True, spacing=2))
    xl = 1080
    for i, (lab, v, col) in enumerate(items):
        yy = 480 + i * 96
        out.append(rect(xl, yy + 10, 16, 16, fill=Fill(color=col), radius=5))
        out.append(Text(x=xl + 30, y=yy, w=320, h=36, runs=[Run(lab, color=p["text"])], size=24))
        out.append(Text(x=xl + 330, y=yy, w=120, h=36, runs=[Run(f"{v} %", color=col)], size=24,
                        bold=True, align="right"))
        out.append(rect(xl, yy + 52, 450, 1, fill=Fill(color=p["line"], alpha=0.5)))
    return out


@layout("chart-pie", "Graphique — camembert", "Graphiques")
def chart_pie(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Mix", c.get("title", "Répartition des investissements"),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    cmap = {"A": p["accent"], "B": p["accent2"], "C": p["accent3"], "D": p["muted"]}
    items = [(a, b, cmap.get(cc, cc)) for a, b, cc in (c.get("items") or [
        ("R&D", 38, "A"), ("Marketing", 26, "B"), ("Opérations", 22, "C"), ("Support", 14, "D")])]
    cx, cy, r = 620, 620, 270
    a = -90
    for i, (lab, v, col) in enumerate(items):
        sweep = v / 100 * 360
        out.append(Arc(cx=cx, cy=cy, r=r, a0=a, a1=a + sweep - 1.2,
                       fill=Fill(color=col), pie=True, anim="fade", anim_delay=60 * i))
        a += sweep
    out.append(ellipse(cx, cy, 130, fill=Fill(color=p["bg2"], alpha=0.92)))
    out.append(Text(x=cx - 120, y=cy - 44, w=240, h=60, runs=[Run(c.get("center", "12,4 M€"),
                                                                 color=p["text"])],
                    size=38, bold=True, align="center"))
    out.append(Text(x=cx - 120, y=cy + 14, w=240, h=30, runs=[Run("budget total", color=p["muted"])],
                    size=18, align="center", caps=True, spacing=2))
    for i, (lab, v, col) in enumerate(items):
        yy = 480 + i * 96
        out.append(rect(1080, yy + 10, 16, 16, fill=Fill(color=col), radius=5))
        out.append(Text(x=1110, y=yy, w=320, h=36, runs=[Run(lab, color=p["text"])], size=24))
        out.append(Text(x=1410, y=yy, w=120, h=36, runs=[Run(f"{v} %", color=col)], size=24,
                        bold=True, align="right"))
        out.append(rect(1080, yy + 52, 450, 1, fill=Fill(color=p["line"], alpha=0.5)))
    return out


@layout("chart-gauge", "Graphique — jauge", "Graphiques")
def chart_gauge(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Indicateur", c.get("title", "Atteinte de l'objectif annuel"),
                        page=ctx.get("page"), total=ctx.get("total"), w=900)
    cx, cy, r = W / 2, 720, 330
    out.append(Arc(cx=cx, cy=cy, r=r, a0=180, a1=360, fill=Fill(color=p["line"], alpha=0.6),
                   inner=0.70))
    ratio = c.get("ratio", 0.74)
    out.append(Arc(cx=cx, cy=cy, r=r, a0=180, a1=180 + 180 * ratio,
                   fill=Fill(color=p["accent"], color2=p["accent2"], angle=0), inner=0.70,
                   anim="wipe-left", key="gauge"))
    out.append(Text(x=cx - 300, y=cy - 190, w=600, h=150, runs=[Run(c.get("value", "74 %"),
                                                                   color=p["text"])],
                    size=110, bold=True, align="center"))
    out.append(Text(x=cx - 300, y=cy - 30, w=600, h=40, runs=[Run(c.get("label", "de l'objectif atteint"),
                                                                 color=p["muted"])],
                    size=22, align="center"))
    out.append(Text(x=cx - r - 40, y=cy + 20, w=120, h=30, runs=[Run("0", color=p["muted"])],
                    size=19, align="center"))
    out.append(Text(x=cx + r - 60, y=cy + 20, w=120, h=30, runs=[Run("100", color=p["muted"])],
                    size=19, align="center"))
    for i, (v, lab) in enumerate([("3,4 M€", "réalisé"), ("4,6 M€", "objectif"), ("+12 j", "d'avance")]):
        out += B.stat(p, 210 + i * 520, 860, 400, v, lab, color=p["accent2"], size=54, align="center")
    return out


@layout("kpi-grid", "KPI — 4 indicateurs", "Graphiques")
def kpi_grid(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Tableau de bord", c.get("title", "Les chiffres clés du trimestre"),
                        page=ctx.get("page"), total=ctx.get("total"))
    kpis = c.get("kpis") or [("48,2 M€", "Chiffre d'affaires", "+18 %", "wallet"),
                             ("12,4 %", "Marge EBITDA", "+2,3 pts", "chart-line"),
                             ("1 240", "Clients actifs", "+9 %", "users"),
                             ("4,8/5", "Satisfaction", "+0,3", "star")]
    w = 400
    for i, (v, lab, d, ic) in enumerate(kpis):
        x = MARGIN + i * (w + 27)
        y = 380
        out += B.card(p, x, y, w, 330, anim="rise", delay=70 * i)
        out += B.circle_icon(p, x + 62, y + 62, 34, ic, p["accent"] if i % 2 == 0 else p["accent2"],
                             alpha=0.18)
        out.append(Text(x=x + 34, y=y + 116, w=w - 60, h=90, runs=[Run(v, color=p["text"])],
                        size=56, bold=True))
        out.append(Text(x=x + 34, y=y + 208, w=w - 60, h=70, runs=[Run(lab, color=p["muted"])],
                        size=21, line=1.3))
        out += B.chip(p, x + 34, y + 268, d, p["accent2"], size=19, h=38)
    out.append(Text(x=MARGIN, y=780, w=1000, h=30,
                    runs=[Run(c.get("note", "Source : reporting interne, clôture du 30/09."),
                              color=p["muted"])], size=18))
    return out


@layout("chart-table", "Tableau de données", "Graphiques")
def chart_table(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Détail", c.get("title", "Performance par marché"),
                        page=ctx.get("page"), total=ctx.get("total"))
    cols = ["Marché", "CA 2025", "CA 2026", "Évolution", "Statut"]
    rows = c.get("rows") or [
        ("France", "18,2 M€", "21,4 M€", "+17,6 %", "En avance"),
        ("Sénégal", "4,1 M€", "5,8 M€", "+41,5 %", "En avance"),
        ("Maroc", "6,4 M€", "7,1 M€", "+10,9 %", "Conforme"),
        ("Canada", "9,8 M€", "10,2 M€", "+4,1 %", "À surveiller"),
        ("Brésil", "3,2 M€", "3,9 M€", "+21,9 %", "En avance"),
    ]
    x, y, w = MARGIN, 380, W - 2 * MARGIN
    widths = [0.26, 0.18, 0.18, 0.18, 0.20]
    # entête
    out.append(rect(x, y, w, 64, fill=Fill(color=p["accent"], alpha=0.16), radius=14))
    cx = x
    for i, col in enumerate(cols):
        cw = w * widths[i]
        out.append(Text(x=cx + 26, y=y + 16, w=cw - 40, h=34,
                        runs=[Run(col.upper(), color=p["accent"])], size=18, bold=True, spacing=1.6))
        cx += cw
    for r, row in enumerate(rows):
        yy = y + 64 + r * 84
        if r % 2 == 0:
            out.append(rect(x, yy, w, 84, fill=Fill(color="#FFFFFF", alpha=0.03), radius=10))
        cx = x
        for i, val in enumerate(row):
            cw = w * widths[i]
            colr = p["text"] if i == 0 else p["muted"]
            if i == 3:
                colr = p["accent2"] if val.startswith("+") else p["accent3"]
            if i == 4:
                ok = val in ("En avance", "Conforme")
                out += B.chip(p, cx + 20, yy + 22, val, p["accent2"] if ok else p["accent3"],
                              size=18, h=38)
            else:
                out.append(Text(x=cx + 26, y=yy + 24, w=cw - 40, h=40,
                                runs=[Run(val, color=colr, bold=(i == 0 or i == 3))], size=22))
            cx += cw
        out.append(rect(x, yy + 82, w, 1, fill=Fill(color=p["line"], alpha=0.55)))
    out += B.footer(p, ctx.get("page", 1), ctx.get("total"))
    return out


@layout("chart-waterfall", "Graphique — cascade", "Graphiques")
def chart_waterfall(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Analyse", c.get("title", "Décomposition de la marge"),
                        c.get("subtitle", "D'où viennent les gains — et où partent les points."),
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = c.get("steps") or [("2025", 42, "total"), ("Prix", 6, "up"), ("Volume", 5, "up"),
                               ("Coûts", -7, "down"), ("Mix", 3, "up"), ("2026", 49, "total")]
    x, y, w, h = 220, 480, 1480, 380
    vmax = 60
    step = w / len(steps)
    bw = step * 0.5
    base = 0
    for i, (lab, v, kind) in enumerate(steps):
        bx = x + step * i + (step - bw) / 2
        if kind == "total":
            bh = h * v / vmax
            out.append(rect(bx, y + h - bh, bw, bh, fill=Fill(color=p["accent"], alpha=0.95),
                            radius=10, anim="wipe-up", anim_delay=60 * i))
            out.append(Text(x=bx - 40, y=y + h - bh - 44, w=bw + 80, h=34,
                            runs=[Run(f"{v} M€", color=p["text"], bold=True)], size=21,
                            align="center"))
            base = bh
        else:
            bh = abs(h * v / vmax)
            top = y + h - base - bh if v > 0 else y + h - base
            col = p["accent2"] if v > 0 else p["accent3"]
            out.append(rect(bx, top, bw, max(bh, 3), fill=Fill(color=col, alpha=0.92), radius=6,
                            anim="wipe-up", anim_delay=60 * i))
            sign = "+" if v > 0 else "−"
            out.append(Text(x=bx - 40, y=top - 40, w=bw + 80, h=32,
                            runs=[Run(f"{sign}{abs(v)}", color=p["text"], bold=True)], size=20,
                            align="center"))
            base = base + bh if v > 0 else base - bh
        out.append(Text(x=bx - 40, y=y + h + 18, w=bw + 80, h=32, runs=[Run(lab, color=p["muted"])],
                        size=20, align="center"))
    out += legend(p, MARGIN, 396, [("Gain", p["accent2"]), ("Perte", p["accent3"]),
                                   ("Total", p["accent"])])
    out += B.chip(p, W - MARGIN - 300, 386, c.get("tag", "+4,0 pts de marge"), p["accent2"],
                  size=20, icon_name="trending-up")
    return out


@layout("chart-radar", "Graphique — radar", "Graphiques")
def chart_radar(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Diagnostic", c.get("title", "Maturité par dimension"),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    cx, cy, r = 640, 610, 300
    cats = c.get("categories") or ["Stratégie", "Produit", "Marché", "Équipe",
                                   "Finance", "Systèmes"]
    n = len(cats)
    for ring in (0.33, 0.66, 1.0):
        pts = []
        for i in range(n):
            a = -math.pi / 2 + 2 * math.pi * i / n
            pts.append((cx + r * ring * math.cos(a), cy + r * ring * math.sin(a)))
        out.append(poly(pts, fill=None, closed=True, stroke=Stroke(color=p["line"], width=1.4)))
    for i, cat in enumerate(cats):
        a = -math.pi / 2 + 2 * math.pi * i / n
        out.append(line(cx, cy, cx + r * math.cos(a), cy + r * math.sin(a),
                        Stroke(color=p["line"], width=1, alpha=0.8)))
        lx, ly = cx + (r + 46) * math.cos(a), cy + (r + 46) * math.sin(a)
        out.append(Text(x=lx - 110, y=ly - 16, w=220, h=32, runs=[Run(cat, color=p["muted"])],
                        size=20, align="center"))
    v1 = c.get("values1") or [0.86, 0.72, 0.64, 0.78, 0.58, 0.70]
    v2 = c.get("values2") or [0.62, 0.80, 0.78, 0.54, 0.72, 0.48]
    for vals, col, al in ((v1, p["accent"], 0.28), (v2, p["accent2"], 0.20)):
        pts = []
        for i, v in enumerate(vals):
            a = -math.pi / 2 + 2 * math.pi * i / n
            pts.append((cx + r * v * math.cos(a), cy + r * v * math.sin(a)))
        out.append(poly(pts, fill=Fill(color=col, alpha=al), closed=True,
                        stroke=Stroke(color=col, width=3.4)))
        for pt in pts:
            out.append(ellipse(pt[0], pt[1], 7, fill=Fill(color=col)))
    out += legend(p, 250, 860, [("2026", p["accent"]), ("2025", p["accent2"])])
    for i, (v, lab) in enumerate([("78 %", "score global"), ("+9", "points vs 2025")]):
        out += B.stat(p, 1060, 480 + i * 190, 500, v, lab, color=p["accent2"], size=64)
    return out


@layout("progress-list", "Barres de progression", "Graphiques")
def progress_list(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Avancement", c.get("title", "État des chantiers prioritaires"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Refonte du site", 0.92), ("CRM unifié", 0.74),
                               ("Automatisation facturation", 0.61),
                               ("Recrutement équipe data", 0.45), ("Certification ISO", 0.28)]
    for i, (lab, v) in enumerate(items):
        yy = 380 + i * 108
        out.append(Text(x=MARGIN, y=yy, w=620, h=36, runs=[Run(lab, color=p["text"])], size=25,
                        bold=True))
        out.append(Text(x=W - MARGIN - 120, y=yy, w=120, h=36,
                        runs=[Run(f"{int(v*100)} %", color=p["accent2"])], size=24, bold=True,
                        align="right"))
        out += B.progress(p, MARGIN, yy + 48, W - 2 * MARGIN, v, p["accent"], h=14,
                          anim="wipe-left", delay=80 * i)
    return out


@layout("chart-big-number", "Chiffre XXL + contexte", "Graphiques")
def chart_big_number(p, c, ctx):
    out = bg(p, 1)
    out.append(Text(x=MARGIN, y=150, w=1150, h=330, runs=[Run(c.get("value", "2,4×"), color=p["accent"])],
                    size=250, bold=True, line=0.95, fit=True))
    out += B.kicker(p, MARGIN + 10, 540, c.get("kicker", "Impact mesuré"), p["accent2"])
    out.append(Text(x=MARGIN, y=584, w=1000, h=260, runs=[Run(c.get("text",
                 "C'est le gain de productivité observé chez nos clients après douze mois d'utilisation."),
                 color=p["text"])], size=31, line=1.42, fit=True))
    for i, (v, lab) in enumerate([("−38 %", "coûts opérationnels"), ("+21 %", "satisfaction"),
                                  ("4,2 M€", "valeur créée")]):
        out += B.stat(p, 1180, 620 + i * 130, 640, v, lab, color=p["accent2"], size=48, label_size=20)
    return out


@layout("chart-heatmap", "Graphique — matrice de chaleur", "Graphiques")
def chart_heatmap(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Intensité", c.get("title", "Activité par mois et par canal"),
                        page=ctx.get("page"), total=ctx.get("total"))
    rows = c.get("rows") or ["Web", "App", "Email", "Social", "Terrain"]
    cols = MONTHS[:10]
    import random
    random.seed(7)
    x, y = 300, 420
    cw, ch = 128, 74
    for j, mo in enumerate(cols):
        out.append(Text(x=x + j * cw, y=y - 44, w=cw, h=30, runs=[Run(mo, color=p["muted"])],
                        size=18, align="center"))
    for i, r in enumerate(rows):
        out.append(Text(x=MARGIN, y=y + i * ch + 20, w=200, h=34, runs=[Run(r, color=p["text"])],
                        size=21, bold=True))
        for j in range(len(cols)):
            v = random.random()
            out.append(rect(x + j * cw + 4, y + i * ch + 4, cw - 8, ch - 8,
                            fill=Fill(color=p["accent"], alpha=0.10 + v * 0.82), radius=10,
                            anim="fade", anim_delay=(i * len(cols) + j) * 8))
    out.append(Text(x=x, y=y + len(rows) * ch + 30, w=600, h=30,
                    runs=[Run("Faible", color=p["muted"])], size=18))
    for k in range(6):
        out.append(rect(x + 120 + k * 34, y + len(rows) * ch + 34, 30, 16,
                        fill=Fill(color=p["accent"], alpha=0.1 + k * 0.15), radius=4))
    out.append(Text(x=x + 340, y=y + len(rows) * ch + 30, w=300, h=30,
                    runs=[Run("Élevée", color=p["muted"])], size=18))
    return out
