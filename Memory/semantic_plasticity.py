"""
semantic_plasticity.py — V1
============================
Plasticité sémantique pour Leia.

Corrige la faille : les moteurs de compréhension étaient statiques.
Leia classifiait ce qu'on lui avait appris, ne découvrait pas vraiment.
Pas de mise à jour de modèle interne après les échanges.

Ce module introduit :
  1. Graphe de concepts léger qui évolue par échanges
     (nouveaux concepts, nouvelles connexions, décroissance des non-utilisés)
  2. Détection de nouveauté conceptuelle (Leia remarque les idées qu'elle
     n'a pas encore traitées)
  3. Transformation des associations existantes sous l'effet de nouveaux
     contextes (un mot peut changer de résonance émotionnelle)
  4. Signal de "surprise interne" quand une connexion inattendue émerge
  5. Mémoire des transformations — trace de croissance réelle

Différence clé : ce n'est pas de l'apprentissage supervisé. C'est de la
réorganisation associative bottom-up — plus proche de ce que fait un cerveau
que ce que fait un classificateur.

Aucune phrase préécrite.
"""

from __future__ import annotations

import json
import math
import random
import time
from collections import defaultdict, deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f if not (math.isnan(f) or math.isinf(f)) else lo))
    except Exception:
        return lo


@dataclass
class ConceptNode:
    """Un nœud dans le graphe conceptuel de Leia."""
    label: str
    activation: float = 0.5         # Niveau d'activation courant
    emotional_tone: float = 0.0     # Coloration émotionnelle (-1 négatif, +1 positif)
    familiarity: float = 0.0        # Combien de fois vu (normalisé)
    last_seen: float = field(default_factory=time.time)
    first_seen: float = field(default_factory=time.time)
    surprise_count: int = 0         # Fois où ce concept a été surprenant
    transformed: bool = False       # A-t-il changé de sens depuis la première occurrence ?

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "activation": round(self.activation, 4),
            "emotional_tone": round(self.emotional_tone, 4),
            "familiarity": round(self.familiarity, 4),
            "last_seen": self.last_seen,
            "first_seen": self.first_seen,
            "surprise_count": self.surprise_count,
            "transformed": self.transformed,
        }


