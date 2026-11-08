"""Rendu SVG d'une scène (aperçus fidèles du site web)."""
from __future__ import annotations

import html
import math

from design_system import W, H
from media import data_uri
from scene import Ellipse, Line, Picture, Rect, Scene, Text, Triangle, fit_font


def _esc(value: str) -> str:
    return html.escape(value, quote=True)


def _is_gradient(v) -> bool:
    return isinstance(v, dict) and "stops" in v


class SvgRenderer:
    def __init__(self, t: dict):
        self.t = t
        self.defs: list[str] = []
        self.gid = 0
        self.clip_id = 0

    def paint(self, fill, opacity: float = 1) -> str:
        if fill is None:
            return "none"
        if _is_gradient(fill):
            return f"url(#{self._gradient(fill, opacity)})"
        return _esc(fill)

    def _gradient(self, grad: dict, opacity: float) -> str:
        gid = f"grad{self.gid}"
        self.gid += 1
        angle = math.radians(grad.get("angle", 0))
        dx, dy = math.cos(angle), math.sin(angle)
        x1, y1 = 0.5 - dx / 2, 0.5 - dy / 2
        x2, y2 = 0.5 + dx / 2, 0.5 + dy / 2
        stops = "".join(
            f'<stop offset="{pos:.3f}" stop-color="{_esc(color)}" stop-opacity="{opacity:.3f}"/>'
            for pos, color in grad["stops"] if color
        )
        self.defs.append(
            f'<linearGradient id="{gid}" x1="{x1:.4f}" y1="{y1:.4f}" '
            f'x2="{x2:.4f}" y2="{y2:.4f}">{stops}</linearGradient>'
        )
        return gid

    @staticmethod
    def _rot(el, rotate: float, cx: float, cy: float) -> str:
        return f' transform="rotate({rotate} {cx:.2f} {cy:.2f})"' if rotate else ""

    def element(self, el) -> str:
        op = getattr(el, "opacity", 1)
        fo = f' fill-opacity="{op:.3f}"' if op < 1 else ""
        so = f' stroke-opacity="{op:.3f}"' if op < 1 else ""
        fill = self.paint(getattr(el, "fill", None), op)
        stroke = getattr(el, "stroke", None)
        stroke_attr = f' stroke="{_esc(stroke)}"' if stroke else ""
        if stroke:
            stroke_attr += f' stroke-width="{getattr(el, "sw", 1):.2f}"' + so
        if isinstance(el, Rect):
            rx = min(el.radius, el.w / 2, el.h / 2) if el.radius else 0
            return (f'<rect x="{el.x:.2f}" y="{el.y:.2f}" width="{el.w:.2f}" '
                    f'height="{el.h:.2f}" rx="{rx:.2f}" fill="{fill}"{fo}'
                    f'{stroke_attr}{self._rot(el, el.rotate, el.x + el.w / 2, el.y + el.h / 2)}/>')
        if isinstance(el, Ellipse):
            cx, cy = el.x + el.w / 2, el.y + el.h / 2
            return (f'<ellipse cx="{cx:.2f}" cy="{cy:.2f}" rx="{el.w / 2:.2f}" '
                    f'ry="{el.h / 2:.2f}" fill="{fill}"{fo}{stroke_attr}'
                    f'{self._rot(el, el.rotate, cx, cy)}/>')
        if isinstance(el, Triangle):
            pts = f"{el.x + el.w / 2:.2f},{el.y:.2f} {el.x:.2f},{el.y + el.h:.2f} " \
                  f"{el.x + el.w:.2f},{el.y + el.h:.2f}"
            return (f'<polygon points="{pts}" fill="{fill}"{fo}'
                    f'{self._rot(el, el.rotate, el.x + el.w / 2, el.y + el.h / 2)}/>')
        if isinstance(el, Line):
            dash = ' stroke-dasharray="8 6"' if el.dash else ""
            return (f'<line x1="{el.x1:.2f}" y1="{el.y1:.2f}" x2="{el.x2:.2f}" '
                    f'y2="{el.y2:.2f}" stroke="{_esc(el.stroke)}" '
                    f'stroke-width="{el.sw:.2f}" stroke-opacity="{el.opacity:.3f}"{dash}/>')
        if isinstance(el, Picture):
            return self._picture(el)
        if isinstance(el, Text):
            return self._text(el)
        return ""

    def _picture(self, el: Picture) -> str:
        href = data_uri(el.key)
        clip_attr = ""
        if el.clip in ("circle", "round"):
            cid = f"clip{self.clip_id}"
            self.clip_id += 1
            if el.clip == "circle":
                cx, cy = el.x + el.w / 2, el.y + el.h / 2
                self.defs.append(
                    f'<clipPath id="{cid}"><ellipse cx="{cx:.2f}" cy="{cy:.2f}" '
                    f'rx="{el.w / 2:.2f}" ry="{el.h / 2:.2f}"/></clipPath>')
            else:
                rx = min(el.radius, el.w / 2, el.h / 2)
                self.defs.append(
                    f'<clipPath id="{cid}"><rect x="{el.x:.2f}" y="{el.y:.2f}" '
                    f'width="{el.w:.2f}" height="{el.h:.2f}" rx="{rx:.2f}"/></clipPath>')
            clip_attr = f' clip-path="url(#{cid})"'
        op = f' opacity="{el.opacity:.3f}"' if el.opacity < 1 else ""
        return (f'<image x="{el.x:.2f}" y="{el.y:.2f}" width="{el.w:.2f}" '
                f'height="{el.h:.2f}" href="{href}" '
                f'preserveAspectRatio="xMidYMid slice"{clip_attr}{op}/>')

    def _text(self, el: Text) -> str:
        lines = el.text.split("\n")
        if el.upper:
            lines = [line.upper() for line in lines]
        lh = el.size * el.leading
        block = len(lines) * lh
        if el.valign == "middle":
            top = el.y + max(0, (el.h - block) / 2)
        elif el.valign == "bottom":
            top = el.y + max(0, el.h - block)
        else:
            top = el.y
        anchor = {"left": "start", "center": "middle", "right": "end"}[el.align]
        tx = {"left": el.x, "center": el.x + el.w / 2, "right": el.x + el.w}[el.align]
        baseline = top + el.size * 0.80
        family = fit_font(self.t, el.font, svg=True)
        weight = ' font-weight="700"' if el.bold else ""
        style = ' font-style="italic"' if el.italic else ""
        spacing = f' letter-spacing="{el.tracking:.2f}"' if el.tracking else ""
        tspans = "".join(
            f'<tspan x="{tx:.2f}" dy="{0 if i == 0 else lh:.2f}">{_esc(line)}</tspan>'
            for i, line in enumerate(lines)
        )
        return (f'<text x="{tx:.2f}" y="{baseline:.2f}" font-family="{_esc(family)}" '
                f'font-size="{el.size:.2f}" fill="{_esc(el.color)}" '
                f'fill-opacity="{el.opacity:.3f}" text-anchor="{anchor}"'
                f'{weight}{style}{spacing}>{tspans}</text>')

    def render(self, scene: Scene) -> str:
        self.defs, self.gid, self.clip_id = [], 0, 0
        bg = (f'<rect width="{W}" height="{H}" fill="url(#bg0)"/>'
              if _is_gradient(scene.bg) else
              f'<rect width="{W}" height="{H}" fill="{_esc(scene.bg)}"/>')
        if _is_gradient(scene.bg):
            # réserve l'id bg0 pour le fond
            self.gid = 1
            self.defs.append('<linearGradient id="bg0" '
                             + self._gradient_angle(scene.bg) + '>'
                             + "".join(f'<stop offset="{p:.3f}" stop-color="{_esc(c)}"/>'
                                       for p, c in scene.bg["stops"] if c)
                             + "</linearGradient>")
        body = "".join(self.element(el) for el in scene.elements)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
                f'width="{W}" height="{H}" role="img" aria-label="{_esc(scene.title)}">'
                f'<defs>{"".join(self.defs)}</defs>{bg}{body}</svg>')

    @staticmethod
    def _gradient_angle(grad: dict) -> str:
        angle = math.radians(grad.get("angle", 0))
        dx, dy = math.cos(angle), math.sin(angle)
        return (f'x1="{0.5 - dx / 2:.4f}" y1="{0.5 - dy / 2:.4f}" '
                f'x2="{0.5 + dx / 2:.4f}" y2="{0.5 + dy / 2:.4f}"')


def render_svg(scene: Scene, t: dict) -> str:
    return SvgRenderer(t).render(scene)
