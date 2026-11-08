#!/usr/bin/env python3
"""Serveur de la galerie Pack 1500 (bibliothèque standard uniquement).

Routes
------
  /                         galerie
  /api/catalog              les 1 500 modèles (JSON)
  /api/thumb/T0001.svg?slide=0   aperçu vectoriel fidèle
  /api/download/T0001.pptx un .pptx généré à la demande
  /api/pack/status          avancement de l'archive complète
  /api/pack                 l'archive ZIP des 1 500 .pptx
"""
from __future__ import annotations

import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
from collections import OrderedDict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))

import core.pack as pack  # noqa: E402
from design_system import get_template  # noqa: E402

WEB = ROOT / "web"
CATALOG = ROOT / "catalog" / "templates.json"
PORT = int(os.environ.get("PORT", "8000"))

THUMB_CACHE: OrderedDict[tuple[str, int], str] = OrderedDict()
THUMB_LOCK = threading.Lock()
THUMB_MAX = 600
CATALOG_CACHE: bytes | None = None
PACK_LOCK = threading.Lock()

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/zip", ".zip")


def start_pack_if_needed() -> None:
    with PACK_LOCK:
        status = pack.read_status()
        if status["ready"] or status["stage"] in ("generation", "compression"):
            return
        log = open(pack.DIST / "export.log", "ab", buffering=0)
        subprocess.Popen(
            [sys.executable, str(ROOT / "scripts" / "export.py"), "--all", "--zip"],
            cwd=str(ROOT), stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
        )
        pack._write_status(ready=False, done=0, stage="generation")


def thumbnail(identifier: str, slide: int) -> str:
    key = (identifier.upper(), slide)
    with THUMB_LOCK:
        if key in THUMB_CACHE:
            THUMB_CACHE.move_to_end(key)
            return THUMB_CACHE[key]
    svg = pack.thumb_svg(identifier, slide)
    with THUMB_LOCK:
        THUMB_CACHE[key] = svg
        if len(THUMB_CACHE) > THUMB_MAX:
            THUMB_CACHE.popitem(last=False)
    return svg


class Handler(BaseHTTPRequestHandler):
    server_version = "Pack1500/1.0"

    # ------------------------------------------------------------------ utils
    def _send(self, code: int, body: bytes, ctype: str, extra: dict | None = None) -> None:
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Access-Control-Allow-Origin", "*")
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _json(self, obj, code: int = 200) -> None:
        self._send(code, json.dumps(obj, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8")

    def _file(self, path: Path, ctype: str, attachment: str | None = None) -> None:
        if not path.exists():
            self._json({"error": "Fichier introuvable"}, 404)
            return
        size = path.stat().st_size
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(size))
        self.send_header("Accept-Ranges", "none")
        if attachment:
            self.send_header("Content-Disposition", f'attachment; filename="{attachment}"')
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        if self.command == "HEAD":
            return
        with path.open("rb") as fh:
            while True:
                chunk = fh.read(1024 * 1024)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return

    def log_message(self, fmt: str, *args) -> None:
        if os.environ.get("PACK_VERBOSE"):
            super().log_message(fmt, *args)

    # ------------------------------------------------------------- dispatch
    def do_HEAD(self) -> None:
        self.do_GET()

    def do_GET(self) -> None:
        url = urlparse(self.path)
        path = url.path
        query = parse_qs(url.query)
        try:
            if path.startswith("/api/"):
                self._api(path, query)
            else:
                self._static(path)
        except (BrokenPipeError, ConnectionResetError):
            return
        except Exception as exc:  # évite de tuer le thread sur une mauvaise requête
            self._json({"error": str(exc)}, 500)

    # ----------------------------------------------------------------- API
    def _api(self, path: str, query: dict) -> None:
        global CATALOG_CACHE
        if path == "/api/health":
            self._json({"ok": True, "total": pack.TOTAL, "version": "1.0.0"})
            return

        if path == "/api/catalog":
            if CATALOG_CACHE is None:
                CATALOG_CACHE = CATALOG.read_bytes()
            self._send(200, CATALOG_CACHE, "application/json; charset=utf-8",
                       {"Cache-Control": "public, max-age=300"})
            return

        m = re.fullmatch(r"/api/thumb/(T?\d{1,4})\.svg", path)
        if m:
            slide = int(query.get("slide", ["0"])[0])
            slide = max(0, min(9, slide))
            svg = thumbnail(m.group(1), slide)
            self._send(200, svg.encode("utf-8"), "image/svg+xml; charset=utf-8",
                       {"Cache-Control": "public, max-age=86400"})
            return

        m = re.fullmatch(r"/api/download/(T?\d{1,4})\.pptx", path)
        if m:
            t = get_template(m.group(1))
            file = pack.ensure_deck(t)
            from design_system import filename_for
            self._file(file, "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                       filename_for(t))
            return

        if path == "/api/pack/status":
            status = pack.read_status()
            status["started"] = status["stage"] in ("generation", "compression")
            status["percent"] = round(100 * status["done"] / pack.TOTAL, 1)
            self._json(status)
            return

        if path == "/api/pack/start":
            start_pack_if_needed()
            self._json({"started": True, "status": pack.read_status()})
            return

        if path == "/api/pack":
            status = pack.read_status()
            if not status["ready"]:
                start_pack_if_needed()
                self._json({"ready": False, "message": "Le pack est en cours de génération",
                            "status": status}, 202)
                return
            self._file(pack.ZIP_PATH, "application/zip", pack.ZIP_PATH.name)
            return

        self._json({"error": "Route inconnue"}, 404)

    # -------------------------------------------------------------- static
    def _static(self, path: str) -> None:
        rel = "index.html" if path in ("/", "") else path.lstrip("/")
        target = (WEB / rel).resolve()
        if not str(target).startswith(str(WEB.resolve())) or not target.is_file():
            self._send(404, b"<h1>404</h1>", "text/html; charset=utf-8")
            return
        ctype = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "image/svg+xml"):
            ctype += "; charset=utf-8"
        self._file(target, ctype)


def main() -> None:
    if not CATALOG.exists():
        from design_system import build_catalog_files
        build_catalog_files()
    start_pack_if_needed()
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    print(f"Pack 1500 — galerie sur http://0.0.0.0:{PORT} ({pack.TOTAL} modèles)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
