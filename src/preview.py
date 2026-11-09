"""Aperçu rapide d'un layout en PNG (contrôle qualité visuel)."""
from __future__ import annotations

import sys

import emit_svg
import theme
from ir import rect, Fill
from layouts import _base as B


def preview(key: str, content: dict, palette="midnight", out="/tmp/prev.png",
            width=1400, variant=0, ctx=None):
    p = theme.PALETTES[palette]
    fn = B.get(key)
    ctx = ctx or {"page": 1, "total": 12, "section": "Section"}
    nodes = fn(p, content, ctx)
    svg = emit_svg.render_svg(nodes, theme.W, theme.H, p["bg"])
    emit_svg.svg_to_png(svg, out, width=width)
    return out


if __name__ == "__main__":
    import json
    key = sys.argv[1]
    content = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
    pal = sys.argv[3] if len(sys.argv) > 3 else "midnight"
    preview(key, content, pal)
    print("ok")
