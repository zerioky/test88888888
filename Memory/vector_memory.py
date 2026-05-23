"""
vector_memory.py — mémoire associative locale pour Leia, sans LLM.

Objectif : rappeler des souvenirs par résonance sémantique locale.
- Utilise sentence-transformers si installé.
- Sinon fallback déterministe par vecteur lexical hashing, sans dépendance lourde.
- Persiste en JSON.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import random
import re
import time
from typing import Any, Dict, List, Mapping, Optional


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
    except Exception:
        return lo
    if math.isnan(f) or math.isinf(f):
        return lo
    return max(lo, min(hi, f))


def _tokenize(text: str) -> List[str]:
    return re.findall(r"\b[\wÀ-ÿ']{3,}\b", str(text or "").lower())


class LeiaVectorMemory:
    def __init__(self, storage_path: str = "data/vector_memory_default.json", dim: int = 384):
        self.storage_path = storage_path
        self.dim = int(dim)
        self.memories: List[Dict[str, Any]] = []
        self.model = None
        self.model_name = "hashing-fallback"
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
            self.model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
            self.model_name = "paraphrase-multilingual-MiniLM-L12-v2"
        except Exception:
            self.model = None
        self.load()

    def _encode(self, text: str) -> List[float]:
        text = str(text or "")
        if self.model is not None:
            try:
                vec = self.model.encode(text)
                return [float(x) for x in list(vec)]
            except Exception:
                pass
        vec = [0.0] * self.dim
        for tok in _tokenize(text):
            h = hashlib.blake2b(tok.encode("utf-8"), digest_size=8).digest()
            idx = int.from_bytes(h[:4], "little") % self.dim
            sign = 1.0 if (h[4] % 2 == 0) else -1.0
            weight = 1.0 + min(2.0, len(tok) / 10.0)
            vec[idx] += sign * weight
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    @staticmethod
    def _cosine(a: List[float], b: List[float]) -> float:
        if not a or not b:
            return 0.0
        n = min(len(a), len(b))
        dot = sum(a[i] * b[i] for i in range(n))
        na = math.sqrt(sum(a[i] * a[i] for i in range(n)))
        nb = math.sqrt(sum(b[i] * b[i] for i in range(n)))
        return dot / (na * nb + 1e-8)

    def store(self, text: str, emotion_state: Optional[Mapping[str, Any]] = None, source: str = "experience", metadata: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        text = re.sub(r"\s+", " ", str(text or "")).strip()
        if not text:
            return {"stored": False, "reason": "empty"}
        emotion_state = emotion_state or {}
        valence = _clamp(emotion_state.get("valence", emotion_state.get("warmth", 0.5)))
        tension = _clamp(emotion_state.get("tension", emotion_state.get("accumulated_tension", 0.0)))
        intensity = _clamp(abs(valence - 0.5) * 1.3 + tension * 0.7)
        item = {
            "text": text[:1200],
            "vector": self._encode(text),
            "valence": round(valence, 4),
            "tension": round(tension, 4),
            "emotional_intensity": round(intensity, 4),
            "weight": round(0.72 + intensity * 0.45, 4),
            "source": source,
            "metadata": dict(metadata or {}),
            "timestamp": time.time(),
            "reactivations": 0,
        }
        self.memories.append(item)
        self.memories = self.memories[-5000:]
        self.save()
        return {"stored": True, "source": source, "weight": item["weight"], "count": len(self.memories)}

    def recall(self, query: str, top_k: int = 5, emotion_state: Optional[Mapping[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self.memories or not str(query or "").strip():
            return []
        qv = self._encode(query)
        current_valence = _clamp((emotion_state or {}).get("valence", (emotion_state or {}).get("warmth", 0.5)))
        scored = []
        now = time.time()
        for m in self.memories:
            sim = self._cosine(qv, list(m.get("vector", []) or []))
            age_days = max(0.0, (now - float(m.get("timestamp", now))) / 86400.0)
            age_factor = 0.55 + 0.45 * math.exp(-age_days / 30.0)
            emotion_affinity = 1.0 - min(0.45, abs(current_valence - _clamp(m.get("valence", 0.5))) * 0.55)
            score = sim * float(m.get("weight", 1.0)) * age_factor * emotion_affinity
            scored.append((score, m))
        scored.sort(key=lambda x: x[0], reverse=True)
        out = []
        for score, m in scored[:max(1, top_k)]:
            m["reactivations"] = int(m.get("reactivations", 0)) + 1
            m["weight"] = round(_clamp(float(m.get("weight", 1.0)) + max(0.0, score) * 0.015, 0.0, 3.0), 4)
            out.append({k: v for k, v in m.items() if k != "vector"} | {"score": round(float(score), 4)})
        if out:
            self.save()
        return out

    def dream_fragment(self) -> Optional[Dict[str, Any]]:
        if not self.memories:
            return None
        weights = [max(0.01, float(m.get("weight", 1.0)) + float(m.get("emotional_intensity", 0.0))) for m in self.memories]
        item = random.choices(self.memories, weights=weights, k=1)[0]
        item["reactivations"] = int(item.get("reactivations", 0)) + 1
        item["weight"] = round(_clamp(float(item.get("weight", 1.0)) + 0.004, 0.0, 3.0), 4)
        self.save()
        return {k: v for k, v in item.items() if k != "vector"}

    def organic_forgetting(self, half_life_days: float = 7.0) -> Dict[str, Any]:
        now = time.time()
        before = len(self.memories)
        kept = []
        for m in self.memories:
            age = max(0.0, now - float(m.get("timestamp", now)))
            decay = math.exp(-age / (max(1.0, half_life_days) * 24 * 3600))
            emotional_protection = abs(float(m.get("valence", 0.5)) - 0.5) * 2.0 + float(m.get("tension", 0.0)) * 0.5
            new_weight = float(m.get("weight", 1.0)) * (0.985 + 0.015 * decay)
            m["weight"] = round(max(new_weight, emotional_protection * 0.08), 4)
            if m["weight"] > 0.01 or int(m.get("reactivations", 0)) > 2:
                kept.append(m)
        self.memories = kept[-5000:]
        self.save()
        return {"before": before, "after": len(self.memories), "forgotten": before - len(self.memories)}

    def snapshot(self) -> Dict[str, Any]:
        return {"available": True, "model": self.model_name, "count": len(self.memories), "storage_path": self.storage_path}

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        payload = {"model": self.model_name, "dim": self.dim, "memories": self.memories[-5000:]}
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            memories = data.get("memories", []) if isinstance(data, dict) else []
            if isinstance(memories, list):
                self.memories = [m for m in memories if isinstance(m, dict) and isinstance(m.get("vector"), list)]
        except Exception:
            self.memories = []
