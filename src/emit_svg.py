"""Backend SVG : rendu d'aperçu (PNG) d'un slide IR, pour contrôle qualité."""
from __future__ import annotations

import math
from typing import Iterable

from ir import (Arc, Ellipse, Fill, Group, Icon, Line, Poly, Rect, Stroke,
                Text, hx)

FONT_DIRS = ["/home/user/Powerpoint/assets/fonts"]


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def _grad_decl(f: Fill, gid: str) -> str:
    """Déclaration SVG <linearGradient>/<radialGradient> pour un Fill."""
    if f.stops:
        stops = "".join(
            f'<stop offset="{p*100:.1f}%" stop-color="{_hex6(hx(c))}" stop-opacity="{a:.3f}"/>'
            for p, c, a in f.stops)
        kind = "radialGradient" if f.radial else "linearGradient"
        return f'<{kind} id="{gid}">{stops}</{kind}>'
    kind = "radialGradient" if f.radial else "linearGradient"
    if f.radial:
        extra = ' cx="50%" cy="50%" r="75%"'
    else:
        a = math.radians(f.angle)
        x1, y1 = 50 - 50 * math.cos(a), 50 - 50 * math.sin(a)
        x2, y2 = 50 + 50 * math.cos(a), 50 + 50 * math.sin(a)
        extra = f' x1="{x1:.1f}%" y1="{y1:.1f}%" x2="{x2:.1f}%" y2="{y2:.1f}%"'
    return (f'<{kind} id="{gid}"{extra}>'
            f'<stop offset="0%" stop-color="{_hex6(hx(f.color))}" stop-opacity="{f.alpha:.3f}"/>'
            f'<stop offset="100%" stop-color="{_hex6(hx(f.color2))}" stop-opacity="{f.alpha:.3f}"/>'
            f'</{kind}>')


def _fill_attr(f: Fill | None, uid: str = "") -> str:
    if not f:
        return 'fill="none"'
    if f.color2 or f.stops:
        return f'fill="url(#{uid})"'
    return f'fill="{_hex6(hx(f.color))}" fill-opacity="{f.alpha:.3f}"'


def _stroke_attr(s: Stroke | None, sc: float = 1.0) -> str:
    if not s:
        return ""
    d = ""
    if s.dash == "dash":
        d = f' stroke-dasharray="{6*sc:.1f} {4*sc:.1f}"'
    elif s.dash == "dot":
        d = f' stroke-dasharray="{1.2*sc:.1f} {5*sc:.1f}"'
    elif s.dash == "sysdash":
        d = f' stroke-dasharray="{4*sc:.1f} {3*sc:.1f}"'
    cap = "round" if s.cap == "round" else "butt"
    join = "round" if s.join == "round" else "miter"
    return (f'stroke="{_hex6(hx(s.color))}" stroke-opacity="{s.alpha:.3f}" '
            f'stroke-width="{s.width:.2f}" stroke-linecap="{cap}" '
            f'stroke-linejoin="{join}"{d}')


def _catmull(pts, closed: bool) -> str:
    if len(pts) < 3:
        return "M " + " L ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in pts)
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    else:
        P = [P[0]] + P + [P[-1]]
    d = f"M {P[1][0]:.2f},{P[1][1]:.2f}"
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += (f" C {c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} "
              f"{p2[0]:.2f},{p2[1]:.2f}")
    if closed:
        d += " Z"
    return d


def _arc_path(cx, cy, r, a0, a1, inner=0.0):
    """Arc (anneau) de a0 à a1 degrés (sens horaire, 0 = est)."""
    sweep = a1 - a0
    large = 1 if abs(sweep) > 180 else 0
    def pt(a, rr):
        ra = math.radians(a)
        return cx + rr * math.cos(ra), cy + rr * math.sin(ra)
    x0, y0 = pt(a0, r)
    x1, y1 = pt(a1, r)
    if inner and inner > 0:
        ri = r * inner
        xi0, yi0 = pt(a0, ri)
        xi1, yi1 = pt(a1, ri)
        return (f"M {x0:.2f},{y0:.2f} A {r:.2f},{r:.2f} 0 {large} 1 {x1:.2f},{y1:.2f} "
                f"L {xi1:.2f},{yi1:.2f} A {ri:.2f},{ri:.2f} 0 {large} 0 {xi0:.2f},{yi0:.2f} Z")
    return f"M {x0:.2f},{y0:.2f} A {r:.2f},{r:.2f} 0 {large} 1 {x1:.2f},{y1:.2f}"


