"""lexical_impregnation.py — V18 — enrichit le réservoir lexical depuis les livres, sans phrase stockée.

Nouveau : rejet de source persistant.
  reject_source(source, strength) réduit le poids des mots venus de cette source
  et marque la source comme rejetée dans le signal d'expression.
  Le rejet décroit lentement — un désaccord peut s'atténuer.
"""
from __future__ import annotations
import json, math, os, re, time
from typing import Any, Dict, Mapping, List

NEG = {"mort","peur","souffrance","angoisse","vide","ombre","douleur","solitude","chaos","abîme","abime"}
POS = {"lumière","lumiere","joie","liberté","liberte","amour","sens","vie","élan","elan","paix","clarté","clarte"}
STOP = {"avec","dans","pour","plus","mais","donc","elle","nous","vous","être","avoir","comme","cette","cela","sans","entre"}

TECHNICAL_OR_METADATA = {
    "pressure", "latent_pressure", "emotional_pressure", "dormant_pressure",
    "auditifs", "auditive", "auditory", "sensoriel", "sensory",
    "payload", "context", "traceback", "snapshot", "metadata", "filename",
    "source", "debug", "field", "fields", "label", "token", "tokens",
    "score", "weight", "valence", "available", "engine", "weaver",
    "pdf", "json", "python", "variable", "mapping", "dict", "list",
}

def _public_lexeme(word: str) -> bool:
    w = str(word or "").strip().lower()
    if not w or w in STOP or w in TECHNICAL_OR_METADATA:
        return False
    if "_" in w or re.search(r"\d", w):
        return False
    if re.search(r"\b(henri|bergson|mati[eè]re|memoire|mémoire)[_-]", w):
        return False
    if re.search(r"\b(file|filename|metadata|payload|context|pressure|auditif|auditory)\b", w):
        return False
    if len(w) < 4 or len(w) > 32:
        return False
    return True

