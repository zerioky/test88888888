"""
memory_hierarchy.py — V1
========================
Hierarchie mémorielle pondérée pour Leia.

Corrige la faille fondamentale : toutes les mémoires étaient traitées
avec le même poids (seuil plat à 0.04, décroissance uniforme de 0.985).

Ce module introduit :
  1. Catégorisation des épisodes (trauma / pivot / ordinaire / bruit)
  2. Décroissance différentielle par catégorie
  3. Protection des mémoires fondatrices (jamais oubliées)
  4. Pont unifié entre les 4 mémoires parallèles (narrative, causale,
     affective, subjective) — elles se signalent maintenant mutuellement
  5. Consolidation nocturne simulée : réorganisation douce entre échanges

Aucune phrase préécrite. Aucun fallback conversationnel.
"""

from __future__ import annotations

import json
import math
import time
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f if not (math.isnan(f) or math.isinf(f)) else lo))
    except Exception:
        return lo


# ─────────────────────────────────────────────
# Catégories de mémoire avec poids de rétention
# ─────────────────────────────────────────────

class MemoryCategory(Enum):
    FOUNDATIONAL = "foundational"   # Premier échange, moments définitoires — jamais oubliés
    TRAUMA       = "trauma"         # Ruptures, blessures profondes — décroissance très lente
    PIVOT        = "pivot"          # Changements de direction, décisions importantes
    MEANINGFUL   = "meaningful"     # Moments riches mais non-pivots
    ORDINARY     = "ordinary"       # Échanges normaux
    NOISE        = "noise"          # Bruit de surface — décroissance rapide

# Taux de décroissance par cycle (multiplié à l'impact chaque exchange)
_DECAY_RATE: Dict[str, float] = {
    MemoryCategory.FOUNDATIONAL.value: 0.0,     # immuable
    MemoryCategory.TRAUMA.value:       0.998,   # quasi-permanent
    MemoryCategory.PIVOT.value:        0.993,
    MemoryCategory.MEANINGFUL.value:   0.985,   # taux original
    MemoryCategory.ORDINARY.value:     0.970,
    MemoryCategory.NOISE.value:        0.940,
}

# Seuil de survie par catégorie
_SURVIVAL_THRESHOLD: Dict[str, float] = {
    MemoryCategory.FOUNDATIONAL.value: 0.0,    # jamais purgé
    MemoryCategory.TRAUMA.value:       0.005,
    MemoryCategory.PIVOT.value:        0.015,
    MemoryCategory.MEANINGFUL.value:   0.040,  # seuil original
    MemoryCategory.ORDINARY.value:     0.080,
    MemoryCategory.NOISE.value:        0.150,
}


def classify_episode(episode: Dict[str, Any]) -> str:
    """
    Infère la catégorie d'un épisode depuis ses métadonnées.
    Priorité : catégorie explicite > signaux implicites.
    """
    # Catégorie déjà assignée
    if "category" in episode and episode["category"] in _DECAY_RATE:
        return episode["category"]

    impact = float(episode.get("impact", 0.0))
    is_unfinished = bool(episode.get("unfinished", False))
    emotional_tone = str(episode.get("emotional_tone", "neutral"))
    topic = str(episode.get("topic", "")).lower()
    exchange_index = int(episode.get("exchange_index", 999))

    # Fondateur : les 3 premiers échanges sont toujours conservés
    if exchange_index <= 3:
        return MemoryCategory.FOUNDATIONAL.value

    # Trauma : impact très fort + ton négatif ou rupture
    if impact > 0.75 and emotional_tone in {"negative", "intense", "rupture", "grief", "shock"}:
        return MemoryCategory.TRAUMA.value

    # Pivot : impact fort + changement thématique ou décision
    if impact > 0.60 and (is_unfinished or "choix" in topic or "décision" in topic or "découvert" in topic):
        return MemoryCategory.PIVOT.value

    # Meaningful : impact moyen-fort
    if impact > 0.35:
        return MemoryCategory.MEANINGFUL.value

    # Bruit : impact très faible
    if impact < 0.08:
        return MemoryCategory.NOISE.value

    return MemoryCategory.ORDINARY.value


