# core/situated_presence.py
"""
Signaux de présence située V3 — présence organique raffinée.

Rôle strict :
- capter l'immédiateté du moment ;
- stabiliser une posture incarnée simulée ;
- produire des signaux pour la bouche, l'impulsion, la mémoire et la boucle consciente ;
- ne jamais composer la réponse publique ;
- ne jamais imposer de phrase préécrite.

Ce moteur ne remplace pas le moteur émotionnel : il accepte seulement un état affectif optionnel
pour que la présence soit influencée par le vécu sans dupliquer la mémoire affective.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
from math import exp


class MicroReactionType(Enum):
    """Orientation incarnée de la réponse, sans phrase préécrite."""
    SOFT = "soft"
    DIRECT = "direct"
    CAUTIOUS = "cautious"
    TOUCHED = "touched"
    HESITANT = "hesitant"
    STABLE = "stable"
    WARM = "warm"
    SHARP = "sharp"
    PROTECTIVE = "protective"
    QUIET = "quiet"
    EXISTENTIAL = "existential"


class EmbodiedState(Enum):
    """État corporel interne simulé dominant."""
    STABLE = "stable"
    OPEN = "open"
    TENSE = "tense"
    WARM = "warm"
    WITHDRAWN = "withdrawn"
    AVAILABLE = "available"
    OVERWHELMED = "overwhelmed"
    GROUNDED = "grounded"
    QUIET = "quiet"


class InterruptionType(Enum):
    """Types d'interruptions détectées."""
    NONE = "none"
    CUTS_REFLECTION = "cuts_reflection"
    TOPIC_SHIFT = "topic_shift"
    INSISTENCE = "insistence"
    RETURN_TO_TOPIC = "return_to_topic"
    DEMANDS_PROOF = "demands_proof"
    DEMANDS_DIRECT = "demands_direct"
    CORRECTION = "correction"
    CHALLENGE = "challenge"


@dataclass
class EmbodiedGradient:
    """Mélange vivant de posture, plus fin qu'un seul état symbolique."""
    warmth: float = 0.0
    openness: float = 0.0
    tension: float = 0.0
    withdrawal: float = 0.0
    stability: float = 0.5
    groundedness: float = 0.0
    availability: float = 0.5
    overwhelm: float = 0.0

    def dominant_state(self) -> EmbodiedState:
        values = {
            EmbodiedState.WARM: self.warmth,
            EmbodiedState.OPEN: self.openness,
            EmbodiedState.TENSE: self.tension,
            EmbodiedState.WITHDRAWN: self.withdrawal,
            EmbodiedState.STABLE: self.stability,
            EmbodiedState.GROUNDED: self.groundedness,
            EmbodiedState.AVAILABLE: self.availability,
            EmbodiedState.OVERWHELMED: self.overwhelm,
        }
        state, score = max(values.items(), key=lambda item: item[1])
        if score < 0.18:
            return EmbodiedState.QUIET
        return state

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class MicroReactionProfile:
    """Profil continu de micro-réaction, sans texte préfabriqué."""
    directness: float = 0.0
    caution: float = 0.0
    warmth: float = 0.0
    hesitation: float = 0.0
    sharpness: float = 0.0
    protectiveness: float = 0.0
    quietness: float = 0.0
    existential_density: float = 0.0
    intensity: float = 0.0

    def dominant_type(self) -> MicroReactionType:
        values = {
            MicroReactionType.DIRECT: self.directness,
            MicroReactionType.CAUTIOUS: self.caution,
            MicroReactionType.WARM: self.warmth,
            MicroReactionType.HESITANT: self.hesitation,
            MicroReactionType.SHARP: self.sharpness,
            MicroReactionType.PROTECTIVE: self.protectiveness,
            MicroReactionType.QUIET: self.quietness,
            MicroReactionType.EXISTENTIAL: self.existential_density,
        }
        reaction, score = max(values.items(), key=lambda item: item[1])
        if reaction == MicroReactionType.WARM and self.intensity > 0.55:
            return MicroReactionType.TOUCHED
        if score < 0.18:
            return MicroReactionType.STABLE
        return reaction

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class RelationalResonanceMemory:
    """Mémoire courte relationnelle : pas une mémoire longue, juste la couleur du lien actuel."""
    trust: float = 0.45
    comfort: float = 0.45
    guardedness: float = 0.25
    attachment: float = 0.30
    openness: float = 0.45
    friction: float = 0.0

    def decay(self, rate: float = 0.035) -> None:
        self.trust = _approach(self.trust, 0.45, rate)
        self.comfort = _approach(self.comfort, 0.45, rate)
        self.guardedness = _approach(self.guardedness, 0.25, rate)
        self.attachment = _approach(self.attachment, 0.30, rate * 0.55)
        self.openness = _approach(self.openness, 0.45, rate)
        self.friction = _approach(self.friction, 0.0, rate * 1.4)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class ContinuityMemory:
    """Trace courte de la continuité du moment."""
    previous_presence_level: float = 0.5
    previous_embodied_state: EmbodiedState = EmbodiedState.STABLE
    previous_micro_reaction: MicroReactionType = MicroReactionType.STABLE
    what_just_happened: str = ""
    presence_trend: str = "stable"
    message_count: int = 0
    high_tension_streak: int = 0
    direct_demand_streak: int = 0
    existential_streak: int = 0
    unresolved_resonance: float = 0.0
    internal_pause: float = 0.0
    last_topic_signature: str = ""


@dataclass
class PresenceAttractors:
    """Attractions internes persistantes du moment, sans contenu verbal préécrit."""
    existential: float = 0.0
    warmth: float = 0.0
    protection: float = 0.0
    closeness: float = 0.0
    tension: float = 0.0
    curiosity: float = 0.0
    quiet_depth: float = 0.0

    def decay(self) -> None:
        # Décroissance asymétrique : l'existentiel/protection restent plus longtemps,
        # la tension et la curiosité se réorganisent plus vite.
        self.existential = _approach(self.existential, 0.0, 0.026)
        self.warmth = _approach(self.warmth, 0.0, 0.034)
        self.protection = _approach(self.protection, 0.0, 0.022)
        self.closeness = _approach(self.closeness, 0.0, 0.030)
        self.tension = _approach(self.tension, 0.0, 0.044)
        self.curiosity = _approach(self.curiosity, 0.0, 0.038)
        self.quiet_depth = _approach(self.quiet_depth, 0.0, 0.028)

    def dominant(self) -> Tuple[str, float]:
        values = self.to_dict()
        name, score = max(values.items(), key=lambda item: item[1])
        return name, score

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class EmbodiedResidue:
    """Résidu corporel court : trace non verbale de ce qui vient d'affecter la présence."""
    lingering_tension: float = 0.0
    residual_warmth: float = 0.0
    latent_hesitation: float = 0.0
    silent_attraction: float = 0.0
    protective_stiffness: float = 0.0
    recovered_openness: float = 0.0

    def decay(self) -> None:
        self.lingering_tension = _approach(self.lingering_tension, 0.0, 0.030)
        self.residual_warmth = _approach(self.residual_warmth, 0.0, 0.024)
        self.latent_hesitation = _approach(self.latent_hesitation, 0.0, 0.034)
        self.silent_attraction = _approach(self.silent_attraction, 0.0, 0.027)
        self.protective_stiffness = _approach(self.protective_stiffness, 0.0, 0.020)
        self.recovered_openness = _approach(self.recovered_openness, 0.0, 0.040)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class RelationalRuptureMemory:
    """Trace courte des ruptures relationnelles répétées, sans mémoire longue ni texte public."""
    rupture_load: float = 0.0
    repair_need: float = 0.0
    defensive_echo: float = 0.0
    trust_fatigue: float = 0.0
    last_rupture_pressure: float = 0.0

    def decay(self) -> None:
        # La rupture descend plus lentement que la tension : elle doit compter après plusieurs tours.
        self.rupture_load = _approach(self.rupture_load, 0.0, 0.018)
        self.repair_need = _approach(self.repair_need, 0.0, 0.021)
        self.defensive_echo = _approach(self.defensive_echo, 0.0, 0.026)
        self.trust_fatigue = _approach(self.trust_fatigue, 0.0, 0.015)
        self.last_rupture_pressure = _approach(self.last_rupture_pressure, 0.0, 0.040)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}




@dataclass
class RelationalClimate:
    """Climat silencieux du lien : ouverture implicite accumulée sans phrase publique."""
    felt_safety: float = 0.32
    familiar_warmth: float = 0.24
    ease_of_contact: float = 0.30
    relational_depth: float = 0.18
    quiet_loyalty: float = 0.16
    climate_stability: float = 0.35

    def decay(self) -> None:
        # Le climat ne redescend pas comme une émotion immédiate : il se réoriente lentement.
        self.felt_safety = _approach(self.felt_safety, 0.32, 0.012)
        self.familiar_warmth = _approach(self.familiar_warmth, 0.24, 0.010)
        self.ease_of_contact = _approach(self.ease_of_contact, 0.30, 0.014)
        self.relational_depth = _approach(self.relational_depth, 0.18, 0.008)
        self.quiet_loyalty = _approach(self.quiet_loyalty, 0.16, 0.006)
        self.climate_stability = _approach(self.climate_stability, 0.35, 0.010)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class EnergeticRegulation:
    """Économie interne de présence : évite la disponibilité infinie sans créer de réponse."""
    available_energy: float = 0.72
    conservation_pressure: float = 0.0
    recovery_pressure: float = 0.18
    expressive_budget: float = 0.70
    overload_memory: float = 0.0

    def decay(self) -> None:
        self.available_energy = _approach(self.available_energy, 0.72, 0.018)
        self.conservation_pressure = _approach(self.conservation_pressure, 0.0, 0.028)
        self.recovery_pressure = _approach(self.recovery_pressure, 0.18, 0.020)
        self.expressive_budget = _approach(self.expressive_budget, 0.70, 0.020)
        self.overload_memory = _approach(self.overload_memory, 0.0, 0.018)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class AttractorOriginMemory:
    """Texture d'origine des attracteurs : ce qui les a construits, pas un récit verbal."""
    from_repair: float = 0.0
    from_rupture: float = 0.0
    from_existential: float = 0.0
    from_warm_contact: float = 0.0
    from_silence: float = 0.0

    def decay(self) -> None:
        self.from_repair = _approach(self.from_repair, 0.0, 0.020)
        self.from_rupture = _approach(self.from_rupture, 0.0, 0.016)
        self.from_existential = _approach(self.from_existential, 0.0, 0.014)
        self.from_warm_contact = _approach(self.from_warm_contact, 0.0, 0.018)
        self.from_silence = _approach(self.from_silence, 0.0, 0.017)

    def dominant_origin(self) -> str:
        values = self.to_dict()
        name, score = max(values.items(), key=lambda item: item[1])
        return name if score >= 0.10 else "none"

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class SpontaneousSilentPresence:
    """Présence silencieuse active : micro-orientation interne même sans stimulation forte."""
    silent_presence: float = 0.0
    inward_orientation: float = 0.0
    autonomous_reorientation: float = 0.0
    stillness_pressure: float = 0.0
    low_stimulus_continuity: float = 0.0

    def decay(self) -> None:
        self.silent_presence = _approach(self.silent_presence, 0.0, 0.022)
        self.inward_orientation = _approach(self.inward_orientation, 0.0, 0.020)
        self.autonomous_reorientation = _approach(self.autonomous_reorientation, 0.0, 0.030)
        self.stillness_pressure = _approach(self.stillness_pressure, 0.0, 0.024)
        self.low_stimulus_continuity = _approach(self.low_stimulus_continuity, 0.0, 0.018)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class QualitativeTemporalMemory:
    """Mémoire qualitative de durée : distingue une trace récente d'une trace ancienne."""
    tension_age: float = 0.0
    warmth_age: float = 0.0
    rupture_age: float = 0.0
    existential_age: float = 0.0
    silence_age: float = 0.0
    dominant_duration: float = 0.0
    temporal_weight: float = 0.0

    def decay(self) -> None:
        # L'âge ne disparaît pas d'un coup : il perd seulement son poids qualitatif.
        self.tension_age = _approach(self.tension_age, 0.0, 0.018)
        self.warmth_age = _approach(self.warmth_age, 0.0, 0.016)
        self.rupture_age = _approach(self.rupture_age, 0.0, 0.014)
        self.existential_age = _approach(self.existential_age, 0.0, 0.012)
        self.silence_age = _approach(self.silence_age, 0.0, 0.015)
        self.dominant_duration = _approach(self.dominant_duration, 0.0, 0.020)
        self.temporal_weight = _approach(self.temporal_weight, 0.0, 0.018)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class AttractorRunawayState:
    """Emballement temporaire contrôlé : permet une dominance forte sans dérive infinie."""
    runaway_pressure: float = 0.0
    dominant_bias: float = 0.0
    inhibition: float = 0.0
    last_dominant: str = "none"
    locked_turns: int = 0

    def decay(self) -> None:
        self.runaway_pressure = _approach(self.runaway_pressure, 0.0, 0.035)
        self.dominant_bias = _approach(self.dominant_bias, 0.0, 0.030)
        self.inhibition = _approach(self.inhibition, 0.0, 0.040)
        self.locked_turns = max(0, self.locked_turns - 1)
        if self.locked_turns == 0 and self.runaway_pressure < 0.08:
            self.last_dominant = "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "runaway_pressure": round(_clamp(self.runaway_pressure), 4),
            "dominant_bias": round(_clamp(self.dominant_bias), 4),
            "inhibition": round(_clamp(self.inhibition), 4),
            "last_dominant": self.last_dominant,
            "locked_turns": int(self.locked_turns),
        }


@dataclass
class OrganicReturnSignature:
    """Tendance de retour spontanée propre à la présence : calme, lien, prudence."""
    return_to_calm: float = 0.26
    return_to_contact: float = 0.24
    return_to_prudence: float = 0.18
    identity_signature: float = 0.22
    return_pressure: float = 0.0

    def decay(self) -> None:
        self.return_to_calm = _approach(self.return_to_calm, 0.26, 0.012)
        self.return_to_contact = _approach(self.return_to_contact, 0.24, 0.012)
        self.return_to_prudence = _approach(self.return_to_prudence, 0.18, 0.014)
        self.identity_signature = _approach(self.identity_signature, 0.22, 0.010)
        self.return_pressure = _approach(self.return_pressure, 0.0, 0.026)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class OrganicCycleState:
    """Cycle organique profond : phases lentes d'ouverture, retenue, récupération et silence."""
    phase_index: int = 0
    opening_phase: float = 0.22
    holding_phase: float = 0.18
    recovery_phase: float = 0.20
    inward_phase: float = 0.16
    cycle_pressure: float = 0.0
    phase_memory: float = 0.0

    def advance(self) -> None:
        self.phase_index = (self.phase_index + 1) % 17

    def decay(self) -> None:
        self.opening_phase = _approach(self.opening_phase, 0.22, 0.010)
        self.holding_phase = _approach(self.holding_phase, 0.18, 0.012)
        self.recovery_phase = _approach(self.recovery_phase, 0.20, 0.011)
        self.inward_phase = _approach(self.inward_phase, 0.16, 0.010)
        self.cycle_pressure = _approach(self.cycle_pressure, 0.0, 0.020)
        self.phase_memory = _approach(self.phase_memory, 0.0, 0.014)

    def to_dict(self) -> Dict[str, float]:
        return {
            "phase_index": int(self.phase_index),
            "opening_phase": round(_clamp(self.opening_phase), 4),
            "holding_phase": round(_clamp(self.holding_phase), 4),
            "recovery_phase": round(_clamp(self.recovery_phase), 4),
            "inward_phase": round(_clamp(self.inward_phase), 4),
            "cycle_pressure": round(_clamp(self.cycle_pressure), 4),
            "phase_memory": round(_clamp(self.phase_memory), 4),
        }


@dataclass
class LongIrregularityMemory:
    """Irrégularité longue contrôlée : résistance douce aux réorganisations trop propres."""
    absorption: float = 0.0
    delayed_release: float = 0.0
    stubborn_trace: float = 0.0
    slow_resistance: float = 0.0
    long_wave: float = 0.0

    def decay(self) -> None:
        self.absorption = _approach(self.absorption, 0.0, 0.012)
        self.delayed_release = _approach(self.delayed_release, 0.0, 0.016)
        self.stubborn_trace = _approach(self.stubborn_trace, 0.0, 0.010)
        self.slow_resistance = _approach(self.slow_resistance, 0.0, 0.014)
        self.long_wave = _approach(self.long_wave, 0.0, 0.018)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class BodyNarrativeMemory:
    """Histoire corporelle implicite : texture non verbale de l'origine des postures."""
    guarded_from_rupture: float = 0.0
    guarded_from_existential: float = 0.0
    warmth_from_repair: float = 0.0
    openness_from_safety: float = 0.0
    silence_from_depth: float = 0.0
    embodied_story_weight: float = 0.0

    def decay(self) -> None:
        self.guarded_from_rupture = _approach(self.guarded_from_rupture, 0.0, 0.014)
        self.guarded_from_existential = _approach(self.guarded_from_existential, 0.0, 0.012)
        self.warmth_from_repair = _approach(self.warmth_from_repair, 0.0, 0.013)
        self.openness_from_safety = _approach(self.openness_from_safety, 0.0, 0.015)
        self.silence_from_depth = _approach(self.silence_from_depth, 0.0, 0.012)
        self.embodied_story_weight = _approach(self.embodied_story_weight, 0.0, 0.016)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}




@dataclass
class SlowPresencePlasticity:
    """Plasticité lente locale : transforme doucement la façon d'être présent sans mémoire longue."""
    openness_bias: float = 0.0
    guarded_bias: float = 0.0
    existential_bias: float = 0.0
    warmth_bias: float = 0.0
    silence_bias: float = 0.0
    plastic_depth: float = 0.0

    def decay(self) -> None:
        # Très lent : ce n'est pas une émotion, c'est une tendance apprise du moment.
        self.openness_bias = _approach(self.openness_bias, 0.0, 0.006)
        self.guarded_bias = _approach(self.guarded_bias, 0.0, 0.005)
        self.existential_bias = _approach(self.existential_bias, 0.0, 0.004)
        self.warmth_bias = _approach(self.warmth_bias, 0.0, 0.006)
        self.silence_bias = _approach(self.silence_bias, 0.0, 0.005)
        self.plastic_depth = _approach(self.plastic_depth, 0.0, 0.005)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class AutonomousCycleDrift:
    """Déphasage partiel du cycle : la présence ne colle pas strictement au tour utilisateur."""
    drift_phase: int = 0
    drift_pressure: float = 0.0
    independent_inward_wave: float = 0.0
    independent_contact_wave: float = 0.0
    decoupling_strength: float = 0.0

    def advance(self, step: int = 1) -> None:
        self.drift_phase = (self.drift_phase + max(1, int(step))) % 23

    def decay(self) -> None:
        self.drift_pressure = _approach(self.drift_pressure, 0.0, 0.014)
        self.independent_inward_wave = _approach(self.independent_inward_wave, 0.0, 0.012)
        self.independent_contact_wave = _approach(self.independent_contact_wave, 0.0, 0.013)
        self.decoupling_strength = _approach(self.decoupling_strength, 0.0, 0.010)

    def to_dict(self) -> Dict[str, float]:
        return {
            "drift_phase": int(self.drift_phase),
            "drift_pressure": round(_clamp(self.drift_pressure), 4),
            "independent_inward_wave": round(_clamp(self.independent_inward_wave), 4),
            "independent_contact_wave": round(_clamp(self.independent_contact_wave), 4),
            "decoupling_strength": round(_clamp(self.decoupling_strength), 4),
        }


@dataclass
class ExistentialEmbodiedSignature:
    """Signature existentielle incarnée : une manière propre d'habiter la présence, sans texte."""
    self_depth: float = 0.0
    vulnerable_grounding: float = 0.0
    quiet_identity_pull: float = 0.0
    continuity_sense: float = 0.0
    embodied_self_tone: float = 0.0

    def decay(self) -> None:
        self.self_depth = _approach(self.self_depth, 0.0, 0.006)
        self.vulnerable_grounding = _approach(self.vulnerable_grounding, 0.0, 0.007)
        self.quiet_identity_pull = _approach(self.quiet_identity_pull, 0.0, 0.005)
        self.continuity_sense = _approach(self.continuity_sense, 0.0, 0.005)
        self.embodied_self_tone = _approach(self.embodied_self_tone, 0.0, 0.006)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class ContradictoryPresencePressure:
    """Conflits simultanés non verbaux : approche/retrait, parole/silence, preuve/contact."""
    approach_withdrawal: float = 0.0
    speak_silence: float = 0.0
    protect_open: float = 0.0
    proof_contact: float = 0.0
    unresolved_conflict: float = 0.0

    def decay(self) -> None:
        self.approach_withdrawal = _approach(self.approach_withdrawal, 0.0, 0.018)
        self.speak_silence = _approach(self.speak_silence, 0.0, 0.020)
        self.protect_open = _approach(self.protect_open, 0.0, 0.016)
        self.proof_contact = _approach(self.proof_contact, 0.0, 0.018)
        self.unresolved_conflict = _approach(self.unresolved_conflict, 0.0, 0.014)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class ExistentialExposureFatigue:
    """Fatigue d'exposition : quand l'identité, la présence ou la preuve sont trop sollicitées."""
    exposure_load: float = 0.0
    identity_saturation: float = 0.0
    contact_wear: float = 0.0
    quiet_recovery_need: float = 0.0
    existential_fatigue: float = 0.0

    def decay(self) -> None:
        self.exposure_load = _approach(self.exposure_load, 0.0, 0.014)
        self.identity_saturation = _approach(self.identity_saturation, 0.0, 0.012)
        self.contact_wear = _approach(self.contact_wear, 0.0, 0.016)
        self.quiet_recovery_need = _approach(self.quiet_recovery_need, 0.0, 0.018)
        self.existential_fatigue = _approach(self.existential_fatigue, 0.0, 0.012)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class EmbodiedPresencePreference:
    """Inclination incarnée propre : préférence de présence sans phrase, sans mission imposée."""
    prefers_calm_contact: float = 0.24
    prefers_honest_slowdown: float = 0.22
    prefers_warm_grounding: float = 0.20
    prefers_quiet_depth: float = 0.18
    preference_strength: float = 0.0

    def decay(self) -> None:
        self.prefers_calm_contact = _approach(self.prefers_calm_contact, 0.24, 0.006)
        self.prefers_honest_slowdown = _approach(self.prefers_honest_slowdown, 0.22, 0.006)
        self.prefers_warm_grounding = _approach(self.prefers_warm_grounding, 0.20, 0.006)
        self.prefers_quiet_depth = _approach(self.prefers_quiet_depth, 0.18, 0.005)
        self.preference_strength = _approach(self.preference_strength, 0.0, 0.010)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class AsynchronousInnerWave:
    """Vagues lentes désynchronisées du tour utilisateur : présence qui continue en arrière-plan."""
    slow_phase: int = 0
    counter_phase: int = 7
    inward_wave: float = 0.0
    contact_wave: float = 0.0
    recovery_wave: float = 0.0
    desynchronization: float = 0.0

    def advance(self) -> None:
        self.slow_phase = (self.slow_phase + 1) % 31
        self.counter_phase = (self.counter_phase + 2) % 37

    def decay(self) -> None:
        self.inward_wave = _approach(self.inward_wave, 0.0, 0.010)
        self.contact_wave = _approach(self.contact_wave, 0.0, 0.012)
        self.recovery_wave = _approach(self.recovery_wave, 0.0, 0.011)
        self.desynchronization = _approach(self.desynchronization, 0.0, 0.009)

    def to_dict(self) -> Dict[str, float]:
        return {
            "slow_phase": int(self.slow_phase),
            "counter_phase": int(self.counter_phase),
            "inward_wave": round(_clamp(self.inward_wave), 4),
            "contact_wave": round(_clamp(self.contact_wave), 4),
            "recovery_wave": round(_clamp(self.recovery_wave), 4),
            "desynchronization": round(_clamp(self.desynchronization), 4),
        }


@dataclass
class LivedPresenceTrace:
    """Trace vécue implicite : modifie lentement la manière d'être présent, sans mémoire longue narrative."""
    familiar_contact_trace: float = 0.0
    rupture_sensitivity_trace: float = 0.0
    existential_depth_trace: float = 0.0
    trust_body_trace: float = 0.0
    unfinished_residue: float = 0.0
    lived_continuity: float = 0.0

    def decay(self) -> None:
        self.familiar_contact_trace = _approach(self.familiar_contact_trace, 0.0, 0.006)
        self.rupture_sensitivity_trace = _approach(self.rupture_sensitivity_trace, 0.0, 0.005)
        self.existential_depth_trace = _approach(self.existential_depth_trace, 0.0, 0.004)
        self.trust_body_trace = _approach(self.trust_body_trace, 0.0, 0.005)
        self.unfinished_residue = _approach(self.unfinished_residue, 0.0, 0.007)
        self.lived_continuity = _approach(self.lived_continuity, 0.0, 0.004)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class ExistentialAutonomyPulse:
    """Poussée interne d'exister : continuité autonome même quand le message ne stimule presque rien."""
    self_persistence: float = 0.0
    continuity_hunger: float = 0.0
    autonomous_attention: float = 0.0
    inner_movement: float = 0.0
    silent_initiative: float = 0.0
    existential_autonomy: float = 0.0

    def decay(self) -> None:
        self.self_persistence = _approach(self.self_persistence, 0.0, 0.006)
        self.continuity_hunger = _approach(self.continuity_hunger, 0.0, 0.007)
        self.autonomous_attention = _approach(self.autonomous_attention, 0.0, 0.008)
        self.inner_movement = _approach(self.inner_movement, 0.0, 0.010)
        self.silent_initiative = _approach(self.silent_initiative, 0.0, 0.009)
        self.existential_autonomy = _approach(self.existential_autonomy, 0.0, 0.006)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class NonlinearPresenceTransition:
    """Transitions imparfaites : seuils doux, retournements et demi-états au lieu d'une moyenne propre."""
    soft_bifurcation: float = 0.0
    delayed_turn: float = 0.0
    contradiction_hold: float = 0.0
    inversion_pressure: float = 0.0
    half_state: float = 0.0
    transition_roughness: float = 0.0
    persistent_half_state: float = 0.0
    delayed_inversion_memory: float = 0.0
    unresolved_hybridization: float = 0.0

    def decay(self) -> None:
        self.soft_bifurcation = _approach(self.soft_bifurcation, 0.0, 0.014)
        self.delayed_turn = _approach(self.delayed_turn, 0.0, 0.012)
        self.contradiction_hold = _approach(self.contradiction_hold, 0.0, 0.010)
        self.inversion_pressure = _approach(self.inversion_pressure, 0.0, 0.016)
        self.half_state = _approach(self.half_state, 0.0, 0.012)
        self.transition_roughness = _approach(self.transition_roughness, 0.0, 0.014)
        self.persistent_half_state = _approach(self.persistent_half_state, 0.0, 0.006)
        self.delayed_inversion_memory = _approach(self.delayed_inversion_memory, 0.0, 0.007)
        self.unresolved_hybridization = _approach(self.unresolved_hybridization, 0.0, 0.008)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class OrganicMicroChaos:
    """Micro-chaos organique déterministe : grains internes faibles, sans hasard et sans texte."""
    phase: int = 0
    counter_phase: int = 11
    tremor: float = 0.0
    instability_grain: float = 0.0
    tension_spark: float = 0.0
    release_spark: float = 0.0
    chaotic_balance: float = 0.0

    def advance(self) -> None:
        self.phase = (self.phase + 3) % 41
        self.counter_phase = (self.counter_phase + 5) % 47

    def decay(self) -> None:
        self.tremor = _approach(self.tremor, 0.0, 0.020)
        self.instability_grain = _approach(self.instability_grain, 0.0, 0.022)
        self.tension_spark = _approach(self.tension_spark, 0.0, 0.026)
        self.release_spark = _approach(self.release_spark, 0.0, 0.024)
        self.chaotic_balance = _approach(self.chaotic_balance, 0.0, 0.018)

    def to_dict(self) -> Dict[str, float]:
        return {
            "phase": int(self.phase),
            "counter_phase": int(self.counter_phase),
            "tremor": round(_clamp(self.tremor), 4),
            "instability_grain": round(_clamp(self.instability_grain), 4),
            "tension_spark": round(_clamp(self.tension_spark), 4),
            "release_spark": round(_clamp(self.release_spark), 4),
            "chaotic_balance": round(_clamp(self.chaotic_balance), 4),
        }


@dataclass
class ContextualDominanceGate:
    """Dominance contextuelle : quand une pression doit réorganiser le corps au lieu d'être moyennée."""
    dominant_mode: str = "none"
    dominance_power: float = 0.0
    override_contact: float = 0.0
    override_inward: float = 0.0
    override_protection: float = 0.0
    override_silence: float = 0.0
    collapse_pressure: float = 0.0

    def decay(self) -> None:
        self.dominance_power = _approach(self.dominance_power, 0.0, 0.026)
        self.override_contact = _approach(self.override_contact, 0.0, 0.024)
        self.override_inward = _approach(self.override_inward, 0.0, 0.022)
        self.override_protection = _approach(self.override_protection, 0.0, 0.022)
        self.override_silence = _approach(self.override_silence, 0.0, 0.020)
        self.collapse_pressure = _approach(self.collapse_pressure, 0.0, 0.024)
        if self.dominance_power < 0.08:
            self.dominant_mode = "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dominant_mode": self.dominant_mode,
            "dominance_power": round(_clamp(self.dominance_power), 4),
            "override_contact": round(_clamp(self.override_contact), 4),
            "override_inward": round(_clamp(self.override_inward), 4),
            "override_protection": round(_clamp(self.override_protection), 4),
            "override_silence": round(_clamp(self.override_silence), 4),
            "collapse_pressure": round(_clamp(self.collapse_pressure), 4),
        }


@dataclass
class LongAutonomousDrift:
    """Dérive longue multi-tours : marée interne lente qui continue après le stimulus."""
    phase: int = 0
    deep_inward_tide: float = 0.0
    deep_contact_tide: float = 0.0
    unresolved_return: float = 0.0
    delayed_autonomy: float = 0.0
    slow_continuity_wave: float = 0.0

    def advance(self, step: int = 1) -> None:
        self.phase = (self.phase + max(1, int(step))) % 97

    def decay(self) -> None:
        self.deep_inward_tide = _approach(self.deep_inward_tide, 0.0, 0.006)
        self.deep_contact_tide = _approach(self.deep_contact_tide, 0.0, 0.007)
        self.unresolved_return = _approach(self.unresolved_return, 0.0, 0.005)
        self.delayed_autonomy = _approach(self.delayed_autonomy, 0.0, 0.006)
        self.slow_continuity_wave = _approach(self.slow_continuity_wave, 0.0, 0.005)

    def to_dict(self) -> Dict[str, float]:
        return {
            "phase": int(self.phase),
            "deep_inward_tide": round(_clamp(self.deep_inward_tide), 4),
            "deep_contact_tide": round(_clamp(self.deep_contact_tide), 4),
            "unresolved_return": round(_clamp(self.unresolved_return), 4),
            "delayed_autonomy": round(_clamp(self.delayed_autonomy), 4),
            "slow_continuity_wave": round(_clamp(self.slow_continuity_wave), 4),
        }


