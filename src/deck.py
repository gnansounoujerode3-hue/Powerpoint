"""Construction du fichier PPTX : master, thème, polices embarquées, animations."""
from __future__ import annotations

import os
import re
import zipfile
from io import BytesIO

from lxml import etree
from pptx import Presentation
from pptx.opc.package import Part
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn
from pptx.util import Emu

import emit_pptx
import theme
from theme import SLIDE_H_IN, SLIDE_W_IN

FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "fonts")
FONT_FILES = {"regular": "Poppins-400.ttf", "bold": "Poppins-700.ttf"}
FONT_RT = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"


def new_presentation():
    prs = Presentation()
    prs.slide_width = Emu(int(SLIDE_W_IN * 914400))
    prs.slide_height = Emu(int(SLIDE_H_IN * 914400))
    lst = prs.slides._sldIdLst
    for sld in list(lst):
        rId = sld.get(qn("r:id"))
        prs.part.drop_rel(rId)
        lst.remove(sld)
    _set_theme_fonts(prs)
    return prs


def _set_theme_fonts(prs):
    part = prs.slide_master.part
    for rel in part.rels.values():
        if "theme" in rel.reltype:
            tp = rel.target_part
            xml = tp.blob.decode("utf-8")
            xml = xml.replace('typeface="Calibri Light"', 'typeface="Poppins"')
            xml = xml.replace('typeface="Calibri"', 'typeface="Poppins"')
            tp._blob = xml.encode("utf-8")
            break


def embed_fonts(prs):
    """Embarque Poppins (regular + bold) : rendu identique sur toute machine."""
    pres_part = prs.part
    pres_el = pres_part._element
    if pres_el.find(qn("p:embeddedFontLst")) is not None:
        return
    lst = etree.Element(qn("p:embeddedFontLst"))
    dts = pres_el.find(qn("p:defaultTextStyle"))
    if dts is not None:
        dts.addprevious(lst)
    else:
        pres_el.append(lst)
    ef = etree.SubElement(lst, qn("p:embeddedFont"))
    f = etree.SubElement(ef, qn("p:font"))
    f.set("typeface", "Poppins")
    f.set("pitchFamily", "34")
    f.set("charset", "-122")
    idx = 1
    for tag, key in (("p:regular", "regular"), ("p:bold", "bold")):
        path = os.path.join(FONT_DIR, FONT_FILES[key])
        if not os.path.exists(path):
            continue
        with open(path, "rb") as fh:
            blob = fh.read()
        uri = PackURI("/ppt/fonts/font%d.fntdata" % idx)
        idx += 1
        part = Part(uri, "application/x-fontdata", package=pres_part.package)
        part._blob = blob
        rId = pres_part.relate_to(part, FONT_RT)
        el = etree.SubElement(ef, qn(tag))
        el.set(qn("r:id"), rId)


def add_slide(prs, bg_colors=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    if bg_colors:
        emit_pptx.set_slide_bg(slide, bg_colors)
    return slide


def emit_nodes(slide, nodes):
    em = emit_pptx.PPTXEmitter(slide)
    em.emit(nodes)
    return em


def save(prs, path, embed=True, animate=True):
    if embed:
        try:
            embed_fonts(prs)
        except Exception as e:          # l'embarquement ne doit jamais bloquer
            print("  ! polices non embarquées :", e)
    if animate:
        _ensure_embedded_flag(prs, embed)
    prs.save(path)


def _ensure_embedded_flag(prs, embed):
    """Ajoute <p:presentationPr> avec les options d'animation si absent."""
    pres_el = prs.part._element
    pr = pres_el.find(qn("p:presentationPr"))
    if pr is not None:
        return
    pr = etree.SubElement(pres_el, qn("p:presentationPr"))
    shows = etree.SubElement(pr, "{http://schemas.openxmlformats.org/presentationml/2006/main}showPr")
    shows.set("useTimings", "1")


def save_static(src, dst, embed=True):
    """Ré-emballe un pptx en retirant toutes les animations (version « statique »)."""
    import re as _re
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if _re.match(r"ppt/slides/slide\d+\.xml$", item.filename):
                txt = data.decode("utf-8")
                txt = _re.sub(r"<p:timing>.*?</p:timing>", "", txt, flags=_re.S)
                txt = _re.sub(r"<p:bldLst>.*?</p:bldLst>", "", txt, flags=_re.S)
                data = txt.encode("utf-8")
            elif item.filename == "ppt/presentation.xml":
                txt = data.decode("utf-8")
                txt = _re.sub(r"<p:embeddedFontLst>.*?</p:embeddedFontLst>", "", txt, flags=_re.S)
                data = txt.encode("utf-8")
            elif item.filename.startswith("ppt/fonts/") and not embed:
                continue
            zout.writestr(item, data)


def slide_count(path):
    with zipfile.ZipFile(path) as z:
        return len([n for n in z.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", n)])
