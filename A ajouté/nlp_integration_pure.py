# -*- coding: utf-8 -*-
"""
nlp_integration_pure.py — Pont NLP pur Python pour Leia V19+
═════════════════════════════════════════════════════════════════════════════
REMPLACEMENT COMPLET de nlp_integration.py + leia_spacy_engine.py

Zéro dépendance externe. Zéro préécrit.
Branché sur leia_comprehension_vivante.py (pur Python stdlib).

Ce module expose exactement les mêmes signatures que :
  • leia_spacy_engine.engine  (analyse linguistique profonde)
  • LeiaNLPBridge             (API compatible leia_living_core.py)

Remplacer dans leia_living_core.py :
    # Avant (ligne ~130) :
    from nlp_integration import LeiaNLPBridge
    # Après :
    from nlp_integration_pure import LeiaNLPBridge

Et en tête de chaque module qui importe leia_spacy_engine :
    # Avant :
    from leia_spacy_engine import engine
    # Après :
    from nlp_integration_pure import engine
"""

from __future__ import annotations

import math
import re
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set

# Import du moteur vivant (même dossier ou chemin Python)
import sys, os
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from leia_comprehension_vivante import (
    LeiaComprehensionVivante,
    ComprehensionDialogue,
    ComprehensionTexte,
    FrenchMorphology,
)


# ═══════════════════════════════════════════════════════════════════════════════
# COMPATIBILITÉ leia_spacy_engine — dataclasses fantômes
# Ces classes exposent la même interface que celles de leia_spacy_engine.py
# afin que les modules qui importaient leia_spacy_engine continuent de fonctionner.
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Proposition:
    """Compatible avec leia_spacy_engine.Proposition"""
    subject: str
    relation: str
    obj: str
    negated: bool = False
    confidence: float = 0.7
    connector_type: str = ""
    source_text: str = ""
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject": self.subject,
            "relation": self.relation,
            "object": self.obj,
            "negated": self.negated,
            "confidence": round(self.confidence, 3),
            "connector_type": self.connector_type,
        }

    def __repr__(self) -> str:
        neg = "¬" if self.negated else ""
        return f"({self.subject}, {neg}{self.relation}, {self.obj})"


@dataclass
class NamedEntity:
    """Compatible avec leia_spacy_engine.NamedEntity"""
    text: str
    label: str
    confidence: float = 0.8
    context: str = ""

    def to_dict(self) -> Dict[str, str]:
        return {"text": self.text, "label": self.label, "context": self.context}


@dataclass
class UtteranceAnalysis:
    """
    Compatible avec leia_spacy_engine.UtteranceAnalysis.
    Produit par engine.analyze_utterance().
    """
    intent: str = ""
    stance: str = ""
    modality: str = ""
    subject: str = ""
    verb_root: str = ""
    obj: str = ""
    is_question: bool = False
    is_negative: bool = False
    is_personal: bool = False
    focus_concepts: List[str] = field(default_factory=list)
    named_entities: List[NamedEntity] = field(default_factory=list)
    propositions: List[Proposition] = field(default_factory=list)
    content_words: List[str] = field(default_factory=list)
    word_count: int = 0
    emotional_charge: float = 0.0
    urgency: float = 0.0
    complexity: float = 0.0
    deep_structure: Dict[str, Any] = field(default_factory=dict)
    parser_used: str = "pure_python"
    raw: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent": self.intent,
            "stance": self.stance,
            "modality": self.modality,
            "subject": self.subject,
            "verb_root": self.verb_root,
            "object": self.obj,
            "is_question": self.is_question,
            "is_negative": self.is_negative,
            "is_personal": self.is_personal,
            "focus_concepts": self.focus_concepts[:8],
            "named_entities": [e.to_dict() for e in self.named_entities],
            "propositions": [p.to_dict() for p in self.propositions],
            "content_words": self.content_words[:12],
            "word_count": self.word_count,
            "emotional_charge": round(self.emotional_charge, 3),
            "urgency": round(self.urgency, 3),
            "complexity": round(self.complexity, 3),
            "deep_structure": self.deep_structure,
            "parser_used": self.parser_used,
        }