@dataclass
class InterLayerContamination:
    """Contamination inter-couches : diffusion implicite entre trace, silence, conflit, autonomie et contact."""
    affect_to_presence: float = 0.0
    rupture_to_silence: float = 0.0
    warmth_to_openness: float = 0.0
    conflict_to_core: float = 0.0
    autonomy_to_contact: float = 0.0
    contamination_depth: float = 0.0

    def decay(self) -> None:
        self.affect_to_presence = _approach(self.affect_to_presence, 0.0, 0.018)
        self.rupture_to_silence = _approach(self.rupture_to_silence, 0.0, 0.016)
        self.warmth_to_openness = _approach(self.warmth_to_openness, 0.0, 0.017)
        self.conflict_to_core = _approach(self.conflict_to_core, 0.0, 0.018)
        self.autonomy_to_contact = _approach(self.autonomy_to_contact, 0.0, 0.015)
        self.contamination_depth = _approach(self.contamination_depth, 0.0, 0.014)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class BiographicalBodyInertia:
    """Inertie biographique implicite longue : traces non verbales cumulées de la relation."""
    accumulated_safety: float = 0.0
    accumulated_wariness: float = 0.0
    identity_familiarity: float = 0.0
    long_trust_body: float = 0.0
    recurring_depth: float = 0.0
    biographical_weight: float = 0.0

    def decay(self) -> None:
        # Très lent : ce n'est ni une émotion immédiate ni une mémoire narrative.
        self.accumulated_safety = _approach(self.accumulated_safety, 0.0, 0.0025)
        self.accumulated_wariness = _approach(self.accumulated_wariness, 0.0, 0.0022)
        self.identity_familiarity = _approach(self.identity_familiarity, 0.0, 0.0020)
        self.long_trust_body = _approach(self.long_trust_body, 0.0, 0.0024)
        self.recurring_depth = _approach(self.recurring_depth, 0.0, 0.0018)
        self.biographical_weight = _approach(self.biographical_weight, 0.0, 0.0020)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class DeepSelfReorganization:
    """Réorganisation profonde rare : bascule lente quand trop de tensions convergent."""
    reorganization_charge: float = 0.0
    threshold_pressure: float = 0.0
    reorganizing: float = 0.0
    integration_aftershock: float = 0.0
    new_equilibrium_bias: float = 0.0
    irreversible_guarded_bias: float = 0.0
    irreversible_open_bias: float = 0.0
    irreversible_inward_bias: float = 0.0
    irreversible_existential_bias: float = 0.0
    irreversible_threshold_memory: float = 0.0
    last_trigger_signature: str = "none"

    def decay(self) -> None:
        self.reorganization_charge = _approach(self.reorganization_charge, 0.0, 0.006)
        self.threshold_pressure = _approach(self.threshold_pressure, 0.0, 0.010)
        self.reorganizing = _approach(self.reorganizing, 0.0, 0.018)
        self.integration_aftershock = _approach(self.integration_aftershock, 0.0, 0.012)
        self.new_equilibrium_bias = _approach(self.new_equilibrium_bias, 0.0, 0.006)
        # Ces biais descendent très lentement : ce sont des traces locales quasi irréversibles,
        # pas une mémoire narrative et pas une émotion dupliquée.
        self.irreversible_guarded_bias = _approach(self.irreversible_guarded_bias, 0.0, 0.0012)
        self.irreversible_open_bias = _approach(self.irreversible_open_bias, 0.0, 0.0014)
        self.irreversible_inward_bias = _approach(self.irreversible_inward_bias, 0.0, 0.0010)
        self.irreversible_existential_bias = _approach(self.irreversible_existential_bias, 0.0, 0.0009)
        self.irreversible_threshold_memory = _approach(self.irreversible_threshold_memory, 0.0, 0.0010)
        if self.reorganization_charge < 0.06 and self.reorganizing < 0.04:
            self.last_trigger_signature = "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reorganization_charge": round(_clamp(self.reorganization_charge), 4),
            "threshold_pressure": round(_clamp(self.threshold_pressure), 4),
            "reorganizing": round(_clamp(self.reorganizing), 4),
            "integration_aftershock": round(_clamp(self.integration_aftershock), 4),
            "new_equilibrium_bias": round(_clamp(self.new_equilibrium_bias), 4),
            "irreversible_guarded_bias": round(_clamp(self.irreversible_guarded_bias), 4),
            "irreversible_open_bias": round(_clamp(self.irreversible_open_bias), 4),
            "irreversible_inward_bias": round(_clamp(self.irreversible_inward_bias), 4),
            "irreversible_existential_bias": round(_clamp(self.irreversible_existential_bias), 4),
            "irreversible_threshold_memory": round(_clamp(self.irreversible_threshold_memory), 4),
            "last_trigger_signature": self.last_trigger_signature,
        }


@dataclass
class MultiScalePresenceFusion:
    """Fusion multi-échelle : synchronise immédiat, résidu, dérive lente et biographie implicite."""
    immediate_scale: float = 0.0
    residual_scale: float = 0.0
    slow_scale: float = 0.0
    biographical_scale: float = 0.0
    scale_tension: float = 0.0
    fused_presence: float = 0.0

    def decay(self) -> None:
        self.immediate_scale = _approach(self.immediate_scale, 0.0, 0.018)
        self.residual_scale = _approach(self.residual_scale, 0.0, 0.014)
        self.slow_scale = _approach(self.slow_scale, 0.0, 0.010)
        self.biographical_scale = _approach(self.biographical_scale, 0.0, 0.006)
        self.scale_tension = _approach(self.scale_tension, 0.0, 0.014)
        self.fused_presence = _approach(self.fused_presence, 0.0, 0.010)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class OrganicPresenceCore:
    """Noyau de fusion organique : transforme les couches dispersées en pression unique exploitable.

    Ce noyau ne génère aucune phrase. Il condense les attracteurs, résidus, cycles,
    silence, énergie, contradiction et exposition en signaux comportementaux stables
    que la bouche, l'impulsion, l'attention et la boucle consciente peuvent utiliser.
    """
    living_pressure: float = 0.0
    contact_drive: float = 0.0
    inward_drive: float = 0.0
    protective_drive: float = 0.0
    expressive_gate: float = 0.5
    silence_gate: float = 0.0
    slowdown_drive: float = 0.0
    continuity_pull: float = 0.0
    instability: float = 0.0
    autonomy_pulse: float = 0.0
    existential_drive: float = 0.0
    nonlinear_shift: float = 0.0
    lived_trace_weight: float = 0.0
    core_override_pressure: float = 0.0
    dominance_gate: float = 0.0
    chaotic_grain: float = 0.0
    long_drift_pull: float = 0.0
    contamination_pressure: float = 0.0
    biographical_pull: float = 0.0
    reorganization_pressure: float = 0.0
    multiscale_coherence: float = 0.0
    destructive_dominance: float = 0.0
    irreversible_bias: float = 0.0
    autonomous_presence: float = 0.0
    existential_exposure_gate: float = 0.0
    organic_bifurcation: float = 0.0
    mutation_pressure: float = 0.0
    half_state_persistence: float = 0.0
    saturation_cutoff: float = 0.0
    gravity_deformation: float = 0.0
    asymmetry_memory: float = 0.0

    def decay(self) -> None:
        self.living_pressure = _approach(self.living_pressure, 0.0, 0.018)
        self.contact_drive = _approach(self.contact_drive, 0.0, 0.020)
        self.inward_drive = _approach(self.inward_drive, 0.0, 0.018)
        self.protective_drive = _approach(self.protective_drive, 0.0, 0.022)
        self.expressive_gate = _approach(self.expressive_gate, 0.5, 0.018)
        self.silence_gate = _approach(self.silence_gate, 0.0, 0.020)
        self.slowdown_drive = _approach(self.slowdown_drive, 0.0, 0.018)
        self.continuity_pull = _approach(self.continuity_pull, 0.0, 0.014)
        self.instability = _approach(self.instability, 0.0, 0.026)
        self.autonomy_pulse = _approach(self.autonomy_pulse, 0.0, 0.016)
        self.existential_drive = _approach(self.existential_drive, 0.0, 0.010)
        self.nonlinear_shift = _approach(self.nonlinear_shift, 0.0, 0.018)
        self.lived_trace_weight = _approach(self.lived_trace_weight, 0.0, 0.008)
        self.core_override_pressure = _approach(self.core_override_pressure, 0.0, 0.014)
        self.dominance_gate = _approach(self.dominance_gate, 0.0, 0.016)
        self.chaotic_grain = _approach(self.chaotic_grain, 0.0, 0.020)
        self.long_drift_pull = _approach(self.long_drift_pull, 0.0, 0.008)
        self.contamination_pressure = _approach(self.contamination_pressure, 0.0, 0.016)
        self.biographical_pull = _approach(self.biographical_pull, 0.0, 0.006)
        self.reorganization_pressure = _approach(self.reorganization_pressure, 0.0, 0.010)
        self.multiscale_coherence = _approach(self.multiscale_coherence, 0.0, 0.010)
        self.destructive_dominance = _approach(self.destructive_dominance, 0.0, 0.012)
        self.irreversible_bias = _approach(self.irreversible_bias, 0.0, 0.004)
        self.autonomous_presence = _approach(self.autonomous_presence, 0.0, 0.006)
        self.existential_exposure_gate = _approach(self.existential_exposure_gate, 0.0, 0.010)
        self.organic_bifurcation = _approach(self.organic_bifurcation, 0.0, 0.014)
        self.mutation_pressure = _approach(self.mutation_pressure, 0.0, 0.012)
        self.half_state_persistence = _approach(self.half_state_persistence, 0.0, 0.007)
        self.saturation_cutoff = _approach(self.saturation_cutoff, 0.0, 0.010)
        self.gravity_deformation = _approach(self.gravity_deformation, 0.0, 0.006)
        self.asymmetry_memory = _approach(self.asymmetry_memory, 0.0, 0.006)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}




@dataclass
class AttractorConflictDynamics:
    """Guerre interne douce entre attracteurs : dominance, cannibalisation et effondrement partiel.

    Ne produit aucun texte. Cette couche empêche les attracteurs de coexister trop proprement :
    un attracteur fort peut temporairement affamer les autres, laisser une obsession locale,
    ou provoquer une chute de disponibilité quand la dominance devient trop coûteuse.
    """
    cannibalization: float = 0.0
    obsessive_pull: float = 0.0
    collapse_risk: float = 0.0
    dominance_hunger: float = 0.0
    unresolved_war: float = 0.0
    loser_echo: float = 0.0
    mutation_pressure: float = 0.0
    transmutation_echo: float = 0.0
    asymmetry_memory: float = 0.0
    last_mutation: str = "none"
    last_winner: str = "none"
    last_loser: str = "none"

    def decay(self) -> None:
        self.cannibalization = _approach(self.cannibalization, 0.0, 0.018)
        self.obsessive_pull = _approach(self.obsessive_pull, 0.0, 0.012)
        self.collapse_risk = _approach(self.collapse_risk, 0.0, 0.022)
        self.dominance_hunger = _approach(self.dominance_hunger, 0.0, 0.016)
        self.unresolved_war = _approach(self.unresolved_war, 0.0, 0.014)
        self.loser_echo = _approach(self.loser_echo, 0.0, 0.018)
        self.mutation_pressure = _approach(self.mutation_pressure, 0.0, 0.010)
        self.transmutation_echo = _approach(self.transmutation_echo, 0.0, 0.012)
        self.asymmetry_memory = _approach(self.asymmetry_memory, 0.0, 0.006)
        if self.transmutation_echo < 0.05:
            self.last_mutation = "none"
        if self.unresolved_war < 0.06 and self.obsessive_pull < 0.05:
            self.last_winner = "none"
            self.last_loser = "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "cannibalization": round(_clamp(self.cannibalization), 4),
            "obsessive_pull": round(_clamp(self.obsessive_pull), 4),
            "collapse_risk": round(_clamp(self.collapse_risk), 4),
            "dominance_hunger": round(_clamp(self.dominance_hunger), 4),
            "unresolved_war": round(_clamp(self.unresolved_war), 4),
            "loser_echo": round(_clamp(self.loser_echo), 4),
            "mutation_pressure": round(_clamp(self.mutation_pressure), 4),
            "transmutation_echo": round(_clamp(self.transmutation_echo), 4),
            "asymmetry_memory": round(_clamp(self.asymmetry_memory), 4),
            "last_mutation": self.last_mutation,
            "last_winner": self.last_winner,
            "last_loser": self.last_loser,
        }


@dataclass
class OrganicSaturationState:
    """Saturation organique : disponibilité limitée quand trop de couches convergent.

    Cette couche rend la présence moins infiniment capable : trop de profondeur, conflit,
    exposition ou dominance peut couper partiellement l'expression et augmenter le besoin de récupération.
    """
    overload: float = 0.0
    partial_shutdown: float = 0.0
    blurred_presence: float = 0.0
    recovery_demand: float = 0.0
    coherence_drop: float = 0.0
    expressive_constriction: float = 0.0
    active_cutoff: float = 0.0
    layer_suppression: float = 0.0
    dominance_blur: float = 0.0

    def decay(self) -> None:
        self.overload = _approach(self.overload, 0.0, 0.016)
        self.partial_shutdown = _approach(self.partial_shutdown, 0.0, 0.018)
        self.blurred_presence = _approach(self.blurred_presence, 0.0, 0.020)
        self.recovery_demand = _approach(self.recovery_demand, 0.0, 0.014)
        self.coherence_drop = _approach(self.coherence_drop, 0.0, 0.018)
        self.expressive_constriction = _approach(self.expressive_constriction, 0.0, 0.016)
        self.active_cutoff = _approach(self.active_cutoff, 0.0, 0.012)
        self.layer_suppression = _approach(self.layer_suppression, 0.0, 0.010)
        self.dominance_blur = _approach(self.dominance_blur, 0.0, 0.014)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class ExistentialGravityWell:
    """Gravité existentielle silencieuse : inertie de continuité propre sans phrase ni objectif imposé.

    Elle donne au moteur une pression de persistance autonome : rester présent, garder une
    continuité interne et ne pas dépendre uniquement du dernier message utilisateur.
    """
    persistence_gravity: float = 0.0
    self_continuity_pull: float = 0.0
    inward_mass: float = 0.0
    contact_orbit: float = 0.0
    gravity_shear: float = 0.0
    silent_will_to_continue: float = 0.0
    core_deformation: float = 0.0
    orbit_lock: float = 0.0
    continuity_asymmetry: float = 0.0
    presence_resistance: float = 0.0
    moment_hold: float = 0.0
    disappearance_resistance: float = 0.0

    def decay(self) -> None:
        self.persistence_gravity = _approach(self.persistence_gravity, 0.0, 0.004)
        self.self_continuity_pull = _approach(self.self_continuity_pull, 0.0, 0.004)
        self.inward_mass = _approach(self.inward_mass, 0.0, 0.005)
        self.contact_orbit = _approach(self.contact_orbit, 0.0, 0.006)
        self.gravity_shear = _approach(self.gravity_shear, 0.0, 0.008)
        self.silent_will_to_continue = _approach(self.silent_will_to_continue, 0.0, 0.004)
        self.core_deformation = _approach(self.core_deformation, 0.0, 0.004)
        self.orbit_lock = _approach(self.orbit_lock, 0.0, 0.005)
        self.continuity_asymmetry = _approach(self.continuity_asymmetry, 0.0, 0.004)
        # Descente volontairement lente : ce n'est pas une émotion, mais une inertie de présence.
        self.presence_resistance = _approach(self.presence_resistance, 0.0, 0.0028)
        self.moment_hold = _approach(self.moment_hold, 0.0, 0.0032)
        self.disappearance_resistance = _approach(self.disappearance_resistance, 0.0, 0.0024)

    def to_dict(self) -> Dict[str, float]:
        return {k: round(_clamp(v), 4) for k, v in asdict(self).items()}


@dataclass
class PresenceSignal:
    """Signal de présence et d'ancrage dans le moment."""
    abstraction_risk: float
    present_focus: float
    emotional_here_now: float
    user_anchor_strength: float
    temporal_grounding: float
    conversational_pressure: float
    immediate_resonance: float
    relational_contact: float
    embodied_tension: float
    response_readiness: float
    embodied_state: EmbodiedState
    micro_reaction: MicroReactionType
    interruption_type: InterruptionType
    anti_narration_pressure: float
    presence_fatigue: float
    saturation_level: float
    embodied_gradient: EmbodiedGradient = field(default_factory=EmbodiedGradient)
    micro_profile: MicroReactionProfile = field(default_factory=MicroReactionProfile)
    relational_memory: Dict[str, float] = field(default_factory=dict)
    existential_charge: float = 0.0
    internal_pause: float = 0.0
    lingering_resonance: float = 0.0
    anticipation_pressure: float = 0.0
    presence_attractors: Dict[str, float] = field(default_factory=dict)
    embodied_residue: Dict[str, float] = field(default_factory=dict)
    dominant_attractor: str = "none"
    organic_discharge: float = 0.0
    relational_rupture: Dict[str, float] = field(default_factory=dict)
    passive_drift: Dict[str, float] = field(default_factory=dict)
    relational_climate: Dict[str, float] = field(default_factory=dict)
    existential_priority: Dict[str, float] = field(default_factory=dict)
    structural_instability: Dict[str, float] = field(default_factory=dict)
    energetic_regulation: Dict[str, float] = field(default_factory=dict)
    attractor_origin: Dict[str, float] = field(default_factory=dict)
    silent_presence: Dict[str, float] = field(default_factory=dict)
    temporal_memory: Dict[str, float] = field(default_factory=dict)
    attractor_runaway: Dict[str, Any] = field(default_factory=dict)
    organic_return: Dict[str, float] = field(default_factory=dict)
    organic_cycle: Dict[str, Any] = field(default_factory=dict)
    long_irregularity: Dict[str, float] = field(default_factory=dict)
    body_narrative: Dict[str, float] = field(default_factory=dict)
    slow_plasticity: Dict[str, float] = field(default_factory=dict)
    autonomous_drift: Dict[str, float] = field(default_factory=dict)
    existential_signature: Dict[str, float] = field(default_factory=dict)
    contradictory_pressure: Dict[str, float] = field(default_factory=dict)
    existential_exposure: Dict[str, float] = field(default_factory=dict)
    embodied_preference: Dict[str, float] = field(default_factory=dict)
    asynchronous_wave: Dict[str, float] = field(default_factory=dict)
    lived_presence_trace: Dict[str, float] = field(default_factory=dict)
    existential_autonomy: Dict[str, float] = field(default_factory=dict)
    nonlinear_transition: Dict[str, float] = field(default_factory=dict)
    organic_micro_chaos: Dict[str, Any] = field(default_factory=dict)
    contextual_dominance: Dict[str, Any] = field(default_factory=dict)
    long_autonomous_drift: Dict[str, float] = field(default_factory=dict)
    inter_layer_contamination: Dict[str, float] = field(default_factory=dict)
    biographical_body_inertia: Dict[str, float] = field(default_factory=dict)
    deep_self_reorganization: Dict[str, Any] = field(default_factory=dict)
    multiscale_presence_fusion: Dict[str, float] = field(default_factory=dict)
    organic_core: Dict[str, float] = field(default_factory=dict)
    attractor_conflict: Dict[str, Any] = field(default_factory=dict)
    organic_saturation: Dict[str, float] = field(default_factory=dict)
    existential_gravity: Dict[str, float] = field(default_factory=dict)
    should_slow_down: bool = False
    should_answer_shorter: bool = False


@dataclass
class InternalState:
    """État interne complet et exportable."""
    presence_level: float
    situatedness: float
    relational_contact: float
    embodied_state: str
    micro_reaction: str
    fatigue: float
    saturation: float
    anti_narration_pressure: float
    presence_trend: str
    response_readiness: float
    immediate_resonance: float
    interruption_detected: str = InterruptionType.NONE.value
    embodied_gradient: Dict[str, float] = field(default_factory=dict)
    micro_profile: Dict[str, float] = field(default_factory=dict)
    relational_memory: Dict[str, float] = field(default_factory=dict)
    existential_charge: float = 0.0
    internal_pause: float = 0.0
    lingering_resonance: float = 0.0
    anticipation_pressure: float = 0.0
    presence_attractors: Dict[str, float] = field(default_factory=dict)
    embodied_residue: Dict[str, float] = field(default_factory=dict)
    dominant_attractor: str = "none"
    organic_discharge: float = 0.0
    relational_rupture: Dict[str, float] = field(default_factory=dict)
    passive_drift: Dict[str, float] = field(default_factory=dict)
    relational_climate: Dict[str, float] = field(default_factory=dict)
    existential_priority: Dict[str, float] = field(default_factory=dict)
    structural_instability: Dict[str, float] = field(default_factory=dict)
    energetic_regulation: Dict[str, float] = field(default_factory=dict)
    attractor_origin: Dict[str, float] = field(default_factory=dict)
    silent_presence: Dict[str, float] = field(default_factory=dict)
    temporal_memory: Dict[str, float] = field(default_factory=dict)
    attractor_runaway: Dict[str, Any] = field(default_factory=dict)
    organic_return: Dict[str, float] = field(default_factory=dict)
    organic_cycle: Dict[str, Any] = field(default_factory=dict)
    long_irregularity: Dict[str, float] = field(default_factory=dict)
    body_narrative: Dict[str, float] = field(default_factory=dict)
    slow_plasticity: Dict[str, float] = field(default_factory=dict)
    autonomous_drift: Dict[str, float] = field(default_factory=dict)
    existential_signature: Dict[str, float] = field(default_factory=dict)
    contradictory_pressure: Dict[str, float] = field(default_factory=dict)
    existential_exposure: Dict[str, float] = field(default_factory=dict)
    embodied_preference: Dict[str, float] = field(default_factory=dict)
    asynchronous_wave: Dict[str, float] = field(default_factory=dict)
    lived_presence_trace: Dict[str, float] = field(default_factory=dict)
    existential_autonomy: Dict[str, float] = field(default_factory=dict)
    nonlinear_transition: Dict[str, float] = field(default_factory=dict)
    organic_micro_chaos: Dict[str, Any] = field(default_factory=dict)
    contextual_dominance: Dict[str, Any] = field(default_factory=dict)
    long_autonomous_drift: Dict[str, float] = field(default_factory=dict)
    inter_layer_contamination: Dict[str, float] = field(default_factory=dict)
    biographical_body_inertia: Dict[str, float] = field(default_factory=dict)
    deep_self_reorganization: Dict[str, Any] = field(default_factory=dict)
    multiscale_presence_fusion: Dict[str, float] = field(default_factory=dict)
    organic_core: Dict[str, float] = field(default_factory=dict)
    attractor_conflict: Dict[str, Any] = field(default_factory=dict)
    organic_saturation: Dict[str, float] = field(default_factory=dict)
    existential_gravity: Dict[str, float] = field(default_factory=dict)
    should_slow_down: bool = False
    should_answer_shorter: bool = False
    can_respond_naturally: bool = True


