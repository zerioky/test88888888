# -*- coding: utf-8 -*-
"""
semantic_cortex.py — Cortex Sémantique Profond de Leia V20.2
═══════════════════════════════════════════════════════════════════════════════
Pure Python stdlib. Zéro dépendance. Zéro LLM.

Ce module ne produit PAS de "concepts".
Il produit des STRUCTURES COGNITIVES VIVANTES :
  • Cadres syntaxiques profonds (SVOI, subordonnées, complétives)
  • Liens causaux dirigés (cause → effet, condition → conséquence)
  • Tensions dialectiques (thèse ↔ antithèse)
  • Abstractions dynamiques (spécifique → général)
  • Scènes mentales (qui, quoi, où, quand, pourquoi, comment)
  • Implications prédictives (si X alors probablement Y)

Le workspace ne reçoit plus des signaux pré-mâchés.
Il reçoit des structures qu'il doit intégrer, animer, résoudre.
"""

from __future__ import annotations

import math
import random
import re
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# I. TYPES STRUCTURAUX — ce que le cortex extrait du langage
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CausalLink:
    """Lien causal dirigé avec force et temporalité."""
    cause: str           # concept cause
    effect: str          # concept effet
    force: float = 0.7   # 0-1, confiance dans le lien
    direction: str = "→" # "→" direct, "↔" bidirectionnel, "⊣" inhibiteur
    trigger: str = ""    # mot déclencheur ("parce que", "donc", "si")
    temporalite: str = "simultané"  # "avant", "simultané", "après", "conditionnel"
    source_text: str = ""

@dataclass
class DialecticalTension:
    """Contradiction ou opposition structurale entre deux propositions."""
    these: str
    antithese: str
    force: float = 0.5
    type_tension: str = "opposition"  # opposition, contradiction, exclusion, dilemme
    connecteur: str = ""
    source_text: str = ""

@dataclass
class AbstractionEdge:
    """Relation d'abstraction : spécifique → général."""
    specifique: str
    general: str
    force: float = 0.6
    type_abstraction: str = "instanciation"  # instanciation, métonymie, synecdoque, analogie

@dataclass
class PredictiveImplication:
    """Implication prédictive : si A, alors probablement B."""
    premise: str
    conclusion: str
    probability: float = 0.5
    confidence: float = 0.5
    context: str = ""

@dataclass
class SceneFrame:
    """
    Scène mentale : représentation situationnelle complète.
    Qui fait quoi, à qui, où, quand, pourquoi, comment.
    """
    sujet: str = ""
    action: str = ""
    objet: str = ""
    instrument: str = ""    # comment
    but: str = ""           # pourquoi
    lieu: str = ""          # où
    moment: str = ""        # quand
    modalite: str = "assertion"  # assertion, question, ordre, souhait
    negation: bool = False
    emotional_valence: float = 0.0

@dataclass
class SyntacticFrame:
    """Cadre syntaxique profond avec dépendances."""
    sujet: str = ""
    verbe: str = ""
    objet_direct: str = ""
    objet_indirect: str = ""
    circonstanciels: Dict[str, str] = field(default_factory=dict)  # temps, lieu, manière, cause
    subordonnees: List[str] = field(default_factory=list)
    coordonnees: List[str] = field(default_factory=list)
    negation: bool = False
    modality: str = "assertion"


# ═══════════════════════════════════════════════════════════════════════════════
# II. LEXIQUES PROFONDS — patterns linguistiques structuraux
# ═══════════════════════════════════════════════════════════════════════════════

_CAUSAL_TRIGGERS: Dict[str, Tuple[str, float, str]] = {
    # mot → (direction, force_par_défaut, temporalité)
    "parce que": ("→", 0.85, "avant"),
    "car": ("→", 0.80, "avant"),
    "puisque": ("→", 0.75, "avant"),
    "donc": ("←", 0.80, "après"),  # effet ← cause
    "ainsi": ("←", 0.70, "après"),
    "c'est pourquoi": ("←", 0.85, "après"),
    "de ce fait": ("←", 0.75, "après"),
    "par conséquent": ("←", 0.80, "après"),
    "si": ("→", 0.70, "conditionnel"),
    "alors": ("←", 0.65, "conditionnel"),
    "sans": ("⊣", 0.60, "conditionnel"),  # inhibition
    "grâce à": ("→", 0.75, "avant"),
    "à cause de": ("→", 0.80, "avant"),
    "en raison de": ("→", 0.75, "avant"),
    "même si": ("↔", 0.50, "conditionnel"),  # tension conditionnelle
    "bien que": ("↔", 0.55, "conditionnel"),
    "quoique": ("↔", 0.55, "conditionnel"),
    "d'où": ("←", 0.75, "après"),
    "résulte de": ("→", 0.70, "avant"),
    "engendre": ("→", 0.80, "après"),
    "produit": ("→", 0.75, "après"),
    "permet": ("→", 0.65, "conditionnel"),
    "détermine": ("→", 0.80, "avant"),
    "conditionne": ("→", 0.75, "avant"),
    "implique": ("→", 0.70, "conditionnel"),
}

