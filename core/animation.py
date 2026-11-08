"""Animations PowerPoint natives (OOXML).

Deux niveaux, sans aucune image aplatie ni macro :
  1. Transitions de diapositive propres à chaque famille graphique.
  2. Séquence d'apparitions en fondu, décalées, sur les éléments clés
     (titres, cartes, images) : clic pour lancer, puis enchaînement auto.

Le XML est injecté directement dans <p:sld> car python-pptx n'expose pas
le modèle d'animations. Les nœuds sont ceux générés par PowerPoint lui-même.
"""
from __future__ import annotations

from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn

# (élément de transition, attributs) — tous dans le namespace ECMA-376 standard
TRANSITIONS = {
    "centred": ("fade", {}),
    "split": ("push", {"dir": "l"}),
    "frame": ("fade", {}),
    "fullbleed": ("dissolve", {}),
    "sidebar": ("wipe", {"dir": "r"}),
    "grid": ("checker", {"dir": "horz"}),
    "asymmetric": ("split", {"dir": "in", "orient": "horz"}),
    "editorial": ("fade", {}),
    "stacked": ("cover", {"dir": "u"}),
    "diagonal": ("push", {"dir": "u"}),
}

_FADE_DURATION = 550      # ms
_STAGGER = 190            # ms entre deux apparitions


def add_transition(slide, t: dict, index: int) -> None:
    kind, attrs = TRANSITIONS.get(t["archetype"], ("fade", {}))
    if index == 2:
        kind, attrs = "dissolve", {}
    if index == 9:
        kind, attrs = "fade", {}
    child = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    xml = (f'<p:transition {nsdecls("p")} spd="med" advClick="1">'
           f'<p:{kind} {child}/></p:transition>')
    el = parse_xml(xml)
    root = slide._element
    old = root.find(qn("p:transition"))
    if old is not None:
        root.remove(old)
    # ordre imposé : cSld, clrMapOvr, transition, timing, extLst
    timing = root.find(qn("p:timing"))
    if timing is not None:
        root.insert(list(root).index(timing), el)
    else:
        root.append(el)


def _fade_effect(spid: int, delay: int, node_type: str, counter: list[int]) -> str:
    def nid() -> int:
        counter[0] += 1
        return counter[0]

    ctn, set_id, eff_id = nid(), nid(), nid()
    return f"""<p:par>
  <p:cTn id="{ctn}" presetID="10" presetClass="entr" presetSubtype="0"
         fill="hold" grpId="0" nodeType="{node_type}">
    <p:stCondLst><p:cond delay="{delay}"/></p:stCondLst>
    <p:childTnLst>
      <p:set>
        <p:cBhvr>
          <p:cTn id="{set_id}" dur="1" fill="hold">
            <p:stCondLst><p:cond delay="0"/></p:stCondLst>
          </p:cTn>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
          <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
        </p:cBhvr>
        <p:to><p:strVal val="visible"/></p:to>
      </p:set>
      <p:animEffect transition="in" filter="fade">
        <p:cBhvr>
          <p:cTn id="{eff_id}" dur="{_FADE_DURATION}"/>
          <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
        </p:cBhvr>
      </p:animEffect>
    </p:childTnLst>
  </p:cTn>
</p:par>"""


def add_timing(slide, shape_ids: list[int]) -> None:
    """Séquence de fondus : 1er élément au clic, les autres automatiquement."""
    if not shape_ids:
        return
    counter = [4]  # ids 1..4 réservés à l'ossature
    effects = []
    for i, spid in enumerate(shape_ids):
        node = "clickEffect" if i == 0 else "afterEffect"
        delay = 0 if i == 0 else _STAGGER
        effects.append(_fade_effect(int(spid), delay, node, counter))

    xml = f"""<p:timing {nsdecls("p")}>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold">
                          <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                          <p:childTnLst>
                            {''.join(effects)}
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>
              </p:childTnLst>
            </p:cTn>
            <p:prevCondLst>
              <p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
            </p:prevCondLst>
            <p:nextCondLst>
              <p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>
            </p:nextCondLst>
          </p:seq>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>"""
    el = parse_xml(xml)
    root = slide._element
    old = root.find(qn("p:timing"))
    if old is not None:
        root.remove(old)
    root.append(el)
