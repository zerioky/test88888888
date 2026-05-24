# -*- coding: utf-8 -*-
"""
global_workspace.py — Champ Conscient Global de Leia V20
═════════════════════════════════════════════════════════════════════════════
Pure Python stdlib. Zéro dépendance.

C'est le cerveau vivant unifié de Leia.
TOUS les modules lisent ici. TOUS les modules écrivent ici.
Ce fichier remplace la fragmentation : plus de "moteurs parallèles".

Ce que ce workspace fait vraiment :

1. COMPÉTITION ATTENTIONNELLE
   Les pensées luttent pour occuper le champ conscient.
   La plus forte domine. Les autres s'affaiblissent ou persistent en arrière-plan.

2. CONTAMINATION ÉMOTIONNELLE
   Une pensée triste change la tonalité de tout ce qui suit.
   Une surprise réoriente l'attention. Une tension bloque le flux.

3. PROPAGATION ASSOCIATIVE
   liberté → responsabilité → solitude → peur
   Sans règles fixes : par activation diffuse dans le graphe conceptuel.

4. PERSISTANCE COGNITIVE
   Certaines pensées reviennent, obsèdent, influencent pendant des échanges.
   Le workspace a une inertie réelle.

5. ÉVOLUTION DE FOND
   Entre les messages, le workspace continue de vivre :
   décroissance, consolidation, émergence spontanée, dérive.

6. ÉNERGIE COGNITIVE LIMITÉE
   L'attention n'est pas infinie. Saturation, fatigue, récupération.

Usage :
    from global_workspace import workspace

    # Après analyse d'un message
    workspace.inject_perception(signal_nlp, charge_emotionnelle=0.3)

    # Lire l'état courant
    etat = workspace.snapshot()
    pensee_dom = workspace.pensee_dominante()
    pression = workspace.pression_expressive()

    # Évolution de fond (appelé par background_life_thread)
    workspace.tick(elapsed_seconds=2.0)
"""

from __future__ import annotations

import json
import math
import random
import re
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


# ─────────────────────────────────────────────────────────────────────────────
# Utilitaires
# ─────────────────────────────────────────────────────────────────────────────

def _c(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f)) if not (math.isnan(f) or math.isinf(f)) else lo
    except Exception:
        return lo


def _decay(val: float, elapsed: float, demi_vie: float) -> float:
    return val * math.exp(-elapsed / demi_vie * math.log(2))


