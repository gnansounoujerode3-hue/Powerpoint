"""Moteur de variation : à partir d'un layout, produit des déclinaisons
visuellement distinctes (peaux) sans dupliquer le code de design.

Une « peau » combine :
  - une permutation des trois accents (identité chromatique),
  - un style de fond (halos / mesh / anneaux / grille dense),
  - un traitement du kicker (barre / point / sans),
  - une Densité décorative différente.
"""
from __future__ import annotations

from ir import mix

# état courant (piloté par le composeur)
VARIANT = 0

SKINS = [
    {"name": "signal", "bg_style": "glow", "kicker": "bar", "perm": (0, 1, 2), "motif": "none"},
    {"name": "orbit", "bg_style": "mesh", "kicker": "dot", "perm": (1, 2, 0), "motif": "rings"},
    {"name": "grid", "bg_style": "griddense", "kicker": "none", "perm": (2, 0, 1), "motif": "dots"},
    {"name": "noir", "bg_style": "noir", "kicker": "bar", "perm": (0, 2, 1), "motif": "diag"},
    {"name": "soft", "bg_style": "soft", "kicker": "dot", "perm": (1, 0, 2), "motif": "none"},
]


def set_variant(v: int):
    global VARIANT
    VARIANT = v % len(SKINS)


def current():
    return SKINS[VARIANT % len(SKINS)]


def skin_palette(p: dict, variant: int | None = None) -> dict:
    """Retourne une palette dont les accents sont permutés selon la peau."""
    v = VARIANT if variant is None else variant
    skin = SKINS[v % len(SKINS)]
    perm = skin["perm"]
    acc = [p["accent"], p["accent2"], p["accent3"]]
    q = dict(p)
    q["accent"] = acc[perm[0]]
    q["accent2"] = acc[perm[1]]
    q["accent3"] = acc[perm[2]]
    q["glow"] = q["accent"]
    q["skin"] = skin["name"]
    return q