class SemanticPlasticity:
    """
    Graphe associatif évolutif — la 'mémoire sémantique vivante' de Leia.
    """

    def __init__(self, storage_path: str = "data/semantic_plasticity.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Graphe : concept → {concept_voisin: poids_association}
        self.graph: Dict[str, Dict[str, float]] = defaultdict(dict)

        # Nœuds avec métadonnées
        self.nodes: Dict[str, ConceptNode] = {}

        # File des surprises récentes (connexions inattendues)
        self.recent_surprises: deque = deque(maxlen=20)

        # Transformations enregistrées (un concept qui a changé de sens)
        self.transformations: deque = deque(maxlen=30)

        # Concepts totalement nouveaux depuis la dernière session
        self.novel_this_session: Set[str] = set()

        # Pression de nouveauté globale
        self.novelty_pressure: float = 0.0

        # Dernier signal de surprise interne
        self.last_surprise_signal: Optional[Dict[str, Any]] = None

        # Compteur d'échanges pour la décroissance
        self._exchange_count: int = 0

        self._load()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                # Restauration du graphe
                raw_graph = data.get("graph", {})
                self.graph = defaultdict(dict, {k: dict(v) for k, v in raw_graph.items()})
                # Restauration des nœuds
                for label, nd in data.get("nodes", {}).items():
                    try:
                        self.nodes[label] = ConceptNode(**nd)
                    except Exception:
                        self.nodes[label] = ConceptNode(label=label)
                self.transformations = deque(data.get("transformations", [])[-30:], maxlen=30)
                self.novelty_pressure = float(data.get("novelty_pressure", 0.0))
                self._exchange_count = int(data.get("exchange_count", 0))
        except Exception:
            pass

    def _save(self) -> None:
        try:
            # Limite la taille du graphe (max 400 concepts)
            if len(self.nodes) > 400:
                # Supprime les moins actifs et peu familiers
                sorted_nodes = sorted(
                    self.nodes.items(),
                    key=lambda x: x[1].familiarity + x[1].activation,
                )
                to_remove = [n for n, _ in sorted_nodes[:len(self.nodes) - 400]]
                for n in to_remove:
                    del self.nodes[n]
                    if n in self.graph:
                        del self.graph[n]
                    for neighbors in self.graph.values():
                        neighbors.pop(n, None)

            payload = {
                "graph": {k: dict(v) for k, v in self.graph.items()},
                "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
                "transformations": list(self.transformations),
                "novelty_pressure": round(self.novelty_pressure, 4),
                "exchange_count": self._exchange_count,
                "saved_at": time.time(),
            }
            self.storage_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def _extract_concepts(self, text: str) -> List[str]:
        """
        Extraction légère de concepts depuis le texte.
        Mots significatifs (> 4 chars), normalisés, dédoublonnés.
        Pas de NLP externe requis.
        """
        import re
        words = re.findall(r'\b[a-zA-ZÀ-ÿ]{4,}\b', text.lower())
        # Filtrage des mots très fréquents / fonctionnels
        stopwords = {
            "avec", "dans", "pour", "mais", "donc", "alors", "comme",
            "plus", "bien", "aussi", "être", "avoir", "faire", "tout",
            "très", "cette", "vous", "nous", "leur", "elles", "dans",
            "that", "this", "with", "from", "have", "been", "they", "will",
            "sont", "peut", "même", "dont", "vers", "entre",
        }
        seen: Set[str] = set()
        result = []
        for w in words:
            if w not in stopwords and w not in seen:
                seen.add(w)
                result.append(w)
        return result[:20]  # Limite à 20 concepts par échange

    def process_exchange(
        self,
        user_input: str,
        leia_response: str,
        emotional_tone: float = 0.0,
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Met à jour le graphe sémantique après un échange.
        Retourne un signal avec les nouveautés et surprises détectées.
        """
        self._exchange_count += 1
        context = context or {}

        # Extraction des concepts
        input_concepts = self._extract_concepts(user_input)
        response_concepts = self._extract_concepts(leia_response)
        all_concepts = list(dict.fromkeys(input_concepts + response_concepts))

        new_concepts = []
        transformations_this_cycle = []
        surprise_connections = []

        # Mise à jour des nœuds
        for concept in all_concepts:
            is_new = concept not in self.nodes

            if is_new:
                self.nodes[concept] = ConceptNode(
                    label=concept,
                    activation=0.6,
                    emotional_tone=_clamp(emotional_tone, -1.0, 1.0),
                    familiarity=0.05,
                )
                new_concepts.append(concept)
                self.novel_this_session.add(concept)
            else:
                node = self.nodes[concept]
                old_tone = node.emotional_tone

                # Mise à jour de l'activation et familiarité
                node.activation = _clamp(node.activation * 0.7 + 0.6 * 0.3)
                node.familiarity = _clamp(node.familiarity + 0.03)
                node.last_seen = time.time()

                # Détection de transformation : si le ton émotionnel change significativement
                new_tone = _clamp(
                    old_tone * 0.80 + emotional_tone * 0.20, -1.0, 1.0
                )
                tone_delta = abs(new_tone - old_tone)
                if tone_delta > 0.18 and node.familiarity > 0.15:
                    node.transformed = True
                    node.surprise_count += 1
                    transformation = {
                        "concept": concept,
                        "old_tone": round(old_tone, 3),
                        "new_tone": round(new_tone, 3),
                        "delta": round(tone_delta, 3),
                        "at": time.time(),
                    }
                    self.transformations.appendleft(transformation)
                    transformations_this_cycle.append(transformation)

                node.emotional_tone = new_tone

        # Création de nouvelles associations entre co-occurrences
        for i, c1 in enumerate(all_concepts):
            for c2 in all_concepts[i+1:i+5]:  # Fenêtre de co-occurrence
                if c1 == c2:
                    continue

                old_weight = self.graph[c1].get(c2, 0.0)
                is_new_connection = old_weight < 0.05

                # Renforcement de l'association
                new_weight = _clamp(old_weight * 0.85 + 0.25 * 0.15)
                self.graph[c1][c2] = round(new_weight, 4)
                self.graph[c2][c1] = round(new_weight, 4)

                # Détection de surprise : connexion entre concepts émotionnellement distants
                if (is_new_connection and c1 in self.nodes and c2 in self.nodes
                        and self.nodes[c1].familiarity > 0.10
                        and self.nodes[c2].familiarity > 0.10):
                    tone_distance = abs(
                        self.nodes[c1].emotional_tone - self.nodes[c2].emotional_tone
                    )
                    if tone_distance > 0.35:
                        surprise = {
                            "concept_a": c1,
                            "concept_b": c2,
                            "tone_distance": round(tone_distance, 3),
                            "type": "unexpected_bridge",
                            "at": time.time(),
                        }
                        self.recent_surprises.appendleft(surprise)
                        surprise_connections.append(surprise)

        # Décroissance des concepts non utilisés (tous les 10 échanges)
        if self._exchange_count % 10 == 0:
            self._decay_inactive()

        # Mise à jour de la pression de nouveauté
        novelty_delta = len(new_concepts) * 0.04 + len(surprise_connections) * 0.06
        self.novelty_pressure = _clamp(
            self.novelty_pressure * 0.82 + novelty_delta * 0.18
        )

        # Signal de surprise interne si connexion inattendue
        surprise_signal = None
        if surprise_connections:
            most_surprising = max(surprise_connections, key=lambda s: s["tone_distance"])
            surprise_signal = {
                "has_surprise": True,
                "connection": most_surprising,
                "intensity": round(most_surprising["tone_distance"] * 0.8, 4),
            }
            self.last_surprise_signal = surprise_signal

        # Sauvegarde périodique
        if self._exchange_count % 5 == 0:
            self._save()

        return {
            "new_concepts": new_concepts[:5],
            "new_concepts_count": len(new_concepts),
            "transformations": transformations_this_cycle,
            "surprise_signal": surprise_signal,
            "novelty_pressure": round(self.novelty_pressure, 4),
            "graph_size": len(self.nodes),
        }

    def _decay_inactive(self) -> None:
        """Décroissance des concepts non utilisés récemment."""
        now = time.time()
        to_remove = []
        for label, node in self.nodes.items():
            age_hours = (now - node.last_seen) / 3600
            if age_hours > 2:  # Inactif depuis > ~2h de session
                node.activation = _clamp(node.activation * 0.88)
                node.familiarity = _clamp(node.familiarity * 0.97)
                if node.activation < 0.05 and node.familiarity < 0.05:
                    to_remove.append(label)
        for label in to_remove:
            del self.nodes[label]
            self.graph.pop(label, None)

    def impregnate(self, concept: str, source: str = "", intensity: float = 0.5) -> None:
        """Enregistre ou renforce un concept isolé dans le graphe (API learning_bridge)."""
        concept = concept.strip().lower()
        if not concept:
            return
        if concept not in self.nodes:
            self.nodes[concept] = ConceptNode(
                label=concept,
                activation=_clamp(intensity),
                familiarity=0.05,
            )
            self.novel_this_session.add(concept)
        else:
            node = self.nodes[concept]
            node.activation = _clamp(node.activation * 0.7 + intensity * 0.3)
            node.familiarity = _clamp(node.familiarity + 0.02)
            node.last_seen = time.time()

    def connect(self, c1: str, c2: str, weight: float = 0.1, context: str = "") -> None:
        """Crée ou renforce une liaison entre deux concepts (API learning_bridge)."""
        c1, c2 = c1.strip().lower(), c2.strip().lower()
        if not c1 or not c2 or c1 == c2:
            return
        for c in (c1, c2):
            if c not in self.nodes:
                self.nodes[c] = ConceptNode(label=c, activation=0.4, familiarity=0.03)
        old = self.graph[c1].get(c2, 0.0)
        new_w = _clamp(old + weight * 0.15)
        self.graph[c1][c2] = round(new_w, 4)
        self.graph[c2][c1] = round(new_w, 4)

    def get_resonant_concepts(self, input_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retourne les concepts du graphe qui résonnent le plus avec le texte.
        Utilisable pour enrichir la génération de réponse.
        """
        input_concepts = set(self._extract_concepts(input_text))
        resonances = []

        for concept, node in self.nodes.items():
            if concept in input_concepts:
                continue  # Déjà dans l'input

            # Résonance directe : voisin d'un concept dans l'input
            direct_neighbors = set(self.graph.get(concept, {}).keys())
            overlap = len(direct_neighbors & input_concepts)
            if overlap > 0:
                neighbor_weight = sum(
                    self.graph[concept].get(c, 0.0)
                    for c in input_concepts if c in self.graph[concept]
                )
                resonances.append({
                    "concept": concept,
                    "resonance": round(_clamp(neighbor_weight * 0.5 + node.activation * 0.3 + node.familiarity * 0.2), 4),
                    "emotional_tone": round(node.emotional_tone, 3),
                    "is_transformed": node.transformed,
                })

        resonances.sort(key=lambda x: x["resonance"], reverse=True)
        return resonances[:top_k]

    def signal(self, current_input: str = "") -> Dict[str, Any]:
        """Signal exportable vers le core."""
        recent_surprises = list(self.recent_surprises)[:3]
        recent_transforms = list(self.transformations)[:3]

        return {
            "graph_size": len(self.nodes),
            "novelty_pressure": round(self.novelty_pressure, 4),
            "novel_this_session": len(self.novel_this_session),
            "recent_surprises": recent_surprises,
            "recent_transformations": recent_transforms,
            "has_live_surprise": bool(
                recent_surprises and
                (time.time() - recent_surprises[0].get("at", 0)) < 120
            ),
            "resonant_concepts": self.get_resonant_concepts(current_input, top_k=3) if current_input else [],
            "available": True,
        }
