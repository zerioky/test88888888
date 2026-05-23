"""
proposition_extractor.py — V18
================================
Extraction de propositions (sujet, relation, objet) depuis les livres.

Sans LLM. Utilise spaCy si disponible, sinon patterns syntaxiques.

Objectif : Leia ne stocke plus des mots isolés depuis les livres,
elle stocke des RELATIONS entre concepts.

Exemple :
  "La mémoire, selon Bergson, n'est pas un tiroir mais une durée vécue"
  →  (mémoire, ne_être_pas, tiroir)
     (mémoire, être, durée_vécue)
     (Bergson, affirmer, durée_vécue)

Ces triplets forment un graphe sémantique propre que la mémoire
associative peut traverser et que le weaver peut formuler.

C'est la différence entre stocker un dictionnaire
et comprendre ce que le livre AFFIRME.
"""

from __future__ import annotations
import re, json, os, time
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict

_SPACY_AVAILABLE = False
_NLP_REF = [None]  # cache partagé

try:
    import spacy as _spacy_mod
    _SPACY_AVAILABLE = True
except ImportError:
    _spacy_mod = None  # type: ignore

def _get_nlp():
    if _NLP_REF[0] is not None:
        return _NLP_REF[0]
    if not _SPACY_AVAILABLE:
        return None
    for model in ("fr_core_news_lg","fr_core_news_md","fr_core_news_sm"):
        try:
            _NLP_REF[0] = _spacy_mod.load(model)
            return _NLP_REF[0]
        except Exception:
            continue
    return None

_STOP = {
    "le","la","les","un","une","des","de","du","et","en","est","à","au","aux",
    "il","elle","ils","elles","on","ce","cet","cette","ces","se","sa","son",
    "ses","leur","leurs","tout","même","bien","plus","moins","très",
    "aussi","encore","toujours","jamais","rien","pas","ne","non",
}

# Verbes épistémiques importants en philosophie
_EPISTEMIC_VERBS = {
    "être","avoir","faire","dire","penser","croire","savoir","vouloir",
    "pouvoir","devoir","affirmer","nier","montrer","démontrer","prouver",
    "supposer","postuler","définir","concevoir","considérer","estimer",
    "reconnaître","admettre","rejeter","contester","distinguer","opposer",
    "comparer","expliquer","analyser","définir","qualifier","appeler",
    "désigner","nommer","identifier","constituer","former","produire",
    "engendrer","causer","déterminer","conditionner","permettre",
}

# Connecteurs d'opposition → crée une tension conceptuelle
_OPPOSITION_CONNECTORS = {
    "mais","cependant","pourtant","néanmoins","toutefois","au contraire",
    "en revanche","à l'opposé","malgré","bien que","quoique","alors que",
    "tandis que","alors même","non pas","plutôt que","au lieu de",
}

# Connecteurs de causalité → crée un lien causal
_CAUSAL_CONNECTORS = {
    "car","parce que","puisque","donc","ainsi","c'est pourquoi","en effet",
    "de ce fait","par conséquent","il s'ensuit","d'où","ce qui explique",
    "ce qui produit","ce qui cause","ce qui permet","en conséquence",
}


class Proposition:
    """Un triplet sémantique extrait d'un texte."""

    __slots__ = ("subject","relation","object","negated","source",
                 "confidence","created_at","connector_type")

    def __init__(self, subject: str, relation: str, obj: str,
                 negated: bool = False, source: str = "",
                 confidence: float = 0.7, connector_type: str = ""):
        self.subject        = subject.strip().lower()
        self.relation       = relation.strip().lower()
        self.object         = obj.strip().lower()
        self.negated        = negated
        self.source         = source
        self.confidence     = min(1.0, max(0.0, confidence))
        self.created_at     = time.time()
        self.connector_type = connector_type  # "opposition", "causal", ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject":        self.subject,
            "relation":       ("ne_" if self.negated else "") + self.relation,
            "object":         self.object,
            "negated":        self.negated,
            "source":         self.source,
            "confidence":     round(self.confidence, 3),
            "connector_type": self.connector_type,
            "created_at":     self.created_at,
        }

    def key(self) -> str:
        neg = "n" if self.negated else "p"
        return f"{self.subject}|{neg}{self.relation}|{self.object}"

    def concepts(self) -> List[str]:
        """Tous les concepts de cette proposition."""
        return [c for c in (self.subject, self.object) if c and len(c) > 2]

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Proposition":
        rel = str(d.get("relation",""))
        neg = rel.startswith("ne_")
        if neg: rel = rel[3:]
        return cls(
            subject=d.get("subject",""),
            relation=rel,
            obj=d.get("object",""),
            negated=neg or bool(d.get("negated",False)),
            source=d.get("source",""),
            confidence=float(d.get("confidence",0.7)),
            connector_type=d.get("connector_type",""),
        )


