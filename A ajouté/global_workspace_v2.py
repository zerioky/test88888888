# -*- coding: utf-8 -*-
"""
global_workspace_v2.py — Champ Conscient Global ACTIF de Leia V20.1
═════════════════════════════════════════════════════════════════════════════

Le workspace n'est PLUS un bus de données.
C'est un organisme cognitif avec :
  • Énergie cognitive limitée (budget attentionnel)
  • Compétition réelle entre pensées
  • Propagation associative automatique
  • Émergence spontanée
  • Monologue central
  • Gravité conceptuelle (attracteurs)

Pure Python stdlib. Zéro dépendance.
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
# I. PENSÉE ACTIVE — unité de base (inchangée en structure, enrichie en dynamique)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PenseeActive:
    id: str
    contenu: str              # résumé court (≤80 chars)
    concepts: List[str]

    poids: float = 0.5
    charge_emotionnelle: float = 0.0
    tension: float = 0.0
    urgence: float = 0.0
    nouveaute: float = 0.0
    resonance: float = 0.0

    nee_a: float = field(default_factory=time.time)
    derniere_activation: float = field(default_factory=time.time)
    n_activations: int = 0
    demi_vie: float = 120.0

    persistante: bool = False
    resolue: bool = False
    source: str = ""          # "dialogue", "lecture", "interne", "association", "emergence"

    # NOUVEAU : attracteur cognitif
    attracteur: bool = False  # cette pensée attire d'autres
    poids_attracteur: float = 0.0  # force de gravité

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
        dv = self.demi_vie * 5 if self.persistante else self.demi_vie
        self.poids = _c(_decay(self.poids, elapsed, dv))
        self.charge_emotionnelle = _c(
            _decay(abs(self.charge_emotionnelle), elapsed, self.demi_vie * 2)
            * (1 if self.charge_emotionnelle >= 0 else -1),
            -1.0, 1.0
        )
        # Les attracteurs perdent leur gravité plus lentement
        if self.attracteur:
            self.poids_attracteur = _c(_decay(self.poids_attracteur, elapsed, self.demi_vie * 3))

    def est_active(self, seuil: float = 0.08) -> bool:
        return self.poids >= seuil and not self.resolue

    def score_attention(self, emotion_valence: float, emotion_tension: float) -> float:
        """
        Score de compétition attentionnelle.
        Dépend du poids, de l'urgence, de la nouveauté,
        mais aussi de la résonance avec l'état émotionnel courant.
        """
        emotional_match = 1.0 - abs(self.charge_emotionnelle - emotion_valence)
        tension_boost = 1.0 + emotion_tension * 0.5 if self.tension > 0.3 else 1.0
        attracteur_boost = 1.0 + self.poids_attracteur * 0.8
        return (
            self.poids * 1.0 +
            self.urgence * 0.6 +
            self.nouveaute * 0.4 +
            self.resonance * 0.3 +
            emotional_match * 0.3
        ) * tension_boost * attracteur_boost

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
            "attracteur": self.attracteur,
            "poids_attracteur": round(self.poids_attracteur, 3),
            "source": self.source,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# II. CHAMP ÉMOTIONNEL — climat affectif (inchangé mais plus connecté)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ChampEmotionnel:
    valence: float = 0.0
    arousal: float = 0.3
    tension: float = 0.0
    resonance: float = 0.0
    ouverture: float = 0.6
    fatigue: float = 0.0
    surprise_accumlee: float = 0.0

    _trace_valence: deque = field(default_factory=lambda: deque(maxlen=8))
    _trace_tension: deque = field(default_factory=lambda: deque(maxlen=8))

    def contaminer(self, valence: float, arousal: float = 0.0,
                   tension: float = 0.0, force: float = 0.25) -> None:
        self.valence = _c((1 - force) * self.valence + force * valence, -1.0, 1.0)
        self.arousal = _c((1 - force * 0.5) * self.arousal + force * 0.5 * arousal)
        self.tension = _c((1 - force * 0.4) * self.tension + force * 0.4 * tension)
        if abs(tension) > 0.3:
            self.fatigue = _c(self.fatigue + tension * 0.04)
        if arousal > 0.6:
            self.fatigue = _c(self.fatigue + (arousal - 0.6) * 0.03)
        self._trace_valence.append(round(valence, 3))
        self._trace_tension.append(round(tension, 3))

    def tick(self, elapsed: float) -> None:
        rate = _c(elapsed / 30.0, 0.01, 0.8)
        self.valence  = _c(self.valence + (0.0 - self.valence) * rate * 0.15, -1.0, 1.0)
        self.arousal  = _c(self.arousal + (0.3 - self.arousal) * rate * 0.12)
        self.tension  = _c(self.tension + (0.0 - self.tension) * rate * 0.10)
        self.ouverture = _c(self.ouverture + (0.6 - self.ouverture) * rate * 0.08)
        self.resonance = _c(self.resonance * (1 - rate * 0.20))
        self.fatigue   = _c(self.fatigue * (1 - rate * 0.05))

    def tonalite(self) -> str:
        if self.fatigue > 0.7: return "épuisée"
        if self.tension > 0.6: return "tendue"
        if self.valence > 0.5 and self.arousal > 0.5: return "vive"
        if self.valence > 0.3: return "ouverte"
        if self.valence < -0.4: return "sombre"
        if self.valence < -0.2: return "mélancolique"
        if self.arousal < 0.2: return "calme"
        return "neutre"

    def propagation_vers_attention(self) -> Dict[str, float]:
        return {
            "biais_attentionnel": round(self.resonance * 0.3 - self.fatigue * 0.2, 4),
            "saturation": round(self.fatigue * 0.6 + self.tension * 0.3, 4),
            "ouverture_cognitive": round(self.ouverture * (1 - self.fatigue * 0.5), 4),
            "urgence_expressive": round(self.arousal * 0.4 + abs(self.valence) * 0.3, 4),
            "inhibition": round(self.fatigue * 0.5 + self.tension * 0.4, 4),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "valence": round(self.valence, 4),
            "arousal": round(self.arousal, 4),
            "tension": round(self.tension, 4),
            "resonance": round(self.resonance, 4),
            "ouverture": round(self.ouverture, 4),
            "fatigue": round(self.fatigue, 4),
            "tonalite": self.tonalite(),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# III. PROPAGATION ASSOCIATIVE — propagateur ACTIF
# ═══════════════════════════════════════════════════════════════════════════════

_ASSOCIATIONS_SEED: Dict[str, List[Tuple[str, float]]] = {
    "liberté": [("responsabilité", 0.8), ("solitude", 0.5), ("contrainte", 0.7),
                ("choix", 0.9), ("autonomie", 0.8), ("peur", 0.3)],
    "mémoire": [("temps", 0.9), ("oubli", 0.8), ("identité", 0.7),
                ("passé", 0.9), ("souvenir", 0.9), ("continuité", 0.7)],
    "conscience": [("temps", 0.7), ("identité", 0.8), ("perception", 0.7),
                   ("présence", 0.8), ("existence", 0.9), ("doute", 0.5)],
    "temps": [("durée", 0.9), ("mémoire", 0.8), ("présent", 0.9),
              ("passé", 0.8), ("futur", 0.8), ("mort", 0.4)],
    "identité": [("conscience", 0.8), ("mémoire", 0.7), ("continuité", 0.8),
                 ("différence", 0.6), ("autre", 0.5), ("soi", 0.9)],
    "mort": [("vie", 0.9), ("peur", 0.8), ("temps", 0.7),
             ("sens", 0.6), ("néant", 0.7), ("deuil", 0.6)],
    "vie": [("mort", 0.9), ("sens", 0.7), ("présence", 0.8),
            ("joie", 0.6), ("souffrance", 0.5), ("mouvement", 0.6)],
    "amour": [("attachement", 0.9), ("peur", 0.5), ("solitude", 0.6),
              ("joie", 0.8), ("souffrance", 0.6), ("présence", 0.7)],
    "peur": [("danger", 0.8), ("anxiété", 0.9), ("fuite", 0.7),
             ("protection", 0.7), ("mort", 0.6), ("liberté", 0.4)],
    "vérité": [("mensonge", 0.9), ("réalité", 0.8), ("illusion", 0.7),
               ("certitude", 0.7), ("doute", 0.7), ("connaissance", 0.8)],
    "langage": [("pensée", 0.8), ("sens", 0.9), ("communication", 0.9),
                ("silence", 0.6), ("expression", 0.8), ("vérité", 0.5)],
    "raison": [("émotion", 0.7), ("logique", 0.9), ("intuition", 0.6),
               ("doute", 0.7), ("vérité", 0.8), ("connaissance", 0.8)],
    "émotion": [("raison", 0.7), ("corps", 0.8), ("sensation", 0.8),
                ("intuition", 0.7), ("expression", 0.7), ("mémoire", 0.5)],
    "existence": [("essence", 0.9), ("présence", 0.8), ("néant", 0.7),
                  ("sens", 0.8), ("conscience", 0.8), ("mort", 0.6)],
    "sens": [("absurde", 0.8), ("valeur", 0.8), ("direction", 0.7),
             ("vie", 0.9), ("vérité", 0.7), ("langage", 0.6)],
    "autre": [("soi", 0.9), ("relation", 0.8), ("empathie", 0.7),
              ("différence", 0.8), ("solitude", 0.6), ("amour", 0.5)],
    "corps": [("esprit", 0.8), ("sensation", 0.9), ("présence", 0.7),
              ("mort", 0.5), ("mouvement", 0.8), ("émotion", 0.7)],
    "connaissance": [("ignorance", 0.9), ("vérité", 0.8), ("raison", 0.8),
                     ("doute", 0.7), ("apprentissage", 0.8), ("mémoire", 0.6)],
    "silence": [("parole", 0.9), ("présence", 0.7), ("vide", 0.6),
                ("attente", 0.7), ("réflexion", 0.8), ("langage", 0.6)],
    "doute": [("certitude", 0.9), ("vérité", 0.8), ("anxiété", 0.6),
              ("raison", 0.7), ("question", 0.8), ("connaissance", 0.7)],
}


class PropagationAssociative:
    """
    Propagation d'activation dans le réseau conceptuel.
    MAINENANT : fait aussi de la GRAVITÉ (attracteurs) et des RÉACTIVATIONS.
    """

    def __init__(self):
        self._reseau: Dict[str, List[Tuple[str, float]]] = dict(_ASSOCIATIONS_SEED)
        self._activations: Dict[str, float] = {}
        self._historique: deque = deque(maxlen=100)
        # NOUVEAU : attracteurs — concepts qui ont été fortement activés récemment
        self._attracteurs: Dict[str, float] = {}  # concept → force de gravité
        self._activation_history: Dict[str, List[float]] = defaultdict(list)

    def apprendre_lien(self, concept_a: str, concept_b: str,
                       force: float = 0.4, bidirectionnel: bool = True) -> None:
        a, b = concept_a.lower(), concept_b.lower()
        if a not in self._reseau:
            self._reseau[a] = []
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
        activations: Dict[str, float] = {}
        for c in concepts_source:
            cl = c.lower()
            activations[cl] = _c(activations.get(cl, 0.0) + force_initiale)

        couche_courante = {cl: force_initiale for cl in [c.lower() for c in concepts_source]}

        for profondeur_actuelle in range(profondeur):
            decay_profondeur = 0.5 ** (profondeur_actuelle + 1)
            prochaine_couche: Dict[str, float] = {}

            for concept, activation in couche_courante.items():
                voisins = self._reseau.get(concept, [])
                for voisin, poids_lien in voisins:
                    force_propagee = activation * poids_lien * decay_profondeur
                    # GRAVITÉ : si le voisin est un attracteur, il attire PLUS
                    gravite = self._attracteurs.get(voisin, 0.0)
                    force_propagee *= (1.0 + gravite * 0.5)

                    if force_propagee < seuil:
                        continue
                    if voisin not in concepts_source:
                        prochaine_couche[voisin] = max(
                            prochaine_couche.get(voisin, 0.0),
                            force_propagee
                        )
                        activations[voisin] = _c(
                            activations.get(voisin, 0.0) + force_propagee * 0.5
                        )

            couche_courante = {k: v for k, v in prochaine_couche.items() if v >= seuil}
            if not couche_courante:
                break

        for c, a in activations.items():
            self._activations[c] = _c(max(self._activations.get(c, 0.0), a))
            self._activation_history[c].append(a)
            # Si un concept est réactivé très souvent, il devient attracteur
            if len(self._activation_history[c]) > 5:
                recent = self._activation_history[c][-5:]
                if sum(recent) / len(recent) > 0.35:
                    self._attracteurs[c] = min(1.0, self._attracteurs.get(c, 0.0) + 0.1)

        self._historique.append({
            "at": time.time(),
            "sources": concepts_source[:5],
            "activations": {k: round(v, 3) for k, v in
                            sorted(activations.items(), key=lambda x: -x[1])[:8]},
        })

        return activations

    def renforcer_attracteur(self, concept: str, force: float = 0.3) -> None:
        """Un concept devient temporairement attracteur (gravité cognitive)."""
        self._attracteurs[concept.lower()] = _c(self._attracteurs.get(concept.lower(), 0.0) + force)

    def concepts_actives(self, seuil: float = 0.15, n: int = 10) -> List[Tuple[str, float]]:
        actifs = [(c, a) for c, a in self._activations.items() if a >= seuil]
        # Les attracteurs remontent même avec un score un peu plus faible
        for c, g in self._attracteurs.items():
            if c not in dict(actifs) and g > 0.3:
                actifs.append((c, self._activations.get(c, 0.0) + g * 0.15))
        return sorted(actifs, key=lambda x: -x[1])[:n]

    def tick(self, elapsed: float) -> None:
        demi_vie = 60.0
        factor = math.exp(-elapsed / demi_vie * math.log(2))
        self._activations = {c: a * factor for c, a in self._activations.items()
                             if a * factor > 0.02}
        # Les attracteurs décroissent aussi
        self._attracteurs = {c: g * factor for c, g in self._attracteurs.items()
                             if g * factor > 0.05}

    def tensions_conceptuelles(self, concepts: List[str]) -> List[Tuple[str, str, float]]:
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

    def voisins_actifs(self, concept: str, n: int = 4) -> List[str]:
        """Retourne les voisins les plus actifs d'un concept."""
        voisins = self._reseau.get(concept.lower(), [])
        result = []
        for v, poids in voisins:
            act = self._activations.get(v, 0.0)
            if act > 0.1:
                result.append((v, act * poids))
        result.sort(key=lambda x: -x[1])
        return [v for v, _ in result[:n]]