@dataclass
class TextAnalysis:
    """
    Compatible avec leia_spacy_engine.TextAnalysis.
    Produit par engine.analyze_text().
    """
    key_concepts: List[str] = field(default_factory=list)
    named_entities: List[NamedEntity] = field(default_factory=list)
    propositions: List[Proposition] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    theses: List[str] = field(default_factory=list)
    objections: List[str] = field(default_factory=list)
    conclusions: List[str] = field(default_factory=list)
    discourse_structure: List[Dict[str, str]] = field(default_factory=list)
    chunks: List[Dict[str, Any]] = field(default_factory=list)
    sentence_count: int = 0
    word_count: int = 0
    lexical_density: float = 0.0
    dominant_modality: str = ""
    source: str = ""
    parser_used: str = "pure_python"
    processed_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_concepts": self.key_concepts[:20],
            "named_entities": [e.to_dict() for e in self.named_entities[:20]],
            "propositions": [p.to_dict() for p in self.propositions[:30]],
            "themes": self.themes[:10],
            "theses": self.theses[:5],
            "objections": self.objections[:5],
            "conclusions": self.conclusions[:5],
            "discourse_structure": self.discourse_structure[:10],
            "sentence_count": self.sentence_count,
            "word_count": self.word_count,
            "lexical_density": round(self.lexical_density, 3),
            "dominant_modality": self.dominant_modality,
            "source": self.source,
            "parser_used": self.parser_used,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# CONVERTISSEURS — ComprehensionDialogue / ComprehensionTexte → formats legacy
# ═══════════════════════════════════════════════════════════════════════════════

def _triplet_to_prop(t: Dict[str, Any]) -> Proposition:
    """Convertit un triplet interne en Proposition compatible legacy."""
    return Proposition(
        subject=t.get("sujet", "")[:50],
        relation=t.get("relation", ""),
        obj=t.get("objet", "")[:50],
        negated=bool(t.get("negation", False)),
        confidence=float(t.get("confiance", 0.7)),
        connector_type=t.get("connecteur", ""),
        source_text=t.get("source", "")[:80],
    )


def _entite_to_ne(e: Dict[str, str]) -> NamedEntity:
    """Convertit une entité interne en NamedEntity compatible legacy."""
    label_map = {
        "PERSONNE": "PERSON", "PROPRE": "PERSON",
        "LIEU": "LOC", "ORG": "ORG", "OEUVRE": "WORK",
    }
    lbl = label_map.get(e.get("type", ""), e.get("type", "MISC"))
    return NamedEntity(
        text=e.get("texte", ""),
        label=lbl,
        confidence=0.85,
        context=e.get("contexte", ""),
    )


def _dialogue_to_utterance(cd: ComprehensionDialogue) -> UtteranceAnalysis:
    """Convertit ComprehensionDialogue → UtteranceAnalysis (format legacy)."""
    propositions = [_triplet_to_prop(t) for t in cd.triplets]
    words = cd.mots_contenu
    n_words = cd.n_mots
    complexity = len(set(words)) / max(n_words, 1) if n_words else 0.0

    return UtteranceAnalysis(
        intent=cd.intention,
        stance=cd.posture,
        modality=cd.modalite,
        subject=cd.sujet_grammatical,
        verb_root=cd.verbe_principal,
        obj=cd.objet_grammatical,
        is_question=cd.est_question,
        is_negative=cd.est_negatif,
        is_personal=cd.est_personnel,
        focus_concepts=cd.concepts_focaux[:8],
        named_entities=[],
        propositions=propositions,
        content_words=words[:15],
        word_count=n_words,
        emotional_charge=cd.charge_emotionnelle,
        urgency=cd.urgence,
        complexity=min(1.0, max(0.0, complexity)),
        deep_structure={
            "resonance": cd.resonance,
            "surprise": cd.surprise,
            "tension": cd.tension,
            "concepts_actives": cd.concepts_actives[:8],
            "voisins_graphe": cd.voisins_graphe[:5],
        },
        parser_used="pure_python",
        raw=cd.raw,
    )


