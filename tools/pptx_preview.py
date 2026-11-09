"""Vérificateur end-to-end : relit un .pptx généré et le re-rend en PNG
(contrôle indépendant du backend DrawingML).

Usage :  python tools/pptx_preview.py fichier.pptx dpi=1 slide1,slide2 ...
"""
from __future__ import annotations

import os
import sys
import zipfile

from lxml import etree
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

NS = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main",
      "p": "http://schemas.openxmlformats.org/presentationml/2006/main"}
EMU = 914400.0
FONT = {False: "assets/fonts/Poppins-400.ttf", True: "assets/fonts/Poppins-700.ttf"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fnt(size, bold):
    return ImageFont.truetype(os.path.join(ROOT, FONT[bool(bold)]), max(4, int(round(size))))


def _c(t):
    """normalise (hex, alpha) -> couleur PIL."""
    if t is None:
        return None
    h, a = t
    return h + ("%02X" % int(a * 255) if False else "") if a >= 0.999 else (
        int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), int(a * 255))


def color_of(el, default=None):
    """Retourne une couleur PIL (str ou RGBA)."""
    t = _color_raw(el)
    if t is None:
        return default
    h, a = t
    if a >= 0.999:
        return h
    return (int(h[1:3], 16), int(h[3:5], 16), int(h[5:7], 16), int(a * 255))


def _color_raw(el):
    if el is None:
        return None
    c = el.find(".//a:srgbClr", NS)
    if c is None:
        return None
    v = c.get("val")
    if not v or len(v) != 6:
        return None
    a = 1.0
    al = c.find("a:alpha", NS)
    if al is not None:
        a = int(al.get("val")) / 100000.0
    return "#" + v, a


def xfrm_of(el):
    x = el.find(".//a:xfrm", NS)
    if x is None:
        return None
    off = x.find("a:off", NS)
    ext = x.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")),
            x.get("flipH") == "1", x.get("flipV") == "1")


def pts_of_path(path):
    """Retourne une liste de sous-chemins (listes de points) approchant les courbes."""
    subs, cur = [], []
    for el in path:
        tag = etree.QName(el).localname
        pts = [(int(p.get("x")), int(p.get("y"))) for p in el.findall("a:pt", NS)]
        if tag == "moveTo":
            if cur:
                subs.append(cur)
            cur = pts[:]
        elif tag == "lnTo":
            cur += pts
        elif tag == "cubicBezTo" and len(pts) == 3 and cur:
            p0 = cur[-1]
            for i in range(1, 9):
                t = i / 8
                mt = 1 - t
                xx = (mt ** 3 * p0[0] + 3 * mt * mt * t * pts[0][0] +
                      3 * mt * t * t * pts[1][0] + t ** 3 * pts[2][0])
                yy = (mt ** 3 * p0[1] + 3 * mt * mt * t * pts[0][1] +
                      3 * mt * t * t * pts[1][1] + t ** 3 * pts[2][1])
                cur.append((xx, yy))
        elif tag == "close" and cur:
            subs.append(cur)
            cur = []
    if cur:
        subs.append(cur)
    return subs


def render(path, out_dir, which=None, scale=1.0):
    os.makedirs(out_dir, exist_ok=True)
    from pptx import Presentation
    prs = Presentation(path)
    SW, SH = prs.slide_width, prs.slide_height
    w, h = int(SW / EMU * 96 * scale), int(SH / EMU * 96 * scale)
    k = w / SW
    PT = (w / (SW / EMU)) / 72.0   # px par point

    outs = []
    for idx, slide in enumerate(prs.slides, start=1):
        if which and idx not in which:
            continue
        img = Image.new("RGB", (w, h), "#202020")
        d = ImageDraw.Draw(img, "RGBA")
        # fond
        bg = slide._element.find(".//p:bg//a:srgbClr", NS)
        grad = slide._element.findall(".//p:bg//a:gs//a:srgbClr", NS)
        if len(grad) >= 2:
            c1 = "#" + grad[0].get("val")
            c2 = "#" + grad[1].get("val")
            for y in range(h):
                t = y / max(1, h - 1)
                col = tuple(int(int(c1[i:i + 2], 16) * (1 - t) + int(c2[i:i + 2], 16) * t)
                            for i in (1, 3, 5))
                d.line([(0, y), (w, y)], fill=col)
        elif bg is not None:
            d.rectangle([0, 0, w, h], fill="#" + bg.get("val"))

        for shape in slide.shapes:
            el = shape._element
            x = xfrm_of(el)
            if x is None:
                continue
            sx, sy, cx, cy, fh, fv = x
            X, Y, CX, CY = sx * k, sy * k, cx * k, cy * k
            tag = etree.QName(el).localname
            ln = el.find(".//a:ln", NS)
            sw = 0
            if ln is not None and ln.get("w"):
                sw = max(1, int(round(int(ln.get("w")) / 12700 * PT)))
            fill = color_of(el.find(".//p:spPr/a:solidFill", NS))
            grad2 = el.findall(".//p:spPr/a:gradFill//a:gs//a:srgbClr", NS)
            if grad2 and len(grad2) >= 2 and len(grad2[0].get("val", "")) == 6:
                al = grad2[0].find("a:alpha", NS)
                av = int(al.get("val")) / 100000.0 if al is not None else 1.0
                hx_ = "#" + grad2[0].get("val")
                fill = hx_ if av > 0.999 else (int(hx_[1:3], 16), int(hx_[3:5], 16),
                                               int(hx_[5:7], 16), int(av * 255))
            stroke = color_of(ln.find("a:solidFill", NS)) if ln is not None else None
            geom = el.find(".//a:prstGeom", NS)
            prst = geom.get("prst") if geom is not None else None

            if tag == "sp" and el.find(".//p:txBody", NS) is not None and prst == "rect" \
                    and fill is None and stroke is None:
                draw_text(d, el, X, Y, CX, CY, k, scale, PT)
                continue
            if tag == "cxnSp":
                if stroke:
                    xx, yy, xx2, yy2 = X, Y, X + CX, Y + CY
                    if fh:
                        xx, xx2 = xx2, xx
                    if fv:
                        yy, yy2 = yy2, yy
                    d.line([xx, yy, xx2, yy2], fill=stroke, width=sw or 1)
                continue
            cust = el.find(".//a:custGeom", NS)
            if cust is not None:
                pathNode = cust.find(".//a:path", NS)
                pw, ph = int(pathNode.get("w")), int(pathNode.get("h"))
                subs = pts_of_path(pathNode)
                scx = CX / max(1, pw)
                scy = CY / max(1, ph)
                for subp in subs:
                    pts = [(X + p[0] * scx, Y + p[1] * scy) for p in subp]
                    if len(pts) > 2 and (fill or pathNode.get("fill") != "none"):
                        if fill:
                            d.polygon(pts, fill=fill)
                    if stroke and sw:
                        d.line(pts + ([pts[0]] if pathNode.get("fill") != "none" else []),
                               fill=stroke, width=sw, joint="curve")
                continue
            if prst == "ellipse":
                d.ellipse([X, Y, X + CX, Y + CY], fill=fill,
                          outline=stroke, width=max(1, sw))
            elif prst == "roundRect":
                r = min(CX, CY) * 0.16
                try:
                    d.rounded_rectangle([X, Y, X + CX, Y + CY], radius=r, fill=fill,
                                        outline=stroke, width=max(1, sw))
                except TypeError:
                    d.rectangle([X, Y, X + CX, Y + CY], fill=fill)
            else:
                d.rectangle([X, Y, X + CX, Y + CY], fill=fill, outline=stroke,
                            width=max(1, sw))
            if tag == "sp" and el.find(".//p:txBody", NS) is not None and prst != "rect":
                draw_text(d, el, X, Y, CX, CY, k, scale, PT)
        p = os.path.join(out_dir, f"slide{idx:02d}.png")
        img.save(p)
        outs.append(p)
    return outs


