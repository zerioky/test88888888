# core/living_expression_engine_v4_2_stable.py
"""
LIVING EXPRESSION ENGINE V4.9 TRUE CONTINUOUS LIVING MOUTH

Changements depuis V4.2 initial :

1. ✅ Fixes bugs
   - curiosity (pas curious)
   - extraction concept plus robuste
   - emotional momentum sans NaN

2. ✅ Composition plus profonde
   - relations → ordre grammatical
   - modificateurs dynamiques
   - rythme depuis tension
   - compression depuis urgence

3. ✅ Mémoire conversationnelle
   - style précédent influence nouveau
   - rythme conversationnel
   - distance conversationnelle
   - continuité du mouvement

4. ✅ Dynamique de langage
   - conflit → phrases courtes sans templates
   - proximité → fluidité
   - doute → hésitations naturelles
   - curiosité → bifurcation
   - fatigue → compression

Architecture inchangée : concepts → relations → composition.
Implémentation : beaucoup plus fiable et profonde.

V4.8 : ajout d’un flux pré-linguistique vivant, propagation de particules
sémantiques, dérive syntaxique continue, respiration cognitive déterministe,
et fusion organique entre impulsion vécue et grammaire. Toujours sans réponse
préécrite ni dictionnaire émotion→mots.
"""

from __future__ import annotations
import re
import random
import time
import inspect
from dataclasses import dataclass, field
from enum import Enum
from collections import deque, defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set

# ============================================================================
# OPTIONAL LIVING LANGUAGE GENERATOR BRIDGE
# ============================================================================

try:
    from living_language_generator import LivingLanguageGenerator
except Exception:
    LivingLanguageGenerator = None



# ==============================================================================
# ENUMS
# ==============================================================================

class ConceptType(Enum):
    IDENTITY    = "identity"
    ACTION      = "action"
    STATE       = "state"
    OBJECT      = "object"
    QUALITY     = "quality"
    RELATION    = "relation"
    ABSTRACT    = "abstract"


class RelationType(Enum):
    ANTAGONISM  = "antagonism"
    SUPPORT     = "support"
    CAUSALITY   = "causality"
    IDENTITY    = "identity"
    COMPOSITION = "composition"
    QUESTION    = "question"
    AFFILIATION = "affiliation"


class ThoughtStance(Enum):
    HONEST     = "honest"
    OPEN       = "open"
    DEFENSIVE  = "defensive"
    WARM       = "warm"
    DISTANT    = "distant"


class GrammaticalRole(Enum):
    SUBJECT    = "subject"
    VERB       = "verb"
    OBJECT     = "object"
    MODIFIER   = "modifier"
    CONNECTOR  = "connector"
    HEDGING    = "hedging"
    EMPHASIS   = "emphasis"
    PAUSE      = "pause"


# ==============================================================================
# STRUCTURES DE DONNÉES CORRIGÉES
# ==============================================================================

@dataclass
class Concept:
    """Unité conceptuelle."""
    text: str
    type: ConceptType
    span: Tuple[int, int] = (0, 0)
    valence: float = 0.0        # -1.0 à 1.0
    intensity: float = 0.5      # 0.0 à 1.0
    confidence: float = 0.8
    semantic_field: str = ""
    
    def __hash__(self):
        return hash((self.text, self.type))
    
    def __eq__(self, other):
        return isinstance(other, Concept) and self.text == other.text and self.type == other.type


@dataclass
class ConceptRelation:
    """Relation entre concepts."""
    source: Concept
    target: Concept
    relation_type: RelationType
    strength: float = 0.5
    reason: str = ""  # Pourquoi cette relation
    
    def __hash__(self):
        return hash((self.source.text, self.target.text, self.relation_type))


@dataclass
class GrammaticalUnit:
    """Unité grammaticale abstraite."""
    role: GrammaticalRole
    source_concept: Optional[Concept] = None
    intensity: float = 0.5
    constraints: Dict[str, Any] = field(default_factory=dict)
    
    def __repr__(self):
        return f"GU({self.role.value}, i={self.intensity:.1f})"


@dataclass
class ConceptReaction:
    """Réaction calculée depuis concepts."""
    concepts: List[Concept] = field(default_factory=list)
    relations: List[ConceptRelation] = field(default_factory=list)
    dominant_concept: Optional[Concept] = None
    
    # Signaux (CORRIGÉ : curiosity, pas curious)
    tension: float = 0.0
    warmth: float = 0.0
    curiosity: float = 0.0
    doubt: float = 0.0
    resistance: float = 0.0
    
    dominant_signal: str = "neutral"


@dataclass
class ConversationalContext:
    """Mémoire du mouvement conversationnel."""
    recent_utterances: deque = field(default_factory=lambda: deque(maxlen=10))
    recent_verbs: deque = field(default_factory=lambda: deque(maxlen=20))
    recent_structures: deque = field(default_factory=lambda: deque(maxlen=20))
    
    conversation_rhythm: float = 0.5   # Rythme : rapide (1.0) vs lent (0.0)
    average_length: float = 10.0       # Longueur moyenne des réponses
    proximity_level: float = 0.5       # Proximité conversationnelle
    
    turn_count: int = 0                # Nombre de tours
    last_tension: float = 0.0          # Tension du dernier message
    last_warmth: float = 0.0           # Chaleur du dernier message
    
    def update(self, utterance: str, tension: float, warmth: float) -> None:
        """Mettre à jour contexte."""
        self.recent_utterances.append(utterance)
        self.average_length = (self.average_length * 0.7) + (len(utterance.split()) * 0.3)
        self.last_tension = tension
        self.last_warmth = warmth
        self.turn_count += 1
    
    def get_rhythm_tendency(self) -> str:
        """Quelle est la tendance du rythme ?"""
        if self.turn_count < 2:
            return "establishing"
        
        if self.conversation_rhythm > 0.7:
            return "fast"
        elif self.conversation_rhythm < 0.3:
            return "slow"
        return "steady"


@dataclass
class EmotionalState:
    """État émotionnel avec inertie réelle."""
    tone: str = "neutral"
    formality: float = 0.5
    distance: float = 0.5
    affiliation: float = 0.0
    
    age: int = 0
    momentum: float = 0.12  # Inertie conservative
    
    def evolve_toward(self, target: EmotionalState) -> None:
        """Évoluer progressivement vers cible."""

        self.formality = (
            (1 - self.momentum) * self.formality
            + self.momentum * target.formality
        )

        self.distance = (
            (1 - self.momentum) * self.distance
            + self.momentum * target.distance
        )

        self.affiliation = (
            (1 - self.momentum) * self.affiliation
            + self.momentum * target.affiliation
        )

        # === NOUVEAU : évolution du tone ===
        if (
            self.age == 0
            or abs(target.affiliation - self.affiliation) > 0.25
            or target.tone != self.tone
        ):
            self.tone = target.tone

        self.age += 1


@dataclass
class LinguisticPressureVector:
    """Pression linguistique réelle."""
    sentence_length: int = 10
    hedge_rate: float = 0.0
    directness: float = 0.5
    lexical_density: float = 0.5
    pause_probability: float = 0.1
    emphasis_frequency: float = 0.0
    
    # Nouvelles : dynamique de langage
    compression_rate: float = 0.0      # Compression du langage (fatigue, urgence)
    bifurcation_probability: float = 0.0  # Question en fin (curiosité)
    fluidity: float = 0.5              # Fluidité vs hésitant
    
    def apply_tension(self, tension: float) -> None:
        """Tension modifie pression."""
        # Tension haute → phrases courtes
        self.sentence_length = max(2, int(15 * (1 - tension * 0.8)))
        # Tension haute → moins de précision
        self.lexical_density = max(0.2, 0.5 - (tension * 0.3))
        # Tension haute → directness
        self.directness = min(1.0, self.directness + tension * 0.3)
    
    def apply_doubt(self, doubt: float) -> None:
        """Doute → hésitations."""
        self.hedge_rate = max(self.hedge_rate, doubt * 0.4)
        self.pause_probability = max(self.pause_probability, doubt * 0.2)
        self.fluidity = 0.3  # Moins fluide
    
    def apply_curiosity(self, curiosity: float) -> None:
        """Curiosité → bifurcations."""
        self.bifurcation_probability = curiosity * 0.4
        self.fluidity = min(1.0, self.fluidity + curiosity * 0.3)
    
    def apply_fatigue(self, turn_count: int) -> None:
        """Fatigue → compression."""
        if turn_count > 10:
            self.compression_rate = min(1.0, (turn_count - 10) * 0.05)
            self.sentence_length = max(2, int(self.sentence_length * (1 - self.compression_rate)))

@dataclass
class LivingImpulse:
    mode: str = "react"
    intensity: float = 0.5
    tension: float = 0.0
    warmth: float = 0.0
    curiosity: float = 0.0
    doubt: float = 0.0
    directness: float = 0.5
    fluidity: float = 0.5
    compression: float = 0.0
    dominant_text: str = ""
    concepts: List[str] = field(default_factory=list)
    modifiers: List[str] = field(default_factory=list)
    relations: List[Tuple[str, str, str]] = field(default_factory=list)
    stance: str = "HONEST"
    intentions: Dict[str, float] = field(default_factory=dict)
    self_review: Dict[str, float] = field(default_factory=dict)
    surface_signature: str = ""
    continuity_signature: Dict[str, float] = field(default_factory=dict)
    trajectory_seed: List[str] = field(default_factory=list)





@dataclass
class LivingSemanticParticle:
    """Particule pré-linguistique : énergie de sens avant les mots.

    Elle transporte un token issu du message actuel, mais son rôle expressif
    vient de sa masse, son attraction, son instabilité, sa collision et sa
    continuité. Ce n'est pas une phrase et ce n'est pas un template.
    """
    token: str
    origin: str = "current"
    mass: float = 0.0
    pull: float = 0.0
    instability: float = 0.0
    activation: float = 0.0
    collision: float = 0.0
    continuity: float = 0.0
    order: int = 0
    links: List[str] = field(default_factory=list)


@dataclass
class OrganicGrammarTrace:
    """Trace interne de grammaire vivante sans phrase préécrite."""
    nucleus: List[str] = field(default_factory=list)
    approach: List[str] = field(default_factory=list)
    tension: List[str] = field(default_factory=list)
    expansion: List[str] = field(default_factory=list)
    restraint: List[str] = field(default_factory=list)
    pause: float = 0.0
    compression: float = 0.0
    coherence: float = 0.0
    vitality: float = 0.0

# ==============================================================================
# MODULE 1 : CONCEPT EXTRACTOR (AMÉLIORÉ)
# ==============================================================================

class ConceptExtractorStable:
    """
    Extraction conceptuelle vivante.

    Correction finale :
    - plus de listes de mots par émotion/intention ;
    - plus de dictionnaire de valence lexical ;
    - les concepts viennent du message et de leur énergie locale ;
    - la ponctuation, la répétition, la position et la forme donnent les signaux.
    """

    TOKEN_RE = re.compile(r"[\wÀ-ÿ']+|[?!…]+", re.UNICODE)

    def extract(self, message: str) -> ConceptReaction:
        raw_tokens = self.TOKEN_RE.findall(str(message or "").lower())
        word_tokens = [t for t in raw_tokens if re.search(r"[\wÀ-ÿ']", t, re.UNICODE)]

        concepts: List[Concept] = []
        seen: Set[str] = set()
        total = max(1, len(word_tokens))

        for index, token in enumerate(word_tokens):
            token = token.strip("'’ ")
            if not token:
                continue

            # V4.8 : une répétition peut être un vrai mouvement de parole
            # (ex. “tu mens tu as…”). On ne déduplique plus ici ; les filtres
            # de surface bloquent seulement les répétitions mortes immédiates.
            local_context = word_tokens[max(0, index - 2):index + 3]
            ctype = self._infer_type(token, index, total, local_context)
            intensity = self._token_intensity(token, word_tokens, raw_tokens, index, total)
            valence = self._contextual_valence(token, raw_tokens, index)

            concepts.append(Concept(
                text=token,
                type=ctype,
                span=(index, index + 1),
                valence=valence,
                intensity=intensity,
                confidence=0.55 + min(0.35, intensity * 0.35),
                semantic_field=ctype.value,
            ))

        relations = self._extract_relations(concepts, raw_tokens)
        dominant = max(concepts, key=lambda c: c.intensity * (0.65 + abs(c.valence))) if concepts else None

        return ConceptReaction(
            concepts=concepts,
            relations=relations,
            dominant_concept=dominant,
            **self._compute_signals(concepts, relations, raw_tokens),
        )

    def _infer_type(
        self,
        token: str,
        index: int,
        total: int,
        local_context: List[str],
    ) -> ConceptType:
        """
        Typage relationnel dynamique.

        Correction V4.3 : plus de suffixes et plus de morphologie fixe.
        Le type naît de la place du token, de la densité locale, de la
        répétition et de la pression relationnelle autour de lui.
        """
        context = [str(t or "").strip() for t in local_context if str(t or "").strip()]
        relational_weight = len(set(context))
        local_energy = sum(len(t) for t in context) / max(1, len(context))
        center_pressure = 1.0 - abs((index / max(1, total - 1)) - 0.5)
        repetition_pressure = max(0.0, len(context) - len(set(context))) / max(1, len(context))

        if index <= 1 and center_pressure < 0.72:
            return ConceptType.IDENTITY

        if repetition_pressure > 0.18 or relational_weight >= 4:
            return ConceptType.RELATION

        if local_energy > 7.2 and center_pressure >= 0.55:
            return ConceptType.ABSTRACT

        if local_energy > 5.8:
            return ConceptType.QUALITY

        return ConceptType.OBJECT

    def _token_intensity(self, token: str, words: List[str], raw: List[str], index: int, total: int) -> float:
        count = words.count(token)
        position_pressure = 1.0 - (index / max(1, total)) * 0.18
        length_pressure = min(0.22, len(token) * 0.018)
        repetition_pressure = min(0.28, max(0, count - 1) * 0.14)
        punctuation_pressure = 0.18 if any(p in raw for p in ("?", "!", "??", "?!")) else 0.0
        return max(0.15, min(1.0, 0.38 + length_pressure + repetition_pressure + punctuation_pressure) * position_pressure)

    def _contextual_valence(self, token: str, raw: List[str], index: int) -> float:
        # Valence non lexicale : contraction/rupture/insistance locale.
        if "!" in raw:
            return -0.25
        if "?" in raw:
            return 0.12
        if raw.count(token) > 1:
            return -0.10
        return 0.0

    def _extract_relations(self, concepts: List[Concept], raw: List[str]) -> List[ConceptRelation]:
        relations: List[ConceptRelation] = []
        if len(concepts) < 2:
            return relations

        for i in range(len(concepts) - 1):
            source = concepts[i]
            target = concepts[i + 1]
            distance = max(1, target.span[0] - source.span[1] + 1)
            strength = max(0.15, 1.0 / distance) * ((source.intensity + target.intensity) * 0.5)

            if "?" in raw:
                rtype = RelationType.QUESTION
            elif abs(source.valence - target.valence) > 0.35:
                rtype = RelationType.ANTAGONISM
            elif source.type == ConceptType.IDENTITY:
                rtype = RelationType.IDENTITY
            else:
                rtype = RelationType.COMPOSITION

            relations.append(ConceptRelation(
                source=source,
                target=target,
                relation_type=rtype,
                strength=min(1.0, strength),
                reason="dynamic adjacency",
            ))

        return relations

    def _compute_signals(self, concepts, relations, raw):
        question_pressure = 1.0 if any("?" in t for t in raw) else 0.0
        rupture_pressure = 1.0 if any("!" in t for t in raw) else 0.0
        repetition_pressure = 0.0

        words = [t for t in raw if re.search(r"[\wÀ-ÿ']", t, re.UNICODE)]
        if words:
            repeated = len(words) - len(set(words))
            repetition_pressure = min(1.0, repeated / max(1, len(words)))

        avg_intensity = sum(c.intensity for c in concepts) / max(1, len(concepts))

        tension = min(1.0, rupture_pressure * 0.55 + repetition_pressure * 0.35 + max(0.0, avg_intensity - 0.62) * 0.55)
        curiosity = min(1.0, question_pressure * 0.75 + len(relations) * 0.025)
        warmth = max(0.0, min(1.0, (1.0 - tension) * 0.18 + avg_intensity * 0.12))
        doubt = min(1.0, question_pressure * 0.25 + tension * 0.18)

        if tension > 0.55:
            dominant_signal = "antagonism"
        elif curiosity > 0.55:
            dominant_signal = "inquiry"
        elif warmth > 0.35:
            dominant_signal = "affection"
        else:
            dominant_signal = "neutral"

        return {
            "tension": tension,
            "warmth": warmth,
            "curiosity": curiosity,
            "doubt": doubt,
            "resistance": tension * 0.35,
            "dominant_signal": dominant_signal,
        }


# ==============================================================================
# MODULE 2 : EMOTIONAL MOMENTUM (AMÉLIORÉ)
# ==============================================================================