def _texte_to_textanalysis(ct: ComprehensionTexte) -> TextAnalysis:
    """Convertit ComprehensionTexte → TextAnalysis (format legacy)."""
    propositions = [_triplet_to_prop(t) for t in ct.triplets]
    entities = [_entite_to_ne(e) for e in ct.entites]
    # Structure du discours
    discourse = []
    for t in ct.theses[:3]:
        discourse.append({"type": "thèse", "text": t[:100]})
    for o in ct.objections[:3]:
        discourse.append({"type": "objection", "text": o[:100]})
    for c in ct.conclusions[:2]:
        discourse.append({"type": "conclusion", "text": c[:100]})
    # Chunks
    chunks = [
        {
            "text": s.get("texte", "")[:300],
            "themes": s.get("concepts", [])[:5],
            "key_concepts": s.get("concepts", [])[:5],
            "propositions": [],
            "argument_type": s.get("arg_type", ""),
            "position": s.get("position", 0),
        }
        for s in ct.segments
    ]
    return TextAnalysis(
        key_concepts=ct.concepts_cles[:25],
        named_entities=entities,
        propositions=propositions,
        themes=ct.themes[:10],
        theses=ct.theses[:5],
        objections=ct.objections[:5],
        conclusions=ct.conclusions[:4],
        discourse_structure=discourse,
        chunks=chunks,
        sentence_count=ct.n_phrases,
        word_count=ct.n_mots,
        lexical_density=ct.densite_lexicale,
        dominant_modality=ct.modalite_dominante,
        source=ct.source,
        parser_used="pure_python",
    )


# ═══════════════════════════════════════════════════════════════════════════════
# ENGINE — point d'entrée compatible leia_spacy_engine.engine
# ═══════════════════════════════════════════════════════════════════════════════

class _PureEngine:
    """
    Drop-in replacement for leia_spacy_engine.engine.
    Expose la même API publique — sans spaCy, sans aucune dépendance.
    """

    def __init__(self):
        self._core = LeiaComprehensionVivante()
        self._morpho = FrenchMorphology()
        self._n_utterances = 0
        self._n_texts = 0
        self._times: deque = deque(maxlen=100)

    # ── API principale ─────────────────────────────────────────────────────

    def analyze_utterance(self, text: str) -> UtteranceAnalysis:
        """Compatible engine.analyze_utterance() de leia_spacy_engine."""
        if not text or not text.strip():
            return UtteranceAnalysis(raw=text or "", parser_used="pure_python")
        t0 = time.monotonic()
        cd = self._core.dialogue(text)
        self._times.append(time.monotonic() - t0)
        self._n_utterances += 1
        return _dialogue_to_utterance(cd)

    def analyze_text(self, text: str, source: str = "",
                     max_chars: int = 80_000) -> TextAnalysis:
        """Compatible engine.analyze_text() de leia_spacy_engine."""
        if not text or not text.strip():
            return TextAnalysis(source=source, parser_used="pure_python")
        ct = self._core.texte(text[:max_chars], source=source)
        self._n_texts += 1
        return _texte_to_textanalysis(ct)

    def extract_propositions(self, text: str, source: str = "") -> List[Proposition]:
        """Compatible engine.extract_propositions()."""
        ct = self._core.texte(text[:10000], source=source)
        return [_triplet_to_prop(t) for t in ct.triplets]

    def extract_named_entities(self, text: str) -> List[NamedEntity]:
        """Compatible engine.extract_named_entities()."""
        ct = self._core.texte(text[:5000])
        return [_entite_to_ne(e) for e in ct.entites]

    def extract_themes(self, text: str) -> List[str]:
        """Compatible engine.extract_themes()."""
        ct = self._core.texte(text[:20000])
        return ct.themes

    def semantic_similarity(self, text_a: str, text_b: str) -> float:
        """Compatible engine.semantic_similarity()."""
        return self._core.similarite(text_a, text_b)

    def segment_text(self, text: str, max_chunk_chars: int = 1500) -> List[str]:
        """Compatible engine.segment_text()."""
        ct = self._core.texte(text[:80000])
        return [s.get("texte", "") for s in ct.segments]

    def concept_overlap(self, a: List[str], b: List[str]) -> float:
        """Compatible engine.concept_overlap()."""
        from leia_comprehension_vivante import _STOP
        sa = {w.lower() for w in a if w.lower() not in _STOP}
        sb = {w.lower() for w in b if w.lower() not in _STOP}
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    def is_coherent_response(self, response: str, active_concepts: List[str],
                              threshold: float = 0.12) -> bool:
        """Compatible engine.is_coherent_response()."""
        return self._core.coherence.est_coherente(response, active_concepts, threshold)

    def detect_meta_leak(self, text: str) -> bool:
        """Compatible engine.detect_meta_leak()."""
        return self._core.coherence.contient_meta(text)

    def get_living_state(self) -> Dict[str, Any]:
        """Accès à l'état vivant du graphe conceptuel — propre à ce moteur."""
        return self._core.etat_vivant()

    def stats(self) -> Dict[str, Any]:
        avg = (sum(self._times) / len(self._times) * 1000) if self._times else 0.0
        return {
            "spacy_model": "none",
            "spacy_available": False,
            "engine": "pure_python",
            "total_utterances": self._n_utterances,
            "total_texts": self._n_texts,
            "avg_parse_ms": round(avg, 2),
            "graphe_concepts": len(self._core.graphe.noeuds),
            "graphe_liens": len(self._core.graphe.liens),
        }

    def save_state(self, path: str) -> None:
        """Sauvegarde le graphe vivant."""
        self._core.sauvegarder(path)

    def load_state(self, path: str) -> None:
        """Charge un graphe sauvegardé."""
        self._core.charger(path)


