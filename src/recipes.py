"""Recettes : quels layouts, dans quel ordre, avec quel contenu.

Chaque recette est une fonction (S, i) -> (layout_key, contenu, options)
où S = données du secteur et i = indice de répétition (pour varier les textes).
"""
from __future__ import annotations

import content_data as CD

S = CD.SECTORS


def _icon(S_, i, k=0):
    ic = S_["icons"]
    return ic[(i + k) % len(ic)]


def build_recipes(S_, sector_key):
    """Retourne la liste ordonnée des recettes du pack pour un secteur."""
    kpis = S_["kpis"]
    items = S_["items"]
    steps = S_["steps"]
    lab = S_["label"]

    def cover(i):
        variants = ["cover-hero-glow", "cover-split-block", "cover-neomorphism",
                    "cover-minimal-type", "cover-image-frame", "cover-dark-mesh"]
        return (variants[i % len(variants)],
                {"title": S_["title"], "subtitle": S_["subtitle"], "kicker": S_["kicker"],
                 "author": "Votre nom", "tag": lab, "icon": _icon(S_, i)})

    def agenda(i):
        return ("agenda-numbered" if i % 2 == 0 else "agenda-cards",
                {"title": "Ce que nous allons voir",
                 "items": [(items[0][0], "Le contexte et les enjeux"),
                           (items[1][0], "Notre approche"),
                           (items[2][0], "Le plan d'action"),
                           (items[3][0], "Les indicateurs"),
                           ("Prochaines étapes", "Décisions attendues")]})

    def about(i):
        return ("about-split" if i % 2 == 0 else "mission-vision",
                {"title": f"{lab} : notre positionnement",
                 "kicker": "Contexte",
                 "text": f"{S_['subtitle']} Nous accompagnons les organisations de notre secteur "
                         f"avec une méthode simple : comprendre, prioriser, exécuter, mesurer.",
                 "icon": _icon(S_, i, 1)})

    def kpi(i):
        return ("kpi-grid", {"title": "Les chiffres clés",
                             "kpis": [(k[0], k[1], ["+12 %", "+4,2 pts", "+9 %", "−6 %"][j], _icon(S_, i + j, 2))
                                      for j, k in enumerate(kpis)]})

    def big(i):
        return ("chart-big-number", {"value": kpis[i % 4][0], "kicker": "Impact mesuré",
                                     "text": f"{kpis[i % 4][1]} : une progression obtenue grâce à "
                                             f"un pilotage resserré et des décisions rapides."})

    def chart_line(i):
        return ("chart-line", {"title": f"Évolution — {kpis[0][1].lower()}",
                               "subtitle": f"Une trajectoire régulière sur douze mois, "
                                           f"portée par {items[0][0].lower()}.",
                               "l1": kpis[0][1][:18], "l2": kpis[1][1][:18]})

    def chart_bar(i):
        return ("chart-bar", {"title": f"{kpis[3][1][:26]} par période",
                              "tag": kpis[3][0] + " vs N-1",
                              "labels": S_.get("years", ["2021", "2022", "2023", "2024", "2025", "2026"])})

    def donut(i):
        return ("chart-donut", {"title": f"Répartition — {kpis[0][1]}",
                                "items": [(items[0][0], 46, "A"), (items[1][0], 28, "B"),
                                          (items[2][0], 16, "C"), (items[3][0], 10, "D")],
                                "center": kpis[0][0], "center_sub": "total"})

    def table(i):
        regions = S_.get("regions", [])
        rows = [(regions[j], f"{8 + j * 3},2 M€", f"{9 + j * 4},1 M€", f"+{(j + 1) * 4},{(j + 3) % 9} %",
                 "En avance" if j % 2 == 0 else "Conforme") for j in range(4)]
        rows.append(("Autres", "3,2 M€", "3,9 M€", "+21,9 %", "En avance"))
        return ("chart-table", {"title": f"Performance par marché — {lab}", "rows": rows})

    def gauge(i):
        return ("chart-gauge", {"title": f"Atteinte de l'objectif — {kpis[1][1][:22]}",
                                "value": "74 %", "ratio": 0.74,
                                "label": "de l'objectif atteint à date"})

    def swot(i):
        return ("swot", {"title": "Analyse SWOT"})

    def swot2(i):
        return ("swot-matrix", {"title": "Matrice de priorisation",
                                "data": [[items[0][0], items[1][0], items[2][0]],
                                         [items[2][0], "Concurrence", "Coûts"],
                                         [items[3][0], "Nouveaux usages", "Partenariats"],
                                         ["Réglementation", "Talents", "Technologie"]]})

    def seven_s(i):
        return ("mckinsey-7s", {"title": "Le modèle McKinsey 7S",
                                "subtitle": "Sept leviers interdépendants : si l'un bouge, tous bougent."})

    def seven_s2(i):
        return ("seven-s-cards", {"title": "Où agir en priorité"})

    def process(i):
        return ("process-horizontal", {"title": f"Notre processus — {lab}", "steps": steps})

    def chevron(i):
        return ("process-chevron", {"title": "Le parcours, étape par étape", "steps": steps})

    def cards(i):
        return ("process-steps-cards", {"title": "Quatre étapes pour démarrer",
                                        "items": [(items[0][0], items[0][1], _icon(S_, i)),
                                                  (items[1][0], items[1][1], _icon(S_, i, 1)),
                                                  (items[2][0], items[2][1], _icon(S_, i, 2)),
                                                  (items[3][0], items[3][1], _icon(S_, i, 3))]})

    def cycle(i):
        return ("cycle-arrows", {"title": "Un cycle d'amélioration continue",
                                 "steps": [steps[0], steps[1], steps[2], steps[3]][:4]})

    def rings(i):
        return ("cycle-rings", {"title": "Trois cercles d'influence", "center": items[0][0],
                                "icon": _icon(S_, i)})

    def ring_progress(i):
        return ("cycle-ring-progress", {"title": "Où nous en sommes"})

    def circular(i):
        return ("cycle-circular-list", {"title": "Six leviers articulés", "center": "Mix",
                                        "items": [(items[0][0], _icon(S_, i)),
                                                  (items[1][0], _icon(S_, i, 1)),
                                                  (items[2][0], _icon(S_, i, 2)),
                                                  (items[3][0], _icon(S_, i, 3)),
                                                  ("Preuve", "badge-check"),
                                                  ("Suivi", "gauge")]})

    def funnel(i):
        return ("funnel-5", {"title": "De l'intérêt à la fidélisation", "steps": None}) \
            if False else ("funnel-5", {"title": "De l'intérêt à la fidélisation",
                                        "steps": [("Contacts", "48 200", 1.0),
                                                  ("Prospects", "12 400", 0.78),
                                                  ("Qualifiés", "4 800", 0.58),
                                                  ("Clients", "1 640", 0.40),
                                                  ("Fidèles", "620", 0.24)]})

    def sales(i):
        return ("funnel-sales", {"title": "Notre pipeline commercial"})

    def scene(i):
        return ("funnel-stage-scene", {"title": "Attirer, convertir, fidéliser",
                                       "scene_title": items[0][0]})

    def pyramid(i):
        return ("pyramid-4", {"title": f"De la vision à l'exécution — {lab}", "keep_order": True,
                              "items": [("Vision", "Où nous allons — l'ambition à trois ans"),
                                        ("Stratégie", "Comment y aller — le cap et les priorités"),
                                        ("Tactique", "Ce que nous faisons cette année — les chantiers"),
                                        ("Opérations", "Qui fait quoi — les rôles et les rituels")]})

    def maslow(i):
        return ("pyramid-maslow", {"title": "Les niveaux de maturité"})

    def timeline(i):
        return ("timeline-horizontal", {"title": "Les grandes étapes du projet",
                                        "items": [(f"T{q+1} 2026", steps[q],
                                                   items[q][1] if q < len(items) else "Étape clé")
                                                  for q in range(4)]})

    def timeline_v(i):
        return ("timeline-vertical", {"title": "Notre historique"})

    def timeline_c(i):
        return ("timeline-curved", {"title": "Un parcours en cinq jalons", "steps": steps[:5]
                                    if len(steps) >= 5 else steps + ["Bilan"]})

    def icons(i):
        return ("icons-grid-8", {"title": "Huit icônes, mille usages",
                                 "items": [(v[0], v[1]) for v in
                                           [(items[0][0], _icon(S_, i)), (items[1][0], _icon(S_, i, 1)),
                                            (items[2][0], _icon(S_, i, 2)), (items[3][0], _icon(S_, i, 3)),
                                            ("Données", "database"), ("Sécurité", "shield-check"),
                                            ("Croissance", "trending-up"), ("Support", "headphones")]]})

    def features(i):
        return ("icons-feature-4", {"title": "Ce qui fait la différence",
                                    "items": [("Rapide", "Déployé en trois semaines, sans projet lourd.", "zap"),
                                              ("Fiable", "Une disponibilité mesurée chaque mois.", "shield-check"),
                                              ("Ouvert", "API documentées et connecteurs standards.", "code"),
                                              ("Humain", "Un accompagnement dédié dès le premier jour.",
                                               "heart-handshake")]})

    def equip(i):
        return ("equipment-scene", {"title": "Des outils connectés entre eux"})

    def marketing(i):
        return ("marketing-funnel-cards", {"title": "Performance de la campagne"})

    def channels(i):
        return ("marketing-channel-score", {"title": "Où investir en priorité"})

    def corporate(i):
        return ("corporate-pillars", {"title": "Quatre piliers de notre modèle",
                                      "base": f"Une exécution alignée sur un seul objectif : {S_['kicker'].lower()}"})

    def timeline_cards(i):
        return ("corporate-timeline-cards", {"title": "Notre trajectoire"})

    def canvas(i):
        return ("business-model-canvas", {"title": "Business model canvas"})

    def org(i):
        return ("corporate-structure", {"title": "Une équipe, quatre pôles"})

    def layers(i):
        return ("scheme-layers", {"title": "Trois couches, un produit",
                                  "items": [(items[0][0], items[0][1], "A"),
                                            (items[1][0], items[1][1], "B"),
                                            (items[2][0], items[2][1], "C")]})

    def arrows(i):
        return ("arrow-steps", {"title": "Cinq niveaux de maturité"})

    def dark(i):
        return ("dark-infographic", {"title": "Dans le bruit, un signal clair"})

    def darkkpi(i):
        return ("dark-kpi", {"title": "Les six indicateurs du comité"})

    def glow(i):
        return ("dark-glow-chart", {"title": "Une accélération visible"})

    def iso(i):
        return ("isometric-stack", {"title": "Une plateforme en couches",
                                    "layers": [(items[3][0], "A"), (items[2][0], "B"),
                                               (items[1][0], "C"), (items[0][0], "D")]})

    def isocity(i):
        return ("isometric-city", {"title": "Un écosystème connecté"})

    def isoflow(i):
        return ("isometric-flow", {"title": "Du signal à la décision"})

    def neo(i):
        return ("neomorphic-cards", {"title": "Un design doux et tactile",
                                     "items": [("Clarté", "layers", "Une hiérarchie visuelle évidente."),
                                               ("Douceur", "feather", "Des formes sans agressivité."),
                                               ("Profondeur", "box", "Des volumes subtilement suggérés.")]})

    def neodash(i):
        return ("neomorphic-dashboard", {"title": "Tableau de bord apaisé"})

    def handmade(i):
        return ("handmade-sketch", {"title": "Le concept, à main levée"})

    def notes(i):
        return ("handmade-notes", {"title": "Idées sorties de l'atelier",
                                   "items": [(items[0][0], items[0][1]),
                                             (items[1][0], items[1][1]),
                                             (items[2][0], items[2][1]),
                                             (items[3][0], items[3][1])]})

    def quote(i):
        t = CD.TESTIMONIALS[i % 3]
        return ("testimonial-quote", {"quote": t[0].strip("« »"), "name": t[1], "role": t[2]})

    def quotes(i):
        return ("testimonial-grid", {"title": "Ce qu'ils en disent"})

    def team(i):
        return ("team-grid", {"title": "Les visages du projet"})

    def teamf(i):
        return ("team-feature", {"title": "Mot de la direction"})

    def values(i):
        return ("values-grid", {"title": "Nos six valeurs"})

    def mission(i):
        return ("mission-vision", {"title": "Mission, vision, valeurs"})

    def progress(i):
        return ("progress-list", {"title": "État des chantiers prioritaires",
                                  "items": [(items[j][0], [0.92, 0.74, 0.61, 0.45][j]) for j in range(4)]})

    def waterfall(i):
        return ("chart-waterfall", {"title": f"Décomposition de la marge — {lab}"})

    def radar(i):
        return ("chart-radar", {"title": f"Maturité — {lab}",
                                "categories": [items[0][0][:11], items[1][0][:11],
                                               items[2][0][:11], items[3][0][:11],
                                               "Équipe", "Finance"][:6]})

    def stacked(i):
        return ("chart-stacked", {"title": f"Répartition du chiffre d'affaires — {lab}",
                                  "labels": S_.get("years", [])})

    def heatmap(i):
        return ("chart-heatmap", {"title": "Activité par mois et par canal"})

    def pie(i):
        return ("chart-pie", {"title": f"Répartition des investissements — {lab}",
                              "items": [(items[0][0], 38, "A"), (items[1][0], 26, "B"),
                                        (items[2][0], 22, "C"), (items[3][0], 14, "D")],
                              "center": "12,4 M€"})

    def barsh(i):
        regs = S_.get("regions", [])
        return ("chart-bar-h", {"title": "Parts de marché par région",
                                "items": [(regs[j], [82, 68, 54, 39, 27][j]) for j in range(len(regs))]})

    def multiline(i):
        return ("chart-line-multi", {"title": "Trois scénarios de croissance"})

    def compare(i):
        return ("comparison-2", {"title": "Avant / après"})

    def illustr(i):
        return ("illustration-abstract", {"title": "Une idée, mille déclinaisons",
                                          "subtitle": "Chaque slide peut être recomposée, recolorée "
                                                      "et adaptée à votre marque.",
                                          "icon": _icon(S_, i), "kicker": "Concept"})

    def illustrs(i):
        return ("illustrations-set", {"title": "Six illustrations prêtes à l'emploi"})

    def neo2(i):
        return ("neomorphic-cards", {"title": "Des cartes douces et modulaires"})

    def portfolio(i):
        return ("portfolio-grid", {"title": "Une sélection de projets"})

    def case(i):
        return ("portfolio-case", {"title": S_["title"], "client": "Groupe Altura",
                                   "icon": _icon(S_, i, 2)})

    def masonry(i):
        return ("portfolio-masonry", {"title": "Nos derniers travaux"})

    def banner(i):
        return ("banner-set", {"title": "Cinq bannières prêtes à l'emploi"})

    def geo(i):
        return ("shape-geometry", {"title": "Composer avec les formes"})

    def symbols(i):
        return ("symbols-signs", {"title": "Signes et repères visuels"})

    def abstract1(i):
        return ("abstract-layout-1", {"title": "Une mise en page audacieuse",
                                      "icon": _icon(S_, i), "kicker": S_["kicker"]})

    def abstract2(i):
        return ("abstract-layout-2", {"title": "Des courbes, des idées",
                                      "kicker": S_["kicker"]})

    def desk(i):
        return ("scene-desk", {"title": "Un environnement de travail repensé"})

    def flags(i):
        return ("flags-grid", {"title": "Nos marchés en un regard"})

    def maps(i):
        return ("map-world-dots", {"title": "Où nous sommes présents",
                                   "subtitle": "Une présence locale, une exigence globale."})

    def social(i):
        return ("social-icons", {"title": "Notre présence sociale"})

    def post(i):
        return ("social-post-mock", {"title": "Nos formats sociaux", "icon": _icon(S_, i)})

    packs = [
        # ---------- ouverture
        cover, agenda, about, mission, kpi, big,
        # ---------- sections & contenus
        ("BREAK", "Contexte", "Où nous en sommes et ce qui change"),
        swot, swot2, seven_s, seven_s2, compare,
        ("BREAK", "Stratégie", "Le cap, les priorités et les arbitrages"),
        process, chevron, cards, timeline, timeline_v, timeline_c, timeline_cards, arrows,
        ("BREAK", "Exécution", "Ce que nous faisons concrètement"),
        cycle, rings, ring_progress, circular, funnel, sales, scene, pyramid, maslow,
        ("BREAK", "Performance", "Ce que nous mesurons"),
        chart_line, multiline, chart_bar, barsh, stacked, donut, pie, gauge, waterfall, radar,
        table, progress, heatmap, darkkpi, glow, dark, kpi,
        ("BREAK", "Marché & clients", "Ce que nos clients attendent"),
        marketing, channels, quotes, quote, values, team, teamf,
        ("BREAK", "Marque & design", "L'expression de notre identité"),
        neo, neo2, neodash, handmade, notes, iso, isocity, isoflow,
        icons, features, illustr, illustrs, equip, org, layers, canvas, corporate, big,
        ("BREAK", "Portfolio & réalisations", "Des preuves, pas des promesses"),
        portfolio, case, masonry, banner, geo, symbols, abstract1, abstract2, desk, flags, maps,
        ("BREAK", "Aller plus loin", "Ce que nous proposons ensuite"),
    ]

    out = []
    for rec in packs:
        if isinstance(rec, tuple) and rec[0] == "BREAK":
            out.append(("SECTION", {"title": rec[1], "subtitle": rec[2]}, rec[1]))
        else:
            out.append((rec, None, None))
    return out
