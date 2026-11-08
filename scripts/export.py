#!/usr/bin/env python3
"""CLI du Pack 1500.

Exemples
--------
  python scripts/export.py --catalogue
  python scripts/export.py --id T0001 --out ~/Bureau/mon-modele.pptx
  python scripts/export.py --all --zip            # les 1 500 .pptx dans un ZIP
  python scripts/export.py --all --zip --force    # régénère l'archive
  python scripts/export.py --apercu T0042 0       # écrit un SVG de contrôle
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import core.pack as pack  # noqa: E402  (initialise le chemin des modules internes)
from design_system import build_catalog_files, get_template  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Pack 1500 — générateur de templates PowerPoint")
    ap.add_argument("--catalogue", action="store_true", help="régénère catalog/templates.json et .csv")
    ap.add_argument("--id", help="identifiant d'un modèle (T0001 … T1500 ou 1 … 1500)")
    ap.add_argument("--out", help="chemin du .pptx pour --id")
    ap.add_argument("--all", action="store_true", help="génère le pack complet")
    ap.add_argument("--zip", action="store_true", help="produit l'archive ZIP (implique --all)")
    ap.add_argument("--force", action="store_true", help="régénère même si l'archive existe")
    ap.add_argument("--workers", type=int, default=None, help="nombre de processus")
    ap.add_argument("--apercu", nargs=2, metavar=("ID", "SLIDE"),
                    help="écrit un aperçu SVG (ex : --apercu T0042 0)")
    args = ap.parse_args()

    if not any((args.catalogue, args.id, args.all, args.zip, args.apercu)):
        args.catalogue = True
        args.all = True

    if args.catalogue:
        build_catalog_files()

    if args.id:
        t = get_template(args.id)
        out = Path(args.out).expanduser() if args.out else pack.CACHE / f"{t['id']}-{t['family']}.pptx"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(pack.deck_bytes(t))
        print(f"✓ {t['id']} · {t['name']} → {out}")

    if args.apercu:
        ident, slide = args.apercu
        svg = pack.thumb_svg(ident, int(slide))
        dest = ROOT / "dist" / f"apercu-{ident.upper()}-s{int(slide):02d}.svg"
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(svg, encoding="utf-8")
        print(f"✓ aperçu → {dest}")

    if args.all or args.zip:
        t0 = time.time()
        print(f"Génération de {pack.TOTAL} modèles PowerPoint (10 000 slides)…", flush=True)
        archive = pack.build_zip(workers=args.workers, force=args.force)
        size = archive.stat().st_size / 1024 / 1024
        print(f"✓ {archive} · {size:.1f} Mio · {time.time() - t0:.1f} s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
