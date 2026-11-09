"""Chapitre : sommaire, à propos, équipe, témoignages, clôture."""
from __future__ import annotations

import iconlib
from layouts._base import (B, H, MARGIN, REGISTRY, T_BODY, T_KICKER, T_SUB,
                           T_TITLE, W, bg, cnt, layout)
from ir import (Arc, Ellipse, Fill, Run, Stroke, Text, ellipse, icon_paths,
                line, poly, rgrad, rect, rich, text, vgrad)
from content_data import TESTIMONIALS, VALUES


# ------------------------------------------------------------------ sommaire
@layout("agenda-numbered", "Sommaire — liste numérotée", "Sommaire")
def agenda_numbered(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Sommaire", c.get("title", "Ce que nous allons voir"),
                        page=ctx.get("page"), total=ctx.get("total"), w=760)
    items = c.get("items") or [("Contexte & enjeux", "Où nous en sommes"),
                               ("Stratégie", "Notre cap à trois ans"),
                               ("Plan d'action", "Les chantiers prioritaires"),
                               ("Indicateurs", "Comment nous mesurons"),
                               ("Prochaines étapes", "Décisions attendues")]
    x = 860
    y0 = 150
    for i, it in enumerate(items):
        y = y0 + i * 150
        t, sub = (it if isinstance(it, tuple) else (it, ""))
        out += B.num_badge(p, x, y, i + 1, size=56, color=p["accent"] if i == 0 else p["accent2"],
                           filled=(i == 0))
        out.append(Text(x=x + 80, y=y + 2, w=780, h=44,
                        runs=[Run(t, color=p["text"])], size=32, bold=True, anim="rise",
                        anim_delay=60 * i))
        out.append(Text(x=x + 80, y=y + 44, w=780, h=36,
                        runs=[Run(sub, color=p["muted"])], size=21, anim="rise",
                        anim_delay=60 * i + 30))
        out.append(rect(x, y + 100, 900, 1, fill=Fill(color=p["line"], alpha=0.6)))
    return out


@layout("agenda-cards", "Sommaire — cartes 2×3", "Sommaire")
def agenda_cards(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Sommaire", c.get("title", "Le programme"),
                        page=ctx.get("page"), total=ctx.get("total"))
    icons = ["target", "compass", "layers", "trending-up", "users", "map"]
    items = c.get("items") or [("Contexte", "Où nous en sommes"), ("Stratégie", "Notre cap"),
                               ("Produit", "Ce que nous livrons"), ("Marché", "Nos clients"),
                               ("Équipe", "Qui fait quoi"), ("Roadmap", "Les prochaines étapes")]
    w, h = 520, 190
    for i, it in enumerate(items):
        col, row = i % 3, i // 3
        x = MARGIN + col * (w + 40)
        y = 330 + row * (h + 40)
        t, desc = (it if isinstance(it, tuple) else (it, ""))
        ic = icons[i % len(icons)]
        out += B.card(p, x, y, w, h, anim="rise", delay=70 * i)
        out += B.circle_icon(p, x + 70, y + 70, 42, ic, p["accent"], alpha=0.16)
        out.append(Text(x=x + 40, y=y + 118, w=w - 80, h=40,
                        runs=[Run(f"{i+1:02d} · {t}", color=p["text"])], size=27, bold=True))
    return out


# ------------------------------------------------------------------ à propos
@layout("about-split", "À propos — texte + visuel", "À propos")
def about_split(p, c, ctx):
    out = bg(p, 0)
    out += B.kicker(p, MARGIN, 150, c.get("kicker", "À propos"), p["accent"])
    out.append(Text(x=MARGIN, y=196, w=800, h=260,
                    runs=[Run(c.get("title", "Qui sommes-nous ?"), color=p["text"])],
                    size=62, bold=True, line=1.06, fit=True))
    out += B.body(p, MARGIN, 430, 720, 260, c.get("text",
                 "Nous concevons des solutions simples pour des problèmes complexes. "
                 "Depuis douze ans, notre équipe accompagne les organisations dans leurs "
                 "transformations les plus ambitieuses, avec une obsession : l'impact réel."),
                 size=25)
    out += B.stat(p, MARGIN, 700, 320, c.get("s1", "12 ans"), "d'expertise", color=p["accent"], size=64)
    out += B.stat(p, MARGIN + 360, 700, 320, c.get("s2", "180+"), "projets livrés", color=p["accent2"], size=64)
    # visuel
    x, y, w, h = 900, 170, 900, 740
    out.append(rect(x, y, w, h, fill=Fill(color=p["card"], color2=p["accent"], angle=150, alpha=0.75),
                    radius=40))
    out.append(rect(x, y, w, h, fill=Fill(color=p["bg"], alpha=0.35), radius=40))
    out.append(ellipse(x + w * 0.5, y + h * 0.42, 250,
                       fill=Fill(color=p["accent2"], stops=[(0, p["accent2"], 0.35), (1, p["accent2"], 0)])))
    out.append(icon_paths(x + w / 2 - 110, y + h / 2 - 130, 220,
                          iconlib.icon_paths(c.get("icon", "building-2")), color=p["text"], width=1.2))
    out += B.chip(p, x + 50, y + h - 90, c.get("tag", "Notre mission"), p["accent2"], size=22)
    out += B.footer(p, ctx.get("page", 1), ctx.get("total"))
    return out


