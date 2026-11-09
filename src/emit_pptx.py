"""Backend DrawingML : IR -> formes PowerPoint natives (éditables, animables)."""
from __future__ import annotations

import math
from typing import Iterable, Sequence

from lxml import etree
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

from ir import (Arc, Ellipse, Fill, Group, Icon, Line, Poly, Rect, Run, Stroke,
                Text, hx, PX)

A_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
P_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def sub(parent, tag, **attrs):
    el = etree.SubElement(parent, qn(tag))
    for k, v in attrs.items():
        el.set(k, str(v))
    return el


def psub(parent, tag, **attrs):
    """Élément dans l'espace de noms presentationml."""
    el = etree.SubElement(parent, "{%s}%s" % (P_NS, tag))
    for k, v in attrs.items():
        if ":" in k:
            pre, local = k.split(":")
            ns = {"r": R_NS, "a": A_NS, "p": P_NS}[pre]
            el.set("{%s}%s" % (ns, local), str(v))
        else:
            el.set(k, str(v))
    return el


# ------------------------------------------------------------------ couleur
def clr(parent, tag: str, color: str, alpha: float = 1.0):
    el = sub(parent, tag)
    c = sub(el, "a:srgbClr", val=hx(color))
    if alpha < 0.999:
        sub(c, "a:alpha", val=int(round(alpha * 100000)))
    return el


def gradient_fill(parent, fill: Fill, angle: float):
    g = sub(parent, "a:gradFill", rotWithShape="1")
    gs = sub(g, "a:gsLst")
    stops = fill.stops or [(0.0, fill.color, fill.alpha), (1.0, fill.color2, fill.alpha)]
    for pos, c, a in stops:
        e = sub(gs, "a:gs", pos=int(round(pos * 100000)))
        sc = sub(e, "a:srgbClr", val=hx(c))
        if a < 0.999:
            sub(sc, "a:alpha", val=int(round(a * 100000)))
    if fill.radial:
        sub(g, "a:path", path="circle")
        sub(g, "a:fillToRect", l="50000", t="50000", r="50000", b="50000")
    else:
        sub(g, "a:lin", ang=int(round((angle % 360) * 60000)), scaled="0")
    return g


def apply_fill(spPr, fill: Fill | None):
    if not fill:
        sub(spPr, "a:noFill")
        return
    if fill.color2 or fill.stops:
        gradient_fill(spPr, fill, fill.angle)
        return
    sf = sub(spPr, "a:solidFill")
    c = sub(sf, "a:srgbClr", val=hx(fill.color))
    if fill.alpha < 0.999:
        sub(c, "a:alpha", val=int(round(fill.alpha * 100000)))


def apply_stroke(spPr, st: Stroke | None):
    if not st or st.width <= 0:
        return
    ln = sub(spPr, "a:ln")
    ln.set("w", str(max(1, int(round(st.width * PX)))))
    ln.set("cap", "rnd" if st.cap == "round" else "flat")
    sf = sub(ln, "a:solidFill")
    c = sub(sf, "a:srgbClr", val=hx(st.color))
    if st.alpha < 0.999:
        sub(c, "a:alpha", val=int(round(st.alpha * 100000)))
    if st.dash:
        sub(ln, "a:prstDash", val={"dash": "dash", "dot": "sysDot", "sysdash": "sysDash"}[st.dash])
    sub(ln, "a:round" if st.join == "round" else "a:miter")


def add_shadow(spPr, sh):
    eff = sub(spPr, "a:effectLst")
    e = sub(eff, "a:outerShdw", blurRad=max(1, int(sh.blur * PX)),
            dist=int(sh.dist * PX), dir=int((sh.angle % 360) * 60000), rotWithShape="0")
    c = sub(e, "a:srgbClr", val=hx(sh.color))
    sub(c, "a:alpha", val=int(round(sh.alpha * 100000)))