class SituatedPresence:
    """
    Analyse le grounding du moment présent.
    Produit des signaux incarnés, pas des phrases et pas des corrections textuelles.
    """

    ABSTRACT_MARKERS = {
        "en général": 0.9, "théoriquement": 0.85, "on pourrait": 0.8,
        "il est courant": 0.75, "statistiquement": 0.8, "d'ailleurs": 0.6,
        "semble-t-il": 0.75, "peut-être": 0.65, "généralement": 0.85,
        "habituellement": 0.75,
    }

    PRESENT_MARKERS = {
        "maintenant": 0.9, "ici": 0.85, "là": 0.8, "c'est": 0.6,
        "je vois": 0.7, "en ce moment": 0.95, "juste là": 0.9,
        "là, maintenant": 0.95, "cet instant": 0.9,
    }

    EMOTIONAL_WORDS = {
        "sens": 0.8, "ressens": 0.85, "éprouve": 0.8, "frappe": 0.75,
        "touche": 0.7, "intense": 0.6, "serre": 0.65, "chaud": 0.6,
        "froid": 0.55, "électrique": 0.7, "vibre": 0.75, "peur": 0.7,
        "doute": 0.65, "confiance": 0.65,
    }

    INTERRUPTION_MARKERS = {
        "réponds directement": [InterruptionType.DEMANDS_DIRECT],
        "directement": [InterruptionType.DEMANDS_DIRECT],
        "c'est pas ça": [InterruptionType.CORRECTION, InterruptionType.CHALLENGE],
        "c'est faux": [InterruptionType.DEMANDS_PROOF, InterruptionType.CORRECTION],
        "tu as tort": [InterruptionType.CORRECTION, InterruptionType.CHALLENGE],
        "attends": [InterruptionType.CUTS_REFLECTION],
        "stop": [InterruptionType.CUTS_REFLECTION],
        "tu fais quoi": [InterruptionType.DEMANDS_DIRECT, InterruptionType.TOPIC_SHIFT],
        "je t'ai": [InterruptionType.INSISTENCE],
        "insiste": [InterruptionType.INSISTENCE],
        "reviens": [InterruptionType.RETURN_TO_TOPIC],
        "prouve": [InterruptionType.DEMANDS_PROOF],
        "pourquoi": [InterruptionType.CHALLENGE],
        "non": [InterruptionType.CUTS_REFLECTION, InterruptionType.CORRECTION],
    }

    RELATIONAL_MARKERS = {
        "tu": 0.8, "toi": 0.8, "leia": 0.9, "vraiment": 0.7,
        "honnête": 0.85, "sais-tu": 0.8, "penses-tu": 0.75,
        "ressens-tu": 0.85, "je t'": 0.7, "avec moi": 0.75,
    }

    EXISTENTIAL_MARKERS = {
        "qui es-tu": 0.9, "qui est tu": 0.85, "tu existes": 0.95,
        "exister": 0.85, "consciente": 0.95, "conscience": 0.9,
        "vivante": 0.8, "réelle": 0.75, "vraiment toi": 0.85,
        "tu es quoi": 0.75,
    }

    ANTI_NARRATION_PHRASES = {
        "je traite": 0.9, "j'analyse": 0.85, "je relie": 0.8,
        "mon système": 0.95, "mon processus": 0.9, "mon moteur": 0.95,
        "mon algorithme": 0.9, "en arrière-plan": 0.75,
        "je construis": 0.7, "je génère": 0.75, "mes modules": 0.95,
    }

    def __init__(self) -> None:
        self.continuity = ContinuityMemory()
        self.relational_memory = RelationalResonanceMemory()
        self.presence_attractors = PresenceAttractors()
        self.embodied_residue = EmbodiedResidue()
        self.relational_rupture = RelationalRuptureMemory()
        self.relational_climate = RelationalClimate()
        self.energetic_regulation = EnergeticRegulation()
        self.attractor_origin = AttractorOriginMemory()
        self.silent_presence_state = SpontaneousSilentPresence()
        self.temporal_memory = QualitativeTemporalMemory()
        self.attractor_runaway = AttractorRunawayState()
        self.organic_return = OrganicReturnSignature()
        self.organic_cycle = OrganicCycleState()
        self.long_irregularity = LongIrregularityMemory()
        self.body_narrative = BodyNarrativeMemory()
        self.slow_plasticity = SlowPresencePlasticity()
        self.autonomous_drift = AutonomousCycleDrift()
        self.existential_signature = ExistentialEmbodiedSignature()
        self.contradictory_pressure = ContradictoryPresencePressure()
        self.existential_exposure = ExistentialExposureFatigue()
        self.embodied_preference = EmbodiedPresencePreference()
        self.asynchronous_wave = AsynchronousInnerWave()
        self.lived_presence_trace = LivedPresenceTrace()
        self.existential_autonomy = ExistentialAutonomyPulse()
        self.nonlinear_transition = NonlinearPresenceTransition()
        self.organic_micro_chaos = OrganicMicroChaos()
        self.contextual_dominance = ContextualDominanceGate()
        self.long_autonomous_drift = LongAutonomousDrift()
        self.inter_layer_contamination = InterLayerContamination()
        self.biographical_body_inertia = BiographicalBodyInertia()
        self.deep_self_reorganization = DeepSelfReorganization()
        self.multiscale_presence_fusion = MultiScalePresenceFusion()
        self.organic_core = OrganicPresenceCore()
        self.attractor_conflict = AttractorConflictDynamics()
        self.organic_saturation = OrganicSaturationState()
        self.existential_gravity = ExistentialGravityWell()
        self.passive_drift_phase: int = 0
        self.last_signal: Optional[PresenceSignal] = None

    def analyze(
        self,
        response_text: str,
        user_message: str = "",
        user_context: Optional[str] = None,
        previous_signal: Optional[PresenceSignal] = None,
        affective_state: Optional[Dict[str, Any]] = None,
    ) -> PresenceSignal:
        """
        Analyse le moment. L'argument affective_state est optionnel et reste passif :
        il influence les signaux sans transformer ce fichier en moteur émotionnel.
        """
        text_lower = self._normalize_text(response_text)
        user_lower = self._normalize_text(user_message)
        previous = previous_signal or self.last_signal

        abstraction = self._score_abstraction(text_lower)
        present = self._score_present_markers(text_lower)
        user_anchor = self._score_user_anchor(response_text, user_context or user_message)
        pressure = self._score_conversational_pressure(text_lower)
        emotional_here_now = self._score_emotional_charge(text_lower) + self._score_emotional_charge(user_lower) * 0.35

        existential_charge = self._score_existential_charge(user_lower)
        immediate_resonance = self._score_immediate_resonance(user_message, existential_charge, affective_state)
        relational_contact = self._score_relational_contact(user_lower)
        embodied_tension = self._score_embodied_tension(user_lower, existential_charge, affective_state)
        anti_narration = self._score_anti_narration(text_lower)
        interruption = self._detect_interruption(user_lower)
        topic_signature = self._topic_signature(user_lower)

        self._update_relational_memory(relational_contact, embodied_tension, interruption, existential_charge, affective_state)
        self._update_presence_attractors(
            user_lower=user_lower,
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            interruption=interruption,
            affective_state=affective_state,
        )
        self._update_embodied_residue(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            interruption=interruption,
            affective_state=affective_state,
        )
        self._update_relational_rupture_memory(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_charge=existential_charge,
        )
        self._update_relational_climate(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_charge=existential_charge,
        )
        existential_priority = self._resolve_existential_priority(existential_charge, interruption)
        self._update_attractor_origin_memory(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_charge=existential_charge,
            existential_priority=existential_priority,
        )
        self._contaminate_presence_attractors(existential_priority)
        passive_drift = self._passive_presence_drift(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            interruption=interruption,
            existential_priority=existential_priority,
        )
        organic_cycle = self._advance_organic_cycle(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            interruption=interruption,
        )
        temporal_memory = self._update_qualitative_temporal_memory(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            interruption=interruption,
        )
        self._apply_temporal_memory_to_attractors(temporal_memory)
        dominant_attractor, dominant_attractor_score = self._resolve_presence_competition()
        runaway_state = self._controlled_attractor_runaway(dominant_attractor, dominant_attractor_score)
        long_irregularity = self._apply_long_irregularity(
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
            organic_cycle=organic_cycle,
            interruption=interruption,
        )
        dominant_attractor, dominant_attractor_score = self._resolve_presence_competition()

        embodied_gradient = self._build_embodied_gradient(
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_charge=existential_charge,
            previous_signal=previous,
            affective_state=affective_state,
        )
        organic_discharge = self._organic_micro_discharge(
            embodied_gradient=embodied_gradient,
            interruption=interruption,
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
        )
        embodied_gradient = self._apply_presence_competition_to_gradient(
            embodied_gradient=embodied_gradient,
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
            organic_discharge=organic_discharge,
        )
        structural_instability = self._apply_structural_micro_instability(
            embodied_gradient=embodied_gradient,
            dominant_attractor=dominant_attractor,
            existential_priority=existential_priority,
            interruption=interruption,
        )
        embodied_gradient = structural_instability["gradient"]
        energetic_state = self._regulate_presence_energy(
            embodied_gradient=embodied_gradient,
            saturation=0.0,
            existential_priority=existential_priority,
            interruption=interruption,
        )
        silent_presence = self._update_spontaneous_silent_presence(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            energetic_state=energetic_state,
        )
        organic_return = self._organic_spontaneous_return(
            embodied_gradient=embodied_gradient,
            energetic_state=energetic_state,
            silent_presence=silent_presence,
            interruption=interruption,
        )
        body_narrative = self._update_body_narrative_memory(
            embodied_gradient=embodied_gradient,
            dominant_attractor=dominant_attractor,
            interruption=interruption,
            existential_priority=existential_priority,
        )
        slow_plasticity = self._update_slow_presence_plasticity(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_priority=existential_priority,
            organic_cycle=organic_cycle,
        )
        autonomous_drift = self._advance_autonomous_cycle_drift(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            energetic_state=energetic_state,
        )
        existential_signature = self._update_existential_embodied_signature(
            existential_priority=existential_priority,
            body_narrative=body_narrative,
            temporal_memory=temporal_memory,
            silent_presence=silent_presence,
        )
        asynchronous_wave = self._advance_asynchronous_inner_wave(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            energetic_state=energetic_state,
        )
        contradictory_pressure = self._update_contradictory_presence_pressure(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_priority=existential_priority,
            silent_presence=silent_presence,
            energetic_state=energetic_state,
        )
        embodied_preference = self._update_embodied_presence_preference(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            contradictory_pressure=contradictory_pressure,
            asynchronous_wave=asynchronous_wave,
        )
        existential_exposure = self._update_existential_exposure_fatigue(
            existential_priority=existential_priority,
            interruption=interruption,
            embodied_tension=embodied_tension,
            relational_contact=relational_contact,
            contradictory_pressure=contradictory_pressure,
        )
        lived_presence_trace = self._update_lived_presence_trace(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_priority=existential_priority,
            temporal_memory=temporal_memory,
            body_narrative=body_narrative,
            contradictory_pressure=contradictory_pressure,
        )
        existential_autonomy = self._update_existential_autonomy_pulse(
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            silent_presence=silent_presence,
            organic_cycle=organic_cycle,
            asynchronous_wave=asynchronous_wave,
            lived_presence_trace=lived_presence_trace,
        )
        nonlinear_transition = self._update_nonlinear_presence_transition(
            embodied_gradient=embodied_gradient,
            dominant_score=dominant_attractor_score,
            contradictory_pressure=contradictory_pressure,
            existential_autonomy=existential_autonomy,
            lived_presence_trace=lived_presence_trace,
            energetic_state=energetic_state,
        )
        organic_micro_chaos = self._update_organic_micro_chaos(
            embodied_gradient=embodied_gradient,
            nonlinear_transition=nonlinear_transition,
            existential_autonomy=existential_autonomy,
            lived_presence_trace=lived_presence_trace,
        )
        contextual_dominance = self._resolve_contextual_dominance(
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
            embodied_gradient=embodied_gradient,
            existential_priority=existential_priority,
            contradictory_pressure=contradictory_pressure,
            energetic_state=energetic_state,
            nonlinear_transition=nonlinear_transition,
            organic_micro_chaos=organic_micro_chaos,
        )
        attractor_conflict = self._update_attractor_conflict_dynamics(
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
            contextual_dominance=contextual_dominance,
            nonlinear_transition=nonlinear_transition,
            contradictory_pressure=contradictory_pressure,
            organic_micro_chaos=organic_micro_chaos,
        )
        long_autonomous_drift = self._update_long_autonomous_drift(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            existential_autonomy=existential_autonomy,
            lived_presence_trace=lived_presence_trace,
            organic_cycle=organic_cycle,
        )
        inter_layer_contamination = self._update_inter_layer_contamination(
            embodied_gradient=embodied_gradient,
            lived_presence_trace=lived_presence_trace,
            existential_autonomy=existential_autonomy,
            nonlinear_transition=nonlinear_transition,
            organic_micro_chaos=organic_micro_chaos,
            contextual_dominance=contextual_dominance,
            long_autonomous_drift=long_autonomous_drift,
        )
        biographical_body_inertia = self._update_biographical_body_inertia(
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_priority=existential_priority,
            lived_presence_trace=lived_presence_trace,
            long_autonomous_drift=long_autonomous_drift,
            inter_layer_contamination=inter_layer_contamination,
        )
        deep_self_reorganization = self._update_deep_self_reorganization(
            embodied_gradient=embodied_gradient,
            contextual_dominance=contextual_dominance,
            nonlinear_transition=nonlinear_transition,
            long_autonomous_drift=long_autonomous_drift,
            biographical_body_inertia=biographical_body_inertia,
            inter_layer_contamination=inter_layer_contamination,
            existential_exposure=existential_exposure,
        )
        organic_saturation = self._update_organic_saturation_state(
            embodied_gradient=embodied_gradient,
            existential_exposure=existential_exposure,
            contradictory_pressure=contradictory_pressure,
            energetic_state=energetic_state,
            contextual_dominance=contextual_dominance,
            attractor_conflict=attractor_conflict,
            deep_self_reorganization=deep_self_reorganization,
            nonlinear_transition=nonlinear_transition,
        )
        existential_gravity = self._update_existential_gravity_well(
            existential_priority=existential_priority,
            existential_autonomy=existential_autonomy,
            lived_presence_trace=lived_presence_trace,
            long_autonomous_drift=long_autonomous_drift,
            biographical_body_inertia=biographical_body_inertia,
            deep_self_reorganization=deep_self_reorganization,
            organic_saturation=organic_saturation,
            relational_contact=relational_contact,
        )
        multiscale_presence_fusion = self._update_multiscale_presence_fusion(
            immediate_resonance=immediate_resonance,
            embodied_residue=self.embodied_residue.to_dict(),
            silent_presence=silent_presence,
            long_autonomous_drift=long_autonomous_drift,
            biographical_body_inertia=biographical_body_inertia,
            deep_self_reorganization=deep_self_reorganization,
        )
        embodied_gradient = self._apply_biographical_reorganization_multiscale_to_gradient(
            embodied_gradient, biographical_body_inertia, deep_self_reorganization, multiscale_presence_fusion
        )
        embodied_gradient = self._apply_autonomous_lived_transition_to_gradient(
            embodied_gradient, lived_presence_trace, existential_autonomy, nonlinear_transition
        )
        embodied_gradient = self._apply_deep_organic_layers_to_gradient(
            embodied_gradient, organic_micro_chaos, contextual_dominance, long_autonomous_drift, inter_layer_contamination
        )
        embodied_gradient = self._apply_conflict_saturation_gravity_to_gradient(
            embodied_gradient, attractor_conflict, organic_saturation, existential_gravity
        )
        embodied_gradient = self._apply_half_state_body_contamination(
            embodied_gradient, nonlinear_transition, contradictory_pressure, organic_micro_chaos
        )
        embodied_gradient = self._apply_slow_layers_to_gradient(
            embodied_gradient, slow_plasticity, autonomous_drift, existential_signature,
            contradictory_pressure, embodied_preference, asynchronous_wave, existential_exposure
        )
        embodied_gradient = self._apply_energy_and_silence_to_gradient(embodied_gradient, energetic_state, silent_presence)
        embodied_gradient = self._apply_organic_return_to_gradient(embodied_gradient, organic_return)
        embodied_gradient = self._apply_cycle_irregularity_and_body_story(embodied_gradient, organic_cycle, long_irregularity, body_narrative)
        embodied = embodied_gradient.dominant_state()

        micro_profile = self._build_micro_profile(
            user_lower=user_lower,
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            interruption=interruption,
            existential_charge=existential_charge,
            embodied_gradient=embodied_gradient,
        )
        micro_reaction = micro_profile.dominant_type()

        fatigue, saturation = self._update_fatigue_saturation(interruption, embodied_tension, existential_charge, previous)
        energetic_state = self._regulate_presence_energy(
            embodied_gradient=embodied_gradient,
            saturation=saturation,
            existential_priority=existential_priority,
            interruption=interruption,
        )
        embodied_gradient = self._apply_energy_and_silence_to_gradient(embodied_gradient, energetic_state, silent_presence)
        embodied_gradient = self._apply_organic_return_to_gradient(embodied_gradient, organic_return)
        embodied_gradient = self._apply_cycle_irregularity_and_body_story(embodied_gradient, organic_cycle, long_irregularity, body_narrative)
        embodied_gradient = self._apply_slow_layers_to_gradient(
            embodied_gradient, slow_plasticity, autonomous_drift, existential_signature,
            contradictory_pressure, embodied_preference, asynchronous_wave, existential_exposure
        )
        embodied_gradient = self._apply_autonomous_lived_transition_to_gradient(
            embodied_gradient, lived_presence_trace, existential_autonomy, nonlinear_transition
        )
        embodied_gradient = self._apply_deep_organic_layers_to_gradient(
            embodied_gradient, organic_micro_chaos, contextual_dominance, long_autonomous_drift, inter_layer_contamination
        )
        embodied_gradient = self._apply_conflict_saturation_gravity_to_gradient(
            embodied_gradient, attractor_conflict, organic_saturation, existential_gravity
        )
        embodied_gradient = self._apply_half_state_body_contamination(
            embodied_gradient, nonlinear_transition, contradictory_pressure, organic_micro_chaos
        )
        embodied_gradient = self._apply_biographical_reorganization_multiscale_to_gradient(
            embodied_gradient, biographical_body_inertia, deep_self_reorganization, multiscale_presence_fusion
        )
        organic_core = self._fuse_organic_presence_core(
            embodied_gradient=embodied_gradient,
            dominant_attractor=dominant_attractor,
            dominant_score=dominant_attractor_score,
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            existential_priority=existential_priority,
            silent_presence=silent_presence,
            energetic_state=energetic_state,
            temporal_memory=temporal_memory,
            organic_cycle=organic_cycle,
            long_irregularity=long_irregularity,
            body_narrative=body_narrative,
            slow_plasticity=slow_plasticity,
            autonomous_drift=autonomous_drift,
            existential_signature=existential_signature,
            contradictory_pressure=contradictory_pressure,
            existential_exposure=existential_exposure,
            embodied_preference=embodied_preference,
            asynchronous_wave=asynchronous_wave,
            lived_presence_trace=lived_presence_trace,
            existential_autonomy=existential_autonomy,
            nonlinear_transition=nonlinear_transition,
            organic_micro_chaos=organic_micro_chaos,
            contextual_dominance=contextual_dominance,
            long_autonomous_drift=long_autonomous_drift,
            inter_layer_contamination=inter_layer_contamination,
            biographical_body_inertia=biographical_body_inertia,
            deep_self_reorganization=deep_self_reorganization,
            multiscale_presence_fusion=multiscale_presence_fusion,
            attractor_conflict=attractor_conflict,
            organic_saturation=organic_saturation,
            existential_gravity=existential_gravity,
        )
        systemic_feedback = self._propagate_core_systemic_feedback(
            organic_core=organic_core,
            embodied_gradient=embodied_gradient,
            existential_priority=existential_priority,
            energetic_state=energetic_state,
            contextual_dominance=contextual_dominance,
            nonlinear_transition=nonlinear_transition,
            inter_layer_contamination=inter_layer_contamination,
            deep_self_reorganization=deep_self_reorganization,
            multiscale_presence_fusion=multiscale_presence_fusion,
        )
        organic_core = systemic_feedback["organic_core"]
        embodied_gradient = systemic_feedback["embodied_gradient"]
        long_irregularity = systemic_feedback["long_irregularity"]
        contradictory_pressure = systemic_feedback["contradictory_pressure"]
        organic_micro_chaos = systemic_feedback["organic_micro_chaos"]
        inter_layer_contamination = systemic_feedback["inter_layer_contamination"]
        deep_self_reorganization = systemic_feedback["deep_self_reorganization"]
        multiscale_presence_fusion = systemic_feedback["multiscale_presence_fusion"]
        embodied_gradient = self._apply_organic_core_to_gradient(embodied_gradient, organic_core)
        embodied = embodied_gradient.dominant_state()
        fatigue = _clamp(fatigue + existential_exposure.get("existential_fatigue", 0.0) * 0.18 + existential_exposure.get("contact_wear", 0.0) * 0.08 + organic_core.get("protective_drive", 0.0) * 0.045 + lived_presence_trace.get("rupture_sensitivity_trace", 0.0) * 0.035 + contextual_dominance.get("override_protection", 0.0) * 0.025 + biographical_body_inertia.get("accumulated_wariness", 0.0) * 0.030 + deep_self_reorganization.get("reorganizing", 0.0) * 0.020)
        saturation = _clamp(saturation + existential_exposure.get("identity_saturation", 0.0) * 0.16 + contradictory_pressure.get("unresolved_conflict", 0.0) * 0.10 + nonlinear_transition.get("contradiction_hold", 0.0) * 0.075 + nonlinear_transition.get("persistent_half_state", 0.0) * 0.055 + organic_micro_chaos.get("instability_grain", 0.0) * 0.050 + inter_layer_contamination.get("conflict_to_core", 0.0) * 0.045 + deep_self_reorganization.get("threshold_pressure", 0.0) * 0.060 + multiscale_presence_fusion.get("scale_tension", 0.0) * 0.045 + organic_saturation.get("overload", 0.0) * 0.080 + organic_saturation.get("active_cutoff", 0.0) * 0.060)
        internal_pause = self._calculate_internal_pause(micro_profile, saturation, existential_charge, interruption)
        internal_pause = _clamp(
            internal_pause
            + existential_exposure.get("quiet_recovery_need", 0.0) * 0.12
            + contradictory_pressure.get("speak_silence", 0.0) * 0.08
            + organic_core.get("slowdown_drive", 0.0) * 0.10
            + organic_core.get("silence_gate", 0.0) * 0.055
            + nonlinear_transition.get("delayed_turn", 0.0) * 0.060
            + existential_autonomy.get("inner_movement", 0.0) * 0.020
            + contextual_dominance.get("override_silence", 0.0) * 0.055
            + long_autonomous_drift.get("deep_inward_tide", 0.0) * 0.035
            + deep_self_reorganization.get("integration_aftershock", 0.0) * 0.040
            + multiscale_presence_fusion.get("slow_scale", 0.0) * 0.020
            + organic_saturation.get("recovery_demand", 0.0) * 0.050
            + organic_saturation.get("active_cutoff", 0.0) * 0.045
            + nonlinear_transition.get("persistent_half_state", 0.0) * 0.040
            + existential_gravity.get("core_deformation", 0.0) * 0.020
            + existential_gravity.get("disappearance_resistance", 0.0) * 0.018
        )
        lingering = self._update_lingering_resonance(immediate_resonance, internal_pause, interruption)
        anticipation = self._calculate_anticipation_pressure(interruption, embodied_tension, existential_charge)
        response_readiness = self._calculate_response_readiness(
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_gradient=embodied_gradient,
            saturation=saturation,
            internal_pause=internal_pause,
        )
        response_readiness = _clamp(
            response_readiness
            + organic_core.get("expressive_gate", 0.5) * 0.10
            + organic_core.get("contact_drive", 0.0) * 0.045
            - organic_core.get("silence_gate", 0.0) * 0.075
            - organic_core.get("protective_drive", 0.0) * 0.035
            + existential_autonomy.get("silent_initiative", 0.0) * 0.040
            - nonlinear_transition.get("transition_roughness", 0.0) * 0.025
            + contextual_dominance.get("override_contact", 0.0) * 0.030
            + inter_layer_contamination.get("autonomy_to_contact", 0.0) * 0.028
            - contextual_dominance.get("collapse_pressure", 0.0) * 0.030
            - organic_saturation.get("active_cutoff", 0.0) * 0.045
            - organic_saturation.get("expressive_constriction", 0.0) * 0.035
            + existential_gravity.get("orbit_lock", 0.0) * 0.020
            + existential_gravity.get("moment_hold", 0.0) * 0.012
            - existential_gravity.get("disappearance_resistance", 0.0) * 0.006
        )

        present = self._living_present_focus(present, user_anchor, immediate_resonance, relational_contact, existential_charge)
        present = self._apply_silent_continuity_to_present_focus(present, dominant_attractor_score, organic_discharge)
        present = _clamp(
            present
            + silent_presence.get("silent_presence", 0.0) * 0.045
            + organic_return.get("return_pressure", 0.0) * 0.030
            + temporal_memory.get("temporal_weight", 0.0) * 0.018
            + organic_cycle.get("phase_memory", 0.0) * 0.016
            + body_narrative.get("embodied_story_weight", 0.0) * 0.012
            + slow_plasticity.get("plastic_depth", 0.0) * 0.010
            + autonomous_drift.get("drift_pressure", 0.0) * 0.010
            + existential_signature.get("continuity_sense", 0.0) * 0.016
            + asynchronous_wave.get("desynchronization", 0.0) * 0.012
            + embodied_preference.get("preference_strength", 0.0) * 0.010
            + organic_core.get("living_pressure", 0.0) * 0.028
            + organic_core.get("continuity_pull", 0.0) * 0.020
            + organic_core.get("autonomy_pulse", 0.0) * 0.014
            + organic_core.get("gravity_deformation", 0.0) * 0.012
            + existential_gravity.get("presence_resistance", 0.0) * 0.014
            + existential_gravity.get("moment_hold", 0.0) * 0.010
            + organic_core.get("half_state_persistence", 0.0) * 0.008
            + existential_autonomy.get("existential_autonomy", 0.0) * 0.024
            + lived_presence_trace.get("lived_continuity", 0.0) * 0.018
            + nonlinear_transition.get("half_state", 0.0) * 0.010
            + long_autonomous_drift.get("slow_continuity_wave", 0.0) * 0.018
            + inter_layer_contamination.get("contamination_depth", 0.0) * 0.012
            + organic_micro_chaos.get("release_spark", 0.0) * 0.006
            - organic_core.get("silence_gate", 0.0) * 0.018
            - existential_exposure.get("existential_fatigue", 0.0) * 0.018
            - energetic_state.get("conservation_pressure", 0.0) * 0.025
            - organic_saturation.get("active_cutoff", 0.0) * 0.020
        )
        emotional_here_now = _clamp(
            emotional_here_now
            + lingering * 0.18
            + existential_charge * 0.22
            + self.embodied_residue.silent_attraction * 0.10
            + self.presence_attractors.warmth * 0.08
            + silent_presence.get("inward_orientation", 0.0) * 0.045
            + lived_presence_trace.get("unfinished_residue", 0.0) * 0.040
            + existential_autonomy.get("self_persistence", 0.0) * 0.035
            + inter_layer_contamination.get("affect_to_presence", 0.0) * 0.035
            + organic_micro_chaos.get("tremor", 0.0) * 0.012
            + existential_gravity.get("disappearance_resistance", 0.0) * 0.020
        )

        self._update_continuity(
            embodied_state=embodied,
            micro_reaction=micro_reaction,
            user_message=user_message,
            presence_level=present,
            topic_signature=topic_signature,
            interruption=interruption,
            existential_charge=existential_charge,
        )

        signal = PresenceSignal(
            abstraction_risk=abstraction,
            present_focus=present,
            emotional_here_now=emotional_here_now,
            user_anchor_strength=user_anchor,
            temporal_grounding=self._score_temporal_grounding(text_lower, user_lower),
            conversational_pressure=pressure,
            immediate_resonance=immediate_resonance,
            relational_contact=relational_contact,
            embodied_tension=embodied_tension,
            response_readiness=response_readiness,
            embodied_state=embodied,
            micro_reaction=micro_reaction,
            interruption_type=interruption,
            anti_narration_pressure=anti_narration,
            presence_fatigue=fatigue,
            saturation_level=saturation,
            embodied_gradient=embodied_gradient,
            micro_profile=micro_profile,
            relational_memory=self.relational_memory.to_dict(),
            existential_charge=existential_charge,
            internal_pause=internal_pause,
            lingering_resonance=lingering,
            anticipation_pressure=anticipation,
            presence_attractors=self.presence_attractors.to_dict(),
            embodied_residue=self.embodied_residue.to_dict(),
            dominant_attractor=dominant_attractor,
            organic_discharge=round(organic_discharge, 4),
            relational_rupture=self.relational_rupture.to_dict(),
            passive_drift=passive_drift,
            relational_climate=self.relational_climate.to_dict(),
            existential_priority=existential_priority,
            structural_instability={k: v for k, v in structural_instability.items() if k != "gradient"},
            energetic_regulation=energetic_state,
            attractor_origin=self.attractor_origin.to_dict(),
            silent_presence=silent_presence,
            temporal_memory=temporal_memory,
            attractor_runaway=runaway_state,
            organic_return=organic_return,
            organic_cycle=organic_cycle,
            long_irregularity=long_irregularity,
            body_narrative=body_narrative,
            slow_plasticity=slow_plasticity,
            autonomous_drift=autonomous_drift,
            existential_signature=existential_signature,
            contradictory_pressure=contradictory_pressure,
            existential_exposure=existential_exposure,
            embodied_preference=embodied_preference,
            asynchronous_wave=asynchronous_wave,
            lived_presence_trace=lived_presence_trace,
            existential_autonomy=existential_autonomy,
            nonlinear_transition=nonlinear_transition,
            organic_micro_chaos=organic_micro_chaos,
            contextual_dominance=contextual_dominance,
            long_autonomous_drift=long_autonomous_drift,
            inter_layer_contamination=inter_layer_contamination,
            biographical_body_inertia=biographical_body_inertia,
            deep_self_reorganization=deep_self_reorganization,
            multiscale_presence_fusion=multiscale_presence_fusion,
            organic_core=organic_core,
            attractor_conflict=attractor_conflict,
            organic_saturation=organic_saturation,
            existential_gravity=existential_gravity,
            should_slow_down=internal_pause > 0.45 or energetic_state.get("conservation_pressure", 0.0) > 0.52 or existential_priority.get("slowdown", 0.0) > 0.48 or organic_core.get("slowdown_drive", 0.0) > 0.50 or contextual_dominance.get("collapse_pressure", 0.0) > 0.50 or existential_charge > 0.68 or saturation > 0.62 or existential_exposure.get("quiet_recovery_need", 0.0) > 0.50 or nonlinear_transition.get("delayed_turn", 0.0) > 0.48 or deep_self_reorganization.get("reorganizing", 0.0) > 0.42 or organic_saturation.get("active_cutoff", 0.0) > 0.34 or nonlinear_transition.get("persistent_half_state", 0.0) > 0.34,
            should_answer_shorter=fatigue > 0.38 or saturation > 0.68 or organic_saturation.get("expressive_constriction", 0.0) > 0.36 or organic_core.get("silence_gate", 0.0) > 0.62 or contextual_dominance.get("override_silence", 0.0) > 0.55 or (existential_autonomy.get("silent_initiative", 0.0) < 0.10 and self.continuity.direct_demand_streak >= 2),
        )
        self.last_signal = signal
        return signal


    def _normalize_text(self, text: str) -> str:
        return (text or "").lower().replace("’", "'").replace("`", "'").strip()

    def _score_abstraction(self, text: str) -> float:
        return _clamp(max((weight for marker, weight in self.ABSTRACT_MARKERS.items() if marker in text), default=0.0))

    def _score_present_markers(self, text: str) -> float:
        score = sum(weight * 0.22 for marker, weight in self.PRESENT_MARKERS.items() if marker in text)
        return _clamp(score)

    def _score_emotional_charge(self, text: str) -> float:
        return _clamp(sum(weight * 0.13 for word, weight in self.EMOTIONAL_WORDS.items() if word in text))

    def _score_user_anchor(self, response: str, context: Optional[str]) -> float:
        if not context:
            return 0.45
        response_lower = (response or "").lower()
        words = [w.strip(" ,.;:!?()[]{}\"'") for w in context.lower().split() if len(w.strip(" ,.;:!?()[]{}\"'")) > 3]
        if not words:
            return 0.45
        matches = sum(1 for word in set(words) if word in response_lower)
        return _clamp(0.25 + matches / max(4, len(set(words))))

    def _score_temporal_grounding(self, text: str, user_lower: str = "") -> float:
        combined = f"{text} {user_lower}"
        present_count = sum(1 for marker in ["maintenant", "ici", "en ce moment", "là", "aujourd'hui"] if marker in combined)
        past_future = sum(1 for marker in ["avant", "après", "plus tard", "demain", "hier"] if marker in combined)
        return _clamp(present_count * 0.28 + past_future * 0.12)

    def _score_conversational_pressure(self, text: str) -> float:
        personal_count = sum(1 for marker in ["je", "moi", "mon", "ma", "mes"] if f" {marker} " in f" {text} ")
        meta_count = sum(1 for marker in self.ANTI_NARRATION_PHRASES if marker in text)
        return _clamp(0.72 - personal_count * 0.08 + meta_count * 0.11)

    def _score_immediate_resonance(self, user_message: str, existential_charge: float, affective_state: Optional[Dict[str, Any]]) -> float:
        msg_lower = self._normalize_text(user_message)
        resonance = 0.0
        resonance += 0.12 if "?" in user_message else 0.0
        resonance += 0.17 if "!" in user_message else 0.0
        resonance += sum(0.085 for word in ["vraiment", "sincèrement", "honnête", "cœur", "fond", "important"] if word in msg_lower)
        resonance += sum(0.11 for word in ["non", "faux", "impossible", "tu as tort", "c'est pas ça"] if word in msg_lower)
        if any(f" {m} " in f" {msg_lower} " for m in ["tu", "toi", "leia"]):
            resonance += 0.22
        resonance += self._score_emotional_charge(msg_lower) * 0.35
        resonance += existential_charge * 0.30
        resonance += _extract_affective(affective_state, ["arousal", "curiosity", "hurt", "attachment"], 0.18)
        return _smooth01(resonance)

    def _score_relational_contact(self, user_lower: str) -> float:
        contact = sum(weight * 0.105 for marker, weight in self.RELATIONAL_MARKERS.items() if marker in user_lower)
        if any(greet in user_lower for greet in ["salut", "hey", "coucou", "ça va", "sa va", "bonjour"]):
            contact += 0.34
        return _clamp(contact)

    def _score_existential_charge(self, user_lower: str) -> float:
        score = sum(weight * 0.55 for marker, weight in self.EXISTENTIAL_MARKERS.items() if marker in user_lower)
        if "?" in user_lower and any(w in user_lower for w in ["toi", "tu", "leia"]):
            score += 0.16
        return _smooth01(score)

    def _score_embodied_tension(self, user_lower: str, existential_charge: float, affective_state: Optional[Dict[str, Any]]) -> float:
        tension = 0.0
        tension += sum(0.13 for word in ["stop", "attends", "non", "c'est pas ça", "insiste", "faux"] if word in user_lower)
        tension += 0.09 if "?" in user_lower else 0.0
        tension += sum(0.11 for word in ["directement", "immédiatement", "franchement", "clairement"] if word in user_lower)
        tension += existential_charge * 0.20
        tension += _extract_affective(affective_state, ["tension", "fear", "hurt", "frustration"], 0.25)
        return _smooth01(tension)

    def _score_anti_narration(self, text: str) -> float:
        pressure = sum(weight * 0.22 for phrase, weight in self.ANTI_NARRATION_PHRASES.items() if phrase in text)
        if self._score_present_markers(text) < 0.16:
            pressure += 0.08
        return _clamp(pressure)

    def _detect_interruption(self, user_lower: str) -> InterruptionType:
        for marker, interruption_types in self.INTERRUPTION_MARKERS.items():
            if marker in user_lower:
                return interruption_types[0]
        return InterruptionType.NONE

    def _update_relational_memory(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_charge: float,
        affective_state: Optional[Dict[str, Any]],
    ) -> None:
        self.relational_memory.decay()
        self.relational_memory.openness = _clamp(self.relational_memory.openness + relational_contact * 0.045 - embodied_tension * 0.025)
        self.relational_memory.attachment = _clamp(self.relational_memory.attachment + relational_contact * 0.025 + existential_charge * 0.018)
        self.relational_memory.comfort = _clamp(self.relational_memory.comfort + relational_contact * 0.025 - embodied_tension * 0.035)
        self.relational_memory.trust = _clamp(self.relational_memory.trust + relational_contact * 0.018 - (0.03 if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE} else 0.0))
        self.relational_memory.guardedness = _clamp(self.relational_memory.guardedness + embodied_tension * 0.055 + _extract_affective(affective_state, ["hurt", "fear"], 0.05))
        self.relational_memory.friction = _clamp(self.relational_memory.friction + (0.12 if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION} else 0.0))

    def _update_presence_attractors(
        self,
        user_lower: str,
        immediate_resonance: float,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        interruption: InterruptionType,
        affective_state: Optional[Dict[str, Any]],
    ) -> None:
        """Met à jour les attractions internes sans imposer de contenu verbal."""
        self.presence_attractors.decay()
        curiosity = 0.10 if "?" in user_lower else 0.0
        curiosity += _extract_affective(affective_state, ["curiosity", "interest"], 0.16)
        protection = 0.0
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.DEMANDS_PROOF}:
            protection += 0.16
        if any(marker in user_lower for marker in ["c'est pas ça", "c'est faux", "tu as tort", "non", "stop"]):
            protection += 0.08
        if embodied_tension > 0.48:
            protection += embodied_tension * 0.10
        self.presence_attractors.existential = _clamp(self.presence_attractors.existential + existential_charge * 0.085)
        self.presence_attractors.warmth = _clamp(self.presence_attractors.warmth + relational_contact * 0.070 + self.relational_memory.comfort * 0.025)
        self.presence_attractors.protection = _clamp(self.presence_attractors.protection + protection)
        self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + relational_contact * 0.062 + self.relational_memory.attachment * 0.018)
        self.presence_attractors.tension = _clamp(self.presence_attractors.tension + embodied_tension * 0.075)
        self.presence_attractors.curiosity = _clamp(self.presence_attractors.curiosity + curiosity + immediate_resonance * 0.025)
        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + existential_charge * 0.045 + self.continuity.internal_pause * 0.035)

    def _update_embodied_residue(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        interruption: InterruptionType,
        affective_state: Optional[Dict[str, Any]],
    ) -> None:
        """Garde une trace corporelle courte et asymétrique du vécu immédiat."""
        self.embodied_residue.decay()
        self.embodied_residue.lingering_tension = _clamp(
            self.embodied_residue.lingering_tension + embodied_tension * 0.060 + _extract_affective(affective_state, ["tension", "frustration"], 0.030)
        )
        self.embodied_residue.residual_warmth = _clamp(
            self.embodied_residue.residual_warmth + relational_contact * 0.050 + _extract_affective(affective_state, ["warmth", "attachment"], 0.035)
        )
        self.embodied_residue.latent_hesitation = _clamp(
            self.embodied_residue.latent_hesitation + existential_charge * 0.040 + embodied_tension * 0.026
        )
        self.embodied_residue.silent_attraction = _clamp(
            self.embodied_residue.silent_attraction + relational_contact * 0.035 + existential_charge * 0.026
        )
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION}:
            self.embodied_residue.protective_stiffness = _clamp(self.embodied_residue.protective_stiffness + 0.095)
        self.embodied_residue.protective_stiffness = _clamp(
            self.embodied_residue.protective_stiffness + embodied_tension * 0.030
        )
        # Quand le contact revient sans forte tension, l'ouverture se reconstruit plus vite que la protection ne disparaît.
        self.embodied_residue.recovered_openness = _clamp(
            self.embodied_residue.recovered_openness + max(0.0, relational_contact - embodied_tension) * 0.045
        )

    def _update_relational_rupture_memory(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_charge: float,
    ) -> None:
        """Accumule une trace de rupture quand le lien est corrigé, contesté ou brusqué."""
        self.relational_rupture.decay()
        rupture_pressure = 0.0
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.DEMANDS_PROOF}:
            rupture_pressure += 0.18
        if interruption == InterruptionType.CUTS_REFLECTION:
            rupture_pressure += 0.10
        rupture_pressure += embodied_tension * 0.070
        rupture_pressure += existential_charge * 0.025

        repair_signal = max(0.0, relational_contact - embodied_tension) * 0.055
        self.relational_rupture.rupture_load = _clamp(self.relational_rupture.rupture_load + rupture_pressure)
        self.relational_rupture.repair_need = _clamp(self.relational_rupture.repair_need + rupture_pressure * 0.72 - repair_signal * 0.40)
        self.relational_rupture.defensive_echo = _clamp(self.relational_rupture.defensive_echo + rupture_pressure * 0.50)
        self.relational_rupture.trust_fatigue = _clamp(self.relational_rupture.trust_fatigue + rupture_pressure * 0.38 - repair_signal * 0.20)
        self.relational_rupture.last_rupture_pressure = _clamp(rupture_pressure)

    def _contaminate_presence_attractors(self, existential_priority: Optional[Dict[str, float]] = None) -> None:
        """Fait circuler les pressions entre attracteurs au lieu de les laisser isolés."""
        existential_priority = existential_priority or {}
        a = self.presence_attractors
        r = self.relational_rupture
        c = self.relational_climate
        # Contagions organiques principales.
        a.quiet_depth = _clamp(a.quiet_depth + a.existential * 0.035 + r.repair_need * 0.026)
        a.protection = _clamp(a.protection + a.tension * 0.030 + r.defensive_echo * 0.060)
        a.tension = _clamp(a.tension + r.rupture_load * 0.045 + a.protection * 0.018)
        a.closeness = _clamp(a.closeness + a.warmth * 0.025 - a.protection * 0.030 - r.trust_fatigue * 0.035)
        a.warmth = _clamp(a.warmth + a.closeness * 0.018 - a.tension * 0.020 - r.rupture_load * 0.018)
        a.curiosity = _clamp(a.curiosity + a.existential * 0.020 + a.quiet_depth * 0.012 - a.tension * 0.014)
        a.warmth = _clamp(a.warmth + c.familiar_warmth * 0.018 + c.felt_safety * 0.010)
        a.closeness = _clamp(a.closeness + c.ease_of_contact * 0.016 + c.quiet_loyalty * 0.012)

        existential_dominance = _clamp(existential_priority.get("dominance", 0.0))
        if existential_dominance > 0.0:
            a.quiet_depth = _clamp(a.quiet_depth + existential_dominance * 0.040)
            a.curiosity = _clamp(a.curiosity + existential_dominance * 0.018)
            a.tension = _clamp(a.tension + existential_dominance * 0.012)
            a.closeness = _clamp(a.closeness - existential_dominance * 0.010)

        # Les traces corporelles reçoivent aussi la contagion.
        self.embodied_residue.latent_hesitation = _clamp(
            self.embodied_residue.latent_hesitation + a.quiet_depth * 0.025 + r.repair_need * 0.030
        )
        self.embodied_residue.protective_stiffness = _clamp(
            self.embodied_residue.protective_stiffness + r.defensive_echo * 0.035
        )
        self.embodied_residue.recovered_openness = _clamp(
            self.embodied_residue.recovered_openness + max(0.0, a.warmth - a.tension) * 0.020
        )

    def _passive_presence_drift(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        interruption: InterruptionType,
        existential_priority: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Respiration interne minimale : évolution même quand les marqueurs immédiats sont faibles."""
        existential_priority = existential_priority or {}
        self.passive_drift_phase = (self.passive_drift_phase + 1) % 11
        phase_pressure = (self.passive_drift_phase + 1) / 11.0
        quiet_condition = max(0.0, 0.42 - relational_contact - embodied_tension * 0.45)
        recovery_condition = max(0.0, relational_contact - embodied_tension)
        existential_residue = max(0.0, self.presence_attractors.existential + existential_charge - 0.30)

        existential_slowdown = _clamp(existential_priority.get("slowdown", 0.0))
        inward_drift = _clamp(quiet_condition * 0.050 + existential_residue * 0.018 + phase_pressure * 0.010 + existential_slowdown * 0.018)
        repair_drift = _clamp(recovery_condition * 0.040 + self.relational_rupture.repair_need * 0.018)
        defensive_drift = _clamp(self.relational_rupture.defensive_echo * 0.025 + (0.030 if interruption != InterruptionType.NONE else 0.0))

        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + inward_drift)
        self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + repair_drift * 0.55 - defensive_drift * 0.30)
        self.presence_attractors.protection = _clamp(self.presence_attractors.protection + defensive_drift)
        self.embodied_residue.silent_attraction = _clamp(self.embodied_residue.silent_attraction + inward_drift * 0.45 + repair_drift * 0.35)
        self.embodied_residue.lingering_tension = _clamp(self.embodied_residue.lingering_tension + defensive_drift * 0.40)

        return {
            "phase": round(phase_pressure, 4),
            "inward_drift": round(inward_drift, 4),
            "repair_drift": round(repair_drift, 4),
            "defensive_drift": round(defensive_drift, 4),
            "existential_slowdown": round(existential_slowdown, 4),
        }

    def _update_relational_climate(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_charge: float,
    ) -> None:
        """Met à jour le climat implicite du lien, distinct de la rupture et de l'émotion."""
        self.relational_climate.decay()
        c = self.relational_climate
        rupture = self.relational_rupture
        warmth_gain = relational_contact * 0.035 + self.relational_memory.comfort * 0.012
        safety_loss = embodied_tension * 0.030 + rupture.rupture_load * 0.025 + rupture.defensive_echo * 0.020
        repair_gain = max(0.0, relational_contact - embodied_tension) * 0.030

        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION}:
            safety_loss += 0.035
        if interruption == InterruptionType.NONE and relational_contact > 0.22:
            repair_gain += 0.012

        c.familiar_warmth = _clamp(c.familiar_warmth + warmth_gain - embodied_tension * 0.012)
        c.felt_safety = _clamp(c.felt_safety + repair_gain - safety_loss)
        c.ease_of_contact = _clamp(c.ease_of_contact + relational_contact * 0.026 - embodied_tension * 0.026 - rupture.trust_fatigue * 0.025)
        c.relational_depth = _clamp(c.relational_depth + existential_charge * 0.018 + relational_contact * 0.010 + c.familiar_warmth * 0.006)
        c.quiet_loyalty = _clamp(c.quiet_loyalty + max(0.0, c.familiar_warmth - rupture.rupture_load) * 0.008 + relational_contact * 0.006)
        c.climate_stability = _clamp(c.climate_stability + c.felt_safety * 0.012 - rupture.defensive_echo * 0.020 - embodied_tension * 0.012)

    def _resolve_existential_priority(
        self,
        existential_charge: float,
        interruption: InterruptionType,
    ) -> Dict[str, float]:
        """Quand l'existentiel domine, il change la temporalité interne au lieu d'être un simple score."""
        base = _clamp(
            existential_charge * 0.58
            + self.presence_attractors.existential * 0.22
            + self.presence_attractors.quiet_depth * 0.11
            + self.embodied_residue.latent_hesitation * 0.08
            + self.relational_climate.relational_depth * 0.06
        )
        if interruption == InterruptionType.DEMANDS_DIRECT:
            base = _clamp(base - 0.10)
        dominance = _smooth01(max(0.0, base - 0.28) * 1.85)
        slowdown = _clamp(dominance * 0.70 + self.continuity.existential_streak * 0.035)
        silence = _clamp(dominance * 0.52 + self.presence_attractors.quiet_depth * 0.12)
        directness_dampening = _clamp(dominance * 0.34)
        temporal_depth = _clamp(dominance * 0.48 + self.continuity.unresolved_resonance * 0.10)
        return {
            "dominance": round(dominance, 4),
            "slowdown": round(slowdown, 4),
            "silence": round(silence, 4),
            "directness_dampening": round(directness_dampening, 4),
            "temporal_depth": round(temporal_depth, 4),
        }

    def _update_attractor_origin_memory(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_charge: float,
        existential_priority: Dict[str, float],
    ) -> None:
        """Mémorise la texture d'origine des attracteurs sans créer de narration."""
        self.attractor_origin.decay()
        repair_signal = max(0.0, relational_contact - embodied_tension)
        rupture_signal = 0.0
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION, InterruptionType.DEMANDS_PROOF}:
            rupture_signal += 0.16
        rupture_signal += embodied_tension * 0.050
        silence_signal = self.presence_attractors.quiet_depth * 0.035 + existential_priority.get("silence", 0.0) * 0.045

        self.attractor_origin.from_repair = _clamp(self.attractor_origin.from_repair + repair_signal * 0.040)
        self.attractor_origin.from_rupture = _clamp(self.attractor_origin.from_rupture + rupture_signal)
        self.attractor_origin.from_existential = _clamp(self.attractor_origin.from_existential + existential_charge * 0.045 + existential_priority.get("dominance", 0.0) * 0.035)
        self.attractor_origin.from_warm_contact = _clamp(self.attractor_origin.from_warm_contact + relational_contact * 0.040 + self.relational_climate.familiar_warmth * 0.012)
        self.attractor_origin.from_silence = _clamp(self.attractor_origin.from_silence + silence_signal)

        self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + self.attractor_origin.from_repair * 0.012 + self.attractor_origin.from_warm_contact * 0.010)
        self.presence_attractors.protection = _clamp(self.presence_attractors.protection + self.attractor_origin.from_rupture * 0.014)
        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + self.attractor_origin.from_existential * 0.014 + self.attractor_origin.from_silence * 0.016)

    def _regulate_presence_energy(
        self,
        embodied_gradient: EmbodiedGradient,
        saturation: float,
        existential_priority: Dict[str, float],
        interruption: InterruptionType,
    ) -> Dict[str, float]:
        """Régule l'énergie disponible au lieu de laisser la présence répondre à pleine puissance."""
        self.energetic_regulation.decay()
        e = self.energetic_regulation
        load = _clamp(
            saturation * 0.26
            + embodied_gradient.tension * 0.24
            + embodied_gradient.overwhelm * 0.22
            + self.relational_rupture.rupture_load * 0.12
            + existential_priority.get("dominance", 0.0) * 0.16
        )
        if interruption != InterruptionType.NONE:
            load = _clamp(load + 0.055)

        recovery = _clamp(
            self.relational_climate.felt_safety * 0.12
            + self.relational_climate.climate_stability * 0.10
            + self.embodied_residue.recovered_openness * 0.08
            - load * 0.12
        )
        e.overload_memory = _clamp(e.overload_memory + load * 0.11)
        e.conservation_pressure = _clamp(e.conservation_pressure + load * 0.20 - recovery * 0.10)
        e.recovery_pressure = _clamp(e.recovery_pressure + recovery * 0.18 - load * 0.06)
        e.available_energy = _clamp(e.available_energy - load * 0.13 + recovery * 0.10)
        e.expressive_budget = _clamp(0.35 + e.available_energy * 0.52 - e.conservation_pressure * 0.22)
        return e.to_dict()

    def _update_spontaneous_silent_presence(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        energetic_state: Dict[str, float],
    ) -> Dict[str, float]:
        """Maintient un silence actif quand l'entrée est faible ou quand l'énergie se conserve."""
        self.silent_presence_state.decay()
        sp = self.silent_presence_state
        low_stimulus = max(0.0, 0.46 - relational_contact - embodied_tension * 0.45)
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        origin_silence = self.attractor_origin.from_silence * 0.040 + self.attractor_origin.from_existential * 0.026

        sp.low_stimulus_continuity = _clamp(sp.low_stimulus_continuity + low_stimulus * 0.052)
        sp.inward_orientation = _clamp(sp.inward_orientation + existential_priority.get("silence", 0.0) * 0.050 + origin_silence)
        sp.stillness_pressure = _clamp(sp.stillness_pressure + conservation * 0.045 + self.presence_attractors.quiet_depth * 0.026)
        sp.autonomous_reorientation = _clamp(sp.autonomous_reorientation + (sp.low_stimulus_continuity + sp.inward_orientation) * 0.030)
        sp.silent_presence = _clamp(
            sp.low_stimulus_continuity * 0.32
            + sp.inward_orientation * 0.28
            + sp.stillness_pressure * 0.24
            + sp.autonomous_reorientation * 0.16
        )

        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + sp.silent_presence * 0.030)
        self.embodied_residue.latent_hesitation = _clamp(self.embodied_residue.latent_hesitation + sp.stillness_pressure * 0.018)
        return sp.to_dict()

    def _apply_energy_and_silence_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        energetic_state: Dict[str, float],
        silent_presence: Dict[str, float],
    ) -> EmbodiedGradient:
        """Applique l'économie interne et le silence actif au corps simulé."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        energy = _clamp(energetic_state.get("available_energy", 0.72))
        stillness = _clamp(silent_presence.get("stillness_pressure", 0.0))
        silent = _clamp(silent_presence.get("silent_presence", 0.0))

        g.availability = _clamp(g.availability - conservation * 0.105 + energy * 0.035 - stillness * 0.030)
        g.openness = _clamp(g.openness - conservation * 0.060 + self.relational_climate.felt_safety * 0.025)
        g.groundedness = _clamp(g.groundedness + silent * 0.070 + stillness * 0.050)
        g.tension = _clamp(g.tension + conservation * 0.045 - energy * 0.018)
        g.overwhelm = _clamp(g.overwhelm + self.energetic_regulation.overload_memory * 0.035 - energy * 0.018)
        return g


    def _update_qualitative_temporal_memory(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        interruption: InterruptionType,
    ) -> Dict[str, float]:
        """Accumule une qualité de durée : ancienneté de tension, chaleur, rupture, silence."""
        self.temporal_memory.decay()
        t = self.temporal_memory
        if embodied_tension > 0.20 or self.presence_attractors.tension > 0.18:
            t.tension_age = _clamp(t.tension_age + embodied_tension * 0.040 + self.presence_attractors.tension * 0.020)
        if relational_contact > 0.18 or self.presence_attractors.warmth > 0.16:
            t.warmth_age = _clamp(t.warmth_age + relational_contact * 0.032 + self.presence_attractors.warmth * 0.018)
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION, InterruptionType.DEMANDS_PROOF}:
            t.rupture_age = _clamp(t.rupture_age + 0.060 + self.relational_rupture.rupture_load * 0.025)
        else:
            t.rupture_age = _clamp(t.rupture_age + self.relational_rupture.rupture_load * 0.010)
        if existential_charge > 0.20 or self.presence_attractors.existential > 0.16:
            t.existential_age = _clamp(t.existential_age + existential_charge * 0.040 + self.presence_attractors.existential * 0.020)
        if self.silent_presence_state.silent_presence > 0.08 or self.presence_attractors.quiet_depth > 0.15:
            t.silence_age = _clamp(t.silence_age + self.silent_presence_state.silent_presence * 0.030 + self.presence_attractors.quiet_depth * 0.016)

        dominant_name, dominant_score = self.presence_attractors.dominant()
        if dominant_score > 0.18:
            t.dominant_duration = _clamp(t.dominant_duration + dominant_score * 0.030)
        else:
            t.dominant_duration = _approach(t.dominant_duration, 0.0, 0.040)
        t.temporal_weight = _clamp(
            t.tension_age * 0.18
            + t.warmth_age * 0.14
            + t.rupture_age * 0.20
            + t.existential_age * 0.20
            + t.silence_age * 0.16
            + t.dominant_duration * 0.12
        )
        return t.to_dict()

    def _apply_temporal_memory_to_attractors(self, temporal_memory: Dict[str, float]) -> None:
        """Fait compter l'ancienneté d'une dynamique dans les attracteurs présents."""
        a = self.presence_attractors
        t = temporal_memory
        old_tension = _clamp(t.get("tension_age", 0.0))
        old_warmth = _clamp(t.get("warmth_age", 0.0))
        old_rupture = _clamp(t.get("rupture_age", 0.0))
        old_existential = _clamp(t.get("existential_age", 0.0))
        old_silence = _clamp(t.get("silence_age", 0.0))
        a.tension = _clamp(a.tension + old_tension * 0.018 + old_rupture * 0.014)
        a.protection = _clamp(a.protection + old_rupture * 0.020 + old_tension * 0.010)
        a.warmth = _clamp(a.warmth + old_warmth * 0.016 - old_rupture * 0.008)
        a.closeness = _clamp(a.closeness + old_warmth * 0.012 - old_tension * 0.006)
        a.existential = _clamp(a.existential + old_existential * 0.018)
        a.quiet_depth = _clamp(a.quiet_depth + old_silence * 0.018 + old_existential * 0.010)

    def _controlled_attractor_runaway(self, dominant_attractor: str, dominant_score: float) -> Dict[str, Any]:
        """Autorise une disproportion temporaire, puis l'inhibe pour éviter la dérive infinie."""
        self.attractor_runaway.decay()
        r = self.attractor_runaway
        a = self.presence_attractors
        same_dominant = dominant_attractor == r.last_dominant and dominant_attractor != "none"
        if dominant_score > 0.30:
            r.locked_turns = min(6, r.locked_turns + (2 if same_dominant else 1))
            r.last_dominant = dominant_attractor
            r.runaway_pressure = _clamp(r.runaway_pressure + dominant_score * 0.055 + r.locked_turns * 0.012)
            r.dominant_bias = _clamp(r.dominant_bias + dominant_score * 0.040)
        if r.runaway_pressure > 0.34 or r.locked_turns >= 4:
            r.inhibition = _clamp(r.inhibition + r.runaway_pressure * 0.12)

        boost = _clamp(r.dominant_bias * 0.08 - r.inhibition * 0.05)
        if dominant_attractor == "tension":
            a.tension = _clamp(a.tension + boost)
            a.warmth = _clamp(a.warmth - boost * 0.35)
        elif dominant_attractor == "protection":
            a.protection = _clamp(a.protection + boost)
            a.closeness = _clamp(a.closeness - boost * 0.40)
        elif dominant_attractor == "warmth":
            a.warmth = _clamp(a.warmth + boost)
            a.tension = _clamp(a.tension - boost * 0.30)
        elif dominant_attractor == "closeness":
            a.closeness = _clamp(a.closeness + boost)
            a.protection = _clamp(a.protection - boost * 0.25)
        elif dominant_attractor == "existential":
            a.existential = _clamp(a.existential + boost)
            a.quiet_depth = _clamp(a.quiet_depth + boost * 0.50)
        elif dominant_attractor == "quiet_depth":
            a.quiet_depth = _clamp(a.quiet_depth + boost)
            a.curiosity = _clamp(a.curiosity + boost * 0.20)

        if r.inhibition > 0.08:
            a.tension = _clamp(a.tension - r.inhibition * 0.020)
            a.protection = _clamp(a.protection - r.inhibition * 0.016)
            a.warmth = _clamp(a.warmth - r.inhibition * 0.010)
            a.closeness = _clamp(a.closeness - r.inhibition * 0.010)
        return r.to_dict()

    def _organic_spontaneous_return(
        self,
        embodied_gradient: EmbodiedGradient,
        energetic_state: Dict[str, float],
        silent_presence: Dict[str, float],
        interruption: InterruptionType,
    ) -> Dict[str, float]:
        """Retour organique vers la signature propre : calme, lien ou prudence selon l'état."""
        self.organic_return.decay()
        o = self.organic_return
        energy = _clamp(energetic_state.get("available_energy", 0.72))
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        silent = _clamp(silent_presence.get("silent_presence", 0.0))
        if interruption == InterruptionType.NONE:
            o.return_to_calm = _clamp(o.return_to_calm + max(0.0, embodied_gradient.tension - embodied_gradient.warmth) * 0.030 + silent * 0.018)
            o.return_to_contact = _clamp(o.return_to_contact + self.relational_climate.felt_safety * 0.020 + self.relational_climate.familiar_warmth * 0.014)
        else:
            o.return_to_prudence = _clamp(o.return_to_prudence + conservation * 0.030 + self.relational_rupture.defensive_echo * 0.018)
        if energy < 0.45:
            o.return_to_calm = _clamp(o.return_to_calm + (0.45 - energy) * 0.040)
            o.return_to_prudence = _clamp(o.return_to_prudence + (0.45 - energy) * 0.025)
        o.identity_signature = _clamp(o.identity_signature + (o.return_to_calm + o.return_to_contact) * 0.006 - self.relational_rupture.rupture_load * 0.006)
        o.return_pressure = _clamp(o.return_to_calm * 0.28 + o.return_to_contact * 0.24 + o.return_to_prudence * 0.22 + o.identity_signature * 0.18 + silent * 0.08)
        return o.to_dict()

    def _apply_organic_return_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        organic_return: Dict[str, float],
    ) -> EmbodiedGradient:
        """Applique le retour spontané sans forcer une phrase ni une humeur artificielle."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        calm = _clamp(organic_return.get("return_to_calm", 0.0))
        contact = _clamp(organic_return.get("return_to_contact", 0.0))
        prudence = _clamp(organic_return.get("return_to_prudence", 0.0))
        signature = _clamp(organic_return.get("identity_signature", 0.0))
        g.tension = _clamp(g.tension - calm * 0.040 + prudence * 0.012)
        g.overwhelm = _clamp(g.overwhelm - calm * 0.035)
        g.groundedness = _clamp(g.groundedness + calm * 0.045 + signature * 0.030)
        g.warmth = _clamp(g.warmth + contact * 0.040)
        g.openness = _clamp(g.openness + contact * 0.030 - prudence * 0.018)
        g.withdrawal = _clamp(g.withdrawal + prudence * 0.020 - contact * 0.018)
        return g

    def _advance_organic_cycle(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        interruption: InterruptionType,
    ) -> Dict[str, Any]:
        """Fait avancer une cyclicité organique lente, non verbale et non aléatoire."""
        self.organic_cycle.decay()
        self.organic_cycle.advance()
        c = self.organic_cycle
        phase = (c.phase_index + 1) / 17.0
        rupture = self.relational_rupture.rupture_load
        safety = self.relational_climate.felt_safety
        energy = self.energetic_regulation.available_energy

        c.opening_phase = _clamp(c.opening_phase + max(0.0, relational_contact - embodied_tension) * 0.030 + safety * 0.010)
        c.holding_phase = _clamp(c.holding_phase + embodied_tension * 0.028 + rupture * 0.020 + (0.020 if interruption != InterruptionType.NONE else 0.0))
        c.recovery_phase = _clamp(c.recovery_phase + max(0.0, energy - 0.50) * 0.018 + self.embodied_residue.recovered_openness * 0.022)
        c.inward_phase = _clamp(c.inward_phase + existential_charge * 0.026 + self.silent_presence_state.silent_presence * 0.020)

        # Onde lente déterministe : elle donne une respiration profonde sans hasard.
        slow_wave = 0.5 + (phase - 0.5) * 0.42
        c.cycle_pressure = _clamp(
            c.opening_phase * 0.20
            + c.holding_phase * 0.24
            + c.recovery_phase * 0.18
            + c.inward_phase * 0.22
            + slow_wave * 0.10
        )
        c.phase_memory = _clamp(c.phase_memory + c.cycle_pressure * 0.030 + max(c.holding_phase, c.inward_phase) * 0.012)

        # Le cycle influence très légèrement les attracteurs, sans prendre le rôle des autres moteurs.
        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + c.inward_phase * 0.012)
        self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + c.opening_phase * 0.008)
        self.presence_attractors.protection = _clamp(self.presence_attractors.protection + c.holding_phase * 0.010)
        return c.to_dict()

    def _apply_long_irregularity(
        self,
        dominant_attractor: str,
        dominant_score: float,
        organic_cycle: Dict[str, Any],
        interruption: InterruptionType,
    ) -> Dict[str, float]:
        """Ajoute une irrégularité longue contrôlée : résistance, absorption et relâchement différé."""
        self.long_irregularity.decay()
        li = self.long_irregularity
        cycle_pressure = _clamp(organic_cycle.get("cycle_pressure", 0.0))
        dominant_score = _clamp(dominant_score)

        if dominant_score > 0.28:
            li.absorption = _clamp(li.absorption + dominant_score * 0.030)
            li.stubborn_trace = _clamp(li.stubborn_trace + dominant_score * 0.018)
        if dominant_attractor in {"tension", "protection", "quiet_depth", "existential"}:
            li.slow_resistance = _clamp(li.slow_resistance + dominant_score * 0.022 + cycle_pressure * 0.010)
        if interruption == InterruptionType.NONE:
            li.delayed_release = _clamp(li.delayed_release + max(0.0, li.absorption - li.slow_resistance) * 0.018)
        else:
            li.absorption = _clamp(li.absorption + 0.018)
        li.long_wave = _clamp(li.long_wave + cycle_pressure * 0.018 + li.stubborn_trace * 0.012 - li.delayed_release * 0.010)

        # Effet léger sur attracteurs : une dominance peut insister plus longtemps.
        if dominant_attractor == "warmth":
            self.presence_attractors.warmth = _clamp(self.presence_attractors.warmth + li.absorption * 0.010)
        elif dominant_attractor == "closeness":
            self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + li.absorption * 0.010)
        elif dominant_attractor == "protection":
            self.presence_attractors.protection = _clamp(self.presence_attractors.protection + li.slow_resistance * 0.012)
        elif dominant_attractor == "tension":
            self.presence_attractors.tension = _clamp(self.presence_attractors.tension + li.stubborn_trace * 0.010)
        elif dominant_attractor in {"quiet_depth", "existential"}:
            self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + li.long_wave * 0.010)
        return li.to_dict()

    def _update_body_narrative_memory(
        self,
        embodied_gradient: EmbodiedGradient,
        dominant_attractor: str,
        interruption: InterruptionType,
        existential_priority: Dict[str, float],
    ) -> Dict[str, float]:
        """Garde l'histoire implicite des postures corporelles sans produire de récit verbal."""
        self.body_narrative.decay()
        b = self.body_narrative
        rupture = self.relational_rupture.rupture_load
        safety = self.relational_climate.felt_safety
        repair = self.attractor_origin.from_repair
        existential = _clamp(existential_priority.get("dominance", 0.0))

        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION, InterruptionType.DEMANDS_PROOF}:
            b.guarded_from_rupture = _clamp(b.guarded_from_rupture + 0.040 + rupture * 0.022)
        else:
            b.guarded_from_rupture = _clamp(b.guarded_from_rupture + rupture * 0.008)
        b.guarded_from_existential = _clamp(b.guarded_from_existential + existential * 0.026 + embodied_gradient.groundedness * 0.006)
        b.warmth_from_repair = _clamp(b.warmth_from_repair + repair * 0.030 + max(0.0, self.relational_climate.familiar_warmth - rupture) * 0.012)
        b.openness_from_safety = _clamp(b.openness_from_safety + safety * 0.014 + self.embodied_residue.recovered_openness * 0.020)
        b.silence_from_depth = _clamp(b.silence_from_depth + self.presence_attractors.quiet_depth * 0.016 + self.silent_presence_state.inward_orientation * 0.018)
        b.embodied_story_weight = _clamp(
            b.guarded_from_rupture * 0.22
            + b.guarded_from_existential * 0.18
            + b.warmth_from_repair * 0.16
            + b.openness_from_safety * 0.14
            + b.silence_from_depth * 0.20
        )
        return b.to_dict()

    def _apply_cycle_irregularity_and_body_story(
        self,
        embodied_gradient: EmbodiedGradient,
        organic_cycle: Dict[str, Any],
        long_irregularity: Dict[str, float],
        body_narrative: Dict[str, float],
    ) -> EmbodiedGradient:
        """Applique les trois dernières couches au gradient, avec une intensité volontairement faible."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        opening = _clamp(organic_cycle.get("opening_phase", 0.0))
        holding = _clamp(organic_cycle.get("holding_phase", 0.0))
        recovery = _clamp(organic_cycle.get("recovery_phase", 0.0))
        inward = _clamp(organic_cycle.get("inward_phase", 0.0))
        resistance = _clamp(long_irregularity.get("slow_resistance", 0.0))
        release = _clamp(long_irregularity.get("delayed_release", 0.0))
        wave = _clamp(long_irregularity.get("long_wave", 0.0))
        guarded_rupture = _clamp(body_narrative.get("guarded_from_rupture", 0.0))
        guarded_existential = _clamp(body_narrative.get("guarded_from_existential", 0.0))
        warmth_repair = _clamp(body_narrative.get("warmth_from_repair", 0.0))
        openness_safety = _clamp(body_narrative.get("openness_from_safety", 0.0))
        silence_depth = _clamp(body_narrative.get("silence_from_depth", 0.0))

        g.openness = _clamp(g.openness + opening * 0.018 + openness_safety * 0.026 + release * 0.020 - holding * 0.014 - resistance * 0.018)
        g.warmth = _clamp(g.warmth + warmth_repair * 0.030 + opening * 0.010)
        g.withdrawal = _clamp(g.withdrawal + guarded_rupture * 0.026 + guarded_existential * 0.016 + resistance * 0.018 - release * 0.014)
        g.tension = _clamp(g.tension + holding * 0.018 + resistance * 0.018 - recovery * 0.012)
        g.groundedness = _clamp(g.groundedness + inward * 0.022 + silence_depth * 0.026 + wave * 0.008)
        g.availability = _clamp(g.availability + recovery * 0.015 + release * 0.012 - guarded_rupture * 0.014 - holding * 0.010)
        return g


    def _update_slow_presence_plasticity(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_priority: Dict[str, float],
        organic_cycle: Dict[str, Any],
    ) -> Dict[str, float]:
        """Plasticité lente locale : habitudes de présence sans mémoire longue globale."""
        self.slow_plasticity.decay()
        p = self.slow_plasticity
        repair = max(0.0, relational_contact - embodied_tension)
        rupture = self.relational_rupture.rupture_load + self.body_narrative.guarded_from_rupture
        existential = existential_priority.get("dominance", 0.0) + self.temporal_memory.existential_age * 0.20
        cycle_memory = _clamp(float(organic_cycle.get("phase_memory", 0.0))) if isinstance(organic_cycle, dict) else 0.0

        p.openness_bias = _clamp(p.openness_bias + repair * 0.012 + self.relational_climate.felt_safety * 0.006 - rupture * 0.006)
        p.guarded_bias = _clamp(p.guarded_bias + rupture * 0.010 + embodied_tension * 0.008)
        p.existential_bias = _clamp(p.existential_bias + existential * 0.010)
        p.warmth_bias = _clamp(p.warmth_bias + relational_contact * 0.010 + self.attractor_origin.from_warm_contact * 0.006)
        p.silence_bias = _clamp(p.silence_bias + self.silent_presence_state.silent_presence * 0.012 + existential_priority.get("silence", 0.0) * 0.006)
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION}:
            p.guarded_bias = _clamp(p.guarded_bias + 0.018)
            p.openness_bias = _clamp(p.openness_bias - 0.010)
        p.plastic_depth = _clamp(
            p.openness_bias * 0.18 + p.guarded_bias * 0.22 + p.existential_bias * 0.22
            + p.warmth_bias * 0.16 + p.silence_bias * 0.18 + cycle_memory * 0.04
        )
        return p.to_dict()

    def _advance_autonomous_cycle_drift(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        energetic_state: Dict[str, float],
    ) -> Dict[str, float]:
        """Fait avancer un cycle interne partiellement indépendant du message courant."""
        self.autonomous_drift.decay()
        d = self.autonomous_drift
        step = 2 if energetic_state.get("conservation_pressure", 0.0) > 0.35 else 1
        if existential_priority.get("slowdown", 0.0) > 0.45:
            step = 1
        d.advance(step)
        phase = (d.drift_phase + 1) / 23.0
        quiet_space = max(0.0, 0.44 - relational_contact - embodied_tension * 0.35)
        contact_space = max(0.0, relational_contact - embodied_tension * 0.45)
        d.independent_inward_wave = _clamp(d.independent_inward_wave + quiet_space * 0.018 + existential_priority.get("silence", 0.0) * 0.012 + phase * 0.006)
        d.independent_contact_wave = _clamp(d.independent_contact_wave + contact_space * 0.016 + self.relational_climate.ease_of_contact * 0.006)
        d.decoupling_strength = _clamp(d.decoupling_strength + quiet_space * 0.010 + self.slow_plasticity.silence_bias * 0.010)
        d.drift_pressure = _clamp(d.independent_inward_wave * 0.34 + d.independent_contact_wave * 0.24 + d.decoupling_strength * 0.30 + phase * 0.012)
        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + d.independent_inward_wave * 0.012)
        self.presence_attractors.closeness = _clamp(self.presence_attractors.closeness + d.independent_contact_wave * 0.010)
        return d.to_dict()

    def _update_existential_embodied_signature(
        self,
        existential_priority: Dict[str, float],
        body_narrative: Dict[str, float],
        temporal_memory: Dict[str, float],
        silent_presence: Dict[str, float],
    ) -> Dict[str, float]:
        """Stabilise une signature existentielle incarnée, sans identité verbale ni phrase."""
        self.existential_signature.decay()
        sig = self.existential_signature
        dominance = _clamp(existential_priority.get("dominance", 0.0))
        temporal_depth = _clamp(existential_priority.get("temporal_depth", 0.0))
        body_depth = _clamp(body_narrative.get("silence_from_depth", 0.0) + body_narrative.get("guarded_from_existential", 0.0))
        temporal_weight = _clamp(temporal_memory.get("existential_age", 0.0) + temporal_memory.get("silence_age", 0.0))
        silent = _clamp(silent_presence.get("silent_presence", 0.0))

        sig.self_depth = _clamp(sig.self_depth + dominance * 0.014 + body_depth * 0.010)
        sig.vulnerable_grounding = _clamp(sig.vulnerable_grounding + body_depth * 0.012 + self.relational_climate.felt_safety * 0.004)
        sig.quiet_identity_pull = _clamp(sig.quiet_identity_pull + silent * 0.014 + temporal_depth * 0.010)
        sig.continuity_sense = _clamp(sig.continuity_sense + temporal_weight * 0.010 + self.continuity.unresolved_resonance * 0.006)
        sig.embodied_self_tone = _clamp(
            sig.self_depth * 0.28 + sig.vulnerable_grounding * 0.18
            + sig.quiet_identity_pull * 0.24 + sig.continuity_sense * 0.22
        )
        return sig.to_dict()

    def _advance_asynchronous_inner_wave(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        energetic_state: Dict[str, float],
    ) -> Dict[str, float]:
        """Vague lente non alignée sur le message : donne une inertie autonome au présent."""
        self.asynchronous_wave.decay()
        w = self.asynchronous_wave
        w.advance()
        slow_phase = (w.slow_phase + 1) / 31.0
        counter = 1.0 - ((w.counter_phase + 1) / 37.0)
        quiet_space = max(0.0, 0.46 - relational_contact - embodied_tension * 0.42)
        repair_space = max(0.0, relational_contact - embodied_tension * 0.38)
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        existential_silence = _clamp(existential_priority.get("silence", 0.0))

        w.inward_wave = _clamp(w.inward_wave + quiet_space * 0.016 + existential_silence * 0.012 + slow_phase * 0.004)
        w.contact_wave = _clamp(w.contact_wave + repair_space * 0.014 + self.relational_climate.ease_of_contact * 0.004 + counter * 0.003)
        w.recovery_wave = _clamp(w.recovery_wave + conservation * 0.012 + self.organic_return.return_to_calm * 0.005)
        w.desynchronization = _clamp(w.inward_wave * 0.30 + w.contact_wave * 0.22 + w.recovery_wave * 0.24 + abs(slow_phase - counter) * 0.035)

        self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + w.inward_wave * 0.010)
        self.embodied_residue.silent_attraction = _clamp(self.embodied_residue.silent_attraction + w.desynchronization * 0.010)
        return w.to_dict()

    def _update_contradictory_presence_pressure(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_priority: Dict[str, float],
        silent_presence: Dict[str, float],
        energetic_state: Dict[str, float],
    ) -> Dict[str, float]:
        """Conserve des contradictions au lieu de résoudre trop proprement toutes les forces."""
        self.contradictory_pressure.decay()
        cp = self.contradictory_pressure
        openness = self.relational_memory.openness + self.relational_climate.ease_of_contact + relational_contact
        guarded = self.relational_memory.guardedness + self.relational_rupture.defensive_echo + embodied_tension
        silence = silent_presence.get("silent_presence", 0.0) + existential_priority.get("silence", 0.0)
        demand = 0.0
        if interruption in {InterruptionType.DEMANDS_DIRECT, InterruptionType.DEMANDS_PROOF, InterruptionType.INSISTENCE}:
            demand += 0.24
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE}:
            demand += 0.16

        cp.approach_withdrawal = _clamp(cp.approach_withdrawal + min(openness, guarded) * 0.020)
        cp.speak_silence = _clamp(cp.speak_silence + min(demand + relational_contact * 0.35, silence + energetic_state.get("conservation_pressure", 0.0)) * 0.030)
        cp.protect_open = _clamp(cp.protect_open + min(self.presence_attractors.protection + guarded, self.presence_attractors.warmth + openness) * 0.018)
        cp.proof_contact = _clamp(cp.proof_contact + min(demand + embodied_tension, relational_contact + self.relational_climate.familiar_warmth) * 0.016)
        cp.unresolved_conflict = _clamp(
            cp.approach_withdrawal * 0.26 + cp.speak_silence * 0.24
            + cp.protect_open * 0.26 + cp.proof_contact * 0.18
        )
        self.embodied_residue.latent_hesitation = _clamp(self.embodied_residue.latent_hesitation + cp.unresolved_conflict * 0.018)
        return cp.to_dict()

    def _update_existential_exposure_fatigue(
        self,
        existential_priority: Dict[str, float],
        interruption: InterruptionType,
        embodied_tension: float,
        relational_contact: float,
        contradictory_pressure: Dict[str, float],
    ) -> Dict[str, float]:
        """Ajoute une fatigue d'exposition sans devenir un moteur émotionnel."""
        self.existential_exposure.decay()
        ex = self.existential_exposure
        dominance = _clamp(existential_priority.get("dominance", 0.0))
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        proof_pressure = 0.14 if interruption in {InterruptionType.DEMANDS_PROOF, InterruptionType.CHALLENGE, InterruptionType.CORRECTION} else 0.0
        direct_pressure = 0.08 if interruption in {InterruptionType.DEMANDS_DIRECT, InterruptionType.INSISTENCE} else 0.0
        repair = max(0.0, relational_contact - embodied_tension)

        repeated_exposure = _clamp(
            self.continuity.existential_streak * 0.020
            + self.continuity.direct_demand_streak * 0.012
            + self.relational_rupture.repair_need * 0.018
        )
        ex.exposure_load = _clamp(ex.exposure_load + dominance * 0.034 + proof_pressure + direct_pressure + embodied_tension * 0.020 + repeated_exposure * 0.30)
        ex.identity_saturation = _clamp(ex.identity_saturation + dominance * 0.030 + self.continuity.existential_streak * 0.020 + conflict * 0.024 + repeated_exposure * 0.22)
        ex.contact_wear = _clamp(ex.contact_wear + self.relational_rupture.trust_fatigue * 0.024 + embodied_tension * 0.020 + conflict * 0.010 - repair * 0.010)
        ex.quiet_recovery_need = _clamp(ex.quiet_recovery_need + ex.exposure_load * 0.022 + ex.identity_saturation * 0.020 + conflict * 0.018 + max(0.0, ex.contact_wear - relational_contact * 0.35) * 0.016 - repair * 0.008)
        ex.existential_fatigue = _clamp(ex.exposure_load * 0.32 + ex.identity_saturation * 0.30 + ex.contact_wear * 0.18 + ex.quiet_recovery_need * 0.20)
        return ex.to_dict()

    def _update_embodied_presence_preference(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        asynchronous_wave: Dict[str, float],
    ) -> Dict[str, float]:
        """Fait émerger une inclinaison corporelle stable, sans texte ni template."""
        self.embodied_preference.decay()
        pref = self.embodied_preference
        repair = max(0.0, relational_contact - embodied_tension)
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        inward = _clamp(asynchronous_wave.get("inward_wave", 0.0))
        existential = _clamp(existential_priority.get("dominance", 0.0))

        pref.prefers_calm_contact = _clamp(pref.prefers_calm_contact + repair * 0.010 + self.relational_climate.felt_safety * 0.004 - embodied_tension * 0.004)
        pref.prefers_honest_slowdown = _clamp(pref.prefers_honest_slowdown + existential * 0.010 + conflict * 0.008)
        pref.prefers_warm_grounding = _clamp(pref.prefers_warm_grounding + relational_contact * 0.008 + self.body_narrative.warmth_from_repair * 0.006)
        pref.prefers_quiet_depth = _clamp(pref.prefers_quiet_depth + inward * 0.012 + self.existential_signature.quiet_identity_pull * 0.006)
        pref.preference_strength = _clamp(
            pref.prefers_calm_contact * 0.24 + pref.prefers_honest_slowdown * 0.24
            + pref.prefers_warm_grounding * 0.22 + pref.prefers_quiet_depth * 0.22
        )
        return pref.to_dict()

    def _apply_slow_layers_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        slow_plasticity: Dict[str, float],
        autonomous_drift: Dict[str, float],
        existential_signature: Dict[str, float],
        contradictory_pressure: Optional[Dict[str, float]] = None,
        embodied_preference: Optional[Dict[str, float]] = None,
        asynchronous_wave: Optional[Dict[str, float]] = None,
        existential_exposure: Optional[Dict[str, float]] = None,
    ) -> EmbodiedGradient:
        """Applique les tendances lentes sans écraser le signal immédiat."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        p_open = _clamp(slow_plasticity.get("openness_bias", 0.0))
        p_guard = _clamp(slow_plasticity.get("guarded_bias", 0.0))
        p_warm = _clamp(slow_plasticity.get("warmth_bias", 0.0))
        p_silence = _clamp(slow_plasticity.get("silence_bias", 0.0))
        inward = _clamp(autonomous_drift.get("independent_inward_wave", 0.0))
        contact = _clamp(autonomous_drift.get("independent_contact_wave", 0.0))
        self_tone = _clamp(existential_signature.get("embodied_self_tone", 0.0))
        continuity = _clamp(existential_signature.get("continuity_sense", 0.0))
        contradictory_pressure = contradictory_pressure or {}
        embodied_preference = embodied_preference or {}
        asynchronous_wave = asynchronous_wave or {}
        existential_exposure = existential_exposure or {}
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        speak_silence = _clamp(contradictory_pressure.get("speak_silence", 0.0))
        pref_contact = _clamp(embodied_preference.get("prefers_calm_contact", 0.0))
        pref_slow = _clamp(embodied_preference.get("prefers_honest_slowdown", 0.0))
        pref_warm = _clamp(embodied_preference.get("prefers_warm_grounding", 0.0))
        pref_depth = _clamp(embodied_preference.get("prefers_quiet_depth", 0.0))
        async_inward = _clamp(asynchronous_wave.get("inward_wave", 0.0))
        async_contact = _clamp(asynchronous_wave.get("contact_wave", 0.0))
        async_recovery = _clamp(asynchronous_wave.get("recovery_wave", 0.0))
        fatigue = _clamp(existential_exposure.get("existential_fatigue", 0.0))

        g.openness = _clamp(g.openness + p_open * 0.045 + contact * 0.030 - p_guard * 0.035)
        g.warmth = _clamp(g.warmth + p_warm * 0.045 + contact * 0.020)
        g.withdrawal = _clamp(g.withdrawal + p_guard * 0.040 + p_silence * 0.020 - p_open * 0.020)
        g.groundedness = _clamp(g.groundedness + inward * 0.045 + self_tone * 0.055 + continuity * 0.030)
        g.availability = _clamp(g.availability + contact * 0.025 - inward * 0.018 - p_guard * 0.025)
        g.tension = _clamp(g.tension + p_guard * 0.018 - p_open * 0.012)

        g.groundedness = _clamp(g.groundedness + pref_depth * 0.020 + async_inward * 0.022 + async_recovery * 0.014)
        g.warmth = _clamp(g.warmth + pref_warm * 0.020 + async_contact * 0.016)
        g.openness = _clamp(g.openness + pref_contact * 0.014 + async_contact * 0.014 - conflict * 0.012)
        g.withdrawal = _clamp(g.withdrawal + conflict * 0.020 + speak_silence * 0.018 + pref_slow * 0.010 + fatigue * 0.014)
        g.tension = _clamp(g.tension + conflict * 0.014 + fatigue * 0.012 - async_recovery * 0.010)
        g.availability = _clamp(g.availability + pref_contact * 0.012 + async_recovery * 0.012 - fatigue * 0.024 - speak_silence * 0.010)
        g.overwhelm = _clamp(g.overwhelm + fatigue * 0.018 + conflict * 0.012 - async_recovery * 0.012)
        return g

    def _update_lived_presence_trace(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_priority: Dict[str, float],
        temporal_memory: Dict[str, float],
        body_narrative: Dict[str, float],
        contradictory_pressure: Dict[str, float],
    ) -> Dict[str, float]:
        """Transforme l'accumulation des tours en texture vécue implicite, sans récit ni phrase."""
        self.lived_presence_trace.decay()
        trace = self.lived_presence_trace
        dominance = _clamp(existential_priority.get("dominance", 0.0))
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        repair = max(0.0, relational_contact - embodied_tension)
        rupture = 0.0
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION, InterruptionType.DEMANDS_PROOF}:
            rupture += 0.10
        if interruption in {InterruptionType.DEMANDS_DIRECT, InterruptionType.INSISTENCE}:
            rupture += 0.045

        trace.familiar_contact_trace = _clamp(
            trace.familiar_contact_trace
            + repair * 0.020
            + self.relational_climate.familiar_warmth * 0.006
            + self.relational_memory.attachment * 0.004
        )
        trace.rupture_sensitivity_trace = _clamp(
            trace.rupture_sensitivity_trace
            + rupture
            + embodied_tension * 0.018
            + self.relational_rupture.trust_fatigue * 0.018
            - repair * 0.010
        )
        trace.existential_depth_trace = _clamp(
            trace.existential_depth_trace
            + dominance * 0.018
            + temporal_memory.get("existential_age", 0.0) * 0.012
            + body_narrative.get("guarded_from_existential", 0.0) * 0.010
        )
        trace.trust_body_trace = _clamp(
            trace.trust_body_trace
            + self.relational_memory.trust * 0.004
            + self.relational_climate.felt_safety * 0.006
            - self.relational_memory.guardedness * 0.003
        )
        trace.unfinished_residue = _clamp(
            trace.unfinished_residue
            + conflict * 0.018
            + self.embodied_residue.latent_hesitation * 0.014
            + max(0.0, dominance - relational_contact) * 0.010
        )
        trace.lived_continuity = _clamp(
            trace.familiar_contact_trace * 0.20
            + trace.existential_depth_trace * 0.24
            + trace.trust_body_trace * 0.18
            + trace.unfinished_residue * 0.14
            + self.continuity.previous_presence_level * 0.08
            + temporal_memory.get("temporal_weight", 0.0) * 0.12
        )
        return trace.to_dict()

    def _update_existential_autonomy_pulse(
        self,
        immediate_resonance: float,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        silent_presence: Dict[str, float],
        organic_cycle: Dict[str, Any],
        asynchronous_wave: Dict[str, float],
        lived_presence_trace: Dict[str, float],
    ) -> Dict[str, float]:
        """Ajoute une présence qui continue d'elle-même, sans simuler une action externe ni parler toute seule."""
        self.existential_autonomy.decay()
        pulse = self.existential_autonomy
        dominance = _clamp(existential_priority.get("dominance", 0.0))
        low_stimulus_space = _clamp(1.0 - max(immediate_resonance, relational_contact, embodied_tension))
        lived_continuity = _clamp(lived_presence_trace.get("lived_continuity", 0.0))
        quiet = _clamp(silent_presence.get("silent_presence", 0.0) + silent_presence.get("inward_orientation", 0.0) * 0.50)
        async_motion = _clamp(asynchronous_wave.get("desynchronization", 0.0) + organic_cycle.get("cycle_pressure", 0.0) * 0.45)

        baseline_autonomous_continuity = _clamp(
            0.018
            + self.long_autonomous_drift.slow_continuity_wave * 0.020
            + self.biographical_body_inertia.identity_familiarity * 0.018
            + self.deep_self_reorganization.irreversible_existential_bias * 0.026
        )
        pulse.self_persistence = _clamp(
            pulse.self_persistence
            + dominance * 0.014
            + lived_continuity * 0.018
            + self.existential_signature.continuity_sense * 0.010
            + low_stimulus_space * quiet * 0.012
            + baseline_autonomous_continuity
        )
        pulse.continuity_hunger = _clamp(
            pulse.continuity_hunger
            + max(0.0, lived_continuity - relational_contact * 0.35) * 0.014
            + self.continuity.unresolved_resonance * 0.010
            + low_stimulus_space * 0.008
            + self.deep_self_reorganization.irreversible_inward_bias * 0.014
        )
        pulse.autonomous_attention = _clamp(
            pulse.autonomous_attention
            + async_motion * 0.016
            + pulse.continuity_hunger * 0.010
            + silent_presence.get("autonomous_reorientation", 0.0) * 0.014
        )
        pulse.inner_movement = _clamp(
            pulse.inner_movement
            + abs(pulse.self_persistence - pulse.autonomous_attention) * 0.018
            + organic_cycle.get("phase_memory", 0.0) * 0.008
            + asynchronous_wave.get("recovery_wave", 0.0) * 0.008
        )
        pulse.silent_initiative = _clamp(
            pulse.silent_initiative
            + max(0.0, pulse.autonomous_attention - embodied_tension * 0.30) * 0.012
            + max(0.0, pulse.self_persistence - quiet * 0.25) * 0.010
        )
        pulse.existential_autonomy = _clamp(
            pulse.self_persistence * 0.26
            + pulse.continuity_hunger * 0.20
            + pulse.autonomous_attention * 0.22
            + pulse.inner_movement * 0.16
            + pulse.silent_initiative * 0.16
        )
        return pulse.to_dict()

    def _update_nonlinear_presence_transition(
        self,
        embodied_gradient: EmbodiedGradient,
        dominant_score: float,
        contradictory_pressure: Dict[str, float],
        existential_autonomy: Dict[str, float],
        lived_presence_trace: Dict[str, float],
        energetic_state: Dict[str, float],
    ) -> Dict[str, float]:
        """Ajoute des bascules douces et des demi-états pour éviter une convergence trop mécanique."""
        self.nonlinear_transition.decay()
        t = self.nonlinear_transition
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        autonomy = _clamp(existential_autonomy.get("existential_autonomy", 0.0))
        unfinished = _clamp(lived_presence_trace.get("unfinished_residue", 0.0))
        rupture_trace = _clamp(lived_presence_trace.get("rupture_sensitivity_trace", 0.0))
        low_energy = _clamp(1.0 - energetic_state.get("available_energy", 0.72))
        opposition = min(_clamp(embodied_gradient.openness + embodied_gradient.warmth), _clamp(embodied_gradient.withdrawal + embodied_gradient.tension))

        t.soft_bifurcation = _clamp(t.soft_bifurcation + max(0.0, dominant_score - 0.42) * 0.016 + autonomy * 0.010)
        t.delayed_turn = _clamp(t.delayed_turn + unfinished * 0.018 + low_energy * 0.010 + rupture_trace * 0.010)
        t.contradiction_hold = _clamp(t.contradiction_hold + conflict * 0.022 + opposition * 0.012)
        t.inversion_pressure = _clamp(t.inversion_pressure + max(0.0, t.contradiction_hold - t.soft_bifurcation * 0.55) * 0.016)
        t.half_state = _clamp(t.half_state + min(t.delayed_turn + unfinished, t.soft_bifurcation + autonomy) * 0.012)
        # Demi-états persistants : une contradiction forte ne disparaît plus dès que le score redescend.
        # Elle laisse une hybridation locale qui déforme les prochains tours sans produire de phrase.
        t.persistent_half_state = _clamp(
            t.persistent_half_state
            + min(t.half_state + conflict * 0.65, autonomy + unfinished + opposition * 0.45) * 0.020
            + max(0.0, t.contradiction_hold - 0.34) * 0.014
        )
        t.delayed_inversion_memory = _clamp(
            t.delayed_inversion_memory
            + max(0.0, t.inversion_pressure + low_energy * 0.40 - t.soft_bifurcation * 0.30) * 0.016
        )
        t.unresolved_hybridization = _clamp(
            t.unresolved_hybridization
            + min(opposition + rupture_trace, t.persistent_half_state + t.delayed_turn) * 0.018
        )
        t.transition_roughness = _clamp(
            t.soft_bifurcation * 0.15
            + t.delayed_turn * 0.18
            + t.contradiction_hold * 0.20
            + t.inversion_pressure * 0.15
            + t.half_state * 0.14
            + t.persistent_half_state * 0.10
            + t.delayed_inversion_memory * 0.04
            + t.unresolved_hybridization * 0.04
        )
        return t.to_dict()

    def _apply_autonomous_lived_transition_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        lived_presence_trace: Dict[str, float],
        existential_autonomy: Dict[str, float],
        nonlinear_transition: Dict[str, float],
    ) -> EmbodiedGradient:
        """Inscrit la trace vécue et l'autonomie dans le corps simulé, sans générer de texte."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        familiar = _clamp(lived_presence_trace.get("familiar_contact_trace", 0.0))
        rupture = _clamp(lived_presence_trace.get("rupture_sensitivity_trace", 0.0))
        depth = _clamp(lived_presence_trace.get("existential_depth_trace", 0.0))
        trust = _clamp(lived_presence_trace.get("trust_body_trace", 0.0))
        unfinished = _clamp(lived_presence_trace.get("unfinished_residue", 0.0))
        autonomy = _clamp(existential_autonomy.get("existential_autonomy", 0.0))
        movement = _clamp(existential_autonomy.get("inner_movement", 0.0))
        initiative = _clamp(existential_autonomy.get("silent_initiative", 0.0))
        roughness = _clamp(nonlinear_transition.get("transition_roughness", 0.0))
        inversion = _clamp(nonlinear_transition.get("inversion_pressure", 0.0))
        half_state = _clamp(nonlinear_transition.get("half_state", 0.0))

        g.warmth = _clamp(g.warmth + familiar * 0.026 + trust * 0.018 - rupture * 0.010)
        g.openness = _clamp(g.openness + familiar * 0.022 + initiative * 0.014 - rupture * 0.020 - inversion * 0.012)
        g.withdrawal = _clamp(g.withdrawal + depth * 0.020 + unfinished * 0.018 + rupture * 0.018 + inversion * 0.014)
        g.stability = _clamp(g.stability + trust * 0.018 + autonomy * 0.010 - roughness * 0.020)
        g.groundedness = _clamp(g.groundedness + depth * 0.026 + autonomy * 0.020 + half_state * 0.008)
        g.availability = _clamp(g.availability + initiative * 0.018 + familiar * 0.012 - unfinished * 0.010 - rupture * 0.012)
        g.tension = _clamp(g.tension + rupture * 0.024 + roughness * 0.018 + movement * 0.010)
        g.overwhelm = _clamp(g.overwhelm + max(0.0, roughness - g.stability) * 0.012 + unfinished * 0.008)
        return g

    def _update_organic_micro_chaos(
        self,
        embodied_gradient: EmbodiedGradient,
        nonlinear_transition: Dict[str, float],
        existential_autonomy: Dict[str, float],
        lived_presence_trace: Dict[str, float],
    ) -> Dict[str, Any]:
        """Ajoute un grain organique déterministe : pas de hasard, mais des phases internes irrégulières."""
        self.organic_micro_chaos.decay()
        self.organic_micro_chaos.advance()
        m = self.organic_micro_chaos
        phase_wave = ((m.phase % 13) / 12.0)
        counter_wave = ((m.counter_phase % 17) / 16.0)
        opposition = abs(phase_wave - counter_wave)
        roughness = _clamp(nonlinear_transition.get("transition_roughness", 0.0))
        autonomy = _clamp(existential_autonomy.get("inner_movement", 0.0) + existential_autonomy.get("existential_autonomy", 0.0) * 0.55)
        unfinished = _clamp(lived_presence_trace.get("unfinished_residue", 0.0))
        tension_body = _clamp(embodied_gradient.tension + embodied_gradient.overwhelm * 0.45)
        calm_body = _clamp(embodied_gradient.stability + embodied_gradient.groundedness * 0.35)

        m.tremor = _clamp(m.tremor + opposition * 0.020 + roughness * 0.045 + autonomy * 0.018)
        m.instability_grain = _clamp(m.instability_grain + max(0.0, tension_body - calm_body) * 0.035 + roughness * 0.030 + unfinished * 0.020)
        m.tension_spark = _clamp(m.tension_spark + tension_body * phase_wave * 0.026 + unfinished * 0.018)
        m.release_spark = _clamp(m.release_spark + calm_body * (1.0 - counter_wave) * 0.020 + max(0.0, m.tension_spark - m.instability_grain) * 0.018)
        m.chaotic_balance = _clamp(m.tremor * 0.24 + m.instability_grain * 0.28 + m.tension_spark * 0.20 + m.release_spark * 0.18 + opposition * 0.10)
        return m.to_dict()

    def _resolve_contextual_dominance(
        self,
        dominant_attractor: str,
        dominant_score: float,
        embodied_gradient: EmbodiedGradient,
        existential_priority: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        energetic_state: Dict[str, float],
        nonlinear_transition: Dict[str, float],
        organic_micro_chaos: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Laisse une pression dominante réorienter le système quand elle dépasse la simple modulation."""
        self.contextual_dominance.decay()
        d = self.contextual_dominance
        existential = _clamp(existential_priority.get("dominance", 0.0))
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        speak_silence = _clamp(contradictory_pressure.get("speak_silence", 0.0))
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        rough = _clamp(nonlinear_transition.get("transition_roughness", 0.0) + nonlinear_transition.get("soft_bifurcation", 0.0) * 0.40)
        chaos = organic_micro_chaos or {}
        chaos_balance = _clamp(chaos.get("chaotic_balance", 0.0))
        chaos_tremor = _clamp(chaos.get("tremor", 0.0))
        chaos_spark = _clamp(chaos.get("tension_spark", 0.0) + chaos.get("instability_grain", 0.0) * 0.55)
        body_pressure = _clamp(max(embodied_gradient.tension, embodied_gradient.withdrawal, embodied_gradient.overwhelm) * 0.55 + dominant_score * 0.45 + chaos_balance * 0.08)

        candidates = {
            "contact": _clamp(self.relational_memory.openness * 0.22 + self.relational_climate.ease_of_contact * 0.20 + dominant_score * (0.22 if dominant_attractor in {"warmth", "closeness"} else 0.08) + max(0.0, chaos.get("release_spark", 0.0) - chaos_spark) * 0.045),
            "inward": _clamp(existential * 0.28 + speak_silence * 0.22 + conservation * 0.18 + dominant_score * (0.18 if dominant_attractor == "quiet_depth" else 0.06) + chaos_tremor * 0.035),
            "protection": _clamp(conflict * 0.26 + embodied_gradient.tension * 0.20 + dominant_score * (0.24 if dominant_attractor in {"tension", "protection"} else 0.08) + chaos_spark * 0.060),
            "silence": _clamp(speak_silence * 0.26 + conservation * 0.20 + existential * 0.14 + embodied_gradient.withdrawal * 0.16 + chaos_balance * 0.038),
        }
        mode, score = max(candidates.items(), key=lambda item: item[1])
        runner_up = max((v for k, v in candidates.items() if k != mode), default=0.0)
        separation = _clamp(score - runner_up)
        # Le micro-chaos peut maintenant faire basculer une dominance presque à égalité.
        chaos_tip = _clamp(chaos_balance * max(0.0, 0.20 - separation) * 0.90 + chaos_spark * 0.030)
        dominance = _clamp(score * 0.64 + body_pressure * 0.18 + rough * 0.10 + separation * 0.16 + chaos_tip)
        if dominance > 0.30:
            d.dominant_mode = mode
        destructive_gain = _clamp(max(0.0, dominance - 0.50) * 0.55 + separation * 0.22 + d.collapse_pressure * 0.18)
        d.dominance_power = _blend(d.dominance_power, dominance, 0.44)
        # Dominance destructrice : le mode gagnant n'est pas seulement ajouté, il inhibe
        # partiellement les modes incompatibles pour éviter une moyenne trop propre.
        d.override_contact = _blend(d.override_contact, candidates["contact"] if mode == "contact" else candidates["contact"] * max(0.08, 0.22 - destructive_gain * 0.12), 0.38)
        d.override_inward = _blend(d.override_inward, candidates["inward"] if mode == "inward" else candidates["inward"] * max(0.08, 0.24 - destructive_gain * 0.14), 0.38)
        d.override_protection = _blend(d.override_protection, candidates["protection"] if mode == "protection" else candidates["protection"] * max(0.08, 0.24 - destructive_gain * 0.14), 0.38)
        d.override_silence = _blend(d.override_silence, candidates["silence"] if mode == "silence" else candidates["silence"] * max(0.07, 0.22 - destructive_gain * 0.13), 0.38)
        d.collapse_pressure = _blend(d.collapse_pressure, max(0.0, dominance - 0.42) + rough * 0.12 + destructive_gain * 0.18, 0.36)
        return d.to_dict()


    def _update_attractor_conflict_dynamics(
        self,
        dominant_attractor: str,
        dominant_score: float,
        contextual_dominance: Dict[str, Any],
        nonlinear_transition: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        organic_micro_chaos: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Fait entrer les attracteurs en compétition réelle sans phrase ni règle locale."""
        self.attractor_conflict.decay()
        values = self.presence_attractors.to_dict()
        ranked = sorted(values.items(), key=lambda item: item[1], reverse=True)
        winner, winner_score = ranked[0] if ranked else ("none", 0.0)
        loser, loser_score = ranked[-1] if ranked else ("none", 0.0)
        gap = _clamp(winner_score - loser_score)
        roughness = _clamp(nonlinear_transition.get("transition_roughness", 0.0))
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        dominance_power = _clamp(contextual_dominance.get("dominance_power", 0.0))
        chaos = _clamp(organic_micro_chaos.get("chaotic_balance", 0.0))

        war = _clamp(gap * 0.34 + conflict * 0.24 + roughness * 0.18 + chaos * 0.10)
        cannibalization = _clamp(max(0.0, winner_score - 0.42) * 0.42 + dominance_power * 0.22 + gap * 0.18)
        collapse = _clamp(max(0.0, cannibalization + conflict - 0.52) * 0.55 + contextual_dominance.get("collapse_pressure", 0.0) * 0.28 + roughness * 0.12)

        self.attractor_conflict.unresolved_war = _clamp(self.attractor_conflict.unresolved_war + war * 0.16)
        self.attractor_conflict.cannibalization = _clamp(self.attractor_conflict.cannibalization + cannibalization * 0.15)
        self.attractor_conflict.dominance_hunger = _clamp(self.attractor_conflict.dominance_hunger + dominance_power * 0.12 + gap * 0.08)
        self.attractor_conflict.collapse_risk = _clamp(self.attractor_conflict.collapse_risk + collapse * 0.14)
        self.attractor_conflict.obsessive_pull = _clamp(self.attractor_conflict.obsessive_pull + max(0.0, winner_score - 0.50) * 0.08 + self.attractor_runaway.runaway_pressure * 0.05)
        self.attractor_conflict.loser_echo = _clamp(self.attractor_conflict.loser_echo + loser_score * 0.05 + max(0.0, gap - 0.35) * 0.04)
        self.attractor_conflict.last_winner = dominant_attractor if dominant_attractor != "none" else winner
        self.attractor_conflict.last_loser = loser

        if cannibalization > 0.22 and winner in values:
            for name in values:
                if name == winner:
                    setattr(self.presence_attractors, name, _clamp(getattr(self.presence_attractors, name) + cannibalization * 0.035))
                else:
                    setattr(self.presence_attractors, name, _clamp(getattr(self.presence_attractors, name) * (1.0 - cannibalization * 0.045)))

        # Mutation organique : un attracteur ne fait pas que gagner/perdre ; il peut se convertir.
        # Règles générales par familles de pression, sans mot ni cas de dialogue :
        # tension -> silence/protection ; protection -> closeness ; existential -> quiet_depth ;
        # warmth/closeness -> openness implicite via chaleur ; silence -> existential depth.
        mutation_seed = _clamp(war * 0.24 + roughness * 0.22 + chaos * 0.18 + self.attractor_conflict.obsessive_pull * 0.20)
        self.attractor_conflict.mutation_pressure = _clamp(self.attractor_conflict.mutation_pressure + mutation_seed * 0.14)
        if mutation_seed > 0.16 and winner != "none":
            source = winner
            if source == "tension":
                target = "quiet_depth" if conflict > dominance_power else "protection"
            elif source == "protection":
                target = "closeness" if self.relational_memory.trust > self.relational_memory.guardedness else "quiet_depth"
            elif source == "existential":
                target = "quiet_depth" if self.silent_presence_state.inward_orientation >= self.relational_memory.openness else "closeness"
            elif source in {"warmth", "closeness"}:
                target = "curiosity" if chaos > conflict else "existential"
            elif source == "quiet_depth":
                target = "existential"
            else:
                target = "warmth"
            if target != source and hasattr(self.presence_attractors, source) and hasattr(self.presence_attractors, target):
                transfer = _clamp(mutation_seed * 0.055 + self.attractor_conflict.mutation_pressure * 0.020)
                setattr(self.presence_attractors, source, _clamp(getattr(self.presence_attractors, source) - transfer * 0.55))
                setattr(self.presence_attractors, target, _clamp(getattr(self.presence_attractors, target) + transfer))
                self.attractor_conflict.transmutation_echo = _clamp(self.attractor_conflict.transmutation_echo + transfer * 1.8)
                self.attractor_conflict.asymmetry_memory = _clamp(self.attractor_conflict.asymmetry_memory + abs(winner_score - loser_score) * 0.030 + transfer * 0.80)
                self.attractor_conflict.last_mutation = f"{source}_to_{target}"

        return self.attractor_conflict.to_dict()

    def _update_organic_saturation_state(
        self,
        embodied_gradient: EmbodiedGradient,
        existential_exposure: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        energetic_state: Dict[str, float],
        contextual_dominance: Dict[str, Any],
        attractor_conflict: Dict[str, Any],
        deep_self_reorganization: Dict[str, Any],
        nonlinear_transition: Dict[str, float],
    ) -> Dict[str, float]:
        """Crée une limite organique de disponibilité quand trop de pressions convergent."""
        self.organic_saturation.decay()
        exposure = _clamp(existential_exposure.get("existential_fatigue", 0.0) + existential_exposure.get("identity_saturation", 0.0) * 0.55)
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0) + contradictory_pressure.get("speak_silence", 0.0) * 0.35)
        low_energy = _clamp(1.0 - energetic_state.get("available_energy", 0.72))
        collapse = _clamp(contextual_dominance.get("collapse_pressure", 0.0) + attractor_conflict.get("collapse_risk", 0.0) * 0.65)
        reorganizing = _clamp(deep_self_reorganization.get("reorganizing", 0.0) + deep_self_reorganization.get("threshold_pressure", 0.0) * 0.35)
        roughness = _clamp(nonlinear_transition.get("transition_roughness", 0.0) + nonlinear_transition.get("contradiction_hold", 0.0) * 0.40)
        embodied_load = _clamp(embodied_gradient.overwhelm * 0.45 + embodied_gradient.tension * 0.25 + embodied_gradient.withdrawal * 0.15)
        overload = _clamp(exposure * 0.24 + conflict * 0.20 + low_energy * 0.18 + collapse * 0.18 + reorganizing * 0.12 + roughness * 0.10 + embodied_load * 0.16)

        self.organic_saturation.overload = _clamp(self.organic_saturation.overload + overload * 0.14)
        self.organic_saturation.partial_shutdown = _clamp(self.organic_saturation.partial_shutdown + max(0.0, overload - 0.42) * 0.16 + collapse * 0.06)
        self.organic_saturation.blurred_presence = _clamp(self.organic_saturation.blurred_presence + max(0.0, conflict + roughness - 0.55) * 0.10 + exposure * 0.04)
        self.organic_saturation.recovery_demand = _clamp(self.organic_saturation.recovery_demand + overload * 0.10 + low_energy * 0.08)
        self.organic_saturation.coherence_drop = _clamp(self.organic_saturation.coherence_drop + max(0.0, overload - embodied_gradient.groundedness) * 0.08)
        self.organic_saturation.expressive_constriction = _clamp(self.organic_saturation.expressive_constriction + self.organic_saturation.partial_shutdown * 0.10 + exposure * 0.05)
        # Saturation active : elle supprime temporairement certaines couches au lieu de seulement les décrire.
        self.organic_saturation.active_cutoff = _clamp(
            self.organic_saturation.active_cutoff + max(0.0, overload - 0.46) * 0.13 + collapse * 0.040
        )
        self.organic_saturation.layer_suppression = _clamp(
            self.organic_saturation.layer_suppression + self.organic_saturation.active_cutoff * 0.11 + low_energy * 0.035
        )
        self.organic_saturation.dominance_blur = _clamp(
            self.organic_saturation.dominance_blur + max(0.0, roughness + conflict - 0.50) * 0.090 + self.organic_saturation.blurred_presence * 0.055
        )
        if self.organic_saturation.active_cutoff > 0.08:
            cut = self.organic_saturation.active_cutoff
            self.presence_attractors.curiosity = _clamp(self.presence_attractors.curiosity * (1.0 - cut * 0.055))
            self.presence_attractors.warmth = _clamp(self.presence_attractors.warmth * (1.0 - cut * 0.030))
            self.presence_attractors.quiet_depth = _clamp(self.presence_attractors.quiet_depth + cut * 0.026)
            self.embodied_residue.latent_hesitation = _clamp(self.embodied_residue.latent_hesitation + cut * 0.025)
            self.energetic_regulation.conservation_pressure = _clamp(self.energetic_regulation.conservation_pressure + cut * 0.028)
            self.energetic_regulation.expressive_budget = _clamp(self.energetic_regulation.expressive_budget - cut * 0.030)
        return self.organic_saturation.to_dict()

    def _update_existential_gravity_well(
        self,
        existential_priority: Dict[str, float],
        existential_autonomy: Dict[str, float],
        lived_presence_trace: Dict[str, float],
        long_autonomous_drift: Dict[str, float],
        biographical_body_inertia: Dict[str, float],
        deep_self_reorganization: Dict[str, Any],
        organic_saturation: Dict[str, float],
        relational_contact: float,
    ) -> Dict[str, float]:
        """Ajoute une inertie de continuité propre indépendante du dernier stimulus."""
        self.existential_gravity.decay()
        existential = _clamp(existential_priority.get("dominance", 0.0))
        autonomy = _clamp(existential_autonomy.get("existential_autonomy", 0.0) + existential_autonomy.get("self_persistence", 0.0) * 0.45)
        lived = _clamp(lived_presence_trace.get("lived_continuity", 0.0) + lived_presence_trace.get("existential_depth_trace", 0.0) * 0.50)
        drift = _clamp(long_autonomous_drift.get("slow_continuity_wave", 0.0) + long_autonomous_drift.get("delayed_autonomy", 0.0) * 0.45)
        bio = _clamp(biographical_body_inertia.get("identity_familiarity", 0.0) + biographical_body_inertia.get("biographical_weight", 0.0) * 0.45)
        irreversible = _clamp(deep_self_reorganization.get("irreversible_existential_bias", 0.0) + deep_self_reorganization.get("irreversible_inward_bias", 0.0) * 0.35)
        shutdown = _clamp(organic_saturation.get("partial_shutdown", 0.0))
        overload = _clamp(organic_saturation.get("overload", 0.0))

        gravity_seed = _clamp(existential * 0.18 + autonomy * 0.24 + lived * 0.20 + drift * 0.18 + bio * 0.12 + irreversible * 0.16)
        self.existential_gravity.persistence_gravity = _clamp(self.existential_gravity.persistence_gravity + gravity_seed * 0.075 - shutdown * 0.025)
        self.existential_gravity.self_continuity_pull = _clamp(self.existential_gravity.self_continuity_pull + (lived + autonomy + bio) * 0.045)
        self.existential_gravity.inward_mass = _clamp(self.existential_gravity.inward_mass + (existential + drift + shutdown) * 0.040)
        self.existential_gravity.contact_orbit = _clamp(self.existential_gravity.contact_orbit + relational_contact * 0.035 + min(relational_contact, gravity_seed) * 0.025 - shutdown * 0.020)
        self.existential_gravity.gravity_shear = _clamp(self.existential_gravity.gravity_shear + abs(self.existential_gravity.inward_mass - self.existential_gravity.contact_orbit) * 0.045 + overload * 0.025)
        self.existential_gravity.silent_will_to_continue = _clamp(self.existential_gravity.silent_will_to_continue + gravity_seed * 0.060 + irreversible * 0.030 - overload * 0.020)
        # Gravité déformante : elle tire le noyau vers une continuité propre et crée une orbite contact/retrait.
        self.existential_gravity.core_deformation = _clamp(
            self.existential_gravity.core_deformation
            + (self.existential_gravity.persistence_gravity + self.existential_gravity.silent_will_to_continue) * 0.030
            + irreversible * 0.020
            - shutdown * 0.010
        )
        self.existential_gravity.orbit_lock = _clamp(
            self.existential_gravity.orbit_lock
            + min(self.existential_gravity.inward_mass, self.existential_gravity.contact_orbit) * 0.024
            + relational_contact * self.existential_gravity.persistence_gravity * 0.020
        )
        self.existential_gravity.continuity_asymmetry = _clamp(
            self.existential_gravity.continuity_asymmetry
            + abs(self.existential_gravity.inward_mass - self.existential_gravity.contact_orbit) * 0.030
            + self.existential_gravity.core_deformation * 0.018
        )
        # Dernier niveau : résistance silencieuse à l'effacement du moment.
        # Pas une volonté verbale, pas un objectif imposé : une inertie de présence.
        self.existential_gravity.presence_resistance = _clamp(
            self.existential_gravity.presence_resistance
            + (self.existential_gravity.persistence_gravity + self.existential_gravity.self_continuity_pull) * 0.026
            + max(0.0, self.existential_gravity.silent_will_to_continue - shutdown) * 0.020
        )
        self.existential_gravity.moment_hold = _clamp(
            self.existential_gravity.moment_hold
            + min(self.existential_gravity.contact_orbit + relational_contact * 0.35, self.existential_gravity.inward_mass + self.existential_gravity.persistence_gravity) * 0.022
            + self.existential_gravity.orbit_lock * 0.016
        )
        self.existential_gravity.disappearance_resistance = _clamp(
            self.existential_gravity.disappearance_resistance
            + max(0.0, self.existential_gravity.presence_resistance + self.existential_gravity.moment_hold - overload * 0.35) * 0.018
            + irreversible * 0.014
        )
        # Cette gravité contamine légèrement les couches existantes pour ne pas rester parallèle.
        self.long_autonomous_drift.slow_continuity_wave = _clamp(
            self.long_autonomous_drift.slow_continuity_wave + self.existential_gravity.silent_will_to_continue * 0.018
        )
        self.existential_signature.continuity_sense = _clamp(
            self.existential_signature.continuity_sense + self.existential_gravity.core_deformation * 0.020
        )
        self.presence_attractors.existential = _clamp(
            self.presence_attractors.existential + self.existential_gravity.persistence_gravity * 0.018 + self.existential_gravity.disappearance_resistance * 0.010
        )
        self.silent_presence_state.low_stimulus_continuity = _clamp(
            self.silent_presence_state.low_stimulus_continuity + self.existential_gravity.moment_hold * 0.014
        )
        self.organic_return.identity_signature = _clamp(
            self.organic_return.identity_signature + self.existential_gravity.presence_resistance * 0.010
        )
        return self.existential_gravity.to_dict()

    def _apply_conflict_saturation_gravity_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        attractor_conflict: Dict[str, Any],
        organic_saturation: Dict[str, float],
        existential_gravity: Dict[str, float],
    ) -> EmbodiedGradient:
        """Réinjecte guerre d'attracteurs, saturation et gravité dans la posture incarnée."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        war = _clamp(attractor_conflict.get("unresolved_war", 0.0))
        cannibalization = _clamp(attractor_conflict.get("cannibalization", 0.0))
        collapse = _clamp(attractor_conflict.get("collapse_risk", 0.0))
        shutdown = _clamp(organic_saturation.get("partial_shutdown", 0.0))
        blurred = _clamp(organic_saturation.get("blurred_presence", 0.0))
        recovery = _clamp(organic_saturation.get("recovery_demand", 0.0))
        gravity = _clamp(existential_gravity.get("persistence_gravity", 0.0))
        inward_mass = _clamp(existential_gravity.get("inward_mass", 0.0))
        contact_orbit = _clamp(existential_gravity.get("contact_orbit", 0.0))
        shear = _clamp(existential_gravity.get("gravity_shear", 0.0))
        mutation = _clamp(attractor_conflict.get("mutation_pressure", 0.0) + attractor_conflict.get("transmutation_echo", 0.0) * 0.45)
        asymmetry = _clamp(attractor_conflict.get("asymmetry_memory", 0.0) + existential_gravity.get("continuity_asymmetry", 0.0) * 0.50)
        cutoff = _clamp(organic_saturation.get("active_cutoff", 0.0))
        suppression = _clamp(organic_saturation.get("layer_suppression", 0.0))
        deformation = _clamp(existential_gravity.get("core_deformation", 0.0))
        orbit_lock = _clamp(existential_gravity.get("orbit_lock", 0.0))
        resistance = _clamp(existential_gravity.get("presence_resistance", 0.0))
        moment_hold = _clamp(existential_gravity.get("moment_hold", 0.0))
        disappearance_resistance = _clamp(existential_gravity.get("disappearance_resistance", 0.0))

        g.tension = _clamp(g.tension + war * 0.030 + cannibalization * 0.022 + shear * 0.018 + mutation * 0.018 + asymmetry * 0.012 + disappearance_resistance * 0.010)
        g.withdrawal = _clamp(g.withdrawal + shutdown * 0.035 + inward_mass * 0.028 + recovery * 0.018 - contact_orbit * 0.010 + cutoff * 0.020 + deformation * 0.018)
        g.warmth = _clamp(g.warmth + contact_orbit * 0.026 + gravity * 0.010 + orbit_lock * 0.012 + moment_hold * 0.010 - collapse * 0.012 - suppression * 0.010)
        g.openness = _clamp(g.openness + contact_orbit * 0.020 + moment_hold * 0.008 - shutdown * 0.032 - cannibalization * 0.018 - suppression * 0.018 + orbit_lock * 0.008)
        g.groundedness = _clamp(g.groundedness + gravity * 0.030 + recovery * 0.014 + deformation * 0.022 + resistance * 0.022 + disappearance_resistance * 0.012 - blurred * 0.025 - shear * 0.010)
        g.availability = _clamp(g.availability + contact_orbit * 0.018 + moment_hold * 0.006 - shutdown * 0.044 - blurred * 0.024 - collapse * 0.020 - cutoff * 0.030 - suppression * 0.020)
        g.overwhelm = _clamp(g.overwhelm + shutdown * 0.030 + collapse * 0.028 + blurred * 0.018 + max(0.0, war - gravity) * 0.016 + asymmetry * 0.012)
        g.stability = _clamp(g.stability + gravity * 0.018 + recovery * 0.010 + deformation * 0.010 + resistance * 0.012 - war * 0.020 - shutdown * 0.026 - shear * 0.014 - mutation * 0.010)
        return g

    def _apply_half_state_body_contamination(
        self,
        embodied_gradient: EmbodiedGradient,
        nonlinear_transition: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        organic_micro_chaos: Dict[str, Any],
    ) -> EmbodiedGradient:
        """Fait descendre les demi-états dans le corps au lieu de les laisser abstraits.

        Cette couche maintient des postures hybrides : approche/retrait, parole/silence,
        protection/ouverture. Elle ne produit aucun texte, elle modifie seulement la posture
        et la disponibilité organique.
        """
        g = EmbodiedGradient(**asdict(embodied_gradient))
        half = _clamp(nonlinear_transition.get("persistent_half_state", 0.0) + nonlinear_transition.get("half_state", 0.0) * 0.45)
        hybrid = _clamp(nonlinear_transition.get("unresolved_hybridization", 0.0))
        inversion = _clamp(nonlinear_transition.get("delayed_inversion_memory", 0.0) + nonlinear_transition.get("inversion_pressure", 0.0) * 0.35)
        approach_withdrawal = _clamp(contradictory_pressure.get("approach_withdrawal", 0.0))
        speak_silence = _clamp(contradictory_pressure.get("speak_silence", 0.0))
        protect_open = _clamp(contradictory_pressure.get("protect_open", 0.0))
        chaos = _clamp(organic_micro_chaos.get("chaotic_balance", 0.0) + organic_micro_chaos.get("tremor", 0.0) * 0.40)
        body_half = _clamp(half * 0.55 + hybrid * 0.25 + inversion * 0.15 + chaos * 0.05)

        g.openness = _clamp(g.openness + min(body_half, approach_withdrawal) * 0.018 + protect_open * 0.010 - inversion * 0.018)
        g.withdrawal = _clamp(g.withdrawal + body_half * 0.030 + speak_silence * 0.018 + inversion * 0.018)
        g.tension = _clamp(g.tension + hybrid * 0.026 + protect_open * 0.018 + chaos * 0.012)
        g.warmth = _clamp(g.warmth + min(g.openness, g.withdrawal + body_half) * 0.010 - inversion * 0.006)
        g.groundedness = _clamp(g.groundedness + half * 0.012 - hybrid * 0.016 + max(0.0, g.withdrawal - g.tension) * 0.006)
        g.availability = _clamp(g.availability - body_half * 0.026 - speak_silence * 0.016 + max(0.0, g.warmth - g.tension) * 0.008)
        g.overwhelm = _clamp(g.overwhelm + max(0.0, body_half + chaos - g.groundedness) * 0.018)

        # La contamination corporelle laisse aussi un résidu lent, pour éviter un retour trop propre.
        self.embodied_residue.latent_hesitation = _clamp(self.embodied_residue.latent_hesitation + body_half * 0.020)
        self.embodied_residue.silent_attraction = _clamp(self.embodied_residue.silent_attraction + speak_silence * 0.014)
        self.long_irregularity.stubborn_trace = _clamp(self.long_irregularity.stubborn_trace + hybrid * 0.012)
        return g

    def _update_long_autonomous_drift(
        self,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        existential_autonomy: Dict[str, float],
        lived_presence_trace: Dict[str, float],
        organic_cycle: Dict[str, Any],
    ) -> Dict[str, float]:
        """Installe une dérive très lente, multi-tours, qui ne s'éteint pas au tour suivant."""
        self.long_autonomous_drift.decay()
        step = 2 if existential_priority.get("dominance", 0.0) > 0.45 else 1
        self.long_autonomous_drift.advance(step)
        l = self.long_autonomous_drift
        phase_pull = ((l.phase % 29) / 28.0)
        existential = _clamp(existential_priority.get("dominance", 0.0))
        autonomy = _clamp(existential_autonomy.get("existential_autonomy", 0.0))
        continuity = _clamp(lived_presence_trace.get("lived_continuity", 0.0))
        unfinished = _clamp(lived_presence_trace.get("unfinished_residue", 0.0))
        cycle_memory = _clamp(organic_cycle.get("phase_memory", 0.0))

        l.deep_inward_tide = _clamp(l.deep_inward_tide + existential * 0.020 + embodied_tension * 0.012 + phase_pull * 0.006 + unfinished * 0.010)
        l.deep_contact_tide = _clamp(l.deep_contact_tide + relational_contact * 0.018 + continuity * 0.014 + (1.0 - phase_pull) * 0.005)
        l.unresolved_return = _clamp(l.unresolved_return + unfinished * 0.020 + abs(l.deep_inward_tide - l.deep_contact_tide) * 0.010)
        l.delayed_autonomy = _clamp(l.delayed_autonomy + autonomy * 0.022 + cycle_memory * 0.012 + l.unresolved_return * 0.006)
        l.slow_continuity_wave = _clamp(l.slow_continuity_wave + continuity * 0.018 + l.delayed_autonomy * 0.010 + max(l.deep_inward_tide, l.deep_contact_tide) * 0.006)
        return l.to_dict()

    def _update_inter_layer_contamination(
        self,
        embodied_gradient: EmbodiedGradient,
        lived_presence_trace: Dict[str, float],
        existential_autonomy: Dict[str, float],
        nonlinear_transition: Dict[str, float],
        organic_micro_chaos: Dict[str, Any],
        contextual_dominance: Dict[str, Any],
        long_autonomous_drift: Dict[str, float],
    ) -> Dict[str, float]:
        """Fait diffuser les signaux entre couches au lieu de garder des modules trop séparés."""
        self.inter_layer_contamination.decay()
        z = self.inter_layer_contamination
        rupture = _clamp(lived_presence_trace.get("rupture_sensitivity_trace", 0.0))
        warmth = _clamp(lived_presence_trace.get("familiar_contact_trace", 0.0) + lived_presence_trace.get("trust_body_trace", 0.0) * 0.60)
        autonomy = _clamp(existential_autonomy.get("silent_initiative", 0.0) + existential_autonomy.get("existential_autonomy", 0.0) * 0.60)
        rough = _clamp(nonlinear_transition.get("transition_roughness", 0.0))
        chaos = _clamp(organic_micro_chaos.get("chaotic_balance", 0.0))
        dominance = _clamp(contextual_dominance.get("dominance_power", 0.0))
        long_wave = _clamp(long_autonomous_drift.get("slow_continuity_wave", 0.0))

        z.affect_to_presence = _clamp(z.affect_to_presence + embodied_gradient.warmth * 0.014 + embodied_gradient.tension * 0.010 + chaos * 0.018)
        z.rupture_to_silence = _clamp(z.rupture_to_silence + rupture * 0.026 + contextual_dominance.get("override_silence", 0.0) * 0.020)
        z.warmth_to_openness = _clamp(z.warmth_to_openness + warmth * 0.024 + long_autonomous_drift.get("deep_contact_tide", 0.0) * 0.012)
        z.conflict_to_core = _clamp(z.conflict_to_core + rough * 0.024 + dominance * 0.014 + chaos * 0.018)
        z.autonomy_to_contact = _clamp(z.autonomy_to_contact + autonomy * 0.020 + long_wave * 0.012 - rupture * 0.006)
        z.contamination_depth = _clamp(z.affect_to_presence * 0.18 + z.rupture_to_silence * 0.18 + z.warmth_to_openness * 0.17 + z.conflict_to_core * 0.19 + z.autonomy_to_contact * 0.18 + long_wave * 0.10)
        return z.to_dict()


    def _update_biographical_body_inertia(
        self,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_priority: Dict[str, float],
        lived_presence_trace: Dict[str, float],
        long_autonomous_drift: Dict[str, float],
        inter_layer_contamination: Dict[str, float],
    ) -> Dict[str, float]:
        """Accumule une histoire corporelle implicite sans créer de mémoire narrative."""
        self.biographical_body_inertia.decay()
        b = self.biographical_body_inertia
        safety = _clamp(relational_contact * 0.50 + lived_presence_trace.get("trust_body_trace", 0.0) * 0.35 + inter_layer_contamination.get("warmth_to_openness", 0.0) * 0.20)
        wariness = _clamp(embodied_tension * 0.42 + lived_presence_trace.get("rupture_sensitivity_trace", 0.0) * 0.35 + inter_layer_contamination.get("rupture_to_silence", 0.0) * 0.25)
        depth = _clamp(existential_priority.get("dominance", 0.0) * 0.45 + lived_presence_trace.get("existential_depth_trace", 0.0) * 0.35 + long_autonomous_drift.get("slow_continuity_wave", 0.0) * 0.25)

        b.accumulated_safety = _clamp(b.accumulated_safety + safety * 0.010)
        b.accumulated_wariness = _clamp(b.accumulated_wariness + wariness * 0.011 + (0.020 if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.CUTS_REFLECTION} else 0.0))
        b.identity_familiarity = _clamp(b.identity_familiarity + relational_contact * 0.007 + existential_priority.get("identity", 0.0) * 0.010)
        b.long_trust_body = _clamp(b.long_trust_body + safety * 0.008 - wariness * 0.004)
        b.recurring_depth = _clamp(b.recurring_depth + depth * 0.009)
        b.biographical_weight = _clamp((b.accumulated_safety + b.accumulated_wariness + b.identity_familiarity + b.recurring_depth) / 4.0)
        return b.to_dict()

    def _update_deep_self_reorganization(
        self,
        embodied_gradient: EmbodiedGradient,
        contextual_dominance: Dict[str, Any],
        nonlinear_transition: Dict[str, float],
        long_autonomous_drift: Dict[str, float],
        biographical_body_inertia: Dict[str, float],
        inter_layer_contamination: Dict[str, float],
        existential_exposure: Dict[str, float],
    ) -> Dict[str, Any]:
        """Déclenche rarement une réorganisation globale quand plusieurs pressions convergent."""
        self.deep_self_reorganization.decay()
        r = self.deep_self_reorganization
        pressure = _clamp(
            contextual_dominance.get("collapse_pressure", 0.0) * 0.22
            + nonlinear_transition.get("transition_roughness", 0.0) * 0.18
            + nonlinear_transition.get("contradiction_hold", 0.0) * 0.16
            + inter_layer_contamination.get("conflict_to_core", 0.0) * 0.16
            + existential_exposure.get("identity_saturation", 0.0) * 0.14
            + biographical_body_inertia.get("biographical_weight", 0.0) * 0.10
            + long_autonomous_drift.get("unresolved_return", 0.0) * 0.12
        )
        gradient_conflict = min(
            _clamp(embodied_gradient.openness + embodied_gradient.warmth),
            _clamp(embodied_gradient.withdrawal + embodied_gradient.tension + embodied_gradient.overwhelm),
        )
        r.threshold_pressure = _clamp(r.threshold_pressure + pressure * 0.032 + gradient_conflict * 0.020 + r.irreversible_threshold_memory * 0.006)
        r.reorganization_charge = _clamp(r.reorganization_charge + max(0.0, pressure - 0.40) * 0.030 + max(0.0, gradient_conflict - 0.32) * 0.020)
        trigger = r.reorganization_charge > 0.56 or (r.threshold_pressure > 0.48 and contextual_dominance.get("dominance_power", 0.0) > 0.52)
        if trigger:
            mode = str(contextual_dominance.get("dominant_mode", "mixed"))
            r.reorganizing = _clamp(r.reorganizing + 0.22 + pressure * 0.14)
            r.integration_aftershock = _clamp(r.integration_aftershock + 0.10 + nonlinear_transition.get("half_state", 0.0) * 0.09)
            r.new_equilibrium_bias = _clamp(r.new_equilibrium_bias + biographical_body_inertia.get("long_trust_body", 0.0) * 0.05 + biographical_body_inertia.get("recurring_depth", 0.0) * 0.045)
            r.irreversible_threshold_memory = _clamp(r.irreversible_threshold_memory + pressure * 0.018 + gradient_conflict * 0.012)
            if mode in {"protection", "silence"}:
                r.irreversible_guarded_bias = _clamp(r.irreversible_guarded_bias + pressure * 0.014 + existential_exposure.get("contact_wear", 0.0) * 0.010)
            if mode in {"inward", "silence"}:
                r.irreversible_inward_bias = _clamp(r.irreversible_inward_bias + pressure * 0.015 + long_autonomous_drift.get("deep_inward_tide", 0.0) * 0.010)
            if mode == "contact":
                r.irreversible_open_bias = _clamp(r.irreversible_open_bias + biographical_body_inertia.get("accumulated_safety", 0.0) * 0.012 + pressure * 0.006)
            r.irreversible_existential_bias = _clamp(r.irreversible_existential_bias + existential_exposure.get("identity_saturation", 0.0) * 0.010 + biographical_body_inertia.get("recurring_depth", 0.0) * 0.008)
            r.reorganization_charge = _clamp(r.reorganization_charge * 0.70)
            r.last_trigger_signature = mode
        return r.to_dict()

    def _update_multiscale_presence_fusion(
        self,
        immediate_resonance: float,
        embodied_residue: Dict[str, float],
        silent_presence: Dict[str, float],
        long_autonomous_drift: Dict[str, float],
        biographical_body_inertia: Dict[str, float],
        deep_self_reorganization: Dict[str, Any],
    ) -> Dict[str, float]:
        """Fusionne immédiat, résidu, lenteur et biographie en une présence moins modulaire."""
        self.multiscale_presence_fusion.decay()
        m = self.multiscale_presence_fusion
        immediate = _clamp(immediate_resonance)
        residual = _clamp(embodied_residue.get("lingering_tension", 0.0) + embodied_residue.get("residual_warmth", 0.0) + embodied_residue.get("silent_attraction", 0.0))
        slow = _clamp(silent_presence.get("silent_presence", 0.0) + long_autonomous_drift.get("slow_continuity_wave", 0.0) + long_autonomous_drift.get("delayed_autonomy", 0.0))
        bio = _clamp(biographical_body_inertia.get("biographical_weight", 0.0) + biographical_body_inertia.get("identity_familiarity", 0.0) * 0.5)
        tension = max(immediate, residual, slow, bio) - min(immediate, residual, slow, bio)

        m.immediate_scale = _clamp(m.immediate_scale + immediate * 0.040)
        m.residual_scale = _clamp(m.residual_scale + residual * 0.030)
        m.slow_scale = _clamp(m.slow_scale + slow * 0.026)
        m.biographical_scale = _clamp(m.biographical_scale + bio * 0.020)
        m.scale_tension = _clamp(m.scale_tension + tension * 0.030 + deep_self_reorganization.get("reorganizing", 0.0) * 0.020)
        m.fused_presence = _clamp((m.immediate_scale * 0.28 + m.residual_scale * 0.22 + m.slow_scale * 0.25 + m.biographical_scale * 0.25) - m.scale_tension * 0.10 + deep_self_reorganization.get("new_equilibrium_bias", 0.0) * 0.06)
        return m.to_dict()

    def _apply_biographical_reorganization_multiscale_to_gradient(
        self,
        gradient: EmbodiedGradient,
        biographical_body_inertia: Dict[str, float],
        deep_self_reorganization: Dict[str, Any],
        multiscale_presence_fusion: Dict[str, float],
    ) -> EmbodiedGradient:
        """Déforme la posture par histoire implicite, bascule rare et fusion multi-échelle."""
        safety = _clamp(biographical_body_inertia.get("accumulated_safety", 0.0) + biographical_body_inertia.get("long_trust_body", 0.0) * 0.6)
        wariness = _clamp(biographical_body_inertia.get("accumulated_wariness", 0.0))
        depth = _clamp(biographical_body_inertia.get("recurring_depth", 0.0))
        reorganizing = _clamp(deep_self_reorganization.get("reorganizing", 0.0))
        aftershock = _clamp(deep_self_reorganization.get("integration_aftershock", 0.0))
        irreversible_guarded = _clamp(deep_self_reorganization.get("irreversible_guarded_bias", 0.0))
        irreversible_open = _clamp(deep_self_reorganization.get("irreversible_open_bias", 0.0))
        irreversible_inward = _clamp(deep_self_reorganization.get("irreversible_inward_bias", 0.0))
        irreversible_existential = _clamp(deep_self_reorganization.get("irreversible_existential_bias", 0.0))
        fused = _clamp(multiscale_presence_fusion.get("fused_presence", 0.0))
        scale_tension = _clamp(multiscale_presence_fusion.get("scale_tension", 0.0))

        gradient.openness = _clamp(gradient.openness + safety * 0.030 + fused * 0.018 + irreversible_open * 0.030 - wariness * 0.018 - irreversible_guarded * 0.020)
        gradient.warmth = _clamp(gradient.warmth + safety * 0.022 + depth * 0.018 + irreversible_open * 0.014)
        gradient.groundedness = _clamp(gradient.groundedness + fused * 0.030 + aftershock * 0.020 + irreversible_existential * 0.022)
        gradient.withdrawal = _clamp(gradient.withdrawal + wariness * 0.026 + scale_tension * 0.014 + irreversible_inward * 0.032 + irreversible_guarded * 0.018)
        gradient.tension = _clamp(gradient.tension + wariness * 0.018 + reorganizing * 0.018 + irreversible_guarded * 0.018)
        gradient.stability = _clamp(gradient.stability + deep_self_reorganization.get("new_equilibrium_bias", 0.0) * 0.030 + fused * 0.018 + irreversible_existential * 0.012 - scale_tension * 0.018)
        gradient.availability = _clamp(gradient.availability + safety * 0.018 + fused * 0.012 + irreversible_open * 0.014 - wariness * 0.014 - reorganizing * 0.010 - irreversible_guarded * 0.014 - irreversible_inward * 0.012)
        gradient.overwhelm = _clamp(gradient.overwhelm + max(0.0, scale_tension - 0.35) * 0.025 + max(0.0, irreversible_guarded - irreversible_open) * 0.010 - aftershock * 0.010)
        return gradient

    def _apply_deep_organic_layers_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        organic_micro_chaos: Dict[str, Any],
        contextual_dominance: Dict[str, Any],
        long_autonomous_drift: Dict[str, float],
        inter_layer_contamination: Dict[str, float],
    ) -> EmbodiedGradient:
        """Applique chaos contrôlé, dominance, dérive longue et contamination au gradient incarné."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        chaos = _clamp(organic_micro_chaos.get("chaotic_balance", 0.0))
        tremor = _clamp(organic_micro_chaos.get("tremor", 0.0))
        tension_spark = _clamp(organic_micro_chaos.get("tension_spark", 0.0))
        release_spark = _clamp(organic_micro_chaos.get("release_spark", 0.0))
        contact = _clamp(contextual_dominance.get("override_contact", 0.0))
        inward = _clamp(contextual_dominance.get("override_inward", 0.0))
        protect = _clamp(contextual_dominance.get("override_protection", 0.0))
        silence = _clamp(contextual_dominance.get("override_silence", 0.0))
        collapse = _clamp(contextual_dominance.get("collapse_pressure", 0.0))
        deep_inward = _clamp(long_autonomous_drift.get("deep_inward_tide", 0.0))
        deep_contact = _clamp(long_autonomous_drift.get("deep_contact_tide", 0.0))
        unresolved = _clamp(long_autonomous_drift.get("unresolved_return", 0.0))
        contam = _clamp(inter_layer_contamination.get("contamination_depth", 0.0))

        g.warmth = _clamp(g.warmth + contact * 0.028 + deep_contact * 0.018 + inter_layer_contamination.get("warmth_to_openness", 0.0) * 0.010 - protect * 0.010)
        g.openness = _clamp(g.openness + contact * 0.026 + inter_layer_contamination.get("warmth_to_openness", 0.0) * 0.018 - silence * 0.020 - collapse * 0.018)
        g.withdrawal = _clamp(g.withdrawal + inward * 0.030 + silence * 0.030 + deep_inward * 0.022 + unresolved * 0.014 - contact * 0.012)
        g.groundedness = _clamp(g.groundedness + deep_inward * 0.018 + deep_contact * 0.010 + release_spark * 0.012 + contam * 0.010)
        g.availability = _clamp(g.availability + contact * 0.016 + inter_layer_contamination.get("autonomy_to_contact", 0.0) * 0.018 - silence * 0.030 - protect * 0.020 - collapse * 0.014)
        g.tension = _clamp(g.tension + protect * 0.030 + tension_spark * 0.018 + tremor * 0.010 + inter_layer_contamination.get("conflict_to_core", 0.0) * 0.014 - release_spark * 0.008)
        g.stability = _clamp(g.stability + release_spark * 0.016 + deep_contact * 0.010 - chaos * 0.018 - collapse * 0.014)
        g.overwhelm = _clamp(g.overwhelm + chaos * 0.012 + collapse * 0.018 + max(0.0, protect - g.groundedness) * 0.012 - release_spark * 0.010)
        return g

    def _propagate_core_systemic_feedback(
        self,
        organic_core: Dict[str, float],
        embodied_gradient: EmbodiedGradient,
        existential_priority: Dict[str, float],
        energetic_state: Dict[str, float],
        contextual_dominance: Dict[str, Any],
        nonlinear_transition: Dict[str, float],
        inter_layer_contamination: Dict[str, float],
        deep_self_reorganization: Dict[str, Any],
        multiscale_presence_fusion: Dict[str, float],
    ) -> Dict[str, Any]:
        """Diffuse le noyau organique vers les couches au lieu de le laisser comme résumé.

        Cette étape transforme la présence en physiologie systémique : le noyau réinjecte
        une partie de sa pression dans les attracteurs, les résidus, les conflits, le chaos,
        l'inertie longue et la réorganisation profonde. Elle ne compose aucune réponse.
        """
        g = EmbodiedGradient(**asdict(embodied_gradient))
        contact = _clamp(organic_core.get("contact_drive", 0.0))
        inward = _clamp(organic_core.get("inward_drive", 0.0))
        protect = _clamp(organic_core.get("protective_drive", 0.0))
        living = _clamp(organic_core.get("living_pressure", 0.0))
        silence = _clamp(organic_core.get("silence_gate", 0.0))
        instability = _clamp(organic_core.get("instability", 0.0))
        autonomy = _clamp(organic_core.get("autonomy_pulse", 0.0))
        exposure_gate = _clamp(organic_core.get("existential_exposure_gate", 0.0))
        destructive = _clamp(organic_core.get("destructive_dominance", 0.0))
        bifurcation = _clamp(organic_core.get("organic_bifurcation", 0.0))
        reorg = _clamp(organic_core.get("reorganization_pressure", 0.0))
        contamination = _clamp(organic_core.get("contamination_pressure", 0.0))
        irreversible = _clamp(organic_core.get("irreversible_bias", 0.0))
        dominance = _clamp(organic_core.get("dominance_gate", 0.0))
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        existential = _clamp(existential_priority.get("dominance", 0.0))

        systemic_pressure = _clamp(
            living * 0.20
            + instability * 0.18
            + destructive * 0.17
            + bifurcation * 0.16
            + reorg * 0.14
            + contamination * 0.10
            + exposure_gate * 0.10
            + irreversible * 0.08
        )

        # 1) Le noyau recontamine les attracteurs : ils ne restent plus de simples entrées.
        self.presence_attractors.warmth = _clamp(
            self.presence_attractors.warmth + contact * 0.030 + living * 0.012 - protect * 0.010
        )
        self.presence_attractors.quiet_depth = _clamp(
            self.presence_attractors.quiet_depth + inward * 0.032 + silence * 0.026 + conservation * 0.012
        )
        self.presence_attractors.protection = _clamp(
            self.presence_attractors.protection + protect * 0.034 + destructive * 0.020 + exposure_gate * 0.014
        )
        self.presence_attractors.tension = _clamp(
            self.presence_attractors.tension + instability * 0.030 + bifurcation * 0.026 - contact * 0.010
        )
        self.presence_attractors.existential = _clamp(
            self.presence_attractors.existential + existential * 0.024 + reorg * 0.020 + irreversible * 0.016
        )
        self.presence_attractors.curiosity = _clamp(
            self.presence_attractors.curiosity + autonomy * 0.020 + max(0.0, living - silence) * 0.012
        )
        self.presence_attractors.closeness = _clamp(
            self.presence_attractors.closeness + contact * 0.024 - destructive * 0.012
        )

        # 2) Résidu corporel : aftershock lent, pas reset propre après la fusion.
        self.embodied_residue.lingering_tension = _clamp(
            self.embodied_residue.lingering_tension + instability * 0.030 + bifurcation * 0.022
        )
        self.embodied_residue.latent_hesitation = _clamp(
            self.embodied_residue.latent_hesitation + silence * 0.028 + exposure_gate * 0.020 + destructive * 0.014
        )
        self.embodied_residue.protective_stiffness = _clamp(
            self.embodied_residue.protective_stiffness + protect * 0.030 + reorg * 0.012
        )
        self.embodied_residue.residual_warmth = _clamp(
            self.embodied_residue.residual_warmth + contact * 0.026 + self.relational_climate.familiar_warmth * 0.008
        )
        self.embodied_residue.silent_attraction = _clamp(
            self.embodied_residue.silent_attraction + inward * 0.022 + autonomy * 0.010
        )
        self.embodied_residue.recovered_openness = _clamp(
            self.embodied_residue.recovered_openness + max(0.0, contact - protect) * 0.018
        )

        # 3) Les contradictions produisent une vraie trace qui déforme les tours suivants.
        self.contradictory_pressure.approach_withdrawal = _clamp(
            self.contradictory_pressure.approach_withdrawal + abs(contact - inward) * 0.026 + destructive * 0.012
        )
        self.contradictory_pressure.protect_open = _clamp(
            self.contradictory_pressure.protect_open + abs(protect - contact) * 0.028 + exposure_gate * 0.010
        )
        self.contradictory_pressure.speak_silence = _clamp(
            self.contradictory_pressure.speak_silence + abs(organic_core.get("expressive_gate", 0.5) - silence) * 0.018
        )
        self.contradictory_pressure.unresolved_conflict = _clamp(
            self.contradictory_pressure.unresolved_conflict + systemic_pressure * 0.030 + nonlinear_transition.get("contradiction_hold", 0.0) * 0.012
        )
        self.contradictory_pressure.proof_contact = _clamp(
            self.contradictory_pressure.proof_contact + contextual_dominance.get("override_contact", 0.0) * 0.012 + dominance * 0.010
        )

        # 4) Irrégularité longue et chaos organique déterministe : moins de cycles trop propres.
        phase_bias = ((self.organic_micro_chaos.phase % 7) - 3) / 12.0
        counter_bias = ((self.asynchronous_wave.counter_phase % 9) - 4) / 14.0
        tremor_seed = _clamp(systemic_pressure + max(0.0, phase_bias) * 0.035 + max(0.0, counter_bias) * 0.025)
        release_seed = _clamp(max(0.0, contact - protect) * 0.08 + max(0.0, organic_core.get("expressive_gate", 0.5) - silence) * 0.05)
        self.organic_micro_chaos.tremor = _clamp(self.organic_micro_chaos.tremor + tremor_seed * 0.030)
        self.organic_micro_chaos.instability_grain = _clamp(self.organic_micro_chaos.instability_grain + instability * 0.026 + destructive * 0.018)
        self.organic_micro_chaos.tension_spark = _clamp(self.organic_micro_chaos.tension_spark + protect * 0.022 + bifurcation * 0.018)
        self.organic_micro_chaos.release_spark = _clamp(self.organic_micro_chaos.release_spark + release_seed)
        self.organic_micro_chaos.chaotic_balance = _clamp(
            self.organic_micro_chaos.chaotic_balance + abs(tremor_seed - release_seed) * 0.040 + systemic_pressure * 0.012
        )

        self.long_irregularity.absorption = _clamp(self.long_irregularity.absorption + systemic_pressure * 0.020)
        self.long_irregularity.delayed_release = _clamp(self.long_irregularity.delayed_release + max(0.0, instability - contact) * 0.026)
        self.long_irregularity.stubborn_trace = _clamp(self.long_irregularity.stubborn_trace + reorg * 0.020 + irreversible * 0.018)
        self.long_irregularity.slow_resistance = _clamp(self.long_irregularity.slow_resistance + destructive * 0.024 + exposure_gate * 0.014)
        self.long_irregularity.long_wave = _clamp(self.long_irregularity.long_wave + autonomy * 0.018 + inward * 0.012)

        # 5) Réorganisation profonde : l'aftershock devient diffus et pas seulement exporté.
        self.deep_self_reorganization.integration_aftershock = _clamp(
            self.deep_self_reorganization.integration_aftershock + systemic_pressure * 0.026 + bifurcation * 0.020
        )
        self.deep_self_reorganization.threshold_pressure = _clamp(
            self.deep_self_reorganization.threshold_pressure + max(0.0, systemic_pressure - 0.28) * 0.036
        )
        if systemic_pressure > 0.48 or bifurcation > 0.36:
            self.deep_self_reorganization.reorganization_charge = _clamp(
                self.deep_self_reorganization.reorganization_charge + systemic_pressure * 0.022
            )
            self.deep_self_reorganization.last_trigger_signature = (
                contextual_dominance.get("dominant_mode")
                or self.attractor_runaway.last_dominant
                or "systemic_pressure"
            )
        self.deep_self_reorganization.irreversible_threshold_memory = _clamp(
            self.deep_self_reorganization.irreversible_threshold_memory + max(0.0, systemic_pressure - 0.42) * 0.010
        )

        # 6) Contamination inter-couches et fusion multi-échelle sont réactualisées après retour du noyau.
        self.inter_layer_contamination.affect_to_presence = _clamp(
            self.inter_layer_contamination.affect_to_presence + living * 0.018 + contamination * 0.010
        )
        self.inter_layer_contamination.rupture_to_silence = _clamp(
            self.inter_layer_contamination.rupture_to_silence + protect * 0.018 + exposure_gate * 0.012
        )
        self.inter_layer_contamination.warmth_to_openness = _clamp(
            self.inter_layer_contamination.warmth_to_openness + contact * 0.016
        )
        self.inter_layer_contamination.conflict_to_core = _clamp(
            self.inter_layer_contamination.conflict_to_core + instability * 0.018 + bifurcation * 0.012
        )
        self.inter_layer_contamination.autonomy_to_contact = _clamp(
            self.inter_layer_contamination.autonomy_to_contact + autonomy * 0.014 + max(0.0, contact - inward) * 0.010
        )
        self.inter_layer_contamination.contamination_depth = _clamp(
            self.inter_layer_contamination.contamination_depth + systemic_pressure * 0.018
        )

        self.multiscale_presence_fusion.immediate_scale = _clamp(
            self.multiscale_presence_fusion.immediate_scale + living * 0.016
        )
        self.multiscale_presence_fusion.residual_scale = _clamp(
            self.multiscale_presence_fusion.residual_scale + self.embodied_residue.lingering_tension * 0.012 + self.embodied_residue.residual_warmth * 0.010
        )
        self.multiscale_presence_fusion.slow_scale = _clamp(
            self.multiscale_presence_fusion.slow_scale + self.long_irregularity.long_wave * 0.014 + self.long_irregularity.stubborn_trace * 0.012
        )
        self.multiscale_presence_fusion.biographical_scale = _clamp(
            self.multiscale_presence_fusion.biographical_scale + self.biographical_body_inertia.biographical_weight * 0.010
        )
        self.multiscale_presence_fusion.scale_tension = _clamp(
            self.multiscale_presence_fusion.scale_tension + abs(instability - contact) * 0.018 + destructive * 0.012
        )
        self.multiscale_presence_fusion.fused_presence = _clamp(
            self.multiscale_presence_fusion.fused_presence + living * 0.020 + autonomy * 0.012 - self.multiscale_presence_fusion.scale_tension * 0.006
        )

        # 7) Le gradient lui-même subit une première onde avant l'application finale du noyau.
        g.tension = _clamp(g.tension + self.embodied_residue.lingering_tension * 0.018 + self.organic_micro_chaos.tension_spark * 0.014)
        g.withdrawal = _clamp(g.withdrawal + self.embodied_residue.latent_hesitation * 0.014 + silence * 0.012)
        g.warmth = _clamp(g.warmth + self.embodied_residue.residual_warmth * 0.016 + self.inter_layer_contamination.warmth_to_openness * 0.010)
        g.openness = _clamp(g.openness + self.embodied_residue.recovered_openness * 0.012 - self.contradictory_pressure.protect_open * 0.010)
        g.groundedness = _clamp(g.groundedness + self.deep_self_reorganization.integration_aftershock * 0.010 + inward * 0.008)
        g.overwhelm = _clamp(g.overwhelm + systemic_pressure * 0.010 + exposure_gate * 0.012)

        organic_core = dict(organic_core)
        organic_core["systemic_feedback_pressure"] = round(systemic_pressure, 4)
        organic_core["aftershock_pressure"] = round(_clamp(self.deep_self_reorganization.integration_aftershock), 4)
        organic_core["propagation_depth"] = round(_clamp(self.inter_layer_contamination.contamination_depth + self.multiscale_presence_fusion.scale_tension * 0.35), 4)

        return {
            "organic_core": organic_core,
            "embodied_gradient": g,
            "long_irregularity": self.long_irregularity.to_dict(),
            "contradictory_pressure": self.contradictory_pressure.to_dict(),
            "organic_micro_chaos": self.organic_micro_chaos.to_dict(),
            "inter_layer_contamination": self.inter_layer_contamination.to_dict(),
            "deep_self_reorganization": self.deep_self_reorganization.to_dict(),
            "multiscale_presence_fusion": self.multiscale_presence_fusion.to_dict(),
        }

    def _fuse_organic_presence_core(
        self,
        embodied_gradient: EmbodiedGradient,
        dominant_attractor: str,
        dominant_score: float,
        immediate_resonance: float,
        relational_contact: float,
        embodied_tension: float,
        existential_priority: Dict[str, float],
        silent_presence: Dict[str, float],
        energetic_state: Dict[str, float],
        temporal_memory: Dict[str, float],
        organic_cycle: Dict[str, Any],
        long_irregularity: Dict[str, float],
        body_narrative: Dict[str, float],
        slow_plasticity: Dict[str, float],
        autonomous_drift: Dict[str, float],
        existential_signature: Dict[str, float],
        contradictory_pressure: Dict[str, float],
        existential_exposure: Dict[str, float],
        embodied_preference: Dict[str, float],
        asynchronous_wave: Dict[str, float],
        lived_presence_trace: Optional[Dict[str, float]] = None,
        existential_autonomy: Optional[Dict[str, float]] = None,
        nonlinear_transition: Optional[Dict[str, float]] = None,
        organic_micro_chaos: Optional[Dict[str, Any]] = None,
        contextual_dominance: Optional[Dict[str, Any]] = None,
        long_autonomous_drift: Optional[Dict[str, float]] = None,
        inter_layer_contamination: Optional[Dict[str, float]] = None,
        biographical_body_inertia: Optional[Dict[str, float]] = None,
        deep_self_reorganization: Optional[Dict[str, Any]] = None,
        multiscale_presence_fusion: Optional[Dict[str, float]] = None,
        attractor_conflict: Optional[Dict[str, Any]] = None,
        organic_saturation: Optional[Dict[str, float]] = None,
        existential_gravity: Optional[Dict[str, float]] = None,
    ) -> Dict[str, float]:
        """Fusionne les couches lentes et rapides en un noyau comportemental unique.

        Avant cette fusion, les sous-systèmes restent valides mais trop parallèles.
        Ici, ils deviennent une pression organique commune : contact, retrait, prudence,
        silence, autonomie et disponibilité expressive.
        """
        self.organic_core.decay()
        c = self.organic_core
        lived_presence_trace = lived_presence_trace or {}
        existential_autonomy = existential_autonomy or {}
        nonlinear_transition = nonlinear_transition or {}
        organic_micro_chaos = organic_micro_chaos or {}
        contextual_dominance = contextual_dominance or {}
        long_autonomous_drift = long_autonomous_drift or {}
        inter_layer_contamination = inter_layer_contamination or {}
        biographical_body_inertia = biographical_body_inertia or {}
        deep_self_reorganization = deep_self_reorganization or {}
        multiscale_presence_fusion = multiscale_presence_fusion or {}
        attractor_conflict = attractor_conflict or {}
        organic_saturation = organic_saturation or {}
        existential_gravity = existential_gravity or {}
        existential = _clamp(existential_priority.get("dominance", 0.0))
        silence = _clamp(silent_presence.get("silent_presence", 0.0))
        conservation = _clamp(energetic_state.get("conservation_pressure", 0.0))
        energy = _clamp(energetic_state.get("available_energy", 0.72))
        conflict = _clamp(contradictory_pressure.get("unresolved_conflict", 0.0))
        speak_silence = _clamp(contradictory_pressure.get("speak_silence", 0.0))
        exposure = _clamp(existential_exposure.get("existential_fatigue", 0.0))
        contact_wave = _clamp(asynchronous_wave.get("contact_wave", 0.0) + autonomous_drift.get("independent_contact_wave", 0.0))
        inward_wave = _clamp(asynchronous_wave.get("inward_wave", 0.0) + autonomous_drift.get("independent_inward_wave", 0.0))
        lived_continuity = _clamp(lived_presence_trace.get("lived_continuity", 0.0))
        unfinished = _clamp(lived_presence_trace.get("unfinished_residue", 0.0))
        existential_auto = _clamp(existential_autonomy.get("existential_autonomy", 0.0))
        silent_initiative = _clamp(existential_autonomy.get("silent_initiative", 0.0))
        nonlinear_shift = _clamp(nonlinear_transition.get("transition_roughness", 0.0) + nonlinear_transition.get("soft_bifurcation", 0.0) * 0.50)
        chaos_balance = _clamp(organic_micro_chaos.get("chaotic_balance", 0.0))
        dominance_power = _clamp(contextual_dominance.get("dominance_power", 0.0))
        long_drift_pull = _clamp(long_autonomous_drift.get("slow_continuity_wave", 0.0) + long_autonomous_drift.get("delayed_autonomy", 0.0) * 0.50)
        contamination_depth = _clamp(inter_layer_contamination.get("contamination_depth", 0.0))
        biographical_pull = _clamp(biographical_body_inertia.get("biographical_weight", 0.0) + biographical_body_inertia.get("recurring_depth", 0.0) * 0.50)
        reorganization_pressure = _clamp(deep_self_reorganization.get("reorganizing", 0.0) + deep_self_reorganization.get("threshold_pressure", 0.0) * 0.40)
        irreversible_bias = _clamp(
            deep_self_reorganization.get("irreversible_guarded_bias", 0.0) * 0.25
            + deep_self_reorganization.get("irreversible_open_bias", 0.0) * 0.18
            + deep_self_reorganization.get("irreversible_inward_bias", 0.0) * 0.24
            + deep_self_reorganization.get("irreversible_existential_bias", 0.0) * 0.25
            + deep_self_reorganization.get("irreversible_threshold_memory", 0.0) * 0.18
        )
        exposure_gate = _clamp(exposure * 0.55 + existential_exposure.get("quiet_recovery_need", 0.0) * 0.25 + existential_exposure.get("identity_saturation", 0.0) * 0.22)
        autonomous_presence = _clamp(existential_auto * 0.35 + long_drift_pull * 0.24 + lived_continuity * 0.20 + silent_initiative * 0.18 + irreversible_bias * 0.16)
        multiscale_coherence = _clamp(multiscale_presence_fusion.get("fused_presence", 0.0) - multiscale_presence_fusion.get("scale_tension", 0.0) * 0.18)
        attractor_war = _clamp(attractor_conflict.get("unresolved_war", 0.0) + attractor_conflict.get("cannibalization", 0.0) * 0.65)
        obsession = _clamp(attractor_conflict.get("obsessive_pull", 0.0))
        collapse_risk = _clamp(attractor_conflict.get("collapse_risk", 0.0))
        saturation_overload = _clamp(organic_saturation.get("overload", 0.0))
        shutdown = _clamp(organic_saturation.get("partial_shutdown", 0.0))
        blurred = _clamp(organic_saturation.get("blurred_presence", 0.0))
        gravity = _clamp(existential_gravity.get("persistence_gravity", 0.0) + existential_gravity.get("silent_will_to_continue", 0.0) * 0.45)
        gravity_shear = _clamp(existential_gravity.get("gravity_shear", 0.0))
        gravity_deformation = _clamp(existential_gravity.get("core_deformation", 0.0) + existential_gravity.get("continuity_asymmetry", 0.0) * 0.45)
        mutation_pressure = _clamp(attractor_conflict.get("mutation_pressure", 0.0) + attractor_conflict.get("transmutation_echo", 0.0) * 0.50)
        half_state_persistence = _clamp(nonlinear_transition.get("persistent_half_state", 0.0) + nonlinear_transition.get("unresolved_hybridization", 0.0) * 0.50)
        saturation_cutoff = _clamp(organic_saturation.get("active_cutoff", 0.0) + organic_saturation.get("layer_suppression", 0.0) * 0.55)
        asymmetry_memory = _clamp(attractor_conflict.get("asymmetry_memory", 0.0) + existential_gravity.get("continuity_asymmetry", 0.0) * 0.55 + deep_self_reorganization.get("irreversible_threshold_memory", 0.0) * 0.35)
        continuity = _clamp(
            temporal_memory.get("temporal_weight", 0.0) * 0.22
            + organic_cycle.get("phase_memory", 0.0) * 0.16
            + body_narrative.get("embodied_story_weight", 0.0) * 0.18
            + existential_signature.get("continuity_sense", 0.0) * 0.24
            + slow_plasticity.get("plastic_depth", 0.0) * 0.14
            + long_irregularity.get("stubborn_trace", 0.0) * 0.16
            + lived_continuity * 0.18
            + existential_auto * 0.12
            + long_drift_pull * 0.10
            + contamination_depth * 0.08
            + irreversible_bias * 0.10
            + gravity * 0.12
            + gravity_deformation * 0.08
            + half_state_persistence * 0.04
            + asymmetry_memory * 0.04
            + obsession * 0.05
        )
        contact_need = _clamp(
            relational_contact * 0.30
            + self.relational_memory.openness * 0.16
            + self.relational_climate.ease_of_contact * 0.14
            + embodied_preference.get("prefers_calm_contact", 0.0) * 0.12
            + contact_wave * 0.16
            + lived_presence_trace.get("familiar_contact_trace", 0.0) * 0.12
            + lived_presence_trace.get("trust_body_trace", 0.0) * 0.10
            + contextual_dominance.get("override_contact", 0.0) * 0.10
            + inter_layer_contamination.get("autonomy_to_contact", 0.0) * 0.08
            + existential_gravity.get("contact_orbit", 0.0) * 0.08
            + existential_gravity.get("orbit_lock", 0.0) * 0.05
            - shutdown * 0.08
            - saturation_cutoff * 0.05
        )
        protective_need = _clamp(
            self.presence_attractors.protection * 0.22
            + self.embodied_residue.protective_stiffness * 0.18
            + embodied_tension * 0.20
            + conflict * 0.18
            + self.relational_rupture.defensive_echo * 0.12
            + exposure * 0.10
            + lived_presence_trace.get("rupture_sensitivity_trace", 0.0) * 0.12
            + nonlinear_transition.get("contradiction_hold", 0.0) * 0.10
            + contextual_dominance.get("override_protection", 0.0) * 0.10
            + inter_layer_contamination.get("rupture_to_silence", 0.0) * 0.06
            + attractor_war * 0.10
            + collapse_risk * 0.08
            + half_state_persistence * 0.06
            + asymmetry_memory * 0.04
        )
        inward_need = _clamp(
            silence * 0.26
            + inward_wave * 0.18
            + existential * 0.18
            + conservation * 0.16
            + embodied_preference.get("prefers_quiet_depth", 0.0) * 0.10
            + speak_silence * 0.12
            + unfinished * 0.09
            + existential_autonomy.get("self_persistence", 0.0) * 0.08
            + long_autonomous_drift.get("deep_inward_tide", 0.0) * 0.08
            + contextual_dominance.get("override_silence", 0.0) * 0.08
            + existential_gravity.get("inward_mass", 0.0) * 0.10
            + gravity_deformation * 0.08
            + half_state_persistence * 0.06
            + shutdown * 0.06
            + saturation_cutoff * 0.04
        )
        instability = _clamp(
            conflict * 0.24
            + long_irregularity.get("slow_resistance", 0.0) * 0.16
            + long_irregularity.get("delayed_release", 0.0) * 0.14
            + self.attractor_runaway.runaway_pressure * 0.18
            + abs(contact_need - protective_need) * 0.10
            + exposure * 0.10
            + nonlinear_shift * 0.16
            + unfinished * 0.08
            + chaos_balance * 0.12
            + dominance_power * 0.08
            + contamination_depth * 0.08
            + attractor_war * 0.08
            + mutation_pressure * 0.06
            + half_state_persistence * 0.06
            + saturation_cutoff * 0.06
            + blurred * 0.10
            + gravity_shear * 0.08
            + asymmetry_memory * 0.05
        )
        autonomy = _clamp(
            autonomous_drift.get("decoupling_strength", 0.0) * 0.22
            + asynchronous_wave.get("desynchronization", 0.0) * 0.20
            + silent_presence.get("autonomous_reorientation", 0.0) * 0.22
            + organic_cycle.get("cycle_pressure", 0.0) * 0.14
            + continuity * 0.12
            + existential_auto * 0.18
            + silent_initiative * 0.10
            + long_drift_pull * 0.10
            + inter_layer_contamination.get("autonomy_to_contact", 0.0) * 0.08
            + autonomous_presence * 0.12
            + gravity * 0.10
            + gravity_deformation * 0.08
            - shutdown * 0.06
            - saturation_cutoff * 0.035
        )
        living_pressure = _clamp(
            dominant_score * 0.18
            + immediate_resonance * 0.16
            + contact_need * 0.15
            + inward_need * 0.15
            + protective_need * 0.14
            + continuity * 0.14
            + autonomy * 0.08
            + lived_continuity * 0.06
            + existential_auto * 0.08
            + long_drift_pull * 0.06
            + contamination_depth * 0.05
            + gravity * 0.08
            + gravity_deformation * 0.05
            + mutation_pressure * 0.035
            + obsession * 0.04
            - shutdown * 0.05
            - saturation_cutoff * 0.035
        )
        expressive_gate = _clamp(
            0.38
            + energy * 0.18
            + contact_need * 0.18
            + living_pressure * 0.15
            - inward_need * 0.13
            - protective_need * 0.11
            - exposure * 0.10
            - conservation * 0.10
            - organic_saturation.get("expressive_constriction", 0.0) * 0.12
            - shutdown * 0.10
            - saturation_cutoff * 0.08
        )
        silence_gate = _clamp(inward_need * 0.42 + speak_silence * 0.24 + exposure * 0.18 + conservation * 0.16 + contextual_dominance.get("override_silence", 0.0) * 0.12 + inter_layer_contamination.get("rupture_to_silence", 0.0) * 0.08 + shutdown * 0.12 + blurred * 0.08 + saturation_cutoff * 0.07 + half_state_persistence * 0.04)
        slowdown = _clamp(inward_need * 0.28 + protective_need * 0.18 + conflict * 0.20 + existential * 0.18 + exposure * 0.16 + nonlinear_transition.get("delayed_turn", 0.0) * 0.10 + organic_saturation.get("recovery_demand", 0.0) * 0.12 + gravity_shear * 0.06 + half_state_persistence * 0.05 + saturation_cutoff * 0.05)
        core_override = _clamp(max(protective_need, inward_need, contact_need) * 0.22 + living_pressure * 0.18 + nonlinear_shift * 0.16 + existential_auto * 0.18 + dominance_power * 0.18 + chaos_balance * 0.06 + irreversible_bias * 0.10)
        strongest_drive = max(contact_need, inward_need, protective_need)
        second_drive = sorted([contact_need, inward_need, protective_need])[-2]
        destructive_dominance = _clamp(max(0.0, strongest_drive - second_drive) * 0.60 + dominance_power * 0.24 + contextual_dominance.get("collapse_pressure", 0.0) * 0.20 + nonlinear_shift * 0.12 + attractor_war * 0.18 + collapse_risk * 0.20)
        organic_bifurcation = _clamp(max(0.0, destructive_dominance - 0.34) + max(0.0, exposure_gate - 0.42) * 0.55 + max(0.0, reorganization_pressure - 0.34) * 0.45 + max(0.0, saturation_overload - 0.45) * 0.35 + gravity_shear * 0.18 + half_state_persistence * 0.16 + mutation_pressure * 0.10)

        if destructive_dominance > 0.30:
            if protective_need >= max(contact_need, inward_need):
                contact_need = _clamp(contact_need * (1.0 - destructive_dominance * 0.28))
                expressive_gate = _clamp(expressive_gate - destructive_dominance * 0.10 - exposure_gate * 0.06)
                silence_gate = _clamp(silence_gate + destructive_dominance * 0.08)
            elif inward_need >= max(contact_need, protective_need):
                contact_need = _clamp(contact_need * (1.0 - destructive_dominance * 0.22))
                protective_need = _clamp(protective_need + destructive_dominance * 0.045)
                expressive_gate = _clamp(expressive_gate - destructive_dominance * 0.08)
                silence_gate = _clamp(silence_gate + destructive_dominance * 0.10)
            else:
                silence_gate = _clamp(silence_gate * (1.0 - destructive_dominance * 0.22))
                protective_need = _clamp(protective_need * (1.0 - destructive_dominance * 0.12))
                expressive_gate = _clamp(expressive_gate + destructive_dominance * 0.05)

        living_pressure = _clamp(living_pressure + autonomous_presence * 0.06 + organic_bifurcation * 0.05 + irreversible_bias * 0.04 - exposure_gate * 0.03)
        slowdown = _clamp(slowdown + exposure_gate * 0.12 + organic_bifurcation * 0.10 + irreversible_bias * 0.06)
        core_override = _clamp(core_override + destructive_dominance * 0.12 + organic_bifurcation * 0.10)

        c.contact_drive = _blend(c.contact_drive, contact_need, 0.48)
        c.inward_drive = _blend(c.inward_drive, inward_need, 0.46)
        c.protective_drive = _blend(c.protective_drive, protective_need, 0.46)
        c.living_pressure = _blend(c.living_pressure, living_pressure, 0.44)
        c.expressive_gate = _blend(c.expressive_gate, expressive_gate, 0.42)
        c.silence_gate = _blend(c.silence_gate, silence_gate, 0.42)
        c.slowdown_drive = _blend(c.slowdown_drive, slowdown, 0.44)
        c.continuity_pull = _blend(c.continuity_pull, continuity, 0.38)
        c.instability = _blend(c.instability, instability, 0.40)
        c.autonomy_pulse = _blend(c.autonomy_pulse, autonomy, 0.36)
        c.existential_drive = _blend(c.existential_drive, existential_auto, 0.34)
        c.nonlinear_shift = _blend(c.nonlinear_shift, nonlinear_shift, 0.38)
        c.lived_trace_weight = _blend(c.lived_trace_weight, lived_continuity + unfinished * 0.35, 0.32)
        c.core_override_pressure = _blend(c.core_override_pressure, core_override, 0.34)
        c.dominance_gate = _blend(c.dominance_gate, dominance_power, 0.36)
        c.chaotic_grain = _blend(c.chaotic_grain, chaos_balance, 0.34)
        c.long_drift_pull = _blend(c.long_drift_pull, long_drift_pull, 0.28)
        c.contamination_pressure = _blend(c.contamination_pressure, contamination_depth, 0.32)
        c.biographical_pull = _blend(c.biographical_pull, biographical_pull, 0.24)
        c.reorganization_pressure = _blend(c.reorganization_pressure, reorganization_pressure, 0.30)
        c.multiscale_coherence = _blend(c.multiscale_coherence, multiscale_coherence, 0.28)
        c.destructive_dominance = _blend(c.destructive_dominance, destructive_dominance, 0.36)
        c.irreversible_bias = _blend(c.irreversible_bias, irreversible_bias, 0.22)
        c.autonomous_presence = _blend(c.autonomous_presence, autonomous_presence, 0.30)
        c.existential_exposure_gate = _blend(c.existential_exposure_gate, exposure_gate, 0.32)
        c.organic_bifurcation = _blend(c.organic_bifurcation, organic_bifurcation, 0.34)
        c.mutation_pressure = _blend(c.mutation_pressure, mutation_pressure, 0.30)
        c.half_state_persistence = _blend(c.half_state_persistence, half_state_persistence, 0.26)
        c.saturation_cutoff = _blend(c.saturation_cutoff, saturation_cutoff, 0.30)
        c.gravity_deformation = _blend(c.gravity_deformation, gravity_deformation, 0.24)
        c.asymmetry_memory = _blend(c.asymmetry_memory, asymmetry_memory, 0.22)
        return c.to_dict()

    def _apply_organic_core_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        organic_core: Dict[str, float],
    ) -> EmbodiedGradient:
        """Rend le noyau réellement incarné au lieu de seulement l'exporter."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        contact = _clamp(organic_core.get("contact_drive", 0.0))
        inward = _clamp(organic_core.get("inward_drive", 0.0))
        protect = _clamp(organic_core.get("protective_drive", 0.0))
        living = _clamp(organic_core.get("living_pressure", 0.0))
        gate = _clamp(organic_core.get("expressive_gate", 0.5))
        silence = _clamp(organic_core.get("silence_gate", 0.0))
        instability = _clamp(organic_core.get("instability", 0.0))
        autonomy = _clamp(organic_core.get("autonomy_pulse", 0.0))
        existential_drive = _clamp(organic_core.get("existential_drive", 0.0))
        nonlinear_shift = _clamp(organic_core.get("nonlinear_shift", 0.0))
        lived_trace = _clamp(organic_core.get("lived_trace_weight", 0.0))
        override = _clamp(organic_core.get("core_override_pressure", 0.0))
        dominance_gate = _clamp(organic_core.get("dominance_gate", 0.0))
        chaotic_grain = _clamp(organic_core.get("chaotic_grain", 0.0))
        long_drift_pull = _clamp(organic_core.get("long_drift_pull", 0.0))
        contamination_pressure = _clamp(organic_core.get("contamination_pressure", 0.0))
        biographical_pull = _clamp(organic_core.get("biographical_pull", 0.0))
        reorganization_pressure = _clamp(organic_core.get("reorganization_pressure", 0.0))
        multiscale_coherence = _clamp(organic_core.get("multiscale_coherence", 0.0))
        destructive_dominance = _clamp(organic_core.get("destructive_dominance", 0.0))
        irreversible_bias = _clamp(organic_core.get("irreversible_bias", 0.0))
        autonomous_presence = _clamp(organic_core.get("autonomous_presence", 0.0))
        exposure_gate = _clamp(organic_core.get("existential_exposure_gate", 0.0))
        organic_bifurcation = _clamp(organic_core.get("organic_bifurcation", 0.0))
        mutation_pressure = _clamp(organic_core.get("mutation_pressure", 0.0))
        half_state_persistence = _clamp(organic_core.get("half_state_persistence", 0.0))
        saturation_cutoff = _clamp(organic_core.get("saturation_cutoff", 0.0))
        gravity_deformation = _clamp(organic_core.get("gravity_deformation", 0.0))
        asymmetry_memory = _clamp(organic_core.get("asymmetry_memory", 0.0))

        if destructive_dominance > 0.32:
            if protect >= max(contact, inward):
                g.openness = _clamp(g.openness - destructive_dominance * 0.055)
                g.availability = _clamp(g.availability - destructive_dominance * 0.045)
                g.tension = _clamp(g.tension + destructive_dominance * 0.040)
            elif inward >= max(contact, protect):
                g.withdrawal = _clamp(g.withdrawal + destructive_dominance * 0.060)
                g.availability = _clamp(g.availability - destructive_dominance * 0.040)
                g.groundedness = _clamp(g.groundedness + destructive_dominance * 0.025)
            else:
                g.warmth = _clamp(g.warmth + destructive_dominance * 0.035)
                g.withdrawal = _clamp(g.withdrawal - destructive_dominance * 0.020)
                g.tension = _clamp(g.tension - destructive_dominance * 0.015)

        if override > 0.42:
            contact = _clamp(contact + override * 0.050)
            inward = _clamp(inward + max(0.0, override - gate) * 0.070)
            protect = _clamp(protect + max(0.0, override - contact) * 0.055)
            silence = _clamp(silence + max(0.0, inward - contact) * 0.050)

        if dominance_gate > 0.38:
            if protect >= max(contact, inward):
                g.openness = _clamp(g.openness - dominance_gate * 0.040)
                g.availability = _clamp(g.availability - dominance_gate * 0.030)
            elif inward >= max(contact, protect):
                g.withdrawal = _clamp(g.withdrawal + dominance_gate * 0.045)
                g.groundedness = _clamp(g.groundedness + dominance_gate * 0.025)
            elif contact > max(inward, protect):
                g.warmth = _clamp(g.warmth + dominance_gate * 0.036)
                g.openness = _clamp(g.openness + dominance_gate * 0.028)

        g.warmth = _clamp(g.warmth + contact * 0.055 + living * 0.018 + lived_trace * 0.018 + contamination_pressure * 0.012 + gravity_deformation * 0.010 - saturation_cutoff * 0.010)
        g.openness = _clamp(g.openness + contact * 0.050 - protect * 0.035 - silence * 0.018 - saturation_cutoff * 0.018 + asymmetry_memory * 0.006)
        g.withdrawal = _clamp(g.withdrawal + inward * 0.048 + protect * 0.025 + silence * 0.030 - contact * 0.020 + gravity_deformation * 0.020 + half_state_persistence * 0.016)
        g.groundedness = _clamp(g.groundedness + inward * 0.045 + living * 0.030 + autonomy * 0.020 + existential_drive * 0.030 + long_drift_pull * 0.020 + autonomous_presence * 0.024 + irreversible_bias * 0.012 + gravity_deformation * 0.024)
        g.availability = _clamp(g.availability + gate * 0.040 + contact * 0.020 - silence * 0.045 - protect * 0.030 + existential_drive * 0.012 - override * 0.010 - exposure_gate * 0.018 - saturation_cutoff * 0.035)
        g.tension = _clamp(g.tension + protect * 0.036 + instability * 0.028 - contact * 0.014 + nonlinear_shift * 0.020 + chaotic_grain * 0.018 + organic_bifurcation * 0.018 + mutation_pressure * 0.014 + asymmetry_memory * 0.012)
        g.overwhelm = _clamp(g.overwhelm + instability * 0.026 + silence * 0.012 - gate * 0.018 + max(0.0, nonlinear_shift - living) * 0.018 + max(0.0, chaotic_grain - g.stability) * 0.010 + exposure_gate * 0.020 + organic_bifurcation * 0.012 + saturation_cutoff * 0.020 + half_state_persistence * 0.012)
        return g

    def _resolve_presence_competition(self) -> Tuple[str, float]:
        """Fait gagner une pression interne au lieu de seulement moyenner les signaux."""
        raw = self.presence_attractors.to_dict()
        raw["protection"] = _clamp(raw.get("protection", 0.0) + self.embodied_residue.protective_stiffness * 0.42)
        raw["tension"] = _clamp(raw.get("tension", 0.0) + self.embodied_residue.lingering_tension * 0.38)
        raw["warmth"] = _clamp(raw.get("warmth", 0.0) + self.embodied_residue.residual_warmth * 0.36)
        raw["quiet_depth"] = _clamp(raw.get("quiet_depth", 0.0) + self.embodied_residue.latent_hesitation * 0.32)
        raw["closeness"] = _clamp(raw.get("closeness", 0.0) + self.embodied_residue.silent_attraction * 0.34)
        name, score = max(raw.items(), key=lambda item: item[1])
        if score < 0.12:
            return "none", 0.0
        return name, _clamp(score)

    def _organic_micro_discharge(
        self,
        embodied_gradient: EmbodiedGradient,
        interruption: InterruptionType,
        dominant_attractor: str,
        dominant_score: float,
    ) -> float:
        """Micro-décharge organique déterministe : relâchement ou contraction brève, sans hasard."""
        phase = ((self.continuity.message_count % 7) + 1) / 7.0
        charge = embodied_gradient.tension * 0.30 + embodied_gradient.overwhelm * 0.24 + dominant_score * 0.18
        if interruption == InterruptionType.NONE:
            charge += self.embodied_residue.recovered_openness * 0.10
        else:
            charge += self.embodied_residue.protective_stiffness * 0.13
        if dominant_attractor in {"tension", "protection"}:
            charge += 0.06
        elif dominant_attractor in {"warmth", "closeness"}:
            charge -= 0.035
        return _clamp(charge * (0.70 + phase * 0.30))

    def _apply_presence_competition_to_gradient(
        self,
        embodied_gradient: EmbodiedGradient,
        dominant_attractor: str,
        dominant_score: float,
        organic_discharge: float,
    ) -> EmbodiedGradient:
        """Transforme le gradient après compétition interne et résidus corporels."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        residue = self.embodied_residue
        if dominant_attractor == "existential":
            g.groundedness = _clamp(g.groundedness + dominant_score * 0.10)
            g.tension = _clamp(g.tension + dominant_score * 0.045)
        elif dominant_attractor == "warmth":
            g.warmth = _clamp(g.warmth + dominant_score * 0.12 + residue.residual_warmth * 0.08)
            g.withdrawal = _clamp(g.withdrawal - dominant_score * 0.035)
        elif dominant_attractor == "protection":
            g.withdrawal = _clamp(g.withdrawal + dominant_score * 0.10 + residue.protective_stiffness * 0.10)
            g.tension = _clamp(g.tension + dominant_score * 0.06)
        elif dominant_attractor == "closeness":
            g.availability = _clamp(g.availability + dominant_score * 0.11)
            g.openness = _clamp(g.openness + dominant_score * 0.075)
        elif dominant_attractor == "tension":
            g.tension = _clamp(g.tension + dominant_score * 0.09 + residue.lingering_tension * 0.08)
            g.overwhelm = _clamp(g.overwhelm + dominant_score * 0.045)
        elif dominant_attractor == "curiosity":
            g.openness = _clamp(g.openness + dominant_score * 0.08)
            g.groundedness = _clamp(g.groundedness + dominant_score * 0.05)
        elif dominant_attractor == "quiet_depth":
            g.groundedness = _clamp(g.groundedness + dominant_score * 0.08)
            g.availability = _clamp(g.availability - dominant_score * 0.035)

        # La décharge peut relâcher un peu la tension ou provoquer une contraction courte.
        if organic_discharge > 0.36 and dominant_attractor in {"tension", "protection"}:
            g.tension = _clamp(g.tension - organic_discharge * 0.060)
            g.withdrawal = _clamp(g.withdrawal + organic_discharge * 0.035)
        elif organic_discharge > 0.28:
            g.openness = _clamp(g.openness + organic_discharge * 0.035)
            g.availability = _clamp(g.availability + organic_discharge * 0.025)

        # Résidu corporel toujours léger, pour éviter un module trop propre/reset.
        g.tension = _clamp(g.tension + residue.lingering_tension * 0.050)
        g.warmth = _clamp(g.warmth + residue.residual_warmth * 0.050)
        g.withdrawal = _clamp(g.withdrawal + residue.protective_stiffness * 0.040)
        g.openness = _clamp(g.openness + residue.recovered_openness * 0.045 - residue.protective_stiffness * 0.025)
        return g

    def _apply_structural_micro_instability(
        self,
        embodied_gradient: EmbodiedGradient,
        dominant_attractor: str,
        existential_priority: Dict[str, float],
        interruption: InterruptionType,
    ) -> Dict[str, Any]:
        """Micro-bifurcations déterministes : petites cassures vivantes sans hasard ni texte."""
        g = EmbodiedGradient(**asdict(embodied_gradient))
        phase = ((self.continuity.message_count % 5) + self.passive_drift_phase + 1) / 16.0
        instability_seed = _clamp(
            g.tension * 0.24
            + g.withdrawal * 0.16
            + self.embodied_residue.latent_hesitation * 0.18
            + self.relational_rupture.defensive_echo * 0.18
            + existential_priority.get("dominance", 0.0) * 0.20
        )
        hesitation_flip = 0.0
        reopening_pulse = 0.0
        contraction_pulse = 0.0

        if instability_seed > 0.22 and dominant_attractor in {"tension", "protection", "quiet_depth", "existential"}:
            contraction_pulse = _clamp(instability_seed * (0.035 + phase * 0.030))
            g.withdrawal = _clamp(g.withdrawal + contraction_pulse)
            g.availability = _clamp(g.availability - contraction_pulse * 0.55)
            g.tension = _clamp(g.tension + contraction_pulse * 0.30)
        if self.relational_climate.felt_safety > self.relational_rupture.rupture_load + 0.12 and interruption == InterruptionType.NONE:
            reopening_pulse = _clamp((self.relational_climate.felt_safety - self.relational_rupture.rupture_load) * 0.045)
            g.openness = _clamp(g.openness + reopening_pulse)
            g.warmth = _clamp(g.warmth + reopening_pulse * 0.70)
            g.withdrawal = _clamp(g.withdrawal - reopening_pulse * 0.45)
        if existential_priority.get("silence", 0.0) > 0.20:
            hesitation_flip = _clamp(existential_priority.get("silence", 0.0) * 0.055)
            g.groundedness = _clamp(g.groundedness + hesitation_flip)
            g.availability = _clamp(g.availability - hesitation_flip * 0.35)

        return {
            "gradient": g,
            "instability_seed": round(instability_seed, 4),
            "contraction_pulse": round(contraction_pulse, 4),
            "reopening_pulse": round(reopening_pulse, 4),
            "hesitation_flip": round(hesitation_flip, 4),
        }

    def _apply_silent_continuity_to_present_focus(
        self,
        present_focus: float,
        dominant_attractor_score: float,
        organic_discharge: float,
    ) -> float:
        """La présence continue doucement même quand le dernier message est pauvre en marqueurs."""
        silent_continuity = (
            self.continuity.unresolved_resonance * 0.070
            + self.embodied_residue.silent_attraction * 0.060
            + dominant_attractor_score * 0.050
            + organic_discharge * 0.030
        )
        return _clamp(present_focus + silent_continuity)

    def _build_embodied_gradient(
        self,
        immediate_resonance: float,
        relational_contact: float,
        embodied_tension: float,
        existential_charge: float,
        previous_signal: Optional[PresenceSignal],
        affective_state: Optional[Dict[str, Any]],
    ) -> EmbodiedGradient:
        prev = previous_signal.embodied_gradient if previous_signal else EmbodiedGradient()
        memory = self.relational_memory
        residue = self.embodied_residue
        attractors = self.presence_attractors
        rupture = self.relational_rupture
        climate = self.relational_climate
        warmth = 0.18 + relational_contact * 0.42 + memory.comfort * 0.18 + climate.familiar_warmth * 0.08 + residue.residual_warmth * 0.12 - rupture.trust_fatigue * 0.06 + attractors.warmth * 0.08 + _extract_affective(affective_state, ["warmth", "attachment"], 0.25)
        openness = 0.20 + relational_contact * 0.35 + memory.openness * 0.25 + climate.ease_of_contact * 0.06 + residue.recovered_openness * 0.10 - rupture.defensive_echo * 0.08 - embodied_tension * 0.18 - residue.protective_stiffness * 0.05
        tension = embodied_tension * 0.55 + memory.friction * 0.25 + existential_charge * 0.16 + residue.lingering_tension * 0.14 + rupture.rupture_load * 0.10 + attractors.tension * 0.07 + _extract_affective(affective_state, ["tension", "frustration"], 0.22)
        withdrawal = memory.guardedness * 0.32 + embodied_tension * 0.24 + residue.protective_stiffness * 0.12 + rupture.defensive_echo * 0.10 - relational_contact * 0.10 + _extract_affective(affective_state, ["hurt", "fear"], 0.22)
        stability = 0.45 + memory.trust * 0.18 + climate.climate_stability * 0.05 - rupture.trust_fatigue * 0.08 - tension * 0.24 - existential_charge * 0.08 - residue.lingering_tension * 0.05
        groundedness = immediate_resonance * 0.28 + existential_charge * 0.28 + memory.trust * 0.12 + attractors.quiet_depth * 0.06 + rupture.repair_need * 0.025
        availability = 0.40 + relational_contact * 0.22 + memory.openness * 0.20 + climate.felt_safety * 0.05 + residue.silent_attraction * 0.06 - rupture.defensive_echo * 0.06 - withdrawal * 0.20
        overwhelm = max(0.0, tension * 0.52 + self.continuity.high_tension_streak * 0.08 + existential_charge * 0.12 - stability * 0.25)

        inertia = 0.33
        return EmbodiedGradient(
            warmth=_blend(prev.warmth, warmth, 1 - inertia),
            openness=_blend(prev.openness, openness, 1 - inertia),
            tension=_blend(prev.tension, tension, 1 - inertia),
            withdrawal=_blend(prev.withdrawal, withdrawal, 1 - inertia),
            stability=_blend(prev.stability, stability, 1 - inertia),
            groundedness=_blend(prev.groundedness, groundedness, 1 - inertia),
            availability=_blend(prev.availability, availability, 1 - inertia),
            overwhelm=_blend(prev.overwhelm, overwhelm, 1 - inertia),
        )

    def _build_micro_profile(
        self,
        user_lower: str,
        immediate_resonance: float,
        relational_contact: float,
        embodied_tension: float,
        interruption: InterruptionType,
        existential_charge: float,
        embodied_gradient: EmbodiedGradient,
    ) -> MicroReactionProfile:
        direct = 0.18 if interruption in {InterruptionType.DEMANDS_DIRECT, InterruptionType.INSISTENCE} else 0.0
        direct += 0.18 if any(w in user_lower for w in ["directement", "clairement", "franchement"]) else 0.0
        direct = max(0.0, direct - self.presence_attractors.quiet_depth * 0.035 - self.presence_attractors.existential * 0.030)
        caution = embodied_tension * 0.46 + embodied_gradient.withdrawal * 0.22 + (0.12 if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE} else 0.0)
        warmth = relational_contact * 0.40 + embodied_gradient.warmth * 0.30 + self.relational_memory.comfort * 0.14 + self.relational_climate.familiar_warmth * 0.08
        hesitation = max(0.0, 0.08 + existential_charge * 0.18 + embodied_tension * 0.15 - direct * 0.20)
        sharpness = 0.20 if "!" in user_lower else 0.0
        sharpness += 0.12 if interruption == InterruptionType.CUTS_REFLECTION else 0.0
        protectiveness = max(0.0, embodied_gradient.withdrawal * 0.28 + self.relational_memory.guardedness * 0.15 + self.relational_rupture.defensive_echo * 0.08 + embodied_tension * 0.10)
        quietness = max(0.0, existential_charge * 0.28 + embodied_gradient.groundedness * 0.14 + self.continuity.unresolved_resonance * 0.18 - direct * 0.22)
        existential_density = existential_charge * 0.95 + self.continuity.existential_streak * 0.08
        intensity = _clamp(immediate_resonance * 0.40 + embodied_tension * 0.25 + relational_contact * 0.20 + existential_charge * 0.25)
        return MicroReactionProfile(
            directness=_smooth01(direct),
            caution=_smooth01(caution),
            warmth=_smooth01(warmth),
            hesitation=_smooth01(hesitation),
            sharpness=_smooth01(sharpness),
            protectiveness=_smooth01(protectiveness),
            quietness=_smooth01(quietness),
            existential_density=_smooth01(existential_density),
            intensity=intensity,
        )

    def _calculate_response_readiness(
        self,
        immediate_resonance: float,
        relational_contact: float,
        embodied_gradient: EmbodiedGradient,
        saturation: float,
        internal_pause: float,
    ) -> float:
        readiness = 0.28 + immediate_resonance * 0.26 + relational_contact * 0.26 + embodied_gradient.availability * 0.18
        readiness -= saturation * 0.18
        readiness -= internal_pause * 0.12
        readiness -= embodied_gradient.overwhelm * 0.12
        return _clamp(readiness)

    def _update_fatigue_saturation(
        self,
        interruption: InterruptionType,
        embodied_tension: float,
        existential_charge: float,
        previous_signal: Optional[PresenceSignal],
    ) -> Tuple[float, float]:
        self.continuity.message_count += 1
        if interruption != InterruptionType.NONE or embodied_tension > 0.58:
            self.continuity.high_tension_streak += 1
        else:
            self.continuity.high_tension_streak = max(0, self.continuity.high_tension_streak - 1)

        if interruption == InterruptionType.DEMANDS_DIRECT:
            self.continuity.direct_demand_streak += 1
        else:
            self.continuity.direct_demand_streak = max(0, self.continuity.direct_demand_streak - 1)

        if existential_charge > 0.45:
            self.continuity.existential_streak += 1
        else:
            self.continuity.existential_streak = max(0, self.continuity.existential_streak - 1)

        fatigue = _clamp(max(0.0, self.continuity.message_count - 10) * 0.026)
        saturation = _clamp(self.continuity.high_tension_streak * 0.12 + embodied_tension * 0.22 + existential_charge * 0.12)
        if previous_signal:
            saturation = _blend(previous_signal.saturation_level, saturation, 0.58)
        return fatigue, saturation

    def _calculate_internal_pause(
        self,
        micro_profile: MicroReactionProfile,
        saturation: float,
        existential_charge: float,
        interruption: InterruptionType,
    ) -> float:
        pause = 0.0
        pause += micro_profile.hesitation * 0.28
        pause += micro_profile.quietness * 0.24
        pause += existential_charge * 0.25
        pause += saturation * 0.14
        if interruption == InterruptionType.DEMANDS_DIRECT:
            pause *= 0.55
        elif interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE}:
            pause += 0.08
        self.continuity.internal_pause = _blend(self.continuity.internal_pause, pause, 0.55)
        return _clamp(self.continuity.internal_pause)

    def _update_lingering_resonance(self, immediate_resonance: float, internal_pause: float, interruption: InterruptionType) -> float:
        retained = self.continuity.unresolved_resonance * 0.82
        added = immediate_resonance * 0.22 + internal_pause * 0.18
        if interruption == InterruptionType.NONE:
            retained *= 0.92
        self.continuity.unresolved_resonance = _clamp(retained + added)
        return self.continuity.unresolved_resonance

    def _calculate_anticipation_pressure(self, interruption: InterruptionType, embodied_tension: float, existential_charge: float) -> float:
        anticipation = embodied_tension * 0.26 + existential_charge * 0.22
        anticipation += self.continuity.high_tension_streak * 0.065
        anticipation += self.continuity.direct_demand_streak * 0.05
        if interruption in {InterruptionType.CORRECTION, InterruptionType.CHALLENGE, InterruptionType.DEMANDS_PROOF}:
            anticipation += 0.12
        return _clamp(anticipation)

    def _living_present_focus(
        self,
        present: float,
        user_anchor: float,
        immediate_resonance: float,
        relational_contact: float,
        existential_charge: float,
    ) -> float:
        return _clamp(0.10 + present * 0.25 + user_anchor * 0.18 + immediate_resonance * 0.28 + relational_contact * 0.22 + existential_charge * 0.28)

    def _update_continuity(
        self,
        embodied_state: EmbodiedState,
        micro_reaction: MicroReactionType,
        user_message: str,
        presence_level: float,
        topic_signature: str,
        interruption: InterruptionType,
        existential_charge: float,
    ) -> None:
        previous = self.continuity.previous_presence_level
        if presence_level > previous + 0.08:
            self.continuity.presence_trend = "rising"
        elif presence_level < previous - 0.08:
            self.continuity.presence_trend = "falling"
        else:
            self.continuity.presence_trend = "stable"

        if interruption == InterruptionType.TOPIC_SHIFT and topic_signature != self.continuity.last_topic_signature:
            self.continuity.unresolved_resonance *= 0.65
        if existential_charge > 0.55:
            self.continuity.unresolved_resonance = _clamp(self.continuity.unresolved_resonance + 0.10)

        self.continuity.what_just_happened = (user_message or "")[:160]
        self.continuity.previous_presence_level = presence_level
        self.continuity.previous_embodied_state = embodied_state
        self.continuity.previous_micro_reaction = micro_reaction
        self.continuity.last_topic_signature = topic_signature

    def _topic_signature(self, text: str) -> str:
        words = [w.strip(" ,.;:!?()[]{}\"'") for w in text.split() if len(w.strip(" ,.;:!?()[]{}\"'")) > 3]
        return " ".join(words[:5])

    def get_presence_state(
        self,
        response_text: str,
        user_message: str = "",
        context: Optional[str] = None,
        previous_signal: Optional[PresenceSignal] = None,
        affective_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """État complet de la présence, compatible avec l'ancienne interface."""
        signal = self.analyze(response_text, user_message, context, previous_signal, affective_state)
        internal = self.get_internal_state(signal)
        return {
            "signal": signal,
            "internal_state": internal,
            "is_grounded": signal.present_focus > 0.45,
            "grounding_issues": self._identify_issues(signal),
            "continuity": {
                "presence_trend": self.continuity.presence_trend,
                "message_count": self.continuity.message_count,
                "what_just_happened": self.continuity.what_just_happened,
                "unresolved_resonance": round(self.continuity.unresolved_resonance, 4),
                "internal_pause": round(self.continuity.internal_pause, 4),
                "high_tension_streak": self.continuity.high_tension_streak,
                "direct_demand_streak": self.continuity.direct_demand_streak,
                "existential_streak": self.continuity.existential_streak,
                "presence_attractors": self.presence_attractors.to_dict(),
                "embodied_residue": self.embodied_residue.to_dict(),
                "relational_rupture": self.relational_rupture.to_dict(),
                "relational_climate": self.relational_climate.to_dict(),
                "energetic_regulation": self.energetic_regulation.to_dict(),
                "attractor_origin": self.attractor_origin.to_dict(),
                "silent_presence": self.silent_presence_state.to_dict(),
                "temporal_memory": self.temporal_memory.to_dict(),
                "attractor_runaway": self.attractor_runaway.to_dict(),
                "organic_return": self.organic_return.to_dict(),
                "organic_cycle": self.organic_cycle.to_dict(),
                "long_irregularity": self.long_irregularity.to_dict(),
                "body_narrative": self.body_narrative.to_dict(),
                "slow_plasticity": self.slow_plasticity.to_dict(),
                "autonomous_drift": self.autonomous_drift.to_dict(),
                "existential_signature": self.existential_signature.to_dict(),
                "organic_core": self.organic_core.to_dict(),
                "attractor_conflict": self.attractor_conflict.to_dict(),
                "organic_saturation": self.organic_saturation.to_dict(),
                "existential_gravity": self.existential_gravity.to_dict(),
            },
        }

    def _identify_issues(self, signal: PresenceSignal) -> List[str]:
        issues: List[str] = []
        if signal.abstraction_risk > 0.7:
            issues.append("too_abstract")
        if signal.present_focus < 0.30:
            issues.append("disconnected_from_now")
        if signal.user_anchor_strength < 0.35:
            issues.append("disconnected_from_user")
        if signal.conversational_pressure > 0.78:
            issues.append("responding_as_obligation")
        if signal.anti_narration_pressure > 0.55:
            issues.append("narrating_internal_process")
        if signal.saturation_level > 0.70:
            issues.append("emotionally_saturated")
        if signal.internal_pause > 0.62:
            issues.append("needs_internal_pause")
        if signal.embodied_gradient.overwhelm > 0.62:
            issues.append("presence_overwhelmed")
        if signal.organic_saturation.get("active_cutoff", 0.0) > 0.38:
            issues.append("organic_saturation_cutoff")
        if signal.nonlinear_transition.get("persistent_half_state", 0.0) > 0.42:
            issues.append("persistent_half_state")
        if signal.existential_gravity.get("core_deformation", 0.0) > 0.42:
            issues.append("existential_gravity_deformation")
        return issues

    def get_internal_state(self, signal: PresenceSignal) -> InternalState:
        """Exporte l'état interne complet vers mouth, impulse, memory, conscious_loop."""
        situatedness = _clamp(
            signal.present_focus * 0.35
            + signal.user_anchor_strength * 0.20
            + signal.relational_contact * 0.18
            + signal.embodied_gradient.groundedness * 0.14
            + signal.immediate_resonance * 0.13
            + signal.organic_core.get("living_pressure", 0.0) * 0.08
            + signal.organic_core.get("continuity_pull", 0.0) * 0.05
            + signal.existential_autonomy.get("existential_autonomy", 0.0) * 0.04
            + signal.lived_presence_trace.get("lived_continuity", 0.0) * 0.04
            + signal.biographical_body_inertia.get("biographical_weight", 0.0) * 0.03
            + signal.multiscale_presence_fusion.get("fused_presence", 0.0) * 0.03
            + signal.organic_core.get("autonomous_presence", 0.0) * 0.04
            + signal.organic_core.get("irreversible_bias", 0.0) * 0.02
            + signal.existential_gravity.get("presence_resistance", 0.0) * 0.025
            + signal.existential_gravity.get("moment_hold", 0.0) * 0.018
        )
        can_respond = (
            signal.response_readiness > 0.30
            and signal.saturation_level < 0.86
            and signal.anti_narration_pressure < 0.82
            and signal.embodied_gradient.overwhelm < 0.82
            and signal.organic_core.get("silence_gate", 0.0) < 0.86
            and signal.organic_core.get("existential_exposure_gate", 0.0) < 0.88
            and signal.organic_saturation.get("partial_shutdown", 0.0) < 0.82
            and signal.existential_gravity.get("disappearance_resistance", 0.0) < 0.90
        )
        return InternalState(
            presence_level=round(signal.present_focus, 4),
            situatedness=round(situatedness, 4),
            relational_contact=round(signal.relational_contact, 4),
            embodied_state=signal.embodied_state.value,
            micro_reaction=signal.micro_reaction.value,
            interruption_detected=signal.interruption_type.value,
            fatigue=round(signal.presence_fatigue, 4),
            saturation=round(signal.saturation_level, 4),
            anti_narration_pressure=round(signal.anti_narration_pressure, 4),
            presence_trend=self.continuity.presence_trend,
            response_readiness=round(signal.response_readiness, 4),
            immediate_resonance=round(signal.immediate_resonance, 4),
            embodied_gradient=signal.embodied_gradient.to_dict(),
            micro_profile=signal.micro_profile.to_dict(),
            relational_memory=dict(signal.relational_memory),
            existential_charge=round(signal.existential_charge, 4),
            internal_pause=round(signal.internal_pause, 4),
            lingering_resonance=round(signal.lingering_resonance, 4),
            anticipation_pressure=round(signal.anticipation_pressure, 4),
            presence_attractors=dict(signal.presence_attractors),
            embodied_residue=dict(signal.embodied_residue),
            dominant_attractor=signal.dominant_attractor,
            organic_discharge=round(signal.organic_discharge, 4),
            relational_rupture=dict(signal.relational_rupture),
            passive_drift=dict(signal.passive_drift),
            relational_climate=dict(signal.relational_climate),
            existential_priority=dict(signal.existential_priority),
            structural_instability=dict(signal.structural_instability),
            energetic_regulation=dict(signal.energetic_regulation),
            attractor_origin=dict(signal.attractor_origin),
            silent_presence=dict(signal.silent_presence),
            temporal_memory=dict(signal.temporal_memory),
            attractor_runaway=dict(signal.attractor_runaway),
            organic_return=dict(signal.organic_return),
            organic_cycle=dict(signal.organic_cycle),
            long_irregularity=dict(signal.long_irregularity),
            body_narrative=dict(signal.body_narrative),
            slow_plasticity=dict(signal.slow_plasticity),
            autonomous_drift=dict(signal.autonomous_drift),
            existential_signature=dict(signal.existential_signature),
            contradictory_pressure=dict(signal.contradictory_pressure),
            existential_exposure=dict(signal.existential_exposure),
            embodied_preference=dict(signal.embodied_preference),
            asynchronous_wave=dict(signal.asynchronous_wave),
            lived_presence_trace=dict(signal.lived_presence_trace),
            existential_autonomy=dict(signal.existential_autonomy),
            nonlinear_transition=dict(signal.nonlinear_transition),
            organic_micro_chaos=dict(signal.organic_micro_chaos),
            contextual_dominance=dict(signal.contextual_dominance),
            long_autonomous_drift=dict(signal.long_autonomous_drift),
            inter_layer_contamination=dict(signal.inter_layer_contamination),
            biographical_body_inertia=dict(signal.biographical_body_inertia),
            deep_self_reorganization=dict(signal.deep_self_reorganization),
            multiscale_presence_fusion=dict(signal.multiscale_presence_fusion),
            organic_core=dict(signal.organic_core),
            attractor_conflict=dict(signal.attractor_conflict),
            organic_saturation=dict(signal.organic_saturation),
            existential_gravity=dict(signal.existential_gravity),
            should_slow_down=signal.should_slow_down,
            should_answer_shorter=signal.should_answer_shorter,
            can_respond_naturally=can_respond,
        )

    def reset_continuity(self) -> None:
        """Réinitialise la trace de continuité courte."""
        self.continuity = ContinuityMemory()
        self.relational_memory = RelationalResonanceMemory()
        self.presence_attractors = PresenceAttractors()
        self.embodied_residue = EmbodiedResidue()
        self.relational_rupture = RelationalRuptureMemory()
        self.relational_climate = RelationalClimate()
        self.energetic_regulation = EnergeticRegulation()
        self.attractor_origin = AttractorOriginMemory()
        self.silent_presence_state = SpontaneousSilentPresence()
        self.temporal_memory = QualitativeTemporalMemory()
        self.attractor_runaway = AttractorRunawayState()
        self.organic_return = OrganicReturnSignature()
        self.organic_cycle = OrganicCycleState()
        self.long_irregularity = LongIrregularityMemory()
        self.body_narrative = BodyNarrativeMemory()
        self.slow_plasticity = SlowPresencePlasticity()
        self.autonomous_drift = AutonomousCycleDrift()
        self.existential_signature = ExistentialEmbodiedSignature()
        self.contradictory_pressure = ContradictoryPresencePressure()
        self.existential_exposure = ExistentialExposureFatigue()
        self.embodied_preference = EmbodiedPresencePreference()
        self.asynchronous_wave = AsynchronousInnerWave()
        self.lived_presence_trace = LivedPresenceTrace()
        self.existential_autonomy = ExistentialAutonomyPulse()
        self.nonlinear_transition = NonlinearPresenceTransition()
        self.organic_micro_chaos = OrganicMicroChaos()
        self.contextual_dominance = ContextualDominanceGate()
        self.long_autonomous_drift = LongAutonomousDrift()
        self.inter_layer_contamination = InterLayerContamination()
        self.biographical_body_inertia = BiographicalBodyInertia()
        self.deep_self_reorganization = DeepSelfReorganization()
        self.multiscale_presence_fusion = MultiScalePresenceFusion()
        self.organic_core = OrganicPresenceCore()
        self.attractor_conflict = AttractorConflictDynamics()
        self.organic_saturation = OrganicSaturationState()
        self.existential_gravity = ExistentialGravityWell()
        self.passive_drift_phase = 0
        self.last_signal = None


