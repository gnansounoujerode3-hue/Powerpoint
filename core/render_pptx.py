"""Rendu PowerPoint natif d'une scène.

Chaque primitive devient une forme / zone de texte PowerPoint éditable :
aucune image aplatie, aucun élément verrouillé.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE, PP_ALIGN
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Pt

import animation
import media
from design_system import W, H, filename_for
from scene import E, Ellipse, Line, PT_PER_UNIT, Picture, Rect, Scene, Text, Triangle, fit_font

_FILL_TAGS = ("a:noFill", "a:solidFill", "a:gradFill", "a:pattFill", "a:blipFill", "a:grpFill")


def _rgb(value: str) -> RGBColor:
    return RGBColor.from_string(value.lstrip("#").upper())


def _alpha(color_el, opacity: float) -> None:
    if color_el is None or opacity >= 1:
        return
    alpha = color_el.find(qn("a:alpha"))
    val = str(max(0, min(100000, int(opacity * 100000))))
    if alpha is None:
        color_el.append(parse_xml(f'<a:alpha {nsdecls("a")} val="{val}"/>'))
    else:
        alpha.set("val", val)


def _spPr(shape):
    return shape._element.spPr


def _apply_fill(shape, fill, opacity: float) -> None:
    if fill is None:
        shape.fill.background()
        return
    if isinstance(fill, dict):
        shape.fill.solid()  # crée un nœud correctement placé, que l'on remplace
        spPr = _spPr(shape)
        solid = spPr.find(qn("a:solidFill"))
        pos = list(spPr).index(solid)
        spPr.remove(solid)
        stops = "".join(
            f'<a:gs pos="{int(p * 100000)}"><a:srgbClr val="{c.lstrip("#").upper()}">'
            f'<a:alpha val="{int(max(0, min(1, opacity)) * 100000)}"/></a:srgbClr></a:gs>'
            for p, c in fill["stops"] if c
        )
        ang = int(fill.get("angle", 0) * 60000) % 21600000
        grad = parse_xml(
            f'<a:gradFill {nsdecls("a")} rotWithShape="1"><a:gsLst>{stops}</a:gsLst>'
            f'<a:lin ang="{ang}" scaled="1"/></a:gradFill>'
        )
        spPr.insert(pos, grad)
        return
    shape.fill.solid()
    shape.fill.fore_color.rgb = _rgb(fill)
    solid = _spPr(shape).find(qn("a:solidFill"))
    _alpha(solid.find(qn("a:srgbClr")) if solid is not None else None, opacity)


def _apply_line(shape, stroke: str | None, sw: float, opacity: float) -> None:
    if stroke is None:
        shape.line.fill.background()
        return
    shape.line.color.rgb = _rgb(stroke)
    shape.line.width = Pt(max(0.4, sw * PT_PER_UNIT))
    ln = _spPr(shape).find(qn("a:ln"))
    if ln is not None:
        solid = ln.find(qn("a:solidFill"))
        _alpha(solid.find(qn("a:srgbClr")) if solid is not None else None, opacity)


def _shape_for(slide, el):
    if isinstance(el, Ellipse):
        shape = slide.shapes.add_shape(MSO_SHAPE.OVAL, E(el.x), E(el.y), E(el.w), E(el.h))
    elif isinstance(el, Triangle):
        shape = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE,
                                       E(el.x), E(el.y), E(el.w), E(el.h))
    elif isinstance(el, Rect):
        kind = MSO_SHAPE.ROUNDED_RECTANGLE if el.radius > 0 else MSO_SHAPE.RECTANGLE
        shape = slide.shapes.add_shape(kind, E(el.x), E(el.y), E(el.w), E(el.h))
        if el.radius > 0:
            try:
                shape.adjustments[0] = min(0.5, el.radius / max(1, min(el.w, el.h)))
            except (IndexError, ValueError, AttributeError):
                pass
    else:
        return None
    _apply_fill(shape, el.fill, el.opacity)
    _apply_line(shape, getattr(el, "stroke", None), getattr(el, "sw", 1), el.opacity)
    if el.rotate:
        shape.rotation = el.rotate % 360
    return shape


def _picture_for(slide, el: Picture):
    """Insère une vraie image, recadrée sans déformation et remplaçable."""
    data, _mime, (nw, nh) = media.asset(el.key)
    pic = slide.shapes.add_picture(BytesIO(data), E(el.x), E(el.y), E(el.w), E(el.h))
    target = el.w / max(1, el.h)
    native = nw / max(1, nh)
    if native > target:
        half = (1 - target / native) / 2
        pic.crop_left, pic.crop_right = half, half
    else:
        half = (1 - native / target) / 2
        pic.crop_top, pic.crop_bottom = half, half
    prst = pic._element.spPr.find(qn("a:prstGeom"))
    if prst is not None and el.clip == "circle":
        prst.set("prst", "ellipse")
    elif prst is not None and el.clip == "round":
        prst.set("prst", "roundRect")
        try:
            pic.adjustments[0] = min(0.5, el.radius / max(1, min(el.w, el.h)))
        except (IndexError, ValueError, AttributeError):
            pass
    return pic


def _text_for(slide, t: dict, el: Text):
    box = slide.shapes.add_textbox(E(el.x), E(el.y), E(el.w), E(el.h))
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE,
                          "bottom": MSO_ANCHOR.BOTTOM}[el.valign]
    aligns = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
    family = fit_font(t, el.font)
    lines = el.text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = aligns[el.align]
        p.line_spacing = el.leading
        p.space_before = Pt(0)
        p.space_after = Pt(0)
        run = p.add_run()
        run.text = line.upper() if el.upper else line
        font = run.font
        font.name = family
        font.size = Pt(el.size * PT_PER_UNIT)
        font.bold = el.bold
        font.italic = el.italic
        font.color.rgb = _rgb(el.color)
        rPr = run._r.get_or_add_rPr()
        if el.opacity < 1:
            solid = rPr.find(qn("a:solidFill"))
            _alpha(solid.find(qn("a:srgbClr")) if solid is not None else None, el.opacity)
        if el.tracking:
            rPr.set("spc", str(int(el.tracking * PT_PER_UNIT * 100)))
    return box


def render_pptx(scenes: list[Scene], t: dict, path) -> Path | object:
    filelike = hasattr(path, "write")
    if not filelike:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
    prs = Presentation()
    prs.slide_width, prs.slide_height = E(W), E(H)
    blank = prs.slide_layouts[6]
    core = prs.core_properties
    core.title = f"{t['name']} — Pack 1500"
    core.subject = "Modèle de présentation premium entièrement modifiable"
    core.author = "Pack 1500 · Studio Design"
    core.keywords = f"PowerPoint, template, {t['family']}, {t['palette']}, {t['univers']}"
    core.comments = f"Modèle {t['id']} · 10 diapositives · 16:9 · généré par le Pack 1500"

    for slide_index, scene in enumerate(scenes):
        slide = prs.slides.add_slide(blank)
        if isinstance(scene.bg, dict):
            # dégradé de fond : une forme plein cadre, sans contour
            bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, E(W), E(H))
            _apply_fill(bg_shape, scene.bg, 1.0)
            bg_shape.line.fill.background()
        else:
            slide.background.fill.solid()
            slide.background.fill.fore_color.rgb = _rgb(scene.bg)
        anim_targets: list[tuple[int, int]] = []
        for el in scene.elements:
            shape = None
            if isinstance(el, Line):
                shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                                   E(el.x1), E(el.y1), E(el.x2), E(el.y2))
                _apply_line(shape, el.stroke, el.sw, el.opacity)
                if el.dash:
                    ln = _spPr(shape).find(qn("a:ln"))
                    if ln is not None:
                        ln.append(parse_xml(f'<a:prstDash {nsdecls("a")} val="dash"/>'))
            elif isinstance(el, Text):
                shape = _text_for(slide, t, el)
            elif isinstance(el, Picture):
                shape = _picture_for(slide, el)
            else:
                shape = _shape_for(slide, el)
            if shape is not None and getattr(el, "anim", 0):
                anim_targets.append((el.anim, shape.shape_id))
        animation.add_transition(slide, t, slide_index)
        animation.add_timing(slide, [sid for _, sid in sorted(anim_targets)])
        if scene.note:
            try:
                slide.notes_slide.notes_text_frame.text = scene.note
            except Exception:
                pass
    if filelike:
        prs.save(path)
        return path
    prs.save(str(path))
    return path


def render_deck(t: dict, path: str | Path) -> Path:
    from layouts import build_scenes
    return render_pptx(build_scenes(t), t, path)


def default_path(t: dict, root: str | Path = "dist/templates") -> Path:
    return Path(root) / filename_for(t)