# ------------------------------------------------------------------ géométrie
def _catmull_beziers(pts, closed: bool):
    if len(pts) < 3:
        return [("M", pts[0])] + [("L", p) for p in pts[1:]]
    P = list(pts)
    P = ([P[-1]] + P + [P[0], P[1]]) if closed else ([P[0]] + P + [P[-1]])
    out = [("M", P[1])]
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        out.append(("C", c1, c2, p2))
    return out


def _arc_points(cx, cy, r, a0, a1, steps=None):
    sweep = a1 - a0
    steps = steps or max(10, int(abs(sweep) / 3))
    return [(cx + r * math.cos(math.radians(a0 + sweep * i / steps)),
             cy + r * math.sin(math.radians(a0 + sweep * i / steps)))
            for i in range(steps + 1)]


class PPTXEmitter:
    def __init__(self, slide):
        self.slide = slide
        self.spTree = slide.shapes._spTree
        self.ids: dict[str, int] = {}
        self.anim_entries: list[tuple[int, str, int]] = []
        self.serial = 0

    # -------------------------------------------------------------- helpers
    def _next_id(self) -> int:
        self.serial += 1
        return 1000 + self.serial

    def _container(self):
        return self.spTree

    def _name(self, n, default="Forme"):
        nm = n.name or n.key or default
        return str(nm)[:40]

    def _sp(self, node, prst: str | None, adj: dict | None = None, name="Forme"):
        sid = self._next_id()
        sp = sub(self.spTree, "p:sp")
        nv = sub(sp, "p:nvSpPr")
        sub(nv, "p:cNvPr", id=sid, name=self._name(node, name))
        sub(nv, "p:cNvSpPr")
        sub(nv, "p:nvPr")
        spr = sub(sp, "p:spPr")
        xfrm = sub(spr, "a:xfrm")
        sub(xfrm, "a:off", x=int(node.x * PX), y=int(node.y * PX))
        sub(xfrm, "a:ext", cx=max(1, int(node.w * PX)), cy=max(1, int(node.h * PX)))
        if prst:
            pg = sub(spr, "a:prstGeom", prst=prst)
            av = sub(pg, "a:avLst")
            for k, v in (adj or {}).items():
                sub(av, "a:gd", name=k, fmla=f"val {int(v)}")
        return sp, spr, sid

    # -------------------------------------------------------------- formes
    def rect(self, n: Rect):
        radius = n.radius or 0
        if radius > 0.5:
            prst = "roundRect"
            adj = {"adj": min(50000, int(radius / max(1, min(n.w, n.h)) * 100000))}
        else:
            prst, adj = "rect", None
        sp, spr, sid = self._sp(n, prst, adj, "Rectangle")
        apply_fill(spr, n.fill)
        apply_stroke(spr, n.stroke)
        self._register(n, sid)
        return sid

    def ellipse(self, n: Ellipse):
        sp, spr, sid = self._sp(n, "ellipse", name="Ellipse")
        apply_fill(spr, n.fill)
        apply_stroke(spr, n.stroke)
        self._register(n, sid)
        return sid

    def line(self, n: Line):
        sid = self._next_id()
        cx = sub(self.spTree, "p:cxnSp")
        nv = sub(cx, "p:nvCxnSpPr")
        sub(nv, "p:cNvPr", id=sid, name=self._name(n, "Ligne"))
        sub(nv, "p:cNvCxnSpPr")
        sub(nv, "p:nvPr")
        spr = sub(cx, "p:spPr")
        x, y = min(n.x1, n.x2), min(n.y1, n.y2)
        xfrm = sub(spr, "a:xfrm")
        if n.x2 < n.x1:
            xfrm.set("flipH", "1")
        if n.y2 < n.y1:
            xfrm.set("flipV", "1")
        sub(xfrm, "a:off", x=int(x * PX), y=int(y * PX))
        sub(xfrm, "a:ext", cx=max(1, int(abs(n.x2 - n.x1) * PX)),
            cy=max(1, int(abs(n.y2 - n.y1) * PX)))
        pg = sub(spr, "a:prstGeom", prst="line")
        sub(pg, "a:avLst")
        apply_stroke(spr, n.stroke)
        self._register(n, sid)
        return sid

    def custgeom(self, node, cmds, closed, fill, stroke, name="Forme"):
        if not cmds:
            return None
        xs, ys = [], []
        for c in cmds:
            for p in c[1:]:
                xs.append(p[0])
                ys.append(p[1])
        x0, y0 = min(xs), min(ys)
        w = max(1.0, max(xs) - x0)
        h = max(1.0, max(ys) - y0)
        node.x, node.y, node.w, node.h = x0, y0, w, h
        sp, spr, sid = self._sp(node, None, name=name)
        cg = sub(spr, "a:custGeom")
        sub(cg, "a:avLst")
        sub(cg, "a:gdLst")
        sub(cg, "a:ahLst")
        sub(cg, "a:cxnLst")
        sub(cg, "a:rect", l="0", t="0", r="r", b="b")
        pl = sub(cg, "a:pathLst")
        path = sub(pl, "a:path", w=max(1, int(w * PX)), h=max(1, int(h * PX)))
        if not fill:
            path.set("fill", "none")

        def P(p):
            return int((p[0] - x0) * PX), int((p[1] - y0) * PX)

        for c in cmds:
            if c[0] == "M":
                pt = sub(path, "a:moveTo")
                px, py = P(c[1])
                sub(pt, "a:pt", x=px, y=py)
            elif c[0] == "L":
                pt = sub(path, "a:lnTo")
                px, py = P(c[1])
                sub(pt, "a:pt", x=px, y=py)
            elif c[0] == "C":
                pt = sub(path, "a:cubicBezTo")
                for pp in c[1:]:
                    px, py = P(pp)
                    sub(pt, "a:pt", x=px, y=py)
        if closed:
            sub(path, "a:close")
        apply_fill(spr, fill)
        apply_stroke(spr, stroke)
        self._register(node, sid)
        return sid

    def poly(self, n: Poly):
        if n.smooth:
            cmds = _catmull_beziers(list(n.pts), n.closed)
        else:
            cmds = [("M", n.pts[0])] + [("L", p) for p in n.pts[1:]]
        return self.custgeom(n, cmds, n.closed, n.fill, n.stroke, "Polygone")

    def arc(self, n: Arc):
        outer = _arc_points(n.cx, n.cy, n.r, n.a0, n.a1)
        if n.inner and n.inner > 0:
            inner = _arc_points(n.cx, n.cy, n.r * n.inner, n.a1, n.a0)
            pts = outer + inner
            cmds = [("M", pts[0])] + [("L", p) for p in pts[1:]]
            return self.custgeom(n, cmds, True, n.fill or Fill(color=n.stroke.color if n.stroke else "#FFFFFF"), None, "Arc")
        if n.pie and n.fill:
            cmds = [("M", (n.cx, n.cy))] + [("L", p) for p in outer]
            return self.custgeom(n, cmds, True, n.fill, n.stroke, "Camembert")
        cmds = [("M", outer[0])] + [("L", p) for p in outer[1:]]
        return self.custgeom(n, cmds, False, None, n.stroke, "Arc")

    # -------------------------------------------------------------- icônes
    def icon(self, n: Icon):
        from iconlib import icon_cmds
        cmds = []
        for d in n.paths:
            cmds += list(icon_cmds(d))
        if not cmds:
            return
        sc = n.size / 24.0
        moved = []
        for c in cmds:
            if c[0] == "Z":
                moved.append(c)
            else:
                moved.append((c[0],) + tuple(
                    (n.x + p[0] * sc, n.y + p[1] * sc) for p in c[1:]))
        st = n.stroke
        if st:
            st = Stroke(color=st.color, alpha=st.alpha, width=max(1.2, st.width * sc),
                        cap="round", join="round")
        return self.custgeom(n, moved, False, None, st, "Icône")

    # -------------------------------------------------------------- texte
    def text(self, n: Text):
        sid = self._next_id()
        sp = sub(self.spTree, "p:sp")
        nv = sub(sp, "p:nvSpPr")
        nm = n.name or (n.runs[0].text[:24] if n.runs else "Texte")
        sub(nv, "p:cNvPr", id=sid, name=str(nm)[:40])
        cnv = sub(nv, "p:cNvSpPr", txBox="1")
        sub(cnv, "a:spLocks", noGrp="1")
        sub(nv, "p:nvPr")
        spr = sub(sp, "p:spPr")
        xfrm = sub(spr, "a:xfrm")
        sub(xfrm, "a:off", x=int(n.x * PX), y=int(n.y * PX))
        sub(xfrm, "a:ext", cx=max(1, int(n.w * PX)), cy=max(1, int(n.h * PX)))
        pg = sub(spr, "a:prstGeom", prst="rect")
        sub(pg, "a:avLst")
        sub(spr, "a:noFill")

        tb = sub(sp, "p:txBody")
        l, t, r, b = n.margins
        bodyPr = sub(tb, "a:bodyPr", wrap="square", lIns=int(l * PX), tIns=int(t * PX),
                     rIns=int(r * PX), bIns=int(b * PX),
                     anchor={"top": "t", "middle": "ctr", "bottom": "b"}[n.valign],
                     anchorCtr="0")
        sub(bodyPr, "a:noAutofit")
        sub(tb, "a:lstStyle")

        from textfit import wrap_runs, line_height
        size = n.size
        if n.fit:
            from textfit import fit_text
            size, lines = fit_text(n.runs, n.w, n.h, n.size, n.line, n.bold)
        else:
            lines = wrap_runs(n.runs, n.size, n.w, n.bold)

        align = {"left": "l", "center": "ctr", "right": "r"}[n.align]
        for parts in lines:
            p = sub(tb, "a:p")
            pPr = sub(p, "a:pPr", algn=align)
            lnSpc = sub(pPr, "a:lnSpc")
            # interligne exact (px -> pt) pour un rendu identique à l'aperçu
            sub(lnSpc, "a:spcPts", val=max(100, int(round(size * n.line * 50))))
            if not parts:
                parts = [(None, None)]
            for i, (tok, run) in enumerate(parts):
                if run is None:
                    rr = Run(" ", color=n.color)
                else:
                    rr = Run((" " if i else "") + tok, color=run.color, bold=run.bold,
                             size=run.size, italic=run.italic, alpha=run.alpha,
                             spacing=run.spacing)
                ar = sub(p, "a:r")
                sz = int(round((rr.size or size) * 50))
                rPr = sub(ar, "a:rPr", sz=sz,
                          b="1" if (rr.bold or n.bold) else "0",
                          i="1" if (rr.italic or n.italic) else "0")
                if rr.spacing:
                    rPr.set("spc", str(int(rr.spacing * 100)))
                if n.caps:
                    rPr.set("cap", "all")
                c = sub(rPr, "a:solidFill")
                cc = sub(c, "a:srgbClr", val=hx(rr.color))
                if rr.alpha < 0.999:
                    sub(cc, "a:alpha", val=int(rr.alpha * 100000))
                sub(rPr, "a:latin", typeface="Poppins")
                tt = sub(ar, "a:t")
                tt.text = rr.text
        self._register(n, sid)
        return sid

    # -------------------------------------------------------------- divers
    def _register(self, n, sid):
        if n.key:
            self.ids[n.key] = sid
        if n.anim:
            self.anim_entries.append((sid, n.anim, n.anim_delay))

    def group(self, n: Group):
        gid = self._next_id()
        kids = [c for c in n.children if hasattr(c, "x")]
        if not kids:
            return
        x0 = min(c.x for c in kids)
        y0 = min(c.y for c in kids)
        x1 = max(c.x + c.w for c in kids)
        y1 = max(c.y + c.h for c in kids)
        W_, H_ = max(1, x1 - x0), max(1, y1 - y0)
        grp = sub(self.spTree, "p:grpSp")
        nv = sub(grp, "p:nvGrpSpPr")
        sub(nv, "p:cNvPr", id=gid, name=str(n.name or "Groupe")[:80])
        sub(nv, "p:cNvGrpSpPr")
        sub(nv, "p:nvPr")
        spr = sub(grp, "p:grpSpPr")
        xfrm = sub(spr, "a:xfrm")
        sub(xfrm, "a:off", x=int(x0 * PX), y=int(y0 * PX))
        sub(xfrm, "a:ext", cx=int(W_ * PX), cy=int(H_ * PX))
        sub(xfrm, "a:chOff", x=int(x0 * PX), y=int(y0 * PX))
        sub(xfrm, "a:chExt", cx=int(W_ * PX), cy=int(H_ * PX))
        saved = self.spTree
        self.spTree = grp
        for c in n.children:
            self.one(c)
        self.spTree = saved
        if n.key:
            self.ids[n.key] = gid

    def one(self, n):
        t = type(n).__name__
        m = getattr(self, t.lower(), None)
        if m is None:
            raise TypeError("noeud non supporté: " + t)
        return m(n)

    def emit(self, nodes):
        for n in nodes:
            self.one(n)


