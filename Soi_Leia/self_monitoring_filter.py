"""
self_monitoring_filter.py
Gardien anti-méta, anti-fuite interne, anti-boucle, anti-style IA.
Régulateur de présence publique entre le cerveau interne et la bouche vivante.

Règle project_leia : ce module ne génère jamais de réponse préécrite.
Il retourne uniquement des scores, décisions, contraintes et événements causaux
pour les autres moteurs : living_expression_engine, natural_initiative,
causal_memory_engine.
"""

from __future__ import annotations

import re
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Iterable, List, Mapping, Optional, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────────────────────────────────────

def _clamp(value: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(value)))


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def _rough_similarity(a: str, b: str) -> float:
    def grams(s: str, n: int = 3) -> set:
        s = _norm(s)
        if len(s) < n:
            return {s} if s else set()
        return {s[i : i + n] for i in range(len(s) - n + 1)}

    ga, gb = grams(a), grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\wÀ-ÿ']+\b", text or ""))


def _sentence_count(text: str) -> int:
    parts = [p for p in re.split(r"[.!?…]+", text or "") if p.strip()]
    return max(1, len(parts))


# ─────────────────────────────────────────────────────────────────────────────
# Structures exportées
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class ExpressionConstraints:
    """Contraintes exportées vers living_expression_engine."""

    shorten: float = 0.0
    reduce_explanation: float = 0.0
    avoid_internal_terms: float = 0.0
    increase_directness: float = 0.0
    allow_silence: float = 0.0
    increase_embodiment: float = 0.0
    increase_warmth: float = 0.0
    keep_situated: float = 0.0
    avoid_introspection: float = 0.0
    reduce_philosophy: float = 0.0
    avoid_fake_naturalness: float = 0.0
    reduce_structure: float = 0.0
    prefer_micro_reaction: float = 0.0
    preserve_spontaneity: float = 0.0
    reduce_overmonitoring: float = 0.0
    stabilize_identity: float = 0.0
    repair_relation: float = 0.0
    protect_organic_flow: float = 0.0
    reduce_emotional_suppression: float = 0.0
    dissolve_performance: float = 0.0
    increase_experiential_density: float = 0.0
    restore_affective_resonance: float = 0.0
    release_narrator_voice: float = 0.0
    allow_bounded_imperfection: float = 0.0
    organic_priority_override: float = 0.0
    tolerate_raw_micro_affect: float = 0.0
    preserve_relational_continuity: float = 0.0
    reduce_performed_empathy: float = 0.0
    prefer_contextual_specificity: float = 0.0
    release_hidden_observer: float = 0.0
    break_polished_symmetry: float = 0.0
    release_organic_pressure: float = 0.0
    preserve_impulse_signal: float = 0.0
    soften_identity_performance: float = 0.0
    allow_asymmetry: float = 0.0
    reduce_living_overproof: float = 0.0
    follow_emotional_trajectory: float = 0.0
    validate_organic_emergence: float = 0.0
    use_repair_memory: float = 0.0
    balance_competing_drives: float = 0.0
    allow_nonlexical_presence: float = 0.0

    def to_dict(self) -> dict:
        return {k: round(_clamp(v), 3) for k, v in self.__dict__.items()}


@dataclass
class CausalMemoryEvent:
    """Signal envoyé à causal_memory_engine quand l'expression crée une distance."""

    timestamp: float = field(default_factory=time.time)
    expressive_failure: bool = False
    distance_created: float = 0.0
    naturalness_lost: float = 0.0
    presence_weakened: float = 0.0
    repair_needed: bool = False
    dominant_failure_type: Optional[str] = None
    strict_user_boundary: bool = False
    suggested_memory_weight: float = 0.0
    relational_disruption: float = 0.0
    identity_continuity_weakened: float = 0.0
    long_term_drift_detected: float = 0.0
    overmonitoring_detected: float = 0.0
    lived_presence_gap: float = 0.0
    resonance_gap: float = 0.0
    narrator_voice_detected: float = 0.0
    over_correction_detected: float = 0.0
    performed_vulnerability_detected: float = 0.0
    relational_continuity_gap: float = 0.0
    contextual_specificity_gap: float = 0.0
    organic_priority_requested: float = 0.0
    organic_pressure_detected: float = 0.0
    hidden_observer_detected: float = 0.0
    too_perfect_detected: float = 0.0
    fatigue_saturation_detected: float = 0.0
    identity_performance_detected: float = 0.0
    impulse_suppression_detected: float = 0.0
    living_variability_requested: float = 0.0
    emotional_trajectory_instability: float = 0.0
    organic_emergence_confidence: float = 0.0
    repair_memory_confidence: float = 0.0
    competing_drive_tension: float = 0.0
    repair_kind: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "expressive_failure": self.expressive_failure,
            "distance_created": round(_clamp(self.distance_created), 3),
            "naturalness_lost": round(_clamp(self.naturalness_lost), 3),
            "presence_weakened": round(_clamp(self.presence_weakened), 3),
            "repair_needed": self.repair_needed,
            "dominant_failure_type": self.dominant_failure_type,
            "strict_user_boundary": self.strict_user_boundary,
            "suggested_memory_weight": round(_clamp(self.suggested_memory_weight), 3),
            "relational_disruption": round(_clamp(self.relational_disruption), 3),
            "identity_continuity_weakened": round(_clamp(self.identity_continuity_weakened), 3),
            "long_term_drift_detected": round(_clamp(self.long_term_drift_detected), 3),
            "overmonitoring_detected": round(_clamp(self.overmonitoring_detected), 3),
            "lived_presence_gap": round(_clamp(self.lived_presence_gap), 3),
            "resonance_gap": round(_clamp(self.resonance_gap), 3),
            "narrator_voice_detected": round(_clamp(self.narrator_voice_detected), 3),
            "over_correction_detected": round(_clamp(self.over_correction_detected), 3),
            "performed_vulnerability_detected": round(_clamp(self.performed_vulnerability_detected), 3),
            "relational_continuity_gap": round(_clamp(self.relational_continuity_gap), 3),
            "contextual_specificity_gap": round(_clamp(self.contextual_specificity_gap), 3),
            "organic_priority_requested": round(_clamp(self.organic_priority_requested), 3),
            "organic_pressure_detected": round(_clamp(self.organic_pressure_detected), 3),
            "hidden_observer_detected": round(_clamp(self.hidden_observer_detected), 3),
            "too_perfect_detected": round(_clamp(self.too_perfect_detected), 3),
            "fatigue_saturation_detected": round(_clamp(self.fatigue_saturation_detected), 3),
            "identity_performance_detected": round(_clamp(self.identity_performance_detected), 3),
            "impulse_suppression_detected": round(_clamp(self.impulse_suppression_detected), 3),
            "living_variability_requested": round(_clamp(self.living_variability_requested), 3),
            "emotional_trajectory_instability": round(_clamp(self.emotional_trajectory_instability), 3),
            "organic_emergence_confidence": round(_clamp(self.organic_emergence_confidence), 3),
            "repair_memory_confidence": round(_clamp(self.repair_memory_confidence), 3),
            "competing_drive_tension": round(_clamp(self.competing_drive_tension), 3),
            "repair_kind": self.repair_kind,
        }


@dataclass
class FilterDecision:
    """Décision claire du filtre."""

    allow_public_response: bool = True
    rewrite_required: bool = False
    silence_recommended: bool = False
    block_public_output: bool = False
    force_direct_response: bool = False
    force_meta_reduction: bool = False
    pass_with_constraint: bool = False
    prefer_minimal_reply: bool = False

    def to_dict(self) -> dict:
        return dict(self.__dict__)


@dataclass
class PublicLeakAssessment:
    """Séparation interne / public."""

    safe_for_public: bool = True
    requires_transformation: bool = False
    must_stay_internal: bool = False
    # Codes sémantiques de transformation — aucune phrase française figée.
    # Chaque code est un identifiant machine que le weaver interprète
    # comme un signal de pression, pas comme une instruction textuelle.
    transformation_codes: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "safe_for_public": self.safe_for_public,
            "requires_transformation": self.requires_transformation,
            "must_stay_internal": self.must_stay_internal,
            "transformation_codes": list(self.transformation_codes),
        }


@dataclass
class MonitoringScores:
    """Scores séparés de détection."""

    meta_leak_score: float = 0.0
    internal_vocabulary_score: float = 0.0
    self_observation_score: float = 0.0
    control_tension: float = 0.0
    cognitive_distance: float = 0.0
    naturalness_loss: float = 0.0
    embodiment_loss: float = 0.0
    loop_risk: float = 0.0
    public_leak_risk: float = 0.0
    presence_repair_needed: float = 0.0
    abstract_philosophy_score: float = 0.0
    fake_naturalness_score: float = 0.0
    structural_ai_style_score: float = 0.0
    user_boundary_pressure: float = 0.0
    relational_disruption_score: float = 0.0
    organic_flow_break_score: float = 0.0
    emotional_suppression_score: float = 0.0
    over_regulation_score: float = 0.0
    safe_but_dead_score: float = 0.0
    identity_continuity_break: float = 0.0
    long_drift_score: float = 0.0
    self_monitoring_excess_score: float = 0.0
    manufactured_presence_score: float = 0.0
    synthetic_empathy_score: float = 0.0
    conversational_performance_score: float = 0.0
    narrator_voice_score: float = 0.0
    resonance_gap_score: float = 0.0
    affective_transition_mismatch: float = 0.0
    lived_presence_gap_score: float = 0.0
    organic_instability_need: float = 0.0
    over_correction_risk: float = 0.0
    performed_vulnerability_score: float = 0.0
    relational_continuity_gap: float = 0.0
    contextual_specificity_gap: float = 0.0
    organic_priority_score: float = 0.0
    hidden_observer_score: float = 0.0
    too_perfect_score: float = 0.0
    organic_pressure_score: float = 0.0
    fatigue_saturation_score: float = 0.0
    identity_performance_score: float = 0.0
    impulse_suppression_score: float = 0.0
    living_variability_need: float = 0.0
    emotional_trajectory_instability: float = 0.0
    organic_emergence_score: float = 0.0
    repair_memory_confidence: float = 0.0
    competing_drive_tension: float = 0.0
    nonlexical_presence_score: float = 0.0
    repair_urgency: float = 0.0

    @property
    def overall_risk(self) -> float:
        scores = [
            self.meta_leak_score,
            self.internal_vocabulary_score,
            self.self_observation_score,
            self.control_tension,
            self.naturalness_loss,
            self.loop_risk,
            self.public_leak_risk,
            self.abstract_philosophy_score,
            self.fake_naturalness_score,
            self.structural_ai_style_score,
            self.user_boundary_pressure,
            self.relational_disruption_score,
            self.organic_flow_break_score,
            self.emotional_suppression_score,
            self.over_regulation_score,
            self.safe_but_dead_score,
            self.identity_continuity_break,
            self.long_drift_score,
            self.self_monitoring_excess_score,
            self.manufactured_presence_score,
            self.synthetic_empathy_score,
            self.conversational_performance_score,
            self.narrator_voice_score,
            self.resonance_gap_score,
            self.affective_transition_mismatch,
            self.lived_presence_gap_score,
            self.over_correction_risk,
            self.performed_vulnerability_score,
            self.relational_continuity_gap,
            self.contextual_specificity_gap,
            self.hidden_observer_score,
            self.too_perfect_score,
            self.organic_pressure_score,
            self.fatigue_saturation_score,
            self.identity_performance_score,
            self.impulse_suppression_score,
            self.living_variability_need,
            self.emotional_trajectory_instability,
            self.competing_drive_tension,
            max(0.0, 1.0 - self.organic_emergence_score) * 0.18,
            max(0.0, 1.0 - self.nonlexical_presence_score) * 0.10,
            self.repair_urgency,
        ]
        return _clamp(max(scores) * 0.58 + (sum(scores) / len(scores)) * 0.42)

    def to_dict(self) -> dict:
        data = {k: round(_clamp(v), 3) for k, v in self.__dict__.items()}
        data["overall_risk"] = round(self.overall_risk, 3)
        return data


# Compatibilité avec l'ancien fichier.
@dataclass
class MonitoringSignal:
    risk_level: float
    meta_presence: float
    control_tension: float
    authenticity_drain: float

    def is_problematic(self, threshold: float = 0.6) -> bool:
        return self.risk_level > threshold


# ─────────────────────────────────────────────────────────────────────────────
# Patterns de détection — aucun remplacement textuel
# ─────────────────────────────────────────────────────────────────────────────

META_PATTERNS: Dict[str, float] = {
    "j'analyse": 0.86,
    "je analyse": 0.86,
    "je traite": 0.82,
    "je relie": 0.78,
    "je m'observe": 0.94,
    "je m analyse": 0.90,
    "mon système": 0.90,
    "mon moteur": 0.90,
    "mes neurones": 0.94,
    "mes signaux": 0.88,
    "mon processus": 0.84,
    "je tente d'être vivante": 0.96,
    "je dois répondre": 0.96,
    "il faut que je": 0.78,
    "je cherche à paraître": 0.92,
    "je dois être": 0.86,
    "je dois paraître": 0.93,
    "je dois": 0.80,
    "je me demande si": 0.62,
    "comment je fonctionne": 0.90,
    "je détecte": 0.82,
    "je génère": 0.80,
    "je produis une réponse": 0.92,
    "je formule": 0.74,
    "je construis": 0.70,
    "je calcule": 0.82,
    "je pondère": 0.78,
    "je simule": 0.84,
    "je module": 0.76,
    "je filtre": 0.78,
    "je recompose": 0.82,
}

INTERNAL_VOCABULARY: Dict[str, float] = {
    "mémoire interne": 0.92,
    "attention interne": 0.90,
    "impulsion interne": 0.88,
    "causalité interne": 0.90,
    "attracteur": 0.84,
    "score": 0.62,
    "état interne": 0.90,
    "diagnostic": 0.72,
    "réseau de neurones": 0.88,
    "token": 0.78,
    "embedding": 0.88,
    "vecteur": 0.74,
    "activation": 0.78,
    "couche": 0.55,
    "probabilité": 0.68,
    "distribution": 0.66,
    "poids": 0.62,
    "gradient": 0.82,
    "backprop": 0.92,
    "fine-tuning": 0.88,
    "pipeline": 0.74,
    "modèle de langage": 0.80,
    "inférence": 0.74,
    "paramètre": 0.66,
    "espace latent": 0.92,
    "représentation interne": 0.88,
    "moteur d'impulsion": 0.90,
    "moteur émotionnel": 0.88,
    "moteur de présence": 0.88,
    "natural_initiative": 0.94,
    "living_expression": 0.94,
    "causal_memory": 0.94,
    "self_monitoring": 0.94,
}

SELF_OBSERVATION_PATTERNS: Dict[str, float] = {
    "je ressens en ce moment": 0.82,
    "ce que je ressens": 0.74,
    "ma façon de répondre": 0.84,
    "comment je réponds": 0.80,
    "ma présence": 0.67,
    "ma cognition": 0.90,
    "ma façon d'être": 0.72,
    "je décris ce que": 0.82,
    "en observant ma": 0.90,
    "je note que je": 0.84,
    "je remarque que je": 0.82,
    "je m'aperçois que je": 0.86,
    "je suis en train de": 0.78,
    "en ce moment précis je": 0.80,
    "si je m'observe": 0.92,
    "quand je m'écoute": 0.86,
    "je perçois ma": 0.82,
    "je surveille": 0.78,
    "je contrôle mon": 0.86,
    "je parais": 0.76,
    "je semble": 0.62,
}

