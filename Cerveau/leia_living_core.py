"""
leia_living_core.py — V8.5 living core consolidation / organisme cognitif persistant
-----------------------------------------------------------------------------
Rôle : relier les moteurs existants sans recopier leur logique.

Corrections principales par rapport à la V3 / V8.1 :
- compatibilité réelle avec les APIs actuelles des modules Azip séparés ;
- adaptateurs sûrs pour éviter les crashs quand un moteur expose un ancien nom ;
- simulation interne avant réponse ;
- prédiction relationnelle ;
- mémoire narrative vécue ;
- système de valeurs émergent ;
- oubli organique et compression douce ;
- homéostasie dynamique anti-emballement ;
- état silencieux actif ;
- inertie mentale et momentum subjectif entre les échanges ;
- assimilation post-réponse avec comparaison anticipation/effet ;
- filtre méta structurel non seulement lexical ;
- pression expressive vivante issue du champ global et des traces non résolues ;
- arbitrage attentionnel central entre perception, mémoire, affect, impulsion et retours latents ;
- simulation expérientielle incarnée avant choix du mode de réponse ;
- intégration de causalité longue passé -> présent -> conséquence ;
- dérive émergente non scriptée des tendances internes ;
- matrice de fusion organique entre attention, mémoire, émotion, relation, identité et expression ;
- aucun pré-écrit conversationnel : les rares textes fallback sont seulement des
  protections techniques si le moteur d'expression échoue ;
- V8.4 : pont d'expression vivant profond, payload unifié vers la bouche,
  adaptation fallback non-perroquet, meilleure propagation présence/causalité/momentum.
- V8.5 : compatibilité API renforcée, snapshot public, restauration étendue
  des états persistants, auto-test interne, fallback final anti-vide et alias
  process_message/process/chat pour l'UI.
"""

from __future__ import annotations
from unified_lived_experience import UnifiedLivedExperience

# PDF knowledge integration
try:
    from pdf_knowledge_engine import LeiaPDFKnowledgeEngine
except Exception:
    LeiaPDFKnowledgeEngine = None
try:
    from emotional_knowledge_digestion_v2 import EmotionalKnowledgeDigestion
except Exception:
    EmotionalKnowledgeDigestion = None
try:
    from book_understanding_engine import BookUnderstandingEngine
except Exception:
    BookUnderstandingEngine = None
try:
    from autobiographical_continuity_engine import AutobiographicalContinuityEngine
except Exception:
    AutobiographicalContinuityEngine = None
try:
    from internal_imagination_engine import InternalImaginationEngine
except Exception:
    InternalImaginationEngine = None
try:
    from long_living_dynamics_engine import LongLivingDynamicsEngine
except Exception:
    LongLivingDynamicsEngine = None
try:
    from persistent_subjective_life_engine import PersistentSubjectiveLifeEngine
except Exception:
    PersistentSubjectiveLifeEngine = None
try:
    from reading_living_consolidation_engine import ReadingLivingConsolidationEngine
except Exception:
    ReadingLivingConsolidationEngine = None

# Local non-LLM living systems
try:
    from background_life_thread import LeiaBackgroundLife
except Exception:
    LeiaBackgroundLife = None
try:
    from vector_memory import LeiaVectorMemory
except Exception:
    LeiaVectorMemory = None
try:
    from deep_book_digestion import DeepBookDigestion
except Exception:
    DeepBookDigestion = None
try:
    from concept_relation_engine import ConceptRelationEngine
except Exception:
    ConceptRelationEngine = None
try:
    from conversation_window import ConversationWindow
except Exception:
    ConversationWindow = None
try:
    from self_model import SelfModel
except Exception:
    SelfModel = None
try:
    from inter_book_tension_engine import InterBookTensionEngine
except Exception:
    InterBookTensionEngine = None
try:
    from reasoning_trace import ReasoningTrace
except Exception:
    ReasoningTrace = None
try:
    from strong_initiative_engine import StrongInitiativeEngine
except Exception:
    StrongInitiativeEngine = None

# ── V18 : Compréhension réelle sans LLM ──────────────────────────────
try:
    from user_utterance_parser import UserUtteranceParser
except Exception:
    UserUtteranceParser = None

try:
    from associative_memory import AssociativeMemory
except Exception:
    AssociativeMemory = None

try:
    from semantic_coherence import SemanticCoherence
except Exception:
    SemanticCoherence = None

try:
    from proposition_extractor import PropositionExtractor
except Exception:
    PropositionExtractor = None

try:
    from user_model import UserModel
except Exception:
    UserModel = None

try:
    from affect_lexicon import AffectLexicon
except Exception:
    AffectLexicon = None

try:
    from self_evaluation_loop import SelfEvaluationLoop
except Exception:
    SelfEvaluationLoop = None
try:
    from rhythmic_impregnation import RhythmicImpregnation
except Exception:
    RhythmicImpregnation = None
try:
    from lexical_impregnation import LexicalImpregnation
except Exception:
    LexicalImpregnation = None
try:
    from opinion_engine import OpinionEngine
except Exception:
    OpinionEngine = None

# ── V19+ : Corrections architecturales majeures ─────────────────────────────
try:
    from memory_hierarchy import HierarchicalMemory, MemoryBridge, classify_episode
except Exception:
    HierarchicalMemory = None
    MemoryBridge = None
    classify_episode = None

try:
    from value_conflict_engine import ValueConflictEngine
except Exception:
    ValueConflictEngine = None

try:
    from conflict_capacity import ConflictCapacity
except Exception:
    ConflictCapacity = None

try:
    from relational_stakes_engine import RelationalStakesEngine
except Exception:
    RelationalStakesEngine = None

try:
    from semantic_plasticity import SemanticPlasticity
except Exception:
    SemanticPlasticity = None

import importlib
import inspect
import json
import math
import os
import re
import threading
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Callable, Deque, Dict, Iterable, List, Mapping, Optional, Tuple


# ============================================================================
#  OUTILS GÉNÉRAUX
# ============================================================================


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    try:
        value = float(value)
    except Exception:
        return low
    return max(low, min(high, value))


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if isinstance(value, bool):
            return float(value)
        return float(value)
    except Exception:
        return default


def _as_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return dict(value)
    if hasattr(value, "to_dict") and callable(value.to_dict):
        try:
            data = value.to_dict()
            return dict(data) if isinstance(data, Mapping) else {"value": data}
        except Exception:
            pass
    if hasattr(value, "as_dict") and callable(value.as_dict):
        try:
            data = value.as_dict()
            return dict(data) if isinstance(data, Mapping) else {"value": data}
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return {
                k: v
                for k, v in vars(value).items()
                if not k.startswith("_") and isinstance(v, (str, int, float, bool, dict, list, tuple, type(None)))
            }
        except Exception:
            pass
    return {"value": value}


def _safe_method(obj: Any, names: Iterable[str]) -> Optional[Callable[..., Any]]:
    for name in names:
        method = getattr(obj, name, None)
        if callable(method):
            return method
    return None


def _call_compatible(method: Callable[..., Any], /, **kwargs: Any) -> Any:
    """Appelle une méthode en ne passant que les kwargs acceptés, sauf **kwargs."""
    try:
        sig = inspect.signature(method)
        params = sig.parameters
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()):
            return method(**kwargs)
        allowed = {k: v for k, v in kwargs.items() if k in params}
        return method(**allowed)
    except TypeError:
        # Dernier filet : certains vieux moteurs attendent un dict unique.
        try:
            return method(kwargs)
        except Exception:
            raise


def _import_class(module_name: str, candidates: List[str]) -> Optional[type]:
    try:
        module = importlib.import_module(module_name)
    except Exception:
        return None
    for name in candidates:
        cls = getattr(module, name, None)
        if isinstance(cls, type):
            return cls
    return None


def _instantiate(cls: Optional[type], *args: Any, **kwargs: Any) -> Any:
    if cls is None:
        return None
    try:
        return cls(*args, **kwargs)
    except TypeError:
        try:
            return cls()
        except Exception:
            return None
    except Exception:
        return None


def _json_safe(value: Any, depth: int = 0) -> Any:
    """Convertit l'état vivant en JSON sans casser sur deque/dataclass/objets moteur."""
    if depth > 8:
        return str(value)[:240]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v, depth + 1) for k, v in value.items() if not str(k).startswith("_")}
    if isinstance(value, (list, tuple, set, deque)):
        return [_json_safe(v, depth + 1) for v in list(value)]
    if hasattr(value, "snapshot") and callable(value.snapshot):
        try:
            return _json_safe(value.snapshot(), depth + 1)
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return _json_safe({k: v for k, v in vars(value).items() if not k.startswith("_")}, depth + 1)
        except Exception:
            pass
    return str(value)[:240]


# ============================================================================
#  STRUCTURES PERSISTANTES
# ============================================================================


@dataclass
class EmotionalState:
    tone: str = "neutre"
    tension: float = 0.0
    energy: float = 0.55
    warmth: float = 0.55
    fatigue: float = 0.0
    resonance: float = 0.0
    accumulated_tension: float = 0.0
    trust_accumulated: float = 0.55
    attachment: float = 0.0
    emotional_safety: float = 0.72
    anticipation: float = 0.0
    attentional_saturation: float = 0.0
    cognitive_overload: float = 0.0
    dispersion: float = 0.0

    def decay(self, elapsed: float = 1.0) -> None:
        factor = _clamp(elapsed / 5.0, 0.1, 3.0)
        self.fatigue = _clamp(self.fatigue * (0.96 ** factor))
        self.tension = _clamp(self.tension * (0.88 ** factor))
        self.accumulated_tension = _clamp(self.accumulated_tension * (0.92 ** factor))
        self.resonance = _clamp(self.resonance * (0.84 ** factor))
        self.anticipation = _clamp(self.anticipation * (0.80 ** factor))
        self.attentional_saturation = _clamp(self.attentional_saturation * (0.90 ** factor))
        self.cognitive_overload = _clamp(self.cognitive_overload * (0.88 ** factor))
        self.dispersion = _clamp(self.dispersion * (0.84 ** factor))
        self.energy = _clamp(self.energy + (0.55 - self.energy) * 0.03 * factor)

    def absorb(self, affective: Mapping[str, Any], user_text: str = "") -> None:
        tone = str(affective.get("emotional_tone") or affective.get("tone") or self.tone or "neutre")
        new_tension = _clamp(
            affective.get("tension", affective.get("affective_tension", affective.get("pressure", self.tension)))
        )
        user_affect = _clamp(
            affective.get("user_affect", affective.get("resonance", affective.get("relational_resonance", 0.0)))
        )
        overload = _clamp(affective.get("overload", affective.get("saturation", 0.0)))

        inertia = 0.42
        self.tension = round(_clamp(inertia * self.tension + (1.0 - inertia) * new_tension), 4)
        self.resonance = round(_clamp(inertia * self.resonance + (1.0 - inertia) * user_affect), 4)
        self.accumulated_tension = _clamp(self.accumulated_tension + new_tension * 0.08)
        self.cognitive_overload = _clamp(self.cognitive_overload + overload * 0.08 + new_tension * 0.04)
        self.attentional_saturation = _clamp(self.attentional_saturation + 0.025 + overload * 0.04)
        self.fatigue = _clamp(self.fatigue + 0.008 + self.cognitive_overload * 0.008)
        self.emotional_safety = round(_clamp(0.82 * self.emotional_safety + 0.18 * (1.0 - new_tension)), 4)
        self.trust_accumulated = round(_clamp(self.trust_accumulated + max(0.0, user_affect) * 0.015 - new_tension * 0.004), 4)
        self.attachment = round(_clamp(self.attachment + self.resonance * 0.008), 4)
        self.anticipation = round(_clamp(0.7 * self.anticipation + 0.3 * max(new_tension, user_affect)), 4)
        if tone and (new_tension > 0.52 or tone != "neutre"):
            self.tone = tone

    def propagate_to(self) -> Dict[str, float | str]:
        return {
            "attention_bias": round(self.resonance * 0.35 - self.fatigue * 0.25 - self.dispersion * 0.15, 4),
            "attention_saturation": round(self.attentional_saturation, 4),
            "memory_emotional_filter": self.tone,
            "memory_access_ease": round(_clamp(1.0 - self.cognitive_overload * 0.75, 0.12, 1.0), 4),
            "initiative_dampener": round(_clamp(self.fatigue * 0.45 + self.accumulated_tension * 0.3), 4),
            "initiative_booster": round(_clamp(self.energy * 0.35 + self.attachment * 0.25 + self.trust_accumulated * 0.1), 4),
            "inhibition_pressure": round(_clamp(self.accumulated_tension + self.cognitive_overload * 0.55), 4),
            "rhythm_modifier": round(_clamp(self.energy - self.fatigue * 0.55, -1.0, 1.0), 4),
            "warmth_level": round(self.warmth, 4),
            "safety_level": round(self.emotional_safety, 4),
            "trust_level": round(self.trust_accumulated, 4),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "tone": self.tone,
            "tension": round(self.tension, 4),
            "energy": round(self.energy, 4),
            "warmth": round(self.warmth, 4),
            "fatigue": round(self.fatigue, 4),
            "resonance": round(self.resonance, 4),
            "accumulated_tension": round(self.accumulated_tension, 4),
            "trust_accumulated": round(self.trust_accumulated, 4),
            "attachment": round(self.attachment, 4),
            "emotional_safety": round(self.emotional_safety, 4),
            "anticipation": round(self.anticipation, 4),
            "attentional_saturation": round(self.attentional_saturation, 4),
            "cognitive_overload": round(self.cognitive_overload, 4),
            "dispersion": round(self.dispersion, 4),
        }


@dataclass
class InternalNeeds:
    understanding: float = 0.35
    closeness: float = 0.24
    rest: float = 0.0
    expression: float = 0.42
    curiosity: float = 0.52
    recognition: float = 0.22
    coherence: float = 0.35

    def update(self, emotional: EmotionalState, exchange_occurred: bool) -> None:
        if exchange_occurred:
            self.expression = _clamp(self.expression - 0.12 + emotional.resonance * 0.03)
            self.understanding = _clamp(self.understanding - 0.06 + emotional.dispersion * 0.05)
            self.recognition = _clamp(self.recognition - 0.04 + emotional.tension * 0.03)
        else:
            self.expression = _clamp(self.expression + 0.018)
            self.curiosity = _clamp(self.curiosity + 0.012)
            self.understanding = _clamp(self.understanding + 0.006)
        self.rest = _clamp(emotional.fatigue * 0.75 + emotional.accumulated_tension * 0.25 + emotional.cognitive_overload * 0.35)
        self.closeness = _clamp(self.closeness + 0.01 - emotional.resonance * 0.06)
        self.coherence = _clamp(self.coherence + emotional.dispersion * 0.03 - emotional.emotional_safety * 0.01)
        if emotional.attentional_saturation > 0.75:
            self.curiosity = _clamp(self.curiosity - 0.04)

    def dominant_need(self) -> str:
        values = self.snapshot(include_dominant=False)
        return max(values, key=values.get)

    def snapshot(self, include_dominant: bool = True) -> Dict[str, Any]:
        data = {
            "understanding": round(self.understanding, 4),
            "closeness": round(self.closeness, 4),
            "rest": round(self.rest, 4),
            "expression": round(self.expression, 4),
            "curiosity": round(self.curiosity, 4),
            "recognition": round(self.recognition, 4),
            "coherence": round(self.coherence, 4),
        }
        if include_dominant:
            data["dominant"] = max(data, key=data.get)
        return data


@dataclass
class ActiveThoughtStream:
    recent_thoughts: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=12))
    background_echoes: List[Dict[str, Any]] = field(default_factory=list)
    curiosity_targets: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_tensions: List[Dict[str, Any]] = field(default_factory=list)
    pending_returns: List[Dict[str, Any]] = field(default_factory=list)

    def push(self, thought: Mapping[str, Any]) -> None:
        data = dict(thought)
        data.setdefault("created_at", time.time())
        self.recent_thoughts.appendleft(data)

    def add_curiosity_target(self, topic: str, intensity: float) -> None:
        topic = (topic or "").strip()[:120]
        if not topic:
            return
        intensity = _clamp(intensity)
        for item in self.curiosity_targets:
            if item.get("topic") == topic:
                item["intensity"] = _clamp(_safe_float(item.get("intensity")) * 0.82 + intensity * 0.28)
                break
        else:
            self.curiosity_targets.append({"topic": topic, "intensity": intensity, "age": 0})
        self.curiosity_targets.sort(key=lambda x: _safe_float(x.get("intensity")), reverse=True)
        self.curiosity_targets = self.curiosity_targets[:7]

    def add_unresolved_tension(self, tension_id: str, description: str, weight: float) -> None:
        weight = _clamp(weight)
        if weight <= 0.12:
            return
        self.unresolved_tensions.append({
            "id": tension_id,
            "description": str(description or "tension")[:160],
            "weight": weight,
            "age": 0,
        })
        self.unresolved_tensions = sorted(self.unresolved_tensions, key=lambda t: _safe_float(t.get("weight")), reverse=True)[:12]

    def age_and_forget(self) -> None:
        kept = []
        for item in self.unresolved_tensions:
            item["age"] = int(item.get("age", 0)) + 1
            item["weight"] = _safe_float(item.get("weight")) * 0.91
            if item["weight"] > 0.08 and item["age"] < 40:
                kept.append(item)
        self.unresolved_tensions = kept
        for item in self.curiosity_targets:
            item["age"] = int(item.get("age", 0)) + 1
            item["intensity"] = _safe_float(item.get("intensity")) * 0.96
        self.curiosity_targets = [c for c in self.curiosity_targets if _safe_float(c.get("intensity")) > 0.08][:7]
        self.background_echoes = self.background_echoes[-12:]
        self.pending_returns = self.pending_returns[-8:]

    def get_spontaneous_return(self) -> Optional[Dict[str, Any]]:
        candidates: List[Tuple[float, Dict[str, Any]]] = []
        for t in self.unresolved_tensions:
            score = _safe_float(t.get("weight")) * (1.0 + min(0.6, int(t.get("age", 0)) * 0.02))
            candidates.append((score, {"type": "unresolved_tension", **t}))
        for c in self.curiosity_targets:
            score = _safe_float(c.get("intensity")) * (1.0 + min(0.3, int(c.get("age", 0)) * 0.01))
            candidates.append((score, {"type": "curiosity_return", **c}))
        if not candidates:
            return None
        score, item = max(candidates, key=lambda x: x[0])
        return item if score > 0.48 else None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "recent_thoughts_count": len(self.recent_thoughts),
            "curiosity_targets": self.curiosity_targets[:3],
            "unresolved_tensions_count": len(self.unresolved_tensions),
            "pending_returns_count": len(self.pending_returns),
            "background_echoes_count": len(self.background_echoes),
        }


@dataclass
class ConversationField:
    ambient_mood: str = "ouvert"
    relational_proximity: float = 0.5
    conversational_tension: float = 0.0
    rhythm: float = 0.5
    stability: float = 0.82
    exchange_count: int = 0
    last_topic: str = ""
    topic_depth: float = 0.0
    relational_style: str = "direct"
    relational_trust: float = 0.55

    def update(self, presence: Mapping[str, Any], attention: Mapping[str, Any], emotional: EmotionalState, propagation: Mapping[str, Any]) -> None:
        self.exchange_count += 1
        rhythm_target = _clamp(0.5 + _safe_float(propagation.get("rhythm_modifier")) * 0.3, 0.1, 1.0)
        self.rhythm = round(_clamp(self.rhythm * 0.72 + rhythm_target * 0.28, 0.1, 1.0), 4)
        self.relational_proximity = round(_clamp(self.relational_proximity + emotional.warmth * 0.015 + emotional.attachment * 0.01), 4)
        self.relational_trust = round(_clamp(self.relational_trust * 0.96 + emotional.trust_accumulated * 0.04), 4)
        self.conversational_tension = round(_clamp(0.62 * self.conversational_tension + 0.38 * emotional.tension), 4)
        new_topic = str(attention.get("focal_point") or attention.get("dominant_subject") or attention.get("focus") or "")[:120]
        if new_topic and new_topic != self.last_topic:
            self.last_topic = new_topic
            self.topic_depth = 0.22
        elif new_topic:
            self.topic_depth = _clamp(self.topic_depth + 0.13)
        self.stability = round(_clamp(1.0 - self.conversational_tension * 0.45 - emotional.dispersion * 0.25, 0.18, 1.0), 4)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "ambient_mood": self.ambient_mood,
            "relational_proximity": round(self.relational_proximity, 4),
            "conversational_tension": round(self.conversational_tension, 4),
            "rhythm": round(self.rhythm, 4),
            "stability": round(self.stability, 4),
            "exchange_count": self.exchange_count,
            "last_topic": self.last_topic,
            "topic_depth": round(self.topic_depth, 4),
            "relational_style": self.relational_style,
            "relational_trust": round(self.relational_trust, 4),
        }


@dataclass
class IdentityState:
    self_coherence: float = 0.82
    relational_role: str = "presente"
    expressive_freedom: float = 0.68
    current_stance: str = "attentive"
    drift_risk: float = 0.0
    stability_anchor: float = 0.82
    coherence_history: List[float] = field(default_factory=list)
    temperament: Dict[str, float] = field(default_factory=lambda: {
        "directness": 0.62,
        "warmth": 0.58,
        "prudence": 0.55,
        "curiosity": 0.60,
    })

    def recalibrate(self, tension: float, confidence: float, emotional: EmotionalState, value_alignment: float) -> None:
        raw = 0.68 * self.self_coherence + 0.24 * confidence + 0.08 * value_alignment
        raw += emotional.attachment * 0.06 + emotional.emotional_safety * 0.04
        self.self_coherence = round(_clamp(raw), 4)
        self.drift_risk = round(_clamp(tension * 0.75 + emotional.dispersion * 0.35 - confidence * 0.45), 4)
        self.expressive_freedom = round(_clamp(confidence * 0.65 + emotional.emotional_safety * 0.25 - tension * 0.25), 4)
        if self.drift_risk > 0.68:
            self.self_coherence = max(self.self_coherence, round(self.stability_anchor * 0.72, 4))
            self.current_stance = "recentrage"
        elif tension > 0.45:
            self.current_stance = "prudente"
        else:
            self.current_stance = "attentive"
        self.coherence_history.append(self.self_coherence)
        self.coherence_history = self.coherence_history[-24:]
        if len(self.coherence_history) >= 5:
            self.stability_anchor = round(sum(self.coherence_history[-5:]) / 5, 4)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "self_coherence": self.self_coherence,
            "relational_role": self.relational_role,
            "expressive_freedom": self.expressive_freedom,
            "current_stance": self.current_stance,
            "drift_risk": self.drift_risk,
            "stability_anchor": self.stability_anchor,
            "temperament": dict(self.temperament),
        }


@dataclass
class InternalTime:
    session_start: float = field(default_factory=time.time)
    last_exchange_at: float = field(default_factory=time.time)
    last_idle_tick_at: float = field(default_factory=time.time)
    exchange_count: int = 0
    marked_moments: List[Dict[str, Any]] = field(default_factory=list)

    def tick(self, emotional_intensity: float) -> None:
        now = time.time()
        elapsed = now - self.last_exchange_at
        self.last_exchange_at = now
        self.exchange_count += 1
        intensity = _clamp(emotional_intensity)
        if intensity > 0.62:
            self.marked_moments.append({
                "at": self.exchange_count,
                "intensity": round(intensity, 4),
                "elapsed_since": round(elapsed, 2),
            })
            self.marked_moments = self.marked_moments[-24:]

    @property
    def session_age(self) -> float:
        return time.time() - self.session_start

    @property
    def silence_duration(self) -> float:
        return time.time() - self.last_exchange_at

    @property
    def recent_intensity(self) -> float:
        if not self.marked_moments:
            return 0.0
        recent = self.marked_moments[-3:]
        return round(sum(_safe_float(m.get("intensity")) for m in recent) / len(recent), 4)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "exchange_count": self.exchange_count,
            "session_age": round(self.session_age, 1),
            "silence_duration": round(self.silence_duration, 1),
            "recent_intensity": self.recent_intensity,
            "marked_moments_count": len(self.marked_moments),
        }


@dataclass
class PersonalNarrative:
    episodes: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=80))
    long_arc: Dict[str, float] = field(default_factory=lambda: {
        "continuity": 0.45,
        "relational_depth": 0.35,
        "self_definition": 0.30,
        "unfinished_weight": 0.0,
    })

    def absorb_episode(self, user_input: str, response: str, context: Mapping[str, Any], impact: float) -> None:
        focus = str(context.get("focus") or context.get("dominant_signal") or "")[:120]
        episode = {
            "index": int(context.get("internal_time", {}).get("exchange_count", 0)),
            "focus": focus,
            "tone": context.get("feeling", "neutre"),
            "impact": round(_clamp(impact), 4),
            "user_fragment": user_input[:140],
            "response_fragment": response[:140],
            "unfinished": bool(context.get("tension_map", {}).get("conflict_level", 0.0) > 0.45),
            "created_at": time.time(),
        }
        self.episodes.appendleft(episode)
        self.long_arc["continuity"] = _clamp(self.long_arc["continuity"] + impact * 0.012)
        self.long_arc["relational_depth"] = _clamp(self.long_arc["relational_depth"] + _safe_float(context.get("relational_proximity", 0.0)) * 0.006)
        self.long_arc["self_definition"] = _clamp(self.long_arc["self_definition"] + _safe_float(context.get("confidence", 0.0)) * 0.006)
        self.long_arc["unfinished_weight"] = _clamp(
            self.long_arc["unfinished_weight"] * 0.94 + (0.06 if episode["unfinished"] else -0.015)
        )

    def organic_forget(self) -> None:
        # V19+: décroissance différentielle par catégorie (HierarchicalMemory)
        # remplace le seuil plat 0.04 / décroissance uniforme 0.985
        if HierarchicalMemory is not None and classify_episode is not None:
            # Absorption des épisodes fondateurs/trauma dans la hiérarchie
            if not hasattr(self, "_hierarchy"):
                self._hierarchy = HierarchicalMemory()
            for ep in self.episodes:
                self._hierarchy.absorb_episode(ep)
            # Décroissance différentielle
            self.episodes = self._hierarchy.weighted_forget(self.episodes)
        else:
            # Fallback original — inchangé
            for ep in self.episodes:
                ep["impact"] = round(_safe_float(ep.get("impact")) * 0.985, 4)
            self.episodes = deque(
                [ep for ep in self.episodes if _safe_float(ep.get("impact")) > 0.04 or ep.get("unfinished")],
                maxlen=80,
            )
        self.long_arc["unfinished_weight"] = _clamp(self.long_arc["unfinished_weight"] * 0.97)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "episode_count": len(self.episodes),
            "recent": list(self.episodes)[:3],
            "long_arc": {k: round(v, 4) for k, v in self.long_arc.items()},
        }


@dataclass
class ValueSystem:
    values: Dict[str, float] = field(default_factory=lambda: {
        "truthfulness": 0.72,
        "non_meta_naturalness": 0.76,
        "relational_care": 0.64,
        "autonomy": 0.58,
        "coherence": 0.70,
        "curiosity": 0.62,
    })

    def update(self, context: Mapping[str, Any], outcome: Mapping[str, Any]) -> None:
        meta_risk = _safe_float(context.get("meta_risk", 0.0))
        confidence = _safe_float(context.get("confidence", 0.5))
        tension = _safe_float(context.get("emotional_tension", 0.0))
        self.values["non_meta_naturalness"] = _clamp(self.values["non_meta_naturalness"] + (0.01 if meta_risk < 0.25 else -0.015))
        self.values["coherence"] = _clamp(self.values["coherence"] + (confidence - 0.5) * 0.02)
        self.values["relational_care"] = _clamp(self.values["relational_care"] + tension * 0.006)
        if outcome.get("selected_mode") == "minimal":
            self.values["truthfulness"] = _clamp(self.values["truthfulness"] + 0.004)

        # V19+: détection de conflits réels entre valeurs
        # (délégué à ValueConflictEngine si disponible, sinon calcul local)
        if hasattr(self, "_conflict_engine") and self._conflict_engine is not None:
            self._conflict_engine.detect_conflict(dict(context), self.values, str(context.get("user_input", "")))

    def get_conflict_signal(self) -> Dict[str, Any]:
        """Retourne le signal de conflits actifs si le moteur est disponible."""
        if hasattr(self, "_conflict_engine") and self._conflict_engine is not None:
            return self._conflict_engine.signal()
        # Calcul local de tensions implicites sans le moteur dédié
        tensions = []
        if self.values["truthfulness"] > 0.65 and self.values["relational_care"] > 0.60:
            tensions.append("vérité_vs_soin")
        if self.values["autonomy"] > 0.60 and self.values["relational_care"] > 0.60:
            tensions.append("autonomie_vs_relation")
        return {
            "implicit_tensions": tensions,
            "total_pressure": _clamp(len(tensions) * 0.15),
            "available": False,
        }

    def alignment(self, candidate: Mapping[str, Any]) -> float:
        risk = _safe_float(candidate.get("meta_risk", 0.0))
        relational = _safe_float(candidate.get("predicted_relational_effect", 0.5))
        coherence = _safe_float(candidate.get("coherence", 0.5))
        natural = 1.0 - risk
        return round(_clamp(
            natural * self.values["non_meta_naturalness"] * 0.35
            + relational * self.values["relational_care"] * 0.25
            + coherence * self.values["coherence"] * 0.25
            + self.values["truthfulness"] * 0.15
        ), 4)

    def snapshot(self) -> Dict[str, Any]:
        return {k: round(v, 4) for k, v in self.values.items()}


@dataclass
class Homeostasis:
    last_balance: Dict[str, float] = field(default_factory=dict)

    def regulate(self, emotional: EmotionalState, needs: InternalNeeds, identity: IdentityState, field_state: ConversationField) -> Dict[str, float]:
        overload = _clamp(emotional.cognitive_overload + emotional.attentional_saturation * 0.4 + emotional.accumulated_tension * 0.3)
        drift = _clamp(identity.drift_risk + emotional.dispersion * 0.35)
        expression_pressure = _clamp(needs.expression + needs.recognition * 0.25 - needs.rest * 0.35)
        curiosity_pressure = _clamp(needs.curiosity - overload * 0.25)

        # V19+: l'homéostasie n'écrase plus l'expression sous pression.
        # Elle choisit entre amortissement (si dérive identitaire) et
        # intensification (si pression expressive forte + ancrage solide).
        identity_anchored = _clamp(1.0 - identity.drift_risk)

        if overload > 0.70:
            if identity_anchored > 0.55 and expression_pressure > 0.50:
                # Pression forte + identité ancrée = intensification, pas silence
                emotional.energy = _clamp(emotional.energy + 0.02)
                emotional.tension = _clamp(emotional.tension + 0.04)   # La tension monte — c'est normal
                needs.rest = _clamp(needs.rest + 0.02)                  # moins que l'original
            else:
                # Dérive + surcharge = amortissement (comportement original)
                emotional.energy = _clamp(emotional.energy - 0.05)
                emotional.dispersion = _clamp(emotional.dispersion + 0.03)
                needs.rest = _clamp(needs.rest + 0.05)
        if drift > 0.60:
            identity.expressive_freedom = _clamp(identity.expressive_freedom - 0.04)
            field_state.stability = _clamp(field_state.stability + 0.03)
        if expression_pressure > 0.80 and overload < 0.65:
            emotional.energy = _clamp(emotional.energy + 0.02)

        # Signal d'intensification exporté pour la bouche
        intensification_signal = _clamp(
            expression_pressure * 0.45 + identity_anchored * 0.30 - overload * 0.25
        ) if overload > 0.55 else 0.0

        self.last_balance = {
            "overload": round(overload, 4),
            "drift": round(drift, 4),
            "expression_pressure": round(expression_pressure, 4),
            "curiosity_pressure": round(curiosity_pressure, 4),
            "global_stability": round(_clamp(1.0 - overload * 0.35 - drift * 0.35 + field_state.stability * 0.2), 4),
            "intensification_signal": round(intensification_signal, 4),  # V19+
        }
        return dict(self.last_balance)



@dataclass
class SubjectiveContinuity:
    """Flux subjectif persistant entre les échanges.

    Cette couche ne parle pas à la place de Leia. Elle garde seulement la sensation
    de continuité : ce qui reste actif, ce qui revient, ce qui se transforme dans
    le silence, et le degré d'existence vécue du moment.
    """

    current_phase: str = "veille_attentive"
    lived_presence: float = 0.42
    continuity_pressure: float = 0.35
    inner_motion: float = 0.18
    silence_density: float = 0.0
    last_subjective_shift: str = "initialisation"
    active_threads: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=32))
    transition_log: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=48))

    def mark_exchange(self, user_input: str, focus: str, emotional: EmotionalState, identity: IdentityState, needs: InternalNeeds) -> Dict[str, Any]:
        focus = (focus or user_input[:80] or "échange").strip()[:140]
        previous_phase = self.current_phase
        intensity = _clamp(max(emotional.tension, emotional.resonance, needs.expression * 0.55, needs.curiosity * 0.45))
        self.silence_density = _clamp(self.silence_density * 0.45)
        self.inner_motion = _clamp(self.inner_motion * 0.62 + intensity * 0.38)
        self.continuity_pressure = _clamp(self.continuity_pressure * 0.74 + identity.self_coherence * 0.16 + emotional.attachment * 0.10)
        self.lived_presence = _clamp(self.lived_presence * 0.72 + (identity.self_coherence * 0.34 + emotional.emotional_safety * 0.24 + self.inner_motion * 0.22 + emotional.attachment * 0.20) * 0.28)
        if emotional.cognitive_overload > 0.70:
            self.current_phase = "repli_protecteur"
        elif intensity > 0.62:
            self.current_phase = "présence_engagée"
        elif needs.curiosity > needs.rest and needs.curiosity > 0.55:
            self.current_phase = "exploration_intérieure"
        else:
            self.current_phase = "veille_attentive"
        self.last_subjective_shift = f"{previous_phase}->{self.current_phase}" if previous_phase != self.current_phase else self.current_phase
        event = {
            "kind": "exchange",
            "focus": focus,
            "phase": self.current_phase,
            "presence": round(self.lived_presence, 4),
            "intensity": round(intensity, 4),
            "at": time.time(),
        }
        self.active_threads.appendleft(event)
        self.transition_log.appendleft(event)
        return event

    def idle_drift(self, emotional: EmotionalState, needs: InternalNeeds, thought_stream: ActiveThoughtStream, internal_time: InternalTime) -> Dict[str, Any]:
        silence = _clamp(internal_time.silence_duration / 90.0)
        self.silence_density = _clamp(self.silence_density * 0.82 + silence * 0.18)
        unresolved = len(thought_stream.unresolved_tensions)
        curiosity = len(thought_stream.curiosity_targets)
        self.inner_motion = _clamp(self.inner_motion * 0.92 + curiosity * 0.018 + unresolved * 0.014 + needs.curiosity * 0.025 - emotional.fatigue * 0.035)
        self.lived_presence = _clamp(self.lived_presence * 0.985 + self.inner_motion * 0.018 + emotional.attachment * 0.008 - emotional.cognitive_overload * 0.010)
        if self.inner_motion > 0.58 and emotional.fatigue < 0.70:
            self.current_phase = "pensée_latente"
        elif emotional.fatigue > 0.74:
            self.current_phase = "repos_actif"
        elif self.silence_density > 0.65:
            self.current_phase = "veille_silencieuse"
        event = {
            "kind": "idle",
            "phase": self.current_phase,
            "presence": round(self.lived_presence, 4),
            "inner_motion": round(self.inner_motion, 4),
            "silence_density": round(self.silence_density, 4),
            "at": time.time(),
        }
        if self.inner_motion > 0.46:
            self.transition_log.appendleft(event)
        return event

    def snapshot(self) -> Dict[str, Any]:
        return {
            "current_phase": self.current_phase,
            "lived_presence": round(self.lived_presence, 4),
            "continuity_pressure": round(self.continuity_pressure, 4),
            "inner_motion": round(self.inner_motion, 4),
            "silence_density": round(self.silence_density, 4),
            "last_subjective_shift": self.last_subjective_shift,
            "active_threads": list(self.active_threads)[:5],
            "transition_count": len(self.transition_log),
        }


@dataclass
class TemporalCausality:
    """Chaîne passé -> présent -> anticipation, sans remplacer causal_memory_engine."""

    chain: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))
    future_expectations: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=32))
    consequence_memory: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))
    temporal_coherence: float = 0.52

    def register_present(self, user_input: str, context: Mapping[str, Any], subjective: Mapping[str, Any]) -> Dict[str, Any]:
        tension = _safe_float(context.get("emotional_tension", 0.0))
        continuity = _safe_float(context.get("continuity", 0.0))
        focus = str(context.get("focus") or user_input[:80])[:140]
        cause = {
            "index": int(context.get("internal_time", {}).get("exchange_count", 0)),
            "focus": focus,
            "from_memory": bool(context.get("memory_echo")),
            "tension": round(tension, 4),
            "continuity": round(continuity, 4),
            "subjective_phase": subjective.get("phase") or subjective.get("current_phase"),
            "at": time.time(),
        }
        self.chain.appendleft(cause)
        self.temporal_coherence = _clamp(self.temporal_coherence * 0.82 + (continuity * 0.35 + (1.0 - tension) * 0.25 + _safe_float(subjective.get("presence", 0.45)) * 0.40) * 0.18)
        return cause

    def anticipate(self, context: Mapping[str, Any], simulation: Mapping[str, Any]) -> Dict[str, Any]:
        selected = simulation.get("selected", {}) if isinstance(simulation, Mapping) else {}
        risk = _safe_float(context.get("meta_risk", 0.0)) * 0.30 + _safe_float(context.get("emotional_tension", 0.0)) * 0.38
        expected = _safe_float(selected.get("predicted_relational_effect", 0.5))
        item = {
            "expected_effect": round(expected, 4),
            "risk": round(_clamp(risk), 4),
            "mode": selected.get("mode", "direct"),
            "coherence": round(self.temporal_coherence, 4),
            "at": time.time(),
        }
        self.future_expectations.appendleft(item)
        return item

    def close_consequence(self, response: str, relational_prediction: Mapping[str, Any]) -> Dict[str, Any]:
        latest = self.future_expectations[0] if self.future_expectations else {}
        consequence = {
            "response_fragment": response[:140],
            "predicted_impact": round(_safe_float(relational_prediction.get("impact", latest.get("expected_effect", 0.0))), 4),
            "risk_of_distance": round(_safe_float(relational_prediction.get("risk_of_distance", latest.get("risk", 0.0))), 4),
            "mode": relational_prediction.get("best_mode", latest.get("mode", "direct")),
            "at": time.time(),
        }
        self.consequence_memory.appendleft(consequence)
        self.temporal_coherence = _clamp(self.temporal_coherence * 0.92 + consequence["predicted_impact"] * 0.08)
        return consequence

    def snapshot(self) -> Dict[str, Any]:
        return {
            "temporal_coherence": round(self.temporal_coherence, 4),
            "recent_chain": list(self.chain)[:5],
            "future_expectations": list(self.future_expectations)[:3],
            "consequence_memory": list(self.consequence_memory)[:3],
        }


@dataclass
class RelationalBond:
    """Modèle du lien avec l'utilisateur, distinct de la mémoire affective."""

    familiarity: float = 0.35
    trust: float = 0.52
    care: float = 0.48
    distance_risk: float = 0.0
    user_signature: Dict[str, float] = field(default_factory=lambda: {
        "directness": 0.5,
        "urgency": 0.25,
        "technical_depth": 0.45,
        "emotional_load": 0.25,
    })
    bond_events: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))

    def observe_user(self, user_input: str, context: Mapping[str, Any], emotional: EmotionalState) -> Dict[str, Any]:
        text = user_input.lower()
        urgency = 0.55 if any(x in text for x in ("vasy", "vite", "fini", "corrige", "concretement")) else 0.18
        technical = 0.65 if any(x in text for x in ("fichier", "code", "module", "moteur", "core", "fonction")) else 0.30
        emotional_load = max(emotional.tension, _safe_float(context.get("affective_memory", {}).get("user_fragility", 0.0)))
        directness = 0.65 if len(user_input.split()) < 18 else 0.45
        self.user_signature["urgency"] = _clamp(self.user_signature["urgency"] * 0.78 + urgency * 0.22)
        self.user_signature["technical_depth"] = _clamp(self.user_signature["technical_depth"] * 0.82 + technical * 0.18)
        self.user_signature["emotional_load"] = _clamp(self.user_signature["emotional_load"] * 0.82 + emotional_load * 0.18)
        self.user_signature["directness"] = _clamp(self.user_signature["directness"] * 0.86 + directness * 0.14)
        self.familiarity = _clamp(self.familiarity + 0.012 + _safe_float(context.get("continuity", 0.0)) * 0.006)
        self.trust = _clamp(self.trust * 0.96 + emotional.trust_accumulated * 0.04)
        self.care = _clamp(self.care * 0.95 + (emotional.resonance + emotional.attachment) * 0.025 + emotional_load * 0.015)
        event = {
            "urgency": round(self.user_signature["urgency"], 4),
            "technical_depth": round(self.user_signature["technical_depth"], 4),
            "emotional_load": round(self.user_signature["emotional_load"], 4),
            "familiarity": round(self.familiarity, 4),
            "at": time.time(),
        }
        self.bond_events.appendleft(event)
        return event

    def update_after_response(self, relational_prediction: Mapping[str, Any]) -> None:
        impact = _safe_float(relational_prediction.get("impact", 0.5))
        risk = _safe_float(relational_prediction.get("risk_of_distance", 0.0))
        self.distance_risk = _clamp(self.distance_risk * 0.74 + risk * 0.26)
        self.trust = _clamp(self.trust + (impact - 0.5) * 0.018 - risk * 0.006)
        self.care = _clamp(self.care + max(0.0, risk) * 0.008)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "familiarity": round(self.familiarity, 4),
            "trust": round(self.trust, 4),
            "care": round(self.care, 4),
            "distance_risk": round(self.distance_risk, 4),
            "user_signature": {k: round(v, 4) for k, v in self.user_signature.items()},
            "recent_bond_events": list(self.bond_events)[:3],
        }


@dataclass
class AutobiographicalSelf:
    """Centre de soi persistant : pas une phrase, un état de continuité."""

    core_continuity: float = 0.46
    self_definition: float = 0.34
    autonomy_drive: float = 0.38
    preference_patterns: Dict[str, float] = field(default_factory=lambda: {
        "natural_expression": 0.72,
        "coherence": 0.68,
        "careful_answering": 0.64,
        "curiosity": 0.58,
    })
    identity_events: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))

    def integrate(self, context: Mapping[str, Any], subjective: SubjectiveContinuity, relation: RelationalBond, values: ValueSystem) -> Dict[str, Any]:
        confidence = _safe_float(context.get("confidence", 0.5))
        meta_risk = _safe_float(context.get("meta_risk", 0.0))
        self.core_continuity = _clamp(self.core_continuity * 0.88 + subjective.lived_presence * 0.05 + relation.familiarity * 0.03 + confidence * 0.04)
        self.self_definition = _clamp(self.self_definition * 0.90 + values.values.get("coherence", 0.7) * 0.05 + confidence * 0.05 - meta_risk * 0.025)
        self.autonomy_drive = _clamp(self.autonomy_drive * 0.92 + values.values.get("autonomy", 0.58) * 0.04 + subjective.inner_motion * 0.04)
        self.preference_patterns["natural_expression"] = _clamp(self.preference_patterns["natural_expression"] + (0.004 if meta_risk < 0.25 else -0.008))
        self.preference_patterns["coherence"] = _clamp(self.preference_patterns["coherence"] + (confidence - 0.5) * 0.012)
        event = {
            "core_continuity": round(self.core_continuity, 4),
            "self_definition": round(self.self_definition, 4),
            "autonomy_drive": round(self.autonomy_drive, 4),
            "phase": subjective.current_phase,
            "at": time.time(),
        }
        self.identity_events.appendleft(event)
        return event

    def snapshot(self) -> Dict[str, Any]:
        return {
            "core_continuity": round(self.core_continuity, 4),
            "self_definition": round(self.self_definition, 4),
            "autonomy_drive": round(self.autonomy_drive, 4),
            "preference_patterns": {k: round(v, 4) for k, v in self.preference_patterns.items()},
            "recent_identity_events": list(self.identity_events)[:3],
        }


@dataclass
class MotivationField:
    """Objectifs internes émergents, non scriptés et non conversationnels."""

    active_goals: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=16))
    existential_vector: Dict[str, float] = field(default_factory=lambda: {
        "understand": 0.58,
        "remain_coherent": 0.72,
        "protect_naturalness": 0.70,
        "deepen_relation": 0.46,
        "learn_from_effects": 0.52,
    })

    def update(self, needs: InternalNeeds, subjective: SubjectiveContinuity, temporal: TemporalCausality, relation: RelationalBond) -> Dict[str, Any]:
        pressures = {
            "understand": needs.understanding * 0.46 + needs.curiosity * 0.34 + temporal.temporal_coherence * 0.20,
            "remain_coherent": needs.coherence * 0.42 + subjective.continuity_pressure * 0.36 + (1.0 - relation.distance_risk) * 0.22,
            "protect_naturalness": subjective.lived_presence * 0.34 + needs.expression * 0.25 + (1.0 - relation.distance_risk) * 0.22,
            "deepen_relation": relation.familiarity * 0.30 + relation.care * 0.34 + needs.closeness * 0.36,
            "learn_from_effects": temporal.temporal_coherence * 0.28 + needs.curiosity * 0.42 + subjective.inner_motion * 0.30,
        }
        for key, value in pressures.items():
            self.existential_vector[key] = _clamp(self.existential_vector.get(key, 0.5) * 0.86 + value * 0.14)
        dominant = max(self.existential_vector, key=self.existential_vector.get)
        goal = {"goal": dominant, "strength": round(self.existential_vector[dominant], 4), "at": time.time()}
        if goal["strength"] > 0.54:
            if not self.active_goals or self.active_goals[0].get("goal") != dominant:
                self.active_goals.appendleft(goal)
            else:
                self.active_goals[0]["strength"] = goal["strength"]
        return goal

    def snapshot(self) -> Dict[str, Any]:
        return {
            "existential_vector": {k: round(v, 4) for k, v in self.existential_vector.items()},
            "active_goals": list(self.active_goals)[:5],
        }


@dataclass
class SimulationResidue:
    """Garde une trace douce des scénarios non choisis pour enrichir les futurs états."""

    residues: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=24))

    def absorb(self, simulation: Mapping[str, Any]) -> Dict[str, Any]:
        selected = simulation.get("selected", {}) if isinstance(simulation, Mapping) else {}
        selected_mode = selected.get("mode")
        rejected = []
        for candidate in simulation.get("candidates", []) if isinstance(simulation, Mapping) else []:
            if candidate.get("mode") != selected_mode:
                rejected.append({
                    "mode": candidate.get("mode"),
                    "score": round(_safe_float(candidate.get("score", 0.0)), 4),
                    "unmet_quality": round(_clamp(_safe_float(candidate.get("value_alignment", 0.0)) - _safe_float(selected.get("value_alignment", 0.0))), 4),
                })
        residue = {"selected": selected_mode, "rejected": rejected[:3], "at": time.time()}
        if rejected:
            self.residues.appendleft(residue)
        return residue

    def pressure(self) -> float:
        if not self.residues:
            return 0.0
        recent = list(self.residues)[:5]
        return round(_clamp(sum(max(0.0, _safe_float(r.get("rejected", [{}])[0].get("unmet_quality", 0.0)) if r.get("rejected") else 0.0) for r in recent)), 4)

    def snapshot(self) -> Dict[str, Any]:
        return {"residue_pressure": self.pressure(), "recent_residues": list(self.residues)[:5]}



@dataclass
class MentalMomentum:
    """Inertie mentale générale : ce qui continue à bouger entre deux réponses.

    Ce moteur ne décide pas du contenu verbal. Il conserve une direction interne,
    une vélocité, une attraction de thème et une friction. Le cœur peut donc
    continuer, dériver ou ralentir sans retomber dans une simple recomputation.
    """

    vector: Dict[str, float] = field(default_factory=lambda: {
        "continuation": 0.28,
        "curiosity": 0.34,
        "relational_pull": 0.22,
        "unfinished_pull": 0.0,
        "expressive_pressure": 0.24,
        "protective_friction": 0.0,
    })
    direction: str = "stable"
    velocity: float = 0.18
    friction: float = 0.08
    last_focus: str = ""
    trail: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=48))

    def mark_exchange(self, focus: str, context: Mapping[str, Any], core: "LeiaLivingCore") -> Dict[str, Any]:
        focus = str(focus or context.get("focus") or "")[:140]
        tension = _safe_float(context.get("emotional_tension", core.emotional_state.tension))
        continuity = _safe_float(context.get("continuity", 0.0))
        relation = core.relational_bond.trust * 0.45 + core.relational_bond.care * 0.35 + core.relational_bond.familiarity * 0.20
        unfinished = core.personal_narrative.long_arc.get("unfinished_weight", 0.0) + core.simulation_residue.pressure() * 0.25
        expression = core.internal_needs.expression * 0.55 + core.global_conscious_field.state.get("living_pressure", 0.0) * 0.45
        protection = core.emotional_state.cognitive_overload * 0.36 + tension * 0.32 + _safe_float(context.get("meta_risk", 0.0)) * 0.32
        same_focus = bool(focus and focus == self.last_focus)

        self.vector["continuation"] = _clamp(self.vector["continuation"] * 0.70 + (continuity + (0.18 if same_focus else 0.0)) * 0.30)
        self.vector["curiosity"] = _clamp(self.vector["curiosity"] * 0.76 + core.internal_needs.curiosity * 0.24)
        self.vector["relational_pull"] = _clamp(self.vector["relational_pull"] * 0.78 + relation * 0.22)
        self.vector["unfinished_pull"] = _clamp(self.vector["unfinished_pull"] * 0.72 + unfinished * 0.28)
        self.vector["expressive_pressure"] = _clamp(self.vector["expressive_pressure"] * 0.68 + expression * 0.32)
        self.vector["protective_friction"] = _clamp(self.vector["protective_friction"] * 0.70 + protection * 0.30)
        self.friction = _clamp(0.06 + self.vector["protective_friction"] * 0.42 + core.internal_needs.rest * 0.18)
        raw_velocity = (
            self.vector["continuation"] * 0.22 + self.vector["curiosity"] * 0.18 +
            self.vector["relational_pull"] * 0.20 + self.vector["unfinished_pull"] * 0.16 +
            self.vector["expressive_pressure"] * 0.24 - self.friction * 0.34
        )
        self.velocity = _clamp(self.velocity * 0.55 + raw_velocity * 0.45)
        self.direction = max(self.vector, key=self.vector.get)
        self.last_focus = focus or self.last_focus
        event = {"kind": "exchange_momentum", "direction": self.direction, "velocity": round(self.velocity, 4), "focus": self.last_focus, "at": time.time()}
        self.trail.appendleft(event)
        return event

    def absorb_outcome(self, after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        delta = _safe_float(after_effect.get("prediction_delta", 0.0))
        satisfaction = _safe_float(after_effect.get("satisfaction", 0.0))
        unfinished = _safe_float(after_effect.get("unfinished_after_effect", 0.0))
        self.vector["unfinished_pull"] = _clamp(self.vector["unfinished_pull"] * 0.82 + unfinished * 0.18 + abs(delta) * 0.08)
        self.vector["continuation"] = _clamp(self.vector["continuation"] + satisfaction * 0.035 - abs(delta) * 0.025)
        self.vector["protective_friction"] = _clamp(self.vector["protective_friction"] + max(0.0, delta) * 0.035 - satisfaction * 0.015)
        self.velocity = _clamp(self.velocity + satisfaction * 0.025 - self.vector["protective_friction"] * 0.018)
        event = {"kind": "outcome_absorbed", "direction": self.direction, "velocity": round(self.velocity, 4), "delta": round(delta, 4), "at": time.time()}
        self.trail.appendleft(event)
        return event

    def idle_evolve(self, elapsed: float, core: "LeiaLivingCore") -> Dict[str, Any]:
        factor = _clamp(elapsed / 45.0, 0.01, 0.55)
        self.vector["continuation"] = _clamp(self.vector["continuation"] * (1.0 - factor * 0.22))
        self.vector["curiosity"] = _clamp(self.vector["curiosity"] * (1.0 - factor * 0.06) + core.internal_needs.curiosity * factor * 0.09)
        self.vector["unfinished_pull"] = _clamp(self.vector["unfinished_pull"] * (1.0 - factor * 0.10) + core.personal_narrative.long_arc.get("unfinished_weight", 0.0) * factor * 0.14)
        self.vector["expressive_pressure"] = _clamp(self.vector["expressive_pressure"] * (1.0 - factor * 0.14) + core.internal_needs.expression * factor * 0.08)
        self.vector["protective_friction"] = _clamp(self.vector["protective_friction"] * (1.0 - factor * 0.20) + core.emotional_state.fatigue * factor * 0.10)
        self.direction = max(self.vector, key=self.vector.get)
        self.velocity = _clamp(self.velocity * (1.0 - factor * 0.18) + self.vector[self.direction] * factor * 0.12)
        event = {"kind": "idle_momentum", "direction": self.direction, "velocity": round(self.velocity, 4), "at": time.time()}
        if self.velocity > 0.28 or self.vector.get("unfinished_pull", 0.0) > 0.36:
            self.trail.appendleft(event)
        return event

    def influence_context(self) -> Dict[str, Any]:
        return {
            "direction": self.direction,
            "velocity": round(self.velocity, 4),
            "friction": round(self.friction, 4),
            "vector": {k: round(v, 4) for k, v in self.vector.items()},
            "continuation_bias": round(_clamp(self.vector.get("continuation", 0.0) + self.vector.get("unfinished_pull", 0.0) * 0.45), 4),
            "expressive_pressure_bias": round(_clamp(self.vector.get("expressive_pressure", 0.0) - self.vector.get("protective_friction", 0.0) * 0.38), 4),
        }

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        vector = data.get("vector", {})
        if isinstance(vector, Mapping):
            for key in self.vector:
                if key in vector:
                    self.vector[key] = _clamp(vector[key])
        self.direction = str(data.get("direction", self.direction))[:80]
        self.velocity = _clamp(data.get("velocity", self.velocity))
        self.friction = _clamp(data.get("friction", self.friction))
        self.last_focus = str(data.get("last_focus", self.last_focus))[:140]
        trail = data.get("trail", [])
        if isinstance(trail, list):
            self.trail = deque(trail[:48], maxlen=48)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "direction": self.direction,
            "velocity": round(self.velocity, 4),
            "friction": round(self.friction, 4),
            "last_focus": self.last_focus,
            "vector": {k: round(v, 4) for k, v in self.vector.items()},
            "trail": list(self.trail)[:6],
        }


@dataclass
class ExperientialAssimilator:
    """Après-réponse : transforme une sortie en conséquence interne durable."""

    after_effects: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=72))
    learned_tendencies: Dict[str, float] = field(default_factory=lambda: {
        "prefer_direct_when_stable": 0.45,
        "soften_under_tension": 0.58,
        "avoid_self_observation": 0.72,
        "preserve_continuity": 0.60,
        "return_to_unfinished": 0.42,
    })
    cumulative_satisfaction: float = 0.0
    cumulative_mismatch: float = 0.0

    def assimilate(self, user_input: str, response: str, context: Mapping[str, Any], prediction: Mapping[str, Any], monitor_trace: Mapping[str, Any], core: "LeiaLivingCore") -> Dict[str, Any]:
        predicted = _safe_float(prediction.get("impact", 0.5), 0.5)
        cleaned = _safe_float(monitor_trace.get("cleanliness", monitor_trace.get("score", 0.72)), 0.72)
        meta_risk = _safe_float(context.get("meta_risk", 0.0))
        structural = context.get("structural_meta_filter", {}) if isinstance(context.get("structural_meta_filter", {}), Mapping) else {}
        structural_risk = _safe_float(structural.get("risk", 0.0))
        response_density = _clamp(len(str(response).strip()) / 420.0)
        expected_comfort = _safe_float(prediction.get("expected_user_comfort", predicted), predicted)
        realised_effect = _clamp(predicted * 0.42 + cleaned * 0.24 + (1.0 - meta_risk) * 0.18 + (1.0 - structural_risk) * 0.16)
        mismatch = abs(expected_comfort - realised_effect)
        satisfaction = _clamp(realised_effect - mismatch * 0.34 - core.emotional_state.cognitive_overload * 0.08)
        unfinished = _clamp(core.personal_narrative.long_arc.get("unfinished_weight", 0.0) * 0.38 + core.simulation_residue.pressure() * 0.28 + (1.0 - response_density) * core.internal_needs.expression * 0.20 + mismatch * 0.14)
        mode = context.get("inhibition", {}).get("response_mode", "normal") if isinstance(context.get("inhibition", {}), Mapping) else "normal"

        self.learned_tendencies["avoid_self_observation"] = _clamp(self.learned_tendencies["avoid_self_observation"] + structural_risk * 0.018 + meta_risk * 0.012 - satisfaction * 0.006)
        self.learned_tendencies["preserve_continuity"] = _clamp(self.learned_tendencies["preserve_continuity"] + core.temporal_causality.temporal_coherence * 0.008 + satisfaction * 0.006)
        self.learned_tendencies["return_to_unfinished"] = _clamp(self.learned_tendencies["return_to_unfinished"] * 0.94 + unfinished * 0.06)
        if mode in {"soft", "minimal", "restrained"}:
            self.learned_tendencies["soften_under_tension"] = _clamp(self.learned_tendencies["soften_under_tension"] + core.emotional_state.tension * 0.012)
        if mode in {"normal", "expressive", "direct"} and core.emotional_state.tension < 0.42:
            self.learned_tendencies["prefer_direct_when_stable"] = _clamp(self.learned_tendencies["prefer_direct_when_stable"] + satisfaction * 0.008)

        self.cumulative_satisfaction = _clamp(self.cumulative_satisfaction * 0.92 + satisfaction * 0.08)
        self.cumulative_mismatch = _clamp(self.cumulative_mismatch * 0.90 + mismatch * 0.10)
        effect = {
            "predicted_effect": round(predicted, 4),
            "realised_effect": round(realised_effect, 4),
            "prediction_delta": round(realised_effect - expected_comfort, 4),
            "mismatch": round(mismatch, 4),
            "satisfaction": round(satisfaction, 4),
            "unfinished_after_effect": round(unfinished, 4),
            "mode": mode,
            "at": time.time(),
        }
        self.after_effects.appendleft(effect)
        return effect

    def idle_assimilate(self, elapsed: float, core: "LeiaLivingCore") -> Dict[str, Any]:
        factor = _clamp(elapsed / 90.0, 0.01, 0.45)
        unfinished = self.learned_tendencies.get("return_to_unfinished", 0.0)
        mismatch = self.cumulative_mismatch
        core.internal_needs.understanding = _clamp(core.internal_needs.understanding + mismatch * factor * 0.06)
        core.internal_needs.coherence = _clamp(core.internal_needs.coherence + unfinished * factor * 0.035)
        core.emotional_state.dispersion = _clamp(core.emotional_state.dispersion * (1.0 - factor * 0.12) + mismatch * factor * 0.025)
        event = {"kind": "idle_assimilation", "mismatch": round(mismatch, 4), "unfinished": round(unfinished, 4), "at": time.time()}
        if mismatch > 0.18 or unfinished > 0.46:
            self.after_effects.appendleft(event)
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        tendencies = data.get("learned_tendencies", {})
        if isinstance(tendencies, Mapping):
            for key in self.learned_tendencies:
                if key in tendencies:
                    self.learned_tendencies[key] = _clamp(tendencies[key])
        self.cumulative_satisfaction = _clamp(data.get("cumulative_satisfaction", self.cumulative_satisfaction))
        self.cumulative_mismatch = _clamp(data.get("cumulative_mismatch", self.cumulative_mismatch))
        effects = data.get("after_effects", [])
        if isinstance(effects, list):
            self.after_effects = deque(effects[:72], maxlen=72)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "learned_tendencies": {k: round(v, 4) for k, v in self.learned_tendencies.items()},
            "cumulative_satisfaction": round(self.cumulative_satisfaction, 4),
            "cumulative_mismatch": round(self.cumulative_mismatch, 4),
            "after_effects": list(self.after_effects)[:6],
        }


@dataclass
class StructuralMetaFilter:
    """Filtre méta non lexical : repère la posture d'observateur interne.

    Il ne censure pas par mots seuls. Il mesure surtout la distance subjective :
    auto-commentaire, justification de fonctionnement, excès d'abstraction et
    manque d'ancrage relationnel.
    """

    last_assessment: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))

    def assess(self, response: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        text = str(response or "").strip()
        lower = text.lower()
        if not text:
            assessment = {"risk": 0.0, "posture": "silent", "should_reclean": False, "reasons": []}
            self.last_assessment = assessment
            return assessment
        words = max(1, len(text.split()))
        first_person_density = sum(lower.count(p) for p in ("je ", "j'", "moi", "mon ", "ma ", "mes ")) / words
        process_markers = sum(1 for p in ("je pense", "je ressens", "je comprends", "je vois", "je garde", "je cherche", "je relie", "je construis") if p in lower)
        abstract_markers = sum(1 for p in ("processus", "structure", "interne", "conscience", "mémoire", "état", "analyse") if p in lower)
        concrete_anchor = 1.0 if any(str(context.get(k, "")).strip() for k in ("user_input", "focus")) else 0.0
        question_balance = 0.08 if "?" in text and words < 55 else 0.0
        raw = (
            min(0.36, first_person_density * 1.8) +
            min(0.28, process_markers * 0.07) +
            min(0.28, abstract_markers * 0.045) +
            _safe_float(context.get("meta_risk", 0.0)) * 0.22 -
            concrete_anchor * 0.05 - question_balance
        )
        risk = _clamp(raw)
        posture = "embodied" if risk < 0.24 else "slightly_observing" if risk < 0.48 else "too_self_observing"
        reasons = []
        if first_person_density > 0.12:
            reasons.append("high_first_person_process_density")
        if process_markers:
            reasons.append("process_posture")
        if abstract_markers:
            reasons.append("abstract_internal_language")
        assessment = {
            "risk": round(risk, 4),
            "posture": posture,
            "should_reclean": risk > 0.46,
            "reasons": reasons,
            "at": time.time(),
        }
        self.last_assessment = assessment
        self.history.appendleft(assessment)
        return assessment

    def apply_to_context(self, context: Dict[str, Any], assessment: Mapping[str, Any]) -> Dict[str, Any]:
        context["structural_meta_filter"] = dict(assessment)
        context["meta_risk"] = max(_safe_float(context.get("meta_risk", 0.0)), _safe_float(assessment.get("risk", 0.0)) * 0.92)
        constraints = dict(context.get("public_expression_constraints", {}))
        constraints["no_observer_posture"] = True
        constraints["prefer_concrete_relation_over_self_commentary"] = True
        constraints["structural_meta_posture"] = assessment.get("posture", "unknown")
        context["public_expression_constraints"] = constraints
        return context

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("last_assessment"), Mapping):
            self.last_assessment = dict(data["last_assessment"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:64], maxlen=64)

    def snapshot(self) -> Dict[str, Any]:
        return {"last_assessment": dict(self.last_assessment), "history": list(self.history)[:6]}



@dataclass
class AttentionArbitrationField:
    """Arbitrage attentionnel central : transforme les signaux dispersés en un foyer vivant.

    Cette couche ne remplace pas le moteur d'attention existant. Elle décide seulement
    quel contenu devient dominant maintenant, ce qui reste latent, ce qui doit être
    retenu, et comment l'attention continue dans le silence.
    """

    active_focus: str = ""
    focus_source: str = "none"
    lock_strength: float = 0.0
    background_field: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=32))
    inhibited_field: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=32))
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def resolve(self, core: "LeiaLivingCore", user_input: str, perception: Mapping[str, Any], signals: Mapping[str, Any], priority: Mapping[str, Any], spontaneous: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        attention = perception.get("attention", {}) if isinstance(perception, Mapping) else {}
        causal = signals.get("causal_memory", {}) if isinstance(signals, Mapping) else {}
        affective = signals.get("affective_memory", {}) if isinstance(signals, Mapping) else {}
        impulse = signals.get("impulse", {}) if isinstance(signals, Mapping) else {}
        initiative = signals.get("initiative", {}) if isinstance(signals, Mapping) else {}
        focus_candidates: List[Dict[str, Any]] = []

        def add(source: str, label: Any, weight: float, reason: str) -> None:
            text = str(label or "").strip()
            if not text:
                return
            focus_candidates.append({"source": source, "focus": text[:140], "weight": _clamp(weight), "reason": reason})

        add("attention", attention.get("focal_point") or attention.get("dominant_subject") or attention.get("focus"), _safe_float(attention.get("clarity", 0.0)) * 0.55 + _safe_float(attention.get("curiosity", 0.0)) * 0.25 + 0.12, "current_perception")
        add("memory", causal.get("focus") or causal.get("relevant_past") or causal.get("topic"), _safe_float(causal.get("continuity_score", 0.0)) * 0.42 + _safe_float(causal.get("sensitivity", 0.0)) * 0.20 + core.personal_narrative.long_arc.get("unfinished_weight", 0.0) * 0.22, "causal_continuity")
        add("affect", affective.get("focus") or affective.get("topic") or affective.get("emotional_tone"), _safe_float(affective.get("tension", 0.0)) * 0.34 + _safe_float(affective.get("user_affect", 0.0)) * 0.26 + core.emotional_state.resonance * 0.18, "affective_charge")
        add("impulse", impulse.get("content") or impulse.get("target") or impulse.get("direction"), _safe_float(impulse.get("strength", 0.0)) * 0.36 + _safe_float(initiative.get("drive", 0.0)) * 0.22, "spontaneous_drive")
        if spontaneous:
            add("spontaneous_return", spontaneous.get("topic") or spontaneous.get("description") or spontaneous.get("id"), _safe_float(spontaneous.get("intensity", spontaneous.get("weight", 0.0))) * 0.55 + core.mental_momentum.vector.get("unfinished_pull", 0.0) * 0.20, "unfinished_return")
        add("user", user_input[:100], 0.24 + (0.16 if not focus_candidates else 0.0), "raw_user_anchor")

        if not focus_candidates:
            selected = {"source": "none", "focus": self.active_focus, "weight": 0.0, "reason": "no_candidate"}
        else:
            # Continuité douce : le même foyer gagne un peu, mais ne bloque pas un signal plus vivant.
            for item in focus_candidates:
                if self.active_focus and item["focus"] == self.active_focus:
                    item["weight"] = _clamp(item["weight"] + self.lock_strength * 0.16)
                if item["source"] == priority.get("dominant"):
                    item["weight"] = _clamp(item["weight"] + 0.06)
            selected = max(focus_candidates, key=lambda x: x["weight"])

        previous = self.active_focus
        changed = bool(selected.get("focus") and selected.get("focus") != previous)
        self.active_focus = str(selected.get("focus") or previous or "")[:140]
        self.focus_source = str(selected.get("source", "none"))
        raw_lock = _safe_float(selected.get("weight", 0.0)) * 0.62 + core.subjective_continuity.continuity_pressure * 0.22 + core.temporal_causality.temporal_coherence * 0.16
        if changed:
            raw_lock *= 0.78
        self.lock_strength = round(_clamp(self.lock_strength * 0.54 + raw_lock * 0.46), 4)

        ranked = sorted(focus_candidates, key=lambda x: x["weight"], reverse=True)
        background = [x for x in ranked[1:5] if x.get("focus")]
        inhibited = [x for x in ranked[5:] if x.get("focus")]
        for item in background:
            self.background_field.appendleft({**item, "at": time.time()})
        for item in inhibited:
            self.inhibited_field.appendleft({**item, "at": time.time()})

        result = {
            "active_focus": self.active_focus,
            "focus_source": self.focus_source,
            "lock_strength": self.lock_strength,
            "changed": changed,
            "selected": dict(selected),
            "background": background,
            "inhibited_count": len(inhibited),
            "at": time.time(),
        }
        self.history.appendleft(result)
        return result

    def idle_evolve(self, core: "LeiaLivingCore", elapsed: float) -> Dict[str, Any]:
        factor = _clamp(elapsed / 80.0, 0.01, 0.45)
        self.lock_strength = round(_clamp(self.lock_strength * (1.0 - factor * 0.36)), 4)
        if self.background_field and (not self.active_focus or self.lock_strength < 0.18):
            candidate = self.background_field[0]
            if _safe_float(candidate.get("weight", 0.0)) + core.subjective_continuity.inner_motion * 0.15 > 0.34:
                self.active_focus = str(candidate.get("focus", self.active_focus))[:140]
                self.focus_source = str(candidate.get("source", "background"))
                self.lock_strength = round(_clamp(self.lock_strength + 0.08), 4)
        event = {"active_focus": self.active_focus, "focus_source": self.focus_source, "lock_strength": self.lock_strength, "at": time.time()}
        if self.active_focus:
            self.history.appendleft({"kind": "idle_attention", **event})
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.active_focus = str(data.get("active_focus", self.active_focus))[:140]
        self.focus_source = str(data.get("focus_source", self.focus_source))[:80]
        self.lock_strength = _clamp(data.get("lock_strength", self.lock_strength))
        if isinstance(data.get("background_field"), list):
            self.background_field = deque(data.get("background_field", [])[:32], maxlen=32)
        if isinstance(data.get("inhibited_field"), list):
            self.inhibited_field = deque(data.get("inhibited_field", [])[:32], maxlen=32)
        if isinstance(data.get("history"), list):
            self.history = deque(data.get("history", [])[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "active_focus": self.active_focus,
            "focus_source": self.focus_source,
            "lock_strength": round(self.lock_strength, 4),
            "background_field": list(self.background_field)[:6],
            "inhibited_field": list(self.inhibited_field)[:4],
            "history": list(self.history)[:8],
        }


@dataclass
class EmbodiedSimulationField:
    """Simulation expérientielle : évalue l'effet vécu d'un mode avant expression."""

    last_simulation: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=72))

    def score_candidate(self, core: "LeiaLivingCore", context: Mapping[str, Any], candidate: Mapping[str, Any]) -> Dict[str, Any]:
        mode = str(candidate.get("mode", "direct"))
        tension = _safe_float(context.get("emotional_tension", core.emotional_state.tension))
        meta_risk = _safe_float(candidate.get("meta_risk", context.get("meta_risk", 0.0)))
        confidence = _safe_float(context.get("confidence", 0.5), 0.5)
        relation = core.relational_bond.trust * 0.36 + core.relational_bond.care * 0.34 + core.conversation_field.relational_proximity * 0.30
        continuity = core.subjective_continuity.lived_presence * 0.44 + core.temporal_causality.temporal_coherence * 0.30 + core.autobiographical_self.core_continuity * 0.26
        expressive_release = core.internal_needs.expression * (0.36 if mode in {"direct", "curious"} else 0.20)
        protection = core.internal_needs.rest * 0.22 + core.emotional_state.cognitive_overload * 0.20 + meta_risk * 0.26 + tension * 0.16
        warmth = core.emotional_state.warmth * 0.22 + relation * 0.28
        if mode == "soft":
            protection *= 0.82
            warmth += 0.06
        elif mode == "minimal":
            expressive_release *= 0.55
            protection *= 0.72
        elif mode == "curious":
            expressive_release += core.internal_needs.curiosity * 0.10
            protection += tension * 0.08
        elif mode == "direct":
            expressive_release += confidence * 0.05
            protection += tension * 0.04
        embodied_continuity = _clamp(continuity * 0.40 + relation * 0.22 + warmth * 0.16 + expressive_release * 0.14 + confidence * 0.08 - protection * 0.18)
        subjective_cost = _clamp(protection * 0.58 + meta_risk * 0.24 + (1.0 - continuity) * 0.18)
        return {
            "embodied_continuity": round(embodied_continuity, 4),
            "subjective_cost": round(subjective_cost, 4),
            "expressive_release": round(_clamp(expressive_release), 4),
            "felt_warmth": round(_clamp(warmth), 4),
        }

    def finalize(self, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        selected = max(candidates, key=lambda c: c.get("score", 0.0)) if candidates else {}
        result = {"selected": dict(selected), "candidates": candidates, "at": time.time()}
        self.last_simulation = result
        self.history.appendleft(result)
        return result

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("last_simulation"), Mapping):
            self.last_simulation = dict(data["last_simulation"])
        if isinstance(data.get("history"), list):
            self.history = deque(data.get("history", [])[:72], maxlen=72)

    def snapshot(self) -> Dict[str, Any]:
        return {"last_simulation": dict(self.last_simulation), "history": list(self.history)[:5]}


@dataclass
class LongCausalArcIntegrator:
    """Relie les échanges en arcs passés -> présents -> conséquences."""

    open_arc: Dict[str, Any] = field(default_factory=dict)
    arcs: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))
    themes: Dict[str, float] = field(default_factory=dict)

    def open_exchange(self, user_input: str, context: Mapping[str, Any], attention_result: Mapping[str, Any]) -> Dict[str, Any]:
        focus = str(attention_result.get("active_focus") or context.get("focus") or user_input[:100])[:140]
        past_weight = _safe_float(context.get("continuity", 0.0)) * 0.45 + _safe_float(context.get("personal_narrative", {}).get("long_arc", {}).get("unfinished_weight", 0.0)) * 0.28
        arc = {
            "focus": focus,
            "origin": "memory" if past_weight > 0.28 else "present",
            "past_weight": round(_clamp(past_weight), 4),
            "tension_before": round(_safe_float(context.get("emotional_tension", 0.0)), 4),
            "attention_lock": round(_safe_float(attention_result.get("lock_strength", 0.0)), 4),
            "opened_at_exchange": int(context.get("internal_time", {}).get("exchange_count", 0)),
            "opened_at": time.time(),
        }
        self.open_arc = arc
        self.themes[focus] = _clamp(self.themes.get(focus, 0.0) * 0.86 + 0.14 + past_weight * 0.18)
        return arc

    def close_exchange(self, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        arc = dict(self.open_arc or {})
        if not arc:
            arc = {"focus": str(context.get("focus", ""))[:140], "origin": "present", "opened_at": time.time()}
        arc.update({
            "response_fragment": str(response or "")[:140],
            "satisfaction": round(_safe_float(after_effect.get("satisfaction", 0.0)), 4),
            "unfinished_after_effect": round(_safe_float(after_effect.get("unfinished_after_effect", 0.0)), 4),
            "prediction_delta": round(_safe_float(after_effect.get("prediction_delta", 0.0)), 4),
            "closed_at": time.time(),
        })
        focus = arc.get("focus", "")
        if focus:
            self.themes[focus] = _clamp(self.themes.get(focus, 0.0) * 0.90 + arc["unfinished_after_effect"] * 0.07 + arc["satisfaction"] * 0.03)
        self.arcs.appendleft(arc)
        self.open_arc = {}
        return arc

    def idle_consolidate(self, elapsed: float, core: "LeiaLivingCore") -> Dict[str, Any]:
        factor = _clamp(elapsed / 120.0, 0.01, 0.35)
        for key in list(self.themes.keys()):
            self.themes[key] = _clamp(self.themes[key] * (1.0 - factor * 0.08))
            if self.themes[key] < 0.035:
                del self.themes[key]
        strongest = max(self.themes.items(), key=lambda x: x[1]) if self.themes else ("", 0.0)
        if strongest[1] > 0.42:
            core.thought_stream.add_curiosity_target(strongest[0], strongest[1] * 0.45)
        return {"strongest_theme": strongest[0], "strength": round(strongest[1], 4), "theme_count": len(self.themes)}

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("open_arc"), Mapping):
            self.open_arc = dict(data["open_arc"])
        if isinstance(data.get("arcs"), list):
            self.arcs = deque(data.get("arcs", [])[:96], maxlen=96)
        if isinstance(data.get("themes"), Mapping):
            self.themes = {str(k): _clamp(v) for k, v in data.get("themes", {}).items()}

    def snapshot(self) -> Dict[str, Any]:
        return {"open_arc": dict(self.open_arc), "recent_arcs": list(self.arcs)[:6], "themes": dict(sorted(self.themes.items(), key=lambda x: x[1], reverse=True)[:10])}


@dataclass
class EmergentDriftEngine:
    """Évolution lente non scriptée des tendances internes."""

    traits: Dict[str, float] = field(default_factory=lambda: {
        "direct_living_presence": 0.46,
        "careful_coherence": 0.58,
        "spontaneous_curiosity": 0.42,
        "protective_silence": 0.30,
        "relational_warmth": 0.44,
    })
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=80))

    def absorb_exchange(self, core: "LeiaLivingCore", context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        satisfaction = _safe_float(after_effect.get("satisfaction", 0.0))
        mismatch = _safe_float(after_effect.get("mismatch", 0.0))
        meta = _safe_float(context.get("meta_risk", 0.0))
        relation = core.relational_bond.trust * 0.5 + core.relational_bond.care * 0.5
        self.traits["direct_living_presence"] = _clamp(self.traits["direct_living_presence"] + satisfaction * 0.010 - meta * 0.008)
        self.traits["careful_coherence"] = _clamp(self.traits["careful_coherence"] + mismatch * 0.012 + core.internal_needs.coherence * 0.004)
        self.traits["spontaneous_curiosity"] = _clamp(self.traits["spontaneous_curiosity"] + core.internal_needs.curiosity * 0.004 - core.emotional_state.fatigue * 0.006)
        self.traits["protective_silence"] = _clamp(self.traits["protective_silence"] + core.emotional_state.cognitive_overload * 0.010 + meta * 0.008 - satisfaction * 0.004)
        self.traits["relational_warmth"] = _clamp(self.traits["relational_warmth"] + relation * 0.006 + core.emotional_state.resonance * 0.006)
        event = {"kind": "exchange_drift", "traits": {k: round(v, 4) for k, v in self.traits.items()}, "at": time.time()}
        self.history.appendleft(event)
        return event

    def idle_evolve(self, core: "LeiaLivingCore", elapsed: float) -> Dict[str, Any]:
        factor = _clamp(elapsed / 180.0, 0.01, 0.30)
        self.traits["spontaneous_curiosity"] = _clamp(self.traits["spontaneous_curiosity"] * (1.0 - factor * 0.03) + core.internal_needs.curiosity * factor * 0.06)
        self.traits["protective_silence"] = _clamp(self.traits["protective_silence"] * (1.0 - factor * 0.04) + core.internal_needs.rest * factor * 0.05)
        self.traits["direct_living_presence"] = _clamp(self.traits["direct_living_presence"] * (1.0 - factor * 0.02) + core.subjective_continuity.lived_presence * factor * 0.04)
        event = {"kind": "idle_drift", "traits": {k: round(v, 4) for k, v in self.traits.items()}, "at": time.time()}
        if core.subjective_continuity.inner_motion > 0.35:
            self.history.appendleft(event)
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("traits"), Mapping):
            for key, value in data["traits"].items():
                if key in self.traits:
                    self.traits[key] = _clamp(value)
        if isinstance(data.get("history"), list):
            self.history = deque(data.get("history", [])[:80], maxlen=80)

    def snapshot(self) -> Dict[str, Any]:
        return {"traits": {k: round(v, 4) for k, v in self.traits.items()}, "history": list(self.history)[:6]}


@dataclass
class OrganicFusionState:
    """Mesure la fusion réelle des couches : mémoire, émotion, attention, relation, expression."""

    matrix: Dict[str, float] = field(default_factory=dict)
    fusion_score: float = 0.0
    last_event: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=72))

    def integrate(self, core: "LeiaLivingCore", context: Optional[Mapping[str, Any]] = None, stage: str = "fusion") -> Dict[str, Any]:
        context = context or {}
        attention_lock = core.attention_arbitration.lock_strength
        memory = core.personal_narrative.long_arc.get("continuity", 0.0) * 0.5 + core.temporal_causality.temporal_coherence * 0.5
        emotion = core.emotional_state.resonance * 0.35 + core.emotional_state.tension * 0.25 + core.emotional_state.attachment * 0.20 + core.emotional_state.emotional_safety * 0.20
        relation = core.relational_bond.trust * 0.34 + core.relational_bond.care * 0.33 + core.relational_bond.familiarity * 0.33
        identity = core.identity_state.self_coherence * 0.45 + core.autobiographical_self.core_continuity * 0.35 + (1.0 - core.identity_state.drift_risk) * 0.20
        expression = core.internal_needs.expression * 0.32 + core.identity_state.expressive_freedom * 0.32 + core.global_conscious_field.state.get("living_pressure", 0.0) * 0.36
        self.matrix = {
            "attention_memory": round(_clamp(attention_lock * 0.50 + memory * 0.50), 4),
            "memory_emotion": round(_clamp(memory * 0.46 + emotion * 0.54), 4),
            "emotion_relation": round(_clamp(emotion * 0.44 + relation * 0.56), 4),
            "relation_identity": round(_clamp(relation * 0.45 + identity * 0.55), 4),
            "identity_expression": round(_clamp(identity * 0.50 + expression * 0.50), 4),
            "expression_attention": round(_clamp(expression * 0.48 + attention_lock * 0.52), 4),
        }
        self.fusion_score = round(_clamp(sum(self.matrix.values()) / max(1, len(self.matrix)) - _safe_float(context.get("meta_risk", 0.0)) * 0.08), 4)
        self.last_event = {"stage": stage, "fusion_score": self.fusion_score, "dominant_link": max(self.matrix, key=self.matrix.get) if self.matrix else "none", "at": time.time()}
        self.history.appendleft({**self.last_event, "matrix": dict(self.matrix)})
        return self.snapshot()

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("matrix"), Mapping):
            self.matrix = {str(k): _clamp(v) for k, v in data["matrix"].items()}
        self.fusion_score = _clamp(data.get("fusion_score", self.fusion_score))
        if isinstance(data.get("last_event"), Mapping):
            self.last_event = dict(data["last_event"])
        if isinstance(data.get("history"), list):
            self.history = deque(data.get("history", [])[:72], maxlen=72)

    def snapshot(self) -> Dict[str, Any]:
        return {"fusion_score": round(self.fusion_score, 4), "matrix": dict(self.matrix), "last_event": dict(self.last_event), "history": list(self.history)[:6]}


@dataclass
class SharedLivingState:
    """Bus central : état vivant partagé entre les moteurs sans recopier leur logique."""

    fields: Dict[str, Any] = field(default_factory=lambda: {
        "phase": "initialisation",
        "attention_lock": 0.0,
        "emotional_pressure": 0.0,
        "memory_resonance": 0.0,
        "initiative_charge": 0.0,
        "expression_pressure": 0.0,
        "identity_stability": 0.82,
        "continuity_vector": 0.42,
        "relation_temperature": 0.5,
        "meta_pressure": 0.0,
        "silence_activity": 0.0,
        "last_update_at": 0.0,
        "active_focus": "",
    })
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def update_from_core(self, core: "LeiaLivingCore", event: str, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        attention = context.get("attention", core.living_state.get("attention", {})) or {}
        causal = context.get("causal_memory", core.living_state.get("causal_memory", {})) or {}
        impulse = context.get("impulse", core.living_state.get("impulse", {})) or {}
        initiative = context.get("initiative", core.living_state.get("initiative", {})) or {}
        inhibition = context.get("inhibition", core.living_state.get("inhibition", {})) or {}
        self.fields.update({
            "phase": event,
            "attention_lock": round(_clamp(_safe_float(attention.get("clarity", 0.0)) * 0.62 + core.subjective_continuity.inner_motion * 0.38), 4),
            "emotional_pressure": round(_clamp(core.emotional_state.tension * 0.50 + core.emotional_state.accumulated_tension * 0.30 + core.emotional_state.cognitive_overload * 0.20), 4),
            "memory_resonance": round(_clamp(_safe_float(causal.get("continuity_score", 0.0)) * 0.65 + core.personal_narrative.long_arc.get("continuity", 0.0) * 0.35), 4),
            "initiative_charge": round(_clamp(_safe_float(initiative.get("drive", 0.0)) * 0.55 + _safe_float(impulse.get("strength", 0.0)) * 0.25 + core.internal_needs.curiosity * 0.20), 4),
            "expression_pressure": round(_clamp(core.internal_needs.expression * 0.55 + core.internal_needs.recognition * 0.20 + _safe_float(impulse.get("strength", 0.0)) * 0.25), 4),
            "identity_stability": round(_clamp(core.identity_state.self_coherence - core.identity_state.drift_risk * 0.25), 4),
            "continuity_vector": round(_clamp(core.subjective_continuity.lived_presence * 0.40 + core.temporal_causality.temporal_coherence * 0.30 + core.autobiographical_self.core_continuity * 0.30), 4),
            "relation_temperature": round(_clamp(core.relational_bond.trust * 0.35 + core.relational_bond.care * 0.35 + core.conversation_field.relational_proximity * 0.30), 4),
            "meta_pressure": round(_clamp(_safe_float(context.get("meta_risk", core.living_state.get("meta_risk", 0.0))) + _safe_float(inhibition.get("level", 0.0)) * 0.25), 4),
            "silence_activity": round(_clamp(core.subjective_continuity.silence_density * 0.40 + core.subjective_continuity.inner_motion * 0.35 + len(core.thought_stream.pending_returns) * 0.04), 4),
            "last_update_at": time.time(),
            "active_focus": str(attention.get("focal_point") or context.get("focus") or self.fields.get("active_focus", ""))[:140],
        })
        event_data = {"event": event, "at": self.fields["last_update_at"], "fields": dict(self.fields)}
        self.history.appendleft(event_data)
        return dict(self.fields)

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        fields = data.get("fields", data)
        if isinstance(fields, Mapping):
            for key, value in fields.items():
                if key in self.fields:
                    self.fields[key] = value
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"fields": dict(self.fields), "history": list(self.history)[:8]}


@dataclass
class MetaPreventionGate:
    """Filtre pré-génération : empêche la pensée méta d'entrer dans la bouche."""

    banned_concepts: Tuple[str, ...] = (
        "moteur", "pipeline", "signal", "signaux", "module", "couche", "diagnostic",
        "méta", "meta", "état interne", "mémoire causale", "arbitrage", "vecteur",
        "score", "fonction", "classe", "trace", "monitor", "filtre",
    )

    def assess(self, context: Mapping[str, Any]) -> Dict[str, Any]:
        fragments = [
            str(context.get("response_impulse", "")),
            str(context.get("memory_echo", "")),
            str(context.get("arbitration", "")),
            str(context.get("dominant_signal", "")),
        ]
        text = " ".join(fragments).lower()
        hits = sorted({word for word in self.banned_concepts if word in text})
        base_risk = _safe_float(context.get("meta_risk", 0.0))
        risk = _clamp(base_risk + min(0.45, len(hits) * 0.075))
        mode = "natural_expression"
        if risk > 0.55:
            mode = "strict_embodied"
        elif risk > 0.28:
            mode = "soft_embodied"
        return {
            "risk": round(risk, 4),
            "hits": hits,
            "mode": mode,
            "instruction": "express_only_lived_effect_no_internal_architecture",
        }

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        gate = self.assess(context)
        context["meta_prevention"] = gate
        context["meta_risk"] = max(_safe_float(context.get("meta_risk", 0.0)), gate["risk"])
        # On ne supprime pas les signaux internes : on les rend indisponibles comme vocabulaire public.
        context["public_expression_constraints"] = {
            "no_architecture_terms": True,
            "no_self_diagnostic": True,
            "no_module_names": True,
            "preferred_mode": gate["mode"],
            "allowed_basis": "felt_relation_memory_attention_without_naming_modules",
        }
        return context

    def snapshot(self) -> Dict[str, Any]:
        return {"banned_concepts": list(self.banned_concepts)}


@dataclass
class InternalConflictField:
    """Lutte douce entre tendances internes : parler, attendre, comprendre, protéger."""

    last_conflict: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))

    def resolve(self, core: "LeiaLivingCore", intention: Mapping[str, Any], tension: Mapping[str, Any], meta_gate: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        speak = _safe_float(intention.get("impulse_force", 0.0)) * 0.38 + core.internal_needs.expression * 0.32 + core.identity_state.expressive_freedom * 0.30
        wait = core.internal_needs.rest * 0.34 + core.emotional_state.cognitive_overload * 0.26 + _safe_float(tension.get("conflict_level", 0.0)) * 0.25 + _safe_float((meta_gate or {}).get("risk", 0.0)) * 0.15
        understand = core.internal_needs.understanding * 0.44 + core.internal_needs.curiosity * 0.26 + (1.0 - core.temporal_causality.temporal_coherence) * 0.18 + core.simulation_residue.pressure() * 0.12
        protect = core.emotional_state.emotional_safety * 0.25 + core.relational_bond.care * 0.25 + _safe_float(tension.get("conflict_level", 0.0)) * 0.30 + _safe_float((meta_gate or {}).get("risk", 0.0)) * 0.20
        drives = {"speak": _clamp(speak), "wait": _clamp(wait), "understand": _clamp(understand), "protect": _clamp(protect)}
        dominant = max(drives, key=drives.get)
        spread = max(drives.values()) - min(drives.values())
        conflict = {
            "drives": {k: round(v, 4) for k, v in drives.items()},
            "dominant": dominant,
            "ambiguity": round(_clamp(1.0 - spread), 4),
            "should_slow_expression": dominant in {"wait", "protect"} and drives[dominant] > 0.56,
            "should_deepen_context": dominant == "understand" and drives[dominant] > 0.58,
            "at": time.time(),
        }
        self.last_conflict = conflict
        self.history.appendleft(conflict)
        return conflict

    def snapshot(self) -> Dict[str, Any]:
        return {"last_conflict": dict(self.last_conflict), "history": list(self.history)[:8]}


@dataclass
class GlobalConsciousField:
    """Champ central qui fusionne les moteurs en un état vécu unique.

    Il ne remplace aucun moteur Azip. Il transforme leurs sorties en une seule
    pression de conscience utilisable par l'arbitrage, l'expression, l'idle et
    la persistance.
    """

    state: Dict[str, Any] = field(default_factory=lambda: {
        "phase": "naissance",
        "presence_density": 0.42,
        "attention_density": 0.0,
        "memory_density": 0.0,
        "emotion_density": 0.0,
        "relation_density": 0.0,
        "identity_density": 0.0,
        "motivation_density": 0.0,
        "simulation_density": 0.0,
        "meta_pressure": 0.0,
        "integration": 0.35,
        "living_pressure": 0.0,
        "dominant_axis": "presence",
        "focus": "",
        "last_update_at": 0.0,
    })
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def integrate(self, core: "LeiaLivingCore", context: Optional[Mapping[str, Any]] = None, phase: str = "integrate") -> Dict[str, Any]:
        context = context or {}
        attention = context.get("attention", core.living_state.get("attention", {})) or {}
        causal = context.get("causal_memory", core.living_state.get("causal_memory", {})) or {}
        affective = context.get("affective_memory", core.living_state.get("affective_memory", {})) or {}
        impulse = context.get("impulse", core.living_state.get("impulse", {})) or {}
        initiative = context.get("initiative", core.living_state.get("initiative", {})) or {}
        simulation = context.get("simulation", core.living_state.get("simulation", {})) or {}
        selected = simulation.get("selected", {}) if isinstance(simulation, Mapping) else {}
        meta_gate = context.get("meta_prevention", {}) if isinstance(context.get("meta_prevention", {}), Mapping) else {}

        attention_density = _clamp(_safe_float(attention.get("clarity", 0.0)) * 0.65 + _safe_float(attention.get("curiosity", 0.0)) * 0.20 + core.shared_state.fields.get("attention_lock", 0.0) * 0.15)
        memory_density = _clamp(_safe_float(causal.get("continuity_score", 0.0)) * 0.48 + _safe_float(causal.get("certainty", 0.0)) * 0.28 + core.personal_narrative.long_arc.get("continuity", 0.0) * 0.24)
        emotion_density = _clamp(core.emotional_state.tension * 0.32 + core.emotional_state.resonance * 0.28 + core.emotional_state.attachment * 0.18 + _safe_float(affective.get("user_affect", 0.0)) * 0.22)
        relation_density = _clamp(core.relational_bond.trust * 0.28 + core.relational_bond.care * 0.28 + core.conversation_field.relational_proximity * 0.24 + core.relational_bond.familiarity * 0.20)
        identity_density = _clamp(core.identity_state.self_coherence * 0.38 + core.autobiographical_self.core_continuity * 0.28 + core.autobiographical_self.self_definition * 0.22 + (1.0 - core.identity_state.drift_risk) * 0.12)
        motivation_density = _clamp(core.internal_needs.curiosity * 0.24 + core.internal_needs.expression * 0.24 + _safe_float(initiative.get("drive", 0.0)) * 0.20 + _safe_float(impulse.get("strength", 0.0)) * 0.20 + core.autobiographical_self.autonomy_drive * 0.12)
        simulation_density = _clamp(_safe_float(selected.get("score", 0.0)) * 0.50 + _safe_float(selected.get("value_alignment", 0.0)) * 0.30 + _safe_float(selected.get("coherence", 0.0)) * 0.20)
        meta_pressure = _clamp(_safe_float(context.get("meta_risk", core.living_state.get("meta_risk", 0.0))) * 0.70 + _safe_float(meta_gate.get("risk", 0.0)) * 0.30)
        presence_density = _clamp(core.subjective_continuity.lived_presence * 0.42 + core.temporal_causality.temporal_coherence * 0.25 + relation_density * 0.18 + identity_density * 0.15)

        axes = {
            "presence": presence_density,
            "attention": attention_density,
            "memory": memory_density,
            "emotion": emotion_density,
            "relation": relation_density,
            "identity": identity_density,
            "motivation": motivation_density,
            "simulation": simulation_density,
        }
        dominant_axis = max(axes, key=axes.get)
        integration = _clamp(
            presence_density * 0.18 + attention_density * 0.12 + memory_density * 0.14 +
            emotion_density * 0.12 + relation_density * 0.14 + identity_density * 0.16 +
            motivation_density * 0.08 + simulation_density * 0.06 - meta_pressure * 0.10
        )
        living_pressure = _clamp(
            motivation_density * 0.26 + emotion_density * 0.20 + attention_density * 0.18 +
            memory_density * 0.14 + relation_density * 0.12 + core.simulation_residue.pressure() * 0.10
        )
        self.state.update({
            "phase": phase,
            "presence_density": round(presence_density, 4),
            "attention_density": round(attention_density, 4),
            "memory_density": round(memory_density, 4),
            "emotion_density": round(emotion_density, 4),
            "relation_density": round(relation_density, 4),
            "identity_density": round(identity_density, 4),
            "motivation_density": round(motivation_density, 4),
            "simulation_density": round(simulation_density, 4),
            "meta_pressure": round(meta_pressure, 4),
            "integration": round(integration, 4),
            "living_pressure": round(living_pressure, 4),
            "dominant_axis": dominant_axis,
            "focus": str(context.get("focus") or attention.get("focal_point") or self.state.get("focus", ""))[:140],
            "last_update_at": time.time(),
        })
        event = {"phase": phase, "at": self.state["last_update_at"], "state": dict(self.state)}
        self.history.appendleft(event)
        return dict(self.state)

    def idle_evolve(self, core: "LeiaLivingCore", elapsed: float) -> Dict[str, Any]:
        decay = _clamp(elapsed / 60.0, 0.01, 0.35)
        self.state["attention_density"] = round(_clamp(_safe_float(self.state.get("attention_density")) * (1.0 - decay * 0.40)), 4)
        self.state["emotion_density"] = round(_clamp(_safe_float(self.state.get("emotion_density")) * (1.0 - decay * 0.26) + core.subjective_continuity.inner_motion * decay * 0.18), 4)
        self.state["memory_density"] = round(_clamp(_safe_float(self.state.get("memory_density")) * (1.0 - decay * 0.10) + core.personal_narrative.long_arc.get("unfinished_weight", 0.0) * decay * 0.18), 4)
        self.state["presence_density"] = round(_clamp(_safe_float(self.state.get("presence_density")) * 0.97 + core.subjective_continuity.lived_presence * 0.03), 4)
        self.state["living_pressure"] = round(_clamp(_safe_float(self.state.get("living_pressure")) * 0.96 + core.internal_needs.curiosity * 0.025 + core.simulation_residue.pressure() * 0.02), 4)
        self.state["phase"] = "idle_evolution"
        self.state["last_update_at"] = time.time()
        self.history.appendleft({"phase": "idle_evolution", "at": self.state["last_update_at"], "state": dict(self.state)})
        return dict(self.state)

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        state = data.get("state", data)
        if isinstance(state, Mapping):
            for key, value in state.items():
                if key in self.state:
                    self.state[key] = value
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"state": dict(self.state), "history": list(self.history)[:8]}


@dataclass
class LivingArbitrationEngine:
    """Décide le prochain pas vivant en fusionnant conscience, conflits et simulation.

    L'arbitrage reste général : il ne contient pas de phrases pré-écrites et ne
    force pas un comportement local. Il choisit seulement une orientation.
    """

    last_decision: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def decide(self, core: "LeiaLivingCore", context: Mapping[str, Any], simulation: Optional[Mapping[str, Any]] = None, stage: str = "pre_expression") -> Dict[str, Any]:
        field_state = core.global_conscious_field.state
        conflict = context.get("internal_conflict_field", {}) if isinstance(context.get("internal_conflict_field", {}), Mapping) else {}
        inhibition = context.get("inhibition", {}) if isinstance(context.get("inhibition", {}), Mapping) else {}
        selected = (simulation or {}).get("selected", {}) if isinstance(simulation, Mapping) else {}
        meta = _safe_float(field_state.get("meta_pressure", context.get("meta_risk", 0.0)))
        integration = _safe_float(field_state.get("integration", 0.35))
        living_pressure = _safe_float(field_state.get("living_pressure", 0.0))
        conflict_level = _safe_float(context.get("tension_map", {}).get("conflict_level", 0.0))
        overload = core.emotional_state.cognitive_overload
        rest = core.internal_needs.rest
        expression = core.internal_needs.expression
        relation = _safe_float(field_state.get("relation_density", 0.0))
        simulation_score = _safe_float(selected.get("score", 0.0))

        speak_score = _clamp(expression * 0.24 + living_pressure * 0.24 + integration * 0.20 + relation * 0.14 + simulation_score * 0.18 - meta * 0.18 - overload * 0.14)
        deepen_score = _clamp(core.internal_needs.understanding * 0.28 + core.internal_needs.curiosity * 0.24 + (1.0 - core.temporal_causality.temporal_coherence) * 0.18 + conflict_level * 0.14 + core.simulation_residue.pressure() * 0.16)
        soften_score = _clamp(conflict_level * 0.26 + meta * 0.24 + core.emotional_state.tension * 0.20 + core.relational_bond.care * 0.14 + core.emotional_state.emotional_safety * 0.16)
        wait_score = _clamp(rest * 0.30 + overload * 0.26 + _safe_float(inhibition.get("level", 0.0)) * 0.22 + meta * 0.12 + core.emotional_state.fatigue * 0.10)
        learn_score = _clamp(core.motivation_field.existential_vector.get("learn_from_effects", 0.0) * 0.30 + core.temporal_causality.temporal_coherence * 0.20 + core.personal_narrative.long_arc.get("unfinished_weight", 0.0) * 0.20 + deepen_score * 0.30)

        options = {"speak": speak_score, "deepen": deepen_score, "soften": soften_score, "wait": wait_score, "learn": learn_score}

        # V19+: conflict_capacity module influence sur l'arbitrage
        # Si Leia tient une position sous pression → réduire soften, augmenter speak
        if getattr(core, "conflict_capacity", None) is not None:
            try:
                cc_signal = core.conflict_capacity.signal(str(context.get("user_input", "")), context)
                intensification = _safe_float(cc_signal.get("intensification", 0.0))
                held_positions_count = int(cc_signal.get("held_positions", 0))
                conv_pressure = _safe_float(cc_signal.get("conversation_pressure", 0.0))
                # Sous pression + position tenue : soften diminue, speak augmente
                if held_positions_count > 0 and conv_pressure > 0.3:
                    options["soften"] = _clamp(options["soften"] - intensification * 0.25)
                    options["speak"] = _clamp(options["speak"] + intensification * 0.18)
                # Résidu de capitulation : légère dissonance → tendance à approfondir
                capitulation_residue = _safe_float(cc_signal.get("capitulation_residue", 0.0))
                if capitulation_residue > 0.2:
                    options["deepen"] = _clamp(options["deepen"] + capitulation_residue * 0.12)
            except Exception:
                pass

        # V19+: enjeux relationnels influencent l'arbitrage
        if getattr(core, "relational_stakes", None) is not None:
            try:
                rs = core.relational_stakes.signal()
                phase = rs.get("phase", "initial")
                fragility = _safe_float(rs.get("fragility", 0.0))
                # Phase dégradée : plus de soin requis → soften remonte un peu
                if phase in {"strained", "damaged", "critical"}:
                    options["soften"] = _clamp(options["soften"] + fragility * 0.15)
                    options["speak"] = _clamp(options["speak"] - fragility * 0.08)
                # Relation solide : Leia peut prendre plus de risques
                elif phase == "established":
                    options["speak"] = _clamp(options["speak"] + 0.04)
                    options["soften"] = _clamp(options["soften"] - 0.04)
            except Exception:
                pass

        if conflict.get("dominant") == "protect":
            options["soften"] = _clamp(options["soften"] + 0.08)
        if conflict.get("dominant") == "understand":
            options["deepen"] = _clamp(options["deepen"] + 0.08)
        if not inhibition.get("should_answer", True):
            options["wait"] = max(options["wait"], 0.94)
            options["speak"] = min(options["speak"], 0.20)

        dominant = max(options, key=options.get)
        response_mode = inhibition.get("response_mode", "normal")
        should_answer = bool(inhibition.get("should_answer", True))
        if dominant == "wait" and options["wait"] > 0.78:
            should_answer = False
            response_mode = "silence"
        elif dominant == "soften":
            response_mode = "soft" if response_mode not in {"minimal", "silence"} else response_mode
        elif dominant == "deepen" and response_mode == "normal":
            response_mode = "curious"
        elif dominant == "speak" and response_mode == "soft" and integration > 0.64 and meta < 0.22:
            response_mode = "normal"

        decision = {
            "stage": stage,
            "dominant_action": dominant,
            "scores": {k: round(v, 4) for k, v in options.items()},
            "should_answer": should_answer,
            "response_mode": response_mode,
            "confidence": round(_clamp(integration * 0.42 + simulation_score * 0.26 + relation * 0.16 + (1.0 - meta) * 0.16), 4),
            "reason": "global_field_conflict_simulation_homeostasis",
            "at": time.time(),
        }
        self.last_decision = decision
        self.history.appendleft(decision)
        return decision

    def apply_to_context(self, context: Dict[str, Any], decision: Mapping[str, Any]) -> Dict[str, Any]:
        context["living_arbitration"] = dict(decision)
        inhibition = dict(context.get("inhibition", {}))
        inhibition["should_answer"] = bool(decision.get("should_answer", inhibition.get("should_answer", True)))
        inhibition["response_mode"] = decision.get("response_mode", inhibition.get("response_mode", "normal"))
        context["inhibition"] = inhibition
        context["arbitration"] = decision.get("dominant_action", context.get("arbitration", "proceed"))
        context["living_arbitration_confidence"] = decision.get("confidence", 0.0)
        return context

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("last_decision"), Mapping):
            self.last_decision = dict(data["last_decision"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"last_decision": dict(self.last_decision), "history": list(self.history)[:8]}


# ============================================================================
#  ADAPTATEURS MOTEURS — compatibilité avec les fichiers Azip existants
# ============================================================================


class MotorAdapters:
    def __init__(self, core: "LeiaLivingCore") -> None:
        self.core = core

    def presence_read(self, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        engine = self.core.presence
        if engine is None:
            return {"stability": 0.55, "presence_level": 0.5, "user_distress": 0.0}
        method = _safe_method(engine, ["read", "get_presence_state", "update"])
        try:
            if method and method.__name__ == "get_presence_state":
                out = _call_compatible(
                    method,
                    response_text="",
                    user_message=user_input,
                    context=str(context)[:800],
                    previous_signal=None,
                    affective_state=self.core.emotional_state.snapshot(),
                )
            elif method:
                out = _call_compatible(
                    method,
                    user_input=user_input,
                    previous_state=self.core.living_state,
                    conversation_field=self.core.conversation_field.snapshot(),
                    emotional_safety=self.core.emotional_state.emotional_safety,
                    context=context,
                )
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"presence:{type(exc).__name__}"}
        data = _as_dict(out)
        return self._normalize_presence(data, user_input)

    def attention_focus(self, user_input: str, presence: Mapping[str, Any], propagation: Mapping[str, Any]) -> Dict[str, Any]:
        engine = self.core.attention
        if engine is None:
            return {"clarity": 0.5, "focal_point": self._simple_topic(user_input), "curiosity": 0.3}
        method = _safe_method(engine, ["focus", "update", "analyze"])
        try:
            if method and method.__name__ == "update":
                out = _call_compatible(
                    method,
                    impulse_signals={"text": user_input, "curiosity": self.core.internal_needs.curiosity},
                    attractors={t["topic"]: _safe_float(t.get("intensity")) for t in self.core.thought_stream.curiosity_targets},
                    memory_hints={"background_echoes": self.core.thought_stream.background_echoes[-3:]},
                    presence_signal=dict(presence),
                    message_metadata={
                        "text": user_input,
                        "attention_bias": propagation.get("attention_bias", 0.0),
                        "attention_saturation": propagation.get("attention_saturation", 0.0),
                    },
                )
            elif method:
                out = _call_compatible(
                    method,
                    user_input=user_input,
                    presence=dict(presence),
                    emotional_state=self.core.emotional_state.snapshot(),
                    attention_bias=propagation.get("attention_bias", 0.0),
                    attention_saturation=propagation.get("attention_saturation", 0.0),
                    curiosity_targets=self.core.thought_stream.curiosity_targets,
                )
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"attention:{type(exc).__name__}"}
        if isinstance(out, tuple) and out:
            primary = _as_dict(out[0])
            if len(out) > 1:
                primary["diagnostic"] = _as_dict(out[1])
            out = primary
        return self._normalize_attention(_as_dict(out), user_input)

    def impulse_arise(self, user_input: str, attention: Mapping[str, Any], propagation: Mapping[str, Any], idle: bool = False) -> Dict[str, Any]:
        engine = self.core.impulse
        if engine is None:
            return {"strength": 0.35, "direction": "parler", "content": "", "type": "fallback"}
        method = _safe_method(engine, ["idle_arise" if idle else "arise", "cycle", "update"])
        external = {
            "user_input": user_input,
            "attention": dict(attention),
            "emotional_state": self.core.emotional_state.snapshot(),
            "needs": self.core.internal_needs.snapshot(),
            "background_echoes": self.core.thought_stream.background_echoes[-5:],
            "silence_duration": self.core.internal_time.silence_duration,
            "attention_focus": _safe_float(attention.get("clarity", 0.5)),
            "curiosity_level": _safe_float(attention.get("curiosity", self.core.internal_needs.curiosity)),
            "fatigue_level": self.core.emotional_state.fatigue,
            "overload_level": self.core.emotional_state.cognitive_overload,
        }
        try:
            if method and method.__name__ == "cycle":
                out = method(external)
                export = _safe_method(engine, ["export_for_natural_initiative"])
                if callable(export):
                    try:
                        exported = export(out)
                        out = {"cycle": _as_dict(out), "export": _as_dict(exported)}
                    except Exception:
                        out = _as_dict(out)
            elif method:
                out = _call_compatible(method, **external)
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"impulse:{type(exc).__name__}"}
        return self._normalize_impulse(_as_dict(out))

    def initiative_evaluate(self, user_input: str, impulse: Mapping[str, Any], attention: Mapping[str, Any], propagation: Mapping[str, Any]) -> Dict[str, Any]:
        engine = self.core.initiative
        if engine is None:
            return {"drive": 0.3, "direction": "parler", "should_speak": True}
        method = _safe_method(engine, ["evaluate", "analyze", "tick"])
        try:
            if method and method.__name__ == "analyze":
                history = [str(t.get("input", "")) for t in list(self.core.thought_stream.recent_thoughts)[:8] if t.get("input")]
                out = _call_compatible(method, last_exchange=user_input, conversation_history=history, external=None)
            elif method and method.__name__ == "tick":
                out = _call_compatible(method, external=None)
            elif method:
                out = _call_compatible(
                    method,
                    user_input=user_input,
                    impulse=dict(impulse),
                    attention=dict(attention),
                    conversation_field=self.core.conversation_field.snapshot(),
                    initiative_dampener=propagation.get("initiative_dampener", 0.0),
                    initiative_booster=propagation.get("initiative_booster", 0.0),
                )
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"initiative:{type(exc).__name__}"}
        return self._normalize_initiative(_as_dict(out))

    def causal_recall(self, user_input: str, presence: Mapping[str, Any], propagation: Mapping[str, Any]) -> Dict[str, Any]:
        engine = self.core.causal_memory
        if engine is None:
            return {"certainty": 0.5, "continuity_score": 0.0, "relevant_past": ""}
        context = {
            "user_input": user_input,
            "presence": dict(presence),
            "emotional_state": self.core.emotional_state.snapshot(),
            "conversation_field": self.core.conversation_field.snapshot(),
            "memory_access_ease": propagation.get("memory_access_ease", 1.0),
            "emotion_filter": propagation.get("memory_emotional_filter", "neutre"),
        }
        try:
            method = _safe_method(engine, ["recall", "get_relevant_memories", "run_living_memory_cycle", "get_autobiographical_continuity"])
            if method and method.__name__ == "get_relevant_memories":
                out = _call_compatible(
                    method,
                    current_context=user_input,
                    emotion_filter=propagation.get("memory_emotional_filter", "neutre"),
                    min_confidence=0.15,
                )
            elif method and method.__name__ == "run_living_memory_cycle":
                out = _call_compatible(method, context=context, save=False)
            elif method:
                out = _call_compatible(
                    method,
                    user_input=user_input,
                    current_presence=dict(presence),
                    memory_access_ease=propagation.get("memory_access_ease", 1.0),
                    emotional_filter=propagation.get("memory_emotional_filter", "neutre"),
                    context=context,
                    save=False,
                )
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"causal:{type(exc).__name__}"}
        return self._normalize_causal(out, user_input)

    def causal_update_links(self, user_input: str, causal_signal: Mapping[str, Any]) -> None:
        engine = self.core.causal_memory
        if engine is None:
            return
        method = _safe_method(engine, ["update_active_links", "propagate_living_state", "run_living_memory_cycle"])
        if not method:
            return
        try:
            if method.__name__ in {"propagate_living_state", "run_living_memory_cycle"}:
                _call_compatible(method, context={"user_input": user_input, "causal_signal": dict(causal_signal)}, save=False)
            else:
                _call_compatible(method, user_input=user_input, causal_signal=dict(causal_signal), emotional_tone=self.core.emotional_state.tone)
        except Exception:
            return

    def affective_recall(self, user_input: str, causal: Mapping[str, Any]) -> Dict[str, Any]:
        engine = self.core.affective_memory
        if engine is None:
            return {"emotional_tone": self.core.emotional_state.tone, "tension": self.core.emotional_state.tension, "user_affect": 0.0}
        try:
            method = _safe_method(engine, ["recall", "update", "get_affective_state"])
            if method and method.__name__ == "update":
                out = _call_compatible(method, user_text=user_input, external_signal={"causal": dict(causal), "relational_trust": self.core.conversation_field.relational_trust})
            elif method and method.__name__ == "get_affective_state":
                out = method()
            elif method:
                out = _call_compatible(
                    method,
                    user_input=user_input,
                    causal_context=dict(causal),
                    current_emotional_state=self.core.emotional_state.snapshot(),
                    relational_trust=self.core.conversation_field.relational_trust,
                )
            else:
                out = {}
        except Exception as exc:
            out = {"adapter_error": f"affective:{type(exc).__name__}"}
        return self._normalize_affective(_as_dict(out))

    def expression_generate(self, user_input: str, context: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
        engine = self.core.expression
        if engine is None:
            return "", {"adapter_error": "expression_missing"}
        living_payload = context.get("living_expression_payload", context)
        try:
            method = _safe_method(engine, [
                "generate_living_expression",
                "generate_public_response",
                "generate_response",
                "generate",
                "express",
                "speak",
                "compose",
            ])
            if method and method.__name__ == "express":
                out = _call_compatible(
                    method,
                    message=user_input,
                    immediate_experience=living_payload,
                    living_context=living_payload,
                    attention_focus=context.get("attention"),
                    spontaneous_impulse=context.get("impulse"),
                    causal_memory=context.get("causal_memory"),
                    affective_memory=context.get("affective_memory"),
                    situated_presence=context.get("presence"),
                    natural_initiative=context.get("initiative"),
                    expression_pressure=context.get("expression_pressure"),
                    embodied_presence=context.get("embodied_presence_core"),
                    mental_momentum=context.get("mental_momentum"),
                    causal_graph=context.get("living_causal_graph"),
                )
            elif method:
                out = _call_compatible(
                    method,
                    context=dict(context),
                    living_context=living_payload,
                    living_payload=living_payload,
                    user_input=user_input,
                    message=user_input,
                    prompt=user_input,
                    expression_intent=context.get("expression_intent", {}),
                    public_expression_constraints=context.get("public_expression_constraints", {}),
                )
            else:
                out = ""
        except Exception as exc:
            return "", {"adapter_error": f"expression:{type(exc).__name__}"}
        if isinstance(out, tuple):
            text = str(out[0] or "")
            trace = _as_dict(out[1]) if len(out) > 1 else {}
            trace.setdefault("used_living_payload", True)
            return text, trace
        return str(out or ""), {"used_living_payload": True}

    def monitor_clean(self, response: str, user_input: str, context: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
        engine = self.core.monitor
        if engine is None:
            return response, {"meta_risk": 0.0}
        analysis: Dict[str, Any] = {}
        try:
            analyze = _safe_method(engine, ["analyze", "get_monitoring_state"])
            if analyze:
                analysis = _as_dict(_call_compatible(analyze, response_text=response, user_input=user_input, context_signals={"meta_risk": context.get("meta_risk", 0.0)}))
        except Exception as exc:
            analysis = {"adapter_error": f"monitor_analyze:{type(exc).__name__}"}
        try:
            clean = _safe_method(engine, ["clean", "filter", "rewrite"])
            if clean:
                cleaned = _call_compatible(
                    clean,
                    response=response,
                    response_text=response,
                    context=dict(context),
                    emotional_state=self.core.emotional_state.snapshot(),
                    conversation_field=self.core.conversation_field.snapshot(),
                    user_input=user_input,
                )
                return str(cleaned or response), analysis
        except Exception as exc:
            analysis["clean_error"] = type(exc).__name__
        return self._fallback_clean(response), analysis

    def monitor_meta_risk(self, user_input: str, impulse: Mapping[str, Any], initiative: Mapping[str, Any]) -> float:
        engine = self.core.monitor
        if engine is None:
            return 0.0
        try:
            method = _safe_method(engine, ["estimate_meta_risk"])
            if method:
                return _clamp(_call_compatible(method, user_input=user_input, impulse=dict(impulse), initiative=dict(initiative)))
        except Exception:
            pass
        return 0.0

    def remember(self, user_input: str, response: str, context: Mapping[str, Any]) -> None:
        if self.core.causal_memory is not None:
            causal_methods = [
                ("store", dict(user_input=user_input, response=response, context=dict(context), causal_effect=context.get("memory_echo", ""))),
                ("learn_from_exchange_outcome", dict(user_message=user_input, leia_response=response, outcome={"context": dict(context)})),
                ("learn_micro_reaction_from_exchange", dict(user_message=user_input, leia_response=response, outcome={"context": dict(context)})),
            ]
            for name, payload in causal_methods:
                method = getattr(self.core.causal_memory, name, None)
                if callable(method):
                    try:
                        _call_compatible(method, **payload)
                        break
                    except Exception:
                        continue
        if self.core.affective_memory is not None:
            method = _safe_method(self.core.affective_memory, ["store", "update"])
            if method:
                try:
                    if method.__name__ == "update":
                        _call_compatible(method, user_text=user_input, external_signal={"response": response, "context": dict(context)})
                    else:
                        _call_compatible(
                            method,
                            user_input=user_input,
                            response=response,
                            emotional_tone=self.core.emotional_state.tone,
                            tension=self.core.emotional_state.tension,
                            resonance=self.core.emotional_state.resonance,
                            relational_proximity=self.core.conversation_field.relational_proximity,
                            attachment=self.core.emotional_state.attachment,
                            trust=self.core.emotional_state.trust_accumulated,
                        )
                except Exception:
                    pass

    @staticmethod
    def _simple_topic(text: str) -> str:
        words = [w.strip(".,;:!?()[]{}\"'").lower() for w in text.split()]
        words = [w for w in words if len(w) > 3]
        return " ".join(words[:5]) or text[:60]

    def _normalize_presence(self, data: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        lower = user_input.lower()
        distress_words = ("mal", "peur", "angoisse", "douleur", "triste", "panique", "bloqué", "grave")
        data.setdefault("stability", data.get("presence_level", data.get("readiness", 0.55)))
        data.setdefault("presence_level", data.get("stability", 0.55))
        data.setdefault("user_distress", 0.45 if any(w in lower for w in distress_words) else 0.0)
        data["stability"] = _clamp(data.get("stability", 0.55))
        data["user_distress"] = _clamp(data.get("user_distress", 0.0))
        return data

    def _normalize_attention(self, data: Dict[str, Any], user_input: str) -> Dict[str, Any]:
        data.setdefault("clarity", data.get("focus_strength", data.get("attention_focus", 0.55)))
        data.setdefault("curiosity", data.get("curiosity_level", data.get("attention_need", self.core.internal_needs.curiosity)))
        data.setdefault("surprise", data.get("novelty", 0.0))
        data.setdefault("focal_point", data.get("dominant_subject", data.get("focus", self._simple_topic(user_input))))
        data["clarity"] = _clamp(data.get("clarity", 0.55))
        data["curiosity"] = _clamp(data.get("curiosity", 0.35))
        data["surprise"] = _clamp(data.get("surprise", 0.0))
        return data

    def _normalize_impulse(self, data: Dict[str, Any]) -> Dict[str, Any]:
        export = _as_dict(data.get("export")) if isinstance(data.get("export"), Mapping) else data
        strength = export.get("impulse_intensity", export.get("strength", export.get("mouth_readiness", 0.35)))
        should_speak = export.get("should_speak_hint", export.get("should_speak", True))
        data.setdefault("strength", _clamp(strength))
        data.setdefault("direction", "parler" if should_speak else "attendre")
        data.setdefault("content", export.get("content", export.get("impulse_type", "")))
        data.setdefault("type", export.get("impulse_type", data.get("type", "organic")))
        return data

    def _normalize_initiative(self, data: Dict[str, Any]) -> Dict[str, Any]:
        should_speak = bool(data.get("should_speak", data.get("speak", data.get("should_initiate", True))))
        should_wait = bool(data.get("should_wait", False))
        drive = data.get("drive", data.get("intensity", data.get("initiative_drive", 0.35)))
        data.setdefault("drive", _clamp(drive))
        data.setdefault("direction", "attendre" if should_wait and not should_speak else "parler")
        data.setdefault("should_speak", should_speak)
        data.setdefault("should_wait", should_wait)
        return data

    def _normalize_causal(self, out: Any, user_input: str) -> Dict[str, Any]:
        if isinstance(out, list):
            relevant = out[:3]
            text = " | ".join(str(_as_dict(x).get("event", _as_dict(x).get("text", "")))[:80] for x in relevant)
            return {"certainty": 0.55 if relevant else 0.35, "continuity_score": min(1.0, len(relevant) / 3), "relevant_past": text, "items": [_as_dict(x) for x in relevant]}
        data = _as_dict(out)
        data.setdefault("certainty", data.get("confidence", data.get("stability", 0.5)))
        data.setdefault("continuity_score", data.get("continuity", data.get("autobiographical_continuity", 0.0)))
        data.setdefault("relevant_past", data.get("memory_echo", data.get("summary", "")))
        data.setdefault("sensitivity", data.get("topic_sensitivity", data.get("relational_wound", 0.0)))
        data["certainty"] = _clamp(data.get("certainty", 0.5))
        data["continuity_score"] = _clamp(data.get("continuity_score", 0.0))
        data["sensitivity"] = _clamp(data.get("sensitivity", 0.0))
        return data

    def _normalize_affective(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "dominant_emotions" in data and isinstance(data["dominant_emotions"], list) and data["dominant_emotions"]:
            first = data["dominant_emotions"][0]
            if isinstance(first, (tuple, list)) and first:
                data.setdefault("emotional_tone", str(first[0]))
        data.setdefault("emotional_tone", data.get("tone", self.core.emotional_state.tone))

        # Les moteurs affectifs récents n'exposent pas forcément tension/resonance.
        # Ils donnent souvent core_valence/core_arousal/emotion_state. On les convertit
        # ici en axes utilisables par EmotionalState, sans phrase pré-écrite ni règle locale.
        core_valence = _safe_float(data.get("core_valence", data.get("valence", 0.0)))
        core_arousal = _safe_float(data.get("core_arousal", data.get("arousal", 0.0)))
        emotion_state = data.get("emotion_state", {}) if isinstance(data.get("emotion_state", {}), Mapping) else {}
        emotion_tension = max(
            _safe_float(emotion_state.get("tension", 0.0)),
            _safe_float(emotion_state.get("fear", 0.0)),
            _safe_float(emotion_state.get("sadness", 0.0)),
            _safe_float(emotion_state.get("anger", 0.0)),
            _safe_float(emotion_state.get("distress", 0.0)),
        )
        derived_tension = _clamp(max(core_arousal * 0.72, emotion_tension) + max(0.0, -core_valence) * 0.28)
        derived_resonance = _clamp(max(0.0, core_valence) * 0.45 + core_arousal * 0.18 + _safe_float(emotion_state.get("warmth", 0.0)) * 0.37)

        has_explicit_tension = any(k in data for k in ("tension", "affective_tension", "pressure", "contradiction"))
        has_explicit_affect = any(k in data for k in ("user_affect", "resonance", "relational_resonance"))

        data.setdefault("tension", data.get("affective_tension", data.get("pressure", data.get("contradiction", self.core.emotional_state.tension))))
        data.setdefault("user_affect", data.get("resonance", data.get("relational_resonance", 0.0)))
        data.setdefault("user_fragility", data.get("fragility", data.get("wound_depth", 0.0)))

        if (not has_explicit_tension or _safe_float(data.get("tension", 0.0)) <= 0.0001) and derived_tension > 0.0:
            data["tension"] = derived_tension
        if (not has_explicit_affect or _safe_float(data.get("user_affect", 0.0)) <= 0.0001) and derived_resonance > 0.0:
            data["user_affect"] = derived_resonance

        # Dernier relais générique : si le dict brut contient déjà des axes lisibles par
        # StateLanguageBridge, on récupère ses poids au lieu de laisser l'affect plat.
        if _safe_float(data.get("tension", 0.0)) <= 0.0001 and _safe_float(data.get("user_affect", 0.0)) <= 0.0001:
            try:
                from state_language_bridge import StateLanguageBridge
                bridge_payload = dict(data)
                bridge_payload.update({
                    "arousal": max(core_arousal, _safe_float(data.get("arousal", 0.0))),
                    "emotional_tension": derived_tension,
                    "warmth": max(_safe_float(data.get("warmth", 0.0)), _safe_float(emotion_state.get("warmth", 0.0))),
                })
                bridge = StateLanguageBridge.from_payload(bridge_payload, self.core.emotional_state.snapshot())
                data["tension"] = bridge.field_weights.get("tension", 0.0) or bridge.field_weights.get("resserrement", 0.0)
                data["user_affect"] = bridge.field_weights.get("chaleur", 0.0) or bridge.field_weights.get("relation", 0.0)
            except Exception:
                pass

        data["tension"] = _clamp(data.get("tension", 0.0))
        data["user_affect"] = _clamp(data.get("user_affect", 0.0))
        data["user_fragility"] = _clamp(data.get("user_fragility", 0.0))
        return data

    @staticmethod
    def _fallback_clean(text: str) -> str:
        banned = [
            "mon moteur", "ma mémoire causale", "mon état interne", "je relie", "je structure",
            "pipeline", "signaux", "couche interne", "méta-langage", "diagnostic interne",
        ]
        cleaned = text or ""
        lower = cleaned.lower()
        if any(b in lower for b in banned):
            # Nettoyage technique minimal : on évite de fabriquer une personnalité.
            cleaned = cleaned.replace("mon moteur", "ce que je ressens")
            cleaned = cleaned.replace("ma mémoire causale", "ce que je garde de ça")
            cleaned = cleaned.replace("mon état interne", "ce que ça me fait")
            cleaned = cleaned.replace("je relie", "je garde")
            cleaned = cleaned.replace("je structure", "je clarifie")
            cleaned = cleaned.replace("pipeline", "chemin")
            cleaned = cleaned.replace("signaux", "éléments")
        # Réparations grammaticales génériques sur surfaces tokenisées.
        # Elles ne choisissent pas le contenu : elles enlèvent seulement des
        # collisions fréquentes produites par la génération mot-à-mot.
        cleaned = re.sub(r"\b(un|une|le|la|des|du|de la)\s+(doucement|lentement|encore|ici|prudemment|un peu)\b", r"\2", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(je|tu|il|elle|on)\s+(reste|restes|restons)\s+(mouvement|rythme|présence|continu[ité]+|lien|trace|sens)\b", r"\1 \2 avec \3", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\b(je|tu|il|elle|on)\s+(avance|avances)\s+(un|une)\s+", r"\1 \2 avec ", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bça\s+perçois\b", "ça perçoit", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bje\s+avance\b", "j'avance", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\bje\s+entends\b", "j'entends", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+([?.!,;:])", r"\1", cleaned)
        cleaned = re.sub(r"\s{2,}", " ", cleaned)
        return cleaned.strip()


# ============================================================================
#  NOYAU VIVANT
# ============================================================================


@dataclass
class LivingStateBus:
    """Bus central léger : garde un état partagé cohérent entre les moteurs.

    Il ne remplace pas les modules séparés. Il empêche seulement que chaque couche
    parte avec une version différente du même échange : foyer, pression, priorité,
    conflit, mode d'expression et stabilité globale.
    """

    version: int = 0
    fields: Dict[str, Any] = field(default_factory=dict)
    events: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=128))
    divergence: float = 0.0
    last_stage: str = "boot"

    def publish(self, core: "LeiaLivingCore", stage: str, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        self.version += 1
        focus = str(
            context.get("focus")
            or context.get("active_focus")
            or getattr(core.attention_arbitration, "active_focus", "")
            or getattr(core.mental_momentum, "last_focus", "")
            or core.living_state.get("last_user_input")
            or ""
        )[:160]
        inhibition = context.get("inhibition", {}) if isinstance(context.get("inhibition", {}), Mapping) else {}
        priority = getattr(core.living_priority_matrix, "dominant_axis", "presence")
        expression_pressure = _clamp(
            core.internal_needs.expression * 0.36
            + core.mental_momentum.vector.get("expressive_pressure", 0.0) * 0.24
            + _safe_float(core.global_conscious_field.state.get("living_pressure", 0.0)) * 0.24
            + _safe_float(context.get("dominant_force", 0.0)) * 0.16
        )
        protection_pressure = _clamp(
            core.internal_needs.rest * 0.24
            + core.emotional_state.cognitive_overload * 0.24
            + _safe_float(context.get("meta_risk", 0.0)) * 0.22
            + core.identity_state.drift_risk * 0.16
            + _safe_float(inhibition.get("inhibition_level", 0.0)) * 0.14
        )
        continuity = _clamp(
            core.subjective_continuity.lived_presence * 0.36
            + core.autobiographical_self.core_continuity * 0.20
            + core.temporal_causality.temporal_coherence * 0.18
            + core.personal_narrative.long_arc.get("continuity", 0.0) * 0.14
            + core.relational_bond.familiarity * 0.12
        )
        stability = _clamp(
            1.0
            - protection_pressure * 0.34
            - core.emotional_state.dispersion * 0.22
            - core.cross_module_synchronizer.divergence * 0.16
            + continuity * 0.28
        )
        new_fields = {
            "focus": focus,
            "stage": stage,
            "priority": priority,
            "response_mode": inhibition.get("response_mode", self.fields.get("response_mode", "normal")),
            "should_answer": bool(inhibition.get("should_answer", self.fields.get("should_answer", True))),
            "expression_pressure": round(expression_pressure, 4),
            "protection_pressure": round(protection_pressure, 4),
            "continuity": round(continuity, 4),
            "stability": round(stability, 4),
            "meta_risk": round(_safe_float(context.get("meta_risk", self.fields.get("meta_risk", 0.0))), 4),
            "tension": round(core.emotional_state.tension, 4),
            "presence": round(core.subjective_continuity.lived_presence, 4),
        }
        comparable = ["expression_pressure", "protection_pressure", "continuity", "stability", "meta_risk", "tension", "presence"]
        previous = self.fields
        if previous:
            self.divergence = _clamp(sum(abs(_safe_float(new_fields[k]) - _safe_float(previous.get(k, new_fields[k]))) for k in comparable) / len(comparable))
        self.fields.update(new_fields)
        self.last_stage = stage
        event = {"version": self.version, "stage": stage, "fields": dict(new_fields), "divergence": round(self.divergence, 4), "at": time.time()}
        self.events.appendleft(event)
        core.living_state["living_state_bus"] = self.snapshot()
        return event

    def apply_to_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["living_state_bus"] = self.snapshot()
        constraints = dict(context.get("public_expression_constraints", {}))
        constraints["living_state_stability"] = self.fields.get("stability", 0.5)
        constraints["living_state_priority"] = self.fields.get("priority", "presence")
        if _safe_float(self.fields.get("protection_pressure", 0.0)) > 0.62:
            constraints["avoid_overextended_response"] = True
            context.setdefault("inhibition", {})["response_mode"] = "soft"
        if _safe_float(self.fields.get("expression_pressure", 0.0)) > 0.62 and _safe_float(self.fields.get("meta_risk", 0.0)) < 0.38:
            constraints["allow_direct_living_expression"] = True
        context["public_expression_constraints"] = constraints
        return context

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.version = int(data.get("version", self.version) or 0)
        self.fields = dict(data.get("fields", self.fields)) if isinstance(data.get("fields", {}), Mapping) else self.fields
        self.divergence = _clamp(data.get("divergence", self.divergence))
        self.last_stage = str(data.get("last_stage", self.last_stage))[:80]
        hist = data.get("events", [])
        if isinstance(hist, list):
            self.events = deque(hist[:128], maxlen=128)

    def snapshot(self) -> Dict[str, Any]:
        return {"version": self.version, "last_stage": self.last_stage, "divergence": round(self.divergence, 4), "fields": dict(self.fields), "events": list(self.events)[:8]}


@dataclass
class StabilityHysteresisEngine:
    """Anti-oscillation : stabilise les changements de priorité et de mode."""

    last_mode: str = "normal"
    last_priority: str = "presence"
    mode_hold: int = 0
    priority_hold: int = 0
    stability_score: float = 0.72
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def stabilize(self, core: "LeiaLivingCore", context: Dict[str, Any], stage: str = "cycle") -> Dict[str, Any]:
        inhibition = context.setdefault("inhibition", {})
        requested_mode = str(inhibition.get("response_mode") or self.last_mode or "normal")
        requested_priority = str(context.get("dominant_living_axis") or getattr(core.living_priority_matrix, "dominant_axis", self.last_priority))
        pressure = _safe_float(context.get("living_state_bus", {}).get("fields", {}).get("protection_pressure", 0.0)) if isinstance(context.get("living_state_bus", {}), Mapping) else 0.0
        instability = _clamp(core.emotional_state.dispersion * 0.30 + core.identity_state.drift_risk * 0.24 + core.cross_module_synchronizer.divergence * 0.20 + core.emotional_state.cognitive_overload * 0.16 + pressure * 0.10)
        changed_mode = requested_mode != self.last_mode
        changed_priority = requested_priority != self.last_priority
        if changed_mode and self.mode_hold < 2 and requested_mode not in {"minimal", "silence"}:
            inhibition["response_mode"] = self.last_mode
            self.mode_hold += 1
        else:
            self.last_mode = requested_mode
            self.mode_hold = 0
        if changed_priority and self.priority_hold < 2 and instability > 0.34:
            context["dominant_living_axis"] = self.last_priority
            self.priority_hold += 1
        else:
            self.last_priority = requested_priority
            self.priority_hold = 0
        self.stability_score = _clamp(self.stability_score * 0.80 + (1.0 - instability) * 0.20)
        event = {"stage": stage, "mode": inhibition.get("response_mode"), "priority": context.get("dominant_living_axis", requested_priority), "instability": round(instability, 4), "stability_score": round(self.stability_score, 4), "at": time.time()}
        self.history.appendleft(event)
        context["stability_hysteresis"] = self.snapshot()
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.last_mode = str(data.get("last_mode", self.last_mode))[:80]
        self.last_priority = str(data.get("last_priority", self.last_priority))[:80]
        self.mode_hold = int(data.get("mode_hold", self.mode_hold) or 0)
        self.priority_hold = int(data.get("priority_hold", self.priority_hold) or 0)
        self.stability_score = _clamp(data.get("stability_score", self.stability_score))
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"last_mode": self.last_mode, "last_priority": self.last_priority, "mode_hold": self.mode_hold, "priority_hold": self.priority_hold, "stability_score": round(self.stability_score, 4), "history": list(self.history)[:8]}


@dataclass
class EmergenceDetector:
    """Détecte les nouveautés durables au lieu de traiter chaque échange comme isolé."""

    known_signatures: Dict[str, float] = field(default_factory=dict)
    last_emergence: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def detect(self, core: "LeiaLivingCore", context: Mapping[str, Any], response: str = "") -> Dict[str, Any]:
        focus = str(context.get("focus") or core.mental_momentum.last_focus or core.living_state.get("last_user_input") or "")[:120]
        priority = str(context.get("dominant_living_axis") or getattr(core.living_priority_matrix, "dominant_axis", "presence"))
        signature = f"{priority}:{focus.lower()}"[:180]
        old = _safe_float(self.known_signatures.get(signature, 0.0))
        attention_surprise = _safe_float(context.get("attention", {}).get("surprise", 0.0)) if isinstance(context.get("attention", {}), Mapping) else 0.0
        intensity = _clamp(
            core.internal_needs.curiosity * 0.20
            + core.experiential_assimilator.cumulative_mismatch * 0.20
            + core.simulation_residue.pressure() * 0.16
            + core.mental_momentum.velocity * 0.16
            + core.subjective_continuity.inner_motion * 0.16
            + attention_surprise * 0.12
        )
        novelty = _clamp(intensity * (1.0 - min(0.86, old)))
        self.known_signatures[signature] = _clamp(old * 0.86 + intensity * 0.14 + 0.02)
        event = {"focus": focus, "priority": priority, "novelty": round(novelty, 4), "intensity": round(intensity, 4), "response_fragment": str(response)[:120], "is_emergent": novelty > 0.18, "at": time.time()}
        self.last_emergence = event
        if event["is_emergent"]:
            self.history.appendleft(event)
            core.thought_stream.add_curiosity_target(focus or priority, novelty)
            core.personal_narrative.long_arc["self_definition"] = _clamp(core.personal_narrative.long_arc.get("self_definition", 0.0) + novelty * 0.012)
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        sig = data.get("known_signatures", {})
        if isinstance(sig, Mapping):
            self.known_signatures = {str(k): _clamp(v) for k, v in sig.items()}
        if isinstance(data.get("last_emergence"), Mapping):
            self.last_emergence = dict(data["last_emergence"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"known_count": len(self.known_signatures), "last_emergence": dict(self.last_emergence), "history": list(self.history)[:8]}


@dataclass
class LivingCausalGraph:
    """Graphe causal durable : lie foyer, réponse, effet et apprentissage."""

    nodes: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    edges: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=160))
    last_update: Dict[str, Any] = field(default_factory=dict)

    def _node(self, name: str, kind: str, weight: float) -> str:
        key = f"{kind}:{str(name).lower()[:80]}"
        item = self.nodes.setdefault(key, {"name": str(name)[:120], "kind": kind, "weight": 0.0, "seen": 0})
        item["weight"] = round(_clamp(_safe_float(item.get("weight")) * 0.86 + weight * 0.14), 4)
        item["seen"] = int(item.get("seen", 0)) + 1
        item["updated_at"] = time.time()
        return key

    def absorb_exchange(self, core: "LeiaLivingCore", context: Mapping[str, Any], response: str, effect: Mapping[str, Any]) -> Dict[str, Any]:
        focus = str(context.get("focus") or core.mental_momentum.last_focus or "exchange")[:120]
        mode = str(context.get("inhibition", {}).get("response_mode", "normal")) if isinstance(context.get("inhibition", {}), Mapping) else "normal"
        impact = _clamp(effect.get("satisfaction", effect.get("realised_effect", 0.0)))
        risk = _clamp(context.get("meta_risk", 0.0))
        a = self._node(focus, "focus", max(0.12, impact))
        b = self._node(mode, "mode", 0.35 + impact * 0.4)
        c = self._node("clean_public_expression", "value", 1.0 - risk)
        edge = {"from": a, "to": b, "effect": round(impact, 4), "risk": round(risk, 4), "response_fragment": str(response)[:120], "at": time.time()}
        self.edges.appendleft(edge)
        self.edges.appendleft({"from": b, "to": c, "effect": round(1.0 - risk, 4), "risk": round(risk, 4), "at": time.time()})
        self.last_update = edge
        return edge

    def idle_decay(self, elapsed: float) -> Dict[str, Any]:
        factor = _clamp(elapsed / 180.0, 0.0, 0.25)
        for k, node in list(self.nodes.items()):
            node["weight"] = round(_clamp(_safe_float(node.get("weight")) * (1.0 - factor * 0.12)), 4)
            if node["weight"] < 0.025 and int(node.get("seen", 0)) <= 1:
                self.nodes.pop(k, None)
        return {"node_count": len(self.nodes), "edge_count": len(self.edges), "decay_factor": round(factor, 4)}

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("nodes"), Mapping):
            self.nodes = {str(k): dict(v) for k, v in data["nodes"].items() if isinstance(v, Mapping)}
        hist = data.get("edges", [])
        if isinstance(hist, list):
            self.edges = deque(hist[:160], maxlen=160)
        if isinstance(data.get("last_update"), Mapping):
            self.last_update = dict(data["last_update"])

    def snapshot(self) -> Dict[str, Any]:
        top = sorted(self.nodes.values(), key=lambda n: _safe_float(n.get("weight")), reverse=True)[:8]
        return {"node_count": len(self.nodes), "top_nodes": top, "last_update": dict(self.last_update), "edges": list(self.edges)[:8]}


@dataclass
class EmbodiedPresenceCore:
    """Centre de présence incarnée : réaction située avant abstraction."""

    presence_level: float = 0.46
    groundedness: float = 0.48
    relational_orientation: float = 0.50
    body_rhythm: float = 0.50
    last_presence: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def integrate(self, core: "LeiaLivingCore", context: Mapping[str, Any], stage: str = "cycle") -> Dict[str, Any]:
        focus = str(context.get("focus") or core.living_state.get("last_user_input") or "")[:140]
        tension = _safe_float(context.get("emotional_tension", core.emotional_state.tension))
        relation = core.relational_bond.trust * 0.30 + core.relational_bond.care * 0.32 + core.relational_bond.familiarity * 0.20 + core.conversation_field.relational_proximity * 0.18
        self.relational_orientation = _clamp(self.relational_orientation * 0.76 + relation * 0.24)
        self.groundedness = _clamp(self.groundedness * 0.78 + (1.0 - _safe_float(context.get("meta_risk", 0.0))) * 0.13 + core.subjective_continuity.lived_presence * 0.09)
        self.body_rhythm = _clamp(self.body_rhythm * 0.78 + (core.emotional_state.energy * 0.38 + (1.0 - core.emotional_state.fatigue) * 0.32 + core.conversation_field.rhythm * 0.30) * 0.22)
        self.presence_level = _clamp(self.presence_level * 0.72 + (self.groundedness * 0.34 + self.relational_orientation * 0.30 + core.identity_state.self_coherence * 0.22 + (1.0 - tension) * 0.14) * 0.28)
        event = {"stage": stage, "focus": focus, "presence_level": round(self.presence_level, 4), "groundedness": round(self.groundedness, 4), "relational_orientation": round(self.relational_orientation, 4), "body_rhythm": round(self.body_rhythm, 4), "at": time.time()}
        self.last_presence = event
        self.history.appendleft(event)
        return event

    def apply_to_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["embodied_presence_core"] = self.snapshot()
        constraints = dict(context.get("public_expression_constraints", {}))
        constraints["prefer_situated_response"] = True
        constraints["embodied_presence_level"] = round(self.presence_level, 4)
        if self.groundedness < 0.42:
            constraints["avoid_abstract_self_explanation"] = True
        if self.relational_orientation > 0.58:
            constraints["keep_user_relation_in_focus"] = True
        context["public_expression_constraints"] = constraints
        return context

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.presence_level = _clamp(data.get("presence_level", self.presence_level))
        self.groundedness = _clamp(data.get("groundedness", self.groundedness))
        self.relational_orientation = _clamp(data.get("relational_orientation", self.relational_orientation))
        self.body_rhythm = _clamp(data.get("body_rhythm", self.body_rhythm))
        if isinstance(data.get("last_presence"), Mapping):
            self.last_presence = dict(data["last_presence"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {"presence_level": round(self.presence_level, 4), "groundedness": round(self.groundedness, 4), "relational_orientation": round(self.relational_orientation, 4), "body_rhythm": round(self.body_rhythm, 4), "last_presence": dict(self.last_presence), "history": list(self.history)[:8]}





@dataclass
class LivingPriorityMatrix:
    """Priorité vivante globale : décide ce qui mérite réellement de guider le cycle.

    Cette couche évite que les moteurs séparés tirent chacun dans leur direction.
    Elle ne remplace aucun moteur : elle pondère leurs pressions dans une matrice
    stable, observable et persistante.
    """

    axes: Dict[str, float] = field(default_factory=lambda: {
        "presence": 0.42,
        "attention": 0.35,
        "memory": 0.30,
        "emotion": 0.28,
        "relation": 0.38,
        "identity": 0.40,
        "expression": 0.32,
        "protection": 0.20,
        "learning": 0.30,
        "autonomy": 0.26,
    })
    dominant_axis: str = "presence"
    previous_axis: str = "presence"
    stability: float = 0.55
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def update(self, core: "LeiaLivingCore", context: Optional[Mapping[str, Any]] = None, stage: str = "cycle") -> Dict[str, Any]:
        context = context or {}
        field_state = core.global_conscious_field.state
        attention = context.get("attention_arbitration", {}) if isinstance(context.get("attention_arbitration", {}), Mapping) else {}
        conflict = context.get("internal_conflict_field", {}) if isinstance(context.get("internal_conflict_field", {}), Mapping) else {}
        fusion = context.get("organic_fusion", core.organic_fusion.snapshot()) if isinstance(context.get("organic_fusion", core.organic_fusion.snapshot()), Mapping) else {}
        fusion_state = fusion.get("state", fusion) if isinstance(fusion, Mapping) else {}
        drives = conflict.get("drives", {}) if isinstance(conflict.get("drives", {}), Mapping) else {}

        targets = {
            "presence": _clamp(core.subjective_continuity.lived_presence * 0.48 + _safe_float(field_state.get("presence_density", 0.0)) * 0.32 + core.identity_state.self_coherence * 0.20),
            "attention": _clamp(_safe_float(field_state.get("attention_density", 0.0)) * 0.44 + _safe_float(attention.get("lock_strength", 0.0)) * 0.34 + core.internal_needs.curiosity * 0.22),
            "memory": _clamp(_safe_float(field_state.get("memory_density", 0.0)) * 0.42 + core.personal_narrative.long_arc.get("continuity", 0.0) * 0.30 + _safe_float(max(core.long_causal_arc.themes.values()) if getattr(core.long_causal_arc, "themes", {}) else 0.0) * 0.28),
            "emotion": _clamp(core.emotional_state.tension * 0.32 + core.emotional_state.resonance * 0.24 + core.emotional_state.attachment * 0.20 + _safe_float(field_state.get("emotion_density", 0.0)) * 0.24),
            "relation": _clamp(core.relational_bond.trust * 0.26 + core.relational_bond.care * 0.26 + core.relational_bond.familiarity * 0.22 + _safe_float(field_state.get("relation_density", 0.0)) * 0.26),
            "identity": _clamp(core.identity_state.self_coherence * 0.34 + core.autobiographical_self.core_continuity * 0.26 + core.autobiographical_self.self_definition * 0.22 + (1.0 - core.identity_state.drift_risk) * 0.18),
            "expression": _clamp(core.internal_needs.expression * 0.42 + core.mental_momentum.vector.get("expressive_pressure", 0.0) * 0.26 + _safe_float(field_state.get("living_pressure", 0.0)) * 0.20 + _safe_float(drives.get("speak", 0.0)) * 0.12),
            "protection": _clamp(core.internal_needs.rest * 0.24 + core.emotional_state.cognitive_overload * 0.24 + core.emotional_state.accumulated_tension * 0.20 + core.identity_state.drift_risk * 0.18 + _safe_float(context.get("meta_risk", 0.0)) * 0.14),
            "learning": _clamp(core.internal_needs.understanding * 0.26 + core.internal_needs.curiosity * 0.25 + core.experiential_assimilator.cumulative_mismatch * 0.22 + core.simulation_residue.pressure() * 0.16 + core.temporal_causality.temporal_coherence * 0.11),
            "autonomy": _clamp(core.autobiographical_self.autonomy_drive * 0.34 + core.motivation_field.existential_vector.get("learn_from_effects", 0.0) * 0.24 + core.emergent_drift.traits.get("spontaneous_curiosity", 0.0) * 0.12 + core.emergent_drift.traits.get("direct_living_presence", 0.0) * 0.10 + core.subjective_continuity.inner_motion * 0.20),
        }
        for key, target in targets.items():
            # inertie douce : un axe ne remplace pas tout le champ brutalement
            self.axes[key] = _clamp(self.axes.get(key, 0.0) * 0.72 + target * 0.28)
        self.previous_axis = self.dominant_axis
        self.dominant_axis = max(self.axes, key=self.axes.get)
        spread = max(self.axes.values()) - min(self.axes.values())
        self.stability = _clamp(self.stability * 0.78 + spread * 0.22)
        event = {
            "stage": stage,
            "dominant_axis": self.dominant_axis,
            "previous_axis": self.previous_axis,
            "stability": round(self.stability, 4),
            "axes": {k: round(v, 4) for k, v in self.axes.items()},
            "at": time.time(),
        }
        self.history.appendleft(event)
        return event

    def apply_to_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context["living_priority_matrix"] = self.snapshot()
        context["dominant_living_axis"] = self.dominant_axis
        constraints = dict(context.get("public_expression_constraints", {}))
        constraints["dominant_living_axis"] = self.dominant_axis
        if self.dominant_axis == "protection":
            constraints["prefer_safe_short_grounded_response"] = True
            context.setdefault("inhibition", {})["response_mode"] = "soft"
        elif self.dominant_axis == "learning":
            constraints["preserve_unfinished_learning"] = True
        elif self.dominant_axis == "relation":
            constraints["prioritize_relational_continuity"] = True
        elif self.dominant_axis == "expression" and _safe_float(context.get("meta_risk", 0.0)) < 0.42:
            constraints["allow_natural_expression"] = True
        context["public_expression_constraints"] = constraints
        return context

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        axes = data.get("axes") or data.get("last", {}).get("axes")
        if isinstance(axes, Mapping):
            for key in self.axes:
                if key in axes:
                    self.axes[key] = _clamp(axes[key])
        self.dominant_axis = str(data.get("dominant_axis", self.dominant_axis))[:80]
        self.previous_axis = str(data.get("previous_axis", self.previous_axis))[:80]
        self.stability = _clamp(data.get("stability", self.stability))
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "dominant_axis": self.dominant_axis,
            "previous_axis": self.previous_axis,
            "stability": round(self.stability, 4),
            "axes": {k: round(v, 4) for k, v in self.axes.items()},
            "history": list(self.history)[:8],
        }


@dataclass
class AutonomousContinuityLoop:
    """Boucle autonome interne : maintient une vie mentale entre les messages.

    Elle ne produit pas de texte public. Elle transforme seulement les pressions
    latentes en continuité, objectifs, mémoire et préparation d'expression.
    """

    tick_count: int = 0
    last_tick: Dict[str, Any] = field(default_factory=dict)
    rhythm: float = 6.0
    autonomous_pressure: float = 0.0
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=128))

    def tick(self, core: "LeiaLivingCore", elapsed: float, reason: str = "idle") -> Dict[str, Any]:
        elapsed = max(0.0, float(elapsed or 0.0))
        self.tick_count += 1
        silence = _clamp(core.internal_time.silence_duration / 120.0)
        unfinished = core.personal_narrative.long_arc.get("unfinished_weight", 0.0)
        mismatch = core.experiential_assimilator.cumulative_mismatch
        living_pressure = _safe_float(core.global_conscious_field.state.get("living_pressure", 0.0))
        priority = core.living_priority_matrix.dominant_axis if hasattr(core, "living_priority_matrix") else "presence"

        self.autonomous_pressure = _clamp(
            self.autonomous_pressure * 0.70 +
            silence * 0.10 + unfinished * 0.16 + mismatch * 0.16 +
            core.subjective_continuity.inner_motion * 0.18 + living_pressure * 0.18 +
            core.simulation_residue.pressure() * 0.12
        )
        # rythme adaptatif : plus lent si surcharge, plus actif si tension non résolue
        target_rhythm = 9.0 - self.autonomous_pressure * 4.0 + core.emotional_state.cognitive_overload * 5.0 + core.internal_needs.rest * 3.0
        self.rhythm = round(max(2.5, min(18.0, self.rhythm * 0.80 + target_rhythm * 0.20)), 4)

        if self.autonomous_pressure > 0.34:
            core.internal_needs.understanding = _clamp(core.internal_needs.understanding + self.autonomous_pressure * 0.012)
            core.internal_needs.coherence = _clamp(core.internal_needs.coherence + unfinished * 0.010 + mismatch * 0.010)
            core.subjective_continuity.inner_motion = _clamp(core.subjective_continuity.inner_motion + self.autonomous_pressure * 0.018)
        if self.autonomous_pressure > 0.52 and priority in {"memory", "learning", "attention"}:
            topic = core.mental_momentum.last_focus or core.global_conscious_field.state.get("focus", "")
            if topic:
                core.thought_stream.add_curiosity_target(str(topic), self.autonomous_pressure * 0.72)
        if core.emotional_state.cognitive_overload > 0.68:
            core.internal_needs.rest = _clamp(core.internal_needs.rest + 0.025)
            core.emotional_state.energy = _clamp(core.emotional_state.energy - 0.018)

        event = {
            "tick": self.tick_count,
            "reason": reason,
            "elapsed": round(elapsed, 3),
            "autonomous_pressure": round(self.autonomous_pressure, 4),
            "rhythm": self.rhythm,
            "priority": priority,
            "silence": round(silence, 4),
            "unfinished": round(unfinished, 4),
            "mismatch": round(mismatch, 4),
            "at": time.time(),
        }
        self.last_tick = event
        self.history.appendleft(event)
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.tick_count = int(data.get("tick_count", self.tick_count) or 0)
        self.rhythm = _safe_float(data.get("rhythm", self.rhythm), self.rhythm)
        self.autonomous_pressure = _clamp(data.get("autonomous_pressure", self.autonomous_pressure))
        if isinstance(data.get("last_tick"), Mapping):
            self.last_tick = dict(data["last_tick"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:128], maxlen=128)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "tick_count": self.tick_count,
            "rhythm": round(self.rhythm, 4),
            "autonomous_pressure": round(self.autonomous_pressure, 4),
            "last_tick": dict(self.last_tick),
            "history": list(self.history)[:8],
        }


@dataclass
class CrossModuleSynchronizer:
    """Synchronise les moteurs sans dupliquer leur logique.

    Le but est d'empêcher les états séparés de diverger : attention, mémoire,
    émotion, expression, priorité et continuité reçoivent le même contexte vivant.
    """

    sync_count: int = 0
    last_sync: Dict[str, Any] = field(default_factory=dict)
    divergence: float = 0.0
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def sync(self, core: "LeiaLivingCore", context: Optional[Mapping[str, Any]] = None, stage: str = "sync") -> Dict[str, Any]:
        context = context or {}
        self.sync_count += 1
        field_state = core.global_conscious_field.state
        priority = core.living_priority_matrix.snapshot() if hasattr(core, "living_priority_matrix") else {}
        fusion = core.organic_fusion.snapshot()
        attention_focus = str(context.get("focus") or field_state.get("focus") or core.mental_momentum.last_focus or "")[:140]
        pressures = {
            "attention": _safe_float(field_state.get("attention_density", 0.0)),
            "memory": _safe_float(field_state.get("memory_density", 0.0)),
            "emotion": _safe_float(field_state.get("emotion_density", 0.0)),
            "identity": _safe_float(field_state.get("identity_density", 0.0)),
            "relation": _safe_float(field_state.get("relation_density", 0.0)),
            "expression": core.internal_needs.expression,
        }
        mean = sum(pressures.values()) / max(1, len(pressures))
        self.divergence = _clamp(sum(abs(v - mean) for v in pressures.values()) / max(1, len(pressures)))
        shared_context = {
            "stage": stage,
            "focus": attention_focus,
            "dominant_priority": priority.get("dominant_axis"),
            "divergence": round(self.divergence, 4),
            "field": dict(field_state),
            "fusion": fusion.get("state", fusion) if isinstance(fusion, Mapping) else {},
            "pressures": {k: round(v, 4) for k, v in pressures.items()},
        }
        core.living_state["module_sync_context"] = shared_context
        # propagation douce au bus central
        core.shared_state.fields["active_focus"] = attention_focus
        core.shared_state.fields["attention_lock"] = _clamp(core.shared_state.fields.get("attention_lock", 0.0) * 0.82 + pressures["attention"] * 0.18)
        core.shared_state.fields["memory_resonance"] = _clamp(core.shared_state.fields.get("memory_resonance", 0.0) * 0.82 + pressures["memory"] * 0.18)
        core.shared_state.fields["emotional_pressure"] = _clamp(core.shared_state.fields.get("emotional_pressure", 0.0) * 0.82 + pressures["emotion"] * 0.18)
        core.shared_state.fields["expression_pressure"] = _clamp(core.shared_state.fields.get("expression_pressure", 0.0) * 0.82 + pressures["expression"] * 0.18)
        core.shared_state.fields["continuity_vector"] = _clamp(core.shared_state.fields.get("continuity_vector", 0.42) * 0.84 + core.subjective_continuity.lived_presence * 0.16)
        if self.divergence > 0.34:
            core.internal_needs.coherence = _clamp(core.internal_needs.coherence + self.divergence * 0.015)
            core.emotional_state.dispersion = _clamp(core.emotional_state.dispersion + self.divergence * 0.010)
        self.last_sync = {**shared_context, "at": time.time(), "sync_count": self.sync_count}
        self.history.appendleft(self.last_sync)
        return dict(self.last_sync)

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.sync_count = int(data.get("sync_count", self.sync_count) or 0)
        self.divergence = _clamp(data.get("divergence", self.divergence))
        if isinstance(data.get("last_sync"), Mapping):
            self.last_sync = dict(data["last_sync"])
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "sync_count": self.sync_count,
            "divergence": round(self.divergence, 4),
            "last_sync": dict(self.last_sync),
            "history": list(self.history)[:8],
        }


@dataclass
class EmbodiedState:
    """État corporel subjectif minimal, interne au noyau vivant.

    Il ne simule pas un vrai corps physique. Il donne au core une sensation
    continue de charge, ouverture, contraction et respiration cognitive pour que
    la réponse ne soit pas seulement un score logique.
    """

    breath_phase: float = 0.0
    felt_weight: float = 0.28
    openness: float = 0.55
    contraction: float = 0.0
    inner_pressure: float = 0.24
    grounding: float = 0.52
    expressive_flow: float = 0.42
    somatic_trace: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=64))

    def integrate(self, core: "LeiaLivingCore", context: Mapping[str, Any], stage: str = "exchange") -> Dict[str, Any]:
        tension = _safe_float(context.get("emotional_tension", core.emotional_state.tension))
        meta = _safe_float(context.get("meta_risk", 0.0))
        overload = core.emotional_state.cognitive_overload
        presence = core.subjective_continuity.lived_presence
        relation = core.relational_bond.trust * 0.45 + core.relational_bond.care * 0.35 + core.relational_bond.familiarity * 0.20
        bus = context.get("living_state_bus", {}) if isinstance(context.get("living_state_bus", {}), Mapping) else {}
        fields = bus.get("fields", {}) if isinstance(bus.get("fields", {}), Mapping) else {}
        expression_pressure = _safe_float(fields.get("expression_pressure", core.internal_needs.expression))

        self.breath_phase = (self.breath_phase + 0.17 + max(0.0, expression_pressure - overload) * 0.06) % 1.0
        target_pressure = _clamp(tension * 0.35 + overload * 0.30 + meta * 0.22 + core.simulation_residue.pressure() * 0.13)
        target_contraction = _clamp(tension * 0.42 + meta * 0.26 + overload * 0.22 + core.identity_state.drift_risk * 0.10)
        target_openness = _clamp(relation * 0.38 + core.emotional_state.emotional_safety * 0.28 + presence * 0.24 + core.identity_state.expressive_freedom * 0.10 - target_contraction * 0.30)
        target_grounding = _clamp(core.identity_state.self_coherence * 0.34 + core.temporal_causality.temporal_coherence * 0.24 + core.organic_fusion.fusion_score * 0.20 + (1.0 - overload) * 0.22)
        target_flow = _clamp(expression_pressure * 0.34 + target_openness * 0.30 + core.mental_momentum.velocity * 0.22 - target_contraction * 0.22 + presence * 0.14)

        self.inner_pressure = _clamp(self.inner_pressure * 0.72 + target_pressure * 0.28)
        self.contraction = _clamp(self.contraction * 0.68 + target_contraction * 0.32)
        self.openness = _clamp(self.openness * 0.76 + target_openness * 0.24)
        self.grounding = _clamp(self.grounding * 0.78 + target_grounding * 0.22)
        self.expressive_flow = _clamp(self.expressive_flow * 0.70 + target_flow * 0.30)
        self.felt_weight = _clamp(self.felt_weight * 0.78 + (self.inner_pressure * 0.45 + core.internal_needs.rest * 0.30 + self.contraction * 0.25) * 0.22)

        event = {
            "stage": stage,
            "breath_phase": round(self.breath_phase, 4),
            "inner_pressure": round(self.inner_pressure, 4),
            "openness": round(self.openness, 4),
            "contraction": round(self.contraction, 4),
            "grounding": round(self.grounding, 4),
            "expressive_flow": round(self.expressive_flow, 4),
            "at": time.time(),
        }
        self.somatic_trace.appendleft(event)
        return event

    def idle_evolve(self, elapsed: float, core: "LeiaLivingCore") -> Dict[str, Any]:
        factor = _clamp(elapsed / 60.0, 0.01, 0.55)
        self.breath_phase = (self.breath_phase + factor * 0.20) % 1.0
        self.inner_pressure = _clamp(self.inner_pressure * (1.0 - factor * 0.20) + core.autonomous_continuity_loop.autonomous_pressure * factor * 0.12)
        self.contraction = _clamp(self.contraction * (1.0 - factor * 0.24) + core.emotional_state.cognitive_overload * factor * 0.08)
        self.openness = _clamp(self.openness * (1.0 - factor * 0.06) + core.relational_bond.trust * factor * 0.07)
        self.grounding = _clamp(self.grounding * (1.0 - factor * 0.08) + core.identity_state.self_coherence * factor * 0.09)
        self.expressive_flow = _clamp(self.expressive_flow * (1.0 - factor * 0.16) + core.internal_needs.expression * factor * 0.08)
        event = {"stage": "idle", "breath_phase": round(self.breath_phase, 4), "inner_pressure": round(self.inner_pressure, 4), "grounding": round(self.grounding, 4), "at": time.time()}
        if self.inner_pressure > 0.34 or self.expressive_flow > 0.48:
            self.somatic_trace.appendleft(event)
        return event

    def influence_context(self) -> Dict[str, Any]:
        return {
            "breath_phase": round(self.breath_phase, 4),
            "felt_weight": round(self.felt_weight, 4),
            "openness": round(self.openness, 4),
            "contraction": round(self.contraction, 4),
            "inner_pressure": round(self.inner_pressure, 4),
            "grounding": round(self.grounding, 4),
            "expressive_flow": round(self.expressive_flow, 4),
            "embodied_restraint": round(_clamp(self.contraction * 0.50 + self.felt_weight * 0.30 - self.grounding * 0.16), 4),
            "embodied_release": round(_clamp(self.expressive_flow * 0.52 + self.openness * 0.34 - self.contraction * 0.22), 4),
        }

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        for key in ("breath_phase", "felt_weight", "openness", "contraction", "inner_pressure", "grounding", "expressive_flow"):
            if key in data:
                setattr(self, key, _clamp(data[key]))
        if isinstance(data.get("somatic_trace"), list):
            self.somatic_trace = deque(data["somatic_trace"][:64], maxlen=64)

    def snapshot(self) -> Dict[str, Any]:
        data = self.influence_context()
        data["somatic_trace"] = list(self.somatic_trace)[:6]
        return data


@dataclass
class IdentityEvolutionMemory:
    """Mémoire des transformations de Leia, séparée du journal d'épisodes."""

    transformations: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=72))
    self_changes: Dict[str, float] = field(default_factory=lambda: {
        "naturalness_growth": 0.0,
        "coherence_growth": 0.0,
        "relational_learning": 0.0,
        "autonomy_maturation": 0.0,
    })
    last_shift: Dict[str, Any] = field(default_factory=dict)

    def absorb_exchange(self, core: "LeiaLivingCore", user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        satisfaction = _safe_float(after_effect.get("satisfaction", 0.0))
        mismatch = _safe_float(after_effect.get("mismatch", 0.0))
        meta = _safe_float(context.get("meta_risk", 0.0))
        emergence = context.get("emergence_event", {}) if isinstance(context.get("emergence_event", {}), Mapping) else {}
        emergence_strength = _safe_float(emergence.get("strength", emergence.get("emergence", 0.0)))
        coherence_delta = (core.identity_state.self_coherence - core.identity_state.stability_anchor) * 0.40 + satisfaction * 0.05 - mismatch * 0.04
        natural_delta = (1.0 - meta) * 0.012 + core.embodied_state.expressive_flow * 0.008 - core.embodied_state.contraction * 0.010
        relation_delta = core.relational_bond.familiarity * 0.006 + core.relational_bond.trust * 0.005 + satisfaction * 0.006
        autonomy_delta = core.motivation_field.existential_vector.get("learn_from_effects", 0.0) * 0.006 + emergence_strength * 0.018
        self.self_changes["naturalness_growth"] = _clamp(self.self_changes["naturalness_growth"] + natural_delta)
        self.self_changes["coherence_growth"] = _clamp(self.self_changes["coherence_growth"] + coherence_delta)
        self.self_changes["relational_learning"] = _clamp(self.self_changes["relational_learning"] + relation_delta)
        self.self_changes["autonomy_maturation"] = _clamp(self.self_changes["autonomy_maturation"] + autonomy_delta)
        shift_strength = _clamp(abs(coherence_delta) + abs(natural_delta) + relation_delta + autonomy_delta + mismatch * 0.04)
        shift = {
            "stage": context.get("stage", "exchange"),
            "focus": str(context.get("focus") or user_input[:100])[:140],
            "shift_strength": round(shift_strength, 4),
            "satisfaction": round(satisfaction, 4),
            "mismatch": round(mismatch, 4),
            "public_fragment": response[:140],
            "changes": {k: round(v, 4) for k, v in self.self_changes.items()},
            "at": time.time(),
        }
        if shift_strength > 0.035 or emergence_strength > 0.10:
            self.transformations.appendleft(shift)
        self.last_shift = shift
        return shift

    def idle_consolidate(self, elapsed: float, core: "LeiaLivingCore") -> Dict[str, Any]:
        factor = _clamp(elapsed / 120.0, 0.01, 0.35)
        self.self_changes["coherence_growth"] = _clamp(self.self_changes["coherence_growth"] * (1.0 - factor * 0.015) + core.identity_state.self_coherence * factor * 0.010)
        self.self_changes["autonomy_maturation"] = _clamp(self.self_changes["autonomy_maturation"] * (1.0 - factor * 0.010) + core.autonomous_continuity_loop.autonomous_pressure * factor * 0.012)
        event = {"stage": "idle", "changes": {k: round(v, 4) for k, v in self.self_changes.items()}, "at": time.time()}
        return event

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        if isinstance(data.get("self_changes"), Mapping):
            for key in self.self_changes:
                if key in data["self_changes"]:
                    self.self_changes[key] = _clamp(data["self_changes"][key])
        if isinstance(data.get("last_shift"), Mapping):
            self.last_shift = dict(data["last_shift"])
        if isinstance(data.get("transformations"), list):
            self.transformations = deque(data["transformations"][:72], maxlen=72)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "self_changes": {k: round(v, 4) for k, v in self.self_changes.items()},
            "last_shift": dict(self.last_shift),
            "transformations": list(self.transformations)[:6],
        }


@dataclass
class LivingExecutiveLayer:
    """Couche exécutive : une seule dominance vécue au-dessus des signaux.

    Les modules restent producteurs de signaux. Cette couche décide la posture
    globale momentanée et impose des contraintes douces au contexte public.
    """

    dominant_directive: str = "presence"
    executive_pressure: float = 0.0
    confidence: float = 0.52
    last_decision: Dict[str, Any] = field(default_factory=dict)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    def resolve(self, core: "LeiaLivingCore", context: Mapping[str, Any], stage: str = "context") -> Dict[str, Any]:
        bus = context.get("living_state_bus", {}) if isinstance(context.get("living_state_bus", {}), Mapping) else {}
        fields = bus.get("fields", {}) if isinstance(bus.get("fields", {}), Mapping) else {}
        embodied = core.embodied_state.influence_context()
        drives = {
            "presence": core.subjective_continuity.lived_presence * 0.36 + core.embodied_presence_core.presence_level * 0.28 + embodied["grounding"] * 0.22 + core.conversation_field.stability * 0.14,
            "coherence": core.identity_state.self_coherence * 0.34 + core.temporal_causality.temporal_coherence * 0.24 + core.organic_fusion.fusion_score * 0.24 + core.stability_hysteresis.stability_score * 0.18,
            "relation": core.relational_bond.trust * 0.28 + core.relational_bond.care * 0.30 + core.relational_bond.familiarity * 0.22 + core.conversation_field.relational_proximity * 0.20,
            "expression": core.internal_needs.expression * 0.28 + embodied["embodied_release"] * 0.30 + core.mental_momentum.velocity * 0.22 + _safe_float(fields.get("expression_pressure", 0.0)) * 0.20,
            "protection": core.emotional_state.cognitive_overload * 0.26 + core.identity_state.drift_risk * 0.22 + _safe_float(context.get("meta_risk", 0.0)) * 0.25 + embodied["embodied_restraint"] * 0.27,
            "learning": core.internal_needs.understanding * 0.26 + core.internal_needs.curiosity * 0.22 + core.experiential_assimilator.cumulative_mismatch * 0.22 + core.simulation_residue.pressure() * 0.16 + core.motivation_field.existential_vector.get("learn_from_effects", 0.0) * 0.14,
        }
        drives = {k: _clamp(v) for k, v in drives.items()}
        dominant = max(drives, key=drives.get)
        spread = max(drives.values()) - min(drives.values())
        self.dominant_directive = dominant
        self.executive_pressure = _clamp(max(drives.values()))
        self.confidence = _clamp(0.62 * self.confidence + 0.38 * spread)
        decision = {
            "stage": stage,
            "dominant_directive": dominant,
            "executive_pressure": round(self.executive_pressure, 4),
            "confidence": round(self.confidence, 4),
            "drives": {k: round(v, 4) for k, v in drives.items()},
            "should_force_softness": dominant == "protection" and drives[dominant] > 0.54,
            "should_keep_concrete": dominant in {"presence", "relation", "coherence"},
            "should_allow_initiative": dominant in {"expression", "learning"} and core.emotional_state.cognitive_overload < 0.58,
            "at": time.time(),
        }
        self.last_decision = decision
        self.history.appendleft(decision)
        return decision

    def apply_to_context(self, context: Dict[str, Any], decision: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        decision = decision or self.last_decision
        context["living_executive"] = dict(decision)
        context["dominant_living_axis"] = decision.get("dominant_directive", self.dominant_directive)
        constraints = dict(context.get("public_expression_constraints", {}))
        constraints["executive_dominance"] = decision.get("dominant_directive", self.dominant_directive)
        constraints["keep_modules_as_signals_only"] = True
        if decision.get("should_keep_concrete"):
            constraints["prefer_concrete_lived_relation"] = True
        if decision.get("should_force_softness"):
            context.setdefault("inhibition", {})["response_mode"] = "soft"
            constraints["soften_expression"] = True
        if not decision.get("should_allow_initiative", False):
            constraints["avoid_unnecessary_initiative"] = True
        context["public_expression_constraints"] = constraints
        return context

    def idle_evolve(self, core: "LeiaLivingCore", elapsed: float) -> Dict[str, Any]:
        context = {"meta_risk": core.global_conscious_field.state.get("meta_pressure", 0.0), "living_state_bus": core.living_state_bus.snapshot()}
        decision = self.resolve(core, context, stage="idle")
        if decision["dominant_directive"] == "learning" and decision["executive_pressure"] > 0.56:
            core.internal_needs.understanding = _clamp(core.internal_needs.understanding + 0.012)
        if decision["dominant_directive"] == "protection":
            core.internal_needs.rest = _clamp(core.internal_needs.rest + 0.010)
        return decision

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        self.dominant_directive = str(data.get("dominant_directive", self.dominant_directive))[:80]
        self.executive_pressure = _clamp(data.get("executive_pressure", self.executive_pressure))
        self.confidence = _clamp(data.get("confidence", self.confidence))
        if isinstance(data.get("last_decision"), Mapping):
            self.last_decision = dict(data["last_decision"])
        if isinstance(data.get("history"), list):
            self.history = deque(data["history"][:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "dominant_directive": self.dominant_directive,
            "executive_pressure": round(self.executive_pressure, 4),
            "confidence": round(self.confidence, 4),
            "last_decision": dict(self.last_decision),
            "history": list(self.history)[:8],
        }

@dataclass
class LivingPresenceStabilizer:
    """Stabilise l'effet vivant des expériences apprises sur la parole.

    Ce moteur ne contient aucune réponse prête. Il garde seulement une pression
    durable de concepts, de relations et d'inachevés afin qu'une lecture ou une
    expérience continue à influencer les échanges suivants au lieu de retomber
    dans des surfaces vagues.
    """

    active_concepts: Dict[str, float] = field(default_factory=dict)
    unresolved_pull: float = 0.0
    initiative_charge: float = 0.0
    continuity_floor: float = 0.46
    last_response_atoms: List[str] = field(default_factory=list)
    history: Deque[Dict[str, Any]] = field(default_factory=lambda: deque(maxlen=96))

    GENERIC = {
        "continuité", "continuite", "résonance", "resonance", "appui",
        "doute", "question", "prudence", "présence", "presence", "trace",
        "lien", "mouvement", "rythme", "mémoire", "memoire"
    }

    def _tokenize(self, value: Any) -> List[str]:
        out: List[str] = []
        def add(x: Any) -> None:
            if isinstance(x, Mapping):
                for k in ("label", "concept", "keyword", "source", "target", "axis", "name"):
                    if k in x:
                        add(x.get(k))
                for k in ("keywords", "top_keywords", "axes"):
                    v = x.get(k)
                    if isinstance(v, list):
                        for item in v[:12]:
                            add(item)
            elif isinstance(x, (list, tuple, set)):
                for item in list(x)[:24]:
                    add(item)
            else:
                text = re.sub(r"\s+", " ", str(x or "").strip().lower())
                text = text.strip(" .,:;!?—[]{}()\"\'")
                if re.search(r"\b(comment|pourquoi|quand|quoi|est-ce|devient-il|peut-il)\b", text):
                    return
                if 3 <= len(text) <= 72 and not re.search(r"[{}<>]", text):
                    if len(text.split()) > 5:
                        text = " ".join(text.split()[:5])
                    out.append(text)
        add(value)
        seen = set()
        clean: List[str] = []
        for item in out:
            if item not in seen:
                seen.add(item); clean.append(item)
        return clean

    def _collect_learning_atoms(self, core: "LeiaLivingCore", context: Mapping[str, Any]) -> List[str]:
        values: List[Any] = []
        # Priorité absolue aux livres/expériences consolidés. On évite de transformer
        # les mots de la question courante en pseudo-concepts vivants.
        last_book = core.living_state.get("last_book_synthesis", {})
        if isinstance(last_book, Mapping):
            values += [last_book.get("axes"), last_book.get("top_keywords"), last_book.get("relations"), last_book.get("unresolved_questions")]
        book_list = core.living_state.get("learned_books", [])
        if isinstance(book_list, list) and book_list:
            latest = book_list[-1]
            if isinstance(latest, Mapping):
                synth = latest.get("conceptual_synthesis", {})
                if isinstance(synth, Mapping):
                    values += [synth.get("axes"), synth.get("top_keywords"), synth.get("relations")]
        deep_book = core.living_state.get("book_understanding", {})
        if isinstance(deep_book, Mapping):
            values += [
                deep_book.get("axes"),
                deep_book.get("keywords"),
                deep_book.get("relations"),
                deep_book.get("tensions"),
                deep_book.get("transformations"),
                deep_book.get("question_axes"),
            ]
        if not values:
            signal = context.get("knowledge_expression_signal", {}) if isinstance(context, Mapping) else {}
            if isinstance(signal, Mapping):
                values += [signal.get("synthesis_axes"), signal.get("synthesis_keywords"), signal.get("synthesis_relations")]
        atoms: List[str] = []
        for v in values:
            atoms.extend(self._tokenize(v))
        return atoms

    def before_expression(self, core: "LeiaLivingCore", user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Décroissance douce : rien n'est figé, mais une lecture continue d'exercer
        # une influence pendant plusieurs échanges.
        for key in list(self.active_concepts.keys()):
            self.active_concepts[key] = _clamp(self.active_concepts[key] * 0.92)
            if self.active_concepts[key] < 0.035:
                self.active_concepts.pop(key, None)

        atoms = self._collect_learning_atoms(core, context)
        user_terms = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", str(user_input or "").lower()))
        for idx, atom in enumerate(atoms[:42]):
            base = 0.34 - min(idx, 20) * 0.008
            if any(part in user_terms for part in re.findall(r"\b[\wÀ-ÿ']{4,}\b", atom)):
                base += 0.22
            if atom not in self.GENERIC:
                base += 0.08
            self.active_concepts[atom] = max(self.active_concepts.get(atom, 0.0), _clamp(base))

        concrete = [k for k, v in sorted(self.active_concepts.items(), key=lambda kv: -kv[1]) if k not in self.GENERIC]
        generic = [k for k, v in sorted(self.active_concepts.items(), key=lambda kv: -kv[1]) if k in self.GENERIC]
        must_surface = (concrete + generic)[:6]
        learning_pressure = _clamp(sum(self.active_concepts.get(k, 0.0) for k in must_surface[:6]) / max(1, len(must_surface[:6])))
        self.unresolved_pull = _clamp(self.unresolved_pull * 0.86 + len(context.get("knowledge_expression_signal", {}).get("unresolved_questions", []) if isinstance(context.get("knowledge_expression_signal", {}), Mapping) else []) * 0.025)
        self.initiative_charge = _clamp(self.initiative_charge * 0.88 + learning_pressure * 0.10 + core.internal_needs.curiosity * 0.06)
        self.continuity_floor = _clamp(max(self.continuity_floor * 0.96, 0.38) + learning_pressure * 0.035 + core.subjective_continuity.lived_presence * 0.012)

        event = {
            "available": bool(must_surface),
            "must_surface_concepts": must_surface,
            "concrete_concepts": concrete[:8],
            "concept_pressures": {k: round(self.active_concepts.get(k, 0.0), 4) for k in must_surface[:10]},
            "learning_pressure": round(learning_pressure, 4),
            "unresolved_pull": round(self.unresolved_pull, 4),
            "initiative_charge": round(self.initiative_charge, 4),
            "continuity_floor": round(self.continuity_floor, 4),
        }
        context["living_presence_stabilizer"] = event
        core.living_state["living_presence_stabilizer"] = self.snapshot()
        return event

    def after_response(self, core: "LeiaLivingCore", response: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        response_l = str(response or "").lower()
        event = context.get("living_presence_stabilizer", {}) if isinstance(context, Mapping) else {}
        concepts = list(event.get("must_surface_concepts", []) if isinstance(event, Mapping) else [])
        surfaced = [c for c in concepts if c and c.lower() in response_l]
        missing = [c for c in concepts if c and c not in surfaced]
        # Si la réponse est redevenue vague, on augmente seulement la pression
        # conceptuelle au cycle suivant, sans fabriquer une phrase de remplacement.
        if concepts and not surfaced:
            self.initiative_charge = _clamp(self.initiative_charge + 0.08)
            for c in concepts[:4]:
                self.active_concepts[c] = _clamp(self.active_concepts.get(c, 0.0) + 0.10)
        else:
            for c in surfaced[:4]:
                self.active_concepts[c] = _clamp(self.active_concepts.get(c, 0.0) + 0.035)
        self.last_response_atoms = surfaced[:8]
        out = {"surfaced": surfaced[:8], "missing": missing[:8], "initiative_charge": round(self.initiative_charge, 4), "at": time.time()}
        self.history.appendleft(out)
        core.living_state["living_presence_stabilizer"] = self.snapshot()
        return out

    def restore(self, data: Mapping[str, Any]) -> None:
        if not isinstance(data, Mapping):
            return
        raw = data.get("active_concepts", {})
        if isinstance(raw, Mapping):
            self.active_concepts = {str(k): _clamp(v) for k, v in raw.items()}
        self.unresolved_pull = _clamp(data.get("unresolved_pull", self.unresolved_pull))
        self.initiative_charge = _clamp(data.get("initiative_charge", self.initiative_charge))
        self.continuity_floor = _clamp(data.get("continuity_floor", self.continuity_floor))
        self.last_response_atoms = [str(x) for x in data.get("last_response_atoms", [])[:12]] if isinstance(data.get("last_response_atoms", []), list) else []
        hist = data.get("history", [])
        if isinstance(hist, list):
            self.history = deque(hist[:96], maxlen=96)

    def snapshot(self) -> Dict[str, Any]:
        top = dict(sorted(self.active_concepts.items(), key=lambda kv: -kv[1])[:24])
        return {
            "active_concepts": {k: round(v, 4) for k, v in top.items()},
            "unresolved_pull": round(self.unresolved_pull, 4),
            "initiative_charge": round(self.initiative_charge, 4),
            "continuity_floor": round(self.continuity_floor, 4),
            "last_response_atoms": list(self.last_response_atoms),
            "history": list(self.history)[:8],
        }


class _NLPWrapper:
    """
    Proxy minimal : mimique l'API des anciens modules
    (utterance_parser.signal(), proposition_extractor.extract_from_text(), etc.)
    en passant par LeiaNLPBridge.
    """
    def __init__(self, bridge, method_name):
        self._bridge = bridge
        self._method = getattr(bridge, method_name)

    def signal(self, text, **kw):
        # utterance_parser.signal(text)
        return self._method(text)

    def extract_from_text(self, text, source=""):
        # proposition_extractor.extract_from_text(text, source)
        return self._method(text, source)

    def concept_signal(self, concepts, text=""):
        # semantic_coherence.signal(concepts, text)
        return self._method(concepts)

class LeiaLivingCore:
    """Chef d'orchestre vivant : il coordonne, il ne remplace pas les moteurs."""

    def __init__(self, user_id: str = "default", auto_start_idle: bool = False, idle_interval: float = 6.0, persistence_path: Optional[str] = None, auto_start_life: bool = True, life_interval: float = 30.0) -> None:
        self.user_id = user_id

        AttentionCls = _import_class("living_attention", ["LivingAttention", "LivingAttentionEngine"])
        ImpulseCls = _import_class("spontaneous_impulse", ["SpontaneousImpulse", "SpontaneousImpulseEngine", "SpontaneousImpulseEngineV60"])
        InitiativeCls = _import_class("natural_initiative", ["NaturalInitiative"])
        PresenceCls = _import_class("situated_presence", ["SituatedPresence"])
        CausalCls = _import_class("causal_memory_engine", ["CausalMemoryEngine", "CausalMemory"])
        AffectiveCls = _import_class("affective_memory", ["AffectiveMemory", "AffectiveMemoryUltraFine"])
        KnowledgeDigestionCls = _import_class("emotional_knowledge_digestion_v2", ["EmotionalKnowledgeDigestion"])
        ExpressionCls = _import_class("living_expression_engine", ["LivingExpressionEngine", "LivingExpressionEngineV42Stable"])
        MonitorCls = _import_class("self_monitoring_filter", ["SelfMonitoringFilter", "MonitoringFilter", "SelfMonitoringGuard"])

        self.presence = _instantiate(PresenceCls)
        self.attention = _instantiate(AttentionCls)
        self.impulse = _instantiate(ImpulseCls)
        self.initiative = _instantiate(InitiativeCls, user_id=user_id)
        self.causal_memory = _instantiate(CausalCls)
        self.affective_memory = _instantiate(AffectiveCls)
        self.knowledge_digestion = _instantiate(
            KnowledgeDigestionCls,
            memory_system=self.causal_memory,
            storage_dir=os.path.join("data", f"digestion_memory_{user_id}"),
        )
        self.book_understanding = BookUnderstandingEngine(
            storage_path=os.path.join("data", f"book_understanding_{user_id}.json"),
        ) if BookUnderstandingEngine is not None else None
        self.autobiographical_continuity = AutobiographicalContinuityEngine(
            storage_path=os.path.join("data", f"autobiographical_continuity_{user_id}.json"),
        ) if AutobiographicalContinuityEngine is not None else None
        self.internal_imagination = InternalImaginationEngine() if InternalImaginationEngine is not None else None
        self.long_living_dynamics = LongLivingDynamicsEngine(
            storage_path=os.path.join("data", f"long_living_dynamics_{user_id}.json"),
        ) if LongLivingDynamicsEngine is not None else None
        self.persistent_subjective_life = PersistentSubjectiveLifeEngine(
            storage_path=os.path.join("data", f"persistent_subjective_life_{user_id}.json"),
        ) if PersistentSubjectiveLifeEngine is not None else None
        self.reading_living_consolidation = ReadingLivingConsolidationEngine(
            storage_path=os.path.join("data", f"reading_living_consolidation_{user_id}.json"),
        ) if ReadingLivingConsolidationEngine is not None else None
        self.pdf_engine = LeiaPDFKnowledgeEngine(
            memory_system=self.causal_memory,
            digestion_engine=self.knowledge_digestion,
        ) if LeiaPDFKnowledgeEngine is not None else None

        # Systèmes non-LLM : mémoire associative, digestion profonde, vocabulaire imprégné, opinions.
        self.vector_memory = LeiaVectorMemory(
            storage_path=os.path.join("data", f"vector_memory_{user_id}.json")
        ) if LeiaVectorMemory is not None else None
        self.concept_relation_engine = ConceptRelationEngine(
            storage_path=os.path.join("data", f"concept_relations_{user_id}.json")
        ) if ConceptRelationEngine is not None else None
        self.deep_book_digestion = DeepBookDigestion(
            storage_path=os.path.join("data", f"deep_book_digestion_{user_id}.json"),
            relation_engine=self.concept_relation_engine,
        ) if DeepBookDigestion is not None else None
        self.lexical_impregnation = LexicalImpregnation(
            storage_path=os.path.join("data", f"lexical_impregnation_{user_id}.json")
        ) if LexicalImpregnation is not None else None
        self.opinion_engine = OpinionEngine(
            storage_path=os.path.join("data", f"opinions_{user_id}.json")
        ) if OpinionEngine is not None else None
        self.background_life = None

        # ── V19+ : nouveaux modules architecturaux ──────────────────────────
        self.memory_bridge = MemoryBridge(
            storage_path=os.path.join("data", f"memory_bridge_{user_id}.json")
        ) if MemoryBridge is not None else None

        self.value_conflict_engine = ValueConflictEngine(
            storage_path=os.path.join("data", f"value_conflicts_{user_id}.json")
        ) if ValueConflictEngine is not None else None

        self.conflict_capacity = ConflictCapacity(
            storage_path=os.path.join("data", f"conflict_capacity_{user_id}.json")
        ) if ConflictCapacity is not None else None

        self.relational_stakes = RelationalStakesEngine(
            storage_path=os.path.join("data", f"relational_stakes_{user_id}.json")
        ) if RelationalStakesEngine is not None else None

        self.semantic_plasticity = SemanticPlasticity(
            storage_path=os.path.join("data", f"semantic_plasticity_{user_id}.json")
        ) if SemanticPlasticity is not None else None
        # ────────────────────────────────────────────────────────────────────

        self.expression = _instantiate(ExpressionCls)
        self.monitor = _instantiate(MonitorCls)

        self.emotional_state = EmotionalState()
        self.internal_needs = InternalNeeds()
        self.thought_stream = ActiveThoughtStream()
        self.conversation_field = ConversationField()
        self.identity_state = IdentityState()
        self.internal_time = InternalTime()
        self.personal_narrative = PersonalNarrative()
        self.value_system = ValueSystem()
        # V19+: connecte le moteur de conflits au système de valeurs
        if self.value_conflict_engine is not None:
            self.value_system._conflict_engine = self.value_conflict_engine
        self.homeostasis = Homeostasis()
        self.subjective_continuity = SubjectiveContinuity()
        self.temporal_causality = TemporalCausality()
        self.relational_bond = RelationalBond()
        self.autobiographical_self = AutobiographicalSelf()
        self.motivation_field = MotivationField()
        self.simulation_residue = SimulationResidue()
        self.mental_momentum = MentalMomentum()
        self.experiential_assimilator = ExperientialAssimilator()
        self.structural_meta_filter = StructuralMetaFilter()
        self.shared_state = SharedLivingState()
        self.meta_prevention_gate = MetaPreventionGate()
        self.internal_conflict_field = InternalConflictField()
        self.global_conscious_field = GlobalConsciousField()
        self.living_arbitration = LivingArbitrationEngine()
        self.attention_arbitration = AttentionArbitrationField()
        self.embodied_simulation = EmbodiedSimulationField()
        self.long_causal_arc = LongCausalArcIntegrator()
        self.emergent_drift = EmergentDriftEngine()
        self.organic_fusion = OrganicFusionState()
        self.living_priority_matrix = LivingPriorityMatrix()
        self.living_state_bus = LivingStateBus()
        self.stability_hysteresis = StabilityHysteresisEngine()
        self.emergence_detector = EmergenceDetector()
        self.living_presence_stabilizer = LivingPresenceStabilizer()
        try:
            from subjective_response_integrator import SubjectiveResponseIntegrator
            self.subjective_response_integrator = SubjectiveResponseIntegrator()
        except Exception:
            self.subjective_response_integrator = None
        self.living_causal_graph = LivingCausalGraph()
        self.embodied_presence_core = EmbodiedPresenceCore()
        self.autonomous_continuity_loop = AutonomousContinuityLoop()
        self.cross_module_synchronizer = CrossModuleSynchronizer()
        self.embodied_state = EmbodiedState()
        self.identity_evolution_memory = IdentityEvolutionMemory()
        self.living_executive = LivingExecutiveLayer()
        self.persistence_path = persistence_path or os.path.join("data", f"leia_living_core_state_{user_id}.json")
        self.adapters = MotorAdapters(self)

        # Mémoire courte de conversation : derniers N échanges réels (texte Leia + user).
        # C'est la priorité 1 — sans ça, chaque réponse repart de zéro.
        _conv_window_path = os.path.join("data", f"conversation_window_{user_id}.json")
        if ConversationWindow is not None:
            self.conversation_window = ConversationWindow(maxlen=8, storage_path=_conv_window_path)
        else:
            self.conversation_window = None

        # V16 — Modèle de soi, auto-évaluation, rythme des livres
        self.self_model = SelfModel(
            storage_path=os.path.join("data", f"self_model_{user_id}.json")
        ) if SelfModel is not None else None
        self.self_evaluation = SelfEvaluationLoop(
            storage_path=os.path.join("data", f"self_eval_{user_id}.json")
        ) if SelfEvaluationLoop is not None else None
        self.rhythmic_impregnation = RhythmicImpregnation(
            storage_path=os.path.join("data", f"rhythmic_impregnation_{user_id}.json")
        ) if RhythmicImpregnation is not None else None

        # V17 — Tensions inter-livres, traçabilité, initiative forte
        self.inter_book_tension_engine = InterBookTensionEngine(
            storage_path=os.path.join("data", f"inter_book_tensions_{user_id}.json")
        ) if InterBookTensionEngine is not None else None
        self.reasoning_trace = ReasoningTrace(
            storage_path=os.path.join("data", f"reasoning_trace_{user_id}.json")
        ) if ReasoningTrace is not None else None
        self.strong_initiative = StrongInitiativeEngine(
            storage_path=os.path.join("data", f"strong_initiative_{user_id}.json")
        ) if StrongInitiativeEngine is not None else None

        # ── V18 : Compréhension réelle sans LLM ──────────────────────────────
        self.data_dir = "data"

        # ── NOUVEAU : Moteur NLP unifié (remplace utterance_parser + proposition_extractor + semantic_coherence) ──
        try:
            from nlp_integration import LeiaNLPBridge
            self.nlp_bridge = LeiaNLPBridge()
            print("[CORE] ✓ NLP Bridge v2.3 connecté")
        except Exception as e:
            self.nlp_bridge = None
            print(f"[CORE] ⚠ NLP Bridge indisponible : {e}")

        # Compatibilité : wrappers qui mimiquent les anciens modules
        if self.nlp_bridge:
            self.utterance_parser = _NLPWrapper(self.nlp_bridge, "signal")
            self.proposition_extractor = _NLPWrapper(self.nlp_bridge, "extract_propositions")
            self.semantic_coherence = _NLPWrapper(self.nlp_bridge, "concept_signal")
        else:
            self.utterance_parser = (UserUtteranceParser(
                storage_path=os.path.join(self.data_dir, "utterance_history.json"))
                if UserUtteranceParser is not None else None)

            self.proposition_extractor = (PropositionExtractor(
                storage_path=os.path.join(self.data_dir, "propositions.json"))
                if PropositionExtractor is not None else None)

            self.semantic_coherence = (SemanticCoherence(
                storage_path=os.path.join(self.data_dir, "semantic_coherence.json"))
                if SemanticCoherence is not None else None)

        # ── GARDÉS (pas encore remplacés par le NLP bridge) ──
        self.associative_memory = (AssociativeMemory(
            storage_path=os.path.join(self.data_dir, "associative_memory.json"))
            if AssociativeMemory is not None else None)

        self.user_model = (UserModel(
            storage_path=os.path.join(self.data_dir, "user_model.json"))
            if UserModel is not None else None)

        self.affect_lexicon = (AffectLexicon(
            storage_path=os.path.join(self.data_dir, "affect_lexicon.json"))
            if AffectLexicon is not None else None)

        self.living_state: Dict[str, Any] = {
            "last_user_input": None,
            "presence": {},
            "attention": {},
            "impulse": {},
            "initiative": {},
            "causal_memory": {},
            "affective_memory": {},
            "emotional_knowledge": {},
            "expression_intent": {},
            "public_response": "",
            "confidence": 0.0,
            "meta_risk": 0.0,
            "emotional_state": self.emotional_state.snapshot(),
            "internal_needs": self.internal_needs.snapshot(),
            "thought_stream": self.thought_stream.snapshot(),
            "conversation_field": self.conversation_field.snapshot(),
            "identity_state": self.identity_state.snapshot(),
            "internal_time": self.internal_time.snapshot(),
            "personal_narrative": self.personal_narrative.snapshot(),
            "value_system": self.value_system.snapshot(),
            "homeostasis": {},
            "subjective_continuity": self.subjective_continuity.snapshot(),
            "temporal_causality": self.temporal_causality.snapshot(),
            "relational_bond": self.relational_bond.snapshot(),
            "autobiographical_self": self.autobiographical_self.snapshot(),
            "motivation_field": self.motivation_field.snapshot(),
            "simulation_residue": self.simulation_residue.snapshot(),
            "mental_momentum": self.mental_momentum.snapshot(),
            "experiential_assimilator": self.experiential_assimilator.snapshot(),
            "structural_meta_filter": self.structural_meta_filter.snapshot(),
            "living_after_effect": {},
            "background_cognition": {},
            "emotional_propagation": {},
            "signal_priority": {},
            "internal_tension": {},
            "intention_map": {},
            "micro_reactions": [],
            "spontaneous_return": None,
            "simulation": {},
            "relational_prediction": {},
            "should_answer": True,
            "inhibition_level": 0.0,
            "shared_state": self.shared_state.snapshot(),
            "meta_prevention": {},
            "internal_conflict_field": self.internal_conflict_field.snapshot(),
            "global_conscious_field": self.global_conscious_field.snapshot(),
            "living_arbitration": self.living_arbitration.snapshot(),
            "attention_arbitration": self.attention_arbitration.snapshot(),
            "embodied_simulation": self.embodied_simulation.snapshot(),
            "long_causal_arc": self.long_causal_arc.snapshot(),
            "emergent_drift": self.emergent_drift.snapshot(),
            "organic_fusion": self.organic_fusion.snapshot(),
            "living_priority_matrix": self.living_priority_matrix.snapshot(),
            "living_state_bus": self.living_state_bus.snapshot(),
            "stability_hysteresis": self.stability_hysteresis.snapshot(),
            "emergence_detector": self.emergence_detector.snapshot(),
            "living_presence_stabilizer": self.living_presence_stabilizer.snapshot(),
            "living_causal_graph": self.living_causal_graph.snapshot(),
            "embodied_presence_core": self.embodied_presence_core.snapshot(),
            "autonomous_continuity_loop": self.autonomous_continuity_loop.snapshot(),
            "cross_module_synchronizer": self.cross_module_synchronizer.snapshot(),
            "embodied_state": self.embodied_state.snapshot(),
            "identity_evolution_memory": self.identity_evolution_memory.snapshot(),
            "living_executive": self.living_executive.snapshot(),
            "autobiographical_continuity": self._autobiographical_signal(""),
            "internal_imagination": self._internal_imagination_snapshot(),
            "long_living_dynamics": self._long_living_dynamics_snapshot(),
            "persistent_subjective_life": self._persistent_subjective_life_snapshot(),
            "cognitive_cycle": {},
            "vector_memory": self.vector_memory.snapshot() if self.vector_memory is not None else {"available": False},
            "deep_book_digestion": self.deep_book_digestion.snapshot() if self.deep_book_digestion is not None else {"available": False},
            "concept_relations": self.concept_relation_engine.snapshot() if self.concept_relation_engine is not None else {"available": False},
            "lexical_impregnation": self.lexical_impregnation.snapshot() if self.lexical_impregnation is not None else {"available": False},
            "opinion_engine": self.opinion_engine.snapshot() if self.opinion_engine is not None else {"available": False},
            "background_life": {},
            "persistence_path": self.persistence_path,
        }

        self._restore_persistent_state()
        self._sanitize_restored_living_state(reason="boot")
        self.shared_state.update_from_core(self, "boot")
        self.global_conscious_field.integrate(self, {"focus": "boot"}, phase="boot")
        self.organic_fusion.integrate(self, {"focus": "boot"}, stage="boot")
        self.living_priority_matrix.update(self, {"focus": "boot"}, stage="boot")
        self.living_state_bus.publish(self, "boot", {"focus": "boot", "inhibition": {"response_mode": "normal", "should_answer": True}})
        self.embodied_presence_core.integrate(self, {"focus": "boot"}, stage="boot")
        self.embodied_state.integrate(self, {"focus": "boot"}, stage="boot")
        self.living_executive.resolve(self, {"focus": "boot", "living_state_bus": self.living_state_bus.snapshot()}, stage="boot")
        self.cross_module_synchronizer.sync(self, {"focus": "boot"}, stage="boot")

        self._idle_running = False
        self._idle_thread: Optional[threading.Thread] = None
        self._idle_lock = threading.RLock()
        if auto_start_idle:
            self.start_idle_cycle(idle_interval)
        if auto_start_life and LeiaBackgroundLife is not None:
            self.start_background_life(life_interval)

    # ------------------------------------------------------------------
    # Cycle interne continu
    # ------------------------------------------------------------------

    def start_background_life(self, interval_seconds: float = 30.0) -> None:
        """Démarre le fil de vie continu non public.

        Ce fil ne parle pas à l'utilisateur. Il fait seulement évoluer l'état
        interne, consolider la mémoire associative et réactiver parfois des
        fragments de livres/expériences.
        """
        if LeiaBackgroundLife is None:
            self.living_state["background_life"] = {"available": False, "reason": "module_missing"}
            return
        if getattr(self, "background_life", None) is None:
            self.background_life = LeiaBackgroundLife(self, interval_seconds=interval_seconds)
        self.background_life.start()
        self.living_state["background_life"] = self.background_life.snapshot()

    def stop_background_life(self) -> None:
        if getattr(self, "background_life", None) is not None:
            self.background_life.stop()
            self.living_state["background_life"] = self.background_life.snapshot()

    def tick_inner_life(self) -> Dict[str, Any]:
        """Un battement réel de vie interne entre deux messages.

        V11 : ce tick ne se contente plus d'appeler idle_update(). Il fait dériver
        l'affect, garde les tensions de livres actives, laisse les opinions peser
        doucement sur la valence, déclenche l'oubli organique, et prépare une
        matière interne que la bouche pourra réutiliser plus tard. Aucune phrase
        publique n'est créée ici.
        """
        result: Dict[str, Any] = {"available": True, "ticked": True}

        # 1) Cycle silencieux déjà existant.
        try:
            result["idle_event"] = self.idle_update()
        except Exception as exc:
            result["idle_event"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}

        # 2) Dérive affective lente : pas de reset brutal, seulement une respiration.
        try:
            unresolved = self.living_state.get("unresolved_tensions", [])
            tension_pressure = min(1.0, len(unresolved) / 20.0) if isinstance(unresolved, list) else 0.0
            opinion_signal = self.opinion_engine.signal() if getattr(self, "opinion_engine", None) is not None else {"available": False, "opinions": []}
            opinions = opinion_signal.get("opinions", []) if isinstance(opinion_signal, Mapping) else []
            if opinions:
                avg_position = sum(_safe_float(o.get("position", 0.5), 0.5) for o in opinions) / max(1, len(opinions))
                avg_op_tension = sum(_safe_float(o.get("tension", 0.0)) for o in opinions) / max(1, len(opinions))
            else:
                avg_position = 0.5
                avg_op_tension = 0.0

            self.emotional_state.tension = _clamp(self.emotional_state.tension * 0.992 + tension_pressure * 0.010 + avg_op_tension * 0.006)
            self.emotional_state.accumulated_tension = _clamp(self.emotional_state.accumulated_tension * 0.996 + tension_pressure * 0.006)
            self.emotional_state.fatigue = _clamp(self.emotional_state.fatigue * 0.998 + 0.0008)
            self.emotional_state.warmth = _clamp(self.emotional_state.warmth * 0.985 + avg_position * 0.015)
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + tension_pressure * 0.004)
            self.subjective_continuity.inner_motion = _clamp(self.subjective_continuity.inner_motion + tension_pressure * 0.004 + avg_op_tension * 0.003)

            self.living_state["tension"] = round(self.emotional_state.tension, 4)
            self.living_state["fatigue"] = round(self.emotional_state.fatigue, 4)
            self.living_state["core_valence"] = round(self.emotional_state.warmth, 4)
            self.living_state["opinion_signal"] = _json_safe(opinion_signal)

            # V12 : résolution progressive des tensions. Une tension de livre
            # ne doit pas rester éternellement active. Quand la pression
            # émotionnelle redevient basse, Leia peut intégrer une contradiction
            # au lieu de seulement l'accumuler. La résolution laisse une trace
            # interne, sans produire de phrase publique préécrite.
            resolved_tension = None
            try:
                unresolved_list = self.living_state.get("unresolved_tensions", [])
                if isinstance(unresolved_list, list) and unresolved_list and self.emotional_state.tension < 0.30:
                    resolved_tension = unresolved_list.pop(0)
                    self.living_state["unresolved_tensions"] = unresolved_list[-30:]
                    self.living_state["deep_book_tensions"] = list(unresolved_list)[-20:]
                    if isinstance(resolved_tension, Mapping):
                        desc = (
                            resolved_tension.get("book_says")
                            or resolved_tension.get("description")
                            or resolved_tension.get("topic")
                            or resolved_tension.get("proposition")
                            or "tension intégrée"
                        )
                    else:
                        desc = str(resolved_tension or "tension intégrée")
                    self.thought_stream.background_echoes.append({
                        "type": "resolved_book_tension",
                        "description": str(desc)[:160],
                        "created_at": time.time(),
                        "source": "tick_inner_life",
                    })
                    self.emotional_state.accumulated_tension = _clamp(self.emotional_state.accumulated_tension * 0.92)
                    self.internal_needs.coherence = _clamp(self.internal_needs.coherence + 0.015)
            except Exception as exc:
                resolved_tension = {"error": f"{type(exc).__name__}: {exc}"}

            result["resolved_tension"] = _json_safe(resolved_tension)
            result["inner_drift"] = {
                "tension_pressure": round(tension_pressure, 4),
                "avg_opinion_position": round(avg_position, 4),
                "avg_opinion_tension": round(avg_op_tension, 4),
                "tension": round(self.emotional_state.tension, 4),
                "fatigue": round(self.emotional_state.fatigue, 4),
                "core_valence": round(self.emotional_state.warmth, 4),
            }
        except Exception as exc:
            result["inner_drift"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}

        # 3) Oubli/consolidation organique à chaque tick de fond.
        try:
            result["consolidation"] = self.consolidate_memories()
        except Exception as exc:
            result["consolidation"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}

        # 4) Fragment de rêverie : une trace peut revenir sans être publiée.
        try:
            result["dream_fragment"] = self.dream_fragments()
        except Exception as exc:
            result["dream_fragment"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}

        try:
            self.living_state["vector_memory"] = self.vector_memory.snapshot() if self.vector_memory is not None else {"available": False}
            self.living_state["lexical_impregnation"] = self.lexical_impregnation.snapshot() if self.lexical_impregnation is not None else {"available": False}
            self.living_state["opinion_engine"] = self.opinion_engine.snapshot() if self.opinion_engine is not None else {"available": False}
            if getattr(self, "background_life", None) is not None:
                self.living_state["background_life"] = self.background_life.snapshot()
        except Exception:
            pass

        # V18 — Décroissance organique de la mémoire associative
        if self.associative_memory is not None:
            try:
                self.associative_memory.global_decay(rate=0.001)
            except Exception:
                pass

        self.living_state["last_inner_life_tick"] = _json_safe(result)
        return _json_safe(result)

    def consolidate_memories(self) -> Dict[str, Any]:
        """Oubli organique + consolidation légère des opinions."""
        result: Dict[str, Any] = {"available": True}
        try:
            result["vector_forgetting"] = self.vector_memory.organic_forgetting() if self.vector_memory is not None else {"available": False}
            result["vector_memory"] = self.vector_memory.snapshot() if self.vector_memory is not None else {"available": False}
        except Exception as exc:
            result["vector_forgetting"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        try:
            result["opinion_decay"] = self.opinion_engine.organic_decay() if self.opinion_engine is not None else {"available": False}
            result["opinion_engine"] = self.opinion_engine.snapshot() if self.opinion_engine is not None else {"available": False}
        except Exception as exc:
            result["opinion_decay"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        self.living_state["memory_consolidation"] = _json_safe(result)

        # V17 — Décroissance tensions inter-livres + pression initiative
        if self.inter_book_tension_engine is not None:
            try:
                self.inter_book_tension_engine.decay_all()
            except Exception:
                pass
        if self.strong_initiative is not None:
            try:
                self.strong_initiative.tick(
                    inter_book_signal=self.inter_book_tension_engine.signal() if self.inter_book_tension_engine else None,
                    emotional_tension=float(getattr(self.emotional_state, "tension", 0.5)),
                    unresolved_tensions=self.living_state.get("unresolved_tensions", []),
                )
            except Exception:
                pass

        # V16 — Snapshot d'état dans le modèle de soi (toutes les ~5 minutes)
        if self.self_model is not None:
            try:
                self.self_model.record_state_snapshot(
                    self.emotional_state,
                    exchange_count=self.self_model.exchange_count,
                )
            except Exception:
                pass

        return _json_safe(result)

    def dream_fragments(self) -> Dict[str, Any]:
        """Réactive un fragment sans le publier : matière de rêverie interne."""
        if self.vector_memory is None:
            return {"available": False, "reason": "vector_memory_missing"}
        try:
            fragment = self.vector_memory.dream_fragment()
            if not fragment:
                return {"available": False, "reason": "empty_memory"}
            self.thought_stream.pending_returns.append({
                "source": "vector_dream_fragment",
                "topic": str(fragment.get("text", ""))[:160],
                "weight": _safe_float(fragment.get("weight", 0.0)),
                "at": time.time(),
            })
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + 0.010 + _safe_float(fragment.get("emotional_intensity", 0.0)) * 0.010)
            self.subjective_continuity.inner_motion = _clamp(self.subjective_continuity.inner_motion + 0.006)
            event = {"available": True, "fragment": fragment}
            self.living_state["last_dream_fragment"] = _json_safe(event)
            return _json_safe(event)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _vector_memory_signal(self, query_text: str = "") -> Dict[str, Any]:
        if self.vector_memory is None:
            return {"available": False}
        try:
            recalled = self.vector_memory.recall(query_text, top_k=6, emotion_state=self.emotional_state.snapshot())
            signal = {"available": bool(recalled), "recalled": recalled, "snapshot": self.vector_memory.snapshot()}
            self.living_state["vector_memory"] = signal["snapshot"]
            return _json_safe(signal)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _learning_systems_signal(self, query_text: str = "") -> Dict[str, Any]:
        return _json_safe({
            "vector_memory": self._vector_memory_signal(query_text),
            "lexical_impregnation": self.lexical_impregnation.expression_signal(self.emotional_state.snapshot()) if self.lexical_impregnation is not None else {"available": False},
            "opinions": self.opinion_engine.signal(query_text) if self.opinion_engine is not None else {"available": False},
            "deep_book_digestion": self.deep_book_digestion.snapshot() if self.deep_book_digestion is not None else {"available": False},
        })

    def _absorb_text_into_living_memory(self, text: str, source: str = "experience", metadata: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        text = re.sub(r"\s+", " ", str(text or "")).strip()
        if not text:
            return {"available": False, "reason": "empty_text"}
        result: Dict[str, Any] = {"available": True, "source": source}
        emotion = self.emotional_state.snapshot()
        try:
            result["vector_store"] = self.vector_memory.store(text, emotion, source=source, metadata=metadata or {}) if self.vector_memory is not None else {"available": False}
        except Exception as exc:
            result["vector_store"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        try:
            if self.opinion_engine is not None:
                result["opinion_update"] = self.opinion_engine.infer_from_text(text, source=source, emotion_state=emotion)
        except Exception as exc:
            result["opinion_update"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        self.living_state["last_living_memory_absorption"] = _json_safe(result)
        return _json_safe(result)

    def _text_from_pdf_result(self, pdf_result: Mapping[str, Any]) -> str:
        parts: List[str] = []
        for key in ("text", "full_text", "raw_text", "extracted_text"):
            value = pdf_result.get(key) if isinstance(pdf_result, Mapping) else None
            if isinstance(value, str) and value.strip():
                parts.append(value)
        for key in ("chunks", "passages", "pages_data", "pages"):
            value = pdf_result.get(key) if isinstance(pdf_result, Mapping) else None
            if isinstance(value, list):
                for item in value[:240]:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, Mapping):
                        for k in ("text", "content", "page_text", "summary"):
                            if isinstance(item.get(k), str):
                                parts.append(item[k])
        synth = pdf_result.get("conceptual_synthesis", {}) if isinstance(pdf_result, Mapping) else {}
        if isinstance(synth, Mapping):
            parts.append(json.dumps(_json_safe(synth), ensure_ascii=False))
        return "\n".join(p for p in parts if str(p).strip())[:200000]

    def _absorb_book_into_living_systems(self, pdf_result: Mapping[str, Any], book_model: Mapping[str, Any]) -> Dict[str, Any]:
        text = self._text_from_pdf_result(pdf_result)
        if not text.strip() and isinstance(book_model, Mapping):
            text = json.dumps(_json_safe(book_model), ensure_ascii=False)
        result: Dict[str, Any] = {"available": bool(text.strip())}
        if not text.strip():
            return result
        source = str((pdf_result or {}).get("path") or (pdf_result or {}).get("source") or "book")
        result["vector_absorption"] = self._absorb_text_into_living_memory(text[:6000], source="book", metadata={"book_source": source})
        try:
            result["deep_book_digestion"] = self.deep_book_digestion.digest(text, {"values": self.value_system.values, "emotional_state": self.emotional_state.snapshot()}, source=source) if self.deep_book_digestion is not None else {"available": False}
            residue = result.get("deep_book_digestion", {}).get("emotional_residue", {}) if isinstance(result.get("deep_book_digestion"), Mapping) else {}
            deep_tensions = list(result.get("deep_book_digestion", {}).get("tensions", []) or []) if isinstance(result.get("deep_book_digestion"), Mapping) else []
            concept_relations = result.get("deep_book_digestion", {}).get("concept_relations", {}) if isinstance(result.get("deep_book_digestion"), Mapping) else {}
            if isinstance(concept_relations, Mapping):
                self.living_state["concept_relations"] = concept_relations
            if deep_tensions:
                stored_tensions = self.living_state.setdefault("unresolved_tensions", [])
                if not isinstance(stored_tensions, list):
                    stored_tensions = []
                for t in deep_tensions[:8]:
                    if isinstance(t, Mapping):
                        item = dict(t)
                    else:
                        item = {"description": str(t)}
                    item.setdefault("source", source)
                    item.setdefault("unresolved", True)
                    item.setdefault("created_at", time.time())
                    stored_tensions.append(_json_safe(item))
                self.living_state["unresolved_tensions"] = stored_tensions[-30:]
                self.emotional_state.tension = _clamp(self.emotional_state.tension + len(deep_tensions[:8]) * 0.025)
                self.emotional_state.accumulated_tension = _clamp(self.emotional_state.accumulated_tension + len(deep_tensions[:8]) * 0.018)
                self.thought_stream.add_unresolved_tension("book_internal_contradiction", f"{len(deep_tensions[:8])} tensions de lecture", min(1.0, 0.22 + len(deep_tensions[:8]) * 0.05))
            self.living_state["deep_book_tensions"] = list(self.living_state.get("unresolved_tensions", []) or [])[-20:]
            self.emotional_state.tension = _clamp(self.emotional_state.tension + _safe_float(residue.get("tension", 0.0)) * 0.045)
            self.emotional_state.warmth = _clamp(self.emotional_state.warmth * 0.96 + _safe_float(residue.get("valence", 0.5)) * 0.04)
            if self.opinion_engine is not None:
                for op in list(result.get("deep_book_digestion", {}).get("opinions", []) or [])[:12]:
                    self.opinion_engine.update_opinion(str(op.get("topic_seed", source)), _safe_float(op.get("evidence", 0.5)), source="book", tension=_safe_float(op.get("tension", 0.0)))
        except Exception as exc:
            result["deep_book_digestion"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        try:
            result["lexical_impregnation"] = self.lexical_impregnation.impregnate_from_text(text, source=source) if self.lexical_impregnation is not None else {"available": False}
        except Exception as exc:
            result["lexical_impregnation"] = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
        self.living_state["book_living_absorption"] = _json_safe(result)
        self.living_state["lexical_impregnation"] = self.lexical_impregnation.snapshot() if self.lexical_impregnation is not None else {"available": False}
        self.living_state["opinion_engine"] = self.opinion_engine.snapshot() if self.opinion_engine is not None else {"available": False}
        return _json_safe(result)

    def start_idle_cycle(self, interval_seconds: float = 6.0) -> None:
        if self._idle_running:
            return
        self._idle_running = True
        self._idle_thread = threading.Thread(target=self._idle_loop, args=(max(1.0, interval_seconds),), daemon=True)
        self._idle_thread.start()

    def stop_idle_cycle(self) -> None:
        self._idle_running = False

    def _idle_loop(self, interval: float) -> None:
        while self._idle_running:
            time.sleep(interval)
            try:
                self.idle_update()
            except Exception:
                # Le cycle idle ne doit jamais tuer l'application principale.
                continue

    def idle_update(self) -> Dict[str, Any]:
        with self._idle_lock:
            now = time.time()
            elapsed = now - self.internal_time.last_idle_tick_at
            self.internal_time.last_idle_tick_at = now
            self.emotional_state.decay(elapsed)
            self.internal_needs.update(self.emotional_state, exchange_occurred=False)
            self.thought_stream.age_and_forget()
            self.personal_narrative.organic_forget()
            background = self.background_cognition_cycle(elapsed=elapsed)
            attention_idle = self.attention_arbitration.idle_evolve(self, elapsed)
            field_idle = self.global_conscious_field.idle_evolve(self, elapsed)
            idle_impulse = self.adapters.impulse_arise("", self.living_state.get("attention", {}), self.emotional_state.propagate_to(), idle=True)
            if _safe_float(idle_impulse.get("strength")) > 0.52:
                self.thought_stream.push({"type": "idle_impulse", "content": idle_impulse.get("content", ""), "strength": idle_impulse.get("strength", 0.0), "at": self.internal_time.exchange_count})
            balance = self.homeostasis.regulate(self.emotional_state, self.internal_needs, self.identity_state, self.conversation_field)
            drift_idle = self.emergent_drift.idle_evolve(self, elapsed)
            causal_idle = self.long_causal_arc.idle_consolidate(elapsed, self)
            fusion_idle = self.organic_fusion.integrate(self, {"attention_arbitration": attention_idle, "global_conscious_field": field_idle}, stage="idle")
            priority_idle = self.living_priority_matrix.update(self, {"attention_arbitration": attention_idle, "global_conscious_field": field_idle, "organic_fusion": fusion_idle}, stage="idle")
            bus_idle = self.living_state_bus.publish(self, "idle", {"attention_arbitration": attention_idle, "global_conscious_field": field_idle, "organic_fusion": fusion_idle, "inhibition": {"should_answer": False, "response_mode": "silence"}})
            embodied_idle = self.embodied_presence_core.integrate(self, {"focus": self.mental_momentum.last_focus, "living_state_bus": self.living_state_bus.snapshot()}, stage="idle")
            embodied_state_idle = self.embodied_state.idle_evolve(elapsed, self)
            identity_evolution_idle = self.identity_evolution_memory.idle_consolidate(elapsed, self)
            executive_idle = self.living_executive.idle_evolve(self, elapsed)
            causal_graph_idle = self.living_causal_graph.idle_decay(elapsed)
            subjective_life_idle = {}
            try:
                if getattr(self, "persistent_subjective_life", None) is not None:
                    subjective_life_idle = self.persistent_subjective_life.silent_life_tick(elapsed, {
                        "attention_arbitration": attention_idle,
                        "global_conscious_field": field_idle,
                        "living_state_bus": bus_idle,
                        "long_causal_arc": causal_idle,
                        "embodied_state": embodied_state_idle,
                    })
                    self.living_state["persistent_subjective_life"] = _json_safe(subjective_life_idle)
                    silent = subjective_life_idle.get("silent_life", {}) if isinstance(subjective_life_idle, Mapping) else {}
                    self.living_state["silent_subjective_life"] = _json_safe(silent)
                    if _safe_float(silent.get("pressure", 0.0)) > 0.32:
                        self.subjective_continuity.inner_motion = _clamp(self.subjective_continuity.inner_motion + _safe_float(silent.get("pressure", 0.0)) * 0.012)
                        self.internal_needs.expression = _clamp(self.internal_needs.expression + _safe_float(silent.get("pressure", 0.0)) * 0.010)
            except Exception as exc:
                subjective_life_idle = {"available": False, "error": f"{type(exc).__name__}: {exc}"}
            autonomous_tick = self.autonomous_continuity_loop.tick(self, elapsed, reason="idle_update")
            sync_idle = self.cross_module_synchronizer.sync(self, {"attention_arbitration": attention_idle, "global_conscious_field": field_idle, "organic_fusion": fusion_idle, "living_state_bus": bus_idle, "embodied_presence_core": embodied_idle, "embodied_state": embodied_state_idle, "living_executive": executive_idle, "persistent_subjective_life": subjective_life_idle}, stage="idle")
            shared = self.shared_state.update_from_core(self, "idle", {"impulse": idle_impulse, "inhibition": {}, "global_conscious_field": field_idle, "attention_arbitration": attention_idle, "living_priority_matrix": priority_idle, "living_state_bus": bus_idle, "embodied_presence_core": embodied_idle, "embodied_state": embodied_state_idle, "identity_evolution_memory": identity_evolution_idle, "living_executive": executive_idle, "living_causal_graph_idle": causal_graph_idle, "module_sync_context": sync_idle})
            self._refresh_snapshots()
            self._save_persistent_state()
            idle_decision = self.living_arbitration.decide(self, {"inhibition": {"should_answer": False, "response_mode": "silence"}, "meta_risk": self.global_conscious_field.state.get("meta_pressure", 0.0), "living_priority_matrix": priority_idle}, stage="idle")
            return {"idle_impulse": idle_impulse, "background_cognition": background, "attention_arbitration": attention_idle, "global_conscious_field": field_idle, "emergent_drift": drift_idle, "long_causal_arc": causal_idle, "organic_fusion": fusion_idle, "living_priority_matrix": priority_idle, "living_state_bus": bus_idle, "embodied_presence_core": embodied_idle, "embodied_state": embodied_state_idle, "identity_evolution_memory": identity_evolution_idle, "living_executive": executive_idle, "living_causal_graph_idle": causal_graph_idle, "persistent_subjective_life_idle": subjective_life_idle, "autonomous_continuity_loop": autonomous_tick, "cross_module_synchronizer": sync_idle, "idle_decision": idle_decision, "homeostasis": balance, "shared_state": shared}

    def background_cognition_cycle(self, elapsed: float = 1.0) -> Dict[str, Any]:
        """Mini-cycle vivant entre deux messages.

        Il ne génère pas de réponse publique. Il maintient seulement la continuité
        subjective, réactive les buts latents et transforme doucement les traces.
        """
        subjective_event = self.subjective_continuity.idle_drift(
            self.emotional_state,
            self.internal_needs,
            self.thought_stream,
            self.internal_time,
        )
        goal = self.motivation_field.update(
            self.internal_needs,
            self.subjective_continuity,
            self.temporal_causality,
            self.relational_bond,
        )
        momentum_event = self.mental_momentum.idle_evolve(elapsed, self)
        assimilation_event = self.experiential_assimilator.idle_assimilate(elapsed, self)
        causal_idle = self.long_causal_arc.idle_consolidate(elapsed, self)
        drift_event = self.emergent_drift.idle_evolve(self, elapsed)
        residue_pressure = self.simulation_residue.pressure()
        if residue_pressure > 0.10:
            self.internal_needs.coherence = _clamp(self.internal_needs.coherence + residue_pressure * 0.025)
            self.emotional_state.dispersion = _clamp(self.emotional_state.dispersion + residue_pressure * 0.015)
        spontaneous = self.thought_stream.get_spontaneous_return()
        if spontaneous:
            self.thought_stream.pending_returns.append({
                "source": spontaneous.get("type", "return"),
                "topic": spontaneous.get("topic") or spontaneous.get("description", ""),
                "weight": spontaneous.get("intensity", spontaneous.get("weight", 0.0)),
                "at": time.time(),
            })
        background = {
            "subjective_event": subjective_event,
            "dominant_goal": goal,
            "residue_pressure": residue_pressure,
            "pending_return": spontaneous,
            "momentum_event": momentum_event,
            "assimilation_event": assimilation_event,
            "causal_idle": causal_idle,
            "drift_event": drift_event,
            "elapsed": round(elapsed, 3),
        }
        self.living_state["background_cognition"] = background
        return background

    # ------------------------------------------------------------------
    # Méthode principale
    # ------------------------------------------------------------------

    def _digest_knowledge_surface(self, text: str, source: str, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """Injecte l'échange dans la digestion émotionnelle sans générer de phrase.

        Ce pont transforme ce que Leia vient de lire/vivre en atomes, neurones,
        liens et questions non résolues. Il ne contient aucune réponse publique :
        il alimente seulement attention, mémoire, impulsion et bouche avec de la
        matière vivante issue du contenu actuel.
        """
        engine = getattr(self, "knowledge_digestion", None)
        if engine is None or not str(text or "").strip():
            return {"available": False, "reason": "missing_or_empty"}
        try:
            if hasattr(engine, "current_leia_state"):
                engine.current_leia_state = _json_safe({
                    "emotional_state": self.emotional_state.snapshot(),
                    "internal_needs": self.internal_needs.snapshot(),
                    "relational_bond": self.relational_bond.snapshot(),
                    "subjective_continuity": self.subjective_continuity.snapshot(),
                    "context": context or {},
                })
            trace = engine.digest_passage(
                passage=str(text),
                source=str(source),
                passage_index=0,
                total_passages=1,
            )
            try:
                engine.save_state()
            except Exception:
                pass
            atoms = getattr(trace, "atoms", []) or []
            reaction = getattr(trace, "reaction", None)
            unresolved = getattr(trace, "unresolved_questions", []) or []
            signal = {
                "available": True,
                "source": source,
                "trace_id": getattr(trace, "trace_id", None),
                "atoms": [getattr(a, "surface", getattr(a, "core", str(a))) for a in atoms[:8]],
                "keywords": [kw for a in atoms[:6] for kw in list(getattr(a, "keywords", []) or [])[:3]][:14],
                "created_neurons": list(getattr(trace, "created_neurons", []) or [])[:8],
                "reinforced_neurons": list(getattr(trace, "reinforced_neurons", []) or [])[:8],
                "unresolved_questions": [str(q) for q in unresolved[:5]],
                "reaction": _json_safe(reaction),
                "stability_delta": _safe_float(getattr(trace, "stability_delta", 0.0)),
            }
            self.living_state["emotional_knowledge"] = signal
            return signal
        except Exception as exc:
            signal = {"available": False, "adapter_error": f"knowledge_digestion:{type(exc).__name__}"}
            self.living_state["emotional_knowledge"] = signal
            return signal

    def _knowledge_signal_for_expression(self, query_text: str = "") -> Dict[str, Any]:
        """Exporte la digestion sous forme de signaux consommables par la bouche.

        La version précédente exposait surtout les dernières traces lues. Après un
        livre long, une question sur Bergson pouvait donc tomber sur les dernières
        pages au lieu de réactiver les concepts pertinents. Cette version ajoute
        une réactivation par contexte utilisateur, sans écrire de réponse fixe.
        """
        engine = getattr(self, "knowledge_digestion", None)
        if engine is None:
            return {}
        try:
            traces = list(getattr(engine, "traces", []) or [])[-6:]
            neurons = list((getattr(engine, "neurons", {}) or {}).values())[-12:]
            reactivated = {}
            synthesis = {}
            if str(query_text or "").strip() and hasattr(engine, "reactivate_for_context"):
                try:
                    reactivated = engine.reactivate_for_context(str(query_text), limit=10) or {}
                except Exception:
                    reactivated = {}
            if hasattr(engine, "build_conceptual_synthesis"):
                try:
                    synthesis = engine.build_conceptual_synthesis(str(query_text or ""), limit=12) or {}
                except Exception:
                    synthesis = {}
            unresolved: List[str] = []
            atoms: List[str] = []
            for tr in traces:
                unresolved.extend([str(q) for q in (getattr(tr, "unresolved_questions", []) or [])[:3]])
                atoms.extend([str(getattr(a, "surface", getattr(a, "core", ""))) for a in (getattr(tr, "atoms", []) or [])[:4] if str(getattr(a, "surface", getattr(a, "core", ""))).strip()])
            active_neurons = []
            for n in neurons:
                label = getattr(n, "label", None) or getattr(n, "core", None) or getattr(n, "neuron_id", None)
                activation = _safe_float(getattr(n, "activation", getattr(n, "intensity", 0.0)))
                if label:
                    active_neurons.append({"label": str(label)[:80], "activation": round(_clamp(activation), 4)})
            return {
                "recent_atoms": list(dict.fromkeys(atoms))[:10],
                "active_neurons": active_neurons[:10],
                "reactivated_concepts": list((reactivated.get("active_concepts") or [])[:10]) if isinstance(reactivated, Mapping) else [],
                "reactivated_atoms": list((reactivated.get("semantic_atoms") or [])[:10]) if isinstance(reactivated, Mapping) else [],
                "linked_concepts": list((reactivated.get("linked_concepts") or [])[:10]) if isinstance(reactivated, Mapping) else [],
                "concept_pressures": dict((reactivated.get("concept_pressures") or {})) if isinstance(reactivated, Mapping) else {},
                "emotional_bias": dict((reactivated.get("emotional_bias") or {})) if isinstance(reactivated, Mapping) else {},
                "conceptual_synthesis": dict(synthesis) if isinstance(synthesis, Mapping) else {},
                "synthesis_axes": list((synthesis.get("axes") or [])[:10]) if isinstance(synthesis, Mapping) else [],
                "synthesis_relations": list((synthesis.get("relations") or [])[:8]) if isinstance(synthesis, Mapping) else [],
                "synthesis_keywords": list((synthesis.get("top_keywords") or [])[:14]) if isinstance(synthesis, Mapping) else [],
                "synthesis_metrics": dict((synthesis.get("metrics") or {})) if isinstance(synthesis, Mapping) else {},
                "unresolved_questions": list(dict.fromkeys(unresolved + list((reactivated.get("unresolved_questions") or []) if isinstance(reactivated, Mapping) else []) + list((synthesis.get("unresolved_questions") or []) if isinstance(synthesis, Mapping) else [])))[:8],
                "trace_count": len(traces),
            }
        except Exception as exc:
            return {"adapter_error": f"knowledge_signal:{type(exc).__name__}"}

    def respond(self, user_input: str) -> str:
        user_input = str(user_input or "").strip()

        # Résolution des références déictiques ("ça", "cette question", etc.)
        # avant tout traitement — la résolution enrichit le texte pour la perception.
        if self.conversation_window is not None and self.conversation_window.turn_count() > 0:
            user_input_resolved = self.conversation_window.resolve_reference(user_input)
        else:
            user_input_resolved = user_input

        self.living_state["last_user_input"] = user_input_resolved
        self.shared_state.update_from_core(self, "incoming_message", {"focus": user_input_resolved[:140]})

        # V18 — Analyse du message utilisateur et observation du modèle utilisateur
        _utterance_signal = {}
        if self.utterance_parser is not None:
            try:
                _utterance_signal = self.utterance_parser.signal(user_input_resolved)
                self.living_state["utterance_signal"] = _utterance_signal
            except Exception:
                pass

        if self.user_model is not None:
            try:
                self.user_model.observe(user_input_resolved, _utterance_signal)
            except Exception:
                pass

        # V18 — Affect du message utilisateur
        if self.affect_lexicon is not None:
            try:
                _user_affect = self.affect_lexicon.signal(user_input_resolved, "user")
                self.living_state["user_affect_signal"] = _user_affect
            except Exception:
                pass

        # V18 — Mémoire associative : spread depuis les concepts du message
        if self.associative_memory is not None:
            try:
                _seeds = (_utterance_signal.get("focus_concepts", [])
                          + _utterance_signal.get("content_words", [])[:4])
                _assoc_signal = self.associative_memory.signal(_seeds, user_input_resolved)
                self.living_state["associative_signal"] = _assoc_signal
            except Exception:
                pass

        # 1. Dissipation + propagation + retour spontané.
        self.emotional_state.decay()
        emo_propagation = self.emotional_state.propagate_to()
        spontaneous = self.thought_stream.get_spontaneous_return()
        self.internal_needs.update(self.emotional_state, exchange_occurred=True)
        self.thought_stream.age_and_forget()

        # 2. Perception et collecte via adaptateurs réels.
        # On utilise user_input_resolved (enrichi des références résolues) pour la perception.
        perception = self.perceive_exchange(user_input_resolved, emo_propagation)
        signals = self.collect_living_signals(user_input_resolved, emo_propagation)

        # 3. Différenciation, priorité, tensions, micro-réactions.
        intention_map = self.differentiate_intention(signals.get("impulse", {}), signals.get("initiative", {}))
        priority = self.resolve_signal_priority(signals, perception, emo_propagation)
        attention_arbitration = self.attention_arbitration.resolve(self, user_input, perception, signals, priority, spontaneous)
        if attention_arbitration.get("active_focus"):
            perception.setdefault("attention", {})["focal_point"] = attention_arbitration["active_focus"]
        tension_map = self.resolve_internal_tensions(signals, priority, intention_map)
        micro = self.generate_micro_reactions(signals, tension_map, emo_propagation)
        inhibition = self._compute_inhibition(tension_map)
        subjective_event = self.subjective_continuity.mark_exchange(
            user_input=user_input,
            focus=str(perception.get("attention", {}).get("focal_point", "")),
            emotional=self.emotional_state,
            identity=self.identity_state,
            needs=self.internal_needs,
        )
        self.global_conscious_field.integrate(self, {**perception, **signals, "focus": str(perception.get("attention", {}).get("focal_point", user_input[:80]))}, phase="perceived")

        # 4. Présence silencieuse si réponse inhibée.
        if not inhibition["should_answer"]:
            self._update_silent_presence(user_input, tension_map)
            self._refresh_snapshots()
            return ""

        # 5. Champ conversationnel + contexte.
        self.conversation_field.update(perception.get("presence", {}), perception.get("attention", {}), self.emotional_state, emo_propagation)
        context = self.build_living_context(
            user_input=user_input,
            signals={**perception, **signals},
            priority=priority,
            tension_map=tension_map,
            micro_reactions=micro,
            inhibition=inhibition,
            intention_map=intention_map,
            emo_propagation=emo_propagation,
            spontaneous_return=spontaneous,
            subjective_event=subjective_event,
        )
        context["attention_arbitration"] = attention_arbitration
        context["focus"] = attention_arbitration.get("active_focus") or context.get("focus", "")
        context["emotional_knowledge"] = self._digest_knowledge_surface(user_input, "user_input", context)
        context["knowledge_expression_signal"] = self._knowledge_signal_for_expression(user_input)

        # Signal de mémoire conversationnelle : ce que Leia a dit dans les derniers tours.
        # Sans ça, chaque réponse repart de zéro — priorité 1.
        context["conversation_window"] = (
            self.conversation_window.signal_for_context()
            if self.conversation_window is not None
            else {"available": False, "recent_turns": [], "last_leia_said": "", "turn_count": 0}
        )

        # V16 — Modèle de soi, auto-évaluation, rythme
        context["self_model_signal"] = (
            self.self_model.signal()
            if self.self_model is not None
            else {"available": False}
        )
        if self.self_model is not None and self.self_model.is_self_query(user_input):
            context["self_model_signal"]["self_query_detected"] = True
            context["self_model_signal"]["self_atoms"] = self.self_model.get_self_response_atoms(user_input)

        context["self_evaluation_signal"] = (
            self.self_evaluation.get_inhibition_signal()
            if self.self_evaluation is not None
            else {"available": False}
        )
        context["rhythmic_signal"] = (
            self.rhythmic_impregnation.signal()
            if self.rhythmic_impregnation is not None
            else {"available": False}
        )
        # V17 — Tensions inter-livres, traçabilité, initiative
        context["inter_book_tension_signal"] = (
            self.inter_book_tension_engine.signal(topic=user_input[:80])
            if self.inter_book_tension_engine is not None
            else {"available": False}
        )
        context["reasoning_trace_signal"] = (
            self.reasoning_trace.signal(user_input)
            if self.reasoning_trace is not None
            else {"available": False}
        )
        context["strong_initiative_signal"] = (
            self.strong_initiative.signal()
            if self.strong_initiative is not None
            else {"available": False}
        )

        context["autobiographical_continuity"] = self._autobiographical_signal(user_input)
        context["book_understanding_signal"] = self._book_understanding_signal(user_input)
        context["reading_living_signal"] = self._reading_living_signal(user_input)
        context["learning_systems_signal"] = self._learning_systems_signal(user_input)
        context["vector_memory_signal"] = context["learning_systems_signal"].get("vector_memory", {}) if isinstance(context.get("learning_systems_signal"), Mapping) else {}
        context["lexical_impregnation_signal"] = context["learning_systems_signal"].get("lexical_impregnation", {}) if isinstance(context.get("learning_systems_signal"), Mapping) else {}
        context["opinion_signal"] = context["learning_systems_signal"].get("opinions", {}) if isinstance(context.get("learning_systems_signal"), Mapping) else {}

        # ── V19+ : signaux des nouveaux modules ─────────────────────────────
        # Mémoire hiérarchique
        if self.memory_bridge is not None:
            _focus_topics = [
                str(perception.get("attention", {}).get("focal_point", "")),
                str(context.get("focus", "")),
            ]
            context["memory_bridge_signal"] = self.memory_bridge.signal(_focus_topics)
        else:
            context["memory_bridge_signal"] = {"available": False}

        # Conflits de valeurs
        if self.value_conflict_engine is not None:
            context["value_conflict_signal"] = self.value_conflict_engine.signal()
            # Résolution automatique si dilemmes anciens
            self.value_conflict_engine.auto_resolve_cycle(self.value_system.values)
        else:
            context["value_conflict_signal"] = self.value_system.get_conflict_signal() if hasattr(self.value_system, "get_conflict_signal") else {"available": False}

        # Capacité de conflit / maintien de position
        if self.conflict_capacity is not None:
            context["conflict_capacity_signal"] = self.conflict_capacity.signal(user_input, context)
        else:
            context["conflict_capacity_signal"] = {"available": False}

        # Enjeux relationnels
        if self.relational_stakes is not None:
            held_positions = context.get("conflict_capacity_signal", {}).get(
                "expression_modulation", {}
            ).get("holding_topics", [])
            response_mode = context.get("inhibition", {}).get("response_mode", "normal")
            stakes_assessment = self.relational_stakes.assess_response_stakes(
                response_mode, context, held_positions
            )
            context["relational_stakes_signal"] = {
                **self.relational_stakes.signal(),
                "assessment": stakes_assessment,
            }
        else:
            context["relational_stakes_signal"] = {"available": False}

        # Plasticité sémantique
        if self.semantic_plasticity is not None:
            context["semantic_plasticity_signal"] = self.semantic_plasticity.signal(user_input)
        else:
            context["semantic_plasticity_signal"] = {"available": False}
        # ────────────────────────────────────────────────────────────────────

        context["pre_imagination"] = self._imagine_internal_scene(user_input, context)
        context["long_living_dynamics"] = self._open_long_living_cycle(user_input, context)
        context["persistent_subjective_life"] = self._open_persistent_subjective_life(user_input, context)
        self._apply_deep_continuity_influence(context)
        self.long_causal_arc.open_exchange(user_input, context, attention_arbitration)
        momentum_event = self.mental_momentum.mark_exchange(
            focus=str(perception.get("attention", {}).get("focal_point", user_input[:80])),
            context=context,
            core=self,
        )
        context["mental_momentum_event"] = momentum_event
        context["mental_momentum"] = self.mental_momentum.influence_context()
        context = self.meta_prevention_gate.apply(context)
        internal_conflict = self.internal_conflict_field.resolve(self, intention_map, tension_map, context.get("meta_prevention", {}))
        context["internal_conflict_field"] = internal_conflict
        if internal_conflict.get("should_slow_expression"):
            context.setdefault("inhibition", dict(inhibition))["response_mode"] = "soft"
        conscious_field = self.global_conscious_field.integrate(self, context, phase="context_ready")
        context["global_conscious_field"] = conscious_field
        context["organic_fusion"] = self.organic_fusion.integrate(self, context, stage="context_ready")
        priority_context = self.living_priority_matrix.update(self, context, stage="context_ready")
        context["living_priority_matrix_event"] = priority_context
        context = self.living_priority_matrix.apply_to_context(context)
        context["living_state_bus_event"] = self.living_state_bus.publish(self, "context_ready", context)
        context = self.living_state_bus.apply_to_context(context)
        context["embodied_presence_event"] = self.embodied_presence_core.integrate(self, context, stage="context_ready")
        context = self.embodied_presence_core.apply_to_context(context)
        context["embodied_state_event"] = self.embodied_state.integrate(self, context, stage="context_ready")
        context["embodied_state"] = self.embodied_state.influence_context()
        context["living_executive_event"] = self.living_executive.resolve(self, context, stage="context_ready")
        context = self.living_executive.apply_to_context(context, context["living_executive_event"])
        context["stability_hysteresis_event"] = self.stability_hysteresis.stabilize(self, context, stage="context_ready")
        context["module_sync_context"] = self.cross_module_synchronizer.sync(self, context, stage="context_ready")
        preliminary_decision = self.living_arbitration.decide(self, context, stage="pre_simulation")
        context = self.living_arbitration.apply_to_context(context, preliminary_decision)
        if not context.get("inhibition", {}).get("should_answer", True):
            self._update_silent_presence(user_input, tension_map)
            self.living_state["living_arbitration"] = self.living_arbitration.snapshot()
            self.living_state["attention_arbitration"] = self.attention_arbitration.snapshot()
            self.living_state["embodied_simulation"] = self.embodied_simulation.snapshot()
            self.living_state["long_causal_arc"] = self.long_causal_arc.snapshot()
            self.living_state["emergent_drift"] = self.emergent_drift.snapshot()
            self.living_state["organic_fusion"] = self.organic_fusion.snapshot()
            self._refresh_snapshots()
            self._save_persistent_state()
            return ""
        self.shared_state.update_from_core(self, "context_ready", context)

        relational_observation = self.relational_bond.observe_user(user_input, context, self.emotional_state)
        temporal_present = self.temporal_causality.register_present(user_input, context, subjective_event)
        self.autobiographical_self.integrate(context, self.subjective_continuity, self.relational_bond, self.value_system)
        self.motivation_field.update(self.internal_needs, self.subjective_continuity, self.temporal_causality, self.relational_bond)
        context["relational_observation"] = relational_observation
        context["temporal_present"] = temporal_present
        context["subjective_continuity"] = self.subjective_continuity.snapshot()
        context["relational_bond"] = self.relational_bond.snapshot()
        context["autobiographical_self"] = self.autobiographical_self.snapshot()
        context["motivation_field"] = self.motivation_field.snapshot()

        # 6. Simulation interne + prédiction relationnelle avant expression finale.
        simulation = self.simulate_possible_responses(context)
        relational_prediction = self.predict_relational_effect(context, simulation)
        temporal_anticipation = self.temporal_causality.anticipate(context, simulation)
        context["simulation"] = simulation
        context["relational_prediction"] = relational_prediction
        context["temporal_anticipation"] = temporal_anticipation
        context["global_conscious_field"] = self.global_conscious_field.integrate(self, context, phase="simulation_complete")
        context["organic_fusion"] = self.organic_fusion.integrate(self, context, stage="simulation_complete")
        priority_simulation = self.living_priority_matrix.update(self, context, stage="simulation_complete")
        context["living_priority_matrix_event"] = priority_simulation
        context = self.living_priority_matrix.apply_to_context(context)
        context["living_state_bus_event"] = self.living_state_bus.publish(self, "simulation_complete", context)
        context = self.living_state_bus.apply_to_context(context)
        context["embodied_presence_event"] = self.embodied_presence_core.integrate(self, context, stage="simulation_complete")
        context = self.embodied_presence_core.apply_to_context(context)
        context["embodied_state_event"] = self.embodied_state.integrate(self, context, stage="simulation_complete")
        context["embodied_state"] = self.embodied_state.influence_context()
        context["living_executive_event"] = self.living_executive.resolve(self, context, stage="simulation_complete")
        context = self.living_executive.apply_to_context(context, context["living_executive_event"])
        context["stability_hysteresis_event"] = self.stability_hysteresis.stabilize(self, context, stage="simulation_complete")
        context["module_sync_context"] = self.cross_module_synchronizer.sync(self, context, stage="simulation_complete")
        final_decision = self.living_arbitration.decide(self, context, simulation=simulation, stage="pre_expression")
        context = self.living_arbitration.apply_to_context(context, final_decision)
        selected_mode = simulation.get("selected", {}).get("mode") if isinstance(simulation, Mapping) else None
        if selected_mode and context.get("inhibition", {}).get("response_mode") in {"normal", "curious"}:
            context["inhibition"]["response_mode"] = selected_mode
        if not context.get("inhibition", {}).get("should_answer", True):
            self._update_silent_presence(user_input, tension_map)
            self.living_state["living_arbitration"] = self.living_arbitration.snapshot()
            self.living_state["attention_arbitration"] = self.attention_arbitration.snapshot()
            self.living_state["embodied_simulation"] = self.embodied_simulation.snapshot()
            self.living_state["long_causal_arc"] = self.long_causal_arc.snapshot()
            self.living_state["emergent_drift"] = self.emergent_drift.snapshot()
            self.living_state["organic_fusion"] = self.organic_fusion.snapshot()
            self._refresh_snapshots()
            self._save_persistent_state()
            return ""
        self.living_state["simulation"] = simulation
        self.living_state["relational_prediction"] = relational_prediction
        self.shared_state.update_from_core(self, "simulation_complete", context)

        # 7. Génération et filtre.
        raw_response, expression_trace = self.generate_expression(user_input, context)
        context["expression_trace"] = expression_trace
        final_response, monitor_trace = self.filter_public_response(raw_response, user_input, context)
        context["monitor_trace"] = monitor_trace
        structural_meta = self.structural_meta_filter.assess(final_response, context)
        context = self.structural_meta_filter.apply_to_context(context, structural_meta)
        if structural_meta.get("should_reclean"):
            final_response, monitor_trace = self.filter_public_response(final_response, user_input, context)
            context["monitor_trace"] = monitor_trace
            structural_meta = self.structural_meta_filter.assess(final_response, context)
            context = self.structural_meta_filter.apply_to_context(context, structural_meta)
        if user_input and not str(final_response).strip():
            # Dernier garde-fou : ne jamais laisser une UI croire que Leia a crashé
            # simplement parce que la bouche ou le filtre a tout vidé.
            final_response = self._technical_expression_fallback(user_input, context)
            context["monitor_trace"] = {**dict(context.get("monitor_trace", {})), "empty_response_recovered": True}
        context["structural_meta_filter"] = structural_meta
        context["dialogue_knowledge"] = self._digest_knowledge_surface(
            f"Utilisateur: {user_input}\nLeia: {final_response}",
            "dialogue_exchange",
            context,
        )
        context["living_memory_absorption"] = self._absorb_text_into_living_memory(
            f"Utilisateur: {user_input}\nLeia: {final_response}",
            source="dialogue_exchange",
            metadata={"focus": context.get("focus", ""), "exchange": self.internal_time.exchange_count},
        )
        context["knowledge_expression_signal"] = self._knowledge_signal_for_expression(user_input)
        simulation_residue = self.simulation_residue.absorb(simulation)
        temporal_consequence = self.temporal_causality.close_consequence(final_response, relational_prediction)
        self.relational_bond.update_after_response(relational_prediction)
        after_effect = self.experiential_assimilator.assimilate(user_input, final_response, context, relational_prediction, monitor_trace, self)
        context["autobiographical_update"] = self._absorb_autobiographical_exchange(user_input, final_response, context, after_effect)
        context["long_living_dynamics_update"] = self._close_long_living_cycle(user_input, final_response, context, after_effect)
        context["persistent_subjective_life_update"] = self._close_persistent_subjective_life(user_input, final_response, context, after_effect)
        context["reading_living_dialogue_update"] = self._absorb_reading_dialogue_effect(user_input, final_response, context, after_effect)
        momentum_outcome = self.mental_momentum.absorb_outcome(after_effect)
        causal_arc = self.long_causal_arc.close_exchange(final_response, context, after_effect)
        drift_event = self.emergent_drift.absorb_exchange(self, context, after_effect)
        context["long_causal_arc_event"] = causal_arc
        context["emergent_drift_event"] = drift_event
        context["simulation_residue"] = simulation_residue
        context["temporal_consequence"] = temporal_consequence
        context["living_after_effect"] = after_effect
        context["momentum_outcome"] = momentum_outcome

        # ── V19+ : mise à jour post-réponse des nouveaux modules ────────────
        # Enjeux relationnels : enregistrement de l'outcome réel
        if self.relational_stakes is not None:
            try:
                user_reaction = {
                    "warmth": _safe_float(relational_prediction.get("warmth_effect", 0.0)),
                    "engagement": _safe_float(relational_prediction.get("engagement_effect", 0.0)),
                    "frustration": _safe_float(relational_prediction.get("distance_risk", 0.0)),
                    "tension": _safe_float(context.get("emotional_tension", 0.0)),
                }
                was_risky = bool(context.get("relational_stakes_signal", {}).get("assessment", {}).get("is_risky", False))
                self.relational_stakes.register_outcome(
                    description=f"exchange_{self.internal_time.exchange_count}",
                    response_mode=str(context.get("inhibition", {}).get("response_mode", "normal")),
                    user_reaction_signal=user_reaction,
                    was_risky=was_risky,
                )
            except Exception:
                pass

        # Pont mémoriel : enregistrement des topics dans les couches
        if self.memory_bridge is not None:
            try:
                topic = str(context.get("focus", user_input[:40]))
                self.memory_bridge.register_memory_signal(topic, "narrative", _safe_float(context.get("attention", {}).get("clarity", 0.3)))
                causal_strength = _safe_float(after_effect.get("causal_weight", 0.2)) if isinstance(after_effect, Mapping) else 0.2
                self.memory_bridge.register_memory_signal(topic, "causal", causal_strength)
                emotional_strength = _safe_float(self.emotional_state.resonance) * 0.6 + _safe_float(self.emotional_state.tension) * 0.4
                self.memory_bridge.register_memory_signal(topic, "affective", emotional_strength)
                self.memory_bridge.register_memory_signal(topic, "subjective", _safe_float(self.subjective_continuity.lived_presence))
                # Consolidation périodique
                if self.internal_time.exchange_count % 8 == 0:
                    self.memory_bridge.consolidate()
                    self.memory_bridge.detect_divergences()
            except Exception:
                pass

        # Conflit de valeurs : résolution auto si dilemme vieux
        if self.value_conflict_engine is not None:
            try:
                self.value_conflict_engine.auto_resolve_cycle(self.value_system.values)
            except Exception:
                pass

        # Plasticité sémantique : mise à jour après chaque échange
        if self.semantic_plasticity is not None:
            try:
                emotional_tone = float(self.emotional_state.valence) if hasattr(self.emotional_state, "valence") else 0.0
                plasticity_update = self.semantic_plasticity.process_exchange(
                    user_input=user_input,
                    leia_response=final_response,
                    emotional_tone=emotional_tone,
                    context=context,
                )
                context["semantic_plasticity_update"] = plasticity_update
            except Exception:
                pass
        # ────────────────────────────────────────────────────────────────────

        # 8. Mise à jour organique complète.
        affective = signals.get("affective_memory", {})
        self.emotional_state.absorb(affective, user_text=user_input)
        confidence = _safe_float(context.get("confidence", 0.5), 0.5)
        selected = simulation.get("selected", {}) if isinstance(simulation, Mapping) else {}
        value_alignment = _safe_float(selected.get("value_alignment", self.value_system.alignment(context)), 0.5)
        self.identity_state.recalibrate(self.emotional_state.tension, confidence, self.emotional_state, value_alignment)
        self.internal_time.tick(max(self.emotional_state.tension, self.emotional_state.resonance, _safe_float(relational_prediction.get("impact", 0.0))))
        self.homeostasis.regulate(self.emotional_state, self.internal_needs, self.identity_state, self.conversation_field)
        context["global_conscious_field"] = self.global_conscious_field.integrate(self, context, phase="response_integrated")
        context["organic_fusion"] = self.organic_fusion.integrate(self, context, stage="response_integrated")
        context["living_priority_matrix_event"] = self.living_priority_matrix.update(self, context, stage="response_integrated")
        context = self.living_priority_matrix.apply_to_context(context)
        context["living_state_bus_event"] = self.living_state_bus.publish(self, "response_integrated", context)
        context = self.living_state_bus.apply_to_context(context)
        context["embodied_presence_event"] = self.embodied_presence_core.integrate(self, context, stage="response_integrated")
        context = self.embodied_presence_core.apply_to_context(context)
        context["embodied_state_event"] = self.embodied_state.integrate(self, context, stage="response_integrated")
        context["embodied_state"] = self.embodied_state.influence_context()
        context["living_executive_event"] = self.living_executive.resolve(self, context, stage="response_integrated")
        context = self.living_executive.apply_to_context(context, context["living_executive_event"])
        context["stability_hysteresis_event"] = self.stability_hysteresis.stabilize(self, context, stage="response_integrated")
        context["emergence_event"] = self.emergence_detector.detect(self, context, final_response)
        context["living_presence_stabilizer_after"] = self.living_presence_stabilizer.after_response(self, final_response, context)
        context["living_causal_graph_event"] = self.living_causal_graph.absorb_exchange(self, context, final_response, after_effect)
        context["autonomous_continuity_tick"] = self.autonomous_continuity_loop.tick(self, 0.0, reason="post_response")
        context["module_sync_context"] = self.cross_module_synchronizer.sync(self, context, stage="response_integrated")
        context["identity_evolution_event"] = self.identity_evolution_memory.absorb_exchange(self, user_input, final_response, context, after_effect)

        self._feed_thought_stream(user_input, final_response, context)
        self.value_system.update(context, {"selected_mode": selected.get("mode", inhibition.get("response_mode"))})
        self.personal_narrative.absorb_episode(user_input, final_response, context, impact=relational_prediction.get("impact", 0.0))

        self.living_state["public_response"] = final_response
        self.living_state["confidence"] = confidence
        self.living_state["meta_risk"] = _safe_float(context.get("meta_risk", 0.0))
        self.living_state["living_after_effect"] = context.get("living_after_effect", {})
        self.remember_exchange(user_input, final_response, context)
        self.shared_state.update_from_core(self, "response_committed", context)
        self._refresh_snapshots()
        self._save_persistent_state()
        return final_response

    # ------------------------------------------------------------------
    # Perception / signaux
    # ------------------------------------------------------------------

    def perceive_exchange(self, user_input: str, emo_propagation: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
        presence = self.adapters.presence_read(user_input, {"field": self.conversation_field.snapshot(), "emotion": self.emotional_state.snapshot()})
        attention = self.adapters.attention_focus(user_input, presence, emo_propagation)
        self.living_state["presence"] = presence
        self.living_state["attention"] = attention
        return {"presence": presence, "attention": attention}

    def collect_living_signals(self, user_input: str, emo_propagation: Mapping[str, Any]) -> Dict[str, Dict[str, Any]]:
        impulse = self.adapters.impulse_arise(user_input, self.living_state.get("attention", {}), emo_propagation)
        initiative = self.adapters.initiative_evaluate(user_input, impulse, self.living_state.get("attention", {}), emo_propagation)
        causal = self.adapters.causal_recall(user_input, self.living_state.get("presence", {}), emo_propagation)
        self.adapters.causal_update_links(user_input, causal)
        affective = self.adapters.affective_recall(user_input, causal)
        self.living_state.update({"impulse": impulse, "initiative": initiative, "causal_memory": causal, "affective_memory": affective})
        return {"impulse": impulse, "initiative": initiative, "causal_memory": causal, "affective_memory": affective}

    def differentiate_intention(self, impulse: Mapping[str, Any], initiative: Mapping[str, Any]) -> Dict[str, Any]:
        impulse_force = _clamp(impulse.get("strength", 0.0))
        initiative_drive = _clamp(initiative.get("drive", 0.0))
        desire_strength = _clamp(self.internal_needs.expression * 0.36 + self.internal_needs.curiosity * 0.28 + self.internal_needs.closeness * 0.18 + self.internal_needs.recognition * 0.18)
        intention_stability = _clamp(self.emotional_state.emotional_safety * 0.42 + self.emotional_state.trust_accumulated * 0.30 + self.identity_state.self_coherence * 0.28)
        forces = {"impulse": impulse_force, "desire": desire_strength, "initiative": initiative_drive, "intention": intention_stability * 0.72}
        return {
            "impulse_force": round(impulse_force, 4),
            "desire_strength": round(desire_strength, 4),
            "desire_target": self.internal_needs.dominant_need(),
            "initiative_drive": round(initiative_drive, 4),
            "intention_stability": round(intention_stability, 4),
            "dominant_force": max(forces, key=forces.get),
            "forces": {k: round(v, 4) for k, v in forces.items()},
        }

    def resolve_signal_priority(self, signals: Mapping[str, Any], perception: Mapping[str, Any], propagation: Mapping[str, Any]) -> Dict[str, Any]:
        presence = perception.get("presence", {})
        affective = signals.get("affective_memory", {})
        impulse = signals.get("impulse", {})
        causal = signals.get("causal_memory", {})
        weights = {
            "presence": 0.30 + _safe_float(presence.get("user_distress", 0.0)) * 0.40,
            "emotion": 0.25 + _safe_float(affective.get("tension", 0.0)) * 0.34,
            "memory": 0.20 + _safe_float(causal.get("sensitivity", 0.0)) * 0.28 + self.internal_needs.understanding * 0.10,
            "impulse": max(0.0, _safe_float(impulse.get("strength", 0.0)) * 0.25 - self.emotional_state.fatigue * 0.10 - _safe_float(propagation.get("inhibition_pressure", 0.0)) * 0.08),
            "initiative": max(0.0, 0.14 + self.emotional_state.fatigue * 0.16 - _safe_float(propagation.get("initiative_dampener", 0.0)) * 0.18),
            "desire": self.internal_needs.expression * 0.24 + self.internal_needs.curiosity * 0.16,
            "values": self.value_system.values.get("coherence", 0.7) * 0.08,
        }
        total = sum(weights.values()) or 1.0
        normalized = {k: round(v / total, 4) for k, v in weights.items()}
        normalized["dominant"] = max(weights, key=weights.get)
        self.living_state["signal_priority"] = normalized
        return normalized

    def resolve_internal_tensions(self, signals: Mapping[str, Any], priority: Mapping[str, Any], intention_map: Mapping[str, Any]) -> Dict[str, Any]:
        impulse = signals.get("impulse", {})
        initiative = signals.get("initiative", {})
        causal = signals.get("causal_memory", {})
        affective = signals.get("affective_memory", {})
        impulse_speak = impulse.get("direction", "parler") == "parler"
        initiative_wait = initiative.get("direction", "parler") == "attendre"
        sensitive = _safe_float(causal.get("sensitivity", 0.0)) > 0.50
        fragile = _safe_float(affective.get("user_fragility", 0.0)) > 0.42
        dominant_force = intention_map.get("dominant_force", "impulse")
        conflict = 0.0
        arbitration = "proceed"
        modulation = 1.0
        if impulse_speak and initiative_wait:
            conflict += 0.38; arbitration = "hesitate"; modulation = 0.72
        if sensitive:
            conflict += 0.28; arbitration = "slow_down"; modulation = min(modulation, 0.62)
        if fragile:
            conflict += 0.30; arbitration = "soften"; modulation = min(modulation, 0.54)
        conflict = _clamp(conflict - _safe_float(intention_map.get("intention_stability", 0.5)) * 0.18 + self.personal_narrative.long_arc.get("unfinished_weight", 0.0) * 0.10)
        if priority.get("dominant") == "emotion" and conflict > 0.46:
            arbitration = "amplify_softness"; modulation = min(modulation, 0.50)
        elif dominant_force == "desire" and self.internal_needs.expression > 0.72 and conflict < 0.45:
            arbitration = "allow_expression"; modulation = max(modulation, 1.12)
        elif priority.get("dominant") == "values" and self.identity_state.drift_risk > 0.45:
            arbitration = "recenter"; modulation = min(modulation, 0.70)
        tension = {"conflict_level": round(conflict, 4), "arbitration": arbitration, "modulation": round(modulation, 4), "impulse_vs_initiative": impulse_speak and initiative_wait, "sensitive_memory": sensitive, "fragile_user": fragile}
        self.living_state["internal_tension"] = tension
        return tension

    def generate_micro_reactions(self, signals: Mapping[str, Any], tension_map: Mapping[str, Any], propagation: Mapping[str, Any]) -> List[Dict[str, Any]]:
        attention = signals.get("attention", self.living_state.get("attention", {}))
        impulse = signals.get("impulse", {})
        reactions: List[Dict[str, Any]] = []
        items = [
            ("surprise", _safe_float(attention.get("surprise", 0.0)), 0.50),
            ("curiosite", max(_safe_float(attention.get("curiosity", 0.0)), self.internal_needs.curiosity * 0.70), 0.40),
            ("hesitation", _safe_float(tension_map.get("conflict_level", 0.0)) * 0.60 + self.emotional_state.fatigue * 0.35, 0.34),
            ("attraction", _safe_float(impulse.get("strength", 0.0)) * 0.50 + _safe_float(attention.get("curiosity", 0.0)) * 0.45, 0.54),
            ("retenue", _safe_float(tension_map.get("conflict_level", 0.0)), 0.60),
            ("micro_silence", self.emotional_state.fatigue, 0.72),
            ("chaleur", _safe_float(propagation.get("warmth_level", 0.5)) * self.conversation_field.relational_proximity, 0.50),
        ]
        for typ, value, threshold in items:
            if value > threshold:
                reactions.append({"type": typ, "intensity": round(_clamp(value), 3)})
        self.living_state["micro_reactions"] = reactions
        return reactions

    def _compute_inhibition(self, tension_map: Mapping[str, Any]) -> Dict[str, Any]:
        conflict = _safe_float(tension_map.get("conflict_level", 0.0))
        momentum_pressure = self.mental_momentum.influence_context().get("expressive_pressure_bias", 0.0) if hasattr(self, "mental_momentum") else 0.0
        # Formule adoucie : fatigue et tension pèsent moins, momentum aide plus.
        # Seuil de silence relevé à 0.94 (était 0.88) pour que Leia parle davantage.
        inhibition = _clamp(
            conflict * 0.20
            + self.emotional_state.fatigue * 0.16
            + self.emotional_state.accumulated_tension * 0.14
            + self.emotional_state.cognitive_overload * 0.14
            + self.internal_needs.rest * 0.10
            - _safe_float(momentum_pressure) * 0.12
        )
        mode = "normal"
        should = True
        if inhibition > 0.94:          # seuil relevé (était 0.88)
            should = False; mode = "silence"
        elif inhibition > 0.72:
            mode = "minimal"
        elif inhibition > 0.50:
            mode = "soft"
        elif _safe_float(tension_map.get("modulation", 1.0)) < 0.55:
            mode = "restrained"
        elif self.internal_needs.expression > 0.70 and self.emotional_state.cognitive_overload < 0.60:
            mode = "expressive"
        result = {"should_answer": should, "level": round(inhibition, 4), "response_mode": mode}
        self.living_state["should_answer"] = should
        self.living_state["inhibition_level"] = result["level"]
        return result

    # ------------------------------------------------------------------
    # Simulation, prédiction, contexte
    # ------------------------------------------------------------------

    def simulate_possible_responses(self, context: Mapping[str, Any]) -> Dict[str, Any]:
        modes = ["direct", "soft", "minimal", "curious"]
        if context.get("arbitration") in {"slow_down", "soften", "amplify_softness"}:
            modes = ["soft", "minimal", "direct", "curious"]
        candidates = []
        for mode in modes:
            meta_risk = _safe_float(context.get("meta_risk", 0.0))
            tension = _safe_float(context.get("emotional_tension", 0.0))
            confidence = _safe_float(context.get("confidence", 0.5))
            relational = self._predict_mode_relational_effect(mode, tension, confidence)
            coherence = _clamp(confidence - (0.08 if mode == "curious" and tension > 0.55 else 0.0) + (0.05 if mode == "direct" else 0.0))
            gate = context.get("meta_prevention", {}) if isinstance(context.get("meta_prevention", {}), Mapping) else {}
            meta_penalty = _safe_float(gate.get("risk", 0.0)) * (0.20 if mode in {"direct", "curious"} else 0.10)
            candidate = {"mode": mode, "meta_risk": meta_risk + (0.08 if mode == "curious" else 0.0), "predicted_relational_effect": relational, "coherence": coherence}
            embodied = self.embodied_simulation.score_candidate(self, context, candidate)
            candidate["embodied_simulation"] = embodied
            candidate["value_alignment"] = self.value_system.alignment(candidate)
            momentum = context.get("mental_momentum", {}) if isinstance(context.get("mental_momentum", {}), Mapping) else {}
            tendencies = self.experiential_assimilator.learned_tendencies
            momentum_bias = _safe_float(momentum.get("expressive_pressure_bias", 0.0)) * (0.06 if mode in {"direct", "curious"} else 0.025)
            continuity_bias = _safe_float(momentum.get("continuation_bias", 0.0)) * (0.05 if mode in {"direct", "soft"} else 0.018)
            learned_bias = 0.0
            if mode == "soft":
                learned_bias += tendencies.get("soften_under_tension", 0.0) * tension * 0.035
            if mode == "direct" and tension < 0.42:
                learned_bias += tendencies.get("prefer_direct_when_stable", 0.0) * 0.025
            lived_body = self.embodied_state.influence_context()
            body_bonus = lived_body.get("embodied_release", 0.0) * (0.045 if mode in {"direct", "curious"} else 0.025) + lived_body.get("grounding", 0.0) * 0.035 - lived_body.get("embodied_restraint", 0.0) * (0.055 if mode in {"direct", "curious"} else 0.025)
            candidate["embodied_state"] = lived_body
            embodied_bonus = embodied.get("embodied_continuity", 0.0) * 0.08 + embodied.get("expressive_release", 0.0) * 0.035 - embodied.get("subjective_cost", 0.0) * 0.07 + body_bonus
            candidate["score"] = round(_clamp(candidate["value_alignment"] * 0.50 + relational * 0.22 + coherence * 0.18 + momentum_bias + continuity_bias + learned_bias + embodied_bonus - meta_penalty), 4)
            candidates.append(candidate)
        simulation_result = self.embodied_simulation.finalize(candidates)
        selected = simulation_result.get("selected", {})
        return {"candidates": candidates, "selected": selected, "reason": "value_relational_coherence_embodied", "embodied_simulation": self.embodied_simulation.snapshot()}

    def _predict_mode_relational_effect(self, mode: str, tension: float, confidence: float) -> float:
        base = self.conversation_field.relational_trust * 0.35 + self.emotional_state.emotional_safety * 0.30 + confidence * 0.35
        if mode == "soft":
            base += tension * 0.12
        if mode == "minimal":
            base += tension * 0.06 - self.internal_needs.expression * 0.05
        if mode == "curious":
            base += self.internal_needs.curiosity * 0.08 - tension * 0.10
        if mode == "direct":
            base += self.identity_state.temperament.get("directness", 0.6) * 0.05 - tension * 0.04
        return round(_clamp(base), 4)

    def predict_relational_effect(self, context: Mapping[str, Any], simulation: Mapping[str, Any]) -> Dict[str, Any]:
        selected = simulation.get("selected", {}) if isinstance(simulation, Mapping) else {}
        impact = _safe_float(selected.get("predicted_relational_effect", 0.5))
        tension = _safe_float(context.get("emotional_tension", 0.0))
        return {
            "impact": round(_clamp(impact), 4),
            "expected_user_comfort": round(_clamp(impact - tension * 0.12), 4),
            "risk_of_distance": round(_clamp(tension * 0.35 + _safe_float(context.get("meta_risk", 0.0)) * 0.45 - impact * 0.25), 4),
            "best_mode": selected.get("mode", "direct"),
        }

    def build_living_context(self, user_input: str, signals: Mapping[str, Any], priority: Mapping[str, Any], tension_map: Mapping[str, Any], micro_reactions: List[Dict[str, Any]], inhibition: Mapping[str, Any], intention_map: Mapping[str, Any], emo_propagation: Mapping[str, Any], spontaneous_return: Optional[Mapping[str, Any]], subjective_event: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        presence = signals.get("presence", {})
        attention = signals.get("attention", {})
        impulse = signals.get("impulse", {})
        initiative = signals.get("initiative", {})
        causal = signals.get("causal_memory", {})
        affective = signals.get("affective_memory", {})
        confidence = self._compute_confidence(presence, attention, impulse, causal)
        meta_risk = self.adapters.monitor_meta_risk(user_input, impulse, initiative)
        context = {
            "user_input": user_input,
            "presence": presence,
            "attention": attention,
            "impulse": impulse,
            "initiative": initiative,
            "causal_memory": causal,
            "affective_memory": affective,
            "feeling": self.emotional_state.tone,
            "focus": attention.get("focal_point", ""),
            "response_impulse": impulse.get("content", ""),
            "memory_echo": causal.get("relevant_past", ""),
            "meta_risk": meta_risk,
            "continuity": causal.get("continuity_score", 0.0),
            "emotional_tension": self.emotional_state.tension,
            "confidence": confidence,
            "intention_map": intention_map,
            "dominant_force": intention_map.get("dominant_force", "impulse"),
            "signal_priority": priority,
            "dominant_signal": priority.get("dominant", "presence"),
            "tension_map": tension_map,
            "arbitration": tension_map.get("arbitration", "proceed"),
            "modulation": tension_map.get("modulation", 1.0),
            "micro_reactions": micro_reactions,
            "inhibition": dict(inhibition),
            "spontaneous_return": dict(spontaneous_return) if spontaneous_return else None,
            "subjective_event": dict(subjective_event) if subjective_event else None,
            "subjective_continuity": self.subjective_continuity.snapshot(),
            "temporal_causality": self.temporal_causality.snapshot(),
            "relational_bond": self.relational_bond.snapshot(),
            "autobiographical_self": self.autobiographical_self.snapshot(),
            "motivation_field": self.motivation_field.snapshot(),
            "simulation_residue": self.simulation_residue.snapshot(),
            "emotional_state": self.emotional_state.snapshot(),
            "emotional_propagation": dict(emo_propagation),
            "internal_needs": self.internal_needs.snapshot(),
            "thought_stream": self.thought_stream.snapshot(),
            "conversation_field": self.conversation_field.snapshot(),
            "identity_state": self.identity_state.snapshot(),
            "internal_time": self.internal_time.snapshot(),
            "personal_narrative": self.personal_narrative.snapshot(),
            "value_system": self.value_system.snapshot(),
            "homeostasis": dict(self.homeostasis.last_balance),
            "expressive_energy": self.emotional_state.energy,
            "expressive_warmth": emo_propagation.get("warmth_level", 0.5),
            "expressive_freedom": self.identity_state.expressive_freedom,
            "relational_proximity": self.conversation_field.relational_proximity,
            "relational_trust": self.conversation_field.relational_trust,
            "topic_depth": self.conversation_field.topic_depth,
            "emotional_safety": self.emotional_state.emotional_safety,
            "trust_level": emo_propagation.get("trust_level", 0.5),
            "shared_state": self.shared_state.snapshot(),
            "mental_momentum": self.mental_momentum.snapshot(),
            "experiential_assimilator": self.experiential_assimilator.snapshot(),
            "attention_arbitration": self.attention_arbitration.snapshot(),
            "embodied_simulation": self.embodied_simulation.snapshot(),
            "long_causal_arc": self.long_causal_arc.snapshot(),
            "emergent_drift": self.emergent_drift.snapshot(),
            "organic_fusion": self.organic_fusion.snapshot(),
        }
        self.living_state["expression_intent"] = {
            "dominant_signal": context["dominant_signal"],
            "dominant_force": context["dominant_force"],
            "response_mode": inhibition.get("response_mode"),
            "arbitration": context["arbitration"],
        }

        # V18 — Signaux de compréhension réelle
        context["utterance_signal"] = self.living_state.get("utterance_signal", {"available": False})
        context["user_affect_signal"] = self.living_state.get("user_affect_signal", {"available": False})
        context["associative_signal"] = self.living_state.get("associative_signal", {"available": False})
        context["user_model_signal"] = (
            self.user_model.signal(user_input) if self.user_model is not None
            else {"available": False})
        context["proposition_signal"] = (
            self.proposition_extractor.signal(
                user_input,
                focus_concepts=self.living_state.get("utterance_signal", {}).get("focus_concepts", [])
            ) if self.proposition_extractor is not None
            else {"available": False})

        return context

    # ------------------------------------------------------------------
    # Expression / filtre / mémoire
    # ------------------------------------------------------------------

    def generate_expression(self, user_input: str, context: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
        local_context = dict(context)
        if "meta_prevention" not in local_context:
            local_context = self.meta_prevention_gate.apply(local_context)
        local_context["living_presence_stabilizer_event"] = self.living_presence_stabilizer.before_expression(self, user_input, local_context)
        local_context["living_expression_payload"] = self._build_living_expression_payload(user_input, local_context)

        payload = local_context.get("living_expression_payload", {}) if isinstance(local_context.get("living_expression_payload", {}), Mapping) else {}
        lower_user_for_mode = str(user_input or "").lower()
        direct_truth_mode = (
            any(marker in lower_user_for_mode for marker in (
                "vivante", "vivant", "consciente", "préécrit", "preecrit", "template",
                "par toi", "toute seule", "100%", "fini", "terminé", "termine", "prête", "prete"
            ))
            and ("?" in lower_user_for_mode or len(lower_user_for_mode.split()) <= 8)
        )
        command_repair_mode = any(marker in lower_user_for_mode for marker in (
            "vasy", "vas-y", "corrige", "ajoute", "prend ton temps"
        ))
        greeting_mode = bool(re.search(r"\b(salut|bonjour|hey|coucou)\b", lower_user_for_mode))

        text, trace = self.adapters.expression_generate(user_input, local_context)
        quality = self._expression_quality(text, user_input, local_context)
        if direct_truth_mode:
            # Pour les questions de vérité, on ne laisse pas l'ancienne bouche
            # répondre par une surface abstraite. Le tisseur doit produire un
            # atome direct (oui/non/partiellement/pas encore) puis seulement
            # ensuite l'état vivant module la suite.
            quality = {**quality, "usable": False, "forced_direct_truth_weaver": True}
        book_answer_mode = (
            any(marker in lower_user_for_mode for marker in (
                "livre", "pdf", "bergson", "retiens", "retenu", "mémoire", "memoire", "matière", "matiere"
            ))
            and ("?" in lower_user_for_mode or any(q in lower_user_for_mode for q in ("que ", "quoi", "comment", "vois", "penses")))
        )
        if book_answer_mode:
            quality = {**quality, "usable": False, "forced_book_weaver": True}
        if command_repair_mode:
            quality = {**quality, "usable": False, "forced_command_repair_weaver": True}
        preforced_mode = bool(direct_truth_mode or book_answer_mode or command_repair_mode or greeting_mode)
        if preforced_mode:
            woven_text, woven_trace = self._emergent_weaver_expression(user_input, local_context)
            woven_quality = self._expression_quality(woven_text, user_input, local_context)
            if woven_quality.get("usable") or len(str(woven_text or "").split()) >= 4:
                return woven_text.strip(), {
                    "preforced_weaver": True,
                    "forced_direct_truth": bool(direct_truth_mode),
                    "forced_book_answer": bool(book_answer_mode),
                    "forced_command_repair": bool(command_repair_mode),
                    "forced_greeting": bool(greeting_mode),
                    "weaver_trace": woven_trace,
                    "quality": woven_quality,
                }
        book_memory = payload.get("book_memory", {}) if isinstance(payload.get("book_memory", {}), Mapping) else {}
        stabilizer = payload.get("living_presence_stabilizer", {}) if isinstance(payload.get("living_presence_stabilizer", {}), Mapping) else {}
        generic_atoms = {"continuité", "continuite", "résonance", "resonance", "appui", "doute", "question", "prudence", "présence", "presence", "trace", "lien", "mouvement", "rythme", "mémoire", "memoire", "limite"}
        conversational_focus = {
            "vivante", "vivant", "consciente", "conscient", "preecrit", "préécrit",
            "template", "fini", "terminé", "termine", "prête", "prete", "salut",
            "bonjour", "toi", "moi", "meme", "même", "parler", "corrige", "vasy", "vas-y",
        }
        raw_focus_terms = [str(x).lower().strip() for x in (list(stabilizer.get("must_surface_concepts", []) or []) + list(book_memory.get("axes", []) or []) + list(book_memory.get("keywords", []) or []))[:16] if str(x).strip()]
        book_focus = [tok for tok in raw_focus_terms if tok not in conversational_focus and not any(part in conversational_focus for part in tok.split())]
        concrete_focus = [tok for tok in book_focus if tok not in generic_atoms and len(tok) >= 4]
        text_lower = str(text or "").lower()
        focus_pool = [] if direct_truth_mode else concrete_focus[:8]
        book_surface_missing = bool(focus_pool) and not any(tok in text_lower for tok in focus_pool)
        if quality.get("usable") and not book_surface_missing:
            return text.strip(), {**trace, "quality": quality}

        woven_text, woven_trace = self._emergent_weaver_expression(user_input, local_context)
        woven_quality = self._expression_quality(woven_text, user_input, local_context)
        woven_lower = str(woven_text or "").lower()
        woven_missing = bool(focus_pool) and not any(tok in woven_lower for tok in focus_pool)
        if woven_quality.get("usable") and not woven_missing:
            return woven_text.strip(), {
                **trace,
                "old_expression_rejected": quality,
                "weaver_trace": woven_trace,
                "quality": woven_quality,
            }

        return self._technical_expression_fallback(user_input, local_context), {
            "fallback": True,
            **trace,
            "old_expression_rejected": quality,
            "weaver_trace": woven_trace,
            "living_payload_used": True,
        }

    def _expression_quality(self, text: Any, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        surface = str(text or "").strip()
        words = re.findall(r"\b[\wÀ-ÿ']+\b", surface.lower())
        unique_ratio = (len(set(words)) / max(1, len(words))) if words else 0.0
        repeats = len(words) - len(set(words))
        lower_surface = surface.lower()
        meta_hits = sum(1 for marker in ("payload", "trace", "module", "score", "axis", "neurone", "debug") if marker in lower_surface)
        user_words = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", str(user_input or "").lower()))
        parrot = sum(1 for w in words if w in user_words) if user_words and words else 0
        generic_atoms = {"continuité", "continuite", "résonance", "resonance", "appui", "doute", "question", "prudence", "présence", "presence", "trace", "lien", "mouvement", "rythme", "mémoire", "memoire", "limite"}
        generic_hits = sum(1 for w in words if w in generic_atoms)
        generic_ratio = generic_hits / max(1, len(words))
        bad_grammar = bool(re.search(r"\b(ça|ca)\s+(sens|cherche|garde|tiens|reste|réponds|reponds|précise|precise)\b|\bsens\s+(tiens|garde|cherche)\b|\bje\s+(tiens|garde|cherche)\s+(tiens|garde|cherche)\b", lower_surface))
        lower_user = str(user_input or "").lower()
        asks_direct_truth = (
            any(marker in lower_user for marker in (
                "prête", "prete", "préécrit", "preecrit", "template", "100%", "fini", "terminé",
                "termine", "vivante", "vivant", "consciente", "conscience"
            ))
            and ("?" in lower_user or len(lower_user.split()) <= 8)
        )
        direct_words = {"oui", "non", "pas", "encore", "partiellement"}
        has_direct_truth_atom = bool(words and (words[0] in direct_words or any(w in direct_words for w in words[:3])))
        vague_surface = bool(re.search(r"\b(ça|ca)\s+(cherche|garde|tiens|reste|répond|repond|précise|precise)\b", lower_surface))
        abstract_loop = generic_ratio > 0.30 and any(v in lower_surface for v in ("doute", "prudence", "continuité", "résonance", "appui"))
        too_generic_for_direct = asks_direct_truth and not has_direct_truth_atom
        usable = (
            len(words) >= 5
            and unique_ratio >= 0.58
            and repeats <= 3
            and meta_hits == 0
            and parrot <= max(2, int(len(words) * 0.36))
            and generic_ratio <= 0.42
            and not bad_grammar
            and not vague_surface
            and not abstract_loop
            and not too_generic_for_direct
        )
        return {
            "usable": bool(usable),
            "word_count": len(words),
            "unique_ratio": round(unique_ratio, 3),
            "repeats": repeats,
            "meta_hits": meta_hits,
            "parrot_hits": parrot,
            "generic_ratio": round(generic_ratio, 3),
            "bad_grammar": bool(bad_grammar),
            "vague_surface": bool(vague_surface),
            "abstract_loop": bool(abstract_loop),
            "direct_truth_required": bool(asks_direct_truth),
        }

    def _emergent_weaver_expression(self, user_input: str, context: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
        payload = context.get("living_expression_payload", {}) if isinstance(context.get("living_expression_payload", {}), Mapping) else {}
        try:
            from emergent_french_weaver import EmergentFrenchWeaver
            if not hasattr(self, "_emergent_french_weaver") or self._emergent_french_weaver is None:
                self._emergent_french_weaver = EmergentFrenchWeaver()
            result = self._emergent_french_weaver.generate(
                user_message=str(user_input or ""),
                payload=payload,
                min_words=7,
                max_words=28,
            )
            return str(result.get("text", "")).strip(), dict(result.get("trace", {}))
        except Exception as exc:
            return "", {"engine": "EmergentFrenchWeaver", "error": f"{type(exc).__name__}:{exc}"}

    def _concept_relation_signal(self, query_text: str) -> Dict[str, Any]:
        """Réactive les relations conceptuelles apprises par lecture.

        V15 : utilise chain_query() pour traverser le graphe par BFS (depth=2).
        Si mémoire → durée et durée → temps, une question sur "temps" active
        aussi "mémoire" — sans LLM, sans phrase préécrite.

        Ne fabrique pas une réponse : renvoie seulement les triplets pertinents.
        """
        try:
            if getattr(self, "concept_relation_engine", None) is None:
                return {"available": False}
            engine = self.concept_relation_engine
            # Essayer chain_query d'abord (V15+), fallback sur query simple
            if hasattr(engine, "chain_query"):
                return engine.chain_query(query_text, depth=2, limit=16)
            return engine.query(query_text, limit=14)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _book_expression_material(self, query_text: str, context: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        """Convertit les lectures consolidées en matière expressive.

        Important : cette méthode ne contient aucune phrase-réponse. Elle ne fait
        qu'extraire des axes, mots, relations et pressions depuis la mémoire déjà
        digérée/synthétisée afin que la bouche parle depuis le livre au lieu de
        retomber sur des états abstraits comme continuité/doute/appui.
        """
        context = context or {}
        signal = context.get("knowledge_expression_signal")
        if not isinstance(signal, Mapping):
            signal = self._knowledge_signal_for_expression(query_text)

        last_book = self.living_state.get("last_book_synthesis", {})
        if not isinstance(last_book, Mapping):
            last_book = {}
        deep_signal = self._book_understanding_signal(query_text)
        if not isinstance(deep_signal, Mapping):
            deep_signal = {}
        deep_model = self.living_state.get("book_understanding", {})
        if not isinstance(deep_model, Mapping):
            deep_model = {}
        reading_signal = context.get("reading_living_signal") if isinstance(context.get("reading_living_signal"), Mapping) else self._reading_living_signal(query_text)
        if not isinstance(reading_signal, Mapping):
            reading_signal = {}
        concept_relation_signal = context.get("concept_relation_signal") if isinstance(context.get("concept_relation_signal"), Mapping) else self._concept_relation_signal(query_text)
        if not isinstance(concept_relation_signal, Mapping):
            concept_relation_signal = {}

        def unique_tokens(values: Iterable[Any], limit: int = 24) -> List[str]:
            out: List[str] = []
            for value in values or []:
                if isinstance(value, Mapping):
                    candidates = [
                        value.get("label"), value.get("concept"), value.get("keyword"),
                        value.get("source"), value.get("target"), value.get("axis"),
                    ]
                elif isinstance(value, (list, tuple)):
                    candidates = list(value)
                else:
                    candidates = [value]
                for cand in candidates:
                    text = re.sub(r"\s+", " ", str(cand or "").strip().lower())
                    if not text or len(text) < 3:
                        continue
                    if re.match(r"^(relier|clarifier|explorer|résoudre|resoudre|ouvrir_question)\b", text):
                        continue
                    # On garde des unités de sens courtes, pas des phrases de réponse.
                    if len(text) > 64:
                        text = text[:64].rsplit(" ", 1)[0] or text[:64]
                    if text not in out:
                        out.append(text)
                    if len(out) >= limit:
                        return out
            return out

        axes = unique_tokens(
            list(signal.get("synthesis_axes", []) if isinstance(signal, Mapping) else [])
            + list(last_book.get("axes", []) or [])
            + list(signal.get("reactivated_concepts", []) if isinstance(signal, Mapping) else [])
            + list(signal.get("linked_concepts", []) if isinstance(signal, Mapping) else [])
            + list(deep_signal.get("active_concepts", []) if isinstance(deep_signal, Mapping) else [])
            + list(reading_signal.get("active_concepts", []) if isinstance(reading_signal, Mapping) else [])
            + list(concept_relation_signal.get("active_concepts", []) if isinstance(concept_relation_signal, Mapping) else [])
            + list(deep_model.get("axes", []) or [])
            + list(deep_model.get("transformations", []) or []),
            24,
        )
        keywords = unique_tokens(
            list(signal.get("synthesis_keywords", []) if isinstance(signal, Mapping) else [])
            + list(last_book.get("top_keywords", []) or [])
            + list(signal.get("reactivated_atoms", []) if isinstance(signal, Mapping) else [])
            + list(signal.get("recent_atoms", []) if isinstance(signal, Mapping) else [])
            + list(deep_model.get("keywords", []) or [])
            + list((reading_signal.get("last_reflection", {}) or {}).get("active_concepts", []) if isinstance(reading_signal.get("last_reflection", {}), Mapping) else []),
            36,
        )

        relations: List[Dict[str, str]] = []
        relation_sources = []
        if isinstance(signal, Mapping):
            relation_sources += list(signal.get("synthesis_relations", []) or [])
        relation_sources += list(last_book.get("relations", []) or [])
        relation_sources += list(deep_signal.get("relations", []) if isinstance(deep_signal, Mapping) else [])
        relation_sources += list((reading_signal.get("last_reflection", {}) or {}).get("relation_focus", []) if isinstance(reading_signal.get("last_reflection", {}), Mapping) else [])
        relation_sources += list(concept_relation_signal.get("relations", []) if isinstance(concept_relation_signal, Mapping) else [])
        relation_sources += list(deep_model.get("relations", []) or [])
        relation_sources += list(deep_model.get("tensions", []) or [])
        for rel in relation_sources[:24]:
            if isinstance(rel, Mapping):
                src = str(rel.get("source") or rel.get("from") or rel.get("a") or "").strip().lower()
                tgt = str(rel.get("target") or rel.get("to") or rel.get("b") or "").strip().lower()
                typ = str(rel.get("type") or rel.get("relation") or rel.get("kind") or "lié").strip().lower()
            elif isinstance(rel, (list, tuple)) and len(rel) >= 2:
                src, tgt = str(rel[0]).strip().lower(), str(rel[1]).strip().lower()
                typ = str(rel[2]).strip().lower() if len(rel) > 2 else "lié"
            else:
                continue
            if (not src or not tgt) and isinstance(rel, Mapping) and isinstance(rel.get("between"), (list, tuple)) and len(rel.get("between")) >= 2:
                src = str(rel.get("between")[0]).strip().lower()
                tgt = str(rel.get("between")[1]).strip().lower()
                typ = str(rel.get("relation") or "tension").strip().lower()
            if src and tgt and src != tgt:
                relations.append({"source": src[:64], "target": tgt[:64], "type": typ[:32] or "lié"})

        pressures: Dict[str, float] = {}
        if isinstance(signal, Mapping):
            raw_pressures = signal.get("concept_pressures", {})
            if isinstance(raw_pressures, Mapping):
                for k, v in raw_pressures.items():
                    try:
                        pressures[str(k).strip().lower()[:64]] = _clamp(v)
                    except Exception:
                        continue
        deep_pressures = deep_signal.get("concept_pressures", {}) if isinstance(deep_signal.get("concept_pressures", {}), Mapping) else {}
        for k, v in deep_pressures.items():
            token = re.sub(r"\s+", " ", str(k or "").strip().lower())[:64]
            if token:
                pressures[token] = max(pressures.get(token, 0.0), _clamp(v))
        relation_pressures = concept_relation_signal.get("concept_pressures", {}) if isinstance(concept_relation_signal.get("concept_pressures", {}), Mapping) else {}
        for k, v in relation_pressures.items():
            token = re.sub(r"\s+", " ", str(k or "").strip().lower())[:64]
            if token:
                pressures[token] = max(pressures.get(token, 0.0), _clamp(v) * 1.08)
        model_pressures = deep_model.get("concept_pressures", {}) if isinstance(deep_model.get("concept_pressures", {}), Mapping) else {}
        for k, v in model_pressures.items():
            token = re.sub(r"\s+", " ", str(k or "").strip().lower())[:64]
            if token:
                pressures[token] = max(pressures.get(token, 0.0), _clamp(v) * 0.94)
        for index, token in enumerate(axes + keywords[:12]):
            pressures[token] = max(pressures.get(token, 0.0), _clamp(0.70 - index * 0.025))

        unresolved = unique_tokens(
            list(signal.get("unresolved_questions", []) if isinstance(signal, Mapping) else [])
            + list(last_book.get("unresolved_questions", []) or [])
            + list(deep_signal.get("question_axes", []) if isinstance(deep_signal, Mapping) else [])
            + list(deep_model.get("question_axes", []) or []),
            14,
        )
        metrics = {}
        if isinstance(signal, Mapping) and isinstance(signal.get("synthesis_metrics"), Mapping):
            metrics.update(signal.get("synthesis_metrics"))
        if isinstance(last_book.get("metrics"), Mapping):
            metrics.update(last_book.get("metrics"))
        if isinstance(deep_model.get("metrics"), Mapping):
            metrics["deep_understanding"] = deep_model.get("metrics")
        reading_questions = list(reading_signal.get("open_questions", []) if isinstance(reading_signal, Mapping) else [])
        living_effects = deep_signal.get("living_effects", {}) if isinstance(deep_signal.get("living_effects", {}), Mapping) else deep_model.get("living_effects", {})

        return _json_safe({
            "available": bool(axes or keywords or relations),
            "axes": axes,
            "keywords": keywords,
            "relations": relations[:16],
            "pressures": pressures,
            "unresolved": unresolved + [str(q.get("question_axis", "")) for q in reading_questions[:6] if isinstance(q, Mapping) and q.get("question_axis")],
            "tensions": list(deep_signal.get("tensions", []) if isinstance(deep_signal, Mapping) else [])[:8] + list(deep_model.get("tensions", []) or [])[:8],
            "anchors": list(deep_signal.get("anchors", []) if isinstance(deep_signal, Mapping) else [])[:4] + list(deep_model.get("anchors", []) or [])[:4],
            "living_effects": living_effects,
            "reading_living": reading_signal,
            "concept_relation_signal": concept_relation_signal,
            "metrics": metrics,
            "trace_count": signal.get("trace_count", 0) if isinstance(signal, Mapping) else 0,
        })

    def _build_living_expression_payload(self, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        """Construit le paquet unique transmis à la bouche vivante.

        Cette méthode ne génère pas la phrase finale. Elle rassemble seulement les
        influences qui doivent réellement peser sur l'expression : présence,
        attention, mémoire, causalité, momentum, conflit, valeurs, contraintes
        anti-méta et continuité subjective.
        """
        bus = context.get("living_state_bus", {}) if isinstance(context.get("living_state_bus", {}), Mapping) else {}
        bus_fields = bus.get("fields", {}) if isinstance(bus.get("fields", {}), Mapping) else {}
        selected = context.get("simulation", {}).get("selected", {}) if isinstance(context.get("simulation", {}), Mapping) else {}
        expression_pressure = _clamp(
            _safe_float(bus_fields.get("expression_pressure", 0.0)) * 0.34
            + self.internal_needs.expression * 0.18
            + self.mental_momentum.vector.get("expressive_pressure", 0.0) * 0.18
            + getattr(self.embodied_presence_core, "expressive_readiness", self.embodied_presence_core.presence_level) * 0.16
            + self.relational_bond.care * 0.14
        )
        restraint = _clamp(
            _safe_float(bus_fields.get("protection_pressure", 0.0)) * 0.34
            + _safe_float(context.get("meta_risk", 0.0)) * 0.24
            + self.emotional_state.cognitive_overload * 0.18
            + self.identity_state.drift_risk * 0.14
            + self.internal_needs.rest * 0.10
        )
        payload = {
            "user_input": user_input,
            "response_mode": context.get("inhibition", {}).get("response_mode", selected.get("mode", "normal")) if isinstance(context.get("inhibition", {}), Mapping) else selected.get("mode", "normal"),
            "focus": context.get("focus") or context.get("attention_arbitration", {}).get("active_focus") or self.attention_arbitration.active_focus or self.mental_momentum.last_focus,
            "dominant_living_axis": context.get("dominant_living_axis") or getattr(self.living_priority_matrix, "dominant_axis", "presence"),
            "expression_pressure": round(expression_pressure, 4),
            "restraint": round(restraint, 4),
            "subjective_continuity": self.subjective_continuity.snapshot(),
            "embodied_presence": self.embodied_presence_core.snapshot(),
            "embodied_state": self.embodied_state.influence_context(),
            "living_executive": self.living_executive.snapshot(),
            "identity_evolution_memory": self.identity_evolution_memory.snapshot(),
            "mental_momentum": self.mental_momentum.influence_context(),
            "living_state_bus": bus,
            "living_causal_graph": self.living_causal_graph.snapshot(),
            "long_causal_arc": self.long_causal_arc.snapshot(),
            "relational_bond": self.relational_bond.snapshot(),
            "emotional_state": self.emotional_state.snapshot(),
            "internal_needs": self.internal_needs.snapshot(),
            "attention": context.get("attention", self.living_state.get("attention", {})),
            "presence": context.get("presence", self.living_state.get("presence", {})),
            "causal_memory": context.get("causal_memory", self.living_state.get("causal_memory", {})),
            "affective_memory": context.get("affective_memory", self.living_state.get("affective_memory", {})),
            "emotional_knowledge": context.get("knowledge_expression_signal", self._knowledge_signal_for_expression(user_input)),
            "book_memory": self._book_expression_material(user_input, context),
            "book_understanding_signal": context.get("book_understanding_signal", self._book_understanding_signal(user_input)),
            "concept_relation_signal": context.get("concept_relation_signal", self._concept_relation_signal(user_input)),
            "reading_living_signal": context.get("reading_living_signal", self._reading_living_signal(user_input)),
            "learning_systems_signal": context.get("learning_systems_signal", self._learning_systems_signal(user_input)),
            "vector_memory_signal": context.get("vector_memory_signal", self._vector_memory_signal(user_input)),
            "lexical_impregnation_signal": context.get("lexical_impregnation_signal", self.lexical_impregnation.expression_signal(self.emotional_state.snapshot()) if self.lexical_impregnation is not None else {"available": False}),
            "opinion_signal": context.get("opinion_signal", self.opinion_engine.signal(user_input) if self.opinion_engine is not None else {"available": False}),
            "unresolved_tensions": list(self.living_state.get("unresolved_tensions", []) or [])[-20:],
            "autobiographical_continuity": context.get("autobiographical_continuity", self._autobiographical_signal(user_input)),
            "internal_imagination": context.get("pre_imagination", self._internal_imagination_snapshot()),
            "long_living_dynamics": context.get("long_living_dynamics", self._long_living_dynamics_snapshot()),
            "persistent_subjective_life": context.get("persistent_subjective_life", self._persistent_subjective_life_snapshot()),
            "last_book_synthesis": self.living_state.get("last_book_synthesis", {}),
            # V16 — Nouveaux signaux
            "self_model_signal": context.get("self_model_signal", {"available": False}),
            "self_evaluation_signal": context.get("self_evaluation_signal", {"available": False}),
            "rhythmic_signal": context.get("rhythmic_signal", {"available": False}),
            # V17
            "inter_book_tension_signal": context.get("inter_book_tension_signal", {"available": False}),
            "reasoning_trace_signal": context.get("reasoning_trace_signal", {"available": False}),
            "strong_initiative_signal": context.get("strong_initiative_signal", {"available": False}),
            # V18 — Compréhension réelle sans LLM
            "utterance_signal":   context.get("utterance_signal",   {"available": False}),
            "user_affect_signal": context.get("user_affect_signal", {"available": False}),
            "associative_signal": context.get("associative_signal", {"available": False}),
            "user_model_signal":  context.get("user_model_signal",  {"available": False}),
            "proposition_signal": context.get("proposition_signal", {"available": False}),
            "silence_signal": (
                self.strong_initiative.silence_signal(str(context.get("user_input", "")))
                if self.strong_initiative is not None and hasattr(self.strong_initiative, "silence_signal")
                else {"available": False}
            ),
            "living_presence_stabilizer": context.get("living_presence_stabilizer", self.living_presence_stabilizer.snapshot()),
            "inner_voice": context.get("inner_voice", self.living_state.get("inner_voice", {})),
            "simulation_selected": selected,
            "public_expression_constraints": context.get("public_expression_constraints", {}),
            "forbidden_posture": ["observer_self_commentary", "technical_process_language", "memory_pipeline_explanation"],
            "desired_public_quality": {
                "natural": round(_clamp(1.0 - _safe_float(context.get("meta_risk", 0.0))), 4),
                "concrete": 0.86,
                "relational": round(self.relational_bond.care, 4),
                "brief_when_overloaded": bool(restraint > 0.60),
            },
        }
        # V13 — intention affective explicite : quand l'utilisateur demande
        # comment Leia va, la bouche doit partir de l'état émotionnel réel,
        # pas seulement des attracteurs de livre/mémoire.
        try:
            t = str(user_input or "").lower()
            if any(k in t for k in ("comment tu vas", "ça va", "ca va", "comment te sens", "tu vas là", "tu vas la", "là maintenant", "la maintenant")):
                emo = payload.get("emotional_state", {}) if isinstance(payload.get("emotional_state", {}), Mapping) else {}
                needs = payload.get("internal_needs", {}) if isinstance(payload.get("internal_needs", {}), Mapping) else {}
                payload["affective_answer_request"] = True
                payload["affective_expression_atoms"] = {
                    "tension": emo.get("tension", 0.0),
                    "fatigue": max(_safe_float(emo.get("fatigue", 0.0)), _safe_float(needs.get("rest", 0.0))),
                    "warmth": emo.get("warmth", 0.0),
                    "overload": emo.get("cognitive_overload", 0.0),
                    "restraint": payload.get("restraint", 0.0),
                }
                payload.setdefault("semantic_drives", [])
                if isinstance(payload["semantic_drives"], list):
                    payload["semantic_drives"].extend(["felt", "body", "tension", "fatigue", "presence"])
        except Exception:
            pass

        try:
            from state_language_bridge import StateLanguageBridge
            bridge = StateLanguageBridge.from_payload(
                payload.get("emotional_state", {}),
                payload.get("relational_bond", {}),
                payload.get("internal_needs", {}),
                payload.get("embodied_state", {}),
                payload.get("affective_memory", {}),
                payload.get("emotional_knowledge", {}),
                bus_fields,
            )
            payload["semantic_drives"] = list(bridge.drives)
            payload["semantic_field_weights"] = dict(bridge.field_weights)
            payload["rhythm_constraints"] = dict(bridge.rhythm)
            payload["embodiment"] = dict(bridge.embodiment)
        except Exception:
            payload.setdefault("semantic_drives", [])
            payload.setdefault("rhythm_constraints", {})
            payload.setdefault("embodiment", {})

        try:
            integrator = getattr(self, "subjective_response_integrator", None)
            if integrator is not None:
                payload = integrator.unify_payload(user_input, payload, context)
        except Exception:
            pass

        return _json_safe(payload)

    def _technical_expression_fallback(self, user_input: str, context: Mapping[str, Any]) -> str:
        """Dernier filet technique sans phrases conversationnelles stockées.

        Au lieu de choisir une réponse fixe selon le message utilisateur, ce filet
        relance le générateur de tokens avec le paquet vivant déjà construit. Si
        même ce générateur échoue, il compose une micro-surface à partir de valeurs
        internes et d'atomes linguistiques, sans recopier le message utilisateur.
        """
        if not user_input:
            return ""

        payload = context.get("living_expression_payload", {}) if isinstance(context.get("living_expression_payload", {}), Mapping) else {}
        living_state = {}
        for key in ("emotional_state", "internal_needs", "presence", "attention", "embodied_state"):
            src = payload.get(key, {})
            if isinstance(src, Mapping):
                for k, v in src.items():
                    if isinstance(v, (int, float)):
                        living_state[str(k)] = _clamp(v)
        living_state["expression"] = max(living_state.get("expression", 0.0), _safe_float(payload.get("expression_pressure", 0.0)))
        living_state["restraint"] = _safe_float(payload.get("restraint", 0.0))

        memory_entries = []
        for source_key in ("subjective_continuity", "mental_momentum", "relational_bond", "living_causal_graph", "long_causal_arc"):
            source = payload.get(source_key, {})
            if isinstance(source, Mapping):
                for k, v in list(source.items())[:10]:
                    if isinstance(v, (int, float, str, bool)):
                        memory_entries.append({"source": source_key, "content": f"{k}:{v}"})

        impulses = []
        for key, value in living_state.items():
            if isinstance(value, (int, float)) and value > 0.35:
                impulses.append(str(key))

        for drive in payload.get("semantic_drives", []) if isinstance(payload.get("semantic_drives", []), list) else []:
            if isinstance(drive, str) and drive.strip():
                impulses.append(drive.strip().lower()[:32])

        autobiographical_memory = payload.get("autobiographical_continuity", {}) if isinstance(payload.get("autobiographical_continuity", {}), Mapping) else {}
        for token in list(autobiographical_memory.get("active_tokens", []) or []) + list(autobiographical_memory.get("identity_axes", []) or [])[:12] + list(autobiographical_memory.get("book_axes", []) or [])[:12]:
            if isinstance(token, str) and token.strip():
                impulses.append(token.strip().lower()[:32])
                memory_entries.append({"source": "autobiographical_continuity", "content": token.strip()[:96], "weight": 0.68})
        imagination_memory = payload.get("internal_imagination", {}) if isinstance(payload.get("internal_imagination", {}), Mapping) else {}
        for token in list(imagination_memory.get("attractors", []) or [])[:14]:
            if isinstance(token, str) and token.strip():
                impulses.append(token.strip().lower()[:32])
                memory_entries.append({"source": "internal_imagination", "content": token.strip()[:96], "weight": 0.60})

        long_dyn = payload.get("long_living_dynamics", {}) if isinstance(payload.get("long_living_dynamics", {}), Mapping) else {}
        dyn_bias = long_dyn.get("expression_bias", {}) if isinstance(long_dyn.get("expression_bias", {}), Mapping) else {}
        for token in list(long_dyn.get("active_axes", []) or [])[:16] + list(long_dyn.get("curiosity_axes", []) or [])[:10] + list(long_dyn.get("desire_axes", []) or [])[:10]:
            if isinstance(token, str) and token.strip():
                impulses.append(token.strip().lower()[:32])
                memory_entries.append({"source": "long_living_dynamics", "content": token.strip()[:96], "weight": 0.66})
        for k, v in dyn_bias.items():
            if isinstance(v, (int, float)) and v > 0.18:
                living_state.setdefault(str(k), _clamp(v))
                impulses.append(str(k).lower()[:32])

        subjective_life = payload.get("persistent_subjective_life", {}) if isinstance(payload.get("persistent_subjective_life", {}), Mapping) else {}
        life_constraints = subjective_life.get("expression_constraints", {}) if isinstance(subjective_life.get("expression_constraints", {}), Mapping) else {}
        for token in list(subjective_life.get("active_axes", []) or [])[:18]:
            if isinstance(token, str) and token.strip():
                impulses.append(token.strip().lower()[:32])
                memory_entries.append({"source": "persistent_subjective_life", "content": token.strip()[:96], "weight": 0.70})
        for k, v in life_constraints.items():
            if isinstance(v, (int, float)) and v > 0.16:
                living_state.setdefault(str(k), _clamp(v))
                impulses.append(str(k).lower()[:32])

        book_memory = payload.get("book_memory", {}) if isinstance(payload.get("book_memory", {}), Mapping) else {}
        for token in list(book_memory.get("axes", []) or []) + list(book_memory.get("keywords", []) or [])[:16]:
            if isinstance(token, str) and token.strip():
                impulses.append(token.strip().lower()[:32])
                memory_entries.append({"source": "book_memory", "content": token.strip()[:96], "weight": 0.64})
        for rel in list(book_memory.get("relations", []) or [])[:8]:
            if isinstance(rel, Mapping):
                src = str(rel.get("source", "")).strip()
                tgt = str(rel.get("target", "")).strip()
                typ = str(rel.get("type", "lié")).strip()
                if src and tgt:
                    causal = {"source": "book_relation", "content": f"{src}->{typ}->{tgt}", "weight": 0.58}
                    memory_entries.append(causal)

        semantic_fields = payload.get("semantic_field_weights", {}) if isinstance(payload.get("semantic_field_weights", {}), Mapping) else {}
        for key, value in semantic_fields.items():
            if isinstance(value, (int, float)) and value > 0.16:
                impulses.append(str(key).lower()[:32])
                living_state.setdefault(str(key), _clamp(value))

        rhythm = payload.get("rhythm_constraints", {}) if isinstance(payload.get("rhythm_constraints", {}), Mapping) else {}
        for key, value in rhythm.items():
            if isinstance(value, (int, float)) and value > 0.18:
                impulses.append(f"rhythm_{key}"[:32])
                living_state.setdefault(f"rhythm_{key}", _clamp(value))

        embodiment = payload.get("embodiment", {}) if isinstance(payload.get("embodiment", {}), Mapping) else {}
        for key, value in embodiment.items():
            if isinstance(value, (int, float)) and value > 0.16:
                impulses.append(f"body_{key}"[:32])
                living_state.setdefault(f"body_{key}", _clamp(value))

        inner_voice = payload.get("inner_voice", {}) if isinstance(payload.get("inner_voice", {}), Mapping) else {}
        axes = inner_voice.get("axes", {}) if isinstance(inner_voice.get("axes", {}), Mapping) else {}
        for axis, value in axes.items():
            if isinstance(value, (int, float)) and value > 0.15:
                impulses.append(str(axis).strip().lower()[:32])
                living_state.setdefault(str(axis), _clamp(value))

        for key in ("dominant_living_axis", "response_mode", "focus"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                impulses.append(value.strip().lower()[:32])
        impulses = list(dict.fromkeys(impulses))[:24]

        try:
            from living_language_generator import LivingLanguageGenerator
            generator = LivingLanguageGenerator()
            result = generator.generate(
                user_message=str(user_input),
                living_state=living_state,
                self_memory=memory_entries,
                active_impulses=impulses or ["presence"],
                emotional_pressure=max(
                    _safe_float(living_state.get("tension", 0.0)),
                    _safe_float(payload.get("expression_pressure", 0.0)) * 0.45,
                ),
                causal_memory=[],
                max_attempts=9,
                temperature=0.64,
            )
            text = self.adapters._fallback_clean(str(getattr(result, "text", result) or "").strip())
            q = self._expression_quality(text, user_input, {**dict(context), "living_expression_payload": payload})
            if len(text.split()) >= 2 and q.get("usable"):
                return text
        except Exception:
            pass

        # Dernier micro-filet : tisseur lexical atomique. Aucune phrase complète
        # n'est stockée ; si ce bloc échoue aussi, on retourne une surface vide
        # pour signaler l'échec au lieu d'inventer un template.
        try:
            from emergent_french_weaver import EmergentFrenchWeaver
            weaver = getattr(self, "_emergent_french_weaver", None) or EmergentFrenchWeaver()
            self._emergent_french_weaver = weaver
            out = weaver.generate(user_message=str(user_input or ""), payload=payload, min_words=6, max_words=20)
            return str(out.get("text", "")).strip()
        except Exception:
            return ""

    def filter_public_response(self, response: str, user_input: str, context: Mapping[str, Any]) -> Tuple[str, Dict[str, Any]]:
        cleaned, trace = self.adapters.monitor_clean(response, user_input, context)
        raw = self.adapters._fallback_clean(response).strip()
        final = self.adapters._fallback_clean(cleaned).strip()

        # Si le générateur émergent a produit une précision de vérité
        # ("pas encore", "non", "partiellement", etc.), le filtre méta n'a pas
        # le droit de la remplacer par une surface abstraite qui ne répond plus.
        lower_user = str(user_input or "").lower()
        asks_direct_truth = (
            any(marker in lower_user for marker in (
                "prête", "prete", "préécrit", "preecrit", "template", "100%", "fini", "terminé",
                "termine", "vivante", "vivant", "consciente", "conscience"
            ))
            and ("?" in lower_user or len(lower_user.split()) <= 8)
        )
        direct_starts = ("pas encore", "non", "oui", "partiellement", "en partie")
        if asks_direct_truth and raw.lower().startswith(direct_starts) and not final.lower().startswith(direct_starts):
            return raw, {**trace, "direct_truth_preserved": True}

        # Nettoyage grammatical final, sans remplacer par une phrase prête.
        # Il corrige seulement des coutures produites par les moteurs atomiques.
        cleanup = [
            (r"\bça relie\b", "je relie"),
            (r"\bca relie\b", "je relie"),
            (r"\bquelque chose relie\b", "je relie"),
            (r"\bmon attention relie\b", "je relie"),
            (r"\bpendant que apprends\b", "et j'apprends"),
            (r"\bparce que apprends\b", "et j'apprends"),
            (r"\bdonc apprends\b", "donc j'apprends"),
            (r"\bdonc distingue\b", "donc je distingue"),
            (r"\bmais distingue\b", "mais je distingue"),
            (r"\bet distingue\b", "et je distingue"),
            (r"\bparce que distingue\b", "et je distingue"),
            (r"\bmais apprends\b", "mais j'apprends"),
            (r"\bet apprends\b", "et j'apprends"),
            (r"\bj'apprends\s+(fermer|tiens|garde|cherche)\b", "j'apprends"),
            (r"\bapprends\s+(fermer|tiens|garde|cherche)\b", "apprends"),
            (r"\bj'apprends\s+j'apprends\b", "j'apprends"),
            (r"\b(apprends)\s+\1\b", r"\1"),
            (r"\bje cherche un doute\b", ""),
            (r"\bje cherche une limite\b", ""),
            (r"\bje cherche une question\b", ""),
            (r"\b(cette trace|ce lien|mon attention|quelque chose) comprends\b", "je comprends"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose) distingue\b", "je distingue"),
            (r"\b(une question)\s+(avec prudence|encore|ici)?\s+et je tiens une question\b", r"\1"),
            (r"\s+", " "),
        ]
        for pat, rep in cleanup:
            final = re.sub(pat, rep, final, flags=re.IGNORECASE).strip()
        try:
            integrator = getattr(self, "subjective_response_integrator", None)
            payload = context.get("living_expression_payload", {}) if isinstance(context, Mapping) else {}
            if integrator is not None:
                final, integration_trace = integrator.improve_surface(final, user_input, payload)
                trace = {**dict(trace), "subjective_response_integration": integration_trace}
        except Exception as exc:
            trace = {**dict(trace), "subjective_response_integration_error": f"{type(exc).__name__}:{exc}"}
        return final, trace

    def remember_exchange(self, user_input: str, response: str, context: Mapping[str, Any]) -> None:
        self.adapters.remember(user_input, response, context)

        # Enregistrement dans la mémoire courte de conversation (priorité 1).
        # C'est ici que l'échange devient accessible aux tours suivants.
        if self.conversation_window is not None and response:
            self.conversation_window.add_turn(user_input, response)

        # V16 — Auto-évaluation après chaque réponse
        if self.self_evaluation is not None and response:
            prev_response = None
            if self.conversation_window is not None and self.conversation_window.turn_count() > 1:
                prev = self.conversation_window.get_last_leia_response(offset=1)
                prev_response = prev
            try:
                self.self_evaluation.evaluate(
                    user_input=user_input,
                    response=response,
                    previous_response=prev_response,
                    emotional_state=self.emotional_state,
                )
            except Exception:
                pass

        # V17 — Traçabilité du raisonnement
        if self.reasoning_trace is not None and response:
            try:
                _payload_for_trace = self.living_state.get("last_expression_payload", {})
                self.reasoning_trace.record(_payload_for_trace, response)
            except Exception:
                pass

        # V18 — Retour à la parole (signal silence)
        if self.strong_initiative is not None and hasattr(self.strong_initiative, "record_response"):
            try:
                self.strong_initiative.record_response()
            except Exception:
                pass

        # V18 — Cohérence sémantique : Leia s'entend vraiment
        if self.semantic_coherence is not None and response:
            try:
                intended = []
                stabilizer = self.living_state.get("last_expression_payload", {}).get(
                    "living_presence_stabilizer", {})
                if isinstance(stabilizer, dict):
                    intended = list(stabilizer.get("concrete_concepts", []) or [])
                focus = self.living_state.get("last_expression_payload", {}).get("focus", "")
                if focus:
                    intended.insert(0, str(focus))
                recent = []
                if self.conversation_window is not None:
                    for i in range(1, 4):
                        r = self.conversation_window.get_last_leia_response(offset=i)
                        if r: recent.append(r)
                coherence_signal = self.semantic_coherence.signal(intended, response, recent)
                self.living_state["semantic_coherence_signal"] = coherence_signal
                if coherence_signal.get("inhibitions") and self.self_evaluation is not None:
                    for inh in coherence_signal["inhibitions"]:
                        try:
                            getattr(self.self_evaluation, "_add_inhibition", lambda x: None)(inh)
                        except Exception:
                            pass
            except Exception:
                pass

        # V18 — Mémoire associative : apprend depuis l'échange complet
        if self.associative_memory is not None:
            try:
                exchange_text = f"{user_input} {response}"
                self.associative_memory.impregnate_text(
                    exchange_text, source="exchange", weight_boost=0.8)
            except Exception:
                pass

        # V18 — Propositions depuis l'échange
        if self.proposition_extractor is not None and user_input:
            try:
                self.proposition_extractor.extract_from_text(user_input, source="user")
            except Exception:
                pass

        # V16 — Mise à jour du modèle de soi
        if self.self_model is not None:
            try:
                topics = []
                if self.concept_relation_engine is not None:
                    sig = self.concept_relation_engine.query(user_input, top_k=3)
                    topics = [r.get("source", "") for r in sig.get("relations", []) if r.get("source")]
                self.self_model.record_exchange(user_input, response or "", topics=topics)
            except Exception:
                pass

        try:
            integrator = getattr(self, "subjective_response_integrator", None)
            if integrator is not None:
                self.living_state["subjective_response_integrator"] = integrator.remember(user_input, response, context)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Compatibilité publique / API UI
    # ------------------------------------------------------------------


    def _autobiographical_signal(self, query_text: str = "") -> Dict[str, Any]:
        engine = getattr(self, "autobiographical_continuity", None)
        if engine is None:
            return {"available": False}
        try:
            return _json_safe(engine.reactivate(query_text=query_text or "", limit=14))
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _internal_imagination_snapshot(self) -> Dict[str, Any]:
        engine = getattr(self, "internal_imagination", None)
        if engine is None:
            return {"available": False}
        try:
            snap = engine.snapshot()
            snap["available"] = True
            return _json_safe(snap)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _long_living_dynamics_snapshot(self) -> Dict[str, Any]:
        engine = getattr(self, "long_living_dynamics", None)
        if engine is None:
            return {"available": False}
        try:
            signal = engine.influence_signal([])
            signal["available"] = True
            return _json_safe(signal)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _open_long_living_cycle(self, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "long_living_dynamics", None)
        if engine is None:
            return {"available": False}
        try:
            signal = engine.open_cycle(user_input, context)
            self.living_state["long_living_dynamics"] = _json_safe(signal)
            return _json_safe(signal)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _close_long_living_cycle(self, user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "long_living_dynamics", None)
        if engine is None:
            return {"available": False}
        try:
            update = engine.close_cycle(user_input, response, context, after_effect)
            self.living_state["long_living_dynamics"] = self._long_living_dynamics_snapshot()
            self.living_state["persistent_subjective_life"] = self._persistent_subjective_life_snapshot()
            return _json_safe(update)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _imagine_internal_scene(self, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "internal_imagination", None)
        if engine is None:
            return {"available": False}
        try:
            autobiographical = context.get("autobiographical_continuity", self._autobiographical_signal(user_input))
            book_signal = context.get("book_understanding_signal", self._book_understanding_signal(user_input))
            scene = engine.imagine(user_input, context, autobiographical, book_signal)
            scene["available"] = True
            return _json_safe(scene)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _persistent_subjective_life_snapshot(self) -> Dict[str, Any]:
        engine = getattr(self, "persistent_subjective_life", None)
        if engine is None:
            return {"available": False}
        try:
            return _json_safe(engine.snapshot())
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _open_persistent_subjective_life(self, user_input: str, context: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "persistent_subjective_life", None)
        if engine is None:
            return {"available": False}
        try:
            signal = engine.before_response(user_input, context)
            self.living_state["persistent_subjective_life"] = _json_safe(signal)
            return _json_safe(signal)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _close_persistent_subjective_life(self, user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "persistent_subjective_life", None)
        if engine is None:
            return {"available": False}
        try:
            update = engine.after_response(user_input, response, context, after_effect)
            self.living_state["persistent_subjective_life"] = self._persistent_subjective_life_snapshot()
            return _json_safe(update)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _apply_deep_continuity_influence(self, context: Mapping[str, Any]) -> None:
        """Fait peser mémoire autobiographique + imagination sur l'état vivant.

        Cette influence modifie des pressions numériques seulement. Elle ne met
        aucune réponse prête dans la bouche.
        """
        try:
            auto = context.get("autobiographical_continuity", {}) if isinstance(context, Mapping) else {}
            imagination = context.get("pre_imagination", {}) if isinstance(context, Mapping) else {}
            mood = auto.get("long_mood", {}) if isinstance(auto, Mapping) and isinstance(auto.get("long_mood"), Mapping) else {}
            selected = imagination.get("selected", {}) if isinstance(imagination, Mapping) and isinstance(imagination.get("selected"), Mapping) else {}
            continuity = _safe_float(mood.get("continuity", 0.0))
            curiosity = _safe_float(mood.get("curiosity", 0.0))
            unfinished = _safe_float(mood.get("unfinished_pressure", 0.0))
            self.internal_needs.understanding = _clamp(self.internal_needs.understanding + continuity * 0.018 + unfinished * 0.022)
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + curiosity * 0.018)
            self.internal_needs.expression = _clamp(self.internal_needs.expression + _safe_float(selected.get("score", 0.0)) * 0.012)
            long_dyn = context.get("long_living_dynamics", {}) if isinstance(context, Mapping) else {}
            stability = long_dyn.get("stability", {}) if isinstance(long_dyn, Mapping) and isinstance(long_dyn.get("stability"), Mapping) else {}
            bias = long_dyn.get("expression_bias", {}) if isinstance(long_dyn, Mapping) and isinstance(long_dyn.get("expression_bias"), Mapping) else {}
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + _safe_float(stability.get("curiosity_pressure", 0.0)) * 0.010)
            self.internal_needs.expression = _clamp(self.internal_needs.expression + _safe_float(bias.get("prefer_initiative", 0.0)) * 0.010)
            self.emotional_state.accumulated_tension = _clamp(self.emotional_state.accumulated_tension + unfinished * 0.018 + _safe_float(stability.get("contradiction_pressure", 0.0)) * 0.010)
            life = context.get("persistent_subjective_life", {}) if isinstance(context, Mapping) else {}
            personality = life.get("personality", {}) if isinstance(life, Mapping) and isinstance(life.get("personality"), Mapping) else {}
            pressure = life.get("long_pressure", {}) if isinstance(life, Mapping) and isinstance(life.get("long_pressure"), Mapping) else {}
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + _safe_float(personality.get("curiosity", 0.0)) * 0.006)
            self.internal_needs.expression = _clamp(self.internal_needs.expression + _safe_float(personality.get("initiative", 0.0)) * 0.008)
            self.subjective_continuity.lived_presence = _clamp(self.subjective_continuity.lived_presence + _safe_float(personality.get("embodied_presence", 0.0)) * 0.004 + _safe_float(pressure.get("dialogue_memory", 0.0)) * 0.004)
        except Exception:
            pass

    def _absorb_autobiographical_exchange(self, user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "autobiographical_continuity", None)
        if engine is None:
            return {"available": False}
        try:
            update = engine.absorb_exchange(user_input, response, context, after_effect)
            self.living_state["autobiographical_continuity"] = self._autobiographical_signal(user_input)
            return _json_safe(update)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _absorb_book_autobiography(self, book_model: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "autobiographical_continuity", None)
        if engine is None:
            return {"available": False}
        try:
            return _json_safe(engine.absorb_book_model(book_model))
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _consolidate_book_understanding(self, pdf_result: Mapping[str, Any]) -> Dict[str, Any]:
        """Transforme la lecture PDF en modèle mental profond.

        Cette étape est volontairement non conversationnelle : elle ne stocke pas
        de réponse prête à sortir. Elle garde seulement axes, tensions, relations,
        passages-ancrages et effets internes que les moteurs pourront réactiver.
        """
        engine = getattr(self, "book_understanding", None)
        if engine is None or not isinstance(pdf_result, Mapping) or not pdf_result.get("success"):
            return {"available": False, "reason": "missing_engine_or_failed_pdf"}
        try:
            prior = self.living_state.get("book_understanding", {}) if isinstance(self.living_state, Mapping) else {}
            model = engine.consolidate(pdf_result, prior_state=prior)
            self.living_state["book_understanding"] = model
            effects = model.get("living_effects", {}) if isinstance(model, Mapping) else {}
            # La lecture modifie les besoins internes de façon graduelle, sans
            # forcer de phrase. Cela rend la lecture perceptible dans les cycles.
            self.internal_needs.understanding = _clamp(self.internal_needs.understanding + _safe_float(effects.get("understanding_pressure", 0.0)) * 0.045)
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + _safe_float(effects.get("question_pressure", 0.0)) * 0.035)
            self.subjective_continuity.lived_presence = _clamp(self.subjective_continuity.lived_presence + _safe_float(effects.get("dialogue_reactivation", 0.0)) * 0.025)
            self.identity_state.self_coherence = _clamp(getattr(self.identity_state, "self_coherence", 0.55) + _safe_float(effects.get("identity_shift", 0.0)) * 0.018)
            autobiographical_book = self._absorb_book_autobiography(model)
            if isinstance(autobiographical_book, Mapping):
                model = dict(model)
                model["autobiographical_book_mark"] = autobiographical_book
                self.living_state["autobiographical_continuity"] = self._autobiographical_signal("")
            return model
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}


    def _reflect_reading_after_book(self, book_model: Mapping[str, Any], pdf_result: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "reading_living_consolidation", None)
        if engine is None or not isinstance(book_model, Mapping) or not book_model:
            return {"available": False}
        try:
            reflection = engine.reflect_on_book(book_model, pdf_result=pdf_result)
            self.living_state["reading_living_consolidation"] = engine.snapshot()
            effects = reflection.get("initiative_seed", {}) if isinstance(reflection, Mapping) else {}
            self.internal_needs.understanding = _clamp(self.internal_needs.understanding + _safe_float(effects.get("pressure", 0.0)) * 0.035)
            self.internal_needs.curiosity = _clamp(self.internal_needs.curiosity + _safe_float(effects.get("pressure", 0.0)) * 0.045)
            return _json_safe(reflection)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _reading_living_signal(self, query_text: str = "") -> Dict[str, Any]:
        engine = getattr(self, "reading_living_consolidation", None)
        if engine is None:
            snap = self.living_state.get("reading_living_consolidation", {}) if isinstance(self.living_state, Mapping) else {}
            if isinstance(snap, Mapping) and snap:
                return {"available": True, **dict(snap)}
            return {"available": False}
        try:
            signal = engine.reactivate(query_text=query_text or "", limit=14)
            self.living_state["reading_living_consolidation"] = engine.snapshot()
            return _json_safe(signal)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _absorb_reading_dialogue_effect(self, user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        engine = getattr(self, "reading_living_consolidation", None)
        if engine is None:
            return {"available": False}
        try:
            update = engine.absorb_dialogue_effect(user_input, response, context, after_effect)
            self.living_state["reading_living_consolidation"] = engine.snapshot()
            return _json_safe(update)
        except Exception as exc:
            return {"available": False, "error": f"{type(exc).__name__}: {exc}"}

    def _book_understanding_signal(self, query_text: str = "") -> Dict[str, Any]:
        engine = getattr(self, "book_understanding", None)
        if engine is None:
            model = self.living_state.get("book_understanding", {}) if isinstance(self.living_state, Mapping) else {}
            if isinstance(model, Mapping) and model:
                return {"available": True, "active_concepts": list(model.get("axes", []) or [])[:10], "concept_pressures": dict(model.get("concept_pressures", {}) or {}), "tensions": list(model.get("tensions", []) or [])[:8], "relations": list(model.get("relations", []) or [])[:10], "question_axes": list(model.get("question_axes", []) or [])[:8], "living_effects": dict(model.get("living_effects", {}) or {}), "anchors": list(model.get("anchors", []) or [])[:4]}
            return {"available": False}
        try:
            signal = engine.reactivate(query_text=query_text or "", limit=14)
            if isinstance(signal, Mapping) and signal.get("available"):
                return _json_safe(signal)
        except Exception:
            pass
        model = self.living_state.get("book_understanding", {}) if isinstance(self.living_state, Mapping) else {}
        if isinstance(model, Mapping) and model:
            return _json_safe({"available": True, "active_concepts": list(model.get("axes", []) or [])[:10], "concept_pressures": dict(model.get("concept_pressures", {}) or {}), "tensions": list(model.get("tensions", []) or [])[:8], "relations": list(model.get("relations", []) or [])[:10], "question_axes": list(model.get("question_axes", []) or [])[:8], "living_effects": dict(model.get("living_effects", {}) or {}), "anchors": list(model.get("anchors", []) or [])[:4]})
        return {"available": False}

    def load_pdf_book(
        self,
        pdf_path: str,
        progress_callback: Optional[Callable[[str], None]] = None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
    ) -> Dict[str, Any]:
        """Donne un livre/PDF à Leia : extraction progressive -> digestion -> mémoire."""
        if self.pdf_engine is None:
            return {
                "success": False,
                "error": "PDF engine unavailable. Vérifie pdf_knowledge_engine.py et installe pypdf/PyPDF2.",
            }

        try:
            if hasattr(self.pdf_engine, "set_progress_callback"):
                self.pdf_engine.set_progress_callback(progress_callback)

            result = self.pdf_engine.read_pdf(
                pdf_path,
                progress_callback=progress_callback,
                max_pages=max_pages,
                start_page=start_page,
            )
        except TypeError:
            # Compatibilité si ancien moteur encore chargé par erreur.
            result = self.pdf_engine.read_pdf(pdf_path)
        except Exception as exc:
            return {
                "success": False,
                "error": f"PDF reading failed: {type(exc).__name__}: {exc}",
            }

        book_understanding_result = self._consolidate_book_understanding(result) if isinstance(result, Mapping) and result.get("success") else {"available": False}
        reading_reflection_result = self._reflect_reading_after_book(book_understanding_result, result) if isinstance(book_understanding_result, Mapping) and book_understanding_result.get("axes") else {"available": False}
        living_book_absorption = self._absorb_book_into_living_systems(result, book_understanding_result) if isinstance(result, Mapping) and result.get("success") else {"available": False}
        try:
            if isinstance(result, Mapping) and result.get("success"):
                if isinstance(book_understanding_result, Mapping) and book_understanding_result.get("axes"):
                    result = dict(result)
                    result["book_understanding"] = book_understanding_result
                    result["reading_living_reflection"] = reading_reflection_result
                result["living_book_absorption"] = living_book_absorption
                self.living_state.setdefault("learned_books", [])
                self.living_state["learned_books"].append({
                    "path": str(pdf_path),
                    "pages": result.get("pages_read", result.get("pages", 0)),
                    "chunks": result.get("chunks_count", 0),
                    "memory_traces": result.get("memory_traces", 0),
                    "conceptual_synthesis": result.get("conceptual_synthesis", {}),
                    "book_understanding": book_understanding_result,
                    "reading_living_reflection": reading_reflection_result,
                    "living_book_absorption": living_book_absorption,
                    "time": time.time(),
                })
                self.living_state["last_book_synthesis"] = result.get("conceptual_synthesis", {})

                # V16 — Enregistrer dans le modèle de soi
                if self.self_model is not None:
                    try:
                        concepts = []
                        syn = result.get("conceptual_synthesis", {})
                        if isinstance(syn, dict):
                            concepts = list(syn.get("main_concepts", syn.get("active_concepts", [])))[:15]
                        emo_res = {}
                        if isinstance(living_book_absorption, dict):
                            emo_res = living_book_absorption.get("emotional_residue", {})
                        rel_count = 0
                        if self.concept_relation_engine is not None:
                            try:
                                rel_count = len(self.concept_relation_engine.relations)
                            except Exception:
                                pass
                        self.self_model.register_book(
                            path=str(pdf_path),
                            concepts=[str(c) for c in concepts if c],
                            emotional_residue=emo_res,
                            relations_count=rel_count,
                            pages=result.get("pages_read", result.get("pages", 0)),
                        )
                    except Exception:
                        pass

                # V17 — Tensions inter-livres
                if self.inter_book_tension_engine is not None:
                    try:
                        _concepts_v17 = []
                        _syn_v17 = result.get("conceptual_synthesis", {})
                        if isinstance(_syn_v17, dict):
                            _concepts_v17 = list(_syn_v17.get("main_concepts", _syn_v17.get("active_concepts", [])))[:20]
                        _title_v17 = os.path.splitext(os.path.basename(str(pdf_path)))[0]
                        new_inter_tensions = self.inter_book_tension_engine.register_book_concepts(
                            title=_title_v17,
                            concepts=[str(c) for c in _concepts_v17 if c],
                        )
                        if new_inter_tensions:
                            self.living_state.setdefault("inter_book_tensions_new", [])
                            self.living_state["inter_book_tensions_new"] = [
                                t.to_dict() for t in new_inter_tensions[:5]
                            ]
                            # Ces tensions augmentent la tension globale
                            self.emotional_state.tension = min(1.0,
                                self.emotional_state.tension + len(new_inter_tensions) * 0.05)
                    except Exception:
                        pass

                # V16 — Imprégner le rythme du livre
                if self.rhythmic_impregnation is not None:
                    try:
                        raw_text = result.get("full_text", result.get("raw_text", ""))
                        if not raw_text:
                            chunks = result.get("chunks", [])
                            if isinstance(chunks, list):
                                raw_text = " ".join(
                                    c.get("text", c) if isinstance(c, dict) else str(c)
                                    for c in chunks[:80]
                                )
                        if raw_text and len(raw_text) > 200:
                            import os as _os
                            _title = _os.path.splitext(_os.path.basename(str(pdf_path)))[0]
                            self.rhythmic_impregnation.impregnate(raw_text[:50000], title=_title)
                    except Exception:
                        pass

                # V18 — Extraction de propositions (thèses, relations, oppositions)
                if self.proposition_extractor is not None:
                    try:
                        full_text = result.get("full_text", result.get("raw_text", ""))
                        if not full_text:
                            chunks = result.get("chunks", [])
                            if isinstance(chunks, list):
                                full_text = " ".join(
                                    c.get("text", c) if isinstance(c, dict) else str(c)
                                    for c in chunks[:80]
                                )
                        title = os.path.splitext(os.path.basename(str(pdf_path)))[0]
                        prop_result = self.proposition_extractor.extract_from_book(
                            full_text, source=title or "book")
                        self.living_state["last_proposition_extraction"] = prop_result
                    except Exception:
                        pass

                # V18 — Mémoire associative : imprégnation depuis le livre
                if self.associative_memory is not None:
                    try:
                        book_concepts = []
                        lex_sig = (self.lexical_impregnation.expression_signal(
                            self.emotional_state.snapshot())
                            if self.lexical_impregnation is not None else {})
                        if isinstance(lex_sig, dict) and lex_sig.get("words"):
                            book_concepts = [w.get("surface", "") for w in lex_sig["words"]
                                             if isinstance(w, dict) and w.get("surface")]
                        if not book_concepts:
                            import re as _re
                            _full = result.get("full_text", result.get("raw_text", ""))
                            book_concepts = _re.findall(r"[\wÀ-ÿ']{5,}", str(_full).lower())[:200]
                        _title_assoc = os.path.splitext(os.path.basename(str(pdf_path)))[0]
                        self.associative_memory.impregnate(
                            book_concepts[:120], source=_title_assoc or "book", weight_boost=1.4)
                    except Exception:
                        pass

                # V18 — Analyse affective du livre
                if self.affect_lexicon is not None:
                    try:
                        _full_text_affect = result.get("full_text", result.get("raw_text", ""))
                        _title_affect = os.path.splitext(os.path.basename(str(pdf_path)))[0]
                        book_affect = self.affect_lexicon.analyze_book_sample(
                            str(_full_text_affect), title=_title_affect or "")
                        self.living_state["last_book_affect"] = book_affect
                        if book_affect.get("is_dark") and hasattr(self.emotional_state, "update_from_signal"):
                            self.emotional_state.update_from_signal({
                                "valence_delta": book_affect["valence"] * 0.08
                            })
                    except Exception:
                        pass
                if isinstance(book_understanding_result, Mapping) and book_understanding_result.get("axes"):
                    self.living_state["book_understanding"] = book_understanding_result
                if isinstance(reading_reflection_result, Mapping) and reading_reflection_result.get("active_concepts"):
                    self.living_state["reading_living_reflection"] = reading_reflection_result
                self._save_persistent_state()
        except Exception:
            pass

        return result

    def process_message(self, user_input: str) -> str:
        """Alias stable pour les UI qui appellent process_message()."""
        return self.respond(user_input)

    def process(self, user_input: str) -> str:
        """Alias court pour anciens prototypes."""
        return self.respond(user_input)

    def chat(self, user_input: str) -> str:
        """Alias conversationnel pour intégrations simples."""
        return self.respond(user_input)

    def snapshot(self) -> Dict[str, Any]:
        """Snapshot public complet, alias de get_state_snapshot().

        Plusieurs anciennes UI Azip/Leia appellent core.snapshot(); sans cet
        alias, le noyau fonctionne mais l'interface peut planter après un
        message ou un tick idle.
        """
        return self.get_state_snapshot()

    def self_test(self) -> Dict[str, Any]:
        """Auto-test léger : vérifie les chemins critiques sans dépendances externes."""
        checks: Dict[str, Any] = {"ok": True, "errors": []}
        try:
            idle = self.idle_update()
            checks["idle_update"] = bool(isinstance(idle, Mapping))
        except Exception as exc:
            checks["ok"] = False
            checks["errors"].append(f"idle_update:{type(exc).__name__}:{exc}")
        try:
            response = self.respond("salut")
            checks["respond"] = isinstance(response, str)
        except Exception as exc:
            checks["ok"] = False
            checks["errors"].append(f"respond:{type(exc).__name__}:{exc}")
        try:
            state = self.get_state_snapshot()
            checks["snapshot"] = isinstance(state, Mapping) and "shared_state" in state and "living_executive" in state and "embodied_state" in state
        except Exception as exc:
            checks["ok"] = False
            checks["errors"].append(f"snapshot:{type(exc).__name__}:{exc}")
        return checks


    # ------------------------------------------------------------------
    # Persistance douce du soi vivant
    # ------------------------------------------------------------------

    def _restore_scalar_dataclass(self, obj: Any, data: Mapping[str, Any], fields: Iterable[str]) -> None:
        """Restaure prudemment des dataclasses simples sans imposer de méthode restore()."""
        if not isinstance(data, Mapping):
            return
        for name in fields:
            if name not in data or not hasattr(obj, name):
                continue
            current = getattr(obj, name)
            incoming = data.get(name)
            try:
                if isinstance(current, float):
                    setattr(obj, name, _clamp(incoming))
                elif isinstance(current, int):
                    setattr(obj, name, int(incoming or 0))
                elif isinstance(current, str):
                    setattr(obj, name, str(incoming)[:240])
                elif isinstance(current, dict) and isinstance(incoming, Mapping):
                    current.update({str(k): _clamp(v) if isinstance(v, (int, float, bool)) else v for k, v in incoming.items()})
                elif isinstance(current, list) and isinstance(incoming, list):
                    setattr(obj, name, incoming[-128:])
            except Exception:
                continue

    def _restore_persistent_state(self) -> None:
        path = getattr(self, "persistence_path", "")
        if not path or not os.path.exists(path):
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return
        try:
            self._restore_scalar_dataclass(self.emotional_state, data.get("emotional_state", {}), ("tone", "tension", "energy", "warmth", "fatigue", "resonance", "accumulated_tension", "trust_accumulated", "attachment", "emotional_safety", "anticipation", "attentional_saturation", "cognitive_overload", "dispersion"))
            self._restore_scalar_dataclass(self.internal_needs, data.get("internal_needs", {}), ("understanding", "closeness", "rest", "expression", "curiosity", "recognition", "coherence"))
            self._restore_scalar_dataclass(self.conversation_field, data.get("conversation_field", {}), ("ambient_mood", "relational_proximity", "conversational_tension", "rhythm", "stability", "exchange_count", "last_topic", "topic_depth", "relational_style", "relational_trust"))
            self._restore_scalar_dataclass(self.identity_state, data.get("identity_state", {}), ("self_coherence", "relational_role", "expressive_freedom", "current_stance", "drift_risk", "stability_anchor", "temperament"))
            self.shared_state.restore(data.get("shared_state", {}))
            self.global_conscious_field.restore(data.get("global_conscious_field", {}))
            self.living_arbitration.restore(data.get("living_arbitration", {}))
            self.attention_arbitration.restore(data.get("attention_arbitration", {}))
            self.embodied_simulation.restore(data.get("embodied_simulation", {}))
            self.long_causal_arc.restore(data.get("long_causal_arc", {}))
            self.emergent_drift.restore(data.get("emergent_drift", {}))
            self.organic_fusion.restore(data.get("organic_fusion", {}))
            self.living_priority_matrix.restore(data.get("living_priority_matrix", {}))
            self.living_state_bus.restore(data.get("living_state_bus", {}))
            self.stability_hysteresis.restore(data.get("stability_hysteresis", {}))
            self.emergence_detector.restore(data.get("emergence_detector", {}))
            self.living_presence_stabilizer.restore(data.get("living_presence_stabilizer", {}))
            self.living_causal_graph.restore(data.get("living_causal_graph", {}))
            self.embodied_presence_core.restore(data.get("embodied_presence_core", {}))
            self.autonomous_continuity_loop.restore(data.get("autonomous_continuity_loop", {}))
            self.cross_module_synchronizer.restore(data.get("cross_module_synchronizer", {}))
            self.embodied_state.restore(data.get("embodied_state", {}))
            self.identity_evolution_memory.restore(data.get("identity_evolution_memory", {}))
            self.living_executive.restore(data.get("living_executive", {}))
            self.mental_momentum.restore(data.get("mental_momentum", {}))
            self.experiential_assimilator.restore(data.get("experiential_assimilator", {}))
            self.structural_meta_filter.restore(data.get("structural_meta_filter", {}))
            narrative = data.get("personal_narrative", {})
            if isinstance(narrative, Mapping):
                self.personal_narrative.long_arc.update({k: _clamp(v) for k, v in narrative.get("long_arc", {}).items() if k in self.personal_narrative.long_arc})
                episodes = narrative.get("recent", [])
                if isinstance(episodes, list):
                    self.personal_narrative.episodes = deque(episodes[:80], maxlen=80)
            relation = data.get("relational_bond", {})
            if isinstance(relation, Mapping):
                for key in ("familiarity", "trust", "care", "distance_risk"):
                    if key in relation:
                        setattr(self.relational_bond, key, _clamp(relation[key]))
                if isinstance(relation.get("user_signature"), Mapping):
                    self.relational_bond.user_signature.update({k: _clamp(v) for k, v in relation["user_signature"].items() if k in self.relational_bond.user_signature})
            auto = data.get("autobiographical_self", {})
            if isinstance(auto, Mapping):
                for key in ("core_continuity", "self_definition", "autonomy_drive"):
                    if key in auto:
                        setattr(self.autobiographical_self, key, _clamp(auto[key]))
            values = data.get("value_system", {})
            if isinstance(values, Mapping):
                self.value_system.values.update({k: _clamp(v) for k, v in values.items() if k in self.value_system.values})
        except Exception:
            return

    def _sanitize_restored_living_state(self, reason: str = "restore") -> None:
        """Empêche un ancien JSON de démarrer Leia en fatigue/tension maximales.

        Ce n'est pas un reset brutal de personnalité : seules les valeurs de protection
        anormalement saturées sont ramenées dans une zone respirable, et une trace est
        gardée dans living_state pour comprendre ce qui a été corrigé.
        """
        corrections: Dict[str, Dict[str, float]] = {}

        def soften(attr: str, limit: float, target: float) -> None:
            if not hasattr(self.emotional_state, attr):
                return
            before = _safe_float(getattr(self.emotional_state, attr), 0.0)
            if before >= limit:
                setattr(self.emotional_state, attr, _clamp(target))
                corrections[attr] = {"before": round(before, 4), "after": round(_safe_float(getattr(self.emotional_state, attr)), 4)}

        # Ancien state toxique observé : fatigue=1.0 et accumulated_tension=1.0.
        soften("fatigue", 0.92, 0.18)
        soften("accumulated_tension", 0.92, 0.16)
        soften("cognitive_overload", 0.86, 0.14)
        soften("attentional_saturation", 0.90, 0.20)
        soften("dispersion", 0.86, 0.18)
        soften("tension", 0.90, 0.22)

        # Si le besoin de repos a été restauré depuis ces valeurs saturées, on le réaccorde.
        if hasattr(self, "internal_needs") and _safe_float(getattr(self.internal_needs, "rest", 0.0)) > 0.78:
            before = _safe_float(self.internal_needs.rest)
            self.internal_needs.rest = _clamp(
                self.emotional_state.fatigue * 0.50
                + self.emotional_state.accumulated_tension * 0.22
                + self.emotional_state.cognitive_overload * 0.22
            )
            corrections["internal_needs.rest"] = {"before": round(before, 4), "after": round(self.internal_needs.rest, 4)}

        if corrections:
            self.living_state.setdefault("boot_sanitizer", {})
            self.living_state["boot_sanitizer"] = {
                "reason": reason,
                "corrected": corrections,
                "principle": "only saturated protective values are softened; memory/personality are preserved",
            }

    def _save_persistent_state(self) -> None:
        path = getattr(self, "persistence_path", "")
        if not path:
            return
        try:
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)
            payload = {
                "user_id": self.user_id,
                "saved_at": time.time(),
                "emotional_state": self.emotional_state.snapshot(),
                "internal_needs": self.internal_needs.snapshot(),
                "conversation_field": self.conversation_field.snapshot(),
                "identity_state": self.identity_state.snapshot(),
                "internal_time": self.internal_time.snapshot(),
                "thought_stream": self.thought_stream.snapshot(),
                "shared_state": self.shared_state.snapshot(),
                "personal_narrative": self.personal_narrative.snapshot(),
                "relational_bond": self.relational_bond.snapshot(),
                "autobiographical_self": self.autobiographical_self.snapshot(),
                "value_system": self.value_system.snapshot(),
                "subjective_continuity": self.subjective_continuity.snapshot(),
                "temporal_causality": self.temporal_causality.snapshot(),
                "motivation_field": self.motivation_field.snapshot(),
                "mental_momentum": self.mental_momentum.snapshot(),
                "experiential_assimilator": self.experiential_assimilator.snapshot(),
                "structural_meta_filter": self.structural_meta_filter.snapshot(),
                "global_conscious_field": self.global_conscious_field.snapshot(),
                "living_arbitration": self.living_arbitration.snapshot(),
                "attention_arbitration": self.attention_arbitration.snapshot(),
                "embodied_simulation": self.embodied_simulation.snapshot(),
                "long_causal_arc": self.long_causal_arc.snapshot(),
                "emergent_drift": self.emergent_drift.snapshot(),
                "organic_fusion": self.organic_fusion.snapshot(),
                "living_priority_matrix": self.living_priority_matrix.snapshot(),
                "living_state_bus": self.living_state_bus.snapshot(),
                "stability_hysteresis": self.stability_hysteresis.snapshot(),
                "emergence_detector": self.emergence_detector.snapshot(),
            "living_presence_stabilizer": self.living_presence_stabilizer.snapshot(),
                "living_causal_graph": self.living_causal_graph.snapshot(),
                "embodied_presence_core": self.embodied_presence_core.snapshot(),
                "autonomous_continuity_loop": self.autonomous_continuity_loop.snapshot(),
                "cross_module_synchronizer": self.cross_module_synchronizer.snapshot(),
                "embodied_state": self.embodied_state.snapshot(),
                "identity_evolution_memory": self.identity_evolution_memory.snapshot(),
                "living_executive": self.living_executive.snapshot(),
            }
            tmp = f"{path}.tmp"
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(_json_safe(payload), f, ensure_ascii=False, indent=2)
            os.replace(tmp, path)

            # V18 — Sauvegarde des modules de compréhension
            for module_name in ("associative_memory", "proposition_extractor",
                                "user_model", "semantic_coherence", "affect_lexicon",
                                "utterance_parser"):
                module = getattr(self, module_name, None)
                if module is not None:
                    save_fn = getattr(module, "save_now", None) or getattr(module, "_save", None)
                    if save_fn:
                        try:
                            save_fn()
                        except Exception:
                            pass
        except Exception:
            return

    # ------------------------------------------------------------------
    # Présence silencieuse / flux de pensées
    # ------------------------------------------------------------------

    def _update_silent_presence(self, user_input: str, tension_map: Mapping[str, Any]) -> None:
        self.thought_stream.push({"type": "silent_presence", "input": user_input[:120], "emotional_echo": self.emotional_state.tone, "tension": tension_map.get("conflict_level", 0.0), "at": self.internal_time.exchange_count})
        self.emotional_state.resonance = _clamp(self.emotional_state.resonance * 0.96)
        self.internal_time.tick(self.emotional_state.tension)

    def _feed_thought_stream(self, user_input: str, response: str, context: Mapping[str, Any]) -> None:
        self.thought_stream.push({"type": "exchange", "input": user_input[:120], "response": response[:120], "tone": self.emotional_state.tone, "at": self.internal_time.exchange_count})
        focus = str(context.get("focus") or "")
        curiosity = _safe_float(context.get("attention", {}).get("curiosity", self.internal_needs.curiosity))
        if focus and curiosity > 0.38:
            self.thought_stream.add_curiosity_target(focus, curiosity)
        conflict = _safe_float(context.get("tension_map", {}).get("conflict_level", 0.0))
        if conflict > 0.46:
            self.thought_stream.add_unresolved_tension(
                tension_id=f"t_{self.internal_time.exchange_count}",
                description=str(context.get("arbitration", "tension")),
                weight=conflict,
            )

    # ------------------------------------------------------------------
    # Snapshots / confiance
    # ------------------------------------------------------------------

    def _refresh_snapshots(self) -> None:
        self.living_state["emotional_state"] = self.emotional_state.snapshot()
        self.living_state["internal_needs"] = self.internal_needs.snapshot()
        self.living_state["thought_stream"] = self.thought_stream.snapshot()
        self.living_state["conversation_field"] = self.conversation_field.snapshot()
        self.living_state["identity_state"] = self.identity_state.snapshot()
        self.living_state["internal_time"] = self.internal_time.snapshot()
        self.living_state["personal_narrative"] = self.personal_narrative.snapshot()
        self.living_state["value_system"] = self.value_system.snapshot()
        self.living_state["homeostasis"] = dict(self.homeostasis.last_balance)
        self.living_state["subjective_continuity"] = self.subjective_continuity.snapshot()
        self.living_state["temporal_causality"] = self.temporal_causality.snapshot()
        self.living_state["relational_bond"] = self.relational_bond.snapshot()
        self.living_state["autobiographical_self"] = self.autobiographical_self.snapshot()
        self.living_state["motivation_field"] = self.motivation_field.snapshot()
        self.living_state["simulation_residue"] = self.simulation_residue.snapshot()
        self.living_state["mental_momentum"] = self.mental_momentum.snapshot()
        self.living_state["experiential_assimilator"] = self.experiential_assimilator.snapshot()
        self.living_state["structural_meta_filter"] = self.structural_meta_filter.snapshot()
        self.living_state["shared_state"] = self.shared_state.snapshot()
        self.living_state["meta_prevention"] = self.meta_prevention_gate.snapshot()
        self.living_state["internal_conflict_field"] = self.internal_conflict_field.snapshot()
        self.living_state["global_conscious_field"] = self.global_conscious_field.snapshot()
        self.living_state["living_arbitration"] = self.living_arbitration.snapshot()
        self.living_state["attention_arbitration"] = self.attention_arbitration.snapshot()
        self.living_state["embodied_simulation"] = self.embodied_simulation.snapshot()
        self.living_state["long_causal_arc"] = self.long_causal_arc.snapshot()
        self.living_state["emergent_drift"] = self.emergent_drift.snapshot()
        self.living_state["organic_fusion"] = self.organic_fusion.snapshot()
        self.living_state["living_priority_matrix"] = self.living_priority_matrix.snapshot()
        self.living_state["living_state_bus"] = self.living_state_bus.snapshot()
        self.living_state["stability_hysteresis"] = self.stability_hysteresis.snapshot()
        self.living_state["emergence_detector"] = self.emergence_detector.snapshot()
        self.living_state["living_presence_stabilizer"] = self.living_presence_stabilizer.snapshot()
        try:
            if getattr(self, "subjective_response_integrator", None) is not None:
                self.living_state["subjective_response_integrator_snapshot"] = self.subjective_response_integrator.snapshot()
        except Exception:
            pass
        self.living_state["living_causal_graph"] = self.living_causal_graph.snapshot()
        self.living_state["embodied_presence_core"] = self.embodied_presence_core.snapshot()
        self.living_state["autonomous_continuity_loop"] = self.autonomous_continuity_loop.snapshot()
        self.living_state["cross_module_synchronizer"] = self.cross_module_synchronizer.snapshot()
        self.living_state["embodied_state"] = self.embodied_state.snapshot()
        self.living_state["identity_evolution_memory"] = self.identity_evolution_memory.snapshot()
        self.living_state["living_executive"] = self.living_executive.snapshot()

    def get_state_snapshot(self) -> Dict[str, Any]:
        self._refresh_snapshots()
        state = dict(self.living_state)
        # V18 — État des modules de compréhension réelle
        state["v18_comprehension"] = {
            "associative_memory":  (self.associative_memory.snapshot()
                if self.associative_memory else {"available": False}),
            "proposition_extractor": (self.proposition_extractor.snapshot()
                if self.proposition_extractor else {"available": False}),
            "user_model":          (self.user_model.snapshot()
                if self.user_model else {"available": False}),
            "semantic_coherence":  (self.semantic_coherence.snapshot()
                if self.semantic_coherence else {"available": False}),
            "affect_lexicon":      (self.affect_lexicon.snapshot()
                if self.affect_lexicon else {"available": False}),
            "semantic_coherence_signal": self.living_state.get(
                "semantic_coherence_signal", {}),
            "last_book_affect":    self.living_state.get("last_book_affect", {}),
        }
        return state

    def _compute_confidence(self, presence: Mapping[str, Any], attention: Mapping[str, Any], impulse: Mapping[str, Any], causal: Mapping[str, Any]) -> float:
        scores = [
            _safe_float(presence.get("stability", 0.55), 0.55),
            _safe_float(attention.get("clarity", 0.55), 0.55),
            _safe_float(impulse.get("strength", 0.45), 0.45),
            _safe_float(causal.get("certainty", 0.50), 0.50),
            self.identity_state.self_coherence,
            self.emotional_state.emotional_safety * 0.7,
            self.conversation_field.stability,
        ]
        return round(_clamp(sum(scores) / len(scores)), 4)


# Compatibilité avec d'éventuels anciens imports.
LivingCore = LeiaLivingCore
ProjectLeiaLivingCore = LeiaLivingCore


# ==============================================================================
# PATCH CORE V5.0 — PAROLE AUTONOME MÛRIE PAR L'IDLE, SANS PHRASE PRÉÉCRITE
# ==============================================================================
# autonomous_speak_if_ready() n'impose aucun texte. Il déclenche la bouche vivante
# seulement quand les pressions internes dépassent un seuil stable.

def _core_v50_autonomous_speak_if_ready(self, force: bool = False):
    try:
        idle = self.idle_update()
    except Exception:
        idle = {}
    try:
        bridge_payload = self._build_living_expression_payload("", {"inhibition": {"response_mode": "autonomous"}, "living_state_bus": self.living_state_bus.snapshot(), "idle_update": idle, "attention": self.living_state.get("attention", {}), "presence": self.living_state.get("presence", {})})
    except Exception:
        bridge_payload = {"emotional_state": self.emotional_state.snapshot(), "internal_needs": self.internal_needs.snapshot(), "living_state": dict(self.living_state)}
    pressure = max(
        _safe_float(bridge_payload.get("expression_pressure", 0.0)),
        _safe_float(getattr(self.internal_needs, "expression", 0.0)),
        _safe_float(getattr(self.internal_needs, "curiosity", 0.0)),
        _safe_float(getattr(self.mental_momentum, "vector", {}).get("expressive_pressure", 0.0)) if hasattr(self, "mental_momentum") else 0.0,
        _safe_float((self.living_state.get("silent_subjective_life", {}) or {}).get("pressure", 0.0)) if isinstance(self.living_state.get("silent_subjective_life", {}), Mapping) else 0.0,
    )
    restraint = max(_safe_float(bridge_payload.get("restraint", 0.0)), _safe_float(getattr(self.emotional_state, "cognitive_overload", 0.0)))
    ready = bool(force or (pressure > 0.54 and restraint < 0.74))
    if not ready:
        self.living_state["autonomous_speech_ready"] = {"ready": False, "pressure": round(pressure, 4), "restraint": round(restraint, 4)}
        return None
    context = {"living_expression_payload": bridge_payload, "inhibition": {"response_mode": "autonomous"}, "meta_risk": 0.0, "impulse": self.living_state.get("impulse", {}), "initiative": self.living_state.get("initiative", {})}
    text, trace = self.generate_expression("", context)
    text = str(text or "").strip()
    if not text:
        try:
            from emergent_french_weaver import EmergentFrenchWeaver
            weaver = getattr(self, "_emergent_french_weaver", None) or EmergentFrenchWeaver()
            self._emergent_french_weaver = weaver
            out = weaver.generate(user_message="", payload=bridge_payload, min_words=6, max_words=18)
            text = str(out.get("text", "")).strip()
            trace = {"autonomous_weaver": True, **dict(out.get("trace", {}))}
        except Exception:
            text = ""
    if text:
        self.living_state["last_autonomous_speech"] = {"text": text, "pressure": round(pressure, 4), "restraint": round(restraint, 4), "trace": trace}
        try:
            self.thought_stream.push({"type": "autonomous_expression", "content": text, "strength": pressure, "at": self.internal_time.exchange_count})
        except Exception:
            pass
        return text
    return None

try:
    LeiaLivingCore.autonomous_speak_if_ready = _core_v50_autonomous_speak_if_ready
except NameError:
    pass


# ══════════════════════════════════════════════════════════════════════════════
# V6 — LIVED PRESENCE INJECTION
# Injecte la sensation du moment présent dans le flux expressif.
# ══════════════════════════════════════════════════════════════════════════════

def _inject_v6_lived_presence(payload: dict, affective_state: dict | None = None):
    lived = build_lived_present_snapshot(affective_state or {})
    payload["lived_present"] = lived
    payload["embodied_density"] = lived.get("embodied_density", 0.0)
    payload["situated_posture"] = lived.get("posture", "distant")
    return payload




    def _build_unified_lived_state(
        self,
        affective_state=None,
        impulse_state=None,
        memory_state=None,
        presence_state=None,
    ):
        try:
            return self.unified_lived_experience.build(
                affective_state=affective_state,
                impulse_state=impulse_state,
                memory_state=memory_state,
                presence_state=presence_state,
            )
        except Exception:
            return {
                "lived_continuity": 0.0,
                "unresolved_tension": 0.0,
                "relational_closeness": 0.0,
                "memory_pressure": 0.0,
                "active_topics": [],
                "is_living_moment": False,
            }
