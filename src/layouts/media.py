"""Chapitre : cartes du monde, cartes & drapeaux, portfolio, bannières,
figures géométriques, signes & symboles, réseaux sociaux, mises en page abstraites."""
from __future__ import annotations

import math

import geolib
import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_KICKER, T_SUB,
                           T_TITLE, W, bg, cnt, layout)
from content_data import COUNTRY_STATS, SECTORS_GEO
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths,
                line, poly, rgrad, rect, rich, text, vgrad)


# ============================================================ CARTES
@layout("map-world-dots", "Carte du monde — points", "Cartes du monde")
def map_world_dots(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Présence mondiale", c.get("title", "Où nous sommes présents"),
                        c.get("subtitle", "Six implantations, une seule équipe."),
                        page=ctx.get("page"), total=ctx.get("total"))
    box = (110, 380, 1700, 620)
    out += geolib.map_nodes(*box, color=p["accent"], alpha=0.26,
                            stroke=Stroke(color=p["accent"], width=0.9, alpha=0.35), anim="fade")
    out += geolib.arcs_routes([((2.35, 48.85), o) for o in
                               [(-17.45, 14.72), (-74.0, 40.71), (55.27, 25.2), (103.82, 1.35)]],
                              box, color=p["accent2"], width=2.2, alpha=0.85)
    out += geolib.pins([(2.35, 48.85), (-17.45, 14.72), (-74.0, 40.71), (55.27, 25.2),
                        (103.82, 1.35), (-46.63, -23.55)], box, color=p["accent2"], r=6)
    out.append(Text(x=box[0] + 10, y=392, w=700, h=34, runs=[Run("SIÈGE", color=p["accent3"])],
                    size=17, bold=True, spacing=3))
    return out


@layout("map-world-filled", "Carte — pays colorés", "Cartes du monde")
def map_world_filled(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Couverture", c.get("title", "Déploiement par pays"),
                        page=ctx.get("page"), total=ctx.get("total"))
    box = (150, 400, 1620, 580)
    out += geolib.map_nodes(*box, color=p["accent"], alpha=0.14,
                            stroke=Stroke(color=p["accent"], width=0.8, alpha=0.3))
    hi = c.get("highlight") or ["france", "senegal", "morocco", "canada", "brazil", "india"]
    out += geolib.map_nodes(*box, color=p["accent2"], alpha=0.92, only=hi)
    for i, (nm, reg, v1, v2) in enumerate(COUNTRY_STATS[:4]):
        x = MARGIN + i * 420
        out += B.card(p, x, 420, 390, 120, radius=18, anim="rise", delay=60 * i)
        out.append(Text(x=x + 22, y=432, w=340, h=34, runs=[Run(nm, color=p["text"])], size=21,
                        bold=True))
        out += B.progress(p, x + 22, 486, 300, v1 / 100, p["accent2"], h=9, delay=60 * i)
        out.append(Text(x=x + 330, y=474, w=50, h=30, runs=[Run(f"{v1}", color=p["accent2"])],
                        size=18, bold=True, align="right"))
    return out