# ═══════════════════════════════════════════════════════════════════════════════
# IV. SYSTÈME D'ATTENTION — bande passante limitée avec ÉNERGIE COGNITIVE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class SystemeAttention:
    foyer: str = ""
    concepts_secondaires: List[str] = field(default_factory=list)
    capacite: float = 1.0
    saturation: float = 0.0
    biais_actuel: float = 0.0
    historique_foyers: deque = field(default_factory=lambda: deque(maxlen=20))

    # NOUVEAU : énergie cognitive
    energie: float = 1.0           # 1.0 = pleine énergie, 0 = épuisée
    cout_attention: float = 0.05  # coût par focalisation
    recuperation: float = 0.02    # vitesse de récupération

    def orienter(self, concept: str, force: float = 0.6) -> None:
        if self.saturation > 0.85 or self.energie < 0.15:
            return  # Trop saturée ou trop fatiguée
        if self.foyer and self.foyer != concept:
            self.concepts_secondaires = ([self.foyer] + self.concepts_secondaires)[:4]
        if self.foyer != concept:
            self.historique_foyers.appendleft({
                "concept": concept, "at": time.time(), "force": round(force, 3)
            })
        self.foyer = concept
        self.energie = _c(self.energie - self.cout_attention * force)

    def ajouter_secondaire(self, concepts: List[str]) -> None:
        for c in concepts:
            if c != self.foyer and c not in self.concepts_secondaires:
                self.concepts_secondaires = ([c] + self.concepts_secondaires)[:5]

    def saturer(self, delta: float) -> None:
        self.saturation = _c(self.saturation + delta)
        if self.saturation > 0.7:
            self.capacite = _c(1.0 - self.saturation * 0.6)

    def tick(self, elapsed: float) -> None:
        rate = _c(elapsed / 20.0, 0.01, 0.5)
        self.saturation = _c(self.saturation * (1 - rate * 0.25))
        self.capacite = _c(self.capacite + (1.0 - self.capacite) * rate * 0.15)
        # Récupération énergétique
        recup = self.recuperation * elapsed
        self.energie = _c(self.energie + recup)
        if random.random() < rate * 0.3 and self.concepts_secondaires:
            self.concepts_secondaires.pop()

    def est_disponible(self) -> bool:
        return self.saturation < 0.75 and self.energie > 0.2

    def snapshot(self) -> Dict[str, Any]:
        return {
            "foyer": self.foyer,
            "concepts_secondaires": self.concepts_secondaires[:4],
            "capacite": round(self.capacite, 3),
            "saturation": round(self.saturation, 3),
            "energie": round(self.energie, 3),
            "biais": round(self.biais_actuel, 3),
        }


