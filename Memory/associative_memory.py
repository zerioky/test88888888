"""
associative_memory.py — V18
=============================
Mémoire associative hebbienne avec propagation d'activation.

Principe : "ce qui s'active ensemble se lie ensemble"
Chaque fois que deux concepts apparaissent dans le même contexte
(échange, page de livre, état interne), leur lien se renforce.

Quand un concept est activé (par un mot de l'utilisateur, un livre,
un état émotionnel), l'activation se propage aux voisins proches —
comme un réseau neuronal associatif simplifié.

Sans LLM. Purement statistique + graphe pondéré.

C'est la pièce architecturale la plus proche d'une vraie compréhension :
le sens émerge des cooccurrences réelles vécues par Leia.
"""

from __future__ import annotations
import json, os, time, math, re
from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

def _clamp(v, lo=0.0, hi=1.0):
    try: return max(lo, min(hi, float(v)))
    except: return lo

def _now(): return time.time()

_STOP = {
    "le","la","les","un","une","des","de","du","et","en","est","à","au","aux",
    "il","elle","ils","elles","on","je","tu","nous","vous","se","sa","son",
    "ses","me","te","lui","leur","leurs","que","qui","quoi","dont","où",
    "mais","ou","donc","or","ni","car","si","lors","alors","ainsi",
    "très","plus","moins","bien","tout","même","aussi","encore","toujours",
    "jamais","rien","ne","pas","avec","sans","sous","sur","dans","par",
    "pour","vers","chez","comme","quand","comment","combien","ce","cet",
    "cette","ces","être","avoir","faire","aller","voir","venir","dire",
    "savoir","pouvoir","vouloir","falloir","prendre","donner","trouver",
}


class AssociativeNode:
    """Un concept dans le graphe associatif."""

    __slots__ = ("name","activation","base_weight","last_activated",
                 "source_tags","creation_time")

    def __init__(self, name: str, base_weight: float = 0.1,
                 source_tag: str = "unknown"):
        self.name           = name
        self.activation     = 0.0
        self.base_weight    = _clamp(base_weight, 0.01, 1.0)
        self.last_activated = _now()
        self.source_tags: Set[str] = {source_tag}
        self.creation_time  = _now()

    def activate(self, strength: float = 1.0):
        self.activation = _clamp(self.activation + strength * 0.6, 0.0, 1.0)
        self.last_activated = _now()

    def decay(self, rate: float = 0.05):
        """Décroissance douce de l'activation."""
        self.activation = _clamp(self.activation * (1.0 - rate))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name":           self.name,
            "base_weight":    round(self.base_weight, 4),
            "last_activated": self.last_activated,
            "source_tags":    list(self.source_tags)[:8],
            "creation_time":  self.creation_time,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "AssociativeNode":
        n = cls(d["name"], float(d.get("base_weight", 0.1)),
                "restored")
        n.last_activated = float(d.get("last_activated", _now()))
        n.source_tags    = set(d.get("source_tags", []))
        n.creation_time  = float(d.get("creation_time", _now()))
        return n