class EmotionalMomentumStable:
    """État émotionnel avec inertie sans bugues."""
    
    def __init__(self):
        self.current_state = EmotionalState()
        self.history = deque(maxlen=10)
    
    def evolve(self, reaction: ConceptReaction) -> EmotionalState:
        """Évoluer vers état cible."""
        target_state = self._compute_target_state(reaction)
        self.current_state.evolve_toward(target_state)
        self.history.append(self.current_state)
        return self.current_state
    
    def _compute_target_state(self, reaction: ConceptReaction) -> EmotionalState:
        """Calculer état cible depuis réaction."""
        state = EmotionalState()
        
        # Tone depuis signal
        tone_map = {
            "antagonism": "challenging",
            "affection": "warm",
            "inquiry": "exploratory",
            "neutral": "neutral",
        }
        state.tone = tone_map.get(reaction.dominant_signal, "neutral")
        
        # Distance (inverse de warmth)
        state.distance = max(0.0, 1.0 - reaction.warmth)
        
        # Formality depuis tension
        state.formality = 0.5 + (reaction.tension * 0.3)
        
        # Affiliation depuis bilan
        state.affiliation = reaction.warmth - reaction.tension
        
        return state


# ==============================================================================
# MODULE 3 : CONVERSATIONAL CONTEXT
# ==============================================================================

class ConversationalMemory:
    """Mémoire du mouvement conversationnel."""
    
    def __init__(self):
        self.context = ConversationalContext()
    
    def update(self, utterance: str, tension: float, warmth: float) -> None:
        """Mettre à jour mémoire."""
        self.context.update(utterance, tension, warmth)
        
        # Ajuster rhythme
        if self.context.turn_count > 1:
            recent_lengths = [len(u.split()) for u in list(self.context.recent_utterances)[-5:]]
            avg_recent = sum(recent_lengths) / len(recent_lengths) if recent_lengths else 10
            
            # Rhythme : accélération ou décélération
            self.context.conversation_rhythm = min(1.0, max(0.0, avg_recent / 20.0))
    
    def get_style_continuity(self) -> Dict[str, float]:
        """Continuer le style conversationnel."""
        if self.context.turn_count < 2:
            return {}
        
        return {
            "rhythm": self.context.conversation_rhythm,
            "average_length": self.context.average_length,
            "proximity": self.context.proximity_level,
        }


# ==============================================================================
# MODULE 4 : LINGUISTIC PRESSURE (APPROFONDI)
# ==============================================================================

class LinguisticPressureStable:
    """Pression linguistique avec dynamique vraie."""
    
    def compute(
        self,
        reaction: ConceptReaction,
        emotional_state: EmotionalState,
        thought_stance: ThoughtStance,
        conversational_memory: ConversationalMemory,
    ) -> LinguisticPressureVector:
        """Calculer pression linguistique."""
        pressure = LinguisticPressureVector()
        
        # Base : tension
        pressure.apply_tension(reaction.tension)
        
        # Doute
        pressure.apply_doubt(reaction.doubt)
        
        # Curiosité
        pressure.apply_curiosity(reaction.curiosity)
        
        # Stance modifie directness
        if thought_stance == ThoughtStance.HONEST:
            pressure.directness = min(1.0, pressure.directness + 0.25)
        elif thought_stance == ThoughtStance.DEFENSIVE:
            pressure.directness = max(0.0, pressure.directness - 0.3)
        
        # Continuit conversationnelle
        rhythm = conversational_memory.context.conversation_rhythm
        pressure.sentence_length = int(pressure.sentence_length * (0.8 + rhythm * 0.4))
        
        # Fatigue : après plusieurs tours
        pressure.apply_fatigue(conversational_memory.context.turn_count)
        
        return pressure


# ==============================================================================
# MODULE 5 : CONCEPTUAL UTTERANCE COMPOSER (APPROFONDI)
# ==============================================================================

