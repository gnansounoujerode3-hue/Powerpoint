"""Visuels de substitution intégrés aux modèles.

Ce sont de VRAIES images (JPEG/PNG) insérées comme objets image PowerPoint :
l'utilisateur fait un clic droit > « Modifier l'image » pour mettre la sienne.

Générées par code à partir de la palette du modèle, donc :
  · aucune dépendance réseau, aucun copyright,
  · cohérence chromatique parfaite avec le reste du slide,
  · 300 visuels uniques (50 palettes × 3 héros + 50 × 3 portraits).
"""
from __future__ import annotations

import base64
import io
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from design_system import PALETTES, ROOT, darken, lighten, mix, rgb

MEDIA_DIR = ROOT / "dist" / "media"
_BY_PALETTE = {p["id"]: p for p in PALETTES}
_CACHE: dict[str, tuple[bytes, str, tuple[int, int]]] = {}

HERO_SIZE = (640, 360)
FACE_SIZE = (240, 240)


def hero_key(t: dict) -> str:
    variant = int(t["family_id"][1:]) % 3
    return f"hero-{t['palette_id']}-{variant}.jpg"


def face_key(t: dict, index: int) -> str:
    return f"face-{t['palette_id']}-{index % 3}.png"


def _font(size: int):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _gradient(c1: str, c2: str, size: tuple[int, int], variant: int = 0) -> Image.Image:
    sw, sh = 128, 128
    small = Image.new("RGB", (sw, sh))
    px = small.load()
    a, b = rgb(c1), rgb(c2)
    for x in range(sw):
        for y in range(sh):
            if variant == 1:
                t = 0.30 * (x / (sw - 1)) + 0.70 * (y / (sh - 1))
            elif variant == 2:
                t = 0.70 * (1 - x / (sw - 1)) + 0.30 * (y / (sh - 1))
            else:
                t = 0.65 * (x / (sw - 1)) + 0.35 * (y / (sh - 1))
            px[x, y] = tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))
    return small.resize(size, Image.BICUBIC)


def _hero(p: dict, variant: int) -> bytes:
    w, h = HERO_SIZE
    if variant == 0:
        c1, c2 = lighten(p["accent"], 0.10), darken(p["accent2"], 0.40)
    elif variant == 1:
        c1, c2 = p["accent"], darken(p["accent"], 0.58)
    else:
        c1, c2 = lighten(p["accent2"], 0.10), p["accent"]

    img = _gradient(c1, c2, (w, h), variant).convert("RGBA")

    # halos flous
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((w * 0.52, -h * 0.42, w * 1.30, h * 0.88), fill=(255, 255, 255, 78))
    g.ellipse((-w * 0.28, h * 0.40, w * 0.54, h * 1.50), fill=(0, 0, 0, 48))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(46)))

    crisp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(crisp)
    if variant == 0:  # cercles concentriques
        for i in range(5):
            r = 42 + i * 34
            cx, cy = int(w * 0.72), int(h * 0.48)
            d.ellipse((cx - r, cy - r, cx + r, cy + r),
                      outline=(255, 255, 255, 105 - i * 14), width=2)
        d.ellipse((int(w * 0.72) - 16, int(h * 0.48) - 16,
                   int(w * 0.72) + 16, int(h * 0.48) + 16), fill=(255, 255, 255, 170))
    elif variant == 1:  # bandes diagonales
        for i in range(5):
            x = -w * 0.2 + i * w * 0.26
            d.polygon([(x, h), (x + w * 0.14, h), (x + w * 0.52, 0), (x + w * 0.38, 0)],
                      fill=(255, 255, 255, 26 + i * 8))
        d.line((0, h * 0.78, w, h * 0.30), fill=(255, 255, 255, 95), width=2)
    else:  # modules arrondis
        for i in range(3):
            x = int(w * 0.12 + i * w * 0.24)
            y = int(h * 0.18 + (i % 2) * h * 0.20)
            bw, bh = int(w * 0.19), int(h * 0.44)
            d.rounded_rectangle((x, y, x + bw, y + bh), radius=16,
                                fill=(255, 255, 255, 40 + i * 18),
                                outline=(255, 255, 255, 90), width=2)
        d.rounded_rectangle((w * 0.08, h * 0.82, w * 0.92, h * 0.86), radius=3,
                            fill=(255, 255, 255, 110))

    img = Image.alpha_composite(img, crisp)
    # filet discret uniquement : les consignes de remplacement sont sur le slide
    d2 = ImageDraw.Draw(img)
    d2.rectangle((6, 6, w - 7, h - 7), outline=(255, 255, 255, 70), width=2)

    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=78, optimize=True, progressive=False)
    return buf.getvalue()


def _face(p: dict, variant: int) -> bytes:
    w, h = FACE_SIZE
    base = p["surface"] if variant % 2 == 0 else p["soft"]
    img = _gradient(base, mix(base, p["accent"], 0.42), (w, h), variant).convert("RGBA")
    accent = [p["accent"], lighten(p["accent2"], 0.08), mix(p["accent"], p["accent2"], 0.5)][variant % 3]
    d = ImageDraw.Draw(img)
    # épaules
    d.ellipse((w * 0.14, h * 0.56, w * 0.86, h * 1.32), fill=(*rgb(accent), 255))
    # tête
    d.ellipse((w * 0.31, h * 0.15, w * 0.69, h * 0.57),
              fill=(*rgb(lighten(accent, 0.38 if variant == 1 else 0.18)), 255))
    # reflets et filet
    d.ellipse((w * 0.34, h * 0.18, w * 0.66, h * 0.52), outline=(255, 255, 255, 80), width=2)
    d.ellipse((5, 5, w - 6, h - 6), outline=(255, 255, 255, 135), width=4)
    d.line((w * 0.20, h - 12, w * 0.80, h - 12), fill=(255, 255, 255, 90), width=3)
    buf = io.BytesIO()
    img.convert("RGB").save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def _parse(key: str):
    m = re.fullmatch(r"(hero|face)-(P\d{2})-(\d)\.(jpg|png)", key)
    if not m:
        raise KeyError(f"Visuel inconnu : {key}")
    return m.group(1), m.group(2), int(m.group(3))


def asset(key: str) -> tuple[bytes, str, tuple[int, int]]:
    """Retourne (octets, type MIME, dimensions) — avec cache mémoire + disque."""
    if key in _CACHE:
        return _CACHE[key]
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    path = MEDIA_DIR / key
    if path.exists():
        data = path.read_bytes()
    else:
        kind, palette_id, variant = _parse(key)
        p = _BY_PALETTE[palette_id]
        data = _hero(p, variant) if kind == "hero" else _face(p, variant)
        path.write_bytes(data)
    mime = "image/jpeg" if key.endswith(".jpg") else "image/png"
    size = HERO_SIZE if key.startswith("hero") else FACE_SIZE
    _CACHE[key] = (data, mime, size)
    return _CACHE[key]


def data_uri(key: str) -> str:
    data, mime, _ = asset(key)
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"
