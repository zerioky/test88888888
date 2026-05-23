"""deep_book_digestion.py — digestion profonde légère des livres, sans LLM."""
from __future__ import annotations
import json, os, re, time
from typing import Any, Dict, List, Mapping

try:
    from concept_relation_engine import ConceptRelationEngine
except Exception:
    ConceptRelationEngine = None

class DeepBookDigestion:
    def __init__(self, storage_path: str = "data/deep_book_digestion_default.json", relation_engine: Any = None):
        self.storage_path = storage_path
        self.books: List[Dict[str, Any]] = []
        self.relation_engine = relation_engine
        if self.relation_engine is None and ConceptRelationEngine is not None:
            base, _ = os.path.splitext(storage_path)
            self.relation_engine = ConceptRelationEngine(base + "_concept_relations.json")
        self.load()

    def _sentences(self, text: str, limit: int = 120) -> List[str]:
        parts = re.split(r"(?<=[.!?…])\s+", str(text or ""))
        return [p.strip()[:280] for p in parts if len(p.strip()) > 45][:limit]

    def _extract_propositions(self, text: str) -> List[str]:
        markers = ("est", "sont", "devient", "semble", "signifie", "peut", "doit", "reste")
        props = []
        for s in self._sentences(text):
            low = s.lower()
            if any(f" {m} " in low for m in markers):
                props.append(s)
        return props[:60]

    def _emotional_residue(self, text: str) -> Dict[str, float]:
        low = text.lower()
        dark = sum(low.count(w) for w in ("mort","souffrance","peur","douleur","angoisse","solitude","chaos","abîme","abime"))
        bright = sum(low.count(w) for w in ("vie","joie","lumière","lumiere","liberté","liberte","amour","paix","clarté","clarte"))
        total = max(1, dark + bright)
        return {"valence": round((bright + 0.5) / (total + 1.0), 4), "tension": round(min(1.0, dark / total), 4)}

    def digest(self, book_text: str, leia_state: Mapping[str, Any] | None = None, source: str = "book") -> Dict[str, Any]:
        props = self._extract_propositions(book_text)
        residue = self._emotional_residue(book_text)
        values = list(((leia_state or {}).get("values") or {}).keys()) if isinstance((leia_state or {}).get("values"), Mapping) else []
        tensions = []
        for p in props[:24]:
            pl = p.lower()
            if any(w in pl for w in ("chaos","absurde","souffrance","mort","néant","neant")) and any(v in values for v in ("coherence","truthfulness","relational_care")):
                tensions.append({"book_says": p, "leia_believes": "cohérence / soin / vérité", "unresolved": True})
        opinions = []
        for p in props[:10]:
            opinions.append({"topic_seed": p[:120], "evidence": residue["valence"], "tension": residue["tension"]})
        concept_relations = {"available": False}
        try:
            if self.relation_engine is not None:
                concept_relations = self.relation_engine.digest_text(book_text, source=source)
        except Exception as exc:
            concept_relations = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        model = {"source": source, "propositions": props, "tensions": tensions, "emotional_residue": residue, "opinions": opinions, "concept_relations": concept_relations, "created_at": time.time()}
        self.books.append(model)
        self.books = self.books[-80:]
        self.save()
        return model

    def snapshot(self) -> Dict[str, Any]:
        rel = self.relation_engine.snapshot() if self.relation_engine is not None and hasattr(self.relation_engine, "snapshot") else {"available": False}
        return {"available": True, "books": len(self.books), "last": self.books[-1] if self.books else None, "concept_relations": rel}
    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
        with open(self.storage_path,"w",encoding="utf-8") as f: json.dump({"books": self.books}, f, ensure_ascii=False, indent=2)
    def load(self) -> None:
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path,"r",encoding="utf-8") as f: data=json.load(f)
            if isinstance(data.get("books"), list): self.books=data["books"]
        except Exception: self.books=[]