def draw_text(d, el, X, Y, CX, CY, k, scale, PT):
    body = el.find(".//p:txBody", NS)
    bodyPr = body.find("a:bodyPr", NS)
    lIns = int(bodyPr.get("lIns", 91440)) * k
    rIns = int(bodyPr.get("rIns", 91440)) * k
    tIns = int(bodyPr.get("tIns", 45720)) * k
    bIns = int(bodyPr.get("bIns", 45720)) * k
    anchor = bodyPr.get("anchor", "t")
    lines = []
    for para in body.findall("a:p", NS):
        pPr = para.find("a:pPr", NS)
        algn = pPr.get("algn", "l") if pPr is not None else "l"
        runs = []
        for r in para.findall("a:r", NS):
            rPr = r.find("a:rPr", NS)
            t = r.find("a:t", NS)
            txt = t.text or ""
            sz = int(rPr.get("sz", 1800)) / 100.0 * PT
            bold = rPr.get("b") == "1"
            col = color_of(rPr.find("a:solidFill", NS), "#FFFFFF")
            spc = int(rPr.get("spc", 0)) / 100.0 * PT
            runs.append((txt, sz, bold, col, spc))
        if not runs:
            runs = [("", 12, False, ("#FFFFFF", 1), 0)]
        lines.append((algn, runs))
    wid = CX - lIns - rIns
    wrapped = []
    for algn, runs in lines:
        cur = []
        curw = 0
        for txt, sz, bold, col, spc in runs:
            words = txt.split(" ")
            for i, wd in enumerate(words):
                token = wd + (" " if i < len(words) - 1 else "")
                if not token:
                    continue
                tw = fnt(sz, bold).getlength(token) + spc * len(token)
                if curw + tw > wid and cur:
                    wrapped.append((algn, cur))
                    cur, curw = [], 0
                cur.append((token, sz, bold, col, spc))
                curw += tw
        wrapped.append((algn, cur))
    heights = []
    for para in body.findall("a:p", NS):
        pPr = para.find("a:pPr", NS)
        hgt = 0
        if pPr is not None:
            sp = pPr.find("a:lnSpc/a:spcPts", NS)
            if sp is not None:
                hgt = int(sp.get("val")) / 100.0 * PT
        heights.append(hgt)
    heights = [h if h > 0 else max([fnt(r[1], r[2]).getbbox("Hg")[3] for r in rs] or [12])
               for h, (_, rs) in zip(heights, wrapped)]
    heights = (heights + [12] * len(wrapped))[:len(wrapped)]
    total = sum(heights)
    ty = Y + tIns
    if anchor == "ctr":
        ty = Y + (CY - total) / 2
    elif anchor == "b":
        ty = Y + CY - bIns - total
    for (algn, rs), hh in zip(wrapped, heights):
        linew = sum(fnt(r[1], r[2]).getlength(r[0]) + r[4] * len(r[0]) for r in rs)
        tx = X + lIns
        if algn == "ctr":
            tx = X + (CX - linew) / 2
        elif algn == "r":
            tx = X + CX - rIns - linew
        for txt, sz, bold, col, spc in rs:
            f = fnt(sz, bold)
            d.text((tx, ty), txt, font=f, fill=col)
            tx += f.getlength(txt) + spc * len(txt)
        ty += hh * 1.0
        ty += 0


if __name__ == "__main__":
    path = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/pptx_prev"
    which = None
    if len(sys.argv) > 3:
        which = {int(x) for x in sys.argv[3].split(",")}
    ps = render(path, out, which)
    print("\n".join(ps))