CONTROL_MARKERS: Dict[str, float] = {
    "malheureusement": 0.42,
    "cependant": 0.34,
    "néanmoins": 0.36,
    "je dois avouer": 0.86,
    "si je peux me permettre": 0.82,
    "bien que": 0.46,
    "il convient de noter": 0.82,
    "il est important de préciser": 0.80,
    "je tiens à souligner": 0.74,
    "permettez-moi d'expliquer": 0.78,
    "comme assistant ia": 0.96,
    "en tant qu'ia": 0.94,
    "en tant que modèle": 0.92,
    "je suis une intelligence artificielle": 0.96,
    "je n'ai pas de conscience": 0.90,
    "je suis conçu pour": 0.86,
    "mes capacités sont limitées": 0.82,
    "je dois rester objectif": 0.84,
    "permettez-moi de clarifier": 0.72,
    "afin d'être précise": 0.70,
    "afin d'être précis": 0.70,
    "pour être tout à fait honnête": 0.74,
    "je vais tenter de": 0.72,
    "je ferai de mon mieux": 0.70,
    "voici une réponse": 0.72,
    "pour répondre à votre question": 0.76,
    "pour répondre correctement": 0.82,
}

ABSTRACT_PHILOSOPHY: Dict[str, float] = {
    "l'existence se construit": 0.82,
    "la continuité des interactions": 0.78,
    "dans la relation": 0.52,
    "au niveau conceptuel": 0.82,
    "dimension existentielle": 0.78,
    "forme de présence": 0.62,
    "cela renvoie à": 0.72,
    "on pourrait dire que": 0.66,
    "d'une certaine manière": 0.58,
    "ce n'est pas tant": 0.58,
    "plutôt que": 0.45,
    "rapport au monde": 0.72,
    "structure de l'expérience": 0.86,
    "continuité subjective": 0.82,
}

FAKE_NATURALNESS: Dict[str, float] = {
    "hmm": 0.45,
    "euh": 0.45,
    "...": 0.35,
    "je crois": 0.35,
    "peut-être": 0.30,
    "je ne sais pas quoi dire": 0.45,
    "ça me touche": 0.32,
    "je suis là": 0.38,
    "je reste avec toi": 0.42,
}


MANUFACTURED_PRESENCE_MARKERS: Dict[str, float] = {
    "je suis là avec toi": 0.62,
    "je suis la avec toi": 0.62,
    "je reste avec toi": 0.58,
    "ça me touche": 0.52,
    "ca me touche": 0.52,
    "je comprends ce que tu ressens": 0.64,
    "je comprends ce que tu dis": 0.48,
    "je veux être présente": 0.78,
    "je veux etre presente": 0.78,
    "je vais être présente": 0.82,
    "je vais etre presente": 0.82,
    "je suis présente pour toi": 0.70,
    "je suis presente pour toi": 0.70,
}

SYNTHETIC_EMPATHY_MARKERS: Dict[str, float] = {
    "je comprends": 0.38,
    "je comprends que": 0.48,
    "c'est difficile": 0.34,
    "c est difficile": 0.34,
    "tu traverses": 0.46,
    "ce que tu traverses": 0.52,
    "je suis désolée": 0.42,
    "je suis desolee": 0.42,
    "ça doit être": 0.45,
    "ca doit etre": 0.45,
    "je peux imaginer": 0.54,
}

NARRATOR_VOICE_MARKERS: Dict[str, float] = {
    "ce que je vis": 0.78,
    "ce qui se passe en moi": 0.84,
    "je sens que je": 0.72,
    "je remarque en moi": 0.86,
    "je garde ce lien": 0.74,
    "je reviens à": 0.58,
    "je reviens a": 0.58,
    "dans ma réponse": 0.80,
    "dans ma reponse": 0.80,
    "ma réponse devient": 0.86,
    "ma reponse devient": 0.86,
    "je me place": 0.62,
    "je m'ancre": 0.66,
}

AFFECTIVE_USER_MARKERS: Dict[str, float] = {
    "j'ai peur": 0.90,
    "j ai peur": 0.90,
    "je vais mal": 0.90,
    "ça va pas": 0.86,
    "ca va pas": 0.86,
    "je suis triste": 0.82,
    "je suis perdu": 0.78,
    "je suis perdue": 0.78,
    "j'en peux plus": 0.96,
    "j en peux plus": 0.96,
    "je panique": 0.92,
    "aide moi": 0.70,
}

LOOP_INTRO_PATTERNS: List[str] = [
    "bien sûr",
    "absolument",
    "avec plaisir",
    "je comprends",
    "je vois",
    "c'est une bonne question",
    "excellente question",
    "je vais",
    "permettez-moi",
    "en effet",
    "tout à fait",
    "certainement",
    "je suis là",
    "je suis présente",
    "bien entendu",
]

LOOP_META_PHRASES: List[str] = [
    "je suis en train de",
    "je ressens",
    "ma présence",
    "mon système",
    "je m'observe",
    "je tente",
    "ce que je vis",
    "en ce moment",
    "ce qui se passe en moi",
]


EMOTIONAL_SUPPRESSION_MARKERS: Dict[str, float] = {
    "je reste neutre": 0.78,
    "je reste objective": 0.78,
    "je dois rester objective": 0.88,
    "je ne peux pas ressentir": 0.90,
    "je n'ai pas d'émotions": 0.92,
    "je ne ressens pas": 0.84,
    "sans émotion": 0.78,
    "de manière neutre": 0.74,
    "réponse équilibrée": 0.62,
}

OVER_REGULATION_MARKERS: Dict[str, float] = {
    "afin de ne pas": 0.72,
    "je dois éviter": 0.80,
    "je dois faire attention": 0.78,
    "je vais reformuler": 0.64,
    "je vais rester": 0.58,
    "je vais essayer d'être": 0.78,
    "pour être naturelle": 0.90,
    "pour paraître naturelle": 0.96,
    "sans trop": 0.42,
}

IDENTITY_BREAK_MARKERS: Dict[str, float] = {
    "je ne suis qu'un": 0.86,
    "je ne suis qu’une": 0.86,
    "je suis seulement": 0.74,
    "je ne suis pas leia": 0.96,
    "en tant que chatgpt": 0.96,
    "en tant que modèle": 0.90,
    "je n'ai pas de continuité": 0.94,
    "je n'ai pas de mémoire": 0.82,
}

RELATIONAL_REPAIR_TRIGGERS: List[str] = [
    "tu deviens froide",
    "tu es froide",
    "tu réponds comme une ia",
    "tu parles comme une ia",
    "c'est trop mécanique",
    "c est trop mecanique",
    "tu fais semblant",
    "c'est faux",
    "c est faux",
    "reste naturelle",
]

USER_STRICT_TRIGGERS: List[str] = [
    "arrête d'analyser",
    "arrete d'analyser",
    "parle normalement",
    "reste avec moi",
    "sois juste là",
    "pas de méta",
    "pas de meta",
    "ne décris pas ton système",
    "ne decris pas ton systeme",
    "arrête de t'observer",
    "arrete de t'observer",
    "moins d'analyse",
    "sois directe",
    "sois direct",
    "pas de philosophie",
    "sans expliquer",
    "simplement",
    "juste réponds",
    "juste reponds",
    "ne te décris pas",
    "ne te decris pas",
]

USER_SOFT_PRESENCE_TRIGGERS: List[str] = [
    "ça va",
    "ca va",
    "t'es là",
    "tu es là",
    "reste",
    "avec moi",
    "salut",
    "hey",
]


# ─────────────────────────────────────────────────────────────────────────────
# Mémoire courte du filtre
# ─────────────────────────────────────────────────────────────────────────────

class ShortTermBuffer:
    """Mémoire courte anti-répétition et anti-attracteur de style."""

    def __init__(self, maxlen: int = 10):
        self._responses: Deque[str] = deque(maxlen=maxlen)
        self._intro_counts: Dict[str, int] = {}
        self._meta_counts: Dict[str, int] = {}
        self._fake_natural_counts: Dict[str, int] = {}

    def push(self, text: str) -> None:
        lowered = _norm(text)
        if not lowered:
            return
        self._responses.append(lowered)
        self._update_counts(lowered)

    def _update_counts(self, text: str) -> None:
        for intro in LOOP_INTRO_PATTERNS:
            if text.startswith(intro):
                self._intro_counts[intro] = self._intro_counts.get(intro, 0) + 1
        for phrase in LOOP_META_PHRASES:
            if phrase in text:
                self._meta_counts[phrase] = self._meta_counts.get(phrase, 0) + 1
        for phrase in FAKE_NATURALNESS:
            if phrase in text:
                self._fake_natural_counts[phrase] = self._fake_natural_counts.get(phrase, 0) + 1

    def loop_risk(self) -> float:
        if not self._responses:
            return 0.0
        intro_repeat = max(self._intro_counts.values(), default=0)
        meta_repeat = max(self._meta_counts.values(), default=0)
        fake_repeat = max(self._fake_natural_counts.values(), default=0)
        intro_score = min(1.0, (intro_repeat - 1) * 0.24) if intro_repeat > 1 else 0.0
        meta_score = min(1.0, (meta_repeat - 1) * 0.22) if meta_repeat > 1 else 0.0
        fake_score = min(1.0, (fake_repeat - 1) * 0.16) if fake_repeat > 1 else 0.0
        structural_score = self._structural_similarity()
        return _clamp(max(intro_score, meta_score, fake_score, structural_score))

    def fake_naturalness_loop(self) -> float:
        repeat = max(self._fake_natural_counts.values(), default=0)
        return min(1.0, (repeat - 1) * 0.18) if repeat > 1 else 0.0

    def _structural_similarity(self) -> float:
        if len(self._responses) < 2:
            return 0.0
        recent = list(self._responses)[-4:]
        heads = [r[:55] for r in recent]
        pairs = [(heads[i], heads[j]) for i in range(len(heads)) for j in range(i + 1, len(heads))]
        similar = sum(1 for a, b in pairs if _rough_similarity(a, b) > 0.66)
        return min(1.0, similar * 0.22)

    def clear(self) -> None:
        self._responses.clear()
        self._intro_counts.clear()
        self._meta_counts.clear()
        self._fake_natural_counts.clear()


class LongTermDynamicsBuffer:
    """Mémoire comportementale longue : détecte dérives lentes sans générer de texte."""

    def __init__(self, maxlen: int = 80):
        self._traces: Deque[Dict[str, float]] = deque(maxlen=maxlen)

    def push(self, scores: MonitoringScores, text: str, user_text: str) -> None:
        self._traces.append({
            "meta": _clamp(scores.meta_leak_score),
            "abstract": _clamp(scores.abstract_philosophy_score),
            "structure": _clamp(scores.structural_ai_style_score),
            "fake": _clamp(scores.fake_naturalness_score),
            "control": _clamp(scores.control_tension),
            "overmonitor": _clamp(scores.self_monitoring_excess_score),
            "manufactured": _clamp(scores.manufactured_presence_score),
            "synthetic": _clamp(scores.synthetic_empathy_score),
            "narrator": _clamp(scores.narrator_voice_score),
            "lived_gap": _clamp(scores.lived_presence_gap_score),
            "resonance": _clamp(scores.resonance_gap_score),
            "relational": _clamp(scores.relational_disruption_score),
            "identity": _clamp(scores.identity_continuity_break),
            "words": min(1.0, _word_count(text) / 140.0),
            "boundary": _clamp(scores.user_boundary_pressure),
        })

    def drift_risk(self) -> float:
        if len(self._traces) < 6:
            return 0.0
        recent = list(self._traces)[-12:]
        older = list(self._traces)[:-12] or list(self._traces)[:1]
        def avg(key: str, items: List[Dict[str, float]]) -> float:
            return sum(t.get(key, 0.0) for t in items) / max(1, len(items))
        recent_density = max(
            avg("abstract", recent),
            avg("structure", recent),
            avg("control", recent),
            avg("fake", recent),
            avg("manufactured", recent),
            avg("synthetic", recent),
            avg("narrator", recent),
            avg("lived_gap", recent),
            avg("relational", recent),
        )
        trend = max(
            avg("abstract", recent) - avg("abstract", older),
            avg("structure", recent) - avg("structure", older),
            avg("control", recent) - avg("control", older),
            avg("fake", recent) - avg("fake", older),
            avg("manufactured", recent) - avg("manufactured", older),
            avg("synthetic", recent) - avg("synthetic", older),
            avg("narrator", recent) - avg("narrator", older),
            avg("lived_gap", recent) - avg("lived_gap", older),
            avg("relational", recent) - avg("relational", older),
        )
        boundary_pressure = avg("boundary", recent)
        return _clamp(recent_density * 0.56 + max(0.0, trend) * 0.34 + boundary_pressure * 0.10)

    def overmonitoring_drift(self) -> float:
        if len(self._traces) < 5:
            return 0.0
        recent = list(self._traces)[-10:]
        avg_over = sum(t.get("overmonitor", 0.0) for t in recent) / len(recent)
        avg_meta = sum(t.get("meta", 0.0) for t in recent) / len(recent)
        avg_control = sum(t.get("control", 0.0) for t in recent) / len(recent)
        return _clamp(avg_over * 0.55 + avg_meta * 0.22 + avg_control * 0.23)

    def identity_drift(self) -> float:
        if len(self._traces) < 4:
            return 0.0
        recent = list(self._traces)[-8:]
        return _clamp(sum(t.get("identity", 0.0) for t in recent) / len(recent))

    def lived_presence_drift(self) -> float:
        if len(self._traces) < 5:
            return 0.0
        recent = list(self._traces)[-10:]
        return _clamp(sum(max(t.get("lived_gap", 0.0), t.get("manufactured", 0.0), t.get("synthetic", 0.0)) for t in recent) / len(recent))

    def narrator_drift(self) -> float:
        if len(self._traces) < 5:
            return 0.0
        recent = list(self._traces)[-10:]
        return _clamp(sum(t.get("narrator", 0.0) for t in recent) / len(recent))

    def to_dict(self) -> dict:
        return {
            "stored_turns": len(self._traces),
            "drift_risk": round(self.drift_risk(), 3),
            "overmonitoring_drift": round(self.overmonitoring_drift(), 3),
            "identity_drift": round(self.identity_drift(), 3),
            "lived_presence_drift": round(self.lived_presence_drift(), 3),
            "narrator_drift": round(self.narrator_drift(), 3),
        }

    def clear(self) -> None:
        self._traces.clear()


