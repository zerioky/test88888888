# book_understanding_engine.py
# Project Leia / project_leia
#
# Rôle:
#   Transformer une synthèse de livre/PDF en compréhension interne réutilisable.
#   Ce module ne génère aucune réponse publique et ne contient aucune phrase
#   conversationnelle préécrite. Il compresse seulement axes, relations, tensions,
#   passages et questions en un modèle mental que la bouche peut ensuite utiliser.

from __future__ import annotations

import json
import math
import re
import time
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Mapping, Optional, Tuple

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_'-]+", re.UNICODE)

_GENERIC = {
    "trace", "traces", "presence", "présence", "continuité", "continuite", "doute",
    "question", "prudence", "appui", "lien", "liens", "mouvement", "rythme",
    "mémoire", "memoire", "résonance", "resonance", "curiosité", "curiosite",
    "friction", "stabilité", "stabilite", "page", "fragment", "pdf", "livre",
}

_STOP = {
    "avec", "dans", "pour", "sans", "vers", "entre", "comme", "mais", "donc", "ainsi",
    "elle", "elles", "nous", "vous", "leur", "leurs", "cette", "celui", "celle", "ceux",
    "être", "etre", "avoir", "fait", "faire", "plus", "tout", "tous", "toute", "très", "tres",
    "cela", "ceci", "dont", "quand", "quoi", "comment", "pourquoi", "parce", "encore",
}


def _clamp(value: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(value)
    except Exception:
        return lo
    if math.isnan(f) or math.isinf(f):
        return lo
    return max(lo, min(hi, f))


def _words(text: str) -> List[str]:
    out = []
    for w in _WORD_RE.findall(str(text or "").lower()):
        w = w.strip("'_- ")
        if len(w) < 3 or w in _STOP:
            continue
        out.append(w)
    return out


def _short(text: Any, limit: int = 72) -> str:
    s = re.sub(r"\s+", " ", str(text or "").strip().lower())
    s = s.strip(" .,:;!?—[]{}()\"'")
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] or s[:limit]
    return s


def _unique(items: Iterable[Any], limit: int = 20, *, allow_generic: bool = False) -> List[str]:
    out: List[str] = []
    seen = set()
    for item in items or []:
        if isinstance(item, Mapping):
            candidates = [item.get(k) for k in ("label", "concept", "keyword", "from", "to", "source", "target", "axis")]
            kws = item.get("keywords")
            if isinstance(kws, list):
                candidates.extend(kws[:8])
        elif isinstance(item, (list, tuple, set)):
            candidates = list(item)
        else:
            candidates = [item]
        for cand in candidates:
            t = _short(cand)
            if not t or len(t) < 3:
                continue
            if re.match(r"^(relier|clarifier|explorer|résoudre|resoudre|ouvrir_question)\b", t):
                continue
            if not allow_generic and t in _GENERIC:
                continue
            if t not in seen:
                seen.add(t)
                out.append(t)
            if len(out) >= limit:
                return out
    return out


