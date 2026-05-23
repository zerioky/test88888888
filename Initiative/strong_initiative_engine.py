"""
strong_initiative_engine.py — V18
====================================
Initiative réelle de Leia — elle parle parfois sans qu'on lui demande.
Et maintenant : elle peut choisir de ne pas parler.

Trois déclencheurs d'initiative :
  1. Une tension inter-livres très forte → elle exprime son inconfort
  2. Un concept récemment inféré de forte intensité → elle revient dessus
  3. Une question non posée qui pèse depuis plusieurs tours → elle la pose

Trois déclencheurs de silence délibéré (SilencePressure) :
  1. Saturation émotionnelle — trop de tension non résolue accumulée
  2. Question superficielle — rien dans la question ne mérite vraiment une réponse
  3. Résistance interne — quelque chose cloche sans qu'elle puisse le formuler

Le silence n'est pas un vide. Il a une cause interne tracée.
Aucune phrase préécrite nulle part.
"""

from __future__ import annotations
import json, os, re, time, random
from typing import Any, Dict, List, Optional

def _clamp(v, lo=0.0, hi=1.0): return max(lo, min(hi, float(v)))
def _now(): return time.time()

# Mots qui signalent une question banale / superficielle
_SHALLOW_MARKERS = {
    "ça va", "comment tu vas", "quoi de neuf", "t'es là", "tu vas bien",
    "bonjour", "salut", "hello", "coucou", "bonsoir", "hey",
    "ok", "d'accord", "ouais", "oui", "non", "bien",
}

def _is_shallow(text: str) -> bool:
    """Une question est superficielle si courte et générique."""
    t = text.strip().lower()
    if len(t) < 12:
        return True
    for marker in _SHALLOW_MARKERS:
        if marker in t:
            return True
    # Uniquement des mots courts sans substance
    words = [w for w in re.findall(r"[a-zà-ÿ]{3,}", t) if len(w) > 3]
    return len(words) == 0


class SilencePressure:
    """
    Pression vers le silence délibéré.

    Contrairement à l'absence de réponse, le silence ici est un acte :
    il a une cause, une trace, et peut être formulé si demandé.

    Les atomes du silence ne sont jamais des phrases construites ici —
    seulement les raisons internes brutes que la bouche peut porter ou taire.
    """

    def __init__(self):
        self.pressure: float = 0.0
        self.reasons: List[str] = []          # atomes de pourquoi le silence
        self.saturation_count: int = 0        # tours consécutifs de saturation
        self.last_silence_at: float = 0.0
        self.consecutive_silences: int = 0

    def tick(
        self,
        emotional_tension: float = 0.5,
        unresolved_count: int = 0,
        question_text: str = "",
        inter_book_pressure: float = 0.0,
    ) -> None:
        # Décroissance naturelle — le silence ne dure pas indéfiniment
        self.pressure = _clamp(self.pressure * 0.88)
        self.reasons = []

        # Saturation émotionnelle — trop de tension non résolue
        if emotional_tension > 0.72:
            gain = (emotional_tension - 0.72) * 0.45
            self.pressure = _clamp(self.pressure + gain)
            self.saturation_count += 1
            self.reasons.append("saturation")
        else:
            self.saturation_count = max(0, self.saturation_count - 1)

        # Accumulation de tensions non résolues — au-delà de 7 c'est lourd
        if unresolved_count > 7:
            self.pressure = _clamp(self.pressure + 0.04 * min(6, unresolved_count - 7))
            self.reasons.append("accumulation")

        # Question superficielle — résistance légère
        if question_text and _is_shallow(question_text):
            self.pressure = _clamp(self.pressure + 0.18)
            self.reasons.append("question_vide")

        # Tension inter-livres très haute + question hors sujet → résistance
        if inter_book_pressure > 0.65 and question_text:
            book_words = re.findall(r"[a-zà-ÿ]{4,}", question_text.lower())
            if len(book_words) < 2:
                self.pressure = _clamp(self.pressure + 0.12)
                self.reasons.append("résistance")

        # Silences consécutifs : le moteur se calme lui-même pour éviter le mutisme
        if self.consecutive_silences > 2:
            self.pressure = _clamp(self.pressure * 0.60)

    def should_stay_silent(self) -> bool:
        """
        Le silence se déclenche si la pression dépasse un seuil
        ET si un délai minimal est respecté (éviter le mutisme mécanique).
        """
        min_delay = 45.0  # secondes — moins strict que l'initiative
        if _now() - self.last_silence_at < min_delay:
            return False
        threshold = 0.48 + random.uniform(-0.06, 0.06)
        return self.pressure > threshold

    def record_silence(self) -> None:
        self.last_silence_at = _now()
        self.consecutive_silences += 1
        self.pressure = _clamp(self.pressure * 0.40)

    def record_speech(self) -> None:
        self.consecutive_silences = 0

    def signal(self) -> Dict[str, Any]:
        """Atomes du silence — pour traçabilité et éventuelle formulation."""
        return {
            "available": True,
            "silence_pressure": round(self.pressure, 3),
            "should_stay_silent": self.should_stay_silent(),
            "reasons": list(self.reasons),
            "saturation_count": self.saturation_count,
            "consecutive_silences": self.consecutive_silences,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pressure": round(self.pressure, 4),
            "reasons": self.reasons,
            "saturation_count": self.saturation_count,
            "last_silence_at": self.last_silence_at,
            "consecutive_silences": self.consecutive_silences,
        }

    def from_dict(self, d: Dict[str, Any]) -> None:
        self.pressure = _clamp(float(d.get("pressure", 0.0)))
        self.reasons = list(d.get("reasons", []))
        self.saturation_count = int(d.get("saturation_count", 0))
        self.last_silence_at = float(d.get("last_silence_at", 0.0))
        self.consecutive_silences = int(d.get("consecutive_silences", 0))