@layout("values-grid", "Valeurs — grille 3×2", "À propos")
def values_grid(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Culture", c.get("title", "Nos six valeurs"),
                        c.get("subtitle", "Ce qui guide nos décisions au quotidien."),
                        page=ctx.get("page"), total=ctx.get("total"), w=900)
    vals = c.get("values") or VALUES
    colors = [p["accent"], p["accent2"], p["accent3"]]
    w, h = 520, 210
    for i, (t, d) in enumerate(vals[:6]):
        col, row = i % 3, i // 3
        x, y = MARGIN + col * (w + 40), 400 + row * (h + 30)
        out += B.card(p, x, y, w, h, anim="rise", delay=60 * i)
        out.append(rect(x, y + 24, 6, h - 48, fill=Fill(color=colors[i % 3]), radius=3))
        out.append(Text(x=x + 34, y=y + 28, w=w - 60, h=38, runs=[Run(t, color=p["text"])],
                        size=28, bold=True))
        out.append(Text(x=x + 34, y=y + 76, w=w - 66, h=110, runs=[Run(d, color=p["muted"])],
                        size=20, line=1.45, fit=True))
    return out


@layout("mission-vision", "Mission / Vision / Valeurs", "À propos")
def mission_vision(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Notre raison d'être", c.get("title", "Mission, vision, valeurs"),
                        page=ctx.get("page"), total=ctx.get("total"))
    cols = [("Mission", c.get("mission", "Rendre la décision évidente."), "target", p["accent"]),
            ("Vision", c.get("vision", "Un monde où chaque équipe voit clair."), "eye", p["accent2"]),
            ("Valeurs", c.get("values", "Exigence, transparence, collectif."), "heart", p["accent3"])]
    w = 560
    for i, (t, d, ic, col) in enumerate(cols):
        x = MARGIN + i * (w + 40)
        y = 360
        out += B.card(p, x, y, w, 480, anim="rise", delay=90 * i)
        out += B.circle_icon(p, x + w / 2, y + 110, 58, ic, col, alpha=0.18)
        out.append(Text(x=x + 40, y=y + 190, w=w - 80, h=44, runs=[Run(t.upper(), color=col)],
                        size=22, bold=True, align="center", spacing=3))
        out.append(Text(x=x + 44, y=y + 244, w=w - 88, h=190,
                        runs=[Run(d, color=p["text"])], size=26, line=1.35,
                        align="center", fit=True))
    return out


# ------------------------------------------------------------------ équipe
@layout("team-grid", "Équipe — portraits 4 col.", "Équipe")
def team_grid(p, c, ctx):
    from content_data import TEAM
    out = bg(p, 0)
    out += B.slide_head(p, "Équipe", c.get("title", "Les visages du projet"),
                        c.get("subtitle", "Une équipe pluridisciplinaire, engagée et disponible."),
                        page=ctx.get("page"), total=ctx.get("total"))
    team = c.get("team") or TEAM
    w, h = 400, 470
    for i, (nm, role, ic) in enumerate(team[:4]):
        x = MARGIN + i * (w + 27)
        y = 400
        out += B.card(p, x, y, w, h, anim="rise", delay=80 * i)
        out.append(ellipse(x + w / 2, y + 150, 96,
                           fill=Fill(color=p["accent"] if i % 2 == 0 else p["accent2"],
                                     color2=p["accent3"], angle=140, alpha=0.9)))
        out.append(icon_paths(x + w / 2 - 52, y + 98, 104, iconlib.icon_paths("user-round"),
                              color="#FFFFFF", width=1.5))
        out.append(Text(x=x + 20, y=y + 268, w=w - 40, h=44, runs=[Run(nm, color=p["text"])],
                        size=26, bold=True, align="center"))
        out.append(Text(x=x + 20, y=y + 312, w=w - 40, h=60, runs=[Run(role, color=p["muted"])],
                        size=20, align="center", line=1.3))
        for j, soc in enumerate(["linkedin", "mail"]):
            out.append(icon_paths(x + w / 2 - 30 + j * 40, y + 396, 24, iconlib.icon_paths(soc),
                                  color=p["muted"], width=1.8))
    return out


