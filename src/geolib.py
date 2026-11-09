"""Cartes du monde (TopoJSON Natural Earth 110m) -> géométries IR.

Décodage TopoJSON sans dépendance externe ; projection équirectangulaire
(ou Mercator), sortie en polygones prêts à dessiner, découpés en ~177 pays.
"""
from __future__ import annotations

import json
import math
import os

from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union
from shapely import affinity

from ir import Fill, Poly, Stroke, poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPO = os.path.join(ROOT, "assets", "geo", "countries-110m.json")

_data = None


def _load():
    global _data
    if _data is None:
        with open(TOPO, encoding="utf-8") as f:
            _data = json.load(f)
    return _data


def _decode_arcs(topo):
    tr = topo.get("transform")
    arcs = []
    for arc in topo["arcs"]:
        pts = []
        x = y = 0
        for dx, dy in arc:
            if tr:
                x += dx
                y += dy
                pts.append((x * tr["scale"][0] + tr["translate"][0],
                            y * tr["scale"][1] + tr["translate"][1]))
            else:
                pts.append((dx, dy))
        arcs.append(pts)
    return arcs


def _ring(arc_idx, arcs):
    pts = []
    for i in arc_idx:
        a = arcs[i] if i >= 0 else list(reversed(arcs[~i]))
        if pts and a:
            a = a[1:]
        pts += a
    return pts


class World:
    LAT_TOP, LAT_BOT = 84.0, -58.0
    def __init__(self):
        topo = _load()
        self._rings = []
        self.arcs = _decode_arcs(topo)
        self.countries = []
        obj = topo["objects"]["countries"]
        for g in obj["geometries"]:
            name = (g.get("properties") or {}).get("name", "")
            polys = []
            if g["type"] == "Polygon":
                polys = [g["arcs"]]
            elif g["type"] == "MultiPolygon":
                polys = g["arcs"]
            rings = []
            for polygon in polys:
                rr = [_ring(r, self.arcs) for r in polygon]
                rr = [r for r in rr if len(r) > 3]
                if rr:
                    rings.append(rr)
            if rings:
                rings = self._clip(rings)
            if rings:
                self.countries.append({"name": name, "polys": rings})
        self.by_name = {c["name"].lower(): c for c in self.countries}

    def _clip(self, rings):
        """Découpe proprement les pays à cheval sur le 180e méridien."""
        frame = sbox(-180, self.LAT_BOT, 180, self.LAT_TOP)
        out = []
        for ringset in rings:
            outer, holes = ringset[0], ringset[1:]
            if max(abs(b[0] - a[0]) for a, b in zip(outer, outer[1:])) <= 180:
                out.append(ringset)
                continue
            # déroule les longitudes puis découpe dans le cadre [-180,180]
            lon0 = outer[0][0]
            unwrapped, shift = [], 0.0
            prev = outer[0][0]
            for lo, la in outer:
                d = lo - prev
                if d > 180:
                    shift -= 360
                elif d < -180:
                    shift += 360
                unwrapped.append((lo + shift, la))
                prev = lo
            try:
                g = Polygon(unwrapped).buffer(0)
            except Exception:
                out.append(ringset)
                continue
            # essaie les translations -360 / 0 / +360 pour garder le morceau visible
            best = None
            base = g.buffer(0)
            for k in (-360, 0, 360):
                try:
                    gg = base if k == 0 else affinity.translate(base, k)
                    inter = gg.intersection(frame)
                except Exception:
                    continue
                if inter.is_empty:
                    continue
                best = inter if best is None else unary_union([best, inter])
            if best is None:
                out.append(ringset)
                continue
            geoms = list(getattr(best, "geoms", [best]))
            for gg in geoms:
                if gg.is_empty or gg.area < 0.05:
                    continue
                ext = list(gg.exterior.coords)
                holes2 = [list(h.coords) for h in gg.interiors]
                out.append([ext] + holes2)
        return out


_W = None


def world() -> World:
    global _W
    if _W is None:
        _W = World()
    return _W


def _split_antimeridian(ring, jump=180.0):
    """Les pays qui chevauchent le 180e méridien sont dessinés d'un seul tenant :
    on ne conserve que le plus grand fragment (évite les traînées horizontales)."""
    parts, cur = [], [ring[0]]
    for a, b in zip(ring, ring[1:]):
        if abs(b[0] - a[0]) > jump:
            if len(cur) > 2:
                parts.append(cur)
            cur = [b]
        else:
            cur.append(b)
    if len(cur) > 2:
        parts.append(cur)
    if len(parts) <= 1:
        return [ring]

    def area(pts):
        s = 0.0
        for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]):
            s += x1 * y2 - x2 * y1
        return abs(s) / 2
    return [max(parts, key=area)]


def project(lon, lat, box, proj="equirect", lat_top=84, lat_bot=-58):
    """(lon, lat) -> (x, y) dans box=(x, y, w, h)."""
    x0, y0, w, h = box
    lo0, lo1 = -180.0, 180.0
    if proj == "mercator":
        def my(la):
            la = max(-85, min(85, la))
            return math.log(math.tan(math.pi / 4 + math.radians(la) / 2))
        yt, yb = my(lat_top), my(lat_bot)
        ny = (yt - my(lat)) / (yt - yb)
    else:
        ny = (lat_top - lat) / (lat_top - lat_bot)
    nx = (lon - lo0) / (lo1 - lo0)
    return x0 + nx * w, y0 + ny * h