@dataclass
class BookUnderstanding:
    source: str
    created_at: float
    axes: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    relations: List[Dict[str, Any]] = field(default_factory=list)
    tensions: List[Dict[str, Any]] = field(default_factory=list)
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    question_axes: List[str] = field(default_factory=list)
    anchors: List[Dict[str, Any]] = field(default_factory=list)
    concept_pressures: Dict[str, float] = field(default_factory=dict)
    living_effects: Dict[str, float] = field(default_factory=dict)
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class BookUnderstandingEngine:
    """Consolidation non conversationnelle d'une lecture.

    Contrairement à une réponse préécrite, ce modèle ne dit jamais quoi répondre.
    Il indique seulement ce qui doit rester actif après lecture : axes profonds,
    contradictions, transformations internes, questions et pression conceptuelle.
    """

    def __init__(self, storage_path: str = "data/book_understanding_memory.json", max_history: int = 16) -> None:
        self.storage_path = Path(storage_path)
        self.max_history = max(2, int(max_history or 16))
        self.history: Deque[Dict[str, Any]] = deque(maxlen=self.max_history)
        self.active_model: Dict[str, Any] = {}
        self.load_state()

    def load_state(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.active_model = data.get("active_model", {}) if isinstance(data, Mapping) else {}
                self.history = deque(data.get("history", [])[-self.max_history:], maxlen=self.max_history)
        except Exception:
            self.active_model = {}
            self.history = deque(maxlen=self.max_history)

    def save_state(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {"active_model": self.active_model, "history": list(self.history)}
            tmp = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.storage_path)
        except Exception:
            pass

    def consolidate(self, pdf_result: Mapping[str, Any], prior_state: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        synthesis = pdf_result.get("conceptual_synthesis", {}) if isinstance(pdf_result, Mapping) else {}
        if not isinstance(synthesis, Mapping):
            synthesis = {}
        source = str(pdf_result.get("file") or pdf_result.get("source") or "book") if isinstance(pdf_result, Mapping) else "book"

        axes_raw = list(synthesis.get("axes", []) or [])
        keywords_raw = list(synthesis.get("top_keywords", []) or [])
        relations_raw = list(synthesis.get("relations", []) or [])
        excerpts_raw = list(synthesis.get("recent_excerpts", []) or [])
        unresolved_raw = list(synthesis.get("unresolved_questions", []) or [])
        metrics_raw = synthesis.get("metrics", {}) if isinstance(synthesis.get("metrics", {}), Mapping) else {}

        axes = _unique(axes_raw, 18)
        keywords = _unique(keywords_raw, 28)
        if not axes:
            axes = _unique(keywords_raw, 12)

        # Pression conceptuelle : combine stabilité/curiosité/incertitude + rang.
        pressures: Dict[str, float] = {}
        for idx, axis in enumerate(axes_raw[:24]):
            if not isinstance(axis, Mapping):
                continue
            label = _short(axis.get("label"))
            if not label or label in _GENERIC:
                continue
            pressure = _clamp(
                0.25
                + _clamp(axis.get("pressure", 0.0)) * 0.34
                + _clamp(axis.get("stability", 0.0)) * 0.18
                + _clamp(axis.get("curiosity", 0.0)) * 0.14
                + _clamp(axis.get("uncertainty", 0.0)) * 0.10
                - idx * 0.008
            )
            pressures[label] = max(pressures.get(label, 0.0), pressure)
            for kw in _unique(axis.get("keywords", []), 5):
                pressures[kw] = max(pressures.get(kw, 0.0), pressure * 0.76)
        for idx, kw in enumerate(keywords[:20]):
            pressures[kw] = max(pressures.get(kw, 0.0), _clamp(0.58 - idx * 0.018))

        relations: List[Dict[str, Any]] = []
        for rel in relations_raw[:36]:
            if not isinstance(rel, Mapping):
                continue
            src = _short(rel.get("from") or rel.get("source"))
            tgt = _short(rel.get("to") or rel.get("target"))
            kind = _short(rel.get("relation") or rel.get("type") or "lié", 32)
            if not src or not tgt or src == tgt:
                continue
            weight = _clamp(rel.get("weight", 0.42))
            relations.append({"source": src, "target": tgt, "type": kind or "lié", "weight": round(weight, 4)})

        # Tensions internes : relations entre axes très pressurisés, sans phrase finale.
        tensions: List[Dict[str, Any]] = []
        for rel in relations[:18]:
            src, tgt = rel.get("source"), rel.get("target")
            p = max(pressures.get(src, 0.0), pressures.get(tgt, 0.0), _clamp(rel.get("weight", 0.0)))
            if p >= 0.28:
                tensions.append({
                    "between": [src, tgt],
                    "relation": rel.get("type", "lié"),
                    "pressure": round(_clamp(p), 4),
                    "unresolved": bool(p > 0.52),
                })

        # Transformations : ce que la lecture change dans le modèle interne.
        prior_axes = set(_unique((prior_state or {}).get("axes", []), 50)) if isinstance(prior_state, Mapping) else set()
        transformations: List[Dict[str, Any]] = []
        for axis in axes[:12]:
            novelty = 0.72 if axis not in prior_axes else 0.34
            transformations.append({
                "axis": axis,
                "novelty": round(novelty, 4),
                "integration_pressure": round(_clamp(pressures.get(axis, 0.45) * (0.75 + novelty * 0.25)), 4),
            })

        anchors: List[Dict[str, Any]] = []
        for ex in excerpts_raw[:10]:
            if not isinstance(ex, Mapping):
                continue
            excerpt = re.sub(r"\s+", " ", str(ex.get("excerpt", "")).strip())[:260]
            if not excerpt:
                continue
            anchors.append({
                "excerpt": excerpt,
                "keywords": _unique(ex.get("keywords", []), 8, allow_generic=False),
                "relevance": round(_clamp(ex.get("relevance", 0.0)), 4),
            })

        question_axes = _unique(unresolved_raw, 10, allow_generic=False)
        if not question_axes:
            question_axes = [t["between"][0] for t in tensions[:4] if t.get("between")]

        density = _clamp(metrics_raw.get("density", 0.0))
        coherence = _clamp(metrics_raw.get("coherence", 0.0))
        question_pressure = _clamp(metrics_raw.get("question_pressure", 0.0))
        living_effects = {
            "understanding_pressure": round(_clamp(coherence * 0.38 + density * 0.25 + len(axes) / 24.0 * 0.22 + len(relations) / 32.0 * 0.15), 4),
            "question_pressure": round(_clamp(question_pressure * 0.55 + len(question_axes) / 12.0 * 0.25 + len(tensions) / 18.0 * 0.20), 4),
            "dialogue_reactivation": round(_clamp(len(anchors) / 8.0 * 0.22 + len(pressures) / 36.0 * 0.45 + coherence * 0.33), 4),
            "identity_shift": round(_clamp(len(transformations) / 16.0 * 0.26 + question_pressure * 0.22 + density * 0.16), 4),
        }

        model = BookUnderstanding(
            source=source,
            created_at=time.time(),
            axes=axes,
            keywords=keywords,
            relations=relations[:20],
            tensions=tensions[:16],
            transformations=transformations[:14],
            question_axes=question_axes[:10],
            anchors=anchors[:8],
            concept_pressures={k: round(v, 4) for k, v in sorted(pressures.items(), key=lambda kv: -kv[1])[:40]},
            living_effects=living_effects,
            metrics={
                "source_metrics": dict(metrics_raw),
                "axes_count": len(axes),
                "keywords_count": len(keywords),
                "relations_count": len(relations),
                "tensions_count": len(tensions),
                "anchors_count": len(anchors),
                "pages_read": pdf_result.get("pages_read", 0) if isinstance(pdf_result, Mapping) else 0,
                "chunks_count": pdf_result.get("chunks_count", 0) if isinstance(pdf_result, Mapping) else 0,
            },
        ).to_dict()

        self.active_model = model
        self.history.append(model)
        self.save_state()
        return model

    def reactivate(self, query_text: str = "", limit: int = 12) -> Dict[str, Any]:
        model = self.active_model if isinstance(self.active_model, Mapping) else {}
        if not model:
            return {"available": False}
        q = Counter(_words(query_text))
        pressures = model.get("concept_pressures", {}) if isinstance(model.get("concept_pressures", {}), Mapping) else {}
        scored: List[Tuple[float, str]] = []
        for concept, pressure in pressures.items():
            words = set(_words(concept))
            overlap = len(words & set(q)) / max(1, len(words)) if q else 0.0
            scored.append((_clamp(float(pressure) * 0.72 + overlap * 0.28), str(concept)))
        scored.sort(reverse=True)
        active = [c for _, c in scored[:max(1, int(limit or 12))]]
        return {
            "available": True,
            "active_concepts": active,
            "concept_pressures": {c: round(dict((name, score) for score, name in scored).get(c, 0.0), 4) for c in active},
            "tensions": list(model.get("tensions", []) or [])[:8],
            "relations": list(model.get("relations", []) or [])[:10],
            "question_axes": list(model.get("question_axes", []) or [])[:8],
            "living_effects": dict(model.get("living_effects", {}) or {}),
            "anchors": list(model.get("anchors", []) or [])[:4],
        }

    def snapshot(self) -> Dict[str, Any]:
        return {"active_model": self.active_model, "history_size": len(self.history)}
