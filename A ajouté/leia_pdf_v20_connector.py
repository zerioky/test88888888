#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leia_pdf_v20_connector.py — Connecteur PDF V20 minimal
═══════════════════════════════════════════════════════
Wrappe LeiaPurePDFReader (natif, zéro dépendance) avec :
  SemanticCortex → CognitiveStructure → workspace.ingest_structure()

Pas besoin de modifier le fichier original. Ce connecteur est autonome.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

# Import du parseur natif
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

try:
    from leia_pure_pdf_reader import LeiaPurePDFReader, PDFDocument, PDFContentParser, PDFFont
    _READER_OK = True
except Exception:
    LeiaPurePDFReader = None  # type: ignore
    _READER_OK = False

try:
    from semantic_cortex import SemanticCortex
    _CORTEX_OK = True
except Exception:
    SemanticCortex = None  # type: ignore
    _CORTEX_OK = False

ProgressCallback = Callable[[str], None]


class LeiaPDFV20Connector:
    """
    Lecteur PDF V20 — parseur natif + pipeline SemanticCortex + workspace.
    Zéro dépendance externe.
    """

    def __init__(
        self,
        cortex: Any = None,
        workspace: Any = None,
        progress_callback: Optional[ProgressCallback] = None,
        max_chars_per_chunk: int = 1800,
        pause_between_chunks: float = 0.003,
    ):
        self.cortex = cortex
        self.workspace = workspace
        self.progress_callback = progress_callback
        self.max_chars_per_chunk = max(500, int(max_chars_per_chunk or 1800))
        self.pause_between_chunks = max(0.0, float(pause_between_chunks or 0.0))
        self.cancel_requested = False

    def set_progress_callback(self, cb: Optional[ProgressCallback]) -> None:
        self.progress_callback = cb

    def request_cancel(self) -> None:
        self.cancel_requested = True

    def _log(self, message: str) -> None:
        msg = f"[PDF-V20] {message}"
        try:
            print(msg, flush=True)
        except Exception:
            pass
        if self.progress_callback:
            try:
                self.progress_callback(msg)
            except Exception:
                pass

    def load_pdf_book(
        self,
        path: str,
        progress_callback: Optional[ProgressCallback] = None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
    ) -> Dict[str, Any]:
        """Pipeline PDF natif → cortex → workspace."""
        if not _READER_OK:
            return {"ok": False, "error": "leia_pure_pdf_reader non disponible"}

        if progress_callback is not None:
            self.progress_callback = progress_callback
        self.cancel_requested = False

        path_obj = Path(path).expanduser()
        if not path_obj.exists():
            return {"ok": False, "error": f"Fichier introuvable : {path}"}

        self._log(f"ouverture : {path_obj} ({path_obj.stat().st_size:,} octets)")

        try:
            raw = path_obj.read_bytes()
        except Exception as exc:
            return {"ok": False, "error": f"Lecture impossible : {exc}"}

        if not raw.startswith(b"%PDF"):
            return {"ok": False, "error": "Header %PDF absent"}

        try:
            doc = PDFDocument(raw)
        except Exception as exc:
            return {"ok": False, "error": f"Parsing PDF : {exc}"}

        if doc.encrypted:
            return {"ok": False, "error": "PDF chiffré — non supporté"}

        try:
            pages = doc.get_pages()
        except Exception as exc:
            return {"ok": False, "error": f"Accès pages : {exc}"}

        total_pages = len(pages)
        if total_pages == 0:
            return {"ok": False, "error": "Aucune page"}

        start_page = max(1, int(start_page or 1))
        end_page = total_pages if max_pages is None else min(total_pages, start_page + max(1, int(max_pages)) - 1)

        self._log(f"{total_pages} pages — lecture {start_page} à {end_page}")

        pages_read = 0
        chunks_done = 0
        cognitive_structures = 0
        workspace_integrations = 0
        errors: List[str] = []
        preview: List[Dict[str, Any]] = []
        PREVIEW_LIMIT = 16

        for page_num in range(start_page, end_page + 1):
            if self.cancel_requested:
                self._log("annulation")
                break

            self._log(f"extraction page {page_num}/{total_pages}")
            page = pages[page_num - 1]

            try:
                raw_fonts = doc.get_page_fonts(page)
                fonts = {}
                for alias, fd in raw_fonts.items():
                    try:
                        fonts[alias] = PDFFont(fd, doc)
                    except Exception:
                        pass
                streams = doc.get_page_content_streams(page)
                text = PDFContentParser(doc, fonts).extract(streams).strip()
            except Exception as exc:
                errors.append(f"page {page_num}: {exc}")
                self._log(f"erreur page {page_num}: {exc}")
                continue

            if not text:
                self._log(f"page {page_num}: vide")
                continue

            pages_read += 1
            fragments = self._split_text(text)
            self._log(f"page {page_num}: {len(fragments)} fragment(s)")

            for frag_idx, fragment in enumerate(fragments, 1):
                if self.cancel_requested:
                    break

                self._log(f"compréhension p{page_num} f{frag_idx}/{len(fragments)}")

                # Passe par SemanticCortex
                cs_obj = None
                cs_dict: Dict[str, Any] = {"available": False}
                if self.cortex is not None:
                    try:
                        cs_obj = self.cortex.process(fragment, source=path_obj.name)
                        if hasattr(cs_obj, "to_dict"):
                            cs_dict = cs_obj.to_dict()
                        cs_dict["available"] = True
                        cognitive_structures += 1
                    except Exception as exc:
                        cs_dict = {"available": False, "error": str(exc)}

                # Injecte dans workspace
                if self.workspace is not None and cs_obj is not None:
                    try:
                        ingest = getattr(self.workspace, "ingest_structure", None)
                        if callable(ingest):
                            ingest(cs_obj, source=path_obj.name)
                            workspace_integrations += 1
                        else:
                            inject = getattr(self.workspace, "inject_perception", None)
                            if callable(inject):
                                inject({"text": fragment, "source": path_obj.name, "page": page_num, "available": True})
                                workspace_integrations += 1
                    except Exception as exc:
                        errors.append(f"workspace p{page_num}: {exc}")

                chunks_done += 1
                if len(preview) < PREVIEW_LIMIT:
                    preview.append({
                        "page": page_num, "fragment": frag_idx,
                        "text_preview": fragment[:240],
                        "cognitive_structure": cs_dict,
                        "workspace_ingested": workspace_integrations > 0,
                    })

                if self.pause_between_chunks:
                    time.sleep(self.pause_between_chunks)

        # Tick post-lecture
        if self.workspace is not None:
            try:
                tick = getattr(self.workspace, "tick", None)
                if callable(tick):
                    tick(elapsed=10.0)
            except Exception:
                pass

        self._log(f"terminé: {pages_read} pages, {chunks_done} fragments, {cognitive_structures} structures, {workspace_integrations} intégrations")

        return {
            "ok": True,
            "success": True,
            "file": str(path_obj),
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page,
            "pages_read": pages_read,
            "chunks_count": chunks_done,
            "cognitive_structures": cognitive_structures,
            "workspace_integrations": workspace_integrations,
            "errors": errors,
            "traces_preview": preview,
            "reader": "LeiaPDFV20Connector (natif, zéro dépendance)",
            "pipeline": "PDF natif → SemanticCortex → workspace.ingest_structure",
        }

    def _split_text(self, text: str) -> List[str]:
        text = " ".join((text or "").split())
        if not text:
            return []
        chunks = []
        start = 0
        n = len(text)
        while start < n:
            end = min(n, start + self.max_chars_per_chunk)
            if end < n:
                boundaries = [
                    text.rfind(". ", start, end),
                    text.rfind("? ", start, end),
                    text.rfind("! ", start, end),
                    text.rfind("; ", start, end),
                ]
                boundary = max(boundaries)
                if boundary > start + 350:
                    end = boundary + 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end <= start:
                break
            start = end
        return chunks

    def get_info(self, path: str) -> Dict[str, Any]:
        if LeiaPurePDFReader is None:
            return {"ok": False, "error": "LeiaPurePDFReader non disponible"}
        result = LeiaPurePDFReader.get_info(path)
        result["ok"] = result.get("success", False)
        return result

    def extract_text_only(self, path: str) -> Dict[str, Any]:
        if LeiaPurePDFReader is None:
            return {"ok": False, "error": "LeiaPurePDFReader non disponible"}
        return LeiaPurePDFReader.extract_text_only(path)
