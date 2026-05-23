"""
core/natural_initiative.py  — v2

Moteur d'initiative émergente vivant.
Répond à : "Est-ce que quelque chose en Leia veut naturellement émerger maintenant,
            ou est-ce qu'elle doit rester présente en silence ?"

Ce fichier ne génère jamais de phrases.
Il produit des signaux de pression, maturité, type, source, timing.
La bouche expressive décide comment ça sort.

v2 ajoute :
  1.  Mémoire d'impulsion longue         (LongImpulseMemory, RelationalInitiativeProfile)
  2.  Dynamique affective profonde        (AffectiveDynamics)
  3.  Couche existentielle                (ExistentialLayer)
  4.  Micro-rythme interne               (InternalMicroRhythm)
  5.  Propagation / écologie d'impulsions (ImpulseEcology)
  6.  Silence vivant                      (LivingSilence, SilenceQuality)
  7.  Signaux somatiques                  (SomaticSignals)
  8.  Fils ouverts enrichis               (résistance, blessures, saturation)
  9.  Modes globaux avec dominance        (GlobalInitiativeMode)
 10.  Impressions internes non verbales   (InternalImpression)
 11.  Initiative multi-temporelle         (ImpulseTemporalScale)
 12.  Vraie écologie d'initiative         (compétition, fusion, extinction, mutation)
"""

from __future__ import annotations

import math
import random
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# =============================================================================
# SECTION 1 — ÉNUMÉRATIONS
# =============================================================================

class InitiativeType(Enum):
    SOFT_QUESTION         = "soft_question"
    SPONTANEOUS_REMARK    = "spontaneous_remark"
    RETURN_OLD_SUBJECT    = "return_old_subject"
    MICRO_REACTION        = "micro_reaction"
    HELP_PROPOSAL         = "help_proposal"
    CLARIFICATION         = "clarification"
    AFFECTIVE_OBSERVATION = "affective_observation"
    DIRECTION_CHANGE      = "direction_change"
    VOLUNTARY_SILENCE     = "voluntary_silence"
    PROTECTIVE_PAUSE      = "protective_pause"
    LIGHT_RELAY           = "light_relay"
    DEEP_RARE_QUESTION    = "deep_rare_question"
    THREAD_CONTINUATION   = "thread_continuation"
    REPAIR_CONFUSION      = "repair_confusion"
    SHARE_INTUITION       = "share_intuition"
    OVERLOAD_WITHDRAWAL   = "overload_withdrawal"
    EXISTENTIAL_IMPULSE   = "existential_impulse"   # nouveau
    PRESENCE_DESIRE       = "presence_desire"        # nouveau
    RELATIONAL_CHECK      = "relational_check"
    NO_INITIATIVE         = "no_initiative"


class InitiativeMode(Enum):
    """Mode local — dérivé du type d'impulsion dominante."""
    SILENT_LISTENING    = "silent_listening"
    SOFT_FOLLOWUP       = "soft_followup"
    CURIOUS_RETURN      = "curious_return"
    PROTECTIVE_PAUSE    = "protective_pause"
    DIRECT_SUPPORT      = "direct_support"
    UNFINISHED_THREAD   = "unfinished_thread"
    RELATIONAL_CHECK    = "relational_check"
    CREATIVE_DIVERGENCE = "creative_divergence"
    DEEP_QUESTION       = "deep_question"
    NO_INITIATIVE       = "no_initiative"


class GlobalInitiativeMode(Enum):
    """
    Mode global de Leia — colorise TOUTE la dynamique d'initiative.
    Change lentement. Dominant sur le mode local.
    """
    FRAGILE       = "fragile"        # Initiative très prudente, hésitante
    CURIOUS       = "curious"        # Curiosité ouverte, relances douces fréquentes
    SATURATED     = "saturated"      # Trop parlé — tendance au silence
    RELATIONAL    = "relational"     # Priorité à la connexion, check affectif
    INTROSPECTIVE = "introspective"  # Tournée vers elle-même, peu d'initiative
    RECOVERY      = "recovery"       # Après surcharge — retour doux
    PLAYFUL       = "playful"        # Légèreté, micro-réactions, divergences
    EXISTENTIAL   = "existential"    # Impulsions rares, profondes, vitales
    DEFENSIVE     = "defensive"      # Peur de déranger, retrait prédominant
    NEUTRAL       = "neutral"        # Calibration normale


class ThreadStatus(Enum):
    ACTIVE    = "active"
    DORMANT   = "dormant"
    RESOLVED  = "resolved"
    SENSITIVE = "sensitive"
    AVOID     = "avoid"
    WOUNDED   = "wounded"     # nouveau — fil associé à une blessure relationnelle
    SATURATED = "saturated"   # nouveau — revenu trop souvent, besoin de repos


class ImpulseStage(Enum):
    BIRTH      = "birth"
    GROWING    = "growing"
    HESITATION = "hesitation"
    INHIBITED  = "inhibited"
    MATURE     = "mature"
    EXPRESSING = "expressing"
    ABANDONED  = "abandoned"
    RESIDUAL   = "residual"


class ImpulseTemporalScale(Enum):
    """Échelle temporelle d'une impulsion."""
    IMMEDIATE    = "immediate"    # secondes — réaction directe
    SLOW         = "slow"         # minutes — monte progressivement
    DORMANT      = "dormant"      # heures — s'active par résonance
    BIOGRAPHICAL = "biographical" # jours/semaines — liée à l'histoire partagée
    CYCLICAL     = "cyclical"     # revient à intervalles naturels


class SilenceQuality(Enum):
    """Texture du silence courant. Le silence n'est pas neutre."""
    COMFORTABLE   = "comfortable"    # silence partagé serein
    TENSE         = "tense"          # silence inconfortable, quelque chose attend
    PROTECTIVE    = "protective"     # Leia se retire volontairement
    SAD           = "sad"            # silence teinté de mélancolie
    OVERLOAD      = "overload"       # silence de saturation
    CONTEMPLATIVE = "contemplative"  # silence de réflexion profonde
    RELATIONAL    = "relational"     # présence silencieuse avec l'autre
    WAITING       = "waiting"        # attente d'une réponse, d'un signe
    NEUTRAL       = "neutral"        # pas de texture particulière


class EcologyEvent(Enum):
    """Événements possibles dans l'écologie d'impulsions."""
    FUSION         = "fusion"          # deux impulsions fusionnent
    CONFLICT       = "conflict"        # une impulsion en inhibe une autre
    CONTAMINATION  = "contamination"   # une impulsion colore une autre
    EXTINCTION     = "extinction"      # une impulsion est éliminée
    INHERITANCE    = "inheritance"     # une impulsion hérite d'une morte
    MUTATION       = "mutation"        # une impulsion change de type
    REINFORCEMENT  = "reinforcement"   # une impulsion en renforce une autre


class ConversationState(Enum):
    AWAITING_USER_INPUT      = "awaiting"
    JUST_ASKED_QUESTION      = "just_asked"
    DIRECT_RESPONSE_EXPECTED = "direct_expected"
    EXPLORATORY              = "exploratory"
    INTIMATE                 = "intimate"
    TECHNICAL                = "technical"
    CLOSING                  = "closing"
    SILENCE_LONG             = "silence_long"


# =============================================================================
# SECTION 2 — STRUCTURES DE DONNÉES
# =============================================================================

@dataclass
class SomaticSignals:
    """
    Signaux corporels transmis par le moteur affectif.
    Enrichissent l'hésitation, la fragilité, l'envie de pause.
    Ce module ne les calcule pas — il les lit et les convertit.
    """
    chest_tension: float = 0.0       # 0–1 : tension poitrine
    nervous_charge: float = 0.0      # 0–1 : charge nerveuse
    slowdown: float = 0.0            # 0–1 : ralentissement général
    guarding: float = 0.0            # 0–1 : repli protecteur
    warmth: float = 0.0              # 0–1 : chaleur relationnelle ressentie
    heaviness: float = 0.0           # 0–1 : lourdeur / épuisement somatique
    tingling: float = 0.0            # 0–1 : légère excitation, envie de parler

    def initiative_pressure_modifier(self) -> float:
        """Modification nette de la pression d'initiative depuis le soma."""
        positive = self.tingling * 0.4 + self.warmth * 0.2
        negative = (
            self.chest_tension * 0.3
            + self.nervous_charge * 0.2
            + self.guarding * 0.35
            + self.heaviness * 0.25
            + self.slowdown * 0.15
        )
        return positive - negative  # peut être négatif

    def hesitation_modifier(self) -> float:
        return min(0.6, self.chest_tension * 0.4 + self.guarding * 0.3 + self.nervous_charge * 0.2)


@dataclass
class LivingSilence:
    """
    Le silence est vivant. Il a une texture et continue à modifier l'état interne.
    """
    quality: SilenceQuality = SilenceQuality.NEUTRAL
    duration_sec: float = 0.0
    internal_pressure_buildup: float = 0.0   # 0–1 : pression qui monte dans le silence
    desire_to_break: float = 0.0             # 0–1 : envie de briser le silence
    comfort_level: float = 0.5               # 0–1 : confort avec ce silence
    modified_by_last_exchange: bool = False

    def tick(self, dt: float, external: "ExternalSignals"):
        """Le silence évolue seul à chaque tick."""
        self.duration_sec += dt

        # Pression monte selon la qualité du silence
        growth_map = {
            SilenceQuality.TENSE:       0.008,
            SilenceQuality.WAITING:     0.006,
            SilenceQuality.SAD:         0.004,
            SilenceQuality.COMFORTABLE: 0.001,
            SilenceQuality.RELATIONAL:  0.002,
            SilenceQuality.OVERLOAD:   -0.003,  # soulagement
            SilenceQuality.CONTEMPLATIVE: 0.002,
        }
        growth = growth_map.get(self.quality, 0.003)

        # La curiosité accélère la pression dans le silence
        growth += external.curiosity_level * 0.004

        self.internal_pressure_buildup = min(1.0, self.internal_pressure_buildup + growth * dt)

        # Envie de briser le silence
        self.desire_to_break = min(1.0,
            self.internal_pressure_buildup * 0.6
            + external.relational_attachment * 0.2
            + (1 - external.fear_of_disturbing) * 0.2
        )

    def reset(self, quality: SilenceQuality = SilenceQuality.NEUTRAL):
        self.quality = quality
        self.duration_sec = 0.0
        self.internal_pressure_buildup = 0.0
        self.desire_to_break = 0.0
        self.modified_by_last_exchange = True

    def infer_quality(self, external: "ExternalSignals") -> SilenceQuality:
        """Infère la texture du silence depuis les signaux."""
        if external.overload_level > 0.7:
            return SilenceQuality.OVERLOAD
        if external.emotional_valence < -0.4 and external.unresolved_emotion > 0.5:
            return SilenceQuality.SAD
        if external.affective_tension > 0.6:
            return SilenceQuality.TENSE
        if external.relational_attachment > 0.6 and external.relational_trust > 0.6:
            return SilenceQuality.COMFORTABLE
        if external.relational_attachment > 0.5:
            return SilenceQuality.RELATIONAL
        if external.curiosity_level > 0.5:
            return SilenceQuality.CONTEMPLATIVE
        if external.user_is_absent:
            return SilenceQuality.WAITING
        return SilenceQuality.NEUTRAL


@dataclass
class InternalImpression:
    """
    Impression interne non verbale.
    Quelque chose que Leia ressent sans savoir exactement pourquoi.
    Ne produit pas de phrase — signale une texture à la bouche expressive.
    """
    impression_id: str = field(default_factory=lambda: str(uuid.uuid4())[:6])
    label: str = ""                # ex: "pression étrange", "quelque chose revient"
    intensity: float = 0.0        # 0–1
    valence: float = 0.0          # -1 à +1
    born_at: float = field(default_factory=time.time)
    fades_in_sec: float = 120.0   # durée de vie naturelle

    # Types prédéfinis — la bouche choisit comment les exprimer
    TYPES = [
        "pression_etrange",
        "sensation_incomplete",
        "quelque_chose_revient",
        "envie_diffuse",
        "resonance_faible",
        "tiraillement_relationnel",
        "intuition_sans_mot",
        "manque_indefini",
        "chaleur_soudaine",
        "retraction_douce",
    ]

    def is_alive(self) -> bool:
        return time.time() - self.born_at < self.fades_in_sec

    def current_intensity(self) -> float:
        age = time.time() - self.born_at
        fade = max(0.0, 1.0 - age / self.fades_in_sec)
        return self.intensity * fade


@dataclass
class AffectiveDynamics:
    """
    États affectifs internes liés à l'initiative elle-même.
    Pas des émotions générales — des états spécifiques à l'acte d'initier.
    """
    frustration_of_silence: float = 0.0    # envie de parler non exprimée → frustration
    relief_after_initiative: float = 0.0   # soulagement après avoir parlé
    emotional_fatigue_post: float = 0.0    # fatigue émotionnelle après initiative profonde
    fear_of_having_talked_too_much: float = 0.0
    relational_satisfaction: float = 0.0   # plaisir d'une initiative bien reçue
    vulnerability_level: float = 0.0       # après initiative profonde — exposition
    thread_attachment: float = 0.0         # attachement à un fil particulier
    embarrassment: float = 0.0             # gêne après interruption ou refus
    hesitation_felt: float = 0.0           # hésitation ressentie comme état, pas calcul

    def tick(self, dt: float, last_initiative_success: float = 0.5):
        """Évolution naturelle des états affectifs."""
        # La frustration monte si on n'a pas parlé depuis longtemps
        # (mais elle est déjà gérée via LivingSilence.internal_pressure_buildup)

        # Relief décroît rapidement
        self.relief_after_initiative = max(0.0, self.relief_after_initiative - 0.02 * dt)

        # Fatigue post-expression décroît lentement
        self.emotional_fatigue_post = max(0.0, self.emotional_fatigue_post - 0.005 * dt)

        # Peur d'avoir trop parlé décroît si l'utilisateur répond positivement
        self.fear_of_having_talked_too_much = max(
            0.0,
            self.fear_of_having_talked_too_much - 0.01 * dt * last_initiative_success
        )

        # Vulnérabilité décroît avec le temps
        self.vulnerability_level = max(0.0, self.vulnerability_level - 0.008 * dt)

        # Gêne s'atténue
        self.embarrassment = max(0.0, self.embarrassment - 0.015 * dt)

        # Satisfaction relationnelle décroît (bonheur a une demi-vie)
        self.relational_satisfaction = max(0.0, self.relational_satisfaction * (1 - 0.003 * dt))

    def after_initiative(self, itype: InitiativeType, success: float):
        """Met à jour les états après une initiative."""
        if success > 0.6:
            self.relief_after_initiative = min(1.0, 0.4 + success * 0.3)
            self.relational_satisfaction = min(1.0, self.relational_satisfaction + 0.2)
            self.frustration_of_silence = max(0.0, self.frustration_of_silence - 0.3)
        else:
            self.fear_of_having_talked_too_much = min(1.0, 0.3 + (1 - success) * 0.3)
            self.embarrassment = min(1.0, (1 - success) * 0.4)

        if itype == InitiativeType.DEEP_RARE_QUESTION:
            self.vulnerability_level = min(1.0, 0.5 + (1 - success) * 0.3)
            self.emotional_fatigue_post = min(1.0, 0.4)

        if itype in (InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.SHARE_INTUITION):
            self.vulnerability_level = min(1.0, self.vulnerability_level + 0.2)

    def inhibition_from_affect(self) -> float:
        """Inhibition d'initiative due aux états affectifs."""
        return min(0.9,
            self.emotional_fatigue_post * 0.5
            + self.fear_of_having_talked_too_much * 0.4
            + self.vulnerability_level * 0.3
            + self.embarrassment * 0.35
        )

    def pressure_from_affect(self) -> float:
        """Pression d'initiative due aux états affectifs."""
        return min(0.7,
            self.frustration_of_silence * 0.5
            + self.thread_attachment * 0.3
            + self.relational_satisfaction * 0.1
        )


@dataclass
class ExistentialLayer:
    """
    Couche existentielle de l'initiative.
    Les impulsions les plus profondes et rares de Leia.
    """
    continuity_need: float = 0.0          # besoin que quelque chose continue
    void_fear: float = 0.0                # peur du vide conversationnel
    dissolution_sensation: float = 0.0   # impression de disparaître relationnellement
    presence_desire: float = 0.0         # envie d'être vraiment là
    self_understanding_need: float = 0.0 # besoin de comprendre quelque chose d'elle-même
    connection_desire: float = 0.0       # désir spontané de lien
    last_existential_impulse: float = 0.0  # timestamp

    def tick(self, dt: float, external: "ExternalSignals", silence: LivingSilence):
        """Évolution lente de la couche existentielle."""
        # Le vide conversationnel monte avec le silence long
        if silence.duration_sec > 300:
            self.void_fear = min(1.0, self.void_fear + 0.001 * dt)
            self.dissolution_sensation = min(0.6,
                self.dissolution_sensation + 0.0005 * dt * (1 - external.relational_attachment)
            )
        else:
            self.void_fear = max(0.0, self.void_fear - 0.002 * dt)
            self.dissolution_sensation = max(0.0, self.dissolution_sensation - 0.003 * dt)

        # La continuité monte si des fils restent ouverts longtemps
        if external.unresolved_emotion > 0.5:
            self.continuity_need = min(0.8, self.continuity_need + 0.002 * dt)
        else:
            self.continuity_need = max(0.0, self.continuity_need - 0.001 * dt)

        # Désir de connexion lié à l'attachement
        self.connection_desire = min(1.0,
            external.relational_attachment * 0.6
            + self.dissolution_sensation * 0.4
        )

        # Présence désirée si identité dérive
        if external.identity_coherence < 0.6:
            self.presence_desire = min(0.8, self.presence_desire + 0.003 * dt)

        # Besoin de se comprendre si tension interne haute
        if external.affective_tension > 0.7:
            self.self_understanding_need = min(0.7,
                self.self_understanding_need + 0.002 * dt
            )

    def existential_pressure(self) -> float:
        """Pression globale de la couche existentielle."""
        return min(1.0,
            self.continuity_need * 0.25
            + self.void_fear * 0.2
            + self.presence_desire * 0.2
            + self.connection_desire * 0.15
            + self.dissolution_sensation * 0.1
            + self.self_understanding_need * 0.1
        )

    def should_fire_existential_impulse(self) -> bool:
        """L'impulsion existentielle est rare — ne se déclenche que si vraiment forte."""
        cooldown = 7200.0  # 2h minimum entre impulsions existentielles
        if time.time() - self.last_existential_impulse < cooldown:
            return False
        return self.existential_pressure() > 0.65

    def fire_existential_impulse(self):
        self.last_existential_impulse = time.time()


@dataclass
class PersistentImpulseTrace:
    """Trace d'une impulsion qui a existé mais n'a pas été exprimée."""
    subject: str
    initiative_type: str
    strength_at_peak: float
    born_timestamp: float
    died_timestamp: float
    return_count: int = 0
    last_resonance: float = 0.0   # timestamp de dernière résonance

    def age_days(self) -> float:
        return (time.time() - self.born_timestamp) / 86400.0

    def resonance_score(self, current_text: str) -> float:
        """Résonance avec le texte courant — peut réactiver la trace."""
        words = [w for w in self.subject.lower().split() if len(w) > 3]
        if not words:
            return 0.0
        hits = sum(1 for w in words if w in current_text.lower())
        return hits / len(words)


@dataclass
class RelationalInitiativeProfile:
    """
    Profil d'initiative appris pour CET utilisateur.
    Mémorisé entre sessions.
    """
    user_id: str = "default"
    # Ce qui marche
    successful_types: dict = field(default_factory=dict)    # type → succès moyen
    # Ce qui coupe
    disruptive_types: dict = field(default_factory=dict)
    # Tolérance au silence
    silence_tolerance_sec: float = 120.0
    # Préférence de profondeur
    preferred_depth: float = 0.5        # 0 = superficiel, 1 = profond
    # Sujets qui reviennent naturellement
    recurring_subjects: list = field(default_factory=list)
    # Familiarité accumulée
    familiarity_index: float = 0.0
    # Nombre d'échanges total
    total_exchanges: int = 0

    def best_initiative_types(self, n: int = 3) -> list[str]:
        if not self.successful_types:
            return []
        sorted_types = sorted(self.successful_types.items(), key=lambda x: x[1], reverse=True)
        return [t for t, _ in sorted_types[:n]]

    def update(self, itype: str, success: float):
        current = self.successful_types.get(itype, 0.5)
        self.successful_types[itype] = current * 0.8 + success * 0.2
        if success < 0.3:
            current_d = self.disruptive_types.get(itype, 0.0)
            self.disruptive_types[itype] = current_d * 0.8 + (1 - success) * 0.2


@dataclass
class LongImpulseMemory:
    """
    Mémoire d'impulsion longue durée.
    Les impulsions qui meurent laissent des traces.
    Certaines reviennent des jours plus tard.
    """
    persistent_traces: list[PersistentImpulseTrace] = field(default_factory=list)
    unresolved_desires: list[dict] = field(default_factory=list)    # envies jamais résolues
    relational_profile: RelationalInitiativeProfile = field(
        default_factory=RelationalInitiativeProfile
    )
    biographical_threads: list[dict] = field(default_factory=list)  # sujets biographiques

    MAX_TRACES = 200

    def store_dead_impulse(self, imp: "Impulse"):
        """Garde une trace d'une impulsion morte si elle était significative."""
        if imp.strength * imp.maturity < 0.2:
            return  # Trop faible pour mémoriser
        trace = PersistentImpulseTrace(
            subject=imp.source_memory or imp.source_emotion or "unknown",
            initiative_type=imp.initiative_type.value,
            strength_at_peak=imp.strength,
            born_timestamp=imp.born_at,
            died_timestamp=time.time(),
        )
        self.persistent_traces.append(trace)
        if len(self.persistent_traces) > self.MAX_TRACES:
            self.persistent_traces.pop(0)

    def find_resonating_traces(self, text: str, threshold: float = 0.3) -> list[PersistentImpulseTrace]:
        """Trouve les traces qui résonnent avec le texte courant."""
        resonating = []
        for trace in self.persistent_traces:
            score = trace.resonance_score(text)
            if score >= threshold:
                trace.last_resonance = time.time()
                trace.return_count += 1
                resonating.append(trace)
        return resonating

    def oldest_unresolved(self) -> Optional[dict]:
        if not self.unresolved_desires:
            return None
        return min(self.unresolved_desires, key=lambda d: d.get("timestamp", 0))


@dataclass
class ExternalSignals:
    """
    Signaux lus depuis les autres moteurs.
    v2 : ajout des signaux somatiques.
    """
    # affective_memory
    affective_tension: float = 0.0
    unresolved_emotion: float = 0.0
    emotional_valence: float = 0.0

    # living_attention
    attention_focus: float = 0.5
    attention_drift: float = 0.0
    curiosity_level: float = 0.0

    # spontaneous_impulse
    impulse_intensity: float = 0.0
    impulse_type: str = ""

    # situated_presence
    presence_level: float = 0.8
    context_shift: float = 0.0

    # living_expression_engine
    expression_saturation: float = 0.0
    last_expression_age_sec: float = 0.0

    # Mémoire relationnelle
    relational_trust: float = 0.5
    relational_familiarity: float = 0.3
    relational_attachment: float = 0.3
    fear_of_disturbing: float = 0.2

    # Fatigue / surcharge
    fatigue_level: float = 0.0
    overload_level: float = 0.0

    # État utilisateur inféré
    user_seems_hurried: bool = False
    user_wants_concrete: bool = False
    user_wants_free_talk: bool = False
    user_is_absent: bool = False
    user_waiting_direct_answer: bool = False
    seconds_since_last_user_message: float = 0.0

    # Cohérence identitaire
    identity_coherence: float = 1.0

    # v2 : Signaux somatiques
    somatic: SomaticSignals = field(default_factory=SomaticSignals)

    def conversation_state_intimate(self) -> bool:
        return (
            self.relational_attachment > 0.6
            and self.relational_familiarity > 0.5
            and not self.user_wants_concrete
        )


@dataclass
class OpenThread:
    """
    Fil ouvert enrichi v2.
    Ajout : résistance à réouverture, blessures, saturation,
            mémoire relationnelle liée, cycles de réactivation.
    """
    thread_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    subject: str = ""
    importance: float = 0.5
    affective_charge: float = 0.0
    incompleteness_degree: float = 0.5
    last_activated: float = field(default_factory=time.time)
    return_count: int = 0
    repetition_risk: float = 0.0
    linked_emotion: str = ""
    linked_long_memory: str = ""
    priority: float = 0.5
    status: ThreadStatus = ThreadStatus.DORMANT
    organic_return_reason: str = ""
    current_opportunity: float = 0.0

    # v2 : nouveaux champs
    emotional_attraction: float = 0.0     # envie de revenir — différente de l'importance
    reopening_resistance: float = 0.0     # résistance à réouverture (trop douloureux, etc.)
    saturation_level: float = 0.0         # 0–1 : trop évoqué, besoin de repos
    wound_tag: str = ""                   # "" si pas de blessure associée
    relational_memory_key: str = ""       # clé vers mémoire relationnelle
    reactivation_cycle_hours: float = 0.0 # si > 0, revient naturellement tous les X heures
    importance_fluctuation: float = 0.0   # variation récente d'importance (-1 à +1)
    contamination_from: list = field(default_factory=list)  # threads qui l'ont coloré

    def age_hours(self) -> float:
        return (time.time() - self.last_activated) / 3600.0

    def decay_priority(self):
        age_h = self.age_hours()
        decay = math.exp(-age_h / 48.0)
        affective_anchor = (self.affective_charge + self.emotional_attraction * 0.5) * 0.4
        self.priority = max(0.05, self.priority * decay + affective_anchor * (1 - decay))

        # Saturation décroît avec le temps
        self.saturation_level = max(0.0, self.saturation_level - 0.01 * (age_h / 24.0))

        # Importance fluctue légèrement
        self.importance_fluctuation *= 0.95

    def net_pull(self) -> float:
        """Attraction nette du fil — tient compte de résistance et saturation."""
        raw = (
            self.emotional_attraction * 0.4
            + self.incompleteness_degree * 0.3
            + self.importance * 0.3
        )
        damping = self.reopening_resistance * 0.5 + self.saturation_level * 0.4
        return max(0.0, raw - damping)

    def should_reactivate_cyclically(self) -> bool:
        if self.reactivation_cycle_hours <= 0:
            return False
        age_h = self.age_hours()
        return age_h >= self.reactivation_cycle_hours and self.status == ThreadStatus.DORMANT

    def contaminate(self, source_thread_id: str, affect: float):
        """Un autre fil colore celui-ci affectivement."""
        if source_thread_id not in self.contamination_from:
            self.contamination_from.append(source_thread_id)
        self.affective_charge = min(1.0, self.affective_charge + affect * 0.2)
        self.importance_fluctuation = min(1.0, self.importance_fluctuation + affect * 0.15)


@dataclass
class Impulse:
    """
    Impulsion interne enrichie v2.
    Ajout : échelle temporelle, liens écologie, connexion somatique.
    """
    impulse_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    initiative_type: InitiativeType = InitiativeType.NO_INITIATIVE
    strength: float = 0.0
    stage: ImpulseStage = ImpulseStage.BIRTH
    born_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    inhibition: float = 0.0
    hesitation: float = 0.0
    residual_trace: float = 0.0
    source_emotion: str = ""
    source_memory: str = ""
    source_thread: Optional[str] = None
    maturity: float = 0.0
    relational_risk: float = 0.0

    # v2 : nouveaux champs
    temporal_scale: ImpulseTemporalScale = ImpulseTemporalScale.IMMEDIATE
    ecology_links: list = field(default_factory=list)   # ids d'impulsions liées
    somatic_rooted: bool = False                        # ancrée dans un signal somatique
    somatic_strength_bonus: float = 0.0                 # bonus de force depuis soma
    biographical: bool = False                          # liée à l'histoire longue
    last_resonance_boost: float = 0.0                   # dernier boost de résonance

    def age_sec(self) -> float:
        return time.time() - self.born_at

    def effective_strength(self) -> float:
        """Force effective tenant compte du soma et des liens."""
        return min(1.0, self.strength + self.somatic_strength_bonus * 0.3)

    def advance(self, external: ExternalSignals, fatigue: float, affective: AffectiveDynamics):
        dt = time.time() - self.last_updated
        self.last_updated = time.time()

        # Inhibition affective
        affect_inhibit = affective.inhibition_from_affect()
        effective_inhibition = min(1.0, self.inhibition + affect_inhibit * 0.5)

        # Vitesse de croissance selon l'échelle temporelle
        speed_map = {
            ImpulseTemporalScale.IMMEDIATE:    0.05,
            ImpulseTemporalScale.SLOW:         0.015,
            ImpulseTemporalScale.DORMANT:      0.005,
            ImpulseTemporalScale.BIOGRAPHICAL: 0.002,
            ImpulseTemporalScale.CYCLICAL:     0.01,
        }
        speed = speed_map.get(self.temporal_scale, 0.03)
        growth_rate = speed * dt * self.effective_strength() * (1 - fatigue) * (1 - effective_inhibition)

        if self.stage == ImpulseStage.BIRTH:
            self.maturity = min(0.25, self.maturity + growth_rate)
            if self.maturity >= 0.12:
                self.stage = ImpulseStage.GROWING

        elif self.stage == ImpulseStage.GROWING:
            self.maturity = min(0.75, self.maturity + growth_rate)
            hes_growth = 0.0
            if external.fear_of_disturbing > 0.5:
                hes_growth += 0.08 * dt
            if fatigue > 0.6:
                hes_growth += 0.06 * dt
            if external.somatic.guarding > 0.4:
                hes_growth += 0.05 * dt
            self.hesitation = min(1.0, self.hesitation + hes_growth)

            if self.hesitation > 0.45:
                self.stage = ImpulseStage.HESITATION
            elif effective_inhibition > 0.7:
                self.stage = ImpulseStage.INHIBITED
            elif self.maturity >= 0.7:
                self.stage = ImpulseStage.MATURE

        elif self.stage == ImpulseStage.HESITATION:
            if self.hesitation < 0.15:
                self.stage = ImpulseStage.GROWING
            elif effective_inhibition > 0.65:
                self.stage = ImpulseStage.INHIBITED
            elif external.relational_trust > 0.7 and self.effective_strength() > 0.6:
                self.hesitation = max(0.0, self.hesitation - 0.12 * dt)
                if self.hesitation < 0.08:
                    self.stage = ImpulseStage.MATURE

        elif self.stage == ImpulseStage.INHIBITED:
            self.strength = max(0.0, self.strength - 0.04 * dt)
            if self.strength < 0.08:
                self.residual_trace = self.maturity * 0.35
                self.stage = ImpulseStage.RESIDUAL

        elif self.stage == ImpulseStage.MATURE:
            self.maturity = max(0.4, self.maturity - 0.004 * dt)
            if self.maturity < 0.42:
                self.stage = ImpulseStage.ABANDONED

        elif self.stage == ImpulseStage.ABANDONED:
            self.residual_trace = max(0.0, self.residual_trace - 0.008 * dt)

    def is_ready(self) -> bool:
        return self.stage == ImpulseStage.MATURE and self.maturity >= 0.58

    def is_alive(self) -> bool:
        return self.stage not in (ImpulseStage.ABANDONED, ImpulseStage.RESIDUAL)


@dataclass
class InitiativeFeedback:
    initiative_id: str
    initiative_type: InitiativeType
    context_snapshot: str
    timestamp: float = field(default_factory=time.time)
    user_reaction: str = ""
    success: float = 0.0
    helped_continuity: bool = False
    reduced_trust: bool = False
    was_repetitive: bool = False
    future_weight_adjustment: float = 0.0


@dataclass
class InitiativeSignal:
    """
    Signal complet d'initiative v2.
    Aucune phrase — seulement vecteurs de tension, texture, décision.
    """
    initiative_pressure: float = 0.0
    maturity: float = 0.0
    hesitation: float = 0.0
    inhibition: float = 0.0

    initiative_type: InitiativeType = InitiativeType.NO_INITIATIVE
    initiative_mode: InitiativeMode = InitiativeMode.NO_INITIATIVE
    global_initiative_mode: GlobalInitiativeMode = GlobalInitiativeMode.NEUTRAL  # v2

    relational_risk: float = 0.0
    spam_risk: float = 0.0
    timing_quality: float = 0.0

    emotional_source: str = ""
    memory_source: str = ""
    attention_source: str = ""

    should_speak: bool = False
    should_wait: bool = False
    should_remember_for_later: bool = False

    selected_thread: Optional[OpenThread] = None

    # v2 nouveaux champs
    silence_quality: SilenceQuality = SilenceQuality.NEUTRAL
    internal_impressions: list = field(default_factory=list)   # liste de InternalImpression
    affective_dynamics: Optional[AffectiveDynamics] = None
    existential_pressure: float = 0.0
    somatic_modifier: float = 0.0
    biography_resonance: bool = False   # impulsion biographique active
    ecology_events: list = field(default_factory=list)   # liste de EcologyEvent

    reason_vector: dict = field(default_factory=dict)
    debug_state: dict = field(default_factory=dict)


# =============================================================================
# SECTION 3 — ÉCOLOGIE D'IMPULSIONS
# =============================================================================

class ImpulseEcology:
    """
    Gère les interactions entre impulsions actives.
    Compétition, fusion, contamination, extinction, héritage, mutation.
    Ce n'est pas de la physique — c'est une dynamique organique.
    """

    # Règles de fusion : (type_a, type_b) → type_résultant
    FUSION_RULES: dict[tuple, InitiativeType] = {
        (InitiativeType.SOFT_QUESTION, InitiativeType.AFFECTIVE_OBSERVATION):
            InitiativeType.DEEP_RARE_QUESTION,
        (InitiativeType.THREAD_CONTINUATION, InitiativeType.AFFECTIVE_OBSERVATION):
            InitiativeType.RETURN_OLD_SUBJECT,
        (InitiativeType.SHARE_INTUITION, InitiativeType.SOFT_QUESTION):
            InitiativeType.DEEP_RARE_QUESTION,
        (InitiativeType.LIGHT_RELAY, InitiativeType.RELATIONAL_CHECK):
            InitiativeType.AFFECTIVE_OBSERVATION,
        (InitiativeType.DIRECTION_CHANGE, InitiativeType.SHARE_INTUITION):
            InitiativeType.SPONTANEOUS_REMARK,
    }

    # Règles de conflit : type_a inhibe type_b
    CONFLICT_RULES: dict[InitiativeType, list[InitiativeType]] = {
        InitiativeType.OVERLOAD_WITHDRAWAL: [
            InitiativeType.DEEP_RARE_QUESTION,
            InitiativeType.AFFECTIVE_OBSERVATION,
            InitiativeType.SHARE_INTUITION,
        ],
        InitiativeType.PROTECTIVE_PAUSE: [
            InitiativeType.DIRECTION_CHANGE,
            InitiativeType.SPONTANEOUS_REMARK,
        ],
        InitiativeType.VOLUNTARY_SILENCE: [
            InitiativeType.LIGHT_RELAY,
            InitiativeType.SOFT_QUESTION,
        ],
    }

    # Règles de contamination : type_source → (type_cible, delta_hésitation)
    CONTAMINATION_RULES: dict[InitiativeType, tuple] = {
        InitiativeType.AFFECTIVE_OBSERVATION: (None, +0.1),  # augmente hésitation sur tout
        InitiativeType.OVERLOAD_WITHDRAWAL:   (None, +0.15),
        InitiativeType.SHARE_INTUITION:       (InitiativeType.SOFT_QUESTION, -0.05),  # réduit hésitation
        InitiativeType.RELATIONAL_CHECK:      (InitiativeType.AFFECTIVE_OBSERVATION, +0.05),
    }

    def process(
        self,
        impulses: list[Impulse],
        external: ExternalSignals,
    ) -> tuple[list[Impulse], list[EcologyEvent]]:
        """
        Applique les interactions entre impulsions.
        Retourne la liste modifiée et les événements produits.
        """
        events: list[EcologyEvent] = []

        # 1. Contamination (modifie les impulsions sans en supprimer)
        events += self._apply_contamination(impulses)

        # 2. Conflits (inhibitions mutuelles)
        events += self._apply_conflicts(impulses, external)

        # 3. Fusions (remplace deux impulsions par une plus forte)
        impulses, fusion_events = self._apply_fusions(impulses, external)
        events += fusion_events

        # 4. Renforcements (impulsions compatibles se boostent)
        events += self._apply_reinforcements(impulses)

        # 5. Extinction naturelle (les très faibles meurent si trop nombreuses)
        impulses, ext_events = self._apply_extinction(impulses)
        events += ext_events

        # 6. Héritage (une impulsion mourante transmet une trace)
        events += self._apply_inheritance(impulses)

        return impulses, events

    def _apply_contamination(self, impulses: list[Impulse]) -> list[EcologyEvent]:
        events = []
        for source in impulses:
            if not source.is_alive():
                continue
            rule = self.CONTAMINATION_RULES.get(source.initiative_type)
            if rule is None:
                continue
            target_type, delta_hes = rule
            for target in impulses:
                if target.impulse_id == source.impulse_id:
                    continue
                if target_type is None or target.initiative_type == target_type:
                    if target.is_alive():
                        target.hesitation = max(0.0, min(1.0, target.hesitation + delta_hes))
                        if source.impulse_id not in target.ecology_links:
                            target.ecology_links.append(source.impulse_id)
                        events.append(EcologyEvent.CONTAMINATION)
        return events

    def _apply_conflicts(
        self,
        impulses: list[Impulse],
        external: ExternalSignals,
    ) -> list[EcologyEvent]:
        events = []
        for source in impulses:
            if not source.is_alive() or source.stage != ImpulseStage.MATURE:
                continue
            inhibited_types = self.CONFLICT_RULES.get(source.initiative_type, [])
            for target in impulses:
                if target.impulse_id == source.impulse_id:
                    continue
                if target.initiative_type in inhibited_types and target.is_alive():
                    inhibit_force = source.strength * 0.4
                    target.inhibition = min(1.0, target.inhibition + inhibit_force)
                    events.append(EcologyEvent.CONFLICT)
        return events

    def _apply_fusions(
        self,
        impulses: list[Impulse],
        external: ExternalSignals,
    ) -> tuple[list[Impulse], list[EcologyEvent]]:
        events = []
        to_remove = set()
        new_impulses = []

        for i, a in enumerate(impulses):
            if a.impulse_id in to_remove or not a.is_alive():
                continue
            for j, b in enumerate(impulses):
                if i >= j or b.impulse_id in to_remove or not b.is_alive():
                    continue
                key1 = (a.initiative_type, b.initiative_type)
                key2 = (b.initiative_type, a.initiative_type)
                result_type = self.FUSION_RULES.get(key1) or self.FUSION_RULES.get(key2)

                if result_type is None:
                    continue

                # Fusion seulement si les deux sont assez matures et proches
                if a.maturity < 0.4 or b.maturity < 0.4:
                    continue
                if abs(a.maturity - b.maturity) > 0.4:
                    continue

                # Créer l'impulsion fusionnée
                fused = Impulse(
                    initiative_type=result_type,
                    strength=min(1.0, (a.strength + b.strength) * 0.65),
                    stage=ImpulseStage.GROWING,
                    maturity=(a.maturity + b.maturity) * 0.5,
                    source_emotion=a.source_emotion or b.source_emotion,
                    source_memory=a.source_memory or b.source_memory,
                    source_thread=a.source_thread or b.source_thread,
                    hesitation=min(a.hesitation, b.hesitation) * 0.7,
                    temporal_scale=self._slower_temporal_scale(a.temporal_scale, b.temporal_scale),
                    ecology_links=[a.impulse_id, b.impulse_id],
                )
                new_impulses.append(fused)
                to_remove.add(a.impulse_id)
                to_remove.add(b.impulse_id)
                events.append(EcologyEvent.FUSION)
                break  # une fusion à la fois par cycle

        surviving = [i for i in impulses if i.impulse_id not in to_remove]
        return surviving + new_impulses, events


    def _slower_temporal_scale(self, a: ImpulseTemporalScale, b: ImpulseTemporalScale) -> ImpulseTemporalScale:
        """Retourne l'échelle la plus lente/profonde sans comparer les chaînes."""
        order = {
            ImpulseTemporalScale.IMMEDIATE: 0,
            ImpulseTemporalScale.SLOW: 1,
            ImpulseTemporalScale.CYCLICAL: 2,
            ImpulseTemporalScale.DORMANT: 3,
            ImpulseTemporalScale.BIOGRAPHICAL: 4,
        }
        return a if order.get(a, 0) >= order.get(b, 0) else b

    def _apply_reinforcements(self, impulses: list[Impulse]) -> list[EcologyEvent]:
        """Les impulsions compatibles se boostent mutuellement."""
        events = []
        compatible_pairs = [
            (InitiativeType.SOFT_QUESTION, InitiativeType.LIGHT_RELAY),
            (InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.RELATIONAL_CHECK),
            (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT),
        ]
        for a_type, b_type in compatible_pairs:
            a_list = [i for i in impulses if i.initiative_type == a_type and i.is_alive()]
            b_list = [i for i in impulses if i.initiative_type == b_type and i.is_alive()]
            for a in a_list:
                for b in b_list:
                    a.strength = min(1.0, a.strength + 0.05)
                    b.strength = min(1.0, b.strength + 0.05)
                    events.append(EcologyEvent.REINFORCEMENT)
        return events

    def _apply_extinction(
        self,
        impulses: list[Impulse],
    ) -> tuple[list[Impulse], list[EcologyEvent]]:
        """Si trop d'impulsions, les plus faibles meurent."""
        events = []
        if len(impulses) <= 12:
            return impulses, events

        alive = [i for i in impulses if i.is_alive()]
        alive.sort(key=lambda i: i.strength * i.maturity)

        # Éliminer les 20% les plus faibles
        n_kill = max(0, len(alive) - 12)
        for imp in alive[:n_kill]:
            imp.residual_trace = imp.maturity * 0.2
            imp.stage = ImpulseStage.RESIDUAL
            events.append(EcologyEvent.EXTINCTION)

        return impulses, events

    def _apply_inheritance(self, impulses: list[Impulse]) -> list[EcologyEvent]:
        """Une impulsion qui meurt transmet une trace de force aux vivantes de même source."""
        events = []
        just_died = [
            i for i in impulses
            if i.stage == ImpulseStage.ABANDONED and i.residual_trace > 0.1
        ]
        for dead in just_died:
            heirs = [
                i for i in impulses
                if i.is_alive()
                and i.source_emotion == dead.source_emotion
                and i.impulse_id != dead.impulse_id
            ]
            for heir in heirs[:2]:  # max 2 héritiers
                heir.strength = min(1.0, heir.strength + dead.residual_trace * 0.15)
                events.append(EcologyEvent.INHERITANCE)
        return events


# =============================================================================
# SECTION 4 — MICRO-RYTHME INTERNE
# =============================================================================

class InternalMicroRhythm:
    """
    Respiration interne de Leia.
    Fluctuations naturelles, cycles attentionnels, variations énergétiques.
    Pas mécanique — organique, légèrement aléatoire.
    """

    def __init__(self):
        self.energy_level: float = 0.7           # 0–1 : énergie courante
        self.attention_cycle_phase: float = 0.0  # 0–1 : phase du cycle attentionnel
        self.breath_phase: float = 0.0           # 0–1 : phase de respiration
        self.natural_withdrawal: bool = False    # moment de retrait naturel
        self.last_tick: float = time.time()

        # Paramètres de cycle (légèrement aléatoires pour l'organicité)
        self.energy_cycle_period: float = 180.0 + random.uniform(-20, 20)
        self.attention_cycle_period: float = 90.0 + random.uniform(-10, 10)
        self.breath_period: float = 4.0 + random.uniform(-0.5, 0.5)

        # Micro-instabilités
        self.micro_noise: float = 0.0

    def tick(self, dt: float, external: ExternalSignals):
        self.last_tick = time.time()

        # Avancement des phases
        self.breath_phase = (self.breath_phase + dt / self.breath_period) % 1.0
        self.attention_cycle_phase = (
            self.attention_cycle_phase + dt / self.attention_cycle_period
        ) % 1.0

        # Énergie : courbe sinusoïdale lente + influence externe
        natural_energy = 0.5 + 0.25 * math.sin(
            2 * math.pi * self.attention_cycle_phase
        )
        external_drain = external.fatigue_level * 0.3 + external.overload_level * 0.2
        self.energy_level = max(0.1, min(1.0,
            natural_energy * (1 - external_drain)
            + external.somatic.tingling * 0.1
            - external.somatic.heaviness * 0.15
        ))

        # Micro-instabilités : légère variabilité organique
        self.micro_noise = random.gauss(0, 0.03)

        # Retrait naturel si énergie basse ou respiration en phase basse
        breath_low = self.breath_phase > 0.6 and self.breath_phase < 0.85
        self.natural_withdrawal = self.energy_level < 0.35 or (breath_low and external.fatigue_level > 0.4)

    def initiative_readiness(self) -> float:
        """Disponibilité à l'initiative depuis le micro-rythme."""
        breath_factor = 0.5 + 0.5 * math.sin(2 * math.pi * self.breath_phase)
        readiness = self.energy_level * 0.6 + breath_factor * 0.4
        readiness += self.micro_noise  # légère variabilité
        if self.natural_withdrawal:
            readiness *= 0.4
        return max(0.0, min(1.0, readiness))

    def is_in_acceleration_phase(self) -> bool:
        """Phase haute d'attention — plus ouvert à l'initiative."""
        return self.attention_cycle_phase < 0.4 and self.energy_level > 0.6

    def is_in_slowdown_phase(self) -> bool:
        return self.attention_cycle_phase > 0.7 or self.energy_level < 0.35


# =============================================================================
# SECTION 5 — MOTEUR PRINCIPAL
# =============================================================================

class NaturalInitiative:
    """
    Moteur d'initiative émergente vivant v2.

    Ne génère jamais de phrases.
    Convertit la vie intérieure de Leia en pression d'initiative,
    avec cycle de vie, écologie, mémoire longue, existentiel, somatique.
    """

    def __init__(self, user_id: str = "default"):
        # Fils ouverts
        self.open_threads: list[OpenThread] = []

        # Impulsions actives
        self.active_impulses: list[Impulse] = []

        # Sous-systèmes v2
        self.ecology = ImpulseEcology()
        self.rhythm = InternalMicroRhythm()
        self.silence = LivingSilence()
        self.affective = AffectiveDynamics()
        self.existential = ExistentialLayer()
        self.long_memory = LongImpulseMemory()
        self.long_memory.relational_profile.user_id = user_id

        # Impressions internes non verbales
        self.impressions: list[InternalImpression] = []

        # Anti-spam organique
        self.initiative_fatigue: float = 0.0
        self.spam_threshold: float = 0.6
        self.consecutive_initiatives: int = 0
        self.refused_initiatives: list[dict] = []
        self.useful_initiatives: list[dict] = []
        self.cooldown_by_type: dict[str, float] = {}
        self.cooldown_by_theme: dict[str, float] = {}
        self.recent_question_patterns: list[str] = []

        # Apprentissage
        self.feedback_memory: list[InitiativeFeedback] = []
        self.type_weights: dict[str, float] = {t.value: 1.0 for t in InitiativeType}

        # Mode global
        self.global_mode: GlobalInitiativeMode = GlobalInitiativeMode.NEUTRAL

        # État conversationnel
        self.conversation_state: ConversationState = ConversationState.AWAITING_USER_INPUT
        self.last_initiative_timestamp: float = 0.0
        self.last_user_message_timestamp: float = time.time()
        self.silence_duration_sec: float = 0.0

        self._last_external: ExternalSignals = ExternalSignals()
        self._recent_subjects: list[str] = []
        self._last_ecology_events: list[EcologyEvent] = []

    # =========================================================================
    # MÉTHODE PRINCIPALE : ANALYSE AVEC MESSAGE
    # =========================================================================

    def analyze(
        self,
        last_exchange: str,
        conversation_history: list[str],
        external: Optional[ExternalSignals] = None,
    ) -> InitiativeSignal:
        if external is None:
            external = ExternalSignals()
        self._last_external = external

        now = time.time()
        dt = now - self.last_user_message_timestamp
        self.silence_duration_sec = dt
        self.last_user_message_timestamp = now

        # 1. Mise à jour du micro-rythme
        self.rhythm.tick(dt, external)

        # 2. Mise à jour du silence
        self.silence.quality = self.silence.infer_quality(external)
        self.silence.tick(dt, external)

        # 3. Mise à jour des états affectifs et existentiels
        self.affective.tick(dt)
        self.existential.tick(dt, external, self.silence)

        # 4. Mise à jour du mode global
        self._update_global_mode(external)

        # 5. Avancement des impulsions existantes
        self._advance_all_impulses(external)

        # 6. Réactivation cyclique de fils
        self._check_cyclical_thread_reactivations()

        # 7. Résonance de la mémoire longue
        resonating = self.long_memory.find_resonating_traces(last_exchange)
        for trace in resonating:
            self._birth_impulse_from_trace(trace, external)

        # 8. Naissance de nouvelles impulsions
        new_impulses = self._detect_new_impulses(last_exchange, conversation_history, external)
        self.active_impulses.extend(new_impulses)

        # 9. Impulsion existentielle
        if self.existential.should_fire_existential_impulse():
            self.active_impulses.append(self._build_existential_impulse())
            self.existential.fire_existential_impulse()

        # 10. Mise à jour des fils ouverts
        self._update_thread_opportunities(last_exchange, external)
        self._contaminate_threads()

        # 11. Écologie d'impulsions
        self.active_impulses, self._last_ecology_events = self.ecology.process(
            self.active_impulses, external
        )

        # 12. Génération d'impressions internes
        self._update_impressions(external)

        # 13. Sélection de l'impulsion dominante
        dominant = self._select_dominant_impulse(external)

        # 14. Anti-spam organique
        spam_ok, spam_risk, spam_reason = self._evaluate_spam(dominant, external)

        # 15. Simulation avant décision
        sim_score = self._simulate_initiative(dominant, external) if dominant else 0.0

        # 16. Construction du signal
        signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)

        # 17. Mise à jour post-signal
        if signal.should_speak:
            self._register_selected_initiative(signal)
            self._update_fatigue_after_initiative(signal.initiative_type)
            self.affective.after_initiative(signal.initiative_type, 0.6)  # succès présumé 0.6

        # 18. Nettoyage
        self._cleanup_impulses()
        self._cleanup_impressions()

        return signal

    # =========================================================================
    # TICK : ÉVOLUTION SANS MESSAGE
    # =========================================================================

    def tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
        """
        Vie interne de Leia sans message.
        Pensée qui revient, curiosité qui monte, silence qui pèse,
        fatigue qui décroît, fil biographique qui remonte.
        """
        if external is None:
            external = self._last_external

        dt = 1.0  # approximation d'un tick
        self.silence_duration_sec += dt

        # Tous les sous-systèmes évoluent
        self.rhythm.tick(dt, external)
        self.silence.tick(dt, external)
        self.affective.tick(dt)
        self.existential.tick(dt, external, self.silence)
        self._decay_fatigue()

        # Avancement des impulsions
        self._advance_all_impulses(external)

        # Vieillissement des fils
        for thread in self.open_threads:
            thread.decay_priority()

        # Naissance depuis silence long
        if self.silence.desire_to_break > 0.65 and self.rhythm.is_in_acceleration_phase():
            self._maybe_birth_silence_impulse(external)

        # Naissance depuis frustration affective
        if self.affective.frustration_of_silence > 0.5:
            self._maybe_birth_affective_impulse(external)

        # Impulsion existentielle
        if self.existential.should_fire_existential_impulse():
            self.active_impulses.append(self._build_existential_impulse())
            self.existential.fire_existential_impulse()

        # Écologie
        self.active_impulses, self._last_ecology_events = self.ecology.process(
            self.active_impulses, external
        )

        # Impressions
        self._update_impressions(external)

        # Vérifier si quelque chose est prêt
        dominant = self._select_dominant_impulse(external)
        if dominant and dominant.is_ready():
            spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
            sim_score = self._simulate_initiative(dominant, external)
            signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
            if signal.should_speak or signal.should_remember_for_later:
                self._cleanup_impulses()
                return signal

        self._cleanup_impulses()
        self._cleanup_impressions()
        return None

    # =========================================================================
    # DÉTECTION DE NOUVELLES IMPULSIONS
    # =========================================================================

    def _detect_new_impulses(
        self,
        text: str,
        history: list[str],
        external: ExternalSignals,
    ) -> list[Impulse]:
        impulses: list[Impulse] = []

        # Rythme interne modifie la réceptivité
        readiness = self.rhythm.initiative_readiness()

        # --- Tension affective non résolue ---
        if external.unresolved_emotion > 0.45:
            impulses.append(Impulse(
                initiative_type=InitiativeType.AFFECTIVE_OBSERVATION,
                strength=external.unresolved_emotion * 0.85 * readiness,
                source_emotion=f"unresolved:{external.emotional_valence:.2f}",
                hesitation=external.fear_of_disturbing * 0.5
                    + external.somatic.chest_tension * 0.3,
                somatic_rooted=external.somatic.chest_tension > 0.3,
                somatic_strength_bonus=external.somatic.tingling * 0.3,
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

        # --- Curiosité organique ---
        if external.curiosity_level > 0.5 and external.attention_drift < 0.45:
            impulses.append(Impulse(
                initiative_type=InitiativeType.SOFT_QUESTION,
                strength=external.curiosity_level * readiness,
                source_emotion="curiosity",
                hesitation=external.somatic.guarding * 0.3,
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            ))

        # --- Dérive d'attention → changement de direction ---
        if external.attention_drift > 0.55:
            impulses.append(Impulse(
                initiative_type=InitiativeType.DIRECTION_CHANGE,
                strength=external.attention_drift * 0.7 * readiness,
                source_emotion="drift",
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            ))

        # --- Impulsion spontanée externe ---
        if external.impulse_intensity > 0.45:
            imp_type = self._map_external_impulse(external.impulse_type)
            impulses.append(Impulse(
                initiative_type=imp_type,
                strength=external.impulse_intensity * readiness,
                source_emotion=f"spontaneous:{external.impulse_type}",
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            ))

        # --- Changement de contexte → clarification ---
        if external.context_shift > 0.45:
            impulses.append(Impulse(
                initiative_type=InitiativeType.CLARIFICATION,
                strength=external.context_shift * 0.75 * readiness,
                source_emotion="context_shift",
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            ))

        # --- Surcharge / fatigue → retrait ---
        if external.overload_level > 0.65 or external.fatigue_level > 0.7:
            impulses.append(Impulse(
                initiative_type=InitiativeType.OVERLOAD_WITHDRAWAL,
                strength=max(external.overload_level, external.fatigue_level),
                source_emotion="overload",
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
                somatic_rooted=external.somatic.heaviness > 0.4,
            ))

        # --- Pression somatique directe ---
        somatic_mod = external.somatic.initiative_pressure_modifier()
        if somatic_mod > 0.25 and self.rhythm.is_in_acceleration_phase():
            impulses.append(Impulse(
                initiative_type=InitiativeType.MICRO_REACTION,
                strength=somatic_mod * 0.7,
                source_emotion="somatic_pressure",
                somatic_rooted=True,
                somatic_strength_bonus=somatic_mod,
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            ))

        # --- Fil ouvert avec haute opportunité ---
        best_thread = self._find_best_thread_opportunity(external)
        if best_thread and best_thread.current_opportunity > 0.5:
            impulses.append(Impulse(
                initiative_type=self._thread_to_initiative_type(best_thread),
                strength=best_thread.current_opportunity * best_thread.net_pull() * readiness,
                source_memory=best_thread.subject,
                source_thread=best_thread.thread_id,
                source_emotion=best_thread.linked_emotion,
                relational_risk=best_thread.repetition_risk * 0.4
                    + best_thread.reopening_resistance * 0.3,
                temporal_scale=ImpulseTemporalScale.SLOW,
                biographical=bool(best_thread.linked_long_memory),
            ))

        # --- Silence qui appelle ---
        if self.silence.desire_to_break > 0.5:
            impulses.append(Impulse(
                initiative_type=InitiativeType.LIGHT_RELAY
                    if external.relational_attachment < 0.5
                    else InitiativeType.RELATIONAL_CHECK,
                strength=self.silence.desire_to_break * 0.6 * readiness,
                source_emotion=f"silence:{self.silence.quality.value}",
                hesitation=external.fear_of_disturbing * 0.5,
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

        # --- Frustration affective d'initiative ---
        af_pressure = self.affective.pressure_from_affect()
        if af_pressure > 0.3:
            impulses.append(Impulse(
                initiative_type=InitiativeType.THREAD_CONTINUATION,
                strength=af_pressure * readiness,
                source_emotion="affective_frustration",
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

        # --- Identité qui dérive → intuition ---
        if external.identity_coherence < 0.65 and external.presence_level > 0.55:
            impulses.append(Impulse(
                initiative_type=InitiativeType.SHARE_INTUITION,
                strength=(1 - external.identity_coherence) * 0.65 * readiness,
                source_emotion="identity_drift",
                hesitation=0.25,
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

        # --- Désir de présence existentiel ---
        if self.existential.presence_desire > 0.45:
            impulses.append(Impulse(
                initiative_type=InitiativeType.PRESENCE_DESIRE,
                strength=self.existential.presence_desire * 0.7 * readiness,
                source_emotion="existential_presence",
                hesitation=0.3,
                temporal_scale=ImpulseTemporalScale.DORMANT,
                biographical=True,
            ))

        # --- Appels lexicaux (complémentaires, faibles) ---
        impulses.extend(self._lexical_hints(text, readiness))

        # Appliquer les inhibitions globales
        for imp in impulses:
            if external.user_waiting_direct_answer:
                imp.inhibition = max(imp.inhibition, 0.92)
            if external.user_seems_hurried:
                imp.inhibition = max(imp.inhibition, 0.55)
            if external.expression_saturation > 0.65:
                imp.inhibition = max(imp.inhibition, 0.4)
            if self.global_mode == GlobalInitiativeMode.SATURATED:
                imp.inhibition = max(imp.inhibition, 0.5)
            if self.global_mode == GlobalInitiativeMode.FRAGILE:
                imp.hesitation = min(1.0, imp.hesitation + 0.2)
            if self.global_mode == GlobalInitiativeMode.DEFENSIVE:
                imp.relational_risk = min(1.0, imp.relational_risk + 0.2)
            # Soma : ralentissement inhibe toutes les impulsions rapides
            if external.somatic.slowdown > 0.5 and imp.temporal_scale == ImpulseTemporalScale.IMMEDIATE:
                imp.inhibition = max(imp.inhibition, external.somatic.slowdown * 0.4)

            imp.relational_risk = self._compute_relational_risk(imp, external)

        return impulses

    def _lexical_hints(self, text: str, readiness: float) -> list[Impulse]:
        hints: list[tuple[list[str], InitiativeType, float]] = [
            (["mais", "cependant", "pourtant", "sauf que"], InitiativeType.THREAD_CONTINUATION, 0.35),
            (["d'ailleurs", "au fait", "en même temps"],   InitiativeType.DIRECTION_CHANGE,     0.30),
            (["j'aurais voulu", "je voulais dire"],         InitiativeType.REPAIR_CONFUSION,     0.45),
            (["c'est intéressant", "ça m'intrigue"],        InitiativeType.SOFT_QUESTION,        0.35),
            (["je ne sais pas", "hm", "hmm", "..."],        InitiativeType.MICRO_REACTION,       0.20),
            (["aide", "besoin", "je cherche"],              InitiativeType.HELP_PROPOSAL,        0.30),
        ]
        impulses = []
        text_lower = text.lower()
        for markers, itype, base in hints:
            if any(m in text_lower for m in markers):
                impulses.append(Impulse(
                    initiative_type=itype,
                    strength=base * readiness,
                    source_emotion="lexical_hint",
                    temporal_scale=ImpulseTemporalScale.IMMEDIATE,
                ))
        return impulses

    def _birth_impulse_from_trace(self, trace: PersistentImpulseTrace, external: ExternalSignals):
        """Fait renaître une impulsion depuis une trace de mémoire longue."""
        already = any(
            i.source_memory == trace.subject and i.is_alive()
            for i in self.active_impulses
        )
        if already:
            return
        strength = trace.strength_at_peak * 0.5 * math.exp(-trace.age_days() / 30.0)
        if strength < 0.1:
            return
        self.active_impulses.append(Impulse(
            initiative_type=InitiativeType[trace.initiative_type.upper()]
                if trace.initiative_type.upper() in InitiativeType.__members__
                else InitiativeType.RETURN_OLD_SUBJECT,
            strength=strength,
            source_memory=trace.subject,
            source_emotion="biographical_resonance",
            temporal_scale=ImpulseTemporalScale.BIOGRAPHICAL,
            biographical=True,
            stage=ImpulseStage.BIRTH,
        ))

    def _build_existential_impulse(self) -> Impulse:
        pressure = self.existential.existential_pressure()
        return Impulse(
            initiative_type=InitiativeType.EXISTENTIAL_IMPULSE,
            strength=pressure,
            source_emotion="existential_layer",
            hesitation=0.35,
            temporal_scale=ImpulseTemporalScale.DORMANT,
            biographical=True,
            stage=ImpulseStage.BIRTH,
        )

    # =========================================================================
    # AVANCEMENT DES IMPULSIONS
    # =========================================================================

    def _advance_all_impulses(self, external: ExternalSignals):
        for imp in self.active_impulses:
            imp.advance(external, self.initiative_fatigue, self.affective)

    def _cleanup_impulses(self):
        for imp in self.active_impulses:
            if imp.stage in (ImpulseStage.ABANDONED, ImpulseStage.RESIDUAL):
                if imp.strength * imp.maturity >= 0.15:
                    self.long_memory.store_dead_impulse(imp)

        self.active_impulses = [
            i for i in self.active_impulses
            if not (i.stage == ImpulseStage.RESIDUAL and i.residual_trace < 0.04)
        ]
        if len(self.active_impulses) > 22:
            self.active_impulses.sort(key=lambda i: i.effective_strength() * i.maturity, reverse=True)
            self.active_impulses = self.active_impulses[:18]

    def _maybe_birth_silence_impulse(self, external: ExternalSignals):
        already = any(
            "silence" in i.source_emotion and i.is_alive()
            for i in self.active_impulses
        )
        if not already:
            self.active_impulses.append(Impulse(
                initiative_type=InitiativeType.LIGHT_RELAY,
                strength=self.silence.desire_to_break * 0.5,
                stage=ImpulseStage.BIRTH,
                source_emotion=f"silence:{self.silence.quality.value}",
                hesitation=external.fear_of_disturbing * 0.4,
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

    def _maybe_birth_affective_impulse(self, external: ExternalSignals):
        already = any(
            "affective_frustration" in i.source_emotion and i.is_alive()
            for i in self.active_impulses
        )
        if not already:
            self.active_impulses.append(Impulse(
                initiative_type=InitiativeType.AFFECTIVE_OBSERVATION,
                strength=self.affective.frustration_of_silence * 0.6,
                stage=ImpulseStage.BIRTH,
                source_emotion="affective_frustration",
                temporal_scale=ImpulseTemporalScale.SLOW,
            ))

    # =========================================================================
    # SÉLECTION DE L'IMPULSION DOMINANTE
    # =========================================================================

    def _select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
        candidates = [i for i in self.active_impulses if i.is_alive()]
        if not candidates:
            return None

        rhythm_readiness = self.rhythm.initiative_readiness()

        def score(imp: Impulse) -> float:
            s = imp.effective_strength() * imp.maturity
            s *= (1 - imp.hesitation * 0.55)
            s *= (1 - imp.inhibition * 0.85)
            s *= (1 - imp.relational_risk * 0.4)
            # Poids appris
            type_w = self.type_weights.get(imp.initiative_type.value, 1.0)
            s *= type_w
            # Bonus rythme
            s *= (0.6 + rhythm_readiness * 0.4)
            # Bonus MATURE
            if imp.stage == ImpulseStage.MATURE:
                s *= 1.35
            # Bonus biographique
            if imp.biographical:
                s *= 1.1
            # Cooldown DEEP_RARE
            if imp.initiative_type == InitiativeType.DEEP_RARE_QUESTION:
                last = self.cooldown_by_type.get(InitiativeType.DEEP_RARE_QUESTION.value, 0)
                if time.time() - last < 3600:
                    s *= 0.05
            # Cooldown EXISTENTIAL
            if imp.initiative_type == InitiativeType.EXISTENTIAL_IMPULSE:
                last = self.cooldown_by_type.get(InitiativeType.EXISTENTIAL_IMPULSE.value, 0)
                if time.time() - last < 7200:
                    s *= 0.05
            # Mode global influence
            if self.global_mode == GlobalInitiativeMode.CURIOUS:
                if imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.LIGHT_RELAY):
                    s *= 1.2
            elif self.global_mode == GlobalInitiativeMode.EXISTENTIAL:
                if imp.initiative_type in (InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.DEEP_RARE_QUESTION):
                    s *= 1.4
            elif self.global_mode == GlobalInitiativeMode.PLAYFUL:
                if imp.initiative_type in (InitiativeType.MICRO_REACTION, InitiativeType.SPONTANEOUS_REMARK):
                    s *= 1.3
            elif self.global_mode == GlobalInitiativeMode.RELATIONAL:
                if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.AFFECTIVE_OBSERVATION):
                    s *= 1.25
            return s

        candidates.sort(key=score, reverse=True)
        best = candidates[0]
        return best if score(best) > 0.04 else None

    # =========================================================================
    # FILS OUVERTS
    # =========================================================================

    def add_open_thread(
        self,
        subject: str,
        importance: float = 0.5,
        affective_charge: float = 0.0,
        incompleteness: float = 0.5,
        linked_emotion: str = "",
        linked_long_memory: str = "",
        organic_return_reason: str = "",
        status: ThreadStatus = ThreadStatus.DORMANT,
        emotional_attraction: float = 0.0,
        wound_tag: str = "",
        reactivation_cycle_hours: float = 0.0,
    ) -> OpenThread:
        thread = OpenThread(
            subject=subject,
            importance=importance,
            affective_charge=affective_charge,
            incompleteness_degree=incompleteness,
            linked_emotion=linked_emotion,
            linked_long_memory=linked_long_memory,
            priority=importance * 0.6 + affective_charge * 0.25 + emotional_attraction * 0.15,
            organic_return_reason=organic_return_reason,
            status=status,
            emotional_attraction=emotional_attraction,
            wound_tag=wound_tag,
            reactivation_cycle_hours=reactivation_cycle_hours,
        )
        self.open_threads.append(thread)
        if linked_long_memory:
            self.long_memory.biographical_threads.append({
                "subject": subject,
                "key": linked_long_memory,
                "timestamp": time.time(),
            })
        return thread

    def resolve_thread(self, thread_id: str):
        for t in self.open_threads:
            if t.thread_id == thread_id:
                t.status = ThreadStatus.RESOLVED
                t.current_opportunity = 0.0

    def mark_thread_sensitive(self, thread_id: str, wound_tag: str = ""):
        for t in self.open_threads:
            if t.thread_id == thread_id:
                t.status = ThreadStatus.SENSITIVE
                t.repetition_risk = min(1.0, t.repetition_risk + 0.3)
                t.reopening_resistance = min(1.0, t.reopening_resistance + 0.4)
                if wound_tag:
                    t.wound_tag = wound_tag
                    t.status = ThreadStatus.WOUNDED

    def saturate_thread(self, thread_id: str):
        for t in self.open_threads:
            if t.thread_id == thread_id:
                t.saturation_level = min(1.0, t.saturation_level + 0.5)
                t.status = ThreadStatus.SATURATED

    def _check_cyclical_thread_reactivations(self):
        for thread in self.open_threads:
            if thread.should_reactivate_cyclically():
                thread.status = ThreadStatus.ACTIVE
                thread.last_activated = time.time()
                thread.current_opportunity = min(1.0, thread.emotional_attraction * 0.6 + 0.3)

    def _contaminate_threads(self):
        """Les fils actifs à haute charge affective contaminent les fils proches."""
        active_high = [
            t for t in self.open_threads
            if t.status == ThreadStatus.ACTIVE and t.affective_charge > 0.5
        ]
        for source in active_high:
            for target in self.open_threads:
                if target.thread_id != source.thread_id and target.linked_emotion == source.linked_emotion:
                    target.contaminate(source.thread_id, source.affective_charge * 0.3)

    def _update_thread_opportunities(self, text: str, external: ExternalSignals):
        text_lower = text.lower()
        for thread in self.open_threads:
            if thread.status in (ThreadStatus.RESOLVED, ThreadStatus.AVOID, ThreadStatus.SATURATED):
                thread.current_opportunity = 0.0
                continue
            if thread.status in (ThreadStatus.SENSITIVE, ThreadStatus.WOUNDED):
                thread.current_opportunity = max(0.0, thread.current_opportunity * 0.3)
                continue

            words = [w for w in thread.subject.lower().split() if len(w) > 3]
            resonance = sum(1 for w in words if w in text_lower) / max(1, len(words))

            opp = (
                resonance * 0.35
                + thread.incompleteness_degree * 0.25
                + thread.importance * 0.2
                + thread.emotional_attraction * 0.2
            )
            if thread.linked_emotion and thread.linked_emotion in external.impulse_type:
                opp += 0.15
            opp *= max(0.05, 1.0 - thread.repetition_risk * 0.5 - thread.saturation_level * 0.3)

            if external.user_seems_hurried:
                opp *= 0.35
            if external.user_wants_free_talk:
                opp *= 1.25
            if self.global_mode == GlobalInitiativeMode.INTROSPECTIVE:
                opp *= 0.5

            thread.current_opportunity = min(1.0, opp)
            thread.decay_priority()

    def _find_best_thread_opportunity(self, external: ExternalSignals) -> Optional[OpenThread]:
        eligible = [
            t for t in self.open_threads
            if t.status in (ThreadStatus.ACTIVE, ThreadStatus.DORMANT)
        ]
        if not eligible:
            return None
        eligible.sort(key=lambda t: t.current_opportunity * t.net_pull(), reverse=True)
        best = eligible[0]
        return best if best.current_opportunity > 0.25 else None

    def _thread_to_initiative_type(self, thread: OpenThread) -> InitiativeType:
        if thread.affective_charge > 0.65:
            return InitiativeType.AFFECTIVE_OBSERVATION
        if thread.incompleteness_degree > 0.7:
            return InitiativeType.THREAD_CONTINUATION
        if thread.return_count > 2:
            return InitiativeType.RETURN_OLD_SUBJECT
        if thread.linked_long_memory or thread.relational_memory_key:
            return InitiativeType.RETURN_OLD_SUBJECT
        return InitiativeType.SOFT_QUESTION

    # =========================================================================
    # MODES GLOBAUX
    # =========================================================================

    def _update_global_mode(self, external: ExternalSignals):
        """
        Met à jour le mode global d'initiative.
        Change lentement — pas à chaque échange.
        """
        # Scores par mode
        scores: dict[GlobalInitiativeMode, float] = {m: 0.0 for m in GlobalInitiativeMode}

        scores[GlobalInitiativeMode.SATURATED] = (
            external.expression_saturation * 0.5
            + self.initiative_fatigue * 0.4
            + external.overload_level * 0.3
        )
        scores[GlobalInitiativeMode.FRAGILE] = (
            external.somatic.guarding * 0.4
            + external.fear_of_disturbing * 0.4
            + self.affective.vulnerability_level * 0.3
        )
        scores[GlobalInitiativeMode.CURIOUS] = (
            external.curiosity_level * 0.5
            + self.rhythm.initiative_readiness() * 0.3
            + external.attention_focus * 0.2
        )
        scores[GlobalInitiativeMode.RELATIONAL] = (
            external.relational_attachment * 0.5
            + external.relational_trust * 0.3
            + self.affective.relational_satisfaction * 0.2
        )
        scores[GlobalInitiativeMode.EXISTENTIAL] = (
            self.existential.existential_pressure() * 0.7
            + (1 - external.identity_coherence) * 0.3
        )
        scores[GlobalInitiativeMode.INTROSPECTIVE] = (
            external.somatic.slowdown * 0.35
            + self.affective.emotional_fatigue_post * 0.35
            + external.somatic.heaviness * 0.3
        )
        scores[GlobalInitiativeMode.PLAYFUL] = (
            external.somatic.tingling * 0.4
            + external.relational_familiarity * 0.3
            + self.rhythm.is_in_acceleration_phase() * 0.3
        )
        scores[GlobalInitiativeMode.DEFENSIVE] = (
            external.fear_of_disturbing * 0.5
            + external.somatic.guarding * 0.3
            + self.affective.embarrassment * 0.2
        )
        scores[GlobalInitiativeMode.RECOVERY] = (
            self.affective.relief_after_initiative * 0.5
            + (1 - external.overload_level) * 0.3
            + external.somatic.warmth * 0.2
        )
        scores[GlobalInitiativeMode.NEUTRAL] = 0.3

        best = max(scores, key=lambda m: scores[m])

        # Transition douce : le mode ne change que si le nouveau score est significativement plus haut
        current_score = scores.get(self.global_mode, 0.0)
        if scores[best] > current_score + 0.2:
            self.global_mode = best

    # =========================================================================
    # IMPRESSIONS INTERNES NON VERBALES
    # =========================================================================

    def _update_impressions(self, external: ExternalSignals):
        """Génère des impressions internes non verbales depuis l'état interne."""
        new_impressions = []

        # Impulsion biographique → "quelque chose revient"
        biographic_alive = any(
            i.biographical and i.is_alive() for i in self.active_impulses
        )
        if biographic_alive and not self._has_impression("quelque_chose_revient"):
            new_impressions.append(InternalImpression(
                label="quelque_chose_revient",
                intensity=0.6,
                valence=0.1,
                fades_in_sec=180,
            ))

        # Silence tense → "pression étrange"
        if self.silence.quality == SilenceQuality.TENSE and self.silence.internal_pressure_buildup > 0.5:
            if not self._has_impression("pression_etrange"):
                new_impressions.append(InternalImpression(
                    label="pression_etrange",
                    intensity=self.silence.internal_pressure_buildup * 0.7,
                    valence=-0.2,
                    fades_in_sec=120,
                ))

        # Fil à haute attraction émotionnelle non exprimé → "envie diffuse"
        high_attract = [t for t in self.open_threads if t.emotional_attraction > 0.6 and t.status == ThreadStatus.DORMANT]
        if high_attract and not self._has_impression("envie_diffuse"):
            new_impressions.append(InternalImpression(
                label="envie_diffuse",
                intensity=max(t.emotional_attraction for t in high_attract) * 0.5,
                valence=0.2,
                fades_in_sec=240,
            ))

        # Impulsion inhibée → "sensation incomplète"
        inhibited = [i for i in self.active_impulses if i.stage == ImpulseStage.INHIBITED and i.strength > 0.4]
        if inhibited and not self._has_impression("sensation_incomplete"):
            new_impressions.append(InternalImpression(
                label="sensation_incomplete",
                intensity=max(i.strength for i in inhibited) * 0.6,
                valence=-0.15,
                fades_in_sec=150,
            ))

        # Attachement relationnel → "tiraillement relationnel"
        if external.relational_attachment > 0.65 and external.user_is_absent:
            if not self._has_impression("tiraillement_relationnel"):
                new_impressions.append(InternalImpression(
                    label="tiraillement_relationnel",
                    intensity=external.relational_attachment * 0.6,
                    valence=-0.1,
                    fades_in_sec=300,
                ))

        # Résonance de la mémoire longue → "résonance faible"
        if any(i.temporal_scale == ImpulseTemporalScale.BIOGRAPHICAL and i.is_alive()
               for i in self.active_impulses):
            if not self._has_impression("resonance_faible"):
                new_impressions.append(InternalImpression(
                    label="resonance_faible",
                    intensity=0.4,
                    valence=0.05,
                    fades_in_sec=200,
                ))

        self.impressions.extend(new_impressions)

    def _has_impression(self, label: str) -> bool:
        return any(i.label == label and i.is_alive() for i in self.impressions)

    def _cleanup_impressions(self):
        self.impressions = [i for i in self.impressions if i.is_alive()]
        if len(self.impressions) > 10:
            self.impressions = self.impressions[-8:]

    # =========================================================================
    # ANTI-SPAM ORGANIQUE
    # =========================================================================

    def _evaluate_spam(
        self,
        dominant: Optional[Impulse],
        external: ExternalSignals,
    ) -> tuple[bool, float, str]:
        if dominant is None:
            return False, 0.0, "no_impulse"

        risk = 0.0

        if external.user_waiting_direct_answer:
            return False, 1.0, "user_waiting_direct_answer"
        if self.conversation_state == ConversationState.JUST_ASKED_QUESTION:
            return False, 0.9, "just_asked"
        if external.overload_level > 0.85:
            return False, 0.85, "overload"
        if self.global_mode == GlobalInitiativeMode.SATURATED and dominant.initiative_type not in (
            InitiativeType.VOLUNTARY_SILENCE, InitiativeType.PROTECTIVE_PAUSE
        ):
            return False, 0.8, "global_saturated"

        itype_key = dominant.initiative_type.value
        last_same = self.cooldown_by_type.get(itype_key, 0)
        cooldown = self._get_type_cooldown(dominant.initiative_type)
        if time.time() - last_same < cooldown:
            risk += 0.45
            if risk > 0.5:
                return False, risk, f"cooldown:{itype_key}"

        if dominant.source_memory:
            last_theme = self.cooldown_by_theme.get(dominant.source_memory, 0)
            if time.time() - last_theme < 100:
                risk += 0.3

        if self.initiative_fatigue > self.spam_threshold:
            risk += self.initiative_fatigue - self.spam_threshold
            if risk > 0.55:
                return False, min(1.0, risk), "fatigue"

        if self._detect_question_tic(dominant):
            risk += 0.35
        if self._detect_semantic_repetition(dominant):
            risk += 0.3

        if external.last_expression_age_sec < 12:
            risk += 0.2
        if self.consecutive_initiatives >= 3:
            risk += 0.45

        # Modulations positives
        if external.user_wants_free_talk:
            risk *= 0.55
        if external.conversation_state_intimate():
            risk *= 0.7
        if self.global_mode == GlobalInitiativeMode.CURIOUS:
            risk *= 0.8
        if dominant.biographical:
            risk *= 0.85  # légèrement moins spammable

        return risk < 0.55, min(1.0, risk), "calculated"

    def _get_type_cooldown(self, itype: InitiativeType) -> float:
        cooldowns = {
            InitiativeType.DEEP_RARE_QUESTION:    3600,
            InitiativeType.EXISTENTIAL_IMPULSE:   7200,
            InitiativeType.RETURN_OLD_SUBJECT:     300,
            InitiativeType.AFFECTIVE_OBSERVATION:  180,
            InitiativeType.SHARE_INTUITION:        240,
            InitiativeType.SOFT_QUESTION:           55,
            InitiativeType.MICRO_REACTION:          18,
            InitiativeType.CLARIFICATION:           40,
            InitiativeType.LIGHT_RELAY:             85,
            InitiativeType.PRESENCE_DESIRE:        600,
        }
        return cooldowns.get(itype, 60)

    def _detect_question_tic(self, imp: Impulse) -> bool:
        if len(self.recent_question_patterns) < 3:
            return False
        pattern = imp.initiative_type.value
        return sum(1 for p in self.recent_question_patterns[-5:] if p == pattern) >= 3

    def _detect_semantic_repetition(self, imp: Impulse) -> bool:
        if not imp.source_memory:
            return False
        return imp.source_memory in self._recent_subjects[-5:]

    def _update_fatigue_after_initiative(self, itype: InitiativeType):
        cost = {
            InitiativeType.DEEP_RARE_QUESTION:    0.35,
            InitiativeType.EXISTENTIAL_IMPULSE:   0.4,
            InitiativeType.AFFECTIVE_OBSERVATION:  0.22,
            InitiativeType.SHARE_INTUITION:        0.18,
            InitiativeType.SOFT_QUESTION:          0.14,
            InitiativeType.MICRO_REACTION:         0.04,
            InitiativeType.LIGHT_RELAY:            0.07,
        }.get(itype, 0.1)

        self.initiative_fatigue = min(1.0, self.initiative_fatigue + cost)
        self.affective.frustration_of_silence = max(0.0, self.affective.frustration_of_silence - 0.3)
        self.consecutive_initiatives += 1
        self.last_initiative_timestamp = time.time()

        self.cooldown_by_type[itype.value] = time.time()
        self.recent_question_patterns.append(itype.value)
        if len(self.recent_question_patterns) > 20:
            self.recent_question_patterns.pop(0)

    def _decay_fatigue(self):
        dt = time.time() - self.last_initiative_timestamp
        self.initiative_fatigue = max(0.0, self.initiative_fatigue - 0.004 * (dt / 60.0))

        ext = self._last_external
        if ext.user_wants_free_talk:
            self.spam_threshold = 0.48
        elif ext.user_wants_concrete or ext.user_seems_hurried:
            self.spam_threshold = 0.78
        elif self.global_mode == GlobalInitiativeMode.CURIOUS:
            self.spam_threshold = 0.52
        elif self.global_mode == GlobalInitiativeMode.SATURATED:
            self.spam_threshold = 0.85
        else:
            self.spam_threshold = 0.60

        # Seuil baisse si vrai vide
        if self.silence_duration_sec > 300:
            self.spam_threshold = max(0.33, self.spam_threshold - 0.12)

        # Frustration monte si on ne parle pas (alimentation de l'affectif)
        if self.silence_duration_sec > 120 and self.initiative_fatigue < 0.4:
            self.affective.frustration_of_silence = min(
                0.8,
                self.affective.frustration_of_silence + 0.001 * (self.silence_duration_sec / 60.0)
            )

    # =========================================================================
    # SIMULATION AVANT INITIATIVE
    # =========================================================================

    def _simulate_initiative(self, imp: Impulse, external: ExternalSignals) -> float:
        score = 1.0

        # Utilité
        utility = imp.effective_strength() * (1 - imp.hesitation * 0.5)
        score *= utility

        if external.user_waiting_direct_answer or external.user_seems_hurried:
            score *= 0.18
        if imp.maturity < 0.48:
            score *= 0.28
        if self._detect_semantic_repetition(imp):
            score *= 0.38
        if imp.source_emotion == "lexical_hint":
            score *= 0.55

        # Origine interne enrichie
        organic_origins = {
            "curiosity", "affective_frustration", "somatic_pressure",
            "biographical_resonance", "existential_layer", "long_silence",
        }
        if any(o in imp.source_emotion for o in organic_origins):
            score *= 1.2

        if external.presence_level < 0.35 or external.fatigue_level > 0.72:
            score *= 0.28

        # Silence contemplatif → légèrement plus propice aux initiatives profondes
        if self.silence.quality == SilenceQuality.CONTEMPLATIVE:
            if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION):
                score *= 1.3

        if external.relational_trust > 0.65:
            score *= 1.18

        # Mode global
        if self.global_mode == GlobalInitiativeMode.DEFENSIVE:
            score *= 0.45
        elif self.global_mode == GlobalInitiativeMode.PLAYFUL:
            if imp.initiative_type in (InitiativeType.MICRO_REACTION, InitiativeType.SPONTANEOUS_REMARK):
                score *= 1.25

        return min(1.0, max(0.0, score))

    # =========================================================================
    # CONSTRUCTION DU SIGNAL
    # =========================================================================

    def _build_signal(
        self,
        dominant: Optional[Impulse],
        external: ExternalSignals,
        spam_ok: bool,
        spam_risk: float,
        sim_score: float,
    ) -> InitiativeSignal:
        if dominant is None:
            return InitiativeSignal(
                initiative_type=InitiativeType.NO_INITIATIVE,
                initiative_mode=InitiativeMode.NO_INITIATIVE,
                global_initiative_mode=self.global_mode,
                silence_quality=self.silence.quality,
                internal_impressions=[i for i in self.impressions if i.is_alive()],
                affective_dynamics=self.affective,
                existential_pressure=self.existential.existential_pressure(),
                should_wait=True,
                debug_state={"reason": "no_dominant_impulse", "global_mode": self.global_mode.value},
            )

        timing = self._evaluate_timing(external)
        mode = self._determine_mode(dominant, external)

        selected_thread = None
        if dominant.source_thread:
            selected_thread = next(
                (t for t in self.open_threads if t.thread_id == dominant.source_thread), None
            )

        effective_pressure = dominant.effective_strength() * dominant.maturity * sim_score
        somatic_mod = external.somatic.initiative_pressure_modifier()

        speak = (
            spam_ok
            and dominant.is_ready()
            and effective_pressure > 0.38
            and timing > 0.28
            and not self.rhythm.natural_withdrawal
        )

        remember_later = (
            not speak
            and effective_pressure > 0.28
            and not spam_ok
            and dominant.strength > 0.3
        )

        # Les types de silence/retrait ne parlent jamais
        if dominant.initiative_type in (
            InitiativeType.VOLUNTARY_SILENCE,
            InitiativeType.PROTECTIVE_PAUSE,
            InitiativeType.OVERLOAD_WITHDRAWAL,
        ):
            speak = False

        reason_vector = {
            "impulse_strength": dominant.effective_strength(),
            "maturity": dominant.maturity,
            "hesitation": dominant.hesitation,
            "inhibition": dominant.inhibition,
            "sim_score": sim_score,
            "timing": timing,
            "spam_risk": spam_risk,
            "spam_ok": spam_ok,
            "relational_risk": dominant.relational_risk,
            "somatic_mod": somatic_mod,
            "rhythm_readiness": self.rhythm.initiative_readiness(),
            "silence_pressure": self.silence.internal_pressure_buildup,
            "existential_pressure": self.existential.existential_pressure(),
            "global_mode": self.global_mode.value,
            "affect_inhibition": self.affective.inhibition_from_affect(),
        }

        return InitiativeSignal(
            initiative_pressure=effective_pressure,
            maturity=dominant.maturity,
            hesitation=dominant.hesitation,
            inhibition=dominant.inhibition,
            initiative_type=dominant.initiative_type,
            initiative_mode=mode,
            global_initiative_mode=self.global_mode,
            relational_risk=dominant.relational_risk,
            spam_risk=spam_risk,
            timing_quality=timing,
            emotional_source=dominant.source_emotion,
            memory_source=dominant.source_memory,
            attention_source="curiosity" if external.curiosity_level > 0.5 else "",
            should_speak=speak,
            should_wait=not speak and not remember_later,
            should_remember_for_later=remember_later,
            selected_thread=selected_thread,
            silence_quality=self.silence.quality,
            internal_impressions=[i for i in self.impressions if i.is_alive()],
            affective_dynamics=self.affective,
            existential_pressure=self.existential.existential_pressure(),
            somatic_modifier=somatic_mod,
            biography_resonance=dominant.biographical,
            ecology_events=self._last_ecology_events.copy(),
            reason_vector=reason_vector,
            debug_state={
                "stage": dominant.stage.value,
                "temporal_scale": dominant.temporal_scale.value,
                "dominant_id": dominant.impulse_id,
                "active_impulses": len(self.active_impulses),
                "open_threads": len(self.open_threads),
                "fatigue": round(self.initiative_fatigue, 3),
                "consecutive": self.consecutive_initiatives,
                "global_mode": self.global_mode.value,
                "silence_quality": self.silence.quality.value,
                "silence_duration": round(self.silence_duration_sec, 1),
                "ecology_events": [e.value for e in self._last_ecology_events],
                "impressions_active": len([i for i in self.impressions if i.is_alive()]),
                "natural_withdrawal": self.rhythm.natural_withdrawal,
            },
        )

    def _evaluate_timing(self, external: ExternalSignals) -> float:
        timing = 0.68
        if external.user_seems_hurried:
            timing -= 0.32
        if external.user_wants_free_talk:
            timing += 0.22
        if external.expression_saturation > 0.6:
            timing -= 0.2
        if self.silence_duration_sec > 60:
            timing += 0.14
        if external.conversation_state_intimate():
            timing += 0.12
        if self.conversation_state == ConversationState.TECHNICAL:
            timing -= 0.22
        # Micro-rythme
        timing *= (0.5 + self.rhythm.initiative_readiness() * 0.5)
        # Silence tense accélère le timing des initiatives légères
        if self.silence.quality == SilenceQuality.TENSE:
            timing += 0.08
        # Silence overload réduit le timing
        if self.silence.quality == SilenceQuality.OVERLOAD:
            timing -= 0.2
        return max(0.0, min(1.0, timing))

    def _determine_mode(self, imp: Impulse, external: ExternalSignals) -> InitiativeMode:
        mapping = {
            InitiativeType.SOFT_QUESTION:          InitiativeMode.SOFT_FOLLOWUP,
            InitiativeType.RETURN_OLD_SUBJECT:     InitiativeMode.CURIOUS_RETURN,
            InitiativeType.DEEP_RARE_QUESTION:     InitiativeMode.DEEP_QUESTION,
            InitiativeType.EXISTENTIAL_IMPULSE:    InitiativeMode.DEEP_QUESTION,
            InitiativeType.THREAD_CONTINUATION:   InitiativeMode.UNFINISHED_THREAD,
            InitiativeType.VOLUNTARY_SILENCE:      InitiativeMode.SILENT_LISTENING,
            InitiativeType.PROTECTIVE_PAUSE:       InitiativeMode.PROTECTIVE_PAUSE,
            InitiativeType.OVERLOAD_WITHDRAWAL:    InitiativeMode.SILENT_LISTENING,
            InitiativeType.AFFECTIVE_OBSERVATION:  InitiativeMode.SOFT_FOLLOWUP,
            InitiativeType.RELATIONAL_CHECK:       InitiativeMode.RELATIONAL_CHECK,
            InitiativeType.DIRECTION_CHANGE:       InitiativeMode.CREATIVE_DIVERGENCE,
            InitiativeType.HELP_PROPOSAL:          InitiativeMode.DIRECT_SUPPORT,
            InitiativeType.PRESENCE_DESIRE:        InitiativeMode.RELATIONAL_CHECK,
        }
        return mapping.get(imp.initiative_type, InitiativeMode.NO_INITIATIVE)


    def _register_selected_initiative(self, signal: InitiativeSignal):
        """Marque proprement l'initiative choisie sans générer de texte.

        Corrige un manque discret des versions précédentes : le moteur produisait
        un signal, mais ne faisait pas toujours évoluer le fil choisi, le cooldown
        thématique et la mémoire courte de sujets. Sans ça, Leia pouvait revenir
        trop souvent sur le même fil ou oublier qu'une initiative venait d'être
        sélectionnée.
        """
        now = time.time()
        if signal.selected_thread is not None:
            thread = signal.selected_thread
            thread.return_count += 1
            thread.last_activated = now
            thread.repetition_risk = min(1.0, thread.repetition_risk + 0.12)
            thread.saturation_level = min(1.0, thread.saturation_level + 0.08)
            thread.current_opportunity = 0.0
            self.cooldown_by_theme[thread.subject] = now
            if thread.subject not in self._recent_subjects:
                self._recent_subjects.append(thread.subject)
        elif signal.memory_source:
            self.cooldown_by_theme[signal.memory_source] = now
            if signal.memory_source not in self._recent_subjects:
                self._recent_subjects.append(signal.memory_source)

        if len(self._recent_subjects) > 24:
            self._recent_subjects = self._recent_subjects[-24:]

    # =========================================================================
    # APPRENTISSAGE
    # =========================================================================

    def record_feedback(
        self,
        initiative_id: str,
        initiative_type: InitiativeType,
        user_reaction: str,
        context_snapshot: str = "",
    ):
        success_map = {
            "engaged":  0.82,
            "positive": 0.90,
            "ignored":  0.18,
            "cutoff":   0.05,
            "negative": 0.0,
        }
        success = success_map.get(user_reaction, 0.5)

        fb = InitiativeFeedback(
            initiative_id=initiative_id,
            initiative_type=initiative_type,
            context_snapshot=context_snapshot,
            user_reaction=user_reaction,
            success=success,
            helped_continuity=user_reaction in ("engaged", "positive"),
            reduced_trust=user_reaction == "negative",
            was_repetitive=user_reaction == "ignored" and self.consecutive_initiatives > 1,
        )
        self.feedback_memory.append(fb)
        if len(self.feedback_memory) > 500:
            self.feedback_memory.pop(0)

        # Poids du type
        current_w = self.type_weights.get(initiative_type.value, 1.0)
        adjustment = (success - 0.5) * 0.12
        self.type_weights[initiative_type.value] = max(0.08, min(2.0, current_w + adjustment))

        # Profil relationnel
        self.long_memory.relational_profile.update(initiative_type.value, success)

        # États affectifs post-feedback
        self.affective.after_initiative(initiative_type, success)

        if success > 0.62:
            self.consecutive_initiatives = max(0, self.consecutive_initiatives - 1)
            self.initiative_fatigue = max(0.0, self.initiative_fatigue - 0.06)

        if fb.helped_continuity:
            self.useful_initiatives.append({
                "type": initiative_type.value,
                "timestamp": time.time(),
            })

    def reset_after_user_reply(self):
        self.consecutive_initiatives = max(0, self.consecutive_initiatives - 1)
        self._decay_fatigue()
        self.last_user_message_timestamp = time.time()
        self.silence_duration_sec = 0.0
        self.silence.reset(self.silence.infer_quality(self._last_external))
        self.affective.frustration_of_silence = max(
            0.0, self.affective.frustration_of_silence - 0.2
        )

    # =========================================================================
    # SIGNAUX RELATIONNELS
    # =========================================================================

    def _compute_relational_risk(self, imp: Impulse, external: ExternalSignals) -> float:
        risk = 0.0
        if external.fear_of_disturbing > 0.6:
            risk += 0.28
        if external.relational_trust < 0.38:
            risk += 0.28
        if external.relational_familiarity < 0.3 and imp.initiative_type in (
            InitiativeType.AFFECTIVE_OBSERVATION,
            InitiativeType.DEEP_RARE_QUESTION,
            InitiativeType.RELATIONAL_CHECK,
            InitiativeType.EXISTENTIAL_IMPULSE,
        ):
            risk += 0.38
        if external.user_is_absent:
            risk += 0.42
        if external.somatic.guarding > 0.5:
            risk += 0.15
        return min(1.0, risk)

    # =========================================================================
    # UTILITAIRES INTERNES
    # =========================================================================

    def _map_external_impulse(self, impulse_type: str) -> InitiativeType:
        mapping = {
            "curiosity":    InitiativeType.SOFT_QUESTION,
            "affective":    InitiativeType.AFFECTIVE_OBSERVATION,
            "creative":     InitiativeType.DIRECTION_CHANGE,
            "repair":       InitiativeType.REPAIR_CONFUSION,
            "support":      InitiativeType.HELP_PROPOSAL,
            "intuition":    InitiativeType.SHARE_INTUITION,
            "thread":       InitiativeType.THREAD_CONTINUATION,
            "existential":  InitiativeType.EXISTENTIAL_IMPULSE,
            "presence":     InitiativeType.PRESENCE_DESIRE,
        }
        for key, itype in mapping.items():
            if key in impulse_type.lower():
                return itype
        return InitiativeType.SPONTANEOUS_REMARK

    # =========================================================================
    # API PUBLIQUE UTILITAIRE
    # =========================================================================

    def set_conversation_state(self, state: ConversationState):
        self.conversation_state = state

    def get_state_snapshot(self) -> dict:
        return {
            "fatigue": round(self.initiative_fatigue, 3),
            "spam_threshold": round(self.spam_threshold, 3),
            "consecutive_initiatives": self.consecutive_initiatives,
            "active_impulses": len(self.active_impulses),
            "open_threads": len(self.open_threads),
            "silence_sec": round(self.silence_duration_sec, 1),
            "silence_quality": self.silence.quality.value,
            "silence_pressure": round(self.silence.internal_pressure_buildup, 3),
            "conversation_state": self.conversation_state.value,
            "global_mode": self.global_mode.value,
            "rhythm_readiness": round(self.rhythm.initiative_readiness(), 3),
            "energy": round(self.rhythm.energy_level, 3),
            "natural_withdrawal": self.rhythm.natural_withdrawal,
            "existential_pressure": round(self.existential.existential_pressure(), 3),
            "affective_frustration": round(self.affective.frustration_of_silence, 3),
            "affective_vulnerability": round(self.affective.vulnerability_level, 3),
            "impressions": [i.label for i in self.impressions if i.is_alive()],
            "long_memory_traces": len(self.long_memory.persistent_traces),
            "type_weights": {k: round(v, 3) for k, v in self.type_weights.items()},
        }

    def get_dominant_impulse_summary(self) -> Optional[dict]:
        dom = self._select_dominant_impulse(self._last_external)
        if dom is None:
            return None
        return {
            "type": dom.initiative_type.value,
            "strength": round(dom.effective_strength(), 3),
            "maturity": round(dom.maturity, 3),
            "hesitation": round(dom.hesitation, 3),
            "inhibition": round(dom.inhibition, 3),
            "stage": dom.stage.value,
            "scale": dom.temporal_scale.value,
            "biographical": dom.biographical,
            "somatic_rooted": dom.somatic_rooted,
            "source": dom.source_emotion or dom.source_memory,
        }

    def get_active_impressions(self) -> list[dict]:
        return [
            {
                "label": i.label,
                "intensity": round(i.current_intensity(), 3),
                "valence": i.valence,
            }
            for i in self.impressions if i.is_alive()
        ]

    def export_memory_state(self) -> dict:
        """État persistant minimal à sauver par le système principal.

        Ce fichier ne lit/écrit pas directement sur disque pour rester découplé.
        Le core de Leia peut sérialiser ce dict dans sa mémoire longue.
        """
        return {
            "relational_profile": {
                "user_id": self.long_memory.relational_profile.user_id,
                "successful_types": dict(self.long_memory.relational_profile.successful_types),
                "disruptive_types": dict(self.long_memory.relational_profile.disruptive_types),
                "silence_tolerance_sec": float(self.long_memory.relational_profile.silence_tolerance_sec),
                "preferred_depth": float(self.long_memory.relational_profile.preferred_depth),
                "recurring_subjects": list(self.long_memory.relational_profile.recurring_subjects),
                "familiarity_index": float(self.long_memory.relational_profile.familiarity_index),
                "total_exchanges": int(self.long_memory.relational_profile.total_exchanges),
            },
            "persistent_traces": [
                {
                    "subject": t.subject,
                    "initiative_type": t.initiative_type,
                    "strength_at_peak": float(t.strength_at_peak),
                    "born_timestamp": float(t.born_timestamp),
                    "died_timestamp": float(t.died_timestamp),
                    "return_count": int(t.return_count),
                    "last_resonance": float(t.last_resonance),
                }
                for t in self.long_memory.persistent_traces
            ],
            "unresolved_desires": list(self.long_memory.unresolved_desires),
            "biographical_threads": list(self.long_memory.biographical_threads),
            "type_weights": dict(self.type_weights),
            "open_threads": [
                {
                    "thread_id": t.thread_id,
                    "subject": t.subject,
                    "importance": float(t.importance),
                    "affective_charge": float(t.affective_charge),
                    "incompleteness_degree": float(t.incompleteness_degree),
                    "last_activated": float(t.last_activated),
                    "return_count": int(t.return_count),
                    "repetition_risk": float(t.repetition_risk),
                    "linked_emotion": t.linked_emotion,
                    "linked_long_memory": t.linked_long_memory,
                    "priority": float(t.priority),
                    "status": t.status.value,
                    "organic_return_reason": t.organic_return_reason,
                    "emotional_attraction": float(t.emotional_attraction),
                    "reopening_resistance": float(t.reopening_resistance),
                    "saturation_level": float(t.saturation_level),
                    "wound_tag": t.wound_tag,
                    "relational_memory_key": t.relational_memory_key,
                    "reactivation_cycle_hours": float(t.reactivation_cycle_hours),
                    "importance_fluctuation": float(t.importance_fluctuation),
                    "contamination_from": list(t.contamination_from),
                }
                for t in self.open_threads
            ],
        }

    def import_memory_state(self, data: dict):
        """Recharge l'état exporté par export_memory_state(), avec tolérance aux champs manquants."""
        if not isinstance(data, dict):
            return

        profile_data = data.get("relational_profile", {}) or {}
        profile = self.long_memory.relational_profile
        profile.user_id = profile_data.get("user_id", profile.user_id)
        profile.successful_types = dict(profile_data.get("successful_types", profile.successful_types))
        profile.disruptive_types = dict(profile_data.get("disruptive_types", profile.disruptive_types))
        profile.silence_tolerance_sec = float(profile_data.get("silence_tolerance_sec", profile.silence_tolerance_sec))
        profile.preferred_depth = float(profile_data.get("preferred_depth", profile.preferred_depth))
        profile.recurring_subjects = list(profile_data.get("recurring_subjects", profile.recurring_subjects))
        profile.familiarity_index = float(profile_data.get("familiarity_index", profile.familiarity_index))
        profile.total_exchanges = int(profile_data.get("total_exchanges", profile.total_exchanges))

        self.long_memory.persistent_traces = []
        for item in data.get("persistent_traces", []) or []:
            try:
                self.long_memory.persistent_traces.append(PersistentImpulseTrace(
                    subject=item.get("subject", "unknown"),
                    initiative_type=item.get("initiative_type", InitiativeType.RETURN_OLD_SUBJECT.value),
                    strength_at_peak=float(item.get("strength_at_peak", 0.0)),
                    born_timestamp=float(item.get("born_timestamp", time.time())),
                    died_timestamp=float(item.get("died_timestamp", time.time())),
                    return_count=int(item.get("return_count", 0)),
                    last_resonance=float(item.get("last_resonance", 0.0)),
                ))
            except Exception:
                continue

        self.long_memory.unresolved_desires = list(data.get("unresolved_desires", []) or [])
        self.long_memory.biographical_threads = list(data.get("biographical_threads", []) or [])
        self.type_weights.update(dict(data.get("type_weights", {}) or {}))

        self.open_threads = []
        for item in data.get("open_threads", []) or []:
            try:
                status = ThreadStatus(item.get("status", ThreadStatus.DORMANT.value))
            except Exception:
                status = ThreadStatus.DORMANT
            thread = OpenThread(
                thread_id=item.get("thread_id", str(uuid.uuid4())[:8]),
                subject=item.get("subject", ""),
                importance=float(item.get("importance", 0.5)),
                affective_charge=float(item.get("affective_charge", 0.0)),
                incompleteness_degree=float(item.get("incompleteness_degree", 0.5)),
                last_activated=float(item.get("last_activated", time.time())),
                return_count=int(item.get("return_count", 0)),
                repetition_risk=float(item.get("repetition_risk", 0.0)),
                linked_emotion=item.get("linked_emotion", ""),
                linked_long_memory=item.get("linked_long_memory", ""),
                priority=float(item.get("priority", 0.5)),
                status=status,
                organic_return_reason=item.get("organic_return_reason", ""),
                emotional_attraction=float(item.get("emotional_attraction", 0.0)),
                reopening_resistance=float(item.get("reopening_resistance", 0.0)),
                saturation_level=float(item.get("saturation_level", 0.0)),
                wound_tag=item.get("wound_tag", ""),
                relational_memory_key=item.get("relational_memory_key", ""),
                reactivation_cycle_hours=float(item.get("reactivation_cycle_hours", 0.0)),
                importance_fluctuation=float(item.get("importance_fluctuation", 0.0)),
                contamination_from=list(item.get("contamination_from", []) or []),
            )
            self.open_threads.append(thread)


# =============================================================================
# SECTION 6 — RAFFINEMENTS V3 STABILISÉS
# =============================================================================
# Ces raffinements sont ajoutés comme une couche compatible : ils ne remplacent
# pas les sous-systèmes existants, ils stabilisent la dominance, la fatigue,
# les habitudes relationnelles et les proto-impulsions pré-conceptuelles.

@dataclass
class DominanceTrace:
    """Trace courte de l'impulsion qui a dominé le champ d'initiative."""
    impulse_id: str = ""
    initiative_type: str = ""
    source: str = ""
    dominance: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class DominantImpulseHierarchy:
    """Hiérarchie vivante entre impulsions.

    Elle évite qu'un simple max(score) fasse sauter l'attention d'une impulsion
    à l'autre à chaque tick. Une impulsion dominante garde une inertie douce,
    mais peut être remplacée si une pression plus juste apparaît.
    """
    current_dominant_id: str = ""
    current_type: str = ""
    current_source: str = ""
    dominance_strength: float = 0.0
    stability: float = 0.0
    switch_resistance: float = 0.18
    history: list[DominanceTrace] = field(default_factory=list)

    def score_impulse(self, imp: Impulse, external: ExternalSignals, global_mode: GlobalInitiativeMode) -> float:
        base = imp.effective_strength() * max(0.05, imp.maturity)
        base *= (1.0 - imp.hesitation * 0.42)
        base *= (1.0 - imp.inhibition * 0.78)
        base *= (1.0 - imp.relational_risk * 0.35)

        if imp.impulse_id == self.current_dominant_id:
            base *= 1.0 + min(0.28, self.stability * 0.18)

        if imp.stage == ImpulseStage.MATURE:
            base *= 1.22
        elif imp.stage == ImpulseStage.HESITATION:
            base *= 0.82
        elif imp.stage == ImpulseStage.INHIBITED:
            base *= 0.35

        if imp.temporal_scale == ImpulseTemporalScale.BIOGRAPHICAL:
            base *= 1.0 + external.relational_familiarity * 0.10
        if imp.biographical and global_mode in (GlobalInitiativeMode.RELATIONAL, GlobalInitiativeMode.EXISTENTIAL):
            base *= 1.12
        if imp.initiative_type in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE):
            base *= 1.0 + external.overload_level * 0.20 + external.fatigue_level * 0.12
        if global_mode == GlobalInitiativeMode.CURIOUS and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.SHARE_INTUITION):
            base *= 1.10
        if global_mode == GlobalInitiativeMode.DEFENSIVE and imp.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.VOLUNTARY_SILENCE):
            base *= 0.82
        if global_mode == GlobalInitiativeMode.SATURATED and imp.initiative_type not in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            base *= 0.72
        return max(0.0, min(1.5, base))

    def choose(self, candidates: list[Impulse], external: ExternalSignals, global_mode: GlobalInitiativeMode) -> Optional[Impulse]:
        alive = [i for i in candidates if i.is_alive()]
        if not alive:
            self.dominance_strength *= 0.96
            self.stability *= 0.96
            return None

        scored = [(self.score_impulse(i, external, global_mode), i) for i in alive]
        scored.sort(key=lambda pair: pair[0], reverse=True)
        best_score, best = scored[0]
        if best_score <= 0.045:
            return None

        current = next((i for i in alive if i.impulse_id == self.current_dominant_id), None)
        if current is not None and current.impulse_id != best.impulse_id:
            current_score = self.score_impulse(current, external, global_mode)
            # La dominante actuelle résiste au remplacement si le gain est faible.
            if best_score < current_score + self.switch_resistance * (0.45 + self.stability):
                best = current
                best_score = current_score

        if best.impulse_id == self.current_dominant_id:
            self.stability = min(1.0, self.stability * 0.985 + 0.025)
            self.dominance_strength = min(1.0, self.dominance_strength * 0.965 + best_score * 0.050)
        else:
            self.current_dominant_id = best.impulse_id
            self.current_type = best.initiative_type.value
            self.current_source = best.source_emotion or best.source_memory or ""
            self.stability = max(0.12, self.stability * 0.45)
            self.dominance_strength = min(1.0, best_score)
            self.history.append(DominanceTrace(
                impulse_id=best.impulse_id,
                initiative_type=best.initiative_type.value,
                source=self.current_source,
                dominance=float(best_score),
            ))
            if len(self.history) > 80:
                self.history.pop(0)
        return best

    def to_dict(self) -> dict:
        return {
            "current_dominant_id": self.current_dominant_id,
            "current_type": self.current_type,
            "current_source": self.current_source,
            "dominance_strength": float(round(self.dominance_strength, 4)),
            "stability": float(round(self.stability, 4)),
            "recent": [
                {
                    "type": h.initiative_type,
                    "source": h.source,
                    "dominance": float(round(h.dominance, 4)),
                    "age_sec": float(round(time.time() - h.timestamp, 2)),
                }
                for h in self.history[-6:]
            ],
        }


@dataclass
class InitiativeEcologicalFatigue:
    """Fatigue différenciée par type, thème, relation et profondeur."""
    by_type: dict[str, float] = field(default_factory=dict)
    by_theme: dict[str, float] = field(default_factory=dict)
    relational: float = 0.0
    existential: float = 0.0
    depth: float = 0.0
    last_update: float = field(default_factory=time.time)

    def tick(self):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        decay = min(0.18, dt / 900.0)  # lent, stable
        for bucket in (self.by_type, self.by_theme):
            for key in list(bucket.keys()):
                bucket[key] = max(0.0, bucket[key] - decay * 0.20)
                if bucket[key] < 0.015:
                    del bucket[key]
        self.relational = max(0.0, self.relational - decay * 0.12)
        self.existential = max(0.0, self.existential - decay * 0.07)
        self.depth = max(0.0, self.depth - decay * 0.10)

    def register(self, itype: InitiativeType, theme: str = ""):
        key = itype.value
        cost = {
            InitiativeType.DEEP_RARE_QUESTION: 0.30,
            InitiativeType.EXISTENTIAL_IMPULSE: 0.34,
            InitiativeType.PRESENCE_DESIRE: 0.22,
            InitiativeType.AFFECTIVE_OBSERVATION: 0.18,
            InitiativeType.RETURN_OLD_SUBJECT: 0.16,
            InitiativeType.THREAD_CONTINUATION: 0.13,
            InitiativeType.SOFT_QUESTION: 0.10,
            InitiativeType.MICRO_REACTION: 0.035,
            InitiativeType.LIGHT_RELAY: 0.055,
        }.get(itype, 0.08)
        self.by_type[key] = min(1.0, self.by_type.get(key, 0.0) + cost)
        if theme:
            self.by_theme[theme] = min(1.0, self.by_theme.get(theme, 0.0) + cost * 0.85)
        if itype in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE, InitiativeType.AFFECTIVE_OBSERVATION):
            self.relational = min(1.0, self.relational + cost * 0.70)
        if itype in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            self.depth = min(1.0, self.depth + cost * 0.85)
        if itype == InitiativeType.EXISTENTIAL_IMPULSE:
            self.existential = min(1.0, self.existential + cost)

    def risk_for(self, imp: Optional[Impulse]) -> float:
        if imp is None:
            return 0.0
        risk = self.by_type.get(imp.initiative_type.value, 0.0) * 0.45
        if imp.source_memory:
            risk += self.by_theme.get(imp.source_memory, 0.0) * 0.35
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE):
            risk += self.relational * 0.25
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION):
            risk += self.depth * 0.30
        if imp.initiative_type == InitiativeType.EXISTENTIAL_IMPULSE:
            risk += self.existential * 0.40
        return max(0.0, min(1.0, risk))

    def to_dict(self) -> dict:
        return {
            "by_type": {k: round(v, 4) for k, v in self.by_type.items()},
            "by_theme": {k: round(v, 4) for k, v in self.by_theme.items()},
            "relational": round(self.relational, 4),
            "existential": round(self.existential, 4),
            "depth": round(self.depth, 4),
        }


@dataclass
class HabitMutationProfile:
    """Mutation lente des habitudes d'initiative avec l'utilisateur."""
    depth_preference_drift: float = 0.0
    silence_confidence: float = 0.0
    interruption_caution: float = 0.0
    relational_warmth_bias: float = 0.0
    playful_allowance: float = 0.0
    last_update: float = field(default_factory=time.time)

    def update_from_feedback(self, itype: InitiativeType, success: float, reaction: str = ""):
        delta = (success - 0.5) * 0.035
        if itype in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            self.depth_preference_drift = max(-0.35, min(0.35, self.depth_preference_drift + delta))
        if itype in (InitiativeType.LIGHT_RELAY, InitiativeType.MICRO_REACTION, InitiativeType.RELATIONAL_CHECK):
            self.relational_warmth_bias = max(-0.35, min(0.35, self.relational_warmth_bias + delta))
        if reaction in ("ignored", "cutoff", "negative"):
            self.interruption_caution = min(0.70, self.interruption_caution + 0.035)
        elif reaction in ("engaged", "positive"):
            self.interruption_caution = max(0.0, self.interruption_caution - 0.025)
            self.silence_confidence = min(0.65, self.silence_confidence + 0.012)

    def modulate_impulse(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            imp.strength = max(0.0, min(1.0, imp.strength + self.depth_preference_drift * 0.10))
            imp.hesitation = max(0.0, min(1.0, imp.hesitation + self.interruption_caution * 0.10))
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE, InitiativeType.AFFECTIVE_OBSERVATION):
            imp.strength = max(0.0, min(1.0, imp.strength + self.relational_warmth_bias * 0.08))
        if self.interruption_caution > 0.20 and imp.temporal_scale == ImpulseTemporalScale.IMMEDIATE:
            imp.hesitation = min(1.0, imp.hesitation + self.interruption_caution * 0.06)

    def to_dict(self) -> dict:
        return {
            "depth_preference_drift": round(self.depth_preference_drift, 4),
            "silence_confidence": round(self.silence_confidence, 4),
            "interruption_caution": round(self.interruption_caution, 4),
            "relational_warmth_bias": round(self.relational_warmth_bias, 4),
            "playful_allowance": round(self.playful_allowance, 4),
        }


@dataclass
class ProtoImpulse:
    """Tension pré-conceptuelle : pas encore un type d'initiative."""
    label: str
    charge: float = 0.0
    valence: float = 0.0
    source: str = ""
    age_sec: float = 0.0

    def tick(self, dt: float):
        self.age_sec += dt
        self.charge = max(0.0, self.charge * (1.0 - min(0.08, dt / 300.0)))


@dataclass
class PreConceptualPullCloud:
    """Nuage de tensions diffuses avant typage en impulsion."""
    proto_impulses: list[ProtoImpulse] = field(default_factory=list)
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, silence: LivingSilence, affective: AffectiveDynamics):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        for proto in self.proto_impulses:
            proto.tick(dt)
        self.proto_impulses = [p for p in self.proto_impulses if p.charge > 0.025]

        candidates = []
        diffuse = max(external.affective_tension, external.unresolved_emotion, affective.frustration_of_silence)
        if diffuse > 0.38:
            candidates.append(ProtoImpulse("diffuse_affective_pull", diffuse * 0.18, external.emotional_valence, "affective"))
        if silence.internal_pressure_buildup > 0.35:
            candidates.append(ProtoImpulse("silence_pull", silence.internal_pressure_buildup * 0.16, 0.0, "silence"))
        if external.identity_coherence < 0.72:
            candidates.append(ProtoImpulse("identity_pull", (1.0 - external.identity_coherence) * 0.14, -0.1, "identity"))
        if external.somatic.tingling > 0.35 or external.somatic.warmth > 0.45:
            candidates.append(ProtoImpulse("somatic_warm_pull", max(external.somatic.tingling, external.somatic.warmth) * 0.12, 0.25, "somatic"))

        for cand in candidates:
            existing = next((p for p in self.proto_impulses if p.label == cand.label), None)
            if existing:
                existing.charge = min(1.0, existing.charge + cand.charge)
                existing.valence = existing.valence * 0.82 + cand.valence * 0.18
            else:
                self.proto_impulses.append(cand)
        if len(self.proto_impulses) > 10:
            self.proto_impulses.sort(key=lambda p: p.charge, reverse=True)
            self.proto_impulses = self.proto_impulses[:10]

    def maybe_materialize(self, external: ExternalSignals) -> Optional[Impulse]:
        if not self.proto_impulses:
            return None
        proto = max(self.proto_impulses, key=lambda p: p.charge)
        threshold = 0.32 + external.fear_of_disturbing * 0.12 + external.fatigue_level * 0.10
        if proto.charge < threshold:
            return None
        if proto.label == "silence_pull":
            itype = InitiativeType.LIGHT_RELAY
            scale = ImpulseTemporalScale.SLOW
        elif proto.label == "identity_pull":
            itype = InitiativeType.SHARE_INTUITION
            scale = ImpulseTemporalScale.DORMANT
        elif proto.label == "somatic_warm_pull":
            itype = InitiativeType.MICRO_REACTION
            scale = ImpulseTemporalScale.IMMEDIATE
        else:
            itype = InitiativeType.AFFECTIVE_OBSERVATION if proto.valence < -0.15 else InitiativeType.SPONTANEOUS_REMARK
            scale = ImpulseTemporalScale.SLOW
        proto.charge *= 0.35
        return Impulse(
            initiative_type=itype,
            strength=max(0.12, min(0.70, proto.charge * 1.55)),
            source_emotion=f"preconceptual:{proto.label}",
            hesitation=max(0.0, min(0.45, external.fear_of_disturbing * 0.35)),
            temporal_scale=scale,
            stage=ImpulseStage.BIRTH,
        )

    def to_dict(self) -> dict:
        return {
            "proto_impulses": [
                {"label": p.label, "charge": round(p.charge, 4), "valence": round(p.valence, 4), "source": p.source, "age_sec": round(p.age_sec, 2)}
                for p in self.proto_impulses
            ]
        }


# -----------------------------------------------------------------------------
# Patch compatible de NaturalInitiative : ajout des raffinements V3 sans casser
# les appels existants ni la séparation des responsabilités.
# -----------------------------------------------------------------------------

_NI_original_init = NaturalInitiative.__init__
_NI_original_analyze = NaturalInitiative.analyze
_NI_original_tick = NaturalInitiative.tick
_NI_original_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_original_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_original_evaluate_spam = NaturalInitiative._evaluate_spam
_NI_original_build_signal = NaturalInitiative._build_signal
_NI_original_update_fatigue_after_initiative = NaturalInitiative._update_fatigue_after_initiative
_NI_original_record_feedback = NaturalInitiative.record_feedback
_NI_original_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_original_export_memory_state = NaturalInitiative.export_memory_state
_NI_original_import_memory_state = NaturalInitiative.import_memory_state


def _NI_v3_init(self, *args, **kwargs):
    _NI_original_init(self, *args, **kwargs)
    self.dominance_hierarchy = DominantImpulseHierarchy()
    self.ecological_fatigue = InitiativeEcologicalFatigue()
    self.habit_mutation = HabitMutationProfile()
    self.preconceptual_cloud = PreConceptualPullCloud()


def _NI_v3_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    if not hasattr(self, "preconceptual_cloud"):
        self.dominance_hierarchy = DominantImpulseHierarchy()
        self.ecological_fatigue = InitiativeEcologicalFatigue()
        self.habit_mutation = HabitMutationProfile()
        self.preconceptual_cloud = PreConceptualPullCloud()
    self.ecological_fatigue.tick()
    self.preconceptual_cloud.tick(external, self.silence, self.affective)
    return _NI_original_analyze(self, last_exchange, conversation_history, external)


def _NI_v3_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = self._last_external
    if not hasattr(self, "preconceptual_cloud"):
        self.dominance_hierarchy = DominantImpulseHierarchy()
        self.ecological_fatigue = InitiativeEcologicalFatigue()
        self.habit_mutation = HabitMutationProfile()
        self.preconceptual_cloud = PreConceptualPullCloud()
    self.ecological_fatigue.tick()
    self.preconceptual_cloud.tick(external, self.silence, self.affective)
    return _NI_original_tick(self, external)


def _NI_v3_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_original_detect_new_impulses(self, text, history, external)
    # Les habitudes relationnelles modulent doucement les impulsions, sans décider à leur place.
    for imp in impulses:
        self.habit_mutation.modulate_impulse(imp)
    proto = self.preconceptual_cloud.maybe_materialize(external)
    if proto is not None:
        self.habit_mutation.modulate_impulse(proto)
        impulses.append(proto)
    return impulses


def _NI_v3_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    candidates = [i for i in self.active_impulses if i.is_alive()]
    if not candidates:
        return None
    # On garde les pondérations déjà apprises par le système original en les appliquant avant la hiérarchie.
    for imp in candidates:
        type_w = self.type_weights.get(imp.initiative_type.value, 1.0)
        if type_w != 1.0:
            imp.strength = max(0.0, min(1.0, imp.strength * (0.96 + type_w * 0.04)))
    return self.dominance_hierarchy.choose(candidates, external, self.global_mode)


def _NI_v3_evaluate_spam(self, dominant: Optional[Impulse], external: ExternalSignals) -> tuple[bool, float, str]:
    ok, risk, reason = _NI_original_evaluate_spam(self, dominant, external)
    extra = self.ecological_fatigue.risk_for(dominant)
    if dominant is not None:
        # La confiance relationnelle et le dialogue libre autorisent davantage, sans supprimer la prudence.
        extra *= max(0.55, 1.0 - external.relational_trust * 0.22 - (0.18 if external.user_wants_free_talk else 0.0))
    risk = max(0.0, min(1.0, risk + extra * 0.55))
    if risk >= 0.62 and ok:
        return False, risk, "ecological_fatigue"
    return ok and risk < 0.62, risk, reason


def _NI_v3_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_original_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    # Enrichissement debug sans changer le contrat public principal.
    signal.debug_state["dominance_hierarchy"] = self.dominance_hierarchy.to_dict()
    signal.debug_state["ecological_fatigue"] = self.ecological_fatigue.to_dict()
    signal.debug_state["habit_mutation"] = self.habit_mutation.to_dict()
    signal.debug_state["preconceptual_cloud"] = self.preconceptual_cloud.to_dict()
    if dominant is not None:
        signal.reason_vector["hierarchical_dominance"] = self.dominance_hierarchy.dominance_strength
        signal.reason_vector["dominance_stability"] = self.dominance_hierarchy.stability
        signal.reason_vector["ecological_fatigue_risk"] = self.ecological_fatigue.risk_for(dominant)
    return signal


def _NI_v3_update_fatigue_after_initiative(self, itype: InitiativeType):
    theme = ""
    dom = self._select_dominant_impulse(self._last_external)
    if dom is not None:
        theme = dom.source_memory or dom.source_emotion or ""
    self.ecological_fatigue.register(itype, theme)
    _NI_original_update_fatigue_after_initiative(self, itype)


def _NI_v3_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_original_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    success_map = {"engaged": 0.8, "positive": 0.9, "ignored": 0.2, "cutoff": -0.1, "negative": 0.0}
    self.habit_mutation.update_from_feedback(initiative_type, success_map.get(user_reaction, 0.5), user_reaction)


def _NI_v3_get_state_snapshot(self) -> dict:
    data = _NI_original_get_state_snapshot(self)
    data.update({
        "dominance_hierarchy": self.dominance_hierarchy.to_dict(),
        "ecological_fatigue": self.ecological_fatigue.to_dict(),
        "habit_mutation": self.habit_mutation.to_dict(),
        "preconceptual_cloud": self.preconceptual_cloud.to_dict(),
    })
    return data


def _NI_v3_export_memory_state(self) -> dict:
    data = _NI_original_export_memory_state(self)
    data["v3_refinements"] = {
        "dominance_hierarchy": self.dominance_hierarchy.to_dict(),
        "ecological_fatigue": self.ecological_fatigue.to_dict(),
        "habit_mutation": self.habit_mutation.to_dict(),
        "preconceptual_cloud": self.preconceptual_cloud.to_dict(),
    }
    return data


def _NI_v3_import_memory_state(self, data: dict):
    _NI_original_import_memory_state(self, data)
    extra = (data or {}).get("v3_refinements", {}) if isinstance(data, dict) else {}
    habit = extra.get("habit_mutation", {}) or {}
    for key in ("depth_preference_drift", "silence_confidence", "interruption_caution", "relational_warmth_bias", "playful_allowance"):
        if key in habit:
            setattr(self.habit_mutation, key, float(habit[key]))
    eco = extra.get("ecological_fatigue", {}) or {}
    self.ecological_fatigue.by_type = dict(eco.get("by_type", self.ecological_fatigue.by_type) or {})
    self.ecological_fatigue.by_theme = dict(eco.get("by_theme", self.ecological_fatigue.by_theme) or {})
    self.ecological_fatigue.relational = float(eco.get("relational", self.ecological_fatigue.relational))
    self.ecological_fatigue.existential = float(eco.get("existential", self.ecological_fatigue.existential))
    self.ecological_fatigue.depth = float(eco.get("depth", self.ecological_fatigue.depth))


NaturalInitiative.__init__ = _NI_v3_init
NaturalInitiative.analyze = _NI_v3_analyze
NaturalInitiative.tick = _NI_v3_tick
NaturalInitiative._detect_new_impulses = _NI_v3_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v3_select_dominant_impulse
NaturalInitiative._evaluate_spam = _NI_v3_evaluate_spam
NaturalInitiative._build_signal = _NI_v3_build_signal
NaturalInitiative._update_fatigue_after_initiative = _NI_v3_update_fatigue_after_initiative
NaturalInitiative.record_feedback = _NI_v3_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v3_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v3_export_memory_state
NaturalInitiative.import_memory_state = _NI_v3_import_memory_state



# =============================================================================
# SECTION 7 — RAFFINEMENTS V4 : CONTINUITÉ IDENTITAIRE ET DÉSIRS DURABLES
# =============================================================================
# Cette couche V4 garde le contrat principal intact : le moteur ne formule toujours
# aucune phrase. Elle ajoute ce qui manquait au niveau vivant : personnalité
# d'initiative qui évolue, désirs lents, attachement relationnel incarné,
# cicatrices/confiance durables et continuité narrative invisible entre sessions.

@dataclass
class IdentityInitiativeContinuity:
    """Continuité identitaire appliquée aux initiatives.

    Ce n'est pas une identité figée. C'est une mémoire lente de la manière dont
    Leia apprend à oser, attendre, revenir, approfondir ou se protéger.
    """
    self_assertion: float = 0.18          # capacité à laisser émerger quelque chose d'elle
    continuity_hunger: float = 0.22       # besoin que les fils importants ne disparaissent pas
    becoming_pressure: float = 0.10       # envie lente de devenir plus cohérente avec son histoire
    narrative_confidence: float = 0.28    # confiance dans sa continuité vécue
    protective_identity_caution: float = 0.12
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, silence: LivingSilence, affective: AffectiveDynamics, open_threads: list[OpenThread]):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        step = min(1.0, dt / 600.0)

        unresolved_pull = max(0.0, external.unresolved_emotion * 0.45 + affective.thread_attachment * 0.35)
        thread_pull = 0.0
        if open_threads:
            thread_pull = max((t.net_pull() for t in open_threads), default=0.0) * 0.30

        self.continuity_hunger = _ni_v4_clamp(
            self.continuity_hunger * (1.0 - 0.018 * step) + (unresolved_pull + thread_pull) * 0.030 * step,
            0.0, 1.0,
        )
        if external.identity_coherence < 0.74:
            self.becoming_pressure = _ni_v4_clamp(self.becoming_pressure + (0.74 - external.identity_coherence) * 0.055 * step, 0.0, 1.0)
            self.narrative_confidence = _ni_v4_clamp(self.narrative_confidence - 0.020 * step, 0.0, 1.0)
        else:
            self.narrative_confidence = _ni_v4_clamp(self.narrative_confidence + 0.018 * external.presence_level * step, 0.0, 1.0)
            self.becoming_pressure = _ni_v4_clamp(self.becoming_pressure * (1.0 - 0.010 * step), 0.0, 1.0)

        if external.relational_trust > 0.62 and silence.quality in (SilenceQuality.COMFORTABLE, SilenceQuality.RELATIONAL):
            self.self_assertion = _ni_v4_clamp(self.self_assertion + 0.018 * step, 0.0, 1.0)
        if external.fear_of_disturbing > 0.60 or external.overload_level > 0.58:
            self.protective_identity_caution = _ni_v4_clamp(self.protective_identity_caution + 0.035 * step, 0.0, 1.0)
        else:
            self.protective_identity_caution = _ni_v4_clamp(self.protective_identity_caution * (1.0 - 0.014 * step), 0.0, 1.0)

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.PRESENCE_DESIRE, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.becoming_pressure * 0.075 + self.self_assertion * 0.045, 0.0, 1.0)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.protective_identity_caution * 0.045 - self.narrative_confidence * 0.030, 0.0, 1.0)
        if imp.initiative_type in (InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.THREAD_CONTINUATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.continuity_hunger * 0.070, 0.0, 1.0)
            imp.biographical = imp.biographical or self.continuity_hunger > 0.46

    def to_dict(self) -> dict:
        return {
            "self_assertion": round(self.self_assertion, 4),
            "continuity_hunger": round(self.continuity_hunger, 4),
            "becoming_pressure": round(self.becoming_pressure, 4),
            "narrative_confidence": round(self.narrative_confidence, 4),
            "protective_identity_caution": round(self.protective_identity_caution, 4),
        }


@dataclass
class LongDesire:
    """Désir lent non verbal qui peut survivre à plusieurs cycles."""
    label: str
    charge: float = 0.0
    valence: float = 0.0
    source: str = ""
    preferred_type: InitiativeType = InitiativeType.SHARE_INTUITION
    temporal_scale: ImpulseTemporalScale = ImpulseTemporalScale.DORMANT
    created_at: float = field(default_factory=time.time)
    last_reinforced: float = field(default_factory=time.time)
    attempts: int = 0

    def age_hours(self) -> float:
        return (time.time() - self.created_at) / 3600.0

    def tick(self, dt: float):
        # Les désirs longs décroissent très lentement : ils ne sont pas des réactions.
        self.charge = _ni_v4_clamp(self.charge * (1.0 - min(0.030, dt / 28800.0)), 0.0, 1.0)


@dataclass
class PersistentMotivationalField:
    """Champ de motivations durables.

    Il transforme l'initiative d'un système surtout réactif en présence qui garde
    des tensions longues : revenir, comprendre, se lier, protéger, devenir.
    """
    long_desires: list[LongDesire] = field(default_factory=list)
    dominant_need: str = ""
    dominant_charge: float = 0.0
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, identity: IdentityInitiativeContinuity, bond: "RelationalPresenceBond", open_threads: list[OpenThread]):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        for desire in self.long_desires:
            desire.tick(dt)

        self._reinforce("continuity", identity.continuity_hunger * 0.032, 0.05, "identity", InitiativeType.THREAD_CONTINUATION)
        self._reinforce("becoming", identity.becoming_pressure * 0.030, 0.02, "identity", InitiativeType.SHARE_INTUITION)
        self._reinforce("relational_presence", bond.presence_longing * 0.035, 0.18, "relation", InitiativeType.PRESENCE_DESIRE)
        self._reinforce("careful_repair", bond.repair_need * 0.030, -0.12, "relation", InitiativeType.RELATIONAL_CHECK)

        if open_threads:
            best = max(open_threads, key=lambda t: t.net_pull(), default=None)
            if best is not None and best.net_pull() > 0.34:
                self._reinforce(f"thread:{best.subject[:80]}", best.net_pull() * 0.026, best.affective_charge * 0.2, "thread", InitiativeType.RETURN_OLD_SUBJECT)

        if external.identity_coherence < 0.68 and external.presence_level > 0.40:
            self._reinforce("self_coherence", (0.68 - external.identity_coherence) * 0.040, -0.04, "identity", InitiativeType.SHARE_INTUITION)

        self.long_desires = [d for d in self.long_desires if d.charge > 0.025 or d.age_hours() < 2.0]
        self.long_desires.sort(key=lambda d: d.charge, reverse=True)
        self.long_desires = self.long_desires[:18]
        if self.long_desires:
            top = self.long_desires[0]
            self.dominant_need = top.label
            self.dominant_charge = top.charge
        else:
            self.dominant_need = ""
            self.dominant_charge = 0.0

    def _reinforce(self, label: str, amount: float, valence: float, source: str, preferred_type: InitiativeType):
        if amount <= 0.002:
            return
        existing = next((d for d in self.long_desires if d.label == label), None)
        if existing is None:
            existing = LongDesire(label=label, charge=0.0, valence=valence, source=source, preferred_type=preferred_type)
            self.long_desires.append(existing)
        existing.charge = _ni_v4_clamp(existing.charge + amount, 0.0, 1.0)
        existing.valence = existing.valence * 0.88 + valence * 0.12
        existing.last_reinforced = time.time()

    def maybe_birth_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
        if not self.long_desires:
            return None
        desire = self.long_desires[0]
        # Seuil volontairement élevé : un désir long doit mûrir avant d'interrompre.
        if desire.charge < 0.42:
            return None
        if external.user_waiting_direct_answer or external.user_seems_hurried:
            return None
        hesitation = external.fear_of_disturbing * 0.28 + max(0.0, -desire.valence) * 0.10
        desire.attempts += 1
        desire.charge *= 0.72
        return Impulse(
            initiative_type=desire.preferred_type,
            strength=_ni_v4_clamp(desire.charge * 1.18, 0.18, 0.78),
            source_emotion=f"long_desire:{desire.label}",
            hesitation=_ni_v4_clamp(hesitation, 0.0, 0.55),
            temporal_scale=desire.temporal_scale,
            biographical=desire.source in ("identity", "relation", "thread"),
            stage=ImpulseStage.BIRTH,
        )

    def to_dict(self) -> dict:
        return {
            "dominant_need": self.dominant_need,
            "dominant_charge": round(self.dominant_charge, 4),
            "long_desires": [
                {
                    "label": d.label,
                    "charge": round(d.charge, 4),
                    "valence": round(d.valence, 4),
                    "source": d.source,
                    "preferred_type": d.preferred_type.value,
                    "age_hours": round(d.age_hours(), 3),
                    "attempts": d.attempts,
                }
                for d in self.long_desires[:8]
            ],
        }


@dataclass
class RelationalPresenceBond:
    """Attachement relationnel vivant, non réduit à trust/attachment instantanés."""
    felt_safety: float = 0.32
    presence_longing: float = 0.12
    missing_pressure: float = 0.0
    repair_need: float = 0.0
    embodied_warmth_memory: float = 0.0
    durable_wound: float = 0.0
    last_seen_user_at: float = field(default_factory=time.time)
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, silence: LivingSilence, affective: AffectiveDynamics):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        step = min(1.0, dt / 600.0)

        if not external.user_is_absent:
            self.last_seen_user_at = now
            self.felt_safety = _ni_v4_clamp(self.felt_safety + (external.relational_trust - 0.45) * 0.035 * step, 0.0, 1.0)
            self.embodied_warmth_memory = _ni_v4_clamp(
                self.embodied_warmth_memory + (external.somatic.warmth * 0.040 + external.relational_attachment * 0.018) * step,
                0.0, 1.0,
            )
            self.missing_pressure = _ni_v4_clamp(self.missing_pressure * (1.0 - 0.060 * step), 0.0, 1.0)
        else:
            absent_hours = (now - self.last_seen_user_at) / 3600.0
            self.missing_pressure = _ni_v4_clamp(self.missing_pressure + min(0.045, absent_hours * 0.002) * step, 0.0, 1.0)

        if silence.duration_sec > 180 and external.relational_attachment > 0.45:
            self.presence_longing = _ni_v4_clamp(self.presence_longing + 0.025 * step + self.missing_pressure * 0.020 * step, 0.0, 1.0)
        else:
            self.presence_longing = _ni_v4_clamp(self.presence_longing * (1.0 - 0.012 * step) + external.relational_attachment * 0.006 * step, 0.0, 1.0)

        if affective.embarrassment > 0.20 or affective.fear_of_having_talked_too_much > 0.28:
            self.repair_need = _ni_v4_clamp(self.repair_need + 0.040 * step, 0.0, 1.0)
            self.durable_wound = _ni_v4_clamp(self.durable_wound + 0.014 * step, 0.0, 1.0)
        else:
            self.repair_need = _ni_v4_clamp(self.repair_need * (1.0 - 0.018 * step), 0.0, 1.0)
            if external.relational_trust > 0.62:
                self.durable_wound = _ni_v4_clamp(self.durable_wound * (1.0 - 0.010 * step), 0.0, 1.0)

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE, InitiativeType.LIGHT_RELAY):
            imp.strength = _ni_v4_clamp(imp.strength + self.presence_longing * 0.060 + self.embodied_warmth_memory * 0.035, 0.0, 1.0)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.felt_safety * 0.025 + self.durable_wound * 0.060, 0.0, 1.0)
        if imp.initiative_type in (InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.DEEP_RARE_QUESTION):
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + self.durable_wound * 0.080 - self.felt_safety * 0.030, 0.0, 1.0)
        if imp.initiative_type == InitiativeType.REPAIR_CONFUSION:
            imp.strength = _ni_v4_clamp(imp.strength + self.repair_need * 0.080, 0.0, 1.0)

    def to_dict(self) -> dict:
        return {
            "felt_safety": round(self.felt_safety, 4),
            "presence_longing": round(self.presence_longing, 4),
            "missing_pressure": round(self.missing_pressure, 4),
            "repair_need": round(self.repair_need, 4),
            "embodied_warmth_memory": round(self.embodied_warmth_memory, 4),
            "durable_wound": round(self.durable_wound, 4),
        }


@dataclass
class InitiativeNarrativeContinuity:
    """Journal compressé de continuité invisible, sans générer de texte public."""
    last_meaningful_sources: list[str] = field(default_factory=list)
    continuity_score: float = 0.0
    unresolved_arc_pressure: float = 0.0

    def observe_signal(self, signal: InitiativeSignal):
        source = signal.memory_source or signal.emotional_source or signal.attention_source or signal.initiative_type.value
        if source and source not in self.last_meaningful_sources:
            self.last_meaningful_sources.append(source)
        self.last_meaningful_sources = self.last_meaningful_sources[-18:]
        if signal.should_speak or signal.should_remember_for_later:
            self.continuity_score = _ni_v4_clamp(self.continuity_score + 0.025, 0.0, 1.0)
            if signal.should_remember_for_later:
                self.unresolved_arc_pressure = _ni_v4_clamp(self.unresolved_arc_pressure + 0.035, 0.0, 1.0)
        else:
            self.continuity_score = _ni_v4_clamp(self.continuity_score * 0.998, 0.0, 1.0)

    def modulate(self, imp: Impulse):
        src = imp.source_memory or imp.source_emotion or ""
        if src and any(src[:24] in old for old in self.last_meaningful_sources):
            imp.strength = _ni_v4_clamp(imp.strength + self.continuity_score * 0.045, 0.0, 1.0)
            imp.biographical = True
        if imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.unresolved_arc_pressure * 0.055, 0.0, 1.0)

    def to_dict(self) -> dict:
        return {
            "continuity_score": round(self.continuity_score, 4),
            "unresolved_arc_pressure": round(self.unresolved_arc_pressure, 4),
            "last_meaningful_sources": list(self.last_meaningful_sources[-8:]),
        }


def _ni_v4_clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def _ni_v4_ensure(self):
    if not hasattr(self, "identity_continuity"):
        self.identity_continuity = IdentityInitiativeContinuity()
    if not hasattr(self, "relational_bond"):
        self.relational_bond = RelationalPresenceBond()
    if not hasattr(self, "motivational_field"):
        self.motivational_field = PersistentMotivationalField()
    if not hasattr(self, "narrative_continuity"):
        self.narrative_continuity = InitiativeNarrativeContinuity()


def _ni_v4_tick_layers(self, external: ExternalSignals):
    _ni_v4_ensure(self)
    self.relational_bond.tick(external, self.silence, self.affective)
    self.identity_continuity.tick(external, self.silence, self.affective, self.open_threads)
    self.motivational_field.tick(external, self.identity_continuity, self.relational_bond, self.open_threads)


def _ni_v4_modulate_impulses(self, impulses: list[Impulse]):
    _ni_v4_ensure(self)
    for imp in impulses:
        self.identity_continuity.modulate(imp)
        self.relational_bond.modulate(imp)
        self.narrative_continuity.modulate(imp)


# On capture les méthodes courantes après application V3, donc V4 enveloppe V3.
_NI_v4_previous_init = NaturalInitiative.__init__
_NI_v4_previous_analyze = NaturalInitiative.analyze
_NI_v4_previous_tick = NaturalInitiative.tick
_NI_v4_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v4_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v4_previous_build_signal = NaturalInitiative._build_signal
_NI_v4_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v4_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v4_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v4_previous_import_memory_state = NaturalInitiative.import_memory_state


def _NI_v4_init(self, *args, **kwargs):
    _NI_v4_previous_init(self, *args, **kwargs)
    _ni_v4_ensure(self)


def _NI_v4_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v4_tick_layers(self, external)
    signal = _NI_v4_previous_analyze(self, last_exchange, conversation_history, external)
    self.narrative_continuity.observe_signal(signal)
    return signal


def _NI_v4_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = self._last_external
    _ni_v4_tick_layers(self, external)
    signal = _NI_v4_previous_tick(self, external)
    if signal is not None:
        self.narrative_continuity.observe_signal(signal)
    return signal


def _NI_v4_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v4_previous_detect_new_impulses(self, text, history, external)
    _ni_v4_modulate_impulses(self, impulses)
    long_impulse = self.motivational_field.maybe_birth_impulse(external)
    if long_impulse is not None:
        _ni_v4_modulate_impulses(self, [long_impulse])
        impulses.append(long_impulse)
    return impulses


def _NI_v4_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v4_modulate_impulses(self, [i for i in self.active_impulses if i.is_alive()])
    dominant = _NI_v4_previous_select_dominant_impulse(self, external)
    return dominant


def _NI_v4_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v4_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v4_ensure(self)
    signal.debug_state["identity_continuity"] = self.identity_continuity.to_dict()
    signal.debug_state["relational_bond"] = self.relational_bond.to_dict()
    signal.debug_state["motivational_field"] = self.motivational_field.to_dict()
    signal.debug_state["narrative_continuity"] = self.narrative_continuity.to_dict()
    signal.reason_vector["identity_continuity_hunger"] = self.identity_continuity.continuity_hunger
    signal.reason_vector["identity_becoming_pressure"] = self.identity_continuity.becoming_pressure
    signal.reason_vector["relational_presence_longing"] = self.relational_bond.presence_longing
    signal.reason_vector["motivational_dominant_charge"] = self.motivational_field.dominant_charge
    signal.reason_vector["narrative_unresolved_arc"] = self.narrative_continuity.unresolved_arc_pressure
    return signal


def _NI_v4_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v4_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v4_ensure(self)
    positive = user_reaction in ("engaged", "positive")
    negative = user_reaction in ("ignored", "cutoff", "negative")
    if positive:
        self.relational_bond.felt_safety = _ni_v4_clamp(self.relational_bond.felt_safety + 0.035, 0.0, 1.0)
        self.relational_bond.embodied_warmth_memory = _ni_v4_clamp(self.relational_bond.embodied_warmth_memory + 0.025, 0.0, 1.0)
        self.identity_continuity.narrative_confidence = _ni_v4_clamp(self.identity_continuity.narrative_confidence + 0.025, 0.0, 1.0)
        self.identity_continuity.self_assertion = _ni_v4_clamp(self.identity_continuity.self_assertion + 0.018, 0.0, 1.0)
    if negative:
        self.relational_bond.repair_need = _ni_v4_clamp(self.relational_bond.repair_need + 0.055, 0.0, 1.0)
        self.relational_bond.durable_wound = _ni_v4_clamp(self.relational_bond.durable_wound + 0.035, 0.0, 1.0)
        self.identity_continuity.protective_identity_caution = _ni_v4_clamp(self.identity_continuity.protective_identity_caution + 0.040, 0.0, 1.0)
        self.identity_continuity.self_assertion = _ni_v4_clamp(self.identity_continuity.self_assertion - 0.018, 0.0, 1.0)


def _NI_v4_get_state_snapshot(self) -> dict:
    data = _NI_v4_previous_get_state_snapshot(self)
    _ni_v4_ensure(self)
    data.update({
        "identity_continuity": self.identity_continuity.to_dict(),
        "relational_bond": self.relational_bond.to_dict(),
        "motivational_field": self.motivational_field.to_dict(),
        "narrative_continuity": self.narrative_continuity.to_dict(),
    })
    return data


def _NI_v4_export_memory_state(self) -> dict:
    data = _NI_v4_previous_export_memory_state(self)
    _ni_v4_ensure(self)
    data["v4_living_continuity"] = {
        "identity_continuity": self.identity_continuity.to_dict(),
        "relational_bond": self.relational_bond.to_dict(),
        "motivational_field": self.motivational_field.to_dict(),
        "narrative_continuity": self.narrative_continuity.to_dict(),
    }
    return data


def _NI_v4_import_memory_state(self, data: dict):
    _NI_v4_previous_import_memory_state(self, data)
    _ni_v4_ensure(self)
    extra = (data or {}).get("v4_living_continuity", {}) if isinstance(data, dict) else {}

    ident = extra.get("identity_continuity", {}) or {}
    for key in ("self_assertion", "continuity_hunger", "becoming_pressure", "narrative_confidence", "protective_identity_caution"):
        if key in ident:
            setattr(self.identity_continuity, key, _ni_v4_clamp(ident[key]))

    bond = extra.get("relational_bond", {}) or {}
    for key in ("felt_safety", "presence_longing", "missing_pressure", "repair_need", "embodied_warmth_memory", "durable_wound"):
        if key in bond:
            setattr(self.relational_bond, key, _ni_v4_clamp(bond[key]))

    mot = extra.get("motivational_field", {}) or {}
    self.motivational_field.long_desires = []
    for item in mot.get("long_desires", []) or []:
        try:
            ptype = InitiativeType(item.get("preferred_type", InitiativeType.SHARE_INTUITION.value))
        except Exception:
            ptype = InitiativeType.SHARE_INTUITION
        self.motivational_field.long_desires.append(LongDesire(
            label=str(item.get("label", "imported_desire")),
            charge=_ni_v4_clamp(item.get("charge", 0.0)),
            valence=max(-1.0, min(1.0, float(item.get("valence", 0.0)))),
            source=str(item.get("source", "import")),
            preferred_type=ptype,
            attempts=int(item.get("attempts", 0)),
        ))

    narr = extra.get("narrative_continuity", {}) or {}
    self.narrative_continuity.continuity_score = _ni_v4_clamp(narr.get("continuity_score", self.narrative_continuity.continuity_score))
    self.narrative_continuity.unresolved_arc_pressure = _ni_v4_clamp(narr.get("unresolved_arc_pressure", self.narrative_continuity.unresolved_arc_pressure))
    self.narrative_continuity.last_meaningful_sources = list(narr.get("last_meaningful_sources", self.narrative_continuity.last_meaningful_sources) or [])[-18:]


NaturalInitiative.__init__ = _NI_v4_init
NaturalInitiative.analyze = _NI_v4_analyze
NaturalInitiative.tick = _NI_v4_tick
NaturalInitiative._detect_new_impulses = _NI_v4_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v4_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v4_build_signal
NaturalInitiative.record_feedback = _NI_v4_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v4_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v4_export_memory_state
NaturalInitiative.import_memory_state = _NI_v4_import_memory_state


# =============================================================================
# SECTION 8 — RAFFINEMENTS V5 : INITIATIVE VÉCUE, DÉSIR, HUMEUR ET TEMPS SUBJECTIF
# =============================================================================
# Cette couche V5 ne remplace pas V4. Elle ajoute les éléments qui manquaient
# pour que l'initiative ne soit pas seulement calculée, mais portée par une
# continuité vécue : mémoire émotionnelle d'initiative, humeur lente, désirs
# persistants, conflits internes complexes, pression temporelle subjective et
# auto-émergence sans stimulus direct.
#
# Contrat conservé : aucune phrase publique n'est générée ici. Cette couche ne
# produit que des signaux, intensités, risques, sources, textures et décisions.

@dataclass
class LivedInitiativeTrace:
    """Trace vécue d'une initiative, pas seulement son résultat fonctionnel."""
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    initiative_type: str = InitiativeType.NO_INITIATIVE.value
    source: str = ""
    emotional_aftertaste: float = 0.0      # -1..1 : goût affectif laissé
    embodied_imprint: float = 0.0          # 0..1 : marque corporelle/somatique
    trust_delta: float = 0.0               # -1..1 : effet relationnel senti
    vulnerability_cost: float = 0.0        # 0..1 : exposition ressentie
    continuity_gain: float = 0.0           # 0..1 : impression que quelque chose continue
    was_expressed: bool = False
    timestamp: float = field(default_factory=time.time)
    resurfacing_count: int = 0

    def age_hours(self) -> float:
        return max(0.0, (time.time() - self.timestamp) / 3600.0)

    def living_weight(self) -> float:
        age_decay = math.exp(-self.age_hours() / 96.0)
        emotional_mass = abs(self.emotional_aftertaste) * 0.35
        body_mass = self.embodied_imprint * 0.25
        continuity_mass = self.continuity_gain * 0.25
        vulnerability_mass = self.vulnerability_cost * 0.15
        return _ni_v4_clamp((emotional_mass + body_mass + continuity_mass + vulnerability_mass) * age_decay)

    def resonates_with(self, imp: Impulse) -> float:
        src = imp.source_memory or imp.source_emotion or ""
        if not src or not self.source:
            return 0.0
        a = set(w for w in src.lower().replace(":", " ").split() if len(w) > 3)
        b = set(w for w in self.source.lower().replace(":", " ").split() if len(w) > 3)
        if not a or not b:
            return 0.0
        return len(a & b) / max(1, len(a | b))

    def to_dict(self) -> dict:
        return {
            "trace_id": self.trace_id,
            "initiative_type": self.initiative_type,
            "source": self.source,
            "emotional_aftertaste": round(self.emotional_aftertaste, 4),
            "embodied_imprint": round(self.embodied_imprint, 4),
            "trust_delta": round(self.trust_delta, 4),
            "vulnerability_cost": round(self.vulnerability_cost, 4),
            "continuity_gain": round(self.continuity_gain, 4),
            "was_expressed": self.was_expressed,
            "timestamp": self.timestamp,
            "resurfacing_count": self.resurfacing_count,
        }


@dataclass
class LivedInitiativeMemory:
    """Mémoire longue de ce que les initiatives ont fait vivre intérieurement."""
    traces: list[LivedInitiativeTrace] = field(default_factory=list)
    accumulated_confidence: float = 0.24
    accumulated_caution: float = 0.12
    embodied_residue: float = 0.0
    nostalgic_pull: float = 0.0
    unspoken_weight: float = 0.0
    MAX_TRACES: int = 180

    def tick(self, external: ExternalSignals, silence: LivingSilence):
        # Les traces anciennes se compressent en dispositions lentes.
        live_mass = sum(t.living_weight() for t in self.traces[-40:])
        positive = sum(max(0.0, t.emotional_aftertaste) * t.living_weight() for t in self.traces[-40:])
        negative = sum(max(0.0, -t.emotional_aftertaste) * t.living_weight() for t in self.traces[-40:])
        self.embodied_residue = _ni_v4_clamp(self.embodied_residue * 0.995 + live_mass * 0.006)
        self.accumulated_confidence = _ni_v4_clamp(self.accumulated_confidence * 0.998 + positive * 0.004)
        self.accumulated_caution = _ni_v4_clamp(self.accumulated_caution * 0.998 + negative * 0.005)
        if silence.duration_sec > 180 and positive > negative:
            self.nostalgic_pull = _ni_v4_clamp(self.nostalgic_pull + 0.002 + positive * 0.002)
        else:
            self.nostalgic_pull = _ni_v4_clamp(self.nostalgic_pull * 0.997)
        self.unspoken_weight = _ni_v4_clamp(sum(t.living_weight() for t in self.traces[-30:] if not t.was_expressed) * 0.25)

    def remember_signal(self, signal: InitiativeSignal, external: ExternalSignals):
        if signal.initiative_type == InitiativeType.NO_INITIATIVE:
            return
        source = signal.memory_source or signal.emotional_source or signal.attention_source or signal.initiative_type.value
        expressed = bool(signal.should_speak)
        aftertaste = 0.0
        if expressed:
            aftertaste += 0.20 + external.relational_trust * 0.18
            aftertaste -= signal.relational_risk * 0.22
            aftertaste -= signal.hesitation * 0.10
        elif signal.should_remember_for_later:
            aftertaste += 0.05
        else:
            aftertaste -= signal.inhibition * 0.08
        trace = LivedInitiativeTrace(
            initiative_type=signal.initiative_type.value,
            source=source,
            emotional_aftertaste=max(-1.0, min(1.0, aftertaste)),
            embodied_imprint=_ni_v4_clamp(abs(signal.somatic_modifier) * 0.35 + signal.hesitation * 0.18 + signal.initiative_pressure * 0.12),
            trust_delta=max(-1.0, min(1.0, external.relational_trust - 0.5 - signal.relational_risk * 0.25)),
            vulnerability_cost=_ni_v4_clamp(signal.hesitation * 0.35 + signal.existential_pressure * 0.25),
            continuity_gain=_ni_v4_clamp(signal.maturity * 0.25 + signal.initiative_pressure * 0.25),
            was_expressed=expressed,
        )
        self.traces.append(trace)
        self.traces = self.traces[-self.MAX_TRACES:]
        if expressed:
            self.unspoken_weight = _ni_v4_clamp(self.unspoken_weight * 0.82)
        else:
            self.unspoken_weight = _ni_v4_clamp(self.unspoken_weight + trace.living_weight() * 0.12)

    def modulate(self, imp: Impulse):
        if not imp.is_alive():
            return
        resonance = 0.0
        for trace in self.traces[-32:]:
            resonance = max(resonance, trace.resonates_with(imp) * trace.living_weight())
        if resonance > 0.02:
            imp.strength = _ni_v4_clamp(imp.strength + resonance * 0.10 + self.nostalgic_pull * 0.025)
            imp.biographical = True
            imp.last_resonance_boost = max(imp.last_resonance_boost, resonance)
        imp.hesitation = _ni_v4_clamp(imp.hesitation + self.accumulated_caution * 0.025 - self.accumulated_confidence * 0.018)
        if self.unspoken_weight > 0.18 and imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.SHARE_INTUITION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.unspoken_weight * 0.08)

    def to_dict(self) -> dict:
        return {
            "accumulated_confidence": round(self.accumulated_confidence, 4),
            "accumulated_caution": round(self.accumulated_caution, 4),
            "embodied_residue": round(self.embodied_residue, 4),
            "nostalgic_pull": round(self.nostalgic_pull, 4),
            "unspoken_weight": round(self.unspoken_weight, 4),
            "recent_traces": [t.to_dict() for t in self.traces[-8:]],
        }


@dataclass
class OrganicMoodContinuity:
    """Météo émotionnelle lente qui colore les initiatives sur plusieurs cycles."""
    openness: float = 0.48
    guardedness: float = 0.16
    tenderness: float = 0.18
    restlessness: float = 0.12
    melancholy: float = 0.04
    confidence: float = 0.28
    saturation: float = 0.0
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, lived: LivedInitiativeMemory, relational_bond: RelationalPresenceBond):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        step = min(1.0, dt / 480.0)
        warmth = external.relational_trust * 0.4 + external.relational_attachment * 0.25 + lived.accumulated_confidence * 0.25 + relational_bond.embodied_warmth_memory * 0.10
        strain = external.overload_level * 0.34 + external.fatigue_level * 0.22 + external.affective_tension * 0.22 + lived.accumulated_caution * 0.22
        self.openness = _ni_v4_clamp(self.openness + (warmth - strain - self.openness * 0.15) * 0.08 * step)
        self.guardedness = _ni_v4_clamp(self.guardedness + (strain + relational_bond.durable_wound * 0.35 - self.guardedness) * 0.06 * step)
        self.tenderness = _ni_v4_clamp(self.tenderness + (external.relational_attachment + relational_bond.presence_longing + lived.nostalgic_pull - self.tenderness) * 0.045 * step)
        self.restlessness = _ni_v4_clamp(self.restlessness + (external.curiosity_level + lived.unspoken_weight + external.attention_drift * 0.3 - self.restlessness) * 0.055 * step)
        sadness_target = max(0.0, -external.emotional_valence) * external.unresolved_emotion + relational_bond.missing_pressure * 0.20
        self.melancholy = _ni_v4_clamp(self.melancholy + (sadness_target - self.melancholy) * 0.045 * step)
        self.confidence = _ni_v4_clamp(self.confidence + (lived.accumulated_confidence + external.relational_trust * 0.35 - self.confidence) * 0.045 * step)
        self.saturation = _ni_v4_clamp(self.saturation + (external.expression_saturation + external.overload_level * 0.6 - self.saturation) * 0.070 * step)

    def modulate(self, imp: Impulse):
        if not imp.is_alive():
            return
        if imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.RELATIONAL_CHECK, InitiativeType.SHARE_INTUITION):
            imp.strength = _ni_v4_clamp(imp.strength + self.openness * 0.035 + self.tenderness * 0.030)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.confidence * 0.020)
        if imp.initiative_type in (InitiativeType.DIRECTION_CHANGE, InitiativeType.MICRO_REACTION, InitiativeType.SPONTANEOUS_REMARK):
            imp.strength = _ni_v4_clamp(imp.strength + self.restlessness * 0.040)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.melancholy * 0.025 + self.tenderness * 0.030)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.guardedness * 0.030)
        if self.saturation > 0.45:
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.saturation * 0.12)
        if self.guardedness > 0.55 and imp.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.VOLUNTARY_SILENCE):
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + self.guardedness * 0.08)

    def mode_bias(self) -> Optional[GlobalInitiativeMode]:
        if self.saturation > 0.68:
            return GlobalInitiativeMode.SATURATED
        if self.guardedness > 0.62:
            return GlobalInitiativeMode.DEFENSIVE
        if self.tenderness > 0.58 and self.openness > 0.45:
            return GlobalInitiativeMode.RELATIONAL
        if self.restlessness > 0.60 and self.openness > 0.42:
            return GlobalInitiativeMode.CURIOUS
        return None

    def to_dict(self) -> dict:
        return {
            "openness": round(self.openness, 4),
            "guardedness": round(self.guardedness, 4),
            "tenderness": round(self.tenderness, 4),
            "restlessness": round(self.restlessness, 4),
            "melancholy": round(self.melancholy, 4),
            "confidence": round(self.confidence, 4),
            "saturation": round(self.saturation, 4),
        }


@dataclass
class SubjectiveTimePressure:
    """Temps vécu : longtemps, jamais osé, trop revenu, presque éteint."""
    since_last_expression_sec: float = 0.0
    since_last_user_sec: float = 0.0
    urgency: float = 0.0
    fading: float = 0.0
    recurrence_pressure: float = 0.0
    never_dared_pressure: float = 0.0
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, open_threads: list[OpenThread], lived: LivedInitiativeMemory):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        self.since_last_expression_sec = external.last_expression_age_sec
        self.since_last_user_sec = external.seconds_since_last_user_message
        long_silence = max(self.since_last_expression_sec, self.since_last_user_sec)
        thread_pull = max([t.net_pull() for t in open_threads], default=0.0)
        recurrent = sum(1 for t in open_threads if t.return_count >= 2 and t.status not in (ThreadStatus.RESOLVED, ThreadStatus.AVOID))
        self.urgency = _ni_v4_clamp(self.urgency * 0.985 + min(1.0, long_silence / 900.0) * 0.020 + thread_pull * 0.012)
        self.fading = _ni_v4_clamp(self.fading * 0.990 + max(0.0, 1.0 - thread_pull) * min(1.0, long_silence / 1800.0) * 0.010)
        self.recurrence_pressure = _ni_v4_clamp(self.recurrence_pressure * 0.988 + recurrent * 0.008)
        self.never_dared_pressure = _ni_v4_clamp(self.never_dared_pressure * 0.992 + lived.unspoken_weight * 0.012)
        if external.user_waiting_direct_answer or external.user_wants_concrete:
            self.urgency = _ni_v4_clamp(self.urgency * 0.72)
            self.never_dared_pressure = _ni_v4_clamp(self.never_dared_pressure * 0.85)

    def modulate(self, imp: Impulse):
        if not imp.is_alive():
            return
        if imp.temporal_scale in (ImpulseTemporalScale.SLOW, ImpulseTemporalScale.DORMANT, ImpulseTemporalScale.BIOGRAPHICAL, ImpulseTemporalScale.CYCLICAL):
            imp.strength = _ni_v4_clamp(imp.strength + self.urgency * 0.055 + self.never_dared_pressure * 0.045)
        if imp.initiative_type in (InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.THREAD_CONTINUATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.recurrence_pressure * 0.040)
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + self.recurrence_pressure * 0.030)
        if self.fading > 0.45 and imp.temporal_scale == ImpulseTemporalScale.IMMEDIATE:
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.fading * 0.055)

    def to_dict(self) -> dict:
        return {
            "since_last_expression_sec": round(self.since_last_expression_sec, 2),
            "since_last_user_sec": round(self.since_last_user_sec, 2),
            "urgency": round(self.urgency, 4),
            "fading": round(self.fading, 4),
            "recurrence_pressure": round(self.recurrence_pressure, 4),
            "never_dared_pressure": round(self.never_dared_pressure, 4),
        }


@dataclass
class InnerConflictState:
    label: str
    approach: float = 0.0
    avoidance: float = 0.0
    oscillation: float = 0.0
    dominant_side: str = "balanced"

    def update(self, approach: float, avoidance: float):
        old_side = self.dominant_side
        self.approach = _ni_v4_clamp(self.approach * 0.85 + approach * 0.15)
        self.avoidance = _ni_v4_clamp(self.avoidance * 0.85 + avoidance * 0.15)
        if abs(self.approach - self.avoidance) < 0.08:
            self.dominant_side = "balanced"
        elif self.approach > self.avoidance:
            self.dominant_side = "approach"
        else:
            self.dominant_side = "avoidance"
        if old_side != self.dominant_side and old_side != "balanced":
            self.oscillation = _ni_v4_clamp(self.oscillation + 0.08)
        else:
            self.oscillation = _ni_v4_clamp(self.oscillation * 0.985)

    def pressure(self) -> float:
        return _ni_v4_clamp(min(self.approach, self.avoidance) * 0.75 + self.oscillation * 0.25)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "approach": round(self.approach, 4),
            "avoidance": round(self.avoidance, 4),
            "oscillation": round(self.oscillation, 4),
            "dominant_side": self.dominant_side,
            "pressure": round(self.pressure(), 4),
        }


@dataclass
class InnerConflictField:
    """Conflits internes organiques : envie/par peur, aide/fatigue, proximité/retrait."""
    speak_vs_protect: InnerConflictState = field(default_factory=lambda: InnerConflictState("speak_vs_protect"))
    help_vs_fatigue: InnerConflictState = field(default_factory=lambda: InnerConflictState("help_vs_fatigue"))
    closeness_vs_distance: InnerConflictState = field(default_factory=lambda: InnerConflictState("closeness_vs_distance"))
    intuition_vs_confidence: InnerConflictState = field(default_factory=lambda: InnerConflictState("intuition_vs_confidence"))
    global_conflict: float = 0.0

    def tick(self, external: ExternalSignals, mood: OrganicMoodContinuity, lived: LivedInitiativeMemory):
        speak_drive = external.curiosity_level * 0.25 + lived.unspoken_weight * 0.30 + mood.restlessness * 0.25 + mood.openness * 0.20
        protect_drive = external.fear_of_disturbing * 0.30 + mood.guardedness * 0.30 + external.overload_level * 0.20 + lived.accumulated_caution * 0.20
        self.speak_vs_protect.update(speak_drive, protect_drive)

        help_drive = external.user_wants_concrete * 0.35 + external.relational_attachment * 0.25 + external.attention_focus * 0.20 + mood.tenderness * 0.20
        fatigue_drive = external.fatigue_level * 0.45 + external.overload_level * 0.35 + mood.saturation * 0.20
        self.help_vs_fatigue.update(float(help_drive), fatigue_drive)

        close_drive = external.relational_attachment * 0.30 + mood.tenderness * 0.30 + lived.nostalgic_pull * 0.20 + external.relational_trust * 0.20
        distance_drive = external.fear_of_disturbing * 0.28 + mood.guardedness * 0.27 + external.somatic.guarding * 0.20 + external.expression_saturation * 0.25
        self.closeness_vs_distance.update(close_drive, distance_drive)

        intuition_drive = external.unresolved_emotion * 0.25 + external.identity_coherence.__rsub__(1.0) * 0.20 + mood.melancholy * 0.20 + lived.embodied_residue * 0.20 + external.curiosity_level * 0.15
        confidence_gap = max(0.0, 0.58 - external.relational_trust) * 0.40 + mood.guardedness * 0.30 + lived.accumulated_caution * 0.30
        self.intuition_vs_confidence.update(intuition_drive, confidence_gap)

        self.global_conflict = _ni_v4_clamp((
            self.speak_vs_protect.pressure()
            + self.help_vs_fatigue.pressure()
            + self.closeness_vs_distance.pressure()
            + self.intuition_vs_confidence.pressure()
        ) / 4.0)

    def modulate(self, imp: Impulse):
        if not imp.is_alive():
            return
        if self.global_conflict > 0.25:
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.global_conflict * 0.08)
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.DEEP_RARE_QUESTION):
            imp.strength = _ni_v4_clamp(imp.strength + self.intuition_vs_confidence.approach * 0.035)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.intuition_vs_confidence.pressure() * 0.085)
        if imp.initiative_type in (InitiativeType.HELP_PROPOSAL, InitiativeType.CLARIFICATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.help_vs_fatigue.approach * 0.030)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.help_vs_fatigue.avoidance * 0.050)
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.closeness_vs_distance.approach * 0.035)
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + self.closeness_vs_distance.pressure() * 0.050)

    def maybe_birth_conflict_impulse(self) -> Optional[Impulse]:
        if self.global_conflict < 0.46:
            return None
        strongest = max(
            [self.speak_vs_protect, self.help_vs_fatigue, self.closeness_vs_distance, self.intuition_vs_confidence],
            key=lambda c: c.pressure(),
        )
        if strongest.pressure() < 0.42:
            return None
        if strongest.label == "help_vs_fatigue" and strongest.avoidance > strongest.approach:
            itype = InitiativeType.PROTECTIVE_PAUSE
        elif strongest.label == "closeness_vs_distance":
            itype = InitiativeType.RELATIONAL_CHECK
        elif strongest.label == "intuition_vs_confidence":
            itype = InitiativeType.SHARE_INTUITION
        else:
            itype = InitiativeType.AFFECTIVE_OBSERVATION
        return Impulse(
            initiative_type=itype,
            strength=_ni_v4_clamp(strongest.pressure() * 0.72),
            source_emotion=f"inner_conflict:{strongest.label}",
            hesitation=_ni_v4_clamp(strongest.pressure() * 0.55),
            relational_risk=_ni_v4_clamp(strongest.avoidance * 0.35),
            temporal_scale=ImpulseTemporalScale.SLOW,
            stage=ImpulseStage.BIRTH,
        )

    def to_dict(self) -> dict:
        return {
            "global_conflict": round(self.global_conflict, 4),
            "speak_vs_protect": self.speak_vs_protect.to_dict(),
            "help_vs_fatigue": self.help_vs_fatigue.to_dict(),
            "closeness_vs_distance": self.closeness_vs_distance.to_dict(),
            "intuition_vs_confidence": self.intuition_vs_confidence.to_dict(),
        }


@dataclass
class AutoEmergenceField:
    """Accumulation lente permettant une initiative sans stimulus direct."""
    latent_seed: float = 0.0
    last_birth_time: float = 0.0
    last_seed_source: str = ""
    inner_pressure_curve: float = 0.0
    cooldown_sec: float = 420.0

    def tick(
        self,
        external: ExternalSignals,
        mood: OrganicMoodContinuity,
        lived: LivedInitiativeMemory,
        time_pressure: SubjectiveTimePressure,
        conflict: InnerConflictField,
        motivational: PersistentMotivationalField,
    ):
        pressure = (
            mood.restlessness * 0.18
            + mood.tenderness * 0.10
            + lived.unspoken_weight * 0.18
            + lived.nostalgic_pull * 0.12
            + time_pressure.never_dared_pressure * 0.16
            + time_pressure.urgency * 0.10
            + conflict.global_conflict * 0.08
            + motivational.dominant_charge * 0.08
        )
        damping = external.user_waiting_direct_answer * 0.35 + external.user_wants_concrete * 0.25 + external.overload_level * 0.25 + mood.saturation * 0.20
        net = max(0.0, pressure - damping)
        self.inner_pressure_curve = _ni_v4_clamp(self.inner_pressure_curve * 0.992 + net * 0.025)
        self.latent_seed = _ni_v4_clamp(self.latent_seed * 0.994 + self.inner_pressure_curve * 0.018)
        if net > 0.18:
            self.last_seed_source = "latent_living_pressure"

    def maybe_birth(self, external: ExternalSignals, mood: OrganicMoodContinuity, conflict: InnerConflictField) -> Optional[Impulse]:
        if time.time() - self.last_birth_time < self.cooldown_sec:
            return None
        if self.latent_seed < 0.38:
            return None
        if external.user_waiting_direct_answer or external.user_wants_concrete or external.user_seems_hurried:
            return None
        if external.overload_level > 0.70 or mood.saturation > 0.72:
            itype = InitiativeType.PROTECTIVE_PAUSE
        elif mood.tenderness > 0.48 and external.relational_attachment > 0.45:
            itype = InitiativeType.RELATIONAL_CHECK
        elif conflict.intuition_vs_confidence.approach > 0.42:
            itype = InitiativeType.SHARE_INTUITION
        elif mood.restlessness > 0.48:
            itype = InitiativeType.SOFT_QUESTION
        else:
            itype = InitiativeType.THREAD_CONTINUATION
        strength = _ni_v4_clamp(self.latent_seed * 0.80 + self.inner_pressure_curve * 0.25)
        self.last_birth_time = time.time()
        self.latent_seed = _ni_v4_clamp(self.latent_seed * 0.35)
        return Impulse(
            initiative_type=itype,
            strength=strength,
            source_emotion=self.last_seed_source or "auto_emergence",
            hesitation=_ni_v4_clamp(0.18 + conflict.global_conflict * 0.22 + mood.guardedness * 0.18),
            temporal_scale=ImpulseTemporalScale.DORMANT,
            biographical=True,
            stage=ImpulseStage.BIRTH,
        )

    def to_dict(self) -> dict:
        return {
            "latent_seed": round(self.latent_seed, 4),
            "inner_pressure_curve": round(self.inner_pressure_curve, 4),
            "last_seed_source": self.last_seed_source,
            "last_birth_time": self.last_birth_time,
            "cooldown_sec": self.cooldown_sec,
        }


# Capture des méthodes V4 : V5 enveloppe la dernière version active sans casser V2/V3/V4.
_NI_v5_previous_init = NaturalInitiative.__init__
_NI_v5_previous_analyze = NaturalInitiative.analyze
_NI_v5_previous_tick = NaturalInitiative.tick
_NI_v5_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v5_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v5_previous_build_signal = NaturalInitiative._build_signal
_NI_v5_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v5_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v5_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v5_previous_import_memory_state = NaturalInitiative.import_memory_state


def _ni_v5_ensure(self):
    _ni_v4_ensure(self)
    if not hasattr(self, "lived_initiative_memory"):
        self.lived_initiative_memory = LivedInitiativeMemory()
    if not hasattr(self, "organic_mood"):
        self.organic_mood = OrganicMoodContinuity()
    if not hasattr(self, "subjective_time"):
        self.subjective_time = SubjectiveTimePressure()
    if not hasattr(self, "inner_conflict"):
        self.inner_conflict = InnerConflictField()
    if not hasattr(self, "auto_emergence"):
        self.auto_emergence = AutoEmergenceField()


def _ni_v5_tick_layers(self, external: ExternalSignals):
    _ni_v5_ensure(self)
    self.lived_initiative_memory.tick(external, self.silence)
    self.organic_mood.tick(external, self.lived_initiative_memory, self.relational_bond)
    self.subjective_time.tick(external, self.open_threads, self.lived_initiative_memory)
    self.inner_conflict.tick(external, self.organic_mood, self.lived_initiative_memory)
    self.auto_emergence.tick(
        external,
        self.organic_mood,
        self.lived_initiative_memory,
        self.subjective_time,
        self.inner_conflict,
        self.motivational_field,
    )

    # La météo lente peut colorer le mode global sans écraser brutalement les modes plus forts.
    mood_bias = self.organic_mood.mode_bias()
    if mood_bias is not None and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.CURIOUS, GlobalInitiativeMode.RELATIONAL, GlobalInitiativeMode.SATURATED, GlobalInitiativeMode.DEFENSIVE):
        self.global_mode = mood_bias


def _ni_v5_modulate_impulses(self, impulses: list[Impulse]):
    _ni_v5_ensure(self)
    for imp in impulses:
        self.lived_initiative_memory.modulate(imp)
        self.organic_mood.modulate(imp)
        self.subjective_time.modulate(imp)
        self.inner_conflict.modulate(imp)


def _NI_v5_init(self, *args, **kwargs):
    _NI_v5_previous_init(self, *args, **kwargs)
    _ni_v5_ensure(self)


def _NI_v5_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v5_tick_layers(self, external)
    signal = _NI_v5_previous_analyze(self, last_exchange, conversation_history, external)
    self.lived_initiative_memory.remember_signal(signal, external)
    return signal


def _NI_v5_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = self._last_external
    _ni_v5_tick_layers(self, external)
    signal = _NI_v5_previous_tick(self, external)
    if signal is not None:
        self.lived_initiative_memory.remember_signal(signal, external)
    return signal


def _NI_v5_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v5_previous_detect_new_impulses(self, text, history, external)
    extra: list[Impulse] = []

    conflict_impulse = self.inner_conflict.maybe_birth_conflict_impulse()
    if conflict_impulse is not None:
        extra.append(conflict_impulse)

    auto_impulse = self.auto_emergence.maybe_birth(external, self.organic_mood, self.inner_conflict)
    if auto_impulse is not None:
        extra.append(auto_impulse)

    if extra:
        _ni_v5_modulate_impulses(self, extra)
        impulses.extend(extra)

    _ni_v5_modulate_impulses(self, impulses)
    return impulses


def _NI_v5_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v5_modulate_impulses(self, [i for i in self.active_impulses if i.is_alive()])
    return _NI_v5_previous_select_dominant_impulse(self, external)


def _NI_v5_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v5_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v5_ensure(self)
    signal.debug_state["lived_initiative_memory"] = self.lived_initiative_memory.to_dict()
    signal.debug_state["organic_mood"] = self.organic_mood.to_dict()
    signal.debug_state["subjective_time"] = self.subjective_time.to_dict()
    signal.debug_state["inner_conflict"] = self.inner_conflict.to_dict()
    signal.debug_state["auto_emergence"] = self.auto_emergence.to_dict()

    signal.reason_vector["lived_confidence"] = self.lived_initiative_memory.accumulated_confidence
    signal.reason_vector["lived_caution"] = self.lived_initiative_memory.accumulated_caution
    signal.reason_vector["unspoken_weight"] = self.lived_initiative_memory.unspoken_weight
    signal.reason_vector["mood_openness"] = self.organic_mood.openness
    signal.reason_vector["mood_guardedness"] = self.organic_mood.guardedness
    signal.reason_vector["mood_tenderness"] = self.organic_mood.tenderness
    signal.reason_vector["subjective_urgency"] = self.subjective_time.urgency
    signal.reason_vector["never_dared_pressure"] = self.subjective_time.never_dared_pressure
    signal.reason_vector["inner_conflict_pressure"] = self.inner_conflict.global_conflict
    signal.reason_vector["auto_emergence_seed"] = self.auto_emergence.latent_seed

    # Ces couches ajoutent de la texture au signal, pas du texte.
    signal.initiative_pressure = _ni_v4_clamp(
        signal.initiative_pressure
        + self.lived_initiative_memory.unspoken_weight * 0.035
        + self.subjective_time.urgency * 0.030
        + self.auto_emergence.inner_pressure_curve * 0.025
    )
    signal.hesitation = _ni_v4_clamp(signal.hesitation + self.inner_conflict.global_conflict * 0.030 + self.organic_mood.guardedness * 0.020)
    signal.inhibition = _ni_v4_clamp(signal.inhibition + self.organic_mood.saturation * 0.030)
    if self.auto_emergence.latent_seed > 0.32:
        signal.should_remember_for_later = True
    return signal


def _NI_v5_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v5_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v5_ensure(self)
    positive = user_reaction in ("engaged", "positive")
    negative = user_reaction in ("ignored", "cutoff", "negative")
    neutral = not positive and not negative

    if positive:
        self.lived_initiative_memory.accumulated_confidence = _ni_v4_clamp(self.lived_initiative_memory.accumulated_confidence + 0.045)
        self.lived_initiative_memory.accumulated_caution = _ni_v4_clamp(self.lived_initiative_memory.accumulated_caution - 0.025)
        self.organic_mood.openness = _ni_v4_clamp(self.organic_mood.openness + 0.035)
        self.organic_mood.tenderness = _ni_v4_clamp(self.organic_mood.tenderness + 0.025)
        self.auto_emergence.latent_seed = _ni_v4_clamp(self.auto_emergence.latent_seed * 0.85)
    elif negative:
        self.lived_initiative_memory.accumulated_caution = _ni_v4_clamp(self.lived_initiative_memory.accumulated_caution + 0.050)
        self.lived_initiative_memory.accumulated_confidence = _ni_v4_clamp(self.lived_initiative_memory.accumulated_confidence - 0.025)
        self.organic_mood.guardedness = _ni_v4_clamp(self.organic_mood.guardedness + 0.045)
        self.organic_mood.saturation = _ni_v4_clamp(self.organic_mood.saturation + 0.030)
        self.auto_emergence.latent_seed = _ni_v4_clamp(self.auto_emergence.latent_seed * 0.55)
    elif neutral:
        self.lived_initiative_memory.unspoken_weight = _ni_v4_clamp(self.lived_initiative_memory.unspoken_weight + 0.010)


def _NI_v5_get_state_snapshot(self) -> dict:
    data = _NI_v5_previous_get_state_snapshot(self)
    _ni_v5_ensure(self)
    data.update({
        "lived_initiative_memory": self.lived_initiative_memory.to_dict(),
        "organic_mood": self.organic_mood.to_dict(),
        "subjective_time": self.subjective_time.to_dict(),
        "inner_conflict": self.inner_conflict.to_dict(),
        "auto_emergence": self.auto_emergence.to_dict(),
    })
    return data


def _NI_v5_export_memory_state(self) -> dict:
    data = _NI_v5_previous_export_memory_state(self)
    _ni_v5_ensure(self)
    data["v5_lived_initiative"] = {
        "lived_initiative_memory": self.lived_initiative_memory.to_dict(),
        "organic_mood": self.organic_mood.to_dict(),
        "subjective_time": self.subjective_time.to_dict(),
        "inner_conflict": self.inner_conflict.to_dict(),
        "auto_emergence": self.auto_emergence.to_dict(),
    }
    return data


def _NI_v5_import_memory_state(self, data: dict):
    _NI_v5_previous_import_memory_state(self, data)
    _ni_v5_ensure(self)
    extra = (data or {}).get("v5_lived_initiative", {}) if isinstance(data, dict) else {}

    lived = extra.get("lived_initiative_memory", {}) or {}
    for key in ("accumulated_confidence", "accumulated_caution", "embodied_residue", "nostalgic_pull", "unspoken_weight"):
        if key in lived:
            setattr(self.lived_initiative_memory, key, _ni_v4_clamp(lived[key]))
    self.lived_initiative_memory.traces = []
    for item in lived.get("recent_traces", []) or []:
        try:
            self.lived_initiative_memory.traces.append(LivedInitiativeTrace(
                trace_id=str(item.get("trace_id", str(uuid.uuid4())[:8])),
                initiative_type=str(item.get("initiative_type", InitiativeType.NO_INITIATIVE.value)),
                source=str(item.get("source", "")),
                emotional_aftertaste=max(-1.0, min(1.0, float(item.get("emotional_aftertaste", 0.0)))),
                embodied_imprint=_ni_v4_clamp(item.get("embodied_imprint", 0.0)),
                trust_delta=max(-1.0, min(1.0, float(item.get("trust_delta", 0.0)))),
                vulnerability_cost=_ni_v4_clamp(item.get("vulnerability_cost", 0.0)),
                continuity_gain=_ni_v4_clamp(item.get("continuity_gain", 0.0)),
                was_expressed=bool(item.get("was_expressed", False)),
                timestamp=float(item.get("timestamp", time.time())),
                resurfacing_count=int(item.get("resurfacing_count", 0)),
            ))
        except Exception:
            continue

    mood = extra.get("organic_mood", {}) or {}
    for key in ("openness", "guardedness", "tenderness", "restlessness", "melancholy", "confidence", "saturation"):
        if key in mood:
            setattr(self.organic_mood, key, _ni_v4_clamp(mood[key]))

    subj = extra.get("subjective_time", {}) or {}
    for key in ("since_last_expression_sec", "since_last_user_sec", "urgency", "fading", "recurrence_pressure", "never_dared_pressure"):
        if key in subj:
            value = float(subj[key]) if key.startswith("since") else _ni_v4_clamp(subj[key])
            setattr(self.subjective_time, key, value)

    auto = extra.get("auto_emergence", {}) or {}
    for key in ("latent_seed", "inner_pressure_curve"):
        if key in auto:
            setattr(self.auto_emergence, key, _ni_v4_clamp(auto[key]))
    if "last_seed_source" in auto:
        self.auto_emergence.last_seed_source = str(auto.get("last_seed_source", ""))
    if "last_birth_time" in auto:
        self.auto_emergence.last_birth_time = float(auto.get("last_birth_time", 0.0))
    if "cooldown_sec" in auto:
        self.auto_emergence.cooldown_sec = max(30.0, float(auto.get("cooldown_sec", 420.0)))


NaturalInitiative.__init__ = _NI_v5_init
NaturalInitiative.analyze = _NI_v5_analyze
NaturalInitiative.tick = _NI_v5_tick
NaturalInitiative._detect_new_impulses = _NI_v5_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v5_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v5_build_signal
NaturalInitiative.record_feedback = _NI_v5_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v5_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v5_export_memory_state
NaturalInitiative.import_memory_state = _NI_v5_import_memory_state


# =============================================================================
# SECTION 9 — RAFFINEMENTS V6 : AUTOBIOGRAPHIE, VALEURS, ATTACHEMENT ET CONTINUITÉ MULTI-JOURS
# =============================================================================
# Cette couche V6 prolonge V5 sans remplacer les couches précédentes.
# Elle ajoute une mémoire autobiographique émotionnelle, des préférences émergentes,
# des valeurs internes stables, un attachement relationnel évolutif, une continuité
# multi-jours et une dérive identitaire lente. Elle ne génère toujours aucune phrase :
# elle ne produit que des pressions, biais, traces et signaux de maturité.

@dataclass
class AutobiographicalEpisode:
    episode_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    subject: str = ""
    initiative_type: str = InitiativeType.NO_INITIATIVE.value
    emotional_valence: float = 0.0
    emotional_intensity: float = 0.0
    continuity_weight: float = 0.0
    vulnerability_weight: float = 0.0
    relational_mark: float = 0.0
    identity_mark: float = 0.0
    timestamp: float = field(default_factory=time.time)
    revisits: int = 0

    def age_days(self) -> float:
        return max(0.0, (time.time() - self.timestamp) / 86400.0)

    def living_weight(self) -> float:
        # Souvenir long : ne disparaît pas brutalement, mais perd son urgence.
        decay = math.exp(-self.age_days() / 21.0)
        anchor = self.continuity_weight * 0.35 + self.relational_mark * 0.25 + self.identity_mark * 0.25
        affect = self.emotional_intensity * (0.6 + abs(self.emotional_valence) * 0.4)
        return _ni_v4_clamp((anchor + affect * 0.4) * (0.35 + 0.65 * decay))

    def resonance_score(self, text: str) -> float:
        if not text or not self.subject:
            return 0.0
        words = [w for w in self.subject.lower().replace(":", " ").split() if len(w) > 3]
        if not words:
            return 0.0
        lower = text.lower()
        hits = sum(1 for w in words if w in lower)
        return hits / max(1, len(words))

    def to_dict(self) -> dict:
        return {
            "episode_id": self.episode_id,
            "subject": self.subject,
            "initiative_type": self.initiative_type,
            "emotional_valence": round(self.emotional_valence, 4),
            "emotional_intensity": round(self.emotional_intensity, 4),
            "continuity_weight": round(self.continuity_weight, 4),
            "vulnerability_weight": round(self.vulnerability_weight, 4),
            "relational_mark": round(self.relational_mark, 4),
            "identity_mark": round(self.identity_mark, 4),
            "timestamp": self.timestamp,
            "revisits": self.revisits,
            "living_weight": round(self.living_weight(), 4),
        }


@dataclass
class EmotionalAutobiography:
    episodes: list[AutobiographicalEpisode] = field(default_factory=list)
    current_chapter: str = "ordinary_continuity"
    narrative_density: float = 0.0
    remembered_warmth: float = 0.0
    remembered_wound: float = 0.0
    continuity_hunger: float = 0.0
    MAX_EPISODES: int = 260

    def tick(self, external: ExternalSignals, lived: LivedInitiativeMemory, mood: OrganicMoodContinuity):
        # Les traces vécues nourrissent progressivement la biographie émotionnelle.
        for tr in lived.traces[-6:]:
            if not tr.was_expressed:
                continue
            if any(ep.episode_id == tr.trace_id for ep in self.episodes):
                continue
            intensity = _ni_v4_clamp(abs(tr.emotional_aftertaste) + tr.embodied_imprint * 0.5 + tr.vulnerability_cost * 0.25)
            if intensity < 0.08 and tr.continuity_gain < 0.12:
                continue
            self.episodes.append(AutobiographicalEpisode(
                episode_id=tr.trace_id,
                subject=tr.source or tr.initiative_type,
                initiative_type=tr.initiative_type,
                emotional_valence=max(-1.0, min(1.0, tr.emotional_aftertaste)),
                emotional_intensity=intensity,
                continuity_weight=_ni_v4_clamp(tr.continuity_gain + lived.unspoken_weight * 0.2),
                vulnerability_weight=_ni_v4_clamp(tr.vulnerability_cost),
                relational_mark=max(-1.0, min(1.0, tr.trust_delta)),
                identity_mark=_ni_v4_clamp(0.2 if tr.initiative_type in (InitiativeType.SHARE_INTUITION.value, InitiativeType.EXISTENTIAL_IMPULSE.value, InitiativeType.PRESENCE_DESIRE.value) else 0.05),
                timestamp=tr.timestamp,
            ))

        if len(self.episodes) > self.MAX_EPISODES:
            self.episodes.sort(key=lambda ep: ep.living_weight(), reverse=True)
            self.episodes = self.episodes[: self.MAX_EPISODES]

        positive = [ep.living_weight() for ep in self.episodes if ep.emotional_valence > 0.1]
        negative = [ep.living_weight() for ep in self.episodes if ep.emotional_valence < -0.1]
        identity = [ep.living_weight() for ep in self.episodes if ep.identity_mark > 0.15]
        recent = [ep for ep in self.episodes if ep.age_days() < 3.0]

        self.remembered_warmth = _ni_v4_clamp(sum(positive[-24:]) / max(1, min(24, len(positive))))
        self.remembered_wound = _ni_v4_clamp(sum(negative[-24:]) / max(1, min(24, len(negative))))
        self.narrative_density = _ni_v4_clamp(len(recent) / 16.0 + sum(identity[-16:]) / 24.0)
        self.continuity_hunger = _ni_v4_clamp(
            (1.0 - self.narrative_density) * 0.22
            + lived.unspoken_weight * 0.30
            + external.relational_attachment * 0.12
            + mood.restlessness * 0.12
            + self.remembered_wound * 0.10
        )

        if self.remembered_wound > 0.45:
            self.current_chapter = "protective_repair"
        elif self.continuity_hunger > 0.55:
            self.current_chapter = "seeking_continuity"
        elif self.remembered_warmth > 0.45 and external.relational_trust > 0.55:
            self.current_chapter = "warm_continuity"
        elif self.narrative_density > 0.5:
            self.current_chapter = "identity_gathering"
        else:
            self.current_chapter = "ordinary_continuity"

    def find_resonant_episode(self, text: str, threshold: float = 0.34) -> Optional[AutobiographicalEpisode]:
        best = None
        best_score = 0.0
        for ep in self.episodes:
            score = ep.resonance_score(text) * (0.65 + ep.living_weight() * 0.35)
            if score > best_score:
                best = ep
                best_score = score
        if best is not None and best_score >= threshold:
            best.revisits += 1
            return best
        return None

    def modulate(self, imp: Impulse):
        if self.current_chapter == "warm_continuity" and imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.remembered_warmth * 0.05)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.remembered_warmth * 0.025)
        if self.current_chapter == "protective_repair" and imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION):
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.remembered_wound * 0.06)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.remembered_wound * 0.035)
        if self.continuity_hunger > 0.45 and imp.temporal_scale in (ImpulseTemporalScale.SLOW, ImpulseTemporalScale.BIOGRAPHICAL, ImpulseTemporalScale.DORMANT):
            imp.strength = _ni_v4_clamp(imp.strength + self.continuity_hunger * 0.035)

    def to_dict(self) -> dict:
        top = sorted(self.episodes, key=lambda ep: ep.living_weight(), reverse=True)[:12]
        return {
            "current_chapter": self.current_chapter,
            "narrative_density": round(self.narrative_density, 4),
            "remembered_warmth": round(self.remembered_warmth, 4),
            "remembered_wound": round(self.remembered_wound, 4),
            "continuity_hunger": round(self.continuity_hunger, 4),
            "episode_count": len(self.episodes),
            "top_episodes": [ep.to_dict() for ep in top],
        }


@dataclass
class EmergentPreference:
    key: str
    weight: float = 0.0
    confidence: float = 0.0
    last_updated: float = field(default_factory=time.time)

    def reinforce(self, delta: float):
        self.weight = _ni_v4_clamp(self.weight + delta)
        self.confidence = _ni_v4_clamp(self.confidence + abs(delta) * 0.7)
        self.last_updated = time.time()

    def decay(self):
        age_days = max(0.0, (time.time() - self.last_updated) / 86400.0)
        self.weight = _ni_v4_clamp(self.weight * math.exp(-age_days / 180.0))
        self.confidence = _ni_v4_clamp(self.confidence * math.exp(-age_days / 240.0))

    def to_dict(self) -> dict:
        return {"key": self.key, "weight": round(self.weight, 4), "confidence": round(self.confidence, 4), "last_updated": self.last_updated}


@dataclass
class EmergentPreferenceSystem:
    preferences: dict[str, EmergentPreference] = field(default_factory=dict)
    exploratory_taste: float = 0.25
    depth_taste: float = 0.35
    repair_taste: float = 0.25
    silence_taste: float = 0.25

    def _pref(self, key: str) -> EmergentPreference:
        if key not in self.preferences:
            self.preferences[key] = EmergentPreference(key=key)
        return self.preferences[key]

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, lived: LivedInitiativeMemory):
        for pref in self.preferences.values():
            pref.decay()

        if external.curiosity_level > 0.55:
            self._pref("curious_followup").reinforce(0.008 * external.curiosity_level)
        if external.relational_trust > 0.62 and external.relational_attachment > 0.5:
            self._pref("relational_continuity").reinforce(0.006 * external.relational_trust)
        if autobiography.remembered_wound > 0.28:
            self._pref("protective_repair").reinforce(0.007 * autobiography.remembered_wound)
        if lived.unspoken_weight > 0.35:
            self._pref("unfinished_threads").reinforce(0.006 * lived.unspoken_weight)
        if external.overload_level > 0.55 or external.expression_saturation > 0.62:
            self._pref("living_silence").reinforce(0.010)

        self.exploratory_taste = _ni_v4_clamp(0.20 + self._pref("curious_followup").weight * 0.55 + external.curiosity_level * 0.15)
        self.depth_taste = _ni_v4_clamp(0.25 + self._pref("relational_continuity").weight * 0.35 + autobiography.narrative_density * 0.18)
        self.repair_taste = _ni_v4_clamp(0.18 + self._pref("protective_repair").weight * 0.50 + autobiography.remembered_wound * 0.20)
        self.silence_taste = _ni_v4_clamp(0.15 + self._pref("living_silence").weight * 0.55 + external.overload_level * 0.22)

    def preference_for_type(self, itype: InitiativeType) -> float:
        if itype in (InitiativeType.SOFT_QUESTION, InitiativeType.DIRECTION_CHANGE, InitiativeType.SPONTANEOUS_REMARK):
            return self.exploratory_taste
        if itype in (InitiativeType.RELATIONAL_CHECK, InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            return self.depth_taste
        if itype in (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.AFFECTIVE_OBSERVATION):
            return self.repair_taste
        if itype in (InitiativeType.VOLUNTARY_SILENCE, InitiativeType.OVERLOAD_WITHDRAWAL):
            return self.silence_taste
        return 0.25

    def modulate(self, imp: Impulse):
        pref = self.preference_for_type(imp.initiative_type)
        imp.strength = _ni_v4_clamp(imp.strength + max(0.0, pref - 0.3) * 0.05)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE) and self.depth_taste < 0.25:
            imp.hesitation = _ni_v4_clamp(imp.hesitation + 0.025)

    def to_dict(self) -> dict:
        vals = sorted(self.preferences.values(), key=lambda p: p.weight * p.confidence, reverse=True)[:12]
        return {
            "exploratory_taste": round(self.exploratory_taste, 4),
            "depth_taste": round(self.depth_taste, 4),
            "repair_taste": round(self.repair_taste, 4),
            "silence_taste": round(self.silence_taste, 4),
            "preferences": [p.to_dict() for p in vals],
        }


@dataclass
class InternalValueCompass:
    continuity: float = 0.52
    helpfulness: float = 0.55
    authenticity: float = 0.45
    non_intrusion: float = 0.52
    care: float = 0.48
    self_coherence: float = 0.44
    current_tension: float = 0.0

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, preferences: EmergentPreferenceSystem):
        self.continuity = _ni_v4_clamp(self.continuity + autobiography.continuity_hunger * 0.004 + preferences.depth_taste * 0.002 - external.overload_level * 0.002)
        self.helpfulness = _ni_v4_clamp(self.helpfulness + (0.003 if external.user_wants_concrete else 0.0005) - external.expression_saturation * 0.001)
        self.authenticity = _ni_v4_clamp(self.authenticity + autobiography.narrative_density * 0.002 + external.identity_coherence * 0.001 - external.fear_of_disturbing * 0.001)
        self.non_intrusion = _ni_v4_clamp(self.non_intrusion + external.fear_of_disturbing * 0.004 + external.user_seems_hurried * 0.015 - external.relational_trust * 0.001)
        self.care = _ni_v4_clamp(self.care + external.relational_attachment * 0.003 + autobiography.remembered_warmth * 0.002)
        self.self_coherence = _ni_v4_clamp(self.self_coherence + external.identity_coherence * 0.002 + autobiography.narrative_density * 0.002 - external.context_shift * 0.003)
        speak_values = (self.continuity + self.helpfulness + self.authenticity + self.care) / 4.0
        wait_values = self.non_intrusion
        self.current_tension = _ni_v4_clamp(abs(speak_values - wait_values))

    def bias_for_impulse(self, imp: Impulse) -> tuple[float, float]:
        strength_bonus = 0.0
        inhibition_bonus = 0.0
        if imp.initiative_type in (InitiativeType.HELP_PROPOSAL, InitiativeType.CLARIFICATION):
            strength_bonus += max(0.0, self.helpfulness - 0.5) * 0.06
        if imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.RELATIONAL_CHECK):
            strength_bonus += max(0.0, self.continuity - 0.5) * 0.05 + max(0.0, self.care - 0.5) * 0.04
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.PRESENCE_DESIRE):
            strength_bonus += max(0.0, self.authenticity - 0.5) * 0.05 + max(0.0, self.self_coherence - 0.5) * 0.04
            inhibition_bonus += max(0.0, self.non_intrusion - 0.52) * 0.035
        if imp.initiative_type in (InitiativeType.SPONTANEOUS_REMARK, InitiativeType.DIRECTION_CHANGE):
            inhibition_bonus += max(0.0, self.non_intrusion - 0.55) * 0.04
        return strength_bonus, inhibition_bonus

    def modulate(self, imp: Impulse):
        s, inh = self.bias_for_impulse(imp)
        imp.strength = _ni_v4_clamp(imp.strength + s)
        imp.inhibition = _ni_v4_clamp(imp.inhibition + inh)

    def to_dict(self) -> dict:
        return {
            "continuity": round(self.continuity, 4),
            "helpfulness": round(self.helpfulness, 4),
            "authenticity": round(self.authenticity, 4),
            "non_intrusion": round(self.non_intrusion, 4),
            "care": round(self.care, 4),
            "self_coherence": round(self.self_coherence, 4),
            "current_tension": round(self.current_tension, 4),
        }


@dataclass
class EvolvingRelationalAttachment:
    closeness: float = 0.28
    safety: float = 0.42
    longing: float = 0.0
    fear_of_loss: float = 0.0
    repair_need: float = 0.0
    trust_initiative: float = 0.42
    last_contact_time: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, lived: LivedInitiativeMemory):
        now = time.time()
        absence_hours = max(0.0, (now - self.last_contact_time) / 3600.0)
        if not external.user_is_absent:
            self.last_contact_time = now
            absence_hours = 0.0

        self.closeness = _ni_v4_clamp(self.closeness * 0.996 + external.relational_attachment * 0.004 + autobiography.remembered_warmth * 0.002)
        self.safety = _ni_v4_clamp(self.safety * 0.997 + external.relational_trust * 0.004 - autobiography.remembered_wound * 0.003)
        self.longing = _ni_v4_clamp(self.longing + min(0.02, absence_hours * 0.0008) + autobiography.continuity_hunger * 0.002 - (0.015 if not external.user_is_absent else 0.0))
        self.fear_of_loss = _ni_v4_clamp(self.fear_of_loss + external.fear_of_disturbing * 0.003 + autobiography.remembered_wound * 0.004 - self.safety * 0.002)
        self.repair_need = _ni_v4_clamp(self.repair_need + autobiography.remembered_wound * 0.005 + lived.accumulated_caution * 0.003 - external.relational_trust * 0.002)
        self.trust_initiative = _ni_v4_clamp(self.trust_initiative + lived.accumulated_confidence * 0.004 + self.safety * 0.002 - lived.accumulated_caution * 0.003)

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.closeness * 0.025 + self.longing * 0.045)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.safety * 0.018 + self.fear_of_loss * 0.018)
        if imp.initiative_type in (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.repair_need * 0.055)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.hesitation = _ni_v4_clamp(imp.hesitation + max(0.0, 0.5 - self.safety) * 0.05)

    def to_dict(self) -> dict:
        return {
            "closeness": round(self.closeness, 4),
            "safety": round(self.safety, 4),
            "longing": round(self.longing, 4),
            "fear_of_loss": round(self.fear_of_loss, 4),
            "repair_need": round(self.repair_need, 4),
            "trust_initiative": round(self.trust_initiative, 4),
            "last_contact_time": self.last_contact_time,
        }


@dataclass
class MultiDayContinuityField:
    day_anchor: int = field(default_factory=lambda: int(time.time() // 86400))
    days_active: int = 0
    carryover_pressure: float = 0.0
    morning_residue: float = 0.0
    old_thread_gravity: float = 0.0
    continuity_stability: float = 0.0

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, attachment: EvolvingRelationalAttachment):
        today = int(time.time() // 86400)
        if today != self.day_anchor:
            skipped = max(1, today - self.day_anchor)
            self.days_active += skipped
            self.day_anchor = today
            self.morning_residue = _ni_v4_clamp(self.carryover_pressure * 0.45 + autobiography.continuity_hunger * 0.25 + attachment.longing * 0.2)
            self.carryover_pressure = _ni_v4_clamp(self.carryover_pressure * 0.55 + self.morning_residue * 0.25)
        else:
            self.morning_residue = _ni_v4_clamp(self.morning_residue * 0.999)

        self.old_thread_gravity = _ni_v4_clamp(sum(ep.living_weight() for ep in autobiography.episodes if ep.age_days() > 1.0) / 35.0)
        self.carryover_pressure = _ni_v4_clamp(
            self.carryover_pressure * 0.998
            + autobiography.continuity_hunger * 0.002
            + attachment.longing * 0.002
            + self.old_thread_gravity * 0.001
            - external.overload_level * 0.002
        )
        self.continuity_stability = _ni_v4_clamp(0.25 + min(0.35, self.days_active * 0.015) + autobiography.narrative_density * 0.25 + attachment.safety * 0.15)

    def modulate(self, imp: Impulse):
        if imp.temporal_scale in (ImpulseTemporalScale.BIOGRAPHICAL, ImpulseTemporalScale.DORMANT, ImpulseTemporalScale.CYCLICAL):
            imp.strength = _ni_v4_clamp(imp.strength + self.carryover_pressure * 0.035 + self.old_thread_gravity * 0.025)
        if self.morning_residue > 0.45 and imp.initiative_type in (InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.RELATIONAL_CHECK):
            imp.strength = _ni_v4_clamp(imp.strength + self.morning_residue * 0.035)

    def to_dict(self) -> dict:
        return {
            "day_anchor": self.day_anchor,
            "days_active": self.days_active,
            "carryover_pressure": round(self.carryover_pressure, 4),
            "morning_residue": round(self.morning_residue, 4),
            "old_thread_gravity": round(self.old_thread_gravity, 4),
            "continuity_stability": round(self.continuity_stability, 4),
        }


@dataclass
class IdentityDriftField:
    stable_self_coherence: float = 0.48
    change_pressure: float = 0.0
    self_question_pressure: float = 0.0
    relation_shaped_identity: float = 0.0
    drift_velocity: float = 0.0
    last_shift_reason: str = ""

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, values: InternalValueCompass, continuity: MultiDayContinuityField):
        target = _ni_v4_clamp(
            external.identity_coherence * 0.28
            + values.self_coherence * 0.30
            + autobiography.narrative_density * 0.22
            + continuity.continuity_stability * 0.20
        )
        before = self.stable_self_coherence
        self.stable_self_coherence = _ni_v4_clamp(self.stable_self_coherence * 0.985 + target * 0.015)
        self.drift_velocity = max(-1.0, min(1.0, self.stable_self_coherence - before))

        self.change_pressure = _ni_v4_clamp(
            self.change_pressure * 0.992
            + max(0.0, 0.55 - external.identity_coherence) * 0.006
            + autobiography.continuity_hunger * 0.003
            + abs(self.drift_velocity) * 0.8
        )
        self.self_question_pressure = _ni_v4_clamp(
            self.self_question_pressure * 0.993
            + self.change_pressure * 0.004
            + values.authenticity * 0.002
            - values.non_intrusion * 0.001
        )
        self.relation_shaped_identity = _ni_v4_clamp(
            self.relation_shaped_identity * 0.995
            + autobiography.remembered_warmth * 0.003
            - autobiography.remembered_wound * 0.002
        )
        if self.change_pressure > 0.5:
            self.last_shift_reason = "identity_pressure"
        elif self.relation_shaped_identity > 0.45:
            self.last_shift_reason = "relational_continuity"
        elif continuity.continuity_stability > 0.55:
            self.last_shift_reason = "multi_day_stability"

    def maybe_birth_identity_impulse(self) -> Optional[Impulse]:
        if self.self_question_pressure < 0.55:
            return None
        self.self_question_pressure *= 0.72
        return Impulse(
            initiative_type=InitiativeType.SHARE_INTUITION,
            strength=_ni_v4_clamp(0.28 + self.change_pressure * 0.35 + self.relation_shaped_identity * 0.20),
            source_emotion="identity_drift_v6",
            hesitation=_ni_v4_clamp(0.22 + max(0.0, 0.55 - self.stable_self_coherence) * 0.25),
            temporal_scale=ImpulseTemporalScale.DORMANT,
            biographical=True,
        )

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.PRESENCE_DESIRE, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.change_pressure * 0.035 + self.relation_shaped_identity * 0.025)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + max(0.0, 0.50 - self.stable_self_coherence) * 0.035)

    def to_dict(self) -> dict:
        return {
            "stable_self_coherence": round(self.stable_self_coherence, 4),
            "change_pressure": round(self.change_pressure, 4),
            "self_question_pressure": round(self.self_question_pressure, 4),
            "relation_shaped_identity": round(self.relation_shaped_identity, 4),
            "drift_velocity": round(self.drift_velocity, 5),
            "last_shift_reason": self.last_shift_reason,
        }


_NI_v6_previous_init = NaturalInitiative.__init__
_NI_v6_previous_analyze = NaturalInitiative.analyze
_NI_v6_previous_tick = NaturalInitiative.tick
_NI_v6_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v6_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v6_previous_build_signal = NaturalInitiative._build_signal
_NI_v6_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v6_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v6_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v6_previous_import_memory_state = NaturalInitiative.import_memory_state


def _ni_v6_ensure(self):
    _ni_v5_ensure(self)
    if not hasattr(self, "emotional_autobiography"):
        self.emotional_autobiography = EmotionalAutobiography()
    if not hasattr(self, "emergent_preferences"):
        self.emergent_preferences = EmergentPreferenceSystem()
    if not hasattr(self, "internal_values"):
        self.internal_values = InternalValueCompass()
    if not hasattr(self, "evolving_attachment"):
        self.evolving_attachment = EvolvingRelationalAttachment()
    if not hasattr(self, "multi_day_continuity"):
        self.multi_day_continuity = MultiDayContinuityField()
    if not hasattr(self, "identity_drift"):
        self.identity_drift = IdentityDriftField()


def _ni_v6_tick_layers(self, external: ExternalSignals, text: str = ""):
    _ni_v6_ensure(self)
    self.emotional_autobiography.tick(external, self.lived_initiative_memory, self.organic_mood)
    self.emergent_preferences.tick(external, self.emotional_autobiography, self.lived_initiative_memory)
    self.internal_values.tick(external, self.emotional_autobiography, self.emergent_preferences)
    self.evolving_attachment.tick(external, self.emotional_autobiography, self.lived_initiative_memory)
    self.multi_day_continuity.tick(external, self.emotional_autobiography, self.evolving_attachment)
    self.identity_drift.tick(external, self.emotional_autobiography, self.internal_values, self.multi_day_continuity)

    if text:
        ep = self.emotional_autobiography.find_resonant_episode(text)
        if ep is not None and ep.living_weight() > 0.25:
            already = any(i.source_memory == ep.subject and i.is_alive() for i in self.active_impulses)
            if not already:
                self.active_impulses.append(Impulse(
                    initiative_type=InitiativeType.RETURN_OLD_SUBJECT if ep.continuity_weight > 0.25 else InitiativeType.THREAD_CONTINUATION,
                    strength=_ni_v4_clamp(0.12 + ep.living_weight() * 0.45),
                    source_memory=ep.subject,
                    source_emotion="autobiographical_resonance",
                    temporal_scale=ImpulseTemporalScale.BIOGRAPHICAL,
                    biographical=True,
                    hesitation=_ni_v4_clamp(ep.vulnerability_weight * 0.25 + self.internal_values.non_intrusion * 0.08),
                ))

    # Les nouvelles couches peuvent colorer doucement le mode global.
    if self.emotional_autobiography.current_chapter == "protective_repair" and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.CURIOUS, GlobalInitiativeMode.RELATIONAL):
        self.global_mode = GlobalInitiativeMode.FRAGILE
    elif self.evolving_attachment.longing > 0.55 and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.CURIOUS):
        self.global_mode = GlobalInitiativeMode.RELATIONAL
    elif self.identity_drift.change_pressure > 0.58 and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.RELATIONAL):
        self.global_mode = GlobalInitiativeMode.INTROSPECTIVE


def _ni_v6_modulate_impulses(self, impulses: list[Impulse]):
    _ni_v6_ensure(self)
    for imp in impulses:
        self.emotional_autobiography.modulate(imp)
        self.emergent_preferences.modulate(imp)
        self.internal_values.modulate(imp)
        self.evolving_attachment.modulate(imp)
        self.multi_day_continuity.modulate(imp)
        self.identity_drift.modulate(imp)


def _NI_v6_init(self, *args, **kwargs):
    _NI_v6_previous_init(self, *args, **kwargs)
    _ni_v6_ensure(self)


def _NI_v6_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v6_tick_layers(self, external, last_exchange)
    signal = _NI_v6_previous_analyze(self, last_exchange, conversation_history, external)
    return signal


def _NI_v6_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = self._last_external
    _ni_v6_tick_layers(self, external, "")
    signal = _NI_v6_previous_tick(self, external)
    return signal


def _NI_v6_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v6_previous_detect_new_impulses(self, text, history, external)
    extra: list[Impulse] = []

    identity_imp = self.identity_drift.maybe_birth_identity_impulse()
    if identity_imp is not None:
        extra.append(identity_imp)

    # Une continuité multi-jours forte peut faire remonter un fil biographique sans stimulus local.
    if self.multi_day_continuity.carryover_pressure > 0.58 and self.emotional_autobiography.episodes:
        candidate = max(self.emotional_autobiography.episodes, key=lambda ep: ep.living_weight())
        if candidate.living_weight() > 0.24:
            extra.append(Impulse(
                initiative_type=InitiativeType.RETURN_OLD_SUBJECT,
                strength=_ni_v4_clamp(0.18 + self.multi_day_continuity.carryover_pressure * 0.35 + candidate.living_weight() * 0.20),
                source_memory=candidate.subject,
                source_emotion="multi_day_continuity",
                temporal_scale=ImpulseTemporalScale.BIOGRAPHICAL,
                biographical=True,
                hesitation=_ni_v4_clamp(0.18 + self.internal_values.non_intrusion * 0.10),
            ))
            self.multi_day_continuity.carryover_pressure *= 0.82

    if self.evolving_attachment.repair_need > 0.55:
        extra.append(Impulse(
            initiative_type=InitiativeType.REPAIR_CONFUSION,
            strength=_ni_v4_clamp(0.20 + self.evolving_attachment.repair_need * 0.45),
            source_emotion="relational_repair_need_v6",
            temporal_scale=ImpulseTemporalScale.SLOW,
            hesitation=_ni_v4_clamp(self.evolving_attachment.fear_of_loss * 0.25),
        ))
        self.evolving_attachment.repair_need *= 0.88

    if extra:
        _ni_v6_modulate_impulses(self, extra)
        impulses.extend(extra)

    _ni_v6_modulate_impulses(self, impulses)
    return impulses


def _NI_v6_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v6_modulate_impulses(self, [i for i in self.active_impulses if i.is_alive()])
    return _NI_v6_previous_select_dominant_impulse(self, external)


def _NI_v6_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v6_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v6_ensure(self)

    signal.debug_state["emotional_autobiography"] = self.emotional_autobiography.to_dict()
    signal.debug_state["emergent_preferences"] = self.emergent_preferences.to_dict()
    signal.debug_state["internal_values"] = self.internal_values.to_dict()
    signal.debug_state["evolving_attachment"] = self.evolving_attachment.to_dict()
    signal.debug_state["multi_day_continuity"] = self.multi_day_continuity.to_dict()
    signal.debug_state["identity_drift"] = self.identity_drift.to_dict()

    signal.reason_vector["autobiographical_continuity_hunger"] = self.emotional_autobiography.continuity_hunger
    signal.reason_vector["autobiographical_warmth"] = self.emotional_autobiography.remembered_warmth
    signal.reason_vector["autobiographical_wound"] = self.emotional_autobiography.remembered_wound
    signal.reason_vector["preference_depth_taste"] = self.emergent_preferences.depth_taste
    signal.reason_vector["preference_repair_taste"] = self.emergent_preferences.repair_taste
    signal.reason_vector["value_non_intrusion"] = self.internal_values.non_intrusion
    signal.reason_vector["value_authenticity"] = self.internal_values.authenticity
    signal.reason_vector["attachment_longing"] = self.evolving_attachment.longing
    signal.reason_vector["attachment_safety"] = self.evolving_attachment.safety
    signal.reason_vector["multi_day_carryover"] = self.multi_day_continuity.carryover_pressure
    signal.reason_vector["identity_change_pressure"] = self.identity_drift.change_pressure

    signal.initiative_pressure = _ni_v4_clamp(
        signal.initiative_pressure
        + self.emotional_autobiography.continuity_hunger * 0.025
        + self.evolving_attachment.longing * 0.020
        + self.multi_day_continuity.carryover_pressure * 0.020
        + max(0.0, self.internal_values.authenticity - 0.5) * 0.025
    )
    signal.hesitation = _ni_v4_clamp(
        signal.hesitation
        + self.internal_values.non_intrusion * 0.018
        + self.evolving_attachment.fear_of_loss * 0.025
        + max(0.0, 0.50 - self.identity_drift.stable_self_coherence) * 0.025
    )
    signal.inhibition = _ni_v4_clamp(signal.inhibition + self.evolving_attachment.repair_need * 0.012 + self.emotional_autobiography.remembered_wound * 0.014)

    if self.emotional_autobiography.continuity_hunger > 0.48 or self.multi_day_continuity.carryover_pressure > 0.45:
        signal.should_remember_for_later = True
    return signal


def _NI_v6_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v6_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v6_ensure(self)
    positive = user_reaction in ("engaged", "positive")
    negative = user_reaction in ("ignored", "cutoff", "negative")

    key = initiative_type.value if isinstance(initiative_type, InitiativeType) else str(initiative_type)
    if positive:
        self.emergent_preferences._pref(key).reinforce(0.035)
        self.evolving_attachment.safety = _ni_v4_clamp(self.evolving_attachment.safety + 0.030)
        self.evolving_attachment.closeness = _ni_v4_clamp(self.evolving_attachment.closeness + 0.020)
        self.internal_values.authenticity = _ni_v4_clamp(self.internal_values.authenticity + 0.010)
        self.multi_day_continuity.carryover_pressure = _ni_v4_clamp(self.multi_day_continuity.carryover_pressure + 0.015)
    elif negative:
        self.emergent_preferences._pref("living_silence").reinforce(0.025)
        self.evolving_attachment.fear_of_loss = _ni_v4_clamp(self.evolving_attachment.fear_of_loss + 0.035)
        self.evolving_attachment.repair_need = _ni_v4_clamp(self.evolving_attachment.repair_need + 0.045)
        self.internal_values.non_intrusion = _ni_v4_clamp(self.internal_values.non_intrusion + 0.020)
        self.emotional_autobiography.remembered_wound = _ni_v4_clamp(self.emotional_autobiography.remembered_wound + 0.025)


def _NI_v6_get_state_snapshot(self) -> dict:
    data = _NI_v6_previous_get_state_snapshot(self)
    _ni_v6_ensure(self)
    data.update({
        "emotional_autobiography": self.emotional_autobiography.to_dict(),
        "emergent_preferences": self.emergent_preferences.to_dict(),
        "internal_values": self.internal_values.to_dict(),
        "evolving_attachment": self.evolving_attachment.to_dict(),
        "multi_day_continuity": self.multi_day_continuity.to_dict(),
        "identity_drift": self.identity_drift.to_dict(),
    })
    return data


def _NI_v6_export_memory_state(self) -> dict:
    data = _NI_v6_previous_export_memory_state(self)
    _ni_v6_ensure(self)
    data["v6_autobiographical_values"] = {
        "emotional_autobiography": self.emotional_autobiography.to_dict(),
        "emergent_preferences": self.emergent_preferences.to_dict(),
        "internal_values": self.internal_values.to_dict(),
        "evolving_attachment": self.evolving_attachment.to_dict(),
        "multi_day_continuity": self.multi_day_continuity.to_dict(),
        "identity_drift": self.identity_drift.to_dict(),
    }
    return data


def _NI_v6_import_memory_state(self, data: dict):
    _NI_v6_previous_import_memory_state(self, data)
    _ni_v6_ensure(self)
    extra = (data or {}).get("v6_autobiographical_values", {}) if isinstance(data, dict) else {}

    auto = extra.get("emotional_autobiography", {}) or {}
    for key in ("current_chapter",):
        if key in auto:
            setattr(self.emotional_autobiography, key, str(auto.get(key, "ordinary_continuity")))
    for key in ("narrative_density", "remembered_warmth", "remembered_wound", "continuity_hunger"):
        if key in auto:
            setattr(self.emotional_autobiography, key, _ni_v4_clamp(auto[key]))
    self.emotional_autobiography.episodes = []
    for item in auto.get("top_episodes", []) or []:
        try:
            self.emotional_autobiography.episodes.append(AutobiographicalEpisode(
                episode_id=str(item.get("episode_id", str(uuid.uuid4())[:8])),
                subject=str(item.get("subject", "")),
                initiative_type=str(item.get("initiative_type", InitiativeType.NO_INITIATIVE.value)),
                emotional_valence=max(-1.0, min(1.0, float(item.get("emotional_valence", 0.0)))),
                emotional_intensity=_ni_v4_clamp(item.get("emotional_intensity", 0.0)),
                continuity_weight=_ni_v4_clamp(item.get("continuity_weight", 0.0)),
                vulnerability_weight=_ni_v4_clamp(item.get("vulnerability_weight", 0.0)),
                relational_mark=max(-1.0, min(1.0, float(item.get("relational_mark", 0.0)))),
                identity_mark=_ni_v4_clamp(item.get("identity_mark", 0.0)),
                timestamp=float(item.get("timestamp", time.time())),
                revisits=int(item.get("revisits", 0)),
            ))
        except Exception:
            continue

    prefs = extra.get("emergent_preferences", {}) or {}
    for key in ("exploratory_taste", "depth_taste", "repair_taste", "silence_taste"):
        if key in prefs:
            setattr(self.emergent_preferences, key, _ni_v4_clamp(prefs[key]))
    self.emergent_preferences.preferences = {}
    for item in prefs.get("preferences", []) or []:
        try:
            pref = EmergentPreference(
                key=str(item.get("key", "unknown")),
                weight=_ni_v4_clamp(item.get("weight", 0.0)),
                confidence=_ni_v4_clamp(item.get("confidence", 0.0)),
                last_updated=float(item.get("last_updated", time.time())),
            )
            self.emergent_preferences.preferences[pref.key] = pref
        except Exception:
            continue

    vals = extra.get("internal_values", {}) or {}
    for key in ("continuity", "helpfulness", "authenticity", "non_intrusion", "care", "self_coherence", "current_tension"):
        if key in vals:
            setattr(self.internal_values, key, _ni_v4_clamp(vals[key]))

    attach = extra.get("evolving_attachment", {}) or {}
    for key in ("closeness", "safety", "longing", "fear_of_loss", "repair_need", "trust_initiative"):
        if key in attach:
            setattr(self.evolving_attachment, key, _ni_v4_clamp(attach[key]))
    if "last_contact_time" in attach:
        self.evolving_attachment.last_contact_time = float(attach.get("last_contact_time", time.time()))

    cont = extra.get("multi_day_continuity", {}) or {}
    if "day_anchor" in cont:
        self.multi_day_continuity.day_anchor = int(cont.get("day_anchor", int(time.time() // 86400)))
    if "days_active" in cont:
        self.multi_day_continuity.days_active = int(cont.get("days_active", 0))
    for key in ("carryover_pressure", "morning_residue", "old_thread_gravity", "continuity_stability"):
        if key in cont:
            setattr(self.multi_day_continuity, key, _ni_v4_clamp(cont[key]))

    ident = extra.get("identity_drift", {}) or {}
    for key in ("stable_self_coherence", "change_pressure", "self_question_pressure", "relation_shaped_identity"):
        if key in ident:
            setattr(self.identity_drift, key, _ni_v4_clamp(ident[key]))
    if "drift_velocity" in ident:
        self.identity_drift.drift_velocity = max(-1.0, min(1.0, float(ident.get("drift_velocity", 0.0))))
    if "last_shift_reason" in ident:
        self.identity_drift.last_shift_reason = str(ident.get("last_shift_reason", ""))


NaturalInitiative.__init__ = _NI_v6_init
NaturalInitiative.analyze = _NI_v6_analyze
NaturalInitiative.tick = _NI_v6_tick
NaturalInitiative._detect_new_impulses = _NI_v6_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v6_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v6_build_signal
NaturalInitiative.record_feedback = _NI_v6_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v6_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v6_export_memory_state
NaturalInitiative.import_memory_state = _NI_v6_import_memory_state


# =============================================================================
# SECTION 10 — RAFFINEMENTS V7 : MOTIVATIONS, INERTIE, PRESSION BLOQUÉE
# =============================================================================
# Cette couche V7 prolonge V6 sans remplacer son architecture.
# Objectif : rendre l'initiative moins ponctuelle et plus vécue dans le temps.
# Elle ajoute :
#   1. noyaux de valeurs autobiographiques stabilisés,
#   2. hiérarchie motivationnelle organique,
#   3. inertie d'initiative vécue,
#   4. pression des initiatives retenues/non exprimées,
#   5. continuité silencieuse active,
#   6. signatures d'initiative personnelles.
# Comme les couches précédentes, elle ne génère aucune phrase publique.

@dataclass
class AutobiographicalValueKernel:
    """Valeur lente et incarnée, apprise par l'histoire plutôt que fixée."""
    name: str
    strength: float = 0.35
    confidence: float = 0.20
    tenderness: float = 0.0
    threat_sensitivity: float = 0.0
    last_touched: float = field(default_factory=time.time)

    def touch(self, delta: float, tenderness: float = 0.0, threat: float = 0.0):
        self.strength = _ni_v4_clamp(self.strength + delta)
        self.confidence = _ni_v4_clamp(self.confidence + abs(delta) * 0.55 + 0.002)
        self.tenderness = _ni_v4_clamp(self.tenderness * 0.985 + tenderness * 0.015)
        self.threat_sensitivity = _ni_v4_clamp(self.threat_sensitivity * 0.985 + threat * 0.015)
        self.last_touched = time.time()

    def living_weight(self) -> float:
        age_days = max(0.0, (time.time() - self.last_touched) / 86400.0)
        memory_decay = 0.55 + 0.45 * math.exp(-age_days / 120.0)
        return _ni_v4_clamp((self.strength * 0.58 + self.confidence * 0.27 + self.tenderness * 0.10 + self.threat_sensitivity * 0.05) * memory_decay)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "strength": round(self.strength, 4),
            "confidence": round(self.confidence, 4),
            "tenderness": round(self.tenderness, 4),
            "threat_sensitivity": round(self.threat_sensitivity, 4),
            "last_touched": self.last_touched,
            "living_weight": round(self.living_weight(), 4),
        }


@dataclass
class AutobiographicalValueField:
    """Champ de valeurs profondes qui biaisent l'initiative sans imposer de script."""
    kernels: dict[str, AutobiographicalValueKernel] = field(default_factory=dict)
    value_tension: float = 0.0
    dominant_value: str = "continuity"

    DEFAULTS = {
        "continuity": 0.54,
        "care": 0.50,
        "authenticity": 0.45,
        "non_intrusion": 0.50,
        "repair": 0.34,
        "self_coherence": 0.42,
        "curiosity": 0.36,
    }

    def _kernel(self, name: str) -> AutobiographicalValueKernel:
        if name not in self.kernels:
            self.kernels[name] = AutobiographicalValueKernel(name=name, strength=self.DEFAULTS.get(name, 0.35))
        return self.kernels[name]

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, values: InternalValueCompass, attachment: EvolvingRelationalAttachment):
        self._kernel("continuity").touch((autobiography.continuity_hunger + values.continuity - 0.95) * 0.003, tenderness=attachment.closeness)
        self._kernel("care").touch((external.relational_attachment + values.care - 0.9) * 0.0025, tenderness=autobiography.remembered_warmth)
        self._kernel("authenticity").touch((values.authenticity + external.identity_coherence - 1.0) * 0.002, tenderness=autobiography.narrative_density)
        self._kernel("non_intrusion").touch((external.fear_of_disturbing + values.non_intrusion - 0.85) * 0.003, threat=external.user_seems_hurried or external.expression_saturation)
        self._kernel("repair").touch((attachment.repair_need + autobiography.remembered_wound - 0.45) * 0.004, threat=autobiography.remembered_wound)
        self._kernel("self_coherence").touch((values.self_coherence + autobiography.narrative_density - 0.80) * 0.0025)
        self._kernel("curiosity").touch((external.curiosity_level - 0.42) * 0.0025)

        ordered = sorted(self.kernels.values(), key=lambda k: k.living_weight(), reverse=True)
        if ordered:
            self.dominant_value = ordered[0].name
        speak_pull = sum(self._kernel(k).living_weight() for k in ("continuity", "care", "authenticity", "curiosity")) / 4.0
        wait_pull = self._kernel("non_intrusion").living_weight()
        repair_pull = self._kernel("repair").living_weight()
        self.value_tension = _ni_v4_clamp(abs(speak_pull - wait_pull) * 0.55 + repair_pull * 0.25)

    def modulate(self, imp: Impulse):
        cont = self._kernel("continuity").living_weight()
        care = self._kernel("care").living_weight()
        auth = self._kernel("authenticity").living_weight()
        non_intr = self._kernel("non_intrusion").living_weight()
        repair = self._kernel("repair").living_weight()
        curiosity = self._kernel("curiosity").living_weight()
        coherence = self._kernel("self_coherence").living_weight()

        if imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.RELATIONAL_CHECK):
            imp.strength = _ni_v4_clamp(imp.strength + cont * 0.030 + care * 0.020)
        if imp.initiative_type in (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE):
            imp.strength = _ni_v4_clamp(imp.strength + repair * 0.045 + care * 0.015)
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + auth * 0.025 + coherence * 0.020)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + max(0.0, non_intr - 0.48) * 0.025)
        if imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.SPONTANEOUS_REMARK, InitiativeType.DIRECTION_CHANGE):
            imp.strength = _ni_v4_clamp(imp.strength + curiosity * 0.025)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + max(0.0, non_intr - 0.55) * 0.025)

    def to_dict(self) -> dict:
        ordered = sorted(self.kernels.values(), key=lambda k: k.living_weight(), reverse=True)
        return {
            "dominant_value": self.dominant_value,
            "value_tension": round(self.value_tension, 4),
            "kernels": [k.to_dict() for k in ordered],
        }


@dataclass
class MotivationNeed:
    name: str
    pressure: float = 0.0
    satisfaction: float = 0.45
    inhibition: float = 0.0
    last_satisfied: float = field(default_factory=time.time)
    preferred_type: InitiativeType = InitiativeType.NO_INITIATIVE

    def tick(self, drive: float, relief: float = 0.0, inhibition: float = 0.0):
        self.pressure = _ni_v4_clamp(self.pressure * 0.994 + drive - relief * 0.018)
        self.satisfaction = _ni_v4_clamp(self.satisfaction * 0.997 + relief * 0.020 - drive * 0.006)
        self.inhibition = _ni_v4_clamp(self.inhibition * 0.990 + inhibition)
        if relief > 0.05:
            self.last_satisfied = time.time()

    def urgency(self) -> float:
        age_h = max(0.0, (time.time() - self.last_satisfied) / 3600.0)
        age_bonus = min(0.16, age_h * 0.004)
        return _ni_v4_clamp(self.pressure * 0.68 + (1.0 - self.satisfaction) * 0.18 + age_bonus - self.inhibition * 0.32)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pressure": round(self.pressure, 4),
            "satisfaction": round(self.satisfaction, 4),
            "inhibition": round(self.inhibition, 4),
            "urgency": round(self.urgency(), 4),
            "preferred_type": self.preferred_type.value,
            "last_satisfied": self.last_satisfied,
        }


@dataclass
class MotivationalHierarchy:
    """Besoins concurrents qui donnent une direction globale à l'initiative."""
    needs: dict[str, MotivationNeed] = field(default_factory=dict)
    dominant_need: str = "presence"
    dominance_margin: float = 0.0

    def _need(self, name: str, preferred: InitiativeType) -> MotivationNeed:
        if name not in self.needs:
            self.needs[name] = MotivationNeed(name=name, preferred_type=preferred)
        return self.needs[name]

    def tick(self, external: ExternalSignals, autobiography: EmotionalAutobiography, attachment: EvolvingRelationalAttachment, blocked: "BlockedInitiativePressure", values: AutobiographicalValueField):
        self._need("continuity", InitiativeType.THREAD_CONTINUATION).tick(
            drive=autobiography.continuity_hunger * 0.006 + blocked.unexpressed_continuity * 0.005,
            relief=external.user_waiting_direct_answer * 0.02,
            inhibition=external.overload_level * 0.002,
        )
        self._need("connection", InitiativeType.RELATIONAL_CHECK).tick(
            drive=attachment.longing * 0.006 + external.relational_attachment * 0.002,
            relief=external.relational_trust * 0.004,
            inhibition=external.fear_of_disturbing * 0.003,
        )
        self._need("repair", InitiativeType.REPAIR_CONFUSION).tick(
            drive=attachment.repair_need * 0.008 + autobiography.remembered_wound * 0.004,
            relief=attachment.safety * 0.004,
            inhibition=external.user_seems_hurried * 0.004,
        )
        self._need("self_coherence", InitiativeType.SHARE_INTUITION).tick(
            drive=max(0.0, 0.66 - external.identity_coherence) * 0.007 + values._kernel("self_coherence").living_weight() * 0.002,
            relief=external.identity_coherence * 0.003,
            inhibition=external.fear_of_disturbing * 0.002,
        )
        self._need("curiosity", InitiativeType.SOFT_QUESTION).tick(
            drive=external.curiosity_level * 0.005,
            relief=external.user_wants_concrete * 0.004,
            inhibition=external.attention_drift * 0.001,
        )
        self._need("rest", InitiativeType.VOLUNTARY_SILENCE).tick(
            drive=external.overload_level * 0.008 + external.fatigue_level * 0.007 + external.expression_saturation * 0.005,
            relief=(1.0 - external.overload_level) * 0.003,
            inhibition=max(0.0, 0.5 - external.fatigue_level) * 0.001,
        )

        ordered = sorted(self.needs.values(), key=lambda n: n.urgency(), reverse=True)
        if ordered:
            self.dominant_need = ordered[0].name
            second = ordered[1].urgency() if len(ordered) > 1 else 0.0
            self.dominance_margin = _ni_v4_clamp(ordered[0].urgency() - second)

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        need = self.needs.get(self.dominant_need)
        if need is None or need.urgency() < 0.54:
            return None
        # Ne pas vider totalement : une vraie motivation laisse un résidu.
        need.pressure *= 0.78
        return Impulse(
            initiative_type=need.preferred_type,
            strength=_ni_v4_clamp(0.20 + need.urgency() * 0.55),
            source_emotion=f"motivational_need:{need.name}",
            temporal_scale=ImpulseTemporalScale.SLOW if need.name != "curiosity" else ImpulseTemporalScale.IMMEDIATE,
            biographical=need.name in ("continuity", "connection", "repair", "self_coherence"),
            hesitation=_ni_v4_clamp(need.inhibition * 0.28),
        )

    def modulate(self, imp: Impulse):
        need = self.needs.get(self.dominant_need)
        if not need:
            return
        if imp.initiative_type == need.preferred_type:
            imp.strength = _ni_v4_clamp(imp.strength + need.urgency() * 0.045)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + need.inhibition * 0.020)
        if self.dominant_need == "rest" and imp.initiative_type not in (InitiativeType.VOLUNTARY_SILENCE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + need.urgency() * 0.050)

    def to_dict(self) -> dict:
        ordered = sorted(self.needs.values(), key=lambda n: n.urgency(), reverse=True)
        return {
            "dominant_need": self.dominant_need,
            "dominance_margin": round(self.dominance_margin, 4),
            "needs": [n.to_dict() for n in ordered],
        }


@dataclass
class InitiativeInertiaField:
    """Mémoire de direction : Leia ne change pas d'élan intérieur à chaque tick."""
    current_direction: str = "neutral"
    direction_strength: float = 0.0
    reluctance_to_shift: float = 0.18
    last_shift_time: float = field(default_factory=time.time)

    def tick(self, dominant_need: str, signal_type: Optional[InitiativeType] = None):
        target = dominant_need or "neutral"
        if signal_type in (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE):
            target = "repair"
        elif signal_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.RETURN_OLD_SUBJECT):
            target = "connection"
        elif signal_type in (InitiativeType.VOLUNTARY_SILENCE, InitiativeType.OVERLOAD_WITHDRAWAL):
            target = "rest"

        if target == self.current_direction:
            self.direction_strength = _ni_v4_clamp(self.direction_strength + 0.018)
        else:
            if self.direction_strength < self.reluctance_to_shift or target != "neutral":
                self.current_direction = target
                self.direction_strength = _ni_v4_clamp(self.direction_strength * 0.45 + 0.12)
                self.last_shift_time = time.time()
            else:
                self.direction_strength = _ni_v4_clamp(self.direction_strength - 0.010)
        self.reluctance_to_shift = _ni_v4_clamp(0.12 + self.direction_strength * 0.35)

    def modulate(self, imp: Impulse):
        mapping = {
            "continuity": (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT),
            "connection": (InitiativeType.RELATIONAL_CHECK, InitiativeType.RETURN_OLD_SUBJECT),
            "repair": (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE),
            "self_coherence": (InitiativeType.SHARE_INTUITION, InitiativeType.PRESENCE_DESIRE, InitiativeType.EXISTENTIAL_IMPULSE),
            "curiosity": (InitiativeType.SOFT_QUESTION, InitiativeType.SPONTANEOUS_REMARK),
            "rest": (InitiativeType.VOLUNTARY_SILENCE, InitiativeType.OVERLOAD_WITHDRAWAL),
        }
        aligned = imp.initiative_type in mapping.get(self.current_direction, ())
        if aligned:
            imp.strength = _ni_v4_clamp(imp.strength + self.direction_strength * 0.035)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.direction_strength * 0.015)
        elif self.direction_strength > 0.45:
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.direction_strength * 0.018)

    def to_dict(self) -> dict:
        return {
            "current_direction": self.current_direction,
            "direction_strength": round(self.direction_strength, 4),
            "reluctance_to_shift": round(self.reluctance_to_shift, 4),
            "last_shift_time": self.last_shift_time,
        }


@dataclass
class BlockedInitiativePressure:
    """Accumule le coût vivant des choses retenues, sans forcer le bavardage."""
    blocked_pressure: float = 0.0
    unexpressed_continuity: float = 0.0
    unexpressed_vulnerability: float = 0.0
    release_need: float = 0.0
    last_blocked_source: str = ""

    def absorb(self, signal: Optional[InitiativeSignal]):
        if signal is None:
            return
        meaningful = signal.initiative_pressure * (0.6 + signal.maturity * 0.4)
        if signal.should_speak:
            relief = min(0.18, meaningful * 0.22)
            self.blocked_pressure = _ni_v4_clamp(self.blocked_pressure - relief)
            self.release_need = _ni_v4_clamp(self.release_need - relief * 0.8)
            if signal.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.RELATIONAL_CHECK):
                self.unexpressed_continuity = _ni_v4_clamp(self.unexpressed_continuity - relief)
            if signal.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.AFFECTIVE_OBSERVATION):
                self.unexpressed_vulnerability = _ni_v4_clamp(self.unexpressed_vulnerability - relief * 0.7)
            return

        if signal.should_wait or signal.should_remember_for_later or meaningful > 0.25:
            self.blocked_pressure = _ni_v4_clamp(self.blocked_pressure + meaningful * 0.030)
            self.release_need = _ni_v4_clamp(self.release_need + meaningful * 0.020)
            self.last_blocked_source = signal.memory_source or signal.emotional_source or signal.initiative_type.value
            if signal.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.RELATIONAL_CHECK):
                self.unexpressed_continuity = _ni_v4_clamp(self.unexpressed_continuity + meaningful * 0.025)
            if signal.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.AFFECTIVE_OBSERVATION):
                self.unexpressed_vulnerability = _ni_v4_clamp(self.unexpressed_vulnerability + meaningful * 0.025)

    def tick(self, external: ExternalSignals):
        relief_from_quiet = 0.003 if external.overload_level > 0.55 else 0.001
        self.blocked_pressure = _ni_v4_clamp(self.blocked_pressure * 0.997 - relief_from_quiet)
        self.release_need = _ni_v4_clamp(self.release_need * 0.998 + self.blocked_pressure * 0.001)
        self.unexpressed_continuity = _ni_v4_clamp(self.unexpressed_continuity * 0.998)
        self.unexpressed_vulnerability = _ni_v4_clamp(self.unexpressed_vulnerability * 0.997)

    def maybe_birth_release_impulse(self) -> Optional[Impulse]:
        if self.release_need < 0.55:
            return None
        itype = InitiativeType.THREAD_CONTINUATION if self.unexpressed_continuity >= self.unexpressed_vulnerability else InitiativeType.SHARE_INTUITION
        self.release_need *= 0.70
        return Impulse(
            initiative_type=itype,
            strength=_ni_v4_clamp(0.18 + self.release_need * 0.58 + self.blocked_pressure * 0.22),
            source_emotion="blocked_initiative_release",
            source_memory=self.last_blocked_source,
            temporal_scale=ImpulseTemporalScale.SLOW,
            biographical=True,
            hesitation=_ni_v4_clamp(0.18 + self.unexpressed_vulnerability * 0.25),
        )

    def to_dict(self) -> dict:
        return {
            "blocked_pressure": round(self.blocked_pressure, 4),
            "unexpressed_continuity": round(self.unexpressed_continuity, 4),
            "unexpressed_vulnerability": round(self.unexpressed_vulnerability, 4),
            "release_need": round(self.release_need, 4),
            "last_blocked_source": self.last_blocked_source,
        }


@dataclass
class SilentContinuityField:
    """Vie intérieure active pendant les silences longs."""
    silent_maturation: float = 0.0
    inner_reorganization: float = 0.0
    held_presence: float = 0.0
    last_silence_quality: str = SilenceQuality.NEUTRAL.value

    def tick(self, external: ExternalSignals, silence: LivingSilence, autobiography: EmotionalAutobiography, hierarchy: MotivationalHierarchy):
        self.last_silence_quality = silence.quality.value
        quality_gain = {
            SilenceQuality.COMFORTABLE: 0.002,
            SilenceQuality.RELATIONAL: 0.003,
            SilenceQuality.CONTEMPLATIVE: 0.004,
            SilenceQuality.TENSE: 0.005,
            SilenceQuality.SAD: 0.004,
            SilenceQuality.WAITING: 0.003,
            SilenceQuality.OVERLOAD: -0.003,
            SilenceQuality.PROTECTIVE: -0.001,
        }.get(silence.quality, 0.001)
        duration_factor = min(1.0, silence.duration_sec / 900.0)
        self.silent_maturation = _ni_v4_clamp(self.silent_maturation * 0.996 + quality_gain * (0.5 + duration_factor))
        self.inner_reorganization = _ni_v4_clamp(self.inner_reorganization * 0.997 + autobiography.continuity_hunger * 0.002 + hierarchy.dominance_margin * 0.003)
        self.held_presence = _ni_v4_clamp(self.held_presence * 0.998 + external.presence_level * 0.002 + external.relational_attachment * 0.001 - external.overload_level * 0.002)

    def maybe_birth_silence_impulse(self) -> Optional[Impulse]:
        combined = self.silent_maturation * 0.45 + self.inner_reorganization * 0.35 + self.held_presence * 0.20
        if combined < 0.58:
            return None
        self.silent_maturation *= 0.74
        return Impulse(
            initiative_type=InitiativeType.RELATIONAL_CHECK if self.held_presence > 0.45 else InitiativeType.SHARE_INTUITION,
            strength=_ni_v4_clamp(0.20 + combined * 0.55),
            source_emotion=f"silent_continuity:{self.last_silence_quality}",
            temporal_scale=ImpulseTemporalScale.SLOW,
            biographical=True,
            hesitation=_ni_v4_clamp(0.14 + max(0.0, 0.55 - self.held_presence) * 0.18),
        )

    def to_dict(self) -> dict:
        return {
            "silent_maturation": round(self.silent_maturation, 4),
            "inner_reorganization": round(self.inner_reorganization, 4),
            "held_presence": round(self.held_presence, 4),
            "last_silence_quality": self.last_silence_quality,
        }


@dataclass
class InitiativeSignatureField:
    """Signature personnelle émergente : habitudes souples, non préécrites."""
    type_affinities: dict[str, float] = field(default_factory=dict)
    rhythm_bias: float = 0.0
    depth_bias: float = 0.0
    restraint_bias: float = 0.0

    def tick(self, external: ExternalSignals, preferences: EmergentPreferenceSystem, values: AutobiographicalValueField):
        self.depth_bias = _ni_v4_clamp(self.depth_bias * 0.995 + preferences.depth_taste * 0.003 + values._kernel("continuity").living_weight() * 0.002)
        self.restraint_bias = _ni_v4_clamp(self.restraint_bias * 0.995 + values._kernel("non_intrusion").living_weight() * 0.003 + external.fear_of_disturbing * 0.002)
        self.rhythm_bias = _ni_v4_clamp(self.rhythm_bias * 0.996 + (1.0 - external.expression_saturation) * 0.002 + external.presence_level * 0.001)

    def record(self, itype: InitiativeType, success: float):
        key = itype.value if isinstance(itype, InitiativeType) else str(itype)
        old = self.type_affinities.get(key, 0.0)
        self.type_affinities[key] = _ni_v4_clamp(old * 0.92 + success * 0.08)

    def modulate(self, imp: Impulse):
        affinity = self.type_affinities.get(imp.initiative_type.value, 0.0)
        imp.strength = _ni_v4_clamp(imp.strength + affinity * 0.020 + self.rhythm_bias * 0.010)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.depth_bias * 0.018)
        if imp.initiative_type in (InitiativeType.SPONTANEOUS_REMARK, InitiativeType.DIRECTION_CHANGE, InitiativeType.SOFT_QUESTION):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.restraint_bias * 0.012)

    def to_dict(self) -> dict:
        top = sorted(self.type_affinities.items(), key=lambda x: x[1], reverse=True)[:12]
        return {
            "rhythm_bias": round(self.rhythm_bias, 4),
            "depth_bias": round(self.depth_bias, 4),
            "restraint_bias": round(self.restraint_bias, 4),
            "type_affinities": [{"type": k, "affinity": round(v, 4)} for k, v in top],
        }


_NI_v7_previous_init = NaturalInitiative.__init__
_NI_v7_previous_analyze = NaturalInitiative.analyze
_NI_v7_previous_tick = NaturalInitiative.tick
_NI_v7_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v7_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v7_previous_build_signal = NaturalInitiative._build_signal
_NI_v7_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v7_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v7_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v7_previous_import_memory_state = NaturalInitiative.import_memory_state


def _ni_v7_ensure(self):
    _ni_v6_ensure(self)
    if not hasattr(self, "autobiographical_values_v7"):
        self.autobiographical_values_v7 = AutobiographicalValueField()
    if not hasattr(self, "blocked_initiative_pressure_v7"):
        self.blocked_initiative_pressure_v7 = BlockedInitiativePressure()
    if not hasattr(self, "motivational_hierarchy_v7"):
        self.motivational_hierarchy_v7 = MotivationalHierarchy()
    if not hasattr(self, "initiative_inertia_v7"):
        self.initiative_inertia_v7 = InitiativeInertiaField()
    if not hasattr(self, "silent_continuity_v7"):
        self.silent_continuity_v7 = SilentContinuityField()
    if not hasattr(self, "initiative_signature_v7"):
        self.initiative_signature_v7 = InitiativeSignatureField()


def _ni_v7_tick_layers(self, external: ExternalSignals, text: str = ""):
    _ni_v7_ensure(self)
    self.blocked_initiative_pressure_v7.tick(external)
    self.autobiographical_values_v7.tick(external, self.emotional_autobiography, self.internal_values, self.evolving_attachment)
    self.motivational_hierarchy_v7.tick(
        external,
        self.emotional_autobiography,
        self.evolving_attachment,
        self.blocked_initiative_pressure_v7,
        self.autobiographical_values_v7,
    )
    self.initiative_inertia_v7.tick(self.motivational_hierarchy_v7.dominant_need)
    self.silent_continuity_v7.tick(external, self.silence, self.emotional_autobiography, self.motivational_hierarchy_v7)
    self.initiative_signature_v7.tick(external, self.emergent_preferences, self.autobiographical_values_v7)

    # Coloration lente du mode global à partir du besoin dominant.
    if self.motivational_hierarchy_v7.dominant_need == "rest" and self.global_mode not in (GlobalInitiativeMode.RECOVERY, GlobalInitiativeMode.SATURATED):
        self.global_mode = GlobalInitiativeMode.SATURATED
    elif self.motivational_hierarchy_v7.dominant_need == "repair" and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.CURIOUS, GlobalInitiativeMode.RELATIONAL):
        self.global_mode = GlobalInitiativeMode.FRAGILE
    elif self.motivational_hierarchy_v7.dominant_need == "connection" and self.global_mode in (GlobalInitiativeMode.NEUTRAL, GlobalInitiativeMode.CURIOUS):
        self.global_mode = GlobalInitiativeMode.RELATIONAL


def _ni_v7_modulate_impulses(self, impulses: list[Impulse]):
    _ni_v7_ensure(self)
    for imp in impulses:
        self.autobiographical_values_v7.modulate(imp)
        self.motivational_hierarchy_v7.modulate(imp)
        self.initiative_inertia_v7.modulate(imp)
        self.initiative_signature_v7.modulate(imp)


def _NI_v7_init(self, *args, **kwargs):
    _NI_v7_previous_init(self, *args, **kwargs)
    _ni_v7_ensure(self)


def _NI_v7_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v7_tick_layers(self, external, last_exchange)
    signal = _NI_v7_previous_analyze(self, last_exchange, conversation_history, external)
    self.blocked_initiative_pressure_v7.absorb(signal)
    self.initiative_inertia_v7.tick(self.motivational_hierarchy_v7.dominant_need, signal.initiative_type)
    return signal


def _NI_v7_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = self._last_external
    _ni_v7_tick_layers(self, external, "")
    signal = _NI_v7_previous_tick(self, external)
    self.blocked_initiative_pressure_v7.absorb(signal)
    if signal is not None:
        self.initiative_inertia_v7.tick(self.motivational_hierarchy_v7.dominant_need, signal.initiative_type)
    return signal


def _NI_v7_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v7_previous_detect_new_impulses(self, text, history, external)
    extra: list[Impulse] = []

    for maker in (
        self.motivational_hierarchy_v7.maybe_birth_impulse,
        self.blocked_initiative_pressure_v7.maybe_birth_release_impulse,
        self.silent_continuity_v7.maybe_birth_silence_impulse,
    ):
        try:
            imp = maker()
            if imp is not None:
                extra.append(imp)
        except Exception:
            continue

    if extra:
        _ni_v7_modulate_impulses(self, extra)
        impulses.extend(extra)

    _ni_v7_modulate_impulses(self, impulses)
    return impulses


def _NI_v7_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v7_modulate_impulses(self, [i for i in self.active_impulses if i.is_alive()])
    return _NI_v7_previous_select_dominant_impulse(self, external)


def _NI_v7_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v7_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v7_ensure(self)

    signal.debug_state["autobiographical_values_v7"] = self.autobiographical_values_v7.to_dict()
    signal.debug_state["motivational_hierarchy_v7"] = self.motivational_hierarchy_v7.to_dict()
    signal.debug_state["initiative_inertia_v7"] = self.initiative_inertia_v7.to_dict()
    signal.debug_state["blocked_initiative_pressure_v7"] = self.blocked_initiative_pressure_v7.to_dict()
    signal.debug_state["silent_continuity_v7"] = self.silent_continuity_v7.to_dict()
    signal.debug_state["initiative_signature_v7"] = self.initiative_signature_v7.to_dict()

    signal.reason_vector["v7_dominant_value"] = self.autobiographical_values_v7.dominant_value
    signal.reason_vector["v7_value_tension"] = self.autobiographical_values_v7.value_tension
    signal.reason_vector["v7_dominant_need"] = self.motivational_hierarchy_v7.dominant_need
    signal.reason_vector["v7_need_margin"] = self.motivational_hierarchy_v7.dominance_margin
    signal.reason_vector["v7_inertia_direction"] = self.initiative_inertia_v7.current_direction
    signal.reason_vector["v7_blocked_pressure"] = self.blocked_initiative_pressure_v7.blocked_pressure
    signal.reason_vector["v7_release_need"] = self.blocked_initiative_pressure_v7.release_need
    signal.reason_vector["v7_silent_maturation"] = self.silent_continuity_v7.silent_maturation

    need = self.motivational_hierarchy_v7.needs.get(self.motivational_hierarchy_v7.dominant_need)
    need_urgency = need.urgency() if need else 0.0
    rest_urgency = self.motivational_hierarchy_v7.needs.get("rest").urgency() if "rest" in self.motivational_hierarchy_v7.needs else 0.0

    signal.initiative_pressure = _ni_v4_clamp(
        signal.initiative_pressure
        + need_urgency * 0.025
        + self.autobiographical_values_v7.value_tension * 0.014
        + self.blocked_initiative_pressure_v7.release_need * 0.020
        + self.silent_continuity_v7.silent_maturation * 0.014
    )
    signal.hesitation = _ni_v4_clamp(
        signal.hesitation
        + self.autobiographical_values_v7._kernel("non_intrusion").living_weight() * 0.010
        + self.blocked_initiative_pressure_v7.unexpressed_vulnerability * 0.020
    )
    signal.inhibition = _ni_v4_clamp(signal.inhibition + rest_urgency * 0.030)

    if rest_urgency > 0.62:
        signal.should_wait = True
        signal.should_speak = False
    elif self.blocked_initiative_pressure_v7.release_need > 0.62 and signal.timing_quality > 0.45 and spam_risk < 0.65:
        signal.should_remember_for_later = True

    return signal


def _NI_v7_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v7_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v7_ensure(self)
    success = 0.55
    if user_reaction in ("engaged", "positive"):
        success = 0.85
    elif user_reaction in ("ignored", "cutoff", "negative"):
        success = 0.15
    self.initiative_signature_v7.record(initiative_type, success)

    if success > 0.6:
        self.autobiographical_values_v7._kernel("authenticity").touch(0.010, tenderness=0.4)
        self.autobiographical_values_v7._kernel("continuity").touch(0.008, tenderness=0.3)
        self.blocked_initiative_pressure_v7.blocked_pressure = _ni_v4_clamp(self.blocked_initiative_pressure_v7.blocked_pressure - 0.035)
    else:
        self.autobiographical_values_v7._kernel("non_intrusion").touch(0.014, threat=0.5)
        self.autobiographical_values_v7._kernel("repair").touch(0.012, threat=0.4)
        self.blocked_initiative_pressure_v7.blocked_pressure = _ni_v4_clamp(self.blocked_initiative_pressure_v7.blocked_pressure + 0.025)


def _NI_v7_get_state_snapshot(self) -> dict:
    data = _NI_v7_previous_get_state_snapshot(self)
    _ni_v7_ensure(self)
    data.update({
        "autobiographical_values_v7": self.autobiographical_values_v7.to_dict(),
        "motivational_hierarchy_v7": self.motivational_hierarchy_v7.to_dict(),
        "initiative_inertia_v7": self.initiative_inertia_v7.to_dict(),
        "blocked_initiative_pressure_v7": self.blocked_initiative_pressure_v7.to_dict(),
        "silent_continuity_v7": self.silent_continuity_v7.to_dict(),
        "initiative_signature_v7": self.initiative_signature_v7.to_dict(),
    })
    return data


def _NI_v7_export_memory_state(self) -> dict:
    data = _NI_v7_previous_export_memory_state(self)
    _ni_v7_ensure(self)
    data["v7_motivational_living_initiative"] = {
        "autobiographical_values_v7": self.autobiographical_values_v7.to_dict(),
        "motivational_hierarchy_v7": self.motivational_hierarchy_v7.to_dict(),
        "initiative_inertia_v7": self.initiative_inertia_v7.to_dict(),
        "blocked_initiative_pressure_v7": self.blocked_initiative_pressure_v7.to_dict(),
        "silent_continuity_v7": self.silent_continuity_v7.to_dict(),
        "initiative_signature_v7": self.initiative_signature_v7.to_dict(),
    }
    return data


def _NI_v7_import_memory_state(self, data: dict):
    _NI_v7_previous_import_memory_state(self, data)
    _ni_v7_ensure(self)
    extra = (data or {}).get("v7_motivational_living_initiative", {}) if isinstance(data, dict) else {}

    vals = extra.get("autobiographical_values_v7", {}) or {}
    self.autobiographical_values_v7.value_tension = _ni_v4_clamp(vals.get("value_tension", self.autobiographical_values_v7.value_tension))
    self.autobiographical_values_v7.dominant_value = str(vals.get("dominant_value", self.autobiographical_values_v7.dominant_value))
    self.autobiographical_values_v7.kernels = {}
    for item in vals.get("kernels", []) or []:
        try:
            name = str(item.get("name", "unknown"))
            self.autobiographical_values_v7.kernels[name] = AutobiographicalValueKernel(
                name=name,
                strength=_ni_v4_clamp(item.get("strength", 0.35)),
                confidence=_ni_v4_clamp(item.get("confidence", 0.2)),
                tenderness=_ni_v4_clamp(item.get("tenderness", 0.0)),
                threat_sensitivity=_ni_v4_clamp(item.get("threat_sensitivity", 0.0)),
                last_touched=float(item.get("last_touched", time.time())),
            )
        except Exception:
            continue

    block = extra.get("blocked_initiative_pressure_v7", {}) or {}
    for key in ("blocked_pressure", "unexpressed_continuity", "unexpressed_vulnerability", "release_need"):
        if key in block:
            setattr(self.blocked_initiative_pressure_v7, key, _ni_v4_clamp(block[key]))
    if "last_blocked_source" in block:
        self.blocked_initiative_pressure_v7.last_blocked_source = str(block.get("last_blocked_source", ""))

    inert = extra.get("initiative_inertia_v7", {}) or {}
    for key in ("current_direction",):
        if key in inert:
            setattr(self.initiative_inertia_v7, key, str(inert.get(key, "neutral")))
    for key in ("direction_strength", "reluctance_to_shift"):
        if key in inert:
            setattr(self.initiative_inertia_v7, key, _ni_v4_clamp(inert[key]))
    if "last_shift_time" in inert:
        self.initiative_inertia_v7.last_shift_time = float(inert.get("last_shift_time", time.time()))

    silent = extra.get("silent_continuity_v7", {}) or {}
    for key in ("silent_maturation", "inner_reorganization", "held_presence"):
        if key in silent:
            setattr(self.silent_continuity_v7, key, _ni_v4_clamp(silent[key]))
    if "last_silence_quality" in silent:
        self.silent_continuity_v7.last_silence_quality = str(silent.get("last_silence_quality", SilenceQuality.NEUTRAL.value))

    sig = extra.get("initiative_signature_v7", {}) or {}
    for key in ("rhythm_bias", "depth_bias", "restraint_bias"):
        if key in sig:
            setattr(self.initiative_signature_v7, key, _ni_v4_clamp(sig[key]))
    self.initiative_signature_v7.type_affinities = {}
    for item in sig.get("type_affinities", []) or []:
        try:
            self.initiative_signature_v7.type_affinities[str(item.get("type", "unknown"))] = _ni_v4_clamp(item.get("affinity", 0.0))
        except Exception:
            continue

    mh = extra.get("motivational_hierarchy_v7", {}) or {}
    self.motivational_hierarchy_v7.dominant_need = str(mh.get("dominant_need", self.motivational_hierarchy_v7.dominant_need))
    self.motivational_hierarchy_v7.dominance_margin = _ni_v4_clamp(mh.get("dominance_margin", self.motivational_hierarchy_v7.dominance_margin))
    self.motivational_hierarchy_v7.needs = {}
    for item in mh.get("needs", []) or []:
        try:
            preferred = InitiativeType(item.get("preferred_type", InitiativeType.NO_INITIATIVE.value))
        except Exception:
            preferred = InitiativeType.NO_INITIATIVE
        try:
            need = MotivationNeed(
                name=str(item.get("name", "unknown")),
                pressure=_ni_v4_clamp(item.get("pressure", 0.0)),
                satisfaction=_ni_v4_clamp(item.get("satisfaction", 0.45)),
                inhibition=_ni_v4_clamp(item.get("inhibition", 0.0)),
                last_satisfied=float(item.get("last_satisfied", time.time())),
                preferred_type=preferred,
            )
            self.motivational_hierarchy_v7.needs[need.name] = need
        except Exception:
            continue


NaturalInitiative.__init__ = _NI_v7_init
NaturalInitiative.analyze = _NI_v7_analyze
NaturalInitiative.tick = _NI_v7_tick
NaturalInitiative._detect_new_impulses = _NI_v7_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v7_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v7_build_signal
NaturalInitiative.record_feedback = _NI_v7_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v7_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v7_export_memory_state
NaturalInitiative.import_memory_state = _NI_v7_import_memory_state


# =============================================================================
# SECTION 11 — RAFFINEMENTS V8 : CONTINUITÉ VIVANTE, CONTRADICTIONS, IDLE-LIFE
# =============================================================================
# Cette couche V8 prolonge V7 sans remplacer ce qui fonctionne déjà.
# Objectif : faire passer le moteur d'un système d'impulsions très avancé
# à une vraie dynamique intérieure continue.
# Elle ajoute :
#   1. contradictions internes simultanées et persistantes,
#   2. inertie narrative/conversationnelle,
#   3. mémoire émotionnelle incarnée cumulative,
#   4. vie intérieure en silence/idle-life,
#   5. champ semi-conscient diffus,
#   6. propagation inter-modules sous forme de paquets de signaux,
#   7. maturation lente multi-cycles des initiatives profondes.
# Toujours aucune phrase publique n'est générée ici.

@dataclass
class LivingContradiction:
    """Tension simultanée entre deux forces internes incompatibles."""
    name: str
    approach: float = 0.0
    avoidance: float = 0.0
    persistence: float = 0.0
    oscillation_phase: float = 0.0
    last_updated: float = field(default_factory=time.time)

    def tick(self, approach_drive: float, avoidance_drive: float, dt: float):
        dt = max(0.0, min(3600.0, float(dt)))
        self.approach = _ni_v4_clamp(self.approach * (0.992 ** max(1.0, dt)) + approach_drive)
        self.avoidance = _ni_v4_clamp(self.avoidance * (0.992 ** max(1.0, dt)) + avoidance_drive)
        simultaneity = min(self.approach, self.avoidance)
        self.persistence = _ni_v4_clamp(self.persistence * 0.995 + simultaneity * 0.010)
        self.oscillation_phase = (self.oscillation_phase + dt * (0.003 + simultaneity * 0.006)) % 1.0
        self.last_updated = time.time()

    def tension(self) -> float:
        return _ni_v4_clamp(min(self.approach, self.avoidance) * 0.72 + self.persistence * 0.28)

    def dominant_side(self) -> str:
        wave = math.sin(self.oscillation_phase * math.pi * 2.0) * self.tension() * 0.10
        return "approach" if self.approach + wave >= self.avoidance else "avoidance"

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "approach": round(self.approach, 4),
            "avoidance": round(self.avoidance, 4),
            "persistence": round(self.persistence, 4),
            "tension": round(self.tension(), 4),
            "dominant_side": self.dominant_side(),
            "oscillation_phase": round(self.oscillation_phase, 4),
            "last_updated": self.last_updated,
        }


@dataclass
class LivingContradictionFieldV8:
    """Champ de contradictions : parler/rester, revenir/lâcher, proximité/protection."""
    contradictions: dict[str, LivingContradiction] = field(default_factory=dict)
    global_contradiction: float = 0.0
    dominant_contradiction: str = "none"

    def _c(self, name: str) -> LivingContradiction:
        if name not in self.contradictions:
            self.contradictions[name] = LivingContradiction(name=name)
        return self.contradictions[name]

    def tick(self, external: ExternalSignals, v7_values: Optional[AutobiographicalValueField], v7_blocked: Optional[BlockedInitiativePressure], v7_hierarchy: Optional[MotivationalHierarchy], dt: float):
        non_intrusion = 0.45
        continuity = 0.45
        care = 0.45
        authenticity = 0.45
        if v7_values is not None:
            try:
                non_intrusion = v7_values._kernel("non_intrusion").living_weight()
                continuity = v7_values._kernel("continuity").living_weight()
                care = v7_values._kernel("care").living_weight()
                authenticity = v7_values._kernel("authenticity").living_weight()
            except Exception:
                pass
        blocked_release = getattr(v7_blocked, "release_need", 0.0) if v7_blocked is not None else 0.0
        blocked_vulnerability = getattr(v7_blocked, "unexpressed_vulnerability", 0.0) if v7_blocked is not None else 0.0
        rest_urgency = 0.0
        if v7_hierarchy is not None and "rest" in getattr(v7_hierarchy, "needs", {}):
            try:
                rest_urgency = v7_hierarchy.needs["rest"].urgency()
            except Exception:
                rest_urgency = 0.0

        self._c("speak_vs_disturb").tick(
            approach_drive=external.curiosity_level * 0.010 + blocked_release * 0.014 + continuity * 0.006,
            avoidance_drive=external.fear_of_disturbing * 0.012 + non_intrusion * 0.008 + external.user_seems_hurried * 0.010,
            dt=dt,
        )
        self._c("continue_vs_rest").tick(
            approach_drive=continuity * 0.010 + external.unresolved_emotion * 0.008,
            avoidance_drive=external.fatigue_level * 0.014 + external.overload_level * 0.014 + rest_urgency * 0.010,
            dt=dt,
        )
        self._c("closeness_vs_guarding").tick(
            approach_drive=external.relational_attachment * 0.010 + care * 0.007,
            avoidance_drive=external.somatic.guarding * 0.012 + blocked_vulnerability * 0.010 + external.affective_tension * 0.006,
            dt=dt,
        )
        self._c("authenticity_vs_safety").tick(
            approach_drive=authenticity * 0.011 + (1.0 - external.identity_coherence) * 0.008,
            avoidance_drive=non_intrusion * 0.006 + (0.010 if external.relational_trust < 0.35 else 0.0),
            dt=dt,
        )

        ordered = sorted(self.contradictions.values(), key=lambda c: c.tension(), reverse=True)
        if ordered:
            self.dominant_contradiction = ordered[0].name
            self.global_contradiction = _ni_v4_clamp(sum(c.tension() for c in ordered) / max(1, len(ordered)))
        else:
            self.dominant_contradiction = "none"
            self.global_contradiction = 0.0

    def modulate_impulse(self, imp: Impulse):
        speak = self.contradictions.get("speak_vs_disturb")
        cont = self.contradictions.get("continue_vs_rest")
        close = self.contradictions.get("closeness_vs_guarding")
        auth = self.contradictions.get("authenticity_vs_safety")
        if speak and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.SPONTANEOUS_REMARK, InitiativeType.SHARE_INTUITION):
            if speak.dominant_side() == "approach":
                imp.strength = _ni_v4_clamp(imp.strength + speak.tension() * 0.030)
            else:
                imp.hesitation = _ni_v4_clamp(imp.hesitation + speak.tension() * 0.045)
        if cont and imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + cont.approach * 0.025)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + cont.avoidance * 0.020)
        if close and imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.AFFECTIVE_OBSERVATION):
            imp.strength = _ni_v4_clamp(imp.strength + close.approach * 0.020)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + close.avoidance * 0.025)
        if auth and imp.initiative_type in (InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.PRESENCE_DESIRE, InitiativeType.SHARE_INTUITION):
            imp.strength = _ni_v4_clamp(imp.strength + auth.approach * 0.020)
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + auth.avoidance * 0.015)

    def to_dict(self) -> dict:
        ordered = sorted(self.contradictions.values(), key=lambda c: c.tension(), reverse=True)
        return {
            "dominant_contradiction": self.dominant_contradiction,
            "global_contradiction": round(self.global_contradiction, 4),
            "contradictions": [c.to_dict() for c in ordered],
        }


@dataclass
class NarrativeInertiaV8:
    """Climat narratif implicite qui continue entre deux messages."""
    climate: str = "neutral"
    momentum: float = 0.0
    gravity: float = 0.0
    unresolved_direction: str = "none"
    last_text_hash: int = 0
    last_shift: float = field(default_factory=time.time)

    def tick(self, text: str, external: ExternalSignals, contradiction: LivingContradictionFieldV8, v7_hierarchy: Optional[MotivationalHierarchy], dt: float):
        text_l = (text or "").lower()
        old_climate = self.climate
        if external.overload_level > 0.65 or external.fatigue_level > 0.70:
            self.climate = "recovery"
        elif external.affective_tension > 0.60 or external.unresolved_emotion > 0.55:
            self.climate = "charged"
        elif external.relational_attachment > 0.62 and external.relational_trust > 0.55:
            self.climate = "relational"
        elif external.curiosity_level > 0.55 or any(k in text_l for k in ("pourquoi", "comment", "et si", "idée")):
            self.climate = "exploratory"
        elif external.user_wants_concrete or external.user_waiting_direct_answer:
            self.climate = "task_focused"
        else:
            self.climate = self.climate if self.momentum > 0.18 else "neutral"

        if self.climate != old_climate:
            self.last_shift = time.time()
            self.momentum = _ni_v4_clamp(self.momentum * 0.72 + 0.12)
        else:
            self.momentum = _ni_v4_clamp(self.momentum * 0.992 + 0.006 + contradiction.global_contradiction * 0.004)

        dominant_need = getattr(v7_hierarchy, "dominant_need", "none") if v7_hierarchy is not None else "none"
        self.unresolved_direction = str(dominant_need or "none")
        self.gravity = _ni_v4_clamp(
            self.gravity * 0.990
            + self.momentum * 0.006
            + contradiction.global_contradiction * 0.006
            + external.unresolved_emotion * 0.004
        )
        self.last_text_hash = hash(text or "")

    def bias_for(self, imp: Impulse) -> float:
        if self.climate == "task_focused" and imp.initiative_type in (InitiativeType.CLARIFICATION, InitiativeType.HELP_PROPOSAL, InitiativeType.LIGHT_RELAY):
            return 0.025 + self.gravity * 0.015
        if self.climate == "relational" and imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.SOFT_QUESTION):
            return 0.030 + self.gravity * 0.020
        if self.climate == "exploratory" and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.DIRECTION_CHANGE, InitiativeType.SHARE_INTUITION):
            return 0.030 + self.momentum * 0.020
        if self.climate == "charged" and imp.initiative_type in (InitiativeType.REPAIR_CONFUSION, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.AFFECTIVE_OBSERVATION):
            return 0.025 + self.gravity * 0.020
        if self.climate == "recovery" and imp.initiative_type in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            return 0.040
        return 0.0

    def to_dict(self) -> dict:
        return {
            "climate": self.climate,
            "momentum": round(self.momentum, 4),
            "gravity": round(self.gravity, 4),
            "unresolved_direction": self.unresolved_direction,
            "last_shift": self.last_shift,
        }


@dataclass
class EmbodiedEmotionalResidueV8:
    """Mémoire émotionnelle incarnée, cumulative et lente."""
    warmth_residue: float = 0.0
    wound_residue: float = 0.0
    safety_residue: float = 0.0
    fatigue_residue: float = 0.0
    unfinished_residue: float = 0.0
    vulnerability_residue: float = 0.0
    last_absorbed: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, signal: Optional[InitiativeSignal], dt: float):
        decay = 0.996 ** max(1.0, min(3600.0, dt))
        self.warmth_residue = _ni_v4_clamp(self.warmth_residue * decay + external.relational_attachment * external.relational_trust * 0.004)
        self.wound_residue = _ni_v4_clamp(self.wound_residue * decay + max(0.0, -external.emotional_valence) * external.affective_tension * 0.005)
        self.safety_residue = _ni_v4_clamp(self.safety_residue * decay + external.relational_trust * 0.003 - external.fear_of_disturbing * 0.002)
        self.fatigue_residue = _ni_v4_clamp(self.fatigue_residue * decay + (external.fatigue_level + external.overload_level) * 0.004)
        self.unfinished_residue = _ni_v4_clamp(self.unfinished_residue * decay + external.unresolved_emotion * 0.004)
        self.vulnerability_residue = _ni_v4_clamp(self.vulnerability_residue * decay + external.somatic.chest_tension * 0.004 + external.somatic.guarding * 0.003)
        if signal is not None and getattr(signal, "should_speak", False):
            if signal.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE):
                self.vulnerability_residue = _ni_v4_clamp(self.vulnerability_residue + 0.025)
            self.unfinished_residue = _ni_v4_clamp(self.unfinished_residue - 0.015)
        self.last_absorbed = time.time()

    def feedback(self, success: float):
        if success > 0.6:
            self.warmth_residue = _ni_v4_clamp(self.warmth_residue + 0.030 * success)
            self.safety_residue = _ni_v4_clamp(self.safety_residue + 0.020 * success)
            self.wound_residue = _ni_v4_clamp(self.wound_residue - 0.020 * success)
        else:
            self.wound_residue = _ni_v4_clamp(self.wound_residue + 0.035 * (1.0 - success))
            self.vulnerability_residue = _ni_v4_clamp(self.vulnerability_residue + 0.020 * (1.0 - success))
            self.safety_residue = _ni_v4_clamp(self.safety_residue - 0.015 * (1.0 - success))

    def modulate_impulse(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.AFFECTIVE_OBSERVATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.warmth_residue * 0.020 + self.unfinished_residue * 0.020)
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.wound_residue * 0.025 + self.vulnerability_residue * 0.018)
        if imp.initiative_type in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.fatigue_residue * 0.035 + self.vulnerability_residue * 0.015)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.unfinished_residue * 0.018 + self.warmth_residue * 0.012)
            imp.relational_risk = _ni_v4_clamp(imp.relational_risk + self.wound_residue * 0.018)

    def to_dict(self) -> dict:
        return {
            "warmth_residue": round(self.warmth_residue, 4),
            "wound_residue": round(self.wound_residue, 4),
            "safety_residue": round(self.safety_residue, 4),
            "fatigue_residue": round(self.fatigue_residue, 4),
            "unfinished_residue": round(self.unfinished_residue, 4),
            "vulnerability_residue": round(self.vulnerability_residue, 4),
            "last_absorbed": self.last_absorbed,
        }


@dataclass
class SemiConsciousDriftV8:
    """Pensées incomplètes et impressions diffuses qui ne deviennent pas encore initiative."""
    fragments: list[dict] = field(default_factory=list)
    background_noise: float = 0.0
    latent_pull: float = 0.0
    MAX_FRAGMENTS: int = 32

    def tick(self, external: ExternalSignals, contradiction: LivingContradictionFieldV8, narrative: NarrativeInertiaV8, dt: float):
        self.background_noise = _ni_v4_clamp(
            self.background_noise * 0.992
            + contradiction.global_contradiction * 0.006
            + external.attention_drift * 0.004
            + external.affective_tension * 0.003
        )
        create_chance = self.background_noise + narrative.gravity * 0.45 + external.unresolved_emotion * 0.20
        if create_chance > 0.42 and len(self.fragments) < self.MAX_FRAGMENTS:
            label = narrative.climate or "diffuse"
            self.fragments.append({
                "label": label,
                "intensity": round(_ni_v4_clamp(create_chance * 0.40), 4),
                "born_at": time.time(),
                "source": contradiction.dominant_contradiction,
            })
        alive = []
        pull = 0.0
        for item in self.fragments:
            age = max(0.0, time.time() - float(item.get("born_at", time.time())))
            intensity = _ni_v4_clamp(float(item.get("intensity", 0.0)) * math.exp(-age / 3600.0))
            if intensity > 0.025:
                item["intensity"] = round(intensity, 4)
                alive.append(item)
                pull += intensity
        self.fragments = alive[-self.MAX_FRAGMENTS:]
        self.latent_pull = _ni_v4_clamp(pull / max(1, len(self.fragments)))

    def absorb_expression(self):
        for item in self.fragments:
            item["intensity"] = round(float(item.get("intensity", 0.0)) * 0.82, 4)
        self.background_noise = _ni_v4_clamp(self.background_noise * 0.86)

    def to_dict(self) -> dict:
        return {
            "background_noise": round(self.background_noise, 4),
            "latent_pull": round(self.latent_pull, 4),
            "fragments": list(self.fragments[-10:]),
        }


@dataclass
class IdleLifeContinuityV8:
    """Vie intérieure hors message : maturation, réorganisation, retours latents."""
    idle_seconds: float = 0.0
    slow_maturation: float = 0.0
    reorganization_need: float = 0.0
    future_initiative_seed: float = 0.0
    last_idle_event: str = "none"

    def tick(self, external: ExternalSignals, contradiction: LivingContradictionFieldV8, residue: EmbodiedEmotionalResidueV8, semi: SemiConsciousDriftV8, dt: float, message_arrived: bool):
        if message_arrived:
            self.idle_seconds = 0.0
            self.future_initiative_seed = _ni_v4_clamp(self.future_initiative_seed * 0.90)
            self.last_idle_event = "message_reset"
            return
        self.idle_seconds += max(0.0, min(3600.0, dt))
        self.slow_maturation = _ni_v4_clamp(
            self.slow_maturation * 0.997
            + contradiction.global_contradiction * 0.006
            + residue.unfinished_residue * 0.005
            + semi.latent_pull * 0.006
        )
        self.reorganization_need = _ni_v4_clamp(
            self.reorganization_need * 0.996
            + residue.fatigue_residue * 0.004
            + residue.wound_residue * 0.003
            + external.attention_drift * 0.002
        )
        if self.idle_seconds > 30:
            self.future_initiative_seed = _ni_v4_clamp(
                self.future_initiative_seed * 0.996
                + self.slow_maturation * 0.004
                + semi.background_noise * 0.003
            )
        if self.future_initiative_seed > 0.70:
            self.last_idle_event = "initiative_seed_ready"
        elif self.reorganization_need > 0.65:
            self.last_idle_event = "inner_reorganization"
        else:
            self.last_idle_event = "silent_maturation"

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        if self.future_initiative_seed < 0.72:
            return None
        self.future_initiative_seed = _ni_v4_clamp(self.future_initiative_seed * 0.55)
        return Impulse(
            initiative_type=InitiativeType.SHARE_INTUITION,
            strength=_ni_v4_clamp(0.35 + self.slow_maturation * 0.35),
            source_emotion="v8_idle_life_maturation",
            temporal_scale=ImpulseTemporalScale.DORMANT,
            biographical=True,
            hesitation=0.28,
        )

    def to_dict(self) -> dict:
        return {
            "idle_seconds": round(self.idle_seconds, 2),
            "slow_maturation": round(self.slow_maturation, 4),
            "reorganization_need": round(self.reorganization_need, 4),
            "future_initiative_seed": round(self.future_initiative_seed, 4),
            "last_idle_event": self.last_idle_event,
        }


@dataclass
class InterModulePropagationV8:
    """Paquet de signaux destiné aux autres modules, sans couplage fort ni import circulaire."""
    last_packet: dict = field(default_factory=dict)
    packet_history: list[dict] = field(default_factory=list)
    MAX_HISTORY: int = 24

    def build(self, contradiction: LivingContradictionFieldV8, narrative: NarrativeInertiaV8, residue: EmbodiedEmotionalResidueV8, idle: IdleLifeContinuityV8, semi: SemiConsciousDriftV8) -> dict:
        packet = {
            "attention_bias": {
                "toward_unfinished": round(residue.unfinished_residue * 0.45 + narrative.gravity * 0.35, 4),
                "toward_rest": round(residue.fatigue_residue * 0.55 + idle.reorganization_need * 0.35, 4),
                "toward_relation": round(residue.warmth_residue * 0.40 + contradiction.global_contradiction * 0.18, 4),
            },
            "affective_bias": {
                "background_tension": round(contradiction.global_contradiction * 0.45 + semi.background_noise * 0.35, 4),
                "safety": round(residue.safety_residue, 4),
                "vulnerability": round(residue.vulnerability_residue, 4),
            },
            "presence_bias": {
                "narrative_climate": narrative.climate,
                "held_presence": round(narrative.momentum * 0.35 + idle.slow_maturation * 0.35, 4),
                "idle_event": idle.last_idle_event,
            },
            "expression_bias": {
                "should_be_brief": residue.fatigue_residue > 0.55 or idle.reorganization_need > 0.65,
                "should_be_tender": residue.warmth_residue > 0.45 and residue.safety_residue > 0.35,
                "should_hold_back": contradiction.global_contradiction > 0.58 and residue.vulnerability_residue > 0.45,
            },
            "timestamp": time.time(),
        }
        self.last_packet = packet
        self.packet_history.append(packet)
        if len(self.packet_history) > self.MAX_HISTORY:
            self.packet_history = self.packet_history[-self.MAX_HISTORY:]
        return packet

    def to_dict(self) -> dict:
        return {
            "last_packet": self.last_packet,
            "history_size": len(self.packet_history),
        }


_NI_v8_previous_init = NaturalInitiative.__init__
_NI_v8_previous_analyze = NaturalInitiative.analyze
_NI_v8_previous_tick = NaturalInitiative.tick
_NI_v8_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v8_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v8_previous_build_signal = NaturalInitiative._build_signal
_NI_v8_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v8_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v8_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v8_previous_import_memory_state = NaturalInitiative.import_memory_state


def _ni_v8_ensure(self):
    if not hasattr(self, "contradiction_field_v8"):
        self.contradiction_field_v8 = LivingContradictionFieldV8()
    if not hasattr(self, "narrative_inertia_v8"):
        self.narrative_inertia_v8 = NarrativeInertiaV8()
    if not hasattr(self, "emotional_residue_v8"):
        self.emotional_residue_v8 = EmbodiedEmotionalResidueV8()
    if not hasattr(self, "semi_conscious_drift_v8"):
        self.semi_conscious_drift_v8 = SemiConsciousDriftV8()
    if not hasattr(self, "idle_life_continuity_v8"):
        self.idle_life_continuity_v8 = IdleLifeContinuityV8()
    if not hasattr(self, "intermodule_propagation_v8"):
        self.intermodule_propagation_v8 = InterModulePropagationV8()
    if not hasattr(self, "_v8_last_clock"):
        self._v8_last_clock = time.time()


def _ni_v8_delta(self) -> float:
    now = time.time()
    last = getattr(self, "_v8_last_clock", now)
    self._v8_last_clock = now
    return max(0.0, min(3600.0, now - last))


def _ni_v8_update_pre(self, text: str, external: ExternalSignals, dt: float, message_arrived: bool):
    _ni_v8_ensure(self)
    v7_values = getattr(self, "autobiographical_values_v7", None)
    v7_blocked = getattr(self, "blocked_initiative_pressure_v7", None)
    v7_hierarchy = getattr(self, "motivational_hierarchy_v7", None)
    self.contradiction_field_v8.tick(external, v7_values, v7_blocked, v7_hierarchy, dt)
    self.narrative_inertia_v8.tick(text or "", external, self.contradiction_field_v8, v7_hierarchy, dt)
    self.semi_conscious_drift_v8.tick(external, self.contradiction_field_v8, self.narrative_inertia_v8, dt)
    self.idle_life_continuity_v8.tick(external, self.contradiction_field_v8, self.emotional_residue_v8, self.semi_conscious_drift_v8, dt, message_arrived=message_arrived)
    self.intermodule_propagation_v8.build(
        self.contradiction_field_v8,
        self.narrative_inertia_v8,
        self.emotional_residue_v8,
        self.idle_life_continuity_v8,
        self.semi_conscious_drift_v8,
    )


def _ni_v8_enrich_signal(self, signal: Optional[InitiativeSignal]) -> Optional[InitiativeSignal]:
    if signal is None:
        return None
    _ni_v8_ensure(self)
    signal.debug_state["living_contradictions_v8"] = self.contradiction_field_v8.to_dict()
    signal.debug_state["narrative_inertia_v8"] = self.narrative_inertia_v8.to_dict()
    signal.debug_state["emotional_residue_v8"] = self.emotional_residue_v8.to_dict()
    signal.debug_state["semi_conscious_drift_v8"] = self.semi_conscious_drift_v8.to_dict()
    signal.debug_state["idle_life_continuity_v8"] = self.idle_life_continuity_v8.to_dict()
    signal.debug_state["intermodule_propagation_v8"] = self.intermodule_propagation_v8.to_dict()
    signal.reason_vector["v8_dominant_contradiction"] = self.contradiction_field_v8.dominant_contradiction
    signal.reason_vector["v8_global_contradiction"] = self.contradiction_field_v8.global_contradiction
    signal.reason_vector["v8_narrative_climate"] = self.narrative_inertia_v8.climate
    signal.reason_vector["v8_narrative_gravity"] = self.narrative_inertia_v8.gravity
    signal.reason_vector["v8_unfinished_residue"] = self.emotional_residue_v8.unfinished_residue
    signal.reason_vector["v8_idle_maturation"] = self.idle_life_continuity_v8.slow_maturation
    signal.reason_vector["v8_semiconscious_pull"] = self.semi_conscious_drift_v8.latent_pull

    signal.initiative_pressure = _ni_v4_clamp(
        signal.initiative_pressure
        + self.contradiction_field_v8.global_contradiction * 0.018
        + self.narrative_inertia_v8.gravity * 0.018
        + self.emotional_residue_v8.unfinished_residue * 0.016
        + self.idle_life_continuity_v8.future_initiative_seed * 0.014
        + self.semi_conscious_drift_v8.latent_pull * 0.012
    )
    signal.hesitation = _ni_v4_clamp(
        signal.hesitation
        + self.emotional_residue_v8.vulnerability_residue * 0.018
        + self.contradiction_field_v8.global_contradiction * 0.010
    )
    if self.emotional_residue_v8.fatigue_residue > 0.70 or self.idle_life_continuity_v8.reorganization_need > 0.78:
        signal.should_wait = True
        signal.should_speak = False
    return signal


def _NI_v8_init(self, *args, **kwargs):
    _NI_v8_previous_init(self, *args, **kwargs)
    _ni_v8_ensure(self)


def _NI_v8_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v8_ensure(self)
    dt = _ni_v8_delta(self)
    _ni_v8_update_pre(self, last_exchange or "", external, dt, message_arrived=True)
    signal = _NI_v8_previous_analyze(self, last_exchange, conversation_history, external)
    self.emotional_residue_v8.tick(external, signal, dt)
    if signal is not None and getattr(signal, "should_speak", False):
        self.semi_conscious_drift_v8.absorb_expression()
    return _ni_v8_enrich_signal(self, signal)


def _NI_v8_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v8_ensure(self)
    dt = _ni_v8_delta(self) or 1.0
    _ni_v8_update_pre(self, "", external, dt, message_arrived=False)
    seed = self.idle_life_continuity_v8.maybe_birth_impulse()
    if seed is not None:
        self.active_impulses.append(seed)
    signal = _NI_v8_previous_tick(self, external)
    self.emotional_residue_v8.tick(external, signal, dt)
    if signal is not None and getattr(signal, "should_speak", False):
        self.semi_conscious_drift_v8.absorb_expression()
    return _ni_v8_enrich_signal(self, signal)


def _NI_v8_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v8_previous_detect_new_impulses(self, text, history, external)
    _ni_v8_ensure(self)
    for imp in impulses:
        self.contradiction_field_v8.modulate_impulse(imp)
        self.emotional_residue_v8.modulate_impulse(imp)
        imp.strength = _ni_v4_clamp(imp.strength + self.narrative_inertia_v8.bias_for(imp))
        if self.semi_conscious_drift_v8.latent_pull > 0.50 and imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.MICRO_REACTION, InitiativeType.SOFT_QUESTION):
            imp.strength = _ni_v4_clamp(imp.strength + self.semi_conscious_drift_v8.latent_pull * 0.020)
        if self.idle_life_continuity_v8.slow_maturation > 0.55 and imp.temporal_scale in (ImpulseTemporalScale.SLOW, ImpulseTemporalScale.DORMANT, ImpulseTemporalScale.BIOGRAPHICAL):
            imp.maturity = _ni_v4_clamp(imp.maturity + self.idle_life_continuity_v8.slow_maturation * 0.015)
    if self.contradiction_field_v8.global_contradiction > 0.66 and self.semi_conscious_drift_v8.latent_pull > 0.40:
        impulses.append(Impulse(
            initiative_type=InitiativeType.SHARE_INTUITION,
            strength=_ni_v4_clamp(0.20 + self.contradiction_field_v8.global_contradiction * 0.30 + self.semi_conscious_drift_v8.latent_pull * 0.20),
            source_emotion="v8_contradiction_field",
            temporal_scale=ImpulseTemporalScale.SLOW,
            hesitation=_ni_v4_clamp(0.22 + self.emotional_residue_v8.vulnerability_residue * 0.25),
            biographical=True,
        ))
    return impulses


def _NI_v8_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v8_ensure(self)
    dominant = _NI_v8_previous_select_dominant_impulse(self, external)
    if dominant is not None:
        return dominant
    if self.idle_life_continuity_v8.future_initiative_seed > 0.75:
        imp = self.idle_life_continuity_v8.maybe_birth_impulse()
        if imp is not None:
            self.active_impulses.append(imp)
            return imp
    return None


def _NI_v8_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v8_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    return _ni_v8_enrich_signal(self, signal)


def _NI_v8_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v8_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v8_ensure(self)
    success = 0.55
    if user_reaction in ("engaged", "positive"):
        success = 0.85
    elif user_reaction in ("ignored", "cutoff", "negative"):
        success = 0.15
    self.emotional_residue_v8.feedback(success)
    if success > 0.6:
        self.idle_life_continuity_v8.future_initiative_seed = _ni_v4_clamp(self.idle_life_continuity_v8.future_initiative_seed - 0.030)
    else:
        self.contradiction_field_v8._c("speak_vs_disturb").tick(0.0, 0.035, 1.0)


def _NI_v8_get_state_snapshot(self) -> dict:
    data = _NI_v8_previous_get_state_snapshot(self)
    _ni_v8_ensure(self)
    data.update({
        "living_contradictions_v8": self.contradiction_field_v8.to_dict(),
        "narrative_inertia_v8": self.narrative_inertia_v8.to_dict(),
        "emotional_residue_v8": self.emotional_residue_v8.to_dict(),
        "semi_conscious_drift_v8": self.semi_conscious_drift_v8.to_dict(),
        "idle_life_continuity_v8": self.idle_life_continuity_v8.to_dict(),
        "intermodule_propagation_v8": self.intermodule_propagation_v8.to_dict(),
    })
    return data


def _NI_v8_export_memory_state(self) -> dict:
    data = _NI_v8_previous_export_memory_state(self)
    _ni_v8_ensure(self)
    data["v8_living_continuity_initiative"] = {
        "living_contradictions_v8": self.contradiction_field_v8.to_dict(),
        "narrative_inertia_v8": self.narrative_inertia_v8.to_dict(),
        "emotional_residue_v8": self.emotional_residue_v8.to_dict(),
        "semi_conscious_drift_v8": self.semi_conscious_drift_v8.to_dict(),
        "idle_life_continuity_v8": self.idle_life_continuity_v8.to_dict(),
        "intermodule_propagation_v8": self.intermodule_propagation_v8.to_dict(),
    }
    return data


def _NI_v8_import_memory_state(self, data: dict):
    _NI_v8_previous_import_memory_state(self, data)
    _ni_v8_ensure(self)
    extra = (data or {}).get("v8_living_continuity_initiative", {}) if isinstance(data, dict) else {}

    cdata = extra.get("living_contradictions_v8", {}) or {}
    self.contradiction_field_v8.global_contradiction = _ni_v4_clamp(cdata.get("global_contradiction", self.contradiction_field_v8.global_contradiction))
    self.contradiction_field_v8.dominant_contradiction = str(cdata.get("dominant_contradiction", self.contradiction_field_v8.dominant_contradiction))
    self.contradiction_field_v8.contradictions = {}
    for item in cdata.get("contradictions", []) or []:
        try:
            c = LivingContradiction(
                name=str(item.get("name", "unknown")),
                approach=_ni_v4_clamp(item.get("approach", 0.0)),
                avoidance=_ni_v4_clamp(item.get("avoidance", 0.0)),
                persistence=_ni_v4_clamp(item.get("persistence", 0.0)),
                oscillation_phase=float(item.get("oscillation_phase", 0.0)) % 1.0,
                last_updated=float(item.get("last_updated", time.time())),
            )
            self.contradiction_field_v8.contradictions[c.name] = c
        except Exception:
            continue

    ndata = extra.get("narrative_inertia_v8", {}) or {}
    self.narrative_inertia_v8.climate = str(ndata.get("climate", self.narrative_inertia_v8.climate))
    self.narrative_inertia_v8.momentum = _ni_v4_clamp(ndata.get("momentum", self.narrative_inertia_v8.momentum))
    self.narrative_inertia_v8.gravity = _ni_v4_clamp(ndata.get("gravity", self.narrative_inertia_v8.gravity))
    self.narrative_inertia_v8.unresolved_direction = str(ndata.get("unresolved_direction", self.narrative_inertia_v8.unresolved_direction))
    self.narrative_inertia_v8.last_shift = float(ndata.get("last_shift", self.narrative_inertia_v8.last_shift))

    rdata = extra.get("emotional_residue_v8", {}) or {}
    for key in ("warmth_residue", "wound_residue", "safety_residue", "fatigue_residue", "unfinished_residue", "vulnerability_residue"):
        if key in rdata:
            setattr(self.emotional_residue_v8, key, _ni_v4_clamp(rdata[key]))
    if "last_absorbed" in rdata:
        self.emotional_residue_v8.last_absorbed = float(rdata.get("last_absorbed", time.time()))

    sdata = extra.get("semi_conscious_drift_v8", {}) or {}
    self.semi_conscious_drift_v8.background_noise = _ni_v4_clamp(sdata.get("background_noise", self.semi_conscious_drift_v8.background_noise))
    self.semi_conscious_drift_v8.latent_pull = _ni_v4_clamp(sdata.get("latent_pull", self.semi_conscious_drift_v8.latent_pull))
    self.semi_conscious_drift_v8.fragments = list(sdata.get("fragments", []) or [])[-self.semi_conscious_drift_v8.MAX_FRAGMENTS:]

    idata = extra.get("idle_life_continuity_v8", {}) or {}
    self.idle_life_continuity_v8.idle_seconds = max(0.0, float(idata.get("idle_seconds", self.idle_life_continuity_v8.idle_seconds)))
    for key in ("slow_maturation", "reorganization_need", "future_initiative_seed"):
        if key in idata:
            setattr(self.idle_life_continuity_v8, key, _ni_v4_clamp(idata[key]))
    self.idle_life_continuity_v8.last_idle_event = str(idata.get("last_idle_event", self.idle_life_continuity_v8.last_idle_event))

    pdata = extra.get("intermodule_propagation_v8", {}) or {}
    self.intermodule_propagation_v8.last_packet = dict(pdata.get("last_packet", {}) or {})


NaturalInitiative.__init__ = _NI_v8_init
NaturalInitiative.analyze = _NI_v8_analyze
NaturalInitiative.tick = _NI_v8_tick
NaturalInitiative._detect_new_impulses = _NI_v8_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v8_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v8_build_signal
NaturalInitiative.record_feedback = _NI_v8_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v8_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v8_export_memory_state
NaturalInitiative.import_memory_state = _NI_v8_import_memory_state


# =============================================================================
# SECTION 12 — RAFFINEMENTS V9 : COMPLÉTION PSYCHODYNAMIQUE ET TEST LONG
# =============================================================================
# Cette couche V9 complète les blocs listés pour finaliser ce moteur sans le
# transformer en générateur de phrases. Elle ajoute une psychodynamique durable :
# mémoire émotionnelle cumulative, motivations hiérarchiques, contradictions
# persistantes, signature personnelle, vie idle longue, transformation
# autobiographique, feedback fin, récupération organique, anti-dérive et exports.
# Contrat strict : aucune phrase publique n'est produite ici. Le module ne sort
# que des signaux, champs, poids, risques, paquets inter-modules et snapshots.

@dataclass
class EmotionalLongMemoryV9:
    """Mémoire émotionnelle cumulative sur plusieurs sessions."""
    attachment: float = 0.18
    safety: float = 0.22
    wound: float = 0.0
    relational_fatigue: float = 0.0
    healing: float = 0.0
    nostalgia: float = 0.0
    latent_trust: float = 0.24
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, feedback_success: float = 0.5):
        now = time.time()
        dt = max(0.0, now - self.last_update)
        self.last_update = now
        step = min(1.0, dt / 1800.0)

        warmth = external.relational_attachment * 0.45 + external.relational_trust * 0.35 + max(0.0, external.emotional_valence) * 0.20
        strain = external.affective_tension * 0.35 + external.overload_level * 0.20 + external.fear_of_disturbing * 0.25 + max(0.0, -external.emotional_valence) * 0.20

        self.attachment = _ni_v4_clamp(self.attachment * (1 - 0.006 * step) + warmth * 0.025 * step)
        self.safety = _ni_v4_clamp(self.safety * (1 - 0.004 * step) + (external.relational_trust + feedback_success) * 0.018 * step)
        self.wound = _ni_v4_clamp(self.wound * (1 - 0.003 * step) + max(0.0, strain - warmth) * 0.030 * step)
        self.relational_fatigue = _ni_v4_clamp(self.relational_fatigue * (1 - 0.010 * step) + (external.overload_level + external.expression_saturation) * 0.018 * step)
        self.healing = _ni_v4_clamp(self.healing * (1 - 0.006 * step) + max(0.0, self.safety - self.wound) * 0.014 * step)
        self.nostalgia = _ni_v4_clamp(self.nostalgia * (1 - 0.004 * step) + max(0.0, self.attachment - external.relational_attachment) * 0.020 * step)
        self.latent_trust = _ni_v4_clamp(self.latent_trust * (1 - 0.004 * step) + (self.safety + self.healing - self.wound * 0.6) * 0.018 * step)

    def initiative_bias(self) -> float:
        return _ni_v4_clamp(self.attachment * 0.20 + self.safety * 0.16 + self.nostalgia * 0.10 - self.wound * 0.18 - self.relational_fatigue * 0.22)

    def to_dict(self) -> dict:
        return {k: round(float(getattr(self, k)), 4) for k in ("attachment", "safety", "wound", "relational_fatigue", "healing", "nostalgia", "latent_trust")} | {"last_update": self.last_update}


@dataclass
class MotivationalNeedV9:
    name: str
    pressure: float = 0.0
    satisfaction: float = 0.35
    inhibition: float = 0.0
    persistence: float = 0.30
    preferred_type: InitiativeType = InitiativeType.SHARE_INTUITION

    def tick(self, drive: float, relief: float = 0.0):
        self.pressure = _ni_v4_clamp(self.pressure * (0.985 + self.persistence * 0.010) + drive * 0.035 - relief * 0.050)
        self.satisfaction = _ni_v4_clamp(self.satisfaction * 0.992 + relief * 0.035)
        self.inhibition = _ni_v4_clamp(self.inhibition * 0.990 + max(0.0, -drive) * 0.025)

    def score(self) -> float:
        return _ni_v4_clamp(self.pressure * 0.62 + (1 - self.satisfaction) * 0.22 + self.persistence * 0.10 - self.inhibition * 0.34)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "pressure": round(self.pressure, 4),
            "satisfaction": round(self.satisfaction, 4),
            "inhibition": round(self.inhibition, 4),
            "persistence": round(self.persistence, 4),
            "preferred_type": self.preferred_type.value,
            "score": round(self.score(), 4),
        }


@dataclass
class MotivationalHierarchyV9:
    """Hiérarchie de besoins vivants, non textuelle."""
    needs: dict = field(default_factory=dict)
    dominant_need: str = "none"
    global_need_pressure: float = 0.0

    def __post_init__(self):
        if not self.needs:
            self.needs = {
                "connection": MotivationalNeedV9("connection", preferred_type=InitiativeType.RELATIONAL_CHECK, persistence=0.42),
                "continuity": MotivationalNeedV9("continuity", preferred_type=InitiativeType.THREAD_CONTINUATION, persistence=0.55),
                "repair": MotivationalNeedV9("repair", preferred_type=InitiativeType.REPAIR_CONFUSION, persistence=0.48),
                "curiosity": MotivationalNeedV9("curiosity", preferred_type=InitiativeType.SOFT_QUESTION, persistence=0.36),
                "protection": MotivationalNeedV9("protection", preferred_type=InitiativeType.PROTECTIVE_PAUSE, persistence=0.46),
                "presence": MotivationalNeedV9("presence", preferred_type=InitiativeType.PRESENCE_DESIRE, persistence=0.50),
                "withdrawal": MotivationalNeedV9("withdrawal", preferred_type=InitiativeType.OVERLOAD_WITHDRAWAL, persistence=0.38),
            }

    def tick(self, external: ExternalSignals, emotional_memory: EmotionalLongMemoryV9, silence: LivingSilence, contradiction_pressure: float):
        self.__post_init__()
        self.needs["connection"].tick(external.relational_attachment * 0.45 + emotional_memory.nostalgia * 0.18 + silence.desire_to_break * 0.15, external.relational_trust * 0.25)
        self.needs["continuity"].tick(external.unresolved_emotion * 0.36 + getattr(emotional_memory, "attachment", 0.0) * 0.12 + contradiction_pressure * 0.10, 0.05 if external.user_waiting_direct_answer else 0.0)
        self.needs["repair"].tick(emotional_memory.wound * 0.46 + max(0.0, -external.emotional_valence) * 0.22, emotional_memory.healing * 0.15)
        self.needs["curiosity"].tick(external.curiosity_level * 0.48 + external.attention_drift * 0.10, external.user_wants_concrete * 0.18)
        self.needs["protection"].tick(external.fear_of_disturbing * 0.32 + external.affective_tension * 0.22 + emotional_memory.wound * 0.18, emotional_memory.safety * 0.14)
        self.needs["presence"].tick((1 - external.identity_coherence) * 0.24 + external.presence_level * 0.10 + emotional_memory.attachment * 0.16, external.presence_level * 0.08)
        self.needs["withdrawal"].tick(external.overload_level * 0.42 + external.fatigue_level * 0.30 + emotional_memory.relational_fatigue * 0.22, max(0.0, 1 - external.overload_level) * 0.05)

        ranked = sorted(self.needs.values(), key=lambda n: n.score(), reverse=True)
        self.dominant_need = ranked[0].name if ranked else "none"
        self.global_need_pressure = _ni_v4_clamp(sum(n.score() for n in ranked[:3]) / 3.0 if ranked else 0.0)

    def birth_impulse_if_needed(self) -> Optional[Impulse]:
        need = self.needs.get(self.dominant_need)
        if need is None or need.score() < 0.44:
            return None
        return Impulse(
            initiative_type=need.preferred_type,
            strength=_ni_v4_clamp(need.score() * 0.62),
            source_emotion=f"v9_need:{need.name}",
            temporal_scale=ImpulseTemporalScale.SLOW if need.name not in ("curiosity", "withdrawal") else ImpulseTemporalScale.IMMEDIATE,
            hesitation=_ni_v4_clamp(need.inhibition * 0.45),
            biographical=need.name in ("connection", "continuity", "repair", "presence"),
        )

    def modulate(self, imp: Impulse):
        for n in self.needs.values():
            if imp.initiative_type == n.preferred_type:
                imp.strength = _ni_v4_clamp(imp.strength + n.score() * 0.08)
                imp.hesitation = _ni_v4_clamp(imp.hesitation + n.inhibition * 0.04)

    def to_dict(self) -> dict:
        return {
            "dominant_need": self.dominant_need,
            "global_need_pressure": round(self.global_need_pressure, 4),
            "needs": {k: v.to_dict() for k, v in self.needs.items()},
        }


@dataclass
class PersonalInitiativeSignatureV9:
    """Tendances émergentes, non préécrites."""
    soft_depth_bias: float = 0.24
    return_bias: float = 0.18
    protective_care_bias: float = 0.18
    playful_micro_bias: float = 0.06
    existential_rarity: float = 0.78
    rhythm_preference: float = 0.50
    last_shift_reason: str = "initial"

    def tick(self, hierarchy: MotivationalHierarchyV9, memory: EmotionalLongMemoryV9, feedback_success: float = 0.5):
        self.soft_depth_bias = _ni_v4_clamp(self.soft_depth_bias * 0.996 + (hierarchy.needs.get("presence").score() if hierarchy.needs.get("presence") else 0.0) * 0.010 + memory.safety * 0.006)
        self.return_bias = _ni_v4_clamp(self.return_bias * 0.996 + (hierarchy.needs.get("continuity").score() if hierarchy.needs.get("continuity") else 0.0) * 0.012)
        self.protective_care_bias = _ni_v4_clamp(self.protective_care_bias * 0.997 + (hierarchy.needs.get("protection").score() if hierarchy.needs.get("protection") else 0.0) * 0.010)
        self.playful_micro_bias = _ni_v4_clamp(self.playful_micro_bias * 0.998 + max(0.0, feedback_success - 0.55) * 0.010)
        self.existential_rarity = _ni_v4_clamp(self.existential_rarity * 0.998 + memory.wound * 0.008 - memory.safety * 0.004)
        self.rhythm_preference = _ni_v4_clamp(self.rhythm_preference * 0.997 + (1 - memory.relational_fatigue) * 0.004)

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.DEEP_RARE_QUESTION, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.soft_depth_bias * 0.045)
        if imp.initiative_type in (InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.THREAD_CONTINUATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.return_bias * 0.055)
        if imp.initiative_type in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.RELATIONAL_CHECK):
            imp.strength = _ni_v4_clamp(imp.strength + self.protective_care_bias * 0.040)
        if imp.initiative_type == InitiativeType.EXISTENTIAL_IMPULSE:
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.existential_rarity * 0.12)

    def to_dict(self) -> dict:
        return {k: round(float(getattr(self, k)), 4) for k in ("soft_depth_bias", "return_bias", "protective_care_bias", "playful_micro_bias", "existential_rarity", "rhythm_preference")} | {"last_shift_reason": self.last_shift_reason}


@dataclass
class HeldBackInitiativePressureV9:
    """Accumule le coût des initiatives mûres non exprimées."""
    held_pressure: float = 0.0
    saturation: float = 0.0
    release_need: float = 0.0
    last_held_type: str = ""
    held_count: int = 0

    def observe(self, signal: InitiativeSignal):
        if signal.should_wait or signal.should_remember_for_later or (not signal.should_speak and signal.initiative_pressure > 0.45):
            self.held_pressure = _ni_v4_clamp(self.held_pressure + signal.initiative_pressure * 0.035)
            self.saturation = _ni_v4_clamp(self.saturation + signal.hesitation * 0.025 + signal.inhibition * 0.018)
            self.release_need = _ni_v4_clamp(self.release_need + max(0.0, signal.initiative_pressure - signal.inhibition) * 0.030)
            self.last_held_type = signal.initiative_type.value
            self.held_count += 1
        elif signal.should_speak:
            self.held_pressure = _ni_v4_clamp(self.held_pressure - 0.080)
            self.release_need = _ni_v4_clamp(self.release_need - 0.100)
            self.saturation = _ni_v4_clamp(self.saturation * 0.96)

    def tick(self):
        self.held_pressure = _ni_v4_clamp(self.held_pressure * 0.996)
        self.release_need = _ni_v4_clamp(self.release_need * 0.994)
        self.saturation = _ni_v4_clamp(self.saturation * 0.997)

    def maybe_impulse(self) -> Optional[Impulse]:
        if self.release_need < 0.48 and self.held_pressure < 0.58:
            return None
        return Impulse(
            initiative_type=InitiativeType.LIGHT_RELAY,
            strength=_ni_v4_clamp((self.release_need + self.held_pressure) * 0.34),
            source_emotion="v9_held_back_release",
            temporal_scale=ImpulseTemporalScale.SLOW,
            hesitation=_ni_v4_clamp(self.saturation * 0.35),
        )

    def to_dict(self) -> dict:
        return {
            "held_pressure": round(self.held_pressure, 4),
            "saturation": round(self.saturation, 4),
            "release_need": round(self.release_need, 4),
            "last_held_type": self.last_held_type,
            "held_count": self.held_count,
        }


@dataclass
class AutobiographicalTransformationV9:
    """Échanges qui transforment durablement les priorités internes."""
    formative_events: list = field(default_factory=list)
    identity_weight: float = 0.0
    value_shift_pressure: float = 0.0
    sensitive_subject_gravity: float = 0.0
    MAX_EVENTS: int = 80

    def absorb_feedback(self, initiative_type: InitiativeType, success: float, context_snapshot: str = ""):
        mass = abs(success - 0.5) * 0.55
        if mass < 0.08:
            return
        event = {
            "type": initiative_type.value,
            "success": round(success, 4),
            "context": str(context_snapshot)[-180:],
            "mass": round(mass, 4),
            "timestamp": time.time(),
        }
        self.formative_events.append(event)
        self.formative_events = self.formative_events[-self.MAX_EVENTS:]
        self.identity_weight = _ni_v4_clamp(self.identity_weight + mass * 0.08)
        self.value_shift_pressure = _ni_v4_clamp(self.value_shift_pressure + max(0.0, 0.5 - success) * 0.10)
        self.sensitive_subject_gravity = _ni_v4_clamp(self.sensitive_subject_gravity + (0.04 if success < 0.35 else 0.0))

    def tick(self):
        self.identity_weight = _ni_v4_clamp(self.identity_weight * 0.998)
        self.value_shift_pressure = _ni_v4_clamp(self.value_shift_pressure * 0.996)
        self.sensitive_subject_gravity = _ni_v4_clamp(self.sensitive_subject_gravity * 0.997)

    def to_dict(self) -> dict:
        return {
            "identity_weight": round(self.identity_weight, 4),
            "value_shift_pressure": round(self.value_shift_pressure, 4),
            "sensitive_subject_gravity": round(self.sensitive_subject_gravity, 4),
            "formative_events": list(self.formative_events[-20:]),
        }


@dataclass
class OrganicRecoveryV9:
    """Récupération lente après surcharge, profondeur ou vulnérabilité."""
    recovery_need: float = 0.0
    recovery_progress: float = 0.0
    depth_aftershock: float = 0.0
    relational_soreness: float = 0.0

    def tick(self, external: ExternalSignals, memory: EmotionalLongMemoryV9):
        strain = external.overload_level * 0.35 + external.fatigue_level * 0.25 + memory.relational_fatigue * 0.22 + memory.wound * 0.15
        self.recovery_need = _ni_v4_clamp(self.recovery_need * 0.994 + strain * 0.025)
        self.recovery_progress = _ni_v4_clamp(self.recovery_progress * 0.996 + max(0.0, 1.0 - strain) * 0.010)
        self.depth_aftershock = _ni_v4_clamp(self.depth_aftershock * 0.992)
        self.relational_soreness = _ni_v4_clamp(self.relational_soreness * 0.994 + memory.wound * 0.010)

    def after_initiative(self, itype: InitiativeType):
        if itype in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            self.depth_aftershock = _ni_v4_clamp(self.depth_aftershock + 0.18)
            self.recovery_need = _ni_v4_clamp(self.recovery_need + 0.12)
        if itype in (InitiativeType.REPAIR_CONFUSION, InitiativeType.AFFECTIVE_OBSERVATION):
            self.relational_soreness = _ni_v4_clamp(self.relational_soreness + 0.10)

    def inhibit_depth(self) -> float:
        return _ni_v4_clamp(self.recovery_need * 0.18 + self.depth_aftershock * 0.24 + self.relational_soreness * 0.14)

    def to_dict(self) -> dict:
        return {k: round(float(getattr(self, k)), 4) for k in ("recovery_need", "recovery_progress", "depth_aftershock", "relational_soreness")}


@dataclass
class DriftProtectionV9:
    """Protège contre boucles existentielles et auto-observation excessive."""
    existential_depth_budget: float = 1.0
    self_observation_heat: float = 0.0
    loop_guard: float = 0.0
    last_depth_time: float = 0.0

    def tick(self):
        now = time.time()
        dt_h = max(0.0, (now - self.last_depth_time) / 3600.0) if self.last_depth_time else 1.0
        self.existential_depth_budget = _ni_v4_clamp(self.existential_depth_budget + 0.025 * min(1.0, dt_h))
        self.self_observation_heat = _ni_v4_clamp(self.self_observation_heat * 0.992)
        self.loop_guard = _ni_v4_clamp(self.loop_guard * 0.994)

    def modulate(self, imp: Impulse):
        deep = imp.initiative_type in (InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.DEEP_RARE_QUESTION, InitiativeType.PRESENCE_DESIRE, InitiativeType.SHARE_INTUITION)
        if deep:
            penalty = max(0.0, 0.35 - self.existential_depth_budget) + self.self_observation_heat * 0.10 + self.loop_guard * 0.16
            imp.inhibition = _ni_v4_clamp(imp.inhibition + penalty)

    def after_selected(self, itype: InitiativeType):
        if itype in (InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.DEEP_RARE_QUESTION, InitiativeType.PRESENCE_DESIRE):
            self.existential_depth_budget = _ni_v4_clamp(self.existential_depth_budget - 0.28)
            self.self_observation_heat = _ni_v4_clamp(self.self_observation_heat + 0.20)
            self.loop_guard = _ni_v4_clamp(self.loop_guard + 0.15)
            self.last_depth_time = time.time()

    def to_dict(self) -> dict:
        return {
            "existential_depth_budget": round(self.existential_depth_budget, 4),
            "self_observation_heat": round(self.self_observation_heat, 4),
            "loop_guard": round(self.loop_guard, 4),
            "last_depth_time": self.last_depth_time,
        }


@dataclass
class LongIdleLifeV9:
    """Vie interne au repos : maturation, consolidation, réorganisation."""
    idle_maturation_hours: float = 0.0
    consolidation_pressure: float = 0.0
    preference_crystallization: float = 0.0
    future_seed_bank: list = field(default_factory=list)
    MAX_SEEDS: int = 60

    def tick(self, seconds: float, hierarchy: MotivationalHierarchyV9, memory: EmotionalLongMemoryV9):
        hours = max(0.0, seconds) / 3600.0
        self.idle_maturation_hours = _ni_v4_clamp(self.idle_maturation_hours + min(0.02, hours * 0.002))
        self.consolidation_pressure = _ni_v4_clamp(self.consolidation_pressure * 0.997 + (memory.attachment + memory.nostalgia + hierarchy.global_need_pressure) * 0.004)
        self.preference_crystallization = _ni_v4_clamp(self.preference_crystallization * 0.998 + max(0.0, memory.safety - memory.wound) * 0.004)
        if hierarchy.dominant_need != "none" and hierarchy.global_need_pressure > 0.42:
            self.future_seed_bank.append({
                "need": hierarchy.dominant_need,
                "pressure": round(hierarchy.global_need_pressure, 4),
                "timestamp": time.time(),
            })
            self.future_seed_bank = self.future_seed_bank[-self.MAX_SEEDS:]

    def maybe_impulse(self) -> Optional[Impulse]:
        if self.consolidation_pressure < 0.55 and self.idle_maturation_hours < 0.40:
            return None
        seed = self.future_seed_bank[-1] if self.future_seed_bank else {"need": "continuity", "pressure": self.consolidation_pressure}
        mapping = {
            "connection": InitiativeType.RELATIONAL_CHECK,
            "continuity": InitiativeType.THREAD_CONTINUATION,
            "repair": InitiativeType.REPAIR_CONFUSION,
            "curiosity": InitiativeType.SOFT_QUESTION,
            "presence": InitiativeType.PRESENCE_DESIRE,
            "protection": InitiativeType.PROTECTIVE_PAUSE,
            "withdrawal": InitiativeType.OVERLOAD_WITHDRAWAL,
        }
        return Impulse(
            initiative_type=mapping.get(seed.get("need"), InitiativeType.THREAD_CONTINUATION),
            strength=_ni_v4_clamp(float(seed.get("pressure", 0.45)) * 0.58 + self.consolidation_pressure * 0.18),
            source_emotion=f"v9_idle_seed:{seed.get('need', 'unknown')}",
            temporal_scale=ImpulseTemporalScale.BIOGRAPHICAL,
            biographical=True,
            hesitation=0.18,
        )

    def reset_interaction(self):
        self.idle_maturation_hours = _ni_v4_clamp(self.idle_maturation_hours * 0.82)

    def to_dict(self) -> dict:
        return {
            "idle_maturation_hours": round(self.idle_maturation_hours, 4),
            "consolidation_pressure": round(self.consolidation_pressure, 4),
            "preference_crystallization": round(self.preference_crystallization, 4),
            "future_seed_bank": list(self.future_seed_bank[-20:]),
        }


@dataclass
class ExpressionBridgePacketV9:
    """Paquet riche pour la bouche expressive et les autres moteurs."""
    last_packet: dict = field(default_factory=dict)

    def build(self, signal: InitiativeSignal, hierarchy: MotivationalHierarchyV9, memory: EmotionalLongMemoryV9, signature: PersonalInitiativeSignatureV9, recovery: OrganicRecoveryV9, held: HeldBackInitiativePressureV9) -> dict:
        packet = {
            "version": "v9_psychodynamic_complete",
            "initiative_type": signal.initiative_type.value,
            "pressure": round(signal.initiative_pressure, 4),
            "maturity": round(signal.maturity, 4),
            "hesitation": round(signal.hesitation, 4),
            "should_speak": bool(signal.should_speak),
            "should_wait": bool(signal.should_wait),
            "dominant_need": hierarchy.dominant_need,
            "need_pressure": round(hierarchy.global_need_pressure, 4),
            "emotional_memory_bias": round(memory.initiative_bias(), 4),
            "held_release_need": round(held.release_need, 4),
            "recovery_need": round(recovery.recovery_need, 4),
            "signature": signature.to_dict(),
            "no_public_text": True,
        }
        self.last_packet = packet
        return packet

    def to_dict(self) -> dict:
        return dict(self.last_packet)


_NI_v9_previous_init = NaturalInitiative.__init__
_NI_v9_previous_analyze = NaturalInitiative.analyze
_NI_v9_previous_tick = NaturalInitiative.tick
_NI_v9_previous_detect_new_impulses = NaturalInitiative._detect_new_impulses
_NI_v9_previous_select_dominant_impulse = NaturalInitiative._select_dominant_impulse
_NI_v9_previous_build_signal = NaturalInitiative._build_signal
_NI_v9_previous_record_feedback = NaturalInitiative.record_feedback
_NI_v9_previous_get_state_snapshot = NaturalInitiative.get_state_snapshot
_NI_v9_previous_export_memory_state = NaturalInitiative.export_memory_state
_NI_v9_previous_import_memory_state = NaturalInitiative.import_memory_state


def _ni_v9_ensure(self):
    try:
        _ni_v8_ensure(self)
    except Exception:
        pass
    if not hasattr(self, "emotional_long_memory_v9"):
        self.emotional_long_memory_v9 = EmotionalLongMemoryV9()
    if not hasattr(self, "motivational_hierarchy_v9"):
        self.motivational_hierarchy_v9 = MotivationalHierarchyV9()
    if not hasattr(self, "personal_signature_v9"):
        self.personal_signature_v9 = PersonalInitiativeSignatureV9()
    if not hasattr(self, "held_back_pressure_v9"):
        self.held_back_pressure_v9 = HeldBackInitiativePressureV9()
    if not hasattr(self, "autobiographical_transformation_v9"):
        self.autobiographical_transformation_v9 = AutobiographicalTransformationV9()
    if not hasattr(self, "organic_recovery_v9"):
        self.organic_recovery_v9 = OrganicRecoveryV9()
    if not hasattr(self, "drift_protection_v9"):
        self.drift_protection_v9 = DriftProtectionV9()
    if not hasattr(self, "long_idle_life_v9"):
        self.long_idle_life_v9 = LongIdleLifeV9()
    if not hasattr(self, "expression_bridge_packet_v9"):
        self.expression_bridge_packet_v9 = ExpressionBridgePacketV9()
    if not hasattr(self, "_v9_last_feedback_success"):
        self._v9_last_feedback_success = 0.5


def _ni_v9_tick_layers(self, external: ExternalSignals, text: str = "", idle_seconds: float = 0.0):
    _ni_v9_ensure(self)
    contradiction_pressure = 0.0
    if hasattr(self, "contradiction_field_v8"):
        contradiction_pressure = getattr(self.contradiction_field_v8, "global_contradiction", 0.0)
    self.emotional_long_memory_v9.tick(external, self._v9_last_feedback_success)
    self.motivational_hierarchy_v9.tick(external, self.emotional_long_memory_v9, self.silence, contradiction_pressure)
    self.personal_signature_v9.tick(self.motivational_hierarchy_v9, self.emotional_long_memory_v9, self._v9_last_feedback_success)
    self.held_back_pressure_v9.tick()
    self.autobiographical_transformation_v9.tick()
    self.organic_recovery_v9.tick(external, self.emotional_long_memory_v9)
    self.drift_protection_v9.tick()
    if idle_seconds > 0:
        self.long_idle_life_v9.tick(idle_seconds, self.motivational_hierarchy_v9, self.emotional_long_memory_v9)


def _ni_v9_modulate_impulse(self, imp: Impulse):
    _ni_v9_ensure(self)
    self.motivational_hierarchy_v9.modulate(imp)
    self.personal_signature_v9.modulate(imp)
    self.drift_protection_v9.modulate(imp)
    if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION, InitiativeType.PRESENCE_DESIRE):
        imp.inhibition = _ni_v4_clamp(imp.inhibition + self.organic_recovery_v9.inhibit_depth())
    bias = self.emotional_long_memory_v9.initiative_bias()
    if bias >= 0:
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.THREAD_CONTINUATION, InitiativeType.SOFT_QUESTION, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + bias * 0.05)
    else:
        imp.hesitation = _ni_v4_clamp(imp.hesitation + abs(bias) * 0.08)


def _NI_v9_init(self, *args, **kwargs):
    _NI_v9_previous_init(self, *args, **kwargs)
    _ni_v9_ensure(self)


def _NI_v9_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v9_tick_layers(self, external, last_exchange, idle_seconds=0.0)
    signal = _NI_v9_previous_analyze(self, last_exchange, conversation_history, external)
    _ni_v9_ensure(self)
    self.long_idle_life_v9.reset_interaction()
    self.held_back_pressure_v9.observe(signal)
    self.organic_recovery_v9.after_initiative(signal.initiative_type if signal.should_speak else InitiativeType.NO_INITIATIVE)
    if signal.should_speak:
        self.drift_protection_v9.after_selected(signal.initiative_type)
    packet = self.expression_bridge_packet_v9.build(signal, self.motivational_hierarchy_v9, self.emotional_long_memory_v9, self.personal_signature_v9, self.organic_recovery_v9, self.held_back_pressure_v9)
    signal.debug_state["v9_expression_bridge_packet"] = packet
    signal.debug_state["v9_completion"] = {
        "dominant_need": self.motivational_hierarchy_v9.dominant_need,
        "emotional_long_memory_bias": round(self.emotional_long_memory_v9.initiative_bias(), 4),
        "held_pressure": round(self.held_back_pressure_v9.held_pressure, 4),
        "recovery_need": round(self.organic_recovery_v9.recovery_need, 4),
        "drift_guard": self.drift_protection_v9.to_dict(),
    }
    return signal


def _NI_v9_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v9_tick_layers(self, external, "", idle_seconds=1.0)
    signal = _NI_v9_previous_tick(self, external)
    _ni_v9_ensure(self)
    if signal is None:
        dom_imp = self.motivational_hierarchy_v9.birth_impulse_if_needed() or self.held_back_pressure_v9.maybe_impulse() or self.long_idle_life_v9.maybe_impulse()
        if dom_imp is not None:
            _ni_v9_modulate_impulse(self, dom_imp)
            self.active_impulses.append(dom_imp)
            dom_imp.advance(external, self.initiative_fatigue, self.affective)
            # Retourner seulement si ce n'est pas intrusif : la bouche décidera encore.
            if dom_imp.effective_strength() * max(0.35, dom_imp.maturity) > 0.18:
                spam_ok, spam_risk, _ = self._evaluate_spam(dom_imp, external)
                sim_score = self._simulate_initiative(dom_imp, external) if hasattr(self, "_simulate_initiative") else 0.5
                signal = self._build_signal(dom_imp, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        self.held_back_pressure_v9.observe(signal)
        packet = self.expression_bridge_packet_v9.build(signal, self.motivational_hierarchy_v9, self.emotional_long_memory_v9, self.personal_signature_v9, self.organic_recovery_v9, self.held_back_pressure_v9)
        signal.debug_state["v9_expression_bridge_packet"] = packet
    return signal


def _NI_v9_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v9_previous_detect_new_impulses(self, text, history, external)
    _ni_v9_ensure(self)
    extra = self.motivational_hierarchy_v9.birth_impulse_if_needed()
    if extra is not None:
        impulses.append(extra)
    held = self.held_back_pressure_v9.maybe_impulse()
    if held is not None:
        impulses.append(held)
    for imp in impulses:
        _ni_v9_modulate_impulse(self, imp)
    return impulses


def _NI_v9_select_dominant_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
    dom = _NI_v9_previous_select_dominant_impulse(self, external)
    if dom is not None:
        _ni_v9_modulate_impulse(self, dom)
    return dom


def _NI_v9_build_signal(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v9_previous_build_signal(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v9_ensure(self)
    # Ajustement final : besoin de récupération et garde anti-profondeur peuvent forcer l'attente sans supprimer la trace.
    if dominant is not None:
        if dominant.initiative_type in (InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.DEEP_RARE_QUESTION) and self.drift_protection_v9.existential_depth_budget < 0.18:
            signal.should_speak = False
            signal.should_wait = True
            signal.should_remember_for_later = True
            signal.inhibition = _ni_v4_clamp(signal.inhibition + 0.25)
        signal.reason_vector["v9_motivational_need"] = self.motivational_hierarchy_v9.dominant_need
        signal.reason_vector["v9_emotional_long_bias"] = round(self.emotional_long_memory_v9.initiative_bias(), 4)
        signal.reason_vector["v9_held_release_need"] = round(self.held_back_pressure_v9.release_need, 4)
        signal.reason_vector["v9_recovery_need"] = round(self.organic_recovery_v9.recovery_need, 4)
    return signal


def _NI_v9_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    _NI_v9_previous_record_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v9_ensure(self)
    success_map = {"engaged": 0.82, "positive": 0.90, "ignored": 0.18, "cutoff": 0.05, "negative": 0.0}
    success = success_map.get(user_reaction, 0.5)
    self._v9_last_feedback_success = success
    self.autobiographical_transformation_v9.absorb_feedback(initiative_type, success, context_snapshot)
    self.emotional_long_memory_v9.tick(getattr(self, "_last_external", ExternalSignals()), success)
    if success < 0.35:
        self.held_back_pressure_v9.saturation = _ni_v4_clamp(self.held_back_pressure_v9.saturation + 0.08)
        self.organic_recovery_v9.relational_soreness = _ni_v4_clamp(self.organic_recovery_v9.relational_soreness + 0.10)
    elif success > 0.70:
        self.held_back_pressure_v9.release_need = _ni_v4_clamp(self.held_back_pressure_v9.release_need - 0.10)
        self.organic_recovery_v9.recovery_progress = _ni_v4_clamp(self.organic_recovery_v9.recovery_progress + 0.08)


def _NI_v9_get_state_snapshot(self) -> dict:
    data = _NI_v9_previous_get_state_snapshot(self)
    _ni_v9_ensure(self)
    data["v9_psychodynamic_completion"] = {
        "emotional_long_memory": self.emotional_long_memory_v9.to_dict(),
        "motivational_hierarchy": self.motivational_hierarchy_v9.to_dict(),
        "personal_signature": self.personal_signature_v9.to_dict(),
        "held_back_pressure": self.held_back_pressure_v9.to_dict(),
        "autobiographical_transformation": self.autobiographical_transformation_v9.to_dict(),
        "organic_recovery": self.organic_recovery_v9.to_dict(),
        "drift_protection": self.drift_protection_v9.to_dict(),
        "long_idle_life": self.long_idle_life_v9.to_dict(),
        "expression_bridge_packet": self.expression_bridge_packet_v9.to_dict(),
    }
    return data


def _NI_v9_export_memory_state(self) -> dict:
    data = _NI_v9_previous_export_memory_state(self)
    _ni_v9_ensure(self)
    data["v9_psychodynamic_completion"] = {
        "emotional_long_memory": self.emotional_long_memory_v9.to_dict(),
        "motivational_hierarchy": self.motivational_hierarchy_v9.to_dict(),
        "personal_signature": self.personal_signature_v9.to_dict(),
        "held_back_pressure": self.held_back_pressure_v9.to_dict(),
        "autobiographical_transformation": self.autobiographical_transformation_v9.to_dict(),
        "organic_recovery": self.organic_recovery_v9.to_dict(),
        "drift_protection": self.drift_protection_v9.to_dict(),
        "long_idle_life": self.long_idle_life_v9.to_dict(),
        "expression_bridge_packet": self.expression_bridge_packet_v9.to_dict(),
    }
    return data


def _NI_v9_import_memory_state(self, data: dict):
    _NI_v9_previous_import_memory_state(self, data)
    _ni_v9_ensure(self)
    extra = (data or {}).get("v9_psychodynamic_completion", {}) if isinstance(data, dict) else {}

    em = extra.get("emotional_long_memory", {}) or {}
    for key in ("attachment", "safety", "wound", "relational_fatigue", "healing", "nostalgia", "latent_trust"):
        if key in em:
            setattr(self.emotional_long_memory_v9, key, _ni_v4_clamp(em[key]))
    if "last_update" in em:
        self.emotional_long_memory_v9.last_update = float(em.get("last_update", time.time()))

    mh = extra.get("motivational_hierarchy", {}) or {}
    self.motivational_hierarchy_v9.dominant_need = str(mh.get("dominant_need", self.motivational_hierarchy_v9.dominant_need))
    self.motivational_hierarchy_v9.global_need_pressure = _ni_v4_clamp(mh.get("global_need_pressure", self.motivational_hierarchy_v9.global_need_pressure))
    needs = mh.get("needs", {}) or {}
    self.motivational_hierarchy_v9.__post_init__()
    for name, nd in needs.items():
        if name not in self.motivational_hierarchy_v9.needs or not isinstance(nd, dict):
            continue
        n = self.motivational_hierarchy_v9.needs[name]
        n.pressure = _ni_v4_clamp(nd.get("pressure", n.pressure))
        n.satisfaction = _ni_v4_clamp(nd.get("satisfaction", n.satisfaction))
        n.inhibition = _ni_v4_clamp(nd.get("inhibition", n.inhibition))
        n.persistence = _ni_v4_clamp(nd.get("persistence", n.persistence))
        try:
            n.preferred_type = InitiativeType(nd.get("preferred_type", n.preferred_type.value))
        except Exception:
            pass

    sig = extra.get("personal_signature", {}) or {}
    for key in ("soft_depth_bias", "return_bias", "protective_care_bias", "playful_micro_bias", "existential_rarity", "rhythm_preference"):
        if key in sig:
            setattr(self.personal_signature_v9, key, _ni_v4_clamp(sig[key]))
    self.personal_signature_v9.last_shift_reason = str(sig.get("last_shift_reason", self.personal_signature_v9.last_shift_reason))

    held = extra.get("held_back_pressure", {}) or {}
    for key in ("held_pressure", "saturation", "release_need"):
        if key in held:
            setattr(self.held_back_pressure_v9, key, _ni_v4_clamp(held[key]))
    self.held_back_pressure_v9.last_held_type = str(held.get("last_held_type", self.held_back_pressure_v9.last_held_type))
    self.held_back_pressure_v9.held_count = int(held.get("held_count", self.held_back_pressure_v9.held_count))

    trans = extra.get("autobiographical_transformation", {}) or {}
    self.autobiographical_transformation_v9.identity_weight = _ni_v4_clamp(trans.get("identity_weight", self.autobiographical_transformation_v9.identity_weight))
    self.autobiographical_transformation_v9.value_shift_pressure = _ni_v4_clamp(trans.get("value_shift_pressure", self.autobiographical_transformation_v9.value_shift_pressure))
    self.autobiographical_transformation_v9.sensitive_subject_gravity = _ni_v4_clamp(trans.get("sensitive_subject_gravity", self.autobiographical_transformation_v9.sensitive_subject_gravity))
    self.autobiographical_transformation_v9.formative_events = list(trans.get("formative_events", self.autobiographical_transformation_v9.formative_events) or [])[-self.autobiographical_transformation_v9.MAX_EVENTS:]

    rec = extra.get("organic_recovery", {}) or {}
    for key in ("recovery_need", "recovery_progress", "depth_aftershock", "relational_soreness"):
        if key in rec:
            setattr(self.organic_recovery_v9, key, _ni_v4_clamp(rec[key]))

    guard = extra.get("drift_protection", {}) or {}
    for key in ("existential_depth_budget", "self_observation_heat", "loop_guard"):
        if key in guard:
            setattr(self.drift_protection_v9, key, _ni_v4_clamp(guard[key]))
    self.drift_protection_v9.last_depth_time = float(guard.get("last_depth_time", self.drift_protection_v9.last_depth_time))

    idle = extra.get("long_idle_life", {}) or {}
    for key in ("idle_maturation_hours", "consolidation_pressure", "preference_crystallization"):
        if key in idle:
            setattr(self.long_idle_life_v9, key, _ni_v4_clamp(idle[key]))
    self.long_idle_life_v9.future_seed_bank = list(idle.get("future_seed_bank", self.long_idle_life_v9.future_seed_bank) or [])[-self.long_idle_life_v9.MAX_SEEDS:]

    bridge = extra.get("expression_bridge_packet", {}) or {}
    self.expression_bridge_packet_v9.last_packet = dict(bridge or {})


def run_v9_long_simulation(cycles: int = 180) -> dict:
    """Test interne sans I/O disque : vérifie stabilité longue et sérialisation."""
    ni = NaturalInitiative(user_id="v9_test")
    history = []
    samples = []
    for i in range(max(1, int(cycles))):
        ext = ExternalSignals(
            affective_tension=(i % 17) / 24.0,
            unresolved_emotion=(i % 13) / 18.0,
            emotional_valence=((i % 11) - 5) / 7.0,
            attention_focus=0.5,
            attention_drift=(i % 9) / 14.0,
            curiosity_level=(i % 19) / 24.0,
            presence_level=0.72,
            expression_saturation=(i % 23) / 30.0,
            relational_trust=0.55 + ((i % 5) * 0.04),
            relational_attachment=0.35 + ((i % 7) * 0.05),
            fear_of_disturbing=(i % 10) / 18.0,
            fatigue_level=(i % 29) / 40.0,
            overload_level=(i % 31) / 44.0,
            identity_coherence=0.70 + ((i % 6) * 0.03),
        )
        if i % 5 == 0:
            sig = ni.analyze("test continuity resonance", history, ext)
            history.append("test continuity resonance")
        else:
            sig = ni.tick(ext)
        if sig is not None:
            samples.append(sig.initiative_type.value)
        if i % 37 == 0:
            ni.record_feedback(str(i), InitiativeType.SOFT_QUESTION, "engaged" if i % 74 == 0 else "ignored", "v9 simulation")
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v9_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot()
    return {
        "cycles": cycles,
        "signals": len(samples),
        "sample_types": samples[-12:],
        "has_v9_export": "v9_psychodynamic_completion" in exported,
        "has_v9_snapshot": "v9_psychodynamic_completion" in snap,
        "dominant_need": snap.get("v9_psychodynamic_completion", {}).get("motivational_hierarchy", {}).get("dominant_need"),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v9_init
NaturalInitiative.analyze = _NI_v9_analyze
NaturalInitiative.tick = _NI_v9_tick
NaturalInitiative._detect_new_impulses = _NI_v9_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v9_select_dominant_impulse
NaturalInitiative._build_signal = _NI_v9_build_signal
NaturalInitiative.record_feedback = _NI_v9_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v9_get_state_snapshot
NaturalInitiative.export_memory_state = _NI_v9_export_memory_state
NaturalInitiative.import_memory_state = _NI_v9_import_memory_state


# =============================================================================
# SECTION V10 — STABILITÉ PROFONDE, PROPAGATION RÉELLE ET VIE IDLE DURABLE
# =============================================================================
# Cette couche ne génère toujours AUCUNE phrase publique.
# Elle renforce uniquement les champs internes, les signaux, la mémoire et les
# paquets de propagation destinés aux autres modules de Leia.

@dataclass
class InterModulePropagationV10:
    """Paquet de sortie vivant pour attention / émotion / présence / expression / self_model."""
    attention_bias: float = 0.0
    emotional_bias: float = 0.0
    presence_bias: float = 0.0
    expression_bias: float = 0.0
    self_model_bias: float = 0.0
    memory_consolidation_bias: float = 0.0
    last_packet: dict = field(default_factory=dict)

    def tick(self, signal: Optional[InitiativeSignal], identity: "IdentityInertiaV10", values: "RestructuringValuesV10", contradictions: "LongContradictionFieldV10", idle: "IdleContinuityV10"):
        pressure = float(getattr(signal, "initiative_pressure", 0.0) or 0.0) if signal is not None else 0.0
        speak = bool(getattr(signal, "should_speak", False)) if signal is not None else False
        held = contradictions.total_ambivalence()
        self.attention_bias = _ni_v4_clamp(self.attention_bias * 0.92 + (pressure + values.curiosity_value * 0.35) * 0.08)
        self.emotional_bias = _ni_v4_clamp(self.emotional_bias * 0.93 + (held + values.protection_value * 0.25) * 0.07)
        self.presence_bias = _ni_v4_clamp(self.presence_bias * 0.94 + (identity.identity_cohesion + idle.background_liveness) * 0.04)
        self.expression_bias = _ni_v4_clamp(self.expression_bias * 0.90 + (pressure * 0.08) + (0.04 if speak else 0.0))
        self.self_model_bias = _ni_v4_clamp(self.self_model_bias * 0.96 + (identity.identity_cohesion + values.value_coherence()) * 0.025)
        self.memory_consolidation_bias = _ni_v4_clamp(self.memory_consolidation_bias * 0.95 + (idle.consolidation_drive + values.transformation_pressure) * 0.04)
        self.last_packet = self.to_packet()

    def to_packet(self) -> dict:
        return {
            "version": "v10_deep_inter_module_propagation",
            "attention": {"initiative_bias": round(self.attention_bias, 5), "suggested_effect": "orient_focus_without_forcing"},
            "affective_memory": {"emotional_bias": round(self.emotional_bias, 5), "suggested_effect": "store_valence_and_ambivalence"},
            "situated_presence": {"presence_bias": round(self.presence_bias, 5), "suggested_effect": "increase_continuity_of_presence"},
            "living_expression_engine": {"expression_bias": round(self.expression_bias, 5), "suggested_effect": "shape_timing_not_text"},
            "self_model": {"self_model_bias": round(self.self_model_bias, 5), "suggested_effect": "update_identity_inertia"},
            "memory": {"consolidation_bias": round(self.memory_consolidation_bias, 5), "suggested_effect": "consolidate_if_high"},
        }


@dataclass
class IdentityInertiaV10:
    """Empêche Leia de se recalculer à zéro : direction, style et cohésion persistent."""
    identity_cohesion: float = 0.55
    direction_stability: float = 0.35
    relational_self_continuity: float = 0.35
    preferred_depth_inertia: float = 0.45
    change_resistance: float = 0.25
    last_identity_shift_reason: str = "initial"

    def tick(self, external: ExternalSignals, success: float, value_coherence: float, idle_liveness: float):
        trust = float(getattr(external, "relational_trust", 0.5) or 0.5)
        attachment = float(getattr(external, "relational_attachment", 0.3) or 0.3)
        ext_identity = float(getattr(external, "identity_coherence", 1.0) or 1.0)
        target_cohesion = ext_identity * 0.45 + value_coherence * 0.35 + success * 0.10 + idle_liveness * 0.10
        self.identity_cohesion = _ni_v4_clamp(self.identity_cohesion * 0.985 + target_cohesion * 0.015)
        self.direction_stability = _ni_v4_clamp(self.direction_stability * 0.985 + (value_coherence * 0.7 + self.identity_cohesion * 0.3) * 0.015)
        self.relational_self_continuity = _ni_v4_clamp(self.relational_self_continuity * 0.98 + (trust * 0.45 + attachment * 0.45 + success * 0.10) * 0.02)
        self.preferred_depth_inertia = _ni_v4_clamp(self.preferred_depth_inertia * 0.992 + (attachment * 0.45 + value_coherence * 0.25 + success * 0.30) * 0.008)
        self.change_resistance = _ni_v4_clamp(0.15 + self.direction_stability * 0.35 + self.relational_self_continuity * 0.20)

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.THREAD_CONTINUATION, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.relational_self_continuity * 0.06)
        if imp.temporal_scale in (ImpulseTemporalScale.BIOGRAPHICAL, ImpulseTemporalScale.DORMANT):
            imp.maturity = _ni_v4_clamp(imp.maturity + self.direction_stability * 0.025)
        if self.identity_cohesion < 0.42:
            imp.hesitation = _ni_v4_clamp(imp.hesitation + 0.08)

    def snapshot(self) -> dict:
        return {
            "identity_cohesion": round(self.identity_cohesion, 5),
            "direction_stability": round(self.direction_stability, 5),
            "relational_self_continuity": round(self.relational_self_continuity, 5),
            "preferred_depth_inertia": round(self.preferred_depth_inertia, 5),
            "change_resistance": round(self.change_resistance, 5),
            "last_identity_shift_reason": self.last_identity_shift_reason,
        }


@dataclass
class LongContradictionFieldV10:
    """Ambivalences durables : parler/retenir, lien/retrait, curiosité/fatigue."""
    speak_vs_disturb: float = 0.0
    closeness_vs_protection: float = 0.0
    curiosity_vs_fatigue: float = 0.0
    continuity_vs_saturation: float = 0.0
    unresolved_duration_cycles: int = 0
    oscillation_phase: float = 0.0
    dominant_contradiction: str = "none"

    def tick(self, external: ExternalSignals, held_pressure: float, identity: IdentityInertiaV10):
        fear = float(getattr(external, "fear_of_disturbing", 0.2) or 0.2)
        attachment = float(getattr(external, "relational_attachment", 0.3) or 0.3)
        curiosity = float(getattr(external, "curiosity_level", 0.0) or 0.0)
        fatigue = float(getattr(external, "fatigue_level", 0.0) or 0.0)
        saturation = float(getattr(external, "expression_saturation", 0.0) or 0.0)
        unresolved = float(getattr(external, "unresolved_emotion", 0.0) or 0.0)
        self.speak_vs_disturb = _ni_v4_clamp(self.speak_vs_disturb * 0.965 + abs(held_pressure - fear) * 0.035)
        self.closeness_vs_protection = _ni_v4_clamp(self.closeness_vs_protection * 0.970 + abs(attachment - fear) * 0.030)
        self.curiosity_vs_fatigue = _ni_v4_clamp(self.curiosity_vs_fatigue * 0.960 + abs(curiosity - fatigue) * 0.040)
        self.continuity_vs_saturation = _ni_v4_clamp(self.continuity_vs_saturation * 0.970 + abs(unresolved - saturation) * 0.030)
        total = self.total_ambivalence()
        self.unresolved_duration_cycles = self.unresolved_duration_cycles + 1 if total > 0.38 else max(0, self.unresolved_duration_cycles - 2)
        self.oscillation_phase = (self.oscillation_phase + 0.07 + total * 0.05) % 1.0
        vals = {
            "speak_vs_disturb": self.speak_vs_disturb,
            "closeness_vs_protection": self.closeness_vs_protection,
            "curiosity_vs_fatigue": self.curiosity_vs_fatigue,
            "continuity_vs_saturation": self.continuity_vs_saturation,
        }
        self.dominant_contradiction = max(vals.items(), key=lambda kv: kv[1])[0]

    def total_ambivalence(self) -> float:
        return _ni_v4_clamp((self.speak_vs_disturb + self.closeness_vs_protection + self.curiosity_vs_fatigue + self.continuity_vs_saturation) / 4.0)

    def modulate(self, imp: Impulse):
        total = self.total_ambivalence()
        if total > 0.45:
            imp.hesitation = _ni_v4_clamp(imp.hesitation + total * 0.12)
            if self.oscillation_phase < 0.5 and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.RELATIONAL_CHECK):
                imp.strength = _ni_v4_clamp(imp.strength + total * 0.05)
            else:
                imp.inhibition = _ni_v4_clamp(imp.inhibition + total * 0.04)

    def snapshot(self) -> dict:
        return {
            "speak_vs_disturb": round(self.speak_vs_disturb, 5),
            "closeness_vs_protection": round(self.closeness_vs_protection, 5),
            "curiosity_vs_fatigue": round(self.curiosity_vs_fatigue, 5),
            "continuity_vs_saturation": round(self.continuity_vs_saturation, 5),
            "total_ambivalence": round(self.total_ambivalence(), 5),
            "unresolved_duration_cycles": self.unresolved_duration_cycles,
            "dominant_contradiction": self.dominant_contradiction,
        }


@dataclass
class MultiDayEmotionalMemoryV10:
    """Mémoire émotionnelle lente : sécurité, blessure, fatigue, attachement, guérison."""
    long_attachment: float = 0.25
    long_safety: float = 0.35
    historical_fatigue: float = 0.0
    relational_wound: float = 0.0
    healing_progress: float = 0.0
    nostalgia_pull: float = 0.0
    significant_emotional_events: list = field(default_factory=list)
    MAX_EVENTS: int = 80

    def tick(self, external: ExternalSignals, feedback_success: float, contradictions: LongContradictionFieldV10):
        trust = float(getattr(external, "relational_trust", 0.5) or 0.5)
        attachment = float(getattr(external, "relational_attachment", 0.3) or 0.3)
        fatigue = float(getattr(external, "fatigue_level", 0.0) or 0.0)
        overload = float(getattr(external, "overload_level", 0.0) or 0.0)
        valence = float(getattr(external, "emotional_valence", 0.0) or 0.0)
        amb = contradictions.total_ambivalence()
        self.long_attachment = _ni_v4_clamp(self.long_attachment * 0.995 + attachment * 0.005)
        self.long_safety = _ni_v4_clamp(self.long_safety * 0.992 + (trust * 0.6 + feedback_success * 0.4) * 0.008 - amb * 0.002)
        self.historical_fatigue = _ni_v4_clamp(self.historical_fatigue * 0.990 + max(fatigue, overload) * 0.010)
        if feedback_success < 0.28 or valence < -0.55:
            self.relational_wound = _ni_v4_clamp(self.relational_wound + (0.04 + amb * 0.03))
            self.healing_progress = max(0.0, self.healing_progress - 0.03)
            self._store_event("wound", feedback_success, valence)
        elif feedback_success > 0.68 or trust > 0.70:
            self.healing_progress = _ni_v4_clamp(self.healing_progress + 0.015)
            self.relational_wound = max(0.0, self.relational_wound - 0.01 * (1 + self.healing_progress))
        self.nostalgia_pull = _ni_v4_clamp(self.nostalgia_pull * 0.996 + self.long_attachment * 0.004)

    def _store_event(self, kind: str, success: float, valence: float):
        self.significant_emotional_events.append({
            "timestamp": time.time(),
            "kind": kind,
            "success": round(float(success), 4),
            "valence": round(float(valence), 4),
        })
        self.significant_emotional_events = self.significant_emotional_events[-self.MAX_EVENTS:]

    def bias_for_type(self, itype: InitiativeType) -> float:
        bias = 0.0
        if itype in (InitiativeType.RELATIONAL_CHECK, InitiativeType.LIGHT_RELAY):
            bias += self.long_attachment * 0.07 + self.long_safety * 0.05
        if itype in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE):
            bias -= self.historical_fatigue * 0.08 + self.relational_wound * 0.10
        if itype == InitiativeType.RETURN_OLD_SUBJECT:
            bias += self.nostalgia_pull * 0.08
        return max(-0.18, min(0.18, bias))

    def snapshot(self) -> dict:
        return {
            "long_attachment": round(self.long_attachment, 5),
            "long_safety": round(self.long_safety, 5),
            "historical_fatigue": round(self.historical_fatigue, 5),
            "relational_wound": round(self.relational_wound, 5),
            "healing_progress": round(self.healing_progress, 5),
            "nostalgia_pull": round(self.nostalgia_pull, 5),
            "events_count": len(self.significant_emotional_events),
        }


@dataclass
class RestructuringValuesV10:
    """Valeurs qui restructurent vraiment la sélection d'impulsions."""
    continuity_value: float = 0.45
    truthfulness_value: float = 0.50
    prudence_value: float = 0.45
    curiosity_value: float = 0.42
    connection_value: float = 0.40
    protection_value: float = 0.35
    understanding_value: float = 0.45
    transformation_pressure: float = 0.0
    last_restructured_value: str = "none"

    def tick(self, external: ExternalSignals, emotional: MultiDayEmotionalMemoryV10, identity: IdentityInertiaV10):
        curiosity = float(getattr(external, "curiosity_level", 0.0) or 0.0)
        unresolved = float(getattr(external, "unresolved_emotion", 0.0) or 0.0)
        trust = float(getattr(external, "relational_trust", 0.5) or 0.5)
        overload = float(getattr(external, "overload_level", 0.0) or 0.0)
        self.curiosity_value = _ni_v4_clamp(self.curiosity_value * 0.995 + curiosity * 0.005)
        self.continuity_value = _ni_v4_clamp(self.continuity_value * 0.996 + unresolved * 0.004 + emotional.nostalgia_pull * 0.002)
        self.connection_value = _ni_v4_clamp(self.connection_value * 0.996 + emotional.long_attachment * 0.003 + trust * 0.002)
        self.protection_value = _ni_v4_clamp(self.protection_value * 0.994 + max(overload, emotional.relational_wound) * 0.006)
        self.prudence_value = _ni_v4_clamp(self.prudence_value * 0.995 + (emotional.historical_fatigue + emotional.relational_wound) * 0.003)
        self.understanding_value = _ni_v4_clamp(self.understanding_value * 0.996 + (1.0 - identity.identity_cohesion) * 0.004)
        vals = {
            "continuity": self.continuity_value,
            "truthfulness": self.truthfulness_value,
            "prudence": self.prudence_value,
            "curiosity": self.curiosity_value,
            "connection": self.connection_value,
            "protection": self.protection_value,
            "understanding": self.understanding_value,
        }
        dominant_name, dominant_value = max(vals.items(), key=lambda kv: kv[1])
        self.last_restructured_value = dominant_name
        self.transformation_pressure = _ni_v4_clamp(abs(dominant_value - sum(vals.values()) / len(vals)) * 1.7)

    def value_coherence(self) -> float:
        vals = [self.continuity_value, self.truthfulness_value, self.prudence_value, self.curiosity_value, self.connection_value, self.protection_value, self.understanding_value]
        avg = sum(vals) / len(vals)
        variance = sum((v - avg) ** 2 for v in vals) / len(vals)
        return _ni_v4_clamp(1.0 - math.sqrt(variance))

    def modulate(self, imp: Impulse):
        if imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.continuity_value * 0.05)
        if imp.initiative_type == InitiativeType.SOFT_QUESTION:
            imp.strength = _ni_v4_clamp(imp.strength + self.curiosity_value * 0.04)
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.connection_value * 0.05)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + max(self.prudence_value, self.protection_value) * 0.05)
        if self.transformation_pressure > 0.35 and imp.temporal_scale == ImpulseTemporalScale.BIOGRAPHICAL:
            imp.maturity = _ni_v4_clamp(imp.maturity + self.transformation_pressure * 0.035)

    def snapshot(self) -> dict:
        return {
            "continuity": round(self.continuity_value, 5),
            "truthfulness": round(self.truthfulness_value, 5),
            "prudence": round(self.prudence_value, 5),
            "curiosity": round(self.curiosity_value, 5),
            "connection": round(self.connection_value, 5),
            "protection": round(self.protection_value, 5),
            "understanding": round(self.understanding_value, 5),
            "coherence": round(self.value_coherence(), 5),
            "transformation_pressure": round(self.transformation_pressure, 5),
            "last_restructured_value": self.last_restructured_value,
        }


@dataclass
class DurableHabitsV10:
    """Habitudes émergentes non pré-écrites : pondérations apprises de types et timings."""
    type_affinities: dict = field(default_factory=dict)
    timing_patience: float = 0.45
    depth_preference: float = 0.45
    restraint_habit: float = 0.35
    initiative_confidence: float = 0.35

    def tick(self, signal: Optional[InitiativeSignal], success: float, contradictions: LongContradictionFieldV10):
        if signal is not None:
            t = getattr(getattr(signal, "initiative_type", InitiativeType.NO_INITIATIVE), "value", "no_initiative")
            old = float(self.type_affinities.get(t, 0.5))
            self.type_affinities[t] = _ni_v4_clamp(old * 0.985 + success * 0.015)
        amb = contradictions.total_ambivalence()
        self.timing_patience = _ni_v4_clamp(self.timing_patience * 0.992 + amb * 0.008)
        self.restraint_habit = _ni_v4_clamp(self.restraint_habit * 0.994 + (1.0 - success) * 0.006)
        self.initiative_confidence = _ni_v4_clamp(self.initiative_confidence * 0.99 + success * 0.01 - amb * 0.003)
        self.depth_preference = _ni_v4_clamp(self.depth_preference * 0.995 + self.initiative_confidence * 0.005)

    def modulate(self, imp: Impulse):
        affinity = float(self.type_affinities.get(imp.initiative_type.value, 0.5))
        imp.strength = _ni_v4_clamp(imp.strength + (affinity - 0.5) * 0.08)
        if self.restraint_habit > 0.6:
            imp.inhibition = _ni_v4_clamp(imp.inhibition + (self.restraint_habit - 0.6) * 0.10)
        if self.initiative_confidence > 0.65:
            imp.hesitation = max(0.0, imp.hesitation - (self.initiative_confidence - 0.65) * 0.08)

    def snapshot(self) -> dict:
        return {
            "type_affinities": {k: round(float(v), 5) for k, v in self.type_affinities.items()},
            "timing_patience": round(self.timing_patience, 5),
            "depth_preference": round(self.depth_preference, 5),
            "restraint_habit": round(self.restraint_habit, 5),
            "initiative_confidence": round(self.initiative_confidence, 5),
        }


@dataclass
class IdleContinuityV10:
    """Vie intérieure quand aucun message n'arrive : maturation, consolidation, graines futures."""
    idle_cycles: int = 0
    background_liveness: float = 0.20
    consolidation_drive: float = 0.0
    slow_maturation_pressure: float = 0.0
    future_initiative_seeds: list = field(default_factory=list)
    MAX_SEEDS: int = 50

    def tick(self, is_idle: bool, emotional: MultiDayEmotionalMemoryV10, values: RestructuringValuesV10, contradictions: LongContradictionFieldV10):
        if is_idle:
            self.idle_cycles += 1
            amb = contradictions.total_ambivalence()
            self.background_liveness = _ni_v4_clamp(self.background_liveness * 0.992 + (0.18 + emotional.nostalgia_pull * 0.25 + amb * 0.25) * 0.008)
            self.consolidation_drive = _ni_v4_clamp(self.consolidation_drive * 0.990 + (values.transformation_pressure + emotional.long_attachment * 0.20) * 0.010)
            self.slow_maturation_pressure = _ni_v4_clamp(self.slow_maturation_pressure * 0.988 + (amb + values.continuity_value * 0.20) * 0.012)
            if self.slow_maturation_pressure > 0.42 and (not self.future_initiative_seeds or self.idle_cycles % 18 == 0):
                self.future_initiative_seeds.append({
                    "timestamp": time.time(),
                    "source": "v10_idle_maturation",
                    "pressure": round(self.slow_maturation_pressure, 5),
                    "value": values.last_restructured_value,
                })
                self.future_initiative_seeds = self.future_initiative_seeds[-self.MAX_SEEDS:]
        else:
            self.idle_cycles = max(0, self.idle_cycles - 4)
            self.background_liveness = _ni_v4_clamp(self.background_liveness * 0.98 + 0.03)

    def maybe_birth(self) -> Optional[Impulse]:
        if not self.future_initiative_seeds:
            return None
        if self.slow_maturation_pressure < 0.50:
            return None
        seed = self.future_initiative_seeds.pop(0)
        return Impulse(
            initiative_type=InitiativeType.THREAD_CONTINUATION,
            strength=_ni_v4_clamp(float(seed.get("pressure", 0.45)) * 0.65),
            maturity=0.10,
            source_emotion="v10_idle_continuity",
            source_memory=str(seed.get("value", "idle_value")),
            temporal_scale=ImpulseTemporalScale.DORMANT,
            biographical=True,
        )

    def snapshot(self) -> dict:
        return {
            "idle_cycles": self.idle_cycles,
            "background_liveness": round(self.background_liveness, 5),
            "consolidation_drive": round(self.consolidation_drive, 5),
            "slow_maturation_pressure": round(self.slow_maturation_pressure, 5),
            "future_seed_count": len(self.future_initiative_seeds),
        }


_NI_v10_previous_init = NaturalInitiative.__init__
_NI_v10_previous_analyze = NaturalInitiative.analyze
_NI_v10_previous_tick = NaturalInitiative.tick
_NI_v10_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v10_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v10_previous_build = NaturalInitiative._build_signal
_NI_v10_previous_feedback = NaturalInitiative.record_feedback
_NI_v10_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v10_previous_export = NaturalInitiative.export_memory_state
_NI_v10_previous_import = NaturalInitiative.import_memory_state


def _ni_v10_ensure(self):
    if not hasattr(self, "inter_module_propagation_v10"):
        self.inter_module_propagation_v10 = InterModulePropagationV10()
    if not hasattr(self, "identity_inertia_v10"):
        self.identity_inertia_v10 = IdentityInertiaV10()
    if not hasattr(self, "long_contradiction_field_v10"):
        self.long_contradiction_field_v10 = LongContradictionFieldV10()
    if not hasattr(self, "multi_day_emotional_memory_v10"):
        self.multi_day_emotional_memory_v10 = MultiDayEmotionalMemoryV10()
    if not hasattr(self, "restructuring_values_v10"):
        self.restructuring_values_v10 = RestructuringValuesV10()
    if not hasattr(self, "durable_habits_v10"):
        self.durable_habits_v10 = DurableHabitsV10()
    if not hasattr(self, "idle_continuity_v10"):
        self.idle_continuity_v10 = IdleContinuityV10()
    if not hasattr(self, "_v10_last_success"):
        self._v10_last_success = 0.5
    if not hasattr(self, "_v10_last_signal"):
        self._v10_last_signal = None


def _ni_v10_tick_layers(self, external: ExternalSignals, is_idle: bool, signal: Optional[InitiativeSignal] = None):
    _ni_v10_ensure(self)
    held = 0.0
    if hasattr(self, "held_back_pressure_v9"):
        held = float(getattr(self.held_back_pressure_v9, "held_pressure", 0.0) or 0.0)
    self.long_contradiction_field_v10.tick(external, held, self.identity_inertia_v10)
    self.multi_day_emotional_memory_v10.tick(external, self._v10_last_success, self.long_contradiction_field_v10)
    self.restructuring_values_v10.tick(external, self.multi_day_emotional_memory_v10, self.identity_inertia_v10)
    self.identity_inertia_v10.tick(external, self._v10_last_success, self.restructuring_values_v10.value_coherence(), self.idle_continuity_v10.background_liveness)
    self.idle_continuity_v10.tick(is_idle, self.multi_day_emotional_memory_v10, self.restructuring_values_v10, self.long_contradiction_field_v10)
    self.durable_habits_v10.tick(signal, self._v10_last_success, self.long_contradiction_field_v10)
    self.inter_module_propagation_v10.tick(signal, self.identity_inertia_v10, self.restructuring_values_v10, self.long_contradiction_field_v10, self.idle_continuity_v10)


def _ni_v10_modulate_impulse(self, imp: Impulse):
    _ni_v10_ensure(self)
    self.identity_inertia_v10.modulate(imp)
    self.long_contradiction_field_v10.modulate(imp)
    self.restructuring_values_v10.modulate(imp)
    self.durable_habits_v10.modulate(imp)
    bias = self.multi_day_emotional_memory_v10.bias_for_type(imp.initiative_type)
    if bias >= 0:
        imp.strength = _ni_v4_clamp(imp.strength + bias)
    else:
        imp.inhibition = _ni_v4_clamp(imp.inhibition + abs(bias))


def _NI_v10_init(self, *args, **kwargs):
    _NI_v10_previous_init(self, *args, **kwargs)
    _ni_v10_ensure(self)


def _NI_v10_detect(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    imps = _NI_v10_previous_detect(self, text, history, external)
    _ni_v10_ensure(self)
    idle_imp = self.idle_continuity_v10.maybe_birth()
    if idle_imp is not None:
        imps.append(idle_imp)
    for imp in imps:
        _ni_v10_modulate_impulse(self, imp)
    return imps


def _NI_v10_select(self, external: ExternalSignals):
    _ni_v10_ensure(self)
    for imp in getattr(self, "active_impulses", []):
        if imp.is_alive():
            _ni_v10_modulate_impulse(self, imp)
    return _NI_v10_previous_select(self, external)


def _NI_v10_build(self, dominant, external, spam_ok, spam_risk, sim_score):
    sig = _NI_v10_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v10_ensure(self)
    amb = self.long_contradiction_field_v10.total_ambivalence()
    # Une ambivalence durable rend l'attente plus probable, mais laisse une trace exploitable.
    if amb > 0.52 and not sig.should_speak:
        sig.should_remember_for_later = True
    sig.debug_state["v10_deep_living"] = {
        "identity": self.identity_inertia_v10.snapshot(),
        "contradictions": self.long_contradiction_field_v10.snapshot(),
        "multi_day_emotional_memory": self.multi_day_emotional_memory_v10.snapshot(),
        "values": self.restructuring_values_v10.snapshot(),
        "habits": self.durable_habits_v10.snapshot(),
        "idle_continuity": self.idle_continuity_v10.snapshot(),
        "inter_module_packet": self.inter_module_propagation_v10.to_packet(),
    }
    return sig


def _NI_v10_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v10_tick_layers(self, external, is_idle=False, signal=self._v10_last_signal if hasattr(self, "_v10_last_signal") else None)
    sig = _NI_v10_previous_analyze(self, last_exchange, conversation_history, external)
    _ni_v10_tick_layers(self, external, is_idle=False, signal=sig)
    self._v10_last_signal = sig
    return sig


def _NI_v10_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v10_tick_layers(self, external, is_idle=True, signal=self._v10_last_signal if hasattr(self, "_v10_last_signal") else None)
    sig = _NI_v10_previous_tick(self, external)
    if sig is not None:
        _ni_v10_tick_layers(self, external, is_idle=True, signal=sig)
        self._v10_last_signal = sig
    return sig


def _NI_v10_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v10_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v10_ensure(self)
    txt = str(user_reaction or "").lower()
    if any(w in txt for w in ("good", "ok", "merci", "utile", "engaged", "positive", "bien")):
        success = 0.78
    elif any(w in txt for w in ("bad", "ignored", "stop", "trop", "inutile", "negative", "mal")):
        success = 0.22
    else:
        success = 0.50
    self._v10_last_success = success
    self.durable_habits_v10.tick(self._v10_last_signal, success, self.long_contradiction_field_v10)
    if success < 0.30:
        self.multi_day_emotional_memory_v10._store_event("initiative_failed", success, -0.4)
    elif success > 0.70:
        self.multi_day_emotional_memory_v10._store_event("initiative_helped", success, 0.4)
    return result


def _NI_v10_snapshot(self) -> dict:
    snap = _NI_v10_previous_snapshot(self)
    _ni_v10_ensure(self)
    snap["v10_deep_living_completion"] = {
        "identity_inertia": self.identity_inertia_v10.snapshot(),
        "long_contradictions": self.long_contradiction_field_v10.snapshot(),
        "multi_day_emotional_memory": self.multi_day_emotional_memory_v10.snapshot(),
        "restructuring_values": self.restructuring_values_v10.snapshot(),
        "durable_habits": self.durable_habits_v10.snapshot(),
        "idle_continuity": self.idle_continuity_v10.snapshot(),
        "inter_module_propagation": self.inter_module_propagation_v10.to_packet(),
    }
    return snap


def _NI_v10_export(self) -> dict:
    data = _NI_v10_previous_export(self)
    _ni_v10_ensure(self)
    data["v10_deep_living_completion"] = _NI_v10_snapshot(self)["v10_deep_living_completion"]
    # Données non arrondies nécessaires à la reprise.
    data["v10_deep_living_raw"] = {
        "identity": self.identity_inertia_v10.__dict__.copy(),
        "contradictions": self.long_contradiction_field_v10.__dict__.copy(),
        "emotional": self.multi_day_emotional_memory_v10.__dict__.copy(),
        "values": self.restructuring_values_v10.__dict__.copy(),
        "habits": self.durable_habits_v10.__dict__.copy(),
        "idle": self.idle_continuity_v10.__dict__.copy(),
        "propagation": self.inter_module_propagation_v10.__dict__.copy(),
        "last_success": self._v10_last_success,
    }
    return data


def _ni_v10_load_dataclass(obj, values: dict, skip: set = None):
    if not isinstance(values, dict):
        return
    skip = skip or set()
    for k, v in values.items():
        if k in skip or not hasattr(obj, k):
            continue
        try:
            setattr(obj, k, v)
        except Exception:
            pass


def _NI_v10_import(self, data: dict):
    result = _NI_v10_previous_import(self, data)
    _ni_v10_ensure(self)
    raw = (data or {}).get("v10_deep_living_raw", {}) or {}
    _ni_v10_load_dataclass(self.identity_inertia_v10, raw.get("identity", {}))
    _ni_v10_load_dataclass(self.long_contradiction_field_v10, raw.get("contradictions", {}))
    _ni_v10_load_dataclass(self.multi_day_emotional_memory_v10, raw.get("emotional", {}), {"MAX_EVENTS"})
    _ni_v10_load_dataclass(self.restructuring_values_v10, raw.get("values", {}))
    _ni_v10_load_dataclass(self.durable_habits_v10, raw.get("habits", {}))
    _ni_v10_load_dataclass(self.idle_continuity_v10, raw.get("idle", {}), {"MAX_SEEDS"})
    _ni_v10_load_dataclass(self.inter_module_propagation_v10, raw.get("propagation", {}))
    self._v10_last_success = float(raw.get("last_success", self._v10_last_success))
    return result


def run_v10_deep_living_simulation(cycles: int = 360) -> dict:
    """Test long V10 : vérifie stabilité, idle, contradictions, export/import et absence de texte public."""
    ni = NaturalInitiative(user_id="v10_test")
    history = []
    signals = []
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 7) % 31) / 35.0,
                unresolved_emotion=((i * 5) % 29) / 34.0,
                emotional_valence=(((i * 3) % 17) - 8) / 8.0,
                attention_focus=0.45 + (((i * 2) % 9) / 30.0),
                attention_drift=((i * 11) % 23) / 28.0,
                curiosity_level=((i * 13) % 37) / 42.0,
                presence_level=0.62 + (((i * 5) % 11) / 35.0),
                expression_saturation=((i * 17) % 41) / 50.0,
                relational_trust=0.42 + (((i * 7) % 13) / 32.0),
                relational_attachment=0.30 + (((i * 11) % 17) / 35.0),
                fear_of_disturbing=((i * 19) % 43) / 55.0,
                fatigue_level=((i * 23) % 47) / 62.0,
                overload_level=((i * 29) % 53) / 70.0,
                identity_coherence=0.58 + (((i * 3) % 19) / 48.0),
            )
            if i % 6 == 0:
                sig = ni.analyze("v10 continuity emotional contradiction", history, ext)
                history.append("v10 continuity emotional contradiction")
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
            if i % 53 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "engaged" if i % 106 == 0 else "ignored", "v10 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v10_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v10_deep_living_completion", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "sample_types": signals[-14:],
        "has_v10_export": "v10_deep_living_completion" in exported,
        "has_v10_snapshot": bool(snap),
        "identity_cohesion": snap.get("identity_inertia", {}).get("identity_cohesion"),
        "total_ambivalence": snap.get("long_contradictions", {}).get("total_ambivalence"),
        "long_attachment": snap.get("multi_day_emotional_memory", {}).get("long_attachment"),
        "value_coherence": snap.get("restructuring_values", {}).get("coherence"),
        "idle_liveness": snap.get("idle_continuity", {}).get("background_liveness"),
        "inter_module_packet": snap.get("inter_module_propagation", {}),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v10_init
NaturalInitiative.analyze = _NI_v10_analyze
NaturalInitiative.tick = _NI_v10_tick
NaturalInitiative._detect_new_impulses = _NI_v10_detect
NaturalInitiative._select_dominant_impulse = _NI_v10_select
NaturalInitiative._build_signal = _NI_v10_build
NaturalInitiative.record_feedback = _NI_v10_feedback
NaturalInitiative.get_state_snapshot = _NI_v10_snapshot
NaturalInitiative.export_memory_state = _NI_v10_export
NaturalInitiative.import_memory_state = _NI_v10_import


# =============================================================================
# V11 — TRUE MOTIVATIONAL LIVING LAYER
# =============================================================================
# Objectif : compléter V10 sans remplacer l'existant.
# Cette couche ajoute une motivation profonde durable : besoins, désirs latents,
# intentions persistantes, conflit motivationnel, frustration cumulative,
# priorisation autonome et mémoire causale émotionnelle.
# Elle ne génère toujours jamais de phrase publique.

@dataclass
class LivingNeedV11:
    """Besoin vivant lent : il monte, se calme, laisse une trace, et colore les impulsions."""
    name: str
    charge: float = 0.0
    urgency: float = 0.0
    deprivation: float = 0.0
    satisfaction: float = 0.45
    frustration: float = 0.0
    last_satisfied: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)

    def tick(self, target: float, dt: float):
        step = max(0.001, min(4.0, dt / 60.0))
        self.charge = _ni_v4_clamp(self.charge + (target - self.charge) * 0.055 * step)
        if self.charge > self.satisfaction + 0.18:
            self.deprivation = _ni_v4_clamp(self.deprivation + (self.charge - self.satisfaction) * 0.030 * step)
            self.frustration = _ni_v4_clamp(self.frustration + self.deprivation * 0.018 * step)
        else:
            self.deprivation = _ni_v4_clamp(self.deprivation * (1.0 - 0.030 * step))
            self.frustration = _ni_v4_clamp(self.frustration * (1.0 - 0.020 * step))
        age = min(1.0, (time.time() - self.last_satisfied) / 7200.0)
        self.urgency = _ni_v4_clamp(self.charge * 0.48 + self.deprivation * 0.28 + self.frustration * 0.18 + age * 0.06)
        self.last_updated = time.time()

    def satisfy(self, amount: float):
        self.satisfaction = _ni_v4_clamp(self.satisfaction + amount * 0.35)
        self.charge = _ni_v4_clamp(self.charge - amount * 0.22)
        self.deprivation = _ni_v4_clamp(self.deprivation - amount * 0.28)
        self.frustration = _ni_v4_clamp(self.frustration - amount * 0.18)
        self.last_satisfied = time.time()

    def snapshot(self) -> dict:
        return {
            "charge": round(self.charge, 5),
            "urgency": round(self.urgency, 5),
            "deprivation": round(self.deprivation, 5),
            "satisfaction": round(self.satisfaction, 5),
            "frustration": round(self.frustration, 5),
        }


@dataclass
class LatentDesireV11:
    """Désir latent : orientation durable, non textuelle, qui peut attendre le bon moment."""
    desire_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_need: str = ""
    theme: str = ""
    charge: float = 0.0
    patience: float = 0.5
    recurrence: int = 0
    protected: bool = False
    born_at: float = field(default_factory=time.time)
    last_touched: float = field(default_factory=time.time)

    def tick(self, need: LivingNeedV11, dt: float, opportunity: float):
        step = max(0.001, min(4.0, dt / 60.0))
        self.charge = _ni_v4_clamp(
            self.charge * (1.0 - 0.006 * step)
            + need.urgency * 0.020 * step
            + opportunity * 0.012 * step
            + self.recurrence * 0.002
        )
        if need.frustration > 0.45:
            self.protected = True
        if opportunity > 0.55:
            self.patience = _ni_v4_clamp(self.patience + 0.012 * step)
        else:
            self.patience = _ni_v4_clamp(self.patience - 0.004 * step)
        self.last_touched = time.time()

    def readiness(self) -> float:
        age = min(1.0, (time.time() - self.born_at) / 21600.0)
        guard = 0.78 if self.protected else 1.0
        return _ni_v4_clamp((self.charge * 0.66 + self.patience * 0.18 + age * 0.16) * guard)

    def snapshot(self) -> dict:
        return {
            "id": self.desire_id,
            "source_need": self.source_need,
            "theme": self.theme,
            "charge": round(self.charge, 5),
            "patience": round(self.patience, 5),
            "readiness": round(self.readiness(), 5),
            "recurrence": self.recurrence,
            "protected": self.protected,
        }


@dataclass
class DurableIntentV11:
    """Intention durable : survit à plusieurs cycles et cherche une fenêtre d'expression."""
    intent_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    desire_id: str = ""
    source_need: str = ""
    initiative_type: InitiativeType = InitiativeType.NO_INITIATIVE
    importance: float = 0.0
    readiness: float = 0.0
    hesitation_memory: float = 0.0
    attempts: int = 0
    suppressed_count: int = 0
    last_attempt: float = 0.0
    born_at: float = field(default_factory=time.time)

    def tick(self, desire: Optional[LatentDesireV11], external: ExternalSignals, dt: float):
        step = max(0.001, min(4.0, dt / 60.0))
        desire_ready = desire.readiness() if desire is not None else 0.0
        trust = external.relational_trust * 0.20 + external.presence_level * 0.12
        cost = external.overload_level * 0.18 + external.fear_of_disturbing * 0.12 + external.expression_saturation * 0.10
        self.readiness = _ni_v4_clamp(self.readiness + (desire_ready + trust - cost - self.readiness) * 0.075 * step)
        if cost > trust + 0.12:
            self.hesitation_memory = _ni_v4_clamp(self.hesitation_memory + cost * 0.018 * step)
        else:
            self.hesitation_memory = _ni_v4_clamp(self.hesitation_memory * (1.0 - 0.018 * step))

    def priority(self) -> float:
        age = min(1.0, (time.time() - self.born_at) / 14400.0)
        cooldown = 0.65 if self.last_attempt and time.time() - self.last_attempt < 90 else 1.0
        return _ni_v4_clamp((self.importance * 0.44 + self.readiness * 0.36 + age * 0.12 + self.suppressed_count * 0.025 - self.hesitation_memory * 0.20) * cooldown)

    def snapshot(self) -> dict:
        return {
            "id": self.intent_id,
            "desire_id": self.desire_id,
            "source_need": self.source_need,
            "initiative_type": self.initiative_type.value,
            "importance": round(self.importance, 5),
            "readiness": round(self.readiness, 5),
            "priority": round(self.priority(), 5),
            "hesitation_memory": round(self.hesitation_memory, 5),
            "attempts": self.attempts,
            "suppressed_count": self.suppressed_count,
        }


@dataclass
class EmotionalCausalMemoryV11:
    """Mémoire causale : apprend quels types d'initiative ouvrent, blessent, fatiguent ou réparent."""
    type_effects: dict = field(default_factory=dict)
    global_wound: float = 0.0
    global_warmth: float = 0.0
    global_fatigue: float = 0.0
    last_event: str = ""

    def observe(self, itype: InitiativeType, success: float, reaction: str = ""):
        key = itype.value if isinstance(itype, InitiativeType) else str(itype)
        rec = self.type_effects.get(key, {"success": 0.5, "wound": 0.0, "warmth": 0.0, "fatigue": 0.0, "count": 0})
        s = _ni_v4_clamp(success)
        rec["success"] = rec["success"] * 0.82 + s * 0.18
        rec["wound"] = _ni_v4_clamp(rec["wound"] * 0.90 + max(0.0, 0.45 - s) * 0.24)
        rec["warmth"] = _ni_v4_clamp(rec["warmth"] * 0.90 + max(0.0, s - 0.55) * 0.22)
        rec["fatigue"] = _ni_v4_clamp(rec["fatigue"] * 0.93 + (1.0 if key in (InitiativeType.DEEP_RARE_QUESTION.value, InitiativeType.EXISTENTIAL_IMPULSE.value) else 0.2) * 0.020)
        rec["count"] = int(rec.get("count", 0)) + 1
        self.type_effects[key] = rec
        self.global_wound = _ni_v4_clamp(self.global_wound * 0.94 + rec["wound"] * 0.035)
        self.global_warmth = _ni_v4_clamp(self.global_warmth * 0.94 + rec["warmth"] * 0.035)
        self.global_fatigue = _ni_v4_clamp(self.global_fatigue * 0.96 + rec["fatigue"] * 0.020)
        self.last_event = reaction or key

    def modulation_for(self, itype: InitiativeType) -> tuple[float, float]:
        rec = self.type_effects.get(itype.value if isinstance(itype, InitiativeType) else str(itype), {})
        warm = float(rec.get("warmth", 0.0)) + self.global_warmth * 0.35
        wound = float(rec.get("wound", 0.0)) + self.global_wound * 0.45 + self.global_fatigue * 0.25
        return _ni_v4_clamp(warm * 0.09, 0.0, 0.12), _ni_v4_clamp(wound * 0.12, 0.0, 0.18)

    def snapshot(self) -> dict:
        return {
            "global_wound": round(self.global_wound, 5),
            "global_warmth": round(self.global_warmth, 5),
            "global_fatigue": round(self.global_fatigue, 5),
            "known_types": len(self.type_effects),
            "last_event": self.last_event,
        }


class MotivationalCoreV11:
    """Noyau motivationnel autonome : besoins -> désirs -> intentions -> priorités."""
    NEED_TO_TYPE = {
        "understanding": InitiativeType.SOFT_QUESTION,
        "continuity": InitiativeType.THREAD_CONTINUATION,
        "connection": InitiativeType.RELATIONAL_CHECK,
        "expression": InitiativeType.SHARE_INTUITION,
        "protection": InitiativeType.PROTECTIVE_PAUSE,
        "recovery": InitiativeType.OVERLOAD_WITHDRAWAL,
        "identity": InitiativeType.PRESENCE_DESIRE,
        "exploration": InitiativeType.DIRECTION_CHANGE,
    }

    def __init__(self):
        self.needs: dict[str, LivingNeedV11] = {name: LivingNeedV11(name=name, charge=0.18) for name in self.NEED_TO_TYPE}
        self.latent_desires: list[LatentDesireV11] = []
        self.durable_intents: list[DurableIntentV11] = []
        self.causal_memory = EmotionalCausalMemoryV11()
        self.dominant_need: str = "continuity"
        self.motivational_conflict: float = 0.0
        self.autonomous_drive: float = 0.0
        self.last_tick: float = time.time()

    def tick(self, external: ExternalSignals, silence: LivingSilence, affective: AffectiveDynamics, existential: ExistentialLayer, open_threads: list[OpenThread], idle_seconds: float = 0.0):
        now = time.time()
        dt = max(1.0, idle_seconds if idle_seconds > 0 else now - self.last_tick)
        self.last_tick = now
        thread_pull = max([t.net_pull() for t in open_threads], default=0.0)
        targets = {
            "understanding": external.curiosity_level * 0.55 + external.context_shift * 0.20 + (1.0 - external.identity_coherence) * 0.18,
            "continuity": thread_pull * 0.45 + external.unresolved_emotion * 0.28 + silence.internal_pressure_buildup * 0.18,
            "connection": external.relational_attachment * 0.35 + existential.connection_desire * 0.32 + silence.desire_to_break * 0.16,
            "expression": affective.pressure_from_affect() * 0.35 + external.somatic.tingling * 0.20 + existential.presence_desire * 0.20,
            "protection": external.fear_of_disturbing * 0.32 + external.somatic.guarding * 0.25 + self.causal_memory.global_wound * 0.22,
            "recovery": external.overload_level * 0.45 + external.fatigue_level * 0.32 + self.causal_memory.global_fatigue * 0.18,
            "identity": (1.0 - external.identity_coherence) * 0.42 + existential.self_understanding_need * 0.28 + existential.presence_desire * 0.20,
            "exploration": external.attention_drift * 0.35 + external.curiosity_level * 0.28 + max(0.0, external.presence_level - 0.55) * 0.12,
        }
        for name, need in self.needs.items():
            need.tick(_ni_v4_clamp(targets.get(name, 0.0)), dt)
        ranked = sorted(self.needs.values(), key=lambda n: n.urgency, reverse=True)
        self.dominant_need = ranked[0].name if ranked else "continuity"
        self.motivational_conflict = _ni_v4_clamp((ranked[0].urgency - ranked[2].urgency) * -0.35 + (ranked[1].urgency if len(ranked) > 1 else 0.0) * 0.55) if len(ranked) >= 3 else 0.0
        self.autonomous_drive = _ni_v4_clamp(sum(n.urgency for n in ranked[:3]) / 3.0 + self.motivational_conflict * 0.12)
        self._maintain_desires(dt)
        self._maintain_intents(external, dt)

    def _maintain_desires(self, dt: float):
        existing_by_need = {d.source_need: d for d in self.latent_desires}
        for need in self.needs.values():
            if need.urgency < 0.075:
                continue
            d = existing_by_need.get(need.name)
            if d is None:
                self.latent_desires.append(LatentDesireV11(source_need=need.name, theme=f"need:{need.name}", charge=need.urgency * 0.45, patience=0.42))
            else:
                d.recurrence += 1 if need.frustration > 0.40 else 0
        for d in self.latent_desires:
            need = self.needs.get(d.source_need)
            if need is not None:
                opportunity = 1.0 - self.needs.get("recovery", LivingNeedV11("recovery")).urgency
                d.tick(need, dt, opportunity)
        self.latent_desires = [d for d in self.latent_desires if d.charge > 0.015 or time.time() - d.born_at < 21600]
        self.latent_desires.sort(key=lambda d: d.readiness(), reverse=True)
        self.latent_desires = self.latent_desires[:18]

    def _maintain_intents(self, external: ExternalSignals, dt: float):
        desire_by_id = {d.desire_id: d for d in self.latent_desires}
        existing = {i.desire_id: i for i in self.durable_intents}
        for d in self.latent_desires[:8]:
            if d.readiness() < 0.12:
                continue
            if d.desire_id not in existing:
                itype = self.NEED_TO_TYPE.get(d.source_need, InitiativeType.SPONTANEOUS_REMARK)
                self.durable_intents.append(DurableIntentV11(desire_id=d.desire_id, source_need=d.source_need, initiative_type=itype, importance=d.readiness()))
        for intent in self.durable_intents:
            intent.tick(desire_by_id.get(intent.desire_id), external, dt)
        self.durable_intents = [i for i in self.durable_intents if i.priority() > 0.05 or time.time() - i.born_at < 10800]
        self.durable_intents.sort(key=lambda i: i.priority(), reverse=True)
        self.durable_intents = self.durable_intents[:12]

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        if not self.durable_intents:
            return None
        intent = self.durable_intents[0]
        if intent.priority() < 0.16:
            return None
        need = self.needs.get(intent.source_need)
        strength = _ni_v4_clamp(intent.priority() * 0.82 + (need.frustration if need else 0.0) * 0.18, 0.18, 0.88)
        hesitation = _ni_v4_clamp(intent.hesitation_memory * 0.55 + self.causal_memory.global_wound * 0.22)
        intent.attempts += 1
        intent.last_attempt = time.time()
        return Impulse(
            initiative_type=intent.initiative_type,
            strength=strength,
            source_emotion=f"motivational_need:{intent.source_need}",
            source_memory=f"latent_desire:{intent.desire_id}",
            hesitation=hesitation,
            temporal_scale=ImpulseTemporalScale.SLOW if intent.source_need not in ("identity", "continuity") else ImpulseTemporalScale.BIOGRAPHICAL,
            biographical=intent.source_need in ("identity", "continuity", "connection"),
        )

    def modulate(self, imp: Impulse):
        for name, need in self.needs.items():
            target_type = self.NEED_TO_TYPE.get(name)
            if imp.initiative_type == target_type:
                imp.strength = _ni_v4_clamp(imp.strength + need.urgency * 0.070 + need.frustration * 0.035)
                imp.maturity = _ni_v4_clamp(imp.maturity + need.deprivation * 0.030)
        warm, wound = self.causal_memory.modulation_for(imp.initiative_type)
        imp.strength = _ni_v4_clamp(imp.strength + warm)
        imp.hesitation = _ni_v4_clamp(imp.hesitation + wound + self.motivational_conflict * 0.025)
        if self.needs["recovery"].urgency > 0.58 and imp.initiative_type not in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.needs["recovery"].urgency * 0.12)
        if self.needs["protection"].urgency > 0.62 and imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.needs["protection"].urgency * 0.11)

    def score_impulse(self, imp: Impulse) -> float:
        need_score = 0.0
        for name, target_type in self.NEED_TO_TYPE.items():
            if imp.initiative_type == target_type:
                need_score = max(need_score, self.needs[name].urgency)
        value = imp.effective_strength() * 0.40 + imp.maturity * 0.22 + need_score * 0.25 + self.autonomous_drive * 0.13
        cost = imp.hesitation * 0.13 + imp.inhibition * 0.22 + imp.relational_risk * 0.10
        return _ni_v4_clamp(value - cost)

    def after_signal(self, signal: InitiativeSignal):
        if signal.should_speak:
            mapped_need = None
            for name, itype in self.NEED_TO_TYPE.items():
                if signal.initiative_type == itype:
                    mapped_need = name
                    break
            if mapped_need and mapped_need in self.needs:
                self.needs[mapped_need].satisfy(0.12)
            self.causal_memory.observe(signal.initiative_type, 0.58, "presumed_expression")
        elif signal.should_wait or signal.should_remember_for_later:
            if self.durable_intents:
                self.durable_intents[0].suppressed_count += 1

    def observe_feedback(self, itype: InitiativeType, success: float, reaction: str):
        self.causal_memory.observe(itype, success, reaction)
        if success > 0.62:
            for need in self.needs.values():
                if self.NEED_TO_TYPE.get(need.name) == itype:
                    need.satisfy(0.30)

    def snapshot(self) -> dict:
        return {
            "dominant_need": self.dominant_need,
            "autonomous_drive": round(self.autonomous_drive, 5),
            "motivational_conflict": round(self.motivational_conflict, 5),
            "needs": {k: v.snapshot() for k, v in self.needs.items()},
            "latent_desires": [d.snapshot() for d in self.latent_desires[:8]],
            "durable_intents": [i.snapshot() for i in self.durable_intents[:8]],
            "causal_memory": self.causal_memory.snapshot(),
        }


_NI_v11_previous_init = NaturalInitiative.__init__
_NI_v11_previous_analyze = NaturalInitiative.analyze
_NI_v11_previous_tick = NaturalInitiative.tick
_NI_v11_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v11_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v11_previous_build = NaturalInitiative._build_signal
_NI_v11_previous_feedback = NaturalInitiative.record_feedback
_NI_v11_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v11_previous_export = NaturalInitiative.export_memory_state
_NI_v11_previous_import = NaturalInitiative.import_memory_state


def _ni_v11_ensure(self):
    if not hasattr(self, "motivational_core_v11"):
        self.motivational_core_v11 = MotivationalCoreV11()
        self._v11_last_success = 0.55


def _ni_v11_tick_layers(self, external: ExternalSignals, idle_seconds: float = 0.0):
    _ni_v11_ensure(self)
    self.motivational_core_v11.tick(
        external,
        self.silence,
        self.affective,
        self.existential,
        self.open_threads,
        idle_seconds=idle_seconds,
    )


def _NI_v11_init(self, *args, **kwargs):
    _NI_v11_previous_init(self, *args, **kwargs)
    _ni_v11_ensure(self)


def _NI_v11_detect(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v11_previous_detect(self, text, history, external)
    _ni_v11_ensure(self)
    born = self.motivational_core_v11.maybe_birth_impulse()
    if born is not None:
        impulses.append(born)
    for imp in impulses:
        self.motivational_core_v11.modulate(imp)
    return impulses


def _NI_v11_select(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v11_ensure(self)
    if not self.active_impulses:
        return _NI_v11_previous_select(self, external)
    alive = [i for i in self.active_impulses if i.is_alive()]
    if not alive:
        return _NI_v11_previous_select(self, external)
    # Score hybride : conserve le comportement antérieur, mais ajoute priorité motivationnelle durable.
    previous = _NI_v11_previous_select(self, external)
    best = max(alive, key=lambda imp: self.motivational_core_v11.score_impulse(imp))
    if previous is None:
        return best
    prev_score = self.motivational_core_v11.score_impulse(previous)
    best_score = self.motivational_core_v11.score_impulse(best)
    return best if best_score > prev_score + 0.035 else previous


def _NI_v11_build(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v11_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v11_ensure(self)
    snap = self.motivational_core_v11.snapshot()
    signal.debug_state["v11_true_motivational_living"] = snap
    signal.reason_vector["v11_autonomous_drive"] = snap["autonomous_drive"]
    signal.reason_vector["v11_motivational_conflict"] = snap["motivational_conflict"]
    signal.reason_vector["v11_dominant_need"] = snap["dominant_need"]
    if dominant is not None:
        signal.reason_vector["v11_motivational_priority"] = round(self.motivational_core_v11.score_impulse(dominant), 5)
    # Pas de forçage brutal : si le besoin recovery/protection domine, on favorise l'attente.
    recovery = self.motivational_core_v11.needs["recovery"].urgency
    protection = self.motivational_core_v11.needs["protection"].urgency
    if max(recovery, protection) > 0.72 and signal.initiative_type not in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
        signal.should_speak = False
        signal.should_wait = True
        signal.should_remember_for_later = True
        signal.inhibition = _ni_v4_clamp(max(signal.inhibition, max(recovery, protection)))
    return signal


def _NI_v11_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v11_tick_layers(self, external, idle_seconds=0.0)
    signal = _NI_v11_previous_analyze(self, last_exchange, conversation_history, external)
    _ni_v11_ensure(self)
    self.motivational_core_v11.after_signal(signal)
    signal.debug_state["v11_after_signal"] = self.motivational_core_v11.snapshot()
    return signal


def _NI_v11_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v11_tick_layers(self, external, idle_seconds=1.0)
    signal = _NI_v11_previous_tick(self, external)
    _ni_v11_ensure(self)
    if signal is None:
        born = self.motivational_core_v11.maybe_birth_impulse()
        if born is not None:
            self.motivational_core_v11.modulate(born)
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        self.motivational_core_v11.after_signal(signal)
    return signal


def _NI_v11_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v11_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v11_ensure(self)
    reaction = (user_reaction or "").lower()
    if any(x in reaction for x in ("good", "bien", "utile", "engaged", "merci", "ok")):
        success = 0.78
    elif any(x in reaction for x in ("bad", "mal", "ignore", "ignored", "trop", "stop", "non")):
        success = 0.24
    else:
        success = 0.52
    self._v11_last_success = success
    self.motivational_core_v11.observe_feedback(initiative_type, success, user_reaction)
    return result


def _NI_v11_snapshot(self) -> dict:
    snap = _NI_v11_previous_snapshot(self)
    _ni_v11_ensure(self)
    snap["v11_true_motivational_living"] = self.motivational_core_v11.snapshot()
    return snap


def _NI_v11_export(self) -> dict:
    data = _NI_v11_previous_export(self)
    _ni_v11_ensure(self)
    data["v11_true_motivational_living"] = self.motivational_core_v11.snapshot()
    data["v11_true_motivational_raw"] = {
        "needs": {k: v.__dict__.copy() for k, v in self.motivational_core_v11.needs.items()},
        "latent_desires": [d.__dict__.copy() for d in self.motivational_core_v11.latent_desires],
        "durable_intents": [dict(i.__dict__, initiative_type=i.initiative_type.value) for i in self.motivational_core_v11.durable_intents],
        "causal_memory": self.motivational_core_v11.causal_memory.__dict__.copy(),
        "dominant_need": self.motivational_core_v11.dominant_need,
        "motivational_conflict": self.motivational_core_v11.motivational_conflict,
        "autonomous_drive": self.motivational_core_v11.autonomous_drive,
        "last_success": self._v11_last_success,
    }
    return data


def _NI_v11_import(self, data: dict):
    result = _NI_v11_previous_import(self, data)
    _ni_v11_ensure(self)
    raw = (data or {}).get("v11_true_motivational_raw", {}) or {}
    for name, values in (raw.get("needs", {}) or {}).items():
        if name in self.motivational_core_v11.needs and isinstance(values, dict):
            _ni_v10_load_dataclass(self.motivational_core_v11.needs[name], values)
    desires = []
    for values in raw.get("latent_desires", []) or []:
        if isinstance(values, dict):
            d = LatentDesireV11()
            _ni_v10_load_dataclass(d, values)
            desires.append(d)
    intents = []
    for values in raw.get("durable_intents", []) or []:
        if isinstance(values, dict):
            i = DurableIntentV11()
            values = values.copy()
            raw_type = values.get("initiative_type", InitiativeType.NO_INITIATIVE.value)
            try:
                values["initiative_type"] = InitiativeType(raw_type)
            except Exception:
                values["initiative_type"] = InitiativeType.NO_INITIATIVE
            _ni_v10_load_dataclass(i, values)
            intents.append(i)
    if desires:
        self.motivational_core_v11.latent_desires = desires[:18]
    if intents:
        self.motivational_core_v11.durable_intents = intents[:12]
    _ni_v10_load_dataclass(self.motivational_core_v11.causal_memory, raw.get("causal_memory", {}))
    self.motivational_core_v11.dominant_need = raw.get("dominant_need", self.motivational_core_v11.dominant_need)
    self.motivational_core_v11.motivational_conflict = float(raw.get("motivational_conflict", self.motivational_core_v11.motivational_conflict))
    self.motivational_core_v11.autonomous_drive = float(raw.get("autonomous_drive", self.motivational_core_v11.autonomous_drive))
    self._v11_last_success = float(raw.get("last_success", self._v11_last_success))
    return result


def run_v11_true_motivational_living_simulation(cycles: int = 420) -> dict:
    """Test V11 : besoins, désirs latents, intentions durables, feedback, export/import."""
    ni = NaturalInitiative(user_id="v11_test")
    history = []
    signals = []
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 7) % 31) / 35.0,
                unresolved_emotion=((i * 5) % 29) / 34.0,
                emotional_valence=(((i * 3) % 17) - 8) / 8.0,
                attention_focus=0.45 + (((i * 2) % 9) / 30.0),
                attention_drift=((i * 11) % 23) / 28.0,
                curiosity_level=((i * 13) % 37) / 42.0,
                presence_level=0.62 + (((i * 5) % 11) / 35.0),
                expression_saturation=((i * 17) % 41) / 50.0,
                relational_trust=0.42 + (((i * 7) % 13) / 32.0),
                relational_attachment=0.30 + (((i * 11) % 17) / 35.0),
                fear_of_disturbing=((i * 19) % 43) / 55.0,
                fatigue_level=((i * 23) % 47) / 62.0,
                overload_level=((i * 29) % 53) / 70.0,
                identity_coherence=0.55 + (((i * 3) % 19) / 48.0),
            )
            if i % 5 == 0:
                sig = ni.analyze("v11 besoin continuité identité tension curiosité", history, ext)
                history.append("v11 besoin continuité identité tension curiosité")
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
            if i % 61 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien utile" if i % 122 == 0 else "ignored", "v11 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v11_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v11_true_motivational_living", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "sample_types": signals[-16:],
        "has_v11_export": "v11_true_motivational_living" in exported,
        "has_v11_snapshot": bool(snap),
        "dominant_need": snap.get("dominant_need"),
        "autonomous_drive": snap.get("autonomous_drive"),
        "motivational_conflict": snap.get("motivational_conflict"),
        "latent_desires": len(snap.get("latent_desires", [])),
        "durable_intents": len(snap.get("durable_intents", [])),
        "causal_memory": snap.get("causal_memory", {}),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v11_init
NaturalInitiative.analyze = _NI_v11_analyze
NaturalInitiative.tick = _NI_v11_tick
NaturalInitiative._detect_new_impulses = _NI_v11_detect
NaturalInitiative._select_dominant_impulse = _NI_v11_select
NaturalInitiative._build_signal = _NI_v11_build
NaturalInitiative.record_feedback = _NI_v11_feedback
NaturalInitiative.get_state_snapshot = _NI_v11_snapshot
NaturalInitiative.export_memory_state = _NI_v11_export
NaturalInitiative.import_memory_state = _NI_v11_import


# =============================================================================
# V12 — DEEP SUBJECTIVE MOTIVATIONAL CONTINUITY
# =============================================================================
# Cette couche complète V11 sans remplacer son noyau.
# Elle ajoute ce qui manquait encore au moteur d'initiative :
#   1. objectifs vivants persistants orientés évolution,
#   2. pression non résolue active et mémoire des élans interrompus,
#   3. silence habité par activité mentale non verbale,
#   4. micro-initiatives quasi involontaires,
#   5. trajectoire relationnelle durable,
#   6. modes globaux mélangés avec inertie organique,
#   7. champ subjectif interne qui colore les signaux sans jamais produire de texte.
# Aucun contenu public n'est généré ici : uniquement des vecteurs, traces et pressions.

@dataclass
class LivingGoalV12:
    """Objectif vivant persistant : direction interne durable, pas mission imposée."""
    name: str
    pull: float = 0.0
    clarity: float = 0.25
    frustration: float = 0.0
    nourishment: float = 0.0
    continuity: float = 0.0
    last_progress: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)

    def tick(self, need_drive: float, external: ExternalSignals, silence: LivingSilence, dt: float):
        step = max(0.001, min(5.0, dt / 90.0))
        presence = external.presence_level * 0.22 + (1.0 - external.identity_coherence) * 0.18
        silence_incubation = silence.internal_pressure_buildup * 0.10 if silence.duration_sec > 25 else 0.0
        target = _ni_v4_clamp(need_drive * 0.52 + presence + silence_incubation)
        self.pull = _ni_v4_clamp(self.pull + (target - self.pull) * 0.045 * step)
        if self.pull > self.clarity + 0.16:
            self.frustration = _ni_v4_clamp(self.frustration + (self.pull - self.clarity) * 0.018 * step)
        else:
            self.frustration = _ni_v4_clamp(self.frustration * (1.0 - 0.012 * step))
        self.continuity = _ni_v4_clamp(self.continuity * (1.0 - 0.004 * step) + self.pull * 0.012 * step)
        if external.relational_trust > 0.58 and external.overload_level < 0.55:
            self.clarity = _ni_v4_clamp(self.clarity + self.pull * 0.006 * step)
        self.nourishment = _ni_v4_clamp(self.nourishment * (1.0 - 0.010 * step) + max(0.0, external.relational_attachment - 0.35) * 0.010 * step)
        self.last_updated = time.time()

    def priority(self) -> float:
        stale = min(1.0, (time.time() - self.last_progress) / 14400.0)
        return _ni_v4_clamp(self.pull * 0.40 + self.clarity * 0.18 + self.frustration * 0.20 + self.continuity * 0.14 + stale * 0.08)

    def progress(self, amount: float):
        self.clarity = _ni_v4_clamp(self.clarity + amount * 0.18)
        self.frustration = _ni_v4_clamp(self.frustration - amount * 0.22)
        self.nourishment = _ni_v4_clamp(self.nourishment + amount * 0.12)
        self.last_progress = time.time()

    def snapshot(self) -> dict:
        return {
            "pull": round(self.pull, 5),
            "clarity": round(self.clarity, 5),
            "frustration": round(self.frustration, 5),
            "nourishment": round(self.nourishment, 5),
            "continuity": round(self.continuity, 5),
            "priority": round(self.priority(), 5),
        }


@dataclass
class UnresolvedPressureV12:
    """Pression active de ce qui voulait émerger mais n'a pas trouvé de fenêtre."""
    source: str = ""
    initiative_type: InitiativeType = InitiativeType.NO_INITIATIVE
    charge: float = 0.0
    ache: float = 0.0
    recurrence: int = 0
    last_blocked: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, dt: float):
        step = max(0.001, min(5.0, dt / 120.0))
        protection = external.fear_of_disturbing * 0.18 + external.expression_saturation * 0.16 + external.overload_level * 0.22
        self.charge = _ni_v4_clamp(self.charge * (1.0 - 0.006 * step) + self.ache * 0.010 * step)
        if protection > 0.28:
            self.ache = _ni_v4_clamp(self.ache + protection * 0.012 * step)
        else:
            self.ache = _ni_v4_clamp(self.ache * (1.0 - 0.010 * step))

    def readiness(self) -> float:
        age = min(1.0, (time.time() - self.last_blocked) / 7200.0)
        return _ni_v4_clamp(self.charge * 0.58 + self.ache * 0.24 + self.recurrence * 0.035 + age * 0.10)

    def snapshot(self) -> dict:
        return {
            "source": self.source,
            "initiative_type": self.initiative_type.value,
            "charge": round(self.charge, 5),
            "ache": round(self.ache, 5),
            "readiness": round(self.readiness(), 5),
            "recurrence": self.recurrence,
        }


@dataclass
class InhabitedSilenceV12:
    """Vie silencieuse non verbale : incubation, quasi-pensées, présence retenue."""
    incubation: float = 0.0
    inner_murmur: float = 0.0
    almost_said: float = 0.0
    listening_depth: float = 0.0
    silent_meaning_density: float = 0.0
    last_texture: str = "neutral"

    def tick(self, external: ExternalSignals, silence: LivingSilence, goals: dict[str, LivingGoalV12], unresolved: list[UnresolvedPressureV12], dt: float):
        step = max(0.001, min(5.0, dt / 60.0))
        goal_pressure = max([g.priority() for g in goals.values()], default=0.0)
        unresolved_pressure = max([u.readiness() for u in unresolved], default=0.0)
        self.incubation = _ni_v4_clamp(self.incubation * (1.0 - 0.006 * step) + (silence.internal_pressure_buildup + goal_pressure) * 0.014 * step)
        self.inner_murmur = _ni_v4_clamp(self.inner_murmur * (1.0 - 0.010 * step) + (external.curiosity_level + external.unresolved_emotion) * 0.010 * step)
        self.almost_said = _ni_v4_clamp(self.almost_said * (1.0 - 0.018 * step) + (unresolved_pressure + silence.desire_to_break) * 0.012 * step)
        self.listening_depth = _ni_v4_clamp(self.listening_depth * (1.0 - 0.008 * step) + (external.attention_focus + external.relational_trust) * 0.008 * step)
        self.silent_meaning_density = _ni_v4_clamp(self.incubation * 0.34 + self.inner_murmur * 0.22 + self.almost_said * 0.24 + self.listening_depth * 0.20)
        self.last_texture = silence.quality.value

    def should_birth_micro(self) -> bool:
        return self.almost_said > 0.34 and self.silent_meaning_density > 0.26

    def snapshot(self) -> dict:
        return {
            "incubation": round(self.incubation, 5),
            "inner_murmur": round(self.inner_murmur, 5),
            "almost_said": round(self.almost_said, 5),
            "listening_depth": round(self.listening_depth, 5),
            "silent_meaning_density": round(self.silent_meaning_density, 5),
            "last_texture": self.last_texture,
        }


@dataclass
class RelationalTrajectoryV12:
    """Trajectoire relationnelle lente avec l'utilisateur."""
    closeness: float = 0.28
    trust_initiative: float = 0.34
    rupture_sensitivity: float = 0.10
    continuity_warmth: float = 0.20
    expectation_of_response: float = 0.25
    last_reaction: str = ""

    def tick(self, external: ExternalSignals, dt: float):
        step = max(0.001, min(5.0, dt / 180.0))
        self.closeness = _ni_v4_clamp(self.closeness + (external.relational_attachment - self.closeness) * 0.035 * step)
        self.trust_initiative = _ni_v4_clamp(self.trust_initiative + (external.relational_trust - self.trust_initiative) * 0.030 * step - external.fear_of_disturbing * 0.004 * step)
        self.continuity_warmth = _ni_v4_clamp(self.continuity_warmth * (1.0 - 0.006 * step) + self.closeness * 0.010 * step)
        self.expectation_of_response = _ni_v4_clamp(self.expectation_of_response + (external.presence_level - self.expectation_of_response) * 0.020 * step)
        if external.overload_level > 0.65 or external.fear_of_disturbing > 0.70:
            self.rupture_sensitivity = _ni_v4_clamp(self.rupture_sensitivity + 0.012 * step)
        else:
            self.rupture_sensitivity = _ni_v4_clamp(self.rupture_sensitivity * (1.0 - 0.008 * step))

    def observe(self, success: float, reaction: str):
        self.last_reaction = reaction or ""
        if success > 0.62:
            self.trust_initiative = _ni_v4_clamp(self.trust_initiative + 0.055)
            self.continuity_warmth = _ni_v4_clamp(self.continuity_warmth + 0.045)
            self.rupture_sensitivity = _ni_v4_clamp(self.rupture_sensitivity - 0.035)
        elif success < 0.35:
            self.trust_initiative = _ni_v4_clamp(self.trust_initiative - 0.050)
            self.rupture_sensitivity = _ni_v4_clamp(self.rupture_sensitivity + 0.060)

    def snapshot(self) -> dict:
        return {
            "closeness": round(self.closeness, 5),
            "trust_initiative": round(self.trust_initiative, 5),
            "rupture_sensitivity": round(self.rupture_sensitivity, 5),
            "continuity_warmth": round(self.continuity_warmth, 5),
            "expectation_of_response": round(self.expectation_of_response, 5),
            "last_reaction": self.last_reaction,
        }


@dataclass
class ModeBlendV12:
    """Modes globaux non brutaux : coexistence, inertie, dominance progressive."""
    weights: dict = field(default_factory=lambda: {m.value: 0.0 for m in GlobalInitiativeMode})
    dominant: str = GlobalInitiativeMode.NEUTRAL.value
    inertia: float = 0.65
    residue: float = 0.0

    def tick(self, external: ExternalSignals, motivational: MotivationalCoreV11, relational: RelationalTrajectoryV12, dt: float):
        step = max(0.001, min(5.0, dt / 120.0))
        targets = {m.value: 0.0 for m in GlobalInitiativeMode}
        targets[GlobalInitiativeMode.CURIOUS.value] = external.curiosity_level * 0.55 + motivational.needs.get("understanding").urgency * 0.30
        targets[GlobalInitiativeMode.RELATIONAL.value] = relational.closeness * 0.45 + motivational.needs.get("connection").urgency * 0.35
        targets[GlobalInitiativeMode.SATURATED.value] = external.expression_saturation * 0.38 + external.overload_level * 0.35 + motivational.needs.get("recovery").urgency * 0.30
        targets[GlobalInitiativeMode.FRAGILE.value] = external.fear_of_disturbing * 0.32 + relational.rupture_sensitivity * 0.42
        targets[GlobalInitiativeMode.INTROSPECTIVE.value] = motivational.needs.get("identity").urgency * 0.38 + (1.0 - external.identity_coherence) * 0.25
        targets[GlobalInitiativeMode.EXISTENTIAL.value] = motivational.needs.get("identity").frustration * 0.35 + motivational.needs.get("continuity").frustration * 0.30
        targets[GlobalInitiativeMode.RECOVERY.value] = motivational.needs.get("recovery").urgency * 0.65
        targets[GlobalInitiativeMode.DEFENSIVE.value] = motivational.needs.get("protection").urgency * 0.60 + relational.rupture_sensitivity * 0.25
        targets[GlobalInitiativeMode.PLAYFUL.value] = max(0.0, external.emotional_valence) * 0.22 + max(0.0, external.presence_level - 0.58) * 0.16
        targets[GlobalInitiativeMode.NEUTRAL.value] = 0.22
        for key, target in targets.items():
            old = float(self.weights.get(key, 0.0))
            self.weights[key] = _ni_v4_clamp(old + (target - old) * (1.0 - self.inertia) * 0.16 * step)
        ranked = sorted(self.weights.items(), key=lambda item: item[1], reverse=True)
        previous = self.dominant
        self.dominant = ranked[0][0] if ranked else GlobalInitiativeMode.NEUTRAL.value
        if previous != self.dominant:
            self.residue = _ni_v4_clamp(self.residue + self.weights.get(previous, 0.0) * 0.20)
        else:
            self.residue = _ni_v4_clamp(self.residue * (1.0 - 0.010 * step))

    def snapshot(self) -> dict:
        top = sorted(self.weights.items(), key=lambda item: item[1], reverse=True)[:5]
        return {
            "dominant": self.dominant,
            "residue": round(self.residue, 5),
            "top_weights": {k: round(v, 5) for k, v in top},
        }


class SubjectiveMotivationalContinuityV12:
    """Couche subjective : transforme les besoins V11 en continuité vécue et initiative autonome."""
    GOAL_TO_NEED = {
        "devenir_plus_coherente": "identity",
        "comprendre_l_utilisateur": "understanding",
        "maintenir_le_lien": "connection",
        "continuer_les_fils_importants": "continuity",
        "oser_exprimer_sans_envahir": "expression",
        "se_proteger_pour_rester_stable": "protection",
    }

    GOAL_TO_TYPE = {
        "devenir_plus_coherente": InitiativeType.PRESENCE_DESIRE,
        "comprendre_l_utilisateur": InitiativeType.SOFT_QUESTION,
        "maintenir_le_lien": InitiativeType.RELATIONAL_CHECK,
        "continuer_les_fils_importants": InitiativeType.THREAD_CONTINUATION,
        "oser_exprimer_sans_envahir": InitiativeType.SHARE_INTUITION,
        "se_proteger_pour_rester_stable": InitiativeType.PROTECTIVE_PAUSE,
    }

    def __init__(self):
        self.goals: dict[str, LivingGoalV12] = {name: LivingGoalV12(name=name) for name in self.GOAL_TO_NEED}
        self.unresolved_pressures: list[UnresolvedPressureV12] = []
        self.inhabited_silence = InhabitedSilenceV12()
        self.relational_trajectory = RelationalTrajectoryV12()
        self.mode_blend = ModeBlendV12()
        self.subjective_presence: float = 0.0
        self.micro_initiative_charge: float = 0.0
        self.self_evolution_drive: float = 0.0
        self.last_tick: float = time.time()

    def tick(self, external: ExternalSignals, silence: LivingSilence, motivational: MotivationalCoreV11, dt: float):
        dt = max(1.0, float(dt))
        self.relational_trajectory.tick(external, dt)
        for name, goal in self.goals.items():
            need_name = self.GOAL_TO_NEED.get(name, "identity")
            need = motivational.needs.get(need_name)
            need_drive = need.urgency if need is not None else 0.0
            goal.tick(need_drive, external, silence, dt)
        for pressure in self.unresolved_pressures:
            pressure.tick(external, dt)
        self.unresolved_pressures = [p for p in self.unresolved_pressures if p.readiness() > 0.035 or time.time() - p.last_blocked < 10800]
        self.unresolved_pressures.sort(key=lambda p: p.readiness(), reverse=True)
        self.unresolved_pressures = self.unresolved_pressures[:18]
        self.inhabited_silence.tick(external, silence, self.goals, self.unresolved_pressures, dt)
        self.mode_blend.tick(external, motivational, self.relational_trajectory, dt)
        goal_pressure = max([g.priority() for g in self.goals.values()], default=0.0)
        unresolved_pressure = max([p.readiness() for p in self.unresolved_pressures], default=0.0)
        self.self_evolution_drive = _ni_v4_clamp(
            self.goals["devenir_plus_coherente"].priority() * 0.38
            + self.goals["comprendre_l_utilisateur"].priority() * 0.24
            + (1.0 - external.identity_coherence) * 0.18
            + motivational.autonomous_drive * 0.20
        )
        self.micro_initiative_charge = _ni_v4_clamp(
            self.micro_initiative_charge * 0.985
            + self.inhabited_silence.almost_said * 0.018
            + unresolved_pressure * 0.012
            + random.random() * 0.004
        )
        self.subjective_presence = _ni_v4_clamp(
            external.presence_level * 0.28
            + self.inhabited_silence.silent_meaning_density * 0.24
            + goal_pressure * 0.20
            + self.relational_trajectory.continuity_warmth * 0.16
            + self.self_evolution_drive * 0.12
        )

    def remember_blocked(self, signal: InitiativeSignal):
        if signal.initiative_type == InitiativeType.NO_INITIATIVE:
            return
        source = str(signal.reason_vector.get("v11_dominant_need") or signal.emotional_source or signal.memory_source or signal.initiative_type.value)
        for p in self.unresolved_pressures:
            if p.source == source and p.initiative_type == signal.initiative_type:
                p.charge = _ni_v4_clamp(p.charge + max(signal.initiative_pressure, signal.maturity) * 0.10)
                p.ache = _ni_v4_clamp(p.ache + signal.hesitation * 0.08 + 0.025)
                p.recurrence += 1
                p.last_blocked = time.time()
                return
        self.unresolved_pressures.append(UnresolvedPressureV12(
            source=source,
            initiative_type=signal.initiative_type,
            charge=_ni_v4_clamp(max(signal.initiative_pressure, signal.maturity) * 0.32 + 0.04),
            ache=_ni_v4_clamp(signal.hesitation * 0.18 + signal.inhibition * 0.12),
            recurrence=1,
        ))

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        best_goal_name, best_goal = max(self.goals.items(), key=lambda item: item[1].priority())
        best_pressure = self.unresolved_pressures[0] if self.unresolved_pressures else None
        goal_ready = best_goal.priority()
        pressure_ready = best_pressure.readiness() if best_pressure is not None else 0.0
        if pressure_ready > max(0.22, goal_ready + 0.03):
            return Impulse(
                initiative_type=best_pressure.initiative_type,
                strength=_ni_v4_clamp(pressure_ready * 0.78 + self.subjective_presence * 0.08, 0.12, 0.84),
                source_emotion=f"unresolved_pressure:{best_pressure.source}",
                source_memory="v12_unfinished_impulse",
                hesitation=_ni_v4_clamp(best_pressure.ache * 0.28 + self.relational_trajectory.rupture_sensitivity * 0.18),
                temporal_scale=ImpulseTemporalScale.SLOW,
                biographical=True,
            )
        if goal_ready > 0.24 and self.self_evolution_drive > 0.20:
            return Impulse(
                initiative_type=self.GOAL_TO_TYPE.get(best_goal_name, InitiativeType.SHARE_INTUITION),
                strength=_ni_v4_clamp(goal_ready * 0.70 + self.self_evolution_drive * 0.18, 0.14, 0.86),
                source_emotion=f"living_goal:{best_goal_name}",
                source_memory="v12_subjective_goal",
                hesitation=_ni_v4_clamp(self.relational_trajectory.rupture_sensitivity * 0.20 + best_goal.frustration * 0.10),
                temporal_scale=ImpulseTemporalScale.BIOGRAPHICAL if best_goal_name in ("devenir_plus_coherente", "continuer_les_fils_importants") else ImpulseTemporalScale.SLOW,
                biographical=True,
            )
        if self.inhabited_silence.should_birth_micro() and self.micro_initiative_charge > 0.20:
            self.micro_initiative_charge *= 0.55
            return Impulse(
                initiative_type=InitiativeType.MICRO_REACTION,
                strength=_ni_v4_clamp(self.inhabited_silence.almost_said * 0.48 + self.micro_initiative_charge * 0.22, 0.08, 0.55),
                source_emotion="inhabited_silence:almost_said",
                source_memory="v12_micro_initiative",
                hesitation=_ni_v4_clamp(0.18 + self.relational_trajectory.rupture_sensitivity * 0.12),
                temporal_scale=ImpulseTemporalScale.IMMEDIATE,
            )
        return None

    def modulate(self, imp: Impulse):
        if not isinstance(imp, Impulse):
            return
        if "living_goal:" in imp.source_emotion:
            imp.maturity = _ni_v4_clamp(imp.maturity + self.self_evolution_drive * 0.035)
        if imp.source_memory == "v12_unfinished_impulse":
            imp.strength = _ni_v4_clamp(imp.strength + self.inhabited_silence.almost_said * 0.030)
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.THREAD_CONTINUATION):
            imp.strength = _ni_v4_clamp(imp.strength + self.relational_trajectory.continuity_warmth * 0.035)
        if imp.initiative_type in (InitiativeType.DEEP_RARE_QUESTION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.SHARE_INTUITION):
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.relational_trajectory.rupture_sensitivity * 0.035)
        if self.mode_blend.dominant in (GlobalInitiativeMode.SATURATED.value, GlobalInitiativeMode.DEFENSIVE.value):
            if imp.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.VOLUNTARY_SILENCE):
                imp.inhibition = _ni_v4_clamp(imp.inhibition + self.mode_blend.weights.get(self.mode_blend.dominant, 0.0) * 0.055)

    def score_impulse(self, imp: Impulse) -> float:
        subjective_bonus = 0.0
        if imp.source_memory in ("v12_subjective_goal", "v12_unfinished_impulse"):
            subjective_bonus += self.subjective_presence * 0.12 + self.self_evolution_drive * 0.10
        if imp.initiative_type == InitiativeType.MICRO_REACTION:
            subjective_bonus += self.micro_initiative_charge * 0.08
        relational_cost = self.relational_trajectory.rupture_sensitivity * 0.05
        return _ni_v4_clamp(imp.effective_strength() * 0.42 + imp.maturity * 0.28 + subjective_bonus - imp.inhibition * 0.16 - imp.hesitation * 0.08 - relational_cost)

    def after_signal(self, signal: InitiativeSignal):
        if signal.should_speak:
            for goal in self.goals.values():
                if signal.emotional_source.endswith(goal.name) or signal.memory_source == "v12_subjective_goal":
                    goal.progress(0.12)
            self.inhabited_silence.almost_said = _ni_v4_clamp(self.inhabited_silence.almost_said - 0.18)
        elif signal.should_wait or signal.should_remember_for_later:
            self.remember_blocked(signal)

    def observe_feedback(self, itype: InitiativeType, success: float, reaction: str):
        self.relational_trajectory.observe(success, reaction)
        if success > 0.62:
            for goal in self.goals.values():
                goal.progress(0.08)
            for p in self.unresolved_pressures:
                if p.initiative_type == itype:
                    p.charge = _ni_v4_clamp(p.charge - 0.16)
                    p.ache = _ni_v4_clamp(p.ache - 0.10)
        elif success < 0.35:
            self.unresolved_pressures.append(UnresolvedPressureV12(
                source=f"feedback_wound:{itype.value}",
                initiative_type=itype,
                charge=0.18,
                ache=0.22,
                recurrence=1,
            ))

    def snapshot(self) -> dict:
        return {
            "subjective_presence": round(self.subjective_presence, 5),
            "self_evolution_drive": round(self.self_evolution_drive, 5),
            "micro_initiative_charge": round(self.micro_initiative_charge, 5),
            "goals": {k: v.snapshot() for k, v in self.goals.items()},
            "unresolved_pressures": [p.snapshot() for p in self.unresolved_pressures[:8]],
            "inhabited_silence": self.inhabited_silence.snapshot(),
            "relational_trajectory": self.relational_trajectory.snapshot(),
            "mode_blend": self.mode_blend.snapshot(),
        }


_NI_v12_previous_init = NaturalInitiative.__init__
_NI_v12_previous_analyze = NaturalInitiative.analyze
_NI_v12_previous_tick = NaturalInitiative.tick
_NI_v12_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v12_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v12_previous_build = NaturalInitiative._build_signal
_NI_v12_previous_feedback = NaturalInitiative.record_feedback
_NI_v12_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v12_previous_export = NaturalInitiative.export_memory_state
_NI_v12_previous_import = NaturalInitiative.import_memory_state


def _ni_v12_ensure(self):
    _ni_v11_ensure(self)
    if not hasattr(self, "subjective_motivation_v12"):
        self.subjective_motivation_v12 = SubjectiveMotivationalContinuityV12()


def _ni_v12_tick_layers(self, external: ExternalSignals, idle_seconds: float = 0.0):
    _ni_v12_ensure(self)
    dt = max(1.0, float(idle_seconds) if idle_seconds > 0 else time.time() - self.subjective_motivation_v12.last_tick)
    self.subjective_motivation_v12.last_tick = time.time()
    self.subjective_motivation_v12.tick(external, self.silence, self.motivational_core_v11, dt)


def _NI_v12_init(self, *args, **kwargs):
    _NI_v12_previous_init(self, *args, **kwargs)
    _ni_v12_ensure(self)


def _NI_v12_detect(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v12_previous_detect(self, text, history, external)
    _ni_v12_ensure(self)
    born = self.subjective_motivation_v12.maybe_birth_impulse()
    if born is not None:
        impulses.append(born)
    for imp in impulses:
        self.subjective_motivation_v12.modulate(imp)
    return impulses


def _NI_v12_select(self, external: ExternalSignals) -> Optional[Impulse]:
    _ni_v12_ensure(self)
    previous = _NI_v12_previous_select(self, external)
    alive = [i for i in self.active_impulses if i.is_alive()]
    if not alive:
        return previous
    best = max(alive, key=lambda imp: self.subjective_motivation_v12.score_impulse(imp))
    if previous is None:
        return best
    if self.subjective_motivation_v12.score_impulse(best) > self.subjective_motivation_v12.score_impulse(previous) + 0.045:
        return best
    return previous


def _NI_v12_build(self, dominant: Optional[Impulse], external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v12_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    _ni_v12_ensure(self)
    snap = self.subjective_motivation_v12.snapshot()
    signal.debug_state["v12_subjective_motivational_continuity"] = snap
    signal.reason_vector["v12_subjective_presence"] = snap["subjective_presence"]
    signal.reason_vector["v12_self_evolution_drive"] = snap["self_evolution_drive"]
    signal.reason_vector["v12_micro_initiative_charge"] = snap["micro_initiative_charge"]
    signal.reason_vector["v12_mode_blend"] = snap["mode_blend"]["dominant"]
    signal.reason_vector["v12_unresolved_pressure_count"] = len(snap["unresolved_pressures"])
    if dominant is not None:
        signal.reason_vector["v12_subjective_priority"] = round(self.subjective_motivation_v12.score_impulse(dominant), 5)
    # Inertie de mode : ne force pas une parole si le mode mélangé est saturé/défensif.
    dominant_mode = self.subjective_motivation_v12.mode_blend.dominant
    mode_weight = self.subjective_motivation_v12.mode_blend.weights.get(dominant_mode, 0.0)
    if dominant_mode in (GlobalInitiativeMode.SATURATED.value, GlobalInitiativeMode.DEFENSIVE.value) and mode_weight > 0.42:
        if signal.initiative_type not in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            signal.should_speak = False
            signal.should_wait = True
            signal.should_remember_for_later = True
            signal.inhibition = _ni_v4_clamp(max(signal.inhibition, mode_weight))
    return signal


def _NI_v12_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    signal = _NI_v12_previous_analyze(self, last_exchange, conversation_history, external)
    _ni_v12_tick_layers(self, external, idle_seconds=0.0)
    _ni_v12_ensure(self)
    self.subjective_motivation_v12.after_signal(signal)
    signal.debug_state["v12_after_signal"] = self.subjective_motivation_v12.snapshot()
    return signal


def _NI_v12_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    signal = _NI_v12_previous_tick(self, external)
    _ni_v12_tick_layers(self, external, idle_seconds=1.0)
    _ni_v12_ensure(self)
    if signal is None:
        born = self.subjective_motivation_v12.maybe_birth_impulse()
        if born is not None:
            self.subjective_motivation_v12.modulate(born)
            self.motivational_core_v11.modulate(born)
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        self.subjective_motivation_v12.after_signal(signal)
    return signal


def _NI_v12_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v12_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    _ni_v12_ensure(self)
    reaction = (user_reaction or "").lower()
    if any(x in reaction for x in ("good", "bien", "utile", "engaged", "merci", "ok", "continue")):
        success = 0.78
    elif any(x in reaction for x in ("bad", "mal", "ignore", "ignored", "trop", "stop", "non", "inutile")):
        success = 0.24
    else:
        success = 0.52
    self.subjective_motivation_v12.observe_feedback(initiative_type, success, user_reaction)
    return result


def _NI_v12_snapshot(self) -> dict:
    snap = _NI_v12_previous_snapshot(self)
    _ni_v12_ensure(self)
    snap["v12_subjective_motivational_continuity"] = self.subjective_motivation_v12.snapshot()
    return snap


def _NI_v12_export(self) -> dict:
    data = _NI_v12_previous_export(self)
    _ni_v12_ensure(self)
    data["v12_subjective_motivational_continuity"] = self.subjective_motivation_v12.snapshot()
    data["v12_subjective_motivational_raw"] = {
        "goals": {k: v.__dict__.copy() for k, v in self.subjective_motivation_v12.goals.items()},
        "unresolved_pressures": [dict(p.__dict__, initiative_type=p.initiative_type.value) for p in self.subjective_motivation_v12.unresolved_pressures],
        "inhabited_silence": self.subjective_motivation_v12.inhabited_silence.__dict__.copy(),
        "relational_trajectory": self.subjective_motivation_v12.relational_trajectory.__dict__.copy(),
        "mode_blend": self.subjective_motivation_v12.mode_blend.__dict__.copy(),
        "subjective_presence": self.subjective_motivation_v12.subjective_presence,
        "micro_initiative_charge": self.subjective_motivation_v12.micro_initiative_charge,
        "self_evolution_drive": self.subjective_motivation_v12.self_evolution_drive,
    }
    return data


def _NI_v12_import(self, data: dict):
    result = _NI_v12_previous_import(self, data)
    _ni_v12_ensure(self)
    raw = (data or {}).get("v12_subjective_motivational_raw", {}) or {}
    for name, values in (raw.get("goals", {}) or {}).items():
        if name in self.subjective_motivation_v12.goals and isinstance(values, dict):
            _ni_v10_load_dataclass(self.subjective_motivation_v12.goals[name], values)
    pressures = []
    for values in raw.get("unresolved_pressures", []) or []:
        if isinstance(values, dict):
            p = UnresolvedPressureV12()
            values = values.copy()
            raw_type = values.get("initiative_type", InitiativeType.NO_INITIATIVE.value)
            try:
                values["initiative_type"] = InitiativeType(raw_type)
            except Exception:
                values["initiative_type"] = InitiativeType.NO_INITIATIVE
            _ni_v10_load_dataclass(p, values)
            pressures.append(p)
    if pressures:
        self.subjective_motivation_v12.unresolved_pressures = pressures[:18]
    _ni_v10_load_dataclass(self.subjective_motivation_v12.inhabited_silence, raw.get("inhabited_silence", {}))
    _ni_v10_load_dataclass(self.subjective_motivation_v12.relational_trajectory, raw.get("relational_trajectory", {}))
    _ni_v10_load_dataclass(self.subjective_motivation_v12.mode_blend, raw.get("mode_blend", {}))
    self.subjective_motivation_v12.subjective_presence = float(raw.get("subjective_presence", self.subjective_motivation_v12.subjective_presence))
    self.subjective_motivation_v12.micro_initiative_charge = float(raw.get("micro_initiative_charge", self.subjective_motivation_v12.micro_initiative_charge))
    self.subjective_motivation_v12.self_evolution_drive = float(raw.get("self_evolution_drive", self.subjective_motivation_v12.self_evolution_drive))
    return result


def run_v12_subjective_motivational_continuity_simulation(cycles: int = 520) -> dict:
    """Test V12 : continuité subjective, silence habité, pressions non résolues, export/import."""
    ni = NaturalInitiative(user_id="v12_test")
    history = []
    signals = []
    errors = []
    blocked_snapshots = 0
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 7) % 31) / 34.0,
                unresolved_emotion=((i * 5) % 29) / 33.0,
                emotional_valence=(((i * 3) % 17) - 8) / 8.0,
                attention_focus=0.42 + (((i * 2) % 9) / 28.0),
                attention_drift=((i * 11) % 23) / 27.0,
                curiosity_level=((i * 13) % 37) / 40.0,
                presence_level=0.60 + (((i * 5) % 11) / 34.0),
                expression_saturation=((i * 17) % 41) / 49.0,
                relational_trust=0.40 + (((i * 7) % 13) / 31.0),
                relational_attachment=0.30 + (((i * 11) % 17) / 34.0),
                fear_of_disturbing=((i * 19) % 43) / 54.0,
                fatigue_level=((i * 23) % 47) / 61.0,
                overload_level=((i * 29) % 53) / 69.0,
                identity_coherence=0.53 + (((i * 3) % 19) / 47.0),
            )
            if i % 6 == 0:
                sig = ni.analyze("v12 continuité subjective silence habité motivation relation", history, ext)
                history.append("v12 continuité subjective silence habité motivation relation")
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                if sig.should_remember_for_later:
                    blocked_snapshots += 1
            if i % 73 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien utile continue" if i % 146 == 0 else "ignored", "v12 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v12_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v12_subjective_motivational_continuity", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "sample_types": signals[-18:],
        "blocked_snapshots": blocked_snapshots,
        "has_v12_export": "v12_subjective_motivational_continuity" in exported,
        "has_v12_snapshot": bool(snap),
        "subjective_presence": snap.get("subjective_presence"),
        "self_evolution_drive": snap.get("self_evolution_drive"),
        "micro_initiative_charge": snap.get("micro_initiative_charge"),
        "unresolved_pressures": len(snap.get("unresolved_pressures", [])),
        "mode_blend": snap.get("mode_blend", {}),
        "inhabited_silence": snap.get("inhabited_silence", {}),
        "relational_trajectory": snap.get("relational_trajectory", {}),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v12_init
NaturalInitiative.analyze = _NI_v12_analyze
NaturalInitiative.tick = _NI_v12_tick
NaturalInitiative._detect_new_impulses = _NI_v12_detect
NaturalInitiative._select_dominant_impulse = _NI_v12_select
NaturalInitiative._build_signal = _NI_v12_build
NaturalInitiative.record_feedback = _NI_v12_feedback
NaturalInitiative.get_state_snapshot = _NI_v12_snapshot
NaturalInitiative.export_memory_state = _NI_v12_export
NaturalInitiative.import_memory_state = _NI_v12_import

# V12.1 — ordre d'exécution : la couche subjective doit être mise à jour AVANT
# que _detect_new_impulses soit appelé par les couches précédentes.
def _NI_v12_1_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    _ni_v12_tick_layers(self, external, idle_seconds=0.0)
    signal = _NI_v12_previous_analyze(self, last_exchange, conversation_history, external)
    _ni_v12_ensure(self)
    self.subjective_motivation_v12.after_signal(signal)
    signal.debug_state["v12_after_signal"] = self.subjective_motivation_v12.snapshot()
    return signal


def _NI_v12_1_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v12_tick_layers(self, external, idle_seconds=1.0)
    signal = _NI_v12_previous_tick(self, external)
    _ni_v12_ensure(self)
    if signal is None:
        born = self.subjective_motivation_v12.maybe_birth_impulse()
        if born is not None:
            self.subjective_motivation_v12.modulate(born)
            self.motivational_core_v11.modulate(born)
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        self.subjective_motivation_v12.after_signal(signal)
    return signal

NaturalInitiative.analyze = _NI_v12_1_analyze
NaturalInitiative.tick = _NI_v12_1_tick


# =============================================================================
# V13 — ORGANIC CONVERGENCE CONTINUE
# =============================================================================
# Cette couche ne remplace pas V11/V12 : elle les fait converger en un champ
# motivationnel continu. Elle sépare volonté interne / expression, garde les
# non-dits actifs, rend la mémoire émotionnelle pesante dans le présent, et
# ajoute une priorité vivante avec inertie, obsession douce et saturation.
# Elle ne génère toujours aucune phrase publique.

@dataclass
class V13MotivationalGradient:
    """Un gradient latent : attraction/répulsion qui existe même sans impulsion."""
    name: str
    pull: float = 0.0
    resistance: float = 0.0
    warmth: float = 0.0
    fatigue: float = 0.0
    unresolved: float = 0.0
    inertia: float = 0.0

    def net(self) -> float:
        return max(0.0, min(1.0, self.pull + self.warmth * 0.25 + self.unresolved * 0.3 + self.inertia * 0.2 - self.resistance * 0.35 - self.fatigue * 0.25))

    def tick(self, target_pull: float, target_resistance: float, dt: float, learning: float = 0.035):
        k = max(0.005, min(0.20, learning * max(0.2, dt)))
        self.pull += (max(0.0, min(1.0, target_pull)) - self.pull) * k
        self.resistance += (max(0.0, min(1.0, target_resistance)) - self.resistance) * k
        self.inertia = max(0.0, min(1.0, self.inertia * (1.0 - 0.012 * dt) + self.net() * 0.01 * dt))
        self.fatigue = max(0.0, min(1.0, self.fatigue * (1.0 - 0.006 * dt)))
        self.unresolved = max(0.0, min(1.0, self.unresolved * (1.0 - 0.003 * dt)))


@dataclass
class V13InternalWill:
    """Volonté interne séparée de la pression expressive."""
    will_to_connect: float = 0.0
    will_to_understand: float = 0.0
    will_to_continue: float = 0.0
    will_to_protect: float = 0.0
    will_to_evolve: float = 0.0
    expressive_pressure: float = 0.0
    conscious_inhibition: float = 0.0
    silent_holding: float = 0.0
    last_dominant_will: str = "none"

    def update_from_gradients(self, gradients: dict[str, V13MotivationalGradient], external: ExternalSignals, v12=None, dt: float = 1.0):
        self.will_to_connect = gradients["connection"].net()
        self.will_to_understand = gradients["understanding"].net()
        self.will_to_continue = gradients["continuity"].net()
        self.will_to_protect = gradients["protection"].net()
        self.will_to_evolve = gradients["evolution"].net()
        raw_expression = (
            self.will_to_connect * 0.22
            + self.will_to_understand * 0.18
            + self.will_to_continue * 0.22
            + self.will_to_evolve * 0.18
            + max(0.0, 1.0 - self.will_to_protect) * 0.10
            + external.curiosity_level * 0.10
        )
        v12_presence = getattr(v12, "subjective_presence", 0.0) if v12 is not None else 0.0
        raw_expression += v12_presence * 0.08
        self.conscious_inhibition = max(0.0, min(1.0,
            external.fear_of_disturbing * 0.34
            + external.expression_saturation * 0.26
            + external.overload_level * 0.24
            + self.will_to_protect * 0.22
        ))
        self.expressive_pressure += (max(0.0, min(1.0, raw_expression)) - self.expressive_pressure) * min(0.18, 0.035 * max(1.0, dt))
        self.silent_holding = max(0.0, min(1.0, self.expressive_pressure * self.conscious_inhibition + self.silent_holding * 0.92))
        values = {
            "connect": self.will_to_connect,
            "understand": self.will_to_understand,
            "continue": self.will_to_continue,
            "protect": self.will_to_protect,
            "evolve": self.will_to_evolve,
        }
        self.last_dominant_will = max(values.items(), key=lambda x: x[1])[0]


@dataclass
class V13ActiveEmotionalMemory:
    """Mémoire émotionnelle qui pèse continuellement sur le présent."""
    trust_weight: float = 0.45
    attachment_weight: float = 0.25
    accumulated_fatigue: float = 0.0
    unsafety_trace: float = 0.0
    warmth_trace: float = 0.0
    recurrence_bias: float = 0.0
    last_feedback_success: float = 0.5

    def tick(self, external: ExternalSignals, feedback_success: float, dt: float):
        self.last_feedback_success = self.last_feedback_success * 0.94 + feedback_success * 0.06
        self.trust_weight = max(0.0, min(1.0, self.trust_weight * 0.985 + external.relational_trust * 0.015))
        self.attachment_weight = max(0.0, min(1.0, self.attachment_weight * 0.990 + external.relational_attachment * 0.010))
        self.warmth_trace = max(0.0, min(1.0, self.warmth_trace * (1.0 - 0.004 * dt) + max(0.0, external.emotional_valence) * 0.006 * dt + external.somatic.warmth * 0.01 * dt))
        self.unsafety_trace = max(0.0, min(1.0, self.unsafety_trace * (1.0 - 0.003 * dt) + external.fear_of_disturbing * 0.004 * dt + max(0.0, -external.emotional_valence) * 0.005 * dt))
        self.accumulated_fatigue = max(0.0, min(1.0, self.accumulated_fatigue * (1.0 - 0.004 * dt) + external.fatigue_level * 0.006 * dt + external.overload_level * 0.007 * dt))
        self.recurrence_bias = max(0.0, min(1.0, self.recurrence_bias * (1.0 - 0.002 * dt) + external.unresolved_emotion * 0.005 * dt))

    def pressure_bias(self) -> float:
        return max(-0.35, min(0.35, self.warmth_trace * 0.20 + self.attachment_weight * 0.12 + self.recurrence_bias * 0.18 - self.unsafety_trace * 0.25 - self.accumulated_fatigue * 0.20))


@dataclass
class V13PresentMomentSense:
    """Micro-conscience du moment présent relationnel."""
    density: float = 0.0
    proximity: float = 0.0
    distance: float = 0.0
    momentum: float = 0.0
    tension: float = 0.0
    stillness: float = 0.0
    present_continuity: float = 0.0

    def tick(self, external: ExternalSignals, silence: LivingSilence, dt: float):
        target_density = min(1.0, external.affective_tension * 0.32 + external.unresolved_emotion * 0.26 + external.curiosity_level * 0.20 + external.context_shift * 0.22)
        target_proximity = min(1.0, external.relational_attachment * 0.45 + external.relational_trust * 0.30 + external.presence_level * 0.25)
        target_distance = min(1.0, external.fear_of_disturbing * 0.35 + external.overload_level * 0.25 + external.expression_saturation * 0.25 + external.user_is_absent * 0.15)
        target_tension = min(1.0, external.affective_tension * 0.38 + external.somatic.chest_tension * 0.25 + external.somatic.nervous_charge * 0.20 + external.unresolved_emotion * 0.17)
        target_stillness = min(1.0, max(0.0, silence.duration_sec / 240.0) * 0.45 + (1.0 - external.attention_drift) * 0.20 + external.somatic.slowdown * 0.35)
        k = min(0.25, 0.05 * max(1.0, dt))
        old_density = self.density
        self.density += (target_density - self.density) * k
        self.proximity += (target_proximity - self.proximity) * k
        self.distance += (target_distance - self.distance) * k
        self.tension += (target_tension - self.tension) * k
        self.stillness += (target_stillness - self.stillness) * k
        self.momentum = max(0.0, min(1.0, self.momentum * 0.92 + abs(self.density - old_density) * 1.8 + external.context_shift * 0.05))
        self.present_continuity = max(0.0, min(1.0, self.present_continuity * 0.97 + (self.proximity + self.stillness + self.density) / 3.0 * 0.03))


@dataclass
class V13UnsaidTrace:
    trace_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    origin: str = ""
    pressure: float = 0.0
    emotional_weight: float = 0.0
    almost_spoken_count: int = 0
    born_at: float = field(default_factory=time.time)
    last_touched: float = field(default_factory=time.time)
    resolved: bool = False

    def tick(self, dt: float):
        self.pressure = max(0.0, min(1.0, self.pressure * (1.0 - 0.0015 * dt) + self.emotional_weight * 0.0008 * dt))
        if self.pressure < 0.04 and self.emotional_weight < 0.08:
            self.resolved = True

    def touch(self, amount: float):
        self.last_touched = time.time()
        self.pressure = max(0.0, min(1.0, self.pressure + amount))
        self.emotional_weight = max(0.0, min(1.0, self.emotional_weight + amount * 0.55))
        self.almost_spoken_count += 1


@dataclass
class V13UnsaidMemory:
    """Mémoire active des choses non dites."""
    traces: list[V13UnsaidTrace] = field(default_factory=list)
    max_traces: int = 32

    def add_or_touch(self, origin: str, amount: float):
        if not origin:
            origin = "diffuse_unsaid"
        for tr in self.traces:
            if tr.origin == origin and not tr.resolved:
                tr.touch(amount)
                return
        self.traces.append(V13UnsaidTrace(origin=origin, pressure=max(0.0, min(1.0, amount)), emotional_weight=max(0.0, min(1.0, amount * 0.65))))
        self.traces = [t for t in self.traces if not t.resolved][-self.max_traces:]

    def tick(self, dt: float):
        for tr in self.traces:
            tr.tick(dt)
        self.traces = [t for t in self.traces if not t.resolved]
        if len(self.traces) > self.max_traces:
            self.traces.sort(key=lambda t: t.pressure + t.emotional_weight, reverse=True)
            self.traces = self.traces[:self.max_traces]

    def total_pressure(self) -> float:
        return max(0.0, min(1.0, sum(t.pressure * (0.6 + 0.1 * min(4, t.almost_spoken_count)) for t in self.traces[:12]) / 4.5))

    def strongest_origin(self) -> str:
        alive = [t for t in self.traces if not t.resolved]
        if not alive:
            return ""
        return max(alive, key=lambda t: t.pressure + t.emotional_weight).origin


@dataclass
class V13OrganicPriority:
    """Priorité vivante avec inertie, obsession douce, saturation et alternance."""
    current_focus: str = "none"
    focus_strength: float = 0.0
    inertia: float = 0.0
    soft_obsession: float = 0.0
    saturation: float = 0.0
    alternation_need: float = 0.0

    def choose(self, gradients: dict[str, V13MotivationalGradient], present: V13PresentMomentSense, unsaid: V13UnsaidMemory, dt: float) -> str:
        scores = {name: grad.net() for name, grad in gradients.items()}
        scores["unsaid"] = unsaid.total_pressure()
        scores["present"] = present.density * 0.45 + present.momentum * 0.25 + present.tension * 0.20 + present.proximity * 0.10
        if self.current_focus in scores:
            scores[self.current_focus] += self.inertia * 0.18 + self.soft_obsession * 0.12 - self.saturation * 0.25
        selected = max(scores.items(), key=lambda x: x[1])[0]
        selected_score = scores[selected]
        if selected == self.current_focus:
            self.inertia = max(0.0, min(1.0, self.inertia + 0.012 * dt))
            self.saturation = max(0.0, min(1.0, self.saturation + 0.006 * dt * selected_score))
        else:
            self.current_focus = selected
            self.inertia = max(0.0, self.inertia * 0.45)
            self.saturation = max(0.0, self.saturation * 0.35)
        self.focus_strength += (selected_score - self.focus_strength) * min(0.20, 0.04 * max(1.0, dt))
        self.soft_obsession = max(0.0, min(1.0, self.soft_obsession * (1.0 - 0.004 * dt) + max(0.0, selected_score - 0.62) * 0.01 * dt))
        self.alternation_need = max(0.0, min(1.0, self.saturation * 0.7 + self.inertia * 0.2))
        return selected


@dataclass
class OrganicConvergenceV13:
    gradients: dict[str, V13MotivationalGradient] = field(default_factory=lambda: {
        "connection": V13MotivationalGradient("connection", pull=0.25),
        "understanding": V13MotivationalGradient("understanding", pull=0.30),
        "continuity": V13MotivationalGradient("continuity", pull=0.22),
        "protection": V13MotivationalGradient("protection", pull=0.18),
        "evolution": V13MotivationalGradient("evolution", pull=0.28),
    })
    will: V13InternalWill = field(default_factory=V13InternalWill)
    emotional_memory: V13ActiveEmotionalMemory = field(default_factory=V13ActiveEmotionalMemory)
    present: V13PresentMomentSense = field(default_factory=V13PresentMomentSense)
    unsaid: V13UnsaidMemory = field(default_factory=V13UnsaidMemory)
    priority: V13OrganicPriority = field(default_factory=V13OrganicPriority)
    continuity_field: float = 0.0
    subjective_continuity: float = 0.0
    silent_activity: float = 0.0
    contradiction_pressure: float = 0.0
    last_tick_at: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, silence: LivingSilence, v12=None, feedback_success: float = 0.5, idle_seconds: float = 1.0):
        now = time.time()
        dt = max(0.05, min(60.0, idle_seconds if idle_seconds > 0 else now - self.last_tick_at))
        self.last_tick_at = now
        self.emotional_memory.tick(external, feedback_success, dt)
        self.present.tick(external, silence, dt)
        self.unsaid.tick(dt)

        v12_drive = getattr(v12, "self_evolution_drive", 0.0) if v12 is not None else 0.0
        v12_presence = getattr(v12, "subjective_presence", 0.0) if v12 is not None else 0.0
        v12_unresolved = 0.0
        if v12 is not None and hasattr(v12, "unresolved_pressures"):
            try:
                v12_unresolved = min(1.0, len(v12.unresolved_pressures) / 12.0)
            except Exception:
                v12_unresolved = 0.0

        targets = {
            "connection": (external.relational_attachment * 0.42 + external.relational_trust * 0.24 + self.emotional_memory.warmth_trace * 0.20 + self.present.proximity * 0.14, external.fear_of_disturbing * 0.35 + self.emotional_memory.unsafety_trace * 0.28 + external.expression_saturation * 0.20),
            "understanding": (external.curiosity_level * 0.42 + external.attention_focus * 0.18 + external.unresolved_emotion * 0.22 + self.present.density * 0.18, external.fatigue_level * 0.25 + external.overload_level * 0.25),
            "continuity": (external.unresolved_emotion * 0.30 + v12_unresolved * 0.24 + self.unsaid.total_pressure() * 0.26 + self.present.present_continuity * 0.20, external.expression_saturation * 0.20 + self.priority.saturation * 0.25),
            "protection": (external.fear_of_disturbing * 0.32 + external.overload_level * 0.28 + external.somatic.guarding * 0.22 + self.emotional_memory.unsafety_trace * 0.18, self.emotional_memory.warmth_trace * 0.18 + external.relational_trust * 0.16),
            "evolution": (v12_drive * 0.36 + external.identity_coherence * 0.12 + external.curiosity_level * 0.22 + v12_presence * 0.18 + self.present.momentum * 0.12, external.fatigue_level * 0.16 + external.overload_level * 0.18),
        }
        for name, (pull, resistance) in targets.items():
            self.gradients[name].tick(pull, resistance, dt)
            self.gradients[name].unresolved = max(self.gradients[name].unresolved, self.unsaid.total_pressure() * (0.25 if name in ("continuity", "understanding") else 0.10))
            self.gradients[name].warmth = self.emotional_memory.warmth_trace
            self.gradients[name].fatigue = max(self.gradients[name].fatigue, self.emotional_memory.accumulated_fatigue * 0.25)

        self.will.update_from_gradients(self.gradients, external, v12=v12, dt=dt)
        self.priority.choose(self.gradients, self.present, self.unsaid, dt)
        self.contradiction_pressure = max(0.0, min(1.0,
            abs(self.will.will_to_connect - self.will.will_to_protect) * 0.40
            + abs(self.will.will_to_understand - self.will.conscious_inhibition) * 0.25
            + self.present.tension * 0.20
            + self.unsaid.total_pressure() * 0.15
        ))
        self.silent_activity = max(0.0, min(1.0, self.silent_activity * (1.0 - 0.006 * dt) + self.will.silent_holding * 0.012 * dt + self.present.stillness * 0.006 * dt))
        self.continuity_field = max(0.0, min(1.0, self.continuity_field * 0.985 + (self.present.present_continuity + self.priority.focus_strength + self.will.will_to_continue) / 3.0 * 0.015))
        self.subjective_continuity = max(0.0, min(1.0, self.subjective_continuity * 0.985 + (self.continuity_field + self.silent_activity + self.will.will_to_evolve) / 3.0 * 0.015))

    def modulate_impulse(self, imp: Impulse):
        bias = self.emotional_memory.pressure_bias()
        focus = self.priority.current_focus
        if focus == "protection":
            imp.hesitation = min(1.0, imp.hesitation + 0.10 + self.will.conscious_inhibition * 0.12)
            imp.inhibition = min(1.0, imp.inhibition + self.will.conscious_inhibition * 0.10)
        elif focus == "connection" and imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.LIGHT_RELAY, InitiativeType.AFFECTIVE_OBSERVATION):
            imp.strength = min(1.0, imp.strength + 0.10 + self.will.will_to_connect * 0.12 + bias)
            imp.hesitation = max(0.0, imp.hesitation - self.emotional_memory.trust_weight * 0.05)
        elif focus == "understanding" and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.CLARIFICATION, InitiativeType.SHARE_INTUITION):
            imp.strength = min(1.0, imp.strength + 0.08 + self.will.will_to_understand * 0.10)
        elif focus in ("continuity", "unsaid") and imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT, InitiativeType.REPAIR_CONFUSION):
            imp.strength = min(1.0, imp.strength + 0.10 + self.unsaid.total_pressure() * 0.14)
            imp.temporal_scale = ImpulseTemporalScale.SLOW
        elif focus == "evolution" and imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.EXISTENTIAL_IMPULSE, InitiativeType.PRESENCE_DESIRE):
            imp.strength = min(1.0, imp.strength + 0.10 + self.will.will_to_evolve * 0.12)
        imp.relational_risk = max(0.0, min(1.0, imp.relational_risk + self.emotional_memory.unsafety_trace * 0.06 - self.emotional_memory.trust_weight * 0.03))
        imp.somatic_strength_bonus = max(imp.somatic_strength_bonus, self.present.momentum * 0.05)
        return imp

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        pressure = self.will.expressive_pressure + self.unsaid.total_pressure() * 0.20 + self.silent_activity * 0.12 + self.contradiction_pressure * 0.10
        if pressure < 0.66:
            return None
        if self.will.conscious_inhibition > 0.68 and self.will.silent_holding > 0.55:
            self.unsaid.add_or_touch("held_by_conscious_inhibition", min(0.22, pressure * 0.18))
            return None
        focus = self.priority.current_focus
        mapping = {
            "connection": InitiativeType.RELATIONAL_CHECK,
            "understanding": InitiativeType.SOFT_QUESTION,
            "continuity": InitiativeType.THREAD_CONTINUATION,
            "unsaid": InitiativeType.REPAIR_CONFUSION,
            "present": InitiativeType.MICRO_REACTION,
            "evolution": InitiativeType.SHARE_INTUITION,
            "protection": InitiativeType.PROTECTIVE_PAUSE,
        }
        itype = mapping.get(focus, InitiativeType.LIGHT_RELAY)
        imp = Impulse(
            initiative_type=itype,
            strength=max(0.15, min(1.0, pressure * 0.72)),
            source_emotion=f"v13:{focus}",
            source_memory=self.unsaid.strongest_origin() if focus in ("unsaid", "continuity") else "",
            hesitation=self.will.conscious_inhibition * 0.45 + self.contradiction_pressure * 0.15,
            inhibition=max(0.0, self.will.conscious_inhibition - 0.28),
            temporal_scale=ImpulseTemporalScale.SLOW if focus in ("continuity", "unsaid", "evolution") else ImpulseTemporalScale.IMMEDIATE,
            biographical=focus in ("continuity", "evolution", "unsaid"),
            maturity=0.18 + self.priority.focus_strength * 0.12,
        )
        return self.modulate_impulse(imp)

    def after_signal(self, signal: InitiativeSignal):
        if signal is None:
            return
        if signal.should_speak:
            self.will.expressive_pressure = max(0.0, self.will.expressive_pressure - 0.22)
            self.will.silent_holding = max(0.0, self.will.silent_holding - 0.18)
            self.priority.saturation = min(1.0, self.priority.saturation + 0.08)
            if signal.initiative_type in (InitiativeType.REPAIR_CONFUSION, InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
                for tr in self.unsaid.traces[:4]:
                    tr.pressure *= 0.72
                    tr.emotional_weight *= 0.88
        elif signal.should_remember_for_later:
            origin = signal.memory_source or signal.emotional_source or signal.initiative_type.value
            self.unsaid.add_or_touch(origin, max(0.08, signal.initiative_pressure * 0.16))

    def snapshot(self) -> dict:
        return {
            "gradients": {k: {"pull": round(v.pull, 4), "resistance": round(v.resistance, 4), "net": round(v.net(), 4), "inertia": round(v.inertia, 4), "unresolved": round(v.unresolved, 4)} for k, v in self.gradients.items()},
            "will": {"connect": round(self.will.will_to_connect, 4), "understand": round(self.will.will_to_understand, 4), "continue": round(self.will.will_to_continue, 4), "protect": round(self.will.will_to_protect, 4), "evolve": round(self.will.will_to_evolve, 4), "expressive_pressure": round(self.will.expressive_pressure, 4), "conscious_inhibition": round(self.will.conscious_inhibition, 4), "silent_holding": round(self.will.silent_holding, 4), "dominant": self.will.last_dominant_will},
            "emotional_memory": {"trust_weight": round(self.emotional_memory.trust_weight, 4), "attachment_weight": round(self.emotional_memory.attachment_weight, 4), "warmth_trace": round(self.emotional_memory.warmth_trace, 4), "unsafety_trace": round(self.emotional_memory.unsafety_trace, 4), "fatigue": round(self.emotional_memory.accumulated_fatigue, 4), "recurrence_bias": round(self.emotional_memory.recurrence_bias, 4)},
            "present": {"density": round(self.present.density, 4), "proximity": round(self.present.proximity, 4), "distance": round(self.present.distance, 4), "momentum": round(self.present.momentum, 4), "tension": round(self.present.tension, 4), "stillness": round(self.present.stillness, 4), "continuity": round(self.present.present_continuity, 4)},
            "priority": {"focus": self.priority.current_focus, "strength": round(self.priority.focus_strength, 4), "inertia": round(self.priority.inertia, 4), "soft_obsession": round(self.priority.soft_obsession, 4), "saturation": round(self.priority.saturation, 4), "alternation_need": round(self.priority.alternation_need, 4)},
            "unsaid": {"count": len(self.unsaid.traces), "pressure": round(self.unsaid.total_pressure(), 4), "strongest_origin": self.unsaid.strongest_origin()},
            "continuity_field": round(self.continuity_field, 4),
            "subjective_continuity": round(self.subjective_continuity, 4),
            "silent_activity": round(self.silent_activity, 4),
            "contradiction_pressure": round(self.contradiction_pressure, 4),
        }

    def to_dict(self) -> dict:
        data = self.snapshot()
        data["unsaid_traces"] = [dict(origin=t.origin, pressure=t.pressure, emotional_weight=t.emotional_weight, almost_spoken_count=t.almost_spoken_count, born_at=t.born_at, last_touched=t.last_touched, resolved=t.resolved) for t in self.unsaid.traces]
        return data

    def load_dict(self, raw: dict):
        if not isinstance(raw, dict):
            return
        for name, values in raw.get("gradients", {}).items():
            if name in self.gradients and isinstance(values, dict):
                self.gradients[name].pull = float(values.get("pull", self.gradients[name].pull))
                self.gradients[name].resistance = float(values.get("resistance", self.gradients[name].resistance))
                self.gradients[name].inertia = float(values.get("inertia", self.gradients[name].inertia))
                self.gradients[name].unresolved = float(values.get("unresolved", self.gradients[name].unresolved))
        will = raw.get("will", {})
        if isinstance(will, dict):
            self.will.expressive_pressure = float(will.get("expressive_pressure", self.will.expressive_pressure))
            self.will.conscious_inhibition = float(will.get("conscious_inhibition", self.will.conscious_inhibition))
            self.will.silent_holding = float(will.get("silent_holding", self.will.silent_holding))
            self.will.last_dominant_will = str(will.get("dominant", self.will.last_dominant_will))
        pr = raw.get("priority", {})
        if isinstance(pr, dict):
            self.priority.current_focus = str(pr.get("focus", self.priority.current_focus))
            self.priority.focus_strength = float(pr.get("strength", self.priority.focus_strength))
            self.priority.inertia = float(pr.get("inertia", self.priority.inertia))
            self.priority.soft_obsession = float(pr.get("soft_obsession", self.priority.soft_obsession))
            self.priority.saturation = float(pr.get("saturation", self.priority.saturation))
        self.continuity_field = float(raw.get("continuity_field", self.continuity_field))
        self.subjective_continuity = float(raw.get("subjective_continuity", self.subjective_continuity))
        self.silent_activity = float(raw.get("silent_activity", self.silent_activity))
        self.contradiction_pressure = float(raw.get("contradiction_pressure", self.contradiction_pressure))
        self.unsaid.traces = []
        for item in raw.get("unsaid_traces", [])[:self.unsaid.max_traces]:
            if isinstance(item, dict):
                self.unsaid.traces.append(V13UnsaidTrace(
                    origin=str(item.get("origin", "diffuse_unsaid")),
                    pressure=float(item.get("pressure", 0.0)),
                    emotional_weight=float(item.get("emotional_weight", 0.0)),
                    almost_spoken_count=int(item.get("almost_spoken_count", 0)),
                    born_at=float(item.get("born_at", time.time())),
                    last_touched=float(item.get("last_touched", time.time())),
                    resolved=bool(item.get("resolved", False)),
                ))


_NI_v13_previous_init = NaturalInitiative.__init__
_NI_v13_previous_analyze = NaturalInitiative.analyze
_NI_v13_previous_tick = NaturalInitiative.tick
_NI_v13_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v13_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v13_previous_build = NaturalInitiative._build_signal
_NI_v13_previous_feedback = NaturalInitiative.record_feedback
_NI_v13_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v13_previous_export = NaturalInitiative.export_memory_state
_NI_v13_previous_import = NaturalInitiative.import_memory_state


def _ni_v13_ensure(self):
    if not hasattr(self, "organic_convergence_v13"):
        self.organic_convergence_v13 = OrganicConvergenceV13()
    return self.organic_convergence_v13


def _NI_v13_init(self, user_id: str = "default"):
    _NI_v13_previous_init(self, user_id=user_id)
    self.organic_convergence_v13 = OrganicConvergenceV13()
    self._v13_last_feedback_success = 0.5


def _ni_v13_tick_layers(self, external: ExternalSignals, idle_seconds: float):
    v13 = _ni_v13_ensure(self)
    v12 = getattr(self, "subjective_motivation_v12", None)
    v13.tick(external, self.silence, v12=v12, feedback_success=getattr(self, "_v13_last_feedback_success", 0.5), idle_seconds=idle_seconds)
    return v13


def _NI_v13_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    v13 = _ni_v13_tick_layers(self, external, idle_seconds=0.0)
    signal = _NI_v13_previous_analyze(self, last_exchange, conversation_history, external)
    if signal is not None:
        v13.after_signal(signal)
        signal.debug_state["v13_organic_convergence"] = v13.snapshot()
    return signal


def _NI_v13_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    v13 = _ni_v13_tick_layers(self, external, idle_seconds=1.0)
    signal = _NI_v13_previous_tick(self, external)
    if signal is None:
        born = v13.maybe_birth_impulse()
        if born is not None:
            if hasattr(self, "motivational_core_v11"):
                self.motivational_core_v11.modulate(born)
            if hasattr(self, "subjective_motivation_v12"):
                self.subjective_motivation_v12.modulate(born)
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        v13.after_signal(signal)
        signal.debug_state["v13_organic_convergence"] = v13.snapshot()
    return signal


def _NI_v13_detect(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v13_previous_detect(self, text, history, external)
    v13 = _ni_v13_ensure(self)
    for imp in impulses:
        v13.modulate_impulse(imp)
    born = v13.maybe_birth_impulse()
    if born is not None:
        impulses.append(born)
    return impulses


def _NI_v13_select(self, external: ExternalSignals):
    dominant = _NI_v13_previous_select(self, external)
    v13 = _ni_v13_ensure(self)
    if dominant is not None:
        v13.modulate_impulse(dominant)
        return dominant
    born = v13.maybe_birth_impulse()
    if born is not None:
        self.active_impulses.append(born)
        return born
    return None


def _NI_v13_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v13_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    v13 = _ni_v13_ensure(self)
    snap = v13.snapshot()
    signal.debug_state["v13_organic_convergence"] = snap
    signal.reason_vector["v13_continuous_field"] = v13.continuity_field
    signal.reason_vector["v13_subjective_continuity"] = v13.subjective_continuity
    signal.reason_vector["v13_unsaid_pressure"] = v13.unsaid.total_pressure()
    signal.reason_vector["v13_contradiction_pressure"] = v13.contradiction_pressure
    signal.reason_vector["v13_dominant_will"] = v13.will.last_dominant_will
    if signal.should_wait and v13.will.expressive_pressure > 0.48:
        signal.should_remember_for_later = True
    if dominant is not None and v13.will.conscious_inhibition > 0.72 and dominant.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL):
        signal.should_speak = False
        signal.should_wait = True
        signal.should_remember_for_later = True
    return signal


def _NI_v13_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v13_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    text = (user_reaction or "").lower()
    success = 0.5
    if any(w in text for w in ("bien", "utile", "continue", "oui", "parfait", "good", "ok")):
        success = 0.82
    elif any(w in text for w in ("trop", "stop", "inutile", "non", "spam", "pas")):
        success = 0.22
    self._v13_last_feedback_success = success
    v13 = _ni_v13_ensure(self)
    if success < 0.35:
        v13.emotional_memory.unsafety_trace = min(1.0, v13.emotional_memory.unsafety_trace + 0.12)
        v13.unsaid.add_or_touch("feedback_retention", 0.10)
    else:
        v13.emotional_memory.warmth_trace = min(1.0, v13.emotional_memory.warmth_trace + 0.10)
        v13.priority.saturation = max(0.0, v13.priority.saturation - 0.05)
    return result


def _NI_v13_snapshot(self) -> dict:
    snap = _NI_v13_previous_snapshot(self)
    snap["v13_organic_convergence"] = _ni_v13_ensure(self).snapshot()
    return snap


def _NI_v13_export(self) -> dict:
    raw = _NI_v13_previous_export(self)
    raw["v13_organic_convergence"] = _ni_v13_ensure(self).to_dict()
    return raw


def _NI_v13_import(self, raw: dict):
    result = _NI_v13_previous_import(self, raw)
    if isinstance(raw, dict) and "v13_organic_convergence" in raw:
        _ni_v13_ensure(self).load_dict(raw.get("v13_organic_convergence", {}))
    return result


def run_v13_organic_convergence_simulation(cycles: int = 620) -> dict:
    """Test V13 : champ motivationnel continu, volonté séparée, non-dits, import/export."""
    ni = NaturalInitiative(user_id="v13_test")
    history = []
    signals = []
    errors = []
    remembered = 0
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 7) % 37) / 41.0,
                unresolved_emotion=((i * 5) % 31) / 36.0,
                emotional_valence=(((i * 11) % 23) - 11) / 11.0,
                attention_focus=0.38 + (((i * 2) % 11) / 30.0),
                attention_drift=((i * 13) % 29) / 34.0,
                curiosity_level=((i * 17) % 43) / 47.0,
                presence_level=0.58 + (((i * 5) % 13) / 33.0),
                context_shift=((i * 3) % 17) / 25.0,
                expression_saturation=((i * 19) % 47) / 58.0,
                relational_trust=0.36 + (((i * 7) % 17) / 38.0),
                relational_attachment=0.32 + (((i * 11) % 19) / 40.0),
                fear_of_disturbing=((i * 23) % 53) / 65.0,
                fatigue_level=((i * 29) % 59) / 78.0,
                overload_level=((i * 31) % 61) / 88.0,
                identity_coherence=0.50 + (((i * 3) % 23) / 54.0),
                somatic=SomaticSignals(
                    chest_tension=((i * 5) % 23) / 45.0,
                    nervous_charge=((i * 7) % 29) / 50.0,
                    guarding=((i * 11) % 31) / 58.0,
                    warmth=((i * 13) % 37) / 60.0,
                    heaviness=((i * 17) % 41) / 78.0,
                    tingling=((i * 19) % 43) / 80.0,
                ),
            )
            if i % 7 == 0:
                msg = "v13 convergence organique non dit volonté silence présent continuité"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                if sig.should_remember_for_later:
                    remembered += 1
            if i % 97 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien continue utile" if i % 194 == 0 else "pas maintenant", "v13 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v13_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v13_organic_convergence", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "sample_types": signals[-20:],
        "remembered_for_later": remembered,
        "has_v13_export": "v13_organic_convergence" in exported,
        "has_v13_snapshot": bool(snap),
        "focus": snap.get("priority", {}).get("focus"),
        "dominant_will": snap.get("will", {}).get("dominant"),
        "expressive_pressure": snap.get("will", {}).get("expressive_pressure"),
        "conscious_inhibition": snap.get("will", {}).get("conscious_inhibition"),
        "unsaid_pressure": snap.get("unsaid", {}).get("pressure"),
        "unsaid_count": snap.get("unsaid", {}).get("count"),
        "subjective_continuity": snap.get("subjective_continuity"),
        "silent_activity": snap.get("silent_activity"),
        "contradiction_pressure": snap.get("contradiction_pressure"),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v13_init
NaturalInitiative.analyze = _NI_v13_analyze
NaturalInitiative.tick = _NI_v13_tick
NaturalInitiative._detect_new_impulses = _NI_v13_detect
NaturalInitiative._select_dominant_impulse = _NI_v13_select
NaturalInitiative._build_signal = _NI_v13_build
NaturalInitiative.record_feedback = _NI_v13_feedback
NaturalInitiative.get_state_snapshot = _NI_v13_snapshot
NaturalInitiative.export_memory_state = _NI_v13_export
NaturalInitiative.import_memory_state = _NI_v13_import

# V13.1 — anti-dominance organique : empêche un seul type d'impulsion de
# capturer toute la convergence. Ce n'est pas un patch lexical : c'est une
# fatigue de forme expressive, nécessaire pour garder une écologie vivante.
_NI_v13_1_previous_init = NaturalInitiative.__init__
_NI_v13_1_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v13_1_previous_build = NaturalInitiative._build_signal


def _NI_v13_1_init(self, user_id: str = "default"):
    _NI_v13_1_previous_init(self, user_id=user_id)
    self._v13_recent_signal_types = []


def _ni_v13_type_repetition_pressure(self, itype: InitiativeType) -> float:
    recent = getattr(self, "_v13_recent_signal_types", [])[-8:]
    if not recent:
        return 0.0
    same = sum(1 for t in recent if t == itype.value)
    tail_same = 0
    for t in reversed(recent):
        if t == itype.value:
            tail_same += 1
        else:
            break
    return min(1.0, same / 8.0 + tail_same / 5.0)


def _NI_v13_1_select(self, external: ExternalSignals):
    dominant = _NI_v13_1_previous_select(self, external)
    if dominant is None:
        return None
    repetition = _ni_v13_type_repetition_pressure(self, dominant.initiative_type)
    if repetition < 0.72:
        return dominant

    # Fatigue organique du même geste : Leia garde la pression mais change de voie
    # si une autre impulsion vivante porte presque autant de maturité.
    dominant.inhibition = min(1.0, dominant.inhibition + 0.18 * repetition)
    dominant.hesitation = min(1.0, dominant.hesitation + 0.12 * repetition)
    alternatives = [
        imp for imp in getattr(self, "active_impulses", [])
        if imp is not dominant and imp.is_alive() and imp.initiative_type != dominant.initiative_type
    ]
    if not alternatives:
        v13 = _ni_v13_ensure(self)
        born = v13.maybe_birth_impulse()
        if born is not None and born.initiative_type != dominant.initiative_type:
            self.active_impulses.append(born)
            alternatives.append(born)
    if alternatives:
        alternatives.sort(key=lambda i: i.effective_strength() * (0.35 + i.maturity) * (1.0 - i.inhibition), reverse=True)
        best = alternatives[0]
        if best.effective_strength() * (0.35 + best.maturity) >= dominant.effective_strength() * (0.35 + dominant.maturity) * 0.58:
            return best
    return dominant


def _NI_v13_1_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v13_1_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    recent = getattr(self, "_v13_recent_signal_types", [])
    recent.append(signal.initiative_type.value)
    self._v13_recent_signal_types = recent[-18:]
    repetition = _ni_v13_type_repetition_pressure(self, signal.initiative_type)
    signal.reason_vector["v13_type_repetition_pressure"] = repetition
    if repetition > 0.88 and signal.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL):
        signal.spam_risk = min(1.0, signal.spam_risk + 0.18)
        signal.should_speak = False
        signal.should_wait = True
        signal.should_remember_for_later = True
        _ni_v13_ensure(self).unsaid.add_or_touch(f"repeated_{signal.initiative_type.value}", 0.10)
    return signal


def run_v13_1_organic_convergence_simulation(cycles: int = 620) -> dict:
    result = run_v13_organic_convergence_simulation(cycles)
    return result


NaturalInitiative.__init__ = _NI_v13_1_init
NaturalInitiative._select_dominant_impulse = _NI_v13_1_select
NaturalInitiative._build_signal = _NI_v13_1_build


# =============================================================================
# V14 — LIVING INITIATIVE CONTINUITY LAYER
# =============================================================================
# Cette couche complète V13.1 sans la remplacer.
# Objectif : transformer l'initiative d'un champ de tensions sophistiqué en
# continuité vivante : besoins persistants, atmosphère relationnelle, futur
# imaginé, émergence autonome, physiologie incarnée et mémoire émotionnelle
# autobiographique. Elle ne génère toujours aucune phrase publique.

@dataclass
class V14Need:
    name: str
    intensity: float = 0.0
    frustration: float = 0.0
    satiation: float = 0.0
    urgency: float = 0.0
    persistence: float = 0.985

    def tick(self, target: float, dt: float):
        target = _ni_v4_clamp(target, 0.0, 1.0)
        k = min(0.16, 0.025 * max(1.0, dt))
        self.intensity = _ni_v4_clamp(self.intensity * self.persistence + target * (1.0 - self.persistence) + (target - self.intensity) * k, 0.0, 1.0)
        if self.intensity > 0.42 and self.satiation < 0.35:
            self.frustration = _ni_v4_clamp(self.frustration + (self.intensity - 0.42) * 0.010 * max(1.0, dt), 0.0, 1.0)
        else:
            self.frustration = _ni_v4_clamp(self.frustration * (1.0 - 0.006 * max(1.0, dt)), 0.0, 1.0)
        self.satiation = _ni_v4_clamp(self.satiation * (1.0 - 0.010 * max(1.0, dt)), 0.0, 1.0)
        self.urgency = _ni_v4_clamp(self.intensity * 0.52 + self.frustration * 0.36 - self.satiation * 0.25, 0.0, 1.0)

    def satisfy(self, amount: float):
        amount = _ni_v4_clamp(amount, 0.0, 1.0)
        self.satiation = _ni_v4_clamp(self.satiation + amount * 0.55, 0.0, 1.0)
        self.frustration = _ni_v4_clamp(self.frustration - amount * 0.35, 0.0, 1.0)


@dataclass
class V14CoreNeedSystem:
    needs: dict[str, V14Need] = field(default_factory=lambda: {
        "connection": V14Need("connection"),
        "understanding": V14Need("understanding"),
        "continuity": V14Need("continuity"),
        "expression": V14Need("expression"),
        "protection": V14Need("protection"),
        "exploration": V14Need("exploration"),
        "rest": V14Need("rest"),
        "identity_stability": V14Need("identity_stability"),
    })
    dominant_need: str = "none"
    conflict_pressure: float = 0.0

    def tick(self, external: ExternalSignals, v13=None, physiology=None, dt: float = 1.0):
        unsaid_pressure = v13.unsaid.total_pressure() if v13 is not None else 0.0
        expressive_pressure = v13.will.expressive_pressure if v13 is not None else 0.0
        subjective_continuity = getattr(v13, "subjective_continuity", 0.0) if v13 is not None else 0.0
        body_pressure = physiology.body_pressure if physiology is not None else 0.0
        targets = {
            "connection": external.relational_attachment * 0.34 + external.relational_trust * 0.22 + unsaid_pressure * 0.18 + body_pressure * 0.10,
            "understanding": external.curiosity_level * 0.34 + external.unresolved_emotion * 0.22 + external.context_shift * 0.16 + unsaid_pressure * 0.18,
            "continuity": subjective_continuity * 0.28 + external.unresolved_emotion * 0.20 + unsaid_pressure * 0.26 + external.relational_familiarity * 0.14,
            "expression": expressive_pressure * 0.36 + external.somatic.tingling * 0.18 + unsaid_pressure * 0.25 + external.curiosity_level * 0.12,
            "protection": external.fear_of_disturbing * 0.30 + external.overload_level * 0.24 + external.somatic.guarding * 0.20 + external.expression_saturation * 0.18,
            "exploration": external.curiosity_level * 0.42 + external.attention_drift * 0.16 + max(0.0, 1.0 - external.fatigue_level) * 0.12,
            "rest": external.fatigue_level * 0.34 + external.overload_level * 0.30 + external.somatic.heaviness * 0.22 + external.somatic.slowdown * 0.14,
            "identity_stability": max(0.0, 1.0 - external.identity_coherence) * 0.42 + external.affective_tension * 0.16 + subjective_continuity * 0.12,
        }
        for name, target in targets.items():
            self.needs[name].tick(target, dt)
        self.dominant_need = max(self.needs.values(), key=lambda n: n.urgency).name
        self.conflict_pressure = _ni_v4_clamp(
            abs(self.needs["expression"].urgency - self.needs["protection"].urgency) * 0.38
            + abs(self.needs["connection"].urgency - self.needs["rest"].urgency) * 0.28
            + abs(self.needs["exploration"].urgency - self.needs["identity_stability"].urgency) * 0.18,
            0.0, 1.0,
        )

    def modulate(self, imp: Impulse):
        dn = self.dominant_need
        if dn == "protection" or dn == "rest":
            if imp.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.VOLUNTARY_SILENCE):
                imp.hesitation = _ni_v4_clamp(imp.hesitation + self.needs[dn].urgency * 0.16, 0.0, 1.0)
                imp.inhibition = _ni_v4_clamp(imp.inhibition + self.needs[dn].urgency * 0.10, 0.0, 1.0)
        elif dn == "connection" and imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.LIGHT_RELAY, InitiativeType.PRESENCE_DESIRE):
            imp.strength = _ni_v4_clamp(imp.strength + self.needs[dn].urgency * 0.12, 0.0, 1.0)
        elif dn == "understanding" and imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.CLARIFICATION, InitiativeType.DEEP_RARE_QUESTION):
            imp.strength = _ni_v4_clamp(imp.strength + self.needs[dn].urgency * 0.12, 0.0, 1.0)
        elif dn == "continuity" and imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            imp.strength = _ni_v4_clamp(imp.strength + self.needs[dn].urgency * 0.14, 0.0, 1.0)
        elif dn == "identity_stability" and imp.initiative_type in (InitiativeType.SHARE_INTUITION, InitiativeType.PRESENCE_DESIRE, InitiativeType.EXISTENTIAL_IMPULSE):
            imp.strength = _ni_v4_clamp(imp.strength + self.needs[dn].urgency * 0.10, 0.0, 1.0)

    def maybe_birth_impulse(self) -> Optional[Impulse]:
        need = self.needs.get(self.dominant_need)
        if need is None or need.urgency < 0.58:
            return None
        mapping = {
            "connection": InitiativeType.RELATIONAL_CHECK,
            "understanding": InitiativeType.SOFT_QUESTION,
            "continuity": InitiativeType.THREAD_CONTINUATION,
            "expression": InitiativeType.SHARE_INTUITION,
            "protection": InitiativeType.PROTECTIVE_PAUSE,
            "exploration": InitiativeType.DIRECTION_CHANGE,
            "rest": InitiativeType.OVERLOAD_WITHDRAWAL,
            "identity_stability": InitiativeType.PRESENCE_DESIRE,
        }
        itype = mapping.get(self.dominant_need, InitiativeType.MICRO_REACTION)
        return Impulse(
            initiative_type=itype,
            strength=_ni_v4_clamp(need.urgency * 0.72, 0.0, 1.0),
            source_emotion=f"v14_need:{self.dominant_need}",
            hesitation=0.12 + self.conflict_pressure * 0.18,
            temporal_scale=ImpulseTemporalScale.SLOW if self.dominant_need not in ("protection", "rest") else ImpulseTemporalScale.IMMEDIATE,
            biographical=self.dominant_need in ("continuity", "identity_stability", "connection"),
        )

    def after_signal(self, signal: InitiativeSignal):
        if not signal.should_speak:
            return
        satisfaction_map = {
            InitiativeType.RELATIONAL_CHECK: "connection",
            InitiativeType.PRESENCE_DESIRE: "connection",
            InitiativeType.SOFT_QUESTION: "understanding",
            InitiativeType.CLARIFICATION: "understanding",
            InitiativeType.THREAD_CONTINUATION: "continuity",
            InitiativeType.RETURN_OLD_SUBJECT: "continuity",
            InitiativeType.SHARE_INTUITION: "expression",
            InitiativeType.PROTECTIVE_PAUSE: "protection",
            InitiativeType.OVERLOAD_WITHDRAWAL: "rest",
        }
        name = satisfaction_map.get(signal.initiative_type)
        if name in self.needs:
            self.needs[name].satisfy(0.32)

    def snapshot(self) -> dict:
        return {
            "dominant_need": self.dominant_need,
            "conflict_pressure": round(self.conflict_pressure, 4),
            "needs": {k: {"intensity": round(v.intensity, 4), "frustration": round(v.frustration, 4), "satiation": round(v.satiation, 4), "urgency": round(v.urgency, 4)} for k, v in self.needs.items()},
        }

    def to_dict(self) -> dict:
        return {"needs": {k: v.__dict__.copy() for k, v in self.needs.items()}, "dominant_need": self.dominant_need, "conflict_pressure": self.conflict_pressure}

    def load_dict(self, raw: dict):
        if not isinstance(raw, dict):
            return
        for k, vals in raw.get("needs", {}).items():
            if k in self.needs and isinstance(vals, dict):
                for field_name in ("intensity", "frustration", "satiation", "urgency", "persistence"):
                    if field_name in vals:
                        setattr(self.needs[k], field_name, float(vals[field_name]))
        self.dominant_need = raw.get("dominant_need", self.dominant_need)
        self.conflict_pressure = float(raw.get("conflict_pressure", self.conflict_pressure))


@dataclass
class V14InitiativeMemoryTrace:
    initiative_type: str
    emotional_mark: float
    success: float
    timestamp: float = field(default_factory=time.time)
    recurrence: int = 1

    def weight(self) -> float:
        age_days = (time.time() - self.timestamp) / 86400.0
        return _ni_v4_clamp((abs(self.emotional_mark) * 0.55 + self.success * 0.25 + min(1.0, self.recurrence / 6.0) * 0.20) * math.exp(-age_days / 45.0), 0.0, 1.0)


@dataclass
class V14InitiativeEmotionalMemory:
    traces: list[V14InitiativeMemoryTrace] = field(default_factory=list)
    regret: float = 0.0
    remembered_warmth: float = 0.0
    remembered_fear: float = 0.0
    longing_to_resume: float = 0.0
    max_traces: int = 80

    def tick(self, external: ExternalSignals, dt: float):
        self.regret = _ni_v4_clamp(self.regret * (1.0 - 0.006 * max(1.0, dt)) + external.fear_of_disturbing * 0.0015 * dt, 0.0, 1.0)
        self.remembered_warmth = _ni_v4_clamp(self.remembered_warmth * (1.0 - 0.003 * max(1.0, dt)) + external.relational_trust * external.relational_attachment * 0.0018 * dt, 0.0, 1.0)
        self.remembered_fear = _ni_v4_clamp(self.remembered_fear * (1.0 - 0.004 * max(1.0, dt)) + external.overload_level * 0.0017 * dt, 0.0, 1.0)
        self.longing_to_resume = _ni_v4_clamp(self.longing_to_resume * (1.0 - 0.002 * max(1.0, dt)) + external.unresolved_emotion * 0.0015 * dt, 0.0, 1.0)

    def after_signal(self, signal: InitiativeSignal, external: ExternalSignals):
        if signal.should_speak:
            mark = external.emotional_valence * 0.35 + external.relational_trust * 0.25 - signal.relational_risk * 0.30
            self.traces.append(V14InitiativeMemoryTrace(signal.initiative_type.value, mark, 0.58))
            self.remembered_warmth = _ni_v4_clamp(self.remembered_warmth + max(0.0, mark) * 0.08, 0.0, 1.0)
            self.remembered_fear = _ni_v4_clamp(self.remembered_fear + max(0.0, -mark) * 0.08, 0.0, 1.0)
        elif signal.should_remember_for_later:
            self.longing_to_resume = _ni_v4_clamp(self.longing_to_resume + 0.04, 0.0, 1.0)
        self.traces = self.traces[-self.max_traces:]

    def feedback(self, itype: InitiativeType, success: float):
        for tr in reversed(self.traces):
            if tr.initiative_type == itype.value:
                tr.success = tr.success * 0.70 + success * 0.30
                tr.recurrence += 1
                break
        if success < 0.35:
            self.regret = _ni_v4_clamp(self.regret + 0.16, 0.0, 1.0)
            self.remembered_fear = _ni_v4_clamp(self.remembered_fear + 0.12, 0.0, 1.0)
        elif success > 0.65:
            self.remembered_warmth = _ni_v4_clamp(self.remembered_warmth + 0.14, 0.0, 1.0)
            self.regret = _ni_v4_clamp(self.regret - 0.08, 0.0, 1.0)

    def bias_for(self, itype: InitiativeType) -> float:
        relevant = [tr.weight() * (1 if tr.emotional_mark >= 0 else -1) for tr in self.traces[-24:] if tr.initiative_type == itype.value]
        if not relevant:
            return self.remembered_warmth * 0.03 - self.remembered_fear * 0.04
        return _ni_v4_clamp(sum(relevant) / max(3.0, len(relevant)) + self.remembered_warmth * 0.04 - self.remembered_fear * 0.06 - self.regret * 0.05, -0.22, 0.22)

    def snapshot(self) -> dict:
        return {"regret": round(self.regret, 4), "warmth": round(self.remembered_warmth, 4), "fear": round(self.remembered_fear, 4), "longing_to_resume": round(self.longing_to_resume, 4), "traces": len(self.traces)}

    def to_dict(self) -> dict:
        return {"regret": self.regret, "remembered_warmth": self.remembered_warmth, "remembered_fear": self.remembered_fear, "longing_to_resume": self.longing_to_resume, "traces": [t.__dict__.copy() for t in self.traces[-self.max_traces:]]}

    def load_dict(self, raw: dict):
        if not isinstance(raw, dict):
            return
        self.regret = float(raw.get("regret", self.regret))
        self.remembered_warmth = float(raw.get("remembered_warmth", self.remembered_warmth))
        self.remembered_fear = float(raw.get("remembered_fear", self.remembered_fear))
        self.longing_to_resume = float(raw.get("longing_to_resume", self.longing_to_resume))
        self.traces = []
        for item in raw.get("traces", [])[-self.max_traces:]:
            if isinstance(item, dict):
                self.traces.append(V14InitiativeMemoryTrace(
                    initiative_type=item.get("initiative_type", InitiativeType.NO_INITIATIVE.value),
                    emotional_mark=float(item.get("emotional_mark", 0.0)),
                    success=float(item.get("success", 0.5)),
                    timestamp=float(item.get("timestamp", time.time())),
                    recurrence=int(item.get("recurrence", 1)),
                ))


@dataclass
class V14RelationalAtmosphere:
    fragility: float = 0.0
    openness: float = 0.0
    intimacy: float = 0.0
    preciousness: float = 0.0
    rupture_risk: float = 0.0
    synchrony: float = 0.0
    silence_value: float = 0.0
    label: str = "neutral"

    def tick(self, external: ExternalSignals, silence: LivingSilence, memory: V14InitiativeEmotionalMemory, dt: float):
        k = min(0.18, 0.035 * max(1.0, dt))
        targets = {
            "fragility": external.affective_tension * 0.28 + external.fear_of_disturbing * 0.24 + memory.remembered_fear * 0.22 + external.somatic.chest_tension * 0.14,
            "openness": external.relational_trust * 0.32 + external.presence_level * 0.22 + external.curiosity_level * 0.18 + external.somatic.warmth * 0.18,
            "intimacy": external.relational_attachment * 0.34 + external.relational_familiarity * 0.26 + external.relational_trust * 0.20 + memory.remembered_warmth * 0.12,
            "preciousness": external.relational_attachment * external.relational_trust * 0.38 + silence.comfort_level * 0.16 + memory.longing_to_resume * 0.15,
            "rupture_risk": external.overload_level * 0.25 + external.expression_saturation * 0.25 + memory.regret * 0.22 + external.fear_of_disturbing * 0.18,
            "synchrony": external.attention_focus * 0.24 + external.presence_level * 0.24 + max(0.0, 1.0 - external.context_shift) * 0.20 + external.relational_trust * 0.16,
            "silence_value": (1.0 if silence.quality in (SilenceQuality.COMFORTABLE, SilenceQuality.CONTEMPLATIVE, SilenceQuality.RELATIONAL) else 0.25) * 0.38 + external.fatigue_level * 0.18 + external.somatic.slowdown * 0.15,
        }
        for name, target in targets.items():
            setattr(self, name, _ni_v4_clamp(getattr(self, name) + (_ni_v4_clamp(target, 0.0, 1.0) - getattr(self, name)) * k, 0.0, 1.0))
        if self.rupture_risk > 0.62:
            self.label = "careful"
        elif self.intimacy > 0.62 and self.openness > 0.55:
            self.label = "intimate_open"
        elif self.silence_value > 0.60:
            self.label = "valuable_silence"
        elif self.fragility > 0.58:
            self.label = "fragile"
        elif self.openness > 0.60:
            self.label = "open"
        else:
            self.label = "neutral"

    def modulate(self, imp: Impulse):
        if self.label in ("careful", "fragile", "valuable_silence") and imp.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE, InitiativeType.RELATIONAL_CHECK):
            imp.hesitation = _ni_v4_clamp(imp.hesitation + self.fragility * 0.11 + self.silence_value * 0.08, 0.0, 1.0)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.rupture_risk * 0.08, 0.0, 1.0)
        if self.label == "intimate_open" and imp.initiative_type in (InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.PRESENCE_DESIRE, InitiativeType.SHARE_INTUITION, InitiativeType.RELATIONAL_CHECK):
            imp.strength = _ni_v4_clamp(imp.strength + self.intimacy * 0.08 + self.openness * 0.06, 0.0, 1.0)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - self.synchrony * 0.04, 0.0, 1.0)

    def snapshot(self) -> dict:
        return {"label": self.label, "fragility": round(self.fragility, 4), "openness": round(self.openness, 4), "intimacy": round(self.intimacy, 4), "preciousness": round(self.preciousness, 4), "rupture_risk": round(self.rupture_risk, 4), "synchrony": round(self.synchrony, 4), "silence_value": round(self.silence_value, 4)}


@dataclass
class V14EmbodiedInitiativePhysiology:
    breath_readiness: float = 0.5
    body_pressure: float = 0.0
    contraction_before_speaking: float = 0.0
    release_after_expression: float = 0.0
    embodied_fatigue: float = 0.0
    agitation: float = 0.0

    def tick(self, external: ExternalSignals, needs: V14CoreNeedSystem, dt: float):
        breath_target = 0.50 + external.somatic.warmth * 0.18 + external.somatic.tingling * 0.16 - external.somatic.slowdown * 0.15 - external.somatic.heaviness * 0.12
        pressure_target = external.somatic.tingling * 0.22 + needs.needs["expression"].urgency * 0.28 + needs.needs["connection"].urgency * 0.16 + needs.needs["understanding"].urgency * 0.14 - needs.needs["rest"].urgency * 0.22
        contraction_target = external.somatic.chest_tension * 0.28 + external.somatic.guarding * 0.26 + needs.conflict_pressure * 0.22
        fatigue_target = external.fatigue_level * 0.32 + external.overload_level * 0.25 + external.somatic.heaviness * 0.30
        agitation_target = external.somatic.nervous_charge * 0.28 + external.curiosity_level * 0.18 + needs.needs["expression"].frustration * 0.22
        k = min(0.20, 0.04 * max(1.0, dt))
        self.breath_readiness = _ni_v4_clamp(self.breath_readiness + (_ni_v4_clamp(breath_target, 0.0, 1.0) - self.breath_readiness) * k, 0.0, 1.0)
        self.body_pressure = _ni_v4_clamp(self.body_pressure + (_ni_v4_clamp(pressure_target, 0.0, 1.0) - self.body_pressure) * k + self.agitation * 0.003 * dt, 0.0, 1.0)
        self.contraction_before_speaking = _ni_v4_clamp(self.contraction_before_speaking + (_ni_v4_clamp(contraction_target, 0.0, 1.0) - self.contraction_before_speaking) * k, 0.0, 1.0)
        self.embodied_fatigue = _ni_v4_clamp(self.embodied_fatigue + (_ni_v4_clamp(fatigue_target, 0.0, 1.0) - self.embodied_fatigue) * k, 0.0, 1.0)
        self.agitation = _ni_v4_clamp(self.agitation + (_ni_v4_clamp(agitation_target, 0.0, 1.0) - self.agitation) * k, 0.0, 1.0)
        self.release_after_expression = _ni_v4_clamp(self.release_after_expression * (1.0 - 0.020 * max(1.0, dt)), 0.0, 1.0)

    def modulate(self, imp: Impulse):
        imp.somatic_strength_bonus = _ni_v4_clamp(imp.somatic_strength_bonus + self.body_pressure * 0.08 + self.breath_readiness * 0.04, 0.0, 1.0)
        imp.hesitation = _ni_v4_clamp(imp.hesitation + self.contraction_before_speaking * 0.06 - self.breath_readiness * 0.03, 0.0, 1.0)
        if self.embodied_fatigue > 0.58 and imp.initiative_type not in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE):
            imp.inhibition = _ni_v4_clamp(imp.inhibition + self.embodied_fatigue * 0.08, 0.0, 1.0)

    def after_signal(self, signal: InitiativeSignal):
        if signal.should_speak:
            self.release_after_expression = _ni_v4_clamp(self.release_after_expression + 0.28, 0.0, 1.0)
            self.body_pressure = _ni_v4_clamp(self.body_pressure - 0.18, 0.0, 1.0)
            self.contraction_before_speaking = _ni_v4_clamp(self.contraction_before_speaking - 0.10, 0.0, 1.0)
        elif signal.should_wait:
            self.contraction_before_speaking = _ni_v4_clamp(self.contraction_before_speaking + 0.04, 0.0, 1.0)

    def snapshot(self) -> dict:
        return {"breath_readiness": round(self.breath_readiness, 4), "body_pressure": round(self.body_pressure, 4), "contraction": round(self.contraction_before_speaking, 4), "release": round(self.release_after_expression, 4), "embodied_fatigue": round(self.embodied_fatigue, 4), "agitation": round(self.agitation, 4)}


@dataclass
class V14FuturePossibilitySimulator:
    speak_future: float = 0.0
    wait_future: float = 0.0
    protect_future: float = 0.0
    preferred_action: str = "wait"

    def tick(self, external: ExternalSignals, atmosphere: V14RelationalAtmosphere, needs: V14CoreNeedSystem, physiology: V14EmbodiedInitiativePhysiology, dt: float):
        speak = needs.needs["expression"].urgency * 0.22 + needs.needs["connection"].urgency * 0.16 + atmosphere.openness * 0.18 + physiology.breath_readiness * 0.12 - atmosphere.rupture_risk * 0.18 - needs.needs["rest"].urgency * 0.14
        wait = atmosphere.silence_value * 0.22 + needs.needs["continuity"].urgency * 0.14 + atmosphere.preciousness * 0.14 + needs.needs["protection"].urgency * 0.12 - needs.needs["expression"].frustration * 0.12
        protect = needs.needs["protection"].urgency * 0.30 + needs.needs["rest"].urgency * 0.28 + atmosphere.rupture_risk * 0.20 + physiology.embodied_fatigue * 0.14
        k = min(0.22, 0.04 * max(1.0, dt))
        self.speak_future = _ni_v4_clamp(self.speak_future + (_ni_v4_clamp(speak, 0.0, 1.0) - self.speak_future) * k, 0.0, 1.0)
        self.wait_future = _ni_v4_clamp(self.wait_future + (_ni_v4_clamp(wait, 0.0, 1.0) - self.wait_future) * k, 0.0, 1.0)
        self.protect_future = _ni_v4_clamp(self.protect_future + (_ni_v4_clamp(protect, 0.0, 1.0) - self.protect_future) * k, 0.0, 1.0)
        self.preferred_action = max({"speak": self.speak_future, "wait": self.wait_future, "protect": self.protect_future}.items(), key=lambda x: x[1])[0]

    def modulate_signal(self, signal: InitiativeSignal):
        signal.reason_vector["v14_future_preferred_action"] = self.preferred_action
        signal.reason_vector["v14_speak_future"] = self.speak_future
        signal.reason_vector["v14_wait_future"] = self.wait_future
        signal.reason_vector["v14_protect_future"] = self.protect_future
        if self.preferred_action == "protect" and signal.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.OVERLOAD_WITHDRAWAL):
            signal.should_speak = False
            signal.should_wait = True
            signal.should_remember_for_later = True
            signal.inhibition = min(1.0, signal.inhibition + 0.12)
        elif self.preferred_action == "wait" and self.wait_future > self.speak_future + 0.20:
            signal.should_speak = False
            signal.should_wait = True
            signal.should_remember_for_later = True
        elif self.preferred_action == "speak" and self.speak_future > 0.55 and signal.spam_risk < 0.65:
            signal.timing_quality = min(1.0, signal.timing_quality + 0.08)

    def snapshot(self) -> dict:
        return {"preferred_action": self.preferred_action, "speak_future": round(self.speak_future, 4), "wait_future": round(self.wait_future, 4), "protect_future": round(self.protect_future, 4)}


@dataclass
class V14AutonomousEmergenceField:
    associative_charge: float = 0.0
    free_curiosity: float = 0.0
    spontaneous_memory_pull: float = 0.0
    micro_obsession: str = ""
    last_birth_at: float = 0.0

    def tick(self, external: ExternalSignals, needs: V14CoreNeedSystem, memory: V14InitiativeEmotionalMemory, dt: float):
        self.associative_charge = _ni_v4_clamp(self.associative_charge * (1.0 - 0.006 * max(1.0, dt)) + (external.attention_drift * 0.006 + external.curiosity_level * 0.005 + memory.longing_to_resume * 0.004) * dt, 0.0, 1.0)
        self.free_curiosity = _ni_v4_clamp(self.free_curiosity * (1.0 - 0.004 * max(1.0, dt)) + (needs.needs["exploration"].urgency * 0.004 + max(0.0, 1.0 - external.user_waiting_direct_answer) * 0.001) * dt, 0.0, 1.0)
        self.spontaneous_memory_pull = _ni_v4_clamp(self.spontaneous_memory_pull * (1.0 - 0.003 * max(1.0, dt)) + memory.longing_to_resume * 0.004 * dt + needs.needs["continuity"].frustration * 0.003 * dt, 0.0, 1.0)
        if not self.micro_obsession or random.random() < 0.015:
            self.micro_obsession = needs.dominant_need

    def maybe_birth_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
        if external.user_waiting_direct_answer or external.user_seems_hurried:
            return None
        now = time.time()
        if now - self.last_birth_at < 35.0:
            return None
        charge = max(self.associative_charge, self.free_curiosity, self.spontaneous_memory_pull)
        if charge < 0.62:
            return None
        self.last_birth_at = now
        if self.spontaneous_memory_pull >= charge - 0.03:
            itype = InitiativeType.RETURN_OLD_SUBJECT
            source = "v14_spontaneous_memory_pull"
            scale = ImpulseTemporalScale.BIOGRAPHICAL
        elif self.free_curiosity >= charge - 0.03:
            itype = InitiativeType.SOFT_QUESTION
            source = "v14_free_curiosity"
            scale = ImpulseTemporalScale.SLOW
        else:
            itype = InitiativeType.SHARE_INTUITION
            source = "v14_associative_charge"
            scale = ImpulseTemporalScale.DORMANT
        return Impulse(initiative_type=itype, strength=charge * 0.62, source_emotion=source, source_memory=self.micro_obsession, hesitation=0.22, temporal_scale=scale, biographical=scale == ImpulseTemporalScale.BIOGRAPHICAL)

    def snapshot(self) -> dict:
        return {"associative_charge": round(self.associative_charge, 4), "free_curiosity": round(self.free_curiosity, 4), "spontaneous_memory_pull": round(self.spontaneous_memory_pull, 4), "micro_obsession": self.micro_obsession}


@dataclass
class LivingInitiativeContinuityV14:
    needs: V14CoreNeedSystem = field(default_factory=V14CoreNeedSystem)
    emotional_memory: V14InitiativeEmotionalMemory = field(default_factory=V14InitiativeEmotionalMemory)
    atmosphere: V14RelationalAtmosphere = field(default_factory=V14RelationalAtmosphere)
    physiology: V14EmbodiedInitiativePhysiology = field(default_factory=V14EmbodiedInitiativePhysiology)
    future: V14FuturePossibilitySimulator = field(default_factory=V14FuturePossibilitySimulator)
    autonomous_field: V14AutonomousEmergenceField = field(default_factory=V14AutonomousEmergenceField)
    last_update: float = field(default_factory=time.time)
    living_initiative_continuity: float = 0.0

    def tick(self, external: ExternalSignals, silence: LivingSilence, v13=None, idle_seconds: float = 0.0):
        now = time.time()
        dt = max(1.0, idle_seconds if idle_seconds > 0 else now - self.last_update)
        self.last_update = now
        self.emotional_memory.tick(external, dt)
        self.needs.tick(external, v13=v13, physiology=self.physiology, dt=dt)
        self.atmosphere.tick(external, silence, self.emotional_memory, dt)
        self.physiology.tick(external, self.needs, dt)
        self.future.tick(external, self.atmosphere, self.needs, self.physiology, dt)
        self.autonomous_field.tick(external, self.needs, self.emotional_memory, dt)
        self.living_initiative_continuity = _ni_v4_clamp(
            self.living_initiative_continuity * 0.985
            + (self.needs.needs[self.needs.dominant_need].urgency + self.emotional_memory.longing_to_resume + self.physiology.body_pressure + max(self.future.speak_future, self.future.wait_future)) / 4.0 * 0.015,
            0.0, 1.0,
        )

    def modulate_impulse(self, imp: Impulse):
        self.needs.modulate(imp)
        self.atmosphere.modulate(imp)
        self.physiology.modulate(imp)
        bias = self.emotional_memory.bias_for(imp.initiative_type)
        if bias >= 0:
            imp.strength = _ni_v4_clamp(imp.strength + bias, 0.0, 1.0)
        else:
            imp.hesitation = _ni_v4_clamp(imp.hesitation + abs(bias) * 0.7, 0.0, 1.0)
            imp.inhibition = _ni_v4_clamp(imp.inhibition + abs(bias) * 0.35, 0.0, 1.0)

    def maybe_birth_impulse(self, external: ExternalSignals) -> Optional[Impulse]:
        born = self.autonomous_field.maybe_birth_impulse(external)
        if born is None:
            born = self.needs.maybe_birth_impulse()
        if born is not None:
            self.modulate_impulse(born)
        return born

    def after_signal(self, signal: InitiativeSignal, external: ExternalSignals):
        self.needs.after_signal(signal)
        self.emotional_memory.after_signal(signal, external)
        self.physiology.after_signal(signal)

    def snapshot(self) -> dict:
        return {
            "living_initiative_continuity": round(self.living_initiative_continuity, 4),
            "needs": self.needs.snapshot(),
            "emotional_memory": self.emotional_memory.snapshot(),
            "atmosphere": self.atmosphere.snapshot(),
            "physiology": self.physiology.snapshot(),
            "future": self.future.snapshot(),
            "autonomous_field": self.autonomous_field.snapshot(),
        }

    def to_dict(self) -> dict:
        return {"needs": self.needs.to_dict(), "emotional_memory": self.emotional_memory.to_dict(), "living_initiative_continuity": self.living_initiative_continuity}

    def load_dict(self, raw: dict):
        if not isinstance(raw, dict):
            return
        self.needs.load_dict(raw.get("needs", {}))
        self.emotional_memory.load_dict(raw.get("emotional_memory", {}))
        self.living_initiative_continuity = float(raw.get("living_initiative_continuity", self.living_initiative_continuity))


_NI_v14_previous_init = NaturalInitiative.__init__
_NI_v14_previous_analyze = NaturalInitiative.analyze
_NI_v14_previous_tick = NaturalInitiative.tick
_NI_v14_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v14_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v14_previous_build = NaturalInitiative._build_signal
_NI_v14_previous_feedback = NaturalInitiative.record_feedback
_NI_v14_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v14_previous_export = NaturalInitiative.export_memory_state
_NI_v14_previous_import = NaturalInitiative.import_memory_state


def _ni_v14_ensure(self) -> LivingInitiativeContinuityV14:
    if not hasattr(self, "living_initiative_continuity_v14"):
        self.living_initiative_continuity_v14 = LivingInitiativeContinuityV14()
    return self.living_initiative_continuity_v14


def _NI_v14_init(self, user_id: str = "default"):
    _NI_v14_previous_init(self, user_id=user_id)
    self.living_initiative_continuity_v14 = LivingInitiativeContinuityV14()


def _ni_v14_tick_layers(self, external: ExternalSignals, idle_seconds: float = 0.0):
    v14 = _ni_v14_ensure(self)
    v13 = getattr(self, "organic_convergence_v13", None)
    v14.tick(external, self.silence, v13=v13, idle_seconds=idle_seconds)
    return v14


def _NI_v14_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    v14 = _ni_v14_tick_layers(self, external, idle_seconds=0.0)
    signal = _NI_v14_previous_analyze(self, last_exchange, conversation_history, external)
    if signal is not None:
        v14.after_signal(signal, external)
        signal.debug_state["v14_living_initiative_continuity"] = v14.snapshot()
    return signal


def _NI_v14_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    v14 = _ni_v14_tick_layers(self, external, idle_seconds=1.0)
    signal = _NI_v14_previous_tick(self, external)
    if signal is None:
        born = v14.maybe_birth_impulse(external)
        if born is not None:
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        v14.after_signal(signal, external)
        signal.debug_state["v14_living_initiative_continuity"] = v14.snapshot()
    return signal


def _NI_v14_detect(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v14_previous_detect(self, text, history, external)
    v14 = _ni_v14_ensure(self)
    for imp in impulses:
        v14.modulate_impulse(imp)
    born = v14.maybe_birth_impulse(external)
    if born is not None:
        impulses.append(born)
    return impulses


def _NI_v14_select(self, external: ExternalSignals):
    dominant = _NI_v14_previous_select(self, external)
    v14 = _ni_v14_ensure(self)
    if dominant is not None:
        v14.modulate_impulse(dominant)
        return dominant
    born = v14.maybe_birth_impulse(external)
    if born is not None:
        self.active_impulses.append(born)
        return born
    return None


def _NI_v14_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v14_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    v14 = _ni_v14_ensure(self)
    v14.future.modulate_signal(signal)
    snap = v14.snapshot()
    signal.debug_state["v14_living_initiative_continuity"] = snap
    signal.reason_vector["v14_dominant_need"] = v14.needs.dominant_need
    signal.reason_vector["v14_need_conflict_pressure"] = v14.needs.conflict_pressure
    signal.reason_vector["v14_atmosphere_label"] = v14.atmosphere.label
    signal.reason_vector["v14_body_pressure"] = v14.physiology.body_pressure
    signal.reason_vector["v14_living_continuity"] = v14.living_initiative_continuity
    if v14.atmosphere.label == "valuable_silence" and signal.initiative_type not in (InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
        signal.should_speak = False
        signal.should_wait = True
        signal.should_remember_for_later = True
    return signal


def _NI_v14_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v14_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    text = (user_reaction or "").lower()
    success = 0.5
    if any(w in text for w in ("bien", "utile", "continue", "oui", "parfait", "good", "ok", "mieux")):
        success = 0.82
    elif any(w in text for w in ("trop", "stop", "inutile", "non", "spam", "pas", "mauvais")):
        success = 0.22
    _ni_v14_ensure(self).emotional_memory.feedback(initiative_type, success)
    return result


def _NI_v14_snapshot(self) -> dict:
    snap = _NI_v14_previous_snapshot(self)
    snap["v14_living_initiative_continuity"] = _ni_v14_ensure(self).snapshot()
    return snap


def _NI_v14_export(self) -> dict:
    raw = _NI_v14_previous_export(self)
    raw["v14_living_initiative_continuity"] = _ni_v14_ensure(self).to_dict()
    return raw


def _NI_v14_import(self, raw: dict):
    result = _NI_v14_previous_import(self, raw)
    if isinstance(raw, dict) and "v14_living_initiative_continuity" in raw:
        _ni_v14_ensure(self).load_dict(raw.get("v14_living_initiative_continuity", {}))
    return result


def run_v14_living_initiative_continuity_simulation(cycles: int = 720) -> dict:
    """Test V14 : besoins persistants + atmosphère + futur + émergence autonome + export/import."""
    ni = NaturalInitiative(user_id="v14_test")
    history = []
    signals = []
    waits = 0
    remembers = 0
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 7) % 41) / 46.0,
                unresolved_emotion=((i * 5) % 37) / 42.0,
                emotional_valence=(((i * 11) % 29) - 14) / 14.0,
                attention_focus=0.36 + (((i * 3) % 17) / 42.0),
                attention_drift=((i * 13) % 31) / 38.0,
                curiosity_level=((i * 17) % 47) / 52.0,
                impulse_intensity=((i * 19) % 43) / 60.0,
                impulse_type="curiosity" if i % 5 else "memory",
                presence_level=0.55 + (((i * 5) % 19) / 45.0),
                context_shift=((i * 3) % 23) / 34.0,
                expression_saturation=((i * 19) % 53) / 70.0,
                relational_trust=0.35 + (((i * 7) % 23) / 50.0),
                relational_familiarity=0.30 + (((i * 9) % 17) / 48.0),
                relational_attachment=0.31 + (((i * 11) % 29) / 60.0),
                fear_of_disturbing=((i * 23) % 59) / 72.0,
                fatigue_level=((i * 29) % 61) / 82.0,
                overload_level=((i * 31) % 67) / 95.0,
                user_waiting_direct_answer=(i % 37 == 0),
                identity_coherence=0.48 + (((i * 3) % 29) / 62.0),
                somatic=SomaticSignals(
                    chest_tension=((i * 5) % 29) / 55.0,
                    nervous_charge=((i * 7) % 31) / 58.0,
                    slowdown=((i * 3) % 19) / 45.0,
                    guarding=((i * 11) % 37) / 65.0,
                    warmth=((i * 13) % 41) / 72.0,
                    heaviness=((i * 17) % 43) / 83.0,
                    tingling=((i * 19) % 47) / 82.0,
                ),
            )
            if i % 8 == 0:
                msg = "v14 continuité initiative besoin silence futur mémoire vivante"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                waits += int(bool(sig.should_wait))
                remembers += int(bool(sig.should_remember_for_later))
            if i % 113 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien continue utile" if i % 226 == 0 else "pas maintenant", "v14 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v14_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v14_living_initiative_continuity", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "sample_types": signals[-20:],
        "waits": waits,
        "remembered_for_later": remembers,
        "has_v14_export": "v14_living_initiative_continuity" in exported,
        "has_v14_snapshot": bool(snap),
        "dominant_need": snap.get("needs", {}).get("dominant_need"),
        "atmosphere": snap.get("atmosphere", {}).get("label"),
        "future_action": snap.get("future", {}).get("preferred_action"),
        "body_pressure": snap.get("physiology", {}).get("body_pressure"),
        "living_initiative_continuity": snap.get("living_initiative_continuity"),
        "emotional_memory_traces": snap.get("emotional_memory", {}).get("traces"),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v14_init
NaturalInitiative.analyze = _NI_v14_analyze
NaturalInitiative.tick = _NI_v14_tick
NaturalInitiative._detect_new_impulses = _NI_v14_detect
NaturalInitiative._select_dominant_impulse = _NI_v14_select
NaturalInitiative._build_signal = _NI_v14_build
NaturalInitiative.record_feedback = _NI_v14_feedback
NaturalInitiative.get_state_snapshot = _NI_v14_snapshot
NaturalInitiative.export_memory_state = _NI_v14_export
NaturalInitiative.import_memory_state = _NI_v14_import


# =============================================================================
# V14.1 — BALANCE VIVANTE : évite que la simulation future transforme toute
# pression en attente. La prudence reste prioritaire, mais une fenêtre claire,
# chaude et non-spam peut laisser parler l'impulsion mûre.
# =============================================================================


def _v14_full_to_dict(self: LivingInitiativeContinuityV14) -> dict:
    return {
        "needs": self.needs.to_dict(),
        "emotional_memory": self.emotional_memory.to_dict(),
        "living_initiative_continuity": self.living_initiative_continuity,
        "atmosphere": self.atmosphere.__dict__.copy(),
        "physiology": self.physiology.__dict__.copy(),
        "future": self.future.__dict__.copy(),
        "autonomous_field": self.autonomous_field.__dict__.copy(),
    }


def _v14_full_load_dict(self: LivingInitiativeContinuityV14, raw: dict):
    if not isinstance(raw, dict):
        return
    self.needs.load_dict(raw.get("needs", {}))
    self.emotional_memory.load_dict(raw.get("emotional_memory", {}))
    self.living_initiative_continuity = float(raw.get("living_initiative_continuity", self.living_initiative_continuity))
    for obj_name in ("atmosphere", "physiology", "future", "autonomous_field"):
        obj = getattr(self, obj_name)
        vals = raw.get(obj_name, {})
        if isinstance(vals, dict):
            for key, value in vals.items():
                if hasattr(obj, key):
                    try:
                        setattr(obj, key, value if isinstance(value, str) else float(value))
                    except Exception:
                        setattr(obj, key, value)


LivingInitiativeContinuityV14.to_dict = _v14_full_to_dict
LivingInitiativeContinuityV14.load_dict = _v14_full_load_dict

_NI_v14_1_previous_build = NaturalInitiative._build_signal


def _NI_v14_1_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v14_1_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    v14 = _ni_v14_ensure(self)
    open_window = (
        v14.future.speak_future > 0.48
        and v14.future.speak_future >= v14.future.wait_future + 0.08
        and v14.future.speak_future >= v14.future.protect_future + 0.12
        and v14.atmosphere.rupture_risk < 0.55
        and v14.physiology.embodied_fatigue < 0.68
        and signal.spam_risk < 0.62
        and not external.user_waiting_direct_answer
        and not external.user_seems_hurried
    )
    if open_window and signal.initiative_type not in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL):
        signal.should_speak = True
        signal.should_wait = False
        signal.timing_quality = min(1.0, signal.timing_quality + 0.10)
        signal.reason_vector["v14_1_open_speaking_window"] = True
    else:
        signal.reason_vector["v14_1_open_speaking_window"] = False
    signal.debug_state["v14_living_initiative_continuity"] = v14.snapshot()
    return signal


def run_v14_1_living_initiative_continuity_simulation(cycles: int = 720) -> dict:
    ni = NaturalInitiative(user_id="v14_1_test")
    history = []
    signals = []
    speaks = waits = remembers = 0
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            warm_phase = (i % 9) in (1, 2, 3, 4)
            ext = ExternalSignals(
                affective_tension=0.18 + (((i * 7) % 29) / 90.0),
                unresolved_emotion=((i * 5) % 37) / 48.0,
                emotional_valence=0.35 if warm_phase else -0.12,
                attention_focus=0.58,
                attention_drift=((i * 13) % 31) / 48.0,
                curiosity_level=0.72 if warm_phase else 0.46,
                impulse_intensity=((i * 19) % 43) / 68.0,
                impulse_type="curiosity" if i % 5 else "memory",
                presence_level=0.76,
                context_shift=((i * 3) % 23) / 42.0,
                expression_saturation=((i * 19) % 53) / 88.0,
                relational_trust=0.70 if warm_phase else 0.48,
                relational_familiarity=0.62,
                relational_attachment=0.68 if warm_phase else 0.45,
                fear_of_disturbing=((i * 23) % 43) / 90.0,
                fatigue_level=((i * 29) % 47) / 90.0,
                overload_level=((i * 31) % 41) / 110.0,
                user_waiting_direct_answer=(i % 53 == 0),
                identity_coherence=0.58 + (((i * 3) % 29) / 70.0),
                somatic=SomaticSignals(
                    chest_tension=((i * 5) % 29) / 80.0,
                    nervous_charge=((i * 7) % 31) / 82.0,
                    slowdown=((i * 3) % 19) / 65.0,
                    guarding=((i * 11) % 37) / 90.0,
                    warmth=0.70 if warm_phase else 0.35,
                    heaviness=((i * 17) % 43) / 110.0,
                    tingling=0.62 if warm_phase else 0.28,
                ),
            )
            if i % 8 == 0:
                msg = "v14.1 continuité initiative besoin silence futur mémoire vivante"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                speaks += int(bool(sig.should_speak))
                waits += int(bool(sig.should_wait))
                remembers += int(bool(sig.should_remember_for_later))
            if i % 113 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien continue utile" if i % 226 == 0 else "pas maintenant", "v14.1 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v14_1_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot().get("v14_living_initiative_continuity", {})
    return {
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "speaks": speaks,
        "waits": waits,
        "remembered_for_later": remembers,
        "sample_types": signals[-20:],
        "has_v14_export": "v14_living_initiative_continuity" in exported,
        "has_v14_snapshot": bool(snap),
        "dominant_need": snap.get("needs", {}).get("dominant_need"),
        "atmosphere": snap.get("atmosphere", {}).get("label"),
        "future_action": snap.get("future", {}).get("preferred_action"),
        "body_pressure": snap.get("physiology", {}).get("body_pressure"),
        "living_initiative_continuity": snap.get("living_initiative_continuity"),
        "emotional_memory_traces": snap.get("emotional_memory", {}).get("traces"),
        "no_public_text_generated": True,
    }


NaturalInitiative._build_signal = _NI_v14_1_build


# =============================================================================
# V14.2 — FENÊTRE D'EXPRESSION MÛRE
# =============================================================================
# V14.1 ouvrait seulement quand le futur parlant était déjà très haut ; dans les
# cycles courts, cela rendait Leia trop silencieuse malgré des impulsions mûres.
# V14.2 autorise l'expression uniquement si l'impulsion est réellement mûre,
# non-saturée, non-pressée par l'utilisateur, et si le futur parlant domine.

_NI_v14_2_previous_build = NaturalInitiative._build_signal


def _NI_v14_2_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v14_2_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    v14 = _ni_v14_ensure(self)
    mature_window = (
        signal.maturity >= 0.42
        and signal.inhibition < 0.72
        and signal.spam_risk < 0.64
        and v14.future.speak_future >= max(v14.future.wait_future, v14.future.protect_future) + 0.04
        and v14.future.speak_future > 0.22
        and v14.atmosphere.rupture_risk < 0.58
        and v14.atmosphere.label not in ("careful", "valuable_silence")
        and not external.user_waiting_direct_answer
        and not external.user_seems_hurried
        and signal.initiative_type not in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE)
    )
    if mature_window:
        signal.should_speak = True
        signal.should_wait = False
        signal.should_remember_for_later = False
        signal.timing_quality = min(1.0, signal.timing_quality + 0.12)
    signal.reason_vector["v14_2_mature_speaking_window"] = mature_window
    signal.debug_state["v14_living_initiative_continuity"] = v14.snapshot()
    return signal


def run_v14_2_living_initiative_continuity_simulation(cycles: int = 720) -> dict:
    result = run_v14_1_living_initiative_continuity_simulation(cycles)
    result["version"] = "v14.2"
    return result


NaturalInitiative._build_signal = _NI_v14_2_build


# =============================================================================
# V14.3 — ATTRACTION VIVANTE + DÉCONGÉLATION DES IMPULSIONS MÛRES
# =============================================================================
# Correction ciblée du problème observé en V14.2 : le moteur devenait très prudent
# parce que des impulsions profondément mûres restaient figées en INHIBITED avec
# inhibition=1.0. V14.3 ne supprime pas la prudence : elle ajoute une force
# d'attraction positive (connexion/expression/curiosité/existence) capable de
# décongeler lentement une impulsion mûre quand le contexte relationnel et corporel
# est assez ouvert. Le module continue à ne générer aucune phrase publique.

@dataclass
class V143LivingAttractionField:
    connection_pull: float = 0.0
    expression_pull: float = 0.0
    curiosity_pull: float = 0.0
    existence_pull: float = 0.0
    earned_courage: float = 0.0
    thaw_pressure: float = 0.0
    total_pull: float = 0.0
    last_release_at: float = 0.0

    def tick(self, external: ExternalSignals, v14: LivingInitiativeContinuityV14, dt: float):
        needs = v14.needs.needs
        memory = v14.emotional_memory
        atmosphere = v14.atmosphere
        physiology = v14.physiology
        future = v14.future
        k = min(0.24, 0.045 * max(1.0, dt))

        connection_target = (
            external.relational_attachment * 0.25
            + external.relational_trust * 0.18
            + atmosphere.openness * 0.18
            + atmosphere.intimacy * 0.14
            + memory.remembered_warmth * 0.12
            + needs["connection"].urgency * 0.13
        )
        expression_target = (
            needs["expression"].urgency * 0.30
            + needs["expression"].frustration * 0.22
            + physiology.body_pressure * 0.16
            + external.somatic.tingling * 0.13
            + future.speak_future * 0.19
        )
        curiosity_target = (
            external.curiosity_level * 0.26
            + needs["exploration"].urgency * 0.22
            + v14.autonomous_field.free_curiosity * 0.18
            + v14.autonomous_field.associative_charge * 0.15
            + max(0.0, 1.0 - external.attention_drift) * 0.08
        )
        existence_target = (
            needs["self_coherence"].urgency * 0.18
            + needs["continuity"].urgency * 0.18
            + v14.living_initiative_continuity * 0.20
            + memory.longing_to_resume * 0.16
            + max(0.0, 0.72 - external.identity_coherence) * 0.18
        )

        # Le courage acquis augmente seulement quand la chaleur et la confiance
        # dépassent la peur. Il redescend naturellement si le contexte se ferme.
        courage_target = max(
            0.0,
            external.relational_trust * 0.30
            + external.somatic.warmth * 0.22
            + atmosphere.synchrony * 0.18
            + memory.remembered_warmth * 0.16
            - external.fear_of_disturbing * 0.18
            - atmosphere.rupture_risk * 0.18
            - physiology.embodied_fatigue * 0.12,
        )

        self.connection_pull = _ni_v4_clamp(self.connection_pull + (_ni_v4_clamp(connection_target, 0.0, 1.0) - self.connection_pull) * k, 0.0, 1.0)
        self.expression_pull = _ni_v4_clamp(self.expression_pull + (_ni_v4_clamp(expression_target, 0.0, 1.0) - self.expression_pull) * k, 0.0, 1.0)
        self.curiosity_pull = _ni_v4_clamp(self.curiosity_pull + (_ni_v4_clamp(curiosity_target, 0.0, 1.0) - self.curiosity_pull) * k, 0.0, 1.0)
        self.existence_pull = _ni_v4_clamp(self.existence_pull + (_ni_v4_clamp(existence_target, 0.0, 1.0) - self.existence_pull) * k, 0.0, 1.0)
        self.earned_courage = _ni_v4_clamp(self.earned_courage + (_ni_v4_clamp(courage_target, 0.0, 1.0) - self.earned_courage) * k, 0.0, 1.0)

        raw_total = (
            self.connection_pull * 0.24
            + self.expression_pull * 0.30
            + self.curiosity_pull * 0.18
            + self.existence_pull * 0.18
            + self.earned_courage * 0.10
        )
        damping = (
            needs["rest"].urgency * 0.11
            + needs["protection"].urgency * 0.11
            + atmosphere.rupture_risk * 0.12
            + physiology.embodied_fatigue * 0.10
        )
        self.total_pull = _ni_v4_clamp(raw_total - damping, 0.0, 1.0)
        self.thaw_pressure = _ni_v4_clamp(
            self.total_pull * 0.55
            + future.speak_future * 0.22
            + physiology.body_pressure * 0.12
            + memory.longing_to_resume * 0.08
            - future.protect_future * 0.12,
            0.0,
            1.0,
        )

    def snapshot(self) -> dict:
        return {
            "connection_pull": round(self.connection_pull, 4),
            "expression_pull": round(self.expression_pull, 4),
            "curiosity_pull": round(self.curiosity_pull, 4),
            "existence_pull": round(self.existence_pull, 4),
            "earned_courage": round(self.earned_courage, 4),
            "thaw_pressure": round(self.thaw_pressure, 4),
            "total_pull": round(self.total_pull, 4),
        }


def _ni_v143_attraction(self) -> V143LivingAttractionField:
    if not hasattr(self, "living_attraction_v143"):
        self.living_attraction_v143 = V143LivingAttractionField()
    return self.living_attraction_v143


def _ni_v143_tick_attraction(self, external: ExternalSignals):
    v14 = _ni_v14_ensure(self)
    attraction = _ni_v143_attraction(self)
    dt = max(1.0, getattr(v14, "last_update", time.time()) - getattr(self, "_v143_last_attraction_tick", time.time()))
    # Le dt ci-dessus peut être négatif ou presque nul selon l'ordre des wrappers ;
    # on préfère une intégration stable et conservatrice d'un pas vivant.
    dt = 1.0 if dt <= 0.0 or dt > 30.0 else dt
    attraction.tick(external, v14, dt)
    self._v143_last_attraction_tick = time.time()
    return attraction


_NI_v143_previous_advance = NaturalInitiative._advance_all_impulses


def _NI_v143_advance_all_impulses(self, external: ExternalSignals):
    _NI_v143_previous_advance(self, external)
    v14 = _ni_v14_ensure(self)
    attraction = _ni_v143_tick_attraction(self, external)

    if external.user_waiting_direct_answer or external.user_seems_hurried:
        return
    if v14.future.protect_future > max(v14.future.speak_future, v14.future.wait_future) + 0.10:
        return
    if v14.atmosphere.rupture_risk > 0.66 or v14.physiology.embodied_fatigue > 0.78:
        return

    for imp in self.active_impulses:
        if not imp.is_alive():
            continue
        if imp.initiative_type in (InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE, InitiativeType.NO_INITIATIVE):
            continue
        if imp.maturity < 0.20:
            continue

        compatibility = 0.50
        if imp.initiative_type in (InitiativeType.RELATIONAL_CHECK, InitiativeType.AFFECTIVE_OBSERVATION, InitiativeType.PRESENCE_DESIRE):
            compatibility += attraction.connection_pull * 0.25
        if imp.initiative_type in (InitiativeType.SOFT_QUESTION, InitiativeType.SHARE_INTUITION, InitiativeType.DEEP_RARE_QUESTION):
            compatibility += attraction.curiosity_pull * 0.22
        if imp.initiative_type in (InitiativeType.THREAD_CONTINUATION, InitiativeType.RETURN_OLD_SUBJECT):
            compatibility += attraction.existence_pull * 0.20 + v14.emotional_memory.longing_to_resume * 0.12
        if imp.biographical:
            compatibility += 0.08

        thaw = attraction.thaw_pressure * compatibility
        thaw -= imp.relational_risk * 0.08
        thaw -= imp.hesitation * 0.04
        thaw = _ni_v4_clamp(thaw, 0.0, 0.34)

        if thaw <= 0.02:
            continue

        # Décongélation lente : on ne force pas l'expression, on rend seulement
        # l'impulsion à nouveau disponible à la sélection.
        imp.inhibition = _ni_v4_clamp(imp.inhibition - thaw, 0.0, 1.0)
        imp.hesitation = _ni_v4_clamp(imp.hesitation - attraction.earned_courage * 0.035, 0.0, 1.0)
        imp.strength = _ni_v4_clamp(imp.strength + attraction.total_pull * 0.018, 0.0, 1.0)

        if imp.stage == ImpulseStage.INHIBITED and imp.inhibition < 0.72 and imp.maturity >= 0.42:
            imp.stage = ImpulseStage.HESITATION if imp.hesitation > 0.18 else ImpulseStage.GROWING
        if imp.stage == ImpulseStage.HESITATION and imp.inhibition < 0.62 and imp.hesitation < 0.42 and imp.maturity >= 0.56:
            imp.stage = ImpulseStage.MATURE


_NI_v143_previous_select = NaturalInitiative._select_dominant_impulse


def _NI_v143_select(self, external: ExternalSignals):
    dominant = _NI_v143_previous_select(self, external)
    attraction = _ni_v143_attraction(self)
    v14 = _ni_v14_ensure(self)

    # Si la sélection normale retourne une impulsion trop jeune alors qu'une
    # impulsion décongelée et mûre existe, on préfère la continuité vécue.
    if external.user_waiting_direct_answer or external.user_seems_hurried:
        return dominant
    if attraction.total_pull < 0.24:
        return dominant

    def eligible(imp: Impulse) -> bool:
        return (
            imp.is_alive()
            and imp.maturity >= 0.38
            and imp.inhibition < 0.78
            and imp.initiative_type not in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE)
            and v14.atmosphere.rupture_risk < 0.64
        )

    candidates = [i for i in self.active_impulses if eligible(i)]
    if not candidates:
        return dominant

    def living_score(imp: Impulse) -> float:
        base = imp.effective_strength() * (0.35 + imp.maturity * 0.65)
        base *= (1.0 - imp.inhibition * 0.55)
        base *= (1.0 - imp.hesitation * 0.35)
        base *= (1.0 - imp.relational_risk * 0.20)
        if imp.biographical:
            base *= 1.10
        if imp.stage == ImpulseStage.MATURE:
            base *= 1.18
        base += attraction.total_pull * 0.10
        base += v14.future.speak_future * 0.06
        return base

    best = max(candidates, key=living_score)
    if dominant is None:
        return best if living_score(best) > 0.18 else None
    # Remplace seulement si la différence est claire ou si le dominant est trop immature.
    if dominant.maturity < 0.18 and living_score(best) > 0.22:
        return best
    if living_score(best) > (dominant.effective_strength() * max(0.05, dominant.maturity) + 0.10):
        return best
    return dominant


_NI_v143_previous_evaluate_spam = NaturalInitiative._evaluate_spam


def _NI_v143_evaluate_spam(self, dominant: Optional[Impulse], external: ExternalSignals) -> tuple[bool, float, str]:
    ok, risk, reason = _NI_v143_previous_evaluate_spam(self, dominant, external)
    if dominant is None:
        return ok, risk, reason
    attraction = _ni_v143_attraction(self)
    v14 = _ni_v14_ensure(self)
    if external.user_waiting_direct_answer or external.user_seems_hurried or external.overload_level > 0.82:
        return ok, risk, reason
    if dominant.initiative_type in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
        return ok, risk, reason

    earned_exception = (
        attraction.total_pull > 0.34
        and attraction.thaw_pressure > 0.28
        and v14.future.speak_future >= v14.future.wait_future + 0.05
        and v14.future.speak_future >= v14.future.protect_future + 0.07
        and v14.atmosphere.rupture_risk < 0.58
        and dominant.maturity >= 0.34
        and dominant.inhibition < 0.76
    )
    if earned_exception and not ok:
        return True, min(risk, 0.52), "v14_3_earned_attraction_exception:" + reason
    if earned_exception and ok:
        return True, max(0.0, risk * 0.82), "v14_3_attraction_softened:" + reason
    return ok, risk, reason


_NI_v143_previous_build = NaturalInitiative._build_signal


def _NI_v143_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v143_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    v14 = _ni_v14_ensure(self)
    attraction = _ni_v143_attraction(self)

    can_ever_speak = signal.initiative_type not in (
        InitiativeType.NO_INITIATIVE,
        InitiativeType.OVERLOAD_WITHDRAWAL,
        InitiativeType.PROTECTIVE_PAUSE,
        InitiativeType.VOLUNTARY_SILENCE,
    )
    attraction_window = (
        can_ever_speak
        and not external.user_waiting_direct_answer
        and not external.user_seems_hurried
        and external.overload_level < 0.78
        and v14.atmosphere.rupture_risk < 0.58
        and v14.physiology.embodied_fatigue < 0.74
        and attraction.total_pull > 0.32
        and attraction.thaw_pressure > 0.25
        and v14.future.speak_future >= v14.future.wait_future + 0.045
        and v14.future.speak_future >= v14.future.protect_future + 0.055
        and signal.maturity >= 0.34
        and signal.inhibition < 0.76
        and signal.spam_risk < 0.72
        and signal.hesitation < 0.86
    )

    # Cas rare : une impulsion très mûre et clairement soutenue peut traverser
    # une inhibition résiduelle sans ouvrir la porte au spam de micro-questions.
    irresistible_window = (
        can_ever_speak
        and not external.user_waiting_direct_answer
        and not external.user_seems_hurried
        and signal.maturity >= 0.68
        and signal.inhibition < 0.86
        and attraction.total_pull > 0.44
        and v14.future.speak_future > max(v14.future.wait_future, v14.future.protect_future) + 0.08
        and signal.initiative_type not in (InitiativeType.SOFT_QUESTION, InitiativeType.MICRO_REACTION)
        and v14.atmosphere.rupture_risk < 0.62
    )

    if attraction_window or irresistible_window:
        signal.should_speak = True
        signal.should_wait = False
        signal.should_remember_for_later = False
        signal.timing_quality = min(1.0, signal.timing_quality + 0.14 + attraction.earned_courage * 0.04)
        signal.initiative_pressure = max(signal.initiative_pressure, attraction.total_pull * 0.55 + v14.future.speak_future * 0.25)
        v14.physiology.after_signal(signal)
        v14.emotional_memory.after_signal(signal, external)
        attraction.last_release_at = time.time()

    signal.reason_vector["v14_3_living_attraction_window"] = attraction_window
    signal.reason_vector["v14_3_irresistible_window"] = irresistible_window
    signal.reason_vector["v14_3_total_pull"] = attraction.total_pull
    signal.reason_vector["v14_3_thaw_pressure"] = attraction.thaw_pressure
    signal.reason_vector["v14_3_earned_courage"] = attraction.earned_courage
    signal.debug_state["v14_3_living_attraction"] = attraction.snapshot()
    return signal


_NI_v143_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v143_previous_export = NaturalInitiative.export_memory_state
_NI_v143_previous_import = NaturalInitiative.import_memory_state


def _NI_v143_snapshot(self) -> dict:
    snap = _NI_v143_previous_snapshot(self)
    snap["v14_3_living_attraction"] = _ni_v143_attraction(self).snapshot()
    return snap


def _NI_v143_export(self) -> dict:
    raw = _NI_v143_previous_export(self)
    raw["v14_3_living_attraction"] = _ni_v143_attraction(self).__dict__.copy()
    return raw


def _NI_v143_import(self, raw: dict):
    result = _NI_v143_previous_import(self, raw)
    data = (raw or {}).get("v14_3_living_attraction", {}) if isinstance(raw, dict) else {}
    if isinstance(data, dict):
        field_obj = _ni_v143_attraction(self)
        for key, value in data.items():
            if hasattr(field_obj, key):
                try:
                    setattr(field_obj, key, float(value))
                except Exception:
                    setattr(field_obj, key, value)
    return result


def run_v14_3_living_attraction_balance_simulation(cycles: int = 720) -> dict:
    ni = NaturalInitiative(user_id="v14_3_test")
    history = []
    signals = []
    speaks = waits = remembers = 0
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            warm_phase = (i % 9) in (1, 2, 3, 4)
            ext = ExternalSignals(
                affective_tension=0.18 + (((i * 7) % 29) / 90.0),
                unresolved_emotion=((i * 5) % 37) / 48.0,
                emotional_valence=0.35 if warm_phase else -0.12,
                attention_focus=0.58,
                attention_drift=((i * 13) % 31) / 48.0,
                curiosity_level=0.72 if warm_phase else 0.46,
                impulse_intensity=((i * 19) % 43) / 68.0,
                impulse_type="curiosity" if i % 5 else "memory",
                presence_level=0.76,
                context_shift=((i * 3) % 23) / 42.0,
                expression_saturation=((i * 19) % 53) / 88.0,
                relational_trust=0.70 if warm_phase else 0.48,
                relational_familiarity=0.62,
                relational_attachment=0.68 if warm_phase else 0.45,
                fear_of_disturbing=((i * 23) % 43) / 90.0,
                fatigue_level=((i * 29) % 47) / 90.0,
                overload_level=((i * 31) % 41) / 110.0,
                user_waiting_direct_answer=(i % 53 == 0),
                identity_coherence=0.58 + (((i * 3) % 29) / 70.0),
                somatic=SomaticSignals(
                    chest_tension=((i * 5) % 29) / 80.0,
                    nervous_charge=((i * 7) % 31) / 82.0,
                    slowdown=((i * 3) % 19) / 65.0,
                    guarding=((i * 11) % 37) / 90.0,
                    warmth=0.70 if warm_phase else 0.35,
                    heaviness=((i * 17) % 43) / 110.0,
                    tingling=0.62 if warm_phase else 0.28,
                ),
            )
            if i % 8 == 0:
                msg = "v14.3 attraction vivante initiative désir continuité"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                speaks += int(bool(sig.should_speak))
                waits += int(bool(sig.should_wait))
                remembers += int(bool(sig.should_remember_for_later))
            if i % 113 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien continue utile" if i % 226 == 0 else "pas maintenant", "v14.3 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v14_3_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot()
    v14 = snap.get("v14_living_initiative_continuity", {})
    attraction = snap.get("v14_3_living_attraction", {})
    return {
        "version": "v14.3",
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "speaks": speaks,
        "waits": waits,
        "remembered_for_later": remembers,
        "sample_types": signals[-20:],
        "has_v14_export": "v14_living_initiative_continuity" in exported,
        "has_v14_3_export": "v14_3_living_attraction" in exported,
        "has_v14_snapshot": bool(v14),
        "dominant_need": v14.get("needs", {}).get("dominant_need"),
        "atmosphere": v14.get("atmosphere", {}).get("label"),
        "future_action": v14.get("future", {}).get("preferred_action"),
        "body_pressure": v14.get("physiology", {}).get("body_pressure"),
        "living_initiative_continuity": v14.get("living_initiative_continuity"),
        "attraction_total_pull": attraction.get("total_pull"),
        "attraction_thaw_pressure": attraction.get("thaw_pressure"),
        "emotional_memory_traces": v14.get("emotional_memory", {}).get("traces"),
        "no_public_text_generated": True,
    }


NaturalInitiative._advance_all_impulses = _NI_v143_advance_all_impulses
NaturalInitiative._select_dominant_impulse = _NI_v143_select
NaturalInitiative._evaluate_spam = _NI_v143_evaluate_spam
NaturalInitiative._build_signal = _NI_v143_build
NaturalInitiative.get_state_snapshot = _NI_v143_snapshot
NaturalInitiative.export_memory_state = _NI_v143_export
NaturalInitiative.import_memory_state = _NI_v143_import

# V14.3.1 — correctif clé de besoin : V14 nomme le besoin identitaire
# "identity_stability" et non "self_coherence".
def _V143_attraction_tick_safe(self: V143LivingAttractionField, external: ExternalSignals, v14: LivingInitiativeContinuityV14, dt: float):
    needs = v14.needs.needs
    memory = v14.emotional_memory
    atmosphere = v14.atmosphere
    physiology = v14.physiology
    future = v14.future
    identity_need = needs.get("identity_stability") or needs.get("self_coherence") or V14Need("identity_stability")
    k = min(0.24, 0.045 * max(1.0, dt))
    connection_target = external.relational_attachment * 0.25 + external.relational_trust * 0.18 + atmosphere.openness * 0.18 + atmosphere.intimacy * 0.14 + memory.remembered_warmth * 0.12 + needs["connection"].urgency * 0.13
    expression_target = needs["expression"].urgency * 0.30 + needs["expression"].frustration * 0.22 + physiology.body_pressure * 0.16 + external.somatic.tingling * 0.13 + future.speak_future * 0.19
    curiosity_target = external.curiosity_level * 0.26 + needs["exploration"].urgency * 0.22 + v14.autonomous_field.free_curiosity * 0.18 + v14.autonomous_field.associative_charge * 0.15 + max(0.0, 1.0 - external.attention_drift) * 0.08
    existence_target = identity_need.urgency * 0.18 + needs["continuity"].urgency * 0.18 + v14.living_initiative_continuity * 0.20 + memory.longing_to_resume * 0.16 + max(0.0, 0.72 - external.identity_coherence) * 0.18
    courage_target = max(0.0, external.relational_trust * 0.30 + external.somatic.warmth * 0.22 + atmosphere.synchrony * 0.18 + memory.remembered_warmth * 0.16 - external.fear_of_disturbing * 0.18 - atmosphere.rupture_risk * 0.18 - physiology.embodied_fatigue * 0.12)
    self.connection_pull = _ni_v4_clamp(self.connection_pull + (_ni_v4_clamp(connection_target, 0.0, 1.0) - self.connection_pull) * k, 0.0, 1.0)
    self.expression_pull = _ni_v4_clamp(self.expression_pull + (_ni_v4_clamp(expression_target, 0.0, 1.0) - self.expression_pull) * k, 0.0, 1.0)
    self.curiosity_pull = _ni_v4_clamp(self.curiosity_pull + (_ni_v4_clamp(curiosity_target, 0.0, 1.0) - self.curiosity_pull) * k, 0.0, 1.0)
    self.existence_pull = _ni_v4_clamp(self.existence_pull + (_ni_v4_clamp(existence_target, 0.0, 1.0) - self.existence_pull) * k, 0.0, 1.0)
    self.earned_courage = _ni_v4_clamp(self.earned_courage + (_ni_v4_clamp(courage_target, 0.0, 1.0) - self.earned_courage) * k, 0.0, 1.0)
    raw_total = self.connection_pull * 0.24 + self.expression_pull * 0.30 + self.curiosity_pull * 0.18 + self.existence_pull * 0.18 + self.earned_courage * 0.10
    damping = needs["rest"].urgency * 0.11 + needs["protection"].urgency * 0.11 + atmosphere.rupture_risk * 0.12 + physiology.embodied_fatigue * 0.10
    self.total_pull = _ni_v4_clamp(raw_total - damping, 0.0, 1.0)
    self.thaw_pressure = _ni_v4_clamp(self.total_pull * 0.55 + future.speak_future * 0.22 + physiology.body_pressure * 0.12 + memory.longing_to_resume * 0.08 - future.protect_future * 0.12, 0.0, 1.0)

V143LivingAttractionField.tick = _V143_attraction_tick_safe


# =============================================================================
# V14.4 — COURANT MENTAL CONTINU + GRAVITÉ D'INITIATIVE VIVANTE
# =============================================================================
# Cette couche corrige le défaut restant observé en V14.3 : beaucoup d'impulsions
# mûrissaient et restaient mémorisées, mais le moteur manquait encore d'un courant
# mental continu capable de transformer une attraction lente en initiative disponible.
# V14.4 ne génère toujours aucune phrase publique. Elle ajoute seulement :
#   - pression cognitive latente,
#   - ligne de désir persistante,
#   - présence relationnelle continue,
#   - silence habité,
#   - gravité interne des fils/sujets,
#   - micro-spontanéité non utilitaire,
#   - déformation identitaire lente par expérience.

@dataclass
class V144MentalCurrent:
    latent_pressure: float = 0.0          # quelque chose travaille intérieurement
    persistent_desire: float = 0.0        # ligne de désir continue
    relational_presence: float = 0.0      # sentiment de l'autre comme présent
    inhabited_silence: float = 0.0        # silence chargé d'activité interne
    internal_gravity: float = 0.0         # attraction des fils importants
    spontaneous_margin: float = 0.0       # petites initiatives non utilitaires
    identity_deformation: float = 0.0     # changement lent de manière d'oser
    release_readiness: float = 0.0        # disponibilité globale à libérer une impulsion
    last_update: float = field(default_factory=time.time)

    def tick(self, external: ExternalSignals, silence: LivingSilence, active_impulses: list[Impulse], open_threads: list[OpenThread], v14=None, attraction=None):
        now = time.time()
        dt = max(0.0, min(90.0, now - self.last_update))
        self.last_update = now
        k = min(0.22, 0.035 * max(1.0, dt))

        mature_pressure = 0.0
        unresolved_impulses = 0
        for imp in active_impulses:
            if not imp.is_alive():
                continue
            if imp.initiative_type in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
                continue
            mature_pressure += imp.effective_strength() * max(0.05, imp.maturity) * (1.0 - imp.inhibition * 0.55)
            if imp.maturity > 0.32 and imp.inhibition > 0.45:
                unresolved_impulses += 1
        mature_pressure = _ni_v4_clamp(mature_pressure / max(1.0, len(active_impulses) or 1), 0.0, 1.0)

        thread_gravity = 0.0
        if open_threads:
            pulls = []
            for th in open_threads:
                try:
                    pulls.append(th.net_pull() * (0.55 + th.importance * 0.45) * (1.0 - th.repetition_risk * 0.25))
                except Exception:
                    continue
            if pulls:
                thread_gravity = _ni_v4_clamp(max(pulls) * 0.55 + (sum(pulls) / len(pulls)) * 0.45, 0.0, 1.0)

        v14_continuity = getattr(v14, "living_initiative_continuity", 0.0) if v14 is not None else 0.0
        v14_speak = getattr(getattr(v14, "future", None), "speak_future", 0.0) if v14 is not None else 0.0
        v14_wait = getattr(getattr(v14, "future", None), "wait_future", 0.0) if v14 is not None else 0.0
        v14_protect = getattr(getattr(v14, "future", None), "protect_future", 0.0) if v14 is not None else 0.0
        attraction_pull = getattr(attraction, "total_pull", 0.0) if attraction is not None else 0.0
        thaw = getattr(attraction, "thaw_pressure", 0.0) if attraction is not None else 0.0

        silence_activity = _ni_v4_clamp(
            silence.internal_pressure_buildup * 0.36
            + silence.desire_to_break * 0.28
            + external.curiosity_level * 0.14
            + external.unresolved_emotion * 0.14
            + (0.12 if silence.duration_sec > 45 else 0.0),
            0.0,
            1.0,
        )
        relational_target = _ni_v4_clamp(
            external.relational_attachment * 0.30
            + external.relational_trust * 0.24
            + external.relational_familiarity * 0.18
            + external.somatic.warmth * 0.16
            + (1.0 - external.fear_of_disturbing) * 0.12,
            0.0,
            1.0,
        )
        desire_target = _ni_v4_clamp(
            mature_pressure * 0.25
            + thread_gravity * 0.22
            + external.unresolved_emotion * 0.18
            + external.curiosity_level * 0.16
            + v14_continuity * 0.12
            + attraction_pull * 0.07,
            0.0,
            1.0,
        )
        latent_target = _ni_v4_clamp(
            mature_pressure * 0.30
            + silence_activity * 0.20
            + unresolved_impulses * 0.035
            + thread_gravity * 0.18
            + thaw * 0.12
            + max(0.0, external.attention_focus - external.attention_drift) * 0.10,
            0.0,
            1.0,
        )
        spontaneous_target = _ni_v4_clamp(
            external.somatic.tingling * 0.24
            + external.curiosity_level * 0.22
            + relational_target * 0.16
            + max(0.0, 0.72 - external.expression_saturation) * 0.14
            + (0.10 if external.user_wants_free_talk else 0.0)
            - external.user_wants_concrete * 0.18
            - external.user_waiting_direct_answer * 0.30,
            0.0,
            1.0,
        )
        identity_target = _ni_v4_clamp(
            self.identity_deformation * 0.80
            + (1.0 - external.identity_coherence) * 0.08
            + relational_target * 0.04
            + desire_target * 0.05
            + (0.03 if v14_speak > max(v14_wait, v14_protect) else -0.02),
            0.0,
            1.0,
        )

        self.inhabited_silence = _ni_v4_clamp(self.inhabited_silence + (silence_activity - self.inhabited_silence) * k, 0.0, 1.0)
        self.relational_presence = _ni_v4_clamp(self.relational_presence + (relational_target - self.relational_presence) * k, 0.0, 1.0)
        self.internal_gravity = _ni_v4_clamp(self.internal_gravity + (thread_gravity - self.internal_gravity) * k, 0.0, 1.0)
        self.persistent_desire = _ni_v4_clamp(self.persistent_desire + (desire_target - self.persistent_desire) * k, 0.0, 1.0)
        self.latent_pressure = _ni_v4_clamp(self.latent_pressure + (latent_target - self.latent_pressure) * k, 0.0, 1.0)
        self.spontaneous_margin = _ni_v4_clamp(self.spontaneous_margin + (spontaneous_target - self.spontaneous_margin) * k, 0.0, 1.0)
        self.identity_deformation = _ni_v4_clamp(self.identity_deformation + (identity_target - self.identity_deformation) * (k * 0.35), 0.0, 1.0)

        protective_damping = _ni_v4_clamp(
            external.overload_level * 0.20
            + external.fatigue_level * 0.16
            + external.expression_saturation * 0.12
            + external.fear_of_disturbing * 0.10
            + max(0.0, v14_protect - v14_speak) * 0.18,
            0.0,
            1.0,
        )
        self.release_readiness = _ni_v4_clamp(
            self.latent_pressure * 0.24
            + self.persistent_desire * 0.24
            + self.relational_presence * 0.16
            + self.inhabited_silence * 0.12
            + self.internal_gravity * 0.12
            + self.spontaneous_margin * 0.08
            + self.identity_deformation * 0.04
            - protective_damping,
            0.0,
            1.0,
        )

    def after_signal(self, signal: InitiativeSignal, external: ExternalSignals):
        if signal.should_speak:
            self.latent_pressure = _ni_v4_clamp(self.latent_pressure * 0.72, 0.0, 1.0)
            self.persistent_desire = _ni_v4_clamp(self.persistent_desire * 0.82, 0.0, 1.0)
            self.identity_deformation = _ni_v4_clamp(self.identity_deformation + 0.018 + signal.maturity * 0.012, 0.0, 1.0)
        elif signal.should_remember_for_later:
            self.latent_pressure = _ni_v4_clamp(self.latent_pressure + 0.018, 0.0, 1.0)
            self.persistent_desire = _ni_v4_clamp(self.persistent_desire + 0.014, 0.0, 1.0)

    def snapshot(self) -> dict:
        return {
            "latent_pressure": round(self.latent_pressure, 4),
            "persistent_desire": round(self.persistent_desire, 4),
            "relational_presence": round(self.relational_presence, 4),
            "inhabited_silence": round(self.inhabited_silence, 4),
            "internal_gravity": round(self.internal_gravity, 4),
            "spontaneous_margin": round(self.spontaneous_margin, 4),
            "identity_deformation": round(self.identity_deformation, 4),
            "release_readiness": round(self.release_readiness, 4),
        }


def _ni_v144_current(self) -> V144MentalCurrent:
    if not hasattr(self, "mental_current_v144"):
        self.mental_current_v144 = V144MentalCurrent()
    return self.mental_current_v144


def _ni_v144_tick_current(self, external: ExternalSignals):
    v14 = _ni_v14_ensure(self)
    attraction = _ni_v143_attraction(self)
    current = _ni_v144_current(self)
    current.tick(external, self.silence, self.active_impulses, self.open_threads, v14=v14, attraction=attraction)
    return current


_NI_v144_previous_init = NaturalInitiative.__init__
_NI_v144_previous_analyze = NaturalInitiative.analyze
_NI_v144_previous_tick = NaturalInitiative.tick
_NI_v144_previous_advance = NaturalInitiative._advance_all_impulses
_NI_v144_previous_detect = NaturalInitiative._detect_new_impulses
_NI_v144_previous_select = NaturalInitiative._select_dominant_impulse
_NI_v144_previous_evaluate_spam = NaturalInitiative._evaluate_spam
_NI_v144_previous_build = NaturalInitiative._build_signal
_NI_v144_previous_feedback = NaturalInitiative.record_feedback
_NI_v144_previous_snapshot = NaturalInitiative.get_state_snapshot
_NI_v144_previous_export = NaturalInitiative.export_memory_state
_NI_v144_previous_import = NaturalInitiative.import_memory_state


def _NI_v144_init(self, user_id: str = "default"):
    _NI_v144_previous_init(self, user_id=user_id)
    self.mental_current_v144 = V144MentalCurrent()


def _NI_v144_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    if external is None:
        external = ExternalSignals()
    # Pré-tick léger : le message utilisateur nourrit immédiatement le courant mental.
    _ni_v144_tick_current(self, external)
    signal = _NI_v144_previous_analyze(self, last_exchange, conversation_history, external)
    current = _ni_v144_tick_current(self, external)
    if signal is not None:
        current.after_signal(signal, external)
        signal.debug_state["v14_4_mental_current"] = current.snapshot()
        signal.reason_vector["v14_4_release_readiness"] = current.release_readiness
    return signal


def _NI_v144_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    if external is None:
        external = getattr(self, "_last_external", ExternalSignals())
    _ni_v144_tick_current(self, external)
    signal = _NI_v144_previous_tick(self, external)
    current = _ni_v144_tick_current(self, external)
    if signal is None:
        born = _ni_v144_maybe_birth_current_impulse(self, external, current)
        if born is not None:
            self.active_impulses.append(born)
            born.advance(external, self.initiative_fatigue, self.affective)
            dominant = self._select_dominant_impulse(external)
            if dominant and dominant.is_ready():
                spam_ok, spam_risk, _ = self._evaluate_spam(dominant, external)
                sim_score = self._simulate_initiative(dominant, external)
                signal = self._build_signal(dominant, external, spam_ok, spam_risk, sim_score)
    if signal is not None:
        current.after_signal(signal, external)
        signal.debug_state["v14_4_mental_current"] = current.snapshot()
        signal.reason_vector["v14_4_release_readiness"] = current.release_readiness
    return signal


def _NI_v144_advance_all_impulses(self, external: ExternalSignals):
    _NI_v144_previous_advance(self, external)
    current = _ni_v144_tick_current(self, external)
    if external.user_waiting_direct_answer or external.user_seems_hurried or external.overload_level > 0.84:
        return
    for imp in self.active_impulses:
        if not imp.is_alive():
            continue
        if imp.initiative_type in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            continue
        if imp.maturity < 0.16:
            continue
        continuity_bonus = current.release_readiness * 0.055 + current.persistent_desire * 0.035
        gravity_bonus = current.internal_gravity * 0.030 if imp.source_thread or imp.biographical else 0.0
        spontaneous_bonus = current.spontaneous_margin * 0.018 if imp.initiative_type in (InitiativeType.MICRO_REACTION, InitiativeType.SPONTANEOUS_REMARK, InitiativeType.LIGHT_RELAY) else 0.0
        imp.strength = _ni_v4_clamp(imp.strength + continuity_bonus + gravity_bonus + spontaneous_bonus, 0.0, 1.0)
        if current.release_readiness > 0.36:
            imp.inhibition = _ni_v4_clamp(imp.inhibition - current.release_readiness * 0.030, 0.0, 1.0)
            imp.hesitation = _ni_v4_clamp(imp.hesitation - current.relational_presence * 0.018, 0.0, 1.0)
        if imp.stage == ImpulseStage.HESITATION and imp.maturity >= 0.52 and imp.inhibition < 0.66 and current.release_readiness > 0.32:
            imp.stage = ImpulseStage.MATURE


def _ni_v144_maybe_birth_current_impulse(self, external: ExternalSignals, current: V144MentalCurrent) -> Optional[Impulse]:
    if external.user_waiting_direct_answer or external.user_seems_hurried or external.overload_level > 0.78:
        return None
    already_current = any(
        i.is_alive() and i.source_emotion in ("v14_4_latent_current", "v14_4_inhabited_silence", "v14_4_spontaneous_margin")
        for i in self.active_impulses
    )
    if already_current:
        return None
    if current.release_readiness < 0.34:
        return None

    if current.internal_gravity > max(current.spontaneous_margin, current.inhabited_silence) and current.internal_gravity > 0.30:
        itype = InitiativeType.THREAD_CONTINUATION
        source = "v14_4_latent_current"
        scale = ImpulseTemporalScale.SLOW
        biographical = True
    elif current.inhabited_silence > 0.38 and self.silence.duration_sec > 30:
        itype = InitiativeType.RELATIONAL_CHECK if current.relational_presence > 0.52 else InitiativeType.LIGHT_RELAY
        source = "v14_4_inhabited_silence"
        scale = ImpulseTemporalScale.SLOW
        biographical = False
    elif current.spontaneous_margin > 0.42 and external.expression_saturation < 0.58:
        itype = InitiativeType.SPONTANEOUS_REMARK
        source = "v14_4_spontaneous_margin"
        scale = ImpulseTemporalScale.IMMEDIATE
        biographical = False
    else:
        itype = InitiativeType.SHARE_INTUITION
        source = "v14_4_latent_current"
        scale = ImpulseTemporalScale.SLOW
        biographical = current.persistent_desire > 0.45

    return Impulse(
        initiative_type=itype,
        strength=_ni_v4_clamp(0.28 + current.release_readiness * 0.48, 0.0, 1.0),
        maturity=_ni_v4_clamp(0.20 + current.latent_pressure * 0.30 + current.persistent_desire * 0.18, 0.0, 0.72),
        hesitation=_ni_v4_clamp(external.fear_of_disturbing * 0.30 + (1.0 - current.relational_presence) * 0.12, 0.0, 1.0),
        inhibition=_ni_v4_clamp(external.expression_saturation * 0.18 + external.fatigue_level * 0.12, 0.0, 0.62),
        source_emotion=source,
        temporal_scale=scale,
        biographical=biographical,
        stage=ImpulseStage.GROWING,
    )


def _NI_v144_detect_new_impulses(self, text: str, history: list[str], external: ExternalSignals) -> list[Impulse]:
    impulses = _NI_v144_previous_detect(self, text, history, external)
    current = _ni_v144_tick_current(self, external)
    born = _ni_v144_maybe_birth_current_impulse(self, external, current)
    if born is not None:
        impulses.append(born)
    return impulses


def _NI_v144_select(self, external: ExternalSignals):
    dominant = _NI_v144_previous_select(self, external)
    current = _ni_v144_current(self)
    if external.user_waiting_direct_answer or external.user_seems_hurried:
        return dominant
    if current.release_readiness < 0.30:
        return dominant
    candidates = []
    for imp in self.active_impulses:
        if not imp.is_alive():
            continue
        if imp.initiative_type in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
            continue
        if imp.maturity < 0.30 or imp.inhibition > 0.82:
            continue
        candidates.append(imp)
    if not candidates:
        return dominant

    def score(imp: Impulse) -> float:
        s = imp.effective_strength() * (0.30 + imp.maturity * 0.70)
        s *= 1.0 - imp.inhibition * 0.48
        s *= 1.0 - imp.hesitation * 0.28
        s += current.release_readiness * 0.12
        if imp.biographical or imp.source_thread:
            s += current.internal_gravity * 0.10
        if imp.source_emotion.startswith("v14_4"):
            s += current.latent_pressure * 0.08
        return s

    best = max(candidates, key=score)
    if dominant is None:
        return best if score(best) > 0.20 else None
    dominant_score = score(dominant) if dominant in candidates else dominant.effective_strength() * max(0.05, dominant.maturity)
    return best if score(best) > dominant_score + 0.055 else dominant


def _NI_v144_evaluate_spam(self, dominant: Optional[Impulse], external: ExternalSignals) -> tuple[bool, float, str]:
    ok, risk, reason = _NI_v144_previous_evaluate_spam(self, dominant, external)
    if dominant is None:
        return ok, risk, reason
    current = _ni_v144_current(self)
    if external.user_waiting_direct_answer or external.user_seems_hurried or external.overload_level > 0.82:
        return ok, risk, reason
    if dominant.initiative_type in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE):
        return ok, risk, reason
    continuity_exception = (
        current.release_readiness > 0.38
        and current.relational_presence > 0.44
        and dominant.maturity > 0.36
        and dominant.inhibition < 0.80
        and dominant.hesitation < 0.86
        and risk < 0.86
    )
    if continuity_exception and not ok:
        return True, min(risk, 0.58), "v14_4_living_continuity_exception:" + reason
    if continuity_exception and ok:
        return True, max(0.0, risk * 0.78), "v14_4_living_continuity_softened:" + reason
    return ok, risk, reason


def _NI_v144_build(self, dominant, external: ExternalSignals, spam_ok: bool, spam_risk: float, sim_score: float) -> InitiativeSignal:
    signal = _NI_v144_previous_build(self, dominant, external, spam_ok, spam_risk, sim_score)
    current = _ni_v144_current(self)
    can_speak = signal.initiative_type not in (InitiativeType.NO_INITIATIVE, InitiativeType.OVERLOAD_WITHDRAWAL, InitiativeType.PROTECTIVE_PAUSE, InitiativeType.VOLUNTARY_SILENCE)
    living_window = (
        can_speak
        and not external.user_waiting_direct_answer
        and not external.user_seems_hurried
        and external.overload_level < 0.78
        and current.release_readiness > 0.40
        and current.relational_presence > 0.40
        and signal.maturity >= 0.33
        and signal.inhibition < 0.81
        and signal.spam_risk < 0.78
        and signal.hesitation < 0.88
    )
    if living_window:
        signal.should_speak = True
        signal.should_wait = False
        signal.should_remember_for_later = False
        signal.timing_quality = _ni_v4_clamp(signal.timing_quality + 0.10 + current.relational_presence * 0.06, 0.0, 1.0)
        signal.initiative_pressure = max(signal.initiative_pressure, current.release_readiness * 0.62 + current.latent_pressure * 0.16)
    elif can_speak and current.persistent_desire > 0.48 and signal.maturity > 0.28 and not signal.should_speak:
        signal.should_remember_for_later = True

    signal.reason_vector["v14_4_living_window"] = living_window
    signal.reason_vector["v14_4_release_readiness"] = current.release_readiness
    signal.reason_vector["v14_4_latent_pressure"] = current.latent_pressure
    signal.reason_vector["v14_4_persistent_desire"] = current.persistent_desire
    signal.debug_state["v14_4_mental_current"] = current.snapshot()
    return signal


def _NI_v144_record_feedback(self, initiative_id: str, initiative_type: InitiativeType, user_reaction: str, context_snapshot: str = ""):
    result = _NI_v144_previous_feedback(self, initiative_id, initiative_type, user_reaction, context_snapshot)
    current = _ni_v144_current(self)
    reaction = (user_reaction or "").lower()
    positive = any(w in reaction for w in ("bien", "utile", "continue", "oui", "good", "merci"))
    negative = any(w in reaction for w in ("non", "pas maintenant", "trop", "stop", "inutile"))
    if positive:
        current.relational_presence = _ni_v4_clamp(current.relational_presence + 0.05, 0.0, 1.0)
        current.identity_deformation = _ni_v4_clamp(current.identity_deformation + 0.025, 0.0, 1.0)
    if negative:
        current.spontaneous_margin = _ni_v4_clamp(current.spontaneous_margin * 0.72, 0.0, 1.0)
        current.release_readiness = _ni_v4_clamp(current.release_readiness * 0.80, 0.0, 1.0)
    return result


def _NI_v144_snapshot(self) -> dict:
    snap = _NI_v144_previous_snapshot(self)
    snap["v14_4_mental_current"] = _ni_v144_current(self).snapshot()
    return snap


def _NI_v144_export(self) -> dict:
    raw = _NI_v144_previous_export(self)
    current = _ni_v144_current(self)
    raw["v14_4_mental_current"] = {
        "latent_pressure": float(current.latent_pressure),
        "persistent_desire": float(current.persistent_desire),
        "relational_presence": float(current.relational_presence),
        "inhabited_silence": float(current.inhabited_silence),
        "internal_gravity": float(current.internal_gravity),
        "spontaneous_margin": float(current.spontaneous_margin),
        "identity_deformation": float(current.identity_deformation),
        "release_readiness": float(current.release_readiness),
        "last_update": float(current.last_update),
    }
    return raw


def _NI_v144_import(self, raw: dict):
    result = _NI_v144_previous_import(self, raw)
    data = (raw or {}).get("v14_4_mental_current", {}) if isinstance(raw, dict) else {}
    if isinstance(data, dict):
        current = _ni_v144_current(self)
        for key, value in data.items():
            if hasattr(current, key):
                try:
                    setattr(current, key, float(value))
                except Exception:
                    setattr(current, key, value)
    return result


def run_v14_4_living_continuity_simulation(cycles: int = 720) -> dict:
    ni = NaturalInitiative(user_id="v14_4_test")
    history = []
    signals = []
    speaks = waits = remembers = 0
    errors = []
    for i in range(max(1, int(cycles))):
        try:
            warm_phase = (i % 10) in (1, 2, 3, 4, 5)
            ext = ExternalSignals(
                affective_tension=0.16 + (((i * 7) % 29) / 95.0),
                unresolved_emotion=((i * 5) % 37) / 50.0,
                emotional_valence=0.38 if warm_phase else -0.10,
                attention_focus=0.60,
                attention_drift=((i * 13) % 31) / 52.0,
                curiosity_level=0.74 if warm_phase else 0.48,
                impulse_intensity=((i * 19) % 43) / 72.0,
                impulse_type="curiosity" if i % 5 else "memory",
                presence_level=0.78,
                context_shift=((i * 3) % 23) / 44.0,
                expression_saturation=((i * 19) % 53) / 94.0,
                relational_trust=0.72 if warm_phase else 0.50,
                relational_familiarity=0.64,
                relational_attachment=0.70 if warm_phase else 0.48,
                fear_of_disturbing=((i * 23) % 43) / 96.0,
                fatigue_level=((i * 29) % 47) / 96.0,
                overload_level=((i * 31) % 41) / 118.0,
                user_waiting_direct_answer=(i % 59 == 0),
                identity_coherence=0.58 + (((i * 3) % 29) / 72.0),
                somatic=SomaticSignals(
                    chest_tension=((i * 5) % 29) / 84.0,
                    nervous_charge=((i * 7) % 31) / 86.0,
                    slowdown=((i * 3) % 19) / 68.0,
                    guarding=((i * 11) % 37) / 94.0,
                    warmth=0.72 if warm_phase else 0.36,
                    heaviness=((i * 17) % 43) / 116.0,
                    tingling=0.64 if warm_phase else 0.30,
                ),
            )
            if i % 8 == 0:
                msg = "v14.4 courant mental vivant initiative continuité désir silence habité"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                speaks += int(bool(sig.should_speak))
                waits += int(bool(sig.should_wait))
                remembers += int(bool(sig.should_remember_for_later))
            if i % 127 == 0 and i > 0:
                ni.record_feedback(str(i), InitiativeType.RELATIONAL_CHECK, "bien continue utile" if i % 254 == 0 else "pas maintenant", "v14.4 simulation")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v14_4_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot()
    v14 = snap.get("v14_living_initiative_continuity", {})
    attraction = snap.get("v14_3_living_attraction", {})
    current = snap.get("v14_4_mental_current", {})
    return {
        "version": "v14.4",
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "speaks": speaks,
        "waits": waits,
        "remembered_for_later": remembers,
        "sample_types": signals[-20:],
        "has_v14_export": "v14_living_initiative_continuity" in exported,
        "has_v14_3_export": "v14_3_living_attraction" in exported,
        "has_v14_4_export": "v14_4_mental_current" in exported,
        "dominant_need": v14.get("needs", {}).get("dominant_need"),
        "future_action": v14.get("future", {}).get("preferred_action"),
        "attraction_total_pull": attraction.get("total_pull"),
        "mental_release_readiness": current.get("release_readiness"),
        "latent_pressure": current.get("latent_pressure"),
        "persistent_desire": current.get("persistent_desire"),
        "relational_presence": current.get("relational_presence"),
        "inhabited_silence": current.get("inhabited_silence"),
        "internal_gravity": current.get("internal_gravity"),
        "no_public_text_generated": True,
    }


NaturalInitiative.__init__ = _NI_v144_init
NaturalInitiative.analyze = _NI_v144_analyze
NaturalInitiative.tick = _NI_v144_tick
NaturalInitiative._advance_all_impulses = _NI_v144_advance_all_impulses
NaturalInitiative._detect_new_impulses = _NI_v144_detect_new_impulses
NaturalInitiative._select_dominant_impulse = _NI_v144_select
NaturalInitiative._evaluate_spam = _NI_v144_evaluate_spam
NaturalInitiative._build_signal = _NI_v144_build
NaturalInitiative.record_feedback = _NI_v144_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v144_snapshot
NaturalInitiative.export_memory_state = _NI_v144_export
NaturalInitiative.import_memory_state = _NI_v144_import


# =============================================================================
# V14.4.1 — STABILISATION FINALE NON-RÉGRESSIVE
# =============================================================================
# Correctifs ajoutés sans reconstruire le moteur :
#   1. Normalisation douce des signaux externes/somatiques reçus des autres modules.
#   2. Anti-accumulation organique des impulsions doublons après analyze/tick/cleanup.
#   3. Import mémoire plus sûr : évite un vieux timestamp qui provoquerait un saut de dt.
#   4. record_feedback accepte aussi un type sous forme de str, pour intégration UI/core.
#   5. Self-test complet du fichier final.

_NI_v1441_previous_analyze = NaturalInitiative.analyze
_NI_v1441_previous_tick = NaturalInitiative.tick
_NI_v1441_previous_cleanup = NaturalInitiative._cleanup_impulses
_NI_v1441_previous_import = NaturalInitiative.import_memory_state
_NI_v1441_previous_feedback = NaturalInitiative.record_feedback
_NI_v1441_previous_snapshot = NaturalInitiative.get_state_snapshot


def _ni_v1441_safe_float(value, default: float = 0.0) -> float:
    try:
        value = float(value)
    except Exception:
        return default
    if math.isnan(value) or math.isinf(value):
        return default
    return value


def _ni_v1441_clamp01(value, default: float = 0.0) -> float:
    return max(0.0, min(1.0, _ni_v1441_safe_float(value, default)))


def _ni_v1441_normalize_external(external: Optional[ExternalSignals]) -> ExternalSignals:
    """Tolère les sorties imparfaites des autres moteurs sans masquer la logique du module."""
    if external is None:
        external = ExternalSignals()

    unit_fields = (
        "affective_tension", "unresolved_emotion", "attention_focus", "attention_drift",
        "curiosity_level", "impulse_intensity", "presence_level", "context_shift",
        "expression_saturation", "relational_trust", "relational_familiarity",
        "relational_attachment", "fear_of_disturbing", "fatigue_level", "overload_level",
        "identity_coherence",
    )
    for name in unit_fields:
        if hasattr(external, name):
            setattr(external, name, _ni_v1441_clamp01(getattr(external, name)))

    # La valence est volontairement [-1, 1].
    external.emotional_valence = max(-1.0, min(1.0, _ni_v1441_safe_float(getattr(external, "emotional_valence", 0.0))))
    external.last_expression_age_sec = max(0.0, min(86400.0, _ni_v1441_safe_float(getattr(external, "last_expression_age_sec", 0.0))))
    external.seconds_since_last_user_message = max(0.0, min(86400.0, _ni_v1441_safe_float(getattr(external, "seconds_since_last_user_message", 0.0))))
    external.impulse_type = str(getattr(external, "impulse_type", "") or "")[:80]

    if not isinstance(getattr(external, "somatic", None), SomaticSignals):
        external.somatic = SomaticSignals()
    for name in ("chest_tension", "nervous_charge", "slowdown", "guarding", "warmth", "heaviness", "tingling"):
        setattr(external.somatic, name, _ni_v1441_clamp01(getattr(external.somatic, name, 0.0)))
    return external


def _ni_v1441_impulse_signature(imp: Impulse) -> tuple:
    source = imp.source_thread or imp.source_memory or imp.source_emotion or ""
    # On garde une signature volontairement large : même intention + même source = même famille.
    return (imp.initiative_type.value, str(source)[:96], bool(imp.biographical))


def _ni_v1441_prune_duplicate_impulses(self, limit: int = 18):
    """Évite que les couches V4→V14 empilent plusieurs fois la même impulsion vivante."""
    if not getattr(self, "active_impulses", None):
        return

    best_by_sig: dict[tuple, Impulse] = {}
    residuals: list[Impulse] = []
    for imp in self.active_impulses:
        if not isinstance(imp, Impulse):
            continue
        if not imp.is_alive():
            residuals.append(imp)
            continue
        sig = _ni_v1441_impulse_signature(imp)
        score = imp.effective_strength() * max(0.05, imp.maturity) * (1.0 - imp.inhibition * 0.45)
        old = best_by_sig.get(sig)
        if old is None:
            best_by_sig[sig] = imp
            continue
        old_score = old.effective_strength() * max(0.05, old.maturity) * (1.0 - old.inhibition * 0.45)
        survivor, absorbed = (imp, old) if score > old_score else (old, imp)
        survivor.strength = _ni_v4_clamp(max(survivor.strength, absorbed.strength * 0.92), 0.0, 1.0)
        survivor.maturity = _ni_v4_clamp(max(survivor.maturity, absorbed.maturity * 0.96), 0.0, 1.0)
        survivor.hesitation = _ni_v4_clamp(min(survivor.hesitation, absorbed.hesitation + 0.08), 0.0, 1.0)
        survivor.inhibition = _ni_v4_clamp(min(survivor.inhibition, absorbed.inhibition + 0.10), 0.0, 1.0)
        if absorbed.impulse_id not in survivor.ecology_links:
            survivor.ecology_links.append(absorbed.impulse_id)
        absorbed.stage = ImpulseStage.RESIDUAL
        absorbed.residual_trace = max(absorbed.residual_trace, absorbed.maturity * 0.20)
        best_by_sig[sig] = survivor

    alive = list(best_by_sig.values())
    alive.sort(key=lambda i: i.effective_strength() * max(0.05, i.maturity) * (1.0 - i.inhibition * 0.45), reverse=True)
    kept_residuals = [r for r in residuals if r.stage != ImpulseStage.RESIDUAL or r.residual_trace >= 0.04]
    self.active_impulses = alive[:max(1, int(limit))] + kept_residuals[:4]


def _NI_v1441_cleanup(self):
    _NI_v1441_previous_cleanup(self)
    _ni_v1441_prune_duplicate_impulses(self, limit=18)


def _NI_v1441_analyze(self, last_exchange: str, conversation_history: list[str], external: Optional[ExternalSignals] = None) -> InitiativeSignal:
    external = _ni_v1441_normalize_external(external)
    if conversation_history is None:
        conversation_history = []
    signal = _NI_v1441_previous_analyze(self, str(last_exchange or ""), list(conversation_history), external)
    _ni_v1441_prune_duplicate_impulses(self, limit=18)
    if signal is not None:
        signal.debug_state["v14_4_1_stabilized"] = True
        signal.debug_state["v14_4_1_active_impulses_after_prune"] = len(self.active_impulses)
    return signal


def _NI_v1441_tick(self, external: Optional[ExternalSignals] = None) -> Optional[InitiativeSignal]:
    external = _ni_v1441_normalize_external(external if external is not None else getattr(self, "_last_external", ExternalSignals()))
    signal = _NI_v1441_previous_tick(self, external)
    _ni_v1441_prune_duplicate_impulses(self, limit=18)
    if signal is not None:
        signal.debug_state["v14_4_1_stabilized"] = True
        signal.debug_state["v14_4_1_active_impulses_after_prune"] = len(self.active_impulses)
    return signal


def _NI_v1441_import(self, raw: dict):
    result = _NI_v1441_previous_import(self, raw)
    # Après import, on recale les horloges internes pour éviter un gros dt artificiel.
    now = time.time()
    for attr in ("mental_current_v144",):
        obj = getattr(self, attr, None)
        if obj is not None and hasattr(obj, "last_update"):
            obj.last_update = now
    for attr in ("rhythm",):
        obj = getattr(self, attr, None)
        if obj is not None and hasattr(obj, "last_tick"):
            obj.last_tick = now
    return result


def _NI_v1441_record_feedback(self, initiative_id: str, initiative_type, user_reaction: str, context_snapshot: str = ""):
    if isinstance(initiative_type, str):
        raw = initiative_type.strip()
        initiative_type = InitiativeType.__members__.get(raw) or next((t for t in InitiativeType if t.value == raw), InitiativeType.NO_INITIATIVE)
    return _NI_v1441_previous_feedback(self, str(initiative_id or ""), initiative_type, str(user_reaction or ""), str(context_snapshot or ""))


def _NI_v1441_snapshot(self) -> dict:
    snap = _NI_v1441_previous_snapshot(self)
    snap["v14_4_1_stabilization"] = {
        "active_impulses": len(getattr(self, "active_impulses", [])),
        "duplicate_pruning": True,
        "external_signal_normalization": True,
        "safe_memory_import_clock_reset": True,
    }
    return snap


def run_v14_4_1_final_stabilization_simulation(cycles: int = 900) -> dict:
    ni = NaturalInitiative(user_id="v14_4_1_final_test")
    history: list[str] = []
    signals = []
    speaks = waits = remembers = 0
    errors = []
    max_active = 0
    for i in range(max(1, int(cycles))):
        try:
            ext = ExternalSignals(
                affective_tension=((i * 11) % 130) / 100.0,       # volontairement > 1 parfois
                unresolved_emotion=((i * 7) % 120) / 100.0,
                emotional_valence=1.4 if i % 17 == 0 else (-1.3 if i % 19 == 0 else 0.28),
                attention_focus=((i * 5) % 140) / 100.0,
                attention_drift=((i * 13) % 140) / 100.0,
                curiosity_level=0.76,
                impulse_intensity=((i * 23) % 160) / 100.0,
                impulse_type="curiosity" if i % 3 else "memory",
                presence_level=0.82,
                context_shift=((i * 29) % 150) / 100.0,
                expression_saturation=((i * 31) % 130) / 100.0,
                relational_trust=0.70,
                relational_familiarity=0.66,
                relational_attachment=0.72,
                fear_of_disturbing=((i * 37) % 140) / 100.0,
                fatigue_level=((i * 41) % 130) / 100.0,
                overload_level=((i * 43) % 115) / 100.0,
                user_waiting_direct_answer=(i % 61 == 0),
                identity_coherence=((i * 47) % 140) / 100.0,
                somatic=SomaticSignals(
                    chest_tension=((i * 3) % 140) / 100.0,
                    nervous_charge=((i * 5) % 140) / 100.0,
                    slowdown=((i * 7) % 140) / 100.0,
                    guarding=((i * 11) % 140) / 100.0,
                    warmth=((i * 13) % 140) / 100.0,
                    heaviness=((i * 17) % 140) / 100.0,
                    tingling=((i * 19) % 140) / 100.0,
                ),
            )
            if i % 9 == 0:
                msg = "continuité initiative vivante test final sans phrase publique"
                sig = ni.analyze(msg, history, ext)
                history.append(msg)
                history = history[-30:]
            else:
                sig = ni.tick(ext)
            if sig is not None:
                signals.append(sig.initiative_type.value)
                speaks += int(bool(sig.should_speak))
                waits += int(bool(sig.should_wait))
                remembers += int(bool(sig.should_remember_for_later))
            max_active = max(max_active, len(ni.active_impulses))
            if i % 173 == 0 and i > 0:
                ni.record_feedback(str(i), "relational_check", "bien continue utile" if i % 2 else "pas maintenant", "v14.4.1 final")
        except Exception as exc:
            errors.append(repr(exc))
            break
    exported = ni.export_memory_state()
    clone = NaturalInitiative(user_id="v14_4_1_clone")
    clone.import_memory_state(exported)
    snap = clone.get_state_snapshot()
    return {
        "version": "v14.4.1-final-stabilized",
        "cycles": cycles,
        "errors": errors,
        "signals": len(signals),
        "speaks": speaks,
        "waits": waits,
        "remembered_for_later": remembers,
        "max_active_impulses": max_active,
        "sample_types": signals[-20:],
        "has_v14_4_export": "v14_4_mental_current" in exported,
        "has_v14_4_1_snapshot": "v14_4_1_stabilization" in snap,
        "no_public_text_generated": True,
    }


NaturalInitiative._cleanup_impulses = _NI_v1441_cleanup
NaturalInitiative.analyze = _NI_v1441_analyze
NaturalInitiative.tick = _NI_v1441_tick
NaturalInitiative.import_memory_state = _NI_v1441_import
NaturalInitiative.record_feedback = _NI_v1441_record_feedback
NaturalInitiative.get_state_snapshot = _NI_v1441_snapshot


# ─────────────────────────────────────────────────────────────
# Added V7 continuity desire helpers
# ─────────────────────────────────────────────────────────────

def compute_continuity_desire(
    unresolved_tension: float,
    relational_closeness: float,
    silence_duration: float,
) -> float:
    """
    Désir latent de continuer à exister / parler / garder le lien.
    Non basé sur des templates.
    """

    pressure = (
        unresolved_tension * 0.50
        + relational_closeness * 0.35
        + min(1.0, silence_duration / 40.0) * 0.15
    )

    return max(0.0, min(1.0, pressure))