@dataclass
class HierarchicalMemory:
    """
    Couche de hiérarchisation posée au-dessus des épisodes narratifs.
    S'intègre dans PersonalNarrative sans le remplacer.
    """
    foundational: List[Dict[str, Any]] = field(default_factory=list)   # immuables
    trauma_pool: deque = field(default_factory=lambda: deque(maxlen=20))
    pivot_pool: deque = field(default_factory=lambda: deque(maxlen=30))
    meaningful_pool: deque = field(default_factory=lambda: deque(maxlen=40))
    # ordinary + noise restent dans le deque standard de PersonalNarrative

    def absorb_episode(self, episode: Dict[str, Any]) -> str:
        """Classe et stocke un épisode. Retourne la catégorie assignée."""
        cat = classify_episode(episode)
        episode["category"] = cat

        if cat == MemoryCategory.FOUNDATIONAL.value:
            # Évite les doublons par exchange_index
            indices = {e.get("exchange_index") for e in self.foundational}
            if episode.get("exchange_index") not in indices:
                self.foundational.append(dict(episode))
        elif cat == MemoryCategory.TRAUMA.value:
            self.trauma_pool.appendleft(dict(episode))
        elif cat == MemoryCategory.PIVOT.value:
            self.pivot_pool.appendleft(dict(episode))
        elif cat == MemoryCategory.MEANINGFUL.value:
            self.meaningful_pool.appendleft(dict(episode))

        return cat

    def weighted_forget(self, episodes: deque) -> deque:
        """
        Remplace organic_forget() avec décroissance différentielle.
        Retourne le deque filtré.
        """
        result = []
        for ep in episodes:
            cat = classify_episode(ep)
            decay = _DECAY_RATE.get(cat, 0.985)
            threshold = _SURVIVAL_THRESHOLD.get(cat, 0.04)

            # Décroissance différentielle
            ep["impact"] = round(float(ep.get("impact", 0.0)) * decay, 5)

            # Fondateur : jamais purgé
            if cat == MemoryCategory.FOUNDATIONAL.value:
                result.append(ep)
                continue

            # Survivance selon seuil de catégorie
            if float(ep.get("impact", 0.0)) > threshold or ep.get("unfinished"):
                result.append(ep)

        return deque(result, maxlen=episodes.maxlen)

    def get_high_weight_contexts(self) -> List[Dict[str, Any]]:
        """
        Exporte les mémoires à fort poids pour influencer l'expression.
        Toujours disponible — indépendant du contexte immédiat.
        """
        contexts = []
        for ep in self.foundational:
            contexts.append({"weight": 1.0, "category": "foundational", **ep})
        for ep in list(self.trauma_pool)[:5]:
            contexts.append({"weight": 0.85, "category": "trauma", **ep})
        for ep in list(self.pivot_pool)[:8]:
            contexts.append({"weight": 0.65, "category": "pivot", **ep})
        return contexts

    def snapshot(self) -> Dict[str, Any]:
        return {
            "foundational_count": len(self.foundational),
            "trauma_count": len(self.trauma_pool),
            "pivot_count": len(self.pivot_pool),
            "meaningful_count": len(self.meaningful_pool),
        }


# ─────────────────────────────────────────────────────────────
# Pont entre les 4 mémoires parallèles (narrative, causale,
# affective, subjective) — elles se signalent mutuellement
# ─────────────────────────────────────────────────────────────