class SVGEmitter:
    def __init__(self, w: int, h: int, bg: str):
        self.w, self.h, self.bg = w, h, bg
        self.out: list[str] = []
        self.defs: list[str] = []
        self.uid = 0

    def paint(self, f: Fill | None) -> str:
        """Enregistre le dégradé éventuel et renvoie les attributs de remplissage."""
        if f and (f.color2 or f.stops):
            self.uid += 1
            gid = f"g{self.uid}"
            self.defs.append(_grad_decl(f, gid))
            return _fill_attr(f, gid)
        return _fill_attr(f)

    # -------------------------------------------------------------- nodes
    def emit(self, nodes: Iterable):
        for n in nodes:
            self.one(n)

    def one(self, n):
        o = self.out
        if isinstance(n, Rect):
            f = self.paint(n.fill)
            st = _stroke_attr(n.stroke)
            if n.radius > 0:
                o.append(f'<rect x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" '
                         f'height="{n.h:.2f}" rx="{min(n.radius, min(n.w,n.h)/2):.2f}" {f} {st}/>')
            else:
                o.append(f'<rect x="{n.x:.2f}" y="{n.y:.2f}" width="{n.w:.2f}" '
                         f'height="{n.h:.2f}" {f} {st}/>')
        elif isinstance(n, Ellipse):
            f = self.paint(n.fill)
            st = _stroke_attr(n.stroke)
            o.append(f'<ellipse cx="{n.x+n.w/2:.2f}" cy="{n.y+n.h/2:.2f}" '
                     f'rx="{n.w/2:.2f}" ry="{n.h/2:.2f}" {f} {st}/>')
        elif isinstance(n, Poly):
            if n.smooth:
                d = _catmull(n.pts, n.closed)
            else:
                d = "M " + " L ".join(f"{p[0]:.2f},{p[1]:.2f}" for p in n.pts)
                if n.closed:
                    d += " Z"
            f = self.paint(n.fill)
            st = _stroke_attr(n.stroke)
            o.append(f'<path d="{d}" {f} {st}/>')
        elif isinstance(n, Arc):
            d = _arc_path(n.cx, n.cy, n.r, n.a0, n.a1, n.inner)
            f = self.paint(n.fill)
            st = _stroke_attr(n.stroke)
            o.append(f'<path d="{d}" {f} {st}/>')
        elif isinstance(n, Line):
            st = _stroke_attr(n.stroke)
            o.append(f'<line x1="{n.x1:.2f}" y1="{n.y1:.2f}" x2="{n.x2:.2f}" '
                     f'y2="{n.y2:.2f}" {st}/>')
        elif isinstance(n, Text):
            self._text(n)
        elif isinstance(n, Icon):
            sc = n.size / 24.0
            st = _stroke_attr(n.stroke, 1.0)
            parts = "".join(f'<path d="{d}" fill="none" {st}/>' for d in n.paths)
            o.append(f'<g transform="translate({n.x:.2f},{n.y:.2f}) scale({sc:.4f})">'
                     f'{parts}</g>')
        elif isinstance(n, Group):
            o.append('<g>')
            self.emit(n.children)
            o.append('</g>')


    def _text(self, n: Text):
        from textfit import fit_text, line_height
        size = n.size
        if n.fit:
            size, lines = fit_text(n.runs, n.w, n.h, n.size, n.line, n.bold)
        else:
            size, lines = n.size, None
            from textfit import wrap_runs
            lines = wrap_runs(n.runs, n.size, n.w, n.bold)
        anchor = {"left": "start", "center": "middle", "right": "end"}[n.align]
        tx = n.x if n.align == "left" else (n.x + n.w / 2 if n.align == "center" else n.x + n.w)
        lh = line_height(size, n.line)
        total = lh * len(lines)
        if n.valign == "middle":
            ty = n.y + (n.h - total) / 2
        elif n.valign == "bottom":
            ty = n.y + n.h - total
        else:
            ty = n.y
        self.out.append('<g>')
        for li, parts in enumerate(lines):
            spans = []
            space = ""
            for txt, r in parts:
                sz = r.size or size
                w = "700" if (r.bold or n.bold) else "400"
                spans.append(space + f'<tspan font-weight="{w}" font-size="{sz:.2f}" '
                             f'fill="{_hex6(hx(r.color))}" fill-opacity="{r.alpha:.3f}"'
                             + (f' letter-spacing="{r.spacing}"' if r.spacing else "")
                             + (' font-style="italic"' if (r.italic or n.italic) else "")
                             + f'>{_esc(txt)}</tspan>')
                space = f'<tspan font-size="{sz:.2f}"> </tspan>'
            content = "".join(spans) or " "
            s = (f'<text x="{tx:.2f}" y="{ty + li*lh + size*0.80:.2f}" '
                 f'text-anchor="{anchor}" font-family="{n_family()}" xml:space="preserve">'
                 f'{content}</text>')
            if n.caps:
                s = s.replace("<text ", '<text style="text-transform:uppercase" ')
            self.out.append(s)
        self.out.append('</g>')

    def render(self) -> str:
        body = "\n".join(self.out)
        defs = "\n".join(f"<defs>{d}</defs>" for d in self.defs)
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" '
                f'height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                f'<rect width="{self.w}" height="{self.h}" fill="{_hex6(hx(self.bg))}"/>'
                f'{defs}{body}</svg>')


def _hex6(c: str) -> str:
    c = c if c.startswith("#") else "#" + c
    return c


def n_family() -> str:
    return "Poppins"


def render_svg(nodes, w, h, bg) -> str:
    e = SVGEmitter(w, h, bg)
    e.emit(nodes)
    return e.render()


def svg_to_png(svg: str, path: str, width: int | None = None):
    import resvg_py
    data = resvg_py.svg_to_bytes(svg_string=svg, font_dirs=FONT_DIRS,
                                 width=width, skip_system_fonts=True)
    with open(path, "wb") as f:
        f.write(bytes(data))