class _LightPropositionParser:
    """
    Extraction de propositions par patterns regex.
    Utilisé quand spaCy n'est pas disponible.
    """

    # Patterns : (sujet)(copule/verbe)(objet)
    _PATTERNS = [
        # "X est Y" / "X n'est pas Y"
        (r"(\b[\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,2})\s+(n'est pas|n'est|n'était pas|n'était|est|était|sont|étaient|sera|serait)\s+([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,3})",
         "être"),
        # "X constitue Y" / "X représente Y"
        (r"(\b[\wÀ-ÿ']{4,}(?:\s+[\wÀ-ÿ']{4,}){0,1})\s+(constitue|représente|désigne|signifie|implique|produit|engendre|cause|permet|explique)\s+([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,3})",
         None),  # verbe pris du match
        # "selon X, Y"
        (r"selon\s+([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+)?)\s*,\s*([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,4})",
         "affirmer"),
        # "X → Y" (implication explicite)
        (r"([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,2})\s+(?:implique|entraîne|produit|conduit à|mène à)\s+([\wÀ-ÿ']+(?:\s+[\wÀ-ÿ']+){0,3})",
         "impliquer"),
    ]

    def extract(self, text: str, source: str = "") -> List[Proposition]:
        props = []
        text_clean = re.sub(r"\s+", " ", text)

        for pattern, default_rel in self._PATTERNS:
            for m in re.finditer(pattern, text_clean, re.IGNORECASE):
                groups = m.groups()
                if len(groups) == 3:
                    subj, rel_or_verb, obj = groups
                    rel = default_rel if default_rel else rel_or_verb.lower()
                    neg = "n'" in rel_or_verb.lower() or "pas" in rel_or_verb.lower()
                    rel = re.sub(r"n['']\w*|pas\s+", "", rel).strip()
                elif len(groups) == 2:
                    subj, obj = groups
                    rel = default_rel or "affirmer"
                    neg = False
                else:
                    continue

                # Nettoyer
                subj = re.sub(r"\s+", " ", subj.strip().lower())
                obj  = re.sub(r"\s+", " ", obj.strip().lower())

                if (not subj or not obj or len(subj) < 3 or len(obj) < 3
                        or subj in _STOP or obj in _STOP):
                    continue

                # Type de connecteur
                ctx = text_clean[max(0, m.start()-60):m.end()+60].lower()
                conn_type = ""
                if any(c in ctx for c in _OPPOSITION_CONNECTORS):
                    conn_type = "opposition"
                elif any(c in ctx for c in _CAUSAL_CONNECTORS):
                    conn_type = "causal"

                props.append(Proposition(
                    subject=subj, relation=rel, obj=obj,
                    negated=neg, source=source,
                    confidence=0.55, connector_type=conn_type,
                ))

        return props


