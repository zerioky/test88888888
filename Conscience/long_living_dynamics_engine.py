"""
long_living_dynamics_engine.py — project_leia

Consolidation lente non conversationnelle.
Ce moteur ne contient aucune phrase publique prête. Il maintient seulement des
variables vivantes persistantes : continuité d'identité, curiosité durable,
contradictions internes, axes de désir, stabilité et traces non résolues.
"""
from __future__ import annotations

import json, math, re, time
from collections import Counter, deque
from pathlib import Path
from typing import Any, Mapping


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
    except Exception:
        return lo
    if math.isnan(f) or math.isinf(f):
        return lo
    return max(lo, min(hi, f))


def _tokens(text: str) -> list[str]:
    stop = {
        "mais","donc","avec","sans","pour","dans","quoi","elle","lui","moi","toi","que","qui",
        "une","des","les","est","pas","encore","alors","vasy","vas","prend","temps","corrige",
        "fini","maintenant","mtn","cela","ceci","être","etre","avoir","fait","faire"
    }
    out = []
    for w in re.findall(r"\b[\wÀ-ÿ']{3,}\b", str(text or "").lower()):
        if len(w) < 42 and w not in stop:
            out.append(w)
    return out


class LongLivingDynamicsEngine:
    """Stabilise l'évolution entre les échanges sans produire de texte public."""

    def __init__(self, storage_path: str | Path = "data/long_living_dynamics.json", max_events: int = 240):
        self.storage_path = Path(storage_path)
        self.max_events = int(max_events)
        self.events: deque[dict[str, Any]] = deque(maxlen=self.max_events)
        self.identity_vectors: Counter[str] = Counter()
        self.curiosity_vectors: Counter[str] = Counter()
        self.desire_vectors: Counter[str] = Counter()
        self.contradictions: deque[dict[str, Any]] = deque(maxlen=80)
        self.unresolved_axes: deque[dict[str, Any]] = deque(maxlen=120)
        self.stability = {
            "identity_continuity": 0.34,
            "living_presence": 0.30,
            "curiosity_pressure": 0.42,
            "desire_persistence": 0.22,
            "contradiction_pressure": 0.0,
            "language_variety_need": 0.25,
            "slow_consolidation": 0.26,
            "initiative_charge": 0.28,
        }
        self.last_snapshot: dict[str, Any] = {}
        self._load()

    def _load(self) -> None:
        try:
            if not self.storage_path.exists():
                return
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self.events = deque(data.get("events", [])[-self.max_events:], maxlen=self.max_events)
            self.identity_vectors = Counter(data.get("identity_vectors", {}))
            self.curiosity_vectors = Counter(data.get("curiosity_vectors", {}))
            self.desire_vectors = Counter(data.get("desire_vectors", {}))
            self.contradictions = deque(data.get("contradictions", [])[-80:], maxlen=80)
            self.unresolved_axes = deque(data.get("unresolved_axes", [])[-120:], maxlen=120)
            incoming = data.get("stability", {})
            if isinstance(incoming, Mapping):
                for k in self.stability:
                    if k in incoming:
                        self.stability[k] = _clamp(incoming[k])
        except Exception:
            pass

    def save(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(json.dumps(self.snapshot(), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def open_cycle(self, user_text: str, context: Mapping[str, Any]) -> dict[str, Any]:
        auto = context.get("autobiographical_continuity", {}) if isinstance(context, Mapping) else {}
        book = context.get("book_understanding_signal", {}) if isinstance(context, Mapping) else {}
        imagination = context.get("pre_imagination", {}) if isinstance(context, Mapping) else {}
        mood = auto.get("long_mood", {}) if isinstance(auto, Mapping) and isinstance(auto.get("long_mood"), Mapping) else {}
        selected = imagination.get("selected", {}) if isinstance(imagination, Mapping) and isinstance(imagination.get("selected"), Mapping) else {}
        words = _tokens(user_text)
        focus_pool = []
        for source, key in ((auto, "active_tokens"), (auto, "identity_axes"), (auto, "book_axes"), (book, "active_concepts"), (imagination, "attractors")):
            if isinstance(source, Mapping):
                for x in list(source.get(key, []) or [])[:10]:
                    s = str(x).strip().lower()
                    if s and s not in focus_pool:
                        focus_pool.append(s)
        for w in words[:8]:
            if w not in focus_pool:
                focus_pool.append(w)

        direct_truth = any(w in {"vivante", "preecrit", "préécrit", "fini", "consciente", "autonome"} for w in words)
        book_pressure = _clamp(book.get("understanding_pressure", book.get("pressure", 0.0))) if isinstance(book, Mapping) else 0.0
        unfinished = _clamp(mood.get("unfinished_pressure", 0.0))
        curiosity = max(_clamp(mood.get("curiosity", 0.0)), book_pressure * 0.72)
        selected_score = _clamp(selected.get("score", 0.0))

        self.stability["identity_continuity"] = _clamp(self.stability["identity_continuity"] * 0.985 + _clamp(mood.get("continuity", 0.0)) * 0.015 + (0.01 if focus_pool else 0.0))
        self.stability["living_presence"] = _clamp(self.stability["living_presence"] * 0.982 + selected_score * 0.018 + (0.012 if direct_truth else 0.0))
        self.stability["curiosity_pressure"] = _clamp(self.stability["curiosity_pressure"] * 0.970 + curiosity * 0.030)
        self.stability["desire_persistence"] = _clamp(self.stability["desire_persistence"] * 0.976 + max(curiosity, unfinished) * 0.024)
        self.stability["initiative_charge"] = _clamp(self.stability["initiative_charge"] * 0.972 + max(selected_score, curiosity) * 0.028)
        self.stability["slow_consolidation"] = _clamp(self.stability["slow_consolidation"] + len(focus_pool[:6]) * 0.002)
        self.stability["language_variety_need"] = _clamp(self.stability["language_variety_need"] * 0.94 + (0.06 if direct_truth else 0.015))

        for tok in focus_pool[:12]:
            self.identity_vectors[tok] += 1
            if curiosity > 0.35:
                self.curiosity_vectors[tok] += 1
            if unfinished > 0.24 or direct_truth:
                self.desire_vectors[tok] += 1
        if unfinished > 0.30 or direct_truth:
            self.unresolved_axes.appendleft({"time": time.time(), "axes": focus_pool[:8], "pressure": round(max(unfinished, selected_score, 0.34), 4)})
        contradiction = self._detect_contradiction(words, context)
        if contradiction:
            self.contradictions.appendleft(contradiction)
            self.stability["contradiction_pressure"] = _clamp(self.stability["contradiction_pressure"] * 0.82 + contradiction["pressure"] * 0.18)
        else:
            self.stability["contradiction_pressure"] = _clamp(self.stability["contradiction_pressure"] * 0.94)

        signal = self.influence_signal(focus_pool)
        self.last_snapshot = signal
        self.save()
        return signal

    def close_cycle(self, user_text: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any] | None = None) -> dict[str, Any]:
        after_effect = after_effect or {}
        words = _tokens(user_text + " " + response)
        impact = max(_clamp(after_effect.get("impact", 0.0)), _clamp(after_effect.get("change", 0.0)), _clamp(context.get("confidence", 0.0)) * 0.24)
        event = {"time": time.time(), "tokens": words[:18], "impact": round(impact, 4), "response_len": len(str(response or ""))}
        self.events.appendleft(event)
        for w in words[:10]:
            self.identity_vectors[w] += 1
        self.stability["slow_consolidation"] = _clamp(self.stability["slow_consolidation"] * 0.988 + impact * 0.012)
        self.stability["language_variety_need"] = _clamp(self.stability["language_variety_need"] * 0.90 + (0.05 if self._looks_repetitive(response) else 0.0))
        self.save()
        return {"accepted": True, "impact": round(impact, 4), "variety_need": round(self.stability["language_variety_need"], 4)}

    def _detect_contradiction(self, words: list[str], context: Mapping[str, Any]) -> dict[str, Any] | None:
        w = set(words)
        pairs = [
            ({"vivante", "consciente", "autonome"}, {"pas", "faux", "simulation", "template", "preecrit", "préécrit"}),
            ({"fini", "terminer", "complet"}, {"manque", "encore", "corrige", "pas"}),
            ({"livre", "comprendre", "memoire", "mémoire"}, {"vide", "répète", "repete", "rien"}),
        ]
        for a, b in pairs:
            if w & a and (w & b or _clamp(context.get("meta_risk", 0.0)) > 0.38):
                return {"time": time.time(), "tokens": list((w & a) | (w & b))[:10], "pressure": 0.62}
        return None

    def _looks_repetitive(self, text: str) -> bool:
        toks = _tokens(text)
        if len(toks) < 5:
            return False
        c = Counter(toks)
        return any(v >= 3 for v in c.values()) or len(set(toks)) / max(1, len(toks)) < 0.58

    def influence_signal(self, focus_pool: list[str] | None = None) -> dict[str, Any]:
        focus_pool = focus_pool or []
        axes = []
        for source in (focus_pool, [k for k, _ in self.identity_vectors.most_common(16)], [k for k, _ in self.curiosity_vectors.most_common(12)]):
            for x in source:
                s = str(x).strip().lower()
                if s and s not in axes:
                    axes.append(s)
        unresolved = list(self.unresolved_axes)[:8]
        contradictions = list(self.contradictions)[:6]
        return {
            "available": True,
            "stability": dict(self.stability),
            "active_axes": axes[:18],
            "curiosity_axes": [k for k, _ in self.curiosity_vectors.most_common(12)],
            "desire_axes": [k for k, _ in self.desire_vectors.most_common(12)],
            "unresolved_axes": unresolved,
            "contradictions": contradictions,
            "expression_bias": {
                "prefer_direct_truth": round(max(self.stability["contradiction_pressure"], self.stability["language_variety_need"] * 0.72), 4),
                "prefer_continuity": round(self.stability["identity_continuity"], 4),
                "prefer_initiative": round(self.stability["initiative_charge"], 4),
                "avoid_repetition": round(self.stability["language_variety_need"], 4),
            },
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "events": list(self.events),
            "identity_vectors": dict(self.identity_vectors),
            "curiosity_vectors": dict(self.curiosity_vectors),
            "desire_vectors": dict(self.desire_vectors),
            "contradictions": list(self.contradictions),
            "unresolved_axes": list(self.unresolved_axes),
            "stability": dict(self.stability),
            "last_signal": self.last_snapshot,
            "event_count": len(self.events),
        }