def set_slide_bg(slide, colors, angle=115.0):
    cSld = slide._element.find(qn("p:cSld"))
    old = cSld.find(qn("p:bg"))
    if old is not None:
        cSld.remove(old)
    bg = etree.Element(qn("p:bg"))
    bgPr = sub(bg, "p:bgPr")
    if isinstance(colors, str):
        sf = sub(bgPr, "a:solidFill")
        sub(sf, "a:srgbClr", val=hx(colors))
    else:
        g = sub(bgPr, "a:gradFill", rotWithShape="1")
        gs = sub(g, "a:gsLst")
        for pos, c in colors:
            e = sub(gs, "a:gs", pos=int(pos * 100000))
            sub(e, "a:srgbClr", val=hx(c))
        sub(g, "a:lin", ang=int((angle % 360) * 60000), scaled="0")
    sub(bgPr, "a:effectLst")
    cSld.insert(0, bg)


# ------------------------------------------------------------------ animation
FILTERS = {
    "fade": ("fade", 10),
    "rise": ("fade", 10),
    "wipe-up": ("wipe(up)", 22),
    "wipe-left": ("wipe(left)", 22),
    "wipe-right": ("wipe(right)", 22),
    "wipe-down": ("wipe(down)", 22),
    "zoom": ("zoom(in)", 23),
    "circle": ("circle(in)", 27),
    "barn": ("barn(inVertical)", 13),
    "checker": ("checkerboard(across)", 12),
    "dissolve": ("dissolve", 9),
    "wheel": ("wheel(1)", 21),
    "strips": ("strips(downRight)", 18),
    "plus": ("plus(in)", 24),
    "diamond": ("diamond(in)", 25),
    "fly-left": ("wipe(left)", 22),
    "fly-right": ("wipe(right)", 22),
    "fly-up": ("wipe(up)", 22),
    "fly-down": ("wipe(down)", 22),
}

