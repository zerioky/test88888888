
from __future__ import annotations
import time
from dataclasses import dataclass, field
from typing import Dict, List, Any


@dataclass
class LivedMoment:
    timestamp: float
    emotional_weight: float
    unresolved_tension: float
    relational_closeness: float
    memory_pressure: float
    continuity: float
    active_topics: List[str] = field(default_factory=list)


class UnifiedLivedExperience:
    """
    Fusionne les signaux séparés du système en une expérience vécue unique.
    Le but n'est PAS de générer du texte ici,
    mais de produire un état intérieur cohérent et continu.
    """

    def __init__(self):
        self.last_moment = None
        self.continuity_trace = 0.0
        self.unresolved_topics = []

    def build(
        self,
        affective_state: Dict[str, Any] | None = None,
        impulse_state: Dict[str, Any] | None = None,
        memory_state: Dict[str, Any] | None = None,
        presence_state: Dict[str, Any] | None = None,
    ) -> Dict[str, Any]:

        affective_state = affective_state or {}
        impulse_state = impulse_state or {}
        memory_state = memory_state or {}
        presence_state = presence_state or {}

        emotional_weight = float(
            affective_state.get("core_arousal", 0.0)
            or affective_state.get("tension", 0.0)
            or 0.0
        )

        unresolved = float(
            impulse_state.get("unfinished_pressure", 0.0)
            or impulse_state.get("latent_pressure", 0.0)
            or 0.0
        )

        closeness = float(
            presence_state.get("relational_presence", 0.0)
            or presence_state.get("warmth", 0.0)
            or 0.0
        )

        memory_pressure = float(
            memory_state.get("emotional_salience", 0.0)
            or memory_state.get("activation", 0.0)
            or 0.0
        )

        self.continuity_trace = (
            self.continuity_trace * 0.92
            + emotional_weight * 0.25
            + unresolved * 0.25
            + memory_pressure * 0.20
            + closeness * 0.15
        )

        topics = []
        if isinstance(memory_state.get("active_topics"), list):
            topics.extend(memory_state.get("active_topics"))

        if unresolved > 0.45 and topics:
            self.unresolved_topics = topics[:4]

        moment = LivedMoment(
            timestamp=time.time(),
            emotional_weight=emotional_weight,
            unresolved_tension=unresolved,
            relational_closeness=closeness,
            memory_pressure=memory_pressure,
            continuity=self.continuity_trace,
            active_topics=self.unresolved_topics[:]
        )

        self.last_moment = moment

        return {
            "lived_continuity": self.continuity_trace,
            "unresolved_tension": unresolved,
            "relational_closeness": closeness,
            "memory_pressure": memory_pressure,
            "active_topics": self.unresolved_topics[:],
            "is_living_moment": (
                self.continuity_trace > 0.25
                or unresolved > 0.25
            )
        }
