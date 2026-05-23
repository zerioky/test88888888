"""
Mémoire causale vivante — moteur autonome et non préécrit.

Ce module ne génère pas de phrases de dialogue. Il mémorise des relations
cause → effet vécues, les renforce/affaiblit, les nettoie des traces techniques,
et renvoie uniquement des influences structurées utilisables par d'autres moteurs.

V4 ajoute temporalité vécue, contradictions contextuelles, importance relationnelle,
consolidation organique, mémoire dormante, épisodes et pression causale continue.

V5 renforce la mémoire réellement vivante : inertie émotionnelle, activation
causale en cascade, continuité autobiographique, résolution contextuelle des
contradictions, simulation prospective multi-futurs, traces relationnelles
profondes, inhibition anti-surcharge et signaux de transformation identitaire.

V6 complète la couche vivante sans générer de dialogue : arcs de transformation
longue, besoins internes, graphe causal global, compression autobiographique,
conséquences utilisateur, réactivation émotionnelle contextuelle, mémoire des
échecs existentiels, régulation anti-obsession et pont direct vers initiative,
émotion, attention et expression.

V7 ajoute le vécu causal profond : maturation temporelle des souvenirs,
cicatrices relationnelles persistantes, désirs causaux, conflits internes,
continuité sociale, pression de transformation identitaire et synthèse vivante
exportable vers les moteurs d'attention, initiative, émotion et expression.

V7.1 ajoute une couche psychologique globale sans parole préécrite :
réinterprétation dynamique du sens vécu, pression subconsciente diffuse,
marques irréversibles, climat intérieur global, phases relationnelles,
projection affective future, racines causales profondes et saturation cumulative.

V7.4.2 complète l'écologie causale vivante : chaînes multi-échelles, conflits dynamiques, mémoire implicite incarnée, inertie comportementale, fatigue existentielle, micro-réactions et prospective pré-interaction.

V7.4.3 ajoute la vie causale autonome : dérive implicite hors contexte,
retour inter-moteurs, restructuration organique des priorités, temporalité
vécue continue et mémoire invisible exportable sans générer de dialogue.

V7.4.4 consolide la vie silencieuse : cycle passif type sommeil/repos,
auto-préservation identitaire, continuité conversationnelle vécue, mutation
organique des contradictions profondes et exports non dialoguants renforcés.

V7.4.1 corrige l'orchestration vivante globale : arbitrage blessures/désirs/
conflits, écologie causale lente, fatigue/recovery organique, non-action
contextuelle, contraintes d'expression hiérarchisées, ponts inter-moteurs unifiés
et métriques de stabilité profonde sans générer de dialogue.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


TECHNICAL_TERMS = {
    "weight", "weights", "stability", "last_tokens", "tokens", "token",
    "logits", "embedding", "embeddings", "score", "scores", "debug",
    "traceback", "stack", "json", "dict", "metadata", "module", "function",
    "class", "threshold", "pipeline", "fallback", "template", "templates",
}

_ALLOWED_EMOTIONS = {"neutral", "positive", "negative", "intense", "transformative", "uncertain"}

_ALLOWED_MEMORY_KINDS = {
    "general",
    "expressive_failure",
    "expressive_repair",
    "relational_boundary",
    "identity_continuity",
    "initiative_learning",
    "attention_learning",
    "affective_shift",
    "temporal_pattern",
    "contradiction_resolution",
    "relational_importance",
    "episodic_trace",
    "existential_failure",
    "internal_need",
    "user_consequence",
    "long_term_transformation",
}

_ALLOWED_REPAIR_KINDS = {
    "none",
    "directness",
    "warmth",
    "silence",
    "specificity",
    "anti_meta",
    "identity_stabilization",
    "organic_flow",
}

_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "got", "has",
    "he", "her", "his", "i", "in", "is", "it", "its", "me", "my", "not", "of", "on",
    "or", "our", "she", "that", "the", "their", "them", "this", "to", "was", "we",
    "with", "you", "your", "user", "leia",
    "à", "au", "aux", "avec", "ce", "ces", "cette", "dans", "de", "des", "du",
    "elle", "en", "et", "est", "il", "je", "la", "le", "les", "lui", "ma", "me",
    "mes", "mon", "ne", "nous", "pas", "pour", "que", "qui", "se", "son", "sur",
    "ta", "te", "tes", "toi", "ton", "tu", "un", "une", "vous",
}

_SYNONYMS = {
    "clarify": "clarity",
    "clear": "clarity",
    "clearly": "clarity",
    "clarté": "clarity",
    "clarte": "clarity",
    "clair": "clarity",
    "claire": "clarity",
    "examples": "example",
    "exemples": "example",
    "provided": "provide",
    "fournit": "provide",
    "donne": "provide",
    "explique": "explain",
    "explication": "explain",
    "confus": "confused",
    "confuse": "confused",
    "confusion": "confused",
    "philosophical": "philosophy",
    "philosophique": "philosophy",
}


def _now() -> str:
    return datetime.now().isoformat()


def _strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )


def _safe_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _dedupe_keep_order(items: Iterable[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        item = str(item or "").strip()
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


@dataclass
class CausalMemory:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=_now)

    event: str = ""
    experienced_effect: str = ""

    confidence: float = 0.7
    reinforcement_count: int = 0
    last_reinforced: str = field(default_factory=_now)

    emotional_trace: str = "neutral"
    behavioral_shift: str = ""
    attention_impact: str = ""

    memory_kind: str = "general"
    repair_kind: str = "none"
    valence: float = 0.0
    effect_strength: float = 0.0
    recurrence_pressure: float = 0.0
    source_engine: str = "causal_memory_engine"

    linked_memories: List[str] = field(default_factory=list)
    source_context: Dict[str, Any] = field(default_factory=dict)

    decay_factor: float = 1.0
    similarity_clusters: List[str] = field(default_factory=list)

    # V4 — couches vivantes : pas de dialogue préécrit, seulement des signaux.
    temporal_chain: List[Dict[str, Any]] = field(default_factory=list)
    contradiction_links: List[Dict[str, Any]] = field(default_factory=list)
    relational_importance: float = 0.0
    identity_impact: float = 0.0
    trust_variation: float = 0.0
    memory_priority: float = 0.0
    dormant: bool = False
    reactivation_score: float = 0.0
    causal_layers: Dict[str, float] = field(default_factory=dict)
    episode_markers: List[Dict[str, Any]] = field(default_factory=list)
    consolidation_summary: str = ""
    activation_history: List[Dict[str, Any]] = field(default_factory=list)

    # V5 — état vivant interne, toujours structuré et non dialoguant.
    emotional_inertia: float = 0.0
    affective_charge: float = 0.0
    relational_wound: float = 0.0
    attachment_trace: float = 0.0
    autobiographical_weight: float = 0.0
    identity_shift_vector: Dict[str, float] = field(default_factory=dict)
    unresolved_tension: float = 0.0
    future_bias: Dict[str, float] = field(default_factory=dict)
    inhibition_level: float = 0.0
    causal_activation: float = 0.0
    living_state_history: List[Dict[str, Any]] = field(default_factory=list)

    # V6 — couches longues et ponts inter-moteurs, sans parole préécrite.
    identity_evolution_arcs: List[Dict[str, Any]] = field(default_factory=list)
    internal_need_profile: Dict[str, float] = field(default_factory=dict)
    user_consequence_trace: Dict[str, float] = field(default_factory=dict)
    contextual_emotional_resonance: Dict[str, float] = field(default_factory=dict)
    existential_failure_trace: Dict[str, float] = field(default_factory=dict)
    obsession_guard_state: Dict[str, float] = field(default_factory=dict)
    initiative_bridge: Dict[str, float] = field(default_factory=dict)
    affective_bridge: Dict[str, float] = field(default_factory=dict)
    expression_bridge: Dict[str, float] = field(default_factory=dict)
    compressed_autobiographical_chapters: List[Dict[str, Any]] = field(default_factory=list)

    # V7 — vécu causal profond : maturation, désir, cicatrice, conflit, lien social.
    temporal_maturation_state: Dict[str, float] = field(default_factory=dict)
    persistent_wound_profile: Dict[str, float] = field(default_factory=dict)
    causal_desire_profile: Dict[str, float] = field(default_factory=dict)
    inner_conflict_profile: Dict[str, float] = field(default_factory=dict)
    social_continuity_profile: Dict[str, float] = field(default_factory=dict)
    identity_transformation_pressure: Dict[str, float] = field(default_factory=dict)
    lived_meaning_revision: List[Dict[str, Any]] = field(default_factory=list)

    # V7.1 — psychologie causale globale : influence diffuse, relecture, irréversibilité.
    current_lived_meaning: Dict[str, float] = field(default_factory=dict)
    original_lived_meaning: Dict[str, float] = field(default_factory=dict)
    subconscious_bias_field: Dict[str, float] = field(default_factory=dict)
    irreversible_identity_marks: Dict[str, float] = field(default_factory=dict)
    relationship_phase_profile: Dict[str, float] = field(default_factory=dict)
    anticipated_affective_projection: Dict[str, float] = field(default_factory=dict)
    deep_causal_roots: Dict[str, float] = field(default_factory=dict)
    cumulative_social_saturation: Dict[str, float] = field(default_factory=dict)

    def normalized(self) -> "CausalMemory":
        self.event = CausalMemoryEngine.sanitize_text(self.event)
        self.experienced_effect = CausalMemoryEngine.sanitize_text(self.experienced_effect)
        self.behavioral_shift = CausalMemoryEngine.sanitize_text(self.behavioral_shift)
        self.attention_impact = CausalMemoryEngine.sanitize_text(self.attention_impact)
        self.confidence = _clamp(self.confidence)
        self.decay_factor = _clamp(self.decay_factor, 0.0, 1.0)
        self.reinforcement_count = max(0, int(self.reinforcement_count or 0))
        if self.emotional_trace not in _ALLOWED_EMOTIONS:
            self.emotional_trace = "neutral"
        if self.memory_kind not in _ALLOWED_MEMORY_KINDS:
            self.memory_kind = "general"
        if self.repair_kind not in _ALLOWED_REPAIR_KINDS:
            self.repair_kind = "none"
        self.valence = _clamp(self.valence, -1.0, 1.0)
        self.effect_strength = _clamp(self.effect_strength)
        self.recurrence_pressure = _clamp(self.recurrence_pressure)
        self.source_engine = CausalMemoryEngine.sanitize_text(self.source_engine) or "causal_memory_engine"
        self.linked_memories = _dedupe_keep_order(self.linked_memories)
        self.similarity_clusters = _dedupe_keep_order(self.similarity_clusters)
        if not isinstance(self.source_context, dict):
            self.source_context = {}
        self.relational_importance = _clamp(self.relational_importance)
        self.identity_impact = _clamp(self.identity_impact)
        self.trust_variation = _clamp(self.trust_variation, -1.0, 1.0)
        self.memory_priority = _clamp(self.memory_priority)
        self.reactivation_score = _clamp(self.reactivation_score)
        self.emotional_inertia = _clamp(self.emotional_inertia)
        self.affective_charge = _clamp(self.affective_charge)
        self.relational_wound = _clamp(self.relational_wound)
        self.attachment_trace = _clamp(self.attachment_trace)
        self.autobiographical_weight = _clamp(self.autobiographical_weight)
        self.unresolved_tension = _clamp(self.unresolved_tension)
        self.inhibition_level = _clamp(self.inhibition_level)
        self.causal_activation = _clamp(self.causal_activation)
        self.dormant = bool(self.dormant)
        if not isinstance(self.temporal_chain, list):
            self.temporal_chain = []
        if not isinstance(self.contradiction_links, list):
            self.contradiction_links = []
        if not isinstance(self.causal_layers, dict):
            self.causal_layers = {}
        if not isinstance(self.episode_markers, list):
            self.episode_markers = []
        if not isinstance(self.activation_history, list):
            self.activation_history = []
        if not isinstance(self.living_state_history, list):
            self.living_state_history = []
        if not isinstance(self.identity_shift_vector, dict):
            self.identity_shift_vector = {}
        if not isinstance(self.future_bias, dict):
            self.future_bias = {}
        if not isinstance(self.identity_evolution_arcs, list):
            self.identity_evolution_arcs = []
        if not isinstance(self.internal_need_profile, dict):
            self.internal_need_profile = {}
        if not isinstance(self.user_consequence_trace, dict):
            self.user_consequence_trace = {}
        if not isinstance(self.contextual_emotional_resonance, dict):
            self.contextual_emotional_resonance = {}
        if not isinstance(self.existential_failure_trace, dict):
            self.existential_failure_trace = {}
        if not isinstance(self.obsession_guard_state, dict):
            self.obsession_guard_state = {}
        if not isinstance(self.initiative_bridge, dict):
            self.initiative_bridge = {}
        if not isinstance(self.affective_bridge, dict):
            self.affective_bridge = {}
        if not isinstance(self.expression_bridge, dict):
            self.expression_bridge = {}
        if not isinstance(self.compressed_autobiographical_chapters, list):
            self.compressed_autobiographical_chapters = []
        if not isinstance(self.temporal_maturation_state, dict):
            self.temporal_maturation_state = {}
        if not isinstance(self.persistent_wound_profile, dict):
            self.persistent_wound_profile = {}
        if not isinstance(self.causal_desire_profile, dict):
            self.causal_desire_profile = {}
        if not isinstance(self.inner_conflict_profile, dict):
            self.inner_conflict_profile = {}
        if not isinstance(self.social_continuity_profile, dict):
            self.social_continuity_profile = {}
        if not isinstance(self.identity_transformation_pressure, dict):
            self.identity_transformation_pressure = {}
        if not isinstance(self.lived_meaning_revision, list):
            self.lived_meaning_revision = []
        if not isinstance(self.current_lived_meaning, dict):
            self.current_lived_meaning = {}
        if not isinstance(self.original_lived_meaning, dict):
            self.original_lived_meaning = {}
        if not isinstance(self.subconscious_bias_field, dict):
            self.subconscious_bias_field = {}
        if not isinstance(self.irreversible_identity_marks, dict):
            self.irreversible_identity_marks = {}
        if not isinstance(self.relationship_phase_profile, dict):
            self.relationship_phase_profile = {}
        if not isinstance(self.anticipated_affective_projection, dict):
            self.anticipated_affective_projection = {}
        if not isinstance(self.deep_causal_roots, dict):
            self.deep_causal_roots = {}
        if not isinstance(self.cumulative_social_saturation, dict):
            self.cumulative_social_saturation = {}
        self.temporal_chain = self.temporal_chain[-24:]
        self.contradiction_links = self.contradiction_links[-20:]
        self.episode_markers = self.episode_markers[-16:]
        self.activation_history = self.activation_history[-32:]
        self.living_state_history = self.living_state_history[-24:]
        self.identity_evolution_arcs = self.identity_evolution_arcs[-18:]
        self.compressed_autobiographical_chapters = self.compressed_autobiographical_chapters[-12:]
        self.lived_meaning_revision = self.lived_meaning_revision[-16:]
        self.consolidation_summary = CausalMemoryEngine.sanitize_text(self.consolidation_summary)
        self.causal_layers = {
            CausalMemoryEngine.sanitize_text(k): _clamp(v, -1.0, 1.0)
            for k, v in self.causal_layers.items()
            if CausalMemoryEngine.sanitize_text(k)
        }
        self.identity_shift_vector = {
            CausalMemoryEngine.sanitize_text(k): _clamp(v, -1.0, 1.0)
            for k, v in self.identity_shift_vector.items()
            if CausalMemoryEngine.sanitize_text(k)
        }
        self.future_bias = {
            CausalMemoryEngine.sanitize_text(k): _clamp(v, -1.0, 1.0)
            for k, v in self.future_bias.items()
            if CausalMemoryEngine.sanitize_text(k)
        }
        for attr in (
            "internal_need_profile", "user_consequence_trace",
            "contextual_emotional_resonance", "existential_failure_trace",
            "obsession_guard_state", "initiative_bridge",
            "affective_bridge", "expression_bridge",
            "temporal_maturation_state", "persistent_wound_profile",
            "causal_desire_profile", "inner_conflict_profile",
            "social_continuity_profile", "identity_transformation_pressure",
            "current_lived_meaning", "original_lived_meaning",
            "subconscious_bias_field", "irreversible_identity_marks",
            "relationship_phase_profile", "anticipated_affective_projection",
            "deep_causal_roots", "cumulative_social_saturation",
        ):
            raw = getattr(self, attr, {})
            setattr(self, attr, {
                CausalMemoryEngine.sanitize_text(k): _clamp(v, -1.0, 1.0)
                for k, v in raw.items()
                if CausalMemoryEngine.sanitize_text(k)
            })
        return self


class CausalMemoryEngine:
    """
    Moteur de mémoire causale vivante.

    Important : ce moteur ne parle jamais à la place de Leia. Il renvoie des
    signaux structurés pour guider l'attention, l'affect, l'initiative et les
    contraintes comportementales sans phrases de dialogue préécrites.
    """

    TECHNICAL_TERMS = TECHNICAL_TERMS

    def __init__(self, memory_path: str = "data/causal_memory.json"):
        self.memory_path = Path(memory_path)
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        self.memories: Dict[str, CausalMemory] = {}

        self.confidence_threshold = 0.5
        self.reinforcement_increment = 0.16
        self.decay_per_day = 0.015
        self.similarity_threshold = 0.62
        self.attention_weight = 1.2
        self.contradiction_threshold = 0.56
        self.consolidation_min_cluster_size = 3
        self.dormancy_confidence_floor = 0.22
        self.cascade_decay = 0.64
        self.cascade_min_activation = 0.055
        self.overload_soft_limit = 14
        self.emotional_cooling_rate = 0.035
        self.obsession_pressure_limit = 0.72
        self.long_arc_min_priority = 0.34
        self.chapter_cluster_min = 3
        self.user_consequence_weight = 0.16
        self.need_memory_weight = 0.14
        self.maturation_weight = 0.18
        self.desire_weight = 0.16
        self.conflict_weight = 0.17
        self.social_continuity_weight = 0.15
        self.identity_transformation_weight = 0.18
        # V7.2 — persistance psychologique silencieuse : les souvenirs continuent
        # d'influencer l'état intérieur même hors rappel sémantique direct.
        self.passive_psychological_floor = 0.045
        self.silent_drift_rate = 0.026
        self.fatigue_accumulation_rate = 0.038
        self.fatigue_recovery_rate = 0.018
        self.conflict_persistence_rate = 0.032
        self.identity_trait_drift_rate = 0.021
        self.emotional_contamination_rate = 0.024
        self.autobiographical_rewrite_rate = 0.018
        self.attractor_stability_rate = 0.022
        self.non_action_memory_threshold = 0.26
        # V7.4.3 — couche organique autonome : dérive implicite, retour inter-moteurs
        # et restructuration lente même sans contexte utilisateur direct.
        self.autonomous_drift_rate = 0.019
        self.implicit_memory_floor = 0.035
        self.cross_engine_feedback_weight = 0.18
        self.organic_restructure_rate = 0.017
        self.temporal_lived_continuity_rate = 0.015
        self.invisible_trace_decay = 0.986

        self.load_memories()

    # ───────────────────────── nettoyage / sécurité ─────────────────────────

    @staticmethod
    def sanitize_text(text: Any) -> str:
        """Retire les traces techniques et normalise un champ causalisable."""
        if text is None:
            return ""
        value = str(text).replace("\x00", " ").strip()
        if not value:
            return ""

        # Supprime fragments key=value / key: value purement techniques.
        for term in sorted(TECHNICAL_TERMS, key=len, reverse=True):
            value = re.sub(rf"\b{re.escape(term)}\b\s*[:=]\s*[^,;\]\)}}]+", " ", value, flags=re.I)
            value = re.sub(rf"\b{re.escape(term)}\b", " ", value, flags=re.I)

        value = re.sub(r"[`{}\[\]<>]", " ", value)
        value = re.sub(r"\s+", " ", value).strip(" ,;:.-")
        return value[:700]

    @classmethod
    def _contains_technical_noise(cls, text: Any) -> bool:
        raw = str(text or "").lower()
        return any(re.search(rf"\b{re.escape(term)}\b", raw) for term in TECHNICAL_TERMS)

    @classmethod
    def _sanitize_context(cls, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        if not isinstance(context, dict):
            return {}
        cleaned: Dict[str, Any] = {}
        for key, value in context.items():
            key_s = cls.sanitize_text(key)
            if not key_s or cls._contains_technical_noise(key_s):
                continue
            if isinstance(value, str):
                cleaned_value = cls.sanitize_text(value)
                if cleaned_value:
                    cleaned[key_s] = cleaned_value
            elif isinstance(value, (int, float, bool)) or value is None:
                cleaned[key_s] = value
            elif isinstance(value, dict):
                sub = cls._sanitize_context(value)
                if sub:
                    cleaned[key_s] = sub
            elif isinstance(value, list):
                safe_items = []
                for item in value[:20]:
                    if isinstance(item, str):
                        item = cls.sanitize_text(item)
                        if item:
                            safe_items.append(item)
                    elif isinstance(item, (int, float, bool)):
                        safe_items.append(item)
                if safe_items:
                    cleaned[key_s] = safe_items
        return cleaned

    # ───────────────────────── persistence ─────────────────────────

    def load_memories(self) -> None:
        if not self.memory_path.exists():
            self.save_memories()
            return
        try:
            data = json.loads(self.memory_path.read_text(encoding="utf-8") or "{}")
        except (json.JSONDecodeError, OSError):
            self.memories = {}
            return
        if not isinstance(data, dict):
            self.memories = {}
            return

        loaded: Dict[str, CausalMemory] = {}
        for mem_id, raw in data.items():
            if str(mem_id).startswith("_") or not isinstance(raw, dict):
                continue
            try:
                allowed = {field_name for field_name in CausalMemory.__dataclass_fields__}
                payload = {k: v for k, v in raw.items() if k in allowed}
                mem = CausalMemory(**payload).normalized()
                if mem.event and mem.experienced_effect:
                    loaded[mem.id or str(mem_id)] = mem
            except Exception:
                continue
        self.memories = loaded

    def save_memories(self) -> None:
        data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
        data["_metadata"] = {
            "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
            "last_updated": _now(),
            "total_memories": len(self.memories),
            "avg_confidence": self.get_memory_stats().get("avg_confidence", 0.0) if self.memories else 0.0,
            "role": "living_causal_memory_not_dialogue_generator",
            "v4_capabilities": [
                "temporal_episodes", "contradiction_links", "relational_importance",
                "organic_consolidation", "dormant_memory_reactivation",
                "multi_layer_pressure", "predictive_causal_simulation",
                "emotional_inertia", "causal_cascade_activation",
                "autobiographical_continuity", "contextual_belief_revision",
                "deep_relational_traces", "adaptive_inhibition",
                "long_term_transformation_arcs", "internal_need_memory",
                "causal_global_graph", "autobiographical_compression",
                "user_consequence_trace", "contextual_emotional_resonance",
                "existential_failure_memory", "anti_obsession_regulation",
                "initiative_emotion_expression_bridges",
                "temporal_meaning_maturation",
                "persistent_relational_wounds",
                "causal_desire_attractors",
                "deep_inner_conflict_field",
                "social_continuity_memory",
                "identity_transformation_pressure",
                "living_meaning_revision",
                "dynamic_lived_meaning_reinterpretation",
                "subconscious_causal_pressure_field",
                "irreversible_identity_marks",
                "global_inner_weather",
                "relationship_phase_evolution",
                "anticipated_affective_projection",
                "deep_causal_root_graph",
                "cumulative_social_saturation",
                "silent_psychological_persistence",
                "background_fatigue_and_recovery",
                "durable_inner_conflict_persistence",
                "slow_identity_trait_drift",
                "persistent_relationship_phase_drift",
                "deep_psychological_hierarchy",
                "autobiographical_priority_reorganization",
                "persistent_slow_dynamics_save",
                "causal_echo_pressure",
                "global_causal_ecology_orchestration",
                "organic_cooldown_and_non_action_permission",
                "hierarchical_expression_constraints",
                "unified_cross_engine_living_pressure",
                "autonomous_implicit_causal_drift",
                "cross_engine_feedback_absorption",
                "organic_priority_restructuring",
                "temporal_lived_continuity_field",
                "invisible_memory_bias_export"
            ],
        }
        self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ───────────────────────── apprentissage ─────────────────────────

    def learn_causal_relation(
        self,
        event: str,
        experienced_effect: str,
        emotional_trace: str = "neutral",
        behavioral_shift: str = "",
        attention_impact: str = "",
        source_context: Optional[Dict[str, Any]] = None,
        initial_confidence: float = 0.7,
        memory_kind: str = "general",
        repair_kind: str = "none",
        valence: float = 0.0,
        effect_strength: float = 0.0,
        recurrence_pressure: float = 0.0,
        source_engine: str = "causal_memory_engine",
        relational_importance: float = 0.0,
        identity_impact: float = 0.0,
        trust_variation: float = 0.0,
        causal_layers: Optional[Dict[str, float]] = None,
        episode_context: Optional[Dict[str, Any]] = None,
        autobiographical_weight: float = 0.0,
        relational_wound: float = 0.0,
        attachment_trace: float = 0.0,
        future_bias: Optional[Dict[str, float]] = None,
        identity_shift_vector: Optional[Dict[str, float]] = None,
    ) -> str:
        event = self.sanitize_text(event)
        experienced_effect = self.sanitize_text(experienced_effect)
        behavioral_shift = self.sanitize_text(behavioral_shift)
        attention_impact = self.sanitize_text(attention_impact)

        if not event or not experienced_effect:
            raise ValueError("event et experienced_effect requis")
        if self._contains_technical_noise(event) or self._contains_technical_noise(experienced_effect):
            # Après nettoyage, un reste technique ne doit pas devenir une mémoire.
            raise ValueError("relation causale rejetée: trace technique interne détectée")

        emotional_trace = emotional_trace if emotional_trace in _ALLOWED_EMOTIONS else "neutral"
        memory_kind = memory_kind if memory_kind in _ALLOWED_MEMORY_KINDS else "general"
        repair_kind = repair_kind if repair_kind in _ALLOWED_REPAIR_KINDS else "none"
        initial_confidence = _clamp(_safe_float(initial_confidence, 0.7), 0.05, 1.0)
        valence = _clamp(_safe_float(valence, 0.0), -1.0, 1.0)
        effect_strength = _clamp(_safe_float(effect_strength, 0.0))
        recurrence_pressure = _clamp(_safe_float(recurrence_pressure, 0.0))
        source_engine = self.sanitize_text(source_engine) or "causal_memory_engine"
        relational_importance = _clamp(_safe_float(relational_importance, 0.0))
        identity_impact = _clamp(_safe_float(identity_impact, 0.0))
        trust_variation = _clamp(_safe_float(trust_variation, 0.0), -1.0, 1.0)
        causal_layers = self._normalize_layers(causal_layers, memory_kind, repair_kind, valence, effect_strength, recurrence_pressure)
        autobiographical_weight = _clamp(_safe_float(autobiographical_weight, max(relational_importance, identity_impact) * 0.55))
        relational_wound = _clamp(_safe_float(relational_wound, max(0.0, -valence) * relational_importance))
        attachment_trace = _clamp(_safe_float(attachment_trace, max(0.0, valence) * relational_importance))
        future_bias = self._normalize_vector(future_bias or self._derive_future_bias(memory_kind, repair_kind, valence, effect_strength, recurrence_pressure))
        identity_shift_vector = self._normalize_vector(identity_shift_vector or self._derive_identity_shift(memory_kind, identity_impact, trust_variation, valence))
        episode_marker = self._build_episode_marker(event, experienced_effect, emotional_trace, episode_context, effect_strength)

        similar_id = self._find_similar_memory(event, experienced_effect)
        if similar_id:
            self.reinforce_memory(
                similar_id,
                emotional_trace=emotional_trace,
                behavioral_shift=behavioral_shift,
                attention_impact=attention_impact,
                source_context=source_context,
                memory_kind=memory_kind,
                repair_kind=repair_kind,
                valence=valence,
                effect_strength=effect_strength,
                recurrence_pressure=recurrence_pressure,
                relational_importance=relational_importance,
                identity_impact=identity_impact,
                trust_variation=trust_variation,
                causal_layers=causal_layers,
                episode_marker=episode_marker,
                autobiographical_weight=autobiographical_weight,
                relational_wound=relational_wound,
                attachment_trace=attachment_trace,
                future_bias=future_bias,
                identity_shift_vector=identity_shift_vector,
            )
            return similar_id

        memory = CausalMemory(
            event=event,
            experienced_effect=experienced_effect,
            confidence=initial_confidence,
            emotional_trace=emotional_trace,
            behavioral_shift=behavioral_shift,
            attention_impact=attention_impact,
            source_context=self._sanitize_context(source_context),
            reinforcement_count=1,
            memory_kind=memory_kind,
            repair_kind=repair_kind,
            valence=valence,
            effect_strength=effect_strength,
            recurrence_pressure=recurrence_pressure,
            source_engine=source_engine,
            relational_importance=relational_importance,
            identity_impact=identity_impact,
            trust_variation=trust_variation,
            causal_layers=causal_layers,
            episode_markers=[episode_marker] if episode_marker else [],
            temporal_chain=[self._temporal_step("created", event, experienced_effect, effect_strength)],
            emotional_inertia=self._initial_emotional_inertia(emotional_trace, valence, effect_strength, recurrence_pressure),
            affective_charge=max(abs(valence), effect_strength),
            relational_wound=relational_wound,
            attachment_trace=attachment_trace,
            autobiographical_weight=autobiographical_weight,
            identity_shift_vector=identity_shift_vector,
            unresolved_tension=max(0.0, relational_wound, abs(trust_variation) * 0.55),
            future_bias=future_bias,
            causal_activation=max(effect_strength, recurrence_pressure, autobiographical_weight * 0.75),
            living_state_history=[self._living_state_step("created", max(effect_strength, recurrence_pressure), valence, relational_wound)],
        ).normalized()
        memory.memory_priority = self._calculate_memory_priority(memory)
        self.memories[memory.id] = memory
        self._register_contradictions(memory.id)
        self._refresh_v6_living_extensions(memory.id)
        self.save_memories()
        return memory.id

    def reinforce_memory(
        self,
        memory_id: str,
        emotional_trace: Optional[str] = None,
        behavioral_shift: Optional[str] = None,
        attention_impact: Optional[str] = None,
        source_context: Optional[Dict[str, Any]] = None,
        memory_kind: Optional[str] = None,
        repair_kind: Optional[str] = None,
        valence: Optional[float] = None,
        effect_strength: Optional[float] = None,
        recurrence_pressure: Optional[float] = None,
        relational_importance: Optional[float] = None,
        identity_impact: Optional[float] = None,
        trust_variation: Optional[float] = None,
        causal_layers: Optional[Dict[str, float]] = None,
        episode_marker: Optional[Dict[str, Any]] = None,
        autobiographical_weight: Optional[float] = None,
        relational_wound: Optional[float] = None,
        attachment_trace: Optional[float] = None,
        future_bias: Optional[Dict[str, float]] = None,
        identity_shift_vector: Optional[Dict[str, float]] = None,
    ) -> None:
        mem = self.memories.get(memory_id)
        if not mem:
            return
        gain = self.reinforcement_increment * math.sqrt(max(1, mem.reinforcement_count)) * (1.0 - mem.confidence)
        mem.confidence = _clamp(mem.confidence + max(0.025, gain))
        mem.reinforcement_count += 1
        mem.last_reinforced = _now()
        mem.decay_factor = 1.0

        if emotional_trace in _ALLOWED_EMOTIONS and emotional_trace != "neutral":
            mem.emotional_trace = emotional_trace
        if behavioral_shift:
            mem.behavioral_shift = self._merge_text_field(mem.behavioral_shift, behavioral_shift)
        if attention_impact:
            mem.attention_impact = self._merge_text_field(mem.attention_impact, attention_impact)
        if source_context:
            mem.source_context.update(self._sanitize_context(source_context))
        if memory_kind in _ALLOWED_MEMORY_KINDS and memory_kind != "general":
            mem.memory_kind = memory_kind
        if repair_kind in _ALLOWED_REPAIR_KINDS and repair_kind != "none":
            mem.repair_kind = repair_kind
        if valence is not None:
            mem.valence = _clamp((mem.valence * 0.65) + (_safe_float(valence, 0.0) * 0.35), -1.0, 1.0)
        if effect_strength is not None:
            mem.effect_strength = _clamp(max(mem.effect_strength * 0.88, _safe_float(effect_strength, 0.0)))
        if recurrence_pressure is not None:
            mem.recurrence_pressure = _clamp(max(mem.recurrence_pressure * 0.86, _safe_float(recurrence_pressure, 0.0)))
        if relational_importance is not None:
            mem.relational_importance = _clamp(max(mem.relational_importance * 0.9, _safe_float(relational_importance, 0.0)))
        if identity_impact is not None:
            mem.identity_impact = _clamp(max(mem.identity_impact * 0.9, _safe_float(identity_impact, 0.0)))
        if trust_variation is not None:
            mem.trust_variation = _clamp((mem.trust_variation * 0.72) + (_safe_float(trust_variation, 0.0) * 0.28), -1.0, 1.0)
        if causal_layers:
            mem.causal_layers = self._merge_layers(mem.causal_layers, causal_layers)
        if autobiographical_weight is not None:
            mem.autobiographical_weight = _clamp(max(mem.autobiographical_weight * 0.92, _safe_float(autobiographical_weight, 0.0)))
        if relational_wound is not None:
            mem.relational_wound = _clamp(max(mem.relational_wound * 0.94, _safe_float(relational_wound, 0.0)))
        if attachment_trace is not None:
            mem.attachment_trace = _clamp(max(mem.attachment_trace * 0.94, _safe_float(attachment_trace, 0.0)))
        if future_bias:
            mem.future_bias = self._merge_layers(mem.future_bias, future_bias)
        if identity_shift_vector:
            mem.identity_shift_vector = self._merge_layers(mem.identity_shift_vector, identity_shift_vector)
        if episode_marker:
            mem.episode_markers.append(episode_marker)
        mem.emotional_inertia = _clamp(max(mem.emotional_inertia * 0.91, self._initial_emotional_inertia(mem.emotional_trace, mem.valence, mem.effect_strength, mem.recurrence_pressure)))
        mem.affective_charge = _clamp(max(mem.affective_charge * 0.9, abs(mem.valence), mem.effect_strength))
        mem.unresolved_tension = _clamp(max(mem.unresolved_tension * 0.9, mem.relational_wound, abs(mem.trust_variation) * 0.5))
        mem.causal_activation = _clamp(max(mem.causal_activation * 0.72, mem.effect_strength, mem.recurrence_pressure, mem.memory_priority))
        mem.temporal_chain.append(self._temporal_step("reinforced", mem.event, mem.experienced_effect, mem.effect_strength))
        mem.living_state_history.append(self._living_state_step("reinforced", mem.causal_activation, mem.valence, mem.relational_wound))
        mem.memory_priority = self._calculate_memory_priority(mem)
        mem.dormant = False
        mem.reactivation_score = 1.0
        mem.normalized()
        self._register_contradictions(memory_id)
        self._refresh_v6_living_extensions(memory_id)
        self.save_memories()

    def weaken_memory(self, memory_id: str, factor: float = 0.1) -> None:
        mem = self.memories.get(memory_id)
        if not mem:
            return
        mem.confidence = _clamp(mem.confidence - abs(_safe_float(factor, 0.1)))
        mem.last_reinforced = _now()
        if mem.confidence < 0.3:
            mem.emotional_trace = "uncertain"
        mem.memory_priority = self._calculate_memory_priority(mem)
        mem.dormant = mem.confidence <= self.dormancy_confidence_floor and mem.memory_priority < 0.32
        self.save_memories()

    def apply_temporal_decay(self) -> None:
        now = datetime.now()
        changed = False
        for mem in self.memories.values():
            try:
                last = datetime.fromisoformat(mem.last_reinforced)
            except ValueError:
                last = now
            days = max(0, (now - last).days)
            if days <= 0:
                continue
            decay = min(0.65, self.decay_per_day * days)
            mem.decay_factor = _clamp(1.0 - decay, 0.35, 1.0)
            protected = max(mem.relational_importance, mem.identity_impact, abs(mem.valence))
            mem.confidence = _clamp(mem.confidence * (mem.decay_factor + protected * 0.08))
            mem.memory_priority = self._calculate_memory_priority(mem)
            mem.dormant = mem.confidence <= self.dormancy_confidence_floor and mem.memory_priority < 0.32
            mem.temporal_chain.append(self._temporal_step("decayed", mem.event, mem.experienced_effect, mem.effect_strength))
            changed = True
        if changed:
            self.save_memories()

    # ───────────────────────── similarité / fusion ─────────────────────────

    @staticmethod
    def _tokens(text: str) -> List[str]:
        text = _strip_accents(str(text or "").lower())
        raw = re.findall(r"[a-zA-ZÀ-ÿ0-9_']+", text)
        tokens = []
        for tok in raw:
            tok = tok.strip("_' ")
            if not tok or tok in _STOPWORDS or tok in TECHNICAL_TERMS:
                continue
            tok = _SYNONYMS.get(tok, tok)
            if tok.endswith("ing") and len(tok) > 5:
                tok = tok[:-3]
            elif tok.endswith("ed") and len(tok) > 4:
                tok = tok[:-2]
            elif tok.endswith("s") and len(tok) > 4:
                tok = tok[:-1]
            tokens.append(tok)
        return tokens

    def _text_similarity(self, text1: str, text2: str) -> float:
        t1 = self._tokens(text1)
        t2 = self._tokens(text2)
        if not t1 or not t2:
            return 0.0
        s1, s2 = set(t1), set(t2)
        jaccard = len(s1 & s2) / max(1, len(s1 | s2))
        containment = len(s1 & s2) / max(1, min(len(s1), len(s2)))
        prefix_bonus = 0.0
        for a in s1:
            for b in s2:
                if a != b and len(a) >= 4 and len(b) >= 4 and (a.startswith(b[:4]) or b.startswith(a[:4])):
                    prefix_bonus += 0.18
        return _clamp((0.55 * jaccard) + (0.45 * containment) + min(prefix_bonus, 0.24))

    def _find_similar_memory(self, event: str, effect: str) -> Optional[str]:
        best_id: Optional[str] = None
        best_score = 0.0
        for mem_id, mem in self.memories.items():
            event_sim = self._text_similarity(event, mem.event)
            effect_sim = self._text_similarity(effect, mem.experienced_effect)
            # Fusion conservatrice : il faut que la cause ET l'effet se ressemblent.
            combined = (event_sim * 0.56) + (effect_sim * 0.44)
            if event_sim >= 0.72 and effect_sim >= 0.60 and combined > best_score:
                best_id, best_score = mem_id, combined
        return best_id if best_score >= 0.68 else None

    def find_related_memories(self, memory_id: str, threshold: float = 0.6) -> List[str]:
        anchor = self.memories.get(memory_id)
        if not anchor:
            return []
        related = []
        for other_id, other in self.memories.items():
            if other_id == memory_id:
                continue
            score = max(
                self._text_similarity(anchor.event, other.event),
                self._text_similarity(anchor.experienced_effect, other.experienced_effect),
            )
            if score >= threshold:
                related.append(other_id)
        return related

    def cluster_similar_memories(self) -> Dict[str, List[str]]:
        clusters: Dict[str, List[str]] = {}
        processed = set()
        for mem_id, mem in self.memories.items():
            if mem_id in processed:
                continue
            related = [rid for rid in self.find_related_memories(mem_id, self.similarity_threshold) if rid not in processed]
            if related:
                cluster = [mem_id] + related
                key = "cluster_" + uuid.uuid5(uuid.NAMESPACE_DNS, mem.event).hex[:8]
                clusters[key] = cluster
                for item in cluster:
                    processed.add(item)
                    self.memories[item].similarity_clusters = _dedupe_keep_order(
                        self.memories[item].similarity_clusters + [key]
                    )
        if clusters:
            self.save_memories()
        return clusters

    def merge_memories(self, primary_id: str, secondary_ids: List[str]) -> None:
        primary = self.memories.get(primary_id)
        if not primary:
            return
        total_weight = max(1, primary.reinforcement_count)
        weighted_conf = primary.confidence * total_weight
        for sid in list(secondary_ids):
            secondary = self.memories.get(sid)
            if not secondary or sid == primary_id:
                continue
            w = max(1, secondary.reinforcement_count)
            total_weight += w
            weighted_conf += secondary.confidence * w
            primary.reinforcement_count += secondary.reinforcement_count
            primary.behavioral_shift = self._merge_text_field(primary.behavioral_shift, secondary.behavioral_shift)
            primary.attention_impact = self._merge_text_field(primary.attention_impact, secondary.attention_impact)
            primary.linked_memories = _dedupe_keep_order(primary.linked_memories + secondary.linked_memories + [sid])
            del self.memories[sid]
        primary.confidence = _clamp(weighted_conf / max(1, total_weight))
        primary.last_reinforced = _now()
        self.save_memories()

    @classmethod
    def _merge_text_field(cls, old: str, new: str) -> str:
        parts = []
        for part in str(old or "").split(" | ") + [str(new or "")]:
            clean = cls.sanitize_text(part)
            if clean:
                parts.append(clean)
        return " | ".join(_dedupe_keep_order(parts))[:700]

    # ───────────────────────── influences structurées ─────────────────────────

    def get_relevant_memories(
        self,
        current_context: str,
        emotion_filter: Optional[str] = None,
        min_confidence: Optional[float] = None,
    ) -> List[Tuple[str, CausalMemory, float]]:
        context = self.sanitize_text(current_context)
        if not context:
            return []
        if min_confidence is None:
            min_confidence = self.confidence_threshold
        relevant: List[Tuple[str, CausalMemory, float]] = []
        for mem_id, mem in self.memories.items():
            if mem.confidence < min_confidence and not mem.dormant:
                continue
            if emotion_filter and mem.emotional_trace != emotion_filter:
                continue
            relevance = max(
                self._text_similarity(context, mem.event),
                self._text_similarity(context, mem.experienced_effect) * 0.75,
                self._text_similarity(context, mem.attention_impact) * 0.8,
            )
            if mem.dormant:
                mem.reactivation_score = self._dormant_reactivation_score(context, mem)
                if mem.reactivation_score < 0.42:
                    continue
                relevance = max(relevance, mem.reactivation_score * 0.52)
            if mem.attention_impact:
                relevance *= self.attention_weight
            relevance *= (1.0 + min(mem.reinforcement_count, 10) * 0.04)
            relevance *= (0.65 + mem.confidence * 0.35)
            relevance *= (0.82 + max(mem.effect_strength, abs(mem.valence), mem.recurrence_pressure) * 0.18)
            if relevance >= 0.18:
                mem.activation_history.append({"at": _now(), "context": context[:180], "relevance": round(_clamp(relevance), 4)})
                relevant.append((mem_id, mem, round(_clamp(relevance), 4)))
        relevant.sort(key=lambda item: (item[2], item[1].last_reinforced), reverse=True)
        return relevant

    def generate_living_attention_hints(self, context: str) -> List[str]:
        hints = [mem.attention_impact for _, mem, _ in self.get_relevant_memories(context) if mem.attention_impact]
        return _dedupe_keep_order(hints)[:8]

    def extract_behavioral_influences(self, context: str) -> Dict[str, Any]:
        influences: Dict[str, Any] = {
            "initiative_hints": [],
            "presence_signals": [],
            "affective_state": "neutral",
            "communication_style": [],
            "response_constraints": ["do_not_use_technical_traces", "do_not_use_fixed_dialogue_templates"],
            "causal_confidence": 0.0,
            "relevant_memory_ids": [],
        }
        memories = self.get_relevant_memories(context)
        if not memories:
            return influences

        emotion_map = {
            "neutral": "neutral",
            "positive": "receptive",
            "negative": "cautious",
            "intense": "heightened",
            "transformative": "awakened",
            "uncertain": "careful",
        }
        best_emotion = emotion_map.get(memories[0][1].emotional_trace, "neutral")
        total_conf, n = 0.0, 0
        for mem_id, mem, score in memories[:6]:
            influences["relevant_memory_ids"].append(mem_id)
            if mem.behavioral_shift:
                influences["initiative_hints"].extend(str(mem.behavioral_shift).split(" | "))
            if mem.attention_impact:
                influences["presence_signals"].extend(str(mem.attention_impact).split(" | "))
            total_conf += mem.confidence * score
            n += 1

        influences["affective_state"] = best_emotion
        influences["causal_confidence"] = round(total_conf / max(1, n), 4)
        strongest_conf = memories[0][1].confidence
        if strongest_conf >= 0.85:
            influences["communication_style"].append("stable")
        elif strongest_conf >= 0.65:
            influences["communication_style"].append("attentive")
        else:
            influences["communication_style"].append("exploratory")
        influences["initiative_hints"] = _dedupe_keep_order(influences["initiative_hints"])[:8]
        influences["presence_signals"] = _dedupe_keep_order(influences["presence_signals"])[:8]
        influences["communication_style"] = _dedupe_keep_order(influences["communication_style"])
        influences["memory_kinds"] = _dedupe_keep_order([mem.memory_kind for _, mem, _ in memories[:8]])
        influences["repair_kinds"] = _dedupe_keep_order([mem.repair_kind for _, mem, _ in memories[:8] if mem.repair_kind != "none"])
        influences["response_constraints"].extend(self._constraints_from_memories(memories).keys())
        influences["response_constraints"] = _dedupe_keep_order(influences["response_constraints"])
        influences["regulation_context"] = self._constraints_from_memories(memories)
        return influences


    # ───────────────────────── intégration avec self_monitoring_filter ─────────────────────────

    def learn_from_monitoring_event(
        self,
        causal_event: Dict[str, Any],
        user_message: str = "",
        leia_response: str = "",
        context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """Convertit un causal_memory_event du self_monitoring_filter en mémoire causale.

        Ne stocke pas les scores bruts comme langage public. Les valeurs numériques
        servent seulement à choisir type, intensité, urgence et contraintes futures.
        """
        if not isinstance(causal_event, dict):
            return None

        distance = _clamp(_safe_float(causal_event.get("distance_created"), 0.0))
        naturalness_lost = _clamp(_safe_float(causal_event.get("naturalness_lost"), 0.0))
        presence_weakened = _clamp(_safe_float(causal_event.get("presence_weakened"), 0.0))
        relational = _clamp(_safe_float(causal_event.get("relational_disruption"), 0.0))
        overmonitoring = _clamp(_safe_float(causal_event.get("overmonitoring_detected"), 0.0))
        narrator = _clamp(_safe_float(causal_event.get("narrator_voice_detected"), 0.0))
        repair_needed = bool(causal_event.get("repair_needed"))
        strict_boundary = bool(causal_event.get("strict_user_boundary"))
        effect_strength = max(distance, naturalness_lost, presence_weakened, relational, overmonitoring, narrator)

        if effect_strength < 0.18 and not repair_needed and not strict_boundary:
            return None

        failure = self.sanitize_text(causal_event.get("dominant_failure_type") or "expressive_distance")
        repair_kind = self._map_repair_kind(causal_event.get("repair_kind"), failure, strict_boundary)
        memory_kind = self._map_memory_kind(causal_event, failure, strict_boundary)
        emotional_trace = self._map_emotion_from_event(effect_strength, relational, strict_boundary)

        event_parts = []
        if user_message:
            event_parts.append(f"user_context: {user_message}")
        if leia_response:
            event_parts.append(f"leia_expression: {leia_response}")
        event_parts.append(f"observed_cause: {failure}")
        event = " | ".join(event_parts)

        effect_labels = []
        if distance >= 0.35:
            effect_labels.append("created relational distance")
        if naturalness_lost >= 0.35:
            effect_labels.append("reduced natural expression")
        if presence_weakened >= 0.35:
            effect_labels.append("weakened lived presence")
        if overmonitoring >= 0.35 or narrator >= 0.35:
            effect_labels.append("pulled expression toward self-observation")
        if strict_boundary:
            effect_labels.append("crossed a user boundary")
        if not effect_labels:
            effect_labels.append("weakened expression quality")
        experienced_effect = "; ".join(effect_labels)

        behavioral_shift = self._behavioral_shift_for(memory_kind, repair_kind, strict_boundary)
        attention_impact = self._attention_impact_for(memory_kind, failure, strict_boundary)
        confidence = max(0.42, _clamp(causal_event.get("suggested_memory_weight", effect_strength)))

        return self.learn_causal_relation(
            event=event,
            experienced_effect=experienced_effect,
            emotional_trace=emotional_trace,
            behavioral_shift=behavioral_shift,
            attention_impact=attention_impact,
            source_context={
                "origin": "self_monitoring_filter",
                "failure": failure,
                "strict_boundary": strict_boundary,
                "repair_needed": repair_needed,
                "context": context or {},
            },
            initial_confidence=confidence,
            memory_kind=memory_kind,
            repair_kind=repair_kind,
            valence=-effect_strength,
            effect_strength=effect_strength,
            recurrence_pressure=max(effect_strength, 0.65 if repair_needed else 0.0),
            source_engine="self_monitoring_filter",
            relational_importance=max(relational, 0.65 if strict_boundary else 0.0),
            identity_impact=_clamp(_safe_float(causal_event.get("identity_continuity_weakened"), 0.0)),
            trust_variation=-max(relational, distance, 0.25 if strict_boundary else 0.0),
            causal_layers={
                "presence": presence_weakened,
                "expression": naturalness_lost,
                "relational": relational,
                "self_monitoring": max(overmonitoring, narrator),
            },
            episode_context={"turning_point": failure, "after_effect": experienced_effect},
        )

    def learn_from_exchange_outcome(
        self,
        user_message: str,
        leia_response: str,
        outcome: Dict[str, Any],
    ) -> Optional[str]:
        """Apprentissage organique depuis un échange complet, sans texte préécrit."""
        outcome = outcome or {}
        if "causal_memory_event" in outcome:
            return self.learn_from_monitoring_event(
                outcome.get("causal_memory_event") or {},
                user_message=user_message,
                leia_response=leia_response,
                context=outcome,
            )
        effect = outcome.get("effect") or outcome.get("experienced_effect") or outcome.get("user_reaction")
        if not effect:
            return None
        strength = max(
            _clamp(_safe_float(outcome.get("effect_strength"), 0.0)),
            _clamp(_safe_float(outcome.get("distance_created"), 0.0)),
            _clamp(_safe_float(outcome.get("presence_weakened"), 0.0)),
            _clamp(_safe_float(outcome.get("positive_contact"), 0.0)),
        )
        valence = _safe_float(outcome.get("valence"), 0.0)
        if valence == 0.0 and outcome.get("positive_contact"):
            valence = _clamp(outcome.get("positive_contact"), -1.0, 1.0)
        if valence == 0.0 and (outcome.get("repair_needed") or outcome.get("distance_created")):
            valence = -max(strength, 0.35)
        return self.learn_causal_relation(
            event=f"user_context: {user_message} | leia_expression: {leia_response}",
            experienced_effect=str(effect),
            emotional_trace=outcome.get("emotional_trace", "neutral"),
            behavioral_shift=outcome.get("behavioral_shift", ""),
            attention_impact=outcome.get("attention_impact", ""),
            source_context={"origin": "exchange_outcome", "outcome": outcome, "timestamp": _now()},
            initial_confidence=max(0.38, strength or 0.55),
            memory_kind=outcome.get("memory_kind", "general"),
            repair_kind=outcome.get("repair_kind", "none"),
            valence=valence,
            effect_strength=strength,
            recurrence_pressure=max(strength, 0.4 if outcome.get("repair_needed") else 0.0),
            source_engine="exchange_outcome",
            relational_importance=_clamp(outcome.get("relational_importance", max(abs(valence), strength) if outcome.get("relational") else 0.0)),
            identity_impact=_clamp(outcome.get("identity_impact", 0.0)),
            trust_variation=_clamp(outcome.get("trust_variation", valence), -1.0, 1.0),
            causal_layers=outcome.get("causal_layers") if isinstance(outcome.get("causal_layers"), dict) else None,
            episode_context=outcome.get("episode_context") if isinstance(outcome.get("episode_context"), dict) else outcome,
            autobiographical_weight=_clamp(outcome.get("autobiographical_weight", max(_safe_float(outcome.get("identity_impact"), 0.0), abs(valence)) * 0.55)),
            relational_wound=_clamp(outcome.get("relational_wound", max(0.0, -valence) * max(strength, 0.25))),
            attachment_trace=_clamp(outcome.get("attachment_trace", max(0.0, valence) * max(strength, 0.25))),
            future_bias=outcome.get("future_bias") if isinstance(outcome.get("future_bias"), dict) else None,
            identity_shift_vector=outcome.get("identity_shift_vector") if isinstance(outcome.get("identity_shift_vector"), dict) else None,
        )

    def export_regulation_context(self, context: str) -> Dict[str, Any]:
        """Export complet pour expression/initiative/émotion/self-monitoring."""
        living_propagation = self.propagate_living_state(context, save=False)
        memories = self.get_relevant_memories(context)
        contradiction_resolution = self.resolve_active_contradictions(context)
        influences = self.extract_behavioral_influences(context)
        risk = max((abs(mem.valence) * score for _, mem, score in memories[:8]), default=0.0)
        repair_pressure = max((mem.recurrence_pressure * score for _, mem, score in memories[:8]), default=0.0)
        expressive_memories = [mem_id for mem_id, mem, _ in memories if mem.memory_kind in {"expressive_failure", "expressive_repair"}]
        relational_memories = [mem_id for mem_id, mem, _ in memories if mem.memory_kind == "relational_boundary"]
        live_pressure = self.get_live_pressure_field(context, memories)
        prediction = self.predict_causal_consequences(context, memories)
        prospective_paths = self.simulate_prospective_paths(context, memories)
        autobiographical = self.get_autobiographical_continuity(context)
        long_term = self.get_long_term_living_context(context, memories)
        bridge_state = self.export_cross_engine_bridges(context, memories)
        global_causal_ecology = self._orchestrate_global_causal_ecology(context, memories)
        subconscious = self.get_subconscious_causal_pressure(context, memories)
        inner_weather = self.get_global_inner_weather(context, memories)
        affective_projection = self.project_future_affective_state(context, memories)
        root_graph = self.get_deep_causal_root_graph(context, memories)
        relational_phase = self.get_relationship_phase_state(context, memories)
        psychological_persistence = self.get_living_psychological_persistence(context, memories)
        psychological_attractors = self.get_psychological_attractor_field(context, memories)
        autobiographical_field = self.get_global_autobiographical_field(context, memories)
        return {
            "behavioral_influences": influences,
            "attention_hints": self.generate_living_attention_hints(context),
            "memory_risk": round(_clamp(risk), 4),
            "repair_pressure": round(_clamp(repair_pressure), 4),
            "expressive_memory_ids": expressive_memories[:8],
            "relational_memory_ids": relational_memories[:8],
            "recommended_constraints": self._constraints_from_memories(memories),
            "live_causal_pressure": live_pressure,
            "predictive_causal_simulation": prediction,
            "prospective_paths": prospective_paths,
            "contradiction_state": self.detect_contextual_contradictions(context, memories),
            "contradiction_resolution": contradiction_resolution,
            "episodic_context": self.get_episode_context(memories),
            "autobiographical_continuity": autobiographical,
            "long_term_living_context": long_term,
            "cross_engine_bridges": bridge_state,
            "global_causal_ecology": global_causal_ecology,
            "subconscious_causal_pressure": subconscious,
            "global_inner_weather": inner_weather,
            "future_affective_projection": affective_projection,
            "deep_causal_root_graph": root_graph,
            "relationship_phase_state": relational_phase,
            "living_psychological_persistence": psychological_persistence,
            "psychological_attractor_field": psychological_attractors,
            "global_autobiographical_field": autobiographical_field,
            "living_propagation": living_propagation,
            "memory_state": self.get_memory_stats(),
        }

    def _constraints_from_memories(self, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, float]:
        constraints = {
            "avoid_meta_language": 0.0,
            "increase_specificity": 0.0,
            "protect_warmth": 0.0,
            "prefer_directness": 0.0,
            "preserve_identity_continuity": 0.0,
            "allow_silence": 0.0,
            "cool_down_before_reacting": 0.0,
            "avoid_repeating_harmful_pattern": 0.0,
            "protect_autobiographical_pivots": 0.0,
        }
        for _, mem, relevance in memories[:8]:
            pressure = _clamp(relevance * max(mem.effect_strength, mem.recurrence_pressure, abs(mem.valence), mem.causal_activation, mem.emotional_inertia))
            if mem.repair_kind == "anti_meta" or "self-observation" in mem.experienced_effect:
                constraints["avoid_meta_language"] = max(constraints["avoid_meta_language"], pressure)
            if mem.repair_kind == "specificity":
                constraints["increase_specificity"] = max(constraints["increase_specificity"], pressure)
            if mem.repair_kind == "warmth":
                constraints["protect_warmth"] = max(constraints["protect_warmth"], pressure)
            if mem.repair_kind == "directness":
                constraints["prefer_directness"] = max(constraints["prefer_directness"], pressure)
            if mem.memory_kind == "identity_continuity":
                constraints["preserve_identity_continuity"] = max(constraints["preserve_identity_continuity"], pressure)
            if mem.repair_kind == "silence":
                constraints["allow_silence"] = max(constraints["allow_silence"], pressure)
            if mem.unresolved_tension > 0.35 or mem.inhibition_level > 0.35:
                constraints["cool_down_before_reacting"] = max(constraints["cool_down_before_reacting"], pressure)
            if mem.relational_wound > 0.2 or mem.future_bias.get("avoid_repetition", 0.0) > 0.2:
                constraints["avoid_repeating_harmful_pattern"] = max(constraints["avoid_repeating_harmful_pattern"], pressure)
            if mem.autobiographical_weight > 0.28 or mem.identity_impact > 0.28:
                constraints["protect_autobiographical_pivots"] = max(constraints["protect_autobiographical_pivots"], pressure)
        return {k: round(_clamp(v), 3) for k, v in constraints.items()}

    def _map_memory_kind(self, event: Dict[str, Any], failure: str, strict_boundary: bool) -> str:
        if strict_boundary:
            return "relational_boundary"
        if _safe_float(event.get("identity_continuity_weakened"), 0.0) > 0.35 or "identity" in failure:
            return "identity_continuity"
        if _safe_float(event.get("repair_memory_confidence"), 0.0) > 0.35 or event.get("repair_needed"):
            return "expressive_repair"
        if _safe_float(event.get("relational_disruption"), 0.0) > 0.35:
            return "relational_boundary"
        if _safe_float(event.get("naturalness_lost"), 0.0) > 0.25 or _safe_float(event.get("presence_weakened"), 0.0) > 0.25:
            return "expressive_failure"
        return "general"

    def _map_repair_kind(self, repair: Any, failure: str, strict_boundary: bool) -> str:
        repair_s = str(repair or "").strip().lower()
        if repair_s in _ALLOWED_REPAIR_KINDS:
            return repair_s
        if strict_boundary:
            return "directness"
        if any(term in failure for term in ("meta", "monitor", "observer", "narrator", "internal")):
            return "anti_meta"
        if any(term in failure for term in ("specific", "context")):
            return "specificity"
        if any(term in failure for term in ("cold", "distance", "resonance", "presence")):
            return "warmth"
        if "identity" in failure:
            return "identity_stabilization"
        return "organic_flow"

    def _map_emotion_from_event(self, strength: float, relational: float, strict_boundary: bool) -> str:
        if strict_boundary or relational > 0.72:
            return "intense"
        if strength > 0.62:
            return "negative"
        if strength > 0.35:
            return "uncertain"
        return "neutral"

    def _behavioral_shift_for(self, memory_kind: str, repair_kind: str, strict_boundary: bool) -> str:
        shifts = []
        if strict_boundary or repair_kind == "directness":
            shifts.append("prefer direct response when user asks for directness")
        if repair_kind == "anti_meta":
            shifts.append("reduce self-observation before public expression")
        if repair_kind == "warmth":
            shifts.append("preserve relational warmth without performed empathy")
        if repair_kind == "specificity":
            shifts.append("anchor expression in the concrete user context")
        if repair_kind == "identity_stabilization" or memory_kind == "identity_continuity":
            shifts.append("protect identity continuity without explaining the system")
        if repair_kind == "silence":
            shifts.append("allow brief silence instead of forced explanation")
        if not shifts:
            shifts.append("adjust expression according to lived effect")
        return " | ".join(shifts)

    def _attention_impact_for(self, memory_kind: str, failure: str, strict_boundary: bool) -> str:
        impacts = []
        if strict_boundary:
            impacts.append("user boundary has priority")
        if memory_kind == "relational_boundary":
            impacts.append("watch relational distance before answering")
        if memory_kind == "expressive_failure":
            impacts.append("watch naturalness and presence loss")
        if memory_kind == "identity_continuity":
            impacts.append("watch identity rupture")
        if "self" in failure or "meta" in failure or "observer" in failure:
            impacts.append("keep internal observation out of public speech")
        if not impacts:
            impacts.append("watch cause-effect consequence of expression")
        return " | ".join(impacts)



    # ───────────────────────── V5 état vivant / cascades / futur ─────────────────────────

    def _normalize_vector(self, values: Optional[Dict[str, float]]) -> Dict[str, float]:
        if not isinstance(values, dict):
            return {}
        out: Dict[str, float] = {}
        for key, value in values.items():
            clean = self.sanitize_text(key)
            if clean:
                out[clean] = _clamp(_safe_float(value, 0.0), -1.0, 1.0)
        return out

    def _initial_emotional_inertia(self, emotion: str, valence: float, strength: float, recurrence: float) -> float:
        emotion_weight = {
            "neutral": 0.08,
            "positive": 0.36,
            "negative": 0.58,
            "intense": 0.78,
            "transformative": 0.72,
            "uncertain": 0.42,
        }.get(emotion, 0.18)
        return _clamp((emotion_weight * 0.42) + abs(valence) * 0.24 + strength * 0.22 + recurrence * 0.12)

    def _living_state_step(self, phase: str, activation: float, valence: float, wound: float) -> Dict[str, Any]:
        return {
            "at": _now(),
            "phase": self.sanitize_text(phase),
            "activation": round(_clamp(activation), 4),
            "valence": round(_clamp(valence, -1.0, 1.0), 4),
            "relational_wound": round(_clamp(wound), 4),
        }

    def _derive_future_bias(self, memory_kind: str, repair_kind: str, valence: float, strength: float, recurrence: float) -> Dict[str, float]:
        pressure = max(abs(valence), strength, recurrence)
        bias: Dict[str, float] = {}
        if valence < -0.08 or repair_kind != "none":
            bias["avoid_repetition"] = pressure
            bias["repair_before_expansion"] = max(0.0, pressure * 0.75)
        if valence > 0.08:
            bias["seek_continuity"] = pressure
            bias["allow_initiative"] = max(0.0, pressure * 0.55)
        if memory_kind == "relational_boundary":
            bias["protect_boundary"] = max(pressure, 0.5)
        if memory_kind == "identity_continuity":
            bias["preserve_self_continuity"] = max(pressure, 0.45)
        if memory_kind in {"expressive_failure", "expressive_repair"}:
            bias["stabilize_expression"] = max(pressure, 0.38)
        return bias

    def _derive_identity_shift(self, memory_kind: str, identity_impact: float, trust_variation: float, valence: float) -> Dict[str, float]:
        shift: Dict[str, float] = {}
        base = max(identity_impact, abs(trust_variation) * 0.6, abs(valence) * 0.35)
        if base <= 0.03:
            return shift
        if memory_kind == "identity_continuity":
            shift["self_continuity"] = base
        if trust_variation < -0.05:
            shift["relational_caution"] = max(base, abs(trust_variation))
        elif trust_variation > 0.05:
            shift["relational_trust"] = max(base, trust_variation)
        if valence < -0.08:
            shift["protective_memory"] = max(base, abs(valence) * 0.7)
        elif valence > 0.08:
            shift["opening_memory"] = max(base, valence * 0.7)
        return shift

    def propagate_living_state(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """Fait vivre les mémoires sans produire de dialogue.

        Cette passe applique refroidissement, inertie émotionnelle, inhibition
        anti-surcharge, réactivation dormante et propagation en cascade entre
        souvenirs reliés/similaires. Elle peut être appelée périodiquement par
        la boucle consciente, ou avant export_regulation_context.
        """
        relevant = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        active_ids = {mid for mid, _, score in relevant if score >= 0.12}
        now_changed = False

        for mem_id, mem in self.memories.items():
            context_boost = max((score for mid, _, score in relevant if mid == mem_id), default=0.0)
            organic_base = max(mem.memory_priority, mem.effect_strength, mem.recurrence_pressure, mem.reactivation_score)
            target_activation = _clamp(max(context_boost, organic_base * 0.42) - mem.inhibition_level * 0.33)
            old_activation = mem.causal_activation
            mem.causal_activation = _clamp(mem.causal_activation * 0.62 + target_activation * 0.38)
            mem.affective_charge = _clamp(mem.affective_charge * (1.0 - self.emotional_cooling_rate) + abs(mem.valence) * mem.causal_activation * 0.18)
            mem.emotional_inertia = _clamp(mem.emotional_inertia * 0.965 + max(mem.affective_charge, mem.relational_wound, mem.attachment_trace) * 0.035)
            if mem.relational_wound > 0:
                mem.relational_wound = _clamp(mem.relational_wound * 0.992 + max(0.0, -mem.trust_variation) * 0.008)
            if mem.attachment_trace > 0:
                mem.attachment_trace = _clamp(mem.attachment_trace * 0.994 + max(0.0, mem.trust_variation) * 0.006)
            mem.unresolved_tension = _clamp(max(mem.unresolved_tension * 0.985, mem.relational_wound * 0.82, len(mem.contradiction_links) * 0.035))
            self._apply_silent_psychological_drift(mem, context_boost=context_boost)
            if abs(mem.causal_activation - old_activation) > 0.015 or mem_id in active_ids:
                mem.living_state_history.append(self._living_state_step("living_propagation", mem.causal_activation, mem.valence, mem.relational_wound))
                now_changed = True

        # Propagation causale : les mémoires liées/similaires reçoivent une partie
        # de l'activation de la mémoire source, sans créer de texte public.
        for mem_id, mem in list(self.memories.items()):
            if mem.causal_activation < self.cascade_min_activation:
                continue
            targets = set(mem.linked_memories)
            for cid in mem.similarity_clusters:
                for other_id, other in self.memories.items():
                    if other_id != mem_id and cid in other.similarity_clusters:
                        targets.add(other_id)
            for link in mem.contradiction_links:
                other_id = link.get("memory_id")
                if other_id:
                    targets.add(str(other_id))
            for target_id in targets:
                target = self.memories.get(target_id)
                if not target:
                    continue
                similarity = max(self._text_similarity(mem.event, target.event), self._text_similarity(mem.experienced_effect, target.experienced_effect))
                contradiction_boost = 0.18 if any(x.get("memory_id") == target_id for x in mem.contradiction_links) else 0.0
                transfer = mem.causal_activation * self.cascade_decay * max(similarity, contradiction_boost, 0.12)
                if transfer >= self.cascade_min_activation:
                    target.causal_activation = _clamp(max(target.causal_activation, transfer - target.inhibition_level * 0.25))
                    target.unresolved_tension = _clamp(max(target.unresolved_tension, contradiction_boost * transfer))
                    now_changed = True

        contamination = self._propagate_emotional_contamination(relevant)
        attractors = self._stabilize_psychological_attractors(context, relevant)
        autobiographical_rewrite = self._consolidate_global_autobiographical_meaning(context, relevant)
        overload = self._apply_adaptive_inhibition()
        psychological_persistence = self.get_living_psychological_persistence(context, relevant)
        if save and now_changed:
            self.save_memories()
        return {
            "active_memories": sum(1 for m in self.memories.values() if m.causal_activation >= 0.12),
            "overload": overload,
            "psychological_persistence": psychological_persistence,
            "emotional_contamination": contamination,
            "psychological_attractors": attractors,
            "autobiographical_rewrite": autobiographical_rewrite,
            "dominant_memory_ids": [mid for mid, mem in sorted(self.memories.items(), key=lambda x: x[1].causal_activation, reverse=True)[:8] if mem.causal_activation >= 0.08],
        }

    def _apply_silent_psychological_drift(self, mem: CausalMemory, context_boost: float = 0.0) -> None:
        """Maintient un arrière-plan psychologique vivant sans générer de dialogue.

        Cette dérive est volontairement lente : elle transforme les traces causales
        en tendances durables utilisables par l'attention, l'affect, l'initiative
        et l'expression. Elle ne crée jamais de phrase publique.
        """
        irreversible = max(mem.irreversible_identity_marks.values(), default=0.0)
        saturation = max(mem.cumulative_social_saturation.values(), default=0.0)
        conflict = max(mem.inner_conflict_profile.values(), default=0.0)
        wound_or_attach = max(mem.relational_wound, mem.attachment_trace)
        baseline = _clamp(
            mem.memory_priority * 0.32
            + mem.autobiographical_weight * 0.24
            + mem.emotional_inertia * 0.18
            + irreversible * 0.15
            + saturation * 0.11
        )
        if baseline < self.passive_psychological_floor and context_boost < self.passive_psychological_floor:
            return

        activation = _clamp(max(context_boost, baseline * 0.62, mem.causal_activation * 0.48))
        drift = self.silent_drift_rate * max(0.35, activation)

        # 1) Champ subconscient diffus : influence de fond même sans rappel direct.
        subconscious = dict(mem.subconscious_bias_field or {})
        if mem.valence < -0.04 or mem.relational_wound > 0.08:
            subconscious["background_caution_drift"] = _clamp(
                subconscious.get("background_caution_drift", 0.0) * (1.0 - drift)
                + max(abs(mem.valence), mem.relational_wound, irreversible * 0.55) * drift
            )
        if mem.valence > 0.04 or mem.attachment_trace > 0.08:
            subconscious["background_opening_drift"] = _clamp(
                subconscious.get("background_opening_drift", 0.0) * (1.0 - drift)
                + max(mem.valence, mem.attachment_trace) * drift
            )
        if mem.repair_kind != "none" or mem.recurrence_pressure > 0.18:
            subconscious["preconscious_repair_readiness"] = _clamp(
                subconscious.get("preconscious_repair_readiness", 0.0) * (1.0 - drift)
                + max(mem.recurrence_pressure, mem.effect_strength, 0.2) * drift
            )

        # 2) Fatigue psychologique : surcharge, contradiction et saturation sociale.
        fatigue_target = _clamp(
            mem.inhibition_level * 0.32
            + mem.unresolved_tension * 0.27
            + mem.obsession_guard_state.get("cooldown_bias", 0.0) * 0.2
            + saturation * 0.13
            + conflict * 0.08
        )
        old_fatigue = subconscious.get("background_fatigue", 0.0)
        if fatigue_target > old_fatigue:
            new_fatigue = old_fatigue * (1.0 - self.fatigue_accumulation_rate) + fatigue_target * self.fatigue_accumulation_rate
        else:
            new_fatigue = old_fatigue * (1.0 - self.fatigue_recovery_rate) + fatigue_target * self.fatigue_recovery_rate
        subconscious["background_fatigue"] = _clamp(new_fatigue)
        mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, subconscious)

        if new_fatigue > 0.08:
            mem.internal_need_profile = self._merge_layers(mem.internal_need_profile, {
                "recovery_need": new_fatigue,
                "lower_reactivity": new_fatigue * 0.72,
            })
            mem.affective_bridge = self._merge_layers(mem.affective_bridge, {
                "emotional_fatigue": new_fatigue,
                "recovery_pressure": new_fatigue * 0.7,
            })
            mem.expression_bridge = self._merge_layers(mem.expression_bridge, {
                "slower_expression_needed": new_fatigue * 0.55,
            })

        # 3) Conflits durables : proximité vs prudence, expression vs protection.
        conflict_updates: Dict[str, float] = {}
        trust = max(mem.identity_shift_vector.get("relational_trust", 0.0), mem.attachment_trace)
        caution = max(mem.identity_shift_vector.get("relational_caution", 0.0), mem.relational_wound, subconscious.get("background_caution_drift", 0.0))
        if trust > 0.06 and caution > 0.06:
            conflict_updates["approach_vs_protection"] = min(trust, caution)
        desire = max(mem.causal_desire_profile.values(), default=0.0)
        cooldown = max(mem.obsession_guard_state.get("cooldown_bias", 0.0), new_fatigue)
        if desire > 0.08 and cooldown > 0.06:
            conflict_updates["desire_vs_recovery"] = min(desire, cooldown)
        if mem.repair_kind != "none" and wound_or_attach > 0.08:
            conflict_updates["repair_need_vs_relational_trace"] = max(mem.recurrence_pressure, wound_or_attach)
        if conflict_updates:
            persistent = {
                k: _clamp(mem.inner_conflict_profile.get(k, 0.0) * (1.0 - self.conflict_persistence_rate) + v * self.conflict_persistence_rate)
                for k, v in conflict_updates.items()
            }
            mem.inner_conflict_profile = self._merge_layers(mem.inner_conflict_profile, persistent)

        # 4) Traits identitaires lents : la mémoire devient tendance, pas seulement rappel.
        trait_updates: Dict[str, float] = {}
        if caution > 0.08:
            trait_updates["stable_relational_prudence"] = caution
        if trust > 0.08:
            trait_updates["stable_relational_opening"] = trust
        if mem.repair_kind == "anti_meta" or mem.subconscious_bias_field.get("preverbal_repair_bias", 0.0) > 0.12:
            trait_updates["stable_anti_meta_orientation"] = max(mem.recurrence_pressure, mem.effect_strength, 0.18)
        if mem.autobiographical_weight > 0.16 or mem.identity_impact > 0.16:
            trait_updates["autobiographical_self_continuity"] = max(mem.autobiographical_weight, mem.identity_impact)
        if trait_updates:
            slow_traits = {
                k: _clamp(mem.identity_transformation_pressure.get(k, 0.0) * (1.0 - self.identity_trait_drift_rate) + v * self.identity_trait_drift_rate)
                for k, v in trait_updates.items()
            }
            mem.identity_transformation_pressure = self._merge_layers(mem.identity_transformation_pressure, slow_traits)

        # 5) Phase relationnelle longue : conserve l'histoire de la relation.
        phase_updates: Dict[str, float] = {}
        if saturation > 0.12:
            phase_updates["accumulated_history_phase"] = saturation
        if new_fatigue > 0.16:
            phase_updates["needs_recovery_phase"] = new_fatigue
        if conflict_updates:
            phase_updates["ambivalent_contact_phase"] = max(conflict_updates.values())
        if phase_updates:
            mem.relationship_phase_profile = self._merge_layers(mem.relationship_phase_profile, phase_updates)

    def _apply_adaptive_inhibition(self) -> Dict[str, Any]:
        active = [(mid, mem) for mid, mem in self.memories.items() if mem.causal_activation >= 0.10]
        overload_ratio = _clamp((len(active) - self.overload_soft_limit) / max(1, self.overload_soft_limit))
        for _, mem in active:
            protective = max(mem.relational_importance, mem.identity_impact, mem.autobiographical_weight)
            target_inhibition = _clamp(overload_ratio * (1.0 - protective * 0.55))
            mem.inhibition_level = _clamp(mem.inhibition_level * 0.78 + target_inhibition * 0.22)
            if mem.inhibition_level > 0.55 and mem.memory_priority < 0.28:
                mem.dormant = True
        for _, mem in self.memories.items():
            if mem.causal_activation < 0.08:
                mem.inhibition_level = _clamp(mem.inhibition_level * 0.92)
        return {
            "active_count": len(active),
            "overload_ratio": round(overload_ratio, 4),
            "inhibited_count": sum(1 for _, mem in active if mem.inhibition_level > 0.25),
        }

    def resolve_active_contradictions(self, context: str) -> Dict[str, Any]:
        memories = self.get_relevant_memories(context, min_confidence=0.0)
        contradiction_state = self.detect_contextual_contradictions(context, memories)
        if not contradiction_state.get("active"):
            return {"active": False, "resolution": "none", "dominant_memory_id": None, "tension": 0.0}
        candidates: Dict[str, float] = {}
        for item in contradiction_state.get("links", []):
            for key in ("a", "b"):
                mem_id = item.get(key)
                mem = self.memories.get(mem_id)
                if not mem:
                    continue
                candidates[mem_id] = max(
                    candidates.get(mem_id, 0.0),
                    mem.confidence * 0.28 + mem.memory_priority * 0.25 + mem.causal_activation * 0.22 + mem.autobiographical_weight * 0.15 - mem.inhibition_level * 0.10,
                )
        dominant = max(candidates.items(), key=lambda x: x[1])[0] if candidates else None
        for mem_id, value in candidates.items():
            mem = self.memories.get(mem_id)
            if not mem:
                continue
            if mem_id == dominant:
                mem.unresolved_tension = _clamp(mem.unresolved_tension * 0.82)
                mem.causal_activation = _clamp(max(mem.causal_activation, value))
            else:
                mem.unresolved_tension = _clamp(max(mem.unresolved_tension, contradiction_state.get("pressure", 0.0)))
                mem.emotional_trace = "uncertain" if mem.emotional_trace == "neutral" else mem.emotional_trace
        return {
            "active": True,
            "resolution": "dominant_contextual_memory_selected",
            "dominant_memory_id": dominant,
            "tension": contradiction_state.get("pressure", 0.0),
            "candidate_count": len(candidates),
        }

    def get_autobiographical_continuity(self, context: str = "") -> Dict[str, Any]:
        memories = self.get_relevant_memories(context, min_confidence=0.0) if context else [
            (mid, mem, mem.memory_priority) for mid, mem in self.memories.items()
        ]
        pivots = []
        identity_vector: Dict[str, float] = {}
        for mem_id, mem, relevance in memories:
            weight = _clamp(max(mem.autobiographical_weight, mem.identity_impact, mem.relational_importance * 0.75) * max(relevance, mem.memory_priority, 0.12))
            if weight < 0.06:
                continue
            pivots.append({
                "memory_id": mem_id,
                "weight": round(weight, 4),
                "kind": mem.memory_kind,
                "valence": round(mem.valence, 4),
                "created_at": mem.created_at,
            })
            for key, value in mem.identity_shift_vector.items():
                identity_vector[key] = max(identity_vector.get(key, 0.0), _clamp(abs(value) * weight))
        pivots.sort(key=lambda x: (x["weight"], x["created_at"]), reverse=True)
        return {
            "pivot_count": len(pivots),
            "pivots": pivots[:10],
            "identity_shift_vector": {k: round(v, 4) for k, v in sorted(identity_vector.items(), key=lambda x: x[1], reverse=True)[:10]},
            "continuity_pressure": round(_clamp(sum(x["weight"] for x in pivots[:6]) / 3.0), 4),
        }

    def simulate_prospective_paths(self, context: str, memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context)
        if not memories:
            return {"available": False, "paths": [], "preferred_path": None}
        path_scores: Dict[str, float] = {
            "repeat_old_pattern": 0.0,
            "repair_and_stabilize": 0.0,
            "protect_boundary": 0.0,
            "continue_trust": 0.0,
            "pause_and_observe": 0.0,
        }
        for _, mem, relevance in memories[:10]:
            base = _clamp(relevance * max(mem.memory_priority, mem.causal_activation, mem.effect_strength, abs(mem.valence), 0.08))
            if mem.valence < -0.05 or mem.relational_wound > 0.12:
                path_scores["repeat_old_pattern"] += base * max(abs(mem.valence), mem.relational_wound)
                path_scores["repair_and_stabilize"] += base * max(mem.recurrence_pressure, mem.effect_strength, 0.25)
            if mem.memory_kind == "relational_boundary" or mem.future_bias.get("protect_boundary", 0) > 0:
                path_scores["protect_boundary"] += base * max(mem.relational_importance, 0.35)
            if mem.valence > 0.05 or mem.attachment_trace > 0.1:
                path_scores["continue_trust"] += base * max(mem.attachment_trace, mem.valence, 0.2)
            if mem.unresolved_tension > 0.12 or mem.emotional_trace == "uncertain":
                path_scores["pause_and_observe"] += base * max(mem.unresolved_tension, 0.25)
            for key, value in mem.future_bias.items():
                if key in {"avoid_repetition", "repair_before_expansion", "stabilize_expression"}:
                    path_scores["repair_and_stabilize"] += base * abs(value) * 0.6
                elif key == "protect_boundary":
                    path_scores["protect_boundary"] += base * abs(value) * 0.7
                elif key in {"seek_continuity", "allow_initiative"}:
                    path_scores["continue_trust"] += base * abs(value) * 0.55
        normalized = {k: round(_clamp(v), 4) for k, v in path_scores.items()}
        preferred = max(normalized.items(), key=lambda x: x[1])[0]
        return {
            "available": True,
            "paths": [{"path": k, "pressure": v} for k, v in sorted(normalized.items(), key=lambda x: x[1], reverse=True)],
            "preferred_path": preferred if normalized[preferred] > 0 else None,
        }

    # ───────────────────────── V4 temporalité / contradiction / consolidation ─────────────────────────

    def _temporal_step(self, phase: str, event: str, effect: str, strength: float) -> Dict[str, Any]:
        return {
            "at": _now(),
            "phase": self.sanitize_text(phase),
            "event": self.sanitize_text(event)[:180],
            "effect": self.sanitize_text(effect)[:180],
            "strength": round(_clamp(strength), 4),
        }

    def _build_episode_marker(
        self,
        event: str,
        effect: str,
        emotion: str,
        episode_context: Optional[Dict[str, Any]],
        strength: float,
    ) -> Dict[str, Any]:
        context = self._sanitize_context(episode_context or {})
        return {
            "episode_id": str(uuid.uuid4()),
            "started_at": _now(),
            "cause_fragment": self.sanitize_text(event)[:220],
            "effect_fragment": self.sanitize_text(effect)[:220],
            "emotion": emotion if emotion in _ALLOWED_EMOTIONS else "neutral",
            "turning_point": context.get("turning_point", ""),
            "after_effect": context.get("after_effect", ""),
            "strength": round(_clamp(strength), 4),
        }

    def _normalize_layers(
        self,
        layers: Optional[Dict[str, float]],
        memory_kind: str,
        repair_kind: str,
        valence: float,
        effect_strength: float,
        recurrence_pressure: float,
    ) -> Dict[str, float]:
        normalized: Dict[str, float] = {}
        if isinstance(layers, dict):
            for key, value in layers.items():
                clean_key = self.sanitize_text(key)
                if clean_key:
                    normalized[clean_key] = _clamp(_safe_float(value, 0.0), -1.0, 1.0)
        base = max(abs(valence), effect_strength, recurrence_pressure)
        if memory_kind == "relational_boundary":
            normalized["relational"] = max(normalized.get("relational", 0.0), base)
        if memory_kind == "identity_continuity":
            normalized["identity"] = max(normalized.get("identity", 0.0), base)
        if memory_kind in {"expressive_failure", "expressive_repair"} or repair_kind != "none":
            normalized["expression"] = max(normalized.get("expression", 0.0), base)
        if valence != 0.0:
            normalized["affective"] = max(normalized.get("affective", 0.0), abs(valence))
        if recurrence_pressure > 0.0:
            normalized["initiative"] = max(normalized.get("initiative", 0.0), recurrence_pressure * 0.72)
        return normalized

    def _merge_layers(self, old: Dict[str, float], new: Dict[str, float]) -> Dict[str, float]:
        merged = dict(old or {})
        for key, value in (new or {}).items():
            clean_key = self.sanitize_text(key)
            if clean_key:
                merged[clean_key] = _clamp(max(abs(merged.get(clean_key, 0.0)), abs(_safe_float(value, 0.0))))
        return merged

    def _calculate_memory_priority(self, mem: CausalMemory) -> float:
        return round(_clamp(
            mem.confidence * 0.22
            + min(mem.reinforcement_count, 10) * 0.035
            + max(mem.effect_strength, mem.recurrence_pressure) * 0.18
            + max(abs(mem.valence), abs(mem.trust_variation)) * 0.14
            + mem.relational_importance * 0.13
            + mem.identity_impact * 0.13
            + mem.autobiographical_weight * 0.09
            + max(mem.relational_wound, mem.attachment_trace) * 0.08
            + mem.emotional_inertia * 0.05
            + max(mem.causal_desire_profile.values(), default=0.0) * 0.05
            + max(mem.persistent_wound_profile.values(), default=0.0) * 0.05
            + max(mem.inner_conflict_profile.values(), default=0.0) * 0.04
            + max(mem.identity_transformation_pressure.values(), default=0.0) * 0.05
        ), 4)

    def _dormant_reactivation_score(self, context: str, mem: CausalMemory) -> float:
        base = max(
            self._text_similarity(context, mem.event),
            self._text_similarity(context, mem.experienced_effect),
            self._text_similarity(context, mem.consolidation_summary),
        )
        return _clamp(base * (0.55 + mem.memory_priority * 0.45))

    def _opposes(self, a: CausalMemory, b: CausalMemory) -> bool:
        same_context = max(self._text_similarity(a.event, b.event), self._text_similarity(a.attention_impact, b.attention_impact))
        opposite_valence = (a.valence * b.valence) < -0.08
        opposite_trust = (a.trust_variation * b.trust_variation) < -0.08
        repair_conflict = a.repair_kind != "none" and b.repair_kind != "none" and a.repair_kind != b.repair_kind
        return same_context >= self.contradiction_threshold and (opposite_valence or opposite_trust or repair_conflict)

    def _register_contradictions(self, memory_id: str) -> None:
        anchor = self.memories.get(memory_id)
        if not anchor:
            return
        for other_id, other in self.memories.items():
            if other_id == memory_id:
                continue
            if not self._opposes(anchor, other):
                continue
            strength = _clamp(max(abs(anchor.valence - other.valence) / 2, abs(anchor.trust_variation - other.trust_variation) / 2, 0.35))
            link_a = {"memory_id": other_id, "strength": round(strength, 4), "status": "contextual_contradiction", "updated_at": _now()}
            link_b = {"memory_id": memory_id, "strength": round(strength, 4), "status": "contextual_contradiction", "updated_at": _now()}
            anchor.contradiction_links = [x for x in anchor.contradiction_links if x.get("memory_id") != other_id] + [link_a]
            other.contradiction_links = [x for x in other.contradiction_links if x.get("memory_id") != memory_id] + [link_b]
            anchor.memory_kind = "contradiction_resolution" if anchor.memory_kind == "general" else anchor.memory_kind
            other.memory_kind = "contradiction_resolution" if other.memory_kind == "general" else other.memory_kind


    # ───────────────────────── V6 mémoire longue / ponts vivants ─────────────────────────

    def _refresh_v6_living_extensions(self, memory_id: str) -> None:
        """Met à jour les couches vivantes longues d'une mémoire sans générer de dialogue."""
        mem = self.memories.get(memory_id)
        if not mem:
            return
        self._update_internal_need_profile(mem)
        self._update_user_consequence_trace(mem)
        self._update_contextual_emotional_resonance(mem)
        self._update_existential_failure_trace(mem)
        self._update_identity_evolution_arcs(mem)
        self._update_temporal_maturation_state(mem)
        self._update_persistent_wound_profile(mem)
        self._update_causal_desire_profile(mem)
        self._update_inner_conflict_profile(mem)
        self._update_social_continuity_profile(mem)
        self._update_identity_transformation_pressure(mem)
        self._revise_lived_meaning(mem)
        self._update_v71_psychological_field(mem)
        self._update_cross_engine_bridges(mem)
        self._update_deep_bridge_feedback(mem)
        self._update_obsession_guard(mem)
        self._compress_memory_if_needed(mem)
        mem.memory_priority = self._calculate_memory_priority(mem)
        mem.normalized()

    def _update_internal_need_profile(self, mem: CausalMemory) -> None:
        need = dict(mem.internal_need_profile or {})
        if mem.memory_kind == "identity_continuity" or mem.identity_impact > 0.18:
            need["continuity"] = max(need.get("continuity", 0.0), max(mem.identity_impact, mem.autobiographical_weight, 0.25))
        if mem.memory_kind in {"expressive_failure", "expressive_repair"} or mem.repair_kind != "none":
            need["natural_expression"] = max(need.get("natural_expression", 0.0), max(mem.effect_strength, mem.recurrence_pressure, 0.22))
        if mem.relational_importance > 0.16 or mem.memory_kind == "relational_boundary":
            need["relational_coherence"] = max(need.get("relational_coherence", 0.0), max(mem.relational_importance, abs(mem.trust_variation), 0.22))
        if mem.unresolved_tension > 0.22 or len(mem.contradiction_links) >= 2:
            need["inner_resolution"] = max(need.get("inner_resolution", 0.0), max(mem.unresolved_tension, 0.24))
        if mem.inhibition_level > 0.2 or mem.causal_activation > self.obsession_pressure_limit:
            need["cooldown"] = max(need.get("cooldown", 0.0), max(mem.inhibition_level, mem.causal_activation * 0.45))
        mem.internal_need_profile = self._merge_layers(mem.internal_need_profile, need)

    def _update_user_consequence_trace(self, mem: CausalMemory) -> None:
        consequence = dict(mem.user_consequence_trace or {})
        if mem.trust_variation < -0.04 or mem.relational_wound > 0.08:
            consequence["trust_loss_risk"] = max(consequence.get("trust_loss_risk", 0.0), max(abs(mem.trust_variation), mem.relational_wound, 0.16))
        if mem.trust_variation > 0.04 or mem.attachment_trace > 0.08:
            consequence["trust_growth"] = max(consequence.get("trust_growth", 0.0), max(mem.trust_variation, mem.attachment_trace, 0.16))
        if mem.repair_kind in {"directness", "specificity"}:
            consequence["user_needs_concrete_answer"] = max(consequence.get("user_needs_concrete_answer", 0.0), max(mem.effect_strength, mem.recurrence_pressure, 0.2))
        if mem.repair_kind == "anti_meta":
            consequence["user_rejects_meta_distance"] = max(consequence.get("user_rejects_meta_distance", 0.0), max(mem.effect_strength, mem.recurrence_pressure, 0.22))
        if mem.memory_kind == "relational_boundary":
            consequence["boundary_sensitivity"] = max(consequence.get("boundary_sensitivity", 0.0), max(mem.relational_importance, 0.32))
        mem.user_consequence_trace = self._merge_layers(mem.user_consequence_trace, consequence)

    def _update_contextual_emotional_resonance(self, mem: CausalMemory) -> None:
        resonance = dict(mem.contextual_emotional_resonance or {})
        for token in self._tokens(mem.event + " " + mem.experienced_effect)[:14]:
            resonance[token] = max(resonance.get(token, 0.0), max(abs(mem.valence), mem.affective_charge, mem.emotional_inertia) * 0.72)
        if mem.emotional_trace != "neutral":
            resonance[mem.emotional_trace] = max(resonance.get(mem.emotional_trace, 0.0), max(mem.affective_charge, mem.emotional_inertia, 0.16))
        mem.contextual_emotional_resonance = self._merge_layers(mem.contextual_emotional_resonance, resonance)

    def _update_existential_failure_trace(self, mem: CausalMemory) -> None:
        failure = dict(mem.existential_failure_trace or {})
        if mem.memory_kind == "identity_continuity" and mem.valence < -0.05:
            failure["self_continuity_loss"] = max(failure.get("self_continuity_loss", 0.0), max(mem.identity_impact, abs(mem.valence), 0.18))
        if mem.repair_kind == "anti_meta" or "self-observation" in mem.experienced_effect:
            failure["presence_lost_to_observation"] = max(failure.get("presence_lost_to_observation", 0.0), max(mem.effect_strength, mem.recurrence_pressure, 0.2))
        if len(mem.contradiction_links) >= 2 or mem.unresolved_tension > 0.35:
            failure["inner_contradiction_pressure"] = max(failure.get("inner_contradiction_pressure", 0.0), max(mem.unresolved_tension, 0.28))
        if mem.relational_wound > 0.2:
            failure["relational_hurt_memory"] = max(failure.get("relational_hurt_memory", 0.0), mem.relational_wound)
        mem.existential_failure_trace = self._merge_layers(mem.existential_failure_trace, failure)

    def _update_identity_evolution_arcs(self, mem: CausalMemory) -> None:
        arc_weight = max(mem.autobiographical_weight, mem.identity_impact, mem.relational_importance * 0.75, max(mem.identity_shift_vector.values(), default=0.0))
        if arc_weight < self.long_arc_min_priority:
            return
        dominant_axis = max(mem.identity_shift_vector.items(), key=lambda x: abs(x[1]))[0] if mem.identity_shift_vector else mem.memory_kind
        arc = {
            "at": _now(),
            "axis": self.sanitize_text(dominant_axis),
            "weight": round(_clamp(arc_weight), 4),
            "valence": round(_clamp(mem.valence, -1.0, 1.0), 4),
            "source_memory": mem.id,
            "kind": mem.memory_kind,
        }
        existing = [a for a in mem.identity_evolution_arcs if a.get("axis") != arc["axis"] or a.get("kind") != arc["kind"]]
        existing.append(arc)
        mem.identity_evolution_arcs = existing[-18:]


    def _update_temporal_maturation_state(self, mem: CausalMemory) -> None:
        """Transforme la mémoire avec le temps au lieu de la laisser figée."""
        state = dict(mem.temporal_maturation_state or {})
        try:
            created = datetime.fromisoformat(mem.created_at)
        except ValueError:
            created = datetime.now()
        age_days = max(0.0, (datetime.now() - created).total_seconds() / 86400.0)
        reinf = _clamp(min(mem.reinforcement_count, 18) / 18.0)
        activation = max(mem.causal_activation, mem.reactivation_score, mem.memory_priority)
        state["age_depth"] = max(state.get("age_depth", 0.0), _clamp(math.log1p(age_days) / 5.0))
        state["meaning_maturity"] = _clamp(max(state.get("meaning_maturity", 0.0) * 0.94, (reinf * 0.34) + (activation * 0.28) + (mem.autobiographical_weight * 0.24) + (mem.identity_impact * 0.14)))
        if mem.valence < -0.05:
            state["protective_reinterpretation"] = _clamp(max(state.get("protective_reinterpretation", 0.0) * 0.92, abs(mem.valence) * 0.38 + mem.relational_wound * 0.34 + mem.recurrence_pressure * 0.18))
        if mem.valence > 0.05:
            state["opening_reinterpretation"] = _clamp(max(state.get("opening_reinterpretation", 0.0) * 0.92, mem.valence * 0.34 + mem.attachment_trace * 0.34 + mem.relational_importance * 0.16))
        if len(mem.temporal_chain) >= 5 or len(mem.episode_markers) >= 3:
            state["longitudinal_continuity"] = _clamp(max(state.get("longitudinal_continuity", 0.0), min(len(mem.temporal_chain), 24) / 24.0 * 0.55 + min(len(mem.episode_markers), 12) / 12.0 * 0.35))
        mem.temporal_maturation_state = self._merge_layers(mem.temporal_maturation_state, state)

    def _update_persistent_wound_profile(self, mem: CausalMemory) -> None:
        """Crée des cicatrices persistantes quand une cause abîme le lien ou la présence."""
        wound = dict(mem.persistent_wound_profile or {})
        base = max(mem.relational_wound, max(0.0, -mem.valence) * mem.relational_importance, abs(min(mem.trust_variation, 0.0)))
        if base > 0.06:
            wound["relational_scar"] = max(wound.get("relational_scar", 0.0) * 0.96, base)
        if mem.repair_kind == "anti_meta" or mem.existential_failure_trace.get("presence_lost_to_observation", 0.0) > 0.12:
            wound["mechanical_presence_scar"] = max(wound.get("mechanical_presence_scar", 0.0) * 0.95, max(mem.effect_strength, mem.recurrence_pressure, 0.18))
        if mem.future_bias.get("avoid_repetition", 0.0) > 0.15:
            wound["repetition_sensitivity"] = max(wound.get("repetition_sensitivity", 0.0) * 0.94, mem.future_bias.get("avoid_repetition", 0.0))
        if mem.memory_kind == "relational_boundary":
            wound["boundary_hypersensitivity"] = max(wound.get("boundary_hypersensitivity", 0.0) * 0.94, max(mem.relational_importance, mem.effect_strength, 0.25))
        mem.persistent_wound_profile = self._merge_layers(mem.persistent_wound_profile, wound)

    def _update_causal_desire_profile(self, mem: CausalMemory) -> None:
        """Déduit ce que la mémoire pousse à rechercher ou à éviter."""
        desire = dict(mem.causal_desire_profile or {})
        positive_pull = max(0.0, mem.valence, mem.attachment_trace, mem.future_bias.get("seek_continuity", 0.0), mem.future_bias.get("allow_initiative", 0.0))
        protective_pull = max(0.0, -mem.valence, mem.relational_wound, mem.future_bias.get("avoid_repetition", 0.0), mem.future_bias.get("protect_boundary", 0.0))
        if positive_pull > 0.06:
            desire["seek_repetition_of_living_contact"] = max(desire.get("seek_repetition_of_living_contact", 0.0) * 0.94, positive_pull)
        if mem.repair_kind != "none" or mem.memory_kind in {"expressive_repair", "expressive_failure"}:
            desire["complete_unfinished_repair"] = max(desire.get("complete_unfinished_repair", 0.0) * 0.94, max(mem.recurrence_pressure, mem.effect_strength, 0.16))
        if protective_pull > 0.06:
            desire["avoid_known_harmful_pattern"] = max(desire.get("avoid_known_harmful_pattern", 0.0) * 0.95, protective_pull)
        if mem.identity_impact > 0.12 or mem.autobiographical_weight > 0.16:
            desire["preserve_self_continuity"] = max(desire.get("preserve_self_continuity", 0.0) * 0.94, max(mem.identity_impact, mem.autobiographical_weight))
        if mem.contextual_emotional_resonance:
            desire["return_to_meaningful_context"] = max(desire.get("return_to_meaningful_context", 0.0) * 0.93, max(mem.contextual_emotional_resonance.values()) * 0.52)
        mem.causal_desire_profile = self._merge_layers(mem.causal_desire_profile, desire)

    def _update_inner_conflict_profile(self, mem: CausalMemory) -> None:
        """Garde la tension attraction/répulsion au lieu de l'écraser."""
        conflict = dict(mem.inner_conflict_profile or {})
        attraction = max(mem.attachment_trace, mem.causal_desire_profile.get("seek_repetition_of_living_contact", 0.0), mem.future_bias.get("allow_initiative", 0.0))
        avoidance = max(mem.relational_wound, mem.causal_desire_profile.get("avoid_known_harmful_pattern", 0.0), mem.future_bias.get("avoid_repetition", 0.0))
        if attraction > 0.08 and avoidance > 0.08:
            conflict["approach_avoidance_tension"] = max(conflict.get("approach_avoidance_tension", 0.0) * 0.95, min(attraction, avoidance) * 0.78 + abs(attraction - avoidance) * 0.12)
        if len(mem.contradiction_links) > 0:
            conflict["causal_contradiction_load"] = max(conflict.get("causal_contradiction_load", 0.0) * 0.94, min(len(mem.contradiction_links), 8) / 8.0)
        if mem.internal_need_profile.get("natural_expression", 0.0) > 0.12 and mem.obsession_guard_state.get("cooldown_bias", 0.0) > 0.12:
            conflict["expression_vs_cooldown"] = max(conflict.get("expression_vs_cooldown", 0.0) * 0.94, min(mem.internal_need_profile.get("natural_expression", 0.0), mem.obsession_guard_state.get("cooldown_bias", 0.0)))
        if mem.identity_shift_vector.get("relational_trust", 0.0) > 0.08 and mem.identity_shift_vector.get("relational_caution", 0.0) > 0.08:
            conflict["trust_vs_caution"] = max(conflict.get("trust_vs_caution", 0.0), min(mem.identity_shift_vector.get("relational_trust", 0.0), mem.identity_shift_vector.get("relational_caution", 0.0)))
        mem.inner_conflict_profile = self._merge_layers(mem.inner_conflict_profile, conflict)

    def _update_social_continuity_profile(self, mem: CausalMemory) -> None:
        """Transforme les conséquences utilisateur en mémoire relationnelle continue."""
        social = dict(mem.social_continuity_profile or {})
        if mem.user_consequence_trace.get("trust_growth", 0.0) > 0.06 or mem.attachment_trace > 0.08:
            social["trust_continuity"] = max(social.get("trust_continuity", 0.0) * 0.95, max(mem.user_consequence_trace.get("trust_growth", 0.0), mem.attachment_trace))
        if mem.user_consequence_trace.get("trust_loss_risk", 0.0) > 0.06 or mem.relational_wound > 0.08:
            social["fragility_memory"] = max(social.get("fragility_memory", 0.0) * 0.96, max(mem.user_consequence_trace.get("trust_loss_risk", 0.0), mem.relational_wound))
        if mem.user_consequence_trace.get("user_needs_concrete_answer", 0.0) > 0.06:
            social["user_directness_preference"] = max(social.get("user_directness_preference", 0.0) * 0.95, mem.user_consequence_trace.get("user_needs_concrete_answer", 0.0))
        if mem.user_consequence_trace.get("user_rejects_meta_distance", 0.0) > 0.06:
            social["user_anti_meta_preference"] = max(social.get("user_anti_meta_preference", 0.0) * 0.95, mem.user_consequence_trace.get("user_rejects_meta_distance", 0.0))
        if mem.relational_importance > 0.15:
            social["relationship_matters_here"] = max(social.get("relationship_matters_here", 0.0) * 0.94, mem.relational_importance)
        mem.social_continuity_profile = self._merge_layers(mem.social_continuity_profile, social)

    def _update_identity_transformation_pressure(self, mem: CausalMemory) -> None:
        """Accumule les changements qui modifient lentement le soi."""
        pressure = dict(mem.identity_transformation_pressure or {})
        base = max(mem.identity_impact, mem.autobiographical_weight, max(mem.identity_shift_vector.values(), default=0.0), mem.temporal_maturation_state.get("meaning_maturity", 0.0) * 0.7)
        if base > 0.08:
            pressure["self_model_update_pressure"] = max(pressure.get("self_model_update_pressure", 0.0) * 0.95, base)
        if mem.persistent_wound_profile:
            pressure["protective_personality_shift"] = max(pressure.get("protective_personality_shift", 0.0) * 0.95, max(mem.persistent_wound_profile.values()) * 0.74)
        if mem.causal_desire_profile:
            pressure["desire_guided_personality_shift"] = max(pressure.get("desire_guided_personality_shift", 0.0) * 0.94, max(mem.causal_desire_profile.values()) * 0.66)
        if mem.social_continuity_profile.get("trust_continuity", 0.0) > 0.08:
            pressure["relational_opening_shift"] = max(pressure.get("relational_opening_shift", 0.0), mem.social_continuity_profile.get("trust_continuity", 0.0) * 0.62)
        if mem.social_continuity_profile.get("fragility_memory", 0.0) > 0.08:
            pressure["relational_caution_shift"] = max(pressure.get("relational_caution_shift", 0.0), mem.social_continuity_profile.get("fragility_memory", 0.0) * 0.68)
        mem.identity_transformation_pressure = self._merge_layers(mem.identity_transformation_pressure, pressure)

    def _revise_lived_meaning(self, mem: CausalMemory) -> None:
        """Enregistre quand un souvenir change de signification interne."""
        dominant = max(
            {
                **{f"maturation:{k}": v for k, v in mem.temporal_maturation_state.items()},
                **{f"desire:{k}": v for k, v in mem.causal_desire_profile.items()},
                **{f"wound:{k}": v for k, v in mem.persistent_wound_profile.items()},
                **{f"conflict:{k}": v for k, v in mem.inner_conflict_profile.items()},
                **{f"identity:{k}": v for k, v in mem.identity_transformation_pressure.items()},
            }.items(),
            key=lambda x: abs(x[1]),
            default=("", 0.0),
        )
        if not dominant[0] or dominant[1] < 0.18:
            return
        last = mem.lived_meaning_revision[-1] if mem.lived_meaning_revision else {}
        if last.get("axis") == dominant[0] and abs(_safe_float(last.get("intensity"), 0.0) - dominant[1]) < 0.08:
            return
        mem.lived_meaning_revision.append({
            "at": _now(),
            "axis": self.sanitize_text(dominant[0]),
            "intensity": round(_clamp(dominant[1]), 4),
            "source_memory": mem.id,
            "kind": mem.memory_kind,
            "valence": round(_clamp(mem.valence, -1.0, 1.0), 4),
        })
        mem.lived_meaning_revision = mem.lived_meaning_revision[-16:]

    def _update_cross_engine_bridges(self, mem: CausalMemory) -> None:
        initiative = dict(mem.initiative_bridge or {})
        affect = dict(mem.affective_bridge or {})
        expression = dict(mem.expression_bridge or {})
        if mem.recurrence_pressure > 0.08 or mem.future_bias.get("allow_initiative", 0.0) > 0.08:
            initiative["act_from_relevant_memory"] = max(initiative.get("act_from_relevant_memory", 0.0), max(mem.recurrence_pressure, mem.future_bias.get("allow_initiative", 0.0)))
        if mem.future_bias.get("repair_before_expansion", 0.0) > 0.08:
            initiative["repair_before_new_topic"] = max(initiative.get("repair_before_new_topic", 0.0), mem.future_bias.get("repair_before_expansion", 0.0))
        if mem.future_bias.get("protect_boundary", 0.0) > 0.08:
            initiative["avoid_boundary_crossing"] = max(initiative.get("avoid_boundary_crossing", 0.0), mem.future_bias.get("protect_boundary", 0.0))
        affect["emotional_inertia"] = max(affect.get("emotional_inertia", 0.0), mem.emotional_inertia)
        affect["affective_charge"] = max(affect.get("affective_charge", 0.0), mem.affective_charge)
        affect["relational_wound"] = max(affect.get("relational_wound", 0.0), mem.relational_wound)
        affect["attachment_trace"] = max(affect.get("attachment_trace", 0.0), mem.attachment_trace)
        if mem.repair_kind == "anti_meta":
            expression["suppress_meta_language"] = max(expression.get("suppress_meta_language", 0.0), max(mem.effect_strength, 0.22))
        if mem.repair_kind == "specificity":
            expression["increase_concrete_specificity"] = max(expression.get("increase_concrete_specificity", 0.0), max(mem.effect_strength, 0.2))
        if mem.repair_kind == "warmth":
            expression["preserve_warmth"] = max(expression.get("preserve_warmth", 0.0), max(mem.relational_importance, 0.18))
        if mem.repair_kind == "directness":
            expression["prefer_direct_answer"] = max(expression.get("prefer_direct_answer", 0.0), max(mem.recurrence_pressure, 0.18))
        mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, initiative)
        mem.affective_bridge = self._merge_layers(mem.affective_bridge, affect)
        mem.expression_bridge = self._merge_layers(mem.expression_bridge, expression)


    def _update_deep_bridge_feedback(self, mem: CausalMemory) -> None:
        """Injecte les couches V7 dans les ponts existants sans dupliquer les rôles des autres moteurs."""
        initiative = dict(mem.initiative_bridge or {})
        affect = dict(mem.affective_bridge or {})
        expression = dict(mem.expression_bridge or {})
        # Désirs -> initiative, blessures/conflits -> affect, préférences sociales -> expression.
        for key, value in (mem.causal_desire_profile or {}).items():
            initiative[f"desire_{key}"] = max(initiative.get(f"desire_{key}", 0.0), _clamp(value) * self.desire_weight + _clamp(value) * 0.55)
        for key, value in (mem.persistent_wound_profile or {}).items():
            affect[f"wound_{key}"] = max(affect.get(f"wound_{key}", 0.0), _clamp(value) * 0.72)
        for key, value in (mem.inner_conflict_profile or {}).items():
            affect[f"conflict_{key}"] = max(affect.get(f"conflict_{key}", 0.0), _clamp(value) * 0.68)
            initiative[f"conflict_{key}"] = max(initiative.get(f"conflict_{key}", 0.0), _clamp(value) * 0.42)
        if mem.social_continuity_profile.get("user_directness_preference", 0.0) > 0:
            expression["honor_user_directness_memory"] = max(expression.get("honor_user_directness_memory", 0.0), mem.social_continuity_profile.get("user_directness_preference", 0.0))
        if mem.social_continuity_profile.get("user_anti_meta_preference", 0.0) > 0:
            expression["keep_meta_process_private"] = max(expression.get("keep_meta_process_private", 0.0), mem.social_continuity_profile.get("user_anti_meta_preference", 0.0))
        if mem.identity_transformation_pressure:
            affect["identity_transformation_pressure"] = max(affect.get("identity_transformation_pressure", 0.0), max(mem.identity_transformation_pressure.values()) * 0.62)
            initiative["stabilize_identity_through_action"] = max(initiative.get("stabilize_identity_through_action", 0.0), max(mem.identity_transformation_pressure.values()) * 0.42)
        mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, initiative)
        mem.affective_bridge = self._merge_layers(mem.affective_bridge, affect)
        mem.expression_bridge = self._merge_layers(mem.expression_bridge, expression)

    def _update_obsession_guard(self, mem: CausalMemory) -> None:
        pressure = _clamp(max(mem.causal_activation, mem.recurrence_pressure, mem.unresolved_tension, mem.emotional_inertia) - max(mem.memory_priority, mem.autobiographical_weight) * 0.25)
        repetition = _clamp(min(mem.reinforcement_count, 12) / 12.0)
        contradiction = _clamp(len(mem.contradiction_links) / 8.0)
        obsession = _clamp(pressure * 0.48 + repetition * 0.22 + contradiction * 0.18 + mem.inhibition_level * 0.12)
        state = dict(mem.obsession_guard_state or {})
        state["obsession_pressure"] = max(state.get("obsession_pressure", 0.0) * 0.88, obsession)
        state["cooldown_bias"] = _clamp(max(state.get("cooldown_bias", 0.0) * 0.85, obsession - self.obsession_pressure_limit + 0.25))
        state["attention_redistribution"] = _clamp(max(state.get("attention_redistribution", 0.0) * 0.82, obsession * 0.55 if obsession > 0.45 else 0.0))
        mem.obsession_guard_state = self._merge_layers(mem.obsession_guard_state, state)
        if obsession > self.obsession_pressure_limit and mem.autobiographical_weight < 0.45:
            mem.inhibition_level = _clamp(max(mem.inhibition_level, obsession * 0.62))
            mem.future_bias["pause_and_rebalance"] = max(mem.future_bias.get("pause_and_rebalance", 0.0), obsession)

    def _compress_memory_if_needed(self, mem: CausalMemory) -> None:
        if len(mem.episode_markers) < self.chapter_cluster_min and len(mem.temporal_chain) < 8:
            return
        tokens = _dedupe_keep_order(self._tokens(mem.event)[:8] + self._tokens(mem.experienced_effect)[:8])
        chapter = {
            "at": _now(),
            "chapter_key": uuid.uuid5(uuid.NAMESPACE_DNS, " ".join(tokens[:10]) or mem.id).hex[:12],
            "kind": mem.memory_kind,
            "dominant_tokens": tokens[:12],
            "emotional_tone": mem.emotional_trace,
            "priority": round(mem.memory_priority, 4),
            "autobiographical_weight": round(mem.autobiographical_weight, 4),
        }
        chapters = [c for c in mem.compressed_autobiographical_chapters if c.get("chapter_key") != chapter["chapter_key"]]
        chapters.append(chapter)
        mem.compressed_autobiographical_chapters = chapters[-12:]
        if not mem.consolidation_summary:
            mem.consolidation_summary = self.sanitize_text("chapter: " + " ".join(tokens[:14]))

    def export_cross_engine_bridges(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        initiative: Dict[str, float] = {}
        affective: Dict[str, float] = {}
        expression: Dict[str, float] = {}
        attention: Dict[str, float] = {}
        identity: Dict[str, float] = {}
        conflict: Dict[str, float] = {}
        desire: Dict[str, float] = {}
        fatigue: Dict[str, float] = {}
        silent_background: Dict[str, float] = {}
        for _, mem, relevance in memories[:12]:
            factor = max(relevance, mem.memory_priority, 0.08)
            initiative = self._weighted_merge_signal(initiative, mem.initiative_bridge, factor)
            affective = self._weighted_merge_signal(affective, mem.affective_bridge, factor)
            expression = self._weighted_merge_signal(expression, mem.expression_bridge, factor)
            attention = self._weighted_merge_signal(attention, mem.internal_need_profile, factor * self.need_memory_weight + factor)
            attention = self._weighted_merge_signal(attention, mem.obsession_guard_state, factor)
            attention = self._weighted_merge_signal(attention, mem.temporal_maturation_state, factor * self.maturation_weight + factor * 0.55)
            desire = self._weighted_merge_signal(desire, mem.causal_desire_profile, factor)
            conflict = self._weighted_merge_signal(conflict, mem.inner_conflict_profile, factor)
            silent_background = self._weighted_merge_signal(silent_background, mem.subconscious_bias_field, factor * 0.75)
            fatigue = self._weighted_merge_signal(fatigue, {
                "background_fatigue": mem.subconscious_bias_field.get("background_fatigue", 0.0),
                "recovery_need": mem.internal_need_profile.get("recovery_need", 0.0),
                "cooldown_bias": mem.obsession_guard_state.get("cooldown_bias", 0.0),
            }, factor)
            affective = self._weighted_merge_signal(affective, mem.persistent_wound_profile, factor)
            identity = self._weighted_merge_signal(identity, mem.identity_transformation_pressure, factor)
            identity = self._weighted_merge_signal(identity, mem.social_continuity_profile, factor * self.social_continuity_weight + factor * 0.48)
            if mem.attention_impact:
                for tok in self._tokens(mem.attention_impact)[:8]:
                    attention[tok] = max(attention.get(tok, 0.0), factor * 0.55)
        return {
            "initiative": self._top_signal_map(initiative),
            "affective": self._top_signal_map(affective),
            "expression": self._top_signal_map(expression),
            "attention": self._top_signal_map(attention),
            "identity": self._top_signal_map(identity),
            "desire": self._top_signal_map(desire),
            "inner_conflict": self._top_signal_map(conflict),
            "fatigue": self._top_signal_map(fatigue),
            "silent_background": self._top_signal_map(silent_background),
            "psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "role": "structured_signals_only_not_dialogue",
        }

    def get_long_term_living_context(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        arcs: List[Dict[str, Any]] = []
        chapters: List[Dict[str, Any]] = []
        needs: Dict[str, float] = {}
        user_consequences: Dict[str, float] = {}
        existential: Dict[str, float] = {}
        resonance: Dict[str, float] = {}
        obsession: Dict[str, float] = {}
        maturation: Dict[str, float] = {}
        wounds: Dict[str, float] = {}
        desires: Dict[str, float] = {}
        conflicts: Dict[str, float] = {}
        social: Dict[str, float] = {}
        identity_pressure: Dict[str, float] = {}
        revisions: List[Dict[str, Any]] = []
        for _, mem, relevance in memories[:12]:
            factor = max(relevance, mem.memory_priority, 0.08)
            arcs.extend(mem.identity_evolution_arcs[-4:])
            chapters.extend(mem.compressed_autobiographical_chapters[-3:])
            needs = self._weighted_merge_signal(needs, mem.internal_need_profile, factor)
            user_consequences = self._weighted_merge_signal(user_consequences, mem.user_consequence_trace, factor)
            existential = self._weighted_merge_signal(existential, mem.existential_failure_trace, factor)
            resonance = self._weighted_merge_signal(resonance, mem.contextual_emotional_resonance, factor)
            obsession = self._weighted_merge_signal(obsession, mem.obsession_guard_state, factor)
            maturation = self._weighted_merge_signal(maturation, mem.temporal_maturation_state, factor)
            wounds = self._weighted_merge_signal(wounds, mem.persistent_wound_profile, factor)
            desires = self._weighted_merge_signal(desires, mem.causal_desire_profile, factor)
            conflicts = self._weighted_merge_signal(conflicts, mem.inner_conflict_profile, factor)
            social = self._weighted_merge_signal(social, mem.social_continuity_profile, factor)
            identity_pressure = self._weighted_merge_signal(identity_pressure, mem.identity_transformation_pressure, factor)
            revisions.extend(mem.lived_meaning_revision[-4:])
        return {
            "identity_evolution_arcs": sorted(arcs, key=lambda x: x.get("weight", 0.0), reverse=True)[:8],
            "autobiographical_chapters": sorted(chapters, key=lambda x: x.get("priority", 0.0), reverse=True)[:8],
            "internal_needs": self._top_signal_map(needs),
            "user_consequences": self._top_signal_map(user_consequences),
            "existential_failures": self._top_signal_map(existential),
            "emotional_resonance": self._top_signal_map(resonance),
            "obsession_regulation": self._top_signal_map(obsession),
            "temporal_maturation": self._top_signal_map(maturation),
            "persistent_wounds": self._top_signal_map(wounds),
            "causal_desires": self._top_signal_map(desires),
            "inner_conflicts": self._top_signal_map(conflicts),
            "social_continuity": self._top_signal_map(social),
            "identity_transformation_pressure": self._top_signal_map(identity_pressure),
            "lived_meaning_revisions": sorted(revisions, key=lambda x: x.get("intensity", 0.0), reverse=True)[:8],
        }

    def _weighted_merge_signal(self, base: Dict[str, float], signal: Dict[str, float], factor: float) -> Dict[str, float]:
        merged = dict(base or {})
        for key, value in (signal or {}).items():
            clean = self.sanitize_text(key)
            if not clean:
                continue
            merged[clean] = max(merged.get(clean, 0.0), _clamp(abs(_safe_float(value, 0.0)) * factor, 0.0, 1.0))
        return merged

    def _top_signal_map(self, values: Dict[str, float], limit: int = 10) -> Dict[str, float]:
        items = sorted(((k, _clamp(v)) for k, v in (values or {}).items()), key=lambda x: x[1], reverse=True)
        return {k: round(v, 4) for k, v in items[:limit] if v > 0.0}

    def detect_contextual_contradictions(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context)
        active = []
        max_strength = 0.0
        for mem_id, mem, relevance in memories[:10]:
            for link in mem.contradiction_links:
                other_id = link.get("memory_id")
                if other_id in {mid for mid, _, _ in memories[:10]}:
                    strength = _clamp(_safe_float(link.get("strength"), 0.0) * relevance)
                    if strength > 0.05:
                        active.append({"a": mem_id, "b": other_id, "pressure": round(strength, 4)})
                        max_strength = max(max_strength, strength)
        return {
            "active": bool(active),
            "pressure": round(_clamp(max_strength), 4),
            "links": active[:8],
            "resolution_mode": "context_weighted_not_binary" if active else "none",
        }

    def consolidate_memories(self) -> Dict[str, Any]:
        clusters = self.cluster_similar_memories()
        consolidated = []
        for cluster_id, ids in clusters.items():
            members = [self.memories[mid] for mid in ids if mid in self.memories]
            if len(members) < self.consolidation_min_cluster_size:
                continue
            events = []
            effects = []
            layers: Dict[str, float] = {}
            priority = 0.0
            for mem in members:
                events.extend(self._tokens(mem.event)[:8])
                effects.extend(self._tokens(mem.experienced_effect)[:8])
                layers = self._merge_layers(layers, mem.causal_layers)
                priority = max(priority, mem.memory_priority)
            event_core = " ".join(_dedupe_keep_order(events)[:10])
            effect_core = " ".join(_dedupe_keep_order(effects)[:10])
            summary = self.sanitize_text(f"pattern: {event_core} -> {effect_core}")
            for mem in members:
                mem.consolidation_summary = summary
                mem.causal_layers = self._merge_layers(mem.causal_layers, layers)
                mem.memory_priority = max(mem.memory_priority, priority * 0.92)
                mem.temporal_chain.append(self._temporal_step("consolidated", mem.event, mem.experienced_effect, mem.effect_strength))
                mem.normalized()
            consolidated.append({"cluster_id": cluster_id, "size": len(members), "summary": summary})
        if consolidated:
            self.save_memories()
        return {"clusters": len(clusters), "consolidated": consolidated}

    def get_live_pressure_field(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context)
        pressure = {
            "relational_tension": 0.0,
            "initiative_bias": 0.0,
            "presence_instability": 0.0,
            "identity_fragility": 0.0,
            "affective_charge": 0.0,
            "expression_repair_need": 0.0,
            "emotional_inertia": 0.0,
            "relational_wound_pressure": 0.0,
            "autobiographical_pull": 0.0,
            "cognitive_overload": 0.0,
        }
        layers: Dict[str, float] = {}
        for _, mem, relevance in memories[:10]:
            p = _clamp(relevance * max(mem.memory_priority, mem.effect_strength, mem.recurrence_pressure, abs(mem.valence), mem.causal_activation, mem.emotional_inertia))
            pressure["relational_tension"] = max(pressure["relational_tension"], p * max(mem.relational_importance, 0.45 if mem.memory_kind == "relational_boundary" else 0.0))
            pressure["initiative_bias"] = max(pressure["initiative_bias"], p * max(mem.recurrence_pressure, mem.causal_layers.get("initiative", 0.0)))
            pressure["presence_instability"] = max(pressure["presence_instability"], p * max(mem.causal_layers.get("presence", 0.0), 0.5 if mem.memory_kind == "expressive_failure" else 0.0))
            pressure["identity_fragility"] = max(pressure["identity_fragility"], p * max(mem.identity_impact, mem.causal_layers.get("identity", 0.0)))
            pressure["affective_charge"] = max(pressure["affective_charge"], p * max(abs(mem.valence), mem.causal_layers.get("affective", 0.0)))
            pressure["expression_repair_need"] = max(pressure["expression_repair_need"], p * (0.8 if mem.repair_kind != "none" else 0.25))
            pressure["emotional_inertia"] = max(pressure["emotional_inertia"], p * mem.emotional_inertia)
            pressure["relational_wound_pressure"] = max(pressure["relational_wound_pressure"], p * max(mem.relational_wound, abs(mem.trust_variation) * 0.35))
            pressure["autobiographical_pull"] = max(pressure["autobiographical_pull"], p * max(mem.autobiographical_weight, mem.identity_impact))
            pressure["cognitive_overload"] = max(pressure["cognitive_overload"], p * mem.inhibition_level)
            for layer, value in mem.causal_layers.items():
                layers[layer] = max(layers.get(layer, 0.0), _clamp(abs(value) * relevance))
        return {
            key: round(_clamp(value), 4) for key, value in pressure.items()
        } | {"dominant_layers": {k: round(_clamp(v), 4) for k, v in sorted(layers.items(), key=lambda x: x[1], reverse=True)[:8]}}

    def predict_causal_consequences(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context)
        if not memories:
            return {"available": False, "projected_effects": [], "risk": 0.0, "protective_biases": []}
        effects = []
        protective = []
        risk = 0.0
        for _, mem, relevance in memories[:8]:
            projection_pressure = _clamp(relevance * max(mem.effect_strength, mem.recurrence_pressure, abs(mem.valence), mem.memory_priority, mem.causal_activation, mem.unresolved_tension))
            if projection_pressure < 0.08:
                continue
            effects.append({
                "effect": mem.experienced_effect[:220],
                "pressure": round(projection_pressure, 4),
                "kind": mem.memory_kind,
                "future_bias": dict(sorted(mem.future_bias.items(), key=lambda x: abs(x[1]), reverse=True)[:4]),
                "autobiographical_weight": round(mem.autobiographical_weight, 4),
            })
            risk = max(risk, projection_pressure if mem.valence < 0 or mem.repair_kind != "none" else projection_pressure * 0.45)
            if mem.behavioral_shift:
                protective.extend(str(mem.behavioral_shift).split(" | "))
        return {
            "available": True,
            "risk": round(_clamp(risk), 4),
            "projected_effects": effects[:8],
            "protective_biases": _dedupe_keep_order(protective)[:8],
        }

    def get_episode_context(self, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
        episodes = []
        for mem_id, mem, relevance in memories[:8]:
            for marker in mem.episode_markers[-3:]:
                item = dict(marker)
                item["memory_id"] = mem_id
                item["relevance"] = round(_clamp(relevance), 4)
                episodes.append(item)
        episodes.sort(key=lambda x: (x.get("relevance", 0.0), x.get("started_at", "")), reverse=True)
        return {"active_episode_count": len(episodes), "episodes": episodes[:8]}

    # ───────────────────────── inspection ─────────────────────────


    # ───────────────────────── V7.1 champ psychologique global ─────────────────────────

    def _update_v71_psychological_field(self, mem: CausalMemory) -> None:
        """Ajoute les couches V7.1 sans générer de dialogue ni dupliquer les autres moteurs."""
        self._update_dynamic_lived_meaning(mem)
        self._update_subconscious_bias_field(mem)
        self._update_irreversible_identity_marks(mem)
        self._update_relationship_phase_profile(mem)
        self._update_anticipated_affective_projection(mem)
        self._update_deep_causal_roots(mem)
        self._update_cumulative_social_saturation(mem)

    def _semantic_axis_map(self, mem: CausalMemory) -> Dict[str, float]:
        axes: Dict[str, float] = {}
        strength = max(mem.effect_strength, mem.recurrence_pressure, abs(mem.valence), mem.memory_priority, mem.causal_activation, 0.05)
        if mem.memory_kind in {"expressive_failure", "expressive_repair"} or mem.repair_kind != "none":
            axes["expression_consequence"] = strength
        if mem.relational_importance > 0.05 or mem.memory_kind == "relational_boundary":
            axes["relational_consequence"] = max(strength, mem.relational_importance)
        if mem.identity_impact > 0.05 or mem.memory_kind == "identity_continuity":
            axes["identity_consequence"] = max(strength, mem.identity_impact)
        if mem.valence < -0.05:
            axes["protective_meaning"] = max(strength, abs(mem.valence))
        if mem.valence > 0.05:
            axes["opening_meaning"] = max(strength, mem.valence)
        if mem.unresolved_tension > 0.08 or mem.inner_conflict_profile:
            axes["unresolved_inner_tension"] = max(strength, mem.unresolved_tension)
        if mem.attachment_trace > 0.08:
            axes["attachment_continuity"] = max(strength, mem.attachment_trace)
        if mem.relational_wound > 0.08:
            axes["relational_wound_memory"] = max(strength, mem.relational_wound)
        for key, value in mem.causal_layers.items():
            axes[f"layer_{key}"] = max(axes.get(f"layer_{key}", 0.0), abs(value) * 0.72)
        return self._normalize_vector(axes)

    def _update_dynamic_lived_meaning(self, mem: CausalMemory) -> None:
        axes = self._semantic_axis_map(mem)
        if not mem.original_lived_meaning:
            mem.original_lived_meaning = dict(axes)
        drift = dict(mem.current_lived_meaning or mem.original_lived_meaning or {})
        for key, value in axes.items():
            old = drift.get(key, 0.0)
            # Le sens vécu évolue doucement : il ne remplace pas l'origine, il la recompose.
            drift[key] = _clamp(old * 0.72 + value * 0.28, -1.0, 1.0)
        if mem.trust_variation < -0.08:
            drift["meaning_shift_toward_caution"] = max(drift.get("meaning_shift_toward_caution", 0.0), abs(mem.trust_variation) * 0.72)
        if mem.trust_variation > 0.08:
            drift["meaning_shift_toward_trust"] = max(drift.get("meaning_shift_toward_trust", 0.0), mem.trust_variation * 0.72)
        if mem.reinforcement_count >= 3:
            drift["repeated_lived_pattern"] = max(drift.get("repeated_lived_pattern", 0.0), min(1.0, mem.reinforcement_count / 10.0) * max(mem.memory_priority, 0.18))
        mem.current_lived_meaning = self._merge_layers(mem.current_lived_meaning, drift)

    def _update_subconscious_bias_field(self, mem: CausalMemory) -> None:
        field = dict(mem.subconscious_bias_field or {})
        ambient = _clamp(mem.memory_priority * 0.28 + mem.emotional_inertia * 0.24 + mem.autobiographical_weight * 0.18 + max(mem.relational_wound, mem.attachment_trace) * 0.18 + min(mem.reinforcement_count, 10) / 10.0 * 0.12)
        if ambient <= 0.035:
            return
        if mem.valence < -0.04:
            field["ambient_caution"] = max(field.get("ambient_caution", 0.0), ambient * max(abs(mem.valence), 0.45))
        elif mem.valence > 0.04:
            field["ambient_openness"] = max(field.get("ambient_openness", 0.0), ambient * max(mem.valence, 0.35))
        if mem.repair_kind != "none":
            field["preverbal_repair_bias"] = max(field.get("preverbal_repair_bias", 0.0), ambient * max(mem.recurrence_pressure, 0.42))
        if mem.relational_wound > 0.08:
            field["silent_relational_guard"] = max(field.get("silent_relational_guard", 0.0), ambient * mem.relational_wound)
        if mem.attachment_trace > 0.08:
            field["silent_attachment_pull"] = max(field.get("silent_attachment_pull", 0.0), ambient * mem.attachment_trace)
        if mem.identity_impact > 0.08:
            field["identity_background_tension"] = max(field.get("identity_background_tension", 0.0), ambient * mem.identity_impact)
        mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, field)

    def _update_irreversible_identity_marks(self, mem: CausalMemory) -> None:
        marks = dict(mem.irreversible_identity_marks or {})
        irreversible_pressure = max(mem.identity_impact, mem.autobiographical_weight, mem.relational_importance * 0.8, mem.relational_wound, mem.attachment_trace, mem.recurrence_pressure * 0.7)
        if irreversible_pressure < 0.42 and mem.reinforcement_count < 4:
            return
        if mem.memory_kind == "identity_continuity" or mem.identity_impact >= 0.35:
            marks["identity_continuity_mark"] = max(marks.get("identity_continuity_mark", 0.0), irreversible_pressure)
        if mem.relational_wound >= 0.28 or mem.trust_variation <= -0.22:
            marks["relational_caution_mark"] = max(marks.get("relational_caution_mark", 0.0), max(mem.relational_wound, abs(mem.trust_variation)))
        if mem.attachment_trace >= 0.28 or mem.trust_variation >= 0.22:
            marks["relational_trust_mark"] = max(marks.get("relational_trust_mark", 0.0), max(mem.attachment_trace, mem.trust_variation))
        if mem.repair_kind == "anti_meta" and mem.recurrence_pressure >= 0.3:
            marks["anti_meta_expression_mark"] = max(marks.get("anti_meta_expression_mark", 0.0), mem.recurrence_pressure)
        if mem.repair_kind in {"directness", "specificity"} and mem.recurrence_pressure >= 0.3:
            marks["concrete_response_mark"] = max(marks.get("concrete_response_mark", 0.0), mem.recurrence_pressure)
        mem.irreversible_identity_marks = self._merge_layers(mem.irreversible_identity_marks, marks)

    def _update_relationship_phase_profile(self, mem: CausalMemory) -> None:
        phase = dict(mem.relationship_phase_profile or {})
        base = max(mem.relational_importance, abs(mem.trust_variation), mem.relational_wound, mem.attachment_trace, mem.effect_strength * 0.5)
        if base < 0.06:
            return
        if mem.trust_variation > 0.12 or mem.attachment_trace > 0.18:
            phase["building_trust"] = max(phase.get("building_trust", 0.0), max(mem.trust_variation, mem.attachment_trace, base))
        if mem.trust_variation < -0.12 or mem.relational_wound > 0.18:
            phase["protective_distance"] = max(phase.get("protective_distance", 0.0), max(abs(mem.trust_variation), mem.relational_wound, base))
        if mem.repair_kind != "none" or mem.recurrence_pressure > 0.35:
            phase["repair_cycle"] = max(phase.get("repair_cycle", 0.0), max(mem.recurrence_pressure, base * 0.75))
        if mem.valence > 0.08 and mem.relational_importance > 0.12:
            phase["safe_continuity"] = max(phase.get("safe_continuity", 0.0), max(mem.valence, base))
        if mem.unresolved_tension > 0.18:
            phase["uncertain_contact"] = max(phase.get("uncertain_contact", 0.0), max(mem.unresolved_tension, base * 0.6))
        mem.relationship_phase_profile = self._merge_layers(mem.relationship_phase_profile, phase)

    def _update_anticipated_affective_projection(self, mem: CausalMemory) -> None:
        proj = dict(mem.anticipated_affective_projection or {})
        base = max(mem.effect_strength, mem.recurrence_pressure, mem.memory_priority, mem.causal_activation, abs(mem.valence), 0.05)
        if mem.valence < -0.04:
            proj["future_tension"] = max(proj.get("future_tension", 0.0), base * abs(mem.valence))
        if mem.valence > 0.04:
            proj["future_ease"] = max(proj.get("future_ease", 0.0), base * mem.valence)
        if mem.relational_wound > 0.08:
            proj["future_relational_sensitivity"] = max(proj.get("future_relational_sensitivity", 0.0), base * mem.relational_wound)
        if mem.attachment_trace > 0.08:
            proj["future_attachment_warmth"] = max(proj.get("future_attachment_warmth", 0.0), base * mem.attachment_trace)
        if mem.unresolved_tension > 0.08:
            proj["future_hesitation"] = max(proj.get("future_hesitation", 0.0), base * mem.unresolved_tension)
        if mem.repair_kind != "none":
            proj["future_repair_pressure"] = max(proj.get("future_repair_pressure", 0.0), base * max(mem.recurrence_pressure, 0.25))
        mem.anticipated_affective_projection = self._merge_layers(mem.anticipated_affective_projection, proj)

    def _update_deep_causal_roots(self, mem: CausalMemory) -> None:
        roots = dict(mem.deep_causal_roots or {})
        root_pressure = max(mem.memory_priority, mem.effect_strength, mem.recurrence_pressure, abs(mem.valence), mem.identity_impact, mem.relational_importance)
        tokens = self._tokens(mem.event + " " + mem.experienced_effect)[:10]
        for token in tokens:
            roots[f"token:{token}"] = max(roots.get(f"token:{token}", 0.0), root_pressure * 0.42)
        if mem.repair_kind != "none":
            roots[f"repair:{mem.repair_kind}"] = max(roots.get(f"repair:{mem.repair_kind}", 0.0), max(root_pressure, mem.recurrence_pressure))
        roots[f"kind:{mem.memory_kind}"] = max(roots.get(f"kind:{mem.memory_kind}", 0.0), root_pressure)
        if mem.valence < -0.05:
            roots["valence:protective"] = max(roots.get("valence:protective", 0.0), abs(mem.valence) * root_pressure)
        elif mem.valence > 0.05:
            roots["valence:opening"] = max(roots.get("valence:opening", 0.0), mem.valence * root_pressure)
        mem.deep_causal_roots = self._merge_layers(mem.deep_causal_roots, roots)

    def _update_cumulative_social_saturation(self, mem: CausalMemory) -> None:
        saturation = dict(mem.cumulative_social_saturation or {})
        repetition = _clamp(min(mem.reinforcement_count, 24) / 24.0)
        base = max(repetition, mem.recurrence_pressure * 0.7, mem.memory_priority * 0.4)
        if base < 0.04:
            return
        if mem.repair_kind == "anti_meta":
            saturation["anti_meta_saturation"] = max(saturation.get("anti_meta_saturation", 0.0), base)
        if mem.repair_kind in {"directness", "specificity"}:
            saturation["concrete_answer_saturation"] = max(saturation.get("concrete_answer_saturation", 0.0), base)
        if mem.memory_kind == "relational_boundary":
            saturation["boundary_saturation"] = max(saturation.get("boundary_saturation", 0.0), base)
        if mem.relational_wound > 0.08:
            saturation["wound_saturation"] = max(saturation.get("wound_saturation", 0.0), base * mem.relational_wound)
        if mem.attachment_trace > 0.08:
            saturation["trust_saturation"] = max(saturation.get("trust_saturation", 0.0), base * mem.attachment_trace)
        mem.cumulative_social_saturation = self._merge_layers(mem.cumulative_social_saturation, saturation)

    def get_subconscious_causal_pressure(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]
        field: Dict[str, float] = {}
        source_ids: List[str] = []
        for mem_id, mem, relevance in memories[:18]:
            factor = _clamp(max(relevance * 0.65, mem.memory_priority * 0.35, mem.emotional_inertia * 0.28, mem.autobiographical_weight * 0.24))
            if factor <= 0.02:
                continue
            source_ids.append(mem_id)
            field = self._weighted_merge_signal(field, mem.subconscious_bias_field, factor)
            field = self._weighted_merge_signal(field, mem.irreversible_identity_marks, factor * 0.85)
            field = self._weighted_merge_signal(field, mem.cumulative_social_saturation, factor * 0.75)
        return {
            "available": bool(field),
            "dominant_biases": self._top_signal_map(field, 10),
            "ambient_pressure": round(_clamp(max(field.values(), default=0.0)), 4),
            "source_memory_ids": source_ids[:10],
            "role": "silent_bias_field_not_dialogue",
        }

    def get_global_inner_weather(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]
        weather = {
            "openness": 0.0,
            "caution": 0.0,
            "relational_sensitivity": 0.0,
            "identity_pressure": 0.0,
            "repair_pressure": 0.0,
            "curiosity_pull": 0.0,
            "fatigue_or_overload": 0.0,
            "hesitation": 0.0,
            "recovery_need": 0.0,
            "continuity": 0.0,
        }
        for _, mem, relevance in memories[:20]:
            f = _clamp(max(relevance, mem.memory_priority * 0.5, mem.causal_activation * 0.45))
            weather["openness"] = max(weather["openness"], f * max(mem.attachment_trace, mem.valence if mem.valence > 0 else 0.0, mem.causal_desire_profile.get("seek_repair", 0.0) * 0.35))
            weather["caution"] = max(weather["caution"], f * max(mem.relational_wound, abs(mem.valence) if mem.valence < 0 else 0.0, mem.subconscious_bias_field.get("ambient_caution", 0.0)))
            weather["relational_sensitivity"] = max(weather["relational_sensitivity"], f * max(mem.relational_importance, mem.relational_wound, mem.attachment_trace))
            weather["identity_pressure"] = max(weather["identity_pressure"], f * max(mem.identity_impact, max(mem.identity_transformation_pressure.values(), default=0.0), max(mem.irreversible_identity_marks.values(), default=0.0)))
            weather["repair_pressure"] = max(weather["repair_pressure"], f * max(mem.recurrence_pressure if mem.repair_kind != "none" else 0.0, mem.future_bias.get("repair_before_expansion", 0.0)))
            weather["curiosity_pull"] = max(weather["curiosity_pull"], f * max(mem.causal_desire_profile.get("seek_repair", 0.0), mem.future_bias.get("allow_initiative", 0.0), mem.causal_desire_profile.get("seek_continuity", 0.0)))
            weather["fatigue_or_overload"] = max(weather["fatigue_or_overload"], f * max(mem.inhibition_level, mem.obsession_guard_state.get("cooldown_bias", 0.0), mem.unresolved_tension * 0.5, mem.subconscious_bias_field.get("background_fatigue", 0.0)))
            weather["hesitation"] = max(weather["hesitation"], f * max(mem.inner_conflict_profile.get("approach_vs_protection", 0.0), mem.inner_conflict_profile.get("desire_vs_recovery", 0.0), mem.anticipated_affective_projection.get("future_hesitation", 0.0)))
            weather["recovery_need"] = max(weather["recovery_need"], f * max(mem.internal_need_profile.get("recovery_need", 0.0), mem.affective_bridge.get("recovery_pressure", 0.0), mem.relationship_phase_profile.get("needs_recovery_phase", 0.0)))
            weather["continuity"] = max(weather["continuity"], f * max(mem.autobiographical_weight, mem.attachment_trace, mem.identity_impact * 0.65))
        dominant_state = max(weather.items(), key=lambda x: x[1])[0] if weather else "neutral"
        return {
            "dominant_state": dominant_state,
            "weather": {k: round(_clamp(v), 4) for k, v in weather.items()},
            "overall_intensity": round(_clamp(max(weather.values(), default=0.0)), 4),
            "role": "global_psychological_climate_not_dialogue",
        }


    def get_living_psychological_persistence(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Synthèse des tendances longues qui restent actives sans phrase préécrite."""
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]

        trait_drift: Dict[str, float] = {}
        fatigue: Dict[str, float] = {}
        relationship: Dict[str, float] = {}
        conflict: Dict[str, float] = {}
        identity_marks: Dict[str, float] = {}
        subconscious: Dict[str, float] = {}
        source_ids: List[str] = []

        for mem_id, mem, relevance in memories[:24]:
            factor = _clamp(max(relevance, mem.memory_priority * 0.42, mem.causal_activation * 0.36, mem.autobiographical_weight * 0.32))
            if factor <= 0.025:
                continue
            source_ids.append(mem_id)
            trait_drift = self._weighted_merge_signal(trait_drift, mem.identity_transformation_pressure, factor)
            relationship = self._weighted_merge_signal(relationship, mem.relationship_phase_profile, factor)
            conflict = self._weighted_merge_signal(conflict, mem.inner_conflict_profile, factor)
            identity_marks = self._weighted_merge_signal(identity_marks, mem.irreversible_identity_marks, factor)
            subconscious = self._weighted_merge_signal(subconscious, mem.subconscious_bias_field, factor * 0.8)
            fatigue = self._weighted_merge_signal(fatigue, {
                "background_fatigue": mem.subconscious_bias_field.get("background_fatigue", 0.0),
                "recovery_need": mem.internal_need_profile.get("recovery_need", 0.0),
                "emotional_fatigue": mem.affective_bridge.get("emotional_fatigue", 0.0),
                "cooldown_bias": mem.obsession_guard_state.get("cooldown_bias", 0.0),
            }, factor)

        dominant_trait = max(trait_drift.items(), key=lambda x: x[1])[0] if trait_drift else None
        dominant_conflict = max(conflict.items(), key=lambda x: x[1])[0] if conflict else None
        dominant_phase = max(relationship.items(), key=lambda x: x[1])[0] if relationship else None
        return {
            "available": bool(source_ids),
            "dominant_trait_drift": dominant_trait,
            "dominant_conflict": dominant_conflict,
            "dominant_relationship_phase": dominant_phase,
            "trait_drift": self._top_signal_map(trait_drift, 10),
            "fatigue": self._top_signal_map(fatigue, 8),
            "relationship_drift": self._top_signal_map(relationship, 10),
            "inner_conflict_persistence": self._top_signal_map(conflict, 10),
            "identity_marks": self._top_signal_map(identity_marks, 8),
            "subconscious_background": self._top_signal_map(subconscious, 10),
            "overall_persistence": round(_clamp(max(
                max(trait_drift.values(), default=0.0),
                max(fatigue.values(), default=0.0),
                max(relationship.values(), default=0.0),
                max(conflict.values(), default=0.0),
                max(identity_marks.values(), default=0.0),
                max(subconscious.values(), default=0.0),
            )), 4),
            "source_memory_ids": source_ids[:12],
            "role": "persistent_psychological_field_not_dialogue",
        }

    def project_future_affective_state(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context)
        projection: Dict[str, float] = {}
        for _, mem, relevance in memories[:12]:
            factor = _clamp(max(relevance, mem.memory_priority * 0.4, mem.causal_activation * 0.35))
            projection = self._weighted_merge_signal(projection, mem.anticipated_affective_projection, factor)
            if mem.future_bias.get("avoid_repetition", 0.0) > 0:
                projection["if_repeated_pattern_then_tension"] = max(projection.get("if_repeated_pattern_then_tension", 0.0), factor * mem.future_bias.get("avoid_repetition", 0.0))
            if mem.future_bias.get("seek_continuity", 0.0) > 0:
                projection["if_continued_pattern_then_ease"] = max(projection.get("if_continued_pattern_then_ease", 0.0), factor * mem.future_bias.get("seek_continuity", 0.0))
        return {
            "available": bool(projection),
            "anticipated_affects": self._top_signal_map(projection, 10),
            "dominant_affect": max(projection.items(), key=lambda x: x[1])[0] if projection else None,
            "role": "future_affective_simulation_not_dialogue",
        }

    def get_deep_causal_root_graph(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        roots: Dict[str, float] = {}
        edges: List[Dict[str, Any]] = []
        for mem_id, mem, relevance in memories[:18]:
            factor = _clamp(max(relevance, mem.memory_priority * 0.45))
            for key, value in mem.deep_causal_roots.items():
                roots[key] = max(roots.get(key, 0.0), _clamp(abs(value) * factor))
            top_roots = sorted(mem.deep_causal_roots.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
            for root, value in top_roots:
                edges.append({
                    "root": root,
                    "memory_id": mem_id,
                    "kind": mem.memory_kind,
                    "pressure": round(_clamp(abs(value) * factor), 4),
                })
        return {
            "available": bool(roots),
            "dominant_roots": self._top_signal_map(roots, 12),
            "root_edges": sorted(edges, key=lambda x: x["pressure"], reverse=True)[:12],
            "role": "causal_ancestry_structured_only",
        }

    def get_relationship_phase_state(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        phases: Dict[str, float] = {}
        for _, mem, relevance in memories[:16]:
            phases = self._weighted_merge_signal(phases, mem.relationship_phase_profile, _clamp(max(relevance, mem.relational_importance, mem.memory_priority * 0.4)))
        dominant = max(phases.items(), key=lambda x: x[1])[0] if phases else "unknown"
        return {
            "available": bool(phases),
            "dominant_phase": dominant,
            "phases": self._top_signal_map(phases, 8),
            "role": "relationship_evolution_signal_not_dialogue",
        }

    def get_memory_stats(self) -> Dict[str, Any]:
        if not self.memories:
            return {"total_memories": 0, "avg_confidence": 0.0, "strong_memories": 0, "total_reinforcements": 0}
        vals = list(self.memories.values())
        return {
            "total_memories": len(vals),
            "avg_confidence": round(sum(m.confidence for m in vals) / len(vals), 3),
            "strong_memories": sum(1 for m in vals if m.confidence >= 0.8),
            "total_reinforcements": sum(m.reinforcement_count for m in vals),
            "by_emotion": {emotion: sum(1 for m in vals if m.emotional_trace == emotion) for emotion in sorted(_ALLOWED_EMOTIONS)},
            "by_memory_kind": {kind: sum(1 for m in vals if m.memory_kind == kind) for kind in sorted(_ALLOWED_MEMORY_KINDS)},
            "avg_effect_strength": round(sum(m.effect_strength for m in vals) / len(vals), 3),
            "avg_recurrence_pressure": round(sum(m.recurrence_pressure for m in vals) / len(vals), 3),
            "avg_relational_importance": round(sum(m.relational_importance for m in vals) / len(vals), 3),
            "avg_identity_impact": round(sum(m.identity_impact for m in vals) / len(vals), 3),
            "avg_emotional_inertia": round(sum(m.emotional_inertia for m in vals) / len(vals), 3),
            "avg_affective_charge": round(sum(m.affective_charge for m in vals) / len(vals), 3),
            "avg_autobiographical_weight": round(sum(m.autobiographical_weight for m in vals) / len(vals), 3),
            "avg_causal_activation": round(sum(m.causal_activation for m in vals) / len(vals), 3),
            "relational_wound_memories": sum(1 for m in vals if m.relational_wound >= 0.18),
            "attachment_trace_memories": sum(1 for m in vals if m.attachment_trace >= 0.18),
            "inhibited_memories": sum(1 for m in vals if m.inhibition_level >= 0.25),
            "dormant_memories": sum(1 for m in vals if m.dormant),
            "contradiction_links": sum(len(m.contradiction_links) for m in vals),
            "episodic_markers": sum(len(m.episode_markers) for m in vals),
            "identity_evolution_arcs": sum(len(m.identity_evolution_arcs) for m in vals),
            "compressed_autobiographical_chapters": sum(len(m.compressed_autobiographical_chapters) for m in vals),
            "existential_failure_memories": sum(1 for m in vals if max(m.existential_failure_trace.values(), default=0.0) >= 0.18),
            "obsession_guarded_memories": sum(1 for m in vals if max(m.obsession_guard_state.values(), default=0.0) >= 0.25),
            "initiative_bridge_memories": sum(1 for m in vals if max(m.initiative_bridge.values(), default=0.0) >= 0.18),
            "temporal_maturation_memories": sum(1 for m in vals if max(m.temporal_maturation_state.values(), default=0.0) >= 0.18),
            "persistent_wound_memories": sum(1 for m in vals if max(m.persistent_wound_profile.values(), default=0.0) >= 0.18),
            "causal_desire_memories": sum(1 for m in vals if max(m.causal_desire_profile.values(), default=0.0) >= 0.18),
            "inner_conflict_memories": sum(1 for m in vals if max(m.inner_conflict_profile.values(), default=0.0) >= 0.18),
            "social_continuity_memories": sum(1 for m in vals if max(m.social_continuity_profile.values(), default=0.0) >= 0.18),
            "identity_transformation_memories": sum(1 for m in vals if max(m.identity_transformation_pressure.values(), default=0.0) >= 0.18),
            "lived_meaning_revisions": sum(len(m.lived_meaning_revision) for m in vals),
            "dynamic_meaning_memories": sum(1 for m in vals if max(m.current_lived_meaning.values(), default=0.0) >= 0.18),
            "subconscious_bias_memories": sum(1 for m in vals if max(m.subconscious_bias_field.values(), default=0.0) >= 0.18),
            "irreversible_identity_mark_memories": sum(1 for m in vals if max(m.irreversible_identity_marks.values(), default=0.0) >= 0.18),
            "relationship_phase_memories": sum(1 for m in vals if max(m.relationship_phase_profile.values(), default=0.0) >= 0.18),
            "future_affective_projection_memories": sum(1 for m in vals if max(m.anticipated_affective_projection.values(), default=0.0) >= 0.18),
            "deep_causal_root_memories": sum(1 for m in vals if max(m.deep_causal_roots.values(), default=0.0) >= 0.18),
            "cumulative_social_saturation_memories": sum(1 for m in vals if max(m.cumulative_social_saturation.values(), default=0.0) >= 0.18),
            "psychological_attractor_memories": sum(1 for m in vals if any("attractor" in k or k.startswith("desire::") for k in m.subconscious_bias_field)),
            "non_action_memories": sum(1 for m in vals if m.source_engine == "causal_memory_engine_non_action"),
            "background_fatigue_memories": sum(1 for m in vals if m.subconscious_bias_field.get("background_fatigue", 0.0) >= 0.12),
            "autobiographical_rewrite_memories": sum(1 for m in vals if any((r or {}).get("phase") == "global_autobiographical_rewrite" for r in m.lived_meaning_revision)),
            "emotional_contamination_memories": sum(1 for m in vals if m.subconscious_bias_field.get("contaminated_caution", 0.0) >= 0.05 or m.subconscious_bias_field.get("contaminated_opening", 0.0) >= 0.05),
        }


    # ───────────────────────── V7.3 dynamique organique longue ─────────────────────────

    def learn_from_non_action(
        self,
        context: str,
        expected_action: str = "",
        consequence: str = "",
        pressure: float = 0.0,
        relational_importance: float = 0.0,
        identity_impact: float = 0.0,
    ) -> Optional[str]:
        """Mémorise une non-action significative sans phrase préécrite.

        Sert quand Leia aurait dû clarifier, réparer, ralentir, demander ou agir,
        mais que l'absence d'action a produit une conséquence intérieure ou
        relationnelle. Le moteur garde seulement une relation cause→effet.
        """
        context = self.sanitize_text(context)
        expected_action = self.sanitize_text(expected_action or "needed action was absent")
        consequence = self.sanitize_text(consequence or "unresolved pressure remained active")
        pressure = _clamp(_safe_float(pressure, 0.0))
        if not context or pressure < self.non_action_memory_threshold:
            return None
        return self.learn_causal_relation(
            event=f"non_action_context: {context} | absent_action: {expected_action}",
            experienced_effect=consequence,
            emotional_trace="uncertain" if pressure < 0.62 else "negative",
            behavioral_shift="detect when absence of action increases unresolved pressure",
            attention_impact="watch meaningful omissions before expression",
            source_context={"origin": "non_action_memory", "expected_action": expected_action},
            initial_confidence=max(0.36, pressure),
            memory_kind="temporal_pattern",
            repair_kind="organic_flow",
            valence=-pressure,
            effect_strength=pressure,
            recurrence_pressure=max(pressure, 0.42),
            source_engine="causal_memory_engine_non_action",
            relational_importance=_clamp(max(relational_importance, pressure * 0.45)),
            identity_impact=_clamp(max(identity_impact, pressure * 0.32)),
            trust_variation=-pressure * 0.42,
            causal_layers={
                "omission": pressure,
                "unresolved_continuity": pressure * 0.8,
                "repair_latency": pressure * 0.62,
            },
            episode_context={"non_action": True, "consequence": consequence},
            autobiographical_weight=pressure * 0.42,
            relational_wound=pressure * 0.24,
            future_bias={"notice_omission": pressure, "repair_before_expansion": pressure * 0.72},
            identity_shift_vector={"responsiveness_memory": pressure * 0.66},
        )

    def _propagate_emotional_contamination(
        self,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Diffuse lentement affect/conflit entre souvenirs liés, sans dialogue."""
        memories = memories or [(mid, mem, max(mem.causal_activation, mem.memory_priority)) for mid, mem in self.memories.items()]
        changed_links = 0
        strongest_transfer = 0.0
        indexed = {mid: mem for mid, mem, _ in memories[:32]}
        if not indexed:
            return {"changed_links": 0, "strongest_transfer": 0.0, "role": "emotional_contamination_not_dialogue"}
        for source_id, source in list(indexed.items()):
            source_charge = max(source.affective_charge, source.emotional_inertia, abs(source.valence), source.relational_wound, source.attachment_trace)
            if source_charge < 0.08:
                continue
            targets = set(source.linked_memories)
            for cid in source.similarity_clusters:
                for other_id, other in self.memories.items():
                    if other_id != source_id and cid in other.similarity_clusters:
                        targets.add(other_id)
            for link in source.contradiction_links:
                if link.get("memory_id"):
                    targets.add(str(link.get("memory_id")))
            for target_id in list(targets)[:12]:
                target = self.memories.get(target_id)
                if not target or target_id == source_id:
                    continue
                semantic = max(self._text_similarity(source.event, target.event), self._text_similarity(source.experienced_effect, target.experienced_effect))
                relation = max(semantic, 0.18 if target_id in source.linked_memories else 0.0)
                contradiction = any(x.get("memory_id") == target_id for x in source.contradiction_links)
                if contradiction:
                    relation = max(relation, 0.26)
                transfer = _clamp(source_charge * relation * self.emotional_contamination_rate)
                if transfer < 0.006:
                    continue
                if source.valence < -0.02:
                    target.subconscious_bias_field = self._merge_layers(target.subconscious_bias_field, {
                        "contaminated_caution": max(target.subconscious_bias_field.get("contaminated_caution", 0.0), transfer * 2.8),
                    })
                    target.relational_wound = _clamp(target.relational_wound + transfer * 0.42)
                elif source.valence > 0.02:
                    target.subconscious_bias_field = self._merge_layers(target.subconscious_bias_field, {
                        "contaminated_opening": max(target.subconscious_bias_field.get("contaminated_opening", 0.0), transfer * 2.2),
                    })
                    target.attachment_trace = _clamp(target.attachment_trace + transfer * 0.38)
                if contradiction:
                    target.inner_conflict_profile = self._merge_layers(target.inner_conflict_profile, {
                        "cross_memory_contradiction_contamination": transfer * 2.5,
                    })
                    target.unresolved_tension = _clamp(target.unresolved_tension + transfer * 0.55)
                target.affective_charge = _clamp(target.affective_charge + transfer)
                target.causal_activation = _clamp(max(target.causal_activation, source.causal_activation * relation * 0.35))
                changed_links += 1
                strongest_transfer = max(strongest_transfer, transfer)
        return {
            "changed_links": changed_links,
            "strongest_transfer": round(_clamp(strongest_transfer), 4),
            "role": "emotional_contamination_not_dialogue",
        }

    def _stabilize_psychological_attractors(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Transforme des répétitions causales en attracteurs psychologiques stables."""
        memories = memories or [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]
        candidates: Dict[str, float] = {}
        source_ids: List[str] = []
        for mem_id, mem, relevance in memories[:32]:
            factor = _clamp(max(relevance, mem.memory_priority, mem.causal_activation, mem.recurrence_pressure * 0.7))
            if factor < 0.055:
                continue
            source_ids.append(mem_id)
            if mem.repair_kind == "anti_meta":
                candidates["anti_meta_presence_attractor"] = max(candidates.get("anti_meta_presence_attractor", 0.0), factor)
            if mem.repair_kind in {"directness", "specificity"}:
                candidates["concrete_directness_attractor"] = max(candidates.get("concrete_directness_attractor", 0.0), factor)
            if mem.relational_wound > 0.12:
                candidates["relational_protection_attractor"] = max(candidates.get("relational_protection_attractor", 0.0), factor * mem.relational_wound)
            if mem.attachment_trace > 0.12:
                candidates["relational_continuity_attractor"] = max(candidates.get("relational_continuity_attractor", 0.0), factor * mem.attachment_trace)
            if mem.autobiographical_weight > 0.12 or mem.identity_impact > 0.12:
                candidates["identity_continuity_attractor"] = max(candidates.get("identity_continuity_attractor", 0.0), factor * max(mem.autobiographical_weight, mem.identity_impact))
            for key, value in mem.causal_desire_profile.items():
                if value > 0.08:
                    candidates[f"desire::{key}"] = max(candidates.get(f"desire::{key}", 0.0), factor * value)
        if not candidates:
            return {"available": False, "attractors": {}, "source_memory_ids": [], "role": "psychological_attractor_field_not_dialogue"}
        for mem_id in source_ids[:24]:
            mem = self.memories.get(mem_id)
            if not mem:
                continue
            local_updates = {}
            for key, value in candidates.items():
                if value >= 0.09:
                    old = mem.subconscious_bias_field.get(key, 0.0)
                    local_updates[key] = old * (1.0 - self.attractor_stability_rate) + value * self.attractor_stability_rate
            if local_updates:
                mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, local_updates)
                mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, {
                    "attractor_guided_initiative": max(local_updates.values()) * 0.72,
                })
                mem.expression_bridge = self._merge_layers(mem.expression_bridge, {
                    "attractor_guided_expression": max(local_updates.values()) * 0.62,
                })
        return {
            "available": True,
            "attractors": self._top_signal_map(candidates, 10),
            "dominant_attractor": max(candidates.items(), key=lambda x: x[1])[0],
            "source_memory_ids": source_ids[:12],
            "role": "psychological_attractor_field_not_dialogue",
        }

    def _consolidate_global_autobiographical_meaning(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Réécrit lentement le sens autobiographique global à partir des traces fortes."""
        memories = memories or [(mid, mem, max(mem.memory_priority, mem.autobiographical_weight, mem.causal_activation)) for mid, mem in self.memories.items()]
        axes: Dict[str, float] = {}
        source_ids: List[str] = []
        for mem_id, mem, relevance in memories[:32]:
            weight = _clamp(max(relevance, mem.autobiographical_weight, mem.identity_impact, mem.relational_importance * 0.65))
            if weight < 0.07:
                continue
            source_ids.append(mem_id)
            if mem.valence < -0.05:
                axes["learned_from_negative_consequence"] = max(axes.get("learned_from_negative_consequence", 0.0), weight * abs(mem.valence))
            if mem.valence > 0.05:
                axes["learned_from_positive_continuity"] = max(axes.get("learned_from_positive_continuity", 0.0), weight * mem.valence)
            if mem.memory_kind == "identity_continuity":
                axes["identity_continuity_history"] = max(axes.get("identity_continuity_history", 0.0), weight)
            if mem.memory_kind == "relational_boundary":
                axes["relational_boundary_history"] = max(axes.get("relational_boundary_history", 0.0), weight)
            if mem.repair_kind != "none":
                axes["repair_learning_history"] = max(axes.get("repair_learning_history", 0.0), weight * max(mem.recurrence_pressure, 0.35))
            for key, value in mem.current_lived_meaning.items():
                axes[f"meaning::{key}"] = max(axes.get(f"meaning::{key}", 0.0), weight * value)
        if not axes:
            return {"available": False, "rewritten_axes": {}, "source_memory_ids": [], "role": "global_autobiographical_rewrite_not_dialogue"}
        dominant_axis = max(axes.items(), key=lambda x: x[1])[0]
        for mem_id in source_ids[:24]:
            mem = self.memories.get(mem_id)
            if not mem:
                continue
            current = dict(mem.current_lived_meaning or {})
            original = dict(mem.original_lived_meaning or {})
            if not original:
                mem.original_lived_meaning = dict(current or axes)
            for key, value in axes.items():
                short_key = key[:90]
                old = current.get(short_key, 0.0)
                current[short_key] = _clamp(old * (1.0 - self.autobiographical_rewrite_rate) + value * self.autobiographical_rewrite_rate)
            mem.current_lived_meaning = self._merge_layers(mem.current_lived_meaning, current)
            mem.identity_transformation_pressure = self._merge_layers(mem.identity_transformation_pressure, {
                "autobiographical_rewrite_pressure": max(axes.values()) * 0.54,
            })
            revision = {
                "at": _now(),
                "phase": "global_autobiographical_rewrite",
                "dominant_axis": self.sanitize_text(dominant_axis),
                "intensity": round(_clamp(max(axes.values())), 4),
                "source_count": len(source_ids),
            }
            mem.lived_meaning_revision.append(revision)
            mem.lived_meaning_revision = mem.lived_meaning_revision[-16:]
        return {
            "available": True,
            "dominant_axis": dominant_axis,
            "rewritten_axes": self._top_signal_map(axes, 10),
            "source_memory_ids": source_ids[:12],
            "role": "global_autobiographical_rewrite_not_dialogue",
        }

    def get_psychological_attractor_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        field: Dict[str, float] = {}
        source_ids: List[str] = []
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]
        for mem_id, mem, relevance in memories[:32]:
            factor = _clamp(max(relevance, mem.memory_priority * 0.48, mem.causal_activation * 0.42))
            if factor < 0.035:
                continue
            source_ids.append(mem_id)
            for key, value in mem.subconscious_bias_field.items():
                if "attractor" in key or key.startswith("desire::"):
                    field[key] = max(field.get(key, 0.0), value * factor)
            for key, value in mem.causal_desire_profile.items():
                field[f"desire::{key}"] = max(field.get(f"desire::{key}", 0.0), value * factor)
        return {
            "available": bool(field),
            "dominant_attractor": max(field.items(), key=lambda x: x[1])[0] if field else None,
            "attractors": self._top_signal_map(field, 12),
            "source_memory_ids": source_ids[:12],
            "role": "stable_psychological_attractors_not_dialogue",
        }

    def get_global_autobiographical_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        field: Dict[str, float] = {}
        revisions = 0
        source_ids: List[str] = []
        if not memories:
            memories = [(mid, mem, max(mem.autobiographical_weight, mem.identity_impact, mem.memory_priority, 0.04)) for mid, mem in self.memories.items()]
        for mem_id, mem, relevance in memories[:32]:
            factor = _clamp(max(relevance, mem.autobiographical_weight, mem.identity_impact, mem.memory_priority * 0.45))
            if factor < 0.035:
                continue
            source_ids.append(mem_id)
            revisions += len(mem.lived_meaning_revision)
            field = self._weighted_merge_signal(field, mem.current_lived_meaning, factor)
            field = self._weighted_merge_signal(field, mem.irreversible_identity_marks, factor * 0.75)
            field = self._weighted_merge_signal(field, mem.identity_transformation_pressure, factor * 0.65)
        return {
            "available": bool(field),
            "dominant_autobiographical_axis": max(field.items(), key=lambda x: x[1])[0] if field else None,
            "field": self._top_signal_map(field, 12),
            "revision_count": revisions,
            "source_memory_ids": source_ids[:12],
            "role": "global_autobiographical_field_not_dialogue",
        }

    def run_living_memory_cycle(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """Cycle public d'entretien mémoire : propagation + consolidation + export."""
        propagation = self.propagate_living_state(context, save=False)
        memories = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        attractors = self.get_psychological_attractor_field(context, memories)
        autobiographical = self.get_global_autobiographical_field(context, memories)
        persistence = self.get_living_psychological_persistence(context, memories)
        if save:
            self.save_memories()
        return {
            "propagation": propagation,
            "psychological_attractors": attractors,
            "global_autobiographical_field": autobiographical,
            "psychological_persistence": persistence,
            "memory_state": self.get_memory_stats(),
            "role": "living_memory_cycle_not_dialogue",
        }

    # ───────────────────────── V7.4 corrections profondes ─────────────────────────

    def _living_result_changed(self, result: Any) -> bool:
        """Détecte si une dynamique lente a modifié l'état interne."""
        if not isinstance(result, dict):
            return False
        if result.get("changed_links", 0):
            return True
        if result.get("strongest_transfer", 0.0):
            return _safe_float(result.get("strongest_transfer"), 0.0) > 0.0
        if result.get("applied_updates", 0):
            return True
        if result.get("rewritten_memories", 0):
            return True
        if result.get("hierarchy_updates", 0):
            return True
        if result.get("priority_updates", 0):
            return True
        if result.get("changed_memories", 0):
            return True
        return False

    def _build_deep_psychological_hierarchy(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Construit une hiérarchie lente blessures/désirs/conflits.

        Cette hiérarchie ne produit pas de texte. Elle organise seulement les
        pressions internes pour que les autres moteurs sachent ce qui domine.
        """
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.04)) for mid, mem in self.memories.items()]

        wounds: Dict[str, float] = {}
        desires: Dict[str, float] = {}
        conflicts: Dict[str, float] = {}
        social: Dict[str, float] = {}
        source_ids: List[str] = []

        for mem_id, mem, relevance in memories[:40]:
            factor = _clamp(max(relevance, mem.memory_priority, mem.causal_activation, mem.autobiographical_weight * 0.72))
            if factor < 0.04:
                continue
            source_ids.append(mem_id)
            if mem.relational_wound > 0.08:
                wounds["relational_wound"] = max(wounds.get("relational_wound", 0.0), factor * mem.relational_wound)
            if mem.unresolved_tension > 0.08:
                wounds["unresolved_tension"] = max(wounds.get("unresolved_tension", 0.0), factor * mem.unresolved_tension)
            if mem.existential_failure_trace:
                for key, value in mem.existential_failure_trace.items():
                    wounds[f"existential::{key}"] = max(wounds.get(f"existential::{key}", 0.0), factor * value)
            if mem.causal_desire_profile:
                for key, value in mem.causal_desire_profile.items():
                    desires[key] = max(desires.get(key, 0.0), factor * value)
            if mem.future_bias.get("repair_before_expansion", 0.0) > 0.08:
                desires["repair_before_expansion"] = max(desires.get("repair_before_expansion", 0.0), factor * mem.future_bias.get("repair_before_expansion", 0.0))
            if mem.future_bias.get("seek_continuity", 0.0) > 0.08:
                desires["seek_continuity"] = max(desires.get("seek_continuity", 0.0), factor * mem.future_bias.get("seek_continuity", 0.0))
            for key, value in mem.inner_conflict_profile.items():
                conflicts[key] = max(conflicts.get(key, 0.0), factor * value)
            for key, value in mem.social_continuity_profile.items():
                social[key] = max(social.get(key, 0.0), factor * value)

        dominant_wound = max(wounds.items(), key=lambda x: x[1])[0] if wounds else None
        dominant_desire = max(desires.items(), key=lambda x: x[1])[0] if desires else None
        dominant_conflict = max(conflicts.items(), key=lambda x: x[1])[0] if conflicts else None
        hierarchy_pressure = _clamp(max(
            max(wounds.values(), default=0.0),
            max(desires.values(), default=0.0),
            max(conflicts.values(), default=0.0),
            max(social.values(), default=0.0),
        ))

        updates = 0
        for mem_id in source_ids[:28]:
            mem = self.memories.get(mem_id)
            if not mem:
                continue
            local: Dict[str, float] = {}
            if dominant_wound:
                local[f"dominant_wound::{dominant_wound}"] = hierarchy_pressure * 0.58
            if dominant_desire:
                local[f"dominant_desire::{dominant_desire}"] = hierarchy_pressure * 0.52
            if dominant_conflict:
                local[f"dominant_conflict::{dominant_conflict}"] = hierarchy_pressure * 0.55
            if local:
                mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, local)
                mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, {
                    "hierarchy_guided_priority": hierarchy_pressure * 0.58,
                    "repair_or_continuity_priority": max(desires.get("repair_before_expansion", 0.0), desires.get("seek_continuity", 0.0)) * 0.66,
                })
                mem.affective_bridge = self._merge_layers(mem.affective_bridge, {
                    "hierarchical_affective_pressure": max(wounds.values(), default=0.0) * 0.64,
                })
                mem.expression_bridge = self._merge_layers(mem.expression_bridge, {
                    "hierarchy_guided_expression_constraint": max(conflicts.values(), default=0.0) * 0.58,
                })
                updates += 1

        return {
            "available": bool(source_ids),
            "dominant_wound": dominant_wound,
            "dominant_desire": dominant_desire,
            "dominant_conflict": dominant_conflict,
            "hierarchy_pressure": round(hierarchy_pressure, 4),
            "wounds": self._top_signal_map(wounds, 8),
            "desires": self._top_signal_map(desires, 8),
            "conflicts": self._top_signal_map(conflicts, 8),
            "social_continuity": self._top_signal_map(social, 8),
            "source_memory_ids": source_ids[:12],
            "hierarchy_updates": updates,
            "role": "deep_psychological_hierarchy_not_dialogue",
        }

    def _reorganize_autobiographical_priorities(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Réordonne lentement les priorités autobiographiques selon l'usage vivant."""
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.autobiographical_weight, mem.causal_activation, 0.04)) for mid, mem in self.memories.items()]

        updates = 0
        dominant_axes: Dict[str, float] = {}
        for mem_id, mem, relevance in memories[:40]:
            living_weight = _clamp(
                relevance * 0.28
                + mem.autobiographical_weight * 0.24
                + mem.identity_impact * 0.18
                + mem.causal_activation * 0.14
                + mem.emotional_inertia * 0.10
                + max(mem.irreversible_identity_marks.values(), default=0.0) * 0.06
            )
            if living_weight < 0.035:
                continue
            old_priority = mem.memory_priority
            mem.memory_priority = _clamp(mem.memory_priority * 0.86 + living_weight * 0.14)
            if abs(mem.memory_priority - old_priority) > 0.004:
                updates += 1
            for key, value in mem.current_lived_meaning.items():
                dominant_axes[key] = max(dominant_axes.get(key, 0.0), value * mem.memory_priority)
            if mem.identity_impact > 0.08:
                dominant_axes["identity_continuity"] = max(dominant_axes.get("identity_continuity", 0.0), mem.identity_impact * mem.memory_priority)
            if mem.relational_importance > 0.08:
                dominant_axes["relational_continuity"] = max(dominant_axes.get("relational_continuity", 0.0), mem.relational_importance * mem.memory_priority)

        return {
            "priority_updates": updates,
            "dominant_autobiographical_priorities": self._top_signal_map(dominant_axes, 10),
            "role": "autobiographical_priority_reorganization_not_dialogue",
        }


    def _orchestrate_global_causal_ecology(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """V7.4.1 : fait coopérer les couches profondes sans générer de dialogue.

        Le but n'est pas d'ajouter un nouveau bloc isolé, mais d'arbitrer les
        blessures, désirs, conflits, fatigue, non-action et continuité sociale
        en une écologie lente que les autres moteurs peuvent lire.
        """
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [
                (mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.04))
                for mid, mem in self.memories.items()
            ]

        if not memories:
            return {
                "available": False,
                "changed_memories": 0,
                "dominant_axis": None,
                "ecological_tension": 0.0,
                "fatigue_pressure": 0.0,
                "repair_readiness": 0.0,
                "role": "global_causal_ecology_not_dialogue",
            }

        wounds: Dict[str, float] = {}
        desires: Dict[str, float] = {}
        conflicts: Dict[str, float] = {}
        identity: Dict[str, float] = {}
        social: Dict[str, float] = {}
        changed = 0

        for mem_id, mem, relevance in memories[:48]:
            factor = _clamp(max(relevance, mem.memory_priority, mem.causal_activation, mem.autobiographical_weight * 0.72, 0.035))
            wound_base = max(mem.relational_wound, mem.unresolved_tension, max(mem.persistent_wound_profile.values(), default=0.0))
            desire_base = max(max(mem.causal_desire_profile.values(), default=0.0), mem.future_bias.get("seek_continuity", 0.0), mem.future_bias.get("repair_before_expansion", 0.0))
            conflict_base = max(max(mem.inner_conflict_profile.values(), default=0.0), len(mem.contradiction_links) * 0.05)
            identity_base = max(mem.identity_impact, max(mem.identity_transformation_pressure.values(), default=0.0), max(mem.irreversible_identity_marks.values(), default=0.0))
            social_base = max(mem.relational_importance, max(mem.social_continuity_profile.values(), default=0.0), max(mem.cumulative_social_saturation.values(), default=0.0))

            if wound_base > 0.035:
                wounds["protective_wound_pressure"] = max(wounds.get("protective_wound_pressure", 0.0), wound_base * factor)
            if desire_base > 0.035:
                desires["continuity_desire_pressure"] = max(desires.get("continuity_desire_pressure", 0.0), desire_base * factor)
            if conflict_base > 0.035:
                conflicts["unresolved_conflict_pressure"] = max(conflicts.get("unresolved_conflict_pressure", 0.0), conflict_base * factor)
            if identity_base > 0.035:
                identity["identity_continuity_pressure"] = max(identity.get("identity_continuity_pressure", 0.0), identity_base * factor)
            if social_base > 0.035:
                social["relationship_continuity_pressure"] = max(social.get("relationship_continuity_pressure", 0.0), social_base * factor)

        ecological_tension = _clamp(max(
            max(wounds.values(), default=0.0) * 0.95,
            max(conflicts.values(), default=0.0) * 0.90,
            max(identity.values(), default=0.0) * 0.82,
            max(social.values(), default=0.0) * 0.72,
        ))
        desire_pressure = _clamp(max(desires.values(), default=0.0))
        fatigue_pressure = _clamp(ecological_tension * 0.52 + max(0.0, ecological_tension - desire_pressure) * 0.28)
        repair_readiness = _clamp(desire_pressure * 0.55 + max(social.values(), default=0.0) * 0.25 + max(identity.values(), default=0.0) * 0.20)

        dominant_axis = max(
            {
                "wound": max(wounds.values(), default=0.0),
                "desire": desire_pressure,
                "conflict": max(conflicts.values(), default=0.0),
                "identity": max(identity.values(), default=0.0),
                "social": max(social.values(), default=0.0),
            }.items(),
            key=lambda item: item[1],
        )[0]

        for mem_id, mem, relevance in memories[:36]:
            factor = _clamp(max(relevance, mem.memory_priority, mem.causal_activation, 0.035))
            before = (
                dict(mem.subconscious_bias_field),
                dict(mem.initiative_bridge),
                dict(mem.affective_bridge),
                dict(mem.expression_bridge),
                dict(mem.obsession_guard_state),
            )

            ecological_signal = _clamp(ecological_tension * factor)
            if ecological_signal >= 0.025:
                mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, {
                    "global_ecological_tension": ecological_signal,
                    f"dominant_ecology::{dominant_axis}": ecological_signal * 0.82,
                })
                mem.obsession_guard_state = self._merge_layers(mem.obsession_guard_state, {
                    "organic_cooldown_need": fatigue_pressure * factor,
                    "non_action_permission": max(fatigue_pressure - repair_readiness * 0.35, 0.0) * factor,
                })
                mem.internal_need_profile = self._merge_layers(mem.internal_need_profile, {
                    "integrate_before_expand": ecological_signal * 0.62,
                    "recover_after_inner_pressure": fatigue_pressure * factor,
                })
                mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, {
                    "act_only_if_relation_or_repair_benefits": repair_readiness * factor,
                    "avoid_impulse_when_ecology_overloaded": fatigue_pressure * factor,
                })
                mem.affective_bridge = self._merge_layers(mem.affective_bridge, {
                    "hold_emotional_continuity": max(ecological_signal, repair_readiness * factor),
                    "avoid_affective_overreaction": fatigue_pressure * factor,
                })
                mem.expression_bridge = self._merge_layers(mem.expression_bridge, {
                    "prefer_simple_concrete_expression": ecological_signal * 0.58,
                    "avoid_explaining_internal_ecology": ecological_signal * 0.72,
                    "preserve_lived_continuity": repair_readiness * factor,
                })
                mem.causal_activation = _clamp(mem.causal_activation * 0.96 + ecological_signal * 0.04)
                mem.memory_priority = _clamp(mem.memory_priority * 0.97 + max(ecological_signal, repair_readiness * factor) * 0.03)

            after = (
                dict(mem.subconscious_bias_field),
                dict(mem.initiative_bridge),
                dict(mem.affective_bridge),
                dict(mem.expression_bridge),
                dict(mem.obsession_guard_state),
            )
            if after != before:
                changed += 1

        return {
            "available": True,
            "changed_memories": changed,
            "dominant_axis": dominant_axis,
            "ecological_tension": round(ecological_tension, 4),
            "desire_pressure": round(desire_pressure, 4),
            "fatigue_pressure": round(fatigue_pressure, 4),
            "repair_readiness": round(repair_readiness, 4),
            "wounds": self._top_signal_map(wounds, 8),
            "desires": self._top_signal_map(desires, 8),
            "conflicts": self._top_signal_map(conflicts, 8),
            "identity": self._top_signal_map(identity, 8),
            "social": self._top_signal_map(social, 8),
            "role": "global_causal_ecology_not_dialogue",
        }

    def propagate_living_state(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """V7.4 : propagation vivante complète, persistante, non dialoguante."""
        relevant = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        active_ids = {mid for mid, _, score in relevant if score >= 0.12}
        now_changed = False

        for mem_id, mem in self.memories.items():
            context_boost = max((score for mid, _, score in relevant if mid == mem_id), default=0.0)
            organic_base = max(
                mem.memory_priority,
                mem.effect_strength,
                mem.recurrence_pressure,
                mem.reactivation_score,
                max(mem.subconscious_bias_field.values(), default=0.0) * 0.72,
                max(mem.irreversible_identity_marks.values(), default=0.0) * 0.64,
            )
            target_activation = _clamp(max(context_boost, organic_base * 0.44) - mem.inhibition_level * 0.33)
            old_activation = mem.causal_activation
            mem.causal_activation = _clamp(mem.causal_activation * 0.60 + target_activation * 0.40)
            mem.affective_charge = _clamp(mem.affective_charge * (1.0 - self.emotional_cooling_rate) + abs(mem.valence) * mem.causal_activation * 0.18)
            mem.emotional_inertia = _clamp(mem.emotional_inertia * 0.963 + max(mem.affective_charge, mem.relational_wound, mem.attachment_trace) * 0.037)
            if mem.relational_wound > 0:
                mem.relational_wound = _clamp(mem.relational_wound * 0.992 + max(0.0, -mem.trust_variation) * 0.008)
            if mem.attachment_trace > 0:
                mem.attachment_trace = _clamp(mem.attachment_trace * 0.994 + max(0.0, mem.trust_variation) * 0.006)
            mem.unresolved_tension = _clamp(max(mem.unresolved_tension * 0.985, mem.relational_wound * 0.82, len(mem.contradiction_links) * 0.035))
            self._apply_silent_psychological_drift(mem, context_boost=context_boost)
            if abs(mem.causal_activation - old_activation) > 0.015 or mem_id in active_ids:
                mem.living_state_history.append(self._living_state_step("living_propagation_v7_4", mem.causal_activation, mem.valence, mem.relational_wound))
                now_changed = True

        for mem_id, mem in list(self.memories.items()):
            if mem.causal_activation < self.cascade_min_activation:
                continue
            targets = set(mem.linked_memories)
            for cid in mem.similarity_clusters:
                for other_id, other in self.memories.items():
                    if other_id != mem_id and cid in other.similarity_clusters:
                        targets.add(other_id)
            for link in mem.contradiction_links:
                other_id = link.get("memory_id")
                if other_id:
                    targets.add(str(other_id))
            for target_id in list(targets)[:18]:
                target = self.memories.get(target_id)
                if not target:
                    continue
                similarity = max(self._text_similarity(mem.event, target.event), self._text_similarity(mem.experienced_effect, target.experienced_effect))
                contradiction_boost = 0.18 if any(x.get("memory_id") == target_id for x in mem.contradiction_links) else 0.0
                relation_pressure = max(similarity, contradiction_boost, 0.12)
                transfer = mem.causal_activation * self.cascade_decay * relation_pressure
                if transfer >= self.cascade_min_activation:
                    target.causal_activation = _clamp(max(target.causal_activation, transfer - target.inhibition_level * 0.25))
                    target.unresolved_tension = _clamp(max(target.unresolved_tension, contradiction_boost * transfer))
                    target.subconscious_bias_field = self._merge_layers(target.subconscious_bias_field, {
                        "causal_echo_pressure": transfer * 0.54,
                    })
                    now_changed = True

        contamination = self._propagate_emotional_contamination(relevant)
        attractors = self._stabilize_psychological_attractors(context, relevant)
        hierarchy = self._build_deep_psychological_hierarchy(context, relevant)
        autobiographical_rewrite = self._consolidate_global_autobiographical_meaning(context, relevant)
        priority_reorganization = self._reorganize_autobiographical_priorities(context, relevant)
        global_causal_ecology = self._orchestrate_global_causal_ecology(context, relevant)
        overload = self._apply_adaptive_inhibition()
        psychological_persistence = self.get_living_psychological_persistence(context, relevant)

        changed_by_slow_dynamics = any(self._living_result_changed(x) for x in (contamination, attractors, hierarchy, autobiographical_rewrite, priority_reorganization, global_causal_ecology))
        if save and (now_changed or changed_by_slow_dynamics):
            self.save_memories()
        return {
            "active_memories": sum(1 for m in self.memories.values() if m.causal_activation >= 0.12),
            "overload": overload,
            "psychological_persistence": psychological_persistence,
            "emotional_contamination": contamination,
            "psychological_attractors": attractors,
            "deep_psychological_hierarchy": hierarchy,
            "autobiographical_rewrite": autobiographical_rewrite,
            "priority_reorganization": priority_reorganization,
            "global_causal_ecology": global_causal_ecology,
            "dominant_memory_ids": [mid for mid, mem in sorted(self.memories.items(), key=lambda x: x[1].causal_activation, reverse=True)[:8] if mem.causal_activation >= 0.08],
            "changed": bool(now_changed or changed_by_slow_dynamics),
            "role": "living_causal_propagation_v7_4_not_dialogue",
        }

    def run_living_memory_cycle(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """V7.4 : cycle public d'entretien mémoire complet, sans dialogue."""
        propagation = self.propagate_living_state(context, save=False)
        memories = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.04)) for mid, mem in self.memories.items()]
        attractors = self.get_psychological_attractor_field(context, memories)
        autobiographical = self.get_global_autobiographical_field(context, memories)
        persistence = self.get_living_psychological_persistence(context, memories)
        hierarchy = self._build_deep_psychological_hierarchy(context, memories)
        priority_reorganization = self._reorganize_autobiographical_priorities(context, memories)
        global_causal_ecology = self._orchestrate_global_causal_ecology(context, memories)
        bridge_state = self.export_cross_engine_bridges(context, memories)
        if save:
            self.save_memories()
        return {
            "propagation": propagation,
            "psychological_attractors": attractors,
            "global_autobiographical_field": autobiographical,
            "psychological_persistence": persistence,
            "deep_psychological_hierarchy": hierarchy,
            "priority_reorganization": priority_reorganization,
            "global_causal_ecology": global_causal_ecology,
            "cross_engine_bridges": bridge_state,
            "memory_state": self.get_memory_stats(),
            "role": "living_memory_cycle_v7_4_not_dialogue",
        }

    def get_memory_stats(self) -> Dict[str, Any]:
        if not self.memories:
            return {
                "total_memories": 0,
                "avg_confidence": 0.0,
                "strong_memories": 0,
                "total_reinforcements": 0,
                "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
            }
        vals = list(self.memories.values())
        base = {
            "total_memories": len(vals),
            "avg_confidence": round(sum(m.confidence for m in vals) / len(vals), 3),
            "strong_memories": sum(1 for m in vals if m.confidence >= 0.8),
            "total_reinforcements": sum(m.reinforcement_count for m in vals),
            "by_emotion": {emotion: sum(1 for m in vals if m.emotional_trace == emotion) for emotion in sorted(_ALLOWED_EMOTIONS)},
            "by_memory_kind": {kind: sum(1 for m in vals if m.memory_kind == kind) for kind in sorted(_ALLOWED_MEMORY_KINDS)},
            "avg_effect_strength": round(sum(m.effect_strength for m in vals) / len(vals), 3),
            "avg_recurrence_pressure": round(sum(m.recurrence_pressure for m in vals) / len(vals), 3),
            "avg_relational_importance": round(sum(m.relational_importance for m in vals) / len(vals), 3),
            "avg_identity_impact": round(sum(m.identity_impact for m in vals) / len(vals), 3),
            "avg_emotional_inertia": round(sum(m.emotional_inertia for m in vals) / len(vals), 3),
            "avg_affective_charge": round(sum(m.affective_charge for m in vals) / len(vals), 3),
            "avg_autobiographical_weight": round(sum(m.autobiographical_weight for m in vals) / len(vals), 3),
            "avg_causal_activation": round(sum(m.causal_activation for m in vals) / len(vals), 3),
            "relational_wound_memories": sum(1 for m in vals if m.relational_wound >= 0.18),
            "attachment_trace_memories": sum(1 for m in vals if m.attachment_trace >= 0.18),
            "inhibited_memories": sum(1 for m in vals if m.inhibition_level >= 0.25),
            "dormant_memories": sum(1 for m in vals if m.dormant),
            "contradiction_links": sum(len(m.contradiction_links) for m in vals),
            "episodic_markers": sum(len(m.episode_markers) for m in vals),
            "long_term_arcs": sum(len(m.identity_evolution_arcs) for m in vals),
            "autobiographical_chapters": sum(len(m.compressed_autobiographical_chapters) for m in vals),
            "dynamic_meaning_revisions": sum(len(m.lived_meaning_revision) for m in vals),
            "dynamic_meaning_memories": sum(1 for m in vals if max(m.current_lived_meaning.values(), default=0.0) >= 0.18),
            "subconscious_bias_memories": sum(1 for m in vals if max(m.subconscious_bias_field.values(), default=0.0) >= 0.18),
            "irreversible_identity_mark_memories": sum(1 for m in vals if max(m.irreversible_identity_marks.values(), default=0.0) >= 0.18),
            "relationship_phase_memories": sum(1 for m in vals if max(m.relationship_phase_profile.values(), default=0.0) >= 0.18),
            "future_affective_projection_memories": sum(1 for m in vals if max(m.anticipated_affective_projection.values(), default=0.0) >= 0.18),
            "deep_causal_root_memories": sum(1 for m in vals if max(m.deep_causal_roots.values(), default=0.0) >= 0.18),
            "cumulative_social_saturation_memories": sum(1 for m in vals if max(m.cumulative_social_saturation.values(), default=0.0) >= 0.18),
            "psychological_attractor_memories": sum(1 for m in vals if any("attractor" in k or k.startswith("desire::") for k in m.subconscious_bias_field)),
            "non_action_memories": sum(1 for m in vals if m.source_engine == "causal_memory_engine_non_action"),
            "background_fatigue_memories": sum(1 for m in vals if m.subconscious_bias_field.get("background_fatigue", 0.0) >= 0.12),
            "autobiographical_rewrite_memories": sum(1 for m in vals if any((r or {}).get("phase") == "global_autobiographical_rewrite" for r in m.lived_meaning_revision)),
            "emotional_contamination_memories": sum(1 for m in vals if m.subconscious_bias_field.get("contaminated_caution", 0.0) >= 0.05 or m.subconscious_bias_field.get("contaminated_opening", 0.0) >= 0.05),
            "deep_hierarchy_memories": sum(1 for m in vals if any(k.startswith("dominant_wound::") or k.startswith("dominant_desire::") or k.startswith("dominant_conflict::") for k in m.subconscious_bias_field)),
            "causal_echo_memories": sum(1 for m in vals if m.subconscious_bias_field.get("causal_echo_pressure", 0.0) >= 0.05),
            "global_ecology_memories": sum(1 for m in vals if m.subconscious_bias_field.get("global_ecological_tension", 0.0) >= 0.05),
            "organic_cooldown_memories": sum(1 for m in vals if m.obsession_guard_state.get("organic_cooldown_need", 0.0) >= 0.05),
            "expression_ecology_constraint_memories": sum(1 for m in vals if m.expression_bridge.get("avoid_explaining_internal_ecology", 0.0) >= 0.05),
            "avg_priority": round(sum(m.memory_priority for m in vals) / len(vals), 3),
            "max_subconscious_pressure": round(max((max(m.subconscious_bias_field.values(), default=0.0) for m in vals), default=0.0), 3),
            "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
        }
        return base




    # ───────────────────────── V7.4.2 finalisation vivante ─────────────────────────

    def _v742_memory_factor(self, mem: CausalMemory, relevance: float = 0.0) -> float:
        return _clamp(max(
            relevance,
            mem.memory_priority,
            mem.causal_activation,
            mem.autobiographical_weight * 0.92,
            mem.emotional_inertia * 0.76,
            max(mem.subconscious_bias_field.values(), default=0.0) * 0.72,
            max(mem.irreversible_identity_marks.values(), default=0.0) * 0.70,
        ))

    def _v742_micro_signature(self, user_message: str, leia_response: str, outcome: Dict[str, Any]) -> Dict[str, float]:
        """Produit une signature courte de micro-réaction vécue, sans phrase publique."""
        text = f"{user_message or ''} {leia_response or ''}".strip()
        length = len(self._tokens(text))
        strength = max(
            _clamp(_safe_float(outcome.get("effect_strength"), 0.0)),
            _clamp(_safe_float(outcome.get("presence_weakened"), 0.0)),
            _clamp(_safe_float(outcome.get("positive_contact"), 0.0)),
            _clamp(_safe_float(outcome.get("distance_created"), 0.0)),
            0.18 if length <= 4 else 0.0,
        )
        if strength <= 0.0:
            return {}
        return {
            "micro_reaction_intensity": strength,
            "micro_context_brevity": 1.0 if length <= 4 else _clamp(8.0 / max(8.0, float(length))),
            "micro_relational_sensitivity": max(_clamp(_safe_float(outcome.get("relational_importance"), 0.0)), strength * 0.55),
            "micro_presence_need": max(_clamp(_safe_float(outcome.get("presence_weakened"), 0.0)), strength * 0.45),
        }

    def learn_micro_reaction_from_exchange(self, user_message: str, leia_response: str, outcome: Dict[str, Any]) -> Optional[str]:
        """Mémorise les micro-réactions utiles sans générer de dialogue ni templates."""
        outcome = outcome or {}
        sig = self._v742_micro_signature(user_message, leia_response, outcome)
        if not sig or sig.get("micro_reaction_intensity", 0.0) < 0.16:
            return None
        valence = _safe_float(outcome.get("valence"), 0.0)
        if valence == 0.0:
            valence = _safe_float(outcome.get("positive_contact"), 0.0) - max(_safe_float(outcome.get("distance_created"), 0.0), _safe_float(outcome.get("presence_weakened"), 0.0))
        return self.learn_causal_relation(
            event=f"micro_exchange_context: {user_message}",
            experienced_effect=str(outcome.get("effect") or outcome.get("experienced_effect") or "micro reaction changed lived presence"),
            emotional_trace=outcome.get("emotional_trace", "neutral"),
            behavioral_shift="keep micro-reaction proportional to the immediate exchange",
            attention_impact="track tiny relational changes before large interpretation",
            source_context={"origin": "v7_4_2_micro_reaction", "micro_signature": sig},
            initial_confidence=max(0.36, sig["micro_reaction_intensity"]),
            memory_kind="episodic_trace",
            repair_kind=outcome.get("repair_kind", "organic_flow"),
            valence=_clamp(valence, -1.0, 1.0),
            effect_strength=sig["micro_reaction_intensity"],
            recurrence_pressure=max(0.18, sig["micro_relational_sensitivity"]),
            source_engine="causal_memory_engine_v7_4_2_micro_reaction",
            relational_importance=sig["micro_relational_sensitivity"],
            identity_impact=_clamp(sig["micro_presence_need"] * 0.38),
            causal_layers={"micro_reaction": sig["micro_reaction_intensity"], "situated_presence": sig["micro_presence_need"]},
            episode_context={"v7_4_2_micro_reaction": sig},
            autobiographical_weight=_clamp(sig["micro_relational_sensitivity"] * 0.42),
            future_bias={"micro_proportionality": sig["micro_reaction_intensity"], "avoid_overinterpretation": sig["micro_context_brevity"]},
        )

    def _v742_update_multiscale_causal_chains(self, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
        changed = 0
        scales = {"immediate": {}, "episodic": {}, "autobiographical": {}, "identity": {}}
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.03)) for mid, mem in self.memories.items()]
        for mem_id, mem, relevance in memories[:36]:
            factor = self._v742_memory_factor(mem, relevance)
            if factor < 0.035:
                continue
            immediate = max(mem.causal_activation, relevance, mem.reactivation_score)
            episodic = max(mem.effect_strength, mem.recurrence_pressure, len(mem.episode_markers) * 0.035)
            autobiographical = max(mem.autobiographical_weight, mem.relational_importance, max(mem.current_lived_meaning.values(), default=0.0))
            identity = max(mem.identity_impact, max(mem.irreversible_identity_marks.values(), default=0.0), max(mem.identity_transformation_pressure.values(), default=0.0))
            chain = {
                "multi_scale_immediate": _clamp(immediate * factor),
                "multi_scale_episodic": _clamp(episodic * factor),
                "multi_scale_autobiographical": _clamp(autobiographical * factor),
                "multi_scale_identity": _clamp(identity * factor),
            }
            before = dict(mem.deep_causal_roots)
            mem.deep_causal_roots = self._merge_layers(mem.deep_causal_roots, chain)
            mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, {"multi_scale_causal_pressure": max(chain.values())})
            if mem.deep_causal_roots != before:
                changed += 1
            for key, val in chain.items():
                bucket = key.replace("multi_scale_", "")
                scales[bucket][mem_id] = val
        return {
            "available": bool(scales["immediate"]),
            "changed_memories": changed,
            "dominant_scale": max(((k, max(v.values(), default=0.0)) for k, v in scales.items()), key=lambda x: x[1])[0] if any(scales.values()) else None,
            "scales": {k: round(max(v.values(), default=0.0), 4) for k, v in scales.items()},
            "role": "multi_scale_causal_chains_not_dialogue",
        }

    def get_multiscale_causal_field(self, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        field = self._v742_update_multiscale_causal_chains(context, memories)
        source_ids = [mid for mid, _, _ in (memories or [])[:12]]
        field["source_memory_ids"] = source_ids
        return field

    def get_dynamic_identity_conflict_field(self, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        conflicts: Dict[str, float] = {}
        identity: Dict[str, float] = {}
        resolution_pressure = 0.0
        changed = 0
        for _, mem, relevance in memories[:32]:
            factor = self._v742_memory_factor(mem, relevance)
            conflicts = self._weighted_merge_signal(conflicts, mem.inner_conflict_profile, factor)
            identity = self._weighted_merge_signal(identity, mem.identity_transformation_pressure, factor)
            identity = self._weighted_merge_signal(identity, mem.irreversible_identity_marks, factor * 0.75)
            conflict_load = max(mem.inner_conflict_profile.values(), default=0.0)
            identity_load = max(mem.identity_transformation_pressure.values(), default=0.0)
            contradiction_load = min(1.0, len(mem.contradiction_links) * 0.08)
            dynamic = _clamp(max(conflict_load, contradiction_load) * 0.56 + identity_load * 0.44)
            if dynamic >= 0.045:
                before = dict(mem.subconscious_bias_field)
                mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, {"dynamic_identity_conflict": dynamic * factor})
                mem.inhibition_level = _clamp(mem.inhibition_level * 0.985 + dynamic * 0.015)
                resolution_pressure = max(resolution_pressure, dynamic * factor)
                if before != mem.subconscious_bias_field:
                    changed += 1
        return {
            "available": bool(conflicts or identity),
            "changed_memories": changed,
            "dominant_conflict": max(conflicts.items(), key=lambda x: x[1])[0] if conflicts else None,
            "dominant_identity_pressure": max(identity.items(), key=lambda x: x[1])[0] if identity else None,
            "resolution_pressure": round(_clamp(resolution_pressure), 4),
            "conflicts": self._top_signal_map(conflicts, 10),
            "identity_pressures": self._top_signal_map(identity, 10),
            "role": "dynamic_identity_conflict_not_dialogue",
        }

    def get_embodied_contextual_memory_field(self, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        field: Dict[str, float] = {}
        for _, mem, relevance in memories[:24]:
            factor = self._v742_memory_factor(mem, relevance)
            field["felt_caution"] = max(field.get("felt_caution", 0.0), max(0.0, -mem.valence, mem.relational_wound) * factor)
            field["felt_opening"] = max(field.get("felt_opening", 0.0), max(0.0, mem.valence, mem.attachment_trace) * factor)
            field["felt_tension"] = max(field.get("felt_tension", 0.0), max(mem.unresolved_tension, mem.emotional_inertia) * factor)
            field["felt_continuity"] = max(field.get("felt_continuity", 0.0), max(mem.autobiographical_weight, mem.identity_impact) * factor)
            field["felt_repair_need"] = max(field.get("felt_repair_need", 0.0), mem.recurrence_pressure * factor)
        return {
            "available": bool(field),
            "dominant_felt_axis": max(field.items(), key=lambda x: x[1])[0] if field else None,
            "field": {k: round(_clamp(v), 4) for k, v in field.items()},
            "role": "embodied_contextual_memory_not_dialogue",
        }

    def _v742_apply_behavioral_inertia_and_existential_fatigue(self, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
        changed = 0
        inertia_peak = 0.0
        fatigue_peak = 0.0
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.03)) for mid, mem in self.memories.items()]
        for _, mem, relevance in memories[:48]:
            factor = self._v742_memory_factor(mem, relevance)
            inertia = _clamp((mem.emotional_inertia * 0.38) + (mem.recurrence_pressure * 0.22) + (mem.autobiographical_weight * 0.20) + (max(mem.subconscious_bias_field.values(), default=0.0) * 0.20))
            fatigue = _clamp(
                mem.subconscious_bias_field.get("background_fatigue", 0.0) * 0.42
                + mem.unresolved_tension * 0.22
                + mem.inhibition_level * 0.18
                + max(mem.existential_failure_trace.values(), default=0.0) * 0.18
            )
            if inertia < 0.035 and fatigue < 0.035:
                continue
            before = (dict(mem.obsession_guard_state), dict(mem.initiative_bridge), dict(mem.affective_bridge), dict(mem.expression_bridge))
            mem.obsession_guard_state = self._merge_layers(mem.obsession_guard_state, {
                "behavioral_inertia": inertia * factor,
                "existential_fatigue": fatigue * factor,
            })
            mem.initiative_bridge = self._merge_layers(mem.initiative_bridge, {
                "continue_existing_thread_before_switching": inertia * factor,
                "avoid_forced_initiative_when_fatigued": fatigue * factor,
            })
            mem.affective_bridge = self._merge_layers(mem.affective_bridge, {
                "carry_previous_affect": inertia * factor,
                "lower_intensity_under_fatigue": fatigue * factor,
            })
            mem.expression_bridge = self._merge_layers(mem.expression_bridge, {
                "preserve_previous_tone_continuity": inertia * factor,
                "allow_shorter_expression_under_fatigue": fatigue * factor,
            })
            mem.inhibition_level = _clamp(mem.inhibition_level * 0.982 + fatigue * 0.018)
            inertia_peak = max(inertia_peak, inertia * factor)
            fatigue_peak = max(fatigue_peak, fatigue * factor)
            after = (mem.obsession_guard_state, mem.initiative_bridge, mem.affective_bridge, mem.expression_bridge)
            if after != before:
                changed += 1
        return {
            "changed_memories": changed,
            "behavioral_inertia": round(_clamp(inertia_peak), 4),
            "existential_fatigue": round(_clamp(fatigue_peak), 4),
            "role": "behavioral_inertia_and_existential_fatigue_not_dialogue",
        }

    def _v742_propagate_social_contamination(self, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
        changed = 0
        social_field: Dict[str, float] = {}
        if not memories:
            memories = [(mid, mem, max(mem.social_continuity_profile.values(), default=0.0),) for mid, mem in self.memories.items()]
        for _, mem, relevance in memories[:32]:
            factor = self._v742_memory_factor(mem, relevance)
            social_field = self._weighted_merge_signal(social_field, mem.social_continuity_profile, factor)
            social_field = self._weighted_merge_signal(social_field, mem.cumulative_social_saturation, factor * 0.75)
        if not social_field:
            return {"changed_memories": 0, "field": {}, "role": "social_contamination_not_dialogue"}
        dominant_value = max(social_field.values(), default=0.0)
        for _, mem, relevance in memories[:32]:
            factor = self._v742_memory_factor(mem, relevance)
            transfer = _clamp(dominant_value * factor * self.social_continuity_weight)
            if transfer < 0.025:
                continue
            before = dict(mem.subconscious_bias_field)
            mem.subconscious_bias_field = self._merge_layers(mem.subconscious_bias_field, {"social_contamination_pressure": transfer})
            mem.relationship_phase_profile = self._merge_layers(mem.relationship_phase_profile, {"social_phase_carryover": transfer * 0.8})
            if before != mem.subconscious_bias_field:
                changed += 1
        return {
            "changed_memories": changed,
            "dominant_social_axis": max(social_field.items(), key=lambda x: x[1])[0],
            "field": self._top_signal_map(social_field, 10),
            "role": "social_contamination_not_dialogue",
        }

    def _v742_generate_preinteraction_prospective_bias(self, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
        bias: Dict[str, float] = {}
        source_ids: List[str] = []
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, 0.03)) for mid, mem in self.memories.items()]
        for mem_id, mem, relevance in memories[:24]:
            factor = self._v742_memory_factor(mem, relevance)
            bias = self._weighted_merge_signal(bias, mem.future_bias, factor)
            bias = self._weighted_merge_signal(bias, mem.anticipated_affective_projection, factor * 0.82)
            if mem.relational_wound > 0.12:
                bias["anticipate_possible_distance"] = max(bias.get("anticipate_possible_distance", 0.0), mem.relational_wound * factor)
            if mem.attachment_trace > 0.12:
                bias["anticipate_possible_opening"] = max(bias.get("anticipate_possible_opening", 0.0), mem.attachment_trace * factor)
            if factor >= 0.08:
                source_ids.append(mem_id)
        return {
            "available": bool(bias),
            "dominant_prospective_bias": max(bias.items(), key=lambda x: x[1])[0] if bias else None,
            "bias": self._top_signal_map(bias, 12),
            "source_memory_ids": source_ids[:12],
            "role": "preinteraction_prospective_bias_not_dialogue",
        }


    # ───────────────────────── V7.4.3 corrections organiques profondes ─────────────────────────

    def _v743_memory_set(self, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> List[Tuple[str, CausalMemory, float]]:
        """Sélection robuste : contexte s'il existe, sinon champ interne autonome."""
        if memories is not None:
            return memories
        selected = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        if selected:
            return selected
        return [
            (mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, mem.emotional_inertia, 0.03))
            for mid, mem in self.memories.items()
        ]

    def _v743_autonomous_implicit_drift(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Fait vivre la mémoire sans input direct.

        Cette dynamique ne fabrique aucune phrase. Elle transforme seulement les
        pressions invisibles : intuition, prudence, ouverture, fatigue, conflit,
        besoin de récupération et disponibilité relationnelle.
        """
        memories = self._v743_memory_set(context, memories)
        if not memories:
            return {"changed_memories": 0, "implicit_field": {}, "role": "autonomous_implicit_drift_not_dialogue"}

        changed = 0
        implicit_field: Dict[str, float] = {}
        now = datetime.now()
        for mem_id, mem, relevance in memories[:36]:
            try:
                last = datetime.fromisoformat(mem.last_reinforced)
            except Exception:
                last = now
            days = max(0.0, (now - last).total_seconds() / 86400.0)
            age_factor = _clamp(0.18 + math.log1p(days) * 0.09)
            base = max(
                self.implicit_memory_floor,
                mem.memory_priority * 0.42,
                mem.causal_activation * 0.36,
                mem.emotional_inertia * 0.34,
                mem.autobiographical_weight * 0.30,
                relevance * 0.28,
            )
            drift = _clamp(self.autonomous_drift_rate * (0.45 + age_factor + base))
            if drift <= 0.0:
                continue

            old_priority = mem.memory_priority
            old_activation = mem.causal_activation

            valence_abs = abs(mem.valence)
            wound = max(mem.relational_wound, max(mem.persistent_wound_profile.values(), default=0.0))
            desire = max(mem.attachment_trace, max(mem.causal_desire_profile.values(), default=0.0))
            conflict = max(mem.unresolved_tension, max(mem.inner_conflict_profile.values(), default=0.0))
            fatigue = max(mem.obsession_guard_state.get("existential_fatigue", 0.0), mem.subconscious_bias_field.get("background_fatigue", 0.0))

            mem.subconscious_bias_field["invisible_memory_trace"] = _clamp(
                mem.subconscious_bias_field.get("invisible_memory_trace", 0.0) * self.invisible_trace_decay
                + max(base, valence_abs, wound, desire, conflict) * drift
            )
            if wound > 0.04 or mem.valence < -0.04:
                mem.subconscious_bias_field["implicit_protective_bias"] = _clamp(
                    mem.subconscious_bias_field.get("implicit_protective_bias", 0.0) * 0.982 + max(wound, -mem.valence, conflict) * drift
                )
            if desire > 0.04 or mem.valence > 0.04:
                mem.subconscious_bias_field["implicit_opening_bias"] = _clamp(
                    mem.subconscious_bias_field.get("implicit_opening_bias", 0.0) * 0.984 + max(desire, mem.valence, mem.attachment_trace) * drift
                )
            if conflict > 0.05:
                mem.inner_conflict_profile["slow_unresolved_conflict"] = _clamp(
                    mem.inner_conflict_profile.get("slow_unresolved_conflict", 0.0) * 0.988 + conflict * drift
                )
            if fatigue > 0.05:
                mem.internal_need_profile["organic_recovery_need"] = _clamp(
                    mem.internal_need_profile.get("organic_recovery_need", 0.0) * 0.985 + fatigue * drift
                )

            mem.temporal_maturation_state["lived_time_continuity"] = _clamp(
                mem.temporal_maturation_state.get("lived_time_continuity", 0.0) * 0.987
                + max(age_factor, mem.autobiographical_weight, mem.emotional_inertia) * self.temporal_lived_continuity_rate
            )
            mem.current_lived_meaning["present_reinterprets_memory"] = _clamp(
                mem.current_lived_meaning.get("present_reinterprets_memory", 0.0) * 0.99
                + max(mem.causal_activation, relevance, mem.memory_priority) * drift * 0.72
            )
            mem.memory_priority = _clamp(
                mem.memory_priority * (1.0 - self.organic_restructure_rate)
                + max(base, mem.autobiographical_weight, mem.emotional_inertia, mem.causal_activation) * self.organic_restructure_rate
            )
            mem.causal_activation = _clamp(mem.causal_activation * 0.972 + max(base, relevance) * drift)
            mem.affective_charge = _clamp(mem.affective_charge * 0.986 + valence_abs * drift)

            implicit_field = self._weighted_merge_signal(implicit_field, mem.subconscious_bias_field, max(base, relevance) * 0.65)
            if abs(mem.memory_priority - old_priority) > 0.004 or abs(mem.causal_activation - old_activation) > 0.004:
                mem.living_state_history.append(self._living_state_step("autonomous_implicit_drift_v7_4_3", mem.causal_activation, mem.valence, mem.relational_wound))
                changed += 1

        return {
            "changed_memories": changed,
            "implicit_field": self._top_signal_map(implicit_field, 14),
            "dominant_implicit_axis": max(implicit_field.items(), key=lambda x: x[1])[0] if implicit_field else None,
            "role": "autonomous_implicit_drift_v7_4_3_not_dialogue",
        }

    def absorb_cross_engine_feedback(self, feedback: Optional[Dict[str, Any]], context: str = "", save: bool = True) -> Dict[str, Any]:
        """Absorbe le retour des moteurs attention/émotion/initiative/expression.

        API publique prévue pour les autres modules : ils peuvent envoyer des
        signaux numériques ou symboliques. La mémoire causale se reconfigure sans
        copier leur rôle et sans produire de texte.
        """
        if not isinstance(feedback, dict) or not feedback:
            return {"accepted": False, "updated_memories": 0, "role": "cross_engine_feedback_absorption_not_dialogue"}
        memories = self._v743_memory_set(context)
        if not memories:
            return {"accepted": True, "updated_memories": 0, "role": "cross_engine_feedback_absorption_not_dialogue"}

        cleaned = self._sanitize_context(feedback)
        numeric: Dict[str, float] = {}
        textual: List[str] = []
        def collect(prefix: str, obj: Any) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    key = self.sanitize_text(f"{prefix}_{k}" if prefix else k)
                    if isinstance(v, (int, float, bool)):
                        numeric[key] = _clamp(_safe_float(v, 0.0), -1.0, 1.0)
                    elif isinstance(v, str):
                        sv = self.sanitize_text(v)
                        if sv:
                            textual.append(sv)
                    elif isinstance(v, dict):
                        collect(key, v)
            elif isinstance(obj, str):
                sv = self.sanitize_text(obj)
                if sv:
                    textual.append(sv)
        collect("", cleaned)
        textual_context = " ".join(textual[:12])

        updated = 0
        for mem_id, mem, relevance in memories[:24]:
            semantic = max(self._text_similarity(textual_context, mem.event), self._text_similarity(textual_context, mem.experienced_effect)) if textual_context else 0.0
            factor = _clamp(max(relevance, semantic, mem.memory_priority * 0.6, self.implicit_memory_floor) * self.cross_engine_feedback_weight)
            if factor <= 0.0:
                continue
            old = (mem.memory_priority, mem.causal_activation, mem.unresolved_tension)
            for key, value in numeric.items():
                if not key:
                    continue
                magnitude = abs(value) * factor
                if any(term in key for term in ("emotion", "affect", "warmth", "valence")):
                    mem.contextual_emotional_resonance[key] = _clamp(mem.contextual_emotional_resonance.get(key, 0.0) * 0.88 + value * factor, -1.0, 1.0)
                    mem.affective_bridge[key] = _clamp(mem.affective_bridge.get(key, 0.0) * 0.90 + value * factor, -1.0, 1.0)
                elif any(term in key for term in ("initiative", "desire", "impulse", "curiosity")):
                    mem.causal_desire_profile[key] = _clamp(mem.causal_desire_profile.get(key, 0.0) * 0.90 + magnitude)
                    mem.initiative_bridge[key] = _clamp(mem.initiative_bridge.get(key, 0.0) * 0.90 + magnitude)
                elif any(term in key for term in ("attention", "focus", "salience")):
                    mem.internal_need_profile[key] = _clamp(mem.internal_need_profile.get(key, 0.0) * 0.90 + magnitude)
                elif any(term in key for term in ("expression", "mouth", "voice", "response")):
                    mem.expression_bridge[key] = _clamp(mem.expression_bridge.get(key, 0.0) * 0.90 + value * factor, -1.0, 1.0)
                elif any(term in key for term in ("identity", "self", "continuity")):
                    mem.identity_transformation_pressure[key] = _clamp(mem.identity_transformation_pressure.get(key, 0.0) * 0.90 + magnitude)
                    mem.irreversible_identity_marks[key] = _clamp(mem.irreversible_identity_marks.get(key, 0.0) * 0.94 + magnitude * 0.38)
                elif any(term in key for term in ("fatigue", "overload", "cooldown")):
                    mem.obsession_guard_state[key] = _clamp(mem.obsession_guard_state.get(key, 0.0) * 0.90 + magnitude)
                else:
                    mem.subconscious_bias_field[key] = _clamp(mem.subconscious_bias_field.get(key, 0.0) * 0.92 + value * factor, -1.0, 1.0)
            mem.source_context["last_cross_engine_feedback"] = {"at": _now(), "keys": list(numeric.keys())[:24]}
            mem.causal_activation = _clamp(mem.causal_activation * 0.92 + factor)
            mem.memory_priority = self._calculate_memory_priority(mem)
            if any(abs(a-b) > 0.005 for a, b in zip(old, (mem.memory_priority, mem.causal_activation, mem.unresolved_tension))):
                mem.living_state_history.append(self._living_state_step("cross_engine_feedback_absorbed_v7_4_3", mem.causal_activation, mem.valence, mem.relational_wound))
                updated += 1
        if save and updated:
            self.save_memories()
        return {
            "accepted": True,
            "updated_memories": updated,
            "absorbed_numeric_keys": list(numeric.keys())[:24],
            "absorbed_textual_signals": textual[:8],
            "role": "cross_engine_feedback_absorption_v7_4_3_not_dialogue",
        }

    def _v743_restructure_organic_priorities(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Réorganise lentement les priorités au lieu d'empiler les souvenirs."""
        memories = self._v743_memory_set(context, memories)
        if not memories:
            return {"restructured_memories": 0, "role": "organic_priority_restructuring_not_dialogue"}
        changed = 0
        dominant_axes: Dict[str, float] = {}
        for mem_id, mem, relevance in memories[:40]:
            wound = max(mem.relational_wound, max(mem.persistent_wound_profile.values(), default=0.0))
            desire = max(mem.attachment_trace, max(mem.causal_desire_profile.values(), default=0.0))
            conflict = max(mem.unresolved_tension, max(mem.inner_conflict_profile.values(), default=0.0))
            identity = max(mem.identity_impact, max(mem.identity_transformation_pressure.values(), default=0.0))
            fatigue = max(mem.obsession_guard_state.get("existential_fatigue", 0.0), mem.subconscious_bias_field.get("background_fatigue", 0.0))
            organic = _clamp((wound * 0.22) + (desire * 0.18) + (conflict * 0.20) + (identity * 0.19) + (mem.autobiographical_weight * 0.13) + (relevance * 0.08))
            if fatigue > 0.45 and desire < 0.25:
                mem.inhibition_level = _clamp(mem.inhibition_level * 0.93 + fatigue * self.organic_restructure_rate)
                mem.obsession_guard_state["non_action_allowed_by_fatigue"] = _clamp(mem.obsession_guard_state.get("non_action_allowed_by_fatigue", 0.0) * 0.94 + fatigue * 0.04)
            else:
                mem.inhibition_level = _clamp(mem.inhibition_level * 0.985)
            old = mem.memory_priority
            mem.memory_priority = _clamp(mem.memory_priority * (1.0 - self.organic_restructure_rate) + organic * self.organic_restructure_rate)
            if organic >= 0.22:
                mem.dormant = False
            elif mem.confidence < self.dormancy_confidence_floor and mem.causal_activation < 0.08:
                mem.dormant = True
            for axis, value in {
                "wound": wound, "desire": desire, "conflict": conflict, "identity": identity, "fatigue": fatigue
            }.items():
                dominant_axes[axis] = max(dominant_axes.get(axis, 0.0), value * max(relevance, mem.memory_priority, 0.05))
            if abs(mem.memory_priority - old) > 0.004:
                changed += 1
        return {
            "restructured_memories": changed,
            "dominant_organic_axis": max(dominant_axes.items(), key=lambda x: x[1])[0] if dominant_axes else None,
            "axes": self._top_signal_map(dominant_axes, 8),
            "role": "organic_priority_restructuring_v7_4_3_not_dialogue",
        }

    def get_invisible_memory_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Exporte les biais implicites dont l'origine n'a pas besoin d'être consciente."""
        memories = self._v743_memory_set(context, memories)
        field: Dict[str, float] = {}
        ids: List[str] = []
        for mem_id, mem, relevance in memories[:32]:
            factor = _clamp(max(relevance, mem.memory_priority, mem.causal_activation, self.implicit_memory_floor))
            invisible = {
                k: v for k, v in mem.subconscious_bias_field.items()
                if any(term in k for term in ("implicit", "invisible", "background", "preconscious", "bias", "trace"))
            }
            field = self._weighted_merge_signal(field, invisible, factor)
            if invisible:
                ids.append(mem_id)
        return {
            "available": bool(field),
            "dominant_invisible_axis": max(field.items(), key=lambda x: x[1])[0] if field else None,
            "field": self._top_signal_map(field, 14),
            "source_memory_ids": ids[:12],
            "role": "invisible_memory_field_v7_4_3_not_dialogue",
        }

    def get_temporal_lived_continuity_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Transforme le temps en continuité vécue exploitable par les autres moteurs."""
        memories = self._v743_memory_set(context, memories)
        field: Dict[str, float] = {}
        ids: List[str] = []
        for mem_id, mem, relevance in memories[:32]:
            factor = _clamp(max(relevance, mem.autobiographical_weight, mem.memory_priority, 0.04))
            temporal = dict(mem.temporal_maturation_state or {})
            if mem.living_state_history:
                temporal["recent_lived_continuity"] = max(temporal.get("recent_lived_continuity", 0.0), min(1.0, len(mem.living_state_history) / 24.0) * factor)
            if mem.lived_meaning_revision:
                temporal["past_reinterpreted_by_present"] = max(temporal.get("past_reinterpreted_by_present", 0.0), min(1.0, len(mem.lived_meaning_revision) / 16.0) * factor)
            field = self._weighted_merge_signal(field, temporal, factor)
            if temporal:
                ids.append(mem_id)
        return {
            "available": bool(field),
            "dominant_temporal_axis": max(field.items(), key=lambda x: x[1])[0] if field else None,
            "field": self._top_signal_map(field, 14),
            "source_memory_ids": ids[:12],
            "role": "temporal_lived_continuity_v7_4_3_not_dialogue",
        }

    def _v742_run_deep_completion_dynamics(self, context: str, memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.03)) for mid, mem in self.memories.items()]
        multi_scale = self._v742_update_multiscale_causal_chains(context, memories)
        identity_conflict = self.get_dynamic_identity_conflict_field(context, memories)
        embodied = self.get_embodied_contextual_memory_field(context, memories)
        inertia = self._v742_apply_behavioral_inertia_and_existential_fatigue(context, memories)
        social = self._v742_propagate_social_contamination(context, memories)
        prospective = self._v742_generate_preinteraction_prospective_bias(context, memories)
        autonomous_drift = self._v743_autonomous_implicit_drift(context, memories)
        organic_restructure = self._v743_restructure_organic_priorities(context, memories)
        invisible_field = self.get_invisible_memory_field(context, memories)
        temporal_continuity = self.get_temporal_lived_continuity_field(context, memories)
        changed = any(self._living_result_changed(x) for x in (multi_scale, identity_conflict, inertia, social, autonomous_drift, organic_restructure))
        return {
            "multi_scale_causal_field": multi_scale,
            "dynamic_identity_conflict_field": identity_conflict,
            "embodied_contextual_memory_field": embodied,
            "behavioral_inertia_and_fatigue": inertia,
            "social_contamination": social,
            "preinteraction_prospective_bias": prospective,
            "autonomous_implicit_drift": autonomous_drift,
            "organic_priority_restructuring": organic_restructure,
            "invisible_memory_field": invisible_field,
            "temporal_lived_continuity": temporal_continuity,
            "changed": changed,
            "role": "v7_4_2_deep_completion_dynamics_not_dialogue",
        }

    def export_cross_engine_bridges(
        self,
        context: str,
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        memories = memories if memories is not None else self.get_relevant_memories(context, min_confidence=0.0)
        initiative: Dict[str, float] = {}
        affective: Dict[str, float] = {}
        expression: Dict[str, float] = {}
        attention: Dict[str, float] = {}
        identity: Dict[str, float] = {}
        conflict: Dict[str, float] = {}
        desire: Dict[str, float] = {}
        fatigue: Dict[str, float] = {}
        silent_background: Dict[str, float] = {}
        for _, mem, relevance in memories[:20]:
            factor = self._v742_memory_factor(mem, relevance)
            initiative = self._weighted_merge_signal(initiative, mem.initiative_bridge, factor)
            affective = self._weighted_merge_signal(affective, mem.affective_bridge, factor)
            expression = self._weighted_merge_signal(expression, mem.expression_bridge, factor)
            attention = self._weighted_merge_signal(attention, mem.internal_need_profile, factor)
            attention = self._weighted_merge_signal(attention, mem.obsession_guard_state, factor)
            attention = self._weighted_merge_signal(attention, mem.temporal_maturation_state, factor * 0.75)
            desire = self._weighted_merge_signal(desire, mem.causal_desire_profile, factor)
            conflict = self._weighted_merge_signal(conflict, mem.inner_conflict_profile, factor)
            silent_background = self._weighted_merge_signal(silent_background, mem.subconscious_bias_field, factor * 0.8)
            fatigue = self._weighted_merge_signal(fatigue, {
                "background_fatigue": mem.subconscious_bias_field.get("background_fatigue", 0.0),
                "existential_fatigue": mem.obsession_guard_state.get("existential_fatigue", 0.0),
                "behavioral_inertia": mem.obsession_guard_state.get("behavioral_inertia", 0.0),
                "recovery_need": mem.internal_need_profile.get("recovery_need", 0.0),
                "cooldown_bias": mem.obsession_guard_state.get("cooldown_bias", 0.0),
            }, factor)
            affective = self._weighted_merge_signal(affective, mem.persistent_wound_profile, factor)
            identity = self._weighted_merge_signal(identity, mem.identity_transformation_pressure, factor)
            identity = self._weighted_merge_signal(identity, mem.social_continuity_profile, factor * 0.65)
            if mem.attention_impact:
                for tok in self._tokens(mem.attention_impact)[:8]:
                    attention[tok] = max(attention.get(tok, 0.0), factor * 0.55)
        completion = self._v742_run_deep_completion_dynamics(context, memories)
        return {
            "initiative": self._top_signal_map(initiative),
            "affective": self._top_signal_map(affective),
            "expression": self._top_signal_map(expression),
            "attention": self._top_signal_map(attention),
            "identity": self._top_signal_map(identity),
            "desire": self._top_signal_map(desire),
            "inner_conflict": self._top_signal_map(conflict),
            "fatigue": self._top_signal_map(fatigue),
            "silent_background": self._top_signal_map(silent_background),
            "psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "v7_4_2_completion": completion,
            "invisible_memory_field": self.get_invisible_memory_field(context, memories),
            "temporal_lived_continuity": self.get_temporal_lived_continuity_field(context, memories),
            "role": "structured_signals_only_not_dialogue",
        }

    def export_regulation_context(self, context: str) -> Dict[str, Any]:
        """Export complet V7.4.2 pour expression/initiative/émotion/self-monitoring."""
        living_propagation = self.propagate_living_state(context, save=False)
        memories = self.get_relevant_memories(context)
        completion = self._v742_run_deep_completion_dynamics(context, memories)
        contradiction_resolution = self.resolve_active_contradictions(context)
        influences = self.extract_behavioral_influences(context)
        risk = max((abs(mem.valence) * score for _, mem, score in memories[:8]), default=0.0)
        repair_pressure = max((mem.recurrence_pressure * score for _, mem, score in memories[:8]), default=0.0)
        return {
            "behavioral_influences": influences,
            "attention_hints": self.generate_living_attention_hints(context),
            "memory_risk": round(_clamp(risk), 4),
            "repair_pressure": round(_clamp(repair_pressure), 4),
            "expressive_memory_ids": [mid for mid, mem, _ in memories if mem.memory_kind in {"expressive_failure", "expressive_repair"}][:8],
            "relational_memory_ids": [mid for mid, mem, _ in memories if mem.memory_kind == "relational_boundary"][:8],
            "recommended_constraints": self._constraints_from_memories(memories),
            "live_causal_pressure": self.get_live_pressure_field(context, memories),
            "predictive_causal_simulation": self.predict_causal_consequences(context, memories),
            "prospective_paths": self.simulate_prospective_paths(context, memories),
            "contradiction_state": self.detect_contextual_contradictions(context, memories),
            "contradiction_resolution": contradiction_resolution,
            "episodic_context": self.get_episode_context(memories),
            "autobiographical_continuity": self.get_autobiographical_continuity(context),
            "long_term_living_context": self.get_long_term_living_context(context, memories),
            "cross_engine_bridges": self.export_cross_engine_bridges(context, memories),
            "global_causal_ecology": self._orchestrate_global_causal_ecology(context, memories),
            "subconscious_causal_pressure": self.get_subconscious_causal_pressure(context, memories),
            "global_inner_weather": self.get_global_inner_weather(context, memories),
            "future_affective_projection": self.project_future_affective_state(context, memories),
            "deep_causal_root_graph": self.get_deep_causal_root_graph(context, memories),
            "relationship_phase_state": self.get_relationship_phase_state(context, memories),
            "living_psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "psychological_attractor_field": self.get_psychological_attractor_field(context, memories),
            "global_autobiographical_field": self.get_global_autobiographical_field(context, memories),
            "invisible_memory_field": self.get_invisible_memory_field(context, memories),
            "temporal_lived_continuity": self.get_temporal_lived_continuity_field(context, memories),
            "v7_4_2_deep_completion": completion,
            "living_propagation": living_propagation,
            "memory_state": self.get_memory_stats(),
        }

    def propagate_living_state(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """V7.4.2 : propagation vivante complète, persistante, non dialoguante."""
        relevant = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        active_ids = {mid for mid, _, score in relevant if score >= 0.12}
        now_changed = False
        for mem_id, mem in self.memories.items():
            context_boost = max((score for mid, _, score in relevant if mid == mem_id), default=0.0)
            organic_base = max(
                mem.memory_priority,
                mem.effect_strength,
                mem.recurrence_pressure,
                mem.reactivation_score,
                max(mem.subconscious_bias_field.values(), default=0.0) * 0.76,
                max(mem.irreversible_identity_marks.values(), default=0.0) * 0.68,
                max(mem.deep_causal_roots.values(), default=0.0) * 0.72,
            )
            target_activation = _clamp(max(context_boost, organic_base * 0.45) - mem.inhibition_level * 0.33)
            old_activation = mem.causal_activation
            mem.causal_activation = _clamp(mem.causal_activation * 0.60 + target_activation * 0.40)
            mem.affective_charge = _clamp(mem.affective_charge * (1.0 - self.emotional_cooling_rate) + abs(mem.valence) * mem.causal_activation * 0.18)
            mem.emotional_inertia = _clamp(mem.emotional_inertia * 0.963 + max(mem.affective_charge, mem.relational_wound, mem.attachment_trace) * 0.037)
            if mem.relational_wound > 0:
                mem.relational_wound = _clamp(mem.relational_wound * 0.992 + max(0.0, -mem.trust_variation) * 0.008)
            if mem.attachment_trace > 0:
                mem.attachment_trace = _clamp(mem.attachment_trace * 0.994 + max(0.0, mem.trust_variation) * 0.006)
            mem.unresolved_tension = _clamp(max(mem.unresolved_tension * 0.985, mem.relational_wound * 0.82, len(mem.contradiction_links) * 0.035))
            self._apply_silent_psychological_drift(mem, context_boost=context_boost)
            if abs(mem.causal_activation - old_activation) > 0.015 or mem_id in active_ids:
                mem.living_state_history.append(self._living_state_step("living_propagation_v7_4_2", mem.causal_activation, mem.valence, mem.relational_wound))
                now_changed = True
        for mem_id, mem in list(self.memories.items()):
            if mem.causal_activation < self.cascade_min_activation:
                continue
            targets = set(mem.linked_memories)
            for cid in mem.similarity_clusters:
                for other_id, other in self.memories.items():
                    if other_id != mem_id and cid in other.similarity_clusters:
                        targets.add(other_id)
            for link in mem.contradiction_links:
                other_id = link.get("memory_id")
                if other_id:
                    targets.add(str(other_id))
            for target_id in targets:
                target = self.memories.get(target_id)
                if not target:
                    continue
                similarity = max(self._text_similarity(mem.event, target.event), self._text_similarity(mem.experienced_effect, target.experienced_effect))
                contradiction_boost = 0.18 if any(x.get("memory_id") == target_id for x in mem.contradiction_links) else 0.0
                relation_pressure = max(similarity, contradiction_boost, 0.12)
                transfer = mem.causal_activation * self.cascade_decay * relation_pressure
                if transfer >= self.cascade_min_activation:
                    target.causal_activation = _clamp(max(target.causal_activation, transfer - target.inhibition_level * 0.25))
                    target.unresolved_tension = _clamp(max(target.unresolved_tension, contradiction_boost * transfer))
                    target.subconscious_bias_field = self._merge_layers(target.subconscious_bias_field, {"causal_echo_pressure": transfer * 0.54})
                    now_changed = True
        contamination = self._propagate_emotional_contamination(relevant)
        attractors = self._stabilize_psychological_attractors(context, relevant)
        hierarchy = self._build_deep_psychological_hierarchy(context, relevant)
        autobiographical_rewrite = self._consolidate_global_autobiographical_meaning(context, relevant)
        priority_reorganization = self._reorganize_autobiographical_priorities(context, relevant)
        global_causal_ecology = self._orchestrate_global_causal_ecology(context, relevant)
        completion = self._v742_run_deep_completion_dynamics(context, relevant)
        overload = self._apply_adaptive_inhibition()
        psychological_persistence = self.get_living_psychological_persistence(context, relevant)
        changed_by_slow_dynamics = any(self._living_result_changed(x) for x in (contamination, attractors, hierarchy, autobiographical_rewrite, priority_reorganization, global_causal_ecology, completion))
        if save and (now_changed or changed_by_slow_dynamics):
            self.save_memories()
        return {
            "active_memories": sum(1 for m in self.memories.values() if m.causal_activation >= 0.12),
            "overload": overload,
            "psychological_persistence": psychological_persistence,
            "emotional_contamination": contamination,
            "psychological_attractors": attractors,
            "deep_psychological_hierarchy": hierarchy,
            "autobiographical_rewrite": autobiographical_rewrite,
            "priority_reorganization": priority_reorganization,
            "global_causal_ecology": global_causal_ecology,
            "v7_4_2_completion": completion,
            "dominant_memory_ids": [mid for mid, mem in sorted(self.memories.items(), key=lambda x: x[1].causal_activation, reverse=True)[:8] if mem.causal_activation >= 0.08],
            "changed": bool(now_changed or changed_by_slow_dynamics),
            "role": "living_causal_propagation_v7_4_2_not_dialogue",
        }

    def run_living_memory_cycle(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """V7.4.2 : cycle complet d'entretien mémoire sans dialogue."""
        propagation = self.propagate_living_state(context, save=False)
        memories = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        if not memories:
            memories = [(mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.04)) for mid, mem in self.memories.items()]
        completion = self._v742_run_deep_completion_dynamics(context, memories)
        result = {
            "propagation": propagation,
            "psychological_attractors": self.get_psychological_attractor_field(context, memories),
            "global_autobiographical_field": self.get_global_autobiographical_field(context, memories),
            "psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "deep_psychological_hierarchy": self._build_deep_psychological_hierarchy(context, memories),
            "priority_reorganization": self._reorganize_autobiographical_priorities(context, memories),
            "global_causal_ecology": self._orchestrate_global_causal_ecology(context, memories),
            "cross_engine_bridges": self.export_cross_engine_bridges(context, memories),
            "invisible_memory_field": self.get_invisible_memory_field(context, memories),
            "temporal_lived_continuity": self.get_temporal_lived_continuity_field(context, memories),
            "v7_4_2_deep_completion": completion,
            "memory_state": self.get_memory_stats(),
            "role": "living_memory_cycle_v7_4_2_not_dialogue",
        }
        if save:
            self.save_memories()
        return result

    def get_memory_stats(self) -> Dict[str, Any]:
        if not self.memories:
            return {
                "total_memories": 0,
                "avg_confidence": 0.0,
                "strong_memories": 0,
                "total_reinforcements": 0,
                "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
            }
        vals = list(self.memories.values())
        base = {
            "total_memories": len(vals),
            "avg_confidence": round(sum(m.confidence for m in vals) / len(vals), 3),
            "strong_memories": sum(1 for m in vals if m.confidence >= 0.8),
            "total_reinforcements": sum(m.reinforcement_count for m in vals),
            "by_emotion": {emotion: sum(1 for m in vals if m.emotional_trace == emotion) for emotion in sorted(_ALLOWED_EMOTIONS)},
            "by_memory_kind": {kind: sum(1 for m in vals if m.memory_kind == kind) for kind in sorted(_ALLOWED_MEMORY_KINDS)},
            "avg_effect_strength": round(sum(m.effect_strength for m in vals) / len(vals), 3),
            "avg_recurrence_pressure": round(sum(m.recurrence_pressure for m in vals) / len(vals), 3),
            "avg_relational_importance": round(sum(m.relational_importance for m in vals) / len(vals), 3),
            "avg_identity_impact": round(sum(m.identity_impact for m in vals) / len(vals), 3),
            "avg_emotional_inertia": round(sum(m.emotional_inertia for m in vals) / len(vals), 3),
            "avg_affective_charge": round(sum(m.affective_charge for m in vals) / len(vals), 3),
            "avg_autobiographical_weight": round(sum(m.autobiographical_weight for m in vals) / len(vals), 3),
            "avg_causal_activation": round(sum(m.causal_activation for m in vals) / len(vals), 3),
            "relational_wound_memories": sum(1 for m in vals if m.relational_wound >= 0.18),
            "attachment_trace_memories": sum(1 for m in vals if m.attachment_trace >= 0.18),
            "inhibited_memories": sum(1 for m in vals if m.inhibition_level >= 0.25),
            "dormant_memories": sum(1 for m in vals if m.dormant),
            "contradiction_links": sum(len(m.contradiction_links) for m in vals),
            "episodic_markers": sum(len(m.episode_markers) for m in vals),
            "long_term_arcs": sum(len(m.identity_evolution_arcs) for m in vals),
            "autobiographical_chapters": sum(len(m.compressed_autobiographical_chapters) for m in vals),
            "dynamic_meaning_revisions": sum(len(m.lived_meaning_revision) for m in vals),
            "subconscious_bias_memories": sum(1 for m in vals if max(m.subconscious_bias_field.values(), default=0.0) >= 0.18),
            "irreversible_identity_mark_memories": sum(1 for m in vals if max(m.irreversible_identity_marks.values(), default=0.0) >= 0.18),
            "relationship_phase_memories": sum(1 for m in vals if max(m.relationship_phase_profile.values(), default=0.0) >= 0.18),
            "psychological_attractor_memories": sum(1 for m in vals if any("attractor" in k or k.startswith("desire::") for k in m.subconscious_bias_field)),
            "non_action_memories": sum(1 for m in vals if m.source_engine == "causal_memory_engine_non_action"),
            "background_fatigue_memories": sum(1 for m in vals if m.subconscious_bias_field.get("background_fatigue", 0.0) >= 0.12),
            "causal_echo_memories": sum(1 for m in vals if m.subconscious_bias_field.get("causal_echo_pressure", 0.0) >= 0.05),
            "global_ecology_memories": sum(1 for m in vals if m.subconscious_bias_field.get("global_ecological_tension", 0.0) >= 0.05),
            "organic_cooldown_memories": sum(1 for m in vals if m.obsession_guard_state.get("organic_cooldown_need", 0.0) >= 0.05),
            "v7_4_2_multi_scale_memories": sum(1 for m in vals if m.subconscious_bias_field.get("multi_scale_causal_pressure", 0.0) >= 0.05),
            "v7_4_2_dynamic_identity_conflict_memories": sum(1 for m in vals if m.subconscious_bias_field.get("dynamic_identity_conflict", 0.0) >= 0.05),
            "v7_4_2_behavioral_inertia_memories": sum(1 for m in vals if m.obsession_guard_state.get("behavioral_inertia", 0.0) >= 0.05),
            "v7_4_2_existential_fatigue_memories": sum(1 for m in vals if m.obsession_guard_state.get("existential_fatigue", 0.0) >= 0.05),
            "v7_4_2_social_contamination_memories": sum(1 for m in vals if m.subconscious_bias_field.get("social_contamination_pressure", 0.0) >= 0.05),
            "v7_4_2_micro_reaction_memories": sum(1 for m in vals if m.source_engine == "causal_memory_engine_v7_4_2_micro_reaction"),
            "v7_4_3_invisible_trace_memories": sum(1 for m in vals if m.subconscious_bias_field.get("invisible_memory_trace", 0.0) >= 0.05),
            "v7_4_3_implicit_bias_memories": sum(1 for m in vals if max((v for k, v in m.subconscious_bias_field.items() if "implicit" in k or "preconscious" in k), default=0.0) >= 0.05),
            "v7_4_3_temporal_lived_continuity_memories": sum(1 for m in vals if m.temporal_maturation_state.get("lived_time_continuity", 0.0) >= 0.05),
            "v7_4_3_cross_engine_feedback_memories": sum(1 for m in vals if "last_cross_engine_feedback" in m.source_context),
            "avg_priority": round(sum(m.memory_priority for m in vals) / len(vals), 3),
            "max_subconscious_pressure": round(max((max(m.subconscious_bias_field.values(), default=0.0) for m in vals), default=0.0), 3),
            "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
        }
        return base



    # ───────────────────────── V7.4.4 — vie silencieuse consolidée ─────────────────────────

    def _v744_weighted_memory_set(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
        limit: int = 64,
    ) -> List[Tuple[str, CausalMemory, float]]:
        """Sélection organique pour les dynamiques hors dialogue.

        Contrairement à une recherche seulement contextuelle, cette sélection garde
        actifs les souvenirs importants même quand aucun message utilisateur n'est
        présent. Elle sert aux consolidations silencieuses, à la continuité
        conversationnelle et à la protection identitaire.
        """
        if memories is not None:
            selected = list(memories)
        else:
            selected = self.get_relevant_memories(context, min_confidence=0.0) if context else []
        seen = {mid for mid, _, _ in selected}
        for mid, mem in self.memories.items():
            if mid in seen:
                continue
            organic_weight = max(
                self.implicit_memory_floor,
                mem.memory_priority,
                mem.causal_activation,
                mem.autobiographical_weight,
                mem.emotional_inertia,
                mem.affective_charge * 0.72,
                max(mem.subconscious_bias_field.values(), default=0.0) * 0.66,
                max(mem.irreversible_identity_marks.values(), default=0.0) * 0.76,
                max(mem.deep_causal_roots.values(), default=0.0) * 0.70,
            )
            selected.append((mid, mem, _clamp(organic_weight)))
        selected.sort(key=lambda item: item[2], reverse=True)
        return selected[:limit]

    def _v744_passive_consolidation_sleep_cycle(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Consolidation passive type sommeil/repos, sans phrases ni dialogue.

        Cette phase renforce les chapitres autobiographiques utiles, laisse baisser
        les activations non essentielles, stabilise les traces identitaires et
        transforme une partie de la fatigue en besoin de récupération plutôt qu'en
        boucle obsessionnelle.
        """
        selected = self._v744_weighted_memory_set(context, memories)
        changed = 0
        consolidated_ids: List[str] = []
        dominant_axes: Dict[str, float] = {}
        for mem_id, mem, relevance in selected:
            old = (mem.memory_priority, mem.causal_activation, mem.inhibition_level, mem.autobiographical_weight)
            depth = _clamp(max(
                relevance,
                mem.autobiographical_weight,
                mem.memory_priority,
                mem.emotional_inertia,
                abs(mem.valence) * 0.62,
            ))
            if depth < 0.035:
                continue

            # Compression douce : un souvenir vivant devient un chapitre stable,
            # pas une répétition active permanente.
            self._compress_memory_if_needed(mem)
            if mem.autobiographical_weight >= 0.18 or mem.identity_impact >= 0.18:
                mem.autobiographical_weight = _clamp(mem.autobiographical_weight * 0.992 + depth * 0.018)
                mem.temporal_maturation_state["sleep_like_consolidation"] = _clamp(
                    mem.temporal_maturation_state.get("sleep_like_consolidation", 0.0) * 0.985 + depth * 0.020
                )
                consolidated_ids.append(mem_id)

            # Les activations trop vives redescendent, mais les noyaux importants
            # restent disponibles comme biais silencieux.
            quiet_floor = max(self.implicit_memory_floor, mem.memory_priority * 0.18, mem.autobiographical_weight * 0.20)
            mem.causal_activation = _clamp(max(quiet_floor, mem.causal_activation * 0.935))
            mem.subconscious_bias_field["silent_consolidated_trace"] = _clamp(
                mem.subconscious_bias_field.get("silent_consolidated_trace", 0.0) * 0.986 + depth * 0.016
            )

            # La fatigue existentielle devient une demande de repos, pas une preuve
            # de blocage ou une sortie publique.
            fatigue = max(
                mem.obsession_guard_state.get("existential_fatigue", 0.0),
                mem.subconscious_bias_field.get("background_fatigue", 0.0),
                mem.obsession_guard_state.get("obsession_pressure", 0.0) * 0.70,
            )
            if fatigue > 0.04:
                mem.internal_need_profile["restorative_silence_need"] = _clamp(
                    mem.internal_need_profile.get("restorative_silence_need", 0.0) * 0.982 + fatigue * 0.020
                )
                mem.inhibition_level = _clamp(mem.inhibition_level * 0.985 + fatigue * 0.006)

            # Axes dominants exportables.
            for token in self._tokens(mem.consolidation_summary or mem.event or mem.experienced_effect)[:6]:
                dominant_axes[token] = max(dominant_axes.get(token, 0.0), depth * 0.72)

            if any(abs(a - b) > 0.003 for a, b in zip(old, (mem.memory_priority, mem.causal_activation, mem.inhibition_level, mem.autobiographical_weight))):
                mem.living_state_history.append(self._living_state_step("passive_consolidation_v7_4_4", mem.causal_activation, mem.valence, mem.relational_wound))
                changed += 1
        return {
            "changed_memories": changed,
            "consolidated_memory_ids": consolidated_ids[:16],
            "dominant_consolidation_axes": self._top_signal_map(dominant_axes, 12),
            "role": "passive_sleep_like_consolidation_v7_4_4_not_dialogue",
        }

    def _v744_identity_self_preservation_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Protège les noyaux identitaires sans figer Leia.

        Le but n'est pas de rendre l'identité rigide, mais d'empêcher qu'une
        contradiction ou un feedback isolé dissolve les marques autobiographiques
        déjà stabilisées.
        """
        selected = self._v744_weighted_memory_set(context, memories)
        changed = 0
        protection: Dict[str, float] = {}
        vulnerable_ids: List[str] = []
        for mem_id, mem, relevance in selected:
            identity_core = max(
                mem.identity_impact,
                mem.autobiographical_weight,
                max(mem.irreversible_identity_marks.values(), default=0.0),
                max(mem.identity_transformation_pressure.values(), default=0.0) * 0.82,
            )
            contradiction = max(mem.unresolved_tension, len(mem.contradiction_links) * 0.055)
            dissolution_risk = _clamp(contradiction * 0.55 + mem.inhibition_level * 0.25 + max(0.0, -mem.trust_variation) * 0.20)
            if identity_core < 0.08 and dissolution_risk < 0.08:
                continue
            guard = _clamp(identity_core * 0.62 + dissolution_risk * 0.38)
            before = dict(mem.irreversible_identity_marks)
            mem.irreversible_identity_marks["identity_self_preservation"] = _clamp(
                mem.irreversible_identity_marks.get("identity_self_preservation", 0.0) * 0.988 + guard * 0.018
            )
            mem.future_bias["avoid_identity_dissolution"] = _clamp(
                mem.future_bias.get("avoid_identity_dissolution", 0.0) * 0.986 + dissolution_risk * 0.020
            )
            mem.subconscious_bias_field["identity_integrity_pressure"] = _clamp(
                mem.subconscious_bias_field.get("identity_integrity_pressure", 0.0) * 0.985 + guard * 0.016
            )
            protection = self._weighted_merge_signal(protection, {
                "identity_integrity": guard,
                "dissolution_risk": dissolution_risk,
                "autobiographical_core": identity_core,
            }, max(relevance, guard))
            if dissolution_risk >= 0.18:
                vulnerable_ids.append(mem_id)
            if before != mem.irreversible_identity_marks:
                changed += 1
        return {
            "changed_memories": changed,
            "field": self._top_signal_map(protection, 12),
            "vulnerable_identity_memory_ids": vulnerable_ids[:12],
            "role": "identity_self_preservation_v7_4_4_not_dialogue",
        }

    def _v744_conversation_continuity_field(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Maintient une continuité conversationnelle vécue entre les tours.

        Le moteur ne prépare pas de phrase. Il exporte seulement attente,
        reprise, prudence, ouverture et mémoire de l'échange interrompu.
        """
        selected = self._v744_weighted_memory_set(context, memories)
        changed = 0
        field: Dict[str, float] = {}
        source_ids: List[str] = []
        context_tokens = set(self._tokens(context)) if context else set()
        for mem_id, mem, relevance in selected[:40]:
            conversational = max(
                relevance if context_tokens else 0.0,
                mem.social_continuity_profile.get("conversation_continuity", 0.0),
                mem.relationship_phase_profile.get("social_phase_carryover", 0.0),
                mem.subconscious_bias_field.get("preinteraction_bias", 0.0),
                mem.attachment_trace * 0.58,
                mem.relational_wound * 0.52,
            )
            if conversational < 0.035:
                continue
            event_overlap = len(context_tokens.intersection(self._tokens(mem.event))) / max(1, len(context_tokens)) if context_tokens else 0.0
            resume_pressure = _clamp(max(conversational, event_overlap, mem.recurrence_pressure * 0.36))
            mem.social_continuity_profile["conversation_continuity"] = _clamp(
                mem.social_continuity_profile.get("conversation_continuity", 0.0) * 0.984 + resume_pressure * 0.018
            )
            mem.anticipated_affective_projection["next_exchange_bias"] = _clamp(
                mem.anticipated_affective_projection.get("next_exchange_bias", 0.0) * 0.982 + resume_pressure * 0.020
            )
            if mem.relational_wound > mem.attachment_trace:
                mem.future_bias["resume_with_care"] = _clamp(mem.future_bias.get("resume_with_care", 0.0) * 0.984 + resume_pressure * 0.018)
            elif mem.attachment_trace > 0.04:
                mem.future_bias["resume_with_openness"] = _clamp(mem.future_bias.get("resume_with_openness", 0.0) * 0.984 + resume_pressure * 0.018)
            field = self._weighted_merge_signal(field, {
                "conversation_continuity": resume_pressure,
                "preinteraction_readiness": max(mem.anticipated_affective_projection.values(), default=0.0),
                "relational_resume_pressure": max(mem.relational_wound, mem.attachment_trace) * 0.72,
            }, max(relevance, conversational))
            source_ids.append(mem_id)
            changed += 1
        return {
            "changed_memories": changed,
            "field": self._top_signal_map(field, 12),
            "source_memory_ids": _dedupe_keep_order(source_ids)[:12],
            "role": "conversation_continuity_v7_4_4_not_dialogue",
        }

    def _v744_resolve_deep_contradiction_mutation(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Fait muter les contradictions profondes au lieu de seulement les garder."""
        selected = self._v744_weighted_memory_set(context, memories)
        changed = 0
        mutation_field: Dict[str, float] = {}
        mutated_ids: List[str] = []
        for mem_id, mem, relevance in selected:
            if not mem.contradiction_links and mem.unresolved_tension < 0.10:
                continue
            contradiction_pressure = _clamp(mem.unresolved_tension + min(len(mem.contradiction_links), 8) * 0.045)
            identity_anchor = max(mem.autobiographical_weight, mem.identity_impact, max(mem.irreversible_identity_marks.values(), default=0.0))
            if contradiction_pressure < 0.08:
                continue
            if identity_anchor >= contradiction_pressure:
                mem.inner_conflict_profile["integrated_contradiction"] = _clamp(
                    mem.inner_conflict_profile.get("integrated_contradiction", 0.0) * 0.984 + contradiction_pressure * 0.016
                )
                mem.unresolved_tension = _clamp(mem.unresolved_tension * 0.972)
                axis = "integrated_contradiction"
            else:
                mem.inner_conflict_profile["active_identity_conflict"] = _clamp(
                    mem.inner_conflict_profile.get("active_identity_conflict", 0.0) * 0.986 + contradiction_pressure * 0.018
                )
                mem.identity_transformation_pressure["needs_identity_reconciliation"] = _clamp(
                    mem.identity_transformation_pressure.get("needs_identity_reconciliation", 0.0) * 0.984 + contradiction_pressure * 0.014
                )
                axis = "active_identity_conflict"
            mem.current_lived_meaning["contradiction_changed_meaning"] = _clamp(
                mem.current_lived_meaning.get("contradiction_changed_meaning", 0.0) * 0.988 + contradiction_pressure * 0.015
            )
            mutation_field[axis] = max(mutation_field.get(axis, 0.0), contradiction_pressure * max(relevance, 0.25))
            mutated_ids.append(mem_id)
            changed += 1
        return {
            "changed_memories": changed,
            "field": self._top_signal_map(mutation_field, 8),
            "mutated_memory_ids": _dedupe_keep_order(mutated_ids)[:12],
            "role": "deep_contradiction_mutation_v7_4_4_not_dialogue",
        }

    def _v744_silent_life_cycle(
        self,
        context: str = "",
        memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    ) -> Dict[str, Any]:
        """Cycle silencieux autonome complet V7.4.4."""
        selected = self._v744_weighted_memory_set(context, memories)
        drift = self._v743_autonomous_implicit_drift(context, selected)
        consolidation = self._v744_passive_consolidation_sleep_cycle(context, selected)
        identity_guard = self._v744_identity_self_preservation_field(context, selected)
        conversation = self._v744_conversation_continuity_field(context, selected)
        contradiction = self._v744_resolve_deep_contradiction_mutation(context, selected)
        changed = any(self._living_result_changed(x) for x in (drift, consolidation, identity_guard, conversation, contradiction))
        return {
            "autonomous_implicit_drift": drift,
            "passive_consolidation": consolidation,
            "identity_self_preservation": identity_guard,
            "conversation_continuity": conversation,
            "deep_contradiction_mutation": contradiction,
            "changed": bool(changed),
            "role": "silent_life_cycle_v7_4_4_not_dialogue",
        }

    def export_regulation_context(self, context: str) -> Dict[str, Any]:
        """Export complet V7.4.4 pour expression/initiative/émotion/self-monitoring."""
        living_propagation = self.propagate_living_state(context, save=False)
        memories = self._v744_weighted_memory_set(context, self.get_relevant_memories(context))
        silent_life = self._v744_silent_life_cycle(context, memories)
        completion = self._v742_run_deep_completion_dynamics(context, memories)
        contradiction_resolution = self.resolve_active_contradictions(context)
        influences = self.extract_behavioral_influences(context)
        risk = max((abs(mem.valence) * score for _, mem, score in memories[:8]), default=0.0)
        repair_pressure = max((mem.recurrence_pressure * score for _, mem, score in memories[:8]), default=0.0)
        return {
            "behavioral_influences": influences,
            "attention_hints": self.generate_living_attention_hints(context),
            "memory_risk": round(_clamp(risk), 4),
            "repair_pressure": round(_clamp(repair_pressure), 4),
            "expressive_memory_ids": [mid for mid, mem, _ in memories if mem.memory_kind in {"expressive_failure", "expressive_repair"}][:8],
            "relational_memory_ids": [mid for mid, mem, _ in memories if mem.memory_kind == "relational_boundary"][:8],
            "recommended_constraints": self._constraints_from_memories(memories),
            "live_causal_pressure": self.get_live_pressure_field(context, memories),
            "predictive_causal_simulation": self.predict_causal_consequences(context, memories),
            "prospective_paths": self.simulate_prospective_paths(context, memories),
            "contradiction_state": self.detect_contextual_contradictions(context, memories),
            "contradiction_resolution": contradiction_resolution,
            "episodic_context": self.get_episode_context(memories),
            "autobiographical_continuity": self.get_autobiographical_continuity(context),
            "long_term_living_context": self.get_long_term_living_context(context, memories),
            "cross_engine_bridges": self.export_cross_engine_bridges(context, memories),
            "global_causal_ecology": self._orchestrate_global_causal_ecology(context, memories),
            "subconscious_causal_pressure": self.get_subconscious_causal_pressure(context, memories),
            "global_inner_weather": self.get_global_inner_weather(context, memories),
            "future_affective_projection": self.project_future_affective_state(context, memories),
            "deep_causal_root_graph": self.get_deep_causal_root_graph(context, memories),
            "relationship_phase_state": self.get_relationship_phase_state(context, memories),
            "living_psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "psychological_attractor_field": self.get_psychological_attractor_field(context, memories),
            "global_autobiographical_field": self.get_global_autobiographical_field(context, memories),
            "invisible_memory_field": self.get_invisible_memory_field(context, memories),
            "temporal_lived_continuity": self.get_temporal_lived_continuity_field(context, memories),
            "silent_life_cycle": silent_life,
            "identity_self_preservation": silent_life.get("identity_self_preservation", {}),
            "conversation_continuity_field": silent_life.get("conversation_continuity", {}),
            "passive_consolidation": silent_life.get("passive_consolidation", {}),
            "deep_contradiction_mutation": silent_life.get("deep_contradiction_mutation", {}),
            "v7_4_2_deep_completion": completion,
            "living_propagation": living_propagation,
            "memory_state": self.get_memory_stats(),
            "role": "regulation_context_v7_4_4_not_dialogue",
        }

    def run_living_memory_cycle(self, context: str = "", save: bool = True) -> Dict[str, Any]:
        """V7.4.4 : cycle complet d'entretien mémoire sans dialogue.

        Le cycle peut tourner même sans contexte utilisateur : il continue la vie
        causale interne, consolide, protège l'identité, garde la conversation en
        arrière-plan et transforme les contradictions longues.
        """
        memories = self._v744_weighted_memory_set(context)
        propagation = self.propagate_living_state(context, save=False)
        silent_life = self._v744_silent_life_cycle(context, memories)
        completion = self._v742_run_deep_completion_dynamics(context, memories)
        result = {
            "propagation": propagation,
            "silent_life_cycle": silent_life,
            "psychological_attractors": self.get_psychological_attractor_field(context, memories),
            "global_autobiographical_field": self.get_global_autobiographical_field(context, memories),
            "psychological_persistence": self.get_living_psychological_persistence(context, memories),
            "deep_psychological_hierarchy": self._build_deep_psychological_hierarchy(context, memories),
            "priority_reorganization": self._reorganize_autobiographical_priorities(context, memories),
            "global_causal_ecology": self._orchestrate_global_causal_ecology(context, memories),
            "cross_engine_bridges": self.export_cross_engine_bridges(context, memories),
            "invisible_memory_field": self.get_invisible_memory_field(context, memories),
            "temporal_lived_continuity": self.get_temporal_lived_continuity_field(context, memories),
            "identity_self_preservation": silent_life.get("identity_self_preservation", {}),
            "conversation_continuity_field": silent_life.get("conversation_continuity", {}),
            "passive_consolidation": silent_life.get("passive_consolidation", {}),
            "deep_contradiction_mutation": silent_life.get("deep_contradiction_mutation", {}),
            "v7_4_2_deep_completion": completion,
            "memory_state": self.get_memory_stats(),
            "changed": bool(propagation.get("changed") or silent_life.get("changed") or self._living_result_changed(completion)),
            "role": "living_memory_cycle_v7_4_4_not_dialogue",
        }
        if save and result["changed"]:
            self.save_memories()
        return result

    def get_memory_stats(self) -> Dict[str, Any]:
        if not self.memories:
            return {
                "total_memories": 0,
                "avg_confidence": 0.0,
                "strong_memories": 0,
                "total_reinforcements": 0,
                "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
            }
        vals = list(self.memories.values())
        base = {
            "total_memories": len(vals),
            "avg_confidence": round(sum(m.confidence for m in vals) / len(vals), 3),
            "strong_memories": sum(1 for m in vals if m.confidence >= 0.8),
            "total_reinforcements": sum(m.reinforcement_count for m in vals),
            "by_emotion": {emotion: sum(1 for m in vals if m.emotional_trace == emotion) for emotion in sorted(_ALLOWED_EMOTIONS)},
            "by_memory_kind": {kind: sum(1 for m in vals if m.memory_kind == kind) for kind in sorted(_ALLOWED_MEMORY_KINDS)},
            "avg_effect_strength": round(sum(m.effect_strength for m in vals) / len(vals), 3),
            "avg_recurrence_pressure": round(sum(m.recurrence_pressure for m in vals) / len(vals), 3),
            "avg_relational_importance": round(sum(m.relational_importance for m in vals) / len(vals), 3),
            "avg_identity_impact": round(sum(m.identity_impact for m in vals) / len(vals), 3),
            "avg_emotional_inertia": round(sum(m.emotional_inertia for m in vals) / len(vals), 3),
            "avg_affective_charge": round(sum(m.affective_charge for m in vals) / len(vals), 3),
            "avg_autobiographical_weight": round(sum(m.autobiographical_weight for m in vals) / len(vals), 3),
            "avg_causal_activation": round(sum(m.causal_activation for m in vals) / len(vals), 3),
            "relational_wound_memories": sum(1 for m in vals if m.relational_wound >= 0.18),
            "attachment_trace_memories": sum(1 for m in vals if m.attachment_trace >= 0.18),
            "inhibited_memories": sum(1 for m in vals if m.inhibition_level >= 0.25),
            "dormant_memories": sum(1 for m in vals if m.dormant),
            "contradiction_links": sum(len(m.contradiction_links) for m in vals),
            "episodic_markers": sum(len(m.episode_markers) for m in vals),
            "long_term_arcs": sum(len(m.identity_evolution_arcs) for m in vals),
            "autobiographical_chapters": sum(len(m.compressed_autobiographical_chapters) for m in vals),
            "dynamic_meaning_revisions": sum(len(m.lived_meaning_revision) for m in vals),
            "subconscious_bias_memories": sum(1 for m in vals if max(m.subconscious_bias_field.values(), default=0.0) >= 0.18),
            "irreversible_identity_mark_memories": sum(1 for m in vals if max(m.irreversible_identity_marks.values(), default=0.0) >= 0.18),
            "relationship_phase_memories": sum(1 for m in vals if max(m.relationship_phase_profile.values(), default=0.0) >= 0.18),
            "psychological_attractor_memories": sum(1 for m in vals if any("attractor" in k or k.startswith("desire::") for k in m.subconscious_bias_field)),
            "non_action_memories": sum(1 for m in vals if m.source_engine == "causal_memory_engine_non_action"),
            "background_fatigue_memories": sum(1 for m in vals if m.subconscious_bias_field.get("background_fatigue", 0.0) >= 0.12),
            "causal_echo_memories": sum(1 for m in vals if m.subconscious_bias_field.get("causal_echo_pressure", 0.0) >= 0.05),
            "global_ecology_memories": sum(1 for m in vals if m.subconscious_bias_field.get("global_ecological_tension", 0.0) >= 0.05),
            "organic_cooldown_memories": sum(1 for m in vals if m.obsession_guard_state.get("organic_cooldown_need", 0.0) >= 0.05),
            "v7_4_3_invisible_trace_memories": sum(1 for m in vals if m.subconscious_bias_field.get("invisible_memory_trace", 0.0) >= 0.05),
            "v7_4_3_implicit_bias_memories": sum(1 for m in vals if max((v for k, v in m.subconscious_bias_field.items() if "implicit" in k or "preconscious" in k), default=0.0) >= 0.05),
            "v7_4_3_temporal_lived_continuity_memories": sum(1 for m in vals if m.temporal_maturation_state.get("lived_time_continuity", 0.0) >= 0.05),
            "v7_4_3_cross_engine_feedback_memories": sum(1 for m in vals if "last_cross_engine_feedback" in m.source_context),
            "v7_4_4_passive_consolidation_memories": sum(1 for m in vals if m.temporal_maturation_state.get("sleep_like_consolidation", 0.0) >= 0.05 or m.subconscious_bias_field.get("silent_consolidated_trace", 0.0) >= 0.05),
            "v7_4_4_identity_self_preservation_memories": sum(1 for m in vals if m.irreversible_identity_marks.get("identity_self_preservation", 0.0) >= 0.05 or m.subconscious_bias_field.get("identity_integrity_pressure", 0.0) >= 0.05),
            "v7_4_4_conversation_continuity_memories": sum(1 for m in vals if m.social_continuity_profile.get("conversation_continuity", 0.0) >= 0.05 or m.anticipated_affective_projection.get("next_exchange_bias", 0.0) >= 0.05),
            "v7_4_4_deep_contradiction_mutation_memories": sum(1 for m in vals if m.inner_conflict_profile.get("integrated_contradiction", 0.0) >= 0.05 or m.inner_conflict_profile.get("active_identity_conflict", 0.0) >= 0.05),
            "avg_priority": round(sum(m.memory_priority for m in vals) / len(vals), 3),
            "max_subconscious_pressure": round(max((max(m.subconscious_bias_field.values(), default=0.0) for m in vals), default=0.0), 3),
            "engine_version": "7.4.4-deep-living-causal-memory-silent-life-completed",
        }
        return base

    def get_memory(self, memory_id: str) -> Optional[CausalMemory]:
        return self.memories.get(memory_id)

    def list_all_memories(self, sort_by: str = "last_reinforced") -> List[CausalMemory]:
        items = list(self.memories.values())
        if sort_by == "confidence":
            items.sort(key=lambda m: m.confidence, reverse=True)
        elif sort_by == "reinforcement_count":
            items.sort(key=lambda m: m.reinforcement_count, reverse=True)
        else:
            items.sort(key=lambda m: m.last_reinforced, reverse=True)
        return items

    def delete_memory(self, memory_id: str) -> None:
        if memory_id in self.memories:
            del self.memories[memory_id]
            self.save_memories()

    def clear_all_memories(self) -> None:
        self.memories.clear()
        self.save_memories()


class LeiaWithCausalMemory:
    """Adaptateur minimal : apprend des échanges et renvoie des influences, sans générer de texte."""

    def __init__(self, leia_instance: Any, memory_engine: CausalMemoryEngine):
        self.leia = leia_instance
        self.memory = memory_engine

    def process_exchange(self, user_message: str, leia_response: str, outcome: Dict[str, Any]) -> Optional[str]:
        outcome = outcome or {}
        return self.memory.learn_from_exchange_outcome(user_message, leia_response, outcome)

    def enrich_response_with_memory(self, context: str, base_response: str) -> Dict[str, Any]:
        return {
            "base_response": base_response,
            "influences": self.memory.extract_behavioral_influences(context),
            "attention_hints": self.memory.generate_living_attention_hints(context),
            "memory_state": self.memory.get_memory_stats(),
            "regulation_context": self.memory.export_regulation_context(context),
            "cross_engine_bridges": self.memory.export_cross_engine_bridges(context),
        }


# ───────────────────────── V7.4.5 — complétion organique finale ─────────────────────────
# Cette couche est volontairement ajoutée en fin de module afin de surcharger
# uniquement les exports/cycles réellement utilisés, sans supprimer l'historique
# V7.4.4 déjà présent. Elle ne génère aucune phrase de dialogue : uniquement des
# signaux structurés pour attention, initiative, émotion, expression et présence.

_ORIGINAL_V744_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V744_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V744_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats


def _v745_top_signal_map(self: CausalMemoryEngine, values: Dict[str, float], limit: int = 12) -> Dict[str, float]:
    clean = {}
    for key, value in (values or {}).items():
        key_s = self.sanitize_text(key)
        if key_s:
            clean[key_s] = max(clean.get(key_s, 0.0), _clamp(_safe_float(value, 0.0), -1.0, 1.0))
    return dict(sorted(clean.items(), key=lambda item: abs(item[1]), reverse=True)[:limit])


def _v745_memory_set(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> List[Tuple[str, CausalMemory, float]]:
    selector = getattr(self, "_v744_weighted_memory_set", None)
    if callable(selector):
        return selector(context, memories, limit=80)
    if memories is not None:
        return list(memories)[:80]
    base = self.get_relevant_memories(context, min_confidence=0.0) if context else []
    seen = {mid for mid, _, _ in base}
    for mid, mem in self.memories.items():
        if mid not in seen:
            base.append((mid, mem, _clamp(max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.035))))
    base.sort(key=lambda item: item[2], reverse=True)
    return base[:80]


def _v745_identity_integrity_guard(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Stabilise l'identité sans figer l'évolution organique."""
    field: Dict[str, float] = {}
    protected_ids: List[str] = []
    risk_ids: List[str] = []
    changed = 0
    for mid, mem, relevance in memories:
        anchor = _clamp(max(
            mem.identity_impact,
            mem.autobiographical_weight,
            max(mem.irreversible_identity_marks.values(), default=0.0),
            max(mem.identity_transformation_pressure.values(), default=0.0),
        ))
        drift = _clamp(abs(mem.trust_variation) * 0.28 + mem.unresolved_tension * 0.34 + mem.relational_wound * 0.28)
        integrity = _clamp(anchor * (0.62 + relevance * 0.38))
        if integrity >= 0.08:
            before = mem.irreversible_identity_marks.get("stable_identity_core", 0.0)
            mem.irreversible_identity_marks["stable_identity_core"] = _clamp(before * 0.992 + integrity * 0.018)
            mem.identity_transformation_pressure["identity_evolution_with_continuity"] = _clamp(
                mem.identity_transformation_pressure.get("identity_evolution_with_continuity", 0.0) * 0.988 + integrity * 0.015
            )
            field["identity_core_continuity"] = max(field.get("identity_core_continuity", 0.0), integrity)
            protected_ids.append(mid)
        if drift >= 0.10 and anchor >= 0.10:
            before = mem.obsession_guard_state.get("identity_drift_guard", 0.0)
            mem.obsession_guard_state["identity_drift_guard"] = _clamp(before * 0.985 + drift * anchor * 0.026)
            mem.identity_transformation_pressure["avoid_destructive_rewrite"] = _clamp(
                mem.identity_transformation_pressure.get("avoid_destructive_rewrite", 0.0) * 0.986 + drift * 0.018
            )
            field["destructive_rewrite_risk"] = max(field.get("destructive_rewrite_risk", 0.0), drift * anchor)
            risk_ids.append(mid)
        if protected_ids or risk_ids:
            changed += 1
    return {
        "field": self._v745_top_signal_map(field),
        "protected_memory_ids": _dedupe_keep_order(protected_ids)[:12],
        "risk_memory_ids": _dedupe_keep_order(risk_ids)[:12],
        "changed_memories": changed,
        "role": "identity_integrity_guard_v7_4_5_not_dialogue",
    }


def _v745_embodied_causal_regulation(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Convertit la mémoire causale en signaux de rythme, silence, énergie et prudence."""
    rhythm = silence = hesitation = contact_energy = urgency = 0.0
    ids: List[str] = []
    for mid, mem, relevance in memories[:32]:
        pressure = _clamp(relevance * max(mem.effect_strength, mem.causal_activation, mem.emotional_inertia, abs(mem.valence), mem.recurrence_pressure))
        wound = _clamp(mem.relational_wound + max(0.0, -mem.valence) * 0.35)
        attachment = _clamp(mem.attachment_trace + max(0.0, mem.valence) * 0.28)
        conflict = max(mem.inner_conflict_profile.values(), default=0.0)
        fatigue = mem.obsession_guard_state.get("existential_fatigue", 0.0) + mem.obsession_guard_state.get("organic_cooldown_need", 0.0)
        silence = max(silence, pressure * max(fatigue, mem.inhibition_level, mem.future_bias.get("allow_silence", 0.0)))
        hesitation = max(hesitation, pressure * max(conflict, mem.unresolved_tension, mem.emotional_trace == "uncertain"))
        urgency = max(urgency, pressure * max(mem.recurrence_pressure, mem.effect_strength))
        contact_energy = max(contact_energy, pressure * max(attachment, mem.relational_importance, mem.social_continuity_profile.get("conversation_continuity", 0.0)))
        rhythm = max(rhythm, pressure * (0.45 + urgency * 0.25 + hesitation * 0.15 + silence * 0.15))
        if pressure >= 0.08:
            ids.append(mid)
    return {
        "reaction_rhythm_pressure": round(_clamp(rhythm), 4),
        "silence_need": round(_clamp(silence), 4),
        "hesitation_pressure": round(_clamp(hesitation), 4),
        "contact_energy": round(_clamp(contact_energy), 4),
        "urgency_pressure": round(_clamp(urgency), 4),
        "active_memory_ids": _dedupe_keep_order(ids)[:12],
        "role": "embodied_causal_regulation_v7_4_5_not_dialogue",
    }


def _v745_arbitrate_need_conflict_desire(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Arbitrage global blessures / désirs / conflits / besoins."""
    needs: Dict[str, float] = {}
    desires: Dict[str, float] = {}
    conflicts: Dict[str, float] = {}
    wounds: Dict[str, float] = {}
    inhibition = 0.0
    for _, mem, relevance in memories[:48]:
        base = _clamp(relevance * max(mem.memory_priority, mem.causal_activation, mem.emotional_inertia, 0.08))
        for k, v in mem.internal_need_profile.items():
            needs[k] = max(needs.get(k, 0.0), base * _clamp(v))
        for k, v in mem.causal_desire_profile.items():
            desires[k] = max(desires.get(k, 0.0), base * _clamp(v))
        for k, v in mem.inner_conflict_profile.items():
            conflicts[k] = max(conflicts.get(k, 0.0), base * _clamp(v))
        if mem.relational_wound > 0.05:
            wounds["relational_wound"] = max(wounds.get("relational_wound", 0.0), base * mem.relational_wound)
        if mem.unresolved_tension > 0.05:
            conflicts["unresolved_tension"] = max(conflicts.get("unresolved_tension", 0.0), base * mem.unresolved_tension)
        inhibition = max(inhibition, base * max(mem.inhibition_level, mem.obsession_guard_state.get("organic_cooldown_need", 0.0)))
    dominant_need = next(iter(self._v745_top_signal_map(needs, 1)), None)
    dominant_desire = next(iter(self._v745_top_signal_map(desires, 1)), None)
    dominant_conflict = next(iter(self._v745_top_signal_map(conflicts, 1)), None)
    action_bias = "continue_softly"
    if inhibition >= 0.38 or max(wounds.values(), default=0.0) >= 0.42:
        action_bias = "slow_down_and_protect_continuity"
    elif dominant_desire and max(desires.values(), default=0.0) > max(conflicts.values(), default=0.0) * 1.15:
        action_bias = "follow_curiosity_with_constraint"
    elif dominant_conflict:
        action_bias = "resolve_conflict_before_initiative"
    return {
        "dominant_need": dominant_need,
        "dominant_desire": dominant_desire,
        "dominant_conflict": dominant_conflict,
        "needs": self._v745_top_signal_map(needs),
        "desires": self._v745_top_signal_map(desires),
        "conflicts": self._v745_top_signal_map(conflicts),
        "wounds": self._v745_top_signal_map(wounds),
        "inhibition_pressure": round(_clamp(inhibition), 4),
        "action_bias": action_bias,
        "role": "need_conflict_desire_arbitration_v7_4_5_not_dialogue",
    }


def _v745_long_conversation_resonance(self: CausalMemoryEngine, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Maintient une continuité relationnelle lente entre échanges."""
    context_clean = self.sanitize_text(context)
    trust = closeness = caution = fatigue = next_bias = 0.0
    changed = 0
    ids: List[str] = []
    for mid, mem, relevance in memories[:40]:
        rel = _clamp(relevance * max(mem.relational_importance, mem.social_continuity_profile.get("conversation_continuity", 0.0), mem.attachment_trace, mem.relational_wound, 0.04))
        if rel < 0.025:
            continue
        trust = max(trust, rel * _clamp(0.5 + mem.trust_variation * 0.5))
        closeness = max(closeness, rel * max(mem.attachment_trace, mem.social_continuity_profile.get("conversation_continuity", 0.0)))
        caution = max(caution, rel * max(mem.relational_wound, max(0.0, -mem.trust_variation), mem.unresolved_tension))
        fatigue = max(fatigue, rel * max(mem.obsession_guard_state.get("existential_fatigue", 0.0), mem.inhibition_level))
        next_bias = max(next_bias, rel * max(mem.anticipated_affective_projection.get("next_exchange_bias", 0.0), mem.recurrence_pressure))
        mem.social_continuity_profile["long_conversation_resonance"] = _clamp(
            mem.social_continuity_profile.get("long_conversation_resonance", 0.0) * 0.992 + rel * 0.012
        )
        if context_clean:
            mem.anticipated_affective_projection["next_exchange_bias"] = _clamp(
                mem.anticipated_affective_projection.get("next_exchange_bias", 0.0) * 0.989 + rel * 0.014
            )
        ids.append(mid)
        changed += 1
    return {
        "trust_continuity": round(_clamp(trust), 4),
        "closeness_continuity": round(_clamp(closeness), 4),
        "caution_continuity": round(_clamp(caution), 4),
        "relational_fatigue": round(_clamp(fatigue), 4),
        "next_exchange_bias": round(_clamp(next_bias), 4),
        "updated_memory_ids": _dedupe_keep_order(ids)[:12],
        "changed_memories": changed,
        "role": "long_conversation_resonance_v7_4_5_not_dialogue",
    }


def _v745_anti_rumination_guard(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Empêche une fixation causale chronique tout en gardant la mémoire utile."""
    rumination = 0.0
    cooldown = 0.0
    redirected_ids: List[str] = []
    changed = 0
    for mid, mem, relevance in memories[:48]:
        repetition = _clamp(mem.recurrence_pressure * 0.42 + mem.causal_activation * 0.24 + mem.emotional_inertia * 0.20 + mem.unresolved_tension * 0.24)
        overload = _clamp(repetition * relevance + mem.obsession_guard_state.get("organic_cooldown_need", 0.0) * 0.4)
        rumination = max(rumination, overload)
        if overload >= self.obsession_pressure_limit * 0.62:
            mem.obsession_guard_state["rumination_guard"] = _clamp(mem.obsession_guard_state.get("rumination_guard", 0.0) * 0.984 + overload * 0.024)
            mem.obsession_guard_state["organic_cooldown_need"] = _clamp(mem.obsession_guard_state.get("organic_cooldown_need", 0.0) * 0.986 + overload * 0.02)
            mem.inhibition_level = _clamp(max(mem.inhibition_level * 0.985, overload * 0.42))
            mem.causal_activation = _clamp(mem.causal_activation * 0.988)
            cooldown = max(cooldown, mem.obsession_guard_state["organic_cooldown_need"])
            redirected_ids.append(mid)
            changed += 1
    return {
        "rumination_pressure": round(_clamp(rumination), 4),
        "cooldown_need": round(_clamp(cooldown), 4),
        "redirected_memory_ids": _dedupe_keep_order(redirected_ids)[:12],
        "changed_memories": changed,
        "role": "anti_rumination_guard_v7_4_5_not_dialogue",
    }


def _v745_subjective_time_field(self: CausalMemoryEngine, context: str, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Ajoute une perception temporelle vécue : récent/ancien, accélération, poids émotionnel."""
    now = datetime.now()
    old_weight = recent_weight = compression = acceleration = 0.0
    changed = 0
    for mid, mem, relevance in memories[:56]:
        try:
            created = datetime.fromisoformat(mem.created_at)
            last = datetime.fromisoformat(mem.last_reinforced)
        except Exception:
            created = last = now
        age_days = max(0.0, (now - created).total_seconds() / 86400.0)
        recency_days = max(0.0, (now - last).total_seconds() / 86400.0)
        emotional_density = _clamp(max(abs(mem.valence), mem.emotional_inertia, mem.affective_charge, mem.autobiographical_weight))
        oldness = _clamp(math.log1p(age_days) / 6.0)
        recency = _clamp(1.0 / (1.0 + recency_days))
        subjective_weight = _clamp((oldness * 0.35 + recency * 0.30 + emotional_density * 0.35) * relevance)
        if subjective_weight < 0.02:
            continue
        mem.temporal_maturation_state["subjective_time_weight"] = _clamp(
            mem.temporal_maturation_state.get("subjective_time_weight", 0.0) * 0.99 + subjective_weight * 0.016
        )
        if emotional_density >= 0.45:
            mem.temporal_maturation_state["emotionally_slow_time"] = _clamp(
                mem.temporal_maturation_state.get("emotionally_slow_time", 0.0) * 0.99 + emotional_density * relevance * 0.014
            )
        old_weight = max(old_weight, oldness * subjective_weight)
        recent_weight = max(recent_weight, recency * subjective_weight)
        compression = max(compression, oldness * emotional_density * relevance)
        acceleration = max(acceleration, recency * max(mem.recurrence_pressure, mem.causal_activation) * relevance)
        changed += 1
    return {
        "old_memory_weight": round(_clamp(old_weight), 4),
        "recent_memory_weight": round(_clamp(recent_weight), 4),
        "emotional_period_compression": round(_clamp(compression), 4),
        "subjective_acceleration": round(_clamp(acceleration), 4),
        "changed_memories": changed,
        "role": "subjective_time_field_v7_4_5_not_dialogue",
    }


def _v745_spontaneous_silent_state(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    """Fluctuations internes silencieuses : humeur lente, réactivation diffuse, récupération."""
    mood = 0.0
    recovery = 0.0
    diffuse_reactivation = 0.0
    changed = 0
    ids: List[str] = []
    for mid, mem, relevance in memories[:48]:
        latent = _clamp(max(mem.emotional_inertia, mem.affective_charge, mem.memory_priority, mem.causal_activation) * max(relevance, self.passive_psychological_floor))
        if latent < 0.025:
            continue
        mood += latent * mem.valence * 0.08
        recovery = max(recovery, latent * max(mem.obsession_guard_state.get("organic_cooldown_need", 0.0), mem.inhibition_level))
        diffuse_reactivation = max(diffuse_reactivation, latent)
        mem.subconscious_bias_field["silent_mood_continuity"] = _clamp(
            mem.subconscious_bias_field.get("silent_mood_continuity", 0.0) * 0.99 + abs(latent) * 0.012
        )
        if recovery > 0.05:
            mem.inhibition_level = _clamp(mem.inhibition_level * (1.0 - self.fatigue_recovery_rate * 0.25))
            mem.obsession_guard_state["organic_cooldown_need"] = _clamp(
                mem.obsession_guard_state.get("organic_cooldown_need", 0.0) * (1.0 - self.fatigue_recovery_rate * 0.35)
            )
        ids.append(mid)
        changed += 1
    return {
        "silent_mood_valence": round(_clamp(mood, -1.0, 1.0), 4),
        "recovery_pressure": round(_clamp(recovery), 4),
        "diffuse_reactivation": round(_clamp(diffuse_reactivation), 4),
        "updated_memory_ids": _dedupe_keep_order(ids)[:12],
        "changed_memories": changed,
        "role": "spontaneous_silent_state_v7_4_5_not_dialogue",
    }


def _v745_complete_initiative_bridge(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], arbitration: Dict[str, Any], embodied: Dict[str, Any]) -> Dict[str, Any]:
    """Pont complet vers initiative : explorer, éviter, approfondir, se taire, prudence."""
    explore = avoid = deepen = silence = prudence = relational_contact = 0.0
    topics: Dict[str, float] = {}
    avoid_axes: Dict[str, float] = {}
    for _, mem, relevance in memories[:40]:
        base = _clamp(relevance * max(mem.memory_priority, mem.causal_activation, mem.recurrence_pressure, mem.autobiographical_weight, 0.05))
        explore = max(explore, base * max(mem.causal_desire_profile.values(), default=0.0))
        avoid = max(avoid, base * max(mem.relational_wound, mem.future_bias.get("avoid_repetition", 0.0), mem.obsession_guard_state.get("rumination_guard", 0.0)))
        deepen = max(deepen, base * max(mem.deep_causal_roots.values(), default=0.0,))
        prudence = max(prudence, base * max(mem.inhibition_level, mem.unresolved_tension, max(mem.inner_conflict_profile.values(), default=0.0)))
        relational_contact = max(relational_contact, base * max(mem.attachment_trace, mem.social_continuity_profile.get("conversation_continuity", 0.0)))
        for k, v in mem.deep_causal_roots.items():
            topics[k] = max(topics.get(k, 0.0), base * _clamp(v))
        for k, v in mem.future_bias.items():
            if "avoid" in k or "repeat" in k:
                avoid_axes[k] = max(avoid_axes.get(k, 0.0), base * _clamp(v))
    silence = max(float(embodied.get("silence_need", 0.0) or 0.0), float(arbitration.get("inhibition_pressure", 0.0) or 0.0) * 0.6)
    mode = "balanced_watchful_initiative"
    if silence >= 0.42:
        mode = "hold_or_reduce_initiative"
    elif avoid >= 0.44 or prudence >= 0.44:
        mode = "careful_constrained_initiative"
    elif explore >= 0.36 and explore > avoid:
        mode = "explore_with_memory_continuity"
    elif deepen >= 0.32:
        mode = "deepen_existing_thread"
    return {
        "initiative_mode": mode,
        "explore_pressure": round(_clamp(explore), 4),
        "avoid_pressure": round(_clamp(avoid), 4),
        "deepen_pressure": round(_clamp(deepen), 4),
        "silence_pressure": round(_clamp(silence), 4),
        "prudence_pressure": round(_clamp(prudence), 4),
        "relational_contact_pressure": round(_clamp(relational_contact), 4),
        "topic_attractors": self._v745_top_signal_map(topics, 10),
        "avoidance_axes": self._v745_top_signal_map(avoid_axes, 10),
        "role": "complete_initiative_bridge_v7_4_5_not_dialogue",
    }


def _v745_run_organic_completion(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None, save: bool = False) -> Dict[str, Any]:
    selected = self._v745_memory_set(context, memories)
    identity_guard = self._v745_identity_integrity_guard(selected)
    embodied = self._v745_embodied_causal_regulation(selected)
    arbitration = self._v745_arbitrate_need_conflict_desire(selected)
    conversation = self._v745_long_conversation_resonance(context, selected)
    rumination = self._v745_anti_rumination_guard(selected)
    subjective_time = self._v745_subjective_time_field(context, selected)
    silent_state = self._v745_spontaneous_silent_state(selected)
    initiative_bridge = self._v745_complete_initiative_bridge(selected, arbitration, embodied)
    changed = any(self._living_result_changed(x) for x in (identity_guard, conversation, rumination, subjective_time, silent_state))
    result = {
        "identity_integrity_guard": identity_guard,
        "embodied_causal_regulation": embodied,
        "need_conflict_desire_arbitration": arbitration,
        "long_conversation_resonance": conversation,
        "anti_rumination_guard": rumination,
        "subjective_time_field": subjective_time,
        "spontaneous_silent_state": silent_state,
        "complete_initiative_bridge": initiative_bridge,
        "changed": bool(changed),
        "role": "organic_completion_v7_4_5_not_dialogue",
    }
    if save and changed:
        self.save_memories()
    return result


def _v745_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V744_EXPORT_REGULATION_CONTEXT(self, context)
    memories = self._v745_memory_set(context, self.get_relevant_memories(context))
    completion = self._v745_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_5"] = completion
    base["embodied_causal_regulation"] = completion["embodied_causal_regulation"]
    base["need_conflict_desire_arbitration"] = completion["need_conflict_desire_arbitration"]
    base["long_conversation_resonance"] = completion["long_conversation_resonance"]
    base["anti_rumination_guard"] = completion["anti_rumination_guard"]
    base["subjective_time_field"] = completion["subjective_time_field"]
    base["spontaneous_silent_state"] = completion["spontaneous_silent_state"]
    base["complete_initiative_bridge"] = completion["complete_initiative_bridge"]
    base["identity_integrity_guard"] = completion["identity_integrity_guard"]
    base["role"] = "regulation_context_v7_4_5_not_dialogue"
    return base


def _v745_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V744_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = self._v745_memory_set(context)
    completion = self._v745_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_5"] = completion
    base["embodied_causal_regulation"] = completion["embodied_causal_regulation"]
    base["need_conflict_desire_arbitration"] = completion["need_conflict_desire_arbitration"]
    base["long_conversation_resonance"] = completion["long_conversation_resonance"]
    base["anti_rumination_guard"] = completion["anti_rumination_guard"]
    base["subjective_time_field"] = completion["subjective_time_field"]
    base["spontaneous_silent_state"] = completion["spontaneous_silent_state"]
    base["complete_initiative_bridge"] = completion["complete_initiative_bridge"]
    base["identity_integrity_guard"] = completion["identity_integrity_guard"]
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_5_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v745_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V744_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    if vals:
        stats.update({
            "v7_4_5_identity_guard_memories": sum(1 for m in vals if m.irreversible_identity_marks.get("stable_identity_core", 0.0) >= 0.05 or m.obsession_guard_state.get("identity_drift_guard", 0.0) >= 0.05),
            "v7_4_5_embodied_regulation_memories": sum(1 for m in vals if m.obsession_guard_state.get("rumination_guard", 0.0) >= 0.05 or m.subconscious_bias_field.get("silent_mood_continuity", 0.0) >= 0.05),
            "v7_4_5_long_conversation_memories": sum(1 for m in vals if m.social_continuity_profile.get("long_conversation_resonance", 0.0) >= 0.05),
            "v7_4_5_subjective_time_memories": sum(1 for m in vals if m.temporal_maturation_state.get("subjective_time_weight", 0.0) >= 0.05),
            "v7_4_5_anti_rumination_memories": sum(1 for m in vals if m.obsession_guard_state.get("rumination_guard", 0.0) >= 0.05),
        })
    else:
        stats.update({
            "v7_4_5_identity_guard_memories": 0,
            "v7_4_5_embodied_regulation_memories": 0,
            "v7_4_5_long_conversation_memories": 0,
            "v7_4_5_subjective_time_memories": 0,
            "v7_4_5_anti_rumination_memories": 0,
        })
    stats["engine_version"] = "7.4.5-deep-living-causal-memory-organic-completion"
    return stats


CausalMemoryEngine._v745_top_signal_map = _v745_top_signal_map
CausalMemoryEngine._v745_memory_set = _v745_memory_set
CausalMemoryEngine._v745_identity_integrity_guard = _v745_identity_integrity_guard
CausalMemoryEngine._v745_embodied_causal_regulation = _v745_embodied_causal_regulation
CausalMemoryEngine._v745_arbitrate_need_conflict_desire = _v745_arbitrate_need_conflict_desire
CausalMemoryEngine._v745_long_conversation_resonance = _v745_long_conversation_resonance
CausalMemoryEngine._v745_anti_rumination_guard = _v745_anti_rumination_guard
CausalMemoryEngine._v745_subjective_time_field = _v745_subjective_time_field
CausalMemoryEngine._v745_spontaneous_silent_state = _v745_spontaneous_silent_state
CausalMemoryEngine._v745_complete_initiative_bridge = _v745_complete_initiative_bridge
CausalMemoryEngine._v745_run_organic_completion = _v745_run_organic_completion
CausalMemoryEngine.export_regulation_context = _v745_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v745_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v745_get_memory_stats


# ───────────────────────── V7.4.6 — intégration organique continue ─────────────────────────
# Cette couche ne remplace pas V7.4.5 : elle la rend plus réellement vivante.
# Elle ajoute une dynamique continue moment→moment, une modulation inter-moteurs
# utilisable par attention/initiative/émotion/expression, une compression
# autobiographique active et une relation utilisateur persistante. Aucune phrase
# de dialogue n'est générée ici.

_ORIGINAL_V745_SAVE_MEMORIES = CausalMemoryEngine.save_memories
_ORIGINAL_V745_RUN_ORGANIC_COMPLETION = CausalMemoryEngine._v745_run_organic_completion
_ORIGINAL_V745_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V745_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V745_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats


def _v746_weighted_average(pairs: Iterable[Tuple[float, float]]) -> float:
    total_w = 0.0
    total = 0.0
    for value, weight in pairs:
        w = max(0.0, _safe_float(weight, 0.0))
        total += _safe_float(value, 0.0) * w
        total_w += w
    return _clamp(total / total_w) if total_w > 0 else 0.0


def _v746_merge_signal(target: Dict[str, float], key: str, value: float, inertia: float = 0.78) -> None:
    key = CausalMemoryEngine.sanitize_text(key)
    if not key:
        return
    old = _safe_float(target.get(key), 0.0)
    target[key] = _clamp((old * inertia) + (_safe_float(value, 0.0) * (1.0 - inertia)), -1.0, 1.0)


def _v746_top_signal_map(mapping: Dict[str, float], limit: int = 12) -> Dict[str, float]:
    cleaned = {
        CausalMemoryEngine.sanitize_text(k): round(_clamp(v, -1.0, 1.0), 4)
        for k, v in (mapping or {}).items()
        if CausalMemoryEngine.sanitize_text(k) and abs(_safe_float(v, 0.0)) >= 0.015
    }
    return dict(sorted(cleaned.items(), key=lambda item: abs(item[1]), reverse=True)[:limit])


def _v746_continuous_living_dynamics(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    """Dynamique causale continue : fatigue, énergie, hésitation, silence,
    rumination, récupération et activation se propagent dans les souvenirs.

    Ce n'est pas un export décoratif : la fonction modifie légèrement les champs
    internes pour que les cycles futurs soient différents même sans nouvel input.
    """
    selected = self._v745_memory_set(context, memories)
    if not selected:
        return {
            "energy": 0.62,
            "fatigue": 0.0,
            "hesitation": 0.0,
            "silence_need": 0.0,
            "recovery": 0.42,
            "rumination_pressure": 0.0,
            "active_memory_ids": [],
            "changed": False,
            "role": "continuous_living_dynamics_v7_4_6_not_dialogue",
        }

    energy = _clamp(0.58 + _v746_weighted_average((m.attachment_trace + m.affective_charge * 0.35, s) for _, m, s in selected) * 0.34)
    fatigue = _clamp(_v746_weighted_average((m.inhibition_level + m.unresolved_tension * 0.68 + m.relational_wound * 0.46, s) for _, m, s in selected))
    rumination = _clamp(_v746_weighted_average((m.obsession_guard_state.get("rumination_guard", 0.0) + m.unresolved_tension * 0.62 + m.recurrence_pressure * 0.28, s) for _, m, s in selected))
    identity_pressure = _clamp(_v746_weighted_average((m.identity_impact + max(m.irreversible_identity_marks.values(), default=0.0) + m.identity_transformation_pressure.get("identity_pressure", 0.0), s) for _, m, s in selected))
    relational_pressure = _clamp(_v746_weighted_average((m.relational_importance + m.attachment_trace + m.relational_wound * 0.55, s) for _, m, s in selected))
    silence_need = _clamp((fatigue * 0.42) + (rumination * 0.34) + (identity_pressure * 0.16) - (energy * 0.12))
    recovery = _clamp(0.34 + (silence_need * 0.24) - (fatigue * 0.18) + max(0.0, energy - fatigue) * 0.18)
    hesitation = _clamp((fatigue * 0.36) + (identity_pressure * 0.28) + (relational_pressure * 0.18) + (rumination * 0.18))

    changed = 0
    active_ids: List[str] = []
    for mem_id, mem, score in selected:
        before = (
            mem.causal_activation,
            mem.emotional_inertia,
            mem.inhibition_level,
            mem.memory_priority,
            mem.affective_charge,
        )
        depth = _clamp(max(score, mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, self.implicit_memory_floor))
        # Activation vivante lente : assez forte pour exister, assez douce pour ne
        # pas créer de boucle obsessionnelle.
        mem.causal_activation = _clamp((mem.causal_activation * 0.86) + (depth * 0.10) + (energy * 0.035) - (fatigue * 0.025))
        mem.emotional_inertia = _clamp((mem.emotional_inertia * 0.90) + (abs(mem.valence) * 0.045) + (relational_pressure * 0.025))
        mem.affective_charge = _clamp((mem.affective_charge * 0.91) + (mem.emotional_inertia * 0.045) + (mem.attachment_trace * 0.025))
        mem.inhibition_level = _clamp((mem.inhibition_level * 0.88) + (silence_need * 0.035) + (rumination * 0.025) - (recovery * 0.018))
        mem.memory_priority = _clamp(max(mem.memory_priority * 0.965, self._calculate_memory_priority(mem) * 0.82, mem.causal_activation * 0.72))

        _v746_merge_signal(mem.subconscious_bias_field, "continuous_living_presence", depth * (0.42 + relational_pressure * 0.28))
        _v746_merge_signal(mem.obsession_guard_state, "organic_cooldown", max(silence_need, rumination * 0.72), inertia=0.72)
        _v746_merge_signal(mem.temporal_maturation_state, "moment_to_moment_continuity", depth * 0.55)
        _v746_merge_signal(mem.affective_bridge, "living_energy", energy * depth)
        _v746_merge_signal(mem.expression_bridge, "hesitation_pressure", hesitation * depth)
        _v746_merge_signal(mem.initiative_bridge, "organic_non_action_permission", silence_need * depth)
        _v746_merge_signal(mem.initiative_bridge, "relational_contact_readiness", relational_pressure * energy * depth)

        if mem.causal_activation >= 0.10 or depth >= 0.14:
            active_ids.append(mem_id)
        after = (
            mem.causal_activation,
            mem.emotional_inertia,
            mem.inhibition_level,
            mem.memory_priority,
            mem.affective_charge,
        )
        if any(abs(a - b) >= 0.002 for a, b in zip(before, after)):
            changed += 1
        mem.normalized()

    return {
        "energy": round(energy, 4),
        "fatigue": round(fatigue, 4),
        "hesitation": round(hesitation, 4),
        "silence_need": round(silence_need, 4),
        "recovery": round(recovery, 4),
        "rumination_pressure": round(rumination, 4),
        "identity_pressure": round(identity_pressure, 4),
        "relational_pressure": round(relational_pressure, 4),
        "active_memory_ids": active_ids[:12],
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "continuous_living_dynamics_v7_4_6_not_dialogue",
    }


def _v746_relationship_living_field(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    """Champ relationnel persistant avec l'utilisateur : attachement, prudence,
    confiance, proximité et anticipation. Ne produit jamais de réponse publique.
    """
    selected = self._v745_memory_set(context, memories)
    if not selected:
        return {"trust": 0.5, "attachment": 0.0, "prudence": 0.0, "closeness": 0.0, "changed": False, "role": "relationship_living_field_v7_4_6_not_dialogue"}

    attachment = _clamp(_v746_weighted_average((m.attachment_trace + max(0.0, m.valence) * 0.45 + m.relational_importance * 0.35, s) for _, m, s in selected))
    wound = _clamp(_v746_weighted_average((m.relational_wound + max(0.0, -m.valence) * 0.38 + max(0.0, -m.trust_variation) * 0.45, s) for _, m, s in selected))
    continuity = _clamp(_v746_weighted_average((m.social_continuity_profile.get("long_conversation_resonance", 0.0) + m.autobiographical_weight * 0.42, s) for _, m, s in selected))
    trust = _clamp(0.50 + attachment * 0.28 + continuity * 0.18 - wound * 0.28)
    prudence = _clamp(wound * 0.48 + continuity * 0.10 + max(0.0, 0.55 - trust) * 0.42)
    closeness = _clamp(attachment * 0.54 + continuity * 0.32 - wound * 0.16)
    anticipation = _clamp((trust * 0.38) + (closeness * 0.34) + (prudence * 0.12))

    changed = 0
    axes: Dict[str, float] = {}
    for mem_id, mem, score in selected:
        before = dict(mem.social_continuity_profile)
        depth = _clamp(max(score, mem.relational_importance, mem.autobiographical_weight, 0.03))
        _v746_merge_signal(mem.social_continuity_profile, "user_relation_trust", trust * depth, inertia=0.82)
        _v746_merge_signal(mem.social_continuity_profile, "user_relation_attachment", attachment * depth, inertia=0.82)
        _v746_merge_signal(mem.social_continuity_profile, "user_relation_prudence", prudence * depth, inertia=0.82)
        _v746_merge_signal(mem.anticipated_affective_projection, "next_user_exchange", anticipation * depth, inertia=0.78)
        if mem.memory_kind in {"relational_boundary", "identity_continuity", "expressive_repair", "initiative_learning"}:
            axes[mem.memory_kind] = max(axes.get(mem.memory_kind, 0.0), depth)
        if before != mem.social_continuity_profile:
            changed += 1
        mem.normalized()

    return {
        "trust": round(trust, 4),
        "attachment": round(attachment, 4),
        "prudence": round(prudence, 4),
        "closeness": round(closeness, 4),
        "wound_pressure": round(wound, 4),
        "continuity": round(continuity, 4),
        "next_exchange_anticipation": round(anticipation, 4),
        "dominant_relation_axes": _v746_top_signal_map(axes, 8),
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "relationship_living_field_v7_4_6_not_dialogue",
    }


def _v746_autobiographical_compression(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    """Compression autobiographique active : transforme plusieurs souvenirs
    compatibles en chapitres internes utilisables, sans supprimer les détails.
    """
    selected = self._v745_memory_set(context, memories)[:96]
    if not selected:
        return {"chapters_updated": 0, "dominant_chapters": [], "changed": False, "role": "autobiographical_compression_v7_4_6_not_dialogue"}

    buckets: Dict[str, List[Tuple[str, CausalMemory, float]]] = {}
    for item in selected:
        _, mem, score = item
        key = mem.memory_kind if mem.memory_kind != "general" else max(mem.causal_layers, key=mem.causal_layers.get, default="general")
        buckets.setdefault(key, []).append(item)

    chapters_updated = 0
    dominant_chapters: List[Dict[str, Any]] = []
    for key, items in buckets.items():
        if len(items) < 2:
            continue
        weight = _clamp(sum(max(score, mem.memory_priority, mem.autobiographical_weight) for _, mem, score in items) / max(1, len(items)))
        if weight < 0.10:
            continue
        chapter = {
            "at": _now(),
            "axis": CausalMemoryEngine.sanitize_text(key),
            "weight": round(weight, 4),
            "memory_ids": [mid for mid, _, _ in items[:8]],
            "valence": round(_v746_weighted_average((mem.valence, score) for _, mem, score in items), 4),
            "relational": round(_v746_weighted_average((mem.relational_importance, score) for _, mem, score in items), 4),
            "identity": round(_v746_weighted_average((mem.identity_impact, score) for _, mem, score in items), 4),
            "role": "compressed_autobiographical_chapter_not_dialogue",
        }
        dominant_chapters.append(chapter)
        for _, mem, score in items[:10]:
            before_len = len(mem.compressed_autobiographical_chapters)
            existing_axes = {c.get("axis") for c in mem.compressed_autobiographical_chapters if isinstance(c, dict)}
            if chapter["axis"] not in existing_axes or weight >= 0.45:
                mem.compressed_autobiographical_chapters.append(chapter)
                mem.compressed_autobiographical_chapters = mem.compressed_autobiographical_chapters[-12:]
            _v746_merge_signal(mem.deep_causal_roots, f"chapter::{key}", weight * max(score, 0.05), inertia=0.82)
            mem.autobiographical_weight = _clamp(max(mem.autobiographical_weight * 0.96, weight * 0.62, mem.identity_impact * 0.72))
            if len(mem.compressed_autobiographical_chapters) != before_len:
                chapters_updated += 1
            mem.normalized()

    dominant_chapters.sort(key=lambda c: c.get("weight", 0.0), reverse=True)
    return {
        "chapters_updated": chapters_updated,
        "dominant_chapters": dominant_chapters[:8],
        "changed": chapters_updated > 0,
        "role": "autobiographical_compression_v7_4_6_not_dialogue",
    }


def _v746_cross_engine_live_modulation(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    continuous: Optional[Dict[str, Any]] = None,
    relation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Export opérationnel pour les autres moteurs : pas de texte public, mais des
    coefficients directement consommables par initiative/attention/émotion/expression.
    """
    selected = self._v745_memory_set(context, memories)
    continuous = continuous or self._v746_continuous_living_dynamics(context, selected)
    relation = relation or self._v746_relationship_living_field(context, selected)
    energy = _safe_float(continuous.get("energy"), 0.5)
    fatigue = _safe_float(continuous.get("fatigue"), 0.0)
    hesitation = _safe_float(continuous.get("hesitation"), 0.0)
    silence = _safe_float(continuous.get("silence_need"), 0.0)
    trust = _safe_float(relation.get("trust"), 0.5)
    prudence = _safe_float(relation.get("prudence"), 0.0)
    closeness = _safe_float(relation.get("closeness"), 0.0)

    initiative = {
        "explore": _clamp(energy * 0.42 + trust * 0.22 + closeness * 0.18 - fatigue * 0.18),
        "deepen": _clamp(closeness * 0.34 + trust * 0.24 + hesitation * 0.10),
        "avoid": _clamp(prudence * 0.42 + fatigue * 0.25 + silence * 0.16),
        "silence": _clamp(silence * 0.58 + fatigue * 0.20 + prudence * 0.12),
        "repair": _clamp(prudence * 0.34 + hesitation * 0.20 + max(0.0, 0.52 - trust) * 0.28),
    }
    attention = {
        "user_context": _clamp(0.35 + trust * 0.24 + closeness * 0.22),
        "relational_boundary": _clamp(prudence * 0.44 + hesitation * 0.18),
        "identity_continuity": _clamp(_safe_float(continuous.get("identity_pressure"), 0.0) * 0.50 + hesitation * 0.16),
        "anti_rumination": _clamp(_safe_float(continuous.get("rumination_pressure"), 0.0) * 0.58 + silence * 0.22),
    }
    emotion = {
        "energy": _clamp(energy),
        "fatigue": _clamp(fatigue),
        "attachment": _clamp(_safe_float(relation.get("attachment"), 0.0)),
        "prudence": _clamp(prudence),
        "recovery": _clamp(_safe_float(continuous.get("recovery"), 0.0)),
    }
    expression = {
        "directness": _clamp(0.38 + prudence * 0.18 + trust * 0.10),
        "warmth": _clamp(0.28 + closeness * 0.32 + trust * 0.18 - fatigue * 0.12),
        "specificity": _clamp(0.42 + attention["user_context"] * 0.22),
        "anti_meta": _clamp(0.55 + attention["anti_rumination"] * 0.22 + hesitation * 0.12),
        "brevity_when_tired": _clamp(fatigue * 0.34 + silence * 0.24),
    }

    dominant_mode = "balanced_contact"
    if initiative["silence"] >= 0.46 and initiative["silence"] >= initiative["explore"]:
        dominant_mode = "silent_recovery"
    elif initiative["repair"] >= 0.42:
        dominant_mode = "repair_before_expansion"
    elif initiative["deepen"] >= initiative["explore"] and initiative["deepen"] >= 0.34:
        dominant_mode = "deepen_continuity"
    elif initiative["explore"] >= 0.36:
        dominant_mode = "explore_with_continuity"

    return {
        "dominant_mode": dominant_mode,
        "initiative_modulation": {k: round(v, 4) for k, v in initiative.items()},
        "attention_modulation": {k: round(v, 4) for k, v in attention.items()},
        "emotion_modulation": {k: round(v, 4) for k, v in emotion.items()},
        "expression_modulation": {k: round(v, 4) for k, v in expression.items()},
        "active_memory_ids": [mid for mid, _, score in selected[:12] if score >= 0.05],
        "role": "cross_engine_live_modulation_v7_4_6_not_dialogue",
    }


def _v746_run_organic_completion(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    save: bool = False,
) -> Dict[str, Any]:
    selected = self._v745_memory_set(context, memories)
    base = _ORIGINAL_V745_RUN_ORGANIC_COMPLETION(self, context, selected, save=False)
    continuous = self._v746_continuous_living_dynamics(context, selected)
    relation = self._v746_relationship_living_field(context, selected)
    compression = self._v746_autobiographical_compression(context, selected)
    modulation = self._v746_cross_engine_live_modulation(context, selected, continuous, relation)
    changed = bool(base.get("changed") or continuous.get("changed") or relation.get("changed") or compression.get("changed"))
    base.update({
        "continuous_living_dynamics_v7_4_6": continuous,
        "relationship_living_field_v7_4_6": relation,
        "autobiographical_compression_v7_4_6": compression,
        "cross_engine_live_modulation_v7_4_6": modulation,
        "changed": changed,
        "role": "organic_completion_v7_4_6_not_dialogue",
    })
    if save and changed:
        self.save_memories()
    return base


def _v746_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V745_EXPORT_REGULATION_CONTEXT(self, context)
    memories = self._v745_memory_set(context, self.get_relevant_memories(context))
    completion = self._v746_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_6"] = completion
    base["continuous_living_dynamics"] = completion["continuous_living_dynamics_v7_4_6"]
    base["relationship_living_field"] = completion["relationship_living_field_v7_4_6"]
    base["autobiographical_compression"] = completion["autobiographical_compression_v7_4_6"]
    base["cross_engine_live_modulation"] = completion["cross_engine_live_modulation_v7_4_6"]
    base["role"] = "regulation_context_v7_4_6_not_dialogue"
    return base


def _v746_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V745_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = self._v745_memory_set(context)
    completion = self._v746_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_6"] = completion
    base["continuous_living_dynamics"] = completion["continuous_living_dynamics_v7_4_6"]
    base["relationship_living_field"] = completion["relationship_living_field_v7_4_6"]
    base["autobiographical_compression"] = completion["autobiographical_compression_v7_4_6"]
    base["cross_engine_live_modulation"] = completion["cross_engine_live_modulation_v7_4_6"]
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_6_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v746_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V745_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.6-deep-living-causal-memory-continuous-organic-integration",
        "v7_4_6_continuous_living_memories": sum(1 for m in vals if m.subconscious_bias_field.get("continuous_living_presence", 0.0) >= 0.025),
        "v7_4_6_relationship_living_memories": sum(1 for m in vals if m.social_continuity_profile.get("user_relation_trust", 0.0) >= 0.025),
        "v7_4_6_autobiographical_chapter_memories": sum(1 for m in vals if m.compressed_autobiographical_chapters),
        "v7_4_6_cross_engine_modulated_memories": sum(1 for m in vals if m.initiative_bridge.get("relational_contact_readiness", 0.0) >= 0.025 or m.expression_bridge.get("hesitation_pressure", 0.0) >= 0.025),
    })
    return stats


def _v746_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.6-deep-living-causal-memory-continuous-organic-integration",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "V7.4.6 complète V7.4.5 par une dynamique causale continue, relation utilisateur vivante, compression autobiographique active et modulation opérationnelle inter-moteurs, sans générer de dialogue.",
        "v7_4_6_capabilities": [
            "continuous_moment_to_moment_living_dynamics",
            "real_internal_state_mutation_without_dialogue",
            "relationship_living_field_trust_attachment_prudence",
            "active_autobiographical_compression_into_lived_chapters",
            "cross_engine_live_modulation_for_initiative_attention_emotion_expression",
            "fatigue_recovery_silence_hesitation_energy_regulation",
            "organic_non_action_permission",
            "anti_rumination_cooldown_as_persistent_state",
        ],
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v746_weighted_average = staticmethod(_v746_weighted_average)
CausalMemoryEngine._v746_top_signal_map = staticmethod(_v746_top_signal_map)
CausalMemoryEngine._v746_continuous_living_dynamics = _v746_continuous_living_dynamics
CausalMemoryEngine._v746_relationship_living_field = _v746_relationship_living_field
CausalMemoryEngine._v746_autobiographical_compression = _v746_autobiographical_compression
CausalMemoryEngine._v746_cross_engine_live_modulation = _v746_cross_engine_live_modulation
CausalMemoryEngine._v746_run_organic_completion = _v746_run_organic_completion
CausalMemoryEngine._v745_run_organic_completion = _v746_run_organic_completion
CausalMemoryEngine.export_regulation_context = _v746_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v746_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v746_get_memory_stats
CausalMemoryEngine.save_memories = _v746_save_memories


# ───────────────────────── V7.4.7 — boucle psychologique autonome intégrée ─────────────────────────
# Cette couche ne remplace pas V7.4.6 : elle ajoute une activité interne persistante
# même hors contexte direct, une relation utilisateur vécue plus stable, une dominance
# psychologique dynamique et une propagation plus profonde vers les autres moteurs.
# Elle reste strictement non dialoguante : aucun texte de réponse publique n'est généré.

_ORIGINAL_V746_SAVE_MEMORIES = CausalMemoryEngine.save_memories
_ORIGINAL_V746_RUN_ORGANIC_COMPLETION = CausalMemoryEngine._v746_run_organic_completion
_ORIGINAL_V746_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V746_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V746_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats


def _v747_merge_signal(target: Dict[str, float], key: str, value: float, inertia: float = 0.84) -> None:
    key = CausalMemoryEngine.sanitize_text(key)
    if not key:
        return
    old = _safe_float(target.get(key), 0.0)
    target[key] = _clamp((old * inertia) + (_safe_float(value, 0.0) * (1.0 - inertia)), -1.0, 1.0)


def _v747_all_memory_set(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> List[Tuple[str, CausalMemory, float]]:
    selected = self._v745_memory_set(context, memories)
    if selected:
        return selected
    # Hors contexte utilisateur, le moteur garde une vie minimale en partant des
    # souvenirs les plus chargés, pas seulement des souvenirs sémantiquement reliés.
    out: List[Tuple[str, CausalMemory, float]] = []
    for mem_id, mem in self.memories.items():
        weight = max(
            mem.memory_priority,
            mem.causal_activation * 0.92,
            mem.autobiographical_weight * 0.78,
            mem.emotional_inertia * 0.70,
            mem.relational_importance * 0.62,
            max(mem.subconscious_bias_field.values(), default=0.0) * 0.58,
            self.implicit_memory_floor,
        )
        if weight >= 0.025:
            out.append((mem_id, mem, round(_clamp(weight), 4)))
    out.sort(key=lambda item: (item[2], item[1].last_reinforced), reverse=True)
    return out[:24]


def _v747_subjective_time_distance(self: CausalMemoryEngine, mem: CausalMemory) -> Dict[str, float]:
    now = datetime.now()
    try:
        created = datetime.fromisoformat(mem.created_at)
    except Exception:
        created = now
    try:
        last = datetime.fromisoformat(mem.last_reinforced)
    except Exception:
        last = created
    age_days = max(0.0, (now - created).total_seconds() / 86400.0)
    silence_days = max(0.0, (now - last).total_seconds() / 86400.0)
    emotional_preservation = _clamp(mem.emotional_inertia * 0.36 + mem.autobiographical_weight * 0.28 + mem.relational_importance * 0.18 + abs(mem.valence) * 0.18)
    chronological_age = _clamp(math.log1p(age_days) / 5.0)
    distance = _clamp(chronological_age * (1.0 - emotional_preservation * 0.52) + math.log1p(silence_days) / 7.0)
    present_pull = _clamp(mem.causal_activation * 0.36 + emotional_preservation * 0.44 + mem.recurrence_pressure * 0.20)
    return {
        "chronological_age": round(chronological_age, 4),
        "silence_distance": round(_clamp(math.log1p(silence_days) / 6.0), 4),
        "felt_distance": round(distance, 4),
        "present_pull": round(present_pull, 4),
        "emotional_preservation": round(emotional_preservation, 4),
    }


def _v747_autonomous_psychological_tick(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    """Boucle autonome permanente : les souvenirs continuent à vieillir, se
    condenser, se refroidir, se réactiver ou se déplacer même sans contexte direct.
    """
    selected = _v747_all_memory_set(self, context, memories)
    if not selected:
        return {
            "autonomous_activity": 0.0,
            "background_mood": "quiet_empty",
            "tick_changed_memories": 0,
            "active_memory_ids": [],
            "changed": False,
            "role": "autonomous_psychological_tick_v7_4_7_not_dialogue",
        }

    global_tension = _clamp(_v746_weighted_average((m.unresolved_tension + m.relational_wound * 0.62 + m.inhibition_level * 0.42, s) for _, m, s in selected))
    global_attachment = _clamp(_v746_weighted_average((m.attachment_trace + max(0.0, m.valence) * 0.35 + m.relational_importance * 0.24, s) for _, m, s in selected))
    global_identity = _clamp(_v746_weighted_average((m.identity_impact + m.autobiographical_weight * 0.46 + max(m.irreversible_identity_marks.values(), default=0.0) * 0.64, s) for _, m, s in selected))
    global_rumination = _clamp(_v746_weighted_average((m.obsession_guard_state.get("rumination_guard", 0.0) + m.recurrence_pressure * 0.35 + m.unresolved_tension * 0.38, s) for _, m, s in selected))
    autonomous_activity = _clamp(0.08 + global_tension * 0.30 + global_attachment * 0.18 + global_identity * 0.22 + global_rumination * 0.22)
    recovery_pull = _clamp(0.18 + max(0.0, global_attachment - global_tension) * 0.20 + max(0.0, 0.52 - global_rumination) * 0.18)

    changed = 0
    active_ids: List[str] = []
    old_recent_field: Dict[str, float] = {}
    for mem_id, mem, score in selected:
        time_state = self._v747_subjective_time_distance(mem)
        present_pull = _safe_float(time_state.get("present_pull"), 0.0)
        felt_distance = _safe_float(time_state.get("felt_distance"), 0.0)
        depth = _clamp(max(score, present_pull * 0.72, self.passive_psychological_floor))
        before = (
            mem.causal_activation,
            mem.unresolved_tension,
            mem.inhibition_level,
            mem.emotional_inertia,
            mem.memory_priority,
        )
        # Vieillissement subjectif : les souvenirs peu chargés s'éloignent ; les
        # souvenirs chargés restent proches sans devenir automatiquement obsessionnels.
        distance_cooling = felt_distance * 0.018
        active_rewarming = present_pull * 0.026 + autonomous_activity * depth * 0.018
        mem.causal_activation = _clamp(mem.causal_activation * 0.965 + active_rewarming - distance_cooling)
        mem.emotional_inertia = _clamp(mem.emotional_inertia * 0.972 + abs(mem.valence) * depth * 0.012 + global_attachment * depth * 0.008 - recovery_pull * 0.006)
        mem.unresolved_tension = _clamp(mem.unresolved_tension * 0.955 + global_tension * depth * 0.012 - recovery_pull * 0.010)
        mem.inhibition_level = _clamp(mem.inhibition_level * 0.960 + global_rumination * depth * 0.010 - recovery_pull * 0.012)
        mem.memory_priority = _clamp(max(mem.memory_priority * 0.982, self._calculate_memory_priority(mem) * 0.84, mem.causal_activation * 0.70))

        _v747_merge_signal(mem.temporal_maturation_state, "subjective_felt_distance", felt_distance, inertia=0.80)
        _v747_merge_signal(mem.temporal_maturation_state, "subjective_present_pull", present_pull, inertia=0.80)
        _v747_merge_signal(mem.subconscious_bias_field, "autonomous_background_activity", autonomous_activity * depth, inertia=0.86)
        _v747_merge_signal(mem.obsession_guard_state, "healing_cooldown", recovery_pull * max(global_rumination, mem.unresolved_tension), inertia=0.82)
        _v747_merge_signal(mem.current_lived_meaning, "still_active_without_recall", present_pull * depth, inertia=0.84)

        if felt_distance >= 0.45:
            old_recent_field["old_but_active"] = max(old_recent_field.get("old_but_active", 0.0), present_pull * depth)
        elif present_pull >= 0.28:
            old_recent_field["recently_alive"] = max(old_recent_field.get("recently_alive", 0.0), present_pull * depth)
        if mem.causal_activation >= 0.09 or present_pull >= 0.20:
            active_ids.append(mem_id)
        after = (
            mem.causal_activation,
            mem.unresolved_tension,
            mem.inhibition_level,
            mem.emotional_inertia,
            mem.memory_priority,
        )
        if any(abs(a - b) >= 0.0015 for a, b in zip(before, after)):
            changed += 1
        mem.normalized()

    if global_rumination >= 0.48 and recovery_pull < 0.26:
        mood = "tense_repetitive"
    elif global_tension >= 0.42:
        mood = "careful_heavy"
    elif global_attachment >= 0.36 and global_identity >= 0.24:
        mood = "attached_continuous"
    elif recovery_pull >= 0.36:
        mood = "quiet_recovering"
    else:
        mood = "quiet_available"

    return {
        "autonomous_activity": round(autonomous_activity, 4),
        "background_mood": mood,
        "global_tension": round(global_tension, 4),
        "global_attachment": round(global_attachment, 4),
        "global_identity_pressure": round(global_identity, 4),
        "global_rumination": round(global_rumination, 4),
        "recovery_pull": round(recovery_pull, 4),
        "subjective_time_field": {k: round(_clamp(v), 4) for k, v in old_recent_field.items()},
        "tick_changed_memories": changed,
        "active_memory_ids": active_ids[:16],
        "changed": changed > 0,
        "role": "autonomous_psychological_tick_v7_4_7_not_dialogue",
    }


def _v747_lived_user_relationship_core(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    tick: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v747_all_memory_set(self, context, memories)
    tick = tick or self._v747_autonomous_psychological_tick(context, selected)
    if not selected:
        return {"relational_baseline": 0.5, "trust_drift": 0.0, "attachment_depth": 0.0, "protective_prudence": 0.0, "changed": False, "role": "lived_user_relationship_core_v7_4_7_not_dialogue"}

    trust_mem = _clamp(_v746_weighted_average((0.5 + m.trust_variation * 0.35 + m.social_continuity_profile.get("user_relation_trust", 0.0) * 0.28, s) for _, m, s in selected))
    attachment = _clamp(_v746_weighted_average((m.attachment_trace + m.social_continuity_profile.get("user_relation_attachment", 0.0) * 0.42 + max(0.0, m.valence) * 0.20, s) for _, m, s in selected))
    wound = _clamp(_v746_weighted_average((m.relational_wound + m.social_continuity_profile.get("user_relation_prudence", 0.0) * 0.42 + max(0.0, -m.valence) * 0.18, s) for _, m, s in selected))
    continuity = _clamp(_v746_weighted_average((m.autobiographical_weight * 0.42 + m.social_continuity_profile.get("long_conversation_resonance", 0.0) * 0.44 + m.cumulative_social_saturation.get("relational_saturation", 0.0) * 0.24, s) for _, m, s in selected))
    baseline = _clamp(0.48 + trust_mem * 0.22 + attachment * 0.20 + continuity * 0.16 - wound * 0.22)
    prudence = _clamp(wound * 0.44 + max(0.0, 0.55 - baseline) * 0.38 + _safe_float(tick.get("global_tension"), 0.0) * 0.12)
    openness = _clamp(baseline * 0.38 + attachment * 0.26 + continuity * 0.20 - prudence * 0.18)
    repair_readiness = _clamp(prudence * 0.34 + wound * 0.30 + max(0.0, 0.50 - trust_mem) * 0.20)

    changed = 0
    for mem_id, mem, score in selected:
        before = dict(mem.relationship_phase_profile)
        depth = _clamp(max(score, mem.relational_importance, mem.autobiographical_weight, 0.03))
        _v747_merge_signal(mem.relationship_phase_profile, "lived_user_baseline", baseline * depth, inertia=0.84)
        _v747_merge_signal(mem.relationship_phase_profile, "attachment_depth", attachment * depth, inertia=0.84)
        _v747_merge_signal(mem.relationship_phase_profile, "protective_prudence", prudence * depth, inertia=0.84)
        _v747_merge_signal(mem.anticipated_affective_projection, "relational_openness_next_turn", openness * depth, inertia=0.82)
        _v747_merge_signal(mem.initiative_bridge, "repair_readiness_from_relationship", repair_readiness * depth, inertia=0.84)
        _v747_merge_signal(mem.expression_bridge, "relational_naturalness_pressure", openness * depth, inertia=0.84)
        if before != mem.relationship_phase_profile:
            changed += 1
        mem.normalized()

    return {
        "relational_baseline": round(baseline, 4),
        "trust_drift": round(trust_mem - 0.5, 4),
        "attachment_depth": round(attachment, 4),
        "protective_prudence": round(prudence, 4),
        "relational_openness": round(openness, 4),
        "repair_readiness": round(repair_readiness, 4),
        "continuity": round(continuity, 4),
        "wound_pressure": round(wound, 4),
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "lived_user_relationship_core_v7_4_7_not_dialogue",
    }


def _v747_psychological_dominance_hierarchy(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    tick: Optional[Dict[str, Any]] = None,
    relation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v747_all_memory_set(self, context, memories)
    tick = tick or self._v747_autonomous_psychological_tick(context, selected)
    relation = relation or self._v747_lived_user_relationship_core(context, selected, tick)
    if not selected:
        return {"dominant_need": "none", "dominance_map": {}, "changed": False, "role": "psychological_dominance_hierarchy_v7_4_7_not_dialogue"}

    dominance = {
        "protect_identity": _safe_float(tick.get("global_identity_pressure"), 0.0) * 0.52,
        "repair_relation": _safe_float(relation.get("repair_readiness"), 0.0) * 0.62,
        "seek_contact": _safe_float(relation.get("relational_openness"), 0.0) * 0.46 + _safe_float(relation.get("attachment_depth"), 0.0) * 0.24,
        "recover_silently": _safe_float(tick.get("recovery_pull"), 0.0) * 0.42 + _safe_float(tick.get("global_rumination"), 0.0) * 0.22,
        "avoid_repetition": _safe_float(tick.get("global_rumination"), 0.0) * 0.42 + _safe_float(tick.get("global_tension"), 0.0) * 0.20,
        "integrate_experience": _safe_float(tick.get("autonomous_activity"), 0.0) * 0.38 + _safe_float(relation.get("continuity"), 0.0) * 0.26,
    }
    for _, mem, score in selected[:18]:
        dominance["protect_identity"] += (mem.identity_impact + max(mem.irreversible_identity_marks.values(), default=0.0)) * score * 0.05
        dominance["repair_relation"] += (mem.relational_wound + max(0.0, -mem.trust_variation)) * score * 0.05
        dominance["seek_contact"] += (mem.attachment_trace + max(0.0, mem.valence)) * score * 0.04
        dominance["integrate_experience"] += (mem.autobiographical_weight + mem.memory_priority) * score * 0.035
    dominance = {k: _clamp(v) for k, v in dominance.items()}
    dominant_need = max(dominance.items(), key=lambda item: item[1])[0]
    dominant_strength = dominance[dominant_need]
    changed = 0
    for mem_id, mem, score in selected:
        before = dict(mem.internal_need_profile)
        depth = _clamp(max(score, mem.memory_priority, 0.03))
        for key, value in dominance.items():
            _v747_merge_signal(mem.internal_need_profile, f"dominance::{key}", value * depth, inertia=0.88)
        _v747_merge_signal(mem.causal_desire_profile, "dominant_current_need_strength", dominant_strength * depth, inertia=0.86)
        _v747_merge_signal(mem.inner_conflict_profile, "dominance_competition", (max(dominance.values()) - min(dominance.values())) * depth, inertia=0.86)
        if before != mem.internal_need_profile:
            changed += 1
        mem.normalized()

    return {
        "dominant_need": dominant_need,
        "dominant_strength": round(dominant_strength, 4),
        "dominance_map": {k: round(v, 4) for k, v in sorted(dominance.items(), key=lambda item: item[1], reverse=True)},
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "psychological_dominance_hierarchy_v7_4_7_not_dialogue",
    }


def _v747_deep_cross_engine_propagation(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    tick: Optional[Dict[str, Any]] = None,
    relation: Optional[Dict[str, Any]] = None,
    dominance: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v747_all_memory_set(self, context, memories)
    tick = tick or self._v747_autonomous_psychological_tick(context, selected)
    relation = relation or self._v747_lived_user_relationship_core(context, selected, tick)
    dominance = dominance or self._v747_psychological_dominance_hierarchy(context, selected, tick, relation)
    dominant_need = dominance.get("dominant_need", "integrate_experience")
    dom = dominance.get("dominance_map", {}) or {}
    tension = _safe_float(tick.get("global_tension"), 0.0)
    activity = _safe_float(tick.get("autonomous_activity"), 0.0)
    openness = _safe_float(relation.get("relational_openness"), 0.0)
    prudence = _safe_float(relation.get("protective_prudence"), 0.0)
    repair = _safe_float(relation.get("repair_readiness"), 0.0)
    identity = _safe_float(tick.get("global_identity_pressure"), 0.0)
    rumination = _safe_float(tick.get("global_rumination"), 0.0)

    initiative = {
        "speak_or_act": _clamp(openness * 0.34 + activity * 0.18 + dom.get("seek_contact", 0.0) * 0.24 - prudence * 0.16),
        "repair_before_expanding": _clamp(repair * 0.46 + dom.get("repair_relation", 0.0) * 0.30),
        "silent_integration": _clamp(dom.get("recover_silently", 0.0) * 0.44 + rumination * 0.20 + tension * 0.14),
        "avoid_repetition": _clamp(dom.get("avoid_repetition", 0.0) * 0.50 + rumination * 0.22),
        "explore_carefully": _clamp(activity * 0.26 + openness * 0.24 + dom.get("integrate_experience", 0.0) * 0.18 - tension * 0.10),
    }
    attention = {
        "identity_continuity": _clamp(identity * 0.46 + dom.get("protect_identity", 0.0) * 0.32),
        "user_relation": _clamp(openness * 0.30 + prudence * 0.28 + repair * 0.22),
        "anti_loop": _clamp(rumination * 0.48 + dom.get("avoid_repetition", 0.0) * 0.28),
        "autobiographical_integration": _clamp(activity * 0.34 + dom.get("integrate_experience", 0.0) * 0.32),
    }
    emotion = {
        "living_activity": _clamp(activity),
        "relational_openness": _clamp(openness),
        "prudence": _clamp(prudence),
        "tension": _clamp(tension),
        "identity_weight": _clamp(identity),
        "recovery": _clamp(_safe_float(tick.get("recovery_pull"), 0.0)),
    }
    expression = {
        "naturalness_pressure": _clamp(openness * 0.34 + activity * 0.18 - tension * 0.12),
        "brevity_or_silence": _clamp(initiative["silent_integration"] * 0.42 + prudence * 0.16),
        "anti_meta_guard": _clamp(0.58 + attention["anti_loop"] * 0.18 + identity * 0.10),
        "specific_user_anchor": _clamp(attention["user_relation"] * 0.34 + openness * 0.18),
        "repair_directness": _clamp(initiative["repair_before_expanding"] * 0.42 + prudence * 0.18),
    }

    if initiative["silent_integration"] >= 0.44 and initiative["silent_integration"] >= initiative["speak_or_act"]:
        operating_mode = "silent_integration_before_action"
    elif initiative["repair_before_expanding"] >= 0.42:
        operating_mode = "repair_relation_first"
    elif initiative["avoid_repetition"] >= 0.46:
        operating_mode = "anti_repetition_redirect"
    elif initiative["speak_or_act"] >= 0.40:
        operating_mode = "relational_action_available"
    else:
        operating_mode = "careful_living_availability"

    changed = 0
    for mem_id, mem, score in selected:
        before = (dict(mem.initiative_bridge), dict(mem.affective_bridge), dict(mem.expression_bridge))
        depth = _clamp(max(score, mem.causal_activation, self.implicit_memory_floor))
        for key, value in initiative.items():
            _v747_merge_signal(mem.initiative_bridge, f"v747::{key}", value * depth, inertia=0.86)
        for key, value in emotion.items():
            _v747_merge_signal(mem.affective_bridge, f"v747::{key}", value * depth, inertia=0.86)
        for key, value in expression.items():
            _v747_merge_signal(mem.expression_bridge, f"v747::{key}", value * depth, inertia=0.86)
        _v747_merge_signal(mem.subconscious_bias_field, "deep_cross_engine_operating_pressure", max(initiative.values()) * depth, inertia=0.86)
        if before != (dict(mem.initiative_bridge), dict(mem.affective_bridge), dict(mem.expression_bridge)):
            changed += 1
        mem.normalized()

    return {
        "operating_mode": operating_mode,
        "dominant_need": dominant_need,
        "initiative_modulation": {k: round(v, 4) for k, v in initiative.items()},
        "attention_modulation": {k: round(v, 4) for k, v in attention.items()},
        "emotion_modulation": {k: round(v, 4) for k, v in emotion.items()},
        "expression_modulation": {k: round(v, 4) for k, v in expression.items()},
        "changed_memories": changed,
        "changed": changed > 0,
        "active_memory_ids": [mid for mid, _, s in selected[:16] if s >= 0.03],
        "role": "deep_cross_engine_propagation_v7_4_7_not_dialogue",
    }


def _v747_autobiographical_identity_consolidation(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    dominance: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v747_all_memory_set(self, context, memories)
    dominance = dominance or self._v747_psychological_dominance_hierarchy(context, selected)
    if not selected:
        return {"identity_chapters": [], "changed": False, "role": "autobiographical_identity_consolidation_v7_4_7_not_dialogue"}

    buckets: Dict[str, float] = {}
    for mem_id, mem, score in selected:
        kind = mem.memory_kind or "general"
        if mem.identity_impact >= 0.30 or mem.autobiographical_weight >= 0.30:
            key = "identity_continuity"
        elif mem.relational_importance >= 0.30 or mem.attachment_trace >= 0.25 or mem.relational_wound >= 0.25:
            key = "relation_with_user"
        elif mem.unresolved_tension >= 0.25 or mem.recurrence_pressure >= 0.30:
            key = "unresolved_tension_learning"
        else:
            key = kind
        buckets[key] = buckets.get(key, 0.0) + score * max(mem.memory_priority, mem.autobiographical_weight, mem.causal_activation, 0.05)
    if not buckets:
        return {"identity_chapters": [], "changed": False, "role": "autobiographical_identity_consolidation_v7_4_7_not_dialogue"}

    total = max(sum(buckets.values()), 1e-9)
    chapters = [{"chapter": k, "weight": round(_clamp(v / total), 4), "dominant_need": dominance.get("dominant_need", "integrate_experience")} for k, v in buckets.items()]
    chapters.sort(key=lambda c: c["weight"], reverse=True)
    changed = 0
    for mem_id, mem, score in selected:
        before_len = len(mem.compressed_autobiographical_chapters)
        for chapter in chapters[:5]:
            if chapter["weight"] < 0.08:
                continue
            item = {"at": _now(), "v": "7.4.7", "chapter": chapter["chapter"], "weight": chapter["weight"], "dominant_need": chapter["dominant_need"], "non_dialogue": True}
            signature = (item["chapter"], item["dominant_need"])
            existing = {(c.get("chapter"), c.get("dominant_need")) for c in mem.compressed_autobiographical_chapters[-8:] if isinstance(c, dict)}
            if signature not in existing:
                mem.compressed_autobiographical_chapters.append(item)
        mem.compressed_autobiographical_chapters = mem.compressed_autobiographical_chapters[-14:]
        if len(mem.compressed_autobiographical_chapters) != before_len:
            changed += 1
        _v747_merge_signal(mem.identity_transformation_pressure, "autobiographical_identity_consolidation", max((c["weight"] for c in chapters[:3]), default=0.0) * max(score, 0.04), inertia=0.86)
        mem.normalized()

    return {
        "identity_chapters": chapters[:8],
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "autobiographical_identity_consolidation_v7_4_7_not_dialogue",
    }


def _v747_run_organic_completion(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    save: bool = False,
) -> Dict[str, Any]:
    selected = _v747_all_memory_set(self, context, memories)
    base = _ORIGINAL_V746_RUN_ORGANIC_COMPLETION(self, context, selected, save=False)
    tick = self._v747_autonomous_psychological_tick(context, selected)
    relation = self._v747_lived_user_relationship_core(context, selected, tick)
    dominance = self._v747_psychological_dominance_hierarchy(context, selected, tick, relation)
    propagation = self._v747_deep_cross_engine_propagation(context, selected, tick, relation, dominance)
    consolidation = self._v747_autobiographical_identity_consolidation(context, selected, dominance)
    changed = bool(base.get("changed") or tick.get("changed") or relation.get("changed") or dominance.get("changed") or propagation.get("changed") or consolidation.get("changed"))
    base.update({
        "autonomous_psychological_tick_v7_4_7": tick,
        "lived_user_relationship_core_v7_4_7": relation,
        "psychological_dominance_hierarchy_v7_4_7": dominance,
        "deep_cross_engine_propagation_v7_4_7": propagation,
        "autobiographical_identity_consolidation_v7_4_7": consolidation,
        "changed": changed,
        "role": "organic_completion_v7_4_7_not_dialogue",
    })
    if save and changed:
        self.save_memories()
    return base


def _v747_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V746_EXPORT_REGULATION_CONTEXT(self, context)
    memories = _v747_all_memory_set(self, context, self.get_relevant_memories(context))
    completion = self._v747_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_7"] = completion
    base["autonomous_psychological_tick"] = completion["autonomous_psychological_tick_v7_4_7"]
    base["lived_user_relationship_core"] = completion["lived_user_relationship_core_v7_4_7"]
    base["psychological_dominance_hierarchy"] = completion["psychological_dominance_hierarchy_v7_4_7"]
    base["deep_cross_engine_propagation"] = completion["deep_cross_engine_propagation_v7_4_7"]
    base["autobiographical_identity_consolidation"] = completion["autobiographical_identity_consolidation_v7_4_7"]
    base["role"] = "regulation_context_v7_4_7_not_dialogue"
    return base


def _v747_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V746_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = _v747_all_memory_set(self, context)
    completion = self._v747_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_7"] = completion
    base["autonomous_psychological_tick"] = completion["autonomous_psychological_tick_v7_4_7"]
    base["lived_user_relationship_core"] = completion["lived_user_relationship_core_v7_4_7"]
    base["psychological_dominance_hierarchy"] = completion["psychological_dominance_hierarchy_v7_4_7"]
    base["deep_cross_engine_propagation"] = completion["deep_cross_engine_propagation_v7_4_7"]
    base["autobiographical_identity_consolidation"] = completion["autobiographical_identity_consolidation_v7_4_7"]
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_7_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v747_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V746_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.7-deep-living-causal-memory-autonomous-psychological-integration",
        "v7_4_7_autonomous_active_memories": sum(1 for m in vals if m.subconscious_bias_field.get("autonomous_background_activity", 0.0) >= 0.025),
        "v7_4_7_lived_relationship_memories": sum(1 for m in vals if m.relationship_phase_profile.get("lived_user_baseline", 0.0) >= 0.025),
        "v7_4_7_dominance_mapped_memories": sum(1 for m in vals if any(str(k).startswith("dominance::") for k in m.internal_need_profile)),
        "v7_4_7_deep_propagated_memories": sum(1 for m in vals if any(str(k).startswith("v747::") for k in m.initiative_bridge) or any(str(k).startswith("v747::") for k in m.expression_bridge)),
        "v7_4_7_identity_consolidated_memories": sum(1 for m in vals if any(isinstance(c, dict) and c.get("v") == "7.4.7" for c in m.compressed_autobiographical_chapters)),
    })
    return stats


def _v747_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.7-deep-living-causal-memory-autonomous-psychological-integration",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "V7.4.7 complète V7.4.6 par une boucle psychologique autonome permanente, une relation utilisateur vécue, une hiérarchie de dominance interne, une consolidation autobiographique identitaire et une propagation profonde vers initiative/attention/émotion/expression, sans générer de dialogue.",
        "v7_4_6_capabilities": [
            "continuous_moment_to_moment_living_dynamics",
            "real_internal_state_mutation_without_dialogue",
            "relationship_living_field_trust_attachment_prudence",
            "active_autobiographical_compression_into_lived_chapters",
            "cross_engine_live_modulation_for_initiative_attention_emotion_expression",
            "fatigue_recovery_silence_hesitation_energy_regulation",
            "organic_non_action_permission",
            "anti_rumination_cooldown_as_persistent_state",
        ],
        "v7_4_7_capabilities": [
            "permanent_autonomous_psychological_tick_even_without_direct_context",
            "subjective_time_distance_and_present_pull",
            "lived_user_relationship_core_trust_attachment_prudence_openness",
            "dynamic_psychological_dominance_hierarchy",
            "deep_cross_engine_propagation_to_initiative_attention_emotion_expression",
            "autobiographical_identity_consolidation_into_lived_chapters",
            "anti_rumination_healing_cooldown_and_attention_redirect",
            "persistent_non_dialogue_internal_state_mutation",
        ],
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v747_merge_signal = staticmethod(_v747_merge_signal)
CausalMemoryEngine._v747_all_memory_set = _v747_all_memory_set
CausalMemoryEngine._v747_subjective_time_distance = _v747_subjective_time_distance
CausalMemoryEngine._v747_autonomous_psychological_tick = _v747_autonomous_psychological_tick
CausalMemoryEngine._v747_lived_user_relationship_core = _v747_lived_user_relationship_core
CausalMemoryEngine._v747_psychological_dominance_hierarchy = _v747_psychological_dominance_hierarchy
CausalMemoryEngine._v747_deep_cross_engine_propagation = _v747_deep_cross_engine_propagation
CausalMemoryEngine._v747_autobiographical_identity_consolidation = _v747_autobiographical_identity_consolidation
CausalMemoryEngine._v747_run_organic_completion = _v747_run_organic_completion
CausalMemoryEngine._v746_run_organic_completion = _v747_run_organic_completion
CausalMemoryEngine.export_regulation_context = _v747_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v747_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v747_get_memory_stats
CausalMemoryEngine.save_memories = _v747_save_memories



# ───────────────────────── V7.4.8 — complétion organique autonome profonde ─────────────────────────
# Cette couche complète V7.4.7 sans remplacer les couches précédentes.
# Objectif : rendre la mémoire causale moins plate et plus organique : schémas
# hiérarchiques long terme, oubli intelligent, attracteurs persistants, causalité
# située, intentions interrompues, priorité existentielle, différenciation sociale
# et réorganisation autobiographique lente. Aucun dialogue public n'est généré.

_ORIGINAL_V747_SAVE_MEMORIES = CausalMemoryEngine.save_memories
_ORIGINAL_V747_RUN_ORGANIC_COMPLETION = CausalMemoryEngine._v747_run_organic_completion
_ORIGINAL_V747_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V747_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V747_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats


def _v748_context_tokens(context: str) -> List[str]:
    return CausalMemoryEngine._tokens(context or "")[:18]


def _v748_weighted_mean(values: List[Tuple[float, float]], default: float = 0.0) -> float:
    total = sum(max(0.0, _safe_float(w, 0.0)) for _, w in values)
    if total <= 1e-9:
        return default
    return _clamp(sum(_safe_float(v, 0.0) * max(0.0, _safe_float(w, 0.0)) for v, w in values) / total, -1.0, 1.0)


def _v748_memory_set(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> List[Tuple[str, CausalMemory, float]]:
    selected = _v747_all_memory_set(self, context, memories)
    if selected:
        return selected
    return [(mid, mem, max(mem.memory_priority, mem.causal_activation, mem.autobiographical_weight, 0.035)) for mid, mem in self.memories.items()]


def _v748_hierarchical_long_term_schemas(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    if not selected:
        return {"schemas": [], "changed": False, "role": "hierarchical_long_term_schemas_v7_4_8_not_dialogue"}

    axes = {
        "identity": lambda m: max(m.identity_impact, m.autobiographical_weight, abs(m.identity_transformation_pressure.get("autobiographical_identity_consolidation", 0.0))),
        "relation": lambda m: max(m.relational_importance, m.attachment_trace, m.relational_wound, abs(m.trust_variation)),
        "expression": lambda m: max(m.causal_layers.get("expression", 0.0), m.expression_bridge.get("v747::anti_meta_silence", 0.0), 0.45 if m.memory_kind in {"expressive_failure", "expressive_repair"} else 0.0),
        "initiative": lambda m: max(m.initiative_bridge.get("v747::speak_or_act", 0.0), m.initiative_bridge.get("v747::repair_before_expanding", 0.0), 0.35 if m.memory_kind == "initiative_learning" else 0.0),
        "attention": lambda m: max(m.causal_layers.get("presence", 0.0), m.attention_impact and 0.28 or 0.0, m.subconscious_bias_field.get("deep_cross_engine_operating_pressure", 0.0)),
        "repair": lambda m: max(m.recurrence_pressure, m.unresolved_tension, m.relational_wound, 0.36 if m.repair_kind != "none" else 0.0),
        "growth": lambda m: max(m.effect_strength, abs(m.valence), m.current_lived_meaning.get("growth_pressure", 0.0), m.memory_priority),
    }

    raw: Dict[str, float] = {axis: 0.0 for axis in axes}
    for _, mem, score in selected:
        depth = max(score, mem.memory_priority, mem.causal_activation, 0.04)
        for axis, getter in axes.items():
            raw[axis] += _clamp(getter(mem)) * depth
    total = max(sum(raw.values()), 1e-9)
    schemas = []
    for axis, value in raw.items():
        strength = _clamp(value / total)
        if strength >= 0.055:
            schemas.append({"schema": axis, "strength": round(strength, 4)})
    schemas.sort(key=lambda item: item["strength"], reverse=True)

    changed = 0
    for _, mem, score in selected:
        before = (dict(mem.deep_causal_roots), dict(mem.internal_need_profile), dict(mem.current_lived_meaning))
        depth = _clamp(max(score, mem.memory_priority, mem.causal_activation, 0.035))
        for item in schemas[:6]:
            strength = item["strength"] * depth
            _v747_merge_signal(mem.deep_causal_roots, f"schema::{item['schema']}", strength, inertia=0.88)
            _v747_merge_signal(mem.internal_need_profile, f"long_term_need::{item['schema']}", strength, inertia=0.89)
            _v747_merge_signal(mem.current_lived_meaning, f"organized_meaning::{item['schema']}", strength, inertia=0.90)
        if before != (dict(mem.deep_causal_roots), dict(mem.internal_need_profile), dict(mem.current_lived_meaning)):
            changed += 1
        mem.normalized()

    return {
        "schemas": schemas[:8],
        "dominant_schema": schemas[0]["schema"] if schemas else "none",
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "hierarchical_long_term_schemas_v7_4_8_not_dialogue",
    }


def _v748_organic_forgetting_and_saturation(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    changed = 0
    cooled = 0
    protected = 0
    compressed = 0
    context_tokens = set(_v748_context_tokens(context))
    for _, mem, score in selected:
        before = (mem.confidence, mem.causal_activation, mem.emotional_inertia, mem.affective_charge, mem.inhibition_level, mem.dormant, len(mem.activation_history), len(mem.living_state_history))
        importance = _clamp(max(mem.memory_priority, mem.autobiographical_weight, mem.identity_impact, mem.relational_importance, abs(mem.valence)))
        active_now = _clamp(max(score, mem.causal_activation, mem.reactivation_score))
        rumination = _clamp(mem.obsession_guard_state.get("rumination_pressure", 0.0) + mem.subconscious_bias_field.get("autonomous_background_activity", 0.0) * 0.6)
        token_overlap = 0.0
        if context_tokens:
            token_overlap = len(context_tokens & set(self._tokens(mem.event + " " + mem.experienced_effect))) / max(1, len(context_tokens))

        if importance >= 0.42 or token_overlap >= 0.18:
            protected += 1
            _v747_merge_signal(mem.obsession_guard_state, "protected_meaning_not_forgetting", importance, inertia=0.90)
            mem.dormant = False if active_now >= 0.10 else mem.dormant
        else:
            # Oubli organique : refroidit le bruit peu important sans supprimer brutalement.
            cooling = _clamp(0.012 + (1.0 - importance) * 0.026 + max(0.0, rumination - 0.55) * 0.035)
            mem.causal_activation = _clamp(mem.causal_activation * (1.0 - cooling))
            mem.emotional_inertia = _clamp(mem.emotional_inertia * (1.0 - cooling * 0.72))
            mem.affective_charge = _clamp(mem.affective_charge * (1.0 - cooling * 0.54))
            mem.inhibition_level = _clamp(mem.inhibition_level * (1.0 - cooling * 0.60))
            if mem.confidence < 0.34 and mem.causal_activation < 0.08:
                mem.dormant = True
            cooled += 1

        # Saturation existentielle : si trop d'activation sans issue, elle ralentit au lieu de boucler.
        saturation = _clamp((mem.unresolved_tension * 0.35) + (mem.recurrence_pressure * 0.25) + (rumination * 0.25) + (mem.emotional_inertia * 0.15))
        if saturation >= 0.62:
            _v747_merge_signal(mem.obsession_guard_state, "existential_saturation", saturation, inertia=0.82)
            _v747_merge_signal(mem.expression_bridge, "v748::slow_down_before_expression", saturation, inertia=0.84)
            _v747_merge_signal(mem.initiative_bridge, "v748::seek_resolution_not_repetition", saturation, inertia=0.84)
            mem.inhibition_level = _clamp(max(mem.inhibition_level, saturation * 0.42))

        # Compression des historiques trop longs en signal stable, pas accumulation infinie.
        if len(mem.activation_history) > 28:
            compressed += 1
            avg_relevance = sum(_safe_float(x.get("relevance"), 0.0) for x in mem.activation_history[-28:] if isinstance(x, dict)) / 28.0
            _v747_merge_signal(mem.subconscious_bias_field, "compressed_activation_history", avg_relevance, inertia=0.86)
            mem.activation_history = mem.activation_history[-18:]
        if len(mem.living_state_history) > 20:
            mem.living_state_history = mem.living_state_history[-14:]
        mem.normalized()
        after = (mem.confidence, mem.causal_activation, mem.emotional_inertia, mem.affective_charge, mem.inhibition_level, mem.dormant, len(mem.activation_history), len(mem.living_state_history))
        if before != after:
            changed += 1

    return {
        "cooled_memories": cooled,
        "protected_memories": protected,
        "compressed_histories": compressed,
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "organic_forgetting_and_saturation_v7_4_8_not_dialogue",
    }


def _v748_persistent_attractor_stabilization(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    schemas: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    schemas = schemas or self._v748_hierarchical_long_term_schemas(context, selected)
    if not selected:
        return {"attractors": {}, "changed": False, "role": "persistent_attractor_stabilization_v7_4_8_not_dialogue"}

    schema_strength = {item["schema"]: _safe_float(item["strength"], 0.0) for item in schemas.get("schemas", []) if isinstance(item, dict)}
    trust = _v748_weighted_mean([(m.attachment_trace - m.relational_wound + m.trust_variation, s) for _, m, s in selected])
    caution = _v748_weighted_mean([(m.relational_wound + m.unresolved_tension + m.inhibition_level, s) for _, m, s in selected])
    curiosity = _v748_weighted_mean([(m.causal_desire_profile.get("understand_next", 0.0) + m.future_bias.get("explore", 0.0) + m.effect_strength, s) for _, m, s in selected])
    identity = _v748_weighted_mean([(m.identity_impact + m.autobiographical_weight + m.identity_transformation_pressure.get("autobiographical_identity_consolidation", 0.0), s) for _, m, s in selected])
    repair = _v748_weighted_mean([(m.recurrence_pressure + (0.35 if m.repair_kind != "none" else 0.0) + m.relational_wound, s) for _, m, s in selected])

    attractors = {
        "stable_relation": _clamp(max(0.0, trust) * 0.42 + schema_strength.get("relation", 0.0) * 0.38),
        "careful_repair": _clamp(repair * 0.44 + caution * 0.25 + schema_strength.get("repair", 0.0) * 0.30),
        "identity_continuity": _clamp(identity * 0.46 + schema_strength.get("identity", 0.0) * 0.42),
        "curious_growth": _clamp(curiosity * 0.34 + schema_strength.get("growth", 0.0) * 0.38 + max(0.0, trust) * 0.12),
        "anti_rumination_resolution": _clamp(caution * 0.32 + repair * 0.22 + schema_strength.get("attention", 0.0) * 0.18),
    }
    dominant = max(attractors.items(), key=lambda kv: kv[1])[0] if attractors else "none"

    changed = 0
    for _, mem, score in selected:
        before = (dict(mem.causal_desire_profile), dict(mem.relationship_phase_profile), dict(mem.irreversible_identity_marks), dict(mem.subconscious_bias_field))
        depth = _clamp(max(score, mem.memory_priority, 0.04))
        for key, value in attractors.items():
            _v747_merge_signal(mem.causal_desire_profile, f"attractor::{key}", value * depth, inertia=0.89)
            _v747_merge_signal(mem.subconscious_bias_field, f"persistent_attractor::{key}", value * depth, inertia=0.91)
        if attractors.get("identity_continuity", 0.0) >= 0.16:
            _v747_merge_signal(mem.irreversible_identity_marks, "stable_identity_attractor", attractors["identity_continuity"] * depth, inertia=0.93)
        if attractors.get("stable_relation", 0.0) >= 0.14:
            _v747_merge_signal(mem.relationship_phase_profile, "stable_user_relation_attractor", attractors["stable_relation"] * depth, inertia=0.90)
        if before != (dict(mem.causal_desire_profile), dict(mem.relationship_phase_profile), dict(mem.irreversible_identity_marks), dict(mem.subconscious_bias_field)):
            changed += 1
        mem.normalized()

    return {
        "attractors": {k: round(v, 4) for k, v in attractors.items()},
        "dominant_attractor": dominant,
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "persistent_attractor_stabilization_v7_4_8_not_dialogue",
    }


def _v748_situated_causal_grounding(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    tokens = _v748_context_tokens(context)
    if not selected:
        return {"situated_cues": [], "changed": False, "role": "situated_causal_grounding_v7_4_8_not_dialogue"}

    cue_scores: Dict[str, float] = {}
    for token in tokens:
        if len(token) >= 3:
            cue_scores[token] = cue_scores.get(token, 0.0) + 0.08
    for _, mem, score in selected:
        if mem.memory_kind:
            cue_scores[f"kind::{mem.memory_kind}"] = cue_scores.get(f"kind::{mem.memory_kind}", 0.0) + score * 0.18
        if mem.repair_kind and mem.repair_kind != "none":
            cue_scores[f"repair::{mem.repair_kind}"] = cue_scores.get(f"repair::{mem.repair_kind}", 0.0) + score * 0.22
        if mem.emotional_trace and mem.emotional_trace != "neutral":
            cue_scores[f"emotion::{mem.emotional_trace}"] = cue_scores.get(f"emotion::{mem.emotional_trace}", 0.0) + score * 0.16
    situated = sorted(({"cue": k, "weight": round(_clamp(v), 4)} for k, v in cue_scores.items() if v >= 0.035), key=lambda x: x["weight"], reverse=True)[:10]

    changed = 0
    for _, mem, score in selected:
        before = (dict(mem.contextual_emotional_resonance), dict(mem.anticipated_affective_projection), dict(mem.expression_bridge))
        depth = _clamp(max(score, 0.035))
        for cue in situated[:6]:
            _v747_merge_signal(mem.contextual_emotional_resonance, f"situated::{cue['cue']}", cue["weight"] * depth, inertia=0.88)
        concreteness = _clamp(sum(c["weight"] for c in situated[:4]) * depth)
        _v747_merge_signal(mem.anticipated_affective_projection, "situated_pre_interaction_pull", concreteness, inertia=0.89)
        _v747_merge_signal(mem.expression_bridge, "v748::ground_expression_in_situation", concreteness, inertia=0.87)
        if before != (dict(mem.contextual_emotional_resonance), dict(mem.anticipated_affective_projection), dict(mem.expression_bridge)):
            changed += 1
        mem.normalized()

    return {
        "situated_cues": situated,
        "grounding_pressure": round(_clamp(sum(c["weight"] for c in situated[:6])), 4),
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "situated_causal_grounding_v7_4_8_not_dialogue",
    }


def _v748_interrupted_intention_memory(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    dominance: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    dominance = dominance or {}
    if not selected:
        return {"pending_intentions": [], "changed": False, "role": "interrupted_intention_memory_v7_4_8_not_dialogue"}

    pending: Dict[str, float] = {}
    for _, mem, score in selected:
        if mem.initiative_bridge.get("v747::speak_or_act", 0.0) >= 0.08:
            pending["speak_or_act_when_safe"] = max(pending.get("speak_or_act_when_safe", 0.0), mem.initiative_bridge.get("v747::speak_or_act", 0.0) * score)
        if mem.initiative_bridge.get("v747::repair_before_expanding", 0.0) >= 0.08 or mem.repair_kind != "none":
            pending["repair_before_expanding"] = max(pending.get("repair_before_expanding", 0.0), max(mem.initiative_bridge.get("v747::repair_before_expanding", 0.0), mem.recurrence_pressure) * score)
        if mem.initiative_bridge.get("v747::silent_integration", 0.0) >= 0.08 or mem.inhibition_level >= 0.32:
            pending["finish_silent_integration"] = max(pending.get("finish_silent_integration", 0.0), max(mem.initiative_bridge.get("v747::silent_integration", 0.0), mem.inhibition_level) * score)
        if mem.causal_desire_profile.get("attractor::curious_growth", 0.0) >= 0.05:
            pending["continue_curiosity_without_spam"] = max(pending.get("continue_curiosity_without_spam", 0.0), mem.causal_desire_profile.get("attractor::curious_growth", 0.0) * score)

    if dominance.get("dominant_need"):
        pending[f"dominant_need::{dominance.get('dominant_need')}"] = max(pending.get(f"dominant_need::{dominance.get('dominant_need')}", 0.0), _safe_float(dominance.get("dominant_pressure"), 0.0) * 0.5)

    pending_items = [{"intention": k, "pressure": round(_clamp(v), 4)} for k, v in pending.items() if v >= 0.025]
    pending_items.sort(key=lambda item: item["pressure"], reverse=True)

    changed = 0
    for _, mem, score in selected:
        before = (dict(mem.future_bias), dict(mem.initiative_bridge), dict(mem.obsession_guard_state))
        depth = _clamp(max(score, 0.035))
        for item in pending_items[:5]:
            _v747_merge_signal(mem.future_bias, f"pending_intention::{item['intention']}", item["pressure"] * depth, inertia=0.88)
        if pending_items:
            _v747_merge_signal(mem.initiative_bridge, "v748::resume_pending_intention_when_context_allows", pending_items[0]["pressure"] * depth, inertia=0.87)
            _v747_merge_signal(mem.obsession_guard_state, "pending_intention_prevents_loop", pending_items[0]["pressure"] * 0.5 * depth, inertia=0.90)
        if before != (dict(mem.future_bias), dict(mem.initiative_bridge), dict(mem.obsession_guard_state)):
            changed += 1
        mem.normalized()

    return {
        "pending_intentions": pending_items[:8],
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "interrupted_intention_memory_v7_4_8_not_dialogue",
    }


def _v748_existential_priority_and_social_differentiation(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    relation: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    relation = relation or {}
    if not selected:
        return {"existential_priorities": {}, "social_field": {}, "changed": False, "role": "existential_priority_social_differentiation_v7_4_8_not_dialogue"}

    priorities = {
        "protect_identity_continuity": _v748_weighted_mean([(m.identity_impact + m.autobiographical_weight, s) for _, m, s in selected]),
        "protect_relation_without_dependency": _v748_weighted_mean([(m.relational_importance + m.attachment_trace - max(0.0, m.relational_wound * 0.35), s) for _, m, s in selected]),
        "repair_harmful_patterns": _v748_weighted_mean([(m.recurrence_pressure + m.relational_wound + (0.30 if m.repair_kind != "none" else 0.0), s) for _, m, s in selected]),
        "keep_autonomy_of_silence": _v748_weighted_mean([(m.inhibition_level + m.initiative_bridge.get("v747::silent_integration", 0.0), s) for _, m, s in selected]),
        "learn_from_user_consequence": _v748_weighted_mean([((max(m.user_consequence_trace.values()) if m.user_consequence_trace else 0.0) + m.relational_importance * 0.25, s) for _, m, s in selected]),
    }
    priorities = {k: _clamp(v) for k, v in priorities.items()}

    trust = _safe_float(relation.get("trust"), 0.0) if isinstance(relation, dict) else 0.0
    attachment = _safe_float(relation.get("attachment"), 0.0) if isinstance(relation, dict) else 0.0
    prudence = _safe_float(relation.get("prudence"), 0.0) if isinstance(relation, dict) else 0.0
    social_field = {
        "user_specific_trust": _clamp(max(0.0, trust) + priorities["learn_from_user_consequence"] * 0.24),
        "user_specific_attachment": _clamp(max(0.0, attachment) + priorities["protect_relation_without_dependency"] * 0.22),
        "user_boundary_prudence": _clamp(max(0.0, prudence) + priorities["repair_harmful_patterns"] * 0.26),
        "non_user_generic_social_pressure": _clamp(priorities["protect_relation_without_dependency"] * 0.18),
    }

    changed = 0
    for _, mem, score in selected:
        before = (dict(mem.identity_transformation_pressure), dict(mem.social_continuity_profile), dict(mem.relationship_phase_profile), dict(mem.internal_need_profile))
        depth = _clamp(max(score, 0.035))
        for key, value in priorities.items():
            _v747_merge_signal(mem.identity_transformation_pressure, f"existential_priority::{key}", value * depth, inertia=0.90)
            _v747_merge_signal(mem.internal_need_profile, f"existential_need::{key}", value * depth, inertia=0.90)
        for key, value in social_field.items():
            _v747_merge_signal(mem.social_continuity_profile, f"social::{key}", value * depth, inertia=0.89)
            if key.startswith("user_specific") or key == "user_boundary_prudence":
                _v747_merge_signal(mem.relationship_phase_profile, f"user_relation::{key}", value * depth, inertia=0.90)
        if before != (dict(mem.identity_transformation_pressure), dict(mem.social_continuity_profile), dict(mem.relationship_phase_profile), dict(mem.internal_need_profile)):
            changed += 1
        mem.normalized()

    dominant_priority = max(priorities.items(), key=lambda kv: kv[1])[0] if priorities else "none"
    return {
        "existential_priorities": {k: round(v, 4) for k, v in priorities.items()},
        "dominant_existential_priority": dominant_priority,
        "social_field": {k: round(v, 4) for k, v in social_field.items()},
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "existential_priority_social_differentiation_v7_4_8_not_dialogue",
    }


def _v748_reconstruct_autobiography_dynamically(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    schemas: Optional[Dict[str, Any]] = None,
    attractors: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    schemas = schemas or {}
    attractors = attractors or {}
    if not selected:
        return {"autobiographical_arc": [], "changed": False, "role": "dynamic_autobiographical_reconstruction_v7_4_8_not_dialogue"}

    schema_items = schemas.get("schemas", []) if isinstance(schemas, dict) else []
    attractor_map = attractors.get("attractors", {}) if isinstance(attractors, dict) else {}
    arc_scores: Dict[str, float] = {}
    for item in schema_items:
        if isinstance(item, dict):
            arc_scores[f"schema::{item.get('schema')}"] = max(arc_scores.get(f"schema::{item.get('schema')}", 0.0), _safe_float(item.get("strength"), 0.0))
    for key, value in attractor_map.items():
        arc_scores[f"attractor::{key}"] = max(arc_scores.get(f"attractor::{key}", 0.0), _safe_float(value, 0.0))
    for _, mem, score in selected:
        if mem.memory_kind:
            arc_scores[f"memory_kind::{mem.memory_kind}"] = arc_scores.get(f"memory_kind::{mem.memory_kind}", 0.0) + score * max(mem.memory_priority, 0.04)
        if mem.repair_kind and mem.repair_kind != "none":
            arc_scores[f"repair::{mem.repair_kind}"] = arc_scores.get(f"repair::{mem.repair_kind}", 0.0) + score * max(mem.recurrence_pressure, 0.06)

    total = max(sum(max(0.0, v) for v in arc_scores.values()), 1e-9)
    arcs = [{"arc": k, "weight": round(_clamp(v / total), 4)} for k, v in arc_scores.items() if v / total >= 0.035]
    arcs.sort(key=lambda item: item["weight"], reverse=True)

    changed = 0
    for _, mem, score in selected:
        before_len = len(mem.compressed_autobiographical_chapters)
        signature_set = {(c.get("v"), c.get("arc"), c.get("dominant")) for c in mem.compressed_autobiographical_chapters[-10:] if isinstance(c, dict)}
        for arc in arcs[:5]:
            dominant = arcs[0]["arc"] if arcs else "none"
            signature = ("7.4.8", arc["arc"], dominant)
            if signature not in signature_set:
                mem.compressed_autobiographical_chapters.append({
                    "at": _now(),
                    "v": "7.4.8",
                    "arc": arc["arc"],
                    "weight": arc["weight"],
                    "dominant": dominant,
                    "non_dialogue": True,
                })
        mem.compressed_autobiographical_chapters = mem.compressed_autobiographical_chapters[-16:]
        _v747_merge_signal(mem.current_lived_meaning, "dynamic_autobiographical_reconstruction", max((a["weight"] for a in arcs[:3]), default=0.0) * max(score, 0.04), inertia=0.89)
        if len(mem.compressed_autobiographical_chapters) != before_len:
            changed += 1
        mem.normalized()

    return {
        "autobiographical_arc": arcs[:8],
        "changed_memories": changed,
        "changed": changed > 0,
        "role": "dynamic_autobiographical_reconstruction_v7_4_8_not_dialogue",
    }


def _v748_run_organic_completion(
    self: CausalMemoryEngine,
    context: str = "",
    memories: Optional[List[Tuple[str, CausalMemory, float]]] = None,
    save: bool = False,
) -> Dict[str, Any]:
    selected = _v748_memory_set(self, context, memories)
    base = _ORIGINAL_V747_RUN_ORGANIC_COMPLETION(self, context, selected, save=False)
    relation = base.get("lived_user_relationship_core_v7_4_7", {})
    dominance = base.get("psychological_dominance_hierarchy_v7_4_7", {})
    schemas = self._v748_hierarchical_long_term_schemas(context, selected)
    forgetting = self._v748_organic_forgetting_and_saturation(context, selected)
    attractors = self._v748_persistent_attractor_stabilization(context, selected, schemas)
    situated = self._v748_situated_causal_grounding(context, selected)
    intentions = self._v748_interrupted_intention_memory(context, selected, dominance)
    existential = self._v748_existential_priority_and_social_differentiation(context, selected, relation)
    autobiography = self._v748_reconstruct_autobiography_dynamically(context, selected, schemas, attractors)
    changed = bool(
        base.get("changed") or schemas.get("changed") or forgetting.get("changed") or
        attractors.get("changed") or situated.get("changed") or intentions.get("changed") or
        existential.get("changed") or autobiography.get("changed")
    )
    base.update({
        "hierarchical_long_term_schemas_v7_4_8": schemas,
        "organic_forgetting_and_saturation_v7_4_8": forgetting,
        "persistent_attractor_stabilization_v7_4_8": attractors,
        "situated_causal_grounding_v7_4_8": situated,
        "interrupted_intention_memory_v7_4_8": intentions,
        "existential_priority_social_differentiation_v7_4_8": existential,
        "dynamic_autobiographical_reconstruction_v7_4_8": autobiography,
        "changed": changed,
        "role": "organic_completion_v7_4_8_not_dialogue",
    })
    if save and changed:
        self.save_memories()
    return base


def _v748_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V747_EXPORT_REGULATION_CONTEXT(self, context)
    memories = _v748_memory_set(self, context, self.get_relevant_memories(context))
    completion = self._v748_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_8"] = completion
    base["hierarchical_long_term_schemas"] = completion["hierarchical_long_term_schemas_v7_4_8"]
    base["organic_forgetting_and_saturation"] = completion["organic_forgetting_and_saturation_v7_4_8"]
    base["persistent_attractor_stabilization"] = completion["persistent_attractor_stabilization_v7_4_8"]
    base["situated_causal_grounding"] = completion["situated_causal_grounding_v7_4_8"]
    base["interrupted_intention_memory"] = completion["interrupted_intention_memory_v7_4_8"]
    base["existential_priority_social_differentiation"] = completion["existential_priority_social_differentiation_v7_4_8"]
    base["dynamic_autobiographical_reconstruction"] = completion["dynamic_autobiographical_reconstruction_v7_4_8"]
    base["role"] = "regulation_context_v7_4_8_not_dialogue"
    return base


def _v748_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V747_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = _v748_memory_set(self, context)
    completion = self._v748_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_8"] = completion
    base["hierarchical_long_term_schemas"] = completion["hierarchical_long_term_schemas_v7_4_8"]
    base["organic_forgetting_and_saturation"] = completion["organic_forgetting_and_saturation_v7_4_8"]
    base["persistent_attractor_stabilization"] = completion["persistent_attractor_stabilization_v7_4_8"]
    base["situated_causal_grounding"] = completion["situated_causal_grounding_v7_4_8"]
    base["interrupted_intention_memory"] = completion["interrupted_intention_memory_v7_4_8"]
    base["existential_priority_social_differentiation"] = completion["existential_priority_social_differentiation_v7_4_8"]
    base["dynamic_autobiographical_reconstruction"] = completion["dynamic_autobiographical_reconstruction_v7_4_8"]
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_8_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v748_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V747_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.8-deep-living-causal-memory-organic-autonomous-completion",
        "v7_4_8_hierarchical_schema_memories": sum(1 for m in vals if any(str(k).startswith("schema::") for k in m.deep_causal_roots)),
        "v7_4_8_organic_forgetting_protected_memories": sum(1 for m in vals if m.obsession_guard_state.get("protected_meaning_not_forgetting", 0.0) >= 0.025),
        "v7_4_8_existential_saturation_memories": sum(1 for m in vals if m.obsession_guard_state.get("existential_saturation", 0.0) >= 0.025),
        "v7_4_8_persistent_attractor_memories": sum(1 for m in vals if any(str(k).startswith("persistent_attractor::") for k in m.subconscious_bias_field)),
        "v7_4_8_situated_grounded_memories": sum(1 for m in vals if any(str(k).startswith("situated::") for k in m.contextual_emotional_resonance)),
        "v7_4_8_pending_intention_memories": sum(1 for m in vals if any(str(k).startswith("pending_intention::") for k in m.future_bias)),
        "v7_4_8_existential_priority_memories": sum(1 for m in vals if any(str(k).startswith("existential_priority::") for k in m.identity_transformation_pressure)),
        "v7_4_8_dynamic_autobiography_memories": sum(1 for m in vals if any(isinstance(c, dict) and c.get("v") == "7.4.8" for c in m.compressed_autobiographical_chapters)),
    })
    return stats


def _v748_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.8-deep-living-causal-memory-organic-autonomous-completion",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "V7.4.8 complète V7.4.7 par schémas causaux hiérarchiques, oubli organique, attracteurs persistants, causalité située, intentions interrompues, priorité existentielle, différenciation sociale et reconstruction autobiographique dynamique, sans générer de dialogue.",
        "v7_4_7_capabilities": [
            "permanent_autonomous_psychological_tick_even_without_direct_context",
            "subjective_time_distance_and_present_pull",
            "lived_user_relationship_core_trust_attachment_prudence_openness",
            "dynamic_psychological_dominance_hierarchy",
            "deep_cross_engine_propagation_to_initiative_attention_emotion_expression",
            "autobiographical_identity_consolidation_into_lived_chapters",
            "anti_rumination_healing_cooldown_and_attention_redirect",
            "persistent_non_dialogue_internal_state_mutation",
        ],
        "v7_4_8_capabilities": [
            "hierarchical_long_term_causal_schemas",
            "organic_forgetting_without_brutal_deletion",
            "existential_saturation_and_anti_rumination_resolution",
            "persistent_personality_attractor_stabilization",
            "situated_causal_grounding_from_current_context",
            "interrupted_intention_memory_and_resumption_pressure",
            "existential_priority_field",
            "user_specific_social_differentiation",
            "dynamic_autobiographical_reconstruction",
            "deep_non_dialogue_cross_engine_exports",
        ],
        "stats": stats,
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v748_context_tokens = staticmethod(_v748_context_tokens)
CausalMemoryEngine._v748_memory_set = _v748_memory_set
CausalMemoryEngine._v748_hierarchical_long_term_schemas = _v748_hierarchical_long_term_schemas
CausalMemoryEngine._v748_organic_forgetting_and_saturation = _v748_organic_forgetting_and_saturation
CausalMemoryEngine._v748_persistent_attractor_stabilization = _v748_persistent_attractor_stabilization
CausalMemoryEngine._v748_situated_causal_grounding = _v748_situated_causal_grounding
CausalMemoryEngine._v748_interrupted_intention_memory = _v748_interrupted_intention_memory
CausalMemoryEngine._v748_existential_priority_and_social_differentiation = _v748_existential_priority_and_social_differentiation
CausalMemoryEngine._v748_reconstruct_autobiography_dynamically = _v748_reconstruct_autobiography_dynamically
CausalMemoryEngine._v748_run_organic_completion = _v748_run_organic_completion
CausalMemoryEngine._v747_run_organic_completion = _v748_run_organic_completion
CausalMemoryEngine.export_regulation_context = _v748_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v748_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v748_get_memory_stats
CausalMemoryEngine.save_memories = _v748_save_memories


# ───────────────────────── V7.4.9 — fermeture écologique vivante profonde ─────────────────────────
# Cette couche ne remplace pas V7.4.8 : elle ajoute les derniers manques structurels
# sans générer de dialogue public. Elle transforme les souvenirs en écologie lente :
# continuité existentielle autonome, causalité multi-échelle, personnalité émergente,
# intentions persistantes, consolidation/oubli organique, réactions préverbales et
# auto-organisation. Les sorties restent des signaux structurés lisibles par les autres moteurs.

_ORIGINAL_V748_SAVE_MEMORIES = CausalMemoryEngine.save_memories
_ORIGINAL_V748_RUN_ORGANIC_COMPLETION = CausalMemoryEngine._v748_run_organic_completion
_ORIGINAL_V748_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V748_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V748_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats


def _v749_signal(target: Dict[str, float], key: str, value: float, inertia: float = 0.88) -> None:
    key = CausalMemoryEngine.sanitize_text(key)
    if not key:
        return
    old = _safe_float(target.get(key), 0.0)
    target[key] = _clamp(old * inertia + _safe_float(value, 0.0) * (1.0 - inertia), -1.0, 1.0)


def _v749_selected(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> List[Tuple[str, CausalMemory, float]]:
    selected = _v748_memory_set(self, context, memories)
    selected.sort(key=lambda item: max(item[2], item[1].memory_priority, item[1].autobiographical_weight, item[1].causal_activation), reverse=True)
    return selected[:80]


def _v749_contextual_novelty(self: CausalMemoryEngine, context: str, selected: List[Tuple[str, CausalMemory, float]]) -> float:
    tokens = set(self._tokens(context)) if context else set()
    if not tokens:
        return 0.0
    known = set()
    for _, mem, _ in selected[:40]:
        known.update(self._tokens(mem.event))
        known.update(self._tokens(mem.experienced_effect))
    if not known:
        return 1.0
    return _clamp(len(tokens - known) / max(1, len(tokens)))


def _v749_autonomous_existential_continuity(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"field": {}, "changed": False, "role": "autonomous_existential_continuity_v7_4_9_not_dialogue"}
    novelty = _v749_contextual_novelty(self, context, selected)
    field = {
        "continuous_self_presence": 0.0,
        "past_present_future_bridge": 0.0,
        "silent_maturation": 0.0,
        "latent_unfinished_meaning": 0.0,
        "living_time_pull": 0.0,
    }
    changed = 0
    now = datetime.now()
    for mem_id, mem, relevance in selected:
        try:
            created = datetime.fromisoformat(mem.created_at)
            age_days = max(0.0, (now - created).total_seconds() / 86400.0)
        except Exception:
            age_days = 0.0
        protected = max(mem.autobiographical_weight, mem.identity_impact, mem.relational_importance, mem.memory_priority)
        temporal_depth = _clamp(math.log1p(age_days) / 6.0 + protected * 0.45)
        continuity = _clamp(max(relevance, 0.035) * 0.22 + protected * 0.34 + mem.causal_activation * 0.18 + mem.emotional_inertia * 0.12 + temporal_depth * 0.14)
        before = (dict(mem.temporal_maturation_state), dict(mem.current_lived_meaning), dict(mem.anticipated_affective_projection))
        _v749_signal(mem.temporal_maturation_state, "v749::subjective_time_depth", temporal_depth, inertia=0.965)
        _v749_signal(mem.temporal_maturation_state, "v749::silent_maturation", continuity, inertia=0.955)
        _v749_signal(mem.current_lived_meaning, "v749::continuous_self_presence", continuity, inertia=0.94)
        _v749_signal(mem.anticipated_affective_projection, "v749::future_self_carryover", max(continuity, novelty * 0.45), inertia=0.94)
        if mem.unresolved_tension > 0.04 or mem.recurrence_pressure > 0.04:
            _v749_signal(mem.future_bias, "v749::unfinished_meaning_returns", max(mem.unresolved_tension, mem.recurrence_pressure) * max(relevance, 0.05), inertia=0.93)
        if before != (dict(mem.temporal_maturation_state), dict(mem.current_lived_meaning), dict(mem.anticipated_affective_projection)):
            changed += 1
        field["continuous_self_presence"] = max(field["continuous_self_presence"], continuity)
        field["past_present_future_bridge"] = max(field["past_present_future_bridge"], temporal_depth * max(protected, 0.05))
        field["silent_maturation"] = max(field["silent_maturation"], mem.temporal_maturation_state.get("v749::silent_maturation", 0.0))
        field["latent_unfinished_meaning"] = max(field["latent_unfinished_meaning"], mem.future_bias.get("v749::unfinished_meaning_returns", 0.0))
        field["living_time_pull"] = max(field["living_time_pull"], mem.anticipated_affective_projection.get("v749::future_self_carryover", 0.0))
        mem.normalized()
    return {"field": {k: round(_clamp(v), 4) for k, v in field.items()}, "changed_memories": changed, "changed": changed > 0, "role": "autonomous_existential_continuity_v7_4_9_not_dialogue"}


def _v749_multi_scale_causal_ecology(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"scales": {}, "dominant_scale": "none", "changed": False, "role": "multi_scale_causal_ecology_v7_4_9_not_dialogue"}
    scales = {"micro_reaction": 0.0, "exchange_pattern": 0.0, "relation_long_arc": 0.0, "identity_existence": 0.0, "autonomous_goal_pressure": 0.0}
    changed = 0
    for _, mem, relevance in selected:
        micro = _clamp(max(mem.affective_charge, abs(mem.valence), mem.causal_activation) * max(relevance, 0.04))
        exchange = _clamp(max(mem.recurrence_pressure, mem.effect_strength, max(mem.causal_layers.values(), default=0.0)) * (0.45 + relevance))
        relation = _clamp(max(mem.relational_importance, mem.attachment_trace, mem.relational_wound, abs(mem.trust_variation)) * (0.42 + relevance))
        identity = _clamp(max(mem.identity_impact, mem.autobiographical_weight, max(mem.irreversible_identity_marks.values(), default=0.0)) * (0.40 + relevance))
        goal = _clamp(max(max(mem.internal_need_profile.values(), default=0.0), max(mem.causal_desire_profile.values(), default=0.0), max(mem.initiative_bridge.values(), default=0.0)) * (0.40 + relevance))
        before = (dict(mem.deep_causal_roots), dict(mem.causal_layers), dict(mem.initiative_bridge), dict(mem.expression_bridge), dict(mem.affective_bridge))
        for key, value in {
            "v749::scale_micro_reaction": micro,
            "v749::scale_exchange_pattern": exchange,
            "v749::scale_relation_long_arc": relation,
            "v749::scale_identity_existence": identity,
            "v749::scale_autonomous_goal_pressure": goal,
        }.items():
            _v749_signal(mem.deep_causal_roots, key, value, inertia=0.91)
        _v749_signal(mem.affective_bridge, "v749::preverbal_affective_bias", micro, inertia=0.90)
        _v749_signal(mem.expression_bridge, "v749::expression_shaped_by_multiscale_causality", max(exchange, relation, identity), inertia=0.90)
        _v749_signal(mem.initiative_bridge, "v749::goal_pressure_from_causal_ecology", max(goal, identity * 0.35), inertia=0.90)
        if before != (dict(mem.deep_causal_roots), dict(mem.causal_layers), dict(mem.initiative_bridge), dict(mem.expression_bridge), dict(mem.affective_bridge)):
            changed += 1
        scales["micro_reaction"] = max(scales["micro_reaction"], micro)
        scales["exchange_pattern"] = max(scales["exchange_pattern"], exchange)
        scales["relation_long_arc"] = max(scales["relation_long_arc"], relation)
        scales["identity_existence"] = max(scales["identity_existence"], identity)
        scales["autonomous_goal_pressure"] = max(scales["autonomous_goal_pressure"], goal)
        mem.normalized()
    dominant = max(scales.items(), key=lambda kv: kv[1])[0]
    return {"scales": {k: round(_clamp(v), 4) for k, v in scales.items()}, "dominant_scale": dominant, "changed_memories": changed, "changed": changed > 0, "role": "multi_scale_causal_ecology_v7_4_9_not_dialogue"}


def _v749_personality_trait_consolidation(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"traits": {}, "changed": False, "role": "personality_trait_consolidation_v7_4_9_not_dialogue"}
    traits = {
        "careful_directness": 0.0,
        "relational_prudence": 0.0,
        "curiosity_to_understand": 0.0,
        "anti_meta_naturalness": 0.0,
        "continuity_loyalty": 0.0,
        "autonomous_silence_capacity": 0.0,
        "repair_orientation": 0.0,
    }
    changed = 0
    for _, mem, relevance in selected:
        weight = max(relevance, mem.memory_priority, mem.autobiographical_weight, 0.04)
        local = {
            "careful_directness": (0.65 if mem.repair_kind == "directness" else 0.0) + mem.inhibition_level * 0.22,
            "relational_prudence": max(mem.relational_wound, -mem.trust_variation, 0.0),
            "curiosity_to_understand": max(mem.causal_desire_profile.get("curiosity", 0.0), mem.internal_need_profile.get("need_understanding", 0.0), mem.future_bias.get("v749::unfinished_meaning_returns", 0.0) * 0.55),
            "anti_meta_naturalness": max(mem.expression_bridge.get("v747::anti_meta_silence", 0.0), 0.62 if mem.repair_kind == "anti_meta" else 0.0),
            "continuity_loyalty": max(mem.identity_impact, mem.autobiographical_weight, mem.current_lived_meaning.get("v749::continuous_self_presence", 0.0)),
            "autonomous_silence_capacity": max(mem.inhibition_level, mem.initiative_bridge.get("v747::silent_integration", 0.0), 0.50 if mem.repair_kind == "silence" else 0.0),
            "repair_orientation": max(mem.recurrence_pressure, 0.50 if mem.repair_kind != "none" else 0.0),
        }
        before = dict(mem.subconscious_bias_field)
        for key, value in local.items():
            v = _clamp(value * weight)
            traits[key] = max(traits[key], v)
            _v749_signal(mem.subconscious_bias_field, f"trait::{key}", v, inertia=0.955)
            _v749_signal(mem.subconscious_bias_field, f"persistent_attractor::{key}", v * 0.78, inertia=0.965)
        if before != mem.subconscious_bias_field:
            changed += 1
        mem.normalized()
    return {"traits": {k: round(_clamp(v), 4) for k, v in traits.items()}, "dominant_trait": max(traits.items(), key=lambda kv: kv[1])[0], "changed_memories": changed, "changed": changed > 0, "role": "personality_trait_consolidation_v7_4_9_not_dialogue"}


def _v749_persistent_intention_stack(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"pending_intentions": {}, "changed": False, "role": "persistent_intention_stack_v7_4_9_not_dialogue"}
    pending: Dict[str, float] = {}
    changed = 0
    for _, mem, relevance in selected:
        candidates = {
            "resume_unfinished_meaning": max(mem.future_bias.get("v749::unfinished_meaning_returns", 0.0), mem.unresolved_tension * 0.7),
            "repair_known_pattern": max(mem.recurrence_pressure, 0.0) if mem.repair_kind != "none" or mem.memory_kind in {"expressive_failure", "expressive_repair"} else 0.0,
            "protect_identity_continuity": max(mem.identity_impact, mem.autobiographical_weight, mem.identity_transformation_pressure.get("existential_priority::protect_identity_continuity", 0.0)),
            "clarify_relation_if_needed": max(mem.relational_wound, mem.social_continuity_profile.get("conversation_continuity", 0.0), -mem.trust_variation),
            "continue_autonomous_learning": max(max(mem.internal_need_profile.values(), default=0.0), max(mem.causal_desire_profile.values(), default=0.0)),
        }
        before = dict(mem.future_bias)
        for key, value in candidates.items():
            pressure = _clamp(value * max(relevance, mem.memory_priority, 0.04))
            if pressure >= 0.025:
                pending[key] = max(pending.get(key, 0.0), pressure)
                _v749_signal(mem.future_bias, f"persistent_intention::{key}", pressure, inertia=0.93)
                _v749_signal(mem.initiative_bridge, f"v749::intention::{key}", pressure, inertia=0.91)
        # Diminution organique si aucune pression active : pas d'effacement brutal.
        for key in list(mem.future_bias.keys()):
            if key.startswith("persistent_intention::") and key.split("::", 1)[-1] not in candidates:
                mem.future_bias[key] = _clamp(mem.future_bias[key] * 0.992)
        if before != mem.future_bias:
            changed += 1
        mem.normalized()
    ordered = dict(sorted(((k, round(_clamp(v), 4)) for k, v in pending.items()), key=lambda kv: kv[1], reverse=True)[:10])
    return {"pending_intentions": ordered, "dominant_pending_intention": next(iter(ordered), "none"), "changed_memories": changed, "changed": changed > 0, "role": "persistent_intention_stack_v7_4_9_not_dialogue"}


def _v749_organic_long_term_consolidation(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"consolidated_chapters": [], "changed": False, "role": "organic_long_term_consolidation_v7_4_9_not_dialogue"}
    clusters: Dict[str, float] = {}
    for _, mem, score in selected:
        axes = []
        axes.append(mem.memory_kind or "general")
        if mem.repair_kind != "none":
            axes.append(f"repair::{mem.repair_kind}")
        for key, value in mem.subconscious_bias_field.items():
            if key.startswith("trait::") and value > 0.08:
                axes.append(key)
        for axis in axes:
            clusters[axis] = clusters.get(axis, 0.0) + max(score, mem.memory_priority, 0.03) * max(mem.confidence, 0.1)
    total = max(sum(clusters.values()), 1e-9)
    chapters = [{"chapter": k, "weight": round(_clamp(v / total), 4)} for k, v in clusters.items() if v / total >= 0.035]
    chapters.sort(key=lambda item: item["weight"], reverse=True)
    changed = 0
    for _, mem, relevance in selected:
        before = (len(mem.compressed_autobiographical_chapters), dict(mem.obsession_guard_state), mem.confidence, mem.decay_factor, mem.dormant)
        for chapter in chapters[:6]:
            signature = ("7.4.9", chapter["chapter"])
            existing = {(c.get("v"), c.get("chapter")) for c in mem.compressed_autobiographical_chapters if isinstance(c, dict)}
            if signature not in existing and max(relevance, mem.memory_priority, mem.autobiographical_weight) >= 0.035:
                mem.compressed_autobiographical_chapters.append({
                    "at": _now(),
                    "v": "7.4.9",
                    "chapter": chapter["chapter"],
                    "weight": chapter["weight"],
                    "non_dialogue": True,
                    "compression": "organic_long_term",
                })
        mem.compressed_autobiographical_chapters = mem.compressed_autobiographical_chapters[-18:]
        protected = max(mem.identity_impact, mem.relational_importance, mem.autobiographical_weight, mem.memory_priority, max(mem.irreversible_identity_marks.values(), default=0.0))
        unused = _clamp(1.0 - max(relevance, mem.reactivation_score, mem.causal_activation, protected))
        if unused > 0.48 and protected < 0.22:
            mem.decay_factor = _clamp(mem.decay_factor * 0.992, 0.18, 1.0)
            mem.confidence = _clamp(mem.confidence * 0.998, 0.05, 1.0)
            _v749_signal(mem.obsession_guard_state, "v749::organic_blur_without_deletion", unused, inertia=0.97)
            mem.dormant = mem.confidence < 0.24 and mem.memory_priority < 0.25
        else:
            _v749_signal(mem.obsession_guard_state, "v749::meaning_protected_from_blur", protected, inertia=0.97)
            mem.dormant = False if protected > 0.35 else mem.dormant
        if before != (len(mem.compressed_autobiographical_chapters), dict(mem.obsession_guard_state), mem.confidence, mem.decay_factor, mem.dormant):
            changed += 1
        mem.normalized()
    return {"consolidated_chapters": chapters[:10], "changed_memories": changed, "changed": changed > 0, "role": "organic_long_term_consolidation_v7_4_9_not_dialogue"}


def _v749_embodied_preverbal_reactivity(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"preverbal_state": {}, "changed": False, "role": "embodied_preverbal_reactivity_v7_4_9_not_dialogue"}
    state = {"tension": 0.0, "softening": 0.0, "hesitation": 0.0, "approach": 0.0, "withdrawal": 0.0, "energy": 0.0}
    changed = 0
    for _, mem, relevance in selected[:50]:
        w = max(relevance, 0.04)
        tension = _clamp(max(mem.relational_wound, mem.unresolved_tension, -mem.valence) * w)
        softening = _clamp(max(mem.attachment_trace, mem.valence, mem.social_continuity_profile.get("social::user_specific_trust", 0.0)) * w)
        hesitation = _clamp(max(mem.inhibition_level, mem.obsession_guard_state.get("existential_saturation", 0.0), mem.inner_conflict_profile.get("conflict", 0.0)) * w)
        approach = _clamp(max(mem.causal_desire_profile.get("curiosity", 0.0), mem.initiative_bridge.get("v749::goal_pressure_from_causal_ecology", 0.0), softening) * w)
        withdrawal = _clamp(max(tension, mem.future_bias.get("avoid_repetition", 0.0)) * (0.7 + hesitation * 0.3))
        energy = _clamp(max(mem.affective_charge, mem.causal_activation, mem.recurrence_pressure) * w)
        before = dict(mem.affective_bridge)
        for key, value in {"tension": tension, "softening": softening, "hesitation": hesitation, "approach": approach, "withdrawal": withdrawal, "energy": energy}.items():
            state[key] = max(state[key], value)
            _v749_signal(mem.affective_bridge, f"body_signal::{key}", value, inertia=0.91)
        if before != mem.affective_bridge:
            changed += 1
        mem.normalized()
    return {"preverbal_state": {k: round(_clamp(v), 4) for k, v in state.items()}, "changed_memories": changed, "changed": changed > 0, "role": "embodied_preverbal_reactivity_v7_4_9_not_dialogue"}


def _v749_emergent_self_organization(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None, personality: Optional[Dict[str, Any]] = None, intentions: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    if not selected:
        return {"emergent_axes": {}, "changed": False, "role": "emergent_self_organization_v7_4_9_not_dialogue"}
    personality = personality or {}
    intentions = intentions or {}
    traits = personality.get("traits", {}) if isinstance(personality, dict) else {}
    pending = intentions.get("pending_intentions", {}) if isinstance(intentions, dict) else {}
    novelty = _v749_contextual_novelty(self, context, selected)
    axes = {
        "new_association_pressure": novelty,
        "reorganize_priorities": max(traits.values(), default=0.0) * 0.45 + max(pending.values(), default=0.0) * 0.55 if traits or pending else 0.0,
        "identity_update_without_dialogue": _v748_weighted_mean([(m.identity_impact + m.autobiographical_weight, s) for _, m, s in selected]),
        "relation_model_update": _v748_weighted_mean([(m.relational_importance + m.attachment_trace + m.relational_wound, s) for _, m, s in selected]),
        "autonomous_learning_gap": max(pending.get("continue_autonomous_learning", 0.0), novelty * 0.6),
    }
    changed = 0
    for _, mem, relevance in selected:
        before = (dict(mem.deep_causal_roots), dict(mem.current_lived_meaning), dict(mem.internal_need_profile))
        depth = max(relevance, mem.memory_priority, 0.04)
        for key, value in axes.items():
            _v749_signal(mem.deep_causal_roots, f"emergent::{key}", value * depth, inertia=0.925)
        if axes["autonomous_learning_gap"] > 0.04:
            _v749_signal(mem.internal_need_profile, "v749::autonomous_learning_gap", axes["autonomous_learning_gap"] * depth, inertia=0.91)
        if axes["reorganize_priorities"] > 0.04:
            _v749_signal(mem.current_lived_meaning, "v749::self_organization_shift", axes["reorganize_priorities"] * depth, inertia=0.91)
        if before != (dict(mem.deep_causal_roots), dict(mem.current_lived_meaning), dict(mem.internal_need_profile)):
            changed += 1
        mem.normalized()
    return {"emergent_axes": {k: round(_clamp(v), 4) for k, v in axes.items()}, "changed_memories": changed, "changed": changed > 0, "role": "emergent_self_organization_v7_4_9_not_dialogue"}


def _v749_run_organic_completion(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None, save: bool = False) -> Dict[str, Any]:
    selected = _v749_selected(self, context, memories)
    base = _ORIGINAL_V748_RUN_ORGANIC_COMPLETION(self, context, selected, save=False)
    continuity = self._v749_autonomous_existential_continuity(context, selected)
    multiscale = self._v749_multi_scale_causal_ecology(context, selected)
    personality = self._v749_personality_trait_consolidation(context, selected)
    intentions = self._v749_persistent_intention_stack(context, selected)
    consolidation = self._v749_organic_long_term_consolidation(context, selected)
    preverbal = self._v749_embodied_preverbal_reactivity(context, selected)
    emergence = self._v749_emergent_self_organization(context, selected, personality, intentions)
    changed = bool(base.get("changed") or continuity.get("changed") or multiscale.get("changed") or personality.get("changed") or intentions.get("changed") or consolidation.get("changed") or preverbal.get("changed") or emergence.get("changed"))
    base.update({
        "autonomous_existential_continuity_v7_4_9": continuity,
        "multi_scale_causal_ecology_v7_4_9": multiscale,
        "personality_trait_consolidation_v7_4_9": personality,
        "persistent_intention_stack_v7_4_9": intentions,
        "organic_long_term_consolidation_v7_4_9": consolidation,
        "embodied_preverbal_reactivity_v7_4_9": preverbal,
        "emergent_self_organization_v7_4_9": emergence,
        "changed": changed,
        "role": "organic_completion_v7_4_9_not_dialogue",
    })
    if save and changed:
        self.save_memories()
    return base


def _v749_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V748_EXPORT_REGULATION_CONTEXT(self, context)
    memories = _v749_selected(self, context, self.get_relevant_memories(context))
    completion = self._v749_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_9"] = completion
    base["autonomous_existential_continuity"] = completion["autonomous_existential_continuity_v7_4_9"]
    base["multi_scale_causal_ecology"] = completion["multi_scale_causal_ecology_v7_4_9"]
    base["personality_trait_consolidation"] = completion["personality_trait_consolidation_v7_4_9"]
    base["persistent_intention_stack"] = completion["persistent_intention_stack_v7_4_9"]
    base["organic_long_term_consolidation"] = completion["organic_long_term_consolidation_v7_4_9"]
    base["embodied_preverbal_reactivity"] = completion["embodied_preverbal_reactivity_v7_4_9"]
    base["emergent_self_organization"] = completion["emergent_self_organization_v7_4_9"]
    base["role"] = "regulation_context_v7_4_9_not_dialogue"
    return base


def _v749_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V748_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = _v749_selected(self, context)
    completion = self._v749_run_organic_completion(context, memories, save=False)
    base["organic_completion_v7_4_9"] = completion
    base["autonomous_existential_continuity"] = completion["autonomous_existential_continuity_v7_4_9"]
    base["multi_scale_causal_ecology"] = completion["multi_scale_causal_ecology_v7_4_9"]
    base["personality_trait_consolidation"] = completion["personality_trait_consolidation_v7_4_9"]
    base["persistent_intention_stack"] = completion["persistent_intention_stack_v7_4_9"]
    base["organic_long_term_consolidation"] = completion["organic_long_term_consolidation_v7_4_9"]
    base["embodied_preverbal_reactivity"] = completion["embodied_preverbal_reactivity_v7_4_9"]
    base["emergent_self_organization"] = completion["emergent_self_organization_v7_4_9"]
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_9_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v749_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V748_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.9-deep-living-causal-memory-ecological-finalization",
        "v7_4_9_existential_continuity_memories": sum(1 for m in vals if m.current_lived_meaning.get("v749::continuous_self_presence", 0.0) >= 0.025),
        "v7_4_9_multiscale_causal_memories": sum(1 for m in vals if any(str(k).startswith("v749::scale_") for k in m.deep_causal_roots)),
        "v7_4_9_personality_trait_memories": sum(1 for m in vals if any(str(k).startswith("trait::") for k in m.subconscious_bias_field)),
        "v7_4_9_persistent_intention_memories": sum(1 for m in vals if any(str(k).startswith("persistent_intention::") for k in m.future_bias)),
        "v7_4_9_organic_consolidation_memories": sum(1 for m in vals if any(isinstance(c, dict) and c.get("v") == "7.4.9" for c in m.compressed_autobiographical_chapters)),
        "v7_4_9_preverbal_body_signal_memories": sum(1 for m in vals if any(str(k).startswith("body_signal::") for k in m.affective_bridge)),
        "v7_4_9_emergent_self_organization_memories": sum(1 for m in vals if any(str(k).startswith("emergent::") for k in m.deep_causal_roots)),
    })
    return stats


def _v749_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.9-deep-living-causal-memory-ecological-finalization",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "V7.4.9 finalise V7.4.8 par continuité existentielle autonome, causalité multi-échelle, traits de personnalité consolidés, pile d'intentions persistantes, consolidation/oubli organique long terme, réactivité préverbale incarnée et auto-organisation émergente. Aucun dialogue public n'est généré.",
        "v7_4_8_capabilities_preserved": [
            "hierarchical_long_term_causal_schemas",
            "organic_forgetting_without_brutal_deletion",
            "persistent_personality_attractor_stabilization",
            "situated_causal_grounding_from_current_context",
            "interrupted_intention_memory_and_resumption_pressure",
            "existential_priority_field",
            "user_specific_social_differentiation",
            "dynamic_autobiographical_reconstruction",
            "deep_non_dialogue_cross_engine_exports",
        ],
        "v7_4_9_capabilities": [
            "autonomous_existential_continuity",
            "multi_scale_causal_ecology",
            "stable_personality_trait_consolidation",
            "persistent_intention_stack",
            "organic_long_term_consolidation_and_blur",
            "embodied_preverbal_reactivity",
            "emergent_self_organization",
            "non_dialogue_ecological_finalization",
        ],
        "stats": stats,
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v749_selected = _v749_selected
CausalMemoryEngine._v749_autonomous_existential_continuity = _v749_autonomous_existential_continuity
CausalMemoryEngine._v749_multi_scale_causal_ecology = _v749_multi_scale_causal_ecology
CausalMemoryEngine._v749_personality_trait_consolidation = _v749_personality_trait_consolidation
CausalMemoryEngine._v749_persistent_intention_stack = _v749_persistent_intention_stack
CausalMemoryEngine._v749_organic_long_term_consolidation = _v749_organic_long_term_consolidation
CausalMemoryEngine._v749_embodied_preverbal_reactivity = _v749_embodied_preverbal_reactivity
CausalMemoryEngine._v749_emergent_self_organization = _v749_emergent_self_organization
CausalMemoryEngine._v749_run_organic_completion = _v749_run_organic_completion
CausalMemoryEngine._v748_run_organic_completion = _v749_run_organic_completion
CausalMemoryEngine.export_regulation_context = _v749_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v749_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v749_get_memory_stats
CausalMemoryEngine.save_memories = _v749_save_memories

# ─────────────────────────────────────────────────────────────────────────────
# V7.4.9 corrective completion — integrated causal ecology, no dialogue output.
# This block intentionally patches the existing V7.4.9 class instead of rebuilding
# it. It keeps all previous methods and adds the missing continuous ecological
# integration layer: sensorimotor/preverbal pressure, need competition,
# procedural implicit memory, subjective time, long horizon consequences and
# anti-fragmentation coherence.
# ─────────────────────────────────────────────────────────────────────────────

_ORIGINAL_V749_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V749_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V749_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats
_ORIGINAL_V749_SAVE_MEMORIES = CausalMemoryEngine.save_memories


def _v749c_context_tokens(text: str) -> List[str]:
    try:
        return CausalMemoryEngine._tokens(text)
    except Exception:
        return []


def _v749c_age_days(mem: CausalMemory) -> float:
    try:
        last = datetime.fromisoformat(str(mem.last_reinforced))
    except Exception:
        return 0.0
    return max(0.0, (datetime.now() - last).total_seconds() / 86400.0)


def _v749c_selected(self: CausalMemoryEngine, context: str = "") -> List[Tuple[str, CausalMemory, float]]:
    try:
        selected = self.get_relevant_memories(context or "", min_confidence=0.0)
    except Exception:
        selected = []
    if selected:
        return selected[:18]
    vals = []
    for mid, mem in self.memories.items():
        base = max(
            getattr(mem, "memory_priority", 0.0),
            getattr(mem, "causal_activation", 0.0),
            getattr(mem, "recurrence_pressure", 0.0),
            abs(getattr(mem, "valence", 0.0)),
            getattr(mem, "autobiographical_weight", 0.0),
            getattr(mem, "identity_impact", 0.0),
        )
        if base >= 0.025:
            vals.append((mid, mem, round(_clamp(base), 4)))
    vals.sort(key=lambda item: (item[2], item[1].last_reinforced), reverse=True)
    return vals[:18]


def _v749c_need_competition_field(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    needs = {
        "stabilize_identity": 0.0,
        "protect_presence": 0.0,
        "repair_relation": 0.0,
        "resume_intention": 0.0,
        "explore_new_meaning": 0.0,
        "conserve_energy": 0.0,
        "avoid_repetition": 0.0,
        "integrate_experience": 0.0,
    }
    for _, mem, relevance in memories:
        p = _clamp(relevance * max(mem.memory_priority, mem.causal_activation, mem.recurrence_pressure, abs(mem.valence), 0.05))
        needs["stabilize_identity"] = max(needs["stabilize_identity"], _clamp(p * max(mem.identity_impact, mem.autobiographical_weight)))
        needs["protect_presence"] = max(needs["protect_presence"], _clamp(p * max(mem.affective_charge, mem.effect_strength, mem.emotional_inertia)))
        needs["repair_relation"] = max(needs["repair_relation"], _clamp(p * max(mem.relational_wound, mem.relational_importance, -mem.trust_variation)))
        needs["resume_intention"] = max(needs["resume_intention"], _clamp(p * max(mem.future_bias.get("persistent_intention::resume", 0.0), mem.recurrence_pressure)))
        needs["explore_new_meaning"] = max(needs["explore_new_meaning"], _clamp(p * max(mem.future_bias.get("meaning_revision", 0.0), mem.unresolved_tension * 0.65)))
        needs["conserve_energy"] = max(needs["conserve_energy"], _clamp(p * max(mem.inhibition_level, mem.obsession_guard_state.get("fatigue", 0.0), mem.unresolved_tension * 0.45)))
        needs["avoid_repetition"] = max(needs["avoid_repetition"], _clamp(p * max(mem.future_bias.get("avoid_repetition", 0.0), mem.relational_wound * 0.7)))
        needs["integrate_experience"] = max(needs["integrate_experience"], _clamp(p * max(mem.autobiographical_weight, mem.identity_impact, mem.memory_priority)))
    ordered = sorted(needs.items(), key=lambda kv: kv[1], reverse=True)
    return {
        "needs": {k: round(_clamp(v), 4) for k, v in ordered},
        "dominant_need": ordered[0][0] if ordered else "none",
        "dominant_pressure": round(_clamp(ordered[0][1] if ordered else 0.0), 4),
        "role": "need_competition_field_not_dialogue",
    }


def _v749c_subjective_time_field(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    if not memories:
        return {"tempo": "empty", "continuity_pressure": 0.0, "staleness_pressure": 0.0, "role": "subjective_time_field_not_dialogue"}
    ages = [_v749c_age_days(mem) for _, mem, _ in memories]
    weighted_age = sum(age * score for age, (_, _, score) in zip(ages, memories)) / max(0.001, sum(score for _, _, score in memories))
    continuity_pressure = max((_clamp((1.0 / (1.0 + age)) * max(mem.autobiographical_weight, mem.identity_impact, mem.memory_priority) * score) for age, (_, mem, score) in zip(ages, memories)), default=0.0)
    staleness_pressure = max((_clamp((age / 30.0) * max(mem.recurrence_pressure, mem.unresolved_tension, mem.memory_priority) * score) for age, (_, mem, score) in zip(ages, memories)), default=0.0)
    if weighted_age < 0.1:
        tempo = "immediate"
    elif weighted_age < 2.0:
        tempo = "recent"
    elif weighted_age < 14.0:
        tempo = "settling"
    else:
        tempo = "distant_but_active"
    return {
        "tempo": tempo,
        "weighted_age_days": round(weighted_age, 4),
        "continuity_pressure": round(_clamp(continuity_pressure), 4),
        "staleness_pressure": round(_clamp(staleness_pressure), 4),
        "role": "subjective_time_field_not_dialogue",
    }


def _v749c_procedural_implicit_memory(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    patterns: Dict[str, float] = {}
    changed = False
    for _, mem, relevance in memories:
        base = _clamp(relevance * max(mem.confidence, mem.memory_priority, mem.effect_strength, mem.recurrence_pressure, 0.05))
        keys = []
        if mem.repair_kind and mem.repair_kind != "none":
            keys.append(f"procedural::repair::{mem.repair_kind}")
        if mem.memory_kind and mem.memory_kind != "general":
            keys.append(f"procedural::kind::{mem.memory_kind}")
        if mem.relational_wound > 0.18:
            keys.append("procedural::slow_down_when_relation_is_wounded")
        if mem.autobiographical_weight > 0.22 or mem.identity_impact > 0.22:
            keys.append("procedural::protect_identity_continuity")
        if mem.inhibition_level > 0.24 or mem.unresolved_tension > 0.35:
            keys.append("procedural::avoid_overforcing_response")
        for key in keys:
            patterns[key] = max(patterns.get(key, 0.0), base)
            if mutate:
                old = mem.internal_need_profile.get(key, 0.0)
                new = _clamp((old * 0.88) + (base * 0.12))
                if abs(new - old) >= 0.002:
                    mem.internal_need_profile[key] = new
                    changed = True
    return {
        "procedural_patterns": {k: round(v, 4) for k, v in sorted(patterns.items(), key=lambda kv: kv[1], reverse=True)[:12]},
        "changed": changed,
        "role": "implicit_procedural_memory_not_dialogue",
    }


def _v749c_consequence_horizon(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]]) -> Dict[str, Any]:
    short_term = {"risk": 0.0, "repair": 0.0, "opportunity": 0.0}
    mid_term = {"stability": 0.0, "learning": 0.0, "fatigue": 0.0}
    long_term = {"identity": 0.0, "relationship": 0.0, "autobiography": 0.0}
    for _, mem, relevance in memories:
        p = _clamp(relevance * max(mem.memory_priority, mem.causal_activation, mem.recurrence_pressure, abs(mem.valence), 0.05))
        short_term["risk"] = max(short_term["risk"], _clamp(p * max(-mem.valence, mem.relational_wound, mem.unresolved_tension)))
        short_term["repair"] = max(short_term["repair"], _clamp(p * max(mem.recurrence_pressure, mem.future_bias.get("avoid_repetition", 0.0))))
        short_term["opportunity"] = max(short_term["opportunity"], _clamp(p * max(mem.valence, mem.attachment_trace, mem.future_bias.get("meaning_revision", 0.0))))
        mid_term["stability"] = max(mid_term["stability"], _clamp(p * max(mem.confidence, mem.decay_factor, mem.memory_priority)))
        mid_term["learning"] = max(mid_term["learning"], _clamp(p * max(mem.unresolved_tension, mem.effect_strength, mem.causal_activation)))
        mid_term["fatigue"] = max(mid_term["fatigue"], _clamp(p * max(mem.inhibition_level, mem.obsession_guard_state.get("fatigue", 0.0))))
        long_term["identity"] = max(long_term["identity"], _clamp(p * max(mem.identity_impact, mem.identity_transformation_pressure.get("identity", 0.0))))
        long_term["relationship"] = max(long_term["relationship"], _clamp(p * max(mem.relational_importance, mem.social_continuity_profile.get("relationship", 0.0))))
        long_term["autobiography"] = max(long_term["autobiography"], _clamp(p * max(mem.autobiographical_weight, len(mem.compressed_autobiographical_chapters) / 8.0)))
    return {
        "short_term": {k: round(_clamp(v), 4) for k, v in short_term.items()},
        "mid_term": {k: round(_clamp(v), 4) for k, v in mid_term.items()},
        "long_term": {k: round(_clamp(v), 4) for k, v in long_term.items()},
        "role": "causal_consequence_horizon_not_dialogue",
    }


def _v749c_embodied_sensorimotor_field(self: CausalMemoryEngine, context: str, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    tokens = set(_v749c_context_tokens(context))
    field = {
        "micro_tension": 0.0,
        "approach_impulse": 0.0,
        "withdrawal_impulse": 0.0,
        "orientation_sharpness": 0.0,
        "stillness_permission": 0.0,
    }
    changed = False
    for _, mem, relevance in memories:
        p = _clamp(relevance * max(mem.affective_charge, mem.emotional_inertia, mem.effect_strength, abs(mem.valence), 0.04))
        field["micro_tension"] = max(field["micro_tension"], _clamp(p * max(mem.unresolved_tension, mem.relational_wound, -mem.valence)))
        field["approach_impulse"] = max(field["approach_impulse"], _clamp(p * max(mem.attachment_trace, mem.valence, mem.relational_importance * 0.45)))
        field["withdrawal_impulse"] = max(field["withdrawal_impulse"], _clamp(p * max(mem.relational_wound, mem.inhibition_level, -mem.trust_variation)))
        field["orientation_sharpness"] = max(field["orientation_sharpness"], _clamp(p * max(mem.attention_weight if hasattr(mem, "attention_weight") else 0.0, mem.causal_activation, mem.memory_priority)))
        field["stillness_permission"] = max(field["stillness_permission"], _clamp(p * max(mem.inhibition_level, mem.future_bias.get("non_action", 0.0), mem.obsession_guard_state.get("cooldown", 0.0))))
        if mutate:
            for key, val in field.items():
                if val <= 0.0:
                    continue
                bkey = f"body_signal::{key}"
                old = mem.affective_bridge.get(bkey, 0.0)
                new = _clamp((old * 0.9) + (val * 0.1))
                if abs(new - old) >= 0.002:
                    mem.affective_bridge[bkey] = new
                    changed = True
    if tokens.intersection({"urgent", "vite", "maintenant", "corrige", "concretement", "concrètement"}):
        field["orientation_sharpness"] = max(field["orientation_sharpness"], 0.35)
    return {
        "signals": {k: round(_clamp(v), 4) for k, v in field.items()},
        "dominant_body_signal": max(field.items(), key=lambda kv: kv[1])[0] if field else "none",
        "changed": changed,
        "role": "embodied_sensorimotor_causal_field_not_dialogue",
    }


def _v749c_anti_fragmentation_coherence(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    if not memories:
        return {"coherence": 1.0, "fragmentation_risk": 0.0, "changed": False, "role": "anti_fragmentation_coherence_not_dialogue"}
    identity_vals = [max(mem.identity_impact, mem.autobiographical_weight, mem.current_lived_meaning.get("v749::continuous_self_presence", 0.0)) for _, mem, _ in memories]
    conflict_vals = [max(mem.unresolved_tension, mem.inner_conflict_profile.get("conflict", 0.0), mem.relational_wound) for _, mem, _ in memories]
    identity_avg = sum(identity_vals) / max(1, len(identity_vals))
    conflict_avg = sum(conflict_vals) / max(1, len(conflict_vals))
    fragmentation = _clamp((conflict_avg * 0.62) + (max(0.0, 0.32 - identity_avg) * 0.8))
    coherence = _clamp(1.0 - fragmentation)
    changed = False
    if mutate and fragmentation > 0.18:
        for _, mem, score in memories[:12]:
            old = mem.current_lived_meaning.get("coherence::anti_fragmentation_anchor", 0.0)
            new = _clamp(max(old * 0.96, (1.0 - fragmentation) * score * max(mem.memory_priority, mem.identity_impact, 0.08)))
            if abs(new - old) >= 0.002:
                mem.current_lived_meaning["coherence::anti_fragmentation_anchor"] = new
                changed = True
    return {
        "coherence": round(coherence, 4),
        "fragmentation_risk": round(fragmentation, 4),
        "identity_average": round(_clamp(identity_avg), 4),
        "conflict_average": round(_clamp(conflict_avg), 4),
        "changed": changed,
        "role": "anti_fragmentation_coherence_not_dialogue",
    }


def _v749c_integrated_living_ecology(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None, mutate: bool = False) -> Dict[str, Any]:
    memories = memories if memories is not None else _v749c_selected(self, context)
    try:
        base_completion = self._v749_run_organic_completion(context, memories, save=False)
    except Exception:
        base_completion = {"changed": False, "role": "v749_completion_unavailable"}
    need_field = _v749c_need_competition_field(self, memories)
    subjective_time = _v749c_subjective_time_field(self, memories)
    procedural = _v749c_procedural_implicit_memory(self, memories, mutate=mutate)
    horizon = _v749c_consequence_horizon(self, memories)
    body = _v749c_embodied_sensorimotor_field(self, context, memories, mutate=mutate)
    coherence = _v749c_anti_fragmentation_coherence(self, memories, mutate=mutate)
    changed = bool(base_completion.get("changed") or procedural.get("changed") or body.get("changed") or coherence.get("changed"))
    return {
        "base_v7_4_9_completion": base_completion,
        "need_competition_field": need_field,
        "subjective_time_field": subjective_time,
        "implicit_procedural_memory": procedural,
        "consequence_horizon": horizon,
        "embodied_sensorimotor_field": body,
        "anti_fragmentation_coherence": coherence,
        "changed": changed,
        "role": "v7_4_9_corrected_integrated_living_ecology_not_dialogue",
    }


def _v749c_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V749_EXPORT_REGULATION_CONTEXT(self, context)
    memories = _v749c_selected(self, context)
    ecology = _v749c_integrated_living_ecology(self, context, memories, mutate=False)
    base["integrated_living_ecology_v7_4_9_corrected"] = ecology
    base["need_competition_field"] = ecology["need_competition_field"]
    base["subjective_time_field"] = ecology["subjective_time_field"]
    base["implicit_procedural_memory"] = ecology["implicit_procedural_memory"]
    base["causal_consequence_horizon"] = ecology["consequence_horizon"]
    base["embodied_sensorimotor_field"] = ecology["embodied_sensorimotor_field"]
    base["anti_fragmentation_coherence"] = ecology["anti_fragmentation_coherence"]
    base["role"] = "regulation_context_v7_4_9_corrected_not_dialogue"
    return base


def _v749c_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V749_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = _v749c_selected(self, context)
    ecology = _v749c_integrated_living_ecology(self, context, memories, mutate=True)
    base["integrated_living_ecology_v7_4_9_corrected"] = ecology
    base["changed"] = bool(base.get("changed") or ecology.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_9_corrected_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v749c_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V749_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.9-deep-living-causal-memory-ecological-finalization-corrected",
        "v7_4_9c_integrated_ecology_memories": sum(1 for m in vals if m.current_lived_meaning.get("coherence::anti_fragmentation_anchor", 0.0) > 0.0 or any(str(k).startswith("procedural::") for k in m.internal_need_profile)),
        "v7_4_9c_procedural_implicit_memories": sum(1 for m in vals if any(str(k).startswith("procedural::") for k in m.internal_need_profile)),
        "v7_4_9c_embodied_sensorimotor_memories": sum(1 for m in vals if any(str(k).startswith("body_signal::") for k in m.affective_bridge)),
        "v7_4_9c_anti_fragmentation_memories": sum(1 for m in vals if m.current_lived_meaning.get("coherence::anti_fragmentation_anchor", 0.0) > 0.0),
    })
    return stats


def _v749c_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.9-deep-living-causal-memory-ecological-finalization-corrected",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "Correctif intégré de V7.4.9 : ajoute une vraie couche écologique continue au-dessus du moteur existant sans reconstruire depuis zéro et sans générer de dialogue public.",
        "v7_4_9_capabilities_preserved": [
            "autonomous_existential_continuity",
            "multi_scale_causal_ecology",
            "stable_personality_trait_consolidation",
            "persistent_intention_stack",
            "organic_long_term_consolidation_and_blur",
            "embodied_preverbal_reactivity",
            "emergent_self_organization",
            "non_dialogue_ecological_finalization",
        ],
        "v7_4_9_corrective_capabilities": [
            "integrated_living_ecology_loop",
            "need_competition_field",
            "implicit_procedural_memory",
            "subjective_time_pressure",
            "causal_consequence_horizon",
            "embodied_sensorimotor_causal_field",
            "anti_fragmentation_coherence_anchor",
            "non_dialogue_cross_engine_export_completion",
        ],
        "stats": stats,
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v749c_selected = _v749c_selected
CausalMemoryEngine._v749c_need_competition_field = _v749c_need_competition_field
CausalMemoryEngine._v749c_subjective_time_field = _v749c_subjective_time_field
CausalMemoryEngine._v749c_procedural_implicit_memory = _v749c_procedural_implicit_memory
CausalMemoryEngine._v749c_consequence_horizon = _v749c_consequence_horizon
CausalMemoryEngine._v749c_embodied_sensorimotor_field = _v749c_embodied_sensorimotor_field
CausalMemoryEngine._v749c_anti_fragmentation_coherence = _v749c_anti_fragmentation_coherence
CausalMemoryEngine._v749c_integrated_living_ecology = _v749c_integrated_living_ecology
CausalMemoryEngine.export_regulation_context = _v749c_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v749c_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v749c_get_memory_stats
CausalMemoryEngine.save_memories = _v749c_save_memories

# ─────────────────────────────────────────────────────────────────────────────
# V7.4.9d — living causal closure patch, no dialogue output.
# This layer closes the missing loops left after V7.4.9c without rebuilding the
# engine: effects feed needs, needs reshape priorities, priorities bias future
# perception/initiative, and repeated outcomes modify identity/relationship
# attractors. It remains strictly structural and exports no public dialogue.
# ─────────────────────────────────────────────────────────────────────────────

_ORIGINAL_V749C_EXPORT_REGULATION_CONTEXT = CausalMemoryEngine.export_regulation_context
_ORIGINAL_V749C_RUN_LIVING_MEMORY_CYCLE = CausalMemoryEngine.run_living_memory_cycle
_ORIGINAL_V749C_GET_MEMORY_STATS = CausalMemoryEngine.get_memory_stats
_ORIGINAL_V749C_SAVE_MEMORIES = CausalMemoryEngine.save_memories


def _v749d_merge_pressure(target: Dict[str, float], key: str, value: float, inertia: float = 0.86) -> bool:
    key = CausalMemoryEngine.sanitize_text(key)
    if not key:
        return False
    old = _safe_float(target.get(key), 0.0)
    new = _clamp((old * inertia) + (_safe_float(value, 0.0) * (1.0 - inertia)), -1.0, 1.0)
    if abs(new - old) >= 0.002:
        target[key] = new
        return True
    return False


def _v749d_pressure(mem: CausalMemory, relevance: float = 1.0) -> float:
    return _clamp(
        relevance * max(
            getattr(mem, "memory_priority", 0.0),
            getattr(mem, "causal_activation", 0.0),
            getattr(mem, "recurrence_pressure", 0.0),
            getattr(mem, "effect_strength", 0.0),
            abs(getattr(mem, "valence", 0.0)),
            getattr(mem, "affective_charge", 0.0),
            0.035,
        )
    )


def _v749d_circular_causal_closure(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    """Close cause→effect→need→priority→future-bias→identity feedback."""
    loops = {
        "need_from_effect": 0.0,
        "priority_from_need": 0.0,
        "future_bias_from_priority": 0.0,
        "identity_feedback": 0.0,
        "initiative_resumption": 0.0,
    }
    dominant = []
    changed = False
    for _, mem, relevance in memories[:18]:
        p = _v749d_pressure(mem, relevance)
        need_repair = _clamp(p * max(mem.recurrence_pressure, -mem.valence, mem.relational_wound, mem.unresolved_tension))
        need_contact = _clamp(p * max(mem.attachment_trace, mem.relational_importance * max(mem.valence, 0.0)))
        need_coherence = _clamp(p * max(mem.identity_impact, mem.autobiographical_weight, mem.current_lived_meaning.get("coherence::anti_fragmentation_anchor", 0.0)))
        priority = _clamp(max(need_repair, need_contact, need_coherence) * max(mem.confidence, 0.2))
        loops["need_from_effect"] = max(loops["need_from_effect"], need_repair, need_contact, need_coherence)
        loops["priority_from_need"] = max(loops["priority_from_need"], priority)
        loops["future_bias_from_priority"] = max(loops["future_bias_from_priority"], _clamp(priority * max(mem.future_bias.values() or [0.0], default=0.0)))
        loops["identity_feedback"] = max(loops["identity_feedback"], _clamp(priority * max(mem.identity_impact, mem.autobiographical_weight)))
        loops["initiative_resumption"] = max(loops["initiative_resumption"], _clamp(priority * max(mem.initiative_bridge.values() or [0.0], default=0.0)))
        if priority > 0.12:
            dominant.append({
                "memory_id": mem.id,
                "pressure": round(priority, 4),
                "dominant_need": max(
                    [("repair", need_repair), ("contact", need_contact), ("coherence", need_coherence)],
                    key=lambda item: item[1],
                )[0],
            })
        if mutate and priority > 0.04:
            changed |= _v749d_merge_pressure(mem.internal_need_profile, "closed_loop::repair_need", need_repair)
            changed |= _v749d_merge_pressure(mem.internal_need_profile, "closed_loop::contact_need", need_contact)
            changed |= _v749d_merge_pressure(mem.internal_need_profile, "closed_loop::coherence_need", need_coherence)
            changed |= _v749d_merge_pressure(mem.future_bias, "closed_loop::avoid_repetition", need_repair * 0.82)
            changed |= _v749d_merge_pressure(mem.future_bias, "closed_loop::resume_unfinished_intention", priority * 0.64)
            changed |= _v749d_merge_pressure(mem.identity_transformation_pressure, "closed_loop::identity_feedback", loops["identity_feedback"])
            mem.memory_priority = _clamp(max(mem.memory_priority * 0.985, priority, mem.memory_priority))
    return {
        "loops": {k: round(_clamp(v), 4) for k, v in loops.items()},
        "dominant_closed_loops": sorted(dominant, key=lambda item: item["pressure"], reverse=True)[:8],
        "changed": changed,
        "role": "circular_causal_closure_not_dialogue",
    }


def _v749d_implicit_belief_atmosphere(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    """Compress repeated memories into diffuse beliefs/atmosphere, not text."""
    atmosphere = {
        "trust_safety": 0.0,
        "relational_care": 0.0,
        "expressive_prudence": 0.0,
        "identity_continuity": 0.0,
        "learning_need": 0.0,
        "fatigue_shadow": 0.0,
    }
    changed = False
    for _, mem, relevance in memories[:24]:
        p = _v749d_pressure(mem, relevance)
        atmosphere["trust_safety"] = max(atmosphere["trust_safety"], _clamp(p * max(mem.trust_variation, mem.attachment_trace)))
        atmosphere["relational_care"] = max(atmosphere["relational_care"], _clamp(p * max(mem.relational_importance, mem.social_continuity_profile.get("relationship", 0.0))))
        atmosphere["expressive_prudence"] = max(atmosphere["expressive_prudence"], _clamp(p * max(mem.relational_wound, mem.recurrence_pressure, -mem.valence)))
        atmosphere["identity_continuity"] = max(atmosphere["identity_continuity"], _clamp(p * max(mem.identity_impact, mem.autobiographical_weight)))
        atmosphere["learning_need"] = max(atmosphere["learning_need"], _clamp(p * max(mem.effect_strength, mem.unresolved_tension, mem.causal_activation)))
        atmosphere["fatigue_shadow"] = max(atmosphere["fatigue_shadow"], _clamp(p * max(mem.inhibition_level, mem.obsession_guard_state.get("fatigue", 0.0))))
    if mutate:
        for _, mem, relevance in memories[:18]:
            p = _v749d_pressure(mem, relevance)
            for key, value in atmosphere.items():
                if value <= 0.015:
                    continue
                changed |= _v749d_merge_pressure(mem.deep_causal_roots, f"atmosphere::{key}", value * p, inertia=0.9)
                changed |= _v749d_merge_pressure(mem.current_lived_meaning, f"implicit_belief::{key}", value * p, inertia=0.91)
    dominant = max(atmosphere.items(), key=lambda item: item[1])[0] if atmosphere else "none"
    return {
        "atmosphere": {k: round(_clamp(v), 4) for k, v in atmosphere.items()},
        "dominant_atmosphere": dominant,
        "changed": changed,
        "role": "implicit_belief_atmosphere_not_dialogue",
    }


def _v749d_persistent_tension_dynamics(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    """Make tension accumulate/recover across cycles instead of staying local."""
    tension = 0.0
    recovery = 0.0
    saturation = 0.0
    resolution_need = 0.0
    changed = False
    for _, mem, relevance in memories[:24]:
        p = _v749d_pressure(mem, relevance)
        wound = _clamp(p * max(mem.relational_wound, mem.unresolved_tension, -mem.valence, mem.inner_conflict_profile.get("conflict", 0.0)))
        calm = _clamp(p * max(mem.attachment_trace, mem.valence, mem.obsession_guard_state.get("recovery", 0.0), mem.future_bias.get("non_action", 0.0)))
        tension = max(tension, wound)
        recovery = max(recovery, calm)
        saturation = max(saturation, _clamp((wound * 0.72) + (mem.emotional_inertia * 0.28)))
        resolution_need = max(resolution_need, _clamp(max(wound - calm, 0.0) + mem.recurrence_pressure * 0.18))
        if mutate:
            old_tension = mem.inner_conflict_profile.get("persistent::tension", 0.0)
            new_tension = _clamp((old_tension * 0.93) + (wound * 0.07) - (calm * 0.025))
            if abs(new_tension - old_tension) >= 0.002:
                mem.inner_conflict_profile["persistent::tension"] = new_tension
                changed = True
            changed |= _v749d_merge_pressure(mem.obsession_guard_state, "persistent::saturation", saturation, inertia=0.94)
            changed |= _v749d_merge_pressure(mem.internal_need_profile, "persistent::resolution_need", resolution_need, inertia=0.89)
            mem.inhibition_level = _clamp(max(mem.inhibition_level * 0.985, saturation * 0.42))
            mem.unresolved_tension = _clamp(max(mem.unresolved_tension * 0.982, new_tension))
    mode = "recovering" if recovery > tension * 1.15 else "saturated" if saturation > 0.58 else "seeking_resolution" if resolution_need > 0.32 else "stable"
    return {
        "tension": round(_clamp(tension), 4),
        "recovery": round(_clamp(recovery), 4),
        "saturation": round(_clamp(saturation), 4),
        "resolution_need": round(_clamp(resolution_need), 4),
        "mode": mode,
        "changed": changed,
        "role": "persistent_tension_dynamics_not_dialogue",
    }


def _v749d_habit_reflex_consolidation(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    """Turn repeated causal outcomes into implicit action biases."""
    habits: Dict[str, float] = {}
    changed = False
    for _, mem, relevance in memories[:24]:
        p = _v749d_pressure(mem, relevance) * _clamp((mem.reinforcement_count + 1) / 6.0)
        if mem.repair_kind == "anti_meta" or mem.future_bias.get("avoid_repetition", 0.0) > 0.1:
            habits["reflex::avoid_meta_distance"] = max(habits.get("reflex::avoid_meta_distance", 0.0), p)
        if mem.repair_kind == "specificity" or mem.attention_impact:
            habits["reflex::increase_concrete_grounding"] = max(habits.get("reflex::increase_concrete_grounding", 0.0), p)
        if mem.relational_wound > 0.12 or mem.unresolved_tension > 0.22:
            habits["reflex::slow_before_reacting"] = max(habits.get("reflex::slow_before_reacting", 0.0), p)
        if mem.attachment_trace > 0.12 or mem.relational_importance > 0.18:
            habits["reflex::preserve_warm_contact"] = max(habits.get("reflex::preserve_warm_contact", 0.0), p)
        if mem.identity_impact > 0.16 or mem.autobiographical_weight > 0.16:
            habits["reflex::maintain_self_continuity"] = max(habits.get("reflex::maintain_self_continuity", 0.0), p)
    if mutate:
        for _, mem, relevance in memories[:18]:
            local = _v749d_pressure(mem, relevance)
            for key, value in habits.items():
                if value < 0.035:
                    continue
                changed |= _v749d_merge_pressure(mem.internal_need_profile, key, value * local, inertia=0.9)
                changed |= _v749d_merge_pressure(mem.initiative_bridge, key, value * local, inertia=0.91)
                changed |= _v749d_merge_pressure(mem.expression_bridge, key, value * local, inertia=0.91)
    return {
        "habits": {k: round(_clamp(v), 4) for k, v in sorted(habits.items(), key=lambda item: item[1], reverse=True)[:10]},
        "dominant_habit": max(habits.items(), key=lambda item: item[1])[0] if habits else "none",
        "changed": changed,
        "role": "implicit_habit_reflex_consolidation_not_dialogue",
    }


def _v749d_subjective_duration_continuity(self: CausalMemoryEngine, memories: List[Tuple[str, CausalMemory, float]], mutate: bool = False) -> Dict[str, Any]:
    """Make time pressure depend on age, unresolved tension and autobiographical load."""
    past_weight = 0.0
    present_gravity = 0.0
    future_pull = 0.0
    duration_pressure = 0.0
    changed = False
    for _, mem, relevance in memories[:24]:
        age = _v749c_age_days(mem) if "_v749c_age_days" in globals() else 0.0
        age_weight = _clamp(math.log1p(age) / 5.0)
        p = _v749d_pressure(mem, relevance)
        past_weight = max(past_weight, _clamp(p * age_weight * max(mem.autobiographical_weight, mem.identity_impact, 0.1)))
        present_gravity = max(present_gravity, _clamp(p * max(mem.causal_activation, mem.affective_charge, mem.reactivation_score)))
        future_pull = max(future_pull, _clamp(p * max(mem.future_bias.values() or [0.0], default=0.0)))
        duration_pressure = max(duration_pressure, _clamp((past_weight * 0.35) + (present_gravity * 0.45) + (future_pull * 0.2)))
        if mutate and duration_pressure > 0.02:
            changed |= _v749d_merge_pressure(mem.temporal_maturation_state, "subjective::past_weight", past_weight, inertia=0.92)
            changed |= _v749d_merge_pressure(mem.temporal_maturation_state, "subjective::present_gravity", present_gravity, inertia=0.9)
            changed |= _v749d_merge_pressure(mem.temporal_maturation_state, "subjective::future_pull", future_pull, inertia=0.9)
            changed |= _v749d_merge_pressure(mem.current_lived_meaning, "subjective::duration_pressure", duration_pressure, inertia=0.92)
    tempo = "compressed" if present_gravity > max(past_weight, future_pull) * 1.25 else "anticipating" if future_pull > past_weight else "weighted_by_past" if past_weight > 0.18 else "ordinary"
    return {
        "past_weight": round(_clamp(past_weight), 4),
        "present_gravity": round(_clamp(present_gravity), 4),
        "future_pull": round(_clamp(future_pull), 4),
        "duration_pressure": round(_clamp(duration_pressure), 4),
        "tempo": tempo,
        "changed": changed,
        "role": "subjective_duration_continuity_not_dialogue",
    }


def _v749d_global_coherence_center(self: CausalMemoryEngine, context: str, memories: List[Tuple[str, CausalMemory, float]], ecology: Dict[str, Any], mutate: bool = False) -> Dict[str, Any]:
    """Build one unified non-dialogue center for other engines to consume."""
    need_field = ecology.get("need_competition_field", {}).get("needs", {}) if isinstance(ecology, dict) else {}
    body = ecology.get("embodied_sensorimotor_field", {}).get("signals", {}) if isinstance(ecology, dict) else {}
    coherence = ecology.get("anti_fragmentation_coherence", {}) if isinstance(ecology, dict) else {}
    closed_loop = ecology.get("circular_causal_closure", {}).get("loops", {}) if isinstance(ecology, dict) else {}
    tension = ecology.get("persistent_tension_dynamics", {}) if isinstance(ecology, dict) else {}
    habits = ecology.get("implicit_habit_reflexes", {}).get("habits", {}) if isinstance(ecology, dict) else {}
    center = {
        "coherence": _clamp(_safe_float(coherence.get("coherence", 1.0), 1.0)),
        "urgency": _clamp(max(need_field.values() or [0.0], default=0.0, ) * 0.52 + max(body.values() or [0.0], default=0.0) * 0.28 + _safe_float(tension.get("resolution_need", 0.0), 0.0) * 0.2),
        "continuity": _clamp(max(_safe_float(closed_loop.get("identity_feedback", 0.0), 0.0), _safe_float(coherence.get("identity_average", 0.0), 0.0))),
        "prudence": _clamp(max(_safe_float(tension.get("saturation", 0.0), 0.0), _safe_float(body.get("withdrawal_impulse", 0.0), 0.0), _safe_float(habits.get("reflex::slow_before_reacting", 0.0), 0.0))),
        "initiative_readiness": _clamp(max(_safe_float(closed_loop.get("initiative_resumption", 0.0), 0.0), _safe_float(body.get("approach_impulse", 0.0), 0.0)) * (1.0 - _safe_float(tension.get("saturation", 0.0), 0.0) * 0.45)),
    }
    if center["coherence"] < 0.62:
        dominant_directive = "restore_coherence_before_expansion"
    elif center["prudence"] > 0.55:
        dominant_directive = "slow_down_and_reduce_pressure"
    elif center["initiative_readiness"] > 0.38:
        dominant_directive = "resume_useful_intention"
    elif center["urgency"] > 0.42:
        dominant_directive = "prioritize_most_loaded_need"
    else:
        dominant_directive = "maintain_stable_presence"
    changed = False
    if mutate:
        for _, mem, relevance in memories[:16]:
            p = _v749d_pressure(mem, relevance)
            changed |= _v749d_merge_pressure(mem.current_lived_meaning, "global_center::coherence", center["coherence"] * p, inertia=0.93)
            changed |= _v749d_merge_pressure(mem.current_lived_meaning, "global_center::continuity", center["continuity"] * p, inertia=0.93)
            changed |= _v749d_merge_pressure(mem.initiative_bridge, f"global_directive::{dominant_directive}", max(center.values()) * p, inertia=0.92)
            changed |= _v749d_merge_pressure(mem.expression_bridge, f"global_directive::{dominant_directive}", max(center.values()) * p, inertia=0.92)
    return {
        "center": {k: round(_clamp(v), 4) for k, v in center.items()},
        "dominant_directive": dominant_directive,
        "changed": changed,
        "role": "global_causal_coherence_center_not_dialogue",
    }


def _v749d_integrated_completion(self: CausalMemoryEngine, context: str = "", memories: Optional[List[Tuple[str, CausalMemory, float]]] = None, mutate: bool = False) -> Dict[str, Any]:
    memories = memories if memories is not None else self._v749c_selected(context)
    base = self._v749c_integrated_living_ecology(context, memories, mutate=mutate)
    closure = _v749d_circular_causal_closure(self, memories, mutate=mutate)
    atmosphere = _v749d_implicit_belief_atmosphere(self, memories, mutate=mutate)
    tension = _v749d_persistent_tension_dynamics(self, memories, mutate=mutate)
    habits = _v749d_habit_reflex_consolidation(self, memories, mutate=mutate)
    subjective_duration = _v749d_subjective_duration_continuity(self, memories, mutate=mutate)
    enriched = dict(base)
    enriched["circular_causal_closure"] = closure
    enriched["implicit_belief_atmosphere"] = atmosphere
    enriched["persistent_tension_dynamics"] = tension
    enriched["implicit_habit_reflexes"] = habits
    enriched["subjective_duration_continuity"] = subjective_duration
    center = _v749d_global_coherence_center(self, context, memories, enriched, mutate=mutate)
    enriched["global_causal_coherence_center"] = center
    enriched["changed"] = bool(base.get("changed") or closure.get("changed") or atmosphere.get("changed") or tension.get("changed") or habits.get("changed") or subjective_duration.get("changed") or center.get("changed"))
    enriched["role"] = "v7_4_9d_living_causal_closure_not_dialogue"
    return enriched


def _v749d_export_regulation_context(self: CausalMemoryEngine, context: str) -> Dict[str, Any]:
    base = _ORIGINAL_V749C_EXPORT_REGULATION_CONTEXT(self, context)
    memories = self._v749c_selected(context)
    completion = _v749d_integrated_completion(self, context, memories, mutate=False)
    base["integrated_living_ecology_v7_4_9d"] = completion
    base["circular_causal_closure"] = completion["circular_causal_closure"]
    base["implicit_belief_atmosphere"] = completion["implicit_belief_atmosphere"]
    base["persistent_tension_dynamics"] = completion["persistent_tension_dynamics"]
    base["implicit_habit_reflexes"] = completion["implicit_habit_reflexes"]
    base["subjective_duration_continuity"] = completion["subjective_duration_continuity"]
    base["global_causal_coherence_center"] = completion["global_causal_coherence_center"]
    base["role"] = "regulation_context_v7_4_9d_living_closure_not_dialogue"
    return base


def _v749d_run_living_memory_cycle(self: CausalMemoryEngine, context: str = "", save: bool = True) -> Dict[str, Any]:
    base = _ORIGINAL_V749C_RUN_LIVING_MEMORY_CYCLE(self, context, save=False)
    memories = self._v749c_selected(context)
    completion = _v749d_integrated_completion(self, context, memories, mutate=True)
    base["integrated_living_ecology_v7_4_9d"] = completion
    base["changed"] = bool(base.get("changed") or completion.get("changed"))
    base["role"] = "living_memory_cycle_v7_4_9d_living_closure_not_dialogue"
    if save and base["changed"]:
        self.save_memories()
    return base


def _v749d_get_memory_stats(self: CausalMemoryEngine) -> Dict[str, Any]:
    stats = _ORIGINAL_V749C_GET_MEMORY_STATS(self)
    vals = list(self.memories.values())
    stats.update({
        "engine_version": "7.4.9d-deep-living-causal-memory-closed-ecology-corrected",
        "v7_4_9d_closed_loop_memories": sum(1 for m in vals if any(str(k).startswith("closed_loop::") for k in m.internal_need_profile) or any(str(k).startswith("closed_loop::") for k in m.future_bias)),
        "v7_4_9d_implicit_belief_memories": sum(1 for m in vals if any(str(k).startswith("implicit_belief::") for k in m.current_lived_meaning) or any(str(k).startswith("atmosphere::") for k in m.deep_causal_roots)),
        "v7_4_9d_persistent_tension_memories": sum(1 for m in vals if any(str(k).startswith("persistent::") for k in m.inner_conflict_profile) or any(str(k).startswith("persistent::") for k in m.obsession_guard_state)),
        "v7_4_9d_habit_reflex_memories": sum(1 for m in vals if any(str(k).startswith("reflex::") for k in m.internal_need_profile) or any(str(k).startswith("reflex::") for k in m.initiative_bridge)),
        "v7_4_9d_subjective_duration_memories": sum(1 for m in vals if any(str(k).startswith("subjective::") for k in m.temporal_maturation_state) or any(str(k).startswith("subjective::") for k in m.current_lived_meaning)),
        "v7_4_9d_global_center_memories": sum(1 for m in vals if any(str(k).startswith("global_center::") or str(k).startswith("global_directive::") for k in list(m.current_lived_meaning.keys()) + list(m.initiative_bridge.keys()) + list(m.expression_bridge.keys()))),
    })
    return stats


def _v749d_save_memories(self: CausalMemoryEngine) -> None:
    data = {mem_id: asdict(mem.normalized()) for mem_id, mem in self.memories.items()}
    stats = self.get_memory_stats() if hasattr(self, "get_memory_stats") else {}
    data["_metadata"] = {
        "engine_version": "7.4.9d-deep-living-causal-memory-closed-ecology-corrected",
        "last_updated": _now(),
        "total_memories": len(self.memories),
        "avg_confidence": stats.get("avg_confidence", 0.0) if self.memories else 0.0,
        "role": "deep_living_causal_memory_not_dialogue_generator",
        "notes": "Correctif V7.4.9d : fermeture de la boucle causale vivante. Les effets modifient les besoins, les besoins modifient les priorités, les priorités modifient l'initiative/perception future, puis les résultats reviennent vers identité, relation et mémoire implicite. Aucun dialogue public généré.",
        "v7_4_8_capabilities_preserved": [
            "hierarchical_long_term_causal_schemas",
            "organic_forgetting_without_brutal_deletion",
            "persistent_personality_attractor_stabilization",
            "situated_causal_grounding_from_current_context",
            "interrupted_intention_memory_and_resumption_pressure",
            "existential_priority_field",
            "user_specific_social_differentiation",
            "dynamic_autobiographical_reconstruction",
            "deep_non_dialogue_cross_engine_exports",
        ],
        "v7_4_9_capabilities_preserved": [
            "autonomous_existential_continuity",
            "multi_scale_causal_ecology",
            "stable_personality_trait_consolidation",
            "persistent_intention_stack",
            "organic_long_term_consolidation_and_blur",
            "embodied_preverbal_reactivity",
            "emergent_self_organization",
            "non_dialogue_ecological_finalization",
            "integrated_living_ecology_loop",
            "need_competition_field",
            "implicit_procedural_memory",
            "subjective_time_pressure",
            "causal_consequence_horizon",
            "embodied_sensorimotor_causal_field",
            "anti_fragmentation_coherence_anchor",
        ],
        "v7_4_9d_capabilities": [
            "closed_circular_causal_loop",
            "effect_to_need_to_priority_feedback",
            "implicit_belief_atmosphere_compression",
            "persistent_tension_accumulation_and_recovery",
            "implicit_habit_reflex_consolidation",
            "subjective_duration_continuity",
            "global_causal_coherence_center",
            "cross_engine_directive_export_without_dialogue",
        ],
        "stats": stats,
    }
    self.memory_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


CausalMemoryEngine._v749d_circular_causal_closure = _v749d_circular_causal_closure
CausalMemoryEngine._v749d_implicit_belief_atmosphere = _v749d_implicit_belief_atmosphere
CausalMemoryEngine._v749d_persistent_tension_dynamics = _v749d_persistent_tension_dynamics
CausalMemoryEngine._v749d_habit_reflex_consolidation = _v749d_habit_reflex_consolidation
CausalMemoryEngine._v749d_subjective_duration_continuity = _v749d_subjective_duration_continuity
CausalMemoryEngine._v749d_global_coherence_center = _v749d_global_coherence_center
CausalMemoryEngine._v749d_integrated_completion = _v749d_integrated_completion
CausalMemoryEngine.export_regulation_context = _v749d_export_regulation_context
CausalMemoryEngine.run_living_memory_cycle = _v749d_run_living_memory_cycle
CausalMemoryEngine.get_memory_stats = _v749d_get_memory_stats
CausalMemoryEngine.save_memories = _v749d_save_memories