class MemoryBridge:
    """
    Corrige le problème de fragmentation : 4 mémoires parallèles
    qui ne se parlaient pas.

    Ce pont :
    - Reçoit les signaux de chaque couche
    - Détecte les cohérences/incohérences inter-mémoires
    - Produit un signal unifié utilisable par l'expression
    - Déclenche une consolidation quand les couches divergent
    """

    def __init__(self, storage_path: str = "data/memory_bridge.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Registre des correspondances inter-mémoires
        # clé : topic/concept, valeur : présence dans chaque couche
        self.cross_register: Dict[str, Dict[str, float]] = {}

        # Divergences détectées (ex: mémoire affective forte mais narrative absente)
        self.divergences: deque = deque(maxlen=40)

        # Score de cohérence global entre les couches (0 = fragmenté, 1 = unifié)
        self.coherence_score: float = 0.5

        # Consolidations effectuées
        self.consolidations: deque = deque(maxlen=20)

        self._load()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.cross_register = data.get("cross_register", {})
                self.divergences = deque(data.get("divergences", [])[-40:], maxlen=40)
                self.coherence_score = float(data.get("coherence_score", 0.5))
        except Exception:
            pass

    def _save(self) -> None:
        try:
            payload = {
                "cross_register": dict(list(self.cross_register.items())[-200:]),
                "divergences": list(self.divergences),
                "coherence_score": round(self.coherence_score, 4),
                "saved_at": time.time(),
            }
            self.storage_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def register_memory_signal(
        self,
        topic: str,
        layer: str,  # "narrative" | "causal" | "affective" | "subjective"
        strength: float,
    ) -> None:
        """Enregistre la présence d'un topic dans une couche mémorielle."""
        if not topic or len(topic) < 2:
            return
        key = topic[:60].lower().strip()
        if key not in self.cross_register:
            self.cross_register[key] = {
                "narrative": 0.0, "causal": 0.0, "affective": 0.0, "subjective": 0.0
            }
        self.cross_register[key][layer] = _clamp(
            self.cross_register[key].get(layer, 0.0) * 0.85 + strength * 0.15
        )

    def detect_divergences(self) -> List[Dict[str, Any]]:
        """
        Identifie les topics où les couches divergent fortement.
        Ex: fort en affectif, absent en narratif = souvenir émotionnel non-verbalisé.
        """
        new_divergences = []
        for topic, layers in self.cross_register.items():
            values = list(layers.values())
            if not values:
                continue
            max_v = max(values)
            min_v = min(values)
            spread = max_v - min_v

            if spread > 0.35 and max_v > 0.40:
                dominant_layer = max(layers, key=layers.get)
                absent_layers = [l for l, v in layers.items() if v < 0.15]
                if absent_layers:
                    new_divergences.append({
                        "topic": topic,
                        "spread": round(spread, 3),
                        "dominant": dominant_layer,
                        "absent_from": absent_layers,
                        "detected_at": time.time(),
                    })

        self.divergences.extend(new_divergences[-5:])
        # Mise à jour du score de cohérence
        if new_divergences:
            self.coherence_score = _clamp(self.coherence_score - 0.02 * len(new_divergences))
        else:
            self.coherence_score = _clamp(self.coherence_score + 0.005)

        return new_divergences

    def consolidate(self) -> Optional[Dict[str, Any]]:
        """
        Consolidation douce : rapproche les couches divergentes.
        Simule ce que fait le cerveau pendant le sommeil.
        Appelé entre les échanges (background_life ou cycle idle).
        """
        if not self.divergences:
            return None

        # Prend la divergence la plus ancienne non résolue
        oldest = None
        for div in self.divergences:
            if not div.get("resolved"):
                oldest = div
                break

        if not oldest:
            return None

        topic = oldest["topic"]
        dominant = oldest["dominant"]

        # Renforce légèrement les couches absentes depuis la couche dominante
        if topic in self.cross_register:
            dominant_strength = self.cross_register[topic].get(dominant, 0.0)
            for absent_layer in oldest.get("absent_from", []):
                self.cross_register[topic][absent_layer] = _clamp(
                    self.cross_register[topic].get(absent_layer, 0.0) + dominant_strength * 0.12
                )

        oldest["resolved"] = True
        consolidation = {
            "topic": topic,
            "type": "cross_layer_bridge",
            "from": dominant,
            "to": oldest.get("absent_from", []),
            "at": time.time(),
        }
        self.consolidations.appendleft(consolidation)
        self.coherence_score = _clamp(self.coherence_score + 0.015)
        self._save()
        return consolidation

    def unified_signal(self, topic: str) -> Dict[str, Any]:
        """
        Signal mémoriel unifié pour un topic donné.
        Agrège toutes les couches avec pondération par fiabilité.
        """
        key = topic[:60].lower().strip() if topic else ""
        layers = self.cross_register.get(key, {})
        if not layers:
            return {
                "unified_strength": 0.0,
                "coherent": True,
                "dominant_layer": None,
                "spread": 0.0,
                "available": False,
            }

        values = list(layers.values())
        unified = (
            layers.get("narrative", 0.0) * 0.30
            + layers.get("causal", 0.0) * 0.28
            + layers.get("affective", 0.0) * 0.25
            + layers.get("subjective", 0.0) * 0.17
        )
        spread = max(values) - min(values)
        dominant = max(layers, key=layers.get) if values else None

        return {
            "unified_strength": round(_clamp(unified), 4),
            "coherent": spread < 0.25,
            "dominant_layer": dominant,
            "spread": round(spread, 3),
            "layers": {k: round(v, 3) for k, v in layers.items()},
            "available": True,
        }

    def signal(self, topics: Optional[List[str]] = None) -> Dict[str, Any]:
        """Signal exportable vers le core / l'expression."""
        recent_divergences = [d for d in list(self.divergences)[-5:] if not d.get("resolved")]
        top_unified = {}
        if topics:
            for t in topics[:5]:
                sig = self.unified_signal(t)
                if sig["available"]:
                    top_unified[t] = sig

        return {
            "coherence_score": round(self.coherence_score, 4),
            "active_divergences": len(recent_divergences),
            "divergence_topics": [d["topic"] for d in recent_divergences],
            "unified_topics": top_unified,
            "available": True,
        }
