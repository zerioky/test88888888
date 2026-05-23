from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional
from dataclasses import asdict, is_dataclass

# ── Lecteur PDF : natif en priorité, pypdf en fallback ──────────────────────
# On essaie d'abord le lecteur 100% natif (zéro dépendance)
try:
    from leia_pure_pdf_reader import LeiaPurePDFReader as _NativeReader
    _NATIVE_AVAILABLE = True
except Exception:
    _NativeReader = None
    _NATIVE_AVAILABLE = False

# Fallback : pypdf ou PyPDF2

try:
    from leia_spacy_engine import engine as nlp_engine
except Exception:
    nlp_engine = None


PdfReader = None
if not _NATIVE_AVAILABLE:
    try:
        from pypdf import PdfReader
    except Exception:
        try:
            from PyPDF2 import PdfReader
        except Exception:
            PdfReader = None

ProgressCallback = Callable[[str], None]


class LeiaPDFKnowledgeEngine:
    """
    Lecture PDF progressive pour Leia.
    Utilise automatiquement le lecteur natif (leia_pure_pdf_reader) si disponible,
    sinon pypdf/PyPDF2. Zéro dépendance externe si leia_pure_pdf_reader.py est présent.
    """

    def __init__(
        self,
        memory_system: Any = None,
        digestion_engine: Any = None,
        progress_callback: Optional[ProgressCallback] = None,
        max_chars_per_chunk: int = 1800,
        pause_between_chunks: float = 0.005,
    ) -> None:
        self.memory_system = memory_system
        self.digestion_engine = digestion_engine
        self.progress_callback = progress_callback
        self.max_chars_per_chunk = max(500, int(max_chars_per_chunk or 1800))
        self.pause_between_chunks = max(0.0, float(pause_between_chunks or 0.0))
        self.cancel_requested = False

        # Instancie le lecteur natif si disponible
        if _NATIVE_AVAILABLE and _NativeReader is not None:
            self._native = _NativeReader(
                memory_system=memory_system,
                digestion_engine=digestion_engine,
                progress_callback=progress_callback,
                max_chars_per_chunk=max_chars_per_chunk,
                pause_between_chunks=pause_between_chunks,
            )
        else:
            self._native = None

    def set_progress_callback(self, callback: Optional[ProgressCallback]) -> None:
        self.progress_callback = callback
        if self._native is not None:
            self._native.progress_callback = callback

    def request_cancel(self) -> None:
        self.cancel_requested = True
        if self._native is not None:
            self._native.cancel_requested = True

    def _log(self, message: str) -> None:
        msg = f"[PDF] {message}"
        try:
            print(msg, flush=True)
        except Exception:
            pass
        if self.progress_callback:
            try:
                self.progress_callback(msg)
            except Exception:
                pass

    def read_pdf(
        self,
        pdf_path: str,
        *,
        progress_callback: Optional[ProgressCallback] = None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
        preview_limit: int = 20,
    ) -> Dict[str, Any]:
        """Point d'entrée principal — délègue au lecteur natif si dispo."""

        if progress_callback is not None:
            self.set_progress_callback(progress_callback)

        # ── Lecteur natif (zéro dépendance) ──────────────────────────────
        if self._native is not None:
            self._log("Utilisation du lecteur PDF natif (zéro dépendance)")
            self._native.memory_system = self.memory_system
            self._native.digestion_engine = self.digestion_engine
            return self._native.read_pdf(
                pdf_path,
                progress_callback=self.progress_callback,
                max_pages=max_pages,
                start_page=start_page,
                preview_limit=preview_limit,
            )

        # ── Fallback : pypdf / PyPDF2 ─────────────────────────────────────
        if PdfReader is None:
            return {
                "success": False,
                "error": (
                    "Aucun lecteur PDF disponible.\n"
                    "→ Solution 1 : placer leia_pure_pdf_reader.py dans le dossier connaissance/\n"
                    "→ Solution 2 : pip install pypdf"
                ),
            }

        return self._read_with_pypdf(pdf_path, max_pages=max_pages, start_page=start_page)

    def _read_with_pypdf(
        self,
        pdf_path: str,
        max_pages: Optional[int] = None,
        start_page: int = 1,
    ) -> Dict[str, Any]:
        """Lecture via pypdf/PyPDF2 (fallback)."""
        self.cancel_requested = False
        path = Path(pdf_path).expanduser()

        if not path.exists():
            return {"success": False, "error": f"Fichier introuvable: {path}"}

        try:
            reader = PdfReader(str(path))
        except Exception as exc:
            return {"success": False, "error": f"Impossible d'ouvrir: {exc}"}

        total_pages = len(reader.pages)
        start_page = max(1, int(start_page or 1))
        end_page = total_pages if max_pages is None else min(total_pages, start_page + max_pages - 1)

        self._log(f"{total_pages} pages. Lecture {start_page} → {end_page}.")

        pages_read = 0
        chunks_created = 0
        memory_traces = 0
        errors: List[str] = []
        preview: List[Dict[str, Any]] = []

        for page_number in range(start_page, end_page + 1):
            if self.cancel_requested:
                break

            self._log(f"page {page_number}/{total_pages}")

            try:
                page = reader.pages[page_number - 1]
                text = page.extract_text() or ""
            except Exception as exc:
                errors.append(f"page {page_number}: {exc}")
                continue

            text = text.strip()
            if not text:
                continue

            pages_read += 1
            fragments = self._split_text(text)

            for chunk_index, fragment in enumerate(fragments, 1):
                if self.cancel_requested:
                    break

                self._log(f"digestion page {page_number}, fragment {chunk_index}/{len(fragments)}")
                digestion = self._call_digestion(fragment, page_number, chunk_index)

                trace = {
                    "type": "pdf_knowledge",
                    "source_file": path.name,
                    "source_path": str(path),
                    "page": page_number,
                    "chunk_index": chunk_index,
                    "text": fragment,
                    "digestion": digestion,
                    "created_at": time.time(),
                }

                stored = self._store_memory(trace)
                if stored:
                    memory_traces += 1
                chunks_created += 1

                if len(preview) < 20:
                    preview.append({
                        "page": page_number,
                        "chunk_index": chunk_index,
                        "text_preview": fragment[:260],
                        "digestion": digestion,
                        "stored": stored,
                    })

                if self.pause_between_chunks:
                    time.sleep(self.pause_between_chunks)

        conceptual_synthesis: Dict[str, Any] = {"available": False}
        if self.digestion_engine is not None:
            build = getattr(self.digestion_engine, "build_conceptual_synthesis", None)
            if callable(build):
                try:
                    conceptual_synthesis = build(
                        context_text=path.stem,
                        source_hint=str(path),
                        limit=14,
                    )
                except Exception as exc:
                    conceptual_synthesis = {"available": False, "error": str(exc)}

        self._log(f"terminé: {pages_read} pages, {chunks_created} fragments, {memory_traces} traces")

        return {
            "success": True,
            "file": str(path),
            "total_pages": total_pages,
            "pages_read": pages_read,
            "chunks_count": chunks_created,
            "memory_traces": memory_traces,
            "conceptual_synthesis": conceptual_synthesis,
            "errors": errors,
            "traces_preview": preview,
            "reader": "pypdf/PyPDF2 (fallback)",
        }

    # ── Méthodes internes (utilisées par _read_with_pypdf) ────────────────────

    def _split_text(self, text: str) -> List[str]:
        text = " ".join((text or "").split())

        if not text:
            return []

        # Nouveau système NLP vivant
        if nlp_engine:
            try:
                segments = nlp_engine.segment_text(
                    text,
                    self.max_chars_per_chunk
                )

                cleaned = [
                    s.strip()
                    for s in segments
                    if s and s.strip()
                ]

                if cleaned:
                    return cleaned

            except Exception:
                pass

        # Fallback ancien système
        chunks: List[str] = []

        start = 0
        n = len(text)

        while start < n:
            end = min(n, start + self.max_chars_per_chunk)

            if end < n:
                boundary = max(
                    text.rfind(". ", start, end),
                    text.rfind("? ", start, end),
                    text.rfind("! ", start, end),
                    text.rfind("; ", start, end),
                    text.rfind(": ", start, end),
                )

                if boundary > start + 350:
                    end = boundary + 1

            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            if end <= start:
                break

            start = end

        return chunks

    def _jsonable(self, value: Any, depth: int = 0) -> Any:
        if depth > 6:
            return str(value)[:500]
        if is_dataclass(value):
            try:
                return self._jsonable(asdict(value), depth + 1)
            except Exception:
                return str(value)[:500]
        if isinstance(value, Mapping):
            return {str(k): self._jsonable(v, depth + 1) for k, v in value.items()}
        if isinstance(value, (list, tuple, set)):
            return [self._jsonable(v, depth + 1) for v in list(value)[:80]]
        if isinstance(value, (str, int, float, bool)) or value is None:
            return value
        return str(value)[:500]

    def _digestion_counts(self, digestion: Mapping[str, Any]) -> Dict[str, int]:
        traces = digestion.get("traces", []) if isinstance(digestion, Mapping) else []
        return {
            "traces": len(traces) if isinstance(traces, list) else 0,
            "atoms": int(digestion.get("atoms_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "neurons_created": int(digestion.get("neurons_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "neurons_reinforced": int(digestion.get("neurons_reinforced", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "links_created": int(digestion.get("links_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
        }

    def _call_digestion(self, text: str, page: int, chunk_index: int) -> Dict[str, Any]:
        if not self.digestion_engine:
            return {"available": False, "resonance": 0.0, "curiosity": 0.0, "friction": 0.0}
        payload = {"text": text, "page": page, "chunk_index": chunk_index, "source": "pdf"}
        for name in ("digest_text", "digest", "process_text", "ingest_text", "digest_knowledge", "learn_text"):
            fn = getattr(self.digestion_engine, name, None)
            if not callable(fn):
                continue
            try:
                result = fn(text)
            except TypeError:
                try:
                    result = fn(payload)
                except Exception as exc:
                    return {"available": True, "error": f"{type(exc).__name__}: {exc}", "method": name}
            except Exception as exc:
                return {"available": True, "error": f"{type(exc).__name__}: {exc}", "method": name}
            out = self._jsonable(result)
            if isinstance(out, Mapping):
                out = dict(out)
                out.setdefault("available", True)
                out.setdefault("method", name)
                return out
            return {"available": True, "method": name, "raw": str(out)[:500]}
        return {"available": False, "reason": "no compatible digestion method"}

    def _store_memory(self, trace: Dict[str, Any]) -> bool:
        if not self.memory_system:
            return False
        text = str(trace.get("text", "")).strip()
        if not text:
            return False
        digestion = trace.get("digestion", {}) if isinstance(trace.get("digestion"), Mapping) else {}
        counts = self._digestion_counts(digestion)
        source_file = str(trace.get("source_file", "PDF"))
        page = trace.get("page", "?")
        chunk = trace.get("chunk_index", "?")
        excerpt = text[:420]
        learn = getattr(self.memory_system, "learn_causal_relation", None)
        if callable(learn):
            try:
                learn(
                    event=f"Lecture du PDF {source_file}, page {page}, fragment {chunk}: {excerpt}",
                    experienced_effect=(
                        "Consolide une connaissance de livre en mémoire active: "
                        f"{counts['atoms']} atomes, {counts['neurons_created']} neurones nouveaux, "
                        f"{counts['neurons_reinforced']} renforcements, {counts['links_created']} liens."
                    ),
                    emotional_trace="curious",
                    behavioral_shift="réactiver les concepts lus quand l'utilisateur questionne le livre",
                    attention_impact="augmenter l'attention sur mémoire, matière, esprit, perception et action si présents",
                    source_context={
                        "type": "pdf_knowledge",
                        "source_file": source_file,
                        "source_path": trace.get("source_path", ""),
                        "page": page,
                        "chunk_index": chunk,
                        "excerpt": excerpt,
                        "digestion_counts": counts,
                    },
                    initial_confidence=0.66,
                    memory_kind="initiative_learning",
                    valence=0.18,
                    effect_strength=min(1.0, 0.35 + counts["atoms"] * 0.035 + counts["links_created"] * 0.01),
                    recurrence_pressure=0.22,
                    source_engine="pdf_knowledge_engine",
                    identity_impact=0.18,
                    autobiographical_weight=0.14,
                    causal_layers={
                        "book_learning": 0.82,
                        "semantic_consolidation": min(1.0, 0.3 + counts["atoms"] * 0.04),
                        "dialogue_reactivation": 0.72,
                    },
                    episode_context={"origin": "pdf_reading", "page": page, "chunk": chunk},
                )
                return True
            except TypeError:
                try:
                    learn(
                        f"Lecture du PDF {source_file}, page {page}: {excerpt}",
                        "Connaissance de livre consolidée pour réactivation en dialogue.",
                    )
                    return True
                except Exception:
                    pass
            except Exception:
                pass
        for name in ("store_memory", "remember", "add_memory", "store", "save_memory", "record", "append"):
            fn = getattr(self.memory_system, name, None)
            if not callable(fn):
                continue
            try:
                fn(trace)
                return True
            except TypeError:
                try:
                    fn(text, metadata={k: v for k, v in trace.items() if k != "text"})
                    return True
                except Exception:
                    continue
            except Exception:
                continue
        return False
