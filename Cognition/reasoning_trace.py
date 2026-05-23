"""
reasoning_trace.py — V18
==========================
Traçabilité du raisonnement de Leia.

Après chaque réponse, Leia peut dire ce qui a pesé sur ce qu'elle a dit.
Pas une explication complète — une trace des influences dominantes.

Nouveau V18 : révision différée autonome.
  Après chaque échange, le moteur examine si la réponse produite
  était cohérente avec l'état interne qui pesait sur elle.
  Si quelque chose cloche, la trace est marquée "douteuse".
  Leia peut revenir dessus d'elle-même — sans qu'on lui demande.

Aucune phrase construite ici — seulement des atomes de traçabilité
et des atomes de doute que la bouche peut formuler à sa façon.
"""

from __future__ import annotations
import json, os, time
from collections import deque
from typing import Any, Dict, List, Optional

def _now(): return time.time()
def _clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, float(v)))

_WHY_PATTERNS = [
    "pourquoi tu dis", "pourquoi tu penses", "pourquoi ça",
    "d'où ça vient", "d'où vient", "tu penses ça pourquoi",
    "comment tu arrives", "qu'est-ce qui te fait dire",
    "explique", "explique-moi", "tu peux expliquer",
]

_LIGHT_RESPONSE_MARKERS = [
    "bien sûr", "bien sur", "absolument", "tout à fait", "évidemment",
    "c'est simple", "c'est clair", "pas de problème",
]


def _response_seems_light(response: str) -> bool:
    r = response.lower()
    if len(response.split()) < 6:
        return True
    return any(m in r for m in _LIGHT_RESPONSE_MARKERS)


def _response_uses_concept(response: str, concepts: List[str]) -> bool:
    r = response.lower()
    return any(c.lower() in r for c in concepts if c and len(c) > 3)


class DeferredReview:
    """
    Révision différée autonome.

    Trois types d'incohérence :
      1. tension_ignorée    — tension haute mais réponse légère
      2. livre_non_exprimé  — mots dominants absents de la réponse
      3. contradiction_muette — tension inter-livres active, non adressée

    Le doute est tracé comme des atomes — pas une auto-critique formulée.
    """

    def __init__(self):
        self.doubted_traces: deque = deque(maxlen=8)
        self.pending_review: Optional[Dict[str, Any]] = None

    def schedule(self, trace: Dict[str, Any]) -> None:
        self.pending_review = trace

    def review(self) -> Optional[Dict[str, Any]]:
        if not self.pending_review:
            return None
        trace = self.pending_review
        self.pending_review = None

        response = trace.get("response_fragment", "")
        doubt_atoms: List[str] = []
        doubt_type: Optional[str] = None

        emo_vals = trace.get("emotion_values", {})
        tension_val = float(emo_vals.get("tension", 0.5))
        if tension_val > 0.65 and _response_seems_light(response):
            doubt_atoms.extend(["tension", "surface"])
            doubt_type = "tension_ignorée"

        book_words = trace.get("dominant_book_words", [])
        if book_words and not _response_uses_concept(response, book_words):
            doubt_atoms.extend(book_words[:2])
            doubt_atoms.append("absent")
            doubt_type = doubt_type or "livre_non_exprimé"

        inter = trace.get("inter_book_tension", {})
        if inter.get("concept") and not _response_uses_concept(response, [inter["concept"]]):
            doubt_atoms.append(inter["concept"])
            doubt_atoms.append("non_dit")
            doubt_type = doubt_type or "contradiction_muette"

        if doubt_type:
            doubt_record = {
                "timestamp": _now(),
                "doubt_type": doubt_type,
                "atoms": [a for a in doubt_atoms if a and len(a) > 2][:6],
                "original_fragment": response[:60],
                "tension_was": round(tension_val, 2),
            }
            self.doubted_traces.appendleft(doubt_record)
            return doubt_record

        return None

    def has_doubt(self) -> bool:
        return bool(self.doubted_traces)

    def get_doubt_atoms(self) -> List[str]:
        if not self.doubted_traces:
            return []
        return list(self.doubted_traces[0].get("atoms", []))

    def get_doubt_type(self) -> Optional[str]:
        if not self.doubted_traces:
            return None
        return self.doubted_traces[0].get("doubt_type")

    def consume_doubt(self) -> Optional[Dict[str, Any]]:
        if not self.doubted_traces:
            return None
        return self.doubted_traces.popleft()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doubted_traces": list(self.doubted_traces),
            "pending_review": self.pending_review,
        }

    def from_dict(self, d: Dict[str, Any]) -> None:
        for t in d.get("doubted_traces", []):
            self.doubted_traces.append(t)
        self.pending_review = d.get("pending_review")