# Instance globale — remplace leia_spacy_engine.engine
engine = _PureEngine()


# ═══════════════════════════════════════════════════════════════════════════════
# LeiaNLPBridge — drop-in pour nlp_integration.LeiaNLPBridge
# ═══════════════════════════════════════════════════════════════════════════════

class LeiaNLPBridge:
    """
    Drop-in replacement for nlp_integration.LeiaNLPBridge.

    Usage dans leia_living_core.py :
        # Remplacer :
        from nlp_integration import LeiaNLPBridge
        # Par :
        from nlp_integration_pure import LeiaNLPBridge
    """

    def __init__(self):
        self.engine = engine           # partage le singleton global
        self.last_analysis: Optional[Dict[str, Any]] = None
        self.last_text_analysis: Optional[Dict[str, Any]] = None

    # ── Même API que nlp_integration.LeiaNLPBridge ─────────────────────────

    def signal(self, text: str) -> Dict[str, Any]:
        """
        Même signature que user_utterance_parser.signal(text).
        Retour étendu : inclut les mesures vivantes (résonance, surprise, tension).
        """
        if not text or not text.strip():
            return {
                "available": False,
                "intent": "", "focus_concept": "", "is_question": False,
                "stance": "neutre", "modality": "assertion",
                "emotional_charge": 0.0, "urgency": 0.0, "complexity": 0.0,
                "resonance": 0.0, "surprise": 0.0, "tension": 0.0,
            }

        ua = self.engine.analyze_utterance(text)
        self.last_analysis = ua.to_dict()

        # Mesures vivantes (du graphe interne)
        deep = ua.deep_structure

        return {
            "available": True,
            # Classique
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
            # Mesures vivantes — nouvelles dans cette version
            "resonance": round(deep.get("resonance", 0.0), 3),
            "surprise": round(deep.get("surprise", 0.0), 3),
            "tension": round(deep.get("tension", 0.0), 3),
            "concepts_actives": deep.get("concepts_actives", [])[:6],
            "voisins_graphe": deep.get("voisins_graphe", [])[:4],
            "deep_structure": deep,
            "parser": "pure_python",
        }

    def extract_propositions(self, text: str, source: str = "") -> List[Dict[str, Any]]:
        """Remplace proposition_extractor.extract_from_text()"""
        ta = self.engine.analyze_text(text, source=source)
        return [p.to_dict() for p in ta.propositions]

    def concept_signal(self, concept: str) -> Dict[str, Any]:
        """Pour semantic_coherence / concept_relation_engine."""
        voisins = self.engine._core.graphe.voisins(concept.lower(), n=5)
        n = self.engine._core.graphe.noeuds.get(concept.lower())
        return {
            "available": True,
            "concept": concept,
            "related": voisins,
            "familiarite": round(n.familiarite, 3) if n else 0.0,
            "activation": round(n.activation, 3) if n else 0.0,
        }

    def analyze_book_chunk(self, text: str, source: str = "") -> Dict[str, Any]:
        """
        Pour Connaissance/pdf_knowledge_engine et deep_book_digestion.
        Même format de sortie que l'ancien LeiaNLPBridge.analyze_book_chunk().
        """
        ta = self.engine.analyze_text(text, source=source)
        self.last_text_analysis = ta.to_dict()

        # Enrichissement avec les mesures vivantes
        ct = self.engine._core.texte(text[:5000], source=source)

        return {
            "available": True,
            "source": source,
            "key_concepts": ta.key_concepts[:20],
            "propositions": [p.to_dict() for p in ta.propositions[:20]],
            "entities": [e.to_dict() for e in ta.named_entities[:10]],
            "themes": ta.themes[:10],
            "theses": ta.theses[:5],
            "objections": ta.objections[:5],
            "conclusions": ta.conclusions[:4],
            "discourse": ta.discourse_structure[:10],
            "lexical_density": ta.lexical_density,
            "sentence_count": ta.sentence_count,
            # Mesures vivantes
            "resonance": round(ct.resonance, 3),
            "surprise": round(ct.surprise, 3),
            "tension": round(ct.tension, 3),
            "charge_emotionnelle": round(ct.charge_emotionnelle, 3),
            "parser": "pure_python",
        }

    def coherence_check(self, response: str) -> bool:
        """Vérifie la cohérence d'une réponse avec les concepts actifs."""
        return self.engine._core.est_coherente(response)

    def meta_check(self, text: str) -> bool:
        """Détecte les fuites de métadonnées dans un texte."""
        return self.engine.detect_meta_leak(text)

    def living_state(self) -> Dict[str, Any]:
        """État vivant du graphe — propre à cette version pure."""
        return self.engine.get_living_state()


