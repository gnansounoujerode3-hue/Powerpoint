"""Contrat commun des layouts.

Un layout est une fonction :  fn(p, c, ctx) -> list[Node]
  p    : palette (dict de couleurs)
  c    : contenu du slide (dict)
  ctx  : contexte global (page, total, titre de section, etc.)
"""
from __future__ import annotations

import functools

from ir import *          # noqa: F401,F403
from ir import Text, Rect, Ellipse, Poly, Arc, Line, Icon, Group, Run, Fill, Stroke, Shadow, Glow
import components as K   # noqa: F401
import iconlib
from theme import *      # noqa: F401,F403

import theme as TH
import components as B

# Chaque layout déclare : (nom lisible, catégorie, fonction)
REGISTRY: dict[str, dict] = {}


def layout(key: str, name: str, category: str, anim="fade", min_items=0):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(p, c, ctx, _fn=fn, _anim=anim):
            ctx.setdefault("accent", p["accent"])
            ctx.setdefault("kicker", "")
            nodes = _fn(p, c, ctx)
            return nodes
        REGISTRY[key] = {"key": key, "name": name, "category": category,
                         "fn": wrapper, "anim": anim, "min_items": min_items}
        return wrapper
    return deco


def get(key: str):
    return REGISTRY[key]["fn"]


def all_layouts():
    return REGISTRY


def cnt(c, key, default=None):
    v = c.get(key)
    return default if v is None else v


def items(c, key="items", n=4):
    v = c.get(key) or []
    return v[:n]


def bg(p, variant=0, dark=None):
    if dark is None:
        dark = K._lum(p["bg"]) < 0.5
    return K.background(p, variant) if dark else K.soft_background(p, variant)
