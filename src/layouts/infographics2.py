"""Chapitre : scènes isométriques, néomorphisme, fait main, anneaux,
marketing, entreprise, schémas, flèches, infographies sombres, pauses."""
from __future__ import annotations

import math
import random

import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_KICKER, T_SUB,
                           T_TITLE, W, bg, cnt, layout)
from content_data import ICON_SETS, MONTHS, SECTORS
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths,
                line, poly, rgrad, rect, rich, text, vgrad)


# ------------------------------------------------------------------ iso
def iso_tile(cx, cy, w=140, h=80, depth=60, top="#7C5CFF", left="#4B3AA8", right="#3A2C86"):
    """Bloc isométrique simple (dessus / gauche / droite)."""
    out = []
    top_pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    left_pts = [(cx - w / 2, cy), (cx, cy + h / 2), (cx, cy + h / 2 + depth), (cx - w / 2, cy + depth)]
    right_pts = [(cx + w / 2, cy), (cx, cy + h / 2), (cx, cy + h / 2 + depth), (cx + w / 2, cy + depth)]
    out.append(poly(top_pts, fill=Fill(color=top)))
    out.append(poly(left_pts, fill=Fill(color=left)))
    out.append(poly(right_pts, fill=Fill(color=right)))
    return out


@layout("isometric-stack", "Isométrie — pile de blocs", "Illustrations isométriques")
def isometric_stack(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Architecture", c.get("title", "Une plateforme en couches"),
                        c.get("subtitle", "Chaque couche est indépendante, testée et remplaçable."),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    cx, cy = 1260, 560
    layers = c.get("layers") or [("Interface", p["accent3"]), ("Applications", p["accent"]),
                                 ("Services", p["accent2"]), ("Données", p["accent3"])]
    cmap = {"A": p["accent"], "B": p["accent2"], "C": p["accent3"], "D": p["accent"]}
    layers = [(l, cmap.get(c, c)) for l, c in layers]
    for i, (lab, col) in enumerate(layers):
        yy = cy - i * 120
        out += iso_tile(cx, yy, 460, 260, 54, top=col,
                        left=_dark(col, 0.42), right=_dark(col, 0.58))
        out.append(Text(x=cx - 230, y=yy - 4, w=460, h=40, runs=[Run(lab, color="#FFFFFF")],
                        size=24, bold=True, align="center"))
    for i, (lab, d) in enumerate([("Découplage", "Chaque service expose une API documentée."),
                                  ("Observabilité", "Traces et métriques de bout en bout."),
                                  ("Résilience", "Dégradation gracieuse et reprise automatique.")]):
        yy = 420 + i * 150
        out.append(rect(MARGIN, yy + 8, 10, 44, fill=Fill(color=p["accent"]), radius=3))
        out.append(Text(x=MARGIN + 34, y=yy, w=560, h=40, runs=[Run(lab, color=p["text"])], size=26,
                        bold=True))
        out.append(Text(x=MARGIN + 34, y=yy + 44, w=600, h=60, runs=[Run(d, color=p["muted"])], size=20,
                        line=1.4, fit=True))
    return out


def _dark(c, f):
    from ir import mix
    return mix(c, "#000000", f)


@layout("isometric-city", "Isométrie — ville / écosystème", "Illustrations isométriques")
def isometric_city(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Écosystème", c.get("title", "Une ville connectée"),
                        page=ctx.get("page"), total=ctx.get("total"), w=700)
    base_y = 860
    random.seed(3)
    for i in range(9):
        x = 780 + i * 96
        hgt = 90 + (i * 53 % 210)
        col = [p["accent"], p["accent2"], p["accent3"]][i % 3]
        out.append(rect(x, base_y - hgt, 70, hgt, fill=Fill(color=col, alpha=0.85), radius=6))
        out.append(rect(x + 10, base_y - hgt + 14, 50, 8, fill=Fill(color="#FFFFFF", alpha=0.25),
                        radius=3))
        for k in range(3):
            out.append(rect(x + 12, base_y - hgt + 34 + k * 26, 16, 12,
                            fill=Fill(color="#FFFFFF", alpha=0.35), radius=2))
        out.append(rect(x + 42, base_y - hgt + 34 + k * 26, 16, 12,
                        fill=Fill(color="#FFFFFF", alpha=0.35), radius=2))
    out.append(rect(700, base_y, 1000, 6, fill=Fill(color=p["line"])))
    for i, (lab, val) in enumerate([("Capteurs", "12 480"), ("Services", "148"), ("Citoyens", "320 k")]):
        out += B.stat(p, MARGIN, 420 + i * 170, 520, val, lab, color=p["accent2"], size=60)
    return out


@layout("isometric-flow", "Isométrie — flux de travail", "Illustrations isométriques")
def isometric_flow(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Flux", c.get("title", "Du signal à la décision"),
                        page=ctx.get("page"), total=ctx.get("total"))
    nodes = [("Collecte", "database", p["accent"]), ("Traitement", "cpu", p["accent2"]),
             ("Modélisation", "brain", p["accent3"]), ("Décision", "target", p["accent2"])]
    y = 600
    for i, (lab, ic, col) in enumerate(nodes):
        x = 260 + i * 400
        out += iso_tile(x, y, 220, 130, 40, top=col, left=_dark(col, 0.4), right=_dark(col, 0.55))
        out.append(icon_paths(x - 28, y - 66, 56, iconlib.icon_paths(ic), color="#FFFFFF", width=1.8))
        out.append(Text(x=x - 140, y=y + 90, w=280, h=36, runs=[Run(lab, color=p["text"])], size=22,
                        bold=True, align="center"))
        if i < len(nodes) - 1:
            out.append(poly([(x + 130, y - 10), (x + 240, y - 10), (x + 240, y + 6), (x + 130, y + 6)],
                            fill=Fill(color=p["line"])))
            out.append(icon_paths(x + 180, y - 22, 32, iconlib.icon_paths("chevron-right"),
                                  color=p["accent"], width=2.4))
    return out


# ------------------------------------------------------------------ néomorphique
@layout("neomorphic-cards", "Néomorphisme — cartes douces", "Style néomorphique")
def neomorphic_cards(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Interface", c.get("title", "Un design doux et tactile"),
                        c.get("subtitle", "Des volumes suggérés plutôt que dessinés."),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Clarté", "layers", "Une hiérarchie visuelle évidente."),
                               ("Douceur", "feather", "Des formes sans agressivité."),
                               ("Profondeur", "box", "Des volumes subtilement suggérés.")]
    w = 540
    for i, (t, ic, d) in enumerate(items):
        x = MARGIN + i * (w + 40)
        y = 400
        out += B.neomorph(p, x, y, w, 420, radius=54)
        out += B.circle_icon(p, x + w / 2, y + 130, 64, ic, p["accent"], alpha=0.14)
        out.append(Text(x=x + 40, y=y + 230, w=w - 80, h=44, runs=[Run(t, color=p["text"])], size=30,
                        bold=True, align="center"))
        out.append(Text(x=x + 50, y=y + 286, w=w - 100, h=80, runs=[Run(d, color=p["muted"])], size=21,
                        align="center", line=1.4, fit=True))
    return out


@layout("neomorphic-dashboard", "Néomorphisme — tableau de bord", "Style néomorphique")
def neomorphic_dashboard(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Suivi", c.get("title", "Tableau de bord apaisé"),
                        page=ctx.get("page"), total=ctx.get("total"))
    out += B.neomorph(p, MARGIN, 350, 1080, 560, radius=48)
    out.append(Text(x=MARGIN + 50, y=390, w=600, h=40, runs=[Run("Revenus récurrents", color=p["muted"])],
                    size=22))
    out.append(Text(x=MARGIN + 50, y=436, w=600, h=90, runs=[Run("128 400 €", color=p["text"])], size=64,
                    bold=True))
    from layouts.charts import area_chart
    out += area_chart(p, MARGIN + 60, 570, 980, 260, [22, 28, 26, 38, 44, 41, 56, 62, 70],
                      p["accent"], 0.35, 4.5, True)
    xs = 1200
    for i, (v, lab) in enumerate([("92 %", "Objectif"), ("+18 %", "Croissance"), ("4,7/5", "Satisfaction")]):
        out += B.neomorph(p, xs, 350 + i * 190, 560, 160, radius=40)
        out.append(Text(x=xs + 44, y=350 + i * 190 + 34, w=400, h=60, runs=[Run(v, color=p["accent"])],
                        size=48, bold=True))
        out.append(Text(x=xs + 44, y=350 + i * 190 + 98, w=400, h=34, runs=[Run(lab, color=p["muted"])],
                        size=21))
    return out


# ------------------------------------------------------------------ fait main
@layout("handmade-sketch", "Fait main — croquis annoté", "Infographie faite à la main")
def handmade_sketch(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Esquisse", c.get("title", "Le concept, à main levée"),
                        page=ctx.get("page"), total=ctx.get("total"))
    # cadre "carnet"
    out.append(rect(MARGIN, 340, 1080, 600, fill=Fill(color="#FFFDF6", alpha=0.06), radius=18,
                    stroke=Stroke(color=p["line"], width=1.5, alpha=0.7)))
    # boucle dessinée
    pts = []
    for i in range(46):
        t = i / 45 * 2 * math.pi
        pts.append((MARGIN + 300 + 190 * math.cos(t) + 5 * math.sin(7 * t),
                    600 + 150 * math.sin(t) + 5 * math.cos(5 * t)))
    out.append(poly(pts, fill=None, closed=False, stroke=Stroke(color=p["accent"], width=5, cap="round")))
    pts2 = []
    for i in range(30):
        t = i / 29 * math.pi
        pts2.append((MARGIN + 700 + 220 * t / math.pi, 470 + 120 * math.sin(t) + 4 * math.cos(9 * t)))
    out.append(poly(pts2, fill=None, closed=False, stroke=Stroke(color=p["accent2"], width=5, cap="round")))
    # flèche annotée
    out.append(poly([(MARGIN + 480, 470), (MARGIN + 640, 420)], fill=None, closed=False,
                    stroke=Stroke(color=p["accent3"], width=4, cap="round")))
    out.append(poly([(MARGIN + 600, 404), (MARGIN + 648, 418), (MARGIN + 608, 440)],
                    fill=Fill(color=p["accent3"])))
    out.append(Text(x=MARGIN + 500, y=396, w=260, h=40, runs=[Run("idée clé", color=p["accent3"])],
                    size=22, bold=True))
    out.append(Text(x=MARGIN + 60, y=800, w=900, h=90,
                    runs=[Run("« Un concept ne se valide pas sur un slide, il se valide auprès "
                              "de dix utilisateurs. »", color=p["text"])], size=23, line=1.45,
                    fit=True))
    for i, (t, d) in enumerate([("Hypothèse", "Ce que nous croyons vrai."),
                                ("Test", "Ce que nous allons mesurer."),
                                ("Apprentissage", "Ce que nous en retirons.")]):
        x = 1220
        y = 380 + i * 190
        out.append(rect(x, y, 8, 150, fill=Fill(color=[p["accent"], p["accent2"], p["accent3"]][i]),
                        radius=4))
        out.append(Text(x=x + 30, y=y + 4, w=520, h=40, runs=[Run(t, color=p["text"])], size=26,
                        bold=True))
        out.append(Text(x=x + 30, y=y + 50, w=540, h=90, runs=[Run(d, color=p["muted"])], size=20,
                        line=1.4, fit=True))
    return out


@layout("handmade-notes", "Fait main — post-its", "Infographie faite à la main")
def handmade_notes(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Atelier", c.get("title", "Idées sorties de l'atelier"),
                        page=ctx.get("page"), total=ctx.get("total"))
    notes = c.get("items") or [("Clarté", "Simplifier le parcours d'achat."),
                               ("Confiance", "Afficher les prix sans détour."),
                               ("Rapidité", "Livrer en 48 h partout."),
                               ("Proximité", "Un référent par client.")]
    cols = ["#FDE68A", "#A7F3D0", "#BFDBFE", "#FBCFE8"]
    for i, (t, d) in enumerate(notes):
        x = MARGIN + (i % 2) * 480
        y = 360 + (i // 2) * 290
        out.append(rect(x, y, 420, 250, fill=Fill(color=cols[i], alpha=0.92), radius=6,
                        anim="zoom", anim_delay=70 * i))
        out.append(rect(x + 170, y - 12, 80, 26, fill=Fill(color="#0C0A1D", alpha=0.22), radius=3))
        out.append(Text(x=x + 30, y=y + 40, w=360, h=44, runs=[Run(t, color="#1F2937")], size=30,
                        bold=True))
        out.append(Text(x=x + 30, y=y + 96, w=350, h=120, runs=[Run(d, color="#374151")], size=21,
                        line=1.45, fit=True))
    out += B.card(p, 1050, 360, 730, 560, anim="fade")
    out.append(Text(x=1090, y=390, w=650, h=40, runs=[Run("SYNTHÈSE DE L'ATELIER", color=p["accent"])],
                    size=19, bold=True, spacing=2))
    for i, v in enumerate(["Prix transparents", "Livraison 48 h", "Référent unique",
                           "Parcours en 3 clics", "Zéro paperasse"]):
        out.append(icon_paths(1090, 460 + i * 84, 30, iconlib.icon_paths("check"), color=p["accent2"],
                              width=2.4))
        out.append(Text(x=1140, y=452 + i * 84, w=600, h=44, runs=[Run(v, color=p["text"])], size=23))
    return out


# ------------------------------------------------------------------ entreprises / marketing
@layout("corporate-timeline-cards", "Entreprise — frise de jalons", "Infographies d'entreprise")
def corporate_timeline_cards(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Jalons", c.get("title", "Notre trajectoire"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("2023", "Fondation", "Premiers clients pilotes."),
                               ("2024", "Industrialisation", "Offre packagée et support 24/7."),
                               ("2025", "International", "Trois pays, quatre langues."),
                               ("2026", "Leadership", "Référence sur notre segment.")]
    w = 400
    for i, (yr, t, d) in enumerate(items):
        x = MARGIN + i * (w + 27)
        y = 420
        col = [p["accent"], p["accent2"], p["accent3"], p["accent"]][i]
        out += B.card(p, x, y, w, 380, anim="rise", delay=80 * i)
        out.append(Text(x=x + 30, y=y + 26, w=w - 60, h=70, runs=[Run(yr, color=col)], size=52,
                        bold=True))
        out.append(rect(x + 30, y + 104, 60, 4, fill=Fill(color=col), radius=2))
        out.append(Text(x=x + 30, y=y + 130, w=w - 60, h=44, runs=[Run(t, color=p["text"])], size=26,
                        bold=True))
        out.append(Text(x=x + 30, y=y + 186, w=w - 60, h=140, runs=[Run(d, color=p["muted"])], size=20,
                        line=1.45, fit=True))
    return out


@layout("marketing-channel-score", "Marketing — score par canal", "Infographies marketing")
def marketing_channel_score(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Canaux", c.get("title", "Où investir en priorité"),
                        page=ctx.get("page"), total=ctx.get("total"))
    chans = c.get("items") or [("Contenu organique", "search", 92, "+41 %"),
                               ("Email", "mail", 78, "+18 %"),
                               ("Réseaux sociaux", "share-2", 64, "+9 %"),
                               ("Publicité payante", "megaphone", 48, "−6 %"),
                               ("Événements", "calendar", 38, "+12 %")]
    for i, (lab, ic, v, d) in enumerate(chans):
        y = 360 + i * 118
        out.append(rect(MARGIN, y, W - 2 * MARGIN, 100, fill=Fill(color=p["card"], alpha=0.75),
                        radius=18, anim="rise", anim_delay=60 * i))
        out += B.circle_icon(p, MARGIN + 56, y + 50, 26, ic, p["accent"] if i == 0 else p["accent2"],
                             alpha=0.18)
        out.append(Text(x=MARGIN + 106, y=y + 30, w=420, h=40, runs=[Run(lab, color=p["text"])],
                        size=23, bold=True))
        out += B.progress(p, MARGIN + 560, y + 44, 700, v / 100,
                          p["accent"] if i == 0 else p["accent2"], h=12, delay=60 * i)
        out.append(Text(x=MARGIN + 1290, y=y + 28, w=110, h=40, runs=[Run(f"{v}", color=p["text"])],
                        size=24, bold=True, align="right"))
        out.append(Text(x=MARGIN + 1420, y=y + 30, w=140, h=40, runs=[Run(d, color=p["accent2"])],
                        size=22, bold=True, align="right"))
    return out


@layout("corporate-structure", "Organigramme", "Schémas")
def corporate_structure(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Organisation", c.get("title", "Une équipe, quatre pôles"),
                        page=ctx.get("page"), total=ctx.get("total"))
    cx, cy = W / 2, 420
    out.append(rect(cx - 200, cy - 60, 400, 120, fill=Fill(color=p["accent"]), radius=20,
                    anim="zoom"))
    out.append(Text(x=cx - 180, y=cy - 34, w=360, h=70, runs=[Run(c.get("ceo", "Direction générale"),
                                                                  color="#FFFFFF")],
                    size=26, bold=True, align="center", line=1.2))
    pods = [("Produit", "layers"), ("Technologie", "code"), ("Commercial", "trending-up"),
            ("Support", "headphones")]
    for i, (lab, ic) in enumerate(pods):
        x = MARGIN + 120 + i * 400
        y = 700
        out.append(rect(cx - 2, cy + 60, 4, 120, fill=Fill(color=p["line"])))
        out.append(rect(x + 140, 640, 4, 60, fill=Fill(color=p["line"])))
        out.append(rect(min(cx, x + 140), 638, abs(cx - (x + 140)), 4, fill=Fill(color=p["line"])))
        out.append(rect(x, y - 60, 280, 120, fill=Fill(color=p["card"]), radius=18,
                        stroke=Stroke(color=p["accent2"], width=1.5, alpha=0.6),
                        anim="rise", anim_delay=70 * i))
        out.append(icon_paths(x + 24, y - 26, 44, iconlib.icon_paths(ic), color=p["accent2"], width=1.8))
        out.append(Text(x=x + 80, y=y - 26, w=190, h=44, runs=[Run(lab, color=p["text"])], size=22,
                        bold=True))
        for j in range(3):
            out.append(Text(x=x + 24, y=y + 46 + j * 0, w=240, h=20, runs=[Run("", color=p["muted"])],
                            size=12))
    return out


@layout("scheme-layers", "Schéma — couches empilées", "Schémas")
def scheme_layers(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Architecture", c.get("title", "Trois couches, un produit"),
                        page=ctx.get("page"), total=ctx.get("total"))
    layers = c.get("items") or [("Expérience", "Interface, parcours et contenus.", p["accent"]),
                                ("Logique", "Règles métier et orchestration.", p["accent2"]),
                                ("Données", "Stockage, synchronisation, sauvegardes.", p["accent3"])]
    for i, (t, d, col) in enumerate(layers):
        x = MARGIN + 80 + i * 90
        y = 380 + i * 190
        w = W - 2 * MARGIN - 160 - i * 180
        out.append(rect(x, y, w, 160, fill=Fill(color=col, alpha=0.16), radius=24,
                        stroke=Stroke(color=col, width=1.6, alpha=0.65),
                        anim="wipe-down", anim_delay=80 * i))
        out.append(rect(x, y, 10, 160, fill=Fill(color=col), radius=5))
        out.append(Text(x=x + 40, y=y + 34, w=480, h=44, runs=[Run(t, color=p["text"])], size=28,
                        bold=True))
        out.append(Text(x=x + 40, y=y + 88, w=w - 200, h=50, runs=[Run(d, color=p["muted"])], size=21,
                        fit=True))
        out.append(Text(x=x + w - 140, y=y + 56, w=110, h=46, runs=[Run(f"0{i+1}", color=col)],
                        size=34, bold=True, align="right"))
    return out


@layout("arrow-steps", "Infographie flèches — progression", "Infographie Arrow")
def arrow_steps(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Progression", c.get("title", "Cinq niveaux de maturité"),
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = c.get("steps") or ["Réactif", "Structuré", "Mesuré", "Optimisé", "Piloté"]
    for i, s in enumerate(steps):
        y = 820 - i * 110
        x = MARGIN + 60 + i * 40
        w = W - 2 * MARGIN - 120 - i * 80
        col = [p["accent3"], p["accent3"], p["accent2"], p["accent2"], p["accent"]][i]
        pts = [(x, y), (x + w, y), (x + w + 60, y + 40), (x + w, y + 80), (x, y + 80), (x + 60, y + 40)]
        out.append(poly(pts, fill=Fill(color=col, alpha=0.22 + i * 0.12),
                        stroke=Stroke(color=col, width=1.4, alpha=0.7),
                        anim="wipe-left", anim_delay=70 * i))
        out.append(Text(x=x + 90, y=y + 22, w=w - 200, h=40, runs=[Run(s, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=x + w - 90, y=y + 22, w=80, h=40,
                        runs=[Run(f"N{i+1}", color=col)], size=22, bold=True, align="right"))
    return out


@layout("dark-infographic", "Infographie sombre — néon", "Infographies sombres")
def dark_infographic(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Signal", c.get("title", "Dans le bruit, un signal clair"),
                        page=ctx.get("page"), total=ctx.get("total"))
    # graphs "néon"
    base = 760
    bars = [180, 250, 210, 320, 280, 380, 430]
    for i, b in enumerate(bars):
        x = MARGIN + 60 + i * 170
        out.append(rect(x, base - b, 96, b, fill=Fill(color=p["accent"], stops=[(0, p["accent"], 0.95),
                                                                              (1, p["accent"], 0.15)],
                                                      angle=90), radius=10,
                        anim="wipe-up", anim_delay=60 * i))
        out.append(rect(x, base - b - 14, 96, 6, fill=Fill(color=p["accent"]), radius=3))
    out.append(rect(MARGIN + 40, base, 1200, 3, fill=Fill(color=p["accent"], alpha=0.5)))
    for i, (v, lab) in enumerate([("+312 %", "croissance des signaux"), ("0,92", "précision du modèle")]):
        out += B.stat(p, 1360, 420 + i * 210, 460, v, lab, color=p["accent2"], size=64)
    return out


# ------------------------------------------------------------------ pauses
@layout("section-break", "Pause — séparateur de section", "Diapositives de section Pause")
def section_break(p, c, ctx):
    out = bg(p, 0)
    num = str(c.get("number", "02")).zfill(2)
    out.append(Text(x=MARGIN, y=120, w=700, h=420, runs=[Run(num, color=p["accent"])], size=340,
                    bold=True, line=0.85, anim="fade"))
    out.append(Text(x=MARGIN + 10, y=520, w=1000, h=120, runs=[Run(c.get("title", "Stratégie"),
                                                                  color=p["text"])],
                    size=72, bold=True))
    out.append(Text(x=MARGIN + 10, y=640, w=900, h=90, runs=[Run(c.get("subtitle", "Le cap et les priorités"),
                                                                color=p["muted"])], size=28, line=1.4))
    for i in range(3):
        out.append(rect(MARGIN + 10 + i * 26, 760, 14, 4, fill=Fill(color=p["accent"] if i == 0 else p["line"]),
                        radius=2))
    out.append(ellipse(W - 260, H * 0.5, 330, fill=None, stroke=Stroke(color=p["accent"], width=1.6,
                                                                       alpha=0.4)))
    out.append(ellipse(W - 260, H * 0.5, 230, fill=None, stroke=Stroke(color=p["accent2"], width=1.2,
                                                                       alpha=0.3)))
    out.append(icon_paths(W - 340, H * 0.5 - 80, 160, iconlib.icon_paths(c.get("icon", "compass")),
                          color=p["accent2"], width=1.2))
    return out


@layout("section-break-image", "Pause — visuel plein cadre", "Diapositives de section Pause")
def section_break_image(p, c, ctx):
    out = bg(p, 1)
    out.append(rect(760, 0, W - 760, H, fill=Fill(color=p["accent"], color2=p["accent3"], angle=150,
                                                  alpha=0.9)))
    for i in range(4):
        out.append(ellipse(W - 200, H / 2, 120 + i * 70, fill=None,
                           stroke=Stroke(color="#FFFFFF", width=1.2, alpha=0.22)))
    out.append(icon_paths(W - 480, H / 2 - 160, 320, iconlib.icon_paths(c.get("icon", "layers")),
                          color="#FFFFFF", width=0.9))
    out += B.kicker(p, MARGIN, 240, "Section", p["accent"])
    out.append(Text(x=MARGIN, y=286, w=620, h=300, runs=[Run(c.get("title", "Produit"), color=p["text"])],
                    size=76, bold=True, line=1.0, fit=True))
    out.append(Text(x=MARGIN, y=600, w=560, h=120, runs=[Run(c.get("subtitle", "Ce que nous construisons, "
                                                                  "et pourquoi c'est différent."),
                                                            color=p["muted"])], size=26, line=1.45,
                    fit=True))
    return out


@layout("section-quote-break", "Pause — citation de section", "Diapositives de section Pause")
def section_quote_break(p, c, ctx):
    out = bg(p, 0)
    out.append(Text(x=MARGIN, y=200, w=200, h=160, runs=[Run("“", color=p["accent"])], size=220,
                    bold=True, line=0.8))
    out.append(Text(x=MARGIN + 40, y=340, w=1240, h=280,
                    runs=[Run(c.get("quote", "La stratégie, c'est choisir ce qu'on ne fait pas."),
                              color=p["text"])], size=46, line=1.36, fit=True))
    out += B.divider(p, MARGIN + 40, 660, 700)
    out.append(Text(x=MARGIN + 40, y=692, w=800, h=40, runs=[Run(c.get("author", "Michael Porter"),
                                                                color=p["muted"])], size=22))
    out += B.num_badge(p, W - MARGIN - 120, 640, c.get("number", "3"), size=110, filled=False,
                       color=p["accent"])
    return out


# ------------------------------------------------------------------ sombres
@layout("dark-kpi", "Sombre — 6 KPI", "Infographies sombres")
def dark_kpi(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Cockpit", c.get("title", "Les six indicateurs du comité"),
                        page=ctx.get("page"), total=ctx.get("total"))
    kpis = c.get("kpis") or [("48,2", "M€ de CA", "+18 %"), ("12,4", "% marge", "+2,3"),
                             ("1 240", "clients", "+9 %"), ("58", "collaborateurs", "+6"),
                             ("4,8", "/5 satisfaction", "+0,3"), ("38", "j de cash", "−4")]
    w = 400
    for i, (v, lab, d) in enumerate(kpis):
        col, row = i % 3, i // 3
        x = MARGIN + col * (w + 27)
        y = 370 + row * 280
        out += B.card(p, x, y, w, 240, anim="rise", delay=50 * i)
        out.append(Text(x=x + 30, y=y + 24, w=w - 60, h=80, runs=[Run(v, color=p["accent2"])], size=52,
                        bold=True))
        out.append(Text(x=x + 30, y=y + 108, w=w - 60, h=34, runs=[Run(lab, color=p["text"])], size=21))
        out.append(Text(x=x + 30, y=y + 168, w=w - 60, h=32, runs=[Run(d, color=p["accent3"])], size=20,
                        bold=True))
        out.append(rect(x + 30, y + 206, w - 60, 3, fill=Fill(color=p["accent"], alpha=0.5)))
    return out


@layout("dark-glow-chart", "Sombre — courbe lumineuse", "Infographies sombres")
def dark_glow_chart(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Tendance", c.get("title", "Une accélération visible"),
                        page=ctx.get("page"), total=ctx.get("total"))
    from layouts.charts import area_chart, axis_x, axis_y
    x, y, w, h = 220, 420, 1500, 460
    out += axis_y(p, x, y, w, h, 4, ["0", "20", "40", "60", "80"])
    out += axis_x(p, x, y, w, MONTHS)
    vals = [12, 18, 22, 34, 30, 42, 56, 62, 58, 70, 78, 88]
    out += area_chart(p, x, y, w, h, vals, p["accent"], 0.42, 5, True)
    out += area_chart(p, x, y, w, h, [v * 0.72 for v in vals], p["accent2"], 0.18, 3, False)
    out += B.chip(p, x + w - 360, y - 100, "+38,4 % sur l'année", p["accent"], size=21,
                  icon_name="trending-up")
    return out


# ------------------------------------------------------------------ illustration simple
@layout("illustration-abstract", "Illustration abstraite", "Illustrations")
def illustration_abstract(p, c, ctx):
    out = bg(p, 0)
    cx, cy = 1300, 600
    for i in range(7):
        out.append(Arc(cx=cx, cy=cy, r=120 + i * 60, a0=-20 + i * 12, a1=200 + i * 8,
                       stroke=Stroke(color=[p["accent"], p["accent2"], p["accent3"]][i % 3],
                                     width=3, alpha=0.28),
                       ))
    out.append(ellipse(cx, cy, 96, fill=Fill(color=p["accent"], color2=p["accent3"], angle=130),
                       anim="circle"))
    out.append(icon_paths(cx - 44, cy - 44, 88, iconlib.icon_paths(c.get("icon", "sparkles")),
                          color="#FFFFFF", width=1.6))
    out += B.kicker(p, MARGIN, 300, c.get("kicker", "Concept"), p["accent"])
    out.append(Text(x=MARGIN, y=346, w=700, h=280, runs=[Run(c.get("title", "Une idée, mille déclinaisons"),
                                                            color=p["text"])], size=56, bold=True,
                    line=1.06, fit=True))
    out.append(Text(x=MARGIN, y=640, w=620, h=120, runs=[Run(c.get("subtitle",
                                                                  "Chaque slide peut être recomposée, "
                                                                  "recolorée et adaptée à votre marque."),
                                                            color=p["muted"])], size=24, line=1.45,
                    fit=True))
    return out


@layout("illustrations-set", "Illustrations — 6 scènes", "Illustrations")
def illustrations_set(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Bibliothèque visuelle", c.get("title", "Six illustrations prêtes à l'emploi"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Croissance", "trending-up"), ("Équipe", "users"),
                               ("Idée", "lightbulb"), ("Sécurité", "shield-check"),
                               ("Livraison", "truck"), ("Support", "headphones")]
    w = 400
    for i, (lab, ic) in enumerate(items):
        col, row = i % 3, i // 3
        x = MARGIN + col * (w + 27)
        y = 380 + row * 290
        out.append(rect(x, y, w, 250, fill=Fill(color=[p["accent"], p["accent2"], p["accent3"]][i % 3],
                                                alpha=0.10), radius=26,
                        stroke=Stroke(color=p["line"], width=1.3)))
        out.append(ellipse(x + w / 2, y + 108, 74,
                           fill=Fill(color=[p["accent"], p["accent2"], p["accent3"]][i % 3], alpha=0.16)))
        out.append(icon_paths(x + w / 2 - 34, y + 74, 68, iconlib.icon_paths(ic),
                              color=[p["accent"], p["accent2"], p["accent3"]][i % 3], width=1.8))
        out.append(Text(x=x + 20, y=y + 192, w=w - 40, h=36, runs=[Run(lab, color=p["text"])], size=23,
                        bold=True, align="center"))
    return out
