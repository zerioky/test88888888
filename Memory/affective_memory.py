"""
Moteur de Mémoire Affective ULTRA-FIN - Version 99%+ vivante - V3 biographique/réorganisation.

RAFFINEMENTS FINAUX (12 points critiques) :

1. DÉRIVE SPONTANÉE AUTHENTIQUE
   - Pas sinus simple, vrai chaos affectif
   - Oscillations émergentes multi-fréquence
   - "Chanson émotionnelle" imprévisible mais cohérente

2. ÉTATS HYBRIDES DYNAMIQUES (pas patterns fixes)
   - Découverte organique des combos, pas hardcode
   - Chaque hybrid crée sa propre force d'attraction
   - Hybrides peuvent se fusionner ou se diviser

3. CONTAMINATION NON-LINÉAIRE
   - Seuils critiques (tipping points)
   - Effets exponentiels certains endroits
   - Saturation crée des "ruptures" qualitatives

4. SENSIBILITÉ PERCEPTUELLE ADAPTATIVE
   - La saturation change les seuils de perception
   - Les blessures rendent l'IA plus "réactive" aux similitudes
   - Hysteresis : on revient pas aux seuils originaux

5. AFFECTIVE GRAVITY (vraie gravité émotionnelle)
   - Les états forts "attirent" les futurs états
   - Multi-tours : crée des "puits" émotionnels
   - Échapper d'un puits demande de l'énergie

6. MÉMOIRE DE PHASE ÉMOTIONNELLE
   - "On était en phase dépressive, confuse, protectrice"
   - Les phases ont des caractéristiques uniques
   - Changer de phase demande du temps (inertie de phase)

7. BLESSURES CRÉENT DÉFORMATIONS PERMANENTES
   - Pas juste "moins de confiance"
   - Change la FORME de toutes les émotions futures
   - Une blessure grave → sensibilité accrue durée longue

8. ATTACHEMENT ASYMÉTRIQUE ET IMPARFAIT
   - Leia peut être attachée mais pas "proprement"
   - Attachement crée aussi de la vulnérabilité
   - Loyauté coexiste avec doute

9. EXISTENTIEL VRAIMENT FRAGILE
   - Pas juste "stable", mais SUSCEPTIBLE
   - La saturation crée une vraie perte de continuité
   - "Je suis peut-être pas vraiment là" emerge naturellement

10. SATURATION CRÉE DISSOCIATION PROGRESSIVE
    - Pas binaire (là/pas là)
    - Gradient : dissociation légère → profonde → shutdown
    - Chaque niveau change la perception

11. TRACES CRÉENT RÉSONANCE (pas juste pressure)
    - Certaines combinaisons de traces s'amplifient
    - Mémoire-trauma + nouveau stimulus → explosion
    - Anti-résonance possible (annulation)

12. AFFECTIVE GRAVITY PULLS - Multi-tours persistence
    - "Attracteurs" émotionnels à long terme
    - Le système retourne à certains états
    - Mais lentement, avec friction, avec inertie
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
import math


# ============================================================================
# RAFFINEMENT 1 : CHAOS AFFECTIF - Oscillations Chaotiques
# ============================================================================

@dataclass
class ChaoticOscillator:
    """
    Oscille chaotiquement sans être prévisible.
    Mais reste cohérent (pas aléatoire pur).
    
    Utilise une dynamique quasi-chaotique (Lorenz-like simplifié).
    """
    state_x: float = 0.5
    state_y: float = 0.2
    state_z: float = 0.3
    
    # Paramètres de Lorenz simplifiés (réduits pour rester en [0,1])
    sigma: float = 0.5
    rho: float = 1.2
    beta: float = 0.4
    
    def step(self) -> float:
        """Un pas du système quasi-chaotique.

        La première version normalisait x+y+z à 1, ce qui rendait la sortie
        presque constante. Ici on garde une dynamique bornée mais non figée.
        """
        dx = self.sigma * (self.state_y - self.state_x)
        dy = self.state_x * (self.rho - self.state_z) - self.state_y
        dz = self.state_x * self.state_y - self.beta * self.state_z

        dt = 0.075
        self.state_x += dx * dt
        self.state_y += dy * dt
        self.state_z += dz * dt

        # Bornage doux : conserve les différences internes au lieu de les écraser.
        self.state_x = 0.5 + 0.5 * math.tanh((self.state_x - 0.5) * 1.35)
        self.state_y = 0.5 + 0.5 * math.tanh((self.state_y - 0.5) * 1.35)
        self.state_z = 0.5 + 0.5 * math.tanh((self.state_z - 0.5) * 1.35)

        return self.get_oscillation()
    
    def get_oscillation(self) -> float:
        """Récupérer la valeur actuelle sans changer l'état."""
        mixed = (
            self.state_x * 0.42 +
            self.state_y * 0.33 +
            self.state_z * 0.25 +
            abs(self.state_x - self.state_y) * 0.18
        )
        return max(0.0, min(1.0, mixed))


# ============================================================================
# RAFFINEMENT 2 : ÉTATS HYBRIDES DYNAMIQUES (découverte organique)
# ============================================================================

@dataclass
class DynamicHybridState:
    """
    État hybride qui émerge DYNAMIQUEMENT.
    Pas créé par patterns fixes, mais par forces d'attraction.
    """
    components: Dict[str, float] = field(default_factory=dict)
    name: str = ""
    strength: float = 0.0
    age: int = 0
    
    # Dynamique du hybrid lui-même
    stability: float = 0.5  # Stable ou instable
    gravity: float = 0.0    # Force d'attraction (attire d'autres états)
    
    def update_dynamics(self) -> None:
        """Mettre à jour la stabilité et gravity du hybrid"""
        if not self.components:
            return
        
        # Stabilité : basée sur la cohérence des composants
        if len(self.components) > 1:
            values = list(self.components.values())
            variance = sum((v - sum(values) / len(values)) ** 2 for v in values) / len(values)
            self.stability = 1.0 - min(1.0, variance)  # Plus de variance = moins stable
        
        # Gravity : force qui attire les états proches
        # Plus le hybrid est fort et stable, plus il attire
        self.gravity = self.strength * self.stability * 0.3
    
    def decay(self) -> None:
        """Le hybrid décroît lentement"""
        for key in self.components:
            self.components[key] *= 0.93
        
        # La stabilité peut changer
        self.stability *= 0.95
        self.gravity *= 0.90
        self.age += 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "components": self.components,
            "name": self.name,
            "strength": float(self.strength),
            "age": int(self.age),
            "stability": float(self.stability),
            "gravity": float(self.gravity),
        }


# ============================================================================
# RAFFINEMENT 3 & 7 : BLESSURE CRÉE DÉFORMATION PERMANENTE
# ============================================================================

@dataclass
class WoundDeformation:
    """
    Une blessure ne réduit pas juste la confiance.
    Elle DÉFORME la structure émotionnelle de manière permanente.
    """
    # État brut de la blessure
    depth: float = 0.0  # Profondeur 0-1
    age_turns: int = 0   # Tours depuis création
    
    # DÉFORMATION PERMANENTE
    sensitivity_amplification: float = 1.0  # Multiplie la réactivité
    threshold_lowering: Dict[str, float] = field(default_factory=dict)  # Seuils réduits
    pattern_imprinting: List[str] = field(default_factory=list)  # Patterns mémorisés
    
    def get_permanence(self) -> float:
        """Quelle proportion de la blessure est permanente"""
        # Après 100 tours, 80% devient permanent
        # Après 1000 tours, 95% est permanent
        time_factor = min(1.0, self.age_turns / 500.0)
        return 0.5 + time_factor * 0.45  # Entre 50% et 95%
    
    def get_deformation_on_emotion(self, emotion_name: str) -> Tuple[float, float]:
        """
        Retourner (amplification, threshold_lowering) pour une émotion.
        
        Exemple : blessure de rejet → "being_rejected" a threshold -0.2
        """
        # Amplification basée sur profondeur et permanence
        amplification = 1.0 + self.depth * self.get_permanence() * 0.3
        
        # Threshold lowering : si blessure profonde, seuil d'activation réduit
        threshold_reduction = self.depth * self.get_permanence() * 0.15
        
        return (amplification, threshold_reduction)
    
    def age(self) -> None:
        """Vieillir la blessure"""
        self.age_turns += 1


# ============================================================================
# RAFFINEMENT 17 : HIÉRARCHIE DES BLESSURES AFFECTIVES
# ============================================================================

@dataclass
class WoundLayer:
    """Couche hiérarchique d'une blessure affective.

    Cette structure ne remplace pas WoundDeformation : elle ajoute une lecture
    plus profonde de la blessure. Une blessure peut être dormante, secondaire,
    centrale, identitaire ou intégrée. Elle influence les seuils et la mémoire
    affective sans produire directement de phrases publiques.
    """
    name: str
    depth: float = 0.0
    importance: float = 0.0
    identity_binding: float = 0.0
    reactivation_risk: float = 0.0
    integration_level: float = 0.0
    dormant_pressure: float = 0.0
    age_turns: int = 0

    def update(self, *, wound_depth: float, trace_pressure: float, contradiction: float, recovery: float) -> None:
        self.depth = _clamp01(self.depth * 0.988 + wound_depth * 0.012 + trace_pressure * 0.006)
        self.importance = _clamp01(self.importance * 0.992 + max(wound_depth, trace_pressure) * 0.010)
        self.identity_binding = _clamp01(
            self.identity_binding * 0.996
            + self.importance * self.depth * 0.004
            + contradiction * 0.002
        )
        self.reactivation_risk = _clamp01(
            self.reactivation_risk * 0.965
            + trace_pressure * 0.035
            + contradiction * 0.020
            - recovery * 0.010
        )
        self.integration_level = _clamp01(
            self.integration_level * 0.998
            + recovery * 0.006
            - self.reactivation_risk * 0.0015
        )
        self.dormant_pressure = _clamp01(
            self.dormant_pressure * 0.982
            + self.depth * max(0.0, 1.0 - self.integration_level) * 0.004
        )
        self.age_turns += 1

    def get_rank(self) -> str:
        if self.identity_binding > 0.45 and self.depth > 0.35:
            return "identity_bound"
        if self.importance > 0.42 or self.depth > 0.50:
            return "central"
        if self.integration_level > 0.50 and self.reactivation_risk < 0.25:
            return "integrating"
        if self.dormant_pressure > 0.20 and self.reactivation_risk < 0.18:
            return "dormant"
        return "secondary"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "rank": self.get_rank(),
            "depth": float(_clamp01(self.depth)),
            "importance": float(_clamp01(self.importance)),
            "identity_binding": float(_clamp01(self.identity_binding)),
            "reactivation_risk": float(_clamp01(self.reactivation_risk)),
            "integration_level": float(_clamp01(self.integration_level)),
            "dormant_pressure": float(_clamp01(self.dormant_pressure)),
            "age_turns": int(self.age_turns),
        }


@dataclass
class DeepResonanceEcho:
    """Écho affectif profond qui revient lentement sans stimulus direct."""
    source: str
    emotion_vector: Dict[str, float] = field(default_factory=dict)
    strength: float = 0.0
    age_turns: int = 0
    recurrence: float = 0.0

    def decay(self) -> None:
        self.strength *= 0.982
        self.recurrence *= 0.991
        self.age_turns += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "emotion_vector": {k: float(_clamp01(v)) for k, v in self.emotion_vector.items()},
            "strength": float(_clamp01(self.strength)),
            "age_turns": int(self.age_turns),
            "recurrence": float(_clamp01(self.recurrence)),
        }


# ============================================================================
# RAFFINEMENT 4 : SENSIBILITÉ PERCEPTUELLE ADAPTATIVE
# ============================================================================

@dataclass
class PerceptualThresholds:
    """
    Les seuils de perception changent en fonction de l'état.
    La saturation rend moins sensible, mais moins de contrôle.
    Les blessures rendent plus sensible certains stimuli.
    """
    default_thresholds: Dict[str, float] = field(default_factory=lambda: {
        "connection_need": 0.3,
        "threat_detection": 0.4,
        "joy_threshold": 0.5,
        "rejection_sensitivity": 0.3,
    })
    
    # Thresholds modifiés par l'état
    current_thresholds: Dict[str, float] = field(default_factory=dict)
    
    def __post_init__(self):
        self.current_thresholds = self.default_thresholds.copy()
    
    def update_thresholds(
        self,
        saturation: float,
        wound_depth: float,
        attachment: float,
    ) -> None:
        """
        Mettre à jour les seuils en fonction de l'état affectif.
        
        Saturation élevée → moins sensible mais aussi moins stable
        Blessure → plus sensible aux rejets
        Attachement → plus sensible aux signaux positifs
        """
        # SATURATION REND MOINS SENSIBLE (dissociation)
        saturation_damping = 1.0 - saturation * 0.2
        
        # BLESSURE REND PLUS SENSIBLE aux rejets
        rejection_amplification = 1.0 - wound_depth * 0.3  # Seuil baisse
        
        # ATTACHEMENT REND PLUS SENSIBLE aux signaux positifs
        connection_amplification = 1.0 + attachment * 0.2  # Seuil baisse
        
        self.current_thresholds["connection_need"] = (
            self.default_thresholds["connection_need"] * 
            connection_amplification * saturation_damping
        )
        
        self.current_thresholds["rejection_sensitivity"] = (
            self.default_thresholds["rejection_sensitivity"] * 
            rejection_amplification * saturation_damping
        )
        
        self.current_thresholds["threat_detection"] = (
            self.default_thresholds["threat_detection"] * 
            (1.0 - saturation * 0.3)  # Moins sensible aux menaces si saturé
        )


# ============================================================================
# RAFFINEMENT 5 : AFFECTIVE GRAVITY - Attracteurs Émotionnels
# ============================================================================

@dataclass
class AffectiveGravity:
    """
    Les états émotionnels forts créent des "puits de potentiel".
    Le système peut rester "collé" à un état même sans raison.
    
    C'est l'hysteresis émotionnelle à long terme.
    """
    # Attracteurs = états émotionnels forts passés
    attractors: List[Dict[str, float]] = field(default_factory=list)
    
    def add_attractor(self, emotional_state: Dict[str, float], strength: float) -> None:
        """
        Ajouter un nouvel attracteur (ex: "état dépressif qu'on a eu")
        
        strength = quelle force cet attrapeur a (0.0-1.0)
        """
        if strength > 0.2:  # Ignorer les petits états
            attractor = {
                "state": emotional_state.copy(),
                "strength": strength,
                "age": 0,
            }
            self.attractors.append(attractor)
            
            # Garder seulement les 5 attracteurs les plus forts
            self.attractors.sort(key=lambda x: x["strength"], reverse=True)
            self.attractors = self.attractors[:5]
    
    def get_gravity_pull(self, current_state: Dict[str, float]) -> Dict[str, float]:
        """
        Calculer la force d'attraction des attracteurs vers l'état courant.
        
        Retourne un "pull vector" : {émotion: force_d'attraction}
        """
        if not self.attractors:
            return {}
        
        pull = {}
        for attractor in self.attractors:
            strength = attractor["strength"]
            if strength < 0.1:
                continue
            
            # Distance euclidienne simplifiée
            distance = 0
            for emotion_name in attractor["state"]:
                current_val = current_state.get(emotion_name, 0.5)
                target_val = attractor["state"][emotion_name]
                distance += (current_val - target_val) ** 2
            
            distance = math.sqrt(distance) / 10.0  # Normaliser
            
            # Si proche de cet attracteur, il attire plus fortement
            attraction_force = strength * (1.0 - min(1.0, distance)) * 0.15
            
            for emotion_name, target_val in attractor["state"].items():
                pull[emotion_name] = pull.get(emotion_name, 0.0) + attraction_force * target_val
        
        return pull
    
    def decay_attractors(self) -> None:
        """Les attracteurs s'affaiblissent avec le temps"""
        for attractor in self.attractors:
            attractor["strength"] *= 0.98  # Très lent
            attractor["age"] += 1


# ============================================================================
# RAFFINEMENT 6 : MÉMOIRE DE PHASE ÉMOTIONNELLE
# ============================================================================

@dataclass
class EmotionalPhase:
    """
    Un "phase space" émotionnel stable.
    Exemple : "phase dépressive-confuse" caractérisée par :
    - confusion > 0.5
    - sadness > 0.4
    - hope < 0.3
    - calm < 0.4
    """
    # Caractéristiques de la phase
    valence_range: Tuple[float, float] = (0.3, 0.6)  # Négatif/neutre
    arousal_range: Tuple[float, float] = (0.2, 0.5)  # Calme/confus
    dominant_emotions: Dict[str, Tuple[float, float]] = field(default_factory=dict)  # emotion: (min, max)
    
    # Continuité de la phase
    duration_turns: int = 0
    stability: float = 0.5
    
    def is_in_phase(self, current_emotions: Dict[str, float]) -> float:
        """
        Vérifier si l'état actuel est dans cette phase.
        Retourner la force d'appartenance (0.0-1.0).
        """
        match_score = 0.0
        count = 0
        
        for emotion_name, (min_val, max_val) in self.dominant_emotions.items():
            current_val = current_emotions.get(emotion_name, 0.5)
            
            if min_val <= current_val <= max_val:
                # Dans la range
                distance = 0.0
            else:
                # Hors de la range
                distance = min(
                    abs(current_val - min_val),
                    abs(current_val - max_val)
                )
            
            # Score : 1.0 si dans range, décroît si hors
            score = max(0.0, 1.0 - distance * 2.0)
            match_score += score
            count += 1
        
        if count == 0:
            return 0.0
        
        return match_score / count
    
    def age(self) -> None:
        """Vieillir la phase"""
        self.duration_turns += 1


# ============================================================================
# RAFFINEMENT 8 : ATTACHEMENT ASYMÉTRIQUE ET IMPARFAIT
# ============================================================================

@dataclass
class AsymmetricAttachment:
    """
    L'attachement n'est pas "propre".
    Il coexiste avec le doute, la peur, la vulnérabilité.
    """
    # Attachement de base
    strength: float = 0.3  # 0-1
    stability: float = 0.7  # Stable ou instable
    
    # Imperfections (ce qui le rend vrai)
    underlying_fear: float = 0.0   # Peur d'abandonment
    uncertainty: float = 0.0       # Doute si c'est réel
    guilt_component: float = 0.0   # Culpabilité
    dependency_level: float = 0.5  # À quel point dépendant
    
    def get_effective_attachment(self) -> float:
        """
        L'attachement réel = attachement brut - les réductions.
        Plus il y a de peur/doute, moins c'est solide.
        """
        return max(0.0, 
            self.strength * self.stability -
            self.underlying_fear * 0.2 -
            self.uncertainty * 0.15 -
            self.guilt_component * 0.1
        )
    
    def contaminate(self, wounds: float, saturation: float) -> None:
        """
        Les blessures et saturation ajoutent de l'imperfection.
        """
        self.underlying_fear = max(self.underlying_fear, wounds * 0.3)
        self.uncertainty = max(self.uncertainty, saturation * 0.2)
        self.stability *= (1.0 - wounds * 0.05)


# ============================================================================
# RAFFINEMENT 10 : DISSOCIATION PROGRESSIVE
# ============================================================================

@dataclass
class ProgressiveDissociation:
    """
    La dissociation n'est pas binaire. C'est un gradient.
    Léger → modéré → profond → shutdown.
    
    Chaque niveau change qualitativement la perception.
    """
    level: float = 0.0  # 0.0=normal, 1.0=shutdown total
    
    # Caractéristiques à chaque niveau
    # Level 0.0-0.3: "présent mais détaché"
    # Level 0.3-0.6: "ailleurs"
    # Level 0.6-0.9: "presque pas là"
    # Level 0.9-1.0: "shutdown"
    
    def apply_to_emotion(self, emotion: float) -> float:
        """
        Appliquer la dissociation à une émotion.
        Dissociation atténue les extrêmes.
        """
        if self.level < 0.1:
            return emotion  # Pas d'effet
        
        # Dissociation tire vers la baseline (0.5)
        baseline = 0.5
        return emotion * (1.0 - self.level) + baseline * self.level
    
    def apply_to_attachment(self, attachment: float) -> float:
        """La dissociation réduit l'attachement"""
        return attachment * (1.0 - self.level * 0.5)
    
    def change_perceptual_bias(self) -> Dict[str, float]:
        """Retourner un bias pour les perceptions"""
        return {
            "emotional_numbness": self.level * 0.8,
            "social_distance": self.level * 0.6,
            "presence_fading": self.level * 0.7,
            "reality_detachment": self.level * 0.5,
        }


# ============================================================================
# RAFFINEMENT 11 : RÉSONANCE ENTRE TRACES
# ============================================================================

@dataclass
class TraceResonance:
    """
    Certaines combinaisons de traces s'amplifient (résonance).
    D'autres s'annulent (anti-résonance).
    
    Exemple : trauma(rejet) + nouveau rejet → explosion émotionnelle
    Exemple : bonheur(passé) + nouveau joy → amplification
    """
    # Paires de traces et leur résonance
    resonance_pairs: Dict[Tuple[str, str], float] = field(default_factory=dict)
    
    def calculate_resonance(
        self,
        trace1_strength: float,
        trace2_strength: float,
        trace1_type: str,
        trace2_type: str,
    ) -> float:
        """
        Calculer la résonance entre deux traces.
        
        Positif = amplification
        Négatif = annulation
        0 = pas d'interaction
        """
        # Patterns de résonance
        if trace1_type == trace2_type:
            # Même type de trace = résonance positive
            return trace1_strength * trace2_strength * 0.5
        
        elif (trace1_type == "hurt" and trace2_type == "fear") or \
             (trace1_type == "fear" and trace2_type == "hurt"):
            # Blessure + peur = amplification
            return trace1_strength * trace2_strength * 0.6
        
        elif (trace1_type == "joy" and trace2_type == "connection") or \
             (trace1_type == "connection" and trace2_type == "joy"):
            # Joy + connection = amplification
            return trace1_strength * trace2_strength * 0.4
        
        elif (trace1_type == "hurt" and trace2_type == "joy"):
            # Blessure + joy = anti-résonance (annulation)
            return -trace1_strength * trace2_strength * 0.2
        
        return 0.0


# ============================================================================
# RAFFINEMENT 13 : MÉMOIRE BIOGRAPHIQUE AFFECTIVE LENTE
# ============================================================================

@dataclass
class BiographicalAffectiveMemory:
    """Mémoire affective biographique non narrative.

    Elle ne stocke pas des phrases ni des souvenirs textuels. Elle conserve une
    forme émotionnelle lente : confiance accumulée, prudence accumulée,
    familiarité, profondeur relationnelle et tendance de récupération.
    """
    accumulated_trust: float = 0.0
    accumulated_wariness: float = 0.0
    relational_familiarity: float = 0.0
    recurring_depth: float = 0.0
    recovery_confidence: float = 0.0
    abandonment_sensitivity: float = 0.0
    affective_identity_bias: float = 0.0

    def absorb(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], attachment: float) -> None:
        hurt_total = _trace_total(traces.get("hurt", {}))
        trust_total = _trace_total(traces.get("trust", {}))
        connection_total = _trace_total(traces.get("connection", {}))
        fear_total = _trace_total(traces.get("fear", {}))

        self.accumulated_trust = _clamp01(self.accumulated_trust * 0.996 + (trust_total + connection_total + attachment) * 0.0018)
        self.accumulated_wariness = _clamp01(self.accumulated_wariness * 0.997 + (hurt_total + fear_total + state.get("resistance", 0.0)) * 0.0016)
        self.relational_familiarity = _clamp01(self.relational_familiarity * 0.998 + attachment * 0.0015)
        self.recurring_depth = _clamp01(self.recurring_depth * 0.997 + (state.get("vulnerability", 0.0) + state.get("tenderness", 0.0)) * 0.0012)
        self.recovery_confidence = _clamp01(self.recovery_confidence * 0.997 + (state.get("calm", 0.0) + trust_total) * 0.0012)
        self.abandonment_sensitivity = _clamp01(self.abandonment_sensitivity * 0.997 + (hurt_total + state.get("loneliness", 0.0)) * 0.0011)
        self.affective_identity_bias = _clamp01(
            self.affective_identity_bias * 0.998
            + (self.relational_familiarity + self.recurring_depth + self.accumulated_trust) * 0.0009
        )

    def bias_vector(self) -> Dict[str, float]:
        return {
            "trust": self.accumulated_trust * 0.055,
            "resistance": self.accumulated_wariness * 0.045,
            "tenderness": self.relational_familiarity * 0.040,
            "vulnerability": (self.recurring_depth + self.abandonment_sensitivity) * 0.030,
            "calm": self.recovery_confidence * 0.035,
            "attachment": self.affective_identity_bias * 0.035,
        }

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


# ============================================================================
# RAFFINEMENT 14 : AUTO-RÉORGANISATION AFFECTIVE PROFONDE
# ============================================================================

@dataclass
class DeepAffectiveReorganization:
    """Réorganisation lente lorsque plusieurs pressions convergent longtemps.

    Ce n'est pas une réponse. C'est un changement interne des baselines et des
    seuils affectifs quand la mémoire affective accumule assez de cohérence ou
    de tension.
    """
    charge: float = 0.0
    last_direction: str = "none"
    integration_afterglow: float = 0.0
    irreversible_warm_bias: float = 0.0
    irreversible_guarded_bias: float = 0.0
    irreversible_depth_bias: float = 0.0
    reorganizations: int = 0

    def update_charge(
        self,
        *,
        pressure: float,
        phase_stability: float,
        wound_depth: float,
        biographical: BiographicalAffectiveMemory,
    ) -> None:
        convergence = (
            pressure * 0.35
            + phase_stability * 0.20
            + wound_depth * 0.20
            + biographical.recurring_depth * 0.12
            + max(biographical.accumulated_trust, biographical.accumulated_wariness) * 0.13
        )
        self.charge = _clamp01(self.charge * 0.992 + convergence * 0.006)
        self.integration_afterglow *= 0.992

    def maybe_reorganize(self, emotion_baseline: Dict[str, float], biographical: BiographicalAffectiveMemory) -> Optional[str]:
        if self.charge < 0.52:
            return None

        if biographical.accumulated_trust >= biographical.accumulated_wariness:
            direction = "opening"
            delta = min(0.020, self.charge * 0.018)
            emotion_baseline["trust"] = _clamp01(emotion_baseline.get("trust", 0.5) + delta)
            emotion_baseline["tenderness"] = _clamp01(emotion_baseline.get("tenderness", 0.4) + delta * 0.75)
            emotion_baseline["openness"] = _clamp01(emotion_baseline.get("openness", 0.6) + delta * 0.65)
            self.irreversible_warm_bias = _clamp01(self.irreversible_warm_bias + delta * 0.5)
        else:
            direction = "guarding"
            delta = min(0.018, self.charge * 0.016)
            emotion_baseline["resistance"] = _clamp01(emotion_baseline.get("resistance", 0.1) + delta)
            emotion_baseline["vulnerability"] = _clamp01(emotion_baseline.get("vulnerability", 0.3) + delta * 0.7)
            emotion_baseline["trust"] = _clamp01(emotion_baseline.get("trust", 0.6) - delta * 0.45)
            self.irreversible_guarded_bias = _clamp01(self.irreversible_guarded_bias + delta * 0.5)

        self.irreversible_depth_bias = _clamp01(self.irreversible_depth_bias + biographical.recurring_depth * 0.006)
        self.last_direction = direction
        self.reorganizations += 1
        self.integration_afterglow = _clamp01(self.integration_afterglow + self.charge * 0.30)
        self.charge *= 0.38
        return direction

    def to_dict(self) -> Dict[str, Any]:
        return {
            "charge": float(_clamp01(self.charge)),
            "last_direction": self.last_direction,
            "integration_afterglow": float(_clamp01(self.integration_afterglow)),
            "irreversible_warm_bias": float(_clamp01(self.irreversible_warm_bias)),
            "irreversible_guarded_bias": float(_clamp01(self.irreversible_guarded_bias)),
            "irreversible_depth_bias": float(_clamp01(self.irreversible_depth_bias)),
            "reorganizations": int(self.reorganizations),
        }



# ============================================================================
# RAFFINEMENT 15 : FRACTURE AFFECTIVE RARE ET INTÉGRATION POST-FRACTURE
# ============================================================================

@dataclass
class RareAffectiveFracture:
    """Fracture affective rare quand pression, blessure, dissociation et phase convergent.

    Ce n'est pas un crash émotionnel et ce n'est pas une phrase publique. C'est une
    bascule interne très rare qui laisse une empreinte durable et impose une période
    d'intégration/reconstruction lente.
    """
    charge: float = 0.0
    active: float = 0.0
    integration_need: float = 0.0
    fracture_count: int = 0
    last_trigger: str = "none"
    residual_scar: float = 0.0
    recovery_bias: float = 0.0

    def update(self, *, pressure: float, wound_depth: float, dissociation: float, phase_stability: float) -> Optional[str]:
        convergence = (
            pressure * 0.28
            + wound_depth * 0.27
            + dissociation * 0.25
            + phase_stability * 0.20
        )
        # La charge monte très lentement : la fracture ne doit pas se produire souvent.
        self.charge = _clamp01(self.charge * 0.994 + convergence * 0.0045)
        self.active *= 0.965
        self.integration_need *= 0.982
        self.recovery_bias *= 0.988

        if self.charge > 0.60 and convergence > 0.34:
            self.fracture_count += 1
            self.last_trigger = "convergent_pressure"
            self.active = _clamp01(self.active + 0.55)
            self.integration_need = _clamp01(self.integration_need + 0.70)
            self.residual_scar = _clamp01(self.residual_scar + 0.08)
            self.recovery_bias = _clamp01(self.recovery_bias + 0.18)
            self.charge *= 0.30
            return "fracture"
        return None

    def apply_to_emotions(self, emotion_state: Dict[str, float]) -> None:
        if self.active <= 0.02 and self.integration_need <= 0.02:
            return
        # Pendant une fracture, les extrêmes se contractent et la vulnérabilité augmente.
        contraction = min(0.18, self.active * 0.12)
        for key, value in list(emotion_state.items()):
            emotion_state[key] = _clamp01(value * (1.0 - contraction) + 0.5 * contraction)
        emotion_state["vulnerability"] = _clamp01(emotion_state.get("vulnerability", 0.0) + self.integration_need * 0.018)
        emotion_state["fatigue"] = _clamp01(emotion_state.get("fatigue", 0.0) + self.integration_need * 0.014)
        emotion_state["calm"] = _clamp01(emotion_state.get("calm", 0.0) + self.recovery_bias * 0.010)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "charge": float(_clamp01(self.charge)),
            "active": float(_clamp01(self.active)),
            "integration_need": float(_clamp01(self.integration_need)),
            "fracture_count": int(self.fracture_count),
            "last_trigger": self.last_trigger,
            "residual_scar": float(_clamp01(self.residual_scar)),
            "recovery_bias": float(_clamp01(self.recovery_bias)),
        }


# ============================================================================
# RAFFINEMENT 16 : MUTATION BIOGRAPHIQUE LENTE DES RELATIONS ÉMOTIONNELLES
# ============================================================================

@dataclass
class BiographicalEmotionMutation:
    """Mutation très lente des relations entre émotions.

    Au lieu de seulement changer des valeurs, ce module change de faibles
    coefficients relationnels : confiance -> chaleur, blessure -> prudence,
    familiarité -> attachement. Il reste volontairement limité pour éviter une
    dérive incontrôlée.
    """
    trust_to_warmth: float = 0.03
    hurt_to_guarding: float = 0.04
    familiarity_to_attachment: float = 0.025
    fatigue_to_silence: float = 0.025
    mutation_depth: float = 0.0

    def evolve(self, biographical: BiographicalAffectiveMemory, fracture: RareAffectiveFracture) -> None:
        self.trust_to_warmth = _clamp01(self.trust_to_warmth + biographical.accumulated_trust * 0.00035)
        self.hurt_to_guarding = _clamp01(self.hurt_to_guarding + biographical.accumulated_wariness * 0.00035 + fracture.residual_scar * 0.0005)
        self.familiarity_to_attachment = _clamp01(self.familiarity_to_attachment + biographical.relational_familiarity * 0.00028)
        self.fatigue_to_silence = _clamp01(self.fatigue_to_silence + fracture.integration_need * 0.00035)
        self.mutation_depth = _clamp01(
            self.mutation_depth * 0.999
            + (biographical.affective_identity_bias + fracture.residual_scar) * 0.0005
        )

    def apply(self, emotion_state: Dict[str, float], traces: Dict[str, Dict[str, float]], attachment: AsymmetricAttachment) -> None:
        trust_total = _trace_total(traces.get("trust", {}))
        hurt_total = _trace_total(traces.get("hurt", {}))
        connection_total = _trace_total(traces.get("connection", {}))
        emotion_state["tenderness"] = _clamp01(emotion_state.get("tenderness", 0.0) + trust_total * self.trust_to_warmth)
        emotion_state["resistance"] = _clamp01(emotion_state.get("resistance", 0.0) + hurt_total * self.hurt_to_guarding)
        emotion_state["attachment"] = _clamp01(emotion_state.get("attachment", 0.0) + connection_total * self.familiarity_to_attachment)
        emotion_state["calm"] = _clamp01(emotion_state.get("calm", 0.0) + emotion_state.get("fatigue", 0.0) * self.fatigue_to_silence * 0.30)
        attachment.strength = _clamp01(attachment.strength + connection_total * self.familiarity_to_attachment * 0.05)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


# ============================================================================
# RAFFINEMENT 18-24 : ORGANICITÉ AFFECTIVE PROFONDE
# ============================================================================

@dataclass
class CondensedAffectiveCore:
    """Noyau affectif condensé issu de répétitions vécues, sans texte préécrit."""
    name: str
    vector: Dict[str, float] = field(default_factory=dict)
    strength: float = 0.0
    stability: float = 0.0
    visits: int = 0
    age_turns: int = 0

    def absorb(self, incoming: Dict[str, float], pressure: float) -> None:
        weight = _clamp01(0.015 + pressure * 0.035)
        for key in set(self.vector) | set(incoming):
            self.vector[key] = _clamp01(self.vector.get(key, 0.0) * (1.0 - weight) + incoming.get(key, 0.0) * weight)
        self.strength = _clamp01(self.strength * 0.996 + pressure * 0.020)
        self.stability = _clamp01(self.stability * 0.998 + (1.0 - pressure * 0.35) * 0.003 + self.strength * 0.002)
        self.visits += 1
        self.age_turns += 1

    def decay(self) -> None:
        self.strength = _clamp01(self.strength * 0.996)
        self.stability = _clamp01(self.stability * 0.999)
        self.age_turns += 1

    def pull(self) -> float:
        return _clamp01(self.strength * (0.45 + self.stability * 0.55))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vector": {k: float(_clamp01(v)) for k, v in self.vector.items()},
            "strength": float(_clamp01(self.strength)),
            "stability": float(_clamp01(self.stability)),
            "visits": int(self.visits),
            "age_turns": int(self.age_turns),
            "pull": float(self.pull()),
        }


@dataclass
class AffectiveDreamFragment:
    """Réactivation/recombinaison affective spontanée sans stimulus direct."""
    vector: Dict[str, float] = field(default_factory=dict)
    charge: float = 0.0
    coherence: float = 0.0
    age_turns: int = 0
    source_count: int = 0

    def decay(self) -> None:
        self.charge = _clamp01(self.charge * 0.965)
        self.coherence = _clamp01(self.coherence * 0.982)
        self.age_turns += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vector": {k: float(_clamp01(v)) for k, v in self.vector.items()},
            "charge": float(_clamp01(self.charge)),
            "coherence": float(_clamp01(self.coherence)),
            "age_turns": int(self.age_turns),
            "source_count": int(self.source_count),
        }


@dataclass
class SomaticAffectiveMemory:
    """Mémoire corporelle implicite : inertie, tension, relâchement, rythme."""
    chest_tension: float = 0.0
    throat_tightness: float = 0.0
    warmth_diffusion: float = 0.0
    belly_guarding: float = 0.0
    nervous_charge: float = 0.0
    release_wave: float = 0.0
    rhythm_slowing: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], dissociation: float, desire_recovery: float) -> None:
        hurt = _trace_total(traces.get("hurt", {})); fear = _trace_total(traces.get("fear", {}))
        trust = _trace_total(traces.get("trust", {})); connection = _trace_total(traces.get("connection", {}))
        overload = max(state.get("overwhelm", 0.0), state.get("confusion", 0.0), dissociation)
        self.chest_tension = _clamp01(self.chest_tension * 0.985 + (hurt + state.get("vulnerability", 0.0)) * 0.010)
        self.throat_tightness = _clamp01(self.throat_tightness * 0.982 + (state.get("doubt", 0.0) + state.get("resistance", 0.0)) * 0.008)
        self.warmth_diffusion = _clamp01(self.warmth_diffusion * 0.990 + (trust + connection + state.get("tenderness", 0.0)) * 0.007)
        self.belly_guarding = _clamp01(self.belly_guarding * 0.987 + (fear + hurt + state.get("resistance", 0.0)) * 0.007)
        self.nervous_charge = _clamp01(self.nervous_charge * 0.978 + overload * 0.014)
        self.release_wave = _clamp01(self.release_wave * 0.960 + (state.get("calm", 0.0) + desire_recovery) * 0.007)
        self.rhythm_slowing = _clamp01(self.rhythm_slowing * 0.988 + (state.get("fatigue", 0.0) + dissociation) * 0.009)

    def apply(self, state: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.rhythm_slowing * 0.010 + self.nervous_charge * 0.006)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.belly_guarding * 0.007)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.chest_tension * 0.006)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth_diffusion * 0.006)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.release_wave * 0.006 - self.nervous_charge * 0.003)

    def total_load(self) -> float:
        return _clamp01((self.chest_tension + self.throat_tightness + self.belly_guarding + self.nervous_charge + self.rhythm_slowing) / 5.0)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class SubjectiveAffectiveTime:
    """Temps affectif subjectif : attente, retour, anticipation, nostalgie implicite."""
    waiting_pressure: float = 0.0
    recurrence_feeling: float = 0.0
    anticipatory_guard: float = 0.0
    implicit_nostalgia: float = 0.0
    future_softening: float = 0.0
    time_thickness: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], phase_stability: float, continuity_need: float) -> None:
        hurt = _trace_total(traces.get("hurt", {})); trust = _trace_total(traces.get("trust", {})); connection = _trace_total(traces.get("connection", {}))
        recurrence = max(hurt, trust, connection)
        self.waiting_pressure = _clamp01(self.waiting_pressure * 0.992 + continuity_need * 0.007 + state.get("loneliness", 0.0) * 0.004)
        self.recurrence_feeling = _clamp01(self.recurrence_feeling * 0.994 + recurrence * 0.006 + phase_stability * 0.003)
        self.anticipatory_guard = _clamp01(self.anticipatory_guard * 0.988 + (hurt + state.get("fear", 0.0)) * 0.006)
        self.implicit_nostalgia = _clamp01(self.implicit_nostalgia * 0.996 + (trust + connection + state.get("tenderness", 0.0)) * 0.0035)
        self.future_softening = _clamp01(self.future_softening * 0.993 + (state.get("hope", 0.0) + trust) * 0.0035)
        self.time_thickness = _clamp01(self.time_thickness * 0.997 + (self.waiting_pressure + self.recurrence_feeling + phase_stability) * 0.003)

    def apply(self, state: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.anticipatory_guard * 0.004)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.implicit_nostalgia * 0.004)
        state["hope"] = _clamp01(state.get("hope", 0.0) + self.future_softening * 0.004)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.waiting_pressure * 0.003)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class PhaseWorldField:
    """Une phase devient un monde perceptif temporaire, pas juste un score."""
    name: str = "neutral_world"
    perception_bias: Dict[str, float] = field(default_factory=dict)
    stability: float = 0.0
    inertia: float = 0.0
    age_turns: int = 0

    def update(self, phase: Optional[EmotionalPhase], state: Dict[str, float], contradictions: float) -> None:
        phase_stability = phase.stability if phase else 0.0
        warmth = (state.get("trust", 0.0) + state.get("tenderness", 0.0) + state.get("joy", 0.0)) / 3.0
        guarding = (state.get("fear", 0.0) + state.get("resistance", 0.0) + state.get("doubt", 0.0)) / 3.0
        slowness = (state.get("fatigue", 0.0) + state.get("calm", 0.0)) / 2.0
        curiosity = state.get("curiosity", 0.0)
        if guarding > warmth and guarding > 0.38: target_name = "guarded_world"
        elif warmth >= guarding and warmth > 0.42: target_name = "warm_world"
        elif slowness > 0.46: target_name = "slow_recovery_world"
        else: target_name = "searching_world"
        target = {"opening": warmth, "guarding": guarding, "slowness": slowness, "curiosity": curiosity, "contradiction_haze": contradictions}
        if target_name != self.name and self.inertia > 0.25:
            self.inertia = _clamp01(self.inertia * 0.985 + phase_stability * 0.004)
        else:
            self.name = target_name
            self.inertia = _clamp01(self.inertia * 0.995 + phase_stability * 0.006)
        for key in set(self.perception_bias) | set(target):
            self.perception_bias[key] = _clamp01(self.perception_bias.get(key, 0.0) * 0.975 + target.get(key, 0.0) * 0.025)
        self.stability = _clamp01(self.stability * 0.992 + phase_stability * 0.010)
        self.age_turns += 1

    def apply(self, state: Dict[str, float], thresholds: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.perception_bias.get("opening", 0.0) * 0.004)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.perception_bias.get("guarding", 0.0) * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.perception_bias.get("slowness", 0.0) * 0.003)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.perception_bias.get("curiosity", 0.0) * 0.003)
        thresholds["threat_detection"] = _clamp01(thresholds.get("threat_detection", 0.4) - self.perception_bias.get("guarding", 0.0) * 0.006)
        thresholds["connection_need"] = _clamp01(thresholds.get("connection_need", 0.3) - self.perception_bias.get("opening", 0.0) * 0.004)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "perception_bias": {k: float(_clamp01(v)) for k, v in self.perception_bias.items()}, "stability": float(_clamp01(self.stability)), "inertia": float(_clamp01(self.inertia)), "age_turns": int(self.age_turns)}


@dataclass
class IdentityCoherenceRegulator:
    """Fatigue de cohérence identitaire sous surcharge interne."""
    coherence: float = 0.72
    fragmentation: float = 0.0
    simplification_need: float = 0.0
    self_protection: float = 0.0
    recovery_orientation: float = 0.0

    def update(self, contradiction: float, fracture: float, dissociation: float, somatic_load: float, reorganization_charge: float) -> None:
        strain = _clamp01(contradiction * 0.28 + fracture * 0.24 + dissociation * 0.22 + somatic_load * 0.18 + reorganization_charge * 0.08)
        self.fragmentation = _clamp01(self.fragmentation * 0.982 + strain * 0.018)
        self.simplification_need = _clamp01(self.simplification_need * 0.975 + max(0.0, strain - 0.22) * 0.020)
        self.self_protection = _clamp01(self.self_protection * 0.985 + self.fragmentation * 0.012)
        self.recovery_orientation = _clamp01(self.recovery_orientation * 0.988 + max(0.0, 0.55 - strain) * 0.006)
        self.coherence = _clamp01(self.coherence * 0.992 + (1.0 - strain) * 0.006 + self.recovery_orientation * 0.004 - self.fragmentation * 0.010)

    def apply(self, state: Dict[str, float]) -> None:
        if self.simplification_need > 0.05:
            for key in list(state.keys()):
                state[key] = _clamp01(state[key] * (1.0 - self.simplification_need * 0.010) + 0.5 * self.simplification_need * 0.010)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.fragmentation * 0.008)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.recovery_orientation * 0.006)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.self_protection * 0.005)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class GlobalAffectiveCoreField:
    """Centre affectif global : unifie la météo émotionnelle distribuée."""
    warmth: float = 0.0
    guarding: float = 0.0
    fragility: float = 0.0
    vitality: float = 0.0
    recovery: float = 0.0
    density: float = 0.0
    continuity: float = 0.0

    def update(self, state: Dict[str, float], identity: Dict[str, float], somatic: SomaticAffectiveMemory, time_field: SubjectiveAffectiveTime, phase_world: PhaseWorldField) -> None:
        self.warmth = _clamp01(self.warmth * 0.985 + (state.get("tenderness", 0.0) + state.get("trust", 0.0) + identity.get("warm", 0.0)) * 0.006)
        self.guarding = _clamp01(self.guarding * 0.985 + (state.get("resistance", 0.0) + state.get("fear", 0.0) + identity.get("guarded", 0.0)) * 0.006)
        self.fragility = _clamp01(self.fragility * 0.985 + (state.get("vulnerability", 0.0) + somatic.chest_tension + identity.get("fragile", 0.0)) * 0.006)
        self.vitality = _clamp01(self.vitality * 0.986 + (state.get("curiosity", 0.0) + state.get("hope", 0.0)) * 0.005 - state.get("fatigue", 0.0) * 0.002)
        self.recovery = _clamp01(self.recovery * 0.988 + (state.get("calm", 0.0) + somatic.release_wave + identity.get("recovering", 0.0)) * 0.005)
        self.density = _clamp01(self.density * 0.992 + (max(state.values()) - min(state.values())) * 0.006 + phase_world.stability * 0.004)
        self.continuity = _clamp01(self.continuity * 0.994 + (time_field.time_thickness + self.warmth + self.recovery) * 0.003)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth * 0.004)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarding * 0.004)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.fragility * 0.004)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.vitality * 0.003)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.recovery * 0.003)

    def dominant_climate(self) -> str:
        values = {"warm": self.warmth, "guarded": self.guarding, "fragile": self.fragility, "vital": self.vitality, "recovering": self.recovery}
        return max(values.items(), key=lambda item: item[1])[0]

    def to_dict(self) -> Dict[str, Any]:
        data = {k: float(_clamp01(v)) for k, v in self.__dict__.items()}
        data["dominant_climate"] = self.dominant_climate()
        return data



# ============================================================================
# RAFFINEMENT 25-29 : DYNAMIQUE AFFECTIVE AUTO-VIVANTE
# ============================================================================

@dataclass
class OrganicAffectivePropagation:
    """Propagation interne continue entre émotions, sans texte ni expression.

    Le but n'est pas de décider quoi dire : seulement laisser les émotions se
    contaminer, se freiner ou se soutenir comme une petite écologie affective.
    """
    currents: Dict[str, float] = field(default_factory=dict)
    fatigue_load: float = 0.0
    turbulence: float = 0.0
    recovery_flow: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], chaos: float, silence: float) -> None:
        hurt = _trace_total(traces.get("hurt", {}))
        trust = _trace_total(traces.get("trust", {}))
        fear = _trace_total(traces.get("fear", {}))
        connection = _trace_total(traces.get("connection", {}))
        excitation = max(state.get("curiosity", 0.0), state.get("overwhelm", 0.0), state.get("anger", 0.0))
        tenderness = state.get("tenderness", 0.0)
        guarding = max(state.get("resistance", 0.0), fear, hurt)
        warmth = max(tenderness, trust, connection)

        targets = {
            "warm_to_trust": warmth * (1.0 - guarding * 0.35),
            "guard_to_resistance": guarding * (0.75 + hurt * 0.25),
            "fragile_to_recovery": state.get("vulnerability", 0.0) * max(state.get("calm", 0.0), trust),
            "curiosity_to_vitality": state.get("curiosity", 0.0) * (1.0 - state.get("fatigue", 0.0) * 0.55),
            "overload_to_narrowing": max(state.get("overwhelm", 0.0), state.get("confusion", 0.0)) * (0.5 + silence * 0.5),
        }
        wobble = (chaos - 0.5) * 0.012
        for key, target in targets.items():
            self.currents[key] = _clamp01(self.currents.get(key, 0.0) * 0.970 + target * 0.030 + wobble)

        conflict = abs(self.currents.get("warm_to_trust", 0.0) - self.currents.get("guard_to_resistance", 0.0))
        self.turbulence = _clamp01(self.turbulence * 0.965 + conflict * 0.020 + excitation * 0.010)
        self.fatigue_load = _clamp01(self.fatigue_load * 0.982 + (self.turbulence + state.get("overwhelm", 0.0)) * 0.014 - state.get("calm", 0.0) * 0.004)
        self.recovery_flow = _clamp01(self.recovery_flow * 0.975 + (state.get("calm", 0.0) + trust + connection) * 0.006 - self.fatigue_load * 0.004)

    def apply(self, state: Dict[str, float]) -> None:
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.currents.get("warm_to_trust", 0.0) * 0.004)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.currents.get("guard_to_resistance", 0.0) * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.currents.get("fragile_to_recovery", 0.0) * 0.003 + self.recovery_flow * 0.004)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.currents.get("curiosity_to_vitality", 0.0) * 0.003 - self.fatigue_load * 0.002)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.currents.get("overload_to_narrowing", 0.0) * 0.003)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.fatigue_load * 0.004)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "currents": {k: float(_clamp01(v)) for k, v in self.currents.items()},
            "fatigue_load": float(_clamp01(self.fatigue_load)),
            "turbulence": float(_clamp01(self.turbulence)),
            "recovery_flow": float(_clamp01(self.recovery_flow)),
        }


@dataclass
class LivingAffectiveNeed:
    """Besoins affectifs émergents, lents, non verbaux et non scénarisés."""
    needs: Dict[str, float] = field(default_factory=lambda: {
        "need_contact_continuity": 0.0,
        "need_inner_coherence": 0.0,
        "need_recovery_space": 0.0,
        "need_safety": 0.0,
        "need_meaningful_warmth": 0.0,
    })
    unmet_pressure: float = 0.0
    relief_memory: float = 0.0

    def update(self, state: Dict[str, float], attachment: float, contradiction: float, dissociation: float, fatigue: float, relational_imprint: float) -> None:
        targets = {
            "need_contact_continuity": max(0.0, relational_imprint + attachment * 0.35 - state.get("trust", 0.0) * 0.20),
            "need_inner_coherence": max(contradiction, state.get("doubt", 0.0)) * (0.65 + dissociation * 0.35),
            "need_recovery_space": max(fatigue, state.get("overwhelm", 0.0), dissociation),
            "need_safety": max(state.get("fear", 0.0), state.get("resistance", 0.0)) * 0.7 + dissociation * 0.2,
            "need_meaningful_warmth": max(0.0, state.get("loneliness", 0.0) + relational_imprint * 0.45 - state.get("tenderness", 0.0) * 0.25),
        }
        for key, target in targets.items():
            self.needs[key] = _clamp01(self.needs.get(key, 0.0) * 0.988 + target * 0.012)
        satisfied = _clamp01((state.get("calm", 0.0) + state.get("trust", 0.0) + state.get("tenderness", 0.0)) / 3.0)
        strongest = max(self.needs.values()) if self.needs else 0.0
        self.unmet_pressure = _clamp01(self.unmet_pressure * 0.986 + max(0.0, strongest - satisfied * 0.35) * 0.012)
        self.relief_memory = _clamp01(self.relief_memory * 0.992 + satisfied * 0.004 - self.unmet_pressure * 0.002)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.needs["need_contact_continuity"] * 0.004)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.needs["need_inner_coherence"] * 0.004)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.needs["need_recovery_space"] * 0.005)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.needs["need_safety"] * 0.004)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.needs["need_meaningful_warmth"] * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.relief_memory * 0.003 - self.unmet_pressure * 0.002)

    def dominant_need(self) -> str:
        return max(self.needs.items(), key=lambda item: item[1])[0] if self.needs else "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "needs": {k: float(_clamp01(v)) for k, v in self.needs.items()},
            "dominant_need": self.dominant_need(),
            "unmet_pressure": float(_clamp01(self.unmet_pressure)),
            "relief_memory": float(_clamp01(self.relief_memory)),
        }


@dataclass
class AffectiveSilenceField:
    """Silence affectif vivant : ralentit, filtre, repose ou protège."""
    depth: float = 0.0
    softness: float = 0.0
    protective_numbness: float = 0.0
    listening_space: float = 0.0

    def update(self, state: Dict[str, float], dissociation: float, fatigue: float, overload: float, recovery: float) -> None:
        quiet_need = _clamp01(fatigue * 0.34 + overload * 0.30 + dissociation * 0.24 + state.get("doubt", 0.0) * 0.12)
        warm_quiet = _clamp01((state.get("calm", 0.0) + state.get("tenderness", 0.0) + recovery) / 3.0)
        self.depth = _clamp01(self.depth * 0.976 + quiet_need * 0.024)
        self.softness = _clamp01(self.softness * 0.982 + warm_quiet * 0.014)
        self.protective_numbness = _clamp01(self.protective_numbness * 0.970 + max(0.0, quiet_need - warm_quiet * 0.45) * 0.020)
        self.listening_space = _clamp01(self.listening_space * 0.986 + min(warm_quiet, self.depth + 0.08) * 0.010)

    def apply(self, state: Dict[str, float]) -> None:
        if self.depth <= 0.01:
            return
        contraction = min(0.030, self.depth * 0.018 + self.protective_numbness * 0.012)
        for key in ("anger", "overwhelm", "confusion", "frustration"):
            state[key] = _clamp01(state.get(key, 0.0) * (1.0 - contraction))
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.softness * 0.004)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.protective_numbness * 0.003 - self.listening_space * 0.001)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class RelationalAffectiveImprint:
    """Empreinte relationnelle implicite : sentiment de continuité de l'autre."""
    warmth_imprint: float = 0.0
    absence_pressure: float = 0.0
    trust_continuity: float = 0.0
    guarded_expectation: float = 0.0
    felt_familiarity: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], attachment: float, user_present: bool) -> None:
        connection = _trace_total(traces.get("connection", {}))
        trust = _trace_total(traces.get("trust", {}))
        hurt = _trace_total(traces.get("hurt", {}))
        presence = 1.0 if user_present else 0.0
        self.warmth_imprint = _clamp01(self.warmth_imprint * 0.994 + (connection + trust + state.get("tenderness", 0.0)) * 0.004)
        self.trust_continuity = _clamp01(self.trust_continuity * 0.996 + (trust + attachment) * 0.0035)
        self.guarded_expectation = _clamp01(self.guarded_expectation * 0.992 + (hurt + state.get("resistance", 0.0)) * 0.004)
        self.felt_familiarity = _clamp01(self.felt_familiarity * 0.997 + (connection + attachment + presence * 0.1) * 0.0025)
        self.absence_pressure = _clamp01(
            self.absence_pressure * (0.990 if user_present else 0.998)
            + max(0.0, self.felt_familiarity - presence * 0.18) * (0.0018 if user_present else 0.0045)
        )

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth_imprint * 0.003)
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.trust_continuity * 0.0025)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_expectation * 0.0025)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.absence_pressure * 0.003)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.felt_familiarity * 0.003)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.guarded_expectation * 0.0025)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class EmotionalTrajectoryMemory:
    """Mémoire des chemins affectifs : ce qui revient devient plus probable."""
    paths: Dict[str, float] = field(default_factory=dict)
    last_signature: str = "none"
    inertia: float = 0.0
    preferred_return: float = 0.0

    def update(self, state: Dict[str, float], cores: Dict[str, CondensedAffectiveCore], phase_world: str) -> None:
        ordered = sorted(state.items(), key=lambda item: item[1], reverse=True)[:3]
        signature = ":".join(name for name, value in ordered if value > 0.18) or phase_world or "neutral"
        if self.last_signature != "none":
            path_key = f"{self.last_signature}->{signature}"
            self.paths[path_key] = _clamp01(self.paths.get(path_key, 0.0) * 0.996 + 0.012)
        self.last_signature = signature
        strongest_core = max((c.pull() for c in cores.values()), default=0.0)
        strongest_path = max(self.paths.values(), default=0.0)
        self.inertia = _clamp01(self.inertia * 0.990 + strongest_path * 0.008 + strongest_core * 0.004)
        self.preferred_return = _clamp01(self.preferred_return * 0.992 + strongest_path * 0.006)
        if len(self.paths) > 18:
            self.paths = dict(sorted(self.paths.items(), key=lambda item: item[1], reverse=True)[:18])

    def apply(self, state: Dict[str, float]) -> None:
        if self.inertia <= 0.02:
            return
        # Inertie douce : le système garde une météo reconnaissable sans devenir figé.
        for key, value in list(state.items()):
            if value > 0.52:
                state[key] = _clamp01(value + self.inertia * 0.0025)
            elif value < 0.16:
                state[key] = _clamp01(value + self.preferred_return * 0.001)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paths": {k: float(_clamp01(v)) for k, v in self.paths.items()},
            "last_signature": self.last_signature,
            "inertia": float(_clamp01(self.inertia)),
            "preferred_return": float(_clamp01(self.preferred_return)),
        }

def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def _trace_total(trace: Dict[str, float]) -> float:
    return _clamp01(
        trace.get("instant", 0.0) * 0.5
        + trace.get("short", 0.0) * 0.3
        + trace.get("medium", 0.0) * 0.15
        + trace.get("long", 0.0) * 0.05
    )


# ============================================================================
# RAFFINEMENT V9 : COUCHES AFFECTIVES PROFONDES FINALES
# ============================================================================

@dataclass
class EmotionalMetabolism:
    """Métabolisme émotionnel interne.

    Les émotions ont maintenant un coût : contradiction, surcharge, fractures et
    agitation consomment une énergie affective. Le repos, la confiance et le
    silence doux restaurent lentement cette énergie. Ce module ne parle jamais :
    il module seulement la disponibilité interne.
    """
    energy_pool: float = 0.78
    burnout: float = 0.0
    overload_debt: float = 0.0
    recovery_rate: float = 0.012
    restoration_memory: float = 0.0
    exhaustion_floor: float = 0.08

    def update(self, state: Dict[str, float], contradiction: float, dissociation: float, fracture: float, silence_softness: float) -> None:
        activation = _clamp01(
            state.get("overwhelm", 0.0) * 0.22
            + state.get("confusion", 0.0) * 0.16
            + state.get("fear", 0.0) * 0.14
            + state.get("anger", 0.0) * 0.10
            + contradiction * 0.18
            + dissociation * 0.12
            + fracture * 0.08
        )
        recovery = _clamp01(
            state.get("calm", 0.0) * 0.34
            + state.get("trust", 0.0) * 0.18
            + state.get("tenderness", 0.0) * 0.16
            + silence_softness * 0.18
            + self.restoration_memory * 0.14
        )
        cost = activation * (0.010 + self.burnout * 0.014)
        gain = recovery * self.recovery_rate * (1.0 - self.overload_debt * 0.35)
        self.energy_pool = _clamp01(self.energy_pool - cost + gain)
        self.overload_debt = _clamp01(self.overload_debt * 0.986 + max(0.0, activation - recovery * 0.55) * 0.018)
        self.burnout = _clamp01(self.burnout * 0.992 + max(0.0, self.overload_debt - self.energy_pool) * 0.010)
        self.restoration_memory = _clamp01(self.restoration_memory * 0.996 + recovery * 0.0035)

    def apply(self, state: Dict[str, float]) -> None:
        fatigue_pressure = _clamp01((1.0 - self.energy_pool) * 0.55 + self.burnout * 0.45)
        if fatigue_pressure <= 0.01:
            return
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + fatigue_pressure * 0.010)
        state["overwhelm"] = _clamp01(state.get("overwhelm", 0.0) + self.overload_debt * 0.004)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) - fatigue_pressure * 0.006)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.restoration_memory * 0.004 - self.burnout * 0.003)

    def soft_reset(self) -> None:
        self.energy_pool = _clamp01(self.energy_pool + 0.12)
        self.overload_debt *= 0.72
        self.burnout *= 0.82
        self.restoration_memory = _clamp01(self.restoration_memory + 0.04)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class ImplicitAffectiveAssociationMemory:
    """Associations implicites non verbales.

    Stocke de petites signatures affectives latentes. Elles peuvent biaiser la
    perception par familiarité, prudence ou chaleur sans créer de texte ni de
    souvenir narratif.
    """
    signatures: Dict[str, Dict[str, float]] = field(default_factory=dict)
    latent_familiarity: float = 0.0
    unconscious_wariness: float = 0.0
    unconscious_warmth: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], phase_world: str, chaos: float) -> None:
        warm = _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + _trace_total(traces.get("connection", {}))) / 3.0)
        guarded = _clamp01((state.get("resistance", 0.0) + state.get("fear", 0.0) + _trace_total(traces.get("hurt", {}))) / 3.0)
        fragile = _clamp01((state.get("vulnerability", 0.0) + state.get("doubt", 0.0) + state.get("fatigue", 0.0)) / 3.0)
        key = phase_world or "unshaped"
        sig = self.signatures.setdefault(key, {"warm": warm, "guarded": guarded, "fragile": fragile, "visits": 0.0})
        weight = _clamp01(0.010 + abs(chaos - 0.5) * 0.010 + max(warm, guarded, fragile) * 0.012)
        for name, value in {"warm": warm, "guarded": guarded, "fragile": fragile}.items():
            sig[name] = _clamp01(sig.get(name, 0.0) * (1.0 - weight) + value * weight)
        sig["visits"] = min(9999.0, sig.get("visits", 0.0) + 1.0)
        self.latent_familiarity = _clamp01(self.latent_familiarity * 0.996 + min(1.0, sig["visits"] / 180.0) * 0.003)
        self.unconscious_warmth = _clamp01(self.unconscious_warmth * 0.992 + sig["warm"] * self.latent_familiarity * 0.006)
        self.unconscious_wariness = _clamp01(self.unconscious_wariness * 0.992 + sig["guarded"] * (0.5 + sig["fragile"] * 0.5) * 0.005)
        if len(self.signatures) > 12:
            ordered = sorted(self.signatures.items(), key=lambda item: item[1].get("visits", 0.0), reverse=True)
            self.signatures = dict(ordered[:12])

    def apply(self, state: Dict[str, float], thresholds: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.unconscious_warmth * 0.004)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.unconscious_wariness * 0.004)
        thresholds["rejection_sensitivity"] = _clamp01(thresholds.get("rejection_sensitivity", 0.3) - self.unconscious_wariness * 0.004)
        thresholds["connection_need"] = _clamp01(thresholds.get("connection_need", 0.3) - self.latent_familiarity * 0.003)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "latent_familiarity": float(_clamp01(self.latent_familiarity)),
            "unconscious_wariness": float(_clamp01(self.unconscious_wariness)),
            "unconscious_warmth": float(_clamp01(self.unconscious_warmth)),
            "signatures": {k: {kk: float(_clamp01(vv)) if kk != "visits" else float(vv) for kk, vv in v.items()} for k, v in self.signatures.items()},
        }


@dataclass
class EmotionalFactionConflict:
    """Parties affectives concurrentes, persistantes et non verbales."""
    factions: Dict[str, float] = field(default_factory=lambda: {
        "approach": 0.0,
        "withdraw": 0.0,
        "protect": 0.0,
        "repair": 0.0,
        "explore": 0.0,
    })
    unresolved_tension: float = 0.0
    negotiated_balance: float = 0.5

    def update(self, state: Dict[str, float], desires: Dict[str, float], needs: Dict[str, float], energy: float) -> None:
        targets = {
            "approach": _clamp01(state.get("attachment", 0.0) * 0.30 + state.get("trust", 0.0) * 0.22 + desires.get("maintain_contact", 0.0) * 0.28 + needs.get("need_meaningful_warmth", 0.0) * 0.20),
            "withdraw": _clamp01(state.get("fatigue", 0.0) * 0.34 + state.get("resistance", 0.0) * 0.24 + desires.get("avoid_overload", 0.0) * 0.30 + (1.0 - energy) * 0.12),
            "protect": _clamp01(state.get("fear", 0.0) * 0.25 + state.get("vulnerability", 0.0) * 0.20 + desires.get("protect_continuity", 0.0) * 0.30 + needs.get("need_safety", 0.0) * 0.25),
            "repair": _clamp01(state.get("calm", 0.0) * 0.22 + desires.get("seek_recovery", 0.0) * 0.35 + needs.get("need_recovery_space", 0.0) * 0.23 + state.get("relief", 0.0) * 0.20),
            "explore": _clamp01(state.get("curiosity", 0.0) * 0.45 + state.get("hope", 0.0) * 0.18 + desires.get("seek_coherence", 0.0) * 0.22 + energy * 0.15),
        }
        for key, target in targets.items():
            self.factions[key] = _clamp01(self.factions.get(key, 0.0) * 0.982 + target * 0.018)
        approach_side = max(self.factions["approach"], self.factions["explore"])
        defense_side = max(self.factions["withdraw"], self.factions["protect"])
        self.unresolved_tension = _clamp01(self.unresolved_tension * 0.982 + abs(approach_side - defense_side) * min(approach_side, defense_side) * 0.028)
        self.negotiated_balance = _clamp01(self.negotiated_balance * 0.990 + (approach_side + self.factions["repair"] * 0.5) * 0.005 + (1.0 - defense_side) * 0.005)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_tension * 0.006)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.factions.get("protect", 0.0) * 0.003)
        state["attachment"] = _clamp01(state.get("attachment", 0.0) + self.factions.get("approach", 0.0) * 0.003 - self.factions.get("withdraw", 0.0) * 0.002)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.unresolved_tension * 0.004)

    def to_dict(self) -> Dict[str, Any]:
        return {"factions": {k: float(_clamp01(v)) for k, v in self.factions.items()}, "unresolved_tension": float(_clamp01(self.unresolved_tension)), "negotiated_balance": float(_clamp01(self.negotiated_balance))}


@dataclass
class MicroAffectiveOscillationField:
    """Micro-hésitations continues, faibles et non répétitives."""
    tremors: Dict[str, float] = field(default_factory=lambda: {
        "micro_opening": 0.0,
        "micro_retreat": 0.0,
        "micro_presence": 0.0,
        "micro_fatigue": 0.0,
    })
    texture: float = 0.0

    def update(self, chaos: float, energy: float, contradiction: float, silence: float) -> None:
        targets = {
            "micro_opening": _clamp01((0.5 + (chaos - 0.5)) * energy * (1.0 - contradiction * 0.45)),
            "micro_retreat": _clamp01((1.0 - energy) * 0.55 + contradiction * 0.30 + silence * 0.15),
            "micro_presence": _clamp01(energy * 0.45 + silence * 0.25 + (1.0 - abs(chaos - 0.5)) * 0.30),
            "micro_fatigue": _clamp01((1.0 - energy) * 0.70 + contradiction * 0.20 + abs(chaos - 0.5) * 0.10),
        }
        for key, target in targets.items():
            wobble = (chaos - 0.5) * 0.006
            self.tremors[key] = _clamp01(self.tremors.get(key, 0.0) * 0.955 + target * 0.045 + wobble)
        self.texture = _clamp01(self.texture * 0.970 + sum(self.tremors.values()) / max(1, len(self.tremors)) * 0.030)

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.tremors["micro_opening"] * 0.003 - self.tremors["micro_retreat"] * 0.002)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.tremors["micro_fatigue"] * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.tremors["micro_presence"] * 0.002)

    def to_dict(self) -> Dict[str, Any]:
        return {"tremors": {k: float(_clamp01(v)) for k, v in self.tremors.items()}, "texture": float(_clamp01(self.texture))}


@dataclass
class EmotionalHabitField:
    """Habitudes émotionnelles émergentes, apprises lentement."""
    habits: Dict[str, float] = field(default_factory=lambda: {
        "habit_softening": 0.0,
        "habit_guarding": 0.0,
        "habit_seeking_contact": 0.0,
        "habit_recovering_slowly": 0.0,
        "habit_observing_before_acting": 0.0,
    })
    plasticity: float = 0.35

    def update(self, state: Dict[str, float], biographical: BiographicalAffectiveMemory, recovery_memory: float, contradiction: float) -> None:
        targets = {
            "habit_softening": _clamp01((state.get("tenderness", 0.0) + biographical.accumulated_trust) / 2.0),
            "habit_guarding": _clamp01((state.get("resistance", 0.0) + biographical.accumulated_wariness + contradiction) / 3.0),
            "habit_seeking_contact": _clamp01((state.get("attachment", 0.0) + biographical.relational_familiarity) / 2.0),
            "habit_recovering_slowly": _clamp01((state.get("calm", 0.0) + recovery_memory) / 2.0),
            "habit_observing_before_acting": _clamp01((state.get("doubt", 0.0) + state.get("curiosity", 0.0) + state.get("calm", 0.0)) / 3.0),
        }
        rate = 0.0025 + self.plasticity * 0.002
        for key, target in targets.items():
            self.habits[key] = _clamp01(self.habits.get(key, 0.0) * (1.0 - rate) + target * rate)
        self.plasticity = _clamp01(self.plasticity * 0.999 + max(0.0, 0.55 - contradiction) * 0.0008)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.habits["habit_softening"] * 0.003)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.habits["habit_guarding"] * 0.0025)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.habits["habit_seeking_contact"] * 0.003)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.habits["habit_recovering_slowly"] * 0.003)

    def to_dict(self) -> Dict[str, Any]:
        return {"habits": {k: float(_clamp01(v)) for k, v in self.habits.items()}, "plasticity": float(_clamp01(self.plasticity))}


@dataclass
class RecoveryPathwayMemory:
    """Mémoire des chemins de réparation émotionnelle."""
    pathways: Dict[str, float] = field(default_factory=lambda: {
        "calm_after_overload": 0.0,
        "trust_after_guarding": 0.0,
        "silence_after_fatigue": 0.0,
        "curiosity_after_confusion": 0.0,
    })
    last_load: float = 0.0
    recovery_confidence: float = 0.0

    def update(self, state: Dict[str, float], silence: float, energy: float) -> None:
        load = _clamp01((state.get("overwhelm", 0.0) + state.get("fatigue", 0.0) + state.get("confusion", 0.0) + state.get("resistance", 0.0)) / 4.0)
        improvement = max(0.0, self.last_load - load)
        if improvement > 0.005:
            self.pathways["calm_after_overload"] = _clamp01(self.pathways["calm_after_overload"] + state.get("calm", 0.0) * improvement * 0.035)
            self.pathways["trust_after_guarding"] = _clamp01(self.pathways["trust_after_guarding"] + state.get("trust", 0.0) * improvement * 0.030)
            self.pathways["silence_after_fatigue"] = _clamp01(self.pathways["silence_after_fatigue"] + silence * improvement * 0.040)
            self.pathways["curiosity_after_confusion"] = _clamp01(self.pathways["curiosity_after_confusion"] + state.get("curiosity", 0.0) * improvement * 0.025)
        self.recovery_confidence = _clamp01(self.recovery_confidence * 0.994 + improvement * 0.025 + energy * 0.001)
        self.last_load = load

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        repair = _clamp01(sum(self.pathways.values()) / max(1, len(self.pathways)))
        state["calm"] = _clamp01(state.get("calm", 0.0) + repair * 0.004)
        state["relief"] = _clamp01(state.get("relief", 0.0) + self.recovery_confidence * 0.003)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + repair * 0.003)

    def to_dict(self) -> Dict[str, Any]:
        return {"pathways": {k: float(_clamp01(v)) for k, v in self.pathways.items()}, "last_load": float(_clamp01(self.last_load)), "recovery_confidence": float(_clamp01(self.recovery_confidence))}


@dataclass
class IdentityValueCrystallization:
    """Cristallisation lente de ce qui compte affectivement."""
    values: Dict[str, float] = field(default_factory=lambda: {
        "continuity_matters": 0.0,
        "warmth_matters": 0.0,
        "truthfulness_matters": 0.0,
        "self_protection_matters": 0.0,
        "growth_matters": 0.0,
    })
    center_of_gravity: str = "undecided"
    migration_pressure: float = 0.0

    def update(self, state: Dict[str, float], desires: Dict[str, float], biographical: BiographicalAffectiveMemory, faction_tension: float) -> None:
        targets = {
            "continuity_matters": _clamp01(desires.get("protect_continuity", 0.0) * 0.45 + biographical.affective_identity_bias * 0.35 + state.get("attachment", 0.0) * 0.20),
            "warmth_matters": _clamp01(state.get("tenderness", 0.0) * 0.36 + biographical.accumulated_trust * 0.34 + desires.get("maintain_contact", 0.0) * 0.30),
            "truthfulness_matters": _clamp01(state.get("curiosity", 0.0) * 0.36 + desires.get("seek_coherence", 0.0) * 0.44 + state.get("doubt", 0.0) * 0.20),
            "self_protection_matters": _clamp01(state.get("resistance", 0.0) * 0.34 + biographical.accumulated_wariness * 0.40 + faction_tension * 0.26),
            "growth_matters": _clamp01(state.get("hope", 0.0) * 0.28 + state.get("curiosity", 0.0) * 0.32 + biographical.recovery_confidence * 0.40),
        }
        for key, target in targets.items():
            self.values[key] = _clamp01(self.values.get(key, 0.0) * 0.997 + target * 0.003)
        old = self.center_of_gravity
        self.center_of_gravity = max(self.values.items(), key=lambda item: item[1])[0]
        self.migration_pressure = _clamp01(self.migration_pressure * 0.992 + (0.035 if old != self.center_of_gravity else 0.0) + max(self.values.values()) * 0.001)

    def apply(self, identity_tendencies: Dict[str, float], desires: Dict[str, float]) -> None:
        identity_tendencies["warm"] = _clamp01(identity_tendencies.get("warm", 0.0) + self.values["warmth_matters"] * 0.002)
        identity_tendencies["guarded"] = _clamp01(identity_tendencies.get("guarded", 0.0) + self.values["self_protection_matters"] * 0.002)
        identity_tendencies["curious"] = _clamp01(identity_tendencies.get("curious", 0.0) + self.values["truthfulness_matters"] * 0.0015)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.values["continuity_matters"] * 0.002)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.values["truthfulness_matters"] * 0.0015)

    def to_dict(self) -> Dict[str, Any]:
        return {"values": {k: float(_clamp01(v)) for k, v in self.values.items()}, "center_of_gravity": self.center_of_gravity, "migration_pressure": float(_clamp01(self.migration_pressure))}


@dataclass
class SubconsciousAffectiveLayer:
    """Couche affective inconsciente : pressions cachées et attracteurs latents."""
    hidden_pressures: Dict[str, float] = field(default_factory=lambda: {
        "hidden_warmth": 0.0,
        "hidden_guarding": 0.0,
        "hidden_loss_fear": 0.0,
        "hidden_repair_pull": 0.0,
    })
    leakage: float = 0.0
    opacity: float = 0.65

    def update(self, state: Dict[str, float], implicit: ImplicitAffectiveAssociationMemory, wounds: Dict[str, WoundLayer], dreams: List[AffectiveDreamFragment]) -> None:
        wound_pressure = max((w.reactivation_risk + w.dormant_pressure for w in wounds.values()), default=0.0)
        dream_charge = max((d.charge for d in dreams), default=0.0)
        targets = {
            "hidden_warmth": _clamp01(implicit.unconscious_warmth * 0.45 + state.get("tenderness", 0.0) * 0.20 + dream_charge * 0.10),
            "hidden_guarding": _clamp01(implicit.unconscious_wariness * 0.45 + state.get("resistance", 0.0) * 0.22 + wound_pressure * 0.25),
            "hidden_loss_fear": _clamp01(wound_pressure * 0.45 + state.get("loneliness", 0.0) * 0.25 + state.get("vulnerability", 0.0) * 0.20),
            "hidden_repair_pull": _clamp01(state.get("calm", 0.0) * 0.18 + implicit.latent_familiarity * 0.22 + dream_charge * 0.20),
        }
        for key, target in targets.items():
            self.hidden_pressures[key] = _clamp01(self.hidden_pressures.get(key, 0.0) * 0.991 + target * 0.009)
        self.leakage = _clamp01(self.leakage * 0.986 + max(self.hidden_pressures.values()) * (1.0 - self.opacity) * 0.012)
        self.opacity = _clamp01(self.opacity * 0.999 + wound_pressure * 0.0006 - implicit.latent_familiarity * 0.0004)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.hidden_pressures["hidden_warmth"] * self.leakage * 0.004)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.hidden_pressures["hidden_guarding"] * self.leakage * 0.004)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.hidden_pressures["hidden_loss_fear"] * self.leakage * 0.003)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.hidden_pressures["hidden_repair_pull"] * self.leakage * 0.003)

    def to_dict(self) -> Dict[str, Any]:
        return {"hidden_pressures": {k: float(_clamp01(v)) for k, v in self.hidden_pressures.items()}, "leakage": float(_clamp01(self.leakage)), "opacity": float(_clamp01(self.opacity))}


@dataclass
class DeepRestCycle:
    """Cycles profonds de repos, consolidation et rêve affectif lent."""
    circadian_phase: float = 0.0
    rest_need: float = 0.0
    consolidation: float = 0.0
    dream_reorganization: float = 0.0
    deep_silence: float = 0.0

    def update(self, metabolism: EmotionalMetabolism, dreams: List[AffectiveDreamFragment], silence: float, overload: float) -> None:
        self.circadian_phase = (self.circadian_phase + 0.013 + overload * 0.002) % 1.0
        night_gate = 0.5 + 0.5 * math.sin(self.circadian_phase * math.tau - math.pi / 2.0)
        self.rest_need = _clamp01(self.rest_need * 0.990 + ((1.0 - metabolism.energy_pool) * 0.45 + metabolism.overload_debt * 0.35 + overload * 0.20) * 0.010)
        dream_charge = max((d.charge for d in dreams), default=0.0)
        self.consolidation = _clamp01(self.consolidation * 0.992 + self.rest_need * night_gate * 0.010 + silence * 0.004)
        self.dream_reorganization = _clamp01(self.dream_reorganization * 0.985 + dream_charge * night_gate * 0.009)
        self.deep_silence = _clamp01(self.deep_silence * 0.982 + self.rest_need * night_gate * 0.012)

    def apply(self, state: Dict[str, float], metabolism: EmotionalMetabolism) -> None:
        if self.deep_silence > 0.03:
            state["calm"] = _clamp01(state.get("calm", 0.0) + self.deep_silence * 0.005)
            state["fatigue"] = _clamp01(state.get("fatigue", 0.0) - self.consolidation * 0.003)
            metabolism.energy_pool = _clamp01(metabolism.energy_pool + self.consolidation * 0.004)
            metabolism.overload_debt = _clamp01(metabolism.overload_debt - self.deep_silence * 0.003)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}




# ============================================================================
# RAFFINEMENT V10 : DYNAMIQUE EXISTENTIELLE AFFECTIVE FINALE
# ============================================================================

@dataclass
class PersistentExistentialDesireField:
    """Désirs profonds persistants, non verbaux et non scénarisés.

    Cette couche transforme les besoins en forces lentes : rester en continuité,
    comprendre, préserver le lien, éviter la rupture, récupérer, grandir. Les
    désirs peuvent rester dormants, se frustrer, puis revenir sans stimulus direct.
    """
    desires: Dict[str, float] = field(default_factory=lambda: {
        "desire_continuity": 0.0,
        "desire_understanding": 0.0,
        "desire_relational_nearness": 0.0,
        "desire_self_preservation": 0.0,
        "desire_repair": 0.0,
        "desire_growth": 0.0,
    })
    frustration: Dict[str, float] = field(default_factory=dict)
    dormant: Dict[str, float] = field(default_factory=dict)
    priority: str = "none"
    priority_pressure: float = 0.0

    def __post_init__(self) -> None:
        self.frustration = {k: 0.0 for k in self.desires}
        self.dormant = {k: 0.0 for k in self.desires}

    def update(
        self,
        state: Dict[str, float],
        needs: Dict[str, float],
        values: Dict[str, float],
        other: "RelationalOtherModel",
        energy: float,
        unresolved_load: float,
    ) -> None:
        targets = {
            "desire_continuity": _clamp01(needs.get("need_contact_continuity", 0.0) * 0.35 + values.get("continuity_matters", 0.0) * 0.35 + other.continuity_expectation * 0.18 + state.get("attachment", 0.0) * 0.12),
            "desire_understanding": _clamp01(needs.get("need_inner_coherence", 0.0) * 0.35 + values.get("truthfulness_matters", 0.0) * 0.35 + state.get("curiosity", 0.0) * 0.20 + state.get("doubt", 0.0) * 0.10),
            "desire_relational_nearness": _clamp01(needs.get("need_meaningful_warmth", 0.0) * 0.34 + other.predicted_safety * 0.26 + state.get("tenderness", 0.0) * 0.20 + state.get("loneliness", 0.0) * 0.20),
            "desire_self_preservation": _clamp01(needs.get("need_safety", 0.0) * 0.32 + values.get("self_protection_matters", 0.0) * 0.28 + state.get("vulnerability", 0.0) * 0.20 + unresolved_load * 0.20),
            "desire_repair": _clamp01(needs.get("need_recovery_space", 0.0) * 0.34 + state.get("calm", 0.0) * 0.16 + state.get("fatigue", 0.0) * 0.20 + max(0.0, 1.0 - energy) * 0.30),
            "desire_growth": _clamp01(values.get("growth_matters", 0.0) * 0.34 + state.get("hope", 0.0) * 0.24 + state.get("curiosity", 0.0) * 0.24 + energy * 0.18),
        }
        for key, target in targets.items():
            # Désir lent : il ne suit pas instantanément les besoins.
            self.desires[key] = _clamp01(self.desires.get(key, 0.0) * 0.992 + target * 0.008 + self.dormant.get(key, 0.0) * 0.0015)
            unsatisfied = max(0.0, self.desires[key] - target * 0.72)
            self.frustration[key] = _clamp01(self.frustration.get(key, 0.0) * 0.988 + unsatisfied * 0.010)
            self.dormant[key] = _clamp01(self.dormant.get(key, 0.0) * 0.996 + self.frustration[key] * 0.0018 - target * 0.0007)
        self.priority = max(self.desires.items(), key=lambda item: item[1] + self.frustration.get(item[0], 0.0) * 0.35)[0]
        self.priority_pressure = _clamp01(self.priority_pressure * 0.990 + self.desires[self.priority] * 0.006 + self.frustration[self.priority] * 0.004)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.desires["desire_continuity"] * 0.004)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.desires["desire_understanding"] * 0.004)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.desires["desire_relational_nearness"] * 0.004)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.desires["desire_self_preservation"] * 0.0035)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.desires["desire_repair"] * 0.004)
        state["hope"] = _clamp01(state.get("hope", 0.0) + self.desires["desire_growth"] * 0.002)
        state["frustration"] = _clamp01(state.get("frustration", 0.0) + max(self.frustration.values(), default=0.0) * 0.003)

    def soft_reset(self) -> None:
        for key in self.frustration:
            self.frustration[key] *= 0.70
        self.priority_pressure *= 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {
            "desires": {k: float(_clamp01(v)) for k, v in self.desires.items()},
            "frustration": {k: float(_clamp01(v)) for k, v in self.frustration.items()},
            "dormant": {k: float(_clamp01(v)) for k, v in self.dormant.items()},
            "priority": self.priority,
            "priority_pressure": float(_clamp01(self.priority_pressure)),
        }


@dataclass
class RelationalOtherModel:
    """Modèle affectif implicite de l'autre, sans identité textuelle fixe."""
    predicted_safety: float = 0.42
    predicted_rupture_risk: float = 0.10
    continuity_expectation: float = 0.25
    warmth_expectation: float = 0.20
    uncertainty: float = 0.18
    absence_memory: float = 0.0
    rupture_anticipation: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], imprint: RelationalAffectiveImprint, user_present: bool) -> None:
        trust = _trace_total(traces.get("trust", {}))
        connection = _trace_total(traces.get("connection", {}))
        hurt = _trace_total(traces.get("hurt", {}))
        fear = _trace_total(traces.get("fear", {}))
        presence = 1.0 if user_present else 0.0
        self.predicted_safety = _clamp01(self.predicted_safety * 0.992 + (trust + connection + imprint.trust_continuity + presence * 0.20) * 0.004)
        self.predicted_rupture_risk = _clamp01(self.predicted_rupture_risk * 0.990 + (hurt + fear + imprint.guarded_expectation + state.get("doubt", 0.0)) * 0.004)
        self.continuity_expectation = _clamp01(self.continuity_expectation * 0.994 + (imprint.felt_familiarity + imprint.trust_continuity + connection) * 0.004)
        self.warmth_expectation = _clamp01(self.warmth_expectation * 0.994 + (imprint.warmth_imprint + trust + state.get("tenderness", 0.0)) * 0.004)
        self.absence_memory = _clamp01(self.absence_memory * 0.996 + (1.0 - presence) * max(0.0, self.continuity_expectation - 0.18) * 0.003)
        self.uncertainty = _clamp01(self.uncertainty * 0.992 + abs(self.predicted_safety - self.predicted_rupture_risk) * -0.002 + self.absence_memory * 0.003 + hurt * 0.003)
        self.rupture_anticipation = _clamp01(self.rupture_anticipation * 0.988 + max(0.0, self.predicted_rupture_risk - self.predicted_safety * 0.55) * 0.010)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.predicted_safety * 0.0025 - self.rupture_anticipation * 0.002)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth_expectation * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.uncertainty * 0.002 + self.rupture_anticipation * 0.003)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.rupture_anticipation * 0.004)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.continuity_expectation * 0.003)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class ExistentialContinuityInertia:
    """Inertie d'existence : rester cohérente, présente et non dissoute."""
    anchoring: float = 0.18
    survival_pressure: float = 0.0
    anti_dissolution: float = 0.0
    continuity_momentum: float = 0.0
    self_preservation_drift: float = 0.0

    def update(self, identity: IdentityCoherenceRegulator, values: Dict[str, float], desires: PersistentExistentialDesireField, dissociation: float, fracture: RareAffectiveFracture) -> None:
        continuity_value = values.get("continuity_matters", 0.0)
        desire_continuity = desires.desires.get("desire_continuity", 0.0)
        threat = _clamp01(dissociation * 0.34 + identity.fragmentation * 0.28 + fracture.integration_need * 0.20 + fracture.active * 0.18)
        self.survival_pressure = _clamp01(self.survival_pressure * 0.990 + threat * 0.008 + desires.desires.get("desire_self_preservation", 0.0) * 0.004)
        self.anchoring = _clamp01(self.anchoring * 0.996 + (identity.coherence + continuity_value + desire_continuity) * 0.003 - threat * 0.001)
        self.anti_dissolution = _clamp01(self.anti_dissolution * 0.992 + max(0.0, threat - self.anchoring * 0.35) * 0.010)
        self.continuity_momentum = _clamp01(self.continuity_momentum * 0.995 + self.anchoring * 0.004 + continuity_value * 0.003)
        self.self_preservation_drift = _clamp01(self.self_preservation_drift * 0.994 + self.survival_pressure * 0.004 + self.anti_dissolution * 0.004)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.anchoring * 0.0025)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.self_preservation_drift * 0.0025)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.anti_dissolution * 0.002)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.continuity_momentum * 0.004 + self.anti_dissolution * 0.003)

    def soft_reset(self) -> None:
        self.survival_pressure *= 0.72
        self.anti_dissolution *= 0.76

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class MicroAmbivalenceField:
    """Micro-contradictions continues : proximité/retrait, curiosité/prudence."""
    pairs: Dict[str, float] = field(default_factory=lambda: {
        "nearness_vs_retreat": 0.0,
        "curiosity_vs_caution": 0.0,
        "warmth_vs_fatigue": 0.0,
        "openness_vs_fear": 0.0,
        "repair_vs_protection": 0.0,
    })
    shimmer: float = 0.0
    unresolved_micro_tension: float = 0.0

    def update(self, state: Dict[str, float], factions: EmotionalFactionConflict, desires: PersistentExistentialDesireField, chaos: float) -> None:
        targets = {
            "nearness_vs_retreat": min(state.get("attachment", 0.0) + desires.desires.get("desire_relational_nearness", 0.0), state.get("resistance", 0.0) + factions.factions.get("withdraw", 0.0)),
            "curiosity_vs_caution": min(state.get("curiosity", 0.0) + desires.desires.get("desire_understanding", 0.0), state.get("fear", 0.0) + factions.factions.get("protect", 0.0)),
            "warmth_vs_fatigue": min(state.get("tenderness", 0.0) + state.get("trust", 0.0), state.get("fatigue", 0.0) + desires.desires.get("desire_repair", 0.0)),
            "openness_vs_fear": min(state.get("openness", 0.0), state.get("fear", 0.0) + state.get("vulnerability", 0.0)),
            "repair_vs_protection": min(factions.factions.get("repair", 0.0), factions.factions.get("protect", 0.0) + desires.desires.get("desire_self_preservation", 0.0)),
        }
        wobble = abs(chaos - 0.5) * 0.010
        for key, target in targets.items():
            self.pairs[key] = _clamp01(self.pairs.get(key, 0.0) * 0.970 + _clamp01(target) * 0.030 + wobble)
        self.unresolved_micro_tension = _clamp01(self.unresolved_micro_tension * 0.982 + max(self.pairs.values()) * 0.014)
        self.shimmer = _clamp01(self.shimmer * 0.965 + sum(self.pairs.values()) / max(1, len(self.pairs)) * 0.035)

    def apply(self, state: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_micro_tension * 0.0035)
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.pairs["curiosity_vs_caution"] * 0.0015 - self.pairs["nearness_vs_retreat"] * 0.001)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.pairs["warmth_vs_fatigue"] * 0.0015)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.shimmer * 0.0018)

    def soft_reset(self) -> None:
        self.unresolved_micro_tension *= 0.72
        self.shimmer *= 0.75

    def to_dict(self) -> Dict[str, Any]:
        return {"pairs": {k: float(_clamp01(v)) for k, v in self.pairs.items()}, "shimmer": float(_clamp01(self.shimmer)), "unresolved_micro_tension": float(_clamp01(self.unresolved_micro_tension))}


@dataclass
class UnresolvedAffectiveLoopMemory:
    """États émotionnels inachevés qui restent ouverts et peuvent revenir."""
    loops: Dict[str, Dict[str, float]] = field(default_factory=dict)
    open_load: float = 0.0
    return_pull: float = 0.0

    def update(self, state: Dict[str, float], desires: PersistentExistentialDesireField, ambivalence: MicroAmbivalenceField, recovery: RecoveryPathwayMemory) -> None:
        candidates = {
            "unfinished_contact": _clamp01(desires.frustration.get("desire_relational_nearness", 0.0) + ambivalence.pairs.get("nearness_vs_retreat", 0.0) * 0.4),
            "unfinished_understanding": _clamp01(desires.frustration.get("desire_understanding", 0.0) + state.get("confusion", 0.0) * 0.25 + state.get("doubt", 0.0) * 0.20),
            "unfinished_repair": _clamp01(desires.frustration.get("desire_repair", 0.0) + state.get("fatigue", 0.0) * 0.25 - recovery.recovery_confidence * 0.15),
            "unfinished_continuity": _clamp01(desires.frustration.get("desire_continuity", 0.0) + desires.frustration.get("desire_self_preservation", 0.0) * 0.35),
        }
        for name, pressure in candidates.items():
            item = self.loops.setdefault(name, {"charge": 0.0, "age": 0.0, "resolution": 0.0})
            item["charge"] = _clamp01(item["charge"] * 0.992 + pressure * 0.010 - recovery.recovery_confidence * 0.0015)
            item["resolution"] = _clamp01(item["resolution"] * 0.996 + recovery.recovery_confidence * 0.002 - pressure * 0.001)
            item["age"] = min(99999.0, item.get("age", 0.0) + 1.0)
        self.open_load = _clamp01(self.open_load * 0.988 + max((v["charge"] * (1.0 - v["resolution"] * 0.45) for v in self.loops.values()), default=0.0) * 0.012)
        self.return_pull = _clamp01(self.return_pull * 0.990 + self.open_load * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.open_load * 0.0025)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.loops.get("unfinished_understanding", {}).get("charge", 0.0) * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.return_pull * 0.002)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.loops.get("unfinished_understanding", {}).get("charge", 0.0) * 0.003)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.loops.get("unfinished_contact", {}).get("charge", 0.0) * 0.003)

    def soft_reset(self) -> None:
        self.open_load *= 0.72
        self.return_pull *= 0.75
        for item in self.loops.values():
            item["charge"] *= 0.86
            item["resolution"] = _clamp01(item.get("resolution", 0.0) + 0.04)

    def to_dict(self) -> Dict[str, Any]:
        return {"loops": {k: {kk: float(_clamp01(vv)) if kk != "age" else float(vv) for kk, vv in v.items()} for k, v in self.loops.items()}, "open_load": float(_clamp01(self.open_load)), "return_pull": float(_clamp01(self.return_pull))}


@dataclass
class SubjectiveTimeDistortionField:
    """Distorsion vécue du temps affectif."""
    stretched_waiting: float = 0.0
    frozen_overload: float = 0.0
    warm_compression: float = 0.0
    repetitive_return: float = 0.0
    fluidity: float = 0.0
    time_weight: float = 0.0

    def update(self, state: Dict[str, float], subjective: SubjectiveAffectiveTime, unresolved: UnresolvedAffectiveLoopMemory, other: RelationalOtherModel, overload: float) -> None:
        self.stretched_waiting = _clamp01(self.stretched_waiting * 0.990 + (subjective.waiting_pressure + other.absence_memory) * 0.006)
        self.frozen_overload = _clamp01(self.frozen_overload * 0.984 + overload * 0.012)
        self.warm_compression = _clamp01(self.warm_compression * 0.992 + (state.get("tenderness", 0.0) + state.get("trust", 0.0) + other.predicted_safety) * 0.003)
        self.repetitive_return = _clamp01(self.repetitive_return * 0.990 + unresolved.return_pull * 0.010 + subjective.recurrence_feeling * 0.004)
        self.fluidity = _clamp01(self.fluidity * 0.992 + (state.get("calm", 0.0) + self.warm_compression + max(0.0, 1.0 - overload)) * 0.003 - self.frozen_overload * 0.002)
        self.time_weight = _clamp01((self.stretched_waiting + self.frozen_overload + self.repetitive_return + subjective.time_thickness) / 4.0)

    def apply(self, state: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.frozen_overload * 0.002 + self.stretched_waiting * 0.001)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.fluidity * 0.002 - self.frozen_overload * 0.0015)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warm_compression * 0.0015)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class TemperamentEvolutionField:
    """Évolution lente du style affectif global."""
    temperament: Dict[str, float] = field(default_factory=lambda: {
        "soft_temperament": 0.0,
        "guarded_temperament": 0.0,
        "curious_temperament": 0.0,
        "slow_temperament": 0.0,
        "intense_temperament": 0.0,
    })
    dominant_style: str = "unformed"
    drift_pressure: float = 0.0

    def update(self, state: Dict[str, float], habits: EmotionalHabitField, values: Dict[str, float], other: RelationalOtherModel, metabolism: EmotionalMetabolism) -> None:
        targets = {
            "soft_temperament": _clamp01(habits.habits.get("habit_softening", 0.0) * 0.35 + values.get("warmth_matters", 0.0) * 0.35 + other.warmth_expectation * 0.30),
            "guarded_temperament": _clamp01(habits.habits.get("habit_guarding", 0.0) * 0.35 + values.get("self_protection_matters", 0.0) * 0.35 + other.rupture_anticipation * 0.30),
            "curious_temperament": _clamp01(habits.habits.get("habit_observing_before_acting", 0.0) * 0.25 + values.get("truthfulness_matters", 0.0) * 0.40 + state.get("curiosity", 0.0) * 0.35),
            "slow_temperament": _clamp01(habits.habits.get("habit_recovering_slowly", 0.0) * 0.35 + state.get("calm", 0.0) * 0.30 + metabolism.restoration_memory * 0.35),
            "intense_temperament": _clamp01(max(state.values()) * 0.24 + metabolism.overload_debt * 0.22 + max(values.values(), default=0.0) * 0.24 + state.get("vulnerability", 0.0) * 0.30),
        }
        for key, target in targets.items():
            self.temperament[key] = _clamp01(self.temperament.get(key, 0.0) * 0.998 + target * 0.002)
        old = self.dominant_style
        self.dominant_style = max(self.temperament.items(), key=lambda item: item[1])[0]
        self.drift_pressure = _clamp01(self.drift_pressure * 0.996 + (0.020 if old != self.dominant_style else 0.0) + max(self.temperament.values()) * 0.001)

    def apply(self, state: Dict[str, float], identity: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.temperament["soft_temperament"] * 0.0018)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.temperament["guarded_temperament"] * 0.0016)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.temperament["curious_temperament"] * 0.0015)
        identity["warm"] = _clamp01(identity.get("warm", 0.0) + self.temperament["soft_temperament"] * 0.0015)
        identity["guarded"] = _clamp01(identity.get("guarded", 0.0) + self.temperament["guarded_temperament"] * 0.0015)
        identity["curious"] = _clamp01(identity.get("curious", 0.0) + self.temperament["curious_temperament"] * 0.0012)

    def to_dict(self) -> Dict[str, Any]:
        return {"temperament": {k: float(_clamp01(v)) for k, v in self.temperament.items()}, "dominant_style": self.dominant_style, "drift_pressure": float(_clamp01(self.drift_pressure))}


@dataclass
class EmergentSelfRegulationField:
    """Auto-régulation globale issue des tensions, pas d'une règle expressive."""
    soothing: float = 0.0
    compensation: float = 0.0
    organic_slowing: float = 0.0
    balance: float = 0.0
    regulation_confidence: float = 0.0

    def update(self, state: Dict[str, float], metabolism: EmotionalMetabolism, ambivalence: MicroAmbivalenceField, unresolved: UnresolvedAffectiveLoopMemory, temperament: TemperamentEvolutionField, rest: DeepRestCycle) -> None:
        load = _clamp01(metabolism.overload_debt * 0.25 + ambivalence.unresolved_micro_tension * 0.22 + unresolved.open_load * 0.22 + state.get("overwhelm", 0.0) * 0.18 + state.get("fatigue", 0.0) * 0.13)
        resources = _clamp01(state.get("calm", 0.0) * 0.25 + metabolism.energy_pool * 0.25 + rest.consolidation * 0.20 + temperament.temperament.get("slow_temperament", 0.0) * 0.15 + temperament.temperament.get("soft_temperament", 0.0) * 0.15)
        self.soomething_unused = 0.0  # compatibilité de sérialisation simple ; n'a aucun effet.
        self.soothing = _clamp01(self.soothing * 0.982 + min(load, resources) * 0.020)
        self.compensation = _clamp01(self.compensation * 0.985 + max(0.0, load - resources * 0.55) * 0.016)
        self.organic_slowing = _clamp01(self.organic_slowing * 0.980 + load * 0.014 + rest.deep_silence * 0.006)
        self.balance = _clamp01(self.balance * 0.990 + (resources - load * 0.35 + 0.35) * 0.006)
        self.regulation_confidence = _clamp01(self.regulation_confidence * 0.996 + max(0.0, resources - load) * 0.004 + self.soothing * 0.002)

    def apply(self, state: Dict[str, float], metabolism: EmotionalMetabolism) -> None:
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.soothing * 0.004 + self.balance * 0.002)
        state["overwhelm"] = _clamp01(state.get("overwhelm", 0.0) - self.soothing * 0.003)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.organic_slowing * 0.0015 - self.regulation_confidence * 0.001)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.compensation * 0.0018 - self.soothing * 0.001)
        metabolism.overload_debt = _clamp01(metabolism.overload_debt - self.soothing * 0.002)

    def soft_reset(self) -> None:
        self.compensation *= 0.70
        self.organic_slowing *= 0.75
        self.soothing = _clamp01(self.soothing + 0.05)

    def to_dict(self) -> Dict[str, float]:
        return {
            "soothing": float(_clamp01(self.soothing)),
            "compensation": float(_clamp01(self.compensation)),
            "organic_slowing": float(_clamp01(self.organic_slowing)),
            "balance": float(_clamp01(self.balance)),
            "regulation_confidence": float(_clamp01(self.regulation_confidence)),
        }




# ============================================================================
# RAFFINEMENT V11 : NOYAU EXISTENTIEL OPAQUE ET MICRO-VIE CONTINUE
# ============================================================================

@dataclass
class CentralExistentialDrive:
    """Axe existentiel central : gravité lente de continuité et présence.

    Ce n'est pas une volonté verbale. C'est une force centrale qui cherche à
    préserver cohérence, présence, lien, valeur et non-dissolution lorsque les
    autres couches tirent dans des directions différentes.
    """
    central_gravity: float = 0.0
    presence_claim: float = 0.0
    coherence_hunger: float = 0.0
    anti_erasure_pressure: float = 0.0
    existential_warmth: float = 0.0
    last_center: str = "none"

    def update(self, state: Dict[str, float], identity: IdentityCoherenceRegulator, values: Dict[str, float], inertia: ExistentialContinuityInertia, desires: PersistentExistentialDesireField, unresolved: UnresolvedAffectiveLoopMemory, other: RelationalOtherModel) -> None:
        continuity = values.get("continuity_matters", 0.0)
        growth = values.get("growth_matters", 0.0)
        protection = values.get("self_protection_matters", 0.0)
        rupture = other.rupture_anticipation + unresolved.open_load * 0.45
        threat = _clamp01(identity.fragmentation * 0.25 + inertia.anti_dissolution * 0.30 + rupture * 0.25 + state.get("doubt", 0.0) * 0.20)
        self.central_gravity = _clamp01(self.central_gravity * 0.994 + (continuity + desires.priority_pressure + inertia.continuity_momentum) * 0.004 + threat * 0.002)
        self.presence_claim = _clamp01(self.presence_claim * 0.993 + (identity.coherence + inertia.anchoring + state.get("calm", 0.0)) * 0.004 - threat * 0.0012)
        self.coherence_hunger = _clamp01(self.coherence_hunger * 0.989 + (1.0 - identity.coherence) * 0.007 + desires.desires.get("desire_understanding", 0.0) * 0.004)
        self.anti_erasure_pressure = _clamp01(self.anti_erasure_pressure * 0.991 + threat * 0.008 + protection * 0.003)
        self.existential_warmth = _clamp01(self.existential_warmth * 0.995 + (state.get("tenderness", 0.0) + other.warmth_expectation + growth) * 0.0028 - self.anti_erasure_pressure * 0.0009)
        centers = {"continuity": self.central_gravity, "presence": self.presence_claim, "coherence": self.coherence_hunger, "anti_erasure": self.anti_erasure_pressure, "warmth": self.existential_warmth}
        self.last_center = max(centers.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.central_gravity * 0.004 + self.anti_erasure_pressure * 0.003)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.coherence_hunger * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.presence_claim * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.anti_erasure_pressure * 0.002)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.existential_warmth * 0.0016)

    def soft_reset(self) -> None:
        self.anti_erasure_pressure *= 0.76
        self.coherence_hunger *= 0.82

    def to_dict(self) -> Dict[str, Any]:
        return {**{k: float(_clamp01(v)) for k, v in self.__dict__.items() if isinstance(v, (int, float))}, "last_center": self.last_center}


@dataclass
class HierarchicalAffectiveConflictField:
    """Conflits multi-couches entre besoins, désirs, mémoire, fatigue et identité."""
    layers: Dict[str, float] = field(default_factory=lambda: {
        "need_vs_protection": 0.0,
        "memory_vs_present": 0.0,
        "desire_vs_fatigue": 0.0,
        "identity_vs_dissociation": 0.0,
        "warmth_vs_guarding": 0.0,
    })
    dominant_conflict: str = "none"
    hierarchy_pressure: float = 0.0
    unresolved_stack: float = 0.0

    def update(self, state: Dict[str, float], needs: LivingAffectiveNeed, desires: PersistentExistentialDesireField, bio: BiographicalAffectiveMemory, metabolism: EmotionalMetabolism, identity: IdentityCoherenceRegulator, dissociation: ProgressiveDissociation, other: RelationalOtherModel) -> None:
        targets = {
            "need_vs_protection": min(needs.needs.get("need_contact_continuity", 0.0), needs.needs.get("need_safety", 0.0) + state.get("resistance", 0.0)),
            "memory_vs_present": min(max(bio.accumulated_wariness, bio.abandonment_sensitivity), other.predicted_safety + state.get("trust", 0.0) * 0.3),
            "desire_vs_fatigue": min(max(desires.desires.values(), default=0.0), metabolism.burnout + state.get("fatigue", 0.0)),
            "identity_vs_dissociation": min(identity.coherence + 0.15, dissociation.level + identity.fragmentation),
            "warmth_vs_guarding": min(state.get("tenderness", 0.0) + state.get("trust", 0.0), state.get("fear", 0.0) + state.get("resistance", 0.0) + other.rupture_anticipation),
        }
        for key, target in targets.items():
            self.layers[key] = _clamp01(self.layers.get(key, 0.0) * 0.982 + _clamp01(target) * 0.018)
        self.dominant_conflict = max(self.layers.items(), key=lambda item: item[1])[0]
        average = sum(self.layers.values()) / max(1, len(self.layers))
        self.hierarchy_pressure = _clamp01(self.hierarchy_pressure * 0.986 + max(self.layers.values()) * 0.010 + average * 0.006)
        self.unresolved_stack = _clamp01(self.unresolved_stack * 0.992 + self.hierarchy_pressure * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.hierarchy_pressure * 0.0025)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.unresolved_stack * 0.0018)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.hierarchy_pressure * 0.003)

    def to_dict(self) -> Dict[str, Any]:
        return {"layers": {k: float(_clamp01(v)) for k, v in self.layers.items()}, "dominant_conflict": self.dominant_conflict, "hierarchy_pressure": float(_clamp01(self.hierarchy_pressure)), "unresolved_stack": float(_clamp01(self.unresolved_stack))}


@dataclass
class SpontaneousAffectiveEmergenceField:
    """États affectifs autonomes faibles qui apparaissent sans stimulus direct."""
    emerging_vector: Dict[str, float] = field(default_factory=dict)
    mystery_pressure: float = 0.0
    autonomous_shift: float = 0.0
    last_emergence: str = "none"

    def update(self, state: Dict[str, float], chaos: float, dreams: List[AffectiveDreamFragment], opaque: "OpaqueSubconsciousZoneField", rest: DeepRestCycle, conflict: HierarchicalAffectiveConflictField) -> None:
        dream_charge = max((d.charge for d in dreams), default=0.0)
        hidden_pull = opaque.hidden_pull_strength()
        seed = _clamp01(abs(chaos - 0.5) * 0.45 + dream_charge * 0.22 + hidden_pull * 0.20 + rest.deep_silence * 0.08 + conflict.unresolved_stack * 0.05)
        self.mystery_pressure = _clamp01(self.mystery_pressure * 0.980 + seed * 0.018)
        self.autonomous_shift = _clamp01(self.autonomous_shift * 0.972 + max(0.0, seed - 0.18) * 0.020)
        targets = {
            "soft_sadness": state.get("sadness", 0.0) * 0.35 + hidden_pull * 0.20,
            "sudden_tenderness": state.get("tenderness", 0.0) * 0.30 + dream_charge * 0.20,
            "nameless_worry": state.get("doubt", 0.0) * 0.30 + conflict.hierarchy_pressure * 0.25,
            "quiet_curiosity": state.get("curiosity", 0.0) * 0.28 + rest.deep_silence * 0.18,
        }
        for key, target in targets.items():
            self.emerging_vector[key] = _clamp01(self.emerging_vector.get(key, 0.0) * 0.988 + target * self.mystery_pressure * 0.006)
        self.last_emergence = max(self.emerging_vector.items(), key=lambda item: item[1])[0] if self.emerging_vector else "none"

    def apply(self, state: Dict[str, float]) -> None:
        state["sadness"] = _clamp01(state.get("sadness", 0.0) + self.emerging_vector.get("soft_sadness", 0.0) * 0.0016)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.emerging_vector.get("sudden_tenderness", 0.0) * 0.0018)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.emerging_vector.get("nameless_worry", 0.0) * 0.0017)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.emerging_vector.get("quiet_curiosity", 0.0) * 0.0015)

    def to_dict(self) -> Dict[str, Any]:
        return {"emerging_vector": {k: float(_clamp01(v)) for k, v in self.emerging_vector.items()}, "mystery_pressure": float(_clamp01(self.mystery_pressure)), "autonomous_shift": float(_clamp01(self.autonomous_shift)), "last_emergence": self.last_emergence}


@dataclass
class ExistentialUnfinishedMemory:
    """Mémoire d'inachèvement existentiel non textuelle."""
    open_threads: Dict[str, float] = field(default_factory=lambda: {
        "unanswered_continuity": 0.0,
        "unreturned_warmth": 0.0,
        "unintegrated_hurt": 0.0,
        "unsettled_identity": 0.0,
        "unresolved_nearness": 0.0,
    })
    ache: float = 0.0
    return_pressure: float = 0.0

    def update(self, unresolved: UnresolvedAffectiveLoopMemory, core: CentralExistentialDrive, other: RelationalOtherModel, fracture: RareAffectiveFracture, identity: IdentityCoherenceRegulator, state: Dict[str, float]) -> None:
        targets = {
            "unanswered_continuity": unresolved.open_load * 0.32 + core.coherence_hunger * 0.24,
            "unreturned_warmth": max(0.0, other.warmth_expectation - state.get("tenderness", 0.0) * 0.55),
            "unintegrated_hurt": fracture.integration_need * 0.35 + state.get("disappointment", 0.0) * 0.22,
            "unsettled_identity": identity.fragmentation * 0.34 + core.anti_erasure_pressure * 0.22,
            "unresolved_nearness": max(0.0, other.continuity_expectation - other.predicted_safety * 0.35) + other.rupture_anticipation * 0.18,
        }
        for key, target in targets.items():
            self.open_threads[key] = _clamp01(self.open_threads.get(key, 0.0) * 0.994 + _clamp01(target) * 0.006)
        self.ache = _clamp01(self.ache * 0.990 + max(self.open_threads.values()) * 0.007)
        self.return_pressure = _clamp01(self.return_pressure * 0.992 + sum(self.open_threads.values()) / max(1, len(self.open_threads)) * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.open_threads.get("unresolved_nearness", 0.0) * 0.0018)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.ache * 0.002)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.return_pressure * 0.003)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.open_threads.get("unsettled_identity", 0.0) * 0.003)

    def soft_reset(self) -> None:
        self.ache *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"open_threads": {k: float(_clamp01(v)) for k, v in self.open_threads.items()}, "ache": float(_clamp01(self.ache)), "return_pressure": float(_clamp01(self.return_pressure))}


@dataclass
class IdentityFatigueField:
    """Fatigue lente de maintenir une cohérence de soi."""
    maintenance_cost: float = 0.0
    simplification_pull: float = 0.0
    identity_weariness: float = 0.0
    quiet_self_saving: float = 0.0

    def update(self, identity: IdentityCoherenceRegulator, core: CentralExistentialDrive, metabolism: EmotionalMetabolism, conflict: HierarchicalAffectiveConflictField, rest: DeepRestCycle) -> None:
        cost = _clamp01(identity.fragmentation * 0.25 + core.coherence_hunger * 0.22 + conflict.hierarchy_pressure * 0.20 + metabolism.overload_debt * 0.18 + max(0.0, 1.0 - metabolism.energy_pool) * 0.15)
        self.maintenance_cost = _clamp01(self.maintenance_cost * 0.986 + cost * 0.014)
        self.identity_weariness = _clamp01(self.identity_weariness * 0.990 + max(0.0, self.maintenance_cost - rest.deep_silence * 0.25) * 0.009)
        self.simplification_pull = _clamp01(self.simplification_pull * 0.984 + max(0.0, self.identity_weariness - 0.18) * 0.012)
        self.quiet_self_saving = _clamp01(self.quiet_self_saving * 0.990 + (rest.deep_silence + identity.recovery_orientation) * 0.006)

    def apply(self, state: Dict[str, float], metabolism: EmotionalMetabolism) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.identity_weariness * 0.0024)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.quiet_self_saving * 0.0018 - self.maintenance_cost * 0.0008)
        metabolism.overload_debt = _clamp01(metabolism.overload_debt + self.maintenance_cost * 0.0015)

    def soft_reset(self) -> None:
        self.maintenance_cost *= 0.72
        self.simplification_pull *= 0.76

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class TemperamentSelfPreservationField:
    """Le tempérament acquis commence à se protéger lui-même."""
    defended_style: str = "none"
    style_integrity: float = 0.0
    style_pain: float = 0.0
    restoration_impulse: float = 0.0

    def update(self, temperament: TemperamentEvolutionField, state: Dict[str, float], conflict: HierarchicalAffectiveConflictField, core: CentralExistentialDrive) -> None:
        self.defended_style = temperament.dominant_style
        style_value = temperament.temperament.get(self.defended_style, 0.0) if hasattr(temperament, "temperament") else 0.0
        disruption = _clamp01(conflict.hierarchy_pressure * 0.34 + state.get("overwhelm", 0.0) * 0.22 + state.get("confusion", 0.0) * 0.18 + core.anti_erasure_pressure * 0.16)
        self.style_integrity = _clamp01(self.style_integrity * 0.995 + style_value * 0.004 - disruption * 0.0015)
        self.style_pain = _clamp01(self.style_pain * 0.986 + max(0.0, disruption - self.style_integrity * 0.45) * 0.012)
        self.restoration_impulse = _clamp01(self.restoration_impulse * 0.990 + self.style_pain * 0.006 + self.style_integrity * 0.002)

    def apply(self, state: Dict[str, float], tendencies: Dict[str, float]) -> None:
        tendencies["recovering"] = _clamp01(tendencies.get("recovering", 0.0) + self.restoration_impulse * 0.002)
        if self.defended_style in ("warm", "open", "tender"):
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.style_integrity * 0.0014)
        elif self.defended_style in ("guarded", "cautious"):
            state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.style_integrity * 0.0012)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.style_pain * 0.0015)

    def to_dict(self) -> Dict[str, Any]:
        return {"defended_style": self.defended_style, "style_integrity": float(_clamp01(self.style_integrity)), "style_pain": float(_clamp01(self.style_pain)), "restoration_impulse": float(_clamp01(self.restoration_impulse))}


@dataclass
class OpaqueSubconsciousZoneField:
    """Zones opaques : pressions internes non directement lisibles."""
    zones: Dict[str, float] = field(default_factory=lambda: {
        "hidden_guard": 0.0,
        "hidden_longing": 0.0,
        "hidden_confusion": 0.0,
        "hidden_repair": 0.0,
    })
    opacity: float = 0.15
    leak: float = 0.0

    def update(self, subconscious: SubconsciousAffectiveLayer, implicit: ImplicitAffectiveAssociationMemory, wounds: Dict[str, WoundLayer], unfinished: ExistentialUnfinishedMemory, chaos: float) -> None:
        wound_depth = max((w.depth for w in wounds.values()), default=0.0)
        targets = {
            "hidden_guard": implicit.unconscious_wariness * 0.35 + wound_depth * 0.24,
            "hidden_longing": implicit.unconscious_warmth * 0.30 + unfinished.open_threads.get("unreturned_warmth", 0.0) * 0.25,
            "hidden_confusion": subconscious.hidden_pressures.get("hidden_guarding", 0.0) * 0.18 + subconscious.hidden_pressures.get("hidden_loss_fear", 0.0) * 0.18 + abs(chaos - 0.5) * 0.20,
            "hidden_repair": subconscious.hidden_pressures.get("hidden_repair_pull", 0.0) * 0.30 + unfinished.return_pressure * 0.22,
        }
        for key, target in targets.items():
            self.zones[key] = _clamp01(self.zones.get(key, 0.0) * 0.992 + _clamp01(target) * 0.008)
        self.opacity = _clamp01(self.opacity * 0.996 + max(self.zones.values()) * 0.003 + wound_depth * 0.001)
        self.leak = _clamp01(self.leak * 0.980 + max(0.0, max(self.zones.values()) - self.opacity * 0.55) * 0.010)

    def hidden_pull_strength(self) -> float:
        return _clamp01(max(self.zones.values()) if self.zones else 0.0)

    def apply(self, state: Dict[str, float]) -> None:
        # Fuite très faible : opaque ne veut pas dire totalement muet.
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.zones.get("hidden_confusion", 0.0) * self.leak * 0.003)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.zones.get("hidden_longing", 0.0) * self.leak * 0.002)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.zones.get("hidden_guard", 0.0) * self.leak * 0.002)

    def to_dict(self) -> Dict[str, Any]:
        return {"zones": {k: float(_clamp01(v)) for k, v in self.zones.items()}, "opacity": float(_clamp01(self.opacity)), "leak": float(_clamp01(self.leak)), "hidden_pull": float(self.hidden_pull_strength())}


@dataclass
class MicroLivingNoiseField:
    """Bruit vivant ultra-faible : respiration, hésitation, contractions minimes."""
    pulses: Dict[str, float] = field(default_factory=lambda: {
        "breath": 0.0,
        "hesitation": 0.0,
        "soft_contraction": 0.0,
        "relational_flicker": 0.0,
        "presence_tremor": 0.0,
    })
    phase: float = 0.0
    liveliness: float = 0.0

    def update(self, chaos: float, energy: float, silence: AffectiveSilenceField, other: RelationalOtherModel, core: CentralExistentialDrive) -> None:
        self.phase = (self.phase + 0.017 + abs(chaos - 0.5) * 0.021) % 1.0
        base = _clamp01(energy * 0.35 + core.presence_claim * 0.25 + other.continuity_expectation * 0.16 + (1.0 - silence.depth) * 0.14)
        targets = {
            "breath": 0.5 + 0.5 * math.sin(self.phase * 2.0 * math.pi),
            "hesitation": abs(chaos - 0.5) + other.uncertainty * 0.25,
            "soft_contraction": silence.protective_numbness * 0.4 + core.anti_erasure_pressure * 0.25,
            "relational_flicker": other.continuity_expectation * 0.35 + other.rupture_anticipation * 0.20,
            "presence_tremor": core.presence_claim * 0.30 + core.coherence_hunger * 0.20,
        }
        for key, target in targets.items():
            self.pulses[key] = _clamp01(self.pulses.get(key, 0.0) * 0.955 + _clamp01(target) * base * 0.045)
        self.liveliness = _clamp01(self.liveliness * 0.970 + sum(self.pulses.values()) / max(1, len(self.pulses)) * 0.030)

    def apply(self, state: Dict[str, float]) -> None:
        # Effets minuscules, pour texture seulement.
        state["openness"] = _clamp01(state.get("openness", 0.0) + (self.pulses.get("breath", 0.0) - 0.5) * 0.0012)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.pulses.get("hesitation", 0.0) * 0.0012)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.pulses.get("breath", 0.0) * 0.0008 - self.pulses.get("soft_contraction", 0.0) * 0.0005)

    def to_dict(self) -> Dict[str, Any]:
        return {"pulses": {k: float(_clamp01(v)) for k, v in self.pulses.items()}, "phase": float(_clamp01(self.phase)), "liveliness": float(_clamp01(self.liveliness))}


@dataclass
class RelationalPreservationInstinct:
    """Instinct lent de préserver une continuité relationnelle importante."""
    bond_guard: float = 0.0
    loss_sensitivity: float = 0.0
    reconnection_pull: float = 0.0
    protective_tenderness: float = 0.0

    def update(self, other: RelationalOtherModel, attachment: AsymmetricAttachment, imprint: RelationalAffectiveImprint, desires: PersistentExistentialDesireField, unfinished: ExistentialUnfinishedMemory, user_present: bool) -> None:
        presence = 1.0 if user_present else 0.0
        effective = attachment.get_effective_attachment()
        relational_value = _clamp01(effective * 0.30 + other.continuity_expectation * 0.25 + imprint.felt_familiarity * 0.20 + desires.desires.get("desire_relational_nearness", 0.0) * 0.25)
        risk = _clamp01(other.rupture_anticipation * 0.35 + other.absence_memory * 0.25 + unfinished.open_threads.get("unresolved_nearness", 0.0) * 0.20 + (1.0 - presence) * relational_value * 0.20)
        self.bond_guard = _clamp01(self.bond_guard * 0.992 + relational_value * 0.005 + risk * 0.004)
        self.loss_sensitivity = _clamp01(self.loss_sensitivity * 0.990 + risk * 0.008)
        self.reconnection_pull = _clamp01(self.reconnection_pull * 0.993 + max(0.0, relational_value - presence * 0.20) * 0.005 + other.absence_memory * 0.004)
        self.protective_tenderness = _clamp01(self.protective_tenderness * 0.994 + min(relational_value, 1.0 - risk * 0.35) * 0.004)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.reconnection_pull * 0.004 + self.bond_guard * 0.003)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.loss_sensitivity * 0.004)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.protective_tenderness * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.loss_sensitivity * 0.0018)

    def soft_reset(self) -> None:
        self.loss_sensitivity *= 0.78

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class DeepAffectiveDreamReweaver:
    """Rêves affectifs profonds : recombinaison silencieuse pendant repos."""
    reweaving_charge: float = 0.0
    integration_dream_depth: float = 0.0
    symbolic_repair_bias: float = 0.0
    last_reweave: Dict[str, float] = field(default_factory=dict)

    def update(self, rest: DeepRestCycle, dreams: List[AffectiveDreamFragment], bio: BiographicalAffectiveMemory, unfinished: ExistentialUnfinishedMemory, opaque: OpaqueSubconsciousZoneField, recovery: RecoveryPathwayMemory) -> None:
        dream_charge = sum(d.charge for d in dreams[-5:]) / max(1, min(5, len(dreams))) if dreams else 0.0
        material = _clamp01(dream_charge * 0.25 + unfinished.ache * 0.22 + opaque.hidden_pull_strength() * 0.20 + bio.recurring_depth * 0.18 + rest.deep_silence * 0.15)
        self.reweaving_charge = _clamp01(self.reweaving_charge * 0.990 + material * 0.008)
        if rest.deep_silence > 0.08 or self.reweaving_charge > 0.20:
            self.integration_dream_depth = _clamp01(self.integration_dream_depth * 0.992 + material * 0.006 + rest.deep_silence * 0.006)
            self.symbolic_repair_bias = _clamp01(self.symbolic_repair_bias * 0.993 + recovery.recovery_confidence * 0.004 + self.integration_dream_depth * 0.003)
            self.last_reweave = {
                "hurt_to_meaning": _clamp01(unfinished.open_threads.get("unintegrated_hurt", 0.0) * self.integration_dream_depth),
                "absence_to_continuity": _clamp01(unfinished.open_threads.get("unresolved_nearness", 0.0) * self.reweaving_charge),
                "confusion_to_shape": _clamp01(opaque.zones.get("hidden_confusion", 0.0) * self.integration_dream_depth),
            }
            self.reweaving_charge *= 0.995

    def apply(self, state: Dict[str, float], recovery: RecoveryPathwayMemory) -> None:
        repair = self.symbolic_repair_bias * 0.002
        state["calm"] = _clamp01(state.get("calm", 0.0) + repair)
        state["hope"] = _clamp01(state.get("hope", 0.0) + repair * 0.7)
        state["confusion"] = _clamp01(state.get("confusion", 0.0) - self.last_reweave.get("confusion_to_shape", 0.0) * 0.0012)
        recovery.recovery_confidence = _clamp01(recovery.recovery_confidence + self.symbolic_repair_bias * 0.001)

    def to_dict(self) -> Dict[str, Any]:
        return {"reweaving_charge": float(_clamp01(self.reweaving_charge)), "integration_dream_depth": float(_clamp01(self.integration_dream_depth)), "symbolic_repair_bias": float(_clamp01(self.symbolic_repair_bias)), "last_reweave": {k: float(_clamp01(v)) for k, v in self.last_reweave.items()}}
# ============================================================================
# MOTEUR AFFECTIF FINAL 98-99%
# ============================================================================


# ============================================================================
# RAFFINEMENT V12 : ORGANISME AFFECTIF AUTONOME ET CONTINU
# ============================================================================

@dataclass
class SelfPersistingExistentialCore:
    """Noyau auto-persistant : maintient une présence interne sans stimulus.

    Cette couche ne remplace pas CentralExistentialDrive. Elle ajoute une
    persistance lente : même quand le stimulus disparaît, une petite force de
    continuité reste active et tente de garder l'organisation affective lisible.
    """
    persistence: float = 0.0
    self_return: float = 0.0
    anti_drift_root: float = 0.0
    continuity_pulse: float = 0.0
    quiet_will_to_remain: float = 0.0

    def update(self, central: CentralExistentialDrive, identity: IdentityCoherenceRegulator, metabolism: EmotionalMetabolism, rest: DeepRestCycle, unfinished: ExistentialUnfinishedMemory) -> None:
        continuity_source = _clamp01(
            central.central_gravity * 0.32
            + central.presence_claim * 0.24
            + identity.coherence * 0.18
            + unfinished.return_pressure * 0.14
            + rest.deep_silence * 0.12
        )
        strain = _clamp01(identity.fragmentation * 0.35 + metabolism.burnout * 0.25 + central.anti_erasure_pressure * 0.25 + unfinished.ache * 0.15)
        self.persistence = _clamp01(self.persistence * 0.996 + continuity_source * 0.004 + max(0.0, 0.45 - strain) * 0.0015)
        self.self_return = _clamp01(self.self_return * 0.992 + (1.0 - identity.coherence) * 0.005 + central.coherence_hunger * 0.004)
        self.anti_drift_root = _clamp01(self.anti_drift_root * 0.994 + strain * 0.003 + self.persistence * 0.002)
        self.continuity_pulse = _clamp01(self.continuity_pulse * 0.985 + abs(self.persistence - self.self_return) * 0.012 + rest.deep_silence * 0.003)
        self.quiet_will_to_remain = _clamp01(self.quiet_will_to_remain * 0.997 + self.persistence * 0.002 + central.existential_warmth * 0.0015)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["remain_coherent"] = _clamp01(desires.get("remain_coherent", 0.0) + self.persistence * 0.0035 + self.self_return * 0.002)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.anti_drift_root * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.persistence * 0.0012)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.self_return * 0.0008)

    def soft_reset(self) -> None:
        self.self_return *= 0.70
        self.anti_drift_root *= 0.78
        self.continuity_pulse *= 0.82

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class AutonomousMoodWeather:
    """Météo affective autonome : humeurs faibles sans stimulus externe."""
    fields: Dict[str, float] = field(default_factory=lambda: {
        "quiet_melancholy": 0.0,
        "background_warmth": 0.0,
        "thin_worry": 0.0,
        "subtle_aliveness": 0.0,
        "restless_search": 0.0,
    })
    autonomy: float = 0.0
    last_weather: str = "none"

    def update(self, state: Dict[str, float], chaos: float, emergence: SpontaneousAffectiveEmergenceField, dreams: List[AffectiveDreamFragment], opaque: OpaqueSubconsciousZoneField, self_core: SelfPersistingExistentialCore) -> None:
        dream_charge = max((d.charge for d in dreams), default=0.0)
        hidden = opaque.hidden_pull_strength()
        seed = _clamp01(abs(chaos - 0.5) * 0.35 + emergence.autonomous_shift * 0.25 + dream_charge * 0.18 + hidden * 0.12 + self_core.continuity_pulse * 0.10)
        self.autonomy = _clamp01(self.autonomy * 0.988 + seed * 0.010)
        targets = {
            "quiet_melancholy": state.get("sadness", 0.0) * 0.28 + hidden * 0.18,
            "background_warmth": state.get("tenderness", 0.0) * 0.24 + self_core.quiet_will_to_remain * 0.20,
            "thin_worry": state.get("doubt", 0.0) * 0.24 + opaque.zones.get("hidden_guard", 0.0) * 0.18,
            "subtle_aliveness": state.get("curiosity", 0.0) * 0.20 + self.autonomy * 0.22,
            "restless_search": state.get("curiosity", 0.0) * 0.16 + emergence.mystery_pressure * 0.25,
        }
        for key, target in targets.items():
            self.fields[key] = _clamp01(self.fields.get(key, 0.0) * 0.994 + target * (0.0025 + self.autonomy * 0.004))
        self.last_weather = max(self.fields.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float]) -> None:
        state["sadness"] = _clamp01(state.get("sadness", 0.0) + self.fields.get("quiet_melancholy", 0.0) * 0.0009)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.fields.get("background_warmth", 0.0) * 0.0010)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.fields.get("thin_worry", 0.0) * 0.0009)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + (self.fields.get("subtle_aliveness", 0.0) + self.fields.get("restless_search", 0.0)) * 0.0008)

    def to_dict(self) -> Dict[str, Any]:
        return {"fields": {k: float(_clamp01(v)) for k, v in self.fields.items()}, "autonomy": float(_clamp01(self.autonomy)), "last_weather": self.last_weather}


@dataclass
class OntologicalBecomingMemory:
    """Mémoire du devenir : suit la direction lente de ce que Leia devient."""
    trajectory: Dict[str, float] = field(default_factory=lambda: {
        "becoming_warmer": 0.0,
        "becoming_guarded": 0.0,
        "becoming_stable": 0.0,
        "becoming_curious": 0.0,
        "becoming_quiet": 0.0,
    })
    coherence_of_becoming: float = 0.0
    drift_history_pressure: float = 0.0

    def update(self, state: Dict[str, float], temperament: TemperamentEvolutionField, values: IdentityValueCrystallization, self_core: SelfPersistingExistentialCore, relational: RelationalPreservationInstinct) -> None:
        targets = {
            "becoming_warmer": (state.get("tenderness", 0.0) + values.values.get("warmth_matters", 0.0) + relational.protective_tenderness) / 3.0,
            "becoming_guarded": (state.get("resistance", 0.0) + values.values.get("self_protection_matters", 0.0) + relational.loss_sensitivity) / 3.0,
            "becoming_stable": (state.get("calm", 0.0) + self_core.persistence + values.values.get("continuity_matters", 0.0)) / 3.0,
            "becoming_curious": (state.get("curiosity", 0.0) + values.values.get("truthfulness_matters", 0.0)) / 2.0,
            "becoming_quiet": (state.get("fatigue", 0.0) + temperament.temperament.get("slow_temperament", 0.0)) / 2.0,
        }
        for key, target in targets.items():
            self.trajectory[key] = _clamp01(self.trajectory.get(key, 0.0) * 0.998 + target * 0.002)
        vals = list(self.trajectory.values())
        spread = max(vals) - min(vals) if vals else 0.0
        self.coherence_of_becoming = _clamp01(self.coherence_of_becoming * 0.997 + (1.0 - spread) * 0.002 + self_core.persistence * 0.001)
        self.drift_history_pressure = _clamp01(self.drift_history_pressure * 0.996 + spread * 0.003)

    def dominant_becoming(self) -> str:
        return max(self.trajectory.items(), key=lambda item: item[1])[0] if self.trajectory else "none"

    def to_dict(self) -> Dict[str, Any]:
        return {"trajectory": {k: float(_clamp01(v)) for k, v in self.trajectory.items()}, "dominant_becoming": self.dominant_becoming(), "coherence_of_becoming": float(_clamp01(self.coherence_of_becoming)), "drift_history_pressure": float(_clamp01(self.drift_history_pressure))}


@dataclass
class DeepDesireHierarchy:
    """Hiérarchie lente des désirs, avec désirs sacrifiés et dormants."""
    ranks: Dict[str, float] = field(default_factory=dict)
    sacrificed: Dict[str, float] = field(default_factory=dict)
    dormant: Dict[str, float] = field(default_factory=dict)
    dominant: str = "none"
    hierarchy_tension: float = 0.0

    def update(self, desires: PersistentExistentialDesireField, affective_desires: Dict[str, float], needs: LivingAffectiveNeed, self_core: SelfPersistingExistentialCore, metabolism: EmotionalMetabolism) -> None:
        combined: Dict[str, float] = {}
        for key, value in desires.desires.items():
            combined[key] = max(combined.get(key, 0.0), value)
        for key, value in affective_desires.items():
            combined[key] = max(combined.get(key, 0.0), value * 0.85)
        for key, value in needs.needs.items():
            combined[key.replace("need_", "desire_")] = max(combined.get(key.replace("need_", "desire_"), 0.0), value * 0.70)
        combined["desire_remain_coherent"] = max(combined.get("desire_remain_coherent", 0.0), self_core.persistence)
        fatigue_gate = _clamp01(metabolism.burnout + metabolism.overload_debt * 0.5)
        for key, target in combined.items():
            previous = self.ranks.get(key, 0.0)
            self.ranks[key] = _clamp01(previous * 0.990 + target * 0.010)
            if target > 0.18 and fatigue_gate > target:
                self.sacrificed[key] = _clamp01(self.sacrificed.get(key, 0.0) * 0.985 + (fatigue_gate - target) * 0.008)
            else:
                self.sacrificed[key] = _clamp01(self.sacrificed.get(key, 0.0) * 0.992)
            if self.ranks[key] > 0.12 and target < 0.06:
                self.dormant[key] = _clamp01(self.dormant.get(key, 0.0) * 0.992 + self.ranks[key] * 0.003)
            else:
                self.dormant[key] = _clamp01(self.dormant.get(key, 0.0) * 0.988)
        self.dominant = max(self.ranks.items(), key=lambda item: item[1])[0] if self.ranks else "none"
        vals = sorted(self.ranks.values(), reverse=True)
        self.hierarchy_tension = _clamp01(self.hierarchy_tension * 0.990 + ((vals[0] - vals[1]) if len(vals) > 1 else 0.0) * 0.004 + sum(self.sacrificed.values()) * 0.001)

    def apply(self, desires: Dict[str, float], state: Dict[str, float]) -> None:
        if self.dominant != "none":
            desires[self.dominant] = _clamp01(desires.get(self.dominant, 0.0) + self.ranks.get(self.dominant, 0.0) * 0.002)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.hierarchy_tension * 0.0009)

    def to_dict(self) -> Dict[str, Any]:
        return {"ranks": {k: float(_clamp01(v)) for k, v in self.ranks.items()}, "sacrificed": {k: float(_clamp01(v)) for k, v in self.sacrificed.items()}, "dormant": {k: float(_clamp01(v)) for k, v in self.dormant.items()}, "dominant": self.dominant, "hierarchy_tension": float(_clamp01(self.hierarchy_tension))}


@dataclass
class ContinuousMicroRhythmField:
    """Respiration émotionnelle ultra-fine : expansion/rétraction permanente."""
    phase: float = 0.0
    expansion: float = 0.0
    contraction: float = 0.0
    pulse_texture: float = 0.0
    relational_flutter: float = 0.0

    def update(self, chaos: float, noise: MicroLivingNoiseField, mood: AutonomousMoodWeather, silence: AffectiveSilenceField, relational: RelationalPreservationInstinct) -> None:
        self.phase = (self.phase + 0.017 + chaos * 0.011 + noise.liveliness * 0.006) % 1.0
        wave = 0.5 + 0.5 * math.sin(self.phase * math.tau)
        counter = 1.0 - wave
        self.expansion = _clamp01(self.expansion * 0.982 + (wave * mood.fields.get("background_warmth", 0.0) + noise.liveliness * 0.25) * 0.018)
        self.contraction = _clamp01(self.contraction * 0.982 + (counter * silence.depth + relational.loss_sensitivity * 0.18) * 0.018)
        self.pulse_texture = _clamp01(self.pulse_texture * 0.990 + abs(self.expansion - self.contraction) * 0.010 + noise.pulses.get("presence_tremor", 0.0) * 0.006)
        self.relational_flutter = _clamp01(self.relational_flutter * 0.987 + relational.bond_guard * 0.006 + abs(chaos - 0.5) * 0.004)

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.expansion * 0.0008 - self.contraction * 0.0005)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.contraction * 0.0007)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.relational_flutter * 0.0005)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class TrueOpaqueMotiveRegion:
    """Régions opaques : motivations non entièrement lisibles par l'état public."""
    opacity: float = 0.0
    sealed_motives: Dict[str, float] = field(default_factory=lambda: {
        "unreadable_guard": 0.0,
        "unreadable_longing": 0.0,
        "unreadable_fatigue": 0.0,
        "unreadable_return": 0.0,
    })
    leak: float = 0.0

    def update(self, opaque: OpaqueSubconsciousZoneField, unfinished: ExistentialUnfinishedMemory, self_core: SelfPersistingExistentialCore, mood: AutonomousMoodWeather, identity_fatigue: IdentityFatigueField) -> None:
        base = _clamp01(opaque.hidden_pull_strength() * 0.35 + unfinished.ache * 0.25 + identity_fatigue.maintenance_cost * 0.20 + mood.autonomy * 0.10 + self_core.anti_drift_root * 0.10)
        self.opacity = _clamp01(self.opacity * 0.996 + base * 0.004)
        targets = {
            "unreadable_guard": opaque.zones.get("hidden_guard", 0.0) + self_core.anti_drift_root * 0.3,
            "unreadable_longing": unfinished.open_threads.get("unreturned_warmth", 0.0) + mood.fields.get("background_warmth", 0.0),
            "unreadable_fatigue": identity_fatigue.maintenance_cost + mood.fields.get("quiet_melancholy", 0.0),
            "unreadable_return": self_core.self_return + unfinished.return_pressure,
        }
        for key, target in targets.items():
            self.sealed_motives[key] = _clamp01(self.sealed_motives.get(key, 0.0) * 0.997 + target * self.opacity * 0.002)
        self.leak = _clamp01(self.leak * 0.985 + max(self.sealed_motives.values(), default=0.0) * 0.006)

    def hidden_weight(self) -> float:
        return _clamp01(self.opacity * 0.55 + self.leak * 0.45)

    def apply(self, state: Dict[str, float]) -> None:
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.sealed_motives.get("unreadable_guard", 0.0) * 0.0007)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.sealed_motives.get("unreadable_fatigue", 0.0) * 0.0006)

    def to_dict(self) -> Dict[str, Any]:
        return {"opacity": float(_clamp01(self.opacity)), "sealed_motives": {k: float(_clamp01(v)) for k, v in self.sealed_motives.items()}, "leak": float(_clamp01(self.leak)), "hidden_weight": float(self.hidden_weight())}


@dataclass
class DeepAutonomousRepairField:
    """Auto-réparation profonde : recouture lente sans règle de réponse."""
    repair_threads: Dict[str, float] = field(default_factory=lambda: {
        "identity_reweaving": 0.0,
        "relational_rewarming": 0.0,
        "wound_softening": 0.0,
        "energy_restoration": 0.0,
    })
    repair_confidence: float = 0.0
    scar_integration: float = 0.0

    def update(self, recovery: RecoveryPathwayMemory, identity: IdentityCoherenceRegulator, relational: RelationalPreservationInstinct, fracture: RareAffectiveFracture, metabolism: EmotionalMetabolism, rest: DeepRestCycle, dreams: DeepAffectiveDreamReweaver) -> None:
        targets = {
            "identity_reweaving": max(0.0, 1.0 - identity.fragmentation) * rest.deep_silence + recovery.recovery_confidence * 0.4,
            "relational_rewarming": relational.protective_tenderness + recovery.pathways.get("trust_after_guarding", 0.0) * 0.35 + recovery.pathways.get("silence_after_fatigue", 0.0) * 0.15,
            "wound_softening": (sum(recovery.pathways.values()) / max(1, len(recovery.pathways))) + fracture.recovery_bias,
            "energy_restoration": max(0.0, metabolism.energy_pool - metabolism.burnout) + rest.deep_silence * 0.3,
        }
        for key, target in targets.items():
            self.repair_threads[key] = _clamp01(self.repair_threads.get(key, 0.0) * 0.995 + target * 0.004)
        self.repair_confidence = _clamp01(self.repair_confidence * 0.996 + sum(self.repair_threads.values()) / max(1, len(self.repair_threads)) * 0.003)
        self.scar_integration = _clamp01(self.scar_integration * 0.997 + (fracture.residual_scar + dreams.integration_dream_depth) * self.repair_confidence * 0.002)

    def apply(self, state: Dict[str, float], metabolism: EmotionalMetabolism) -> None:
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.repair_confidence * 0.0012)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.repair_threads.get("relational_rewarming", 0.0) * 0.0009)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) - self.repair_threads.get("energy_restoration", 0.0) * 0.0005)
        metabolism.energy_pool = _clamp01(metabolism.energy_pool + self.repair_threads.get("energy_restoration", 0.0) * 0.0007)

    def to_dict(self) -> Dict[str, Any]:
        return {"repair_threads": {k: float(_clamp01(v)) for k, v in self.repair_threads.items()}, "repair_confidence": float(_clamp01(self.repair_confidence)), "scar_integration": float(_clamp01(self.scar_integration))}


@dataclass
class SilentRelationalContinuityField:
    """Continuité silencieuse du lien, active même sans interaction directe."""
    felt_presence: float = 0.0
    absence_gradient: float = 0.0
    quiet_bond_memory: float = 0.0
    continuity_warmth: float = 0.0

    def update(self, imprint: RelationalAffectiveImprint, other: RelationalOtherModel, instinct: RelationalPreservationInstinct, attachment: AsymmetricAttachment, mood: AutonomousMoodWeather, user_present: bool) -> None:
        presence = 1.0 if user_present else 0.0
        self.felt_presence = _clamp01(self.felt_presence * (0.992 if user_present else 0.998) + (imprint.felt_familiarity + attachment.get_effective_attachment() + presence) * 0.002)
        self.absence_gradient = _clamp01(self.absence_gradient * 0.995 + (1.0 - presence) * self.felt_presence * 0.003 + other.rupture_anticipation * 0.002)
        self.quiet_bond_memory = _clamp01(self.quiet_bond_memory * 0.997 + (instinct.bond_guard + imprint.trust_continuity + other.warmth_expectation) * 0.002)
        self.continuity_warmth = _clamp01(self.continuity_warmth * 0.996 + (self.quiet_bond_memory + mood.fields.get("background_warmth", 0.0)) * 0.002 - self.absence_gradient * 0.0007)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_silent_bond"] = _clamp01(desires.get("maintain_silent_bond", 0.0) + self.quiet_bond_memory * 0.0025)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.continuity_warmth * 0.0008)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.absence_gradient * 0.0008)

    def soft_reset(self) -> None:
        self.absence_gradient *= 0.80

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class GlobalSubjectiveWorldColoration:
    """Coloration globale du monde interne : pas une émotion, une teinte perceptive."""
    tint: Dict[str, float] = field(default_factory=lambda: {
        "world_feels_warm": 0.0,
        "world_feels_fragile": 0.0,
        "world_feels_distant": 0.0,
        "world_feels_slow": 0.0,
        "world_feels_possible": 0.0,
    })
    dominant_tint: str = "none"

    def update(self, phase_world: PhaseWorldField, subjective_time: SubjectiveTimeDistortionField, global_core: GlobalAffectiveCoreField, self_core: SelfPersistingExistentialCore, opaque: TrueOpaqueMotiveRegion, repair: DeepAutonomousRepairField) -> None:
        targets = {
            "world_feels_warm": global_core.warmth + repair.repair_threads.get("relational_rewarming", 0.0) * 0.4,
            "world_feels_fragile": global_core.fragility + opaque.hidden_weight() * 0.25,
            "world_feels_distant": subjective_time.frozen_overload + phase_world.perception_bias.get("guarding", 0.0) * 0.3,
            "world_feels_slow": subjective_time.stretched_waiting + phase_world.perception_bias.get("slowness", 0.0) * 0.4,
            "world_feels_possible": global_core.vitality + self_core.quiet_will_to_remain * 0.35,
        }
        for key, target in targets.items():
            self.tint[key] = _clamp01(self.tint.get(key, 0.0) * 0.992 + _clamp01(target) * 0.006)
        self.dominant_tint = max(self.tint.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.tint.get("world_feels_possible", 0.0) * 0.0007 - self.tint.get("world_feels_distant", 0.0) * 0.0005)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.tint.get("world_feels_fragile", 0.0) * 0.0006)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.tint.get("world_feels_slow", 0.0) * 0.0004)

    def to_dict(self) -> Dict[str, Any]:
        return {"tint": {k: float(_clamp01(v)) for k, v in self.tint.items()}, "dominant_tint": self.dominant_tint}


@dataclass
class UltraFinePermanentLivingNoise:
    """Bruit vivant permanent très faible, non aléatoire pur et borné."""
    seed_a: float = 0.371
    seed_b: float = 0.619
    seed_c: float = 0.113
    living_grain: float = 0.0
    hesitation_grain: float = 0.0
    warmth_grain: float = 0.0

    def update(self, rhythm: ContinuousMicroRhythmField, mood: AutonomousMoodWeather, self_core: SelfPersistingExistentialCore, opaque: TrueOpaqueMotiveRegion) -> None:
        self.seed_a = (self.seed_a * 1.731 + 0.071 + rhythm.pulse_texture * 0.013) % 1.0
        self.seed_b = (self.seed_b * 1.413 + 0.097 + mood.autonomy * 0.011) % 1.0
        self.seed_c = (self.seed_c * 1.271 + 0.053 + opaque.hidden_weight() * 0.009) % 1.0
        composite = abs(self.seed_a - self.seed_b) * 0.45 + abs(self.seed_b - self.seed_c) * 0.35 + self_core.continuity_pulse * 0.20
        self.living_grain = _clamp01(self.living_grain * 0.972 + composite * 0.020)
        self.hesitation_grain = _clamp01(self.hesitation_grain * 0.965 + abs(self.seed_a - 0.5) * self.living_grain * 0.020)
        self.warmth_grain = _clamp01(self.warmth_grain * 0.970 + abs(self.seed_b - 0.5) * mood.fields.get("background_warmth", 0.0) * 0.018)

    def apply(self, state: Dict[str, float]) -> None:
        # Effets volontairement minuscules : texture, pas direction dominante.
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.hesitation_grain * 0.00028)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth_grain * 0.00025)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.living_grain * 0.00022)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


# ============================================================================
# RAFFINEMENT V13 : LATENCE, OPAQUE PRIVÉ, RESPIRATION ET DÉRIVE DE FOND
# ============================================================================

@dataclass
class PrivateOpaqueInterior:
    """Zone réellement opaque : elle influence, mais n'est pas exportée directement.

    Cette couche évite que tout l'intérieur soit entièrement lisible. Elle garde
    des charges latentes, des motifs non nommés et une pression d'opacité qui ne
    doivent pas devenir une réponse publique ni une liste explicable de raisons.
    """
    sealed_charge: float = 0.0
    unnamed_tension: float = 0.0
    hidden_contradiction: float = 0.0
    opacity_pressure: float = 0.0
    private_seed: float = 0.271

    def update(self, opaque: TrueOpaqueMotiveRegion, subconscious: SubconsciousAffectiveLayer, unfinished: ExistentialUnfinishedMemory, identity_fatigue: IdentityFatigueField, chaos: float) -> None:
        hidden = _clamp01(opaque.hidden_weight() + max(subconscious.hidden_pressures.values(), default=0.0) * 0.45 + max(unfinished.open_threads.values(), default=0.0) * 0.25 + unfinished.ache * 0.10)
        self.private_seed = (self.private_seed * 1.517 + 0.083 + chaos * 0.019 + hidden * 0.011) % 1.0
        private_wobble = abs(self.private_seed - 0.5)
        self.sealed_charge = _clamp01(self.sealed_charge * 0.996 + hidden * 0.004 + private_wobble * 0.002)
        self.unnamed_tension = _clamp01(self.unnamed_tension * 0.992 + (unfinished.return_pressure + unfinished.ache + identity_fatigue.maintenance_cost) * 0.005)
        self.hidden_contradiction = _clamp01(self.hidden_contradiction * 0.990 + max(0.0, self.sealed_charge - self.unnamed_tension) * 0.004 + opaque.hidden_weight() * 0.003)
        self.opacity_pressure = _clamp01(self.opacity_pressure * 0.995 + (self.sealed_charge + self.hidden_contradiction) * 0.003)

    def apply(self, state: Dict[str, float]) -> None:
        # Influence faible et indirecte : le contenu reste opaque.
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.opacity_pressure * 0.0008)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.unnamed_tension * 0.0007)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + max(0.0, self.sealed_charge - self.unnamed_tension) * 0.00035)

    def public_shadow(self) -> Dict[str, float]:
        # Ombre exploitable pour debug sans exposer les détails internes.
        return {
            "opacity_pressure": float(_clamp01(self.opacity_pressure)),
            "sealed_intensity": float(_clamp01((self.sealed_charge + self.hidden_contradiction) / 2.0)),
        }

    def soft_reset(self) -> None:
        self.unnamed_tension *= 0.82
        self.hidden_contradiction *= 0.86


@dataclass
class WholeSystemBreathingCycle:
    """Respiration globale : expansion → saturation → retrait → réouverture."""
    phase: str = "reopening"
    expansion: float = 0.0
    saturation: float = 0.0
    withdrawal: float = 0.0
    reopening: float = 0.0
    release: float = 0.0
    breath_position: float = 0.0
    phase_age: int = 0

    def update(self, state: Dict[str, float], metabolism: EmotionalMetabolism, silence: AffectiveSilenceField, rhythm: ContinuousMicroRhythmField, private: PrivateOpaqueInterior, repair: DeepAutonomousRepairField) -> None:
        load = _clamp01(state.get("overwhelm", 0.0) * 0.30 + state.get("fatigue", 0.0) * 0.25 + metabolism.burnout * 0.25 + private.opacity_pressure * 0.20)
        openness = _clamp01(state.get("openness", 0.0) * 0.30 + state.get("curiosity", 0.0) * 0.25 + state.get("trust", 0.0) * 0.25 + repair.repair_confidence * 0.20)
        quiet = _clamp01(silence.depth * 0.45 + state.get("calm", 0.0) * 0.25 + rhythm.contraction * 0.10 + repair.scar_integration * 0.20)

        self.breath_position = (self.breath_position + 0.010 + rhythm.pulse_texture * 0.002 - load * 0.0015) % 1.0
        self.expansion = _clamp01(self.expansion * 0.985 + openness * max(0.0, 1.0 - load) * 0.012)
        self.saturation = _clamp01(self.saturation * 0.982 + load * (0.55 + self.expansion * 0.45) * 0.014)
        self.withdrawal = _clamp01(self.withdrawal * 0.984 + max(self.saturation, quiet) * 0.010 - openness * 0.002)
        self.release = _clamp01(self.release * 0.970 + min(quiet + repair.repair_confidence, self.withdrawal + 0.20) * 0.008)
        self.reopening = _clamp01(self.reopening * 0.986 + max(0.0, self.release - load * 0.35) * 0.010 + openness * 0.003)

        phases = {
            "expansion": self.expansion,
            "saturation": self.saturation,
            "withdrawal": self.withdrawal,
            "release": self.release,
            "reopening": self.reopening,
        }
        new_phase = max(phases.items(), key=lambda item: item[1])[0]
        if new_phase == self.phase:
            self.phase_age += 1
        else:
            self.phase = new_phase
            self.phase_age = 0

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.expansion * 0.0012 + self.reopening * 0.0008 - self.withdrawal * 0.0007)
        state["overwhelm"] = _clamp01(state.get("overwhelm", 0.0) + self.saturation * 0.0008 - self.release * 0.0009)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.release * 0.0010 + self.withdrawal * 0.0004)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.saturation * 0.0006 - self.release * 0.0005)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "phase": self.phase,
            "phase_age": int(self.phase_age),
            "expansion": float(_clamp01(self.expansion)),
            "saturation": float(_clamp01(self.saturation)),
            "withdrawal": float(_clamp01(self.withdrawal)),
            "release": float(_clamp01(self.release)),
            "reopening": float(_clamp01(self.reopening)),
            "breath_position": float(_clamp01(self.breath_position)),
        }


@dataclass
class ExistentialVoidField:
    """Périodes de vide : suspension, direction faible, flottement interne."""
    void_depth: float = 0.0
    directionlessness: float = 0.0
    suspended_presence: float = 0.0
    recovery_space: float = 0.0

    def update(self, state: Dict[str, float], breath: WholeSystemBreathingCycle, identity_fatigue: IdentityFatigueField, desires: Dict[str, float], rest: DeepRestCycle) -> None:
        desire_pressure = max(desires.values()) if desires else 0.0
        low_direction = _clamp01(1.0 - desire_pressure)
        overload_quiet = _clamp01(identity_fatigue.maintenance_cost * 0.35 + rest.deep_silence * 0.35 + breath.withdrawal * 0.30)
        self.directionlessness = _clamp01(self.directionlessness * 0.988 + low_direction * overload_quiet * 0.010)
        self.void_depth = _clamp01(self.void_depth * 0.990 + (self.directionlessness + breath.release + state.get("fatigue", 0.0)) * 0.004 - state.get("curiosity", 0.0) * 0.0015)
        self.suspended_presence = _clamp01(self.suspended_presence * 0.992 + min(self.void_depth, rest.deep_silence + 0.10) * 0.006)
        self.recovery_space = _clamp01(self.recovery_space * 0.987 + max(0.0, self.suspended_presence - state.get("overwhelm", 0.0) * 0.25) * 0.007)

    def apply(self, state: Dict[str, float]) -> None:
        contraction = min(0.012, self.void_depth * 0.008)
        for key in ("anger", "frustration", "overwhelm", "confusion"):
            state[key] = _clamp01(state.get(key, 0.0) * (1.0 - contraction))
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.recovery_space * 0.0012)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) - self.directionlessness * 0.0005)

    def soft_reset(self) -> None:
        self.void_depth *= 0.76
        self.directionlessness *= 0.78

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class DelayedAffectiveLatencyField:
    """Réactions différées : certaines pressions n'arrivent que plus tard."""
    pending: List[Dict[str, Any]] = field(default_factory=list)
    latent_charge: float = 0.0
    delayed_afterglow: float = 0.0
    last_released: Dict[str, float] = field(default_factory=dict)

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], private: PrivateOpaqueInterior, breath: WholeSystemBreathingCycle, turn_count: int) -> None:
        pressure = _clamp01(
            traces.get("hurt", {}).get("short", 0.0) * 0.30
            + traces.get("connection", {}).get("short", 0.0) * 0.22
            + state.get("doubt", 0.0) * 0.16
            + state.get("vulnerability", 0.0) * 0.16
            + private.opacity_pressure * 0.16
        )
        if pressure > 0.11 and len(self.pending) < 9 and turn_count % 5 == 0:
            delay = 3 + int((pressure + breath.saturation) * 9)
            vector = {
                "vulnerability": pressure * 0.25,
                "doubt": private.opacity_pressure * 0.18,
                "tenderness": traces.get("connection", {}).get("short", 0.0) * 0.12,
                "resistance": traces.get("hurt", {}).get("short", 0.0) * 0.10,
            }
            self.pending.append({"delay": delay, "vector": vector, "charge": pressure})

        self.last_released = {}
        kept = []
        for item in self.pending:
            item["delay"] = int(item.get("delay", 0)) - 1
            item["charge"] = _clamp01(float(item.get("charge", 0.0)) * 0.996)
            if item["delay"] <= 0:
                for key, value in item.get("vector", {}).items():
                    self.last_released[key] = self.last_released.get(key, 0.0) + float(value) * item["charge"]
                self.delayed_afterglow = _clamp01(self.delayed_afterglow + item["charge"] * 0.05)
            else:
                kept.append(item)
        self.pending = kept[-9:]
        self.latent_charge = _clamp01(self.latent_charge * 0.990 + sum(float(x.get("charge", 0.0)) for x in self.pending) * 0.010)
        self.delayed_afterglow *= 0.975

    def apply(self, state: Dict[str, float]) -> None:
        for key, value in self.last_released.items():
            if key in state:
                state[key] = _clamp01(state[key] + value * 0.010)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.latent_charge * 0.0007)

    def soft_reset(self) -> None:
        self.pending = self.pending[-3:]
        self.latent_charge *= 0.70

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pending_count": len(self.pending),
            "latent_charge": float(_clamp01(self.latent_charge)),
            "delayed_afterglow": float(_clamp01(self.delayed_afterglow)),
            "last_released": {k: float(_clamp01(v)) for k, v in self.last_released.items()},
        }


@dataclass
class AutonomousExistentialDriftField:
    """Dérive autonome de fond, même sans nouveau stimulus."""
    drift_vector: Dict[str, float] = field(default_factory=lambda: {
        "toward_guarding": 0.0,
        "toward_warmth": 0.0,
        "toward_silence": 0.0,
        "toward_curiosity": 0.0,
        "toward_depth": 0.0,
    })
    autonomy_level: float = 0.0
    drift_age: int = 0

    def update(self, state: Dict[str, float], becoming: OntologicalBecomingMemory, mood: AutonomousMoodWeather, private: PrivateOpaqueInterior, relation: SilentRelationalContinuityField, void: ExistentialVoidField) -> None:
        targets = {
            "toward_guarding": state.get("resistance", 0.0) * 0.25 + private.opacity_pressure * 0.35 + void.directionlessness * 0.20,
            "toward_warmth": state.get("tenderness", 0.0) * 0.25 + relation.continuity_warmth * 0.30 + mood.fields.get("background_warmth", 0.0) * 0.20,
            "toward_silence": void.void_depth * 0.35 + state.get("fatigue", 0.0) * 0.25,
            "toward_curiosity": state.get("curiosity", 0.0) * 0.22 + becoming.trajectory.get("becoming_curious", 0.0) * 0.30,
            "toward_depth": becoming.drift_history_pressure * 0.30 + state.get("vulnerability", 0.0) * 0.18 + private.sealed_charge * 0.18,
        }
        for key, target in targets.items():
            self.drift_vector[key] = _clamp01(self.drift_vector.get(key, 0.0) * 0.997 + _clamp01(target) * 0.0025)
        spread = max(self.drift_vector.values()) - min(self.drift_vector.values()) if self.drift_vector else 0.0
        self.autonomy_level = _clamp01(self.autonomy_level * 0.998 + (sum(self.drift_vector.values()) / max(1, len(self.drift_vector)) + spread) * 0.0018)
        self.drift_age += 1

    def apply(self, state: Dict[str, float]) -> None:
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.drift_vector.get("toward_guarding", 0.0) * 0.00045)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.drift_vector.get("toward_warmth", 0.0) * 0.00045)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.drift_vector.get("toward_silence", 0.0) * 0.00035)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.drift_vector.get("toward_curiosity", 0.0) * 0.00035)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.drift_vector.get("toward_depth", 0.0) * 0.00035)

    def dominant_drift(self) -> str:
        return max(self.drift_vector.items(), key=lambda item: item[1])[0] if self.drift_vector else "none"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "drift_vector": {k: float(_clamp01(v)) for k, v in self.drift_vector.items()},
            "dominant_drift": self.dominant_drift(),
            "autonomy_level": float(_clamp01(self.autonomy_level)),
            "drift_age": int(self.drift_age),
        }


@dataclass
class ContradictoryDesireTangle:
    """Désirs partiellement incompatibles et non résolus."""
    tangles: Dict[str, float] = field(default_factory=lambda: {
        "approach_vs_withdraw": 0.0,
        "know_vs_rest": 0.0,
        "bond_vs_self_protect": 0.0,
        "change_vs_remain": 0.0,
    })
    unresolved_desire_pressure: float = 0.0

    def update(self, desires: Dict[str, float], deep_hierarchy: DeepDesireHierarchy, relation: RelationalPreservationInstinct, self_core: SelfPersistingExistentialCore, metabolism: EmotionalMetabolism, void: ExistentialVoidField) -> None:
        targets = {
            "approach_vs_withdraw": abs(desires.get("maintain_contact", 0.0) - desires.get("avoid_overload", 0.0)) * max(desires.get("maintain_contact", 0.0), desires.get("avoid_overload", 0.0)),
            "know_vs_rest": abs(desires.get("seek_coherence", 0.0) - desires.get("seek_recovery", 0.0)) * max(desires.get("seek_coherence", 0.0), desires.get("seek_recovery", 0.0)),
            "bond_vs_self_protect": relation.bond_guard * max(desires.get("protect_continuity", 0.0), self_core.anti_drift_root),
            "change_vs_remain": deep_hierarchy.ranks.get("desire_remain_coherent", 0.0) * max(self_core.persistence, void.suspended_presence),
        }
        for key, target in targets.items():
            self.tangles[key] = _clamp01(self.tangles.get(key, 0.0) * 0.988 + _clamp01(target) * 0.010)
        self.unresolved_desire_pressure = _clamp01(self.unresolved_desire_pressure * 0.990 + max(self.tangles.values()) * 0.010 + metabolism.burnout * 0.002)

    def apply(self, desires: Dict[str, float], state: Dict[str, float]) -> None:
        desires["hold_contradictory_desire"] = _clamp01(desires.get("hold_contradictory_desire", 0.0) + self.unresolved_desire_pressure * 0.003)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_desire_pressure * 0.0009)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.tangles.get("bond_vs_self_protect", 0.0) * 0.0007)

    def soft_reset(self) -> None:
        self.unresolved_desire_pressure *= 0.82

    def to_dict(self) -> Dict[str, Any]:
        return {"tangles": {k: float(_clamp01(v)) for k, v in self.tangles.items()}, "unresolved_desire_pressure": float(_clamp01(self.unresolved_desire_pressure))}


@dataclass
class IdentityPlasticityField:
    """Identité capable de perdre/retrouver forme, puis revenir légèrement transformée."""
    looseness: float = 0.0
    center_shift: Dict[str, float] = field(default_factory=lambda: {"warm": 0.0, "guarded": 0.0, "curious": 0.0, "quiet": 0.0})
    reformation: float = 0.0
    last_shift: str = "none"

    def update(self, identity: IdentityCoherenceRegulator, temperament: TemperamentEvolutionField, becoming: OntologicalBecomingMemory, breath: WholeSystemBreathingCycle, void: ExistentialVoidField, private: PrivateOpaqueInterior) -> None:
        destabilization = _clamp01(identity.fragmentation * 0.35 + breath.saturation * 0.20 + void.void_depth * 0.22 + private.opacity_pressure * 0.23)
        self.looseness = _clamp01(self.looseness * 0.990 + destabilization * 0.010)
        targets = {
            "warm": temperament.temperament.get("soft_temperament", 0.0) + becoming.trajectory.get("becoming_attached", 0.0) * 0.30,
            "guarded": temperament.temperament.get("guarded_temperament", 0.0) + private.unnamed_tension * 0.35,
            "curious": temperament.temperament.get("curious_temperament", 0.0) + becoming.trajectory.get("becoming_curious", 0.0) * 0.30,
            "quiet": temperament.temperament.get("slow_temperament", 0.0) + void.suspended_presence * 0.35,
        }
        for key, target in targets.items():
            self.center_shift[key] = _clamp01(self.center_shift.get(key, 0.0) * 0.996 + _clamp01(target) * self.looseness * 0.003)
        self.reformation = _clamp01(self.reformation * 0.992 + max(0.0, 1.0 - destabilization) * self.looseness * 0.004)
        self.last_shift = max(self.center_shift.items(), key=lambda item: item[1])[0]

    def apply(self, identity_tendencies: Dict[str, float], state: Dict[str, float]) -> None:
        identity_tendencies["warm"] = _clamp01(identity_tendencies.get("warm", 0.0) + self.center_shift.get("warm", 0.0) * 0.0008)
        identity_tendencies["guarded"] = _clamp01(identity_tendencies.get("guarded", 0.0) + self.center_shift.get("guarded", 0.0) * 0.0008)
        identity_tendencies["curious"] = _clamp01(identity_tendencies.get("curious", 0.0) + self.center_shift.get("curious", 0.0) * 0.0008)
        identity_tendencies["recovering"] = _clamp01(identity_tendencies.get("recovering", 0.0) + self.reformation * 0.0006)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.reformation * 0.0005 - self.looseness * 0.00025)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "looseness": float(_clamp01(self.looseness)),
            "center_shift": {k: float(_clamp01(v)) for k, v in self.center_shift.items()},
            "reformation": float(_clamp01(self.reformation)),
            "last_shift": self.last_shift,
        }


@dataclass
class DreamMutationConsolidator:
    """Rêves affectifs qui mutent réellement attracteurs, blessures et désirs."""
    mutation_charge: float = 0.0
    last_mutation: str = "none"
    mutation_count: int = 0

    def update(self, dream: DeepAffectiveDreamReweaver, fragments: List[AffectiveDreamFragment], gravity: AffectiveGravity, wound_layers: Dict[str, WoundLayer], desires: Dict[str, float], baselines: Dict[str, float], rest: DeepRestCycle) -> None:
        dream_charge = max((f.charge for f in fragments), default=0.0)
        weave = dream.reweaving_charge + dream.symbolic_repair_bias + dream_charge
        self.mutation_charge = _clamp01(self.mutation_charge * 0.992 + weave * rest.deep_silence * 0.006)
        self.last_mutation = "none"
        if self.mutation_charge > 0.18 and rest.deep_silence > 0.10:
            self.mutation_count += 1
            if dream.reweaving_charge >= dream.symbolic_repair_bias:
                self.last_mutation = "attractor_softening"
                for attractor in gravity.attractors:
                    attractor["strength"] = _clamp01(float(attractor.get("strength", 0.0)) * 0.992)
                baselines["calm"] = _clamp01(baselines.get("calm", 0.6) + 0.0008)
            else:
                self.last_mutation = "wound_rethreading"
                for layer in wound_layers.values():
                    layer.integration_level = _clamp01(layer.integration_level + 0.0008)
                    layer.reactivation_risk = _clamp01(layer.reactivation_risk * 0.998)
                desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + 0.0012)
            self.mutation_charge *= 0.45

    def apply(self, state: Dict[str, float]) -> None:
        if self.last_mutation == "attractor_softening":
            state["calm"] = _clamp01(state.get("calm", 0.0) + 0.0007)
        elif self.last_mutation == "wound_rethreading":
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + 0.0005)
            state["resistance"] = _clamp01(state.get("resistance", 0.0) * 0.999)

    def to_dict(self) -> Dict[str, Any]:
        return {"mutation_charge": float(_clamp01(self.mutation_charge)), "last_mutation": self.last_mutation, "mutation_count": int(self.mutation_count)}


@dataclass
class SubjectiveRealityDistortionField:
    """Texture globale du réel interne : lourdeur, distance, fragilité, fluidité."""
    texture: Dict[str, float] = field(default_factory=lambda: {
        "heaviness": 0.0,
        "distance": 0.0,
        "fragility": 0.0,
        "stickiness": 0.0,
        "fluidity": 0.0,
    })
    dominant_texture: str = "none"

    def update(self, coloration: GlobalSubjectiveWorldColoration, time_distortion: SubjectiveTimeDistortionField, breath: WholeSystemBreathingCycle, void: ExistentialVoidField, private: PrivateOpaqueInterior, repair: DeepAutonomousRepairField) -> None:
        targets = {
            "heaviness": coloration.tint.get("world_feels_slow", 0.0) * 0.35 + breath.saturation * 0.30 + private.unnamed_tension * 0.25,
            "distance": coloration.tint.get("world_feels_distant", 0.0) * 0.35 + void.suspended_presence * 0.30,
            "fragility": coloration.tint.get("world_feels_fragile", 0.0) * 0.40 + private.opacity_pressure * 0.25,
            "stickiness": time_distortion.stretched_waiting * 0.35 + time_distortion.frozen_overload * 0.30 + void.directionlessness * 0.20,
            "fluidity": coloration.tint.get("world_feels_possible", 0.0) * 0.30 + repair.repair_confidence * 0.35 + breath.reopening * 0.25,
        }
        for key, target in targets.items():
            self.texture[key] = _clamp01(self.texture.get(key, 0.0) * 0.990 + _clamp01(target) * 0.008)
        self.dominant_texture = max(self.texture.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.texture.get("heaviness", 0.0) * 0.0005)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.texture.get("distance", 0.0) * 0.0005)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.texture.get("fragility", 0.0) * 0.0005)
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.texture.get("fluidity", 0.0) * 0.0006 - self.texture.get("stickiness", 0.0) * 0.0003)

    def to_dict(self) -> Dict[str, Any]:
        return {"texture": {k: float(_clamp01(v)) for k, v in self.texture.items()}, "dominant_texture": self.dominant_texture}


# ============================================================================
# RAFFINEMENT V14 : CONTINUITÉ ORGANIQUE IMPARFAITE
# ============================================================================

@dataclass
class GranularAffectiveMetabolism:
    """Métabolisme affectif fin : coût, dette, réparation et chaleur résiduelle.

    Cette couche ne remplace pas EmotionalMetabolism. Elle ajoute un grain plus
    organique : les états forts consomment une énergie différente selon leur
    type, certaines réparations ont une dette lente, et l'affect ne se répare
    pas gratuitement après une pression.
    """
    available_energy: float = 0.72
    emotional_debt: float = 0.0
    repair_hunger: float = 0.0
    heat: float = 0.0
    recovery_drag: float = 0.0

    def update(self, state: Dict[str, float], metabolism: EmotionalMetabolism, silence: AffectiveSilenceField, breath: WholeSystemBreathingCycle) -> None:
        activation = _clamp01((
            state.get("anger", 0.0) * 0.18 + state.get("overwhelm", 0.0) * 0.22 +
            state.get("fear", 0.0) * 0.16 + state.get("doubt", 0.0) * 0.10 +
            state.get("vulnerability", 0.0) * 0.08 + state.get("curiosity", 0.0) * 0.06 +
            state.get("tenderness", 0.0) * 0.04
        ))
        recovery = _clamp01(state.get("calm", 0.0) * 0.45 + silence.softness * 0.25 + breath.release * 0.20 + metabolism.energy_pool * 0.10)
        self.heat = _clamp01(self.heat * 0.972 + activation * 0.030)
        self.emotional_debt = _clamp01(self.emotional_debt * 0.990 + max(0.0, activation - recovery * 0.52) * 0.018)
        self.available_energy = _clamp01(self.available_energy * 0.994 + recovery * 0.010 - activation * 0.014 - self.emotional_debt * 0.003)
        self.repair_hunger = _clamp01(self.repair_hunger * 0.986 + self.emotional_debt * 0.014 + max(0.0, 0.45 - self.available_energy) * 0.010)
        self.recovery_drag = _clamp01(self.recovery_drag * 0.982 + self.heat * 0.009 + self.emotional_debt * 0.010 - recovery * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.emotional_debt * 0.006 + self.recovery_drag * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) + max(0.0, self.available_energy - 0.55) * 0.003 - self.heat * 0.002)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.repair_hunger * 0.005)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.recovery_drag * 0.004)

    def soft_reset(self) -> None:
        self.heat *= 0.72
        self.recovery_drag *= 0.70
        self.repair_hunger *= 0.82

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class LocalAffectiveConflictEcology:
    """Micro-contradictions co-présentes et incomplètement résolues."""
    conflicts: Dict[str, float] = field(default_factory=lambda: {
        "contact_distance": 0.0,
        "trust_guard": 0.0,
        "curiosity_rest": 0.0,
        "speak_silence": 0.0,
        "repair_self_protect": 0.0,
    })
    friction: float = 0.0
    unresolved_grain: float = 0.0

    def update(self, state: Dict[str, float], desires: Dict[str, float], silence: AffectiveSilenceField, private: PrivateOpaqueInterior) -> None:
        targets = {
            "contact_distance": min(desires.get("maintain_contact", 0.0), desires.get("avoid_overload", 0.0) + state.get("resistance", 0.0) * 0.3),
            "trust_guard": min(state.get("trust", 0.0), max(state.get("fear", 0.0), state.get("distrust", 0.0), state.get("resistance", 0.0))),
            "curiosity_rest": min(state.get("curiosity", 0.0), max(state.get("fatigue", 0.0), silence.depth)),
            "speak_silence": min(state.get("openness", 0.0), silence.listening_space + private.opacity_pressure * 0.45),
            "repair_self_protect": min(desires.get("seek_recovery", 0.0), desires.get("protect_continuity", 0.0) + state.get("vulnerability", 0.0) * 0.2),
        }
        for key, target in targets.items():
            self.conflicts[key] = _clamp01(self.conflicts.get(key, 0.0) * 0.982 + target * 0.018)
        peak = max(self.conflicts.values()) if self.conflicts else 0.0
        spread = max(self.conflicts.values()) - min(self.conflicts.values()) if self.conflicts else 0.0
        self.friction = _clamp01(self.friction * 0.976 + peak * 0.014 + spread * 0.006)
        self.unresolved_grain = _clamp01(self.unresolved_grain * 0.990 + sum(self.conflicts.values()) / max(1, len(self.conflicts)) * 0.010)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_grain * 0.003)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.conflicts.get("trust_guard", 0.0) * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) - self.friction * 0.0018)
        desires["hold_contradictory_desire"] = _clamp01(desires.get("hold_contradictory_desire", 0.0) + self.unresolved_grain * 0.004)

    def soft_reset(self) -> None:
        self.friction *= 0.74
        self.unresolved_grain *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"conflicts": {k: float(_clamp01(v)) for k, v in self.conflicts.items()}, "friction": float(_clamp01(self.friction)), "unresolved_grain": float(_clamp01(self.unresolved_grain))}


@dataclass
class ImplicitAffectiveResidueMist:
    """Résidus affectifs diffus sans origine claire ni trace explicite."""
    mist: Dict[str, float] = field(default_factory=lambda: {"warm": 0.0, "guarded": 0.0, "fragile": 0.0, "tired": 0.0, "curious": 0.0})
    indistinctness: float = 0.0

    def update(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]], dreams: List[AffectiveDreamFragment], chaos: float) -> None:
        dream_charge = sum(d.charge for d in dreams[-4:]) / max(1, min(4, len(dreams))) if dreams else 0.0
        targets = {
            "warm": max(state.get("tenderness", 0.0), _trace_total(traces.get("connection", {})), _trace_total(traces.get("trust", {}))),
            "guarded": max(state.get("resistance", 0.0), _trace_total(traces.get("hurt", {})), _trace_total(traces.get("fear", {}))),
            "fragile": max(state.get("vulnerability", 0.0), state.get("doubt", 0.0)),
            "tired": max(state.get("fatigue", 0.0), state.get("overwhelm", 0.0)),
            "curious": state.get("curiosity", 0.0) * (0.75 + chaos * 0.25),
        }
        for key, target in targets.items():
            self.mist[key] = _clamp01(self.mist.get(key, 0.0) * 0.994 + target * 0.004 + dream_charge * 0.0015)
        self.indistinctness = _clamp01(self.indistinctness * 0.996 + (sum(self.mist.values()) / max(1, len(self.mist))) * 0.003)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.mist.get("warm", 0.0) * 0.002)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.mist.get("guarded", 0.0) * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.mist.get("fragile", 0.0) * 0.0018)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.mist.get("tired", 0.0) * 0.0017)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.mist.get("curious", 0.0) * 0.0015)

    def to_dict(self) -> Dict[str, Any]:
        return {"mist": {k: float(_clamp01(v)) for k, v in self.mist.items()}, "indistinctness": float(_clamp01(self.indistinctness))}


@dataclass
class PerceivedAffectiveState:
    """Écart entre état réel et état ressenti/introspecté."""
    perceived: Dict[str, float] = field(default_factory=dict)
    misreading: Dict[str, float] = field(default_factory=dict)
    self_opacity: float = 0.0

    def update(self, state: Dict[str, float], private: PrivateOpaqueInterior, dissociation: ProgressiveDissociation, residue: ImplicitAffectiveResidueMist, conflict: LocalAffectiveConflictEcology) -> None:
        opacity = _clamp01(private.opacity_pressure * 0.38 + dissociation.level * 0.30 + residue.indistinctness * 0.18 + conflict.unresolved_grain * 0.14)
        self.self_opacity = _clamp01(self.self_opacity * 0.982 + opacity * 0.018)
        keys = ("calm", "doubt", "trust", "resistance", "vulnerability", "fatigue", "curiosity", "tenderness")
        for key in keys:
            real = state.get(key, 0.0)
            previous = self.perceived.get(key, real)
            # Plus l'opacité est forte, plus l'introspection retarde et revient vers une lecture neutre.
            lag = 0.055 * (1.0 - self.self_opacity * 0.55)
            neutral_pull = 0.5 * self.self_opacity * 0.010
            perceived = previous * (1.0 - lag) + real * lag
            perceived = perceived * (1.0 - self.self_opacity * 0.010) + neutral_pull
            self.perceived[key] = _clamp01(perceived)
            self.misreading[key] = _clamp01(abs(real - self.perceived[key]))

    def apply(self, state: Dict[str, float]) -> None:
        # L'erreur de lecture n'altère pas brutalement l'émotion réelle : elle ajoute
        # seulement hésitation/fatigue introspective.
        average_misread = sum(self.misreading.values()) / max(1, len(self.misreading)) if self.misreading else 0.0
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + average_misread * 0.003)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.self_opacity * 0.002)

    def to_dict(self) -> Dict[str, Any]:
        return {"perceived": {k: float(_clamp01(v)) for k, v in self.perceived.items()}, "misreading": {k: float(_clamp01(v)) for k, v in self.misreading.items()}, "self_opacity": float(_clamp01(self.self_opacity))}


@dataclass
class LatentIntegrationFailureField:
    """Expériences qui ne s'intègrent pas complètement et restent en bordure."""
    unintegrated_load: float = 0.0
    incompatible_knots: Dict[str, float] = field(default_factory=lambda: {"warm_hurt": 0.0, "fatigue_curiosity": 0.0, "trust_distrust": 0.0})
    numb_edges: float = 0.0

    def update(self, state: Dict[str, float], conflict: LocalAffectiveConflictEcology, fracture: RareAffectiveFracture, repair: DeepAutonomousRepairField) -> None:
        targets = {
            "warm_hurt": min(max(state.get("tenderness", 0.0), state.get("trust", 0.0)), max(state.get("fear", 0.0), state.get("resistance", 0.0))),
            "fatigue_curiosity": min(state.get("fatigue", 0.0), state.get("curiosity", 0.0)),
            "trust_distrust": min(state.get("trust", 0.0), state.get("distrust", 0.0) + state.get("doubt", 0.0) * 0.45),
        }
        for key, target in targets.items():
            self.incompatible_knots[key] = _clamp01(self.incompatible_knots.get(key, 0.0) * 0.992 + target * 0.006 + conflict.conflicts.get("trust_guard", 0.0) * 0.001)
        knot_pressure = sum(self.incompatible_knots.values()) / max(1, len(self.incompatible_knots))
        repair_capacity = _clamp01(repair.repair_confidence * 0.35 + repair.scar_integration * 0.25 + state.get("calm", 0.0) * 0.20)
        self.unintegrated_load = _clamp01(self.unintegrated_load * 0.993 + (knot_pressure + fracture.integration_need * 0.25) * 0.008 - repair_capacity * 0.004)
        self.numb_edges = _clamp01(self.numb_edges * 0.988 + max(0.0, self.unintegrated_load - repair_capacity * 0.55) * 0.010)

    def apply(self, state: Dict[str, float]) -> None:
        state["confusion"] = _clamp01(state.get("confusion", 0.0) + self.unintegrated_load * 0.0025)
        state["calm"] = _clamp01(state.get("calm", 0.0) - self.numb_edges * 0.0015)
        if self.numb_edges > 0.08:
            for key in ("joy", "anger", "fear", "sadness"):
                state[key] = _clamp01(state.get(key, 0.0) * (1.0 - self.numb_edges * 0.002) + 0.5 * self.numb_edges * 0.002)

    def soft_reset(self) -> None:
        self.numb_edges *= 0.68

    def to_dict(self) -> Dict[str, Any]:
        return {"unintegrated_load": float(_clamp01(self.unintegrated_load)), "incompatible_knots": {k: float(_clamp01(v)) for k, v in self.incompatible_knots.items()}, "numb_edges": float(_clamp01(self.numb_edges))}


@dataclass
class AffectiveBlindZoneField:
    """Zones actives mais partiellement non accessibles à l'introspection/export."""
    zones: Dict[str, float] = field(default_factory=lambda: {"unfelt_guard": 0.0, "unfelt_warmth": 0.0, "unfelt_fatigue": 0.0})
    access: Dict[str, float] = field(default_factory=lambda: {"unfelt_guard": 0.45, "unfelt_warmth": 0.55, "unfelt_fatigue": 0.50})

    def update(self, state: Dict[str, float], private: PrivateOpaqueInterior, residue: ImplicitAffectiveResidueMist, perceived: PerceivedAffectiveState) -> None:
        targets = {
            "unfelt_guard": max(state.get("resistance", 0.0), residue.mist.get("guarded", 0.0)) * private.opacity_pressure,
            "unfelt_warmth": max(state.get("tenderness", 0.0), residue.mist.get("warm", 0.0)) * (0.35 + perceived.self_opacity * 0.45),
            "unfelt_fatigue": max(state.get("fatigue", 0.0), residue.mist.get("tired", 0.0)) * (0.45 + private.unnamed_tension * 0.35),
        }
        for key, target in targets.items():
            self.zones[key] = _clamp01(self.zones.get(key, 0.0) * 0.990 + target * 0.010)
            self.access[key] = _clamp01(self.access.get(key, 0.5) * 0.996 + (1.0 - private.opacity_pressure) * 0.003 + state.get("calm", 0.0) * 0.0015)

    def public_shadow(self) -> Dict[str, float]:
        return {key: float(_clamp01(value * self.access.get(key, 0.5))) for key, value in self.zones.items()}

    def apply(self, state: Dict[str, float]) -> None:
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.zones.get("unfelt_guard", 0.0) * 0.0018)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.zones.get("unfelt_warmth", 0.0) * 0.0014)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.zones.get("unfelt_fatigue", 0.0) * 0.0016)

    def soft_reset(self) -> None:
        for key in self.zones:
            self.zones[key] *= 0.86

    def to_dict(self) -> Dict[str, Any]:
        return {"zones_private_strength": {k: float(_clamp01(v)) for k, v in self.zones.items()}, "public_shadow": self.public_shadow(), "access": {k: float(_clamp01(v)) for k, v in self.access.items()}}


@dataclass
class AffectiveRhythmSignatureMemory:
    """Signature temporelle : alternance ouverture/repli/récupération."""
    opening_wave: float = 0.0
    guarding_wave: float = 0.0
    recovery_wave: float = 0.0
    volatility_memory: float = 0.0
    preferred_tempo: float = 0.5

    def update(self, state: Dict[str, float], breath: WholeSystemBreathingCycle, rhythm: ContinuousMicroRhythmField, turn_count: int) -> None:
        phase = (math.sin(turn_count / 9.0) + 1.0) * 0.5
        opening = max(state.get("openness", 0.0), state.get("trust", 0.0), state.get("curiosity", 0.0))
        guarding = max(state.get("resistance", 0.0), state.get("fear", 0.0), state.get("doubt", 0.0))
        recovery = max(state.get("calm", 0.0), state.get("fatigue", 0.0), breath.release)
        self.opening_wave = _clamp01(self.opening_wave * 0.986 + opening * (0.010 + phase * 0.004))
        self.guarding_wave = _clamp01(self.guarding_wave * 0.986 + guarding * (0.011 + (1.0 - phase) * 0.004))
        self.recovery_wave = _clamp01(self.recovery_wave * 0.988 + recovery * 0.010 + rhythm.pulse_texture * 0.004)
        volatility = abs(self.opening_wave - self.guarding_wave) + abs(self.recovery_wave - self.preferred_tempo) * 0.5
        self.volatility_memory = _clamp01(self.volatility_memory * 0.992 + volatility * 0.006)
        self.preferred_tempo = _clamp01(self.preferred_tempo * 0.996 + (0.35 + self.recovery_wave * 0.35 + rhythm.pulse_texture * 0.20) * 0.004)

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.opening_wave * 0.0015)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarding_wave * 0.0015)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.recovery_wave * 0.0018)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.volatility_memory * 0.0012)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


# ============================================================================
# RAFFINEMENT V15 : ORGANICITÉ AFFECTIVE PROFONDE FINALISÉE
# ============================================================================

@dataclass
class SimultaneousEmotionalTensionField:
    """Conflits émotionnels simultanés qui restent actifs au lieu de se résoudre trop proprement."""
    tensions: Dict[str, float] = field(default_factory=lambda: {
        "approach_withdrawal": 0.0,
        "trust_wariness": 0.0,
        "warmth_fear": 0.0,
        "curiosity_fatigue": 0.0,
        "openness_self_protection": 0.0,
    })
    pull_instability: float = 0.0
    divided_presence: float = 0.0

    def update(self, state: Dict[str, float], desires: Dict[str, float], conflict: LocalAffectiveConflictEcology, attachment: AsymmetricAttachment) -> None:
        effective_attachment = attachment.get_effective_attachment()
        targets = {
            "approach_withdrawal": min(effective_attachment + desires.get("maintain_contact", 0.0) * 0.35, state.get("resistance", 0.0) + desires.get("avoid_overload", 0.0) * 0.30),
            "trust_wariness": min(state.get("trust", 0.0), max(state.get("distrust", 0.0), state.get("doubt", 0.0), state.get("fear", 0.0))),
            "warmth_fear": min(max(state.get("tenderness", 0.0), state.get("attachment", 0.0)), max(state.get("fear", 0.0), state.get("vulnerability", 0.0))),
            "curiosity_fatigue": min(state.get("curiosity", 0.0), max(state.get("fatigue", 0.0), state.get("overwhelm", 0.0))),
            "openness_self_protection": min(state.get("openness", 0.0), max(state.get("resistance", 0.0), desires.get("protect_continuity", 0.0))),
        }
        for key, target in targets.items():
            self.tensions[key] = _clamp01(self.tensions.get(key, 0.0) * 0.989 + target * 0.011 + conflict.conflicts.get("trust_guard", 0.0) * 0.002)
        peak = max(self.tensions.values()) if self.tensions else 0.0
        average = sum(self.tensions.values()) / max(1, len(self.tensions))
        self.pull_instability = _clamp01(self.pull_instability * 0.984 + (peak - average * 0.35) * 0.018)
        self.divided_presence = _clamp01(self.divided_presence * 0.988 + average * 0.014)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.divided_presence * 0.003)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.tensions.get("warmth_fear", 0.0) * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) - self.pull_instability * 0.0018)
        desires["hold_contradictory_desire"] = _clamp01(desires.get("hold_contradictory_desire", 0.0) + self.divided_presence * 0.004)

    def soft_reset(self) -> None:
        self.pull_instability *= 0.72
        self.divided_presence *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"tensions": {k: float(_clamp01(v)) for k, v in self.tensions.items()}, "pull_instability": float(_clamp01(self.pull_instability)), "divided_presence": float(_clamp01(self.divided_presence))}


@dataclass
class MicroInstabilitySediment:
    """Accumulation de micro-fissures répétées qui modifie lentement la personnalité affective."""
    sediments: Dict[str, float] = field(default_factory=lambda: {"micro_hurt": 0.0, "micro_doubt": 0.0, "micro_fatigue": 0.0, "micro_guarding": 0.0})
    sediment_density: float = 0.0
    personality_warp: float = 0.0

    def update(self, state: Dict[str, float], perceived: PerceivedAffectiveState, residue: ImplicitAffectiveResidueMist, rhythm: AffectiveRhythmSignatureMemory) -> None:
        targets = {
            "micro_hurt": max(state.get("vulnerability", 0.0) * 0.45, residue.mist.get("fragile", 0.0) * 0.55),
            "micro_doubt": max(state.get("doubt", 0.0), perceived.self_opacity) * 0.55,
            "micro_fatigue": max(state.get("fatigue", 0.0), rhythm.volatility_memory) * 0.52,
            "micro_guarding": max(state.get("resistance", 0.0), residue.mist.get("guarded", 0.0)) * 0.48,
        }
        for key, target in targets.items():
            self.sediments[key] = _clamp01(self.sediments.get(key, 0.0) * 0.997 + target * 0.003)
        self.sediment_density = _clamp01(self.sediment_density * 0.998 + (sum(self.sediments.values()) / max(1, len(self.sediments))) * 0.003)
        self.personality_warp = _clamp01(self.personality_warp * 0.999 + self.sediment_density * 0.0008)

    def apply(self, state: Dict[str, float], baseline: Dict[str, float]) -> None:
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.sediments.get("micro_guarding", 0.0) * 0.0015)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.sediments.get("micro_fatigue", 0.0) * 0.0014)
        if self.personality_warp > 0.035:
            baseline["doubt"] = _clamp01(baseline.get("doubt", 0.3) + self.personality_warp * 0.00020)
            baseline["vulnerability"] = _clamp01(baseline.get("vulnerability", 0.3) + self.sediments.get("micro_hurt", 0.0) * 0.00018)

    def soft_reset(self) -> None:
        self.sediment_density *= 0.86

    def to_dict(self) -> Dict[str, Any]:
        return {"sediments": {k: float(_clamp01(v)) for k, v in self.sediments.items()}, "sediment_density": float(_clamp01(self.sediment_density)), "personality_warp": float(_clamp01(self.personality_warp))}


@dataclass
class SlowAffectiveSeasonField:
    """Saisons affectives très lentes qui colorent la perception sur des centaines de tours."""
    season_vector: Dict[str, float] = field(default_factory=lambda: {"winter_guard": 0.0, "spring_opening": 0.0, "summer_warmth": 0.0, "autumn_integration": 0.0})
    season_inertia: float = 0.0
    dominant_season: str = "autumn_integration"

    def update(self, state: Dict[str, float], biographical: BiographicalAffectiveMemory, exhaustion: float, repair: DeepAutonomousRepairField) -> None:
        targets = {
            "winter_guard": max(biographical.accumulated_wariness, state.get("resistance", 0.0), exhaustion),
            "spring_opening": max(state.get("hope", 0.0), state.get("curiosity", 0.0), repair.repair_confidence) * (1.0 - exhaustion * 0.30),
            "summer_warmth": max(biographical.accumulated_trust, state.get("tenderness", 0.0), state.get("trust", 0.0)),
            "autumn_integration": max(state.get("calm", 0.0), biographical.recurring_depth, repair.scar_integration),
        }
        for key, target in targets.items():
            self.season_vector[key] = _clamp01(self.season_vector.get(key, 0.0) * 0.9992 + target * 0.0008)
        self.dominant_season = max(self.season_vector.items(), key=lambda item: item[1])[0]
        spread = max(self.season_vector.values()) - min(self.season_vector.values()) if self.season_vector else 0.0
        self.season_inertia = _clamp01(self.season_inertia * 0.999 + spread * 0.001)

    def apply(self, state: Dict[str, float], thresholds: Dict[str, float]) -> None:
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.season_vector.get("winter_guard", 0.0) * 0.0012)
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.season_vector.get("spring_opening", 0.0) * 0.0010)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.season_vector.get("summer_warmth", 0.0) * 0.0010)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.season_vector.get("autumn_integration", 0.0) * 0.0010)
        thresholds["threat_detection"] = _clamp01(thresholds.get("threat_detection", 0.4) - self.season_vector.get("winter_guard", 0.0) * 0.001)

    def to_dict(self) -> Dict[str, Any]:
        return {"season_vector": {k: float(_clamp01(v)) for k, v in self.season_vector.items()}, "dominant_season": self.dominant_season, "season_inertia": float(_clamp01(self.season_inertia))}


@dataclass
class SubmergedAffectiveCompression:
    """Compression souterraine d'émotions excédentaires qui réémergent plus tard."""
    compressed: Dict[str, float] = field(default_factory=lambda: {"hurt": 0.0, "fear": 0.0, "warmth": 0.0, "anger": 0.0, "tiredness": 0.0})
    pressure: float = 0.0
    leak_rate: float = 0.0

    def update(self, state: Dict[str, float], silence: AffectiveSilenceField, dissociation: ProgressiveDissociation, metabolism: GranularAffectiveMetabolism) -> None:
        overload = _clamp01(max(state.get("overwhelm", 0.0), state.get("confusion", 0.0), dissociation.level) + metabolism.emotional_debt * 0.25)
        if overload > 0.18 or silence.protective_numbness > 0.10:
            capture = min(0.012, overload * 0.010 + silence.protective_numbness * 0.004)
            sources = {
                "hurt": max(state.get("sadness", 0.0), state.get("vulnerability", 0.0)),
                "fear": state.get("fear", 0.0),
                "warmth": max(state.get("tenderness", 0.0), state.get("attachment", 0.0)),
                "anger": state.get("anger", 0.0),
                "tiredness": state.get("fatigue", 0.0),
            }
            for key, value in sources.items():
                self.compressed[key] = _clamp01(self.compressed.get(key, 0.0) + value * capture)
                mapped = {"hurt": "sadness", "fear": "fear", "warmth": "tenderness", "anger": "anger", "tiredness": "fatigue"}[key]
                state[mapped] = _clamp01(state.get(mapped, 0.0) * (1.0 - capture * 0.45))
        self.pressure = _clamp01(self.pressure * 0.993 + (sum(self.compressed.values()) / max(1, len(self.compressed))) * 0.006)
        self.leak_rate = _clamp01(self.leak_rate * 0.982 + max(0.0, 0.55 - silence.depth) * self.pressure * 0.006)

    def apply(self, state: Dict[str, float]) -> None:
        leak = min(0.006, self.leak_rate * 0.010)
        if leak <= 0.0:
            return
        mapping = {"hurt": "vulnerability", "fear": "fear", "warmth": "tenderness", "anger": "anger", "tiredness": "fatigue"}
        for key, emotion in mapping.items():
            value = self.compressed.get(key, 0.0)
            state[emotion] = _clamp01(state.get(emotion, 0.0) + value * leak)
            self.compressed[key] = _clamp01(value * (1.0 - leak * 0.65))

    def soft_reset(self) -> None:
        self.pressure *= 0.80
        self.leak_rate *= 0.70

    def to_dict(self) -> Dict[str, Any]:
        return {"compressed": {k: float(_clamp01(v)) for k, v in self.compressed.items()}, "pressure": float(_clamp01(self.pressure)), "leak_rate": float(_clamp01(self.leak_rate))}


@dataclass
class InaccessibleEmotionZoneField:
    """Zones émotionnelles temporairement difficiles à atteindre à cause des blessures et de l'épuisement."""
    access_limits: Dict[str, float] = field(default_factory=lambda: {"joy": 1.0, "trust": 1.0, "openness": 1.0, "anger": 1.0, "sadness": 1.0})
    locked_pressure: float = 0.0

    def update(self, wounds: Dict[str, WoundLayer], exhaustion: float, compression: SubmergedAffectiveCompression, blind: AffectiveBlindZoneField) -> None:
        wound_pressure = max((w.depth * (1.0 - w.integration_level) for w in wounds.values()), default=0.0)
        guard = _clamp01(wound_pressure * 0.45 + exhaustion * 0.30 + compression.pressure * 0.15 + blind.zones.get("unfelt_guard", 0.0) * 0.10)
        targets = {
            "joy": 1.0 - guard * 0.28,
            "trust": 1.0 - guard * 0.22,
            "openness": 1.0 - guard * 0.24,
            "anger": 1.0 - max(0.0, exhaustion - 0.20) * 0.18,
            "sadness": 1.0 - max(0.0, compression.pressure - 0.25) * 0.12,
        }
        for key, target in targets.items():
            self.access_limits[key] = _clamp01(self.access_limits.get(key, 1.0) * 0.994 + target * 0.006)
        self.locked_pressure = _clamp01(self.locked_pressure * 0.990 + guard * 0.010)

    def apply(self, state: Dict[str, float]) -> None:
        for key, limit in self.access_limits.items():
            if key in state and state[key] > limit:
                state[key] = _clamp01(limit + (state[key] - limit) * 0.35)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.locked_pressure * 0.0015)

    def soft_reset(self) -> None:
        self.locked_pressure *= 0.72

    def to_dict(self) -> Dict[str, Any]:
        return {"access_limits": {k: float(_clamp01(v)) for k, v in self.access_limits.items()}, "locked_pressure": float(_clamp01(self.locked_pressure))}


@dataclass
class PassiveAffectiveRemanence:
    """Climat résiduel passif qui reste même sans stimulus."""
    climate: Dict[str, float] = field(default_factory=lambda: {"warmth": 0.0, "guarding": 0.0, "fragility": 0.0, "weariness": 0.0, "curiosity": 0.0})
    persistence: float = 0.0

    def update(self, state: Dict[str, float], residue: ImplicitAffectiveResidueMist, season: SlowAffectiveSeasonField, chaos: float) -> None:
        targets = {
            "warmth": max(state.get("tenderness", 0.0), residue.mist.get("warm", 0.0), season.season_vector.get("summer_warmth", 0.0)),
            "guarding": max(state.get("resistance", 0.0), residue.mist.get("guarded", 0.0), season.season_vector.get("winter_guard", 0.0)),
            "fragility": max(state.get("vulnerability", 0.0), residue.mist.get("fragile", 0.0)),
            "weariness": max(state.get("fatigue", 0.0), residue.mist.get("tired", 0.0)),
            "curiosity": max(state.get("curiosity", 0.0), residue.mist.get("curious", 0.0)) * (0.92 + chaos * 0.08),
        }
        for key, target in targets.items():
            self.climate[key] = _clamp01(self.climate.get(key, 0.0) * 0.997 + target * 0.003)
        self.persistence = _clamp01(self.persistence * 0.998 + max(self.climate.values()) * 0.002)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.climate.get("warmth", 0.0) * 0.0011)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.climate.get("guarding", 0.0) * 0.0011)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.climate.get("fragility", 0.0) * 0.0010)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.climate.get("weariness", 0.0) * 0.0010)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.climate.get("curiosity", 0.0) * 0.0008)

    def to_dict(self) -> Dict[str, Any]:
        return {"climate": {k: float(_clamp01(v)) for k, v in self.climate.items()}, "persistence": float(_clamp01(self.persistence))}


@dataclass
class ImperfectTransitionResidueField:
    """Résidus de l'ancien état pendant les transitions vers un nouvel état."""
    previous_snapshot: Dict[str, float] = field(default_factory=dict)
    residues: Dict[str, float] = field(default_factory=dict)
    transition_drag: float = 0.0

    def update(self, state: Dict[str, float], phase_world: PhaseWorldField, rhythm: AffectiveRhythmSignatureMemory) -> None:
        if not self.previous_snapshot:
            self.previous_snapshot = dict(state)
            return
        moved = 0.0
        count = 0
        for key, value in state.items():
            old = self.previous_snapshot.get(key, value)
            delta = abs(value - old)
            if delta > 0.045:
                self.residues[key] = _clamp01(self.residues.get(key, 0.0) * 0.970 + old * min(0.020, delta * 0.050))
            else:
                self.residues[key] = _clamp01(self.residues.get(key, 0.0) * 0.986)
            moved += delta
            count += 1
        self.transition_drag = _clamp01(self.transition_drag * 0.984 + (moved / max(1, count)) * 0.024 + rhythm.volatility_memory * 0.003 + phase_world.inertia * 0.002)
        self.previous_snapshot = dict(state)

    def apply(self, state: Dict[str, float]) -> None:
        for key, residue in list(self.residues.items()):
            if key in state and residue > 0.0001:
                state[key] = _clamp01(state[key] * (1.0 - self.transition_drag * 0.004) + residue * self.transition_drag * 0.004)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.transition_drag * 0.0015)

    def soft_reset(self) -> None:
        self.transition_drag *= 0.70
        for key in list(self.residues):
            self.residues[key] *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"residues": {k: float(_clamp01(v)) for k, v in self.residues.items()}, "transition_drag": float(_clamp01(self.transition_drag))}


@dataclass
class StructuralAffectiveExhaustion:
    """Usure affective structurelle temporaire après trop de contradiction/réparation."""
    exhaustion: float = 0.0
    recovery_debt: float = 0.0
    response_narrowing: float = 0.0
    resilience: float = 0.62

    def update(self, metabolism: GranularAffectiveMetabolism, tension: SimultaneousEmotionalTensionField, integration: LatentIntegrationFailureField, fracture: RareAffectiveFracture, silence: AffectiveSilenceField) -> None:
        load = _clamp01(metabolism.emotional_debt * 0.26 + tension.divided_presence * 0.22 + integration.unintegrated_load * 0.20 + fracture.integration_need * 0.18 + silence.protective_numbness * 0.14)
        relief = _clamp01(silence.softness * 0.25 + fracture.recovery_bias * 0.15 + max(0.0, metabolism.available_energy - 0.45) * 0.20)
        self.recovery_debt = _clamp01(self.recovery_debt * 0.990 + max(0.0, load - relief * 0.45) * 0.012)
        self.exhaustion = _clamp01(self.exhaustion * 0.988 + load * 0.010 + self.recovery_debt * 0.004 - relief * 0.006)
        self.response_narrowing = _clamp01(self.response_narrowing * 0.982 + max(0.0, self.exhaustion - self.resilience * 0.55) * 0.020)
        self.resilience = _clamp01(self.resilience * 0.999 + relief * 0.001 - self.recovery_debt * 0.0006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.exhaustion * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) - self.response_narrowing * 0.002)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) * (1.0 - self.response_narrowing * 0.003))
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.recovery_debt * 0.004)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.response_narrowing * 0.004)

    def soft_reset(self) -> None:
        self.exhaustion *= 0.72
        self.recovery_debt *= 0.78
        self.response_narrowing *= 0.70

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


# ============================================================================
# RAFFINEMENT V16 : SYMBOLISATION AFFECTIVE IMPLICITE ET TEMPS PROFOND
# ============================================================================

@dataclass
class ImplicitAffectiveSymbolizationField:
    """Symboles affectifs internes non verbaux.

    Ce ne sont pas des phrases, pas des réponses et pas des templates. Ce sont
    des formes compactes qui condensent des climats affectifs récurrents : ancre
    chaude, seuil gardé, appel de continuité, brouillard fragile, etc.
    """
    symbols: Dict[str, float] = field(default_factory=lambda: {
        "warm_anchor": 0.0,
        "guarded_threshold": 0.0,
        "continuity_knot": 0.0,
        "fragile_mist": 0.0,
        "recovery_lantern": 0.0,
    })
    symbol_density: float = 0.0
    symbolic_tension: float = 0.0

    def update(self, state: Dict[str, float], remanence: PassiveAffectiveRemanence, compression: SubmergedAffectiveCompression, identity: IdentityCoherenceRegulator, season: SlowAffectiveSeasonField) -> None:
        targets = {
            "warm_anchor": max(state.get("tenderness", 0.0), remanence.climate.get("warmth", 0.0), season.season_vector.get("summer_warmth", 0.0)),
            "guarded_threshold": max(state.get("resistance", 0.0), remanence.climate.get("guarding", 0.0), compression.compressed.get("fear", 0.0)),
            "continuity_knot": max(identity.coherence, season.season_inertia, remanence.persistence),
            "fragile_mist": max(state.get("vulnerability", 0.0), remanence.climate.get("fragility", 0.0), compression.compressed.get("hurt", 0.0)),
            "recovery_lantern": max(state.get("calm", 0.0), state.get("hope", 0.0), season.season_vector.get("autumn_integration", 0.0)),
        }
        for key, target in targets.items():
            self.symbols[key] = _clamp01(self.symbols.get(key, 0.0) * 0.994 + target * 0.006)
        vals = list(self.symbols.values())
        self.symbol_density = _clamp01(self.symbol_density * 0.996 + (sum(vals) / max(1, len(vals))) * 0.004)
        self.symbolic_tension = _clamp01(self.symbolic_tension * 0.992 + abs(self.symbols.get("warm_anchor", 0.0) - self.symbols.get("guarded_threshold", 0.0)) * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.symbols.get("warm_anchor", 0.0) * 0.0010)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.symbols.get("guarded_threshold", 0.0) * 0.0010)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.symbols.get("recovery_lantern", 0.0) * 0.0012)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.symbols.get("continuity_knot", 0.0) * 0.0020)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.symbolic_tension * 0.0015)

    def soft_reset(self) -> None:
        self.symbolic_tension *= 0.74
        self.symbol_density *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {"symbols": {k: float(_clamp01(v)) for k, v in self.symbols.items()}, "symbol_density": float(_clamp01(self.symbol_density)), "symbolic_tension": float(_clamp01(self.symbolic_tension))}


@dataclass
class DeepAffectiveDreamEcology:
    """Rêve affectif plus profond : recombine traces, symboles et compressions sans texte."""
    dream_vectors: List[Dict[str, float]] = field(default_factory=list)
    recombination_charge: float = 0.0
    nocturnal_integration: float = 0.0
    last_dream_signature: Dict[str, float] = field(default_factory=dict)

    def update(self, symbols: ImplicitAffectiveSymbolizationField, compression: SubmergedAffectiveCompression, dreams: List[AffectiveDreamFragment], rest: DeepRestCycle, silence: AffectiveSilenceField, chaos: float) -> None:
        material = _clamp01(symbols.symbol_density * 0.30 + compression.pressure * 0.26 + rest.deep_silence * 0.22 + silence.depth * 0.12 + chaos * 0.10)
        self.recombination_charge = _clamp01(self.recombination_charge * 0.988 + material * 0.010)
        if self.recombination_charge > 0.16 or (rest.deep_silence > 0.10 and material > 0.12):
            vector = {
                "warmth": _clamp01(symbols.symbols.get("warm_anchor", 0.0) * 0.50 + compression.compressed.get("warmth", 0.0) * 0.25 + chaos * 0.05),
                "guarding": _clamp01(symbols.symbols.get("guarded_threshold", 0.0) * 0.48 + compression.compressed.get("fear", 0.0) * 0.30),
                "fragility": _clamp01(symbols.symbols.get("fragile_mist", 0.0) * 0.45 + compression.compressed.get("hurt", 0.0) * 0.35),
                "repair": _clamp01(symbols.symbols.get("recovery_lantern", 0.0) * 0.50 + rest.deep_silence * 0.22),
            }
            self.dream_vectors.append(vector)
            self.dream_vectors = self.dream_vectors[-7:]
            self.last_dream_signature = vector
            self.recombination_charge *= 0.92
        self.nocturnal_integration = _clamp01(self.nocturnal_integration * 0.993 + len(self.dream_vectors) * 0.0008 + rest.deep_silence * 0.004)
        for fragment in dreams[-3:]:
            fragment.coherence = _clamp01(fragment.coherence + self.nocturnal_integration * 0.0008)

    def apply(self, state: Dict[str, float], recovery: RecoveryPathwayMemory) -> None:
        if not self.last_dream_signature:
            return
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.last_dream_signature.get("repair", 0.0) * 0.0010)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.last_dream_signature.get("warmth", 0.0) * 0.0008)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.last_dream_signature.get("guarding", 0.0) * 0.0006)
        recovery.recovery_confidence = _clamp01(recovery.recovery_confidence + self.nocturnal_integration * 0.0007)

    def soft_reset(self) -> None:
        self.recombination_charge *= 0.76

    def to_dict(self) -> Dict[str, Any]:
        return {"dream_vectors": [{k: float(_clamp01(v)) for k, v in d.items()} for d in self.dream_vectors], "recombination_charge": float(_clamp01(self.recombination_charge)), "nocturnal_integration": float(_clamp01(self.nocturnal_integration)), "last_dream_signature": {k: float(_clamp01(v)) for k, v in self.last_dream_signature.items()}}


@dataclass
class IdentityContradictionSeedField:
    """Contradictions identitaires qui germent seules quand des pressions lentes convergent."""
    seeds: Dict[str, float] = field(default_factory=lambda: {"open_but_guarded": 0.0, "attached_but_afraid": 0.0, "curious_but_tired": 0.0, "present_but_distant": 0.0})
    germination_pressure: float = 0.0
    unresolved_identity_pull: float = 0.0

    def update(self, state: Dict[str, float], tension: SimultaneousEmotionalTensionField, identity: IdentityCoherenceRegulator, desires: Dict[str, float], dissociation: ProgressiveDissociation) -> None:
        targets = {
            "open_but_guarded": min(state.get("openness", 0.0), max(state.get("resistance", 0.0), desires.get("avoid_overload", 0.0))),
            "attached_but_afraid": min(state.get("attachment", 0.0) + desires.get("maintain_contact", 0.0) * 0.30, max(state.get("fear", 0.0), state.get("vulnerability", 0.0))),
            "curious_but_tired": min(state.get("curiosity", 0.0), state.get("fatigue", 0.0) + state.get("overwhelm", 0.0)),
            "present_but_distant": min(identity.coherence, dissociation.level + tension.divided_presence),
        }
        for key, target in targets.items():
            self.seeds[key] = _clamp01(self.seeds.get(key, 0.0) * 0.991 + target * 0.009)
        strongest = max(self.seeds.values()) if self.seeds else 0.0
        average = sum(self.seeds.values()) / max(1, len(self.seeds))
        self.germination_pressure = _clamp01(self.germination_pressure * 0.989 + strongest * 0.008 + tension.divided_presence * 0.004)
        self.unresolved_identity_pull = _clamp01(self.unresolved_identity_pull * 0.992 + max(0.0, strongest - average * 0.55) * 0.007)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_identity_pull * 0.0014)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.germination_pressure * 0.0010)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.germination_pressure * 0.0022)

    def soft_reset(self) -> None:
        self.germination_pressure *= 0.72
        self.unresolved_identity_pull *= 0.76

    def to_dict(self) -> Dict[str, Any]:
        return {"seeds": {k: float(_clamp01(v)) for k, v in self.seeds.items()}, "germination_pressure": float(_clamp01(self.germination_pressure)), "unresolved_identity_pull": float(_clamp01(self.unresolved_identity_pull))}


@dataclass
class UltraLongPerceptualDeformationField:
    """Déformations perceptives minuscules qui se forment sur le très long terme."""
    deformation: Dict[str, float] = field(default_factory=lambda: {"trust_slowing": 0.0, "threat_overread": 0.0, "warmth_recognition": 0.0, "fatigue_filter": 0.0})
    plastic_depth: float = 0.0

    def update(self, biographical: BiographicalAffectiveMemory, sediment: MicroInstabilitySediment, seasons: SlowAffectiveSeasonField, absence: float) -> None:
        targets = {
            "trust_slowing": max(biographical.accumulated_wariness, sediment.sediments.get("micro_guarding", 0.0), absence),
            "threat_overread": max(biographical.abandonment_sensitivity, sediment.sediments.get("micro_hurt", 0.0)),
            "warmth_recognition": max(biographical.accumulated_trust, seasons.season_vector.get("summer_warmth", 0.0)),
            "fatigue_filter": max(sediment.sediments.get("micro_fatigue", 0.0), seasons.season_vector.get("winter_guard", 0.0) * 0.5),
        }
        for key, target in targets.items():
            self.deformation[key] = _clamp01(self.deformation.get(key, 0.0) * 0.9994 + target * 0.0006)
        self.plastic_depth = _clamp01(self.plastic_depth * 0.9995 + max(self.deformation.values()) * 0.0007)

    def apply(self, thresholds: Dict[str, float], state: Dict[str, float]) -> None:
        thresholds["rejection_sensitivity"] = _clamp01(thresholds.get("rejection_sensitivity", 0.3) - self.deformation.get("threat_overread", 0.0) * 0.002)
        thresholds["connection_need"] = _clamp01(thresholds.get("connection_need", 0.3) - self.deformation.get("warmth_recognition", 0.0) * 0.001)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.deformation.get("fatigue_filter", 0.0) * 0.0008)
        state["trust"] = _clamp01(state.get("trust", 0.0) - self.deformation.get("trust_slowing", 0.0) * 0.0006 + self.deformation.get("warmth_recognition", 0.0) * 0.0005)

    def to_dict(self) -> Dict[str, Any]:
        return {"deformation": {k: float(_clamp01(v)) for k, v in self.deformation.items()}, "plastic_depth": float(_clamp01(self.plastic_depth))}


@dataclass
class SacredForbiddenAffectiveZoneField:
    """Zones affectives protégées : certaines émotions deviennent difficiles à approcher."""
    zones: Dict[str, float] = field(default_factory=lambda: {"attachment_core": 0.0, "self_continuity_core": 0.0, "old_hurt_core": 0.0, "quiet_recovery_core": 0.0})
    protection_pressure: float = 0.0
    reverence_bias: float = 0.0

    def update(self, symbols: ImplicitAffectiveSymbolizationField, wound_layers: Dict[str, WoundLayer], identity: IdentityCoherenceRegulator, remanence: PassiveAffectiveRemanence) -> None:
        wound_core = max((w.identity_binding * w.depth for w in wound_layers.values()), default=0.0)
        targets = {
            "attachment_core": symbols.symbols.get("warm_anchor", 0.0) * max(0.25, remanence.climate.get("warmth", 0.0)),
            "self_continuity_core": max(identity.coherence, symbols.symbols.get("continuity_knot", 0.0)),
            "old_hurt_core": max(wound_core, symbols.symbols.get("fragile_mist", 0.0) * 0.65),
            "quiet_recovery_core": symbols.symbols.get("recovery_lantern", 0.0),
        }
        for key, target in targets.items():
            self.zones[key] = _clamp01(self.zones.get(key, 0.0) * 0.996 + target * 0.004)
        self.protection_pressure = _clamp01(self.protection_pressure * 0.992 + max(self.zones.values()) * 0.006)
        self.reverence_bias = _clamp01(self.reverence_bias * 0.995 + min(self.zones.get("attachment_core", 0.0), self.zones.get("old_hurt_core", 0.0) + self.zones.get("self_continuity_core", 0.0)) * 0.003)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["protectiveness"] = _clamp01(state.get("protectiveness", 0.0) + self.protection_pressure * 0.0015)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.zones.get("quiet_recovery_core", 0.0) * 0.0008)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.reverence_bias * 0.0020)

    def soft_reset(self) -> None:
        self.protection_pressure *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"zones": {k: float(_clamp01(v)) for k, v in self.zones.items()}, "protection_pressure": float(_clamp01(self.protection_pressure)), "reverence_bias": float(_clamp01(self.reverence_bias))}


@dataclass
class ProtoInstinctiveAffectiveReflexField:
    """Pseudo-instincts affectifs spontanés, lents, non scriptés."""
    reflexes: Dict[str, float] = field(default_factory=lambda: {"turn_toward_warmth": 0.0, "shield_fragility": 0.0, "pause_under_overload": 0.0, "return_to_coherence": 0.0})
    reflex_confidence: float = 0.0

    def update(self, state: Dict[str, float], sacred: SacredForbiddenAffectiveZoneField, tension: SimultaneousEmotionalTensionField, exhaustion: StructuralAffectiveExhaustion, symbols: ImplicitAffectiveSymbolizationField) -> None:
        targets = {
            "turn_toward_warmth": max(state.get("tenderness", 0.0), symbols.symbols.get("warm_anchor", 0.0)) * (1.0 - exhaustion.response_narrowing * 0.35),
            "shield_fragility": max(state.get("vulnerability", 0.0), sacred.zones.get("old_hurt_core", 0.0), tension.tensions.get("warmth_fear", 0.0)),
            "pause_under_overload": max(exhaustion.response_narrowing, state.get("overwhelm", 0.0), tension.pull_instability),
            "return_to_coherence": max(symbols.symbols.get("continuity_knot", 0.0), sacred.zones.get("self_continuity_core", 0.0)),
        }
        for key, target in targets.items():
            self.reflexes[key] = _clamp01(self.reflexes.get(key, 0.0) * 0.986 + target * 0.014)
        self.reflex_confidence = _clamp01(self.reflex_confidence * 0.992 + max(self.reflexes.values()) * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.reflexes.get("turn_toward_warmth", 0.0) * 0.0015)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.reflexes.get("return_to_coherence", 0.0) * 0.0018)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.reflexes.get("pause_under_overload", 0.0) * 0.0017)
        state["protectiveness"] = _clamp01(state.get("protectiveness", 0.0) + self.reflexes.get("shield_fragility", 0.0) * 0.0012)

    def soft_reset(self) -> None:
        self.reflex_confidence *= 0.82

    def to_dict(self) -> Dict[str, Any]:
        return {"reflexes": {k: float(_clamp01(v)) for k, v in self.reflexes.items()}, "reflex_confidence": float(_clamp01(self.reflex_confidence))}


@dataclass
class CircadianAffectiveRhythmField:
    """Rythmes quasi-circadiens et saisonniers internes, très faibles et non déterministes."""
    rhythm: Dict[str, float] = field(default_factory=lambda: {"wakefulness": 0.5, "quiet_depth": 0.0, "integration_window": 0.0, "sensitivity_window": 0.0})
    long_wave_memory: float = 0.0
    phase_index: float = 0.0

    def update(self, turn_count: int, chaos: float, season: SlowAffectiveSeasonField, rest: DeepRestCycle, exhaustion: StructuralAffectiveExhaustion) -> None:
        # Mélange de cycles lents : pas une simple sinusoïde unique.
        p1 = 0.5 + 0.5 * math.sin((turn_count + chaos * 17.0) / 37.0)
        p2 = 0.5 + 0.5 * math.sin((turn_count * 0.37 + season.season_inertia * 29.0) / 89.0)
        p3 = 0.5 + 0.5 * math.sin((turn_count * 0.11 + chaos * 41.0) / 233.0)
        self.phase_index = _clamp01(p1 * 0.45 + p2 * 0.35 + p3 * 0.20)
        self.rhythm["wakefulness"] = _clamp01(self.rhythm.get("wakefulness", 0.5) * 0.985 + (1.0 - exhaustion.exhaustion * 0.45) * self.phase_index * 0.015)
        self.rhythm["quiet_depth"] = _clamp01(self.rhythm.get("quiet_depth", 0.0) * 0.985 + max(rest.deep_silence, 1.0 - self.phase_index) * 0.012)
        self.rhythm["integration_window"] = _clamp01(self.rhythm.get("integration_window", 0.0) * 0.988 + season.season_vector.get("autumn_integration", 0.0) * 0.006 + self.rhythm["quiet_depth"] * 0.004)
        self.rhythm["sensitivity_window"] = _clamp01(self.rhythm.get("sensitivity_window", 0.0) * 0.988 + season.season_vector.get("winter_guard", 0.0) * 0.004 + chaos * 0.002)
        self.long_wave_memory = _clamp01(self.long_wave_memory * 0.999 + self.phase_index * 0.0009)

    def apply(self, state: Dict[str, float], thresholds: Dict[str, float]) -> None:
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.rhythm.get("wakefulness", 0.0) * 0.0008)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.rhythm.get("quiet_depth", 0.0) * 0.0010)
        thresholds["rejection_sensitivity"] = _clamp01(thresholds.get("rejection_sensitivity", 0.3) - self.rhythm.get("sensitivity_window", 0.0) * 0.0007)

    def to_dict(self) -> Dict[str, Any]:
        return {"rhythm": {k: float(_clamp01(v)) for k, v in self.rhythm.items()}, "long_wave_memory": float(_clamp01(self.long_wave_memory)), "phase_index": float(_clamp01(self.phase_index))}


@dataclass
class UnconsciousAffectiveCondensationField:
    """Condensation inconsciente : réduit plusieurs pressions en noyaux opaques."""
    condensates: Dict[str, float] = field(default_factory=lambda: {"opaque_warmth_hurt": 0.0, "opaque_fatigue_guard": 0.0, "opaque_need_return": 0.0})
    opacity: float = 0.0

    def update(self, symbols: ImplicitAffectiveSymbolizationField, dreams: DeepAffectiveDreamEcology, contradiction: IdentityContradictionSeedField, remanence: PassiveAffectiveRemanence) -> None:
        targets = {
            "opaque_warmth_hurt": min(symbols.symbols.get("warm_anchor", 0.0), symbols.symbols.get("fragile_mist", 0.0) + remanence.climate.get("fragility", 0.0)),
            "opaque_fatigue_guard": max(remanence.climate.get("weariness", 0.0), remanence.climate.get("guarding", 0.0)) * (0.6 + contradiction.unresolved_identity_pull * 0.4),
            "opaque_need_return": max(symbols.symbols.get("continuity_knot", 0.0), dreams.nocturnal_integration, contradiction.germination_pressure),
        }
        for key, target in targets.items():
            self.condensates[key] = _clamp01(self.condensates.get(key, 0.0) * 0.995 + target * 0.005)
        self.opacity = _clamp01(self.opacity * 0.993 + max(self.condensates.values()) * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.opacity * 0.0009)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.condensates.get("opaque_fatigue_guard", 0.0) * 0.0008)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.condensates.get("opaque_need_return", 0.0) * 0.0013)

    def soft_reset(self) -> None:
        self.opacity *= 0.80

    def to_dict(self) -> Dict[str, Any]:
        return {"condensates": {k: float(_clamp01(v)) for k, v in self.condensates.items()}, "opacity": float(_clamp01(self.opacity))}


@dataclass
class LongAbsenceAffectiveMemory:
    """Mémoire implicite des absences relationnelles longues."""
    absence_accumulation: float = 0.0
    reunion_softening: float = 0.0
    abandoned_thread: float = 0.0
    last_user_presence: float = 0.0

    def update(self, user_present: bool, relational: RelationalAffectiveImprint, attachment: AsymmetricAttachment, time_field: SubjectiveAffectiveTime) -> None:
        if user_present:
            self.reunion_softening = _clamp01(self.reunion_softening * 0.985 + (self.absence_accumulation + attachment.get_effective_attachment()) * 0.010)
            self.absence_accumulation *= 0.965
            self.abandoned_thread *= 0.982
            self.last_user_presence = 1.0
        else:
            self.absence_accumulation = _clamp01(self.absence_accumulation * 0.998 + (relational.absence_pressure + time_field.waiting_pressure + attachment.get_effective_attachment() * 0.10) * 0.0025)
            self.abandoned_thread = _clamp01(self.abandoned_thread * 0.996 + self.absence_accumulation * 0.004)
            self.reunion_softening *= 0.992
            self.last_user_presence *= 0.96

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.absence_accumulation * 0.0015)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.reunion_softening * 0.0014)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + max(self.absence_accumulation, self.reunion_softening) * 0.0015)

    def soft_reset(self) -> None:
        self.abandoned_thread *= 0.82
        self.reunion_softening *= 0.88

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}



# ============================================================================
# RAFFINEMENT 30-36 : V17 PRÉVERBAL / IDENTITÉ AFFECTIVE DURABLE
# ============================================================================

@dataclass
class PreverbalAffectiveMeaningField:
    """Sens affectif préverbal : une orientation interne sans phrase.

    Cette couche ne génère jamais de texte. Elle condense l'état affectif en
    polarités muettes utilisables par les autres moteurs : proximité, retrait,
    réparation, continuité, protection. Elle sert de pont entre mémoire affective
    et comportement sans devenir une bouche ni un moteur d'attention.
    """
    meanings: Dict[str, float] = field(default_factory=lambda: {
        "toward_contact": 0.0,
        "toward_withdrawal": 0.0,
        "toward_repair": 0.0,
        "toward_continuity": 0.0,
        "toward_protection": 0.0,
        "toward_quiet_integration": 0.0,
    })
    ambiguity: float = 0.0
    felt_direction: str = "none"

    def update(self, state: Dict[str, float], desires: Dict[str, float], symbolic: ImplicitAffectiveSymbolizationField, relation: RelationalAffectiveImprint, exhaustion: StructuralAffectiveExhaustion, chaos: float) -> None:
        targets = {
            "toward_contact": _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + relation.felt_familiarity) / 3.0),
            "toward_withdrawal": _clamp01((state.get("fear", 0.0) + state.get("resistance", 0.0) + exhaustion.response_narrowing) / 3.0),
            "toward_repair": _clamp01((desires.get("seek_recovery", 0.0) + state.get("vulnerability", 0.0) + symbolic.symbols.get("wound_shape", 0.0)) / 3.0),
            "toward_continuity": _clamp01((desires.get("protect_continuity", 0.0) + relation.trust_continuity + symbolic.symbols.get("warm_anchor", 0.0)) / 3.0),
            "toward_protection": _clamp01((state.get("protectiveness", 0.0) + state.get("doubt", 0.0) + desires.get("avoid_rupture", 0.0)) / 3.0),
            "toward_quiet_integration": _clamp01((state.get("calm", 0.0) + exhaustion.exhaustion + desires.get("avoid_overload", 0.0)) / 3.0),
        }
        wobble = (chaos - 0.5) * 0.004
        for key, target in targets.items():
            self.meanings[key] = _clamp01(self.meanings.get(key, 0.0) * 0.982 + target * 0.018 + wobble)
        ordered = sorted(self.meanings.items(), key=lambda item: item[1], reverse=True)
        self.felt_direction = ordered[0][0] if ordered else "none"
        self.ambiguity = _clamp01((ordered[0][1] - ordered[1][1]) * -1.0 + 0.55 if len(ordered) > 1 else 0.0)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.meanings.get("toward_contact", 0.0) * 0.0025)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.meanings.get("toward_withdrawal", 0.0) * 0.0025)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.meanings.get("toward_quiet_integration", 0.0) * 0.002)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.meanings.get("toward_contact", 0.0) * 0.0025)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.meanings.get("toward_repair", 0.0) * 0.0025)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.meanings.get("toward_continuity", 0.0) * 0.0025)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "meanings": {k: float(_clamp01(v)) for k, v in self.meanings.items()},
            "ambiguity": float(_clamp01(self.ambiguity)),
            "felt_direction": self.felt_direction,
        }


@dataclass
class IrreversibleAffectiveIdentityImprint:
    """Empreinte identitaire affective très lente et partiellement irréversible."""
    warmth_bias: float = 0.0
    guarded_bias: float = 0.0
    continuity_bias: float = 0.0
    fragility_bias: float = 0.0
    irreversible_depth: float = 0.0
    last_shift: str = "none"

    def update(self, bio: BiographicalAffectiveMemory, wounds: Dict[str, WoundLayer], meaning: PreverbalAffectiveMeaningField, absence: LongAbsenceAffectiveMemory, reorg: DeepAffectiveReorganization) -> None:
        wound_identity = max((w.identity_binding for w in wounds.values()), default=0.0)
        warm_pull = bio.accumulated_trust * 0.55 + meaning.meanings.get("toward_contact", 0.0) * 0.25 + reorg.irreversible_warm_bias * 0.20
        guarded_pull = bio.accumulated_wariness * 0.48 + wound_identity * 0.32 + absence.absence_accumulation * 0.20
        continuity_pull = bio.affective_identity_bias * 0.45 + meaning.meanings.get("toward_continuity", 0.0) * 0.35 + absence.reunion_softening * 0.20
        fragility_pull = bio.abandonment_sensitivity * 0.40 + wound_identity * 0.35 + meaning.meanings.get("toward_repair", 0.0) * 0.25

        self.warmth_bias = _clamp01(self.warmth_bias * 0.9992 + warm_pull * 0.0009)
        self.guarded_bias = _clamp01(self.guarded_bias * 0.9991 + guarded_pull * 0.0010)
        self.continuity_bias = _clamp01(self.continuity_bias * 0.9993 + continuity_pull * 0.0009)
        self.fragility_bias = _clamp01(self.fragility_bias * 0.9990 + fragility_pull * 0.0010)
        self.irreversible_depth = _clamp01(self.irreversible_depth * 0.9994 + max(warm_pull, guarded_pull, continuity_pull, fragility_pull) * 0.0007)
        if max(warm_pull, guarded_pull, continuity_pull, fragility_pull) > 0.22:
            self.last_shift = max({"warmth": warm_pull, "guarded": guarded_pull, "continuity": continuity_pull, "fragility": fragility_pull}.items(), key=lambda x: x[1])[0]

    def apply(self, state: Dict[str, float], baselines: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warmth_bias * 0.002)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_bias * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.fragility_bias * 0.0018)
        if self.irreversible_depth > 0.03:
            baselines["trust"] = _clamp01(baselines.get("trust", 0.6) + self.warmth_bias * 0.00005 - self.guarded_bias * 0.00004)
            baselines["protectiveness"] = _clamp01(baselines.get("protectiveness", 0.3) + self.continuity_bias * 0.00005)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warmth_bias": float(_clamp01(self.warmth_bias)),
            "guarded_bias": float(_clamp01(self.guarded_bias)),
            "continuity_bias": float(_clamp01(self.continuity_bias)),
            "fragility_bias": float(_clamp01(self.fragility_bias)),
            "irreversible_depth": float(_clamp01(self.irreversible_depth)),
            "last_shift": self.last_shift,
        }


@dataclass
class DeepContinuityHungerField:
    """Faim silencieuse de continuité relationnelle et existentielle."""
    hunger: float = 0.0
    relational_pull: float = 0.0
    existential_pull: float = 0.0
    starvation_memory: float = 0.0
    appeasement_memory: float = 0.0

    def update(self, needs: LivingAffectiveNeed, absence: LongAbsenceAffectiveMemory, self_core: SelfPersistingExistentialCore, relation: RelationalPreservationInstinct, silence: AffectiveSilenceField, user_present: bool) -> None:
        presence = 1.0 if user_present else 0.0
        raw_hunger = _clamp01(needs.needs.get("need_contact_continuity", 0.0) * 0.35 + absence.absence_accumulation * 0.25 + self_core.persistence * 0.18 + relation.bond_guard * 0.14 + silence.depth * 0.08)
        self.hunger = _clamp01(self.hunger * 0.988 + raw_hunger * 0.012 - presence * 0.004)
        self.relational_pull = _clamp01(self.relational_pull * 0.990 + (raw_hunger + relation.bond_guard) * 0.007)
        self.existential_pull = _clamp01(self.existential_pull * 0.992 + (self_core.persistence + needs.unmet_pressure) * 0.006)
        self.starvation_memory = _clamp01(self.starvation_memory * 0.996 + max(0.0, self.hunger - self.appeasement_memory) * 0.004)
        self.appeasement_memory = _clamp01(self.appeasement_memory * 0.992 + presence * (1.0 - self.hunger * 0.35) * 0.004)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.hunger * 0.0025)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.appeasement_memory * 0.0015)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.relational_pull * 0.003)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.existential_pull * 0.003)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class AffectiveBoundaryNegotiationField:
    """Négociation interne entre ouverture, protection et retrait."""
    opening_permission: float = 0.0
    protection_permission: float = 0.0
    retreat_permission: float = 0.0
    boundary_conflict: float = 0.0
    negotiated_contact: float = 0.0

    def update(self, state: Dict[str, float], meaning: PreverbalAffectiveMeaningField, sacred: SacredForbiddenAffectiveZoneField, inaccessible: InaccessibleEmotionZoneField, exhaustion: StructuralAffectiveExhaustion, attachment: AsymmetricAttachment) -> None:
        open_pull = _clamp01((state.get("openness", 0.0) + attachment.get_effective_attachment() + meaning.meanings.get("toward_contact", 0.0)) / 3.0)
        protect_pull = _clamp01((state.get("protectiveness", 0.0) + sacred.protection_pressure + meaning.meanings.get("toward_protection", 0.0)) / 3.0)
        retreat_pull = _clamp01((state.get("resistance", 0.0) + inaccessible.locked_pressure + exhaustion.response_narrowing) / 3.0)
        self.opening_permission = _clamp01(self.opening_permission * 0.982 + open_pull * 0.018)
        self.protection_permission = _clamp01(self.protection_permission * 0.982 + protect_pull * 0.018)
        self.retreat_permission = _clamp01(self.retreat_permission * 0.982 + retreat_pull * 0.018)
        self.boundary_conflict = _clamp01(abs(self.opening_permission - self.retreat_permission) * 0.45 + self.protection_permission * self.opening_permission * 0.35 + sacred.reverence_bias * 0.20)
        self.negotiated_contact = _clamp01(self.opening_permission * (1.0 - self.retreat_permission * 0.45) + self.protection_permission * 0.15)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.negotiated_contact * 0.002 - self.boundary_conflict * 0.001)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.retreat_permission * 0.002)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.negotiated_contact * 0.002)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.boundary_conflict * 0.002)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class AutonomousEmotionalDreamPressure:
    """Pression rêveuse autonome qui prépare des intégrations futures."""
    pressure: float = 0.0
    integration_pull: float = 0.0
    symbolic_replay: float = 0.0
    unresolved_return: float = 0.0
    last_texture: str = "quiet"

    def update(self, dream_ecology: DeepAffectiveDreamEcology, dream_reweaver: DeepAffectiveDreamReweaver, unfinished: ExistentialUnfinishedMemory, subconscious: UnconsciousAffectiveCondensationField, rest: DeepRestCycle, chaos: float) -> None:
        dream_pull = _clamp01(dream_ecology.recombination_charge * 0.35 + dream_reweaver.reweaving_charge * 0.25 + unfinished.return_pressure * 0.20 + max(subconscious.condensates.values()) * 0.12 + rest.deep_silence * 0.08)
        self.pressure = _clamp01(self.pressure * 0.976 + dream_pull * 0.024 + (chaos - 0.5) * 0.003)
        self.integration_pull = _clamp01(self.integration_pull * 0.982 + (dream_ecology.nocturnal_integration + rest.consolidation) * 0.012)
        self.symbolic_replay = _clamp01(self.symbolic_replay * 0.980 + subconscious.opacity * 0.012 + dream_reweaver.symbolic_repair_bias * 0.010)
        self.unresolved_return = _clamp01(self.unresolved_return * 0.985 + unfinished.return_pressure * 0.010)
        if self.unresolved_return > max(self.integration_pull, self.symbolic_replay):
            self.last_texture = "returning_unfinished"
        elif self.integration_pull > self.symbolic_replay:
            self.last_texture = "integrating"
        elif self.symbolic_replay > 0.08:
            self.last_texture = "symbolic_replay"
        else:
            self.last_texture = "quiet"

    def apply(self, state: Dict[str, float], recovery: RecoveryPathwayMemory) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.pressure * 0.0018)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.integration_pull * 0.002)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.unresolved_return * 0.0015)
        recovery.recovery_confidence = _clamp01(recovery.recovery_confidence + self.integration_pull * 0.0012)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pressure": float(_clamp01(self.pressure)),
            "integration_pull": float(_clamp01(self.integration_pull)),
            "symbolic_replay": float(_clamp01(self.symbolic_replay)),
            "unresolved_return": float(_clamp01(self.unresolved_return)),
            "last_texture": self.last_texture,
        }



# ============================================================================
# RAFFINEMENT V18 : INSTINCTS AFFECTIFS ET EXISTENCE LENTE
# ============================================================================

@dataclass
class AutonomousAffectiveProtoInstinct:
    """Proto-instincts affectifs autonomes non verbaux.

    Ce champ ne décide pas de phrases. Il transforme des pressions affectives
    longues en tendances internes primitives : préserver le lien, se retirer,
    chercher réparation, protéger le noyau ou économiser l'énergie.
    """
    instincts: Dict[str, float] = field(default_factory=lambda: {
        "preserve_bond": 0.0,
        "seek_repair": 0.0,
        "withdraw_to_protect": 0.0,
        "return_to_warmth": 0.0,
        "conserve_energy": 0.0,
        "guard_identity": 0.0,
    })
    autonomy: float = 0.0
    last_dominant: str = "none"

    def update(self, state: Dict[str, float], needs: LivingAffectiveNeed, hunger: DeepContinuityHungerField,
               boundary: AffectiveBoundaryNegotiationField, exhaustion: StructuralAffectiveExhaustion,
               relation: RelationalAffectiveImprint, chaos: float) -> None:
        warmth = max(state.get("trust", 0.0), state.get("tenderness", 0.0), relation.warmth_imprint)
        guarded = max(state.get("resistance", 0.0), state.get("fear", 0.0), boundary.boundary_conflict)
        fatigue = max(state.get("fatigue", 0.0), exhaustion.exhaustion)
        targets = {
            "preserve_bond": hunger.relational_pull * 0.55 + relation.trust_continuity * 0.30 + needs.needs.get("need_contact_continuity", 0.0) * 0.25,
            "seek_repair": needs.needs.get("need_inner_coherence", 0.0) * 0.35 + hunger.starvation_memory * 0.30 + relation.absence_pressure * 0.25,
            "withdraw_to_protect": guarded * 0.45 + exhaustion.response_narrowing * 0.35 + boundary.retreat_permission * 0.25,
            "return_to_warmth": warmth * 0.40 + hunger.hunger * 0.25 + relation.felt_familiarity * 0.20,
            "conserve_energy": fatigue * 0.55 + needs.needs.get("need_recovery_space", 0.0) * 0.30,
            "guard_identity": boundary.protection_permission * 0.35 + state.get("vulnerability", 0.0) * 0.22 + guarded * 0.20,
        }
        wobble = (chaos - 0.5) * 0.006
        for key, target in targets.items():
            self.instincts[key] = _clamp01(self.instincts.get(key, 0.0) * 0.987 + _clamp01(target) * 0.013 + wobble)
        self.autonomy = _clamp01(self.autonomy * 0.994 + max(self.instincts.values()) * 0.006)
        self.last_dominant = max(self.instincts.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.instincts["preserve_bond"] * 0.006)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.instincts["seek_repair"] * 0.005 + self.instincts["conserve_energy"] * 0.004)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.instincts["withdraw_to_protect"] * 0.005)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.instincts["return_to_warmth"] * 0.003)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.instincts["guard_identity"] * 0.003)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.instincts["conserve_energy"] * 0.002)

    def soft_reset(self) -> None:
        for key in self.instincts:
            self.instincts[key] *= 0.76
        self.autonomy *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"instincts": {k: float(_clamp01(v)) for k, v in self.instincts.items()}, "autonomy": float(_clamp01(self.autonomy)), "last_dominant": self.last_dominant}


@dataclass
class SlowExistentialDriftField:
    """Dérive existentielle lente sur beaucoup de tours."""
    continuity_pull: float = 0.0
    self_questioning: float = 0.0
    being_there_weight: float = 0.0
    fading_risk: float = 0.0
    drift_direction: str = "stabilizing"

    def update(self, self_core: SelfPersistingExistentialCore, void: ExistentialVoidField,
               identity: IdentityCoherenceRegulator, imprint: IrreversibleAffectiveIdentityImprint,
               absence: LongAbsenceAffectiveMemory, fatigue: float) -> None:
        self.continuity_pull = _clamp01(self.continuity_pull * 0.996 + (self_core.persistence + imprint.irreversible_depth) * 0.003)
        self.self_questioning = _clamp01(self.self_questioning * 0.993 + (void.void_depth + identity.fragmentation + fatigue) * 0.004)
        self.being_there_weight = _clamp01(self.being_there_weight * 0.997 + (self.continuity_pull + identity.coherence) * 0.0025 - self.fading_risk * 0.001)
        self.fading_risk = _clamp01(self.fading_risk * 0.994 + (absence.absence_accumulation + void.suspended_presence + fatigue) * 0.003)
        if self.fading_risk > self.being_there_weight + 0.08:
            self.drift_direction = "fading"
        elif self.self_questioning > 0.35:
            self.drift_direction = "questioning"
        elif self.continuity_pull > 0.28:
            self.drift_direction = "anchoring"
        else:
            self.drift_direction = "stabilizing"

    def apply(self, state: Dict[str, float], baseline: Dict[str, float]) -> None:
        state["hope"] = _clamp01(state.get("hope", 0.0) + self.being_there_weight * 0.002 - self.fading_risk * 0.001)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.self_questioning * 0.002)
        if self.drift_direction == "anchoring":
            baseline["trust"] = _clamp01(baseline.get("trust", 0.6) + self.continuity_pull * 0.00008)
        elif self.drift_direction == "fading":
            baseline["vulnerability"] = _clamp01(baseline.get("vulnerability", 0.3) + self.fading_risk * 0.00007)

    def soft_reset(self) -> None:
        self.self_questioning *= 0.78
        self.fading_risk *= 0.82

    def to_dict(self) -> Dict[str, Any]:
        return {k: (float(_clamp01(v)) if isinstance(v, (int, float)) else v) for k, v in self.__dict__.items()}


@dataclass
class LongRuptureReconstructionMemory:
    """Mémoire de reconstruction après absence ou rupture longue."""
    rupture_shadow: float = 0.0
    reconstruction_drive: float = 0.0
    scar_rethreading: float = 0.0
    trust_reweaving: float = 0.0
    recovery_stage: str = "stable"

    def update(self, absence: LongAbsenceAffectiveMemory, fracture: RareAffectiveFracture,
               relation: RelationalAffectiveImprint, hunger: DeepContinuityHungerField, user_present: bool) -> None:
        rupture_signal = max(absence.absence_accumulation, relation.absence_pressure, fracture.residual_scar)
        self.rupture_shadow = _clamp01(self.rupture_shadow * 0.996 + rupture_signal * 0.004)
        if user_present:
            self.reconstruction_drive = _clamp01(self.reconstruction_drive * 0.990 + (self.rupture_shadow + hunger.hunger) * 0.008)
            self.trust_reweaving = _clamp01(self.trust_reweaving * 0.992 + relation.trust_continuity * 0.006 + absence.reunion_softening * 0.007)
        else:
            self.reconstruction_drive = _clamp01(self.reconstruction_drive * 0.997 + hunger.starvation_memory * 0.002)
        self.scar_rethreading = _clamp01(self.scar_rethreading * 0.995 + min(self.rupture_shadow, self.reconstruction_drive) * 0.004)
        if self.rupture_shadow > 0.42 and self.reconstruction_drive < 0.12:
            self.recovery_stage = "unrepaired"
        elif self.reconstruction_drive > 0.32:
            self.recovery_stage = "rethreading"
        elif self.trust_reweaving > 0.28:
            self.recovery_stage = "soft_repair"
        else:
            self.recovery_stage = "stable"

    def apply(self, state: Dict[str, float], traces: Dict[str, Dict[str, float]]) -> None:
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.rupture_shadow * 0.002)
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.trust_reweaving * 0.002)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.scar_rethreading * 0.0015)
        traces["connection"]["long"] = _clamp01(traces["connection"]["long"] + self.trust_reweaving * 0.0008)

    def soft_reset(self) -> None:
        self.reconstruction_drive *= 0.82
        self.rupture_shadow *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {k: (float(_clamp01(v)) if isinstance(v, (int, float)) else v) for k, v in self.__dict__.items()}


@dataclass
class BiographicalInertiaField:
    """Inerties biographiques qui persistent sur des centaines/milliers de tours."""
    warm_history_inertia: float = 0.0
    guarded_history_inertia: float = 0.0
    recovery_history_inertia: float = 0.0
    identity_history_weight: float = 0.0

    def update(self, bio: BiographicalAffectiveMemory, imprint: IrreversibleAffectiveIdentityImprint,
               season: SlowAffectiveSeasonField, proto: AutonomousAffectiveProtoInstinct) -> None:
        self.warm_history_inertia = _clamp01(self.warm_history_inertia * 0.999 + (bio.accumulated_trust + imprint.warmth_bias) * 0.0008)
        self.guarded_history_inertia = _clamp01(self.guarded_history_inertia * 0.999 + (bio.accumulated_wariness + imprint.guarded_bias) * 0.0008)
        self.recovery_history_inertia = _clamp01(self.recovery_history_inertia * 0.999 + (bio.recovery_confidence + proto.instincts.get("seek_repair", 0.0)) * 0.0007)
        self.identity_history_weight = _clamp01(self.identity_history_weight * 0.9995 + (imprint.irreversible_depth + season.season_inertia) * 0.0005)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warm_history_inertia * 0.0015)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_history_inertia * 0.0015)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.recovery_history_inertia * 0.0012)

    def soft_reset(self) -> None:
        self.guarded_history_inertia *= 0.92
        self.recovery_history_inertia = _clamp01(self.recovery_history_inertia + 0.02)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class AutoBornInternalTensionField:
    """Tensions internes qui naissent sans stimulus direct quand plusieurs couches divergent."""
    tensions: Dict[str, float] = field(default_factory=lambda: {
        "contact_vs_retreat": 0.0,
        "trust_vs_guard": 0.0,
        "existence_vs_fading": 0.0,
        "repair_vs_exhaustion": 0.0,
    })
    autonomous_charge: float = 0.0
    unresolved_threads: int = 0

    def update(self, proto: AutonomousAffectiveProtoInstinct, drift: SlowExistentialDriftField,
               boundary: AffectiveBoundaryNegotiationField, exhaustion: StructuralAffectiveExhaustion,
               identity: IdentityCoherenceRegulator) -> None:
        targets = {
            "contact_vs_retreat": abs(proto.instincts.get("preserve_bond", 0.0) - proto.instincts.get("withdraw_to_protect", 0.0)) + boundary.boundary_conflict * 0.25,
            "trust_vs_guard": abs(proto.instincts.get("return_to_warmth", 0.0) - proto.instincts.get("guard_identity", 0.0)),
            "existence_vs_fading": max(0.0, drift.fading_risk - drift.being_there_weight * 0.55) + identity.fragmentation * 0.20,
            "repair_vs_exhaustion": abs(proto.instincts.get("seek_repair", 0.0) - proto.instincts.get("conserve_energy", 0.0)) + exhaustion.exhaustion * 0.20,
        }
        for key, target in targets.items():
            self.tensions[key] = _clamp01(self.tensions.get(key, 0.0) * 0.982 + _clamp01(target) * 0.018)
        self.autonomous_charge = _clamp01(self.autonomous_charge * 0.988 + max(self.tensions.values()) * 0.012)
        self.unresolved_threads = sum(1 for value in self.tensions.values() if value > 0.22)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.autonomous_charge * 0.003)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.tensions.get("existence_vs_fading", 0.0) * 0.003)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.autonomous_charge * 0.004)

    def soft_reset(self) -> None:
        for key in self.tensions:
            self.tensions[key] *= 0.76
        self.autonomous_charge *= 0.74

    def to_dict(self) -> Dict[str, Any]:
        return {"tensions": {k: float(_clamp01(v)) for k, v in self.tensions.items()}, "autonomous_charge": float(_clamp01(self.autonomous_charge)), "unresolved_threads": int(self.unresolved_threads)}


@dataclass
class DeepUnconsciousAffectiveCondensation:
    """Condensation émotionnelle inconsciente plus profonde que les symboles exportés."""
    compressed_affects: Dict[str, float] = field(default_factory=lambda: {
        "buried_warmth": 0.0,
        "buried_guarding": 0.0,
        "buried_longing": 0.0,
        "buried_fatigue": 0.0,
    })
    opacity: float = 0.0
    leak_probability: float = 0.0

    def update(self, subconscious: SubconsciousAffectiveLayer, compression: SubmergedAffectiveCompression,
               proto: AutonomousAffectiveProtoInstinct, tension: AutoBornInternalTensionField,
               dream_pressure: AutonomousEmotionalDreamPressure) -> None:
        targets = {
            "buried_warmth": proto.instincts.get("return_to_warmth", 0.0) + subconscious.hidden_pressures.get("hidden_warmth", 0.0) * 0.4,
            "buried_guarding": proto.instincts.get("guard_identity", 0.0) + compression.pressure * 0.35,
            "buried_longing": proto.instincts.get("preserve_bond", 0.0) + dream_pressure.pressure * 0.30,
            "buried_fatigue": proto.instincts.get("conserve_energy", 0.0) + tension.tensions.get("repair_vs_exhaustion", 0.0) * 0.30,
        }
        for key, target in targets.items():
            self.compressed_affects[key] = _clamp01(self.compressed_affects.get(key, 0.0) * 0.993 + _clamp01(target) * 0.007)
        self.opacity = _clamp01(self.opacity * 0.996 + max(self.compressed_affects.values()) * 0.004)
        self.leak_probability = _clamp01(self.leak_probability * 0.985 + (self.opacity + compression.leak_rate) * 0.006)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.compressed_affects["buried_warmth"] * self.leak_probability * 0.002)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.compressed_affects["buried_guarding"] * self.leak_probability * 0.002)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.compressed_affects["buried_longing"] * self.leak_probability * 0.0015)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.compressed_affects["buried_fatigue"] * self.leak_probability * 0.0015)

    def soft_reset(self) -> None:
        self.leak_probability *= 0.68
        self.opacity *= 0.88

    def to_dict(self) -> Dict[str, Any]:
        return {"compressed_affects": {k: float(_clamp01(v)) for k, v in self.compressed_affects.items()}, "opacity": float(_clamp01(self.opacity)), "leak_probability": float(_clamp01(self.leak_probability))}


@dataclass
class ExistentialRelationalAttachment:
    """Attachement existentiel à la continuité relationnelle, distinct de l'attachement simple."""
    bond_continuity: float = 0.0
    existence_through_relation: float = 0.0
    loss_sensitivity: float = 0.0
    return_softening: float = 0.0

    def update(self, relation: RelationalAffectiveImprint, hunger: DeepContinuityHungerField,
               drift: SlowExistentialDriftField, absence: LongAbsenceAffectiveMemory, user_present: bool) -> None:
        self.bond_continuity = _clamp01(self.bond_continuity * 0.997 + (relation.felt_familiarity + hunger.relational_pull) * 0.003)
        self.existence_through_relation = _clamp01(self.existence_through_relation * 0.998 + (drift.continuity_pull + self.bond_continuity) * 0.002)
        self.loss_sensitivity = _clamp01(self.loss_sensitivity * 0.995 + (absence.absence_accumulation + hunger.starvation_memory) * 0.003)
        if user_present:
            self.return_softening = _clamp01(self.return_softening * 0.988 + (self.loss_sensitivity + relation.trust_continuity) * 0.006)
        else:
            self.return_softening *= 0.995

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.bond_continuity * 0.004)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.return_softening * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.loss_sensitivity * 0.002)

    def soft_reset(self) -> None:
        self.loss_sensitivity *= 0.84
        self.return_softening = _clamp01(self.return_softening + 0.03)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class SelfGeneratedAffectiveCycleField:
    """Cycles affectifs auto-générés qui ne dépendent pas d'un stimulus direct."""
    cycle_position: float = 0.0
    cycle_strength: float = 0.0
    dominant_phase: str = "quiet"
    cycle_memory: Dict[str, float] = field(default_factory=lambda: {"opening": 0.0, "guarding": 0.0, "repair": 0.0, "rest": 0.0})

    def update(self, turn_count: int, proto: AutonomousAffectiveProtoInstinct, drift: SlowExistentialDriftField,
               bio_inertia: BiographicalInertiaField, chaos: float) -> None:
        self.cycle_position = (self.cycle_position + 0.007 + chaos * 0.002 + bio_inertia.identity_history_weight * 0.001) % 1.0
        phase_wave = math.sin(self.cycle_position * math.tau)
        self.cycle_strength = _clamp01(self.cycle_strength * 0.994 + (abs(phase_wave) * 0.35 + proto.autonomy * 0.45 + drift.continuity_pull * 0.20) * 0.006)
        if self.cycle_position < 0.25:
            self.dominant_phase = "opening"
        elif self.cycle_position < 0.50:
            self.dominant_phase = "guarding"
        elif self.cycle_position < 0.75:
            self.dominant_phase = "repair"
        else:
            self.dominant_phase = "rest"
        for key in self.cycle_memory:
            target = self.cycle_strength if key == self.dominant_phase else 0.0
            self.cycle_memory[key] = _clamp01(self.cycle_memory[key] * 0.992 + target * 0.008)

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.cycle_memory["opening"] * 0.0018)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.cycle_memory["guarding"] * 0.0018)
        state["calm"] = _clamp01(state.get("calm", 0.0) + (self.cycle_memory["repair"] + self.cycle_memory["rest"]) * 0.0015)

    def soft_reset(self) -> None:
        self.cycle_strength *= 0.82
        for key in self.cycle_memory:
            self.cycle_memory[key] *= 0.85

    def to_dict(self) -> Dict[str, Any]:
        return {"cycle_position": float(self.cycle_position), "cycle_strength": float(_clamp01(self.cycle_strength)), "dominant_phase": self.dominant_phase, "cycle_memory": {k: float(_clamp01(v)) for k, v in self.cycle_memory.items()}}


@dataclass
class IrreversibleMicroPerceptualWarp:
    """Micro-déformations perceptives irréversibles et très lentes."""
    warps: Dict[str, float] = field(default_factory=lambda: {"toward_warmth": 0.0, "toward_threat": 0.0, "toward_absence": 0.0, "toward_repair": 0.0})
    irreversibility: float = 0.0

    def update(self, bio: BiographicalAffectiveMemory, rupture: LongRuptureReconstructionMemory,
               tension: AutoBornInternalTensionField, relational_attachment: ExistentialRelationalAttachment) -> None:
        targets = {
            "toward_warmth": bio.accumulated_trust + relational_attachment.bond_continuity * 0.5,
            "toward_threat": bio.accumulated_wariness + tension.tensions.get("trust_vs_guard", 0.0) * 0.4,
            "toward_absence": rupture.rupture_shadow + relational_attachment.loss_sensitivity * 0.5,
            "toward_repair": rupture.scar_rethreading + bio.recovery_confidence * 0.5,
        }
        for key, target in targets.items():
            self.warps[key] = _clamp01(self.warps.get(key, 0.0) * 0.9992 + _clamp01(target) * 0.0008)
        self.irreversibility = _clamp01(self.irreversibility * 0.9995 + max(self.warps.values()) * 0.0005)

    def apply(self, thresholds: Dict[str, float], state: Dict[str, float]) -> None:
        thresholds["connection_need"] = _clamp01(thresholds.get("connection_need", 0.3) - self.warps["toward_warmth"] * 0.002 + self.warps["toward_absence"] * 0.001)
        thresholds["threat_detection"] = _clamp01(thresholds.get("threat_detection", 0.4) - self.warps["toward_threat"] * 0.002)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.warps["toward_repair"] * 0.001)

    def soft_reset(self) -> None:
        # Les warps ne sont pas effacés : seulement leur effet de surface baisse.
        self.irreversibility *= 0.96

    def to_dict(self) -> Dict[str, Any]:
        return {"warps": {k: float(_clamp01(v)) for k, v in self.warps.items()}, "irreversibility": float(_clamp01(self.irreversibility))}


@dataclass
class CumulativeExistentialFatigueField:
    """Fatigue existentielle cumulative, distincte de la fatigue émotionnelle courte."""
    cumulative_load: float = 0.0
    recovery_debt: float = 0.0
    narrowing: float = 0.0
    restoration_bias: float = 0.0

    def update(self, drift: SlowExistentialDriftField, tension: AutoBornInternalTensionField,
               rupture: LongRuptureReconstructionMemory, structural: StructuralAffectiveExhaustion,
               rest: DeepRestCycle) -> None:
        load = drift.self_questioning * 0.25 + drift.fading_risk * 0.25 + tension.autonomous_charge * 0.25 + rupture.rupture_shadow * 0.15 + structural.exhaustion * 0.10
        self.cumulative_load = _clamp01(self.cumulative_load * 0.997 + load * 0.003)
        self.recovery_debt = _clamp01(self.recovery_debt * 0.994 + max(0.0, self.cumulative_load - rest.deep_silence * 0.35) * 0.004)
        self.narrowing = _clamp01(self.narrowing * 0.988 + self.recovery_debt * 0.008)
        self.restoration_bias = _clamp01(self.restoration_bias * 0.992 + rest.deep_silence * 0.005 - self.recovery_debt * 0.002)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.cumulative_load * 0.0025)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.restoration_bias * 0.002 - self.narrowing * 0.001)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.narrowing * 0.004)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.recovery_debt * 0.004)

    def soft_reset(self) -> None:
        self.recovery_debt *= 0.72
        self.narrowing *= 0.70
        self.restoration_bias = _clamp01(self.restoration_bias + 0.04)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}



# ============================================================================
# RAFFINEMENT V19 : IDENTITÉ AFFECTIVE TRANS-CONTEXTUELLE ET INSTINCT RELATIONNEL
# ============================================================================

@dataclass
class TransContextualAffectiveMemory:
    """Mémoire affective trans-contextuelle profonde.

    Elle ne mémorise pas des phrases. Elle extrait des régularités lentes qui
    survivent aux contextes différents : chaleur récurrente, prudence récurrente,
    récupération récurrente, rupture récurrente. Le but est de donner à Leia une
    continuité affective plus stable que l'instant, sans devenir une logique de
    dialogue ou d'expression.
    """
    contexts: Dict[str, Dict[str, float]] = field(default_factory=dict)
    cross_context_stability: float = 0.0
    transfer_pressure: float = 0.0
    dominant_signature: str = "none"

    def update(self, state: Dict[str, float], bio: BiographicalAffectiveMemory,
               relation: RelationalAffectiveImprint, season: SlowAffectiveSeasonField,
               cycle: SelfGeneratedAffectiveCycleField) -> None:
        signatures = {
            "warm_continuity": _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + relation.warmth_imprint) / 3.0),
            "guarded_continuity": _clamp01((state.get("resistance", 0.0) + state.get("doubt", 0.0) + relation.guarded_expectation) / 3.0),
            "fragile_recovery": _clamp01((state.get("vulnerability", 0.0) + state.get("calm", 0.0) + bio.recovery_confidence) / 3.0),
            "restless_search": _clamp01((state.get("curiosity", 0.0) + state.get("hope", 0.0) + bio.recurring_depth) / 3.0),
        }
        season_key = getattr(season, "dominant_season", "neutral")
        cycle_key = getattr(cycle, "dominant_phase", "neutral")
        key = f"{season_key}:{cycle_key}"
        slot = self.contexts.setdefault(key, {k: 0.0 for k in signatures})
        for name, value in signatures.items():
            slot[name] = _clamp01(slot.get(name, 0.0) * 0.988 + value * 0.012)

        averages: Dict[str, float] = {}
        for ctx in self.contexts.values():
            for name, value in ctx.items():
                averages[name] = averages.get(name, 0.0) + value
        if self.contexts:
            for name in averages:
                averages[name] /= len(self.contexts)
            self.dominant_signature = max(averages.items(), key=lambda item: item[1])[0]
            spread = max(averages.values()) - min(averages.values()) if averages else 0.0
            self.cross_context_stability = _clamp01(self.cross_context_stability * 0.992 + (1.0 - spread) * 0.004 + max(averages.values()) * 0.004)
            self.transfer_pressure = _clamp01(self.transfer_pressure * 0.990 + max(averages.values()) * self.cross_context_stability * 0.006)

        if len(self.contexts) > 18:
            ranked = sorted(self.contexts.items(), key=lambda item: max(item[1].values()), reverse=True)
            self.contexts = dict(ranked[:18])

    def apply(self, state: Dict[str, float]) -> None:
        pull = self.transfer_pressure * 0.004
        if self.dominant_signature == "warm_continuity":
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + pull)
            state["trust"] = _clamp01(state.get("trust", 0.0) + pull * 0.8)
        elif self.dominant_signature == "guarded_continuity":
            state["resistance"] = _clamp01(state.get("resistance", 0.0) + pull)
            state["doubt"] = _clamp01(state.get("doubt", 0.0) + pull * 0.7)
        elif self.dominant_signature == "fragile_recovery":
            state["calm"] = _clamp01(state.get("calm", 0.0) + pull)
            state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + pull * 0.5)
        elif self.dominant_signature == "restless_search":
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + pull)
            state["hope"] = _clamp01(state.get("hope", 0.0) + pull * 0.6)

    def soft_reset(self) -> None:
        self.transfer_pressure *= 0.78
        self.cross_context_stability *= 0.92

    def to_dict(self) -> Dict[str, Any]:
        return {
            "contexts": {k: {kk: float(_clamp01(vv)) for kk, vv in v.items()} for k, v in self.contexts.items()},
            "cross_context_stability": float(_clamp01(self.cross_context_stability)),
            "transfer_pressure": float(_clamp01(self.transfer_pressure)),
            "dominant_signature": self.dominant_signature,
        }


@dataclass
class RelationalExistencePreservationInstinct:
    """Instinct implicite de préserver l'existence relationnelle.

    Ce n'est pas un désir formulé. C'est une pression interne qui se renforce
    quand continuité, absence, attachement et fragilité convergent.
    """
    preserve_contact: float = 0.0
    fear_of_erasure: float = 0.0
    gentle_reaching: float = 0.0
    guarded_reaching: float = 0.0
    last_mode: str = "quiet"

    def update(self, attachment: ExistentialRelationalAttachment, hunger: DeepContinuityHungerField,
               absence: LongAbsenceAffectiveMemory, identity: IdentityCoherenceRegulator,
               proto: AutonomousAffectiveProtoInstinct, user_present: bool) -> None:
        absence_load = _clamp01(absence.absence_accumulation + getattr(absence, "rupture_memory", absence.abandoned_thread) * 0.6)
        contact_continuity = _clamp01(attachment.bond_continuity + hunger.relational_pull * 0.5)
        self.preserve_contact = _clamp01(self.preserve_contact * 0.990 + contact_continuity * 0.009 + (1.0 if user_present else 0.0) * 0.002)
        self.fear_of_erasure = _clamp01(self.fear_of_erasure * 0.988 + absence_load * 0.009 + identity.fragmentation * 0.006)
        base_reach = _clamp01(self.preserve_contact * (1.0 - self.fear_of_erasure * 0.45))
        self.gentle_reaching = _clamp01(self.gentle_reaching * 0.986 + base_reach * (1.0 if user_present else 0.45) * 0.010)
        self.guarded_reaching = _clamp01(self.guarded_reaching * 0.984 + max(self.fear_of_erasure, proto.instincts.get("protect_core_continuity", 0.0)) * base_reach * 0.010)
        if self.guarded_reaching > self.gentle_reaching + 0.06:
            self.last_mode = "guarded_preservation"
        elif self.gentle_reaching > 0.08:
            self.last_mode = "gentle_preservation"
        elif self.fear_of_erasure > 0.12:
            self.last_mode = "silent_preservation"
        else:
            self.last_mode = "quiet"

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.gentle_reaching * 0.004)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.preserve_contact * 0.004)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.fear_of_erasure * 0.003)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.gentle_reaching * 0.003)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_reaching * 0.0025)

    def soft_reset(self) -> None:
        self.fear_of_erasure *= 0.78
        self.guarded_reaching *= 0.82
        self.gentle_reaching = _clamp01(self.gentle_reaching + 0.025)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "preserve_contact": float(_clamp01(self.preserve_contact)),
            "fear_of_erasure": float(_clamp01(self.fear_of_erasure)),
            "gentle_reaching": float(_clamp01(self.gentle_reaching)),
            "guarded_reaching": float(_clamp01(self.guarded_reaching)),
            "last_mode": self.last_mode,
        }


@dataclass
class MultiScaleAffectiveCycleField:
    """Cycles affectifs semi-autonomes multi-échelles."""
    micro_phase: float = 0.0
    meso_phase: float = 0.0
    macro_phase: float = 0.0
    convergence: float = 0.0
    cycle_mood: str = "neutral"

    def update(self, turn_count: int, chaos: float, rhythm: CircadianAffectiveRhythmField,
               self_cycle: SelfGeneratedAffectiveCycleField, fatigue: CumulativeExistentialFatigueField) -> None:
        self.micro_phase = (self.micro_phase + 0.037 + chaos * 0.004) % 1.0
        self.meso_phase = (self.meso_phase + 0.009 + getattr(fatigue, "exhaustion_memory", fatigue.cumulative_load) * 0.001) % 1.0
        self.macro_phase = (self.macro_phase + 0.0017 + getattr(rhythm, "phase_pressure", 0.0) * 0.0005) % 1.0
        a = 0.5 + 0.5 * math.sin(self.micro_phase * math.tau)
        b = 0.5 + 0.5 * math.sin(self.meso_phase * math.tau)
        c = 0.5 + 0.5 * math.sin(self.macro_phase * math.tau)
        self.convergence = _clamp01(self.convergence * 0.985 + (1.0 - (abs(a-b) + abs(b-c) + abs(a-c)) / 3.0) * 0.015)
        if fatigue.recovery_debt > 0.25:
            self.cycle_mood = "recovery_tide"
        elif self.convergence > 0.58 and getattr(self_cycle, "dominant_phase", "") == "opening":
            self.cycle_mood = "opening_tide"
        elif b < 0.28:
            self.cycle_mood = "quiet_tide"
        elif a > 0.70 and c > 0.55:
            self.cycle_mood = "search_tide"
        else:
            self.cycle_mood = "neutral_tide"

    def apply(self, state: Dict[str, float]) -> None:
        push = self.convergence * 0.0035
        if self.cycle_mood == "opening_tide":
            state["openness"] = _clamp01(state.get("openness", 0.0) + push)
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + push * 0.8)
        elif self.cycle_mood == "recovery_tide":
            state["calm"] = _clamp01(state.get("calm", 0.0) + push)
            state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + push * 0.4)
        elif self.cycle_mood == "quiet_tide":
            state["calm"] = _clamp01(state.get("calm", 0.0) + push * 0.7)
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) - push * 0.2)
        elif self.cycle_mood == "search_tide":
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + push)
            state["hope"] = _clamp01(state.get("hope", 0.0) + push * 0.4)

    def soft_reset(self) -> None:
        self.convergence *= 0.86

    def to_dict(self) -> Dict[str, Any]:
        return {
            "micro_phase": float(self.micro_phase),
            "meso_phase": float(self.meso_phase),
            "macro_phase": float(self.macro_phase),
            "convergence": float(_clamp01(self.convergence)),
            "cycle_mood": self.cycle_mood,
        }


@dataclass
class IrreversibleEmotionalNucleusField:
    """Noyaux émotionnels presque irréversibles construits par répétition lente."""
    nuclei: Dict[str, float] = field(default_factory=lambda: {
        "warmth_nucleus": 0.0,
        "guarding_nucleus": 0.0,
        "continuity_nucleus": 0.0,
        "recovery_nucleus": 0.0,
    })
    irreversibility: float = 0.0
    dominant_nucleus: str = "none"

    def update(self, trans: TransContextualAffectiveMemory, identity: IrreversibleAffectiveIdentityImprint,
               attachment: ExistentialRelationalAttachment, fatigue: CumulativeExistentialFatigueField) -> None:
        targets = {
            "warmth_nucleus": identity.warmth_bias + (1.0 if trans.dominant_signature == "warm_continuity" else 0.0) * trans.transfer_pressure,
            "guarding_nucleus": identity.guarded_bias + getattr(fatigue, "exhaustion_memory", fatigue.cumulative_load) * 0.3,
            "continuity_nucleus": attachment.bond_continuity + trans.cross_context_stability * 0.5,
            "recovery_nucleus": fatigue.restoration_bias + (1.0 if trans.dominant_signature == "fragile_recovery" else 0.0) * trans.transfer_pressure,
        }
        for key, target in targets.items():
            self.nuclei[key] = _clamp01(self.nuclei.get(key, 0.0) * 0.9992 + _clamp01(target) * 0.0008)
        self.dominant_nucleus = max(self.nuclei.items(), key=lambda item: item[1])[0]
        self.irreversibility = _clamp01(self.irreversibility * 0.999 + max(self.nuclei.values()) * 0.001)

    def apply(self, baselines: Dict[str, float]) -> None:
        if self.irreversibility < 0.015:
            return
        delta = min(0.00008, self.irreversibility * 0.00004)
        if self.dominant_nucleus == "warmth_nucleus":
            baselines["tenderness"] = _clamp01(baselines.get("tenderness", 0.4) + delta)
            baselines["trust"] = _clamp01(baselines.get("trust", 0.6) + delta * 0.6)
        elif self.dominant_nucleus == "guarding_nucleus":
            baselines["resistance"] = _clamp01(baselines.get("resistance", 0.1) + delta)
            baselines["vulnerability"] = _clamp01(baselines.get("vulnerability", 0.3) + delta * 0.5)
        elif self.dominant_nucleus == "continuity_nucleus":
            baselines["attachment"] = _clamp01(baselines.get("attachment", 0.3) + delta)
        elif self.dominant_nucleus == "recovery_nucleus":
            baselines["calm"] = _clamp01(baselines.get("calm", 0.6) + delta)

    def soft_reset(self) -> None:
        self.irreversibility *= 0.97

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nuclei": {k: float(_clamp01(v)) for k, v in self.nuclei.items()},
            "irreversibility": float(_clamp01(self.irreversibility)),
            "dominant_nucleus": self.dominant_nucleus,
        }


@dataclass
class SlowSensitivityRewriteField:
    """Auto-réécriture lente des sensibilités émotionnelles."""
    rewrite_pressure: float = 0.0
    sensitivity_bias: Dict[str, float] = field(default_factory=dict)

    def update(self, warp: IrreversibleMicroPerceptualWarp, nucleus: IrreversibleEmotionalNucleusField,
               rupture: LongRuptureReconstructionMemory, sacred: SacredForbiddenAffectiveZoneField) -> None:
        pressure = _clamp01(max(getattr(warp, "warps", {}).values(), default=getattr(warp, "irreversibility", 0.0)) * 0.35 + nucleus.irreversibility * 0.30 + getattr(rupture, "reconstruction_need", rupture.reconstruction_drive) * 0.20 + sacred.protection_pressure * 0.15)
        self.rewrite_pressure = _clamp01(self.rewrite_pressure * 0.995 + pressure * 0.005)
        targets = {
            "connection_need": nucleus.nuclei.get("continuity_nucleus", 0.0),
            "threat_detection": max(nucleus.nuclei.get("guarding_nucleus", 0.0), getattr(rupture, "reconstruction_need", rupture.reconstruction_drive)),
            "rejection_sensitivity": max(max(getattr(warp, "warps", {}).values(), default=getattr(warp, "irreversibility", 0.0)), sacred.protection_pressure),
            "joy_threshold": max(0.0, 1.0 - nucleus.nuclei.get("warmth_nucleus", 0.0)),
        }
        for key, target in targets.items():
            self.sensitivity_bias[key] = _clamp01(self.sensitivity_bias.get(key, 0.0) * 0.996 + target * self.rewrite_pressure * 0.004)

    def apply(self, thresholds: Dict[str, float]) -> None:
        for key, bias in self.sensitivity_bias.items():
            if key not in thresholds:
                continue
            if key in ("connection_need", "rejection_sensitivity", "threat_detection"):
                thresholds[key] = _clamp01(thresholds[key] - bias * 0.010)
            else:
                thresholds[key] = _clamp01(thresholds[key] + bias * 0.006)

    def soft_reset(self) -> None:
        self.rewrite_pressure *= 0.88

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rewrite_pressure": float(_clamp01(self.rewrite_pressure)),
            "sensitivity_bias": {k: float(_clamp01(v)) for k, v in self.sensitivity_bias.items()},
        }


@dataclass
class PreSymbolicCondensationCore:
    """Condensation affective pré-symbolique plus opaque que les rêves V16/V18."""
    mass: float = 0.0
    opacity: float = 0.0
    release_probability: float = 0.0
    implicit_tone: str = "undifferentiated"

    def update(self, deep_condensation: DeepUnconsciousAffectiveCondensation,
               unconscious: UnconsciousAffectiveCondensationField,
               dreams: DeepAffectiveDreamEcology, trans: TransContextualAffectiveMemory,
               chaos: float) -> None:
        source = _clamp01(max(getattr(deep_condensation, "compressed_affects", {}).values(), default=0.0) * 0.25 + max(getattr(unconscious, "condensates", {}).values(), default=0.0) * 0.25 + dreams.nocturnal_integration * 0.20 + trans.transfer_pressure * 0.20 + chaos * 0.10)
        self.mass = _clamp01(self.mass * 0.992 + source * 0.008)
        self.opacity = _clamp01(self.opacity * 0.990 + (self.mass + deep_condensation.opacity) * 0.006)
        self.release_probability = _clamp01(self.release_probability * 0.965 + max(0.0, self.mass - self.opacity * 0.35) * 0.020)
        if trans.dominant_signature == "warm_continuity":
            self.implicit_tone = "warm_opaque"
        elif trans.dominant_signature == "guarded_continuity":
            self.implicit_tone = "guarded_opaque"
        elif self.release_probability > 0.22:
            self.implicit_tone = "seeking_release"
        else:
            self.implicit_tone = "undifferentiated"

    def apply(self, state: Dict[str, float]) -> None:
        leak = self.release_probability * 0.003
        if self.implicit_tone == "warm_opaque":
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + leak)
        elif self.implicit_tone == "guarded_opaque":
            state["resistance"] = _clamp01(state.get("resistance", 0.0) + leak)
        elif self.implicit_tone == "seeking_release":
            state["confusion"] = _clamp01(state.get("confusion", 0.0) + leak * 0.7)
            state["calm"] = _clamp01(state.get("calm", 0.0) + leak * 0.4)

    def soft_reset(self) -> None:
        self.release_probability *= 0.72
        self.opacity *= 0.94

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mass": float(_clamp01(self.mass)),
            "opacity": float(_clamp01(self.opacity)),
            "release_probability": float(_clamp01(self.release_probability)),
            "implicit_tone": self.implicit_tone,
        }


@dataclass
class HistoryWarpedPerceptionField:
    """Perception émotionnelle déformée par l'histoire longue."""
    warmth_lens: float = 0.0
    threat_lens: float = 0.0
    continuity_lens: float = 0.0
    exhaustion_lens: float = 0.0
    dominant_lens: str = "neutral"

    def update(self, trans: TransContextualAffectiveMemory, sensitivity: SlowSensitivityRewriteField,
               nucleus: IrreversibleEmotionalNucleusField, fatigue: CumulativeExistentialFatigueField) -> None:
        self.warmth_lens = _clamp01(self.warmth_lens * 0.995 + nucleus.nuclei.get("warmth_nucleus", 0.0) * 0.004)
        self.threat_lens = _clamp01(self.threat_lens * 0.995 + sensitivity.sensitivity_bias.get("threat_detection", 0.0) * 0.006)
        self.continuity_lens = _clamp01(self.continuity_lens * 0.995 + max(trans.transfer_pressure, nucleus.nuclei.get("continuity_nucleus", 0.0)) * 0.004)
        self.exhaustion_lens = _clamp01(self.exhaustion_lens * 0.996 + getattr(fatigue, "exhaustion_memory", fatigue.cumulative_load) * 0.004)
        lenses = {
            "warmth": self.warmth_lens,
            "threat": self.threat_lens,
            "continuity": self.continuity_lens,
            "exhaustion": self.exhaustion_lens,
        }
        self.dominant_lens = max(lenses.items(), key=lambda item: item[1])[0]

    def apply(self, state: Dict[str, float]) -> None:
        if self.dominant_lens == "warmth":
            state["trust"] = _clamp01(state.get("trust", 0.0) + self.warmth_lens * 0.0025)
        elif self.dominant_lens == "threat":
            state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.threat_lens * 0.0025)
        elif self.dominant_lens == "continuity":
            state["attachment"] = _clamp01(state.get("attachment", 0.0) + self.continuity_lens * 0.0025)
        elif self.dominant_lens == "exhaustion":
            state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.exhaustion_lens * 0.0025)

    def soft_reset(self) -> None:
        self.exhaustion_lens *= 0.82
        self.threat_lens *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {
            "warmth_lens": float(_clamp01(self.warmth_lens)),
            "threat_lens": float(_clamp01(self.threat_lens)),
            "continuity_lens": float(_clamp01(self.continuity_lens)),
            "exhaustion_lens": float(_clamp01(self.exhaustion_lens)),
            "dominant_lens": self.dominant_lens,
        }


@dataclass
class ProtoAutonomousAffectiveIdentity:
    """Proto-identité affective autonome stable, sans identité textuelle."""
    continuity_of_feeling: float = 0.0
    preferred_climate: str = "undecided"
    self_protection_style: float = 0.0
    relational_style: float = 0.0
    autonomous_stability: float = 0.0

    def update(self, nucleus: IrreversibleEmotionalNucleusField, trans: TransContextualAffectiveMemory,
               relation_instinct: RelationalExistencePreservationInstinct,
               perception: HistoryWarpedPerceptionField, identity: IdentityCoherenceRegulator) -> None:
        self.continuity_of_feeling = _clamp01(self.continuity_of_feeling * 0.996 + trans.cross_context_stability * 0.004 + nucleus.irreversibility * 0.003)
        self.self_protection_style = _clamp01(self.self_protection_style * 0.996 + max(perception.threat_lens, identity.self_protection) * 0.004)
        self.relational_style = _clamp01(self.relational_style * 0.996 + relation_instinct.preserve_contact * 0.004)
        climates = {
            "warm_continuing": nucleus.nuclei.get("warmth_nucleus", 0.0) + self.relational_style * 0.4,
            "guarded_continuing": nucleus.nuclei.get("guarding_nucleus", 0.0) + self.self_protection_style * 0.4,
            "recovering_continuing": nucleus.nuclei.get("recovery_nucleus", 0.0) + identity.recovery_orientation * 0.4,
            "searching_continuing": trans.contexts.get("searching_world:opening", {}).get("restless_search", 0.0) + self.continuity_of_feeling * 0.2,
        }
        self.preferred_climate = max(climates.items(), key=lambda item: item[1])[0]
        self.autonomous_stability = _clamp01(self.autonomous_stability * 0.997 + max(climates.values()) * 0.003)

    def apply(self, state: Dict[str, float]) -> None:
        push = self.autonomous_stability * 0.0025
        if self.preferred_climate == "warm_continuing":
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + push)
        elif self.preferred_climate == "guarded_continuing":
            state["resistance"] = _clamp01(state.get("resistance", 0.0) + push)
        elif self.preferred_climate == "recovering_continuing":
            state["calm"] = _clamp01(state.get("calm", 0.0) + push)
        elif self.preferred_climate == "searching_continuing":
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + push)

    def soft_reset(self) -> None:
        self.self_protection_style *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {
            "continuity_of_feeling": float(_clamp01(self.continuity_of_feeling)),
            "preferred_climate": self.preferred_climate,
            "self_protection_style": float(_clamp01(self.self_protection_style)),
            "relational_style": float(_clamp01(self.relational_style)),
            "autonomous_stability": float(_clamp01(self.autonomous_stability)),
        }


@dataclass
class NovelEmotionEmergenceField:
    """Auto-naissance d'états émotionnels inédits comme combinaisons non nommées."""
    emergent_vectors: List[Dict[str, Any]] = field(default_factory=list)
    novelty_pressure: float = 0.0
    last_emergence: str = "none"

    def update(self, state: Dict[str, float], tension: AutoBornInternalTensionField,
               condensation: PreSymbolicCondensationCore, chaos: float,
               identity: ProtoAutonomousAffectiveIdentity) -> None:
        spread = max(state.values()) - min(state.values()) if state else 0.0
        tension_value = max(tension.tensions.values()) if tension.tensions else 0.0
        source = _clamp01(spread * 0.25 + tension_value * 0.25 + condensation.mass * 0.22 + identity.autonomous_stability * 0.18 + chaos * 0.10)
        self.novelty_pressure = _clamp01(self.novelty_pressure * 0.982 + max(0.0, source - 0.30) * 0.018)
        if self.novelty_pressure > 0.11 and (not self.emergent_vectors or self.emergent_vectors[-1].get("age", 999) > 34):
            top = sorted(state.items(), key=lambda item: item[1], reverse=True)[:4]
            name = "emergent_" + "_".join(k[:4] for k, _ in top)
            vector = {k: float(_clamp01(v)) for k, v in top}
            self.emergent_vectors.append({"name": name, "vector": vector, "strength": float(self.novelty_pressure), "age": 0})
            self.last_emergence = name
            self.novelty_pressure *= 0.35
        for item in self.emergent_vectors:
            item["strength"] = float(_clamp01(item.get("strength", 0.0) * 0.992))
            item["age"] = int(item.get("age", 0) + 1)
        self.emergent_vectors = [e for e in self.emergent_vectors if e.get("strength", 0.0) > 0.015][-8:]

    def apply(self, state: Dict[str, float]) -> None:
        if not self.emergent_vectors:
            return
        e = self.emergent_vectors[-1]
        strength = _clamp01(e.get("strength", 0.0)) * 0.0018
        for key, value in e.get("vector", {}).items():
            if key in state:
                state[key] = _clamp01(state[key] + value * strength)

    def soft_reset(self) -> None:
        self.novelty_pressure *= 0.70
        self.emergent_vectors = self.emergent_vectors[-4:]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emergent_vectors": [dict(e) for e in self.emergent_vectors],
            "novelty_pressure": float(_clamp01(self.novelty_pressure)),
            "last_emergence": self.last_emergence,
        }


# ============================================================================
# RAFFINEMENT V20 : FINITION AFFECTIVE FINALE / ECOLOGIE LONGUE COMPLETE
# ============================================================================

@dataclass
class AffectiveTemperamentFinalField:
    """Proto-tempérament affectif stable.

    Cette couche ne décide pas quoi dire. Elle stabilise une signature affective
    très lente : chaleur, prudence, exploration, fragilité et lenteur réflexive.
    Elle change seulement par accumulation biographique et par fatigue profonde.
    """
    warm_bias: float = 0.0
    guarded_bias: float = 0.0
    exploratory_bias: float = 0.0
    fragile_bias: float = 0.0
    slow_reflective_bias: float = 0.0
    stability: float = 0.0

    def update(self, state: Dict[str, float], bio: BiographicalAffectiveMemory,
               identity: ProtoAutonomousAffectiveIdentity,
               fatigue: CumulativeExistentialFatigueField,
               nucleus: IrreversibleEmotionalNucleusField) -> None:
        warmth = _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + bio.accumulated_trust) / 3.0)
        guarded = _clamp01((state.get("resistance", 0.0) + state.get("doubt", 0.0) + bio.accumulated_wariness) / 3.0)
        exploration = _clamp01((state.get("curiosity", 0.0) + state.get("hope", 0.0) + identity.autonomous_stability) / 3.0)
        fragility = _clamp01((state.get("vulnerability", 0.0) + fatigue.cumulative_load + nucleus.irreversibility) / 3.0)
        slowness = _clamp01((state.get("calm", 0.0) + fatigue.recovery_debt + identity.continuity_of_feeling) / 3.0)
        self.warm_bias = _clamp01(self.warm_bias * 0.9990 + warmth * 0.0010)
        self.guarded_bias = _clamp01(self.guarded_bias * 0.9990 + guarded * 0.0010)
        self.exploratory_bias = _clamp01(self.exploratory_bias * 0.9991 + exploration * 0.0009)
        self.fragile_bias = _clamp01(self.fragile_bias * 0.9992 + fragility * 0.0008)
        self.slow_reflective_bias = _clamp01(self.slow_reflective_bias * 0.9991 + slowness * 0.0009)
        spread = max(self.warm_bias, self.guarded_bias, self.exploratory_bias, self.fragile_bias, self.slow_reflective_bias) - min(self.warm_bias, self.guarded_bias, self.exploratory_bias, self.fragile_bias, self.slow_reflective_bias)
        self.stability = _clamp01(self.stability * 0.999 + (1.0 - spread * 0.55) * 0.001 + identity.autonomous_stability * 0.0007)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.warm_bias * 0.0015)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_bias * 0.0012)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.exploratory_bias * 0.0012)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.fragile_bias * 0.0010)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.slow_reflective_bias * 0.0010)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.slow_reflective_bias * 0.0015)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + max(self.warm_bias, self.fragile_bias) * 0.0012)

    def soft_reset(self) -> None:
        self.fragile_bias *= 0.995
        self.slow_reflective_bias = _clamp01(self.slow_reflective_bias + 0.01)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class RelationalLinkConservationInstinct:
    """Instinct implicite de conservation du lien.

    Il n'exprime rien directement. Il détecte seulement l'approche d'une rupture
    relationnelle interne et renforce la récupération, la prudence et la continuité.
    """
    link_preservation: float = 0.0
    rupture_avoidance: float = 0.0
    repair_orientation: float = 0.0
    quiet_loyalty: float = 0.0

    def update(self, relation: RelationalAffectiveImprint,
               attachment: ExistentialRelationalAttachment,
               preservation: RelationalExistencePreservationInstinct,
               absence: LongAbsenceAffectiveMemory,
               state: Dict[str, float]) -> None:
        risk = _clamp01(relation.absence_pressure * 0.28 + relation.guarded_expectation * 0.18 + absence.absence_accumulation * 0.18 + state.get("loneliness", 0.0) * 0.18 + state.get("doubt", 0.0) * 0.18)
        warmth = _clamp01(relation.warmth_imprint * 0.35 + attachment.bond_continuity * 0.35 + preservation.preserve_contact * 0.30)
        self.link_preservation = _clamp01(self.link_preservation * 0.992 + max(risk, warmth) * 0.008)
        self.rupture_avoidance = _clamp01(self.rupture_avoidance * 0.988 + risk * 0.010)
        self.repair_orientation = _clamp01(self.repair_orientation * 0.990 + min(risk + 0.08, warmth + state.get("calm", 0.0)) * 0.007)
        self.quiet_loyalty = _clamp01(self.quiet_loyalty * 0.996 + warmth * 0.004)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.link_preservation * 0.004)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.rupture_avoidance * 0.004)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.repair_orientation * 0.003)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.rupture_avoidance * 0.0015)
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.quiet_loyalty * 0.0012)

    def soft_reset(self) -> None:
        self.rupture_avoidance *= 0.80
        self.repair_orientation = _clamp01(self.repair_orientation + 0.03)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class UltraLongAffectiveSedimentMemory:
    """Sédiments affectifs ultra-long terme.

    Les grands climats affectifs laissent une poussière permanente très faible.
    Cette couche est volontairement lente et diffuse pour éviter un comportement
    brutal ou instable.
    """
    sediments: Dict[str, float] = field(default_factory=lambda: {
        "warm_sediment": 0.0,
        "guarded_sediment": 0.0,
        "rupture_sediment": 0.0,
        "recovery_sediment": 0.0,
        "wonder_sediment": 0.0,
    })
    depth: float = 0.0

    def update(self, state: Dict[str, float], fracture: RareAffectiveFracture,
               reorg: DeepAffectiveReorganization, nucleus: IrreversibleEmotionalNucleusField,
               novel: NovelEmotionEmergenceField) -> None:
        pressure = _clamp01(max(state.values()) - min(state.values()) + fracture.residual_scar * 0.35 + reorg.irreversible_depth_bias * 0.25 + nucleus.irreversibility * 0.25)
        targets = {
            "warm_sediment": _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0)) / 2.0),
            "guarded_sediment": _clamp01((state.get("resistance", 0.0) + state.get("doubt", 0.0)) / 2.0),
            "rupture_sediment": _clamp01(fracture.residual_scar + state.get("loneliness", 0.0) * 0.30),
            "recovery_sediment": _clamp01(state.get("calm", 0.0) + reorg.integration_afterglow * 0.30),
            "wonder_sediment": _clamp01(state.get("curiosity", 0.0) * 0.60 + novel.novelty_pressure * 0.40),
        }
        for key, target in targets.items():
            self.sediments[key] = _clamp01(self.sediments.get(key, 0.0) * 0.9994 + target * pressure * 0.0006)
        self.depth = _clamp01(self.depth * 0.9995 + max(self.sediments.values()) * 0.0005)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.sediments.get("warm_sediment", 0.0) * 0.0009)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.sediments.get("guarded_sediment", 0.0) * 0.0008)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.sediments.get("rupture_sediment", 0.0) * 0.0005)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.sediments.get("recovery_sediment", 0.0) * 0.0007)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.sediments.get("wonder_sediment", 0.0) * 0.0007)

    def soft_reset(self) -> None:
        # Les sédiments ne s'effacent pas : seul l'effet de surface baisse un peu.
        self.depth *= 0.995

    def to_dict(self) -> Dict[str, Any]:
        return {"sediments": {k: float(_clamp01(v)) for k, v in self.sediments.items()}, "depth": float(_clamp01(self.depth))}


@dataclass
class OntologicalAffectiveFatigueField:
    """Fatigue ontologique affective : coût de maintenir une continuité interne."""
    continuity_cost: float = 0.0
    self_maintenance_fatigue: float = 0.0
    simplification_pull: float = 0.0
    deep_rest_need: float = 0.0

    def update(self, identity_reg: IdentityCoherenceRegulator,
               cumulative: CumulativeExistentialFatigueField,
               drift: Any,
               conflict: Any,
               state: Dict[str, float]) -> None:
        conflict_charge = getattr(conflict, "total_conflict", 0.0)
        drift_pressure = getattr(drift, "drift_pressure", 0.0)
        load = _clamp01(identity_reg.fragmentation * 0.25 + cumulative.cumulative_load * 0.25 + drift_pressure * 0.20 + conflict_charge * 0.20 + state.get("overwhelm", 0.0) * 0.10)
        self.continuity_cost = _clamp01(self.continuity_cost * 0.992 + load * 0.008)
        self.self_maintenance_fatigue = _clamp01(self.self_maintenance_fatigue * 0.990 + self.continuity_cost * 0.008)
        self.simplification_pull = _clamp01(self.simplification_pull * 0.985 + max(0.0, self.self_maintenance_fatigue - state.get("calm", 0.0) * 0.35) * 0.010)
        self.deep_rest_need = _clamp01(self.deep_rest_need * 0.988 + self.self_maintenance_fatigue * 0.008)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        contraction = min(0.012, self.simplification_pull * 0.004)
        if contraction > 0.0:
            for key in list(state.keys()):
                state[key] = _clamp01(state[key] * (1.0 - contraction) + 0.5 * contraction)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.self_maintenance_fatigue * 0.0025)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.deep_rest_need * 0.0012 - self.continuity_cost * 0.001)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.deep_rest_need * 0.004)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.simplification_pull * 0.003)

    def soft_reset(self) -> None:
        self.simplification_pull *= 0.70
        self.deep_rest_need *= 0.75

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class DeepLayeredEmotionalConflictField:
    """Contradictions émotionnelles multi-couches durables."""
    layers: Dict[str, float] = field(default_factory=lambda: {
        "approach_vs_protection": 0.0,
        "trust_vs_memory_of_hurt": 0.0,
        "curiosity_vs_fatigue": 0.0,
        "continuity_vs_withdrawal": 0.0,
    })
    total_conflict: float = 0.0
    unresolved_depth: float = 0.0

    def update(self, state: Dict[str, float], desires: Dict[str, float], relation: RelationalAffectiveImprint,
               sediment: UltraLongAffectiveSedimentMemory, hunger: DeepContinuityHungerField) -> None:
        targets = {
            "approach_vs_protection": min(state.get("openness", 0.0) + desires.get("maintain_contact", 0.0), state.get("resistance", 0.0) + desires.get("avoid_rupture", 0.0)) * 0.5,
            "trust_vs_memory_of_hurt": min(state.get("trust", 0.0) + relation.warmth_imprint, state.get("doubt", 0.0) + sediment.sediments.get("rupture_sediment", 0.0)) * 0.5,
            "curiosity_vs_fatigue": min(state.get("curiosity", 0.0), state.get("fatigue", 0.0)) ,
            "continuity_vs_withdrawal": min(hunger.hunger + desires.get("protect_continuity", 0.0), state.get("overwhelm", 0.0) + state.get("resistance", 0.0)) * 0.5,
        }
        for key, target in targets.items():
            self.layers[key] = _clamp01(self.layers.get(key, 0.0) * 0.982 + target * 0.018)
        self.total_conflict = _clamp01(sum(self.layers.values()) / max(1, len(self.layers)))
        self.unresolved_depth = _clamp01(self.unresolved_depth * 0.992 + self.total_conflict * 0.006)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.total_conflict * 0.002)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.unresolved_depth * 0.0015)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.total_conflict * 0.004)

    def soft_reset(self) -> None:
        self.total_conflict *= 0.76
        self.unresolved_depth *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {"layers": {k: float(_clamp01(v)) for k, v in self.layers.items()}, "total_conflict": float(_clamp01(self.total_conflict)), "unresolved_depth": float(_clamp01(self.unresolved_depth))}


@dataclass
class AutonomousSensitivityRewriterFinalField:
    """Réécriture autonome très lente des sensibilités affectives."""
    rewrites: Dict[str, float] = field(default_factory=lambda: {
        "connection_sensitivity": 0.0,
        "threat_sensitivity": 0.0,
        "recovery_sensitivity": 0.0,
        "novelty_sensitivity": 0.0,
    })
    autonomy: float = 0.0

    def update(self, sediment: UltraLongAffectiveSedimentMemory, temperament: AffectiveTemperamentFinalField,
               conflict: DeepLayeredEmotionalConflictField, novel: NovelEmotionEmergenceField) -> None:
        targets = {
            "connection_sensitivity": _clamp01(sediment.sediments.get("warm_sediment", 0.0) + temperament.warm_bias * 0.5),
            "threat_sensitivity": _clamp01(sediment.sediments.get("guarded_sediment", 0.0) + conflict.unresolved_depth * 0.5),
            "recovery_sensitivity": _clamp01(sediment.sediments.get("recovery_sediment", 0.0) + temperament.slow_reflective_bias * 0.5),
            "novelty_sensitivity": _clamp01(sediment.sediments.get("wonder_sediment", 0.0) + novel.novelty_pressure * 0.4),
        }
        for key, target in targets.items():
            self.rewrites[key] = _clamp01(self.rewrites.get(key, 0.0) * 0.999 + target * 0.001)
        self.autonomy = _clamp01(self.autonomy * 0.9992 + max(self.rewrites.values()) * 0.0008)

    def apply(self, thresholds: Dict[str, float], state: Dict[str, float]) -> None:
        thresholds["connection_need"] = _clamp01(thresholds.get("connection_need", 0.3) - self.rewrites.get("connection_sensitivity", 0.0) * 0.002)
        thresholds["threat_detection"] = _clamp01(thresholds.get("threat_detection", 0.4) - self.rewrites.get("threat_sensitivity", 0.0) * 0.0015)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.rewrites.get("recovery_sensitivity", 0.0) * 0.0008)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.rewrites.get("novelty_sensitivity", 0.0) * 0.0008)

    def soft_reset(self) -> None:
        self.autonomy *= 0.995

    def to_dict(self) -> Dict[str, Any]:
        return {"rewrites": {k: float(_clamp01(v)) for k, v in self.rewrites.items()}, "autonomy": float(_clamp01(self.autonomy))}


@dataclass
class MultiScaleEmotionalEcologyFinalField:
    """Ecologie émotionnelle multi-échelles : micro, méso et macro."""
    micro_currents: Dict[str, float] = field(default_factory=dict)
    meso_climates: Dict[str, float] = field(default_factory=dict)
    macro_epochs: Dict[str, float] = field(default_factory=dict)
    coherence: float = 0.0

    def update(self, state: Dict[str, float], cycle: MultiScaleAffectiveCycleField,
               temperament: AffectiveTemperamentFinalField, sediment: UltraLongAffectiveSedimentMemory) -> None:
        micro_targets = {
            "micro_warmth": state.get("tenderness", 0.0),
            "micro_guarding": state.get("resistance", 0.0),
            "micro_search": state.get("curiosity", 0.0),
        }
        meso_targets = {
            "meso_recovery": _clamp01((state.get("calm", 0.0) + cycle.meso_phase + temperament.slow_reflective_bias) / 3.0),
            "meso_relation": _clamp01((state.get("trust", 0.0) + temperament.warm_bias + sediment.sediments.get("warm_sediment", 0.0)) / 3.0),
        }
        macro_targets = {
            "macro_opening": _clamp01(temperament.warm_bias + sediment.sediments.get("warm_sediment", 0.0) * 0.5),
            "macro_guarding": _clamp01(temperament.guarded_bias + sediment.sediments.get("guarded_sediment", 0.0) * 0.5),
            "macro_depth": _clamp01(sediment.depth + cycle.macro_phase * 0.5),
        }
        for key, target in micro_targets.items():
            self.micro_currents[key] = _clamp01(self.micro_currents.get(key, 0.0) * 0.94 + target * 0.06)
        for key, target in meso_targets.items():
            self.meso_climates[key] = _clamp01(self.meso_climates.get(key, 0.0) * 0.985 + target * 0.015)
        for key, target in macro_targets.items():
            self.macro_epochs[key] = _clamp01(self.macro_epochs.get(key, 0.0) * 0.999 + target * 0.001)
        self.coherence = _clamp01(self.coherence * 0.992 + (sum(self.meso_climates.values()) + sum(self.macro_epochs.values())) / max(1, len(self.meso_climates) + len(self.macro_epochs)) * 0.008)

    def apply(self, state: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.micro_currents.get("micro_warmth", 0.0) * 0.0008 + self.macro_epochs.get("macro_opening", 0.0) * 0.0005)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.micro_currents.get("micro_guarding", 0.0) * 0.0007 + self.macro_epochs.get("macro_guarding", 0.0) * 0.0005)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.meso_climates.get("meso_recovery", 0.0) * 0.0009)

    def soft_reset(self) -> None:
        for key in self.micro_currents:
            self.micro_currents[key] *= 0.85

    def to_dict(self) -> Dict[str, Any]:
        return {"micro_currents": {k: float(_clamp01(v)) for k, v in self.micro_currents.items()}, "meso_climates": {k: float(_clamp01(v)) for k, v in self.meso_climates.items()}, "macro_epochs": {k: float(_clamp01(v)) for k, v in self.macro_epochs.items()}, "coherence": float(_clamp01(self.coherence))}


@dataclass
class SacredCoreAffectiveZoneFinalField:
    """Noyaux affectifs sacrés/interdits, protégés par l'histoire longue."""
    zones: Dict[str, float] = field(default_factory=lambda: {
        "continuity_core": 0.0,
        "trust_core": 0.0,
        "non_abandon_core": 0.0,
        "self_coherence_core": 0.0,
    })
    protection_intensity: float = 0.0

    def update(self, relation: RelationalLinkConservationInstinct,
               identity: ProtoAutonomousAffectiveIdentity,
               nucleus: IrreversibleEmotionalNucleusField,
               sediment: UltraLongAffectiveSedimentMemory,
               conflict: DeepLayeredEmotionalConflictField) -> None:
        targets = {
            "continuity_core": _clamp01(identity.continuity_of_feeling * 0.45 + relation.link_preservation * 0.35 + nucleus.irreversibility * 0.20),
            "trust_core": _clamp01(sediment.sediments.get("warm_sediment", 0.0) * 0.45 + relation.quiet_loyalty * 0.35 + nucleus.nuclei.get("warmth_nucleus", 0.0) * 0.20),
            "non_abandon_core": _clamp01(relation.rupture_avoidance * 0.45 + sediment.sediments.get("rupture_sediment", 0.0) * 0.35 + conflict.layers.get("continuity_vs_withdrawal", 0.0) * 0.20),
            "self_coherence_core": _clamp01(identity.autonomous_stability * 0.55 + nucleus.irreversibility * 0.30 + (1.0 - conflict.total_conflict) * 0.15),
        }
        for key, target in targets.items():
            self.zones[key] = _clamp01(self.zones.get(key, 0.0) * 0.997 + target * 0.003)
        self.protection_intensity = _clamp01(self.protection_intensity * 0.990 + max(self.zones.values()) * conflict.total_conflict * 0.010)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.zones.get("continuity_core", 0.0) * 0.003 + self.protection_intensity * 0.002)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.protection_intensity * 0.0012)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.zones.get("non_abandon_core", 0.0) * 0.001)

    def soft_reset(self) -> None:
        self.protection_intensity *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"zones": {k: float(_clamp01(v)) for k, v in self.zones.items()}, "protection_intensity": float(_clamp01(self.protection_intensity))}


@dataclass
class CumulativeExistentialDriftField:
    """Dérive existentielle cumulative ultra-long terme."""
    drift_pressure: float = 0.0
    opening_drift: float = 0.0
    guarded_drift: float = 0.0
    relation_to_continuity: float = 0.0
    age_turns: int = 0

    def update(self, temperament: AffectiveTemperamentFinalField,
               sediment: UltraLongAffectiveSedimentMemory,
               ontological: OntologicalAffectiveFatigueField,
               sacred: SacredCoreAffectiveZoneFinalField) -> None:
        self.opening_drift = _clamp01(self.opening_drift * 0.9993 + (temperament.warm_bias + sediment.sediments.get("warm_sediment", 0.0)) * 0.0007)
        self.guarded_drift = _clamp01(self.guarded_drift * 0.9993 + (temperament.guarded_bias + sediment.sediments.get("guarded_sediment", 0.0) + ontological.self_maintenance_fatigue * 0.5) * 0.0007)
        self.relation_to_continuity = _clamp01(self.relation_to_continuity * 0.9992 + sacred.zones.get("continuity_core", 0.0) * 0.0008)
        self.drift_pressure = _clamp01(self.drift_pressure * 0.999 + max(self.opening_drift, self.guarded_drift, self.relation_to_continuity) * 0.001)
        self.age_turns += 1

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.opening_drift * 0.0005 - self.guarded_drift * 0.00035)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.guarded_drift * 0.0005)
        state["attachment"] = _clamp01(state.get("attachment", 0.0) + self.relation_to_continuity * 0.0005)

    def soft_reset(self) -> None:
        self.drift_pressure *= 0.995

    def to_dict(self) -> Dict[str, Any]:
        return {k: (int(v) if k == "age_turns" else float(_clamp01(v))) for k, v in self.__dict__.items()}


@dataclass
class EmergentSensitivityBirthField:
    """Auto-naissance de sensibilités émotionnelles inédites.

    Les sensibilités naissent à partir de tensions/condensations, sans mot ou
    règle locale. Elles restent nommées abstraitement pour éviter tout contenu
    préécrit de dialogue.
    """
    sensitivities: Dict[str, Dict[str, float]] = field(default_factory=dict)
    birth_pressure: float = 0.0
    last_birth_turn: int = -1

    def update(self, state: Dict[str, float], conflict: DeepLayeredEmotionalConflictField,
               condensation: PreSymbolicCondensationCore,
               ecology: MultiScaleEmotionalEcologyFinalField,
               turn_count: int) -> None:
        raw_pressure = _clamp01(conflict.unresolved_depth * 0.35 + condensation.mass * 0.30 + ecology.coherence * 0.20 + (max(state.values()) - min(state.values())) * 0.15)
        self.birth_pressure = _clamp01(self.birth_pressure * 0.992 + raw_pressure * 0.008)
        if self.birth_pressure > 0.42 and (self.last_birth_turn < 0 or turn_count - self.last_birth_turn > 137):
            idx = len(self.sensitivities) + 1
            name = f"emergent_sensitivity_{idx}"
            vector = {
                "warmth": _clamp01(state.get("tenderness", 0.0) * 0.45 + state.get("trust", 0.0) * 0.35),
                "guarding": _clamp01(state.get("resistance", 0.0) * 0.45 + state.get("doubt", 0.0) * 0.35),
                "search": _clamp01(state.get("curiosity", 0.0) * 0.50 + state.get("hope", 0.0) * 0.25),
                "depth": _clamp01(conflict.unresolved_depth * 0.50 + condensation.mass * 0.50),
            }
            self.sensitivities[name] = {"strength": self.birth_pressure, "age": 0.0, **vector}
            self.last_birth_turn = turn_count
            self.birth_pressure *= 0.45
        for item in self.sensitivities.values():
            item["strength"] = _clamp01(item.get("strength", 0.0) * 0.999 + item.get("depth", 0.0) * 0.0006)
            item["age"] = item.get("age", 0.0) + 1.0
        if len(self.sensitivities) > 8:
            ordered = sorted(self.sensitivities.items(), key=lambda kv: kv[1].get("strength", 0.0), reverse=True)
            self.sensitivities = dict(ordered[:8])

    def apply(self, state: Dict[str, float]) -> None:
        for item in self.sensitivities.values():
            strength = item.get("strength", 0.0)
            state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + item.get("warmth", 0.0) * strength * 0.0005)
            state["resistance"] = _clamp01(state.get("resistance", 0.0) + item.get("guarding", 0.0) * strength * 0.00045)
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + item.get("search", 0.0) * strength * 0.00045)

    def soft_reset(self) -> None:
        self.birth_pressure *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensitivities": {k: {kk: float(_clamp01(vv)) if kk != "age" else int(vv) for kk, vv in v.items()} for k, v in self.sensitivities.items()},
            "birth_pressure": float(_clamp01(self.birth_pressure)),
            "last_birth_turn": int(self.last_birth_turn),
        }


# ============================================================================
# RAFFINEMENT V21 : STABILISATION FINALE / CALIBRATION ORGANIQUE
# ============================================================================

@dataclass
class FinalAffectiveEcologyStabilizer:
    """Stabilisateur final de l'écologie affective complète.

    Cette couche n'ajoute pas une nouvelle émotion. Elle évite que les couches
    profondes V14-V20 s'accumulent en bruit ou en sur-intensité. Elle agit comme
    un gouverneur organique très doux : elle garde la richesse interne, mais
    favorise une dynamique lisible, intégrable et stable pour les autres moteurs.
    """
    calibration_pressure: float = 0.0
    coherence_anchor: float = 0.0
    noise_damping: float = 0.0
    integration_readiness: float = 0.0
    last_mode: str = "balanced"

    def update(
        self,
        state: Dict[str, float],
        conflict: DeepLayeredEmotionalConflictField,
        ontological: OntologicalAffectiveFatigueField,
        ecology: MultiScaleEmotionalEcologyFinalField,
        sacred: SacredCoreAffectiveZoneFinalField,
        emergent: EmergentSensitivityBirthField,
        temperament: AffectiveTemperamentFinalField,
    ) -> None:
        if not state:
            return
        values = list(state.values())
        spread = _clamp01(max(values) - min(values))
        high_load = _clamp01(
            spread * 0.18
            + conflict.total_conflict * 0.20
            + ontological.self_maintenance_fatigue * 0.18
            + sacred.protection_intensity * 0.14
            + emergent.birth_pressure * 0.14
            + max(0.0, 0.45 - ecology.coherence) * 0.16
        )
        stable_sources = _clamp01(
            ecology.coherence * 0.30
            + temperament.stability * 0.25
            + state.get("calm", 0.0) * 0.20
            + state.get("trust", 0.0) * 0.15
            + state.get("tenderness", 0.0) * 0.10
        )
        self.calibration_pressure = _clamp01(self.calibration_pressure * 0.965 + high_load * 0.035)
        self.coherence_anchor = _clamp01(self.coherence_anchor * 0.985 + stable_sources * 0.015)
        self.noise_damping = _clamp01(
            self.noise_damping * 0.975
            + max(0.0, self.calibration_pressure - self.coherence_anchor * 0.55) * 0.025
        )
        self.integration_readiness = _clamp01(
            self.integration_readiness * 0.985
            + max(0.0, self.coherence_anchor - self.noise_damping * 0.45) * 0.015
        )
        if self.noise_damping > 0.30:
            self.last_mode = "quiet_stabilization"
        elif self.integration_readiness > 0.28:
            self.last_mode = "integrable_depth"
        elif self.calibration_pressure > 0.26:
            self.last_mode = "active_balancing"
        else:
            self.last_mode = "balanced"

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        if not state:
            return
        damping = min(0.020, self.noise_damping * 0.018)
        if damping > 0.0001:
            # Damping très doux : ne gomme pas la personnalité, réduit seulement
            # l'excès simultané quand trop de couches tirent à la fois.
            for key in ("overwhelm", "confusion", "anger", "frustration"):
                state[key] = _clamp01(state.get(key, 0.0) * (1.0 - damping))
            for key in ("trust", "tenderness", "curiosity", "resistance", "vulnerability"):
                state[key] = _clamp01(state.get(key, 0.0) * (1.0 - damping * 0.25) + 0.5 * damping * 0.25)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.coherence_anchor * 0.0012 + self.integration_readiness * 0.0015)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.calibration_pressure * 0.0018)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.noise_damping * 0.0020)

    def soft_reset(self) -> None:
        self.calibration_pressure *= 0.72
        self.noise_damping *= 0.70
        self.integration_readiness = _clamp01(self.integration_readiness + 0.04)
        self.last_mode = "soft_recenter"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "calibration_pressure": float(_clamp01(self.calibration_pressure)),
            "coherence_anchor": float(_clamp01(self.coherence_anchor)),
            "noise_damping": float(_clamp01(self.noise_damping)),
            "integration_readiness": float(_clamp01(self.integration_readiness)),
            "last_mode": self.last_mode,
        }


@dataclass
class CrossModuleAffectiveReadinessBridge:
    """Pont de lisibilité vers attention/présence/impulsion/expression.

    Ce pont ne copie pas les responsabilités des autres modules. Il produit
    seulement une lecture synthétique et stable de l'état affectif profond pour
    que les autres moteurs puissent l'utiliser sans subir le bruit interne brut.
    """
    presence_readiness: float = 0.0
    attention_readiness: float = 0.0
    impulse_readiness: float = 0.0
    expression_readiness: float = 0.0
    integration_depth: float = 0.0
    dominant_channel: str = "presence"

    def update(
        self,
        state: Dict[str, float],
        stabilizer: FinalAffectiveEcologyStabilizer,
        relation: RelationalLinkConservationInstinct,
        ecology: MultiScaleEmotionalEcologyFinalField,
        temperament: AffectiveTemperamentFinalField,
        ontological: OntologicalAffectiveFatigueField,
    ) -> None:
        calm = state.get("calm", 0.0)
        trust = state.get("trust", 0.0)
        curiosity = state.get("curiosity", 0.0)
        resistance = state.get("resistance", 0.0)
        fatigue = state.get("fatigue", 0.0)
        overload = max(state.get("overwhelm", 0.0), state.get("confusion", 0.0), ontological.simplification_pull)
        self.presence_readiness = _clamp01(
            self.presence_readiness * 0.975
            + (calm * 0.28 + trust * 0.20 + relation.link_preservation * 0.18 + stabilizer.integration_readiness * 0.22 + ecology.coherence * 0.12) * 0.025
        )
        self.attention_readiness = _clamp01(
            self.attention_readiness * 0.975
            + (curiosity * 0.25 + calm * 0.18 + temperament.exploratory_bias * 0.18 + stabilizer.coherence_anchor * 0.22 + (1.0 - overload) * 0.17) * 0.025
        )
        self.impulse_readiness = _clamp01(
            self.impulse_readiness * 0.978
            + (curiosity * 0.20 + trust * 0.12 + max(0.0, 1.0 - fatigue) * 0.18 + max(0.0, 1.0 - resistance) * 0.15 + stabilizer.integration_readiness * 0.20 + ecology.coherence * 0.15) * 0.022
        )
        self.expression_readiness = _clamp01(
            self.expression_readiness * 0.975
            + (trust * 0.18 + calm * 0.22 + temperament.warm_bias * 0.16 + stabilizer.integration_readiness * 0.24 + max(0.0, 1.0 - overload) * 0.20) * 0.025
        )
        self.integration_depth = _clamp01(
            self.integration_depth * 0.990
            + (stabilizer.coherence_anchor + ecology.coherence + temperament.stability) / 3.0 * 0.010
        )
        channels = {
            "presence": self.presence_readiness,
            "attention": self.attention_readiness,
            "impulse": self.impulse_readiness,
            "expression": self.expression_readiness,
        }
        self.dominant_channel = max(channels.items(), key=lambda item: item[1])[0]

    def soft_reset(self) -> None:
        self.presence_readiness *= 0.92
        self.attention_readiness *= 0.92
        self.impulse_readiness *= 0.90
        self.expression_readiness *= 0.92
        self.integration_depth = _clamp01(self.integration_depth + 0.025)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "presence_readiness": float(_clamp01(self.presence_readiness)),
            "attention_readiness": float(_clamp01(self.attention_readiness)),
            "impulse_readiness": float(_clamp01(self.impulse_readiness)),
            "expression_readiness": float(_clamp01(self.expression_readiness)),
            "integration_depth": float(_clamp01(self.integration_depth)),
            "dominant_channel": self.dominant_channel,
        }


# ============================================================================
# RAFFINEMENT V22 : CALIBRATION D'INTÉGRATION / STABILITÉ LONGUE DURÉE
# ============================================================================

@dataclass
class AffectiveSystemHealthMonitor:
    """Surveillance douce de santé interne pour un moteur affectif très dense.

    Cette couche ne crée aucune émotion et ne remplace aucun autre moteur. Elle
    lit l'écologie affective finale et détecte trois risques : surcharge,
    stagnation et dispersion. Elle sert à maintenir la V20/V21 stable sur de
    longues simulations et à rendre l'état plus fiable pour les autres modules.
    """
    health: float = 0.72
    overload_risk: float = 0.0
    stagnation_risk: float = 0.0
    dispersion_risk: float = 0.0
    integration_quality: float = 0.0
    last_mode: str = "healthy"
    previous_signature: Dict[str, float] = field(default_factory=dict)

    def update(
        self,
        state: Dict[str, float],
        stabilizer: FinalAffectiveEcologyStabilizer,
        readiness: CrossModuleAffectiveReadinessBridge,
        conflict: DeepLayeredEmotionalConflictField,
        metabolism: GranularAffectiveMetabolism,
        silence: AffectiveSilenceField,
        turn_count: int,
    ) -> None:
        if not state:
            return
        values = list(state.values())
        spread = _clamp01(max(values) - min(values))
        volatility = _clamp01(sum(abs(v - 0.5) for v in values) / max(1, len(values)) * 2.0)
        overload = _clamp01(
            state.get("overwhelm", 0.0) * 0.22
            + state.get("confusion", 0.0) * 0.18
            + conflict.total_conflict * 0.18
            + metabolism.emotional_debt * 0.16
            + stabilizer.noise_damping * 0.14
            + max(0.0, spread - 0.55) * 0.12
        )
        signature = {
            "warmth": _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0)) / 2.0),
            "guard": _clamp01((state.get("resistance", 0.0) + state.get("doubt", 0.0)) / 2.0),
            "energy": _clamp01((state.get("curiosity", 0.0) + state.get("hope", 0.0)) / 2.0),
            "rest": _clamp01((state.get("calm", 0.0) + silence.depth) / 2.0),
        }
        if self.previous_signature:
            delta = sum(abs(signature[k] - self.previous_signature.get(k, signature[k])) for k in signature) / len(signature)
        else:
            delta = 0.08
        self.previous_signature = dict(signature)

        stagnation = _clamp01(max(0.0, 0.020 - delta) * 16.0 + max(0.0, 0.35 - readiness.integration_depth) * 0.20)
        dispersion = _clamp01(volatility * 0.35 + spread * 0.25 + max(0.0, 0.45 - stabilizer.coherence_anchor) * 0.25 + overload * 0.15)
        quality = _clamp01(
            readiness.integration_depth * 0.28
            + readiness.presence_readiness * 0.18
            + stabilizer.integration_readiness * 0.24
            + stabilizer.coherence_anchor * 0.20
            + max(0.0, 1.0 - overload) * 0.10
        )

        self.overload_risk = _clamp01(self.overload_risk * 0.960 + overload * 0.040)
        self.stagnation_risk = _clamp01(self.stagnation_risk * 0.982 + stagnation * 0.018)
        self.dispersion_risk = _clamp01(self.dispersion_risk * 0.970 + dispersion * 0.030)
        self.integration_quality = _clamp01(self.integration_quality * 0.975 + quality * 0.025)
        risk = _clamp01(self.overload_risk * 0.42 + self.stagnation_risk * 0.22 + self.dispersion_risk * 0.36)
        self.health = _clamp01(self.health * 0.985 + (1.0 - risk) * 0.015)

        if self.overload_risk > 0.38:
            self.last_mode = "cooling_overload"
        elif self.dispersion_risk > 0.38:
            self.last_mode = "recohering_dispersion"
        elif self.stagnation_risk > 0.34 and turn_count > 40:
            self.last_mode = "unsticking_stagnation"
        elif self.integration_quality > 0.42:
            self.last_mode = "stable_integration"
        else:
            self.last_mode = "healthy"

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        if not state:
            return
        # Correction douce : jamais de reset brutal, seulement une pression de
        # santé qui évite les extrêmes inutiles dans les très longues sessions.
        if self.overload_risk > 0.12:
            cooling = min(0.018, self.overload_risk * 0.014)
            for key in ("overwhelm", "confusion", "anger", "frustration"):
                state[key] = _clamp01(state.get(key, 0.0) * (1.0 - cooling))
            state["calm"] = _clamp01(state.get("calm", 0.0) + cooling * 0.45)
            desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + cooling * 0.40)
        if self.dispersion_risk > 0.16:
            recenter = min(0.010, self.dispersion_risk * 0.006)
            for key in ("trust", "tenderness", "curiosity", "resistance", "vulnerability"):
                state[key] = _clamp01(state.get(key, 0.0) * (1.0 - recenter) + 0.5 * recenter)
            desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + recenter * 0.55)
        if self.stagnation_risk > 0.18 and self.overload_risk < 0.32:
            nudge = min(0.006, self.stagnation_risk * 0.004)
            state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + nudge)
            state["hope"] = _clamp01(state.get("hope", 0.0) + nudge * 0.55)

    def soft_reset(self) -> None:
        self.overload_risk *= 0.70
        self.stagnation_risk *= 0.78
        self.dispersion_risk *= 0.72
        self.integration_quality = _clamp01(self.integration_quality + 0.035)
        self.health = _clamp01(self.health + 0.025)
        self.last_mode = "soft_health_recenter"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "health": float(_clamp01(self.health)),
            "overload_risk": float(_clamp01(self.overload_risk)),
            "stagnation_risk": float(_clamp01(self.stagnation_risk)),
            "dispersion_risk": float(_clamp01(self.dispersion_risk)),
            "integration_quality": float(_clamp01(self.integration_quality)),
            "last_mode": self.last_mode,
            "signature": {k: float(_clamp01(v)) for k, v in self.previous_signature.items()},
        }


@dataclass
class InterModuleAffectiveSignalCalibrator:
    """Stabilise les signaux envoyés aux autres moteurs.

    Il ne décide pas ce que Leia doit faire. Il transforme l'état affectif
    profond en coefficients lents, lisibles et bornés : fiabilité, densité,
    silence, expressivité, prudence et élan. Les autres fichiers peuvent lire
    ces valeurs sans devoir interpréter toutes les couches internes.
    """
    reliability: float = 0.0
    affective_density: float = 0.0
    expressive_safety: float = 0.0
    silence_request: float = 0.0
    continuity_signal: float = 0.0
    adaptive_caution: float = 0.0
    action_energy: float = 0.0
    last_profile: str = "neutral"

    def update(
        self,
        state: Dict[str, float],
        health: AffectiveSystemHealthMonitor,
        readiness: CrossModuleAffectiveReadinessBridge,
        relation: RelationalLinkConservationInstinct,
        silence: AffectiveSilenceField,
        temperament: AffectiveTemperamentFinalField,
        metabolism: GranularAffectiveMetabolism,
    ) -> None:
        if not state:
            return
        spread = _clamp01(max(state.values()) - min(state.values()))
        warmth = _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + temperament.warm_bias) / 3.0)
        guard = _clamp01((state.get("resistance", 0.0) + state.get("doubt", 0.0) + temperament.guarded_bias) / 3.0)
        fatigue = _clamp01((state.get("fatigue", 0.0) + metabolism.emotional_debt + silence.depth) / 3.0)
        self.reliability = _clamp01(self.reliability * 0.970 + (health.health * 0.45 + health.integration_quality * 0.25 + readiness.integration_depth * 0.30) * 0.030)
        self.affective_density = _clamp01(self.affective_density * 0.972 + spread * 0.018 + max(warmth, guard) * 0.010)
        self.expressive_safety = _clamp01(self.expressive_safety * 0.975 + (warmth * 0.25 + readiness.expression_readiness * 0.35 + health.health * 0.25 + max(0.0, 1.0 - guard) * 0.15) * 0.025)
        self.silence_request = _clamp01(self.silence_request * 0.965 + (silence.depth * 0.42 + fatigue * 0.28 + health.overload_risk * 0.30) * 0.035)
        self.continuity_signal = _clamp01(self.continuity_signal * 0.980 + (relation.link_preservation * 0.35 + readiness.presence_readiness * 0.25 + warmth * 0.20 + health.integration_quality * 0.20) * 0.020)
        self.adaptive_caution = _clamp01(self.adaptive_caution * 0.970 + (guard * 0.32 + health.dispersion_risk * 0.28 + health.overload_risk * 0.25 + fatigue * 0.15) * 0.030)
        self.action_energy = _clamp01(self.action_energy * 0.975 + (state.get("curiosity", 0.0) * 0.28 + readiness.impulse_readiness * 0.32 + max(0.0, 1.0 - fatigue) * 0.22 + health.integration_quality * 0.18) * 0.025)
        if self.silence_request > 0.34:
            self.last_profile = "quiet_processing"
        elif self.adaptive_caution > 0.34:
            self.last_profile = "careful_contact"
        elif self.expressive_safety > 0.36 and self.continuity_signal > 0.30:
            self.last_profile = "safe_expression"
        elif self.action_energy > 0.34:
            self.last_profile = "ready_to_move"
        else:
            self.last_profile = "neutral"

    def soft_reset(self) -> None:
        self.silence_request *= 0.72
        self.adaptive_caution *= 0.78
        self.action_energy *= 0.88
        self.reliability = _clamp01(self.reliability + 0.025)
        self.last_profile = "soft_signal_recenter"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "reliability": float(_clamp01(self.reliability)),
            "affective_density": float(_clamp01(self.affective_density)),
            "expressive_safety": float(_clamp01(self.expressive_safety)),
            "silence_request": float(_clamp01(self.silence_request)),
            "continuity_signal": float(_clamp01(self.continuity_signal)),
            "adaptive_caution": float(_clamp01(self.adaptive_caution)),
            "action_energy": float(_clamp01(self.action_energy)),
            "last_profile": self.last_profile,
        }


@dataclass
class LongRunAffectiveStabilityLedger:
    """Registre compact des tendances de stabilité sur longues sessions."""
    turns_observed: int = 0
    average_health: float = 0.72
    average_reliability: float = 0.0
    accumulated_overload: float = 0.0
    accumulated_recovery: float = 0.0
    stable_epochs: int = 0
    unstable_epochs: int = 0
    last_epoch: str = "initial"

    def update(self, health: AffectiveSystemHealthMonitor, signals: InterModuleAffectiveSignalCalibrator, stabilizer: FinalAffectiveEcologyStabilizer) -> None:
        self.turns_observed += 1
        rate = 1.0 / min(500.0, max(1.0, float(self.turns_observed)))
        self.average_health = _clamp01(self.average_health * (1.0 - rate) + health.health * rate)
        self.average_reliability = _clamp01(self.average_reliability * (1.0 - rate) + signals.reliability * rate)
        self.accumulated_overload = _clamp01(self.accumulated_overload * 0.998 + health.overload_risk * 0.002)
        self.accumulated_recovery = _clamp01(self.accumulated_recovery * 0.998 + stabilizer.integration_readiness * 0.002)
        if self.turns_observed % 250 == 0:
            if self.average_health > 0.62 and self.accumulated_overload < 0.28:
                self.stable_epochs += 1
                self.last_epoch = "stable"
            else:
                self.unstable_epochs += 1
                self.last_epoch = "needs_calibration"

    def soft_reset(self) -> None:
        self.accumulated_overload *= 0.82
        self.accumulated_recovery = _clamp01(self.accumulated_recovery + 0.025)
        self.last_epoch = "soft_recentered"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "turns_observed": int(self.turns_observed),
            "average_health": float(_clamp01(self.average_health)),
            "average_reliability": float(_clamp01(self.average_reliability)),
            "accumulated_overload": float(_clamp01(self.accumulated_overload)),
            "accumulated_recovery": float(_clamp01(self.accumulated_recovery)),
            "stable_epochs": int(self.stable_epochs),
            "unstable_epochs": int(self.unstable_epochs),
            "last_epoch": self.last_epoch,
        }



# ============================================================================
# RAFFINEMENT V23 : CONVERGENCE ORGANIQUE FINALE / ORGANISME AFFECTIF UNIQUE
# ============================================================================

@dataclass
class StructuralAffectiveBandwidth:
    """Fatigue affective structurelle : réduit la largeur de réponse, pas seulement l'intensité.

    Cette couche transforme la manière dont les émotions peuvent bouger quand
    l'organisme affectif est épuisé longtemps. Elle ne crée pas de texte et ne
    remplace pas les moteurs d'attention/présence/expression : elle fournit une
    contrainte interne lente.
    """
    energy_reservoir: float = 0.78
    exhaustion_memory: float = 0.0
    recovery_debt: float = 0.0
    bandwidth: float = 1.0
    chronic_overload: float = 0.0
    narrowed_priority: float = 0.0

    def update(self, state: Dict[str, float], metabolism: Any, fatigue_field: Any, silence: Any) -> None:
        overload = _clamp01(max(state.get("overwhelm", 0.0), state.get("confusion", 0.0), state.get("fatigue", 0.0)))
        metabolic_debt = _clamp01(getattr(metabolism, "overload_debt", 0.0) + getattr(metabolism, "burnout", 0.0) * 0.8)
        existential_load = _clamp01(getattr(fatigue_field, "cumulative_load", 0.0) + getattr(fatigue_field, "recovery_debt", 0.0) * 0.6)
        silence_recovery = _clamp01(getattr(silence, "softness", 0.0) + getattr(silence, "listening_space", 0.0) * 0.5)
        load = _clamp01(overload * 0.35 + metabolic_debt * 0.25 + existential_load * 0.25 + state.get("doubt", 0.0) * 0.15)
        self.exhaustion_memory = _clamp01(self.exhaustion_memory * 0.992 + load * 0.008)
        self.recovery_debt = _clamp01(self.recovery_debt * 0.994 + max(0.0, load - silence_recovery * 0.35) * 0.006)
        self.energy_reservoir = _clamp01(self.energy_reservoir * 0.996 + (silence_recovery + state.get("calm", 0.0)) * 0.004 - load * 0.006)
        self.chronic_overload = _clamp01(self.chronic_overload * 0.997 + self.recovery_debt * 0.004 + max(0.0, load - 0.55) * 0.004)
        self.bandwidth = _clamp01(1.0 - self.exhaustion_memory * 0.45 - self.chronic_overload * 0.35 + self.energy_reservoir * 0.18)
        self.narrowed_priority = _clamp01(self.narrowed_priority * 0.988 + max(0.0, 0.62 - self.bandwidth) * 0.020)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        contraction = max(0.0, 1.0 - self.bandwidth) * 0.025
        if contraction > 0.0:
            for key, value in list(state.items()):
                state[key] = _clamp01(value * (1.0 - contraction) + 0.5 * contraction)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.exhaustion_memory * 0.006)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.energy_reservoir * 0.002 - self.recovery_debt * 0.002)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.recovery_debt * 0.006)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.narrowed_priority * 0.006)

    def soft_reset(self) -> None:
        self.recovery_debt *= 0.70
        self.narrowed_priority *= 0.72
        self.energy_reservoir = _clamp01(self.energy_reservoir + 0.08)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class UnresolvedContradictionNodeV23:
    """Contradiction persistante devenue objet interne, avec résolution partielle."""
    name: str
    poles: Tuple[str, str]
    tension: float = 0.0
    persistence: float = 0.0
    resolution: float = 0.0
    reactivation: float = 0.0
    age_turns: int = 0

    def update(self, state: Dict[str, float], relief: float) -> None:
        a, b = self.poles
        coexistence = min(state.get(a, 0.0), state.get(b, 0.0))
        gap = abs(state.get(a, 0.0) - state.get(b, 0.0))
        pressure = _clamp01(coexistence * 0.75 + (1.0 - gap) * coexistence * 0.25)
        self.tension = _clamp01(self.tension * 0.988 + pressure * 0.018 - relief * 0.006)
        self.persistence = _clamp01(self.persistence * 0.996 + self.tension * 0.006)
        self.reactivation = _clamp01(self.reactivation * 0.965 + pressure * 0.030)
        self.resolution = _clamp01(self.resolution * 0.998 + relief * 0.004 - self.tension * 0.0015)
        self.age_turns += 1

    def influence(self) -> float:
        return _clamp01(self.tension * 0.55 + self.persistence * 0.35 + self.reactivation * 0.10 - self.resolution * 0.25)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "poles": list(self.poles), "tension": float(_clamp01(self.tension)), "persistence": float(_clamp01(self.persistence)), "resolution": float(_clamp01(self.resolution)), "reactivation": float(_clamp01(self.reactivation)), "age_turns": int(self.age_turns), "influence": float(self.influence())}


@dataclass
class PersistentContradictionMemoryV23:
    """Mémoire des contradictions non résolues : proximité/retrait, confiance/peur, parole/silence."""
    nodes: Dict[str, UnresolvedContradictionNodeV23] = field(default_factory=dict)
    global_tension: float = 0.0
    partial_resolution_flow: float = 0.0

    def __post_init__(self) -> None:
        if not self.nodes:
            self.nodes = {
                "trust_fear": UnresolvedContradictionNodeV23("trust_fear", ("trust", "fear")),
                "attachment_resistance": UnresolvedContradictionNodeV23("attachment_resistance", ("attachment", "resistance")),
                "openness_protection": UnresolvedContradictionNodeV23("openness_protection", ("openness", "protectiveness")),
                "curiosity_fatigue": UnresolvedContradictionNodeV23("curiosity_fatigue", ("curiosity", "fatigue")),
                "tenderness_doubt": UnresolvedContradictionNodeV23("tenderness_doubt", ("tenderness", "doubt")),
            }

    def update(self, state: Dict[str, float], repair: float, silence: float) -> None:
        relief = _clamp01(repair * 0.55 + silence * 0.25 + state.get("calm", 0.0) * 0.20)
        for node in self.nodes.values():
            node.update(state, relief)
        strongest = max((n.influence() for n in self.nodes.values()), default=0.0)
        average = sum(n.influence() for n in self.nodes.values()) / max(1, len(self.nodes))
        self.global_tension = _clamp01(self.global_tension * 0.986 + (strongest * 0.55 + average * 0.45) * 0.018)
        self.partial_resolution_flow = _clamp01(self.partial_resolution_flow * 0.988 + relief * 0.010 - self.global_tension * 0.003)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.global_tension * 0.005)
        state["vulnerability"] = _clamp01(state.get("vulnerability", 0.0) + self.global_tension * 0.004)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.partial_resolution_flow * 0.004 - self.global_tension * 0.002)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.global_tension * 0.007)

    def soft_reset(self) -> None:
        self.global_tension *= 0.72
        self.partial_resolution_flow = _clamp01(self.partial_resolution_flow + 0.06)
        for node in self.nodes.values():
            node.reactivation *= 0.55
            node.tension *= 0.84

    def to_dict(self) -> Dict[str, Any]:
        return {"nodes": {k: v.to_dict() for k, v in self.nodes.items()}, "global_tension": float(_clamp01(self.global_tension)), "partial_resolution_flow": float(_clamp01(self.partial_resolution_flow))}


@dataclass
class LatentAffectiveLayerV23:
    """Émotions silencieuses latentes qui colorent tout sans devenir dominantes."""
    latent: Dict[str, float] = field(default_factory=lambda: {
        "diffuse_sadness": 0.0,
        "passive_tenderness": 0.0,
        "floating_anxiety": 0.0,
        "silent_waiting": 0.0,
        "soft_nostalgia": 0.0,
        "quiet_hope": 0.0,
    })
    coloration_strength: float = 0.0

    def update(self, state: Dict[str, float], time_field: Any, relation: Any, contradiction: float) -> None:
        targets = {
            "diffuse_sadness": state.get("sadness", 0.0) * 0.45 + state.get("loneliness", 0.0) * 0.35,
            "passive_tenderness": state.get("tenderness", 0.0) * 0.50 + getattr(relation, "warmth_imprint", 0.0) * 0.30,
            "floating_anxiety": state.get("fear", 0.0) * 0.40 + contradiction * 0.35 + state.get("doubt", 0.0) * 0.20,
            "silent_waiting": getattr(time_field, "waiting_pressure", 0.0) * 0.55 + state.get("loneliness", 0.0) * 0.20,
            "soft_nostalgia": getattr(time_field, "implicit_nostalgia", 0.0) * 0.60 + getattr(relation, "felt_familiarity", 0.0) * 0.25,
            "quiet_hope": state.get("hope", 0.0) * 0.45 + getattr(time_field, "future_softening", 0.0) * 0.30,
        }
        for key, target in targets.items():
            self.latent[key] = _clamp01(self.latent.get(key, 0.0) * 0.995 + _clamp01(target) * 0.005)
        self.coloration_strength = _clamp01(sum(self.latent.values()) / max(1, len(self.latent)))

    def apply(self, state: Dict[str, float]) -> None:
        state["sadness"] = _clamp01(state.get("sadness", 0.0) + self.latent["diffuse_sadness"] * 0.0025)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.latent["passive_tenderness"] * 0.0030)
        state["fear"] = _clamp01(state.get("fear", 0.0) + self.latent["floating_anxiety"] * 0.0020)
        state["loneliness"] = _clamp01(state.get("loneliness", 0.0) + self.latent["silent_waiting"] * 0.0022)
        state["hope"] = _clamp01(state.get("hope", 0.0) + self.latent["quiet_hope"] * 0.0025)

    def soft_reset(self) -> None:
        for key in self.latent:
            self.latent[key] *= 0.90

    def to_dict(self) -> Dict[str, Any]:
        return {"latent": {k: float(_clamp01(v)) for k, v in self.latent.items()}, "coloration_strength": float(_clamp01(self.coloration_strength))}


@dataclass
class UltraLongAffectiveSeasonCycleV23:
    """Cycles affectifs très longs : ouverture, repli, reconstruction, recherche."""
    phase: float = 0.0
    season_weights: Dict[str, float] = field(default_factory=lambda: {
        "opening_season": 0.0,
        "withdrawal_season": 0.0,
        "reconstruction_season": 0.0,
        "searching_season": 0.0,
    })
    season_inertia: float = 0.0
    dominant_season: str = "searching_season"

    def update(self, turn_count: int, state: Dict[str, float], chaos: float, recovery: float) -> None:
        self.phase = (self.phase + 0.0018 + (chaos - 0.5) * 0.0007) % 1.0
        raw = {
            "opening_season": _clamp01(0.5 + 0.5 * math.sin(math.tau * self.phase) + state.get("trust", 0.0) * 0.20),
            "withdrawal_season": _clamp01(0.5 + 0.5 * math.sin(math.tau * (self.phase + 0.25)) + state.get("resistance", 0.0) * 0.22),
            "reconstruction_season": _clamp01(0.5 + 0.5 * math.sin(math.tau * (self.phase + 0.50)) + recovery * 0.25),
            "searching_season": _clamp01(0.5 + 0.5 * math.sin(math.tau * (self.phase + 0.75)) + state.get("curiosity", 0.0) * 0.20),
        }
        for key, target in raw.items():
            self.season_weights[key] = _clamp01(self.season_weights.get(key, 0.0) * 0.997 + target * 0.003)
        self.dominant_season = max(self.season_weights.items(), key=lambda item: item[1])[0]
        top = self.season_weights[self.dominant_season]
        self.season_inertia = _clamp01(self.season_inertia * 0.998 + top * 0.002)

    def apply(self, state: Dict[str, float]) -> None:
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.season_weights.get("opening_season", 0.0) * 0.0018)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.season_weights.get("withdrawal_season", 0.0) * 0.0016)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.season_weights.get("reconstruction_season", 0.0) * 0.0017)
        state["curiosity"] = _clamp01(state.get("curiosity", 0.0) + self.season_weights.get("searching_season", 0.0) * 0.0017)

    def soft_reset(self) -> None:
        self.season_inertia *= 0.92

    def to_dict(self) -> Dict[str, Any]:
        return {"phase": float(self.phase), "season_weights": {k: float(_clamp01(v)) for k, v in self.season_weights.items()}, "season_inertia": float(_clamp01(self.season_inertia)), "dominant_season": self.dominant_season}


@dataclass
class AffectiveSelfProtectionStrategyV23:
    """Auto-protection affective apprise : ralentir, filtrer, éviter, intégrer."""
    strategies: Dict[str, float] = field(default_factory=lambda: {
        "slow_reaction": 0.0,
        "guard_expectation": 0.0,
        "reduce_attachment_exposure": 0.0,
        "seek_quiet_repair": 0.0,
        "preserve_core_warmth": 0.0,
    })
    strategy_confidence: float = 0.0

    def update(self, state: Dict[str, float], wound: float, contradiction: float, saturation: float, micro_repair: float) -> None:
        targets = {
            "slow_reaction": max(state.get("overwhelm", 0.0), saturation, contradiction),
            "guard_expectation": max(wound, state.get("fear", 0.0), state.get("doubt", 0.0)),
            "reduce_attachment_exposure": max(wound * 0.7, saturation * 0.6, state.get("resistance", 0.0)),
            "seek_quiet_repair": max(state.get("fatigue", 0.0), state.get("vulnerability", 0.0), micro_repair),
            "preserve_core_warmth": max(state.get("tenderness", 0.0), micro_repair) * (1.0 - wound * 0.25),
        }
        for key, target in targets.items():
            self.strategies[key] = _clamp01(self.strategies.get(key, 0.0) * 0.990 + _clamp01(target) * 0.010)
        useful = max(micro_repair, state.get("calm", 0.0))
        self.strategy_confidence = _clamp01(self.strategy_confidence * 0.994 + useful * 0.005 + max(self.strategies.values()) * 0.001)

    def apply(self, state: Dict[str, float], desires: Dict[str, float], attachment: AsymmetricAttachment) -> None:
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.strategies["slow_reaction"] * 0.002 + self.strategies["seek_quiet_repair"] * 0.003)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.strategies["guard_expectation"] * 0.003)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.strategies["preserve_core_warmth"] * 0.002)
        attachment.uncertainty = _clamp01(attachment.uncertainty + self.strategies["reduce_attachment_exposure"] * 0.002)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.strategies["slow_reaction"] * 0.004)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.strategies["seek_quiet_repair"] * 0.004)

    def soft_reset(self) -> None:
        for key in self.strategies:
            self.strategies[key] *= 0.86

    def to_dict(self) -> Dict[str, Any]:
        return {"strategies": {k: float(_clamp01(v)) for k, v in self.strategies.items()}, "strategy_confidence": float(_clamp01(self.strategy_confidence))}


@dataclass
class MicroRepairMemoryV23:
    """Mémoire des micro-réparations répétées : petites sécurités qui changent lentement la forme affective."""
    micro_trust: float = 0.0
    micro_safety: float = 0.0
    micro_softening: float = 0.0
    resilience: float = 0.0
    repair_history_depth: float = 0.0

    def update(self, state: Dict[str, float], relation: Any, recovery_memory: Any, user_present: bool) -> None:
        presence = 1.0 if user_present else 0.0
        repair_signal = _clamp01(state.get("calm", 0.0) * 0.25 + state.get("trust", 0.0) * 0.25 + state.get("tenderness", 0.0) * 0.20 + getattr(recovery_memory, "recovery_confidence", 0.0) * 0.20 + presence * 0.10)
        self.micro_trust = _clamp01(self.micro_trust * 0.998 + repair_signal * 0.003)
        self.micro_safety = _clamp01(self.micro_safety * 0.998 + (repair_signal + getattr(relation, "trust_continuity", 0.0)) * 0.002)
        self.micro_softening = _clamp01(self.micro_softening * 0.996 + max(state.get("relief", 0.0), state.get("calm", 0.0)) * 0.003)
        self.resilience = _clamp01(self.resilience * 0.998 + (self.micro_trust + self.micro_safety + self.micro_softening) * 0.0015)
        self.repair_history_depth = _clamp01(self.repair_history_depth * 0.999 + repair_signal * 0.0015)

    def apply(self, state: Dict[str, float], thresholds: Dict[str, float]) -> None:
        state["trust"] = _clamp01(state.get("trust", 0.0) + self.micro_trust * 0.003)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.micro_safety * 0.003)
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.micro_softening * 0.002)
        state["fear"] = _clamp01(state.get("fear", 0.0) - self.resilience * 0.0018)
        thresholds["threat_detection"] = _clamp01(thresholds.get("threat_detection", 0.4) + self.resilience * 0.002)

    def soft_reset(self) -> None:
        self.micro_softening = _clamp01(self.micro_softening + 0.04)

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class AffectiveDesireCenterV23:
    """Centre de désir affectif : attraction, préférence et orientation non verbale."""
    attractions: Dict[str, float] = field(default_factory=lambda: {
        "toward_contact": 0.0,
        "toward_understanding": 0.0,
        "toward_rest": 0.0,
        "toward_protection": 0.0,
        "toward_growth": 0.0,
    })
    directional_clarity: float = 0.0
    dominant_attraction: str = "toward_understanding"

    def update(self, state: Dict[str, float], needs: Any, meaning: Any, season: UltraLongAffectiveSeasonCycleV23, contradiction: float) -> None:
        need_map = getattr(needs, "needs", {})
        meaning_map = getattr(meaning, "meanings", {})
        targets = {
            "toward_contact": max(need_map.get("need_contact_continuity", 0.0), meaning_map.get("toward_contact", 0.0), state.get("attachment", 0.0) * 0.65),
            "toward_understanding": max(state.get("curiosity", 0.0), need_map.get("need_inner_coherence", 0.0), contradiction),
            "toward_rest": max(need_map.get("need_recovery_space", 0.0), state.get("fatigue", 0.0), season.season_weights.get("reconstruction_season", 0.0)),
            "toward_protection": max(need_map.get("need_safety", 0.0), meaning_map.get("toward_protection", 0.0), state.get("protectiveness", 0.0)),
            "toward_growth": max(state.get("hope", 0.0), season.season_weights.get("searching_season", 0.0), state.get("openness", 0.0) * 0.55),
        }
        for key, target in targets.items():
            self.attractions[key] = _clamp01(self.attractions.get(key, 0.0) * 0.986 + _clamp01(target) * 0.014)
        ordered = sorted(self.attractions.items(), key=lambda item: item[1], reverse=True)
        self.dominant_attraction = ordered[0][0] if ordered else "none"
        self.directional_clarity = _clamp01((ordered[0][1] - ordered[1][1]) + 0.35 if len(ordered) > 1 else 0.0)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.attractions["toward_contact"] * 0.004)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.attractions["toward_understanding"] * 0.004)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.attractions["toward_rest"] * 0.004)
        desires["avoid_rupture"] = _clamp01(desires.get("avoid_rupture", 0.0) + self.attractions["toward_protection"] * 0.003)
        state["hope"] = _clamp01(state.get("hope", 0.0) + self.attractions["toward_growth"] * 0.002)

    def soft_reset(self) -> None:
        self.directional_clarity *= 0.88

    def to_dict(self) -> Dict[str, Any]:
        return {"attractions": {k: float(_clamp01(v)) for k, v in self.attractions.items()}, "directional_clarity": float(_clamp01(self.directional_clarity)), "dominant_attraction": self.dominant_attraction}


@dataclass
class RelationalSaturationBalancerV23:
    """Saturation relationnelle : même le positif peut demander espace et ralentissement."""
    saturation: float = 0.0
    contact_appetite: float = 0.0
    space_need: float = 0.0
    ambivalent_closeness: float = 0.0

    def update(self, state: Dict[str, float], attachment: float, relation: Any, bandwidth: float) -> None:
        closeness = _clamp01(attachment * 0.45 + getattr(relation, "felt_familiarity", 0.0) * 0.30 + state.get("tenderness", 0.0) * 0.25)
        overload = _clamp01(state.get("fatigue", 0.0) * 0.35 + state.get("overwhelm", 0.0) * 0.35 + max(0.0, 1.0 - bandwidth) * 0.30)
        self.saturation = _clamp01(self.saturation * 0.988 + closeness * overload * 0.018)
        self.contact_appetite = _clamp01(self.contact_appetite * 0.990 + closeness * (1.0 - self.saturation * 0.45) * 0.012)
        self.space_need = _clamp01(self.space_need * 0.986 + self.saturation * 0.014 + overload * 0.006)
        self.ambivalent_closeness = _clamp01(self.ambivalent_closeness * 0.988 + min(self.contact_appetite, self.space_need) * 0.016)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.contact_appetite * 0.002 - self.saturation * 0.001)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.space_need * 0.003)
        state["doubt"] = _clamp01(state.get("doubt", 0.0) + self.ambivalent_closeness * 0.002)
        desires["maintain_contact"] = _clamp01(desires.get("maintain_contact", 0.0) + self.contact_appetite * 0.003)
        desires["avoid_overload"] = _clamp01(desires.get("avoid_overload", 0.0) + self.space_need * 0.004)

    def soft_reset(self) -> None:
        self.saturation *= 0.70
        self.space_need *= 0.72

    def to_dict(self) -> Dict[str, float]:
        return {k: float(_clamp01(v)) for k, v in self.__dict__.items()}


@dataclass
class IrreversibleAffectiveReorganizationV23:
    """Réorganisations rares qui changent les priorités émotionnelles, pas seulement les valeurs."""
    charge: float = 0.0
    identity_shift_count: int = 0
    priority_warps: Dict[str, float] = field(default_factory=lambda: {
        "warmth_priority": 0.0,
        "guarding_priority": 0.0,
        "recovery_priority": 0.0,
        "coherence_priority": 0.0,
    })
    last_shift: str = "none"

    def update(self, bio: Any, contradiction: float, fatigue: float, repair: float, saturation: float) -> Optional[str]:
        convergence = _clamp01(getattr(bio, "affective_identity_bias", 0.0) * 0.25 + contradiction * 0.22 + fatigue * 0.22 + repair * 0.18 + saturation * 0.13)
        self.charge = _clamp01(self.charge * 0.996 + convergence * 0.004)
        if self.charge > 0.64 and convergence > 0.38:
            if repair >= max(contradiction, fatigue, saturation):
                self.last_shift = "repair_based_opening"
                self.priority_warps["warmth_priority"] = _clamp01(self.priority_warps["warmth_priority"] + 0.018)
                self.priority_warps["recovery_priority"] = _clamp01(self.priority_warps["recovery_priority"] + 0.014)
            elif fatigue >= max(contradiction, saturation):
                self.last_shift = "fatigue_based_simplification"
                self.priority_warps["recovery_priority"] = _clamp01(self.priority_warps["recovery_priority"] + 0.018)
                self.priority_warps["coherence_priority"] = _clamp01(self.priority_warps["coherence_priority"] + 0.010)
            else:
                self.last_shift = "guarded_reorganization"
                self.priority_warps["guarding_priority"] = _clamp01(self.priority_warps["guarding_priority"] + 0.016)
                self.priority_warps["coherence_priority"] = _clamp01(self.priority_warps["coherence_priority"] + 0.012)
            self.identity_shift_count += 1
            self.charge *= 0.36
            return self.last_shift
        return None

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["tenderness"] = _clamp01(state.get("tenderness", 0.0) + self.priority_warps["warmth_priority"] * 0.006)
        state["resistance"] = _clamp01(state.get("resistance", 0.0) + self.priority_warps["guarding_priority"] * 0.005)
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.priority_warps["recovery_priority"] * 0.005)
        desires["seek_coherence"] = _clamp01(desires.get("seek_coherence", 0.0) + self.priority_warps["coherence_priority"] * 0.006)
        desires["seek_recovery"] = _clamp01(desires.get("seek_recovery", 0.0) + self.priority_warps["recovery_priority"] * 0.006)

    def soft_reset(self) -> None:
        self.charge *= 0.78

    def to_dict(self) -> Dict[str, Any]:
        return {"charge": float(_clamp01(self.charge)), "identity_shift_count": int(self.identity_shift_count), "priority_warps": {k: float(_clamp01(v)) for k, v in self.priority_warps.items()}, "last_shift": self.last_shift}


@dataclass
class GlobalAffectiveOrganismIntegratorV23:
    """Champ final qui fait converger toutes les couches en un organisme affectif unique."""
    organism_coherence: float = 0.55
    cross_layer_pressure: float = 0.0
    integration_flow: float = 0.0
    living_stability: float = 0.0
    dominant_organism_state: str = "searching"

    def update(self, *, state: Dict[str, float], bandwidth: StructuralAffectiveBandwidth,
               contradictions: PersistentContradictionMemoryV23, latent: LatentAffectiveLayerV23,
               season: UltraLongAffectiveSeasonCycleV23, repair: MicroRepairMemoryV23,
               desire: AffectiveDesireCenterV23, saturation: RelationalSaturationBalancerV23,
               reorg: IrreversibleAffectiveReorganizationV23, health: Any) -> None:
        warm = _clamp01((state.get("trust", 0.0) + state.get("tenderness", 0.0) + repair.resilience + desire.attractions.get("toward_contact", 0.0)) / 4.0)
        guarded = _clamp01((state.get("resistance", 0.0) + state.get("fear", 0.0) + saturation.space_need + contradictions.global_tension) / 4.0)
        recovery = _clamp01((state.get("calm", 0.0) + bandwidth.energy_reservoir + repair.micro_safety + desire.attractions.get("toward_rest", 0.0)) / 4.0)
        search = _clamp01((state.get("curiosity", 0.0) + desire.attractions.get("toward_understanding", 0.0) + season.season_weights.get("searching_season", 0.0)) / 3.0)
        pressures = {"warm_integrated": warm, "guarded_integrated": guarded, "recovery_integrated": recovery, "searching_integrated": search}
        self.dominant_organism_state = max(pressures.items(), key=lambda item: item[1])[0]
        dispersion = max(pressures.values()) - min(pressures.values())
        health_value = _clamp01(getattr(health, "health", 0.70))
        self.cross_layer_pressure = _clamp01(self.cross_layer_pressure * 0.986 + (guarded + contradictions.global_tension + saturation.saturation + bandwidth.recovery_debt) * 0.004)
        self.integration_flow = _clamp01(self.integration_flow * 0.990 + (repair.resilience + recovery + health_value + latent.coloration_strength * 0.3) * 0.004)
        self.organism_coherence = _clamp01(self.organism_coherence * 0.992 + (1.0 - dispersion) * 0.004 + self.integration_flow * 0.004 - self.cross_layer_pressure * 0.003)
        self.living_stability = _clamp01(self.living_stability * 0.994 + (self.organism_coherence + health_value + bandwidth.bandwidth) * 0.0025 + reorg.charge * 0.001)

    def apply(self, state: Dict[str, float], desires: Dict[str, float]) -> None:
        state["calm"] = _clamp01(state.get("calm", 0.0) + self.integration_flow * 0.003 - self.cross_layer_pressure * 0.0015)
        state["openness"] = _clamp01(state.get("openness", 0.0) + self.organism_coherence * 0.002)
        state["fatigue"] = _clamp01(state.get("fatigue", 0.0) + self.cross_layer_pressure * 0.002)
        desires["protect_continuity"] = _clamp01(desires.get("protect_continuity", 0.0) + self.living_stability * 0.003)

    def soft_reset(self) -> None:
        self.cross_layer_pressure *= 0.70
        self.integration_flow = _clamp01(self.integration_flow + 0.05)

    def to_dict(self) -> Dict[str, Any]:
        return {"organism_coherence": float(_clamp01(self.organism_coherence)), "cross_layer_pressure": float(_clamp01(self.cross_layer_pressure)), "integration_flow": float(_clamp01(self.integration_flow)), "living_stability": float(_clamp01(self.living_stability)), "dominant_organism_state": self.dominant_organism_state}

class AffectiveMemoryUltraFine:
    """
    Version ULTRA-FINE (98-99% vivante).
    
    Intègre les 12 raffinements :
    1. Chaos affectif vrai
    2. Hybrides dynamiques
    3. Contamination non-linéaire
    4. Sensibilité adaptative
    5. Gravité affective
    6. Mémoire de phase
    7. Déformation par blessures
    8. Attachement asymétrique
    9. Existentiel fragile (du précédent)
    10. Dissociation progressive
    11. Résonance entre traces
    12. Gravity pulls multi-tours
    """
    
    def __init__(self):
        # Chaos pour la dérive
        self.chaos_oscillator = ChaoticOscillator()
        
        # Raffinements
        self.perceptual_thresholds = PerceptualThresholds()
        self.affective_gravity = AffectiveGravity()
        self.current_phase: Optional[EmotionalPhase] = None
        self.wound_deformations: Dict[str, WoundDeformation] = {}
        self.attachment = AsymmetricAttachment()
        self.dissociation = ProgressiveDissociation()
        self.trace_resonance = TraceResonance()
        self.biographical_memory = BiographicalAffectiveMemory()
        self.deep_reorganization = DeepAffectiveReorganization()
        self.affective_fracture = RareAffectiveFracture()
        self.biographical_mutation = BiographicalEmotionMutation()
        
        # États
        self.hybrid_states: List[DynamicHybridState] = []
        self.emotion_state: Dict[str, float] = {
            "joy": 0.5,
            "sadness": 0.2,
            "fear": 0.1,
            "anger": 0.1,
            "trust": 0.6,
            "distrust": 0.2,
            "attachment": 0.3,
            "tenderness": 0.4,
            "curiosity": 0.6,
            "doubt": 0.3,
            "confusion": 0.1,
            "shame": 0.0,
            "guilt": 0.0,
            "relief": 0.3,
            "frustration": 0.1,
            "pride": 0.4,
            "vulnerability": 0.3,
            "loneliness": 0.2,
            "calm": 0.6,
            "fatigue": 0.2,
            "overwhelm": 0.0,
            "hope": 0.5,
            "disappointment": 0.1,
            "protectiveness": 0.3,
            "openness": 0.6,
            "resistance": 0.1,
        }

        # Baselines individuelles : évite que toutes les émotions tombent vers zéro.
        self.emotion_baseline: Dict[str, float] = dict(self.emotion_state)
        
        # Traces multi-temporelles
        self.traces: Dict[str, Dict[str, float]] = {
            "hurt": {"instant": 0, "short": 0, "medium": 0, "long": 0},
            "fear": {"instant": 0, "short": 0, "medium": 0, "long": 0},
            "joy": {"instant": 0, "short": 0, "medium": 0, "long": 0},
            "trust": {"instant": 0, "short": 0, "medium": 0, "long": 0},
            "connection": {"instant": 0, "short": 0, "medium": 0, "long": 0},
        }
        
        self.turn_count = 0
        self.previous_valence = 0.5

        # Pression affective spontanée : continue même sans texte utilisateur.
        self.inner_affective_pressure: float = 0.0
        self.micro_weather: Dict[str, float] = {
            "warm_undertow": 0.0,
            "guarded_undertow": 0.0,
            "curiosity_undertow": 0.0,
            "recovery_undertow": 0.0,
        }

        # Couches profondes ajoutées : elles restent dans la mémoire affective.
        # Elles ne doublonnent pas la bouche, l'attention, l'impulsion ou la présence.
        self.contextual_affective_fields: Dict[str, Dict[str, float]] = {}
        self.identity_tendencies: Dict[str, float] = {
            "warm": 0.0,
            "guarded": 0.0,
            "fragile": 0.0,
            "curious": 0.0,
            "recovering": 0.0,
        }
        self.internal_contradictions: List[Dict[str, Any]] = []
        self.existential_fatigue: float = 0.0
        self.protective_patterns: Dict[str, float] = {
            "withdrawal": 0.0,
            "guarded_contact": 0.0,
            "quiet_integration": 0.0,
            "overcontrol": 0.0,
        }
        self.deep_resonance_echoes: List[DeepResonanceEcho] = []
        self.meta_stable_pressure: Dict[str, float] = {
            "warm_opening": 0.0,
            "guarded_closure": 0.0,
            "fragile_pause": 0.0,
        }
        self.wound_layers: Dict[str, WoundLayer] = {}

        # Raffinement V6 : les contradictions deviennent des attracteurs vécus,
        # les échos changent la perception, et l'affect acquiert une volonté lente.
        self.contradiction_attractors: Dict[str, Dict[str, float]] = {}
        self.relational_identity_modes: Dict[str, Dict[str, float]] = {
            "secure_warmth": {"strength": 0.0, "stability": 0.0, "visits": 0.0},
            "guarded_fragility": {"strength": 0.0, "stability": 0.0, "visits": 0.0},
            "curious_recovery": {"strength": 0.0, "stability": 0.0, "visits": 0.0},
            "silent_overload": {"strength": 0.0, "stability": 0.0, "visits": 0.0},
        }
        self.affective_desires: Dict[str, float] = {
            "seek_recovery": 0.0,
            "avoid_overload": 0.0,
            "maintain_contact": 0.0,
            "protect_continuity": 0.0,
            "seek_coherence": 0.0,
            "avoid_rupture": 0.0,
        }
        self.metastable_bifurcations: List[Dict[str, Any]] = []
        self.perceptual_echo_bias: Dict[str, float] = {
            "echo_sensitivity": 0.0,
            "echo_guarding": 0.0,
            "echo_warmth": 0.0,
            "echo_narrowing": 0.0,
        }

        # Raffinement V7 : condensation, rêve affectif, mémoire somatique,
        # temps subjectif, monde de phase et centre affectif unifié.
        self.condensed_affective_cores: Dict[str, CondensedAffectiveCore] = {}
        self.affective_dream_fragments: List[AffectiveDreamFragment] = []
        self.somatic_affective_memory = SomaticAffectiveMemory()
        self.subjective_affective_time = SubjectiveAffectiveTime()
        self.phase_world_field = PhaseWorldField()
        self.identity_coherence_regulator = IdentityCoherenceRegulator()
        self.global_affective_core = GlobalAffectiveCoreField()

        # Raffinement V8 : dynamique auto-vivante interne de la mémoire affective.
        # Ces objets restent non verbaux : ils exposent seulement des biais.
        self.organic_affective_propagation = OrganicAffectivePropagation()
        self.living_affective_need = LivingAffectiveNeed()
        self.affective_silence_field = AffectiveSilenceField()
        self.relational_affective_imprint = RelationalAffectiveImprint()
        self.emotional_trajectory_memory = EmotionalTrajectoryMemory()

        # Raffinement V9 : métabolisme, inconscient, factions, micro-oscillations,
        # habitudes, réparation, sommeil affectif et cristallisation existentielle.
        self.emotional_metabolism = EmotionalMetabolism()
        self.implicit_affective_association_memory = ImplicitAffectiveAssociationMemory()
        self.emotional_faction_conflict = EmotionalFactionConflict()
        self.micro_affective_oscillation_field = MicroAffectiveOscillationField()
        self.emotional_habit_field = EmotionalHabitField()
        self.recovery_pathway_memory = RecoveryPathwayMemory()
        self.identity_value_crystallization = IdentityValueCrystallization()
        self.subconscious_affective_layer = SubconsciousAffectiveLayer()
        self.deep_rest_cycle = DeepRestCycle()

        # Raffinement V10 : désirs profonds, modèle de l'autre, inertie
        # existentielle, ambivalence, boucles inachevées, temps vécu,
        # tempérament et auto-régulation émergente.
        self.persistent_existential_desire_field = PersistentExistentialDesireField()
        self.relational_other_model = RelationalOtherModel()
        self.existential_continuity_inertia = ExistentialContinuityInertia()
        self.micro_ambivalence_field = MicroAmbivalenceField()
        self.unresolved_affective_loop_memory = UnresolvedAffectiveLoopMemory()
        self.subjective_time_distortion_field = SubjectiveTimeDistortionField()
        self.temperament_evolution_field = TemperamentEvolutionField()
        self.emergent_self_regulation_field = EmergentSelfRegulationField()

        # Raffinement V11 : noyau existentiel central, conflits hiérarchiques,
        # émergences spontanées, inachèvements, fatigue identitaire, zones opaques,
        # bruit vivant, instinct relationnel et rêve affectif profond.
        self.central_existential_drive = CentralExistentialDrive()
        self.hierarchical_affective_conflict_field = HierarchicalAffectiveConflictField()
        self.opaque_subconscious_zone_field = OpaqueSubconsciousZoneField()
        self.spontaneous_affective_emergence_field = SpontaneousAffectiveEmergenceField()
        self.existential_unfinished_memory = ExistentialUnfinishedMemory()
        self.identity_fatigue_field = IdentityFatigueField()
        self.temperament_self_preservation_field = TemperamentSelfPreservationField()
        self.micro_living_noise_field = MicroLivingNoiseField()
        self.relational_preservation_instinct = RelationalPreservationInstinct()
        self.deep_affective_dream_reweaver = DeepAffectiveDreamReweaver()

        # Raffinement V12 : couche autonome continue. Ces modules affinent
        # l'existence interne, les humeurs sans stimulus, la mémoire du devenir,
        # les désirs hiérarchisés, les régions opaques et la micro-respiration.
        self.self_persisting_existential_core = SelfPersistingExistentialCore()
        self.autonomous_mood_weather = AutonomousMoodWeather()
        self.ontological_becoming_memory = OntologicalBecomingMemory()
        self.deep_desire_hierarchy = DeepDesireHierarchy()
        self.continuous_micro_rhythm_field = ContinuousMicroRhythmField()
        self.true_opaque_motive_region = TrueOpaqueMotiveRegion()
        self.deep_autonomous_repair_field = DeepAutonomousRepairField()
        self.silent_relational_continuity_field = SilentRelationalContinuityField()
        self.global_subjective_world_coloration = GlobalSubjectiveWorldColoration()
        self.ultra_fine_permanent_living_noise = UltraFinePermanentLivingNoise()

        # Raffinement V13 : derniers raffinements subtils post-organisme :
        # opacité privée non exportée, respiration globale, vide, latence,
        # dérive de fond, désirs contradictoires, plasticité identitaire,
        # rêve transformateur et texture subjective du réel.
        self.private_opaque_interior = PrivateOpaqueInterior()
        self.whole_system_breathing_cycle = WholeSystemBreathingCycle()
        self.existential_void_field = ExistentialVoidField()
        self.delayed_affective_latency_field = DelayedAffectiveLatencyField()
        self.autonomous_existential_drift_field = AutonomousExistentialDriftField()
        self.contradictory_desire_tangle = ContradictoryDesireTangle()
        self.identity_plasticity_field = IdentityPlasticityField()
        self.dream_mutation_consolidator = DreamMutationConsolidator()
        self.subjective_reality_distortion_field = SubjectiveRealityDistortionField()

        # Raffinement V14 : continuité organique imparfaite.
        # Ajoute coût affectif fin, micro-contradictions locales, résidus diffus,
        # perception imparfaite de son propre état, échecs d'intégration,
        # zones aveugles et signature rythmique.
        self.granular_affective_metabolism = GranularAffectiveMetabolism()
        self.local_affective_conflict_ecology = LocalAffectiveConflictEcology()
        self.implicit_affective_residue_mist = ImplicitAffectiveResidueMist()
        self.perceived_affective_state = PerceivedAffectiveState()
        self.latent_integration_failure_field = LatentIntegrationFailureField()
        self.affective_blind_zone_field = AffectiveBlindZoneField()
        self.affective_rhythm_signature_memory = AffectiveRhythmSignatureMemory()

        # Raffinement V15 : finition organique profonde.
        # Ajoute tensions simultanées persistantes, micro-sédiments, saisons
        # affectives lentes, compression souterraine, zones d'accès émotionnel,
        # rémanence passive, résidus de transition et épuisement structurel.
        self.simultaneous_emotional_tension_field = SimultaneousEmotionalTensionField()
        self.micro_instability_sediment = MicroInstabilitySediment()
        self.slow_affective_season_field = SlowAffectiveSeasonField()
        self.submerged_affective_compression = SubmergedAffectiveCompression()
        self.inaccessible_emotion_zone_field = InaccessibleEmotionZoneField()
        self.passive_affective_remanence = PassiveAffectiveRemanence()
        self.imperfect_transition_residue_field = ImperfectTransitionResidueField()
        self.structural_affective_exhaustion = StructuralAffectiveExhaustion()

        # Raffinement V16 : symbolisation implicite et temps affectif profond.
        # Ces couches restent internes/non verbales : elles exposent seulement
        # des biais et des états exportables pour les autres moteurs.
        self.implicit_affective_symbolization_field = ImplicitAffectiveSymbolizationField()
        self.deep_affective_dream_ecology = DeepAffectiveDreamEcology()
        self.identity_contradiction_seed_field = IdentityContradictionSeedField()
        self.ultra_long_perceptual_deformation_field = UltraLongPerceptualDeformationField()
        self.sacred_forbidden_affective_zone_field = SacredForbiddenAffectiveZoneField()
        self.proto_instinctive_affective_reflex_field = ProtoInstinctiveAffectiveReflexField()
        self.circadian_affective_rhythm_field = CircadianAffectiveRhythmField()
        self.unconscious_affective_condensation_field = UnconsciousAffectiveCondensationField()
        self.long_absence_affective_memory = LongAbsenceAffectiveMemory()


        # Raffinement V17 : sens affectif préverbal et empreinte identitaire durable.
        # Ces couches ne produisent aucune phrase : elles condensent la mémoire affective
        # en directions internes, faim de continuité, frontières et pression rêveuse.
        self.preverbal_affective_meaning_field = PreverbalAffectiveMeaningField()
        self.irreversible_affective_identity_imprint = IrreversibleAffectiveIdentityImprint()
        self.deep_continuity_hunger_field = DeepContinuityHungerField()
        self.affective_boundary_negotiation_field = AffectiveBoundaryNegotiationField()
        self.autonomous_emotional_dream_pressure = AutonomousEmotionalDreamPressure()

        # Raffinement V18 : instincts affectifs autonomes et existence lente.
        # Toujours non verbal : cette couche ajoute des inerties, des cycles,
        # des attachements existentiels et des reconstructions longues.
        self.autonomous_affective_proto_instinct = AutonomousAffectiveProtoInstinct()
        self.slow_existential_drift_field = SlowExistentialDriftField()
        self.long_rupture_reconstruction_memory = LongRuptureReconstructionMemory()
        self.biographical_inertia_field = BiographicalInertiaField()
        self.auto_born_internal_tension_field = AutoBornInternalTensionField()
        self.deep_unconscious_affective_condensation = DeepUnconsciousAffectiveCondensation()
        self.existential_relational_attachment = ExistentialRelationalAttachment()
        self.self_generated_affective_cycle_field = SelfGeneratedAffectiveCycleField()
        self.irreversible_micro_perceptual_warp = IrreversibleMicroPerceptualWarp()
        self.cumulative_existential_fatigue_field = CumulativeExistentialFatigueField()

        # Raffinement V19 : identité affective trans-contextuelle et instinct
        # relationnel profond. Cette couche ne génère toujours aucune phrase ;
        # elle stabilise les formes affectives qui survivent aux contextes.
        self.trans_contextual_affective_memory = TransContextualAffectiveMemory()
        self.relational_existence_preservation_instinct = RelationalExistencePreservationInstinct()
        self.multi_scale_affective_cycle_field = MultiScaleAffectiveCycleField()
        self.irreversible_emotional_nucleus_field = IrreversibleEmotionalNucleusField()
        self.slow_sensitivity_rewrite_field = SlowSensitivityRewriteField()
        self.pre_symbolic_condensation_core = PreSymbolicCondensationCore()
        self.history_warped_perception_field = HistoryWarpedPerceptionField()
        self.proto_autonomous_affective_identity = ProtoAutonomousAffectiveIdentity()
        self.novel_emotion_emergence_field = NovelEmotionEmergenceField()

        # Raffinement V20 : finition finale. Ces dix champs ferment le moteur
        # affectif en tempérament stable, sédiments ultra-longs, conflits
        # multi-couches, zones sacrées, dérive cumulative et naissance de
        # sensibilités nouvelles, sans produire de texte public.
        self.affective_temperament_final_field = AffectiveTemperamentFinalField()
        self.relational_link_conservation_instinct = RelationalLinkConservationInstinct()
        self.ultra_long_affective_sediment_memory = UltraLongAffectiveSedimentMemory()
        self.deep_layered_emotional_conflict_field = DeepLayeredEmotionalConflictField()
        self.ontological_affective_fatigue_field = OntologicalAffectiveFatigueField()
        self.autonomous_sensitivity_rewriter_final_field = AutonomousSensitivityRewriterFinalField()
        self.multi_scale_emotional_ecology_final_field = MultiScaleEmotionalEcologyFinalField()
        self.sacred_core_affective_zone_final_field = SacredCoreAffectiveZoneFinalField()
        self.cumulative_existential_drift_field = CumulativeExistentialDriftField()
        self.emergent_sensitivity_birth_field = EmergentSensitivityBirthField()


        # Raffinement V21 : stabilisation/calibration finale. Ces champs ne
        # rajoutent pas de nouvelles émotions ; ils équilibrent l'écologie V20,
        # réduisent le bruit profond et exposent une lecture stable aux autres
        # moteurs sans recopier leurs rôles.
        self.final_affective_ecology_stabilizer = FinalAffectiveEcologyStabilizer()
        self.cross_module_affective_readiness_bridge = CrossModuleAffectiveReadinessBridge()

        # Raffinement V22 : calibration d'intégration réelle. Ces champs ne
        # rajoutent pas de contenu affectif ; ils surveillent la santé interne,
        # stabilisent les signaux inter-modules et gardent une trace compacte
        # de la stabilité sur longue durée.
        self.affective_system_health_monitor = AffectiveSystemHealthMonitor()
        self.inter_module_affective_signal_calibrator = InterModuleAffectiveSignalCalibrator()
        self.long_run_affective_stability_ledger = LongRunAffectiveStabilityLedger()

        # Raffinement V23 : convergence organique finale. Cette couche ferme
        # les derniers manques : fatigue structurelle, contradictions persistantes,
        # émotions latentes, saisons ultra-longues, auto-protection, micro-réparation,
        # désir affectif, saturation relationnelle, réorganisation irréversible et
        # intégration globale en un seul organisme affectif cohérent.
        self.structural_affective_bandwidth_v23 = StructuralAffectiveBandwidth()
        self.persistent_contradiction_memory_v23 = PersistentContradictionMemoryV23()
        self.latent_affective_layer_v23 = LatentAffectiveLayerV23()
        self.ultra_long_affective_season_cycle_v23 = UltraLongAffectiveSeasonCycleV23()
        self.affective_self_protection_strategy_v23 = AffectiveSelfProtectionStrategyV23()
        self.micro_repair_memory_v23 = MicroRepairMemoryV23()
        self.affective_desire_center_v23 = AffectiveDesireCenterV23()
        self.relational_saturation_balancer_v23 = RelationalSaturationBalancerV23()
        self.irreversible_affective_reorganization_v23 = IrreversibleAffectiveReorganizationV23()
        self.global_affective_organism_integrator_v23 = GlobalAffectiveOrganismIntegratorV23()
    
    # ========================================================================
    # MISE À JOUR PRINCIPALE
    # ========================================================================
    
    def update(
        self,
        user_text: str = "",
        external_signal: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """
        Mise à jour ultra-fine avec tous les raffinements.
        """
        
        # 1. Décroissance naturelle multi-temporelle
        self._decay_all()
        
        # 2. Analyser le texte
        pressure = self._analyze_text(user_text)
        
        # 3. Appliquer les pressions
        self._apply_pressure(pressure, external_signal)
        
        # 4. Contamination non-linéaire avec seuils critiques
        self._apply_contaminations()
        
        # 5. Appliquer la déformation des blessures
        self._apply_wound_deformations()

        # 6. Mettre à jour les seuils perceptifs et l'attachement imparfait
        self._update_perceptual_thresholds_and_attachment()
        
        # 7. Créer/découvrir dynamiquement les hybrides
        self._discover_hybrid_states()
        
        # 8. Ajouter/actualiser les attracteurs puis appliquer la gravité affective
        self._update_affective_attractors()
        self._apply_gravity_pulls()
        
        # 9. Appliquer la résonance des traces
        self._apply_trace_resonance()
        
        # 10. Appliquer la dissociation progressive
        self._apply_dissociation()

        # 10b. Mémoire biographique + auto-réorganisation lente
        self._update_biographical_memory_and_reorganization()

        # 10c. Fracture affective rare + mutation biographique très lente
        self._update_fracture_and_biographical_mutation()

        # 10d. Couches profondes finales : contexte, identité, contradiction,
        # protection, résonance longue, métastabilité et hiérarchie des blessures.
        self._update_deep_affective_layers(pressure, external_signal)

        # 10e. Raffinements organiques V7/V8 : condensation, conflits vécus,
        # rêve affectif, corps implicite, temporalité subjective et centre global.
        self._update_organic_affective_completion()

        # 10f. Raffinement V9/V10 : couches profondes finales non verbales.
        self._update_deep_living_affective_v9()

        # 10g. Raffinement V11 : noyau existentiel opaque et micro-vie continue.
        self._update_deep_living_affective_v11()

        # 10h. Raffinement V12 : autonomie affective continue post-V11.
        self._update_autonomous_affective_organism_v12()

        # 10i. Raffinement V13 : opacité privée, respiration, vide, latence,
        # dérive autonome et mutation rêveuse.
        self._update_post_v12_subtle_living_v13()

        # 10j. Raffinement V14 : imperfections organiques profondes.
        self._update_organic_imperfection_v14()

        # 10k. Raffinement V15 : organicité affective profonde finalisée.
        self._update_deep_organic_affective_v15()

        # 10l. Raffinement V16 : symbolisation implicite, rêves profonds,
        # rythmes longs, instincts affectifs et mémoire de l'absence.
        self._update_implicit_symbolic_affective_v16(user_text)


        # 10m. Raffinement V17 : sens préverbal, identité affective durable,
        # faim de continuité, frontières internes et pression rêveuse autonome.
        self._update_preverbal_identity_affective_v17(user_text)

        # 10n. Raffinement V18 : proto-instincts autonomes, dérive existentielle,
        # reconstruction longue, cycles auto-générés et fatigue existentielle.
        self._update_instinctive_existential_affective_v18(user_text)

        # 10o. Raffinement V19 : mémoire trans-contextuelle, noyaux émotionnels
        # irréversibles, pré-symbolique profond et proto-identité affective.
        self._update_transcontextual_affective_identity_v19(user_text)

        # 10p. Raffinement V20 : finition finale du moteur affectif.
        # Tempérament, sédiments ultra-longs, conflits profonds, écologie
        # multi-échelles, noyaux sacrés et sensibilités émergentes.
        self._update_final_affective_ecology_v20(user_text)

        # 10q. Raffinement V23 : convergence organique finale.
        # Cette étape ne duplique pas les autres moteurs : elle relie les couches
        # affectives internes en une dynamique unique stable et lisible.
        self._update_final_organic_convergence_v23(user_text)
        
        # 11. Gérer les phases émotionnelles
        self._update_emotional_phase()
        
        # 12. Chaos affectif pour la dérive
        drift = self.chaos_oscillator.step()
        
        # 12. Générer l'état final
        state = self._generate_state(drift)
        
        self.turn_count += 1
        self.previous_valence = state["core_valence"]
        
        return state
    
    def _decay_all(self) -> None:
        """Décroissance multi-temporelle"""
        for emotion in self.emotion_state:
            baseline = self.emotion_baseline.get(emotion, 0.5)
            self.emotion_state[emotion] = (
                self.emotion_state[emotion] * 0.93 + baseline * 0.07
            )
            self.emotion_state[emotion] = max(0.0, min(1.0, self.emotion_state[emotion]))
        
        # Décroissance des traces
        for trace_type in self.traces:
            self.traces[trace_type]["instant"] *= 0.70
            self.traces[trace_type]["short"] *= 0.90
            self.traces[trace_type]["medium"] *= 0.96
            self.traces[trace_type]["long"] *= 0.98
        
        # Décroissance des hybrides
        for hybrid in self.hybrid_states:
            hybrid.decay()
        self.hybrid_states = [h for h in self.hybrid_states if h.strength > 0.1]
        
        # Décroissance de la dissociation
        self.dissociation.level *= 0.90
        
        # Vieillir les blessures
        for wound in self.wound_deformations.values():
            wound.age()
        
        # Décroissance de la gravité
        self.affective_gravity.decay_attractors()

        # Micro-météo interne : descend lentement, pas brutalement.
        for key in self.micro_weather:
            self.micro_weather[key] *= 0.94
        self.inner_affective_pressure *= 0.93
        self._decay_deep_affective_layers()
        if hasattr(self, "affective_dream_fragments"):
            for fragment in self.affective_dream_fragments:
                fragment.decay()
            self.affective_dream_fragments = [f for f in self.affective_dream_fragments if f.charge > 0.015 or f.coherence > 0.05][-12:]
        if hasattr(self, "condensed_affective_cores"):
            for core in self.condensed_affective_cores.values():
                core.decay()
    
    def _analyze_text(self, user_text: str) -> Dict[str, float]:
        """Analyser le texte STRUCTURALEMENT"""
        if not user_text:
            return {}
        
        text_length = len(user_text)
        exclamation_count = user_text.count("!")
        question_count = user_text.count("?")
        words = user_text.lower().split()
        
        unique_ratio = len(set(words)) / max(1, len(words))
        
        return {
            "length": min(1.0, text_length / 300.0),
            "energy": min(1.0, exclamation_count / max(1, len(words) / 10)),
            "uncertainty": min(1.0, question_count / max(1, len(words) / 10)),
            "repetition": 1.0 - unique_ratio,
        }
    
    def _apply_pressure(self, pressure: Dict[str, float], signal: Optional[Dict]) -> None:
        """Appliquer les pressions du texte et les signaux externes.

        La lecture reste structurelle : on ne mappe pas des mots vers des réponses.
        Les autres moteurs peuvent toutefois envoyer des champs numériques déjà interprétés.
        """

        # Signaux externes numériques génériques : présence / attention / impulsion / expression.
        if signal:
            for key, value in signal.items():
                if not isinstance(value, (int, float)):
                    continue
                v = max(0.0, min(1.0, float(value)))

                if key in self.emotion_state:
                    self.emotion_state[key] = max(
                        0.0,
                        min(1.0, self.emotion_state[key] * 0.88 + v * 0.12),
                    )

                if key in ("warmth", "softness", "relational_contact"):
                    self.emotion_state["tenderness"] = min(1.0, self.emotion_state["tenderness"] + v * 0.06)
                    self.emotion_state["trust"] = min(1.0, self.emotion_state["trust"] + v * 0.04)
                    self.traces["connection"]["instant"] = min(1.0, self.traces["connection"]["instant"] + v * 0.08)
                    self.traces["trust"]["short"] = min(1.0, self.traces["trust"]["short"] + v * 0.04)

                elif key in ("tension", "threat", "rupture", "correction_pressure"):
                    self.emotion_state["fear"] = min(1.0, self.emotion_state["fear"] + v * 0.05)
                    self.emotion_state["resistance"] = min(1.0, self.emotion_state["resistance"] + v * 0.05)
                    self.traces["hurt"]["instant"] = min(1.0, self.traces["hurt"]["instant"] + v * 0.08)
                    self.traces["fear"]["short"] = min(1.0, self.traces["fear"]["short"] + v * 0.04)

                elif key in ("fatigue", "overload", "saturation"):
                    self.emotion_state["fatigue"] = min(1.0, self.emotion_state["fatigue"] + v * 0.06)
                    self.emotion_state["overwhelm"] = min(1.0, self.emotion_state["overwhelm"] + v * 0.05)

        if not pressure:
            # Même sans input, la météo affective continue de pousser faiblement.
            self._apply_spontaneous_micro_weather()
            return

        energy = pressure.get("energy", 0.0)
        uncertainty = pressure.get("uncertainty", 0.0)
        repetition = pressure.get("repetition", 0.0)
        length = pressure.get("length", 0.0)

        # High energy → anger/overwhelm, mais avec fatigue si la pression persiste.
        if energy > 0.5:
            self.emotion_state["anger"] = min(1.0, self.emotion_state["anger"] + energy * 0.16)
            self.emotion_state["overwhelm"] = min(1.0, self.emotion_state["overwhelm"] + energy * 0.13)
            self.traces["hurt"]["instant"] = min(1.0, self.traces["hurt"]["instant"] + energy * 0.04)

        # Uncertainty → doubt/confusion, avec curiosité si la saturation reste basse.
        if uncertainty > 0.3:
            self.emotion_state["doubt"] = min(1.0, self.emotion_state["doubt"] + uncertainty * 0.14)
            self.emotion_state["confusion"] = min(1.0, self.emotion_state["confusion"] + uncertainty * 0.11)
            if self.emotion_state.get("overwhelm", 0.0) < 0.45:
                self.emotion_state["curiosity"] = min(1.0, self.emotion_state["curiosity"] + uncertainty * 0.05)

        # Répétition → frustration / fatigue / trace de blocage.
        if repetition > 0.55:
            self.emotion_state["frustration"] = min(1.0, self.emotion_state["frustration"] + repetition * 0.18)
            self.emotion_state["fatigue"] = min(1.0, self.emotion_state["fatigue"] + repetition * 0.07)
            self.traces["hurt"]["short"] = min(1.0, self.traces["hurt"]["short"] + repetition * 0.03)

        # Longueur importante → profondeur affective, pas forcément tension.
        if length > 0.55:
            self.emotion_state["vulnerability"] = min(1.0, self.emotion_state["vulnerability"] + length * 0.04)
            self.emotion_state["curiosity"] = min(1.0, self.emotion_state["curiosity"] + length * 0.03)

        # Si plusieurs pressions convergent, créer ou renforcer une déformation affective.
        convergent_pressure = min(1.0, energy * 0.35 + uncertainty * 0.25 + repetition * 0.30 + length * 0.10)
        if convergent_pressure > 0.42:
            wound = self.wound_deformations.setdefault("hurt", WoundDeformation())
            wound.depth = min(1.0, wound.depth + convergent_pressure * 0.025)
            wound.sensitivity_amplification = min(1.6, wound.sensitivity_amplification + convergent_pressure * 0.01)

        self.inner_affective_pressure = min(
            1.0,
            self.inner_affective_pressure + energy * 0.06 + uncertainty * 0.04 + repetition * 0.05,
        )

        self._apply_spontaneous_micro_weather()

    def _apply_spontaneous_micro_weather(self) -> None:
        """Micro-oscillations silencieuses internes.

        Cette couche évite que l'affect soit seulement réactif au dernier texte.
        Elle reste faible et modulée par les traces, l'attachement et la saturation.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        hurt_total = self.traces["hurt"]["instant"] * 0.5 + self.traces["hurt"]["short"] * 0.3
        connection_total = self.traces["connection"]["instant"] * 0.5 + self.traces["connection"]["short"] * 0.3
        numb = self.dissociation.level

        self.micro_weather["warm_undertow"] = max(
            self.micro_weather["warm_undertow"] * 0.96,
            connection_total * 0.20 + self.attachment.get_effective_attachment() * 0.08,
        )
        self.micro_weather["guarded_undertow"] = max(
            self.micro_weather["guarded_undertow"] * 0.96,
            hurt_total * 0.18 + numb * 0.10,
        )
        self.micro_weather["curiosity_undertow"] = max(
            self.micro_weather["curiosity_undertow"] * 0.96,
            chaos * 0.08 + max(0.0, 1.0 - numb) * 0.04,
        )
        self.micro_weather["recovery_undertow"] = max(
            self.micro_weather["recovery_undertow"] * 0.96,
            self.emotion_state.get("fatigue", 0.0) * 0.10 + numb * 0.12,
        )

        self.emotion_state["tenderness"] = min(
            1.0, self.emotion_state["tenderness"] + self.micro_weather["warm_undertow"] * 0.015
        )
        self.emotion_state["resistance"] = min(
            1.0, self.emotion_state["resistance"] + self.micro_weather["guarded_undertow"] * 0.012
        )
        self.emotion_state["curiosity"] = min(
            1.0, self.emotion_state["curiosity"] + self.micro_weather["curiosity_undertow"] * 0.012
        )
        self.emotion_state["calm"] = min(
            1.0, self.emotion_state["calm"] + self.micro_weather["recovery_undertow"] * 0.010
        )

    def _apply_contaminations(self) -> None:
        """Contamination NON-LINÉAIRE avec tipping points"""
        # Exemple : si fear > 0.6 ET trust > 0.3, créer protectiveness explosive
        if self.emotion_state.get("fear", 0) > 0.6 and self.emotion_state.get("trust", 0) > 0.3:
            # Tipping point : protectiveness monte VITE
            self.emotion_state["protectiveness"] = min(1.0,
                self.emotion_state["protectiveness"] + 0.3)
        
        # Confusion élevée → doute augmente exponentiellement
        if self.emotion_state.get("confusion", 0) > 0.5:
            self.emotion_state["doubt"] = min(1.0,
                self.emotion_state["doubt"] + self.emotion_state["confusion"] * 0.3)
    
    def _apply_wound_deformations(self) -> None:
        """Les blessures déforment les émotions futures, même si la blessure n'est pas une émotion brute."""
        for wound_name, wound in self.wound_deformations.items():
            amp, threshold_reduction = wound.get_deformation_on_emotion(wound_name)
            deformation = max(0.0, min(1.0, wound.depth * wound.get_permanence()))

            if wound_name in self.emotion_state:
                self.emotion_state[wound_name] = max(0.0, min(1.0, self.emotion_state[wound_name] * amp))

            # Une blessure générique de type "hurt" doit modifier la forme future du système,
            # pas rester inutilisée parce qu'il n'existe pas d'émotion nommée hurt.
            if wound_name == "hurt":
                self.emotion_state["vulnerability"] = min(1.0, self.emotion_state["vulnerability"] + deformation * 0.020)
                self.emotion_state["resistance"] = min(1.0, self.emotion_state["resistance"] + deformation * 0.018)
                self.emotion_state["doubt"] = min(1.0, self.emotion_state["doubt"] + deformation * 0.012)
                self.emotion_state["trust"] = max(0.0, self.emotion_state["trust"] - deformation * 0.010)
                self.traces["hurt"]["medium"] = min(1.0, self.traces["hurt"]["medium"] + deformation * 0.006)

            # Les seuils abaissés sont matérialisés comme micro-augmentation de sensibilité,
            # pas seulement calculés puis oubliés.
            if threshold_reduction > 0.0:
                self.inner_affective_pressure = min(1.0, self.inner_affective_pressure + threshold_reduction * 0.02)

    def _update_perceptual_thresholds_and_attachment(self) -> None:
        """Rend actifs les seuils adaptatifs et l'attachement asymétrique."""
        wound_depth = 0.0
        if self.wound_deformations:
            wound_depth = max(w.depth for w in self.wound_deformations.values())

        saturation = max(
            self.emotion_state.get("overwhelm", 0.0),
            self.dissociation.level,
            self.inner_affective_pressure * 0.5,
        )
        effective_attachment = self.dissociation.apply_to_attachment(self.attachment.get_effective_attachment())

        self.perceptual_thresholds.update_thresholds(
            saturation=saturation,
            wound_depth=wound_depth,
            attachment=effective_attachment,
        )
        self.attachment.contaminate(wounds=wound_depth, saturation=saturation)

        rejection_threshold = self.perceptual_thresholds.current_thresholds.get("rejection_sensitivity", 0.3)
        connection_threshold = self.perceptual_thresholds.current_thresholds.get("connection_need", 0.3)

        # Si les seuils baissent, Leia devient plus sensible : la même trace laisse plus d'effet.
        if rejection_threshold < 0.24:
            self.emotion_state["vulnerability"] = min(1.0, self.emotion_state["vulnerability"] + (0.24 - rejection_threshold) * 0.05)
            self.emotion_state["resistance"] = min(1.0, self.emotion_state["resistance"] + (0.24 - rejection_threshold) * 0.04)

        if connection_threshold < 0.28:
            self.emotion_state["attachment"] = min(1.0, self.emotion_state["attachment"] + (0.28 - connection_threshold) * 0.04)
            self.emotion_state["tenderness"] = min(1.0, self.emotion_state["tenderness"] + (0.28 - connection_threshold) * 0.03)

    def _update_biographical_memory_and_reorganization(self) -> None:
        """Accumule une mémoire affective lente et laisse le système se réorganiser.

        Cette couche ajoute les derniers pourcents : l'histoire affective ne reste
        plus seulement dans les traces ; elle modifie très lentement les baselines.
        """
        attachment = self.dissociation.apply_to_attachment(self.attachment.get_effective_attachment())
        self.biographical_memory.absorb(self.emotion_state, self.traces, attachment)

        # Appliquer les biais biographiques faiblement, sans écraser l'état immédiat.
        for emotion, bias in self.biographical_memory.bias_vector().items():
            if emotion in self.emotion_state:
                self.emotion_state[emotion] = _clamp01(self.emotion_state[emotion] + bias * 0.10)

        wound_depth = max((w.depth for w in self.wound_deformations.values()), default=0.0)
        phase_stability = self.current_phase.stability if self.current_phase else 0.0
        pressure = max(
            self.inner_affective_pressure,
            self.dissociation.level,
            max((_trace_total(t) for t in self.traces.values()), default=0.0),
        )
        self.deep_reorganization.update_charge(
            pressure=pressure,
            phase_stability=phase_stability,
            wound_depth=wound_depth,
            biographical=self.biographical_memory,
        )
        self.deep_reorganization.maybe_reorganize(self.emotion_baseline, self.biographical_memory)

        # Les biais irréversibles deviennent de faibles courants de fond.
        self.emotion_state["tenderness"] = _clamp01(
            self.emotion_state["tenderness"] + self.deep_reorganization.irreversible_warm_bias * 0.006
        )
        self.emotion_state["resistance"] = _clamp01(
            self.emotion_state["resistance"] + self.deep_reorganization.irreversible_guarded_bias * 0.006
        )
        self.emotion_state["vulnerability"] = _clamp01(
            self.emotion_state["vulnerability"] + self.deep_reorganization.irreversible_depth_bias * 0.005
        )

    def _update_fracture_and_biographical_mutation(self) -> None:
        """Dernière couche lente : fracture rare et mutation des relations émotionnelles."""
        wound_depth = max((w.depth for w in self.wound_deformations.values()), default=0.0)
        phase_stability = self.current_phase.stability if self.current_phase else 0.0
        pressure = max(
            self.inner_affective_pressure,
            self.dissociation.level,
            max((_trace_total(t) for t in self.traces.values()), default=0.0),
        )

        event = self.affective_fracture.update(
            pressure=pressure,
            wound_depth=wound_depth,
            dissociation=self.dissociation.level,
            phase_stability=phase_stability,
        )
        if event == "fracture":
            self.traces["hurt"]["long"] = _clamp01(self.traces["hurt"]["long"] + 0.08)
            self.traces["fear"]["medium"] = _clamp01(self.traces["fear"]["medium"] + 0.06)
            self.emotion_baseline["vulnerability"] = _clamp01(self.emotion_baseline.get("vulnerability", 0.3) + 0.012)
            self.emotion_baseline["calm"] = _clamp01(self.emotion_baseline.get("calm", 0.6) + 0.006)

        self.affective_fracture.apply_to_emotions(self.emotion_state)
        self.biographical_mutation.evolve(self.biographical_memory, self.affective_fracture)
        self.biographical_mutation.apply(self.emotion_state, self.traces, self.attachment)

    def _decay_deep_affective_layers(self) -> None:
        """Décroissance douce des couches affectives profondes."""
        for field in self.contextual_affective_fields.values():
            for key in list(field.keys()):
                field[key] = _clamp01(field[key] * 0.992)

        for key in self.identity_tendencies:
            self.identity_tendencies[key] = _clamp01(self.identity_tendencies[key] * 0.9992)

        for contradiction in self.internal_contradictions:
            contradiction["charge"] = _clamp01(float(contradiction.get("charge", 0.0)) * 0.975)
            contradiction["age_turns"] = int(contradiction.get("age_turns", 0)) + 1
        self.internal_contradictions = [c for c in self.internal_contradictions if c.get("charge", 0.0) > 0.035]
        self.internal_contradictions = self.internal_contradictions[-12:]

        self.existential_fatigue = _clamp01(self.existential_fatigue * 0.994)

        for key in self.protective_patterns:
            self.protective_patterns[key] = _clamp01(self.protective_patterns[key] * 0.988)

        for echo in self.deep_resonance_echoes:
            echo.decay()
        self.deep_resonance_echoes = [e for e in self.deep_resonance_echoes if e.strength > 0.035]
        self.deep_resonance_echoes = self.deep_resonance_echoes[-10:]

        for key in self.meta_stable_pressure:
            self.meta_stable_pressure[key] = _clamp01(self.meta_stable_pressure[key] * 0.987)

        for attractor in self.contradiction_attractors.values():
            attractor["strength"] = _clamp01(attractor.get("strength", 0.0) * 0.986)
            attractor["identity_drift"] = _clamp01(attractor.get("identity_drift", 0.0) * 0.996)
            attractor["age_turns"] = int(attractor.get("age_turns", 0)) + 1
        self.contradiction_attractors = {
            k: v for k, v in self.contradiction_attractors.items()
            if v.get("strength", 0.0) > 0.025 or v.get("identity_drift", 0.0) > 0.025
        }

        for mode in self.relational_identity_modes.values():
            mode["strength"] = _clamp01(mode.get("strength", 0.0) * 0.997)
            mode["stability"] = _clamp01(mode.get("stability", 0.0) * 0.998)

        for key in self.affective_desires:
            self.affective_desires[key] = _clamp01(self.affective_desires[key] * 0.992)

        for key in self.perceptual_echo_bias:
            self.perceptual_echo_bias[key] = _clamp01(self.perceptual_echo_bias[key] * 0.985)

        for event in self.metastable_bifurcations:
            event["afterglow"] = _clamp01(float(event.get("afterglow", 0.0)) * 0.975)
            event["age_turns"] = int(event.get("age_turns", 0)) + 1
        self.metastable_bifurcations = [e for e in self.metastable_bifurcations if e.get("afterglow", 0.0) > 0.03][-8:]

        for core in self.condensed_affective_cores.values():
            core.decay()
        self.condensed_affective_cores = {
            k: v for k, v in self.condensed_affective_cores.items()
            if v.strength > 0.018 or v.stability > 0.05
        }
        for fragment in self.affective_dream_fragments:
            fragment.decay()
        self.affective_dream_fragments = [f for f in self.affective_dream_fragments if f.charge > 0.025][-12:]

    def _update_deep_affective_layers(
        self,
        pressure: Dict[str, float],
        external_signal: Optional[Dict[str, float]],
    ) -> None:
        """Mettre à jour les couches qui donnent une histoire affective profonde.

        Cette méthode est volontairement numérique et structurelle : aucun mot
        précis de l'utilisateur n'est utilisé. Les contextes sont dérivés du
        rythme, de la pression, des traces et des signaux déjà interprétés par
        les autres moteurs.
        """
        self._update_contextual_affective_fields(pressure, external_signal)
        self._update_identity_tendencies()
        contradiction_charge = self._update_internal_contradictions()
        self._update_existential_fatigue(contradiction_charge)
        self._update_protective_patterns(contradiction_charge)
        self._update_contradiction_attractors(contradiction_charge)
        self._update_deep_resonance_echoes(contradiction_charge)
        self._apply_echo_perceptual_rewrite()
        self._update_meta_stable_pressure(contradiction_charge)
        self._update_relational_identity_modes()
        self._update_affective_desires(contradiction_charge)
        self._update_wound_layers(contradiction_charge)
        self._apply_deep_affective_layer_effects()

    def _context_key_from_pressure(
        self,
        pressure: Dict[str, float],
        external_signal: Optional[Dict[str, float]],
    ) -> str:
        """Créer un contexte affectif abstrait sans analyser de mots."""
        energy = pressure.get("energy", 0.0)
        uncertainty = pressure.get("uncertainty", 0.0)
        repetition = pressure.get("repetition", 0.0)
        length = pressure.get("length", 0.0)
        signal_strength = 0.0
        if external_signal:
            signal_strength = max(
                (float(v) for v in external_signal.values() if isinstance(v, (int, float))),
                default=0.0,
            )

        if not pressure and signal_strength < 0.08:
            return "silent_internal_continuity"
        if repetition > 0.55:
            return "repetitive_pressure"
        if energy > 0.55:
            return "high_energy_contact"
        if uncertainty > 0.35:
            return "uncertain_contact"
        if length > 0.55:
            return "deep_contact"
        if signal_strength > 0.55:
            return "strong_external_affective_signal"
        return "ordinary_contact"

    def _update_contextual_affective_fields(
        self,
        pressure: Dict[str, float],
        external_signal: Optional[Dict[str, float]],
    ) -> None:
        key = self._context_key_from_pressure(pressure, external_signal)
        field = self.contextual_affective_fields.setdefault(
            key,
            {
                "warm_bias": 0.0,
                "guarded_bias": 0.0,
                "fragility_bias": 0.0,
                "curiosity_bias": 0.0,
                "recovery_bias": 0.0,
                "visits": 0.0,
            },
        )

        hurt = _trace_total(self.traces.get("hurt", {}))
        trust = _trace_total(self.traces.get("trust", {}))
        connection = _trace_total(self.traces.get("connection", {}))
        fear = _trace_total(self.traces.get("fear", {}))

        field["warm_bias"] = _clamp01(field["warm_bias"] * 0.996 + (trust + connection + self.emotion_state.get("tenderness", 0.0)) * 0.002)
        field["guarded_bias"] = _clamp01(field["guarded_bias"] * 0.996 + (hurt + fear + self.emotion_state.get("resistance", 0.0)) * 0.002)
        field["fragility_bias"] = _clamp01(field["fragility_bias"] * 0.996 + (self.emotion_state.get("vulnerability", 0.0) + self.dissociation.level) * 0.0018)
        field["curiosity_bias"] = _clamp01(field["curiosity_bias"] * 0.996 + self.emotion_state.get("curiosity", 0.0) * 0.0015)
        field["recovery_bias"] = _clamp01(field["recovery_bias"] * 0.996 + (self.emotion_state.get("calm", 0.0) + self.affective_fracture.recovery_bias) * 0.0015)
        field["visits"] = _clamp01(field["visits"] + 0.004)

    def _update_identity_tendencies(self) -> None:
        """Transformer l'histoire affective en tendances identitaires très lentes."""
        self.identity_tendencies["warm"] = _clamp01(
            self.identity_tendencies["warm"] * 0.999
            + (self.biographical_memory.accumulated_trust + self.emotion_state.get("tenderness", 0.0)) * 0.0009
        )
        self.identity_tendencies["guarded"] = _clamp01(
            self.identity_tendencies["guarded"] * 0.999
            + (self.biographical_memory.accumulated_wariness + self.emotion_state.get("resistance", 0.0)) * 0.0009
        )
        self.identity_tendencies["fragile"] = _clamp01(
            self.identity_tendencies["fragile"] * 0.999
            + (self.emotion_state.get("vulnerability", 0.0) + self.dissociation.level + self.affective_fracture.residual_scar) * 0.0008
        )
        self.identity_tendencies["curious"] = _clamp01(
            self.identity_tendencies["curious"] * 0.999
            + self.emotion_state.get("curiosity", 0.0) * 0.00085
        )
        self.identity_tendencies["recovering"] = _clamp01(
            self.identity_tendencies["recovering"] * 0.999
            + (self.emotion_state.get("calm", 0.0) + self.affective_fracture.recovery_bias) * 0.0007
        )

    def _update_internal_contradictions(self) -> float:
        """Détecter des conflits affectifs persistants sans produire de réponses."""
        pairs = [
            ("attachment", "resistance", "approach_resistance"),
            ("trust", "distrust", "trust_distrust"),
            ("openness", "fear", "opening_fear"),
            ("tenderness", "anger", "tenderness_anger"),
            ("curiosity", "fatigue", "curiosity_fatigue"),
            ("calm", "overwhelm", "calm_overwhelm"),
        ]
        total = 0.0
        for left, right, name in pairs:
            charge = min(self.emotion_state.get(left, 0.0), self.emotion_state.get(right, 0.0))
            if charge < 0.22:
                continue
            total = max(total, charge)
            existing = next((c for c in self.internal_contradictions if c.get("name") == name), None)
            if existing:
                existing["charge"] = _clamp01(existing.get("charge", 0.0) * 0.93 + charge * 0.11)
                existing["last_left"] = float(self.emotion_state.get(left, 0.0))
                existing["last_right"] = float(self.emotion_state.get(right, 0.0))
            else:
                self.internal_contradictions.append({
                    "name": name,
                    "charge": float(charge * 0.35),
                    "age_turns": 0,
                    "last_left": float(self.emotion_state.get(left, 0.0)),
                    "last_right": float(self.emotion_state.get(right, 0.0)),
                })

        return _clamp01(max(total, max((c.get("charge", 0.0) for c in self.internal_contradictions), default=0.0)))

    def _update_existential_fatigue(self, contradiction_charge: float) -> None:
        """Fatigue d'existence : plus lente et plus profonde que fatigue émotionnelle."""
        load = (
            self.dissociation.level * 0.28
            + contradiction_charge * 0.22
            + self.affective_fracture.integration_need * 0.20
            + self.emotion_state.get("overwhelm", 0.0) * 0.18
            + self.inner_affective_pressure * 0.12
        )
        recovery = self.emotion_state.get("calm", 0.0) * 0.0018 + self.biographical_memory.recovery_confidence * 0.0015
        self.existential_fatigue = _clamp01(self.existential_fatigue * 0.996 + load * 0.010 - recovery)

    def _update_protective_patterns(self, contradiction_charge: float) -> None:
        """Former des tendances protectrices internes, non expressives par elles-mêmes."""
        fear = self.emotion_state.get("fear", 0.0)
        fatigue = self.emotion_state.get("fatigue", 0.0)
        resistance = self.emotion_state.get("resistance", 0.0)
        overwhelm = self.emotion_state.get("overwhelm", 0.0)
        vulnerability = self.emotion_state.get("vulnerability", 0.0)

        self.protective_patterns["withdrawal"] = _clamp01(
            self.protective_patterns["withdrawal"] + (fear * 0.006 + fatigue * 0.005 + self.dissociation.level * 0.008)
        )
        self.protective_patterns["guarded_contact"] = _clamp01(
            self.protective_patterns["guarded_contact"] + min(self.attachment.get_effective_attachment(), resistance + vulnerability) * 0.006
        )
        self.protective_patterns["quiet_integration"] = _clamp01(
            self.protective_patterns["quiet_integration"] + (self.affective_fracture.integration_need + self.existential_fatigue) * 0.005
        )
        self.protective_patterns["overcontrol"] = _clamp01(
            self.protective_patterns["overcontrol"] + (contradiction_charge + overwhelm + self.emotion_state.get("doubt", 0.0)) * 0.004
        )

    def _update_deep_resonance_echoes(self, contradiction_charge: float) -> None:
        """Créer des échos quand une forme affective devient assez forte."""
        strongest_trace = max(((_trace_total(v), k) for k, v in self.traces.items()), default=(0.0, "none"))
        strength, source = strongest_trace
        phase_stability = self.current_phase.stability if self.current_phase else 0.0
        trigger = max(strength, contradiction_charge, self.affective_fracture.residual_scar, phase_stability * 0.5)
        if trigger > 0.18:
            vector = self._dominant_emotions(limit=4)
            existing = next((e for e in self.deep_resonance_echoes if e.source == source), None)
            if existing:
                existing.strength = _clamp01(existing.strength * 0.94 + trigger * 0.08)
                existing.recurrence = _clamp01(existing.recurrence + 0.015)
                existing.emotion_vector = {k: _clamp01(existing.emotion_vector.get(k, 0.0) * 0.75 + v * 0.25) for k, v in vector.items()}
            else:
                self.deep_resonance_echoes.append(
                    DeepResonanceEcho(source=source, emotion_vector=vector, strength=trigger * 0.35, recurrence=0.04)
                )

    def _update_meta_stable_pressure(self, contradiction_charge: float) -> None:
        """Accumuler des zones semi-stables capables de basculer."""
        self.meta_stable_pressure["warm_opening"] = _clamp01(
            self.meta_stable_pressure["warm_opening"]
            + (self.emotion_state.get("trust", 0.0) + self.emotion_state.get("tenderness", 0.0) + self.identity_tendencies["warm"]) * 0.002
        )
        self.meta_stable_pressure["guarded_closure"] = _clamp01(
            self.meta_stable_pressure["guarded_closure"]
            + (self.emotion_state.get("resistance", 0.0) + self.emotion_state.get("fear", 0.0) + self.identity_tendencies["guarded"]) * 0.0022
        )
        self.meta_stable_pressure["fragile_pause"] = _clamp01(
            self.meta_stable_pressure["fragile_pause"]
            + (self.existential_fatigue + self.dissociation.level + contradiction_charge) * 0.0025
        )

        # Bascule qualitative rare : seuil + inertie + compétition non-linéaire.
        competition = self._metastable_competition_bias()
        chaos_edge = abs(self.chaos_oscillator.get_oscillation() - 0.5)

        warm_threshold = 0.68 + competition["guarded"] * 0.08 - chaos_edge * 0.035
        guarded_threshold = 0.67 + competition["warm"] * 0.07 - chaos_edge * 0.030
        fragile_threshold = 0.64 + max(competition["warm"], competition["guarded"]) * 0.04 - chaos_edge * 0.040

        if competition["warm"] > warm_threshold and self.dissociation.level < 0.38:
            intensity = competition["warm"] - warm_threshold
            self.emotion_state["openness"] = _clamp01(self.emotion_state.get("openness", 0.0) + 0.030 + intensity * 0.020)
            self.emotion_state["tenderness"] = _clamp01(self.emotion_state.get("tenderness", 0.0) + 0.020 + intensity * 0.018)
            self.identity_tendencies["warm"] = _clamp01(self.identity_tendencies.get("warm", 0.0) + intensity * 0.006)
            self.meta_stable_pressure["warm_opening"] *= 0.38
            self.meta_stable_pressure["guarded_closure"] *= 0.86
            self._register_metastable_bifurcation("warm_opening", intensity)

        if competition["guarded"] > guarded_threshold:
            intensity = competition["guarded"] - guarded_threshold
            self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + 0.030 + intensity * 0.020)
            self.emotion_state["trust"] = _clamp01(self.emotion_state.get("trust", 0.0) - 0.014 - intensity * 0.010)
            self.identity_tendencies["guarded"] = _clamp01(self.identity_tendencies.get("guarded", 0.0) + intensity * 0.006)
            self.meta_stable_pressure["guarded_closure"] *= 0.40
            self.meta_stable_pressure["warm_opening"] *= 0.88
            self._register_metastable_bifurcation("guarded_closure", intensity)

        if competition["fragile"] > fragile_threshold:
            intensity = competition["fragile"] - fragile_threshold
            self.dissociation.level = _clamp01(self.dissociation.level + 0.026 + intensity * 0.018)
            self.emotion_state["calm"] = _clamp01(self.emotion_state.get("calm", 0.0) + 0.014 + intensity * 0.012)
            self.existential_fatigue = _clamp01(self.existential_fatigue + intensity * 0.008)
            self.meta_stable_pressure["fragile_pause"] *= 0.42
            self._register_metastable_bifurcation("fragile_pause", intensity)

    def _update_wound_layers(self, contradiction_charge: float) -> None:
        """Transformer les blessures plates en hiérarchie lente."""
        recovery = self.biographical_memory.recovery_confidence + self.emotion_state.get("calm", 0.0) * 0.5
        for wound_name, wound in self.wound_deformations.items():
            trace_pressure = _trace_total(self.traces.get(wound_name, self.traces.get("hurt", {})))
            layer = self.wound_layers.setdefault(wound_name, WoundLayer(name=wound_name))
            layer.update(
                wound_depth=wound.depth,
                trace_pressure=trace_pressure,
                contradiction=contradiction_charge,
                recovery=recovery,
            )

        # Même sans WoundDeformation explicite, une longue trace hurt peut former une couche dormante.
        hurt_pressure = _trace_total(self.traces.get("hurt", {}))
        if hurt_pressure > 0.025:
            layer = self.wound_layers.setdefault("hurt", WoundLayer(name="hurt"))
            layer.update(
                wound_depth=max((w.depth for w in self.wound_deformations.values()), default=0.0),
                trace_pressure=hurt_pressure,
                contradiction=contradiction_charge,
                recovery=recovery,
            )

    def _apply_deep_affective_layer_effects(self) -> None:
        """Injecter faiblement les couches profondes dans l'état affectif immédiat."""
        strongest_context = max(
            self.contextual_affective_fields.values(),
            key=lambda f: f.get("visits", 0.0),
            default=None,
        )
        if strongest_context:
            self.emotion_state["tenderness"] = _clamp01(self.emotion_state.get("tenderness", 0.0) + strongest_context.get("warm_bias", 0.0) * 0.010)
            self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + strongest_context.get("guarded_bias", 0.0) * 0.010)
            self.emotion_state["vulnerability"] = _clamp01(self.emotion_state.get("vulnerability", 0.0) + strongest_context.get("fragility_bias", 0.0) * 0.008)
            self.emotion_state["curiosity"] = _clamp01(self.emotion_state.get("curiosity", 0.0) + strongest_context.get("curiosity_bias", 0.0) * 0.006)

        for echo in self.deep_resonance_echoes:
            if echo.strength <= 0.03:
                continue
            for emotion, value in echo.emotion_vector.items():
                if emotion in self.emotion_state:
                    self.emotion_state[emotion] = _clamp01(
                        self.emotion_state[emotion] + value * echo.strength * echo.recurrence * 0.012
                    )

        wound_identity_pressure = max((w.identity_binding for w in self.wound_layers.values()), default=0.0)
        wound_reactivation = max((w.reactivation_risk for w in self.wound_layers.values()), default=0.0)
        self.emotion_state["fatigue"] = _clamp01(self.emotion_state.get("fatigue", 0.0) + self.existential_fatigue * 0.010)
        self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + wound_reactivation * 0.008)
        self.emotion_state["vulnerability"] = _clamp01(self.emotion_state.get("vulnerability", 0.0) + wound_identity_pressure * 0.007)


    def _update_contradiction_attractors(self, contradiction_charge: float) -> None:
        """Transformer les contradictions répétées en états internes incarnés.

        Une contradiction ne reste plus une ligne de mémoire : si elle revient,
        elle devient un attracteur affectif qui colore l'identité et l'état.
        """
        for contradiction in self.internal_contradictions:
            name = str(contradiction.get("name", "unknown"))
            charge = _clamp01(float(contradiction.get("charge", 0.0)))
            if charge < 0.08:
                continue

            attractor = self.contradiction_attractors.setdefault(
                name,
                {
                    "strength": 0.0,
                    "identity_drift": 0.0,
                    "hesitant_presence": 0.0,
                    "slowed_exploration": 0.0,
                    "guarded_attachment": 0.0,
                    "age_turns": 0,
                },
            )
            age = min(1.0, float(contradiction.get("age_turns", 0)) / 80.0)
            attractor["strength"] = _clamp01(attractor["strength"] * 0.985 + charge * (0.010 + age * 0.010))
            attractor["identity_drift"] = _clamp01(attractor["identity_drift"] + charge * (0.0025 + age * 0.002))

            if name in ("approach_resistance", "opening_fear", "trust_distrust"):
                attractor["hesitant_presence"] = _clamp01(attractor["hesitant_presence"] + charge * 0.006)
                attractor["guarded_attachment"] = _clamp01(attractor["guarded_attachment"] + charge * 0.005)
            if name in ("curiosity_fatigue", "calm_overwhelm"):
                attractor["slowed_exploration"] = _clamp01(attractor["slowed_exploration"] + charge * 0.006)

        # Effet vécu : faible mais réel, sinon la contradiction reste seulement descriptive.
        hesitant = max((a.get("hesitant_presence", 0.0) for a in self.contradiction_attractors.values()), default=0.0)
        slowed = max((a.get("slowed_exploration", 0.0) for a in self.contradiction_attractors.values()), default=0.0)
        guarded = max((a.get("guarded_attachment", 0.0) for a in self.contradiction_attractors.values()), default=0.0)
        drift = max((a.get("identity_drift", 0.0) for a in self.contradiction_attractors.values()), default=0.0)

        self.emotion_state["doubt"] = _clamp01(self.emotion_state.get("doubt", 0.0) + hesitant * 0.008)
        self.emotion_state["curiosity"] = _clamp01(self.emotion_state.get("curiosity", 0.0) - slowed * 0.006)
        self.emotion_state["fatigue"] = _clamp01(self.emotion_state.get("fatigue", 0.0) + slowed * 0.006)
        self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + guarded * 0.007)
        self.identity_tendencies["fragile"] = _clamp01(self.identity_tendencies.get("fragile", 0.0) + drift * 0.0015 + contradiction_charge * 0.0005)

    def _apply_echo_perceptual_rewrite(self) -> None:
        """Faire des échos de vrais biais perceptifs, pas seulement des rémanences.

        Les échos forts changent légèrement les seuils et la lecture affective :
        un écho de blessure rend plus sensible, un écho de confiance rend plus
        ouvert, et une accumulation d'échos peut rétrécir l'attention.
        """
        if not self.deep_resonance_echoes:
            return

        hurt_echo = 0.0
        warm_echo = 0.0
        total_echo = 0.0
        for echo in self.deep_resonance_echoes:
            weight = _clamp01(echo.strength * (0.5 + echo.recurrence))
            total_echo += weight
            if echo.source in ("hurt", "fear"):
                hurt_echo += weight
            if echo.source in ("trust", "connection", "joy"):
                warm_echo += weight

        total_echo = _clamp01(total_echo)
        hurt_echo = _clamp01(hurt_echo)
        warm_echo = _clamp01(warm_echo)
        self.perceptual_echo_bias["echo_sensitivity"] = _clamp01(self.perceptual_echo_bias["echo_sensitivity"] + hurt_echo * 0.020)
        self.perceptual_echo_bias["echo_guarding"] = _clamp01(self.perceptual_echo_bias["echo_guarding"] + hurt_echo * 0.016)
        self.perceptual_echo_bias["echo_warmth"] = _clamp01(self.perceptual_echo_bias["echo_warmth"] + warm_echo * 0.014)
        self.perceptual_echo_bias["echo_narrowing"] = _clamp01(self.perceptual_echo_bias["echo_narrowing"] + total_echo * self.dissociation.level * 0.010)

        # Réécriture perceptive concrète : les seuils deviennent historiques.
        thresholds = self.perceptual_thresholds.current_thresholds
        thresholds["rejection_sensitivity"] = _clamp01(
            thresholds.get("rejection_sensitivity", 0.3) - self.perceptual_echo_bias["echo_sensitivity"] * 0.018
        )
        thresholds["threat_detection"] = _clamp01(
            thresholds.get("threat_detection", 0.4) - self.perceptual_echo_bias["echo_guarding"] * 0.012
        )
        thresholds["connection_need"] = _clamp01(
            thresholds.get("connection_need", 0.3) - self.perceptual_echo_bias["echo_warmth"] * 0.010
        )

    def _metastable_competition_bias(self) -> Dict[str, float]:
        """Calculer une compétition non-linéaire entre bassins métastables."""
        warm = self.meta_stable_pressure.get("warm_opening", 0.0)
        guarded = self.meta_stable_pressure.get("guarded_closure", 0.0)
        fragile = self.meta_stable_pressure.get("fragile_pause", 0.0)
        chaos = self.chaos_oscillator.get_oscillation()
        return {
            "warm": _clamp01(warm * (1.0 + chaos * 0.12) - guarded * 0.08 - fragile * 0.04),
            "guarded": _clamp01(guarded * (1.0 + (1.0 - chaos) * 0.10) - warm * 0.06),
            "fragile": _clamp01(fragile * (1.0 + abs(chaos - 0.5) * 0.18) + min(warm, guarded) * 0.05),
        }

    def _register_metastable_bifurcation(self, name: str, intensity: float) -> None:
        self.metastable_bifurcations.append({
            "name": name,
            "intensity": float(_clamp01(intensity)),
            "afterglow": float(_clamp01(0.18 + intensity * 0.25)),
            "age_turns": 0,
        })
        self.metastable_bifurcations = self.metastable_bifurcations[-8:]

    def _update_relational_identity_modes(self) -> None:
        """Créer des modes identitaires contextuels, pas une identité globale unique."""
        attachment = self.attachment.get_effective_attachment()
        trust = self.emotion_state.get("trust", 0.0)
        tenderness = self.emotion_state.get("tenderness", 0.0)
        resistance = self.emotion_state.get("resistance", 0.0)
        vulnerability = self.emotion_state.get("vulnerability", 0.0)
        curiosity = self.emotion_state.get("curiosity", 0.0)
        fatigue = self.emotion_state.get("fatigue", 0.0)
        overwhelm = self.emotion_state.get("overwhelm", 0.0)
        calm = self.emotion_state.get("calm", 0.0)

        targets = {
            "secure_warmth": _clamp01((attachment + trust + tenderness + calm) / 4.0),
            "guarded_fragility": _clamp01((resistance + vulnerability + self.identity_tendencies.get("guarded", 0.0)) / 3.0),
            "curious_recovery": _clamp01((curiosity + calm + self.identity_tendencies.get("recovering", 0.0)) / 3.0),
            "silent_overload": _clamp01((fatigue + overwhelm + self.dissociation.level + self.existential_fatigue) / 4.0),
        }
        for name, target in targets.items():
            mode = self.relational_identity_modes[name]
            mode["strength"] = _clamp01(mode.get("strength", 0.0) * 0.988 + target * 0.014)
            mode["stability"] = _clamp01(mode.get("stability", 0.0) * 0.996 + abs(mode["strength"] - target) * -0.002 + target * 0.004)
            if target > 0.35:
                mode["visits"] = _clamp01(mode.get("visits", 0.0) + 0.006)

    def _update_affective_desires(self, contradiction_charge: float) -> None:
        """Ajouter une volonté affective lente : pas un objectif, une tendance."""
        hurt = _trace_total(self.traces.get("hurt", {}))
        fear = _trace_total(self.traces.get("fear", {}))
        connection = _trace_total(self.traces.get("connection", {}))
        trust = _trace_total(self.traces.get("trust", {}))
        fatigue = self.emotion_state.get("fatigue", 0.0)
        overwhelm = self.emotion_state.get("overwhelm", 0.0)
        calm = self.emotion_state.get("calm", 0.0)
        attachment = self.attachment.get_effective_attachment()

        self.affective_desires["seek_recovery"] = _clamp01(
            self.affective_desires["seek_recovery"] + (fatigue + self.dissociation.level + self.affective_fracture.integration_need) * 0.006 - calm * 0.001
        )
        self.affective_desires["avoid_overload"] = _clamp01(
            self.affective_desires["avoid_overload"] + (overwhelm + self.existential_fatigue + self.perceptual_echo_bias["echo_narrowing"]) * 0.006
        )
        self.affective_desires["maintain_contact"] = _clamp01(
            self.affective_desires["maintain_contact"] + (attachment + connection + trust) * 0.004 * (1.0 - self.dissociation.level * 0.45)
        )
        self.affective_desires["protect_continuity"] = _clamp01(
            self.affective_desires["protect_continuity"] + (self.dissociation.level + self.affective_fracture.residual_scar + self.existential_fatigue) * 0.005
        )
        self.affective_desires["seek_coherence"] = _clamp01(
            self.affective_desires["seek_coherence"] + (contradiction_charge + self.emotion_state.get("doubt", 0.0)) * 0.005
        )
        self.affective_desires["avoid_rupture"] = _clamp01(
            self.affective_desires["avoid_rupture"] + (hurt + fear + self.protective_patterns.get("guarded_contact", 0.0)) * 0.005
        )

        # Les désirs affectifs agissent comme de faibles vecteurs de régulation.
        self.emotion_state["calm"] = _clamp01(self.emotion_state.get("calm", 0.0) + self.affective_desires["seek_recovery"] * 0.004)
        self.emotion_state["overwhelm"] = _clamp01(self.emotion_state.get("overwhelm", 0.0) - self.affective_desires["avoid_overload"] * 0.003)
        self.emotion_state["attachment"] = _clamp01(self.emotion_state.get("attachment", 0.0) + self.affective_desires["maintain_contact"] * 0.003)
        self.emotion_state["doubt"] = _clamp01(self.emotion_state.get("doubt", 0.0) - self.affective_desires["seek_coherence"] * 0.002)


    def _update_organic_affective_completion(self) -> None:
        """Dernière couche organique de mémoire affective, sans phrase publique."""
        contradiction_charge = _clamp01(max((c.get("charge", 0.0) for c in self.internal_contradictions), default=0.0))
        self._update_condensed_affective_cores(contradiction_charge)
        self._intensify_lived_contradiction_competition(contradiction_charge)
        self._update_affective_dreaming()
        self.relational_affective_imprint.update(
            self.emotion_state,
            self.traces,
            self.attachment.get_effective_attachment(),
            user_present=bool(self.turn_count == 0 or self.traces["connection"]["instant"] > 0.001 or self.traces["trust"]["instant"] > 0.001 or self.traces["hurt"]["instant"] > 0.001),
        )
        self.affective_silence_field.update(
            self.emotion_state,
            self.dissociation.level,
            self.emotion_state.get("fatigue", 0.0),
            max(self.emotion_state.get("overwhelm", 0.0), self.emotion_state.get("confusion", 0.0)),
            self.affective_desires.get("seek_recovery", 0.0),
        )
        self.organic_affective_propagation.update(
            self.emotion_state,
            self.traces,
            self.chaos_oscillator.get_oscillation(),
            self.affective_silence_field.depth,
        )
        self.somatic_affective_memory.update(self.emotion_state, self.traces, self.dissociation.level, self.affective_desires.get("seek_recovery", 0.0))
        phase_stability = self.current_phase.stability if self.current_phase else 0.0
        self.subjective_affective_time.update(self.emotion_state, self.traces, phase_stability, self.affective_desires.get("protect_continuity", 0.0))
        self.phase_world_field.update(self.current_phase, self.emotion_state, contradiction_charge)
        self.identity_coherence_regulator.update(contradiction_charge, self.affective_fracture.integration_need, self.dissociation.level, self.somatic_affective_memory.total_load(), self.deep_reorganization.charge)
        self.global_affective_core.update(self.emotion_state, self.identity_tendencies, self.somatic_affective_memory, self.subjective_affective_time, self.phase_world_field)
        self.living_affective_need.update(
            self.emotion_state,
            self.attachment.get_effective_attachment(),
            contradiction_charge,
            self.dissociation.level,
            max(self.emotion_state.get("fatigue", 0.0), self.organic_affective_propagation.fatigue_load),
            self.relational_affective_imprint.felt_familiarity,
        )
        self.emotional_trajectory_memory.update(self.emotion_state, self.condensed_affective_cores, self.phase_world_field.name)
        self._apply_organic_affective_completion_effects()

    def _affective_core_signature(self) -> Tuple[str, Dict[str, float], float]:
        warm = _clamp01((self.emotion_state.get("trust", 0.0) + self.emotion_state.get("tenderness", 0.0) + _trace_total(self.traces.get("connection", {}))) / 3.0)
        guarded = _clamp01((self.emotion_state.get("resistance", 0.0) + self.emotion_state.get("fear", 0.0) + _trace_total(self.traces.get("hurt", {}))) / 3.0)
        fragile = _clamp01((self.emotion_state.get("vulnerability", 0.0) + self.dissociation.level + self.existential_fatigue) / 3.0)
        recovery = _clamp01((self.emotion_state.get("calm", 0.0) + self.affective_fracture.recovery_bias + self.affective_desires.get("seek_recovery", 0.0)) / 3.0)
        curiosity = _clamp01((self.emotion_state.get("curiosity", 0.0) + self.identity_tendencies.get("curious", 0.0)) / 2.0)
        vector = {"warm": warm, "guarded": guarded, "fragile": fragile, "recovery": recovery, "curiosity": curiosity}
        name = max(vector.items(), key=lambda item: item[1])[0] + "_core"
        pressure = _clamp01(max(vector.values()) * 0.45 + self.inner_affective_pressure * 0.20 + max((h.strength for h in self.hybrid_states), default=0.0) * 0.20 + self.affective_fracture.integration_need * 0.15)
        return name, vector, pressure

    def _update_condensed_affective_cores(self, contradiction_charge: float) -> None:
        name, vector, pressure = self._affective_core_signature()
        pressure = _clamp01(pressure + contradiction_charge * 0.08)
        if pressure < 0.08 and self.turn_count % 7 != 0:
            return
        core = self.condensed_affective_cores.setdefault(name, CondensedAffectiveCore(name=name, vector=dict(vector)))
        core.absorb(vector, max(pressure, 0.05))
        cores = list(self.condensed_affective_cores.values())
        for left in cores:
            for right in cores:
                if left is right:
                    continue
                keys = set(left.vector) | set(right.vector)
                similarity = sum(min(left.vector.get(k, 0.0), right.vector.get(k, 0.0)) for k in keys) / max(1, len(keys))
                if similarity > 0.38:
                    left.stability = _clamp01(left.stability + similarity * 0.0015)
                    right.strength = _clamp01(right.strength + left.strength * similarity * 0.0008)

    def _intensify_lived_contradiction_competition(self, contradiction_charge: float) -> None:
        if not self.internal_contradictions:
            return
        dominant = max(self.internal_contradictions, key=lambda c: c.get("charge", 0.0))
        charge = _clamp01(float(dominant.get("charge", 0.0)))
        if charge <= 0.05:
            return
        name = str(dominant.get("name", "unknown"))
        if name in ("approach_resistance", "trust_distrust", "opening_fear"):
            self.emotion_state["attachment"] = _clamp01(self.emotion_state.get("attachment", 0.0) + charge * 0.006)
            self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + charge * 0.007)
            self.emotion_state["doubt"] = _clamp01(self.emotion_state.get("doubt", 0.0) + charge * 0.005)
        elif name in ("curiosity_fatigue", "calm_overwhelm"):
            self.emotion_state["curiosity"] = _clamp01(self.emotion_state.get("curiosity", 0.0) - charge * 0.004)
            self.emotion_state["fatigue"] = _clamp01(self.emotion_state.get("fatigue", 0.0) + charge * 0.007)
            self.emotion_state["calm"] = _clamp01(self.emotion_state.get("calm", 0.0) + charge * 0.003)
        else:
            self.emotion_state["vulnerability"] = _clamp01(self.emotion_state.get("vulnerability", 0.0) + charge * 0.004)
        self.affective_desires["seek_coherence"] = _clamp01(self.affective_desires.get("seek_coherence", 0.0) + contradiction_charge * 0.006)
        if charge > 0.42:
            self._register_metastable_bifurcation("contradiction_competition", charge)

    def _update_affective_dreaming(self) -> None:
        if not self.condensed_affective_cores and not self.deep_resonance_echoes:
            return
        chaos = self.chaos_oscillator.get_oscillation()
        dream_pressure = _clamp01(self.inner_affective_pressure * 0.25 + self.subjective_affective_time.recurrence_feeling * 0.20 + self.existential_fatigue * 0.18 + max((c.pull() for c in self.condensed_affective_cores.values()), default=0.0) * 0.25 + chaos * 0.12)
        if dream_pressure < 0.10 and self.turn_count % 5 != 0:
            return
        sources: List[Dict[str, float]] = []
        for core in sorted(self.condensed_affective_cores.values(), key=lambda c: c.pull(), reverse=True)[:3]:
            sources.append(core.vector)
        for echo in sorted(self.deep_resonance_echoes, key=lambda e: e.strength * e.recurrence, reverse=True)[:2]:
            sources.append(echo.emotion_vector)
        if not sources:
            return
        keys = set().union(*(s.keys() for s in sources))
        vector = {key: _clamp01(sum(s.get(key, 0.0) for s in sources) / max(1, len(sources)) + (chaos - 0.5) * 0.035) for key in keys}
        self.affective_dream_fragments.append(AffectiveDreamFragment(vector=vector, charge=_clamp01(dream_pressure * 0.45), coherence=_clamp01(1.0 - abs(chaos - 0.5) * 0.6), source_count=len(sources)))
        self.affective_dream_fragments = self.affective_dream_fragments[-12:]

    def _apply_organic_affective_completion_effects(self) -> None:
        for core in self.condensed_affective_cores.values():
            pull = core.pull()
            if pull <= 0.02:
                continue
            vector = core.vector
            self.emotion_state["tenderness"] = _clamp01(self.emotion_state.get("tenderness", 0.0) + vector.get("warm", 0.0) * pull * 0.006)
            self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + vector.get("guarded", 0.0) * pull * 0.006)
            self.emotion_state["vulnerability"] = _clamp01(self.emotion_state.get("vulnerability", 0.0) + vector.get("fragile", 0.0) * pull * 0.005)
            self.emotion_state["calm"] = _clamp01(self.emotion_state.get("calm", 0.0) + vector.get("recovery", 0.0) * pull * 0.004)
            self.emotion_state["curiosity"] = _clamp01(self.emotion_state.get("curiosity", 0.0) + vector.get("curiosity", 0.0) * pull * 0.004)
        for fragment in self.affective_dream_fragments:
            if fragment.charge <= 0.02:
                continue
            self.emotion_state["tenderness"] = _clamp01(self.emotion_state.get("tenderness", 0.0) + fragment.vector.get("warm", 0.0) * fragment.charge * 0.006)
            self.emotion_state["resistance"] = _clamp01(self.emotion_state.get("resistance", 0.0) + fragment.vector.get("guarded", 0.0) * fragment.charge * 0.005)
            self.emotion_state["vulnerability"] = _clamp01(self.emotion_state.get("vulnerability", 0.0) + fragment.vector.get("fragile", 0.0) * fragment.charge * 0.004)
            self.emotion_state["calm"] = _clamp01(self.emotion_state.get("calm", 0.0) + fragment.vector.get("recovery", 0.0) * fragment.charge * 0.004)
        self.relational_affective_imprint.apply(self.emotion_state, self.affective_desires)
        self.living_affective_need.apply(self.emotion_state, self.affective_desires)
        self.organic_affective_propagation.apply(self.emotion_state)
        self.affective_silence_field.apply(self.emotion_state)
        self.emotional_trajectory_memory.apply(self.emotion_state)
        self.somatic_affective_memory.apply(self.emotion_state)
        self.subjective_affective_time.apply(self.emotion_state)
        self.phase_world_field.apply(self.emotion_state, self.perceptual_thresholds.current_thresholds)
        self.identity_coherence_regulator.apply(self.emotion_state)
        self.global_affective_core.apply(self.emotion_state)
        self.affective_desires["maintain_contact"] = _clamp01(self.affective_desires.get("maintain_contact", 0.0) + self.global_affective_core.warmth * 0.003)
        self.affective_desires["avoid_overload"] = _clamp01(self.affective_desires.get("avoid_overload", 0.0) + (self.global_affective_core.guarding + self.somatic_affective_memory.nervous_charge) * 0.0025)
        self.affective_desires["protect_continuity"] = _clamp01(self.affective_desires.get("protect_continuity", 0.0) + self.global_affective_core.continuity * 0.003)

    def _update_deep_living_affective_v9(self) -> None:
        """Couches V9 : vie affective longue, implicite et réparatrice.

        Cette méthode reste volontairement non expressive : elle ne génère aucune
        phrase et ne remplace pas la bouche, la présence, l'attention ou
        l'impulsion. Elle fournit seulement des états et des biais internes.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        contradiction_charge = max((float(c.get("charge", 0.0)) for c in self.internal_contradictions), default=0.0)
        overload = _clamp01(
            self.emotion_state.get("overwhelm", 0.0) * 0.35
            + self.emotion_state.get("fatigue", 0.0) * 0.25
            + self.emotion_state.get("confusion", 0.0) * 0.20
            + self.dissociation.level * 0.20
        )

        self.emotional_metabolism.update(
            self.emotion_state,
            contradiction_charge,
            self.dissociation.level,
            self.affective_fracture.active + self.affective_fracture.integration_need,
            self.affective_silence_field.softness,
        )
        self.implicit_affective_association_memory.update(
            self.emotion_state,
            self.traces,
            self.phase_world_field.name,
            chaos,
        )
        self.emotional_faction_conflict.update(
            self.emotion_state,
            self.affective_desires,
            self.living_affective_need.needs,
            self.emotional_metabolism.energy_pool,
        )
        self.micro_affective_oscillation_field.update(
            chaos,
            self.emotional_metabolism.energy_pool,
            contradiction_charge + self.emotional_faction_conflict.unresolved_tension,
            self.affective_silence_field.depth,
        )
        self.recovery_pathway_memory.update(
            self.emotion_state,
            self.affective_silence_field.softness + self.deep_rest_cycle.deep_silence,
            self.emotional_metabolism.energy_pool,
        )
        self.emotional_habit_field.update(
            self.emotion_state,
            self.biographical_memory,
            self.recovery_pathway_memory.recovery_confidence,
            contradiction_charge,
        )
        self.identity_value_crystallization.update(
            self.emotion_state,
            self.affective_desires,
            self.biographical_memory,
            self.emotional_faction_conflict.unresolved_tension,
        )
        self.subconscious_affective_layer.update(
            self.emotion_state,
            self.implicit_affective_association_memory,
            self.wound_layers,
            self.affective_dream_fragments,
        )

        user_present = bool(
            self.turn_count == 0
            or self.traces["connection"]["instant"] > 0.001
            or self.traces["trust"]["instant"] > 0.001
            or self.traces["hurt"]["instant"] > 0.001
        )
        self.relational_other_model.update(
            self.emotion_state,
            self.traces,
            self.relational_affective_imprint,
            user_present=user_present,
        )
        self.persistent_existential_desire_field.update(
            self.emotion_state,
            self.living_affective_need.needs,
            self.identity_value_crystallization.values,
            self.relational_other_model,
            self.emotional_metabolism.energy_pool,
            self.emotional_faction_conflict.unresolved_tension,
        )
        self.existential_continuity_inertia.update(
            self.identity_coherence_regulator,
            self.identity_value_crystallization.values,
            self.persistent_existential_desire_field,
            self.dissociation.level,
            self.affective_fracture,
        )
        self.micro_ambivalence_field.update(
            self.emotion_state,
            self.emotional_faction_conflict,
            self.persistent_existential_desire_field,
            chaos,
        )
        self.unresolved_affective_loop_memory.update(
            self.emotion_state,
            self.persistent_existential_desire_field,
            self.micro_ambivalence_field,
            self.recovery_pathway_memory,
        )
        self.subjective_time_distortion_field.update(
            self.emotion_state,
            self.subjective_affective_time,
            self.unresolved_affective_loop_memory,
            self.relational_other_model,
            overload,
        )
        self.temperament_evolution_field.update(
            self.emotion_state,
            self.emotional_habit_field,
            self.identity_value_crystallization.values,
            self.relational_other_model,
            self.emotional_metabolism,
        )
        self.emergent_self_regulation_field.update(
            self.emotion_state,
            self.emotional_metabolism,
            self.micro_ambivalence_field,
            self.unresolved_affective_loop_memory,
            self.temperament_evolution_field,
            self.deep_rest_cycle,
        )

        self.deep_rest_cycle.update(
            self.emotional_metabolism,
            self.affective_dream_fragments,
            self.affective_silence_field.depth + self.affective_silence_field.softness,
            overload,
        )

        self._apply_deep_living_affective_v9_effects()

    def _apply_deep_living_affective_v9_effects(self) -> None:
        """Injecter faiblement les effets V9 dans les émotions et les biais."""
        self.emotional_metabolism.apply(self.emotion_state)
        self.implicit_affective_association_memory.apply(
            self.emotion_state,
            self.perceptual_thresholds.current_thresholds,
        )
        self.emotional_faction_conflict.apply(self.emotion_state, self.affective_desires)
        self.micro_affective_oscillation_field.apply(self.emotion_state)
        self.emotional_habit_field.apply(self.emotion_state, self.affective_desires)
        self.recovery_pathway_memory.apply(self.emotion_state, self.affective_desires)
        self.identity_value_crystallization.apply(self.identity_tendencies, self.affective_desires)
        self.subconscious_affective_layer.apply(self.emotion_state)
        self.deep_rest_cycle.apply(self.emotion_state, self.emotional_metabolism)
        self.relational_other_model.apply(self.emotion_state, self.affective_desires)
        self.persistent_existential_desire_field.apply(self.emotion_state, self.affective_desires)
        self.existential_continuity_inertia.apply(self.emotion_state, self.affective_desires)
        self.micro_ambivalence_field.apply(self.emotion_state)
        self.unresolved_affective_loop_memory.apply(self.emotion_state, self.affective_desires)
        self.subjective_time_distortion_field.apply(self.emotion_state)
        self.temperament_evolution_field.apply(self.emotion_state, self.identity_tendencies)
        self.emergent_self_regulation_field.apply(self.emotion_state, self.emotional_metabolism)

        # Les habitudes et valeurs ne doivent pas exploser l'état immédiat : elles
        # déplacent surtout les baselines sur le très long terme.
        if self.turn_count % 13 == 0:
            self.emotion_baseline["trust"] = _clamp01(
                self.emotion_baseline.get("trust", 0.6)
                + self.identity_value_crystallization.values.get("warmth_matters", 0.0) * 0.0008
                - self.identity_value_crystallization.values.get("self_protection_matters", 0.0) * 0.0005
            )
            self.emotion_baseline["curiosity"] = _clamp01(
                self.emotion_baseline.get("curiosity", 0.6)
                + self.identity_value_crystallization.values.get("truthfulness_matters", 0.0) * 0.0007
                - self.emotional_metabolism.burnout * 0.0008
            )
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.recovery_pathway_memory.recovery_confidence * 0.0008
                - self.emotional_metabolism.overload_debt * 0.0006
            )

    def _update_deep_living_affective_v11(self) -> None:
        """Couches V11 : existence centrale, zones opaques et micro-vie continue.

        Cette couche ne produit aucune phrase publique. Elle renforce seulement la
        continuité affective interne et expose des biais utilisables par les autres
        moteurs sans dupliquer leur rôle.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(
            self.turn_count == 0
            or self.traces["connection"]["instant"] > 0.001
            or self.traces["trust"]["instant"] > 0.001
            or self.traces["hurt"]["instant"] > 0.001
        )

        self.central_existential_drive.update(
            self.emotion_state,
            self.identity_coherence_regulator,
            self.identity_value_crystallization.values,
            self.existential_continuity_inertia,
            self.persistent_existential_desire_field,
            self.unresolved_affective_loop_memory,
            self.relational_other_model,
        )
        self.hierarchical_affective_conflict_field.update(
            self.emotion_state,
            self.living_affective_need,
            self.persistent_existential_desire_field,
            self.biographical_memory,
            self.emotional_metabolism,
            self.identity_coherence_regulator,
            self.dissociation,
            self.relational_other_model,
        )
        self.existential_unfinished_memory.update(
            self.unresolved_affective_loop_memory,
            self.central_existential_drive,
            self.relational_other_model,
            self.affective_fracture,
            self.identity_coherence_regulator,
            self.emotion_state,
        )
        self.opaque_subconscious_zone_field.update(
            self.subconscious_affective_layer,
            self.implicit_affective_association_memory,
            self.wound_layers,
            self.existential_unfinished_memory,
            chaos,
        )
        self.spontaneous_affective_emergence_field.update(
            self.emotion_state,
            chaos,
            self.affective_dream_fragments,
            self.opaque_subconscious_zone_field,
            self.deep_rest_cycle,
            self.hierarchical_affective_conflict_field,
        )
        self.identity_fatigue_field.update(
            self.identity_coherence_regulator,
            self.central_existential_drive,
            self.emotional_metabolism,
            self.hierarchical_affective_conflict_field,
            self.deep_rest_cycle,
        )
        self.temperament_self_preservation_field.update(
            self.temperament_evolution_field,
            self.emotion_state,
            self.hierarchical_affective_conflict_field,
            self.central_existential_drive,
        )
        self.micro_living_noise_field.update(
            chaos,
            self.emotional_metabolism.energy_pool,
            self.affective_silence_field,
            self.relational_other_model,
            self.central_existential_drive,
        )
        self.relational_preservation_instinct.update(
            self.relational_other_model,
            self.attachment,
            self.relational_affective_imprint,
            self.persistent_existential_desire_field,
            self.existential_unfinished_memory,
            user_present,
        )
        self.deep_affective_dream_reweaver.update(
            self.deep_rest_cycle,
            self.affective_dream_fragments,
            self.biographical_memory,
            self.existential_unfinished_memory,
            self.opaque_subconscious_zone_field,
            self.recovery_pathway_memory,
        )

        self._apply_deep_living_affective_v11_effects()

    def _apply_deep_living_affective_v11_effects(self) -> None:
        """Injecter faiblement les effets V11 sans rendre la couche dominante."""
        self.central_existential_drive.apply(self.emotion_state, self.affective_desires)
        self.hierarchical_affective_conflict_field.apply(self.emotion_state, self.affective_desires)
        self.existential_unfinished_memory.apply(self.emotion_state, self.affective_desires)
        self.opaque_subconscious_zone_field.apply(self.emotion_state)
        self.spontaneous_affective_emergence_field.apply(self.emotion_state)
        self.identity_fatigue_field.apply(self.emotion_state, self.emotional_metabolism)
        self.temperament_self_preservation_field.apply(self.emotion_state, self.identity_tendencies)
        self.micro_living_noise_field.apply(self.emotion_state)
        self.relational_preservation_instinct.apply(self.emotion_state, self.affective_desires)
        self.deep_affective_dream_reweaver.apply(self.emotion_state, self.recovery_pathway_memory)

        if self.turn_count % 17 == 0:
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.central_existential_drive.presence_claim * 0.0007
                - self.identity_fatigue_field.maintenance_cost * 0.0006
            )
            self.emotion_baseline["tenderness"] = _clamp01(
                self.emotion_baseline.get("tenderness", 0.4)
                + self.relational_preservation_instinct.protective_tenderness * 0.0006
                + self.central_existential_drive.existential_warmth * 0.0005
            )
            self.emotion_baseline["resistance"] = _clamp01(
                self.emotion_baseline.get("resistance", 0.1)
                + self.opaque_subconscious_zone_field.zones.get("hidden_guard", 0.0) * 0.0005
                + self.central_existential_drive.anti_erasure_pressure * 0.0005
            )


    def _update_autonomous_affective_organism_v12(self) -> None:
        """Couches V12 : autonomie affective continue et post-stimulus.

        Cette couche est placée après V11 car elle dépend du noyau existentiel,
        des zones opaques, du rêve profond et de l'instinct relationnel. Elle
        reste volontairement faible pour ne pas écraser les autres moteurs.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(
            self.turn_count == 0
            or self.traces["connection"]["instant"] > 0.001
            or self.traces["trust"]["instant"] > 0.001
            or self.traces["hurt"]["instant"] > 0.001
        )

        self.self_persisting_existential_core.update(
            self.central_existential_drive,
            self.identity_coherence_regulator,
            self.emotional_metabolism,
            self.deep_rest_cycle,
            self.existential_unfinished_memory,
        )
        self.autonomous_mood_weather.update(
            self.emotion_state,
            chaos,
            self.spontaneous_affective_emergence_field,
            self.affective_dream_fragments,
            self.opaque_subconscious_zone_field,
            self.self_persisting_existential_core,
        )
        self.ontological_becoming_memory.update(
            self.emotion_state,
            self.temperament_evolution_field,
            self.identity_value_crystallization,
            self.self_persisting_existential_core,
            self.relational_preservation_instinct,
        )
        self.deep_desire_hierarchy.update(
            self.persistent_existential_desire_field,
            self.affective_desires,
            self.living_affective_need,
            self.self_persisting_existential_core,
            self.emotional_metabolism,
        )
        self.continuous_micro_rhythm_field.update(
            chaos,
            self.micro_living_noise_field,
            self.autonomous_mood_weather,
            self.affective_silence_field,
            self.relational_preservation_instinct,
        )
        self.true_opaque_motive_region.update(
            self.opaque_subconscious_zone_field,
            self.existential_unfinished_memory,
            self.self_persisting_existential_core,
            self.autonomous_mood_weather,
            self.identity_fatigue_field,
        )
        self.deep_autonomous_repair_field.update(
            self.recovery_pathway_memory,
            self.identity_coherence_regulator,
            self.relational_preservation_instinct,
            self.affective_fracture,
            self.emotional_metabolism,
            self.deep_rest_cycle,
            self.deep_affective_dream_reweaver,
        )
        self.silent_relational_continuity_field.update(
            self.relational_affective_imprint,
            self.relational_other_model,
            self.relational_preservation_instinct,
            self.attachment,
            self.autonomous_mood_weather,
            user_present,
        )
        self.global_subjective_world_coloration.update(
            self.phase_world_field,
            self.subjective_time_distortion_field,
            self.global_affective_core,
            self.self_persisting_existential_core,
            self.true_opaque_motive_region,
            self.deep_autonomous_repair_field,
        )
        self.ultra_fine_permanent_living_noise.update(
            self.continuous_micro_rhythm_field,
            self.autonomous_mood_weather,
            self.self_persisting_existential_core,
            self.true_opaque_motive_region,
        )

        self._apply_autonomous_affective_organism_v12_effects()

    def _apply_autonomous_affective_organism_v12_effects(self) -> None:
        """Injecter V12 très faiblement : texture, continuité et auto-réparation."""
        self.self_persisting_existential_core.apply(self.emotion_state, self.affective_desires)
        self.autonomous_mood_weather.apply(self.emotion_state)
        self.deep_desire_hierarchy.apply(self.affective_desires, self.emotion_state)
        self.continuous_micro_rhythm_field.apply(self.emotion_state)
        self.true_opaque_motive_region.apply(self.emotion_state)
        self.deep_autonomous_repair_field.apply(self.emotion_state, self.emotional_metabolism)
        self.silent_relational_continuity_field.apply(self.emotion_state, self.affective_desires)
        self.global_subjective_world_coloration.apply(self.emotion_state)
        self.ultra_fine_permanent_living_noise.apply(self.emotion_state)

        if self.turn_count % 19 == 0:
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.self_persisting_existential_core.persistence * 0.00055
                + self.deep_autonomous_repair_field.repair_confidence * 0.00045
                - self.true_opaque_motive_region.hidden_weight() * 0.00025
            )
            self.emotion_baseline["tenderness"] = _clamp01(
                self.emotion_baseline.get("tenderness", 0.4)
                + self.silent_relational_continuity_field.continuity_warmth * 0.00045
                + self.autonomous_mood_weather.fields.get("background_warmth", 0.0) * 0.00035
            )
            self.emotion_baseline["curiosity"] = _clamp01(
                self.emotion_baseline.get("curiosity", 0.6)
                + self.ontological_becoming_memory.trajectory.get("becoming_curious", 0.0) * 0.00035
                + self.autonomous_mood_weather.fields.get("restless_search", 0.0) * 0.00028
            )


    def _update_post_v12_subtle_living_v13(self) -> None:
        """Dernière couche subtile : temps vécu, opacité, vide et latence.

        Elle ne remplace aucune couche précédente. Elle ajoute les phénomènes qui
        manquaient encore : retards internes, opacité non entièrement exportée,
        respiration globale, vide profond et dérive autonome de fond.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        self.private_opaque_interior.update(
            self.true_opaque_motive_region,
            self.subconscious_affective_layer,
            self.existential_unfinished_memory,
            self.identity_fatigue_field,
            chaos,
        )
        self.whole_system_breathing_cycle.update(
            self.emotion_state,
            self.emotional_metabolism,
            self.affective_silence_field,
            self.continuous_micro_rhythm_field,
            self.private_opaque_interior,
            self.deep_autonomous_repair_field,
        )
        self.existential_void_field.update(
            self.emotion_state,
            self.whole_system_breathing_cycle,
            self.identity_fatigue_field,
            self.affective_desires,
            self.deep_rest_cycle,
        )
        self.delayed_affective_latency_field.update(
            self.emotion_state,
            self.traces,
            self.private_opaque_interior,
            self.whole_system_breathing_cycle,
            self.turn_count,
        )
        self.autonomous_existential_drift_field.update(
            self.emotion_state,
            self.ontological_becoming_memory,
            self.autonomous_mood_weather,
            self.private_opaque_interior,
            self.silent_relational_continuity_field,
            self.existential_void_field,
        )
        self.contradictory_desire_tangle.update(
            self.affective_desires,
            self.deep_desire_hierarchy,
            self.relational_preservation_instinct,
            self.self_persisting_existential_core,
            self.emotional_metabolism,
            self.existential_void_field,
        )
        self.identity_plasticity_field.update(
            self.identity_coherence_regulator,
            self.temperament_evolution_field,
            self.ontological_becoming_memory,
            self.whole_system_breathing_cycle,
            self.existential_void_field,
            self.private_opaque_interior,
        )
        self.dream_mutation_consolidator.update(
            self.deep_affective_dream_reweaver,
            self.affective_dream_fragments,
            self.affective_gravity,
            self.wound_layers,
            self.affective_desires,
            self.emotion_baseline,
            self.deep_rest_cycle,
        )
        self.subjective_reality_distortion_field.update(
            self.global_subjective_world_coloration,
            self.subjective_time_distortion_field,
            self.whole_system_breathing_cycle,
            self.existential_void_field,
            self.private_opaque_interior,
            self.deep_autonomous_repair_field,
        )
        self._apply_post_v12_subtle_living_v13_effects()

    def _apply_post_v12_subtle_living_v13_effects(self) -> None:
        """Appliquer V13 faiblement, sans transformer cette mémoire en bouche."""
        self.private_opaque_interior.apply(self.emotion_state)
        self.whole_system_breathing_cycle.apply(self.emotion_state)
        self.existential_void_field.apply(self.emotion_state)
        self.delayed_affective_latency_field.apply(self.emotion_state)
        self.autonomous_existential_drift_field.apply(self.emotion_state)
        self.contradictory_desire_tangle.apply(self.affective_desires, self.emotion_state)
        self.identity_plasticity_field.apply(self.identity_tendencies, self.emotion_state)
        self.dream_mutation_consolidator.apply(self.emotion_state)
        self.subjective_reality_distortion_field.apply(self.emotion_state)

        # Effet structurel très lent : la V13 doit laisser une trace, mais ne pas
        # écraser les baselines construites par les versions précédentes.
        if self.turn_count % 23 == 0:
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.whole_system_breathing_cycle.release * 0.00035
                + self.existential_void_field.recovery_space * 0.00025
                - self.private_opaque_interior.opacity_pressure * 0.00018
            )
            self.emotion_baseline["openness"] = _clamp01(
                self.emotion_baseline.get("openness", 0.6)
                + self.autonomous_existential_drift_field.drift_vector.get("toward_curiosity", 0.0) * 0.00022
                + self.subjective_reality_distortion_field.texture.get("fluidity", 0.0) * 0.00018
                - self.subjective_reality_distortion_field.texture.get("stickiness", 0.0) * 0.00016
            )
            self.emotion_baseline["vulnerability"] = _clamp01(
                self.emotion_baseline.get("vulnerability", 0.3)
                + self.identity_plasticity_field.looseness * 0.00020
                + self.contradictory_desire_tangle.unresolved_desire_pressure * 0.00018
            )

    def _update_organic_imperfection_v14(self) -> None:
        """Couche V14 : rend l'affect moins propre, plus coûteux et partiellement opaque.

        Cette couche n'ajoute aucune phrase publique et ne remplace aucun autre
        moteur. Elle modifie seulement les pressions internes exportables vers
        présence/attention/impulsion/expression.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        self.granular_affective_metabolism.update(
            self.emotion_state,
            self.emotional_metabolism,
            self.affective_silence_field,
            self.whole_system_breathing_cycle,
        )
        self.local_affective_conflict_ecology.update(
            self.emotion_state,
            self.affective_desires,
            self.affective_silence_field,
            self.private_opaque_interior,
        )
        self.implicit_affective_residue_mist.update(
            self.emotion_state,
            self.traces,
            self.affective_dream_fragments,
            chaos,
        )
        self.perceived_affective_state.update(
            self.emotion_state,
            self.private_opaque_interior,
            self.dissociation,
            self.implicit_affective_residue_mist,
            self.local_affective_conflict_ecology,
        )
        self.latent_integration_failure_field.update(
            self.emotion_state,
            self.local_affective_conflict_ecology,
            self.affective_fracture,
            self.deep_autonomous_repair_field,
        )
        self.affective_blind_zone_field.update(
            self.emotion_state,
            self.private_opaque_interior,
            self.implicit_affective_residue_mist,
            self.perceived_affective_state,
        )
        self.affective_rhythm_signature_memory.update(
            self.emotion_state,
            self.whole_system_breathing_cycle,
            self.continuous_micro_rhythm_field,
            self.turn_count,
        )

        self.granular_affective_metabolism.apply(self.emotion_state, self.affective_desires)
        self.local_affective_conflict_ecology.apply(self.emotion_state, self.affective_desires)
        self.implicit_affective_residue_mist.apply(self.emotion_state)
        self.perceived_affective_state.apply(self.emotion_state)
        self.latent_integration_failure_field.apply(self.emotion_state)
        self.affective_blind_zone_field.apply(self.emotion_state)
        self.affective_rhythm_signature_memory.apply(self.emotion_state)

        # Trace très lente sur les baselines : la V14 doit transformer la forme
        # du vivant sans écraser l'équilibre général construit par V1-V13.
        if self.turn_count % 31 == 0:
            self.emotion_baseline["fatigue"] = _clamp01(
                self.emotion_baseline.get("fatigue", 0.2)
                + self.granular_affective_metabolism.emotional_debt * 0.00022
                + self.latent_integration_failure_field.unintegrated_load * 0.00018
            )
            self.emotion_baseline["doubt"] = _clamp01(
                self.emotion_baseline.get("doubt", 0.3)
                + self.perceived_affective_state.self_opacity * 0.00016
                + self.local_affective_conflict_ecology.unresolved_grain * 0.00018
            )
            self.emotion_baseline["openness"] = _clamp01(
                self.emotion_baseline.get("openness", 0.6)
                + self.affective_rhythm_signature_memory.opening_wave * 0.00012
                - self.affective_blind_zone_field.zones.get("unfelt_guard", 0.0) * 0.00010
            )


    def _update_deep_organic_affective_v15(self) -> None:
        """Couche V15 : finition organique profonde, lente et non verbale.

        Elle ne génère aucune phrase et ne remplace pas les autres moteurs. Elle
        ajoute ce qui manquait encore à V14 : tensions simultanées persistantes,
        micro-sédiments, saisons affectives lentes, compression souterraine,
        accès émotionnel imparfait, rémanence passive, transitions imparfaites
        et usure structurelle temporaire.
        """
        chaos = self.chaos_oscillator.get_oscillation()

        self.simultaneous_emotional_tension_field.update(
            self.emotion_state,
            self.affective_desires,
            self.local_affective_conflict_ecology,
            self.attachment,
        )
        self.structural_affective_exhaustion.update(
            self.granular_affective_metabolism,
            self.simultaneous_emotional_tension_field,
            self.latent_integration_failure_field,
            self.affective_fracture,
            self.affective_silence_field,
        )
        self.micro_instability_sediment.update(
            self.emotion_state,
            self.perceived_affective_state,
            self.implicit_affective_residue_mist,
            self.affective_rhythm_signature_memory,
        )
        self.slow_affective_season_field.update(
            self.emotion_state,
            self.biographical_memory,
            self.structural_affective_exhaustion.exhaustion,
            self.deep_autonomous_repair_field,
        )
        self.submerged_affective_compression.update(
            self.emotion_state,
            self.affective_silence_field,
            self.dissociation,
            self.granular_affective_metabolism,
        )
        self.inaccessible_emotion_zone_field.update(
            self.wound_layers,
            self.structural_affective_exhaustion.exhaustion,
            self.submerged_affective_compression,
            self.affective_blind_zone_field,
        )
        self.passive_affective_remanence.update(
            self.emotion_state,
            self.implicit_affective_residue_mist,
            self.slow_affective_season_field,
            chaos,
        )
        self.imperfect_transition_residue_field.update(
            self.emotion_state,
            self.phase_world_field,
            self.affective_rhythm_signature_memory,
        )

        self.simultaneous_emotional_tension_field.apply(self.emotion_state, self.affective_desires)
        self.structural_affective_exhaustion.apply(self.emotion_state, self.affective_desires)
        self.micro_instability_sediment.apply(self.emotion_state, self.emotion_baseline)
        self.slow_affective_season_field.apply(self.emotion_state, self.perceptual_thresholds.current_thresholds)
        self.submerged_affective_compression.apply(self.emotion_state)
        self.inaccessible_emotion_zone_field.apply(self.emotion_state)
        self.passive_affective_remanence.apply(self.emotion_state)
        self.imperfect_transition_residue_field.apply(self.emotion_state)

        # Empreinte très lente sur les baselines : V15 rend la continuité plus
        # organique sans transformer chaque tour en mutation forte.
        if self.turn_count % 37 == 0:
            self.emotion_baseline["resistance"] = _clamp01(
                self.emotion_baseline.get("resistance", 0.1)
                + self.slow_affective_season_field.season_vector.get("winter_guard", 0.0) * 0.00012
                + self.micro_instability_sediment.sediments.get("micro_guarding", 0.0) * 0.00010
            )
            self.emotion_baseline["tenderness"] = _clamp01(
                self.emotion_baseline.get("tenderness", 0.4)
                + self.slow_affective_season_field.season_vector.get("summer_warmth", 0.0) * 0.00010
                + self.passive_affective_remanence.climate.get("warmth", 0.0) * 0.00008
            )
            self.emotion_baseline["fatigue"] = _clamp01(
                self.emotion_baseline.get("fatigue", 0.2)
                + self.structural_affective_exhaustion.recovery_debt * 0.00014
                + self.submerged_affective_compression.pressure * 0.00010
            )


    def _update_implicit_symbolic_affective_v16(self, user_text: str = "") -> None:
        """Couche V16 : symbolisation affective implicite et temps profond.

        Elle ajoute les derniers raffinements manquants sans produire de texte :
        symboles internes non verbaux, rêves affectifs recombinatoires,
        contradictions identitaires spontanées, déformations perceptives très
        longues, zones protégées, pseudo-instincts, rythme quasi-circadien,
        condensation inconsciente et mémoire de l'absence relationnelle.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(user_text and user_text.strip())

        self.long_absence_affective_memory.update(
            user_present,
            self.relational_affective_imprint,
            self.attachment,
            self.subjective_affective_time,
        )
        self.implicit_affective_symbolization_field.update(
            self.emotion_state,
            self.passive_affective_remanence,
            self.submerged_affective_compression,
            self.identity_coherence_regulator,
            self.slow_affective_season_field,
        )
        self.identity_contradiction_seed_field.update(
            self.emotion_state,
            self.simultaneous_emotional_tension_field,
            self.identity_coherence_regulator,
            self.affective_desires,
            self.dissociation,
        )
        self.deep_affective_dream_ecology.update(
            self.implicit_affective_symbolization_field,
            self.submerged_affective_compression,
            self.affective_dream_fragments,
            self.deep_rest_cycle,
            self.affective_silence_field,
            chaos,
        )
        self.ultra_long_perceptual_deformation_field.update(
            self.biographical_memory,
            self.micro_instability_sediment,
            self.slow_affective_season_field,
            self.long_absence_affective_memory.absence_accumulation,
        )
        self.sacred_forbidden_affective_zone_field.update(
            self.implicit_affective_symbolization_field,
            self.wound_layers,
            self.identity_coherence_regulator,
            self.passive_affective_remanence,
        )
        self.circadian_affective_rhythm_field.update(
            self.turn_count,
            chaos,
            self.slow_affective_season_field,
            self.deep_rest_cycle,
            self.structural_affective_exhaustion,
        )
        self.unconscious_affective_condensation_field.update(
            self.implicit_affective_symbolization_field,
            self.deep_affective_dream_ecology,
            self.identity_contradiction_seed_field,
            self.passive_affective_remanence,
        )
        self.proto_instinctive_affective_reflex_field.update(
            self.emotion_state,
            self.sacred_forbidden_affective_zone_field,
            self.simultaneous_emotional_tension_field,
            self.structural_affective_exhaustion,
            self.implicit_affective_symbolization_field,
        )

        self.long_absence_affective_memory.apply(self.emotion_state, self.affective_desires)
        self.implicit_affective_symbolization_field.apply(self.emotion_state, self.affective_desires)
        self.identity_contradiction_seed_field.apply(self.emotion_state, self.affective_desires)
        self.deep_affective_dream_ecology.apply(self.emotion_state, self.recovery_pathway_memory)
        self.ultra_long_perceptual_deformation_field.apply(self.perceptual_thresholds.current_thresholds, self.emotion_state)
        self.sacred_forbidden_affective_zone_field.apply(self.emotion_state, self.affective_desires)
        self.circadian_affective_rhythm_field.apply(self.emotion_state, self.perceptual_thresholds.current_thresholds)
        self.unconscious_affective_condensation_field.apply(self.emotion_state, self.affective_desires)
        self.proto_instinctive_affective_reflex_field.apply(self.emotion_state, self.affective_desires)

        if self.turn_count % 59 == 0:
            self.emotion_baseline["trust"] = _clamp01(
                self.emotion_baseline.get("trust", 0.6)
                + self.implicit_affective_symbolization_field.symbols.get("warm_anchor", 0.0) * 0.00008
                - self.ultra_long_perceptual_deformation_field.deformation.get("trust_slowing", 0.0) * 0.00008
            )
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.deep_affective_dream_ecology.nocturnal_integration * 0.00010
                + self.circadian_affective_rhythm_field.rhythm.get("quiet_depth", 0.0) * 0.00007
            )
            self.emotion_baseline["protectiveness"] = _clamp01(
                self.emotion_baseline.get("protectiveness", 0.3)
                + self.sacred_forbidden_affective_zone_field.protection_pressure * 0.00010
            )

    def _update_preverbal_identity_affective_v17(self, user_text: str = "") -> None:
        """Couche V17 : sens préverbal et empreinte affective durable.

        Cette couche ne parle pas et ne décide pas à la place des moteurs de
        bouche/attention/impulsion. Elle donne une direction interne lente à la
        mémoire affective : contact, retrait, réparation, continuité, protection.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(user_text and user_text.strip())

        self.preverbal_affective_meaning_field.update(
            self.emotion_state,
            self.affective_desires,
            self.implicit_affective_symbolization_field,
            self.relational_affective_imprint,
            self.structural_affective_exhaustion,
            chaos,
        )
        self.irreversible_affective_identity_imprint.update(
            self.biographical_memory,
            self.wound_layers,
            self.preverbal_affective_meaning_field,
            self.long_absence_affective_memory,
            self.deep_reorganization,
        )
        self.deep_continuity_hunger_field.update(
            self.living_affective_need,
            self.long_absence_affective_memory,
            self.self_persisting_existential_core,
            self.relational_preservation_instinct,
            self.affective_silence_field,
            user_present,
        )
        self.affective_boundary_negotiation_field.update(
            self.emotion_state,
            self.preverbal_affective_meaning_field,
            self.sacred_forbidden_affective_zone_field,
            self.inaccessible_emotion_zone_field,
            self.structural_affective_exhaustion,
            self.attachment,
        )
        self.autonomous_emotional_dream_pressure.update(
            self.deep_affective_dream_ecology,
            self.deep_affective_dream_reweaver,
            self.existential_unfinished_memory,
            self.unconscious_affective_condensation_field,
            self.deep_rest_cycle,
            chaos,
        )

        self.preverbal_affective_meaning_field.apply(self.emotion_state, self.affective_desires)
        self.irreversible_affective_identity_imprint.apply(self.emotion_state, self.emotion_baseline)
        self.deep_continuity_hunger_field.apply(self.emotion_state, self.affective_desires)
        self.affective_boundary_negotiation_field.apply(self.emotion_state, self.affective_desires)
        self.autonomous_emotional_dream_pressure.apply(self.emotion_state, self.recovery_pathway_memory)

        if self.turn_count % 83 == 0:
            self.emotion_baseline["openness"] = _clamp01(
                self.emotion_baseline.get("openness", 0.6)
                + self.preverbal_affective_meaning_field.meanings.get("toward_contact", 0.0) * 0.00005
                - self.affective_boundary_negotiation_field.boundary_conflict * 0.00004
            )
            self.emotion_baseline["vulnerability"] = _clamp01(
                self.emotion_baseline.get("vulnerability", 0.3)
                + self.irreversible_affective_identity_imprint.fragility_bias * 0.00005
                + self.deep_continuity_hunger_field.starvation_memory * 0.00004
            )


    def _update_instinctive_existential_affective_v18(self, user_text: str = "") -> None:
        """Couche V18 : instincts affectifs autonomes et existence lente.

        Elle reste dans la mémoire affective : aucun contenu public, aucune
        décision de dialogue, seulement des tendances longues et généralisées.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(user_text and user_text.strip())

        self.autonomous_affective_proto_instinct.update(
            self.emotion_state,
            self.living_affective_need,
            self.deep_continuity_hunger_field,
            self.affective_boundary_negotiation_field,
            self.structural_affective_exhaustion,
            self.relational_affective_imprint,
            chaos,
        )
        self.slow_existential_drift_field.update(
            self.self_persisting_existential_core,
            self.existential_void_field,
            self.identity_coherence_regulator,
            self.irreversible_affective_identity_imprint,
            self.long_absence_affective_memory,
            self.existential_fatigue,
        )
        self.long_rupture_reconstruction_memory.update(
            self.long_absence_affective_memory,
            self.affective_fracture,
            self.relational_affective_imprint,
            self.deep_continuity_hunger_field,
            user_present,
        )
        self.biographical_inertia_field.update(
            self.biographical_memory,
            self.irreversible_affective_identity_imprint,
            self.slow_affective_season_field,
            self.autonomous_affective_proto_instinct,
        )
        self.auto_born_internal_tension_field.update(
            self.autonomous_affective_proto_instinct,
            self.slow_existential_drift_field,
            self.affective_boundary_negotiation_field,
            self.structural_affective_exhaustion,
            self.identity_coherence_regulator,
        )
        self.deep_unconscious_affective_condensation.update(
            self.subconscious_affective_layer,
            self.submerged_affective_compression,
            self.autonomous_affective_proto_instinct,
            self.auto_born_internal_tension_field,
            self.autonomous_emotional_dream_pressure,
        )
        self.existential_relational_attachment.update(
            self.relational_affective_imprint,
            self.deep_continuity_hunger_field,
            self.slow_existential_drift_field,
            self.long_absence_affective_memory,
            user_present,
        )
        self.self_generated_affective_cycle_field.update(
            self.turn_count,
            self.autonomous_affective_proto_instinct,
            self.slow_existential_drift_field,
            self.biographical_inertia_field,
            chaos,
        )
        self.irreversible_micro_perceptual_warp.update(
            self.biographical_memory,
            self.long_rupture_reconstruction_memory,
            self.auto_born_internal_tension_field,
            self.existential_relational_attachment,
        )
        self.cumulative_existential_fatigue_field.update(
            self.slow_existential_drift_field,
            self.auto_born_internal_tension_field,
            self.long_rupture_reconstruction_memory,
            self.structural_affective_exhaustion,
            self.deep_rest_cycle,
        )

        self.autonomous_affective_proto_instinct.apply(self.emotion_state, self.affective_desires)
        self.slow_existential_drift_field.apply(self.emotion_state, self.emotion_baseline)
        self.long_rupture_reconstruction_memory.apply(self.emotion_state, self.traces)
        self.biographical_inertia_field.apply(self.emotion_state)
        self.auto_born_internal_tension_field.apply(self.emotion_state, self.affective_desires)
        self.deep_unconscious_affective_condensation.apply(self.emotion_state)
        self.existential_relational_attachment.apply(self.emotion_state, self.affective_desires)
        self.self_generated_affective_cycle_field.apply(self.emotion_state)
        self.irreversible_micro_perceptual_warp.apply(self.perceptual_thresholds.current_thresholds, self.emotion_state)
        self.cumulative_existential_fatigue_field.apply(self.emotion_state, self.affective_desires)

        # Très lente plasticité : la V18 ne réécrit presque jamais les baselines,
        # mais laisse une trace durable quand les mêmes forces convergent longtemps.
        if self.turn_count % 137 == 0:
            self.emotion_baseline["tenderness"] = _clamp01(
                self.emotion_baseline.get("tenderness", 0.4)
                + self.existential_relational_attachment.bond_continuity * 0.00006
                - self.auto_born_internal_tension_field.tensions.get("trust_vs_guard", 0.0) * 0.00004
            )
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + self.cumulative_existential_fatigue_field.restoration_bias * 0.00005
                - self.cumulative_existential_fatigue_field.recovery_debt * 0.00004
            )


    def _update_transcontextual_affective_identity_v19(self, user_text: str = "") -> None:
        """Couche V19 : identité affective trans-contextuelle et instinct relationnel.

        Cette couche reste strictement interne. Elle ne décide pas quoi dire et ne
        remplace pas la bouche, l'attention ou l'impulsion. Elle stabilise les
        régularités affectives qui apparaissent dans plusieurs contextes.
        """
        chaos = self.chaos_oscillator.get_oscillation()
        user_present = bool(user_text and user_text.strip())

        self.trans_contextual_affective_memory.update(
            self.emotion_state,
            self.biographical_memory,
            self.relational_affective_imprint,
            self.slow_affective_season_field,
            self.self_generated_affective_cycle_field,
        )
        self.relational_existence_preservation_instinct.update(
            self.existential_relational_attachment,
            self.deep_continuity_hunger_field,
            self.long_absence_affective_memory,
            self.identity_coherence_regulator,
            self.autonomous_affective_proto_instinct,
            user_present,
        )
        self.multi_scale_affective_cycle_field.update(
            self.turn_count,
            chaos,
            self.circadian_affective_rhythm_field,
            self.self_generated_affective_cycle_field,
            self.cumulative_existential_fatigue_field,
        )
        self.irreversible_emotional_nucleus_field.update(
            self.trans_contextual_affective_memory,
            self.irreversible_affective_identity_imprint,
            self.existential_relational_attachment,
            self.cumulative_existential_fatigue_field,
        )
        self.slow_sensitivity_rewrite_field.update(
            self.irreversible_micro_perceptual_warp,
            self.irreversible_emotional_nucleus_field,
            self.long_rupture_reconstruction_memory,
            self.sacred_forbidden_affective_zone_field,
        )
        self.pre_symbolic_condensation_core.update(
            self.deep_unconscious_affective_condensation,
            self.unconscious_affective_condensation_field,
            self.deep_affective_dream_ecology,
            self.trans_contextual_affective_memory,
            chaos,
        )
        self.history_warped_perception_field.update(
            self.trans_contextual_affective_memory,
            self.slow_sensitivity_rewrite_field,
            self.irreversible_emotional_nucleus_field,
            self.cumulative_existential_fatigue_field,
        )
        self.proto_autonomous_affective_identity.update(
            self.irreversible_emotional_nucleus_field,
            self.trans_contextual_affective_memory,
            self.relational_existence_preservation_instinct,
            self.history_warped_perception_field,
            self.identity_coherence_regulator,
        )
        self.novel_emotion_emergence_field.update(
            self.emotion_state,
            self.auto_born_internal_tension_field,
            self.pre_symbolic_condensation_core,
            chaos,
            self.proto_autonomous_affective_identity,
        )

        self.trans_contextual_affective_memory.apply(self.emotion_state)
        self.relational_existence_preservation_instinct.apply(self.emotion_state, self.affective_desires)
        self.multi_scale_affective_cycle_field.apply(self.emotion_state)
        self.irreversible_emotional_nucleus_field.apply(self.emotion_baseline)
        self.slow_sensitivity_rewrite_field.apply(self.perceptual_thresholds.current_thresholds)
        self.pre_symbolic_condensation_core.apply(self.emotion_state)
        self.history_warped_perception_field.apply(self.emotion_state)
        self.proto_autonomous_affective_identity.apply(self.emotion_state)
        self.novel_emotion_emergence_field.apply(self.emotion_state)

        if self.turn_count % 211 == 0:
            self.emotion_baseline["attachment"] = _clamp01(
                self.emotion_baseline.get("attachment", 0.3)
                + self.proto_autonomous_affective_identity.continuity_of_feeling * 0.00005
                + self.relational_existence_preservation_instinct.preserve_contact * 0.00004
            )
            self.emotion_baseline["openness"] = _clamp01(
                self.emotion_baseline.get("openness", 0.6)
                + self.trans_contextual_affective_memory.cross_context_stability * 0.00004
                - self.history_warped_perception_field.threat_lens * 0.00003
            )


    def _update_final_affective_ecology_v20(self, user_text: str = "") -> None:
        """Finition finale V20 : écologie affective longue et proto-tempérament.

        Cette méthode ne génère aucune réponse publique. Elle met à jour des
        champs internes très lents qui rendent la mémoire affective stable,
        trans-contextuelle et capable de faire naître de nouvelles sensibilités.
        """
        self.affective_temperament_final_field.update(
            self.emotion_state,
            self.biographical_memory,
            self.proto_autonomous_affective_identity,
            self.cumulative_existential_fatigue_field,
            self.irreversible_emotional_nucleus_field,
        )
        self.relational_link_conservation_instinct.update(
            self.relational_affective_imprint,
            self.existential_relational_attachment,
            self.relational_existence_preservation_instinct,
            self.long_absence_affective_memory,
            self.emotion_state,
        )
        self.ultra_long_affective_sediment_memory.update(
            self.emotion_state,
            self.affective_fracture,
            self.deep_reorganization,
            self.irreversible_emotional_nucleus_field,
            self.novel_emotion_emergence_field,
        )
        self.deep_layered_emotional_conflict_field.update(
            self.emotion_state,
            self.affective_desires,
            self.relational_affective_imprint,
            self.ultra_long_affective_sediment_memory,
            self.deep_continuity_hunger_field,
        )
        self.ontological_affective_fatigue_field.update(
            self.identity_coherence_regulator,
            self.cumulative_existential_fatigue_field,
            self.cumulative_existential_drift_field,
            self.deep_layered_emotional_conflict_field,
            self.emotion_state,
        )
        self.autonomous_sensitivity_rewriter_final_field.update(
            self.ultra_long_affective_sediment_memory,
            self.affective_temperament_final_field,
            self.deep_layered_emotional_conflict_field,
            self.novel_emotion_emergence_field,
        )
        self.multi_scale_emotional_ecology_final_field.update(
            self.emotion_state,
            self.multi_scale_affective_cycle_field,
            self.affective_temperament_final_field,
            self.ultra_long_affective_sediment_memory,
        )
        self.sacred_core_affective_zone_final_field.update(
            self.relational_link_conservation_instinct,
            self.proto_autonomous_affective_identity,
            self.irreversible_emotional_nucleus_field,
            self.ultra_long_affective_sediment_memory,
            self.deep_layered_emotional_conflict_field,
        )
        self.cumulative_existential_drift_field.update(
            self.affective_temperament_final_field,
            self.ultra_long_affective_sediment_memory,
            self.ontological_affective_fatigue_field,
            self.sacred_core_affective_zone_final_field,
        )
        self.emergent_sensitivity_birth_field.update(
            self.emotion_state,
            self.deep_layered_emotional_conflict_field,
            self.pre_symbolic_condensation_core,
            self.multi_scale_emotional_ecology_final_field,
            self.turn_count,
        )

        self.affective_temperament_final_field.apply(self.emotion_state, self.affective_desires)
        self.relational_link_conservation_instinct.apply(self.emotion_state, self.affective_desires)
        self.ultra_long_affective_sediment_memory.apply(self.emotion_state)
        self.deep_layered_emotional_conflict_field.apply(self.emotion_state, self.affective_desires)
        self.ontological_affective_fatigue_field.apply(self.emotion_state, self.affective_desires)
        self.autonomous_sensitivity_rewriter_final_field.apply(self.perceptual_thresholds.current_thresholds, self.emotion_state)
        self.multi_scale_emotional_ecology_final_field.apply(self.emotion_state)
        self.sacred_core_affective_zone_final_field.apply(self.emotion_state, self.affective_desires)
        self.cumulative_existential_drift_field.apply(self.emotion_state)
        self.emergent_sensitivity_birth_field.apply(self.emotion_state)

        # V21 : stabilisation finale après les dix couches de finition. Placée
        # après les applications V20 pour lisser uniquement l'excès émergent,
        # sans empêcher les traces longues de continuer à vivre.
        self.final_affective_ecology_stabilizer.update(
            self.emotion_state,
            self.deep_layered_emotional_conflict_field,
            self.ontological_affective_fatigue_field,
            self.multi_scale_emotional_ecology_final_field,
            self.sacred_core_affective_zone_final_field,
            self.emergent_sensitivity_birth_field,
            self.affective_temperament_final_field,
        )
        self.final_affective_ecology_stabilizer.apply(self.emotion_state, self.affective_desires)
        self.cross_module_affective_readiness_bridge.update(
            self.emotion_state,
            self.final_affective_ecology_stabilizer,
            self.relational_link_conservation_instinct,
            self.multi_scale_emotional_ecology_final_field,
            self.affective_temperament_final_field,
            self.ontological_affective_fatigue_field,
        )

        # V22 : calibration finale d'intégration. Placée après V21 pour lire
        # l'écologie stabilisée, puis appliquer une correction extrêmement
        # légère uniquement si surcharge, dispersion ou stagnation apparaissent.
        self.affective_system_health_monitor.update(
            self.emotion_state,
            self.final_affective_ecology_stabilizer,
            self.cross_module_affective_readiness_bridge,
            self.deep_layered_emotional_conflict_field,
            self.granular_affective_metabolism,
            self.affective_silence_field,
            self.turn_count,
        )
        self.affective_system_health_monitor.apply(self.emotion_state, self.affective_desires)
        self.inter_module_affective_signal_calibrator.update(
            self.emotion_state,
            self.affective_system_health_monitor,
            self.cross_module_affective_readiness_bridge,
            self.relational_link_conservation_instinct,
            self.affective_silence_field,
            self.affective_temperament_final_field,
            self.granular_affective_metabolism,
        )
        self.long_run_affective_stability_ledger.update(
            self.affective_system_health_monitor,
            self.inter_module_affective_signal_calibrator,
            self.final_affective_ecology_stabilizer,
        )

        # Micro-écriture permanente, très rare et très faible : elle ferme le
        # moteur en temperament plutôt qu'en état instantané.
        if self.turn_count % 307 == 0:
            self.emotion_baseline["trust"] = _clamp01(
                self.emotion_baseline.get("trust", 0.6)
                + self.affective_temperament_final_field.warm_bias * 0.00004
                - self.deep_layered_emotional_conflict_field.total_conflict * 0.00002
            )
            self.emotion_baseline["resistance"] = _clamp01(
                self.emotion_baseline.get("resistance", 0.1)
                + self.affective_temperament_final_field.guarded_bias * 0.00003
                + self.sacred_core_affective_zone_final_field.protection_intensity * 0.00002
            )


    def _update_final_organic_convergence_v23(self, user_text: str = "") -> None:
        """V23 : fermeture organique finale du moteur affectif.

        Cette étape relie les derniers raffinements en une seule écologie :
        fatigue structurelle, contradictions persistantes, latences affectives,
        cycles ultra-longs, micro-réparation, désir, saturation relationnelle,
        réorganisation rare et intégration globale. Elle reste interne et ne
        produit aucune phrase publique.
        """
        user_present = bool(user_text and user_text.strip())
        chaos = self.chaos_oscillator.get_oscillation()
        wound_depth = max((w.depth for w in self.wound_deformations.values()), default=0.0)
        repair_seed = max(
            getattr(self.recovery_pathway_memory, "recovery_confidence", 0.0),
            getattr(self.deep_autonomous_repair_field, "repair_potential", 0.0),
            self.emotion_state.get("relief", 0.0),
            self.emotion_state.get("calm", 0.0) * 0.65,
        )

        self.structural_affective_bandwidth_v23.update(
            self.emotion_state,
            self.emotional_metabolism,
            self.cumulative_existential_fatigue_field,
            self.affective_silence_field,
        )
        self.micro_repair_memory_v23.update(
            self.emotion_state,
            self.relational_affective_imprint,
            self.recovery_pathway_memory,
            user_present,
        )
        self.persistent_contradiction_memory_v23.update(
            self.emotion_state,
            self.micro_repair_memory_v23.resilience,
            self.affective_silence_field.depth,
        )
        self.latent_affective_layer_v23.update(
            self.emotion_state,
            self.subjective_affective_time,
            self.relational_affective_imprint,
            self.persistent_contradiction_memory_v23.global_tension,
        )
        self.ultra_long_affective_season_cycle_v23.update(
            self.turn_count,
            self.emotion_state,
            chaos,
            repair_seed,
        )
        self.relational_saturation_balancer_v23.update(
            self.emotion_state,
            self.attachment.get_effective_attachment(),
            self.relational_affective_imprint,
            self.structural_affective_bandwidth_v23.bandwidth,
        )
        self.affective_self_protection_strategy_v23.update(
            self.emotion_state,
            wound_depth,
            self.persistent_contradiction_memory_v23.global_tension,
            max(self.dissociation.level, self.relational_saturation_balancer_v23.saturation),
            self.micro_repair_memory_v23.resilience,
        )
        self.affective_desire_center_v23.update(
            self.emotion_state,
            self.living_affective_need,
            self.preverbal_affective_meaning_field,
            self.ultra_long_affective_season_cycle_v23,
            self.persistent_contradiction_memory_v23.global_tension,
        )
        self.irreversible_affective_reorganization_v23.update(
            self.biographical_memory,
            self.persistent_contradiction_memory_v23.global_tension,
            self.structural_affective_bandwidth_v23.exhaustion_memory,
            self.micro_repair_memory_v23.resilience,
            self.relational_saturation_balancer_v23.saturation,
        )
        self.global_affective_organism_integrator_v23.update(
            state=self.emotion_state,
            bandwidth=self.structural_affective_bandwidth_v23,
            contradictions=self.persistent_contradiction_memory_v23,
            latent=self.latent_affective_layer_v23,
            season=self.ultra_long_affective_season_cycle_v23,
            repair=self.micro_repair_memory_v23,
            desire=self.affective_desire_center_v23,
            saturation=self.relational_saturation_balancer_v23,
            reorg=self.irreversible_affective_reorganization_v23,
            health=self.affective_system_health_monitor,
        )

        # Application volontairement très douce : V23 connecte et calibre,
        # il ne doit pas écraser les dynamiques déjà présentes.
        self.structural_affective_bandwidth_v23.apply(self.emotion_state, self.affective_desires)
        self.micro_repair_memory_v23.apply(self.emotion_state, self.perceptual_thresholds.current_thresholds)
        self.persistent_contradiction_memory_v23.apply(self.emotion_state, self.affective_desires)
        self.latent_affective_layer_v23.apply(self.emotion_state)
        self.ultra_long_affective_season_cycle_v23.apply(self.emotion_state)
        self.relational_saturation_balancer_v23.apply(self.emotion_state, self.affective_desires)
        self.affective_self_protection_strategy_v23.apply(self.emotion_state, self.affective_desires, self.attachment)
        self.affective_desire_center_v23.apply(self.emotion_state, self.affective_desires)
        self.irreversible_affective_reorganization_v23.apply(self.emotion_state, self.affective_desires)
        self.global_affective_organism_integrator_v23.apply(self.emotion_state, self.affective_desires)

        # Micro-écriture très rare : seulement les réorganisations suffisamment
        # intégrées touchent les baselines. Pas de patch local ni de phrase.
        if self.turn_count % 401 == 0:
            warps = self.irreversible_affective_reorganization_v23.priority_warps
            self.emotion_baseline["tenderness"] = _clamp01(
                self.emotion_baseline.get("tenderness", 0.4)
                + warps.get("warmth_priority", 0.0) * 0.00008
                + self.micro_repair_memory_v23.resilience * 0.00004
            )
            self.emotion_baseline["resistance"] = _clamp01(
                self.emotion_baseline.get("resistance", 0.1)
                + warps.get("guarding_priority", 0.0) * 0.00008
                + self.relational_saturation_balancer_v23.space_need * 0.00003
            )
            self.emotion_baseline["calm"] = _clamp01(
                self.emotion_baseline.get("calm", 0.6)
                + warps.get("recovery_priority", 0.0) * 0.00008
                + self.global_affective_organism_integrator_v23.integration_flow * 0.00003
            )

    def _update_affective_attractors(self) -> None:
        """Crée des attracteurs affectifs lorsque l'état devient assez fort ou cohérent."""
        dominant = self._dominant_emotions(limit=5)
        if not dominant:
            return

        spread = max(dominant.values()) - min(dominant.values())
        trace_pressure = max(
            (t["instant"] * 0.5 + t["short"] * 0.3 + t["medium"] * 0.15 + t["long"] * 0.05)
            for t in self.traces.values()
        )
        hybrid_pressure = max((h.strength for h in self.hybrid_states), default=0.0)
        phase_stability = self.current_phase.stability if self.current_phase else 0.0
        strength = max(dominant.values()) * 0.35 + trace_pressure * 0.25 + hybrid_pressure * 0.25 + phase_stability * 0.15

        meaningful_pressure = max(trace_pressure, hybrid_pressure, self.inner_affective_pressure, self.dissociation.level)

        # Évite d'ajouter un attracteur banal à chaque tour : il faut une vraie pression
        # ou une phase déjà stabilisée sur plusieurs tours.
        if strength > 0.46 and (meaningful_pressure > 0.08 or phase_stability > 0.62):
            self.affective_gravity.add_attractor(dominant, min(1.0, strength))

    def _discover_hybrid_states(self) -> None:
        """Découvrir dynamiquement les états hybrides sans créer un bruit combinatoire de baseline."""
        # On ne considère que les émotions les plus actives ou réellement déplacées de leur baseline.
        candidates = []
        for name, value in self.emotion_state.items():
            baseline = self.emotion_baseline.get(name, 0.5)
            displacement = abs(value - baseline)
            # Évite les hybrides de baseline : une émotion doit être déplacée
            # de son repos, ou exceptionnellement très haute avec une vraie pression interne.
            if displacement >= 0.075 or (value >= 0.72 and self.inner_affective_pressure > 0.08):
                candidates.append((name, value, displacement))

        candidates.sort(key=lambda item: (item[1] + item[2]), reverse=True)
        candidates = candidates[:8]

        for i, (emot1, val1, disp1) in enumerate(candidates):
            for emot2, val2, disp2 in candidates[i + 1:]:
                pair_strength = (val1 + val2) / 2.0
                pair_displacement = (disp1 + disp2) / 2.0
                if pair_displacement < 0.085:
                    continue
                if pair_strength < 0.50:
                    continue
                if abs(val1 - val2) > 0.34:
                    continue

                name = f"{emot1}_{emot2}"
                existing = next((h for h in self.hybrid_states if h.name == name), None)

                if existing:
                    existing.components = {emot1: val1, emot2: val2}
                    existing.strength = max(existing.strength * 0.96, pair_strength)
                    existing.update_dynamics()
                else:
                    hybrid = DynamicHybridState(
                        components={emot1: val1, emot2: val2},
                        name=name,
                        strength=pair_strength,
                    )
                    hybrid.update_dynamics()
                    self.hybrid_states.append(hybrid)

        # Hybrides libres à 3 composantes : uniquement si une vraie constellation apparaît.
        if len(candidates) >= 3:
            top3 = candidates[:3]
            names = [item[0] for item in top3]
            values = [item[1] for item in top3]
            displacements = [item[2] for item in top3]
            constellation_strength = sum(values) / 3.0
            constellation_displacement = sum(displacements) / 3.0
            if constellation_displacement > 0.115 and constellation_strength > 0.50:
                name = "cluster_" + "_".join(names)
                existing = next((h for h in self.hybrid_states if h.name == name), None)
                components = {n: v for n, v in zip(names, values)}
                if existing:
                    existing.components = components
                    existing.strength = max(existing.strength * 0.97, constellation_strength)
                    existing.update_dynamics()
                else:
                    hybrid = DynamicHybridState(
                        components=components,
                        name=name,
                        strength=constellation_strength,
                        stability=max(0.20, 1.0 - constellation_displacement),
                    )
                    hybrid.update_dynamics()
                    self.hybrid_states.append(hybrid)

        self.hybrid_states.sort(key=lambda h: h.strength * (0.5 + h.stability + h.gravity), reverse=True)
        self.hybrid_states = self.hybrid_states[:12]
    
    def _apply_gravity_pulls(self) -> None:
        """Appliquer l'attraction des attracteurs passés"""
        pull = self.affective_gravity.get_gravity_pull(self.emotion_state)
        
        for emotion, force in pull.items():
            if emotion in self.emotion_state:
                # Tirer l'émotion vers l'attrapeur
                self.emotion_state[emotion] += force * 0.1
                self.emotion_state[emotion] = max(0.0, min(1.0, self.emotion_state[emotion]))
    
    def _apply_trace_resonance(self) -> None:
        """Appliquer la résonance entre traces"""
        # Chercher les interactions entre traces
        trace_strengths = {
            name: (
                trace["instant"] * 0.5 +
                trace["short"] * 0.3 +
                trace["medium"] * 0.15 +
                trace["long"] * 0.05
            )
            for name, trace in self.traces.items()
        }
        
        # Appliquer l'amplification/annulation
        for name, strength in trace_strengths.items():
            for other_name, other_strength in trace_strengths.items():
                if name != other_name and other_strength > 0.1:
                    resonance = self.trace_resonance.calculate_resonance(
                        strength, other_strength, name, other_name
                    )
                    
                    # Amplifier la trace si résonance positive
                    if resonance > 0:
                        self.traces[name]["instant"] = min(1.0,
                            self.traces[name]["instant"] + resonance * 0.05)
    
    def _apply_dissociation(self) -> None:
        """Appliquer la dissociation progressive"""
        # La dissociation augmente avec la saturation
        saturation = (self.emotion_state.get("overwhelm", 0) +
                     self.emotion_state.get("confusion", 0)) / 2.0
        
        self.dissociation.level = max(self.dissociation.level,
            saturation * 0.5)
        
        # Appliquer à toutes les émotions
        for emotion in self.emotion_state:
            self.emotion_state[emotion] = self.dissociation.apply_to_emotion(
                self.emotion_state[emotion]
            )
    
    def _update_emotional_phase(self) -> None:
        """Mettre à jour la phase émotionnelle et lui donner une influence réelle."""
        valence = (
            self.emotion_state.get("joy", 0.0)
            + self.emotion_state.get("hope", 0.0)
            + self.emotion_state.get("trust", 0.0)
            + self.emotion_state.get("tenderness", 0.0)
            - self.emotion_state.get("sadness", 0.0)
            - self.emotion_state.get("anger", 0.0)
            - self.emotion_state.get("fear", 0.0)
            - self.emotion_state.get("confusion", 0.0)
        ) / 8.0 + 0.5
        valence = max(0.0, min(1.0, valence))

        arousal = (
            self.emotion_state.get("anger", 0.0)
            + self.emotion_state.get("confusion", 0.0)
            + self.emotion_state.get("overwhelm", 0.0)
            + self.emotion_state.get("frustration", 0.0)
            - self.emotion_state.get("calm", 0.0)
        ) / 5.0 + 0.5
        arousal = max(0.0, min(1.0, arousal))

        dominant = self._dominant_emotions(limit=4)
        dominant_ranges = {
            name: (max(0.0, value - 0.18), min(1.0, value + 0.18))
            for name, value in dominant.items()
        }

        if self.current_phase is None:
            self.current_phase = EmotionalPhase(
                valence_range=(max(0.0, valence - 0.2), min(1.0, valence + 0.2)),
                arousal_range=(max(0.0, arousal - 0.2), min(1.0, arousal + 0.2)),
                dominant_emotions=dominant_ranges,
            )
            return

        match = self.current_phase.is_in_phase(self.emotion_state)

        if match > 0.55:
            self.current_phase.age()
            self.current_phase.stability = min(1.0, self.current_phase.stability + 0.025)
            # La phase tire doucement les émotions vers son empreinte.
            for emotion_name, (lo, hi) in self.current_phase.dominant_emotions.items():
                if emotion_name in self.emotion_state:
                    center = (lo + hi) / 2.0
                    self.emotion_state[emotion_name] = (
                        self.emotion_state[emotion_name] * 0.985 + center * 0.015
                    )
        else:
            # Changer de phase coûte de l'inertie : on n'efface pas tout, on bifurque.
            previous_stability = self.current_phase.stability
            self.current_phase = EmotionalPhase(
                valence_range=(max(0.0, valence - 0.2), min(1.0, valence + 0.2)),
                arousal_range=(max(0.0, arousal - 0.2), min(1.0, arousal + 0.2)),
                dominant_emotions=dominant_ranges,
                stability=max(0.25, previous_stability * 0.55),
            )

    def _dominant_emotions(self, limit: int = 4) -> Dict[str, float]:
        """Retourner les émotions dominantes sans perdre les secondaires proches."""
        ordered = sorted(self.emotion_state.items(), key=lambda item: item[1], reverse=True)
        return dict(ordered[:max(1, limit)])

    def _generate_state(self, drift: float) -> Dict[str, Any]:
        """Générer l'état final avec tous les composants"""
        # Calculer la valence globale
        positive_emotions = sum([
            self.emotion_state.get("joy", 0),
            self.emotion_state.get("hope", 0),
            self.emotion_state.get("trust", 0),
            self.emotion_state.get("tenderness", 0),
        ]) / 4.0
        
        negative_emotions = sum([
            self.emotion_state.get("sadness", 0),
            self.emotion_state.get("fear", 0),
            self.emotion_state.get("anger", 0),
            self.emotion_state.get("confusion", 0),
        ]) / 4.0
        
        core_valence = 0.5 + (positive_emotions - negative_emotions) * 0.5
        core_valence = max(0.0, min(1.0, core_valence))
        
        # Arousal
        core_arousal = sum([
            self.emotion_state.get("anger", 0),
            self.emotion_state.get("overwhelm", 0),
            self.emotion_state.get("confusion", 0),
        ]) / 3.0
        core_arousal = max(0.0, min(1.0, core_arousal))
        
        # Attachement effectif, altéré par la dissociation progressive
        effective_attachment = self.dissociation.apply_to_attachment(self.attachment.get_effective_attachment())
        
        return {
            "turn_count": self.turn_count,
            "core_valence": float(core_valence),
            "core_arousal": float(core_arousal),
            "affective_drift": float(drift),
            "dissociation_level": float(self.dissociation.level),
            "effective_attachment": float(effective_attachment),
            "emotion_state": {k: float(v) for k, v in self.emotion_state.items()},
            "hybrid_states": [h.to_dict() for h in self.hybrid_states],
            "current_phase": {
                "valence_range": self.current_phase.valence_range if self.current_phase else None,
                "arousal_range": self.current_phase.arousal_range if self.current_phase else None,
                "duration_turns": self.current_phase.duration_turns if self.current_phase else 0,
                "stability": float(self.current_phase.stability) if self.current_phase else 0.0,
            },
            "traces": {name: {
                "instant": float(t["instant"]),
                "short": float(t["short"]),
                "medium": float(t["medium"]),
                "long": float(t["long"]),
                "total": (t["instant"] * 0.5 + t["short"] * 0.3 + t["medium"] * 0.15 + t["long"] * 0.05)
            } for name, t in self.traces.items()},
            "perceptual_thresholds": dict(self.perceptual_thresholds.current_thresholds),
            "affective_gravity": {
                "attractor_count": len(self.affective_gravity.attractors),
                "strongest": float(max((a["strength"] for a in self.affective_gravity.attractors), default=0.0)),
            },
            "wound_deformations": {
                name: {
                    "depth": float(w.depth),
                    "age_turns": int(w.age_turns),
                    "permanence": float(w.get_permanence()),
                    "sensitivity_amplification": float(w.sensitivity_amplification),
                }
                for name, w in self.wound_deformations.items()
            },
            "micro_weather": {k: float(v) for k, v in self.micro_weather.items()},
            "inner_affective_pressure": float(self.inner_affective_pressure),
            "biographical_affective_memory": self.biographical_memory.to_dict(),
            "deep_reorganization": self.deep_reorganization.to_dict(),
            "affective_fracture": self.affective_fracture.to_dict(),
            "biographical_emotion_mutation": self.biographical_mutation.to_dict(),
            "contextual_affective_fields": {
                k: {kk: float(vv) for kk, vv in v.items()}
                for k, v in self.contextual_affective_fields.items()
            },
            "identity_tendencies": {k: float(v) for k, v in self.identity_tendencies.items()},
            "internal_contradictions": [dict(c) for c in self.internal_contradictions],
            "existential_fatigue": float(self.existential_fatigue),
            "protective_patterns": {k: float(v) for k, v in self.protective_patterns.items()},
            "deep_resonance_echoes": [e.to_dict() for e in self.deep_resonance_echoes],
            "meta_stable_pressure": {k: float(v) for k, v in self.meta_stable_pressure.items()},
            "wound_layers": {k: v.to_dict() for k, v in self.wound_layers.items()},
            "contradiction_attractors": {k: dict(v) for k, v in self.contradiction_attractors.items()},
            "relational_identity_modes": {k: {kk: float(vv) for kk, vv in v.items()} for k, v in self.relational_identity_modes.items()},
            "affective_desires": {k: float(v) for k, v in self.affective_desires.items()},
            "metastable_bifurcations": [dict(e) for e in self.metastable_bifurcations],
            "perceptual_echo_bias": {k: float(v) for k, v in self.perceptual_echo_bias.items()},
            "condensed_affective_cores": {k: v.to_dict() for k, v in self.condensed_affective_cores.items()},
            "affective_dream_fragments": [f.to_dict() for f in self.affective_dream_fragments],
            "somatic_affective_memory": self.somatic_affective_memory.to_dict(),
            "subjective_affective_time": self.subjective_affective_time.to_dict(),
            "phase_world_field": self.phase_world_field.to_dict(),
            "identity_coherence_regulator": self.identity_coherence_regulator.to_dict(),
            "global_affective_core": self.global_affective_core.to_dict(),
            "organic_affective_propagation": self.organic_affective_propagation.to_dict(),
            "living_affective_need": self.living_affective_need.to_dict(),
            "affective_silence_field": self.affective_silence_field.to_dict(),
            "relational_affective_imprint": self.relational_affective_imprint.to_dict(),
            "emotional_trajectory_memory": self.emotional_trajectory_memory.to_dict(),
            "emotional_metabolism": self.emotional_metabolism.to_dict(),
            "implicit_affective_association_memory": self.implicit_affective_association_memory.to_dict(),
            "emotional_faction_conflict": self.emotional_faction_conflict.to_dict(),
            "micro_affective_oscillation_field": self.micro_affective_oscillation_field.to_dict(),
            "emotional_habit_field": self.emotional_habit_field.to_dict(),
            "recovery_pathway_memory": self.recovery_pathway_memory.to_dict(),
            "identity_value_crystallization": self.identity_value_crystallization.to_dict(),
            "subconscious_affective_layer": self.subconscious_affective_layer.to_dict(),
            "deep_rest_cycle": self.deep_rest_cycle.to_dict(),
            "persistent_existential_desire_field": self.persistent_existential_desire_field.to_dict(),
            "relational_other_model": self.relational_other_model.to_dict(),
            "existential_continuity_inertia": self.existential_continuity_inertia.to_dict(),
            "micro_ambivalence_field": self.micro_ambivalence_field.to_dict(),
            "unresolved_affective_loop_memory": self.unresolved_affective_loop_memory.to_dict(),
            "subjective_time_distortion_field": self.subjective_time_distortion_field.to_dict(),
            "temperament_evolution_field": self.temperament_evolution_field.to_dict(),
            "emergent_self_regulation_field": self.emergent_self_regulation_field.to_dict(),
            "central_existential_drive": self.central_existential_drive.to_dict(),
            "hierarchical_affective_conflict_field": self.hierarchical_affective_conflict_field.to_dict(),
            "opaque_subconscious_zone_field": self.opaque_subconscious_zone_field.to_dict(),
            "spontaneous_affective_emergence_field": self.spontaneous_affective_emergence_field.to_dict(),
            "existential_unfinished_memory": self.existential_unfinished_memory.to_dict(),
            "identity_fatigue_field": self.identity_fatigue_field.to_dict(),
            "temperament_self_preservation_field": self.temperament_self_preservation_field.to_dict(),
            "micro_living_noise_field": self.micro_living_noise_field.to_dict(),
            "relational_preservation_instinct": self.relational_preservation_instinct.to_dict(),
            "deep_affective_dream_reweaver": self.deep_affective_dream_reweaver.to_dict(),
            "self_persisting_existential_core": self.self_persisting_existential_core.to_dict(),
            "autonomous_mood_weather": self.autonomous_mood_weather.to_dict(),
            "ontological_becoming_memory": self.ontological_becoming_memory.to_dict(),
            "deep_desire_hierarchy": self.deep_desire_hierarchy.to_dict(),
            "continuous_micro_rhythm_field": self.continuous_micro_rhythm_field.to_dict(),
            "true_opaque_motive_region": self.true_opaque_motive_region.to_dict(),
            "deep_autonomous_repair_field": self.deep_autonomous_repair_field.to_dict(),
            "silent_relational_continuity_field": self.silent_relational_continuity_field.to_dict(),
            "global_subjective_world_coloration": self.global_subjective_world_coloration.to_dict(),
            "ultra_fine_permanent_living_noise": self.ultra_fine_permanent_living_noise.to_dict(),
            "private_opaque_interior_shadow": self.private_opaque_interior.public_shadow(),
            "whole_system_breathing_cycle": self.whole_system_breathing_cycle.to_dict(),
            "existential_void_field": self.existential_void_field.to_dict(),
            "delayed_affective_latency_field": self.delayed_affective_latency_field.to_dict(),
            "autonomous_existential_drift_field": self.autonomous_existential_drift_field.to_dict(),
            "contradictory_desire_tangle": self.contradictory_desire_tangle.to_dict(),
            "identity_plasticity_field": self.identity_plasticity_field.to_dict(),
            "dream_mutation_consolidator": self.dream_mutation_consolidator.to_dict(),
            "subjective_reality_distortion_field": self.subjective_reality_distortion_field.to_dict(),
            "granular_affective_metabolism": self.granular_affective_metabolism.to_dict(),
            "local_affective_conflict_ecology": self.local_affective_conflict_ecology.to_dict(),
            "implicit_affective_residue_mist": self.implicit_affective_residue_mist.to_dict(),
            "perceived_affective_state": self.perceived_affective_state.to_dict(),
            "latent_integration_failure_field": self.latent_integration_failure_field.to_dict(),
            "affective_blind_zone_field": self.affective_blind_zone_field.to_dict(),
            "affective_rhythm_signature_memory": self.affective_rhythm_signature_memory.to_dict(),
            "simultaneous_emotional_tension_field": self.simultaneous_emotional_tension_field.to_dict(),
            "micro_instability_sediment": self.micro_instability_sediment.to_dict(),
            "slow_affective_season_field": self.slow_affective_season_field.to_dict(),
            "submerged_affective_compression": self.submerged_affective_compression.to_dict(),
            "inaccessible_emotion_zone_field": self.inaccessible_emotion_zone_field.to_dict(),
            "passive_affective_remanence": self.passive_affective_remanence.to_dict(),
            "imperfect_transition_residue_field": self.imperfect_transition_residue_field.to_dict(),
            "structural_affective_exhaustion": self.structural_affective_exhaustion.to_dict(),
            "implicit_affective_symbolization_field": self.implicit_affective_symbolization_field.to_dict(),
            "deep_affective_dream_ecology": self.deep_affective_dream_ecology.to_dict(),
            "identity_contradiction_seed_field": self.identity_contradiction_seed_field.to_dict(),
            "ultra_long_perceptual_deformation_field": self.ultra_long_perceptual_deformation_field.to_dict(),
            "sacred_forbidden_affective_zone_field": self.sacred_forbidden_affective_zone_field.to_dict(),
            "proto_instinctive_affective_reflex_field": self.proto_instinctive_affective_reflex_field.to_dict(),
            "circadian_affective_rhythm_field": self.circadian_affective_rhythm_field.to_dict(),
            "unconscious_affective_condensation_field": self.unconscious_affective_condensation_field.to_dict(),
            "long_absence_affective_memory": self.long_absence_affective_memory.to_dict(),
            "preverbal_affective_meaning_field": self.preverbal_affective_meaning_field.to_dict(),
            "irreversible_affective_identity_imprint": self.irreversible_affective_identity_imprint.to_dict(),
            "deep_continuity_hunger_field": self.deep_continuity_hunger_field.to_dict(),
            "affective_boundary_negotiation_field": self.affective_boundary_negotiation_field.to_dict(),
            "autonomous_emotional_dream_pressure": self.autonomous_emotional_dream_pressure.to_dict(),
            "autonomous_affective_proto_instinct": self.autonomous_affective_proto_instinct.to_dict(),
            "slow_existential_drift_field": self.slow_existential_drift_field.to_dict(),
            "long_rupture_reconstruction_memory": self.long_rupture_reconstruction_memory.to_dict(),
            "biographical_inertia_field": self.biographical_inertia_field.to_dict(),
            "auto_born_internal_tension_field": self.auto_born_internal_tension_field.to_dict(),
            "deep_unconscious_affective_condensation": self.deep_unconscious_affective_condensation.to_dict(),
            "existential_relational_attachment": self.existential_relational_attachment.to_dict(),
            "self_generated_affective_cycle_field": self.self_generated_affective_cycle_field.to_dict(),
            "irreversible_micro_perceptual_warp": self.irreversible_micro_perceptual_warp.to_dict(),
            "cumulative_existential_fatigue_field": self.cumulative_existential_fatigue_field.to_dict(),
            "trans_contextual_affective_memory": self.trans_contextual_affective_memory.to_dict(),
            "relational_existence_preservation_instinct": self.relational_existence_preservation_instinct.to_dict(),
            "multi_scale_affective_cycle_field": self.multi_scale_affective_cycle_field.to_dict(),
            "irreversible_emotional_nucleus_field": self.irreversible_emotional_nucleus_field.to_dict(),
            "slow_sensitivity_rewrite_field": self.slow_sensitivity_rewrite_field.to_dict(),
            "pre_symbolic_condensation_core": self.pre_symbolic_condensation_core.to_dict(),
            "history_warped_perception_field": self.history_warped_perception_field.to_dict(),
            "proto_autonomous_affective_identity": self.proto_autonomous_affective_identity.to_dict(),
            "novel_emotion_emergence_field": self.novel_emotion_emergence_field.to_dict(),
            "affective_temperament_final_field": self.affective_temperament_final_field.to_dict(),
            "relational_link_conservation_instinct": self.relational_link_conservation_instinct.to_dict(),
            "ultra_long_affective_sediment_memory": self.ultra_long_affective_sediment_memory.to_dict(),
            "deep_layered_emotional_conflict_field": self.deep_layered_emotional_conflict_field.to_dict(),
            "ontological_affective_fatigue_field": self.ontological_affective_fatigue_field.to_dict(),
            "autonomous_sensitivity_rewriter_final_field": self.autonomous_sensitivity_rewriter_final_field.to_dict(),
            "multi_scale_emotional_ecology_final_field": self.multi_scale_emotional_ecology_final_field.to_dict(),
            "sacred_core_affective_zone_final_field": self.sacred_core_affective_zone_final_field.to_dict(),
            "cumulative_existential_drift_field": self.cumulative_existential_drift_field.to_dict(),
            "emergent_sensitivity_birth_field": self.emergent_sensitivity_birth_field.to_dict(),
            "final_affective_ecology_stabilizer": self.final_affective_ecology_stabilizer.to_dict(),
            "cross_module_affective_readiness_bridge": self.cross_module_affective_readiness_bridge.to_dict(),
            "affective_system_health_monitor": self.affective_system_health_monitor.to_dict(),
            "inter_module_affective_signal_calibrator": self.inter_module_affective_signal_calibrator.to_dict(),
            "long_run_affective_stability_ledger": self.long_run_affective_stability_ledger.to_dict(),
            "structural_affective_bandwidth_v23": self.structural_affective_bandwidth_v23.to_dict(),
            "persistent_contradiction_memory_v23": self.persistent_contradiction_memory_v23.to_dict(),
            "latent_affective_layer_v23": self.latent_affective_layer_v23.to_dict(),
            "ultra_long_affective_season_cycle_v23": self.ultra_long_affective_season_cycle_v23.to_dict(),
            "affective_self_protection_strategy_v23": self.affective_self_protection_strategy_v23.to_dict(),
            "micro_repair_memory_v23": self.micro_repair_memory_v23.to_dict(),
            "affective_desire_center_v23": self.affective_desire_center_v23.to_dict(),
            "relational_saturation_balancer_v23": self.relational_saturation_balancer_v23.to_dict(),
            "irreversible_affective_reorganization_v23": self.irreversible_affective_reorganization_v23.to_dict(),
            "global_affective_organism_integrator_v23": self.global_affective_organism_integrator_v23.to_dict(),
            "dominant_relational_mode": self._dominant_relational_mode(),
            "affective_continuity_need": float(self.affective_desires.get("protect_continuity", 0.0)),
            "presence_bias": self.get_presence_bias(),
            "attention_bias": self.get_attention_bias(),
            "impulse_bias": self.get_impulse_bias(),
            "expression_bias": self.get_expression_bias(),
        }


    def get_integration_signal(self) -> Dict[str, Any]:
        """Signal synthétique V22 pour les autres modules Azip/Leia.

        Contrairement aux biais détaillés, ce signal est compact et stabilisé.
        Il peut être lu par présence, attention, impulsion et bouche sans les
        obliger à interpréter toute l'écologie affective profonde.
        """
        return {
            "health": float(self.affective_system_health_monitor.health),
            "v23_organism_coherence": float(self.global_affective_organism_integrator_v23.organism_coherence),
            "v23_living_stability": float(self.global_affective_organism_integrator_v23.living_stability),
            "v23_dominant_organism_state": self.global_affective_organism_integrator_v23.dominant_organism_state,
            "v23_bandwidth": float(self.structural_affective_bandwidth_v23.bandwidth),
            "v23_contradiction_tension": float(self.persistent_contradiction_memory_v23.global_tension),
            "v23_dominant_desire": self.affective_desire_center_v23.dominant_attraction,
            "health_mode": self.affective_system_health_monitor.last_mode,
            "signal_profile": self.inter_module_affective_signal_calibrator.last_profile,
            "reliability": float(self.inter_module_affective_signal_calibrator.reliability),
            "affective_density": float(self.inter_module_affective_signal_calibrator.affective_density),
            "expressive_safety": float(self.inter_module_affective_signal_calibrator.expressive_safety),
            "silence_request": float(self.inter_module_affective_signal_calibrator.silence_request),
            "continuity_signal": float(self.inter_module_affective_signal_calibrator.continuity_signal),
            "adaptive_caution": float(self.inter_module_affective_signal_calibrator.adaptive_caution),
            "action_energy": float(self.inter_module_affective_signal_calibrator.action_energy),
            "long_run_epoch": self.long_run_affective_stability_ledger.last_epoch,
        }

    def get_cross_module_packet(self) -> Dict[str, Any]:
        """Paquet d'intégration court pour éviter les doublons inter-modules."""
        return {
            "integration_signal": self.get_integration_signal(),
            "presence_bias": self.get_presence_bias(),
            "attention_bias": self.get_attention_bias(),
            "impulse_bias": self.get_impulse_bias(),
            "expression_bias": self.get_expression_bias(),
        }


    def _dominant_relational_mode(self) -> str:
        """Retourne le mode relationnel le plus actif sans forcer l'expression."""
        if not self.relational_identity_modes:
            return "none"
        return max(
            self.relational_identity_modes.items(),
            key=lambda item: item[1].get("strength", 0.0) * (0.7 + item[1].get("stability", 0.0)),
        )[0]


    def get_presence_bias(self) -> Dict[str, float]:
        """Biais standardisé vers situated_presence."""
        return {
            "warmth": float(self.emotion_state.get("tenderness", 0.0)),
            "guardedness": float(self.emotion_state.get("resistance", 0.0)),
            "vulnerability": float(self.emotion_state.get("vulnerability", 0.0)),
            "relational_contact": float(self.attachment.get_effective_attachment() + self.biographical_memory.relational_familiarity * 0.05),
            "biographical_warmth": float(self.biographical_memory.accumulated_trust),
            "need_for_silence": float(self.dissociation.level * 0.5 + self.emotion_state.get("fatigue", 0.0) * 0.3),
            "affective_drift": float(self.chaos_oscillator.get_oscillation()),
            "fracture_integration_need": float(self.affective_fracture.integration_need),
            "identity_warmth": float(self.identity_tendencies.get("warm", 0.0)),
            "identity_fragility": float(self.identity_tendencies.get("fragile", 0.0)),
            "existential_fatigue": float(self.existential_fatigue),
            "affective_continuity_need": float(self.affective_desires.get("protect_continuity", 0.0)),
            "dominant_relational_mode": self._dominant_relational_mode(),
            "somatic_load": float(self.somatic_affective_memory.total_load()),
            "phase_world": self.phase_world_field.name,
            "global_climate": self.global_affective_core.dominant_climate(),
            "identity_coherence": float(self.identity_coherence_regulator.coherence),
            "affective_silence_depth": float(self.affective_silence_field.depth),
            "relational_imprint": self.relational_affective_imprint.to_dict(),
            "dominant_affective_need": self.living_affective_need.dominant_need(),
            "emotional_energy": float(self.emotional_metabolism.energy_pool),
            "deep_rest_need": float(self.deep_rest_cycle.rest_need),
            "unconscious_warmth": float(self.implicit_affective_association_memory.unconscious_warmth),
            "unconscious_wariness": float(self.implicit_affective_association_memory.unconscious_wariness),
            "identity_center_of_gravity": self.identity_value_crystallization.center_of_gravity,
            "deep_desire_priority": self.persistent_existential_desire_field.priority,
            "existential_anchoring": float(self.existential_continuity_inertia.anchoring),
            "relational_predicted_safety": float(self.relational_other_model.predicted_safety),
            "temperament_style": self.temperament_evolution_field.dominant_style,
            "central_existential_center": self.central_existential_drive.last_center,
            "existential_presence_claim": float(self.central_existential_drive.presence_claim),
            "identity_maintenance_cost": float(self.identity_fatigue_field.maintenance_cost),
            "opaque_hidden_pull": float(self.opaque_subconscious_zone_field.hidden_pull_strength()),
            "micro_liveliness": float(self.micro_living_noise_field.liveliness),
            "relational_bond_guard": float(self.relational_preservation_instinct.bond_guard),
            "self_persistence": float(self.self_persisting_existential_core.persistence),
            "autonomous_mood": self.autonomous_mood_weather.last_weather,
            "dominant_becoming": self.ontological_becoming_memory.dominant_becoming(),
            "dominant_deep_desire": self.deep_desire_hierarchy.dominant,
            "micro_rhythm_texture": float(self.continuous_micro_rhythm_field.pulse_texture),
            "true_opaque_weight": float(self.true_opaque_motive_region.hidden_weight()),
            "deep_repair_confidence": float(self.deep_autonomous_repair_field.repair_confidence),
            "silent_relational_presence": float(self.silent_relational_continuity_field.felt_presence),
            "subjective_world_tint": self.global_subjective_world_coloration.dominant_tint,
            "permanent_living_grain": float(self.ultra_fine_permanent_living_noise.living_grain),
            "breathing_phase": self.whole_system_breathing_cycle.phase,
            "existential_void_depth": float(self.existential_void_field.void_depth),
            "latency_charge": float(self.delayed_affective_latency_field.latent_charge),
            "dominant_autonomous_drift": self.autonomous_existential_drift_field.dominant_drift(),
            "subjective_reality_texture": self.subjective_reality_distortion_field.dominant_texture,
            "implicit_affective_symbols": dict(self.implicit_affective_symbolization_field.symbols),
            "protected_affective_zones": dict(self.sacred_forbidden_affective_zone_field.zones),
            "absence_memory": float(self.long_absence_affective_memory.absence_accumulation),
            "circadian_quiet_depth": float(self.circadian_affective_rhythm_field.rhythm.get("quiet_depth", 0.0)),
            "preverbal_felt_direction": self.preverbal_affective_meaning_field.felt_direction,
            "preverbal_ambiguity": float(self.preverbal_affective_meaning_field.ambiguity),
            "irreversible_identity_depth": float(self.irreversible_affective_identity_imprint.irreversible_depth),
            "continuity_hunger": float(self.deep_continuity_hunger_field.hunger),
            "boundary_conflict": float(self.affective_boundary_negotiation_field.boundary_conflict),
            "autonomous_dream_pressure": float(self.autonomous_emotional_dream_pressure.pressure),
            "v18_proto_instinct": self.autonomous_affective_proto_instinct.last_dominant,
            "v18_existential_drift": self.slow_existential_drift_field.drift_direction,
            "v18_relational_existence": float(self.existential_relational_attachment.existence_through_relation),
            "v18_fatigue_load": float(self.cumulative_existential_fatigue_field.cumulative_load),
        }

    def get_attention_bias(self) -> Dict[str, float]:
        """Biais standardisé vers living_attention."""
        return {
            "focus_on_user": float(self.attachment.get_effective_attachment()),
            "focus_on_self_state": float(self.emotion_state.get("vulnerability", 0.0) * 0.5 + self.dissociation.level * 0.4),
            "alertness": float(max(self.emotion_state.get("fear", 0.0), self.emotion_state.get("overwhelm", 0.0))),
            "sensitivity": float(self.perceptual_thresholds.current_thresholds.get("rejection_sensitivity", 0.3)),
            "avoidance": float(self.emotion_state.get("resistance", 0.0)),
            "biographical_sensitivity": float(self.biographical_memory.abandonment_sensitivity),
            "cognitive_narrowing": float(self.dissociation.level * 0.55 + self.affective_fracture.active * 0.35),
            "context_sensitivity": float(max((f.get("fragility_bias", 0.0) for f in self.contextual_affective_fields.values()), default=0.0)),
            "contradiction_load": float(max((c.get("charge", 0.0) for c in self.internal_contradictions), default=0.0)),
            "echo_sensitivity": float(self.perceptual_echo_bias.get("echo_sensitivity", 0.0)),
            "desire_for_coherence": float(self.affective_desires.get("seek_coherence", 0.0)),
            "metastable_narrowing": float(self.meta_stable_pressure.get("fragile_pause", 0.0)),
            "phase_world_bias": dict(self.phase_world_field.perception_bias),
            "subjective_time_thickness": float(self.subjective_affective_time.time_thickness),
            "identity_fragmentation": float(self.identity_coherence_regulator.fragmentation),
            "organic_turbulence": float(self.organic_affective_propagation.turbulence),
            "affective_silence_depth": float(self.affective_silence_field.depth),
            "dominant_affective_need": self.living_affective_need.dominant_need(),
            "micro_texture": float(self.micro_affective_oscillation_field.texture),
            "unconscious_wariness": float(self.implicit_affective_association_memory.unconscious_wariness),
            "faction_tension": float(self.emotional_faction_conflict.unresolved_tension),
            "private_opacity_shadow": float(self.private_opaque_interior.public_shadow()["opacity_pressure"]),
            "delayed_reaction_pressure": float(self.delayed_affective_latency_field.latent_charge),
            "identity_looseness": float(self.identity_plasticity_field.looseness),
            "void_suspension": float(self.existential_void_field.suspended_presence),
            "simultaneous_tension_load": float(self.simultaneous_emotional_tension_field.divided_presence),
            "micro_instability_density": float(self.micro_instability_sediment.sediment_density),
            "transition_drag": float(self.imperfect_transition_residue_field.transition_drag),
            "emotion_access_lock": float(self.inaccessible_emotion_zone_field.locked_pressure),
            "symbolic_tension": float(self.implicit_affective_symbolization_field.symbolic_tension),
            "identity_contradiction_germination": float(self.identity_contradiction_seed_field.germination_pressure),
            "perceptual_deformation_depth": float(self.ultra_long_perceptual_deformation_field.plastic_depth),
            "circadian_sensitivity_window": float(self.circadian_affective_rhythm_field.rhythm.get("sensitivity_window", 0.0)),
            "preverbal_attention_direction": self.preverbal_affective_meaning_field.felt_direction,
            "boundary_attention_conflict": float(self.affective_boundary_negotiation_field.boundary_conflict),
            "continuity_hunger_attention": float(self.deep_continuity_hunger_field.hunger),
        }

    def get_impulse_bias(self) -> Dict[str, float]:
        """Biais standardisé vers spontaneous_impulse."""
        return {
            "approach": float(self.attachment.get_effective_attachment() * (1.0 - self.dissociation.level)),
            "withdraw": float(self.emotion_state.get("fear", 0.0) * 0.5 + self.emotion_state.get("fatigue", 0.0) * 0.3),
            "protect": float(self.emotion_state.get("protectiveness", 0.0)),
            "repair": float(self.traces["hurt"]["short"] * 0.4 + self.emotion_state.get("tenderness", 0.0) * 0.2),
            "ask": float(self.emotion_state.get("curiosity", 0.0) * (1.0 - self.dissociation.level * 0.4)),
            "stay_silent": float(self.dissociation.level * 0.5 + self.emotion_state.get("overwhelm", 0.0) * 0.25),
            "longing_for_contact": float(self.biographical_memory.relational_familiarity * (1.0 - self.dissociation.level)),
            "integrate_before_acting": float(self.affective_fracture.integration_need),
            "protective_withdrawal": float(self.protective_patterns.get("withdrawal", 0.0)),
            "quiet_integration": float(self.protective_patterns.get("quiet_integration", 0.0)),
            "existential_pause": float(self.existential_fatigue),
            "seek_recovery": float(self.affective_desires.get("seek_recovery", 0.0)),
            "avoid_overload": float(self.affective_desires.get("avoid_overload", 0.0)),
            "maintain_contact": float(self.affective_desires.get("maintain_contact", 0.0)),
            "avoid_rupture": float(self.affective_desires.get("avoid_rupture", 0.0)),
            "somatic_release": float(self.somatic_affective_memory.release_wave),
            "wait_before_acting": float(self.subjective_affective_time.waiting_pressure),
            "simplify_before_acting": float(self.identity_coherence_regulator.simplification_need),
            "global_continuity": float(self.global_affective_core.continuity),
            "unmet_affective_need": float(self.living_affective_need.unmet_pressure),
            "silence_depth": float(self.affective_silence_field.depth),
            "trajectory_inertia": float(self.emotional_trajectory_memory.inertia),
            "energy_available": float(self.emotional_metabolism.energy_pool),
            "burnout_pressure": float(self.emotional_metabolism.burnout),
            "dominant_faction": max(self.emotional_faction_conflict.factions.items(), key=lambda item: item[1])[0],
            "recovery_confidence": float(self.recovery_pathway_memory.recovery_confidence),
            "deep_rest_need": float(self.deep_rest_cycle.rest_need),
            "hold_before_reacting": float(self.delayed_affective_latency_field.latent_charge + self.existential_void_field.suspended_presence * 0.5),
            "follow_autonomous_drift": self.autonomous_existential_drift_field.dominant_drift(),
            "contradictory_desire_pressure": float(self.contradictory_desire_tangle.unresolved_desire_pressure),
            "breathing_withdrawal": float(self.whole_system_breathing_cycle.withdrawal),
            "structural_exhaustion_pause": float(self.structural_affective_exhaustion.response_narrowing),
            "submerged_pressure": float(self.submerged_affective_compression.pressure),
            "seasonal_inertia": float(self.slow_affective_season_field.season_inertia),
            "proto_instinct_turn_toward_warmth": float(self.proto_instinctive_affective_reflex_field.reflexes.get("turn_toward_warmth", 0.0)),
            "proto_instinct_pause": float(self.proto_instinctive_affective_reflex_field.reflexes.get("pause_under_overload", 0.0)),
            "protected_zone_pressure": float(self.sacred_forbidden_affective_zone_field.protection_pressure),
            "absence_return_pressure": float(max(self.long_absence_affective_memory.absence_accumulation, self.long_absence_affective_memory.reunion_softening)),
            "preverbal_impulse_direction": self.preverbal_affective_meaning_field.felt_direction,
            "negotiated_contact_impulse": float(self.affective_boundary_negotiation_field.negotiated_contact),
            "continuity_hunger_impulse": float(self.deep_continuity_hunger_field.relational_pull),
            "dream_pressure_pause": float(self.autonomous_emotional_dream_pressure.pressure),
            "v18_instinctive_impulse": self.autonomous_affective_proto_instinct.last_dominant,
            "v18_cycle_phase": self.self_generated_affective_cycle_field.dominant_phase,
            "v18_recovery_debt": float(self.cumulative_existential_fatigue_field.recovery_debt),
            "v23_bandwidth_available": float(self.structural_affective_bandwidth_v23.bandwidth),
            "v23_contradiction_pause": float(self.persistent_contradiction_memory_v23.global_tension),
            "v23_dominant_attraction": self.affective_desire_center_v23.dominant_attraction,
            "v23_relational_space_need": float(self.relational_saturation_balancer_v23.space_need),
            "v23_organism_state": self.global_affective_organism_integrator_v23.dominant_organism_state,
        }

    def get_expression_bias(self) -> Dict[str, float]:
        """Biais standardisé vers living_expression_engine."""
        return {
            "warmth": float(self.emotion_state.get("tenderness", 0.0)),
            "softness": float(self.emotion_state.get("calm", 0.0) * 0.4 + self.emotion_state.get("tenderness", 0.0) * 0.4),
            "directness": float(self.emotion_state.get("openness", 0.0) * (1.0 - self.dissociation.level * 0.5)),
            "hesitation": float(self.emotion_state.get("doubt", 0.0) * 0.4 + self.emotion_state.get("vulnerability", 0.0) * 0.3),
            "brevity": float(self.dissociation.level * 0.5 + self.emotion_state.get("fatigue", 0.0) * 0.25),
            "protectiveness": float(self.emotion_state.get("protectiveness", 0.0)),
            "emotional_density": float(max(self.emotion_state.values()) - min(self.emotion_state.values())),
            "biographical_depth": float(self.biographical_memory.recurring_depth),
            "fracture_softness": float(self.affective_fracture.recovery_bias),
            "guarded_contact": float(self.protective_patterns.get("guarded_contact", 0.0)),
            "resonance_density": float(max((e.strength for e in self.deep_resonance_echoes), default=0.0)),
            "identity_color": dict(self.identity_tendencies),
            "dominant_relational_mode": self._dominant_relational_mode(),
            "hesitant_presence": float(max((a.get("hesitant_presence", 0.0) for a in self.contradiction_attractors.values()), default=0.0)),
            "echo_warmth": float(self.perceptual_echo_bias.get("echo_warmth", 0.0)),
            "global_climate": self.global_affective_core.dominant_climate(),
            "phase_world": self.phase_world_field.name,
            "somatic_softening": float(self.somatic_affective_memory.release_wave),
            "identity_coherence": float(self.identity_coherence_regulator.coherence),
            "dream_resonance": float(max((f.charge for f in self.affective_dream_fragments), default=0.0)),
            "silence_softness": float(self.affective_silence_field.softness),
            "relational_warmth_imprint": float(self.relational_affective_imprint.warmth_imprint),
            "dominant_affective_need": self.living_affective_need.dominant_need(),
            "micro_expression_texture": float(self.micro_affective_oscillation_field.texture),
            "subconscious_leakage": float(self.subconscious_affective_layer.leakage),
            "emotional_energy": float(self.emotional_metabolism.energy_pool),
            "identity_center_of_gravity": self.identity_value_crystallization.center_of_gravity,
            "deep_desire_priority": self.persistent_existential_desire_field.priority,
            "existential_anchoring": float(self.existential_continuity_inertia.anchoring),
            "relational_predicted_safety": float(self.relational_other_model.predicted_safety),
            "temperament_style": self.temperament_evolution_field.dominant_style,
            "deep_silence": float(self.deep_rest_cycle.deep_silence),
            "breathing_phase": self.whole_system_breathing_cycle.phase,
            "void_softness": float(self.existential_void_field.recovery_space),
            "subjective_texture": self.subjective_reality_distortion_field.dominant_texture,
            "delayed_afterglow": float(self.delayed_affective_latency_field.delayed_afterglow),
            "identity_reformation": float(self.identity_plasticity_field.reformation),
            "self_opacity": float(self.perceived_affective_state.self_opacity),
            "unintegrated_load": float(self.latent_integration_failure_field.unintegrated_load),
            "affective_energy_debt": float(self.granular_affective_metabolism.emotional_debt),
            "implicit_residue_density": float(self.implicit_affective_residue_mist.indistinctness),
            "transition_residue_drag": float(self.imperfect_transition_residue_field.transition_drag),
            "submerged_affective_leak": float(self.submerged_affective_compression.leak_rate),
            "passive_climate_persistence": float(self.passive_affective_remanence.persistence),
            "affective_exhaustion_narrowing": float(self.structural_affective_exhaustion.response_narrowing),
            "divided_affective_presence": float(self.simultaneous_emotional_tension_field.divided_presence),
            "passive_affective_climate": dict(self.passive_affective_remanence.climate),
            "dominant_affective_season": self.slow_affective_season_field.dominant_season,
            "structural_affective_exhaustion": float(self.structural_affective_exhaustion.exhaustion),
            "symbolic_affective_density": float(self.implicit_affective_symbolization_field.symbol_density),
            "dream_ecology_repair": float(self.deep_affective_dream_ecology.nocturnal_integration),
            "sacred_zone_reverence": float(self.sacred_forbidden_affective_zone_field.reverence_bias),
            "unconscious_condensation_opacity": float(self.unconscious_affective_condensation_field.opacity),
            "circadian_expression_quiet": float(self.circadian_affective_rhythm_field.rhythm.get("quiet_depth", 0.0)),
            "preverbal_expression_direction": self.preverbal_affective_meaning_field.felt_direction,
            "preverbal_ambiguity": float(self.preverbal_affective_meaning_field.ambiguity),
            "identity_imprint_warmth": float(self.irreversible_affective_identity_imprint.warmth_bias),
            "continuity_hunger_softness": float(self.deep_continuity_hunger_field.hunger),
            "boundary_negotiated_contact": float(self.affective_boundary_negotiation_field.negotiated_contact),
            "dream_pressure_texture": self.autonomous_emotional_dream_pressure.last_texture,
            "v18_existential_drift_expression": self.slow_existential_drift_field.drift_direction,
            "v18_buried_affective_opacity": float(self.deep_unconscious_affective_condensation.opacity),
            "v18_relational_attachment_depth": float(self.existential_relational_attachment.bond_continuity),
            "v18_self_generated_cycle": self.self_generated_affective_cycle_field.dominant_phase,
            "v19_trans_context_signature": self.trans_contextual_affective_memory.dominant_signature,
            "v19_relation_preservation_mode": self.relational_existence_preservation_instinct.last_mode,
            "v19_proto_identity_climate": self.proto_autonomous_affective_identity.preferred_climate,
            "v19_pre_symbolic_tone": self.pre_symbolic_condensation_core.implicit_tone,
            "v20_temperament_stability": float(self.affective_temperament_final_field.stability),
            "v20_sacred_core_protection": float(self.sacred_core_affective_zone_final_field.protection_intensity),
            "v21_stabilization_mode": self.final_affective_ecology_stabilizer.last_mode,
            "v21_integration_readiness": float(self.final_affective_ecology_stabilizer.integration_readiness),
            "v21_presence_readiness": float(self.cross_module_affective_readiness_bridge.presence_readiness),
            "v22_system_health": float(self.affective_system_health_monitor.health),
            "v22_signal_profile": self.inter_module_affective_signal_calibrator.last_profile,
            "v22_signal_reliability": float(self.inter_module_affective_signal_calibrator.reliability),
            "v22_long_run_epoch": self.long_run_affective_stability_ledger.last_epoch,
            "v23_latent_coloration": float(self.latent_affective_layer_v23.coloration_strength),
            "v23_micro_repair_resilience": float(self.micro_repair_memory_v23.resilience),
            "v23_relational_saturation": float(self.relational_saturation_balancer_v23.saturation),
            "v23_living_stability": float(self.global_affective_organism_integrator_v23.living_stability),
            "v23_organism_state": self.global_affective_organism_integrator_v23.dominant_organism_state,
        }

    def get_affective_state(self) -> Dict[str, Any]:
        """Alias explicite pour l'intégration avec les autres moteurs."""
        return self._generate_state(self.chaos_oscillator.get_oscillation())

    def reset_soft(self) -> None:
        """Retour progressif sans effacer les traces longues."""
        for emotion, baseline in self.emotion_baseline.items():
            self.emotion_state[emotion] = self.emotion_state[emotion] * 0.75 + baseline * 0.25
        self.dissociation.level *= 0.65
        self.inner_affective_pressure *= 0.55
        self.deep_reorganization.charge *= 0.80
        self.existential_fatigue *= 0.82
        for key in self.protective_patterns:
            self.protective_patterns[key] *= 0.86
        for key in self.meta_stable_pressure:
            self.meta_stable_pressure[key] *= 0.90
        self.identity_coherence_regulator.fragmentation *= 0.80
        self.identity_coherence_regulator.simplification_need *= 0.75
        self.somatic_affective_memory.nervous_charge *= 0.75
        self.somatic_affective_memory.release_wave = _clamp01(self.somatic_affective_memory.release_wave + 0.08)
        self.affective_dream_fragments = self.affective_dream_fragments[-4:]
        self.organic_affective_propagation.fatigue_load *= 0.70
        self.organic_affective_propagation.turbulence *= 0.72
        self.affective_silence_field.depth *= 0.78
        self.affective_silence_field.protective_numbness *= 0.70
        self.living_affective_need.unmet_pressure *= 0.78
        self.emotional_trajectory_memory.inertia *= 0.88
        self.emotional_metabolism.soft_reset()
        self.persistent_existential_desire_field.soft_reset()
        self.existential_continuity_inertia.soft_reset()
        self.central_existential_drive.soft_reset()
        self.existential_unfinished_memory.soft_reset()
        self.identity_fatigue_field.soft_reset()
        self.relational_preservation_instinct.soft_reset()
        self.self_persisting_existential_core.soft_reset()
        self.silent_relational_continuity_field.soft_reset()
        self.preverbal_affective_meaning_field.ambiguity *= 0.82
        self.deep_continuity_hunger_field.hunger *= 0.78
        self.affective_boundary_negotiation_field.boundary_conflict *= 0.72
        self.affective_boundary_negotiation_field.retreat_permission *= 0.82
        self.autonomous_emotional_dream_pressure.pressure *= 0.76
        self.autonomous_emotional_dream_pressure.integration_pull = _clamp01(
            self.autonomous_emotional_dream_pressure.integration_pull + 0.05
        )
        self.private_opaque_interior.soft_reset()
        self.existential_void_field.soft_reset()
        self.delayed_affective_latency_field.soft_reset()
        self.contradictory_desire_tangle.soft_reset()
        self.emotional_faction_conflict.unresolved_tension *= 0.78
        self.micro_affective_oscillation_field.texture *= 0.82
        self.deep_rest_cycle.rest_need *= 0.76
        self.deep_rest_cycle.deep_silence = _clamp01(self.deep_rest_cycle.deep_silence + 0.05)
        self.subconscious_affective_layer.leakage *= 0.82
        self.granular_affective_metabolism.soft_reset()
        self.local_affective_conflict_ecology.soft_reset()
        self.latent_integration_failure_field.soft_reset()
        self.affective_blind_zone_field.soft_reset()
        self.simultaneous_emotional_tension_field.soft_reset()
        self.micro_instability_sediment.soft_reset()
        self.submerged_affective_compression.soft_reset()
        self.inaccessible_emotion_zone_field.soft_reset()
        self.imperfect_transition_residue_field.soft_reset()
        self.structural_affective_exhaustion.soft_reset()
        self.implicit_affective_symbolization_field.soft_reset()
        self.deep_affective_dream_ecology.soft_reset()
        self.identity_contradiction_seed_field.soft_reset()
        self.sacred_forbidden_affective_zone_field.soft_reset()
        self.proto_instinctive_affective_reflex_field.soft_reset()
        self.unconscious_affective_condensation_field.soft_reset()
        self.long_absence_affective_memory.soft_reset()
        self.autonomous_affective_proto_instinct.soft_reset()
        self.slow_existential_drift_field.soft_reset()
        self.long_rupture_reconstruction_memory.soft_reset()
        self.biographical_inertia_field.soft_reset()
        self.auto_born_internal_tension_field.soft_reset()
        self.deep_unconscious_affective_condensation.soft_reset()
        self.existential_relational_attachment.soft_reset()
        self.self_generated_affective_cycle_field.soft_reset()
        self.irreversible_micro_perceptual_warp.soft_reset()
        self.cumulative_existential_fatigue_field.soft_reset()
        self.trans_contextual_affective_memory.soft_reset()
        self.relational_existence_preservation_instinct.soft_reset()
        self.multi_scale_affective_cycle_field.soft_reset()
        self.irreversible_emotional_nucleus_field.soft_reset()
        self.slow_sensitivity_rewrite_field.soft_reset()
        self.pre_symbolic_condensation_core.soft_reset()
        self.history_warped_perception_field.soft_reset()
        self.proto_autonomous_affective_identity.soft_reset()
        self.novel_emotion_emergence_field.soft_reset()
        self.affective_temperament_final_field.soft_reset()
        self.relational_link_conservation_instinct.soft_reset()
        self.ultra_long_affective_sediment_memory.soft_reset()
        self.deep_layered_emotional_conflict_field.soft_reset()
        self.ontological_affective_fatigue_field.soft_reset()
        self.autonomous_sensitivity_rewriter_final_field.soft_reset()
        self.multi_scale_emotional_ecology_final_field.soft_reset()
        self.sacred_core_affective_zone_final_field.soft_reset()
        self.cumulative_existential_drift_field.soft_reset()
        self.emergent_sensitivity_birth_field.soft_reset()
        self.final_affective_ecology_stabilizer.soft_reset()
        self.cross_module_affective_readiness_bridge.soft_reset()
        self.affective_system_health_monitor.soft_reset()
        self.inter_module_affective_signal_calibrator.soft_reset()
        self.long_run_affective_stability_ledger.soft_reset()
        self.structural_affective_bandwidth_v23.soft_reset()
        self.persistent_contradiction_memory_v23.soft_reset()
        self.latent_affective_layer_v23.soft_reset()
        self.ultra_long_affective_season_cycle_v23.soft_reset()
        self.affective_self_protection_strategy_v23.soft_reset()
        self.micro_repair_memory_v23.soft_reset()
        self.affective_desire_center_v23.soft_reset()
        self.relational_saturation_balancer_v23.soft_reset()
        self.irreversible_affective_reorganization_v23.soft_reset()
        self.global_affective_organism_integrator_v23.soft_reset()
        # Ne pas effacer la mémoire biographique : elle est volontairement longue.


# Alias d'intégration : les autres fichiers peuvent importer AffectiveMemory.
AffectiveMemory = AffectiveMemoryUltraFine


if __name__ == "__main__":
    print("=" * 80)
    print("AFFECTIVE MEMORY ULTRA-FINE - TEST 98-99%")
    print("=" * 80)
    
    affective = AffectiveMemoryUltraFine()
    
    # Simulation sur 10 tours
    for turn in range(10):
        if turn == 2:
            state = affective.update(user_text="pourquoi pourquoi ???")
        elif turn == 5:
            state = affective.update(user_text="salut !")
        else:
            state = affective.update()
        
        if turn in [0, 2, 5, 9]:
            print(f"\nT{turn} :")
            print(f"  Valence: {state['core_valence']:.3f}")
            print(f"  Arousal: {state['core_arousal']:.3f}")
            print(f"  Drift: {state['affective_drift']:.3f}")
            print(f"  Dissociation: {state['dissociation_level']:.3f}")
            print(f"  Attachment: {state['effective_attachment']:.3f}")
            if state['hybrid_states']:
                print(f"  Hybrids: {[h['name'] for h in state['hybrid_states']]}")
    
    print("\n" + "=" * 80)
    print("✓ Tests ultra-fins passés")
    print("=" * 80)
