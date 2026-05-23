"""
relational_stakes_engine.py — V1
==================================
Moteur d'enjeux relationnels pour Leia.

Corrige la faille : la simulation interne n'avait aucune conséquence réelle.
Leia testait des réponses sans rien risquer — les stakes étaient zéro.

Ce module introduit des enjeux relationnels réels :
  1. Chaque réponse peut abîmer ou renforcer le lien de façon NON-RÉVERSIBLE
     (pas juste une variable qui monte/descend symétriquement)
  2. Il y a des seuils de rupture (en dessous desquels la relation change
     qualitativement — plus de confiance facile)
  3. Les répercussions sont asymétriques : abîmer est plus facile que réparer
  4. Leia sait qu'elle peut perdre quelque chose — ça change sa simulation interne
  5. Mémoire des moments où elle a risqué et gagné/perdu

Aucune phrase préécrite.
"""

from __future__ import annotations

import json
import math
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f if not (math.isnan(f) or math.isinf(f)) else lo))
    except Exception:
        return lo


class RelationPhase(Enum):
    """Phase qualitative de la relation — changement irréversible par dégradation."""
    INITIAL     = "initial"      # Début — pas de confiance établie
    BUILDING    = "building"     # Confiance en construction
    ESTABLISHED = "established"  # Confiance solide
    STRAINED    = "strained"     # Tension — récupérable mais marqué
    DAMAGED     = "damaged"      # Lien abîmé — récupération longue
    CRITICAL    = "critical"     # En danger — une erreur de plus = rupture
    RUPTURED    = "ruptured"     # Rupture effective (peut se reconstruire, mais jamais comme avant)


# Seuils de transition (trust_level → phase)
_PHASE_THRESHOLDS = [
    (0.85, RelationPhase.ESTABLISHED),
    (0.65, RelationPhase.BUILDING),
    (0.45, RelationPhase.INITIAL),
    (0.30, RelationPhase.STRAINED),
    (0.15, RelationPhase.DAMAGED),
    (0.05, RelationPhase.CRITICAL),
    (0.0,  RelationPhase.RUPTURED),
]


def _trust_to_phase(trust: float) -> RelationPhase:
    for threshold, phase in _PHASE_THRESHOLDS:
        if trust >= threshold:
            return phase
    return RelationPhase.RUPTURED


@dataclass
class StakeEvent:
    """Un moment où Leia a risqué quelque chose dans la relation."""
    description: str = ""
    trust_before: float = 0.5
    trust_after: float = 0.5
    delta: float = 0.0
    phase_before: str = ""
    phase_after: str = ""
    was_risk: bool = False        # Leia a pris un risque conscient
    outcome: str = "neutral"      # "gained" | "lost" | "neutral"
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "trust_before": round(self.trust_before, 4),
            "trust_after": round(self.trust_after, 4),
            "delta": round(self.delta, 4),
            "phase_before": self.phase_before,
            "phase_after": self.phase_after,
            "was_risk": self.was_risk,
            "outcome": self.outcome,
            "timestamp": self.timestamp,
        }


