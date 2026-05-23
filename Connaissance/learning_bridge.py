# -*- coding: utf-8 -*-
"""
Connaissance/learning_bridge.py — Pont d'apprentissage depuis le NLP

Rôle : quand Leia lit un livre ou un PDF, ce module :
  1. Analyse le texte avec leia_spacy_engine
  2. Injecte les concepts dans SemanticPlasticity (graphe vivant)
  3. Stocke les épisodes dans HierarchicalMemory (mémoire hiérarchisée)
  4. Consolide la compréhension dans BookUnderstandingEngine

Zéro dépendance externe. Utilise les modules existants du dépôt.
"""

from __future__ import annotations

import sys
import os
from typing import Any, Dict, List, Optional

# --- Chemins projet ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for sub in ["", "Cerveau", "Memory", "Connaissance", "Soi_Leia"]:
    p = os.path.join(ROOT, sub)
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from leia_spacy_engine import engine as nlp_engine
except Exception as e:
    raise RuntimeError(f"learning_bridge requiert leia_spacy_engine.py à la racine : {e}")

# Imports des modules existants (ils sont dans le dépôt)
try:
    from semantic_plasticity import SemanticPlasticity
except Exception:
    SemanticPlasticity = None

try:
    from memory_hierarchy import HierarchicalMemory
except Exception:
    HierarchicalMemory = None

try:
    from book_understanding_engine import BookUnderstandingEngine
except Exception:
    BookUnderstandingEngine = None


class ReadingBridge:
    """
    Pipeline complet : texte brut → connaissance persistante.
    """

    def __init__(self, data_dir: str = "data"):
        self.engine = nlp_engine
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

        # Modules existants du dépôt (fallback si absents)
        self.plasticity = SemanticPlasticity() if SemanticPlasticity else None
        self.hierarchy = HierarchicalMemory() if HierarchicalMemory else None
        self.books = BookUnderstandingEngine() if BookUnderstandingEngine else None

        self._books_read: List[str] = []

    def read_text(self, text: str, source: str = "inconnu") -> Dict[str, Any]:
        """
        Appel principal : lire et intégrer un texte.
        Retourne un rapport d'apprentissage.
        """
        if not text or not text.strip():
            return {"status": "empty", "concepts": 0}

        # 1. Segmentation en blocs cohérents
        chunks = self.engine.segment_text(text, max_chars=2000)

        total_concepts: set = set()
        total_props = 0
        all_analyses = []

        for chunk in chunks:
            # 2. Analyse profonde
            analysis = self.engine.analyze_text(chunk, source=source)
            all_analyses.append(analysis)
            total_concepts.update(analysis.key_concepts[:15])
            total_props += len(analysis.propositions)

            # 3. Intégration graphe sémantique (plasticité)
            if self.plasticity:
                for concept in analysis.key_concepts[:10]:
                    self.plasticity.impregnate(concept, source=source, intensity=0.6)
                for i, c1 in enumerate(analysis.key_concepts[:6]):
                    for c2 in analysis.key_concepts[i+1:7]:
                        self.plasticity.connect(c1, c2, weight=0.12, context=source)

            # 4. Mémoire hiérarchique
            if self.hierarchy:
                episode = {
                    "type": "lecture",
                    "source": source,
                    "concepts": analysis.key_concepts[:8],
                    "propositions_count": len(analysis.propositions),
                    "lexical_density": analysis.lexical_density,
                    "impact": min(1.0, 0.4 + analysis.lexical_density * 0.4),
                    "unfinished": any(p.conf < 0.7 for p in analysis.propositions[:5]),
                    "emotional_tone": "neutral",  # pourrait être enrichi par affect_lexicon
                }
                self.hierarchy.absorb_episode(episode)

            # 5. Compréhension structurée du livre
            if self.books:
                self.books.consolidate({
                    "source": source,
                    "key_concepts": analysis.key_concepts[:20],
                    "propositions": [p.to_dict() for p in analysis.propositions[:20]],
                    "entities": [e.to_dict() for e in analysis.named_entities[:10]],
                    "themes": analysis.themes,
                    "discourse": analysis.discourse_structure,
                    "lexical_density": analysis.lexical_density,
                })

        self._books_read.append(source)

        return {
            "status": "learned",
            "source": source,
            "chunks_analyzed": len(chunks),
            "unique_concepts": len(total_concepts),
            "propositions_found": total_props,
            "concepts": sorted(total_concepts)[:20],
            "plasticity_active": self.plasticity is not None,
            "hierarchy_active": self.hierarchy is not None,
            "books_active": self.books is not None,
        }

    def read_book_file(self, filepath: str) -> Dict[str, Any]:
        """Lire un fichier texte/PDF (PDF nécessite pdf_knowledge_engine pour extraction brute)."""
        if not os.path.exists(filepath):
            return {"status": "error", "reason": "file_not_found"}
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        except Exception as e:
            return {"status": "error", "reason": str(e)}
        source = os.path.basename(filepath)
        return self.read_text(text, source=source)

    def get_knowledge_state(self) -> Dict[str, Any]:
        """État courant de la connaissance (pour le debug / self_model)."""
        state = {
            "books_read": self._books_read,
            "plasticity_nodes": 0,
            "memory_foundational": 0,
            "memory_pivot": 0,
        }
        if self.plasticity and hasattr(self.plasticity, "nodes"):
            state["plasticity_nodes"] = len(self.plasticity.nodes)
        if self.hierarchy:
            snap = self.hierarchy.snapshot()
            state["memory_foundational"] = snap.get("foundational_count", 0)
            state["memory_pivot"] = snap.get("pivot_count", 0)
        return state

    def react_to_concepts(self, concepts: List[str]) -> List[str]:
        """
        Pour la réactivation : quand l'utilisateur parle de 'durée',
        ce module dit quels concepts du livre sont réactivés.
        """
        if not self.plasticity or not hasattr(self.plasticity, "graph"):
            return []
        related = set()
        for c in concepts:
            c = c.lower().strip()
            for linked, weight in self.plasticity.graph.get(c, {}).items():
                if weight > 0.15:
                    related.add(linked)
        return list(related)[:10]