class _SpacyPropositionParser:
    """
    Extraction de propositions via analyse syntaxique spaCy.
    Bien plus précis : utilise les dépendances réelles.
    """

    def extract(self, text: str, source: str, nlp) -> List[Proposition]:
        props = []
        # Traiter par chunks (spaCy a une limite)
        chunks = [text[i:i+10000] for i in range(0, len(text), 9000)]

        for chunk in chunks[:5]:  # max 5 chunks par livre
            try:
                doc = nlp(chunk)
                props.extend(self._extract_from_doc(doc, source))
            except Exception:
                continue

        return props

    def _extract_from_doc(self, doc, source: str) -> List[Proposition]:
        props = []
        for sent in doc.sents:
            sent_props = self._sentence_props(sent, source)
            props.extend(sent_props)
        return props

    def _sentence_props(self, sent, source: str) -> List[Proposition]:
        props = []
        # Chercher le verbe principal (ROOT)
        for token in sent:
            if token.dep_ != "ROOT" or token.pos_ not in ("VERB","AUX"):
                continue

            # Sujet
            subjects = [c for c in token.children
                        if c.dep_ in ("nsubj","nsubj:pass","expl:subj")]
            # Objets / attributs
            objects = [c for c in token.children
                       if c.dep_ in ("obj","dobj","attr","xcomp","acomp",
                                     "iobj","obl")]
            # Négation
            negated = any(c.dep_ == "neg" for c in token.children)

            # Connecteur de contexte
            sent_text = sent.text.lower()
            conn_type = ""
            if any(c in sent_text for c in _OPPOSITION_CONNECTORS):
                conn_type = "opposition"
            elif any(c in sent_text for c in _CAUSAL_CONNECTORS):
                conn_type = "causal"

            for subj_tok in subjects:
                subj_str = self._expand_noun(subj_tok)
                if not subj_str or subj_str in _STOP: continue
                for obj_tok in objects:
                    obj_str = self._expand_noun(obj_tok)
                    if not obj_str or obj_str in _STOP: continue
                    props.append(Proposition(
                        subject=subj_str,
                        relation=token.lemma_.lower(),
                        obj=obj_str,
                        negated=negated,
                        source=source,
                        confidence=0.8 if token.lemma_.lower() in _EPISTEMIC_VERBS else 0.6,
                        connector_type=conn_type,
                    ))

            # Propositions attributives sans objet : X est/devient Y
            if not objects and token.lemma_ in ("être","devenir","rester","paraître","sembler"):
                attrs = [c for c in token.children if c.dep_ == "attr"]
                for subj_tok in subjects:
                    for attr_tok in attrs:
                        subj_str = self._expand_noun(subj_tok)
                        attr_str = self._expand_noun(attr_tok)
                        if subj_str and attr_str:
                            props.append(Proposition(
                                subject=subj_str, relation=token.lemma_.lower(),
                                obj=attr_str, negated=negated, source=source,
                                confidence=0.75, connector_type=conn_type,
                            ))

        return props

    def _expand_noun(self, token) -> str:
        """Récupère le groupe nominal autour d'un token."""
        # Inclure les modificateurs nominaux directs
        parts = []
        for child in token.lefts:
            if child.dep_ in ("amod","nmod","det") and not child.is_stop:
                parts.append(child.lemma_.lower())
        parts.append(token.lemma_.lower())
        for child in token.rights:
            if child.dep_ in ("amod","nmod") and not child.is_stop:
                parts.append(child.lemma_.lower())
        result = " ".join(p for p in parts if p not in _STOP and len(p) > 2)
        return result[:50]  # limiter la longueur