@layout("team-feature", "Équipe — focus dirigeant", "Équipe")
def team_feature(p, c, ctx):
    out = bg(p, 1)
    x, y, w, h = MARGIN, 170, 520, 740
    out.append(rect(x, y, w, h, fill=Fill(color=p["card"], color2=p["accent"], angle=150, alpha=0.8),
                    radius=36))
    out.append(ellipse(x + w / 2, y + 260, 150, fill=Fill(color=p["accent2"], alpha=0.35)))
    out.append(icon_paths(x + w / 2 - 110, y + 150, 220, iconlib.icon_paths("user-round"),
                          color="#FFFFFF", width=1.3))
    out.append(Text(x=x + 40, y=y + 480, w=w - 80, h=60,
                    runs=[Run(c.get("name", "Aminata Diallo"), color=p["text"])],
                    size=34, bold=True, align="center"))
    out.append(Text(x=x + 40, y=y + 536, w=w - 80, h=40,
                    runs=[Run(c.get("role", "Directrice générale"), color=p["accent2"])],
                    size=22, align="center"))
    out += B.kicker(p, 760, 200, "Mot de la direction", p["accent"])
    out.append(Text(x=760, y=250, w=1000, h=400,
                    runs=[Run("« " + c.get("quote", "Notre force, c'est de transformer une ambition "
                              "collective en résultats concrets, trimestre après trimestre. Nous "
                              "avançons vite, mais jamais sans nos valeurs.") + " »", color=p["text"])],
                    size=40, line=1.35, fit=True, italic=False))
    out += B.divider(p, 760, 690, 900)
    for i, v in enumerate([("+12 ans", "d'expérience"), ("18", "pays"), ("4", "langues")]):
        out += B.stat(p, 760 + i * 330, 726, 300, v[0], v[1], color=p["accent"], size=58)
    return out


# ------------------------------------------------------------------ témoignages
@layout("testimonial-quote", "Témoignage — citation pleine page", "Témoignages")
def testimonial_quote(p, c, ctx):
    out = bg(p, 0)
    out.append(Text(x=MARGIN, y=150, w=300, h=200, runs=[Run("“", color=p["accent"])],
                    size=240, bold=True, line=0.8))
    out.append(Text(x=MARGIN + 30, y=300, w=1400, h=420,
                    runs=[Run(c.get("quote", TESTIMONIALS[0][0].strip("« »")), color=p["text"])],
                    size=48, line=1.34, fit=True))
    out += B.divider(p, MARGIN + 30, 760, 900)
    out += B.circle_icon(p, MARGIN + 90, 840, 44, "user-round", p["accent2"], alpha=0.2)
    out.append(Text(x=MARGIN + 160, y=800, w=800, h=40,
                    runs=[Run(c.get("name", "Claire Fontaine"), color=p["text"])], size=25, bold=True))
    out.append(Text(x=MARGIN + 160, y=842, w=800, h=40,
                    runs=[Run(c.get("role", "Directrice des opérations, Novara"), color=p["muted"])],
                    size=20))
    out += B.footer(p, ctx.get("page", 1), ctx.get("total"))
    return out


@layout("testimonial-grid", "Témoignages — 3 cartes", "Témoignages")
def testimonial_grid(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Ils nous font confiance", c.get("title", "Ce qu'ils en disent"),
                        page=ctx.get("page"), total=ctx.get("total"))
    w = 560
    for i, (q, nm, role) in enumerate(TESTIMONIALS):
        x = MARGIN + i * (w + 40)
        y = 380
        out += B.card(p, x, y, w, 430, anim="rise", delay=90 * i)
        for s in range(5):
            out.append(icon_paths(x + 34 + s * 30, y + 32, 24, iconlib.icon_paths("star"),
                                  color=p["accent"] if i == 0 else p["accent2"], width=2.2))
        out.append(Text(x=x + 34, y=y + 80, w=w - 68, h=230, runs=[Run(q, color=p["text"])],
                        size=22, line=1.5, fit=True))
        out.append(Text(x=x + 34, y=y + 330, w=w - 68, h=36, runs=[Run(nm, color=p["text"])],
                        size=21, bold=True))
        out.append(Text(x=x + 34, y=y + 366, w=w - 68, h=50, runs=[Run(role, color=p["muted"])],
                        size=18, line=1.3))
    return out