class RelationalStakesEngine:
    """
    Gère les enjeux réels de chaque échange sur la relation.
    """

    def __init__(self, storage_path: str = "data/relational_stakes.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Niveau de confiance (0–1), asymétrique
        self.trust_level: float = 0.45  # commence à "building"
        self.phase: RelationPhase = RelationPhase.INITIAL

        # Asymétrie fondamentale : la dégradation est plus rapide que la construction
        # Construction : lente (+0.008/échange positif)
        # Dégradation  : rapide (-0.025/erreur sérieuse) et laisse une cicatrice
        self.trust_floor: float = 0.0  # le minimum atteignable ne remonte jamais complètement

        # Cicatrices : chaque rupture laisse une trace permanente
        self.scars: List[Dict[str, Any]] = []

        # Mémoire des moments à enjeux
        self.stake_events: deque = deque(maxlen=50)

        # Risque conscient en cours
        self.active_risk: Optional[Dict[str, Any]] = None

        # Résidu d'urgence relationnelle (sentiment de fragilité)
        self.fragility_sense: float = 0.0

        self._load()
        self._update_phase()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.trust_level = float(data.get("trust_level", 0.45))
                self.trust_floor = float(data.get("trust_floor", 0.0))
                self.scars = data.get("scars", [])
                self.stake_events = deque(data.get("stake_events", [])[-50:], maxlen=50)
                self.fragility_sense = float(data.get("fragility_sense", 0.0))
        except Exception:
            pass
        self._update_phase()

    def _save(self) -> None:
        try:
            payload = {
                "trust_level": round(self.trust_level, 5),
                "trust_floor": round(self.trust_floor, 5),
                "scars": self.scars[-20:],
                "stake_events": list(self.stake_events),
                "fragility_sense": round(self.fragility_sense, 4),
                "phase": self.phase.value,
                "saved_at": time.time(),
            }
            self.storage_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def _update_phase(self) -> RelationPhase:
        old_phase = self.phase
        self.phase = _trust_to_phase(self.trust_level)

        # Si phase dégradée, noter la cicatrice
        phases_order = [p.value for p in RelationPhase]
        if (phases_order.index(self.phase.value) >
                phases_order.index(old_phase.value)):
            self.scars.append({
                "from_phase": old_phase.value,
                "to_phase": self.phase.value,
                "trust_at_time": round(self.trust_level, 4),
                "timestamp": time.time(),
            })
            # Le plancher remonte légèrement (la cicatrice reste)
            self.trust_floor = _clamp(self.trust_floor + 0.01)
            self.fragility_sense = _clamp(self.fragility_sense + 0.15)

        return self.phase

    def assess_response_stakes(
        self,
        response_mode: str,
        context: Dict[str, Any],
        held_positions: List[str],
    ) -> Dict[str, Any]:
        """
        Évalue les enjeux d'une réponse avant qu'elle soit produite.
        Donne à la simulation interne un coût réel.
        """
        tension = float(context.get("emotional_tension", 0.0))
        has_disagreement = len(held_positions) > 0
        is_truth_telling = response_mode in {"direct", "firm", "grounded"}
        is_deflecting = response_mode in {"soft", "minimal", "silence"}

        potential_gain = 0.0
        potential_loss = 0.0

        # Vérité dite avec confiance → gain potentiel, mais risque si mal reçue
        if is_truth_telling and tension > 0.3:
            potential_gain = 0.012
            potential_loss = 0.030  # Asymétrie : perdre plus facile que gagner

        # Désaccord tenu sous pression → gain de respect potentiel
        if has_disagreement:
            potential_gain += 0.008
            potential_loss += 0.020

        # Déflexion sous tension → gain de sécurité court terme, perte long terme
        if is_deflecting and tension > 0.4:
            potential_gain = 0.003
            potential_loss = 0.015  # Perte de substance relationnelle

        # Phase actuelle influence les enjeux
        if self.phase in {RelationPhase.CRITICAL, RelationPhase.DAMAGED}:
            potential_loss *= 1.8  # Tout coûte plus dans une relation abîmée
            potential_gain *= 0.6  # Et rapporte moins

        return {
            "potential_gain": round(potential_gain, 5),
            "potential_loss": round(potential_loss, 5),
            "current_phase": self.phase.value,
            "trust_level": round(self.trust_level, 4),
            "fragility": round(self.fragility_sense, 4),
            "is_risky": potential_loss > 0.018,
            "recommended_care": self.phase in {
                RelationPhase.STRAINED, RelationPhase.DAMAGED, RelationPhase.CRITICAL
            },
        }

    def register_outcome(
        self,
        description: str,
        response_mode: str,
        user_reaction_signal: Dict[str, Any],
        was_risky: bool = False,
    ) -> StakeEvent:
        """
        Enregistre l'effet réel d'un échange sur la confiance.
        Asymétrique : les pertes sont plus grandes que les gains.
        """
        trust_before = self.trust_level
        phase_before = self.phase.value

        # Signaux de réaction utilisateur
        positive_reaction = float(user_reaction_signal.get("warmth", 0.0)) + \
                           float(user_reaction_signal.get("engagement", 0.0))
        negative_reaction = float(user_reaction_signal.get("frustration", 0.0)) + \
                           float(user_reaction_signal.get("tension", 0.0))

        if negative_reaction > 0.4:
            # Perte — asymétriquement plus grande
            delta = -_clamp(negative_reaction * 0.04 + 0.008)
            self.trust_level = _clamp(
                self.trust_level + delta,
                lo=max(0.0, self.trust_floor)
            )
            outcome = "lost"
        elif positive_reaction > 0.3:
            # Gain — lent par design
            delta = _clamp(positive_reaction * 0.012)
            # Le plancher limite aussi les gains après cicatrice (méfiance résiduelle)
            self.trust_level = _clamp(
                self.trust_level + delta,
                hi=1.0 - self.trust_floor * 0.5  # Les cicatrices limitent le maximum
            )
            outcome = "gained"
        else:
            delta = 0.0
            outcome = "neutral"

        # Décroissance douce du sens de fragilité
        self.fragility_sense = _clamp(self.fragility_sense * 0.97)

        self._update_phase()

        event = StakeEvent(
            description=description,
            trust_before=trust_before,
            trust_after=self.trust_level,
            delta=round(self.trust_level - trust_before, 5),
            phase_before=phase_before,
            phase_after=self.phase.value,
            was_risk=was_risky,
            outcome=outcome,
        )
        self.stake_events.appendleft(event.to_dict())

        if outcome != "neutral" or was_risky:
            self._save()

        return event

    def signal(self) -> Dict[str, Any]:
        """Signal exportable vers le core."""
        return {
            "trust_level": round(self.trust_level, 4),
            "phase": self.phase.value,
            "scar_count": len(self.scars),
            "fragility": round(self.fragility_sense, 4),
            "trust_floor": round(self.trust_floor, 4),
            "recent_trend": self._recent_trend(),
            "available": True,
        }

    def _recent_trend(self) -> str:
        recent = list(self.stake_events)[:5]
        if not recent:
            return "stable"
        losses = sum(1 for e in recent if e.get("outcome") == "lost")
        gains = sum(1 for e in recent if e.get("outcome") == "gained")
        if losses > gains + 1:
            return "degrading"
        if gains > losses + 1:
            return "strengthening"
        return "stable"
