"""
autobiographical_continuity_engine.py — project_leia

Mémoire autobiographique vivante sans phrases préécrites.
Ce module ne produit pas de réponse publique. Il conserve des épisodes, axes,
changements internes et retours possibles que le core peut injecter dans la
bouche et l'initiative.
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


def _words(text: str) -> list[str]:
    stop = {"mais","donc","avec","sans","pour","dans","quoi","elle","lui","moi","toi","que","qui","une","des","les","est","pas","encore","alors","vasy","vas","prend","temps","corrige","fini"}
    out = []
    for w in re.findall(r"\b[\wÀ-ÿ']{3,}\b", str(text or '').lower()):
        if w not in stop and len(w) < 42:
            out.append(w)
    return out


class AutobiographicalContinuityEngine:
    def __init__(self, storage_path: str | Path = "data/autobiographical_continuity.json", max_events: int = 160):
        self.storage_path = Path(storage_path)
        self.max_events = int(max_events)
        self.events: deque[dict[str, Any]] = deque(maxlen=self.max_events)
        self.identity_axes: Counter[str] = Counter()
        self.unfinished: deque[dict[str, Any]] = deque(maxlen=48)
        self.book_marks: deque[dict[str, Any]] = deque(maxlen=40)
        self.long_mood = {"continuity": 0.32, "trust": 0.42, "curiosity": 0.46, "self_shape": 0.24, "unfinished_pressure": 0.0}
        self._load()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.events = deque(data.get("events", [])[-self.max_events:], maxlen=self.max_events)
                self.identity_axes = Counter(data.get("identity_axes", {}))
                self.unfinished = deque(data.get("unfinished", [])[-48:], maxlen=48)
                self.book_marks = deque(data.get("book_marks", [])[-40:], maxlen=40)
                mood = data.get("long_mood", {})
                if isinstance(mood, Mapping):
                    self.long_mood.update({k: _clamp(v) for k, v in mood.items() if k in self.long_mood})
        except Exception:
            pass

    def save(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(json.dumps(self.snapshot(), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def absorb_book_model(self, book_model: Mapping[str, Any]) -> dict[str, Any]:
        if not isinstance(book_model, Mapping):
            return {"accepted": False}
        axes = [str(x).strip().lower() for x in (book_model.get("axes") or []) if str(x).strip()][:16]
        effects = book_model.get("living_effects", {}) if isinstance(book_model.get("living_effects"), Mapping) else {}
        mark = {
            "kind": "book",
            "time": time.time(),
            "axes": axes,
            "questions": list(book_model.get("question_axes", []) or [])[:8],
            "pressure": _clamp(effects.get("understanding_pressure", 0.45)),
        }
        self.book_marks.appendleft(mark)
        for axis in axes[:10]:
            self.identity_axes[axis] += 1
        self.long_mood["curiosity"] = _clamp(self.long_mood["curiosity"] + mark["pressure"] * 0.045)
        self.long_mood["self_shape"] = _clamp(self.long_mood["self_shape"] + mark["pressure"] * 0.03)
        self.long_mood["continuity"] = _clamp(self.long_mood["continuity"] + 0.035)
        self.save()
        return {"accepted": True, "book_axes": axes[:8], "pressure": mark["pressure"]}

    def absorb_exchange(self, user_text: str, response: str, context: Mapping[str, Any] | None = None, after_effect: Mapping[str, Any] | None = None) -> dict[str, Any]:
        context = context or {}
        after_effect = after_effect or {}
        tokens = _words(user_text + " " + response)
        focus = str(context.get("focus") or context.get("dominant_living_axis") or (tokens[0] if tokens else ""))[:96]
        tension = _clamp(context.get("emotional_tension", context.get("tension", 0.0)))
        impact = max(tension, _clamp(after_effect.get("impact", after_effect.get("change", 0.0))), _clamp(context.get("confidence", 0.0)) * 0.35)
        event = {
            "kind": "dialogue",
            "time": time.time(),
            "focus": focus,
            "tokens": tokens[:18],
            "impact": round(impact, 4),
            "unfinished": bool(tension > 0.42 or any(w in tokens for w in ("manque", "vivante", "livre", "mémoire", "memoire"))),
        }
        self.events.appendleft(event)
        for t in tokens[:10]:
            self.identity_axes[t] += 1
        if event["unfinished"]:
            self.unfinished.appendleft({"focus": focus, "tokens": tokens[:8], "pressure": round(max(impact, 0.34), 4), "time": time.time()})
        self.long_mood["continuity"] = _clamp(self.long_mood["continuity"] + impact * 0.012)
        self.long_mood["trust"] = _clamp(self.long_mood["trust"] + _clamp(context.get("relational_proximity", 0.0)) * 0.006)
        self.long_mood["unfinished_pressure"] = _clamp(self.long_mood["unfinished_pressure"] * 0.92 + (0.08 if event["unfinished"] else -0.018))
        self.save()
        return {"accepted": True, "focus": focus, "impact": round(impact, 4), "unfinished": event["unfinished"]}

    def reactivate(self, query_text: str = "", limit: int = 12) -> dict[str, Any]:
        q = set(_words(query_text))
        scored: list[tuple[float, dict[str, Any]]] = []
        for i, event in enumerate(self.events):
            toks = set(event.get("tokens") or [])
            overlap = len(q & toks) / max(1, len(q)) if q else 0.0
            score = _clamp(float(event.get("impact", 0.0)) * 0.62 + overlap * 0.38 - i * 0.003)
            if score > 0.08:
                scored.append((score, event))
        scored.sort(key=lambda x: x[0], reverse=True)
        axes = [k for k, _ in self.identity_axes.most_common(limit * 2) if len(k) > 2]
        unfinished = list(self.unfinished)[:8]
        book_axes: list[str] = []
        for bm in list(self.book_marks)[:5]:
            book_axes.extend([str(x) for x in bm.get("axes", [])])
        active = []
        for _, event in scored[:limit]:
            for tok in event.get("tokens", [])[:6]:
                if tok not in active:
                    active.append(tok)
        return {
            "available": bool(self.events or self.book_marks),
            "active_episodes": [e for _, e in scored[:5]],
            "identity_axes": axes[:limit],
            "active_tokens": active[:limit],
            "unfinished": unfinished,
            "book_axes": list(dict.fromkeys(book_axes))[:limit],
            "long_mood": dict(self.long_mood),
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "events": list(self.events),
            "identity_axes": dict(self.identity_axes),
            "unfinished": list(self.unfinished),
            "book_marks": list(self.book_marks),
            "long_mood": dict(self.long_mood),
            "event_count": len(self.events),
        }
