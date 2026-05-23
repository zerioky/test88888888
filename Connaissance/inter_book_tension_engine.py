"""
inter_book_tension_engine.py — V17
====================================
Tensions entre livres lus par Leia.

Quand Leia lit deux livres qui s'opposent sur un même concept,
une tension inter-livres naît. Elle persiste, colore ses réponses,
et peut se formuler quand le sujet est abordé.
"""

from __future__ import annotations
import json, os, time
from typing import Any, Dict, List, Optional, Tuple

def _clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, float(v)))
def _now(): return time.time()

_OPPOSITION_AXES: List[Tuple[str, str]] = [
    ("mémoire","oubli"),("durée","instant"),("sens","absurde"),
    ("liberté","déterminisme"),("souffrance","bonheur"),("dieu","atheisme"),
    ("raison","sentiment"),("progrès","déclin"),("individu","société"),
    ("corps","esprit"),("mort","vie"),("temps","éternité"),
    ("action","contemplation"),("vérité","illusion"),("nature","culture"),
]

class InterBookTension:
    def __init__(self, concept, book_a, position_a, book_b, position_b, intensity=0.5):
        self.concept = concept
        self.book_a = book_a; self.position_a = position_a
        self.book_b = book_b; self.position_b = position_b
        self.intensity = _clamp(intensity)
        self.resolved = False
        self.created_at = _now(); self.last_activated = _now()

    def activate(self):
        self.last_activated = _now()
        self.intensity = _clamp(self.intensity + 0.05)

    def decay(self):
        age = _now() - self.last_activated
        if age > 86400: self.intensity = _clamp(self.intensity * 0.92)

    def to_dict(self):
        return {"concept":self.concept,"book_a":self.book_a,"position_a":self.position_a,
                "book_b":self.book_b,"position_b":self.position_b,
                "intensity":round(self.intensity,3),"resolved":self.resolved,
                "created_at":self.created_at,"last_activated":self.last_activated}

    @classmethod
    def from_dict(cls, d):
        t = cls(d.get("concept",""),d.get("book_a",""),d.get("position_a",""),
                d.get("book_b",""),d.get("position_b",""),float(d.get("intensity",0.5)))
        t.resolved = bool(d.get("resolved",False))
        t.created_at = float(d.get("created_at",_now()))
        t.last_activated = float(d.get("last_activated",_now()))
        return t


class InterBookTensionEngine:
    def __init__(self, storage_path="data/inter_book_tensions_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self.tensions: List[InterBookTension] = []
        self.book_concepts: Dict[str, Dict] = {}
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f: data = json.load(f)
            self.tensions = [InterBookTension.from_dict(t) for t in data.get("tensions",[])]
            self.book_concepts = data.get("book_concepts",{})
        except Exception: pass

    def _save(self):
        try:
            with open(self.storage_path,"w",encoding="utf-8") as f:
                json.dump({"tensions":[t.to_dict() for t in self.tensions[-40:]],
                           "book_concepts":{k:v for k,v in list(self.book_concepts.items())[-20:]},
                           "timestamp":_now()}, f, ensure_ascii=False, indent=2)
        except Exception: pass

    def register_book_concepts(self, title, concepts, relations=None):
        if not title or not concepts: return []
        self.book_concepts[title] = {"positive":[c for c in concepts if c],"relations":relations or []}
        new_tensions = []
        for other_title, other_data in self.book_concepts.items():
            if other_title == title: continue
            other_concepts = other_data.get("positive",[])
            for axis_a, axis_b in _OPPOSITION_AXES:
                this_has_a = any(axis_a in c.lower() for c in concepts)
                this_has_b = any(axis_b in c.lower() for c in concepts)
                other_has_a = any(axis_a in c.lower() for c in other_concepts)
                other_has_b = any(axis_b in c.lower() for c in other_concepts)
                tension_concept = pos_this = pos_other = None
                if this_has_a and other_has_b:
                    tension_concept, pos_this, pos_other = axis_a, axis_a, axis_b
                elif this_has_b and other_has_a:
                    tension_concept, pos_this, pos_other = axis_b, axis_b, axis_a
                if tension_concept and not self._tension_exists(tension_concept, title, other_title):
                    freq = sum(1 for c in concepts if tension_concept in c.lower())
                    freq_o = sum(1 for c in other_concepts if tension_concept in c.lower())
                    t = InterBookTension(tension_concept, title, pos_this, other_title, pos_other,
                                        _clamp(0.3 + (freq + freq_o) * 0.08))
                    self.tensions.append(t); new_tensions.append(t)
        self.tensions = self.tensions[-40:]
        self._save()
        return new_tensions

    def _tension_exists(self, concept, book_a, book_b):
        return any(t.concept == concept and
                   ((t.book_a==book_a and t.book_b==book_b) or (t.book_a==book_b and t.book_b==book_a))
                   for t in self.tensions)

    def activate_for_topic(self, topic):
        activated = []
        for t in self.tensions:
            if not t.resolved and (topic.lower() in t.concept.lower() or t.concept.lower() in topic.lower()):
                t.activate(); activated.append(t)
        return sorted(activated, key=lambda x: -x.intensity)

    def decay_all(self):
        for t in self.tensions: t.decay()
        self.tensions = [t for t in self.tensions if t.intensity > 0.08]

    def signal(self, topic=""):
        if topic: self.activate_for_topic(topic)
        active = sorted([t for t in self.tensions if not t.resolved and t.intensity > 0.2],
                        key=lambda x: -x.intensity)[:4]
        return {
            "available": bool(active),
            "tensions": [{"concept":t.concept,"book_a":t.book_a,"book_b":t.book_b,
                          "position_a":t.position_a,"position_b":t.position_b,
                          "intensity":round(t.intensity,3)} for t in active],
            "total_active": len([t for t in self.tensions if not t.resolved]),
            "tension_pressure": round(sum(t.intensity for t in active)/max(len(active),1),3) if active else 0.0,
            "tension_atoms": list({a for t in active for a in [t.concept,t.position_a,t.position_b] if a})[:8],
        }

    def snapshot(self):
        return {"total_tensions":len(self.tensions),
                "active_tensions":len([t for t in self.tensions if not t.resolved]),
                "books_indexed":len(self.book_concepts)}