TIMING_HEAD = (
    '<p:timing xmlns:p="%s" xmlns:a="%s"><p:tnLst>'
    '<p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">'
    '<p:childTnLst><p:seq concurrent="1" nextAc="seek">'
    '<p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst/></p:cTn>'
    '<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
    '<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst>'
    '</p:seq></p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>' % (P_NS, A_NS)
)


def build_timing(slide, entries, dur=380, click_first=True):
    """entries : [(shape_id, effect, delay_ms)] — enchaînement automatique."""
    if not entries:
        return
    sld = slide._element
    old = sld.find(qn("p:timing"))
    if old is not None:
        sld.remove(old)
    timing = etree.fromstring(TIMING_HEAD)
    seq_ctn = timing.findall(".//" + qn("p:cTn"))[1]
    child = seq_ctn.find(qn("p:childTnLst"))
    nid = 3
    for idx, (spid, kind, delay) in enumerate(entries):
        filt, preset = FILTERS.get(kind, ("fade", 10))
        first = (idx == 0 and click_first)
        node_type = "clickEffect" if first else "afterEffect"
        start_delay = "indefinite" if first else str(int(delay))

        outer = etree.SubElement(child, "{%s}par" % P_NS)
        ctn = psub(outer, "cTn", id=nid, fill="hold")
        nid += 1
        st = psub(ctn, "stCondLst")
        psub(st, "cond", delay="indefinite" if first else "0")
        ch1 = psub(ctn, "childTnLst")
        par2 = psub(ch1, "par")
        ctn2 = psub(par2, "cTn", id=nid, fill="hold")
        nid += 1
        st2 = psub(ctn2, "stCondLst")
        psub(st2, "cond", delay="0")
        ch2 = psub(ctn2, "childTnLst")
        par3 = psub(ch2, "par")
        ctn3 = psub(par3, "cTn", id=nid, presetID=preset, presetClass="entr",
                    presetSubtype="0", fill="hold", grpId="0", nodeType=node_type)
        nid += 1
        st3 = psub(ctn3, "stCondLst")
        psub(st3, "cond", delay="0")
        ch3 = psub(ctn3, "childTnLst")

        s = psub(ch3, "set")
        bh = psub(s, "cBhvr")
        ct = psub(bh, "cTn", id=nid, dur="1", fill="hold")
        nid += 1
        sc = psub(ct, "stCondLst")
        psub(sc, "cond", delay="0")
        tg = psub(bh, "tgtEl")
        psub(tg, "spTgt", spid=str(spid))
        anl = psub(bh, "attrNameLst")
        psub(anl, "attrName").text = "style.visibility"
        to = psub(s, "to")
        psub(to, "strVal", val="visible")

        ae = psub(ch3, "animEffect", transition="in", filter=filt)
        bh2 = psub(ae, "cBhvr")
        psub(bh2, "cTn", id=nid, dur=str(dur))
        nid += 1
        tg2 = psub(bh2, "tgtEl")
        psub(tg2, "spTgt", spid=str(spid))

        if kind in ("rise", "fly-up", "fly-left", "fly-right", "fly-down"):
            # petit déplacement (mouvement "rise")
            dx = {"fly-left": "0.03", "fly-right": "-0.03"}.get(kind, "0")
            dy = "0.03" if kind in ("rise", "fly-up") else ("-0.03" if kind == "fly-down" else "0")
            an2 = psub(ch3, "anim", calcmode="lin", valueType="num")
            bh3 = psub(an2, "cBhvr")
            psub(bh3, "cTn", id=nid, dur=str(dur), fill="hold")
            nid += 1
            tg3 = psub(bh3, "tgtEl")
            psub(tg3, "spTgt", spid=str(spid))
            al3 = psub(bh3, "attrNameLst")
            psub(al3, "attrName").text = "ppt_x" if dx != "0" else "ppt_y"
            tav = psub(an2, "tavLst")
            t0 = psub(tav, "tav", tm="0")
            v0 = psub(t0, "val")
            base = "#ppt_x" if dx != "0" else "#ppt_y"
            psub(v0, "strVal", val=f"{base}+{dx if dx != '0' else dy}")
            t1 = psub(tav, "tav", tm="100000")
            v1 = psub(t1, "val")
            psub(v1, "strVal", val=base)

    sld.append(timing)
