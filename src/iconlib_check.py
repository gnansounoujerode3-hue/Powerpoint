"""Validation des noms d'icônes utilisés par les layouts."""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iconlib import has_icon, ICON_NAMES  # noqa

SRC = os.path.dirname(os.path.abspath(__file__))


def used():
    names = set()
    for root, _, files in os.walk(os.path.join(SRC, "layouts")):
        for f in files:
            if f.endswith(".py"):
                s = open(os.path.join(root, f), encoding="utf-8").read()
                for m in re.findall(r"""icon_paths\([^,]+,\s*["']([a-z0-9-]+)["']""", s):
                    names.add(m)
                for m in re.findall(r"""icon(?:_name)?\s*=\s*["']([a-z0-9-]+)["']""", s):
                    names.add(m)
                for m in re.findall(r"""["']icon["']\s*:\s*["']([a-z0-9-]+)["']""", s):
                    names.add(m)
    return names


if __name__ == "__main__":
    u = used()
    bad = sorted(n for n in u if not has_icon(n))
    print(f"{len(u)} icônes référencées, {len(bad)} inconnues")
    for b in bad:
        print("  !", b)
    if bad and len(sys.argv) > 1:
        cand = [n for n in ICON_NAMES if bad[0].split("-")[0] in n][:15]
        print("proches de", bad[0], cand)
