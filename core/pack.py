"""Construction du pack complet : 1 500 fichiers .pptx dans une archive ZIP."""
from __future__ import annotations

import io
import json
import os
import zipfile
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from design_system import ROOT, TEMPLATES, filename_for, get_template
from layouts import build_scene
from render_pptx import render_pptx
from render_svg import render_svg

DIST = ROOT / "dist"
CACHE = DIST / "cache"
ZIP_PATH = DIST / "Pack-1500-Templates-PowerPoint.zip"
STATUS_PATH = DIST / "pack-status.json"
TOTAL = len(TEMPLATES)
ZIP_ROOT = "Pack-1500-Templates-PowerPoint"


def deck_bytes(t: dict) -> bytes:
    buf = io.BytesIO()
    render_pptx([build_scene(t, i) for i in range(10)], t, buf)
    return buf.getvalue()


def ensure_deck(t: dict) -> Path:
    """Génère un .pptx à la demande et le met en cache."""
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / filename_for(t)
    if not path.exists() or path.stat().st_size < 1000:
        tmp = path.with_suffix(".tmp")
        tmp.write_bytes(deck_bytes(t))
        tmp.replace(path)
    return path


def _job(number: int) -> tuple[str, bytes]:
    from design_system import TEMPLATES  # propre à chaque processus
    t = TEMPLATES[number - 1]
    return filename_for(t), deck_bytes(t)


def _write_status(**data) -> None:
    DIST.mkdir(parents=True, exist_ok=True)
    payload = {
        "ready": False,
        "done": 0,
        "total": TOTAL,
        "stage": "waiting",
        "zip_bytes": 0,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    payload.update(data)
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def read_status() -> dict:
    if STATUS_PATH.exists():
        try:
            return json.loads(STATUS_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    ready = ZIP_PATH.exists() and ZIP_PATH.stat().st_size > 1_000_000
    return {"ready": ready, "done": TOTAL if ready else 0, "total": TOTAL,
            "stage": "ready" if ready else "waiting",
            "zip_bytes": ZIP_PATH.stat().st_size if ready else 0,
            "updated_at": ""}


def build_zip(workers: int | None = None, force: bool = False) -> Path:
    """Crée l'archive des 1 500 modèles (10 000 diapositives)."""
    DIST.mkdir(parents=True, exist_ok=True)
    if ZIP_PATH.exists() and not force:
        _write_status(ready=True, done=TOTAL, stage="ready",
                      zip_bytes=ZIP_PATH.stat().st_size)
        return ZIP_PATH
    tmp = ZIP_PATH.with_suffix(".part")
    if tmp.exists():
        tmp.unlink()
    _write_status(ready=False, done=0, stage="generation", zip_bytes=0)
    workers = workers or min(8, max(2, (os.cpu_count() or 4)))
    done = 0
    with zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr(f"{ZIP_ROOT}/LISEZ-MOI.txt", readme_text())
        zf.writestr(f"{ZIP_ROOT}/INDEX.csv", index_csv())
        with ProcessPoolExecutor(max_workers=workers) as pool:
            for name, data in pool.map(_job, range(1, TOTAL + 1), chunksize=4):
                zf.writestr(f"{ZIP_ROOT}/{name}", data)
                done += 1
                if done % 10 == 0 or done == TOTAL:
                    _write_status(ready=False, done=done, stage="generation",
                                  zip_bytes=tmp.stat().st_size)
    _write_status(ready=False, done=TOTAL, stage="compression",
                  zip_bytes=tmp.stat().st_size)
    tmp.replace(ZIP_PATH)
    _write_status(ready=True, done=TOTAL, stage="ready",
                  zip_bytes=ZIP_PATH.stat().st_size)
    return ZIP_PATH


def readme_text() -> str:
    return """PACK 1500 — TEMPLATES POWERPOINT PREMIUM
==========================================

1 500 modèles uniques · 10 diapositives chacun · 15 000 slides au total.
Format 16:9 (13,33 × 7,5 pouces). 100 % modifiables dans PowerPoint,
Keynote, Google Slides et LibreOffice Impress.

CONTENU
-------
· 1 500 fichiers .pptx (10 slides : couverture, sommaire, transition,
  vision, chiffres clés, données, processus, équipe, citation, clôture)
· INDEX.csv : la liste complète avec famille, palette, univers et mode
· Ce fichier

COMMENT UTILISER UN MODÈLE
--------------------------
1. Ouvrez le .pptx dans PowerPoint.
2. Remplacez « VOTRE MARQUE », les titres et les chiffres par les vôtres.
3. Modifiez les couleurs via Forme > Remplissage, ou directement avec
   les couleurs du thème (chaque modèle a sa propre palette).
4. Dupliquez les slides de transition pour ajouter des sections.
5. Chaque slide contient une note de présentation avec une astuce.

TOUS LES ÉLÉMENTS SONT ÉDITABLES
--------------------------------
Textes, formes, graphiques, dégradés et notes sont natifs : aucune image
aplatie, aucun élément verrouillé, aucune police exotique requise.

Les 30 familles graphiques × 50 palettes sont décrites dans le dépôt :
core/design_system.py. Vous pouvez régénérer ou personnaliser le pack
avec : python scripts/export.py --all --zip

Designs originaux générés par code — utilisation libre, personnelle
et commerciale, sans attribution obligatoire.

Bonnes présentations !
"""


def index_csv() -> str:
    import csv
    import io as _io
    buf = _io.StringIO()
    w = csv.writer(buf)
    w.writerow(["ID", "Nom", "Famille", "Palette", "Univers", "Mode", "Motif",
                "Typographie", "Archetype", "Fichier"])
    for t in TEMPLATES:
        w.writerow([t["id"], t["name"], t["family"], t["palette"], t["univers"],
                    t["mode"], t["motif"], t["typo_label"], t["archetype"],
                    filename_for(t)])
    return "\ufeff" + buf.getvalue()


def thumb_svg(identifier: str | int, slide: int = 0) -> str:
    t = get_template(identifier)
    return render_svg(build_scene(t, slide), t)