class ReasoningTrace:
    """
    Garde une trace des influences qui ont pesé sur chaque réponse.
    Avec révision différée : elle peut douter d'elle-même.
    """

    def __init__(self, storage_path="data/reasoning_trace_default.json", maxlen=10):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self.traces: deque = deque(maxlen=maxlen)
        self.deferred = DeferredReview()
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f: data = json.load(f)
            for t in data.get("traces", []): self.traces.append(t)
            if "deferred" in data:
                self.deferred.from_dict(data["deferred"])
        except Exception: pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({"traces": list(self.traces),
                           "deferred": self.deferred.to_dict(),
                           "timestamp": _now()},
                          f, ensure_ascii=False, indent=2)
        except Exception: pass

    def record(self, payload: Dict[str, Any], response: str) -> Dict[str, Any]:
        # Exécuter la révision de la trace précédente avant d'enregistrer la nouvelle
        self.deferred.review()

        trace: Dict[str, Any] = {"timestamp": _now(), "response_fragment": response[:60]}

        lex = payload.get("lexical_impregnation_signal", {})
        if isinstance(lex, dict) and lex.get("words"):
            words = lex["words"]
            if words:
                top = sorted(words, key=lambda w: float(w.get("score", 0)) if isinstance(w, dict) else 0, reverse=True)
                trace["dominant_book_words"] = [w.get("surface", "") for w in top[:3] if isinstance(w, dict)]

        tensions = payload.get("unresolved_tensions", [])
        if tensions:
            t = tensions[0] if isinstance(tensions[0], dict) else {}
            trace["dominant_tension"] = t.get("book_says", t.get("description", ""))[:60]

        inter = payload.get("inter_book_tension_signal", {})
        if isinstance(inter, dict) and inter.get("tensions"):
            it = inter["tensions"][0]
            trace["inter_book_tension"] = {
                "concept": it.get("concept", ""),
                "book_a": it.get("book_a", ""),
                "book_b": it.get("book_b", ""),
            }

        emo = payload.get("emotional_state", {})
        if isinstance(emo, dict):
            tension_val = float(emo.get("tension", 0.5))
            fatigue_val = float(emo.get("fatigue", 0.3))
            valence_val = float(emo.get("tone", emo.get("valence", 0.5)))
            dominant = "tension" if tension_val > 0.6 else ("fatigue" if fatigue_val > 0.55 else "equilibre")
            if valence_val < 0.35: dominant = "obscurité"
            elif valence_val > 0.7: dominant = "ouverture"
            trace["dominant_emotion"] = dominant
            trace["emotion_values"] = {
                "tension": round(tension_val, 2),
                "fatigue": round(fatigue_val, 2),
                "valence": round(valence_val, 2),
            }

        op_sig = payload.get("opinion_signal", {})
        if isinstance(op_sig, dict) and op_sig.get("opinions"):
            ops = op_sig["opinions"]
            if ops:
                top_op = max(ops, key=lambda o: abs(float(o.get("certainty", 0))) if isinstance(o, dict) else 0)
                if isinstance(top_op, dict):
                    trace["dominant_opinion"] = {
                        "topic": top_op.get("topic", ""),
                        "position": round(float(top_op.get("position", 0.5)), 2),
                        "certainty": round(float(top_op.get("certainty", 0)), 2),
                    }

        self_sig = payload.get("self_model_signal", {})
        if isinstance(self_sig, dict) and self_sig.get("self_query_detected"):
            trace["self_query"] = True
            trace["self_atoms_used"] = self_sig.get("self_atoms", [])[:4]

        self.traces.append(trace)
        self.deferred.schedule(trace)
        self._save()
        return trace

    def is_why_question(self, user_input: str) -> bool:
        text = user_input.lower().strip()
        return any(p in text for p in _WHY_PATTERNS)

    def get_last_trace_atoms(self) -> List[str]:
        if not self.traces:
            return []
        trace = list(self.traces)[-1]
        atoms: List[str] = []
        for w in trace.get("dominant_book_words", [])[:2]:
            if w: atoms.append(w)
        tension = trace.get("dominant_tension", "")
        if tension:
            words = tension.split()[:3]
            atoms.extend(w for w in words if len(w) > 3)
        inter = trace.get("inter_book_tension", {})
        if inter:
            atoms.append(inter.get("concept", ""))
        emo = trace.get("dominant_emotion", "")
        if emo and emo != "equilibre":
            atoms.append(emo)
        op = trace.get("dominant_opinion", {})
        if op:
            atoms.append(op.get("topic", ""))
        return [a for a in atoms if a and len(a) > 2][:8]

    def signal(self, user_input: str = "") -> Dict[str, Any]:
        doubt_result = self.deferred.review()
        is_why = self.is_why_question(user_input)
        atoms = self.get_last_trace_atoms() if is_why else []
        return {
            "available": bool(self.traces),
            "why_question_detected": is_why,
            "why_atoms": atoms,
            "last_trace": dict(list(self.traces)[-1]) if self.traces else {},
            "has_doubt": self.deferred.has_doubt(),
            "doubt_atoms": self.deferred.get_doubt_atoms(),
            "doubt_type": self.deferred.get_doubt_type(),
            "new_doubt": doubt_result,
        }

    def consume_doubt(self) -> Optional[Dict[str, Any]]:
        result = self.deferred.consume_doubt()
        self._save()
        return result