# ------------------------------------------------------------------ clôture
@layout("closing-thanks", "Clôture — merci", "Clôture")
def closing_thanks(p, c, ctx):
    out = bg(p, 0)
    out.append(ellipse(W * 0.5, H * 0.42, 560,
                       fill=Fill(color=p["accent"], stops=[(0, p["accent"], 0.34), (1, p["accent"], 0)])))
    out.append(Text(x=MARGIN, y=300, w=W - 2 * MARGIN, h=180,
                    runs=[Run(c.get("title", "Merci."), color=p["text"])], size=130, bold=True,
                    align="center"))
    out.append(Text(x=340, y=470, w=W - 680, h=110,
                    runs=[Run(c.get("subtitle", "Des questions ? Discutons de vos prochains enjeux."),
                              color=p["muted"])], size=30, line=1.4, align="center", fit=True))
    out += B.chip(p, W / 2 - 220, 610, c.get("contact", "contact@exemple.com"), p["accent2"], size=24, w=440)
    out.append(rect(W / 2 - 60, 700, 120, 4, fill=Fill(color=p["accent"]), radius=2))
    return out


@layout("closing-contact", "Clôture — contact 4 blocs", "Clôture")
def closing_contact(p, c, ctx):
    out = bg(p, 1)
    out += B.slide_head(p, "Contact", c.get("title", "Restons en contact"),
                        page=ctx.get("page"), total=ctx.get("total"))
    blocks = [("Adresse", "12 avenue de la Paix\n75011 Paris", "map-pin"),
              ("Téléphone", "+33 1 84 80 00 00", "phone"),
              ("Email", "contact@exemple.com", "mail"),
              ("Site web", "www.exemple.com", "globe")]
    w = 400
    for i, (t, d, ic) in enumerate(blocks):
        x = MARGIN + (i % 4) * (w + 27)
        y = 380
        out += B.card(p, x, y, w, 260, anim="rise", delay=80 * i)
        out += B.circle_icon(p, x + w / 2, y + 80, 46, ic, p["accent"], alpha=0.18)
        out.append(Text(x=x + 20, y=y + 140, w=w - 40, h=34, runs=[Run(t, color=p["muted"])],
                        size=19, align="center", caps=True, spacing=2))
        out.append(Text(x=x + 20, y=y + 176, w=w - 40, h=70, runs=[Run(d, color=p["text"])],
                        size=21, align="center", line=1.35, bold=True))
    out.append(rect(MARGIN, 700, W - 2 * MARGIN, 1, fill=Fill(color=p["line"])))
    for j, soc in enumerate(["linkedin", "instagram", "youtube", "x"]):
        out += B.circle_icon(p, W / 2 - 90 + j * 60, 780, 22, soc, p["accent2"], alpha=0.15)
    return out


@layout("guide-mode-emploi", "Mode d'emploi du pack", "Sommaire")
def guide_mode_emploi(p, c, ctx):
    out = bg(p, 0)
    out += B.slide_head(p, "Mode d'emploi", "Comment utiliser ce pack",
                        "Tout est vectoriel : chaque bloc se modifie en deux clics.",
                        page=ctx.get("page"), total=ctx.get("total"))
    steps = [("1", "Choisissez une diapositive", "Parcourez le volume, dupliquez la slide qui "
              "vous intéresse (Ctrl+C / Ctrl+V dans votre présentation).", "copy"),
             ("2", "Modifiez les textes", "Cliquez dans la zone de texte et tapez. La police "
              "Poppins est embarquée dans le fichier.", "type"),
             ("3", "Changez les couleurs", "Sélectionnez une forme → Format → Remplissage. "
              "Les dégradés restent nets (vectoriels).", "palette"),
             ("4", "Lancez les animations", "Touche F5 : les éléments apparaissent en cascade. "
              "Ajustez-les dans Animations.", "play")]
    w = 400
    for i, (n, t, d, ic) in enumerate(steps):
        x = MARGIN + i * (w + 27)
        y = 420
        out += B.card(p, x, y, w, 400, anim="rise", delay=80 * i)
        out.append(Text(x=x + 30, y=y + 22, w=80, h=80, runs=[Run(n, color=p["accent"])], size=52,
                        bold=True))
        out += B.circle_icon(p, x + w - 68, y + 62, 32, ic, p["accent2"], alpha=0.18)
        out.append(Text(x=x + 30, y=y + 108, w=w - 60, h=78, runs=[Run(t, color=p["text"])], size=23,
                        bold=True, line=1.25, fit=True))
        out.append(Text(x=x + 30, y=y + 196, w=w - 60, h=180, runs=[Run(d, color=p["muted"])], size=18,
                        line=1.45, fit=True))
    out += B.chip(p, MARGIN, 880, "Astuce : Ctrl+A puis remplacer la couleur d'accent sur tout un slide",
                  p["accent3"], size=18, h=42)
    return out