def map_nodes(x, y, w, h, proj="equirect", color="#FFFFFF", alpha=0.18,
              stroke=None, only=None, exclude=None, anim="fade", key="map",
              lat_top=84, lat_bot=-58, min_area=0.0):
    """Carte du monde en polygones (un par pays -> recolorable un par un)."""
    W_ = world()
    box = (x, y, w, h)
    out = []
    for c in W_.countries:
        nm = c["name"].lower()
        if only and not any(o in nm for o in only):
            continue
        if exclude and any(e in nm for e in exclude):
            continue
        for ringset in c["polys"]:
            outer = ringset[0]
            if min(la for lo, la in outer) < lat_bot + 1:
                continue      # Antarctique / zones hors cadre
            for part in _split_antimeridian(outer):
                pts = [project(lo, la, box, proj, lat_top, lat_bot) for lo, la in part]
                if len(pts) < 3:
                    continue
                if min_area > 0:
                    xs = [p[0] for p in pts]
                    ys = [p[1] for p in pts]
                    if (max(xs) - min(xs)) < min_area or (max(ys) - min(ys)) < min_area:
                        continue
                out.append(poly(pts, fill=Fill(color=color, alpha=alpha), stroke=stroke,
                                anim=anim, key=key, name="Pays " + c["name"]))
            continue
        for ringset in []:
            if min_area > 0:
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                if (max(xs) - min(xs)) < min_area or (max(ys) - min(ys)) < min_area:
                    continue
            out.append(poly(pts, fill=Fill(color=color, alpha=alpha), stroke=stroke,
                            anim=anim, key=key, name="Pays " + c["name"]))
    return out


def country_nodes(name, x, y, w, h, proj="equirect", color="#FFFFFF", alpha=1.0,
                  stroke=None, anim="zoom", key="country", lat_top=84, lat_bot=-58,
                  grow=0.0):
    """Un seul pays, ajusté au cadre demandé."""
    W_ = world()
    c = W_.by_name.get(name.lower())
    if c is None:
        return []
    box = (x, y, w, h)
    out = []
    for ringset in c["polys"]:
        pts = [project(lo, la, box, proj, lat_top, lat_bot) for lo, la in ringset[0]]
        if len(pts) > 2:
            out.append(poly(pts, fill=Fill(color=color, alpha=alpha), stroke=stroke,
                            anim=anim, key=key, name=name))
    return out


def country_zoom(name, x, y, w, h, color="#FFFFFF", alpha=1.0, stroke=None,
                 anim="zoom", key="country", pad=0.12):
    """Un pays cadré au plus près (zoom automatique sur son emprise)."""
    W_ = world()
    c = W_.by_name.get(name.lower())
    if c is None:
        return []
    # cadre = plus grande masse continentale du pays (hors territoires lointains)
    best, best_a = None, -1
    for ringset in c["polys"]:
        pts = ringset[0]
        lx = [q[0] for q in pts]
        ly = [q[1] for q in pts]
        a = (max(lx) - min(lx)) * (max(ly) - min(ly))
        if a > best_a:
            best, best_a = (min(lx), max(lx), min(ly), max(ly)), a
    x0, x1, y0, y1 = best
    ww, hh = max(1e-6, x1 - x0), max(1e-6, y1 - y0)
    sc = min(w / ww, h / hh) * (1 - pad * 2)
    ox = x + (w - ww * sc) / 2
    oy = y + (h - hh * sc) / 2
    out = []
    for ringset in c["polys"]:
        ring = ringset[0]
        lx = [q[0] for q in ring]
        ly = [q[1] for q in ring]
        cx_, cy_ = sum(lx) / len(lx), sum(ly) / len(ly)
        if not (x0 - 0.6 * ww <= cx_ <= x1 + 0.6 * ww and y0 - 0.6 * hh <= cy_ <= y1 + 0.6 * hh):
            continue
        pts = [(ox + (lo - x0) * sc, oy + (y1 - la) * sc) for lo, la in ring]
        if len(pts) > 2:
            out.append(poly(pts, fill=Fill(color=color, alpha=alpha), stroke=stroke,
                            anim=anim, key=key, name="Pays " + name))
    return out


def pins(pts, box, proj="equirect", color="#FFFFFF", r=7, lat_top=84, lat_bot=-58):
    """Marqueurs géolocalisés : pts = [(lon, lat, label|None)]."""
    from ir import ellipse
    out = []
    for p in pts:
        lon, lat = p[0], p[1]
        px, py = project(lon, lat, box, proj, lat_top, lat_bot)
        out.append(ellipse(px, py, r * 2.4, fill=Fill(color=color, alpha=0.18)))
        out.append(ellipse(px, py, r, fill=Fill(color=color)))
    return out


def arcs_routes(pairs, box, proj="equirect", color="#FFFFFF", width=2, alpha=0.8,
                lat_top=84, lat_bot=-58, bend=0.18):
    """Arcs de connexion entre villes/pays (style « réseau mondial »)."""
    from ir import Poly, poly
    out = []
    for (a, b) in pairs:
        x1, y1 = project(a[0], a[1], box, proj, lat_top, lat_bot)
        x2, y2 = project(b[0], b[1], box, proj, lat_top, lat_bot)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        cx, cy = mx - dy * bend, my + dx * bend
        pts = []
        for i in range(25):
            t = i / 24
            xx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2
            yy = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2
            pts.append((xx, yy))
        out.append(poly(pts, fill=None, closed=False,
                        stroke=Stroke(color=color, width=width, alpha=alpha, cap="round")))
    return out