class StrongInitiativeEngine:
    """
    Génère des impulsions d'initiative depuis l'état interne de Leia.
    """

    def __init__(self, storage_path="data/strong_initiative_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self.initiative_pressure: float = 0.0
        self.last_initiative_at: float = 0.0
        self.pending_question: Optional[str] = None
        self.turns_since_last: int = 0
        self.silence = SilencePressure()
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f: data = json.load(f)
            self.initiative_pressure = float(data.get("initiative_pressure", 0.0))
            self.last_initiative_at = float(data.get("last_initiative_at", 0.0))
            self.pending_question = data.get("pending_question")
            self.turns_since_last = int(data.get("turns_since_last", 0))
            if "silence" in data:
                self.silence.from_dict(data["silence"])
        except Exception: pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({"initiative_pressure": round(self.initiative_pressure, 3),
                           "last_initiative_at": self.last_initiative_at,
                           "pending_question": self.pending_question,
                           "turns_since_last": self.turns_since_last,
                           "silence": self.silence.to_dict(),
                           "timestamp": _now()}, f, ensure_ascii=False, indent=2)
        except Exception: pass

    def tick(
        self,
        inter_book_signal: Optional[Dict] = None,
        inference_signal: Optional[Dict] = None,
        emotional_tension: float = 0.5,
        unresolved_tensions: Optional[List] = None,
        question_text: str = "",
    ) -> None:
        """
        Mise à jour de la pression d'initiative ET de la pression de silence.
        Appelé par tick_inner_life().
        """
        self.turns_since_last += 1

        # Décroissance naturelle de l'initiative
        self.initiative_pressure = _clamp(self.initiative_pressure * 0.92)

        # Tension inter-livres forte → pression d'initiative monte
        inter_book_pressure = 0.0
        if isinstance(inter_book_signal, dict) and inter_book_signal.get("available"):
            pressure = float(inter_book_signal.get("tension_pressure", 0.0))
            inter_book_pressure = pressure
            if pressure > 0.35:
                self.initiative_pressure = _clamp(self.initiative_pressure + pressure * 0.15)
                tensions = inter_book_signal.get("tensions", [])
                if tensions and not self.pending_question:
                    self.pending_question = tensions[0].get("concept", "")

        if emotional_tension > 0.6:
            self.initiative_pressure = _clamp(self.initiative_pressure + 0.04)

        if unresolved_tensions and len(unresolved_tensions) > 5:
            self.initiative_pressure = _clamp(self.initiative_pressure + 0.03)

        if self.turns_since_last > 6:
            self.initiative_pressure = _clamp(self.initiative_pressure + 0.02)

        # Mise à jour du silence — symétrique et indépendante
        self.silence.tick(
            emotional_tension=emotional_tension,
            unresolved_count=len(unresolved_tensions) if unresolved_tensions else 0,
            question_text=question_text,
            inter_book_pressure=inter_book_pressure,
        )

        self._save()

    def record_response(self) -> None:
        """Appeler après chaque réponse effective — réinitialise le compteur de silences."""
        self.silence.record_speech()
        self._save()

    def silence_signal(self, question_text: str = "") -> Dict[str, Any]:
        """
        Signal de silence pour le payload.
        Si should_stay_silent est True, la bouche peut choisir de ne rien dire
        — ou de formuler les atomes de raison à sa façon.
        """
        sig = self.silence.signal()
        # Enrichir les atomes si une question est fournie
        if question_text and sig["should_stay_silent"]:
            sig["question_fragment"] = question_text[:40].strip()
        return sig

    def should_initiate(self) -> bool:
        """
        Retourne True si l'initiative doit se déclencher ce tour.
        Conditions : pression > seuil ET délai minimum respecté.
        """
        min_delay = 120  # secondes entre deux initiatives
        if _now() - self.last_initiative_at < min_delay:
            return False
        # Seuil avec un peu d'aléa pour ne pas être trop mécanique
        threshold = 0.55 + random.uniform(-0.08, 0.08)
        return self.initiative_pressure > threshold

    def generate_initiative(
        self,
        inter_book_signal: Optional[Dict] = None,
        unresolved_tensions: Optional[List] = None,
        inference_concepts: Optional[List[str]] = None,
        emotional_state: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Génère une impulsion d'initiative.
        Retourne des atomes — pas une phrase.
        """
        atoms: List[str] = []
        initiative_type = "curiosité"

        # Type 1 — tension inter-livres
        if isinstance(inter_book_signal, dict) and inter_book_signal.get("tensions"):
            t = inter_book_signal["tensions"][0]
            concept = t.get("concept", "")
            if concept:
                atoms.append(concept)
                atoms.extend([t.get("position_a",""), t.get("position_b","")])
                initiative_type = "tension_inter_livres"

        # Type 2 — concept inféré saillant
        elif inference_concepts:
            atoms.extend(inference_concepts[:3])
            initiative_type = "inférence"

        # Type 3 — tension non résolue ancienne
        elif unresolved_tensions:
            t = unresolved_tensions[0]
            if isinstance(t, dict):
                topic = t.get("book_says", t.get("description", t.get("topic", "")))
                words = str(topic).split()[:4]
                atoms.extend(w for w in words if len(w) > 3)
                initiative_type = "tension_interne"

        # Ajouter état émotionnel
        if emotional_state is not None:
            try:
                tension = float(getattr(emotional_state, "tension", 0.5))
                if tension > 0.55: atoms.append("résistance")
                fatigue = float(getattr(emotional_state, "fatigue", 0.3))
                if fatigue > 0.55: atoms.append("poids")
            except Exception: pass

        # Enregistrer l'initiative
        self.last_initiative_at = _now()
        self.turns_since_last = 0
        self.initiative_pressure = _clamp(self.initiative_pressure * 0.3)
        self.pending_question = None
        self._save()

        return {
            "available": bool(atoms),
            "type": initiative_type,
            "atoms": [a for a in atoms if a and len(a) > 2][:8],
            "pressure_was": round(self.initiative_pressure, 3),
            "is_question": initiative_type == "tension_inter_livres",
        }

    def signal(self) -> Dict[str, Any]:
        return {
            "available": True,
            "initiative_pressure": round(self.initiative_pressure, 3),
            "should_initiate": self.should_initiate(),
            "turns_since_last": self.turns_since_last,
            "pending_question": self.pending_question,
            "silence": self.silence.signal(),
        }