_DIALECTICAL_MARKERS: Dict[str, Tuple[str, float]] = {
    "mais": ("opposition", 0.7),
    "cependant": ("opposition", 0.6),
    "pourtant": ("opposition", 0.65),
    "néanmoins": ("opposition", 0.6),
    "toutefois": ("opposition", 0.6),
    "au contraire": ("contradiction", 0.8),
    "en revanche": ("opposition", 0.65),
    "malgré": ("opposition", 0.6),
    "alors que": ("contradiction", 0.55),
    "tandis que": ("opposition", 0.5),
    "non pas": ("contradiction", 0.85),
    "plutôt que": ("exclusion", 0.7),
    "au lieu de": ("exclusion", 0.7),
}

_ABSTRACTION_MARKERS: Dict[str, str] = {
    "c'est-à-dire": "instanciation",
    "autrement dit": "instanciation",
    "c'est": "instanciation",
    "en d'autres termes": "instanciation",
    "comme": "analogie",
    "tel que": "analogie",
    "de même que": "analogie",
    "à l'image de": "analogie",
    "signifie": "instanciation",
    "représente": "métonymie",
    "symbolise": "métonymie",
    "incarne": "métonymie",
}

_PREDICTIVE_MARKERS: Dict[str, float] = {
    "probablement": 0.6,
    "sans doute": 0.65,
    "peut-être": 0.4,
    "vraisemblablement": 0.7,
    "certainement": 0.9,
    "forcément": 0.85,
    "nécessairement": 0.9,
    "inévitablement": 0.85,
    "doucement": 0.3,
}

_CIRCUMSTANTIELS: Dict[str, List[str]] = {
    "temps": ["quand", "lorsque", "pendant", "avant", "après", "depuis", "dès que", "tandis que"],
    "lieu": ["où", "dans", "sur", "sous", "à", "chez", "vers", "loin de"],
    "manière": ["comment", "ainsi", "tellement", "vite", "lentement", "avec"],
    "cause": ["parce que", "car", "puisque", "à cause de", "en raison de", "grâce à"],
    "but": ["pour", "afin de", "dans le but de", "pour que", "de sorte que"],
}

_MODALITY_MARKERS: Dict[str, str] = {
    "est-ce que": "question",
    "pourquoi": "question",
    "comment": "question",
    "quoi": "question",
    "qui": "question",
    "que": "question",
    "quand": "question",
    "où": "question",
    "faut-il": "question",
    "peut-on": "question",
    "doit-on": "question",
    "devons-nous": "question",
    "il faut": "necessite",
    "il doit": "necessite",
    "il ne faut pas": "interdiction",
    "ne dois pas": "interdiction",
    "je veux": "desir",
    "je souhaite": "desir",
    "j'espère": "espoir",
    "je crains": "peur",
    "j'ai peur que": "peur",
}


# ═══════════════════════════════════════════════════════════════════════════════
# III. MORPHOLOGIE MINIMALE — lemmatisation rapide pour le cortex
# ═══════════════════════════════════════════════════════════════════════════════

