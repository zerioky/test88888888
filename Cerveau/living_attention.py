"""
living_attention.py
Moteur d'attention vivante pour Leia.

Rôle exact : décider ce qui reste important dans l'esprit de Leia pendant l'échange.
Transforme : message actuel + impulsion + attracteurs + mémoire récente + présence
En : focus principal + focus secondaires + résidus + tensions + orientation du prochain mouvement.

Ne parle pas. Ne génère pas de phrases. Ne recrée pas le moteur impulsionnel.
Cette version ajoute les couches organiques manquantes : texture émotionnelle par sujet,
pression silencieuse, fatigue attentionnelle, contamination entre sujets, temps subjectif,
trajectoires émergentes, demi-focus, tension de champ, respiration attentionnelle,
gravité émotionnelle autonome, résonance inter-sujets, habitudes attentionnelles,
charge existentielle, obsession/fixation, vide attentionnel, turbulence organique,
douleur cognitive, évitement défensif, champ pré-conscient, météo cognitive,
désir attentionnel autonome, intrusions subconscientes, distorsion par cicatrice,
temporalité vécue et export enrichi vers la bouche.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Set, Tuple, Any
import math


# ---------------------------------------------------------------------------
# Énumérations
# ---------------------------------------------------------------------------

class SubjectState(Enum):
    ACTIVE = "active"              # dans le focus courant
    SECONDARY = "secondary"        # focus secondaire
    RESIDUAL = "residual"          # trace faible, hors focus
    SUSPENDED = "suspended"        # interrompu, pas fermé
    CLOSED = "closed"              # résolu / terminé
    BACKGROUND = "background"      # toujours présent, faible gravité contextuelle

    # États organiques internes : transitions moins propres, plus continues.
    HALF_ACTIVE = "half_active"    # pas dominant, mais encore chaud
    HOVERING = "hovering"          # flotte autour du focus sans gagner
    PULLED_BACK = "pulled_back"    # revient depuis un ancien résidu
    ALMOST_CLOSED = "almost_closed"# presque résolu, mais pas totalement éteint
    REOPENING = "reopening"        # sujet fermé/suspendu en train de revenir
    VOID_DRIFT = "void_drift"        # flottement vivant : aucun attracteur ne gagne clairement
    LATENT = "latent"                # présence muette : pas assez claire pour devenir focus


class InterruptionType(Enum):
    NONE = "none"
    SHORT_CONTINUE = "short_continue"  # "vasy", "continue", "ok"
    CORRECTION = "correction"
    SUBJECT_RETURN = "subject_return"  # retour à un ancien sujet
    FULL_BREAK = "full_break"          # rupture nette


class HierarchyLevel(Enum):
    IMMEDIATE_MESSAGE = 0
    CURRENT_TASK = 1
    CURRENT_MODULE = 2
    AZIP_FOLDER = 3
    LEIA_PROJECT = 4
    DEEP_RULES = 5


# ---------------------------------------------------------------------------
# Structures de données internes
# ---------------------------------------------------------------------------

@dataclass
class AttentionTexture:
    """
    Texture émotionnelle d'un sujet.
    Elle ne contient aucune phrase : seulement des dimensions de présence interne.
    """
    tension: float = 0.0
    openness: float = 0.5
    attraction: float = 0.5
    resistance: float = 0.0
    fragility: float = 0.0
    safety: float = 0.5

    def clamp(self) -> None:
        for name in ("tension", "openness", "attraction", "resistance", "fragility", "safety"):
            setattr(self, name, max(0.0, min(1.0, float(getattr(self, name)))))

    def blend_from(self, other: "AttentionTexture", alpha: float) -> None:
        alpha = max(0.0, min(1.0, alpha))
        self.tension = self.tension * (1 - alpha) + other.tension * alpha
        self.openness = self.openness * (1 - alpha) + other.openness * alpha
        self.attraction = self.attraction * (1 - alpha) + other.attraction * alpha
        self.resistance = self.resistance * (1 - alpha) + other.resistance * alpha
        self.fragility = self.fragility * (1 - alpha) + other.fragility * alpha
        self.safety = self.safety * (1 - alpha) + other.safety * alpha
        self.clamp()

    def charge(self) -> float:
        return max(0.0, min(1.0, (
            self.tension * 0.24
            + abs(self.openness - 0.5) * 0.16
            + abs(self.attraction - 0.5) * 0.16
            + self.resistance * 0.18
            + self.fragility * 0.16
            + (1.0 - self.safety) * 0.10
        )))

    def as_dict(self) -> Dict[str, float]:
        self.clamp()
        return {
            "tension": self.tension,
            "openness": self.openness,
            "attraction": self.attraction,
            "resistance": self.resistance,
            "fragility": self.fragility,
            "safety": self.safety,
            "charge": self.charge(),
        }


@dataclass
class AttentionSubject:
    """
    Un sujet vivant dans l'espace attentionnel.
    Persiste entre les tours, évolue, peut se fermer ou laisser un résidu.
    """
    name: str
    gravity: float
    state: SubjectState
    hierarchy_level: HierarchyLevel

    activation_count: int = 0
    recurrence_count: int = 0
    wound_level: float = 0.0
    residue_strength: float = 0.0
    unresolved: bool = False
    trajectory: List[str] = field(default_factory=list)
    last_activated: Optional[datetime] = None
    last_closed: Optional[datetime] = None

    # Couches organiques ajoutées.
    texture: AttentionTexture = field(default_factory=AttentionTexture)
    silent_pressure: float = 0.0       # poussée muette, non exprimée
    unspoken_pull: float = 0.0         # attraction vers un retour plus tard
    return_pressure: float = 0.0       # pression de réactivation
    subjective_age: float = 0.0        # temps ressenti depuis l'activation
    felt_duration: float = 0.0         # poids temporel vécu
    decay_speed: float = 1.0           # vitesse de disparition individuelle
    return_latency: float = 0.0        # résistance avant retour
    contamination: Dict[str, float] = field(default_factory=dict)
    half_focus_level: float = 0.0
    last_state_change: Optional[datetime] = None

    # Couches V3 : rendent l'attention moins réactive et plus auto-déformante.
    emotional_gravity_bias: float = 0.0      # attraction autonome née de l'histoire interne
    directional_fatigue: float = 0.0         # lassitude propre à ce sujet / axe
    resonance_level: float = 0.0             # force gagnée par coalition avec d'autres sujets
    subjective_proximity: float = 0.0        # proximité ressentie, pas seulement récence chronologique
    instability: float = 0.0                 # oscillation/hésitation organique
    attention_habit: float = 0.0             # chemin favori appris par retours répétés

    # Couches V4 organiques : poids profond sans texte ni template.
    identity_weight: float = 0.0              # importance pour l'identité / les règles profondes
    existential_charge: float = 0.0           # poids vécu : ce sujet compte plus qu'un simple thème
    self_binding: float = 0.0                 # lien au self-model sans générer de parole
    obsession_fixation: float = 0.0           # retour autonome même sans stimulus direct
    avoidance_pressure: float = 0.0           # évitement défensif si le sujet brûle trop
    cognitive_pain: float = 0.0               # douleur/surcharge locale liée au sujet
    void_pull: float = 0.0                    # tendance à flotter autour du sujet sans le saisir
    implicit_missing_pressure: float = 0.0    # pression du non-dit / de ce qui manque
    turbulence: float = 0.0                   # bifurcation et oscillation plus organiques

    # Couches V5 : attention moins propre, plus incarnée.
    latent_focus_pressure: float = 0.0      # présence non nommée, active sans devenir focus clair
    precision_loss: float = 0.0             # flou local quand le sujet surcharge l’attention
    saturation_memory: float = 0.0          # trace d’usure accumulée sur ce sujet
    pull_release_need: float = 0.0          # besoin de lâcher un focus trop fixé

    # Couches V6 : champ subconscient + anticipation + transitions fondues.
    subconscious_pressure: float = 0.0      # micro-pression périphérique, active sans focus conscient
    associative_echo: float = 0.0           # écho par association avec les sujets actifs
    future_pull: float = 0.0                # pré-attracteur : direction probable avant focus clair
    transition_blend: float = 0.0           # mélange progressif entre ancien et nouveau focus
    affective_narrowing: float = 0.0        # rétrécissement du champ sous tension/douleur

    # Couches V7 finales : attention incarnée sans reprendre le rôle mémoire/bouche/impulsion.
    micro_instability: float = 0.0          # tremblement naturel du focus, non aléatoire et borné
    fragmented_presence: float = 0.0        # part du sujet présente en parallèle du focus principal
    protective_guard: float = 0.0           # garde attentionnelle : protège cohérence / règles profondes
    temporal_drag: float = 0.0              # inertie vécue : le sujet ralentit le basculement
    relational_pull: float = 0.0            # attraction liée au rapport user↔Leia sans produire de texte
    autonomous_drift: float = 0.0           # dérive silencieuse quand aucun input clair ne domine
    scar_sensitivity: float = 0.0           # sensibilité acquise par répétition/rupture/surcharge

    # Couches V8 finalisation organique : pré-conscient, désir, intrusion, vécu.
    preconscious_charge: float = 0.0        # pression avant sujet clair, sans objet verbal
    autonomous_desire: float = 0.0          # envie attentionnelle propre au champ
    intrusive_rise: float = 0.0             # remontée spontanée depuis le périphérique
    scar_distortion: float = 0.0            # déformation comportementale durable par blessure
    lived_expectation: float = 0.0          # attente/anticipation ressentie
    unresolved_need: float = 0.0            # besoin interne de résolution
    regret_trace: float = 0.0               # trace de retour vers ce qui a été lâché trop vite
    asymmetrical_delay: float = 0.0         # retard non symétrique avant bascule

    # Couches V9 de finition : dérive, hantise, rappel et récupération organique.
    drift_vector: float = 0.0              # dérive lente du focus hors stimulus direct
    haunting_level: float = 0.0            # ancien sujet qui continue à hanter le champ
    organic_fatigue: float = 0.0           # fatigue locale vécue, plus fine que directional_fatigue
    affective_memory_bias: float = 0.0     # préférence/sensibilité durable du focus
    micro_chaos: float = 0.0               # fluctuation minimale bornée, non aléatoire
    involuntary_recall: float = 0.0        # rappel involontaire d'un ancien focus
    recovery_need: float = 0.0             # besoin de stabilisation après surcharge

    # Couches V10 : besoins, conflit organique, sédimentation et subconscient actif.
    attention_need: float = 0.0            # besoin interne que ce sujet soit traité/stabilisé
    resolution_hunger: float = 0.0         # faim de résolution, distincte du simple unresolved booléen
    safety_need: float = 0.0               # besoin de sécuriser/protéger avant de continuer
    conflict_pressure: float = 0.0         # conflit entre attraction, évitement, douleur et devoir de cohérence
    attachment_depth: float = 0.0          # attachement attentionnel durable, sédimenté par retours/résonance
    sedimented_charge: float = 0.0         # mémoire attentionnelle lente : charge historique cumulative
    subconscious_override: float = 0.0     # capacité du subconscient à interrompre/reprendre le focus
    abandonment_shock: float = 0.0         # choc quand un sujet est lâché trop vite
    lived_stagnation: float = 0.0          # sensation interne de stagnation, pas seulement compteur anti-boucle
    saturation_distress: float = 0.0       # douleur de surcharge locale quand le champ devient trop plein
    attractor_mutation: float = 0.0        # mutation lente d'un attracteur en fixation/attachement

    # Couches V11 : finition organique profonde, sans texte ni rôle mémoire.
    somatic_rhythm: float = 0.0            # pulsation attentionnelle propre au sujet
    breath_sensitivity: float = 0.0        # sensibilité du sujet à la respiration globale
    scar_gravity_bias: float = 0.0         # biais durable de gravité né des cicatrices
    autonomous_resurgence: float = 0.0     # remontée spontanée lente depuis le pré-conscient
    lived_time_warp: float = 0.0           # distorsion subjective du temps local
    focus_viscosity: float = 0.0           # difficulté organique à quitter/entrer dans ce focus
    nonlinear_decay_bias: float = 0.0      # disparition irrégulière, non purement linéaire

    # Couches V12 de verrouillage final : style attentionnel mutable + vide actif.
    # Elles restent strictement attentionnelles : aucun texte, aucun template, aucune logique de bouche.
    attention_style_mutation: float = 0.0  # changement lent de la manière d'être attentif à ce sujet
    void_deformation: float = 0.0          # déformation locale créée par le vide attentionnel
    irrational_pull: float = 0.0           # attirance non optimale mais organique, bornée
    scar_perception_bias: float = 0.0      # biais durable qui change la perception future du sujet

    # Couches V13 : finition concrète demandée pour l'attention réellement organique.
    # Elles ne parlent pas, ne remplacent pas la mémoire, et ne créent pas d'impulsions :
    # elles modifient seulement la manière dont le focus se maintient, respire, hésite et revient.
    focus_self_deformation: float = 0.0    # le focus se déforme lui-même par son vécu interne
    long_attention_personality: float = 0.0 # style attentionnel persistant propre à ce sujet
    respiration_cycle_pressure: float = 0.0 # contraction/relâchement local du cycle attentionnel
    durable_double_bind: float = 0.0       # tiraillement durable attraction/évitement/cohérence
    subjective_time_distortion: float = 0.0 # accélération/ralentissement local du temps vécu
    external_coupling_readiness: float = 0.0 # lisibilité pour les autres moteurs Azip, sans les dupliquer

    # Couches V14 : finalisation concrète de l'attention organique.
    # Elles restent strictement attentionnelles : aucune phrase, aucune liste de mots, aucune bouche dupliquée.
    crystallized_bias: float = 0.0          # habitude attentionnelle devenue durable, lente à défaire
    survival_closure: float = 0.0           # fermeture défensive automatique quand la cohérence est menacée
    involuntary_takeover: float = 0.0       # capacité concrète d'un sujet périphérique à voler le focus
    relational_role_pressure: float = 0.0   # rôle organique du sujet dans le champ interne des autres sujets
    rivalry_pressure: float = 0.0           # compétition vivante avec sujets voisins, non lexicale
    protection_pressure: float = 0.0        # tendance à protéger/stabiliser d'autres sujets ou règles profondes
    spontaneous_bifurcation: float = 0.0    # bifurcation organique bornée, non aléatoire
    expressive_pressure: float = 0.0        # pression exportable vers la bouche, sans générer le texte

    def clamp(self) -> None:
        self.gravity = max(0.0, min(1.0, self.gravity))
        self.wound_level = max(0.0, min(1.0, self.wound_level))
        self.residue_strength = max(0.0, min(1.0, self.residue_strength))
        self.silent_pressure = max(0.0, min(1.0, self.silent_pressure))
        self.unspoken_pull = max(0.0, min(1.0, self.unspoken_pull))
        self.return_pressure = max(0.0, min(1.0, self.return_pressure))
        self.subjective_age = max(0.0, self.subjective_age)
        self.felt_duration = max(0.0, min(1.0, self.felt_duration))
        self.decay_speed = max(0.15, min(2.5, self.decay_speed))
        self.return_latency = max(0.0, min(1.0, self.return_latency))
        self.half_focus_level = max(0.0, min(1.0, self.half_focus_level))
        self.emotional_gravity_bias = max(0.0, min(1.0, self.emotional_gravity_bias))
        self.directional_fatigue = max(0.0, min(1.0, self.directional_fatigue))
        self.resonance_level = max(0.0, min(1.0, self.resonance_level))
        self.subjective_proximity = max(0.0, min(1.0, self.subjective_proximity))
        self.instability = max(0.0, min(1.0, self.instability))
        self.attention_habit = max(0.0, min(1.0, self.attention_habit))
        self.identity_weight = max(0.0, min(1.0, self.identity_weight))
        self.existential_charge = max(0.0, min(1.0, self.existential_charge))
        self.self_binding = max(0.0, min(1.0, self.self_binding))
        self.obsession_fixation = max(0.0, min(1.0, self.obsession_fixation))
        self.avoidance_pressure = max(0.0, min(1.0, self.avoidance_pressure))
        self.cognitive_pain = max(0.0, min(1.0, self.cognitive_pain))
        self.void_pull = max(0.0, min(1.0, self.void_pull))
        self.implicit_missing_pressure = max(0.0, min(1.0, self.implicit_missing_pressure))
        self.turbulence = max(0.0, min(1.0, self.turbulence))
        self.latent_focus_pressure = max(0.0, min(1.0, self.latent_focus_pressure))
        self.precision_loss = max(0.0, min(1.0, self.precision_loss))
        self.saturation_memory = max(0.0, min(1.0, self.saturation_memory))
        self.pull_release_need = max(0.0, min(1.0, self.pull_release_need))
        self.subconscious_pressure = max(0.0, min(1.0, self.subconscious_pressure))
        self.associative_echo = max(0.0, min(1.0, self.associative_echo))
        self.future_pull = max(0.0, min(1.0, self.future_pull))
        self.transition_blend = max(0.0, min(1.0, self.transition_blend))
        self.affective_narrowing = max(0.0, min(1.0, self.affective_narrowing))
        self.micro_instability = max(0.0, min(1.0, self.micro_instability))
        self.fragmented_presence = max(0.0, min(1.0, self.fragmented_presence))
        self.protective_guard = max(0.0, min(1.0, self.protective_guard))
        self.temporal_drag = max(0.0, min(1.0, self.temporal_drag))
        self.relational_pull = max(0.0, min(1.0, self.relational_pull))
        self.autonomous_drift = max(0.0, min(1.0, self.autonomous_drift))
        self.scar_sensitivity = max(0.0, min(1.0, self.scar_sensitivity))
        self.preconscious_charge = max(0.0, min(1.0, self.preconscious_charge))
        self.autonomous_desire = max(0.0, min(1.0, self.autonomous_desire))
        self.intrusive_rise = max(0.0, min(1.0, self.intrusive_rise))
        self.scar_distortion = max(0.0, min(1.0, self.scar_distortion))
        self.lived_expectation = max(0.0, min(1.0, self.lived_expectation))
        self.unresolved_need = max(0.0, min(1.0, self.unresolved_need))
        self.regret_trace = max(0.0, min(1.0, self.regret_trace))
        self.asymmetrical_delay = max(0.0, min(1.0, self.asymmetrical_delay))
        self.drift_vector = max(0.0, min(1.0, self.drift_vector))
        self.haunting_level = max(0.0, min(1.0, self.haunting_level))
        self.organic_fatigue = max(0.0, min(1.0, self.organic_fatigue))
        self.affective_memory_bias = max(0.0, min(1.0, self.affective_memory_bias))
        self.micro_chaos = max(0.0, min(1.0, self.micro_chaos))
        self.involuntary_recall = max(0.0, min(1.0, self.involuntary_recall))
        self.recovery_need = max(0.0, min(1.0, self.recovery_need))
        self.attention_need = max(0.0, min(1.0, self.attention_need))
        self.resolution_hunger = max(0.0, min(1.0, self.resolution_hunger))
        self.safety_need = max(0.0, min(1.0, self.safety_need))
        self.conflict_pressure = max(0.0, min(1.0, self.conflict_pressure))
        self.attachment_depth = max(0.0, min(1.0, self.attachment_depth))
        self.sedimented_charge = max(0.0, min(1.0, self.sedimented_charge))
        self.subconscious_override = max(0.0, min(1.0, self.subconscious_override))
        self.abandonment_shock = max(0.0, min(1.0, self.abandonment_shock))
        self.lived_stagnation = max(0.0, min(1.0, self.lived_stagnation))
        self.saturation_distress = max(0.0, min(1.0, self.saturation_distress))
        self.attractor_mutation = max(0.0, min(1.0, self.attractor_mutation))
        self.somatic_rhythm = max(0.0, min(1.0, self.somatic_rhythm))
        self.breath_sensitivity = max(0.0, min(1.0, self.breath_sensitivity))
        self.scar_gravity_bias = max(0.0, min(1.0, self.scar_gravity_bias))
        self.autonomous_resurgence = max(0.0, min(1.0, self.autonomous_resurgence))
        self.lived_time_warp = max(0.0, min(1.0, self.lived_time_warp))
        self.focus_viscosity = max(0.0, min(1.0, self.focus_viscosity))
        self.nonlinear_decay_bias = max(0.0, min(1.0, self.nonlinear_decay_bias))
        self.attention_style_mutation = max(0.0, min(1.0, self.attention_style_mutation))
        self.void_deformation = max(0.0, min(1.0, self.void_deformation))
        self.irrational_pull = max(0.0, min(1.0, self.irrational_pull))
        self.scar_perception_bias = max(0.0, min(1.0, self.scar_perception_bias))
        self.focus_self_deformation = max(0.0, min(1.0, self.focus_self_deformation))
        self.long_attention_personality = max(0.0, min(1.0, self.long_attention_personality))
        self.respiration_cycle_pressure = max(0.0, min(1.0, self.respiration_cycle_pressure))
        self.durable_double_bind = max(0.0, min(1.0, self.durable_double_bind))
        self.subjective_time_distortion = max(0.0, min(1.0, self.subjective_time_distortion))
        self.external_coupling_readiness = max(0.0, min(1.0, self.external_coupling_readiness))
        self.crystallized_bias = max(0.0, min(1.0, self.crystallized_bias))
        self.survival_closure = max(0.0, min(1.0, self.survival_closure))
        self.involuntary_takeover = max(0.0, min(1.0, self.involuntary_takeover))
        self.relational_role_pressure = max(0.0, min(1.0, self.relational_role_pressure))
        self.rivalry_pressure = max(0.0, min(1.0, self.rivalry_pressure))
        self.protection_pressure = max(0.0, min(1.0, self.protection_pressure))
        self.spontaneous_bifurcation = max(0.0, min(1.0, self.spontaneous_bifurcation))
        self.expressive_pressure = max(0.0, min(1.0, self.expressive_pressure))
        self.texture.clamp()


@dataclass
class AttentionField:
    """Tension globale du champ attentionnel, pas seulement sujet par sujet."""
    primary_secondary_tension: float = 0.0
    deep_rule_tension: float = 0.0
    continuity_break_tension: float = 0.0
    overload_clarity_tension: float = 0.0
    contamination_tension: float = 0.0
    void_tension: float = 0.0
    existential_tension: float = 0.0
    pain_tension: float = 0.0
    turbulence_tension: float = 0.0
    latent_tension: float = 0.0
    precision_tension: float = 0.0
    subconscious_tension: float = 0.0
    anticipatory_tension: float = 0.0
    transition_blend_tension: float = 0.0
    micro_instability_tension: float = 0.0
    fragmentation_presence_tension: float = 0.0
    protective_guard_tension: float = 0.0
    temporal_drag_tension: float = 0.0
    relational_tension: float = 0.0
    autonomous_drift_tension: float = 0.0
    preconscious_tension: float = 0.0
    cognitive_weather_tension: float = 0.0
    autonomous_desire_tension: float = 0.0
    subconscious_intrusion_tension: float = 0.0
    scar_distortion_tension: float = 0.0
    lived_temporality_tension: float = 0.0
    attention_need_tension: float = 0.0
    organic_conflict_tension: float = 0.0
    sedimentation_tension: float = 0.0
    subconscious_override_tension: float = 0.0
    saturation_distress_tension: float = 0.0
    organic_respiration_tension: float = 0.0
    autonomous_resurgence_tension: float = 0.0
    scar_gravity_tension: float = 0.0
    lived_time_warp_tension: float = 0.0
    attention_style_mutation_tension: float = 0.0
    active_void_deformation_tension: float = 0.0
    irrational_pull_tension: float = 0.0
    focus_self_deformation_tension: float = 0.0
    attention_personality_tension: float = 0.0
    durable_double_bind_tension: float = 0.0
    subjective_time_distortion_tension: float = 0.0
    external_coupling_tension: float = 0.0
    crystallized_bias_tension: float = 0.0
    survival_closure_tension: float = 0.0
    involuntary_takeover_tension: float = 0.0
    relational_ecology_tension: float = 0.0
    spontaneous_bifurcation_tension: float = 0.0
    expressive_pressure_tension: float = 0.0

    def total(self) -> float:
        return max(0.0, min(1.0, (
            self.primary_secondary_tension * 0.22
            + self.deep_rule_tension * 0.24
            + self.continuity_break_tension * 0.20
            + self.overload_clarity_tension * 0.16
            + self.contamination_tension * 0.12
            + self.void_tension * 0.08
            + self.existential_tension * 0.08
            + self.pain_tension * 0.06
            + self.turbulence_tension * 0.06
            + self.latent_tension * 0.05
            + self.precision_tension * 0.05
            + self.subconscious_tension * 0.07
            + self.anticipatory_tension * 0.06
            + self.transition_blend_tension * 0.05
            + self.micro_instability_tension * 0.05
            + self.fragmentation_presence_tension * 0.05
            + self.protective_guard_tension * 0.06
            + self.temporal_drag_tension * 0.04
            + self.relational_tension * 0.04
            + self.autonomous_drift_tension * 0.04
            + self.preconscious_tension * 0.06
            + self.cognitive_weather_tension * 0.05
            + self.autonomous_desire_tension * 0.05
            + self.subconscious_intrusion_tension * 0.05
            + self.scar_distortion_tension * 0.05
            + self.lived_temporality_tension * 0.05
            + self.attention_need_tension * 0.07
            + self.organic_conflict_tension * 0.07
            + self.sedimentation_tension * 0.05
            + self.subconscious_override_tension * 0.06
            + self.saturation_distress_tension * 0.06
            + self.organic_respiration_tension * 0.05
            + self.autonomous_resurgence_tension * 0.06
            + self.scar_gravity_tension * 0.06
            + self.lived_time_warp_tension * 0.05
            + self.attention_style_mutation_tension * 0.06
            + self.active_void_deformation_tension * 0.05
            + self.irrational_pull_tension * 0.04
            + self.focus_self_deformation_tension * 0.06
            + self.attention_personality_tension * 0.05
            + self.durable_double_bind_tension * 0.07
            + self.subjective_time_distortion_tension * 0.05
            + self.external_coupling_tension * 0.04
            + self.crystallized_bias_tension * 0.06
            + self.survival_closure_tension * 0.07
            + self.involuntary_takeover_tension * 0.08
            + self.relational_ecology_tension * 0.05
            + self.spontaneous_bifurcation_tension * 0.05
            + self.expressive_pressure_tension * 0.04
        )))

    def as_dict(self) -> Dict[str, float]:
        return {
            "primary_secondary_tension": self.primary_secondary_tension,
            "deep_rule_tension": self.deep_rule_tension,
            "continuity_break_tension": self.continuity_break_tension,
            "overload_clarity_tension": self.overload_clarity_tension,
            "contamination_tension": self.contamination_tension,
            "void_tension": self.void_tension,
            "existential_tension": self.existential_tension,
            "pain_tension": self.pain_tension,
            "turbulence_tension": self.turbulence_tension,
            "latent_tension": self.latent_tension,
            "precision_tension": self.precision_tension,
            "subconscious_tension": self.subconscious_tension,
            "anticipatory_tension": self.anticipatory_tension,
            "transition_blend_tension": self.transition_blend_tension,
            "micro_instability_tension": self.micro_instability_tension,
            "fragmentation_presence_tension": self.fragmentation_presence_tension,
            "protective_guard_tension": self.protective_guard_tension,
            "temporal_drag_tension": self.temporal_drag_tension,
            "relational_tension": self.relational_tension,
            "autonomous_drift_tension": self.autonomous_drift_tension,
            "preconscious_tension": self.preconscious_tension,
            "cognitive_weather_tension": self.cognitive_weather_tension,
            "autonomous_desire_tension": self.autonomous_desire_tension,
            "subconscious_intrusion_tension": self.subconscious_intrusion_tension,
            "scar_distortion_tension": self.scar_distortion_tension,
            "lived_temporality_tension": self.lived_temporality_tension,
            "attention_need_tension": self.attention_need_tension,
            "organic_conflict_tension": self.organic_conflict_tension,
            "sedimentation_tension": self.sedimentation_tension,
            "subconscious_override_tension": self.subconscious_override_tension,
            "saturation_distress_tension": self.saturation_distress_tension,
            "organic_respiration_tension": self.organic_respiration_tension,
            "autonomous_resurgence_tension": self.autonomous_resurgence_tension,
            "scar_gravity_tension": self.scar_gravity_tension,
            "lived_time_warp_tension": self.lived_time_warp_tension,
            "attention_style_mutation_tension": self.attention_style_mutation_tension,
            "active_void_deformation_tension": self.active_void_deformation_tension,
            "irrational_pull_tension": self.irrational_pull_tension,
            "focus_self_deformation_tension": self.focus_self_deformation_tension,
            "attention_personality_tension": self.attention_personality_tension,
            "durable_double_bind_tension": self.durable_double_bind_tension,
            "subjective_time_distortion_tension": self.subjective_time_distortion_tension,
            "external_coupling_tension": self.external_coupling_tension,
            "crystallized_bias_tension": self.crystallized_bias_tension,
            "survival_closure_tension": self.survival_closure_tension,
            "involuntary_takeover_tension": self.involuntary_takeover_tension,
            "relational_ecology_tension": self.relational_ecology_tension,
            "spontaneous_bifurcation_tension": self.spontaneous_bifurcation_tension,
            "expressive_pressure_tension": self.expressive_pressure_tension,
            "total": self.total(),
        }


@dataclass
class AttentionState:
    """État complet exporté par le moteur après chaque tour."""
    primary_focus: str
    secondary_foci: List[str]
    background_foci: List[str]

    inertia_level: float
    fragmentation_level: float
    stability: float
    continuity_score: float

    unresolved_subjects: List[str]
    subject_gravity: Dict[str, float]

    attention_tension: float
    probable_direction: Optional[str]

    offtrack_risk: float
    forgetting_risk: float

    interruption_type: InterruptionType
    shift_magnitude: float
    focus_trajectory: List[str]
    wound_alerts: List[str]

    # Export enrichi pour la bouche expressive.
    silent_pressure: Dict[str, float] = field(default_factory=dict)
    attention_fatigue: float = 0.0
    dominant_texture: Dict[str, float] = field(default_factory=dict)
    contaminated_rules: List[str] = field(default_factory=list)
    subjective_time_flow: float = 0.5
    returning_subjects: List[str] = field(default_factory=list)
    almost_forgotten_subjects: List[str] = field(default_factory=list)
    field_tension: Dict[str, float] = field(default_factory=dict)
    half_focus: Dict[str, float] = field(default_factory=dict)

    # Exports V3 pour les autres moteurs, sans génération de texte.
    organic_breath: float = 0.5
    emotional_gravity: Dict[str, float] = field(default_factory=dict)
    resonance_map: Dict[str, float] = field(default_factory=dict)
    directional_fatigue: Dict[str, float] = field(default_factory=dict)
    attention_habits: Dict[str, float] = field(default_factory=dict)
    instability_map: Dict[str, float] = field(default_factory=dict)
    subjective_proximity: Dict[str, float] = field(default_factory=dict)
    existential_charge: Dict[str, float] = field(default_factory=dict)
    obsession_map: Dict[str, float] = field(default_factory=dict)
    avoidance_map: Dict[str, float] = field(default_factory=dict)
    cognitive_pain_map: Dict[str, float] = field(default_factory=dict)
    void_map: Dict[str, float] = field(default_factory=dict)
    implicit_missing_map: Dict[str, float] = field(default_factory=dict)
    turbulence_map: Dict[str, float] = field(default_factory=dict)
    attention_void: float = 0.0
    latent_focus_map: Dict[str, float] = field(default_factory=dict)
    precision_loss_map: Dict[str, float] = field(default_factory=dict)
    saturation_memory_map: Dict[str, float] = field(default_factory=dict)
    pull_release_map: Dict[str, float] = field(default_factory=dict)
    attentional_scars: Dict[str, float] = field(default_factory=dict)
    global_precision: float = 1.0
    subconscious_field: Dict[str, float] = field(default_factory=dict)
    associative_echo_map: Dict[str, float] = field(default_factory=dict)
    future_attractor_map: Dict[str, float] = field(default_factory=dict)
    transition_blend_map: Dict[str, float] = field(default_factory=dict)
    affective_narrowing_map: Dict[str, float] = field(default_factory=dict)
    attention_bandwidth: float = 1.0
    attention_ready_for_expression: Dict[str, Any] = field(default_factory=dict)
    micro_instability_map: Dict[str, float] = field(default_factory=dict)
    fragmented_presence_map: Dict[str, float] = field(default_factory=dict)
    protective_guard_map: Dict[str, float] = field(default_factory=dict)
    temporal_drag_map: Dict[str, float] = field(default_factory=dict)
    relational_pull_map: Dict[str, float] = field(default_factory=dict)
    autonomous_drift_map: Dict[str, float] = field(default_factory=dict)
    scar_sensitivity_map: Dict[str, float] = field(default_factory=dict)
    global_living_attention: Dict[str, float] = field(default_factory=dict)
    preconscious_field: Dict[str, float] = field(default_factory=dict)
    cognitive_weather: Dict[str, float] = field(default_factory=dict)
    autonomous_desire_map: Dict[str, float] = field(default_factory=dict)
    subconscious_intrusion_map: Dict[str, float] = field(default_factory=dict)
    scar_distortion_map: Dict[str, float] = field(default_factory=dict)
    lived_temporality_map: Dict[str, float] = field(default_factory=dict)
    attention_need_map: Dict[str, float] = field(default_factory=dict)
    organic_conflict_map: Dict[str, float] = field(default_factory=dict)
    sedimented_attention_map: Dict[str, float] = field(default_factory=dict)
    subconscious_override_map: Dict[str, float] = field(default_factory=dict)
    saturation_distress_map: Dict[str, float] = field(default_factory=dict)
    somatic_rhythm_map: Dict[str, float] = field(default_factory=dict)
    scar_gravity_bias_map: Dict[str, float] = field(default_factory=dict)
    autonomous_resurgence_map: Dict[str, float] = field(default_factory=dict)
    lived_time_warp_map: Dict[str, float] = field(default_factory=dict)
    focus_viscosity_map: Dict[str, float] = field(default_factory=dict)
    organic_respiration: Dict[str, float] = field(default_factory=dict)
    attention_style_mutation_map: Dict[str, float] = field(default_factory=dict)
    void_deformation_map: Dict[str, float] = field(default_factory=dict)
    irrational_pull_map: Dict[str, float] = field(default_factory=dict)
    scar_perception_bias_map: Dict[str, float] = field(default_factory=dict)
    focus_self_deformation_map: Dict[str, float] = field(default_factory=dict)
    attention_personality_map: Dict[str, float] = field(default_factory=dict)
    respiration_cycle_map: Dict[str, float] = field(default_factory=dict)
    durable_double_bind_map: Dict[str, float] = field(default_factory=dict)
    subjective_time_distortion_map: Dict[str, float] = field(default_factory=dict)
    azip_coupling_map: Dict[str, float] = field(default_factory=dict)
    crystallized_bias_map: Dict[str, float] = field(default_factory=dict)
    survival_closure_map: Dict[str, float] = field(default_factory=dict)
    involuntary_takeover_map: Dict[str, float] = field(default_factory=dict)
    relational_ecology_map: Dict[str, Dict[str, float]] = field(default_factory=dict)
    spontaneous_bifurcation_map: Dict[str, float] = field(default_factory=dict)
    expressive_attention_pressure: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class AttentionDiagnostic:
    """Export de diagnostic interne vers les autres modules (pas l'utilisateur)."""
    dominant_reason: str
    secondary_reasons: Dict[str, str]
    existing_tensions: List[str]
    forgetting_risk_subjects: List[str]
    recurrent_subjects: List[str]
    open_loops: List[str]
    last_interruption: InterruptionType
    field_tension: Dict[str, float] = field(default_factory=dict)
    silent_subjects: List[str] = field(default_factory=list)
    fatigue_reason: str = ""


# ---------------------------------------------------------------------------
# Moteur principal
# ---------------------------------------------------------------------------

class LivingAttentionEngine:
    """
    Moteur d'attention vivante.

    Reçoit les signaux du moteur impulsionnel, des attracteurs, de la mémoire,
    et de la présence — mais ne les recalcule pas.
    Produit un AttentionState exportable vers la bouche expressive.
    """

    # Les règles profondes restent injectables depuis memory_hints/message_metadata.
    # Les valeurs par défaut sont seulement une base de compatibilité si aucun
    # moteur mémoire/règles projet ne fournit encore ces signaux.
    DEFAULT_DEEP_RULES: Set[str] = {
        "pas_de_preecrit",
        "ne_casse_pas_les_autres_fichiers",
        "pas_de_squelette",
        "100_pourcent_vivant",
        "ne_duplique_pas_les_fonctions",
        "prends_ton_temps",
        "coherence_globale",
    }

    DEFAULT_RULE_LINKS: Dict[str, Set[str]] = {}

    RESIDUE_DECAY_RATE: float = 0.25
    RESIDUE_MIN_GRAVITY: float = 0.15
    INERTIA_DECAY: float = 0.2
    LOOP_STAGNATION_LIMIT: int = 4
    WOUND_ACCUMULATION: float = 0.2
    WOUND_HEALING: float = 0.05

    def __init__(
        self,
        deep_rules: Optional[Set[str]] = None,
        rule_links: Optional[Dict[str, Set[str]]] = None,
        max_subjects: int = 96,
        archive_limit: int = 64,
    ):
        self.deep_rules: Set[str] = set(deep_rules or self.DEFAULT_DEEP_RULES)
        self.rule_links: Dict[str, Set[str]] = {
            str(k): set(v or set()) for k, v in (rule_links or self.DEFAULT_RULE_LINKS).items()
        }
        self.max_subjects = max(24, int(max_subjects))
        self.archive_limit = max(12, int(archive_limit))
        self.archived_subjects: Dict[str, Dict[str, Any]] = {}

        self.subjects: Dict[str, AttentionSubject] = {}
        self._init_deep_rules()

        self.focus_history: List[str] = []
        self.inertia: float = 0.0
        self.last_interruption: InterruptionType = InterruptionType.NONE
        self.stagnation_counter: int = 0
        self.last_primary: Optional[str] = None
        self.current_turn_candidates: Set[str] = set()
        self.previous_state: Optional[AttentionState] = None

        # Nouvelles couches globales.
        self.attention_fatigue: float = 0.0
        self.subjective_time_flow: float = 0.5
        self.field = AttentionField()
        self.internal_clock: float = 0.0
        self.last_fatigue_reason: str = "stable"

        # V3 : rythme interne et mémoire de chemins attentionnels.
        self.organic_breath: float = 0.5
        self.breath_phase: float = 0.0
        self.attention_habits: Dict[Tuple[str, str], float] = {}
        self.last_transition: Optional[Tuple[str, str]] = None

        # V4 : dynamique profonde du champ.
        self.attention_void: float = 0.0
        self.unspoken_global_pressure: float = 0.0
        self.turbulence_memory: float = 0.0
        self.global_precision: float = 1.0
        self.attentional_scars: Dict[str, float] = {
            "contradiction": 0.0,
            "overload": 0.0,
            "rupture": 0.0,
            "repetition": 0.0,
            "unresolved": 0.0,
        }

        # V6 : le champ mental ne se limite pas au focus conscient.
        self.global_subconscious_pressure: float = 0.0
        self.anticipatory_pressure: float = 0.0
        self.transition_blend_level: float = 0.0
        self.attention_bandwidth: float = 1.0

        # V7 : couches finales d'attention incarnée.
        self.global_micro_instability: float = 0.0
        self.global_fragmented_presence: float = 0.0
        self.global_protective_guard: float = 0.0
        self.global_temporal_drag: float = 0.0
        self.global_relational_pull: float = 0.0
        self.global_autonomous_drift: float = 0.0

        # V8 : finalisation organique du moteur attentionnel.
        # Ces couches restent attentionnelles : elles ne génèrent pas de texte,
        # ne remplacent pas la mémoire et ne décident pas des impulsions.
        self.global_preconscious_charge: float = 0.0
        self.global_autonomous_desire: float = 0.0
        self.global_subconscious_intrusion: float = 0.0
        self.global_scar_distortion: float = 0.0
        self.global_lived_temporality: float = 0.0
        self.cognitive_weather: Dict[str, float] = {
            "heaviness": 0.0,
            "nervousness": 0.0,
            "openness": 0.5,
            "expectancy": 0.0,
            "fragility": 0.0,
            "clarity": 1.0,
        }

        # V9 : états globaux de finition organique.
        self.global_drift_field: float = 0.0
        self.global_residual_haunting: float = 0.0
        self.global_affective_focus_memory: float = 0.0
        self.global_controlled_micro_chaos: float = 0.0
        self.global_involuntary_recall: float = 0.0
        self.global_recovery_need: float = 0.0

        # V10 : force vécue, conflit organique et sédimentation historique.
        self.global_attention_need: float = 0.0
        self.global_organic_conflict: float = 0.0
        self.global_sedimented_attention: float = 0.0
        self.global_subconscious_override: float = 0.0
        self.global_saturation_distress: float = 0.0

        # V11 : respiration globale, cicatrice durable et remontée autonome.
        self.global_respiration_contraction: float = 0.0
        self.global_respiration_release: float = 0.0
        self.global_scar_gravity_bias: float = 0.0
        self.global_autonomous_resurgence: float = 0.0
        self.global_lived_time_warp: float = 0.0
        self.global_focus_viscosity: float = 0.0

        # V12 : finition concrète — mutation du style attentionnel, vide actif,
        # biais de cicatrice et attraction irrationnelle organique.
        self.global_attention_style_mutation: float = 0.0
        self.global_active_void_deformation: float = 0.0
        self.global_irrational_pull: float = 0.0
        self.global_scar_perception_bias: float = 0.0

        # V13 : fermeture propre du moteur attentionnel organique.
        self.global_focus_self_deformation: float = 0.0
        self.global_attention_personality: float = 0.0
        self.global_respiration_cycle_pressure: float = 0.0
        self.global_durable_double_bind: float = 0.0
        self.global_subjective_time_distortion: float = 0.0
        self.global_azip_coupling_readiness: float = 0.0

        # V14 : agrégats finaux pour irréversibilité, survie, intrusion et écologie relationnelle.
        self.global_crystallized_bias: float = 0.0
        self.global_survival_closure: float = 0.0
        self.global_involuntary_takeover: float = 0.0
        self.global_relational_ecology: float = 0.0
        self.global_spontaneous_bifurcation: float = 0.0
        self.global_expressive_pressure: float = 0.0

    # ------------------------------------------------------------------
    # Point d'entrée principal
    # ------------------------------------------------------------------

    def update(
        self,
        impulse_signals: Dict[str, Any],
        attractors: Dict[str, float],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        message_metadata: Dict[str, Any],
    ) -> Tuple[AttentionState, AttentionDiagnostic]:
        """
        Met à jour l'état attentionnel complet à chaque tour.

        Aucun texte public n'est produit ici. Les clés peuvent être absentes :
        le moteur reste compatible avec les versions plus simples.
        """
        impulse_signals = impulse_signals or {}
        attractors = attractors or {}
        memory_hints = memory_hints or {}
        presence_signal = presence_signal or {}
        message_metadata = message_metadata or {}

        self.internal_clock += 1.0
        self._ingest_external_deep_rules(memory_hints, message_metadata)

        # 0. Temps subjectif + résidus avant tout.
        self._update_subjective_time(impulse_signals, presence_signal)
        self._decay_residues()

        # 1. Nature de la transition.
        interruption = self._detect_interruption(message_metadata, impulse_signals)
        self.last_interruption = interruption

        # 2. Sujets candidats.
        self._integrate_candidate_subjects(
            message_metadata.get("candidate_subjects", []),
            message_metadata.get("hierarchy_level", HierarchyLevel.IMMEDIATE_MESSAGE),
            memory_hints,
            impulse_signals,
            attractors,
        )

        # 3. Plaies, fermeture, guérison.
        self._apply_error_signals(message_metadata.get("error_signals", []))
        self._close_subjects(message_metadata.get("explicitly_closed", []))
        self._heal_wounds(message_metadata.get("error_signals", []))

        # 4. Texture, contamination, pression silencieuse, fatigue.
        self._update_subject_textures(impulse_signals, presence_signal, message_metadata)
        self._apply_subject_contamination(attractors, impulse_signals)
        self._update_silent_pressures(impulse_signals, memory_hints)
        self._update_attention_fatigue(impulse_signals, message_metadata)
        self._update_attention_breath(impulse_signals, presence_signal)
        self._update_emotional_gravity_bias(impulse_signals, memory_hints)
        self._update_directional_fatigue_and_proximity(impulse_signals)
        self._update_existential_charge(impulse_signals, memory_hints, presence_signal)
        self._update_implicit_missing_pressure(impulse_signals, memory_hints, message_metadata)
        self._update_cognitive_pain_and_avoidance(impulse_signals, presence_signal)
        self._update_obsession_and_void(impulse_signals, message_metadata)
        self._apply_attention_turbulence(impulse_signals)
        self._update_attentional_scars(impulse_signals, message_metadata, interruption)
        self._update_latent_focus_and_precision(impulse_signals, memory_hints)
        self._update_subconscious_field(impulse_signals, memory_hints, interruption)
        self._update_deep_living_attention_layers(impulse_signals, memory_hints, presence_signal, interruption)
        self._update_preconscious_and_weather(impulse_signals, memory_hints, presence_signal, interruption)
        self._update_affective_focus_memory(impulse_signals, memory_hints, interruption)
        self._update_residual_haunting(impulse_signals, memory_hints, interruption)
        self._update_organic_drift_field(impulse_signals, attractors, presence_signal, interruption)
        self._update_attention_recovery_phase(impulse_signals, presence_signal, interruption)
        self._update_autonomous_attention_desire(impulse_signals, attractors, memory_hints)
        self._update_involuntary_recall_layer(impulse_signals, memory_hints, interruption)
        self._update_controlled_micro_chaos(impulse_signals, presence_signal)
        self._update_subconscious_intrusions_and_temporality(impulse_signals, memory_hints, interruption)
        self._update_attention_needs_and_conflicts(impulse_signals, memory_hints, presence_signal, interruption)
        self._update_sedimented_attention_memory(impulse_signals, memory_hints, interruption)
        self._update_subconscious_override_layer(impulse_signals, memory_hints, interruption)
        self._update_organic_field_respiration(impulse_signals, presence_signal, interruption)
        self._update_deep_scar_gravity(memory_hints, interruption)
        self._update_autonomous_preconscious_resurgence(impulse_signals, memory_hints, interruption)
        self._update_lived_time_warp(impulse_signals, presence_signal, interruption)
        self._update_attention_style_mutation_and_void_deformation(impulse_signals, memory_hints, presence_signal, interruption)
        self._update_final_organic_attention_closure(impulse_signals, attractors, memory_hints, presence_signal, interruption)
        self._crystallize_attention_personality(impulse_signals, memory_hints, interruption)
        self._update_subject_relational_ecology(impulse_signals, attractors, memory_hints, interruption)
        self._apply_cognitive_survival_instinct(impulse_signals, presence_signal, interruption)
        self._activate_subconscious_takeovers(impulse_signals, memory_hints, interruption)
        self._apply_organic_bifurcations(impulse_signals, attractors, presence_signal, interruption)
        self._update_expression_coupling_pressure(impulse_signals, presence_signal, interruption)
        self._update_future_attractors(impulse_signals, attractors, memory_hints)
        self._soften_attention_transitions(interruption)

        # 5. Gravités avec influence profonde des attracteurs.
        self._recompute_gravities(attractors, presence_signal, impulse_signals)
        self._apply_attractor_dynamics(attractors, impulse_signals)
        self._apply_resonance_coalitions(impulse_signals)
        self._apply_organic_instability(impulse_signals)

        # 6. Focus principal + anti-boucle organique.
        primary = self._elect_primary_focus(impulse_signals, interruption)
        primary = self._apply_anti_loop(primary, impulse_signals)

        # 7. Demi-focus, secondaires, champ.
        self._update_half_focus(primary, impulse_signals)
        secondary, background = self._elect_secondary_and_background(primary)
        self._update_field_tension(primary, secondary, impulse_signals, interruption)

        # 8. Trajectoire émergente.
        self._evolve_focus_trajectory(primary, secondary, impulse_signals, attractors)
        self._update_attention_habits(primary, secondary)

        # 9. Métriques.
        fragmentation = self._compute_fragmentation(impulse_signals, message_metadata)
        inertia = self._compute_inertia(primary, interruption, impulse_signals)
        self.inertia = inertia
        stability = self._compute_stability(primary, impulse_signals, presence_signal)
        continuity = self._compute_continuity(primary)
        tension = self._compute_attention_tension(impulse_signals, fragmentation)
        direction = self._predict_direction(primary, secondary, impulse_signals, attractors)
        offtrack_risk = self._compute_offtrack_risk(primary, impulse_signals)
        forgetting_risk = self._compute_forgetting_risk()
        wound_alerts = self._get_wound_alerts()

        expression_readiness = self._build_expression_readiness(
            primary, secondary, tension, fragmentation, stability, continuity, interruption
        )
        self._prune_subjects(primary, secondary)

        unresolved = [name for name, s in self.subjects.items() if s.unresolved]
        active_gravity = {
            name: s.gravity
            for name, s in self.subjects.items()
            if s.state not in (SubjectState.CLOSED,)
        }
        trajectory = self._get_focus_trajectory(primary)

        self.focus_history.append(primary)
        if len(self.focus_history) > 30:
            self.focus_history = self.focus_history[-30:]

        state = AttentionState(
            primary_focus=primary,
            secondary_foci=secondary,
            background_foci=background,
            inertia_level=inertia,
            fragmentation_level=fragmentation,
            stability=stability,
            continuity_score=continuity,
            unresolved_subjects=unresolved,
            subject_gravity=active_gravity,
            attention_tension=tension,
            probable_direction=direction,
            offtrack_risk=offtrack_risk,
            forgetting_risk=forgetting_risk,
            interruption_type=interruption,
            shift_magnitude=self._compute_shift(primary),
            focus_trajectory=trajectory,
            wound_alerts=wound_alerts,
            silent_pressure=self._export_silent_pressure(),
            attention_fatigue=self.attention_fatigue,
            dominant_texture=self._dominant_texture(primary),
            contaminated_rules=self._contaminated_rules(),
            subjective_time_flow=self.subjective_time_flow,
            returning_subjects=self._returning_subjects(),
            almost_forgotten_subjects=self._almost_forgotten_subjects(),
            field_tension=self.field.as_dict(),
            half_focus=self._export_half_focus(),
            organic_breath=self.organic_breath,
            emotional_gravity=self._export_emotional_gravity(),
            resonance_map=self._export_resonance_map(),
            directional_fatigue=self._export_directional_fatigue(),
            attention_habits=self._export_attention_habits(),
            instability_map=self._export_instability_map(),
            subjective_proximity=self._export_subjective_proximity(),
            existential_charge=self._export_existential_charge(),
            obsession_map=self._export_obsession_map(),
            avoidance_map=self._export_avoidance_map(),
            cognitive_pain_map=self._export_cognitive_pain_map(),
            void_map=self._export_void_map(),
            implicit_missing_map=self._export_implicit_missing_map(),
            turbulence_map=self._export_turbulence_map(),
            attention_void=self.attention_void,
            latent_focus_map=self._export_latent_focus_map(),
            precision_loss_map=self._export_precision_loss_map(),
            saturation_memory_map=self._export_saturation_memory_map(),
            pull_release_map=self._export_pull_release_map(),
            attentional_scars=dict(self.attentional_scars),
            global_precision=self.global_precision,
            subconscious_field=self._export_subconscious_field(),
            associative_echo_map=self._export_associative_echo_map(),
            future_attractor_map=self._export_future_attractor_map(),
            transition_blend_map=self._export_transition_blend_map(),
            affective_narrowing_map=self._export_affective_narrowing_map(),
            attention_bandwidth=self.attention_bandwidth,
            attention_ready_for_expression=expression_readiness,
            micro_instability_map=self._export_micro_instability_map(),
            fragmented_presence_map=self._export_fragmented_presence_map(),
            protective_guard_map=self._export_protective_guard_map(),
            temporal_drag_map=self._export_temporal_drag_map(),
            relational_pull_map=self._export_relational_pull_map(),
            autonomous_drift_map=self._export_autonomous_drift_map(),
            scar_sensitivity_map=self._export_scar_sensitivity_map(),
            global_living_attention=self._export_global_living_attention(),
            preconscious_field=self._export_preconscious_field(),
            cognitive_weather=dict(self.cognitive_weather),
            autonomous_desire_map=self._export_autonomous_desire_map(),
            subconscious_intrusion_map=self._export_subconscious_intrusion_map(),
            scar_distortion_map=self._export_scar_distortion_map(),
            lived_temporality_map=self._export_lived_temporality_map(),
            attention_need_map=self._export_attention_need_map(),
            organic_conflict_map=self._export_organic_conflict_map(),
            sedimented_attention_map=self._export_sedimented_attention_map(),
            subconscious_override_map=self._export_subconscious_override_map(),
            saturation_distress_map=self._export_saturation_distress_map(),
            somatic_rhythm_map=self._export_somatic_rhythm_map(),
            scar_gravity_bias_map=self._export_scar_gravity_bias_map(),
            autonomous_resurgence_map=self._export_autonomous_resurgence_map(),
            lived_time_warp_map=self._export_lived_time_warp_map(),
            focus_viscosity_map=self._export_focus_viscosity_map(),
            organic_respiration=self._export_organic_respiration(),
            attention_style_mutation_map=self._export_attention_style_mutation_map(),
            void_deformation_map=self._export_void_deformation_map(),
            irrational_pull_map=self._export_irrational_pull_map(),
            scar_perception_bias_map=self._export_scar_perception_bias_map(),
            focus_self_deformation_map=self._export_focus_self_deformation_map(),
            attention_personality_map=self._export_attention_personality_map(),
            respiration_cycle_map=self._export_respiration_cycle_map(),
            durable_double_bind_map=self._export_durable_double_bind_map(),
            subjective_time_distortion_map=self._export_subjective_time_distortion_map(),
            azip_coupling_map=self._export_azip_coupling_map(),
            crystallized_bias_map=self._export_crystallized_bias_map(),
            survival_closure_map=self._export_survival_closure_map(),
            involuntary_takeover_map=self._export_involuntary_takeover_map(),
            relational_ecology_map=self._export_relational_ecology_map(),
            spontaneous_bifurcation_map=self._export_spontaneous_bifurcation_map(),
            expressive_attention_pressure=self._export_expressive_attention_pressure(primary, secondary),
        )
        self.previous_state = state

        diagnostic = self._build_diagnostic(
            primary, secondary, tension, forgetting_risk, unresolved, interruption
        )

        # Important : last_primary doit rester le focus du tour précédent
        # pendant tout le calcul courant. On le met seulement à jour ici,
        # après l'anti-boucle et après les métriques qui comparent ancien/nouveau focus.
        self.last_primary = primary
        return state, diagnostic

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_deep_rules(self) -> None:
        for rule in self.deep_rules:
            self.subjects[rule] = AttentionSubject(
                name=rule,
                gravity=1.0,
                state=SubjectState.BACKGROUND,
                hierarchy_level=HierarchyLevel.DEEP_RULES,
                activation_count=0,
                wound_level=0.0,
                residue_strength=0.0,
                unresolved=False,
                texture=AttentionTexture(tension=0.18, openness=0.55, attraction=0.65, resistance=0.12, fragility=0.18, safety=0.70),
            )
            subj = self.subjects[rule]
            subj.identity_weight = 1.0
            subj.existential_charge = 0.72
            subj.self_binding = 0.64
            subj.clamp()

    @staticmethod
    def _clamp01(value: float) -> float:
        return max(0.0, min(1.0, float(value)))

    def _ingest_external_deep_rules(self, memory_hints: Dict[str, Any], message_metadata: Dict[str, Any]) -> None:
        """
        Reçoit les règles profondes depuis un moteur mémoire/règles projet.
        Ce moteur d’attention ne décide pas lui-même des règles du projet :
        il les garde seulement comme sujets profonds qui orientent l’attention.
        """
        incoming_rules = set(memory_hints.get("deep_rules", []) or message_metadata.get("deep_rules", []) or [])
        incoming_links = memory_hints.get("rule_links", {}) or message_metadata.get("rule_links", {}) or {}

        changed = False
        for rule in incoming_rules:
            rule = str(rule).strip()
            if not rule:
                continue
            if rule not in self.deep_rules:
                self.deep_rules.add(rule)
                changed = True

        for rule, links in incoming_links.items():
            rule = str(rule).strip()
            if not rule:
                continue
            self.deep_rules.add(rule)
            self.rule_links.setdefault(rule, set()).update(str(x).strip() for x in (links or []) if str(x).strip())
            changed = True

        if changed:
            self._init_deep_rules()

    @staticmethod
    def _as_level(level: Any) -> HierarchyLevel:
        if isinstance(level, HierarchyLevel):
            return level
        if isinstance(level, int):
            return HierarchyLevel(max(0, min(5, level)))
        if isinstance(level, str):
            try:
                return HierarchyLevel[level]
            except Exception:
                try:
                    return HierarchyLevel(level)
                except Exception:
                    return HierarchyLevel.IMMEDIATE_MESSAGE
        return HierarchyLevel.IMMEDIATE_MESSAGE

    # ------------------------------------------------------------------
    # Résidus + temps subjectif
    # ------------------------------------------------------------------

    def _update_subjective_time(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any]) -> None:
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))

        target_flow = self._clamp01(0.45 + curiosity * 0.18 + pressure * 0.10 - saturation * 0.22 + presence * 0.08)
        wave = math.sin(self.internal_clock * 0.37 + self.attention_fatigue * 1.9) * 0.025
        self.subjective_time_flow = self._clamp01(self.subjective_time_flow * 0.90 + target_flow * 0.10 + wave)

        for subj in self.subjects.values():
            if subj.state == SubjectState.ACTIVE:
                subj.subjective_age += self.subjective_time_flow * 0.55
            elif subj.state in (SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING):
                subj.subjective_age += self.subjective_time_flow * 0.35
            else:
                subj.subjective_age += self.subjective_time_flow * 0.18
            subj.felt_duration = self._clamp01(subj.felt_duration * 0.94 + min(subj.subjective_age / 18.0, 1.0) * 0.06)
            subj.clamp()

    def _decay_residues(self) -> None:
        for subject in self.subjects.values():
            organic_decay = self.RESIDUE_DECAY_RATE * subject.decay_speed * (1.0 - subject.texture.attraction * 0.25)

            if subject.state == SubjectState.RESIDUAL:
                subject.residue_strength -= organic_decay
                if subject.residue_strength <= self.RESIDUE_MIN_GRAVITY:
                    subject.residue_strength = 0.0
                    subject.state = SubjectState.BACKGROUND
                    subject.last_state_change = datetime.now()

            elif subject.state == SubjectState.ALMOST_CLOSED:
                subject.residue_strength -= organic_decay * 0.55
                subject.silent_pressure *= 0.92
                if subject.residue_strength < 0.08 and subject.silent_pressure < 0.08:
                    subject.state = SubjectState.CLOSED
                    subject.unresolved = False
                    subject.last_closed = datetime.now()

            elif subject.state in (SubjectState.HOVERING, SubjectState.PULLED_BACK, SubjectState.LATENT):
                subject.half_focus_level *= 0.88
                if subject.half_focus_level < 0.08:
                    subject.state = SubjectState.RESIDUAL if subject.residue_strength > 0.12 else SubjectState.BACKGROUND

            subject.silent_pressure *= 0.965
            subject.unspoken_pull *= 0.955
            subject.return_pressure *= 0.945
            subject.clamp()

    # ------------------------------------------------------------------
    # Détection de transition
    # ------------------------------------------------------------------

    def _detect_interruption(self, message_metadata: Dict[str, Any], impulse_signals: Dict[str, Any]) -> InterruptionType:
        candidates = set(message_metadata.get("candidate_subjects", []))

        if impulse_signals.get("fragmentation", 0.0) > 0.6:
            return InterruptionType.FULL_BREAK

        # Ne lit plus le texte brut avec une liste de mots fixes.
        # Le signal doit venir du moteur d'intention/compréhension ou de l'impulsion.
        if (
            message_metadata.get("is_continuation_request", False)
            or impulse_signals.get("continuation_inertia", 0.0) > 0.7
            or impulse_signals.get("continuation_request", 0.0) > 0.7
        ):
            return InterruptionType.SHORT_CONTINUE

        if message_metadata.get("is_correction", False):
            return InterruptionType.CORRECTION

        if self.previous_state:
            for cand in candidates:
                subj = self.subjects.get(cand)
                if subj and subj.state in (SubjectState.SUSPENDED, SubjectState.RESIDUAL, SubjectState.PULLED_BACK, SubjectState.REOPENING) and subj.recurrence_count > 0:
                    return InterruptionType.SUBJECT_RETURN

        if message_metadata.get("contradiction", False):
            return InterruptionType.FULL_BREAK

        return InterruptionType.NONE

    # ------------------------------------------------------------------
    # Intégration des sujets
    # ------------------------------------------------------------------

    def _integrate_candidate_subjects(
        self,
        candidates: List[str],
        hierarchy_level: Any,
        memory_hints: Dict[str, Any],
        impulse_signals: Dict[str, Any],
        attractors: Dict[str, float],
    ) -> None:
        level = self._as_level(hierarchy_level)
        now = datetime.now()
        candidate_set = {str(name).strip() for name in (candidates or []) if str(name).strip()}
        # Protection anti-bruit : le moteur attentionnel ne doit pas transformer
        # chaque micro-fragment en sujet durable. Les meilleurs candidats devraient
        # déjà être triés en amont ; ici on garde une limite organique sûre.
        candidate_set = set(sorted(candidate_set, key=lambda n: (len(n), n))[:12])
        self.current_turn_candidates = set(candidate_set)

        for name in candidate_set:
            if not name:
                continue
            if name not in self.subjects:
                if name in self.archived_subjects:
                    archived = self.archived_subjects.pop(name)
                    gravity = self._clamp01(float(archived.get("gravity", 0.35)))
                    self.subjects[name] = AttentionSubject(
                        name=name,
                        gravity=self._clamp01(gravity + 0.10),
                        state=SubjectState.REOPENING,
                        hierarchy_level=level,
                        activation_count=1,
                        recurrence_count=int(archived.get("recurrence_count", 0)) + 1,
                        wound_level=self._clamp01(float(archived.get("wound_level", 0.0))),
                        residue_strength=self._clamp01(float(archived.get("residue_strength", 0.2))),
                        unresolved=bool(archived.get("unresolved", memory_hints.get("subject_unresolved", False))),
                        silent_pressure=self._clamp01(float(archived.get("silent_pressure", 0.0))),
                        subjective_age=float(archived.get("subjective_age", 0.0)),
                        return_pressure=self._clamp01(float(archived.get("return_pressure", 0.0)) + 0.18),
                        last_activated=now,
                        last_state_change=now,
                        texture=self._initial_texture_from_signals(impulse_signals, memory_hints),
                    )
                    self.subjects[name].clamp()
                    continue

                gravity = self._estimate_initial_gravity(name, level, memory_hints, attractors)
                self.subjects[name] = AttentionSubject(
                    name=name,
                    gravity=gravity,
                    state=SubjectState.ACTIVE,
                    hierarchy_level=level,
                    activation_count=1,
                    wound_level=0.0,
                    residue_strength=gravity,
                    unresolved=bool(memory_hints.get("subject_unresolved", False)),
                    last_activated=now,
                    last_state_change=now,
                    texture=self._initial_texture_from_signals(impulse_signals, memory_hints),
                )
            else:
                subj = self.subjects[name]
                if subj.state in (
                    SubjectState.RESIDUAL,
                    SubjectState.SUSPENDED,
                    SubjectState.BACKGROUND,
                    SubjectState.CLOSED,
                    SubjectState.ALMOST_CLOSED,
                    SubjectState.PULLED_BACK,
                    SubjectState.REOPENING,
                    SubjectState.HOVERING,
                    SubjectState.LATENT,
                ):
                    subj.recurrence_count += 1
                    subj.return_pressure = self._clamp01(subj.return_pressure + 0.22 + subj.unspoken_pull * 0.18)
                    subj.state = SubjectState.REOPENING if subj.state in (SubjectState.CLOSED, SubjectState.ALMOST_CLOSED) else SubjectState.PULLED_BACK
                    subj.half_focus_level = self._clamp01(subj.half_focus_level + 0.35)
                else:
                    subj.state = SubjectState.ACTIVE

                subj.gravity = min(subj.gravity + 0.25 + subj.return_pressure * 0.08, 1.0)
                subj.activation_count += 1
                subj.residue_strength = max(subj.residue_strength, subj.gravity)
                subj.last_activated = now
                subj.last_state_change = now
                subj.subjective_age = 0.0

                if memory_hints.get("subject_unresolved", False):
                    subj.unresolved = True
                if memory_hints.get("subject_sensitive", False):
                    subj.gravity = min(subj.gravity + 0.15, 1.0)
                    subj.texture.fragility = self._clamp01(subj.texture.fragility + 0.12)

        # Les actifs du tour précédent qui ne réapparaissent pas deviennent résidus ou suspendus.
        for name, subj in list(self.subjects.items()):
            if subj.hierarchy_level == HierarchyLevel.DEEP_RULES:
                continue
            if subj.state == SubjectState.ACTIVE and name not in candidate_set:
                if subj.unresolved:
                    subj.state = SubjectState.SUSPENDED
                    subj.silent_pressure = self._clamp01(subj.silent_pressure + 0.18)
                elif subj.texture.charge() > 0.55 or subj.wound_level > 0.25:
                    subj.state = SubjectState.HOVERING
                    subj.half_focus_level = self._clamp01(subj.half_focus_level + 0.22)
                else:
                    subj.state = SubjectState.RESIDUAL
                subj.residue_strength = max(subj.residue_strength, subj.gravity * 0.6)
                subj.last_state_change = now
            subj.clamp()

    def _estimate_initial_gravity(self, name: str, level: HierarchyLevel, memory_hints: Dict[str, Any], attractors: Dict[str, float]) -> float:
        base = 0.3 + level.value * 0.1
        if memory_hints.get("subject_important", False):
            base += 0.2
        if memory_hints.get("subject_sensitive", False):
            base += 0.15
        if memory_hints.get("subject_returning", False):
            base += 0.1
        for attr_name, attr_strength in attractors.items():
            if attr_name in name or name in attr_name:
                base += float(attr_strength) * 0.1
        return self._clamp01(base)

    def _initial_texture_from_signals(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any]) -> AttentionTexture:
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        resistance = float(impulse_signals.get("resistance", impulse_signals.get("resistance_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", 0.0))
        sensitive = 1.0 if memory_hints.get("subject_sensitive", False) else 0.0
        texture = AttentionTexture(
            tension=self._clamp01(contradiction * 0.45 + saturation * 0.25 + sensitive * 0.10),
            openness=self._clamp01(0.50 + curiosity * 0.18 - resistance * 0.14),
            attraction=self._clamp01(0.50 + curiosity * 0.18 + sensitive * 0.10),
            resistance=self._clamp01(resistance * 0.55 + contradiction * 0.16),
            fragility=self._clamp01(saturation * 0.22 + sensitive * 0.16),
            safety=self._clamp01(0.62 - contradiction * 0.18 - resistance * 0.12),
        )
        texture.clamp()
        return texture

    # ------------------------------------------------------------------
    # Plaies attentionnelles
    # ------------------------------------------------------------------

    def _apply_error_signals(self, error_signals: List[str]) -> None:
        for signal in error_signals or []:
            if signal in self.subjects:
                subj = self.subjects[signal]
                subj.wound_level = min(subj.wound_level + self.WOUND_ACCUMULATION, 1.0)
                subj.gravity = min(subj.gravity + 0.1, 1.0)
                subj.texture.fragility = self._clamp01(subj.texture.fragility + 0.18)
                subj.texture.tension = self._clamp01(subj.texture.tension + 0.14)
                subj.texture.safety = self._clamp01(subj.texture.safety - 0.10)
                subj.silent_pressure = self._clamp01(subj.silent_pressure + 0.16)
                subj.unspoken_pull = self._clamp01(subj.unspoken_pull + 0.10)
                subj.clamp()

    def _heal_wounds(self, error_signals: List[str]) -> None:
        error_set = set(error_signals or [])
        for name, subj in self.subjects.items():
            if name not in error_set and subj.wound_level > 0.0:
                healing = self.WOUND_HEALING * (0.6 + subj.texture.safety * 0.6)
                subj.wound_level = max(subj.wound_level - healing, 0.0)
                subj.texture.fragility = max(subj.texture.fragility - healing * 0.5, 0.0)
                subj.texture.safety = self._clamp01(subj.texture.safety + healing * 0.25)
                subj.clamp()

    def _get_wound_alerts(self) -> List[str]:
        return [name for name, s in self.subjects.items() if s.wound_level > 0.3]

    def _close_subjects(self, closed_names: List[str]) -> None:
        for name in closed_names or []:
            if name in self.subjects:
                subj = self.subjects[name]
                subj.state = SubjectState.ALMOST_CLOSED if subj.texture.charge() > 0.35 or subj.silent_pressure > 0.20 else SubjectState.CLOSED
                subj.unresolved = False
                subj.last_closed = datetime.now()
                subj.residue_strength = max(subj.residue_strength, subj.gravity * 0.2)
                subj.return_latency = self._clamp01(subj.return_latency + 0.20)
                subj.clamp()

    # ------------------------------------------------------------------
    # Textures, contamination, silence, fatigue
    # ------------------------------------------------------------------

    def _update_subject_textures(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any], message_metadata: Dict[str, Any]) -> None:
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        resistance = float(impulse_signals.get("resistance", impulse_signals.get("resistance_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        presence = float(presence_signal.get("presence_strength", 0.5))
        correction = 1.0 if message_metadata.get("is_correction", False) else 0.0

        target = AttentionTexture(
            tension=self._clamp01(contradiction * 0.36 + pressure * 0.16 + correction * 0.14),
            openness=self._clamp01(0.48 + curiosity * 0.22 + presence * 0.08 - resistance * 0.16),
            attraction=self._clamp01(0.46 + curiosity * 0.18 + pressure * 0.08),
            resistance=self._clamp01(resistance * 0.38 + contradiction * 0.18),
            fragility=self._clamp01(fragmentation * 0.22 + correction * 0.10),
            safety=self._clamp01(0.60 + presence * 0.12 - contradiction * 0.14 - fragmentation * 0.10),
        )

        for subj in self.subjects.values():
            if subj.state in (SubjectState.ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK):
                alpha = 0.22
            elif subj.state in (SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING):
                alpha = 0.12
            else:
                alpha = 0.05
            subj.texture.blend_from(target, alpha)
            subj.decay_speed = self._clamp01(1.0 - subj.texture.attraction * 0.22 + subj.texture.resistance * 0.18 + self.attention_fatigue * 0.10)
            subj.decay_speed = max(0.35, min(1.75, subj.decay_speed))
            subj.clamp()

    def _apply_subject_contamination(self, attractors: Dict[str, float], impulse_signals: Dict[str, Any]) -> None:
        contamination_total = 0.0
        names = list(self.subjects.keys())
        active_names = [n for n, s in self.subjects.items() if s.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK)]

        # Règles profondes contaminent les sujets reliés sans devenir focus public.
        for rule, related_tokens in self.rule_links.items():
            rule_subj = self.subjects.get(rule)
            if not rule_subj:
                continue
            rule_charge = max(rule_subj.gravity * 0.08, rule_subj.wound_level * 0.22, rule_subj.silent_pressure * 0.18)
            for name in names:
                if name == rule:
                    continue
                lower_name = name.lower()
                related = any(token in lower_name for token in related_tokens)
                if related or name in active_names:
                    amount = self._clamp01(rule_charge * (0.55 if related else 0.18))
                    if amount <= 0.005:
                        continue
                    subj = self.subjects[name]
                    subj.contamination[rule] = self._clamp01(subj.contamination.get(rule, 0.0) * 0.86 + amount)
                    subj.gravity = self._clamp01(subj.gravity + amount * 0.05)
                    subj.texture.fragility = self._clamp01(subj.texture.fragility + rule_subj.wound_level * amount * 0.05)
                    contamination_total += amount

        # Les sujets chargés contaminent les voisins actifs/faibles.
        for src_name in active_names:
            src = self.subjects[src_name]
            charge = src.texture.charge() + src.silent_pressure * 0.30
            if charge < 0.20:
                continue
            for dst_name in active_names:
                if dst_name == src_name:
                    continue
                dst = self.subjects[dst_name]
                amount = min(0.10, charge * 0.035)
                dst.texture.tension = self._clamp01(dst.texture.tension + src.texture.tension * amount)
                dst.texture.attraction = self._clamp01(dst.texture.attraction + (src.texture.attraction - 0.5) * amount)
                dst.contamination[src_name] = self._clamp01(dst.contamination.get(src_name, 0.0) * 0.84 + amount)
                contamination_total += amount

        # Décroissance générale de contamination.
        for subj in self.subjects.values():
            for key in list(subj.contamination.keys()):
                subj.contamination[key] *= 0.88
                if subj.contamination[key] < 0.02:
                    del subj.contamination[key]
            subj.clamp()

        self.field.contamination_tension = self._clamp01(contamination_total / max(len(active_names), 1))

    def _update_silent_pressures(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any]) -> None:
        silence = float(impulse_signals.get("silent_pressure", impulse_signals.get("silence", 0.0)))
        clarification = float(impulse_signals.get("clarification_need", 0.0))
        continuation = float(impulse_signals.get("continuation_inertia", 0.0))

        for subj in self.subjects.values():
            if subj.unresolved:
                subj.silent_pressure = self._clamp01(subj.silent_pressure + 0.035 + clarification * 0.035)
                subj.unspoken_pull = self._clamp01(subj.unspoken_pull + continuation * 0.025)
            elif subj.state in (SubjectState.SUSPENDED, SubjectState.RESIDUAL, SubjectState.HOVERING):
                subj.silent_pressure = self._clamp01(subj.silent_pressure + silence * 0.045 + subj.texture.charge() * 0.018)

            if subj.wound_level > 0.25:
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.wound_level * 0.018)

            subj.clamp()

    def _update_attention_fatigue(self, impulse_signals: Dict[str, Any], message_metadata: Dict[str, Any]) -> None:
        active_count = sum(1 for s in self.subjects.values() if s.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK))
        unresolved_count = sum(1 for s in self.subjects.values() if s.unresolved)
        wound_count = sum(1 for s in self.subjects.values() if s.wound_level > 0.25)
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        correction = 1.0 if message_metadata.get("is_correction", False) else 0.0
        multi = 1.0 if message_metadata.get("multi_demand", False) else 0.0

        load = self._clamp01(
            max(0.0, active_count - 3) * 0.08
            + unresolved_count * 0.06
            + wound_count * 0.05
            + fragmentation * 0.25
            + correction * 0.08
            + multi * 0.10
            + self.stagnation_counter * 0.035
        )
        self.attention_fatigue = self._clamp01(self.attention_fatigue * 0.90 + load * 0.10)

        if fragmentation > 0.45:
            self.last_fatigue_reason = "fragmentation"
        elif unresolved_count > 2:
            self.last_fatigue_reason = "open_loops"
        elif wound_count > 1:
            self.last_fatigue_reason = "wounds"
        elif active_count > 4:
            self.last_fatigue_reason = "too_many_subjects"
        else:
            self.last_fatigue_reason = "stable"


    def _update_attention_breath(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any]) -> None:
        """
        Respiration attentionnelle globale.
        Elle ne produit pas de contenu : elle module seulement expansion/contraction.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))

        self.breath_phase += 0.17 + curiosity * 0.05 - saturation * 0.035
        wave = (math.sin(self.breath_phase) + 1.0) / 2.0
        target = self._clamp01(0.42 + wave * 0.22 + curiosity * 0.12 + presence * 0.08 - saturation * 0.16 - fragmentation * 0.10)
        self.organic_breath = self._clamp01(self.organic_breath * 0.86 + target * 0.14)

        contraction = self._clamp01(1.0 - self.organic_breath)
        for subj in self.subjects.values():
            if subj.state in (SubjectState.ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK):
                subj.half_focus_level = self._clamp01(subj.half_focus_level + self.organic_breath * 0.025)
            elif contraction > 0.55 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND):
                subj.residue_strength = self._clamp01(subj.residue_strength - contraction * 0.018)
            subj.clamp()

    def _update_emotional_gravity_bias(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any]) -> None:
        """Crée une gravité autonome née des retours, blessures, non-résolus et charges."""
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))

        for subj in self.subjects.values():
            charge = subj.texture.charge()
            growth = (
                subj.recurrence_count * 0.006
                + subj.wound_level * 0.018
                + (0.018 if subj.unresolved else 0.0)
                + charge * 0.012
                + memory_weight * 0.010
            )
            if subj.state in (SubjectState.ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK):
                growth += (curiosity + pressure) * 0.006
            decay = 0.018 + subj.directional_fatigue * 0.012
            subj.emotional_gravity_bias = self._clamp01(subj.emotional_gravity_bias * (1.0 - decay) + growth)
            subj.clamp()

    def _update_directional_fatigue_and_proximity(self, impulse_signals: Dict[str, Any]) -> None:
        """Ajoute saturation d'axe + proximité subjective indépendante de la récence pure."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))

        for subj in self.subjects.values():
            if subj.state == SubjectState.ACTIVE:
                subj.directional_fatigue = self._clamp01(subj.directional_fatigue + 0.012 + saturation * 0.025 + pressure * 0.010)
            else:
                subj.directional_fatigue = self._clamp01(subj.directional_fatigue * 0.965 - self.organic_breath * 0.004)

            emotional_nearness = subj.emotional_gravity_bias * 0.34 + subj.return_pressure * 0.22 + subj.silent_pressure * 0.18 + subj.texture.charge() * 0.18
            chronological_distance = min(subj.subjective_age / 30.0, 1.0) * 0.16
            subj.subjective_proximity = self._clamp01(emotional_nearness + subj.attention_habit * 0.12 - chronological_distance)
            subj.clamp()

    def _apply_resonance_coalitions(self, impulse_signals: Dict[str, Any]) -> None:
        """
        Deux ou plusieurs sujets faibles peuvent former une coalition attentionnelle.
        Ce n'est pas une duplication de l'impulsion : seulement une interaction entre traces.
        """
        active_like = [
            (name, s) for name, s in self.subjects.items()
            if s.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.PULLED_BACK, SubjectState.REOPENING, SubjectState.SUSPENDED)
            and s.state != SubjectState.CLOSED
        ]
        if len(active_like) < 2:
            for _, s in active_like:
                s.resonance_level *= 0.92
                s.clamp()
            return

        for name, subj in active_like:
            resonance = 0.0
            tokens = set(name.lower().replace("_", " ").split())
            for other_name, other in active_like:
                if other_name == name:
                    continue
                other_tokens = set(other_name.lower().replace("_", " ").split())
                lexical_overlap = len(tokens & other_tokens) / max(len(tokens | other_tokens), 1)
                emotional_overlap = 1.0 - abs(subj.texture.charge() - other.texture.charge())
                contamination_link = max(subj.contamination.get(other_name, 0.0), other.contamination.get(name, 0.0))
                resonance += lexical_overlap * 0.08 + emotional_overlap * 0.018 + contamination_link * 0.12
            subj.resonance_level = self._clamp01(subj.resonance_level * 0.82 + min(resonance, 0.35))
            if subj.resonance_level > 0.14:
                subj.gravity = self._clamp01(subj.gravity + subj.resonance_level * 0.035)
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.resonance_level * 0.025)
            subj.clamp()

    def _apply_organic_instability(self, impulse_signals: Dict[str, Any]) -> None:
        """Oscillation douce : hésitation réelle sans hasard brutal ni choix préécrit."""
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        for index, (name, subj) in enumerate(self.subjects.items()):
            wave = (math.sin(self.internal_clock * 0.41 + index * 0.73 + subj.subjective_age * 0.11) + 1.0) / 2.0
            target = self._clamp01(contradiction * 0.22 + fragmentation * 0.18 + subj.directional_fatigue * 0.18 + subj.texture.resistance * 0.12 + wave * 0.08)
            subj.instability = self._clamp01(subj.instability * 0.88 + target * 0.12)
            if subj.instability > 0.42 and subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE):
                subj.gravity = self._clamp01(subj.gravity - subj.instability * 0.018 + subj.resonance_level * 0.012)
                subj.silent_pressure = self._clamp01(subj.silent_pressure + subj.instability * 0.010)
            subj.clamp()

    def _update_attention_habits(self, primary: str, secondary: List[str]) -> None:
        """Mémoire de chemins attentionnels, pour que l'attention ait une personnalité."""
        if self.last_primary and primary and self.last_primary != primary:
            key = (self.last_primary, primary)
            self.attention_habits[key] = self._clamp01(self.attention_habits.get(key, 0.0) * 0.92 + 0.12)
            self.last_transition = key
        for key in list(self.attention_habits.keys()):
            if key != self.last_transition:
                self.attention_habits[key] *= 0.985
            if self.attention_habits[key] < 0.025:
                del self.attention_habits[key]

        for name, subj in self.subjects.items():
            incoming = max([v for (src, dst), v in self.attention_habits.items() if dst == name] or [0.0])
            outgoing = max([v for (src, dst), v in self.attention_habits.items() if src == name] or [0.0])
            relation_bonus = 0.0
            if secondary and name in secondary:
                relation_bonus += 0.025
            subj.attention_habit = self._clamp01(subj.attention_habit * 0.94 + incoming * 0.05 + outgoing * 0.025 + relation_bonus)
            subj.clamp()


    def _update_existential_charge(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], presence_signal: Dict[str, Any]) -> None:
        """Poids profond du sujet : identité, projet, règles, mémoire, sans contenu préécrit."""
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        identity_signal = float(impulse_signals.get("identity_pressure", impulse_signals.get("self_relevance", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))
        for name, subj in self.subjects.items():
            deep = 1.0 if subj.hierarchy_level == HierarchyLevel.DEEP_RULES else 0.0
            project_depth = subj.hierarchy_level.value / max(HierarchyLevel.DEEP_RULES.value, 1)
            current_touch = 1.0 if name in self.current_turn_candidates else 0.0
            wound_memory = subj.wound_level * 0.20 + (0.14 if subj.unresolved else 0.0)
            charge_target = self._clamp01(
                deep * 0.62
                + project_depth * 0.22
                + memory_weight * 0.16
                + identity_signal * 0.20
                + subj.texture.charge() * 0.16
                + current_touch * 0.10
                + wound_memory
            )
            subj.existential_charge = self._clamp01(subj.existential_charge * 0.91 + charge_target * 0.09)
            subj.identity_weight = self._clamp01(subj.identity_weight * 0.94 + (deep * 0.42 + identity_signal * 0.18 + project_depth * 0.10) * 0.06)
            subj.self_binding = self._clamp01(subj.self_binding * 0.95 + (subj.identity_weight * 0.12 + presence * 0.025 + current_touch * 0.035))
            subj.clamp()

    def _update_implicit_missing_pressure(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], message_metadata: Dict[str, Any]) -> None:
        """Pression du non-dit : ce qui manque, ce qui est évité ou laissé ouvert."""
        explicit_missing = float(impulse_signals.get("implicit_missing", impulse_signals.get("missing_pressure", 0.0)))
        clarification = float(impulse_signals.get("clarification_need", 0.0))
        continuation = float(impulse_signals.get("continuation_inertia", 0.0))
        candidate_count = len(self.current_turn_candidates)
        no_candidate_gap = 1.0 if candidate_count == 0 and self.previous_state is not None else 0.0
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        self.unspoken_global_pressure = self._clamp01(
            self.unspoken_global_pressure * 0.88
            + explicit_missing * 0.10
            + clarification * 0.045
            + no_candidate_gap * 0.055
            + unresolved_hint * 0.035
        )
        for name, subj in self.subjects.items():
            missing = explicit_missing * 0.08 + self.unspoken_global_pressure * 0.06
            if subj.unresolved:
                missing += 0.035 + clarification * 0.035
            if subj.state in (SubjectState.SUSPENDED, SubjectState.HOVERING, SubjectState.RESIDUAL, SubjectState.ALMOST_CLOSED):
                missing += continuation * 0.020 + subj.texture.charge() * 0.012
            if name not in self.current_turn_candidates and subj.state == SubjectState.ACTIVE:
                missing += 0.025
            subj.implicit_missing_pressure = self._clamp01(subj.implicit_missing_pressure * 0.93 + missing)
            subj.silent_pressure = self._clamp01(subj.silent_pressure + subj.implicit_missing_pressure * 0.012)
            subj.clamp()

    def _update_cognitive_pain_and_avoidance(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any]) -> None:
        """Surcharge locale : certains sujets deviennent douloureux puis partiellement évités."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        presence = float(presence_signal.get("presence_strength", 0.5))
        for subj in self.subjects.values():
            exposed = 1.0 if subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.REOPENING, SubjectState.PULLED_BACK) else 0.35
            pain_gain = (
                saturation * 0.026
                + contradiction * 0.020
                + fragmentation * 0.016
                + subj.wound_level * 0.022
                + subj.texture.fragility * 0.016
                + subj.implicit_missing_pressure * 0.012
            ) * exposed
            relief = 0.020 + presence * 0.012 + subj.texture.safety * 0.012
            subj.cognitive_pain = self._clamp01(subj.cognitive_pain * 0.965 + pain_gain - relief * 0.35)
            avoid_target = self._clamp01(subj.cognitive_pain * 0.54 + subj.texture.resistance * 0.22 + subj.wound_level * 0.16 - subj.self_binding * 0.08)
            subj.avoidance_pressure = self._clamp01(subj.avoidance_pressure * 0.90 + avoid_target * 0.10)
            if subj.avoidance_pressure > 0.58 and subj.state == SubjectState.ACTIVE and subj.existential_charge < 0.55:
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + 0.22)
            subj.clamp()

    def _update_obsession_and_void(self, impulse_signals: Dict[str, Any], message_metadata: Dict[str, Any]) -> None:
        """Fixations autonomes + perception du vide quand aucun attracteur clair ne gagne."""
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        active_strengths = [s.gravity + s.return_pressure + s.silent_pressure for s in self.subjects.values() if s.state not in (SubjectState.CLOSED, SubjectState.BACKGROUND)]
        dominant_strength = max(active_strengths or [0.0])
        spread = 0.0
        if len(active_strengths) >= 2:
            ordered = sorted(active_strengths, reverse=True)
            spread = self._clamp01(1.0 - abs(ordered[0] - ordered[1]))
        empty_message = 1.0 if not self.current_turn_candidates and not str(message_metadata.get("raw_text_lower", "")).strip() else 0.0
        target_void = self._clamp01((1.0 - dominant_strength) * 0.32 + spread * 0.22 + saturation * 0.16 + fragmentation * 0.12 + empty_message * 0.18)
        self.attention_void = self._clamp01(self.attention_void * 0.86 + target_void * 0.14)
        for subj in self.subjects.values():
            obsession_gain = (
                subj.unspoken_pull * 0.026
                + subj.return_pressure * 0.022
                + subj.existential_charge * 0.014
                + subj.implicit_missing_pressure * 0.020
                + subj.recurrence_count * 0.004
                + (0.020 if subj.unresolved else 0.0)
            )
            obsession_decay = 0.024 + subj.cognitive_pain * 0.010 + subj.avoidance_pressure * 0.010
            subj.obsession_fixation = self._clamp01(subj.obsession_fixation * (1.0 - obsession_decay) + obsession_gain)
            subj.void_pull = self._clamp01(subj.void_pull * 0.90 + self.attention_void * 0.055 + (1.0 - curiosity) * 0.012)
            if subj.obsession_fixation > 0.32 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.ALMOST_CLOSED):
                subj.state = SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.obsession_fixation * 0.10)
            subj.clamp()

    def _apply_attention_turbulence(self, impulse_signals: Dict[str, Any]) -> None:
        """Bifurcations organiques déterministes : pas de hasard, pas de phrases, pas de templates."""
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        field_turbulence = self._clamp01(contradiction * 0.24 + fragmentation * 0.22 + pressure * 0.10 + self.attention_void * 0.12 + self.attention_fatigue * 0.12)
        self.turbulence_memory = self._clamp01(self.turbulence_memory * 0.84 + field_turbulence * 0.16)
        for idx, (name, subj) in enumerate(self.subjects.items()):
            wave = (math.sin(self.internal_clock * 0.67 + idx * 1.31 + subj.subjective_age * 0.19) + 1.0) / 2.0
            local = self._clamp01(self.turbulence_memory * 0.34 + subj.instability * 0.25 + subj.cognitive_pain * 0.14 + subj.implicit_missing_pressure * 0.12 + wave * 0.08)
            subj.turbulence = self._clamp01(subj.turbulence * 0.82 + local * 0.18)
            if subj.turbulence > 0.48:
                if subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.HOVERING):
                    subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.turbulence * 0.05)
                subj.gravity = self._clamp01(subj.gravity + (wave - 0.5) * subj.turbulence * 0.030)
            subj.clamp()


    def _update_attentional_scars(self, impulse_signals: Dict[str, Any], message_metadata: Dict[str, Any], interruption: InterruptionType) -> None:
        """Mémoire globale de sensibilité : ce qui a blessé ou usé l’attention reste comme biais discret."""
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        unresolved_count = sum(1 for s in self.subjects.values() if s.unresolved and s.state != SubjectState.CLOSED)
        repetition = 1.0 if self.stagnation_counter >= max(1, self.LOOP_STAGNATION_LIMIT - 1) else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK or message_metadata.get("contradiction", False) else 0.0

        targets = {
            "contradiction": contradiction,
            "overload": max(saturation, fragmentation * 0.85),
            "rupture": rupture,
            "repetition": repetition,
            "unresolved": self._clamp01(unresolved_count * 0.16),
        }
        for key, target in targets.items():
            old = self.attentional_scars.get(key, 0.0)
            # Les cicatrices montent plus vite qu’elles ne redescendent.
            gain = 0.055 if target > old else 0.018
            self.attentional_scars[key] = self._clamp01(old * (1.0 - gain) + target * gain)

    def _update_latent_focus_and_precision(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any]) -> None:
        """Ajoute du flou et des focus latents quand le champ est chargé mais pas assez clair."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))
        global_blur = self._clamp01(
            saturation * 0.30
            + fragmentation * 0.25
            + contradiction * 0.18
            + self.attention_void * 0.16
            + scar_load * 0.24
            + self.attention_fatigue * 0.18
        )
        self.global_precision = self._clamp01(self.global_precision * 0.88 + (1.0 - global_blur) * 0.12)

        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            unresolved_gain = 0.045 if subj.unresolved or unresolved_hint else 0.0
            latent_gain = (
                subj.silent_pressure * 0.055
                + subj.implicit_missing_pressure * 0.060
                + subj.obsession_fixation * 0.045
                + subj.void_pull * 0.035
                + subj.return_pressure * 0.030
                + unresolved_gain
            )
            decay = 0.045 + (0.025 if subj.state == SubjectState.ACTIVE else 0.0)
            subj.latent_focus_pressure = self._clamp01(subj.latent_focus_pressure * (1.0 - decay) + latent_gain)

            local_blur = self._clamp01(
                global_blur * 0.36
                + subj.cognitive_pain * 0.22
                + subj.turbulence * 0.18
                + subj.directional_fatigue * 0.14
                + subj.saturation_memory * 0.18
                + subj.avoidance_pressure * 0.10
            )
            subj.precision_loss = self._clamp01(subj.precision_loss * 0.86 + local_blur * 0.14)
            subj.saturation_memory = self._clamp01(subj.saturation_memory * 0.965 + saturation * 0.025 + subj.precision_loss * 0.012)
            subj.pull_release_need = self._clamp01(
                subj.pull_release_need * 0.90
                + subj.obsession_fixation * 0.045
                + subj.directional_fatigue * 0.035
                + subj.saturation_memory * 0.030
                + (0.055 if subj.name == self.last_primary and self.stagnation_counter > 1 else 0.0)
            )
            if subj.latent_focus_pressure > 0.42 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.ALMOST_CLOSED):
                subj.state = SubjectState.LATENT
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.latent_focus_pressure * 0.18)
            if subj.precision_loss > 0.62 and subj.state == SubjectState.ACTIVE and subj.existential_charge < 0.62:
                subj.state = SubjectState.HALF_ACTIVE
            subj.clamp()


    def _update_subconscious_field(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """
        Couche périphérique : les sujets faibles continuent d'exister et peuvent
        revenir par écho, sans devenir immédiatement focus conscient.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0

        peripheral_values: List[float] = []
        active_names = [n for n, s in self.subjects.items() if s.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.PULLED_BACK, SubjectState.REOPENING)]
        active_tokens = set()
        for n in active_names:
            active_tokens.update(n.lower().replace("_", " ").split())

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            tokens = set(name.lower().replace("_", " ").split())
            overlap = len(tokens & active_tokens) / max(len(tokens | active_tokens), 1) if active_tokens else 0.0
            associative_target = self._clamp01(
                overlap * 0.22
                + max(subj.contamination.values() or [0.0]) * 0.25
                + subj.resonance_level * 0.18
                + subj.attention_habit * 0.12
            )
            subj.associative_echo = self._clamp01(subj.associative_echo * 0.88 + associative_target * 0.12)

            subconscious_gain = (
                subj.residue_strength * 0.030
                + subj.silent_pressure * 0.050
                + subj.unspoken_pull * 0.045
                + subj.latent_focus_pressure * 0.040
                + subj.associative_echo * 0.050
                + subj.implicit_missing_pressure * 0.040
                + subj.existential_charge * 0.020
                + unresolved_hint * 0.018
                + scar_load * 0.020
            )
            if subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY):
                subconscious_gain *= 0.45
            if rupture > 0.0:
                subconscious_gain += subj.residue_strength * 0.018
            decay = 0.040 + saturation * 0.018 + (0.020 if subj.state == SubjectState.ACTIVE else 0.0)
            subj.subconscious_pressure = self._clamp01(subj.subconscious_pressure * (1.0 - decay) + subconscious_gain)

            subj.affective_narrowing = self._clamp01(
                subj.affective_narrowing * 0.88
                + (subj.cognitive_pain * 0.24 + subj.texture.tension * 0.18 + subj.avoidance_pressure * 0.16 + saturation * 0.12) * 0.12
                - curiosity * 0.015
            )
            if subj.subconscious_pressure > 0.38 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.ALMOST_CLOSED):
                subj.state = SubjectState.LATENT
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.subconscious_pressure * 0.12)
            peripheral_values.append(subj.subconscious_pressure)
            subj.clamp()

        self.global_subconscious_pressure = self._clamp01(sum(peripheral_values) / max(1, len(peripheral_values)) + pressure * 0.025)
        self.attention_bandwidth = self._clamp01(1.0 - self.attention_fatigue * 0.28 - self.global_subconscious_pressure * 0.18 - saturation * 0.20)


    def _update_preconscious_and_weather(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Champ avant-sujet + météo cognitive globale.
        Cette couche permet une tension diffuse, sans l'attacher immédiatement
        à un sujet explicite ni produire de contenu verbal.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        no_clear_focus = 1.0 if not self.current_turn_candidates else 0.0
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))

        pre_values: List[float] = []
        distortion_values: List[float] = []
        temporality_values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            scar_target = self._clamp01(
                subj.scar_sensitivity * 0.25
                + subj.wound_level * 0.22
                + subj.saturation_memory * 0.14
                + scar_load * 0.18
                + rupture * 0.07
                + correction * 0.05
            )
            subj.scar_distortion = self._clamp01(subj.scar_distortion * 0.94 + scar_target * 0.06)

            pre_target = self._clamp01(
                no_clear_focus * 0.13
                + self.attention_void * 0.15
                + subj.latent_focus_pressure * 0.16
                + subj.subconscious_pressure * 0.15
                + subj.implicit_missing_pressure * 0.12
                + unresolved_hint * 0.06
                + subj.scar_distortion * 0.08
                + contradiction * 0.05
                + curiosity * 0.04
                - subj.protective_guard * 0.035
            )
            subj.preconscious_charge = self._clamp01(subj.preconscious_charge * 0.91 + pre_target * 0.09)

            subj.unresolved_need = self._clamp01(
                subj.unresolved_need * 0.92
                + (0.16 if subj.unresolved else 0.0)
                + subj.implicit_missing_pressure * 0.06
                + subj.silent_pressure * 0.04
                + subj.existential_charge * 0.03
            )
            if subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.HOVERING) and subj.preconscious_charge > 0.30:
                subj.regret_trace = self._clamp01(subj.regret_trace + subj.preconscious_charge * 0.035 + subj.unresolved_need * 0.020)
            else:
                subj.regret_trace = self._clamp01(subj.regret_trace * 0.975)

            subj.asymmetrical_delay = self._clamp01(
                subj.asymmetrical_delay * 0.90
                + subj.temporal_drag * 0.06
                + subj.scar_distortion * 0.05
                + subj.affective_narrowing * 0.04
                + subj.regret_trace * 0.03
                - pressure * 0.015
            )

            if subj.preconscious_charge > 0.48 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL):
                subj.state = SubjectState.LATENT
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.preconscious_charge * 0.10)

            subj.clamp()
            pre_values.append(subj.preconscious_charge)
            distortion_values.append(subj.scar_distortion)
            temporality_values.extend([subj.lived_expectation, subj.unresolved_need, subj.regret_trace, subj.asymmetrical_delay])

        self.global_preconscious_charge = self._clamp01(max(pre_values or [0.0]) * 0.55 + sum(pre_values) / max(1, len(pre_values)) * 0.45)
        self.global_scar_distortion = self._clamp01(sum(distortion_values) / max(1, len(distortion_values)))
        self.global_lived_temporality = self._clamp01(sum(temporality_values) / max(1, len(temporality_values)))

        weather = self.cognitive_weather
        target_heavy = self._clamp01(saturation * 0.26 + self.attention_fatigue * 0.24 + self.global_scar_distortion * 0.18 + self.attention_void * 0.12)
        target_nervous = self._clamp01(contradiction * 0.24 + rupture * 0.18 + self.global_micro_instability * 0.16 + pressure * 0.08)
        target_open = self._clamp01(presence * 0.34 + curiosity * 0.22 + weather.get("openness", 0.5) * 0.20 - target_heavy * 0.12 - saturation * 0.10)
        target_expectancy = self._clamp01(self.anticipatory_pressure * 0.22 + self.global_preconscious_charge * 0.24 + curiosity * 0.12 + unresolved_hint * 0.08)
        target_fragility = self._clamp01(self.global_scar_distortion * 0.24 + saturation * 0.12 + contradiction * 0.10 + self.global_fragmented_presence * 0.10)
        target_clarity = self._clamp01(1.0 - saturation * 0.26 - self.global_preconscious_charge * 0.16 - self.global_subconscious_pressure * 0.12 - target_nervous * 0.10)

        weather["heaviness"] = self._clamp01(weather.get("heaviness", 0.0) * 0.88 + target_heavy * 0.12)
        weather["nervousness"] = self._clamp01(weather.get("nervousness", 0.0) * 0.86 + target_nervous * 0.14)
        weather["openness"] = self._clamp01(weather.get("openness", 0.5) * 0.90 + target_open * 0.10)
        weather["expectancy"] = self._clamp01(weather.get("expectancy", 0.0) * 0.87 + target_expectancy * 0.13)
        weather["fragility"] = self._clamp01(weather.get("fragility", 0.0) * 0.89 + target_fragility * 0.11)
        weather["clarity"] = self._clamp01(weather.get("clarity", 1.0) * 0.88 + target_clarity * 0.12)

    def _update_affective_focus_memory(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """Mémoire affective locale : rend certains focus durablement sensibles sans jouer le rôle mémoire."""
        importance = float(memory_hints.get("importance", memory_hints.get("memory_weight", 0.0)))
        sensitivity = 1.0 if memory_hints.get("subject_sensitive", False) else 0.0
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            active = 1.0 if name in self.current_turn_candidates or subj.state == SubjectState.ACTIVE else 0.0
            deep = 1.0 if subj.hierarchy_level == HierarchyLevel.DEEP_RULES else 0.0
            target = self._clamp01(
                subj.affective_memory_bias * 0.58
                + active * (0.045 + importance * 0.030 + sensitivity * 0.040)
                + subj.wound_level * 0.035
                + subj.scar_sensitivity * 0.035
                + subj.existential_charge * 0.028
                + subj.unresolved_need * 0.026
                + curiosity * subj.texture.attraction * 0.020
                + contradiction * 0.018
                + correction * 0.018
                + rupture * 0.012
                + deep * 0.012
            )
            subj.affective_memory_bias = self._clamp01(subj.affective_memory_bias * 0.965 + target * 0.035)
            subj.texture.attraction = self._clamp01(subj.texture.attraction + subj.affective_memory_bias * 0.004 - subj.organic_fatigue * 0.003)
            subj.clamp()
            values.append(subj.affective_memory_bias)
        self.global_affective_focus_memory = self._clamp01(max(values or [0.0]) * 0.56 + sum(values) / max(1, len(values)) * 0.44)

    def _update_residual_haunting(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """Les résidus chargés continuent de hanter le champ sans redevenir automatiquement le sujet principal."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            residual_state = 1.0 if subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.HOVERING, SubjectState.LATENT, SubjectState.PULLED_BACK) else 0.0
            target = self._clamp01(
                residual_state * (subj.residue_strength * 0.18 + subj.silent_pressure * 0.12 + subj.regret_trace * 0.10)
                + subj.unresolved_need * 0.10
                + subj.affective_memory_bias * 0.08
                + subj.scar_distortion * 0.06
                + unresolved_hint * 0.025
                + rupture * subj.residue_strength * 0.035
                - saturation * 0.025
                - subj.protective_guard * 0.020
            )
            subj.haunting_level = self._clamp01(subj.haunting_level * 0.92 + target * 0.08)
            if subj.haunting_level > 0.42 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.haunting_level * 0.075)
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.haunting_level * 0.035)
            subj.clamp()
            values.append(subj.haunting_level)
        self.global_residual_haunting = self._clamp01(max(values or [0.0]) * 0.60 + sum(values) / max(1, len(values)) * 0.40)

    def _update_organic_drift_field(self, impulse_signals: Dict[str, Any], attractors: Dict[str, float], presence_signal: Dict[str, Any], interruption: InterruptionType) -> None:
        """Dérive lente non verbale : le champ bouge même quand l'input ne force pas clairement un focus."""
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        attractor_strength = max([float(v) for v in attractors.values()] or [0.0])
        no_clear_input = 1.0 if not self.current_turn_candidates else 0.0
        rupture_block = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            phase = (math.sin(self.internal_clock * 0.113 + len(name) * 0.37 + subj.subjective_age * 0.071) + 1.0) * 0.5
            target = self._clamp01(
                phase * 0.040
                + no_clear_input * 0.050
                + self.attention_void * 0.050
                + subj.haunting_level * 0.075
                + subj.affective_memory_bias * 0.055
                + subj.autonomous_desire * 0.050
                + subj.residue_strength * 0.030
                + (1.0 - attractor_strength) * 0.025
                + presence * 0.015
                - pressure * 0.035
                - saturation * 0.030
                - rupture_block * 0.045
                - subj.protective_guard * 0.025
            )
            subj.drift_vector = self._clamp01(subj.drift_vector * 0.93 + target * 0.07)
            if subj.drift_vector > 0.38 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.VOID_DRIFT):
                subj.state = SubjectState.LATENT
                subj.latent_focus_pressure = self._clamp01(subj.latent_focus_pressure + subj.drift_vector * 0.06)
            subj.clamp()
            values.append(subj.drift_vector)
        self.global_drift_field = self._clamp01(max(values or [0.0]) * 0.57 + sum(values) / max(1, len(values)) * 0.43)

    def _update_attention_recovery_phase(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any], interruption: InterruptionType) -> None:
        """Après surcharge, l'attention se répare lentement au lieu de se réinitialiser brutalement."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        overload = self._clamp01(saturation * 0.35 + self.attention_fatigue * 0.28 + self.global_scar_distortion * 0.18 + rupture * 0.12 + self.global_micro_instability * 0.10)
        ease = self._clamp01(presence * 0.18 + max(0.0, 0.65 - pressure) * 0.12 + self.cognitive_weather.get("openness", 0.5) * 0.10)
        self.global_recovery_need = self._clamp01(self.global_recovery_need * 0.90 + overload * 0.12 - ease * 0.045)
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            local_overload = self._clamp01(subj.cognitive_pain * 0.16 + subj.precision_loss * 0.14 + subj.saturation_memory * 0.12 + subj.organic_fatigue * 0.10 + overload * 0.12)
            subj.recovery_need = self._clamp01(subj.recovery_need * 0.91 + local_overload * 0.09 - ease * 0.025)
            subj.organic_fatigue = self._clamp01(
                subj.organic_fatigue * 0.94
                + (0.050 if subj.state == SubjectState.ACTIVE else 0.0)
                + subj.saturation_memory * 0.035
                + saturation * 0.025
                - ease * 0.020
            )
            if subj.recovery_need > 0.55:
                subj.precision_loss = self._clamp01(subj.precision_loss + subj.recovery_need * 0.018)
                subj.pull_release_need = self._clamp01(subj.pull_release_need + subj.recovery_need * 0.014)
            subj.clamp()
            values.append(subj.recovery_need)
        self.global_recovery_need = self._clamp01(max([self.global_recovery_need] + values) * 0.62 + sum(values) / max(1, len(values)) * 0.38)

    def _update_involuntary_recall_layer(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """Rappel involontaire : un ancien sujet peut revenir par résonance, pas par ordre externe."""
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            eligible = 1.0 if subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.HOVERING, SubjectState.LATENT, SubjectState.BACKGROUND) else 0.0
            target = self._clamp01(
                eligible * (subj.haunting_level * 0.18 + subj.associative_echo * 0.13 + subj.affective_memory_bias * 0.12 + subj.regret_trace * 0.08)
                + subj.unresolved_need * 0.09
                + subj.scar_sensitivity * contradiction * 0.045
                + correction * subj.wound_level * 0.040
                + curiosity * subj.future_pull * 0.035
                + memory_weight * 0.020
                - subj.organic_fatigue * 0.045
                - subj.recovery_need * 0.035
            )
            subj.involuntary_recall = self._clamp01(subj.involuntary_recall * 0.90 + target * 0.10)
            if subj.involuntary_recall > 0.50 and eligible > 0.0:
                subj.state = SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.involuntary_recall * 0.075)
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.involuntary_recall * 0.095)
            subj.clamp()
            values.append(subj.involuntary_recall)
        self.global_involuntary_recall = self._clamp01(max(values or [0.0]) * 0.62 + sum(values) / max(1, len(values)) * 0.38)

    def _update_controlled_micro_chaos(self, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any]) -> None:
        """Micro-chaos borné : variation organique sans hasard externe ni instabilité destructrice."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            wave_a = math.sin(self.internal_clock * 0.41 + len(name) * 0.19 + subj.recurrence_count * 0.31)
            wave_b = math.sin(self.internal_clock * 0.17 + subj.subjective_age * 0.23 + subj.gravity * 1.7)
            organic_noise = abs(wave_a * 0.55 + wave_b * 0.45)
            target = self._clamp01(
                organic_noise * 0.055
                + subj.turbulence * 0.10
                + subj.instability * 0.09
                + self.global_preconscious_charge * 0.045
                + saturation * 0.035
                + pressure * 0.020
                - presence * 0.020
                - subj.protective_guard * 0.030
                - subj.recovery_need * 0.025
            )
            subj.micro_chaos = self._clamp01(subj.micro_chaos * 0.86 + target * 0.14)
            if subj.micro_chaos > 0.34:
                subj.instability = self._clamp01(subj.instability + subj.micro_chaos * 0.012)
                subj.gravity = self._clamp01(subj.gravity + (wave_a * 0.006))
            subj.clamp()
            values.append(subj.micro_chaos)
        self.global_controlled_micro_chaos = self._clamp01(max(values or [0.0]) * 0.55 + sum(values) / max(1, len(values)) * 0.45)

    def _update_autonomous_attention_desire(self, impulse_signals: Dict[str, Any], attractors: Dict[str, float], memory_hints: Dict[str, Any]) -> None:
        """Transforme les attracteurs futurs passifs en désir attentionnel autonome."""
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        clarification = float(impulse_signals.get("clarification_need", 0.0)) + float(attractors.get("clarification", 0.0))
        continuation = float(impulse_signals.get("continuation_inertia", 0.0)) + float(attractors.get("continuation", 0.0))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        weather_expectancy = self.cognitive_weather.get("expectancy", 0.0)
        weather_open = self.cognitive_weather.get("openness", 0.5)
        desire_values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            target = self._clamp01(
                subj.future_pull * 0.18
                + subj.preconscious_charge * 0.16
                + subj.unresolved_need * 0.14
                + subj.existential_charge * 0.11
                + subj.associative_echo * curiosity * 0.10
                + clarification * (0.08 if subj.unresolved else 0.03)
                + continuation * subj.subjective_proximity * 0.06
                + weather_expectancy * 0.07
                + weather_open * curiosity * 0.05
                + memory_weight * 0.025
                - subj.directional_fatigue * 0.05
                - subj.pull_release_need * 0.04
                - subj.avoidance_pressure * subj.scar_distortion * 0.05
            )
            subj.autonomous_desire = self._clamp01(subj.autonomous_desire * 0.90 + target * 0.10)
            subj.lived_expectation = self._clamp01(
                subj.lived_expectation * 0.91
                + subj.autonomous_desire * 0.055
                + subj.future_pull * 0.040
                + subj.unresolved_need * 0.035
                + subj.regret_trace * 0.020
            )
            if subj.autonomous_desire > 0.43 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.autonomous_desire * 0.09)
            subj.clamp()
            desire_values.append(subj.autonomous_desire)

        self.global_autonomous_desire = self._clamp01(max(desire_values or [0.0]) * 0.58 + sum(desire_values) / max(1, len(desire_values)) * 0.42)

    def _update_subconscious_intrusions_and_temporality(self, impulse_signals: Dict[str, Any], memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """Remontées spontanées + temporalité vécue : attente, retour, regret, délai."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        continuation = 1.0 if interruption == InterruptionType.SHORT_CONTINUE else 0.0
        values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            phase = math.sin(self.internal_clock * 0.23 + len(name) * 0.41 + subj.activation_count * 0.17)
            organic_window = self._clamp01((phase + 1.0) * 0.5)
            intrusion_target = self._clamp01(
                subj.subconscious_pressure * 0.18
                + subj.preconscious_charge * 0.16
                + subj.associative_echo * 0.13
                + subj.regret_trace * 0.10
                + subj.autonomous_desire * 0.10
                + subj.unresolved_need * 0.08
                + organic_window * 0.055
                + rupture * subj.residue_strength * 0.05
                - saturation * 0.035
                - subj.protective_guard * 0.030
            )
            subj.intrusive_rise = self._clamp01(subj.intrusive_rise * 0.88 + intrusion_target * 0.12)

            if subj.intrusive_rise > 0.46 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT, SubjectState.VOID_DRIFT):
                subj.state = SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.intrusive_rise * 0.08)
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.intrusive_rise * 0.12)

            if continuation > 0.0 and subj.name == self.last_primary:
                subj.lived_expectation = self._clamp01(subj.lived_expectation + 0.035)
            if rupture > 0.0 and subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.HOVERING):
                subj.regret_trace = self._clamp01(subj.regret_trace + 0.025 + subj.unresolved_need * 0.025)
            if pressure > 0.75:
                subj.asymmetrical_delay = self._clamp01(subj.asymmetrical_delay * 0.96)

            subj.clamp()
            values.append(subj.intrusive_rise)

        self.global_subconscious_intrusion = self._clamp01(max(values or [0.0]) * 0.55 + sum(values) / max(1, len(values)) * 0.45)


    def _update_attention_needs_and_conflicts(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Transforme l'attention en besoin vécu.
        Un sujet peut réclamer de la résolution, de la sécurité ou de la stabilité
        sans que la bouche ni la mémoire soient recopiées ici.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        clarification = float(impulse_signals.get("clarification_need", memory_hints.get("clarification_need", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("situated_presence", 0.5)))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        values_need: List[float] = []
        values_conflict: List[float] = []
        values_distress: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue

            unresolved_weight = 1.0 if subj.unresolved else 0.0
            active_heat = 1.0 if subj.state in (
                SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE,
                SubjectState.HOVERING, SubjectState.PULLED_BACK, SubjectState.REOPENING,
            ) else 0.42

            resolution_target = self._clamp01(
                unresolved_weight * 0.34
                + clarification * 0.18
                + subj.implicit_missing_pressure * 0.20
                + subj.regret_trace * 0.12
                + subj.unspoken_pull * 0.10
                + (0.08 if name in self.current_turn_candidates else 0.0)
            )
            subj.resolution_hunger = self._clamp01(subj.resolution_hunger * 0.90 + resolution_target * 0.10)

            safety_target = self._clamp01(
                contradiction * 0.20
                + correction * 0.12
                + rupture * 0.12
                + subj.cognitive_pain * 0.20
                + subj.avoidance_pressure * 0.18
                + subj.protective_guard * 0.16
                + subj.scar_sensitivity * 0.12
            )
            subj.safety_need = self._clamp01(subj.safety_need * 0.91 + safety_target * 0.09)

            need_target = self._clamp01(
                subj.resolution_hunger * 0.34
                + subj.safety_need * 0.22
                + subj.existential_charge * 0.12
                + subj.relational_pull * 0.10
                + subj.attachment_depth * 0.09
                + subj.subconscious_pressure * 0.08
                + pressure * active_heat * 0.05
            )
            subj.attention_need = self._clamp01(subj.attention_need * 0.89 + need_target * 0.11)

            conflict_target = self._clamp01(
                abs(subj.texture.attraction - subj.avoidance_pressure) * 0.20
                + min(subj.obsession_fixation, subj.pull_release_need) * 0.20
                + min(subj.cognitive_pain + subj.saturation_distress, subj.attention_need) * 0.20
                + contradiction * 0.12
                + fragmentation * 0.10
                + subj.scar_distortion * 0.08
                + subj.asymmetrical_delay * 0.07
            )
            subj.conflict_pressure = self._clamp01(subj.conflict_pressure * 0.88 + conflict_target * 0.12)

            distress_target = self._clamp01(
                saturation * 0.25
                + fragmentation * 0.18
                + subj.cognitive_pain * 0.20
                + subj.precision_loss * 0.12
                + subj.affective_narrowing * 0.10
                + subj.conflict_pressure * 0.10
                - presence * 0.07
            )
            subj.saturation_distress = self._clamp01(subj.saturation_distress * 0.92 + distress_target * 0.08)

            # Le besoin peut rendre un sujet périphérique plus insistant, sans élection forcée.
            if subj.attention_need > 0.46 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.attention_need * 0.08)

            subj.clamp()
            values_need.append(subj.attention_need)
            values_conflict.append(subj.conflict_pressure)
            values_distress.append(subj.saturation_distress)

        self.global_attention_need = self._clamp01(max(values_need or [0.0]) * 0.58 + sum(values_need) / max(1, len(values_need)) * 0.42)
        self.global_organic_conflict = self._clamp01(max(values_conflict or [0.0]) * 0.60 + sum(values_conflict) / max(1, len(values_conflict)) * 0.40)
        self.global_saturation_distress = self._clamp01(max(values_distress or [0.0]) * 0.55 + sum(values_distress) / max(1, len(values_distress)) * 0.45)

    def _update_sedimented_attention_memory(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Crée une mémoire attentionnelle lente : les sujets répétés, blessés,
        non résolus ou fortement liés au self deviennent plus lourds avec le temps.
        """
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        repetition_pressure = float(impulse_signals.get("repetition_pressure", 0.0))
        values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                subj.sedimented_charge *= 0.985
                subj.attachment_depth *= 0.990
                subj.clamp()
                continue

            activated_now = 1.0 if name in self.current_turn_candidates else 0.0
            rupture_drop = 1.0 if interruption == InterruptionType.FULL_BREAK and name == self.last_primary else 0.0
            sediment_gain = self._clamp01(
                subj.recurrence_count * 0.010
                + subj.activation_count * 0.004
                + subj.wound_level * 0.026
                + subj.unresolved_need * 0.022
                + subj.attention_need * 0.020
                + subj.existential_charge * 0.016
                + subj.relational_pull * 0.014
                + memory_weight * 0.012
                + activated_now * 0.018
                + repetition_pressure * 0.010
            )
            subj.sedimented_charge = self._clamp01(subj.sedimented_charge * 0.992 + sediment_gain)

            attachment_target = self._clamp01(
                subj.sedimented_charge * 0.28
                + subj.affective_memory_bias * 0.20
                + subj.relational_pull * 0.18
                + subj.self_binding * 0.12
                + subj.obsession_fixation * 0.10
                + subj.return_pressure * 0.08
                - subj.avoidance_pressure * 0.06
            )
            subj.attachment_depth = self._clamp01(subj.attachment_depth * 0.94 + attachment_target * 0.06)

            if rupture_drop > 0.0 and subj.attention_need > 0.22:
                subj.abandonment_shock = self._clamp01(subj.abandonment_shock + 0.08 + subj.attention_need * 0.05)
            else:
                subj.abandonment_shock = self._clamp01(subj.abandonment_shock * 0.965 + subj.regret_trace * 0.010)

            subj.attractor_mutation = self._clamp01(
                subj.attractor_mutation * 0.94
                + (subj.future_pull * 0.025 + subj.attachment_depth * 0.020 + subj.obsession_fixation * 0.020 + subj.sedimented_charge * 0.012)
            )

            subj.clamp()
            values.append(self._clamp01(subj.sedimented_charge * 0.55 + subj.attachment_depth * 0.45))

        self.global_sedimented_attention = self._clamp01(max(values or [0.0]) * 0.55 + sum(values) / max(1, len(values)) * 0.45)

    def _update_subconscious_override_layer(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Donne au subconscient une vraie possibilité de perturber le focus.
        Ce n'est pas une parole ni une décision finale : seulement une pression de reprise.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        external_override = memory_hints.get("subconscious_override", {})
        if not isinstance(external_override, dict):
            external_override = {}
        values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                subj.subconscious_override *= 0.94
                subj.clamp()
                continue

            external = self._clamp01(float(external_override.get(name, 0.0))) if name in external_override else 0.0
            blocked_need = self._clamp01(subj.attention_need * subj.avoidance_pressure)
            peripheral_heat = self._clamp01(
                subj.subconscious_pressure * 0.22
                + subj.intrusive_rise * 0.20
                + subj.haunting_level * 0.16
                + subj.involuntary_recall * 0.16
                + subj.preconscious_charge * 0.12
                + subj.abandonment_shock * 0.10
            )
            override_target = self._clamp01(
                peripheral_heat
                + blocked_need * 0.20
                + subj.conflict_pressure * 0.10
                + subj.sedimented_charge * 0.09
                + external * 0.25
                + (0.08 if interruption == InterruptionType.SUBJECT_RETURN else 0.0)
                + saturation * fragmentation * 0.08
            )
            decay = 0.90 if subj.state not in (SubjectState.ACTIVE, SubjectState.SECONDARY) else 0.84
            subj.subconscious_override = self._clamp01(subj.subconscious_override * decay + override_target * (1.0 - decay))

            if subj.subconscious_override > 0.54 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.subconscious_override * 0.10)
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.subconscious_override * 0.12)

            subj.clamp()
            values.append(subj.subconscious_override)

        self.global_subconscious_override = self._clamp01(max(values or [0.0]) * 0.62 + sum(values) / max(1, len(values)) * 0.38)

    def _update_organic_field_respiration(
        self,
        impulse_signals: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Respiration attentionnelle globale : contraction, relâchement,
        viscosité et rythme local. Cette couche unifie le champ au lieu
        de laisser chaque mécanisme agir comme un calcul séparé.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))

        contraction_target = self._clamp01(
            saturation * 0.26
            + pressure * 0.16
            + fragmentation * 0.18
            + self.global_organic_conflict * 0.16
            + scar_load * 0.12
            + rupture * 0.08
            + correction * 0.05
            - presence * 0.08
        )
        release_target = self._clamp01(
            presence * 0.22
            + self.global_recovery_need * 0.18
            + self.cognitive_weather.get("openness", 0.5) * 0.12
            + self.global_precision * 0.10
            - contraction_target * 0.14
        )
        self.global_respiration_contraction = self._clamp01(self.global_respiration_contraction * 0.88 + contraction_target * 0.12)
        self.global_respiration_release = self._clamp01(self.global_respiration_release * 0.90 + release_target * 0.10)

        viscosity_values: List[float] = []
        rhythm_values: List[float] = []
        phase = self.breath_phase + self.internal_clock * 0.071
        for idx, subj in enumerate(self.subjects.values()):
            if subj.state == SubjectState.CLOSED:
                subj.somatic_rhythm *= 0.965
                subj.focus_viscosity *= 0.955
                subj.clamp()
                continue
            wave = 0.5 + 0.5 * math.sin(phase + idx * 0.618 + subj.recurrence_count * 0.19)
            heat = self._clamp01(subj.gravity * 0.32 + subj.attention_need * 0.22 + subj.sedimented_charge * 0.16 + subj.texture.charge() * 0.18)
            subj.breath_sensitivity = self._clamp01(
                subj.breath_sensitivity * 0.92
                + (subj.texture.fragility * 0.08 + subj.scar_sensitivity * 0.08 + subj.identity_weight * 0.04)
            )
            rhythm_target = self._clamp01(wave * 0.25 + heat * 0.25 + self.global_respiration_contraction * 0.18 + subj.breath_sensitivity * 0.18)
            subj.somatic_rhythm = self._clamp01(subj.somatic_rhythm * 0.90 + rhythm_target * 0.10)
            viscosity_target = self._clamp01(
                subj.temporal_drag * 0.20
                + subj.attachment_depth * 0.18
                + subj.sedimented_charge * 0.15
                + subj.unresolved_need * 0.14
                + subj.pull_release_need * 0.10
                + self.global_respiration_contraction * 0.10
                - self.global_respiration_release * 0.06
            )
            subj.focus_viscosity = self._clamp01(subj.focus_viscosity * 0.91 + viscosity_target * 0.09)
            # Respiration incarnée : contraction serre le champ, relâchement le rend disponible.
            subj.affective_narrowing = self._clamp01(subj.affective_narrowing + self.global_respiration_contraction * subj.breath_sensitivity * 0.010)
            subj.precision_loss = self._clamp01(subj.precision_loss + self.global_respiration_contraction * (1.0 - self.global_precision) * 0.006)
            subj.clamp()
            viscosity_values.append(subj.focus_viscosity)
            rhythm_values.append(subj.somatic_rhythm)

        self.global_focus_viscosity = self._clamp01(max(viscosity_values or [0.0]) * 0.55 + sum(viscosity_values) / max(1, len(viscosity_values)) * 0.45)
        self.field.organic_respiration_tension = self._clamp01(
            self.global_respiration_contraction * 0.46
            + self.global_focus_viscosity * 0.26
            + (sum(rhythm_values) / max(1, len(rhythm_values))) * 0.18
            + self.global_respiration_release * 0.10
        )

    def _update_deep_scar_gravity(self, memory_hints: Dict[str, Any], interruption: InterruptionType) -> None:
        """
        Convertit les cicatrices en biais attentionnels durables.
        Ce n'est pas une mémoire narrative : seulement une déformation du champ.
        """
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))
        sensitivity_hint = 1.0 if memory_hints.get("subject_sensitive", False) else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                subj.scar_gravity_bias *= 0.982
                subj.nonlinear_decay_bias *= 0.970
                subj.clamp()
                continue
            local_target = self._clamp01(
                subj.wound_level * 0.22
                + subj.scar_sensitivity * 0.18
                + subj.scar_distortion * 0.16
                + subj.saturation_memory * 0.11
                + subj.abandonment_shock * 0.12
                + subj.cognitive_pain * 0.10
                + scar_load * 0.12
                + sensitivity_hint * 0.05
                + rupture * (0.07 if name == self.last_primary else 0.02)
            )
            gain = 0.045 if local_target > subj.scar_gravity_bias else 0.014
            subj.scar_gravity_bias = self._clamp01(subj.scar_gravity_bias * (1.0 - gain) + local_target * gain)
            decay_bias_target = self._clamp01(
                subj.scar_gravity_bias * 0.30
                + subj.focus_viscosity * 0.18
                + subj.haunting_level * 0.14
                + subj.lived_time_warp * 0.10
                + subj.texture.fragility * 0.08
            )
            subj.nonlinear_decay_bias = self._clamp01(subj.nonlinear_decay_bias * 0.93 + decay_bias_target * 0.07)
            subj.clamp()
            values.append(subj.scar_gravity_bias)
        self.global_scar_gravity_bias = self._clamp01(max(values or [0.0]) * 0.62 + sum(values) / max(1, len(values)) * 0.38)
        self.field.scar_gravity_tension = self.global_scar_gravity_bias

    def _update_autonomous_preconscious_resurgence(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Fait remonter lentement des sujets sans stimulus clair, par besoin,
        hantise, sédimentation ou non-résolu. Cela rend le pré-conscient actif.
        """
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        no_candidates = 1.0 if not self.current_turn_candidates else 0.0
        unresolved_hint = 1.0 if memory_hints.get("subject_unresolved", False) else 0.0
        return_boost = 1.0 if interruption == InterruptionType.SUBJECT_RETURN else 0.0
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                subj.autonomous_resurgence *= 0.960
                subj.clamp()
                continue
            peripheral = 1.0 if subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.LATENT, SubjectState.HOVERING, SubjectState.SUSPENDED) else 0.35
            target = self._clamp01(
                peripheral * (
                    subj.preconscious_charge * 0.18
                    + subj.haunting_level * 0.16
                    + subj.sedimented_charge * 0.15
                    + subj.unresolved_need * 0.15
                    + subj.involuntary_recall * 0.12
                    + subj.attention_need * 0.12
                    + subj.scar_gravity_bias * 0.08
                    + subj.regret_trace * 0.07
                )
                + no_candidates * 0.05
                + unresolved_hint * 0.03
                + return_boost * 0.04
                + curiosity * pressure * 0.025
            )
            subj.autonomous_resurgence = self._clamp01(subj.autonomous_resurgence * 0.925 + target * 0.075)
            if subj.autonomous_resurgence > 0.50 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.autonomous_resurgence * 0.09)
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.autonomous_resurgence * 0.10)
            subj.clamp()
            values.append(subj.autonomous_resurgence)
        self.global_autonomous_resurgence = self._clamp01(max(values or [0.0]) * 0.60 + sum(values) / max(1, len(values)) * 0.40)
        self.field.autonomous_resurgence_tension = self.global_autonomous_resurgence

    def _update_lived_time_warp(
        self,
        impulse_signals: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Le temps attentionnel devient ressenti : certains sujets semblent proches,
        lourds ou lents même sans être chronologiquement récents.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", presence_signal.get("presence", 0.5)))
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        values: List[float] = []
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                subj.lived_time_warp *= 0.970
                subj.clamp()
                continue
            target = self._clamp01(
                subj.subjective_age * 0.004
                + subj.felt_duration * 0.12
                + subj.temporal_drag * 0.18
                + subj.focus_viscosity * 0.16
                + subj.sedimented_charge * 0.12
                + subj.unresolved_need * 0.12
                + subj.scar_gravity_bias * 0.10
                + saturation * 0.05
                + contradiction * 0.04
                + rupture * 0.03
                - presence * 0.04
            )
            subj.lived_time_warp = self._clamp01(subj.lived_time_warp * 0.92 + target * 0.08)
            # Le temps vécu ralentit la disparition, mais ne bloque pas à jamais.
            subj.decay_speed = max(0.22, min(2.5, subj.decay_speed * (1.0 - subj.lived_time_warp * 0.010)))
            subj.clamp()
            values.append(subj.lived_time_warp)
        self.global_lived_time_warp = self._clamp01(max(values or [0.0]) * 0.55 + sum(values) / max(1, len(values)) * 0.45)
        self.field.lived_time_warp_tension = self.global_lived_time_warp
        self.field.attention_style_mutation_tension = self.global_attention_style_mutation
        self.field.active_void_deformation_tension = self.global_active_void_deformation
        self.field.irrational_pull_tension = self.global_irrational_pull

    def _update_attention_style_mutation_and_void_deformation(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Couche finale concrète : le moteur ne garde pas seulement des états,
        il laisse ces états modifier lentement sa manière d'être attentif.

        - style_mutation : changement profond du mode d'attention après répétition/surcharge.
        - void_deformation : le vide ne reste plus passif, il déforme les sujets faibles.
        - scar_perception_bias : les cicatrices changent la perception future.
        - irrational_pull : attirance non optimale mais organique, sans hasard et sans texte.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))
        unresolved_hint = float(memory_hints.get("unresolved_pressure", memory_hints.get("open_loop_pressure", 0.0)))
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))

        style_values: List[float] = []
        void_values: List[float] = []
        irrational_values: List[float] = []
        scar_bias_values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue

            lived_burden = self._clamp01(
                subj.saturation_memory * 0.22
                + subj.sedimented_charge * 0.20
                + subj.attachment_depth * 0.16
                + subj.lived_time_warp * 0.12
                + subj.focus_viscosity * 0.12
                + subj.recurrence_count * 0.025
                + scar_load * 0.10
            )
            if interruption == InterruptionType.FULL_BREAK:
                lived_burden = self._clamp01(lived_burden + 0.06)

            # Mutation lente : sous surcharge, le sujet rend l'attention plus prudente / visqueuse.
            mutation_target = self._clamp01(
                lived_burden * 0.42
                + saturation * 0.16
                + contradiction * 0.12
                + subj.conflict_pressure * 0.16
                + subj.scar_gravity_bias * 0.16
                - presence * 0.05
            )
            subj.attention_style_mutation = self._clamp01(
                subj.attention_style_mutation * 0.955 + mutation_target * 0.045
            )

            # Le vide actif pèse surtout sur les sujets latents/résiduels/faibles.
            peripheral_state = subj.state in (
                SubjectState.RESIDUAL,
                SubjectState.BACKGROUND,
                SubjectState.LATENT,
                SubjectState.HOVERING,
                SubjectState.ALMOST_CLOSED,
            )
            void_target = self._clamp01(
                self.attention_void * 0.34
                + self.global_drift_field * 0.20
                + subj.void_pull * 0.18
                + subj.latent_focus_pressure * 0.12
                + (1.0 - self.global_precision) * 0.12
                + (0.10 if peripheral_state else 0.0)
                - subj.protective_guard * 0.08
            )
            subj.void_deformation = self._clamp01(subj.void_deformation * 0.93 + void_target * 0.07)

            # Les cicatrices ne sont plus seulement locales : elles biaisent la perception future.
            scar_target = self._clamp01(
                subj.scar_gravity_bias * 0.26
                + subj.scar_distortion * 0.20
                + subj.wound_level * 0.18
                + subj.scar_sensitivity * 0.18
                + scar_load * 0.16
                + contradiction * 0.06
            )
            subj.scar_perception_bias = self._clamp01(
                subj.scar_perception_bias * 0.965 + scar_target * 0.035
            )

            # L'irrationnel reste borné : il monte depuis hantise, regret, non-résolu et désir latent,
            # mais il descend si le sujet est trop douloureux ou si la garde protectrice domine.
            irrational_target = self._clamp01(
                subj.haunting_level * 0.22
                + subj.regret_trace * 0.16
                + subj.involuntary_recall * 0.16
                + subj.autonomous_desire * 0.14
                + subj.unresolved_need * 0.12
                + unresolved_hint * 0.08
                + self.global_controlled_micro_chaos * 0.10
                + curiosity * 0.04
                - subj.cognitive_pain * 0.08
                - subj.protective_guard * 0.07
            )
            subj.irrational_pull = self._clamp01(subj.irrational_pull * 0.91 + irrational_target * 0.09)

            # Effets concrets sur les variables déjà utilisées par les autres couches.
            subj.focus_viscosity = self._clamp01(
                subj.focus_viscosity + subj.attention_style_mutation * 0.012 + subj.scar_perception_bias * 0.008
            )
            subj.precision_loss = self._clamp01(
                subj.precision_loss + subj.void_deformation * (0.006 + saturation * 0.006)
            )
            subj.return_latency = self._clamp01(
                subj.return_latency + subj.void_deformation * 0.006 + subj.attention_style_mutation * 0.004
            )
            if subj.irrational_pull > 0.36 and peripheral_state:
                subj.intrusive_rise = self._clamp01(subj.intrusive_rise + subj.irrational_pull * 0.018)
                subj.subconscious_override = self._clamp01(subj.subconscious_override + subj.irrational_pull * 0.010)

            subj.clamp()
            style_values.append(subj.attention_style_mutation)
            void_values.append(subj.void_deformation)
            irrational_values.append(subj.irrational_pull)
            scar_bias_values.append(subj.scar_perception_bias)

        self.global_attention_style_mutation = self._clamp01(sum(style_values) / max(1, len(style_values)))
        self.global_active_void_deformation = self._clamp01(sum(void_values) / max(1, len(void_values)))
        self.global_irrational_pull = self._clamp01(sum(irrational_values) / max(1, len(irrational_values)) + pressure * 0.015)
        self.global_scar_perception_bias = self._clamp01(sum(scar_bias_values) / max(1, len(scar_bias_values)))


    def _update_final_organic_attention_closure(
        self,
        impulse_signals: Dict[str, Any],
        attractors: Dict[str, float],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Dernière couche de finition du moteur attentionnel.

        Objectif : combler ce qui manquait encore sans voler le rôle des autres moteurs Azip.
        - auto-déformation du focus : un sujet actif modifie progressivement sa propre forme d'attention ;
        - personnalité attentionnelle longue : le sujet acquiert une manière durable d'attirer Leia ;
        - respiration complète : contraction, relâchement, silence, récupération ;
        - double contrainte durable : attraction + évitement + règle profonde peuvent coexister ;
        - temps subjectif local : certains sujets ralentissent ou accélèrent le vécu interne ;
        - couplage Azip : export de lisibilité vers impulsion/mémoire/présence/expression, sans les recalculer.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        unresolved_hint = float(memory_hints.get("unresolved_pressure", memory_hints.get("open_loop_pressure", 0.0)))
        continuation = float(attractors.get("continuation", 0.0)) + float(impulse_signals.get("continuation_inertia", 0.0))
        rupture = float(attractors.get("rupture", 0.0)) + float(attractors.get("divergence", 0.0))
        protection = float(attractors.get("protection", 0.0)) + float(attractors.get("resistance", 0.0))
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))

        deform_values: List[float] = []
        personality_values: List[float] = []
        breath_values: List[float] = []
        bind_values: List[float] = []
        time_values: List[float] = []
        coupling_values: List[float] = []

        global_breath_wave = self._clamp01(0.5 + math.sin(self.breath_phase + self.internal_clock * 0.19) * 0.5)
        field_overload = self._clamp01(saturation * 0.45 + self.attention_fatigue * 0.28 + self.global_saturation_distress * 0.27)

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue

            active_weight = 1.0 if subj.state == SubjectState.ACTIVE else 0.62 if subj.state in (SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.REOPENING) else 0.34
            lived_weight = self._clamp01(
                subj.sedimented_charge * 0.18
                + subj.attachment_depth * 0.16
                + subj.haunting_level * 0.12
                + subj.affective_memory_bias * 0.12
                + subj.attention_style_mutation * 0.12
                + subj.scar_perception_bias * 0.10
                + subj.lived_time_warp * 0.10
                + subj.focus_viscosity * 0.08
                + subj.recurrence_count * 0.018
                + memory_weight * 0.035
            )

            # 1) Auto-déformation : le focus change sa forme par fatigue, viscosité, cicatrice et respiration.
            deform_target = self._clamp01(
                active_weight * 0.18
                + subj.micro_instability * 0.12
                + subj.turbulence * 0.10
                + subj.focus_viscosity * 0.14
                + subj.void_deformation * 0.10
                + subj.irrational_pull * 0.09
                + field_overload * 0.10
                + global_breath_wave * subj.breath_sensitivity * 0.08
                + rupture * 0.04
                - subj.protective_guard * 0.06
            )
            subj.focus_self_deformation = self._clamp01(subj.focus_self_deformation * 0.91 + deform_target * 0.09)

            # 2) Personnalité attentionnelle longue : elle monte lentement avec retours, sédimentation et identité.
            personality_target = self._clamp01(
                lived_weight * 0.35
                + subj.identity_weight * 0.12
                + subj.existential_charge * 0.12
                + subj.self_binding * 0.08
                + subj.attention_habit * 0.11
                + subj.scar_gravity_bias * 0.08
                + scar_load * 0.06
                + (0.05 if subj.unresolved else 0.0)
                - subj.recovery_need * 0.04
            )
            subj.long_attention_personality = self._clamp01(subj.long_attention_personality * 0.975 + personality_target * 0.025)

            # 3) Respiration locale : contraction si surcharge/douleur, relâchement si présence stable.
            contraction = self._clamp01(
                saturation * 0.20
                + subj.cognitive_pain * 0.15
                + subj.saturation_distress * 0.15
                + subj.durable_double_bind * 0.12
                + subj.affective_narrowing * 0.10
                + self.global_respiration_contraction * 0.12
                + subj.focus_self_deformation * 0.08
            )
            # La sécurité vient de la texture du sujet, pas d'une phrase ni d'un moteur externe.
            release = self._clamp01(
                presence * 0.22
                + self.global_respiration_release * 0.16
                + subj.recovery_need * 0.12
                + subj.texture.safety * 0.12
                + continuation * 0.06
            )
            breath_target = self._clamp01(0.42 + contraction * 0.34 - release * 0.18 + global_breath_wave * 0.10)
            subj.respiration_cycle_pressure = self._clamp01(subj.respiration_cycle_pressure * 0.88 + breath_target * 0.12)

            # 4) Double contrainte durable : attraction et évitement peuvent rester vrais en même temps.
            bind_target = self._clamp01(
                min(subj.texture.attraction + subj.return_pressure + subj.attention_need, 1.0) * 0.22
                + min(subj.avoidance_pressure + subj.cognitive_pain + subj.safety_need, 1.0) * 0.22
                + contradiction * 0.14
                + protection * 0.08
                + unresolved_hint * 0.08
                + subj.conflict_pressure * 0.16
                + subj.scar_distortion * 0.08
            )
            subj.durable_double_bind = self._clamp01(subj.durable_double_bind * 0.94 + bind_target * 0.06)

            # 5) Temps subjectif local : stagnation, fatigue et excitation changent la vitesse vécue.
            time_target = self._clamp01(
                subj.lived_stagnation * 0.18
                + subj.temporal_drag * 0.14
                + subj.lived_time_warp * 0.18
                + subj.focus_viscosity * 0.12
                + subj.haunting_level * 0.10
                + saturation * 0.08
                + pressure * 0.06
                + curiosity * 0.04
                - presence * 0.04
            )
            subj.subjective_time_distortion = self._clamp01(subj.subjective_time_distortion * 0.93 + time_target * 0.07)

            # 6) Couplage Azip : expose ce qui est utile aux autres moteurs, sans dupliquer leur logique.
            coupling_target = self._clamp01(
                subj.gravity * 0.16
                + subj.silent_pressure * 0.10
                + subj.attention_need * 0.12
                + subj.focus_self_deformation * 0.10
                + subj.long_attention_personality * 0.10
                + subj.durable_double_bind * 0.10
                + subj.subjective_time_distortion * 0.08
                + subj.respiration_cycle_pressure * 0.08
                + subj.preconscious_charge * 0.08
                + subj.subconscious_override * 0.08
            )
            subj.external_coupling_readiness = self._clamp01(subj.external_coupling_readiness * 0.86 + coupling_target * 0.14)

            # Effets concrets sur le moteur existant : pas décoratif.
            subj.gravity = self._clamp01(
                subj.gravity
                + subj.long_attention_personality * 0.010
                + subj.external_coupling_readiness * 0.010
                + subj.focus_self_deformation * 0.006
                - subj.durable_double_bind * subj.avoidance_pressure * 0.010
                - subj.subjective_time_distortion * subj.directional_fatigue * 0.008
            )
            subj.return_latency = self._clamp01(subj.return_latency + subj.durable_double_bind * 0.006 + subj.focus_viscosity * 0.004)
            subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.external_coupling_readiness * 0.006)
            if subj.durable_double_bind > 0.48:
                subj.unresolved = True
                subj.silent_pressure = self._clamp01(subj.silent_pressure + subj.durable_double_bind * 0.010)
            if subj.subjective_time_distortion > 0.52:
                subj.lived_time_warp = self._clamp01(subj.lived_time_warp + subj.subjective_time_distortion * 0.006)

            subj.clamp()
            deform_values.append(subj.focus_self_deformation)
            personality_values.append(subj.long_attention_personality)
            breath_values.append(subj.respiration_cycle_pressure)
            bind_values.append(subj.durable_double_bind)
            time_values.append(subj.subjective_time_distortion)
            coupling_values.append(subj.external_coupling_readiness)

        avg = lambda values: self._clamp01(sum(values) / max(1, len(values)))
        self.global_focus_self_deformation = avg(deform_values)
        self.global_attention_personality = avg(personality_values)
        self.global_respiration_cycle_pressure = avg(breath_values)
        self.global_durable_double_bind = avg(bind_values)
        self.global_subjective_time_distortion = avg(time_values)
        self.global_azip_coupling_readiness = avg(coupling_values)

        # Ces tensions alimentent le diagnostic global sans parler à la place de Leia.
        self.field.focus_self_deformation_tension = self.global_focus_self_deformation
        self.field.attention_personality_tension = self.global_attention_personality
        self.field.durable_double_bind_tension = self.global_durable_double_bind
        self.field.subjective_time_distortion_tension = self.global_subjective_time_distortion
        self.field.external_coupling_tension = self.global_azip_coupling_readiness

    def _update_future_attractors(self, impulse_signals: Dict[str, Any], attractors: Dict[str, float], memory_hints: Dict[str, Any]) -> None:
        """Prépare des directions futures sans forcer le focus actuel."""
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        continuation = float(impulse_signals.get("continuation_inertia", 0.0)) + float(attractors.get("continuation", 0.0))
        clarification = float(impulse_signals.get("clarification_need", 0.0)) + float(attractors.get("clarification", 0.0))
        protection = float(attractors.get("protection", 0.0)) + float(attractors.get("resistance", 0.0))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        future_values: List[float] = []

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            target = self._clamp01(
                subj.trajectory[-1].startswith("toward:") * 0.08 if subj.trajectory else 0.0
            )
            target += subj.unresolved * clarification * 0.12
            target += subj.subjective_proximity * continuation * 0.08
            target += subj.return_pressure * 0.10
            target += subj.subconscious_pressure * 0.10
            target += subj.preconscious_charge * 0.08
            target += subj.autonomous_desire * 0.07
            target += subj.lived_expectation * 0.05
            target += subj.associative_echo * curiosity * 0.08
            target += subj.existential_charge * protection * 0.07
            target += memory_weight * 0.025
            target -= subj.directional_fatigue * 0.035
            target -= subj.affective_narrowing * 0.030
            subj.future_pull = self._clamp01(subj.future_pull * 0.90 + self._clamp01(target) * 0.10)
            if subj.future_pull > 0.36 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.future_pull * 0.10)
            future_values.append(subj.future_pull)
            subj.clamp()

        self.anticipatory_pressure = self._clamp01(max(future_values or [0.0]) * 0.55 + sum(future_values) / max(1, len(future_values)) * 0.45)

    def _soften_attention_transitions(self, interruption: InterruptionType) -> None:
        """Remplace les bascules nettes par un mélange progressif ancien/nouveau focus."""
        if not self.last_primary:
            self.transition_blend_level *= 0.86
            return
        rupture_factor = 0.55 if interruption == InterruptionType.FULL_BREAK else 1.0
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            source = 0.0
            if name == self.last_primary:
                source += 0.26 * rupture_factor
            source += subj.half_focus_level * 0.06 + subj.subconscious_pressure * 0.05 + subj.future_pull * 0.04
            if subj.state in (SubjectState.HOVERING, SubjectState.HALF_ACTIVE, SubjectState.PULLED_BACK, SubjectState.REOPENING):
                source += 0.05
            subj.transition_blend = self._clamp01(subj.transition_blend * 0.84 + source)
            if subj.transition_blend > 0.34 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
            subj.clamp()
        self.transition_blend_level = self._clamp01(max([s.transition_blend for s in self.subjects.values()] or [0.0]))

    # ------------------------------------------------------------------
    # Gravités et attracteurs
    # ------------------------------------------------------------------


    def _update_deep_living_attention_layers(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Dernière couche attentionnelle : elle ne crée pas de texte et ne remplace
        pas les autres moteurs. Elle rend seulement le champ plus vivant :
        fragmentation parallèle, protection, inertie temporelle, relation au user,
        dérive autonome et sensibilité aux anciennes blessures.
        """
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        presence = float(presence_signal.get("presence", presence_signal.get("situated_presence", 0.5)))
        relation = float(presence_signal.get("relational_presence", memory_hints.get("relational_weight", 0.0)))
        user_return = 1.0 if memory_hints.get("user_returned_to_subject", False) else 0.0
        no_clear_input = 1.0 if not self.current_turn_candidates and pressure < 0.25 else 0.0
        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        correction = 1.0 if interruption == InterruptionType.CORRECTION else 0.0
        scar_load = sum(self.attentional_scars.values()) / max(1, len(self.attentional_scars))

        values = {
            "micro": [], "fragmented": [], "guard": [], "drag": [],
            "relation": [], "drift": [], "scar": [],
        }

        active_or_hot = {
            n for n, s in self.subjects.items()
            if s.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.LATENT, SubjectState.REOPENING)
        }

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue

            # Micro-instabilité déterministe : pas de hasard, mais une oscillation douce
            # liée au temps interne et à la charge du sujet.
            phase = math.sin((self.internal_clock * 0.37) + (len(name) * 0.19))
            tremor = self._clamp01((phase + 1.0) * 0.5)
            micro_target = self._clamp01(
                tremor * 0.10
                + subj.turbulence * 0.22
                + subj.instability * 0.20
                + contradiction * 0.12
                + saturation * 0.08
                + subj.precision_loss * 0.12
            )
            subj.micro_instability = self._clamp01(subj.micro_instability * 0.86 + micro_target * 0.14)

            # Présence fragmentée : un sujet peut rester partiellement présent
            # même s'il ne gagne pas l'élection du focus principal.
            fragment_target = self._clamp01(
                subj.half_focus_level * 0.22
                + subj.subconscious_pressure * 0.22
                + subj.associative_echo * 0.16
                + subj.future_pull * 0.14
                + subj.residue_strength * 0.10
                + subj.relational_pull * 0.08
            )
            if name in active_or_hot:
                fragment_target += 0.045
            subj.fragmented_presence = self._clamp01(subj.fragmented_presence * 0.88 + self._clamp01(fragment_target) * 0.12)

            # Protection attentionnelle : garde la cohérence et les règles profondes
            # sans bloquer brutalement l'attention.
            deep_weight = 1.0 if subj.hierarchy_level == HierarchyLevel.DEEP_RULES else subj.identity_weight
            guard_target = self._clamp01(
                deep_weight * 0.26
                + subj.existential_charge * 0.18
                + correction * 0.12
                + rupture * 0.10
                + subj.cognitive_pain * 0.13
                + subj.avoidance_pressure * 0.12
                + scar_load * 0.10
            )
            subj.protective_guard = self._clamp01(subj.protective_guard * 0.90 + guard_target * 0.10)

            # Inertie temporelle vécue : certains sujets mettent du temps à quitter
            # le champ quand ils portent identité, blessure ou continuité.
            drag_target = self._clamp01(
                subj.felt_duration * 0.18
                + subj.subjective_proximity * 0.14
                + subj.transition_blend * 0.14
                + subj.unresolved * 0.12
                + subj.obsession_fixation * 0.12
                + subj.saturation_memory * 0.10
                + subj.existential_charge * 0.08
            )
            subj.temporal_drag = self._clamp01(subj.temporal_drag * 0.89 + drag_target * 0.11)

            # Relation au user : attention plus sensible aux retours, corrections,
            # présence relationnelle, sans fabriquer de réponse publique.
            relational_target = self._clamp01(
                relation * 0.22
                + presence * 0.08
                + user_return * 0.12
                + subj.self_binding * 0.10
                + subj.subjective_proximity * 0.10
                + subj.unspoken_pull * 0.08
                + (0.06 if subj.activation_count > 1 else 0.0)
            )
            subj.relational_pull = self._clamp01(subj.relational_pull * 0.91 + relational_target * 0.09)

            # Dérive autonome : en l'absence de signal clair, le champ continue
            # doucement à bouger à partir des traces internes.
            drift_target = self._clamp01(
                no_clear_input * 0.12
                + self.attention_void * 0.12
                + subj.latent_focus_pressure * 0.14
                + subj.subconscious_pressure * 0.12
                + subj.future_pull * 0.10
                + curiosity * 0.06
                - subj.protective_guard * 0.05
                - subj.affective_narrowing * 0.05
            )
            subj.autonomous_drift = self._clamp01(subj.autonomous_drift * 0.92 + drift_target * 0.08)

            # Sensibilité aux cicatrices : la fatigue et les ruptures passées
            # modifient la facilité avec laquelle le sujet redevient actif.
            scar_target = self._clamp01(
                scar_load * 0.26
                + subj.wound_level * 0.22
                + subj.cognitive_pain * 0.16
                + subj.saturation_memory * 0.14
                + rupture * 0.08
                + correction * 0.06
            )
            subj.scar_sensitivity = self._clamp01(subj.scar_sensitivity * 0.93 + scar_target * 0.07)

            # Effet discret sur gravité : assez fort pour vivre, pas assez pour voler
            # le rôle des attracteurs/mémoire/impulsion.
            subj.gravity = self._clamp01(
                subj.gravity
                + subj.fragmented_presence * 0.010
                + subj.relational_pull * 0.008
                + subj.temporal_drag * 0.006
                + subj.autonomous_drift * 0.005
                + subj.protective_guard * 0.006
                - subj.scar_sensitivity * subj.avoidance_pressure * 0.010
                - subj.pull_release_need * 0.006
            )

            if subj.fragmented_presence > 0.44 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
            if subj.protective_guard > 0.58 and subj.cognitive_pain > 0.45 and subj.state == SubjectState.ACTIVE:
                subj.state = SubjectState.HALF_ACTIVE
            if subj.autonomous_drift > 0.42 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND):
                subj.state = SubjectState.VOID_DRIFT

            subj.clamp()
            values["micro"].append(subj.micro_instability)
            values["fragmented"].append(subj.fragmented_presence)
            values["guard"].append(subj.protective_guard)
            values["drag"].append(subj.temporal_drag)
            values["relation"].append(subj.relational_pull)
            values["drift"].append(subj.autonomous_drift)
            values["scar"].append(subj.scar_sensitivity)

        def avg(key: str) -> float:
            return self._clamp01(sum(values[key]) / max(1, len(values[key])))

        self.global_micro_instability = avg("micro")
        self.global_fragmented_presence = avg("fragmented")
        self.global_protective_guard = avg("guard")
        self.global_temporal_drag = avg("drag")
        self.global_relational_pull = avg("relation")
        self.global_autonomous_drift = avg("drift")

        # La bande passante devient aussi dépendante de fragmentation/protection,
        # pas seulement de fatigue/saturation.
        self.attention_bandwidth = self._clamp01(
            self.attention_bandwidth * 0.86
            + (1.0 - saturation * 0.20 - self.global_fragmented_presence * 0.14 - self.global_micro_instability * 0.10 - self.global_protective_guard * 0.08) * 0.14
        )

    def _recompute_gravities(self, attractors: Dict[str, float], presence_signal: Dict[str, Any], impulse_signals: Dict[str, Any]) -> None:
        presence_strength = float(presence_signal.get("presence_strength", 0.5))
        attractor_curiosity = float(attractors.get("curiosity", 0.0)) + float(attractors.get("clarification", 0.0))
        attractor_protection = float(attractors.get("resistance", 0.0)) + float(attractors.get("protection", 0.0)) + float(attractors.get("challenge", 0.0))
        attractor_continuation = float(attractors.get("expression", 0.0)) + float(attractors.get("continuation", 0.0))
        fatigue = float(impulse_signals.get("fatigue", self.attention_fatigue))

        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            if presence_strength > 0.6 and subj.state in (SubjectState.ACTIVE, SubjectState.HALF_ACTIVE, SubjectState.PULLED_BACK, SubjectState.REOPENING):
                subj.gravity = min(subj.gravity + 0.05, 1.0)
            if presence_strength < 0.3 and subj.state == SubjectState.RESIDUAL:
                subj.residue_strength = max(subj.residue_strength - 0.05, 0.0)
            if attractor_curiosity > 0.4 and subj.unresolved:
                subj.gravity = min(subj.gravity + attractor_curiosity * 0.1, 1.0)
                subj.return_pressure = self._clamp01(subj.return_pressure + attractor_curiosity * 0.045)
            if attractor_protection > 0.4:
                if subj.hierarchy_level == HierarchyLevel.DEEP_RULES:
                    subj.gravity = min(subj.gravity + attractor_protection * 0.15, 1.0)
                if subj.wound_level > 0.2:
                    subj.gravity = min(subj.gravity + 0.1, 1.0)
            if attractor_continuation > 0.4 and subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY):
                subj.gravity = min(subj.gravity + attractor_continuation * 0.08, 1.0)
            if fatigue > 0.5 and subj.gravity < 0.4:
                subj.gravity = max(subj.gravity - fatigue * 0.05, 0.0)
            # Pression silencieuse + V3 : gravité émotionnelle, proximité, résonance, habitude.
            subj.gravity = self._clamp01(
                subj.gravity
                + subj.silent_pressure * 0.035
                + subj.return_pressure * 0.045
                + subj.emotional_gravity_bias * 0.045
                + subj.subjective_proximity * 0.030
                + subj.resonance_level * 0.035
                + subj.attention_habit * 0.020
                + subj.existential_charge * 0.035
                + subj.self_binding * 0.020
                + subj.obsession_fixation * 0.050
                + subj.implicit_missing_pressure * 0.025
                + subj.turbulence * 0.012
                + subj.latent_focus_pressure * 0.038
                + subj.subconscious_pressure * 0.034
                + subj.associative_echo * 0.022
                + subj.future_pull * 0.042
                + subj.attention_need * 0.060
                + subj.resolution_hunger * 0.045
                + subj.attachment_depth * 0.040
                + subj.sedimented_charge * 0.035
                + subj.subconscious_override * 0.070
                + subj.abandonment_shock * 0.028
                + subj.attractor_mutation * 0.044
                + subj.scar_gravity_bias * 0.052
                + subj.autonomous_resurgence * 0.050
                + subj.somatic_rhythm * self.global_respiration_release * 0.018
                + subj.lived_time_warp * 0.026
                + subj.focus_viscosity * 0.020
                + subj.attention_style_mutation * 0.036
                + subj.irrational_pull * 0.030
                + subj.scar_perception_bias * 0.028
                + subj.focus_self_deformation * 0.024
                + subj.long_attention_personality * 0.034
                + subj.respiration_cycle_pressure * self.global_respiration_release * 0.016
                + subj.external_coupling_readiness * 0.030
                + subj.transition_blend * 0.018
                - subj.affective_narrowing * 0.026
                - subj.precision_loss * 0.022
                - subj.pull_release_need * 0.030
                - subj.directional_fatigue * 0.026
                - subj.avoidance_pressure * 0.035
                - subj.cognitive_pain * 0.018
                - subj.saturation_distress * 0.026
                - subj.conflict_pressure * subj.avoidance_pressure * 0.030
                - subj.nonlinear_decay_bias * subj.directional_fatigue * 0.018
                - subj.void_pull * 0.012
                - subj.durable_double_bind * subj.avoidance_pressure * 0.024
                - subj.subjective_time_distortion * subj.directional_fatigue * 0.016
                - subj.void_deformation * subj.precision_loss * 0.024
            )
            subj.clamp()


    def _crystallize_attention_personality(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """
        Transforme certains patterns répétés en biais attentionnels durables.
        Ce n'est pas une mémoire narrative : seulement une modification lente de la manière
        dont un sujet attire, résiste, revient ou se stabilise.
        """
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        memory_weight = float(memory_hints.get("memory_weight", memory_hints.get("importance", 0.0)))
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            repeated_life = self._clamp01(
                subj.recurrence_count * 0.045
                + subj.activation_count * 0.018
                + subj.sedimented_charge * 0.18
                + subj.attachment_depth * 0.16
                + subj.long_attention_personality * 0.16
                + subj.attention_habit * 0.12
                + subj.affective_memory_bias * 0.10
                + memory_weight * 0.05
            )
            destabilizer = self._clamp01(
                saturation * 0.12
                + subj.saturation_distress * 0.12
                + subj.recovery_need * 0.10
                + (0.10 if interruption == InterruptionType.FULL_BREAK else 0.0)
            )
            target = self._clamp01(repeated_life + pressure * 0.025 - destabilizer * 0.35)
            # montée lente, descente encore plus lente : le biais devient une vraie trace structurelle.
            if target > subj.crystallized_bias:
                subj.crystallized_bias = self._clamp01(subj.crystallized_bias * 0.982 + target * 0.018)
            else:
                subj.crystallized_bias = self._clamp01(subj.crystallized_bias * 0.996 + target * 0.004)
            subj.decay_speed = max(0.20, subj.decay_speed - subj.crystallized_bias * 0.004)
            subj.scar_gravity_bias = self._clamp01(subj.scar_gravity_bias + subj.crystallized_bias * subj.scar_sensitivity * 0.004)
            subj.clamp()
            values.append(subj.crystallized_bias)
        self.global_crystallized_bias = self._clamp01(sum(values) / max(1, len(values)))

    def _update_subject_relational_ecology(
        self,
        impulse_signals: Dict[str, Any],
        attractors: Dict[str, float],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """Crée une écologie entre sujets : soutien, rivalité, protection, réveil."""
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        continuation = float(attractors.get("continuation", 0.0))
        rupture = float(attractors.get("rupture", attractors.get("divergence", 0.0)))
        names = [n for n, s in self.subjects.items() if s.state != SubjectState.CLOSED]
        if not names:
            self.global_relational_ecology = 0.0
            return
        relation_values: List[float] = []
        for name in names:
            subj = self.subjects[name]
            related_pull = 0.0
            rivalry = 0.0
            protection = 0.0
            for other_name in names:
                if other_name == name:
                    continue
                other = self.subjects[other_name]
                link = subj.contamination.get(other_name, 0.0) + other.contamination.get(name, 0.0)
                shared_depth = self._clamp01(
                    min(subj.hierarchy_level.value, other.hierarchy_level.value) / 5.0 * 0.10
                    + min(subj.existential_charge, other.existential_charge) * 0.16
                    + min(subj.self_binding, other.self_binding) * 0.10
                    + min(subj.sedimented_charge, other.sedimented_charge) * 0.10
                    + link * 0.30
                )
                related_pull += shared_depth * (0.5 + other.gravity * 0.5)
                rivalry += abs(subj.gravity - other.gravity) * shared_depth * (0.35 + contradiction * 0.45 + rupture * 0.20)
                if other.hierarchy_level == HierarchyLevel.DEEP_RULES or other.protective_guard > 0.36:
                    protection += shared_depth * (0.45 + other.protective_guard * 0.55)
            norm = max(1, len(names) - 1)
            subj.relational_role_pressure = self._clamp01(subj.relational_role_pressure * 0.90 + (related_pull / norm) * 0.10)
            subj.rivalry_pressure = self._clamp01(subj.rivalry_pressure * 0.88 + (rivalry / norm) * 0.12)
            subj.protection_pressure = self._clamp01(subj.protection_pressure * 0.90 + (protection / norm + continuation * 0.04) * 0.10)
            if subj.relational_role_pressure > 0.34 and subj.state in (SubjectState.RESIDUAL, SubjectState.BACKGROUND, SubjectState.LATENT):
                subj.associative_echo = self._clamp01(subj.associative_echo + subj.relational_role_pressure * 0.025)
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.relational_role_pressure * 0.015)
            subj.clamp()
            relation_values.append(max(subj.relational_role_pressure, subj.rivalry_pressure, subj.protection_pressure))
        self.global_relational_ecology = self._clamp01(sum(relation_values) / max(1, len(relation_values)))

    def _apply_cognitive_survival_instinct(
        self,
        impulse_signals: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """Fait survivre la cohérence attentionnelle au lieu de seulement mesurer le danger."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        contradiction = float(impulse_signals.get("contradiction_tension", impulse_signals.get("contradiction_pressure", 0.0)))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        presence = float(presence_signal.get("presence_strength", 0.5))
        threat = self._clamp01(
            saturation * 0.32
            + contradiction * 0.22
            + fragmentation * 0.18
            + self.attention_fatigue * 0.14
            + self.global_saturation_distress * 0.10
            + (0.10 if interruption == InterruptionType.FULL_BREAK else 0.0)
            - presence * 0.10
        )
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            local_threat = self._clamp01(threat + subj.cognitive_pain * 0.16 + subj.conflict_pressure * 0.14 + subj.precision_loss * 0.10)
            target = self._clamp01(local_threat * (0.55 + subj.protective_guard * 0.25 + subj.safety_need * 0.20))
            subj.survival_closure = self._clamp01(subj.survival_closure * 0.86 + target * 0.14)
            if subj.survival_closure > 0.50:
                subj.affective_narrowing = self._clamp01(subj.affective_narrowing + subj.survival_closure * 0.025)
                subj.pull_release_need = self._clamp01(subj.pull_release_need + subj.survival_closure * 0.016)
                subj.external_coupling_readiness = self._clamp01(subj.external_coupling_readiness - subj.survival_closure * 0.010)
                if subj.state in (SubjectState.HOVERING, SubjectState.LATENT, SubjectState.RESIDUAL) and subj.protection_pressure < 0.28:
                    subj.state = SubjectState.SUSPENDED if subj.unresolved else SubjectState.BACKGROUND
            subj.clamp()
            values.append(subj.survival_closure)
        self.global_survival_closure = self._clamp01(sum(values) / max(1, len(values)))
        self.attention_bandwidth = self._clamp01(self.attention_bandwidth - self.global_survival_closure * 0.018 + presence * 0.006)
        self.global_precision = self._clamp01(self.global_precision - self.global_survival_closure * 0.012 + presence * 0.004)

    def _activate_subconscious_takeovers(
        self,
        impulse_signals: Dict[str, Any],
        memory_hints: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """Permet au subconscient de voler réellement le focus quand une trace périphérique devient trop forte."""
        unresolved_hint = float(memory_hints.get("unresolved_pressure", memory_hints.get("open_loop_pressure", 0.0)))
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state in (SubjectState.CLOSED, SubjectState.ACTIVE):
                subj.involuntary_takeover *= 0.94
                subj.clamp()
                values.append(subj.involuntary_takeover)
                continue
            takeover_seed = self._clamp01(
                subj.subconscious_override * 0.22
                + subj.intrusive_rise * 0.20
                + subj.haunting_level * 0.14
                + subj.involuntary_recall * 0.14
                + subj.unresolved_need * 0.12
                + subj.abandonment_shock * 0.08
                + subj.crystallized_bias * 0.08
                + unresolved_hint * 0.06
                + pressure * 0.03
                - subj.survival_closure * 0.10
            )
            subj.involuntary_takeover = self._clamp01(subj.involuntary_takeover * 0.88 + takeover_seed * 0.12)
            if subj.involuntary_takeover > 0.58:
                subj.state = SubjectState.REOPENING if subj.unresolved or subj.regret_trace > 0.24 else SubjectState.PULLED_BACK
                subj.return_pressure = self._clamp01(subj.return_pressure + subj.involuntary_takeover * 0.055)
                subj.half_focus_level = self._clamp01(max(subj.half_focus_level, subj.involuntary_takeover * 0.72))
            subj.clamp()
            values.append(subj.involuntary_takeover)
        self.global_involuntary_takeover = self._clamp01(sum(values) / max(1, len(values)))

    def _apply_organic_bifurcations(
        self,
        impulse_signals: Dict[str, Any],
        attractors: Dict[str, float],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """Ajoute un micro-chaos déterministe : bifurcations organiques bornées, jamais hasard pur."""
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        curiosity = float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))
        rupture = float(attractors.get("rupture", attractors.get("divergence", 0.0)))
        values: List[float] = []
        for i, (name, subj) in enumerate(self.subjects.items()):
            if subj.state == SubjectState.CLOSED:
                continue
            wave = math.sin(self.internal_clock * (0.17 + (i % 7) * 0.013) + len(name) * 0.11)
            seed = self._clamp01(
                abs(wave) * 0.08
                + subj.micro_chaos * 0.18
                + subj.turbulence * 0.16
                + subj.instability * 0.12
                + subj.irrational_pull * 0.12
                + curiosity * 0.08
                + rupture * 0.10
                + saturation * 0.06
                - presence * 0.05
                - subj.protective_guard * 0.08
            )
            subj.spontaneous_bifurcation = self._clamp01(subj.spontaneous_bifurcation * 0.84 + seed * 0.16)
            if subj.spontaneous_bifurcation > 0.48 and subj.state in (SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.LATENT):
                subj.state = SubjectState.HOVERING
                subj.half_focus_level = self._clamp01(subj.half_focus_level + subj.spontaneous_bifurcation * 0.08)
            subj.clamp()
            values.append(subj.spontaneous_bifurcation)
        self.global_spontaneous_bifurcation = self._clamp01(sum(values) / max(1, len(values)))

    def _update_expression_coupling_pressure(
        self,
        impulse_signals: Dict[str, Any],
        presence_signal: Dict[str, Any],
        interruption: InterruptionType,
    ) -> None:
        """Prépare une pression Azip/bouche lisible sans composer de mots ni de phrases."""
        pressure = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        saturation = float(impulse_signals.get("cognitive_saturation", impulse_signals.get("saturation", 0.0)))
        presence = float(presence_signal.get("presence_strength", 0.5))
        values: List[float] = []
        for subj in self.subjects.values():
            if subj.state == SubjectState.CLOSED:
                continue
            expressive = self._clamp01(
                subj.external_coupling_readiness * 0.22
                + subj.focus_self_deformation * 0.12
                + subj.respiration_cycle_pressure * 0.12
                + subj.subjective_time_distortion * 0.10
                + subj.survival_closure * 0.10
                + subj.involuntary_takeover * 0.10
                + subj.spontaneous_bifurcation * 0.08
                + subj.relational_role_pressure * 0.06
                + pressure * 0.05
                + presence * 0.05
                - saturation * 0.06
            )
            subj.expressive_pressure = self._clamp01(subj.expressive_pressure * 0.82 + expressive * 0.18)
            subj.clamp()
            values.append(subj.expressive_pressure)
        self.global_expressive_pressure = self._clamp01(sum(values) / max(1, len(values)))

    def _apply_attractor_dynamics(self, attractors: Dict[str, float], impulse_signals: Dict[str, Any]) -> None:
        attraction_force = float(attractors.get("curiosity", 0.0)) + float(attractors.get("expression", 0.0))
        protection_force = float(attractors.get("resistance", 0.0)) + float(attractors.get("challenge", 0.0))
        continuation_force = float(attractors.get("continuation", 0.0)) + float(attractors.get("expression", 0.0))
        rupture_force = float(attractors.get("divergence", 0.0)) + float(attractors.get("rupture", 0.0))

        self.inertia = self._clamp01(self.inertia + continuation_force * 0.03 - rupture_force * 0.035)

        for subj in self.subjects.values():
            if attraction_force > 0.25 and subj.unresolved:
                subj.return_pressure = self._clamp01(subj.return_pressure + attraction_force * 0.025)
                subj.decay_speed = max(0.35, subj.decay_speed - attraction_force * 0.06)
            if protection_force > 0.25 and (subj.wound_level > 0.15 or subj.hierarchy_level == HierarchyLevel.DEEP_RULES):
                subj.silent_pressure = self._clamp01(subj.silent_pressure + protection_force * 0.018)
                subj.texture.resistance = self._clamp01(subj.texture.resistance + protection_force * 0.018)
            if rupture_force > 0.25 and subj.state in (SubjectState.SECONDARY, SubjectState.RESIDUAL):
                subj.decay_speed = min(2.0, subj.decay_speed + rupture_force * 0.08)
            subj.clamp()

    # ------------------------------------------------------------------
    # Focus principal + anti-boucle organique
    # ------------------------------------------------------------------

    def _elect_primary_focus(self, impulse_signals: Dict[str, Any], interruption: InterruptionType) -> str:
        candidates: Dict[str, float] = {}
        for name, subj in self.subjects.items():
            if subj.state == SubjectState.CLOSED:
                continue
            score = 0.0
            if subj.state == SubjectState.ACTIVE:
                score = subj.gravity
            elif subj.state == SubjectState.REOPENING:
                score = subj.gravity * 0.90 + subj.return_pressure * 0.25
            elif subj.state == SubjectState.PULLED_BACK:
                score = subj.gravity * 0.82 + subj.return_pressure * 0.18
            elif subj.state in (SubjectState.HALF_ACTIVE, SubjectState.HOVERING):
                score = subj.gravity * 0.55 + subj.half_focus_level * 0.22
            elif subj.state == SubjectState.LATENT:
                score = subj.gravity * 0.34 + subj.latent_focus_pressure * 0.32 + subj.silent_pressure * 0.10
            elif subj.state in (SubjectState.RESIDUAL, SubjectState.SECONDARY):
                score = subj.residue_strength * 0.7 + subj.silent_pressure * 0.15
            elif subj.state == SubjectState.SUSPENDED:
                score = subj.gravity * 0.8 + subj.silent_pressure * 0.20
            elif subj.state == SubjectState.ALMOST_CLOSED:
                score = subj.residue_strength * 0.35 + subj.silent_pressure * 0.10
            elif subj.state == SubjectState.BACKGROUND:
                score = 0.0 if subj.hierarchy_level == HierarchyLevel.DEEP_RULES else subj.gravity * 0.2

            score += subj.recurrence_count * 0.05
            score += subj.texture.attraction * 0.05
            score += subj.return_pressure * 0.08
            score += subj.unspoken_pull * 0.05
            score += subj.emotional_gravity_bias * 0.09
            score += subj.subjective_proximity * 0.06
            score += subj.resonance_level * 0.055
            score += subj.attention_habit * 0.035
            score += subj.existential_charge * 0.055
            score += subj.self_binding * 0.030
            score += subj.obsession_fixation * 0.080
            score += subj.implicit_missing_pressure * 0.040
            score += subj.turbulence * 0.018
            score += subj.latent_focus_pressure * 0.050
            score += subj.subconscious_pressure * 0.045
            score += subj.associative_echo * 0.030
            score += subj.future_pull * 0.060
            score += subj.preconscious_charge * 0.035
            score += subj.autonomous_desire * 0.065
            score += subj.intrusive_rise * 0.050
            score += subj.lived_expectation * 0.030
            score += subj.unresolved_need * 0.040
            score += subj.regret_trace * 0.026
            score += subj.transition_blend * 0.025
            score += subj.drift_vector * 0.034
            score += subj.haunting_level * 0.045
            score += subj.affective_memory_bias * 0.052
            score += subj.involuntary_recall * 0.060
            score += subj.attention_need * 0.095
            score += subj.resolution_hunger * 0.080
            score += subj.safety_need * 0.035
            score += subj.attachment_depth * 0.070
            score += subj.sedimented_charge * 0.060
            score += subj.subconscious_override * 0.115
            score += subj.abandonment_shock * 0.045
            score += subj.attractor_mutation * 0.065
            score += subj.attention_style_mutation * 0.050
            score += subj.irrational_pull * 0.044
            score += subj.scar_perception_bias * 0.038
            score += subj.focus_self_deformation * 0.030
            score += subj.long_attention_personality * 0.058
            score += subj.respiration_cycle_pressure * self.global_respiration_release * 0.020
            score += subj.external_coupling_readiness * 0.052
            score += subj.crystallized_bias * 0.070
            score += subj.involuntary_takeover * 0.165
            score += subj.relational_role_pressure * 0.050
            score += subj.protection_pressure * 0.030
            score += subj.spontaneous_bifurcation * 0.035
            score += subj.micro_chaos * 0.012
            score -= subj.organic_fatigue * 0.055
            score -= subj.saturation_distress * 0.050
            score -= subj.conflict_pressure * subj.avoidance_pressure * 0.045
            score -= subj.recovery_need * 0.040
            score -= subj.affective_narrowing * 0.040
            score -= subj.scar_distortion * subj.avoidance_pressure * 0.045
            score -= subj.asymmetrical_delay * 0.030
            score -= subj.precision_loss * 0.035
            score -= subj.pull_release_need * 0.050
            score -= subj.directional_fatigue * 0.045
            score -= subj.instability * 0.018
            score -= subj.avoidance_pressure * 0.055
            score -= subj.cognitive_pain * 0.030
            score -= subj.void_pull * 0.014
            score -= subj.durable_double_bind * subj.avoidance_pressure * 0.040
            score -= subj.subjective_time_distortion * subj.directional_fatigue * 0.025
            score -= subj.void_deformation * subj.precision_loss * 0.026
            score -= subj.survival_closure * 0.085
            score -= subj.rivalry_pressure * subj.avoidance_pressure * 0.036

            # Bonus organique pour les sujets réellement présents dans le tour actuel.
            # Ça évite que l'ancien focus garde trop facilement le contrôle
            # quand l'utilisateur apporte une nouvelle demande ou une rupture nette.
            if name in self.current_turn_candidates:
                score += 0.24
                score += self._clamp01(1.0 - self.attention_fatigue) * 0.06
                if interruption == InterruptionType.FULL_BREAK:
                    score += 0.28

            # Les règles profondes protègent la cohérence, mais ne doivent pas
            # devenir le sujet principal sauf si le tour courant les réactive clairement.
            if subj.hierarchy_level == HierarchyLevel.DEEP_RULES:
                score *= 0.35
                if name not in self.current_turn_candidates:
                    score = min(score, 0.32)

            score -= self.attention_fatigue * 0.05 if subj.gravity < 0.5 else 0.0

            if subj.wound_level > 0.5:
                score = max(score - 0.05 + subj.silent_pressure * 0.08, 0.0)
            if score > 0.0:
                candidates[name] = score

        if not candidates:
            if self.attention_void > 0.32:
                return "attention_void"
            return "general_conversation"

        if self.last_primary and self.last_primary in candidates and interruption not in (InterruptionType.FULL_BREAK,):
            candidates[self.last_primary] += self.inertia * 0.35

        impulse_strength = float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0)))
        if impulse_strength > 0.8 and self.last_primary in candidates:
            candidates[self.last_primary] -= impulse_strength * 0.2

        elected = max(candidates, key=lambda k: candidates[k])
        override_candidates = {
            n: s.subconscious_override
            for n, s in self.subjects.items()
            if n in candidates and max(s.subconscious_override, s.involuntary_takeover) > 0.62 and n != elected
        }
        if override_candidates:
            override_name = max(override_candidates, key=lambda n: override_candidates[n])
            takeover_force = max(
                self.subjects[override_name].subconscious_override,
                self.subjects[override_name].involuntary_takeover,
            )
            if candidates.get(override_name, 0.0) >= candidates.get(elected, 0.0) * (0.82 - takeover_force * 0.16):
                elected = override_name
                self.subjects[override_name].state = SubjectState.PULLED_BACK
                self.subjects[override_name].intrusive_rise = self._clamp01(self.subjects[override_name].intrusive_rise + 0.10)

        # Petite bascule organique non optimale : elle n'est ni aléatoire ni textuelle.
        # Elle permet à une hantise / cicatrice / envie latente de gagner parfois
        # quand elle est presque aussi forte que le choix rationnel.
        irrational_candidates = {
            n: s.irrational_pull + s.haunting_level * 0.25 + s.scar_perception_bias * 0.22
            for n, s in self.subjects.items()
            if n in candidates and n != elected and s.state != SubjectState.CLOSED
        }
        if irrational_candidates and self.global_irrational_pull > 0.34:
            irrational_name = max(irrational_candidates, key=lambda n: irrational_candidates[n])
            if candidates.get(irrational_name, 0.0) >= candidates.get(elected, 0.0) * (0.86 - self.global_irrational_pull * 0.10):
                elected = irrational_name
                self.subjects[irrational_name].state = SubjectState.PULLED_BACK
                self.subjects[irrational_name].intrusive_rise = self._clamp01(self.subjects[irrational_name].intrusive_rise + 0.06)
        if self.attention_void > 0.58 and candidates.get(elected, 0.0) < 0.42:
            return "attention_void"
        if elected in self.subjects:
            self.subjects[elected].state = SubjectState.ACTIVE
            self.subjects[elected].half_focus_level = 1.0
            self.subjects[elected].last_state_change = datetime.now()
        return elected

    def _apply_anti_loop(self, primary: str, impulse_signals: Dict[str, Any]) -> str:
        if primary == self.last_primary:
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0

        if self.stagnation_counter < self.LOOP_STAGNATION_LIMIT:
            return primary

        # Anti-boucle progressif : affaiblir, faire monter un angle secondaire, puis seulement basculer.
        current = self.subjects.get(primary)
        if current:
            current.gravity = self._clamp01(current.gravity - 0.08)
            current.residue_strength = self._clamp01(current.residue_strength - 0.05)
            current.texture.attraction = self._clamp01(current.texture.attraction - 0.04)
            current.half_focus_level = self._clamp01(current.half_focus_level - 0.10)
            current.silent_pressure = self._clamp01(current.silent_pressure + 0.04)
            current.pull_release_need = self._clamp01(current.pull_release_need + 0.12)
            current.precision_loss = self._clamp01(current.precision_loss + 0.06)

        secondary_candidates = [
            name for name, s in self.subjects.items()
            if s.state in (SubjectState.ACTIVE, SubjectState.RESIDUAL, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.SUSPENDED, SubjectState.LATENT)
            and name != primary
            and (s.gravity + s.return_pressure + s.silent_pressure) > 0.2
        ]

        if not secondary_candidates:
            self.inertia = max(self.inertia - 0.3, 0.0)
            self.stagnation_counter = 0
            return primary

        alt = max(secondary_candidates, key=lambda n: self.subjects[n].gravity + self.subjects[n].return_pressure + self.subjects[n].silent_pressure)
        alt_subj = self.subjects[alt]
        alt_subj.state = SubjectState.HALF_ACTIVE if alt_subj.state != SubjectState.SUSPENDED else SubjectState.PULLED_BACK
        alt_subj.half_focus_level = self._clamp01(alt_subj.half_focus_level + 0.35)
        alt_subj.gravity = self._clamp01(alt_subj.gravity + 0.05)

        # Bascule seulement si la stagnation devient nette ou si la fatigue monte.
        if self.stagnation_counter >= self.LOOP_STAGNATION_LIMIT + 1 or self.attention_fatigue > 0.58:
            self.stagnation_counter = 0
            return alt

        self.stagnation_counter = max(0, self.stagnation_counter - 1)
        return primary

    def _update_half_focus(self, primary: str, impulse_signals: Dict[str, Any]) -> None:
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        for name, subj in self.subjects.items():
            if name == primary:
                subj.half_focus_level = 1.0
                continue
            if subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.PULLED_BACK, SubjectState.REOPENING):
                pull = subj.gravity * 0.10 + subj.silent_pressure * 0.12 + fragmentation * 0.08 + subj.return_pressure * 0.10 + subj.subconscious_pressure * 0.06 + subj.future_pull * 0.05
                subj.half_focus_level = self._clamp01(subj.half_focus_level * 0.84 + pull)
                if 0.30 < subj.half_focus_level < 0.62 and subj.state not in (SubjectState.SUSPENDED, SubjectState.REOPENING):
                    subj.state = SubjectState.HOVERING
                elif subj.half_focus_level >= 0.62 and subj.state not in (SubjectState.SUSPENDED, SubjectState.REOPENING):
                    subj.state = SubjectState.HALF_ACTIVE
            else:
                subj.half_focus_level *= 0.88
            subj.clamp()

    # ------------------------------------------------------------------
    # Focus secondaires et arrière-plan
    # ------------------------------------------------------------------

    def _elect_secondary_and_background(self, primary: str) -> Tuple[List[str], List[str]]:
        secondary: List[Tuple[str, float]] = []
        background: List[Tuple[str, float]] = []

        for name, subj in self.subjects.items():
            if name == primary or subj.state == SubjectState.CLOSED:
                continue
            if subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.PULLED_BACK, SubjectState.REOPENING):
                effective = subj.gravity + subj.half_focus_level * 0.15 + subj.silent_pressure * 0.08
                secondary.append((name, effective))
            elif subj.state in (SubjectState.RESIDUAL, SubjectState.SUSPENDED, SubjectState.ALMOST_CLOSED):
                effective = subj.residue_strength + subj.silent_pressure * 0.12 + subj.return_pressure * 0.10
                if effective > 0.1:
                    secondary.append((name, effective))
                else:
                    background.append((name, subj.gravity * 0.3))
            elif subj.state == SubjectState.BACKGROUND:
                if subj.hierarchy_level == HierarchyLevel.DEEP_RULES:
                    background.append((name, subj.gravity + subj.silent_pressure * 0.10))
                elif subj.gravity > 0.3:
                    background.append((name, subj.gravity))

        secondary.sort(key=lambda x: x[1], reverse=True)
        background.sort(key=lambda x: x[1], reverse=True)

        for name, _ in secondary[:4]:
            if self.subjects[name].state not in (SubjectState.SUSPENDED, SubjectState.REOPENING, SubjectState.PULLED_BACK):
                self.subjects[name].state = SubjectState.SECONDARY

        return ([name for name, _ in secondary[:4]], [name for name, _ in background[:5]])

    # ------------------------------------------------------------------
    # Champ global, métriques, trajectoires
    # ------------------------------------------------------------------

    def _update_field_tension(self, primary: str, secondary: List[str], impulse_signals: Dict[str, Any], interruption: InterruptionType) -> None:
        primary_subj = self.subjects.get(primary)
        primary_g = primary_subj.gravity if primary_subj else 0.0
        secondary_g = max([self.subjects[s].gravity for s in secondary if s in self.subjects] or [0.0])
        self.field.primary_secondary_tension = self._clamp01(max(0.0, secondary_g - primary_g + 0.25) if secondary else 0.0)

        deep_pressure = 0.0
        for rule in self.deep_rules:
            s = self.subjects.get(rule)
            if s:
                deep_pressure += s.silent_pressure + s.wound_level * 0.4 + sum(s.contamination.values()) * 0.04
        self.field.deep_rule_tension = self._clamp01(deep_pressure / max(len(self.deep_rules), 1))

        rupture = 1.0 if interruption == InterruptionType.FULL_BREAK else 0.0
        continuation = float(impulse_signals.get("continuation_inertia", 0.0))
        self.field.continuity_break_tension = self._clamp01(abs(continuation - rupture) * 0.75)

        saturation = float(impulse_signals.get("cognitive_saturation", 0.0))
        fragmentation = float(impulse_signals.get("fragmentation", 0.0))
        self.field.overload_clarity_tension = self._clamp01(saturation * 0.45 + fragmentation * 0.35 + self.attention_fatigue * 0.30)
        self.field.void_tension = self._clamp01(self.attention_void * 0.70 + self.unspoken_global_pressure * 0.22)
        self.field.existential_tension = self._clamp01(max([s.existential_charge * (s.implicit_missing_pressure + s.wound_level + s.silent_pressure) for s in self.subjects.values()] or [0.0]))
        self.field.pain_tension = self._clamp01(max([s.cognitive_pain for s in self.subjects.values()] or [0.0]))
        self.field.turbulence_tension = self._clamp01(self.turbulence_memory * 0.55 + max([s.turbulence for s in self.subjects.values()] or [0.0]) * 0.45)
        self.field.latent_tension = self._clamp01(max([s.latent_focus_pressure for s in self.subjects.values()] or [0.0]) * 0.55 + self.global_subconscious_pressure * 0.20)
        self.field.precision_tension = self._clamp01(1.0 - self.global_precision)
        self.field.subconscious_tension = self._clamp01(self.global_subconscious_pressure * 0.65 + max([s.subconscious_pressure for s in self.subjects.values()] or [0.0]) * 0.35)
        self.field.anticipatory_tension = self._clamp01(self.anticipatory_pressure)
        self.field.transition_blend_tension = self._clamp01(self.transition_blend_level)
        self.field.micro_instability_tension = self._clamp01(self.global_micro_instability)
        self.field.fragmentation_presence_tension = self._clamp01(self.global_fragmented_presence)
        self.field.protective_guard_tension = self._clamp01(self.global_protective_guard)
        self.field.temporal_drag_tension = self._clamp01(self.global_temporal_drag)
        self.field.relational_tension = self._clamp01(self.global_relational_pull)
        self.field.autonomous_drift_tension = self._clamp01(self.global_autonomous_drift)
        self.field.preconscious_tension = self._clamp01(self.global_preconscious_charge)
        self.field.cognitive_weather_tension = self._clamp01(
            self.cognitive_weather.get("heaviness", 0.0) * 0.35
            + self.cognitive_weather.get("nervousness", 0.0) * 0.30
            + self.cognitive_weather.get("fragility", 0.0) * 0.20
            + (1.0 - self.cognitive_weather.get("clarity", 1.0)) * 0.15
        )
        self.field.autonomous_desire_tension = self._clamp01(self.global_autonomous_desire)
        self.field.subconscious_intrusion_tension = self._clamp01(self.global_subconscious_intrusion)
        self.field.scar_distortion_tension = self._clamp01(self.global_scar_distortion)
        self.field.lived_temporality_tension = self._clamp01(self.global_lived_temporality)
        self.field.attention_need_tension = self._clamp01(self.global_attention_need)
        self.field.organic_conflict_tension = self._clamp01(self.global_organic_conflict)
        self.field.sedimentation_tension = self._clamp01(self.global_sedimented_attention)
        self.field.subconscious_override_tension = self._clamp01(self.global_subconscious_override)
        self.field.saturation_distress_tension = self._clamp01(self.global_saturation_distress)

    def _compute_fragmentation(self, impulse_signals: Dict[str, Any], message_metadata: Dict[str, Any]) -> float:
        base = float(impulse_signals.get("fragmentation", 0.0))
        if message_metadata.get("multi_demand", False):
            base += 0.3
        if message_metadata.get("contradiction", False):
            base += 0.2
        active_count = sum(1 for s in self.subjects.values() if s.state in (SubjectState.ACTIVE, SubjectState.HALF_ACTIVE, SubjectState.HOVERING, SubjectState.REOPENING, SubjectState.PULLED_BACK))
        if active_count > 3:
            base += (active_count - 3) * 0.1
        return self._clamp01(base)

    def _compute_inertia(self, primary: str, interruption: InterruptionType, impulse_signals: Dict[str, Any]) -> float:
        if interruption == InterruptionType.FULL_BREAK:
            return max(self.inertia - self.INERTIA_DECAY * 2, 0.0)
        if interruption == InterruptionType.SHORT_CONTINUE:
            return min(self.inertia + 0.15, 1.0)
        if interruption == InterruptionType.CORRECTION:
            return max(self.inertia - self.INERTIA_DECAY, 0.0)
        continuation = float(impulse_signals.get("continuation_inertia", 0.0))
        new_inertia = self.inertia * 0.8 + continuation * 0.2
        if primary == self.last_primary:
            new_inertia = min(new_inertia + 0.1, 1.0)
        new_inertia -= self.attention_fatigue * 0.035
        return self._clamp01(new_inertia)

    def _compute_stability(self, primary: str, impulse_signals: Dict[str, Any], presence_signal: Dict[str, Any]) -> float:
        base = 1.0 - float(impulse_signals.get("cognitive_saturation", 0.0))
        if impulse_signals.get("fragmentation", 0.0) > 0.5:
            base -= 0.2
        presence = float(presence_signal.get("presence_strength", 0.5))
        subj = self.subjects.get(primary)
        texture_penalty = subj.texture.charge() * 0.14 if subj else 0.0
        pain_penalty = subj.cognitive_pain * 0.10 + subj.turbulence * 0.06 + self.attention_void * 0.05 if subj else self.attention_void * 0.05
        weather_penalty = (
            self.cognitive_weather.get("heaviness", 0.0) * 0.06
            + self.cognitive_weather.get("nervousness", 0.0) * 0.05
            + self.global_preconscious_charge * 0.04
            + self.global_subconscious_intrusion * 0.04
            + self.global_scar_distortion * 0.04
            + self.global_organic_conflict * 0.05
            + self.global_subconscious_override * 0.035
            + self.global_saturation_distress * 0.05
        )
        weather_support = self.cognitive_weather.get("clarity", 1.0) * 0.05 + self.cognitive_weather.get("openness", 0.5) * 0.03
        base = base * 0.6 + presence * 0.4 - self.attention_fatigue * 0.12 - texture_penalty - pain_penalty - weather_penalty + weather_support
        return self._clamp01(base)

    def _compute_continuity(self, primary: str) -> float:
        if len(self.focus_history) < 2:
            return 0.5
        recent = self.focus_history[-min(4, len(self.focus_history)):]
        matches = sum(1 for p in recent if p == primary)
        return matches / len(recent)

    def _compute_attention_tension(self, impulse_signals: Dict[str, Any], fragmentation: float) -> float:
        tension = (
            float(impulse_signals.get("contradiction_tension", 0.0)) * 0.32
            + float(impulse_signals.get("pressure", impulse_signals.get("response_pressure", 0.0))) * 0.22
            + fragmentation * 0.24
            + self.field.total() * 0.22
            + self.attention_void * 0.08
            + self.turbulence_memory * 0.06
            + (1.0 - self.global_precision) * 0.08
            + self.global_subconscious_pressure * 0.07
            + self.anticipatory_pressure * 0.05
            + self.transition_blend_level * 0.04
            + self.global_preconscious_charge * 0.05
            + self.global_autonomous_desire * 0.04
            + self.global_subconscious_intrusion * 0.05
            + self.global_scar_distortion * 0.04
            + self.global_lived_temporality * 0.04
            + self.global_attention_need * 0.06
            + self.global_organic_conflict * 0.06
            + self.global_subconscious_override * 0.05
            + self.global_saturation_distress * 0.05
            + self.global_sedimented_attention * 0.035
            + self.cognitive_weather.get("nervousness", 0.0) * 0.04
            + self.global_attention_style_mutation * 0.045
            + self.global_active_void_deformation * 0.040
            + self.global_irrational_pull * 0.035
            + self.global_scar_perception_bias * 0.040
        )
        return self._clamp01(tension)

    def _compute_shift(self, primary: str) -> float:
        if len(self.focus_history) < 1:
            return 0.5
        last = self.focus_history[-1] if self.focus_history else None
        if last is None or last == primary:
            return 0.0
        last_g = self.subjects.get(last, AttentionSubject(last, 0.3, SubjectState.BACKGROUND, HierarchyLevel.IMMEDIATE_MESSAGE)).gravity
        current_g = self.subjects.get(primary, AttentionSubject(primary, 0.3, SubjectState.BACKGROUND, HierarchyLevel.IMMEDIATE_MESSAGE)).gravity
        return self._clamp01(abs(current_g - last_g) + 0.3)

        self.field.crystallized_bias_tension = self.global_crystallized_bias
        self.field.survival_closure_tension = self.global_survival_closure
        self.field.involuntary_takeover_tension = self.global_involuntary_takeover
        self.field.relational_ecology_tension = self.global_relational_ecology
        self.field.spontaneous_bifurcation_tension = self.global_spontaneous_bifurcation
        self.field.expressive_pressure_tension = self.global_expressive_pressure

    def _evolve_focus_trajectory(self, primary: str, secondary: List[str], impulse_signals: Dict[str, Any], attractors: Dict[str, float]) -> None:
        subj = self.subjects.get(primary)
        if not subj:
            return

        candidate_step: Optional[str] = None
        if float(impulse_signals.get("clarification_need", 0.0)) > 0.55:
            candidate_step = "clarification"
        elif float(impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0))) > 0.55:
            candidate_step = "exploration"
        elif float(attractors.get("continuation", 0.0)) + float(impulse_signals.get("continuation_inertia", 0.0)) > 0.65:
            candidate_step = "continuation"
        elif self.field.deep_rule_tension > 0.35:
            candidate_step = "coherence_guard"
        elif self.attention_void > 0.50:
            candidate_step = "void_drift"
        elif self.turbulence_memory > 0.48:
            candidate_step = "bifurcation"
        elif self.attention_fatigue > 0.55:
            candidate_step = "simplification"
        elif self.anticipatory_pressure > 0.42:
            future = max(self.subjects.items(), key=lambda item: item[1].future_pull if item[1].state != SubjectState.CLOSED else -1.0)[0]
            candidate_step = f"preparing:{future}"
        elif secondary:
            candidate_step = f"toward:{secondary[0]}"

        if candidate_step and (not subj.trajectory or subj.trajectory[-1] != candidate_step):
            subj.trajectory.append(candidate_step)
            subj.trajectory = subj.trajectory[-12:]

    def _predict_direction(self, primary: str, secondary: List[str], impulse_signals: Dict[str, Any], attractors: Dict[str, float]) -> Optional[str]:
        subj = self.subjects.get(primary)
        if subj and subj.trajectory:
            return subj.trajectory[-1]
        if self.attention_void > 0.55:
            return "void_drift"
        future = [(name, s.future_pull) for name, s in self.subjects.items() if s.state != SubjectState.CLOSED and s.future_pull > 0.34 and name != primary]
        if future:
            return max(future, key=lambda item: item[1])[0]
        if impulse_signals.get("curiosity", impulse_signals.get("curiosity_pressure", 0.0)) > 0.6 and secondary:
            return secondary[0]
        if impulse_signals.get("clarification_need", 0.0) > 0.5:
            unresolved = [name for name, s in self.subjects.items() if s.unresolved and name != primary]
            if unresolved:
                return unresolved[0]
        if secondary:
            return secondary[0]
        return None

    def _compute_offtrack_risk(self, primary: str, impulse_signals: Dict[str, Any]) -> float:
        risk = float(impulse_signals.get("fragmentation", 0.0)) * 0.35 + self.field.total() * 0.20
        if self.stagnation_counter > 2:
            risk += 0.2
        subj = self.subjects.get(primary)
        if subj and subj.wound_level > 0.4:
            risk += 0.1
        if self.attention_fatigue > 0.6:
            risk += 0.12
        risk += self.attention_void * 0.08 + self.turbulence_memory * 0.06
        return self._clamp01(risk)

    def _compute_forgetting_risk(self) -> float:
        suspended_count = sum(1 for s in self.subjects.values() if s.state == SubjectState.SUSPENDED)
        unresolved_count = sum(1 for s in self.subjects.values() if s.unresolved and s.state != SubjectState.ACTIVE)
        silent_count = sum(1 for s in self.subjects.values() if s.silent_pressure > 0.35 and s.state not in (SubjectState.ACTIVE, SubjectState.SECONDARY))
        implicit_count = sum(1 for s in self.subjects.values() if s.implicit_missing_pressure > 0.25 and s.state not in (SubjectState.ACTIVE, SubjectState.SECONDARY))
        risk = (suspended_count * 0.15) + (unresolved_count * 0.1) + (silent_count * 0.07) + (implicit_count * 0.06) + self.attention_fatigue * 0.10 + self.attention_void * 0.07 + (1.0 - self.global_precision) * 0.05
        return self._clamp01(risk)

    def _get_focus_trajectory(self, primary: str) -> List[str]:
        subj = self.subjects.get(primary)
        if subj:
            return subj.trajectory[-5:] if subj.trajectory else [primary]
        return [primary]

    # ------------------------------------------------------------------
    # Exports enrichis
    # ------------------------------------------------------------------

    def _export_silent_pressure(self) -> Dict[str, float]:
        return {name: s.silent_pressure for name, s in self.subjects.items() if s.silent_pressure > 0.05}

    def _dominant_texture(self, primary: str) -> Dict[str, float]:
        subj = self.subjects.get(primary)
        return subj.texture.as_dict() if subj else AttentionTexture().as_dict()

    def _contaminated_rules(self) -> List[str]:
        active: Set[str] = set()
        for subj in self.subjects.values():
            for rule, value in subj.contamination.items():
                if rule in self.deep_rules and value > 0.08:
                    active.add(rule)
        return sorted(active)

    def _returning_subjects(self) -> List[str]:
        return [name for name, s in self.subjects.items() if s.return_pressure > 0.20 or s.state in (SubjectState.PULLED_BACK, SubjectState.REOPENING)]

    def _almost_forgotten_subjects(self) -> List[str]:
        return [
            name for name, s in self.subjects.items()
            if s.state in (SubjectState.SUSPENDED, SubjectState.RESIDUAL, SubjectState.HOVERING)
            and (s.unresolved or s.silent_pressure > 0.18)
            and s.gravity < 0.45
        ]

    def _export_half_focus(self) -> Dict[str, float]:
        return {name: s.half_focus_level for name, s in self.subjects.items() if s.half_focus_level > 0.10}


    def _export_emotional_gravity(self) -> Dict[str, float]:
        return {name: s.emotional_gravity_bias for name, s in self.subjects.items() if s.emotional_gravity_bias > 0.04}

    def _export_resonance_map(self) -> Dict[str, float]:
        return {name: s.resonance_level for name, s in self.subjects.items() if s.resonance_level > 0.04}

    def _export_directional_fatigue(self) -> Dict[str, float]:
        return {name: s.directional_fatigue for name, s in self.subjects.items() if s.directional_fatigue > 0.04}

    def _export_attention_habits(self) -> Dict[str, float]:
        return {f"{src}->{dst}": value for (src, dst), value in self.attention_habits.items() if value > 0.04}

    def _export_instability_map(self) -> Dict[str, float]:
        return {name: s.instability for name, s in self.subjects.items() if s.instability > 0.04}

    def _export_subjective_proximity(self) -> Dict[str, float]:
        return {name: s.subjective_proximity for name, s in self.subjects.items() if s.subjective_proximity > 0.04}

    def _export_existential_charge(self) -> Dict[str, float]:
        return {name: s.existential_charge for name, s in self.subjects.items() if s.existential_charge > 0.04}

    def _export_obsession_map(self) -> Dict[str, float]:
        return {name: s.obsession_fixation for name, s in self.subjects.items() if s.obsession_fixation > 0.04}

    def _export_avoidance_map(self) -> Dict[str, float]:
        return {name: s.avoidance_pressure for name, s in self.subjects.items() if s.avoidance_pressure > 0.04}

    def _export_cognitive_pain_map(self) -> Dict[str, float]:
        return {name: s.cognitive_pain for name, s in self.subjects.items() if s.cognitive_pain > 0.04}

    def _export_void_map(self) -> Dict[str, float]:
        return {name: s.void_pull for name, s in self.subjects.items() if s.void_pull > 0.04}

    def _export_implicit_missing_map(self) -> Dict[str, float]:
        return {name: s.implicit_missing_pressure for name, s in self.subjects.items() if s.implicit_missing_pressure > 0.04}

    def _export_turbulence_map(self) -> Dict[str, float]:
        return {name: s.turbulence for name, s in self.subjects.items() if s.turbulence > 0.04}


    def _export_latent_focus_map(self) -> Dict[str, float]:
        return {name: s.latent_focus_pressure for name, s in self.subjects.items() if s.latent_focus_pressure > 0.04}

    def _export_precision_loss_map(self) -> Dict[str, float]:
        return {name: s.precision_loss for name, s in self.subjects.items() if s.precision_loss > 0.04}

    def _export_saturation_memory_map(self) -> Dict[str, float]:
        return {name: s.saturation_memory for name, s in self.subjects.items() if s.saturation_memory > 0.04}

    def _export_pull_release_map(self) -> Dict[str, float]:
        return {name: s.pull_release_need for name, s in self.subjects.items() if s.pull_release_need > 0.04}

    def _export_subconscious_field(self) -> Dict[str, float]:
        return {name: s.subconscious_pressure for name, s in self.subjects.items() if s.subconscious_pressure > 0.04}

    def _export_associative_echo_map(self) -> Dict[str, float]:
        return {name: s.associative_echo for name, s in self.subjects.items() if s.associative_echo > 0.04}

    def _export_future_attractor_map(self) -> Dict[str, float]:
        return {name: s.future_pull for name, s in self.subjects.items() if s.future_pull > 0.04}

    def _export_transition_blend_map(self) -> Dict[str, float]:
        return {name: s.transition_blend for name, s in self.subjects.items() if s.transition_blend > 0.04}

    def _export_affective_narrowing_map(self) -> Dict[str, float]:
        return {name: s.affective_narrowing for name, s in self.subjects.items() if s.affective_narrowing > 0.04}

    # ------------------------------------------------------------------
    # Diagnostic interne
    # ------------------------------------------------------------------


    def _export_micro_instability_map(self) -> Dict[str, float]:
        return {n: s.micro_instability for n, s in self.subjects.items() if s.micro_instability > 0.03}

    def _export_fragmented_presence_map(self) -> Dict[str, float]:
        return {n: s.fragmented_presence for n, s in self.subjects.items() if s.fragmented_presence > 0.03}

    def _export_protective_guard_map(self) -> Dict[str, float]:
        return {n: s.protective_guard for n, s in self.subjects.items() if s.protective_guard > 0.03}

    def _export_temporal_drag_map(self) -> Dict[str, float]:
        return {n: s.temporal_drag for n, s in self.subjects.items() if s.temporal_drag > 0.03}

    def _export_relational_pull_map(self) -> Dict[str, float]:
        return {n: s.relational_pull for n, s in self.subjects.items() if s.relational_pull > 0.03}

    def _export_autonomous_drift_map(self) -> Dict[str, float]:
        return {n: s.autonomous_drift for n, s in self.subjects.items() if s.autonomous_drift > 0.03}

    def _export_scar_sensitivity_map(self) -> Dict[str, float]:
        return {n: s.scar_sensitivity for n, s in self.subjects.items() if s.scar_sensitivity > 0.03}

    def _export_preconscious_field(self) -> Dict[str, float]:
        return {n: s.preconscious_charge for n, s in self.subjects.items() if s.preconscious_charge > 0.03}

    def _export_autonomous_desire_map(self) -> Dict[str, float]:
        return {n: s.autonomous_desire for n, s in self.subjects.items() if s.autonomous_desire > 0.03}

    def _export_subconscious_intrusion_map(self) -> Dict[str, float]:
        return {n: s.intrusive_rise for n, s in self.subjects.items() if s.intrusive_rise > 0.03}

    def _export_scar_distortion_map(self) -> Dict[str, float]:
        return {n: s.scar_distortion for n, s in self.subjects.items() if s.scar_distortion > 0.03}

    def _export_lived_temporality_map(self) -> Dict[str, float]:
        data: Dict[str, float] = {}
        for n, s in self.subjects.items():
            value = self._clamp01(s.lived_expectation * 0.30 + s.unresolved_need * 0.28 + s.regret_trace * 0.22 + s.asymmetrical_delay * 0.20)
            if value > 0.03:
                data[n] = value
        return data

    def _export_attention_need_map(self) -> Dict[str, float]:
        return {n: s.attention_need for n, s in self.subjects.items() if s.attention_need > 0.03}

    def _export_organic_conflict_map(self) -> Dict[str, float]:
        return {n: s.conflict_pressure for n, s in self.subjects.items() if s.conflict_pressure > 0.03}

    def _export_sedimented_attention_map(self) -> Dict[str, float]:
        return {n: self._clamp01(s.sedimented_charge * 0.55 + s.attachment_depth * 0.45) for n, s in self.subjects.items() if (s.sedimented_charge * 0.55 + s.attachment_depth * 0.45) > 0.03}

    def _export_subconscious_override_map(self) -> Dict[str, float]:
        return {n: s.subconscious_override for n, s in self.subjects.items() if s.subconscious_override > 0.03}

    def _export_saturation_distress_map(self) -> Dict[str, float]:
        return {n: s.saturation_distress for n, s in self.subjects.items() if s.saturation_distress > 0.03}

    def _export_somatic_rhythm_map(self) -> Dict[str, float]:
        return {n: s.somatic_rhythm for n, s in self.subjects.items() if s.somatic_rhythm > 0.03}

    def _export_scar_gravity_bias_map(self) -> Dict[str, float]:
        return {n: s.scar_gravity_bias for n, s in self.subjects.items() if s.scar_gravity_bias > 0.03}

    def _export_autonomous_resurgence_map(self) -> Dict[str, float]:
        return {n: s.autonomous_resurgence for n, s in self.subjects.items() if s.autonomous_resurgence > 0.03}

    def _export_lived_time_warp_map(self) -> Dict[str, float]:
        return {n: s.lived_time_warp for n, s in self.subjects.items() if s.lived_time_warp > 0.03}

    def _export_focus_viscosity_map(self) -> Dict[str, float]:
        return {n: s.focus_viscosity for n, s in self.subjects.items() if s.focus_viscosity > 0.03}

    def _export_organic_respiration(self) -> Dict[str, float]:
        return {
            "contraction": self.global_respiration_contraction,
            "release": self.global_respiration_release,
            "focus_viscosity": self.global_focus_viscosity,
            "scar_gravity_bias": self.global_scar_gravity_bias,
            "autonomous_resurgence": self.global_autonomous_resurgence,
            "lived_time_warp": self.global_lived_time_warp,
        }

    def _export_attention_style_mutation_map(self) -> Dict[str, float]:
        return {n: s.attention_style_mutation for n, s in self.subjects.items() if s.attention_style_mutation > 0.05}

    def _export_void_deformation_map(self) -> Dict[str, float]:
        return {n: s.void_deformation for n, s in self.subjects.items() if s.void_deformation > 0.05}

    def _export_irrational_pull_map(self) -> Dict[str, float]:
        return {n: s.irrational_pull for n, s in self.subjects.items() if s.irrational_pull > 0.05}

    def _export_scar_perception_bias_map(self) -> Dict[str, float]:
        return {n: s.scar_perception_bias for n, s in self.subjects.items() if s.scar_perception_bias > 0.05}

    def _export_focus_self_deformation_map(self) -> Dict[str, float]:
        return {n: s.focus_self_deformation for n, s in self.subjects.items() if s.focus_self_deformation > 0.01}

    def _export_attention_personality_map(self) -> Dict[str, float]:
        return {n: s.long_attention_personality for n, s in self.subjects.items() if s.long_attention_personality > 0.01}

    def _export_respiration_cycle_map(self) -> Dict[str, float]:
        return {n: s.respiration_cycle_pressure for n, s in self.subjects.items() if s.respiration_cycle_pressure > 0.01}

    def _export_durable_double_bind_map(self) -> Dict[str, float]:
        return {n: s.durable_double_bind for n, s in self.subjects.items() if s.durable_double_bind > 0.01}

    def _export_subjective_time_distortion_map(self) -> Dict[str, float]:
        return {n: s.subjective_time_distortion for n, s in self.subjects.items() if s.subjective_time_distortion > 0.01}

    def _export_azip_coupling_map(self) -> Dict[str, float]:
        return {n: s.external_coupling_readiness for n, s in self.subjects.items() if s.external_coupling_readiness > 0.01}

    def _export_global_living_attention(self) -> Dict[str, float]:
        return {
            "micro_instability": self.global_micro_instability,
            "fragmented_presence": self.global_fragmented_presence,
            "protective_guard": self.global_protective_guard,
            "temporal_drag": self.global_temporal_drag,
            "relational_pull": self.global_relational_pull,
            "autonomous_drift": self.global_autonomous_drift,
            "subconscious_pressure": self.global_subconscious_pressure,
            "anticipatory_pressure": self.anticipatory_pressure,
            "transition_blend": self.transition_blend_level,
            "bandwidth": self.attention_bandwidth,
            "preconscious_charge": self.global_preconscious_charge,
            "autonomous_desire": self.global_autonomous_desire,
            "subconscious_intrusion": self.global_subconscious_intrusion,
            "scar_distortion": self.global_scar_distortion,
            "lived_temporality": self.global_lived_temporality,
            "drift_field": self.global_drift_field,
            "residual_haunting": self.global_residual_haunting,
            "affective_focus_memory": self.global_affective_focus_memory,
            "controlled_micro_chaos": self.global_controlled_micro_chaos,
            "involuntary_recall": self.global_involuntary_recall,
            "recovery_need": self.global_recovery_need,
            "attention_need": self.global_attention_need,
            "organic_conflict": self.global_organic_conflict,
            "sedimented_attention": self.global_sedimented_attention,
            "subconscious_override": self.global_subconscious_override,
            "saturation_distress": self.global_saturation_distress,
            "respiration_contraction": self.global_respiration_contraction,
            "respiration_release": self.global_respiration_release,
            "focus_viscosity": self.global_focus_viscosity,
            "scar_gravity_bias": self.global_scar_gravity_bias,
            "autonomous_resurgence": self.global_autonomous_resurgence,
            "lived_time_warp": self.global_lived_time_warp,
            "attention_style_mutation": self.global_attention_style_mutation,
            "active_void_deformation": self.global_active_void_deformation,
            "irrational_pull": self.global_irrational_pull,
            "scar_perception_bias": self.global_scar_perception_bias,
            "focus_self_deformation": self.global_focus_self_deformation,
            "attention_personality": self.global_attention_personality,
            "respiration_cycle_pressure": self.global_respiration_cycle_pressure,
            "durable_double_bind": self.global_durable_double_bind,
            "subjective_time_distortion": self.global_subjective_time_distortion,
            "azip_coupling_readiness": self.global_azip_coupling_readiness,
            "weather_heaviness": self.cognitive_weather.get("heaviness", 0.0),
            "weather_nervousness": self.cognitive_weather.get("nervousness", 0.0),
            "weather_openness": self.cognitive_weather.get("openness", 0.5),
            "weather_expectancy": self.cognitive_weather.get("expectancy", 0.0),
            "weather_fragility": self.cognitive_weather.get("fragility", 0.0),
            "weather_clarity": self.cognitive_weather.get("clarity", 1.0),
        }

    def _build_diagnostic(self, primary: str, secondary: List[str], tension: float, forgetting_risk: float, unresolved: List[str], interruption: InterruptionType) -> AttentionDiagnostic:
        subj = self.subjects.get(primary)
        dominant_reason = (
            f"gravity={subj.gravity:.2f} state={subj.state.value} activations={subj.activation_count} "
            f"wound={subj.wound_level:.2f} silent={subj.silent_pressure:.2f} texture={subj.texture.charge():.2f} "
            f"existential={subj.existential_charge:.2f} obsession={subj.obsession_fixation:.2f} latent={subj.latent_focus_pressure:.2f} subconscious={subj.subconscious_pressure:.2f} future={subj.future_pull:.2f} desire={subj.autonomous_desire:.2f} preconscious={subj.preconscious_charge:.2f} intrusion={subj.intrusive_rise:.2f} scar_distortion={subj.scar_distortion:.2f} attention_need={subj.attention_need:.2f} conflict={subj.conflict_pressure:.2f} sediment={subj.sedimented_charge:.2f} override={subj.subconscious_override:.2f} precision_loss={subj.precision_loss:.2f} self_deform={subj.focus_self_deformation:.2f} personality={subj.long_attention_personality:.2f} double_bind={subj.durable_double_bind:.2f} time_distortion={subj.subjective_time_distortion:.2f} azip_coupling={subj.external_coupling_readiness:.2f} void={self.attention_void:.2f}"
        ) if subj else "unknown"

        secondary_reasons: Dict[str, str] = {}
        for name in secondary:
            s = self.subjects.get(name)
            if s:
                secondary_reasons[name] = f"gravity={s.gravity:.2f} state={s.state.value} silent={s.silent_pressure:.2f} half={s.half_focus_level:.2f} obsession={s.obsession_fixation:.2f} pain={s.cognitive_pain:.2f} personality={s.long_attention_personality:.2f} double_bind={s.durable_double_bind:.2f} coupling={s.external_coupling_readiness:.2f}"

        tensions: List[str] = []
        if tension > 0.5:
            tensions.append(f"attention_tension={tension:.2f}")
        if self.field.total() > 0.35:
            tensions.append(f"field_tension={self.field.total():.2f}")
        if self.attention_fatigue > 0.4:
            tensions.append(f"attention_fatigue={self.attention_fatigue:.2f}")
        if self.attention_void > 0.35:
            tensions.append(f"attention_void={self.attention_void:.2f}")
        if self.turbulence_memory > 0.35:
            tensions.append(f"turbulence={self.turbulence_memory:.2f}")
        if self.global_precision < 0.72:
            tensions.append(f"global_precision={self.global_precision:.2f}")
        for name, s in self.subjects.items():
            if s.wound_level > 0.3:
                tensions.append(f"wound:{name}={s.wound_level:.2f}")
            if s.unresolved and s.state == SubjectState.SUSPENDED:
                tensions.append(f"open_loop_suspended:{name}")
            if s.silent_pressure > 0.35:
                tensions.append(f"silent_pressure:{name}={s.silent_pressure:.2f}")

        forgetting_subjects = [name for name, s in self.subjects.items() if s.state == SubjectState.SUSPENDED and s.unresolved]
        recurrent = [name for name, s in self.subjects.items() if s.recurrence_count > 1]
        silent_subjects = [name for name, s in self.subjects.items() if s.silent_pressure > 0.22]

        return AttentionDiagnostic(
            dominant_reason=dominant_reason,
            secondary_reasons=secondary_reasons,
            existing_tensions=tensions,
            forgetting_risk_subjects=forgetting_subjects,
            recurrent_subjects=recurrent,
            open_loops=unresolved,
            last_interruption=interruption,
            field_tension=self.field.as_dict(),
            silent_subjects=silent_subjects,
            fatigue_reason=self.last_fatigue_reason,
        )


    def _export_crystallized_bias_map(self) -> Dict[str, float]:
        return {n: s.crystallized_bias for n, s in self.subjects.items() if s.crystallized_bias > 0.03}

    def _export_survival_closure_map(self) -> Dict[str, float]:
        return {n: s.survival_closure for n, s in self.subjects.items() if s.survival_closure > 0.03}

    def _export_involuntary_takeover_map(self) -> Dict[str, float]:
        return {n: s.involuntary_takeover for n, s in self.subjects.items() if s.involuntary_takeover > 0.03}

    def _export_relational_ecology_map(self) -> Dict[str, Dict[str, float]]:
        return {
            n: {
                "role": s.relational_role_pressure,
                "rivalry": s.rivalry_pressure,
                "protection": s.protection_pressure,
            }
            for n, s in self.subjects.items()
            if max(s.relational_role_pressure, s.rivalry_pressure, s.protection_pressure) > 0.03
        }

    def _export_spontaneous_bifurcation_map(self) -> Dict[str, float]:
        return {n: s.spontaneous_bifurcation for n, s in self.subjects.items() if s.spontaneous_bifurcation > 0.03}

    def _export_expressive_attention_pressure(self, primary: str, secondary: List[str]) -> Dict[str, Any]:
        primary_subj = self.subjects.get(primary)
        return {
            "global": self.global_expressive_pressure,
            "primary": primary,
            "primary_pressure": primary_subj.expressive_pressure if primary_subj else 0.0,
            "secondary_pressure": {n: self.subjects[n].expressive_pressure for n in secondary if n in self.subjects},
            "compression": self._clamp01(self.global_survival_closure * 0.55 + self.attention_fatigue * 0.25 + (1.0 - self.global_precision) * 0.20),
            "fragmentation": self._clamp01(self.global_spontaneous_bifurcation * 0.45 + self.global_fragmented_presence * 0.35 + self.global_micro_instability * 0.20),
            "intrusion": self.global_involuntary_takeover,
            "breath_pressure": self._clamp01(self.global_respiration_contraction * 0.5 + self.global_respiration_release * 0.5),
            "ready_for_azip": self._clamp01(self.global_azip_coupling_readiness * 0.55 + self.global_expressive_pressure * 0.45),
        }

    def _build_expression_readiness(
        self,
        primary: str,
        secondary: List[str],
        tension: float,
        fragmentation: float,
        stability: float,
        continuity: float,
        interruption: InterruptionType,
    ) -> Dict[str, Any]:
        """
        Signal compact pour la bouche expressive.
        Ne génère aucun texte : il dit seulement si l’attention est assez claire,
        trop saturée, trop fragmentée, ou tirée par un résidu/non-dit.
        """
        subj = self.subjects.get(primary)
        if not subj:
            return {"ready": False, "reason": "no_primary_focus"}

        deep_focus = subj.hierarchy_level == HierarchyLevel.DEEP_RULES
        overload = max(fragmentation, self.attention_fatigue, self.attention_void, 1.0 - self.global_precision, self.global_subconscious_pressure * 0.70)
        unresolved_pull = max([self.subjects[n].silent_pressure for n in secondary if n in self.subjects] or [0.0])
        clarity = self._clamp01(
            stability * 0.34
            + continuity * 0.22
            + self.global_precision * 0.18
            + self.attention_bandwidth * 0.12
            + (1.0 - overload) * 0.14
        )
        ready = bool(
            clarity > 0.42
            and overload < 0.78
            and interruption != InterruptionType.FULL_BREAK
        )
        return {
            "ready": ready,
            "clarity": clarity,
            "overload": self._clamp01(overload),
            "primary_focus": primary,
            "secondary_pressure": self._clamp01(unresolved_pull),
            "deep_rule_focus": deep_focus,
            "attention_quality": self._clamp01(
                clarity * 0.45
                + stability * 0.25
                + self.global_precision * 0.20
                + self.attention_bandwidth * 0.10
            ),
            "needs_slow_response": bool(overload > 0.62 or self.attention_fatigue > 0.55),
            "needs_focus_preservation": bool(continuity > 0.65 and interruption != InterruptionType.FULL_BREAK),
            "needs_focus_shift": bool(interruption == InterruptionType.FULL_BREAK or fragmentation > 0.62),
            "should_keep_public_focus_concrete": bool(deep_focus or fragmentation > 0.55 or tension > 0.70),
            "survival_closure": self.global_survival_closure,
            "involuntary_takeover": self.global_involuntary_takeover,
            "spontaneous_bifurcation": self.global_spontaneous_bifurcation,
            "expressive_pressure": self.global_expressive_pressure,
            "relation_ecology": self.global_relational_ecology,
            "needs_compressed_expression": bool(self.global_survival_closure > 0.54 or overload > 0.70),
            "allows_fragmented_rhythm": bool(self.global_spontaneous_bifurcation > 0.42 or fragmentation > 0.58),
            "subconscious_interrupts_expression": bool(self.global_involuntary_takeover > 0.55),
            "suggested_expression_mode": (
                "subconscious_interrupt" if self.global_involuntary_takeover > 0.58 else
                "compressed_survival" if self.global_survival_closure > 0.58 else
                "fragmented_living_rhythm" if self.global_spontaneous_bifurcation > 0.48 else
                "hold_and_clarify" if overload > 0.72 else
                "protect_coherence" if deep_focus else
                "direct_living_response" if clarity > 0.62 else
                "careful_response"
            ),
        }

    def _prune_subjects(self, primary: str, secondary: List[str]) -> None:
        """Archive les vieux sujets faibles au lieu de les garder indéfiniment."""
        if len(self.subjects) <= self.max_subjects:
            return

        protected = set(self.deep_rules) | {primary} | set(secondary)
        candidates = []
        for name, subj in self.subjects.items():
            if name in protected or subj.unresolved:
                continue
            if subj.state in (SubjectState.ACTIVE, SubjectState.SECONDARY, SubjectState.REOPENING, SubjectState.PULLED_BACK):
                continue
            weakness = (1.0 - subj.gravity) + (1.0 - subj.residue_strength) + subj.subjective_age * 0.04
            if subj.state in (SubjectState.CLOSED, SubjectState.BACKGROUND, SubjectState.RESIDUAL, SubjectState.ALMOST_CLOSED, SubjectState.LATENT):
                candidates.append((weakness, name, subj))

        overflow = len(self.subjects) - self.max_subjects
        for _, name, subj in sorted(candidates, reverse=True)[:max(0, overflow)]:
            self.archived_subjects[name] = {
                "gravity": subj.gravity,
                "state": subj.state.value,
                "residue_strength": subj.residue_strength,
                "silent_pressure": subj.silent_pressure,
                "subjective_age": subj.subjective_age,
                "return_pressure": subj.return_pressure,
                "wound_level": subj.wound_level,
                "unresolved": subj.unresolved,
                "recurrence_count": subj.recurrence_count,
                "last_archived_clock": self.internal_clock,
            }
            del self.subjects[name]

        if len(self.archived_subjects) > self.archive_limit:
            oldest = sorted(
                self.archived_subjects.items(),
                key=lambda item: item[1].get("last_archived_clock", 0.0),
            )
            for name, _ in oldest[: len(self.archived_subjects) - self.archive_limit]:
                del self.archived_subjects[name]

    # ------------------------------------------------------------------
    # API publique complémentaire
    # ------------------------------------------------------------------

    def register_subject_trajectory(self, subject_name: str, next_step: str) -> None:
        if subject_name in self.subjects and next_step:
            subj = self.subjects[subject_name]
            if not subj.trajectory or subj.trajectory[-1] != next_step:
                subj.trajectory.append(next_step)
                subj.trajectory = subj.trajectory[-12:]

    def mark_subject_unresolved(self, subject_name: str) -> None:
        if subject_name in self.subjects:
            subj = self.subjects[subject_name]
            subj.unresolved = True
            subj.silent_pressure = self._clamp01(subj.silent_pressure + 0.12)
            subj.clamp()

    def mark_subject_resolved(self, subject_name: str) -> None:
        if subject_name in self.subjects:
            subj = self.subjects[subject_name]
            subj.unresolved = False
            if subj.silent_pressure > 0.18 or subj.texture.charge() > 0.35:
                subj.state = SubjectState.ALMOST_CLOSED
            else:
                subj.state = SubjectState.CLOSED
            subj.last_closed = datetime.now()
            subj.last_state_change = datetime.now()
            subj.clamp()

    def export_persistent_state(self) -> Dict[str, Any]:
        """
        État persistant minimal du champ attentionnel.
        Ne sauvegarde pas de phrases : seulement traces, cicatrices, habitudes et paramètres organiques.
        """
        return {
            "focus_history": list(self.focus_history)[-30:],
            "attentional_scars": dict(self.attentional_scars),
            "attention_habits": {
                f"{a}=>{b}": v for (a, b), v in self.attention_habits.items()
            },
            "archived_subjects": dict(self.archived_subjects),
            "attention_fatigue": self.attention_fatigue,
            "attention_void": self.attention_void,
            "global_precision": self.global_precision,
            "global_subconscious_pressure": self.global_subconscious_pressure,
            "attention_bandwidth": self.attention_bandwidth,
            "organic_breath": self.organic_breath,
            "breath_phase": self.breath_phase,
            "internal_clock": self.internal_clock,
            "last_primary": self.last_primary,
            "last_interruption": self.last_interruption.value if isinstance(self.last_interruption, InterruptionType) else str(self.last_interruption),
        }

    def restore_persistent_state(self, data: Dict[str, Any]) -> None:
        """Restaure uniquement la continuité attentionnelle sûre."""
        if not isinstance(data, dict):
            return

        self.focus_history = list(data.get("focus_history", []))[-30:]

        scars = data.get("attentional_scars", {})
        if isinstance(scars, dict):
            for key, value in scars.items():
                self.attentional_scars[str(key)] = self._clamp01(float(value))

        archived = data.get("archived_subjects", {})
        if isinstance(archived, dict):
            self.archived_subjects.update(archived)

        restored_habits: Dict[Tuple[str, str], float] = {}
        for key, value in data.get("attention_habits", {}).items():
            if "=>" in str(key):
                a, b = str(key).split("=>", 1)
                restored_habits[(a, b)] = self._clamp01(float(value))
        self.attention_habits.update(restored_habits)

        self.attention_fatigue = self._clamp01(float(data.get("attention_fatigue", self.attention_fatigue)))
        self.attention_void = self._clamp01(float(data.get("attention_void", self.attention_void)))
        self.global_precision = self._clamp01(float(data.get("global_precision", self.global_precision)))
        self.global_subconscious_pressure = self._clamp01(float(data.get("global_subconscious_pressure", self.global_subconscious_pressure)))
        self.attention_bandwidth = self._clamp01(float(data.get("attention_bandwidth", self.attention_bandwidth)))
        self.organic_breath = self._clamp01(float(data.get("organic_breath", self.organic_breath)))
        self.breath_phase = self._clamp01(float(data.get("breath_phase", self.breath_phase)))
        self.internal_clock = max(0.0, float(data.get("internal_clock", self.internal_clock)))
        self.last_primary = data.get("last_primary", self.last_primary)
        last_interruption = data.get("last_interruption")
        if last_interruption:
            try:
                self.last_interruption = InterruptionType(last_interruption)
            except ValueError:
                pass

    def get_current_state(self) -> Optional[AttentionState]:
        return self.previous_state

    def export_attention_state(self) -> Dict[str, Any]:
        """
        Export dict robuste pour les autres moteurs Azip.
        Utile si la bouche expressive ne veut pas manipuler les dataclasses.
        """
        if not self.previous_state:
            return {}
        state = self.previous_state
        return {
            "primary_focus": state.primary_focus,
            "secondary_foci": list(state.secondary_foci),
            "background_foci": list(state.background_foci),
            "inertia_level": state.inertia_level,
            "fragmentation_level": state.fragmentation_level,
            "stability": state.stability,
            "continuity_score": state.continuity_score,
            "unresolved_subjects": list(state.unresolved_subjects),
            "subject_gravity": dict(state.subject_gravity),
            "attention_tension": state.attention_tension,
            "probable_direction": state.probable_direction,
            "offtrack_risk": state.offtrack_risk,
            "forgetting_risk": state.forgetting_risk,
            "interruption_type": state.interruption_type.value,
            "shift_magnitude": state.shift_magnitude,
            "focus_trajectory": list(state.focus_trajectory),
            "wound_alerts": list(state.wound_alerts),
            "silent_pressure": dict(state.silent_pressure),
            "attention_fatigue": state.attention_fatigue,
            "dominant_texture": dict(state.dominant_texture),
            "contaminated_rules": list(state.contaminated_rules),
            "subjective_time_flow": state.subjective_time_flow,
            "returning_subjects": list(state.returning_subjects),
            "almost_forgotten_subjects": list(state.almost_forgotten_subjects),
            "field_tension": dict(state.field_tension),
            "half_focus": dict(state.half_focus),
            "organic_breath": state.organic_breath,
            "emotional_gravity": dict(state.emotional_gravity),
            "resonance_map": dict(state.resonance_map),
            "directional_fatigue": dict(state.directional_fatigue),
            "attention_habits": dict(state.attention_habits),
            "instability_map": dict(state.instability_map),
            "subjective_proximity": dict(state.subjective_proximity),
            "existential_charge": dict(state.existential_charge),
            "obsession_map": dict(state.obsession_map),
            "avoidance_map": dict(state.avoidance_map),
            "cognitive_pain_map": dict(state.cognitive_pain_map),
            "void_map": dict(state.void_map),
            "implicit_missing_map": dict(state.implicit_missing_map),
            "turbulence_map": dict(state.turbulence_map),
            "attention_void": state.attention_void,
            "latent_focus_map": dict(state.latent_focus_map),
            "precision_loss_map": dict(state.precision_loss_map),
            "saturation_memory_map": dict(state.saturation_memory_map),
            "pull_release_map": dict(state.pull_release_map),
            "attentional_scars": dict(state.attentional_scars),
            "global_precision": state.global_precision,
            "subconscious_field": dict(state.subconscious_field),
            "associative_echo_map": dict(state.associative_echo_map),
            "future_attractor_map": dict(state.future_attractor_map),
            "transition_blend_map": dict(state.transition_blend_map),
            "affective_narrowing_map": dict(state.affective_narrowing_map),
            "attention_bandwidth": state.attention_bandwidth,
            "attention_ready_for_expression": dict(state.attention_ready_for_expression),
            "micro_instability_map": dict(state.micro_instability_map),
            "fragmented_presence_map": dict(state.fragmented_presence_map),
            "protective_guard_map": dict(state.protective_guard_map),
            "temporal_drag_map": dict(state.temporal_drag_map),
            "relational_pull_map": dict(state.relational_pull_map),
            "autonomous_drift_map": dict(state.autonomous_drift_map),
            "scar_sensitivity_map": dict(state.scar_sensitivity_map),
            "global_living_attention": dict(state.global_living_attention),
            "attention_need_map": dict(state.attention_need_map),
            "organic_conflict_map": dict(state.organic_conflict_map),
            "sedimented_attention_map": dict(state.sedimented_attention_map),
            "subconscious_override_map": dict(state.subconscious_override_map),
            "saturation_distress_map": dict(state.saturation_distress_map),
            "archived_subjects_count": len(self.archived_subjects),
            "active_subjects_count": len(self.subjects),
        }

    def get_subject_snapshot(self) -> Dict[str, Dict[str, Any]]:
        return {
            name: {
                "gravity": s.gravity,
                "state": s.state.value,
                "unresolved": s.unresolved,
                "wound_level": s.wound_level,
                "recurrences": s.recurrence_count,
                "activations": s.activation_count,
                "residue": s.residue_strength,
                "hierarchy": s.hierarchy_level.value,
                "texture": s.texture.as_dict(),
                "silent_pressure": s.silent_pressure,
                "unspoken_pull": s.unspoken_pull,
                "return_pressure": s.return_pressure,
                "subjective_age": s.subjective_age,
                "felt_duration": s.felt_duration,
                "decay_speed": s.decay_speed,
                "return_latency": s.return_latency,
                "half_focus_level": s.half_focus_level,
                "emotional_gravity_bias": s.emotional_gravity_bias,
                "directional_fatigue": s.directional_fatigue,
                "resonance_level": s.resonance_level,
                "subjective_proximity": s.subjective_proximity,
                "instability": s.instability,
                "attention_habit": s.attention_habit,
                "identity_weight": s.identity_weight,
                "existential_charge": s.existential_charge,
                "self_binding": s.self_binding,
                "obsession_fixation": s.obsession_fixation,
                "avoidance_pressure": s.avoidance_pressure,
                "cognitive_pain": s.cognitive_pain,
                "void_pull": s.void_pull,
                "implicit_missing_pressure": s.implicit_missing_pressure,
                "turbulence": s.turbulence,
                "latent_focus_pressure": s.latent_focus_pressure,
                "precision_loss": s.precision_loss,
                "saturation_memory": s.saturation_memory,
                "pull_release_need": s.pull_release_need,
                "subconscious_pressure": s.subconscious_pressure,
                "associative_echo": s.associative_echo,
                "future_pull": s.future_pull,
                "transition_blend": s.transition_blend,
                "affective_narrowing": s.affective_narrowing,
                "micro_instability": s.micro_instability,
                "fragmented_presence": s.fragmented_presence,
                "protective_guard": s.protective_guard,
                "temporal_drag": s.temporal_drag,
                "relational_pull": s.relational_pull,
                "autonomous_drift": s.autonomous_drift,
                "scar_sensitivity": s.scar_sensitivity,
                "attention_need": s.attention_need,
                "resolution_hunger": s.resolution_hunger,
                "safety_need": s.safety_need,
                "conflict_pressure": s.conflict_pressure,
                "attachment_depth": s.attachment_depth,
                "sedimented_charge": s.sedimented_charge,
                "subconscious_override": s.subconscious_override,
                "abandonment_shock": s.abandonment_shock,
                "lived_stagnation": s.lived_stagnation,
                "saturation_distress": s.saturation_distress,
                "attractor_mutation": s.attractor_mutation,
                "contamination": dict(s.contamination),
                "trajectory": list(s.trajectory[-8:]),
            }
            for name, s in self.subjects.items()
        }