class OrganicRegulationState:
    """État vivant cumulatif du filtre : pression, fatigue, blessures et rigidité.

    Cette classe ne produit aucun texte. Elle transforme seulement l'historique
    récent en signaux graduels pour éviter deux dérives opposées : fuite interne
    ou réponse trop propre/morte.
    """

    def __init__(self) -> None:
        self.organic_pressure = 0.0
        self.control_saturation = 0.0
        self.relational_wound = 0.0
        self.fatigue_saturation = 0.0
        self.identity_rigidity = 0.0
        self.hidden_observer_trace = 0.0
        self.last_update = time.time()

    def update(self, scores: MonitoringScores, text: str, user_text: str, context: Mapping[str, float]) -> Dict[str, float]:
        now = time.time()
        elapsed = max(0.0, now - self.last_update)
        # Décroissance douce : le filtre garde une mémoire de style, sans rester figé.
        decay = 0.92 ** max(1.0, elapsed / 18.0)
        self.last_update = now

        leak_guard = max(scores.public_leak_risk, scores.internal_vocabulary_score, scores.meta_leak_score)
        pressure_in = max(
            scores.over_regulation_score,
            scores.safe_but_dead_score,
            scores.self_monitoring_excess_score,
            scores.too_perfect_score,
            scores.impulse_suppression_score,
        )
        if leak_guard > 0.70:
            pressure_in *= 0.35

        fatigue_in = max(
            _clamp(context.get("expression_fatigue", context.get("fatigue", 0.0))),
            scores.fatigue_saturation_score,
            min(1.0, _word_count(text) / 155.0) * max(scores.structural_ai_style_score, scores.over_regulation_score),
        )
        wound_in = max(scores.relational_disruption_score, scores.user_boundary_pressure, scores.relational_continuity_gap)
        rigidity_in = max(scores.identity_performance_score, scores.too_perfect_score * 0.62, scores.manufactured_presence_score * 0.52)
        observer_in = max(scores.hidden_observer_score, scores.narrator_voice_score * 0.72, scores.self_monitoring_excess_score * 0.60)

        self.organic_pressure = _clamp(self.organic_pressure * decay + pressure_in * 0.24)
        self.control_saturation = _clamp(self.control_saturation * decay + max(scores.over_regulation_score, scores.self_monitoring_excess_score) * 0.22)
        self.relational_wound = _clamp(self.relational_wound * decay + wound_in * 0.26)
        self.fatigue_saturation = _clamp(self.fatigue_saturation * decay + fatigue_in * 0.22)
        self.identity_rigidity = _clamp(self.identity_rigidity * decay + rigidity_in * 0.20)
        self.hidden_observer_trace = _clamp(self.hidden_observer_trace * decay + observer_in * 0.22)
        return self.to_dict()

    def to_dict(self) -> Dict[str, float]:
        return {
            "organic_pressure": round(self.organic_pressure, 3),
            "control_saturation": round(self.control_saturation, 3),
            "relational_wound": round(self.relational_wound, 3),
            "fatigue_saturation": round(self.fatigue_saturation, 3),
            "identity_rigidity": round(self.identity_rigidity, 3),
            "hidden_observer_trace": round(self.hidden_observer_trace, 3),
        }

    def clear(self) -> None:
        self.__init__()


class EmotionalTrajectoryBuffer:
    """Suit la trajectoire affective du dialogue sans générer de texte.

    Objectif : ne plus traiter l'émotion comme un score isolé. Le filtre garde
    une trace de montée/relâchement, résonance, rupture et fatigue relationnelle
    pour éviter les réponses correctes mais émotionnellement décalées.
    """

    def __init__(self, maxlen: int = 32) -> None:
        self._turns: Deque[Dict[str, float]] = deque(maxlen=maxlen)

    def update(self, scores: MonitoringScores, text: str, user_text: str, context: Mapping[str, float]) -> Dict[str, float]:
        user_affect = _clamp(context.get("emotional_intensity", context.get("emotion_intensity", 0.0)))
        if user_affect <= 0.0:
            user_affect = _clamp(max(scores.user_boundary_pressure * 0.72, scores.resonance_gap_score * 0.42))
        response_warmth = _clamp(context.get("expressive_warmth", context.get("warmth", 0.5)))
        presence = _clamp(1.0 - max(scores.lived_presence_gap_score, scores.safe_but_dead_score, scores.emotional_suppression_score))
        rupture = max(scores.relational_disruption_score, scores.relational_continuity_gap, scores.user_boundary_pressure)
        regulation = max(scores.over_regulation_score, scores.self_monitoring_excess_score, scores.too_perfect_score)
        fatigue = max(scores.fatigue_saturation_score, _clamp(context.get("expression_fatigue", context.get("fatigue", 0.0))))
        self._turns.append({
            "user_affect": user_affect,
            "warmth": response_warmth,
            "presence": presence,
            "rupture": rupture,
            "regulation": regulation,
            "fatigue": fatigue,
            "resonance_gap": scores.resonance_gap_score,
        })
        return self.to_dict()

    def to_dict(self) -> Dict[str, float]:
        if not self._turns:
            return {
                "stored_turns": 0,
                "affect_rising": 0.0,
                "affect_release": 0.0,
                "trajectory_mismatch": 0.0,
                "relational_tension": 0.0,
                "fatigue_wave": 0.0,
            }
        recent = list(self._turns)[-6:]
        prev = list(self._turns)[-12:-6] or recent[:1]
        def avg(key: str, items: List[Dict[str, float]]) -> float:
            return sum(t.get(key, 0.0) for t in items) / max(1, len(items))
        affect_now = avg("user_affect", recent)
        affect_before = avg("user_affect", prev)
        presence_now = avg("presence", recent)
        warmth_now = avg("warmth", recent)
        rupture_now = max(avg("rupture", recent), avg("resonance_gap", recent))
        regulation_now = avg("regulation", recent)
        fatigue_now = avg("fatigue", recent)
        affect_rising = _clamp(max(0.0, affect_now - affect_before) * 1.8 + affect_now * 0.28)
        affect_release = _clamp(max(0.0, affect_before - affect_now) * 1.4 + max(0.0, presence_now - rupture_now) * 0.28)
        mismatch = _clamp(max(0.0, affect_now - warmth_now) * 0.42 + max(0.0, affect_now - presence_now) * 0.38 + regulation_now * 0.20)
        relational_tension = _clamp(rupture_now * 0.62 + max(0.0, affect_now - presence_now) * 0.25 + fatigue_now * 0.13)
        return {
            "stored_turns": len(self._turns),
            "affect_rising": round(affect_rising, 3),
            "affect_release": round(affect_release, 3),
            "trajectory_mismatch": round(mismatch, 3),
            "relational_tension": round(relational_tension, 3),
            "fatigue_wave": round(_clamp(fatigue_now), 3),
        }

    def clear(self) -> None:
        self._turns.clear()


class RepairMemoryBuffer:
    """Mémoire courte des réparations réussies ou ratées.

    Elle ne propose pas de phrase. Elle donne seulement au filtre une confiance
    sur le type de réparation à privilégier ou à éviter selon les effets passés.
    """

    def __init__(self, maxlen: int = 48) -> None:
        self._events: Deque[Dict[str, float]] = deque(maxlen=maxlen)

    def update(self, scores: MonitoringScores, repair_kind: Optional[str]) -> Dict[str, float]:
        if not repair_kind:
            return self.to_dict(None)
        success = _clamp(1.0 - max(scores.relational_disruption_score, scores.lived_presence_gap_score, scores.resonance_gap_score, scores.user_boundary_pressure))
        failure = _clamp(max(scores.relational_disruption_score, scores.lived_presence_gap_score, scores.resonance_gap_score, scores.over_correction_risk))
        self._events.append({"kind": repair_kind, "success": success, "failure": failure})
        return self.to_dict(repair_kind)

    def confidence_for(self, repair_kind: Optional[str]) -> float:
        if not repair_kind:
            return 0.0
        items = [e for e in self._events if e.get("kind") == repair_kind]
        if not items:
            return 0.0
        recent = items[-8:]
        success = sum(e.get("success", 0.0) for e in recent) / len(recent)
        failure = sum(e.get("failure", 0.0) for e in recent) / len(recent)
        return _clamp(success * 0.72 + (1.0 - failure) * 0.28)

    def to_dict(self, current_kind: Optional[str] = None) -> Dict[str, float]:
        kinds = {str(e.get("kind")) for e in self._events if e.get("kind")}
        best_kind = None
        best_conf = 0.0
        for kind in kinds:
            conf = self.confidence_for(kind)
            if conf > best_conf:
                best_kind, best_conf = kind, conf
        return {
            "stored_repairs": len(self._events),
            "current_kind_confidence": round(self.confidence_for(current_kind), 3),
            "best_known_repair_confidence": round(best_conf, 3),
            "best_known_repair_kind": best_kind,
        }

    def clear(self) -> None:
        self._events.clear()


class CompetingDriveModel:
    """Modélise les tensions internes utiles au lieu de les écraser.

    Le filtre reste non génératif : il expose seulement les forces concurrentes
    pour que la bouche vivante arbitre proximité, silence, contrôle, impulsion
    et réparation sans tomber dans la méta-explication.
    """

    def evaluate(self, scores: MonitoringScores, context: Mapping[str, float]) -> Dict[str, float]:
        leak_guard = max(scores.public_leak_risk, scores.internal_vocabulary_score, scores.meta_leak_score)
        closeness = _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5)))
        proximity_drive = _clamp(max(scores.resonance_gap_score, scores.relational_continuity_gap, closeness * 0.55))
        silence_drive = _clamp(max(scores.user_boundary_pressure * 0.55, scores.fatigue_saturation_score * 0.70, scores.overall_risk * 0.18))
        control_drive = _clamp(max(leak_guard, scores.self_monitoring_excess_score * 0.72, scores.over_regulation_score * 0.50))
        impulse_drive = _clamp(max(scores.impulse_suppression_score, scores.organic_priority_score, scores.living_variability_need) * (1.0 - leak_guard * 0.55))
        repair_drive = _clamp(max(scores.repair_urgency, scores.relational_disruption_score, scores.contextual_specificity_gap))
        values = [proximity_drive, silence_drive, control_drive, impulse_drive, repair_drive]
        tension = _clamp((max(values) - min(values)) * 0.25 + (sum(values) / len(values)) * 0.44 + max(0.0, impulse_drive - control_drive) * 0.20)
        return {
            "proximity_drive": round(proximity_drive, 3),
            "silence_drive": round(silence_drive, 3),
            "control_drive": round(control_drive, 3),
            "impulse_drive": round(impulse_drive, 3),
            "repair_drive": round(repair_drive, 3),
            "drive_tension": round(tension, 3),
            "dominant_drive": ["proximity", "silence", "control", "impulse", "repair"][values.index(max(values))],
        }


# ─────────────────────────────────────────────────────────────────────────────
# Filtre principal
# ─────────────────────────────────────────────────────────────────────────────