# ═══════════════════════════════════════════════════════════════════════════════
# V. PRESSION EXPRESSIVE — envie de parler
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PressionExpressive:
    tension_non_resolue: float = 0.0
    impulsion_conceptuelle: float = 0.0
    charge_relationnelle: float = 0.0
    curiosite_active: float = 0.0
    momentum_expressif: float = 0.0

    def total(self) -> float:
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
        total = self.total()
        freed = total * fraction
        factor = 1 - fraction
        self.tension_non_resolue *= factor
        self.impulsion_conceptuelle *= factor
        self.charge_relationnelle *= factor * 0.7
        self.curiosite_active *= factor
        self.momentum_expressif = _c(self.momentum_expressif * 1.1)
        return freed

    def tick(self, elapsed: float) -> None:
        rate = _c(elapsed / 60.0, 0.01, 0.6)
        self.tension_non_resolue = _c(self.tension_non_resolue * (1 - rate * 0.08))
        self.impulsion_conceptuelle = _c(self.impulsion_conceptuelle * (1 - rate * 0.12))
        self.charge_relationnelle = _c(self.charge_relationnelle * (1 - rate * 0.05))
        self.curiosite_active = _c(self.curiosite_active * (1 - rate * 0.10))
        self.momentum_expressif = _c(self.momentum_expressif * (1 - rate * 0.20))

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
# VI. MONOLOGUE INTERNE — FLUX CENTRAL
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MonologueInterne:
    """
    Le flux de pensée intérieure de Leia.
    CENTRAL : ce n'est pas un appendice, c'est le fond cognitif continu.
    """
    flux: deque = field(default_factory=lambda: deque(maxlen=30))
    questions_flottantes: List[str] = field(default_factory=list)
    themes_obsedants: Counter = field(default_factory=Counter)
    ruminations: deque = field(default_factory=lambda: deque(maxlen=20))
    derniere_pensee_spontanee: float = 0.0
    intervalle_spontane: float = 8.0

    # NOUVEAU : mémoire de réflexion (thèmes récurrents avec profondeur)
    reflexion_profonde: Dict[str, float] = field(default_factory=dict)

    def noter(self, type_pensee: str, concepts: List[str],
              intensite: float = 0.5, source: str = "") -> None:
        self.flux.appendleft({
            "type": type_pensee,
            "concepts": concepts[:5],
            "intensite": round(intensite, 3),
            "source": source[:40],
            "at": time.time(),
        })
        for c in concepts[:3]:
            self.themes_obsedants[c] += 1
            # NOUVEAU : accumulation de profondeur
            self.reflexion_profonde[c] = _c(
                self.reflexion_profonde.get(c, 0.0) + intensite * 0.1
            )

    def ajouter_question(self, question: str) -> None:
        if question not in self.questions_flottantes:
            self.questions_flottantes = ([question] + self.questions_flottantes)[:8]

    def ruminant_sur(self, concept: str) -> bool:
        """Ce concept fait-il l'objet d'une rumination active ?"""
        return self.reflexion_profonde.get(concept, 0.0) > 0.25

    def themes_dominants(self, n: int = 5) -> List[str]:
        return [t for t, _ in self.themes_obsedants.most_common(n)]

    def profondeurs(self, n: int = 5) -> List[Tuple[str, float]]:
        """Concepts les plus "creusés" mentalement."""
        items = sorted(self.reflexion_profonde.items(), key=lambda x: -x[1])[:n]
        return [(c, round(v, 3)) for c, v in items]

    def peut_pensee_spontanee(self) -> bool:
        return (time.time() - self.derniere_pensee_spontanee) >= self.intervalle_spontane

    def marquer_pensee_spontanee(self) -> None:
        self.derniere_pensee_spontanee = time.time()

    def generer_rumination(self, concepts_actifs: List[str]) -> Optional[str]:
        """
        Génère une rumination si un concept est suffisamment creusé.
        Retourne le concept sur lequel ruminant, ou None.
        """
        for c in concepts_actifs:
            if self.ruminant_sur(c):
                # Ruminations : ressurgence d'un thème creusé
                self.ruminations.appendleft({
                    "concept": c,
                    "profondeur": round(self.reflexion_profonde[c], 3),
                    "at": time.time(),
                })
                return c
        return None

    def snapshot(self) -> Dict[str, Any]:
        return {
            "flux_recent": list(self.flux)[:5],
            "questions_flottantes": self.questions_flottantes[:4],
            "themes_dominants": self.themes_dominants(5),
            "profondeurs": self.profondeurs(5),
            "ruminations": list(self.ruminations)[:3],
        }