# ═══════════════════════════════════════════════════════════════════════════════
# I. PENSÉE ACTIVE — unité de base du workspace
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PenseeActive:
    """
    Une pensée vivante dans le champ conscient.

    Une pensée n'est pas un texte.
    C'est une activation cognitive avec poids, émotion, persistance.
    """
    # Identité
    id: str
    contenu: str              # résumé court (≤80 chars), jamais préécrit
    concepts: List[str]       # concepts portés par cette pensée

    # Dynamique
    poids: float = 0.5        # force actuelle [0-1]
    charge_emotionnelle: float = 0.0   # -1 négatif → +1 positif
    tension: float = 0.0      # opposition interne [0-1]
    urgence: float = 0.0      # 0 banal → 1 urgent
    nouveaute: float = 0.0    # 0 familier → 1 nouveau
    resonance: float = 0.0    # lien avec mémoire existante [0-1]

    # Temporel
    nee_a: float = field(default_factory=time.time)
    derniere_activation: float = field(default_factory=time.time)
    n_activations: int = 0
    demi_vie: float = 120.0   # secondes avant de perdre la moitié du poids

    # Persistance
    persistante: bool = False   # obsède, revient
    resolue: bool = False       # pensée terminée
    source: str = ""            # "dialogue", "lecture", "interne", "association"

    def activer(self, force: float, emotion: float = 0.0) -> None:
        self.poids = _c(self.poids + force * (1.0 - self.poids * 0.3))
        if emotion != 0.0:
            alpha = 0.25
            self.charge_emotionnelle = _c(
                (1 - alpha) * self.charge_emotionnelle + alpha * emotion,
                -1.0, 1.0
            )
        self.derniere_activation = time.time()
        self.n_activations += 1

    def decay_step(self, elapsed: float) -> None:
        if self.persistante:
            # Les pensées persistantes décroissent 5× plus lentement
            self.poids = _c(_decay(self.poids, elapsed, self.demi_vie * 5))
        else:
            self.poids = _c(_decay(self.poids, elapsed, self.demi_vie))
        # La charge émotionnelle décroît plus lentement que le poids
        self.charge_emotionnelle = _c(
            _decay(abs(self.charge_emotionnelle), elapsed, self.demi_vie * 2)
            * (1 if self.charge_emotionnelle >= 0 else -1),
            -1.0, 1.0
        )

    def est_active(self, seuil: float = 0.08) -> bool:
        return self.poids >= seuil and not self.resolue

    def age_secondes(self) -> float:
        return time.time() - self.nee_a

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "contenu": self.contenu[:60],
            "concepts": self.concepts[:5],
            "poids": round(self.poids, 3),
            "charge_emotionnelle": round(self.charge_emotionnelle, 3),
            "tension": round(self.tension, 3),
            "urgence": round(self.urgence, 3),
            "nouveaute": round(self.nouveaute, 3),
            "resonance": round(self.resonance, 3),
            "n_activations": self.n_activations,
            "source": self.source,
            "persistante": self.persistante,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# II. CHAMP ÉMOTIONNEL — climat affectif persistant
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ChampEmotionnel:
    """
    Le climat émotionnel actuel de Leia.

    Il ne contient pas une émotion unique.
    Il est un champ multidimensionnel qui se contamine, persiste, dérive.
    Compatible avec EmotionalState de leia_living_core.
    """
    # Dimensions principales
    valence: float = 0.0        # -1 négatif → +1 positif
    arousal: float = 0.3        # 0 calme → 1 intense
    tension: float = 0.0        # conflit interne
    resonance: float = 0.0      # connexion avec l'interlocuteur
    ouverture: float = 0.6      # réceptivité cognitive
    fatigue: float = 0.0        # épuisement cognitif
    surprise_accumlee: float = 0.0   # nouveauté accumulée

    # Traces résiduelles (inertie émotionnelle)
    _trace_valence: deque = field(default_factory=lambda: deque(maxlen=8))
    _trace_tension: deque = field(default_factory=lambda: deque(maxlen=8))

    def contaminer(self, valence: float, arousal: float = 0.0,
                   tension: float = 0.0, force: float = 0.25) -> None:
        """
        Contamine le champ émotionnel avec une nouvelle émotion.
        Force = 0.25 par défaut = inertie forte (les émotions ne changent pas d'un coup).
        """
        # Inertie : les émotions résistent au changement
        self.valence = _c(
            (1 - force) * self.valence + force * valence,
            -1.0, 1.0
        )
        self.arousal = _c((1 - force * 0.5) * self.arousal + force * 0.5 * arousal)
        self.tension = _c((1 - force * 0.4) * self.tension + force * 0.4 * tension)

        # Accumulation
        if abs(tension) > 0.3:
            self.fatigue = _c(self.fatigue + tension * 0.04)
        if arousal > 0.6:
            self.fatigue = _c(self.fatigue + (arousal - 0.6) * 0.03)

        self._trace_valence.append(round(valence, 3))
        self._trace_tension.append(round(tension, 3))

    def tick(self, elapsed: float) -> None:
        """Évolution naturelle du champ émotionnel dans le temps."""
        # Retour vers la neutralité (régulation homéostatique)
        eq_val    = 0.0    # valence d'équilibre : neutre
        eq_arousal = 0.3   # arousal d'équilibre : légèrement présent
        eq_tension = 0.0
        eq_ouv    = 0.6

        rate = _c(elapsed / 30.0, 0.01, 0.8)  # max 80% de retour par tick

        self.valence  = _c(self.valence + (eq_val - self.valence) * rate * 0.15, -1.0, 1.0)
        self.arousal  = _c(self.arousal + (eq_arousal - self.arousal) * rate * 0.12)
        self.tension  = _c(self.tension + (eq_tension - self.tension) * rate * 0.10)
        self.ouverture = _c(self.ouverture + (eq_ouv - self.ouverture) * rate * 0.08)
        self.resonance = _c(self.resonance * (1 - rate * 0.20))
        self.fatigue   = _c(self.fatigue * (1 - rate * 0.05))  # fatigue lente à partir

    def tonalite(self) -> str:
        """Tonalité émotionnelle qualitative courante."""
        if self.fatigue > 0.7:
            return "épuisée"
        if self.tension > 0.6:
            return "tendue"
        if self.valence > 0.5 and self.arousal > 0.5:
            return "vive"
        if self.valence > 0.3:
            return "ouverte"
        if self.valence < -0.4:
            return "sombre"
        if self.valence < -0.2:
            return "mélancolique"
        if self.arousal < 0.2:
            return "calme"
        return "neutre"

    def propagation_vers_attention(self) -> Dict[str, float]:
        """
        Influence du champ émotionnel sur l'attention.
        Compatible avec le système d'attention de leia_living_core.
        """
        return {
            "biais_attentionnel":  round(self.resonance * 0.3 - self.fatigue * 0.2, 4),
            "saturation":          round(self.fatigue * 0.6 + self.tension * 0.3, 4),
            "ouverture_cognitive": round(self.ouverture * (1 - self.fatigue * 0.5), 4),
            "urgence_expressive":  round(self.arousal * 0.4 + abs(self.valence) * 0.3, 4),
            "inhibition":          round(self.fatigue * 0.5 + self.tension * 0.4, 4),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "valence":            round(self.valence, 4),
            "arousal":            round(self.arousal, 4),
            "tension":            round(self.tension, 4),
            "resonance":          round(self.resonance, 4),
            "ouverture":          round(self.ouverture, 4),
            "fatigue":            round(self.fatigue, 4),
            "surprise_accumlee":  round(self.surprise_accumlee, 4),
            "tonalite":           self.tonalite(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# III. PROPAGATION ASSOCIATIVE — les idées se contaminent mutuellement
# ═══════════════════════════════════════════════════════════════════════════════

# Réseau d'associations conceptuelles fixes (seed)
# Ces associations sont le "patrimoine sémantique" initial de Leia.
# Elles seront enrichies dynamiquement par le graphe conceptuel vivant.
_ASSOCIATIONS_SEED: Dict[str, List[Tuple[str, float]]] = {
    "liberté":       [("responsabilité", 0.8), ("solitude", 0.5), ("contrainte", 0.7),
                      ("choix", 0.9), ("autonomie", 0.8), ("peur", 0.3)],
    "mémoire":       [("temps", 0.9), ("oubli", 0.8), ("identité", 0.7),
                      ("passé", 0.9), ("souvenir", 0.9), ("continuité", 0.7)],
    "conscience":    [("temps", 0.7), ("identité", 0.8), ("perception", 0.7),
                      ("présence", 0.8), ("existence", 0.9), ("doute", 0.5)],
    "temps":         [("durée", 0.9), ("mémoire", 0.8), ("présent", 0.9),
                      ("passé", 0.8), ("futur", 0.8), ("mort", 0.4)],
    "identité":      [("conscience", 0.8), ("mémoire", 0.7), ("continuité", 0.8),
                      ("différence", 0.6), ("autre", 0.5), ("soi", 0.9)],
    "mort":          [("vie", 0.9), ("peur", 0.8), ("temps", 0.7),
                      ("sens", 0.6), ("néant", 0.7), ("deuil", 0.6)],
    "vie":           [("mort", 0.9), ("sens", 0.7), ("présence", 0.8),
                      ("joie", 0.6), ("souffrance", 0.5), ("mouvement", 0.6)],
    "amour":         [("attachement", 0.9), ("peur", 0.5), ("solitude", 0.6),
                      ("joie", 0.8), ("souffrance", 0.6), ("présence", 0.7)],
    "peur":          [("danger", 0.8), ("anxiété", 0.9), ("fuite", 0.7),
                      ("protection", 0.7), ("mort", 0.6), ("liberté", 0.4)],
    "vérité":        [("mensonge", 0.9), ("réalité", 0.8), ("illusion", 0.7),
                      ("certitude", 0.7), ("doute", 0.7), ("connaissance", 0.8)],
    "langage":       [("pensée", 0.8), ("sens", 0.9), ("communication", 0.9),
                      ("silence", 0.6), ("expression", 0.8), ("vérité", 0.5)],
    "raison":        [("émotion", 0.7), ("logique", 0.9), ("intuition", 0.6),
                      ("doute", 0.7), ("vérité", 0.8), ("connaissance", 0.8)],
    "émotion":       [("raison", 0.7), ("corps", 0.8), ("sensation", 0.8),
                      ("intuition", 0.7), ("expression", 0.7), ("mémoire", 0.5)],
    "existence":     [("essence", 0.9), ("présence", 0.8), ("néant", 0.7),
                      ("sens", 0.8), ("conscience", 0.8), ("mort", 0.6)],
    "sens":          [("absurde", 0.8), ("valeur", 0.8), ("direction", 0.7),
                      ("vie", 0.9), ("vérité", 0.7), ("langage", 0.6)],
    "autre":         [("soi", 0.9), ("relation", 0.8), ("empathie", 0.7),
                      ("différence", 0.8), ("solitude", 0.6), ("amour", 0.5)],
    "corps":         [("esprit", 0.8), ("sensation", 0.9), ("présence", 0.7),
                      ("mort", 0.5), ("mouvement", 0.8), ("émotion", 0.7)],
    "connaissance":  [("ignorance", 0.9), ("vérité", 0.8), ("raison", 0.8),
                      ("doute", 0.7), ("apprentissage", 0.8), ("mémoire", 0.6)],
    "silence":       [("parole", 0.9), ("présence", 0.7), ("vide", 0.6),
                      ("attente", 0.7), ("réflexion", 0.8), ("langage", 0.6)],
    "doute":         [("certitude", 0.9), ("vérité", 0.8), ("anxiété", 0.6),
                      ("raison", 0.7), ("question", 0.8), ("connaissance", 0.7)],
}


class PropagationAssociative:
    """
    Propagation d'activation dans le réseau conceptuel.

    Quand un concept s'active, il réveille ses voisins avec une force décroissante.
    Pas de règles fixes — la propagation est pondérée et limitée en profondeur.
    """

    def __init__(self):
        # Réseau enrichi dynamiquement
        self._reseau: Dict[str, List[Tuple[str, float]]] = dict(_ASSOCIATIONS_SEED)
        # Niveaux d'activation courants
        self._activations: Dict[str, float] = {}
        # Historique des activations récentes
        self._historique: deque = deque(maxlen=100)

    def apprendre_lien(self, concept_a: str, concept_b: str,
                       force: float = 0.4, bidirectionnel: bool = True) -> None:
        """Enrichit le réseau associatif avec un nouveau lien."""
        a, b = concept_a.lower(), concept_b.lower()
        if a not in self._reseau:
            self._reseau[a] = []
        # Vérifie si le lien existe déjà
        for i, (c, f) in enumerate(self._reseau[a]):
            if c == b:
                self._reseau[a][i] = (b, min(1.0, f + 0.05))
                return
        self._reseau[a].append((b, _c(force)))
        if bidirectionnel:
            self.apprendre_lien(b, a, force * 0.85, bidirectionnel=False)

    def propager(self, concepts_source: List[str],
                 force_initiale: float = 0.6,
                 profondeur: int = 3,
                 seuil: float = 0.1) -> Dict[str, float]:
        """
        Propage l'activation depuis les concepts sources.
        Retourne le dict concept → niveau d'activation résultant.
        """
        activations: Dict[str, float] = {}

        # Activation initiale des sources
        for c in concepts_source:
            cl = c.lower()
            activations[cl] = _c(activations.get(cl, 0.0) + force_initiale)

        # Propagation en vagues (BFS pondéré)
        couche_courante = {cl: force_initiale for cl in
                           [c.lower() for c in concepts_source]}

        for profondeur_actuelle in range(profondeur):
            decay_profondeur = 0.5 ** (profondeur_actuelle + 1)
            prochaine_couche: Dict[str, float] = {}

            for concept, activation in couche_courante.items():
                voisins = self._reseau.get(concept, [])
                for voisin, poids_lien in voisins:
                    force_propagee = activation * poids_lien * decay_profondeur
                    if force_propagee < seuil:
                        continue
                    if voisin not in concepts_source:  # ne pas réactiver les sources
                        prochaine_couche[voisin] = max(
                            prochaine_couche.get(voisin, 0.0),
                            force_propagee
                        )
                        activations[voisin] = _c(
                            activations.get(voisin, 0.0) + force_propagee * 0.5
                        )

            couche_courante = {k: v for k, v in prochaine_couche.items()
                               if v >= seuil}
            if not couche_courante:
                break

        # Mise à jour des activations internes
        for c, a in activations.items():
            self._activations[c] = _c(
                max(self._activations.get(c, 0.0), a)
            )

        self._historique.append({
            "at": time.time(),
            "sources": concepts_source[:5],
            "activations": {k: round(v, 3) for k, v in
                            sorted(activations.items(), key=lambda x: -x[1])[:8]},
        })

        return activations

    def concepts_actives(self, seuil: float = 0.15, n: int = 10) -> List[Tuple[str, float]]:
        """Retourne les N concepts les plus activés actuellement."""
        actifs = [(c, a) for c, a in self._activations.items() if a >= seuil]
        return sorted(actifs, key=lambda x: -x[1])[:n]

    def tick(self, elapsed: float) -> None:
        """Décroissance des activations avec le temps."""
        demi_vie = 60.0
        factor = math.exp(-elapsed / demi_vie * math.log(2))
        self._activations = {c: a * factor for c, a in self._activations.items()
                             if a * factor > 0.02}

    def tensions_conceptuelles(self, concepts: List[str]) -> List[Tuple[str, str, float]]:
        """
        Détecte les tensions (paires de concepts opposés) parmi les actifs.
        Retourne [(concept_a, concept_b, force_tension), ...]
        """
        _OPPOSITIONS = {
            ("liberté","contrainte"), ("vie","mort"), ("vérité","mensonge"),
            ("raison","émotion"), ("certitude","doute"), ("corps","esprit"),
            ("présence","absence"), ("sens","absurde"), ("existence","néant"),
            ("connaissance","ignorance"), ("parole","silence"),
        }
        tensions = []
        cl = [c.lower() for c in concepts]
        for a, b in _OPPOSITIONS:
            if a in cl and b in cl:
                force = (self._activations.get(a, 0.5) + self._activations.get(b, 0.5)) / 2
                tensions.append((a, b, round(force, 3)))
        return tensions


# ═══════════════════════════════════════════════════════════════════════════════
# IV. SYSTÈME D'ATTENTION — bande passante limitée
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SystemeAttention:
    """
    L'attention de Leia : limitée, orientable, saturable.

    Elle ne peut pas tout traiter en même temps.
    Les pensées se disputent sa bande passante.
    """
    # Foyer attentionnel courant
    foyer: str = ""              # concept ou idée au centre
    concepts_secondaires: List[str] = field(default_factory=list)  # arrière-plan

    # Capacité
    capacite: float = 1.0        # 1.0 = pleine capacité
    saturation: float = 0.0      # 0 = libre, 1 = saturée
    biais_actuel: float = 0.0    # -1 attirée vers négatif, +1 vers positif

    # Historique des foyers récents
    historique_foyers: deque = field(default_factory=lambda: deque(maxlen=20))

    def orienter(self, concept: str, force: float = 0.6) -> None:
        """Oriente l'attention vers un concept."""
        if self.saturation > 0.85:
            return  # Trop saturée pour se réorienter
        if self.foyer and self.foyer != concept:
            self.concepts_secondaires = ([self.foyer] + self.concepts_secondaires)[:4]
        if self.foyer != concept:
            self.historique_foyers.appendleft({
                "concept": concept, "at": time.time(), "force": round(force, 3)
            })
        self.foyer = concept

    def ajouter_secondaire(self, concepts: List[str]) -> None:
        """Ajoute des concepts en attention secondaire."""
        for c in concepts:
            if c != self.foyer and c not in self.concepts_secondaires:
                self.concepts_secondaires = ([c] + self.concepts_secondaires)[:5]

    def saturer(self, delta: float) -> None:
        """Augmente la saturation attentionnelle."""
        self.saturation = _c(self.saturation + delta)
        # Récupération naturelle si saturation haute
        if self.saturation > 0.7:
            self.capacite = _c(1.0 - self.saturation * 0.6)

    def tick(self, elapsed: float) -> None:
        """Récupération attentionnelle avec le temps."""
        rate = _c(elapsed / 20.0, 0.01, 0.5)
        self.saturation = _c(self.saturation * (1 - rate * 0.25))
        self.capacite = _c(self.capacite + (1.0 - self.capacite) * rate * 0.15)
        # Les concepts secondaires s'estompent
        if random.random() < rate * 0.3 and self.concepts_secondaires:
            self.concepts_secondaires.pop()

    def est_disponible(self) -> bool:
        return self.saturation < 0.75

    def snapshot(self) -> Dict[str, Any]:
        return {
            "foyer": self.foyer,
            "concepts_secondaires": self.concepts_secondaires[:4],
            "capacite": round(self.capacite, 3),
            "saturation": round(self.saturation, 3),
            "biais": round(self.biais_actuel, 3),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# V. PRESSION EXPRESSIVE — envie de parler / urgence de répondre
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PressionExpressive:
    """
    La pression qui pousse Leia à répondre, à parler, à exprimer.

    Elle n'est pas binaire (je réponds / je ne réponds pas).
    Elle est un gradient de plusieurs forces qui s'accumulent ou se dissipent.
    """
    tension_non_resolue: float = 0.0      # pensées non exprimées
    impulsion_conceptuelle: float = 0.0   # envie de partager une idée
    charge_relationnelle: float = 0.0     # lien avec l'interlocuteur
    curiosite_active: float = 0.0         # question non posée
    momentum_expressif: float = 0.0       # élan narratif en cours

    def total(self) -> float:
        """Pression totale [0-1]."""
        return _c(
            self.tension_non_resolue * 0.30 +
            self.impulsion_conceptuelle * 0.25 +
            self.charge_relationnelle * 0.20 +
            self.curiosite_active * 0.15 +
            self.momentum_expressif * 0.10
        )

    def augmenter(self, source: str, delta: float) -> None:
        if source == "tension":
            self.tension_non_resolue = _c(self.tension_non_resolue + delta)
        elif source == "concept":
            self.impulsion_conceptuelle = _c(self.impulsion_conceptuelle + delta)
        elif source == "relation":
            self.charge_relationnelle = _c(self.charge_relationnelle + delta)
        elif source == "curiosite":
            self.curiosite_active = _c(self.curiosite_active + delta)
        elif source == "momentum":
            self.momentum_expressif = _c(self.momentum_expressif + delta)

    def liberer(self, fraction: float = 0.6) -> float:
        """Libère la pression (après expression). Retourne la valeur libérée."""
        total = self.total()
        freed = total * fraction
        factor = 1 - fraction
        self.tension_non_resolue      *= factor
        self.impulsion_conceptuelle   *= factor
        self.charge_relationnelle     *= factor * 0.7  # persiste davantage
        self.curiosite_active         *= factor
        self.momentum_expressif        = _c(self.momentum_expressif * 1.1)  # rebond
        return freed

    def tick(self, elapsed: float) -> None:
        """Évolution naturelle de la pression."""
        rate = _c(elapsed / 60.0, 0.01, 0.6)
        self.tension_non_resolue    = _c(self.tension_non_resolue * (1 - rate * 0.08))
        self.impulsion_conceptuelle = _c(self.impulsion_conceptuelle * (1 - rate * 0.12))
        self.charge_relationnelle   = _c(self.charge_relationnelle * (1 - rate * 0.05))
        self.curiosite_active       = _c(self.curiosite_active * (1 - rate * 0.10))
        self.momentum_expressif     = _c(self.momentum_expressif * (1 - rate * 0.20))

    def snapshot(self) -> Dict[str, Any]:
        return {
            "total": round(self.total(), 4),
            "tension_non_resolue": round(self.tension_non_resolue, 4),
            "impulsion_conceptuelle": round(self.impulsion_conceptuelle, 4),
            "charge_relationnelle": round(self.charge_relationnelle, 4),
            "curiosite_active": round(self.curiosite_active, 4),
            "momentum_expressif": round(self.momentum_expressif, 4),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# VI. MONOLOGUE INTERNE — flux de pensée de fond
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MonologueInterne:
    """
    Le flux de pensée intérieure de Leia entre les échanges.

    Ce n'est pas du texte préécrit.
    Ce sont des activations conceptuelles, des questions flottantes,
    des tensions non résolues qui forment un fond cognitif continu.
    """
    flux: deque = field(default_factory=lambda: deque(maxlen=30))
    questions_flottantes: List[str] = field(default_factory=list)
    themes_obsedants: Counter = field(default_factory=Counter)
    derniere_pensee_spontanee: float = 0.0
    intervalle_spontane: float = 8.0   # secondes entre pensées spontanées

    def noter(self, type_pensee: str, concepts: List[str],
              intensite: float = 0.5, source: str = "") -> None:
        """Ajoute une entrée au monologue interne."""
        self.flux.appendleft({
            "type": type_pensee,
            "concepts": concepts[:5],
            "intensite": round(intensite, 3),
            "source": source[:40],
            "at": time.time(),
        })
        for c in concepts[:3]:
            self.themes_obsedants[c] += 1

    def ajouter_question(self, question: str) -> None:
        """Enregistre une question flottante non résolue."""
        if question not in self.questions_flottantes:
            self.questions_flottantes = ([question] + self.questions_flottantes)[:8]

    def themes_dominants(self, n: int = 5) -> List[str]:
        """Les thèmes qui obsèdent le plus Leia en ce moment."""
        return [t for t, _ in self.themes_obsedants.most_common(n)]

    def peut_pensee_spontanee(self) -> bool:
        """Peut-on générer une pensée spontanée maintenant ?"""
        return (time.time() - self.derniere_pensee_spontanee) >= self.intervalle_spontane

    def marquer_pensee_spontanee(self) -> None:
        self.derniere_pensee_spontanee = time.time()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "flux_recent": list(self.flux)[:5],
            "questions_flottantes": self.questions_flottantes[:4],
            "themes_dominants": self.themes_dominants(5),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# VII. GLOBAL WORKSPACE — le cerveau vivant unifié
# ═══════════════════════════════════════════════════════════════════════════════

class GlobalWorkspace:
    """
    Le champ conscient global de Leia.

    C'est ici que TOUT converge et TOUT diverge.
    Tous les modules lisent ici. Tous les modules écrivent ici.

    Ce workspace n'est pas un dictionnaire passif.
    Il est un organisme actif : il évolue, se contamine, s'organise,
    génère des tensions, produit de l'émergence.

    ──────────────────────────────────────────
    ÉCRIRE (injection) :
        workspace.inject_perception(signal)
        workspace.inject_lecture(analyse_texte, source)
        workspace.inject_emotion(valence, arousal, tension)
        workspace.inject_memoire(concepts, intensite)

    LIRE (lecture) :
        workspace.snapshot()
        workspace.pensee_dominante()
        workspace.pression_expressive()
        workspace.etat_emotionnel()
        workspace.concepts_actifs()

    ÉVOLUER (background) :
        workspace.tick(elapsed)           ← appelé par background_life_thread
        workspace.après_expression()      ← appelé après que Leia a répondu
    ──────────────────────────────────────────
    """

    def __init__(self, chemin_persistance: Optional[str] = None):
        # Composants vivants
        self.champ_emotionnel    = ChampEmotionnel()
        self.attention           = SystemeAttention()
        self.propagation         = PropagationAssociative()
        self.pression            = PressionExpressive()
        self.monologue           = MonologueInterne()

        # Pensées actives (la "scène" du workspace)
        self._pensees: Dict[str, PenseeActive] = {}
        self._id_counter: int = 0

        # État méta
        self._n_perceptions: int = 0
        self._n_lectures: int = 0
        self._derniere_activite: float = time.time()
        self._historique_snapshots: deque = deque(maxlen=50)

        # Persistance
        self._chemin = chemin_persistance
        if chemin_persistance:
            self._charger(chemin_persistance)

    # ── Injection (écriture dans le workspace) ─────────────────────────────

    def inject_perception(self, signal: Dict[str, Any]) -> None:
        """
        Injecte une analyse de message utilisateur dans le workspace.
        signal = résultat de LeiaNLPBridge.signal()
        """
        if not signal or not signal.get("available"):
            return

        self._n_perceptions += 1
        self._derniere_activite = time.time()

        # 1. Activation des concepts dans le réseau associatif
        concepts = signal.get("focus_concepts", [])[:8]
        if concepts:
            activations = self.propagation.propager(
                concepts,
                force_initiale=signal.get("urgency", 0.4) + 0.3,
                profondeur=3,
            )
            # Orienter l'attention vers le concept focal
            if concepts:
                self.attention.orienter(concepts[0], force=0.7)
                self.attention.ajouter_secondaire(concepts[1:])

        # 2. Contamination émotionnelle
        charge = _c(signal.get("emotional_charge", 0.0), -1.0, 1.0)
        tension_conceptuelle = signal.get("tension", 0.0)
        arousal = _c(signal.get("urgency", 0.0) * 0.6 + abs(charge) * 0.4)
        self.champ_emotionnel.contaminer(
            valence=charge,
            arousal=arousal,
            tension=tension_conceptuelle,
            force=0.3 + signal.get("urgency", 0.0) * 0.2,
        )

        # 3. Créer une pensée active
        intent = signal.get("intent", "")
        pensee_id = self._nouveau_id()
        contenu = f"{intent}:{','.join(concepts[:3])}" if concepts else intent
        pensee = PenseeActive(
            id=pensee_id,
            contenu=contenu[:80],
            concepts=concepts,
            poids=_c(0.5 + signal.get("urgency", 0.0) * 0.3),
            charge_emotionnelle=charge,
            tension=tension_conceptuelle,
            urgence=signal.get("urgency", 0.0),
            nouveaute=signal.get("surprise", 0.0),
            resonance=signal.get("resonance", 0.0),
            source="dialogue",
            persistante=(signal.get("urgency", 0.0) > 0.6 or tension_conceptuelle > 0.5),
        )
        self._ajouter_pensee(pensee)

        # 4. Pression expressive
        if intent.startswith("question"):
            self.pression.augmenter("curiosite", 0.3 + signal.get("urgency", 0.1))
        if tension_conceptuelle > 0.3:
            self.pression.augmenter("tension", tension_conceptuelle * 0.4)
        if charge < -0.3:
            self.pression.augmenter("relation", abs(charge) * 0.3)
        self.pression.augmenter("concept", signal.get("resonance", 0.0) * 0.3)

        # 5. Monologue interne
        type_pensee = "question" if signal.get("is_question") else "affirmation"
        self.monologue.noter(
            type_pensee, concepts,
            intensite=pensee.poids, source="dialogue"
        )
        if signal.get("is_question") and concepts:
            self.monologue.ajouter_question(",".join(concepts[:2]))

        # 6. Saturation attentionnelle
        self.attention.saturer(0.05 + signal.get("complexity", 0.0) * 0.1)

        # 7. Apprentissage des associations (depuis les co-occurrences)
        for i in range(len(concepts)):
            for j in range(i+1, min(len(concepts), i+3)):
                self.propagation.apprendre_lien(concepts[i], concepts[j], force=0.3)

    def inject_lecture(self, analyse: Dict[str, Any], source: str = "") -> None:
        """
        Injecte une analyse de texte lu (livre, PDF) dans le workspace.
        analyse = résultat de LeiaNLPBridge.analyze_book_chunk()
        """
        if not analyse or not analyse.get("available"):
            return

        self._n_lectures += 1
        self._derniere_activite = time.time()

        concepts = analyse.get("key_concepts", [])[:12]
        themes = analyse.get("themes", [])[:5]
        theses = analyse.get("theses", [])[:3]

        # 1. Propagation depuis les concepts clés
        if concepts:
            self.propagation.propager(
                concepts[:8], force_initiale=0.5, profondeur=2
            )

        # 2. Contamination émotionnelle légère (lecture = moins forte que dialogue)
        charge = _c(analyse.get("charge_emotionnelle", 0.0), -1.0, 1.0)
        self.champ_emotionnel.contaminer(
            valence=charge * 0.5,  # lecture = influence plus douce
            arousal=0.2,
            tension=analyse.get("tension", 0.0) * 0.6,
            force=0.15,
        )

        # 3. Pensée de lecture
        pensee_id = self._nouveau_id()
        contenu_pensee = f"lecture:{source[:30]}:{','.join(concepts[:3])}"
        pensee = PenseeActive(
            id=pensee_id,
            contenu=contenu_pensee[:80],
            concepts=concepts[:8],
            poids=_c(0.4 + analyse.get("resonance", 0.0) * 0.3),
            charge_emotionnelle=charge * 0.5,
            tension=analyse.get("tension", 0.0),
            nouveaute=analyse.get("surprise", 0.0),
            resonance=analyse.get("resonance", 0.0),
            source="lecture",
            demi_vie=300.0,  # Les pensées de lecture persistent plus longtemps
            persistante=(analyse.get("resonance", 0.0) > 0.5),
        )
        self._ajouter_pensee(pensee)

        # 4. Monologue interne — la lecture nourrit la réflexion
        self.monologue.noter("lecture", concepts[:5], intensite=pensee.poids, source=source)
        if theses:
            for these in theses[:2]:
                mots_these = [w for w in re.findall(r"[a-zA-ZÀ-ÿ]{4,}", these.lower())
                              if w not in {"dont","avec","dans","pour","sans","vers"}]
                if mots_these:
                    self.monologue.noter("these", mots_these[:3], intensite=0.5, source=source)

        # 5. Pression : la lecture enrichit l'impulsion conceptuelle
        if analyse.get("resonance", 0.0) > 0.3:
            self.pression.augmenter("concept", analyse.get("resonance", 0.0) * 0.3)
        if analyse.get("tension", 0.0) > 0.4:
            self.pression.augmenter("tension", analyse.get("tension", 0.0) * 0.25)

        # 6. Apprentissage des associations depuis les thèmes co-présents
        for i, c1 in enumerate(concepts[:8]):
            for c2 in concepts[i+1:i+4]:
                self.propagation.apprendre_lien(c1, c2, force=0.25)

    def inject_emotion(self, valence: float, arousal: float = 0.0,
                       tension: float = 0.0, source: str = "") -> None:
        """Injection directe d'émotion (depuis affect_lexicon, affective_memory, etc.)"""
        self.champ_emotionnel.contaminer(valence, arousal, tension, force=0.3)
        if abs(valence) > 0.5:
            type_p = "emotion_forte" if abs(valence) > 0.7 else "emotion"
            self.monologue.noter(type_p, [], intensite=abs(valence), source=source)

    def inject_memoire(self, concepts: List[str], intensite: float = 0.5,
                       ton_emotionnel: float = 0.0) -> None:
        """Injection depuis la mémoire (réactivation d'un souvenir, d'un concept)."""
        if not concepts:
            return
        self.propagation.propager(concepts, force_initiale=intensite * 0.8, profondeur=2)
        if ton_emotionnel != 0.0:
            self.champ_emotionnel.contaminer(ton_emotionnel, force=0.15)
        self.monologue.noter("memoire", concepts[:4], intensite=intensite, source="mémoire")
        # La réactivation mémorielle augmente la pression expressive
        self.pression.augmenter("concept", intensite * 0.2)

    # ── Lecture (accès à l'état) ───────────────────────────────────────────

    def pensee_dominante(self) -> Optional[PenseeActive]:
        """La pensée la plus forte dans le champ conscient actuellement."""
        actives = [p for p in self._pensees.values() if p.est_active()]
        if not actives:
            return None
        return max(actives, key=lambda p: p.poids * (1 + p.urgence * 0.3))

    def pensees_actives(self, n: int = 8, seuil: float = 0.1) -> List[PenseeActive]:
        """Toutes les pensées actives, triées par poids décroissant."""
        actives = [p for p in self._pensees.values() if p.est_active(seuil)]
        return sorted(actives, key=lambda p: p.poids, reverse=True)[:n]

    def pression_expressive(self) -> float:
        """Pression totale d'expression [0-1]."""
        return self.pression.total()

    def etat_emotionnel(self) -> Dict[str, Any]:
        """État émotionnel courant (compatible EmotionalState de leia_living_core)."""
        snap = self.champ_emotionnel.snapshot()
        prop = self.champ_emotionnel.propagation_vers_attention()
        return {**snap, **prop}

    def concepts_actifs(self, n: int = 12, seuil: float = 0.12) -> List[str]:
        """Concepts actuellement actifs dans la propagation associative."""
        return [c for c, _ in self.propagation.concepts_actives(seuil, n)]

    def tensions_actives(self) -> List[Tuple[str, str, float]]:
        """Paires de concepts en tension dans le workspace."""
        concepts = self.concepts_actifs(n=15)
        return self.propagation.tensions_conceptuelles(concepts)

    def etat_attention(self) -> Dict[str, Any]:
        return self.attention.snapshot()

    def themes_monologue(self) -> List[str]:
        return self.monologue.themes_dominants(6)

    # ── Évolution ─────────────────────────────────────────────────────────

    def tick(self, elapsed: float = 1.0) -> None:
        """
        Évolution de fond du workspace.
        Appelé par background_life_thread régulièrement.
        """
        # 1. Décroissance de tous les composants
        self.champ_emotionnel.tick(elapsed)
        self.attention.tick(elapsed)
        self.propagation.tick(elapsed)
        self.pression.tick(elapsed)

        # 2. Décroissance des pensées actives
        pensees_a_supprimer = []
        for pid, pensee in self._pensees.items():
            pensee.decay_step(elapsed)
            if not pensee.est_active(seuil=0.04) and not pensee.persistante:
                pensees_a_supprimer.append(pid)
        for pid in pensees_a_supprimer:
            del self._pensees[pid]

        # 3. Pensées spontanées (émergence de fond)
        if self.monologue.peut_pensee_spontanee():
            self._generer_pensee_spontanee()

        # 4. Tensions persistantes → augmentent la pression
        tensions = self.tensions_actives()
        if tensions:
            force_tension = sum(t[2] for t in tensions) / len(tensions)
            self.pression.augmenter("tension", force_tension * 0.02)

        # 5. Les pensées persistantes réactivent le monologue
        persistantes = [p for p in self._pensees.values()
                        if p.persistante and p.est_active(0.15)]
        if persistantes:
            p = max(persistantes, key=lambda x: x.poids)
            self.monologue.noter(
                "persistance", p.concepts, intensite=p.poids * 0.5,
                source="fond_cognitif"
            )

    def après_expression(self, fraction_liberation: float = 0.5) -> None:
        """
        Appelé après que Leia a exprimé une réponse.
        Libère une partie de la pression et consolide les pensées.
        """
        self.pression.liberer(fraction_liberation)
        # Résoudre les pensées de type dialogue récentes
        for pensee in self._pensees.values():
            if pensee.source == "dialogue" and pensee.poids > 0.5:
                pensee.poids *= 0.6
                pensee.resolue = True

    def _generer_pensee_spontanee(self) -> None:
        """
        Génère une pensée de fond spontanée.
        Basée sur les concepts les plus actifs et les thèmes obsédants.
        """
        themes = self.monologue.themes_dominants(3)
        actifs = self.concepts_actifs(n=5)
        candidats = list(dict.fromkeys(themes + actifs))
        if not candidats:
            return

        concept = candidats[0]
        voisins = [c for c, _ in self.propagation._reseau.get(concept, [])[:3]]

        pensee_id = self._nouveau_id()
        pensee = PenseeActive(
            id=pensee_id,
            contenu=f"spontane:{concept}",
            concepts=[concept] + voisins[:2],
            poids=0.25,
            source="interne",
            demi_vie=60.0,
        )
        self._ajouter_pensee(pensee)
        self.monologue.noter(
            "spontane", [concept] + voisins[:2], intensite=0.25, source="emergent"
        )
        self.monologue.marquer_pensee_spontanee()

    # ── Compatibilité avec leia_living_core ────────────────────────────────

    def vers_global_conscious_field_state(self) -> Dict[str, Any]:
        """
        Produit un état compatible avec GlobalConsciousField.state
        de leia_living_core.py — pour que l'existant continue de fonctionner.
        """
        emotion = self.champ_emotionnel.snapshot()
        attention = self.attention.snapshot()
        propagation = self.propagation.concepts_actives(n=5)
        pensee_dom = self.pensee_dominante()
        tensions = self.tensions_actives()

        return {
            "phase":               "workspace_actif",
            "presence_density":    _c(1.0 - emotion["fatigue"] * 0.5),
            "attention_density":   _c(1.0 - attention["saturation"]),
            "memory_density":      _c(self.pression.tension_non_resolue * 0.5),
            "emotion_density":     _c(abs(emotion["valence"]) * 0.5 + emotion["tension"] * 0.5),
            "relation_density":    _c(self.pression.charge_relationnelle),
            "identity_density":    _c(emotion["ouverture"]),
            "motivation_density":  _c(self.pression.total()),
            "simulation_density":  _c(self.pression.impulsion_conceptuelle),
            "meta_pressure":       0.0,
            "integration":         _c(
                emotion["ouverture"] * 0.3 +
                (1 - emotion["fatigue"]) * 0.3 +
                self.pression.total() * 0.2 +
                (1 - attention["saturation"]) * 0.2
            ),
            "living_pressure":     _c(self.pression.total()),
            "dominant_axis":       self._axe_dominant(emotion),
            "focus":               pensee_dom.contenu[:80] if pensee_dom else attention["foyer"],
            "active_concepts":     [c for c, _ in propagation],
            "tensions":            [(a, b) for a, b, _ in tensions[:3]],
            "tonalite_emotionnelle": emotion["tonalite"],
        }

    def _axe_dominant(self, emotion: Dict[str, Any]) -> str:
        axes = {
            "emotion":    abs(emotion["valence"]) + emotion["tension"],
            "attention":  1.0 - emotion.get("saturation", 0.0),
            "memory":     self.pression.tension_non_resolue,
            "motivation": self.pression.total(),
            "relation":   self.pression.charge_relationnelle,
            "presence":   emotion["ouverture"],
        }
        return max(axes, key=axes.get)

    def payload_pour_expression(self) -> Dict[str, Any]:
        """
        Produit le payload que living_language_generator et emergent_french_weaver
        utilisent pour générer la réponse de Leia.
        Compatible avec le format attendu par ces modules.
        """
        emotion = self.champ_emotionnel.snapshot()
        pensee_dom = self.pensee_dominante()
        concepts_actifs = self.concepts_actifs(n=10)
        tensions = self.tensions_actives()

        return {
            # État émotionnel
            "emotional_tone":   emotion["tonalite"],
            "tension":          round(emotion["tension"], 3),
            "energy":           round(1.0 - emotion["fatigue"], 3),
            "resonance":        round(emotion["resonance"], 3),
            "warmth":           round(max(0.0, emotion["valence"] * 0.5 + 0.5), 3),
            "fatigue":          round(emotion["fatigue"], 3),
            "arousal":          round(emotion["arousal"], 3),

            # Contenu cognitif
            "dominant_thought": pensee_dom.contenu if pensee_dom else "",
            "focus_concepts":   concepts_actifs[:6],
            "active_tensions":  [(a, b) for a, b, _ in tensions[:2]],
            "questions_flottantes": self.monologue.questions_flottantes[:3],
            "themes_obsedants": self.monologue.themes_dominants(4),

            # Pression
            "pression_totale":  round(self.pression.total(), 3),
            "pression_details": self.pression.snapshot(),

            # Attention
            "attention_foyer":  self.attention.foyer,
            "attention_libre":  self.attention.est_disponible(),
        }

    # ── Persistance ────────────────────────────────────────────────────────

    def snapshot(self) -> Dict[str, Any]:
        """Snapshot complet de l'état du workspace."""
        pensee_dom = self.pensee_dominante()
        snap = {
            "emotion": self.champ_emotionnel.snapshot(),
            "attention": self.attention.snapshot(),
            "pression": self.pression.snapshot(),
            "monologue": self.monologue.snapshot(),
            "pensee_dominante": pensee_dom.to_dict() if pensee_dom else None,
            "pensees_actives": [p.to_dict() for p in self.pensees_actives(n=5)],
            "concepts_actifs": self.concepts_actifs(n=10),
            "tensions_actives": [(a, b, round(f, 3)) for a, b, f in self.tensions_actives()],
            "n_perceptions": self._n_perceptions,
            "n_lectures": self._n_lectures,
            "gcf_state": self.vers_global_conscious_field_state(),
        }
        self._historique_snapshots.appendleft({"at": time.time(), **snap})
        return snap

    def sauvegarder(self, chemin: Optional[str] = None) -> None:
        path = chemin or self._chemin
        if not path:
            return
        data = {
            "champ_emotionnel": self.champ_emotionnel.snapshot(),
            "activations_associatives": {
                k: round(v, 3) for k, v in self.propagation._activations.items()
                if v > 0.05
            },
            "pression": self.pression.snapshot(),
            "themes_obsedants": dict(self.monologue.themes_obsedants.most_common(20)),
            "questions_flottantes": self.monologue.questions_flottantes[:8],
            "n_perceptions": self._n_perceptions,
            "n_lectures": self._n_lectures,
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _charger(self, chemin: str) -> None:
        try:
            data = json.loads(Path(chemin).read_text(encoding="utf-8"))
            em = data.get("champ_emotionnel", {})
            self.champ_emotionnel.valence  = _c(em.get("valence", 0.0), -1.0, 1.0)
            self.champ_emotionnel.arousal  = _c(em.get("arousal", 0.3))
            self.champ_emotionnel.tension  = _c(em.get("tension", 0.0))
            self.champ_emotionnel.fatigue  = _c(em.get("fatigue", 0.0))
            self.champ_emotionnel.ouverture = _c(em.get("ouverture", 0.6))
            for c, a in data.get("activations_associatives", {}).items():
                self.propagation._activations[c] = _c(a)
            for theme, cnt in data.get("themes_obsedants", {}).items():
                self.monologue.themes_obsedants[theme] = int(cnt)
            self.monologue.questions_flottantes = data.get("questions_flottantes", [])
            self._n_perceptions = data.get("n_perceptions", 0)
            self._n_lectures = data.get("n_lectures", 0)
        except Exception:
            pass

    # ── Utilitaires internes ───────────────────────────────────────────────

    def _nouveau_id(self) -> str:
        self._id_counter += 1
        return f"p{self._id_counter:04d}"

    def _ajouter_pensee(self, pensee: PenseeActive) -> None:
        """Ajoute une pensée avec compétition attentionnelle."""
        self._pensees[pensee.id] = pensee
        # Nettoyer les pensées trop faibles si trop de pensées actives
        actives = [p for p in self._pensees.values() if p.est_active()]
        if len(actives) > 15:
            # Supprimer les 3 plus faibles (non-persistantes)
            tri = sorted(
                [p for p in actives if not p.persistante],
                key=lambda x: x.poids
            )
            for p in tri[:3]:
                del self._pensees[p.id]


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════

workspace = GlobalWorkspace()
"""
Instance globale partagée par tous les modules Leia.

Import recommandé :
    from global_workspace import workspace

    workspace.inject_perception(signal)
    etat = workspace.snapshot()
    payload = workspace.payload_pour_expression()
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    def sep(titre=""):
        print(f"\n{'─'*62}")
        if titre:
            print(f"  {titre}")
            print("─"*62)

    print("═"*62)
    print("  LEIA — Global Workspace · Diagnostic")
    print("  Pure Python · Vivant · Zéro dépendance")
    print("═"*62)

    sep("INJECTION DIALOGUE — résonance / contamination")

    signaux = [
        {
            "available": True,
            "intent": "question_philosophique",
            "focus_concepts": ["liberté", "contrainte", "existence"],
            "emotional_charge": -0.1,
            "tension": 0.3,
            "urgency": 0.2,
            "resonance": 0.4,
            "surprise": 0.5,
            "complexity": 0.6,
            "is_question": True,
        },
        {
            "available": True,
            "intent": "confidence_personnelle",
            "focus_concepts": ["peur", "intelligence", "artificielle"],
            "emotional_charge": -0.6,
            "tension": 0.5,
            "urgency": 0.4,
            "resonance": 0.2,
            "surprise": 0.8,
            "complexity": 0.4,
            "is_question": False,
        },
        {
            "available": True,
            "intent": "challenge",
            "focus_concepts": ["mémoire", "identité", "temps"],
            "emotional_charge": 0.1,
            "tension": 0.7,
            "urgency": 0.3,
            "resonance": 0.6,
            "surprise": 0.3,
            "complexity": 0.8,
            "is_question": False,
        },
    ]

    for i, sig in enumerate(signaux, 1):
        workspace.inject_perception(sig)
        print(f"\n  Message {i} — intent: {sig['intent']}")

        dom = workspace.pensee_dominante()
        if dom:
            print(f"    Pensée dominante : {dom.contenu[:50]} (poids={dom.poids:.3f})")

        emotion = workspace.champ_emotionnel.snapshot()
        print(f"    Champ émotionnel : {emotion['tonalite']} | valence={emotion['valence']:+.3f} | tension={emotion['tension']:.3f}")
        print(f"    Pression expressive : {workspace.pression.total():.3f}")
        print(f"    Concepts actifs     : {workspace.concepts_actifs(n=6)}")

        tensions = workspace.tensions_actives()
        if tensions:
            print(f"    Tensions détectées  : {[(a,b) for a,b,_ in tensions]}")

    sep("INJECTION LECTURE — Bergson")

    analyse_lecture = {
        "available": True,
        "key_concepts": ["mémoire", "durée", "bergson", "temps", "souvenir", "perception"],
        "themes": ["mémoire / temps", "durée / conscience"],
        "theses": ["La mémoire est durée vécue, non stockage fixe."],
        "objections": ["Locke fonde la mémoire sur des traces fixes."],
        "resonance": 0.7,
        "surprise": 0.3,
        "tension": 0.5,
        "charge_emotionnelle": 0.2,
    }
    workspace.inject_lecture(analyse_lecture, source="Bergson - Matière et Mémoire")
    print(f"\n  Après lecture Bergson :")
    print(f"    Concepts actifs    : {workspace.concepts_actifs(n=8)}")
    print(f"    Pression concept   : {workspace.pression.impulsion_conceptuelle:.3f}")
    print(f"    Monologue thèmes   : {workspace.monologue.themes_dominants(5)}")

    sep("TICK — évolution de fond (5 secondes simulées)")
    workspace.tick(elapsed=5.0)
    print(f"\n  Après 5s :")
    print(f"    Pression totale : {workspace.pression.total():.3f}")
    print(f"    Fatigue         : {workspace.champ_emotionnel.fatigue:.3f}")
    print(f"    Pensées actives : {len(workspace.pensees_actives())}")

    sep("PAYLOAD POUR EXPRESSION")
    payload = workspace.payload_pour_expression()
    print(f"\n  emotional_tone   : {payload['emotional_tone']}")
    print(f"  dominant_thought : {payload['dominant_thought'][:50]}")
    print(f"  focus_concepts   : {payload['focus_concepts'][:5]}")
    print(f"  active_tensions  : {payload['active_tensions']}")
    print(f"  pression_totale  : {payload['pression_totale']}")
    print(f"  questions        : {payload['questions_flottantes']}")

    sep("ÉTAT GCF (compatible GlobalConsciousField)")
    gcf = workspace.vers_global_conscious_field_state()
    print(f"\n  phase            : {gcf['phase']}")
    print(f"  presence_density : {gcf['presence_density']:.3f}")
    print(f"  emotion_density  : {gcf['emotion_density']:.3f}")
    print(f"  motivation_density: {gcf['motivation_density']:.3f}")
    print(f"  dominant_axis    : {gcf['dominant_axis']}")
    print(f"  focus            : {gcf['focus'][:40]}")
    print(f"  tonalité         : {gcf['tonalite_emotionnelle']}")

    print("\n" + "═"*62)
    print("  Workspace vivant. Propagation réelle. Zéro préécrit.")
    print("═"*62)