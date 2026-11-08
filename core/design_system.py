"""Système de design du pack 1500.

30 univers graphiques × 50 palettes = 1 500 modèles uniques.
Tout est déterministe : un même identifiant produit toujours exactement le même design.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

W, H = 1333, 750  # unités de scène : 1 unité = 0,01 pouce (16:9)

ROOT = Path(__file__).resolve().parent.parent
CATALOG_DIR = ROOT / "catalog"


# ---------------------------------------------------------------------------
# Couleurs
# ---------------------------------------------------------------------------
def rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def hexcolor(c: tuple[int, int, int]) -> str:
    return "#{:02X}{:02X}{:02X}".format(*[max(0, min(255, round(v))) for v in c])


def mix(a: str, b: str, t: float) -> str:
    ca, cb = rgb(a), rgb(b)
    return hexcolor(tuple(ca[i] * (1 - t) + cb[i] * t for i in range(3)))


def lighten(c: str, t: float) -> str:
    return mix(c, "#FFFFFF", t)


def darken(c: str, t: float) -> str:
    return mix(c, "#000000", t)


def luminance(c: str) -> float:
    def channel(v: int) -> float:
        v /= 255
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(v) for v in rgb(c))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def on_color(c: str) -> str:
    """Texte lisible posé sur une couleur pleine."""
    return "#10131A" if luminance(c) > 0.45 else "#FFFFFF"


# 25 histoires chromatiques × 2 modes (clair / nuit) = 50 palettes
# (nom, accent, accent secondaire, fond clair, fond nuit)
STORIES = [
    ("Cobalt", "#2563EB", "#60A5FA", "#F4F7FF", "#0A1024"),
    ("Outremer", "#1E3A8A", "#5B8DEF", "#F2F5FC", "#080F22"),
    ("Cyan", "#0891B2", "#22D3EE", "#F0FAFC", "#04141A"),
    ("Turquoise", "#0D9488", "#5EEAD4", "#F0FBF8", "#071A17"),
    ("Émeraude", "#059669", "#34D399", "#F1FBF6", "#061A12"),
    ("Sauge", "#4B7F52", "#A7C4A0", "#F5F8F1", "#101A12"),
    ("Olive", "#65723B", "#C2D16B", "#F8F8EE", "#161A0E"),
    ("Soleil", "#C9970B", "#FDE047", "#FFFBEA", "#1C1704"),
    ("Ambre", "#D97706", "#FBBF24", "#FFF8ED", "#1F1305"),
    ("Corail", "#E2624A", "#FDAF9B", "#FFF5F1", "#1E0D09"),
    ("Rubis", "#C62828", "#F87171", "#FFF4F3", "#1B0909"),
    ("Bordeaux", "#8B1E3F", "#D4547C", "#FCF3F6", "#190810"),
    ("Rose Poudré", "#C72E6D", "#F9A8D4", "#FEF5FA", "#1C0A15"),
    ("Violet", "#6D34D9", "#A78BFA", "#F7F4FF", "#120A24"),
    ("Indigo", "#4338CA", "#818CF8", "#F5F5FF", "#0B0B22"),
    ("Lavande", "#7A6BCB", "#C4B5FD", "#F8F7FE", "#121026"),
    ("Ardoise", "#334155", "#94A3B8", "#F5F7FA", "#0E131B"),
    ("Graphite", "#1F2937", "#8A94A6", "#F7F7F6", "#0B0D10"),
    ("Sable", "#A97C4E", "#E3C49B", "#FBF7F0", "#17120B"),
    ("Terracotta", "#BC573B", "#E8A487", "#FDF4EF", "#1B0E08"),
    ("Menthe", "#2F9E8F", "#9FE3D6", "#F0FAF8", "#071816"),
    ("Azur", "#0284C7", "#7DD3FC", "#F1F9FE", "#05131E"),
    ("Framboise", "#BE185D", "#F472B6", "#FDF3F8", "#1B0712"),
    ("Citron Vert", "#5D9713", "#BEF264", "#F7FBEC", "#101705"),
    ("Océan", "#0E7490", "#38BDF8", "#F0F9FC", "#04121A"),
]


def _build_palettes() -> list[dict]:
    out: list[dict] = []
    for i, (name, accent, accent2, light_bg, dark_bg) in enumerate(STORIES):
        for j, mode in enumerate(("light", "dark")):
            if mode == "light":
                bg, surface, ink = light_bg, "#FFFFFF", "#121722"
                acc, acc2 = accent, accent2
                muted, line = mix(ink, bg, 0.52), mix(bg, ink, 0.11)
                label = f"{name} Clair"
            else:
                bg, surface, ink = dark_bg, mix(dark_bg, "#FFFFFF", 0.07), "#F6F8FC"
                acc, acc2 = lighten(accent, 0.24), lighten(accent2, 0.16)
                muted, line = mix(ink, bg, 0.45), mix(bg, ink, 0.15)
                label = f"{name} Nuit"
            out.append(
                {
                    "id": f"P{i * 2 + j + 1:02d}",
                    "name": label,
                    "hue": name,
                    "mode": mode,
                    "bg": bg,
                    "surface": surface,
                    "ink": ink,
                    "muted": muted,
                    "line": line,
                    "accent": acc,
                    "accent2": acc2,
                    "on_accent": on_color(acc),
                    "soft": mix(bg, acc, 0.12 if mode == "light" else 0.18),
                    "panel": mix(surface, acc, 0.06 if mode == "light" else 0.10),
                }
            )
    return out


PALETTES = _build_palettes()


# ---------------------------------------------------------------------------
# Typographies (polices présentes dans PowerPoint / Office)
# ---------------------------------------------------------------------------
FONTS = {
    "suisse": {"label": "Suisse", "heading": "Arial", "body": "Arial",
               "svg_heading": "Arial, Helvetica, sans-serif", "svg_body": "Arial, Helvetica, sans-serif"},
    "editorial": {"label": "Éditorial", "heading": "Georgia", "body": "Arial",
                  "svg_heading": "Georgia, 'Times New Roman', serif", "svg_body": "Arial, Helvetica, sans-serif"},
    "modern": {"label": "Moderne", "heading": "Aptos Display", "body": "Calibri",
               "svg_heading": "'Helvetica Neue', Arial, sans-serif", "svg_body": "Arial, Helvetica, sans-serif"},
    "mono": {"label": "Technique", "heading": "Consolas", "body": "Calibri",
             "svg_heading": "'Courier New', monospace", "svg_body": "Arial, Helvetica, sans-serif"},
    "serif": {"label": "Sérif", "heading": "Georgia", "body": "Georgia",
              "svg_heading": "Georgia, 'Times New Roman', serif", "svg_body": "Georgia, serif"},
    "soft": {"label": "Ronde", "heading": "Trebuchet MS", "body": "Trebuchet MS",
             "svg_heading": "'Trebuchet MS', Verdana, sans-serif", "svg_body": "'Trebuchet MS', Verdana, sans-serif"},
    "display": {"label": "Affiche", "heading": "Arial Black", "body": "Arial",
                "svg_heading": "'Arial Black', Impact, sans-serif", "svg_body": "Arial, Helvetica, sans-serif"},
    "classic": {"label": "Classique", "heading": "Cambria", "body": "Calibri",
                "svg_heading": "Cambria, Georgia, serif", "svg_body": "Arial, Helvetica, sans-serif"},
}


# ---------------------------------------------------------------------------
# 30 familles de mise en page
# ---------------------------------------------------------------------------
# archetype : centred / split / frame / fullbleed / sidebar / grid / asymmetric /
#             editorial / stacked / diagonal
# motif     : lignes, barres, grille, blobs, cercles, points, blocs, ondes,
#             triangles, arcs
_FAMILY_ROWS = [
    # (nom, univers, archetype, motif, typo, rayon, densité, description)
    ("Suisse Minimal", "Business", "centred", "lines", "suisse", 0, "low",
     "Grille suisse, grands blancs, hiérarchie radicale."),
    ("Atlantic Corporate", "Business", "split", "bars", "modern", 8, "medium",
     "Le classique des comités de direction, net et rassurant."),
    ("Executive Frame", "Business", "frame", "lines", "classic", 0, "low",
     "Cadre fin, sérifs sobres, élégance institutionnelle."),
    ("Néon Startup", "Tech", "fullbleed", "blobs", "modern", 26, "medium",
     "Dégradés vibrants et typographie XXL pour pitcher."),
    ("Code Grid", "Tech", "grid", "grid", "mono", 4, "high",
     "Trame technique, repères chiffrés, esprit produit."),
    ("Orbite Spatiale", "Tech", "asymmetric", "circles", "display", 40, "low",
     "Cercles orbitaux et composition décentrée."),
    ("Data Room", "Finance", "sidebar", "bars", "modern", 6, "high",
     "Dense en données, pensée pour les revues chiffrées."),
    ("Précision Finance", "Finance", "split", "grid", "editorial", 0, "medium",
     "Sérifs, colonnes et rigueur de reporting."),
    ("Tableau de Bord", "Finance", "grid", "blocks", "suisse", 12, "high",
     "Modules KPI empilés, lecture instantanée."),
    ("Éditorial Bold", "Créatif", "editorial", "blocks", "editorial", 0, "medium",
     "Titres magazine, contrastes francs, photo-emplacement."),
    ("Atelier Pastel", "Créatif", "centred", "blobs", "soft", 30, "low",
     "Formes douces et couleurs tendres pour studios."),
    ("Studio Pop", "Créatif", "asymmetric", "dots", "display", 16, "high",
     "Énergie pop, trames de points, audace assumée."),
    ("Campus Clair", "Éducation", "sidebar", "circles", "soft", 20, "low",
     "Pédagogique, aéré, très lisible en amphithéâtre."),
    ("Cahier Notes", "Éducation", "frame", "lines", "soft", 12, "medium",
     "Lignes de cahier et annotation, esprit cours."),
    ("Science Lab", "Éducation", "grid", "dots", "mono", 8, "medium",
     "Trame scientifique, schémas et légendes."),
    ("Clinique Pure", "Santé", "centred", "waves", "modern", 28, "low",
     "Blanc, calme et courbes rassurantes."),
    ("Vitalité", "Santé", "split", "arcs", "soft", 24, "medium",
     "Arcs dynamiques, tonus et bien-être."),
    ("Care & Calme", "Santé", "stacked", "blobs", "soft", 40, "low",
     "Bandes douces, respiration maximale."),
    ("Noir & Or", "Luxe", "fullbleed", "lines", "serif", 0, "low",
     "Fond profond, filets dorés, sobriété absolue."),
    ("Maison Couture", "Luxe", "editorial", "lines", "serif", 0, "low",
     "Éditorial de mode, lettrage ample, raffinement."),
    ("Velours", "Luxe", "asymmetric", "circles", "classic", 0, "medium",
     "Composition décentrée, tons profonds."),
    ("Campagne 360", "Marketing", "split", "triangles", "display", 16, "medium",
     "Flèches, impact et appels à l'action."),
    ("Social Pulse", "Marketing", "grid", "dots", "modern", 28, "high",
     "Rythme de réseaux sociaux, vignettes modulaires."),
    ("Brand Book", "Marketing", "frame", "blocks", "editorial", 0, "medium",
     "Charte graphique, nuances et règles d'usage."),
    ("Terre Organique", "Écologie", "fullbleed", "waves", "soft", 32, "low",
     "Ondes naturelles, matières et engagement."),
    ("Vert Forêt", "Écologie", "sidebar", "lines", "classic", 16, "medium",
     "Colonne latérale, tons bois et verdure."),
    ("Impact Positif", "Écologie", "centred", "circles", "suisse", 24, "low",
     "Cercles concentriques, message central."),
    ("Béton Brut", "Architecture", "editorial", "blocks", "display", 0, "medium",
     "Blocs massifs, brutalisme maîtrisé."),
    ("Plan Technique", "Architecture", "grid", "grid", "mono", 0, "high",
     "Plan coté, trame millimétrée, précision."),
    ("Horizon Moderne", "Architecture", "diagonal", "bars", "modern", 12, "low",
     "Bande diagonale, lignes d'horizon, modernité."),
]

FAMILIES = []
for i, (name, univers, archetype, motif, typo, radius, density, desc) in enumerate(_FAMILY_ROWS):
    FAMILIES.append({
        "id": f"F{i + 1:02d}",
        "name": name,
        "univers": univers,
        "archetype": archetype,
        "motif": motif,
        "typo": typo,
        "typo_label": FONTS[typo]["label"],
        "radius": radius,
        "density": density,
        "description": desc,
    })


HEADLINES = [
    "Donnez une forme à vos idées",
    "La clarté change tout",
    "Une vision qui se voit",
    "Racontez ce qui compte",
    "Des idées qui prennent de l'ampleur",
    "Le fond mérite une forme",
    "Présentez avec conviction",
    "Simplifiez l'essentiel",
    "Du sens, du rythme, de l'impact",
    "Faites passer le message",
    "Construisons la suite ensemble",
    "L'élégance au service du propos",
]

SUBTITLES = [
    "Un modèle de présentation premium, entièrement modifiable",
    "Stratégie · Design · Résultats — édition 2026",
    "Support de présentation professionnel, 100 % éditable",
    "Votre marque, votre voix, votre histoire",
]


def _digest(*parts: object) -> int:
    return int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:8], 16)


def _build_templates() -> list[dict]:
    out: list[dict] = []
    n = 0
    # boucle palette-major : les premières pages affichent les 30 familles
    for pi, palette in enumerate(PALETTES):
        for fi, family in enumerate(FAMILIES):
            n += 1
            d = _digest(n, family["name"], palette["name"])
            out.append({
                "id": f"T{n:04d}",
                "number": n,
                "name": f"{family['name']} · {palette['name']}",
                "family_id": family["id"],
                "family": family["name"],
                "palette_id": palette["id"],
                "palette": palette["name"],
                "univers": family["univers"],
                "mode": palette["mode"],
                "hue": palette["hue"],
                "archetype": family["archetype"],
                "motif": family["motif"],
                "typo": family["typo"],
                "typo_label": family["typo_label"],
                "radius": family["radius"],
                "density": family["density"],
                "description": family["description"],
                "headline": HEADLINES[(fi + pi) % len(HEADLINES)],
                "subtitle": SUBTITLES[(fi * 3 + pi) % len(SUBTITLES)],
                "popularity": 70 + d % 30,
                "colors": {k: palette[k] for k in (
                    "bg", "surface", "ink", "muted", "line", "accent", "accent2", "soft", "panel", "on_accent")},
                "search": " ".join([
                    f"T{n:04d}", str(n), family["name"].lower(), palette["name"].lower(),
                    family["univers"].lower(), family["motif"], family["typo_label"].lower(),
                    palette["mode"], palette["hue"].lower(), "powerpoint", "pptx", "template",
                    "modèle", "présentation", "slide", "design",
                ]),
            })
    return out


TEMPLATES = _build_templates()
BY_ID = {t["id"]: t for t in TEMPLATES}

UNIVERS = sorted({f["univers"] for f in FAMILIES})
MOTIFS = sorted({f["motif"] for f in FAMILIES})
ARCHETYPES = sorted({f["archetype"] for f in FAMILIES})
TYPOS = [FONTS[k]["label"] for k in FONTS]
HUES = [s[0] for s in STORIES]


def get_template(identifier: str | int) -> dict:
    if isinstance(identifier, int):
        identifier = f"T{identifier:04d}"
    key = str(identifier).upper()
    if key.isdigit():
        key = f"T{int(key):04d}"
    if key not in BY_ID:
        raise KeyError(f"Modèle inconnu : {identifier}")
    return BY_ID[key]


def family_of(t: dict) -> dict:
    return next(f for f in FAMILIES if f["id"] == t["family_id"])


def slugify(text: str) -> str:
    import re
    import unicodedata
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()


def filename_for(t: dict) -> str:
    return f"{t['id']}-{slugify(t['family'])}-{slugify(t['palette'])}.pptx"


def build_catalog_files() -> None:
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "meta": {
            "name": "Pack 1500 — Templates PowerPoint Premium",
            "total": len(TEMPLATES),
            "slides_per_template": 10,
            "total_slides": len(TEMPLATES) * 10,
            "families": len(FAMILIES),
            "palettes": len(PALETTES),
            "images_per_template": 4,
            "animations": "Transitions natives + apparitions en fondu séquencées",
            "unique_designs": len(TEMPLATES) * 10,
            "design_dimensions": 8,
            "features": ["design unique par slide", "animations", "images remplaçables",
                         "notes de présentation"],
            "univers": UNIVERS,
            "motifs": MOTIFS,
            "archetypes": ARCHETYPES,
            "typos": TYPOS,
            "hues": HUES,
            "fonts": FONTS,
            "format": "16:9 (13,33 × 7,5 pouces)",
            "version": "1.0.0",
        },
        "families": FAMILIES,
        "palettes": PALETTES,
        "templates": TEMPLATES,
    }
    (CATALOG_DIR / "templates.json").write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    with (CATALOG_DIR / "templates.csv").open("w", encoding="utf-8-sig", newline="") as fh:
        import csv
        writer = csv.writer(fh)
        writer.writerow(["ID", "Nom", "Famille", "Palette", "Univers", "Mode", "Motif", "Typographie", "Fichier"])
        for t in TEMPLATES:
            writer.writerow([t["id"], t["name"], t["family"], t["palette"], t["univers"],
                             t["mode"], t["motif"], t["typo_label"], filename_for(t)])
    print(f"Catalogue : {len(TEMPLATES)} modèles, {len(FAMILIES)} familles, {len(PALETTES)} palettes")


if __name__ == "__main__":
    build_catalog_files()