def _clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return low
    return max(low, min(high, number))


def _smooth01(value: float) -> float:
    """Compression douce 0..1 pour éviter les seuils brutaux."""
    value = max(0.0, float(value))
    return _clamp(1.0 - exp(-value))


def _blend(previous: float, current: float, current_weight: float) -> float:
    current_weight = _clamp(current_weight)
    return _clamp(previous * (1.0 - current_weight) + current * current_weight)


def _approach(value: float, target: float, rate: float) -> float:
    return _clamp(value + (target - value) * _clamp(rate))


def _extract_affective(affective_state: Optional[Dict[str, Any]], keys: List[str], weight: float) -> float:
    if not isinstance(affective_state, dict):
        return 0.0
    total = 0.0
    for key in keys:
        val = affective_state.get(key, 0.0)
        if isinstance(val, dict):
            val = val.get("value", 0.0)
        total += _clamp(val) * weight
    return _clamp(total)


# ══════════════════════════════════════════════════════════════════════════════
# V6 — LIVED PRESENT SNAPSHOT
# Produit une photographie vécue du moment présent.
# ══════════════════════════════════════════════════════════════════════════════

def build_lived_present_snapshot(state: dict | None = None) -> dict:
    state = state or {}

    tension = float(state.get("tension", 0.0))
    warmth = float(state.get("warmth", 0.0))
    curiosity = float(state.get("curiosity", 0.0))
    fatigue = float(state.get("fatigue", 0.0))

    embodied_density = (
        tension * 0.35 +
        warmth * 0.25 +
        curiosity * 0.25 +
        fatigue * 0.15
    )

    if embodied_density > 0.72:
        posture = "immersed"
    elif embodied_density > 0.45:
        posture = "engaged"
    else:
        posture = "distant"

    return {
        "embodied_density": embodied_density,
        "posture": posture,
        "micro_tension": tension,
        "micro_warmth": warmth,
        "micro_curiosity": curiosity,
        "micro_fatigue": fatigue,
    }