# ═══════════════════════════════════════════════════════════════════════════════
# COMPATIBILITÉ — get_nlp_legacy pour les modules qui importaient spaCy directement
# ═══════════════════════════════════════════════════════════════════════════════

def get_nlp():
    """
    Retourne None — pas de spaCy.
    Compatibilité pour les modules qui appelaient _get_nlp().
    """
    return None


def get_nlp_legacy():
    """Alias de get_nlp() — compatibilité maximale."""
    return None


def spacy_model_info() -> Dict[str, Any]:
    """Compatibilité avec leia_spacy_engine.spacy_model_info()"""
    return {
        "available": False,
        "loaded": False,
        "model": "pure_python",
        "has_vectors": False,
        "engine": "leia_comprehension_vivante",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 60)
    print("  nlp_integration_pure — Diagnostic")
    print("  Pure Python | Zéro dépendance")
    print("=" * 60)

    bridge = LeiaNLPBridge()

    # Test signal
    print("\n── TEST signal() ──────────────────────────────────────")
    msgs = [
        "Est-ce que la liberté peut exister sans contrainte ?",
        "Je ne suis pas d'accord — la mémoire n'est pas un tiroir.",
        "Bergson affirme que la durée est irréductible à l'espace.",
    ]
    for msg in msgs:
        s = bridge.signal(msg)
        print(f"\n  ▶ {msg[:55]}")
        print(f"    intent     : {s['intent']}")
        print(f"    focus      : {s['focus_concepts'][:4]}")
        print(f"    stance     : {s['stance']} | modal : {s['modality']}")
        print(f"    résonance  : {s['resonance']} | surprise : {s['surprise']}")
        print(f"    parser     : {s['parser']}")

    # Test analyze_book_chunk
    print("\n── TEST analyze_book_chunk() ──────────────────────────")
    passage = (
        "Bergson affirme que la mémoire n'est pas un tiroir. "
        "Elle est durée vécue, flux irréductible au stockage. "
        "Locke, au contraire, la fonde sur des impressions fixes. "
        "Cette opposition révèle deux philosophies du temps."
    )
    r = bridge.analyze_book_chunk(passage, source="Bergson test")
    print(f"\n  Concepts clés : {r['key_concepts'][:8]}")
    print(f"  Thèmes        : {r['themes'][:4]}")
    print(f"  Propositions  : {len(r['propositions'])}")
    print(f"  Résonance     : {r['resonance']} | Surprise : {r['surprise']}")
    print(f"  Parser        : {r['parser']}")

    # Stats
    print("\n── STATS ──────────────────────────────────────────────")
    print(f"  {engine.stats()}")

    print("\n  ✓ Zéro dépendance externe.")
    print("=" * 60)
