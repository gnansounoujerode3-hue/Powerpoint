"""Mesure et césure typographiques (Poppins) pour garantir que le texte
tient exactement dans sa boîte, comme PowerPoint le fera."""
from __future__ import annotations

import os
from functools import lru_cache

from PIL import ImageFont

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "fonts")
WEIGHTS = {False: 400, True: 700}


@lru_cache(maxsize=256)
def _font(size_px: int, bold: bool):
    path = os.path.join(FONT_DIR, f"Poppins-{WEIGHTS[bool(bold)]}.ttf")
    return ImageFont.truetype(path, max(4, int(size_px)))


def text_width(s: str, size: float, bold: bool = False, spacing: float = 0.0) -> float:
    if not s:
        return 0.0
    f = _font(int(round(size * 2)), bold)
    w = f.getlength(s) / 2.0
    return w + spacing * max(0, len(s) - 1)


def split_tokens(runs):
    """Transforme des runs en jetons (mot + espace) en conservant le style."""
    toks = []
    for r in runs:
        parts = r.text.split("\n")
        for i, part in enumerate(parts):
            if i:
                toks.append(("\n", r))
            for w in part.split(" "):
                toks.append((w, r))
    # reconstruit avec espaces : un jeton = mot, l'espace est implicite
    return toks


def wrap_runs(runs, size: float, box_w: float, bold_default=False) -> list[list[tuple[str, object]]]:
    """Retourne les lignes : list[list[(texte, run)]]."""
    lines: list[list[tuple[str, object]]] = [[]]
    cur_w = 0.0
    for tok, r in split_tokens(runs):
        if tok == "\n":
            lines.append([])
            cur_w = 0.0
            continue
        sz = (r.size or size)
        b = bool(r.bold or bold_default)
        sp = getattr(r, "spacing", 0.0) or 0.0
        w = text_width(tok, sz, b, sp)
        space_w = text_width(" ", sz, b, sp)
        need = w if not lines[-1] else space_w + w
        if lines[-1] and cur_w + need > box_w + 0.5:
            lines.append([(tok, r)])
            cur_w = w
        else:
            if lines[-1]:
                cur_w += space_w
            lines[-1].append((tok, r))
            cur_w += w
    return [ln for ln in lines]


def line_height(size: float, mult: float) -> float:
    return size * mult


def block_height(nlines: int, size: float, mult: float) -> float:
    return nlines * line_height(size, mult)


def fit_text(runs, box_w: float, box_h: float, size: float, line_mult: float,
             bold: bool = False, min_size: float = 9.0):
    """Réduit la taille jusqu'à ce que le texte tienne ; retourne (size, lignes)."""
    s = size
    while s >= min_size:
        lines = wrap_runs(runs, s, box_w, bold)
        h = block_height(len(lines), s, line_mult)
        widest = 0
        for ln in lines:
            w = 0.0
            for i, (t, r) in enumerate(ln):
                w += text_width(t, (r.size or s), bool(r.bold or bold))
                if i:
                    w += text_width(" ", (r.size or s), bool(r.bold or bold))
            widest = max(widest, w)
        if h <= box_h + 0.5 and widest <= box_w + 0.5:
            return s, lines
        s -= 1.0
    return max(min_size, s), wrap_runs(runs, max(min_size, s), box_w, bold)
