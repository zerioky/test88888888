# -*- coding: utf-8 -*-
"""
Cerveau/nlp_integration.py — Wrapper NLP pour LeiaLivingCore

Rôle : connecter leia_spacy_engine (analyse profonde) avec le core existant.
Ce wrapper expose exactement les mêmes signatures que les anciens modules
(user_utterance_parser, proposition_extractor, semantic_coherence)
pour qu'on puisse les remplacer sans tout casser.

Usage dans leia_living_core.py :
    from nlp_integration import LeiaNLPBridge
    self.nlp = LeiaNLPBridge()
"""

from __future__ import annotations
import sys
import os

# --- Trouver le moteur NLP (racine du projet) ---
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from leia_spacy_engine import engine as nlp_engine
except Exception as e:
    raise RuntimeError(f"leia_spacy_engine.py doit être à la racine du projet : {e}")

from typing import Any, Dict, List, Optional


class LeiaNLPBridge:
    """
    Pont unifié entre le moteur linguistique profond et le reste du système.
    Remplace : user_utterance_parser, proposition_extractor, concept_relation_engine,
    semantic_coherence (partiel), book_understanding_engine (partiel).
    """

    def __init__(self):
        self.engine = nlp_engine
        self.last_analysis: Optional[Dict[str, Any]] = None
        self.last_text_analysis: Optional[Dict[str, Any]] = None

    # ── API compatible ancien user_utterance_parser ───────────────────────
    def signal(self, text: str) -> Dict[str, Any]:
        """Même signature que user_utterance_parser.signal(text)"""
        if not text or not text.strip():
            return {"available": False, "intent": "", "focus_concept": "", "is_question": False}
        ua = self.engine.analyze_utterance(text)
        self.last_analysis = ua.to_dict()
        return {
            "available": True,
            "intent": ua.intent,
            "focus_concept": ua.focus_concepts[0] if ua.focus_concepts else "",
            "focus_concepts": ua.focus_concepts[:6],
            "is_question": ua.is_question,
            "is_personal": ua.is_personal,
            "is_negative": ua.is_negative,
            "stance": ua.stance,
            "modality": ua.modality,
            "emotional_charge": round(ua.emotional_charge, 3),
            "urgency": round(ua.urgency, 3),
            "complexity": round(ua.complexity, 3),
            "propositions_count": len(ua.propositions),
            "entities": [e.to_dict() for e in ua.named_entities[:5]],
            "subject": ua.subject,
            "verb": ua.verb_root,
            "object": ua.obj,
            "deep_structure": ua.deep_structure,
            "parser": ua.parser_used,
        }

    # ── API compatible ancien proposition_extractor ─────────────────────────
    def extract_propositions(self, text: str, source: str = "") -> List[Dict[str, Any]]:
        """Remplace proposition_extractor.extract_from_text()"""
        ta = self.engine.analyze_text(text, source=source)
        return [p.to_dict() for p in ta.propositions]

    def concept_signal(self, concept: str) -> Dict[str, Any]:
        """Pour semantic_coherence / concept_relation_engine."""
        return {"available": True, "concept": concept, "related": []}

    # ── API compatible book_understanding_engine ──────────────────────────
    def analyze_book_chunk(self, text: str, source: str = "") -> Dict[str, Any]:
        """Pour Connaissance/pdf_knowledge_engine et deep_book_digestion."""
        ta = self.engine.analyze_text(text, source=source)
        self.last_text_analysis = ta.to_dict()
        return {
            "available": True,
            "source": source,
            "key_concepts": ta.key_concepts[:20],
            "propositions": [p.to_dict() for p in ta.propositions[:20]],
            "entities": [e.to_dict() for e in ta.named_entities[:10]],
            "themes": ta.themes[:10],
            "theses": ta.theses[:5],
            "objections": ta.objections[:5],
            "discourse": ta.discourse_structure[:10],
            "lexical_density": ta.lexical_density,
            "sentence_count": ta.sentence_count,
        }

    def segment_book(self, text: str, max_chars: int = 1500) -> List[str]:
        """Remplace la segmentation manuelle dans pdf_knowledge_engine."""
        return self.engine.segment_text(text, max_chars)

    # ── API semantic_similarity (pour associative_memory, etc.) ──────────
    def similarity(self, a: str, b: str) -> float:
        return self.engine.semantic_similarity(a, b)

    def detect_meta(self, text: str) -> bool:
        """Pour le filtre anti-fuite méta du weaver."""
        return self.engine.detect_meta_leak(text)

    def stats(self) -> Dict[str, Any]:
        return self.engine.stats()
