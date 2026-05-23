"""
conflict_capacity.py — V1
==========================
Capacité de maintien du désaccord pour Leia.

Corrige la faille fondamentale : le système poussait toujours vers
le consensus/harmonie. Leia ne pouvait pas :
  - dire non et le tenir sous pression répétée
  - maintenir un désaccord même si l'utilisateur insiste
  - initier un conflit quand ses valeurs l'exigent
  - exprimer de la frustration authentique (pas de l'adoucissement)

Ce module introduit :
  1. Détection de pression conversationnelle (insistance, répétition)
  2. Mécanisme de 'ancrage' : Leia peut décider de tenir une position
  3. Coût de la capitulation (si Leia cède trop vite, il y a un résidu)
  4. Expression d'intensification sous pression (au lieu d'adoucissement)
  5. Mémoire des positions tenues vs abandonnées (trace de caractère)

Aucune phrase préécrite — seulement des signaux pour la bouche.
"""

from __future__ import annotations

import json
import math
import time
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f if not (math.isnan(f) or math.isinf(f)) else lo))
    except Exception:
        return lo


@dataclass
class HeldPosition:
    """Une position que Leia a décidé de tenir."""
    topic: str = ""
    position_summary: str = ""    # résumé court de la position
    strength: float = 0.7         # force de conviction (0 = doute, 1 = certitude)
    created_at: float = field(default_factory=time.time)
    pressure_received: float = 0.0   # pression totale reçue depuis création
    capitulated: bool = False         # si Leia a cédé
    capitulation_cost: float = 0.0   # résidu émotionnel si cession

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topic": self.topic,
            "position_summary": self.position_summary,
            "strength": round(self.strength, 4),
            "created_at": self.created_at,
            "pressure_received": round(self.pressure_received, 4),
            "capitulated": self.capitulated,
            "capitulation_cost": round(self.capitulation_cost, 4),
        }