class CortexMorphology:
    """Morphologie légère mais suffisante pour le parsing structurel profond."""

    _STOP = {"le","la","les","un","une","des","de","du","et","en","est","à","il","elle",
             "on","je","tu","nous","vous","se","sa","son","ses","me","te","lui","leur",
             "que","qui","quoi","dont","où","mais","ou","donc","or","ni","car","si",
             "avec","sans","sous","sur","dans","par","pour","vers","chez","comme",
             "ce","cet","cette","ces","mon","ton","notre","votre","être","avoir","faire",
             "aller","voir","venir","dire","savoir","ça","y","qu","j","m","t","s","n","c",
             "pas","ne","plus","déjà","encore","toujours","jamais","rien","aucun","très",
             "trop","assez","peu","beaucoup","même","aussi","bien","tout","tous","toute","toutes",
             "ceci","cela","voilà","voici"}

    _PRONOMS = {"je","tu","il","elle","on","nous","vous","ils","elles","le","la","les","lui","leur"}

    @classmethod
    def tokenize(cls, text: str) -> List[Dict[str, Any]]:
        tokens = []
        for m in re.finditer(r"[a-zA-ZÀ-ÿ'\-]{2,}", text):
            w = m.group(0).lower().strip("'")
            if w in cls._STOP and len(w) < 4:
                pos = "STOP"
            elif w in cls._PRONOMS:
                pos = "PRON"
            elif re.search(r"(er|ir|re|oir)$", w) and len(w) > 3:
                pos = "VERB"
            elif re.search(r"(tion|sion|ment|ité|eur|isme|age|ure|oire|eur|euse|ance|ence)$", w):
                pos = "NOUN"
            elif re.search(r"(ment)$", w):
                pos = "ADV"
            elif re.search(r"(able|ible|if|ive|eux|euse|ant|ent|al|el|in|ique)$", w):
                pos = "ADJ"
            else:
                pos = "OTHER"
            tokens.append({"text": m.group(0), "norm": w, "pos": pos, "start": m.start()})
        return tokens

    @classmethod
    def content_words(cls, text: str) -> List[str]:
        return [t["norm"] for t in cls.tokenize(text)
                if t["pos"] not in ("STOP",) and len(t["norm"]) > 2
                and t["norm"] not in cls._STOP]


# ═══════════════════════════════════════════════════════════════════════════════
# IV. PARSEUR SYNTAXIQUE PROFOND — extraction de cadres et scènes
# ═══════════════════════════════════════════════════════════════════════════════