class PropositionExtractor:
    """
    Point d'entrée public.
    Extrait et stocke les propositions depuis les livres.
    Construit un graphe sémantique qui enrichit la mémoire associative.
    """

    MAX_PROPS = 1500  # limite de stockage

    def __init__(self, storage_path: str = "data/propositions_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self._light  = _LightPropositionParser()
        self._spacy_p = _SpacyPropositionParser()
        self._props: Dict[str, Proposition] = {}  # key → Proposition
        self._by_subject: Dict[str, List[str]] = defaultdict(list)  # sujet → [keys]
        self._by_concept: Dict[str, List[str]] = defaultdict(list)  # concept → [keys]
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            for d in data.get("propositions", []):
                p = Proposition.from_dict(d)
                self._store_prop(p)
        except Exception:
            pass

    def _save(self):
        try:
            props = sorted(self._props.values(),
                           key=lambda p: p.confidence, reverse=True)[:self.MAX_PROPS]
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "propositions": [p.to_dict() for p in props],
                    "count":        len(props),
                    "timestamp":    time.time(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _store_prop(self, p: Proposition):
        key = p.key()
        if key not in self._props:
            self._props[key] = p
            self._by_subject[p.subject].append(key)
            for c in p.concepts():
                self._by_concept[c].append(key)
        else:
            # Renforcer la confiance si vue plusieurs fois
            self._props[key].confidence = min(1.0,
                self._props[key].confidence + 0.05)

    # ── Extraction principale ─────────────────────────────────────────────────
    def extract_from_book(self, text: str, source: str = "book",
                          max_props: int = 400) -> Dict[str, Any]:
        """
        Extrait les propositions d'un livre entier.
        Appelé par load_pdf_book dans le core.
        """
        nlp = _get_nlp()
        if nlp is not None:
            props = self._spacy_p.extract(text[:80000], source, nlp)
        else:
            # Traitement par phrases pour le parseur léger
            sentences = re.split(r"[.!?]\s+", text[:40000])
            props = []
            for sent in sentences[:500]:
                props.extend(self._light.extract(sent, source))

        # Filtrer et dédupliquer
        new_count = 0
        for p in props[:max_props]:
            if (p.subject and p.object and
                    len(p.subject) > 2 and len(p.object) > 2 and
                    p.subject not in _STOP and p.object not in _STOP):
                self._store_prop(p)
                new_count += 1

        self._save()
        return {
            "extracted":    new_count,
            "total_stored": len(self._props),
            "source":       source,
            "oppositions":  sum(1 for p in props if p.connector_type == "opposition"),
            "causals":      sum(1 for p in props if p.connector_type == "causal"),
        }

    def extract_from_text(self, text: str, source: str = "exchange") -> List[Dict]:
        """Extraction légère depuis un échange ou une phrase."""
        nlp = _get_nlp()
        if nlp is not None:
            props = self._spacy_p.extract(text[:2000], source, nlp)
        else:
            props = self._light.extract(text, source)
        for p in props[:20]:
            self._store_prop(p)
        return [p.to_dict() for p in props[:10]]

    # ── Requêtes ──────────────────────────────────────────────────────────────
    def query_concept(self, concept: str, top_k: int = 8) -> List[Dict[str, Any]]:
        """Toutes les propositions impliquant un concept."""
        concept = concept.strip().lower()
        keys = self._by_concept.get(concept, [])[:top_k]
        return [self._props[k].to_dict() for k in keys if k in self._props]

    def query_relation(self, concept_a: str, concept_b: str) -> Optional[Dict]:
        """Cherche une proposition reliant deux concepts."""
        ca, cb = concept_a.lower(), concept_b.lower()
        for key, p in self._props.items():
            if ((p.subject == ca and p.object == cb) or
                    (p.subject == cb and p.object == ca)):
                return p.to_dict()
        return None

    def get_theses(self, source: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Les propositions les plus confiantes d'un livre donné."""
        props = [p for p in self._props.values() if p.source == source]
        props.sort(key=lambda p: p.confidence, reverse=True)
        return [p.to_dict() for p in props[:top_k]]

    def get_oppositions(self, source: str = "") -> List[Dict[str, Any]]:
        """Propositions d'opposition — tensions potentielles."""
        props = [p for p in self._props.values()
                 if p.connector_type == "opposition"
                 and (not source or p.source == source)]
        return [p.to_dict() for p in props[:15]]

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, user_input: str = "", focus_concepts: List[str] = None) -> Dict[str, Any]:
        """Interface standard."""
        focus_concepts = focus_concepts or []
        if not self._props:
            return {"available": False, "propositions": [], "count": 0}

        relevant_props = []
        # Propositions liées aux concepts focus
        for c in focus_concepts[:4]:
            relevant_props.extend(self.query_concept(c, top_k=3))

        # Compléter avec propositions du message utilisateur
        if user_input:
            words = [w for w in re.findall(r"[\wÀ-ÿ']{4,}", user_input.lower())
                     if w not in _STOP]
            for w in words[:5]:
                relevant_props.extend(self.query_concept(w, top_k=2))

        # Dédupliquer
        seen: Set[str] = set()
        unique = []
        for p in relevant_props:
            k = f"{p.get('subject','')}|{p.get('relation','')}|{p.get('object','')}"
            if k not in seen:
                seen.add(k)
                unique.append(p)

        # Récupérer les propositions les plus fortes
        high_conf = sorted(
            [p.to_dict() for p in self._props.values()],
            key=lambda d: d.get("confidence",0), reverse=True
        )[:5]

        return {
            "available":     True,
            "propositions":  unique[:8],
            "high_confidence": high_conf,
            "oppositions":   self.get_oppositions()[:3],
            "count":         len(self._props),
        }

    def snapshot(self) -> Dict[str, Any]:
        opp = sum(1 for p in self._props.values() if p.connector_type == "opposition")
        return {
            "total_propositions": len(self._props),
            "oppositions":        opp,
            "subjects":           len(self._by_subject),
        }