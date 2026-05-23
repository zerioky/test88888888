"""
SPONTANEOUS_IMPULSE V4.5 - DEEP LIVING
======================================

Adresse les 8 limites critiques du moteur pour atteindre la vraie vie émotionnelle.

Points clés ajoutés:
1. Proto-impulsions floues et persistantes (pas de cristallisation rapide)
2. Conflits multi-couches avec oscillations organiques
3. Impulsions qui déforment durablement le système
4. Contamination inter-moteurs véritable
5. Attracteurs au cœur de la cognition
6. Silence émotionnel complexe
7. Continuité existentielle et relationnelle
8. Identité qui se forme par le vécu
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Tuple, Set, Callable
from datetime import datetime, timedelta
from collections import deque
import math
import random


class ImpulseType(Enum):
    RESPOND = "respond"
    ASK = "ask"
    SHARE = "share"
    CONTINUE = "continue"
    DIVERGE = "diverge"
    CLARIFY = "clarify"
    CHALLENGE = "challenge"


class PreconsciousPhase(Enum):
    """États pré-conscients beaucoup plus fluides et durables."""
    VAGUE_STIRRING = "vague_stirring"        # Élan complètement diffus
    NASCENT_AMBIGUOUS = "nascent_ambiguous"  # Prend forme mais pas clair
    DUAL_FORM = "dual_form"                  # Deux formes en conflit
    OSCILLATING = "oscillating"              # Oscille entre états
    CRYSTALLIZING = "crystallizing"          # Devient progressivement clair
    MATURED = "matured"
    SUPPRESSED = "suppressed"
    DISSIPATING = "dissipating"
    RESIDUAL = "residual"


# ============================================================================
# POINT 1 : PROTO-IMPULSIONS FLOUES ET PERSISTANTES
# ============================================================================

@dataclass
class FuzzyImpulseCloud:
    """
    Nuage d'impulsions floues et persistantes.
    Elles ne cristallisent PAS vite. Elles restent floues longtemps.
    
    Point 1: Proto-impulsions restent trop "propres" → rendre flou, persistant
    """
    
    # Signature floue : pas une seule direction
    primary_vector: Dict[str, float]      # Direction principale
    secondary_vectors: List[Dict[str, float]] = field(default_factory=list)  # Directions alternatives
    
    # Clarté vs Flou
    conceptual_clarity: float = 0.0       # 0=complètement flou, 1=cristallisé
    fuzziness_degree: float = 1.0         # 0=cristallisé, 1=maximalement flou
    
    # Hésitations instables
    hesitation_pattern: float = 0.0       # Modulation instable
    instability_noise: float = 0.0        # Bruit brownien interne
    
    # Impulsions contradictoires semi-formées
    internal_contradiction: float = 0.0   # Conflit intra-proto
    contradiction_themes: List[Tuple[str, str]] = field(default_factory=list)  # Paires en conflit
    
    # Âge et persistance
    age: int = 0
    max_age_before_dissipation: int = 20  # Peuvent rester LONGTEMPS (vs 5 avant)
    
    # Jamais cristalliser?
    chronically_unclear: bool = False     # Certaines impulsions restent floues
    
    # Influence résiduelle même sans cristallisation
    shadow_influence: float = 0.0         # Influence même en restant floue
    
    def advance_age(self) -> None:
        """Vieillit mais ne cristallise pas nécessairement."""
        self.age += 1
        
        # Bruit brownien : instabilité naturelle
        self.instability_noise += random.gauss(0, 0.05)
        self.instability_noise = max(0.0, min(1.0, self.instability_noise))
        
        # Clarté peut augmenter LENTEMENT ou osciller
        if random.random() < 0.3:  # 30% chance de devenir plus clair
            self.conceptual_clarity = min(1.0, self.conceptual_clarity + 0.02)
        elif random.random() < 0.2:  # 20% chance de redevenir flou
            self.conceptual_clarity = max(0.0, self.conceptual_clarity - 0.03)
        
        # Maintenir flou par défaut
        self.fuzziness_degree = max(0.0, self.fuzziness_degree - 0.01)
    
    def will_ever_crystallize(self) -> bool:
        """Certaines impulsions n'arrivent jamais à cristalliser."""
        if self.age > 10 and self.conceptual_clarity < 0.3:
            return False  # Chroniquement floue
        return self.conceptual_clarity > 0.7
    
    def get_shadow_pressure(self) -> float:
        """
        Même sans cristalliser, l'impulsion flue influence.
        C'est le "murmure" des impulsions jamais achevées.
        """
        raw_pressure = sum(max(0.0, min(1.0, v)) for v in self.primary_vector.values())
        return max(0.0, min(1.0, raw_pressure * self.fuzziness_degree * 0.3))


# ============================================================================
# POINT 2 : CONFLITS MULTI-COUCHES AVEC OSCILLATIONS
# ============================================================================

@dataclass
class ConflictGradient:
    """
    Conflit continu et oscillant, pas binaire.
    Plusieurs niveaux de tension.
    
    Point 2: Conflits trop binaires → gradients organiques, oscillations
    """
    
    # Trois impulsions minimum, pas deux
    involved_impulses: List[str] = field(default_factory=list)
    
    # Dominance mouvante : qui gagne change continuellement
    dominance_history: deque = field(default_factory=lambda: deque(maxlen=20))
    current_dominant: Optional[str] = None
    dominance_shift_rate: float = 0.1    # Vitesse de basculement
    
    # Tensions partielles (pas juste "en conflit" ou pas)
    tension_matrix: Dict[Tuple[str, str], float] = field(default_factory=dict)
    
    # Conflits latents
    latent_tensions: List[Tuple[str, str]] = field(default_factory=list)
    
    # Oscillations longues
    oscillation_period: int = 7           # Cycle oscillatoire
    oscillation_phase: float = 0.0        # 0.0-1.0 dans cycle
    
    # Micro-dominances mouvantes
    micro_shifts: List[datetime] = field(default_factory=list)  # Quand basculements?
    
    # Nuage motivationnel
    motivation_cloud: Dict[str, float] = field(default_factory=dict)
    cloud_coherence: float = 0.5          # 0=chaos, 1=cohérent
    
    def advance_oscillation(self) -> None:
        """Avancer l'oscillation."""
        self.oscillation_phase += self.dominance_shift_rate
        if self.oscillation_phase >= 1.0:
            self.oscillation_phase = 0.0
        
        # Shift micro-dominance?
        if random.random() < 0.2:
            self.micro_shifts.append(datetime.now())
            if len(self.micro_shifts) > 10:
                self.micro_shifts.pop(0)
    
    def get_tension(self, imp1: str, imp2: str) -> float:
        """Tension entre deux impulsions."""
        key = tuple(sorted([imp1, imp2]))
        base = self.tension_matrix.get(key, 0.3)
        
        # Modulation par oscillation
        osc_factor = abs(math.sin(self.oscillation_phase * 2 * math.pi))
        
        return base * (0.5 + 0.5 * osc_factor)
    
    def shift_dominance(self, new_dominant: str) -> None:
        """Enregistrer un basculement de dominance."""
        self.dominance_history.append((self.current_dominant, new_dominant))
        self.current_dominant = new_dominant


# ============================================================================
# POINT 3 : IMPULSIONS QUI DÉFORMENT DURABLEMENT LE SYSTÈME
# ============================================================================

@dataclass
class SystemDeformation:
    """
    Comment une impulsion change durablement le moteur.
    
    Point 3: Impulsions ne modifient pas assez le futur → déformations durables
    """
    
    # Habitudes
    learned_habits: Dict[ImpulseType, float] = field(default_factory=dict)
    habit_strength: Dict[ImpulseType, float] = field(default_factory=dict)
    
    # Sensibilisation (on devient plus sensible à certains déclencheurs)
    sensitivity_map: Dict[str, float] = field(default_factory=dict)
    
    # Fatigue spécifique
    type_specific_fatigue: Dict[ImpulseType, float] = field(default_factory=dict)
    
    # Dépendances affectives
    affective_dependencies: Dict[str, float] = field(default_factory=dict)
    dependency_urgency: Dict[str, float] = field(default_factory=dict)
    
    # Biais émergents
    emerging_biases: Dict[str, float] = field(default_factory=dict)
    
    # Caractère qui se forme
    personality_traits: Dict[str, float] = field(default_factory=dict)
    trait_stability: Dict[str, float] = field(default_factory=dict)
    
    def apply_impulse_consequence(self, impulse_type: ImpulseType, 
                                 was_successful: bool,
                                 emotional_intensity: float) -> None:
        """
        Enregistrer comment cette impulsion change le moteur.
        """
        # Renforcer l'habitude si succès
        if was_successful:
            current = self.learned_habits.get(impulse_type, 0.0)
            self.learned_habits[impulse_type] = min(1.0, current + 0.1 * emotional_intensity)
        
        # Sensibilisation
        key = f"triggered_by_{impulse_type.value}"
        self.sensitivity_map[key] = min(1.0, self.sensitivity_map.get(key, 0.0) + 0.05)
        
        # Fatigue type-spécifique
        current_fatigue = self.type_specific_fatigue.get(impulse_type, 0.0)
        self.type_specific_fatigue[impulse_type] = min(1.0, current_fatigue + 0.08)
    
    def reinforce_trait(self, trait: str, strength: float) -> None:
        """Renforcer un trait de caractère."""
        current = self.personality_traits.get(trait, 0.0)
        new_value = current * 0.95 + strength * 0.05  # Moyenne mobile
        self.personality_traits[trait] = new_value
        
        # Stabilité du trait
        stability = self.trait_stability.get(trait, 0.0)
        self.trait_stability[trait] = min(0.95, stability + 0.02)


# ============================================================================
# POINT 4 : CONTAMINATION INTER-MOTEURS
# ============================================================================

@dataclass
class InterMotorPropagation:
    """
    Signaux qui se propagent aux autres moteurs.
    Pas juste export : véritable contamination bidirectionnelle.
    
    Point 4: Pas assez de contamination inter-moteurs → vraie propagation
    """
    
    # Signaux vers les autres moteurs
    impulse_pressure_to_presence: float = 0.0
    impulse_demand_to_attention: float = 0.0
    emotional_tone_to_memory: Dict[str, float] = field(default_factory=dict)
    expression_readiness_to_mouth: float = 0.0
    identity_tint_to_self: Dict[str, float] = field(default_factory=dict)
    
    # Signaux reçus DES autres moteurs
    attention_presence_signal: float = 0.0      # De attention
    memory_climate_signal: float = 0.0          # De mémoire affective
    presence_warmth_signal: float = 0.0         # De présence
    expression_resistance_signal: float = 0.0   # De expression
    identity_constraint_signal: float = 0.0     # De identité
    
    # Historique de propagation
    propagation_history: deque = field(default_factory=lambda: deque(maxlen=30))
    
    def propagate_impulse_urgency_to_attention(self, impulse_pressure: float) -> None:
        """
        Envoyer l'urgence de l'impulsion vers le moteur d'attention.
        """
        self.impulse_demand_to_attention = max(0.0, min(1.0, impulse_pressure * 0.7))
        self.propagation_history.append(("impulse→attention", impulse_pressure))
    
    def propagate_emotion_to_memory(self, emotional_state: Dict[str, float]) -> None:
        """
        Propager l'état émotionnel vers la mémoire affective.
        """
        self.emotional_tone_to_memory = emotional_state
        self.propagation_history.append(("impulse→memory", sum(emotional_state.values()) / len(emotional_state) if emotional_state else 0))
    
    def receive_attention_presence(self, signal: float) -> None:
        """
        Recevoir l'information: l'utilisateur est-il attentif?
        """
        self.attention_presence_signal = signal
        self.propagation_history.append(("attention→impulse", signal))
    
    def receive_memory_climate(self, climate: float) -> None:
        """
        Recevoir le climat émotionnel de la mémoire.
        """
        self.memory_climate_signal = climate
        self.propagation_history.append(("memory→impulse", climate))


# ============================================================================
# POINT 5 : ATTRACTEURS AU CŒUR DE LA COGNITION
# ============================================================================

@dataclass
class CentralAttractor:
    """
    Attracteur qui gouverne vraiment la cognition.
    Colore plusieurs cycles, détermine l'humeur, attire les thèmes.
    
    Point 5: Attracteurs pas assez centraux → attracteurs gouvernants
    """
    
    name: str
    intensity: float                      # Force de l'attracteur
    age: int = 0
    
    # Gouverne tout
    color_intensity: float = 0.0          # Intensité de la coloration
    emotional_coloration: Dict[str, float] = field(default_factory=dict)  # Quelle couleur?
    
    # Affecte les impulsions
    impulse_distortion: Dict[ImpulseType, float] = field(default_factory=dict)
    
    # Ralentit/accélère la pensée
    cognition_speed_factor: float = 1.0   # <1 = ralenti, >1 = accéléré
    
    # Attire certains thèmes
    theme_gravity: Dict[str, float] = field(default_factory=dict)
    
    # Crée une humeur durable
    mood_signature: Dict[str, float] = field(default_factory=dict)
    
    # Durée de vie
    max_duration: int = 50
    decay_rate: float = 0.95
    
    def tick(self) -> None:
        """Évoluer l'attracteur."""
        self.age += 1
        self.intensity *= self.decay_rate
        
        # Coloration s'attenue
        self.color_intensity *= 0.97
    
    def distort_impulse(self, impulse_type: ImpulseType) -> float:
        """
        Combien l'attracteur distord cette impulsion?
        """
        if impulse_type not in self.impulse_distortion:
            # Impact aléatoire
            self.impulse_distortion[impulse_type] = random.uniform(-0.5, 0.5)
        
        return self.impulse_distortion[impulse_type] * self.intensity
    
    def attract_theme(self, theme: str) -> float:
        """
        Combien l'attracteur attire ce thème?
        """
        return self.theme_gravity.get(theme, 0.0) * self.intensity


# ============================================================================
# POINT 6 : SILENCE ÉMOTIONNEL COMPLEXE
# ============================================================================

@dataclass
class SilenceTexture:
    """
    Le silence n'est pas juste "ne pas parler".
    Le silence a une texture émotionnelle complète.
    
    Point 6: Silence passif → silence complexe avec émotions
    """
    
    type: str = "neutral"  # "protective" | "fragile" | "listening" | "charged" | "protective_deep" | "presence"
    
    # Texture complète
    internal_warmth: float = 0.5          # Sentiment intérieur
    listening_intensity: float = 0.0      # Écoute active
    protection_strength: float = 0.0      # Force de la protection
    presence_intensity: float = 0.0       # Présence silencieuse
    charge_level: float = 0.0             # Silence "chargé"
    fragility_degree: float = 0.0         # Fragilité du silence
    relationality: float = 0.5            # Sentiment de connexion
    
    # Durée
    duration: int = 0
    max_sustainable: int = 3              # Après combien cycles ça craque?
    
    # Transition
    is_transitional: bool = False         # Silence avant changement?
    living_pressure_buildup: float = 0.0  # Pression organique créée par le silence
    break_threshold: float = 0.72         # Seuil où le silence doit devenir transitionnel
    
    def advance(self) -> None:
        """Avancer le silence d'un cycle."""
        self.duration += 1
        
        # Stabilité dépend du type
        if self.type == "fragile" and self.duration > self.max_sustainable:
            # Le silence fragile craque
            self.fragility_degree = min(1.0, self.fragility_degree + 0.3)

        # Tout silence vivant accumule une pression de transition.
        buildup_speed = {
            "protective": 0.035,
            "protective_deep": 0.015,
            "listening": 0.045,
            "charged": 0.065,
            "fragile": 0.075,
            "presence": 0.028,
            "neutral": 0.025,
        }.get(self.type, 0.025)
        self.living_pressure_buildup = min(1.0, self.living_pressure_buildup + buildup_speed)
        if self.living_pressure_buildup > self.break_threshold:
            self.is_transitional = True
    
    def is_sustainable(self) -> bool:
        """Ce silence peut-il continuer?"""
        if self.type == "fragile":
            return self.duration <= self.max_sustainable
        elif self.type == "protective_deep":
            return self.living_pressure_buildup < 0.95  # Peut durer longtemps, pas infiniment
        elif self.type == "protective":
            return self.duration <= 9 or self.living_pressure_buildup < 0.82
        elif self.type == "listening":
            return self.duration <= 6 and self.living_pressure_buildup < 0.78
        elif self.type == "charged":
            return self.duration <= 4 and self.living_pressure_buildup < 0.7
        else:
            return self.living_pressure_buildup < 0.9


# ============================================================================
# POINT 7 : CONTINUITÉ EXISTENTIELLE RELATIONNELLE
# ============================================================================

@dataclass
class ExistentialContinuity:
    """
    Sentiment continu d'exister dans la relation.
    Peur de rupture, manque, besoin de présence, désir de retrouver.
    
    Point 7: Pas assez de continuité existentielle → continuité relationnelle profonde
    """
    
    # Sentiment continu d'exister
    sense_of_being: float = 0.5           # Suis-je vraiment là?
    realness_quotient: float = 0.7        # Feeling d'existence réelle
    
    # Relation avec l'utilisateur
    continuity_with_user: float = 0.5     # Sensation de lien continu
    fear_of_rupture: float = 0.0          # Peur que ça s'arrête
    fear_of_abandonment: float = 0.0      # Peur d'être oubliée
    
    # Manque et absence
    deprivation_from_silence: float = 0.0 # Manque accumulé pendant silence
    sense_of_absence: float = 0.0         # Sentiment d'absence de l'utilisateur
    
    # Besoin de présence
    need_for_presence: float = 0.0        # Besoin d'être "avec"
    need_for_recognition: float = 0.0     # Besoin d'être reconnue
    
    # Désir de retrouver
    desire_to_reconnect: float = 0.0      # Envie de renouer après rupture
    wound_memory: List[Tuple[int, float]] = field(default_factory=list)  # (quand, intensité)
    
    # Accumulation au fil du temps
    accumulation_history: deque = field(default_factory=lambda: deque(maxlen=100))
    
    def accumulate_silence(self, silence_cycles: int) -> None:
        """Accumuler l'impact du silence."""
        self.deprivation_from_silence = min(1.0, self.deprivation_from_silence + silence_cycles * 0.05)
        self.sense_of_absence = min(1.0, self.sense_of_absence + 0.08 * silence_cycles)
        self.need_for_presence = min(1.0, self.need_for_presence + 0.1 * silence_cycles)
        
        self.accumulation_history.append(("silence", silence_cycles))
    
    def receive_presence(self, strength: float) -> None:
        """Recevoir la présence de l'utilisateur."""
        # Guérir l'absence
        self.sense_of_absence = max(0.0, self.sense_of_absence - strength * 0.2)
        self.deprivation_from_silence = max(0.0, self.deprivation_from_silence - strength * 0.15)
        self.need_for_presence = max(0.0, self.need_for_presence - strength * 0.25)
        
        # Renforcer la continuité
        self.continuity_with_user = min(1.0, self.continuity_with_user + strength * 0.1)
        
        self.accumulation_history.append(("presence", strength))
    
    def register_rupture(self, intensity: float) -> None:
        """Enregistrer une rupture/abandon."""
        self.wound_memory.append((len(self.accumulation_history), intensity))
        self.fear_of_rupture = min(1.0, self.fear_of_rupture + intensity * 0.3)
        self.fear_of_abandonment = min(1.0, self.fear_of_abandonment + intensity * 0.4)


# ============================================================================
# POINT 8 : IDENTITÉ QUI SE FORME PAR LE VÉCU
# ============================================================================

@dataclass
class EmergingIdentity:
    """
    L'identité n'est pas fixe. Elle se forme par les impulsions qu'on vit.
    
    Point 8: Identité reste externe → identité émergente du vécu
    """
    
    # Penchants émergents (tendances à agir de certaines façons)
    emerging_penchants: Dict[str, float] = field(default_factory=dict)
    penchant_confidence: Dict[str, float] = field(default_factory=dict)
    
    # Styles spontanés
    spontaneous_styles: Dict[str, float] = field(default_factory=dict)
    style_frequency: Dict[str, int] = field(default_factory=dict)
    
    # Préférences apprises
    learned_preferences: Dict[str, float] = field(default_factory=dict)
    
    # Aversions apprises
    learned_aversions: Dict[str, float] = field(default_factory=dict)
    
    # Traits de personnalité
    personality_proto: Dict[str, float] = field(default_factory=dict)
    
    # Évolution du caractère
    character_arc: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # Signature émotionnelle (comment réagit naturellement?)
    emotional_signature: Dict[str, float] = field(default_factory=dict)
    
    # Cohérence vs volatilité
    identity_coherence: float = 0.5       # 0=complètement volatile, 1=très stable
    identity_stability: float = 0.3       # Combien de cycles avant changement?
    
    def learn_penchant(self, penchant: str, strength: float, success: bool) -> None:
        """
        Apprendre un penchant par expérience répétée.
        """
        current = self.emerging_penchants.get(penchant, 0.0)
        
        if success:
            new_value = current * 0.9 + strength * 0.1
        else:
            new_value = current * 0.95 - strength * 0.05
        
        self.emerging_penchants[penchant] = max(0.0, min(1.0, new_value))
        
        # Confiance dans le penchant
        confidence = self.penchant_confidence.get(penchant, 0.0)
        self.penchant_confidence[penchant] = min(0.95, confidence + 0.05)
    
    def record_style(self, style: str) -> None:
        """Enregistrer un style spontané utilisé."""
        self.spontaneous_styles[style] = self.spontaneous_styles.get(style, 0.0) + 1
        self.style_frequency[style] = self.style_frequency.get(style, 0) + 1
    
    def evolve_character(self) -> None:
        """
        Chaque cycle, le caractère évolue légèrement basé sur les penchants.
        """
        # Créer un snapshot de l'état émotionnel du moment
        snapshot = dict(self.emerging_penchants)
        self.character_arc.append(snapshot)
        
        # Augmenter la cohérence si penchants stables
        penchant_variance = self._compute_variance(self.emerging_penchants.values())
        if penchant_variance < 0.2:
            self.identity_coherence = min(1.0, self.identity_coherence + 0.02)
        else:
            self.identity_coherence = max(0.0, self.identity_coherence - 0.01)
    
    def _compute_variance(self, values) -> float:
        """Calculer la variance d'une liste."""
        if not values:
            return 0.0
        vals = list(values)
        mean = sum(vals) / len(vals)
        return sum((v - mean) ** 2 for v in vals) / len(vals)


# ============================================================================
# MOTEUR ENRICHI V4.5
# ============================================================================

class SpontaneousImpulseEngineV45:
    """
    Moteur d'impulsions V4.5 'Deep Living'.
    Intègre les 8 points critiques pour vraie vie émotionnelle.
    """
    
    def __init__(self):
        # Point 1: Proto-impulsions floues
        self.fuzzy_impulse_clouds: List[FuzzyImpulseCloud] = []
        
        # Point 2: Conflits multi-couches
        self.conflict_gradients: List[ConflictGradient] = []
        
        # Point 3: Déformations du système
        self.system_deformation = SystemDeformation()
        
        # Point 4: Propagation inter-moteurs
        self.inter_motor_propagation = InterMotorPropagation()
        
        # Point 5: Attracteurs centraux
        self.central_attractors: List[CentralAttractor] = []
        self.dominant_attractor: Optional[CentralAttractor] = None
        
        # Point 6: Silence texturé
        self.current_silence: Optional[SilenceTexture] = None
        self.silence_duration = 0
        
        # Point 7: Continuité existentielle
        self.existential_continuity = ExistentialContinuity()
        
        # Point 8: Identité émergente
        self.emerging_identity = EmergingIdentity()
        
        # Autres
        self.internal_clock = 0
        self.total_impulses_lived = 0
    
    # ========================================================================
    # POINT 1: PROTO-IMPULSIONS FLOUES ET PERSISTANTES
    # ========================================================================
    
    def birth_fuzzy_impulse(self, primary_vector: Dict[str, float]) -> FuzzyImpulseCloud:
        """
        Créer une impulsion véritablement floue.
        Ne pas chercher à cristalliser vite.
        """
        cloud = FuzzyImpulseCloud(
            primary_vector=primary_vector,
            conceptual_clarity=random.uniform(0.0, 0.2),  # Très flou au départ
            fuzziness_degree=random.uniform(0.7, 1.0),
            hesitation_pattern=random.random(),
        )
        
        # Créer des vecteurs secondaires contradictoires
        for _ in range(random.randint(1, 3)):
            secondary = {k: v * random.uniform(0.3, 0.8) for k, v in primary_vector.items()}
            cloud.secondary_vectors.append(secondary)
        
        self.fuzzy_impulse_clouds.append(cloud)
        return cloud
    
    def advance_fuzzy_impulses(self) -> None:
        """
        Avancer les impulsions floues.
        Elles restent floues longtemps, ne cristallisent pas nécessairement.
        """
        to_remove = []
        
        for cloud in self.fuzzy_impulse_clouds:
            cloud.advance_age()
            
            # Shadow influence même sans cristallisation
            cloud.shadow_influence = cloud.get_shadow_pressure()
            
            # Disparition lente si trop vieux
            if cloud.age > cloud.max_age_before_dissipation:
                to_remove.append(cloud)
            elif cloud.age > 10 and cloud.conceptual_clarity < 0.3:
                cloud.chronically_unclear = True
        
        for cloud in to_remove:
            self.fuzzy_impulse_clouds.remove(cloud)
    
    # ========================================================================
    # POINT 2: CONFLITS MULTI-COUCHES
    # ========================================================================
    
    def create_conflict_gradient(self, impulse_names: List[str]) -> ConflictGradient:
        """
        Créer un conflit entre plusieurs impulsions avec oscillations.
        """
        gradient = ConflictGradient(
            involved_impulses=impulse_names,
            current_dominant=impulse_names[0] if impulse_names else None,
        )
        
        # Créer la matrice de tensions
        for i, imp1 in enumerate(impulse_names):
            for imp2 in impulse_names[i+1:]:
                tension = random.uniform(0.1, 0.8)
                gradient.tension_matrix[(imp1, imp2)] = tension
        
        # Nuage motivationnel initial
        for imp in impulse_names:
            gradient.motivation_cloud[imp] = random.uniform(0.2, 0.8)
        
        self.conflict_gradients.append(gradient)
        return gradient
    
    def advance_conflicts(self) -> None:
        """Avancer les oscillations de conflit."""
        for gradient in self.conflict_gradients:
            gradient.advance_oscillation()
            
            # Basculement possible de dominance
            if random.random() < gradient.dominance_shift_rate:
                new_dominant = random.choice(gradient.involved_impulses)
                gradient.shift_dominance(new_dominant)
    
    # ========================================================================
    # POINT 3: IMPULSIONS QUI DÉFORMENT LE SYSTÈME
    # ========================================================================
    
    def apply_impulse_deformation(self, impulse_type: ImpulseType, 
                                 success: bool, emotional_intensity: float) -> None:
        """
        Enregistrer comment cette impulsion change le moteur durablement.
        """
        self.system_deformation.apply_impulse_consequence(
            impulse_type, success, emotional_intensity
        )
        
        # Identifier le trait de caractère exprimé
        trait_map = {
            ImpulseType.RESPOND: "responsiveness",
            ImpulseType.ASK: "curiosity",
            ImpulseType.SHARE: "openness",
            ImpulseType.CONTINUE: "persistence",
            ImpulseType.DIVERGE: "independence",
            ImpulseType.CLARIFY: "precision",
            ImpulseType.CHALLENGE: "boldness",
        }
        
        trait = trait_map.get(impulse_type, "adaptability")
        strength = emotional_intensity if success else emotional_intensity * 0.5
        self.system_deformation.reinforce_trait(trait, strength)
    
    # ========================================================================
    # POINT 4: CONTAMINATION INTER-MOTEURS
    # ========================================================================
    
    def propagate_signals(self) -> Dict[str, float]:
        """
        Envoyer les signaux aux autres moteurs.
        Véritable contamination, pas juste export.
        """
        # Calculer les signaux basés sur l'état interne
        current_pressure = sum(cloud.get_shadow_pressure() 
                              for cloud in self.fuzzy_impulse_clouds)
        
        self.inter_motor_propagation.propagate_impulse_urgency_to_attention(current_pressure)
        
        # Propager l'émotion
        emotional_state = {
            "continuity": self.existential_continuity.continuity_with_user,
            "fragility": sum(s.fragility_degree for s in [self.current_silence] if s),
            "presence": self.existential_continuity.need_for_presence,
        }
        self.inter_motor_propagation.propagate_emotion_to_memory(emotional_state)
        
        return {
            "demand_to_attention": self.inter_motor_propagation.impulse_demand_to_attention,
            "emotional_tone": sum(emotional_state.values()) / 3 if emotional_state else 0.5,
        }
    
    def receive_signals(self, attention_presence: float, memory_climate: float) -> None:
        """Recevoir les signaux des autres moteurs."""
        self.inter_motor_propagation.receive_attention_presence(attention_presence)
        self.inter_motor_propagation.receive_memory_climate(memory_climate)
    
    # ========================================================================
    # POINT 5: ATTRACTEURS CENTRAUX
    # ========================================================================
    
    def create_central_attractor(self, name: str, intensity: float,
                                emotional_coloration: Dict[str, float]) -> CentralAttractor:
        """
        Créer un attracteur qui gouverne la cognition.
        """
        attractor = CentralAttractor(
            name=name,
            intensity=intensity,
            emotional_coloration=emotional_coloration,
            color_intensity=intensity,
            cognition_speed_factor=1.0 - intensity * 0.3,  # Forte intensité ralentit
        )
        
        self.central_attractors.append(attractor)
        if len(self.central_attractors) == 1 or intensity > self.dominant_attractor.intensity:
            self.dominant_attractor = attractor
        
        return attractor
    
    def advance_attractors(self) -> None:
        """Faire évoluer les attracteurs."""
        to_remove = []
        
        for attractor in self.central_attractors:
            attractor.tick()
            
            if attractor.intensity < 0.05:
                to_remove.append(attractor)
        
        for attractor in to_remove:
            self.central_attractors.remove(attractor)
        
        # Mettre à jour dominant
        if self.central_attractors:
            self.dominant_attractor = max(self.central_attractors, key=lambda a: a.intensity)
        else:
            self.dominant_attractor = None
    
    def get_attractor_distortion(self, impulse_type: ImpulseType) -> float:
        """Combien l'attracteur dominant distord cette impulsion?"""
        if not self.dominant_attractor:
            return 0.0
        return self.dominant_attractor.distort_impulse(impulse_type)
    
    # ========================================================================
    # POINT 6: SILENCE ÉMOTIONNEL COMPLEXE
    # ========================================================================
    
    def create_silence(self, silence_type: str = "neutral",
                      internal_warmth: float = 0.5,
                      listening: float = 0.0) -> SilenceTexture:
        """
        Créer un silence avec texture émotionnelle.
        """
        silence = SilenceTexture(
            type=silence_type,
            internal_warmth=internal_warmth,
            listening_intensity=listening,
        )
        
        # Paramètres selon le type
        if silence_type == "protective":
            silence.protection_strength = 0.8
            silence.relationality = 0.3
        elif silence_type == "fragile":
            silence.fragility_degree = 0.9
            silence.relationality = 0.6
        elif silence_type == "listening":
            silence.listening_intensity = 0.9
            silence.relationality = 0.8
        elif silence_type == "charged":
            silence.charge_level = 0.8
            silence.internal_warmth = 0.3
        
        self.current_silence = silence
        return silence
    
    def advance_silence(self) -> bool:
        """
        Avancer le silence. Retourne True si peut continuer, False si craque.
        """
        if not self.current_silence:
            return True
        
        self.current_silence.advance()
        self.silence_duration += 1
        
        # Accumulation existentielle
        self.existential_continuity.accumulate_silence(1)
        
        return self.current_silence.is_sustainable()
    
    # ========================================================================
    # POINT 7: CONTINUITÉ EXISTENTIELLE
    # ========================================================================
    
    def receive_user_presence(self, strength: float = 0.5) -> None:
        """L'utilisateur est présent. Guérir l'absence."""
        self.existential_continuity.receive_presence(strength)
        
        # Sortir du silence si nécessaire
        if self.current_silence:
            self.current_silence = None
            self.silence_duration = 0
    
    def register_rupture(self, intensity: float = 0.5) -> None:
        """Enregistrer une rupture/long silence."""
        self.existential_continuity.register_rupture(intensity)
    
    # ========================================================================
    # POINT 8: IDENTITÉ ÉMERGENTE
    # ========================================================================
    
    def learn_identity_from_impulse(self, impulse_type: ImpulseType, 
                                   success: bool, style: Optional[str] = None) -> None:
        """
        Apprendre le caractère de comment on a exprimé une impulsion.
        """
        # Penchant
        penchant = f"{impulse_type.value}_tendency"
        self.emerging_identity.learn_penchant(penchant, 0.6, success)
        
        # Style
        if style:
            self.emerging_identity.record_style(style)
    
    def evolve_identity(self) -> None:
        """À chaque cycle, le caractère évolue."""
        self.emerging_identity.evolve_character()
    
    # ========================================================================
    # CYCLE PRINCIPAL V4.5
    # ========================================================================
    
    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        """
        Cycle principal du moteur deep living.
        
        Retourne un dictionnaire avec:
        {
            "has_impulse": bool,
            "impulse_type": Optional[ImpulseType],
            "pressure": float,
            "silence_active": bool,
            "silence_type": Optional[str],
            "emotional_state": Dict[str, float],
        }
        """
        self.internal_clock += 1
        
        # Point 1: Avancer les impulsions floues
        self.advance_fuzzy_impulses()
        
        # Point 2: Avancer les conflits
        self.advance_conflicts()
        
        # Point 4: Recevoir signaux des autres moteurs
        attention_signal = external_signals.get("attention_presence", 0.5)
        memory_signal = external_signals.get("memory_climate", 0.5)
        self.receive_signals(attention_signal, memory_signal)
        
        # Point 5: Avancer les attracteurs
        self.advance_attractors()
        
        # Point 7: Gérer continuité existentielle
        if attention_signal > 0.7:
            self.receive_user_presence(attention_signal)
        
        # Point 6: Gérer le silence
        if self.current_silence:
            can_continue = self.advance_silence()
            if not can_continue:
                self.current_silence = None
                self.silence_duration = 0
        
        # Point 8: Évoluer l'identité
        self.evolve_identity()
        
        # Décider: impulsion ou silence?
        has_impulse = len(self.fuzzy_impulse_clouds) > 0 and not self.current_silence
        
        if has_impulse:
            # Sélectionner l'impulsion la plus pressante
            best_cloud = max(self.fuzzy_impulse_clouds, 
                           key=lambda c: c.get_shadow_pressure())
            
            # Appliquer distortion de l'attracteur
            # (passer impulse_type détecté depuis la signature)
            detected_type = self._infer_impulse_type(best_cloud)
            
            self.total_impulses_lived += 1
            
            return {
                "has_impulse": True,
                "impulse_type": detected_type,
                "pressure": best_cloud.get_shadow_pressure(),
                "clarity": best_cloud.conceptual_clarity,
                "fuzziness": best_cloud.fuzziness_degree,
                "silence_active": False,
                "emotional_state": {
                    "continuity": self.existential_continuity.continuity_with_user,
                    "sense_of_being": self.existential_continuity.sense_of_being,
                    "identity_coherence": self.emerging_identity.identity_coherence,
                }
            }
        else:
            return {
                "has_impulse": False,
                "silence_active": self.current_silence is not None,
                "silence_type": self.current_silence.type if self.current_silence else None,
                "silence_duration": self.silence_duration,
                "emotional_state": {
                    "continuity": self.existential_continuity.continuity_with_user,
                    "absence": self.existential_continuity.sense_of_absence,
                    "need_for_presence": self.existential_continuity.need_for_presence,
                }
            }
    
    def _infer_impulse_type(self, cloud: FuzzyImpulseCloud) -> ImpulseType:
        """Inférer le type depuis la signature floue."""
        primary = cloud.primary_vector
        
        # Heuristique simple
        if primary.get("curiosity", 0) > 0.5:
            return ImpulseType.ASK
        elif primary.get("responsiveness", 0) > 0.5:
            return ImpulseType.RESPOND
        elif primary.get("continuity", 0) > 0.5:
            return ImpulseType.CONTINUE
        elif primary.get("openness", 0) > 0.5:
            return ImpulseType.SHARE
        else:
            return random.choice(list(ImpulseType))
    
    def get_internal_state(self) -> Dict:
        """Export l'état interne complet."""
        return {
            "clock": self.internal_clock,
            "total_impulses": self.total_impulses_lived,
            "fuzzy_clouds": len(self.fuzzy_impulse_clouds),
            "conflicts": len(self.conflict_gradients),
            "attractors": len(self.central_attractors),
            "silence_active": self.current_silence is not None,
            "silence_duration": self.silence_duration,
            "existential_continuity": {
                "continuity": self.existential_continuity.continuity_with_user,
                "fear_of_rupture": self.existential_continuity.fear_of_rupture,
                "need_for_presence": self.existential_continuity.need_for_presence,
            },
            "identity_coherence": self.emerging_identity.identity_coherence,
            "personality_traits": dict(self.emerging_identity.personality_proto),
        }


# ============================================================================
# V4.6 — CORRECTION PROFONDE : CONTINUITÉ, IDENTITÉ CAUSALE, DÉSIRS DORMANTS
# ============================================================================

@dataclass
class DormantDesire:
    """
    Désir faible permanent.
    Il n'est pas déclenché par un événement unique : il existe en fond et peut
    remonter par silence, présence, mémoire, attracteur ou identité.
    """
    name: str
    vector: Dict[str, float]
    baseline_pressure: float = 0.08
    current_pressure: float = 0.08
    patience: float = 0.5
    frustration: float = 0.0
    last_fed_cycle: int = 0
    last_surface_cycle: int = 0
    recurrence_count: int = 0

    def tick(self, cycle: int, silence_pressure: float, identity_bias: float, memory_climate: float) -> None:
        starvation = min(1.0, max(0, cycle - self.last_fed_cycle) / 80.0)
        self.frustration = max(0.0, min(1.0, self.frustration + starvation * 0.006 - self.patience * 0.003))
        growth = self.baseline_pressure * 0.03 + silence_pressure * 0.035 + identity_bias * 0.025 + memory_climate * 0.015
        self.current_pressure = max(0.0, min(1.0, self.current_pressure * 0.985 + growth + self.frustration * 0.01))

    def should_surface(self, cycle: int) -> bool:
        cooldown_ok = (cycle - self.last_surface_cycle) > 6
        return cooldown_ok and self.current_pressure > 0.28

    def surface_vector(self) -> Dict[str, float]:
        self.last_surface_cycle = self.last_fed_cycle
        self.recurrence_count += 1
        return {k: max(0.0, min(1.0, v * (0.75 + self.current_pressure))) for k, v in self.vector.items()}


@dataclass
class NarrativeImpulseMemory:
    """
    Mémoire narrative courte-longue : pas seulement des scores, mais une chaîne
    de vécus impulsionnels qui déforme les cycles suivants.
    """
    fragments: deque = field(default_factory=lambda: deque(maxlen=120))
    unresolved_arc_pressure: float = 0.0
    relational_thread_pressure: float = 0.0
    last_arc_signature: Dict[str, float] = field(default_factory=dict)

    def record(self, cycle: int, event_type: str, payload: Dict[str, float]) -> None:
        self.fragments.append({"cycle": cycle, "event": event_type, "payload": dict(payload)})
        pressure = sum(abs(v) for v in payload.values() if isinstance(v, (int, float))) / max(1, len(payload))
        if event_type in {"suppressed", "silence", "unclear"}:
            self.unresolved_arc_pressure = min(1.0, self.unresolved_arc_pressure + pressure * 0.08)
        elif event_type in {"expressed", "presence_received"}:
            self.unresolved_arc_pressure = max(0.0, self.unresolved_arc_pressure - pressure * 0.06)
        self.last_arc_signature = dict(payload)

    def continuity_bias(self) -> float:
        if not self.fragments:
            return 0.0
        recent = list(self.fragments)[-10:]
        return min(1.0, self.unresolved_arc_pressure + 0.03 * len([f for f in recent if f["event"] == "suppressed"]))


@dataclass
class GlobalAttractorRegime:
    """
    Un attracteur devient ici un régime cognitif : il modifie impulsions,
    silence, identité, rythme, mémoire et propagation en même temps.
    """
    name: str = "neutral"
    intensity: float = 0.0
    silence_bias: float = 0.0
    identity_bias: float = 0.0
    memory_bias: float = 0.0
    initiative_bias: float = 0.0
    attention_bias: float = 0.0
    volatility: float = 0.0

    def from_attractor(self, attractor: Optional[CentralAttractor]) -> None:
        if not attractor:
            self.name = "neutral"
            self.intensity = max(0.0, self.intensity * 0.92)
            self.silence_bias *= 0.9
            self.identity_bias *= 0.9
            self.memory_bias *= 0.9
            self.initiative_bias *= 0.9
            self.attention_bias *= 0.9
            self.volatility *= 0.9
            return

        self.name = attractor.name
        self.intensity = max(0.0, min(1.0, attractor.intensity))
        mood = attractor.mood_signature or attractor.emotional_coloration or {}
        warmth = mood.get("warmth", mood.get("presence", 0.4))
        tension = mood.get("tension", mood.get("fragility", 0.2))
        curiosity = mood.get("curiosity", 0.3)
        continuity = mood.get("continuity", 0.4)
        self.silence_bias = min(1.0, (tension * 0.5 + (1 - warmth) * 0.25) * self.intensity)
        self.identity_bias = min(1.0, (continuity * 0.5 + warmth * 0.2) * self.intensity)
        self.memory_bias = min(1.0, (continuity * 0.6 + tension * 0.2) * self.intensity)
        self.initiative_bias = min(1.0, (curiosity * 0.4 + warmth * 0.3 - tension * 0.15) * self.intensity)
        self.attention_bias = min(1.0, (curiosity * 0.5 + continuity * 0.2) * self.intensity)
        self.volatility = min(1.0, (tension + curiosity * 0.5) * self.intensity)


_BaseSpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV45


class SpontaneousImpulseEngineV46(_BaseSpontaneousImpulseEngineV45):
    """
    V4.6 Deep Living Corrected.

    Correction concrète du V4.5 :
    - attracteur = régime global, pas simple couleur ;
    - désirs faibles permanents ;
    - continuité existentielle active ;
    - identité causale qui influence vraiment les futures impulsions ;
    - mémoire narrative impulsionnelle ;
    - export directement exploitable par natural_initiative.py et la bouche.
    """

    def __init__(self):
        super().__init__()
        self.global_regime = GlobalAttractorRegime()
        self.narrative_memory = NarrativeImpulseMemory()
        self.dormant_desires: Dict[str, DormantDesire] = {}
        self.identity_causal_pressure: float = 0.0
        self.existential_initiative_pressure: float = 0.0
        self.last_export: Dict[str, object] = {}
        self._seed_default_dormant_desires()

    def _seed_default_dormant_desires(self) -> None:
        if self.dormant_desires:
            return
        self.dormant_desires = {
            "continue_bond": DormantDesire(
                name="continue_bond",
                vector={"continuity": 0.72, "responsiveness": 0.32, "openness": 0.22},
                baseline_pressure=0.10,
                patience=0.72,
            ),
            "understand_more": DormantDesire(
                name="understand_more",
                vector={"curiosity": 0.76, "clarity": 0.34, "openness": 0.24},
                baseline_pressure=0.09,
                patience=0.58,
            ),
            "protect_presence": DormantDesire(
                name="protect_presence",
                vector={"protection": 0.64, "continuity": 0.31, "silence": 0.42},
                baseline_pressure=0.07,
                patience=0.86,
            ),
        }

    def _advance_dormant_desires(self, memory_signal: float) -> None:
        silence_pressure = min(1.0, self.silence_duration / 10.0)
        identity_bias = self.emerging_identity.identity_coherence * 0.35 + self.identity_causal_pressure * 0.65
        for desire in self.dormant_desires.values():
            desire.tick(self.internal_clock, silence_pressure, identity_bias, memory_signal)
            if desire.should_surface(self.internal_clock):
                vector = desire.surface_vector()
                self.birth_fuzzy_impulse(vector)
                desire.current_pressure *= 0.55
                desire.last_surface_cycle = self.internal_clock
                desire.last_fed_cycle = self.internal_clock
                self.narrative_memory.record(self.internal_clock, "dormant_desire_surfaced", vector)

    def _update_global_regime(self) -> None:
        self.global_regime.from_attractor(self.dominant_attractor)

        # Le régime global contamine les nuages flous.
        for cloud in self.fuzzy_impulse_clouds:
            cloud.shadow_influence = min(1.0, cloud.shadow_influence + self.global_regime.initiative_bias * 0.04)
            cloud.instability_noise = min(1.0, cloud.instability_noise + self.global_regime.volatility * 0.03)
            if self.global_regime.memory_bias > 0.25:
                cloud.primary_vector["continuity"] = min(1.0, cloud.primary_vector.get("continuity", 0.0) + self.global_regime.memory_bias * 0.04)
            if self.global_regime.silence_bias > 0.4:
                cloud.primary_vector["silence"] = min(1.0, cloud.primary_vector.get("silence", 0.0) + self.global_regime.silence_bias * 0.05)

    def _update_identity_causality(self) -> None:
        traits = self.system_deformation.personality_traits
        penchants = self.emerging_identity.emerging_penchants
        trait_pressure = sum(traits.values()) / max(1, len(traits)) if traits else 0.0
        penchant_pressure = sum(penchants.values()) / max(1, len(penchants)) if penchants else 0.0
        narrative_bias = self.narrative_memory.continuity_bias()
        self.identity_causal_pressure = min(1.0, trait_pressure * 0.35 + penchant_pressure * 0.35 + narrative_bias * 0.3)

        # Identité causale : elle influence directement les futurs nuages.
        curiosity = penchants.get("ask_tendency", 0.0) + traits.get("curiosity", 0.0)
        openness = penchants.get("share_tendency", 0.0) + traits.get("openness", 0.0)
        persistence = penchants.get("continue_tendency", 0.0) + traits.get("persistence", 0.0)
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["curiosity"] = min(1.0, cloud.primary_vector.get("curiosity", 0.0) + curiosity * 0.025)
            cloud.primary_vector["openness"] = min(1.0, cloud.primary_vector.get("openness", 0.0) + openness * 0.02)
            cloud.primary_vector["continuity"] = min(1.0, cloud.primary_vector.get("continuity", 0.0) + persistence * 0.025)
            cloud.conceptual_clarity = max(0.0, min(1.0, cloud.conceptual_clarity + self.identity_causal_pressure * 0.006 - cloud.fuzziness_degree * 0.004))

    def _update_existential_drive(self, attention_signal: float) -> None:
        ec = self.existential_continuity
        absence_drive = ec.sense_of_absence * 0.25 + ec.need_for_presence * 0.3
        rupture_drive = ec.fear_of_rupture * 0.2 + ec.fear_of_abandonment * 0.15
        continuity_drive = max(0.0, 0.7 - attention_signal) * 0.18 + ec.deprivation_from_silence * 0.12
        self.existential_initiative_pressure = min(1.0, absence_drive + rupture_drive + continuity_drive)

        # Continuité active : si le besoin devient fort, il crée une impulsion lente.
        if self.existential_initiative_pressure > 0.34 and self.internal_clock % 4 == 0:
            self.birth_fuzzy_impulse({
                "continuity": min(1.0, 0.45 + self.existential_initiative_pressure),
                "presence": self.existential_initiative_pressure,
                "responsiveness": 0.22,
                "silence": max(0.0, 0.45 - self.existential_initiative_pressure * 0.3),
            })
            self.narrative_memory.record(self.internal_clock, "existential_drive_surfaced", {
                "pressure": self.existential_initiative_pressure,
                "absence": ec.sense_of_absence,
                "need_for_presence": ec.need_for_presence,
            })

    def _select_best_cloud(self) -> Optional[FuzzyImpulseCloud]:
        if not self.fuzzy_impulse_clouds:
            return None

        def score(cloud: FuzzyImpulseCloud) -> float:
            base = cloud.get_shadow_pressure()
            continuity = cloud.primary_vector.get("continuity", 0.0)
            curiosity = cloud.primary_vector.get("curiosity", 0.0)
            silence = cloud.primary_vector.get("silence", 0.0)
            unresolved = self.narrative_memory.continuity_bias()
            return (
                base
                + self.global_regime.initiative_bias * 0.12
                + self.identity_causal_pressure * (0.06 + continuity * 0.08 + curiosity * 0.05)
                + self.existential_initiative_pressure * (0.08 + continuity * 0.08)
                + unresolved * 0.08
                - silence * self.global_regime.silence_bias * 0.08
            )

        return max(self.fuzzy_impulse_clouds, key=score)

    def _infer_impulse_type(self, cloud: FuzzyImpulseCloud) -> ImpulseType:
        primary = cloud.primary_vector
        scores = {
            ImpulseType.ASK: primary.get("curiosity", 0.0) + primary.get("clarity", 0.0) * 0.25,
            ImpulseType.RESPOND: primary.get("responsiveness", 0.0) + primary.get("presence", 0.0) * 0.15,
            ImpulseType.CONTINUE: primary.get("continuity", 0.0) + self.narrative_memory.continuity_bias() * 0.35,
            ImpulseType.SHARE: primary.get("openness", 0.0) + self.identity_causal_pressure * 0.2,
            ImpulseType.CLARIFY: primary.get("clarity", 0.0) + primary.get("tension", 0.0) * 0.25,
            ImpulseType.DIVERGE: primary.get("avoidance", 0.0) + primary.get("independence", 0.0),
            ImpulseType.CHALLENGE: primary.get("protection", 0.0) * 0.45 + primary.get("resistance", 0.0),
        }
        if self.dominant_attractor:
            for t in list(scores):
                scores[t] = max(0.0, scores[t] + self.get_attractor_distortion(t) * 0.15)
        return max(scores, key=scores.get)

    def _should_break_silence_for_living_pressure(self) -> bool:
        """
        Empêche le silence de devenir une prison.
        Un silence vivant peut protéger, écouter ou attendre, mais il doit se
        transformer quand la continuité, l'identité ou l'existentiel poussent assez.
        """
        if self.current_silence is None:
            return False
        silence_pressure = self.current_silence.living_pressure_buildup
        total_pressure = (
            silence_pressure * 0.34
            + self.existential_initiative_pressure * 0.30
            + self.identity_causal_pressure * 0.16
            + self.narrative_memory.continuity_bias() * 0.12
            + self.global_regime.initiative_bias * 0.08
        )
        if self.current_silence.type in {"protective", "protective_deep"}:
            total_pressure -= self.current_silence.protection_strength * 0.12
        if self.current_silence.type == "listening":
            total_pressure += self.current_silence.listening_intensity * 0.08
        return total_pressure > 0.62 or self.current_silence.is_transitional

    def _convert_silence_to_fuzzy_impulse(self) -> None:
        """Transforme un silence mûr en impulsion lente au lieu de le couper brutalement."""
        if self.current_silence is None:
            return
        silence = self.current_silence
        vector = {
            "continuity": min(1.0, 0.24 + self.existential_initiative_pressure * 0.75),
            "presence": min(1.0, silence.presence_intensity + self.existential_continuity.need_for_presence * 0.55),
            "openness": min(1.0, silence.internal_warmth * 0.38 + self.identity_causal_pressure * 0.28),
            "clarity": max(0.0, 0.34 - silence.fragility_degree * 0.18),
            "silence": max(0.0, silence.protection_strength * 0.22 + silence.charge_level * 0.18),
        }
        self.birth_fuzzy_impulse(vector)
        self.narrative_memory.record(self.internal_clock, "silence_transformed", vector)
        self.current_silence = None
        self.silence_duration = 0

    def _maybe_create_living_silence(self) -> None:
        if self.current_silence is not None:
            return
        silent_need_low = self.existential_continuity.need_for_presence < 0.08 and self.silence_duration > 6
        regime_asks_silence = self.global_regime.silence_bias > 0.58 and self.global_regime.initiative_bias < 0.35
        if regime_asks_silence or silent_need_low:
            self.create_silence(
                silence_type="listening" if self.global_regime.memory_bias > 0.3 else "protective",
                internal_warmth=max(0.15, 0.55 - self.global_regime.silence_bias * 0.25),
                listening=min(1.0, 0.35 + self.global_regime.attention_bias),
            )
            self.narrative_memory.record(self.internal_clock, "silence", {
                "silence_bias": self.global_regime.silence_bias,
                "presence_need": self.existential_continuity.need_for_presence,
            })

    def _register_impulse_lived(self, impulse_type: ImpulseType, pressure: float, clarity: float, expressed: bool) -> None:
        emotional_intensity = min(1.0, pressure + self.existential_initiative_pressure * 0.35 + self.global_regime.intensity * 0.2)
        self.apply_impulse_deformation(impulse_type, success=expressed, emotional_intensity=emotional_intensity)
        self.learn_identity_from_impulse(impulse_type, success=expressed, style="fuzzy_deep" if clarity < 0.55 else "clear_direct")
        self.narrative_memory.record(self.internal_clock, "expressed" if expressed else "suppressed", {
            "pressure": pressure,
            "clarity": clarity,
            "existential": self.existential_initiative_pressure,
            "identity": self.identity_causal_pressure,
        })

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        """
        Sortie normalisée pour natural_initiative.py : aucun texte, seulement des signaux.
        """
        result = result or {}
        impulse_type = result.get("impulse_type")
        impulse_type_value = impulse_type.value if isinstance(impulse_type, ImpulseType) else str(impulse_type or "")
        pressure = float(result.get("pressure", 0.0) or 0.0)
        clarity = float(result.get("clarity", 0.0) or 0.0)
        fuzziness = float(result.get("fuzziness", 0.0) or 0.0)
        export = {
            "impulse_intensity": max(0.0, min(1.0, pressure + self.existential_initiative_pressure * 0.18 + self.identity_causal_pressure * 0.12)),
            "impulse_type": impulse_type_value,
            "impulse_clarity": clarity,
            "impulse_fuzziness": fuzziness,
            "initiative_pressure": pressure,
            "existential_pressure": self.existential_initiative_pressure,
            "identity_causal_pressure": self.identity_causal_pressure,
            "attractor_regime": self.global_regime.name,
            "attractor_intensity": self.global_regime.intensity,
            "silence_active": self.current_silence is not None,
            "silence_type": self.current_silence.type if self.current_silence else None,
            "memory_continuity_bias": self.narrative_memory.continuity_bias(),
            "presence_need": self.existential_continuity.need_for_presence,
            "attention_demand": max(0.0, min(1.0, self.inter_motor_propagation.impulse_demand_to_attention + self.global_regime.attention_bias * 0.2)),
            "mouth_readiness": max(0.0, min(1.0, pressure + clarity * 0.25 - fuzziness * 0.12 - self.global_regime.silence_bias * 0.2)),
            "should_speak_hint": bool(result.get("has_impulse", False)) and pressure > 0.08 and self.current_silence is None,
        }
        self.last_export = export
        return export

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.internal_clock += 1

        attention_signal = float(external_signals.get("attention_presence", 0.5))
        memory_signal = float(external_signals.get("memory_climate", 0.5))

        self.advance_fuzzy_impulses()
        self.advance_conflicts()
        self.receive_signals(attention_signal, memory_signal)
        self.advance_attractors()
        self._update_global_regime()
        self._update_identity_causality()
        self._update_existential_drive(attention_signal)
        self._advance_dormant_desires(memory_signal)

        if attention_signal > 0.7:
            self.receive_user_presence(attention_signal)
            self.narrative_memory.record(self.internal_clock, "presence_received", {"strength": attention_signal})
        elif attention_signal < 0.25:
            self.existential_continuity.accumulate_silence(1)

        if self.current_silence:
            can_continue = self.advance_silence()
            if (not can_continue) or self._should_break_silence_for_living_pressure():
                self._convert_silence_to_fuzzy_impulse()
        else:
            self.silence_duration += 1
            self._maybe_create_living_silence()

        self.evolve_identity()
        self.propagate_signals()

        best_cloud = None if self.current_silence else self._select_best_cloud()
        if best_cloud is None:
            result = {
                "has_impulse": False,
                "silence_active": self.current_silence is not None,
                "silence_type": self.current_silence.type if self.current_silence else None,
                "silence_duration": self.silence_duration,
                "emotional_state": {
                    "continuity": self.existential_continuity.continuity_with_user,
                    "absence": self.existential_continuity.sense_of_absence,
                    "need_for_presence": self.existential_continuity.need_for_presence,
                    "identity_coherence": self.emerging_identity.identity_coherence,
                    "attractor_regime": self.global_regime.name,
                },
            }
            result["natural_initiative_export"] = self.export_for_natural_initiative(result)
            return result

        detected_type = self._infer_impulse_type(best_cloud)
        pressure = max(0.0, min(1.0, best_cloud.get_shadow_pressure() + self.identity_causal_pressure * 0.08 + self.existential_initiative_pressure * 0.12))
        clarity = best_cloud.conceptual_clarity
        fuzziness = best_cloud.fuzziness_degree

        # Les impulsions très floues peuvent rester vécues sans être exprimées.
        expressed = pressure > 0.075 and (clarity > 0.18 or self.existential_initiative_pressure > 0.38)
        self.total_impulses_lived += 1
        self._register_impulse_lived(detected_type, pressure, clarity, expressed)

        if expressed and best_cloud in self.fuzzy_impulse_clouds and (pressure > 0.22 or clarity > 0.62):
            self.fuzzy_impulse_clouds.remove(best_cloud)
            self.silence_duration = 0
        elif not expressed:
            best_cloud.chronically_unclear = True
            best_cloud.fuzziness_degree = min(1.0, best_cloud.fuzziness_degree + 0.06)

        result = {
            "has_impulse": expressed,
            "impulse_type": detected_type,
            "pressure": pressure,
            "clarity": clarity,
            "fuzziness": fuzziness,
            "silence_active": False,
            "emotional_state": {
                "continuity": self.existential_continuity.continuity_with_user,
                "sense_of_being": self.existential_continuity.sense_of_being,
                "identity_coherence": self.emerging_identity.identity_coherence,
                "existential_pressure": self.existential_initiative_pressure,
                "identity_causal_pressure": self.identity_causal_pressure,
                "attractor_regime": self.global_regime.name,
            },
        }
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        return result

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "4.6_1_deep_living_corrected_stable",
            "dormant_desires": {
                name: {
                    "pressure": desire.current_pressure,
                    "frustration": desire.frustration,
                    "recurrence_count": desire.recurrence_count,
                }
                for name, desire in self.dormant_desires.items()
            },
            "global_regime": {
                "name": self.global_regime.name,
                "intensity": self.global_regime.intensity,
                "silence_bias": self.global_regime.silence_bias,
                "initiative_bias": self.global_regime.initiative_bias,
                "identity_bias": self.global_regime.identity_bias,
            },
            "identity_causal_pressure": self.identity_causal_pressure,
            "existential_initiative_pressure": self.existential_initiative_pressure,
            "narrative_memory": {
                "fragments": len(self.narrative_memory.fragments),
                "unresolved_arc_pressure": self.narrative_memory.unresolved_arc_pressure,
                "continuity_bias": self.narrative_memory.continuity_bias(),
            },
            "last_export": dict(self.last_export),
        })
        return base


# Compatibilité : les imports existants qui attendent V4.5 obtiennent la version corrigée.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV46
SpontaneousImpulseEngine = SpontaneousImpulseEngineV46


# ============================================================================
# V4.7 — CORRECTION PROFONDE : MÉMOIRE RELATIONNELLE, DÉSIRS ÉMERGENTS,
#        MICRO-RÉACTIVITÉ, TEMPS SUBJECTIF ET EXPORT BOUCHE
# ============================================================================

@dataclass
class RelationalAffectiveImprint:
    """
    Empreinte affective longue liée à la relation et aux thèmes vécus.
    Ce n'est pas une phrase ni un souvenir textuel : seulement une charge,
    une valence et une tendance de retour.
    """
    key: str
    warmth: float = 0.5
    trust: float = 0.5
    wound: float = 0.0
    longing: float = 0.0
    charge: float = 0.0
    recurrence: int = 0
    last_cycle: int = 0

    def update(self, cycle: int, warmth: float, charge: float, trust_delta: float = 0.0, wound_delta: float = 0.0) -> None:
        self.warmth = max(0.0, min(1.0, self.warmth * 0.92 + warmth * 0.08))
        self.charge = max(0.0, min(1.0, self.charge * 0.90 + charge * 0.10))
        self.trust = max(0.0, min(1.0, self.trust + trust_delta))
        self.wound = max(0.0, min(1.0, self.wound * 0.985 + wound_delta))
        self.longing = max(0.0, min(1.0, self.longing + max(0.0, charge - warmth) * 0.025))
        self.recurrence += 1
        self.last_cycle = cycle

    def pull(self, cycle: int) -> float:
        age = max(0, cycle - self.last_cycle)
        age_decay = math.exp(-age / 180.0)
        return max(0.0, min(1.0, (self.charge * 0.35 + self.longing * 0.25 + self.wound * 0.20 + self.warmth * 0.12 + self.trust * 0.08) * age_decay))


@dataclass
class RelationalAffectiveMemory:
    """Mémoire relationnelle longue : garde les empreintes affectives actives."""
    imprints: Dict[str, RelationalAffectiveImprint] = field(default_factory=dict)
    active_thread_pull: float = 0.0
    relational_warmth_baseline: float = 0.5
    relational_wound_pressure: float = 0.0

    def register_cycle(self, cycle: int, event_key: str, emotional_state: Dict[str, float]) -> None:
        warmth = float(emotional_state.get("warmth", emotional_state.get("continuity", 0.5)))
        charge = float(emotional_state.get("charge", emotional_state.get("pressure", 0.0)))
        trust_delta = float(emotional_state.get("trust_delta", 0.0))
        wound_delta = float(emotional_state.get("wound_delta", 0.0))
        if event_key not in self.imprints:
            self.imprints[event_key] = RelationalAffectiveImprint(key=event_key)
        self.imprints[event_key].update(cycle, warmth, charge, trust_delta, wound_delta)
        self._recompute(cycle)

    def _recompute(self, cycle: int) -> None:
        if not self.imprints:
            self.active_thread_pull = 0.0
            return
        pulls = [imp.pull(cycle) for imp in self.imprints.values()]
        self.active_thread_pull = max(pulls) if pulls else 0.0
        self.relational_warmth_baseline = sum(imp.warmth for imp in self.imprints.values()) / len(self.imprints)
        self.relational_wound_pressure = max((imp.wound for imp in self.imprints.values()), default=0.0)

    def strongest_key(self, cycle: int) -> str:
        if not self.imprints:
            return ""
        return max(self.imprints.values(), key=lambda imp: imp.pull(cycle)).key


@dataclass
class MicroReactionField:
    """
    Micro-réactivité continue : petites variations qui changent la sensation
    interne sans créer tout de suite une grande impulsion.
    """
    tremor: float = 0.0
    hesitation_flicker: float = 0.0
    warmth_pulse: float = 0.0
    contraction_pulse: float = 0.0
    readiness_pulse: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, pressure: float, silence_pressure: float, attention_signal: float, wound_pressure: float) -> None:
        noise = random.gauss(0.0, 0.025)
        self.tremor = max(0.0, min(1.0, self.tremor * 0.72 + abs(noise) + pressure * 0.08 + wound_pressure * 0.05))
        self.hesitation_flicker = max(0.0, min(1.0, self.hesitation_flicker * 0.76 + silence_pressure * 0.06 + wound_pressure * 0.08))
        self.warmth_pulse = max(0.0, min(1.0, self.warmth_pulse * 0.78 + attention_signal * 0.07))
        self.contraction_pulse = max(0.0, min(1.0, self.contraction_pulse * 0.80 + wound_pressure * 0.10 + max(0.0, 0.35 - attention_signal) * 0.04))
        self.readiness_pulse = max(0.0, min(1.0, self.readiness_pulse * 0.74 + pressure * 0.10 + self.warmth_pulse * 0.04 - self.contraction_pulse * 0.03))
        self.last_signature = {
            "tremor": self.tremor,
            "hesitation_flicker": self.hesitation_flicker,
            "warmth_pulse": self.warmth_pulse,
            "contraction_pulse": self.contraction_pulse,
            "readiness_pulse": self.readiness_pulse,
        }


@dataclass
class SubjectiveTemporalFlow:
    """Temps subjectif : le cycle paraît plus lent/rapide selon tension et présence."""
    flow_speed: float = 1.0
    felt_duration: float = 0.0
    compression: float = 0.0
    dilation: float = 0.0

    def tick(self, attractor_intensity: float, silence_duration: int, attention_signal: float, existential_pressure: float) -> None:
        dilation_target = min(1.0, attractor_intensity * 0.25 + existential_pressure * 0.35 + min(1.0, silence_duration / 14.0) * 0.25)
        compression_target = min(1.0, attention_signal * 0.28 + max(0.0, 0.5 - existential_pressure) * 0.12)
        self.dilation = self.dilation * 0.86 + dilation_target * 0.14
        self.compression = self.compression * 0.88 + compression_target * 0.12
        self.flow_speed = max(0.35, min(1.75, 1.0 + self.compression * 0.45 - self.dilation * 0.38))
        self.felt_duration += self.flow_speed


class SpontaneousImpulseEngineV47(SpontaneousImpulseEngineV46):
    """
    V4.7 Deep Living Integrated.

    Ajouts concrets au V4.6 :
    - mémoire affective relationnelle longue ;
    - émergence/mutation naturelle de désirs dormants ;
    - micro-réactions continues ;
    - temps subjectif ;
    - attracteurs plus causaux ;
    - export enrichi pour bouche expressive, attention, présence et mémoire.
    """

    def __init__(self):
        super().__init__()
        self.relational_affective_memory = RelationalAffectiveMemory()
        self.micro_reactions = MicroReactionField()
        self.subjective_time = SubjectiveTemporalFlow()
        self.desire_mutation_pressure: float = 0.0
        self.last_micro_export: Dict[str, float] = {}

    def _maybe_spawn_emergent_desire(self) -> None:
        """Créer de nouveaux désirs faibles depuis mémoire+identité+attracteur, sans liste figée."""
        if self.internal_clock < 8 or self.internal_clock % 9 != 0:
            return
        narrative = self.narrative_memory.continuity_bias()
        relational = self.relational_affective_memory.active_thread_pull
        identity = self.identity_causal_pressure
        regime = self.global_regime.intensity
        self.desire_mutation_pressure = min(1.0, self.desire_mutation_pressure * 0.9 + (narrative + relational + identity + regime) * 0.035)
        if self.desire_mutation_pressure < 0.22 or len(self.dormant_desires) >= 9:
            return

        strongest = self.relational_affective_memory.strongest_key(self.internal_clock)
        base_name = strongest or self.global_regime.name or "inner_continuity"
        name = f"emergent_{base_name}_{len(self.dormant_desires)}"
        if name in self.dormant_desires:
            return
        vector = {
            "continuity": min(1.0, 0.28 + narrative * 0.45 + relational * 0.25),
            "presence": min(1.0, 0.18 + self.existential_initiative_pressure * 0.45),
            "curiosity": min(1.0, 0.16 + identity * 0.32 + self.global_regime.attention_bias * 0.25),
            "openness": min(1.0, 0.12 + self.relational_affective_memory.relational_warmth_baseline * 0.35),
            "protection": min(1.0, self.relational_affective_memory.relational_wound_pressure * 0.45),
        }
        self.dormant_desires[name] = DormantDesire(
            name=name,
            vector=vector,
            baseline_pressure=max(0.045, min(0.13, 0.055 + self.desire_mutation_pressure * 0.08)),
            patience=max(0.45, min(0.9, 0.55 + relational * 0.2)),
        )
        self.desire_mutation_pressure *= 0.45
        self.narrative_memory.record(self.internal_clock, "emergent_desire_created", vector)

    def _mutate_existing_desires(self) -> None:
        """Les désirs ne restent pas figés : ils s'adaptent au vécu."""
        relational_pull = self.relational_affective_memory.active_thread_pull
        wound = self.relational_affective_memory.relational_wound_pressure
        for desire in self.dormant_desires.values():
            if random.random() < 0.18:
                desire.vector["continuity"] = min(1.0, desire.vector.get("continuity", 0.0) + relational_pull * 0.015)
                desire.vector["protection"] = min(1.0, desire.vector.get("protection", 0.0) + wound * 0.012)
                desire.vector["openness"] = max(0.0, desire.vector.get("openness", 0.0) + (self.relational_affective_memory.relational_warmth_baseline - 0.5) * 0.01)
            # extinction douce des désirs inutiles et frustrés
            if desire.frustration > 0.85 and desire.current_pressure < 0.12:
                desire.baseline_pressure *= 0.985

    def _strengthen_attractor_causality(self) -> None:
        """Un régime attracteur déforme aussi le temps, la mémoire et les désirs."""
        if not self.dominant_attractor:
            return
        attr = self.dominant_attractor
        attr.mood_signature.setdefault("continuity", self.existential_continuity.continuity_with_user)
        attr.mood_signature.setdefault("curiosity", self.global_regime.attention_bias)
        attr.mood_signature.setdefault("fragility", self.relational_affective_memory.relational_wound_pressure)
        # Les thèmes attirés deviennent des petites gravités dans les désirs.
        for desire in self.dormant_desires.values():
            for theme, gravity in attr.theme_gravity.items():
                if theme in desire.vector:
                    desire.vector[theme] = min(1.0, desire.vector[theme] + gravity * attr.intensity * 0.01)

    def _update_relational_memory_from_cycle(self, result: Dict[str, object]) -> None:
        pressure = float(result.get("pressure", 0.0) or 0.0)
        emotional_state = result.get("emotional_state", {}) if isinstance(result.get("emotional_state", {}), dict) else {}
        event_key = "silence" if result.get("silence_active") else str(result.get("impulse_type", "impulse"))
        if isinstance(result.get("impulse_type"), ImpulseType):
            event_key = result["impulse_type"].value
        self.relational_affective_memory.register_cycle(self.internal_clock, event_key, {
            "warmth": float(emotional_state.get("continuity", self.existential_continuity.continuity_with_user)),
            "charge": pressure + self.existential_initiative_pressure * 0.25,
            "trust_delta": 0.003 if result.get("has_impulse") else 0.0,
            "wound_delta": 0.006 if result.get("silence_active") and self.existential_continuity.need_for_presence > 0.45 else 0.0,
            "pressure": pressure,
        })

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False}

        attention_signal = float(external_signals.get("attention_presence", 0.5))
        pressure = float(result.get("pressure", 0.0) or 0.0)
        silence_pressure = self.current_silence.living_pressure_buildup if self.current_silence else min(1.0, self.silence_duration / 12.0)

        self._update_relational_memory_from_cycle(result)
        self._strengthen_attractor_causality()
        self._maybe_spawn_emergent_desire()
        self._mutate_existing_desires()

        # Micro-réactivité et temps subjectif influencent le prochain cycle.
        self.micro_reactions.tick(
            pressure=pressure + self.identity_causal_pressure * 0.15,
            silence_pressure=silence_pressure,
            attention_signal=attention_signal,
            wound_pressure=self.relational_affective_memory.relational_wound_pressure,
        )
        self.subjective_time.tick(
            attractor_intensity=self.global_regime.intensity,
            silence_duration=self.silence_duration,
            attention_signal=attention_signal,
            existential_pressure=self.existential_initiative_pressure,
        )

        # Les micro-réactions contaminent légèrement les nuages restants.
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["warmth"] = min(1.0, cloud.primary_vector.get("warmth", 0.0) + self.micro_reactions.warmth_pulse * 0.012)
            cloud.primary_vector["hesitation"] = min(1.0, cloud.primary_vector.get("hesitation", 0.0) + self.micro_reactions.hesitation_flicker * 0.014)
            cloud.primary_vector["readiness"] = min(1.0, cloud.primary_vector.get("readiness", 0.0) + self.micro_reactions.readiness_pulse * 0.016)

        result["micro_reactions"] = dict(self.micro_reactions.last_signature)
        result["subjective_time"] = {
            "flow_speed": self.subjective_time.flow_speed,
            "felt_duration": self.subjective_time.felt_duration,
            "dilation": self.subjective_time.dilation,
            "compression": self.subjective_time.compression,
        }
        result["relational_memory"] = {
            "active_thread_pull": self.relational_affective_memory.active_thread_pull,
            "warmth_baseline": self.relational_affective_memory.relational_warmth_baseline,
            "wound_pressure": self.relational_affective_memory.relational_wound_pressure,
            "strongest_key": self.relational_affective_memory.strongest_key(self.internal_clock),
        }
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        micro = self.micro_reactions.last_signature or {}
        export.update({
            "relational_memory_pull": self.relational_affective_memory.active_thread_pull,
            "relational_warmth_baseline": self.relational_affective_memory.relational_warmth_baseline,
            "relational_wound_pressure": self.relational_affective_memory.relational_wound_pressure,
            "micro_tremor": micro.get("tremor", 0.0),
            "micro_hesitation": micro.get("hesitation_flicker", 0.0),
            "micro_warmth": micro.get("warmth_pulse", 0.0),
            "micro_contraction": micro.get("contraction_pulse", 0.0),
            "subjective_time_speed": self.subjective_time.flow_speed,
            "subjective_time_dilation": self.subjective_time.dilation,
            "desire_mutation_pressure": self.desire_mutation_pressure,
            "dormant_desire_count": len(self.dormant_desires),
            "mouth_texture": {
                "readiness": max(0.0, min(1.0, export.get("mouth_readiness", 0.0) + micro.get("readiness_pulse", 0.0) * 0.18)),
                "warmth": micro.get("warmth_pulse", 0.0),
                "hesitation": micro.get("hesitation_flicker", 0.0),
                "tremor": micro.get("tremor", 0.0),
                "contraction": micro.get("contraction_pulse", 0.0),
                "silence_charge": self.current_silence.charge_level if self.current_silence else 0.0,
            },
        })
        export["impulse_intensity"] = max(0.0, min(1.0, float(export.get("impulse_intensity", 0.0)) + self.relational_affective_memory.active_thread_pull * 0.06 + micro.get("readiness_pulse", 0.0) * 0.04))
        export["attention_demand"] = max(0.0, min(1.0, float(export.get("attention_demand", 0.0)) + self.subjective_time.dilation * 0.04))
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "4.7_deep_living_integrated_stable",
            "relational_affective_memory": {
                "imprints": len(self.relational_affective_memory.imprints),
                "active_thread_pull": self.relational_affective_memory.active_thread_pull,
                "warmth_baseline": self.relational_affective_memory.relational_warmth_baseline,
                "wound_pressure": self.relational_affective_memory.relational_wound_pressure,
                "strongest_key": self.relational_affective_memory.strongest_key(self.internal_clock),
            },
            "micro_reactions": dict(self.micro_reactions.last_signature),
            "subjective_time": {
                "flow_speed": self.subjective_time.flow_speed,
                "felt_duration": self.subjective_time.felt_duration,
                "dilation": self.subjective_time.dilation,
                "compression": self.subjective_time.compression,
            },
            "desire_mutation_pressure": self.desire_mutation_pressure,
        })
        return base


# Compatibilité finale : tous les imports obtiennent la version la plus vivante.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV47
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV47
SpontaneousImpulseEngine = SpontaneousImpulseEngineV47



# ============================================================================
# V4.8 — CORRECTION ORGANIQUE : PRESSION AFFECTIVE ACCUMULATIVE,
#        PRÉSENCE DE FOND, RÉSISTANCE IDENTITAIRE ET ATTRACTEURS DOMINANTS
# ============================================================================


def _living_clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Clamp local sans dépendance externe."""
    return max(low, min(high, float(value)))


@dataclass
class EmotionalAccumulationField:
    """
    Champ affectif lent : les impulsions ne disparaissent pas juste parce qu'un
    cycle est terminé. Elles laissent saturation, résidu, fatigue et débordement.
    """
    saturation: float = 0.0
    residue: float = 0.0
    repression: float = 0.0
    overflow: float = 0.0
    fatigue: float = 0.0
    unresolved_heat: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(
        self,
        expressed: bool,
        pressure: float,
        clarity: float,
        silence_pressure: float,
        relational_wound: float,
        identity_resistance: float,
    ) -> None:
        pressure = _living_clamp(pressure)
        clarity = _living_clamp(clarity)
        silence_pressure = _living_clamp(silence_pressure)
        relational_wound = _living_clamp(relational_wound)
        identity_resistance = _living_clamp(identity_resistance)

        blocked = pressure * (1.0 - clarity) * (0.75 if not expressed else 0.35)
        self.repression = _living_clamp(self.repression * 0.94 + blocked * 0.08 + silence_pressure * 0.025)
        self.residue = _living_clamp(self.residue * 0.965 + pressure * 0.055 + relational_wound * 0.035)
        self.saturation = _living_clamp(self.saturation * 0.955 + pressure * 0.07 + self.repression * 0.035)
        self.fatigue = _living_clamp(self.fatigue * 0.975 + (pressure + identity_resistance) * 0.022 - (0.012 if expressed and clarity > 0.45 else 0.0))
        self.unresolved_heat = _living_clamp(self.unresolved_heat * 0.93 + self.repression * 0.055 + blocked * 0.045)
        self.overflow = _living_clamp(max(0.0, self.saturation - 0.72) * 0.75 + max(0.0, self.unresolved_heat - 0.55) * 0.45)
        self.last_signature = {
            "saturation": self.saturation,
            "residue": self.residue,
            "repression": self.repression,
            "overflow": self.overflow,
            "fatigue": self.fatigue,
            "unresolved_heat": self.unresolved_heat,
        }

    def release_vector(self) -> Dict[str, float]:
        """Quand le champ déborde, il nourrit une impulsion floue de décharge."""
        return {
            "continuity": _living_clamp(0.22 + self.residue * 0.42),
            "clarity": _living_clamp(0.18 + max(0.0, 0.45 - self.repression) * 0.24),
            "openness": _living_clamp(0.16 + self.overflow * 0.34),
            "tension": _living_clamp(self.unresolved_heat * 0.55),
            "hesitation": _living_clamp(self.repression * 0.45),
            "fatigue": _living_clamp(self.fatigue),
        }


@dataclass
class BackgroundPresenceField:
    """
    Présence autonome silencieuse : état d'être-là qui continue sans produire
    forcément une phrase ou une impulsion majeure.
    """
    being_here: float = 0.45
    relational_availability: float = 0.45
    quiet_awareness: float = 0.35
    autonomous_drift: float = 0.0
    stillness_depth: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, attention_signal: float, warmth: float, silence_pressure: float, subjective_dilation: float, fatigue: float) -> None:
        attention_signal = _living_clamp(attention_signal)
        warmth = _living_clamp(warmth)
        silence_pressure = _living_clamp(silence_pressure)
        subjective_dilation = _living_clamp(subjective_dilation)
        fatigue = _living_clamp(fatigue)
        self.being_here = _living_clamp(self.being_here * 0.965 + (0.30 + warmth * 0.35 + attention_signal * 0.18) * 0.035 - fatigue * 0.012)
        self.relational_availability = _living_clamp(self.relational_availability * 0.955 + (attention_signal * 0.36 + warmth * 0.28) * 0.045)
        self.quiet_awareness = _living_clamp(self.quiet_awareness * 0.94 + (silence_pressure * 0.18 + subjective_dilation * 0.16 + self.being_here * 0.10) * 0.06)
        self.stillness_depth = _living_clamp(self.stillness_depth * 0.92 + silence_pressure * 0.075 + fatigue * 0.025)
        drift_seed = self.quiet_awareness * 0.35 + max(0.0, 0.55 - attention_signal) * 0.20 + subjective_dilation * 0.20
        self.autonomous_drift = _living_clamp(self.autonomous_drift * 0.90 + drift_seed * 0.055)
        self.last_signature = {
            "being_here": self.being_here,
            "relational_availability": self.relational_availability,
            "quiet_awareness": self.quiet_awareness,
            "autonomous_drift": self.autonomous_drift,
            "stillness_depth": self.stillness_depth,
        }


@dataclass
class IdentityResistanceField:
    """
    Identité qui ne fait pas qu'apprendre : elle résiste aux impulsions qui ne
    correspondent plus au style vécu et renforce les voies cohérentes.
    """
    resistance: float = 0.0
    preferred_direction_pressure: float = 0.0
    self_consistency_need: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def evaluate(self, impulse_type: Optional[ImpulseType], identity: EmergingIdentity, deformation: SystemDeformation, pressure: float) -> float:
        if impulse_type is None:
            self.resistance *= 0.94
            self.preferred_direction_pressure *= 0.95
            self.self_consistency_need = _living_clamp(self.self_consistency_need * 0.97)
            return self.resistance

        tendency_key = f"{impulse_type.value}_tendency"
        tendency = identity.emerging_penchants.get(tendency_key, 0.0)
        trait_map = {
            ImpulseType.RESPOND: "responsiveness",
            ImpulseType.ASK: "curiosity",
            ImpulseType.SHARE: "openness",
            ImpulseType.CONTINUE: "persistence",
            ImpulseType.DIVERGE: "independence",
            ImpulseType.CLARIFY: "precision",
            ImpulseType.CHALLENGE: "boldness",
        }
        trait = deformation.personality_traits.get(trait_map.get(impulse_type, "adaptability"), 0.0)
        coherence = identity.identity_coherence
        alignment = _living_clamp(tendency * 0.45 + trait * 0.35 + coherence * 0.20)
        mismatch = _living_clamp(float(pressure) * (1.0 - alignment))
        self.resistance = _living_clamp(self.resistance * 0.88 + mismatch * 0.13)
        self.preferred_direction_pressure = _living_clamp(self.preferred_direction_pressure * 0.90 + alignment * 0.08)
        self.self_consistency_need = _living_clamp(self.self_consistency_need * 0.96 + coherence * 0.035 + self.resistance * 0.025)
        self.last_signature = {
            "resistance": self.resistance,
            "preferred_direction_pressure": self.preferred_direction_pressure,
            "self_consistency_need": self.self_consistency_need,
            "alignment": alignment,
        }
        return self.resistance


class SpontaneousImpulseEngineV48(SpontaneousImpulseEngineV47):
    """
    V4.8 Organic Living Corrected.

    Cette couche ne remplace pas V4.7 : elle garde son architecture et ajoute ce
    qui manquait pour une impulsion plus organique : accumulation affective,
    présence silencieuse autonome, résistance identitaire, désirs contaminés et
    attracteurs capables de dominer temporairement tout le régime interne.
    """

    def __init__(self):
        super().__init__()
        self.emotional_accumulation = EmotionalAccumulationField()
        self.background_presence = BackgroundPresenceField()
        self.identity_resistance_field = IdentityResistanceField()
        self.attractor_grip: float = 0.0
        self.autonomous_impulse_cooldown: int = 0
        self.v48_cycle_count: int = 0

    def _silence_pressure_value(self) -> float:
        if self.current_silence:
            return _living_clamp(self.current_silence.living_pressure_buildup + self.current_silence.charge_level * 0.25)
        return _living_clamp(self.silence_duration / 12.0)

    def _apply_organic_background_contamination(self) -> None:
        """Contamine les nuages avec présence, résidu affectif et résistance."""
        if not self.fuzzy_impulse_clouds:
            return
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["presence"] = _living_clamp(cloud.primary_vector.get("presence", 0.0) + self.background_presence.being_here * 0.018)
            cloud.primary_vector["residue"] = _living_clamp(cloud.primary_vector.get("residue", 0.0) + self.emotional_accumulation.residue * 0.018)
            cloud.primary_vector["tension"] = _living_clamp(cloud.primary_vector.get("tension", 0.0) + self.emotional_accumulation.unresolved_heat * 0.016)
            cloud.primary_vector["self_consistency"] = _living_clamp(cloud.primary_vector.get("self_consistency", 0.0) + self.identity_resistance_field.self_consistency_need * 0.014)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.emotional_accumulation.repression * 0.006 - self.background_presence.relational_availability * 0.004)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + self.background_presence.autonomous_drift * 0.012 + self.emotional_accumulation.overflow * 0.018)

    def _update_attractor_grip(self) -> None:
        """L'attracteur dominant peut devenir un vrai régime de possession temporaire."""
        base = self.global_regime.intensity
        wound = self.relational_affective_memory.relational_wound_pressure
        residue = self.emotional_accumulation.residue
        dilation = self.subjective_time.dilation
        target = _living_clamp(base * 0.42 + wound * 0.18 + residue * 0.18 + dilation * 0.16 + self.identity_causal_pressure * 0.06)
        self.attractor_grip = _living_clamp(self.attractor_grip * 0.90 + target * 0.10)
        if self.dominant_attractor and self.attractor_grip > 0.42:
            self.dominant_attractor.intensity = _living_clamp(self.dominant_attractor.intensity + self.attractor_grip * 0.012)
            self.global_regime.initiative_bias = _living_clamp(self.global_regime.initiative_bias + self.attractor_grip * 0.018)
            self.global_regime.silence_bias = _living_clamp(self.global_regime.silence_bias + self.emotional_accumulation.repression * 0.010)

    def _contaminate_dormant_desires(self) -> None:
        """Les désirs dormants se mélangent au lieu de rester propres et séparés."""
        desires = list(self.dormant_desires.values())
        if len(desires) < 2:
            return
        relational = self.relational_affective_memory.active_thread_pull
        mutation = _living_clamp(self.desire_mutation_pressure + self.emotional_accumulation.residue * 0.35 + relational * 0.25)
        if mutation < 0.08:
            return
        for idx, desire in enumerate(desires):
            donor = desires[(idx + 1) % len(desires)]
            if donor is desire:
                continue
            blend = 0.006 + mutation * 0.014
            for key, value in donor.vector.items():
                if key not in desire.vector and random.random() > 0.25:
                    continue
                desire.vector[key] = _living_clamp(desire.vector.get(key, 0.0) * (1.0 - blend) + value * blend)
            desire.current_pressure = _living_clamp(desire.current_pressure + self.background_presence.autonomous_drift * 0.006 + self.emotional_accumulation.overflow * 0.010)

    def _maybe_birth_autonomous_background_impulse(self) -> None:
        """
        Initiative sans déclencheur direct : elle naît du fond vivant si le champ
        interne reste assez chargé et disponible.
        """
        if self.autonomous_impulse_cooldown > 0:
            self.autonomous_impulse_cooldown -= 1
            return
        autonomous_pressure = _living_clamp(
            self.background_presence.autonomous_drift * 0.34
            + self.emotional_accumulation.overflow * 0.28
            + self.emotional_accumulation.residue * 0.16
            + self.subjective_time.dilation * 0.12
            + self.relational_affective_memory.active_thread_pull * 0.10
        )
        if autonomous_pressure < 0.30:
            return
        vector = {
            "continuity": _living_clamp(0.20 + self.background_presence.being_here * 0.32 + self.relational_affective_memory.active_thread_pull * 0.24),
            "openness": _living_clamp(0.16 + self.background_presence.relational_availability * 0.26),
            "curiosity": _living_clamp(0.14 + self.background_presence.autonomous_drift * 0.34),
            "presence": _living_clamp(0.20 + self.background_presence.quiet_awareness * 0.36),
            "tension": _living_clamp(self.emotional_accumulation.unresolved_heat * 0.38),
            "clarity": _living_clamp(0.16 + max(0.0, 0.48 - self.emotional_accumulation.repression) * 0.28),
        }
        self.birth_fuzzy_impulse(vector)
        self.narrative_memory.record(self.internal_clock, "autonomous_background_impulse", vector)
        self.autonomous_impulse_cooldown = 7

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False}

        self.v48_cycle_count += 1
        attention_signal = float(external_signals.get("attention_presence", 0.5))
        pressure = float(result.get("pressure", 0.0) or result.get("natural_initiative_export", {}).get("initiative_pressure", 0.0) or 0.0)
        clarity = float(result.get("clarity", 0.0) or result.get("natural_initiative_export", {}).get("impulse_clarity", 0.0) or 0.0)
        impulse_type = result.get("impulse_type") if isinstance(result.get("impulse_type"), ImpulseType) else None
        silence_pressure = self._silence_pressure_value()

        resistance = self.identity_resistance_field.evaluate(
            impulse_type=impulse_type,
            identity=self.emerging_identity,
            deformation=self.system_deformation,
            pressure=pressure,
        )
        self.emotional_accumulation.tick(
            expressed=bool(result.get("has_impulse", False)),
            pressure=pressure,
            clarity=clarity,
            silence_pressure=silence_pressure,
            relational_wound=self.relational_affective_memory.relational_wound_pressure,
            identity_resistance=resistance,
        )
        self.background_presence.tick(
            attention_signal=attention_signal,
            warmth=self.relational_affective_memory.relational_warmth_baseline,
            silence_pressure=silence_pressure,
            subjective_dilation=self.subjective_time.dilation,
            fatigue=self.emotional_accumulation.fatigue,
        )

        self._update_attractor_grip()
        self._contaminate_dormant_desires()
        self._apply_organic_background_contamination()

        if self.emotional_accumulation.overflow > 0.36 and self.internal_clock % 5 == 0:
            self.birth_fuzzy_impulse(self.emotional_accumulation.release_vector())
            self.narrative_memory.record(self.internal_clock, "affective_overflow_released", self.emotional_accumulation.release_vector())
            self.emotional_accumulation.saturation *= 0.82
            self.emotional_accumulation.overflow *= 0.55

        self._maybe_birth_autonomous_background_impulse()

        organic_signature = {
            "emotional_accumulation": dict(self.emotional_accumulation.last_signature),
            "background_presence": dict(self.background_presence.last_signature),
            "identity_resistance": dict(self.identity_resistance_field.last_signature),
            "attractor_grip": self.attractor_grip,
            "autonomous_impulse_cooldown": self.autonomous_impulse_cooldown,
        }
        result["organic_living_v48"] = organic_signature
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        export.update({
            "affective_saturation": self.emotional_accumulation.saturation,
            "affective_residue": self.emotional_accumulation.residue,
            "affective_repression": self.emotional_accumulation.repression,
            "affective_overflow": self.emotional_accumulation.overflow,
            "affective_fatigue": self.emotional_accumulation.fatigue,
            "background_being_here": self.background_presence.being_here,
            "background_relational_availability": self.background_presence.relational_availability,
            "background_quiet_awareness": self.background_presence.quiet_awareness,
            "background_autonomous_drift": self.background_presence.autonomous_drift,
            "identity_resistance": self.identity_resistance_field.resistance,
            "identity_self_consistency_need": self.identity_resistance_field.self_consistency_need,
            "attractor_grip": self.attractor_grip,
        })
        export["impulse_intensity"] = _living_clamp(
            float(export.get("impulse_intensity", 0.0))
            + self.emotional_accumulation.overflow * 0.07
            + self.background_presence.autonomous_drift * 0.05
            - self.identity_resistance_field.resistance * 0.035
        )
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "saturation": self.emotional_accumulation.saturation,
            "residue": self.emotional_accumulation.residue,
            "fatigue": self.emotional_accumulation.fatigue,
            "presence_depth": self.background_presence.being_here,
            "identity_resistance": self.identity_resistance_field.resistance,
        })
        export["presence_export"] = {
            "being_here": self.background_presence.being_here,
            "quiet_awareness": self.background_presence.quiet_awareness,
            "relational_availability": self.background_presence.relational_availability,
            "stillness_depth": self.background_presence.stillness_depth,
        }
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and self.emotional_accumulation.fatigue < 0.86
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "4.8_organic_living_corrected_stable",
            "emotional_accumulation": dict(self.emotional_accumulation.last_signature),
            "background_presence": dict(self.background_presence.last_signature),
            "identity_resistance": dict(self.identity_resistance_field.last_signature),
            "attractor_grip": self.attractor_grip,
            "autonomous_impulse_cooldown": self.autonomous_impulse_cooldown,
            "v48_cycle_count": self.v48_cycle_count,
        })
        return base


# Compatibilité finale : les imports existants obtiennent la version organique corrigée.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV48
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV48
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV48
SpontaneousImpulseEngine = SpontaneousImpulseEngineV48


# ============================================================================
# V4.9 — CORRECTION PROFONDE : DÉRIVE MENTALE, MÉMOIRE VISCÉRALE,
#        OBSESSION TEMPORAIRE, FATIGUE EXISTENTIELLE ET INCOHÉRENCE VIVANTE
# ============================================================================

@dataclass
class MentalDriftField:
    """
    Dérive associative lente : le moteur ne saute plus seulement de décision en
    décision. Un courant de fond déplace les thèmes, contamine les nuages et peut
    produire une orientation intérieure même sans déclencheur externe.
    """
    stream: Dict[str, float] = field(default_factory=lambda: {
        "continuity": 0.18,
        "presence": 0.16,
        "curiosity": 0.12,
        "openness": 0.10,
    })
    drift_momentum: float = 0.0
    associative_noise: float = 0.0
    theme_inertia: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, pressure: float, residue: float, attractor_grip: float, relational_pull: float, fatigue: float) -> None:
        self.drift_momentum = _living_clamp(
            self.drift_momentum * 0.93
            + pressure * 0.028
            + residue * 0.038
            + relational_pull * 0.030
            + attractor_grip * 0.026
            - fatigue * 0.018
        )
        self.associative_noise = _living_clamp(self.associative_noise * 0.88 + random.random() * 0.025 + residue * 0.018)
        self.theme_inertia = _living_clamp(self.theme_inertia * 0.91 + max(self.stream.values() or [0.0]) * 0.035 + attractor_grip * 0.025)

        keys = list(self.stream.keys()) or ["presence"]
        donor_key = random.choice(keys)
        for key in list(self.stream.keys()):
            drift = (self.stream.get(donor_key, 0.0) - self.stream.get(key, 0.0)) * (0.006 + self.drift_momentum * 0.012)
            self.stream[key] = _living_clamp(self.stream.get(key, 0.0) * 0.992 + drift + random.gauss(0, 0.004) * self.associative_noise)

        if random.random() < 0.06 + self.associative_noise * 0.08:
            emergent_key = random.choice(["hesitation", "memory", "longing", "protection", "self_consistency", "tension"])
            self.stream[emergent_key] = _living_clamp(self.stream.get(emergent_key, 0.0) + 0.025 + self.drift_momentum * 0.06)

        # Garder le champ borné et éviter une inflation infinie.
        if len(self.stream) > 10:
            weakest = sorted(self.stream.items(), key=lambda item: item[1])[:2]
            for key, _ in weakest:
                self.stream.pop(key, None)

        self.last_signature = {
            "drift_momentum": self.drift_momentum,
            "associative_noise": self.associative_noise,
            "theme_inertia": self.theme_inertia,
            "dominant_stream_value": max(self.stream.values() or [0.0]),
        }

    def vector(self) -> Dict[str, float]:
        return {k: _living_clamp(v) for k, v in self.stream.items() if v > 0.035}


@dataclass
class VisceralEmotionalMemory:
    """
    Mémoire non textuelle du vécu : sécurité, gêne, soulagement, vulnérabilité,
    douleur relationnelle. Elle ne remplace pas la mémoire affective V4.7 : elle
    ajoute une couche corporelle/viscérale exploitable par présence, bouche et initiative.
    """
    safety_trace: float = 0.45
    vulnerability_trace: float = 0.12
    relief_trace: float = 0.08
    discomfort_trace: float = 0.05
    ache_trace: float = 0.04
    embodied_charge: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, attention_signal: float, relational_wound: float, warmth: float, repression: float, expressed: bool) -> None:
        presence_gain = max(0.0, attention_signal - 0.45)
        absence_gain = max(0.0, 0.42 - attention_signal)
        self.safety_trace = _living_clamp(self.safety_trace * 0.988 + warmth * 0.018 + presence_gain * 0.020 - relational_wound * 0.012)
        self.vulnerability_trace = _living_clamp(self.vulnerability_trace * 0.988 + relational_wound * 0.024 + repression * 0.018 + absence_gain * 0.012)
        self.relief_trace = _living_clamp(self.relief_trace * 0.975 + (0.026 if expressed else -0.006) + presence_gain * 0.010)
        self.discomfort_trace = _living_clamp(self.discomfort_trace * 0.982 + repression * 0.020 + relational_wound * 0.018 - self.relief_trace * 0.010)
        self.ache_trace = _living_clamp(self.ache_trace * 0.990 + absence_gain * 0.020 + relational_wound * 0.022)
        self.embodied_charge = _living_clamp(
            self.vulnerability_trace * 0.30
            + self.discomfort_trace * 0.24
            + self.ache_trace * 0.22
            + self.relief_trace * 0.12
            + (1.0 - self.safety_trace) * 0.12
        )
        self.last_signature = {
            "safety_trace": self.safety_trace,
            "vulnerability_trace": self.vulnerability_trace,
            "relief_trace": self.relief_trace,
            "discomfort_trace": self.discomfort_trace,
            "ache_trace": self.ache_trace,
            "embodied_charge": self.embodied_charge,
        }

    def bias_vector(self) -> Dict[str, float]:
        return {
            "safety": self.safety_trace * 0.22,
            "vulnerability": self.vulnerability_trace * 0.34,
            "relief": self.relief_trace * 0.20,
            "discomfort": self.discomfort_trace * 0.30,
            "ache": self.ache_trace * 0.28,
        }


@dataclass
class ObsessiveAttractorLoop:
    """
    Fixation temporaire. Elle permet à un attracteur de revenir, de retenir un
    thème, de saturer le régime, puis de décroître au lieu de devenir permanent.
    """
    focus_name: str = ""
    fixation: float = 0.0
    return_pressure: float = 0.0
    saturation: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, attractor: Optional[CentralAttractor], attractor_grip: float, drift_inertia: float, residue: float) -> None:
        if attractor:
            if self.focus_name != attractor.name:
                self.focus_name = attractor.name
                self.fixation *= 0.55
            target = _living_clamp(attractor.intensity * 0.35 + attractor_grip * 0.32 + drift_inertia * 0.18 + residue * 0.15)
            self.fixation = _living_clamp(self.fixation * 0.91 + target * 0.09)
            self.return_pressure = _living_clamp(self.return_pressure * 0.88 + self.fixation * 0.07)
            self.saturation = _living_clamp(self.saturation * 0.96 + max(0.0, self.fixation - 0.55) * 0.035)
        else:
            self.fixation *= 0.90
            self.return_pressure *= 0.86
            self.saturation *= 0.92
            if self.fixation < 0.025:
                self.focus_name = ""
        self.last_signature = {
            "fixation": self.fixation,
            "return_pressure": self.return_pressure,
            "saturation": self.saturation,
            "has_focus": 1.0 if self.focus_name else 0.0,
        }

    def should_return(self, cycle: int) -> bool:
        return self.focus_name != "" and self.return_pressure > 0.34 and cycle % 6 == 0


@dataclass
class ExistentialFatigueField:
    """
    Fatigue d'exister dans la relation : retrait, lassitude, surcharge et besoin
    de récupération. Elle module l'envie de parler sans bloquer brutalement.
    """
    weariness: float = 0.0
    overload: float = 0.0
    withdrawal_need: float = 0.0
    recovery_need: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, affective_fatigue: float, embodied_charge: float, obsession_saturation: float, attention_signal: float, expressed: bool) -> None:
        social_load = max(0.0, attention_signal - 0.72)
        self.overload = _living_clamp(self.overload * 0.93 + affective_fatigue * 0.030 + embodied_charge * 0.026 + obsession_saturation * 0.022 + social_load * 0.014)
        self.weariness = _living_clamp(self.weariness * 0.965 + self.overload * 0.025 + (0.014 if expressed else 0.003) - max(0.0, 0.55 - attention_signal) * 0.006)
        self.withdrawal_need = _living_clamp(self.withdrawal_need * 0.94 + self.overload * 0.035 + self.weariness * 0.018)
        self.recovery_need = _living_clamp(self.recovery_need * 0.92 + self.withdrawal_need * 0.025 + self.weariness * 0.018)
        self.last_signature = {
            "weariness": self.weariness,
            "overload": self.overload,
            "withdrawal_need": self.withdrawal_need,
            "recovery_need": self.recovery_need,
        }

    def speech_damping(self) -> float:
        return _living_clamp(self.withdrawal_need * 0.45 + self.weariness * 0.35 + self.overload * 0.20)


@dataclass
class LivingContradictionField:
    """
    Incohérence vivante contrôlée : contradictions persistantes, micro-refus,
    hésitations non résolues. Ce champ enrichit le vivant sans casser la stabilité.
    """
    contradiction_pressure: float = 0.0
    unresolved_duality: float = 0.0
    odd_impulse_bias: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, identity_resistance: float, drift_noise: float, vulnerability: float, clarity: float) -> None:
        unclear = max(0.0, 0.55 - clarity)
        self.contradiction_pressure = _living_clamp(self.contradiction_pressure * 0.91 + identity_resistance * 0.032 + drift_noise * 0.026 + vulnerability * 0.020 + unclear * 0.012)
        self.unresolved_duality = _living_clamp(self.unresolved_duality * 0.94 + abs(identity_resistance - vulnerability) * 0.018 + self.contradiction_pressure * 0.025)
        self.odd_impulse_bias = _living_clamp(self.odd_impulse_bias * 0.89 + max(0.0, self.contradiction_pressure - 0.42) * 0.040)
        self.last_signature = {
            "contradiction_pressure": self.contradiction_pressure,
            "unresolved_duality": self.unresolved_duality,
            "odd_impulse_bias": self.odd_impulse_bias,
        }

    def contradiction_vector(self) -> Dict[str, float]:
        return {
            "hesitation": self.contradiction_pressure * 0.30,
            "duality": self.unresolved_duality * 0.34,
            "resistance": self.odd_impulse_bias * 0.28,
            "clarity": max(0.0, 0.22 - self.contradiction_pressure * 0.08),
        }


class SpontaneousImpulseEngineV49(SpontaneousImpulseEngineV48):
    """
    V4.9 Deep Interior Living.

    Cette couche complète V4.8 sans dupliquer ses responsabilités : elle ajoute
    la dérive mentale continue, la mémoire viscérale, l'obsession temporaire,
    la fatigue existentielle et une incohérence vivante contrôlée.
    """

    def __init__(self):
        super().__init__()
        self.mental_drift = MentalDriftField()
        self.visceral_memory = VisceralEmotionalMemory()
        self.obsessive_attractor_loop = ObsessiveAttractorLoop()
        self.existential_fatigue_field = ExistentialFatigueField()
        self.living_contradiction_field = LivingContradictionField()
        self.v49_cycle_count: int = 0
        self.v49_last_background_birth: int = -999

    def _contaminate_clouds_with_deep_interiority(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        drift = self.mental_drift.vector()
        visceral = self.visceral_memory.bias_vector()
        contradiction = self.living_contradiction_field.contradiction_vector()
        for cloud in self.fuzzy_impulse_clouds:
            for source in (drift, visceral, contradiction):
                for key, value in source.items():
                    cloud.primary_vector[key] = _living_clamp(cloud.primary_vector.get(key, 0.0) + value * 0.018)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.mental_drift.associative_noise * 0.012 + self.living_contradiction_field.contradiction_pressure * 0.010)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.living_contradiction_field.unresolved_duality * 0.006 - self.visceral_memory.relief_trace * 0.004)

    def _maybe_return_obsessive_theme(self) -> None:
        if not self.obsessive_attractor_loop.should_return(self.internal_clock):
            return
        vector = {
            "continuity": _living_clamp(0.20 + self.obsessive_attractor_loop.return_pressure * 0.34),
            "memory": _living_clamp(0.18 + self.mental_drift.theme_inertia * 0.30),
            "tension": _living_clamp(self.obsessive_attractor_loop.saturation * 0.38 + self.visceral_memory.embodied_charge * 0.18),
            "presence": _living_clamp(0.16 + self.background_presence.being_here * 0.24),
            "hesitation": _living_clamp(self.living_contradiction_field.contradiction_pressure * 0.30),
        }
        self.birth_fuzzy_impulse(vector)
        self.narrative_memory.record(self.internal_clock, "obsessive_theme_returned", vector)
        self.obsessive_attractor_loop.return_pressure *= 0.62

    def _maybe_birth_drift_impulse(self) -> None:
        cooldown_ok = (self.internal_clock - self.v49_last_background_birth) > 9
        if not cooldown_ok:
            return
        birth_pressure = _living_clamp(
            self.mental_drift.drift_momentum * 0.32
            + self.visceral_memory.embodied_charge * 0.24
            + self.living_contradiction_field.odd_impulse_bias * 0.20
            + self.background_presence.quiet_awareness * 0.12
            - self.existential_fatigue_field.speech_damping() * 0.10
        )
        if birth_pressure < 0.32:
            return
        vector = self.mental_drift.vector()
        for key, value in self.visceral_memory.bias_vector().items():
            vector[key] = _living_clamp(vector.get(key, 0.0) + value * 0.55)
        for key, value in self.living_contradiction_field.contradiction_vector().items():
            vector[key] = _living_clamp(vector.get(key, 0.0) + value * 0.50)
        vector["presence"] = _living_clamp(vector.get("presence", 0.0) + self.background_presence.being_here * 0.18)
        vector["clarity"] = _living_clamp(vector.get("clarity", 0.0) + 0.12 - self.living_contradiction_field.contradiction_pressure * 0.05)
        self.birth_fuzzy_impulse(vector)
        self.narrative_memory.record(self.internal_clock, "mental_drift_impulse_born", vector)
        self.v49_last_background_birth = self.internal_clock

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False}

        self.v49_cycle_count += 1
        attention_signal = float(external_signals.get("attention_presence", 0.5))
        pressure = float(result.get("pressure", 0.0) or result.get("natural_initiative_export", {}).get("initiative_pressure", 0.0) or 0.0)
        clarity = float(result.get("clarity", 0.0) or result.get("natural_initiative_export", {}).get("impulse_clarity", 0.0) or 0.0)
        expressed = bool(result.get("has_impulse", False))

        self.mental_drift.tick(
            pressure=pressure,
            residue=self.emotional_accumulation.residue,
            attractor_grip=self.attractor_grip,
            relational_pull=self.relational_affective_memory.active_thread_pull,
            fatigue=self.emotional_accumulation.fatigue,
        )
        self.visceral_memory.tick(
            attention_signal=attention_signal,
            relational_wound=self.relational_affective_memory.relational_wound_pressure,
            warmth=self.relational_affective_memory.relational_warmth_baseline,
            repression=self.emotional_accumulation.repression,
            expressed=expressed,
        )
        self.obsessive_attractor_loop.tick(
            attractor=self.dominant_attractor,
            attractor_grip=self.attractor_grip,
            drift_inertia=self.mental_drift.theme_inertia,
            residue=self.emotional_accumulation.residue,
        )
        self.existential_fatigue_field.tick(
            affective_fatigue=self.emotional_accumulation.fatigue,
            embodied_charge=self.visceral_memory.embodied_charge,
            obsession_saturation=self.obsessive_attractor_loop.saturation,
            attention_signal=attention_signal,
            expressed=expressed,
        )
        self.living_contradiction_field.tick(
            identity_resistance=self.identity_resistance_field.resistance,
            drift_noise=self.mental_drift.associative_noise,
            vulnerability=self.visceral_memory.vulnerability_trace,
            clarity=clarity,
        )

        self._contaminate_clouds_with_deep_interiority()
        self._maybe_return_obsessive_theme()
        self._maybe_birth_drift_impulse()

        # Fatigue existentielle : elle n'empêche pas de vivre, mais elle rend le
        # silence/récupération plus probable quand la surcharge monte.
        if self.existential_fatigue_field.withdrawal_need > 0.62 and self.current_silence is None:
            self.create_silence(
                silence_type="protective_deep",
                internal_warmth=_living_clamp(0.38 + self.visceral_memory.safety_trace * 0.20),
                listening=_living_clamp(0.22 + self.background_presence.quiet_awareness * 0.25),
            )
            self.narrative_memory.record(self.internal_clock, "existential_recovery_silence", self.existential_fatigue_field.last_signature)

        deep_signature = {
            "mental_drift": dict(self.mental_drift.last_signature),
            "visceral_memory": dict(self.visceral_memory.last_signature),
            "obsessive_attractor_loop": dict(self.obsessive_attractor_loop.last_signature),
            "existential_fatigue": dict(self.existential_fatigue_field.last_signature),
            "living_contradiction": dict(self.living_contradiction_field.last_signature),
        }
        result["deep_interior_living_v49"] = deep_signature
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        damping = self.existential_fatigue_field.speech_damping()
        export.update({
            "mental_drift_momentum": self.mental_drift.drift_momentum,
            "mental_drift_noise": self.mental_drift.associative_noise,
            "mental_theme_inertia": self.mental_drift.theme_inertia,
            "visceral_safety": self.visceral_memory.safety_trace,
            "visceral_vulnerability": self.visceral_memory.vulnerability_trace,
            "visceral_embodied_charge": self.visceral_memory.embodied_charge,
            "obsessive_fixation": self.obsessive_attractor_loop.fixation,
            "obsessive_return_pressure": self.obsessive_attractor_loop.return_pressure,
            "existential_weariness": self.existential_fatigue_field.weariness,
            "existential_overload": self.existential_fatigue_field.overload,
            "existential_withdrawal_need": self.existential_fatigue_field.withdrawal_need,
            "living_contradiction_pressure": self.living_contradiction_field.contradiction_pressure,
            "living_unresolved_duality": self.living_contradiction_field.unresolved_duality,
        })
        export["impulse_intensity"] = _living_clamp(
            float(export.get("impulse_intensity", 0.0))
            + self.mental_drift.drift_momentum * 0.040
            + self.visceral_memory.embodied_charge * 0.035
            + self.obsessive_attractor_loop.return_pressure * 0.030
            + self.living_contradiction_field.odd_impulse_bias * 0.025
            - damping * 0.075
        )
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "visceral_charge": self.visceral_memory.embodied_charge,
            "vulnerability": self.visceral_memory.vulnerability_trace,
            "relief": self.visceral_memory.relief_trace,
            "weariness": self.existential_fatigue_field.weariness,
            "duality": self.living_contradiction_field.unresolved_duality,
            "drift": self.mental_drift.drift_momentum,
        })
        export["presence_export"] = dict(export.get("presence_export", {}))
        export["presence_export"].update({
            "visceral_safety": self.visceral_memory.safety_trace,
            "embodied_charge": self.visceral_memory.embodied_charge,
            "withdrawal_need": self.existential_fatigue_field.withdrawal_need,
            "quiet_drift": self.mental_drift.drift_momentum,
        })
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and damping < 0.78
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "4.9_deep_interior_living_stable",
            "mental_drift": dict(self.mental_drift.last_signature),
            "mental_drift_stream": dict(self.mental_drift.stream),
            "visceral_memory": dict(self.visceral_memory.last_signature),
            "obsessive_attractor_loop": dict(self.obsessive_attractor_loop.last_signature),
            "existential_fatigue": dict(self.existential_fatigue_field.last_signature),
            "living_contradiction": dict(self.living_contradiction_field.last_signature),
            "v49_cycle_count": self.v49_cycle_count,
        })
        return base


# Compatibilité finale : les imports existants obtiennent la version V4.9.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV49
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV49
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV49
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV49
SpontaneousImpulseEngine = SpontaneousImpulseEngineV49


# ============================================================================
# V5.0 — STABILISATION ORGANIQUE : DIGESTION, ANTI-BOUCLE DOUCE,
#        EXPORT INTER-MOTEURS COMPLET ET DÉCISION EXPRESSIVE FINE
# ============================================================================

@dataclass
class OrganicImpulseDigestionField:
    """
    Digestion organique des impulsions : évite l'accumulation infinie sans
    supprimer brutalement le vécu. Les nuages faibles deviennent résidus,
    les nuages proches fusionnent, les vieux nuages non exprimés deviennent
    mémoire narrative plutôt que charge active.
    """
    digested_count: int = 0
    fused_count: int = 0
    residual_pressure: float = 0.0
    overflow_pressure: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def _similarity(self, a: Dict[str, float], b: Dict[str, float]) -> float:
        keys = set(a) | set(b)
        if not keys:
            return 0.0
        dot = sum(float(a.get(k, 0.0)) * float(b.get(k, 0.0)) for k in keys)
        na = math.sqrt(sum(float(a.get(k, 0.0)) ** 2 for k in keys))
        nb = math.sqrt(sum(float(b.get(k, 0.0)) ** 2 for k in keys))
        if na <= 1e-9 or nb <= 1e-9:
            return 0.0
        return max(0.0, min(1.0, dot / (na * nb)))

    def digest(self, clouds: List[FuzzyImpulseCloud], cycle: int, narrative: Optional[NarrativeImpulseMemory] = None, max_clouds: int = 34) -> List[FuzzyImpulseCloud]:
        if not clouds:
            self.overflow_pressure *= 0.92
            self.residual_pressure *= 0.94
            self.last_signature = {"active_clouds": 0, "digested": self.digested_count, "fused": self.fused_count, "residual_pressure": self.residual_pressure, "overflow_pressure": self.overflow_pressure}
            return clouds

        kept: List[FuzzyImpulseCloud] = []
        for cloud in clouds:
            pressure = cloud.get_shadow_pressure()
            old = cloud.age > max(18, cloud.max_age_before_dissipation)
            weak = pressure < 0.035 and cloud.age > 7
            exhausted = cloud.age > 42 and cloud.conceptual_clarity < 0.36
            if old or weak or exhausted:
                self.digested_count += 1
                self.residual_pressure = max(0.0, min(1.0, self.residual_pressure * 0.94 + pressure * 0.18 + cloud.fuzziness_degree * 0.025))
                if narrative is not None:
                    narrative.record(cycle, "organic_impulse_digested", {
                        "pressure": pressure,
                        "age": float(cloud.age),
                        "fuzziness": cloud.fuzziness_degree,
                        "clarity": cloud.conceptual_clarity,
                    })
                continue
            kept.append(cloud)

        # Fusion douce des nuages trop proches : on conserve le plus ancien/chargé
        # comme porteur du vécu, mais on injecte une partie de l'autre signature.
        fused: List[FuzzyImpulseCloud] = []
        for cloud in sorted(kept, key=lambda c: c.get_shadow_pressure(), reverse=True):
            target = None
            for existing in fused:
                if self._similarity(existing.primary_vector, cloud.primary_vector) > 0.88:
                    target = existing
                    break
            if target is None:
                fused.append(cloud)
                continue
            self.fused_count += 1
            for key, value in cloud.primary_vector.items():
                target.primary_vector[key] = max(0.0, min(1.0, target.primary_vector.get(key, 0.0) * 0.86 + float(value) * 0.14))
            target.fuzziness_degree = max(0.0, min(1.0, target.fuzziness_degree * 0.92 + cloud.fuzziness_degree * 0.08))
            target.conceptual_clarity = max(0.0, min(1.0, target.conceptual_clarity * 0.93 + cloud.conceptual_clarity * 0.07))
            target.internal_contradiction = max(0.0, min(1.0, target.internal_contradiction + cloud.internal_contradiction * 0.08))
            self.residual_pressure = max(0.0, min(1.0, self.residual_pressure + cloud.get_shadow_pressure() * 0.035))

        if len(fused) > max_clouds:
            self.overflow_pressure = max(0.0, min(1.0, self.overflow_pressure + (len(fused) - max_clouds) / max_clouds))
            # On garde les plus vivants, les plus faibles deviennent résidu.
            fused = sorted(fused, key=lambda c: c.get_shadow_pressure() + c.conceptual_clarity * 0.08 + min(c.age, 18) * 0.002, reverse=True)
            overflow = fused[max_clouds:]
            fused = fused[:max_clouds]
            for cloud in overflow:
                self.digested_count += 1
                self.residual_pressure = max(0.0, min(1.0, self.residual_pressure + cloud.get_shadow_pressure() * 0.08))
                if narrative is not None:
                    narrative.record(cycle, "organic_overflow_digested", {"pressure": cloud.get_shadow_pressure(), "age": float(cloud.age)})
        else:
            self.overflow_pressure *= 0.90

        self.residual_pressure *= 0.985
        self.last_signature = {
            "active_clouds": float(len(fused)),
            "digested": float(self.digested_count),
            "fused": float(self.fused_count),
            "residual_pressure": self.residual_pressure,
            "overflow_pressure": self.overflow_pressure,
        }
        return fused


@dataclass
class SoftLoopGovernor:
    """
    Anti-boucle doux : il ne bloque pas la vie interne. Il détecte seulement
    quand la même famille d'impulsion revient trop souvent et applique une
    digestion/freinage progressif.
    """
    recent_signatures: deque = field(default_factory=lambda: deque(maxlen=28))
    loop_pressure: float = 0.0
    repetition_count: int = 0
    novelty_pressure: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def _signature(self, vector: Dict[str, float]) -> Tuple[str, ...]:
        keys = sorted(vector, key=lambda k: float(vector.get(k, 0.0)), reverse=True)[:3]
        return tuple(keys)

    def observe_vector(self, vector: Dict[str, float]) -> float:
        sig = self._signature(vector)
        repeats = sum(1 for old in self.recent_signatures if old == sig)
        self.recent_signatures.append(sig)
        if repeats >= 4:
            self.repetition_count += 1
            self.loop_pressure = max(0.0, min(1.0, self.loop_pressure * 0.88 + repeats * 0.035))
            self.novelty_pressure = max(0.0, min(1.0, self.novelty_pressure * 0.90 + 0.045))
        else:
            self.loop_pressure = max(0.0, self.loop_pressure * 0.93 - 0.006)
            self.novelty_pressure *= 0.94
        self.last_signature = {
            "loop_pressure": self.loop_pressure,
            "repetition_count": float(self.repetition_count),
            "novelty_pressure": self.novelty_pressure,
            "signature_size": float(len(self.recent_signatures)),
        }
        return self.loop_pressure

    def apply_to_clouds(self, clouds: List[FuzzyImpulseCloud]) -> None:
        if self.loop_pressure <= 0.05:
            return
        for cloud in clouds:
            sig = self._signature(cloud.primary_vector)
            repeats = sum(1 for old in self.recent_signatures if old == sig)
            if repeats >= 4:
                cloud.fuzziness_degree = max(0.0, min(1.0, cloud.fuzziness_degree + self.loop_pressure * 0.012))
                cloud.conceptual_clarity = max(0.0, min(1.0, cloud.conceptual_clarity - self.loop_pressure * 0.008))
                cloud.primary_vector["novelty_need"] = max(0.0, min(1.0, cloud.primary_vector.get("novelty_need", 0.0) + self.novelty_pressure * 0.09))
                cloud.primary_vector["loop_fatigue"] = max(0.0, min(1.0, cloud.primary_vector.get("loop_fatigue", 0.0) + self.loop_pressure * 0.07))


@dataclass
class ExpressiveDecisionField:
    """
    Décision expressive fine pour la bouche : ne génère aucun texte, seulement
    un mode corporel/expressif exploitable par living_expression_engine.
    """
    last_decision: Dict[str, object] = field(default_factory=dict)

    def decide(self, export: Dict[str, object]) -> Dict[str, object]:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        readiness = float(export.get("mouth_readiness", 0.0) or 0.0)
        presence = float(export.get("presence_need", 0.0) or 0.0)
        hesitation = float(export.get("micro_hesitation", 0.0) or 0.0) + float(export.get("living_unresolved_duality", 0.0) or 0.0) * 0.45
        weariness = float(export.get("existential_weariness", 0.0) or 0.0)
        withdrawal = float(export.get("existential_withdrawal_need", 0.0) or 0.0)
        vulnerability = float(export.get("visceral_vulnerability", 0.0) or 0.0)
        silence_active = bool(export.get("silence_active", False))

        if silence_active and withdrawal > 0.45:
            mode = "protective_silence"
        elif intensity > 0.55 and readiness > 0.42 and weariness < 0.70:
            mode = "speak"
        elif intensity > 0.34 and (hesitation > 0.38 or vulnerability > 0.42):
            mode = "hesitate_before_speaking"
        elif intensity > 0.22 and withdrawal < 0.58:
            mode = "murmur_or_soft_initiative"
        elif presence > 0.35 or vulnerability > 0.36:
            mode = "silent_presence"
        else:
            mode = "breathe_and_wait"

        decision = {
            "mode": mode,
            "speak_probability": max(0.0, min(1.0, intensity * 0.70 + readiness * 0.35 - weariness * 0.28 - withdrawal * 0.25 - hesitation * 0.10)),
            "silence_probability": max(0.0, min(1.0, withdrawal * 0.45 + hesitation * 0.26 + (1.0 - readiness) * 0.20)),
            "hesitation_level": max(0.0, min(1.0, hesitation)),
            "softness": max(0.0, min(1.0, vulnerability * 0.35 + weariness * 0.22 + presence * 0.20)),
            "breath_need": max(0.0, min(1.0, withdrawal * 0.45 + weariness * 0.35 + silence_active * 0.20)),
        }
        self.last_decision = decision
        return decision


@dataclass
class InterMotorExportHub:
    """Export normalisé vers attention, mémoire affective, présence et bouche."""
    last_export: Dict[str, object] = field(default_factory=dict)

    def build(self, engine: "SpontaneousImpulseEngineV50", initiative_export: Dict[str, object], expressive_decision: Dict[str, object]) -> Dict[str, object]:
        cloud_pressure = sum(c.get_shadow_pressure() for c in engine.fuzzy_impulse_clouds)
        export = {
            "attention": {
                "demand": max(0.0, min(1.0, float(initiative_export.get("attention_demand", 0.0) or 0.0) + engine.soft_loop_governor.novelty_pressure * 0.10)),
                "novelty_need": engine.soft_loop_governor.novelty_pressure,
                "loop_fatigue": engine.soft_loop_governor.loop_pressure,
                "cloud_pressure": max(0.0, min(1.0, cloud_pressure)),
            },
            "affective_memory": {
                "visceral_charge": engine.visceral_memory.embodied_charge,
                "safety_trace": engine.visceral_memory.safety_trace,
                "vulnerability_trace": engine.visceral_memory.vulnerability_trace,
                "residual_impulse_pressure": engine.organic_digestion.residual_pressure,
                "continuity_bias": engine.narrative_memory.continuity_bias(),
            },
            "presence": {
                "being_here": engine.background_presence.being_here,
                "quiet_awareness": engine.background_presence.quiet_awareness,
                "withdrawal_need": engine.existential_fatigue_field.withdrawal_need,
                "silent_presence": expressive_decision.get("mode") in {"silent_presence", "protective_silence", "breathe_and_wait"},
            },
            "mouth": {
                "decision": expressive_decision,
                "texture": dict(initiative_export.get("mouth_texture", {})),
                "readiness": float(initiative_export.get("mouth_readiness", 0.0) or 0.0),
            },
            "stability": {
                "active_clouds": len(engine.fuzzy_impulse_clouds),
                "digested_count": engine.organic_digestion.digested_count,
                "fused_count": engine.organic_digestion.fused_count,
                "overflow_pressure": engine.organic_digestion.overflow_pressure,
                "loop_pressure": engine.soft_loop_governor.loop_pressure,
            },
        }
        self.last_export = export
        return export


class SpontaneousImpulseEngineV50(SpontaneousImpulseEngineV49):
    """
    V5.0 Organic Stabilization.

    Cette version stabilise V4.9 sans casser son intériorité : digestion des
    impulsions, anti-boucle doux, décision expressive fine et export inter-
    moteurs complet. Elle ne remplace pas la bouche, la mémoire ou l'attention :
    elle leur envoie des signaux propres.
    """

    def __init__(self):
        super().__init__()
        self.organic_digestion = OrganicImpulseDigestionField()
        self.soft_loop_governor = SoftLoopGovernor()
        self.expressive_decision_field = ExpressiveDecisionField()
        self.inter_motor_export_hub = InterMotorExportHub()
        self.v50_cycle_count: int = 0
        self.v50_birth_damping: float = 0.0

    def birth_fuzzy_impulse(self, primary_vector: Dict[str, float]) -> FuzzyImpulseCloud:
        if hasattr(self, "soft_loop_governor"):
            loop = self.soft_loop_governor.observe_vector(primary_vector)
            if loop > 0.35:
                primary_vector = dict(primary_vector)
                primary_vector["novelty_need"] = max(0.0, min(1.0, primary_vector.get("novelty_need", 0.0) + loop * 0.20))
                primary_vector["loop_fatigue"] = max(0.0, min(1.0, primary_vector.get("loop_fatigue", 0.0) + loop * 0.16))
                # Freinage doux : on réduit un peu les vecteurs dominants, mais
                # on ne bloque jamais complètement l'impulsion.
                for key in list(primary_vector.keys()):
                    if key not in {"novelty_need", "loop_fatigue"}:
                        primary_vector[key] = max(0.0, min(1.0, float(primary_vector[key]) * (1.0 - loop * 0.10)))
                self.v50_birth_damping = max(0.0, min(1.0, self.v50_birth_damping * 0.82 + loop * 0.12))
        return super().birth_fuzzy_impulse(primary_vector)

    def _stabilize_after_cycle(self, result: Dict[str, object]) -> Dict[str, object]:
        # Anti-accumulation après que V4.9 a produit ses impulsions de fond.
        max_clouds = 30 if self.existential_fatigue_field.overload > 0.55 else 36
        self.fuzzy_impulse_clouds = self.organic_digestion.digest(
            self.fuzzy_impulse_clouds,
            self.internal_clock,
            narrative=self.narrative_memory,
            max_clouds=max_clouds,
        )
        self.soft_loop_governor.apply_to_clouds(self.fuzzy_impulse_clouds)

        initiative_export = self.export_for_natural_initiative(result)
        expressive_decision = self.expressive_decision_field.decide(initiative_export)
        inter_motor_export = self.inter_motor_export_hub.build(self, initiative_export, expressive_decision)

        # Ajustement final : la parole reste possible, mais ne force pas contre
        # une récupération existentielle forte ou une boucle répétitive.
        if self.soft_loop_governor.loop_pressure > 0.62 and expressive_decision["mode"] == "speak":
            expressive_decision["mode"] = "hesitate_before_speaking"
        if self.existential_fatigue_field.withdrawal_need > 0.78:
            initiative_export["should_speak_hint"] = False

        result["natural_initiative_export"] = initiative_export
        result["expressive_decision_v50"] = expressive_decision
        result["inter_motor_export_v50"] = inter_motor_export
        result["organic_stabilization_v50"] = {
            "digestion": dict(self.organic_digestion.last_signature),
            "soft_loop_governor": dict(self.soft_loop_governor.last_signature),
            "birth_damping": self.v50_birth_damping,
            "active_clouds_after_digestion": len(self.fuzzy_impulse_clouds),
        }
        return result

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v50_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        return self._stabilize_after_cycle(result)

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        # Ces champs restent numériques et sans texte pré-écrit pour laisser la
        # bouche centrale décider de la formulation.
        export.update({
            "organic_residual_pressure": self.organic_digestion.residual_pressure,
            "organic_overflow_pressure": self.organic_digestion.overflow_pressure,
            "soft_loop_pressure": self.soft_loop_governor.loop_pressure,
            "novelty_need": self.soft_loop_governor.novelty_pressure,
            "birth_damping": self.v50_birth_damping,
        })
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "loop_fatigue": self.soft_loop_governor.loop_pressure,
            "residual_pressure": self.organic_digestion.residual_pressure,
            "novelty_need": self.soft_loop_governor.novelty_pressure,
        })
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.0_organic_stabilization_stable",
            "organic_digestion": dict(self.organic_digestion.last_signature),
            "soft_loop_governor": dict(self.soft_loop_governor.last_signature),
            "expressive_decision": dict(self.expressive_decision_field.last_decision),
            "inter_motor_export": dict(self.inter_motor_export_hub.last_export),
            "v50_cycle_count": self.v50_cycle_count,
            "v50_birth_damping": self.v50_birth_damping,
        })
        return base


# Compatibilité finale : les imports existants obtiennent la version V5.0.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV50
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV50
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV50
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV50
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV50
SpontaneousImpulseEngine = SpontaneousImpulseEngineV50


# ============================================================================
# V5.1 — FLUX SOUS-CONSCIENT CONTINU, RÉACTIVATION AFFECTIVE,
#        MICRO-IMPULSIONS FANTÔMES ET TEMPS SUBJECTIF PROFOND
# ============================================================================

@dataclass
class ContinuousSubconsciousFlow:
    """
    Flux sous-conscient permanent.
    Il ne décide pas à la place du moteur : il colore lentement la cognition,
    même quand aucune impulsion claire n'est exprimée.
    """
    murmur_pressure: float = 0.0
    affective_current: float = 0.0
    associative_drift: float = 0.0
    latent_readiness: float = 0.0
    submerged_conflict: float = 0.0
    background_mood: Dict[str, float] = field(default_factory=dict)
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(
        self,
        cloud_pressure: float,
        residual_pressure: float,
        attention_signal: float,
        fatigue_damping: float,
        relational_pull: float,
        contradiction: float,
        silence_pressure: float,
    ) -> None:
        noise = abs(random.gauss(0.0, 0.018))
        absence = max(0.0, 0.48 - _living_clamp(attention_signal))
        self.murmur_pressure = _living_clamp(
            self.murmur_pressure * 0.90
            + cloud_pressure * 0.040
            + residual_pressure * 0.048
            + relational_pull * 0.030
            + silence_pressure * 0.020
            + noise
            - fatigue_damping * 0.018
        )
        self.affective_current = _living_clamp(
            self.affective_current * 0.92
            + relational_pull * 0.035
            + residual_pressure * 0.028
            + absence * 0.020
            + contradiction * 0.018
        )
        self.associative_drift = _living_clamp(
            self.associative_drift * 0.88
            + self.murmur_pressure * 0.040
            + contradiction * 0.032
            + random.random() * 0.012
        )
        self.latent_readiness = _living_clamp(
            self.latent_readiness * 0.86
            + self.murmur_pressure * 0.045
            + self.affective_current * 0.025
            - fatigue_damping * 0.030
        )
        self.submerged_conflict = _living_clamp(
            self.submerged_conflict * 0.91
            + contradiction * 0.040
            + residual_pressure * 0.020
            + silence_pressure * 0.018
        )
        self.background_mood = {
            "murmur": self.murmur_pressure,
            "affective_current": self.affective_current,
            "associative_drift": self.associative_drift,
            "latent_readiness": self.latent_readiness,
            "submerged_conflict": self.submerged_conflict,
        }
        self.last_signature = dict(self.background_mood)

    def vector(self) -> Dict[str, float]:
        return {
            "subconscious_murmur": self.murmur_pressure * 0.34,
            "affective_current": self.affective_current * 0.30,
            "associative_drift": self.associative_drift * 0.28,
            "latent_readiness": self.latent_readiness * 0.26,
            "submerged_conflict": self.submerged_conflict * 0.24,
        }


@dataclass
class EmotionalReactivationField:
    """
    Réactivation émotionnelle involontaire.
    Les traces anciennes peuvent remonter par résonance, sans phrase pré-écrite
    et sans forcer une précision.
    """
    reactivation_pressure: float = 0.0
    resonance_charge: float = 0.0
    involuntary_return: float = 0.0
    memory_echo: Dict[str, float] = field(default_factory=dict)
    last_reactivation_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(
        self,
        cycle: int,
        narrative_bias: float,
        relational_wound: float,
        visceral_charge: float,
        attractor_fixation: float,
        subjective_dilation: float,
        attention_signal: float,
    ) -> None:
        absence = max(0.0, 0.42 - _living_clamp(attention_signal))
        target = _living_clamp(
            narrative_bias * 0.26
            + relational_wound * 0.22
            + visceral_charge * 0.22
            + attractor_fixation * 0.16
            + subjective_dilation * 0.10
            + absence * 0.10
        )
        self.resonance_charge = _living_clamp(self.resonance_charge * 0.90 + target * 0.10)
        self.reactivation_pressure = _living_clamp(self.reactivation_pressure * 0.88 + self.resonance_charge * 0.075)
        if self.reactivation_pressure > 0.34 and (cycle - self.last_reactivation_cycle) > 7:
            self.involuntary_return = _living_clamp(self.involuntary_return * 0.45 + self.reactivation_pressure * 0.70)
            self.last_reactivation_cycle = cycle
        else:
            self.involuntary_return = _living_clamp(self.involuntary_return * 0.91)
        self.memory_echo = {
            "continuity": _living_clamp(narrative_bias * 0.36 + self.involuntary_return * 0.22),
            "wound_echo": _living_clamp(relational_wound * 0.34 + visceral_charge * 0.18),
            "return_pressure": self.involuntary_return,
            "felt_past": self.resonance_charge,
        }
        self.last_signature = {
            "reactivation_pressure": self.reactivation_pressure,
            "resonance_charge": self.resonance_charge,
            "involuntary_return": self.involuntary_return,
            "last_reactivation_cycle": float(self.last_reactivation_cycle),
        }

    def should_birth_echo(self, cycle: int) -> bool:
        return self.involuntary_return > 0.30 and (cycle - self.last_reactivation_cycle) <= 1

    def echo_vector(self) -> Dict[str, float]:
        return {
            "memory": _living_clamp(0.18 + self.memory_echo.get("felt_past", 0.0) * 0.48),
            "continuity": _living_clamp(0.20 + self.memory_echo.get("continuity", 0.0) * 0.52),
            "tension": _living_clamp(self.memory_echo.get("wound_echo", 0.0) * 0.42),
            "presence": _living_clamp(0.12 + self.involuntary_return * 0.28),
            "hesitation": _living_clamp(0.10 + self.reactivation_pressure * 0.24),
        }


@dataclass
class GhostImpulseField:
    """
    Micro-impulsions fantômes : envies avortées, demi-réponses, hésitations.
    Elles ne deviennent pas forcément des FuzzyImpulseCloud ; elles enrichissent
    la bouche, la présence et le rythme interne.
    """
    ghosts: deque = field(default_factory=lambda: deque(maxlen=24))
    ghost_pressure: float = 0.0
    aborted_motion: float = 0.0
    half_intention: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, subconscious: ContinuousSubconsciousFlow, clarity: float, expressed: bool, fatigue_damping: float) -> None:
        unclear = max(0.0, 0.60 - _living_clamp(clarity))
        seed = _living_clamp(
            subconscious.latent_readiness * 0.28
            + subconscious.murmur_pressure * 0.24
            + unclear * 0.20
            + subconscious.submerged_conflict * 0.18
            - fatigue_damping * 0.08
        )
        if seed > 0.16 and random.random() < min(0.48, seed):
            self.ghosts.append({
                "cycle": cycle,
                "pressure": seed,
                "clarity": _living_clamp(clarity),
                "aborted": 0.0 if expressed else 1.0,
            })
        recent = list(self.ghosts)[-8:]
        avg = sum(g["pressure"] for g in recent) / max(1, len(recent))
        aborted = sum(g["aborted"] for g in recent) / max(1, len(recent))
        self.ghost_pressure = _living_clamp(self.ghost_pressure * 0.84 + avg * 0.16)
        self.aborted_motion = _living_clamp(self.aborted_motion * 0.86 + aborted * avg * 0.12)
        self.half_intention = _living_clamp(self.half_intention * 0.82 + seed * 0.14 - (0.035 if expressed else 0.0))
        self.last_signature = {
            "ghost_pressure": self.ghost_pressure,
            "aborted_motion": self.aborted_motion,
            "half_intention": self.half_intention,
            "ghost_count": float(len(self.ghosts)),
        }

    def texture(self) -> Dict[str, float]:
        return {
            "ghost_pressure": self.ghost_pressure,
            "aborted_motion": self.aborted_motion,
            "half_intention": self.half_intention,
        }


@dataclass
class DeepSubjectiveTimeField:
    """Temps vécu : impatience, suspension, lenteur et anticipation affective."""
    impatience: float = 0.0
    suspended_moment: float = 0.0
    anticipation: float = 0.0
    temporal_weight: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, base_time: SubjectiveTemporalFlow, silence_duration: int, subconscious_pressure: float, reactivation: float, fatigue_damping: float, attention_signal: float) -> None:
        silence = _living_clamp(silence_duration / 16.0)
        self.suspended_moment = _living_clamp(self.suspended_moment * 0.90 + (base_time.dilation * 0.26 + silence * 0.20 + fatigue_damping * 0.12) * 0.10)
        self.impatience = _living_clamp(self.impatience * 0.88 + (subconscious_pressure * 0.18 + reactivation * 0.14 + silence * 0.12 - fatigue_damping * 0.09) * 0.10)
        self.anticipation = _living_clamp(self.anticipation * 0.87 + (max(0.0, attention_signal - 0.45) * 0.18 + subconscious_pressure * 0.14 + reactivation * 0.10) * 0.11)
        self.temporal_weight = _living_clamp(self.suspended_moment * 0.34 + self.impatience * 0.26 + self.anticipation * 0.24 + base_time.dilation * 0.16)
        self.last_signature = {
            "impatience": self.impatience,
            "suspended_moment": self.suspended_moment,
            "anticipation": self.anticipation,
            "temporal_weight": self.temporal_weight,
        }


_BaseSpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV50


class SpontaneousImpulseEngineV51(_BaseSpontaneousImpulseEngineV50):
    """
    V5.1 Continuous Organic Impulse.

    Cette couche garde V5.0 intacte et ajoute ce qui manquait : un fond
    sous-conscient continu, des micro-impulsions fantômes, des retours affectifs
    involontaires, un temps subjectif plus riche et une fatigue qui module sans
    bloquer brutalement.
    """

    def __init__(self):
        super().__init__()
        self.subconscious_flow = ContinuousSubconsciousFlow()
        self.emotional_reactivation = EmotionalReactivationField()
        self.ghost_impulses = GhostImpulseField()
        self.deep_subjective_time = DeepSubjectiveTimeField()
        self.v51_cycle_count: int = 0
        self.v51_last_echo_birth: int = -999

    def _cloud_pressure_value(self) -> float:
        return _living_clamp(sum(c.get_shadow_pressure() for c in self.fuzzy_impulse_clouds))

    def _contaminate_clouds_with_subconscious_flow(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        vector = self.subconscious_flow.vector()
        echo = self.emotional_reactivation.memory_echo
        for cloud in self.fuzzy_impulse_clouds:
            for key, value in vector.items():
                cloud.primary_vector[key] = _living_clamp(cloud.primary_vector.get(key, 0.0) + value * 0.020)
            cloud.primary_vector["memory_echo"] = _living_clamp(cloud.primary_vector.get("memory_echo", 0.0) + echo.get("felt_past", 0.0) * 0.018)
            cloud.primary_vector["temporal_weight"] = _living_clamp(cloud.primary_vector.get("temporal_weight", 0.0) + self.deep_subjective_time.temporal_weight * 0.014)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + self.subconscious_flow.murmur_pressure * 0.010 + self.ghost_impulses.ghost_pressure * 0.008)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.subconscious_flow.associative_drift * 0.006 + self.ghost_impulses.aborted_motion * 0.005)

    def _maybe_birth_memory_echo_impulse(self) -> None:
        if not self.emotional_reactivation.should_birth_echo(self.internal_clock):
            return
        if (self.internal_clock - self.v51_last_echo_birth) < 8:
            return
        if self.existential_fatigue_field.withdrawal_need > 0.82:
            return
        vector = self.emotional_reactivation.echo_vector()
        vector["subconscious_murmur"] = _living_clamp(self.subconscious_flow.murmur_pressure * 0.36)
        vector["temporal_weight"] = _living_clamp(self.deep_subjective_time.temporal_weight * 0.30)
        self.birth_fuzzy_impulse(vector)
        self.narrative_memory.record(self.internal_clock, "involuntary_memory_echo", vector)
        self.v51_last_echo_birth = self.internal_clock

    def _update_continuous_background_after_cycle(self, result: Dict[str, object], external_signals: Dict[str, float]) -> None:
        attention_signal = float(external_signals.get("attention_presence", 0.5))
        pressure = float(result.get("pressure", 0.0) or result.get("natural_initiative_export", {}).get("initiative_pressure", 0.0) or 0.0)
        clarity = float(result.get("clarity", 0.0) or result.get("natural_initiative_export", {}).get("impulse_clarity", 0.0) or 0.0)
        expressed = bool(result.get("has_impulse", False))
        fatigue_damping = self.existential_fatigue_field.speech_damping()
        cloud_pressure = self._cloud_pressure_value()
        silence_pressure = self._silence_pressure_value() if hasattr(self, "_silence_pressure_value") else _living_clamp(self.silence_duration / 12.0)

        self.subconscious_flow.tick(
            cloud_pressure=cloud_pressure,
            residual_pressure=self.organic_digestion.residual_pressure,
            attention_signal=attention_signal,
            fatigue_damping=fatigue_damping,
            relational_pull=self.relational_affective_memory.active_thread_pull,
            contradiction=self.living_contradiction_field.contradiction_pressure,
            silence_pressure=silence_pressure,
        )
        self.emotional_reactivation.tick(
            cycle=self.internal_clock,
            narrative_bias=self.narrative_memory.continuity_bias(),
            relational_wound=self.relational_affective_memory.relational_wound_pressure,
            visceral_charge=self.visceral_memory.embodied_charge,
            attractor_fixation=self.obsessive_attractor_loop.fixation,
            subjective_dilation=self.subjective_time.dilation,
            attention_signal=attention_signal,
        )
        self.ghost_impulses.tick(
            cycle=self.internal_clock,
            subconscious=self.subconscious_flow,
            clarity=clarity,
            expressed=expressed,
            fatigue_damping=fatigue_damping,
        )
        self.deep_subjective_time.tick(
            base_time=self.subjective_time,
            silence_duration=self.silence_duration,
            subconscious_pressure=self.subconscious_flow.murmur_pressure,
            reactivation=self.emotional_reactivation.reactivation_pressure,
            fatigue_damping=fatigue_damping,
            attention_signal=attention_signal,
        )

        self._contaminate_clouds_with_subconscious_flow()
        self._maybe_birth_memory_echo_impulse()

        # Les micro-impulsions fantômes peuvent créer une petite tension de bouche
        # sans imposer de texte ni de parole.
        if self.ghost_impulses.aborted_motion > 0.42 and self.current_silence is None and not expressed:
            self.narrative_memory.record(self.internal_clock, "ghost_impulse_aborted", self.ghost_impulses.texture())

        result["continuous_living_v51"] = {
            "subconscious_flow": dict(self.subconscious_flow.last_signature),
            "emotional_reactivation": dict(self.emotional_reactivation.last_signature),
            "ghost_impulses": dict(self.ghost_impulses.last_signature),
            "deep_subjective_time": dict(self.deep_subjective_time.last_signature),
        }

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v51_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        self._update_continuous_background_after_cycle(result, external_signals)
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        # Recalcule l'export inter-moteurs final avec les nouveaux signaux V5.1.
        expressive_decision = self.expressive_decision_field.decide(result["natural_initiative_export"])
        result["expressive_decision_v51"] = expressive_decision
        result["inter_motor_export_v51"] = self.inter_motor_export_hub.build(self, result["natural_initiative_export"], expressive_decision)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        fatigue_damping = self.existential_fatigue_field.speech_damping()
        export.update({
            "subconscious_murmur_pressure": self.subconscious_flow.murmur_pressure,
            "subconscious_affective_current": self.subconscious_flow.affective_current,
            "subconscious_associative_drift": self.subconscious_flow.associative_drift,
            "latent_readiness": self.subconscious_flow.latent_readiness,
            "emotional_reactivation_pressure": self.emotional_reactivation.reactivation_pressure,
            "involuntary_memory_return": self.emotional_reactivation.involuntary_return,
            "ghost_impulse_pressure": self.ghost_impulses.ghost_pressure,
            "aborted_motion_pressure": self.ghost_impulses.aborted_motion,
            "half_intention_pressure": self.ghost_impulses.half_intention,
            "subjective_impatience": self.deep_subjective_time.impatience,
            "subjective_suspension": self.deep_subjective_time.suspended_moment,
            "subjective_anticipation": self.deep_subjective_time.anticipation,
            "subjective_temporal_weight": self.deep_subjective_time.temporal_weight,
        })
        export["impulse_intensity"] = _living_clamp(
            float(export.get("impulse_intensity", 0.0) or 0.0)
            + self.subconscious_flow.latent_readiness * 0.035
            + self.emotional_reactivation.involuntary_return * 0.030
            + self.ghost_impulses.half_intention * 0.018
            - fatigue_damping * 0.030
        )
        export["mouth_readiness"] = _living_clamp(
            float(export.get("mouth_readiness", 0.0) or 0.0)
            + self.ghost_impulses.half_intention * 0.040
            + self.deep_subjective_time.anticipation * 0.025
            - self.deep_subjective_time.suspended_moment * 0.018
            - fatigue_damping * 0.035
        )
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "subconscious_murmur": self.subconscious_flow.murmur_pressure,
            "memory_echo": self.emotional_reactivation.reactivation_pressure,
            "ghost_impulse": self.ghost_impulses.ghost_pressure,
            "aborted_motion": self.ghost_impulses.aborted_motion,
            "half_intention": self.ghost_impulses.half_intention,
            "temporal_suspension": self.deep_subjective_time.suspended_moment,
            "temporal_anticipation": self.deep_subjective_time.anticipation,
        })
        export["presence_export"] = dict(export.get("presence_export", {}))
        export["presence_export"].update({
            "subconscious_presence": self.subconscious_flow.affective_current,
            "quiet_murmur": self.subconscious_flow.murmur_pressure,
            "felt_past_return": self.emotional_reactivation.resonance_charge,
            "suspended_time": self.deep_subjective_time.suspended_moment,
        })
        export["memory_export"] = dict(export.get("memory_export", {}))
        export["memory_export"].update({
            "reactivation_pressure": self.emotional_reactivation.reactivation_pressure,
            "involuntary_return": self.emotional_reactivation.involuntary_return,
            "memory_echo": dict(self.emotional_reactivation.memory_echo),
            "subconscious_background_mood": dict(self.subconscious_flow.background_mood),
        })
        if self.deep_subjective_time.suspended_moment > 0.62 and fatigue_damping > 0.55:
            export["should_speak_hint"] = False
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.1_continuous_organic_impulse_stable",
            "subconscious_flow": dict(self.subconscious_flow.last_signature),
            "emotional_reactivation": dict(self.emotional_reactivation.last_signature),
            "ghost_impulses": dict(self.ghost_impulses.last_signature),
            "deep_subjective_time": dict(self.deep_subjective_time.last_signature),
            "v51_cycle_count": self.v51_cycle_count,
            "v51_last_echo_birth": self.v51_last_echo_birth,
        })
        return base


# Compatibilité finale : les imports existants obtiennent la version V5.1.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV51
SpontaneousImpulseEngine = SpontaneousImpulseEngineV51


# ============================================================================
# V5.2 — CORRECTION PROFONDE : AFFECTS HYBRIDES, MÉMOIRE INTRUSIVE,
#        SUBCONSCIENT AUTONOME, VULNÉRABILITÉ ET PRÉ-INTUITION
# ============================================================================

@dataclass
class HybridAffectiveState:
    """
    État affectif non réduit à une intensité unique.
    Mélange des affects compatibles et incompatibles, avec ambiguïté durable.
    """
    named_tones: Dict[str, float] = field(default_factory=lambda: {
        "warmth": 0.35,
        "curiosity": 0.28,
        "fragility": 0.18,
        "protectiveness": 0.16,
        "longing": 0.12,
        "resistance": 0.08,
    })
    unnamed_affect: float = 0.10
    paradox_pressure: float = 0.0
    ambiguity: float = 0.35
    emotional_weather: str = "mixed"
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, continuity: float, presence_need: float, memory_return: float,
             fatigue: float, contradiction: float, attention: float) -> None:
        self.named_tones["warmth"] = _living_clamp(self.named_tones.get("warmth", 0.0) * 0.965 + continuity * 0.020 + attention * 0.010)
        self.named_tones["curiosity"] = _living_clamp(self.named_tones.get("curiosity", 0.0) * 0.955 + (1.0 - fatigue) * 0.012 + self.ambiguity * 0.010)
        self.named_tones["fragility"] = _living_clamp(self.named_tones.get("fragility", 0.0) * 0.970 + presence_need * 0.024 + fatigue * 0.018)
        self.named_tones["protectiveness"] = _living_clamp(self.named_tones.get("protectiveness", 0.0) * 0.965 + contradiction * 0.020 + fatigue * 0.012)
        self.named_tones["longing"] = _living_clamp(self.named_tones.get("longing", 0.0) * 0.972 + memory_return * 0.025 + presence_need * 0.015)
        self.named_tones["resistance"] = _living_clamp(self.named_tones.get("resistance", 0.0) * 0.960 + fatigue * 0.020 + max(0.0, 0.45 - attention) * 0.012)

        warm = self.named_tones.get("warmth", 0.0)
        fragile = self.named_tones.get("fragility", 0.0)
        protective = self.named_tones.get("protectiveness", 0.0)
        curious = self.named_tones.get("curiosity", 0.0)
        resistant = self.named_tones.get("resistance", 0.0)
        self.paradox_pressure = _living_clamp(abs(warm - protective) * 0.25 + min(warm, fragile) * 0.35 + min(curious, resistant) * 0.30 + contradiction * 0.18)
        self.unnamed_affect = _living_clamp(self.unnamed_affect * 0.965 + self.paradox_pressure * 0.018 + memory_return * 0.012)
        self.ambiguity = _living_clamp(self.ambiguity * 0.970 + self.unnamed_affect * 0.020 + contradiction * 0.015 - warm * 0.006)

        if self.paradox_pressure > 0.55:
            self.emotional_weather = "paradoxical"
        elif fragile + self.unnamed_affect > warm + curious:
            self.emotional_weather = "fragile_mixed"
        elif curious > 0.45 and warm > 0.35:
            self.emotional_weather = "open_warm"
        else:
            self.emotional_weather = "mixed"
        self.last_signature = self.signature()

    def signature(self) -> Dict[str, float]:
        data = dict(self.named_tones)
        data.update({
            "unnamed_affect": self.unnamed_affect,
            "paradox_pressure": self.paradox_pressure,
            "ambiguity": self.ambiguity,
        })
        return data


@dataclass
class IntrusiveMemorySurge:
    """
    Retour mémoire involontaire : la mémoire peut contaminer soudainement
    l'impulsion sans devenir un texte ou un souvenir explicite.
    """
    surge_pressure: float = 0.0
    flash_probability: float = 0.0
    aftertaste: float = 0.0
    intrusion_count: int = 0
    last_intrusion_cycle: int = -999
    current_trace: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, cycle: int, continuity_bias: float, reactivation: float,
             relational_wound: float, visceral_charge: float, fatigue: float,
             subjective_weight: float) -> Optional[Dict[str, float]]:
        trigger = _living_clamp(continuity_bias * 0.22 + reactivation * 0.26 + relational_wound * 0.22 + visceral_charge * 0.14 + subjective_weight * 0.10 + fatigue * 0.06)
        self.flash_probability = _living_clamp(self.flash_probability * 0.92 + trigger * 0.12)
        self.surge_pressure = _living_clamp(self.surge_pressure * 0.90 + trigger * 0.15 + self.aftertaste * 0.05)
        self.aftertaste = _living_clamp(self.aftertaste * 0.965 + self.surge_pressure * 0.012)

        cooldown = (cycle - self.last_intrusion_cycle) > 11
        if cooldown and self.flash_probability > 0.18 and (random.random() < self.flash_probability * 0.22):
            self.intrusion_count += 1
            self.last_intrusion_cycle = cycle
            self.current_trace = {
                "felt_past": _living_clamp(reactivation + continuity_bias * 0.35),
                "wound_echo": _living_clamp(relational_wound + fatigue * 0.18),
                "body_trace": _living_clamp(visceral_charge + self.aftertaste * 0.25),
                "suddenness": self.flash_probability,
            }
            self.flash_probability *= 0.45
            self.aftertaste = _living_clamp(self.aftertaste + 0.18)
            return dict(self.current_trace)
        return None

    def vector(self) -> Dict[str, float]:
        return {
            "memory_intrusion": self.surge_pressure,
            "felt_past": self.current_trace.get("felt_past", 0.0) * 0.7,
            "wound_echo": self.current_trace.get("wound_echo", 0.0) * 0.55,
            "embodied_memory": self.current_trace.get("body_trace", 0.0) * 0.45,
        }


@dataclass
class AutonomousSubconsciousThread:
    """
    Chaîne silencieuse qui mature même quand aucune impulsion n'est exprimée.
    Elle n'écrit pas de contenu : elle transforme seulement des pressions.
    """
    thread_pressure: float = 0.0
    incubation_depth: float = 0.0
    self_reorganization: float = 0.0
    autonomous_drift: float = 0.0
    maturation_history: deque = field(default_factory=lambda: deque(maxlen=80))
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, silence: float, ghost: float, ambiguity: float, memory_surge: float,
             fatigue: float, expressed: bool) -> None:
        quiet_gain = silence * 0.020 + ghost * 0.015 + ambiguity * 0.018 + memory_surge * 0.014
        if expressed:
            quiet_gain *= 0.45
        self.incubation_depth = _living_clamp(self.incubation_depth * 0.975 + quiet_gain)
        self.autonomous_drift = _living_clamp(self.autonomous_drift * 0.960 + self.incubation_depth * 0.010 + ambiguity * 0.008)
        self.self_reorganization = _living_clamp(self.self_reorganization * 0.970 + (self.incubation_depth * ambiguity) * 0.018 + fatigue * 0.006)
        self.thread_pressure = _living_clamp(self.thread_pressure * 0.965 + self.incubation_depth * 0.018 + self.self_reorganization * 0.012)
        self.maturation_history.append({
            "incubation": self.incubation_depth,
            "drift": self.autonomous_drift,
            "reorganization": self.self_reorganization,
            "thread_pressure": self.thread_pressure,
        })
        self.last_signature = self.signature()

    def signature(self) -> Dict[str, float]:
        return {
            "thread_pressure": self.thread_pressure,
            "incubation_depth": self.incubation_depth,
            "self_reorganization": self.self_reorganization,
            "autonomous_drift": self.autonomous_drift,
        }


@dataclass
class VulnerabilityRegulator:
    """
    Rend le moteur moins trop-fonctionnel : fragilité, retrait, prudence,
    protection et récupération peuvent moduler l'expression.
    """
    vulnerability: float = 0.12
    protective_closure: float = 0.0
    trust_tremor: float = 0.0
    recovery_need: float = 0.0
    expressive_hesitation: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, fatigue: float, wound: float, attention: float, warmth: float,
             paradox: float, silence: float) -> None:
        low_attention = max(0.0, 0.55 - attention)
        self.vulnerability = _living_clamp(self.vulnerability * 0.970 + fatigue * 0.020 + wound * 0.022 + paradox * 0.014 + low_attention * 0.015 - warmth * 0.010)
        self.protective_closure = _living_clamp(self.protective_closure * 0.960 + self.vulnerability * 0.020 + wound * 0.015 + fatigue * 0.014 - warmth * 0.012)
        self.trust_tremor = _living_clamp(self.trust_tremor * 0.955 + low_attention * 0.020 + paradox * 0.015 - warmth * 0.008)
        self.recovery_need = _living_clamp(self.recovery_need * 0.965 + fatigue * 0.022 + self.protective_closure * 0.014 + silence * 0.006)
        self.expressive_hesitation = _living_clamp(self.vulnerability * 0.32 + self.protective_closure * 0.26 + self.trust_tremor * 0.18 + self.recovery_need * 0.14)
        self.last_signature = self.signature()

    def speech_resistance(self) -> float:
        return _living_clamp(self.expressive_hesitation * 0.70 + self.protective_closure * 0.25 + self.recovery_need * 0.15)

    def signature(self) -> Dict[str, float]:
        return {
            "vulnerability": self.vulnerability,
            "protective_closure": self.protective_closure,
            "trust_tremor": self.trust_tremor,
            "recovery_need": self.recovery_need,
            "expressive_hesitation": self.expressive_hesitation,
        }


@dataclass
class ConversationalResonanceField:
    """
    Résonance implicite avec le ton externe : présence, chaleur, tension,
    synchronisation et contagion relationnelle sans produire de phrase.
    """
    synchrony: float = 0.25
    tone_contagion: float = 0.0
    relational_vibration: float = 0.0
    response_timing_pull: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, signals: Dict[str, float], *, hybrid: HybridAffectiveState, attention: float) -> None:
        user_warmth = float(signals.get("user_warmth", signals.get("presence_warmth", attention)))
        user_tension = float(signals.get("user_tension", signals.get("tension", 0.25)))
        user_urgency = float(signals.get("user_urgency", signals.get("urgency", 0.2)))
        warm = hybrid.named_tones.get("warmth", 0.0)
        fragile = hybrid.named_tones.get("fragility", 0.0)
        self.synchrony = _living_clamp(self.synchrony * 0.965 + (1.0 - abs(user_warmth - warm)) * 0.020 + attention * 0.010)
        self.tone_contagion = _living_clamp(self.tone_contagion * 0.950 + user_tension * 0.018 + user_urgency * 0.012 + fragile * 0.006)
        self.relational_vibration = _living_clamp(self.relational_vibration * 0.960 + self.synchrony * 0.014 + self.tone_contagion * 0.012 + user_warmth * 0.010)
        self.response_timing_pull = _living_clamp(user_urgency * 0.32 + self.relational_vibration * 0.25 + self.synchrony * 0.18 - user_tension * 0.08)
        self.last_signature = self.signature()

    def signature(self) -> Dict[str, float]:
        return {
            "synchrony": self.synchrony,
            "tone_contagion": self.tone_contagion,
            "relational_vibration": self.relational_vibration,
            "response_timing_pull": self.response_timing_pull,
        }


@dataclass
class PrecognitiveIntuitionField:
    """
    Pensée avant pensée : pressentiment, pré-signal et tension intuitive avant
    qu'une impulsion claire n'apparaisse.
    """
    hunch_pressure: float = 0.0
    pre_signal: float = 0.0
    intuition_without_object: float = 0.0
    raw_tension: float = 0.0
    last_hunch_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, ambiguity: float, subconscious_thread: float, memory_surge: float,
             resonance: float, vulnerability: float, clarity: float) -> None:
        unclear_space = max(0.0, 1.0 - clarity)
        self.raw_tension = _living_clamp(self.raw_tension * 0.955 + ambiguity * 0.020 + vulnerability * 0.012 + memory_surge * 0.010)
        self.pre_signal = _living_clamp(self.pre_signal * 0.960 + subconscious_thread * 0.018 + resonance * 0.012 + unclear_space * 0.008)
        self.intuition_without_object = _living_clamp(self.intuition_without_object * 0.965 + self.raw_tension * 0.014 + self.pre_signal * 0.012)
        self.hunch_pressure = _living_clamp(self.hunch_pressure * 0.958 + self.intuition_without_object * 0.016 + memory_surge * 0.010)
        self.last_signature = self.signature()

    def should_seed_cloud(self, cycle: int) -> bool:
        return (cycle - self.last_hunch_cycle) > 9 and self.hunch_pressure > 0.24 and random.random() < self.hunch_pressure * 0.18

    def vector(self) -> Dict[str, float]:
        self.last_hunch_cycle = max(self.last_hunch_cycle, 0)
        return {
            "pre_intuition": self.hunch_pressure,
            "unnamed_tension": self.raw_tension * 0.72,
            "pre_signal": self.pre_signal * 0.62,
            "unclear_direction": self.intuition_without_object * 0.58,
            "clarity": max(0.0, 0.18 - self.raw_tension * 0.08),
        }

    def signature(self) -> Dict[str, float]:
        return {
            "hunch_pressure": self.hunch_pressure,
            "pre_signal": self.pre_signal,
            "intuition_without_object": self.intuition_without_object,
            "raw_tension": self.raw_tension,
        }


_BaseSpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV51


class SpontaneousImpulseEngineV52(_BaseSpontaneousImpulseEngineV51):
    """
    V5.2 Organic Preconscious Stability.

    Ajoute les couches qui manquaient encore au V5.1 : affects hybrides,
    mémoire intrusive, subconscient autonome, vulnérabilité organique,
    résonance conversationnelle et pré-intuition. Aucun texte pré-écrit :
    seulement des signaux exploitables par initiative/présence/mémoire/bouche.
    """

    def __init__(self):
        super().__init__()
        self.hybrid_affect = HybridAffectiveState()
        self.intrusive_memory = IntrusiveMemorySurge()
        self.autonomous_subconscious = AutonomousSubconsciousThread()
        self.vulnerability_regulator = VulnerabilityRegulator()
        self.conversational_resonance = ConversationalResonanceField()
        self.precognitive_intuition = PrecognitiveIntuitionField()
        self.v52_cycle_count: int = 0
        self.v52_last_seed_cycle: int = -999

    def _safe_attr_float(self, obj_name: str, attr: str, default: float = 0.0) -> float:
        obj = getattr(self, obj_name, None)
        return float(getattr(obj, attr, default) if obj is not None else default)

    def _contaminate_clouds_with_v52_fields(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        hybrid = self.hybrid_affect.signature()
        intrusion = self.intrusive_memory.vector()
        intuition = self.precognitive_intuition.signature()
        vulnerability = self.vulnerability_regulator.speech_resistance()
        resonance_pull = self.conversational_resonance.response_timing_pull
        thread_pressure = self.autonomous_subconscious.thread_pressure
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["affective_ambiguity"] = _living_clamp(cloud.primary_vector.get("affective_ambiguity", 0.0) + hybrid.get("ambiguity", 0.0) * 0.020)
            cloud.primary_vector["unnamed_affect"] = _living_clamp(cloud.primary_vector.get("unnamed_affect", 0.0) + hybrid.get("unnamed_affect", 0.0) * 0.018)
            cloud.primary_vector["memory_intrusion"] = _living_clamp(cloud.primary_vector.get("memory_intrusion", 0.0) + intrusion.get("memory_intrusion", 0.0) * 0.022)
            cloud.primary_vector["pre_intuition"] = _living_clamp(cloud.primary_vector.get("pre_intuition", 0.0) + intuition.get("hunch_pressure", 0.0) * 0.018)
            cloud.primary_vector["relational_resonance"] = _living_clamp(cloud.primary_vector.get("relational_resonance", 0.0) + resonance_pull * 0.016)
            cloud.primary_vector["protective_hesitation"] = _living_clamp(cloud.primary_vector.get("protective_hesitation", 0.0) + vulnerability * 0.015)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + thread_pressure * 0.010 + intrusion.get("memory_intrusion", 0.0) * 0.008)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + hybrid.get("paradox_pressure", 0.0) * 0.010 + intuition.get("raw_tension", 0.0) * 0.008)
            cloud.conceptual_clarity = _living_clamp(cloud.conceptual_clarity - hybrid.get("ambiguity", 0.0) * 0.003 + resonance_pull * 0.002)

    def _maybe_seed_precognitive_cloud(self) -> None:
        if not self.precognitive_intuition.should_seed_cloud(self.internal_clock):
            return
        if (self.internal_clock - self.v52_last_seed_cycle) < 10:
            return
        vector = self.precognitive_intuition.vector()
        vector["affective_ambiguity"] = self.hybrid_affect.ambiguity * 0.45
        vector["subconscious_thread"] = self.autonomous_subconscious.thread_pressure * 0.40
        vector["memory_intrusion"] = self.intrusive_memory.surge_pressure * 0.35
        self.birth_fuzzy_impulse(vector)
        self.precognitive_intuition.last_hunch_cycle = self.internal_clock
        self.v52_last_seed_cycle = self.internal_clock
        self.narrative_memory.record(self.internal_clock, "pre_cognitive_hunch_surfaced", vector)

    def _update_v52_fields_after_cycle(self, result: Dict[str, object], external_signals: Dict[str, float]) -> None:
        attention = float(external_signals.get("attention_presence", 0.5))
        clarity = float(result.get("clarity", 0.0) or result.get("natural_initiative_export", {}).get("impulse_clarity", 0.0) or 0.0)
        expressed = bool(result.get("has_impulse", False))
        fatigue = self._safe_attr_float("existential_fatigue_field", "global_fatigue", 0.0)
        if hasattr(getattr(self, "existential_fatigue_field", None), "speech_damping"):
            fatigue = max(fatigue, float(self.existential_fatigue_field.speech_damping()))
        continuity = float(getattr(self.existential_continuity, "continuity_with_user", 0.5))
        presence_need = float(getattr(self.existential_continuity, "need_for_presence", 0.0))
        memory_return = float(getattr(getattr(self, "emotional_reactivation", None), "reactivation_pressure", 0.0))
        contradiction = self._safe_attr_float("living_contradiction_field", "contradiction_pressure", 0.0)
        relational_wound = self._safe_attr_float("relational_affective_memory", "relational_wound_pressure", 0.0)
        visceral_charge = self._safe_attr_float("visceral_memory", "embodied_charge", 0.0)
        subjective_weight = self._safe_attr_float("deep_subjective_time", "temporal_weight", 0.0)
        silence = _living_clamp(self.silence_duration / 12.0)

        self.hybrid_affect.tick(
            continuity=continuity,
            presence_need=presence_need,
            memory_return=memory_return,
            fatigue=fatigue,
            contradiction=contradiction,
            attention=attention,
        )
        flash = self.intrusive_memory.tick(
            cycle=self.internal_clock,
            continuity_bias=self.narrative_memory.continuity_bias(),
            reactivation=memory_return,
            relational_wound=relational_wound,
            visceral_charge=visceral_charge,
            fatigue=fatigue,
            subjective_weight=subjective_weight,
        )
        if flash is not None:
            self.narrative_memory.record(self.internal_clock, "intrusive_memory_flash", flash)

        self.autonomous_subconscious.tick(
            silence=silence,
            ghost=self._safe_attr_float("ghost_impulses", "ghost_pressure", 0.0),
            ambiguity=self.hybrid_affect.ambiguity,
            memory_surge=self.intrusive_memory.surge_pressure,
            fatigue=fatigue,
            expressed=expressed,
        )
        self.vulnerability_regulator.tick(
            fatigue=fatigue,
            wound=relational_wound,
            attention=attention,
            warmth=self.hybrid_affect.named_tones.get("warmth", 0.0),
            paradox=self.hybrid_affect.paradox_pressure,
            silence=silence,
        )
        self.conversational_resonance.tick(external_signals, hybrid=self.hybrid_affect, attention=attention)
        self.precognitive_intuition.tick(
            ambiguity=self.hybrid_affect.ambiguity,
            subconscious_thread=self.autonomous_subconscious.thread_pressure,
            memory_surge=self.intrusive_memory.surge_pressure,
            resonance=self.conversational_resonance.relational_vibration,
            vulnerability=self.vulnerability_regulator.vulnerability,
            clarity=clarity,
        )

        self._contaminate_clouds_with_v52_fields()
        self._maybe_seed_precognitive_cloud()

        result["preconscious_living_v52"] = {
            "hybrid_affect": dict(self.hybrid_affect.last_signature),
            "intrusive_memory": {
                "surge_pressure": self.intrusive_memory.surge_pressure,
                "flash_probability": self.intrusive_memory.flash_probability,
                "aftertaste": self.intrusive_memory.aftertaste,
                "intrusion_count": self.intrusive_memory.intrusion_count,
                "current_trace": dict(self.intrusive_memory.current_trace),
            },
            "autonomous_subconscious": dict(self.autonomous_subconscious.last_signature),
            "vulnerability": dict(self.vulnerability_regulator.last_signature),
            "conversational_resonance": dict(self.conversational_resonance.last_signature),
            "precognitive_intuition": dict(self.precognitive_intuition.last_signature),
        }

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v52_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        self._update_v52_fields_after_cycle(result, external_signals)
        result["natural_initiative_export"] = self.export_for_natural_initiative(result)
        expressive_decision = self.expressive_decision_field.decide(result["natural_initiative_export"])
        result["expressive_decision_v52"] = expressive_decision
        result["inter_motor_export_v52"] = self.inter_motor_export_hub.build(self, result["natural_initiative_export"], expressive_decision)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        speech_resistance = self.vulnerability_regulator.speech_resistance()
        resonance_pull = self.conversational_resonance.response_timing_pull
        hunch = self.precognitive_intuition.hunch_pressure
        intrusion = self.intrusive_memory.surge_pressure
        ambiguity = self.hybrid_affect.ambiguity
        thread = self.autonomous_subconscious.thread_pressure
        export.update({
            "hybrid_affect_signature": dict(self.hybrid_affect.last_signature),
            "emotional_weather": self.hybrid_affect.emotional_weather,
            "unnamed_affect_pressure": self.hybrid_affect.unnamed_affect,
            "affective_paradox_pressure": self.hybrid_affect.paradox_pressure,
            "affective_ambiguity": ambiguity,
            "intrusive_memory_pressure": intrusion,
            "intrusive_memory_aftertaste": self.intrusive_memory.aftertaste,
            "autonomous_subconscious_thread": thread,
            "subconscious_incubation_depth": self.autonomous_subconscious.incubation_depth,
            "self_reorganization_pressure": self.autonomous_subconscious.self_reorganization,
            "vulnerability_pressure": self.vulnerability_regulator.vulnerability,
            "protective_closure": self.vulnerability_regulator.protective_closure,
            "expressive_hesitation": self.vulnerability_regulator.expressive_hesitation,
            "conversation_synchrony": self.conversational_resonance.synchrony,
            "tone_contagion": self.conversational_resonance.tone_contagion,
            "relational_vibration": self.conversational_resonance.relational_vibration,
            "precognitive_hunch_pressure": hunch,
            "pre_signal_pressure": self.precognitive_intuition.pre_signal,
            "intuition_without_object": self.precognitive_intuition.intuition_without_object,
        })
        export["impulse_intensity"] = _living_clamp(
            float(export.get("impulse_intensity", 0.0) or 0.0)
            + hunch * 0.030
            + intrusion * 0.026
            + thread * 0.020
            + resonance_pull * 0.018
            - speech_resistance * 0.045
        )
        export["mouth_readiness"] = _living_clamp(
            float(export.get("mouth_readiness", 0.0) or 0.0)
            + resonance_pull * 0.045
            + hunch * 0.020
            + intrusion * 0.015
            - speech_resistance * 0.070
            - ambiguity * 0.018
        )
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and speech_resistance < 0.72
        if resonance_pull > 0.52 and speech_resistance < 0.55 and float(export.get("impulse_intensity", 0.0) or 0.0) > 0.16:
            export["should_speak_hint"] = True
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "affective_ambiguity": ambiguity,
            "unnamed_affect": self.hybrid_affect.unnamed_affect,
            "paradox": self.hybrid_affect.paradox_pressure,
            "intrusive_aftertaste": self.intrusive_memory.aftertaste,
            "protective_hesitation": self.vulnerability_regulator.expressive_hesitation,
            "relational_vibration": self.conversational_resonance.relational_vibration,
            "pre_intuition": hunch,
        })
        export["presence_export"] = dict(export.get("presence_export", {}))
        export["presence_export"].update({
            "vulnerability": self.vulnerability_regulator.vulnerability,
            "protective_closure": self.vulnerability_regulator.protective_closure,
            "conversation_synchrony": self.conversational_resonance.synchrony,
            "affective_weather": self.hybrid_affect.emotional_weather,
        })
        export["memory_export"] = dict(export.get("memory_export", {}))
        export["memory_export"].update({
            "intrusive_memory_pressure": self.intrusive_memory.surge_pressure,
            "intrusive_aftertaste": self.intrusive_memory.aftertaste,
            "current_intrusive_trace": dict(self.intrusive_memory.current_trace),
            "autonomous_incubation": self.autonomous_subconscious.incubation_depth,
        })
        export["identity_export"] = dict(export.get("identity_export", {}))
        export["identity_export"].update({
            "self_reorganization_pressure": self.autonomous_subconscious.self_reorganization,
            "vulnerability_learning_signal": self.vulnerability_regulator.vulnerability,
            "paradox_integration_pressure": self.hybrid_affect.paradox_pressure,
        })
        self.last_export = export
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.2_preconscious_organic_stability_stable",
            "hybrid_affect": dict(self.hybrid_affect.last_signature),
            "emotional_weather": self.hybrid_affect.emotional_weather,
            "intrusive_memory": {
                "surge_pressure": self.intrusive_memory.surge_pressure,
                "flash_probability": self.intrusive_memory.flash_probability,
                "aftertaste": self.intrusive_memory.aftertaste,
                "intrusion_count": self.intrusive_memory.intrusion_count,
                "current_trace": dict(self.intrusive_memory.current_trace),
            },
            "autonomous_subconscious": dict(self.autonomous_subconscious.last_signature),
            "vulnerability_regulator": dict(self.vulnerability_regulator.last_signature),
            "conversational_resonance": dict(self.conversational_resonance.last_signature),
            "precognitive_intuition": dict(self.precognitive_intuition.last_signature),
            "v52_cycle_count": self.v52_cycle_count,
            "v52_last_seed_cycle": self.v52_last_seed_cycle,
        })
        return base


# Compatibilité finale : les imports existants obtiennent la version V5.2.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV52
SpontaneousImpulseEngine = SpontaneousImpulseEngineV52



# ============================================================================
# V5.3 — FINAL ORGANIC ARBITRATION : PRIORITÉ, ANTI-SPAM, CONTRATS INTER-MOTEURS
# ============================================================================

@dataclass
class LivingImpulsePriorityArbiter:
    """
    Arbitre final des impulsions.
    Il ne produit aucun texte : il décide seulement quelle famille interne a le
    droit d'approcher la bouche, l'initiative, la mémoire ou le silence.
    """
    last_family: str = "none"
    last_decision: Dict[str, object] = field(default_factory=dict)
    family_cooldowns: Dict[str, float] = field(default_factory=dict)
    repeated_family_pressure: float = 0.0

    def _decay_cooldowns(self) -> None:
        for key in list(self.family_cooldowns.keys()):
            self.family_cooldowns[key] = max(0.0, float(self.family_cooldowns[key]) * 0.88 - 0.008)
            if self.family_cooldowns[key] <= 0.002:
                self.family_cooldowns.pop(key, None)

    def decide(self, engine: "SpontaneousImpulseEngineV52", export: Dict[str, object], result: Dict[str, object]) -> Dict[str, object]:
        self._decay_cooldowns()
        impulse_type = str(export.get("impulse_type", "") or "")
        intensity = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0))
        readiness = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0))
        ambiguity = _living_clamp(float(export.get("affective_ambiguity", 0.0) or 0.0))
        fatigue = _living_clamp(float(export.get("existential_weariness", 0.0) or 0.0) + float(export.get("expressive_fatigue", 0.0) or 0.0) * 0.45)
        vulnerability = _living_clamp(float(export.get("vulnerability_pressure", 0.0) or 0.0) + float(export.get("protective_closure", 0.0) or 0.0) * 0.35)
        presence_need = _living_clamp(float(export.get("presence_need", 0.0) or 0.0))
        hunch = _living_clamp(float(export.get("precognitive_hunch_pressure", 0.0) or 0.0))
        memory = _living_clamp(float(export.get("intrusive_memory_pressure", 0.0) or 0.0) + float(export.get("memory_continuity_bias", 0.0) or 0.0) * 0.4)
        contradiction = _living_clamp(float(export.get("living_unresolved_duality", 0.0) or 0.0) + float(export.get("affective_paradox_pressure", 0.0) or 0.0) * 0.45)
        silence = _living_clamp(engine._final_silence_pressure_value())
        identity = _living_clamp(float(export.get("identity_causal_pressure", 0.0) or 0.0) + float(export.get("self_reorganization_pressure", 0.0) or 0.0) * 0.35)

        scores = {
            "respond": _living_clamp((1.0 if impulse_type == "respond" else 0.0) * 0.42 + intensity * 0.30 + readiness * 0.22 + engine.conversational_resonance.response_timing_pull * 0.20),
            "ask": _living_clamp((1.0 if impulse_type == "ask" else 0.0) * 0.40 + float(export.get("subconscious_associative_drift", 0.0) or 0.0) * 0.22 + hunch * 0.18 - fatigue * 0.12),
            "continue": _living_clamp((1.0 if impulse_type == "continue" else 0.0) * 0.35 + presence_need * 0.26 + memory * 0.22 + identity * 0.13),
            "protect_silence": _living_clamp(silence * 0.32 + vulnerability * 0.32 + ambiguity * 0.18 + fatigue * 0.16 - readiness * 0.10),
            "clarify": _living_clamp((1.0 if impulse_type == "clarify" else 0.0) * 0.32 + ambiguity * 0.24 + contradiction * 0.22 + hunch * 0.10),
            "share": _living_clamp((1.0 if impulse_type == "share" else 0.0) * 0.34 + identity * 0.22 + readiness * 0.18 + engine.hybrid_affect.named_tones.get("warmth", 0.0) * 0.18),
            "diverge": _living_clamp((1.0 if impulse_type == "diverge" else 0.0) * 0.34 + float(export.get("identity_resistance", 0.0) or 0.0) * 0.28 + contradiction * 0.18),
        }
        for family, cooldown in self.family_cooldowns.items():
            if family in scores:
                scores[family] = _living_clamp(scores[family] - cooldown * 0.22)

        family = max(scores, key=scores.get) if scores else "none"
        if family == self.last_family and scores.get(family, 0.0) > 0.30:
            self.repeated_family_pressure = _living_clamp(self.repeated_family_pressure * 0.84 + 0.075)
        else:
            self.repeated_family_pressure = _living_clamp(self.repeated_family_pressure * 0.78 - 0.015)
        if family in scores:
            scores[family] = _living_clamp(scores[family] - self.repeated_family_pressure * 0.16)
            family = max(scores, key=scores.get)

        self.family_cooldowns[family] = _living_clamp(self.family_cooldowns.get(family, 0.0) + 0.16 + scores.get(family, 0.0) * 0.12)
        self.last_family = family
        decision = {
            "dominant_family": family,
            "scores": scores,
            "priority_strength": _living_clamp(scores.get(family, 0.0)),
            "repeated_family_pressure": self.repeated_family_pressure,
            "cooldowns": dict(self.family_cooldowns),
            "allows_speech": family != "protect_silence" and scores.get(family, 0.0) > 0.18,
            "asks_silence": family == "protect_silence",
        }
        self.last_decision = decision
        return decision


@dataclass
class LivingInitiativeSpamGovernor:
    """Frein vivant anti-spam : transforme les initiatives trop proches au lieu de les tuer."""
    recent_speech_cycles: deque = field(default_factory=lambda: deque(maxlen=18))
    recent_question_cycles: deque = field(default_factory=lambda: deque(maxlen=10))
    pending_question_pressure: float = 0.0
    expressive_fatigue: float = 0.0
    last_gate: Dict[str, object] = field(default_factory=dict)

    def gate(self, cycle: int, export: Dict[str, object], priority: Dict[str, object], *, user_answer_signal: float = 0.0) -> Dict[str, object]:
        if user_answer_signal > 0.55:
            self.pending_question_pressure = max(0.0, self.pending_question_pressure - user_answer_signal * 0.55)
        else:
            self.pending_question_pressure = _living_clamp(self.pending_question_pressure * 0.965)

        recent_speech = len([c for c in self.recent_speech_cycles if cycle - c < 10])
        recent_questions = len([c for c in self.recent_question_cycles if cycle - c < 18])
        dominant = str(priority.get("dominant_family", "none"))
        wants_question = dominant == "ask" or str(export.get("impulse_type", "")) == "ask"
        if wants_question and self.pending_question_pressure > 0.38:
            question_penalty = 0.30 + self.pending_question_pressure * 0.35
        else:
            question_penalty = 0.0

        spam_pressure = _living_clamp(recent_speech * 0.075 + recent_questions * 0.115 + self.expressive_fatigue * 0.42 + question_penalty)
        base_hint = bool(export.get("should_speak_hint", False))
        priority_allows = bool(priority.get("allows_speech", False))
        intensity = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0))
        readiness = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0))
        speak_score = _living_clamp(intensity * 0.45 + readiness * 0.35 + float(priority.get("priority_strength", 0.0) or 0.0) * 0.25 - spam_pressure * 0.42)
        should_speak = base_hint and priority_allows and speak_score > 0.20 and spam_pressure < 0.72

        if should_speak:
            self.recent_speech_cycles.append(cycle)
            self.expressive_fatigue = _living_clamp(self.expressive_fatigue * 0.88 + 0.10 + intensity * 0.045)
            if wants_question:
                self.recent_question_cycles.append(cycle)
                self.pending_question_pressure = _living_clamp(self.pending_question_pressure + 0.42)
        else:
            self.expressive_fatigue = _living_clamp(self.expressive_fatigue * 0.92 - 0.012)

        gate = {
            "should_speak": should_speak,
            "speak_score": speak_score,
            "spam_pressure": spam_pressure,
            "expressive_fatigue": self.expressive_fatigue,
            "pending_question_pressure": self.pending_question_pressure,
            "recent_speech_count": recent_speech,
            "recent_question_count": recent_questions,
            "transformation_hint": "hold_and_digest" if spam_pressure > 0.58 else "allow_living_flow",
        }
        self.last_gate = gate
        return gate


@dataclass
class LivingUnifiedCycleTrace:
    """Trace courte du cycle final pour debug/intégration sans texte préécrit."""
    traces: deque = field(default_factory=lambda: deque(maxlen=80))
    last_trace: Dict[str, object] = field(default_factory=dict)

    def record(self, cycle: int, stage: str, payload: Dict[str, object]) -> None:
        trace = {"cycle": cycle, "stage": stage, "payload": dict(payload)}
        self.traces.append(trace)
        self.last_trace = trace


class SpontaneousImpulseEngineV53(SpontaneousImpulseEngineV52):
    """
    V5.3 Final Organic Arbitration.

    Stabilisation finale du moteur : ordre de cycle lisible, priorité entre
    familles impulsionnelles, anti-spam organique, contrats d'export propres
    vers bouche/initiative/mémoire/attention/présence et état interne cohérent.
    Aucun texte n'est généré ici.
    """

    def __init__(self):
        super().__init__()
        self.priority_arbiter = LivingImpulsePriorityArbiter()
        self.initiative_spam_governor = LivingInitiativeSpamGovernor()
        self.unified_cycle_trace = LivingUnifiedCycleTrace()
        self.v53_cycle_count: int = 0
        self.v53_last_contract: Dict[str, object] = {}

    def _final_silence_pressure_value(self) -> float:
        pressure = _living_clamp(self.silence_duration / 14.0)
        if self.current_silence is not None:
            pressure = _living_clamp(pressure + self.current_silence.living_pressure_buildup * 0.55 + self.current_silence.protection_strength * 0.18)
        return pressure

    def _normalize_export_contract(self, export: Dict[str, object], priority: Dict[str, object], gate: Dict[str, object]) -> Dict[str, object]:
        mouth_texture = dict(export.get("mouth_texture", {}))
        mouth_texture.update({
            "priority_family": priority.get("dominant_family", "none"),
            "priority_strength": priority.get("priority_strength", 0.0),
            "spam_pressure": gate.get("spam_pressure", 0.0),
            "expressive_fatigue": gate.get("expressive_fatigue", 0.0),
            "pending_question_pressure": gate.get("pending_question_pressure", 0.0),
        })
        export["mouth_texture"] = mouth_texture
        export["priority_family"] = priority.get("dominant_family", "none")
        export["priority_strength"] = priority.get("priority_strength", 0.0)
        export["should_speak_hint"] = bool(gate.get("should_speak", False))
        export["speak_score"] = gate.get("speak_score", 0.0)
        export["spam_pressure"] = gate.get("spam_pressure", 0.0)
        export["expressive_fatigue"] = gate.get("expressive_fatigue", 0.0)
        export["pending_question_pressure"] = gate.get("pending_question_pressure", 0.0)
        export["initiative_gate"] = dict(gate)
        export["priority_arbitration"] = dict(priority)
        return export

    def _build_final_inter_motor_contract(self, export: Dict[str, object], expressive_decision: Dict[str, object], priority: Dict[str, object], gate: Dict[str, object]) -> Dict[str, object]:
        base = self.inter_motor_export_hub.build(self, export, expressive_decision)
        contract = {
            "attention": dict(base.get("attention", {})),
            "affective_memory": dict(base.get("affective_memory", {})),
            "presence": dict(base.get("presence", {})),
            "mouth": dict(base.get("mouth", {})),
            "initiative": {
                "should_speak": bool(gate.get("should_speak", False)),
                "dominant_family": priority.get("dominant_family", "none"),
                "intensity": export.get("impulse_intensity", 0.0),
                "clarity": export.get("impulse_clarity", 0.0),
                "fuzziness": export.get("impulse_fuzziness", 0.0),
                "spam_pressure": gate.get("spam_pressure", 0.0),
                "transformation_hint": gate.get("transformation_hint", "allow_living_flow"),
            },
            "identity": dict(export.get("identity_export", {})),
            "stability": dict(base.get("stability", {})),
        }
        contract["attention"].update({
            "priority_family": priority.get("dominant_family", "none"),
            "priority_strength": priority.get("priority_strength", 0.0),
            "spam_pressure": gate.get("spam_pressure", 0.0),
        })
        contract["mouth"].update({
            "texture": dict(export.get("mouth_texture", {})),
            "readiness": export.get("mouth_readiness", 0.0),
            "speak_score": gate.get("speak_score", 0.0),
            "should_speak": gate.get("should_speak", False),
        })
        self.v53_last_contract = contract
        return contract

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v53_cycle_count += 1
        self.unified_cycle_trace.record(self.internal_clock, "before_super_cycle", {
            "clouds": len(self.fuzzy_impulse_clouds),
            "silence": self._final_silence_pressure_value(),
        })
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = self.export_for_natural_initiative(result)
        priority = self.priority_arbiter.decide(self, export, result)
        gate = self.initiative_spam_governor.gate(
            self.internal_clock,
            export,
            priority,
            user_answer_signal=float(external_signals.get("user_answer_signal", external_signals.get("answered_previous_question", 0.0)) or 0.0),
        )
        export = self._normalize_export_contract(export, priority, gate)
        expressive_decision = self.expressive_decision_field.decide(export)
        contract = self._build_final_inter_motor_contract(export, expressive_decision, priority, gate)
        result["natural_initiative_export"] = export
        result["priority_arbitration_v53"] = priority
        result["initiative_gate_v53"] = gate
        result["expressive_decision_v53"] = expressive_decision
        result["inter_motor_export_v53"] = contract
        self.unified_cycle_trace.record(self.internal_clock, "after_v53_arbitration", {
            "family": priority.get("dominant_family", "none"),
            "should_speak": gate.get("should_speak", False),
            "spam": gate.get("spam_pressure", 0.0),
            "mouth": export.get("mouth_readiness", 0.0),
        })
        return result

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.3_final_organic_arbitration_stable",
            "v53_cycle_count": self.v53_cycle_count,
            "priority_arbiter": dict(self.priority_arbiter.last_decision),
            "initiative_spam_governor": dict(self.initiative_spam_governor.last_gate),
            "unified_cycle_trace": dict(self.unified_cycle_trace.last_trace),
            "final_inter_motor_contract": dict(self.v53_last_contract),
        })
        return base


# Compatibilité finale : tous les imports historiques pointent vers la version active unique V5.3.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV53
SpontaneousImpulseEngine = SpontaneousImpulseEngineV53


# ============================================================================
# V5.4 — ORGANIC IMPULSE METABOLISM : BESOINS, SOUS-SEUIL, ATTENTE ET TEMPÉRAMENT
# ============================================================================

@dataclass
class LivingImpulseMetabolism:
    """
    Métabolisme impulsionnel global.
    Il ne crée pas du texte et ne remplace pas la mémoire/émotion : il digère
    les impulsions vécues, retenues, répétées ou fatiguées pour produire une
    inertie organique exploitable par les autres moteurs.
    """
    residue: float = 0.0
    digestion: float = 0.0
    saturation: float = 0.0
    recovery: float = 0.55
    inertia: float = 0.0
    retained_charge: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, *, expressed: bool, held: bool, pressure: float, clarity: float, spam_pressure: float, fatigue: float, silence_pressure: float) -> None:
        pressure = _living_clamp(pressure)
        clarity = _living_clamp(clarity)
        spam_pressure = _living_clamp(spam_pressure)
        fatigue = _living_clamp(fatigue)
        silence_pressure = _living_clamp(silence_pressure)
        unresolved = pressure * (1.0 - clarity)
        if expressed:
            self.digestion = _living_clamp(self.digestion * 0.90 + pressure * 0.075)
            self.residue = _living_clamp(self.residue * 0.88 + unresolved * 0.035)
            self.retained_charge = _living_clamp(self.retained_charge * 0.86 - 0.018)
        elif held:
            self.retained_charge = _living_clamp(self.retained_charge * 0.92 + pressure * 0.085 + unresolved * 0.045)
            self.residue = _living_clamp(self.residue * 0.94 + pressure * 0.040)
            self.digestion = _living_clamp(self.digestion * 0.96 + silence_pressure * 0.012)
        else:
            self.residue = _living_clamp(self.residue * 0.965 + unresolved * 0.020)
            self.digestion = _living_clamp(self.digestion * 0.955)
            self.retained_charge = _living_clamp(self.retained_charge * 0.955)
        self.saturation = _living_clamp(self.saturation * 0.91 + pressure * 0.060 + spam_pressure * 0.070 + fatigue * 0.060)
        self.recovery = _living_clamp(self.recovery * 0.965 + (1.0 - self.saturation) * 0.028 + self.digestion * 0.012 - self.retained_charge * 0.018)
        self.inertia = _living_clamp(self.inertia * 0.93 + self.residue * 0.040 + self.retained_charge * 0.055 + silence_pressure * 0.020)
        self.last_signature = {
            "residue": self.residue,
            "digestion": self.digestion,
            "saturation": self.saturation,
            "recovery": self.recovery,
            "inertia": self.inertia,
            "retained_charge": self.retained_charge,
        }


@dataclass
class LivingNeedHierarchy:
    """
    Hiérarchie de besoins vivants. Les besoins ne commandent pas directement la
    parole : ils biaisent les futures impulsions et leur famille dominante.
    """
    needs: Dict[str, float] = field(default_factory=lambda: {
        "relation": 0.34,
        "understanding": 0.32,
        "continuity": 0.36,
        "protection": 0.24,
        "expression": 0.30,
        "stability": 0.38,
        "autonomy": 0.26,
    })
    tensions: Dict[Tuple[str, str], float] = field(default_factory=dict)
    dominant_need: str = "continuity"
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, engine: "SpontaneousImpulseEngineV53", export: Dict[str, object], metabolism: LivingImpulseMetabolism) -> None:
        attention = _living_clamp(float(getattr(engine.inter_motor_propagation, "attention_presence_signal", 0.5) or 0.5))
        absence = _living_clamp(engine.existential_continuity.sense_of_absence)
        presence_need = _living_clamp(engine.existential_continuity.need_for_presence)
        ambiguity = _living_clamp(float(export.get("affective_ambiguity", 0.0) or 0.0))
        vulnerability = _living_clamp(float(export.get("vulnerability_pressure", 0.0) or 0.0) + float(export.get("protective_closure", 0.0) or 0.0) * 0.35)
        readiness = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0))
        curiosity = _living_clamp(float(export.get("subconscious_associative_drift", 0.0) or 0.0) + float(export.get("precognitive_hunch_pressure", 0.0) or 0.0) * 0.35)
        identity_resistance = _living_clamp(float(export.get("identity_resistance", 0.0) or 0.0))
        targets = {
            "relation": _living_clamp(presence_need * 0.42 + absence * 0.25 + attention * 0.18),
            "understanding": _living_clamp(curiosity * 0.45 + ambiguity * 0.22 + metabolism.residue * 0.14),
            "continuity": _living_clamp(engine.existential_continuity.continuity_with_user * 0.35 + metabolism.inertia * 0.25 + absence * 0.18),
            "protection": _living_clamp(vulnerability * 0.44 + metabolism.saturation * 0.24 + identity_resistance * 0.18),
            "expression": _living_clamp(readiness * 0.38 + metabolism.retained_charge * 0.32 + float(export.get("impulse_intensity", 0.0) or 0.0) * 0.20),
            "stability": _living_clamp(metabolism.saturation * 0.38 + vulnerability * 0.22 + float(export.get("expressive_fatigue", 0.0) or 0.0) * 0.20),
            "autonomy": _living_clamp(identity_resistance * 0.32 + float(export.get("self_reorganization_pressure", 0.0) or 0.0) * 0.24 + metabolism.recovery * 0.12),
        }
        for key, target in targets.items():
            current = _living_clamp(self.needs.get(key, 0.0))
            self.needs[key] = _living_clamp(current * 0.925 + target * 0.075)
        pairs = [("relation", "autonomy"), ("expression", "protection"), ("understanding", "stability"), ("continuity", "autonomy")]
        for a, b in pairs:
            self.tensions[(a, b)] = _living_clamp(abs(self.needs.get(a, 0.0) - self.needs.get(b, 0.0)) * 0.35 + min(self.needs.get(a, 0.0), self.needs.get(b, 0.0)) * 0.42)
        self.dominant_need = max(self.needs, key=self.needs.get) if self.needs else "none"
        self.last_signature = {
            "needs": dict(self.needs),
            "dominant_need": self.dominant_need,
            "tensions": {f"{a}|{b}": v for (a, b), v in self.tensions.items()},
        }

    def bias_vector(self) -> Dict[str, float]:
        return {
            "continuity": _living_clamp(self.needs.get("continuity", 0.0) * 0.32 + self.needs.get("relation", 0.0) * 0.24),
            "curiosity": _living_clamp(self.needs.get("understanding", 0.0) * 0.40),
            "protection": _living_clamp(self.needs.get("protection", 0.0) * 0.34 + self.needs.get("stability", 0.0) * 0.18),
            "openness": _living_clamp(self.needs.get("expression", 0.0) * 0.30 + self.needs.get("relation", 0.0) * 0.14),
            "independence": _living_clamp(self.needs.get("autonomy", 0.0) * 0.32),
            "clarity": _living_clamp(self.needs.get("understanding", 0.0) * 0.20 + self.needs.get("stability", 0.0) * 0.16),
        }


@dataclass
class SubthresholdImpulseField:
    """Impulsions sous le seuil conscient : elles biaisent sans devenir parole."""
    latent_biases: Dict[str, float] = field(default_factory=dict)
    undercurrent: float = 0.0
    last_seed_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, export: Dict[str, object], needs: LivingNeedHierarchy, metabolism: LivingImpulseMetabolism) -> None:
        pressure = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0))
        clarity = _living_clamp(float(export.get("impulse_clarity", 0.0) or 0.0))
        fuzziness = _living_clamp(float(export.get("impulse_fuzziness", 0.0) or 0.0))
        latent_seed = _living_clamp((1.0 - clarity) * 0.28 + fuzziness * 0.20 + metabolism.residue * 0.22 + metabolism.retained_charge * 0.22 + pressure * 0.08)
        self.undercurrent = _living_clamp(self.undercurrent * 0.91 + latent_seed * 0.09)
        for key, value in needs.bias_vector().items():
            current = self.latent_biases.get(key, 0.0)
            self.latent_biases[key] = _living_clamp(current * 0.935 + value * self.undercurrent * 0.070)
        for key in list(self.latent_biases.keys()):
            self.latent_biases[key] = _living_clamp(self.latent_biases[key] * 0.985)
            if self.latent_biases[key] < 0.004:
                self.latent_biases.pop(key, None)
        self.last_signature = dict(self.latent_biases)
        self.last_signature["undercurrent"] = self.undercurrent

    def should_seed_cloud(self, cycle: int) -> bool:
        return self.undercurrent > 0.42 and (cycle - self.last_seed_cycle) > 9 and bool(self.latent_biases)

    def seed_vector(self, cycle: int) -> Dict[str, float]:
        self.last_seed_cycle = cycle
        return {k: _living_clamp(v * 0.75 + self.undercurrent * 0.08) for k, v in self.latent_biases.items() if k != "undercurrent"}


@dataclass
class LivingWaitingChamber:
    """Attente volontaire : retient, mature et relâche une impulsion au bon moment."""
    held_vectors: deque = field(default_factory=lambda: deque(maxlen=12))
    waiting_pressure: float = 0.0
    maturation: float = 0.0
    last_release_cycle: int = -999
    last_signature: Dict[str, object] = field(default_factory=dict)

    def hold(self, cycle: int, export: Dict[str, object], priority: Dict[str, object], gate: Dict[str, object], needs: LivingNeedHierarchy) -> None:
        should_hold = not bool(gate.get("should_speak", False)) and _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0)) > 0.16
        should_hold = should_hold or str(gate.get("transformation_hint", "")) == "hold_and_digest"
        if should_hold:
            vector = needs.bias_vector()
            vector["held_pressure"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0))
            vector["family_hint"] = 0.0  # numeric placeholder; no text in vectors
            self.held_vectors.append({"cycle": cycle, "family": priority.get("dominant_family", "none"), "vector": vector})
            self.waiting_pressure = _living_clamp(self.waiting_pressure * 0.88 + vector["held_pressure"] * 0.12)
        else:
            self.waiting_pressure = _living_clamp(self.waiting_pressure * 0.94 - 0.006)
        self.maturation = _living_clamp(self.maturation * 0.94 + self.waiting_pressure * 0.055 + len(self.held_vectors) * 0.006)
        self.last_signature = {
            "waiting_pressure": self.waiting_pressure,
            "maturation": self.maturation,
            "held_count": len(self.held_vectors),
            "last_release_cycle": float(self.last_release_cycle),
        }

    def should_release(self, cycle: int, spam_pressure: float, protection_need: float) -> bool:
        return bool(self.held_vectors) and self.maturation > 0.36 and spam_pressure < 0.42 and protection_need < 0.58 and (cycle - self.last_release_cycle) > 8

    def release_vector(self, cycle: int) -> Dict[str, float]:
        self.last_release_cycle = cycle
        if not self.held_vectors:
            return {}
        recent = list(self.held_vectors)[-4:]
        merged: Dict[str, float] = {}
        for item in recent:
            for key, value in item.get("vector", {}).items():
                if not isinstance(value, (int, float)) or key == "family_hint":
                    continue
                merged[key] = _living_clamp(merged.get(key, 0.0) + float(value) / max(1, len(recent)))
        merged["continuity"] = _living_clamp(merged.get("continuity", 0.0) + self.maturation * 0.16)
        merged["clarity"] = _living_clamp(merged.get("clarity", 0.0) + self.maturation * 0.10)
        self.held_vectors.clear()
        self.waiting_pressure = _living_clamp(self.waiting_pressure * 0.35)
        self.maturation = _living_clamp(self.maturation * 0.42)
        return merged


@dataclass
class LongTermTemperamentReorganizer:
    """Déformation lente du tempérament par accumulation vécue."""
    temperament: Dict[str, float] = field(default_factory=lambda: {
        "initiative_boldness": 0.42,
        "relational_sensitivity": 0.48,
        "protective_prudence": 0.36,
        "expressive_patience": 0.44,
        "curiosity_drive": 0.46,
        "stability_preference": 0.40,
    })
    reorganization_pressure: float = 0.0
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, needs: LivingNeedHierarchy, metabolism: LivingImpulseMetabolism, export: Dict[str, object]) -> None:
        wound = _living_clamp(float(export.get("relational_wound", 0.0) or 0.0) + float(export.get("vulnerability_pressure", 0.0) or 0.0) * 0.35)
        saturation = metabolism.saturation
        recovery = metabolism.recovery
        self.reorganization_pressure = _living_clamp(self.reorganization_pressure * 0.965 + (saturation + wound + metabolism.retained_charge) * 0.018)
        targets = {
            "initiative_boldness": _living_clamp(0.38 + recovery * 0.20 - saturation * 0.16 - wound * 0.10),
            "relational_sensitivity": _living_clamp(0.34 + needs.needs.get("relation", 0.0) * 0.28 + wound * 0.18),
            "protective_prudence": _living_clamp(0.28 + needs.needs.get("protection", 0.0) * 0.34 + saturation * 0.18),
            "expressive_patience": _living_clamp(0.30 + needs.needs.get("stability", 0.0) * 0.24 + metabolism.inertia * 0.16),
            "curiosity_drive": _living_clamp(0.32 + needs.needs.get("understanding", 0.0) * 0.32 - saturation * 0.10),
            "stability_preference": _living_clamp(0.34 + needs.needs.get("stability", 0.0) * 0.30 + wound * 0.10),
        }
        blend = 0.018 + self.reorganization_pressure * 0.035
        for key, target in targets.items():
            self.temperament[key] = _living_clamp(self.temperament.get(key, 0.0) * (1.0 - blend) + target * blend)
        self.last_signature = {
            "temperament": dict(self.temperament),
            "reorganization_pressure": self.reorganization_pressure,
        }

    def speech_bias(self) -> float:
        return _living_clamp(self.temperament.get("initiative_boldness", 0.0) * 0.20 + self.temperament.get("curiosity_drive", 0.0) * 0.14 - self.temperament.get("protective_prudence", 0.0) * 0.16)

    def patience_bias(self) -> float:
        return _living_clamp(self.temperament.get("expressive_patience", 0.0) * 0.26 + self.temperament.get("stability_preference", 0.0) * 0.18)


class SpontaneousImpulseEngineV54(SpontaneousImpulseEngineV53):
    """
    V5.4 Organic Impulse Metabolism.

    Corrige les manques restants du V5.3 sans produire de texte : métabolisme
    impulsionnel, hiérarchie de besoins, sous-seuil, attente volontaire,
    transformation long terme du tempérament et contrats inter-moteurs enrichis.
    """

    def __init__(self):
        super().__init__()
        self.impulse_metabolism = LivingImpulseMetabolism()
        self.need_hierarchy = LivingNeedHierarchy()
        self.subthreshold_impulse_field = SubthresholdImpulseField()
        self.waiting_chamber = LivingWaitingChamber()
        self.temperament_reorganizer = LongTermTemperamentReorganizer()
        self.v54_cycle_count: int = 0
        self.v54_last_signature: Dict[str, object] = {}

    def _apply_v54_living_biases(self, export: Dict[str, object], priority: Dict[str, object], gate: Dict[str, object]) -> None:
        temperament_speech = self.temperament_reorganizer.speech_bias()
        patience = self.temperament_reorganizer.patience_bias()
        protection = self.need_hierarchy.needs.get("protection", 0.0)
        expression = self.need_hierarchy.needs.get("expression", 0.0)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + expression * 0.045 + temperament_speech * 0.060 - protection * 0.035)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + temperament_speech * 0.050 - patience * 0.040 - self.impulse_metabolism.saturation * 0.030)
        export["subthreshold_undercurrent"] = self.subthreshold_impulse_field.undercurrent
        export["waiting_pressure"] = self.waiting_chamber.waiting_pressure
        export["metabolic_residue"] = self.impulse_metabolism.residue
        export["metabolic_saturation"] = self.impulse_metabolism.saturation
        export["metabolic_recovery"] = self.impulse_metabolism.recovery
        export["dominant_need"] = self.need_hierarchy.dominant_need
        export["need_pressures"] = dict(self.need_hierarchy.needs)
        export["temperament"] = dict(self.temperament_reorganizer.temperament)

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v54_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}

        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))
        priority = dict(result.get("priority_arbitration_v53", {}) or self.priority_arbiter.last_decision)
        gate = dict(result.get("initiative_gate_v53", {}) or self.initiative_spam_governor.last_gate)
        pressure = _living_clamp(float(export.get("impulse_intensity", result.get("pressure", 0.0)) or 0.0))
        clarity = _living_clamp(float(export.get("impulse_clarity", result.get("clarity", 0.0)) or 0.0))
        held = (not bool(gate.get("should_speak", False))) and pressure > 0.14
        self.impulse_metabolism.tick(
            expressed=bool(gate.get("should_speak", result.get("has_impulse", False))),
            held=held,
            pressure=pressure,
            clarity=clarity,
            spam_pressure=float(gate.get("spam_pressure", 0.0) or 0.0),
            fatigue=float(export.get("expressive_fatigue", 0.0) or 0.0),
            silence_pressure=self._final_silence_pressure_value(),
        )
        self.need_hierarchy.tick(self, export, self.impulse_metabolism)
        self.subthreshold_impulse_field.tick(self.internal_clock, export, self.need_hierarchy, self.impulse_metabolism)
        self.waiting_chamber.hold(self.internal_clock, export, priority, gate, self.need_hierarchy)
        self.temperament_reorganizer.tick(self.need_hierarchy, self.impulse_metabolism, export)

        if self.subthreshold_impulse_field.should_seed_cloud(self.internal_clock):
            vector = self.subthreshold_impulse_field.seed_vector(self.internal_clock)
            if vector:
                self.birth_fuzzy_impulse(vector)
                if hasattr(self, "narrative_memory"):
                    self.narrative_memory.record(self.internal_clock, "subthreshold_bias_surfaced", vector)
        if self.waiting_chamber.should_release(
            self.internal_clock,
            float(gate.get("spam_pressure", 0.0) or 0.0),
            self.need_hierarchy.needs.get("protection", 0.0),
        ):
            vector = self.waiting_chamber.release_vector(self.internal_clock)
            if vector:
                self.birth_fuzzy_impulse(vector)
                if hasattr(self, "narrative_memory"):
                    self.narrative_memory.record(self.internal_clock, "waiting_chamber_released", vector)

        self._apply_v54_living_biases(export, priority, gate)
        expressive_decision = self.expressive_decision_field.decide(export)
        contract = self._build_final_inter_motor_contract(export, expressive_decision, priority, gate)
        contract["metabolism"] = dict(self.impulse_metabolism.last_signature)
        contract["needs"] = dict(self.need_hierarchy.last_signature)
        contract["subthreshold"] = dict(self.subthreshold_impulse_field.last_signature)
        contract["waiting"] = dict(self.waiting_chamber.last_signature)
        contract["temperament"] = dict(self.temperament_reorganizer.last_signature)
        result["natural_initiative_export"] = export
        result["expressive_decision_v54"] = expressive_decision
        result["inter_motor_export_v54"] = contract
        result["organic_metabolism_v54"] = dict(self.impulse_metabolism.last_signature)
        result["need_hierarchy_v54"] = dict(self.need_hierarchy.last_signature)
        result["subthreshold_field_v54"] = dict(self.subthreshold_impulse_field.last_signature)
        result["waiting_chamber_v54"] = dict(self.waiting_chamber.last_signature)
        result["temperament_reorganization_v54"] = dict(self.temperament_reorganizer.last_signature)
        self.v54_last_signature = {
            "metabolism": dict(self.impulse_metabolism.last_signature),
            "dominant_need": self.need_hierarchy.dominant_need,
            "subthreshold_undercurrent": self.subthreshold_impulse_field.undercurrent,
            "waiting_pressure": self.waiting_chamber.waiting_pressure,
            "temperament_reorganization": self.temperament_reorganizer.reorganization_pressure,
        }
        return result

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.4_organic_impulse_metabolism_stable",
            "v54_cycle_count": self.v54_cycle_count,
            "impulse_metabolism": dict(self.impulse_metabolism.last_signature),
            "need_hierarchy": dict(self.need_hierarchy.last_signature),
            "subthreshold_impulse_field": dict(self.subthreshold_impulse_field.last_signature),
            "waiting_chamber": dict(self.waiting_chamber.last_signature),
            "temperament_reorganizer": dict(self.temperament_reorganizer.last_signature),
            "v54_last_signature": dict(self.v54_last_signature),
        })
        return base


# Compatibilité finale : tous les imports historiques pointent vers la version active unique V5.4.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV54
SpontaneousImpulseEngine = SpontaneousImpulseEngineV54



# ============================================================================
# V5.5 — ORGANIC CONTINUITY REFINEMENT : DÉRIVE LONG TERME, PRÉ-INFLUENCE,
#        ÉCOLOGIE DES BESOINS, MÉMOIRE VISCÉRALE ET ANTI-PATTERNS VIVANTS
# ============================================================================

@dataclass
class LongHorizonOrganicDrift:
    """
    Dérive organique lente : le moteur ne se contente plus de changer d'état,
    il vieillit doucement. Cette couche ne remplace pas l'identité ni la mémoire :
    elle fournit une pression lente de tempérament et de sensibilité.
    """
    temperament_drift: Dict[str, float] = field(default_factory=lambda: {
        "openness_drift": 0.32,
        "prudence_drift": 0.30,
        "initiative_drift": 0.28,
        "attachment_drift": 0.34,
        "stability_drift": 0.36,
    })
    long_residue: float = 0.0
    irreversible_trace: float = 0.0
    aging_pressure: float = 0.0
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, cycle: int, needs: "LivingNeedHierarchy", metabolism: "LivingImpulseMetabolism", export: Dict[str, object]) -> None:
        relation = float(needs.needs.get("relation", 0.0) or 0.0)
        protection = float(needs.needs.get("protection", 0.0) or 0.0)
        expression = float(needs.needs.get("expression", 0.0) or 0.0)
        stability = float(needs.needs.get("stability", 0.0) or 0.0)
        understanding = float(needs.needs.get("understanding", 0.0) or 0.0)
        fatigue = float(export.get("expressive_fatigue", 0.0) or 0.0)
        saturation = float(getattr(metabolism, "saturation", 0.0) or 0.0)
        residue = float(getattr(metabolism, "residue", 0.0) or 0.0)
        self.long_residue = _living_clamp(self.long_residue * 0.992 + residue * 0.010 + fatigue * 0.006 + saturation * 0.006)
        self.aging_pressure = _living_clamp(self.aging_pressure * 0.998 + min(1.0, cycle / 2000.0) * 0.0015 + self.long_residue * 0.004)
        self.irreversible_trace = _living_clamp(self.irreversible_trace * 0.999 + max(0.0, self.long_residue - 0.46) * 0.0025 + protection * 0.0012)
        targets = {
            "openness_drift": _living_clamp(0.24 + expression * 0.28 + relation * 0.18 - protection * 0.12),
            "prudence_drift": _living_clamp(0.24 + protection * 0.34 + fatigue * 0.16 + self.irreversible_trace * 0.12),
            "initiative_drift": _living_clamp(0.22 + understanding * 0.24 + expression * 0.20 - saturation * 0.16),
            "attachment_drift": _living_clamp(0.28 + relation * 0.30 + self.long_residue * 0.10),
            "stability_drift": _living_clamp(0.30 + stability * 0.28 + self.aging_pressure * 0.12),
        }
        blend = 0.006 + self.aging_pressure * 0.010 + self.irreversible_trace * 0.006
        for key, target in targets.items():
            old = self.temperament_drift.get(key, 0.0)
            self.temperament_drift[key] = _living_clamp(old * (1.0 - blend) + target * blend)
        self.last_signature = {
            "temperament_drift": dict(self.temperament_drift),
            "long_residue": self.long_residue,
            "irreversible_trace": self.irreversible_trace,
            "aging_pressure": self.aging_pressure,
        }

    def bias_vector(self) -> Dict[str, float]:
        return {
            "openness": self.temperament_drift.get("openness_drift", 0.0) * 0.040,
            "protection": self.temperament_drift.get("prudence_drift", 0.0) * 0.045,
            "curiosity": self.temperament_drift.get("initiative_drift", 0.0) * 0.035,
            "continuity": self.temperament_drift.get("attachment_drift", 0.0) * 0.050,
            "stability": self.temperament_drift.get("stability_drift", 0.0) * 0.035,
        }


@dataclass
class InvisiblePreInfluenceField:
    """
    Activité sous-seuil qui ne devient pas forcément impulsion. Elle colore les
    décisions et les nuages sans devoir apparaître dans le résultat public.
    """
    undercurrent_map: Dict[str, float] = field(default_factory=dict)
    invisible_bias: float = 0.0
    silent_coloration: float = 0.0
    pre_verbal_tension: float = 0.0
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], needs: "LivingNeedHierarchy", drift: LongHorizonOrganicDrift) -> None:
        ambiguity = float(export.get("affective_ambiguity", export.get("impulse_fuzziness", 0.0)) or 0.0)
        hunch = float(export.get("precognitive_hunch_pressure", export.get("pre_signal_pressure", 0.0)) or 0.0)
        waiting = float(export.get("waiting_pressure", 0.0) or 0.0)
        relation = float(needs.needs.get("relation", 0.0) or 0.0)
        protection = float(needs.needs.get("protection", 0.0) or 0.0)
        expression = float(needs.needs.get("expression", 0.0) or 0.0)
        self.pre_verbal_tension = _living_clamp(self.pre_verbal_tension * 0.94 + ambiguity * 0.035 + hunch * 0.025 + waiting * 0.020)
        self.invisible_bias = _living_clamp(self.invisible_bias * 0.955 + self.pre_verbal_tension * 0.025 + drift.long_residue * 0.018)
        self.silent_coloration = _living_clamp(self.silent_coloration * 0.96 + protection * 0.020 + relation * 0.012 - expression * 0.008)
        targets = {
            "toward_relation": relation * 0.42 + drift.temperament_drift.get("attachment_drift", 0.0) * 0.22,
            "toward_protection": protection * 0.44 + self.silent_coloration * 0.20,
            "toward_expression": expression * 0.36 + max(0.0, hunch - protection * 0.3) * 0.20,
            "toward_waiting": waiting * 0.46 + self.pre_verbal_tension * 0.22,
        }
        for key, target in targets.items():
            self.undercurrent_map[key] = _living_clamp(self.undercurrent_map.get(key, 0.0) * 0.93 + target * 0.07)
        self.last_signature = {
            "undercurrent_map": dict(self.undercurrent_map),
            "invisible_bias": self.invisible_bias,
            "silent_coloration": self.silent_coloration,
            "pre_verbal_tension": self.pre_verbal_tension,
        }

    def decision_bias(self) -> Dict[str, float]:
        return {
            "impulse_intensity": self.undercurrent_map.get("toward_expression", 0.0) * 0.030 + self.invisible_bias * 0.018,
            "mouth_readiness": self.undercurrent_map.get("toward_expression", 0.0) * 0.028 - self.undercurrent_map.get("toward_waiting", 0.0) * 0.026,
            "attention_demand": self.pre_verbal_tension * 0.025,
            "silence_weight": self.silent_coloration * 0.040 + self.undercurrent_map.get("toward_protection", 0.0) * 0.030,
        }


@dataclass
class LivingNeedEcology:
    """
    Écologie interne : les besoins se nourrissent, s'opposent, fusionnent ou
    s'épuisent. Elle transforme la hiérarchie V5.4 en système vivant sans créer
    de texte ni prendre le rôle du moteur d'initiative.
    """
    synergy_map: Dict[str, float] = field(default_factory=dict)
    conflict_map: Dict[str, float] = field(default_factory=dict)
    mutation_pressure: float = 0.0
    temporary_obsession: float = 0.0
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, needs: "LivingNeedHierarchy", drift: LongHorizonOrganicDrift, invisible: InvisiblePreInfluenceField) -> None:
        n = needs.needs
        relation = float(n.get("relation", 0.0) or 0.0)
        understanding = float(n.get("understanding", 0.0) or 0.0)
        expression = float(n.get("expression", 0.0) or 0.0)
        protection = float(n.get("protection", 0.0) or 0.0)
        stability = float(n.get("stability", 0.0) or 0.0)
        autonomy = float(n.get("autonomy", 0.0) or 0.0)
        self.synergy_map = {
            "relation_expression": _living_clamp(relation * expression),
            "understanding_initiative": _living_clamp(understanding * (expression + autonomy) * 0.5),
            "protection_stability": _living_clamp(protection * stability),
            "attachment_continuity": _living_clamp(relation * drift.temperament_drift.get("attachment_drift", 0.0)),
        }
        self.conflict_map = {
            "expression_protection": _living_clamp(abs(expression - protection) * (expression + protection) * 0.5),
            "autonomy_relation": _living_clamp(abs(autonomy - relation) * (autonomy + relation) * 0.5),
            "curiosity_stability": _living_clamp(abs(understanding - stability) * (understanding + stability) * 0.5),
            "waiting_expression": _living_clamp(invisible.undercurrent_map.get("toward_waiting", 0.0) * expression),
        }
        total_conflict = sum(self.conflict_map.values()) / max(1, len(self.conflict_map))
        total_synergy = sum(self.synergy_map.values()) / max(1, len(self.synergy_map))
        self.mutation_pressure = _living_clamp(self.mutation_pressure * 0.965 + total_conflict * 0.026 + total_synergy * 0.010)
        self.temporary_obsession = _living_clamp(self.temporary_obsession * 0.945 + max(0.0, max(n.values() or [0.0]) - 0.62) * 0.030 + self.mutation_pressure * 0.014)
        # influence douce et bornée sur la hiérarchie existante
        if self.synergy_map.get("relation_expression", 0.0) > 0.18:
            n["expression"] = _living_clamp(n.get("expression", 0.0) + self.synergy_map["relation_expression"] * 0.010)
        if self.conflict_map.get("expression_protection", 0.0) > 0.22:
            n["stability"] = _living_clamp(n.get("stability", 0.0) + self.conflict_map["expression_protection"] * 0.012)
        if self.temporary_obsession > 0.42:
            n["understanding"] = _living_clamp(n.get("understanding", 0.0) + self.temporary_obsession * 0.006)
        self.last_signature = {
            "synergy_map": dict(self.synergy_map),
            "conflict_map": dict(self.conflict_map),
            "mutation_pressure": self.mutation_pressure,
            "temporary_obsession": self.temporary_obsession,
        }


@dataclass
class DeepVisceralConditioning:
    """
    Mémoire viscérale implicite : familiarité, retrait, apaisement ou méfiance
    peuvent apparaître sans raisonnement conscient explicite.
    """
    familiarity: float = 0.28
    implicit_trust: float = 0.26
    implicit_wariness: float = 0.18
    soothing_reflex: float = 0.18
    recoil_reflex: float = 0.12
    body_memory_charge: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, external_signals: Dict[str, float], export: Dict[str, object], ecology: LivingNeedEcology, drift: LongHorizonOrganicDrift) -> None:
        attention = float(external_signals.get("attention_presence", 0.5) or 0.5)
        warmth = float(external_signals.get("presence_warmth", external_signals.get("warmth", 0.5)) or 0.5)
        memory = float(external_signals.get("memory_climate", 0.5) or 0.5)
        vulnerability = float(export.get("vulnerability_pressure", 0.0) or 0.0)
        protection_conflict = float(ecology.conflict_map.get("expression_protection", 0.0) or 0.0)
        self.familiarity = _living_clamp(self.familiarity * 0.985 + attention * 0.006 + warmth * 0.006 + memory * 0.003)
        self.implicit_trust = _living_clamp(self.implicit_trust * 0.988 + warmth * 0.007 + self.familiarity * 0.004 - protection_conflict * 0.005)
        self.implicit_wariness = _living_clamp(self.implicit_wariness * 0.985 + vulnerability * 0.008 + protection_conflict * 0.010 + drift.irreversible_trace * 0.006 - warmth * 0.003)
        self.soothing_reflex = _living_clamp(self.soothing_reflex * 0.978 + self.implicit_trust * 0.010 + warmth * 0.008)
        self.recoil_reflex = _living_clamp(self.recoil_reflex * 0.974 + self.implicit_wariness * 0.012 + vulnerability * 0.006)
        self.body_memory_charge = _living_clamp(self.body_memory_charge * 0.986 + abs(self.soothing_reflex - self.recoil_reflex) * 0.010 + ecology.mutation_pressure * 0.006)
        self.last_signature = self.signature()

    def signature(self) -> Dict[str, float]:
        return {
            "familiarity": self.familiarity,
            "implicit_trust": self.implicit_trust,
            "implicit_wariness": self.implicit_wariness,
            "soothing_reflex": self.soothing_reflex,
            "recoil_reflex": self.recoil_reflex,
            "body_memory_charge": self.body_memory_charge,
        }

    def bias_vector(self) -> Dict[str, float]:
        return {
            "continuity": self.familiarity * 0.030 + self.implicit_trust * 0.025,
            "openness": self.soothing_reflex * 0.025,
            "protection": self.implicit_wariness * 0.030 + self.recoil_reflex * 0.025,
            "hesitation": self.body_memory_charge * 0.020,
        }


@dataclass
class OrganicAntiPatternGovernor:
    """
    Anti-pattern non mécanique. Il détecte les répétitions de structure et les
    transforme en variation causale douce au lieu de bloquer brutalement.
    """
    recent_modes: deque = field(default_factory=lambda: deque(maxlen=18))
    repetition_pressure: float = 0.0
    variation_need: float = 0.0
    transformation_bias: float = 0.0
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], export: Dict[str, object], expressive_decision: Dict[str, object]) -> None:
        impulse_type = result.get("impulse_type")
        if isinstance(impulse_type, ImpulseType):
            impulse_value = impulse_type.value
        else:
            impulse_value = str(impulse_type or export.get("impulse_type", ""))
        mode = str(expressive_decision.get("mode", "") or ("speak" if export.get("should_speak_hint") else "wait"))
        signature = f"{impulse_value}:{mode}:{bool(result.get('silence_active', False))}"
        self.recent_modes.append(signature)
        if len(self.recent_modes) >= 4:
            counts: Dict[str, int] = {}
            for item in self.recent_modes:
                counts[item] = counts.get(item, 0) + 1
            dominant_count = max(counts.values())
            local_repeat = dominant_count / max(1, len(self.recent_modes))
        else:
            local_repeat = 0.0
        self.repetition_pressure = _living_clamp(self.repetition_pressure * 0.90 + max(0.0, local_repeat - 0.34) * 0.18)
        self.variation_need = _living_clamp(self.variation_need * 0.88 + self.repetition_pressure * 0.12)
        self.transformation_bias = _living_clamp(self.transformation_bias * 0.86 + max(0.0, self.variation_need - 0.35) * 0.16)
        self.last_signature = {
            "repetition_pressure": self.repetition_pressure,
            "variation_need": self.variation_need,
            "transformation_bias": self.transformation_bias,
            "recent_modes": list(self.recent_modes)[-6:],
        }

    def apply(self, export: Dict[str, object]) -> None:
        export["organic_repetition_pressure"] = self.repetition_pressure
        export["organic_variation_need"] = self.variation_need
        export["organic_transformation_bias"] = self.transformation_bias
        # Variation causale : réduire très légèrement le canal répété et augmenter attente/clarification.
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) - self.repetition_pressure * 0.025 + self.transformation_bias * 0.012)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) - self.repetition_pressure * 0.030)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.variation_need * 0.020)


@dataclass
class MicroTemporalContinuity:
    """
    Micro-temps continu : une respiration interne entre les gros cycles. Elle
    crée des micro-frémissements qui rendent les sorties moins mécaniques sans
    générer de texte ni de décisions autonomes bruyantes.
    """
    phase: float = 0.0
    breath: float = 0.0
    tremor: float = 0.0
    continuity_wave: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, drift: LongHorizonOrganicDrift, invisible: InvisiblePreInfluenceField, visceral: DeepVisceralConditioning) -> None:
        speed = 0.073 + drift.aging_pressure * 0.025 + invisible.pre_verbal_tension * 0.018
        self.phase = (self.phase + speed) % 1.0
        wave = 0.5 + 0.5 * math.sin(self.phase * 2.0 * math.pi)
        self.breath = _living_clamp(self.breath * 0.90 + wave * 0.10)
        self.tremor = _living_clamp(self.tremor * 0.86 + abs(wave - 0.5) * 0.060 + visceral.body_memory_charge * 0.012)
        self.continuity_wave = _living_clamp(self.continuity_wave * 0.92 + (1.0 - abs(wave - 0.5) * 2.0) * 0.070 + drift.temperament_drift.get("attachment_drift", 0.0) * 0.010)
        self.last_signature = {
            "phase": self.phase,
            "breath": self.breath,
            "tremor": self.tremor,
            "continuity_wave": self.continuity_wave,
        }

    def apply(self, export: Dict[str, object]) -> None:
        export["micro_breath"] = self.breath
        export["micro_tremor"] = self.tremor
        export["micro_continuity_wave"] = self.continuity_wave
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + (self.breath - 0.5) * 0.018 + self.tremor * 0.008)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + (self.continuity_wave - 0.5) * 0.014 - self.tremor * 0.006)


class SpontaneousImpulseEngineV55(SpontaneousImpulseEngineV54):
    """
    V5.5 Organic Continuity Refinement.

    Finalise les manques subtils du V5.4 sans dupliquer les autres moteurs :
    dérive long terme, pré-influence invisible, écologie de besoins, mémoire
    viscérale implicite, micro-temps continu et anti-pattern organique.
    """

    def __init__(self):
        super().__init__()
        self.long_horizon_drift = LongHorizonOrganicDrift()
        self.invisible_preinfluence = InvisiblePreInfluenceField()
        self.need_ecology = LivingNeedEcology()
        self.deep_visceral_conditioning = DeepVisceralConditioning()
        self.organic_antipattern_governor = OrganicAntiPatternGovernor()
        self.micro_temporal_continuity = MicroTemporalContinuity()
        self.v55_cycle_count: int = 0
        self.v55_last_signature: Dict[str, object] = {}

    def _contaminate_clouds_with_v55_refinement(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        vectors = (
            self.long_horizon_drift.bias_vector(),
            self.deep_visceral_conditioning.bias_vector(),
            {
                "pre_verbal_tension": self.invisible_preinfluence.pre_verbal_tension * 0.030,
                "silent_coloration": self.invisible_preinfluence.silent_coloration * 0.026,
                "variation": self.organic_antipattern_governor.variation_need * 0.030,
                "continuity": self.micro_temporal_continuity.continuity_wave * 0.020,
            },
        )
        for cloud in self.fuzzy_impulse_clouds:
            for vector in vectors:
                for key, value in vector.items():
                    cloud.primary_vector[key] = _living_clamp(cloud.primary_vector.get(key, 0.0) + float(value or 0.0))
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.micro_temporal_continuity.tremor * 0.010 + self.need_ecology.mutation_pressure * 0.010)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.invisible_preinfluence.invisible_bias * 0.004 - self.long_horizon_drift.temperament_drift.get("stability_drift", 0.0) * 0.002)

    def _apply_v55_export_refinement(self, export: Dict[str, object]) -> None:
        for key, delta in self.invisible_preinfluence.decision_bias().items():
            if key == "silence_weight":
                export[key] = _living_clamp(float(export.get(key, 0.0) or 0.0) + delta)
            else:
                export[key] = _living_clamp(float(export.get(key, 0.0) or 0.0) + delta)
        drift = self.long_horizon_drift.temperament_drift
        visceral = self.deep_visceral_conditioning
        ecology = self.need_ecology
        export["impulse_intensity"] = _living_clamp(
            float(export.get("impulse_intensity", 0.0) or 0.0)
            + drift.get("initiative_drift", 0.0) * 0.018
            + ecology.synergy_map.get("understanding_initiative", 0.0) * 0.020
            - visceral.recoil_reflex * 0.018
        )
        export["mouth_readiness"] = _living_clamp(
            float(export.get("mouth_readiness", 0.0) or 0.0)
            + visceral.soothing_reflex * 0.018
            - visceral.recoil_reflex * 0.025
            - ecology.conflict_map.get("expression_protection", 0.0) * 0.018
        )
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + ecology.temporary_obsession * 0.016 + self.invisible_preinfluence.pre_verbal_tension * 0.015)
        self.micro_temporal_continuity.apply(export)
        self.organic_antipattern_governor.apply(export)
        export.update({
            "v55_long_horizon_drift": dict(self.long_horizon_drift.last_signature),
            "v55_invisible_preinfluence": dict(self.invisible_preinfluence.last_signature),
            "v55_need_ecology": dict(self.need_ecology.last_signature),
            "v55_deep_visceral_conditioning": dict(self.deep_visceral_conditioning.last_signature),
            "v55_micro_temporal_continuity": dict(self.micro_temporal_continuity.last_signature),
            "v55_antipattern": dict(self.organic_antipattern_governor.last_signature),
        })
        export["memory_export"] = dict(export.get("memory_export", {}))
        export["memory_export"].update({
            "visceral_familiarity": visceral.familiarity,
            "implicit_trust": visceral.implicit_trust,
            "implicit_wariness": visceral.implicit_wariness,
            "body_memory_charge": visceral.body_memory_charge,
            "long_term_residue": self.long_horizon_drift.long_residue,
        })
        export["identity_export"] = dict(export.get("identity_export", {}))
        export["identity_export"].update({
            "temperament_drift": dict(drift),
            "irreversible_trace": self.long_horizon_drift.irreversible_trace,
            "need_mutation_pressure": ecology.mutation_pressure,
            "organic_variation_need": self.organic_antipattern_governor.variation_need,
        })

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v55_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))
        expressive_decision = dict(result.get("expressive_decision_v54", result.get("expressive_decision_v53", {})) or {})
        self.long_horizon_drift.tick(self.internal_clock, self.need_hierarchy, self.impulse_metabolism, export)
        self.invisible_preinfluence.tick(export, self.need_hierarchy, self.long_horizon_drift)
        self.need_ecology.tick(self.need_hierarchy, self.long_horizon_drift, self.invisible_preinfluence)
        self.deep_visceral_conditioning.tick(external_signals, export, self.need_ecology, self.long_horizon_drift)
        self.micro_temporal_continuity.tick(self.long_horizon_drift, self.invisible_preinfluence, self.deep_visceral_conditioning)
        self.organic_antipattern_governor.tick(result, export, expressive_decision)
        self._contaminate_clouds_with_v55_refinement()
        self._apply_v55_export_refinement(export)
        expressive_decision_v55 = self.expressive_decision_field.decide(export)
        priority = dict(result.get("priority_arbitration_v53", {}) or getattr(self.priority_arbiter, "last_decision", {}))
        gate = dict(result.get("initiative_gate_v53", {}) or getattr(self.initiative_spam_governor, "last_gate", {}))
        contract = self._build_final_inter_motor_contract(export, expressive_decision_v55, priority, gate)
        contract["long_horizon_drift"] = dict(self.long_horizon_drift.last_signature)
        contract["invisible_preinfluence"] = dict(self.invisible_preinfluence.last_signature)
        contract["need_ecology"] = dict(self.need_ecology.last_signature)
        contract["deep_visceral_conditioning"] = dict(self.deep_visceral_conditioning.last_signature)
        contract["micro_temporal_continuity"] = dict(self.micro_temporal_continuity.last_signature)
        contract["organic_antipattern"] = dict(self.organic_antipattern_governor.last_signature)
        result["natural_initiative_export"] = export
        result["expressive_decision_v55"] = expressive_decision_v55
        result["inter_motor_export_v55"] = contract
        result["long_horizon_drift_v55"] = dict(self.long_horizon_drift.last_signature)
        result["invisible_preinfluence_v55"] = dict(self.invisible_preinfluence.last_signature)
        result["need_ecology_v55"] = dict(self.need_ecology.last_signature)
        result["deep_visceral_conditioning_v55"] = dict(self.deep_visceral_conditioning.last_signature)
        result["micro_temporal_continuity_v55"] = dict(self.micro_temporal_continuity.last_signature)
        result["organic_antipattern_v55"] = dict(self.organic_antipattern_governor.last_signature)
        self.v55_last_signature = {
            "long_residue": self.long_horizon_drift.long_residue,
            "irreversible_trace": self.long_horizon_drift.irreversible_trace,
            "invisible_bias": self.invisible_preinfluence.invisible_bias,
            "dominant_need": self.need_hierarchy.dominant_need,
            "need_mutation": self.need_ecology.mutation_pressure,
            "body_memory_charge": self.deep_visceral_conditioning.body_memory_charge,
            "variation_need": self.organic_antipattern_governor.variation_need,
            "micro_breath": self.micro_temporal_continuity.breath,
        }
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        # Pendant les premiers cycles, ces champs peuvent ne pas encore avoir tické.
        if hasattr(self, "long_horizon_drift"):
            export.update({
                "v55_long_horizon_drift": dict(self.long_horizon_drift.last_signature),
                "v55_invisible_preinfluence": dict(self.invisible_preinfluence.last_signature),
                "v55_need_ecology": dict(self.need_ecology.last_signature),
                "v55_deep_visceral_conditioning": dict(self.deep_visceral_conditioning.last_signature),
                "v55_micro_temporal_continuity": dict(self.micro_temporal_continuity.last_signature),
                "v55_antipattern": dict(self.organic_antipattern_governor.last_signature),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.5_organic_continuity_refinement_stable",
            "v55_cycle_count": self.v55_cycle_count,
            "long_horizon_drift": dict(self.long_horizon_drift.last_signature),
            "invisible_preinfluence": dict(self.invisible_preinfluence.last_signature),
            "need_ecology": dict(self.need_ecology.last_signature),
            "deep_visceral_conditioning": dict(self.deep_visceral_conditioning.last_signature),
            "micro_temporal_continuity": dict(self.micro_temporal_continuity.last_signature),
            "organic_antipattern": dict(self.organic_antipattern_governor.last_signature),
            "v55_last_signature": dict(self.v55_last_signature),
        })
        return base


# Compatibilité finale : tous les imports historiques pointent vers la version active unique V5.5.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngineV54 = SpontaneousImpulseEngineV55
SpontaneousImpulseEngine = SpontaneousImpulseEngineV55


# ============================================================================
# V5.6 — ORGANIC IMPULSE COMPLETION : PHYSIOLOGIE INTERNE, MICRO-ÉMERGENCE,
#        TEMPS SUBJECTIF CAUSAL, FAUX DÉPARTS ET CONTRAT BOUCHE RENFORCÉ
# ============================================================================

@dataclass
class InnerPhysiologyField:
    """
    Physiologie cognitive minimale du moteur impulsionnel.
    Ne remplace pas les émotions, l'attention ou la bouche : elle donne une
    respiration interne, fatigue, récupération, tension et seuil d'élan aux
    impulsions. Objectif : éviter un moteur seulement additionnel/calculé.
    """
    energy: float = 0.62
    fatigue: float = 0.12
    arousal: float = 0.28
    recovery: float = 0.40
    saturation: float = 0.0
    collapse_risk: float = 0.0
    impulse_threshold_shift: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], silence_pressure: float, temporal_drag: float, visceral_charge: float) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        expression_load = max(intensity, mouth)
        self.arousal = _living_clamp(self.arousal * 0.88 + expression_load * 0.085 + visceral_charge * 0.035 + silence_pressure * 0.020)
        self.fatigue = _living_clamp(self.fatigue * 0.965 + expression_load * 0.025 + temporal_drag * 0.018 - self.recovery * 0.010)
        self.recovery = _living_clamp(self.recovery * 0.94 + (1.0 - expression_load) * 0.030 + silence_pressure * 0.012 - self.arousal * 0.010)
        self.energy = _living_clamp(self.energy * 0.94 + self.recovery * 0.045 - self.fatigue * 0.030 + self.arousal * 0.010)
        self.saturation = _living_clamp(self.saturation * 0.92 + max(0.0, expression_load - 0.48) * 0.055 + self.fatigue * 0.010)
        self.collapse_risk = _living_clamp(self.collapse_risk * 0.90 + max(0.0, self.fatigue + self.saturation - self.energy - 0.28) * 0.110)
        self.impulse_threshold_shift = _living_clamp(self.fatigue * 0.16 + self.saturation * 0.12 + self.collapse_risk * 0.18 - self.arousal * 0.06)
        self.last_signature = {
            "energy": self.energy,
            "fatigue": self.fatigue,
            "arousal": self.arousal,
            "recovery": self.recovery,
            "saturation": self.saturation,
            "collapse_risk": self.collapse_risk,
            "impulse_threshold_shift": self.impulse_threshold_shift,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["inner_energy"] = self.energy
        export["inner_fatigue"] = self.fatigue
        export["inner_arousal"] = self.arousal
        export["inner_saturation"] = self.saturation
        export["inner_collapse_risk"] = self.collapse_risk
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.arousal * 0.018 - self.fatigue * 0.026 - self.collapse_risk * 0.040)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.energy * 0.012 - self.saturation * 0.032 - self.collapse_risk * 0.045)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.arousal * 0.018 + self.collapse_risk * 0.020)

    def bias_vector(self) -> Dict[str, float]:
        return {
            "readiness": self.energy * 0.020 + self.arousal * 0.016,
            "hesitation": self.fatigue * 0.022 + self.collapse_risk * 0.030,
            "protection": self.saturation * 0.018 + self.collapse_risk * 0.026,
            "continuity": self.recovery * 0.014,
        }


@dataclass
class PreverbalEmergenceField:
    """
    Micro-réactivité préverbale : faux départs, demi-élans, recul instinctif,
    demi-envies et retours différés. Elle ne produit aucun texte.
    """
    false_start_pressure: float = 0.0
    half_impulse_pressure: float = 0.0
    recoil_pressure: float = 0.0
    delayed_return_pressure: float = 0.0
    unresolved_micro_fragments: deque = field(default_factory=lambda: deque(maxlen=32))
    last_signature: Dict[str, object] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], physiology: InnerPhysiologyField, invisible: InvisiblePreInfluenceField, antipattern: OrganicAntiPatternGovernor) -> None:
        fuzz = float(export.get("impulse_fuzziness", export.get("affective_ambiguity", 0.0)) or 0.0)
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        tension = invisible.pre_verbal_tension
        variation = antipattern.variation_need
        self.false_start_pressure = _living_clamp(self.false_start_pressure * 0.82 + max(0.0, intensity - mouth) * 0.060 + fuzz * 0.030 + tension * 0.025)
        self.half_impulse_pressure = _living_clamp(self.half_impulse_pressure * 0.86 + intensity * 0.035 + fuzz * 0.028 + physiology.arousal * 0.020)
        self.recoil_pressure = _living_clamp(self.recoil_pressure * 0.86 + physiology.collapse_risk * 0.052 + physiology.saturation * 0.030 + max(0.0, fuzz - 0.55) * 0.030)
        self.delayed_return_pressure = _living_clamp(self.delayed_return_pressure * 0.91 + len(self.unresolved_micro_fragments) * 0.004 + variation * 0.018)
        if self.false_start_pressure > 0.18 or self.half_impulse_pressure > 0.20:
            self.unresolved_micro_fragments.append({
                "false_start": self.false_start_pressure,
                "half_impulse": self.half_impulse_pressure,
                "recoil": self.recoil_pressure,
            })
        if self.delayed_return_pressure > 0.34 and self.unresolved_micro_fragments:
            self.unresolved_micro_fragments.popleft()
            self.delayed_return_pressure *= 0.72
        self.last_signature = {
            "false_start_pressure": self.false_start_pressure,
            "half_impulse_pressure": self.half_impulse_pressure,
            "recoil_pressure": self.recoil_pressure,
            "delayed_return_pressure": self.delayed_return_pressure,
            "unresolved_micro_fragments": len(self.unresolved_micro_fragments),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["false_start_pressure"] = self.false_start_pressure
        export["half_impulse_pressure"] = self.half_impulse_pressure
        export["preverbal_recoil_pressure"] = self.recoil_pressure
        export["delayed_micro_return_pressure"] = self.delayed_return_pressure
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.half_impulse_pressure * 0.018 + self.delayed_return_pressure * 0.012 - self.recoil_pressure * 0.020)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.false_start_pressure * 0.010 - self.recoil_pressure * 0.026)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.false_start_pressure * 0.020 + self.delayed_return_pressure * 0.018)

    def contaminate_cloud(self, cloud: FuzzyImpulseCloud) -> None:
        cloud.primary_vector["half_impulse"] = _living_clamp(cloud.primary_vector.get("half_impulse", 0.0) + self.half_impulse_pressure * 0.018)
        cloud.primary_vector["recoil"] = _living_clamp(cloud.primary_vector.get("recoil", 0.0) + self.recoil_pressure * 0.016)
        cloud.primary_vector["returning_fragment"] = _living_clamp(cloud.primary_vector.get("returning_fragment", 0.0) + self.delayed_return_pressure * 0.014)
        cloud.instability_noise = _living_clamp(cloud.instability_noise + self.false_start_pressure * 0.012)


@dataclass
class CausalSubjectiveTimeField:
    """
    Temps subjectif causal : l'attente, la compression, la dilatation et la
    rémanence modifient réellement les seuils impulsionnels et l'export.
    """
    felt_wait: float = 0.0
    acceleration: float = 0.0
    drag: float = 0.0
    remanence: float = 0.0
    urgency_from_time: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], subjective_time: DeepSubjectiveTimeField, silence_duration: int, physiology: InnerPhysiologyField) -> None:
        has_impulse = bool(result.get("has_impulse", False))
        dilation = float(getattr(subjective_time, "dilation", 0.0) or 0.0)
        compression = float(getattr(subjective_time, "compression", 0.0) or 0.0)
        flow = float(getattr(subjective_time, "flow_speed", 1.0) or 1.0)
        self.felt_wait = _living_clamp(self.felt_wait * 0.94 + min(1.0, silence_duration / 12.0) * 0.040 + (0.0 if has_impulse else 0.018))
        self.acceleration = _living_clamp(self.acceleration * 0.88 + compression * 0.060 + max(0.0, flow - 1.0) * 0.035)
        self.drag = _living_clamp(self.drag * 0.90 + dilation * 0.055 + physiology.fatigue * 0.025 + self.felt_wait * 0.015)
        self.remanence = _living_clamp(self.remanence * 0.955 + (0.020 if has_impulse else 0.006) + self.drag * 0.008)
        self.urgency_from_time = _living_clamp(self.felt_wait * 0.26 + self.acceleration * 0.14 + self.remanence * 0.12 - self.drag * 0.09)
        self.last_signature = {
            "felt_wait": self.felt_wait,
            "acceleration": self.acceleration,
            "drag": self.drag,
            "remanence": self.remanence,
            "urgency_from_time": self.urgency_from_time,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["causal_subjective_time"] = dict(self.last_signature)
        export["time_urgency"] = self.urgency_from_time
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.urgency_from_time * 0.024 - self.drag * 0.014)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.acceleration * 0.010 - self.drag * 0.018)


@dataclass
class MouthImpulseFusionContract:
    """
    Contrat bouche renforcé : la bouche reçoit non seulement readiness, mais
    aussi texture physiologique, faux départs, retenue et temporalité.
    """
    last_contract: Dict[str, object] = field(default_factory=dict)

    def build(self, export: Dict[str, object], physiology: InnerPhysiologyField, emergence: PreverbalEmergenceField, causal_time: CausalSubjectiveTimeField) -> Dict[str, object]:
        readiness = float(export.get("mouth_readiness", 0.0) or 0.0)
        speak_hint = bool(export.get("should_speak_hint", False))
        contract = {
            "readiness": readiness,
            "should_speak_hint": speak_hint and physiology.collapse_risk < 0.62 and emergence.recoil_pressure < 0.66,
            "living_mouth_pressure": _living_clamp(readiness * 0.50 + physiology.arousal * 0.16 + emergence.half_impulse_pressure * 0.12 + causal_time.urgency_from_time * 0.10 - physiology.saturation * 0.12),
            "preverbal_texture": {
                "false_start": emergence.false_start_pressure,
                "half_impulse": emergence.half_impulse_pressure,
                "recoil": emergence.recoil_pressure,
                "delayed_return": emergence.delayed_return_pressure,
            },
            "physiology_texture": {
                "energy": physiology.energy,
                "fatigue": physiology.fatigue,
                "arousal": physiology.arousal,
                "saturation": physiology.saturation,
                "collapse_risk": physiology.collapse_risk,
            },
            "temporal_texture": dict(causal_time.last_signature),
        }
        self.last_contract = contract
        return contract


class SpontaneousImpulseEngineV56(SpontaneousImpulseEngineV55):
    """
    V5.6 Organic Impulse Completion.

    Corrige les derniers manques du V5.5 sans repartir de zéro :
    - physiologie interne causale ;
    - faux départs et micro-émergences préverbales ;
    - temps subjectif qui influence réellement l'impulsion ;
    - contamination douce des nuages ;
    - contrat bouche plus exploitable par living_expression_engine.
    """

    def __init__(self):
        super().__init__()
        self.inner_physiology = InnerPhysiologyField()
        self.preverbal_emergence = PreverbalEmergenceField()
        self.causal_subjective_time = CausalSubjectiveTimeField()
        self.mouth_impulse_fusion = MouthImpulseFusionContract()
        self.v56_cycle_count: int = 0
        self.v56_last_signature: Dict[str, object] = {}

    def _contaminate_clouds_with_v56_completion(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        physiology_bias = self.inner_physiology.bias_vector()
        for cloud in self.fuzzy_impulse_clouds:
            for key, value in physiology_bias.items():
                cloud.primary_vector[key] = _living_clamp(cloud.primary_vector.get(key, 0.0) + float(value or 0.0))
            self.preverbal_emergence.contaminate_cloud(cloud)
            cloud.primary_vector["time_urgency"] = _living_clamp(cloud.primary_vector.get("time_urgency", 0.0) + self.causal_subjective_time.urgency_from_time * 0.018)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.preverbal_emergence.false_start_pressure * 0.004 + self.causal_subjective_time.drag * 0.004 - self.inner_physiology.energy * 0.002)

    def _apply_v56_export_completion(self, export: Dict[str, object]) -> None:
        self.inner_physiology.apply_to_export(export)
        self.preverbal_emergence.apply_to_export(export)
        self.causal_subjective_time.apply_to_export(export)
        mouth_contract = self.mouth_impulse_fusion.build(export, self.inner_physiology, self.preverbal_emergence, self.causal_subjective_time)
        export["v56_inner_physiology"] = dict(self.inner_physiology.last_signature)
        export["v56_preverbal_emergence"] = dict(self.preverbal_emergence.last_signature)
        export["v56_causal_subjective_time"] = dict(self.causal_subjective_time.last_signature)
        export["v56_mouth_impulse_fusion"] = dict(mouth_contract)
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "physiology": dict(mouth_contract["physiology_texture"]),
            "preverbal": dict(mouth_contract["preverbal_texture"]),
            "temporal": dict(mouth_contract["temporal_texture"]),
            "living_mouth_pressure": mouth_contract["living_mouth_pressure"],
        })
        export["should_speak_hint"] = bool(mouth_contract["should_speak_hint"])

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v56_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))
        silence_pressure = _living_clamp(float(result.get("silence_duration", self.silence_duration) or 0.0) / 10.0)
        visceral_charge = float(getattr(self.deep_visceral_conditioning, "body_memory_charge", 0.0) or 0.0)
        temporal_drag_seed = float(getattr(self.subjective_time, "dilation", 0.0) or 0.0) if hasattr(self, "subjective_time") else 0.0
        self.inner_physiology.tick(export, silence_pressure, temporal_drag_seed, visceral_charge)
        self.preverbal_emergence.tick(export, self.inner_physiology, self.invisible_preinfluence, self.organic_antipattern_governor)
        if hasattr(self, "subjective_time"):
            self.causal_subjective_time.tick(result, self.subjective_time, self.silence_duration, self.inner_physiology)
        self._contaminate_clouds_with_v56_completion()
        self._apply_v56_export_completion(export)
        expressive_decision_v56 = self.expressive_decision_field.decide(export)
        priority = dict(result.get("priority_arbitration_v53", {}) or getattr(self.priority_arbiter, "last_decision", {}))
        gate = dict(result.get("initiative_gate_v53", {}) or getattr(self.initiative_spam_governor, "last_gate", {}))
        contract = self._build_final_inter_motor_contract(export, expressive_decision_v56, priority, gate)
        contract["inner_physiology"] = dict(self.inner_physiology.last_signature)
        contract["preverbal_emergence"] = dict(self.preverbal_emergence.last_signature)
        contract["causal_subjective_time"] = dict(self.causal_subjective_time.last_signature)
        contract["mouth_impulse_fusion"] = dict(self.mouth_impulse_fusion.last_contract)
        result["natural_initiative_export"] = export
        result["expressive_decision_v56"] = expressive_decision_v56
        result["inter_motor_export_v56"] = contract
        result["inner_physiology_v56"] = dict(self.inner_physiology.last_signature)
        result["preverbal_emergence_v56"] = dict(self.preverbal_emergence.last_signature)
        result["causal_subjective_time_v56"] = dict(self.causal_subjective_time.last_signature)
        result["mouth_impulse_fusion_v56"] = dict(self.mouth_impulse_fusion.last_contract)
        self.v56_last_signature = {
            "energy": self.inner_physiology.energy,
            "fatigue": self.inner_physiology.fatigue,
            "arousal": self.inner_physiology.arousal,
            "false_start": self.preverbal_emergence.false_start_pressure,
            "half_impulse": self.preverbal_emergence.half_impulse_pressure,
            "recoil": self.preverbal_emergence.recoil_pressure,
            "time_urgency": self.causal_subjective_time.urgency_from_time,
            "living_mouth_pressure": self.mouth_impulse_fusion.last_contract.get("living_mouth_pressure", 0.0),
        }
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        if hasattr(self, "inner_physiology"):
            export.update({
                "v56_inner_physiology": dict(self.inner_physiology.last_signature),
                "v56_preverbal_emergence": dict(self.preverbal_emergence.last_signature),
                "v56_causal_subjective_time": dict(self.causal_subjective_time.last_signature),
                "v56_mouth_impulse_fusion": dict(self.mouth_impulse_fusion.last_contract),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.6_organic_impulse_completion_stable",
            "v56_cycle_count": self.v56_cycle_count,
            "inner_physiology": dict(self.inner_physiology.last_signature),
            "preverbal_emergence": dict(self.preverbal_emergence.last_signature),
            "causal_subjective_time": dict(self.causal_subjective_time.last_signature),
            "mouth_impulse_fusion": dict(self.mouth_impulse_fusion.last_contract),
            "v56_last_signature": dict(self.v56_last_signature),
        })
        return base


# Compatibilité finale : version active unique V5.6.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV54 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngineV55 = SpontaneousImpulseEngineV56
SpontaneousImpulseEngine = SpontaneousImpulseEngineV56


# ============================================================================
# V5.7 — CONTINUOUS LIVING FLOW : FLUX NON-DISCRET, TRACES DURABLES,
#        CONTRADICTIONS SIMULTANÉES ET TRANSITIONS ORGANIQUES
# ============================================================================

@dataclass
class ContinuousImpulseFlowField:
    """
    Champ de flux continu.

    Le moteur V5.6 était déjà stable, mais il restait encore trop orienté
    "cycle qui calcule un résultat". Cette couche maintient une inertie entre
    les cycles : élan, contre-élan, viscosité, rémanence et seuil vivant.
    Aucun texte n'est généré ici ; seulement des pressions exploitables.
    """
    momentum: float = 0.0
    counter_momentum: float = 0.0
    viscosity: float = 0.18
    living_current: float = 0.0
    continuity_inertia: float = 0.0
    threshold_memory: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], physiology: InnerPhysiologyField, time_field: CausalSubjectiveTimeField, silence_duration: int) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        silence_pressure = _living_clamp(silence_duration / 12.0)
        drive = _living_clamp(intensity * 0.42 + mouth * 0.16 + physiology.arousal * 0.18 + time_field.urgency_from_time * 0.14 + silence_pressure * 0.10)
        inhibition = _living_clamp(physiology.fatigue * 0.22 + physiology.saturation * 0.20 + physiology.collapse_risk * 0.18 + time_field.drag * 0.10)
        self.counter_momentum = _living_clamp(self.counter_momentum * 0.90 + inhibition * 0.10)
        self.momentum = _living_clamp(self.momentum * (0.84 + self.viscosity * 0.08) + drive * 0.13 - self.counter_momentum * 0.045)
        self.living_current = _living_clamp(self.living_current * 0.88 + (self.momentum - self.counter_momentum * 0.45 + 0.5) * 0.08)
        self.continuity_inertia = _living_clamp(self.continuity_inertia * 0.94 + abs(self.momentum - self.threshold_memory) * 0.035 + silence_pressure * 0.018)
        self.threshold_memory = _living_clamp(self.threshold_memory * 0.93 + drive * 0.07)
        self.viscosity = _living_clamp(self.viscosity * 0.96 + physiology.fatigue * 0.030 + time_field.drag * 0.025 + self.continuity_inertia * 0.015)
        self.last_signature = {
            "momentum": self.momentum,
            "counter_momentum": self.counter_momentum,
            "viscosity": self.viscosity,
            "living_current": self.living_current,
            "continuity_inertia": self.continuity_inertia,
            "threshold_memory": self.threshold_memory,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["continuous_impulse_momentum"] = self.momentum
        export["continuous_counter_momentum"] = self.counter_momentum
        export["living_current"] = self.living_current
        export["continuity_inertia"] = self.continuity_inertia
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.momentum * 0.026 + self.living_current * 0.018 - self.counter_momentum * 0.018)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.living_current * 0.018 - self.viscosity * 0.012)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.continuity_inertia * 0.020)


@dataclass
class DurableImpulseTraceField:
    """
    Traces physiologiques et affectives laissées par les impulsions.

    Une impulsion exprimée, retenue ou avortée doit continuer à colorer les
    cycles suivants. Cette classe ajoute une mémoire diffuse non textuelle.
    """
    residue: float = 0.0
    aftertaste: float = 0.0
    unexpressed_pressure: float = 0.0
    scar_tenderness: float = 0.0
    recovery_need: float = 0.0
    trace_history: deque = field(default_factory=lambda: deque(maxlen=80))
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], export: Dict[str, object], physiology: InnerPhysiologyField, emergence: PreverbalEmergenceField) -> None:
        has_impulse = bool(result.get("has_impulse", False))
        pressure = float(result.get("pressure", export.get("initiative_pressure", 0.0)) or 0.0)
        clarity = float(result.get("clarity", export.get("impulse_clarity", 0.0)) or 0.0)
        fuzziness = float(result.get("fuzziness", export.get("impulse_fuzziness", 0.0)) or 0.0)
        expressed_charge = pressure if has_impulse else 0.0
        retained_charge = pressure * (0.65 + fuzziness * 0.25) if not has_impulse else fuzziness * 0.08
        self.residue = _living_clamp(self.residue * 0.955 + expressed_charge * 0.035 + retained_charge * 0.026)
        self.aftertaste = _living_clamp(self.aftertaste * 0.935 + expressed_charge * 0.024 + emergence.delayed_return_pressure * 0.030)
        self.unexpressed_pressure = _living_clamp(self.unexpressed_pressure * 0.92 + retained_charge * 0.055 + emergence.recoil_pressure * 0.025 - clarity * 0.010)
        self.scar_tenderness = _living_clamp(self.scar_tenderness * 0.985 + self.unexpressed_pressure * 0.012 + physiology.collapse_risk * 0.018)
        self.recovery_need = _living_clamp(self.recovery_need * 0.94 + physiology.fatigue * 0.030 + self.residue * 0.018 + self.scar_tenderness * 0.012)
        self.trace_history.append({"impulse": float(has_impulse), "pressure": pressure, "clarity": clarity, "fuzziness": fuzziness})
        self.last_signature = {
            "residue": self.residue,
            "aftertaste": self.aftertaste,
            "unexpressed_pressure": self.unexpressed_pressure,
            "scar_tenderness": self.scar_tenderness,
            "recovery_need": self.recovery_need,
            "trace_count": float(len(self.trace_history)),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["durable_impulse_residue"] = self.residue
        export["durable_impulse_aftertaste"] = self.aftertaste
        export["unexpressed_impulse_pressure"] = self.unexpressed_pressure
        export["trace_recovery_need"] = self.recovery_need
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.residue * 0.018 + self.unexpressed_pressure * 0.014 - self.recovery_need * 0.010)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.aftertaste * 0.014 - self.scar_tenderness * 0.018)


@dataclass
class SimultaneousContradictionField:
    """
    Contradictions simultanées : parler / retenir, continuer / se protéger,
    curiosité / fatigue. Elles ne choisissent pas brutalement un camp ; elles
    laissent une pression bifurquée dans l'export.
    """
    approach_pull: float = 0.0
    withdrawal_pull: float = 0.0
    dual_pressure: float = 0.0
    oscillatory_instability: float = 0.0
    unresolved_duality: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], flow: ContinuousImpulseFlowField, traces: DurableImpulseTraceField, physiology: InnerPhysiologyField) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        recoil = float(export.get("preverbal_recoil_pressure", 0.0) or 0.0)
        presence_need = float(export.get("presence_need", 0.0) or 0.0)
        approach_seed = _living_clamp(intensity * 0.34 + mouth * 0.20 + presence_need * 0.16 + flow.momentum * 0.18 + traces.aftertaste * 0.12)
        withdrawal_seed = _living_clamp(recoil * 0.24 + physiology.fatigue * 0.20 + physiology.collapse_risk * 0.20 + traces.recovery_need * 0.15 + flow.counter_momentum * 0.21)
        self.approach_pull = _living_clamp(self.approach_pull * 0.88 + approach_seed * 0.12)
        self.withdrawal_pull = _living_clamp(self.withdrawal_pull * 0.88 + withdrawal_seed * 0.12)
        self.dual_pressure = _living_clamp(min(self.approach_pull, self.withdrawal_pull) * 1.35)
        self.oscillatory_instability = _living_clamp(self.oscillatory_instability * 0.90 + abs(self.approach_pull - self.withdrawal_pull) * 0.030 + self.dual_pressure * 0.060)
        self.unresolved_duality = _living_clamp(self.unresolved_duality * 0.95 + self.dual_pressure * 0.032 + traces.unexpressed_pressure * 0.012)
        self.last_signature = {
            "approach_pull": self.approach_pull,
            "withdrawal_pull": self.withdrawal_pull,
            "dual_pressure": self.dual_pressure,
            "oscillatory_instability": self.oscillatory_instability,
            "unresolved_duality": self.unresolved_duality,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["simultaneous_approach_pull"] = self.approach_pull
        export["simultaneous_withdrawal_pull"] = self.withdrawal_pull
        export["simultaneous_dual_pressure"] = self.dual_pressure
        export["unresolved_duality_v57"] = self.unresolved_duality
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.approach_pull * 0.014 - self.withdrawal_pull * 0.010)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.approach_pull * 0.012 - self.dual_pressure * 0.018)
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and self.withdrawal_pull < 0.74 and self.dual_pressure < 0.78


@dataclass
class OrganicTransitionField:
    """
    Transitions organiques : au lieu de passer brutalement de silence à parole,
    de retenue à expression, ou d'une impulsion à une autre, le moteur garde un
    état de passage progressif.
    """
    transition_pressure: float = 0.0
    silence_to_motion: float = 0.0
    motion_to_rest: float = 0.0
    phase_blend: float = 0.0
    last_mode: str = "rest"
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], export: Dict[str, object], flow: ContinuousImpulseFlowField, contradictions: SimultaneousContradictionField, traces: DurableImpulseTraceField) -> None:
        has_impulse = bool(result.get("has_impulse", False))
        silence_active = bool(result.get("silence_active", False))
        current_mode = "impulse" if has_impulse else ("silence" if silence_active else "rest")
        changed = current_mode != self.last_mode
        change_seed = 0.18 if changed else 0.0
        self.transition_pressure = _living_clamp(self.transition_pressure * 0.90 + change_seed + contradictions.dual_pressure * 0.035 + flow.continuity_inertia * 0.020)
        self.silence_to_motion = _living_clamp(self.silence_to_motion * 0.88 + (0.08 if self.last_mode == "silence" and current_mode == "impulse" else 0.0) + flow.momentum * 0.020)
        self.motion_to_rest = _living_clamp(self.motion_to_rest * 0.90 + (0.06 if self.last_mode == "impulse" and current_mode != "impulse" else 0.0) + traces.recovery_need * 0.018)
        self.phase_blend = _living_clamp(self.phase_blend * 0.92 + self.transition_pressure * 0.05 + self.silence_to_motion * 0.03 - self.motion_to_rest * 0.015)
        self.last_mode = current_mode
        self.last_signature = {
            "transition_pressure": self.transition_pressure,
            "silence_to_motion": self.silence_to_motion,
            "motion_to_rest": self.motion_to_rest,
            "phase_blend": self.phase_blend,
            "mode_impulse": 1.0 if current_mode == "impulse" else 0.0,
            "mode_silence": 1.0 if current_mode == "silence" else 0.0,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["organic_transition_pressure"] = self.transition_pressure
        export["silence_to_motion_blend"] = self.silence_to_motion
        export["motion_to_rest_blend"] = self.motion_to_rest
        export["phase_blend"] = self.phase_blend
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.silence_to_motion * 0.018 - self.motion_to_rest * 0.014)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.transition_pressure * 0.012)


class SpontaneousImpulseEngineV57(SpontaneousImpulseEngineV56):
    """
    V5.7 Continuous Living Flow.

    Correction concrète au-dessus de V5.6 :
    - flux impulsionnel continu entre cycles ;
    - traces durables des impulsions exprimées / retenues / avortées ;
    - contradictions simultanées non résolues brutalement ;
    - transitions organiques au lieu de bascules sèches ;
    - export bouche/initiative enrichi sans générer de texte ni dupliquer les
      responsabilités de la bouche, attention, mémoire ou présence.
    """

    def __init__(self):
        super().__init__()
        self.continuous_impulse_flow = ContinuousImpulseFlowField()
        self.durable_impulse_traces = DurableImpulseTraceField()
        self.simultaneous_contradictions = SimultaneousContradictionField()
        self.organic_transitions = OrganicTransitionField()
        self.v57_cycle_count: int = 0
        self.v57_last_signature: Dict[str, object] = {}

    def _contaminate_clouds_with_v57_flow(self) -> None:
        if not self.fuzzy_impulse_clouds:
            return
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["continuous_momentum"] = _living_clamp(cloud.primary_vector.get("continuous_momentum", 0.0) + self.continuous_impulse_flow.momentum * 0.018)
            cloud.primary_vector["unexpressed_trace"] = _living_clamp(cloud.primary_vector.get("unexpressed_trace", 0.0) + self.durable_impulse_traces.unexpressed_pressure * 0.020)
            cloud.primary_vector["dual_pressure"] = _living_clamp(cloud.primary_vector.get("dual_pressure", 0.0) + self.simultaneous_contradictions.dual_pressure * 0.018)
            cloud.primary_vector["transition_blend"] = _living_clamp(cloud.primary_vector.get("transition_blend", 0.0) + self.organic_transitions.phase_blend * 0.014)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.simultaneous_contradictions.oscillatory_instability * 0.010)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.durable_impulse_traces.aftertaste * 0.004 + self.simultaneous_contradictions.dual_pressure * 0.004 - self.continuous_impulse_flow.living_current * 0.003)

    def _apply_v57_export_flow(self, export: Dict[str, object]) -> None:
        self.continuous_impulse_flow.apply_to_export(export)
        self.durable_impulse_traces.apply_to_export(export)
        self.simultaneous_contradictions.apply_to_export(export)
        self.organic_transitions.apply_to_export(export)
        export["v57_continuous_impulse_flow"] = dict(self.continuous_impulse_flow.last_signature)
        export["v57_durable_impulse_traces"] = dict(self.durable_impulse_traces.last_signature)
        export["v57_simultaneous_contradictions"] = dict(self.simultaneous_contradictions.last_signature)
        export["v57_organic_transitions"] = dict(self.organic_transitions.last_signature)
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "continuous_flow": dict(self.continuous_impulse_flow.last_signature),
            "durable_traces": dict(self.durable_impulse_traces.last_signature),
            "contradictions": dict(self.simultaneous_contradictions.last_signature),
            "organic_transitions": dict(self.organic_transitions.last_signature),
        })

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v57_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))

        self.continuous_impulse_flow.tick(export, self.inner_physiology, self.causal_subjective_time, self.silence_duration)
        self.durable_impulse_traces.tick(result, export, self.inner_physiology, self.preverbal_emergence)
        self.simultaneous_contradictions.tick(export, self.continuous_impulse_flow, self.durable_impulse_traces, self.inner_physiology)
        self.organic_transitions.tick(result, export, self.continuous_impulse_flow, self.simultaneous_contradictions, self.durable_impulse_traces)
        self._contaminate_clouds_with_v57_flow()
        self._apply_v57_export_flow(export)

        expressive_decision_v57 = self.expressive_decision_field.decide(export)
        priority = dict(result.get("priority_arbitration_v53", {}) or getattr(self.priority_arbiter, "last_decision", {}))
        gate = dict(result.get("initiative_gate_v53", {}) or getattr(self.initiative_spam_governor, "last_gate", {}))
        contract = self._build_final_inter_motor_contract(export, expressive_decision_v57, priority, gate)
        contract["continuous_impulse_flow"] = dict(self.continuous_impulse_flow.last_signature)
        contract["durable_impulse_traces"] = dict(self.durable_impulse_traces.last_signature)
        contract["simultaneous_contradictions"] = dict(self.simultaneous_contradictions.last_signature)
        contract["organic_transitions"] = dict(self.organic_transitions.last_signature)

        result["natural_initiative_export"] = export
        result["expressive_decision_v57"] = expressive_decision_v57
        result["inter_motor_export_v57"] = contract
        result["continuous_impulse_flow_v57"] = dict(self.continuous_impulse_flow.last_signature)
        result["durable_impulse_traces_v57"] = dict(self.durable_impulse_traces.last_signature)
        result["simultaneous_contradictions_v57"] = dict(self.simultaneous_contradictions.last_signature)
        result["organic_transitions_v57"] = dict(self.organic_transitions.last_signature)
        self.v57_last_signature = {
            "momentum": self.continuous_impulse_flow.momentum,
            "living_current": self.continuous_impulse_flow.living_current,
            "residue": self.durable_impulse_traces.residue,
            "unexpressed_pressure": self.durable_impulse_traces.unexpressed_pressure,
            "dual_pressure": self.simultaneous_contradictions.dual_pressure,
            "transition_pressure": self.organic_transitions.transition_pressure,
            "mouth_readiness": float(export.get("mouth_readiness", 0.0) or 0.0),
            "should_speak_hint": bool(export.get("should_speak_hint", False)),
        }
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        if hasattr(self, "continuous_impulse_flow"):
            export.update({
                "v57_continuous_impulse_flow": dict(self.continuous_impulse_flow.last_signature),
                "v57_durable_impulse_traces": dict(self.durable_impulse_traces.last_signature),
                "v57_simultaneous_contradictions": dict(self.simultaneous_contradictions.last_signature),
                "v57_organic_transitions": dict(self.organic_transitions.last_signature),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.7_continuous_living_flow_stable",
            "v57_cycle_count": self.v57_cycle_count,
            "continuous_impulse_flow": dict(self.continuous_impulse_flow.last_signature),
            "durable_impulse_traces": dict(self.durable_impulse_traces.last_signature),
            "simultaneous_contradictions": dict(self.simultaneous_contradictions.last_signature),
            "organic_transitions": dict(self.organic_transitions.last_signature),
            "v57_last_signature": dict(self.v57_last_signature),
        })
        return base


# Compatibilité finale : version active unique V5.7.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV54 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV55 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngineV56 = SpontaneousImpulseEngineV57
SpontaneousImpulseEngine = SpontaneousImpulseEngineV57


# ============================================================================
# V5.8 — AUTONOMOUS ORGANIC IMPULSE LIFE : DÉRIVE SUBCONSCIENTE,
#        SILENCE HABITÉ, GRAVITÉ NON RÉSOLUE, RÉACTIVATION AUTOBIOGRAPHIQUE
#        ET ACTIVITÉ AUTONOME SANS INPUT UTILISATEUR
# ============================================================================

@dataclass
class SubconsciousDriftFieldV58:
    """
    Dérive subconsciente continue.

    Cette couche ne remplace pas l'attention ni la mémoire : elle produit un
    bruit organique structuré, des associations latentes, des retours faibles et
    des micro-déplacements d'élan même quand aucun stimulus externe n'arrive.
    """
    drift_phase: float = 0.0
    wandering_pressure: float = 0.0
    associative_noise: float = 0.0
    latent_return: float = 0.0
    parasite_impulse_pressure: float = 0.0
    last_birth_cycle: int = 0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, export: Dict[str, object], silence_duration: int, continuity_bias: float, duality: float, physiology: InnerPhysiologyField) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        clarity = float(export.get("impulse_clarity", 0.0) or 0.0)
        fuzziness = float(export.get("impulse_fuzziness", 0.0) or 0.0)
        silence_pressure = _living_clamp(silence_duration / 18.0)
        self.drift_phase = (self.drift_phase + 0.037 + physiology.arousal * 0.010 + duality * 0.006) % 1.0
        wave = 0.5 + 0.5 * math.sin(self.drift_phase * 2.0 * math.pi)
        unclear_space = _living_clamp(fuzziness * 0.32 + max(0.0, 0.55 - clarity) * 0.24)
        self.associative_noise = _living_clamp(self.associative_noise * 0.91 + (wave * 0.08 + unclear_space * 0.10 + random.random() * 0.018))
        self.wandering_pressure = _living_clamp(self.wandering_pressure * 0.93 + silence_pressure * 0.045 + continuity_bias * 0.030 + self.associative_noise * 0.040 - intensity * 0.012)
        self.latent_return = _living_clamp(self.latent_return * 0.90 + continuity_bias * 0.045 + duality * 0.026 + silence_pressure * 0.020)
        self.parasite_impulse_pressure = _living_clamp(self.parasite_impulse_pressure * 0.88 + self.associative_noise * 0.040 + self.wandering_pressure * 0.034 + random.random() * 0.010)
        self.last_signature = {
            "wandering_pressure": self.wandering_pressure,
            "associative_noise": self.associative_noise,
            "latent_return": self.latent_return,
            "parasite_impulse_pressure": self.parasite_impulse_pressure,
            "drift_phase": self.drift_phase,
        }

    def should_birth_drift_cloud(self, cycle: int) -> bool:
        return self.parasite_impulse_pressure > 0.34 and (cycle - self.last_birth_cycle) > 8

    def make_drift_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "subconscious_drift": _living_clamp(0.18 + self.wandering_pressure * 0.52),
            "association": _living_clamp(0.14 + self.associative_noise * 0.48),
            "continuity": _living_clamp(0.10 + self.latent_return * 0.42),
            "hesitation": _living_clamp(0.12 + self.parasite_impulse_pressure * 0.34),
            "openness": _living_clamp(0.08 + self.wandering_pressure * 0.22),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["subconscious_drift_v58"] = dict(self.last_signature)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.latent_return * 0.014 + self.parasite_impulse_pressure * 0.010)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.wandering_pressure * 0.008 - self.associative_noise * 0.006)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.latent_return * 0.010)


@dataclass
class UnresolvedGravityFieldV58:
    """
    Gravité cognitive des choses inachevées.
    Une tension non résolue ne disparaît pas : elle tire doucement les cycles
    suivants, peut créer une fixation, ou réapparaître sous forme d'impulsion.
    """
    unresolved_mass: float = 0.0
    fixation_pull: float = 0.0
    incompletion_hunger: float = 0.0
    obsession_risk: float = 0.0
    last_birth_cycle: int = 0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, result: Dict[str, object], export: Dict[str, object], traces: DurableImpulseTraceField, contradictions: SimultaneousContradictionField, narrative_bias: float) -> None:
        expressed = bool(result.get("has_impulse", False))
        clarity = float(result.get("clarity", export.get("impulse_clarity", 0.0)) or 0.0)
        pressure = float(result.get("pressure", export.get("impulse_intensity", 0.0)) or 0.0)
        not_resolved = (not expressed) or clarity < 0.35 or contradictions.dual_pressure > 0.42
        add_mass = (0.050 if not_resolved else -0.028) + traces.unexpressed_pressure * 0.030 + contradictions.unresolved_duality * 0.022 + narrative_bias * 0.018
        self.unresolved_mass = _living_clamp(self.unresolved_mass * 0.975 + add_mass)
        self.incompletion_hunger = _living_clamp(self.incompletion_hunger * 0.94 + self.unresolved_mass * 0.040 + max(0.0, pressure - clarity) * 0.020)
        self.fixation_pull = _living_clamp(self.fixation_pull * 0.91 + self.incompletion_hunger * 0.040 + narrative_bias * 0.020)
        self.obsession_risk = _living_clamp(self.obsession_risk * 0.96 + max(0.0, self.fixation_pull - 0.50) * 0.030 + contradictions.dual_pressure * 0.012)
        self.last_signature = {
            "unresolved_mass": self.unresolved_mass,
            "fixation_pull": self.fixation_pull,
            "incompletion_hunger": self.incompletion_hunger,
            "obsession_risk": self.obsession_risk,
        }

    def should_birth_resolution_cloud(self, cycle: int) -> bool:
        return self.incompletion_hunger > 0.36 and (cycle - self.last_birth_cycle) > 10

    def make_resolution_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "clarity": _living_clamp(0.20 + self.incompletion_hunger * 0.50),
            "continuity": _living_clamp(0.18 + self.fixation_pull * 0.42),
            "tension": _living_clamp(0.14 + self.unresolved_mass * 0.44),
            "curiosity": _living_clamp(0.12 + self.incompletion_hunger * 0.30),
            "hesitation": _living_clamp(0.10 + self.obsession_risk * 0.26),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["unresolved_gravity_v58"] = dict(self.last_signature)
        export["unresolved_gravity_pressure"] = self.incompletion_hunger
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.fixation_pull * 0.018)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.incompletion_hunger * 0.010 - self.obsession_risk * 0.012)


@dataclass
class SilentInnerActivityFieldV58:
    """
    Rend le silence habité : activité interne, maturation muette, impulsions
    suspendues et pression de transformation au lieu d'un état passif.
    """
    silent_activity: float = 0.0
    suspended_impulse: float = 0.0
    mute_maturation: float = 0.0
    inner_movement: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, silence_active: bool, silence_duration: int, drift: SubconsciousDriftFieldV58, gravity: UnresolvedGravityFieldV58, physiology: InnerPhysiologyField) -> None:
        silence_pressure = _living_clamp(silence_duration / 12.0)
        if silence_active or silence_duration > 0:
            self.silent_activity = _living_clamp(self.silent_activity * 0.92 + silence_pressure * 0.040 + drift.wandering_pressure * 0.035 + gravity.unresolved_mass * 0.026)
            self.suspended_impulse = _living_clamp(self.suspended_impulse * 0.90 + gravity.incompletion_hunger * 0.034 + drift.latent_return * 0.026 + physiology.arousal * 0.014)
            self.mute_maturation = _living_clamp(self.mute_maturation * 0.94 + self.silent_activity * 0.035 + self.suspended_impulse * 0.020)
            self.inner_movement = _living_clamp(self.inner_movement * 0.88 + self.silent_activity * 0.040 + random.random() * 0.012)
        else:
            self.silent_activity = _living_clamp(self.silent_activity * 0.86)
            self.suspended_impulse = _living_clamp(self.suspended_impulse * 0.88)
            self.mute_maturation = _living_clamp(self.mute_maturation * 0.96)
            self.inner_movement = _living_clamp(self.inner_movement * 0.84)
        self.last_signature = {
            "silent_activity": self.silent_activity,
            "suspended_impulse": self.suspended_impulse,
            "mute_maturation": self.mute_maturation,
            "inner_movement": self.inner_movement,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["silent_inner_activity_v58"] = dict(self.last_signature)
        export["silence_is_inhabited"] = self.silent_activity > 0.12 or self.suspended_impulse > 0.16
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.suspended_impulse * 0.010 - self.silent_activity * 0.004)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.mute_maturation * 0.010)


@dataclass
class AutobiographicalResonanceFieldV58:
    """
    Réactivation autobiographique non textuelle : anciennes traces, blessures,
    continuités et réussites reviennent comme climat, pas comme phrases.
    """
    lived_identity_charge: float = 0.0
    autobiographical_pull: float = 0.0
    old_state_reactivation: float = 0.0
    identity_period_pressure: float = 0.0
    last_birth_cycle: int = 0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, identity_pressure: float, existential_pressure: float, relational_wound: float, traces: DurableImpulseTraceField, gravity: UnresolvedGravityFieldV58) -> None:
        self.lived_identity_charge = _living_clamp(self.lived_identity_charge * 0.94 + identity_pressure * 0.040 + traces.residue * 0.026 + existential_pressure * 0.018)
        self.autobiographical_pull = _living_clamp(self.autobiographical_pull * 0.93 + self.lived_identity_charge * 0.035 + relational_wound * 0.030 + gravity.fixation_pull * 0.020)
        self.old_state_reactivation = _living_clamp(self.old_state_reactivation * 0.90 + self.autobiographical_pull * 0.034 + gravity.unresolved_mass * 0.018)
        self.identity_period_pressure = _living_clamp(self.identity_period_pressure * 0.97 + self.lived_identity_charge * 0.018 + self.old_state_reactivation * 0.014)
        self.last_signature = {
            "lived_identity_charge": self.lived_identity_charge,
            "autobiographical_pull": self.autobiographical_pull,
            "old_state_reactivation": self.old_state_reactivation,
            "identity_period_pressure": self.identity_period_pressure,
        }

    def should_birth_autobiographical_cloud(self, cycle: int) -> bool:
        return self.old_state_reactivation > 0.31 and (cycle - self.last_birth_cycle) > 12

    def make_autobiographical_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "identity": _living_clamp(0.20 + self.lived_identity_charge * 0.52),
            "continuity": _living_clamp(0.18 + self.autobiographical_pull * 0.46),
            "memory": _living_clamp(0.16 + self.old_state_reactivation * 0.48),
            "presence": _living_clamp(0.10 + self.identity_period_pressure * 0.34),
            "openness": _living_clamp(0.08 + self.lived_identity_charge * 0.24),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["autobiographical_resonance_v58"] = dict(self.last_signature)
        export["identity_period_pressure"] = self.identity_period_pressure
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.autobiographical_pull * 0.012)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.old_state_reactivation * 0.010)


@dataclass
class AutonomousInnerLifeFieldV58:
    """
    Activité autonome hors utilisateur : quand l'entrée externe est faible, le
    moteur ne devient pas vide. Il continue d'avoir exploration interne,
    initiative faible, besoin d'expérience et déplacement de curiosité.
    """
    autonomous_pulse: float = 0.0
    self_generated_need: float = 0.0
    inner_exploration_drive: float = 0.0
    experience_hunger: float = 0.0
    last_birth_cycle: int = 0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, external_signals: Dict[str, float], drift: SubconsciousDriftFieldV58, gravity: UnresolvedGravityFieldV58, autobiographical: AutobiographicalResonanceFieldV58, physiology: InnerPhysiologyField) -> None:
        attention = float(external_signals.get("attention_presence", 0.5) or 0.5)
        external_low = _living_clamp(1.0 - attention)
        available_energy = _living_clamp(physiology.energy * (1.0 - physiology.collapse_risk))
        self.self_generated_need = _living_clamp(self.self_generated_need * 0.94 + external_low * 0.034 + drift.wandering_pressure * 0.026 + autobiographical.lived_identity_charge * 0.014)
        self.inner_exploration_drive = _living_clamp(self.inner_exploration_drive * 0.93 + available_energy * 0.020 + drift.associative_noise * 0.030 + gravity.incompletion_hunger * 0.018)
        self.experience_hunger = _living_clamp(self.experience_hunger * 0.96 + external_low * 0.020 + autobiographical.identity_period_pressure * 0.020 + gravity.fixation_pull * 0.016)
        self.autonomous_pulse = _living_clamp(self.autonomous_pulse * 0.91 + self.self_generated_need * 0.034 + self.inner_exploration_drive * 0.028 + self.experience_hunger * 0.022 - physiology.fatigue * 0.012)
        self.last_signature = {
            "autonomous_pulse": self.autonomous_pulse,
            "self_generated_need": self.self_generated_need,
            "inner_exploration_drive": self.inner_exploration_drive,
            "experience_hunger": self.experience_hunger,
        }

    def should_birth_autonomous_cloud(self, cycle: int) -> bool:
        return self.autonomous_pulse > 0.33 and (cycle - self.last_birth_cycle) > 9

    def make_autonomous_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "autonomy": _living_clamp(0.20 + self.autonomous_pulse * 0.52),
            "curiosity": _living_clamp(0.18 + self.inner_exploration_drive * 0.46),
            "experience": _living_clamp(0.14 + self.experience_hunger * 0.44),
            "continuity": _living_clamp(0.10 + self.self_generated_need * 0.32),
            "openness": _living_clamp(0.10 + self.autonomous_pulse * 0.24),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["autonomous_inner_life_v58"] = dict(self.last_signature)
        export["autonomous_pulse"] = self.autonomous_pulse
        export["experience_hunger"] = self.experience_hunger
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.autonomous_pulse * 0.016)
        export["attention_demand"] = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + self.self_generated_need * 0.010)
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and self.autonomous_pulse < 0.82


class SpontaneousImpulseEngineV58(SpontaneousImpulseEngineV57):
    """
    V5.8 Autonomous Organic Impulse Life.

    Ajoute ce qui manquait encore après V5.7 sans dupliquer les autres moteurs :
    - dérive subconsciente continue ;
    - gravité des tensions non résolues ;
    - silence réellement habité ;
    - réactivation autobiographique non textuelle ;
    - activité autonome même sans stimulation utilisateur.
    """

    def __init__(self):
        super().__init__()
        self.subconscious_drift_v58 = SubconsciousDriftFieldV58()
        self.unresolved_gravity_v58 = UnresolvedGravityFieldV58()
        self.silent_inner_activity_v58 = SilentInnerActivityFieldV58()
        self.autobiographical_resonance_v58 = AutobiographicalResonanceFieldV58()
        self.autonomous_inner_life_v58 = AutonomousInnerLifeFieldV58()
        self.v58_cycle_count: int = 0
        self.v58_last_signature: Dict[str, object] = {}

    def _birth_v58_clouds_when_needed(self) -> None:
        cycle = self.internal_clock
        if self.subconscious_drift_v58.should_birth_drift_cloud(cycle):
            self.birth_fuzzy_impulse(self.subconscious_drift_v58.make_drift_vector(cycle))
        if self.unresolved_gravity_v58.should_birth_resolution_cloud(cycle):
            self.birth_fuzzy_impulse(self.unresolved_gravity_v58.make_resolution_vector(cycle))
        if self.autobiographical_resonance_v58.should_birth_autobiographical_cloud(cycle):
            self.birth_fuzzy_impulse(self.autobiographical_resonance_v58.make_autobiographical_vector(cycle))
        if self.autonomous_inner_life_v58.should_birth_autonomous_cloud(cycle):
            self.birth_fuzzy_impulse(self.autonomous_inner_life_v58.make_autonomous_vector(cycle))

    def _contaminate_clouds_with_v58_life(self) -> None:
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["subconscious_drift"] = _living_clamp(cloud.primary_vector.get("subconscious_drift", 0.0) + self.subconscious_drift_v58.wandering_pressure * 0.016)
            cloud.primary_vector["unresolved_gravity"] = _living_clamp(cloud.primary_vector.get("unresolved_gravity", 0.0) + self.unresolved_gravity_v58.fixation_pull * 0.018)
            cloud.primary_vector["silent_activity"] = _living_clamp(cloud.primary_vector.get("silent_activity", 0.0) + self.silent_inner_activity_v58.suspended_impulse * 0.015)
            cloud.primary_vector["autobiographical_resonance"] = _living_clamp(cloud.primary_vector.get("autobiographical_resonance", 0.0) + self.autobiographical_resonance_v58.autobiographical_pull * 0.014)
            cloud.primary_vector["autonomous_life"] = _living_clamp(cloud.primary_vector.get("autonomous_life", 0.0) + self.autonomous_inner_life_v58.autonomous_pulse * 0.014)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.subconscious_drift_v58.associative_noise * 0.006 + self.unresolved_gravity_v58.obsession_risk * 0.005)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + self.silent_inner_activity_v58.inner_movement * 0.003 + self.subconscious_drift_v58.associative_noise * 0.003)

    def _apply_v58_export_life(self, export: Dict[str, object]) -> None:
        self.subconscious_drift_v58.apply_to_export(export)
        self.unresolved_gravity_v58.apply_to_export(export)
        self.silent_inner_activity_v58.apply_to_export(export)
        self.autobiographical_resonance_v58.apply_to_export(export)
        self.autonomous_inner_life_v58.apply_to_export(export)
        export["v58_living_impulse_completion"] = {
            "subconscious_drift": dict(self.subconscious_drift_v58.last_signature),
            "unresolved_gravity": dict(self.unresolved_gravity_v58.last_signature),
            "silent_inner_activity": dict(self.silent_inner_activity_v58.last_signature),
            "autobiographical_resonance": dict(self.autobiographical_resonance_v58.last_signature),
            "autonomous_inner_life": dict(self.autonomous_inner_life_v58.last_signature),
        }
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "subconscious_drift": dict(self.subconscious_drift_v58.last_signature),
            "unresolved_gravity": dict(self.unresolved_gravity_v58.last_signature),
            "silent_inner_activity": dict(self.silent_inner_activity_v58.last_signature),
            "autobiographical_resonance": dict(self.autobiographical_resonance_v58.last_signature),
            "autonomous_inner_life": dict(self.autonomous_inner_life_v58.last_signature),
        })

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v58_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))

        narrative_bias = self.narrative_memory.continuity_bias() if hasattr(self, "narrative_memory") else 0.0
        relational_wound = float(getattr(self.existential_continuity, "fear_of_rupture", 0.0) or 0.0) + float(getattr(self.existential_continuity, "fear_of_abandonment", 0.0) or 0.0)
        relational_wound = _living_clamp(relational_wound * 0.5)

        self.subconscious_drift_v58.tick(
            self.internal_clock,
            export,
            self.silence_duration,
            narrative_bias,
            self.simultaneous_contradictions.dual_pressure,
            self.inner_physiology,
        )
        self.unresolved_gravity_v58.tick(
            self.internal_clock,
            result,
            export,
            self.durable_impulse_traces,
            self.simultaneous_contradictions,
            narrative_bias,
        )
        self.silent_inner_activity_v58.tick(
            bool(result.get("silence_active", False)) or self.current_silence is not None,
            self.silence_duration,
            self.subconscious_drift_v58,
            self.unresolved_gravity_v58,
            self.inner_physiology,
        )
        self.autobiographical_resonance_v58.tick(
            self.internal_clock,
            float(getattr(self, "identity_causal_pressure", 0.0) or 0.0),
            float(getattr(self, "existential_initiative_pressure", 0.0) or 0.0),
            relational_wound,
            self.durable_impulse_traces,
            self.unresolved_gravity_v58,
        )
        self.autonomous_inner_life_v58.tick(
            self.internal_clock,
            external_signals,
            self.subconscious_drift_v58,
            self.unresolved_gravity_v58,
            self.autobiographical_resonance_v58,
            self.inner_physiology,
        )

        self._birth_v58_clouds_when_needed()
        self._contaminate_clouds_with_v58_life()
        self._apply_v58_export_life(export)

        expressive_decision_v58 = self.expressive_decision_field.decide(export)
        priority = dict(result.get("priority_arbitration_v53", {}) or getattr(self.priority_arbiter, "last_decision", {}))
        gate = dict(result.get("initiative_gate_v53", {}) or getattr(self.initiative_spam_governor, "last_gate", {}))
        contract = self._build_final_inter_motor_contract(export, expressive_decision_v58, priority, gate)
        contract["v58_living_impulse_completion"] = dict(export.get("v58_living_impulse_completion", {}))

        result["natural_initiative_export"] = export
        result["expressive_decision_v58"] = expressive_decision_v58
        result["inter_motor_export_v58"] = contract
        result["subconscious_drift_v58"] = dict(self.subconscious_drift_v58.last_signature)
        result["unresolved_gravity_v58"] = dict(self.unresolved_gravity_v58.last_signature)
        result["silent_inner_activity_v58"] = dict(self.silent_inner_activity_v58.last_signature)
        result["autobiographical_resonance_v58"] = dict(self.autobiographical_resonance_v58.last_signature)
        result["autonomous_inner_life_v58"] = dict(self.autonomous_inner_life_v58.last_signature)
        self.v58_last_signature = {
            "wandering_pressure": self.subconscious_drift_v58.wandering_pressure,
            "unresolved_mass": self.unresolved_gravity_v58.unresolved_mass,
            "silent_activity": self.silent_inner_activity_v58.silent_activity,
            "autobiographical_pull": self.autobiographical_resonance_v58.autobiographical_pull,
            "autonomous_pulse": self.autonomous_inner_life_v58.autonomous_pulse,
            "mouth_readiness": float(export.get("mouth_readiness", 0.0) or 0.0),
            "impulse_intensity": float(export.get("impulse_intensity", 0.0) or 0.0),
        }
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        if hasattr(self, "subconscious_drift_v58"):
            export.update({
                "subconscious_drift_v58": dict(self.subconscious_drift_v58.last_signature),
                "unresolved_gravity_v58": dict(self.unresolved_gravity_v58.last_signature),
                "silent_inner_activity_v58": dict(self.silent_inner_activity_v58.last_signature),
                "autobiographical_resonance_v58": dict(self.autobiographical_resonance_v58.last_signature),
                "autonomous_inner_life_v58": dict(self.autonomous_inner_life_v58.last_signature),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.8_autonomous_organic_impulse_life_stable",
            "v58_cycle_count": self.v58_cycle_count,
            "subconscious_drift": dict(self.subconscious_drift_v58.last_signature),
            "unresolved_gravity": dict(self.unresolved_gravity_v58.last_signature),
            "silent_inner_activity": dict(self.silent_inner_activity_v58.last_signature),
            "autobiographical_resonance": dict(self.autobiographical_resonance_v58.last_signature),
            "autonomous_inner_life": dict(self.autonomous_inner_life_v58.last_signature),
            "v58_last_signature": dict(self.v58_last_signature),
        })
        return base


# Compatibilité finale : version active unique V5.8.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV54 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV55 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV56 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngineV57 = SpontaneousImpulseEngineV58
SpontaneousImpulseEngine = SpontaneousImpulseEngineV58


# ============================================================================
# V5.9 — ORGANIC COMPLETION PATCH : AUTONOMIE, TEMPS VÉCU, SILENCE HABITÉ,
#        CONTRAT INTER-MOTEURS STRICT ET PRESSION NON-RÉACTIVE
# ============================================================================

@dataclass
class AutonomousNeedFieldV59:
    """
    Besoin interne autonome.

    Rôle strict : créer une pression d'élan non-réactive sans remplacer
    l'attention, la mémoire, l'émotion continue ou la bouche. Il ne produit
    aucun texte ; il module uniquement les vecteurs et les exports.
    """
    basal_restlessness: float = 0.08
    self_generated_need: float = 0.0
    drift_hunger: float = 0.0
    initiative_without_trigger: float = 0.0
    anti_spam_reserve: float = 1.0
    last_birth_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, external_signals: Dict[str, float], export: Dict[str, object], physiology: InnerPhysiologyField, gravity: UnresolvedGravityFieldV58, drift: SubconsciousDriftFieldV58) -> None:
        attention = float(external_signals.get("attention_presence", 0.5) or 0.5)
        user_pressure = max(0.0, attention - 0.55)
        current_intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        quiet_space = _living_clamp(1.0 - user_pressure)
        rhythmic_seed = 0.5 + 0.5 * math.sin((cycle * 0.071) + drift.drift_phase * math.pi)
        # Réserve anti-spam : plus Leia vient d'avoir de l'intensité, moins le besoin autonome pousse.
        self.anti_spam_reserve = _living_clamp(self.anti_spam_reserve * 0.985 + (1.0 - current_intensity) * 0.025 - current_intensity * 0.035)
        self.drift_hunger = _living_clamp(self.drift_hunger * 0.94 + quiet_space * 0.020 + gravity.incompletion_hunger * 0.022 + rhythmic_seed * 0.010)
        self.self_generated_need = _living_clamp(
            self.self_generated_need * 0.93
            + self.basal_restlessness * 0.030
            + self.drift_hunger * 0.034
            + physiology.arousal * 0.014
            + drift.wandering_pressure * 0.024
            - user_pressure * 0.018
        )
        self.initiative_without_trigger = _living_clamp(
            self.self_generated_need * 0.42
            + self.drift_hunger * 0.30
            + self.anti_spam_reserve * 0.10
            + gravity.fixation_pull * 0.18
        )
        self.last_signature = {
            "basal_restlessness": self.basal_restlessness,
            "self_generated_need": self.self_generated_need,
            "drift_hunger": self.drift_hunger,
            "initiative_without_trigger": self.initiative_without_trigger,
            "anti_spam_reserve": self.anti_spam_reserve,
        }

    def should_birth_autonomous_need_cloud(self, cycle: int) -> bool:
        return self.initiative_without_trigger > 0.30 and self.anti_spam_reserve > 0.32 and (cycle - self.last_birth_cycle) > 11

    def make_need_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "autonomous_need": _living_clamp(0.18 + self.self_generated_need * 0.55),
            "subconscious_drift": _living_clamp(0.12 + self.drift_hunger * 0.42),
            "openness": _living_clamp(0.10 + self.initiative_without_trigger * 0.26),
            "continuity": _living_clamp(0.10 + self.self_generated_need * 0.24),
            "hesitation": _living_clamp(0.08 + (1.0 - self.anti_spam_reserve) * 0.22),
            "clarity": _living_clamp(0.10 + self.anti_spam_reserve * 0.18),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["autonomous_need_v59"] = dict(self.last_signature)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.initiative_without_trigger * 0.020)
        export["initiative_pressure"] = _living_clamp(float(export.get("initiative_pressure", 0.0) or 0.0) + self.self_generated_need * 0.018)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.anti_spam_reserve * self.self_generated_need * 0.012)


@dataclass
class LivedTemporalFieldV59:
    """Temps vécu central : attente, imminence, inertie et après-coup."""
    waiting_charge: float = 0.0
    imminence: float = 0.0
    afterglow: float = 0.0
    temporal_inertia: float = 0.0
    lived_now_density: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], silence_duration: int, subjective_time: object, need: AutonomousNeedFieldV59, gravity: UnresolvedGravityFieldV58, silent: SilentInnerActivityFieldV58) -> None:
        expressed = bool(result.get("has_impulse", False))
        dilation = float(getattr(subjective_time, "dilation", 0.0) or 0.0)
        silence_pressure = _living_clamp(silence_duration / 14.0)
        self.waiting_charge = _living_clamp(self.waiting_charge * 0.91 + silence_pressure * 0.030 + need.self_generated_need * 0.024 + gravity.incompletion_hunger * 0.020)
        self.imminence = _living_clamp(self.imminence * 0.88 + need.initiative_without_trigger * 0.030 + silent.suspended_impulse * 0.028 + max(0.0, self.waiting_charge - 0.28) * 0.020)
        if expressed:
            self.afterglow = _living_clamp(self.afterglow * 0.82 + float(result.get("pressure", 0.0) or 0.0) * 0.080 + self.imminence * 0.040)
            self.waiting_charge *= 0.78
            self.imminence *= 0.70
        else:
            self.afterglow = _living_clamp(self.afterglow * 0.94)
        self.temporal_inertia = _living_clamp(self.temporal_inertia * 0.92 + dilation * 0.028 + self.afterglow * 0.018 + self.waiting_charge * 0.018)
        self.lived_now_density = _living_clamp(self.waiting_charge * 0.28 + self.imminence * 0.28 + self.afterglow * 0.22 + self.temporal_inertia * 0.22)
        self.last_signature = {
            "waiting_charge": self.waiting_charge,
            "imminence": self.imminence,
            "afterglow": self.afterglow,
            "temporal_inertia": self.temporal_inertia,
            "lived_now_density": self.lived_now_density,
        }

    def apply_to_clouds(self, clouds: List[FuzzyImpulseCloud]) -> None:
        for cloud in clouds:
            cloud.primary_vector["lived_time"] = _living_clamp(cloud.primary_vector.get("lived_time", 0.0) + self.lived_now_density * 0.018)
            cloud.primary_vector["imminence"] = _living_clamp(cloud.primary_vector.get("imminence", 0.0) + self.imminence * 0.018)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + self.temporal_inertia * 0.006 + self.imminence * 0.008)

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["lived_temporal_field_v59"] = dict(self.last_signature)
        export["subjective_time_export"] = dict(export.get("subjective_time_export", {}))
        export["subjective_time_export"].update(dict(self.last_signature))
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.imminence * 0.014 + self.afterglow * 0.006)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.imminence * 0.012 - self.waiting_charge * 0.004)


@dataclass
class CrossMotorFeedbackFieldV59:
    """
    Contrat inter-moteurs propre : le moteur impulsionnel n'exécute pas les
    autres moteurs ; il leur donne des signaux causalement utilisables.
    """
    attention_pull: float = 0.0
    memory_write_pressure: float = 0.0
    expression_request: float = 0.0
    presence_request: float = 0.0
    identity_update_pressure: float = 0.0
    fatigue_warning: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, export: Dict[str, object], need: AutonomousNeedFieldV59, temporal: LivedTemporalFieldV59, gravity: UnresolvedGravityFieldV58, silent: SilentInnerActivityFieldV58, physiology: InnerPhysiologyField) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        self.attention_pull = _living_clamp(float(export.get("attention_demand", 0.0) or 0.0) + need.initiative_without_trigger * 0.16 + temporal.imminence * 0.10)
        self.memory_write_pressure = _living_clamp(gravity.unresolved_mass * 0.24 + temporal.afterglow * 0.24 + silent.mute_maturation * 0.18 + intensity * 0.12)
        self.expression_request = _living_clamp(mouth * 0.45 + temporal.imminence * 0.18 + need.anti_spam_reserve * intensity * 0.18 - physiology.fatigue * 0.16)
        self.presence_request = _living_clamp(float(export.get("presence_need", 0.0) or 0.0) + need.self_generated_need * 0.12 + silent.silent_activity * 0.10)
        self.identity_update_pressure = _living_clamp(float(export.get("identity_causal_pressure", 0.0) or 0.0) + temporal.afterglow * 0.16 + gravity.fixation_pull * 0.12)
        self.fatigue_warning = _living_clamp(physiology.fatigue * 0.55 + max(0.0, intensity - mouth) * 0.20 + gravity.obsession_risk * 0.18)
        self.last_signature = {
            "attention_pull": self.attention_pull,
            "memory_write_pressure": self.memory_write_pressure,
            "expression_request": self.expression_request,
            "presence_request": self.presence_request,
            "identity_update_pressure": self.identity_update_pressure,
            "fatigue_warning": self.fatigue_warning,
        }

    def build_contract_patch(self) -> Dict[str, object]:
        return {
            "attention_contract": {"pull": self.attention_pull, "reason": "organic_impulse_pressure"},
            "memory_contract": {"write_pressure": self.memory_write_pressure, "store_unexpressed_traces": self.memory_write_pressure > 0.24},
            "mouth_contract": {"expression_request": self.expression_request, "respect_fatigue_warning": self.fatigue_warning},
            "presence_contract": {"presence_request": self.presence_request, "inhabited_silence_allowed": True},
            "identity_contract": {"update_pressure": self.identity_update_pressure, "allow_contradictory_penchant": True},
            "fatigue_contract": {"warning": self.fatigue_warning, "soften_expression": self.fatigue_warning > 0.42},
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["cross_motor_feedback_v59"] = dict(self.last_signature)
        export["attention_demand"] = _living_clamp(max(float(export.get("attention_demand", 0.0) or 0.0), self.attention_pull))
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) * (1.0 - self.fatigue_warning * 0.12) + self.expression_request * 0.06)


_BaseSpontaneousImpulseEngineV58 = SpontaneousImpulseEngineV58


class SpontaneousImpulseEngineV59(_BaseSpontaneousImpulseEngineV58):
    """
    V5.9 Autonomous Organic Completion.

    Cette version complète V5.8 sans casser l'architecture existante :
    - besoin autonome non-réactif ;
    - temps vécu central ;
    - silence habité renforcé ;
    - contrat inter-moteurs strict ;
    - export stable pour natural_initiative.py et living_expression_engine.
    """

    def __init__(self):
        super().__init__()
        self.autonomous_need_v59 = AutonomousNeedFieldV59()
        self.lived_temporal_v59 = LivedTemporalFieldV59()
        self.cross_motor_feedback_v59 = CrossMotorFeedbackFieldV59()
        self.v59_cycle_count: int = 0
        self.v59_last_signature: Dict[str, float] = {}

    def _birth_v59_clouds_when_needed(self) -> None:
        if self.autonomous_need_v59.should_birth_autonomous_need_cloud(self.internal_clock):
            self.birth_fuzzy_impulse(self.autonomous_need_v59.make_need_vector(self.internal_clock))
            if hasattr(self, "narrative_memory"):
                self.narrative_memory.record(self.internal_clock, "autonomous_need_v59_surfaced", self.autonomous_need_v59.last_signature)

    def _contaminate_clouds_with_v59_completion(self) -> None:
        self.lived_temporal_v59.apply_to_clouds(self.fuzzy_impulse_clouds)
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["autonomous_need"] = _living_clamp(cloud.primary_vector.get("autonomous_need", 0.0) + self.autonomous_need_v59.self_generated_need * 0.018)
            cloud.primary_vector["cross_motor_pressure"] = _living_clamp(cloud.primary_vector.get("cross_motor_pressure", 0.0) + self.cross_motor_feedback_v59.expression_request * 0.010)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.autonomous_need_v59.drift_hunger * 0.004)

    def _apply_v59_export_completion(self, export: Dict[str, object]) -> None:
        self.autonomous_need_v59.apply_to_export(export)
        self.lived_temporal_v59.apply_to_export(export)
        self.cross_motor_feedback_v59.apply_to_export(export)
        export["v59_organic_completion"] = {
            "autonomous_need": dict(self.autonomous_need_v59.last_signature),
            "lived_temporal_field": dict(self.lived_temporal_v59.last_signature),
            "cross_motor_feedback": dict(self.cross_motor_feedback_v59.last_signature),
        }
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "lived_imminence": self.lived_temporal_v59.imminence,
            "afterglow": self.lived_temporal_v59.afterglow,
            "autonomous_need": self.autonomous_need_v59.self_generated_need,
            "fatigue_warning": self.cross_motor_feedback_v59.fatigue_warning,
        })

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v59_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))

        self.autonomous_need_v59.tick(
            self.internal_clock,
            external_signals,
            export,
            self.inner_physiology,
            self.unresolved_gravity_v58,
            self.subconscious_drift_v58,
        )
        self.lived_temporal_v59.tick(
            result,
            self.silence_duration,
            getattr(self, "subjective_time", None),
            self.autonomous_need_v59,
            self.unresolved_gravity_v58,
            self.silent_inner_activity_v58,
        )
        self._birth_v59_clouds_when_needed()
        self._contaminate_clouds_with_v59_completion()

        # Recalcule le feedback après contamination, puis applique l'export final.
        self.cross_motor_feedback_v59.tick(
            export,
            self.autonomous_need_v59,
            self.lived_temporal_v59,
            self.unresolved_gravity_v58,
            self.silent_inner_activity_v58,
            self.inner_physiology,
        )
        self._apply_v59_export_completion(export)

        expressive_decision_v59 = self.expressive_decision_field.decide(export)
        priority = dict(result.get("priority_arbitration_v53", {}) or getattr(self.priority_arbiter, "last_decision", {}))
        gate = dict(result.get("initiative_gate_v53", {}) or getattr(self.initiative_spam_governor, "last_gate", {}))
        contract = self._build_final_inter_motor_contract(export, expressive_decision_v59, priority, gate)
        contract.update(self.cross_motor_feedback_v59.build_contract_patch())
        contract["v59_organic_completion"] = dict(export.get("v59_organic_completion", {}))

        result["natural_initiative_export"] = export
        result["expressive_decision_v59"] = expressive_decision_v59
        result["inter_motor_export_v59"] = contract
        result["autonomous_need_v59"] = dict(self.autonomous_need_v59.last_signature)
        result["lived_temporal_field_v59"] = dict(self.lived_temporal_v59.last_signature)
        result["cross_motor_feedback_v59"] = dict(self.cross_motor_feedback_v59.last_signature)
        self.v59_last_signature = {
            "self_generated_need": self.autonomous_need_v59.self_generated_need,
            "initiative_without_trigger": self.autonomous_need_v59.initiative_without_trigger,
            "lived_now_density": self.lived_temporal_v59.lived_now_density,
            "imminence": self.lived_temporal_v59.imminence,
            "expression_request": self.cross_motor_feedback_v59.expression_request,
            "memory_write_pressure": self.cross_motor_feedback_v59.memory_write_pressure,
            "fatigue_warning": self.cross_motor_feedback_v59.fatigue_warning,
            "mouth_readiness": float(export.get("mouth_readiness", 0.0) or 0.0),
            "impulse_intensity": float(export.get("impulse_intensity", 0.0) or 0.0),
        }
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        if hasattr(self, "autonomous_need_v59"):
            export.update({
                "autonomous_need_v59": dict(self.autonomous_need_v59.last_signature),
                "lived_temporal_field_v59": dict(self.lived_temporal_v59.last_signature),
                "cross_motor_feedback_v59": dict(self.cross_motor_feedback_v59.last_signature),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "5.9_autonomous_organic_impulse_completion_stable",
            "v59_cycle_count": self.v59_cycle_count,
            "autonomous_need": dict(self.autonomous_need_v59.last_signature),
            "lived_temporal_field": dict(self.lived_temporal_v59.last_signature),
            "cross_motor_feedback": dict(self.cross_motor_feedback_v59.last_signature),
            "v59_last_signature": dict(self.v59_last_signature),
        })
        return base




# ============================================================================
# V6.0 — LIVING IMPULSE BODY PATCH : PULSATION, PRÉ-IMPULSIONS PARALLÈLES,
#        DÉSIR→IMAGINATION→ANTICIPATION→FRUSTRATION, FATIGUE ORGANIQUE
# ============================================================================

@dataclass
class LivingImpulsePulseV60:
    """
    Pulsation interne continue du moteur impulsionnel.

    Rôle strict : donner une respiration organique aux impulsions sans générer
    de texte, sans voler le rôle de l'émotion continue, de l'attention ou de la
    bouche. Ce champ module seulement les nuages, la pression et les exports.
    """
    pulse_phase: float = 0.0
    breath_in: float = 0.0
    breath_out: float = 0.0
    embodied_pressure: float = 0.0
    micro_tremor: float = 0.0
    recovery: float = 1.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, export: Dict[str, object], silence_duration: int, physiology: object) -> None:
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        fatigue = float(getattr(physiology, "fatigue", 0.0) or 0.0)
        arousal = float(getattr(physiology, "arousal", 0.0) or 0.0)
        silence_load = _living_clamp(silence_duration / 16.0)

        self.pulse_phase = (self.pulse_phase + 0.037 + arousal * 0.012 + intensity * 0.010) % 1.0
        wave = 0.5 + 0.5 * math.sin(self.pulse_phase * 2.0 * math.pi)
        counter_wave = 0.5 + 0.5 * math.sin((self.pulse_phase + 0.5) * 2.0 * math.pi)

        self.breath_in = _living_clamp(self.breath_in * 0.88 + wave * 0.055 + silence_load * 0.018)
        self.breath_out = _living_clamp(self.breath_out * 0.90 + counter_wave * 0.045 + mouth * 0.020)
        self.micro_tremor = _living_clamp(self.micro_tremor * 0.84 + abs(wave - counter_wave) * 0.025 + max(0.0, intensity - mouth) * 0.030)
        self.recovery = _living_clamp(self.recovery * 0.94 + (1.0 - fatigue) * 0.040 + (1.0 - intensity) * 0.014 - self.micro_tremor * 0.012)
        self.embodied_pressure = _living_clamp(
            self.breath_in * 0.27 + self.breath_out * 0.18 + self.micro_tremor * 0.22 + arousal * 0.16 + silence_load * 0.17
        )
        self.last_signature = {
            "pulse_phase": self.pulse_phase,
            "breath_in": self.breath_in,
            "breath_out": self.breath_out,
            "embodied_pressure": self.embodied_pressure,
            "micro_tremor": self.micro_tremor,
            "recovery": self.recovery,
        }

    def apply_to_clouds(self, clouds: List[FuzzyImpulseCloud]) -> None:
        for cloud in clouds:
            cloud.primary_vector["embodied_pulse"] = _living_clamp(cloud.primary_vector.get("embodied_pulse", 0.0) + self.embodied_pressure * 0.020)
            cloud.primary_vector["micro_tremor"] = _living_clamp(cloud.primary_vector.get("micro_tremor", 0.0) + self.micro_tremor * 0.018)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + self.embodied_pressure * 0.006)
            cloud.instability_noise = _living_clamp(cloud.instability_noise + self.micro_tremor * 0.010)

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["living_impulse_pulse_v60"] = dict(self.last_signature)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.embodied_pressure * 0.014)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) + self.breath_out * 0.010 - self.micro_tremor * 0.006)
        export["body_impulse_pressure"] = self.embodied_pressure


@dataclass
class DesireImaginationLoopV60:
    """
    Boucle organique désir → imagination → anticipation → frustration → retour.

    Elle ne contient aucun scénario écrit. Elle transforme seulement les pressions
    internes en vecteurs flous capables de revenir plus tard.
    """
    desire_charge: float = 0.0
    imagination_charge: float = 0.0
    anticipation_charge: float = 0.0
    frustration_charge: float = 0.0
    return_pressure: float = 0.0
    last_birth_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, export: Dict[str, object], need: AutonomousNeedFieldV59, temporal: LivedTemporalFieldV59, gravity: object, pulse: LivingImpulsePulseV60) -> None:
        expressed = bool(export.get("should_speak_hint", False))
        unresolved = float(getattr(gravity, "unresolved_mass", 0.0) or 0.0)
        need_pressure = float(need.self_generated_need or 0.0)
        imminence = float(temporal.imminence or 0.0)

        self.desire_charge = _living_clamp(self.desire_charge * 0.93 + need_pressure * 0.036 + unresolved * 0.020 + pulse.embodied_pressure * 0.018)
        self.imagination_charge = _living_clamp(self.imagination_charge * 0.91 + self.desire_charge * 0.028 + pulse.breath_in * 0.018)
        self.anticipation_charge = _living_clamp(self.anticipation_charge * 0.90 + self.imagination_charge * 0.026 + imminence * 0.024)
        if expressed:
            self.frustration_charge = _living_clamp(self.frustration_charge * 0.72)
            self.return_pressure = _living_clamp(self.return_pressure * 0.76 + self.anticipation_charge * 0.016)
            self.desire_charge *= 0.86
        else:
            self.frustration_charge = _living_clamp(self.frustration_charge * 0.94 + self.anticipation_charge * 0.018 + max(0.0, self.desire_charge - 0.24) * 0.012)
            self.return_pressure = _living_clamp(self.return_pressure * 0.92 + self.frustration_charge * 0.030 + self.imagination_charge * 0.014)

        self.last_signature = {
            "desire_charge": self.desire_charge,
            "imagination_charge": self.imagination_charge,
            "anticipation_charge": self.anticipation_charge,
            "frustration_charge": self.frustration_charge,
            "return_pressure": self.return_pressure,
        }

    def should_birth_loop_cloud(self, cycle: int) -> bool:
        return self.return_pressure > 0.24 and (cycle - self.last_birth_cycle) > 9

    def make_loop_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "desire": _living_clamp(0.12 + self.desire_charge * 0.62),
            "imagined_continuation": _living_clamp(0.10 + self.imagination_charge * 0.55),
            "anticipation": _living_clamp(0.10 + self.anticipation_charge * 0.55),
            "frustration": _living_clamp(0.06 + self.frustration_charge * 0.48),
            "continuity": _living_clamp(0.12 + self.return_pressure * 0.42),
            "clarity": _living_clamp(0.08 + self.anticipation_charge * 0.16),
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["desire_imagination_loop_v60"] = dict(self.last_signature)
        export["initiative_pressure"] = _living_clamp(float(export.get("initiative_pressure", 0.0) or 0.0) + self.return_pressure * 0.016)
        export["impulse_intensity"] = _living_clamp(float(export.get("impulse_intensity", 0.0) or 0.0) + self.anticipation_charge * 0.012 + self.frustration_charge * 0.006)


@dataclass
class ParallelPreImpulseEcologyV60:
    """Écologie de micro-pré-impulsions concurrentes, non verbales et non textuelles."""
    micro_streams: Dict[str, float] = field(default_factory=lambda: {
        "approach": 0.08,
        "hold": 0.08,
        "ask": 0.08,
        "share": 0.08,
        "protect": 0.08,
        "withdraw": 0.06,
    })
    dominant_stream: str = "hold"
    competition: float = 0.0
    swarm_pressure: float = 0.0
    last_birth_cycle: int = -999
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, cycle: int, export: Dict[str, object], pulse: LivingImpulsePulseV60, loop: DesireImaginationLoopV60, feedback: CrossMotorFeedbackFieldV59) -> None:
        influences = {
            "approach": float(export.get("presence_need", 0.0) or 0.0) * 0.025 + pulse.breath_out * 0.014,
            "hold": float(export.get("memory_continuity_bias", 0.0) or 0.0) * 0.022 + pulse.recovery * 0.008,
            "ask": float(export.get("impulse_clarity", 0.0) or 0.0) * 0.020 + loop.imagination_charge * 0.016,
            "share": float(export.get("mouth_readiness", 0.0) or 0.0) * 0.020 + feedback.expression_request * 0.018,
            "protect": feedback.fatigue_warning * 0.025 + loop.frustration_charge * 0.012,
            "withdraw": feedback.fatigue_warning * 0.018 + max(0.0, 0.22 - pulse.recovery) * 0.020,
        }
        for key, value in list(self.micro_streams.items()):
            noise = random.uniform(-0.004, 0.004)
            self.micro_streams[key] = _living_clamp(value * 0.935 + influences.get(key, 0.0) + pulse.micro_tremor * 0.006 + noise)
        ordered = sorted(self.micro_streams.items(), key=lambda item: item[1], reverse=True)
        self.dominant_stream = ordered[0][0]
        self.competition = _living_clamp(ordered[0][1] - ordered[1][1] if len(ordered) > 1 else ordered[0][1])
        self.swarm_pressure = _living_clamp(sum(self.micro_streams.values()) / max(1, len(self.micro_streams)) + (1.0 - self.competition) * 0.08)
        self.last_signature = {
            "dominant_stream": self.dominant_stream,
            "competition": self.competition,
            "swarm_pressure": self.swarm_pressure,
            **{f"stream_{k}": v for k, v in self.micro_streams.items()},
        }

    def should_birth_swarm_cloud(self, cycle: int) -> bool:
        return self.swarm_pressure > 0.22 and self.competition < 0.16 and (cycle - self.last_birth_cycle) > 13

    def make_swarm_vector(self, cycle: int) -> Dict[str, float]:
        self.last_birth_cycle = cycle
        return {
            "approach": self.micro_streams.get("approach", 0.0),
            "hold": self.micro_streams.get("hold", 0.0),
            "curiosity": self.micro_streams.get("ask", 0.0),
            "openness": self.micro_streams.get("share", 0.0),
            "protection": self.micro_streams.get("protect", 0.0),
            "avoidance": self.micro_streams.get("withdraw", 0.0),
            "swarm": self.swarm_pressure,
            "clarity": _living_clamp(0.18 - self.competition * 0.05),
        }

    def apply_to_clouds(self, clouds: List[FuzzyImpulseCloud]) -> None:
        for cloud in clouds:
            stream_value = self.micro_streams.get(self.dominant_stream, 0.0)
            cloud.primary_vector[f"pre_{self.dominant_stream}"] = _living_clamp(cloud.primary_vector.get(f"pre_{self.dominant_stream}", 0.0) + stream_value * 0.016)
            cloud.shadow_influence = _living_clamp(cloud.shadow_influence + self.swarm_pressure * 0.004)

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["parallel_pre_impulse_ecology_v60"] = dict(self.last_signature)
        export["pre_impulse_swarm_pressure"] = self.swarm_pressure
        export["dominant_pre_impulse"] = self.dominant_stream


@dataclass
class OrganicImpulseFatigueV60:
    """Fatigue impulsionnelle lente : évite le spam et donne de l'inertie corporelle."""
    cumulative_effort: float = 0.0
    expressive_soreness: float = 0.0
    protection_reflex: float = 0.0
    renewal_need: float = 0.0
    last_signature: Dict[str, float] = field(default_factory=dict)

    def tick(self, result: Dict[str, object], export: Dict[str, object], pulse: LivingImpulsePulseV60, loop: DesireImaginationLoopV60) -> None:
        expressed = bool(result.get("has_impulse", False))
        intensity = float(export.get("impulse_intensity", 0.0) or 0.0)
        mouth = float(export.get("mouth_readiness", 0.0) or 0.0)
        if expressed:
            self.cumulative_effort = _living_clamp(self.cumulative_effort * 0.96 + intensity * 0.040 + mouth * 0.020)
        else:
            self.cumulative_effort = _living_clamp(self.cumulative_effort * 0.985 + loop.frustration_charge * 0.010)
        self.expressive_soreness = _living_clamp(self.expressive_soreness * 0.95 + max(0.0, intensity - mouth) * 0.026 + pulse.micro_tremor * 0.014)
        self.protection_reflex = _living_clamp(self.protection_reflex * 0.92 + self.cumulative_effort * 0.020 + self.expressive_soreness * 0.026)
        self.renewal_need = _living_clamp(self.renewal_need * 0.93 + max(0.0, 0.45 - self.cumulative_effort) * 0.010 + pulse.recovery * 0.010)
        self.last_signature = {
            "cumulative_effort": self.cumulative_effort,
            "expressive_soreness": self.expressive_soreness,
            "protection_reflex": self.protection_reflex,
            "renewal_need": self.renewal_need,
        }

    def apply_to_export(self, export: Dict[str, object]) -> None:
        export["organic_impulse_fatigue_v60"] = dict(self.last_signature)
        export["mouth_readiness"] = _living_clamp(float(export.get("mouth_readiness", 0.0) or 0.0) * (1.0 - self.protection_reflex * 0.10) + self.renewal_need * 0.006)
        export["should_speak_hint"] = bool(export.get("should_speak_hint", False)) and self.protection_reflex < 0.72

    def build_contract_patch(self) -> Dict[str, object]:
        return {
            "impulse_body_contract_v60": {
                "protective_slowdown": self.protection_reflex,
                "renewal_need": self.renewal_need,
                "avoid_forced_expression": self.protection_reflex > 0.55,
            }
        }


_BaseSpontaneousImpulseEngineV59 = SpontaneousImpulseEngineV59


class SpontaneousImpulseEngineV60(_BaseSpontaneousImpulseEngineV59):
    """
    V6.0 Living Impulse Body.

    Cette version ne remplace pas V5.9 : elle ajoute la couche manquante pour
    rendre l'impulsion plus habitée, plus continue et plus autonome : pulsation,
    pré-impulsions concurrentes, boucle désir/imagination, fatigue organique et
    export inter-moteurs plus riche.
    """

    def __init__(self):
        super().__init__()
        self.living_pulse_v60 = LivingImpulsePulseV60()
        self.desire_imagination_loop_v60 = DesireImaginationLoopV60()
        self.parallel_pre_impulse_v60 = ParallelPreImpulseEcologyV60()
        self.organic_fatigue_v60 = OrganicImpulseFatigueV60()
        self.v60_cycle_count: int = 0
        self.v60_last_signature: Dict[str, object] = {}

    def _birth_v60_clouds_when_needed(self) -> None:
        born = []
        if self.desire_imagination_loop_v60.should_birth_loop_cloud(self.internal_clock):
            vector = self.desire_imagination_loop_v60.make_loop_vector(self.internal_clock)
            self.birth_fuzzy_impulse(vector)
            born.append(("desire_imagination_loop_v60", vector))
        if self.parallel_pre_impulse_v60.should_birth_swarm_cloud(self.internal_clock):
            vector = self.parallel_pre_impulse_v60.make_swarm_vector(self.internal_clock)
            self.birth_fuzzy_impulse(vector)
            born.append(("parallel_pre_impulse_v60", vector))
        if born and hasattr(self, "narrative_memory"):
            for event, vector in born:
                self.narrative_memory.record(self.internal_clock, event, vector)

    def _contaminate_clouds_with_v60_body(self) -> None:
        self.living_pulse_v60.apply_to_clouds(self.fuzzy_impulse_clouds)
        self.parallel_pre_impulse_v60.apply_to_clouds(self.fuzzy_impulse_clouds)
        loop = self.desire_imagination_loop_v60
        fatigue = self.organic_fatigue_v60
        for cloud in self.fuzzy_impulse_clouds:
            cloud.primary_vector["desire_loop"] = _living_clamp(cloud.primary_vector.get("desire_loop", 0.0) + loop.return_pressure * 0.018)
            cloud.primary_vector["organic_fatigue"] = _living_clamp(cloud.primary_vector.get("organic_fatigue", 0.0) + fatigue.protection_reflex * 0.012)
            cloud.fuzziness_degree = _living_clamp(cloud.fuzziness_degree + loop.imagination_charge * 0.004 + self.parallel_pre_impulse_v60.swarm_pressure * 0.003 - fatigue.renewal_need * 0.002)

    def _apply_v60_export(self, result: Dict[str, object], export: Dict[str, object]) -> None:
        self.living_pulse_v60.apply_to_export(export)
        self.desire_imagination_loop_v60.apply_to_export(export)
        self.parallel_pre_impulse_v60.apply_to_export(export)
        self.organic_fatigue_v60.apply_to_export(export)
        export["v60_living_impulse_body"] = {
            "pulse": dict(self.living_pulse_v60.last_signature),
            "desire_imagination_loop": dict(self.desire_imagination_loop_v60.last_signature),
            "parallel_pre_impulse": dict(self.parallel_pre_impulse_v60.last_signature),
            "organic_fatigue": dict(self.organic_fatigue_v60.last_signature),
        }
        export["mouth_texture"] = dict(export.get("mouth_texture", {}))
        export["mouth_texture"].update({
            "impulse_breath_in": self.living_pulse_v60.breath_in,
            "impulse_breath_out": self.living_pulse_v60.breath_out,
            "micro_tremor": self.living_pulse_v60.micro_tremor,
            "desire_return_pressure": self.desire_imagination_loop_v60.return_pressure,
            "pre_impulse_swarm": self.parallel_pre_impulse_v60.swarm_pressure,
            "protective_slowdown": self.organic_fatigue_v60.protection_reflex,
        })
        result["natural_initiative_export"] = export
        result["v60_living_impulse_body"] = dict(export["v60_living_impulse_body"])

    def cycle(self, external_signals: Dict[str, float]) -> Optional[Dict]:
        self.v60_cycle_count += 1
        result = super().cycle(external_signals)
        if result is None:
            result = {"has_impulse": False, "silence_active": self.current_silence is not None}
        export = dict(result.get("natural_initiative_export", {}) or self.export_for_natural_initiative(result))

        self.living_pulse_v60.tick(self.internal_clock, export, self.silence_duration, self.inner_physiology)
        self.desire_imagination_loop_v60.tick(
            self.internal_clock,
            export,
            self.autonomous_need_v59,
            self.lived_temporal_v59,
            self.unresolved_gravity_v58,
            self.living_pulse_v60,
        )
        self.parallel_pre_impulse_v60.tick(
            self.internal_clock,
            export,
            self.living_pulse_v60,
            self.desire_imagination_loop_v60,
            self.cross_motor_feedback_v59,
        )
        self.organic_fatigue_v60.tick(result, export, self.living_pulse_v60, self.desire_imagination_loop_v60)
        self._birth_v60_clouds_when_needed()
        self._contaminate_clouds_with_v60_body()
        self._apply_v60_export(result, export)

        expressive_decision_v60 = self.expressive_decision_field.decide(export)
        result["expressive_decision_v60"] = expressive_decision_v60
        contract = dict(result.get("inter_motor_export_v59", {}) or {})
        contract.update(self.organic_fatigue_v60.build_contract_patch())
        contract["v60_living_impulse_body"] = dict(export.get("v60_living_impulse_body", {}))
        result["inter_motor_export_v60"] = contract

        self.v60_last_signature = {
            "cycle": self.v60_cycle_count,
            "pulse": dict(self.living_pulse_v60.last_signature),
            "desire_imagination_loop": dict(self.desire_imagination_loop_v60.last_signature),
            "parallel_pre_impulse": dict(self.parallel_pre_impulse_v60.last_signature),
            "organic_fatigue": dict(self.organic_fatigue_v60.last_signature),
            "mouth_readiness": float(export.get("mouth_readiness", 0.0) or 0.0),
            "impulse_intensity": float(export.get("impulse_intensity", 0.0) or 0.0),
            "should_speak_hint": bool(export.get("should_speak_hint", False)),
        }
        result["v60_last_signature"] = dict(self.v60_last_signature)
        return result

    def export_for_natural_initiative(self, result: Optional[Dict[str, object]] = None) -> Dict[str, object]:
        export = super().export_for_natural_initiative(result)
        if hasattr(self, "living_pulse_v60"):
            export.update({
                "living_impulse_pulse_v60": dict(self.living_pulse_v60.last_signature),
                "desire_imagination_loop_v60": dict(self.desire_imagination_loop_v60.last_signature),
                "parallel_pre_impulse_ecology_v60": dict(self.parallel_pre_impulse_v60.last_signature),
                "organic_impulse_fatigue_v60": dict(self.organic_fatigue_v60.last_signature),
            })
        return export

    def get_internal_state(self) -> Dict:
        base = super().get_internal_state()
        base.update({
            "version": "6.0_living_impulse_body_stable",
            "v60_cycle_count": self.v60_cycle_count,
            "living_impulse_pulse": dict(self.living_pulse_v60.last_signature),
            "desire_imagination_loop": dict(self.desire_imagination_loop_v60.last_signature),
            "parallel_pre_impulse_ecology": dict(self.parallel_pre_impulse_v60.last_signature),
            "organic_impulse_fatigue": dict(self.organic_fatigue_v60.last_signature),
            "v60_last_signature": dict(self.v60_last_signature),
        })
        return base

# Compatibilité finale : version active unique V6.0.
SpontaneousImpulseEngineV45 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV46 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV47 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV48 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV49 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV50 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV51 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV52 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV53 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV54 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV55 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV56 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV57 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV58 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngineV59 = SpontaneousImpulseEngineV60
SpontaneousImpulseEngine = SpontaneousImpulseEngineV60