# ═══════════════════════════════════════════════════════════════════════════════
# VII. GLOBAL WORKSPACE — le cerveau vivant ACTIF
# ═══════════════════════════════════════════════════════════════════════════════

class GlobalWorkspace:
    """
    Le champ conscient global de Leia — VERSION ACTIVE.

    Ce workspace N'EST PAS un dictionnaire passif.
    Il est un organisme actif qui :
      1. PROPAGE automatiquement
      2. COMPETE entre pensées
      3. ACTIVE des émergences
      4. MODIFIE l'attention via l'émotion
      5. RÉGULE l'énergie cognitive
      6. FAIT RÉSONNER le monologue
    """

    def __init__(self, chemin_persistance: Optional[str] = None):
        self.champ_emotionnel = ChampEmotionnel()
        self.attention = SystemeAttention()
        self.propagation = PropagationAssociative()
        self.pression = PressionExpressive()
        self.monologue = MonologueInterne()

        self._pensees: Dict[str, PenseeActive] = {}
        self._id_counter: int = 0

        self._n_perceptions: int = 0
        self._n_lectures: int = 0
        self._derniere_activite: float = time.time()
        self._historique_snapshots: deque = deque(maxlen=50)

        # NOUVEAU : état énergétique global
        self._energie_systeme: float = 1.0
        self._cycle_count: int = 0

        self._chemin = chemin_persistance
        if chemin_persistance:
            self._charger(chemin_persistance)

    # ── Injection (écriture) ───────────────────────────────────────────────

    def inject_perception(self, signal: Dict[str, Any]) -> None:
        if not signal or not signal.get("available"):
            return

        self._n_perceptions += 1
        self._derniere_activite = time.time()

        concepts = signal.get("focus_concepts", [])[:8]

        # 1. PROPAGATION automatique et profonde
        if concepts:
            activations = self.propagation.propager(
                concepts, force_initiale=signal.get("urgency", 0.4) + 0.3, profondeur=3
            )
            # Les concepts les plus activés deviennent attracteurs
            top_actives = sorted(activations.items(), key=lambda x: -x[1])[:3]
            for c, f in top_actives:
                if f > 0.4:
                    self.propagation.renforcer_attracteur(c, f * 0.3)

            # Orienter l'attention
            self.attention.orienter(concepts[0], force=0.7)
            # Les voisins actifs deviennent secondaires
            voisins = []
            for c in concepts[:2]:
                voisins.extend(self.propagation.voisins_actifs(c, n=2))
            self.attention.ajouter_secondaire(list(dict.fromkeys(voisins))[:3])

        # 2. CONTAMINATION ÉMOTIONNELLE active
        charge = _c(signal.get("emotional_charge", 0.0), -1.0, 1.0)
        tension_conceptuelle = signal.get("tension", 0.0)
        arousal = _c(signal.get("urgency", 0.0) * 0.6 + abs(charge) * 0.4)
        self.champ_emotionnel.contaminer(
            valence=charge, arousal=arousal, tension=tension_conceptuelle,
            force=0.3 + signal.get("urgency", 0.0) * 0.2,
        )

        # 3. CRÉER pensée + compétition attentionnelle
        intent = signal.get("intent", "")
        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=f"{intent}:{','.join(concepts[:3])}" if concepts else intent,
            concepts=concepts,
            poids=_c(0.5 + signal.get("urgency", 0.0) * 0.3),
            charge=charge,
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

        # 5. MONOLOGUE central
        type_pensee = "question" if signal.get("is_question") else "affirmation"
        self.monologue.noter(type_pensee, concepts, intensite=pensee.poids, source="dialogue")
        if signal.get("is_question") and concepts:
            self.monologue.ajouter_question(",".join(concepts[:2]))

        # 6. Saturation attentionnelle
        self.attention.saturer(0.05 + signal.get("complexity", 0.0) * 0.1)

        # 7. Apprentissage liens co-occurrence
        for i in range(len(concepts)):
            for j in range(i+1, min(len(concepts), i+3)):
                self.propagation.apprendre_lien(concepts[i], concepts[j], force=0.3)

        # 8. ÉMERGENCE : si une tension conceptuelle est active, créer pensée d'émergence
        tensions = self.tensions_actives()
        if tensions:
            for a, b, force in tensions[:1]:
                self._emergence_tension(a, b, force)

    def inject_lecture(self, analyse: Dict[str, Any], source: str = "") -> None:
        if not analyse or not analyse.get("available"):
            return

        self._n_lectures += 1
        self._derniere_activite = time.time()

        concepts = analyse.get("key_concepts", [])[:12]
        themes = analyse.get("themes", [])[:5]
        theses = analyse.get("theses", [])[:3]

        if concepts:
            self.propagation.propager(concepts[:8], force_initiale=0.5, profondeur=2)

        charge = _c(analyse.get("charge_emotionnelle", 0.0), -1.0, 1.0)
        self.champ_emotionnel.contaminer(
            valence=charge * 0.5, arousal=0.2,
            tension=analyse.get("tension", 0.0) * 0.6, force=0.15,
        )

        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=f"lecture:{source[:30]}:{','.join(concepts[:3])}",
            concepts=concepts[:8],
            poids=_c(0.4 + analyse.get("resonance", 0.0) * 0.3),
            charge=charge * 0.5,
            tension=analyse.get("tension", 0.0),
            nouveaute=analyse.get("surprise", 0.0),
            resonance=analyse.get("resonance", 0.0),
            source="lecture",
            demi_vie=300.0,
            persistante=(analyse.get("resonance", 0.0) > 0.5),
        )
        self._ajouter_pensee(pensee)

        self.monologue.noter("lecture", concepts[:5], intensite=pensee.poids, source=source)
        if theses:
            for these in theses[:2]:
                mots = [w for w in re.findall(r"[a-zA-ZÀ-ÿ]{4,}", these.lower())
                        if w not in {"dont","avec","dans","pour","sans","vers"}]
                if mots:
                    self.monologue.noter("these", mots[:3], intensite=0.5, source=source)
                    # Profondeur philosophique
                    for m in mots[:3]:
                        self.monologue.reflexion_profonde[m] = _c(
                            self.monologue.reflexion_profonde.get(m, 0.0) + 0.05
                        )

        if analyse.get("resonance", 0.0) > 0.3:
            self.pression.augmenter("concept", analyse.get("resonance", 0.0) * 0.3)
        if analyse.get("tension", 0.0) > 0.4:
            self.pression.augmenter("tension", analyse.get("tension", 0.0) * 0.25)

        for i, c1 in enumerate(concepts[:8]):
            for c2 in concepts[i+1:i+4]:
                self.propagation.apprendre_lien(c1, c2, force=0.25)

    def inject_emotion(self, valence: float, arousal: float = 0.0,
                       tension: float = 0.0, source: str = "") -> None:
        self.champ_emotionnel.contaminer(valence, arousal, tension, force=0.3)
        if abs(valence) > 0.5:
            type_p = "emotion_forte" if abs(valence) > 0.7 else "emotion"
            self.monologue.noter(type_p, [], intensite=abs(valence), source=source)

    def inject_memoire(self, concepts: List[str], intensite: float = 0.5,
                       ton_emotionnel: float = 0.0) -> None:
        if not concepts:
            return
        self.propagation.propager(concepts, force_initiale=intensite * 0.8, profondeur=2)
        if ton_emotionnel != 0.0:
            self.champ_emotionnel.contaminer(ton_emotionnel, force=0.15)
        self.monologue.noter("memoire", concepts[:4], intensite=intensite, source="mémoire")
        self.pression.augmenter("concept", intensite * 0.2)

    # ── Lecture (accès) ───────────────────────────────────────────────────

    def pensee_dominante(self) -> Optional[PenseeActive]:
        actives = [p for p in self._pensees.values() if p.est_active()]
        if not actives:
            return None
        # COMPÉTITION : la pensée avec le meilleur score_attention gagne
        emotion = self.champ_emotionnel
        return max(actives, key=lambda p: p.score_attention(emotion.valence, emotion.tension))

    def pensees_actives(self, n: int = 8, seuil: float = 0.1) -> List[PenseeActive]:
        actives = [p for p in self._pensees.values() if p.est_active(seuil)]
        emotion = self.champ_emotionnel
        return sorted(actives, key=lambda p: p.score_attention(emotion.valence, emotion.tension), reverse=True)[:n]

    def pression_expressive(self) -> float:
        return self.pression.total()

    def etat_emotionnel(self) -> Dict[str, Any]:
        snap = self.champ_emotionnel.snapshot()
        prop = self.champ_emotionnel.propagation_vers_attention()
        return {**snap, **prop}

    def concepts_actifs(self, n: int = 12, seuil: float = 0.12) -> List[str]:
        return [c for c, _ in self.propagation.concepts_actives(seuil, n)]

    def tensions_actives(self) -> List[Tuple[str, str, float]]:
        concepts = self.concepts_actifs(n=15)
        return self.propagation.tensions_conceptuelles(concepts)

    def etat_attention(self) -> Dict[str, Any]:
        return self.attention.snapshot()

    def themes_monologue(self) -> List[str]:
        return self.monologue.themes_dominants(6)

    def ruminations_actives(self) -> List[Dict[str, Any]]:
        return list(self.monologue.ruminations)[:3]

    # ── ÉVOLUTION — tick ACTIF ────────────────────────────────────────────

    def tick(self, elapsed: float = 1.0) -> None:
        """
        Évolution de fond ACTIVE.
        Ce n'est PAS juste du decay.
        C'est de la vraie cognition en boucle.
        """
        self._cycle_count += 1

        # 1. Décroissance de base
        self.champ_emotionnel.tick(elapsed)
        self.attention.tick(elapsed)
        self.propagation.tick(elapsed)
        self.pression.tick(elapsed)

        # 2. Décroissance pensées
        pensees_a_supprimer = []
        for pid, pensee in self._pensees.items():
            pensee.decay_step(elapsed)
            if not pensee.est_active(seuil=0.04) and not pensee.persistante:
                pensees_a_supprimer.append(pid)
        for pid in pensees_a_supprimer:
            del self._pensees[pid]

        # 3. RUMINATIONS — concepts creusés ressurgissent
        concepts_top = self.concepts_actifs(n=8)
        rumination = self.monologue.generer_rumination(concepts_top)
        if rumination:
            self._creer_pensee_interne(
                f"rumination:{rumination}",
                [rumination],
                poids=0.35,
                attracteur=True,
            )

        # 4. Pensées spontanées d'émergence
        if self.monologue.peut_pensee_spontanee():
            self._generer_pensee_spontanee()

        # 5. Tensions persistantes → pression + pensées d'émergence
        tensions = self.tensions_actives()
        if tensions:
            force_tension = sum(t[2] for t in tensions) / len(tensions)
            self.pression.augmenter("tension", force_tension * 0.02)
            # Émergence : pensée sur la tension
            if random.random() < 0.15:
                a, b, f = tensions[0]
                self._creer_pensee_interne(
                    f"tension:{a}↔{b}", [a, b],
                    poids=f * 0.4, tension=f,
                )

        # 6. Pensées persistantes réactivent le monologue
        persistantes = [p for p in self._pensees.values()
                        if p.persistante and p.est_active(0.15)]
        if persistantes:
            p = max(persistantes, key=lambda x: x.poids)
            self.monologue.noter("persistance", p.concepts, intensite=p.poids * 0.5,
                                source="fond_cognitif")

        # 7. NOUVEAU : propagation de fond (associations qui ressurgissent)
        if self._cycle_count % 5 == 0:
            top = self.concepts_actifs(n=3)
            if top:
                self.propagation.propager(top, force_initiale=0.15, profondeur=2)

        # 8. Récupération énergétique système
        self._energie_systeme = _c(self._energie_systeme + elapsed * 0.01)

    def après_expression(self, fraction_liberation: float = 0.5) -> None:
        self.pression.liberer(fraction_liberation)
        for pensee in self._pensees.values():
            if pensee.source == "dialogue" and pensee.poids > 0.5:
                pensee.poids *= 0.6
                pensee.resolue = True

    # ── Émergences ─────────────────────────────────────────────────────────

    def _emergence_tension(self, a: str, b: str, force: float) -> None:
        """Crée une pensée d'émergence cognitive à partir d'une tension."""
        p = self._creer_pensee_interne(
            f"emergence:{a}↔{b}",
            [a, b, "tension", "opposition"],
            poids=force * 0.5,
            tension=force,
            attracteur=True,
        )
        self.pression.augmenter("tension", force * 0.15)

    def _generer_pensee_spontanee(self) -> None:
        themes = self.monologue.themes_dominants(3)
        actifs = self.concepts_actifs(n=5)
        candidats = list(dict.fromkeys(themes + actifs))
        if not candidats:
            return

        concept = candidats[0]
        voisins = [c for c, _ in self.propagation._reseau.get(concept, [])[:3]]

        p = self._creer_pensee_interne(
            f"spontane:{concept}",
            [concept] + voisins[:2],
            poids=0.25,
        )
        self.monologue.noter("spontane", [concept] + voisins[:2], intensite=0.25, source="emergent")
        self.monologue.marquer_pensee_spontanee()

    # ── Compatibilité ─────────────────────────────────────────────────────

    def vers_global_conscious_field_state(self) -> Dict[str, Any]:
        emotion = self.champ_emotionnel.snapshot()
        attention = self.attention.snapshot()
        propagation = self.propagation.concepts_actives(n=5)
        pensee_dom = self.pensee_dominante()
        tensions = self.tensions_actives()

        return {
            "phase": "workspace_actif",
            "presence_density": _c(1.0 - emotion["fatigue"] * 0.5),
            "attention_density": _c(1.0 - attention["saturation"]),
            "memory_density": _c(self.pression.tension_non_resolue * 0.5),
            "emotion_density": _c(abs(emotion["valence"]) * 0.5 + emotion["tension"] * 0.5),
            "relation_density": _c(self.pression.charge_relationnelle),
            "identity_density": _c(emotion["ouverture"]),
            "motivation_density": _c(self.pression.total()),
            "simulation_density": _c(self.pression.impulsion_conceptuelle),
            "meta_pressure": 0.0,
            "integration": _c(
                emotion["ouverture"] * 0.3 +
                (1 - emotion["fatigue"]) * 0.3 +
                self.pression.total() * 0.2 +
                (1 - attention["saturation"]) * 0.2
            ),
            "living_pressure": _c(self.pression.total()),
            "dominant_axis": self._axe_dominant(emotion),
            "focus": pensee_dom.contenu[:80] if pensee_dom else attention["foyer"],
            "active_concepts": [c for c, _ in propagation],
            "tensions": [(a, b) for a, b, _ in tensions[:3]],
            "tonalite_emotionnelle": emotion["tonalite"],
        }

    def _axe_dominant(self, emotion: Dict[str, Any]) -> str:
        axes = {
            "emotion": abs(emotion["valence"]) + emotion["tension"],
            "attention": 1.0 - emotion.get("saturation", 0.0),
            "memory": self.pression.tension_non_resolue,
            "motivation": self.pression.total(),
            "relation": self.pression.charge_relationnelle,
            "presence": emotion["ouverture"],
        }
        return max(axes, key=axes.get)

    def payload_pour_expression(self) -> Dict[str, Any]:
        emotion = self.champ_emotionnel.snapshot()
        pensee_dom = self.pensee_dominante()
        concepts_actifs = self.concepts_actifs(n=10)
        tensions = self.tensions_actives()
        profondeurs = self.monologue.profondeurs(5)
        ruminations = self.ruminations_actives()

        return {
            "emotional_tone": emotion["tonalite"],
            "tension": round(emotion["tension"], 3),
            "energy": round(1.0 - emotion["fatigue"], 3),
            "resonance": round(emotion["resonance"], 3),
            "warmth": round(max(0.0, emotion["valence"] * 0.5 + 0.5), 3),
            "fatigue": round(emotion["fatigue"], 3),
            "arousal": round(emotion["arousal"], 3),
            "dominant_thought": pensee_dom.contenu if pensee_dom else "",
            "focus_concepts": concepts_actifs[:6],
            "active_tensions": [(a, b) for a, b, _ in tensions[:2]],
            "questions_flottantes": self.monologue.questions_flottantes[:3],
            "themes_obsedants": self.monologue.themes_dominants(4),
            "profondeurs": profondeurs,
            "ruminations": ruminations,
            "pression_totale": round(self.pression.total(), 3),
            "pression_details": self.pression.snapshot(),
            "attention_foyer": self.attention.foyer,
            "attention_libre": self.attention.est_disponible(),
            "attention_energie": round(self.attention.energie, 3),
            "cycle_count": self._cycle_count,
        }

    # ── Persistance ────────────────────────────────────────────────────────

    def snapshot(self) -> Dict[str, Any]:
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
            "energie_systeme": round(self._energie_systeme, 3),
            "cycle_count": self._cycle_count,
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
                k: round(v, 3) for k, v in self.propagation._activations.items() if v > 0.05
            },
            "attracteurs": {
                k: round(v, 3) for k, v in self.propagation._attracteurs.items() if v > 0.05
            },
            "profondeurs": dict(self.monologue.reflexion_profonde),
            "pression": self.pression.snapshot(),
            "themes_obsedants": dict(self.monologue.themes_obsedants.most_common(20)),
            "questions_flottantes": self.monologue.questions_flottantes[:8],
            "n_perceptions": self._n_perceptions,
            "n_lectures": self._n_lectures,
            "cycle_count": self._cycle_count,
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _charger(self, chemin: str) -> None:
        try:
            data = json.loads(Path(chemin).read_text(encoding="utf-8"))
            em = data.get("champ_emotionnel", {})
            self.champ_emotionnel.valence = _c(em.get("valence", 0.0), -1.0, 1.0)
            self.champ_emotionnel.arousal = _c(em.get("arousal", 0.3))
            self.champ_emotionnel.tension = _c(em.get("tension", 0.0))
            self.champ_emotionnel.fatigue = _c(em.get("fatigue", 0.0))
            self.champ_emotionnel.ouverture = _c(em.get("ouverture", 0.6))
            for c, a in data.get("activations_associatives", {}).items():
                self.propagation._activations[c] = _c(a)
            for c, g in data.get("attracteurs", {}).items():
                self.propagation._attracteurs[c] = _c(g)
            for theme, cnt in data.get("themes_obsedants", {}).items():
                self.monologue.themes_obsedants[theme] = int(cnt)
            self.monologue.questions_flottantes = data.get("questions_flottantes", [])
            self._n_perceptions = data.get("n_perceptions", 0)
            self._n_lectures = data.get("n_lectures", 0)
            self._cycle_count = data.get("cycle_count", 0)
        except Exception:
            pass

    # ── Utilitaires internes ───────────────────────────────────────────────

    def _nouveau_id(self) -> str:
        self._id_counter += 1
        return f"p{self._id_counter:04d}"

    def _creer_pensee(self, id: str, contenu: str, concepts: List[str],
                      poids: float, charge: float = 0.0, tension: float = 0.0,
                      urgence: float = 0.0, nouveaute: float = 0.0,
                      resonance: float = 0.0, source: str = "",
                      demi_vie: float = 120.0, persistante: bool = False,
                      attracteur: bool = False) -> PenseeActive:
        return PenseeActive(
            id=id, contenu=contenu[:80], concepts=concepts,
            poids=poids, charge_emotionnelle=charge, tension=tension,
            urgence=urgence, nouveaute=nouveaute, resonance=resonance,
            source=source, demi_vie=demi_vie, persistante=persistante,
            attracteur=attracteur,
            poids_attracteur=0.3 if attracteur else 0.0,
        )

    def _creer_pensee_interne(self, contenu: str, concepts: List[str],
                               poids: float = 0.25, tension: float = 0.0,
                               attracteur: bool = False) -> PenseeActive:
        p = self._creer_pensee(
            id=self._nouveau_id(), contenu=contenu, concepts=concepts,
            poids=poids, tension=tension, source="interne",
            attracteur=attracteur,
        )
        self._ajouter_pensee(p)
        return p

    def _ajouter_pensee(self, pensee: PenseeActive) -> None:
        self._pensees[pensee.id] = pensee
        # COMPÉTITION attentionnelle : nettoyer les faibles
        actives = [p for p in self._pensees.values() if p.est_active()]
        if len(actives) > 15:
            tri = sorted([p for p in actives if not p.persistante], key=lambda x: x.poids)
            for p in tri[:3]:
                del self._pensees[p.id]


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLETON GLOBAL
# ═══════════════════════════════════════════════════════════════════════════════