class ConceptualUtteranceComposerStable:
    """Composition progressive profonde."""
    
    def __init__(self):
        # LivingLanguageGenerator bridge
        self.external_living_language_generator = None

        if LivingLanguageGenerator is not None:
            try:
                self.external_living_language_generator = LivingLanguageGenerator()
            except Exception:
                self.external_living_language_generator = None

        self.recent_verbs = deque(maxlen=15)
        self.recent_subjects = deque(maxlen=15)


        self.activation_memory = defaultdict(float)
        self.relation_memory = defaultdict(float)
        self.internal_concept_field = defaultdict(float)
        self.cognitive_gravity = defaultdict(float)
        self.coherence_field = defaultdict(float)
        self.unresolved_tensions = defaultdict(float)

        # V4.4 — mémoire de surface non lexicale : elle ne stocke pas des phrases
        # à réutiliser, seulement des empreintes de forme pour éviter les templates cachés.
        self.surface_fingerprint_memory = deque(maxlen=32)
        self.self_review_history = deque(maxlen=24)
        self.silence_tension_memory = 0.0

        # V4.5 — organe expressif : mémoire de souffle, continuité organique,
        # et auto-mesure de vitalité sans stocker de réponses.
        self.organic_breath_memory = deque(maxlen=18)
        self.organic_surface_memory = deque(maxlen=18)
        self.vitality_history = deque(maxlen=24)
        self.breath_phase = 0.0

        # V4.6 — grammaire organique interne : rôles de souffle, jamais réponses stockées.
        self.grammar_pulse_memory = deque(maxlen=32)
        self.grammar_role_memory = defaultdict(float)
        self.living_quality_history = deque(maxlen=32)
        self.last_full_living_trace = {}

        # V4.7 — continuité profonde : mémoire de mouvement, pas de contenu à répéter.
        # Elle conserve des vecteurs de forme et de pression pour que la bouche
        # continue un dialogue au lieu de repartir à zéro.
        self.deep_continuity_memory = deque(maxlen=24)
        self.syntax_trajectory_memory = deque(maxlen=24)
        self.relation_flow_memory = defaultdict(float)
        self.fragment_repair_memory = defaultdict(float)

        # V4.8 — flux pré-linguistique vivant. Cette mémoire conserve seulement
        # des vecteurs de mouvement, pas des phrases ni des mots à ressortir.
        self.prelinguistic_flow_memory = deque(maxlen=32)
        self.semantic_particle_memory = defaultdict(float)
        self.syntax_mutation_memory = deque(maxlen=32)
        self.drift_phase = 0.0
        self.last_prelanguage_trace = {}

        # V4.8.1 — garde-fous runtime : limites de matière vivante,
        # pas de fallback préécrit. Si une étape devient trop lourde,
        # la bouche compacte le matériau actuel au lieu de bloquer.
        self.max_current_concepts = 18
        self.max_current_relations = 16
        self.max_relation_units = 8
        self.expression_time_budget = 0.18
        self.last_runtime_guard_trace = {}

        # V4.9 — temporalité expressive interne de la bouche seule.
        # Ce n'est ni mémoire globale, ni attention, ni initiative : seulement
        # la rémanence de l'organe de parole entre deux réalisations.
        self.expressive_time_phase = 0.0
        self.expressive_inertia = {
            "tension": 0.0,
            "warmth": 0.0,
            "curiosity": 0.0,
            "doubt": 0.0,
            "flow": 0.0,
        }
        self.dominance_residue = defaultdict(float)
        self.micro_rupture_residue = 0.0
        self.last_living_autonomy_trace = {}
    
    def compose(
        self,
        reaction: ConceptReaction,
        emotional_state: EmotionalState,
        pressure: LinguisticPressureVector,
        thought_stance: ThoughtStance,
        conversational_memory: ConversationalMemory,
    ) -> str:
        """Composer utterance progressivement."""
        
        # 1. Décider sujet grammatical
        subject_unit = self._compose_subject(reaction, pressure)
        
        # 2. Choisir verbe depuis relation conceptuelle
        verb_unit = self._compose_verb(reaction, thought_stance, pressure)
        
        # 3. Construire complément depuis concepts
        complement_unit = self._compose_complement(reaction, pressure)
        
        # 4. Ajouter modificateurs dynamiques
        modifiers = self._compose_modifiers(reaction, emotional_state, pressure)
        
        # 5. Assembler unités en texte
        utterance = self._express_living_state(
            subject_unit=subject_unit,
            intent_unit=verb_unit,
            complement_unit=complement_unit,
            modifiers=modifiers,
            reaction=reaction,
            emotional_state=emotional_state,
            pressure=pressure,
            conversational_memory=conversational_memory,
        )
        
        # 6. Appliquer pression linguistique
        utterance = self._apply_pressure(utterance, pressure)
        
        # 7. Adapter à continuit conversationnelle
        utterance = self._adapt_to_continuation(
            utterance,
            conversational_memory,
            pressure,
        )

        # V4.9.2 : la pression et la continuité peuvent réintroduire des pauses
        # ou collisions après la réalisation vivante. On stabilise donc une
        # dernière fois la surface finale, sans changer le fond cognitif.
        utterance = self._final_living_language_stabilizer(
            utterance,
            getattr(self, "_last_living_impulse", LivingImpulse()),
            getattr(self, "_last_living_field", {}),
        )
        utterance = self._organic_text_finish(utterance, getattr(self, "_last_living_impulse", LivingImpulse()))
        
        return utterance
    
    def _compose_subject(self, reaction: ConceptReaction, pressure: LinguisticPressureVector) -> GrammaticalUnit:
        """Sujet grammatical."""
        if pressure.directness > 0.7 and reaction.dominant_signal == "antagonism":
            # Accusation → sujet explicite
            tu = next((c for c in reaction.concepts if c.text == "tu"), None)
            if tu:
                return GrammaticalUnit(
                    role=GrammaticalRole.SUBJECT,
                    source_concept=tu,
                    intensity=pressure.directness,
                )
        
        # Implicite
        return GrammaticalUnit(
            role=GrammaticalRole.SUBJECT,
            source_concept=None,
            intensity=0.0,
        )
    
    def _compose_verb(
        self,
        reaction: ConceptReaction,
        thought_stance: ThoughtStance,
        pressure: LinguisticPressureVector
    ) -> GrammaticalUnit:

        # V4.3 : plus de mode fixe react/understand/feel/explore/answer.
        # L'intention reste un vecteur de forces qui sera résolu plus tard
        # par le champ émergent, pas par une catégorie préécrite.
        intent = {
            "vector": {
                "approach": reaction.warmth,
                "pressure": reaction.tension,
                "expansion": reaction.curiosity,
                "stability": max(0.0, 1.0 - reaction.doubt),
                "exposure": pressure.directness,
            },
            "tension": reaction.tension,
            "emotion": reaction.warmth,
            "novelty": reaction.curiosity,
            "directness": pressure.directness,
            "stance": thought_stance.name,
        }

        return GrammaticalUnit(
            role=GrammaticalRole.VERB,
            source_concept=None,
            intensity=pressure.directness,
            constraints={
                "intent": intent
            },
        )
    
    def _compose_complement(self, reaction: ConceptReaction, pressure: LinguisticPressureVector) -> GrammaticalUnit:
        """Complément depuis concepts dominants."""
        key_concepts = [c for c in reaction.concepts if c.intensity > 0.5]
        
        if not key_concepts:
            return GrammaticalUnit(role=GrammaticalRole.OBJECT)
        
        # Concept dominant
        concept = max(key_concepts, key=lambda c: c.intensity * abs(c.valence))
        
        return GrammaticalUnit(
            role=GrammaticalRole.OBJECT,
            source_concept=concept,
            intensity=concept.intensity,
            constraints={
                "hedge": pressure.hedge_rate > 0.2,
                "emphasize": pressure.emphasis_frequency > 0.2,
            }
        )
    
    def _compose_modifiers(
        self,
        reaction: ConceptReaction,
        emotional_state: EmotionalState,
        pressure: LinguisticPressureVector
    ) -> List[GrammaticalUnit]:
        modifiers = []

        if reaction.tension > 0.7:
            modifiers.append(GrammaticalUnit(
                role=GrammaticalRole.MODIFIER,
                constraints={"type": "intensity"},
                intensity=reaction.tension,
            ))

        if reaction.doubt > 0.5:
            modifiers.append(GrammaticalUnit(
                role=GrammaticalRole.HEDGING,
                constraints={"type": "hesitation"},
                intensity=reaction.doubt,
            ))

        return modifiers


    def _emergent_intention_field(
        self,
        reaction,
        emotional_state,
        pressure,
        conversational_memory=None,
    ) -> Dict[str, float]:
        """
        Intention émergente avant la phrase.

        Ce champ ne choisit pas une réponse et ne contient aucun mot à dire.
        Il mesure seulement les nécessités internes qui poussent la bouche :
        contact, résolution, exploration, protection, continuité.
        """
        turn_count = 0
        if conversational_memory is not None:
            turn_count = getattr(getattr(conversational_memory, "context", None), "turn_count", 0)

        continuity = min(1.0, max(0.0, turn_count / 12.0))
        need_for_contact = max(0.0, emotional_state.affiliation + reaction.warmth * 0.6)
        need_for_resolution = max(0.0, reaction.tension + reaction.doubt * 0.5)
        need_for_exploration = max(0.0, reaction.curiosity + pressure.fluidity * 0.3)
        need_for_protection = max(0.0, reaction.tension - emotional_state.affiliation)

        total = max(0.001, (
            need_for_contact
            + need_for_resolution
            + need_for_exploration
            + need_for_protection
            + continuity * 0.35
        ))

        need_for_silence = max(0.0, reaction.doubt * 0.45 + reaction.tension * 0.20 - pressure.directness * 0.22)
        need_for_repair = max(0.0, reaction.doubt * 0.35 + need_for_resolution * 0.20)

        return {
            "need_for_contact": min(1.0, need_for_contact / total),
            "need_for_resolution": min(1.0, need_for_resolution / total),
            "need_for_exploration": min(1.0, need_for_exploration / total),
            "need_for_protection": min(1.0, need_for_protection / total),
            "need_for_silence": min(1.0, need_for_silence),
            "need_for_repair": min(1.0, need_for_repair),
            "continuity": continuity,
            "flow_need": min(1.0, pressure.fluidity * 0.45 + continuity * 0.30 + reaction.warmth * 0.25),
            "sentence_need": min(1.0, pressure.directness * 0.35 + reaction.curiosity * 0.25 + max(0.0, 1.0 - reaction.tension) * 0.20 + continuity * 0.20),
        }


    def _conversation_continuity_signature(self, conversational_memory=None) -> Dict[str, float]:
        """Signature de continuité sans stocker de phrase à réutiliser."""
        if conversational_memory is None:
            return {"depth": 0.0, "rhythm": 0.5, "length_gravity": 0.5, "proximity": 0.5}
        ctx = getattr(conversational_memory, "context", None)
        if ctx is None:
            return {"depth": 0.0, "rhythm": 0.5, "length_gravity": 0.5, "proximity": 0.5}
        utterances = list(getattr(ctx, "recent_utterances", []) or [])
        lengths = [len(str(u).split()) for u in utterances[-6:] if str(u).strip()]
        avg_len = sum(lengths) / max(1, len(lengths))
        variation = 0.0
        if len(lengths) >= 2:
            variation = sum(abs(lengths[i] - lengths[i - 1]) for i in range(1, len(lengths))) / max(1, len(lengths) - 1)
        return {
            "depth": min(1.0, getattr(ctx, "turn_count", 0) / 14.0),
            "rhythm": max(0.0, min(1.0, getattr(ctx, "conversation_rhythm", 0.5))),
            "length_gravity": max(0.0, min(1.0, avg_len / 18.0)),
            "variation": max(0.0, min(1.0, variation / 10.0)),
            "proximity": max(0.0, min(1.0, getattr(ctx, "proximity_level", 0.5))),
        }

    def _trajectory_seed_from_current_concepts(self, reaction, conversational_memory=None) -> List[str]:
        """Point de départ du flux : concepts actuels d'abord, mémoire seulement comme pression."""
        seed = []
        for concept in getattr(reaction, "concepts", []) or []:
            tok = self._normalize_surface_token(getattr(concept, "text", ""))
            if tok and (not seed or tok != seed[-1]):
                seed.append(tok)
        return seed[:10]

    def _build_living_impulse(
        self,
        subject_unit,
        intent_unit,
        complement_unit,
        modifiers,
        reaction,
        emotional_state,
        pressure,
        conversational_memory=None,
    ) -> LivingImpulse:
        """
        Construit une impulsion vivante depuis la dynamique interne.
        """

        intent = intent_unit.constraints.get("intent", {})

        dominant_text = ""

        if complement_unit and complement_unit.source_concept:
            dominant_text = complement_unit.source_concept.text

        elif reaction.dominant_concept:
            dominant_text = reaction.dominant_concept.text

        concept_texts = []

        for concept in reaction.concepts:
            if concept.text and (not concept_texts or concept.text != concept_texts[-1]):
                concept_texts.append(concept.text)
            if len(concept_texts) >= self.max_current_concepts:
                break

        modifier_texts = []

        relation_data = []

        for rel in reaction.relations:
            relation_data.append(
                (
                    rel.source.text,
                    rel.target.text,
                    rel.relation_type.value,
                )
            )
            if len(relation_data) >= self.max_current_relations:
                break

        intensity = max(
            reaction.tension,
            reaction.warmth,
            reaction.curiosity,
            reaction.doubt,
            pressure.directness,
            0.35,
        )

        intention_field = self._emergent_intention_field(
            reaction,
            emotional_state,
            pressure,
            conversational_memory,
        )

        return LivingImpulse(
            mode="emergent",
            intensity=intensity,
            tension=reaction.tension,
            warmth=reaction.warmth,
            curiosity=reaction.curiosity,
            doubt=reaction.doubt,
            directness=pressure.directness,
            fluidity=pressure.fluidity,
            compression=pressure.compression_rate,
            dominant_text=dominant_text,
            concepts=concept_texts,
            modifiers=modifier_texts,
            relations=relation_data,
            stance=intent.get("stance", "HONEST"),
            intentions=intention_field,
            continuity_signature=self._conversation_continuity_signature(conversational_memory),
            trajectory_seed=self._trajectory_seed_from_current_concepts(reaction, conversational_memory),
        )



    def _advance_expression_temporality(self, field: Dict[str, float], impulse: LivingImpulse) -> Dict[str, float]:
        """Temporalité propre à la bouche : rémanence expressive, pas mémoire globale Azip."""
        field = dict(field or {})
        self.expressive_time_phase = (self.expressive_time_phase + 0.17 + impulse.intensity * 0.07) % 1.0
        targets = {
            "tension": impulse.tension,
            "warmth": impulse.warmth,
            "curiosity": impulse.curiosity,
            "doubt": impulse.doubt,
            "flow": field.get("flow_need", 0.0),
        }
        for key, target in targets.items():
            previous = self.expressive_inertia.get(key, 0.0)
            self.expressive_inertia[key] = previous * 0.82 + max(0.0, min(1.0, target)) * 0.18
        residual_tension = self.expressive_inertia["tension"]
        residual_flow = self.expressive_inertia["flow"]
        residual_doubt = self.expressive_inertia["doubt"]
        living_wave = (self.expressive_time_phase - 0.5) * 0.12
        field["rupture"] = max(0.0, min(1.0, field.get("rupture", 0.0) * 0.86 + residual_tension * 0.14))
        field["flow_need"] = max(0.0, min(1.0, field.get("flow_need", 0.0) * 0.84 + residual_flow * 0.16 + living_wave))
        field["silence"] = max(0.0, min(1.0, field.get("silence", 0.0) * 0.88 + residual_doubt * 0.12))
        field["living_temporality"] = max(0.0, min(1.0, sum(self.expressive_inertia.values()) / 5.0))
        field["temporal_wave"] = living_wave
        return field

    def _living_competition_order(self, nodes, field, impulse, limit=None):
        """Ordre par dominance fluctuante : pas de max brutal ni de hasard de surface."""
        ordered = []
        phase = self.expressive_time_phase
        for index, node in enumerate(list(nodes or [])):
            src = self._normalize_surface_token(node.get("source", ""))
            tgt = self._normalize_surface_token(node.get("target", ""))
            key = f"{src}>{tgt}"
            base = (
                node.get("activation", 0.0) * 0.34
                + node.get("weight", 0.0) * 0.22
                + node.get("coherence", 0.0) * 0.18
                + node.get("tension", 0.0) * 0.14
                + (1.0 / (1.0 + node.get("order", index))) * 0.12
            )
            residue = self.dominance_residue[key] * 0.13
            wave = ((index * 0.173 + phase) % 1.0 - 0.5) * 0.055
            score = base + residue + wave + field.get("living_temporality", 0.0) * 0.035
            self.dominance_residue[key] = self.dominance_residue[key] * 0.90 + max(0.0, base) * 0.10
            ordered.append((score, node))
        for key in list(self.dominance_residue.keys()):
            self.dominance_residue[key] *= 0.988
            if self.dominance_residue[key] < 0.01:
                del self.dominance_residue[key]
        ordered.sort(key=lambda pair: pair[0], reverse=True)
        nodes = [node for _, node in ordered]
        return nodes[:limit] if limit is not None else nodes

    def _soften_surface_control(self, text, grammar, units, field, impulse) -> str:
        """Dernière modulation douce : elle mesure et infléchit, mais ne remplace pas le flux vivant."""
        words = [w for w in str(text or "").split() if w]
        lexical = [self._normalize_surface_token(w) for w in words if w != "…"]
        lexical = [w for w in lexical if w]
        fingerprint = self._surface_fingerprint(words)
        repeated = sum(1 for fp in self.surface_fingerprint_memory if fp == fingerprint)
        unique_ratio = len(set(lexical)) / max(1, len(lexical))
        flow_quality = (
            min(1.0, len(lexical) / 4.0) * 0.18
            + unique_ratio * 0.20
            + getattr(grammar, "vitality", 0.0) * 0.22
            + getattr(grammar, "coherence", 0.0) * 0.16
            + max(0.0, 1.0 - repeated * 0.18) * 0.12
            + field.get("living_temporality", 0.0) * 0.12
        )
        self.last_full_living_trace["soft_final_quality"] = round(flow_quality, 3)
        if lexical:
            if repeated >= 2 and len(lexical) > 3:
                pivot = 1 + int((self.expressive_time_phase * max(1, len(lexical) - 2)))
                lexical = lexical[:1] + lexical[pivot:pivot + 2] + lexical[1:pivot] + lexical[pivot + 2:]
            if flow_quality < 0.34 and getattr(impulse, "dominant_text", ""):
                dom = self._normalize_surface_token(impulse.dominant_text)
                if dom and dom not in lexical:
                    lexical.insert(0, dom)
            if field.get("rupture", 0.0) < 0.70:
                lexical = self._restore_living_concept_order(lexical, impulse)
            return " ".join(self._stabilize_linguistic_flow(lexical, impulse))
        material = []
        for source in (getattr(grammar, "nucleus", []), getattr(grammar, "approach", []), getattr(grammar, "tension", []), getattr(grammar, "expansion", []), getattr(impulse, "concepts", [])):
            for token in source:
                tok = self._normalize_surface_token(token)
                if tok and tok not in material:
                    material.append(tok)
                if len(material) >= 4:
                    break
            if len(material) >= 4:
                break
        return " ".join(self._stabilize_linguistic_flow(material, impulse)) if material else "…"

    def _inhabit_living_surface(self, text, impulse, field, units, particles, grammar) -> str:
        """
        V4.9.1 — incarnation finale de la bouche.

        But : ne plus laisser une surface qui recopie simplement l'utilisateur.
        Cette étape ne fabrique pas de réponse complète et ne vole pas le rôle
        de l'attention/mémoire/initiative. Elle fait uniquement le travail de
        bouche : changer le point de vue, respirer, éviter le miroir brut, et
        produire une surface prononçable depuis la matière déjà active.
        """
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        seed = [self._normalize_surface_token(w) for w in getattr(impulse, "trajectory_seed", []) or []]
        seed = [w for w in seed if w]
        if not seed:
            return text

        lexical = [w for w in words if w != "…"]
        seed_set = set(seed)
        overlap = len(set(lexical) & seed_set) / max(1, len(set(lexical))) if lexical else 0.0
        same_start = lexical[:max(2, min(len(seed), len(lexical)))] == seed[:max(2, min(len(seed), len(lexical)))]
        mirror_pressure = max(0.0, overlap * 0.65 + (0.35 if same_start else 0.0))

        explicit_address = any(w in {"tu", "toi"} for w in seed)
        address_index = next((i for i, w in enumerate(seed) if w in {"tu", "toi"}), 999)
        direct_address_statement = explicit_address and address_index <= 1 and impulse.curiosity < 0.42

        # Si la surface ne miroir pas trop, on corrige seulement les collisions,
        # sauf quand l'adresse directe risque de devenir une récitation de l'utilisateur.
        if mirror_pressure < 0.58 and not direct_address_statement and len(lexical) >= 3:
            return " ".join(self._repair_operator_collisions(words, impulse))

        # Matière actuelle, pas phrase prête : dominant, concepts, particules, relations.
        material = []
        def push(tok):
            tok = self._normalize_surface_token(tok)
            if tok and tok not in material:
                material.append(tok)

        for tok in [getattr(impulse, "dominant_text", "")] + seed:
            push(tok)
        for particle in sorted(list(particles or []), key=lambda p: getattr(p, "activation", 0.0), reverse=True):
            push(getattr(particle, "token", ""))
        for node in list(units or [])[:8]:
            push(node.get("source", "")); push(node.get("target", ""))

        material = self._restore_living_concept_order(material, impulse)
        material = self._stabilize_linguistic_flow(material, impulse)

        # Transposition de perspective minimale : opérateurs grammaticaux, pas contenu.
        addressed = any(w in {"tu", "toi"} for w in seed)

        rupture = field.get("rupture", 0.0) + impulse.tension + mirror_pressure
        if direct_address_statement and rupture > 0.62:
            # Adresse directe tendue : la bouche refuse le miroir brut et garde
            # seulement le prédicat actif + matière courante. Ce n'est pas une
            # phrase stockée ; c'est une opération de point de vue.
            predicate = ""
            after_address = False
            for tok in seed:
                if tok in {"tu", "toi"}:
                    after_address = True
                    continue
                if after_address and tok not in {"as", "es", "est", "du", "de", "la", "le", "les", "un", "une", "des"}:
                    predicate = tok
                    break
            if not predicate:
                predicate = material[0] if material else ""
            content = []
            for tok in material:
                if tok in {"tu", "toi", "te", "t", "je", "me", "moi", "as", "es", "est", "du", "de", "la", "le", "les", "un", "une", "des", predicate}:
                    continue
                if tok not in content:
                    content.append(tok)
            transposed = ["je", "ne", predicate, "pas"] + content[:2]
        else:
            transposed = []
            first_inserted = False
            previous_was_address = False
            for tok in material:
                if tok == "…":
                    transposed.append(tok); previous_was_address = False; continue
                if tok in {"tu", "toi"}:
                    if not first_inserted:
                        transposed.append("je")
                        first_inserted = True
                    previous_was_address = True
                    continue
                if tok in {"je", "me", "moi"} and addressed:
                    transposed.append("toi")
                    previous_was_address = False
                    continue
                if previous_was_address and tok == "es":
                    transposed.append("suis"); previous_was_address = False; continue
                if previous_was_address and tok == "as":
                    transposed.append("ai"); previous_was_address = False; continue
                transposed.append(tok)
                previous_was_address = False

            if addressed and not first_inserted:
                transposed.insert(0, "je")

        # Limite organique : bouche, pas monologue.
        target = 3 + int(field.get("sentence_need", 0.0) * 4 + field.get("flow_need", 0.0) * 2)
        target -= int(impulse.compression * 2)
        target = max(3, min(10, max(target, min(len(material), len(seed) + 1))))
        transposed = [w for w in transposed if w]
        transposed = self._repair_operator_collisions(transposed[:target], impulse)
        if not transposed:
            return text
        return " ".join(transposed)

    def _repair_operator_collisions(self, words, impulse) -> List[str]:
        """Répare seulement des collisions de particules grammaticales."""
        cleaned = []
        previous = ""
        for tok in words or []:
            tok = self._normalize_surface_token(tok) if tok != "…" else "…"
            if not tok:
                continue
            if tok == previous and tok != "…":
                continue
            if previous == "je" and tok in {"je", "tu", "toi", "te", "t"}:
                continue
            if previous == "ne" and tok == "pas":
                # Attend au moins une matière entre ne/pas quand c'est possible.
                continue
            cleaned.append(tok)
            previous = tok
        # contractions minimales pour éviter les surfaces cassées
        repaired = []
        i = 0
        while i < len(cleaned):
            tok = cleaned[i]
            nxt = cleaned[i + 1] if i + 1 < len(cleaned) else ""
            if tok == "je" and nxt in {"ai", "aime", "avance", "entends"}:
                repaired.append("j'" + nxt)
                i += 2
                continue
            if tok == "ne" and nxt in {"ai", "aime", "avance", "entends"}:
                repaired.append("n'" + nxt)
                i += 2
                continue
            repaired.append(tok)
            i += 1
        return repaired

    def _final_living_language_stabilizer(self, text: str, impulse: LivingImpulse, field: Optional[Dict[str, float]] = None) -> str:
        """
        Stabilisateur linguistique final V4.9.2.

        Rôle exact : protéger la phrase publique après les mutations vivantes.
        Il ne décide pas du fond, ne choisit pas une réponse pré-écrite et ne
        remplace pas la cognition. Il répare seulement la surface française :
        perspective, collisions de pronoms, particules internes, petits trous
        syntaxiques et ordre minimal sujet/verbe.
        """
        field = field or {}
        raw = str(text or "").strip()
        if not raw:
            return "…"

        # 1) Nettoyage des fuites internes et marqueurs de trace.
        raw = re.sub(r"\b(?:coherence[_-]?globale|coh[ée]rence[_-]?globale|neutral|inquiry|antagonism|affection)\b", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\b(?:meaning|signal|trace|score|runtime|guard|v\d+)\b", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"[_]{2,}", " ", raw)

        tokens = [self._normalize_surface_token(w) if w != "…" else "…" for w in raw.split()]
        tokens = [w for w in tokens if w]
        if not tokens:
            return "…"

        # 2) Réparations de perspective : on évite les formes impossibles
        # produites par les transpositions token-par-token.
        repaired: List[str] = []
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            nxt = tokens[i + 1] if i + 1 < len(tokens) else ""

            if tok == "avec" and nxt == "je":
                repaired.extend(["avec", "moi"]); i += 2; continue
            if tok == "pour" and nxt == "je":
                repaired.extend(["pour", "moi"]); i += 2; continue
            if tok == "chez" and nxt == "je":
                repaired.extend(["chez", "moi"]); i += 2; continue

            # "toi + verbe" en position sujet devient "tu + verbe conjugué".
            if tok == "toi" and nxt:
                repaired.append("tu")
                repaired.append(self._second_person_surface(nxt))
                i += 2
                continue

            # "que toi parle" / "quand toi ..." etc.
            if tok in {"que", "quand", "si", "avant", "apres", "après"} and nxt == "toi":
                repaired.append(tok)
                repaired.append("tu")
                third = tokens[i + 2] if i + 2 < len(tokens) else ""
                if third:
                    repaired.append(self._second_person_surface(third))
                    i += 3
                else:
                    i += 2
                continue

            repaired.append(tok)
            i += 1
        tokens = repaired

        # 3) Réparations syntaxiques globales très limitées.
        s = " ".join(tokens)
        s = re.sub(r"\bje pensais quoi\b", "je pensais à quoi", s)
        s = re.sub(r"\bje pense quoi\b", "je pense à quoi", s)
        s = re.sub(r"\bje sens\s+(vivant|vivante|présent|presente|présente)\b", r"je me sens \1", s)
        s = re.sub(r"\bje me\s+…\s+sens\b", "je me sens", s)
        s = re.sub(r"\bje me\s+sens\s+…\s+", "je me sens ", s)
        s = re.sub(r"\best ce que\s+…\s+(j'ai|je suis|je peux|je veux)\b", r"est ce que \1", s)
        s = re.sub(r"\bje ressens\s+maintenant\b", "ce que je ressens maintenant", s)
        s = re.sub(r"\braconte\s+tu\s+ce\s+que\s+…\s+ce\s+que\s+je\s+ressens\s+maintenant\b", "ce que je ressens maintenant", s)
        s = re.sub(r"\braconte\s+tu\s+ce\s+que\b", "ce que", s)
        s = re.sub(r"\bce\s+que\s+ce\s+…\s+que\b", "ce que", s)
        s = re.sub(r"\bce\s+que\s+ce\s+que\b", "ce que", s)
        s = re.sub(r"\braconte\s+toi\b", "raconte-moi", s)
        s = re.sub(r"\bqui\s+es\s+je\b", "qui suis-je", s)
        s = re.sub(r"\bqui\s+je\s+vraiment\b", "qui je suis vraiment", s)
        s = re.sub(r"\best\s+ce\s+que\s+je\s+as\b", "est ce que j'ai", s)
        s = re.sub(r"\bje\s+as\b", "j'ai", s)
        s = re.sub(r"\bje\s+es\b", "je suis", s)
        s = re.sub(r"\bje\s+ai\b", "j'ai", s)
        s = re.sub(r"\btu\s+es\b", "tu es", s)
        s = re.sub(r"\btu\s+as\b", "tu as", s)

        # 4) Si le résultat est une récitation brute du message utilisateur,
        # on réduit vers un noyau prononçable plutôt que de le retourner cassé.
        words = [w for w in s.split() if w]
        seed = [self._normalize_surface_token(w) for w in getattr(impulse, "trajectory_seed", []) or []]
        seed = [w for w in seed if w]
        if seed and words:
            overlap = len(set(words) & set(seed)) / max(1, len(set(words)))
            same_head = words[:min(3, len(words), len(seed))] == seed[:min(3, len(words), len(seed))]
            if overlap > 0.88 and same_head and len(words) >= 6 and getattr(impulse, "curiosity", 0.0) < 0.50:
                nucleus = []
                for w in words:
                    if w in {"tu", "toi", "je", "me", "moi"} and nucleus:
                        continue
                    if w not in nucleus:
                        nucleus.append(w)
                    if len(nucleus) >= 7:
                        break
                words = nucleus

        # 5) Dernière hygiène : pauses, doublons, longueur, minuscule naturelle.
        # Les pauses ne doivent pas couper des groupes grammaticaux courts.
        if getattr(impulse, "doubt", 0.0) < 0.58 and getattr(impulse, "tension", 0.0) < 0.70:
            words = [w for w in words if w != "…"]
        else:
            protected_pause = []
            for idx, w in enumerate(words):
                prev_w = words[idx - 1] if idx > 0 else ""
                next_w = words[idx + 1] if idx + 1 < len(words) else ""
                if w == "…" and (prev_w in {"je", "tu", "me", "te", "ce", "que", "est", "dialogue"} or next_w in {"suis", "sens", "ai", "as", "es", "que"}):
                    continue
                protected_pause.append(w)
            words = protected_pause

        s2 = " ".join(words)
        s2 = re.sub(r"\bce\s+que\s+ce\s+que\b", "ce que", s2)
        s2 = re.sub(r"\bce\s+que\s+que\b", "ce que", s2)
        words = [w for w in s2.split() if w]

        clean: List[str] = []
        for w in words:
            w = self._normalize_surface_token(w) if w != "…" else "…"
            if not w:
                continue
            if clean and clean[-1] == w and w != "…":
                continue
            if w == "…" and (not clean or clean[-1] == "…"):
                continue
            clean.append(w)

        max_len = 14
        if getattr(impulse, "compression", 0.0) > 0.55 or getattr(impulse, "tension", 0.0) > 0.72:
            max_len = 9
        elif field.get("flow_need", 0.0) > 0.55:
            max_len = 16
        clean = clean[:max_len]
        return " ".join(clean) if clean else "…"

    def _second_person_surface(self, token: str) -> str:
        """Conjugaison de surface très limitée pour réparer 'toi + verbe'."""
        tok = self._normalize_surface_token(token)
        if not tok:
            return tok
        irregular = {
            "suis": "es", "es": "es", "est": "es", "etre": "es", "être": "es",
            "ai": "as", "as": "as", "a": "as", "avoir": "as",
            "vais": "vas", "va": "vas", "aller": "vas",
            "veux": "veux", "veut": "veux", "vouloir": "veux",
            "peux": "peux", "peut": "peux", "pouvoir": "peux",
            "fais": "fais", "fait": "fais", "faire": "fais",
            "dis": "dis", "dit": "dis", "dire": "dis",
            "sens": "sens", "sent": "sens", "sentir": "sens",
            "ressens": "ressens", "ressent": "ressens", "ressentir": "ressens",
            "pense": "penses", "pensais": "pensais", "parle": "parles",
            "écoute": "écoutes", "ecoute": "écoutes", "regarde": "regardes",
        }
        if tok in irregular:
            return irregular[tok]
        if tok.endswith("er") and len(tok) > 3:
            return tok[:-2] + "es"
        if tok.endswith("e") and len(tok) > 3:
            return tok + "s"
        return tok

    def _organic_text_finish(self, text: str, impulse: LivingImpulse) -> str:
        """Nettoyage minimal : pas de lissage artificiel ni de ponctuation forcée ici."""
        text = self._clean_living_text(text)
        return self._punctuate_living_text(text, impulse)


    def _collect_full_living_language_context(
        self,
        impulse: LivingImpulse,
        field: Optional[Dict[str, float]] = None,
        units: Optional[List[Dict[str, Any]]] = None,
        particles: Optional[List[Any]] = None,
        grammar: Optional[Any] = None,
        current_surface: str = "",
    ) -> Dict[str, Any]:
        """
        Bridge profond vers LivingLanguageGenerator.

        Ce paquet n'est pas une réponse et ne contient aucune phrase préécrite.
        Il transporte les signaux vivants disponibles dans la bouche :
        impulsion, pression, continuité, temporalité, concepts, particules,
        relations, trajectoire, inertie expressive et traces de qualité.
        """
        field = dict(field or {})
        units = list(units or [])
        particles = list(particles or [])

        def clamp01(value: Any) -> float:
            try:
                return max(0.0, min(1.0, float(value)))
            except Exception:
                return 0.0

        def norm_token(value: Any) -> str:
            try:
                return self._normalize_surface_token(str(value))
            except Exception:
                return str(value or "").strip().lower()

        concepts = []
        for token in list(getattr(impulse, "concepts", []) or []):
            tok = norm_token(token)
            if tok and tok not in concepts:
                concepts.append(tok)

        trajectory = []
        for token in list(getattr(impulse, "trajectory_seed", []) or []):
            tok = norm_token(token)
            if tok and tok not in trajectory:
                trajectory.append(tok)

        particle_tokens = []
        particle_energy = {}
        for particle in particles:
            tok = norm_token(getattr(particle, "token", ""))
            if not tok:
                continue
            if tok not in particle_tokens:
                particle_tokens.append(tok)
            particle_energy[tok] = max(
                particle_energy.get(tok, 0.0),
                clamp01(getattr(particle, "activation", 0.0))
                + clamp01(getattr(particle, "pull", 0.0)) * 0.5
                + clamp01(getattr(particle, "continuity", 0.0)) * 0.35,
            )

        relation_tokens = []
        relations = []
        for source, target, relation_type in list(getattr(impulse, "relations", []) or []):
            src = norm_token(source)
            tgt = norm_token(target)
            typ = str(relation_type or "").strip()
            if src and tgt:
                relations.append({"source": src, "target": tgt, "type": typ})
                for tok in (src, tgt):
                    if tok not in relation_tokens:
                        relation_tokens.append(tok)

        unit_tokens = []
        for node in units:
            if not isinstance(node, dict):
                continue
            for key in ("source", "target"):
                tok = norm_token(node.get(key, ""))
                if tok and tok not in unit_tokens:
                    unit_tokens.append(tok)

        grammar_context = {}
        if grammar is not None:
            for key in ("nucleus", "approach", "tension", "expansion", "restraint"):
                vals = []
                for tok in list(getattr(grammar, key, []) or []):
                    nt = norm_token(tok)
                    if nt and nt not in vals:
                        vals.append(nt)
                grammar_context[key] = vals
            grammar_context["pause"] = clamp01(getattr(grammar, "pause", 0.0))
            grammar_context["compression"] = clamp01(getattr(grammar, "compression", 0.0))
            grammar_context["coherence"] = clamp01(getattr(grammar, "coherence", 0.0))
            grammar_context["vitality"] = clamp01(getattr(grammar, "vitality", 0.0))

        continuity_signature = dict(getattr(impulse, "continuity_signature", {}) or {})
        intentions = dict(getattr(impulse, "intentions", {}) or {})

        living_state = {
            "tension": clamp01(getattr(impulse, "tension", 0.0)),
            "warmth": clamp01(getattr(impulse, "warmth", 0.0)),
            "curiosity": clamp01(getattr(impulse, "curiosity", 0.0)),
            "doubt": clamp01(getattr(impulse, "doubt", 0.0)),
            "directness": clamp01(getattr(impulse, "directness", 0.0)),
            "fluidity": clamp01(getattr(impulse, "fluidity", 0.0)),
            "compression": clamp01(getattr(impulse, "compression", 0.0)),
            "intensity": clamp01(getattr(impulse, "intensity", 0.0)),
            "field_flow_need": clamp01(field.get("flow_need", 0.0)),
            "field_sentence_need": clamp01(field.get("sentence_need", 0.0)),
            "field_silence": clamp01(field.get("silence", 0.0)),
            "field_rupture": clamp01(field.get("rupture", 0.0)),
            "living_temporality": clamp01(field.get("living_temporality", 0.0)),
            "temporal_wave": field.get("temporal_wave", 0.0),
        }

        expressive_inertia = {
            key: clamp01(value)
            for key, value in getattr(self, "expressive_inertia", {}).items()
        }

        # Mémoire textuelle non préécrite : traces compactes, pas phrases à ressortir.
        self_memory = [
            f"state:{k}:{round(v, 3)}"
            for k, v in living_state.items()
            if isinstance(v, (int, float))
        ]
        self_memory += [
            f"intention:{k}:{round(float(v), 3)}"
            for k, v in intentions.items()
            if isinstance(v, (int, float))
        ]
        self_memory += [
            f"continuity:{k}:{round(float(v), 3)}"
            for k, v in continuity_signature.items()
            if isinstance(v, (int, float))
        ]
        self_memory += [
            f"inertia:{k}:{round(float(v), 3)}"
            for k, v in expressive_inertia.items()
            if isinstance(v, (int, float))
        ]

        if getattr(impulse, "dominant_text", ""):
            self_memory.append(f"dominant:{norm_token(impulse.dominant_text)}")

        active_impulses = []
        for key, value in intentions.items():
            if isinstance(value, (int, float)) and value > 0.12:
                active_impulses.append(key)
        for key, value in living_state.items():
            if isinstance(value, (int, float)) and value > 0.45:
                active_impulses.append(key)
        active_impulses = list(dict.fromkeys(active_impulses))

        # Priorité aux traces propres de Leia / trajectoire interne plutôt qu'au miroir utilisateur.
        leia_words = []
        for source in (
            grammar_context.get("nucleus", []),
            grammar_context.get("approach", []),
            grammar_context.get("tension", []),
            grammar_context.get("expansion", []),
            particle_tokens,
            unit_tokens,
            concepts,
        ):
            for tok in source:
                if tok and tok not in leia_words:
                    leia_words.append(tok)

        user_words = trajectory

        focus_words = []
        for source in (leia_words, particle_tokens, relation_tokens, user_words):
            for tok in source:
                if tok and tok not in focus_words:
                    focus_words.append(tok)
                if len(focus_words) >= 16:
                    break
            if len(focus_words) >= 16:
                break

        emotional_pressure = (
            living_state["tension"] * 0.45
            + living_state["curiosity"] * 0.25
            + living_state["doubt"] * 0.20
            + living_state["field_rupture"] * 0.20
            - living_state["warmth"] * 0.18
        )

        payload = getattr(self, "_current_living_payload", {}) or {}
        external = getattr(self, "_current_external_signals", {}) or {}
        user_message = str(getattr(self, "_current_user_message", "") or "")

        def flatten_numeric(prefix: str, obj: Any, limit: int = 18) -> List[str]:
            out: List[str] = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if len(out) >= limit:
                        break
                    if isinstance(v, (int, float)):
                        out.append(f"{prefix}:{k}:{round(float(v), 3)}")
                    elif isinstance(v, dict):
                        for kk, vv in list(v.items())[:6]:
                            if isinstance(vv, (int, float)) and len(out) < limit:
                                out.append(f"{prefix}:{k}.{kk}:{round(float(vv), 3)}")
            return out

        merged_living_state = dict(living_state)
        for source_key in ("emotional_state", "internal_needs", "mental_momentum", "embodied_state", "presence", "attention"):
            src = payload.get(source_key, {})
            if isinstance(src, dict):
                for k, v in src.items():
                    if isinstance(v, (int, float)):
                        merged_living_state[k] = max(float(merged_living_state.get(k, 0.0)), clamp01(v))
        if "expression_pressure" in payload:
            merged_living_state["expression"] = max(float(merged_living_state.get("expression", 0.0)), clamp01(payload.get("expression_pressure")))
        if "restraint" in payload:
            merged_living_state["restraint"] = clamp01(payload.get("restraint"))

        self_memory += flatten_numeric("payload", payload, 24)
        self_memory += flatten_numeric("external", external, 12)

        causal_entries: List[Dict[str, Any]] = []
        for key in ("causal_memory", "living_causal_graph", "long_causal_arc", "relational_bond"):
            val = payload.get(key)
            if isinstance(val, dict):
                causal_entries.append({"source": key, "values": {k: v for k, v in list(val.items())[:12] if isinstance(v, (str, int, float, bool))}})

        # Ajoute des mots internes propres, mais limite les mots utilisateur pour éviter le perroquet.
        for key in ("dominant_living_axis", "focus", "response_mode"):
            val = payload.get(key)
            if isinstance(val, str):
                tok = norm_token(val)
                if tok and tok not in focus_words:
                    focus_words.insert(0, tok)

        return {
            "user_message": user_message,
            "self_memory": [m if isinstance(m, dict) else {"content": str(m), "source": "expression_bridge"} for m in self_memory[:64]],
            "active_impulses": active_impulses[:20],
            "emotional_pressure": emotional_pressure,
            "focus_words": focus_words[:18],
            "user_words": user_words[:10],
            "leia_words": leia_words[:22],
            "living_state": merged_living_state,
            "causal_memory": causal_entries[:10],
            "intentions": intentions,
            "continuity_signature": continuity_signature,
            "relations": relations[:12],
            "grammar_context": grammar_context,
            "particle_energy": particle_energy,
            "expressive_inertia": expressive_inertia,
            "current_surface": str(current_surface or "")[:300],
        }

    def _generate_with_full_living_language_context(
        self,
        impulse: LivingImpulse,
        field: Optional[Dict[str, float]] = None,
        units: Optional[List[Dict[str, Any]]] = None,
        particles: Optional[List[Any]] = None,
        grammar: Optional[Any] = None,
        current_surface: str = "",
    ) -> Optional[str]:
        """
        Appelle LivingLanguageGenerator avec tout ce qu'il peut accepter.
        Si sa signature est ancienne, on compacte quand même le contexte complet
        dans self_memory/focus_words/active_impulses pour ne pas perdre le vivant.
        """
        generator = getattr(self, "external_living_language_generator", None)
        if generator is None:
            return None

        context = self._collect_full_living_language_context(
            impulse=impulse,
            field=field,
            units=units,
            particles=particles,
            grammar=grammar,
            current_surface=current_surface,
        )

        try:
            signature = inspect.signature(generator.generate)
            accepted = set(signature.parameters.keys())
            accepts_kwargs = any(
                p.kind == inspect.Parameter.VAR_KEYWORD
                for p in signature.parameters.values()
            )

            payload = {}
            for key, value in context.items():
                if accepts_kwargs or key in accepted:
                    payload[key] = value

            # Compatibilité minimale avec les signatures récentes et anciennes.
            required_defaults = {
                "user_message": context.get("user_message", ""),
                "living_state": context.get("living_state", {}),
                "self_memory": context.get("self_memory", []),
                "active_impulses": context.get("active_impulses", []),
                "emotional_pressure": context.get("emotional_pressure", 0.0),
                "causal_memory": context.get("causal_memory", []),
                "focus_words": context.get("focus_words", []),
            }
            for required, default in required_defaults.items():
                if accepts_kwargs or required in accepted:
                    payload.setdefault(required, default)

            generated = generator.generate(**payload)

            if isinstance(generated, str):
                generated_text = generated.strip()
            else:
                generated_text = str(getattr(generated, "text", "") or "").strip()

            if len(generated_text.split()) < 2:
                return None

            confidence = getattr(generated, "confidence", None)
            if isinstance(confidence, (int, float)) and confidence < 0.28:
                return None

            return generated_text

        except Exception:
            return None


    def _realize_living_impulse(self, impulse: LivingImpulse) -> str:
        """
        V4.9 : réalisation vivante plus libre.

        Les garde-fous existent encore pour éviter le crash, mais la fin n'est
        plus une porte dure qui remplace le flux. Elle module doucement ce qui
        est né du tour actuel.
        """
        started = time.perf_counter()
        self.last_runtime_guard_trace = {"guarded": False, "stage": "start", "elapsed_ms": 0}

        def elapsed() -> float:
            return time.perf_counter() - started

        def guard(stage: str, field=None, units=None, particles=None, grammar=None, text=""):
            if elapsed() <= self.expression_time_budget:
                return None
            self.last_runtime_guard_trace = {
                "guarded": True,
                "stage": stage,
                "elapsed_ms": round(elapsed() * 1000, 2),
                "concepts": len(getattr(impulse, "concepts", []) or []),
                "relations": len(getattr(impulse, "relations", []) or []),
                "units": len(units or []),
                "particles": len(particles or []),
            }
            compact = self._compact_living_surface_from_current_material(
                impulse=impulse,
                field=field or {},
                units=units or [],
                particles=particles or [],
                grammar=grammar,
                text=text,
            )
            return self._organic_text_finish(compact, impulse)

        field = self._advance_expression_temporality(
            self._build_expressive_field(impulse),
            impulse,
        )
        self._last_living_impulse = impulse
        self._last_living_field = field
        guarded = guard("field", field=field)
        if guarded is not None:
            return guarded

        raw_units = self._generate_linguistic_units_from_field(field, impulse)
        units = self._living_competition_order(raw_units, field, impulse, limit=self.max_relation_units)
        guarded = guard("units", field=field, units=units)
        if guarded is not None:
            return guarded

        particles = self._build_prelanguage_particles(impulse, field, units)
        propagated_particles = self._propagate_prelanguage_particles(particles, impulse, field)
        prelanguage_surface = self._materialize_particle_stream(propagated_particles, impulse, field)
        guarded = guard("prelanguage", field=field, units=units, particles=propagated_particles, text=prelanguage_surface)
        if guarded is not None:
            return guarded

        grammar = self._organize_units_with_internal_grammar(units, field, impulse)
        shaped = self._materialize_organic_grammar(grammar, field, impulse)
        continuous = self._stabilize_continuous_sentence_trajectory(shaped, grammar, units, field, impulse)
        guarded = guard("grammar", field=field, units=units, particles=propagated_particles, grammar=grammar, text=continuous)
        if guarded is not None:
            return guarded

        fused = self._fuse_prelanguage_and_grammar_streams(
            prelanguage_surface,
            continuous,
            propagated_particles,
            grammar,
            field,
            impulse,
        )
        drifted = self._apply_living_syntax_drift(fused, propagated_particles, field, impulse)
        breathed = self._cognitive_breath_modulate(drifted, propagated_particles, field, impulse)

        # Les réparations restent présentes, mais elles ne reprennent plus le pouvoir
        # sur la surface : si elles cassent trop le flux, le texte respiré gagne.
        repaired = self._repair_fragmented_relation_flow(breathed, grammar, units, field, impulse)
        reviewed = self._self_review_and_repair(repaired, units, field, impulse)
        candidate = reviewed if len(str(reviewed or "").split()) >= max(1, len(str(breathed or "").split()) // 2) else breathed
        final = self._soften_surface_control(candidate, grammar, units, field, impulse)
        final = self._deecho_living_surface(final, impulse, field, units, propagated_particles, grammar)
        final = self._inhabit_living_surface(final, impulse, field, units, propagated_particles, grammar)

        # =========================================================================
        # FULL LIVING LANGUAGE GENERATOR PRIORITY
        # =========================================================================
        external_surface = self._generate_with_full_living_language_context(
            impulse=impulse,
            field=field,
            units=units,
            particles=propagated_particles,
            grammar=grammar,
            current_surface=final,
        )
        if external_surface:
            final = external_surface

        final = self._final_living_language_stabilizer(final, impulse, field)

        self.last_living_autonomy_trace = {
            "field_temporality": round(field.get("living_temporality", 0.0), 3),
            "phase": round(self.expressive_time_phase, 3),
            "inertia": {k: round(v, 3) for k, v in self.expressive_inertia.items()},
            "soft_gate": self.last_full_living_trace.get("soft_final_quality"),
        }
        self.last_runtime_guard_trace = {"guarded": False, "stage": "complete", "elapsed_ms": round(elapsed() * 1000, 2)}
        return self._organic_text_finish(final, impulse)

    def _compact_living_surface_from_current_material(self, impulse, field=None, units=None, particles=None, grammar=None, text="") -> str:
        """Compaction non préécrite : seulement matière actuelle + pression interne."""
        field = field or {}
        candidates = []
        for particle in sorted(list(particles or []), key=lambda p: (getattr(p, "activation", 0.0), getattr(p, "pull", 0.0)), reverse=True):
            tok = self._normalize_surface_token(getattr(particle, "token", ""))
            if tok and tok not in candidates:
                candidates.append(tok)
        for node in list(units or [])[:self.max_relation_units]:
            for key in ("source", "target"):
                tok = self._normalize_surface_token(node.get(key, ""))
                if tok and tok not in candidates:
                    candidates.append(tok)
        if grammar is not None:
            for group in (getattr(grammar, "nucleus", []), getattr(grammar, "approach", []), getattr(grammar, "tension", []), getattr(grammar, "expansion", [])):
                for tok in group:
                    tok = self._normalize_surface_token(tok)
                    if tok and tok not in candidates:
                        candidates.append(tok)
        for tok in list(getattr(impulse, "trajectory_seed", []) or []) + list(getattr(impulse, "concepts", []) or []):
            tok = self._normalize_surface_token(tok)
            if tok and tok not in candidates:
                candidates.append(tok)

        target = 3 + int(field.get("sentence_need", 0.0) * 3 + field.get("flow_need", 0.0) * 2)
        target -= int(getattr(impulse, "compression", 0.0) * 2 + field.get("silence", 0.0) * 2)
        target = max(2, min(7, target))
        if not candidates:
            return "…"
        return " ".join(self._stabilize_linguistic_flow(candidates[:target], impulse))

    def _deecho_living_surface(self, text, impulse, field, units, particles, grammar) -> str:
        """Évite que la bouche répète mécaniquement tout le message utilisateur."""
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        lexical = [w for w in words if w != "…"]
        seed = [self._normalize_surface_token(w) for w in getattr(impulse, "trajectory_seed", []) or []]
        seed = [w for w in seed if w]
        if not lexical or not seed:
            return text
        same_order = lexical == seed[:len(lexical)] or lexical[:len(seed)] == seed
        overlap = len(set(lexical) & set(seed)) / max(1, len(set(lexical)))
        too_mirror = same_order and overlap > 0.88 and len(lexical) >= 6 and impulse.curiosity < 0.55
        if not too_mirror:
            return text

        material = self._compact_living_surface_from_current_material(impulse, field, units, particles, grammar, text)
        mat_words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(material).split()]
        mat_words = [w for w in mat_words if w and w != "…"]
        # V4.9 : désécho doux. On compresse sans casser l'ordre naturel.
        ordered = self._restore_living_concept_order(mat_words or lexical, impulse)
        if len(ordered) >= len(seed):
            ordered = ordered[:max(2, len(seed) - 2)]
        ordered = self._stabilize_linguistic_flow(ordered, impulse)
        return " ".join(ordered or lexical[:2])



    def _build_prelanguage_particles(self, impulse: LivingImpulse, field: Dict[str, float], units) -> List[LivingSemanticParticle]:
        """
        Crée un flux pré-linguistique depuis le tour actuel.
        Aucun contenu ancien n'est réinjecté en surface : la mémoire ne change
        que l'énergie et la continuité des particules présentes maintenant.
        """
        ordered_tokens: List[str] = []

        def push(token: Any) -> None:
            tok = self._normalize_surface_token(token)
            if tok and tok not in ordered_tokens:
                ordered_tokens.append(tok)

        push(impulse.dominant_text)
        for token in getattr(impulse, "trajectory_seed", []) or []:
            push(token)
        for source, target, _relation in getattr(impulse, "relations", []) or []:
            push(source)
            push(target)
        for node in list(units or []):
            push(node.get("source", ""))
            push(node.get("target", ""))
        for token in getattr(impulse, "concepts", []) or []:
            push(token)

        particles: List[LivingSemanticParticle] = []
        total = max(1, len(ordered_tokens))
        continuity = field.get("continuity", 0.0)
        for index, token in enumerate(ordered_tokens[:12]):
            memory_pressure = self.semantic_particle_memory[token]
            position_pull = 1.0 - min(1.0, index / max(1, total)) * 0.32
            mass = (
                len(token) * 0.028
                + impulse.intensity * 0.32
                + field.get("resolution", 0.0) * 0.18
                + field.get("contact", 0.0) * 0.12
                + memory_pressure * 0.16
            )
            pull = (
                position_pull * 0.34
                + field.get("flow_need", 0.0) * 0.26
                + impulse.fluidity * 0.18
                + continuity * 0.18
            )
            instability = (
                impulse.tension * 0.28
                + impulse.doubt * 0.24
                + field.get("rupture", 0.0) * 0.22
                + abs(0.5 - position_pull) * 0.10
            )
            particles.append(LivingSemanticParticle(
                token=token,
                origin="current",
                mass=max(0.0, min(1.8, mass)),
                pull=max(0.0, min(1.4, pull)),
                instability=max(0.0, min(1.2, instability)),
                activation=0.0,
                continuity=max(0.0, min(1.0, continuity + memory_pressure * 0.08)),
                order=index,
            ))

        link_map = defaultdict(list)
        for source, target, _relation in getattr(impulse, "relations", []) or []:
            src = self._normalize_surface_token(source)
            tgt = self._normalize_surface_token(target)
            if src and tgt:
                link_map[src].append(tgt)
                link_map[tgt].append(src)
        for particle in particles:
            particle.links = [t for t in link_map.get(particle.token, []) if t]

        return particles

    def _propagate_prelanguage_particles(self, particles: List[LivingSemanticParticle], impulse: LivingImpulse, field: Dict[str, float]) -> List[LivingSemanticParticle]:
        """Propagation courte : activation, collision et dominance sans template."""
        if not particles:
            return []

        activations = {p.token: p.mass + p.pull - p.instability * 0.18 for p in particles}
        index = {p.token: p for p in particles}
        steps = 2 + int(min(2, field.get("continuity", 0.0) * 2 + impulse.curiosity))
        for _ in range(steps):
            nxt = {}
            for particle in particles:
                linked_energy = 0.0
                for linked in particle.links:
                    linked_energy += activations.get(linked, 0.0) * 0.18
                local_memory = self.semantic_particle_memory[particle.token] * 0.05
                decay = particle.instability * 0.10 + impulse.compression * 0.08
                nxt[particle.token] = max(0.0, activations.get(particle.token, 0.0) * 0.72 + linked_energy + particle.pull * 0.18 + local_memory - decay)
            activations = nxt

        avg = sum(activations.values()) / max(1, len(activations))
        for particle in particles:
            particle.activation = max(0.0, min(2.0, activations.get(particle.token, 0.0)))
            particle.collision = abs(particle.activation - avg) + particle.instability * 0.35
            self.semantic_particle_memory[particle.token] = (
                self.semantic_particle_memory[particle.token] * 0.94
                + particle.activation * 0.06
            )

        for key in list(self.semantic_particle_memory.keys()):
            self.semantic_particle_memory[key] *= 0.992
            if self.semantic_particle_memory[key] < 0.015:
                del self.semantic_particle_memory[key]

        self.last_prelanguage_trace = {
            "particles": len(particles),
            "dominance": round(max((p.activation for p in particles), default=0.0), 3),
            "collision": round(sum(p.collision for p in particles) / max(1, len(particles)), 3),
            "flow": round(field.get("flow_need", 0.0), 3),
        }
        self.prelinguistic_flow_memory.append(dict(self.last_prelanguage_trace))
        return particles

    def _materialize_particle_stream(self, particles: List[LivingSemanticParticle], impulse: LivingImpulse, field: Dict[str, float]) -> str:
        """Matérialise le flux pré-linguistique : ordre dynamique, pas phrase prête."""
        if not particles:
            return ""

        ordered = sorted(
            particles,
            key=lambda p: (
                p.activation * 0.42
                + p.pull * 0.24
                + p.continuity * 0.16
                - p.collision * 0.10
                + (1.0 / (1.0 + p.order)) * 0.08
            ),
            reverse=True,
        )

        if field.get("flow_need", 0.0) > field.get("rupture", 0.0):
            ordered.sort(key=lambda p: (p.order, -p.activation))

        target = 3 + int(field.get("sentence_need", 0.0) * 4 + field.get("flow_need", 0.0) * 3)
        target -= int(impulse.compression * 3 + field.get("silence", 0.0) * 2)
        current_sequence_len = len([w for w in getattr(impulse, "trajectory_seed", []) or [] if self._normalize_surface_token(w)])
        if impulse.tension < 0.66 and impulse.compression < 0.45:
            target = max(target, min(8, current_sequence_len))
        target = max(2, min(10, target))

        words: List[str] = []
        for particle in ordered:
            if particle.token and particle.token not in words:
                words.append(particle.token)
            if len(words) >= target:
                break

        current_sequence = [self._normalize_surface_token(w) for w in getattr(impulse, "trajectory_seed", []) or []]
        current_sequence = [w for w in current_sequence if w]
        if (
            current_sequence
            and impulse.tension < 0.66
            and field.get("rupture", 0.0) < field.get("flow_need", 0.0) + 0.45
            and len(current_sequence) >= len(words)
        ):
            words = current_sequence[:max(len(words), min(len(current_sequence), target))]

        if not words and impulse.dominant_text:
            words = [self._normalize_surface_token(impulse.dominant_text)]

        return " ".join(self._stabilize_linguistic_flow(words, impulse))

    def _fuse_prelanguage_and_grammar_streams(self, prelanguage_text, grammar_text, particles, grammar, field, impulse) -> str:
        """Fusionne impulsion pré-linguistique et grammaire sans imposer de phrase."""
        particle_words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(prelanguage_text or "").split()]
        grammar_words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(grammar_text or "").split()]
        particle_words = [w for w in particle_words if w]
        grammar_words = [w for w in grammar_words if w]

        activation_rank = {p.token: p.activation + p.pull - p.collision * 0.12 for p in particles or []}
        fused: List[str] = []
        # Le flux pré-linguistique est prioritaire. La grammaire complète
        # seulement avec du matériau absent pour éviter les échos mécaniques.
        grammar_additions = [w for w in grammar_words if w not in particle_words]
        candidates = particle_words + grammar_additions
        for word in candidates:
            if not word:
                continue
            if fused and word == fused[-1]:
                continue
            fused.append(word)

        if activation_rank and field.get("rupture", 0.0) > field.get("flow_need", 0.0):
            fused.sort(key=lambda w: activation_rank.get(w, 0.0), reverse=True)
        elif not (particle_words and impulse.tension < 0.66):
            fused = self._restore_living_concept_order(fused, impulse)

        if not fused:
            return prelanguage_text or grammar_text or "…"
        return " ".join(self._stabilize_linguistic_flow(fused, impulse))

    def _apply_living_syntax_drift(self, text, particles, field, impulse) -> str:
        """Dérive syntaxique vivante : changement doux de trajectoire, pas random."""
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        lexical = [w for w in words if w != "…"]
        if len(lexical) < 3:
            return " ".join(words)

        collision = sum((p.collision for p in particles or []), 0.0) / max(1, len(particles or []))
        self.drift_phase = max(-1.0, min(1.0, self.drift_phase * 0.70 + (field.get("flow_need", 0.0) - field.get("rupture", 0.0)) * 0.20 + (impulse.curiosity - impulse.doubt) * 0.10))
        drift_pressure = abs(self.drift_phase) + collision * 0.12 + field.get("continuity", 0.0) * 0.08

        if drift_pressure > 0.38 and len(lexical) >= 5:
            head = lexical[:2]
            tail = lexical[2:]
            if self.drift_phase >= 0:
                lexical = head + tail[:2] + tail[2:]
            else:
                lexical = head[:1] + tail[:1] + head[1:] + tail[1:]

        if (impulse.doubt + field.get("silence", 0.0)) > 0.72 and "…" not in lexical and len(lexical) > 3:
            lexical.insert(max(1, min(len(lexical) - 1, 2 + int(collision))), "…")

        signature = self._surface_fingerprint(lexical)
        self.syntax_mutation_memory.append(signature)
        return " ".join(self._stabilize_linguistic_flow(lexical, impulse))

    def _cognitive_breath_modulate(self, text, particles, field, impulse) -> str:
        """Respiration cognitive : dose la longueur depuis charge interne."""
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        if not words:
            return "…"

        lexical = [w for w in words if w != "…"]
        collision = sum((p.collision for p in particles or []), 0.0) / max(1, len(particles or []))
        breath = (
            field.get("flow_need", 0.0) * 0.34
            + field.get("contact", 0.0) * 0.18
            + field.get("exploration", 0.0) * 0.18
            - field.get("silence", 0.0) * 0.28
            - impulse.compression * 0.22
            - collision * 0.05
        )
        target = 4 + int(max(-1.0, min(1.0, breath)) * 4)
        target += int(field.get("continuity", 0.0) * 2)
        current_material = len([c for c in getattr(impulse, "concepts", []) or [] if self._normalize_surface_token(c)])
        if impulse.tension < 0.62 and impulse.compression < 0.45:
            target = max(target, min(7, current_material))
        target = max(2, min(11, target))
        if impulse.tension > 0.72:
            target = min(target, 6)
        if impulse.doubt > 0.66 and impulse.directness < 0.55:
            target = min(target, 5)

        selected = lexical[:target]
        if "…" in words and len(selected) > 3 and (impulse.doubt + field.get("silence", 0.0)) > 0.55:
            selected.insert(min(len(selected) - 1, max(1, target // 2)), "…")
        return " ".join(self._stabilize_linguistic_flow(selected, impulse))

    def _build_expressive_field(self, impulse: LivingImpulse) -> Dict[str, float]:
        """
        Champ expressif interne.
        Il ne contient pas de mots, seulement des forces.
        """
        intentions = getattr(impulse, "intentions", {}) or {}
        return {
            "movement": (
                impulse.curiosity
                + impulse.warmth
                + intentions.get("need_for_exploration", 0.0) * 0.35
                + intentions.get("need_for_contact", 0.0) * 0.25
                - impulse.tension
                - intentions.get("need_for_protection", 0.0) * 0.20
            ),
            "intensity": impulse.intensity,
            "openness": max(0.0, impulse.curiosity + impulse.warmth + intentions.get("need_for_contact", 0.0) * 0.25 - impulse.tension),
            "compression": impulse.compression,
            "fluidity": impulse.fluidity,
            "directness": impulse.directness,
            "rupture": max(0.0, impulse.tension + intentions.get("need_for_protection", 0.0) * 0.35 - impulse.fluidity),
            "resolution": intentions.get("need_for_resolution", 0.0),
            "exploration": intentions.get("need_for_exploration", 0.0),
            "contact": intentions.get("need_for_contact", 0.0),
            "silence": intentions.get("need_for_silence", 0.0),
            "repair": intentions.get("need_for_repair", 0.0),
            "continuity": intentions.get("continuity", 0.0),
            "flow_need": intentions.get("flow_need", 0.0),
            "sentence_need": intentions.get("sentence_need", 0.0),
            "memory_depth": (getattr(impulse, "continuity_signature", {}) or {}).get("depth", 0.0),
            "rhythmic_gravity": (getattr(impulse, "continuity_signature", {}) or {}).get("rhythm", 0.5),
            "length_gravity": (getattr(impulse, "continuity_signature", {}) or {}).get("length_gravity", 0.5),
        }

    def _generate_linguistic_units_from_field(
        self,
        field,
        impulse,
    ):
        """
        Génère des noyaux linguistiques dynamiques.
        Aucun mot fixe émotion→mot.
        """

        concepts = []

        if impulse.dominant_text:
            concepts.append(impulse.dominant_text)

        concepts.extend(impulse.concepts)

        for source, target, relation_type in impulse.relations:
            if source:
                concepts.append(source)
            if target:
                concepts.append(target)

        # =========================
        # RÉINJECTION CONCEPTUELLE INTERNE
        # =========================

        # Correction finale : la mémoire interne ne doit pas réinjecter
        # des mots anciens dans la bouche sans cause actuelle.
        # Elle garde du poids interne, mais ne contamine pas la surface.
        internal_echoes = []

        clean = []
        seen = set()

        for c in concepts:
            c = str(c or "").strip()

            if not c:
                continue

            if c in seen:
                continue

            seen.add(c)
            clean.append(c)

        relation_graph = []

        for source, target, relation_type in impulse.relations:

            source = str(source or "").strip()
            target = str(target or "").strip()

            if not source or not target:
                continue

            source_weight = self._concept_dynamic_weight(
                source,
                impulse,
                field,
            )

            target_weight = self._concept_dynamic_weight(
                target,
                impulse,
                field,
            )

            source_memory = self.activation_memory[source]
            target_memory = self.activation_memory[target]

            source_weight += source_memory * 0.35
            target_weight += target_memory * 0.35

            relation_tension = abs(source_weight - target_weight)

            relation_key = f"{source}->{target}"

            previous_tension = self.unresolved_tensions[relation_key]

            relation_tension = (
                relation_tension * 0.7
                + previous_tension * 0.3
            )

            self.unresolved_tensions[relation_key] = (
                previous_tension * 0.94
                + relation_tension * 0.06
            )

            relation_graph.append({
                "source": source,
                "target": target,
                "relation": relation_type,
                "weight": source_weight + target_weight,
                "tension": relation_tension,
                "order": len(relation_graph),
                "surface_origin": "adjacent",
            })

        if not relation_graph:

            fallback = []

            for c in clean:
                fallback.append({
                    "source": c,
                    "target": "",
                    "relation": "isolated",
                    "weight": self._concept_dynamic_weight(
                        c,
                        impulse,
                        field,
                    ),
                    "tension": 0.0,
                    "order": len(fallback),
                    "surface_origin": "isolated",
                })

            relation_graph = fallback

        # =========================
        # AUTO-ÉMERGENCE RELATIONNELLE
        # =========================

        emergent_relations = []

        concept_list = list(clean)[:self.max_current_concepts]

        for i, c1 in enumerate(concept_list):

            for c2 in concept_list[i + 1:]:

                if c1 == c2:
                    continue

                similarity = self._latent_concept_resonance(
                    c1,
                    c2,
                    impulse,
                    field,
                )

                if similarity > 0.42:

                    emergent_relations.append({
                        "source": c1,
                        "target": c2,
                        "relation": "emergent",
                        "weight": similarity,
                        "tension": abs(len(c1) - len(c2)) * 0.03,
                        "order": len(concept_list) + len(emergent_relations),
                        "surface_origin": "emergent",
                    })

        relation_graph.extend(emergent_relations[:self.max_current_relations])
        relation_graph = relation_graph[: max(self.max_current_relations * 2, self.max_relation_units)]

        activation_pool = {}

        for node in relation_graph:

            source = node["source"]
            target = node["target"]

            source_energy = activation_pool.get(source, 0.0)
            target_energy = activation_pool.get(target, 0.0)

            propagated = (
                node["weight"] * 0.4
                + node["tension"] * 0.6
            )

            activation_pool[source] = (
                max(
                    0.0,
                    source_energy * 0.65
                    - abs(target_energy - source_energy) * 0.08
                )
                + propagated
            )

            activation_pool[target] = (
                max(
                    0.0,
                    target_energy * 0.65
                    - abs(target_energy - source_energy) * 0.08
                )
                + propagated * 0.85
            )

        for node in relation_graph:

            source = node["source"]
            target = node["target"]

            node["activation"] = (
                activation_pool.get(source, 0.0)
                + activation_pool.get(target, 0.0)
            ) * 0.5

            self.activation_memory[source] = (
                self.activation_memory[source] * 0.82
                + node["activation"] * 0.18
            )

            self.activation_memory[target] = (
                self.activation_memory[target] * 0.82
                + node["activation"] * 0.18
            )

        # =========================
        # COHÉRENCE COGNITIVE
        # =========================

        for node in relation_graph:

            source = node["source"]
            target = node["target"]

            gravity_source = self.cognitive_gravity[source]
            gravity_target = self.cognitive_gravity[target]

            coherence = (
                gravity_source * 0.5
                + gravity_target * 0.5
            )

            node["coherence"] = coherence

            self.coherence_field[source] = (
                self.coherence_field[source] * 0.96
                + coherence * 0.04
            )

            self.coherence_field[target] = (
                self.coherence_field[target] * 0.96
                + coherence * 0.04
            )

        relation_graph.sort(
            key=lambda x: (
                x["activation"] * 0.42
                + x["coherence"] * 0.28
                + x["weight"] * 0.20
                + x["tension"] * 0.10
            ),
            reverse=True,
        )

        for key in list(self.activation_memory.keys()):

            self.activation_memory[key] *= 0.965

            if self.activation_memory[key] < 0.01:
                del self.activation_memory[key]

        # =========================
        # MÉMOIRE CONCEPTUELLE VIVANTE
        # =========================

        for node in relation_graph:

            source = node["source"]
            target = node["target"]

            activation = node.get("activation", 0.0)

            self.internal_concept_field[source] = (
                self.internal_concept_field[source] * 0.94
                + activation * 0.06
            )

            self.internal_concept_field[target] = (
                self.internal_concept_field[target] * 0.94
                + activation * 0.06
            )

            gravity_gain = activation * 0.04

            self.cognitive_gravity[source] = (
                self.cognitive_gravity[source] * 0.985
                + gravity_gain
            )

            self.cognitive_gravity[target] = (
                self.cognitive_gravity[target] * 0.985
                + gravity_gain
            )

        for key in list(self.internal_concept_field.keys()):

            self.internal_concept_field[key] *= 0.992

            if self.internal_concept_field[key] < 0.02:
                del self.internal_concept_field[key]

        for key in list(self.cognitive_gravity.keys()):

            self.cognitive_gravity[key] *= 0.997

            if self.cognitive_gravity[key] < 0.01:
                del self.cognitive_gravity[key]

        for key in list(self.coherence_field.keys()):

            self.coherence_field[key] *= 0.994

            if self.coherence_field[key] < 0.01:
                del self.coherence_field[key]

        for key in list(self.unresolved_tensions.keys()):

            self.unresolved_tensions[key] *= 0.991

            if self.unresolved_tensions[key] < 0.015:
                del self.unresolved_tensions[key]

        return relation_graph[:self.max_relation_units]

    def _latent_concept_resonance(
        self,
        c1,
        c2,
        impulse,
        field,
    ):
        """
        Résonance latente entre concepts.
        Pas basée sur règles fixes.
        """

        if not c1 or not c2:
            return 0.0

        score = 0.0

        # Similarité structurelle
        common = len(set(c1) & set(c2))
        score += common * 0.04

        # Longueur proche
        score += 1.0 / (
            1.0 + abs(len(c1) - len(c2))
        )

        # Champ émotionnel
        score += impulse.intensity * 0.25

        # Ouverture
        score += field["openness"] * 0.15

        return score

    def _concept_dynamic_weight(
        self,
        concept: str,
        impulse: LivingImpulse,
        field: Dict[str, float],
    ) -> float:
        """
        Poids dynamique d’un concept.
        Remplace le random pur par une compétition interne.
        """

        if not concept:
            return 0.0

        score = 0.0

        score += len(str(concept)) * 0.03

        if concept == impulse.dominant_text:
            score += 1.0

        if concept in impulse.modifiers:
            score += 0.25

        score += field["intensity"] * 0.5
        score += field["rupture"] * 0.2
        score += field["openness"] * 0.15

        return score


    def _role_pressure_for_node(self, node, field, impulse):
        """Attribue un rôle organique sans mot ni phrase imposés."""
        activation = node.get("activation", 0.0)
        tension = node.get("tension", 0.0)
        coherence = node.get("coherence", 0.0)
        weight = node.get("weight", 0.0)
        order = node.get("order", 0)
        contact = field.get("contact", 0.0) + impulse.warmth * 0.35
        exploration = field.get("exploration", 0.0) + impulse.curiosity * 0.35
        resolution = field.get("resolution", 0.0) + impulse.directness * 0.20
        restraint = field.get("silence", 0.0) + impulse.doubt * 0.35 + impulse.compression * 0.25
        rupture = field.get("rupture", 0.0) + impulse.tension * 0.25
        return {
            "nucleus": activation * 0.38 + weight * 0.26 + coherence * 0.18 + (1.0 / (1.0 + order)) * 0.18,
            "approach": contact * 0.48 + coherence * 0.22 + activation * 0.18 - rupture * 0.16,
            "tension": rupture * 0.52 + tension * 0.32 + resolution * 0.16,
            "expansion": exploration * 0.50 + activation * 0.20 + max(0.0, 1.0 - impulse.compression) * 0.18,
            "restraint": restraint * 0.54 + impulse.compression * 0.28 + impulse.doubt * 0.18,
        }

    def _organize_units_with_internal_grammar(self, units, field, impulse) -> OrganicGrammarTrace:
        """Organisation organique V4.9 : rôles poreux, dominance fluctuante, pas de max brutal."""
        trace = OrganicGrammarTrace(
            pause=self._living_silence_pressure(field, impulse),
            compression=max(0.0, min(1.0, impulse.compression + field.get("silence", 0.0) * 0.35)),
        )
        if not units:
            if impulse.dominant_text:
                trace.nucleus.append(impulse.dominant_text)
            return trace

        role_buckets = {"nucleus": [], "approach": [], "tension": [], "expansion": [], "restraint": []}
        ordered_units = self._living_competition_order(units, field, impulse, limit=None)

        for unit_index, node in enumerate(ordered_units):
            scores = self._role_pressure_for_node(node, field, impulse)
            src = self._normalize_surface_token(node.get("source", ""))
            tgt = self._normalize_surface_token(node.get("target", ""))
            key_base = f"{src}:{tgt}"

            total_pressure = max(0.001, sum(max(0.0, score) for score in scores.values()))
            ranked_roles = sorted(
                scores.items(),
                key=lambda item: (
                    item[1]
                    + self.grammar_role_memory[f"{item[0]}:{key_base}"] * 0.06
                    + (((unit_index + len(item[0])) * 0.137 + self.expressive_time_phase) % 1.0 - 0.5) * 0.035
                ),
                reverse=True,
            )

            # Le rôle principal reçoit l'unité, mais un deuxième rôle peut garder
            # une trace faible si la pression est proche : la grammaire respire.
            for role_index, (role, score) in enumerate(ranked_roles[:2]):
                share = max(0.0, score) / total_pressure
                if role_index == 0 or share > 0.24:
                    role_buckets[role].append((score * (1.0 - role_index * 0.35), node))
                    mem_key = f"{role}:{key_base}"
                    self.grammar_role_memory[mem_key] = self.grammar_role_memory[mem_key] * 0.92 + score * 0.08

        def ordered_tokens(bucket_name, limit):
            bucket = role_buckets[bucket_name]
            bucket.sort(
                key=lambda pair: (
                    pair[0]
                    + pair[1].get("activation", 0.0) * 0.16
                    + field.get("living_temporality", 0.0) * 0.06
                    - pair[1].get("order", 0) * 0.015
                ),
                reverse=True,
            )
            out = []
            for _, node in bucket:
                for key in ("source", "target"):
                    tok = self._normalize_surface_token(node.get(key, ""))
                    if tok and (not out or tok != out[-1]):
                        out.append(tok)
                if len(out) >= limit:
                    break
            return out

        trace.nucleus = ordered_tokens("nucleus", 4)
        trace.approach = ordered_tokens("approach", 3)
        trace.tension = ordered_tokens("tension", 3)
        trace.expansion = ordered_tokens("expansion", 4)
        trace.restraint = ordered_tokens("restraint", 2)

        if impulse.dominant_text:
            dom = self._normalize_surface_token(impulse.dominant_text)
            if dom and dom not in trace.nucleus:
                # Le dominant n'écrase plus tout : il entre comme attracteur.
                insert_at = 0 if field.get("rupture", 0.0) > field.get("flow_need", 0.0) else min(1, len(trace.nucleus))
                trace.nucleus.insert(insert_at, dom)

        all_tokens = trace.nucleus + trace.approach + trace.tension + trace.expansion + trace.restraint
        total = max(1, len([t for t in all_tokens if t]))
        unique = len(set(t for t in all_tokens if t))
        trace.coherence = min(
            1.0,
            (unique / total) * 0.45
            + field.get("continuity", 0.0) * 0.18
            + impulse.fluidity * 0.16
            + field.get("living_temporality", 0.0) * 0.21,
        )
        trace.vitality = min(
            1.0,
            trace.coherence * 0.36
            + max(0.0, 1.0 - trace.compression) * 0.20
            + max(0.0, 1.0 - trace.pause) * 0.12
            + field.get("openness", 0.0) * 0.14
            + field.get("flow_need", 0.0) * 0.18,
        )
        pulse = f"n{len(trace.nucleus)}-a{len(trace.appearance) if hasattr(trace, 'appearance') else len(trace.approach)}-t{len(trace.tension)}-e{len(trace.expansion)}-r{len(trace.restraint)}"
        self.grammar_pulse_memory.append(pulse)
        self.last_full_living_trace = {
            "grammar_pulse": pulse,
            "coherence": round(trace.coherence, 3),
            "vitality": round(trace.vitality, 3),
            "pause": round(trace.pause, 3),
            "compression": round(trace.compression, 3),
            "v49_temporal": round(field.get("living_temporality", 0.0), 3),
        }
        self.living_quality_history.append(self.last_full_living_trace)
        return trace

    def _restore_living_concept_order(self, words, impulse):
        """Replace les concepts selon leur apparition actuelle quand la grammaire se casse."""
        order_map = {}
        for i, concept in enumerate(list(getattr(impulse, "concepts", []) or [])):
            tok = self._normalize_surface_token(concept)
            if tok and tok not in order_map:
                order_map[tok] = i
        if not order_map:
            return list(words or [])
        pauses = [(i, w) for i, w in enumerate(words or []) if w == "…"]
        lexical = [w for w in (words or []) if w != "…"]
        lexical.sort(key=lambda w: order_map.get(self._normalize_surface_token(w), 10_000))
        for idx, pause in pauses:
            if lexical and 0 < idx < len(lexical):
                lexical.insert(idx, pause)
        return lexical

    def _materialize_organic_grammar(self, trace: OrganicGrammarTrace, field, impulse) -> str:
        """Matérialise la grammaire organique sans phrase prête."""
        if trace.pause > 0.78:
            return self._materialize_silent_fragment(impulse)
        segments = []
        used = set()
        def add_many(tokens, max_count=None):
            count = 0
            for token in tokens:
                tok = self._normalize_surface_token(token)
                if not tok or tok in used:
                    continue
                segments.append(tok)
                used.add(tok)
                count += 1
                if max_count is not None and count >= max_count:
                    break
        add_many(trace.nucleus, 3)
        if field.get("contact", 0.0) > field.get("resolution", 0.0):
            add_many(trace.approach, 2)
        else:
            add_many(trace.tension, 2)
        if trace.pause > 0.48 and len(segments) > 1 and "…" not in segments:
            segments.insert(min(len(segments), 2), "…")
        if field.get("exploration", 0.0) > 0.38 and trace.compression < 0.65:
            add_many(trace.expansion, 2)
        if trace.compression > 0.55 or impulse.doubt > 0.55:
            add_many(trace.restraint, 1)
        if not segments:
            add_many([impulse.dominant_text] + list(impulse.concepts[:3]), 3)
        segments = self._restore_living_concept_order(segments, impulse)
        segments = self._stabilize_linguistic_flow(segments, impulse)
        segments = self._organic_breath_trim(segments, field, impulse)
        segments = self._restore_living_concept_order(segments, impulse)
        segments = self._prevent_hidden_template_surface(segments, impulse)
        return " ".join(segments)

    def _stabilize_continuous_sentence_trajectory(self, text, grammar, units, field, impulse) -> str:
        """
        V4.7 : transforme une juxtaposition de concepts en trajectoire.
        Aucun connecteur lexical n'est imposé : la continuité vient de l'ordre,
        des pauses, de la densité et de la mémoire de mouvement.
        """
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        seed = [self._normalize_surface_token(w) for w in getattr(impulse, "trajectory_seed", []) or []]
        seed = [w for w in seed if w]

        if not words:
            words = seed[:4]

        # Réinsère les concepts actuels importants si la surface est trop pauvre.
        lexical = [w for w in words if w != "…"]
        if len(lexical) < 3:
            for tok in seed:
                if tok not in words:
                    words.append(tok)
                if len([w for w in words if w != "…"]) >= 4:
                    break

        # Trajectoire relationnelle : privilégie les chaînes source→target actives.
        path = []
        for node in sorted(list(units or []), key=lambda n: (n.get("order", 0), -n.get("activation", 0.0))):
            src = self._normalize_surface_token(node.get("source", ""))
            tgt = self._normalize_surface_token(node.get("target", ""))
            for tok in (src, tgt):
                if tok and (not path or tok != path[-1]):
                    path.append(tok)
        if path:
            merged = []
            for tok in path + words:
                if tok and (not merged or tok != merged[-1]):
                    merged.append(tok)
            words = merged

        # Respiration : pauses seulement quand tension/doute le justifie.
        pause_pressure = (
            field.get("silence", 0.0) * 0.35
            + impulse.doubt * 0.25
            + impulse.tension * 0.18
            - field.get("flow_need", 0.0) * 0.20
        )
        if pause_pressure > 0.38 and "…" not in words and len(words) > 3:
            words.insert(max(1, min(len(words) - 1, int(len(words) * 0.55))), "…")
        elif pause_pressure < 0.18:
            words = [w for w in words if w != "…"]

        target = int(3 + field.get("sentence_need", 0.0) * 4 + field.get("flow_need", 0.0) * 3)
        target = max(3, min(10, target))
        if impulse.compression > 0.55 or impulse.tension > 0.70:
            target = min(target, 6)
        words = words[:target]

        signature = self._surface_fingerprint(words)
        self.syntax_trajectory_memory.append(signature)
        self.deep_continuity_memory.append({
            "signature": signature,
            "density": len([w for w in words if w != "…"]),
            "flow": round(field.get("flow_need", 0.0), 3),
            "sentence": round(field.get("sentence_need", 0.0), 3),
        })
        return " ".join(self._stabilize_linguistic_flow(words, impulse))

    def _repair_fragmented_relation_flow(self, text, grammar, units, field, impulse) -> str:
        """
        Répare les sorties qui ressemblent à des mots isolés. La réparation
        utilise uniquement les concepts et relations du tour actuel.
        """
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in str(text or "").split()]
        words = [w for w in words if w]
        lexical = [w for w in words if w != "…"]
        if not lexical:
            return "…"

        avg_len = sum(len(w) for w in lexical) / max(1, len(lexical))
        unique_ratio = len(set(lexical)) / max(1, len(lexical))
        fragment_score = 0.0
        fragment_score += 0.35 if len(lexical) <= 2 else 0.0
        fragment_score += 0.25 if avg_len <= 3.2 else 0.0
        fragment_score += 0.20 if unique_ratio < 0.75 else 0.0
        fragment_score += field.get("repair", 0.0) * 0.20

        if fragment_score < 0.34 and len(lexical) >= 3:
            return " ".join(words)

        candidates = []
        for group in (getattr(grammar, "nucleus", []), getattr(grammar, "approach", []), getattr(grammar, "tension", []), getattr(grammar, "expansion", [])):
            for token in group:
                tok = self._normalize_surface_token(token)
                if tok and tok not in candidates:
                    candidates.append(tok)
        for node in list(units or [])[:10]:
            for key in ("source", "target"):
                tok = self._normalize_surface_token(node.get(key, ""))
                if tok and tok not in candidates:
                    candidates.append(tok)
        for tok in getattr(impulse, "trajectory_seed", []) or []:
            tok = self._normalize_surface_token(tok)
            if tok and tok not in candidates:
                candidates.append(tok)

        if not candidates:
            return " ".join(words)

        target = 3 + int(max(0.0, 1.0 - impulse.compression) * 3)
        if field.get("silence", 0.0) > 0.52:
            target = min(target, 3)
        repaired = candidates[:max(3, min(7, target))]
        repaired = self._restore_living_concept_order(repaired, impulse)
        repaired = self._prevent_hidden_template_surface(repaired, impulse)
        self.fragment_repair_memory[self._surface_fingerprint(repaired)] += 1.0
        return " ".join(repaired)

    def _final_living_quality_gate(self, text, grammar, units, field, impulse) -> str:
        """Compatibilité V4.8 : conservée, mais devenue une modulation douce."""
        return self._soften_surface_control(text, grammar, units, field, impulse)

    def _shape_units_by_pressure(
        self,
        units,
        field,
        impulse,
    ):
        """
        Forme grammaticale finale.

        Correction finale :
        - interdit fusion de mots ;
        - interdit découpage aléatoire ;
        - interdit répétition morte ;
        - conserve l'émergence par ordre, tension, activation et mémoire.
        """

        if not units:
            return ""

        if self._living_silence_pressure(field, impulse) > 0.72:
            return self._materialize_silent_fragment(impulse)

        ordered = list(units)

        ordered.sort(
            key=lambda x: (
                x.get("activation", 0.0) * 0.38
                + x.get("coherence", 0.0) * 0.22
                + x.get("weight", 0.0) * 0.20
                + x.get("tension", 0.0) * 0.12
                + (1.0 / (1.0 + x.get("order", 0))) * 0.08
            ),
            reverse=True,
        )

        dynamic_flow = []
        for node in ordered:
            tension = node.get("tension", 0.0)
            coherence = node.get("coherence", 0.0)
            activation = node.get("activation", 0.0)
            flow_force = (
                activation * 0.45
                + coherence * 0.30
                + tension * 0.25
                + field.get("resolution", 0.0) * 0.08
                + field.get("exploration", 0.0) * 0.08
                + field.get("contact", 0.0) * 0.06
            )
            enriched = dict(node)
            enriched["flow_force"] = flow_force
            dynamic_flow.append(enriched)

        dynamic_flow.sort(
            key=lambda x: (
                x.get("flow_force", 0.0),
                x.get("activation", 0.0),
                x.get("tension", 0.0),
            ),
            reverse=True,
        )

        surface_instability = field.get("rupture", 0.0) * 0.4 + abs(self.drift_phase) * 0.18
        if surface_instability > 0.55:
            random.shuffle(dynamic_flow)

        words = self._materialize_relation_fragments(dynamic_flow, impulse)
        words = self._stabilize_linguistic_flow(words, impulse)
        words = self._organic_breath_trim(words, field, impulse)

        vitality = self._organic_vitality_score(words, field, impulse)
        if vitality.get("vitality", 0.0) < 0.38 and impulse.dominant_text:
            # Si la bouche devient trop pauvre, revenir au noyau actif, pas à une phrase.
            nucleus = [impulse.dominant_text] + [w for w in words if w != impulse.dominant_text]
            words = self._stabilize_linguistic_flow(nucleus, impulse)

        living_width = (
            field.get("contact", 0.0) * 2.2
            + field.get("exploration", 0.0) * 2.0
            + field.get("resolution", 0.0) * 1.2
            - field.get("silence", 0.0) * 2.8
            - impulse.compression * 2.2
        )
        max_len = max(2, int(5 + impulse.fluidity * 4 + living_width))
        if impulse.directness > 0.72 or impulse.tension > 0.55:
            max_len = min(max_len, 8)

        selected = words[:max_len]
        selected = self._prevent_hidden_template_surface(selected, impulse)
        return " ".join(selected)

    def _materialize_relation_fragments(
        self,
        relation_graph,
        impulse,
    ):
        """
        V4.5 : matérialisation organique.
        La surface respecte d'abord le flux adjacent réellement né du message,
        puis laisse les relations émergentes renforcer la sélection sans casser
        l'ordre naturel. Aucune phrase stockée n'est injectée.
        """

        if not relation_graph:
            return []

        adjacent = [
            n for n in relation_graph
            if n.get("surface_origin") in ("adjacent", "isolated")
        ]
        emergent = [n for n in relation_graph if n.get("surface_origin") == "emergent"]

        adjacent.sort(key=lambda n: n.get("order", 0))
        emergent.sort(
            key=lambda n: (n.get("activation", 0.0), n.get("weight", 0.0)),
            reverse=True,
        )

        fragments = []
        seen = set()

        def push(token):
            token = self._normalize_surface_token(token)
            if not token or token in seen:
                return
            fragments.append(token)
            seen.add(token)

        # 1) flux principal : ordre d'apparition et de relation.
        for node in adjacent:
            push(node.get("source", ""))
            push(node.get("target", ""))

        # 2) renfort émergent seulement si la bouche a besoin de largeur.
        organic_need = (
            impulse.curiosity * 0.35
            + impulse.warmth * 0.20
            + max(0.0, 1.0 - impulse.compression) * 0.18
            - impulse.tension * 0.12
        )
        if organic_need > 0.25:
            for node in emergent[:2]:
                push(node.get("source", ""))
                push(node.get("target", ""))

        # 3) hésitation organique : seulement une pause, jamais un texte prêt.
        if impulse.doubt > 0.66 and len(fragments) > 2:
            cut = max(1, min(len(fragments) - 1, int(len(fragments) * 0.55)))
            fragments.insert(cut, "…")

        return fragments

    def _stabilize_linguistic_flow(
        self,
        words,
        impulse,
    ):
        """
        Hygiène minimale V4.9.
        On évite seulement les sorties mortes/collées ; on ne gomme plus toute
        micro-répétition, car une bouche vivante peut hésiter ou reprendre.
        """
        clean = []
        immediate_repeat_budget = 1 if (impulse.tension + impulse.doubt) > 0.85 else 0

        for raw in words:
            word = self._normalize_surface_token(raw)
            if not word:
                continue
            if word != "…" and len(word) < 2:
                continue
            if word == "…" and (not clean or clean[-1] == "…"):
                continue

            if clean and word == clean[-1] and word != "…":
                if immediate_repeat_budget <= 0:
                    continue
                immediate_repeat_budget -= 1

            clean.append(word)

        if len([w for w in clean if w != "…"]) == 0 and impulse.dominant_text:
            clean.append(self._normalize_surface_token(impulse.dominant_text))

        return clean


    def _living_silence_pressure(self, field, impulse) -> float:
        """
        Mesure le besoin de retenue. Ce n'est pas une phrase préécrite :
        c'est la possibilité qu'une bouche vivante ne force pas une réponse longue.
        """
        pressure = (
            field.get("silence", 0.0) * 0.55
            + impulse.doubt * 0.22
            + impulse.compression * 0.18
            + max(0.0, impulse.tension - impulse.warmth) * 0.18
            - impulse.directness * 0.16
        )
        self.silence_tension_memory = self.silence_tension_memory * 0.86 + max(0.0, pressure) * 0.14
        return max(0.0, min(1.0, pressure + self.silence_tension_memory * 0.25))

    def _materialize_silent_fragment(self, impulse) -> str:
        """
        Produit un fragment minimal à partir du matériau actuel, jamais une phrase stockée.
        """
        material = []
        if impulse.dominant_text:
            material.append(impulse.dominant_text)
        material.extend(impulse.concepts[:3])
        clean = self._stabilize_linguistic_flow(material, impulse)
        if not clean:
            return "…"
        if impulse.doubt > 0.45:
            return "… " + " ".join(clean[:2])
        return " ".join(clean[:2])

    def _surface_fingerprint(self, words) -> str:
        """
        Empreinte de forme sans contenu exact : longueur, rythme, positions.
        Sert à détecter les templates cachés sans garder de phrases.
        """
        cleaned = [w for w in words if w and w != "…"]
        if not cleaned:
            return "silence"
        lengths = [len(w) for w in cleaned]
        bins = []
        for n in lengths[:8]:
            if n <= 3:
                bins.append("s")
            elif n <= 6:
                bins.append("m")
            else:
                bins.append("l")
        pause_count = sum(1 for w in words if w == "…")
        return f"{len(cleaned)}:{pause_count}:" + "".join(bins)

    def _prevent_hidden_template_surface(self, words, impulse):
        """
        Anti-template profond : si la même forme revient trop souvent,
        on ne remplace pas par une phrase fixe ; on compresse, pivote ou fragmente
        avec les concepts présents.
        """
        clean = list(words or [])
        fingerprint = self._surface_fingerprint(clean)
        repeated_shape = sum(1 for fp in self.surface_fingerprint_memory if fp == fingerprint)
        self.surface_fingerprint_memory.append(fingerprint)

        if repeated_shape < 2:
            return clean

        # Variation structurelle sans ajout lexical imposé.
        if len(clean) > 4:
            midpoint = max(1, len(clean) // 2)
            rotated = clean[midpoint:] + clean[:midpoint]
            return self._stabilize_linguistic_flow(rotated[:max(2, len(clean) - 1)], impulse)

        if impulse.dominant_text:
            material = [impulse.dominant_text] + [w for w in clean if w != impulse.dominant_text]
            return self._stabilize_linguistic_flow(material[:3], impulse)

        return clean[:max(1, len(clean) - 1)]

    def _organic_vitality_score(self, words, field, impulse) -> Dict[str, float]:
        """Mesure si la bouche est vivante sans juger par phrases stockées."""
        lexical = [w for w in words if w and w != "…"]
        if not lexical:
            return {"vitality": 0.0, "breath": 0.0, "coherence": 0.0, "novelty": 0.0}

        unique_ratio = len(set(lexical)) / max(1, len(lexical))
        length_balance = 1.0 - min(1.0, abs(len(lexical) - 5) / 7.0)
        continuity = min(1.0, field.get("continuity", 0.0) + 0.25)
        pressure_match = 1.0 - min(1.0, abs(len(lexical) - (3 + impulse.fluidity * 5)) / 8.0)

        fingerprint = self._surface_fingerprint(words)
        novelty = 1.0 - min(1.0, sum(1 for fp in self.organic_surface_memory if fp == fingerprint) / 3.0)

        vitality = (
            unique_ratio * 0.26
            + length_balance * 0.20
            + continuity * 0.18
            + pressure_match * 0.18
            + novelty * 0.18
        )

        score = {
            "vitality": round(max(0.0, min(1.0, vitality)), 3),
            "breath": round(length_balance, 3),
            "coherence": round((continuity + pressure_match) * 0.5, 3),
            "novelty": round(novelty, 3),
        }
        self.vitality_history.append(score)
        self.organic_surface_memory.append(fingerprint)
        return score

    def _organic_breath_trim(self, words, field, impulse):
        """
        Ajuste la longueur comme une respiration expressive : expansion, retenue,
        compression. Ne crée pas de contenu ; ne fait que doser le matériau né.
        """
        clean = self._stabilize_linguistic_flow(words, impulse)
        if not clean:
            return clean

        self.breath_phase = (
            self.breath_phase * 0.72
            + (field.get("exploration", 0.0) + field.get("contact", 0.0)) * 0.18
            - (field.get("silence", 0.0) + impulse.compression) * 0.10
        )
        self.breath_phase = max(-1.0, min(1.0, self.breath_phase))

        base = 4 + int(impulse.fluidity * 3)
        expansion = int(max(0.0, self.breath_phase) * 3)
        restraint = int(max(0.0, -self.breath_phase) * 2 + impulse.compression * 3 + impulse.tension * 1.5)
        target = max(2, min(10, base + expansion - restraint))

        if impulse.directness > 0.75:
            target = min(target, 7)
        if field.get("silence", 0.0) > 0.55:
            target = min(target, 3)

        return clean[:target]

    def _self_review_and_repair(self, text, units, field, impulse) -> str:
        """
        Relecture vivante de la bouche : détecte sortie morte, trop pauvre,
        trop répétitive, trop mécanique, puis répare par le matériau conceptuel.
        """
        original = str(text or "").strip()
        words = [self._normalize_surface_token(w) if w != "…" else "…" for w in original.split()]
        words = [w for w in words if w]

        lexical_words = [w for w in words if w != "…"]
        unique_ratio = len(set(lexical_words)) / max(1, len(lexical_words))
        density = len(lexical_words)
        pause_load = words.count("…") / max(1, len(words))
        form = self._surface_fingerprint(words)
        repeated_form = sum(1 for fp in self.surface_fingerprint_memory if fp == form)

        naturalness = 0.0
        naturalness += min(1.0, density / 5.0) * 0.28
        naturalness += unique_ratio * 0.28
        naturalness += max(0.0, 1.0 - pause_load * 2.5) * 0.16
        naturalness += max(0.0, 1.0 - repeated_form * 0.22) * 0.18
        naturalness += min(1.0, field.get("continuity", 0.0) + 0.35) * 0.10

        repair_need = max(0.0, 0.68 - naturalness) + field.get("repair", 0.0) * 0.18

        self.self_review_history.append({
            "naturalness": round(naturalness, 3),
            "repair_need": round(repair_need, 3),
            "density": density,
            "unique_ratio": round(unique_ratio, 3),
            "surface": form,
        })

        if repair_need <= 0.22 and lexical_words:
            return original

        # Réparer depuis les unités déjà nées, jamais depuis une phrase prête.
        candidates = []
        for node in list(units or [])[:8]:
            for key in ("source", "target"):
                token = self._normalize_surface_token(node.get(key, ""))
                if token and token not in candidates:
                    candidates.append(token)

        if impulse.dominant_text:
            dom = self._normalize_surface_token(impulse.dominant_text)
            if dom and dom not in candidates:
                candidates.insert(0, dom)

        for concept in impulse.concepts[:6]:
            token = self._normalize_surface_token(concept)
            if token and token not in candidates:
                candidates.append(token)

        candidates = self._stabilize_linguistic_flow(candidates, impulse)
        if not candidates:
            return "…"

        target_len = 3 + int(max(0.0, 1.0 - impulse.compression) * 4)
        if field.get("silence", 0.0) > 0.45:
            target_len = min(target_len, 3)

        repaired = candidates[:target_len]
        repaired = self._prevent_hidden_template_surface(repaired, impulse)
        return " ".join(repaired)

    def _normalize_surface_token(self, value: Any) -> str:
        token = str(value or "").strip().lower()
        token = re.sub(r"\s+", " ", token)
        token = re.sub(r"[^\wÀ-ÿ'’…-]+", "", token, flags=re.UNICODE)
        token = token.strip("-_'’ ")
        return token

    def _clean_living_text(self, text: str) -> str:
        """Nettoyage minimal : ne force pas une surface trop parfaite."""
        text = re.sub(r"\s+", " ", str(text or "")).strip()
        text = re.sub(r"(…\s*){3,}", "…", text)
        text = re.sub(r"\s+([.?!…])", r"\1", text)
        text = re.sub(r"([.?!]){3,}", r"\1", text)
        return text


    def _punctuate_living_text(self, text: str, impulse: LivingImpulse) -> str:
        """Ponctuation depuis pression interne, pas depuis phrase préécrite."""
        text = str(text or "").strip()
        if not text:
            return "…"
        text = re.sub(r"[.?!]+$", "", text).strip()
        if not text:
            return "…"
        if impulse.curiosity > 0.58 and impulse.tension < 0.72:
            return text + "?"
        if impulse.tension > 0.72 and impulse.directness > 0.65:
            return text + "."
        if impulse.doubt > 0.66 and impulse.directness < 0.55:
            return text + "…"
        return text + "."

    def _express_living_state(
        self,
        subject_unit,
        intent_unit,
        complement_unit,
        modifiers,
        reaction,
        emotional_state,
        pressure,
        conversational_memory=None,
    ):
        impulse = self._build_living_impulse(
            subject_unit,
            intent_unit,
            complement_unit,
            modifiers,
            reaction,
            emotional_state,
            pressure,
            conversational_memory,
        )

        return self._realize_living_impulse(impulse)
    
    def _apply_pressure(self, utterance: str, pressure: LinguisticPressureVector) -> str:
        """Appliquer pression de manière déterministe : pas de hasard de surface."""
        words = utterance.split()

        if len(words) > pressure.sentence_length:
            words = words[:pressure.sentence_length]

        pause_load = words.count("…") / max(1, len(words))
        if pressure.pause_probability > 0.24 and pause_load < 0.25 and len(words) > 2:
            idx = len(words) // 2
            words.insert(idx, "…")

        if pressure.hedge_rate > 0.30 and pause_load < 0.34 and len(words) > 3:
            idx = max(1, len(words) // 3)
            if words[idx] != "…":
                words.insert(idx, "…")

        return " ".join(words)
    
    def _adapt_to_continuation(
        self,
        utterance: str,
        conversational_memory: ConversationalMemory,
        pressure: LinguisticPressureVector,
    ) -> str:
        """Adapter à continuation conversationnelle."""
        rhythm = conversational_memory.context.conversation_rhythm
        
        # Rhythme rapide → pas de pauses
        if rhythm > 0.8:
            utterance = utterance.replace("…", "")
        
        # Rhythme lent → plus de pauses
        if rhythm < 0.3 and pressure.pause_probability < 0.3:
            words = utterance.split()
            if len(words) > 3:
                idx = len(words) // 2
                words.insert(idx, "…")
                utterance = " ".join(words)
        
        return utterance


# ==============================================================================
# ENGINE V4.2 STABLE
# ==============================================================================

class LivingExpressionEngineV42Stable:
    """Engine compositionnel stable."""
    
    def __init__(self):
        self.concept_extractor = ConceptExtractorStable()
        self.emotional_momentum = EmotionalMomentumStable()
        self.conversational_memory = ConversationalMemory()
        self.linguistic_pressure = LinguisticPressureStable()
        self.utterance_composer = ConceptualUtteranceComposerStable()
        
        self.composition_history = deque(maxlen=50)

    def _merge_azip_living_signals(
        self,
        reaction,
        immediate_experience=None,
        attention_focus=None,
        spontaneous_impulse=None,
        causal_memory=None,
        affective_memory=None,
        situated_presence=None,
        natural_initiative=None,
    ):
        def get(obj, name, default=0.0):
            if obj is None:
                return default
            if isinstance(obj, dict):
                return obj.get(name, default)
            return getattr(obj, name, default)

        reaction.tension += get(immediate_experience, "tension", 0.0) * 0.35
        reaction.warmth += get(immediate_experience, "warmth", 0.0) * 0.35
        reaction.curiosity += get(immediate_experience, "curiosity", 0.0) * 0.30
        reaction.doubt += get(immediate_experience, "doubt", 0.0) * 0.25

        reaction.tension += get(attention_focus, "focus_intensity", 0.0) * 0.15
        reaction.curiosity += get(attention_focus, "shift_magnitude", 0.0) * 0.20

        reaction.tension += get(spontaneous_impulse, "urgency", 0.0) * 0.25
        reaction.warmth += get(spontaneous_impulse, "approach", 0.0) * 0.20
        reaction.doubt += get(spontaneous_impulse, "hesitation", 0.0) * 0.20

        reaction.tension += get(causal_memory, "causal_weight", 0.0) * 0.20
        reaction.curiosity += get(causal_memory, "unresolved_weight", 0.0) * 0.20

        reaction.warmth += get(affective_memory, "positive_charge", 0.0) * 0.25
        reaction.tension += get(affective_memory, "negative_charge", 0.0) * 0.25

        presence = get(situated_presence, "presence", 0.0)
        reaction.warmth += presence * 0.15
        reaction.doubt *= max(0.4, 1.0 - presence * 0.35)

        reaction.curiosity += get(natural_initiative, "initiative_pressure", 0.0) * 0.20

        reaction.tension = max(0.0, min(1.0, reaction.tension))
        reaction.warmth = max(0.0, min(1.0, reaction.warmth))
        reaction.curiosity = max(0.0, min(1.0, reaction.curiosity))
        reaction.doubt = max(0.0, min(1.0, reaction.doubt))

        return reaction
    
    def _extract_external_surface_material(self, *sources) -> List[str]:
        """Lit les autres moteurs Azip sans reprendre leurs responsabilités."""
        material: List[str] = []

        def push(value):
            if value is None:
                return
            if isinstance(value, (list, tuple, set)):
                for item in value:
                    push(item)
                return
            if isinstance(value, dict):
                for key in (
                    "surface", "text", "token", "concept", "dominant", "dominant_text",
                    "primary_focus", "focus", "anchor", "anchors", "concepts",
                    "felt_meaning", "raw", "raw_impulse", "living_words",
                    "recent_atoms", "active_neurons", "unresolved_questions", "label", "keywords",
                ):
                    if key in value:
                        push(value.get(key))
                return
            for attr in (
                "surface", "text", "token", "concept", "dominant", "dominant_text",
                "primary_focus", "focus", "anchor", "anchors", "concepts",
                "felt_meaning", "raw", "raw_impulse", "living_words",
                "recent_atoms", "active_neurons", "unresolved_questions", "label", "keywords",
            ):
                if hasattr(value, attr):
                    push(getattr(value, attr))
            if isinstance(value, str):
                for tok in re.findall(r"[\wÀ-ÿ']+", value.lower(), flags=re.UNICODE):
                    tok = tok.strip("'’ ")
                    if tok and tok not in material:
                        material.append(tok)

        for source in sources:
            push(source)
        return material[:12]

    def _inject_external_material_into_reaction(self, reaction, external_words: List[str]):
        """Ajoute les surfaces fournies par attention/mémoire/impulsion comme concepts actifs."""
        if not external_words:
            return reaction
        existing = [c.text for c in reaction.concepts]
        base_index = len(reaction.concepts)
        added = []
        for offset, word in enumerate(external_words):
            if not word or word in existing:
                continue
            concept = Concept(
                text=word,
                type=ConceptType.ABSTRACT if len(word) > 6 else ConceptType.OBJECT,
                span=(base_index + offset, base_index + offset + 1),
                valence=0.0,
                intensity=0.62,
                confidence=0.66,
                semantic_field="external_azip",
            )
            reaction.concepts.append(concept)
            added.append(concept)
            existing.append(word)
        if added and reaction.dominant_concept is None:
            reaction.dominant_concept = added[0]
        if added and reaction.concepts:
            prev = reaction.concepts[0]
            for concept in added:
                reaction.relations.append(ConceptRelation(
                    source=prev,
                    target=concept,
                    relation_type=RelationType.COMPOSITION,
                    strength=0.48,
                    reason="azip external surface pressure",
                ))
                prev = concept
            reaction.curiosity = max(reaction.curiosity, min(1.0, 0.18 + 0.04 * len(added)))
        return reaction

    def express(
        self,
        message: str,
        thought_stance: ThoughtStance = ThoughtStance.HONEST,
        immediate_experience=None,
        attention_focus=None,
        spontaneous_impulse=None,
        causal_memory=None,
        affective_memory=None,
        situated_presence=None,
        natural_initiative=None,
        living_context=None,
        living_payload=None,
        expression_pressure=None,
        embodied_presence=None,
        mental_momentum=None,
        causal_graph=None,
        **extra_living_signals,
    ) -> Tuple[str, Dict[str, Any]]:
        """Pipeline complet V4.2 Stable.

        Cette signature accepte maintenant le paquet vivant complet envoyé par
        leia_living_core. Les signaux ne sont pas transformés en phrases fixes :
        ils deviennent seulement matière/pression pour le générateur de tokens.
        """
        deep_payload = living_payload if isinstance(living_payload, dict) else living_context
        if not isinstance(deep_payload, dict) and isinstance(immediate_experience, dict):
            deep_payload = immediate_experience
        if not isinstance(deep_payload, dict):
            deep_payload = {}
        self.utterance_composer._current_user_message = message or ""
        self.utterance_composer._current_living_payload = dict(deep_payload)
        self.utterance_composer._current_external_signals = {
            "attention_focus": attention_focus,
            "spontaneous_impulse": spontaneous_impulse,
            "causal_memory": causal_memory,
            "affective_memory": affective_memory,
            "situated_presence": situated_presence,
            "natural_initiative": natural_initiative,
            "expression_pressure": expression_pressure,
            "embodied_presence": embodied_presence,
            "mental_momentum": mental_momentum,
            "causal_graph": causal_graph,
            **extra_living_signals,
        }
        
        # 1. Extraire concepts
        reaction = self.concept_extractor.extract(message)
        
        reaction = self._merge_azip_living_signals(
            reaction=reaction,
            immediate_experience=immediate_experience,
            attention_focus=attention_focus,
            spontaneous_impulse=spontaneous_impulse,
            causal_memory=causal_memory,
            affective_memory=affective_memory,
            situated_presence=situated_presence,
            natural_initiative=natural_initiative,
        )
        external_words = self._extract_external_surface_material(
            self.utterance_composer._current_living_payload,
            self.utterance_composer._current_external_signals,
            immediate_experience,
            attention_focus,
            spontaneous_impulse,
            causal_memory,
            affective_memory,
            situated_presence,
            natural_initiative,
        )
        reaction = self._inject_external_material_into_reaction(reaction, external_words)

        # 2. Évoluer émotionnellement
        emotional_state = self.emotional_momentum.evolve(reaction)
        
        # 3. Calculer pression linguistique
        pressure = self.linguistic_pressure.compute(
            reaction,
            emotional_state,
            thought_stance,
            self.conversational_memory,
        )
        
        # 4. Composer utterance
        utterance = self.utterance_composer.compose(
            reaction,
            emotional_state,
            pressure,
            thought_stance,
            self.conversational_memory,
        )
        
        # 5. Mettre à jour mémoire conversationnelle
        self.conversational_memory.update(
            utterance,
            reaction.tension,
            reaction.warmth,
        )
        
        # 6. Tracer
        trace = {
            "utterance": utterance,
            "concepts": len(reaction.concepts),
            "dominant": reaction.dominant_concept.text if reaction.dominant_concept else None,
            "signal": reaction.dominant_signal,
            "emotion": {
                "tone": emotional_state.tone,
                "distance": round(emotional_state.distance, 2),
            },
            "pressure": {
                "length": pressure.sentence_length,
                "directness": round(pressure.directness, 2),
            },
            "self_review": (
                self.utterance_composer.self_review_history[-1]
                if self.utterance_composer.self_review_history else {}
            ),
            "organic_vitality": (
                self.utterance_composer.vitality_history[-1]
                if self.utterance_composer.vitality_history else {}
            ),
            "full_living_mouth": getattr(self.utterance_composer, "last_full_living_trace", {}),
            "prelanguage_v48": getattr(self.utterance_composer, "last_prelanguage_trace", {}),
            "continuity_v47": (
                self.utterance_composer.deep_continuity_memory[-1]
                if self.utterance_composer.deep_continuity_memory else {}
            ),
            "runtime_guard_v481": getattr(self.utterance_composer, "last_runtime_guard_trace", {}),
            "v49_living_autonomy": getattr(self.utterance_composer, "last_living_autonomy_trace", {}),
        }
        
        self.composition_history.append(trace)
        
        return utterance, trace


# ==============================================================================
# POINT D'ENTRÉE
# ==============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("LIVING EXPRESSION ENGINE V4.9 TRUE CONTINUOUS LIVING MOUTH")
    print("=" * 70)
    
    engine = LivingExpressionEngineV42Stable()
    
    test_messages = [
        "tu mens tu as du préécrit",
        "pourquoi tu fais ça ?",
        "je t'aime",
        "c'est vrai que tu es du code ?",
    ]
    
    for msg in test_messages:
        utterance, trace = engine.express(msg)
        print(f"\n> {msg}")
        print(f"< {utterance}")
        print(f"  Signal: {trace['signal']}, Tone: {trace['emotion']['tone']}")


# ==============================================================================
# PATCH V5.0 — BOUCHE CENTRALE CONNECTÉE AU PONT ÉTAT→LANGAGE
# ==============================================================================
# Cette extension n'ajoute pas de phrases complètes. Elle force la bouche centrale
# à recevoir le payload vivant complet et à déléguer la surface au générateur token.

def _v50_generate_living_expression(self, context=None, living_context=None, living_payload=None, user_input="", message="", **kwargs):
    payload = living_payload or living_context or context or {}
    if not isinstance(payload, dict):
        payload = {}
    user_message = str(user_input or message or payload.get("user_input", ""))
    try:
        from state_language_bridge import StateLanguageBridge
        from living_language_generator import LivingLanguageGenerator
        bridge = StateLanguageBridge.from_payload(payload)
        living_state = dict(bridge.as_living_state())
        for source_key in ("emotional_state", "internal_needs", "embodied_state", "presence", "attention", "relational_bond"):
            source = payload.get(source_key, {})
            if isinstance(source, dict):
                for k, v in source.items():
                    if isinstance(v, (int, float)):
                        living_state[str(k)] = max(float(living_state.get(str(k), 0.0) or 0.0), max(0.0, min(1.0, float(v))))
        memory = bridge.memory_atoms()
        for source_key in ("subjective_continuity", "mental_momentum", "causal_memory", "affective_memory", "thought_stream"):
            source = payload.get(source_key, {})
            if isinstance(source, dict):
                for k, v in list(source.items())[:12]:
                    if isinstance(v, (str, int, float, bool)):
                        memory.append({"source": source_key, "content": str(k), "weight": 0.42 if not isinstance(v, (int, float)) else max(0.08, min(1.0, float(v)))})

        # Pont livre -> bouche. Aucune phrase préécrite : seulement des unités
        # conceptuelles consolidées par la lecture, utilisables comme matière.
        book = payload.get("book_memory", {}) if isinstance(payload.get("book_memory", {}), dict) else {}
        book_tokens = []
        for token in list(book.get("axes", []) or []) + list(book.get("keywords", []) or []):
            text = str(token or "").strip().lower()
            if text and text not in book_tokens:
                book_tokens.append(text[:64])
                memory.append({"source": "book_memory", "content": text[:96], "weight": 0.72})
        causal_memory = []
        for rel in list(book.get("relations", []) or [])[:12]:
            if isinstance(rel, dict):
                src = str(rel.get("source", "")).strip().lower()
                tgt = str(rel.get("target", "")).strip().lower()
                typ = str(rel.get("type", "lié")).strip().lower()
                if src and tgt:
                    causal_memory.append({"source": src[:64], "target": tgt[:64], "relation": typ[:32], "weight": 0.64})
                    memory.append({"source": "book_relation", "content": f"{src}->{typ}->{tgt}", "weight": 0.64})
        raw_pressures = book.get("pressures", {}) if isinstance(book.get("pressures", {}), dict) else {}
        for k, v in raw_pressures.items():
            try:
                living_state[str(k)[:48]] = max(float(living_state.get(str(k)[:48], 0.0) or 0.0), max(0.0, min(1.0, float(v))))
            except Exception:
                pass

        impulses = list(dict.fromkeys(bridge.drives + book_tokens[:14] + [str(payload.get("dominant_living_axis", "")), str(payload.get("response_mode", ""))]))
        generator = getattr(self, "_v50_language_generator", None)
        if generator is None:
            generator = LivingLanguageGenerator()
            setattr(self, "_v50_language_generator", generator)
        result = generator.generate(
            user_message=user_message,
            living_state=living_state,
            self_memory=memory,
            active_impulses=[x for x in impulses if x],
            emotional_pressure=max(bridge.field_weights.values() or [0.0]) * 0.70,
            causal_memory=causal_memory,
            max_attempts=12,
            temperature=0.62,
            response_constraint={"prefer_focus_words": book_tokens[:12], "avoid_generic_only": True},
        )
        trace = dict(getattr(result, "meaning_trace", {}) or {})
        trace["v50_connected_mouth"] = True
        trace["book_memory_injected"] = bool(book_tokens or causal_memory)
        trace["book_focus_words"] = book_tokens[:12]
        trace["state_bridge"] = {"fields": bridge.field_weights, "rhythm": bridge.rhythm, "embodiment": bridge.embodiment, "drives": bridge.drives}
        return result.text, trace
    except Exception as exc:
        return "", {"v50_connected_mouth_error": f"{type(exc).__name__}:{exc}"}

try:
    LivingExpressionEngineV42Stable.generate_living_expression = _v50_generate_living_expression
except NameError:
    pass
try:
    LivingExpressionEngine = LivingExpressionEngineV42Stable
except NameError:
    pass


# ─────────────────────────────────────────────────────────────
# Added V7 lived continuity weighting
# ─────────────────────────────────────────────────────────────

def apply_lived_continuity_weight(
    lexical_weight: float,
    lived_state: dict | None = None,
) -> float:

    lived_state = lived_state or {}

    continuity = float(lived_state.get("lived_continuity", 0.0))
    unresolved = float(lived_state.get("unresolved_tension", 0.0))
    closeness = float(lived_state.get("relational_closeness", 0.0))

    multiplier = (
        1.0
        + continuity * 0.35
        + unresolved * 0.20
        + closeness * 0.15
    )

    return lexical_weight * multiplier