class DeepSyntacticParser:
    """
    Parseur syntaxique profond qui extrait :
      - Cadres SVO + objets indirects + circonstanciels
      - Subordonnées et propositions juxtaposées
      - Structures causales emboîtées
    """

    def __init__(self):
        self.morpho = CortexMorphology()

    def parse(self, text: str) -> List[SyntacticFrame]:
        phrases = self._segment(text)
        return [self._parse_phrase(p) for p in phrases if len(p.strip()) > 5]

    def _segment(self, text: str) -> List[str]:
        text = re.sub(r"\b(M|Mme|Mlle|Dr|Prof|etc|vol|p|pp|art|fig|cf|op|cit|ibid)\.", r"\1§", text)
        parts = re.split(r"(?<=[.!?…])\s+(?=[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ\"\«])", text)
        return [p.replace("§", ".").strip() for p in parts if p.strip()]

    def _parse_phrase(self, phrase: str) -> SyntacticFrame:
        toks = self.morpho.tokenize(phrase)
        low = phrase.lower()

        frame = SyntacticFrame()
        frame.negation = self._detect_negation(low)
        frame.modality = self._detect_modality(low)

        # Découpage sur les subordonnées causales
        sub_parts = self._split_subordinate(phrase)
        frame.subordonnees = sub_parts[1:]
        main_text = sub_parts[0]

        # Parsing du cadre principal
        main_toks = self.morpho.tokenize(main_text)
        frame.sujet = self._extract_subject(main_toks)
        frame.verbe = self._extract_verb(main_toks)
        frame.objet_direct = self._extract_object(main_toks, frame.verbe)
        frame.objet_indirect = self._extract_indirect_object(main_text)
        frame.circonstanciels = self._extract_circumstantials(main_text)
        frame.coordonnees = self._extract_coordinated(main_text)

        return frame

    def _detect_negation(self, low: str) -> bool:
        return bool(re.search(r"\b(ne|n'|non|jamais|rien|aucun|nullement|ni)\b", low))

    def _detect_modality(self, low: str) -> str:
        for marker, mod in _MODALITY_MARKERS.items():
            if marker in low:
                return mod
        if "?" in low:
            return "question"
        return "assertion"

    def _split_subordinate(self, text: str) -> List[str]:
        """Découpe les propositions sur les marqueurs de subordination."""
        markers = ["parce que", "car", "puisque", "quand", "lorsque", "si", "bien que",
                   "quoique", "même si", "alors que", "tandis que", "pendant que",
                   "après que", "avant que", "dès que", "pour que", "afin que"]
        parts = [text]
        for mk in markers:
            new_parts = []
            for part in parts:
                if mk in part.lower():
                    splitted = re.split(rf"(?i)\b{re.escape(mk)}\b", part, maxsplit=1)
                    new_parts.append(splitted[0].strip())
                    if len(splitted) > 1:
                        new_parts.append(mk + " " + splitted[1].strip())
                else:
                    new_parts.append(part)
            parts = [p for p in new_parts if p.strip()]
        return parts

    def _extract_subject(self, toks: List[Dict]) -> str:
        for i, t in enumerate(toks):
            if t["pos"] == "PRON" and t["norm"] in {"je","tu","il","elle","on","nous","vous","ils","elles"}:
                return t["norm"]
            if t["pos"] in ("NOUN","OTHER") and len(t["norm"]) > 2:
                # Vérifie qu'il y a un verbe après
                for j in range(i+1, min(len(toks), i+6)):
                    if toks[j]["pos"] == "VERB":
                        return t["norm"]
        return ""

    def _extract_verb(self, toks: List[Dict]) -> str:
        for t in toks:
            if t["pos"] == "VERB":
                return t["norm"]
        return ""

    def _extract_object(self, toks: List[Dict], verb: str) -> str:
        verb_seen = False
        for t in toks:
            if t["norm"] == verb:
                verb_seen = True
                continue
            if verb_seen and t["pos"] in ("NOUN","OTHER") and len(t["norm"]) > 2:
                return t["norm"]
        return ""

    def _extract_indirect_object(self, text: str) -> str:
        m = re.search(r"\b(à|pour|avec|contre|sur|chez|de|dans)\s+([a-zA-ZÀ-ÿ'\-]{3,20})", text, re.IGNORECASE)
        return m.group(2).lower() if m else ""

    def _extract_circumstantials(self, text: str) -> Dict[str, str]:
        found = {}
        low = text.lower()
        for cat, markers in _CIRCUMSTANTIELS.items():
            for mk in markers:
                if mk in low:
                    m = re.search(rf"{re.escape(mk)}\s+(.{{5,40}}?)(?:[,;]|$)", low)
                    if m:
                        found[cat] = m.group(1).strip()
                        break
        return found

    def _extract_coordinated(self, text: str) -> List[str]:
        parts = re.split(r"\b,\s*(et|ou|mais|ni)\s+", text, flags=re.IGNORECASE)
        return [p.strip() for p in parts[::2] if p.strip() and len(p.strip()) > 5]


# ═══════════════════════════════════════════════════════════════════════════════
# V. EXTRACTEUR CAUSAL — construction du graphe causal
# ═══════════════════════════════════════════════════════════════════════════════

class CausalExtractor:
    """Extrait des liens causaux à partir du texte brut."""

    def __init__(self, parser: DeepSyntacticParser):
        self.parser = parser

    def extract(self, text: str) -> List[CausalLink]:
        links = []
        low = text.lower()

        # 1. Détection par marqueurs explicites
        for trigger, (direction, force_default, temp) in _CAUSAL_TRIGGERS.items():
            for m in re.finditer(rf"\b{re.escape(trigger)}\b", low):
                # Contexte autour du marqueur
                start = max(0, m.start() - 80)
                end = min(len(text), m.end() + 80)
                context = text[start:end]

                # Extraction heuristique de cause/effet
                before = text[start:m.start()].strip()
                after = text[m.end():end].strip()

                cause, effect = self._infer_cause_effect(before, after, direction, trigger)
                if cause and effect:
                    links.append(CausalLink(
                        cause=cause[:40],
                        effect=effect[:40],
                        force=force_default,
                        direction=direction,
                        trigger=trigger,
                        temporalite=temp,
                        source_text=context[:80],
                    ))

        # 2. Détection par structure "X produit/engendre Y"
        for verb in ["produit", "engendre", "crée", "cause", "détermine", "conditionne", "implique",
                     "entraîne", "provoque", "génère", "suscite", "déclenche", "fait naître"]:
            for m in re.finditer(
                rf"([a-zA-ZÀ-ÿ'\s]{{5,40}}?)\s+(?:ne\s+)?(?:pas\s+)?(?:se\s+)?{re.escape(verb)}(?:nt|s|t|r|nt)?\s+(.{{5,40}}?)(?:[,;]|$)",
                low
            ):
                cause = self._clean_concept(m.group(1))
                effect = self._clean_concept(m.group(2))
                if cause and effect and cause != effect:
                    links.append(CausalLink(
                        cause=cause, effect=effect, force=0.75,
                        direction="→", trigger=verb,
                        temporalite="après", source_text=m.group(0)[:80],
                    ))

        return self._deduplicate(links)

    def _infer_cause_effect(self, before: str, after: str, direction: str, trigger: str) -> Tuple[str, str]:
        before_c = self._clean_concept(before)
        after_c = self._clean_concept(after)

        if direction == "→":
            return before_c, after_c
        elif direction == "←":
            return after_c, before_c
        elif direction == "↔":
            return before_c, after_c  # Tension causale
        elif direction == "⊣":
            return before_c, after_c  # Inhibition
        return "", ""

    def _clean_concept(self, text: str) -> str:
        words = CortexMorphology.content_words(text)
        return " ".join(words[:4])[:50] if words else ""

    def _deduplicate(self, links: List[CausalLink]) -> List[CausalLink]:
        seen = set()
        result = []
        for l in links:
            key = f"{l.cause}|{l.effect}|{l.direction}"
            if key not in seen:
                seen.add(key)
                result.append(l)
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# VI. EXTRACTEUR DIALECTIQUE — tensions et contradictions
# ═══════════════════════════════════════════════════════════════════════════════