@layout("map-globe-routes", "Carte — routes globales", "Cartes du monde")
def map_globe_routes(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Réseau", c.get("title", "Un réseau sans frontières"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    box = (760, 300, 1060, 640)
    out += geolib.map_nodes(*box, color=p["accent"], alpha=0.20,
                            stroke=Stroke(color=p["accent"], width=0.8, alpha=0.30))
    pairs = [((2.35, 48.85), (-17.45, 14.72)), ((2.35, 48.85), (37.62, 55.75)),
             ((-17.45, 14.72), (-46.63, -23.55)), ((2.35, 48.85), (103.82, 1.35)),
             ((-74.0, 40.71), (2.35, 48.85)), ((103.82, 1.35), (-122.4, 37.77))]
    out += geolib.arcs_routes(pairs, box, color=p["accent2"], width=2.0, alpha=0.9)
    out += geolib.pins([(2.35, 48.85), (-17.45, 14.72), (-46.63, -23.55), (103.82, 1.35),
                        (-74.0, 40.71), (37.62, 55.75)], box, color=p["accent3"], r=5)
    stats = [("6", "bureaux"), ("18", "pays livrés"), ("3", "langues"), ("24/7", "support")]
    for i, (v, lab) in enumerate(stats):
        out += B.stat(p, MARGIN, 360 + i * 130, 560, v, lab, color=p["accent2"], size=54)
    return out


@layout("map-country-focus", "Carte — focus pays", "Cartes du monde")
def map_country_focus(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Marché cible", c.get("title", "Opportunité par pays"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    box = (960, 330, 700, 640)
    out.append(rect(box[0], box[1], box[2], box[3], fill=Fill(color=p["accent"], alpha=0.05),
                    radius=28, stroke=Stroke(color=p["line"], width=1.2, alpha=0.6)))
    out += geolib.country_zoom(c.get("country", "france"), *box, color=p["accent2"], alpha=0.92,
                               stroke=Stroke(color=p["text"], width=1.4, alpha=0.55), anim="zoom")
    for i, (nm, reg, v1, v2) in enumerate(COUNTRY_STATS[:4]):
        y = 380 + i * 140
        out.append(rect(MARGIN, y, 660, 112, fill=Fill(color=p["card"], alpha=0.8), radius=18,
                        anim="rise", anim_delay=60 * i))
        out.append(Text(x=MARGIN + 26, y=y + 18, w=380, h=36, runs=[Run(nm, color=p["text"])],
                        size=23, bold=True))
        out.append(Text(x=MARGIN + 26, y=y + 58, w=380, h=30, runs=[Run(reg, color=p["muted"])],
                        size=18))
        out += B.progress(p, MARGIN + 400, y + 46, 200, v1 / 100, p["accent"], h=10, delay=60 * i)
        out.append(Text(x=MARGIN + 600, y=y + 34, w=60, h=30,
                        runs=[Run(f"{v1}", color=p["accent2"])], size=20, bold=True, align="right"))
    return out


# ============================================================ DRAPEAUX / SOCIAL
def flag(p, code, x, y, w=140, h=92, radius=10):
    """Drapeaux stylisés (dessinés vectoriellement, 100 % éditables)."""
    out = [rect(x, y, w, h, fill=Fill(color="#FFFFFF", alpha=0.10), radius=radius)]
    if code == "fr":
        for i, col in enumerate(["#1E40AF", "#FFFFFF", "#DC2626"]):
            out.append(rect(x + i * w / 3, y, w / 3, h, fill=Fill(color=col), radius=0))
    elif code == "sn":
        for i, col in enumerate(["#0B8A3E", "#FDE047", "#E11D48"]):
            out.append(rect(x + i * w / 3, y, w / 3, h, fill=Fill(color=col), radius=0))
        out.append(icon_paths(x + w / 2 - 11, y + h / 2 - 11, 22, iconlib.icon_paths("star"),
                              color="#0B8A3E", width=3))
    elif code == "jp":
        out.append(rect(x, y, w, h, fill=Fill(color="#FFFFFF"), radius=0))
        out.append(ellipse(x + w / 2, y + h / 2, h * 0.3, fill=Fill(color="#DC2626")))
    elif code == "ma":
        out.append(rect(x, y, w, h, fill=Fill(color="#C1272D"), radius=0))
        out.append(icon_paths(x + w / 2 - 14, y + h / 2 - 14, 28, iconlib.icon_paths("star"),
                              color="#0B6B3A", width=2.4))
    elif code == "ca":
        out.append(rect(x, y, w, h, fill=Fill(color="#FFFFFF"), radius=0))
        out.append(rect(x, y, w * 0.26, h, fill=Fill(color="#DC2626"), radius=0))
        out.append(rect(x + w * 0.74, y, w * 0.26, h, fill=Fill(color="#DC2626"), radius=0))
        out.append(icon_paths(x + w / 2 - 12, y + h / 2 - 12, 24, iconlib.icon_paths("leaf"),
                              color="#DC2626", width=2.6))
    elif code == "br":
        out.append(rect(x, y, w, h, fill=Fill(color="#0B8A3E"), radius=0))
        out.append(poly([(x + w / 2, y + h * 0.14), (x + w * 0.9, y + h / 2),
                         (x + w / 2, y + h * 0.86), (x + w * 0.1, y + h / 2)],
                        fill=Fill(color="#FDE047")))
        out.append(ellipse(x + w / 2, y + h / 2, h * 0.22, fill=Fill(color="#1E40AF")))
    elif code == "de":
        for i, col in enumerate(["#111827", "#DC2626", "#FDE047"]):
            out.append(rect(x, y + i * h / 3, w, h / 3, fill=Fill(color=col), radius=0))
    else:
        out.append(rect(x, y, w, h, fill=Fill(color=p["accent"], alpha=0.8), radius=0))
    out.append(rect(x, y, w, h, fill=Fill(color=p["accent3"], alpha=0.16), radius=radius))
    out.append(rect(x, y, w, h, fill=None, stroke=Stroke(color=p["text"], width=1, alpha=0.25),
                    radius=radius))
    return out


@layout("flags-grid", "Cartes et drapeaux — grille", "Cartes et drapeaux")
def flags_grid(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "International", c.get("title", "Nos marchés en un regard"),
                        page=ctx.get("page"), total=ctx.get("total"))
    rows = c.get("items") or [("fr", "France", "48,2 M€"), ("sn", "Sénégal", "5,8 M€"),
                              ("ma", "Maroc", "7,1 M€"), ("ca", "Canada", "10,2 M€"),
                              ("br", "Brésil", "3,9 M€"), ("jp", "Japon", "6,4 M€")]
    w = 400
    for i, (code, nm, val) in enumerate(rows):
        col, row = i % 3, i // 3
        x = MARGIN + col * (w + 27)
        y = 380 + row * 260
        out += B.card(p, x, y, w, 230, anim="rise", delay=60 * i)
        out += flag(p, code, x + 28, y + 28, 132, 86)
        out.append(Text(x=x + 184, y=y + 44, w=200, h=36, runs=[Run(nm, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=x + 184, y=y + 82, w=200, h=30, runs=[Run(val, color=p["accent2"])],
                        size=20, bold=True))
        out += B.progress(p, x + 28, y + 170, w - 56, 0.42 + i * 0.08, p["accent"], h=8, delay=60 * i)
    return out


@layout("flags-map-combo", "Carte + drapeaux", "Cartes et drapeaux")
def flags_map_combo(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Expansion", c.get("title", "Trois marchés prioritaires"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    box = (820, 340, 940, 560)
    out += geolib.map_nodes(*box, color=p["accent"], alpha=0.12,
                            stroke=Stroke(color=p["accent"], width=0.8, alpha=0.25))
    for nm, col in [("france", p["accent2"]), ("senegal", p["accent2"]), ("morocco", p["accent3"])]:
        out += geolib.country_nodes(nm, *box, color=col, alpha=0.95)
    for i, (code, nm, d) in enumerate([("fr", "France", "Marché historique, +17,6 %"),
                                       ("sn", "Sénégal", "Croissance la plus forte, +41,5 %"),
                                       ("ma", "Maroc", "Nouveau hub régional, +10,9 %")]):
        y = 400 + i * 160
        out += flag(p, code, MARGIN, y, 120, 78)
        out.append(Text(x=MARGIN + 150, y=y + 4, w=520, h=36, runs=[Run(nm, color=p["text"])],
                        size=24, bold=True))
        out.append(Text(x=MARGIN + 150, y=y + 44, w=560, h=60, runs=[Run(d, color=p["muted"])],
                        size=19, line=1.35, fit=True))
    return out


@layout("social-icons", "Réseaux sociaux — pastilles", "Icônes des réseaux sociaux")
def social_icons(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Réseaux sociaux", c.get("title", "Notre présence sociale"),
                        page=ctx.get("page"), total=ctx.get("total"))
    nets = c.get("items") or [("Instagram", "instagram", "48,2 k"), ("LinkedIn", "linkedin", "32,4 k"),
                              ("YouTube", "youtube", "18,9 k"), ("X", "x", "12,6 k"),
                              ("TikTok", "music", "41,1 k"), ("Facebook", "facebook", "27,3 k")]
    w = 400
    for i, (nm, ic, fans) in enumerate(nets):
        col, row = i % 3, i // 3
        x = MARGIN + col * (w + 27)
        y = 380 + row * 250
        colr = [p["accent"], p["accent2"], p["accent3"]][i % 3]
        out += B.card(p, x, y, w, 220, anim="zoom", delay=50 * i)
        out += B.circle_icon(p, x + w / 2, y + 84, 50, ic, colr, alpha=0.18)
        out.append(Text(x=x + 20, y=y + 146, w=w - 40, h=34, runs=[Run(nm, color=p["text"])], size=22,
                        bold=True, align="center"))
        out.append(Text(x=x + 20, y=y + 180, w=w - 40, h=30, runs=[Run(fans + " abonnés", color=colr)],
                        size=18, align="center"))
    return out


@layout("social-post-mock", "Réseaux sociaux — post mockup", "Icônes des réseaux sociaux")
def social_post_mock(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Contenus", c.get("title", "Nos formats sociaux"),
                        page=ctx.get("page"), total=ctx.get("total"), w=700)
    x, y, w, h = 880, 320, 520, 620
    out.append(rect(x, y, w, h, fill=Fill(color=p["card"]), radius=26,
                    stroke=Stroke(color=p["line"], width=1.4)))
    out.append(ellipse(x + 60, y + 56, 30, fill=Fill(color=p["accent"], color2=p["accent3"],
                                                    angle=140)))
    out.append(icon_paths(x + 46, y + 42, 28, iconlib.icon_paths("user-round"), color="#FFFFFF",
                          width=2))
    out.append(Text(x=x + 104, y=y + 38, w=300, h=28, runs=[Run("votre.marque", color=p["text"])],
                    size=19, bold=True))
    out.append(Text(x=x + 104, y=y + 66, w=300, h=24, runs=[Run("Sponsorisé", color=p["muted"])],
                    size=16))
    out.append(rect(x + 24, y + 120, w - 48, 340,
                    fill=Fill(color=p["accent"], color2=p["accent2"], angle=140, alpha=0.9), radius=18))
    out.append(icon_paths(x + w / 2 - 60, y + 250, 120, iconlib.icon_paths(c.get("icon", "sparkles")),
                          color="#FFFFFF", width=1.4))
    for j, ic in enumerate(["heart", "message-circle", "send", "bookmark"]):
        out.append(icon_paths(x + 30 + j * 44, y + 490, 26, iconlib.icon_paths(ic), color=p["text"],
                              width=1.9))
    out.append(Text(x=x + 30, y=y + 540, w=w - 60, h=60,
                    runs=[Run(c.get("caption", "1 248 j'aime · 84 commentaires"), color=p["muted"])],
                    size=17, line=1.35))
    for i, (t, d) in enumerate([("Post carrousel", "5 visuels, un seul message."),
                                ("Vidéo courte", "15 s, sous-titrée, verticale."),
                                ("Story", "Sondage et lien direct.")]):
        yy = 360 + i * 170
        out.append(rect(MARGIN, yy, 8, 110, fill=Fill(color=[p["accent"], p["accent2"], p["accent3"]][i]),
                        radius=4))
        out.append(Text(x=MARGIN + 30, y=yy + 4, w=600, h=38, runs=[Run(t, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=MARGIN + 30, y=yy + 48, w=620, h=60, runs=[Run(d, color=p["muted"])], size=19,
                        line=1.35, fit=True))
    return out


# ============================================================ PORTFOLIO
@layout("portfolio-grid", "Portfolio — grille projets", "Diapositives du portfolio")
def portfolio_grid(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Portfolio", c.get("title", "Une sélection de projets"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = c.get("items") or [("Refonte de marque", "Identité", p["accent"]),
                               ("Application mobile", "Produit", p["accent2"]),
                               ("Campagne 360°", "Marketing", p["accent3"]),
                               ("Plateforme data", "Technologie", p["accent2"]),
                               ("Site e-commerce", "Digital", p["accent"]),
                               ("Film institutionnel", "Contenu", p["accent3"])]
    w, h = 540, 300
    for i, (t, tag, col) in enumerate(items):
        col_i, row = i % 3, i // 3
        x = MARGIN + col_i * (w + 27)
        y = 360 + row * (h + 27)
        out.append(rect(x, y, w, h, fill=Fill(color=col, alpha=0.16), radius=22,
                        stroke=Stroke(color=col, width=1.3, alpha=0.5), anim="rise", anim_delay=60 * i))
        out.append(ellipse(x + w - 80, y + 56, 96, fill=Fill(color=col, alpha=0.20)))
        out.append(icon_paths(x + w - 56, y + 80, 32, iconlib.icon_paths("arrow-up-right"),
                              color=col, width=2.2))
        out += B.chip(p, x + 24, y + 24, tag, col, size=17, h=36)
        out.append(Text(x=x + 24, y=y + h - 90, w=w - 48, h=40, runs=[Run(t, color=p["text"])],
                        size=25, bold=True))
        out.append(Text(x=x + 24, y=y + h - 48, w=w - 48, h=30,
                        runs=[Run("Voir le projet  →", color=col)], size=17, bold=True))
    return out


@layout("portfolio-case", "Portfolio — étude de cas", "Diapositives du portfolio")
def portfolio_case(p, c, ctx):
    out = bg(p, 1)
    x, y, w, h = MARGIN, 150, 820, 800
    out.append(rect(x, y, w, h, fill=Fill(color=p["accent"], color2=p["accent3"], angle=140,
                                          alpha=0.85), radius=32))
    out.append(rect(x, y, w, h, fill=Fill(color=p["bg"], alpha=0.25), radius=32))
    out.append(icon_paths(x + w / 2 - 110, y + h / 2 - 150, 220,
                          iconlib.icon_paths(c.get("icon", "layers")), color="#FFFFFF", width=1.2))
    for i, (v, lab) in enumerate([("+142 %", "engagement"), ("3,2 M", "impressions")]):
        out += B.stat(p, x + 50 + i * 380, y + h - 150, 340, v, lab, color="#FFFFFF", size=54,
                      label_size=21)
    out += B.kicker(p, 980, 180, "Étude de cas", p["accent2"])
    out.append(Text(x=980, y=222, w=760, h=160, runs=[Run(c.get("title", "Refonte de marque"),
                                                          color=p["text"])], size=54, bold=True,
                    line=1.06, fit=True))
    out.append(Text(x=980, y=400, w=760, h=200, runs=[Run(c.get("text",
                 "Une identité repensée de fond en comble : positionnement, territoire visuel, "
                 "ton de voix et déclinaison sur tous les supports."), color=p["muted"])],
                    size=23, line=1.5, fit=True))
    for i, (t, d) in enumerate([("Client", c.get("client", "Groupe Altura")),
                                ("Secteur", "Services B2B"),
                                ("Durée", "14 semaines")]):
        yy = 630 + i * 90
        out.append(Text(x=980, y=yy, w=200, h=32, runs=[Run(t.upper(), color=p["accent2"])], size=16,
                        bold=True, spacing=2))
        out.append(Text(x=1200, y=yy - 4, w=520, h=36, runs=[Run(d, color=p["text"])], size=21))
    return out


@layout("portfolio-masonry", "Portfolio — mosaïque", "Diapositives du portfolio")
def portfolio_masonry(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Réalisations", c.get("title", "Nos derniers travaux"),
                        page=ctx.get("page"), total=ctx.get("total"))
    blocks = [(850, 300, 0, 0), (420, 300, 880, 0), (420, 300, 1330, 0),
              (620, 300, 0, 330), (650, 300, 650, 330), (420, 300, 1330, 330)]
    cols = [p["accent"], p["accent2"], p["accent3"], p["accent2"], p["accent"], p["accent3"]]
    icons = ["palette", "smartphone", "megaphone", "database", "shopping-bag", "film"]
    for i, (w, h, dx, dy) in enumerate(blocks):
        x, y = MARGIN + dx, 360 + dy
        w = min(w, W - MARGIN - x)
        out.append(rect(x, y, w, h, fill=Fill(color=cols[i], alpha=0.16), radius=22,
                        stroke=Stroke(color=cols[i], width=1.2, alpha=0.45),
                        anim="fade", anim_delay=50 * i))
        out.append(icon_paths(x + 30, y + 30, 44, iconlib.icon_paths(icons[i]), color=cols[i],
                              width=1.8))
        out.append(Text(x=x + 30, y=y + h - 62, w=w - 60, h=40,
                        runs=[Run(["Identité", "App mobile", "Campagne", "Data", "E-commerce",
                                   "Film"][i], color=p["text"])], size=22, bold=True))
    return out


# ============================================================ BANNIÈRES / FORMES
@layout("banner-set", "Bannières — 5 styles", "Bannières")
def banner_set(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Bannières", c.get("title", "Cinq bannières prêtes à l'emploi"),
                        page=ctx.get("page"), total=ctx.get("total"))
    y0 = 360
    # 1 ruban
    pts = [(MARGIN, y0), (1250, y0), (1310, y0 + 50), (1250, y0 + 100), (MARGIN, y0 + 100),
           (MARGIN + 60, y0 + 50)]
    out.append(poly(pts, fill=Fill(color=p["accent"], alpha=0.95)))
    out.append(Text(x=MARGIN + 120, y=y0 + 26, w=1000, h=46, runs=[Run("Bannière ruban", color="#FFFFFF")],
                    size=30, bold=True))
    # 2 pill
    out.append(rect(MARGIN, y0 + 130, 900, 88, fill=Fill(color=p["accent2"], alpha=0.2), radius=44,
                    stroke=Stroke(color=p["accent2"], width=1.6, alpha=0.7)))
    out.append(Text(x=MARGIN + 46, y=y0 + 150, w=800, h=44, runs=[Run("Bannière pilule", color=p["accent2"])],
                    size=26, bold=True))
    out.append(icon_paths(MARGIN + 830, y0 + 156, 36, iconlib.icon_paths("arrow-right"),
                          color=p["accent2"], width=2.4))
    # 3 flag
    out.append(rect(MARGIN, y0 + 250, 1040, 70, fill=Fill(color=p["accent3"], alpha=0.9), radius=8))
    out.append(poly([(MARGIN + 1040, y0 + 250), (MARGIN + 1100, y0 + 285),
                     (MARGIN + 1040, y0 + 320)], fill=Fill(color=p["accent3"], alpha=0.9)))
    out.append(Text(x=MARGIN + 40, y=y0 + 266, w=900, h=40, runs=[Run("Bannière fanion", color="#FFFFFF")],
                    size=26, bold=True))
    # 4 bracket
    out.append(rect(MARGIN, y0 + 360, 1040, 90, fill=Fill(color=p["accent"], alpha=0.14), radius=14))
    out.append(rect(MARGIN, y0 + 360, 10, 90, fill=Fill(color=p["accent"]), radius=5))
    out.append(Text(x=MARGIN + 40, y=y0 + 382, w=900, h=44, runs=[Run("Bannière encadrée", color=p["text"])],
                    size=26, bold=True))
    # 5 gradient
    out.append(rect(MARGIN, y0 + 480, 1140, 100, fill=Fill(color=p["accent"], color2=p["accent2"],
                                                           angle=15, alpha=0.95), radius=18))
    out.append(Text(x=MARGIN + 40, y=y0 + 504, w=1000, h=44,
                    runs=[Run("Bannière dégradé", color="#FFFFFF")], size=28, bold=True))
    # aside
    out += B.card(p, 1450, 380, 400, 500, anim="fade")
    out.append(Text(x=1480, y=404, w=340, h=36, runs=[Run("À RETENIR", color=p["accent2"])], size=17,
                    bold=True, spacing=2))
    for i, t in enumerate(["Couleurs modifiables", "Texte libre", "Forme vectorielle",
                           "Aucune image liée", "Export PDF net"]):
        out.append(icon_paths(1480, 462 + i * 74, 26, iconlib.icon_paths("check"), color=p["accent"],
                              width=2.4))
        out.append(Text(x=1520, y=454 + i * 74, w=330, h=40, runs=[Run(t, color=p["text"])], size=19))
    return out


@layout("shape-geometry", "Figures géométriques", "Figures géométriques")
def shape_geometry(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Géométrie", c.get("title", "Composer avec les formes"),
                        c.get("subtitle", "Une bibliothèque de formes vectorielles modifiables."),
                        page=ctx.get("page"), total=ctx.get("total"))
    cx, cy = 1300, 620
    shapes = []
    shapes.append(("hexagone", None))
    # hexagone
    pts = [(cx + 210 * math.cos(math.radians(60 * i)), cy + 210 * math.sin(math.radians(60 * i)))
           for i in range(6)]
    out.append(poly(pts, fill=None, stroke=Stroke(color=p["accent"], width=3)))
    pts2 = [(cx + 140 * math.cos(math.radians(60 * i + 30)), cy + 140 * math.sin(math.radians(60 * i + 30)))
            for i in range(6)]
    out.append(poly(pts2, fill=Fill(color=p["accent"], alpha=0.18),
                    stroke=Stroke(color=p["accent2"], width=2)))
    out.append(ellipse(cx, cy, 92, fill=Fill(color=p["accent3"], alpha=0.22),
                       stroke=Stroke(color=p["accent3"], width=2.5)))
    out.append(icon_paths(cx - 40, cy - 40, 80, iconlib.icon_paths("shapes"), color=p["text"],
                          width=1.6))
    for i, (t, d) in enumerate([("Cercles", "hiérarchie et focus"),
                                ("Triangles", "progression et tension"),
                                ("Hexagones", "systèmes et modularité"),
                                ("Lignes", "rythme et connexion")]):
        yy = 400 + i * 130
        out.append(rect(MARGIN, yy + 10, 44, 44, fill=Fill(color=[p["accent"], p["accent2"],
                                                                 p["accent3"], p["accent"]][i],
                                                           alpha=0.28), radius=10))
        out.append(Text(x=MARGIN + 70, y=yy + 6, w=560, h=38, runs=[Run(t, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=MARGIN + 70, y=yy + 48, w=600, h=50, runs=[Run(d, color=p["muted"])], size=19))
    return out


@layout("symbols-signs", "Signes et symboles", "Signes et symboles")
def symbols_signs(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Symboles", c.get("title", "Signes et repères visuels"),
                        page=ctx.get("page"), total=ctx.get("total"))
    items = [("check", "Validé"), ("x", "Rejeté"), ("circle-alert", "Attention"),
             ("info", "Information"), ("arrow-right", "Suite"), ("star", "Favori"),
             ("heart", "Préférence"), ("bookmark", "À revoir")]
    w = 400
    for i, (ic, lab) in enumerate(items):
        col_i, row = i % 4, i // 4
        x = MARGIN + col_i * (w + 27)
        y = 380 + row * 280
        out.append(rect(x, y, w, 240, fill=Fill(color=p["card"], alpha=0.85), radius=24,
                        stroke=Stroke(color=p["line"], width=1.3)))
        out += B.circle_icon(p, x + w / 2, y + 96, 52, ic,
                             [p["accent2"], p["accent3"], p["accent"], p["accent2"]][i % 4],
                             alpha=0.16)
        out.append(Text(x=x + 20, y=y + 168, w=w - 40, h=34, runs=[Run(lab, color=p["text"])], size=22,
                        bold=True, align="center"))
    return out


@layout("abstract-layout-1", "Mise en page abstraite — bloc", "Mises en page abstraites")
def abstract_1(p, c, ctx):
    out = bg(p, 0)
    out.append(rect(0, 0, W * 0.46, H, fill=Fill(color=p["accent"], color2=p["accent3"], angle=160,
                                                 alpha=0.9)))
    for i in range(3):
        out.append(ellipse(W * 0.30, H * 0.5, 160 + i * 90, fill=None,
                           stroke=Stroke(color="#FFFFFF", width=1.2, alpha=0.20)))
    out.append(icon_paths(W * 0.30 - 90, H * 0.5 - 90, 180,
                          iconlib.icon_paths(c.get("icon", "sparkles")), color="#FFFFFF", width=1.2))
    out += B.kicker(p, W * 0.52, 220, c.get("kicker", "Concept"), p["accent2"])
    out.append(Text(x=W * 0.52, y=262, w=820, h=260, runs=[Run(c.get("title", "Une mise en page audacieuse"),
                                                              color=p["text"])], size=58, bold=True,
                    line=1.06, fit=True))
    out.append(Text(x=W * 0.52, y=560, w=760, h=180, runs=[Run(c.get("text",
                 "De grandes zones de respiration, un contraste fort et une hiérarchie limpide : "
                 "la forme sert toujours le propos."), color=p["muted"])], size=23, line=1.5, fit=True))
    out += B.chip(p, W * 0.52, 780, "Éditable", p["accent2"], size=20)
    return out


@layout("abstract-layout-2", "Mise en page abstraite — ondes", "Mises en page abstraites")
def abstract_2(p, c, ctx):
    out = bg(p, 1)
    for k in range(4):
        pts = []
        for i in range(60):
            t = i / 59
            pts.append((MARGIN + t * (W - 2 * MARGIN),
                        H * 0.62 + 120 * math.sin(t * 6.2 + k * 0.9) - k * 26))
        out.append(poly(pts, fill=None, closed=False, smooth=True,
                        stroke=Stroke(color=[p["accent"], p["accent2"], p["accent3"], p["accent"]][k],
                                      width=2.4, alpha=0.55 - k * 0.08)))
    out += B.kicker(p, MARGIN, 200, c.get("kicker", "Exploration"), p["accent"])
    out.append(Text(x=MARGIN, y=244, w=1000, h=220, runs=[Run(c.get("title", "Des courbes, des idées"),
                                                             color=p["text"])], size=64, bold=True,
                    line=1.05, fit=True))
    out.append(Text(x=MARGIN, y=470, w=780, h=120, runs=[Run(c.get("text",
                 "Les ondes traduisent le mouvement : elles donnent du rythme sans jamais "
                 "concurrencer le message."), color=p["muted"])], size=22, line=1.5, fit=True))
    return out


@layout("scene-desk", "Infographie de scène — bureau", "Infographies de scène")
def scene_desk(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Scène", c.get("title", "Un environnement de travail repensé"),
                        page=ctx.get("page"), total=ctx.get("total"), w=800)
    bx, by = 900, 760
    # bureau
    out.append(rect(bx - 40, by, 900, 22, fill=Fill(color=p["accent"], alpha=0.55), radius=8))
    out.append(rect(bx + 40, by + 22, 26, 150, fill=Fill(color=p["line"])))
    out.append(rect(bx + 720, by + 22, 26, 150, fill=Fill(color=p["line"])))
    # écran
    out.append(rect(bx + 220, by - 330, 420, 280, fill=Fill(color=p["card"]), radius=18,
                    stroke=Stroke(color=p["accent2"], width=2, alpha=0.7)))
    out.append(rect(bx + 250, by - 300, 360, 200, fill=Fill(color=p["accent2"], alpha=0.14), radius=10))
    out.append(icon_paths(bx + 380, by - 258, 100, iconlib.icon_paths("chart-line"),
                          color=p["accent2"], width=1.7))
    out.append(rect(bx + 410, by - 50, 40, 50, fill=Fill(color=p["line"])))
    # plante
    out.append(rect(bx + 60, by - 100, 80, 100, fill=Fill(color=p["accent3"], alpha=0.35), radius=10))
    for k in range(4):
        out.append(ellipse(bx + 100 + (k - 1.5) * 22, by - 130 - abs(k - 1.5) * 10, 30,
                           fill=Fill(color=p["accent3"], alpha=0.35)))
    # clavier + souris
    out.append(rect(bx + 300, by - 34, 260, 30, fill=Fill(color=p["card"]), radius=8,
                    stroke=Stroke(color=p["line"], width=1.2)))
    out.append(ellipse(bx + 620, by - 24, 22, 18, fill=Fill(color=p["card"]),
                       stroke=Stroke(color=p["line"], width=1.2)))
    for i, (t, d) in enumerate([("Poste ergonomique", "Écran à hauteur des yeux, lumière naturelle."),
                                ("Outils intégrés", "Un seul espace pour tout piloter."),
                                ("Flexibilité", "Présentiel et distanciel sans friction.")]):
        yy = 380 + i * 150
        out += B.circle_icon(p, MARGIN + 40, yy + 40, 30,
                             ["monitor", "layers", "house"][i], p["accent2"], alpha=0.18)
        out.append(Text(x=MARGIN + 96, y=yy + 8, w=680, h=38, runs=[Run(t, color=p["text"])], size=24,
                        bold=True))
        out.append(Text(x=MARGIN + 96, y=yy + 50, w=700, h=60, runs=[Run(d, color=p["muted"])], size=19,
                        line=1.35, fit=True))
    return out