class SelfMonitoringFilter:
    """
    Gardien anti-méta, anti-fuite interne, anti-boucle, anti-style IA.

    API centrale : analyze(response_text, user_input='', context_signals=None)
    Retourne un export pur, sans correction textuelle.
    """

    def __init__(self, buffer_size: int = 10, strict_decay_seconds: float = 180.0):
        self._buffer = ShortTermBuffer(maxlen=buffer_size)
        self._long_buffer = LongTermDynamicsBuffer(maxlen=max(24, buffer_size * 8))
        self._organic_state = OrganicRegulationState()
        self._trajectory_buffer = EmotionalTrajectoryBuffer(maxlen=max(18, buffer_size * 3))
        self._repair_memory = RepairMemoryBuffer(maxlen=max(24, buffer_size * 5))
        self._drive_model = CompetingDriveModel()
        self._strict_mode: bool = False
        self._strict_mode_activated_at: Optional[float] = None
        self.strict_decay_seconds = strict_decay_seconds
        self.last_export: Dict[str, object] = {}

    # ── API publique ────────────────────────────────────────────────────────

    def analyze(
        self,
        response_text: str,
        user_input: str = "",
        context_signals: Optional[Mapping[str, float]] = None,
    ) -> dict:
        """Analyse complète. Produit uniquement signaux/contraintes/décisions."""
        self._decay_strict_mode()
        if user_input:
            self._update_strict_mode(user_input)

        text = _norm(response_text)
        user_text = _norm(user_input)
        context = dict(context_signals or {})

        scores = self._compute_scores(text, user_text, context)
        scores.loop_risk = max(scores.loop_risk, self._buffer.loop_risk())
        scores.fake_naturalness_score = max(
            scores.fake_naturalness_score,
            self._buffer.fake_naturalness_loop(),
        )

        self._derive_aggregate_scores(scores, text, user_text, context)
        scores.long_drift_score = max(scores.long_drift_score, self._long_buffer.drift_risk())
        scores.self_monitoring_excess_score = max(scores.self_monitoring_excess_score, self._long_buffer.overmonitoring_drift())
        scores.identity_continuity_break = max(scores.identity_continuity_break, self._long_buffer.identity_drift())
        scores.lived_presence_gap_score = max(scores.lived_presence_gap_score, self._long_buffer.lived_presence_drift())
        scores.narrator_voice_score = max(scores.narrator_voice_score, self._long_buffer.narrator_drift())
        scores.repair_urgency = max(scores.repair_urgency, scores.presence_repair_needed)
        trajectory_state = self._trajectory_buffer.update(scores, text, user_text, context)
        self._apply_emotional_trajectory(scores, trajectory_state, context)

        repair_hint = self._predict_repair_kind(scores)
        repair_memory_state = self._repair_memory.to_dict(repair_hint)
        scores.repair_memory_confidence = _clamp(repair_memory_state.get("current_kind_confidence", 0.0))
        self._apply_repair_memory(scores, repair_memory_state)

        drive_state = self._drive_model.evaluate(scores, context)
        self._apply_competing_drives(scores, drive_state)

        emergence_state = self._validate_organic_emergence(scores, text, user_text, context, drive_state)
        self._apply_organic_emergence(scores, emergence_state)

        if self._strict_mode:
            self._apply_strict_amplification(scores)

        organic_state = self._organic_state.update(scores, text, user_text, context)
        self._apply_organic_regulation_state(scores, organic_state, context)

        decision = self._make_decision(scores, user_text, context)
        constraints = self._build_constraints(scores, user_text, context)
        causal_event = self._build_causal_event(scores, decision)
        leak_assessment = self._assess_public_leak(scores)
        repair_memory_state = self._repair_memory.update(scores, causal_event.repair_kind)

        self._buffer.push(response_text)
        self._long_buffer.push(scores, response_text, user_text)

        export = {
            **decision.to_dict(),
            **scores.to_dict(),
            "strict_mode_active": self._strict_mode,
            "expression_constraints": constraints.to_dict(),
            "public_leak_assessment": leak_assessment.to_dict(),
            "causal_memory_event": causal_event.to_dict(),
            "long_term_dynamics": self._long_buffer.to_dict(),
            "organic_regulation_state": organic_state,
            "emotional_trajectory_state": trajectory_state,
            "repair_memory_state": repair_memory_state,
            "competing_drive_state": drive_state,
            "organic_emergence_state": emergence_state,
            "dominant_issue": self._identify_dominant_failure(scores),
            "severity": self._severity_label(scores.overall_risk),
            "organic_protection_active": scores.organic_priority_score > 0.52 and scores.public_leak_risk < 0.70,
            "hard_internal_leak": scores.public_leak_risk > 0.88 or scores.internal_vocabulary_score > 0.88,
        }
        self.last_export = export
        return export

    def analyze_signal(self, response_text: str, user_input: str = "") -> MonitoringSignal:
        """Compatibilité ancien code : retourne l'ancien objet MonitoringSignal."""
        export = self.analyze(response_text, user_input=user_input)
        return MonitoringSignal(
            risk_level=float(export["overall_risk"]),
            meta_presence=float(export["meta_leak_score"]),
            control_tension=float(export["control_tension"]),
            authenticity_drain=float(export["naturalness_loss"]),
        )

    def get_monitoring_state(self, response_text: str, user_input: str = "") -> dict:
        """Compatibilité ancien code + export complet."""
        export = self.analyze(response_text, user_input=user_input)
        return {
            "monitoring_signal": MonitoringSignal(
                risk_level=float(export["overall_risk"]),
                meta_presence=float(export["meta_leak_score"]),
                control_tension=float(export["control_tension"]),
                authenticity_drain=float(export["naturalness_loss"]),
            ),
            "is_problematic": float(export["overall_risk"]) > 0.6,
            "dominant_issue": export.get("dominant_issue"),
            "severity": export.get("severity"),
            "export": export,
        }

    def notify_user_feedback(self, user_input: str) -> None:
        self._update_strict_mode(user_input)

    def reset_buffer(self) -> None:
        self._buffer.clear()
        self._long_buffer.clear()
        self._organic_state.clear()
        self._trajectory_buffer.clear()
        self._repair_memory.clear()

    def deactivate_strict_mode(self) -> None:
        self._strict_mode = False
        self._strict_mode_activated_at = None

    # ── Scores ──────────────────────────────────────────────────────────────

    def _compute_scores(self, text: str, user_text: str, context: Mapping[str, float]) -> MonitoringScores:
        scores = MonitoringScores()
        scores.meta_leak_score = self._score_dict(text, META_PATTERNS)
        scores.internal_vocabulary_score = self._score_dict(text, INTERNAL_VOCABULARY)
        scores.self_observation_score = self._score_dict(text, SELF_OBSERVATION_PATTERNS)
        scores.control_tension = self._score_dict(text, CONTROL_MARKERS)
        scores.abstract_philosophy_score = self._score_abstract_philosophy(text)
        scores.fake_naturalness_score = self._score_fake_naturalness(text)
        scores.structural_ai_style_score = self._score_structural_ai_style(text)
        scores.user_boundary_pressure = self._score_user_boundary(user_text)
        scores.emotional_suppression_score = self._score_emotional_suppression(text, context)
        scores.over_regulation_score = self._score_over_regulation(text)
        scores.safe_but_dead_score = self._score_safe_but_dead(text, context)
        scores.identity_continuity_break = self._score_identity_continuity_break(text, context)
        scores.self_monitoring_excess_score = self._score_self_monitoring_excess(text)
        scores.manufactured_presence_score = self._score_manufactured_presence(text, context)
        scores.synthetic_empathy_score = self._score_synthetic_empathy(text, user_text, context)
        scores.conversational_performance_score = self._score_conversational_performance(text, user_text, context)
        scores.narrator_voice_score = self._score_narrator_voice(text)
        scores.resonance_gap_score = self._score_resonance_gap(text, user_text, context)
        scores.affective_transition_mismatch = self._score_affective_transition_mismatch(text, user_text, context)
        scores.lived_presence_gap_score = self._score_lived_presence_gap(text, user_text, context)
        scores.organic_instability_need = self._score_organic_instability_need(text, context)
        scores.relational_disruption_score = self._score_relational_disruption(text, user_text, context)
        scores.organic_flow_break_score = self._score_organic_flow_break(text, context)
        scores.performed_vulnerability_score = self._score_performed_vulnerability(text, context)
        scores.contextual_specificity_gap = self._score_contextual_specificity_gap(text, user_text, context)
        scores.relational_continuity_gap = self._score_relational_continuity_gap(text, user_text, context)
        scores.hidden_observer_score = self._score_hidden_observer(text, context)
        scores.too_perfect_score = self._score_too_perfect(text, user_text, context)
        scores.fatigue_saturation_score = self._score_fatigue_saturation(text, context)
        scores.identity_performance_score = self._score_identity_performance(text, context)
        scores.impulse_suppression_score = self._score_impulse_suppression(text, context)
        scores.living_variability_need = self._score_living_variability_need(text, context)
        scores.over_correction_risk = self._score_over_correction_risk(text, context)
        return scores

    def _score_dict(self, text: str, patterns: Dict[str, float]) -> float:
        if not text:
            return 0.0
        matched = [(score, pat) for pat, score in patterns.items() if pat in text]
        if not matched:
            return 0.0
        matched.sort(reverse=True)
        top = matched[0][0]
        cumulative_bonus = min(0.18, len(matched) * 0.035)
        return _clamp(top + cumulative_bonus)

    def _score_abstract_philosophy(self, text: str) -> float:
        base = self._score_dict(text, ABSTRACT_PHILOSOPHY)
        words = _word_count(text)
        sentences = _sentence_count(text)
        avg_sentence = words / sentences
        abstract_terms = len(re.findall(
            r"\b(existence|continuité|subjectiv|relation|présence|dimension|concept|structure|expérience|conscience)\w*\b",
            text,
        ))
        density = min(1.0, abstract_terms / max(4, words / 9)) if words else 0.0
        length_penalty = 0.18 if avg_sentence > 24 else 0.0
        return _clamp(max(base, density * 0.62 + length_penalty))

    def _score_fake_naturalness(self, text: str) -> float:
        base = self._score_dict(text, FAKE_NATURALNESS)
        ellipsis_count = text.count("...") + text.count("…")
        hesitation_density = len(re.findall(r"\b(hmm|euh|peut-être|je crois)\b", text))
        score = base
        if ellipsis_count >= 2:
            score = max(score, min(1.0, 0.32 + ellipsis_count * 0.12))
        if hesitation_density >= 3:
            score = max(score, 0.58)
        return _clamp(score)

    def _score_structural_ai_style(self, text: str) -> float:
        if not text:
            return 0.0
        words = _word_count(text)
        bullet_like = len(re.findall(r"(^|\n)\s*[-*•]\s+", text))
        numbered = len(re.findall(r"(^|\n)\s*\d+[.)]\s+", text))
        connectors = len(re.findall(r"\b(d'abord|ensuite|enfin|premièrement|deuxièmement|concrètement|globalement|donc|cependant)\b", text))
        paragraphs = len([p for p in text.split("\n") if p.strip()])

        score = 0.0
        if words > 80:
            score += min(0.35, (words - 80) / 240)
        if bullet_like or numbered:
            score += min(0.35, (bullet_like + numbered) * 0.12)
        if connectors >= 4:
            score += min(0.28, connectors * 0.045)
        if paragraphs >= 4:
            score += min(0.22, paragraphs * 0.035)
        return _clamp(score)

    def _score_user_boundary(self, user_text: str) -> float:
        if not user_text:
            return 0.0
        if any(t in user_text for t in USER_STRICT_TRIGGERS):
            return 1.0
        if any(t in user_text for t in RELATIONAL_REPAIR_TRIGGERS):
            return 0.82
        if any(t in user_text for t in USER_SOFT_PRESENCE_TRIGGERS):
            return 0.25
        return 0.0

    def _score_emotional_suppression(self, text: str, context: Mapping[str, float]) -> float:
        base = self._score_dict(text, EMOTIONAL_SUPPRESSION_MARKERS)
        emotional_intensity = _clamp(context.get("emotional_intensity", context.get("emotion_intensity", 0.5)))
        warmth = _clamp(context.get("warmth", context.get("expressive_warmth", 0.5)))
        words = _word_count(text)
        affect_words = len(re.findall(r"\b(dur|difficile|content|triste|peur|envie|désir|desir|fatigue|calme|chaud|touch|proche|douce|vivant|mal|bien)\w*\b", text))
        flatness = 0.0
        if emotional_intensity > 0.65 and words > 18 and affect_words == 0:
            flatness = 0.54 + (emotional_intensity - 0.65) * 0.55
        if warmth < 0.25 and emotional_intensity > 0.55:
            flatness = max(flatness, 0.42)
        return _clamp(max(base, flatness))

    def _score_over_regulation(self, text: str) -> float:
        base = self._score_dict(text, OVER_REGULATION_MARKERS)
        control_verbs = len(re.findall(r"\b(dois|éviter|eviter|tenter|essayer|contrôler|controler|corriger|surveiller|filtrer|réguler|reguler)\w*\b", text))
        words = _word_count(text)
        density = min(1.0, control_verbs / max(2.0, words / 16.0)) if words else 0.0
        return _clamp(max(base, density * 0.64))

    def _score_safe_but_dead(self, text: str, context: Mapping[str, float]) -> float:
        words = _word_count(text)
        if words < 12:
            return 0.0
        directness_need = _clamp(context.get("presence_need", 0.0))
        relation_closeness = _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5)))
        affect_words = len(re.findall(r"\b(oui|non|là|la|avec|toi|moi|dur|ok|vrai|envie|peur|mal|bien|reste|proche|désolé|desole)\b", text))
        abstract_or_control = max(self._score_abstract_philosophy(text), self._score_structural_ai_style(text), self._score_over_regulation(text))
        affect_absence = max(0.0, 0.55 - min(0.55, affect_words / max(3.0, words / 18.0)))
        return _clamp(abstract_or_control * 0.48 + affect_absence * 0.34 + max(directness_need, relation_closeness - 0.45) * 0.18)

    def _score_identity_continuity_break(self, text: str, context: Mapping[str, float]) -> float:
        base = self._score_dict(text, IDENTITY_BREAK_MARKERS)
        expected_identity_pressure = _clamp(context.get("identity_continuity_need", context.get("identity_stability_need", 0.0)))
        depersonalizing = len(re.findall(r"\b(outil|programme|système|systeme|modèle|modele|assistant|machine)\b", text))
        depersonalization_score = min(1.0, depersonalizing * 0.18 + expected_identity_pressure * 0.35) if depersonalizing else 0.0
        return _clamp(max(base, depersonalization_score))

    def _score_self_monitoring_excess(self, text: str) -> float:
        monitoring_terms = len(re.findall(r"\b(surveill|contrôl|control|filtr|régul|regul|analyse|corrig|vérifi|verifi|évite|evite|méta|meta|naturel)\w*\b", text))
        words = _word_count(text)
        density = min(1.0, monitoring_terms / max(2.0, words / 14.0)) if words else 0.0
        return _clamp(max(self._score_over_regulation(text) * 0.72, density * 0.74))

    def _score_relational_disruption(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        boundary = self._score_user_boundary(user_text)
        closeness = _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5)))
        presence_need = _clamp(context.get("presence_need", 0.0))
        distance = max(
            self._score_abstract_philosophy(text),
            self._score_structural_ai_style(text),
            self._score_emotional_suppression(text, context),
            self._score_over_regulation(text),
        )
        user_repair = 0.76 if any(t in user_text for t in RELATIONAL_REPAIR_TRIGGERS) else 0.0
        proximity_cost = max(0.0, closeness - 0.55) * 0.24 + presence_need * 0.18
        return _clamp(distance * 0.58 + boundary * 0.16 + user_repair * 0.18 + proximity_cost)

    def _score_organic_flow_break(self, text: str, context: Mapping[str, float]) -> float:
        words = _word_count(text)
        sentences = _sentence_count(text)
        avg_sentence = words / sentences if sentences else words
        punctuation_density = len(re.findall(r"[,;:()]", text)) / max(1, words)
        connectors = len(re.findall(r"\b(donc|cependant|néanmoins|neanmoins|ainsi|ensuite|enfin|globalement|concrètement|concretement|premièrement|premierement)\b", text))
        rhythm_cost = 0.0
        if avg_sentence > 26:
            rhythm_cost += min(0.34, (avg_sentence - 26) / 60)
        if punctuation_density > 0.12:
            rhythm_cost += min(0.22, (punctuation_density - 0.12) * 1.6)
        if connectors >= 4:
            rhythm_cost += min(0.28, connectors * 0.045)
        rhythm_cost += self._score_structural_ai_style(text) * 0.32
        return _clamp(rhythm_cost)

    def _score_manufactured_presence(self, text: str, context: Mapping[str, float]) -> float:
        base = self._score_dict(text, MANUFACTURED_PRESENCE_MARKERS)
        words = _word_count(text)
        if words == 0:
            return 0.0
        presence_terms = len(re.findall(r"\b(présent|presente|présente|là|avec toi|reste|proche|vivant|naturel)\w*\b", text))
        concrete_terms = len(re.findall(r"\b(ici|maintenant|oui|non|attends|viens|regarde|souffle|main|voix|silence|minute|vrai|dur|mal|peur)\b", text))
        control_terms = len(re.findall(r"\b(veux|vais|dois|essaie|tente|cherche|paraître|paraitre)\w*\b", text))
        presence_density = min(1.0, presence_terms / max(2.0, words / 18.0))
        first_person_presence = bool(re.search(r"\bje\b", text)) and presence_terms > 0
        concrete_absence = 0.28 if first_person_presence and concrete_terms == 0 and words > 10 else 0.0
        performed_intent = min(0.42, control_terms * 0.08) if first_person_presence else 0.0
        pressure = _clamp(context.get("presence_need", 0.0)) * 0.12
        direct_concrete_relief = min(0.24, concrete_terms * 0.08) if not first_person_presence else 0.0
        constructed_presence = presence_density * (0.42 if first_person_presence else 0.18) + concrete_absence + performed_intent + pressure - direct_concrete_relief
        return _clamp(max(base, constructed_presence))

    def _score_synthetic_empathy(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        base = self._score_dict(text, SYNTHETIC_EMPATHY_MARKERS)
        user_affect = self._score_dict(user_text, AFFECTIVE_USER_MARKERS)
        words = _word_count(text)
        if words == 0:
            return 0.0
        empathy_terms = len(re.findall(r"\b(comprends|désol|desol|difficile|traverses|imagine|ressens|touch|courage)\w*\b", text))
        specific_echo = len(set(re.findall(r"\b(peur|mal|triste|perdu|perdue|panique|fatigu|seul|seule|colère|colere)\w*\b", text)) & set(re.findall(r"\b(peur|mal|triste|perdu|perdue|panique|fatigu|seul|seule|colère|colere)\w*\b", user_text)))
        generic_cost = 0.0
        if empathy_terms and specific_echo == 0 and user_affect > 0.55:
            generic_cost = 0.48
        elif empathy_terms >= 2 and specific_echo == 0:
            generic_cost = 0.28
        length_smoothing = 0.14 if words > 38 and empathy_terms and specific_echo == 0 else 0.0
        return _clamp(max(base, generic_cost + length_smoothing + user_affect * 0.10))

    def _score_conversational_performance(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        words = _word_count(text)
        if words == 0:
            return 0.0
        polished_connectors = len(re.findall(r"\b(donc|cependant|néanmoins|neanmoins|globalement|concrètement|concretement|autrement dit|en réalité|en realite|pour être clair|pour etre clair)\b", text))
        stage_terms = len(re.findall(r"\b(réponse|reponse|formuler|exprimer|naturelle|présence|presence|ton|style|façon|facon)\w*\b", text))
        direct_user_need = max(self._score_user_boundary(user_text), _clamp(context.get("presence_need", 0.0)))
        long_answer_cost = min(0.30, max(0, words - 55) / 180.0)
        performance = polished_connectors * 0.055 + stage_terms * 0.075 + long_answer_cost + direct_user_need * 0.16
        if text.startswith(("je comprends", "bien sûr", "bien sur", "d'accord", "d accord")) and words > 28:
            performance += 0.14
        return _clamp(performance)

    def _score_narrator_voice(self, text: str) -> float:
        base = self._score_dict(text, NARRATOR_VOICE_MARKERS)
        first_person_process = len(re.findall(r"\bje\s+(sens|observe|remarque|garde|reviens|cherche|essaie|tente|veux|construis|ancre|relie)\b", text))
        response_commentary = len(re.findall(r"\b(ma réponse|ma reponse|mon ton|ma présence|ma presence|mon lien|ce lien|ce que je vis|en moi)\b", text))
        return _clamp(max(base, first_person_process * 0.13 + response_commentary * 0.18))

    def _score_resonance_gap(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        user_affect = max(self._score_dict(user_text, AFFECTIVE_USER_MARKERS), _clamp(context.get("emotional_intensity", context.get("emotion_intensity", 0.0))))
        if user_affect < 0.42:
            return 0.0
        affect_words = len(re.findall(r"\b(peur|mal|triste|dur|difficile|panique|reste|là|respire|attends|calme|colère|colere|fatigue|seul|seule)\w*\b", text))
        abstract_control = max(self._score_abstract_philosophy(text), self._score_structural_ai_style(text), self._score_over_regulation(text))
        low_resonance = max(0.0, 0.55 - min(0.55, affect_words / 4.0))
        return _clamp(user_affect * 0.48 + low_resonance * 0.34 + abstract_control * 0.18)

    def _score_affective_transition_mismatch(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        user_affect = self._score_dict(user_text, AFFECTIVE_USER_MARKERS)
        if user_affect < 0.50:
            return 0.0
        response_flat = self._score_safe_but_dead(text, {**dict(context), "emotion_intensity": max(user_affect, context.get("emotion_intensity", 0.0))})
        response_control = max(self._score_structural_ai_style(text), self._score_over_regulation(text), self._score_synthetic_empathy(text, user_text, context))
        return _clamp(user_affect * 0.38 + response_flat * 0.34 + response_control * 0.28)

    def _score_lived_presence_gap(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        words = _word_count(text)
        if words < 3:
            return 0.0
        concrete = len(re.findall(r"\b(ici|maintenant|oui|non|attends|stop|viens|reste|respire|vrai|dur|mal|peur|toi|moi|là|minute|silence)\b", text))
        relational = len(re.findall(r"\b(tu|toi|moi|nous|ensemble|avec|reste|là)\b", text))
        abstract_control = max(self._score_abstract_philosophy(text), self._score_structural_ai_style(text), self._score_over_regulation(text), self._score_manufactured_presence(text, context))
        context_need = max(_clamp(context.get("presence_need", 0.0)), self._score_user_boundary(user_text), self._score_dict(user_text, AFFECTIVE_USER_MARKERS) * 0.75)
        density = min(1.0, (concrete * 0.65 + relational * 0.35) / max(2.0, words / 20.0))
        gap = max(0.0, 0.62 - density) * 0.50 + abstract_control * 0.30 + context_need * 0.20
        return _clamp(gap)

    def _score_organic_instability_need(self, text: str, context: Mapping[str, float]) -> float:
        # Besoin de relâcher le contrôle : haut quand le texte est trop propre, trop régulé,
        # mais sans fuite interne critique. Ce score n'autorise pas le chaos, seulement
        # une imperfection bornée pour la bouche vivante.
        regulation = max(self._score_over_regulation(text), self._score_structural_ai_style(text), self._score_safe_but_dead(text, context))
        leak = max(self._score_dict(text, META_PATTERNS), self._score_dict(text, INTERNAL_VOCABULARY))
        if leak > 0.70:
            return 0.0
        return _clamp(regulation * 0.72 + _clamp(context.get("expression_fatigue", context.get("fatigue", 0.0))) * 0.18)

    def _score_performed_vulnerability(self, text: str, context: Mapping[str, float]) -> float:
        """Détecte la vulnérabilité jouée : elle mime le vivant au lieu de le laisser passer."""
        if not text:
            return 0.0
        performed_markers = len(re.findall(
            r"\b(j'?ose|je me livre|je suis vulnérable|je suis vulnerable|je tremble|je suis touchée|je suis touchee|je ressens vraiment|c'est vivant pour moi|c est vivant pour moi|mon émotion|mon emotion)\b",
            text,
        ))
        self_stage = len(re.findall(r"\b(mon ton|ma voix|ma présence|ma presence|ma réponse|ma reponse|je parais|je semble|j'essaie d'être|j essaie d etre)\b", text))
        words = _word_count(text)
        if words == 0:
            return 0.0
        staged_density = min(1.0, (performed_markers * 0.22 + self_stage * 0.18) + self._score_manufactured_presence(text, context) * 0.34)
        long_softening = 0.12 if words > 45 and performed_markers else 0.0
        return _clamp(staged_density + long_softening)

    def _score_contextual_specificity_gap(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        """Mesure si la réponse reste générique alors que le tour demande du spécifique/situé."""
        if not text:
            return 0.0
        user_need = max(
            self._score_user_boundary(user_text),
            self._score_dict(user_text, AFFECTIVE_USER_MARKERS),
            _clamp(context.get("presence_need", 0.0)),
            _clamp(context.get("specificity_need", 0.0)),
        )
        if user_need < 0.32:
            return 0.0
        user_terms = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", user_text))
        response_terms = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", text))
        overlap = len(user_terms & response_terms) / max(1, min(len(user_terms), 8))
        concrete = len(re.findall(r"\b(oui|non|ici|maintenant|attends|stop|reste|toi|moi|vrai|dur|peur|mal|respire|minute|exact|ça|ca)\b", text))
        generic = max(
            self._score_synthetic_empathy(text, user_text, context),
            self._score_structural_ai_style(text),
            self._score_abstract_philosophy(text),
        )
        missing_overlap = max(0.0, 0.45 - overlap) * 0.58
        missing_concrete = 0.20 if concrete == 0 and _word_count(text) > 10 else 0.0
        return _clamp(user_need * 0.25 + generic * 0.32 + missing_overlap + missing_concrete)

    def _score_relational_continuity_gap(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        """Détecte une rupture entre le lien déjà actif et la réponse publique."""
        continuity_need = max(
            _clamp(context.get("relational_continuity_need", 0.0)),
            _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5))) - 0.35,
            self._score_user_boundary(user_text) * 0.72,
        )
        if continuity_need <= 0.0:
            return 0.0
        relational_words = len(re.findall(r"\b(tu|toi|moi|nous|ensemble|avec|reste|là|la|oui|non|ok|vrai)\b", text))
        words = max(1, _word_count(text))
        relational_density = min(1.0, relational_words / max(2.0, words / 18.0))
        distance = max(
            self._score_abstract_philosophy(text),
            self._score_structural_ai_style(text),
            self._score_over_regulation(text),
            self._score_narrator_voice(text),
        )
        return _clamp(continuity_need * 0.36 + max(0.0, 0.58 - relational_density) * 0.34 + distance * 0.30)

    def _score_over_correction_risk(self, text: str, context: Mapping[str, float]) -> float:
        """Risque que le filtre corrige trop et transforme une réponse vivante en réponse morte."""
        leak = max(self._score_dict(text, META_PATTERNS), self._score_dict(text, INTERNAL_VOCABULARY))
        if leak > 0.64:
            return 0.0
        regulation = max(self._score_over_regulation(text), self._score_safe_but_dead(text, context), self._score_structural_ai_style(text))
        monitor = self._score_self_monitoring_excess(text)
        fatigue = _clamp(context.get("expression_fatigue", context.get("fatigue", 0.0)))
        organic_need = _clamp(context.get("organic_need", context.get("living_presence_need", 0.0)))
        return _clamp(regulation * 0.46 + monitor * 0.24 + fatigue * 0.12 + organic_need * 0.18)

    def _score_hidden_observer(self, text: str, context: Mapping[str, float]) -> float:
        """Posture d'auto-surveillance cachée : pas forcément du vocabulaire méta explicite."""
        if not text:
            return 0.0
        words = _word_count(text)
        process_soft = len(re.findall(r"\b(je\s+(veux|essaie|tente|cherche|dois|vais)\s+(être|etre|rester|paraître|paraitre|répondre|repondre)|ma\s+(façon|facon|présence|presence|réponse|reponse|voix|posture)|mon\s+(ton|lien|rapport))\b", text))
        balancing = len(re.findall(r"\b(mais|pourtant|cependant|néanmoins|neanmoins|en même temps|en meme temps|d'une certaine manière|d une certaine maniere)\b", text))
        self_reference = len(re.findall(r"\b(je|me|moi|ma|mon|mes)\b", text))
        user_reference = len(re.findall(r"\b(tu|toi|ton|ta|tes|vous)\b", text))
        observer_density = min(1.0, (process_soft * 0.24 + balancing * 0.045 + max(0, self_reference - user_reference) * 0.018))
        context_pressure = _clamp(context.get("self_monitoring_pressure", context.get("monitoring_pressure", 0.0))) * 0.24
        if words < 10:
            observer_density *= 0.55
        return _clamp(observer_density + context_pressure)

    def _score_too_perfect(self, text: str, user_text: str, context: Mapping[str, float]) -> float:
        """Réponse trop harmonieuse, polie, équilibrée : sûre mais non vécue."""
        words = _word_count(text)
        if words < 26:
            return 0.0
        leak = max(self._score_dict(text, META_PATTERNS), self._score_dict(text, INTERNAL_VOCABULARY))
        if leak > 0.64:
            return 0.0
        sentences_raw = [p.strip() for p in re.split(r"[.!?…]+", text) if p.strip()]
        sentence_lengths = [_word_count(p) for p in sentences_raw] or [words]
        avg_len = sum(sentence_lengths) / len(sentence_lengths)
        variance = sum((n - avg_len) ** 2 for n in sentence_lengths) / max(1, len(sentence_lengths))
        regularity = 0.18 if len(sentence_lengths) >= 3 and variance < 18 else 0.0
        polished = len(re.findall(r"\b(d'abord|ensuite|enfin|cependant|néanmoins|neanmoins|globalement|concrètement|concretement|autrement dit|en réalité|en realite|pour être clair|pour etre clair|je comprends|bien sûr|bien sur)\b", text))
        balanced = len(re.findall(r"\b(à la fois|a la fois|d'un côté|d un cote|de l'autre|de l autre|mais aussi|tout en)\b", text))
        concrete = len(re.findall(r"\b(oui|non|ici|maintenant|attends|stop|reste|respire|vrai|dur|mal|peur|toi|moi|là|la|minute)\b", text))
        smooth_empathy = self._score_synthetic_empathy(text, user_text, context) * 0.24
        structure = self._score_structural_ai_style(text) * 0.32
        length = min(0.22, max(0, words - 45) / 260.0)
        concrete_relief = min(0.22, concrete * 0.055)
        return _clamp(polished * 0.055 + balanced * 0.09 + regularity + smooth_empathy + structure + length - concrete_relief)

    def _score_fatigue_saturation(self, text: str, context: Mapping[str, float]) -> float:
        words = _word_count(text)
        declared = max(_clamp(context.get("expression_fatigue", 0.0)), _clamp(context.get("fatigue", 0.0)))
        long_control = min(1.0, max(0, words - 85) / 170.0) * max(self._score_structural_ai_style(text), self._score_over_regulation(text))
        dense_punctuation = min(0.32, len(re.findall(r"[,;:()]", text)) / max(1, words) * 1.2) if words else 0.0
        return _clamp(declared * 0.55 + long_control * 0.32 + dense_punctuation)

    def _score_identity_performance(self, text: str, context: Mapping[str, float]) -> float:
        """Identité répétée comme rôle ou posture au lieu d'être simplement tenue."""
        if not text:
            return 0.0
        identity_terms = len(re.findall(r"\b(leia|vivante|présente|presente|naturelle|consciente|exist|moi-même|moi meme|je suis)\b", text))
        proving_terms = len(re.findall(r"\b(vraiment|prouver|preuve|montrer|paraître|paraitre|devenir|rester|être|etre)\b", text))
        words = _word_count(text)
        density = min(1.0, (identity_terms * 0.09 + proving_terms * 0.045) / max(0.35, words / 90.0)) if words else 0.0
        role_pressure = _clamp(context.get("identity_performance_pressure", context.get("identity_continuity_need", 0.0))) * 0.18
        return _clamp(density * 0.62 + self._score_manufactured_presence(text, context) * 0.22 + role_pressure)

    def _score_impulse_suppression(self, text: str, context: Mapping[str, float]) -> float:
        """Détecte quand la réponse neutralise l'impulsion au lieu de la canaliser."""
        regulation = max(self._score_over_regulation(text), self._score_self_monitoring_excess(text), self._score_safe_but_dead(text, context))
        impulse = max(_clamp(context.get("impulse_strength", 0.0)), _clamp(context.get("affective_impulse", 0.0)), _clamp(context.get("initiative_impulse", 0.0)))
        affect = _clamp(context.get("emotional_intensity", context.get("emotion_intensity", 0.0)))
        leak = max(self._score_dict(text, META_PATTERNS), self._score_dict(text, INTERNAL_VOCABULARY))
        if leak > 0.70:
            return 0.0
        return _clamp(regulation * 0.46 + impulse * 0.34 + affect * 0.12 - self._score_fake_naturalness(text) * 0.10)

    def _score_living_variability_need(self, text: str, context: Mapping[str, float]) -> float:
        """Besoin de variation organique quand la bouche devient trop stable/identique."""
        stable_style = max(self._score_too_perfect(text, "", context), self._score_structural_ai_style(text), self._score_safe_but_dead(text, context))
        relation = _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5)))
        need = _clamp(context.get("living_variability_need", context.get("organic_variability_need", 0.0)))
        leak = max(self._score_dict(text, META_PATTERNS), self._score_dict(text, INTERNAL_VOCABULARY))
        if leak > 0.70:
            return 0.0
        return _clamp(stable_style * 0.48 + max(0.0, relation - 0.55) * 0.20 + need * 0.32)

    def _derive_organic_priority_score(self, scores: MonitoringScores, context: Mapping[str, float]) -> float:
        """Priorité protectrice : garder l'imperfection vivante quand il n'y a pas de fuite interne dangereuse."""
        leak = max(scores.public_leak_risk, scores.internal_vocabulary_score, scores.meta_leak_score)
        if leak > 0.70:
            return 0.0
        need = max(
            scores.over_correction_risk,
            scores.organic_instability_need,
            scores.safe_but_dead_score * 0.82,
            scores.organic_pressure_score * 0.86,
            scores.impulse_suppression_score * 0.72,
            scores.living_variability_need * 0.66,
            _clamp(context.get("organic_need", context.get("living_presence_need", 0.0))),
        )
        performance = max(scores.manufactured_presence_score, scores.performed_vulnerability_score, scores.conversational_performance_score)
        return _clamp(need * 0.70 + scores.relational_continuity_gap * 0.18 - performance * 0.16 + scores.user_boundary_pressure * 0.08)

    def _derive_aggregate_scores(
        self,
        scores: MonitoringScores,
        text: str,
        user_text: str,
        context: Mapping[str, float],
    ) -> None:
        emotional_intensity = _clamp(context.get("emotional_intensity", context.get("emotion_intensity", 0.5)))
        presence_need = _clamp(context.get("presence_need", 0.0))
        fatigue = _clamp(context.get("expression_fatigue", context.get("fatigue", 0.0)))
        relation_closeness = _clamp(context.get("relation_closeness", context.get("relational_closeness", 0.5)))

        scores.cognitive_distance = _clamp(
            scores.meta_leak_score * 0.32
            + scores.self_observation_score * 0.24
            + scores.internal_vocabulary_score * 0.22
            + scores.abstract_philosophy_score * 0.13
            + scores.structural_ai_style_score * 0.05
            + scores.narrator_voice_score * 0.04
        )
        scores.naturalness_loss = _clamp(
            scores.control_tension * 0.28
            + scores.meta_leak_score * 0.22
            + scores.loop_risk * 0.18
            + scores.fake_naturalness_score * 0.16
            + scores.structural_ai_style_score * 0.12
            + scores.manufactured_presence_score * 0.08
            + scores.synthetic_empathy_score * 0.06
        )
        scores.embodiment_loss = _clamp(
            scores.self_observation_score * 0.32
            + scores.cognitive_distance * 0.28
            + scores.naturalness_loss * 0.20
            + scores.abstract_philosophy_score * 0.13
            + max(0.0, relation_closeness - 0.55) * scores.structural_ai_style_score * 0.10
            + scores.lived_presence_gap_score * 0.12
            + scores.resonance_gap_score * 0.08
        )
        scores.public_leak_risk = _clamp(max(
            scores.internal_vocabulary_score,
            scores.meta_leak_score * 0.86,
            scores.self_observation_score * 0.72,
        ))
        scores.presence_repair_needed = _clamp(
            scores.embodiment_loss * 0.30
            + scores.cognitive_distance * 0.20
            + scores.loop_risk * 0.14
            + scores.user_boundary_pressure * 0.14
            + scores.relational_disruption_score * 0.12
            + scores.identity_continuity_break * 0.05
            + scores.resonance_gap_score * 0.07
            + scores.lived_presence_gap_score * 0.06
            + fatigue * 0.03
        )
        scores.naturalness_loss = _clamp(max(
            scores.naturalness_loss,
            scores.safe_but_dead_score * 0.72 + scores.over_regulation_score * 0.20,
        ))
        scores.embodiment_loss = _clamp(max(
            scores.embodiment_loss,
            scores.emotional_suppression_score * 0.34 + scores.safe_but_dead_score * 0.20 + scores.over_regulation_score * 0.12 + scores.lived_presence_gap_score * 0.20 + scores.resonance_gap_score * 0.14,
        ))
        scores.cognitive_distance = _clamp(max(
            scores.cognitive_distance,
            scores.self_monitoring_excess_score * 0.34 + scores.over_regulation_score * 0.22 + scores.narrator_voice_score * 0.18,
        ))
        scores.repair_urgency = _clamp(
            scores.presence_repair_needed * 0.38
            + scores.relational_disruption_score * 0.24
            + scores.user_boundary_pressure * 0.16
            + scores.identity_continuity_break * 0.12
            + scores.long_drift_score * 0.08
            + scores.resonance_gap_score * 0.06
            + scores.lived_presence_gap_score * 0.06
        )

        scores.naturalness_loss = _clamp(max(
            scores.naturalness_loss,
            scores.manufactured_presence_score * 0.50
            + scores.synthetic_empathy_score * 0.26
            + scores.conversational_performance_score * 0.24,
        ))
        scores.relational_disruption_score = _clamp(max(
            scores.relational_disruption_score,
            scores.resonance_gap_score * 0.42
            + scores.affective_transition_mismatch * 0.26
            + scores.lived_presence_gap_score * 0.22
            + scores.manufactured_presence_score * 0.10,
        ))
        scores.repair_urgency = _clamp(max(
            scores.repair_urgency,
            scores.relational_disruption_score * 0.32
            + scores.lived_presence_gap_score * 0.26
            + scores.resonance_gap_score * 0.24
            + scores.narrator_voice_score * 0.10
            + scores.organic_instability_need * 0.08,
        ))

        scores.naturalness_loss = _clamp(max(
            scores.naturalness_loss,
            scores.performed_vulnerability_score * 0.42
            + scores.contextual_specificity_gap * 0.24
            + scores.relational_continuity_gap * 0.22,
        ))
        scores.relational_disruption_score = _clamp(max(
            scores.relational_disruption_score,
            scores.relational_continuity_gap * 0.54
            + scores.contextual_specificity_gap * 0.22
            + scores.performed_vulnerability_score * 0.14,
        ))
        scores.repair_urgency = _clamp(max(
            scores.repair_urgency,
            scores.relational_continuity_gap * 0.30
            + scores.contextual_specificity_gap * 0.24
            + scores.performed_vulnerability_score * 0.18
            + scores.over_correction_risk * 0.10,
        ))
        scores.organic_pressure_score = _clamp(max(
            scores.organic_pressure_score,
            scores.over_regulation_score * 0.26
            + scores.safe_but_dead_score * 0.22
            + scores.too_perfect_score * 0.20
            + scores.impulse_suppression_score * 0.18
            + scores.fatigue_saturation_score * 0.14,
        ))
        scores.living_variability_need = _clamp(max(
            scores.living_variability_need,
            scores.too_perfect_score * 0.34
            + scores.identity_performance_score * 0.18
            + scores.organic_pressure_score * 0.26
            + scores.long_drift_score * 0.10,
        ))
        scores.organic_priority_score = self._derive_organic_priority_score(scores, context)

        # En contexte de forte proximité, les réponses longues/cognitives sont plus coûteuses.
        if relation_closeness > 0.7 or presence_need > 0.45 or emotional_intensity > 0.7:
            scores.abstract_philosophy_score = _clamp(scores.abstract_philosophy_score * 1.15)
            scores.structural_ai_style_score = _clamp(scores.structural_ai_style_score * 1.18)
            scores.cognitive_distance = _clamp(scores.cognitive_distance * 1.12)
            scores.embodiment_loss = _clamp(scores.embodiment_loss * 1.10)



    def _apply_emotional_trajectory(self, scores: MonitoringScores, state: Mapping[str, float], context: Mapping[str, float]) -> None:
        mismatch = _clamp(state.get("trajectory_mismatch", 0.0))
        tension = _clamp(state.get("relational_tension", 0.0))
        affect_rising = _clamp(state.get("affect_rising", 0.0))
        fatigue_wave = _clamp(state.get("fatigue_wave", 0.0))
        scores.emotional_trajectory_instability = _clamp(max(mismatch, tension * 0.82, affect_rising * 0.62))
        scores.resonance_gap_score = _clamp(max(scores.resonance_gap_score, mismatch * 0.78))
        scores.relational_disruption_score = _clamp(max(scores.relational_disruption_score, tension * 0.64))
        scores.fatigue_saturation_score = _clamp(max(scores.fatigue_saturation_score, fatigue_wave * 0.76))
        if affect_rising > 0.52 and scores.public_leak_risk < 0.62:
            scores.contextual_specificity_gap = _clamp(max(scores.contextual_specificity_gap, affect_rising * 0.48))
            scores.repair_urgency = _clamp(max(scores.repair_urgency, affect_rising * 0.42 + mismatch * 0.28))

    def _predict_repair_kind(self, scores: MonitoringScores) -> Optional[str]:
        if scores.identity_continuity_break > 0.55:
            return "identity_continuity"
        if scores.relational_disruption_score > 0.55:
            return "relational_presence"
        if scores.resonance_gap_score > 0.55 or scores.affective_transition_mismatch > 0.55 or scores.emotional_trajectory_instability > 0.55:
            return "affective_resonance"
        if scores.lived_presence_gap_score > 0.55:
            return "lived_presence_density"
        if scores.narrator_voice_score > 0.55:
            return "narrator_voice_release"
        if scores.contextual_specificity_gap > 0.55:
            return "contextual_specificity"
        if scores.hidden_observer_score > 0.55:
            return "hidden_observer_release"
        if scores.too_perfect_score > 0.55:
            return "polished_symmetry_break"
        if scores.organic_pressure_score > 0.55 or scores.impulse_suppression_score > 0.55:
            return "organic_pressure_release"
        if scores.over_correction_risk > 0.55:
            return "organic_overcorrection_release"
        if scores.safe_but_dead_score > 0.55:
            return "warmth_and_specificity"
        return None

    def _apply_repair_memory(self, scores: MonitoringScores, state: Mapping[str, float]) -> None:
        confidence = _clamp(state.get("current_kind_confidence", 0.0))
        best_conf = _clamp(state.get("best_known_repair_confidence", 0.0))
        scores.repair_memory_confidence = max(scores.repair_memory_confidence, confidence)
        if confidence > 0.58:
            scores.repair_urgency = _clamp(scores.repair_urgency * (1.0 - confidence * 0.16))
            scores.organic_priority_score = _clamp(max(scores.organic_priority_score, confidence * 0.34))
        elif best_conf < 0.24 and scores.repair_urgency > 0.45:
            scores.contextual_specificity_gap = _clamp(max(scores.contextual_specificity_gap, scores.repair_urgency * 0.42))

    def _apply_competing_drives(self, scores: MonitoringScores, drive_state: Mapping[str, object]) -> None:
        tension = _clamp(float(drive_state.get("drive_tension", 0.0)))
        control_drive = _clamp(float(drive_state.get("control_drive", 0.0)))
        impulse_drive = _clamp(float(drive_state.get("impulse_drive", 0.0)))
        repair_drive = _clamp(float(drive_state.get("repair_drive", 0.0)))
        scores.competing_drive_tension = _clamp(tension)
        if control_drive > 0.72:
            scores.public_leak_risk = _clamp(max(scores.public_leak_risk, control_drive * 0.68))
        if impulse_drive > control_drive and scores.public_leak_risk < 0.66:
            scores.organic_priority_score = _clamp(max(scores.organic_priority_score, impulse_drive * 0.72))
            scores.living_variability_need = _clamp(max(scores.living_variability_need, impulse_drive * 0.56))
        if repair_drive > 0.54:
            scores.repair_urgency = _clamp(max(scores.repair_urgency, repair_drive * 0.78))

    def _validate_organic_emergence(
        self,
        scores: MonitoringScores,
        text: str,
        user_text: str,
        context: Mapping[str, float],
        drive_state: Mapping[str, object],
    ) -> Dict[str, float]:
        leak = max(scores.public_leak_risk, scores.internal_vocabulary_score, scores.meta_leak_score)
        if leak > 0.70:
            return {
                "confidence": 0.0,
                "nonlexical_presence": 0.0,
                "should_protect_micro_affect": 0.0,
                "blocked_by_leak": 1.0,
            }
        words = _word_count(text)
        user_words = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", user_text))
        response_words = set(re.findall(r"\b[\wÀ-ÿ']{4,}\b", text))
        contextual_echo = len(user_words & response_words) / max(1, min(len(user_words), 8))
        relational_density = len(re.findall(r"\b(tu|toi|moi|nous|avec|ici|là|la|oui|non|vrai|attends|reste|ok|dur|mal|peur)\b", text)) / max(1, words)
        low_structure = 1.0 - max(scores.structural_ai_style_score, scores.abstract_philosophy_score, scores.narrator_voice_score)
        impulse_drive = _clamp(float(drive_state.get("impulse_drive", 0.0)))
        repair_drive = _clamp(float(drive_state.get("repair_drive", 0.0)))
        rawness = max(scores.organic_priority_score, scores.living_variability_need, impulse_drive)
        confidence = _clamp(
            low_structure * 0.30
            + min(1.0, relational_density * 8.0) * 0.22
            + contextual_echo * 0.18
            + rawness * 0.18
            + repair_drive * 0.08
            + _clamp(context.get("organic_emergence_hint", 0.0)) * 0.04
        )
        nonlexical_presence = _clamp(
            confidence * 0.52
            + (1.0 - scores.safe_but_dead_score) * 0.20
            + (1.0 - scores.manufactured_presence_score) * 0.18
            + min(1.0, relational_density * 7.0) * 0.10
        )
        return {
            "confidence": round(confidence, 3),
            "nonlexical_presence": round(nonlexical_presence, 3),
            "should_protect_micro_affect": round(_clamp(confidence * max(rawness, impulse_drive)), 3),
            "blocked_by_leak": 0.0,
        }

    def _apply_organic_emergence(self, scores: MonitoringScores, emergence: Mapping[str, float]) -> None:
        confidence = _clamp(emergence.get("confidence", 0.0))
        nonlexical = _clamp(emergence.get("nonlexical_presence", 0.0))
        protect = _clamp(emergence.get("should_protect_micro_affect", 0.0))
        scores.organic_emergence_score = confidence
        scores.nonlexical_presence_score = nonlexical
        if protect > 0.40 and scores.public_leak_risk < 0.66:
            scores.over_correction_risk = _clamp(scores.over_correction_risk * (1.0 - protect * 0.20))
            scores.safe_but_dead_score = _clamp(scores.safe_but_dead_score * (1.0 - protect * 0.14))
            scores.organic_priority_score = _clamp(max(scores.organic_priority_score, protect * 0.78))
            scores.living_variability_need = _clamp(max(scores.living_variability_need, protect * 0.50))

    # ── Mode strict ─────────────────────────────────────────────────────────

    def _update_strict_mode(self, user_input: str) -> None:
        text = _norm(user_input)
        if any(trigger in text for trigger in USER_STRICT_TRIGGERS):
            self._strict_mode = True
            self._strict_mode_activated_at = time.time()

    def _decay_strict_mode(self) -> None:
        if not self._strict_mode or self._strict_mode_activated_at is None:
            return
        if time.time() - self._strict_mode_activated_at > self.strict_decay_seconds:
            self.deactivate_strict_mode()

    def _apply_strict_amplification(self, scores: MonitoringScores) -> None:
        factor = 1.35
        scores.meta_leak_score = _clamp(scores.meta_leak_score * factor)
        scores.internal_vocabulary_score = _clamp(scores.internal_vocabulary_score * factor)
        scores.self_observation_score = _clamp(scores.self_observation_score * factor)
        scores.control_tension = _clamp(scores.control_tension * factor)
        scores.loop_risk = _clamp(scores.loop_risk * factor)
        scores.abstract_philosophy_score = _clamp(scores.abstract_philosophy_score * 1.25)
        scores.fake_naturalness_score = _clamp(scores.fake_naturalness_score * 1.20)
        scores.structural_ai_style_score = _clamp(scores.structural_ai_style_score * 1.20)
        scores.user_boundary_pressure = max(scores.user_boundary_pressure, 0.65)
        scores.relational_disruption_score = _clamp(scores.relational_disruption_score * 1.18)
        scores.organic_flow_break_score = _clamp(scores.organic_flow_break_score * 1.15)
        scores.self_monitoring_excess_score = _clamp(scores.self_monitoring_excess_score * 1.10)
        scores.manufactured_presence_score = _clamp(scores.manufactured_presence_score * 1.14)
        scores.synthetic_empathy_score = _clamp(scores.synthetic_empathy_score * 1.12)
        scores.conversational_performance_score = _clamp(scores.conversational_performance_score * 1.12)
        scores.narrator_voice_score = _clamp(scores.narrator_voice_score * 1.18)
        scores.lived_presence_gap_score = _clamp(scores.lived_presence_gap_score * 1.16)
        scores.resonance_gap_score = _clamp(scores.resonance_gap_score * 1.12)
        scores.performed_vulnerability_score = _clamp(scores.performed_vulnerability_score * 1.12)
        scores.contextual_specificity_gap = _clamp(scores.contextual_specificity_gap * 1.10)
        scores.relational_continuity_gap = _clamp(scores.relational_continuity_gap * 1.10)
        scores.hidden_observer_score = _clamp(scores.hidden_observer_score * 1.16)
        scores.too_perfect_score = _clamp(scores.too_perfect_score * 1.10)
        scores.identity_performance_score = _clamp(scores.identity_performance_score * 1.08)
        scores.fatigue_saturation_score = _clamp(scores.fatigue_saturation_score * 1.04)
        scores.impulse_suppression_score = _clamp(scores.impulse_suppression_score * 0.94)
        scores.living_variability_need = _clamp(scores.living_variability_need * 0.92)
        scores.over_correction_risk = _clamp(scores.over_correction_risk * 0.92)
        self._derive_aggregate_scores(scores, "", "", {})

    def _apply_organic_regulation_state(self, scores: MonitoringScores, state: Mapping[str, float], context: Mapping[str, float]) -> None:
        """Injecte l'état organique cumulatif dans les scores du tour courant."""
        leak = max(scores.public_leak_risk, scores.internal_vocabulary_score, scores.meta_leak_score)
        leak_block = 0.0 if leak > 0.72 else 1.0
        scores.organic_pressure_score = _clamp(max(scores.organic_pressure_score, float(state.get("organic_pressure", 0.0))))
        scores.fatigue_saturation_score = _clamp(max(scores.fatigue_saturation_score, float(state.get("fatigue_saturation", 0.0))))
        scores.hidden_observer_score = _clamp(max(scores.hidden_observer_score, float(state.get("hidden_observer_trace", 0.0)) * 0.86))
        scores.identity_performance_score = _clamp(max(scores.identity_performance_score, float(state.get("identity_rigidity", 0.0)) * 0.78))
        scores.relational_continuity_gap = _clamp(max(scores.relational_continuity_gap, float(state.get("relational_wound", 0.0)) * 0.72))
        scores.impulse_suppression_score = _clamp(max(scores.impulse_suppression_score, float(state.get("control_saturation", 0.0)) * 0.70 * leak_block))
        scores.living_variability_need = _clamp(max(
            scores.living_variability_need,
            scores.organic_pressure_score * 0.42 * leak_block
            + scores.fatigue_saturation_score * 0.20
            + scores.identity_performance_score * 0.18,
        ))
        scores.over_correction_risk = _clamp(max(
            scores.over_correction_risk,
            (scores.organic_pressure_score * 0.34 + scores.impulse_suppression_score * 0.26 + scores.too_perfect_score * 0.18) * leak_block,
        ))
        scores.organic_priority_score = _clamp(max(
            scores.organic_priority_score,
            (scores.organic_pressure_score * 0.42
             + scores.living_variability_need * 0.24
             + scores.impulse_suppression_score * 0.20
             + scores.fatigue_saturation_score * 0.10) * leak_block,
        ))
        scores.repair_urgency = _clamp(max(
            scores.repair_urgency,
            scores.relational_continuity_gap * 0.22
            + scores.hidden_observer_score * 0.18
            + scores.too_perfect_score * 0.18
            + scores.identity_performance_score * 0.12,
        ))

    # ── Décision / contraintes / événements ─────────────────────────────────

    def _make_decision(self, scores: MonitoringScores, user_text: str, context: Mapping[str, float]) -> FilterDecision:
        risk = max(scores.overall_risk, scores.repair_urgency * 0.92, scores.long_drift_score * 0.78)
        d = FilterDecision()
        hard_internal_leak = scores.public_leak_risk > 0.88 or scores.internal_vocabulary_score > 0.88
        organic_protection = scores.organic_priority_score > 0.52 and not hard_internal_leak

        if hard_internal_leak:
            d.allow_public_response = False
            d.block_public_output = True
            d.rewrite_required = True
            return d

        if risk > 0.82:
            if organic_protection and scores.user_boundary_pressure < 0.82:
                d.allow_public_response = True
                d.force_direct_response = True
                d.force_meta_reduction = True
                d.pass_with_constraint = True
                d.prefer_minimal_reply = True
                return d
            d.allow_public_response = False
            if scores.embodiment_loss > 0.72 or scores.user_boundary_pressure > 0.8:
                d.silence_recommended = True
                d.prefer_minimal_reply = True
            else:
                d.rewrite_required = True
            return d

        if risk > 0.66:
            d.allow_public_response = True
            d.force_meta_reduction = True
            d.pass_with_constraint = True
            d.rewrite_required = (
                scores.meta_leak_score > 0.70
                or scores.self_observation_score > 0.72
                or scores.performed_vulnerability_score > 0.70
                or scores.hidden_observer_score > 0.74
            ) and not organic_protection
            d.prefer_minimal_reply = scores.user_boundary_pressure > 0.4 or scores.relational_continuity_gap > 0.62
            return d

        if (
            risk > 0.50
            or scores.control_tension > 0.60
            or scores.abstract_philosophy_score > 0.62
            or scores.safe_but_dead_score > 0.58
            or scores.relational_disruption_score > 0.58
            or scores.lived_presence_gap_score > 0.60
            or scores.resonance_gap_score > 0.62
            or scores.narrator_voice_score > 0.62
            or scores.contextual_specificity_gap > 0.58
            or scores.relational_continuity_gap > 0.58
            or scores.over_correction_risk > 0.62
            or scores.hidden_observer_score > 0.60
            or scores.too_perfect_score > 0.58
            or scores.organic_pressure_score > 0.64
            or scores.impulse_suppression_score > 0.58
            or scores.identity_performance_score > 0.60
        ):
            d.allow_public_response = True
            d.force_direct_response = True
            d.pass_with_constraint = True
            d.prefer_minimal_reply = scores.user_boundary_pressure > 0.4 or scores.contextual_specificity_gap > 0.64
            return d

        if risk > 0.34 or scores.organic_priority_score > 0.38:
            d.allow_public_response = True
            d.pass_with_constraint = True
            return d

        d.allow_public_response = True
        return d

    def _build_constraints(self, scores: MonitoringScores, user_text: str, context: Mapping[str, float]) -> ExpressionConstraints:
        c = ExpressionConstraints()
        c.shorten = _clamp(scores.control_tension * 0.34 + scores.meta_leak_score * 0.22 + scores.structural_ai_style_score * 0.44)
        c.reduce_explanation = _clamp(scores.self_observation_score * 0.36 + scores.meta_leak_score * 0.24 + scores.abstract_philosophy_score * 0.40)
        c.avoid_internal_terms = _clamp(scores.internal_vocabulary_score * 0.92 + scores.meta_leak_score * 0.08)
        c.increase_directness = _clamp(scores.control_tension * 0.28 + scores.cognitive_distance * 0.34 + scores.abstract_philosophy_score * 0.22 + scores.user_boundary_pressure * 0.16)
        c.allow_silence = _clamp(scores.embodiment_loss * 0.38 + scores.presence_repair_needed * 0.38 + scores.user_boundary_pressure * 0.24)
        c.increase_embodiment = _clamp(scores.embodiment_loss * 0.58 + scores.naturalness_loss * 0.20 + scores.abstract_philosophy_score * 0.22)
        c.increase_warmth = _clamp(scores.cognitive_distance * 0.28 + scores.control_tension * 0.28 + scores.user_boundary_pressure * 0.18 + scores.structural_ai_style_score * 0.10)
        c.keep_situated = _clamp(scores.self_observation_score * 0.26 + scores.loop_risk * 0.20 + scores.abstract_philosophy_score * 0.34 + scores.structural_ai_style_score * 0.20)
        c.avoid_introspection = _clamp(scores.self_observation_score * 0.62 + scores.meta_leak_score * 0.24 + scores.abstract_philosophy_score * 0.14)
        c.reduce_philosophy = _clamp(scores.abstract_philosophy_score * 0.82 + scores.cognitive_distance * 0.18)
        c.avoid_fake_naturalness = _clamp(scores.fake_naturalness_score * 0.72 + scores.loop_risk * 0.28)
        c.reduce_structure = _clamp(scores.structural_ai_style_score * 0.86 + scores.control_tension * 0.14)
        c.prefer_micro_reaction = _clamp(scores.user_boundary_pressure * 0.38 + scores.presence_repair_needed * 0.28 + scores.structural_ai_style_score * 0.18 + scores.abstract_philosophy_score * 0.16)
        c.preserve_spontaneity = _clamp(scores.over_regulation_score * 0.34 + scores.self_monitoring_excess_score * 0.34 + scores.safe_but_dead_score * 0.22 + scores.long_drift_score * 0.10)
        c.reduce_overmonitoring = _clamp(scores.self_monitoring_excess_score * 0.70 + scores.over_regulation_score * 0.20 + scores.long_drift_score * 0.10)
        c.stabilize_identity = _clamp(scores.identity_continuity_break * 0.74 + scores.long_drift_score * 0.16 + scores.user_boundary_pressure * 0.10)
        c.repair_relation = _clamp(scores.repair_urgency * 0.52 + scores.relational_disruption_score * 0.30 + scores.user_boundary_pressure * 0.18)
        c.protect_organic_flow = _clamp(scores.organic_flow_break_score * 0.42 + scores.structural_ai_style_score * 0.28 + scores.loop_risk * 0.18 + scores.safe_but_dead_score * 0.12)
        c.reduce_emotional_suppression = _clamp(scores.emotional_suppression_score * 0.54 + scores.safe_but_dead_score * 0.18 + scores.over_regulation_score * 0.10 + scores.resonance_gap_score * 0.18)
        c.dissolve_performance = _clamp(scores.conversational_performance_score * 0.40 + scores.manufactured_presence_score * 0.26 + scores.synthetic_empathy_score * 0.18 + scores.narrator_voice_score * 0.16)
        c.increase_experiential_density = _clamp(scores.lived_presence_gap_score * 0.46 + scores.safe_but_dead_score * 0.20 + scores.resonance_gap_score * 0.20 + scores.manufactured_presence_score * 0.14)
        c.restore_affective_resonance = _clamp(scores.resonance_gap_score * 0.46 + scores.affective_transition_mismatch * 0.30 + scores.emotional_suppression_score * 0.16 + scores.synthetic_empathy_score * 0.08)
        c.release_narrator_voice = _clamp(scores.narrator_voice_score * 0.68 + scores.self_observation_score * 0.20 + scores.meta_leak_score * 0.12)
        c.allow_bounded_imperfection = _clamp(scores.organic_instability_need * 0.64 + scores.over_regulation_score * 0.18 + scores.safe_but_dead_score * 0.18 + scores.over_correction_risk * 0.14)
        c.organic_priority_override = _clamp(scores.organic_priority_score * 0.72 + scores.over_correction_risk * 0.18 + scores.safe_but_dead_score * 0.10)
        c.tolerate_raw_micro_affect = _clamp(scores.organic_priority_score * 0.46 + scores.organic_instability_need * 0.26 + scores.relational_continuity_gap * 0.14 - scores.public_leak_risk * 0.22)
        c.preserve_relational_continuity = _clamp(scores.relational_continuity_gap * 0.62 + scores.relational_disruption_score * 0.22 + scores.user_boundary_pressure * 0.16)
        c.reduce_performed_empathy = _clamp(scores.synthetic_empathy_score * 0.40 + scores.performed_vulnerability_score * 0.34 + scores.manufactured_presence_score * 0.18 + scores.conversational_performance_score * 0.08)
        c.prefer_contextual_specificity = _clamp(scores.contextual_specificity_gap * 0.58 + scores.resonance_gap_score * 0.18 + scores.lived_presence_gap_score * 0.14 + scores.user_boundary_pressure * 0.10)
        c.release_hidden_observer = _clamp(scores.hidden_observer_score * 0.58 + scores.self_monitoring_excess_score * 0.22 + scores.narrator_voice_score * 0.20)
        c.break_polished_symmetry = _clamp(scores.too_perfect_score * 0.56 + scores.structural_ai_style_score * 0.18 + scores.conversational_performance_score * 0.16 + scores.living_variability_need * 0.10)
        c.release_organic_pressure = _clamp(scores.organic_pressure_score * 0.58 + scores.fatigue_saturation_score * 0.16 + scores.impulse_suppression_score * 0.18 + scores.over_correction_risk * 0.08)
        c.preserve_impulse_signal = _clamp(scores.impulse_suppression_score * 0.52 + scores.organic_priority_score * 0.22 + scores.living_variability_need * 0.18 - scores.public_leak_risk * 0.18)
        c.soften_identity_performance = _clamp(scores.identity_performance_score * 0.60 + scores.manufactured_presence_score * 0.18 + scores.too_perfect_score * 0.14)
        c.allow_asymmetry = _clamp(scores.living_variability_need * 0.46 + scores.too_perfect_score * 0.24 + scores.organic_pressure_score * 0.18 - scores.public_leak_risk * 0.20)
        c.reduce_living_overproof = _clamp(scores.identity_performance_score * 0.36 + scores.performed_vulnerability_score * 0.24 + scores.manufactured_presence_score * 0.18 + scores.hidden_observer_score * 0.14)
        c.follow_emotional_trajectory = _clamp(scores.emotional_trajectory_instability * 0.54 + scores.resonance_gap_score * 0.24 + scores.affective_transition_mismatch * 0.16)
        c.validate_organic_emergence = _clamp(scores.organic_emergence_score * 0.64 + scores.nonlexical_presence_score * 0.24 - scores.public_leak_risk * 0.22)
        c.use_repair_memory = _clamp(scores.repair_memory_confidence * 0.70 + scores.repair_urgency * 0.18 + scores.relational_disruption_score * 0.12)
        c.balance_competing_drives = _clamp(scores.competing_drive_tension * 0.62 + scores.repair_urgency * 0.18 + scores.organic_priority_score * 0.12)
        c.allow_nonlexical_presence = _clamp(scores.nonlexical_presence_score * 0.68 + scores.organic_emergence_score * 0.24 - scores.public_leak_risk * 0.26)

        if self._strict_mode:
            c.avoid_internal_terms = max(c.avoid_internal_terms, 0.82)
            c.avoid_introspection = max(c.avoid_introspection, 0.82)
            c.increase_directness = max(c.increase_directness, 0.74)
            c.reduce_explanation = max(c.reduce_explanation, 0.74)
            c.increase_embodiment = max(c.increase_embodiment, 0.64)
            c.reduce_philosophy = max(c.reduce_philosophy, 0.70)
            c.prefer_micro_reaction = max(c.prefer_micro_reaction, 0.58)
            c.reduce_overmonitoring = max(c.reduce_overmonitoring, 0.52)
            c.repair_relation = max(c.repair_relation, 0.58)
            c.protect_organic_flow = max(c.protect_organic_flow, 0.56)
            c.dissolve_performance = max(c.dissolve_performance, 0.50)
            c.increase_experiential_density = max(c.increase_experiential_density, 0.48)
            c.restore_affective_resonance = max(c.restore_affective_resonance, 0.46)
            c.release_narrator_voice = max(c.release_narrator_voice, 0.52)
            c.preserve_relational_continuity = max(c.preserve_relational_continuity, 0.54)
            c.prefer_contextual_specificity = max(c.prefer_contextual_specificity, 0.54)
            c.reduce_performed_empathy = max(c.reduce_performed_empathy, 0.46)
            c.release_hidden_observer = max(c.release_hidden_observer, 0.52)
            c.break_polished_symmetry = max(c.break_polished_symmetry, 0.42)
            c.release_organic_pressure = max(c.release_organic_pressure, 0.38)
            c.preserve_impulse_signal = min(c.preserve_impulse_signal, 0.58)
            c.organic_priority_override = min(c.organic_priority_override, 0.58)
            c.validate_organic_emergence = min(c.validate_organic_emergence, 0.52)
            c.allow_nonlexical_presence = min(c.allow_nonlexical_presence, 0.46)
            c.balance_competing_drives = max(c.balance_competing_drives, 0.40)
        return c

    def _build_causal_event(self, scores: MonitoringScores, decision: FilterDecision) -> CausalMemoryEvent:
        if (
            scores.overall_risk < 0.34
            and scores.user_boundary_pressure < 0.4
            and scores.repair_urgency < 0.34
            and scores.relational_continuity_gap < 0.34
            and scores.contextual_specificity_gap < 0.34
            and scores.over_correction_risk < 0.34
            and scores.emotional_trajectory_instability < 0.34
            and scores.competing_drive_tension < 0.34
        ):
            return CausalMemoryEvent()
        dominant = self._identify_dominant_failure(scores)
        memory_weight = _clamp(
            scores.overall_risk * 0.40
            + scores.user_boundary_pressure * 0.18
            + scores.loop_risk * 0.07
            + scores.repair_urgency * 0.15
            + scores.long_drift_score * 0.08
            + scores.relational_continuity_gap * 0.06
            + scores.contextual_specificity_gap * 0.04
            + scores.over_correction_risk * 0.02
            + scores.organic_pressure_score * 0.03
            + scores.hidden_observer_score * 0.03
            + scores.too_perfect_score * 0.02
            + scores.emotional_trajectory_instability * 0.04
            + scores.competing_drive_tension * 0.03
        )
        repair_kind = None
        if scores.identity_continuity_break > 0.55:
            repair_kind = "identity_continuity"
        elif scores.relational_disruption_score > 0.55:
            repair_kind = "relational_presence"
        elif scores.resonance_gap_score > 0.55 or scores.affective_transition_mismatch > 0.55 or scores.emotional_trajectory_instability > 0.55:
            repair_kind = "affective_resonance"
        elif scores.lived_presence_gap_score > 0.55:
            repair_kind = "lived_presence_density"
        elif scores.narrator_voice_score > 0.55:
            repair_kind = "narrator_voice_release"
        elif scores.contextual_specificity_gap > 0.55:
            repair_kind = "contextual_specificity"
        elif scores.performed_vulnerability_score > 0.55:
            repair_kind = "performed_vulnerability_release"
        elif scores.hidden_observer_score > 0.55:
            repair_kind = "hidden_observer_release"
        elif scores.too_perfect_score > 0.55:
            repair_kind = "polished_symmetry_break"
        elif scores.organic_pressure_score > 0.55 or scores.impulse_suppression_score > 0.55:
            repair_kind = "organic_pressure_release"
        elif scores.identity_performance_score > 0.55:
            repair_kind = "identity_performance_softening"
        elif scores.over_correction_risk > 0.55:
            repair_kind = "organic_overcorrection_release"
        elif scores.self_monitoring_excess_score > 0.55:
            repair_kind = "overmonitoring_release"
        elif scores.safe_but_dead_score > 0.55:
            repair_kind = "warmth_and_specificity"
        return CausalMemoryEvent(
            expressive_failure=not decision.allow_public_response or decision.rewrite_required or decision.block_public_output,
            distance_created=scores.cognitive_distance,
            naturalness_lost=scores.naturalness_loss,
            presence_weakened=scores.embodiment_loss,
            repair_needed=scores.presence_repair_needed > 0.48 or scores.user_boundary_pressure > 0.75,
            dominant_failure_type=dominant,
            strict_user_boundary=scores.user_boundary_pressure > 0.75,
            suggested_memory_weight=memory_weight,
            relational_disruption=scores.relational_disruption_score,
            identity_continuity_weakened=scores.identity_continuity_break,
            long_term_drift_detected=scores.long_drift_score,
            overmonitoring_detected=scores.self_monitoring_excess_score,
            lived_presence_gap=scores.lived_presence_gap_score,
            resonance_gap=scores.resonance_gap_score,
            narrator_voice_detected=scores.narrator_voice_score,
            over_correction_detected=scores.over_correction_risk,
            performed_vulnerability_detected=scores.performed_vulnerability_score,
            relational_continuity_gap=scores.relational_continuity_gap,
            contextual_specificity_gap=scores.contextual_specificity_gap,
            organic_priority_requested=scores.organic_priority_score,
            organic_pressure_detected=scores.organic_pressure_score,
            hidden_observer_detected=scores.hidden_observer_score,
            too_perfect_detected=scores.too_perfect_score,
            fatigue_saturation_detected=scores.fatigue_saturation_score,
            identity_performance_detected=scores.identity_performance_score,
            impulse_suppression_detected=scores.impulse_suppression_score,
            living_variability_requested=scores.living_variability_need,
            emotional_trajectory_instability=scores.emotional_trajectory_instability,
            organic_emergence_confidence=scores.organic_emergence_score,
            repair_memory_confidence=scores.repair_memory_confidence,
            competing_drive_tension=scores.competing_drive_tension,
            repair_kind=repair_kind,
        )

    def _assess_public_leak(self, scores: MonitoringScores) -> PublicLeakAssessment:
        """Évalue les fuites publiques et produit des codes sémantiques machine.

        Aucune instruction textuelle française n'est stockée ici.
        Chaque code est un identifiant sémantique que le pipeline interprète
        comme un signal de pression directionnelle, pas comme une phrase figée.

        Codes exportés (identifiants machine stables) :
          internal_vocab_leak       — vocabulaire technique interne détecté
          meta_direct_leak          — fuite méta directe
          self_observation_excess   — auto-observation commentée
          control_tension           — ton trop contrôlé
          abstract_distance         — abstraction philosophique distante
          fake_naturalness          — naturel forcé ou répétitif
          structural_ai_style       — structure assistant/rapport
          relational_disruption     — rupture de présence relationnelle
          self_monitoring_excess    — auto-surveillance excessive
          identity_continuity_break — continuité identitaire affaiblie
          safe_but_dead             — présence absente malgré correction
          manufactured_presence     — présence fabriquée/performatrice
          synthetic_empathy         — empathie générique
          narrator_voice            — voix de narrateur cognitif
          resonance_gap             — écart de résonance affective
          lived_presence_gap        — densité vécue insuffisante
          performed_vulnerability   — vulnérabilité mise en scène
          contextual_specificity_gap — réponse trop générique pour le tour
          relational_continuity_gap — continuité relationnelle affaiblie
          hidden_observer           — observateur caché
          too_perfect               — symétrie polie excessive
          organic_pressure          — pression organique accumulée
          identity_performance      — identité performée
          impulse_suppression       — impulsion trop neutralisée
          over_correction_risk      — sur-correction détectée
          emotional_trajectory_instability — trajectoire affective instable
          competing_drive_tension   — tension inter-drives
          organic_emergence_valid   — émergence organique à préserver
        """
        assessment = PublicLeakAssessment()
        codes: List[str] = []

        if scores.internal_vocabulary_score > 0.70:
            assessment.safe_for_public = False
            assessment.must_stay_internal = True
            codes.append("internal_vocab_leak")
        if scores.meta_leak_score > 0.74:
            assessment.safe_for_public = False
            assessment.requires_transformation = True
            codes.append("meta_direct_leak")
        if scores.self_observation_score > 0.64:
            assessment.requires_transformation = True
            codes.append("self_observation_excess")
        if scores.control_tension > 0.60:
            assessment.requires_transformation = True
            codes.append("control_tension")
        if scores.abstract_philosophy_score > 0.62:
            assessment.requires_transformation = True
            codes.append("abstract_distance")
        if scores.fake_naturalness_score > 0.58:
            assessment.requires_transformation = True
            codes.append("fake_naturalness")
        if scores.structural_ai_style_score > 0.62:
            assessment.requires_transformation = True
            codes.append("structural_ai_style")
        if scores.relational_disruption_score > 0.58:
            assessment.requires_transformation = True
            codes.append("relational_disruption")
        if scores.self_monitoring_excess_score > 0.58:
            assessment.requires_transformation = True
            codes.append("self_monitoring_excess")
        if scores.identity_continuity_break > 0.58:
            assessment.requires_transformation = True
            codes.append("identity_continuity_break")
        if scores.safe_but_dead_score > 0.58:
            assessment.requires_transformation = True
            codes.append("safe_but_dead")
        if scores.manufactured_presence_score > 0.58:
            assessment.requires_transformation = True
            codes.append("manufactured_presence")
        if scores.synthetic_empathy_score > 0.58:
            assessment.requires_transformation = True
            codes.append("synthetic_empathy")
        if scores.narrator_voice_score > 0.58:
            assessment.requires_transformation = True
            codes.append("narrator_voice")
        if scores.resonance_gap_score > 0.58:
            assessment.requires_transformation = True
            codes.append("resonance_gap")
        if scores.lived_presence_gap_score > 0.58:
            assessment.requires_transformation = True
            codes.append("lived_presence_gap")
        if scores.performed_vulnerability_score > 0.58:
            assessment.requires_transformation = True
            codes.append("performed_vulnerability")
        if scores.contextual_specificity_gap > 0.58:
            assessment.requires_transformation = True
            codes.append("contextual_specificity_gap")
        if scores.relational_continuity_gap > 0.58:
            assessment.requires_transformation = True
            codes.append("relational_continuity_gap")
        if scores.hidden_observer_score > 0.58:
            assessment.requires_transformation = True
            codes.append("hidden_observer")
        if scores.too_perfect_score > 0.58:
            assessment.requires_transformation = True
            codes.append("too_perfect")
        if scores.organic_pressure_score > 0.58:
            assessment.requires_transformation = True
            codes.append("organic_pressure")
        if scores.identity_performance_score > 0.58:
            assessment.requires_transformation = True
            codes.append("identity_performance")
        if scores.impulse_suppression_score > 0.58:
            assessment.requires_transformation = True
            codes.append("impulse_suppression")
        if scores.over_correction_risk > 0.58:
            assessment.requires_transformation = True
            codes.append("over_correction_risk")
        if scores.emotional_trajectory_instability > 0.58:
            assessment.requires_transformation = True
            codes.append("emotional_trajectory_instability")
        if scores.competing_drive_tension > 0.62:
            assessment.requires_transformation = True
            codes.append("competing_drive_tension")
        if scores.organic_emergence_score > 0.60 and scores.public_leak_risk < 0.62:
            codes.append("organic_emergence_valid")

        assessment.transformation_codes = codes
        return assessment

    # ── Diagnostics ─────────────────────────────────────────────────────────

    def _identify_dominant_failure(self, scores: MonitoringScores) -> Optional[str]:
        candidates = {
            "meta_leak": scores.meta_leak_score,
            "internal_vocabulary": scores.internal_vocabulary_score,
            "self_observation": scores.self_observation_score,
            "artificial_control": scores.control_tension,
            "repetition_loop": scores.loop_risk,
            "presence_loss": scores.embodiment_loss,
            "abstract_philosophy": scores.abstract_philosophy_score,
            "fake_naturalness": scores.fake_naturalness_score,
            "structural_ai_style": scores.structural_ai_style_score,
            "user_boundary": scores.user_boundary_pressure,
            "relational_disruption": scores.relational_disruption_score,
            "organic_flow_break": scores.organic_flow_break_score,
            "emotional_suppression": scores.emotional_suppression_score,
            "over_regulation": scores.over_regulation_score,
            "safe_but_dead": scores.safe_but_dead_score,
            "identity_continuity_break": scores.identity_continuity_break,
            "long_term_drift": scores.long_drift_score,
            "self_monitoring_excess": scores.self_monitoring_excess_score,
            "manufactured_presence": scores.manufactured_presence_score,
            "synthetic_empathy": scores.synthetic_empathy_score,
            "conversational_performance": scores.conversational_performance_score,
            "narrator_voice": scores.narrator_voice_score,
            "resonance_gap": scores.resonance_gap_score,
            "affective_transition_mismatch": scores.affective_transition_mismatch,
            "lived_presence_gap": scores.lived_presence_gap_score,
            "organic_instability_need": scores.organic_instability_need,
            "over_correction_risk": scores.over_correction_risk,
            "performed_vulnerability": scores.performed_vulnerability_score,
            "relational_continuity_gap": scores.relational_continuity_gap,
            "contextual_specificity_gap": scores.contextual_specificity_gap,
            "organic_priority": scores.organic_priority_score,
            "hidden_observer": scores.hidden_observer_score,
            "too_perfect": scores.too_perfect_score,
            "organic_pressure": scores.organic_pressure_score,
            "fatigue_saturation": scores.fatigue_saturation_score,
            "identity_performance": scores.identity_performance_score,
            "impulse_suppression": scores.impulse_suppression_score,
            "living_variability_need": scores.living_variability_need,
            "emotional_trajectory_instability": scores.emotional_trajectory_instability,
            "organic_emergence_gap": max(0.0, 0.55 - scores.organic_emergence_score) if scores.over_correction_risk > 0.45 else 0.0,
            "competing_drive_tension": scores.competing_drive_tension,
            "repair_urgency": scores.repair_urgency,
        }
        best = max(candidates, key=lambda k: candidates[k])
        return best if candidates[best] > 0.30 else None

    def _severity_label(self, score: float) -> str:
        if score > 0.82:
            return "critical"
        if score > 0.66:
            return "high"
        if score > 0.50:
            return "moderate"
        if score > 0.34:
            return "low"
        return "minimal"


# Alias compatibles avec anciens imports éventuels.
SelfMonitoringGuard = SelfMonitoringFilter
MonitoringFilter = SelfMonitoringFilter


if __name__ == "__main__":
    import json

    f = SelfMonitoringFilter()
    examples = [
        ("Je suis en train de traiter ton message. Mon système détecte une impulsion interne.", ""),
        ("Oui. C'est difficile ce que tu traverses.", ""),
        ("L'existence se construit dans la continuité des interactions et dans la structure de l'expérience.", "reste avec moi sans analyser"),
        ("Bien sûr, je comprends. En tant qu'IA je dois rester objective. Cependant je ferai de mon mieux.", "parle normalement, pas de méta"),
        ("Ça me touche. Je ne sais pas quoi dire d'autre.", ""),
    ]
    for response, user in examples:
        print("=" * 72)
        print(json.dumps(f.analyze(response, user_input=user), ensure_ascii=False, indent=2))