class LexicalImpregnation:
    def __init__(self, storage_path: str = "data/lexical_impregnation_default.json"):
        self.storage_path = storage_path
        self.lexicon: Dict[str, Dict[str, Any]] = {}
        # source → strength (0-1) : plus c'est haut, plus les mots de cette source sont atténués
        self.rejected_sources: Dict[str, float] = {}
        self.load()

    def _valence(self, word: str, context: str) -> float:
        w = word.lower()
        if w in NEG: return -0.45
        if w in POS: return 0.45
        ctx = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", context.lower()))
        return 0.18 * len(ctx & POS) - 0.18 * len(ctx & NEG)

    def impregnate_from_text(self, text: str, source: str = "book", limit: int = 220) -> Dict[str, Any]:
        words = re.findall(r"\b[\wÀ-ÿ']{4,}\b", str(text or "").lower())
        freq: Dict[str, int] = {}
        for w in words:
            if _public_lexeme(w) and not w.isdigit():
                freq[w] = freq.get(w, 0) + 1
        selected = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:limit]
        now = time.time()
        # Facteur de rejet : si la source est rejetée, les nouveaux mots arrivent atténués
        rejection_factor = 1.0 - self.rejected_sources.get(source, 0.0) * 0.85
        for word, count in selected:
            if len(word) < 4: continue
            old = self.lexicon.get(word, {"weight": 0.0, "valence": 0.0, "sources": {}})
            weight = min(1.0, math.log1p(count) / 5.0) * rejection_factor
            valence = self._valence(word, text[:4000])
            old["weight"] = round(min(2.5, float(old.get("weight", 0.0)) * 0.82 + weight), 4)
            old["valence"] = round(float(old.get("valence", 0.0)) * 0.7 + valence * 0.3, 4)
            old["role"] = "object"
            old.setdefault("sources", {})[source] = int(old.get("sources", {}).get(source, 0)) + count
            old["updated_at"] = now
            self.lexicon[word] = old
        self.save()
        return {"available": True, "added_or_updated": len(selected), "sample": list(self.lexicon.items())[:12]}

    def reject_source(self, source: str, strength: float = 0.7) -> Dict[str, Any]:
        """
        Marque une source comme rejetée avec une intensité donnée.
        Réduit immédiatement le poids de tous les mots issus de cette source
        proportionnellement à la force du rejet.
        Le rejet est persistant — il décroit de ~3% par jour naturellement.
        """
        strength = max(0.0, min(1.0, float(strength)))
        self.rejected_sources[source] = strength

        # Réduction immédiate du poids des mots existants issus de cette source
        attenuation = 1.0 - strength * 0.75
        affected = 0
        for word, data in self.lexicon.items():
            sources = data.get("sources", {})
            if source in sources:
                # Proportion du poids attribuable à cette source (estimation)
                total_count = sum(int(v) for v in sources.values())
                source_count = int(sources.get(source, 0))
                if total_count > 0:
                    source_fraction = source_count / total_count
                    # Atténuer en proportion de ce que cette source contribue
                    current = float(data.get("weight", 0.0))
                    reduction = current * source_fraction * (1.0 - attenuation)
                    data["weight"] = round(max(0.0, current - reduction), 4)
                    affected += 1

        self.save()
        return {
            "available": True,
            "source": source,
            "rejection_strength": round(strength, 3),
            "words_attenuated": affected,
        }

    def clear_rejection(self, source: str) -> Dict[str, Any]:
        """Annule le rejet d'une source."""
        removed = source in self.rejected_sources
        self.rejected_sources.pop(source, None)
        self.save()
        return {"available": True, "source": source, "rejection_cleared": removed}

    def decay_rejections(self, elapsed_days: float = 1.0) -> None:
        """Décroissance naturelle des rejets — un désaccord peut s'atténuer avec le temps."""
        factor = 0.97 ** max(0.0, float(elapsed_days))
        for source in list(self.rejected_sources.keys()):
            self.rejected_sources[source] = round(self.rejected_sources[source] * factor, 4)
            if self.rejected_sources[source] < 0.04:
                del self.rejected_sources[source]

    def expression_signal(self, emotion_state: Mapping[str, Any] | None = None, limit: int = 20) -> Dict[str, Any]:
        val = float((emotion_state or {}).get("warmth", 0.5)) - 0.5
        scored = []
        for word, data in self.lexicon.items():
            affinity = 1.0 - min(1.0, abs(float(data.get("valence", 0.0)) - val))
            # Pénalité pour les mots issus majoritairement de sources rejetées
            sources = data.get("sources", {})
            rejection_penalty = 0.0
            if sources and self.rejected_sources:
                total = sum(int(v) for v in sources.values())
                if total > 0:
                    rejected_weight = sum(
                        int(sources.get(src, 0)) * strength
                        for src, strength in self.rejected_sources.items()
                    )
                    rejection_penalty = min(0.9, rejected_weight / total * 1.2)
            effective_score = float(data.get("weight", 0.0)) * (0.5 + affinity) * (1.0 - rejection_penalty)
            scored.append((effective_score, word, data))
        scored.sort(key=lambda x: x[0], reverse=True)
        return {
            "available": bool(scored),
            "words": [{"surface": w, **d, "score": round(s, 4)} for s, w, d in scored[:limit]],
            "rejected_sources": {k: round(v, 3) for k, v in self.rejected_sources.items()},
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "available": True,
            "count": len(self.lexicon),
            "top": self.expression_signal(limit=10).get("words", []),
            "rejected_sources": dict(self.rejected_sources),
        }

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump({"lexicon": self.lexicon, "rejected_sources": self.rejected_sources},
                      f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f: data = json.load(f)
            if isinstance(data.get("lexicon"), dict):
                self.lexicon = {k: v for k, v in data["lexicon"].items() if _public_lexeme(k)}
            if isinstance(data.get("rejected_sources"), dict):
                self.rejected_sources = {k: float(v) for k, v in data["rejected_sources"].items()}
        except Exception:
            self.lexicon = {}
            self.rejected_sources = {}