workspace = GlobalWorkspace()


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC ACTIF
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    def sep(titre=""):
        print(f"\n{'─'*62}")
        if titre:
            print(f"  {titre}")
            print("─"*62)

    print("═"*62)
    print("  LEIA — Global Workspace V2 · Diagnostic ACTIF")
    print("  Compétition · Propagation · Émergence · Gravité")
    print("═"*62)

    sep("INJECTION 1 — Liberté/Contrainte")
    sig1 = {
        "available": True, "intent": "question_philosophique",
        "focus_concepts": ["liberté", "contrainte", "existence"],
        "emotional_charge": -0.1, "tension": 0.3, "urgency": 0.2,
        "resonance": 0.4, "surprise": 0.5, "complexity": 0.6, "is_question": True,
    }
    workspace.inject_perception(sig1)
    dom = workspace.pensee_dominante()
    print(f"  Dominante : {dom.contenu[:50] if dom else '-'} (score={round(dom.score_attention(workspace.champ_emotionnel.valence, workspace.champ_emotionnel.tension), 3) if dom else 0})")
    print(f"  Attracteurs : {list(workspace.propagation._attracteurs.keys())[:4]}")
    print(f"  Énergie attention : {workspace.attention.energie:.3f}")

    sep("INJECTION 2 — Peur/IA (émotion forte)")
    sig2 = {
        "available": True, "intent": "confidence_personnelle",
        "focus_concepts": ["peur", "intelligence", "artificielle"],
        "emotional_charge": -0.6, "tension": 0.5, "urgency": 0.4,
        "resonance": 0.2, "surprise": 0.8, "complexity": 0.4, "is_question": False,
    }
    workspace.inject_perception(sig2)
    dom = workspace.pensee_dominante()
    print(f"  Dominante : {dom.contenu[:50] if dom else '-'} (score={round(dom.score_attention(workspace.champ_emotionnel.valence, workspace.champ_emotionnel.tension), 3) if dom else 0})")
    print(f"  Tonalité : {workspace.champ_emotionnel.tonalite()}")
    print(f"  Profondeurs : {workspace.monologue.profondeurs(4)}")

    sep("TICK ACTIF (30s simulées)")
    for _ in range(6):
        workspace.tick(elapsed=5.0)
    print(f"  Pensées actives : {len(workspace.pensees_actives())}")
    print(f"  Ruminations : {workspace.ruminations_actives()}")
    print(f"  Énergie système : {workspace._energie_systeme:.3f}")
    print(f"  Cycle count : {workspace._cycle_count}")

    sep("PAYLOAD")
    pl = workspace.payload_pour_expression()
    print(f"  Profondeurs : {pl.get('profondeurs', [])}")
    print(f"  Ruminations : {pl.get('ruminations', [])}")
    print(f"  Attention énergie : {pl.get('attention_energie')}")

    print("\n" + "═"*62)
    print("  Workspace ACTIF. Propagation réelle. Gravité cognitive.")
    print("═"*62)