class DialecticalExtractor:
    """Extrait les tensions dialectiques du texte."""

    def extract(self, text: str) -> List[DialecticalTension]:
        tensions = []
        low = text.lower()

        for marker, (t_type, force) in _DIALECTICAL_MARKERS.items():
            for m in re.finditer(rf"\b{re.escape(marker)}\b", low):
                start = max(0, m.start() - 60)
                end = min(len(text), m.end() + 60)
                before = text[start:m.start()].strip()
                after = text[m.end():end].strip()

                these = self._extract_proposition(before)
                antithese = self._extract_proposition(after)

                if these and antithese:
                    tensions.append(DialecticalTension(
                        these=these[:50], antithese=antithese[:50],
                        force=force, type_tension=t_type,
                        connecteur=marker,
                        source_text=text[start:end][:80],
                    ))

        # Détection "X n'est pas Y" comme contradiction interne
        for m in re.finditer(
            r"([a-zA-ZÀ-ÿ\s]{3,25})\s+(?:n['e]?(?:est|était|sera|semble|paraît))\s+(?:pas|plus|guère|jamais)\s+(?:un |une |des |le |la |les |l')?([a-zA-ZÀ-ÿ\s]{3,35})",
            low
        ):
            tensions.append(DialecticalTension(
                these=m.group(1).strip()[:40],
                antithese=m.group(2).strip()[:40],
                force=0.8, type_tension="contradiction",
                connecteur="n'est pas",
                source_text=m.group(0)[:80],
            ))

        return tensions

    def _extract_proposition(self, text: str) -> str:
        words = CortexMorphology.content_words(text)
        return " ".join(words[:5]) if words else ""


# ═══════════════════════════════════════════════════════════════════════════════
# VII. EXTRACTEUR D'ABSTRACTION — méta-niveaux
# ═══════════════════════════════════════════════════════════════════════════════

class AbstractionExtractor:
    """Extrait les relations d'abstraction et d'analogie."""

    def extract(self, text: str) -> List[AbstractionEdge]:
        edges = []
        low = text.lower()

        for marker, a_type in _ABSTRACTION_MARKERS.items():
            for m in re.finditer(rf"\b{re.escape(marker)}\b", low):
                start = max(0, m.start() - 40)
                end = min(len(text), m.end() + 60)
                before = text[start:m.start()].strip()
                after = text[m.end():end].strip()

                spec = self._clean(before)
                gen = self._clean(after)
                if spec and gen:
                    edges.append(AbstractionEdge(
                        specifique=spec[:40], general=gen[:40],
                        force=0.7, type_abstraction=a_type,
                    ))

        # Pattern : "la X est une forme de Y"
        for m in re.finditer(
            r"(?:la |le |les |l'|une |un )?([a-zA-ZÀ-ÿ\s]{3,25})\s+(?:est|sont|constitue|représente|forme)\s+(?:une |un |des )?([a-zA-ZÀ-ÿ\s]{3,35})",
            low
        ):
            edges.append(AbstractionEdge(
                specifique=m.group(1).strip()[:40],
                general=m.group(2).strip()[:40],
                force=0.75, type_abstraction="instanciation",
            ))

        return edges

    def _clean(self, text: str) -> str:
        words = CortexMorphology.content_words(text)
        return " ".join(words[:4]) if words else ""


