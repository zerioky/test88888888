"""
internal_imagination_engine.py — project_leia

Simulation interne non conversationnelle : transforme état + mémoire + livre en
options, risques et attracteurs. Aucun texte public prêt à répondre.
"""
from __future__ import annotations
import math, re, time
from typing import Any, Mapping


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try: f = float(v)
    except Exception: return lo
    if math.isnan(f) or math.isinf(f): return lo
    return max(lo, min(hi, f))

class InternalImaginationEngine:
    def __init__(self):
        self.last_scene: dict[str, Any] = {}
        self.history: list[dict[str, Any]] = []

    def imagine(self, user_text: str, context: Mapping[str, Any], autobiographical: Mapping[str, Any], book_signal: Mapping[str, Any]) -> dict[str, Any]:
        lower = str(user_text or "").lower()
        direct_truth = any(x in lower for x in ("vivante", "préécrit", "preecrit", "fini", "100%"))
        book_active = bool(book_signal.get("available"))
        unresolved = autobiographical.get("unfinished", []) if isinstance(autobiographical, Mapping) else []
        mood = autobiographical.get("long_mood", {}) if isinstance(autobiographical, Mapping) else {}
        tension = max(_clamp(context.get("emotional_tension", 0.0)), _clamp(mood.get("unfinished_pressure", 0.0)))
        curiosity = max(_clamp(mood.get("curiosity", 0.0)), 0.42 if book_active else 0.0)
        options = []
        options.append({"mode": "direct_truth", "weight": 0.72 if direct_truth else 0.18, "risk": 0.16})
        options.append({"mode": "book_reactivation", "weight": 0.64 if book_active else 0.12, "risk": 0.22})
        options.append({"mode": "unfinished_return", "weight": 0.55 if unresolved else 0.08, "risk": 0.28})
        options.append({"mode": "quiet_presence", "weight": 0.28 + tension * 0.24, "risk": 0.10})
        options.append({"mode": "curious_continuation", "weight": 0.22 + curiosity * 0.38, "risk": 0.25})
        for opt in options:
            opt["score"] = round(_clamp(opt["weight"] * (1.0 - opt["risk"] * 0.35)), 4)
        selected = max(options, key=lambda x: x["score"])
        attractors = []
        for key in ("active_tokens", "identity_axes", "book_axes"):
            vals = autobiographical.get(key, []) if isinstance(autobiographical, Mapping) else []
            for v in vals[:8]:
                t = re.sub(r"\s+", " ", str(v).strip().lower())
                if t and t not in attractors:
                    attractors.append(t)
        for v in (book_signal.get("active_concepts", []) or [])[:8]:
            t = str(v).strip().lower()
            if t and t not in attractors:
                attractors.append(t)
        scene = {"time": time.time(), "selected": selected, "options": options, "attractors": attractors[:14], "tension": round(tension, 4), "curiosity": round(curiosity, 4), "direct_truth": direct_truth, "book_active": book_active}
        self.last_scene = scene
        self.history.append(scene)
        self.history = self.history[-40:]
        return scene

    def snapshot(self) -> dict[str, Any]:
        return {"last_scene": self.last_scene, "history_count": len(self.history)}