class AssociativeMemory:
    """
    Graphe associatif hebbien.

    Apprentissage :
      impregnate(concepts, source) → renforce les liens entre tous ces concepts

    Compréhension :
      spread(seeds) → propage l'activation depuis les concepts seeds
                     → retourne les concepts les plus activés

    C'est le cœur de la compréhension sans LLM :
    les associations ne sont pas codées en dur,
    elles émergent de l'expérience réelle de Leia.
    """

    MAX_NODES = 2000  # limite pour la mémoire
    MAX_EDGES_PER_NODE = 40

    def __init__(self, storage_path: str = "data/associative_memory_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)

        self.nodes: Dict[str, AssociativeNode] = {}
        # edges[a][b] = poids du lien a→b (0.0 à 1.0)
        self.edges: Dict[str, Dict[str, float]] = defaultdict(dict)
        self._learn_count: int = 0  # nombre d'apprentissages
        self._load()

    # ── Persistance ───────────────────────────────────────────────────────────
    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            for nd in data.get("nodes", []):
                n = AssociativeNode.from_dict(nd)
                self.nodes[n.name] = n
            for src, targets in data.get("edges", {}).items():
                if isinstance(targets, dict):
                    self.edges[src] = dict(targets)
            self._learn_count = int(data.get("learn_count", 0))
        except Exception:
            pass

    def _save(self):
        try:
            # Ne sauvegarder que les N nœuds les plus actifs/récents
            important = sorted(
                self.nodes.values(),
                key=lambda n: (n.base_weight + n.last_activated / 1e10),
                reverse=True
            )[:self.MAX_NODES]
            keep = {n.name for n in important}
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "nodes": [n.to_dict() for n in important],
                    "edges": {
                        k: {kk: round(v,4) for kk,v in vv.items()
                            if kk in keep}
                        for k,vv in self.edges.items() if k in keep
                    },
                    "learn_count": self._learn_count,
                    "timestamp": _now(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Extraction de mots ────────────────────────────────────────────────────
    @staticmethod
    def _extract_concepts(text: str) -> List[str]:
        words = re.findall(r"[\wÀ-ÿ']{4,}", text.lower())
        return [w for w in words if w not in _STOP and not w.isdigit()]

    # ── Apprentissage hebbien ─────────────────────────────────────────────────
    def impregnate(self, concepts: List[str], source: str = "experience",
                   weight_boost: float = 1.0) -> Dict[str, Any]:
        """
        Renforce les liens entre tous les concepts donnés.
        Hebb : si A et B s'activent ensemble → lien(A,B) se renforce.

        concepts   : liste de strings (mots, lemmes, etc.)
        source     : "book", "exchange", "emotion", "inference"
        weight_boost : multiplicateur (livres importants → 1.5)
        """
        # Filtrer et normaliser
        clean = []
        for c in concepts:
            c = str(c).strip().lower()
            if c and c not in _STOP and len(c) >= 3 and not c.isdigit():
                clean.append(c)
        clean = list(dict.fromkeys(clean))[:60]  # dédupliquer, limiter

        if len(clean) < 2:
            return {"learned": 0}

        # Créer les nœuds manquants
        for c in clean:
            if c not in self.nodes:
                self.nodes[c] = AssociativeNode(c, 0.05, source)
            self.nodes[c].source_tags.add(source)

        # Renforcement des liens (Hebb)
        # La force du lien décroît avec la distance dans la liste
        learned_pairs = 0
        window = 12  # fenêtre de cooccurrence
        for i, a in enumerate(clean):
            for j, b in enumerate(clean):
                if a == b: continue
                distance = abs(i - j)
                if distance > window: continue
                # Force du lien : inversement proportionnelle à la distance
                delta = weight_boost * (0.08 / (1.0 + distance * 0.4))
                # Renforcement symétrique
                old_ab = self.edges[a].get(b, 0.0)
                old_ba = self.edges[b].get(a, 0.0)
                self.edges[a][b] = _clamp(old_ab + delta, 0.0, 1.0)
                self.edges[b][a] = _clamp(old_ba + delta * 0.7, 0.0, 1.0)
                # Renforcer le poids de base du nœud
                self.nodes[a].base_weight = _clamp(
                    self.nodes[a].base_weight + delta * 0.3, 0.01, 1.0)
                learned_pairs += 1

        # Élaguer les voisins en trop
        for node in clean:
            if len(self.edges[node]) > self.MAX_EDGES_PER_NODE:
                # Garder les liens les plus forts
                sorted_edges = sorted(self.edges[node].items(),
                                      key=lambda x: x[1], reverse=True)
                self.edges[node] = dict(sorted_edges[:self.MAX_EDGES_PER_NODE])

        self._learn_count += 1
        if self._learn_count % 5 == 0:
            self._save()

        return {"learned": learned_pairs, "concepts_count": len(clean)}

    def impregnate_text(self, text: str, source: str = "exchange",
                        weight_boost: float = 1.0) -> Dict[str, Any]:
        """Imprégnation directe depuis un texte brut."""
        concepts = self._extract_concepts(text)
        return self.impregnate(concepts, source=source, weight_boost=weight_boost)

    # ── Propagation d'activation (Spreading Activation) ───────────────────────
    def spread(self, seed_concepts: List[str], steps: int = 3,
               decay: float = 0.45, top_k: int = 20) -> List[Dict[str, Any]]:
        """
        Propage l'activation depuis les concepts seeds.
        Retourne les nœuds les plus activés (hors seeds).

        C'est ici que la "compréhension" émerge :
        si l'utilisateur dit "mémoire", Leia active aussi
        "durée","souvenir","Bergson","oubli"... selon ce qu'elle a vraiment lu.

        steps  : profondeur de propagation (2-3 suffit)
        decay  : facteur d'atténuation à chaque étape (0.3-0.6)
        top_k  : nombre de résultats retournés
        """
        if not seed_concepts or not self.nodes:
            return []

        # Normaliser les seeds
        seeds = set()
        for s in seed_concepts:
            s = str(s).strip().lower()
            if s in self.nodes:
                seeds.add(s)
            else:
                # Recherche partielle : si "mémoire" → "mémoires" (flexion)
                for node_name in self.nodes:
                    if s in node_name or node_name in s:
                        seeds.add(node_name)
                        break

        # Activation initiale
        activation: Dict[str, float] = {s: 1.0 for s in seeds}

        # Propagation en plusieurs étapes
        for step in range(steps):
            next_activation: Dict[str, float] = {}
            step_decay = decay ** (step + 1)
            for node, act in activation.items():
                if node not in self.edges: continue
                for neighbor, edge_weight in self.edges[node].items():
                    if neighbor in seeds: continue
                    bonus = (self.nodes[neighbor].base_weight
                             if neighbor in self.nodes else 0.1)
                    spread_val = act * edge_weight * step_decay * (1.0 + bonus * 0.3)
                    next_activation[neighbor] = max(
                        next_activation.get(neighbor, 0.0), spread_val)
            # Fusionner avec activation courante
            for node, val in next_activation.items():
                activation[node] = max(activation.get(node, 0.0), val)

        # Trier et retourner (hors seeds)
        results = [
            {
                "concept":  node,
                "activation": round(val, 4),
                "weight":   round(self.nodes[node].base_weight, 4) if node in self.nodes else 0.0,
                "sources":  list(self.nodes[node].source_tags)[:3] if node in self.nodes else [],
            }
            for node, val in activation.items()
            if node not in seeds and val > 0.005
        ]
        results.sort(key=lambda x: x["activation"], reverse=True)
        return results[:top_k]

    # ── Requête de similarité ─────────────────────────────────────────────────
    def similar_concepts(self, concept: str, top_k: int = 8) -> List[str]:
        """Retourne les concepts les plus liés à un concept donné."""
        concept = concept.strip().lower()
        if concept not in self.edges:
            return []
        neighbors = sorted(self.edges[concept].items(),
                            key=lambda x: x[1], reverse=True)
        return [n for n, _ in neighbors[:top_k]]

    def shared_neighbors(self, a: str, b: str) -> List[str]:
        """Concepts partagés entre deux concepts → détecte les ponts conceptuels."""
        na = set(self.edges.get(a.lower(), {}).keys())
        nb = set(self.edges.get(b.lower(), {}).keys())
        shared = na & nb - {a.lower(), b.lower()}
        return sorted(shared, key=lambda x: (
            self.edges.get(a.lower(),{}).get(x,0) +
            self.edges.get(b.lower(),{}).get(x,0)
        ), reverse=True)[:6]

    # ── Décroissance globale ──────────────────────────────────────────────────
    def global_decay(self, rate: float = 0.002):
        """
        Décroissance lente des liens les moins récents.
        À appeler dans tick_inner_life().
        """
        now = _now()
        to_weaken = []
        for a in self.edges:
            for b in list(self.edges[a].keys()):
                # Affaiblir les liens vieux et faibles
                last = self.nodes[b].last_activated if b in self.nodes else 0
                age_days = (now - last) / 86400.0
                if age_days > 7 and self.edges[a][b] < 0.15:
                    to_weaken.append((a, b))
        for a, b in to_weaken:
            self.edges[a][b] = max(0.0, self.edges[a][b] - rate)
            if self.edges[a][b] < 0.01:
                del self.edges[a][b]

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, seeds: List[str], context_text: str = "",
               top_k: int = 12) -> Dict[str, Any]:
        """
        Interface standard.
        seeds : concepts à activer (mots du message utilisateur, focus du core...)
        """
        if not seeds and not context_text:
            return {"available": False, "activated": [], "seed_count": 0}

        # Compléter les seeds depuis le texte si peu de seeds
        if len(seeds) < 3 and context_text:
            text_concepts = self._extract_concepts(context_text)
            seeds = list(dict.fromkeys(seeds + text_concepts[:6]))

        activated = self.spread(seeds, steps=3, top_k=top_k)

        # Résumer les sources impliquées
        all_sources: Set[str] = set()
        for item in activated[:5]:
            all_sources.update(item.get("sources", []))

        return {
            "available":    True,
            "activated":    activated,
            "seed_count":   len(seeds),
            "activated_count": len(activated),
            "top_concept":  activated[0]["concept"] if activated else "",
            "top_activation": activated[0]["activation"] if activated else 0.0,
            "involved_sources": list(all_sources)[:6],
            "graph_size":   len(self.nodes),
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "node_count":   len(self.nodes),
            "edge_count":   sum(len(v) for v in self.edges.values()),
            "learn_count":  self._learn_count,
            "top_nodes":    sorted(
                [(n.name, round(n.base_weight,3)) for n in self.nodes.values()],
                key=lambda x: x[1], reverse=True
            )[:10],
        }

    def save_now(self):
        self._save()