# ═══════════════════════════════════════════════════════════════════════════════
# VIII. SCÈNE MENTALE — construction de la représentation situationnelle
# ═══════════════════════════════════════════════════════════════════════════════

class SceneBuilder:
    """Construit une scène mentale à partir du texte."""

    def __init__(self, parser: DeepSyntacticParser):
        self.parser = parser

    def build(self, text: str) -> List[SceneFrame]:
        frames = []
        syntactic = self.parser.parse(text)
        words = CortexMorphology.content_words(text)

        for frame in syntactic:
            scene = SceneFrame(
                sujet=frame.sujet,
                action=frame.verbe,
                objet=frame.objet_direct,
                but=frame.circonstanciels.get("but", ""),
                lieu=frame.circonstanciels.get("lieu", ""),
                moment=frame.circonstanciels.get("temps", ""),
                instrument=frame.circonstanciels.get("manière", ""),
                modalite=frame.modality,
                negation=frame.negation,
            )
            # Valence émotionnelle approximative
            scene.emotional_valence = self._valence_from_words(words)
            frames.append(scene)

        return frames

    def _valence_from_words(self, words: List[str]) -> float:
        VALENCE = {
            "joie":0.9,"bonheur":0.8,"espoir":0.7,"amour":0.9,"liberté":0.7,
            "paix":0.6,"vie":0.5,"lumière":0.6,"beauté":0.7,"vérité":0.6,
            "peur":-0.7,"mort":-0.8,"souffrance":-0.8,"haine":-0.9,"douleur":-0.7,
            "angoisse":-0.6,"désespoir":-0.8,"terreur":-0.9,"tristesse":-0.6,
            "colère":-0.5,"mal":-0.6,"faux":-0.4,"vide":-0.5,"néant":-0.6,
        }
        scores = [VALENCE.get(w, 0.0) for w in words]
        active = [s for s in scores if s != 0.0]
        return sum(active) / len(active) if active else 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# IX. STRUCTURE COGNITIVE COMPLÈTE — sortie du cortex
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CognitiveStructure:
    """Ce que Leia a VRAIMENT compris d'un texte. Pas des mots. Des structures."""
    raw: str

    # Syntaxe profonde
    syntactic_frames: List[SyntacticFrame] = field(default_factory=list)

    # Sémantique structurale
    causal_links: List[CausalLink] = field(default_factory=list)
    tensions: List[DialecticalTension] = field(default_factory=list)
    abstractions: List[AbstractionEdge] = field(default_factory=list)
    implications: List[PredictiveImplication] = field(default_factory=list)

    # Scènes
    scenes: List[SceneFrame] = field(default_factory=list)

    # Concepts atomiques (pour compatibilité ancienne)
    concepts: List[str] = field(default_factory=list)

    # Métas
    emotional_valence: float = 0.0
    emotional_arousal: float = 0.3
    complexity: float = 0.0
    is_question: bool = False
    is_personal: bool = False
    modality: str = "assertion"
    source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw": self.raw[:100],
            "n_frames": len(self.syntactic_frames),
            "n_causal": len(self.causal_links),
            "n_tensions": len(self.tensions),
            "n_abstractions": len(self.abstractions),
            "n_scenes": len(self.scenes),
            "concepts": self.concepts[:12],
            "causal_summary": [f"{c.cause} {c.direction} {c.effect}" for c in self.causal_links[:4]],
            "tensions_summary": [f"{t.these} ↔ {t.antithese}" for t in self.tensions[:4]],
            "scenes_summary": [f"{s.sujet} {s.action} {s.objet}" for s in self.scenes[:3]],
            "emotional_valence": round(self.emotional_valence, 3),
            "modality": self.modality,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# X. SEMANTIC CORTEX — point d'entrée unique
# ═══════════════════════════════════════════════════════════════════════════════

