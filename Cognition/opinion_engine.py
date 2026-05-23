"""opinion_engine.py — positions persistantes lentes, sans phrases préécrites."""
from __future__ import annotations

import json, math, os, time, re
from typing import Any, Dict, Mapping, List


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try: f = float(v)
    except Exception: return lo
    if math.isnan(f) or math.isinf(f): return lo
    return max(lo, min(hi, f))


class OpinionEngine:
    def __init__(self, storage_path: str = "data/opinions_default.json"):
        self.storage_path = storage_path
        self.opinions: Dict[str, Dict[str, Any]] = {}
        self.load()

    def _topic(self, text: str) -> str:
        toks = re.findall(r"\b[\wÀ-ÿ']{4,}\b", str(text or "").lower())
        stop = {"dans","avec","pour","quoi","comment","cette","celui","celle","être","avoir","mais","donc","livre","lecture"}
        toks = [t for t in toks if t not in stop]
        return " ".join(toks[:4]) or "expérience"

    def update_opinion(self, topic: str, new_evidence: float, source: str = "experience", tension: float = 0.0) -> Dict[str, Any]:
        topic = self._topic(topic)
        if topic not in self.opinions:
            self.opinions[topic] = {"position": 0.5, "certainty": 0.08, "tension": 0.0, "sources": {}, "updated_at": time.time()}
        op = self.opinions[topic]
        lr = 0.035 if source in {"book", "pdf", "reading"} else 0.11
        before = float(op.get("position", 0.5))
        op["position"] = round(_clamp(before + lr * (_clamp(new_evidence) - before)), 4)
        op["certainty"] = round(_clamp(float(op.get("certainty", 0.1)) + 0.012 + abs(op["position"] - before) * 0.04), 4)
        op["tension"] = round(_clamp(float(op.get("tension", 0.0)) * 0.92 + _clamp(tension) * 0.12), 4)
        op.setdefault("sources", {})[source] = int(op.get("sources", {}).get(source, 0)) + 1
        op["updated_at"] = time.time()
        self.save()
        return {"topic": topic, **op}

    def infer_from_text(self, text: str, source: str = "experience", emotion_state: Mapping[str, Any] | None = None) -> Dict[str, Any]:
        emotion_state = emotion_state or {}
        val = _clamp(emotion_state.get("warmth", emotion_state.get("valence", 0.5)))
        tension = _clamp(emotion_state.get("tension", emotion_state.get("accumulated_tension", 0.0)))
        # Evidence faible : l'opinion bouge lentement, mais la tension est conservée.
        return self.update_opinion(self._topic(text), val * 0.65 + (1.0 - tension) * 0.20 + 0.075, source=source, tension=tension)

    def signal(self, query: str = "", top_k: int = 5) -> Dict[str, Any]:
        if not self.opinions:
            return {"available": False, "opinions": []}
        q = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", str(query or "").lower()))
        scored: List[tuple[float, str, Dict[str, Any]]] = []
        for topic, op in self.opinions.items():
            overlap = len(q & set(topic.split())) if q else 0
            score = overlap * 0.4 + float(op.get("certainty", 0.0)) * 0.35 + float(op.get("tension", 0.0)) * 0.25
            scored.append((score, topic, op))
        scored.sort(key=lambda x: x[0], reverse=True)
        return {"available": True, "opinions": [{"topic": t, **op, "score": round(s, 4)} for s,t,op in scored[:top_k]]}

    def organic_decay(self) -> Dict[str, Any]:
        for op in self.opinions.values():
            op["tension"] = round(_clamp(float(op.get("tension", 0.0)) * 0.985), 4)
            op["certainty"] = round(_clamp(float(op.get("certainty", 0.1)) * 0.999), 4)
        self.save()
        return {"count": len(self.opinions)}

    def snapshot(self) -> Dict[str, Any]:
        return {"available": True, "count": len(self.opinions), "opinions": self.signal().get("opinions", [])[:5]}

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({"opinions": self.opinions}, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f: data = json.load(f)
            if isinstance(data.get("opinions"), dict): self.opinions = data["opinions"]
        except Exception:
            self.opinions = {}