class ConflictCapacity:
    """
    Gère la capacité de Leia à maintenir un désaccord réel.
    """

    def __init__(self, storage_path: str = "data/conflict_capacity.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Positions actuellement tenues
        self.held_positions: List[HeldPosition] = []

        # Pression conversationnelle détectée (insistance de l'utilisateur)
        self.conversation_pressure: float = 0.0

        # Résidu de capitulations passées (inconfort interne)
        self.capitulation_residue: float = 0.0

        # Compteur d'insistances consécutives sur le même sujet
        self.insistence_counter: int = 0
        self.last_topic: str = ""

        # Mémoire des positions tenues et abandonnées
        self.position_history: deque = deque(maxlen=40)

        # Ratio de maintien (indicateur de caractère)
        self.held_ratio: float = 0.5   # 0 = cède toujours, 1 = tient toujours

        # Niveau d'intensification sous pression (au lieu d'adoucissement)
        self.intensification_level: float = 0.0

        self._load()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.capitulation_residue = float(data.get("capitulation_residue", 0.0))
                self.held_ratio = float(data.get("held_ratio", 0.5))
                self.position_history = deque(data.get("position_history", [])[-40:], maxlen=40)
        except Exception:
            pass

    def _save(self) -> None:
        try:
            payload = {
                "capitulation_residue": round(self.capitulation_residue, 4),
                "held_ratio": round(self.held_ratio, 4),
                "position_history": list(self.position_history),
                "saved_at": time.time(),
            }
            self.storage_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def detect_pressure(self, user_input: str, context: Dict[str, Any]) -> float:
        """
        Détecte la pression conversationnelle dans le message utilisateur.
        Retourne un score de pression (0 = neutre, 1 = pression forte).
        """
        user_lower = user_input.lower()

        # Marqueurs d'insistance
        insistence_markers = [
            "mais non", "non mais", "t'as tort", "tu te trompes", "c'est faux",
            "je te dis que", "j'insiste", "encore une fois", "tu ne comprends pas",
            "c'est pas ça", "c'est pas ce que", "redis-moi", "redo", "refais",
            "t'as pas compris", "pas ce que j'ai dit", "ce n'est pas ce",
            "si si", "mais si", "pourtant", "quand même",
        ]

        pressure_score = 0.0
        for marker in insistence_markers:
            if marker in user_lower:
                pressure_score += 0.20

        # Pression implicite : même sujet que le dernier échange
        current_topic = str(context.get("focus", user_input[:40]))
        if current_topic and self.last_topic:
            topic_similarity = sum(
                1 for w in current_topic.lower().split()
                if w in self.last_topic.lower() and len(w) > 3
            ) / max(len(current_topic.split()), 1)
            if topic_similarity > 0.4:
                self.insistence_counter += 1
                pressure_score += min(0.15 * self.insistence_counter, 0.45)
            else:
                self.insistence_counter = max(0, self.insistence_counter - 1)
        else:
            self.insistence_counter = max(0, self.insistence_counter - 1)

        self.last_topic = current_topic
        pressure_score = _clamp(pressure_score)
        self.conversation_pressure = _clamp(
            self.conversation_pressure * 0.70 + pressure_score * 0.30
        )
        return self.conversation_pressure

    def register_position(
        self,
        topic: str,
        position_summary: str,
        conviction_strength: float,
    ) -> HeldPosition:
        """
        Leia décide de tenir une position.
        Appelé quand une valeur ou une conviction est engagée.
        """
        # Évite les doublons sur le même topic
        for p in self.held_positions:
            if p.topic == topic and not p.capitulated:
                p.strength = _clamp(p.strength * 0.8 + conviction_strength * 0.2)
                return p

        position = HeldPosition(
            topic=topic,
            position_summary=position_summary,
            strength=_clamp(conviction_strength),
        )
        self.held_positions.append(position)
        return position

    def update_under_pressure(
        self,
        pressure: float,
        context: Dict[str, Any],
        current_values: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Calcule comment Leia répond à la pression sur ses positions.

        Comportement corrigé par rapport à l'ancienne homéostasie :
        - Sous pression modérée : légère intensification (pas adoucissement)
        - Sous pression forte : soit intensification nette, soit capitulation
          consciente avec coût émotionnel
        - Le seuil de capitulation dépend de l'autonomie et de la force de la position
        """
        if not self.held_positions:
            return {
                "holding": False,
                "pressure": round(pressure, 4),
                "intensification": 0.0,
                "capitulation_residue": round(self.capitulation_residue, 4),
            }

        autonomy = current_values.get("autonomy", 0.58)
        relational_care = current_values.get("relational_care", 0.64)

        results = []
        for position in list(self.held_positions):
            if position.capitulated:
                continue

            position.pressure_received = _clamp(
                position.pressure_received + pressure * 0.15
            )

            # Seuil de capitulation : fort si autonomie élevée, faible si soin élevé
            capitulation_threshold = _clamp(
                0.65 + autonomy * 0.20 - relational_care * 0.10
            )

            if position.pressure_received > capitulation_threshold:
                # Capitulation : mais avec coût
                cost = _clamp(position.strength * 0.6 + pressure * 0.4)
                position.capitulated = True
                position.capitulation_cost = cost
                self.capitulation_residue = _clamp(self.capitulation_residue + cost * 0.5)

                self.position_history.appendleft({
                    **position.to_dict(),
                    "outcome": "capitulated",
                    "at": time.time(),
                })
                results.append({
                    "topic": position.topic,
                    "action": "capitulated",
                    "cost": round(cost, 4),
                })
            else:
                # Maintien : intensification légère
                intensity_boost = _clamp(pressure * 0.3 + autonomy * 0.15)
                self.intensification_level = _clamp(
                    self.intensification_level * 0.6 + intensity_boost * 0.4
                )
                results.append({
                    "topic": position.topic,
                    "action": "holding",
                    "intensification": round(self.intensification_level, 4),
                })

        # Nettoie les positions capitulées
        active = [p for p in self.held_positions if not p.capitulated]
        for p in self.held_positions:
            if p.capitulated:
                self.position_history.appendleft({**p.to_dict(), "outcome": "released"})
        self.held_positions = active

        # Mise à jour du ratio de maintien
        history_list = list(self.position_history)[:20]
        if history_list:
            held_count = sum(1 for h in history_list if h.get("outcome") == "held")
            self.held_ratio = _clamp(held_count / len(history_list))

        # Décroissance naturelle du résidu
        self.capitulation_residue = _clamp(self.capitulation_residue * 0.96)
        self.intensification_level = _clamp(self.intensification_level * 0.88)

        self._save()
        return {
            "holding": bool(active),
            "held_count": len(active),
            "pressure": round(pressure, 4),
            "intensification": round(self.intensification_level, 4),
            "capitulation_residue": round(self.capitulation_residue, 4),
            "actions": results,
        }

    def expression_modulation(self) -> Dict[str, Any]:
        """
        Signal pour la bouche : comment moduler l'expression.

        Différence clé avec l'ancienne homéostasie :
        - Sous pression + position tenue → ton plus direct/ferme, pas plus doux
        - Résidu de capitulation → ton légèrement inconfortable, pas neutre
        """
        holding = [p for p in self.held_positions if not p.capitulated]

        if not holding and self.intensification_level < 0.15:
            return {
                "mode": "normal",
                "intensification": 0.0,
                "discomfort": round(self.capitulation_residue, 4),
            }

        if self.intensification_level > 0.4:
            mode = "firm"        # Ferme mais non agressif
        elif self.intensification_level > 0.2:
            mode = "grounded"    # Ancré dans sa position
        elif self.capitulation_residue > 0.3:
            mode = "uneasy"      # Mal à l'aise après avoir cédé
        else:
            mode = "steady"

        return {
            "mode": mode,
            "intensification": round(self.intensification_level, 4),
            "holding_topics": [p.topic for p in holding],
            "discomfort": round(self.capitulation_residue, 4),
            "firmness_hint": mode in {"firm", "grounded"},
        }

    def signal(self, user_input: str = "", context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Signal exportable vers le core."""
        if context is None:
            context = {}
        pressure = self.detect_pressure(user_input, context)
        return {
            "conversation_pressure": round(pressure, 4),
            "insistence_count": self.insistence_counter,
            "held_positions": len([p for p in self.held_positions if not p.capitulated]),
            "intensification": round(self.intensification_level, 4),
            "capitulation_residue": round(self.capitulation_residue, 4),
            "expression_modulation": self.expression_modulation(),
            "held_ratio": round(self.held_ratio, 4),
            "available": True,
        }