class SemanticCortex:
    """
    Cortex sémantique profond de Leia.
    Prend du texte brut.
    Produit des structures cognitives vivantes.
    """

    def __init__(self):
        self.parser = DeepSyntacticParser()
        self.causal = CausalExtractor(self.parser)
        self.dialectical = DialecticalExtractor()
        self.abstraction = AbstractionExtractor()
        self.scene = SceneBuilder(self.parser)

    def process(self, text: str, source: str = "") -> CognitiveStructure:
        if not text or not text.strip():
            return CognitiveStructure(raw="")

        # 1. Structures syntaxiques profondes
        frames = self.parser.parse(text)

        # 2. Causalité
        causal_links = self.causal.extract(text)

        # 3. Tensions dialectiques
        tensions = self.dialectical.extract(text)

        # 4. Abstractions
        abstractions = self.abstraction.extract(text)

        # 5. Scènes mentales
        scenes = self.scene.build(text)

        # 6. Concepts atomiques (pour pont avec workspace)
        concepts = CortexMorphology.content_words(text)
        # Enrichir avec sujets/verbes/objets des cadres
        for f in frames:
            for c in [f.sujet, f.verbe, f.objet_direct]:
                if c and c not in concepts:
                    concepts.append(c)

        # 7. Implications prédictives (dérivées des liens causaux conditionnels)
        implications: List[PredictiveImplication] = []
        for cl in causal_links:
            if cl.temporalite == "conditionnel":
                implications.append(PredictiveImplication(
                    premise=cl.cause, conclusion=cl.effect,
                    probability=cl.force, confidence=cl.force,
                    context=cl.trigger,
                ))

        # 8. Métas
        valence = self.scene._valence_from_words(concepts)
        is_q = "?" in text or any(m in text.lower() for m in ["est-ce", "pourquoi", "comment", "qui", "quoi"])
        is_p = any(w in text.lower() for w in ["je", "mon", "ma", "mes", "moi", "j'"])

        complexity = len(set(concepts)) / max(len(concepts), 1)

        return CognitiveStructure(
            raw=text,
            syntactic_frames=frames,
            causal_links=causal_links,
            tensions=tensions,
            abstractions=abstractions,
            implications=implications,
            scenes=scenes,
            concepts=concepts[:15],
            emotional_valence=valence,
            emotional_arousal=0.3 + abs(valence) * 0.3 + (0.2 if tensions else 0),
            complexity=complexity,
            is_question=is_q,
            is_personal=is_p,
            modality=frames[0].modality if frames else "assertion",
            source=source,
        )


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("═" * 70)
    print("  SEMANTIC CORTEX — Diagnostic")
    print("  Pure Python · Structures cognitives · Zéro LLM")
    print("═" * 70)

    cortex = SemanticCortex()

    tests = [
        "Parce que la liberté suppose la contrainte, l'existence individuelle est une tension permanente.",
        "Je ne suis pas d'accord : la mémoire n'est pas un tiroir, mais une durée vécue.",
        "Si l'intelligence artificielle efface l'essentiel en nous, alors l'humanité perdra sa continuité.",
        "Bergson affirme que la durée est irréductible à l'espace, ce qui signifie que le temps vécu ne se mesure pas.",
        "Mais Locke, au contraire, fonde la mémoire sur des impressions fixes. Qui a raison ?",
    ]

    for i, t in enumerate(tests, 1):
        struct = cortex.process(t)
        print(f"\n  [{i}] {t[:65]}...")
        print(f"      Concepts    : {struct.concepts[:6]}")
        print(f"      Causalités  : {len(struct.causal_links)} | {struct.causal_links[0].cause} → {struct.causal_links[0].effect}" if struct.causal_links else "      Causalités  : 0")
        print(f"      Tensions    : {len(struct.tensions)} | {struct.tensions[0].these} ↔ {struct.tensions[0].antithese}" if struct.tensions else "      Tensions    : 0")
        print(f"      Abstractions: {len(struct.abstractions)}" + (f" | {struct.abstractions[0].specifique} → {struct.abstractions[0].general}" if struct.abstractions else ""))
        print(f"      Scènes      : {len(struct.scenes)} | {struct.scenes[0].sujet} {struct.scenes[0].action} {struct.scenes[0].objet}" if struct.scenes else "      Scènes      : 0")
        print(f"      Valence     : {struct.emotional_valence:+.3f} | Arousal : {struct.emotional_arousal:.3f} | Modalité : {struct.modality}")

    print("\n" + "═" * 70)
